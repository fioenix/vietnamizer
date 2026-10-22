"""Feature 010 User Story 1: a request budget spent in tier order (candidate, focus, signal, spread)."""
import unittest

from jev.core import evaluate, prepare
from jev.coverage import expand_records
from tests.test_jev import response
from tests.test_preparation_limits import SECTION, markdown

SIGNAL = SECTION.replace('cùng một giám khảo chấm.', 'cùng một giám khảo chấm, và cùng một bộ dữ liệu.')


def note(sections=10, signal_sections=(), **extra):
    text = ''.join((SIGNAL if i in signal_sections else SECTION).format(n=i) for i in range(sections))
    return markdown(text, **extra)


def run(doc):
    sent = []
    def fake(payload, *_):
        sent.append(payload)
        return response(payload)
    return evaluate(doc, environ={'TYPESAFE_API_KEY': 'fake'}, transport=fake), sent


def requests_of(report):
    """Per receipt, in send order: its unit and the (unit, pattern, check name) of each answered check."""
    by_digest = {}
    for j in report['judgments']:
        by_digest.setdefault(j['request_digest'], []).append((j['section'], j['coverage_key'], j['check']))
    return [(r['section'], by_digest.get(r['request_digest'], [])) for r in report['receipts']]


class EvaluationInputTest(unittest.TestCase):
    def assert_invalid(self, doc):
        report, sent = run(doc)
        self.assertEqual(report['status'], 'invalid_input')
        self.assertEqual(sent, [])

    def test_budget_limits_requests_and_is_reported(self):
        report, sent = run(note(evaluation={'requests': 3}))
        self.assertEqual(len(sent), 3)
        self.assertEqual(report['priority']['budget'], 3)
        self.assertFalse(report['priority']['budget_capped'])

    def test_budget_above_limit_is_capped(self):
        report, sent = run(note(evaluation={'requests': 40}))
        self.assertEqual(len(sent), 32)
        self.assertEqual(report['priority']['budget'], 32)
        self.assertTrue(report['priority']['budget_capped'])

    def test_absent_object_means_full_budget(self):
        report, sent = run(note())
        self.assertEqual(len(sent), 32)
        self.assertEqual(report['priority']['budget'], 32)

    def test_invalid_budgets(self):
        for value in (0, -1, 2.5, True, '3', None):
            with self.subTest(value=value):
                self.assert_invalid(note(evaluation={'requests': value}))

    def test_invalid_object_and_deferred_previous(self):
        self.assert_invalid(note(evaluation=[]))
        self.assert_invalid(note(evaluation={'previous': {'encoding': 'answered-checks-v1'}}))

    def test_invalid_focus(self):
        size = len(note()['source']['text'])
        for focus in ([{'start': 0, 'end': size + 1}], [{'start': 5, 'end': 5}], [{'start': -1, 'end': 3}],
                      [{'start': 0, 'end': 3, 'patterns': ['V99']}], [{'start': 0, 'end': 3, 'patterns': 'V11'}],
                      [{'start': 0, 'end': 3}] * 257, {'start': 0, 'end': 3}):
            with self.subTest(focus=str(focus)[:40]):
                self.assert_invalid(note(evaluation={'focus': focus}))

    def test_focus_needs_schema_two(self):
        doc = {'transmission_allowed': True, 'context_review': {'reviewed': True, 'unresolved': []},
               'sections': [{'id': 'p1', 'profile': 'blog', 'kind': 'prose', 'text': 'Tôi về.'}],
               'evaluation': {'focus': [{'start': 0, 'end': 3}]}}
        self.assert_invalid(doc)

    def test_focus_over_protected_text_adds_no_checks(self):
        text = 'Tôi về nhà.\n\n```text\nmật khẩu\n```\n\nBạn ở lại.\n'
        start = text.index('```'); end = text.index('```', start + 3) + 3
        protect = {'annotations': [{'start': start, 'end': end, 'protected': True}]}
        plain, _ = run(markdown(text, **protect))
        focused, _ = run(markdown(text, evaluation={'focus': [{'start': start, 'end': end}]}, **protect))
        self.assertEqual(requests_of(plain), requests_of(focused))


