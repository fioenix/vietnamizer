# Tasks: Complete preparation of long Markdown documents

**Input**: [spec](spec.md), [plan](plan.md), [research](research.md), [data model](data-model.md),
[segmentation delta](contracts/segmentation-delta.md), [quickstart](quickstart.md), RED baseline in
[baseline/](baseline/).
**Branch**: `codex/009-long-document-preparation`
**Approval**: The owner accepted research R2 and R3 and authorized task generation on 2026-10-22.
This file is a backlog. Implementation, commits, push, merge and release each need separate owner
authorization. Check a box only for verified work.

**Tests**: Required by FR-011 and constitution gate 1. Every behavioral change follows a test that
fails first for the stated reason; an import error is not a behavioral RED. Record RED → GREEN
commands, revision and output in `specs/009-long-document-preparation/evidence.md`. All inputs are
synthetic; no key, network or real user text is used.
**Format**: `- [ ] Tnnn [P?] [USn?] Action with exact repository-relative paths`. `[P]` means
file-disjoint work once its prerequisites are done.

## Phase 1: Setup — evidence

**Purpose**: Freeze the starting state before any runtime change.

- [X] T001 Create `specs/009-long-document-preparation/evidence.md` recording the starting revision (`feed64d` plus spec commits), Python version and machine, the output of `python3 -B -m unittest discover -s tests -t .` (184 tests), and the RED baseline output copied from `specs/009-long-document-preparation/baseline/red-output.txt` (4 tests, 4 failures). State the authority limits from the Approval line above.

**Checkpoint**: Starting state recorded; nothing in `jev/` or `tests/` changed yet.

---

## Phase 2: Foundational — explicit inventory cap

**Purpose**: Separate the 4,096 unit-plus-sentence cap from the work budget (research R5), so that
raising the work bound in US1 cannot remove it. Blocks US1.

- [X] T002 Add a guard test to `tests/test_structure.py` that pins the inventory cap: a source whose units plus sentences exceed 4,096 keeps "at most 4,096 units plus emitted sentence spans (`MAX_INVENTORY`)", reports the remainder as `preparation_limit`, and keeps the classified prefix exact. This passes today only because the scan budget enforces the cap implicitly; record that in `evidence.md` instead of claiming a RED.
- [X] T003 In `jev/preparation.py`, introduce a `WORK_LIMIT = 4096` constant used by both work budgets (metadata and scan) in place of `MAX_INVENTORY`, and an explicit inventory counter: "Counted when a unit is inventoried; a sentence span (exact or unresolved) is emitted"; on exhaustion the "remainder of the current unit and every later unit reported as `preparation_limit`". Charge each emitted span to both the scan work budget and the inventory counter. Then extend T002 to patch `jev.preparation.WORK_LIMIT` to `2**20`, so only the cap can stop it, and show it fails with the counter removed and passes with it. Keep the full suite green; behavior is unchanged at this step.

**Checkpoint**: The cap is enforced by its own counter; behavior on every existing test is unchanged.

---

## Phase 3: User Story 1 — Prepare a whole long technical note (Priority: P1) 🎯 MVP

**Goal**: Ordinary notes up to 10,000 words prepare fully; pathological inputs still stop quickly.

**Independent Test**: Network-free `prepare` on synthetic long notes reports no `preparation_limit`,
and every feature 008 time and memory assertion passes unchanged.

### Tests for User Story 1 ⚠️ write first, confirm they fail

- [X] T004 [P] [US1] Move `test_long_markdown_crosses_scan_budget_without_preparation_limit` and `test_many_short_units_do_not_exhaust_metadata_budget` from `specs/009-long-document-preparation/baseline/test_red_baseline.py` into `tests/test_preparation_limits.py` with their helpers, and add a synthetic 10,000-word Markdown note for SC-002 that must be `prepared` with zero `preparation_limit` regions. It must contain "headings, nested lists, tables, links, numbers and a code block": `#`–`###` headings, bullets nested at least two levels, at least one `|`-table, absolute and relative links, tokens such as `91,4%`, `1.000`, `v0.4.19`, `p50/p95`, and one fenced block annotated as protected. For the 10,000-word note, also assert that the reported unit and sentence counts equal counts fixed by hand from the generator (units per repeated section × sections, sentences per section × sections), not counts read back from the scanner. Confirm all three fail with `preparation_limit`.
- [X] T005 [P] [US1] In `tests/test_review_boundaries.py`, grow the fixture of `test_scan_limit_keeps_classified_exact_prefix_and_context` from `'Tôi về. '*1100` (1,100 sentences) to `'Tôi về. '*4200` (4,200 sentences), so it reaches the 4,096 inventory cap after the bound rises (research R5; `*2100` would prepare completely). Add an assertion that the unresolved reason is `preparation_limit`. Keep every existing assertion, including that `SECRET_AFTER_LIMIT` is never sent.

### Implementation for User Story 1

