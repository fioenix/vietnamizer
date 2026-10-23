# Tasks: Structural exclusions and the T4 sign gate

**Input**: [spec](spec.md), [plan](plan.md), [research](research.md), [data model](data-model.md),
[contract delta](contracts/exclusion-contract.md), [quickstart](quickstart.md).
**Branch**: `codex/011-structural-exclusions`
**Approval**: The owner answered Q1 (option B), accepted the research R3 deviation and authorized
task generation on 2026-10-22. Rule maintenance for V11 is authorized. This file is a backlog.
Implementation, commits, push, merge, release and any live service run each need separate owner
authorization. Check a box only for verified work.

**Tests**: Required by constitution gate 1. Every behavioral change follows a test that fails first
for the stated reason; an import error or a missing attribute is not a behavioral RED. Record
RED → GREEN commands, revision and output in `specs/011-structural-exclusions/evidence.md`. All
inputs are synthetic and every evaluation test uses a fake transport; no key, network or real user
text is used.
**Format**: `- [ ] Tnnn [P?] [USn?] Action with exact repository-relative paths`. `[P]` means
file-disjoint work once its prerequisites are done.

## Phase 1: Setup — evidence

- [X] T001 Create `specs/011-structural-exclusions/evidence.md` recording the starting revision (`2670959` plus spec commits), Python version and machine, the output of `python3 -B -m unittest discover -s tests -t .` (201 tests), and for the ~1,000-word synthetic note built from `SECTION` in `tests/test_preparation_limits.py`: checks required (7,381), T4 checks, and checks per heading unit. State the authority limits from the Approval line above.

**Checkpoint**: Starting state recorded; nothing in `jev/`, `scripts/`, `SKILL.md` or `calibration/` changed yet.

---

## Phase 2: Foundational — one subject list per pattern group

**Purpose**: Let each pattern group own its subjects and record excluded ones (research R4), with
no exclusion yet and no behavior change. Blocks every user story.

- [X] T002 Create `tests/test_structural_exclusions.py` with a guard test: for the ~1,000-word synthetic note, pin `counts.required`, the per-sentence `required` values in `sentences`, and the check keys `Ledger.checks` yields for one heading unit and one prose unit. It passes today; record in `evidence.md` that it is a guard, not a RED.
- [X] T003 In `jev/coverage.py`, give each target-scope pattern group its own subject list, make `Ledger.checks` iterate each group's own subjects instead of assuming the first group's count, add an empty `excluded_subjects` list to coverage entries, and compute each sentence's `required` as "the sum of recipes over the groups that include the sentence". With no exclusion applied, T002 and the full suite pass unchanged.

**Checkpoint**: Per-group subjects in place; observable behavior identical apart from the empty
`excluded_subjects` field.

---

## Phase 3: User Story 1 — No T4 question where `, và` is absent (Priority: P1) 🎯 MVP

**Goal**: T4 is asked only about subjects whose editable text matches `,\s+và\s`.

**Independent Test**: Evaluate (fake transport) a synthetic note mixing sentences with and without
`, và`; count T4 questions and `sign_absent` exclusions.

### Tests for User Story 1 ⚠️ write first, confirm they fail

- [X] T004 [US1] In `tests/test_structural_exclusions.py`, add RED tests: a sentence without `, và` gets no T4 question and its coverage entry lists `{subject, reason: "sign_absent"}` in `excluded_subjects`; `,và` with no whitespace does not open T4 and `,\nvà ` does; a sentence containing `, và ` still gets T4, including when *và* is written in decomposed form (NFD, `a` plus U+0300) and the source text is kept unnormalized; `, và` only inside inline code or a protected span does not open T4; an H1 heading unit and a `- Ngày: 22/10/2026 (Asia/Ho_Chi_Minh)` item get no T4 question; a section where no subject opens T4 has T4 `status: excluded` with reason `sign_absent`; excluded subjects do not count in `counts.required`.
- [X] T005 [P] [US1] Create `tests/test_registry_exclusions.py` with RED tests: the T4 entry of `jev/registry.json` has `gate` equal to `,\s+và\s`; running the generator's check against a temporary copy of `SKILL.md` whose T4 **Dấu hiệu** no longer contains `` `,\s+và\s` `` fails.

