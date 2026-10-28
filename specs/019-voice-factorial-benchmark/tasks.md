# Tasks019 — serial, bounded public-author pilot

## Setup and foundations
- [x] T001 Record approved public-author amendment and source eligibility in specs/019-voice-factorial-benchmark/spec.md and artifacts/019-public-author-pilot-20261027-v2/corpus.json.
- [x] T002 Pin source/runtime metadata and historical preservation baseline in artifacts/019-public-author-pilot-20261027-v2/.
- [x] T003 Add RED tests for ledger/parity/blinding/evidence/calibration in tests/test_voice_pilot.py and stream/tool guard tests in tests/test_voice_guard.mjs.

## US1/US3 — fixed four-arm execution
- [x] T004 [US1] Implement benchmarks/voice_pilot.py and benchmarks/voice_guard.mjs with global56start cap, one fresh session per cell, full binary raw and no retries.
- [x] T005 [US3] Independently review frozen corpus/source/agent/config/ledger before inference; save evidence under artifacts/019-public-author-pilot-20261027-v2/.
- [x] T006 [US1] Run four judge calibration calls, then four neutral-draft calls and32Codex edits within the same ledger; keep failures visible.

## US2 — blinded judgment and analysis
- [x] T007 [US2] Run16blinded main judgments, validate evidence, and report per-judge/stratum contrasts and limitations in specs/019-voice-factorial-benchmark/results.md.

## US4 — delivery
- [x] T008 [US4] Reproduce offline analysis, audit interpretation/raw, rehash history and archive all new data/code/metadata separately under artifacts/019-public-author-pilot-20261027-v2/.

Dependencies: T001–T005 before any model; calibration before draft/edit/judge stages. No parallel implementation writers. Independent provider cells may run at most2concurrently after reservation. No new rule tuning, Forms access or publication.
