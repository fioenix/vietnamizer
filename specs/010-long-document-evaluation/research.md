# Research: Prioritized evaluation within a request budget

All measurements were taken on branch `codex/010-long-document-evaluation` at `5420c8c` (runner
`jev-1.14.0`, profile `vi-spans-2`) on the maintainer's machine, with synthetic notes built from the
`SECTION` template in `tests/test_preparation_limits.py`. A fake transport answered every request
validly. Numbers describe this machine and these fixtures only.

## R1. One static request plan shared by `prepare` and `evaluate`

**Decision**: Compute the whole request plan before the first request: an ordered list of requests,
each naming one unit and its check keys. `prepare` reports this plan; `evaluate` sends exactly its
requests in order. Replies never reorder or add work; they only decide which planned requests are
still sent (FR-014, FR-015).

**Rationale**: FR-008 and SC-001 require the plan and the run to match exactly. Today the scheduler
packs batches while it sends (`jev/core.py:412–431`), and halts depend on replies, so an estimator
written separately would drift. With one function producing the plan, equality holds by
construction and the test only has to confirm that the sender follows the list.

Building a payload needs redaction (`protected_matches`/`redact`, now closures inside `evaluate`),
because packing is limited by encoded bytes. Those helpers move to a small builder used by both
commands; their behaviour does not change.

**Bounds (FR-010)**: planning checks the invocation deadline between phases and while packing. If
it expires, no request is sent, the plan built so far is reported with `deadline_exceeded`, and
every unplanned check carries that reason. Focus spans (at most 256) are charged one unit each to
the preparation work budget. Previous keys are validated and matched in linear time with a set,
bounded by the 1 MiB input limit. Tier assignment visits each check once, and checks are bounded by
the 4,096 unit-plus-sentence inventory cap of feature 009.

**Measured cost**: the current depth-first packer sends 32 requests for the ~12,100-word note in
4.5 s including preparation (fake transport). The plan has the same number of requests and the
same per-request packing loop, plus tier assignment (R3) and previous-answer matching (R5), each
measured below at well under 1 s for that note. Planning shares the existing 120 s deadline.

**Alternatives considered**:

- Estimate by a separate counting pass. Rejected: two implementations of byte-limited packing
  drift, which is exactly the failure SC-001 guards against.
- Plan lazily, one request ahead. Rejected: it cannot report the full plan before any request.

## R2. Priority input lives in the input document

**Decision**: Add an optional top-level `evaluation` object to the input document:

- `requests`: the budget X, an integer. 0, negatives and non-integers are `invalid_input`; values
  above the per-invocation limit (32) are capped and the report says `budget_capped: true`.
  Missing means 32.
- `focus`: host-named source spans, each `{start, end, patterns?}`, source-global offsets as in
  schema 2 annotations, with optional pattern IDs. Schema 2 only; in a schema 1 document it is
  `invalid_input`.
- `previous`: the `answered_checks` block of an earlier report (R5).

Candidate edits keep their existing fields; they are tier 1 without any new input.

**Rationale**: The document is already the single authorized, size-limited input, and its digest
already binds every report (`input_digest`, `manifest_digest`). Putting priorities there means the
plan is bound to them too, and the CLI needs no new flags. Unknown top-level keys are not rejected
today, so older runners ignore the object; the report's `priority` block (data model) shows a host
whether the object was honoured.

**Alternatives considered**: CLI flags (`--budget`, `--focus`). Rejected: they would sit outside the
digest and the `prepare`/`evaluate` parity, and spans do not fit on a command line.

## R3. Tier assignment and request order

**Decision**:

- Tier 1: the four review checks of every candidate edit.
- Tier 2: for each focus span, the sentence- or unit-scope checks whose subject overlaps the span,
  and the paragraph-scope checks of every unit the span overlaps; limited to the listed patterns
  when `patterns` is given. Unknown pattern IDs and spans outside the source are `invalid_input`.
  Spans over protected text add nothing, because protected text has no checks.
- Tier 3: checks of a pattern whose local signal (R4) matches in the unit's editable text; for a
  sentence- or unit-scope pattern only the subjects containing a match, for a paragraph-scope
  pattern the whole unit.
- Tier 4: every other remaining check.

A check belongs to its highest tier. Request order: the next request is opened for the unit that
owns the highest-tier unplanned check, ties broken by document order; in tier 4 a unit not yet
reached comes before any reached unit. A unit is reached when this plan already has a request for
it or one of its checks matched a key in the accepted previous block (R5), so a second run spreads
to units the first run did not touch instead of revisiting them in document order. The request is then filled, within the
existing limits (48 questions, 48,000 encoded bytes, 16 targets), with that unit's unplanned checks
in within-unit order: tier ascending, then today's order (paragraph recipes, then sentence by
sentence across patterns, then candidate reviews).

