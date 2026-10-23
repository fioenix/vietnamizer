# Tasks: Runner cleanup

**Input**: [spec](spec.md), [plan](plan.md).
**Branch**: `codex/013-runner-cleanup`
**Approval**: short path authorized by the owner on 2026-10-23. Commits, push, merge and release each
need separate owner authorization.

**Tests**: RED before GREEN for each behavioral change, recorded in [evidence.md](evidence.md).
Synthetic text only; no key or network.
**Format**: `- [ ] Tnnn [USn?] Action with exact paths`.

## Phase 1: Setup

- [X] T001 Create `specs/013-runner-cleanup/evidence.md` with the starting revision, Python version,
  baseline suite output and the ledger build time on 2,100 units.

## Phase 2: User Story 1 — links and URLs with parentheses (P1)

- [X] T002 [US1] RED in `tests/test_preparation.py`: the four resolvable forms and two unbalanced
  forms of the spec, the prose-parenthesis edge case, and a 1 MiB parenthesis token within limits;
  rename the feature 009 test per the plan.
- [X] T003 [US1] GREEN in `jev/preparation.py` per plan D1 and D2.

## Phase 3: User Story 2 — unreadable input (P2)

- [X] T004 [US2] RED in `tests/test_jev.py`: CLI subprocess with a key on a missing path for
  `evaluate` and `prepare`, malformed input, and no key.
- [X] T005 [US2] GREEN in `jev/__main__.py` per plan D3.

## Phase 4: User Story 3 — one editable-text helper (P3)

- [X] T006 [US3] In `jev/coverage.py`, replace `_editable` per plan D4; run the suite and the guard;
  measure the ledger build time again.

## Phase 5: Polish

- [X] T007 Update `references/typesafe-advisor.md` (FR-007).
- [X] T008 Short independent review; reproduce findings, fix verified ones test-first.
- [X] T009 Run the suite, `build-jev-registry.py --check`, `validate-package.py` and
  `package-plugin.py`; record results in evidence.
