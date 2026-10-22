# Tasks: Prioritized evaluation within a request budget

**Input**: [spec](spec.md), [plan](plan.md), [research](research.md), [data model](data-model.md),
[contract delta](contracts/evaluation-contract.md), [quickstart](quickstart.md).
**Branch**: `codex/010-long-document-evaluation`
**Approval**: The owner accepted the research R5 deviation and authorized task generation on
2026-10-22. This file is a backlog. Implementation, commits, push, merge, release and any live
service run each need separate owner authorization. Check a box only for verified work.

**Tests**: Required by constitution gate 1. Every behavioral change follows a test that fails first
for the stated reason; an import error or a missing attribute is not a behavioral RED. Record
RED → GREEN commands, revision and output in `specs/010-long-document-evaluation/evidence.md`. All
inputs are synthetic and every evaluation test uses a fake transport; no key, network or real user
text is used.
**Format**: `- [ ] Tnnn [P?] [USn?] Action with exact repository-relative paths`. `[P]` means
file-disjoint work once its prerequisites are done.

## Phase 1: Setup — evidence

**Purpose**: Freeze the starting state before any runtime change.

- [ ] T001 Create `specs/010-long-document-evaluation/baseline/measure_reach.py`, a script that builds the ~1,000, ~6,000 and ~12,100-word synthetic notes from `SECTION` in `tests/test_preparation_limits.py`, evaluates each with an always-valid fake transport (`tests.test_jev.response`) and prints units, checks required, validated, requests and units reached. Create `specs/010-long-document-evaluation/evidence.md` recording the starting revision, Python version and machine, the output of `python3 -B -m unittest discover -s tests -t .` (200 tests), and the script's output, which must match the table in spec Background (9 units reached; 7,381 / 44,281 / 89,299 checks). State the authority limits from the Approval line above.

**Checkpoint**: Starting state recorded; nothing in `jev/`, `scripts/` or `tests/` changed yet.

---

## Phase 2: Foundational — one static request plan

**Purpose**: Replace send-time packing with a plan computed before the first request and shared by
both commands (research R1), with today's order and behavior unchanged. Blocks every user story.

- [ ] T002 Create `tests/test_evaluation_plan.py` with a characterization test: evaluate the ~1,000-word synthetic note with an always-valid fake transport and pin today's request sequence as `(section ID, question count)` pairs, plus the `missing` reasons. It passes today; record in `evidence.md` that it is a guard, not a RED.
- [ ] T003 In `jev/core.py`, move the redaction and payload helpers now defined inside `evaluate` (`protected_matches`, `redact`, `candidate_state`, `question`, `project` and the per-section `common` state) into a module-level builder that both `evaluate` and `prepare` can construct from a prepared document. Behavior must not change: T002 and the full suite pass, and the redaction cache keeps its 1 MiB cap.
- [ ] T004 In `jev/core.py`, add a planner that returns the ordered request list (section, check keys) before any request, reproducing today's depth-first packing exactly, including per-key `context_too_large` and the 48-question, 48,000-byte and 16-target limits. Make `evaluate` send the planned requests in order; halting on replies stays as today. T002 and the full suite pass unchanged.

**Checkpoint**: One planner drives evaluation; observable behavior is identical to the starting
revision.

---

## Phase 3: User Story 1 — Spend a budget on the checks that matter most (Priority: P1) 🎯 MVP

**Goal**: A run spends at most X requests in tier order (candidate, focus, signal, spread) and
reports what each tier got and what was left.

**Independent Test**: With a fake transport, a ~1,000-word synthetic note with candidate edits late
in the document, two focus spans and a budget of 8 serves tiers in order; without an `evaluation`
object, at least 30 units get validated answers.

### Tests for User Story 1 ⚠️ write first, confirm they fail

