# Contract delta: prioritized evaluation (config v2, input schemas 1 and 2)

This document amends the runner contract in `references/typesafe-advisor.md` and feature 008's
coverage contract. Everything not listed here is unchanged: request and invocation limits, model,
transport, redaction, protected text, context rules, exit codes and the `prepare`/`evaluate`
commands.

## Input: `evaluation` object

```json
{
  "evaluation": {
    "requests": 8,
    "focus": [{"start": 1200, "end": 1340, "patterns": ["V11", "T4"]}, {"start": 5100, "end": 5180}],
    "previous": {"encoding": "answered-checks-v1", "...": "block from an earlier report"}
  }
}
```

| Case | Result |
|---|---|
| object absent | budget 32, no focus, no previous; tiers 3 and 4 decide the order |
| `requests` 1–32 | budget as given |
| `requests` > 32 | budget 32, `priority.budget_capped: true` |
| `requests` ≤ 0, not an integer, or boolean | `invalid_input` |
| `focus` in a schema 1 document | `invalid_input` |
| focus span outside the source, `start >= end`, or more than 256 spans | `invalid_input` |
| unknown pattern ID in `patterns` | `invalid_input` |
| focus span only over protected text | accepted; adds no checks |
| `previous` with another model, registry, config, segmentation profile or a non-full scope | `invalid_input` |
| `previous` whose `own` keys are not all listed under its `receipts` | `invalid_input` |
| `previous.encoding` other than `answered-checks-v1` | `invalid_input` |
| a key in `own` or `carried` that is not 16 lowercase hex digits, or appears twice across them | `invalid_input` |
| `own` with more than 1,536 keys, or `receipts` whose indexes are out of range or name one `own` key twice | `invalid_input` |
| `previous_digest` neither `null` nor 64 lowercase hex digits | `invalid_input` |

## Order of work

1. Remove checks whose reuse key is in an accepted `previous` block (`own` or `carried`).
2. Assign each remaining check its highest tier: 1 candidate, 2 focus, 3 signal, 4 spread.
3. Open the next request for the unit owning the highest-tier unplanned check (document order breaks
   ties). In tier 4, units not yet reached come first: no request earlier in this plan and no check
   matched in the accepted `previous` block.
4. Fill the request with that unit's unplanned checks, tier ascending then today's within-unit order,
   up to 48 questions, 48,000 encoded bytes and 16 targets.
5. Stop planning at the budget. Everything unplanned is `budget_exhausted`.

`prepare` and `evaluate` run steps 1–5 with the same code and report the same plan. Planning checks
the invocation deadline between steps and while packing; if it expires, no request is sent, the
plan is reported as built so far with `deadline_exceeded`, and every unplanned check carries that
reason. Each focus span is charged one unit of the preparation work budget; previous keys are
validated and matched in linear time, bounded by the 1 MiB input limit.

## Replies

| Event | Effect |
|---|---|
| valid reply | checks validated; reuse keys added to `answered_checks.own` |
| invalid reply, 1st or 2nd | batch `invalid_response`; next planned request is sent |
| invalid reply, 3rd | batch and every unsent planned check `invalid_response`; run stops |
| authentication or service failure, cancellation, deadline | run stops at once, as today |

No batch is resent. No run starts another run.

## Report additions

| Field | Command | Notes |
|---|---|---|
| `priority` | both | budget, capped flag, per-tier counts (`planned`, `unplanned` in `prepare`; `planned`, `answered`, `missing` in `evaluate`), units reached, skipped previous, invalid replies; `prepare` adds `plan` |
| `judgments[].tier` | evaluate | tier of the check that produced the judgment |
| `missing[].missing_by_tier` | both | counts per tier |
| `answered_checks` | evaluate | `answered-checks-v1` block, the only field a host passes back as `previous` |
| `missing[].missing_by_reason` | both | counts per reason |
| reason `budget_exhausted` | both | replaces `limit_exceeded` |
| reason `answered_previously` | both | skipped because the accepted previous block answered it |

No added field contains source text. `status`, `evaluation_complete` and exit codes keep their
meaning: a run that skipped checks answered earlier is not `evaluated`, because its own answers do
not cover the scope.

## Exit codes (documented, unchanged)

| Code | Statuses |
|---|---|
| 0 | `evaluated`, `key_absent`, `prepared` |
| 2 | every other status, including `incomplete`, `preparation_incomplete`, `permission_denied`, `invalid_input` |

The JSON report is written to standard output in both cases.
