import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from benchmarks import public_human as h


def binding():
    forms = {}
    for wi, who in enumerate('AB'):
        groups = []
        for n in range(20):
            first = 1000 + wi * 1000 + n * 8
            cid = f'R{(n if who == "A" else 19-n)+1:03}'
            groups.append({'id': f'Q{n+1:03}', 'page': first,
                           'page_title': 'Page', 'page_help': '',
                           'images': {l: {'item_id': first+1+i,
                                         'provider_sha256': hashlib.sha256(bytes([1, 2, 3])).hexdigest()}
                                      for i, l in enumerate('ABCD')},
                           'preservation': first+5, 'readability': first+6, 'notes': first+7,
                           'assignments': {l: {'source_case_id': cid, 'arm': arm}
                                           for l, arm in zip('ABCD', h.ARMS)}})
        forms[who] = {'form_id': 'form-'+who, 'contract_digest': 'contract-'+who,
                      'groups': groups, 'item_ids': list(range(1000+wi*1000, 1160+wi*1000)),
                      'responder_url': 'https://example.test/'+who}
    return {'schema': h.BINDING_SCHEMA, 'cohort': 'fixture', 'is_fixture': True,
            'source_ids': [f'R{n+1:03}' for n in range(20)], 'arms': list(h.ARMS),
            'questions': h.QUESTIONS, 'forms': forms,
            'analysis': {'bootstrap_draws': 10000, 'seed': 25033}}


def packet(b, who, response_ids=('one',)):
    answers = []
    for g in b['forms'][who]['groups']:
        answers += [{'item_id': g['preservation'], 'response': ['Giữ đúng']*4},
                    {'item_id': g['readability'], 'response': ['Tương đương']*4},
                    {'item_id': g['notes'], 'response': 'Không có'}]
    return {'schema': h.EXPORT_SCHEMA, 'binding_digest': h.digest(b), 'reviewer': who,
            'form_id': b['forms'][who]['form_id'], 'audit_complete': True, 'is_fixture': True,
            'responses': [{'id': i, 'timestamp': '2026-10-26T00:00:00.000Z',
                           'answers': copy.deepcopy(answers)} for i in response_ids]}


