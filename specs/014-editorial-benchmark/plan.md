# Implementation Plan: Editorial Pilot

**Current scope — owner correction2026-10-26:** within-agent original/edited comparison;
no cross-agent ranking or pooled runtime labels. Codex80/80 and Gemini80/80 already
exist; use them without new inference or changes to the two live Codex Forms.
See [within-agent-amendment.md](within-agent-amendment.md); earlier run/recovery
sections below remain historical evidence, not instructions to restart generation.

**Current amendment**: The owner added Vietnamizer + Jev as arm four, Codex first.
See [jev-extension.md](jev-extension.md) for the owner-approved USD 2 Jev ceiling, matched
revision control, separate epoch and pending gates. The three-arm authorization below
is historical; it does not cover new paid Jev calls. The separate fourth-arm runner passed independent review; 40 new Codex outputs are generated. Jev coverage/quality acceptance remains unmet; see codex-jev-results.md.

**Date**: 2026-10-25 | **Spec**: [spec.md](spec.md)
**Authorization**: Owner approved the 120-output development pilot, Codex gpt-6.1-sol medium
and Antigravity gemini-3.8-flash-medium, existing subscription quota only, USD 0 incremental.
The independent holdout and human-scored quality claims remain outside this execution slice.

## Summary

Create twenty original synthetic development cases, freeze prompt bundles and configuration,
run each case/arm/runtime in a fresh conversation, preserve all attempts and collect an offline
operational report plus blinded review packets. No skill/runtime edits or external dependencies.

## Technical Context

Python 3 standard library; existing Codex CLI 0.164.0, Antigravity CLI 1.4.7 and installed
Agybird 0.3.0. JSON/JSONL local storage under ignored artifacts/. Source scripts in benchmarks/,
targeted unittest in tests/test_editorial_pilot.py. macOS local execution. 120 valid output slots;
maximum 132 pilot attempts including failures, no automatic retries or paid-credit fallback.
CLI subprocesses have bounded timeouts; progress is emitted per attempt. No code generation
or filesystem action is requested from the trial models.

## Research and depth gate

See research.md. Tasks/implement route is required: multiple runtime and data/report contracts,
quota permissions and independent trial ordering make a direct seam inappropriate.
No new implementation agents; one read-only research agent was dispatched by speckit-plan.
Independent code review is required before live orchestration.

## Constitution Check

Before and after design: no common language rules or numerical edit policy changed. Original
synthetic cases are development-only and labels remain host drafts. Model/skill/corpus/config
versions bind every attempt; policy_version=null. Failures and missing output cannot be PASS.
Core uses no Jev; absent script capability in the text-only task is explicit. Reports label
harmful-edit recall and valid-edit false-block rate N/A (no edit guard), and human review pending.
No publication, package release, unrelated refactor or shared configuration change.

For the amendment, retain tasks/implement: orchestration, spend accounting and blinded
report contracts change together. Preserve the existing runner and frozen artifacts until
the extension has targeted tests and independent review. Owner approved the USD 2 ceiling on 2026-10-25. No paid call before targeted verification and independent review.

## Project Structure

benchmarks/editorial_pilot.py: frozen prompts, adapters, durable attempts, report/review export.
benchmarks/jev_pilot.py: separate extension epoch, durable Jev reservations/receipts, matched revisions.
tests/test_jev_pilot.py: spend caps, no-retry recovery, raw response reconciliation and lossless advice semantics.
benchmarks/pilot-cases.json: twenty original synthetic development documents plus draft invariants.
tests/test_editorial_pilot.py: output/failure parsing, duplicate protection, prompt isolation,
artifact binding, subprocess timeout and completeness tests.
artifacts/014-editorial-pilot/: prompts, raw CLI outputs, results, report and review packets.

## Validation

RED/GREEN targeted unittest; review final patch before running inference. Smoke one source's
six cells, inspect contamination/tool evidence, then bounded batches. Inspect quota between
batches; stop at quota exhaustion or if USD 0 cannot be maintained. CLI output alone establishes
generation, never semantic correctness. No full suite requested or run.


## v2 recovery amendment

Before any new Codex output: retain v1 source snapshot and 23requests; create a separate v2
manifest binding byte-identical inherited evidence. Fix core-versus-experiment digest encoding
comparison without changing native core. Generate matched revisions with explicit exposure
(full/partial/unavailable/not-attempted); fallback is not a Jev treatment or service pass.
A third failed case stops further Jev dispatch globally. Keep inherited reservations, max 640
requests/max 40 Codex starts, USD 2 cap and no retries across epochs. See jev-extension.md.
Targeted fake end-to-end test covers inherited partial/unavailable, report and resume.


