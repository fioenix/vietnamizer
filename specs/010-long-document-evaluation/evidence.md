# Evidence — feature 010

Authority: the owner authorized `speckit-implement` for T001–T012 only (Setup, Foundational, US1)
on 2026-10-22, without commit or push. US2 and US3 are deferred. No key, network, live service or
real user text is used; every evaluation below uses a fake transport and synthetic notes.

## T001 — starting state

- Branch `codex/010-long-document-evaluation` at `4e44da9`, rebased on `origin/main` `1d118b5`
  (feature 009 merged as PR #19). The spec and plan still describe the branch as starting from the
  unmerged 009 tip; the runtime here is identical to that tip plus the PR review fix `2670959`.
- Python 3.15.0 on Darwin arm64 (maintainer machine).
- `python3 -B -m unittest discover -s tests -t .`: `Ran 201 tests in 108.223s`, `OK`. The time is
  higher than earlier runs (about 40 s) because the machine was under load; no test failed.
- `python3 -B specs/010-long-document-evaluation/baseline/measure_reach.py`:

```text
words=1000 units=70 required=7381 validated=1018 requests=32 units_reached=9 reasons={'inactive_profile': 1190}
words=6000 units=420 required=44281 validated=1018 requests=32 units_reached=9 reasons={'inactive_profile': 7140}
words=12100 units=847 required=89299 validated=1018 requests=32 units_reached=9 reasons={'inactive_profile': 14399}
```

This matches the table in spec Background (9 units reached; 7,381 / 44,281 / 89,299 checks).

## T002–T004 — static request plan (Foundational)

- T002 guard (`tests/test_evaluation_plan.py`) pinned the depth-first sequence at `4e44da9`: 32
  requests over units 0–8 (8–42 questions each), 1,018 answers, 2,270 missing groups
  `limit_exceeded`. It passed before any change (a guard, not a RED).
- T003 moved redaction and projection into `jev.core._Requests`; T004 added `_plan`, reproducing
  depth-first packing, and made `evaluate` send the planned requests. After T004 two tests failed
  because `_plan(..., budget=MAX_REQUESTS)` bound the limit at definition time, so tests that patch
  `jev.core.MAX_REQUESTS` no longer applied; the budget is now passed at call time. Then
  `Ran 202 tests`, `OK`, with the T002 sequence unchanged.

## T005–T011 — tier order (User Story 1)

- RED (before T008–T011): `tests/test_evaluation_priority.py` failed for the intended reasons
  (no `priority` field, `requests` ignored: `32 != 3`, invalid `evaluation` values accepted,
  depth-first order: first requests on one unit, 9 units reached). Two tests passed from the start
  and are guards: identical input gives identical requests, and work that fits is sent once.
  The first version of the fits-once test compared question names across requests, which are
  unique only within a request (`V12_paragraph_violation` repeats per unit); it now compares
  (unit, name).
- RED for signals: `tests/test_registry_signals.py` failed (no `signals` in the registry).
- T008 kept and dropped alternatives (generator output; grounding is case-insensitive and ignores
  line anchors, because the canonical sections quote signs in lowercase inside sentences):
  kept T2 `—`; T4 `, và `; T5 both forms; V11 all six phrases; V9 all but `Thông qua`; V12 all but
  `Thêm vào đó,` and `Chính vì thế,`; V15 all but `triển khai thực hiện`. Dropped V16 and V18
  entirely. This matches research R4. `jev/registry.json` gains 41 lines; `--check` passes.
- T009–T011 GREEN: 18 tests in `tests/test_evaluation_priority.py` and 3 in
  `tests/test_registry_signals.py` pass, including the plan invariants (opening tier never rises,
  each check at most once, unreached units first in tier 4).
- T012: the T002 characterization changed by design and was updated: the ~1,000-word note now gets
  one full request (42 questions) in each of units 0–31, 1,344 answers, all missing groups
  `budget_exhausted`. `tests/test_jev.py` now expects `budget_exhausted` instead of
  `limit_exceeded`. No other pre-existing test changed.

## T018–T019 — invalid replies (User Story 4)

The continuation code was written together with the T011 planner, before its tests. To keep a real
RED, the new and changed tests in `tests/test_coverage_faults.py` were run against `4e44da9` in a
temporary worktree: 3 failures (`2 != 4`, `2 != 32`, `2 != 9`: the old runner stops at the first
invalid reply). On the new code they pass: one invalid reply loses only its batch and 32 requests
are sent; invalid replies at requests 2, 5 and 9 send exactly 9; no batch is resent; invalid
receipts keep only `{"reason"}`, and a provider body marker never reaches the report.

## T020, T024 — documentation

- `references/typesafe-advisor.md`: the limits paragraph now points to a new section "Request budget
  and partial runs" (the `evaluation` object, tier order, invalid-reply rule, `priority`, reasons,
  what to tell the user, exit codes 0 and 2).
- `AGENTS.md` and `README.md`: `scripts/scan-tells.sh` is described as the source of the registry's
  priority signals, and `--check` is required when it changes.
