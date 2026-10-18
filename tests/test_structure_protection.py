import unittest
from tests.test_structure import raw
from jev.preparation import prepare_document

class StructureProtectionTests(unittest.TestCase):
    def test_combining_crlf_and_emoji_endpoints_rejected(self):
        for text,n in [('a\u0301 về.',1),('Tôi\r\nvề.',4),('X 👩🏽\u200d💻.',3),('X 🇻🇳.',3)]:
            with self.subTest(text=text),self.assertRaisesRegex(ValueError,'^invalid_input$'):
                prepare_document(raw(text,boundary_overrides=[n]))
    def test_opaque_endpoint_override_rejected(self):
        with self.assertRaisesRegex(ValueError,'^invalid_input$'):
            prepare_document(raw('Chạy `a.b()` nhé.',boundary_overrides=[8]))
    def test_lexical_endpoint_override_rejected(self):
        with self.assertRaisesRegex(ValueError,'^invalid_input$'):
            prepare_document(raw('Xem https://example.org nhé.',boundary_overrides=[15]))
    def test_protected_full_parent_not_editable(self):
        got=prepare_document(raw('Tôi về.',annotations=[{'start':0,'end':7,'protected':True}]))
        self.assertFalse(got['sections'][0]['editable'])
    def test_crossing_structure_protection_rejected(self):
        with self.assertRaisesRegex(ValueError,'^invalid_input$'):
            prepare_document(raw('Tôi giữ SECRET rồi về.',annotations=[{'start':0,'end':12,'paragraph':True},{'start':8,'end':14,'protected':True}]))
    def test_variation_selector_and_emoji_tag_boundaries_rejected(self):
        for text,n in [('X ☺\ufe0e.',3),('X 🏴\U000e0067\U000e0062\U000e007f.',3)]:
            with self.subTest(text=text),self.assertRaisesRegex(ValueError,'^invalid_input$'):
                prepare_document(raw(text,boundary_overrides=[n]))
    def test_same_start_protection_nested_inside_explicit_parent(self):
        text='SECRET rồi về. Bạn chờ.'
        got=prepare_document(raw(text,annotations=[{'start':0,'end':len(text),'paragraph':True},{'start':0,'end':6,'protected':True}]))
        self.assertEqual([{'start':0,'end':6}],got['sections'][0]['protected_spans'])
        self.assertTrue(got['source_accounted'])
        self.assertEqual(2,len(got['sections'][0]['sentences']))