## Data retention follow-up

Owner requested complete retention for later scientific analysis/charts. Direct, offline archival
path: one bounded data-preservation seam with known raw artifacts; no trial runner, production
contract, external processor, dependency or permission change. Preserve raw epochs/source snapshot,
export lossless keyed tables, document units/missingness/provenance and re-read checksummed archive.
See data-archive.md; local storage only, off-device backup remains unconfigured.


## Owner-authorized recovery to complete 20 Jev-treated cases

Owner explicitly requested diagnose/fix failures, retain full raw bodies and continue to 20
cases under the SAME USD 2 cumulative ceiling. Resume tasks/implement route: raw capture crosses
privacy, budget, timeout and replay boundaries. Preserve production jev/ behavior and frozen
v1/v2 drivers; implement benchmark-only capture and a separate recovery runner. Persist raw
request body before dispatch, response bytes before JSON/schema validation, HTTP status and
bounded error phase without auth headers/credentials. Missing/truncated response is explicit.
First run one recorded diagnostic; classify observed root cause before adapting dispatch.
Reuse only exact-input/model validated request evidence; never reroll a validated judgment.
Cumulative max 640 network requests and 32 per document, including original 33, max 3 recovery
evaluation passes/case. Retry only identified transient transport/HTTP failures, bounded and
recorded; nonretryable schema failures stop for an offline correction/review. Earlier no-retry
protocol remains historical; this amendment implements the owner's new recovery instruction.
New Codex+Jev finals require all required remote answers, source accounting and complete
segmentation. Native context/scope/evaluation abstentions remain separate and are never rerolled.
Keep old controls and baseline sources with explicit epoch/timing provenance. New generation starts capped 20, separate from 40 old starts.
Independent review before paid diagnostic and again before a changed live recovery policy.

Observed schema inconsistency recovery follows recovery-protocol.md: preserve every individually
valid answer, request only invalid score/choice checks with identical state/question/model, and
retain a sealed composite with per-check raw provenance. Independent review approved adapter
SHA-256 19af9752f7fb12414b460986a618de8877461fcc2b0bf18c4b70d2a6289e3fcb before any repair.

## Authorized quality-evaluation amendment

Owner authorized model grading plus convenient human handoff on 2026-10-25. Resume014
plan/tasks/implement; preserve all earlier epochs and archives. See quality-protocol.md.
Tasks required: new label/provenance contracts, independent model runs, human data export and
UI/Forms lifecycle cross more than one seam. No production skill changes or paid APIs.
Use two Codex models (Sol/Astra), two source-only calls plus 40 fresh four-output calls,
max 42 starts,180seconds/call,two concurrent processes. Freeze corpus/output identities,
blind position mappings, schema/rubric and source code before smoke. No automatic retries.
Human packets run locally without network, with source-label freeze before output access,
per-reviewer remapping, progress/export/import and no answer key/model judgments. Forms
creation only through supported authenticated UI; otherwise deliver a ready-to-run generator
and explicitly label cloud creation unverified. Do not send invitations or collect email.

## Owner-approved simple human form amendment (2026-10-25)

Fio explicitly requested replacing the two A/B Forms with direct original/edited comparisons,
three understandable questions and blinded four-arm identities, with no source-only phase.
Reuse current published form IDs/responder URLs; both UI response counts are zero before work.
Tasks/implement route remains required: label contract, cloud mutation, rendering and response
analysis change together. No new inference, Jev spend, providers, permissions or dependencies.

Use four two-column comparison images per document (original left, edited right), two simple
four-row radio grids and one evidence paragraph. Twenty document pages preserve current A/B
packet randomization and all80outputs. This fits Google's300item limit;80separate image/three-
question pairs would exceed it. Image text is neutral, same typography/size in both columns.
Avoid arm names or model grades in forms/images. Google native Forms remains single-column;
comparison images provide the requested adjacent display and can be enlarged.

Pause each form during rebuild; before deleting old items require zero live responses and
save the old item IDs/titles/helptext and provider receipt. User's instruction to replace and
remove the old source-only step explicitly authorizes that scoped replacement. If any live
responses appear, stop destructive rebuild and preserve them. Batches seal exact packet/image/
question identities, never automatically repeat partially applied items. After final readback
of20pages/80outputs/60questions, restore anyone-with-link acceptance already authorized by Fio.
No invitation or test submission into the live study. Save raw logs/item mappings and snapshots.

