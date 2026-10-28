# Feature Specification: Editorial Benchmark and README Evidence

**Reporting-stage decision2026-10-26:** owner defers human grading. Deliver an offline
descriptive execution report with scientific charts from existing outputs only;
quality remains unassessed. Preserve Forms and all raw, no generation or grading calls.

**Current scope — owner correction2026-10-26:** within-agent original/edited comparison;
no cross-agent ranking or pooled runtime labels. Codex80/80 and Gemini80/80 already
exist; use them without new inference or changes to the two live Codex Forms.
See [within-agent-amendment.md](within-agent-amendment.md); earlier run/recovery
sections below remain historical evidence, not instructions to restart generation.

**Feature Directory**: `specs/014-editorial-benchmark`
**Created**: 2026-10-25
**Status**: Operational recovery complete: 20/20 new Codex+Jev finals and 80 canonical comparison outputs. All required Jev answers received; native context/scope complete for 3/20 cases. Owner authorized exploratory model grading and convenient human reviewer handoff on 2026-10-25. Model grading accounted for all 42 starts: 156/160 valid output reviews, four missing after one serialization failure, under quality-protocol.md and quality-enum-amendment.md; human labels and independent holdout remain pending.
**Input**: Fio wants clear benchmarks, tests and proof in README to encourage adoption,
using Hindsight as a presentation reference. Fio selected a same-model comparison:
no skill / ordinary editing prompt / Vietnamizer / Vietnamizer + Jev.
The fourth-arm amendment is defined in [jev-extension.md](jev-extension.md); it does not
retroactively change the frozen three-arm run. The owner separately authorized the USD 2
Jev ceiling; recovery usage and reserves remain below that ceiling.

## User Scenarios & Testing

### User Story 1 - Assess whether Vietnamizer earns its overhead (Priority: P1)

A prospective user compares editorial outcomes for the same source and model with and
without Vietnamizer, including cases where leaving the source unchanged is correct.

**Why this priority**: Adoption depends on better writing with fewer damaging changes,
not the number of patterns or passing infrastructure tests.

**Independent Test**: A report on a frozen, independently labeled set accounts for all arms,
metric numerators and denominators, uncertainty and failures.

**Acceptance Scenarios**:

1. **Given** identical source, context, model and generation settings, **When** the four arms
   are evaluated, **Then** comparison claims apply only within that controlled setup.
2. **Given** fluent output that changes a fact, commitment or causal relation, **When** assessed,
   **Then** the meaning violation is reported separately and cannot be canceled by preference.
3. **Given** appropriate source text, **When** an arm introduces an unjustified change,
   **Then** the unnecessary-edit metric counts it.
4. **Given** missing, invalid or timed-out output, **When** aggregated, **Then** it remains
   an explicitly failed/missing attempt rather than disappearing or becoming a pass.

### User Story 2 - Inspect and reproduce the evidence (Priority: P2)

A contributor inspects permitted sources, labels, prompts, outputs and scoring rules,
then reproduces the deterministic report without buying inference.

**Why this priority**: A headline percentage needs an inspectable denominator.

**Independent Test**: Recomputing the report from the same evidence yields identical counts,
rates and claim eligibility; changed sources or labels invalidate the old binding.

**Acceptance Scenarios**:

1. **Given** a released evidence bundle, **When** recomputed, **Then** every headline number
   traces to versioned cases, attempts and reviews.
2. **Given** a development example or its paraphrase, **When** assembling the holdout,
   **Then** it is excluded from independent claims and remains a disclosed regression case.
3. **Given** reviewer disagreement, **When** reporting, **Then** original judgments,
   adjudication and unresolved cases stay distinguishable.

### User Story 3 - Read a short, honest README proof section (Priority: P3)

A reader sees what is established, for which model and genres, before installing, with
links to the complete protocol, evidence and limitations.

**Independent Test**: Every numerical quality claim resolves to a matching report; absent
results are explicitly pending and never replaced with illustrative scores.

**Acceptance Scenarios**:

1. **Given** only runtime tests and calibration examples, **When** README is read,
   **Then** neither is presented as a controlled measurement of editorial improvement.
2. **Given** a valid result, **When** summarized, **Then** README names model, skill version,
   evaluation-set version, date, sample size, comparator, metric and material limitations.
3. **Given** changed skill/model bytes, **When** viewing earlier evidence, **Then** its tested
   revision stays visible and is not silently relabeled as current validation.

### Edge Cases

- A legitimate alternative differs from the reference rewrite; regional language is intentional.
- A document mixes prose, code, quotations, tables and typography-only genres.
- Missing social context makes changing pronouns unjustifiable.
- Related excerpts from one author/document leak across development and holdout sets.
- All outputs are unchanged, comparisons tie, or a metric has no eligible cases.
- One arm fails more often or exhausts its tool budget.
- Jev availability differs across attempts or the evaluator also participates in generation.
- Publicly readable source text has no permission for redistribution.

