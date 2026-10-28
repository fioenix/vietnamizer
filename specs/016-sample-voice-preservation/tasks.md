# Tasks: supplied-sample voice preservation

- [x] T001 Pin public source files, licenses, hashes and method decisions in research.md and artifacts/016-voice-preservation-research-20261026/sources.json.
- [x] T002 [US1] Add original references/giu-giong-tu-mau.md and conditional pointers in SKILL.md and references/bo-giai-phong-cach.md.
- [x] T003 [US2] Add eight positive/negative manual VG cases in calibration/ca-kiem-thu.md, covering weak/absent evidence, context and protected material.
- [x] T004 [US3] Document style-vs-content feedback and explicit-only persistence; update README.md/AGENTS.md sources and tree.
- [x] T005 Demonstrate archive-inclusion RED in tests/test_package_security.py; extend scripts/validate-package.py exact allowlist, source version and manifests; verify targeted archive/plugin paths.
- [x] T006 Independently review, preserve old data and source0.11.1baseline, record checks and untested-efficacy limits in results.md.

Dependencies:T001→T005RED→T002→T003→T004→T005implementation→T006. Serial, no implementation workers.

Receipt:6targeted package consumer tests pass; observed inclusion RED before implementation.
Source validator v0.12.0/55patterns and registry check pass;3actual ZIPs include the new
reference byte-identically and one skill each. Independent static review no blockers.
5719historical data files unchanged. No new inference/Jev/Forms, personal profile,
external skill installation, publishing or native-invocation/voice-quality claim.

## Owner-approved Mindfio execution extension — 2026-10-27

- [x] T007 [US1] Preserve approved profile/original preparation archive; verify public-page correspondence and freeze local inputs/config/source/prompts in artifacts/017-mindfio-run-20261027-v1/ and reconciled v2/.
- [x] T008 [US1] Add offline oracle tests in tests/test_mindfio_pilot.py for strict raw completion/tool rejection, prompt treatment isolation, start cap and source tamper detection; observe RED before benchmarks/mindfio_pilot.py implementation.
- [x] T009 [US1] Implement benchmarks/mindfio_pilot.py with exactly12 planned fresh Codex starts, raw stdin/stdout/stderr, no silent retry and deterministic before/after outputs.
- [x] T010 [US1] Run12 outputs with frozen source0.12.0 and approved profile; verify schema, distinct sessions, zero operational calls, hashes and recorded runtime/usage.
- [x] T011 [US2] Produce descriptive per-cell metrics, reviewable before/after diffs and exploratory evidence-linked quality findings in specs/016-sample-voice-preservation/mindfio-results.md; no quality percentage or causal population claim.
- [x] T012 [US3] Verify community-derived source integration and package payloads, independently review harness/report, prove historical preservation, update README.md/AGENTS.md and archive all new evidence separately.

Dependencies:T007→T008RED→T009→T010→T011→T012. No source-rule tuning during
generation. Raw preservation and twelve-start cap take priority over retrying failures.

Final receipt:12/12 outputs,12 unique sessions,1 original start recovered offline +11
new starts;9harness and6package tests pass. Two descriptive scientific figures viewed,
all3ZIPs checked,5,772protected historical/preparation files unchanged. Independent
scoped review no blockers. Archive017-mindfio-pilot-20261027.tar.gz verified245payloads,
SHA2564e798bedc09799fd0837258b3b75b6e86e9939bf6fac41b7e0db9440a3f243a3.
No liveForms/Jev/fullsuite/install/release. No extension hooks configured.
