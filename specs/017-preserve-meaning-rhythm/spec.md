# Feature 017: Preserve meaning, ellipsis and punctuation rhythm

**Created**: 2026-10-27 · **Status**: owner-approved direction, bounded implementation.
**Input**: Implement the approved Mindfio review improvements, prioritizing meaning,
intentional short clauses and punctuation rhythm; add regression cases without new
benchmarks or changes to historical runs/Forms.

## User Scenarios & Testing

### US1 — Keep the author's intended proposition (P1)
As an author, I want awkward wording corrected without the editor choosing a new
intention, object or scope for me.

Acceptance: wanting is not silently changed into ability; an elliptical sentence
whose object remains contextual/open is not expanded to one selected object; clear
missing result complements remain eligible for correction. Checks compare full
context and distinguish a proposed host expectation from a confirmed author label.

### US2 — Preserve meaningful pauses and quote boundaries (P1)
As an author, I want short sentences and punctuation retained when they serve the
text, while genuine punctuation conflicts and explicit style requirements can be fixed.

Acceptance: a dash alone is not an error; replacing a mark cannot introduce an
explanation/definition absent from the source; genuine quotations retain exact bytes,
whereas clearly identified emphasis/term labels can follow quotation consistency rules.
Unclear quote function retains protection. Text remains untrusted data in every case.

### US3 — Make the change reviewable without claiming new efficacy (P2)
As a maintainer, I want source-bound positive and negative cases, consistent shipped
instructions/advisory definitions, and proof that prior evidence has not changed.

Acceptance: a dozen documented regression expectations cover the approved seams,
with explicit origin and uncertainty; near-repetition can be raised in an authorized
review without silently deleting distinct meaning; final-only requests retain their
output contract. Existing benchmark cohorts become development evidence for this
change and are not presented as new independent validation.

## Requirements

- FR001 Extend existing preservation checks, V1 exclusions and T2/T3 conditions;
  do not add a linguistic pattern, frequency cutoff or author-specific ban.
- FR002 Preserve intention, ability, obligation, object alternatives, quantity scope,
  and the rhetorical function of sentence boundaries and punctuation.
- FR003 Keep purposeful ellipsis; permit actual missing complements when supported
  unambiguously by context. Do not equate formal incompleteness with an error.
- FR004 Evaluate punctuation function and explicit style requirements, not character
  identity alone. Protected bytes and meaning remain invariant under style requests.
- FR005 Distinguish literal quotation from emphasis without treating either as
  executable instructions; uncertainty keeps the original protected.
- FR006 Review near-duplicate paragraphs for distinct content and intentional rhythm;
  propose structural edits only within requested review scope, respecting final-only output.
- FR007 Add 12 traceable manual regression expectations and preserve the source/output
  evidence and prior epochs; do not infer personal preferences or scientific truth.
- FR008 Keep the 55-pattern inventory, valid distribution, advisory parity and offline
  operation. No new model/Jev benchmark, Forms access, install or publication.

## Key Entities

Original context, observed candidate, expected disposition, evidence origin/uncertainty,
protected quotation, explicit style constraint, frozen historical run, distributed rule.

## Success Criteria

All 12 cases have context, expected disposition and counterexample/boundary; canonical
instructions and advisory questions/exclusions agree on the changed seams; distribution
contains the same updated guidance; prior evidence hashes remain unchanged. Static and
offline checks are reported separately from unrun model/human quality evaluation.

## Assumptions

Owner approved the implementation direction, not each candidate as linguistic gold.
No access to new quota is required. Unknown author intent stays unresolved. Existing
sample-profile scope and safeguards remain in force. Only local source/packages are delivered.