class TierOrderTest(unittest.TestCase):
    def test_candidates_then_focus_before_lower_tiers(self):
        doc = note()
        units = prepare(doc)['units']
        last, early, middle = units[-1], units[20], units[40]
        doc['candidates'] = [{'id': 'e1', 'start': last['start'], 'end': last['start'] + 4, 'replacement': 'Chạy lại'}]
        doc['evaluation'] = {'requests': 8, 'focus': [
            {'start': early['start'], 'end': early['end'], 'patterns': ['V11', 'T4']},
            {'start': middle['start'], 'end': middle['end']}]}
        report, sent = run(doc)
        self.assertEqual(len(sent), 8)
        answered = {(s, k, c) for _, checks in requests_of(report) for s, k, c in checks}
        candidate = {x for x in answered if x[1] == 'edit_e1'}
        self.assertEqual(len(candidate), 4)
        early_focus = {x for x in answered if x[0] == early['id'] and x[1] in ('V11', 'T4')}
        self.assertTrue(early_focus)
        def tier12(checks):
            return any(k == 'edit_e1' or s == middle['id'] or s == early['id'] and k in ('V11', 'T4')
                       for s, k, _ in checks)
        flags = [tier12(checks) for _, checks in requests_of(report)]
        self.assertEqual(flags, sorted(flags, reverse=True), 'a lower-tier request came before tier 1-2 work')
        missing = [m for m in expand_records(report['missing']) if m['section'] == middle['id']]
        self.assertEqual(missing, [], 'every check of the unfiltered focus unit must be answered')

    def test_signal_units_first_and_requests_filled(self):
        doc = note(signal_sections=(5, 8))
        units = prepare(doc)['units']
        signal_units = [u['id'] for u in units
                        if ', và ' in doc['source']['text'][u['start']:u['end']]]
        self.assertEqual(len(signal_units), 2)
        report, _ = run(doc)
        order = requests_of(report)
        self.assertEqual([unit for unit, _ in order[:2]], signal_units)
        for unit, checks in order[:2]:
            self.assertIn('T4', {k for _, k, _ in checks})
            self.assertGreater(len(checks), 2, 'room left after the T4 checks must be filled')

    def test_spread_reaches_thirty_units(self):
        report, _ = run(note())
        self.assertGreaterEqual(len({j['section'] for j in report['judgments']}), 30)

    def test_reports_tiers_and_budget_exhausted(self):
        report, _ = run(note())
        tiers = report['priority']['tiers']
        self.assertEqual(set(tiers), {'1', '2', '3', '4'})
        for counts in tiers.values():
            self.assertEqual(set(counts), {'planned', 'answered', 'missing'})
        self.assertEqual(sum(t['answered'] for t in tiers.values()), report['counts']['validated'])
        self.assertTrue(all(j['tier'] in (1, 2, 3, 4) for j in report['judgments']))
        missing = expand_records(report['missing'])
        self.assertTrue(any(m['reason'] == 'budget_exhausted' for m in missing))
        for m in missing:
            self.assertEqual(sum(m['missing_by_tier'].values()), m['missing'])
            self.assertEqual(sum(m['missing_by_reason'].values()), m['missing'])
        self.assertEqual(sum(t['missing'] for t in tiers.values()), sum(m['missing'] for m in missing))

    def test_plan_invariants(self):
        doc = note(signal_sections=(2, 7))
        units = prepare(doc)['units']
        doc['candidates'] = [{'id': 'e1', 'start': units[-1]['start'], 'end': units[-1]['start'] + 4,
                              'replacement': 'Chạy lại'}]
        doc['evaluation'] = {'focus': [{'start': units[30]['start'], 'end': units[30]['end']}]}
        report, sent = run(doc)
        self.assertLessEqual(len(sent), 32)
        tier = {(j['request_digest'], j['check']): j['tier'] for j in report['judgments']}
        opened = [min(tier[(r['request_digest'], n)] for n in r['question_ids']) for r in report['receipts']]
        self.assertEqual(opened, sorted(opened), 'the opening tier never goes back up')
        checks = [(r['section'], n) for r in report['receipts'] for n in r['question_ids']]
        self.assertEqual(len(checks), len(set(checks)))
        seen = set(); reached_again = False
        for r, t in zip(report['receipts'], opened):
            if t == 4:
                if r['section'] in seen: reached_again = True
                else: self.assertFalse(reached_again, 'an unreached unit came after a reached one in tier 4')
            seen.add(r['section'])

    def test_identical_input_identical_requests(self):
        first, _ = run(note(signal_sections=(3,)))
        second, _ = run(note(signal_sections=(3,)))
        self.assertEqual([r['request_digest'] for r in first['receipts']],
                         [r['request_digest'] for r in second['receipts']])

    def test_work_that_fits_is_sent_exactly_once(self):
        report, sent = run(note(sections=1))
        self.assertLess(len(sent), 32)
        # Question names are unique per request only; a check is identified by its unit and name.
        checks = [(r['section'], n) for r in report['receipts'] for n in r['question_ids']]
        self.assertEqual(len(checks), len(set(checks)))
        self.assertEqual(report['counts']['validated'], report['counts']['required'] - report['counts']['mechanical'])


