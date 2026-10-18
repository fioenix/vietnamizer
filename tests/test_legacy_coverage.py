import unittest
from tests.test_coverage import EvaluationCase, raw
from tests.test_jev import response

class LegacyTest(EvaluationCase):
    def doc(self):
        return {'transmission_allowed':True,'context_review':{'reviewed':True,'unresolved':[]},
                'sections':[{'id':'p1','profile':'blog','kind':'prose','text':'Tôi về. Bạn ở lại.'}]}
    def test_full_mode_fills_missing_explicit_sentences(self):
        d=self.doc();d['sections'][0]['targets']=[{'id':'myfirst','start':0,'end':7}]
        r=self.evaluate(d,only_pattern='V1')
        self.assertEqual(r['counts']['sentences'],2)
        self.assertEqual(r['counts']['required'],4)
        self.assertEqual(r['source_scope'],'provided_sections')
        self.assertIn('myfirst',r['sentences'][0]['aliases'])
    def test_selected_custom_span_is_explicit_partial_scope(self):
        d=self.doc();d['sections'][0]['targets']=[{'id':'custom','start':0,'end':3}]
        r=self.evaluate(d,only_pattern='V1',scope='selected')
        self.assertEqual(r['counts']['required'],2)
        self.assertFalse(r['evaluation_complete'])
        self.assertEqual(r['status'],'evaluated')
    def test_overlapping_explicit_targets_are_invalid(self):
        d=self.doc();d['sections'][0]['targets']=[{'id':'a','start':0,'end':7},{'id':'b','start':1,'end':8}]
        r=self.evaluate(d)
        self.assertEqual(r['status'],'invalid_input')
        self.assertEqual(self.calls,[])
    def test_candidate_guards_separate_from_sentence_matrix(self):
        d=self.doc();d['sections'][0]['candidates']=[{'id':'e','start':0,'end':7,'replacement':'Tôi đã về.'}]
        r=self.evaluate(d,only_pattern='V1')
        self.assertEqual(r['counts']['required'],8)
        self.assertEqual(len(r['candidate_reviews']),1)
        self.assertEqual(r['candidate_reviews'][0]['status'],'jev_evaluated')
        self.assertEqual(sum(x['required'] for x in r['sentences']),4)
    def test_alias_cannot_replace_another_occurrence_id(self):
        from jev.preparation import prepare_document
        d=self.doc();s=prepare_document(d)['sections'][0]['sentences']
        d['sections'][0]['targets']=[{'id':s[1]['id'],'start':s[0]['start'],'end':s[0]['end']}]
        r=self.evaluate(d,only_pattern='V1')
        self.assertEqual(r['status'],'evaluated')
        self.assertEqual(len({x['id'] for x in r['sentences']}),2)
        self.assertEqual({t['text'] for p in self.calls for t in p['state']['targets']},{'Tôi về.','Bạn ở lại.'})

    def test_link_role_and_external_id_cannot_echo_protected_value(self):
        d=raw('TOPSECRET.\nTôi về.')
        d['annotations']=[{'start':0,'end':9,'protected':True}]
        d['context_links']=[{'parent_start':11,'parent_end':18,'id':'TOPSECRET','text':'Nội dung.','role':'TOPSECRET'}]
        r=self.evaluate(d,only_pattern='V1')
        self.assertEqual(r['status'],'evaluated')
        self.assertNotIn('TOPSECRET',str(self.calls))

    def test_heading_target_patterns_are_not_silently_skipped(self):
        d=raw('# Tiêu đề\n\nTôi về.')
        d['source']['layout']='markdown'
        r=self.evaluate(d,only_pattern='T1')
        self.assertEqual(r['counts']['required'],4)
        self.assertEqual(r['counts']['sentences'],1)
        self.assertTrue(any(g['scope']=='unit' for g in r['work_groups']))

    def test_candidate_identifier_cannot_echo_protected_source(self):
        d=self.doc();d['sections'][0].update(text='TOPSECRET. Tôi về.',protected_spans=[{'start':0,'end':9}],candidates=[{'id':'TOPSECRET','start':11,'end':18,'replacement':'Tôi đi.'}])
        r=self.evaluate(d,only_pattern='V1')
        self.assertNotEqual(r['status'],'invalid_input')
        self.assertNotIn('TOPSECRET',str(self.calls))

    def test_selected_identity_is_source_bound_not_supplied_alias(self):
        d=self.doc();d['sections'][0].update(text='Tôi giữ TOPSECRET. Bạn về.',
            protected_spans=[{'start':8,'end':17}],targets=[{'id':'TOPSECRET','start':19,'end':26}])
        r=self.evaluate(d,only_pattern='V1',scope='selected')
        self.assertEqual(r['status'],'evaluated')
        self.assertNotIn('TOPSECRET',str(self.calls))
        self.assertNotIn('TOPSECRET',str(r))
        first=r['sentences'][0]['id']
        d['sections'][0]['targets'][0]['id']='different_alias'
        other=self.evaluate(d,only_pattern='V1',scope='selected')
        self.assertEqual(first,other['sentences'][0]['id'])
