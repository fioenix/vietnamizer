"""Offline evidence checks, not semantic judgments or actual agent-read attestation."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from benchmarks import review_contract as review

ROOT = Path(__file__).resolve().parents[1]


class ReviewContractTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'SKILL.md').write_text('Read the meaning rubric before review.\n')
        self.case = {'id': 'fixture', 'task': 'Review only.', 'source': 'Một số bản có thể chậm.',
                     'required_reads': ['SKILL.md'], 'semantic_expectations': ['keep scope and modality']}
        self.candidate = 'Mọi bản sẽ chậm.'.encode()
        self.packet = review.prepare(self.case, self.root, self.candidate)
        self.report = {'packet_sha256': self.packet['packet_sha256'],
                       'candidate_sha256': self.packet['candidate_sha256'],
                       'meaning': {'status': 'issue', 'findings': [{'source_quote': 'Một số',
                                   'candidate_quote': 'Mọi', 'reason': 'scope changed'}]},
                       'style': {'status': 'clear', 'findings': []}}

    def trace(self):
        return [{'event': 'read', 'path': f['path'], 'sha256': f['sha256']}
                for f in self.packet['required_reads']] + [
                    {'event': 'review', 'candidate_sha256': self.packet['candidate_sha256']}]

    def test_valid_format_keeps_meaning_and_style_separate(self):
        result = review.check(self.packet, self.report, self.candidate)
        self.assertEqual(result['meaning_status'], 'issue')
        self.assertEqual(result['style_status'], 'clear')
        self.assertEqual(result['semantic_correctness'], 'not_evaluated')
        self.assertNotIn('overall_score', result)

    def test_changed_uncommitted_candidate_invalidates_old_review(self):
        with self.assertRaises(ValueError):
            review.check(self.packet, self.report, 'Một số bản có thể chậm.'.encode())

    def test_wrong_packet_or_candidate_binding_is_rejected(self):
        for key in ('packet_sha256', 'candidate_sha256'):
            report = copy.deepcopy(self.report); report[key] = '0' * 64
            with self.subTest(key=key), self.assertRaises(ValueError):
                review.check(self.packet, report, self.candidate)

    def test_invented_quote_is_rejected(self):
        self.report['meaning']['findings'][0]['candidate_quote'] = 'không có trong candidate'
        with self.assertRaises(ValueError):
            review.check(self.packet, self.report, self.candidate)

    def test_clear_or_unassessed_verdict_cannot_discard_recorded_findings(self):
        for status in ('clear', 'not_assessed'):
            report = copy.deepcopy(self.report); report['meaning']['status'] = status
            with self.subTest(status=status), self.assertRaises(ValueError):
                review.check(self.packet, report, self.candidate)

    def test_one_aggregate_score_does_not_replace_two_judgments(self):
        self.report['overall_score'] = 5
        with self.assertRaises(ValueError):
            review.check(self.packet, self.report, self.candidate)
        self.report.pop('overall_score'); self.report.pop('meaning')
        with self.assertRaises(ValueError):
            review.check(self.packet, self.report, self.candidate)

    def test_self_reported_reads_are_not_actual_trace(self):
        self.report['claimed_reads'] = ['SKILL.md']
        result = review.check(self.packet, self.report, self.candidate)
        self.assertEqual(result['provided_trace'], 'absent')
        self.assertEqual(result['actual_agent_reads'], 'not_attested')

    def test_rubric_read_after_review_does_not_satisfy_trace(self):
        trace = self.trace(); trace.reverse()
        with self.assertRaises(ValueError):
            review.check(self.packet, self.report, self.candidate, trace)

    def test_missing_or_stale_read_event_is_rejected(self):
        for trace in (self.trace()[1:], [{**self.trace()[0], 'sha256': '0' * 64}, self.trace()[1]]):
            with self.subTest(trace=trace), self.assertRaises(ValueError):
                review.check(self.packet, self.report, self.candidate, trace)

    def test_ordered_trace_is_checked_but_not_authenticated(self):
        result = review.check(self.packet, self.report, self.candidate, self.trace())
        self.assertEqual(result['provided_trace'], 'ordered_receipts_match_packet')
        self.assertEqual(result['actual_agent_reads'], 'not_attested')

    def test_packet_does_not_reveal_expected_semantic_answer(self):
        self.assertNotIn('semantic_expectations', self.packet)

    def test_catalog_path_cannot_escape_authorized_root(self):
        self.case['required_reads'] = ['../outside.md']
        with self.assertRaises(ValueError):
            review.prepare(self.case, self.root, self.candidate)

    def test_development_cases_have_readable_expected_routes_and_no_holdout_claim(self):
        data = json.loads((ROOT / 'tests/fixtures/review_contract/development.json').read_text())
        self.assertEqual(data['role'], 'development')
        ids = [c['id'] for c in data['cases']]
        self.assertTrue(ids)
        self.assertEqual(len(ids), len(set(ids)))
        for case in data['cases']:
            packet = review.prepare(case, ROOT, case['candidate'].encode())
            self.assertTrue(packet['required_reads'])
        heldout = json.loads((ROOT / 'tests/fixtures/review_contract/heldout-plan.json').read_text())
        self.assertEqual(heldout['cases'], [])
        self.assertEqual(heldout['status'], 'pending_collection')
