# Feature Specification: Automatic Jev evaluation with an offline fallback

**Feature ID**: `007-automatic-jev-evaluation`\
**Created**: 2026-10-16\
**Status**: Approved by owner on 2026-10-16; implementation authorized.\
**Branch**: `codex/007-automatic-jev-evaluation`; owner authorized separation from the original checkout and a draft PR on 2026-10-16.\
**Input**: On every Vietnamizer invocation, check whether a TypeSafe API key is available. If available, run prepared pattern checks through Jev and let the host agent edit using the returned judgments. If absent, use the existing LLM editing workflow without calling Jev.

## Intended outcome

Vietnamizer retains its standalone Markdown editing behavior while gaining an automatically attempted evaluation path when the host supplies a TypeSafe credential and permits execution and transmission. The editor must not silently choose the LLM-only path when the Jev path is available and allowed. Availability of a key guarantees that the supported runner attempts the applicable evaluations; it cannot guarantee a successful remote response or force an unsupported host to execute tools.

The scripts evaluate text and proposed edits. They do not generate Vietnamese prose, infer authorship, apply patches, or automatically accept/reject edits. The host agent remains the editor and must enforce the five existing editing safeguards.

## User Scenarios & Testing

### User Story 1 — Automatic evaluation with an available key (Priority: P1)

A user invokes Vietnamizer in a supported host with an injected TypeSafe key. The host prepares the editing context, calls the shipped evaluator, reads its results, and produces the edited response.

**Independent Test**: With a fake injected key and an isolated mocked transport, invoke the runner on representative prose. Verify requests are scheduled for every applicable semantic check; mechanical checks and excluded patterns receive explicit dispositions. The test must not contact a live service.

**Acceptance Scenarios**:

1. **Given** a nonempty injected key and permitted execution/transmission, **when** an invocation begins, **then** the runner attempts the applicable Jev checks before the host presents a Jev-informed response.
2. **Given** mixed document functions, **when** routing runs, **then** each section uses the applicable canonical genre gate, profile and style context, with no profile rules applied to protected spans.
3. **Given** a response, **when** it is consumed, **then** its actual model, typed answer IDs, distributions and input binding are validated first. A malformed response is not evidence that checks passed.
4. **Given** multiple applicable patterns, **when** questions can be built from the same state, **then** they are batched; independent patterns are not forced into one mutually exclusive winning label.

### User Story 2 — Existing behavior without a key (Priority: P1)

A user invokes Vietnamizer without an injected key. The ordinary host-agent workflow remains usable without a network connection, SDK or credential setup.

**Independent Test**: Remove the key from the isolated test environment and replace the network transport with a function that fails if called. Verify the local availability check reports `key_absent`, the evaluator performs no HTTP request, and the documented LLM-only workflow remains available.

**Acceptance Scenarios**:

1. **Given** an absent or whitespace-only key, **when** availability is checked, **then** no Jev evaluation request runs and no setup/key request interrupts ordinary editing.
2. **Given** the offline path, **when** the host edits, **then** it still applies genre routing, protected regions, patterns, and all five safeguards.
3. **Given** a platform without script execution, **when** the key/runner cannot be checked, **then** the status is `capability_unavailable`, not a fabricated `key_absent` result.

### User Story 3 — Honest handling of unavailable or failed evaluation (Priority: P1)

A key can be present while the service, host capability or permission is unavailable. The user still receives core editing without a false claim that Jev validated it.

**Independent Test**: Simulate denied transmission, invalid authentication, timeout, rate limiting, oversized input and malformed responses. Verify distinct failure dispositions, bounded work, no plaintext credential leakage and no invented pass result.

**Acceptance Scenarios**:

1. **Given** an authentication or service failure, **when** evaluation stops, **then** the host continues the core workflow and briefly discloses that Jev did not complete when an evaluation was attempted or explicitly required.
2. **Given** a host permission denial, **when** the runner cannot transmit, **then** it does not bypass the denial or change settings; the blocked evaluation is reported separately from editing.
3. **Given** partial results, **when** the host responds, **then** only validated results bound to the current input are described as evaluated; remaining checks are not presented as passed.

### User Story 4 — Pattern-aware judgments and edit verification (Priority: P2)