- [ ] T005 [P] [US1] Create `tests/test_evaluation_priority.py` with RED tests for the `evaluation` input rules in `specs/010-long-document-evaluation/contracts/evaluation-contract.md`: `requests` "1 or more; above 32 is capped to 32 and reported; absent means 32" (`priority.budget_capped`), `requests` ≤ 0, non-integer or boolean is `invalid_input`; `focus` "schema 2 only", spans must be "source-global half-open code-point offsets inside the source" with "at most 256 spans", unknown pattern IDs are `invalid_input`, and a span only over protected text adds no checks. Each `invalid_input` case makes zero transport calls.
- [ ] T006 [US1] In the same new file `tests/test_evaluation_priority.py` (after T005, same file, so not parallel with it), add RED ordering tests from User Story 1: candidate edits in the last unit with budget 8 are all sent before any request is opened for a lower tier (SC-002); focus spans with and without `patterns` are served before any tier 3 or tier 4 request; with signal text such as `, và ` in some units only and no higher tier, those units' T4 checks are sent before any tier 4 request (SC-003); a request with room after its unit's higher-tier checks is filled with that unit's next checks; without an `evaluation` object, the ~1,000-word note gets validated answers in at least 30 units (SC-004); unsent checks carry `budget_exhausted` and `priority.tiers` gives planned, answered and missing per tier; every judgment carries its check's `tier` and every `missing` record a `missing_by_tier` count; identical input yields an identical request sequence; a note whose work fits within 32 requests, with no `evaluation` object, sends every check exactly once (FR-018).
- [ ] T007 [P] [US1] Create `tests/test_registry_signals.py` with RED tests: every signal in `jev/registry.json` is a top-level alternative of that pattern's expression in `scripts/scan-tells.sh` after translating `[[:space:]]` to `\s`, and matches, without line anchors, the pattern's own section of `SKILL.md` (FR-003, research R4); alternatives that do not match are absent (at `5420c8c`: `Thông qua` for V9, `Thêm vào đó` and `Chính vì thế` for V12, `triển khai thực hiện` for V15, and the whole V16 and V18 expressions); each signal compiles with `re.MULTILINE`; each scans 1 MiB of adversarial text (long `**` runs, spaces, `, ` repeats) in under 1 s.

### Implementation for User Story 1

- [ ] T008 [US1] In `scripts/build-jev-registry.py`, read the `scan "<ID> ..." '<regex>'` lines of `scripts/scan-tells.sh`, translate `[[:space:]]` to `\s`, compile each in Python, keep each top-level alternative only if it matches, without line anchors, the pattern's own `SKILL.md` section, list the dropped ones in the generator output, and write the kept ones as `signals: [<python regex>]` on the pattern entry; "Absent or empty means the pattern never reaches tier 3". Make `--check` fail when `scripts/scan-tells.sh`, `SKILL.md` and `jev/registry.json` drift. Record the kept and dropped alternatives in `specs/010-long-document-evaluation/evidence.md`. Regenerate `jev/registry.json` with `python3 -B scripts/build-jev-registry.py` and pass T007. Do not edit `scripts/scan-tells.sh`.
- [ ] T009 [US1] In `jev/core.py`, parse and validate the optional top-level `evaluation` object per the contract table (`requests`, `focus`; `previous` is accepted only from US3 on and is `invalid_input` until then). Charge each focus span one unit of the preparation work budget, as the data model states: "The 256-span cap and the per-span charge to the preparation work budget keep focus processing inside existing bounds". The object stays inside the input digest. Pass T005.
- [ ] T010 [US1] In `jev/coverage.py`, assign each check its highest tier per research R3: 1 `candidate` (the four review checks of each candidate edit); 2 `focus` (sentence- or unit-scope checks whose subject overlaps a focus span, and paragraph-scope checks of every overlapped unit, limited to the span's `patterns`); 3 `signal` (signal matched with `re.MULTILINE` against the unit's editable text with protected spans blanked: the matching subjects for target-scope patterns, the whole unit for paragraph-scope patterns); 4 `spread`.
- [ ] T011 [US1] In `jev/core.py`, change the planner to the tier order of research R3: open each request for the unit owning the highest-tier unplanned check, document order breaking ties; in tier 4 a unit not yet reached precedes any reached unit, where reached means an earlier entry in this plan targets it or one of its checks matched a key in the accepted previous block; fill with that unit's unplanned checks, tier ascending then today's within-unit order; stop at the budget. Report unplanned checks as `budget_exhausted` (replacing `limit_exceeded`; update the assertion in `tests/test_jev.py` `test_request_budget_keeps_unattempted_checks_visible`), add `tier` to every judgment, `missing_by_tier` and `missing_by_reason` to `missing` records, the latter with the precedence in `specs/010-long-document-evaluation/data-model.md`, and add the `priority` summary (`budget`, `budget_capped`, `tiers`, `units_reached`, `invalid_replies`) to `evaluate` reports. Pass T006 and the plan invariants in the data model: "at most `requests` entries", "every check appears in at most one entry", "the `tier` sequence is non-decreasing", "within tier 4, every entry for a unit not yet reached precedes any entry for a reached unit".
- [ ] T012 [US1] Run the full suite. Update T002's characterization in `tests/test_evaluation_plan.py` only where the order changed by design (tier 3 before tier 4) and record each change in `specs/010-long-document-evaluation/evidence.md`. Confirm that every other pre-existing test, in particular the request-count, time, memory and privacy assertions, passes unchanged (research R3 risk, SC-007). If one fails, stop and report instead of loosening it.

