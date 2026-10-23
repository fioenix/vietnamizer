# Implementation Plan: Runner cleanup

**Branch**: `codex/013-runner-cleanup` | **Date**: 2026-10-23 | **Spec**: [spec.md](spec.md)

**Approval**: short path chosen by the owner on 2026-10-23 (as for 012): plan and tasks in one pass,
no `speckit-analyze`, test-first, short independent review, no commit.

## Summary

Three independent fixes in the runner: balanced parentheses in link destinations and bare URLs
(`jev/preparation.py`), a distinct CLI status for unreadable input (`jev/__main__.py`), and one
editable-text helper in the coverage ledger (`jev/coverage.py`).

## Technical Context

**Language/Version**: Python 3 standard library. **Dependencies**: none new.
**Testing**: `python3 -B -m unittest discover -s tests -t .`; synthetic text; CLI via subprocess.
**Constraints**: preparation stays linear and budgeted; no rule, registry or report-field change
other than the new status.

## Decisions

- **D1, link destination.** In the token scan, find the destination's closing `)` by counting
  parentheses over `re.finditer(r'[()]', destination)`, charging the work budget per parenthesis.
  The first `)` at depth 0 closes the link. Found: the destination ends there and is not ambiguous,
  for `http(s)` and relative destinations alike. Not found: keep today's handling (strip trailing
  punctuation; ambiguous when a `(` is inside).
- **D2, bare URL.** Count `(` and `)` in the token once; strip trailing characters from
  `.,!?;:]}”»"` and trailing `)` while closers outnumber openers, adjusting the counts as each `)` is
  removed (GFM). Ambiguous when the kept URL still contains a parenthesis: the independently
  annotated fixture `url-ambiguous-closer` labels `https://example.org/a(b).` ambiguous, and
  `tests/fixtures/segmentation/README.md` forbids changing a label to fit the scanner. Linear in the
  trailing run.
- **D5, work budget.** Addresses without parentheses take the old C-level path and charge nothing
  extra, so preparation of ordinary text spends exactly the same work as before (checked on 2,100
  units: 1,094 sentences on both). Only parentheses are charged.
- **D3, CLI.** Catch `OSError` from opening or reading the input separately and report
  `input_unreadable`; every other failure keeps `invalid_input`. The key check still runs first.
- **D4, editable text.** `jev/coverage.py` imports `editable_text` from `jev/core.py` (core imports
  coverage only inside functions, so there is no import cycle) and computes it once per unit, lazily,
  replacing `_editable`. Protected units never reach the gates, so the helper's empty result for them
  is not observable.

## Expected changes to existing tests

- `tests/test_preparation.py::test_parenthesis_inside_destination_keeps_url_closer_rule` pins
  `Xem [a](b(c).md) nhé.` as ambiguous; by FR-001 it becomes one exact sentence. The test is renamed
  and an unbalanced destination keeps the ambiguous expectation.

## Constitution Check

No rule text or pattern changes (I–III); no threshold (IV); the Markdown skill is untouched (V).
Gates: RED before GREEN for User Stories 1 and 2; User Story 3 is a refactor guarded by the existing
suite and the check-order guard.

## Project Structure

```text
specs/013-runner-cleanup/ (spec, plan, tasks, evidence, checklists/requirements.md)
jev/preparation.py, jev/__main__.py, jev/coverage.py
tests/test_preparation.py, tests/test_jev.py
references/typesafe-advisor.md
```

## Complexity Tracking

None.
