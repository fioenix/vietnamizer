"""Independent source/check oracles for v2, not copies of scheduler calculations."""
import copy
import unittest
from unittest.mock import patch
from jev import core
from tests.test_jev import response


def raw(text='Tôi về. Bạn ở lại.', **extra):
    return {'schema_version':2,'transmission_allowed':True,
            'source':{'id':'article','layout':'paragraph-lines','text':text},
            'defaults':{'profile':'blog'},
            'context_review':{'reviewed':True,'unresolved':[]}, **extra}


class EvaluationCase(unittest.TestCase):
    def evaluate(self, doc=None, **kwargs):
        self.calls=[]
        def fake(p,*_):
            self.calls.append(copy.deepcopy(p));return response(p)
        return core.evaluate(raw() if doc is None else doc,
                             environ={'TYPESAFE_API_KEY':'fake'},transport=kwargs.pop('transport',fake),**kwargs)


class CoverageTest(EvaluationCase):
    def test_raw_source_gets_each_sentence_and_complete_parent(self):
        r=self.evaluate(only_pattern='V1')
        self.assertEqual(r['status'],'evaluated')
        self.assertEqual(r['schema_version'],2)
        self.assertEqual(r['counts']['sentences'],2)
        self.assertEqual(r['counts']['required'],4)
        self.assertEqual(r['counts']['validated'],4)
        self.assertEqual(r['missing'],[])
        self.assertTrue(all(p['state']['paragraph']=='Tôi về. Bạn ở lại.' for p in self.calls))
        target_text={t['text'] for p in self.calls for t in p['state']['targets']}
        self.assertEqual(target_text,{'Tôi về.','Bạn ở lại.'})
        self.assertFalse(r['evaluation_complete']) # pattern diagnostic is partial
        self.assertTrue(r['scope_complete'])

    def test_all_pattern_success_reconciles(self):
        r=self.evaluate()
        self.assertEqual(r['status'],'evaluated')
        self.assertTrue(r['evaluation_complete'])
        # Registry-derived profile baseline independently recorded in plan: 82/câu+36/đoạn+T3
        self.assertEqual(r['counts']['required'],201)
        self.assertEqual(r['counts']['validated'],200)
        self.assertEqual(r['counts']['mechanical'],1)
        self.assertEqual(len(r['sentences']),2)
        self.assertTrue(all(s['answers_complete'] for s in r['sentences']))
        self.assertEqual(r['missing'],[])

    def test_same_words_distinct_occurrences(self):
        r=self.evaluate(raw('Tôi về. Tôi về.'),only_pattern='V1')
        self.assertEqual(len({s['id'] for s in r['sentences']}),2)
        self.assertEqual(r['counts']['required'],4)

    def test_missing_review_is_not_completed(self):
        d=raw();d.pop('context_review')
        r=self.evaluate(d,only_pattern='V1')
        self.assertEqual(r['status'],'incomplete')
        self.assertTrue(r['answers_complete'])
        self.assertFalse(r['context_complete'])

    def test_invalid_batch_never_credits_answers(self):
        def bad(p,*_):
            a=response(p);a['answers'].pop(next(iter(a['answers'])));return a
        r=self.evaluate(transport=bad,only_pattern='V1')
        self.assertEqual(r['counts']['validated'],0)
        self.assertEqual(r['counts']['uncompleted'],4)
        self.assertEqual(r['status'],'incomplete')

    def test_only_excluded_is_not_vacuous_evaluation(self):
        d=raw('Bí mật.');d['annotations']=[{'start':0,'end':7,'protected':True}]
        r=self.evaluate(d)
        self.assertFalse(r['evaluation_complete'])
        self.assertTrue(r['all_excluded'])
        self.assertEqual(self.calls,[])

    def test_model_binding_changes_manifest(self):
        a=self.evaluate(only_pattern='V1')
        d=raw();d['defaults']['purpose']='Report an event.'
        b=self.evaluate(d,only_pattern='V1')
        self.assertNotEqual(a['manifest_digest'],b['manifest_digest'])

    def test_no_key_does_not_read_document(self):
        self.assertEqual(core.evaluate(None,environ={})['status'],'key_absent')
