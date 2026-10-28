# Tasks: Editorial Benchmark — historical pilot and current public cohort

Current state: see CURRENT.md. Earlier pilot checkpoints are preserved as history.
The active public cohort is80Codexoutputs; T006Gemini isolation, T015missing historical
raw causes and T029superseded source-first forms are not unfinished work to resume
automatically. Human quality T016 remains pending.

The original three-arm execution is retained below. The fourth-arm amendment is tracked
separately; adding its scope is approved, owner approved a USD 2 Jev ceiling on 2026-10-25; Codex execution is now authorized.

## Setup and foundation
- [x] T001 Record approved pilot scope, design and runtime research in specs/014-editorial-benchmark/plan.md.
- [x] T002 Write failing contract tests in tests/test_editorial_pilot.py for contamination, missing output, immutable resume and duplicate cells.
- [x] T003 Create twenty original synthetic cases in benchmarks/pilot-cases.json, draft labels and source provenance.

## US1 — Run comparable editing trials
- [x] T004 [US1] Implement frozen prompts, Codex/Agybird adapters and attempt ledger in benchmarks/editorial_pilot.py.
- [x] T005 [US1] Independently review benchmarks/editorial_pilot.py and resolve blocking findings before live execution.
- [ ] T006 [US1] Execute six-cell smoke then remaining bounded batches under artifacts/014-editorial-pilot/; account for all 120 cells.

## US2 — Inspect evidence
- [x] T007 [US2] Produce operational report and blinded review packet under artifacts/014-editorial-pilot/.

## US3 — Summarize evidence honestly
- [x] T008 [US3] Record actual generation, validation limits and remaining semantic review in specs/014-editorial-benchmark/pilot-results.md and README.md.

## Dependencies and execution
T001 → T002/T003 → T004 → T005 → T006 → T007 → T008. Work serially; no implementation
agent split. The two independent runtime subprocesses may run concurrently in a bounded batch.
Each story has observable output: US1 attempts, US2 recomputable report, US3 evidence links.
The 100-document holdout and two-reviewer quality evaluation are deferred, not completed by pilot.

## Current execution limit

T006 remains open: 60 Codex + 10 Gemini outputs, one quarantined Gemini cell, 49 unattempted.
Automatic approval review blocked further host-CLI Gemini generation; see isolation-gate.md.
T007/T008 deliver the current partial evidence, not acceptance of the 120-output target.

## Fourth arm — Codex first

- [x] T009 Record the fourth-arm protocol, matched revision control and proposed Jev budget in jev-extension.md; align spec, plan, data model and README.
- [x] T010 Record owner approval for the USD 2 Jev ceiling; `python3 -B -m jev status` verified key_available without exposing credentials. Official fixed-origin transport retained.
- [x] T011 Add failing targeted tests and implement a separate extension epoch: paired draft bindings, bounded Jev calls, spend reservations, failure/coverage receipts and matched Codex revision passes. Preserve the old three-arm runner behavior.
- [x] T012 Independently review the extension and pass its targeted tests before inference. Reviewer approved one paired-case smoke after the 26-test run and independent lossless-encoding audit; full-run continuation depends on actual smoke receipts.
- [x] T013 Execute the amended v2 accounting pilot: all 40 Codex starts completed; account for all 20 source cases with 2 partial / 1 unavailable / 17 not-attempted Jev dispositions, 33 requests inherited/new, no retries, within USD 2. Jev treatment completion remains unmet and is not a quality pass.
- [x] T014 Export 80 blinded outputs, separate review keys and two unscored reviewer worksheets; record operational report and codex-jev-results.md. Quality assessment remains open under T016.

T009 → T010; T011 → T012; both T010 and T012 gate T013 → T014. Implementation can proceed
offline before T010; no paid inference can. Antigravity remains independently gated by isolation-gate.md.

Extension verification so far: `python3 -B -m unittest tests.test_jev_pilot tests.test_editorial_pilot`
passes 26 tests. RED before implementation and RED before reconciliation/encoding fixes were
observed. Offline fake-response audit on all 20 frozen cases: 0 candidate omissions, 2–26 planned
requests, largest encoded revision prompt 648621 bytes (<1000000 guard). No full suite run.


