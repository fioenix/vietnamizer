# Feature Specification: Meaning-first reference voice

**Feature Branch**: existing checkout; no branch switch
**Created**: 2026-10-28
**Status**: Accepted scope; implementation authorized by owner
**Input**: Implement approved P0/P1 from pilot021 diagnosis; preserve meaning before reference voice, add V1/example regressions; no further benchmark or Forms changes.

## User Scenarios & Testing

### User Story 1 - Preserve supplied meaning (Priority: P1)
A user receives an edited text containing every original proposition without new factual or explanatory claims.
**Independent Test**: Inspect V1 source/addition and contradictory profile examples against the instructions and regression expectations; this is a manual contract review, not model execution.
**Acceptance Scenarios**:
1. Given the V1 repositories sentence, when its grammar is repaired, then no singular/plural explanation is added.
2. Given vague benefits, when wording is simplified, then no numbers, causes, experiences, negations or unique benefits are invented or deleted.
3. Given an available example elsewhere in the authorized document, when moved, then its scope and qualifications remain intact.

### User Story 2 - Learn scoped voice traits (Priority: P2)
A user explicitly requesting reference voice can receive legitimate structural and surface changes without flattening the author's relation to the reader.
**Independent Test**: Review positive/negative examples for numeral notation, functional questions and pronoun roles.
**Acceptance Scenarios**:
1. Given a sample using digits for explicit counts, then quantity-preserving notation changes may apply, while expressions such as một số and protected bytes remain unchanged.
2. Given a shared-action chúng ta and a reader instruction bạn, then both may coexist without forced global pronoun normalization.
3. Given a functional technical question heading, then B6 does not flag it solely for question syntax; fabricated consensus remains excluded.

### User Story 3 - Use only relevant instructions (Priority: P2)
The host reads the root, resolver, applicable profile/card and necessary reference material without collecting every alternative.
**Independent Test**: Trace blog, SOP, typography-only and tool-unavailable branches; inspect all generated package bytes.
**Acceptance Scenarios**:
1. Given a single-function article, then choose one applicable profile/card before loading it; use voice guide only when supplied samples/profile trigger it.
2. Given all documents already inline or no file tools, then apply only the relevant documents without pretending to unload context or executing unavailable tools.

### Edge Cases
- Correct external knowledge is still outside-source content.
- New connective, pronoun or heading can introduce a proposition or relationship.
- Ambiguous sources stay ambiguous; numbers in idioms differ from explicit quantities.
- Mixed-function documents select documents per real section, not every paragraph.
- Weak or conflicting samples narrow adaptation instead of manufacturing a voice.

## Requirements

### Functional Requirements
- **FR-001**: Root owns source-to-edit and edit-to-source meaning checks, including omissions and true-but-new explanations; meaning precedes voice selection.
- **FR-002**: Supplied context can support an edit only within the authorized content scope; samples supply style evidence, not transferable facts.
- **FR-003**: Repair all contradictory before/after examples in the touched blog profile, not only B5/B11; keep all unique source claims.
- **FR-004**: Record scoped numeral, pronoun-function, rhythm and structural traits with sample evidence and exceptions; no quotas or global replacements.
- **FR-005**: Clarify B6/B15 and relevant card exclusions without new patterns, weakened safety or changed protected spans.
- **FR-006**: Root owns selective document loading; guide/resolver point to it without duplicating authority. No automatic host loader or benchmark rewrite.
- **FR-007**: Add documented V1 and contradictory-example regressions with allowed/rejected outcomes and provenance; no claim of new model pass.
- **FR-008**: Synchronize source patch0.13.1, package bytes and generated Jev registry. Preserve runtime/API/question scope and55patterns.
- **FR-009**: Preserve historical benchmark files and both Forms; no new model/Jev calls, rescoring, publication or global install.

### Key Entities
- Source proposition: actor/action/object, quantity/time, conditions, negation and modality with source span.
- Style trait: observed form/function, example, applicable scope and exception.
- Edit: source support, preserved propositions, bounded style justification and protected bytes.

## Success Criteria

### Measurable Outcomes
- **SC-001**: Every added regression has explicit source, allowed behavior, rejected behavior and offline/manual status.
- **SC-002**: No repaired example requires a claim absent from its displayed source/context.
- **SC-003**: All affected package/registry checks pass; three archives preserve canonical instruction bytes.
- **SC-004**: Every pre-existing historical file matches its pre-edit hash; zero new inference calls and zero Forms interactions.
- **SC-005**: Documentation distinguishes implemented instructions from untested model effectiveness.

## Assumptions
- Owner approved the P0/P1 design in the preceding diagnosis; no additional product decision is needed.
- Existing benchmark data are development evidence, not independent correctness labels or proof of causes.
- No new evaluator budget is authorized; deterministic checks and host manual review proceed without Jev.
