# Jev recovery diagnosis — 2026-10-25

The original three unvalidated requests cannot be diagnosed retrospectively: their transport
exceptions and failed reply bodies were not retained. The observed harness defects were collapsing
transport/schema/artifact failures into `service_failed` and saving replies only after validation.
The benchmark-only capture now retains request and reply bodies before validation, HTTP status,
elapsed time, validation reason and partial-body flags. Production `jev/` has not been changed.

P01/P02 one-record diagnostics returned HTTP 200 and validated. This confirms current successful
execution of those exact payloads, not the cause of the historical failures.

## First newly observed failure

After four new Codex + Jev finals completed, P05 stopped before Codex generation. New request
`0092` (125th cumulative network attempt) returned HTTP 200 with complete 7,574-byte response.
The retained raw reply contains:

- Check: `V9_s_9abf0da6d32d07c5841cf372_degree`.
- Reported score: `0.51`.
- Probabilities: level 0 = `0.60`, 1 = `0.32`, 2 = `0.08`, 3 = `0.00`.
- Probability-weighted mean: `0.48`; difference = `0.03`.
- Validator rejection: `score_distribution` (existing tolerance `0.025`).

The live [Score contract](https://docs.typesafe.ai/primitives/score), checked 2026-10-25, defines
Score as the probability-weighted mean of level numbers. The observed reply fails the current
runner's consistency check. No evidence establishes whether this is provider arithmetic,
serialization precision or another provider-side cause. Do not loosen the tolerance around the
observed answer, rewrite the raw response, or reroll valid semantic answers to conceal the failure.

Raw evidence is local under `artifacts/014-jev-recovery-20261025/requests/0092/`:
`request.body`, `response.body`, `request.json`, `response.json`, `http.json`, `record.json`.
Known request usage is 11,327 input tokens, USD 0.000475734; it remains in cumulative spending.
The P05 pass retains 703 validated checks and 249 missing checks. Its final is not completed.

Independent review approved the per-question amendment and verified the first live P05 repair.
It preserved 39 valid answers, requested only the inconsistent Score, and received all 952
required remote answers before a new Codex final. Original and repair network costs are retained
separately; the composite is explicitly derived evidence with sealed per-answer provenance.
The same policy applies to observed Choice inconsistencies at P07 request 0126 and P09
request 0154. No tolerance was relaxed; no valid semantic answer was resampled. No new semantic answer is accepted solely
because its numbers are favorable; no quality claim is established by execution or schema validity.