- [X] T006 [US1] In `jev/preparation.py`, set `WORK_LIMIT = 32768`, the absolute bound "used separately for the metadata phase and the scan phase" (research R2). Do not add a length term. Keep `MAX_INVENTORY = 4096` as the inventory cap from T003. Pass T004 and T005.
- [X] T006a [US1] Added 2026-10-22 after T007 was blocked (research R2 addendum, owner-accepted). First add a deterministic RED test to `tests/test_preparation_limits.py`: the scan work charged for 1,000 initial tokens (`X. `) is at least 4× the work charged for 1,000 plain words (the charges give 4.99×; the old code gives 1.5×, and an exact 5× threshold would sit on the boundary). Then, in `jev/preparation.py`, let `_WorkBudget.take` accept an amount and charge "one extra unit per initials lookahead step" and "four units, instead of one, per terminal-punctuation event outside a lexical span" (after the `inside()` and parenthesis checks). Keep `WORK_LIMIT = 32768` and the quarter-of-remaining token allowance. Pass the new test and T004–T005.
- [X] T007 [US1] Run `tests/test_structure.py`, `tests/test_coverage_scaling.py`, `tests/test_preparation_limits.py` and the full suite with no change to any time or memory limit (SC-003). Before any US2 change, also run `tests/test_preparation.py` and confirm the 54 corpus cases keep identical spans after T006, which shows that raising the bound alone leaves spans unchanged (US3 scenario 2). Record timings of the `X. ` × 250,000 tracemalloc cases and the full output in `specs/009-long-document-preparation/evidence.md`. If any 008 time assertion fails, stop and report instead of loosening it.

**Checkpoint**: US1 complete. Long notes prepare fully; boundary rules are still `vi-spans-1`.

---

## Phase 4: User Story 2 — Keep sentences whole around file names, links and quoted questions (Priority: P1)

**Goal**: File names, domains, relative link destinations and `?",` / `!,` / `?".` no longer create
unresolved regions; a real missing space stays unresolved.

**Independent Test**: Every row of `contracts/segmentation-delta.md` and all 54 corpus cases give the
expected spans and reasons on short synthetic inputs.

### Tests for User Story 2 ⚠️ write first, confirm they fail

- [X] T008 [P] [US2] Add RED tests to `tests/test_preparation.py`, one per row of `specs/009-long-document-preparation/contracts/segmentation-delta.md`, including the two baseline cases moved from `specs/009-long-document-preparation/baseline/test_red_baseline.py`. Assert exact spans and reason codes: no `unsafe_boundary` for a missing separator, and `ambiguous_separator` for `Tôi về.bạn ở lại.` and `Done.Next step.`.
- [X] T009 [P] [US2] Add a linearity test to `tests/test_structure.py` for the dotted-identifier recognizer: one giant token of the form `'a'*N + '.b' + 'é'` and a token of many dotted segments that ends in a non-ASCII letter, both near the input size limit, must finish under the existing 2 s tracemalloc bound used in `test_huge_tokens_have_linear_marker_dispatch`.

### Implementation for User Story 2

- [X] T010 [US2] In `_scan` in `jev/preparation.py`, after the punctuation run and closers: if the next character is one of `,` `;` `:` `.` `!` `?` `…`, it is "**not a boundary**; continue scanning". Any other character outside a recognized token is "**unresolved**, reason `ambiguous_separator`". Use `unsafe_boundary` only when a boundary would split a grapheme cluster, CRLF pair, combining or emoji sequence (FR-008).
- [X] T011 [US2] In `jev/preparation.py`, add the dotted ASCII identifier lexical token: "ASCII letters, digits, `_` or `-`, then one or more `.` segments, each starting with a lowercase ASCII letter or digit; not touching another word character on either side". Run it only on tokens that contain `.`. Pass T009.
- [X] T012 [US2] In `jev/preparation.py`, treat a Markdown link destination as opaque: "text directly after `](` up to the first `)`, any scheme including relative paths; not the `<...>` or quoted form". A `(` inside the destination keeps the whole-unit `ambiguous_url_closer` reason. Pass T008.
- [X] T013 [US2] Run `tests/test_preparation.py` (54 corpus cases, unchanged labels) and the full suite; record the output in `specs/009-long-document-preparation/evidence.md`. Any corpus disagreement is recorded for the owner, never fixed by relabelling (FR-010).

**Checkpoint**: US2 complete. Boundary decisions changed, so US3 must land before integration.

---

## Phase 5: User Story 3 — Know which segmentation rules produced a result (Priority: P2)

**Goal**: Results produced under the new boundary rules are labelled `vi-spans-2`.

**Independent Test**: Preparation reports `vi-spans-2`, and the coverage manifest digest changes
when the profile constant changes.