class PublicHumanTests(unittest.TestCase):
    def test_before_after_rates_are_original_relative_and_source_clustered(self):
        b=binding(); exports={w:packet(b,w) for w in 'AB'}
        # One source improves only for A; B's reversed order maps the same source.
        exports['A']['responses'][0]['answers'][1]['response'][2]='Tự nhiên, rõ ràng hơn'
        r=h.analyze(b,exports,{'A':'one','B':'one'},test_data=True)
        rows=[x for x in r['before_after'] if x['arm']=='vietnamizer' and x['metric']=='better']
        by={x['reviewer']:x for x in rows}
        self.assertAlmostEqual(by['A']['estimate'],1/20)
        self.assertEqual(by['B']['estimate'],0)
        self.assertAlmostEqual(by['pooled']['estimate'],1/40)
        self.assertEqual(by['pooled']['n_sources'],20)
        self.assertEqual(by['pooled']['reference'],'original')
        self.assertTrue(by['pooled']['primary'])
        self.assertTrue(all(not x['primary'] for x in r['comparisons']))
        self.assertEqual(r['study_design']['runtime'],'Codex gpt-6.1-sol / medium')

    def test_before_after_missing_uncertain_are_not_failures_and_small_n_has_no_ci(self):
        b=binding(); exports={w:packet(b,w) for w in 'AB'}
        for w,p in exports.items():
            for n in range(20):
                p['responses'][0]['answers'][n*3+1]['response'][2]='Chưa rõ'
        # Only source R001 is determinate for both; other source R002 missing for A.
        exports['A']['responses'][0]['answers'][1]['response'][2]='Khó đọc hơn'
        exports['B']['responses'][0]['answers'][19*3+1]['response'][2]='Tự nhiên, rõ ràng hơn'
        exports['A']['responses'][0]['answers'][4]['response'][2]=''
        r=h.analyze(b,exports,{'A':'one','B':'one'},test_data=True)
        row=next(x for x in r['before_after'] if x['arm']=='vietnamizer' and x['metric']=='better' and x['reviewer']=='pooled')
        self.assertEqual(row['estimate'],.5)
        self.assertEqual(row['n_sources'],1)
        self.assertIsNone(row['low'])
        self.assertEqual(row['excluded_sources'],19)
        self.assertEqual(row['excluded_missing'],1)
        self.assertEqual(row['excluded_uncertain'],19)
        self.assertTrue(row['exclusion_counts_may_overlap'])

    def test_provider_records_cannot_substitute_canonical_context_or_image(self):
        b = binding(); groups = copy.deepcopy(b['forms']['A']['groups']); contract={'groups':[]}; images={}; key={}
        for g in groups:
            g['who']='A';g['page_title']='Đoạn '+g['id'][1:]+' · Đánh giá bốn bản sửa'
            g['page_help']='Người đọc: Reader\nMục đích: Edit'
            contract['groups'].append({'id':g['id'],'audience':'Reader','purpose':'Edit'})
            images[g['id']]={l:{'sha256':'canonical-'+l} for l in 'ABCD'}
            key[g['id']]=g['assignments']
            for l in 'ABCD':g['images'][l]['input_sha256']='canonical-'+l
        self.assertEqual(len(h.bind_groups(groups,contract,images,key,'A')),20)
        for change in (lambda g:g[0].update(who='B'),lambda g:g[0].update(page_help='Different source'),
                       lambda g:g[0]['images']['A'].update(input_sha256='foreign'),lambda g:g.reverse()):
            wrong=copy.deepcopy(groups);change(wrong)
            with self.assertRaises(ValueError):h.bind_groups(wrong,contract,images,key,'A')

    def test_source_pairing_uses_private_key_not_display_order(self):
        b = binding(); exports = {w: packet(b, w) for w in 'AB'}
        result = h.analyze(b, exports, {'A': 'one', 'B': 'one'}, test_data=True)
        self.assertEqual(len(result['rows']), 160)
        self.assertEqual(result['rows'][0]['source_id'], 'R001')
        self.assertEqual(next(r for r in result['rows'] if r['reviewer']=='B')['source_id'], 'R020')
        self.assertEqual(result['status'], 'synthetic_test_only')

    def test_no_auto_select_even_one_response(self):
        b = binding()
        result = h.analyze(b, {'A': packet(b, 'A'), 'B': packet(b, 'B')}, {}, test_data=True)
        self.assertEqual(result['status'], 'selection_required')
        self.assertEqual(result['rows'], [])

    def test_duplicate_response_selection_and_unknown_answer_rejected(self):
        b = binding(); p = packet(b, 'A', ('one', 'two'))
        h.validate_export(b, p)
        p['responses'].append(copy.deepcopy(p['responses'][0]))
        with self.assertRaises(ValueError): h.validate_export(b, p)
        p = packet(b, 'A'); p['responses'][0]['answers'][0]['response'][0] = 'AI invented label'
        with self.assertRaises(ValueError): h.analyze(b, {'A':p, 'B':packet(b,'B')}, {'A':'one','B':'one'}, test_data=True)

    def test_wrong_form_item_cohort_and_grid_cardinality_rejected(self):
        for mutate in (lambda p:p.update(form_id='wrong'),
                       lambda p:p.update(binding_digest='wrong'),
                       lambda p:p['responses'][0]['answers'].append({'item_id':999999, 'response':'x'}),
                       lambda p:p['responses'][0]['answers'][1].update(response=['Tương đương'])):
            b = binding(); p = packet(b,'A'); mutate(p)
            with self.assertRaises(ValueError): h.analyze(b, {'A':p,'B':packet(b,'B')}, {'A':'one','B':'one'}, test_data=True)

    def test_fixture_cannot_be_mixed_or_reported_as_real(self):
        b = binding()
        with self.assertRaises(ValueError): h.analyze(b, {'A':packet(b,'A'),'B':packet(b,'B')}, {'A':'one','B':'one'})
        p = packet(b,'B'); p['is_fixture'] = False
        with self.assertRaises(ValueError): h.analyze(b, {'A':packet(b,'A'),'B':p}, {'A':'one','B':'one'}, test_data=True)

    def test_missing_uncertain_are_separate_and_exclude_whole_pooled_source(self):
        b = binding(); exports = {w:packet(b,w) for w in 'AB'}
        # R001, ordinary is missing in A; R002, Vietnamizer uncertain in B.
        exports['A']['responses'][0]['answers'][1]['response'][1] = ''
        bg = b['forms']['B']['groups'][18]
        row = next(a for a in exports['B']['responses'][0]['answers'] if a['item_id']==bg['readability'])
        row['response'][2] = 'Chưa rõ'
        r = h.analyze(b,exports,{'A':'one','B':'one'},test_data=True)
        c = next(x for x in r['comparisons'] if x['a']=='vietnamizer' and x['b']=='ordinary' and x['metric']=='better' and x['reviewer']=='pooled')
        self.assertEqual((c['n_sources'], c['excluded_sources']), (18, 2))
        self.assertEqual(c['excluded_missing'], 1)
        self.assertEqual(c['excluded_uncertain'], 1)
        rate = next(x for x in r['rates'] if x['reviewer']=='A' and x['arm']=='ordinary' and x['dimension']=='readability')
        self.assertEqual((rate['counts']['missing'], rate['determinate']), (1,19))

    def test_known_bootstrap_oracles_and_determinism(self):
        self.assertEqual(h.cluster_interval([1,1], draws=100), {'estimate':1.0,'low':1.0,'high':1.0,'n_sources':2,'degenerate':True})
        self.assertEqual(h.cluster_interval([],draws=100)['estimate'], None)
        self.assertEqual(h.cluster_interval([.5],draws=100)['low'], None)
        self.assertEqual(h.cluster_interval([-1,1],draws=10000), h.cluster_interval([-1,1],draws=10000))
        ci = h.cluster_interval([-1,1],draws=10000)
        self.assertEqual((ci['estimate'],ci['low'],ci['high']), (0.0,-1.0,1.0))

    def test_agreement_degenerate_marginals_and_uncertainty(self):
        r = h.agreement([('preserved','preserved')]*80, ['preserved','changed','uncertain','missing'])
        self.assertEqual(r['exact_agreement'],1)
        self.assertIsNone(r['kappa'])
        r = h.agreement([('uncertain','uncertain'),('missing','changed')], ['preserved','changed','uncertain','missing'])
        self.assertEqual(r['determinate_pairs'],0)
        self.assertEqual(r['missing_pairs'],1)
        self.assertEqual(r['uncertain_pairs'],1)
        self.assertIsNone(r['exact_agreement'])

    def test_utf8_chunks_complete_digest_and_duplicate_guard(self):
        b = binding(); p = packet(b,'A'); p['responses'][0]['answers'][2]['response'] = 'Tiếng Việt 👋\n'*3000
        log = h.test_log(p)
        self.assertEqual(h.parse_export_log(log,b),p)
        for corrupt in (log.rsplit('\n',2)[0], log+log.splitlines()[0]+'\n', log.replace('Tiếng','Sai',1)):
            with self.assertRaises(ValueError): h.parse_export_log(corrupt,b)

    def test_empty_actual_readiness_no_quality_charts_or_zero_success(self):
        b = binding(); b['is_fixture'] = False
        r = h.analyze(b,{}, {})
        self.assertEqual(r['status'],'awaiting_human')
        self.assertEqual(r['rows'],[])
        self.assertEqual(r['human_labels_imported'],0)
        self.assertFalse(r['quality_chart_allowed'])

    def test_two_empty_selected_submissions_still_have_no_quality_labels(self):
        b = binding(); exports = {w:packet(b,w) for w in 'AB'}
        for p in exports.values(): p['responses'][0]['answers'] = []
        r = h.analyze(b,exports,{'A':'one','B':'one'},test_data=True)
        self.assertFalse(r['quality_chart_allowed'])
        self.assertEqual(r['categorical_labels_observed'],0)
        self.assertTrue(all(x['counts']['missing']==20 for x in r['rates']))

    def test_exporter_roundtrip_and_live_schema_drift_guards(self):
        import subprocess
        b = binding(); job = {'reviewer':'A','binding_digest':h.digest(b),'cohort':b['cohort'],
                              'is_fixture':True,'ui_revision':'no-background-v2','questions':h.QUESTIONS,
                              **b['forms']['A']}
        source = Path(h.__file__).with_suffix('.gs').read_text().replace('/*__EXPORT_JOB__*/',json.dumps(job,ensure_ascii=False))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'export.gs'; path.write_text(source)
            run = subprocess.run(['node',str(Path(__file__).with_name('public_human_export.cjs')),str(path)],capture_output=True,text=True,check=True)
            result = h.parse_export_log(run.stdout,b)
            self.assertEqual(len(result['responses']),1)
            self.assertIn('Tiếng Việt 👋', result['responses'][0]['answers'][2]['response'])

    def test_immutable_output_and_csv_formula_escape(self):
        b = binding(); r = h.analyze(b,{}, {},test_data=True)
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder)/'report'; h.write_report(out,r,{}, {})
            with self.assertRaises(FileExistsError): h.write_report(out,r,{}, {})
            h.csv_file(Path(folder)/'notes.csv',[{'note':' =HYPERLINK("x")','number':-.2}])
            text = (Path(folder)/'notes.csv').read_text()
            self.assertIn("' =HYPERLINK", text)
            self.assertIn(',-0.2',text)

    def test_selected_report_writes_both_categorical_vocabularies(self):
        import csv
        b=binding();exports={w:packet(b,w) for w in 'AB'}
        r=h.analyze(b,exports,{'A':'one','B':'one'},test_data=True)
        with tempfile.TemporaryDirectory() as folder:
            out=Path(folder)/'report';h.write_report(out,r,exports,{'A':'one','B':'one'})
            with (out/'label-counts.csv').open() as f: rows=list(csv.DictReader(f))
            self.assertEqual(len(rows),16)
            self.assertEqual({x['dimension'] for x in rows},{'readability','preservation'})
            self.assertIn('better',rows[0]);self.assertIn('preserved',rows[0])


if __name__ == '__main__': unittest.main()
