"""Parent-verified regressions from independent Claude/Antigravity reviews."""
import copy
import unittest
from unittest.mock import patch
from jev import core
from jev.preparation import prepare_document, _safe
from tests.test_coverage import EvaluationCase,raw
from tests.test_jev import response

class ExternalReviewTest(EvaluationCase):
    def test_missing_evidence_and_too_large_state_are_not_context_complete(self):
        with patch('jev.core.MAX_QUESTIONS',1),patch('jev.core.MAX_REQUESTS',1):
            r=self.evaluate(raw('Tôi về.'),only_pattern='V9')
        self.assertFalse(r['context_complete'])
        self.assertFalse(r['sentences'][0]['context_complete'])
        r=self.evaluate(raw('a'*49000),only_pattern='V1')
        self.assertFalse(r['context_complete'])
    def test_mechanical_only_does_not_skip_context_review(self):
        d=raw('Tôi về.');d.pop('context_review')
        r=self.evaluate(d,only_pattern='T3')
        self.assertFalse(r['context_complete'])
    def test_selected_requires_targets_and_never_schedules_other_units(self):
        self.assertEqual(self.evaluate(raw(),scope='selected')['status'],'invalid_input')
        d={'transmission_allowed':True,'context_review':{'reviewed':True,'unresolved':[]},'sections':[
            {'id':'title','kind':'heading','profile':'blog','text':'Tiêu đề'},
            {'id':'p','kind':'prose','profile':'blog','text':'Tôi về.','targets':[{'id':'x','start':0,'end':7}]}]}
        r=self.evaluate(d,scope='selected',only_pattern='V1')
        self.assertEqual(r['status'],'evaluated')
        self.assertEqual({e['section'] for e in r['coverage']},{'p'})
        self.assertTrue(all(p['state']['paragraph']=='Tôi về.' for p in self.calls))
    def test_unknown_work_is_not_a_protected_exclusion(self):
        d=raw('x\n'*5000)
        r=self.evaluate(d)
        self.assertFalse(r['all_excluded'])
        self.assertFalse(r['context_complete'])
    def test_code_fence_annotation_cannot_make_it_editable(self):
        text='Chạy lệnh sau.\n```\nexport TOKEN=SECRET_FENCE\n```\nXong.'
        for annotation in ([{'start':0,'end':len(text),'paragraph':True}],
                           [{'start':text.index('```'),'end':text.rindex('```')+3,'kind':'prose'}]):
            d=raw(text);d['source']['layout']='markdown';d['annotations']=annotation
            r=self.evaluate(d,only_pattern='V1')
            self.assertNotIn('SECRET_FENCE',str(self.calls))
            self.assertIn(r['status'],('invalid_input','incomplete','evaluated'))
    def test_markdown_code_runs_softwrap_and_unclosed_are_opaque(self):
        for text in ('Dùng ``SECRET_A. Giá trị `x`` trong câu. Câu hai.',
                     'Dùng `ls\n-la SECRET_B` rồi về.',
                     'Dùng `SECRET_C. Rồi về.'):
            with self.subTest(text=text):
                d=raw(text);d['source']['layout']='markdown'
                r=self.evaluate(d,only_pattern='V1')
                self.assertNotIn('SECRET_',str(self.calls))
                if text.endswith('Rồi về.'):self.assertFalse(r['segmentation_complete'])
    def test_automatic_unicode_and_missing_separators_never_certified(self):
        for text in ('Tôi về!\ufe0f Bạn ở lại.','Tôi về?\u0301 Bạn ở lại.','Yahoo!Bạn ở lại.','Tôi về. \u0301Bạn ở lại.'):
            d=prepare_document(raw(text))
            self.assertFalse(d['segmentation_complete'],text)
            for s in d['sections']:
                for t in s['sentences']:
                    if t['boundary_status']=='exact':
                        self.assertTrue(_safe(s['text'],t['start']))
                        self.assertTrue(_safe(s['text'],t['end']))
    def test_sparse_override_cannot_certify_other_unknown_boundaries(self):
        for text,overrides in [('Tôi về. Anh nói: "Đi thôi.',[7]),
                               ('Tôi chưa biết… Có lẽ mai. Bạn về.',[24])]:
            d=prepare_document(raw(text,boundary_overrides=overrides))
            self.assertFalse(d['segmentation_complete'])
    def test_ellipsis_before_quote_or_number_stays_uncertain(self):
        for text in ('Tôi chưa biết… “Có lẽ mai.”','Tôi chưa biết... 2027 sẽ khác.'):
            self.assertFalse(prepare_document(raw(text))['segmentation_complete'])
    def test_short_secret_does_not_corrupt_generated_role_or_source_context(self):
        text='Biến p bằng 1.\nĐoạn p hai.'
        d=raw(text);d['annotations']=[{'start':5,'end':6,'protected':True}]
        self.evaluate(d,only_pattern='V1')
        contexts=[c for p in self.calls for c in p['state']['related_paragraphs']]
        self.assertIn('previous',{c['role'] for c in contexts})
        self.assertTrue(any(c['text']=='Đoạn p hai.' for c in contexts))
    def test_replacement_seam_cannot_recreate_protected_string(self):
        d=raw('TOPSECRET.\nTOPx.');d['annotations']=[{'start':0,'end':9,'protected':True}]
        d['candidates']=[{'id':'e','start':14,'end':15,'replacement':'SECRET'}]
        self.evaluate(d,only_pattern='V1')
        for p in self.calls:
            for e in p['state'].get('edits',{}).values():self.assertNotIn('TOPSECRET',e['revised_paragraph'])
    def test_permission_reason_not_lost_in_generic_context_gap(self):
        d=raw();d['context_links']=[{'parent_start':0,'parent_end':18,'id':'ext','text':'Context.','allowed':False}]
        r=self.evaluate(d,only_pattern='V1')
        self.assertTrue(any(x['reason']=='permission_blocked' for x in r['missing']))
    def test_output_for_many_paragraphs_is_compact_and_exact(self):
        from jev.transport import encoded
        d=raw('\n'.join('Tôi về.' for _ in range(300)))
        r=self.evaluate(d,only_pattern='V1')
        self.assertLess(len(encoded(r)),1024*1024)
        self.assertEqual(r['counts']['required'],600)
        self.assertEqual(r['counts']['validated'],64)
        self.assertEqual(r['counts']['uncompleted'],536)
    def test_local_context_is_source_bound_and_overrides_resolve_only_prose(self):
        first=prepare_document(raw('Tôi về.'))['sections'][0]['sentences'][0]['id']
        second=prepare_document(raw('Tôi đi.'))['sections'][0]['sentences'][0]['id']
        self.assertNotEqual(first,second)
        d=raw('# Tựa đề');d['source']['layout']='markdown';d['boundary_overrides']=[3]
        self.assertEqual(self.evaluate(d)['status'],'invalid_input')