New human schema human-simple-v2 is separate from model-v1 and full human-v1. Question1 combines
meaning/facts/voice preservation; question2 is comparative readability; question3 is evidence
notes keyed A–D. Do not infer edit precision, required-fix recall, separate meaning/voice flags,
rank preference, wins/ties/losses or a human superiority claim from these simpler labels.
Keep unknown/missing and original submissions; model results and historical protocols unchanged.

Simple human amendment acceptance: completed25/10/2026. T031–T035 delivered. Both old62-item
forms had zero responses; paused/snapshotted, replaced in place, each20groups80images3Qs/group
(162items). Same responderURLs, anyone-with-link, published+accepting verified in provider
status and UI. All160PNG/text bindings and40provider group maps checked;11targetedPython
tests+4JSaudit checks PASS, packagevalidator PASS, nofullsuite/model/Jevcalls. Independent
review resolved canonicalbinding/order/readback blockers before reopening. Google long-log
truncation retained explicitly; complete maps/snapshots exported separately. No human labels.
Local epoch: artifacts/014-human-simple-v2-reviewed-20261025; archive/checksum sibling.

## Real-world source amendment — design prepared, collection pending

Canonical coding workflow read via approved Obsidian CLI on25/10/2026; sandbox connection
failure retried once with the identical authorized command under supported escalation and
succeeded. Resume feature014 Spec Kit: specify/plan amendment, then tasks/implement. Depth gate
requires tasks because new source/provenance/privacy, budget, execution and cloud-data contracts
cross boundaries; no implementation children. No extension hooks (.specify/extensions.yml absent).

Input cohort: real posts from owner-selected group, target20complete eligible sources; retain
candidate/query/feed order and exclusions. Freeze source bytes/permalink/context/provenance
before any model outcome exists. Protocol realworld-protocol.md separates author-disclosed
AI assistance, verifiable model output and unknown authorship. No calibrated detector exists in
this experiment; Jev may judge explicit evidence/editing needs but not certify AI authorship.

Keep the existing four editing conditions and per-rater blind layout. Design matched editing
round counts/model/source exposure before adapting a runner; do not carry forward unequal-pass
historical baselines. New Jev calls require the existing authenticated interface, a reviewed
spend guard accounting for cumulative used/reserved spend under owner authority, and full raw
retention. Do not reset the previous USD2 ledger or assume a new budget. No new API calls yet.

New epoch artifacts/014-facebook-realworld-20261025 contains candidate observations and an
empty intake template only. Browser origin auto-review twice denied expanding a group post,
the second after owner explicitly reauthorized group-only reading. Stop browser operations;
no alternate surface/network workaround. Continue from owner-provided post text+permalinks.
Existing pilot Forms remain unchanged; make separate real-world A/B Forms after complete
frozen data, matched output runs, targeted tests/review, provider readback and human UI smoke.

Open obligations: collect eligible sources; provenance/data gates; matched-prompt/round/cost
freeze; implementation/RED-GREEN checks; independent review before live orchestration;
raw execution and failure reconciliation; new Forms with immutable source-output-item mapping;
separate human labels, uncertainty and scientific archive. No completed benchmark claim.

## Public dataset execution amendment (2026-10-25)

Continue feature014 tasks/implement (cross-source, execution, spend and cloud contracts).
Prerequisites checked and canonical workflow read through approved Obsidian CLI with supported
one-time escalation. No extension hooks. Source candidate cards/metadata downloaded read-only
from public HuggingFace, pinned revisions and retained under artifacts/014-public-ai-sources-20261025.
Select TTP01/Vietverse-SFT-Preview revision6b4e4a86e3b399318ac4fe91b2bbe64501037f40:
Apache2.0 declaration, raw100-row JSONL + original prompts + source_type=synthetic_llm and
pipeline traces. These are publisher-declared AI outputs, not provider-attested raw calls;
actual generator model/system prompt unavailable. Upstream Gold labels are not our groundtruth.
Other candidates retained: BKAI native vi-alpaca has generation description but missing explicit
license; NVIDIA personas CC-BY4.0 have strong AI provenance but differ from prose responses.

