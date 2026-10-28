# Recorded Jev recovery protocol

Owner explicitly authorized diagnosis, complete raw capture and completing all 20 documents within
the SAME cumulative USD 2 cap on 2026-10-25. Earlier no-retry/fallback-only dispositions remain
historical; no raw result or archive from those epochs is overwritten.

## Evidence and spending

Use benchmarks/jev_capture.py for benchmark-only fixed-origin HTTP capture; production jev/
remains unchanged. Capture request bytes, response bytes before JSON/schema validation, HTTP
status, timeout/phase and partial-body size/digest. Authorization is memory/stdin only; auth
headers never enter artifacts. A rare credential echo is redacted before any disk write.
Only an observed EOF permits flushing the complete sanitized body; interrupted/oversized
responses retain a safe prefix and are explicitly partial. Maximum response is 1 MiB.

A reservation of 65536 input tokens precedes every fresh request. The budget includes the 33
old requests once, including 3 unknown-billing reservations, plus every new diagnostic/retry.
Global max 640 network requests, max 32 per document across epochs, USD 2 total. No fallback API,
long context, purchased credits, auto-upgrade or resampling of a validated answer. Model pinned
jev-1.14.0; official price checked 2026-10-25 remains USD 0.042/M input tokens, free output.

Cache reuse requires exact request/input/model bindings, validated core receipts and raw-reply
schema/digest reconciliation. New pass seals bind source/manifest/input; replayed evidence is
recorded separately and is not a fresh paid call. All recovery source snapshots are retained.

## Completion versus semantic uncertainty

Offline end-to-end reproduced 876 validated P01 answers, one mechanical check and zero missing
checks while native scope_complete/evaluation_complete stay false. coverage.py intentionally
marks context incomplete for insufficient-context choices. That is an advisory abstention,
not a failed request. Do not retry valid answers to erase uncertainty.

For the requested 20-document run, execution completion requires answers_complete, zero
uncompleted checks, source_accounted, segmentation_complete and actual validated remote answers.
Semantic context completeness and evaluation_complete remain separate native fields. Advice
keeps these flags and dispositions that say to ignore unsupported scores. Generation never
uses a numerical policy to automatically apply/block edits. Independent human assessment remains
pending; execution completion does not establish correct Vietnamese editing.

## Bounded recovery and final outputs

One-record diagnostics first: P01's historically failed payload returned HTTP 200 in 3.026s;
P02's first payload returned HTTP 200 in 1.058s. These successes do not establish old failure cause.
The previously missing bodies cannot be recovered retrospectively. The observable harness bugs
were saving replies only after validation and collapsing unrelated errors into service_failed.

At most 3 recovery passes per case, replaying prior valid requests. Retry only observed timeout,
deadline/network failures or HTTP 429/5xx; respect bounded Retry-After, stop for schema/4xx or
artifact failures and diagnose offline. Each pass and failed request stays in the ledger.
An intentional diagnostic max-new limit is distinguished from a service failure.

Before each new Codex final, reconstruct checks and independently replay the whole evaluation
without network to prove answer accounting from retained raw replies. Use the same frozen source,
initial draft and revision instructions. New 20 Codex+Jev outputs replace the old fallback/partial
arm in a new 80-output review packet. Reuse the previous 20 self-review controls and 40 baselines,
recording source epochs and temporal reuse. Never overwrite the old 40 Codex outputs or old packets.
Quality claims require the independent reviews and a separate holdout; model backend version
attestation is still unavailable in the native Codex records.

## Per-question schema recovery amendment

A later raw capture reproduced `score_distribution` on P05 and `choice_distribution` on P07.
Both failures are internal inconsistencies in the returned fields, not unavailable context.
The existing full-batch validator correctly stopped. The diagnostics are retained; these
observations do not retroactively diagnose the three missing historical replies.

The reviewed successor adapter may recover ONLY these two observed inconsistency classes.
First validate the envelope/model/IDs/usage, then validate every answer separately with the
unchanged core validator. Preserve all individually valid answers. A new request contains only
the invalid question(s), with the same full state, model, instructions and criteria. No valid
answer is resampled. At most one repair network attempt per failed original request; an invalid
repair stays unresolved rather than triggering an unbounded loop. All existing cash, request,
pass and Codex-start caps remain in force.

Any assembled response is explicitly `composite_evidence`, never a provider raw response.
Retain the original HTTP body, repair HTTP body, per-check source mapping, composite seal and
adapter/finish-manifest binding. Its logical usage sums distinct supporting provider sources;
the spend ledger counts only actual network attempts once. Independent replay must reconstruct
and validate every check from its original provider response before Codex sees the advice.

This is a repair of an invalid interface response under the existing finish-20 authorization,
not permission to change score tolerances, derive replacement answers or reroll uncertainty.
Freeze and independently review the adapter before any new repair inference.
