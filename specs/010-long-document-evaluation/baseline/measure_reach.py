"""Measure one invocation's reach on synthetic long notes with an always-valid fake transport.

Run from the repository root:
  python3 -B specs/010-long-document-evaluation/baseline/measure_reach.py

No key, network or real text: notes are built from SECTION in tests/test_preparation_limits.py.
"""
import collections
import os
import sys

sys.path.insert(0, os.getcwd())
from jev.core import evaluate, prepare  # noqa: E402
from jev.coverage import expand_records  # noqa: E402
from tests.test_jev import response  # noqa: E402
from tests.test_preparation_limits import SECTION, markdown  # noqa: E402

for sections in (10, 60, 121):
    text = ''.join(SECTION.format(n=i) for i in range(sections))
    doc = markdown(text)
    prepared = prepare(doc)
    sent = []

    def fake(payload, *_):
        sent.append(payload)
        return response(payload)

    report = evaluate(doc, environ={'TYPESAFE_API_KEY': 'fake'}, transport=fake)
    reached = {j['section'] for j in report['judgments']}
    print(f'words={len(text.split())} units={len(prepared["units"])} '
          f'required={report["counts"]["required"]} validated={report["counts"]["validated"]} '
          f'requests={len(sent)} units_reached={len(reached)} '
          f'reasons={dict(collections.Counter(e.get("reason") for e in expand_records(report["coverage"]) if e.get("reason")))}')
