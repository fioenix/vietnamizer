from tests.test_coverage import EvaluationCase
from tests.test_jev import response


class RoleTest(EvaluationCase):
    def test_evidence_nonefit_blocks_but_preserves_answers(self):
        def fake(p,*_):
            r=response(p)
            for key,q in p['questions'].items():
                if key.endswith('_evidence'):
                    r['answers'][key].update(choice='none_fit',probabilities={k:float(k=='none_fit') for k in q['criteria']})
            return r
        r=self.evaluate(transport=fake,only_pattern='V9')
        self.assertTrue(r['answers_complete'])
        self.assertFalse(r['context_complete'])
        self.assertEqual(r['status'],'incomplete')
        self.assertTrue(any(j.get('disposition')=='ignore_unresolved_context' for j in r['judgments']))

    def test_interpretation_nonefit_valid_no_match(self):
        def fake(p,*_):
            r=response(p)
            for key,q in p['questions'].items():
                if key.endswith('_interpretation'):
                    r['answers'][key].update(choice='none_fit',probabilities={k:float(k=='none_fit') for k in q['criteria']})
            return r
        r=self.evaluate(transport=fake,only_pattern='V1')
        self.assertEqual(r['status'],'evaluated')
        self.assertTrue(r['context_complete'])
