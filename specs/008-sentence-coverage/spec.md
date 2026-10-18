# Feature Specification: Automatic paragraph and sentence coverage

**Feature Branch**: `codex/008-sentence-coverage`

**Created**: 2026-10-16

**Status**: Approved by owner on 2026-10-16. Plan/tasks approved; local implementation verified on 2026-10-16; not integrated or released.

**Input**: Automatically divide supplied writing into paragraphs and individual sentences, check coverage so no sentence silently disappears, and evaluate each sentence with its full parent paragraph and relevant context in state. Create the Spec Kit specification before changing code.

## User Scenarios & Testing

### User Story 1 — Check every sentence without hand-prepared targets (Priority: P1)

A user supplies a Vietnamese article. The workflow identifies its paragraphs and sentences automatically and evaluates every eligible sentence without requiring manually enumerated targets.

**Why this priority**: v0.10.0 accepts prepared sections and optional targets; absent targets mean paragraph-level targeting. Having 55 pattern definitions does not establish sentence coverage.

**Independent Test**: Compare automatic preparation and recorded checks with an independently annotated article using controlled evaluator responses, without transmitting real user text.

**Acceptance Scenarios**:

1. **Given** several paragraphs containing multiple sentences, **when** automatic preparation runs, **then** every sentence receives a distinct source-bound identity, exact span and parent paragraph, and every applicable sentence-pattern check has a recorded disposition.
2. **Given** more sentences than one batch supports, **when** evaluation runs, **then** late sentences remain accounted for across bounded batches, with the complete parent paragraph preserved.
3. **Given** abbreviations, decimals, dates, URLs and nested quotations, **when** segmentation runs, **then** reference sentence boundaries are retained without lost or duplicated text.
4. **Given** a final sentence without terminal punctuation, **when** preparation finishes, **then** it is represented rather than dropped.

### User Story 2 — Interpret each sentence in context (Priority: P1)

Each sentence is judged with its complete parent paragraph and the supplied supporting paragraphs needed to understand references, conditions and contrasts.

**Why this priority**: Isolated sentences can turn legitimate ellipsis or a single-syllable ending into a false missing-complement finding.

**Independent Test**: Use pairs containing the same sentence in different paragraphs and a nonadjacent reference. Inspect actual prepared inputs for exact context binding. Test preparation separately from semantic judgment quality.

**Acceptance Scenarios**:

1. **Given** the same sentence in different paragraphs, **when** each is checked, **then** its result is bound to its own complete paragraph and context; results cannot be reused solely because target wording matches.
2. **Given** a nonadjacent definition or antecedent supplied as related context, **when** the target is checked, **then** the complete supporting paragraph accompanies it, rather than a sentence fragment or generated summary.
3. **Given** an unresolved reference, **when** necessary context cannot be supplied, **then** affected work is context-insufficient, not certified complete.
4. **Given** required context exceeding a limit, **when** it cannot fit, **then** affected work remains incomplete; context is not silently truncated.

### User Story 3 — Know exactly what was checked (Priority: P1)

The host and user can distinguish completed sentence checks, explicit exclusions, insufficient context and uncompleted work due to service or execution limits.

**Why this priority**: Attempted requests and successful subsets must not be presented as complete article evaluation.

**Independent Test**: Reconcile expected work against successful, missing, duplicate, invalid, stale, timed-out and budget-exhausted responses.

**Acceptance Scenarios**:

1. **Given** all required checks have validated results, **when** reconciliation finishes, **then** every eligible sentence is complete and exclusions are separately listed.
2. **Given** one missing answer or unprocessed final sentence, **when** other checks succeed, **then** the affected sentence and overall evaluation remain incomplete, identifying the missing work.
3. **Given** no key, denied transmission or service failure, **when** offline editing continues, **then** offline completion does not count as Jev evaluation.
4. **Given** a paragraph-scoped result, **when** coverage is reconciled, **then** it cannot satisfy outstanding sentence-scoped work; paragraph checks also need not be repeated per sentence.

### User Story 4 — Preserve structure, protections and existing inputs (Priority: P2)

Mixed headings, lists, quotations and protected material remain source-faithful and explicitly accounted for. Existing prepared input remains usable.