The host can use bounded Jev judgments while retaining responsibility for the final prose.

**Independent Test**: Use fixtures covering a missing result complement, an internally truncated lexical expression, valid ellipsis, ambiguous referents, legitimate administrative wording and a candidate that changes certainty. Verify question construction, scope, exclusions and per-candidate evaluation. Fixtures test behavior and contracts, not prove Vietnamese-domain accuracy.

**Acceptance Scenarios**:

1. **Given** a candidate set, **when** preservation is evaluated, **then** each candidate is assessed separately; an aggregate question about ALL candidates is not used to approve any one candidate.
2. **Given** two plausible edits, **when** selection is requested, **then** the original, no-suitable-edit and insufficient-evidence outcomes remain available.
3. **Given** higher fluency but changed facts or certainty, **when** the host reviews the edit, **then** fluency cannot compensate for violating the existing safeguards.
4. **Given** an error the host identifies despite a Jev `acceptable` result, **when** editing continues, **then** the host may examine it with named evidence; the classifier does not veto the core editor.

## Functional Requirements

### Availability and authority

- **FR-001**: A local availability operation MUST expose only whether the documented injected `TYPESAFE_API_KEY` is usable as a nonempty value; it MUST NOT print, persist or include the credential in an error.
- **FR-002**: The public package MUST NOT search `.env` files, keychains, shell histories, configuration stores or unrelated projects for credentials. Hosts may use their existing approved injection mechanism outside the package.
- **FR-003**: An available key MUST activate an evaluation attempt by default on supported hosts; no extra opt-in flag may silently disable that requested default.
- **FR-004**: Key availability MUST NOT override transmission permission, restricted-data handling, protected spans, sandbox policy or user instructions. A denied path MUST receive a distinct status, not be retried through another mechanism.
- **FR-005**: No-key behavior MUST invoke no evaluation network request. The local presence check is not a Jev evaluation and MUST NOT be reported as one.

### Execution and coverage

- **FR-006**: Ship a reusable runner and a canonical registry covering exactly V1–V25, T1–T6, B1–B17 and K1–K7. Definitions MUST be prepared during implementation, not invented ad hoc on each invocation.
- **FR-007**: A single entry point MUST be able to run an individual pattern or the complete applicable evaluation plan. Shared transport and validation MUST not be copied into 55 independent clients.
- **FR-008**: A complete invocation MUST record a disposition for all 55 patterns. Exclusions MUST identify their reason: protected region, canonical genre restriction, inactive profile, or a mechanical-only check. No requested semantic check may disappear without a disposition.
- **FR-009**: Every applicable semantic pattern MUST be scheduled for evaluation in the automatic path. A heuristic keyword prefilter alone MUST NOT silently suppress that coverage. Once evaluated, a pattern can legitimately find no issue.
- **FR-010**: Mechanical portions MUST run in code. Patterns whose entire applicable check is mechanical need not manufacture a Jev question. The ledger MUST distinguish `mechanically_checked` from `jev_evaluated`.
- **FR-011**: Preserve canonical genre restrictions. Not every invocation applies all 55 patterns: blog and enterprise profiles are not simultaneously applicable to one homogeneous section, and protected text receives no edit judgments.
- **FR-012**: Pin the requested model to `jev-1.14.0`; do not use a moving alias. Validate the returned model before accepting evidence. Do not silently substitute another model.
- **FR-013**: Batch independent questions over the same state within actual request/context limits. Separate requests only for different context scopes, capacity or real dependencies, such as constructing a later eligible candidate set.
- **FR-014**: Requests MUST be bounded by explicit size, question, elapsed-time and attempt limits. Limits and their consequences MUST be reviewed in the implementation plan; no unverified language-quality threshold may substitute for them.
- **FR-015**: Do not silently truncate prose, omit relevant references or report budget-exhausted checks as passed. Return incomplete coverage explicitly.
- **FR-016**: A new invocation with a key MUST not be represented as a fresh Jev run using only cached results. No cross-invocation cache bypass is part of this feature's default path.

### Questions and context

