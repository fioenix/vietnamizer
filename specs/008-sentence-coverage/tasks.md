# Tasks: Automatic paragraph and sentence coverage

**Input**: Approved [spec](spec.md), approved [plan](plan.md), [research](research.md),
[data model](data-model.md), [contracts](contracts/) and [quickstart](quickstart.md).
**Branch**: `codex/008-sentence-coverage`
**Approval**: Owner approved plan and task generation on 2026-10-16. This file is a backlog;
owner authorized local implementation after analysis on 2026-10-16. That initial authorization excluded remote evaluation and publication. Subsequent owner decisions authorized review/push/merge (PR #12, merged 2026-10-18), then release v0.10.5 and shared installation; live evaluator use remains separately scoped. Check boxes only for verified work.

**Tests**: Required by owner, FR-016 and constitution. Each behavioral implementation must follow
its listed failing test(s). Record actual RED → GREEN commands, revision and output in `evidence.md`;
an import error alone is not behavioral RED. Use local fake transports/clocks, not real API quota.
**Format**: `- [ ] Tnnn [P?] [USn?] Action with exact repository-relative paths`.
`[P]` means file-disjoint work after stated prerequisites, not permission to spawn or publish.
New file paths below are proposed deliverables, not files already present.

## Phase 1: Setup — evidence and independent corpus

**Goal**: Freeze the starting state and establish reference annotations before tuning boundaries.

- [x] T001 Record the implementation starting revision, source/config versions, existing suite results, Python/environment identity and authority limits in `specs/008-sentence-coverage/evidence.md`; distinguish the historical 86-test baseline from current command output. Do not alter unrelated working-tree files.
- [x] T002 Create independently annotated synthetic source fixtures and provenance in `tests/fixtures/segmentation/cases.json` and `tests/fixtures/segmentation/README.md`: exact spans/parents, expected unresolved regions, CRLF, decomposed Vietnamese, emoji, abbreviations, decimals, dates, URLs, ellipsis, dialogue and counterexamples. Obtain an annotation check independent of the scanner output before accepting labels; record unresolved disagreements, and never remove failing cases to inflate accuracy.

**Dependencies**: T001 → T002. Source fixtures use synthetic prose; no export of user articles.

## Phase 2: Foundational — source and work identities

**Goal**: Establish immutable source coordinates and compact expected-work accounting shared by stories.

- [x] T003 [P] Write behavioral RED tests in `tests/test_preparation_input.py` for v2 raw-source input and valid v1 sections, required layout/profile, “≤1 MiB entire input”, half-open code-point offsets, parent containment, incompatible/overlapping annotations, source digests and unchanged source reconstruction; use small hand-annotated units without relying on the future scanner.
- [x] T004 [P] Write behavioral RED tests in `tests/test_coverage_model.py` for the canonical key `(manifest_digest, scope, unit_id, sentence_id_or_null, pattern_id, recipe_key)`, distinct repeated occurrences, sparse outcomes, explicit exclusions and source/context/model/registry binding invalidation. Verify “Array positions are never durable identities” and no Cartesian-product prose copies.
- [x] T005 Implement immutable input/source/unit/span validation in `jev/preparation.py` to pass T003: “one raw source or legacy supplied sections; no offset normalization”, “siblings disjoint, parent containment”, “exact source slice” and protected-token/CRLF/combining-sequence endpoint checks. Preserve the exact decoded string, not a normalized or reconstructed substitute.
- [x] T006 Implement work-group identities, exact expandable recipe sets, sparse outcomes and exclusion accounting in `jev/coverage.py` to pass T004; enforce “no duplicate credit” and `required = validated + mechanical + uncompleted` without eagerly materializing all sentence×recipe rows.
- [x] T007 First add behavioral RED remainder/deadline tests in `tests/test_coverage_model.py`, then define the shared source/context/version bindings and invocation deadline handoff between `jev/preparation.py` and `jev/coverage.py`, extending `tests/test_coverage_model.py` to cover unprocessed remainder spans on preparation timeout. Include preparation in the same 120-second evaluation budget and keep pending denominators explicitly provisional when inventory is incomplete.

**Dependencies**: T001–T002 before T003/T004; T003 → T005, T004 → T006; T005+T006 → T007.
**Checkpoint**: Shared contracts pass behavioral tests. No story may claim source/evaluation completion yet.

## Phase 3: US1 — Check every sentence without hand-prepared targets (P1)

**Goal**: Automatically prepare exact paragraphs/sentences and expose required work without manual targets.
**Independent Test**: Compare prepared source spans/parents and required recipe identities against
independent annotations. Remote success is not needed to demonstrate local segmentation.

### Tests first

- [x] T008 [P] [US1] Write behavioral RED tests in `tests/test_preparation.py` against the T002 annotations and `contracts/segmentation.md`: abbreviations/initials, number/date/version tokens, URL trailing punctuation, `...`/`…`, mixed `?!`, quotation attribution, multi-sentence dialogue, nested closers, lowercase ambiguity and a final sentence without punctuation. Assert exact boundaries and explicit unresolved intervals, not only sentence counts.
- [x] T009 [P] [US1] Write behavioral RED tests in `tests/test_structure.py` for paragraph-lines versus Markdown layout, soft wrapping, paragraph overrides, empty/whitespace input, headings, list continuations, code/table blocks, source partitions/separators, CRLF and decomposed characters. Verify no detected-unit cap of 16 sentences or 32 paragraphs and exact source reconstruction.
- [x] T010 [P] [US1] Write behavioral RED CLI tests in `tests/test_cli_preparation.py` for network-free `prepare`, no credential access, versioned span/manifest output, no raw-prose diagnostics and exit 2 for invalid/unresolved preparation. Verify no-key `evaluate` still returns before reading input and does not masquerade as preparation.

### Implementation and verification

- [x] T011 [US1] Implement the structural pass in `jev/preparation.py` to pass T009: explicit layout, lossless parent/separator spans, structural ancestry and authoritative host overrides; preserve host genre/protection metadata and retain unsupported/ambiguous structures with explicit dispositions.
- [x] T012 [US1] Implement profile `vi-spans-1` and its ordered token/boundary rules in `jev/preparation.py` to pass T008: scan original source before redaction, retain final remainder, apply bounded lookahead and versioned abbreviation exceptions, and resolve only validated host boundary overrides. Do not certify uncertain merged regions as sentences or claim UAX #29 conformance.
- [x] T013 [US1] Add the offline `prepare` command in `jev/__main__.py` using `jev/preparation.py` and `jev/coverage.py` to pass T010. Emit source accounting, segmentation/context dispositions and compact expected-work groups without evaluator calls or source prose in ordinary diagnostics.
- [x] T014 [US1] First add a behavioral RED independent profile/recipe-set oracle in `tests/test_preparation.py`, then connect automatic preparation to full evaluation in `jev/core.py`: generate every applicable sentence-pattern recipe from the unchanged registry, retain paragraph/document scopes and explicit genre/protection exclusions, and expose the complete planned universe before dispatch. Extend `tests/test_preparation.py` with an independent profile/recipe-set oracle; full remote status remains subject to US2/US3 completion gates.
- [x] T015 [US1] Run the US1 input/structure/scanner/CLI tests and record exact-boundary, parent, reconstruction and unresolved-case results in `specs/008-sentence-coverage/evidence.md`; label this checkpoint local preparation, not full article evaluation or Vietnamese judgment accuracy.

**Dependencies**: Phase 2 → T008/T009/T010; T009 → T011; T008+T011 → T012;
T010+T012 → T013; T013 → T014 → T015. Tests in T008–T010 are file-disjoint.
**MVP checkpoint**: US1 is a useful offline preparation preview only. Do not publish or claim
full Jev coverage until all required context/accounting/protection work below passes.

## Phase 4: US2 — Interpret each sentence in context (P1)

**Goal**: Preserve full parents, complete relevant context, permission and reviewed dependencies.
**Independent Test**: Feed annotated sentence/context pairs through a recording fake transport and
inspect actual state, exact source/context identities and context-completion dispositions.

### Tests first

- [x] T016 [P] [US2] Write behavioral RED tests in `tests/test_context.py` for identical sentence text in different parents, complete previous/next paragraphs, heading/list ancestry, complete nonadjacent definitions/antecedents, explicit external supplied paragraphs and missing/false/stale host context review. Assert identity-based deduplication, stable source order and no summary substituted for original text.
- [x] T017 [P] [US2] Write behavioral RED tests in `tests/test_context_protection.py` for unauthorized linked context, protected text repeated in neighbors/external context, missing links and known unresolved dependencies; assert zero affected dispatch for known missing/unauthorized required context, no silent expansion of consent, and no protected bytes in any projected parent/target/context field.

### Implementation and verification

- [x] T018 [US2] Implement context links, full-neighbor/ancestry assembly and immutable bundles in `jev/preparation.py` to pass T016/T017: “full paragraph or full structural unit; no invented summaries; stable source order” and “default neighbors + ancestry + explicit links; deduplicate identities; no silent drops”. Preserve supplied nonlocal links rather than using adjacency as proof of sufficiency.
- [x] T019 [US2] Implement source-bound global/per-parent host review and explicit unresolved/permission dispositions in `jev/preparation.py` and `jev/coverage.py`: missing review is `context_not_reviewed`; known missing required members block affected checks, while unreviewed local-context evidence remains provisional and cannot establish full completion.
- [x] T020 [US2] Project full redacted parent, sentence identity and structured related-context records into state in `jev/core.py`, with explicit question-path references and “full paragraph and relevant related_paragraphs” instructions. Apply the same protection policy to every derived field, and bind receipts/work to actual context and metadata digests; do not rely on wire question IDs to convey judgment meaning.
- [x] T021 [US2] Run the same-sentence/different-context, nonlocal dependency and protection tests with recorded fake payloads; record exact binding and whole-paragraph assertions in `specs/008-sentence-coverage/evidence.md`. State explicitly that these tests prove preparation, not live Jev semantic discrimination.

**Dependencies**: Phase 2 and US1 preparation contracts → T016/T017; both → T018 → T019 → T020 → T021.
US2 can be tested with supplied exact units; its integrated checkpoint also runs US1 regressions.

## Phase 5: US3 — Know exactly what was checked (P1)

**Goal**: Reconcile every required check across bounded batches, including unscheduled late work.
**Independent Test**: Compare ledger outcomes with an independently calculated expected-key set under
controlled successful, partial, stale, invalid and exhausted runs.

### Tests first

- [x] T022 [P] [US3] Write behavioral RED tests in `tests/test_coverage.py` for exact `E − (V ∪ M)` gaps, duplicate/no extra credit, per-sentence and parent/document independence, all-excluded input, candidate guards separate from detection, repeated wording at distinct spans, stale source/context/model/registry results and aliases changing target indexes.
- [x] T023 [P] [US3] Write behavioral RED multi-batch tests in `tests/test_coverage_batches.py` for >16 sentences in one parent, >32 detected paragraphs, one sentence's recipes crossing requests, exact 48-question edges, window-size reduction when target copies alone exceed bytes, and a single required state that cannot fit one question. Compare full parent/context bytes across requests and identify every late missing sentence/recipe.
- [x] T024 [P] [US3] Write behavioral RED fault tests in `tests/test_coverage_faults.py` for exactly 32 allowed requests with no 33rd call, no per-parent/window budget reset, 120-second absolute deadline including preparation, ≤15-second call deadlines, cancellation, late responses, malformed/missing/extra answers and service halt. Assert atomic rejection of a bad response, retained earlier valid batches and final explicit reasons for all never-scheduled work; no retry/chained invocation.
- [x] T025 [P] [US3] Write behavioral RED role-sensitive tests in `tests/test_coverage_context_status.py`: evidence-role Choice requires `sufficient`; `insufficient`, `none_fit` and absent evidence block affected context completion; interpretation-role `none_fit` remains a legitimate no-match. Preserve raw distributions, no Noul threshold and no inference of recipe roles solely from arbitrary ID suffixes.
- [x] T026 [P] [US3] Write behavioral RED stress tests in `tests/test_coverage_scaling.py` for the 1 MiB high-sentence-count corpus, compact pending groups, exact expansion/counts and a preparation-deadline remainder. Measure the plan's ≤2-second/≤128-MiB incremental preparation targets in a recorded environment and detect eager sentence×recipe text duplication separately from remote latency.

### Implementation and verification

- [x] T027 [US3] Complete expected-work enumeration and stable wire-ID mappings in `jev/coverage.py` to pass T022/T026: derive recipe counts from the registry, use bounded ASCII aliases, retain source/context/version bindings and sparse status groups, and enumerate missing identities without storing full prose per check.
- [x] T028 [US3] Implement ledger-driven bounded packing in `jev/core.py` to pass T023/T024: at most 16 target references/window, one full parent/context bundle, exact post-redaction UTF-8 payload ≤48,000 bytes and ≤48 questions, stable check keys across windows, one invocation budget of 32 calls/120 seconds and ≤15 seconds/call. Shrink target membership before declaring `context_too_large`; never trim required parent/context or recipes to fit.
- [x] T029 [US3] Reconcile strict response/receipt validation in `jev/core.py` and `jev/coverage.py` to pass T022/T024: “validate entire response before credit”, bind actual model/state/request digests, preserve earlier valid evidence after halt and finalize every pending group, including parents not yet reached. Preserve `jev/transport.py` fixed-origin, response-size and cancellation protections; change it only if the existing deadline handoff cannot satisfy the tests.
- [x] T030 [US3] Implement explicit recipe-role context gates and granular/aggregate completion in `jev/coverage.py` and `jev/core.py` to pass T025: separate source accounting, segmentation, answers and context completeness; full success also requires supplied candidate guards. Preserve all-excluded and partial diagnostics without vacuous remote success, and derive legacy aggregates from the ledger rather than competing counters.
- [x] T031 [US3] First extend `tests/test_cli_preparation.py` with behavioral RED status/scope cases, then implement schema/config version 2 output, declared `source_scope`, `--scope selected` diagnostics and exit/status behavior in `jev/__main__.py`; extend `tests/test_cli_preparation.py` for key-absent early return, denied transmission, prepared-only, selected-scope success and incomplete/full states. Ordinary reports expose IDs/spans/reasons rather than raw prose or credentials.
- [x] T032 [US3] Run T022–T026 and CLI tests, record exact denominator/missing-set comparisons, request/byte/time bounds, actual stress measurements and uncertainty outcomes in `specs/008-sentence-coverage/evidence.md`. If stress targets fail, diagnose the measured cause and reverify affected changes; do not silently raise limits, omit checks or reinterpret partial coverage as complete.

**Dependencies**: Shared foundation and US1/US2 contracts → T022–T026; they are file-disjoint.
T022+T026 → T027; T023+T024+T027+US2 state projection → T028;
T022+T024+T028 → T029; T025+T029 → T030 → T031 → T032.
**Checkpoint**: Every required check is either validated/mechanical or explicitly uncompleted;
context insufficiency and unresolved boundaries still veto full completion. Complete accounting
is not a guarantee that every article can finish within the budget.

## Phase 6: US4 — Preserve structure, protections and existing inputs (P2)

**Goal**: Keep v1 input/candidates working and protected/structured writing safe under auto-targeting.
**Independent Test**: Run legacy explicit-input and mixed-structure fixtures through preparation,
recording transport and coverage reconciliation, comparing exact protected bytes and source binding.

### Tests first

- [x] T033 [P] [US4] Write behavioral RED compatibility tests in `tests/test_legacy_coverage.py` for v1 supplied-sections scope, exact-sentence aliases, missing explicit targets filled in full mode, broad/partial custom targets retained only as supplemental diagnostics, duplicate/overlap rejection, legacy validity caps, and source-bound candidate offsets after segmentation. Paragraph/custom-target success cannot fill canonical sentence work.
- [x] T034 [P] [US4] Write behavioral RED integration tests in `tests/test_structure_protection.py` for editable list prose, headings, unsupported/table structure, inline/fenced code, wholly/partly protected sentences and boundaries hidden inside protection. Assert explicit exclusions/unresolved spans, original local protected bytes and consistent redaction of targets, parents, context and candidate revised paragraphs, including sentinel-enclosing matches.

### Implementation and verification

- [x] T035 [US4] Implement legacy normalization and exact sentence alias/custom-diagnostic mapping in `jev/preparation.py` and `jev/core.py` to pass T033; preserve valid existing sections and full source scope, keep invalid overlapping targets distinguishable, and ensure diagnostic success cannot claim full-source coverage.
- [x] T036 [US4] Finish structural/protected-unit routing in `jev/preparation.py` and shared projection in `jev/core.py` to pass T034: no segmentation after redaction, no guessed boundary inside opaque material, authoritative exclusions and one consistent protected-span policy across all derived fields.
- [x] T037 [US4] First extend `tests/test_legacy_coverage.py` with behavioral RED candidate cases, then integrate candidate guards in `jev/core.py` and `jev/coverage.py`, extending `tests/test_legacy_coverage.py` for unchanged parent-local source offsets, protection-overlap rejection, numeric-token reporting, separate meaning/new-claim/improvement/voice checks and candidate incompleteness. No guard automatically accepts, rejects, applies or reverts text; all five host safeguards remain mandatory.
- [x] T038 [US4] Run legacy/structure/protection integration and existing `tests/test_jev.py`, `tests/test_jev_transport.py` regressions, updating only assertions affected by documented contract v2 semantics; record exact scope/protection/candidate results and remaining limits in `specs/008-sentence-coverage/evidence.md`.

**Dependencies**: US1/US2 preparation and US3 reconciliation → T033/T034 (file-disjoint);
T033 → T035; T034+T035 → T036 → T037 → T038. Earlier stories retain their independent local tests.

## Phase 7: Cross-cutting acceptance and delivery readiness

**Goal**: Prove all runtime consumers and packages match final source, without publishing/installing.

- [x] T039 Write behavioral RED archive/consumer tests in `tests/test_distribution.py` and `tests/test_package_security.py` requiring all new runtime modules in all three archives, exact canonical/resource bytes, extracted-root network-free `prepare` and no-key `evaluate`, plus compatibility aggregate/versioned-status behavior. A source checkout passing is not archive parity.
- [x] T040 Update the prescribed runtime inventory and packaging consumers in `scripts/validate-package.py`, `scripts/package-skill.sh` and `scripts/package-plugin.py` as needed to pass T039; verify newly added `jev/preparation.py` and `jev/coverage.py` ship without tests, local artifacts or secrets. Keep registry recipes/scopes unchanged and verify generated-source parity.
- [x] T041 Document v2 preparation, source/context review, exact coverage states, supplied-sections scope and stricter completion migration in `SKILL.md`, `references/typesafe-advisor.md`, `README.md`, `AGENTS.md`, `CONTRIBUTING.md` and `docs/plugin-distribution.md`; keep canonical ownership/line limits. Coordinate source version metadata in `SKILL.md`, `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` plus changelog under the repository's current version rules, without creating a tag, release or shared installation.
- [x] T042 Execute the full offline suite, registry `--check`, package validation/build, pinned Skills CLI listing, both Claude validators and all extracted-package parity scenarios from `specs/008-sentence-coverage/quickstart.md`; record commands, final tested revision, Python/environment, results and unavailable checks in `specs/008-sentence-coverage/evidence.md`. No live TypeSafe call or shared-profile install is included.
- [x] T043 Obtain independent exact-revision code/security review covering segmentation/source binding, context permissions/redaction, ledger/response validation, limits/cancellation, compatibility and package consumers; record findings, scope and limitations in `specs/008-sentence-coverage/review.md`. A reviewer report alone is not proof of acceptance.
- [x] T044 Verify and resolve applicable review findings in their specifically affected runtime/test/doc files, record dispositions and focused regression evidence in `specs/008-sentence-coverage/review.md`, and rerun invalidated acceptance checks from T042. If no findings require edits, record that result without manufacturing code churn.
- [x] T045 Reconcile all FR-001–016 and SC-001–006 against final evidence in `specs/008-sentence-coverage/evidence.md`, mark only verified tasks complete in `specs/008-sentence-coverage/tasks.md`, and summarize unresolved owner decisions in `specs/README.md`. Separate implemented/verified from publication, merge and shared deployment; none of those external actions is authorized by this task list.

**Dependencies**: US1–US4 → T039 → T040 → T041 → T042 → T043 → T044 → T045.
Review and integration policy from the canonical coding workflow still applies at execution time.

## Dependencies & execution order

```text
T001 → T002
             ├─ T003 → T005 ─┐
             └─ T004 → T006 ─┴─ T007
                                  ↓
                     US1 tests → structure/scanner → prepare → planned work
                                  ↓
                     US2 tests → context links/review → protected state
                                  ↓
                     US3 tests → ledger → bounded scheduler → reconciliation/status
                                  ↓
                     US4 tests → legacy/structure/protection/candidate integration
                                  ↓
                     archive RED → packaging/docs → full checks → review → evidence
```

Order the P1 stories as US1 → US2 → US3 because integrated execution uses prepared units and context.
US4 is P2 but its protection invariants apply throughout: do not defer safe redaction or genre gates
until that phase. Tests for each story can run against controlled prepared units independently;
this does not mean their runtime writers can edit shared modules simultaneously.

All tests for a seam must exhibit behavioral RED before its implementation and GREEN afterward.
Independent annotations/oracles cannot be generated by importing the scanner or scheduler under test.
This graph originally authorized task generation only. The owner later approved implementation and then independent external review, fixes, tests, commit, push and a draft PR. The subsequent 2026-10-18 decisions authorized merge (PR #12), release v0.10.5 and shared installation; live evaluator use still needs its own authority.

## Parallel opportunities and examples

Run only after the prerequisites above are complete, under one writer per file:

| Stage | File-disjoint task pair/group | Restriction |
|---|---|---|
| Foundation | T003 + T004 | Independent test files; no runtime writer yet |
| US1 | T008 + T009 + T010 | Scanner, structure and CLI RED tests only |
| US2 | T016 + T017 | Context semantics versus transmission-protection RED fixtures |
| US3 | T022 + T023 + T024 + T025 + T026 | Separate ledger/batch/fault/context-role/stress test modules |
| US4 | T033 + T034 | Legacy compatibility versus structure/protection RED integration tests |

For example, US3 batch tests can be authored in `tests/test_coverage_batches.py` while fault tests
are authored in `tests/test_coverage_faults.py`. Both must precede T028/T029. Keep writes to
`jev/preparation.py`, `jev/coverage.py`, `jev/core.py` and shared evidence serial, or explicitly
hand them over between responsible writers. `[P]` does not bypass capacity/delegation authority.

## Requirement coverage

| Requirements / outcomes | Primary tasks | Independent acceptance |
|---|---|---|
| FR-001–003; SC-001 | T002–T003, T005, T008–T015 | Exact annotated boundaries/parents; partition reconstruction; explicit uncertainty |
| FR-004, FR-008–009; SC-002 | T004, T006, T014, T022, T027, T029–T032 | Independently calculated expected/missing key sets, no duplicate credit |
| FR-005–007; SC-003 | T016–T021, T025, T030 | Whole parent/nonlocal context pairs, permission/review/evidence-role gates |
| FR-010; SC-004–005 | T007, T023–T024, T026, T028–T032 | Multi-window, impossible-state, 32-call/deadline and exact late-work gaps |
| FR-011–012; SC-005 | T004, T022, T031, T033, T035, T037–T038 | Legacy aliases/diagnostics, source-scope and stale-binding checks |
| FR-013–015; SC-004, SC-006 | T010, T017–T020, T031, T034, T036–T038 | Zero-network fallback, all derived redaction, independent candidate guards |
| FR-016; all SC | Test-first tasks, T039–T045 | Independent corpus/oracles, fault/stress/package evidence and exact-revision review |

## Implementation strategy and evidence limits

First deliverable is the offline US1 preparation preview, with exact spans and uncertainty. The
full feature requires context, ledger, protection, compatibility and final package/review gates;
US1 alone cannot be described as complete Jev sentence evaluation. Advance incrementally and keep
required test evidence at each checkpoint. Do not make a draft PR, merge, release, contact another
user-owned session or update shared skills merely because a task suggests later readiness.

Long articles can have complete source accounting and incomplete remote evaluation. No test should
force every large article into a 32-call success expectation. Real model judgment quality remains
outside fake-transport evidence; optional live smoke/semantic trials need separate data/quota authority.
No tasks introduce new edit patterns, automatic edit decisions, thresholds or service dependencies.
