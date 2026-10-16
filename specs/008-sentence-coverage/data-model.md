# Data model — feature 008

Proposed local contract version 2. No database, persistent cache or automatic edits.
Text stays in the input/local preparation; ordinary coverage/health output contains spans, IDs,
status and digests, not source prose. Evaluator payloads carry only authorized redacted content.

## Entities

| Entity | Fields and binding | Validation |
|---|---|---|
| Source | source ID, exact text, digest, layout, source_scope, defaults, protected spans | ≤1 MiB entire input; one raw source or legacy supplied sections; no offset normalization |
| Unit | unit ID, parent ID, role, absolute start/end, source digest, host profile, protected spans | siblings disjoint, parent containment; every source character covered by region/separator partition |
| Sentence | sentence ID, parent unit ID, absolute span, parent-local span, boundary status/reason, profile version | exact source slice; repeated words retain distinct IDs; unresolved intervals are not certified sentences |
| Separator | exact source span, parent/source ID | whitespace/markup not discarded; source reconstruction exact |
| Context member | ID, role, source identity/span or external supplied text identity, digest, protection, permission | full paragraph or full structural unit; no invented summaries; stable source order |
| Context bundle | parent ID/digest, ordered member IDs/digests, metadata/protection/permission digest, host review, unresolved dependencies | default neighbors + ancestry + explicit links; deduplicate identities; no silent drops |
| Expected work group | scope, subject IDs/spans, applicable pattern IDs, recipe key sets, manifest binding | groups expand to unique check keys; no duplicate credit; exclusions have reasons |
| Check outcome | canonical check key, status/reason, validated answer, receipt ID, context disposition | local mechanical or validated remote evidence only; answer type/model/distributions match |
| Request receipt | ID, requested model, exact request digest, manifest binding, wire-ID→check-key mapping, state digest, usage, elapsed time | validate entire response before credit; don't infer evidence from attempted dispatch |
| Candidate review | candidate ID, source parent/span, replacement binding, independent guard outcomes | keep legacy offsets; never substitute for pattern/sentence work |

## Identifiers and versions

Occurrence IDs derive from source identity + source span + structural role; sentence IDs also bind
segmentation profile/override digest. They are repeatable for the same unchanged input and distinct
across repeated source occurrences. No global identity stability is promised after source edits.
All mutable-looking inputs are actually immutable per invocation.

Canonical check key:
`(manifest_digest, scope, unit_id, sentence_id_or_null, pattern_id, recipe_key)`.
Manifest binding includes source, ordered context bundles, protections/permissions, genre metadata,
layout/overrides, segmentation profile version, registry digest, evaluator config and exact model.
Wire question IDs are bounded ASCII aliases with a local reversible mapping; prompts explicitly
point to the actual state field and meaning. Array positions are never durable identities.

A compact work group and its applicable recipe set mathematically enumerate expected checks before
calls. Store sparse outcomes and compact pending/failed groups, not a full copy of text per check.
Expose expandable IDs/ranges with counts so the host can identify every pending sentence/recipe.
If a local preparation deadline prevents full inventory, record the untouched source remainder as
unresolved spans; do not invent a complete expected denominator or report segmentation complete.

## Transitions

- Source region: `unprocessed → structural | protected | sentence_exact | boundary_unresolved`.
- Context: `not_reviewed → reviewed_complete | unresolved | permission_blocked | too_large`.
  Host attestation must bind the actual source/context snapshot. New links invalidate affected work.
- Remote check: `planned → dispatched → validated`; or `uncompleted(reason)` on a failure/limit.
  A valid answer can still have `context=insufficient`; this preserves evidence but blocks semantic
  completion. `dispatched` is not `validated`. No automatic retries or favorable rerolls.
- Exclusion: explicit `excluded(reason)` before scheduling; not a successful evaluator answer.
- Mechanical check: `planned → mechanically_checked`, once at its canonical scope.
- Candidate reviews follow separate guard transitions; they do not fill any detection check.

## Reconciliation invariants

Let E be all required check keys after genre/protection decisions, V the validated remote keys and
M the completed mechanical keys. Let X be excluded check groups, which are reported separately.
`missing = E − (V ∪ M)`; duplicates cannot increase `|V|`. No key outside E can satisfy E.
Counts satisfy `required = validated + mechanical + uncompleted` at finalization, even after halt.
Excluded work is outside that denominator and never relabeled evaluated. A run with only exclusions
reports `evaluation_complete=false`, `all_excluded=true` rather than a vacuous remote success.

`answers_complete` requires `missing` empty. `segmentation_complete` requires complete source
accounting and exact/resolved boundaries for all eligible prose. `context_complete` requires
reviewed dependency bundles and no required permission/size/insufficient-evidence blockers.
`evaluation_complete` requires all three, full declared scope, required candidate guards complete
when candidates were supplied, and no unresolved scope/validation issue. It says nothing about
absence of a linguistic violation or accuracy of model judgment.

Per-sentence aggregates follow the same rules for that sentence. Parent/document check completion
is independent. Output includes exact sentence/pattern/recipe-level gaps, not only a percent.
A numeric denominator over an unresolved region is labeled provisional, never exact.

## Existing-answer uncertainty

Retain every validated raw probability/distribution. Evaluate Choice by its recipe role, not just
an option name. An evidence-role Choice requires its explicit `sufficient` selection for a
context-supported result. `insufficient` means missing evidence; `none_fit` means unresolved context;
a missing evidence answer is uncompleted work. All three block affected context completion.
An interpretation-role `none_fit` can legitimately mean no offered interpretation applies and is
not by itself a context blocker; its explicit `insufficient` still signals insufficient context.
Recipe-role mapping is explicit in the versioned evaluator config, not guessed from arbitrary
question-ID suffixes or option words. No registry recipe is changed. No Noul probability threshold
is introduced to certify sufficiency; independent signals are not averaged into a completion score.
Host-known unresolved context always blocks completion even if Jev returns a favorable value.
Future dependencies or resolved context require new state-bound judgments, not relabeling old ones.
