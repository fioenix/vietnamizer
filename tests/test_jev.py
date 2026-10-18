from __future__ import annotations

import copy
import importlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def response(payload):
    answers = {}
    for name, q in payload['questions'].items():
        if q['type'] == 'noul':
            answers[name] = {'type': 'noul', 'noul': 0.1}
        elif q['type'] == 'choice':
            keys = list(q['criteria'])
            answers[name] = {'type': 'choice', 'choice': keys[0], 'confidence': 1.0,
                             'probabilities': {k: float(k == keys[0]) for k in keys}}
        else:
            keys = [str(i) for i in range(len(q['criteria']))]
            answers[name] = {'type': 'score', 'score': 0.0, 'confidence': 1.0,
                             'legend': dict(enumerate(q['criteria'])),
                             'probabilities': {k: float(k == '0') for k in keys}}
    return {'model': 'jev-1.14.0', 'answers': answers,
            'usage': {'input_tokens': 12, 'output_tokens': 4}}


class JevTest(unittest.TestCase):
    def setUp(self):
        try:
            self.core = importlib.import_module('jev.core')
        except ImportError:
            self.fail('Jev runner is missing: automatic/offline behavior is not implemented')
        self.doc = {'transmission_allowed': True, 'context_review': {'reviewed':True,'unresolved':[]}, 'sections': [
            {'id': 'p1', 'profile': 'blog', 'kind': 'prose',
             'text': 'Tao hiểu. Mày cứ làm đi.', 'context': ['Đây là trao đổi công việc.']}]}
        self.calls = []

    def evaluate(self, document=None, environ=None, transport=None, **kwargs):
        def fake(payload, key, timeout):
            self.calls.append(copy.deepcopy(payload))
            self.assertEqual(key, 'test-key')
            self.assertGreater(timeout, 0)
            self.assertLessEqual(timeout, 15)
            return response(payload)
        return self.core.evaluate(document or self.doc,
                                  environ={'TYPESAFE_API_KEY': 'test-key'} if environ is None else environ,
                                  transport=transport or fake, **kwargs)

    def test_no_key_makes_zero_network_calls_even_without_document(self):
        for env in ({}, {'TYPESAFE_API_KEY': ' \t'}):
            result = self.core.evaluate(None, environ=env,
                transport=lambda *_: self.fail('network used without key'))
            self.assertEqual(result['status'], 'key_absent')

    def test_denied_transmission_sends_nothing(self):
        self.doc['transmission_allowed'] = False
        self.assertEqual(self.evaluate()['status'], 'permission_denied')
        self.assertEqual(self.calls, [])

    def test_blog_coverage_full_paragraph_and_no_raw_output(self):
        result = self.evaluate()
        self.assertEqual(result['status'], 'evaluated')
        self.assertEqual(len(result['coverage']), 55)
        self.assertTrue(all(e['status'] == 'excluded' for e in result['coverage'] if e['pattern'].startswith('K')))
        self.assertTrue(any(e['pattern'] == 'V20' and e['status'] == 'jev_evaluated' for e in result['coverage']))
        self.assertEqual(self.calls[0]['state']['paragraph'], self.doc['sections'][0]['text'])
        self.assertEqual([c['text'] for c in self.calls[0]['state']['related_paragraphs']], ['Đây là trao đổi công việc.'])
        self.assertNotIn('Tao hiểu', json.dumps(result, ensure_ascii=False))
        self.assertNotIn('test-key', json.dumps(result))
        self.assertTrue(result['judgments'])

    def test_typography_only_excludes_semantic_prose_profiles(self):
        self.doc['sections'][0]['profile'] = 'typography-only'
        result = self.evaluate()
        self.assertTrue(all(e['status'] == 'excluded' for e in result['coverage'] if not e['pattern'].startswith('T')))
        self.assertTrue(any(e['pattern'] == 'T3' and e['status'] == 'mechanically_checked' for e in result['coverage']))

    def test_protected_span_and_context_are_not_exported(self):
        self.doc['sections'][0]['text'] = 'Code: PRIVATE. Tao hiểu.'
        self.doc['sections'][0]['protected_spans'] = [{'start': 6, 'end': 13}]
        result = self.evaluate()
        self.assertNotIn('PRIVATE', json.dumps(self.calls))
        self.assertEqual(result['status'], 'evaluated')

    def test_protected_section_no_network(self):
        self.doc['sections'][0]['kind'] = 'protected'
        result = self.evaluate()
        self.assertEqual(self.calls, [])
        self.assertTrue(all(e['status'] == 'excluded' for e in result['coverage']))

    def test_invalid_response_diagnostic_is_bounded_and_sanitized(self):
        def invalid(payload, *_):
            r=response(payload)
            r['answers']['PRIVATE']=r['answers'].pop(next(iter(payload['questions'])))
            return r
        r=self.evaluate(transport=invalid,only_pattern='V20')
        self.assertEqual(r['receipts'][0]['validation_error'], {'reason':'answer_ids'})
        self.assertNotIn('PRIVATE',json.dumps(r))

    def test_wrong_model_is_invalid_not_pass(self):
        def fake(payload, *_):
            r = response(payload); r['model'] = 'jev-1.13.0'; return r
        result = self.evaluate(transport=fake)
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(result['judgments'], [])
        self.assertTrue(any(e['status'] == 'invalid_response' for e in result['coverage']))

    def test_nan_extra_ids_and_untrusted_echo_are_rejected(self):
        for mutation in ('nan', 'extra', 'wrong_type', 'bad_score', 'bool_usage'):
            def fake(payload, *_, mutation=mutation):
                r = response(payload); k = next(iter(r['answers']))
                if mutation == 'nan': r['answers'][k] = {'type': 'noul', 'noul': float('nan')}
                if mutation == 'extra': r['answers']['echo-PRIVATE'] = {'type': 'noul', 'noul': .5}
                if mutation == 'wrong_type': r['answers'][k]['type'] = 'box'
                if mutation == 'bad_score':
                    for v in r['answers'].values():
                        if v['type'] == 'score': v['score'] = 99
                if mutation == 'bool_usage': r['usage']['input_tokens'] = True
                return r
            result = self.evaluate(transport=fake)
            self.assertEqual(result['status'], 'incomplete', mutation)
            self.assertNotIn('PRIVATE', json.dumps(result))

    def test_failure_echo_is_not_returned_and_has_no_retry(self):
        calls = []
        def broken(*_):
            calls.append(1); raise RuntimeError('test-key PRIVATE')
        r = self.evaluate(transport=broken)
        self.assertEqual(r['status'], 'incomplete')
        self.assertEqual(len(calls), 1)
        self.assertNotIn('PRIVATE', json.dumps(r))

    def test_candidates_separate_guards_and_protected_edit_blocked(self):
        section = self.doc['sections'][0]
        section['candidates'] = [
            {'id': 'e1', 'start': 0, 'end': 8, 'replacement': 'Tao đã hiểu.'},
            {'id': 'e2', 'start': 0, 'end': 8, 'replacement': 'Tao hiểu rồi.'}]
        r = self.evaluate()
        keys = {k for c in self.calls for k in c['questions']}
        self.assertIn('edit_e1_meaning', keys)
        self.assertIn('edit_e2_meaning', keys)
        self.assertIn('edit_e1_improvement', keys)
        self.assertNotIn('auto_accept', json.dumps(r))
        section['protected_spans'] = [{'start': 0, 'end': 8}]
        self.calls.clear()
        self.assertEqual(self.evaluate()['status'], 'invalid_input')
        self.assertEqual(self.calls, [])

    def test_invalid_spans_profiles_and_duplicate_ids_do_not_send(self):
        for change in ('profile', 'span', 'duplicate', 'permission_type'):
            doc = copy.deepcopy(self.doc)
            if change == 'profile': doc['sections'][0]['profile'] = 'unknown'
            if change == 'span': doc['sections'][0]['protected_spans'] = [{'start': 99, 'end': 100}]
            if change == 'duplicate': doc['sections'].append(copy.deepcopy(doc['sections'][0]))
            if change == 'permission_type': doc['transmission_allowed'] = 'true'
            self.calls.clear()
            self.assertIn(self.evaluate(doc)['status'], ('invalid_input', 'permission_denied'))
            self.assertEqual(self.calls, [])

    def test_oversized_state_has_explicit_unattempted_coverage(self):
        self.doc['sections'][0]['text'] = 'x' * 49000
        r = self.evaluate()
        self.assertEqual(r['status'], 'incomplete')
        self.assertEqual(self.calls, [])
        self.assertTrue(any(e['status'] == 'context_too_large' for e in r['coverage']))

    def test_registry_covers_exact_ids_and_canonical_exclusions(self):
        registry = self.core.load_registry()
        expected = {f'{p}{i}' for p, n in [('V', 25), ('T', 6), ('B', 17), ('K', 7)] for i in range(1, n+1)}
        self.assertEqual({x['id'] for x in registry}, expected)
        self.assertEqual(len(registry), 55)
        for entry in registry:
            self.assertTrue(entry['no_flag'])
            self.assertTrue(entry['questions'] or entry['mode'] == 'mechanical')

    def test_mechanical_quotes_report_unbalanced_straight_pairs(self):
        self.doc['sections'][0]['text'] = 'Một dấu " bị thiếu cặp.'
        r = self.evaluate(only_pattern='T3')
        self.assertEqual(self.calls, [])
        self.assertIn({'kind': 'unbalanced_straight_quotes'}, r['coverage'][0]['findings'])

    def test_request_budget_keeps_unattempted_checks_visible(self):
        self.doc['sections'] = [dict(self.doc['sections'][0], id=f'p{i}') for i in range(32)]
        r = self.evaluate()
        self.assertEqual(len(self.calls), 32)
        self.assertEqual(r['status'], 'incomplete')
        self.assertEqual(len(r['coverage']), 1760)
        self.assertTrue(any(e['status'] == 'limit_exceeded' for e in r['coverage']))

    def test_protected_substring_is_redacted_from_related_context(self):
        section = self.doc['sections'][0]
        section['text'] = 'Code: PRIVATE. Tao hiểu.'
        section['protected_spans'] = [{'start': 6, 'end': 13}]
        section['context'] = ['PRIVATE is also mentioned here.']
        self.evaluate()
        self.assertNotIn('PRIVATE', json.dumps(self.calls))

    def test_single_pattern_does_not_claim_full_coverage(self):
        r = self.evaluate(only_pattern='V20')
        self.assertEqual(r['coverage_mode'], 'single_pattern')
        self.assertEqual({e['pattern'] for e in r['coverage']}, {'V20'})

    def test_fully_protected_spans_exclude_default_target(self):
        section = self.doc['sections'][0]
        section['text'] = ' PRIVATE '
        section['protected_spans'] = [{'start': 1, 'end': 8}]
        r = self.evaluate()
        self.assertEqual(self.calls, [])
        self.assertTrue(all(e['status'] == 'excluded' for e in r['coverage']))

    def test_t3_checks_document_scope_and_allows_nested_quotes(self):
        self.doc['sections'][0]['text'] = 'Một “cụm từ”.'
        self.doc['sections'].append(dict(self.doc['sections'][0], id='p2', text='Một "cụm khác".'))
        r = self.evaluate(only_pattern='T3')
        self.assertIn({'kind': 'mixed_quote_styles'}, r['coverage'][0]['findings'])
        self.doc['sections'] = [dict(self.doc['sections'][0], text='Cô nói: “Từ "nhà" ở đây đúng.”')]
        r = self.evaluate(only_pattern='T3')
        self.assertEqual(r['coverage'][0]['findings'], [])

    def test_late_response_cannot_supply_judgments(self):
        ticks = [0.0]
        def late(payload, *_):
            ticks[0] += 16
            return response(payload)
        with patch('jev.core.time.monotonic', side_effect=lambda: ticks[0]):
            r = self.evaluate(transport=late, only_pattern='V20')
        self.assertEqual(r['status'], 'incomplete')
        self.assertEqual(r['judgments'], [])
        self.assertEqual(r['receipts'][0]['status'], 'deadline_exceeded')

    def test_every_score_has_sufficiency_and_is_ignored_when_insufficient(self):
        for pattern in self.core.load_registry():
            if any(q['type'] == 'score' for q in pattern['questions']):
                self.assertTrue(any(q['key'] == 'evidence' and 'insufficient' in q['criteria']
                                    for q in pattern['questions']), pattern['id'])
        def insufficient(payload, *_):
            r = response(payload)
            for key, q in payload['questions'].items():
                if key.endswith('_evidence'):
                    r['answers'][key].update(choice='insufficient', probabilities={k:float(k=='insufficient') for k in q['criteria']})
            return r
        r = self.evaluate(only_pattern='V9', transport=insufficient)
        score = next(j for j in r['judgments'] if j['answer']['type'] == 'score')
        self.assertEqual(score['disposition'], 'ignore_insufficient_context')
        self.assertIn('probabilities', score['answer'])

    def test_overlap_redaction_and_derived_targets_do_not_leak(self):
        section=self.doc['sections'][0]
        section.update(text='call ABCD EFG HIJ now',protected_spans=[{'start':5,'end':17}],
                       targets=[{'id':'s1','start':0,'end':14}])
        section['context']=['call ABCD EFG HIJ now']
        self.doc['sections'].append({'id':'p2','profile':'blog','kind':'protected','text':'call ABCD EFG'})
        self.evaluate(only_pattern='V20')
        self.assertTrue(self.calls)
        wire=json.dumps(self.calls)
        self.assertNotIn('HIJ',wire)
        self.assertNotIn('ABCD',wire)
        self.assertNotIn('EFG',wire)

    def test_short_protected_tokens_do_not_corrupt_prose_or_placeholders(self):
        section=self.doc['sections'][0]
        section.update(text='SECRET E; rà và rà soát',protected_spans=[{'start':0,'end':6},{'start':7,'end':8},{'start':10,'end':12}])
        self.evaluate(only_pattern='V20')
        state=self.calls[0]['state']
        self.assertEqual(state['paragraph'],'[PROTECTED] [PROTECTED]; [PROTECTED] và rà soát')
        self.assertEqual(state['register'],'Preserve the supplied text’s register.')

    def test_protected_targets_do_not_suppress_paragraph_and_document_checks(self):
        section=self.doc['sections'][0]
        section.update(text='An nói thiếu rõ ràng.',protected_spans=[{'start':0,'end':2}],targets=[{'id':'s1','start':0,'end':2}])
        result=self.evaluate()
        coverage={e['pattern']:e for e in result['coverage']}
        self.assertEqual(coverage['V20']['status'],'jev_evaluated') # full mode fills uncovered sentence
        self.assertEqual(coverage['V13']['status'],'jev_evaluated')
        self.assertEqual(coverage['T3']['status'],'mechanically_checked')

    def test_t3_mismatched_low_and_cross_paragraph_quotes_are_visible(self):
        for text in ('Câu 1: “Xin chào". Câu 2: "Tạm biệt”.','„Xin chào" và „tạm biệt"','Mở “câu\nMột "câu khác".'):
            with self.subTest(text=text):
                self.assertTrue(self.core.mechanical(text))
        self.assertEqual(self.core.mechanical('Cô nói: “Từ "nhà" ở đây đúng.”'),[])

    def test_elapsed_deadline_between_sections_is_not_size_limit(self):
        self.doc['sections'].append(dict(self.doc['sections'][0],id='p2'))
        ticks=[0.0]
        def advance(payload,*_):
            ticks[0]+=121
            return response(payload)
        with patch('jev.core.time.monotonic',side_effect=lambda:ticks[0]):
            result=self.evaluate(only_pattern='V20',transport=advance)
        self.assertTrue(any(e['status']=='deadline_exceeded' for e in result['coverage']))

    def test_candidate_revised_paragraph_masks_inserted_protected_values(self):
        section=self.doc['sections'][0];text='Mã ABC123 hết hạn.'
        section.update(text=text,protected_spans=[{'start':3,'end':9}],candidates=[{'id':'e_1','start':text.index('hết'),'end':len(text)-1,'replacement':'ABC123 hết hạn'}])
        self.evaluate(only_pattern='V20')
        self.assertNotIn('ABC123',json.dumps(self.calls))

    def test_partial_candidate_judgment_carries_actual_review_status(self):
        self.doc['sections'][0]['candidates']=[{'id':'e_1','start':0,'end':8,'replacement':'Tao hiểu rồi.'}]
        seen=[]
        def fail_second_guard(payload,*_):
            seen.append(payload);r=response(payload)
            if any(k.endswith('_new_claim') and k.startswith('edit_') for k in payload['questions']):r['model']='wrong'
            return r
        with patch('jev.core.MAX_QUESTIONS',1):
            result=self.evaluate(only_pattern='V20',transport=fail_second_guard)
        candidate=next(j for j in result['judgments'] if j['check'].startswith('edit_'))
        self.assertEqual(candidate['coverage_status'],'invalid_response')

    def test_related_context_preserves_preexisting_mask_markers(self):
        self.doc['sections'][0].update(text='E là biến.',protected_spans=[{'start':0,'end':1}],context=['Đã che [PROTECTED].'])
        self.evaluate(only_pattern='V20')
        self.assertEqual([c['text'] for c in self.calls[0]['state']['related_paragraphs']],['Đã che [PROTECTED].'])

    def test_protected_value_enclosing_a_marker_is_still_masked(self):
        secret='Token: [PROTECTED] abc123'
        section=self.doc['sections'][0]
        section.update(text=secret+'; cứ làm đi.',protected_spans=[{'start':0,'end':len(secret)}],context=[secret],
                       candidates=[{'id':'e1','start':len(secret)+2,'end':len(secret)+4,'replacement':secret}])
        self.evaluate(only_pattern='V20')
        self.assertTrue(self.calls)
        self.assertNotIn('abc123',json.dumps(self.calls))

    def test_cli_no_key_works_without_input(self):
        env = {k: v for k, v in os.environ.items() if k != 'TYPESAFE_API_KEY'}
        run = subprocess.run([sys.executable, '-B', '-m', 'jev', 'evaluate'], cwd=ROOT,
                             env=env, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)['status'], 'key_absent')


if __name__ == '__main__':
    unittest.main()