Freeze the first20eligible whole assistant responses in canonical row order before editing:
120–550 whitespace-delimited Vietnamese units; single-turn/no-code; domains education,
technology, general_chat, knowledge_vn. Exclude27(running/health),49(immigration/legal),
69(time-dependent holiday),85(food-safety),93(land-contract legal),96(asset-license legal)
based on original prompt scope; record all100 eligibility decisions and retain the complete
raw rows. No quality/AI-detector/editing-outcome filter. Original response text unchanged.
One publisher, curated SFT responses, limited genre/model coverage; not a natural-web sample.

All four arms get one final-generation call directly from the same original response/query:
bare editing, ordinary copyedit, Vietnamizer core, Vietnamizer+Jev. Jev evaluates original
source before final generation (no extra LLM revision for that arm). Preserve complete source
context, raw request/replies and service/context abstentions. New guarded budget carries
forward all previous used/reserved cost toward the same USD2 ceiling; serial Jev execution,
max32new requests/case and640new requests overall; log old request count separately.
No valid-answer rerolls; invalid service/schema answer stops paid dispatch for review.
Codex requestedgpt-6.1-sol/medium, existing ChatGPTsubscriptiononly, no tools/files/network in
model trials, no APIkey/creditfallback. Max80starts for20x4, no automatic retries.

Implementation: new benchmarks/public_ai.py and targeted tests/test_public_ai.py, reusing
unchanged editorial_pilot adapters and Jev capture/preparation/advice helpers. New Forms
preparer/runtime separate from frozen simple_forms.py/.gs, with new provider IDs, exact
sequence/image/question audits and split logs under8KB. Independent review before inference
and cloud mutation. Smoke one source/4arms, then bounded batches; inspect unmodified-output
rate before handoff without selecting different cases or forcing edits. Retain unknowns and
report all output changes as descriptive until real independent human ratings arrive.


### Reviewed single-question recovery amendment (public v2)

First-source Jev request0016 returned33valid answers and one invalid Score distribution
(score0.52 versus weighted mean0.55). Original STOP_PAID and all raw records remain.
A separate public_recovery.py adapter and sealed recovery-manifest bind to the frozen
public runner; only invalid score/choice distribution questions may be queried once,
with identical full state/model/question. Valid answers remain exact; derived composites
seal per-question provenance and all six source raw files. Replaying accepted prefix
incurs no new call. No limits are increased: repairs count within32network/case,640new
network total and cumulative USD2 including old pilot spend/reserves. Budget exhaustion
produces explicitly partial advice; all other failures stop. No valid answer resampling.
Independent read-only review cleared first-source four-arm smoke after13targeted tests
and recovery-manifest preparation/readback. Broader run and Forms remain separate gates.


### Reviewed empty opening-deadline amendment

After24completed Codex outputs, R007 request0202 reached15s with HTTPnone and zero
response bytes. This does not establish nonprocessing or zero billing; full unknown
reservation remains in the cumulative ledger. public_deadline.py is a separate adapter
and deadline-manifest binds all observed0202files, originalSTOP_RECOVERY/R007started,
previous recovery manifest and adapter sources. Original stop markers remain unchanged.
Under owner-authorized benchmark completion and independently reviewed bounded repair,
permit exactly one fresh network attempt per exact payload only for this narrow empty
opening deadline. Ticket persisted before dispatch; successful raw/ticket/receipt proof
reconciled before generation. Any second failure or other transport/HTTP failure stops.
All original source/model/arm/start and32/640/USD2caps remain, counting both attempts.
This explicitly amends the original stop-for-review policy prospectively; it does not
resample valid semantic answers. Failed core results now persist before abort. First
R007four-arm smoke required; no blanket remaining-case clearance yet.45scoped Python
tests and4provider-free Apps Script audit checks pass. Historical proof tests use an
explicit offline reviewed-disposition fixture; operational markers are never removed.

R007smoke subsequently passed4/4with zero recorded tools; reviewer verified canonical
prompts, raw bindings,0202→0203retryproof, sealed partialadvice and unchangedSTOPmarkers.
Remaining13cases cleared under unchangedcaps. Cumulative reservationUSD0.296640456
at28/80outputs. No human-quality or full-coverage conclusion.

### Architecture checkpoint: terminal schema abstention

Observed R0130404invalid Score followed by0405invalid single-question repair. No third
request is allowed. Stop before another correction: raw network artifacts own service
truth; only validated responses/composites own accepted semantic evidence; core owns
coverage/missingness; host advice owns the declared partial workflow; generation cannot
turn a service error into a negative finding or completed check. The mismatch is in the
host completion gate, which rejects explicit abstention despite a valid evidence prefix.

