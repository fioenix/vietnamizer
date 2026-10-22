# Feature Specification: Prioritized evaluation within a request budget

**Feature Branch**: `codex/010-long-document-evaluation`

**Created**: 2026-10-22

**Status**: Draft. Owner asked on 2026-10-22 to open the next feature for the evaluation limits that
feature 009 left out of scope. Owner decision the same day: full evaluation of a long note is not
the goal. A host sets a request budget X, the runner spends at most X and chooses the checks by a
fixed priority order (candidate edits, then host-named text, then local mechanical signals, then
unreached units). A previous report is used only to avoid repeating answered checks. This replaces
the continuation and unit-order questions of the first draft. Owner answered Q2 the same day: drop
an invalid batch, continue, and stop after 3 invalid replies in one run. No open decisions. Not
planned, not implemented. The branch starts from the unmerged feature 009 tip `5420c8c`, because
long documents only reach evaluation once feature 009's preparation fixes are in place. Revised
during planning on 2026-10-22: research R5 binds previous answers per check instead of per document,
so FR-011, a User Story 3 scenario, SC-005 and one edge case now accept a changed document and
re-plan only its changed units. The owner accepted this deviation on 2026-10-22 and authorized
`speckit-tasks`.

**Input**: Open the next feature for the evaluation limits: request preflight, breadth-first
scheduling, chunked or resumable evaluation, continuing after an invalid response, and host
documentation for exit codes and documents longer than the budget. Revised by the owner: evaluate
up to a budget X and choose the evaluated work so that it is worth the most.

## Background

Feature 009 made long Markdown notes prepare fully. On the owner's private reported note, preparation
now yields 281 units and 382 sentences with no `preparation_limit` region. Preparing a note is not
evaluating it: one invocation is still bounded by 32 requests, 48 questions and 48,000 encoded bytes
per request, and 120 seconds in total. These are local safety and spend limits accepted in feature
008 (`specs/008-sentence-coverage/research.md`, R5) and this feature keeps them.

Observed in the session that opened feature 009 (reported note, before feature 009, live service):

- The scheduler works through units in document order and sends all of a unit's checks before
  moving on. A heading or one-sentence unit under the technical profile needs 86 checks.
- Requests carried 35–42 questions, not 48, because the byte limit fills first. One invocation
  therefore validates about 1,200 questions at most.
- The run stopped at its first `invalid_response` (validation reason `score_distribution`) after 26
  requests and 20 seconds; every later unit was blocked. Stopping on an invalid response is a tested
  contract (`tests/test_coverage_faults.py`).
- `python3 -B -m jev` exits 2 for every status except `evaluated`, `key_absent` and `prepared`.
  No host-facing document mentions the exit code.

Observed on branch tip `5420c8c` with synthetic technical notes and a fake transport that always
returns valid answers (a throwaway script built from the synthetic section in
`tests/test_preparation_limits.py`; to be kept as a test during planning):

| Synthetic note | Units | Checks required | Validated in one invocation | Units reached |
|---|---|---|---|---|
| ~1,000 words | 70 | 7,381 | 1,018 (13.8%) | 9 |
| ~6,000 words | 420 | 44,281 | 1,018 (2.3%) | 9 |
| ~12,100 words | 847 | 89,299 | 1,018 (1.1%) | 9 |

Each request carries one unit's paragraph and context, so X requests reach at most X units, and
each unit gets at most 48 questions per request. Choosing well therefore means choosing which units
get a request and which of their checks fill it. Asking the service to rank units would spend the
same requests that are scarce, so the ranking must come from the host or from local signals.

The order is deterministic and honest about what it skips. Whether it finds more real errors per
request than another order cannot be measured yet: the repository has no labeled corpus for that
(`AGENTS.md`, "Những việc còn thiếu"). This spec does not claim the order is optimal.

## Clarifications

### Session 2026-10-22

- Q: Should several invocations add up to full evaluation (first-draft Q1)? → A: No. The host sets a
  budget X and the runner evaluates up to X. Chaining invocations is allowed, but a previous report
  only removes checks that already have a validated answer; reaching full evaluation is not a goal.
