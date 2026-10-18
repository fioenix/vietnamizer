# Research — feature 008

Status: design decisions, 2026-10-16. No runtime changes or live evaluator calls.
Baseline: released v0.10.0, commit `a4e61bf0d5453be5a346c031bdecb68ae79933b3`.

## R1. Lossless deterministic segmentation, with explicit uncertainty

**Decision:** Keep Python 3.12+ and the standard library. Implement a versioned source-span scanner
for the documented Vietnamese subset, followed by host-resolvable boundary overrides. The profile
in [segmentation.md](contracts/segmentation.md) defines rule precedence and reference cases.
Segment the original source before redaction. Never ask Jev to count, split or reconstruct text.

**Rationale:** Offsets, exact coverage and protection must be reproducible offline. A punctuation-only
split fails abbreviations, quoted speech and decimals. Unicode explicitly acknowledges ambiguous
periods and permits tailored profiles; it does not establish that this proposed scanner is a
complete Vietnamese segmenter. No UAX #29 conformance claim is made.

**Alternatives:** Full UAX #29 implementation/data vendoring would add property-table maintenance;
NLP packages would add dependencies and model downloads without demonstrated benefit for this
scope. A model-based structure recovery step adds cost and uncertain source mappings. Neither
is necessary for the initial bounded profile. Unknown/ambiguous spans remain unresolved, not
silently merged into a certified sentence. A future algorithm replacement requires corpus parity.