**Why this priority**: Automatic splitting must not expand editing or transmission authority.

**Independent Test**: Compare mixed-structure fixtures, protected spans and existing explicit-target inputs against source reconstruction, redacted requests and expected coverage.

**Acceptance Scenarios**:

1. **Given** headings, multiline lists, tables and code, **when** preparation runs, **then** structural roles remain identifiable; editable list prose is covered and protected/code units are explicitly excluded.
2. **Given** partial protection within a sentence, **when** evaluated, **then** protection applies to the target, parent paragraph, related context and proposed edits; wholly protected sentences are accounted for as excluded.
3. **Given** explicit targets covering only some sentences, **when** full evaluation runs, **then** omissions are filled or explicitly unresolved; it cannot silently become a selected-sentences-only diagnostic.

### Edge Cases

- Empty or whitespace-only input; mixed line endings; repeated blank lines; soft-wrapped paragraphs.
- Ellipsis, fragments, `?!`, closing brackets/quotes, initials, abbreviations, decimals, dates, URLs, emoji and combining Vietnamese characters.
- Identical sentences at different source locations; quoted multi-sentence speech; multiline list items and punctuation-free headings.
- Partial protection, repeated sensitive text in context and edits shifting later source positions.
- Inputs exceeding current 16-target or 32-section limits; question, request-size, request-count and deadline limits. Budget increases are not assumed.
- Ambiguous sentence boundaries: preserve the complete unresolved source region and flag uncertainty; do not certify exact segmentation.
- Missing, duplicate, overlapping or stale explicit targets and evaluator answers.
- Unresolved nonlocal references, absent source passages and source text containing instructions.

## Requirements

### Functional Requirements

- **FR-001**: Full evaluation MUST automatically identify paragraphs, structural units and individual sentences from supplied writing without manual targets. Host genre, audience, purpose and protection decisions remain authoritative.
- **FR-002**: Every sentence occurrence MUST retain a distinct identity, exact source span and parent paragraph. Every non-whitespace source span MUST belong to an accounted-for sentence, structural unit, protected region or explicitly unresolved region.
- **FR-003**: Segmentation MUST preserve original characters, whitespace, punctuation and order. Reconstructing ordered regions and separators MUST reproduce the original exactly. Splitting MUST NOT rewrite or normalize source text.
- **FR-004**: Every eligible sentence MUST receive every applicable sentence-scoped check from the existing 55-pattern registry. Paragraph/document patterns MUST retain their scope; excluded patterns MUST have explicit reasons. Pattern inventory is not sentence completion.
- **FR-005**: Every sentence-evaluation state MUST include its exact target, complete parent paragraph and relevant supplied context, subject to authorized redaction. Batching MUST preserve these associations without shortening the parent paragraph.
- **FR-006**: Preparation MUST automatically associate structural context and complete immediately preceding/following paragraphs when present in the supplied document, and preserve explicit relevant context. The host MUST be able to add complete nonadjacent supporting paragraphs for references, definitions, conditions, contrasts and source support. Adjacency alone does not establish context sufficiency.
- **FR-007**: Unresolved context dependencies MUST be explicit. Required context MUST NOT be invented, silently dropped or replaced by a summary. External retrieval requires separate authority. A check with an unresolved required dependency cannot be certified context-sufficient; evaluator uncertainty remains visible.
- **FR-008**: A source-bound coverage account MUST enumerate expected work before evaluation and reconcile validated outcomes afterward. It MUST separately report segmentation completeness, evaluation completion, exclusions and unresolved context; sentence, check and request counts MUST remain distinct.
- **FR-009**: Attempted, duplicate, stale or invalid answers MUST NOT satisfy missing work. Sentence completion requires all its required checks validated and no unresolved boundary or necessary-context gap. Overall completion requires all eligible sentence, paragraph and document checks complete, with exclusions separately accounted for.
- **FR-010**: Multi-batch work MUST retain identity and context binding under existing execution, cancellation and transmission limits. Unsupported work MUST remain explicitly uncompleted with a reason, without silent truncation or unbounded calls.
- **FR-011**: Existing prepared sections, explicit targets, context and candidate edits MUST remain supported with valid source binding. Full mode MUST reconcile supplied targets against all source sentences and fill omissions or expose unresolved coverage. Selected-scope diagnostics MUST declare partial scope and cannot report full coverage.
- **FR-012**: Coverage MUST bind to actual source, context, protections, pattern definitions and evaluator model. Changing a relevant binding invalidates affected work. Matching words alone cannot transfer completion between source occurrences.
- **FR-013**: Local source bytes and positions MUST be preserved, while protection applies consistently to all transmitted derived fields. Automatic context expansion MUST stay within approved data scope; unauthorized necessary context leaves affected work incomplete.
- **FR-014**: Missing keys, denied transmission, unsupported execution and service failure MUST preserve offline editing with truthful unavailable/incomplete dispositions. The no-key path MUST make zero evaluator requests; offline preparation is not successful Jev evaluation.
- **FR-015**: The host retains generation and all five editing safeguards. This feature MUST NOT add authorship detection, new linguistic patterns, automatic score-based edit acceptance/rejection/reversion or authority to edit protected content.
- **FR-016**: Verification MUST include an independently annotated synthetic Vietnamese boundary corpus, source reconstruction, context pairs, mixed structures/protections, explicit-target compatibility and fault/limit cases. Segmentation/coverage correctness MUST be distinguished from semantic accuracy and holdout editing-quality claims.

