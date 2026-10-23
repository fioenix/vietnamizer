# Tasks: Label lines recognized by position

**Input**: [spec](spec.md), [plan](plan.md).
**Branch**: `codex/012-standalone-label-lines`
**Approval**: Short path authorized by the owner on 2026-10-23 (see plan). Implementation is
authorized; commits, push, merge and release each need separate owner authorization.

**Tests**: Constitution gate 1. Each behavioral change follows a test that fails first for the stated
reason. Record RED → GREEN output in [evidence.md](evidence.md). Synthetic text and fake transport
only.
**Format**: `- [ ] Tnnn [USn?] Action with exact paths`.

## Phase 1: Setup

- [X] T001 Create `specs/012-standalone-label-lines/evidence.md` with the starting revision, Python
  version and the baseline suite output.

## Phase 2: User Story 1 — a colon line standing alone is a label (P1)

- [X] T002 [US1] RED: in `tests/test_label_value.py`, add the owner-rated lines that satisfy the label
  conditions as standalone cases (a paragraph, a single list item, and lines separated by single line
  breaks, with and without a final period); keep the feature 011 forms and the form-based rejections;
  move the seven lines named in the plan out of `NOT_LABEL`. In `tests/test_structural_exclusions.py`,
  expect V11 to be excluded on the lone date line of `V11RuleTest`, kept on the lone line showing a V11
  sign, and expect the mixed-list block to yield label lines. Record the failures.
- [X] T003 [US1] GREEN: in `jev/preparation.py`, extend `_mark_label_values` per plan D1.

## Phase 3: User Story 2 — a colon inside running prose stays prose (P1)

- [X] T004 [US2] Tests in `tests/test_label_value.py`: each owner-rated line placed on the same line
  as another sentence (before and after), in prose and in a list item; a hard-wrapped paragraph whose
  plain-label sentence starts mid-line; a blockquote line. Expected: no label unless a feature 011 form
  applies. Record whether each passes before T003 (guard) or fails (RED).

## Phase 4: Polish

- [X] T005 Update `references/typesafe-advisor.md` (FR-008) and the docstring of `_mark_label_values`.
- [X] T006 Run the suite, `python3 scripts/build-jev-registry.py --check`,
  `python3 scripts/validate-package.py` and `python3 scripts/package-plugin.py`; record counts and the
  guard result on the ~1,000-word note (SC-004) in evidence.
- [X] T007 Short independent review of the diff against spec and plan; reproduce each finding, fix
  verified ones test-first, record dispositions in evidence.