## v2 disposition and remaining blocker

After P01/P02, the core-input digest mismatch was reproduced and fixed with separate encoding
checks. New v2 manifest inherits all 23 requests/reservations/evaluations without mutation or
retry. Read-only independent review cleared v2 partial/unavailable Codex smoke, then P03.
P03 added 10 requests (9 validated), then a third unvalidated request tripped the global circuit.
No later source is sent to Jev. Retained valid advice remains partial; fallback is not treatment.

- [ ] T015 [US1] Diagnose unvalidated-request phases with safe transport/validation/artifact diagnostics before any new Jev run. Existing raw failures lack enough detail to establish cause; do not call it a provider outage or retry failed cells. Record a new reviewed protocol before further inference.
- [ ] T016 [US2] Obtain two independent Vietnamese-proficient human reviews using reviewer-guide.md and the blinded packet; preserve original reviews and adjudication before quality claims.

Latest targeted verification: 32 tests pass, including inherited partial/unavailable end-to-end,
byte-identical provenance, encoding round-trips and circuit-breaker no-dispatch. No full suite.

- [x] T017 [US2] Preserve all available raw epochs and source snapshot; export analysis tables and data dictionary; package local tar.gz and independently verify 937 payload digests / CSV counts/archive checksum. Record provenance and unrecoverable gaps in data-archive.md. No new inference.


## Authorized recovery after archival

- [x] T018 [US1] Add failing tests and benchmark-only raw transport capture in benchmarks/jev_capture.py and tests/test_jev_capture.py; separate HTTP/network/deadline/JSON/validation/artifact errors without credentials.
- [x] T019 [US1] Implement cumulative budget/exact replay, recorded diagnostic and bounded recovery in benchmarks/jev_recovery.py with tests/test_jev_recovery.py; preserve all v1/v2 bytes and count their spend once.
- [x] T020 [US1] Independently review capture/recovery, run recorded diagnostics, distinguish observable harness defects from unrecoverable old causes, and verify corrective behavior before remaining paid calls.
- [x] T021 [US1] Receive all required Jev answers and new Codex+Jev finals for 20 documents within USD 2 cumulative; preserve native context abstentions, retries, failures and exposure state separately from execution completion.
- [x] T022 [US2] Refresh research tables, full raw archive/checksums and README evidence after execution; retain prior snapshots.

T018→T019→T020→T021→T022. T016 independent human review remains required for quality claims.

- [x] T023 [US1] Review/test a frozen per-question recovery adapter for the observed score/choice distribution inconsistencies. Preserve valid answers and all raw provider replies, seal composite provenance and reconcile actual source usage before repairing only invalid checks. This amendment gates affected T021 cases; no numerical tolerance changes.

Recovery verification: 50 targeted tests passed; reviewed capture/recovery/finish/composite
adapters and observed P05 live repair preserving 39 valid answers, requesting only one invalid
Score, receiving all 952 answers, then completing a new Codex final. Raw old failures remain
unrecoverable; T015 is not a claim that their historical root cause is known.

Final operational acceptance: 20/20 new Codex finals, 80 review entries, 15,449 validated
answers plus 20 mechanical checks, and zero missing checks. Native context/scope is complete
for 3/20 cases. Independent review cleared raw evidence, bindings and budget: 435 network
requests, USD 0.192088554 known usage plus three unknown-billing reserves totals
USD 0.200346090, below USD 2. Successor archive 20261025T082946Z verified 3,556 payloads,
with independently checked tar checksum and table counts. T016 human labels and the original
Gemini isolation gate remain open; no quality claim is established.

## Quality evaluation and human handoff

- [x] T024 [US2] Freeze detailed annotation/analysis/README rules in quality-protocol.md and align current source contracts.
- [x] T025 [US2] Add RED tests for blind balanced packaging, exact diff alignment, label validation, immutable model-run resume, missing/zero denominators and clustered analysis in tests/test_quality_review.py.
- [x] T026 [US2] Implement benchmarks/quality_review.py and benchmarks/reviewer.html with distinct source-only/quality phases, independent views, export/import and private coordinator key.
- [x] T027 [US2] Independently review code/security/provenance and run one-case/model smoke before remaining authorized quota calls.
- [x] T028 [US2] Execute source-only inventories and40case/model grades with raw records; report model-only findings, missingness and agreement separately from human labels.
- [ ] T029 [US2] Deliver convenient human HTML bundles and Google Forms generator/drafts with instructions; verify UI and round-trip export, never send invitations.
- [x] T030 [US3] Produce labeled exploratory charts/data, update README/status and archive the new evidence without overwriting prior bundles.

