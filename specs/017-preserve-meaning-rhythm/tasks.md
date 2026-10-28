# Tasks: preserve meaning and rhythm

## Setup and evidence
- [x] T001 Pin source0.12.0 and historical/benchmark hashes in artifacts/017-meaning-rhythm-calibration-20261027/; load spec/plan/constitution and validate checklist.
- [x] T002 Record observed counterexamples, contexts and host-label uncertainty in calibration/LOG.md and local observations.json before editing rules.

## US1 — Meaning and contextual ellipsis
- [x] T003 [US1] Update safeguards/V1 and paragraph review in SKILL.md; retain source ambiguity, positive complement repair and final-only output.

## US2 — Punctuation and quote boundaries
- [x] T004 [US2] Replace unconditional dash correction in SKILL.md T2 with functional/context/style checks; clarify actual verbatim vs emphasis and T3 without weakening unknown/protected input handling.

## US3 — Regression, parity and delivery
- [x] T005 [US3] Add MR01–MR12 in calibration/ca-kiem-thu.md, pin source/candidate mappings and uncertainty in observations.json; distinguish observed vs synthetic cases and unrun behavior.
- [x] T006 [US3] Update V1/T2/T3 recipes in scripts/build-jev-registry.py; capture source/registry parity RED before regenerating jev/registry.json; sync source0.12.1 manifests and README.md.
- [x] T007 [US3] Run targeted Jev/source-gate/package checks and build local archives; inspect instruction/registry/case bytes and one skill per archive.
- [x] T008 [US3] Independently review final source/recipe/expectation consistency; verify23,469historical files unchanged, save logs/source/patch/package hashes and results.md, archive delivery without new inference/Forms.

Dependencies:T001→T002→T003→T004→T005→T006RED→regenerate→T007→T008.
Single implementation writer. No implementation children or parallel edits; one bounded
independent review is permitted by requesting-code-review after source is ready.
Full suite and new model/Jev runs are excluded; no extension hooks configured.

Closure:41offline tests pass on final source, source/registry validation and actual
three-ZIP parity pass,12manual expectations statically reviewed,23,469protected
files unchanged. Archive017-meaning-rhythm-calibration-20261027.tar.gz verified58
payloads, SHA256a5220911197be79ddded89ac7937ebca6c082630f339d0eddfe22b730c7f7d8a.
Its tasks snapshot precedes this final archive-completion tick; this file records closure.
No benchmark generation, Jev API, Forms access, install or release.
