# Implementation Plan: Label lines recognized by position

**Branch**: `codex/012-standalone-label-lines` | **Date**: 2026-10-23 | **Spec**: [spec.md](spec.md)

**Approval**: On 2026-10-23 the owner chose a short path for this feature: plan and tasks in one pass,
no `speckit-analyze`, test-first implementation, a short independent review, verified findings
fixed, no commit. This plan therefore carries the research decision and the test list; there is no
separate research, data model, contract or quickstart file.

## Summary

Widen label–value recognition in `jev/preparation.py` from the two feature 011 forms to any sentence
that starts with a plain label and stands alone on its lines (Q1: A). Only V11 reads the structure,
so only V11 subjects change. The calibration entry of 2026-10-23 holds the owner's rule and the 28
rated lines used as the reference set.

## Technical Context

**Language/Version**: Python 3 standard library (runner), Markdown (rules and contract).
**Primary Dependencies**: none new.
**Testing**: `python3 -B -m unittest discover -s tests -t .`; synthetic text only, fake transport.
**Target Platform**: the packaged runner in every archive.
**Constraints**: no tuned threshold (constitution IV); linear regexes; no change to `SKILL.md`,
`jev/registry.json` or `jev/coverage.py`.
**Scale/Scope**: one function, two test files, one contract paragraph.

## Decision D1: how a standalone sentence is detected

Sentence spans (`start`, `end`) are offsets into the section text, and section text keeps its line
breaks and list marker. A sentence stands alone when:

- the text between the start of its line and `start` is whitespace only (a continuation line's
  indentation), or the sentence is the first one of a list section, whose line starts with the
  list marker;
- the text between `end` and the end of its line is whitespace only.

Two sentences cannot overlap, so these two conditions also mean that no other sentence shares the
lines (FR-001). The label is then read from the sentence text after any list marker, with the
existing `BOLD_LABEL`, `PLAIN_LABEL` and `LEAD_IN` expressions (FR-004); bold was added after review
finding 1, so a bold label never loses to the same label written plain. Only `prose` and `list` sections qualify;
headings, tables and blockquotes keep their handling, because a quote line starts with `>` and so
never matches a label at its start.

Rejected alternative: testing the whole section (only sentence of the paragraph). Q1 chose source
lines, so fields written one per line without blank lines must count.

The feature 011 forms stay as they are (FR-002): a bold label on the section's first sentence, and the
first sentence of each plain label item in a run of at least two adjacent items. The V11 sign
override lives in `jev/coverage.py` and is untouched (FR-005).

## Expected changes to existing tests (by design)

- `tests/test_label_value.py`: seven `NOT_LABEL` lines become labels when they stand alone
  (`Trạng thái: đang xử lý`, `- Người phụ trách: chị Lan`, `Kết luận: tao sai.`,
  `Lý do rất đơn giản: …`, `Tóm lại: …`, `Nói cách khác: …`, `Vậy thì sao: …`); they move to a
  standalone set and are also tested in running prose, where they stay prose.
- `tests/test_structural_exclusions.py`: `V11RuleTest` expects V11 on a lone `Ngày: 22/10/2026`
  line (R3); it now expects the exclusion. The mixed-list case `- Ngày: …` then `1. Bước: …` now
  yields two standalone label lines.
- The ~1,000-word synthetic note has no standalone plain-label prose line, so the guard counts
  (7,001 required) are expected not to change (SC-004).

## Constitution Check

- I, II, III: no rule text changes; V11's **Không flag** already names label–value lines.
- IV: the rule is a native-speaker rule with examples, logged before any runner change; no
  threshold is added.
- V: the Markdown skill is untouched; the runner stays optional.
- Gates: RED before GREEN for each story, evidence with command output, short independent review.

## Project Structure

```text
specs/012-standalone-label-lines/
├── spec.md, plan.md, tasks.md, evidence.md
└── checklists/requirements.md
jev/preparation.py                  # _mark_label_values
tests/test_label_value.py           # owner-rated reference set
tests/test_structural_exclusions.py # V11 expectations
references/typesafe-advisor.md      # label–value forms (FR-008)
```

## Complexity Tracking

None.