- [X] T014 [P] [US3] Add RED tests to `tests/test_coverage_model.py`: `prepare_document` reports `segmentation_profile == 'vi-spans-2'`, and patching `jev.preparation.PROFILE_VERSION` changes the coverage `manifest_digest` (today `jev/coverage.py:23` hard-codes `'vi-spans-1'`).
- [X] T015 [US3] Set `PROFILE_VERSION = 'vi-spans-2'` and update the module docstring in `jev/preparation.py`; make `jev/coverage.py` bind the manifest to the profile instead of the literal. Pass T014. (Implemented by reading `prepared['segmentation_profile']`, so the manifest records the profile actually used; an import-time copy of the constant would not follow it.)
- [X] T016 [P] [US3] Change the `profile` field to `vi-spans-2` in `tests/fixtures/segmentation/cases.json` and describe the delta in `tests/fixtures/segmentation/README.md` (link `specs/009-long-document-preparation/contracts/segmentation-delta.md`; state that no case label changed).

**Checkpoint**: All three stories complete.

---

## Phase 6: Polish & cross-cutting

- [ ] T017 [P] Update the limits paragraph of `references/typesafe-advisor.md` (research R7): each preparation phase has an absolute work bound, one invocation inventories at most 4,096 units and sentences, notes of roughly 12,000–17,000 words or more may still report `preparation_limit`, and `ambiguous_separator` is a reason code. Do not promise full remote evaluation of a long document.
- [ ] T018 Run the RED baseline command from `specs/009-long-document-preparation/quickstart.md` section 1 and confirm 4 passes; mark `specs/009-long-document-preparation/baseline/test_red_baseline.py` in its docstring as superseded by the cases in `tests/`.
- [ ] T019 Run quickstart sections 2–4: full suite, `python3 scripts/validate-package.py`, `python3 scripts/package-plugin.py`, and `python3 -B scripts/build-jev-registry.py --check`; confirm archive parity for `jev/preparation.py` and `jev/coverage.py`. Record outputs in `specs/009-long-document-preparation/evidence.md`. Do not commit generated `dist/` output.
- [ ] T020 Request an independent code and security review of the final diff (untrusted input parsing: regex linearity, work bound, inventory cap, no protected text in diagnostics); record findings and dispositions in `specs/009-long-document-preparation/evidence.md`.
- [ ] T021 Owner-only (SC-005): the owner runs `python3 -B -m jev prepare` on the private reported note and records only counts and reason codes in `specs/009-long-document-preparation/evidence.md`. Expected: no `preparation_limit` and no `unsafe_boundary`.

---

## Dependencies & Execution Order

### Phase dependencies

- **Setup (T001)**: none.
- **Foundational (T002 → T003)**: after T001. Blocks US1, because raising the work bound without an explicit cap would break `tests/test_structure.py:36`.
- **US1 (T004–T007, including T006a)**: after T003. T006a follows T006 and precedes T007.
- **US2 (T008–T013)**: after T001. Independent of US1 in behavior, but T010–T012 edit `jev/preparation.py`, the same file as T003 and T006, so do them after T006 or in a separate worktree with a planned merge.
- **US3 (T014–T016)**: after US2, because the profile name changes because boundary decisions change.
- **Polish (T017–T021)**: after all stories. T021 needs the owner.

### Within each story

- Tests first and confirmed failing for the stated reason, then implementation, then the verification run.
- T010 → T011 → T012 are sequential (same function in `jev/preparation.py`).

### Parallel opportunities

- T004 and T005 (different test files).
- T008 and T009 (different test files), and either can be written while US1 is implemented.
- T014 and T016 (test file versus fixture metadata).
- T017 alongside T018–T019.

## Parallel Example: User Story 2

```text
Task: "T008 RED tests for each segmentation-delta row in tests/test_preparation.py"
Task: "T009 dotted-identifier linearity test in tests/test_structure.py"
```

## Implementation Strategy

### MVP first (User Story 1)

1. T001 evidence, T002–T003 explicit inventory cap.
2. T004–T007: long notes prepare fully.
3. Stop and validate: suite green, time limits unchanged. This alone removes the 12k-character stop.

### Incremental delivery

1. MVP above.
2. US2: boundary exemptions, corpus unchanged.
3. US3: profile `vi-spans-2`. US2 and US3 should ship together, so no build labels new boundary rules as `vi-spans-1`.
4. Polish, review, then the owner-only SC-005 check.

## Notes

- Requirement coverage: FR-001/FR-002 → T004, T006; FR-003 → T006, T006a, T007, T009; FR-004 → existing deadline tests, T007; FR-005/FR-006/FR-008 → T008, T010; FR-007 → T008, T011, T012; FR-009 → T014–T016; FR-010 → T013; FR-011 → T004, T008, T018; FR-012 → no task changes request limits, checked in T020 review; FR-013 → T017; FR-014 → T002, T003.
- SC-001 → T018; SC-002 → T004; SC-003 → T006a, T007, T009; SC-004 → T005, T013, T019; SC-005 → T021.
