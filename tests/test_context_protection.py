import unittest
from tests.test_structure import raw
from jev.preparation import prepare_document

class ContextProtectionTests(unittest.TestCase):
    def test_code_context_remains_opaque(self):
        got=prepare_document(raw('```\nSECRET.A.B\n```\n\nTôi về.'))
        context=got['sections'][1]['contexts'][0]
        self.assertEqual('protected',context['kind'])
        self.assertFalse(context['editable'])
    def test_short_protection_and_candidates_keep_original_offsets(self):
        text='Tôi giữ X. Bạn về.'
        got=prepare_document(raw(text,annotations=[{'start':8,'end':9,'protected':True}],candidates=[{'id':'edit','start':11,'end':18,'replacement':'Bạn đi.'}]))
        self.assertEqual((11,18),(got['sections'][0]['candidates'][0]['start'],got['sections'][0]['candidates'][0]['end']))
        self.assertEqual((0,10),(got['sections'][0]['sentences'][0]['start'],got['sections'][0]['sentences'][0]['end']))
    def test_legacy_exact_alias_and_supplemental(self):
        doc={'sections':[{'id':'p','profile':'blog','kind':'prose','text':'Tôi về. Bạn ở.','targets':[{'id':'old','start':0,'end':7},{'id':'diag','start':8,'end':11}]}]}
        got=prepare_document(doc)
        self.assertEqual(['old'],got['sections'][0]['sentences'][0]['aliases'])
        self.assertEqual(2,len(got['sections'][0]['sentences']))
        self.assertEqual('diag',got['sections'][0]['targets'][1]['id'])
