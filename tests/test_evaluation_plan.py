"""Request plans: which units each request serves and how many questions it carries."""
import collections
import unittest

from jev.core import MAX_REQUEST, encoded, evaluate, prepare
from jev.coverage import expand_records
from tests.test_jev import response
from tests.test_preparation_limits import SECTION, markdown


def note(sections=10, **extra):
    return markdown(''.join(SECTION.format(n=i) for i in range(sections)), **extra)


def run(doc, transport=None):
    sent = []
    def fake(payload, *_):
        sent.append(payload)
        return response(payload)
    report = evaluate(doc, environ={'TYPESAFE_API_KEY': 'fake'}, transport=transport or fake)
    return report, sent


class RequestSequenceCharacterizationTest(unittest.TestCase):
    """Pinned request sequence for the ~1,000-word note.

    Before feature 010 (T002) the runner went depth-first: units 0-8, 32 requests of 8-42 questions,
    1,018 answers, every missing group `limit_exceeded`. With no signal or higher tier in this note,
    the tier-4 spread now gives each of 32 units one full request (changed by design in T011).
    """
    def test_request_sequence_for_thousand_word_note(self):
        doc = note()
        units = [u['id'] for u in prepare(doc)['units']]
        report, sent = run(doc)
        sequence = [(units.index(r['section']), len(r['question_ids'])) for r in report['receipts']]
        # The 0.13.2 V1/T2/T3 exceptions and recipes consume more of the unchanged
        # 48,000-byte request limit. Later headings include preceding context:
        # they fit 39 questions; the first heading and prose units fit 40.
        later_headings = {7, 14, 21, 28}
        self.assertEqual(sequence, [(i, 39 if i in later_headings else 40) for i in range(32)])
        self.assertEqual(len(sent), 32)
        self.assertTrue(all(len(encoded(payload)) <= MAX_REQUEST for payload in sent))
        self.assertEqual(report['counts']['validated'], 1276)
        self.assertEqual(collections.Counter(m['reason'] for m in expand_records(report['missing'])),
                         {'budget_exhausted': 1932})


if __name__ == '__main__':
    unittest.main()
