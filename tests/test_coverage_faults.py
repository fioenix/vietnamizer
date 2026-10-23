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
        # Feature 010: an invalid reply loses only its own batch; the run continues.
        self.assertEqual(len(seen),4)
        self.assertEqual(r['counts']['validated'],3)
        self.assertEqual(r['counts']['uncompleted'],1)
        self.assertEqual(r['status'],'incomplete')
        self.assertEqual([m['reason'] for m in r['missing']],['invalid_response'])

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


class InvalidReplyTest(EvaluationCase):
    """Feature 010 User Story 4: drop an invalid batch, continue, stop at the third invalid reply."""
    def note_run(self, invalid_at=()):
        from tests.test_evaluation_priority import note
        from jev.core import evaluate
        sent=[]
        def fake(p,*_):
            sent.append(p);r=response(p)
            if len(sent) in invalid_at:r['model']='SECRET-BODY'
            return r
        return evaluate(note(),environ={'TYPESAFE_API_KEY':'fake'},transport=fake),sent

    def invalid_count(self, report):
        from jev.coverage import expand_records
        return sum(m['missing_by_reason'].get('invalid_response',0) for m in expand_records(report['missing']))

    def test_one_invalid_reply_loses_only_its_batch(self):
        report,sent=self.note_run({2})
        self.assertEqual(len(sent),32)
        self.assertEqual(self.invalid_count(report),len(sent[1]['questions']))
        self.assertEqual(report['priority']['invalid_replies'],1)
        self.assertEqual(len({r['request_digest'] for r in report['receipts']}),32,'no batch is resent')

    def test_third_invalid_reply_stops_the_run(self):
        clean,planned=self.note_run()
        report,sent=self.note_run({2,5,9})
        self.assertEqual(len(sent),9)
        sizes=[len(p['questions']) for p in planned]
        self.assertEqual(self.invalid_count(report),sizes[1]+sizes[4]+sizes[8]+sum(sizes[9:]))
        self.assertEqual(report['priority']['invalid_replies'],3)
        invalid=[r for r in report['receipts'] if r['status']=='invalid_response']
        self.assertEqual(len(invalid),3)
        for receipt in invalid:
            self.assertEqual(set(receipt['validation_error']),{'reason'})
        self.assertNotIn('SECRET-BODY',str(report))