## Requirements

### Functional Requirements

- **FR-001**: Compare a pinned model and host in four arms: the common editing request alone;
  that request plus an ordinary editing prompt; that request plus Vietnamizer; and Vietnamizer
  with actual Jev advice. All arms
  receive identical source, audience, purpose and supplied voice sample. The ordinary prompt
  MUST be credible, fixed before holdout use, and include meaning/voice preservation. Record
  all loaded instructions, profiles and tools; do not weaken the baseline to manufacture a win.
- **FR-002**: The standalone arms MUST keep Jev disabled through supported configuration.
  The fourth arm MUST record actual Jev calls, coverage, latency and cost, including failures.
  A claim about Jev's incremental contribution MUST compare matched host revision passes
  from the same initial draft. An extra revision pass alone MUST NOT be attributed to Jev.
  Lack of Jev is not core failure. Jev advice MUST NOT automatically apply or block edits
  based on a numeric score.
- **FR-003**: Each run MUST bind model/version, host version, generation settings, instruction
  context, skill revision/digest, prompt version, corpus version, evaluation-config version,
  date, repeat policy and capabilities. Judgment-only records MUST carry `policy_version=null`;
  records applying a policy MUST name that version.
- **FR-004**: Cases MUST cover all seven style families, valid no-edit text, terminology,
  regional variants, context dependencies, factual commitments, protected spans and
  typography-only genres. Record source and redistribution permission; report synthetic
  and naturally occurring cases separately.
- **FR-005**: Calibration examples MAY be development/regression cases. Independent quality
  claims MUST use a frozen holdout not used to tune rules, prompts, rubrics or policy. Split
  by source document/author group and inspect semantic near-duplicates. Retuning after
  seeing holdout results requires a new holdout.
- **FR-006**: Labels MUST describe required fixes, acceptable alternatives, invariants and
  reasons. Equality with one reference string MUST NOT define quality. Explicitly check
  facts, pronouns, modality, chronology, causality and protected spans.
- **FR-007**: Two Vietnamese-proficient reviewers MUST independently assess blinded,
  randomized outputs against source and rubric. Preserve agreement, adjudication and
  unresolved cases. The generating agent and any evaluator used by Vietnamizer MUST NOT
  be the sole ground truth.
- **FR-008**: Reports MUST show correction precision (justified successful edits / all edits),
  required-fix recall (resolved labeled issues / all required issues), clean-case unnecessary
  edit rate (clean cases unnecessarily changed / all clean cases), document-level meaning
  and voice violation rates, and blinded pairwise wins/ties/losses against each baseline.
  Define edit alignment and multi-issue counting before measurement.
- **FR-009**: Report raw counts, denominators, per-genre outcomes, paired uncertainty for arm
  differences, sample/repeat counts and reviewer agreement. Account for source-group
  dependence; repeated generations are not independent documents. Zero denominators
  are undefined, not 100% success. Pilot size does not establish statistical sufficiency.
- **FR-010**: Report failures, missing judgments, human-review rate, wall time and cost,
  including failed attempts, skill tokens, tools and optional Jev calls. Separate inference
  cost and reviewer effort. Unknown cost is not zero. When evaluating an edit guard, also
  report harmful-edit recall and valid-edit false-block rate per the constitution; these
  guard metrics are N/A for core-only generation.
- **FR-011**: Aggregation MUST work offline from recorded evidence. Duplicate, orphaned,
  mismatched or incomplete records MUST block a complete publishable report; partial
  diagnostics MUST carry incomplete status and missingness counts.
- **FR-012**: README MUST separate technical tests, calibration and controlled editorial
  outcomes. Quality claims MUST link to inspectable reports/evidence. Selected examples
  MUST be labeled with a selection rule; the full report MUST also include failures.
  Unsupported rankings and superiority claims are forbidden.
- **FR-013**: The experiment MUST allow no detectable improvement, mixed results or regression.
  Infrastructure acceptance MUST NOT require Vietnamizer to win. Freeze metrics and claim
  eligibility rules before holdout use.
- **FR-014**: Preserve standalone operation and the current runner; do not restore retired
  features 001/002/005, activate a production edit policy, install tooling, change shared
  settings or release as a side effect. Live generation requires a named authorized runtime,
  model and spend cap. Publication is a separate action.

### Key Entities

- **Case**: source, genre, audience/purpose/context, permitted origin, source group, split,
  expected issues, acceptable alternatives and invariants.
- **Run**: frozen configuration and artifact identities shared by arms.
- **Attempt**: case/arm/repeat identity, output/failure, elapsed time, usage and cost.
- **Review**: blinded assessment, issue/edit alignment, violations, preference and adjudication.
- **Report**: denominators, stratified metrics, uncertainty, evidence and claim eligibility.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every published headline number traces to cases, attempts and assessments and
  can be recomputed offline without a model call.
- **SC-002**: All three arms use identical source/context and a pinned model; every planned
  attempt is accounted for as completed, failed or missing.