Independent architecture review accepts a separately frozen terminal-abstention adapter:
reconcile every accepted receipt/judgment, bind exact original/repair raw+ticket, preserve
failed receipt and missing checks as unavailable, no more Jev calls for that source. This
prospectively covers only exhausted one-attempt score/choice-distribution repairs in the
remaining cases. Second transport failures remain outside and stop. Advice receives an
explicit service-partial disposition; reporting separates per-case availability/coverage.
The measured treatment is a bounded service-assisted workflow, not fully available Jev.
No source/model/arm/cap change, no valid-answer reroll, no original artifact replacement.
This is owner-authorized completion within the partial/fallback benchmark, with a reviewed
protocol amendment before implementation; implementation review remains required.

### Availability abstention at the overall evaluation deadline

R0190546and0547 are the same payload, both HTTPnone/empty body, ending around1.1s.
The unchanged core caps each transport timeout by the remaining120s evaluation budget;
this is deadline exhaustion, not proof of a service outage. The permitted retry ticket
is already consumed; no third call or further R019Jev dispatch is allowed. Both unknown
cost reservations remain. Architecture review accepts a separately bound availability
certificate, distinct from schema abstention: exact two failed raw attempts + one ticket,
no later case calls, valid prefix only, failed batch unavailable. Same narrow prospective
disposition may cover R020. Unsupported failures still stop. No transport, retry, time,
model, source, arm or cash-cap change; original modules and stop markers remain immutable.

### R020 late-valid response: reconciliation proposal

R019completed with no further Jev calls. Final R020 has548validated,549empty15sdeadline,
550validated retry≈9s. The frozen core rejects the callback because total24s exceeds15s;
valid raw550 remains, original failed core receipt remains. No R020Codex output exists.
Proposed one final case-only reconciliation: freeze all current source/manifests/stops
and the R020failed pass/raw/ticket; replay548/550 without network, then evaluate only
unasked tail within remaining29network slots (same32case/640new/USD2), one evaluation
pass only and no new transport retries. Do not alter the original callback outcome.
Retain late raw traces separately; admit advice only when normalized answer/usage matches
an accepted core receipt. A later failed batch stays unknown; no new semantic rerolls.
Architecture/implementation clearance pending before execution.

R020architecture and implementation reviews subsequently cleared the single final pass
and four Codex outputs after final-case-manifest preparation/readback. No transport
retry is enabled in that pass; previously validated raw548/550is replay-only.

### Publication-dependent image availability

New unpublished Forms returned Fife400/naturalWidth0 for original1600px, Google-normalized
819x2048 and rerendered640px controls. The old published pilot decoded in the same browser.
Publishing the isolated diagnostic with no image change made all three decode at620px
wide. Diagnostic closed again with0responses. No production image/render amendment needed.
Reviewer clears updated order: completeB, full mapping/providerhash/sequence and0response
checks, publish mainForms whilepaused, then verifyresponderimages/longest/readability and
anyone-linkpermissions beforeenablingresponses/handoff. Existing frozenimagebodies unchanged.
A separate publication helper will retain originalcohortkey and preflight audits; user
already authorized anyone-linkpublication. No invitations or testsubmissions.

### Canceled Forms batch recovery

Google execution history records cancellation after20.877s for Bstart2, leaving23items:
2completegroups plusQ003page/fourimages, noquestions. Read-only snapshot binds all23IDs,
metadata, imageproviderhashes, originalSTARTEDticket, paused/unpublished and0responses.
Threeimages match sameinput verifiedAtwins; fourth has missinghelp and differentprovider
bytes. Reviewed separate recovery restores onlyDcanonicalPNG on its existingID, sets
help, adds3missingquestions, preserves23IDs andoriginalticket, and writes its own one-shot
recoverycertificate. Q004thenuses anewstart3catchupbatch. No deletion, regeneration of
modeloutputs, change to cohortcontracts, imageinputs or evaluationordering. Sixprecondition
checks failclosed withoutmutation; actual providerreadback remainsrequired after execution.

Q003recovery completed and provider audit passed at26items,0responses. Reapplying its
canonicalDblob on the sameID returned the same priorDproviderhash; a providerhash
mismatch with anotherform alone is therefore not proof of incorrectimagecontent.
The recovery addresses the interruptedmetadata/questions; do not report imagecorruption.

### Verified Forms delivery and evidence archive