- Q: How should one invocation choose its work (first-draft Q1/Q3)? → A: By a fixed priority order:
  (1) checks of the host's candidate edits; (2) checks on text and patterns the host names;
  (3) checks whose pattern has a local mechanical signal in the unit; (4) remaining checks, spread
  across units not yet reached. The local signal orders work only; it never excludes a check.
- Q: Does one invalid reply still end the run (Q2)? → A: No. Drop that batch, continue with the next
  one, and stop the run after 3 invalid replies.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Spend a budget on the checks that matter most (Priority: P1)

A host editing a long note has candidate edits for some sentences and suspicions about others. It
runs one evaluation with a request budget X. The runner first checks the candidate edits, then the
text and patterns the host named, then patterns with a local signal in the text, and spends what is
left spreading across units nobody has reached yet. The report says which priority tier each
answered check came from and what remained unchecked.

**Why this priority**: It turns a fixed budget from "the first nine units in document order" into
evidence where the host is about to change text or already suspects an error, without changing any
limit or rule.

**Independent Test**: With a fake transport, evaluate a synthetic ~1,000-word note with candidate
edits late in the document, a few host-named spans and a budget of 8 requests; check from the
receipts that tiers were served in order.

**Acceptance Scenarios**:

1. **Given** candidate edits on a unit near the end of the note and budget X, **When** the host
   evaluates, **Then** every candidate check is sent before any request is opened for a lower tier,
   whatever the unit's position.
2. **Given** host-named spans with or without named patterns, **When** tier 1 is done, **Then** the
   checks for those spans (all applicable patterns, or only the named ones) are sent before any
   request is opened for tier 3 or tier 4.
3. **Given** no candidates or named spans, **When** the host evaluates, **Then** checks whose pattern
   has a local mechanical signal in the unit are sent before any request is opened for tier 4.
4. **Given** budget left after tiers 1–3, **When** the runner continues, **Then** each further request
   goes to a unit not yet reached (no request in this run and no answer in an accepted previous
   report), until none remains, and only then to reached units.
5. **Given** a request with room left after its unit's higher-tier checks, **When** the runner packs
   it, **Then** the room is filled with the same unit's next-priority checks, not left empty.
6. **Given** X is smaller than the higher-tier work, **When** the budget runs out, **Then** the report
   lists the unsent checks of every tier as missing, with reason `budget_exhausted`.
7. **Given** a host that sets no budget and no priorities, **When** it evaluates, **Then** the budget
   is the current request limit and tiers 3 and 4 decide the order.

---

### User Story 2 - Know what a budget buys before spending it (Priority: P1)

Before any request, the host runs the network-free preparation step with the same budget and
priorities and learns which units and checks of each tier the run would reach, how many checks full
evaluation would need, and how many remain uncovered. The host can tell the user what one run will
and will not check, and ask before spending more.

**Why this priority**: It needs no network, removes the surprise in the original report and gives
the user the numbers for every spend decision.

**Independent Test**: Prepare synthetic notes of about 1,000, 6,000 and 12,000 words with and without
priorities; evaluate them with a fake transport that answers validly; compare the plan with the run.

**Acceptance Scenarios**:

1. **Given** a prepared note, a budget and priorities, **When** the host runs preparation, **Then**
   the result lists the planned requests per tier, the units reached, the checks required for full
   evaluation and the checks left unplanned.
2. **Given** the same input evaluated with a fake transport that answers every request validly,
   **When** the host compares plan and run, **Then** requests, units reached and checks per tier
   match exactly.
3. **Given** a note that preparation could not finish, **When** the host runs preparation, **Then**
   the plan is marked provisional.
4. **Given** a unit whose context alone exceeds the request size, **When** the host runs preparation,
   **Then** the plan lists it as unreachable and spends no request on it.

---

### User Story 3 - Do not pay twice for the same check (Priority: P2)

A host that already ran one evaluation and has the user's authority for another passes the previous
report in. The new run skips every check that already has a validated answer for the same bindings
and spends its budget on the rest by the same priority order. The two reports together never claim
more coverage than was actually answered.

