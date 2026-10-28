# Tasks: Meaning-first reference voice

Input: spec.md and plan.md; owner approved P0/P1. Serial execution, no model runs.

## Phase 1: Setup
- [x] T001 Snapshot historical and owned source bytes in artifacts/022-meaning-first-20261028/history-before.json and before/.

## Phase 2: Foundation
- [x] T002 Record observed V1/example red cases in calibration/LOG.md and add MS01–MS16 expectations in calibration/ca-kiem-thu.md before rule edits.

## Phase 3: US1 — meaning first (MVP)
Independent check: every repaired example is source-supported; V1 added explanation is rejected.
- [x] T003 [US1] Add bidirectional proposition checks and remove vague-claim deletion permission in SKILL.md; constrain public expertise-card explanations in profiles/blog-ca-nhan/styles/chuyen-mon-cong-khai.md.
- [x] T004 [US1] Repair contradictory displayed examples and deletion guidance in profiles/blog-ca-nhan/rules.md, preserving all unique claims and qualifiers.

## Phase 4: US2 — scoped voice
Independent check: digit/idiom, mixed pronoun-function and technical-question positive/negative cases remain distinct.
- [x] T005 [US2] Add scoped notation/pronoun/rhythm extraction and meaning-first adaptation in references/giu-giong-tu-mau.md; clarify B6/B15 exclusions in profiles/blog-ca-nhan/rules.md.

## Phase 5: US3 — selective loading
Independent check: trace blog, SOP, mixed-function, typography-only and inline/unavailable-tools paths.
- [x] T006 [US3] Specify selective-loading order in SKILL.md; keep resolver/guide subordinate in references/bo-giai-phong-cach.md and references/giu-giong-tu-mau.md.

## Phase 6: Integration and verification
- [x] T007 Update README.md and all three version metadata files for source0.13.1; regenerate jev/registry.json through scripts/build-jev-registry.py; preserve runtime schema and55patterns.
- [x] T008 Run targeted package/registry tests, offline regression walk-through, required package/CLI validation and three-archive parity; save evidence in specs/022-meaning-first-voice/verification.md and artifacts/022-meaning-first-20261028/.
- [x] T009 Obtain independent patch review bound to before/ snapshot and final source; resolve findings, recheck affected proof and historical hashes, record final status in specs/022-meaning-first-voice/verification.md.

## Dependencies / opportunities
T001→T002→T003→T004→T005→T006→T007→T008→T009. US1 delivers safety contract independently; US2/US3 keep US1 invariant. Shared root/profile ownership makes serial work appropriate; no implementation parallel split. Independent read-only package tests may batch; final reviewer owns review only.

## Implementation strategy
Finish meaning-first MVP before voice/loading refinements. Use observed historical red examples as semantic reproducers and offline/manual acceptance cases. Static/package pass is not model behavior pass. No benchmark rerun, rescoring, Forms interaction, publish, global installation or commit.