Both A/B passed canonical mapping/input-image checks (40groups,160images,162items each),
full provider sequence/metadata audits, published-paused image decoding, longest-image
readability, and anyone-link published-options UI. Final readback2026-10-25T16:58Z:
published/accepting true,0responses,collect-email/summary/shuffle/limit-one false. Actual
responder URLs opened in signed-in owner browser; anonymous session not tested. No
test submission. B had one transient Google server error during prepublication audit;
retained log, read-only state confirmed no mutation, unchanged helper succeeded once
after waiting. Data-generation epoch and original stopped/canceled receipts preserved.

All55scoped Python tests,4provider-free GS audit checks,5publication guards and6partial
recovery precondition checks passed; package validator v0.11.0/55patterns passed after
README update; README/AGENTS diff whitespace check passed. No full suite. Five analysis
outputs regenerated offline and byte-identical. First archive read back4471filechecksums;
final archive is resealed after completion ledger update and verified again for delivery.
Human quality remains pending actual independent ratings; no quality chart published.

### Remove reviewer background fields — 2026-10-26

Source: canonical coding-workflow.md via approved Obsidian CLI; sandbox connection
error recovered by identical escalated read. Owner-approved version adaptive-2026-10;
review-by2026-10-21 is expired. Route: resume Spec Kit014 with a bounded schema amendment;
tasks/implement path because live data/schema changes. Requirements checklist12/12.
First snapshot both schemas, IDs/state and submitted responses locally. A one-shot
script compares exact snapshots before removing only the first two known paragraph
items, in reverse order. Preserve all160 remaining itemIDs/content and response values
for those IDs, publication/acceptance/privacy flags and URLs. Old frozen runtime and
archive remain historical; record a separate no-background-fields amendment and new
response/mapping contract. Verify API and both actual responder pages after mutation.
No semantic selection, evaluator calls, new model generation or changed ratings.

No-background amendment verified: both0responses before mutation, exactly2authorized
paragraph items removed per form, all160remaining IDs/order and response data retained.
Both actual responder pages omit background fields and enter Q001 without any input;
three rating questions and4images decode. Visibility/privacy/URLs unchanged. Six
removal-path scenarios and chunk transport roundtrip passed. Amendment archive22file
checksums read back; parent239MBarchive unchanged. T042-T044complete; human ratings
remain pending. No new model/Jev calls or full-suite run.

### Human analysis readiness —2026-10-26

Canonical workflow read through Obsidian CLI in this session; unchanged guidance reused.
Resume Spec Kit014 through tasks/implement because the importer is an analysis/data
contract with multiple consumers. Requirements checklist12/12; no extension hooks.
New modules public_human.py/.gs and public_human_charts.py own only the public-human
cohort. Freeze original Forms and generation artifacts; prepare a new portable binding
from public_forms.verify plus no-background amendment and provider mappings. Keep
export read-only and never send notifications. Exact schema/IDs and SHA256/UTF8 guard
chunk import. Multiple responses require explicit A/B IDs; defer quality decoding until
both are selected. Tests use clearly labeled synthetic provider fixtures in temporary
folders. Analysis uses20source clusters, fixed2raters,10000percentile-bootstrap draws
seed25033, exact missingness denominators; fewer than2complete clusters gives no CI.
Charts via existing bundled ReportLab and Sharp, no dependency installation. Actual
readiness report has0human labels and refuses quality plots. Request independent code/
statistical-integrity review after targeted tests. Antigravity host CLI gate persists;
no denied-runtime workaround or new authentication setup.

Human readiness delivered2026-10-26: T045-T049complete with21targetedtests, peer code/
statistical/provenance review, A/Bempty real-provider export/audit/strictUTF8 import,
fixture-positive roundtrip and6SVG/PDF/PNG300DPIfigure QA. Portable source copy gives
identical real empty summary; synthetic core summary exact acrossPython3.12/3.15.
Zero-label chart CLI refuses before writing. New bundle170checksums readback verified;
prior archives unchanged. No additional benchmark inference/Jev calls or survey edits;
code reviewer used2Codexagent turns, not counted as text-quality grading. Only selected
real human labels remain for current cohort; old Gemini isolation remains a separate
external gate.


## Isolated Gemini recovery authorized 2026-10-26

