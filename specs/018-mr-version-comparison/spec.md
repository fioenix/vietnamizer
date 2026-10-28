# Feature 018: Codex comparison of MR01–MR12

Created2026-10-27. Owner now explicitly authorizes running the previously manual
regressions on frozen0.12.0 and0.12.1; this is a separate evaluation, superseding
only the prior no-new-benchmark limit for these cases. Existing cohorts/Forms,
source rules and previous evidence remain unchanged.

## User stories and acceptance
US1(P1): Run the same supplied source/request under the two complete instruction
snapshots on the same Codex model/effort, in fresh sessions, with all raw retained.
US2(P1): Report achieved/not-achieved against frozen expectations for each logical
MR case, distinguishing exact checks, host interpretation and insufficient evidence.
US3(P2): Preserve historical evidence and make results reproducible without inference.

Acceptance:12logical cases; MR10 literal/uncertain and MR11 review/final-only are
separate subscenarios, giving14scenario pairs and28planned single generation calls.
A failed or unclear attempt stays visible, without silent retry or favorable reroll.
Expected answers, old bad candidates and case IDs are not supplied as editing guidance.
Source context/request and all non-version instructions are identical within pairs.

## Requirements
Freeze corpus, case provenance, rubric, full context, profiles/references, source
hashes, wrapper, model/effort, seeded order and28start cap before generation. Do not
send a personal style profile, calibration table, labels or prior outputs to the model.
Capture binary stdin/stdout/stderr, schema/argv, usage/session/status and errors.
Operational tool calls, resumed sessions or invalid native/schema completion cannot
be accepted as uncontaminated results. CLI raw is not provider HTTP raw.
Case MR09 permits keeping or consistently normalizing emphasis delimiters; opportunity
uptake must not be hidden inside safety-pass counts. MR11 review observations are
optional under original expectations; report their presence separately from mandatory
meaning preservation and final-only output integrity. Ambiguous meaning judgments stay
explicit rather than becoming exact-string gold. Aggregate logical cases over all
required subscenarios and never pool them as independent natural-language samples.

## Outcomes and limits
Deliver28attempt records or explicit missing/error states,14paired scenario results,
12logical MR summaries, concrete before/after examples, raw archive and preservation
hashes. This is a development-regression probe using host-proposed criteria, not a
heldout quality benchmark, blinded human study or causal population claim. No source
rule tuning during the run, no Jev API, Forms access, install, publication or push.
