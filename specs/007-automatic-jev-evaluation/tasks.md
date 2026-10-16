# Tasks: Automatic Jev evaluation

Input: accepted spec.md, plan.md, research.md, data-model.md and contracts/cli.md.
Reconciled with installed speckit-tasks after authorized Codex bootstrap. Existing work and observed RED/GREEN evidence retained in evidence.md; no design approval was restarted.

## Phase 1: Setup

- [X] T001 Record the owner-approved active-advisory amendment in `.specify/memory/constitution.md` and `specs/007-automatic-jev-evaluation/spec.md`.
- [X] T002 Verify Python standard-library layout and ignored local integration/cache paths in `.gitignore`, `jev/__init__.py` and `CONTRIBUTING.md`.

## Phase 2: Foundational

- [X] T003 Add RED tests for exact 55 IDs and canonical exclusions in `tests/test_jev.py`; implement `scripts/build-jev-registry.py` and `jev/registry.json` and verify GREEN.
- [X] T004 Validate section profile blog/technical/typography-only, kind prose/heading/list/protected, unique ASCII IDs and nonoverlapping Python character spans in `jev/core.py`, with fixtures in `tests/test_jev.py`.

## Phase 3: User Story 1 — Automatic evaluation (P1)

Independent test: a fake injected key with isolated transport schedules all applicable questions and accounts for all 55 patterns without contacting a service.

- [X] T005 [US1] Add RED routing/coverage/full-paragraph tests in `tests/test_jev.py`; implement batching and current input/model/registry bindings in `jev/core.py`.
- [X] T006 [US1] Preserve full paragraph and supplied related context, target offsets and protected-region redaction in `jev/core.py`; verify fixtures in `tests/test_jev.py`.
- [X] T007 [US1] Add regression tests and fix protected-only default targets and document-wide T3 nested quotation handling in `tests/test_jev.py` and `jev/core.py`.

## Phase 4: User Story 2 — Offline behavior (P1)

Independent test: absent/whitespace keys produce zero HTTP calls, and the extracted CLI succeeds before reading input.

- [X] T008 [US2] Add no-key/permission tests in `tests/test_jev.py`; implement injected-key-only status/evaluate operations in `jev/__main__.py` and `jev/core.py`.
- [X] T009 [US2] Document capability_unavailable and standalone core editing in `SKILL.md` and `references/typesafe-advisor.md`.

## Phase 5: User Story 3 — Failures and incomplete evidence (P1)

Independent test: invalid model/schema/distributions, request limits, denied transmission and elapsed deadlines remain non-pass and cannot echo prose/secrets.

- [X] T010 [US3] Add RED response/limit/error tests in `tests/test_jev.py` and `tests/test_jev_transport.py`; implement bounded fixed-origin transport without redirects in `jev/transport.py`.
- [X] T011 [US3] Reproduce deadline and serialization review findings; share exact request bytes, kill timed-out I/O workers and reject late replies in `jev/transport.py`, `jev/core.py` and their tests.
- [X] T012 [US3] Add sanitized invalid-response field diagnostics in `jev/core.py`; preserve the historical failure and exact-payload diagnostic outcome in `specs/007-automatic-jev-evaluation/evidence.md`.

## Phase 6: User Story 4 — Pattern judgments and candidates (P2)

Independent test: candidate guards remain separate; every ordinal Score has a separate sufficiency judgment and cannot become usable when context is missing.

- [X] T013 [US4] Implement English per-pattern Noul/Choice/Score recipes and source exclusions in `scripts/build-jev-registry.py` and `jev/registry.json`.
- [X] T014 [US4] Add RED context-sufficiency tests in `tests/test_jev.py`; expose ignored-score dispositions while preserving distributions in `jev/core.py`.
- [X] T015 [US4] Add per-candidate meaning/new-claim/improvement/voice tests and numeric/protected constraints in `tests/test_jev.py`; implement advisory-only candidate reviews in `jev/core.py`.

## Phase 7: Distribution and final verification

- [X] T016 Add an extracted-runtime RED test, package exactly five runtime files and preserve synchronized version 0.10.0 across `scripts/package-skill.sh`, `scripts/validate-package.py`, tests, manifests and `SKILL.md`.
- [X] T017 Reconcile automatic workflow, privacy, errors, Score dispositions and canonical ownership in `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `PRIVACY.md` and `references/typesafe-advisor.md`.
- [X] T018 Run all offline tests, registry/package validation, Skills listing and both Claude validations; record final observations in `specs/007-automatic-jev-evaluation/evidence.md`.
- [X] T019 Rebuild/extract all three archives, compare runtime bytes and run a permitted synthetic shipped-CLI smoke; record exact model, usage, latency and incomplete statuses in `specs/007-automatic-jev-evaluation/evidence.md`.
- [X] T020 Recheck code/security review findings on final affected bytes and spec alignment; record limitations and final file bindings in `specs/007-automatic-jev-evaluation/evidence.md`.

## Dependencies and execution strategy

Phase 1 → Phase 2 → US1; offline/failure/candidate work uses the same runtime files and executes serially. All stories precede final distribution checks. The minimal usable slice is US1 plus offline/failure safeguards; the authorized delivery includes all four stories.

Independent checks may run concurrently: US1 registry check and transport tests; US2 source status and extracted status; US3 malformed fixtures and deadline fixture; US4 recipe check and candidate fixture after shared edits stop. No parallel writers or implementation children are needed.

## Execution ledger

Canonical workflow read through approved Obsidian CLI. Spec Kit owns artifacts and execution; installed speckit-implement resumed accepted work after owner-approved local Codex bootstrap. No extension hook file/checklists directory exists. Bootstrap preserved the twelve existing shared infrastructure files. Current checkout is retained, with no commit/push/shared skill installation/release authority.

All 55 definitions share one runner; individual-pattern runs explicitly declare diagnostic coverage. Failures preserve attempted/validated counts and never satisfy evaluation coverage. Historical live invalid_response remains evidence even when the exact-payload diagnostic succeeds.

## Phase 8: Convergence

- [X] T021 Update stale no-runtime distribution claims in `docs/plugin-distribution.md` per FR-035 (partial); distinguish automatic permitted evaluation from offline packaging tests.

Final checkpoint: all 21 tasks verified against the evidence in evidence.md. Python 3.12 and 3.15 full suites each passed 72 tests; current runtime hashes match independent re-review and all extracted archives. Installed-copy live smoke completed all applicable checks. Historical invalid_response bad field remains unrecoverable and is explicitly documented, not claimed fixed. No extension hooks are configured.

## Phase 9: Owner-authorized independent reviews and draft PR

Owner authorized branch separation, Claude Code and Antigravity review, finding fixes, targeted verification and draft PR on 2026-10-16. No merge authority.

- [ ] T022 Separate only feature 007 changes onto `codex/007-automatic-jev-evaluation` based on current `origin/main`; preserve the former branch and unrelated README commit.
- [ ] T023 Obtain independent read-only Claude Code runtime/security/package review and Antigravity spec/rubric/context/overediting review on the same immutable feature revision.
- [ ] T024 Reproduce and dispose actionable findings, run affected/final checks, and record exact reviewed/tested revisions in `specs/007-automatic-jev-evaluation/review.md`.
- [ ] T025 Push the dedicated branch, create and attach a draft PR against `main`, verify draft/head/base state and leave unmerged.
