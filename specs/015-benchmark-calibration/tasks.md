# Tasks: benchmark calibration

## Foundation
- [x] T001 Preserve old canonical files and record source-bound observations in calibration/LOG.md and artifacts/015-benchmark-calibration-20261026/observations.json.

## US1: preserve action
- [x] T002 [US1] Add action-ambiguity and positive repair cases in calibration/ca-kiem-thu.md, then clarify existing safeguard2 in SKILL.md.

## US2: limit collateral style edits
- [x] T003 [US2] Add punctuation/terminology counterexamples in calibration/ca-kiem-thu.md; clarify T2 and V19 in SKILL.md without changing triggers or inventory.

## US3: advisory independence
- [x] T004 [US3] Record bounded R001 prompt/advice trace in specs/015-benchmark-calibration/jev-trace.md; clarify references/typesafe-advisor.md and SKILL.md without changing frozen runners or thresholds.

## Delivery
- [x] T005 Regenerate jev/registry.json, synchronize patch0.11.1 metadata/README and mark old20sources development-only for future claims.
- [x] T006 Run targeted offline checks and independent review, verify historical raw/Forms preservation and record limits in specs/015-benchmark-calibration/results.md.

Dependencies:T001→T002→T003→T004→T005→T006. Serial; no implementation workers.

Receipt:33targeted tests pass;55registry definitions match, unchanged byte; package
source validator v0.11.1passes. Independent static review no blockers.5719historical
files unchanged; manual cases not model-tested; no new provider/Jev/Forms calls or release.
