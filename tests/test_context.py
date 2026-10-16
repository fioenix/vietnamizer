import unittest
from tests.test_structure import raw
from jev.preparation import prepare_document

class ContextTests(unittest.TestCase):
    def test_neighbors_and_ancestry_are_complete(self):
        text='# Chủ đề\n\nĐoạn trước. Đủ câu.\n\nĐoạn giữa. Câu hai.\n\nĐoạn sau.'
        got=prepare_document(raw(text,context_review={'reviewed':True,'unresolved':[]}))
        section=got['sections'][2]
        self.assertTrue(section['context_reviewed'])
        self.assertEqual({'# Chủ đề','Đoạn trước. Đủ câu.','Đoạn sau.'},{x['text'] for x in section['contexts']})
    def test_nonlocal_link_and_blocked_scope(self):
        text='Một.\n\nHai.\n\nBa.'; doc=raw(text,context_links=[{'parent_start':0,'parent_end':4,'source_start':12,'source_end':15,'role':'definition','allowed':False}],context_review={'reviewed':True,'unresolved':[]})
        got=prepare_document(doc); section=got['sections'][0]
        self.assertIn('context_permission_denied',section['context_unresolved'])
        self.assertEqual('Ba.',section['contexts'][-1]['text'])
        self.assertFalse(section['contexts'][-1]['allowed'])
    def test_missing_full_unit_does_not_silently_drop(self):
        got=prepare_document(raw('Một.\n\nHai.',context_links=[{'parent_start':0,'parent_end':4,'source_start':6,'source_end':9}]))
        self.assertIn('context_link_unresolved',got['sections'][0]['context_unresolved'])
    def test_raw_review_prose_not_in_diagnostic(self):
        got=prepare_document(raw('Tôi về.',context_review={'reviewed':True,'unresolved':['SECRET dependency']}))
        self.assertEqual(['host_context_unresolved'],got['sections'][0]['context_unresolved'])
    def test_input_is_not_mutated(self):
        doc=raw('Một.\n\nHai.'); before=repr(doc)
        prepare_document(doc)
        self.assertEqual(before,repr(doc))
    def test_nested_list_retains_enclosing_item_and_leadin(self):
        text='Cần chuẩn bị:\n\n- Hồ sơ.\n  - Bản gốc.\n  - Bản sao.\n- Lịch hẹn.'
        got=prepare_document(raw(text))
        inner=next(s for s in got['sections'] if s['text']=='- Bản sao.')
        values={m['text'] for m in inner['contexts']}
        self.assertIn('- Hồ sơ.',values)
        self.assertIn('Cần chuẩn bị:',values)
    def test_parent_review_overrides_global_host_gap(self):
        got=prepare_document(raw('Một.\n\nHai.',context_review={'reviewed':False,'unresolved':['Check antecedent']},context_reviews=[{'start':0,'end':4,'reviewed':True,'unresolved':[]}]))
        self.assertTrue(got['sections'][0]['context_reviewed'])
        self.assertEqual([],got['sections'][0]['context_unresolved'])
        self.assertFalse(got['sections'][1]['context_reviewed'])
        self.assertTrue(got['sections'][1]['context_unresolved'])
