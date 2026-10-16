import unittest
from jev.preparation import prepare_document
from tests.test_coverage import raw, EvaluationCase
from jev import core
from unittest.mock import patch

class ReviewedBoundaries(EvaluationCase):
    def test_opaque_terminal_candidate_cannot_escape_at_span_end(self):
        d=raw('Tôi giữ SECRET. Bạn về.')
        d['annotations']=[{'start':8,'end':15,'protected':True}]
        self.assertFalse(prepare_document(d)['segmentation_complete'])
    def test_markdown_link_destination_is_lexical(self):
        d=raw('Xem [bài](https://example.org/a.b). Đọc tiếp.');d['source']['layout']='markdown'
        p=prepare_document(d)
        self.assertTrue(p['segmentation_complete'])
        self.assertEqual(2,len(p['sections'][0]['sentences']))
    def test_quoted_title_recognizer_keeps_name_together(self):
        p=prepare_document(raw('“TS. Lan đã đến.” Cuộc họp bắt đầu.'))
        self.assertTrue(p['segmentation_complete'])
        self.assertEqual(2,len(p['sections'][0]['sentences']))
    def test_parenthesis_depth_closes_on_internal_ellipsis(self):
        p=prepare_document(raw('Tôi (ngập ngừng...) rồi về. Bạn ở lại.'))
        self.assertTrue(p['segmentation_complete'])
        self.assertEqual(2,len(p['sections'][0]['sentences']))
    def test_quote_attribution_closes_parenthesis(self):
        p=prepare_document(raw('Anh hỏi ("Xong chưa?") rồi bước đi. Câu tiếp theo.'))
        self.assertTrue(p['segmentation_complete'])
        self.assertEqual(2,len(p['sections'][0]['sentences']))
    def test_selected_retains_protection_from_unselected_distant_parent(self):
        d={'transmission_allowed':True,'context_review':{'reviewed':True},'sections':[
          {'id':'a','kind':'prose','profile':'blog','text':'SECRET_TOKEN','protected_spans':[{'start':0,'end':12}]},
          {'id':'b','kind':'prose','profile':'blog','text':'Giữa.'},
          {'id':'c','kind':'prose','profile':'blog','text':'Tôi về.','targets':[{'id':'SECRET_TOKEN','start':0,'end':7}], 'context':['Ghi chú SECRET_TOKEN']} ]}
        r=self.evaluate(d,scope='selected',only_pattern='V1')
        self.assertEqual(r['status'],'evaluated')
        self.assertNotIn('SECRET_TOKEN',str(self.calls))
        self.assertNotIn('SECRET_TOKEN',str(r))
    def test_escaped_backtick_does_not_expose_real_inline_code(self):
        d=raw(r'\`a` SECRET_ESCAPED `b`');d['source']['layout']='markdown'
        self.evaluate(d,only_pattern='V1')
        self.assertNotIn('SECRET_ESCAPED',str(self.calls))
    def test_revised_paragraph_keeps_unmarked_source_copies(self):
        d=raw('Biến p bằng 1; phải giữ.');d['annotations']=[{'start':5,'end':6,'protected':True}]
        d['candidates']=[{'id':'e','start':12,'end':13,'replacement':'2'}]
        self.evaluate(d,only_pattern='V1')
        edits=[e for p in self.calls for e in p['state'].get('edits',{}).values()]
        self.assertTrue(edits)
        self.assertTrue(all('phải giữ' in e['revised_paragraph'] for e in edits))
    def test_scan_limit_keeps_classified_exact_prefix_and_context(self):
        d=raw('Tôi về. '*1100+'\n```\nSECRET_AFTER_LIMIT\n```');d['source']['layout']='markdown'
        p=prepare_document(d)
        self.assertFalse(p['segmentation_complete'])
        self.assertTrue(p['sections'])
        self.assertTrue(any(t['boundary_status']=='exact' for s in p['sections'] for t in s['sentences']))
        self.evaluate(d,only_pattern='V1')
        self.assertNotIn('SECRET_AFTER_LIMIT',str(self.calls))
    def test_selected_scope_excludes_unrelated_boundary_uncertainty(self):
        d={'transmission_allowed':True,'context_review':{'reviewed':True},'sections':[
          {'id':'a','kind':'prose','profile':'blog','text':'Anh nói: "Đi thôi.'},
          {'id':'b','kind':'prose','profile':'blog','text':'Tôi về.','targets':[{'id':'t','start':0,'end':7}]}]}
        r=self.evaluate(d,scope='selected',only_pattern='V1')
        self.assertEqual(r['status'],'evaluated')
        self.assertFalse(r['evaluation_complete'])
    def test_escaped_first_tick_leaves_multi_run_opener(self):
        d=raw(r'Dùng \`` SECRET_ESCAPED_MULTI ` rồi.');d['source']['layout']='markdown'
        self.evaluate(d,only_pattern='V12')
        self.assertNotIn('SECRET_ESCAPED_MULTI',str(self.calls))