class ReviewFixTest(unittest.TestCase):
    """Feature 010 independent review (T022): verified findings, each RED before its fix."""
    def sections(self, text, **extra):
        return dict({'transmission_allowed': True, 'context_review': {'reviewed': True, 'unresolved': []},
                     'sections': [{'id': 'p1', 'profile': 'blog', 'kind': 'prose', 'text': text}]}, **extra)

    def totals(self, report):
        total = {}
        for m in expand_records(report['missing']):
            for reason, count in m['missing_by_reason'].items():
                total[reason] = total.get(reason, 0) + count
        return total

    def test_stop_reason_covers_planned_work_only(self):
        # Review finding S2 was not adopted: FR-006 and the contract keep work the budget never
        # reached as budget_exhausted; planned work a stop prevented carries the stop reason.
        from jev.transport import ServiceError
        _, planned = run(note())
        def fake(*_): raise ServiceError('authentication_failed')
        report = evaluate(note(), environ={'TYPESAFE_API_KEY': 'fake'}, transport=fake)
        self.assertEqual(len(report['receipts']), 1)
        totals = self.totals(report)
        self.assertEqual(totals['authentication_failed'], sum(len(p['questions']) for p in planned))
        self.assertEqual(set(totals), {'authentication_failed', 'budget_exhausted'})

    def test_oversized_check_does_not_relabel_its_group(self):
        text = 'Đây là ' + 'một câu rất dài ' * 800 + 'xong. ' + ' '.join(f'Câu {i:04d} ổn.' for i in range(1500))
        report, _ = run(self.sections(text, evaluation={'requests': 14}))
        totals = self.totals(report)
        self.assertGreater(totals.get('budget_exhausted', 0), 100000)
        self.assertLess(totals.get('context_too_large', 0), 1000)
        self.assertFalse(report['context_complete'])

    def test_packing_respects_the_deadline(self):
        import time
        from unittest.mock import patch
        text = ' '.join(f'Câu {i:04d} ổn.' for i in range(2950))
        start = time.monotonic()
        with patch('jev.core.TOTAL_SECONDS', 1):
            report, sent = run(self.sections(text))
        self.assertLess(time.monotonic() - start, 6)
        self.assertIn('deadline_exceeded', self.totals(report))

    def test_skipped_top_tier_check_does_not_open_a_lower_tier_request(self):
        doc = note()
        units = prepare(doc)['units']
        last, focus = units[-1], units[20]
        doc['candidates'] = [{'id': 'e1', 'start': last['start'], 'end': last['start'] + 4, 'replacement': 'x' * 50000}]
        doc['evaluation'] = {'requests': 2, 'focus': [{'start': focus['start'], 'end': focus['end']}]}
        report, _ = run(doc)
        self.assertEqual(report['receipts'][0]['section'], focus['id'])


if __name__ == '__main__':
    unittest.main()
