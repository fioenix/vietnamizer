# Tasks023

## Setup / foundation
- [x] T001 Freeze historical scope in artifacts/023-voice-patch-preflight-20261028/history-before.json and record approved design in specs/023-voice-patch-pilot/.
- [x] T002 Add red offline invariants in tests/test_voice_patch_versions.py and tests/test_voice_patch_analysis.py before new runner implementation.

## US1 — comparable outputs
- [x] T003 [US1] Implement new pinned derivative benchmarks/voice_patch_versions.py and benchmarks/voice_patch_analysis.py; verify packages/currentruntime and frozen input parity.
- [x] T004 [US1] Run targeted checks and obtain independent preflight review; freeze artifacts/023-voice-patch-pilot-20261028-v1/manifest.json.
- [x] T005 [US1] Execute52planned starts into artifacts/023-voice-patch-pilot-20261028-v1/attempts/, retaining full raw/errors and missing judgments.
- [x] T006 [US1] Analyze contrasts/meaning and manually review V1new propositions and16B/Ddiffs; report specs/023-voice-patch-pilot/results.md with exact examples and limits.

## US2 — auditable delivery
- [x] T007 [US2] Generate offline tables/SVG/PDF/before-after/ledger and captured-code reproduction in artifacts/023-voice-patch-pilot-20261028-v1/.
- [x] T008 [US2] Complete independent final review, historical rehash, seal/archive checksum and offline reproduction; record specs/023-voice-patch-pilot/verification.md.

Dependencies:T001→T002→T003→T004→T005→T006/T007→T008. No implementation parallel split. Read-only reviews scoped independently. Failure/missing input never grants reroll. Full benchmark is the requested deliverable, preparation alone is incomplete.
