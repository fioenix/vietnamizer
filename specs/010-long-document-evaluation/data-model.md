# Data model: Prioritized evaluation within a request budget

All entities are local, in-memory, and rebuilt on every invocation. Nothing is persisted by the
runner; the host decides whether to keep a report and pass its `answered_checks` block back.

## Check key (existing)

`(group_index, subject_index, recipe_key)` as produced by `Ledger.checks` (`jev/coverage.py`).
Valid only inside one invocation, because group indexes depend on candidates and section order.

## Evaluation request (input, new)

Optional top-level `evaluation` object of the input document.

| Field | Type | Rule |
|---|---|---|
| `requests` | integer | 1 or more; above 32 is capped to 32 and reported; absent means 32 |
| `focus` | list of `{start, end, patterns?}` | schema 2 only; source-global half-open code-point offsets inside the source; `patterns` lists registry IDs; at most 256 spans |
| `previous` | object | an `answered_checks` block from an earlier full-scope report |

Validation failures (wrong types, 0 or negative `requests`, out-of-range spans, unknown pattern IDs,
`focus` in schema 1, a `previous` block that fails R5's checks) make the invocation `invalid_input`
before any request. The object is part of the input digest, so it is bound into `input_digest` and
`manifest_digest` like every other input field. The 256-span cap and the per-span charge to the
preparation work budget keep focus processing inside existing bounds.

## Priority tier (new)

| Tier | Name | Source |
|---|---|---|
| 1 | `candidate` | review checks of candidate edits |
| 2 | `focus` | checks overlapping a focus span, filtered by its patterns |
| 3 | `signal` | checks of a pattern whose registry signal matches the subject or unit |
| 4 | `spread` | all other checks |

Each check has exactly one tier, its highest. Tier is assigned after previous-answer removal.

## Signal (registry field, new)

`signals: [<python regex>]` on a registry pattern entry, generated from `scripts/scan-tells.sh`,
keeping only top-level alternatives that match, without line anchors, the pattern's own `SKILL.md`
section (research R4). At `5420c8c` that leaves signals for T2, T4, T5, V9, V11, V12 and V15.
Matched with `re.MULTILINE` against the unit's editable text (protected spans blanked). Absent or
empty means the pattern never reaches tier 3.

## Request plan (new)

Ordered list built before any request (research R1).

| Field | Meaning |
|---|---|
| `unit` | section ID |
| `start`, `end` | unit source span |
| `tier` | tier of the request's first (highest) check |
| `questions` | number of checks packed |
| `tiers` | count of packed checks per tier |

Internally each entry also holds its check keys; those never leave the process. Invariants:

- at most `requests` entries; each entry respects the per-request limits;
- every check appears in at most one entry;
- the `tier` sequence is non-decreasing;
- within tier 4, every entry for a unit not yet reached precedes any entry for a reached unit; a unit
  is reached when an earlier entry in this plan targets it or one of its checks matched a key in the
  accepted previous block.

## Reuse key (new)

`sha256(encoded([model, pattern_entry_digest, recipe_key, unit_state_digest, subject]))[:16]` hex,
where `unit_state_digest` covers the redacted unit state without `targets` or `edits`, and `subject`
is the redacted target text with its unit-local offsets, the candidate state, or `null` for
paragraph scope (research R5). Computed only for checks being planned or answered.

## Answered-checks block (report field, new)

| Field | Meaning |
|---|---|
| `encoding` | `answered-checks-v1` |
| `model`, `registry_digest`, `config_version`, `segmentation_profile`, `scope` | binding; `scope` must be `full` to be reused |
| `own` | reuse keys validated in this invocation |
| `carried` | reuse keys accepted from the previous block (its `own` plus its `carried`) |
| `receipts` | `{request_digest: [indexes into own]}` for this invocation's validated receipts |
| `previous_digest` | digest of the accepted previous block, or `null` |

Acceptance rules are in research R5 and the contract table. As untrusted input, a block must also
have `encoding` `answered-checks-v1`; every key in `own` and `carried` must be 16 lowercase hex digits
and unique across both lists; `own` holds at most 1,536 keys (32 requests × 48 questions); every
`receipts` index must point into `own`, and each `own` key must be named by exactly one receipt;
`previous_digest` is `null` or 64 lowercase hex digits. `carried` has no count limit of its own; the
1 MiB input limit bounds it. A report never counts `carried` keys as answered.

## Priority summary (report field, new)

| Field | Meaning |
|---|---|
| `budget`, `budget_capped` | effective request budget and whether the input was capped |
| `tiers` | per tier: `planned`, `unplanned`, `answered`, `missing`; `prepare` fills `planned` and `unplanned` only |
| `units_reached` | units with at least one planned (prepare) or validated (evaluate) check |
| `skipped_previous` | checks not planned because an accepted previous block answered them |
| `invalid_replies` | count, at most 3 |
| `plan` | `prepare` only: the request plan without check keys |

## Judgment (existing, extended)

Adds `tier` (1–4): the tier of the check that produced the judgment.

## Missing record (existing, extended)

Adds `missing_by_reason: {reason: count}` and `missing_by_tier: {tier: count}`. `reason` stays a single value chosen by precedence
`invalid_response` > `deadline_exceeded` > service, authentication, cancellation and permission
reasons > `budget_exhausted` > `answered_previously`. `budget_exhausted` replaces `limit_exceeded`.
`answered_previously` marks checks skipped because an accepted previous block answered them; they
stay missing in this report, which counts only its own answers.

## Run state transitions (evaluate)

```text
planned ──send──▶ validated
   │                │
   │                └─(reply invalid)──▶ invalid_response ──(3rd)──▶ stop: rest invalid_response
   ├─(auth/service/cancel/deadline)──▶ stop: rest marked with that reason
   └─(never sent, budget spent)──▶ budget_exhausted
unplanned (beyond budget) ──▶ budget_exhausted
skipped (previous block) ──▶ answered_previously; counted in skipped_previous, listed as missing
```