Owner explicitly authorizes provisioning the isolated runtime and resuming Gemini 3.8 Flash,
with complete available raw evidence and no modification of the Codex/human-review cohort.
Resume tasks/implement: this crosses runtime, authentication and data boundaries. Existing
subscription only; no host credential reads/transfers, paid API or credit fallback.
Prepare pinned Linux ARM64 CLI 1.4.7 in a digest-pinned Node container, no host HOME/repo/Vault
mount, non-root, dropped capabilities and no-new-privileges. Separate container-owned auth
state requires the official user-operated login. Preserve provider streams, stdin, stderr,
exit/timeout/usage and exact binaries/prompts/config hashes; provider-internal HTTP bodies
are not exposed by the official CLI and must not be fabricated. Native permissions stay on.
Authenticate before inference; verify isolation/config and independent review before trials.
Public-source four-arm epoch versus historical three-arm pilot is awaiting owner selection.
The old 132-attempt cap applies to the historical pilot, not an implicitly expanded cohort.
No Jev calls are authorized by this provisioning task; reuse exact frozen advice only if
the public-source epoch is selected and provenance binding verifies.
Source: approved Obsidian coding-workflow read on 2026-10-26; review-by 2026-10-21 expired.
No task/implement hooks configured. Requirements checklist: 12 checked, zero open.

Owner selected the public-source epoch: 20 identical frozen public sources × four arms =
80 Gemini finals. No replacement of 80 Codex finals or either human Form. Reuse existing
exact-source Jev advice; no new Jev spend. The historical 60-output Gemini pilot stays
partial and excluded. Maximum 80 generation starts for this epoch, no automatic retries;
preflight must use native non-inference commands only. Stop on native permission, quota,
paid-credit uncertainty or unexpected model/tool/subagent activity; failed attempts remain raw.


## Owner-operated host script —2026-10-26

Owner explicitly requests a script they themselves run in terminal. Scope is offline
preparation/delivery only; Codex does not launch agy or clear the existing tool-review denial.
Resume tasks/implement for raw/process/ledger contracts. Preserve frozen drivers and all
Codex/Forms data. New gemini_manual.py copies the exact85public input files/80prompts,
uses durable artifact storage and an empty per-cell cwd outside the repo, reserves starts
before spawn, cap80, no retries, stops on tool/subagent/error/permission/quota, checks
subscription credit selectors without changing settings. Strict raw native capture and
wrapper envelope retained; internal providerHTTP not exposed. Source-global context is
not isolated/attested. No model/Jev calls or auth/token reads in prepare/tests.
Targeted7Python+6Node tests pass (Nodeps test needs supported escalation); independent
review resolved process-group interruption and strict output-schema findings. No full suite.


Manual script cwd defect: reproduced FileNotFoundError from foreign terminal cwd.
One-line correction roots protected paths at ROOT; relative and absolute path fixtures
pass and mutation still fails. Eight targeted Python tests pass; actual status from
/private/tmp is0/80. Original prepared driver reconstructed byte-for-byte to verify
the sole source change. Before any starts, update only driver fingerprint, archive
original manifest and preserve a hash-bound amendment receipt. Inputs85/Codex4323
unchanged; no inference or Forms calls. No full-suite or Node rerun (unchanged helpers).


Native event-key parser recovery: first owner-run R002-bare completed successfully,
but type-only parser produced6unknown_event errors. RED regression reproduced exact
envelope; event/type normalization added with conflicting-key rejection. Ten tests
pass incl bound reconciliation, immutable failure/STOP and future-stop preservation.
Independent reviewer verified actual sealed raw/finish/wrapper parity and no external
tools. Append-only reconciliation sidecar accepts the existing output, preserves all
attempt bytes/STOP, archives prior manifest and amends driver hash. Status verified
from repo and foreign cwd:1/80, one start; nextR011-ordinary. No model retry, no new
Jev call, no Forms changes. Protected4,323files unchanged.


Architecture checkpoint after R011-ordinary: parser now correctly rejects actual tools.
Native used2run_command(ls) and2read_file calls against its own cwd/raw before SUCCESS.
This is neither quota failure nor another parser defect. Raw in cwd and prompt-only
no-tool policy are the observed design weakness. Keep cell invalid, original seal/STOP,
1accepted/2starts; no retry or relaxing acceptance. Prepare a reviewable text-only-agent
proposal with native capability verification and raw outside workspace. Selecting a
custom agent is an explicit Agybird override requiring owner direction; revised80cell
epoch would preserve2historicalstarts separately (82total). No implementation/runtime
change or inference before this decision. Evidence: architecture-checkpoint-R011/.


## Owner-approved custom-agent epoch —2026-10-26