### Key Entities

- **Source document**: Immutable supplied writing, editing metadata and permitted transmission scope.
- **Paragraph / structural unit**: Source-bound parent region, structural role, protection/profile decisions and context links.
- **Sentence occurrence**: Distinct source region, parent and exact or unresolved boundary disposition.
- **Context dependency**: Supporting original paragraph or an unresolved need, with source and permission binding.
- **Expected check**: Required sentence-, paragraph- or document-scoped judgment for an applicable pattern.
- **Coverage account**: Expected work, validated outcomes, exclusions and unresolved/uncompleted work bound to the actual input.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every reference sentence in the approved annotated corpus is identified exactly once with correct boundaries and parent. All non-whitespace spans are accounted for, and source reconstruction matches exactly. Unresolved boundaries cannot count as exact segmentation successes.
- **SC-002**: In controlled complete runs, 100% of expected sentence-pattern checks have validated outcomes without duplicate credit. Paragraph/document work and exclusions reconcile independently.
- **SC-003**: Every context fixture supplies each target's complete parent and required supplied supporting paragraphs, with authorized redaction and no silently added external source.
- **SC-004**: Every injected missing-answer, invalid-response, context-gap, stale-binding, permission and execution-limit case prevents false completion and identifies affected work. No-key runs make zero evaluator requests.
- **SC-005**: Multi-batch and repeated-sentence articles and existing prepared-input fixtures preserve identity, context and coverage without dropping late text or converting full evaluation into partial scope.
- **SC-006**: All protection/source-fidelity fixtures preserve protected local bytes and transmit none of their disallowed content. The five canonical editing safeguards remain applicable.

## Assumptions

- This extends released v0.10.0 and approved feature 007. It does not reopen advisory governance or restore retired 001/002/005 runtimes.
- Source structure is available; ambiguous soft wrapping or sentence boundaries may require host clarification or explicit unresolved status. Universal perfect Vietnamese segmentation is not claimed.
- FR-006 neighboring context is a local minimum, not a one- or two-sentence cap or semantic-sufficiency guarantee. The host supplies nonlocal semantic links; exact segmentation and accounting remain deterministic responsibilities.
- Full coverage means source-bound completion of eligible checks, not favorable judgments or unlimited service availability. Protected/genre exclusions remain distinct from evaluated sentences.
- Existing model binding, consent, budgets, fallback and package parity remain applicable. Planning must resolve current input limits without assuming increased budget or silent context truncation.
- Owner approved this spec, its plan and task generation on 2026-10-16. Code, API spending, packaging, release and shared-skill updates remain later work.
- Live TypeSafe state/structure documentation was inaccessible during specification. No new API capability is assumed; planning must recheck live contracts if integration changes are proposed.
