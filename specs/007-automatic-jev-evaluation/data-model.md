# Evaluation Data Model

Document: transmission_allowed must be literal true before export; sections is a bounded list.

Section: unique ASCII id, profile blog/technical/typography-only, kind prose/heading/list/protected, original paragraph text, optional related context strings and register/audience/purpose. Protected spans use nonoverlapping Python character offsets. Explicit targets use verified offsets; otherwise the editable paragraph is the target. An entirely protected section is excluded.

Candidate: unique section-local id, original start/end span and replacement; edits overlapping a protected span are invalid. Candidates are compared separately and are never applied by the runner.

Pattern: unique canonical ID, source, scope (target/paragraph), semantic/mechanical mode, canonical No flag text and prepared English question recipes.

Coverage: one section/pattern disposition, scheduled and validated counts. Protected, genre and inactive-profile exclusions are distinct from mechanically_checked. Successful remote checks are jev_evaluated, not automatic approval.

Receipt: request digest, requested/actual model, fixed question IDs, safe status and token usage; no source prose, keys or provider error body. Invalid schema adds a fixed reason and a requested check ID only. Judgment includes its request binding and only validated Noul/Choice/Score fields.

Lifecycle: pending → excluded or mechanically_checked, or scheduled → attempted → validated. Limits/service/schema failures leave explicit incomplete/non-pass dispositions. A changed payload, context, rubric or candidate requires new evaluation.

Scores retain raw distributions plus context_supported, ignore_insufficient_context or ignore_unresolved_context dispositions derived from their independent evidence Choice. Ignored scores cannot justify an edit. T3 findings are document-wide observations, with nested quotation styles excluded; host still applies canonical exceptions.