### Implementation for User Story 1

- [X] T006 [US1] In `scripts/build-jev-registry.py`, add the gate table (T4: `,\s+và\s`), write `gate` into the T4 entry, and make `--check` fail when the expression is missing from T4's **Dấu hiệu** in `SKILL.md` or the registry differs. Regenerate `jev/registry.json` with `python3 -B scripts/build-jev-registry.py`. Pass T005.
- [X] T007 [US1] In `jev/coverage.py`, filter T4's subjects by its `gate` against the NFC form of each subject's editable text with protected spans blanked (normalization for the gate decision only; offsets and request text unchanged), recording `sign_absent` per research R4 and the data model. Pass T004 and the full suite; list in `specs/011-structural-exclusions/evidence.md` each pre-existing test whose required-check count changed and why (SC-005).

**Checkpoint**: US1 complete. T4 no longer reaches text without its sign.

---

## Phase 4: User Story 2 — Patterns skip structures their own rules exclude (Priority: P1)

**Goal**: Headings lose V2, V3, V5 and V14; label–value lines are recognized; exclusions are
generated from quoted canonical phrases.

**Independent Test**: Evaluate (fake transport) a synthetic note with headings, field lists and prose;
compare patterns asked per subject with the contract table.

### Tests for User Story 2 ⚠️ write first, confirm they fail

- [X] T008 [P] [US2] Create `tests/test_label_value.py` with RED tests on at least 20 lines that must be recognized and at least 20 that must not (SC-003), per the contract table: recognized are `**Nhãn:** giá trị`, `**Nhãn**: giá trị`, and plain `- Nhãn: giá trị` items "in a run of ≥ 2 adjacent list items that all have a label"; not recognized are a lone plain `Nhãn: giá trị` line or single list item, prose with a colon (`Kết quả lệch khoảng ±10% so với bản cũ: mày đừng so trực tiếp.`, `Kết luận: tao sai.`), lead-ins ending in `:` with no value, and labels containing digits, a comma, terminal punctuation, a link, code or emphasis. Only the first sentence of a recognized item is `label_value`.
- [X] T009 [US2] In `tests/test_structural_exclusions.py`, add RED tests: a heading unit gets no V2, V3, V5 or V14 question and lists them with `{reason: "structure_excluded", structure: "heading"}`; T1, T5, T6, K3 (technical profile), V6 and V20 are still asked about it; a unit marked heading by a host `kind` annotation behaves the same; a recognized label–value item loses no pattern yet (V11 and T5 still asked); candidate review checks on an excluded subject are unchanged; a typography-only unit keeps reason `genre_gate`.
- [X] T010 [P] [US2] In `tests/test_registry_exclusions.py`, add RED tests: `excluded_structures` equals `["heading"]` for V2, V3, V5 and V14 and is absent elsewhere; for each pair, deleting its quoted phrase (V2 "tít, sapo"; V3 "Không áp dụng pattern này cho tiêu đề, nhãn, mục lục hoặc ô bảng"; V5 "tiêu đề, bảng biểu"; V14 "tít, sapo, chú thích ảnh, nhãn nút, mục lục, ô bảng, checklist") from a temporary copy of `SKILL.md` makes the check fail.

### Implementation for User Story 2