**Source:** [Unicode UAX #29 revision 49](https://www.unicode.org/reports/tr29/tr29-49.html),
introduction and sentence-boundary conformance/tailoring sections, read 2026-10-16. This informs
uncertainty handling; our Vietnamese rules are engineering hypotheses to verify with annotations.

## R2. Explicit layout, structure and genre authority

**Decision:** New raw-source input declares `layout` as `paragraph-lines` or `markdown`.
The host chooses it; it is not inferred semantically by the runner. Paragraph-lines treats each
nonblank physical line as a paragraph. Markdown joins soft-wrapped prose lines into a logical
source span without changing their characters. Explicit paragraph-span overrides resolve exported
or ambiguously wrapped text. Host defaults/annotations supply genre/profile and protected spans.
Recognized Markdown structure supplies headings/list ancestry; it does not invent genre.
Unsupported markup becomes unresolved or typography-only structure, never an unaccounted gap.

**Rationale:** Plain pasted articles and soft-wrapped Markdown assign different meanings to a
single newline. Choosing a documented layout avoids silently moving paragraph boundaries.

**Alternatives:** Blank-line-only splitting misses single-newline pasted paragraphs; splitting
all newlines breaks Markdown soft wraps. Automatic semantic reconstruction is outside this feature.

## R3. Complete context plus explicit dependency review

**Decision:** For each parent unit, assemble its full text, heading/list ancestry, complete immediate
previous/next paragraph and all supplied nonlocal links. Deduplicate by source identity, not wording.
Every member has a role, source span or external supplied identity, digest, permission and protection
binding. The host reviews context dependencies before claiming full completion. Missing review
is `context_not_reviewed`, not evidence that adjacency suffices. A host can attest reviewed/no
unresolved dependencies or supply explicit unresolved records. This is an auditable host judgment,
not mathematical proof that every implicit reference in arbitrary prose has been found.

**Rationale:** Automatic lexical reference detection cannot guarantee semantic completeness.
The host already owns genre and meaning. Preserve this boundary rather than claiming the scanner
can recover every nonadjacent antecedent. Existing typed `insufficient` choices also veto context
completion for the affected check. Evidence-role `none_fit` remains unresolved and blocks completion;
interpretation-role `none_fit` is not automatically a context gap. Only an evidence-role `sufficient`
selection supports that evidence gate. No new uncalibrated Noul cutoff is introduced.

**Alternatives:** Entire-document state adds unrelated data/cost and often exceeds local limits;
adjacency-only context loses nonlocal definitions. Generated summaries lose source fidelity.

**Sources:** [TypeSafe State](https://docs.typesafe.ai/concepts/state) and
[API reference](https://docs.typesafe.ai/api), read 2026-10-16: named structured state can carry
related facts; question IDs are response keys, not a substitute for meaningful question instructions.
Live extensionless pages worked during planning. The structure-recovery cookbook remained inaccessible;
no undocumented capability is inferred from its index description.

## R4. Ledger first, transport windows second

**Decision:** Inventory source units and expected scope/pattern/recipe checks before dispatch.
Use a compact manifest of units and applicable recipe sets rather than duplicating full prose
or materializing the complete Cartesian product. Expand check keys lazily; pending spans/ranges
and their recipe sets still enumerate exactly which work remains. Results and receipts carry
immutable manifest/state bindings. Paragraph/document results and candidate reviews are separate.

Use up to 16 target references per transport window from one parent/context bundle. This is not
a detection limit. A sentence's recipes may cross requests. Pack by the actual encoded payload
and 48-question cap; rebind question paths to the current window. The full parent and context
stay intact. Prefer smaller target windows if duplicate target text alone prevents fitting.
If one target plus one question cannot fit required state, mark affected work `context_too_large`.

**Rationale:** Current section-pattern counters cannot locate missing sentence work. A transport
window must not become the definition of a paragraph or coverage universe.

**Alternatives:** One request per sentence wastes shared state and still fails a sentence needing
more than 48 questions; one state containing all article targets duplicates data and hits byte limits.

**Source:** [TypeSafe parallel questions cookbook](https://docs.typesafe.ai/cookbooks/parallel_questions),
read 2026-10-16, describes asking independent questions together over the same state. Its example
cost/speed figures are not performance forecasts for Vietnamese or this implementation.

## R5. Preserve global limits and honest incomplete results

**Decision:** Keep 1 MiB input/response, 48,000 encoded bytes/request, 48 questions/request,
32 requests/invocation, 120 seconds overall and 15 seconds/request. These are local safety limits,
not provider maxima. Include preparation/scheduling in the invocation deadline. No automatic retries,
continuation invocations or persistent result-cache/resume feature. A later run needs ordinary host
authority and fresh bindings; it must not silently bypass a prior run's budget.

Direct registry inspection gives 82 sentence questions +36 per paragraph for blog; technical
68 +18; typography-only 8 +2. There are 38 semantic target patterns, 16 semantic paragraph patterns
and T3 mechanical at document scope across the full registry. Profile/genre exclusions reduce each
run's applicable work. Exact counts must be derived from registry recipes, never hardcoded.

The 1,536 question-slot ceiling is only an upper bound: 19 blog sentences alone need 1,558 questions,
before paragraph work, candidates, packing losses and latency. More than 32 source paragraphs can
be inventoried even if only some fit the execution budget. The scheduler attempts the bounded prefix;
the ledger exposes all remaining units/checks. It never claims universal remote completion.

**Alternatives:** Raising budgets or quietly launching more invocations is outside accepted scope.
Dropping recipes or context changes evaluation semantics and cannot be used as a fitting strategy.

## R6. Compatibility and outputs

**Decision:** Add a versioned raw-source input and a network-free `prepare` command. Preserve v1
`sections` input and no-key early return. V1 full mode auto-segments each supplied section;
its coverage scope is `provided_sections`, not unseen original prose. Exact-sentence explicit targets
become aliases; broader/partial custom targets remain optional diagnostics and cannot satisfy
canonical sentence work. Overlapping/duplicate explicit targets are invalid; missing ones are filled.
Original candidate offsets remain parent-local and are mapped without rewriting source.

Output schema/config version 2 retains the existing aggregate `coverage`, `judgments`,
`candidate_reviews` and receipts while adding the manifest and granular outcomes. `evaluated`
becomes stricter: required typed answers, no unresolved boundary/context and all required scoped
work complete. Add `answers_complete` separately from `context_complete`; valid `insufficient`
answers are preserved but do not establish a complete evaluation. The selected-scope diagnostic
keeps its explicit partial coverage designation.

**Rationale:** Existing consumers need their aggregate fields, but retaining a weaker completion
meaning would conflict with approved FR-009. Contract versioning and migration notes make the change
visible. No new edit decisions or automatic acceptance policy are introduced.

## Research disposition

No design unknown remains blocking plan generation. Boundary accuracy, memory/latency targets,
packaging parity and response reconciliation remain implementation acceptance gates, not completed
proof. Spec approval does not authorize code changes or evaluator spending in this planning turn.