**Checkpoint**: US1 complete. Budget and tiers decide the work; reports say what each tier got.

---

## Phase 4: User Story 2 — Know what a budget buys before spending it (Priority: P1)

**Goal**: Network-free `prepare` returns the same plan `evaluate` will follow.

**Independent Test**: For the three synthetic sizes, `prepare`'s plan equals the receipts of an
always-valid fake-transport run, with and without an `evaluation` object.

### Tests for User Story 2 ⚠️ write first, confirm they fail

- [ ] T013 [US2] In `tests/test_evaluation_plan.py`, add RED tests: for the ~1,000, ~6,000 and ~12,100-word notes, each with no `evaluation` object, with budget 8, and with focus spans plus candidate edits, `prepare` returns `priority.plan` entries `{unit, start, end, tier, questions, tiers}` whose sequence equals the run's receipts (SC-001), and `priority.tiers` gives `planned` and `unplanned` per tier, which sum to the checks required after skipped previous answers (FR-007); a note whose preparation is incomplete yields a plan marked provisional; a unit whose context fits no request is listed as unreachable and gets no entry; no plan or priority value contains a fragment of the source text; `prepare` makes no transport call and needs no key; with the deadline expiring during planning (patch `jev.core.time.monotonic`), `evaluate` sends no request and both commands report the plan built so far with `deadline_exceeded` on every unplanned check (FR-010). Bound the 12,100-word case with a 30 s subprocess timeout and record the measured time in `evidence.md`.

### Implementation for User Story 2

- [ ] T014 [US2] In `jev/core.py` `prepare`, build the payload builder and planner from the prepared document without key or network and add the `priority` block with `plan`, per-tier `planned` and `unplanned`, `provisional` and `unreachable`, using exactly the planner `evaluate` uses. Keep the existing `prepare` fields. Pass T013.

**Checkpoint**: US2 complete. A host can read what a budget buys before any request.

---

## Phase 5: User Story 3 — Do not pay twice for the same check (Priority: P2)

**Goal**: A run given an earlier `answered_checks` block skips checks already answered for an
unchanged unit state and re-plans everything else.

**Independent Test**: Two chained fake-transport runs on the same synthetic note send no check twice;
editing one unit between them re-plans only that unit.

### Tests for User Story 3 ⚠️ write first, confirm they fail