- **SC-003**: Every required category has cases; every holdout case has two independent reviews
  or an explicit unresolved status that blocks a complete quality claim.
- **SC-004**: Reports separate corrections, omissions, unnecessary edits, meaning/voice
  violations, preference, review burden and overhead. No combined score conceals harm.
- **SC-005**: README has no unsupported percentage, rank or victory claim; evidence stays
  attributed to tested versions and samples, including negative results.

## Assumptions

- This is a new editorial benchmark, not a continuation of retired guard research.
- The owner confirmed the three comparison arms. Competitor skills and cross-model rankings
  are outside the first slice.
- Full-document editing is the adoption outcome; isolated pattern tests remain diagnostic.
- Corpus size and repeats will be chosen during planning from pilot variability and review
  capacity; an arbitrary count is not a claim of representativeness.
- Owner requested Codex and Antigravity first, with Claude deferred until its usage limit
  clears. Proposed models, pilot/holdout sizes, quota limits and reviewer effort are recorded
  in [runtime-proposal.md](runtime-proposal.md); they remain proposals, not approved settings
  or spend. Reviewer availability and redistributable sources are still prerequisites.

## Owner amendment: direct human A/B Forms (2026-10-25)

Fio approved replacing the source-only human collection step with original/edited side-by-side
comparisons and three understandable questions per document, retaining blind four-arm
assignment and existing A/B responder URLs. Both forms had zero responses at preflight.
The current human contract is [human-simple-protocol.md](human-simple-protocol.md), delivered
through [human-handoff.md](human-handoff.md). The earlier source-inventory/lock contract remains
historical for human-v1 and unchanged for completed model-v1 grading. No equivalence of
metrics is claimed between schemas; no human quality result exists until real responses arrive.

## Owner amendment: Facebook real-world sources (2026-10-25)

Fio requested sourcing real posts from Facebook group3262256010653927, retaining source
provenance, generating benchmark edits including Vietnamizer and Vietnamizer+Jev, and producing
new blinded human-rating Forms. The synthetic development corpus remains historical; it does
not establish effectiveness on naturally occurring AI writing. See realworld-protocol.md.

Every admitted source must bind full post/declared contiguous excerpt, verified permalink,
capture time, sampling record and immutable hash before editing. Authorship provenance remains
unknown without text-specific disclosure or verifiable model-output evidence. Style judgments
or a media AI label must not become a validated AI-authorship probability. Report disclosed
AI-assisted and unknown-origin posts separately. Retain failures, unchanged outputs and
uncertainty. No post-outcome source selection, fabricated missing sources or overwritten pilot
forms/responses. Current collection blocked by browser origin auto-review even after explicit
owner confirmation for group-only reads;0sources frozen,0new outputs,0new Forms.

## Owner amendment: public AI-authored sources (2026-10-25)

Owner abandoned Facebook and authorized finding other public sources with text-specific
AI-generation evidence, retaining complete provenance, running the matched benchmark and
creating new Google Forms. Resume T037–T041 with public dataset intake; the Facebook origin
denial remains historical and is not bypassed. No old corpus/outputs/forms are overwritten.

### Owner amendment — 2026-10-26

Remove both reviewer-background questions (editing experience and project/conflict
relationship) from live public A/B Forms. Keep existing responder URLs, all20groups,
source/output images, blind assignments and three evaluation questions per group.
Preserve submitted responses before mutation; retain original frozen research archive.
No respondent background metadata is required for this pilot.

### Pre-survey completion — owner authorized2026-10-26

Complete all independent readiness work while waiting for both human reviewers. Add a
read-only Forms export and immutable import/analysis path for the current public cohort
and no-background UI. Bind form/item IDs, original assignments, response identities,
raw hashes and analysis protocol. Require coordinator response selection before
unblinding; never silently choose a favorable/latest submission. Preserve missing and
uncertain labels. Implement preregistered paired clustered estimates and scientific
figures; no real quality chart or superiority claim before actual selected ratings.
Archive prior evidence unchanged, clarify historical gates and provide an actionable
runbook. No new model calls, participant messages, publishing/merge or unsafe Gemini
runtime retries are needed for this phase.


## Owner correction — 2026-10-26: within-agent before/after

The primary research question is: for the same original and fixed editing agent/model,
is the result after Vietnamizer easier to read while preserving meaning, figures and
voice? Original means the frozen public AI source, not an output from the bare arm.
Existing bare/ordinary controls support secondary skill-attribution checks.
Codex and Gemini are separate replications; never rank agents or pool their labels.
Current Forms remain Codex-only and unchanged. Use existing outputs only.
Acceptance: original-relative rates/counts and source-cluster CIs; unknown/missing
explicit; preservation separate; secondary contrasts labelled; versioned offline
workspace retaining form/item/mapping identity; updated README without quality claims.
This amendment changes the previous primary comparator transparently; no selected
human labels have been read in this change and no new inference is authorized.
