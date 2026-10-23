"""Request plans: which units each request serves and how many questions it carries."""
import collections
import unittest

from jev.core import evaluate, prepare
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
        # Feature 011: heading units (0, 7, 14, 21, 28) lost T4, V2, V3, V5, V11 and V14, and
        # V11's longer Không flag text adds bytes to every request, so units pack 41 questions and
        # headings 40; before 011 every request held 42 (1,344 answers, 2,069 missing).
        headings = {0, 7, 14, 21, 28}
        self.assertEqual(sequence, [(i, 40 if i in headings else 41) for i in range(32)])
        self.assertEqual(len(sent), 32)
        self.assertEqual(report['counts']['validated'], 1307)
        self.assertEqual(collections.Counter(m['reason'] for m in expand_records(report['missing'])),
                         {'budget_exhausted': 1924})


if __name__ == '__main__':
    unittest.main()