- [ ] T015 [P] [US3] Create `tests/test_evaluation_previous.py` with RED tests: chained runs send no check twice and the second report counts only its own answers, listing skipped checks as `answered_previously` with `priority.skipped_previous` (SC-005); after editing one unit's text between runs, that unit's checks are planned again and no unchanged unit's answered check is; a changed register, context or candidate replacement re-plans the affected checks; a third run given the second block skips keys from both runs (`carried`); a block with another model, registry digest, `config_version`, `segmentation_profile`, a non-`full` `scope`, an `own` key not listed under its `receipts`, an `encoding` other than `answered-checks-v1`, a key that is not 16 lowercase hex digits or repeats across `own` and `carried`, more than 1,536 `own` keys, a `receipts` index out of range or naming one key twice, or a malformed `previous_digest` is `invalid_input` with zero transport calls; `own` holds at most 1,536 keys of 16 hex digits; `previous_digest` names the accepted block; without focus or candidates, the second run's tier 4 requests go to units the first run did not reach before any unit it reached (SC-005).

### Implementation for User Story 3

- [ ] T016 [US3] In `jev/coverage.py` (with the builder from T003), compute reuse keys as "`sha256(encoded([model, pattern_entry_digest, recipe_key, unit_state_digest, subject]))[:16]` hex", where `unit_state_digest` covers "the redacted unit state without `targets` or `edits`" and `subject` is "the redacted target text with its unit-local offsets, the candidate state, or `null` for paragraph scope". Compute keys only for checks being planned or answered.
- [ ] T017 [US3] In `jev/core.py`, accept `evaluation.previous` under the rules of research R5, the contract table and the data model's untrusted-input rules, validating and matching keys in linear time with a set and checking the deadline, remove checks whose key is in the block's `own` or `carried` lists before tier assignment, and add the `answered_checks` block (`encoding: answered-checks-v1`, `model`, `registry_digest`, `config_version`, `segmentation_profile`, `scope`, `own`, `carried`, `receipts`, `previous_digest`) to `evaluate` reports. Never count `carried` keys as answered and never start another run. Pass T015.

**Checkpoint**: US3 complete. Chained runs avoid repeats without claiming merged coverage.

---

## Phase 6: User Story 4 — One invalid reply does not end the run (Priority: P2)

**Goal**: An invalid reply drops its batch; the run continues and stops at the third.

**Independent Test**: A fake transport returning invalid replies at chosen requests.

### Tests for User Story 4 ⚠️ write first, confirm they fail

- [ ] T018 [P] [US4] In `tests/test_coverage_faults.py`, change `test_prior_batches_survive_atomic_failure` to the new contract (the run continues after the invalid second request) and add RED tests: an invalid reply at request 2 of a 32-request run is followed by at least 30 further requests and only that batch carries `invalid_response` (SC-006); invalid replies at requests 2, 5 and 9 send exactly 9 requests and mark every unsent planned check `invalid_response`; no batch is resent; each invalid receipt keeps only the fixed validation reason and check ID, never the provider body. Keep the existing deadline, transport-exception and cancellation tests unchanged; they still stop the run at once.

### Implementation for User Story 4

- [ ] T019 [US4] In `jev/core.py`, count invalid replies (`InvalidResponse` and the decoding errors that already map to `invalid_response`), mark the failed batch missing with `invalid_response`, continue with the next planned request, and stop at the third, marking every unsent planned check `invalid_response`; report `priority.invalid_replies`. Authentication failure, service failure, cancellation and the deadline still stop at once. Pass T018 and the full suite.

**Checkpoint**: US4 complete.

---

## Phase 7: User Story 5 — Hosts know what a partial result means (Priority: P3)

**Goal**: The advisor reference explains exit codes, the `evaluation` object, the plan and the
partial-run report.

**Independent Test**: Read `references/typesafe-advisor.md` against SC-008; the package validator
passes.

