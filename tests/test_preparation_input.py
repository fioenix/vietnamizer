import unittest
from jev.preparation import prepare_document

class PreparationInputTests(unittest.TestCase):
    def test_v2_preserves_source_and_sentences(self):
        source='Tôi về. Bạn ở lại.\r\nNgày mai họp.'
        got=prepare_document({'schema_version':2,'source':{'id':'article','layout':'paragraph-lines','text':source},'defaults':{'profile':'blog'}})
        self.assertTrue(got['source_accounted'])
        self.assertEqual(['Tôi về.','Bạn ở lại.','Ngày mai họp.'],[s['text'][t['start']:t['end']] for s in got['sections'] for t in s['sentences']])
    def test_overlapping_targets_invalid(self):
        doc={'sections':[{'id':'a','text':'Tôi về. Bạn ở.','profile':'blog','kind':'prose','targets':[{'id':'a','start':0,'end':7},{'id':'b','start':5,'end':9}]}]}
        with self.assertRaisesRegex(ValueError,'^invalid_input$'): prepare_document(doc)
    def test_override_does_not_disable_other_clear_boundaries(self):
        text='Tôi chưa biết… Có lẽ mai. Bạn về.'
        got=prepare_document({'schema_version':2,'source':{'id':'article','layout':'paragraph-lines','text':text},'defaults':{'profile':'blog'},'boundary_overrides':[14]})
        self.assertEqual(['Tôi chưa biết…','Có lẽ mai.','Bạn về.'],[s['text'][t['start']:t['end']]for s in got['sections']for t in s['sentences']])