- [X] T011 [US2] In `scripts/build-jev-registry.py`, add the exclusion table of research R1 with each quoted phrase, write `excluded_structures` into the pattern entries, and make `--check` fail when a phrase is missing from that pattern's **Không flag**. Regenerate `jev/registry.json`. Pass T010.
- [X] T012 [US2] In `jev/preparation.py`, where list items and their adjacency are known, mark the first sentence of each recognized label–value item per research R3 ("letters and spaces only (no digits, comma, terminal punctuation, link, code or emphasis), followed by a non-empty value"; bold labels; plain labels only in a run of at least two adjacent label items of the same list). Keep it one linear pass per unit with no backtracking regex. Pass T008.
- [X] T013 [US2] In `jev/coverage.py`, filter each pattern group's subjects by `excluded_structures` (heading units, label–value sentences), recording `structure_excluded` with the structure kind, after the existing protected, typography-only and inactive-profile gates and before the T4 gate. Pass T009.
- [X] T014 [US2] Run the full suite. Update only tests whose required-check counts change because of heading exclusions, and list each with its cause in `specs/011-structural-exclusions/evidence.md` (SC-005). If any other test fails, stop and report instead of loosening it.

**Checkpoint**: US2 complete. Rule-stated exclusions are deterministic; no rule text changed.

---

## Phase 5: User Story 3 — V11 names the structures it does not apply to (Priority: P2)

**Goal**: Rule maintenance for V11, owner decision Q1: B, with the calibration entry first.

**Independent Test**: The calibration entry precedes the rule edit in history; the registry check
passes; synthetic H1 and field-list date item get no V11 question; a prose lead-in still does.

### Tests for User Story 3 ⚠️ write first, confirm they fail

- [X] T015 [US3] In `tests/test_structural_exclusions.py`, add RED tests: a heading unit and a recognized label–value item (field list starting `- Ngày: 22/10/2026 (Asia/Ho_Chi_Minh)` followed by `- Người viết: Fio`) get no V11 question, with `structure_excluded`; a lone plain `Ngày: 22/10/2026` line still gets V11 and no T4; the prose sentence `Điều quan trọng cần lưu ý là hệ thống chỉ đồng bộ 15 phút một lần.` still gets V11 (SC-001).

### Implementation for User Story 3