- [ ] T020 [US5] In `references/typesafe-advisor.md`, add a section on exit codes (0 for `evaluated`, `key_absent`, `prepared`; 2 for every other status; JSON on standard output in both cases), the `evaluation` object (`requests`, `focus`, `previous`), reading `priority.plan` before spending, the reasons `budget_exhausted`, `invalid_response` (stop at the third) and `answered_previously`, passing back only `answered_checks`, the limit of about 28 chained runs before carried keys fill the 1 MiB input, and what to tell the user for a partial run (counts per tier, what was not checked, not "checked by Jev", ask before spending more). Update the limits paragraph so it no longer implies one depth-first pass. Do not change `SKILL.md`. Run `python3 scripts/validate-package.py`.

**Checkpoint**: All user stories complete.

---

## Phase 8: Polish & cross-cutting

- [ ] T021 Run quickstart sections 2–6: full suite, `python3 -B scripts/build-jev-registry.py --check`, `python3 scripts/validate-package.py`, `python3 scripts/package-plugin.py`; confirm the rebuilt archives hold byte-identical copies of the changed `jev/` files, `jev/registry.json` and `references/typesafe-advisor.md`. Rerun `specs/010-long-document-evaluation/baseline/measure_reach.py` and record before/after units reached. Record outputs in `specs/010-long-document-evaluation/evidence.md`. Do not commit `dist/`.
- [ ] T022 Request an independent code and security review of the final diff covering untrusted input (`evaluation` object, `previous` block, focus spans), regex linearity of signals, budget enforcement, no source prose in plan, priority or answered-checks fields, and the two intended contract changes (invalid-reply continuation, `budget_exhausted`); record findings and dispositions in `specs/010-long-document-evaluation/evidence.md`.
- [ ] T023 Optional, owner-only: with the owner's spend approval, one live run on synthetic text with a small budget to confirm the plan matches live receipts; record only counts, reasons and digests in `evidence.md`.
- [ ] T024 Update the `scripts/scan-tells.sh` and `scripts/build-jev-registry.py` rows in `AGENTS.md` and the matching lines of the repository tree in `README.md` (around the `scripts/scan-tells.sh` entry): `scan-tells.sh` is no longer review-only, because its expressions, filtered against `SKILL.md`, become the registry's tier 3 signals; editing it or a canonical pattern section requires `python3 -B scripts/build-jev-registry.py` and `--check`. Do not change the README version history. Run `python3 scripts/validate-package.py`. Depends on T008.

---

## Dependencies & Execution Order

- **Setup (T001)** → **Foundational (T002–T004)** → every user story.
- **US1 (T005–T012)** depends on Foundational.
- **US2 (T013–T014)** depends on US1: the plan reports tiers and the `priority` block.
- **US3 (T015–T017)** depends on US1: skipped checks are removed before tier assignment and reported
  in the `priority` block.
- **US4 (T018–T019)** depends only on Foundational, but shares `jev/core.py` with US1–US3, so run it
  after the story currently editing `jev/core.py`, not alongside it.
- **US5 (T020)** after US1–US4, because it documents their final fields.
- **Polish (T021–T024)** last. T024 needs only T008 and may run any time after it.

Within each story: tests first and failing, then implementation, then the story's checkpoint.

## Parallel Opportunities

- T005 and T007 touch different files and can be written together; T006 follows T005 in the same
  file.
- T015 (`tests/test_evaluation_previous.py`) and T018 (`tests/test_coverage_faults.py`) can be
  written while US1 implementation is in progress, because they touch only test files; they must
  still fail for the stated reason when their implementation starts.
- T008 (`scripts/build-jev-registry.py`, `jev/registry.json`) is file-disjoint from T009–T010 once
  T007 exists.

```text
Example after T004:
  T005 tests/test_evaluation_priority.py   |  T007 tests/test_registry_signals.py
  then T006, then T008 | T009 → T010 → T011
```

## Implementation Strategy

- **MVP**: Setup, Foundational and US1. A host gets tier-ordered work within a budget and an honest
  report; this alone moves the ~1,000-word note from 9 to at least 30 units reached per run.
- **Next**: US2 (plan before spending), then US4 (small, high value for live runs), then US3.
- **Last**: US5 documentation and Polish.
- Stop at each checkpoint, run the full suite, and record evidence before the next story.