- The new Vietnamese lines were reviewed with the vietnamizer skill. The host check found
  `key_available`, so the runner was tried live on those three lines only, with
  `evaluation.requests: 3`: 3 receipts `validated`, 3 units reached, status `incomplete` by
  budget. The advisory flags above 0.4 (V11, T5, V3, V7 at 0.42–0.57) named no error the host could
  confirm (no lead-in clause, no label colon, table cells, a real `của` relation), so no line was
  changed. This was not T023's synthetic owner-approved run; it is recorded here as the skill's own
  required attempt.

## T021 — verification

- `python3 -B -m unittest discover -s tests -t .`: `Ran 222 tests`, `OK` (final run, after the
  evidence and task marks).
- `python3 -B scripts/build-jev-registry.py --check`, `python3 scripts/validate-package.py` and
  `python3 scripts/package-plugin.py` exit 0. The three archives in `dist/` hold byte-identical
  copies of `jev/core.py`, `jev/coverage.py`, `jev/preparation.py`, `jev/registry.json` and
  `references/typesafe-advisor.md`. `dist/` is not committed.
- `measure_reach.py` after the change:

```text
words=1000 units=70 required=7381 validated=1344 requests=32 units_reached=32
words=6000 units=420 required=44281 validated=1344 requests=32 units_reached=32
words=12100 units=847 required=89299 validated=1344 requests=32 units_reached=32
```

Units reached rose from 9 to 32 and answers from 1,018 to 1,344 per invocation (SC-004).

## T022 — independent code and security review

An independent reviewer (a separate agent given the diff against `4e44da9`, the spec, contract and
task list; offline, no key) reported 1 blocking, 3 should-fix and 5 notes. Each finding was
reproduced by the parent before acting. Fixes were made test-first; RED was recorded on the
pre-fix working tree.

| ID | Finding | Disposition |
|---|---|---|
| B1 | The T5 signal `^\s*[-*] \*\*[^*]+:\*\*` is quadratic on newline runs (`\s` crosses lines): 5k/10k/20k newlines took 0.13/0.53/1.98 s alone; the reviewer measured 117 s inside `evaluate` on a 300 KB input, past the 120 s deadline | Fixed. The generator now keeps grep's line semantics: `[[:space:]]` becomes `[ \t]` and every negated class excludes `\n`. `assign_tiers` also checks the deadline per group. RED: linearity test timed out after 30 s; line-semantics test failed on both T5 signals. GREEN: both pass; 500k newlines take about 0.01 s. |
| S1 | Packing a unit no longer checked the deadline (22.9 s against a 3 s deadline in the reviewer's run) | Fixed: deadline checked before every key. RED: 20.35 s against a 1 s deadline; GREEN under 6 s with `deadline_exceeded`. |
| S2 | After an early stop, work the plan never reached is `budget_exhausted`, not the stop reason | Not adopted. FR-006 and the contract keep checks the budget never reached as `budget_exhausted`; planned checks a stop prevented carry the stop reason. The advisor now says to read the receipts for the stop before suggesting a larger budget, and a guard test pins the split. |
| S3 | One oversized check relabeled its whole group `context_too_large` (123,052 checks in the reviewer's case) | Fixed: the oversized check gets its own `context_too_large` reason and the group a separate `oversized` flag for context completeness. RED: `0 not greater than 100000` budget_exhausted; GREEN. |
| N1 | Skipping an oversized top-tier check filled the request with the same unit's lower-tier checks, ahead of another unit's tier 2 | Fixed: after skipping, the planner chooses again. RED: first request went to the candidate unit; GREEN: it goes to the focus unit. |
| N2 | `numeric_tokens_preserved` is now computed for every unblocked unit, including units the budget never reaches | Kept: local, harmless and more complete; recorded as a change beyond the spec. |
| N3 | Anchored V9/V12 signals only match at line starts, so mid-paragraph connectors never reach tier 3 | Kept: matches research R4 and grep's own behaviour. |
| N4 | `prepare` does not parse `evaluation`; `evaluate` prepares before rejecting a bad object | Kept: User Story 2 (plan in `prepare`) is deferred. |
| N5 | Memory grows: a chosen unit's key list is materialized; `finalize` walks every missing check | Kept: bounded by the 4,096-item inventory; existing memory assertions pass. |

Verified without finding (reviewer): budget never exceeded, each check sent at most once, invalid
reply continuation and stop at the third, halts, input validation, no source prose in the new
fields, redaction unchanged, `--pattern` and selected scope.

After the fixes: `Ran 227 tests`, `OK`; `build-jev-registry.py --check`, `validate-package.py` and
`package-plugin.py` exit 0.

## Open

- T023 owner-only synthetic live run: not done.
- T013–T017 (User Stories 2 and 3) remain deferred by the owner.

## PR #20 review fix — focus over protected text

Automated review on PR #20 (commit `a344d0a`) found that a focus span lying entirely inside an
inline protected range (inline code) still promoted the surrounding sentence and paragraph checks
to tier 2, against the contract row "focus span only over protected text — accepted; adds no
checks". Tier 2 now requires the focus span and the subject to share at least one code point outside
the unit's protected spans.

- RED: `test_focus_inside_inline_code_does_not_promote_its_unit` (two paragraphs, focus on `foo`
  inside the second one's inline code, budget 1) sent its only request to the second paragraph.
- GREEN: the request goes to the first paragraph and tier 2 plans nothing; full suite
  `Ran 228 tests`, `OK`; `build-jev-registry.py --check` and `validate-package.py` exit 0.