- [X] T016 [US3] Add a `calibration/LOG.md` entry in the format `AGENTS.md` prescribes (date, genre, source, before text, comparison text, observed scores, named difference, pattern V11, classification "Pattern sửa nhầm", decision). Use synthetic text equivalent to the private case (an H1 title and a field list starting `- Ngày: …`), state that the source note is private, and give as comparison text the lines kept unchanged because they are correct. Record titles and label–value lines as resting on the observed false positives. Record table cells, captions, tables of contents and checklist items as native-speaker rules (`AGENTS.md` evidence source 4), each with the synthetic example from research R5 (`| Hạng mục | Điểm cần lưu ý |`; `*Hình 3. Những điểm cần lưu ý trong quy trình nhập kho*`; `4. Những điều cần lưu ý khi chạy lại phép đo`; `- [ ] Cần lưu ý: sao lưu dữ liệu trước khi chạy lại`), pending the owner's confirmation in T023. Review the new Vietnamese text with the skill itself (`AGENTS.md`, "Tự rà lại phần vừa viết bằng chính `SKILL.md`"). This entry must land in an earlier commit than T017 (SC-006).
- [X] T017 [US3] After the owner has confirmed the four native-speaker rules and examples recorded in T016 (T023, part a), in `SKILL.md`, extend V11's **Không flag** to name titles and headings, label–value lines, table cells, captions, tables of contents and checklist items, starting from the draft in research R5 and keeping the wording consistent with V14 and T5. Review the new sentence with the skill itself (`AGENTS.md`, "Tự rà lại phần vừa viết bằng chính `SKILL.md`") and keep `SKILL.md` under 550 lines. Change no other pattern.
- [X] T018 [P] [US3] In `calibration/ca-kiem-thu.md`, add V11 cases: one per newly named structure (title, label–value line, table cell, caption, table of contents, checklist item) as "không flag", and one prose lead-in sentence that must still be flagged. Review the new Vietnamese text with the skill itself, as in T017.
- [X] T019 [US3] In `scripts/build-jev-registry.py`, add V11 to the exclusion table for `heading` and `label_value` with phrases quoted from the new V11 text, regenerate `jev/registry.json` (V11's `no_flag` text changes too) and run `--check`. Extend T010 in `tests/test_registry_exclusions.py` with the V11 pairs. Pass T015 and the full suite.

**Checkpoint**: All user stories complete.

---

## Phase 6: Polish & cross-cutting

- [X] T020 In `references/typesafe-advisor.md`, document `excluded_subjects`, the reasons `sign_absent` and `structure_excluded`, which structures exclude which patterns, and that label–value lines are recognized only as bold labels or field lists of at least two items. Run `python3 scripts/validate-package.py`.
- [X] T021 Run quickstart sections 2–6: registry `--check` (including the negative check on a temporary copy), full suite, `python3 scripts/validate-package.py`, `python3 scripts/package-plugin.py`; confirm the rebuilt archives hold byte-identical copies of the changed `jev/` files, `jev/registry.json`, `SKILL.md` and `references/typesafe-advisor.md`; confirm the README pattern table and numbering are unchanged; record the measured check reduction on the ~1,000-word note against the estimate in research R1. Record outputs in `specs/011-structural-exclusions/evidence.md`. Do not commit `dist/`.
- [X] T022 Request an independent code and security review of the final diff covering label–value recognition on untrusted input (linear time, no catastrophic regex), exclusions never hiding source text from the ledger (FR-013), no source prose in new report fields, and the canonical traceability of every exclusion (SC-004); record findings and dispositions in `specs/011-structural-exclusions/evidence.md`.
- [ ] T023 Owner-only, in two parts. (a) Before T017: confirm, as a native speaker, each of the four rules and synthetic examples recorded in `calibration/LOG.md` by T016 (table cells, captions, tables of contents, checklist items); a structure the owner does not confirm is dropped from T017 and T019. (b) After T017 and T008: review the labels of the SC-003 fixtures in `tests/test_label_value.py` and the final V11 wording in `SKILL.md`. Record both outcomes in `specs/011-structural-exclusions/evidence.md`. The fixtures were labeled by the agent, not a native-speaker annotator.

---

## Dependencies & Execution Order

- **Setup (T001)** → **Foundational (T002–T003)** → every user story.
- **US1 (T004–T007)** depends on Foundational.
- **US2 (T008–T014)** depends on Foundational and, because it shares `jev/coverage.py`,
  `scripts/build-jev-registry.py` and `jev/registry.json` with US1, runs after US1.
- **US3 (T015–T019)** depends on US2 (the exclusion mechanism and label–value recognition). T016
  lands in an earlier commit than T017.
- **Polish (T020–T022)** last. T023 is split: part (a) runs after T016 and before T017, because
  constitution IV needs the evidence before the rule edit; part (b) runs after T017 and T008.

Within each story: tests first and failing, then implementation, then the checkpoint.

## Parallel Opportunities

- T005 (`tests/test_registry_exclusions.py`) can be written alongside T004.
- T008 (`tests/test_label_value.py`) and T010 can be written alongside T009.
- T018 (`calibration/ca-kiem-thu.md`) can run alongside T019 once T017 is done.

```text
After T003:  T004 tests/test_structural_exclusions.py | T005 tests/test_registry_exclusions.py
             then T006 → T007
After T007:  T008 tests/test_label_value.py | T009 | T010   then T011 → T012 → T013 → T014
```

## Implementation Strategy

- **MVP**: Setup, Foundational and US1. The T4 gate alone removes both observed T4 false flags and
  changes no rule text.
- **Next**: US2 (heading exclusions and label–value recognition), then US3 (the V11 rule change).
- Stop at each checkpoint, run the full suite, and record evidence before the next story.