Owner explicitly approves no-operational-tool agent, fresh80outputs and preserving
2historicalmodelstarts. Follow SpecKit014tasks/implement; no hooks. New text_only.py
keeps old driver/evidence immutable, fingerprints agent/code/publicinputs/history,
reserves before subprocess, retains native byte streams outside workspace and checks
actual init agent/model/request-review/tools⊆{finish} before accepting any response.
No global/default settings change: create-exclusive new agent file only, owner-approved
name. Documentation-based tools[]workspace definition did not prove capability masking.
Native catalog recognized explicitfinish-only global definition, but second guarded
probe still advertised60tools. Both native terminal results show0turns/0tokens.
Keep raw/failedprobes distinct from80qualityoutputs and2historicalmodelcalls.
Architecture checkpoint: no third local fix; unresolved authority between native
custom-agent discovery, primary-agent dispatch and advertised tool registry. No guard
relaxation or further inference until invariant has authoritative proof. Code14Python
+4Nodepass and independent review; live CLI gate FAIL, not codePASS or runtimePASS.


## Capability root cause resolved with paired controls

Owner authorized actual bounded tool-capability investigation. Three public-fixture
diagnostics retained: finish-onlyUNAVAILABLE; doc/registryview_filecontrolUNAVAILABLE;
runtimeIDread_filecontrol read exact nonce absentprompt (one finalLFignored), DONE.
Same prompt/body/model/fixture; registry60identical. Thus init.tools is sharedregistry,
not per-agent callable whitelist; view_file registry name differs from read_file
runtimecallID. Earlier guard conflated metadata with capability and rejected valid
agent before generation. No claim of exhaustive60tool proof.

Keep old drivers/probes/raw immutable. New epoch-v3 pins paired evidence, agentfile,
CLIbinary/version, wrapper, code and publicinputs; permits only verifiedregistry but
still rejects operationalactivity/subagents/schema/errors.15Python+5Nodepass; peer
review validated pairedproof/limits; live R002-bare nowcompleted1/80,finishonly,guardOK.
Owner command resumes79remaining.2oldmodelstarts+3diagnosticmodelcalls separate from
80new;2rejectedpreflights0turn/0tokens. No newJev or Forms changes. No fullsuite.


## Within-agent before/after amendment — 2026-10-26

Owner correction: the outcome is whether editing the same original with Vietnamizer
improves it within one fixed agent/model configuration. No Codex-vs-Gemini ranking,
pooled runtime estimates, new inference, Jev calls or live Forms mutations. Existing
80-cell cohorts remain separate; Gemini generation is complete and audited80/80.
The current A/B human forms cover Codex only.

Source: approved Obsidian coding-workflow.md read through supported escalation;
review-by2026-10-21 is expired. Route: Spec Kit014 amendment, tasks then implement
because the analysis/report contract changes. Known consumers: public_human.py,
public_human_charts.py, runbook/template and README.

Primary report: original-relative readability categories and preservation, separately
for each arm and fixed reviewer; add original-relative rate CIs clustered by source
for A/B and their fixed-rater average. Unknown/missing remain explicit and excluded
only from determinate estimates. Do not assign a numerical score to the original or
subtract invented pre-scores. Mode contrasts remain secondary, with no confirmatory
tests. Original-relative improvement alone does not isolate the skill contribution;
ordinary/bare controls supply that additional within-agent comparison.

Freeze a new offline workspace with current code/protocol and identical Forms mapping;
retain old readiness workspaces/exporters/raw intact. No label inspection in this
amendment. Preserve5719data files by hash. Targeted analytic oracle tests and chart
smoke are required, no full suite or model calls.

## Execution report without human grading — owner approved 2026-10-26

Suspend human grading at this stage, leave both Forms untouched. Produce a descriptive
report from160existing outputs, separately within each agent. No new generation or
Jev calls. Deterministic full-text raw equality, whitespace-collapsed equality,
character SequenceMatcher change (autojunk=False), length change, CLI time and usage;
none are editorial-quality scores. Source-level dot plots and heatmaps, median and IQR,
no quality inference, cross-agent ranking, significance tests or population CIs.
Capture provenance, fail on incomplete/tampered inputs; use reconciled Jev cost table
rather than mixing new-cohort known cost with cumulative totals. Route: Spec Kit014
existing amendment → tasks/implement; independent statistical/code review and meaningful
metric oracles. Standard-library analysis, existing ReportLab SVG/PDF + Sharp PNG300DPI.