T024→T025→T026→T027→T028; T026 also gates T029; T028/T029 gate T030. T016 remains
open until two actual human reviews are returned and reconciled. No full suite or release.

Quality assessment execution: 42 starts including inherited smoke; 2 valid source inventories,
39 valid output groups, 1 invalid group retained, 156/160 valid output reviews. No retry or paid
API calls. Original failed group remains missing; comparison CIs use 19 complete document
clusters. 46 targeted quality/consumer tests passed; no full suite. Human HTML source lock,
first-group controls, synthetic fixture import and final export/server validation verified.
T029: HTML/ZIPs and Forms generator delivered; two source-only Google Forms created and
UI-verified on 2026-10-25 (20 sources/42 questions each, unpublished, 0 responses). Quality Forms
await reviewer-approved frozen source inventories; no publication or invitations. T016 remains open: 0 real human submissions.

T030 local delivery verified: five figures with SVG/PDF/PNG 300 DPI and CSV behind them; README
labels findings exploratory; archive 20261025T093528Z retains 513 new payloads plus nested
operational evidence. Packaging checks every payload during tar readback; separate read-only reviewer audit
verified all 513 payloads, canonical counts, reviewer ZIP separation, QA exclusion and nested hash. No commit,
push, publication or invitations.

## Simple human Forms replacement — owner approved

- [x] T031 [US2] Freeze simple-v2 question/data and rendering contracts in human-simple-protocol.md; retain old protocols/results.
- [x] T032 [US2] Add RED tests for four-arm blind binding, exact preserved original/output text, three-question structure, human response mapping and unknown/missing handling.
- [x] T033 [US2] Implement comparison image/rendered batch preparation and bounded Apps Script replacement with no-response gate, raw snapshot, idempotent batch records and final acceptance readback.
- [x] T034 [US2] Independently review final mutation/schema/rendering code before live rebuild; targeted tests and one-document UI smoke.
- [x] T035 [US2] Replace both zero-response Forms, verify every source/output/image/question mapping and responder permissions, then deliver same A/B responder links with new evidence archive.

T031→T032→T033→T034→T035. No implementation workers, model calls, paid APIs or full suite.
The latest owner-approved human simple-v2 amendment supersedes the source-first human workflow
only; previous raw model runs/results remain valid at their original scope and are not relabeled.

## Real-world Facebook source amendment — 25/10/2026

- [x] T036 [US2] Record the owner-requested real-world source contract, provenance uncertainty, collection failure and intake template. Evidence: realworld-protocol.md and artifacts/014-facebook-realworld-20261025; JSON parsed; no raw private chat saved in these artifacts.
- [x] T037 [US2] Freeze20eligible whole public AI responses with publisher-declared provenance, original prompts, pinned revision, Apache2.0 card, raw100rows and complete eligibility ledger. Owner abandoned Facebook; evidence: artifacts/014-public-ai-benchmark-20261025-v2. Generator model/provider raw unavailable; not independently attested.
- [x] T038 [US2] Freeze matched four-arm editing protocol/model/rounds/prompts and cumulative Jev cost guard; implement only necessary benchmark adapters with meaningful RED/GREEN targeted tests and independent review before inference.
- [x] T039 [US2] Run frozen real-source editing treatments; retain raw requests/responses, errors, usage, advice scope, unchanged-output counts and exact source bindings; no outcome-based rerolls or source selection.
- [x] T040 [US2] Create separate blinded real-world A/B Google Forms with adjacent original/edited views and three simple questions; preserve pilot Forms/responses; verify full provider/UI/item mapping and authorized response permissions before handing over links.
- [x] T041 [US2] Package/re-read all real-world evidence checksums and analysis contracts, report provenance cohorts and missingness separately; publish no human-quality chart before actual independent ratings.