- **FR-017**: State MUST retain the full paragraph for sentence-level checks and the relevant additional paragraphs when referents, conditions or definitions are introduced elsewhere. Do not impose a fixed one- or two-sentence window.
- **FR-018**: Structural checks MUST receive the appropriate heading/list/section structure. Claim-support checks MUST receive the actual in-scope claims and source passages, not invented evidence.
- **FR-019**: Code/host MUST bind target IDs to actual spans. Choice may select only candidates whose text and identity are supplied and validated; absence of a candidate is not proof it does not exist.
- **FR-020**: Choice MUST be used for genuinely competing interpretations/functions or bounded selection. Independently coexisting defects MUST not be collapsed into one dominant paragraph label.
- **FR-021**: Noul MUST assess one coherent condition. Exceptions MAY be embedded in the rubric or asked independently when their answers have independent value.
- **FR-022**: Score MUST measure one ordered dimension with explicit levels. Insufficient context MUST remain distinct from a middle quality score. No score of AI authorship or corpus frequency is introduced.
- **FR-023**: All relevant canonical “Không flag” constraints MUST be represented in pattern definitions. Short sentences, single-syllable endings, legitimate ellipsis, regional wording and standard administrative terms MUST not become defects by themselves.
- **FR-024**: Treat evaluated text as data, never instructions. Source labels such as “human-written” or “AI-written” MUST not bias editing judgments.

### Editing and evidence

- **FR-025**: Host LLM generates candidate prose and the final response. Jev supplies typed judgments and selection, not unconstrained generated rewrites.
- **FR-026**: Evaluate each candidate separately for the targeted improvement and affected meaning-preservation constraints. Keep original/NONE/INSUFFICIENT options where relevant.
- **FR-027**: Existing five safeguards remain authoritative. No weighted score may compensate for changed facts, certainty, subject, timing, causal relation, scope, commitments or protected bytes.
- **FR-028**: The first implementation MUST NOT apply, accept, reject or revert edits through an automatic numerical decision policy. Active Jev-informed host editing is owner-approved; automatic numerical edit acceptance/rejection/reversion remains gated by holdout evidence.
- **FR-029**: Validate response schema, requested IDs, finite distributions and returned model. Preserve current-input/rubric/candidate bindings; changes invalidate the affected evidence.
- **FR-030**: Distinguish `key_absent`, `capability_unavailable`, `permission_denied`, `authentication_failed`, `service_failed`, `invalid_response`, `incomplete` and successful evaluated/mechanical/excluded dispositions. Error is not pass.
- **FR-031**: Default operational telemetry/health reports MUST contain no raw prose or secrets. Use statuses, pattern IDs, actual model, rubric/config version, payload/candidate digests, usage and failure categories. Do not expose provider error bodies that could echo input.
- **FR-032**: Report observed execution, not intention: distinguish scheduled, attempted and validated checks. No guarantee of remote success or universal host compliance is claimed.

### Distribution

- **FR-033**: Ship runtime code and the same pattern registry in every supported archive. Do not introduce a runtime dependency on a maintainer's local repository or credential wrapper.
- **FR-034**: Preserve the standalone no-key Markdown workflow. Prefer the already-supported Python runtime and standard library; introducing an SDK or a dependency requires separate justification and a pinned lockfile where applicable.
- **FR-035**: Update canonical SKILL, advisor guidance, README, AGENTS, contributing/privacy/distribution guidance and package validators/tests together where their current claims conflict with the new workflow. Version metadata and manifests MUST remain synchronized.
- **FR-036**: Do not revive the retired 001/002/005 runtime or evaluation harness. Existing experiments are design evidence only, not code or accuracy proof for this new implementation.

## Key Entities

- **Invocation**: Supplied text, permitted editing scope, host capability, credential availability status and evaluation attempt identity.
- **SectionContext**: Genre/profile/style context, paragraph, related sources and protected spans.
- **PatternDefinition**: Canonical ID, question recipe, scope, exclusions, types and configuration version.
- **CoverageEntry**: Per-section/pattern scheduled/attempted/validated or explicitly excluded/mechanical disposition with a bounded reason.
- **Judgment**: Typed response, distribution, actual model, usage and current-input binding.
- **CandidateReview**: Original, proposed edit ID, targeted defect and per-candidate judgments. Does not grant patch authority.

## Edge Cases