**Why this priority**: Without it, a second run under the same priorities repeats the first one's
work. It matters only once a host spends more than one run on a note.

**Independent Test**: With a fake transport, run twice on the same synthetic note, feeding the first
report into the second; count checks sent in both runs.

**Acceptance Scenarios**:

1. **Given** a first run's report, **When** the host runs again with it for the same input, **Then**
   no check with a validated answer in that report is sent again.
2. **Given** a report from a different registry, model, segmentation profile or configuration, or
   from a non-full-scope run, **When** the host supplies it, **Then** the runner rejects it before
   any request.
3. **Given** a first run's report and a document the host has since edited in some units, **When**
   the host runs again with it, **Then** checks of unchanged units with a validated answer are not
   sent again, and every check of a changed unit, or of a sentence whose boundaries moved, is
   planned again.
4. **Given** a report whose answers do not match their own recorded request digests and check keys,
   **When** the host supplies it, **Then** the runner rejects it before any request.
5. **Given** a previous report, **When** the new run ends, **Then** its report counts only answers it
   received itself, and refers to the previous report by digest; it does not merge the two into a
   claim of full evaluation.

---

### User Story 4 - One invalid reply does not end the run (Priority: P2)

A host receives one reply that fails validation partway through a run. That batch's checks stay
unanswered with the validation reason, and the runner goes on spending the budget instead of
blocking every later unit.

**Why this priority**: In the reported run a single invalid reply cost most of the budget. The fix
changes no limit and sends no extra data.

**Independent Test**: Use a fake transport that returns an invalid reply for one chosen request;
check that later requests are still sent and that only the failed batch is unanswered.

**Acceptance Scenarios**:

1. **Given** request 2 of a run returns an invalid reply, **When** the run continues, **Then** requests
   3 onward are sent, and the failed batch's checks are missing with reason `invalid_response`, the
   fixed validation reason and the check ID.
2. **Given** invalid replies keep arriving, **When** the stop condition in FR-014 is met, **Then** the
   run stops and marks the remaining work `invalid_response`.
3. **Given** an authentication failure, a service failure, a cancellation or the deadline, **When**
   it occurs, **Then** the run still stops at once, as today.
4. **Given** a failed batch, **When** the run continues, **Then** that batch is not resent in the
   same run.

---

### User Story 5 - Hosts know what a partial result means (Priority: P3)

A host reading the advisor reference learns what each exit code means, how to set a budget and
priorities, and what to tell the user when a run covers part of a note: the counts per tier, what
was left unchecked, and that the note was not fully checked by Jev.

**Why this priority**: Documentation only; it prevents misreporting.

**Independent Test**: Read the advisor reference and confirm it covers exit codes, budget,
priorities and the partial-result report; the package validator still passes.

**Acceptance Scenarios**:

1. **Given** the advisor reference, **When** a host looks up exit code 2, **Then** it finds which
   statuses produce it and that the JSON report is still written to standard output.
2. **Given** a plan that leaves checks uncovered, **When** a host follows the reference, **Then** it
   reports partial coverage with counts and asks the user before spending more.

### Edge Cases

- Host-named spans outside the source, overlapping a protected region, or naming an unknown pattern:
  out-of-range spans and unknown patterns are `invalid_input`; protected text stays excluded as
  today and is never promoted by a priority.
- Tier 1 or tier 2 alone exceeds the budget: higher tiers are served in document order within the
  tier, and the rest is reported as `budget_exhausted`.
- Two units tie within a tier: document order breaks the tie, so the same input always yields the
  same plan.
- A budget of 0, a negative budget or a budget above the request limit: 0 and negative values are
  `invalid_input`; values above the limit are capped at the limit and the report says so.
- The deadline expires while a batch is in flight: the reply is discarded and the run stops, as
  today.
- Every reply is invalid: the run stops after the third, so at most 3 requests are spent on invalid
  replies; no batch is resent.
- A unit's context is larger than one request: reported `context_too_large` and never planned.
- A previous report from single-pattern or selected diagnostic mode: rejected as input for a full
  run.
- The document changes between runs: the previous report is still accepted; a validated answer is
  reused only for a check whose unit state and subject are unchanged, so edited units, changed
  context, register or candidates, and sentences moved by boundary overrides are planned again.
