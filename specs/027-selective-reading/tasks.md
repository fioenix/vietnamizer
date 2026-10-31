# Tasks: Selective reading

## Setup
- [x] T001 Snapshot incoming files/archive hashes and baseline footprints in output/simplification-20261031/.

## Foundation
- [x] T002 Add failing relocated-owner/package contract coverage in tests/test_selective_reading.py.

## User Story 1 — local edit
- [x] T003 [US1] Replace SKILL.md with compact guards/routes and move unchanged V/T bodies to references/loi-*.md and references/typography.md.

## User Story 2 — articles and samples
- [x] T004 [US2] Add references/quy-trinh-viet.md and narrow resolver/profile/voice/evaluator eager loads; move source directory to references/nguon-van-phong.md.

## User Story 3 — canonical distribution
- [x] T005 [US3] Update scripts/validate-package.py and scripts/build-jev-registry.py bindings; adapt existing registry tests and regenerate jev/registry.json.
- [x] T006 [US3] Update AGENTS.md, docs/architecture.md, docs/patterns.md, docs/usage.md, docs/style-and-voice.md, docs/sources.md and docs/changelog.md; preserve README bytes and version.

## Verification and review
- [x] T007 Run relevant tests/validators; compare pattern parity and footprints; record specs/027-selective-reading/verification.md and measurements.json.
- [x] T008 Review guards/routes; validate labelled Unreleased packages and restore baseline dist hashes; record findings and pending behavioral A/B.

## Dependencies and execution
T001 → T002 → T003 → T004 → T005 → T006 → T007 → T008. Execute serially because source routing and package bindings overlap; no parallel implementation. US1 is the entrypoint slice; full deliverable includes US2/US3. No model costs/install/commit/push/release. Checkbox completion requires evidence in verification.md, not intent.


## Approved Matt-research follow-up
- [x] T009 Update SKILL.md review-only/independent verdicts and adapter invocation; keep existing rubric and add thin-input checks to references/quy-trinh-viet.md.
- [x] T010 Add benchmarks/review_contract.py, tests/test_review_contract.py and development/heldout-plan fixtures; verify exact candidate and supplied trace evidence without semantic claims.
- [x] T011 Record pinned provenance, refreshed footprints and local verification in specs/027-selective-reading/matt-followup.md; external commit/push/CI/review completion is tracked on PR28.