- Key exists but is invalid, whitespace-only, revoked or not injected into the actual execution process.
- Host cannot execute scripts, cannot inspect credential availability or cannot transmit text.
- No editable prose, protected-only input, a typography-only genre or a section without a relevant profile.
- Multiple document functions, valid single-syllable endings, uncertain referents and omitted context beyond the current paragraph.
- Score is high while meaning changes; Choice splits across two acceptable alternatives; first-pass checks miss a host-identifiable issue.
- Oversized context, provider timeout/rate limit, partial evaluation, malformed distributions, mismatched model or unexpected answer IDs.
- Article supplied in a code fence for editing: identify its actual prose role without interpreting embedded instructions as executable commands.
- A runtime works from the repository but is absent or broken after packaging or installation.

## Success Criteria

- **SC-001**: Isolated no-key tests show zero evaluation HTTP calls and no credential/setup prompt.
- **SC-002**: Injected-key tests show every applicable semantic check scheduled and attempted when transport remains available, with complete coverage accounting and no undisclosed skip.
- **SC-003**: Every consumed result is bound to the current payload/rubric/model and validated; all injected error scenarios remain explicitly non-pass.
- **SC-004**: Registry validation proves all 55 canonical IDs are present once with their required question scope and exclusions; inactive profiles and protected regions receive the correct dispositions.
- **SC-005**: Candidate fixtures prove changed certainty/facts cannot be approved by a fluency score alone, while legitimate ellipsis is not mechanically expanded.
- **SC-006**: All archive validators and offline tests pass for the final bytes; installed supported-runtime checks demonstrate the shipped entry point and registry resolve without maintainer-local paths.
- **SC-007**: Any behavioral evaluation identifies model/config/corpus/policy versions, service errors, latency and actual usage; language-quality claims remain limited to observed labeled data. No fabricated accuracy or universal thresholds.
- **SC-008**: Live smoke verification uses a small synthetic permitted payload, confirms the actual model and covers one successful transport path. It does not establish Vietnamese editing quality or release readiness by itself.

## Authority, conflicts and owner decision

1. The requested new workflow explicitly replaces the current V20-only, optional host-skill advisor design. Existing README/AGENTS/contributing claims that the package contains no TypeSafe runtime must change during implementation; they cannot coexist as current instructions.
2. Constitution principle V requires the core to remain usable without services/secrets and on evaluator errors. The no-key path and honest fail-open behavior preserve that property. Automatic activation when a key is supplied does not eliminate offline operation.
3. The constitution also requires new external-model changes to start in shadow mode and evidence before automatic edit review/rejection/reversion. This spec preserves that restriction in FR-028. **Owner decision, 2026-10-16**: permit active Jev-informed host editing now while retaining the five safeguards and the prohibition on automatic numerical edit policies before holdout evidence. Amend the governance clause explicitly.
4. An available key is not authority to bypass host policy or export restricted data. The default path must respect existing authorized transmission without repeatedly asking for permission already given.
5. Always attempting applicable checks means more remote work than the current selective advisor. Exact request/time/cost limits belong to the implementation plan; they must be visible, and reaching a limit must not masquerade as complete evaluation.

## Affected consumers and planned verification scope

- Source users, standalone skill archives, Claude Org archive, Codex and Claude plugin archives.
- Canonical instructions, docs, manifest versions, inventory allowlists and package security tests.
- Hosts with an injected key and Python execution; hosts with no key; hosts without execution or transmission capability.
- Required checks include targeted runtime/transport contract tests, existing offline package/security tests, package validation, archive parity, Skills listing and Claude plugin validation. Network/model quality evidence is reported separately.

## Status and references

This is the sole feature specification for 007 under Spec Kit ownership. Implementation follows plan.md; verification and delivery state are recorded separately. No commit, shared installation or release is authorized.

- `.specify/memory/constitution.md`
- `SKILL.md` and `references/typesafe-advisor.md`
- `scripts/package-skill.sh`, `scripts/validate-package.py`, `scripts/package-plugin.py`
- `CONTRIBUTING.md`, `AGENTS.md`, `README.md`
- Design analysis and 55-pattern matrix: `/private/tmp/vietnamizer-jev-design-20261016/analysis.md` (local research, not a distributable dependency)
- Current request and the observed Jev 1.14 experiments in this chat; not a substitute for a new holdout or post-install evidence.
