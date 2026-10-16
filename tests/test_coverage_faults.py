from unittest.mock import patch
from tests.test_coverage import EvaluationCase, raw
from tests.test_jev import response


class FaultTest(EvaluationCase):
    def test_prior_batches_survive_atomic_failure(self):
        seen=[]
        def fake(p,*_):
            seen.append(p);r=response(p)
            if len(seen)==2:r['model']='wrong'
            return r
        with patch('jev.core.MAX_QUESTIONS',1):
            r=self.evaluate(transport=fake,only_pattern='V1')
        self.assertEqual(len(seen),2)
        self.assertEqual(r['counts']['validated'],1)
        self.assertEqual(r['counts']['uncompleted'],3)
        self.assertEqual(r['status'],'incomplete')

    def test_absolute_deadline_and_late_answer(self):
        ticks=[0.0]
        def fake(p,*_):ticks[0]+=16;return response(p)
        with patch('jev.core.time.monotonic',side_effect=lambda:ticks[0]):
            r=self.evaluate(transport=fake,only_pattern='V1')
        self.assertEqual(r['counts']['validated'],0)
        self.assertEqual(r['receipts'][0]['status'],'deadline_exceeded')

    def test_transport_echo_not_in_diagnostic(self):
        def fake(*_):raise RuntimeError('SECRET-INPUT')
        r=self.evaluate(transport=fake,only_pattern='V1')
        self.assertNotIn('SECRET-INPUT',str(r))
        self.assertEqual(r['counts']['uncompleted'],4)