Dependencies: T036→T037→T038→T039→T040→T041. Original synthetic/model/human-simple-v2 evidence remains unchanged. Public-source cohort execution is recorded separately; see live sealed manifest and recovery amendment.

Public-source gates: 40 scoped tests pass (public runner/recovery/Forms and traced capture/Codex adapters). Recovery and first4/4output smoke independently reviewed; remaining19cases authorized under unchanged caps. New Forms code reviewed for creation while paused; publication requires complete provider/UI readback. See public-ai-human-protocol.md for frozen human analysis denominators and missingness.

T039receipt:80/80Codexoutputs from20publicAIresponses,80canonicalprompts/raw/advicebindingsverified,0recordedtools.576newJevrequests,max32/case,USD0.456368556cumulativeinclallreserves.19partial/1fullscope;schema/availability/reconciliationpassboundariesretained.55scopedPython+4GSauditchecksPASS;packagevalidatorv0.11.0/55patternsPASS. Humanquality0labels;Formsprovider/publication/archivegatesremainopen.

## Owner amendment — Remove background questions

- [x] T042 [US2] Snapshot both live public Forms schemas/state and all submitted responses before removing reviewer-background fields; freeze local evidence.
- [x] T043 [US2] Remove exactly the two authorized profile items with snapshot/identity guards; preserve remaining160IDs, rating values, blind keys, publication/privacy and responder URLs.
- [x] T044 [US2] Verify both provider readbacks and actual responder pages, update human protocol and publish a separately checksummed evidence amendment without replacing the original archive.

Dependencies: T042→T043→T044. Human quality collection remains pending.

## Pre-survey analysis readiness

- [x] T045 [US2] Freeze public-human analysis/import/export contract, current cohort binding, response selection and raw conservation; add meaningful RED tests for schema contamination, Unicode logs, unknown/missing labels, duplicates and selection gates.
- [x] T046 [US2] Implement read-only Forms exporter and immutable participant-data import with exact item/form/assignment identities, original raw conservation and explicit coordinator A/B response selection.
- [x] T047 [US3] Implement paired source-cluster analysis, missingness, agreement and scientific chart rendering against the frozen public-human protocol; verify analytic toy oracles and zero-label safeguards.
- [x] T048 [US3] Independently review affected code/statistical claims, verify real zero-label readiness and an isolated clearly marked synthetic round-trip/chart QA without publishing fabricated quality results.
- [x] T049 [US3] Reconcile current-vs-historical task status, finalize README/runbook/report templates and checksummed readiness bundle; leave only human labels or explicit external-runtime gates pending.

Dependencies: T045→T046→T047→T048→T049. No raw generation or live survey schema changes.

T045–T048receipt:21targeted tests passed; peer reviewer cleared source/provenance and
statistics after fixes. A/B real empty exports passed full source/image/question audits
and strictUTF8 roundtrip. Positive responses verified using fixture only. Six QAfigures
inSVG/PDF/PNG300DPI; three figure families visually inspected; exact synthetic summary
reproduction acrossPython3.12/3.15. Zero-label quality chart CLI refuses before writing.
No new model/Jev calls, survey edits, participant notifications or full suite. See
readiness-review.md, human-analysis-runbook.md and CURRENT.md.

T049receipt:readiness bundle verified170filechecksums,2.09MB; source/raw archives
unchanged SHA256. Prepared source imported real empty A/B logs offline with exact
summary reproduction. Current workspace-v2 locked to reviewed code/protocol. See
artifacts/014-public-human-readiness-delivery-20261026.json.


## Owner-authorized isolated Gemini recovery — 2026-10-26

- [x] T050 Provision pinned official Linux CLI in an isolated, non-root container; retain installer/manifest/payload and checksum records.
- [ ] T051 Complete user-operated official authentication, inspect native settings/quota, verify host-data isolation and review execution boundary before inference.
- [ ] T052 Freeze the separately approved Gemini corpus/arms and run bounded trials with complete available native raw evidence; no host-token transfer, credit fallback or silent retries.
- [ ] T053 Reconcile trial counts, raw completeness and unchanged Codex/Forms hashes; deliver a separate archive and report with attestation limits.

