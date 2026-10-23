# Evidence — feature 011

Authority: on 2026-10-23 the owner authorized rebasing onto the new `main` and `speckit-implement`
for every user story that is not too complex, without commit or push. Rule maintenance for V11 is
authorized, but constitution IV and task T023 (a) require the owner to confirm the four
native-speaker rules recorded by T016 before the `SKILL.md` edit (T017). No key, network, live
service or real user text is used.

## T001 — starting state

- Branch `codex/011-structural-exclusions` at `5b7f6b1` (spec commit), rebased onto `origin/main`
  `8c83a33` (feature 010 merged as PR #20). The spec and plan still name `2670959` as the start;
  the runtime now also includes feature 010.
- Python 3.15.0 on Darwin arm64.
- `python3 -B -m unittest discover -s tests -t .`: `Ran 228 tests`, `OK`.
- ~1,000-word synthetic note from `SECTION` in `tests/test_preparation_limits.py`: 7,381 checks
  required, 180 T4 checks (90 subjects × 2 recipes, no subject contains `, và`), 86 checks on the
  first heading unit.

## T002–T003 — per-group subjects (Foundational)

- T002 guard (`tests/test_structural_exclusions.py`) pinned the check order of the first heading and
  prose units (86 and 222 checks, by digest), 7,381 checks required and 68 per sentence. It passed
  before any change (a guard, not a RED).
- T003 gave each target-scope group its own subject list with `positions` back to the unit's
  subjects, made `Ledger.checks` walk positions, mapped context-insufficiency to positions, and
  computed each sentence's `required` from the groups that include it. Guard unchanged;
  `Ran 229 tests`, `OK`.

## T004–T007 — T4 sign gate (User Story 1)

- RED: 7 of 8 tests failed for the intended reasons (T4 asked about every subject; no `gate` in the
  registry). The NFD case passed before the gate, as a guard against a naive gate.
- T006: the generator gained a `GATES` table (T4 `,\s+và\s`), checked against T4's **Dấu hiệu**;
  `build(root)` now takes a root so the negative check runs on a copy (`ValueError` when the sign is
  edited out). T007 filters T4's subjects on NFC editable text.
- Count changes by design (SC-005): the T002 guard went to 84/216 checks, 7,201 required, 66 per
  sentence; `tests/test_coverage.py::test_all_pattern_success_reconciles` 201 → 197 required and
  200 → 196 validated (two sentences without `, và`); `tests/test_evaluation_plan.py` missing
  groups 2,069 → 1,999 (70 T4 groups now fully excluded).

## T008–T014 — structure exclusions (User Story 2)

- The exclusion table for V2, V3, V5 and V14 was generated together with the gate in T006, so the
  registry part of T010 had no RED of its own; its negative build checks (each quoted phrase edited
  out raises `ValueError`) were written in T010 and pass.
- RED: label recognition (21 field-list and bold cases, first-sentence-only) and heading exclusion
  (V2/V3/V5/V14 asked on headings, by layout and by host annotation, and beside a candidate review)
  failed for the intended reasons. Guards that passed from the start: the label item still loses
  nothing before User Story 3, typography-only units keep `genre_gate`, and the 20 non-label lines.
- Implementation: `jev.preparation._mark_label_values` (bold label, or plain label in a run of at
  least two adjacent label items of the same list and indent; no threshold) and per-subject
  structure filtering in the ledger before the T4 gate. Label regexes run in 0.043 s and 0.012 s on
  800 KB adversarial lines.
- Count changes by design: the T002 guard went to 76/216 checks and 7,121 required; in
  `tests/test_evaluation_plan.py` heading units 0, 7, 14, 21 and 28 now pack 41 questions, 1,339
  answers and 1,959 missing groups.

## T015–T016 — V11 (User Story 3), stopped before the rule edit

- T015 RED: `V11RuleTest` fails because V11 is still asked about the title and the field-list date
  item. It is marked `expectedFailure` until T017, so the suite stays green.
- T016: `calibration/LOG.md` gained the entry dated 2026-10-23 (synthetic before text, comparison
  text, observed scores, three named differences, classification and decision, and the four
  native-speaker examples for table cells, captions, tables of contents and checklist items). The
  Vietnamese text was self-reviewed against `SKILL.md`.
- Stopped: T017–T019 wait for the owner to confirm the four rules and examples (T023 part a), as
  constitution IV requires evidence before the rule edit.

## T023 part a — owner confirmation

On 2026-10-23, before any edit to `SKILL.md`, the owner wrote: "T023 part a: I confirm, as a native
speaker, all four rules and examples in calibration/LOG.md (table cells, captions, tables of
contents, checklist items)." The calibration entry records the confirmation in row 3 and its note.

## T017–T019 — V11 rule maintenance (User Story 3)

- T017: V11's **Không flag** in `SKILL.md` gained one sentence naming titles, label–value lines
  (*Ngày: 22/10/2026*), table cells, captions, tables of contents and checklist items, with the
  reason (labels or item names, not lead-in clauses). The wording follows V3's "Không áp dụng
  pattern này cho …" and was self-reviewed against `SKILL.md`. `SKILL.md` stays at 486 lines; no
  pattern was added or renumbered, so the README table is unchanged.
- T018: `calibration/ca-kiem-thu.md` gained a V11 section: one prose case that must still be flagged
  and six anti-over-correction cases, one per named structure.
- T019: the generator's exclusion table gained V11 (`heading` and `label_value`), each quoted from the
  new text; the registry was regenerated (V11's `no_flag` text changed too). The `expectedFailure`
  marker on `V11RuleTest` was removed and it passes.
- Count changes by design: the guard went to 73/216 checks, 7,001 required, 66 checks for 50
  sentences and 63 for the 30 field-list label items; `test_label_item_loses_nothing_yet` became
  `test_label_item_loses_only_v11`; in `tests/test_evaluation_plan.py` the longer V11 text adds
  bytes to every request, so units pack 41 questions and headings 40 (1,307 answers, 1,924 missing).
- Measured reduction on the ~1,000-word note: 7,381 → 7,001 checks (380, 5.1%), equal to the
  estimate in research R1.
- Commit order (SC-006): the `calibration/LOG.md` entry must be committed before the `SKILL.md`
  edit; nothing is committed yet.

## T022 — independent code and security review

An independent reviewer (separate agent; the diff against `5b7f6b1`, spec, contract and tasks;
offline, no key) reported 1 blocking, 3 should-fix and several notes. Each was reproduced before
acting; fixes were test-first (`ReviewFixTest` in `tests/test_structural_exclusions.py`: 6 RED
failures recorded, then GREEN).

| ID | Finding | Disposition |
|---|---|---|
| 1 | `missing[]` named subjects by the group's own index after exclusions: with `--pattern T4` on `Tao về. Mày ở lại. Tao mua táo, cam, và lê.`, sentence 2 was reported as `[0,1]` | Fixed: `subject_positions` and `validated_keys` use the unit's subject indexes; `subject_range` is kept only when a group covers every subject. Advisor and contract updated. |
| 2 | Label recognition hid real V11 lead-ins (`**Lưu ý:** Điều quan trọng cần lưu ý là …`; `- Cần lưu ý rằng: …` beside `- Có thể thấy rằng: …`) | Fixed: a subject showing one of the pattern's own canonical signs is never structure-excluded, and a label ending in `rằng` or `là` is not a label. `Vậy thì sao:` / `Lý do rất đơn giản:` inside a two-item list remain recognized: accepted trade-off, documented here. |
| 3 | Adjacent items of different list kinds (`-` then `1.`) formed one field list | Fixed: marker kind must match. |
| 4 | `--scope selected` applied no structure exclusions | Not changed: the host's explicit targets are evaluated as given; documented in the advisor and contract. |
| N | Bold labels accepted digits, commas, punctuation and links | Fixed: bold labels use the same letters-and-spaces rule. |
| N | `--pattern T4` on text without `, và` reports `incomplete` (all excluded) | Kept (008 all-excluded contract); documented in the advisor. |
| N | Decomposed (NFD) labels and nested lists are not recognized | Kept: the safe direction. |
| N | Blanked protected spans can open T4 (`` `a`, `b` và `c` ``) | Kept: only adds checks. |
| N | `_editable` duplicates `core.editable_text`; a full run on 2,100 units takes 7–8 s against about 5 s; `excluded_subjects` grows reports | Kept: bounded; mostly the existing `Ledger.block` cost; noted for later. |
| N | V11 reason did not fit checklist items; LOG row 1 said "tiêu đề và heading" | Fixed: "vì đó là nhãn, tên mục hoặc việc cần làm …"; row 1 now "tiêu đề". The quoted generator phrases are unaffected. |
| N | Version stays 0.10.6 after a rule and runtime change | Release is a separate owner decision. |

Verified without finding (reviewer): only the contract pairs are excluded; T1, T5, T6, K3, V6 and
V20 still run on headings; positions mapping in `checks`, `finalize` and per-sentence `required`;
tiers consistent; no new prose in reports; requests only lose targets; regexes linear (under 35 ms on
1 MB); every quoted phrase is guarded by `build()`.

## PR #21 review fix — complete V11 signs

Automated review on PR #21 (commit `d713c87`) found that the structure-exclusion override used the
priority `signals`, a subset of V11's canonical signs: `**Lưu ý:** Điều này có nghĩa là …` and
`… việc kiểm tra lại … là điều cần thiết` lost V11. The generator now quotes V11's whole **Dấu hiệu**
list into `applicability_signs` (eight patterns; `X` becomes a bounded same-line gap) and fails the
check when the list changes; the ledger matches them case-insensitively.

- RED: both label-line cases lacked V11; the registry had no `applicability_signs`.
- GREEN: both keep V11; the build check fails when a sign is edited out of `SKILL.md`.

## T020 and checks

- `references/typesafe-advisor.md`: `excluded_subjects`, `sign_absent`, `structure_excluded`, the
  heading exclusions and the label–value forms.
- After US3: `Ran 248 tests`, `OK`; `build-jev-registry.py --check`, `validate-package.py` and
  `package-plugin.py` exit 0; the three archives in `dist/` hold byte-identical copies of
  `jev/coverage.py`, `jev/preparation.py`, `jev/registry.json`, `SKILL.md` and
  `references/typesafe-advisor.md`. `dist/` is not committed.

## Open

- T023 part b (owner review of the label fixtures and the final V11 wording).