- Preparation is incomplete: the plan is provisional; text without checks is never reported as
  covered.

## Requirements *(mandatory)*

### Functional Requirements

**Budget and priority (User Story 1)**

- **FR-001**: The host MUST be able to set a request budget X for one run; without it, X MUST equal
  the per-invocation request limit, and X MUST NOT exceed that limit.
- **FR-002**: The runner MUST send at most X requests and MUST choose checks in this order: (1) checks
  of the host's candidate edits; (2) checks on host-named source spans, restricted to host-named
  patterns when given; (3) checks whose pattern has a local mechanical signal in the unit; (4) all
  other checks, giving each further request to a unit not yet reached before any reached unit gets
  another request. A unit is reached when this run has planned a request for it or an accepted
  previous report holds a validated answer for one of its checks. A request is opened for the highest-tier unsent check; no request is opened for a
  tier while a higher tier has unsent, reachable checks.
- **FR-003**: Local mechanical signals MUST be derived from signs that the canonical pattern text
  states and that can be checked without the service, MUST only change order, and MUST NOT exclude
  a check or change which patterns apply.
- **FR-004**: Within a tier, ties MUST be broken by document order, so identical input yields an
  identical plan.
- **FR-005**: A request with room after its unit's highest-tier checks MUST be filled with the same
  unit's next-priority checks, within the per-request limits.
- **FR-006**: Every check not sent because the budget ran out MUST be reported missing with reason
  `budget_exhausted`; the report MUST give, per tier, the checks planned, answered and missing.

**Plan (User Story 2)**

- **FR-007**: Preparation MUST accept the same budget and priorities and report, without network
  access, the planned requests per tier, the units reached, the checks required for full evaluation
  and the checks left unplanned.
- **FR-008**: The plan MUST be computed by the same selection and batching rules as evaluation, so a
  run answered validly by a fake transport sends exactly the planned requests.
- **FR-009**: The plan MUST identify units by ID and source span only, MUST be marked provisional
  when preparation is incomplete, and MUST list units that fit no request as unreachable.
- **FR-010**: Planning MUST stay within the existing preparation deadline and work bounds.

**Previous report (User Story 3)**

- **FR-011**: The runner MUST accept a previous report only when its registry, model, segmentation
  profile and configuration bindings match the current run and it comes from a full-scope run;
  otherwise it MUST reject it before any request. The document may differ: a previous answer MUST
  be reused only for a check whose unit state (text, context, register, audience, purpose, kind,
  profile) and subject are unchanged, so every other check is planned again.
- **FR-012**: The runner MUST reject a previous report whose answers cannot be matched to their own
  recorded request digests and check keys, and MUST NOT send any check that has a validated answer
  in an accepted previous report.
- **FR-013**: A run's report MUST count only answers received in that run and MUST reference an
  accepted previous report by digest; the runner MUST NOT start another run on its own.

**Invalid replies (User Story 4)**

- **FR-014**: An invalid reply MUST leave that batch's checks missing with reason `invalid_response`,
  keep the fixed validation reason and check ID and never the provider body, and MUST NOT be resent
  in the same run. The run MUST then continue with the next batch, and MUST stop after the third
  invalid reply in that run, marking the remaining work `invalid_response`.
- **FR-015**: Authentication failure, service failure, cancellation and the deadline MUST still stop
  the run immediately.

**Unchanged limits and data**

- **FR-016**: The per-request limits (48 questions, 48,000 encoded bytes, 16 targets), the
  per-invocation limits (32 requests, 120 seconds, 15 seconds per request) and the 1 MiB input and
  response limits MUST NOT change.
- **FR-017**: A request MUST NOT carry more source or context text than an equivalent request does
  today; plans, priorities in reports and previous-report references MUST NOT contain source prose.
- **FR-018**: With no budget, no priorities and no previous report, a note whose work fits within the
  request limit MUST send every check exactly once, as today.

**Documentation (User Story 5)**

- **FR-019**: The advisor reference MUST list each exit code with the statuses that produce it and
  state that the JSON report is written to standard output in every case.