T050 → T051 → T052 → T053. Preserve all historical tasks/artifacts and live Forms.


## Owner-operated script handoff —2026-10-26

- [x] T054 Prepare a terminal-operated public-only80-cell host runner, immutable inputs, durable raw streams, no-grant/native permissions and no automatic retries.
- [x] T055 Independently review and run offline fake-process/raw/schema/resume/interruption tests before delivering one command; no live Antigravity invocation.
- [x] T056 Owner completed epoch-v3;80/80 raw outputs/model/tool/unique conversations/seals reconciled in completion-audit-20261026.json. Quality still pending.

This handoff does not clear host tool-review denial or mark Docker authenticationT051 done.


## Explicit no-tool agent amendment

- [x] T057 Prepare separate80-cell custom-agent runner/stream guard, raw outside workspace, immutable old2calls, fingerprints and meaningful offline tests/review.
- [x] T058 Verify live capability by matched public-fixture controls: registry60iscommon; finish-onlyagent cannot read, read_file-enabled clone reads nonce; preserve3diagnostics and2zero-tokenpreflights. Guard uses boundproof and rejects actualoperationalcalls. Live R002-bare passes1/80.
- [x] T059 Deliver verified one-command handoff in gemini-text-only-runbook.md;15Python+5Nodepass, independent review and real1cell smoke. Owner runs remaining79; old hostcommand remains retired.

T057:14Python+4Nodepass; native gate remains unmet. No Forms change.


## Within-agent before/after correction — owner approved2026-10-26

- [x] T060 [US3] Add analytical oracle tests in tests/test_public_human.py for original-relative rates, source pairing, missing/uncertain exclusions and secondary-only mode contrasts.
- [x] T061 [US3] Extend benchmarks/public_human.py and benchmarks/public_human_charts.py with original-relative estimates/CSV/figures; preserve existing export identity and selection guards.
- [x] T062 [US3] Correct README.md, public-ai-human-protocol.md, human-analysis-runbook.md, human-results-template.md and CURRENT.md; freeze new offline workspace and verify existing cohort/Forms/raw hashes unchanged.

Dependencies:T060→T061→T062. Serial implementation; no parallel work needed.
Independent acceptance: deterministic toy oracle plus synthetic-only chart smoke;
no model, Jev, survey mutation or label collection. Historical results remain archived.

T060–T062 receipt:23targeted tests pass; two analytic RED cases preceded code.
Read-only peer review found and resolved two chart-interpretation issues. Synthetic-only
QA produced8SVG+8PDF+8PNG300DPI, with original-relative axes, fixture watermark and
observed-CI-degeneracy warning. No-label chart gate verified; workspace-v5 load check
passes, exact form/item/image/assignment/cohort parity against v2.5719protected files
unchanged by SHA256. No full suite, model/Jev calls, human label inspection or Forms
API/mutation. V3/v4 pre-review retained, v5 is current. See amendment artifact receipt.

## Descriptive execution report — no human grading at this stage

- [x] T063 [US3] Add analytic oracles in tests/test_execution_report.py; implement read-only raw validation, per-cell tables, medians/IQR and provenance in benchmarks/execution_report.py.
- [x] T064 [US3] Render scientific per-source charts as SVG/PDF/PNG300DPI with explicit units, sample size and non-quality captions; review numerical claims and visuals.
- [x] T065 [US3] Write execution-report.md and update README.md/CURRENT.md to reflect deferred human grading; freeze report/data/source checksums without changing existing raw or Forms.

T063→T064→T065; no benchmark inference, Jev calls, participant data or live survey edits.

T063–T065 receipt:6analytic oracle tests pass;160raw outputs validated across1377input
files. Exact independent offline recollection reproduces cells.csv,summary.csv/JSON
and input manifest. Seven scientific figures inSVG/PDF/PNG300DPI visually inspected;
Unicode font/renderer provenance retained. Independent scoped code/statistical review
cleared after canonical-source/session guards.5719historical files unchanged. No
provider/Jev calls, participant data or Forms access. No full suite. Human grading
is deferred, not completed; no quality superiority claim.