**Rationale**: This is the order the owner chose, made deterministic (FR-004) and compatible with
one-unit requests. Filling from the same unit uses room that would otherwise go unused (FR-005) and
is the only way to fill it, because a request cannot carry a second unit's paragraph.

**Effect on runs that fit**: when all work fits in the budget, every check is still planned exactly
once (FR-018). Only the position of tier 3 checks inside a unit changes, which can move a byte
boundary by a few questions. Existing tests that count requests for small inputs are rerun
unchanged as the check (SC-007); a test that fails here is reported, not loosened.

**Alternatives considered**: interleave units within one tier (one request per unit per tier).
Rejected for tiers 1–3: it delays a unit's remaining high-tier checks behind every other unit and
gains nothing when the budget covers the tier. Spreading is applied in tier 4 only, as decided.

## R4. Local signals come from `scripts/scan-tells.sh`

**Decision**: The registry generator (`scripts/build-jev-registry.py`) reads the `scan "<ID> ..."
'<regex>'` lines of `scripts/scan-tells.sh`, translates the one POSIX class used (`[[:space:]]` to
`\s`), compiles each expression in Python, and keeps only what the canonical pattern text supports:
each top-level alternative of an expression is kept when it matches, without line anchors,
somewhere in that pattern's own section of `SKILL.md` (heading to next heading), and dropped
otherwise. The kept alternatives are written into the pattern's registry entry as `signals`, and the
dropped ones are listed by the generator. `--check` fails when `scan-tells.sh`, `SKILL.md` and the
registry drift. Signals are matched with multiline anchors against the unit text with
protected spans blanked, the same text the mechanical T3 check reads.

**Rationale**: FR-003 requires signals that canonical pattern text states and that can be checked
without the service. `scan-tells.sh` is the maintainer's existing list of regex-checkable signs, and
its header already says that a hit only marks text for reading, but it was not written under that
requirement: analysis finding F4 showed alternatives absent from the canonical sections. Matching
each alternative against its own section turns FR-003 into a mechanical check without editing
`scan-tells.sh` or `SKILL.md`. One source avoids a second, diverging list. A signal only moves checks to tier 3, so a false hit costs
order, never coverage, and a pattern without a signal is unaffected.