- **FR-020**: The advisor reference MUST describe how to set a budget and priorities, how to read the
  plan, and what to report when a run covers part of a note: counts per tier, what was not checked,
  and that the note was not fully checked by Jev; and it MUST say to ask the user before spending
  further runs.

### Key Entities

- **Request budget**: the maximum number of requests one run may send, set by the host, at most the
  per-invocation limit.
- **Priority input**: candidate edits (existing), host-named source spans with optional pattern IDs,
  and an optional previous report. Contains offsets and IDs, no new prose.
- **Priority tier**: 1 candidate, 2 host-named, 3 local signal, 4 spread. Recorded per answered and
  missing check.
- **Evaluation plan**: planned requests per tier, units reached, unreachable units, checks required
  and unplanned, provisional flag. Bound to the same manifest as the ledger.
- **Previous-report reference**: digest of an accepted previous report whose validated answers were
  skipped.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For synthetic notes of about 1,000, 6,000 and 12,000 words, with and without priorities,
  the plan's requests, units reached and checks per tier equal those of a run answered validly by a
  fake transport, with no difference.
- **SC-002**: In a synthetic ~1,000-word note with candidate edits in its last unit and two host-named
  spans, a run with a budget of 8 sends every candidate check and every host-named check before it
  opens any request for tier 3 or tier 4.
- **SC-003**: In a synthetic note where only some units contain a pattern's local signal, and no
  higher tier exists, every check of that pattern in those units is sent before any request is
  opened for tier 4.
- **SC-004**: Without priorities, one run with the full request limit over the ~1,000-word synthetic
  note gives validated answers in at least 30 units, compared with 9 today.
- **SC-005**: Two chained runs on the same synthetic note send no check twice, and the second report
  counts only its own answers. When one unit is edited between the runs, that unit's checks are
  planned again and no unchanged unit's answered check is. Without focus or candidates, the second
  run's tier 4 requests go to units the first run did not reach before any unit it reached.
- **SC-006**: With one invalid reply injected at request 2 of a 32-request run, at least 30 further
  requests are sent, and only that batch's checks carry `invalid_response`. With invalid replies at
  requests 2, 5 and 9, no request after the ninth is sent.
- **SC-007**: Every existing test of the per-request and per-invocation limits passes unchanged, and
  no plan or report field added by this feature contains source prose.
- **SC-008**: A reader of the advisor reference can state the meaning of exit codes 0 and 2, how to
  set a budget and priorities, and what to report for a partial run, without reading the runner's
  code.

## Assumptions

- The per-invocation limits stay as accepted in feature 008; this feature changes how the budget is
  chosen and reported, not its size.
- Continuing after an invalid reply replaces the stop-at-first-invalid contract tested in
  `tests/test_coverage_faults.py`; that test changes with this feature. A run is never retried and a
  failed batch is never resent, so feature 008's no-retry rule still holds.
- The priority order is an owner decision, not a measured optimum. It is deterministic and testable;
  its effect on how many real errors are found per request needs a labeled corpus that does not
  exist yet.
- Asking the service to rank units is out of scope: each ranking request carries one unit, so it
  spends the same scarce requests.
- Local signals order work and never exclude it, so they do not change rule application and are not
  rule maintenance. Structural exclusions for headings, table cells and label–value lines, and a T4
  gate that removes checks, remain rule maintenance and out of scope.
- The existing `--scope selected` diagnostic is unchanged. Host-named spans in this feature are a
  priority inside a full-scope run, so everything not answered stays listed as missing.
- A fake transport that always answers validly is a sound oracle for plans and request counts,
  because selection and batching are deterministic given the prepared document, registry and
  priority input. It says nothing about how the service answers.
- The 0.025 score-consistency tolerance that produced the observed `invalid_response` is out of
  scope; whether it matches the service's Score semantics needs checking against the TypeSafe
  documentation first.
- Also out of scope: the `ambiguous_url_closer` rule, and the CLI reporting an unreadable input file
  as `invalid_input`.
- No live service run is needed to accept this feature; any live run needs the owner's spend
  approval and uses synthetic text only.
- No real user text is committed.