**Measured grounding** (at `5420c8c`, unanchored match against each pattern's `SKILL.md` section):
kept in full for T2 (`—`), T4 (`, và `), T5 (both heading and bold-label forms) and V11 (all six
phrases); kept in part for V9 (all but `Thông qua`), V12 (all but `Thêm vào đó` and
`Chính vì thế`) and V15 (all but `triển khai thực hiện`); dropped for V16 (`được [a-zà-ỹ]+ bởi`) and
V18 (`, (điều|việc) này [a-zà-ỹ]`), whose sections show the sign in forms the expression does not
match. V16 and V18 therefore have no tier 3 signal until their canonical text or the scan line
changes; that is rule maintenance and out of scope.

**Measured speed**: the nine expressions over the 847 units of the ~12,100-word note took 1.8 ms; over a
1 MiB adversarial string (long `**` runs and spaces) 0.01 s. All nine are alternations and
character classes without nested quantifiers.

**Alternatives considered**:

- Hand-written signals in the generator. Rejected: a second list that drifts from `scan-tells.sh`.
- Ask the service to rank units. Rejected in the spec: it spends the scarce requests.

## R5. Previous answers are matched by per-check reuse keys

**Decision**: Every validated check gets a reuse key: the first 16 hex digits of SHA-256 over the
model, the registry entry of its pattern, the recipe key, the unit's request state without targets
or edits (redacted paragraph, related paragraphs, register, audience, purpose, kind, profile) and
its subject (the redacted target text and offsets, or the candidate state, or nothing for paragraph
scope). Each report carries an `answered_checks` block with the keys it validated itself, the keys
it carried forward from an accepted previous block, the receipts that produced its own keys, and a
digest of the previous block it accepted.

A run given `evaluation.previous` accepts it only when the block's model, registry digest,
configuration version and segmentation profile equal the current ones, every own key is listed
under one of the block's validated receipts, and the block is the full-scope kind. Otherwise the run
is `invalid_input` before any request. Because the block is untrusted input, the run also rejects a
wrong `encoding`, keys that are not 16 lowercase hex digits or repeat across `own` and `carried`,
more than 1,536 `own` keys, receipt indexes out of range or naming one key twice, and a malformed
`previous_digest` (analysis finding F5). Planning drops every check whose key is in the accepted
block's own or carried keys.

**Rationale**: `manifest_digest` binds the whole input, including candidates and the new
`evaluation` object, and group indexes shift when a candidate is added (`jev/coverage.py:65–71`).
Either would reject every realistic second run, in which the host has new candidates. A key per
check binds exactly what the question saw, so a changed paragraph, context, register or
replacement invalidates only the affected checks. The other targets in a request belong to the same
paragraph, which the state already carries, so they do not change what a check means.

**Deviation from the spec, accepted by the owner on 2026-10-22**: FR-011 and one edge case say a previous report
from a different document, or from a document changed between runs, is rejected. This design binds
the block to model, registry, configuration and segmentation profile only, and binds each check to
its own unit state. A changed document is therefore accepted: checks of unchanged units are skipped,
and checks of changed units, including the units a host just edited, are planned again. Rejecting a
changed document would make every run after the host applies an edit start from zero. Boundary
overrides still invalidate exactly the sentences they move, because a moved sentence has a
different subject. FR-011, a User Story 3 scenario, SC-005 and the edge case were reworded to this
rule before `speckit-tasks`.

**Integrity limit**: the runner has no secret, so it cannot tell a forged block from a real one.
The checks catch corruption and mismatched bindings (FR-011, FR-012). A forged block can only make
the forger skip checks, and the new report never counts skipped checks as answered (FR-013).

**Measured size**: 1,536 keys (32 requests × 48 questions) encode to 30,720 bytes of JSON. With the
1 MiB input limit and a ~60 KB note, a chain of about 28 runs fits before carried keys exhaust the
input; the advisor reference says so. Hashing 89,299 keys took 0.15 s.

**Alternatives considered**:

- Reuse by `manifest_digest` and group index. Rejected for the reasons above.
- Pass several earlier reports. Rejected: carrying keys forward keeps one block and one input.
- Feed back the previous answers themselves. Rejected: the new run does not need them, and they
  would bring answer text into the input.

## R6. Invalid replies: drop the batch, stop at the third

**Decision**: A reply that fails validation (`InvalidResponse`, or the decoding errors that today
also become `invalid_response`) marks that request's checks missing with reason
`invalid_response`, keeps the receipt's fixed validation reason and check ID, and increments a
counter. The run continues with the next planned request. At the third invalid reply the run stops
and marks every unsent planned check `invalid_response`. Authentication failure, service failure,
cancellation and the deadline stop at once, as today.

**Rationale**: Owner decision Q2. A failed batch is never resent, so feature 008's no-retry rule
(research R5 of 008) still holds. The stop count is an operational spend guard, not a language
threshold, so constitution principle IV does not apply to it. The fault test that asserts stopping
at the first invalid reply (`tests/test_coverage_faults.py:7`) changes with this feature.

## R7. Report changes

**Decision**:

- Request-budget exhaustion is reported as `budget_exhausted`, replacing `limit_exceeded`; only
  `tests/test_jev.py:196` and `jev/core.py` use the old reason, and no host document names it.
- Each `missing` record keeps one `reason` (precedence: `invalid_response`, `deadline_exceeded`,
  service and permission reasons, then `budget_exhausted`) and gains `missing_by_reason`, so a group
  that lost one batch and ran out of budget for the rest is reported exactly.
- A new `priority` block reports the budget, whether it was capped, per-tier counts (planned,
  answered, missing), units reached, and the accepted previous block's digest. `prepare` returns
  the same block with `planned` and `unplanned` per tier and a `plan` list of
  `{unit, start, end, tier, questions, tiers}` per request.
- Every judgment carries its check's `tier`, and every `missing` record gains `missing_by_tier`,
  so the report shows which tier each answered and each missing check belongs to (User Story 1,
  Key Entities).
- `answered_checks` (R5) is added to `evaluate` reports.

None of these fields contains source prose (FR-017). Large lists use the existing `templates-v1`
compaction when they cross its threshold.

## R8. Documentation and exit codes

**Decision**: `references/typesafe-advisor.md` gains a short section: exit 0 for `evaluated`,
`key_absent` and `prepared`; exit 2 for every other status, with the JSON report on standard output
in every case; how to set `evaluation`; how to read the plan; and what to tell the user for a
partial run. Exit codes themselves do not change. `SKILL.md` is not changed, because it already
defers runner details to the reference.

## R9. Verification approach

- RED first: synthetic tests for each acceptance scenario, written before the code they cover.
- Plan–run equality (SC-001) on the three synthetic sizes, with and without focus and candidates.
- Ordering (SC-002, SC-003) from receipts: the tier of each request's first check is
  non-increasing across the run.
- Spread (SC-004): count units with at least one validated answer.
- Chained runs (SC-005): no reuse key appears in two runs' own keys.
- Invalid replies (SC-006): fake transport returning invalid replies at chosen requests.
- Existing limit, time and privacy tests unchanged (SC-007), apart from the two contract changes
  named in R6 and R7.
- The earlier throwaway measurement becomes a test of the depth-first baseline numbers only if it
  stays stable; otherwise it is recorded in `evidence.md`, not kept.
