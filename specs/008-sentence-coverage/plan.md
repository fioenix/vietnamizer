# Implementation Plan: Automatic paragraph and sentence coverage

**Branch**: `codex/008-sentence-coverage` | **Date**: 2026-10-16 | **Spec**: [spec.md](spec.md)

**Input**: Owner-approved spec 008. Owner approved this plan and authorized task generation on 2026-10-16; local implementation subsequently authorized on 2026-10-16; publication and shared installation remain outside scope.

## Summary

Add lossless local paragraph/sentence preparation and a source-bound expected-work ledger ahead
of the existing Jev scheduler. The host supplies genre/protection and reviews context dependencies;
code owns segmentation, exact source coordinates, batching and coverage reconciliation. Each
sentence judgment receives its full parent paragraph, neighboring/structural context and supplied
nonlocal supporting paragraphs. Uncertain boundaries/context and exhausted budgets remain visible.

Planning resolves three central issues:

1. A versioned deterministic Vietnamese source-span profile handles documented punctuation cases
   and emits explicit unresolved regions when the source cannot disambiguate boundaries.
2. Transport windows contain up to 16 target references from one complete parent/context bundle;
   they do not redefine paragraphs or cap detected sentence count. Context is never truncated to fit.
3. A compact manifest enumerates the full required sentence/pattern/recipe universe before calls.
   Validated batches credit only their bound checks; every remaining item survives as missing work.

Design artifacts: [research](research.md), [data model](data-model.md),
[segmentation contract](contracts/segmentation.md), [CLI contract](contracts/cli.md),
[validation guide](quickstart.md). No tasks or source edits are part of this phase.

## Technical Context

**Language/Version**: Python 3.12+ standard library; existing Markdown skill remains standalone.

**Primary Dependencies**: No new dependency or language-model tokenizer. Existing `jev` transport
stays at fixed endpoint and pinned `jev-1.14.0`; question recipes and all 55 editing patterns remain
unchanged. Unicode UAX #29 is a design reference, not a new runtime dependency/conformance claim.

**Storage**: Invocation-local immutable source/context manifests and sparse result maps; no database,
automatic persistent cache, raw-prose telemetry or automatic continuation state.

**Testing**: `unittest`, controlled transport/clock responses, independently annotated synthetic
boundary/context fixtures, subprocess and archive parity checks. Real Vietnamese semantic accuracy
requires separate labeled evaluation and is not inferred from offline mocks.

**Target Platform**: Existing Python-capable Codex/Claude/custom-skill hosts on macOS/Linux; host
execution/transmission permissions remain prerequisites. No host configuration change in this plan.

**Project Type**: Markdown skill with optional Python advisory CLI and three generated archive formats.

**Performance Goals**: Linear bounded scanning of source plus bounded token lookahead; lazy check
expansion avoids sentence×recipe text copies. Proposed local preparation target on a 1 MiB synthetic
fixture: ≤2 seconds and ≤128 MiB incremental peak memory on the recorded development environment.
These are engineering acceptance targets to measure, not current benchmark results or semantic
thresholds. Preparation timeout must return exact unprocessed spans without false completion.

**Constraints**: Existing 1 MiB input/response, 48,000 bytes/request, 48 questions/request, 32 requests,
120-second invocation deadline, 15-second per-call ceiling. No truncation, automatic retry, unbounded
batch loop, new auto-edit policy or transmission expansion. Preserve all five editing safeguards.

**Scale/Scope**: Entire input may exceed 16 sentences/32 paragraphs while retaining existing input
byte limit. Full source accounting is distinct from remote evaluation completeness. Blog currently
needs 82 sentence questions +36 per paragraph; 1,536 question slots are only a theoretical upper
bound per invocation. A long article can be fully inventoried yet only partially evaluated.

## Constitution Check

Pre-research gate: PASS for design scope against constitution 2.0.0. Post-design recheck: PASS,
with implementation evidence below still pending. No amendment or governance waiver is required.

| Principle / gate | Design disposition | Required later proof |
|---|---|---|
| Vietnamese evidence | No new language/editing pattern or frequency threshold; segmentation profile is a tested engineering hypothesis | Independent annotated boundaries and ambiguous contrast cases |
| Meaning, voice and five safeguards | Split only source spans; host generates edits; candidate review stays independent | Source reconstruction, protected offsets, candidate regressions |
| General/profile separation | Existing registry scopes and genre gates retained | Expected matrix per profile; no inactive pattern credit |
| Calibration | No numerical edit-decision policy or model threshold added | Report semantic uncertainty; do not label mock success holdout accuracy |
| Offline independence | `prepare` is local; no-key evaluate early return remains | Network-forbidden fixtures and installed-package execution |
| Data minimization | Complete required context, explicit scope/permission and consistent redaction | Protected neighbor/nonlocal-context payload tests |
| Deterministic code ownership | Scanner and coverage are code; host supplies semantic context links | Independent exact-denominator/union oracle tests |
| RED-first work | New behaviors require failing behavioral tests before implementation | RED/GREEN evidence recorded per implementation seam |
| Publication/install gates | No packaging publication or shared install now | Full suite, all archives, validators, installed byte parity before a later release |

Full coverage is not an assurance that all judgments are correct or that no linguistic issue exists.
Missing host context review cannot be hidden by typed-answer success. No prerequisite is delegated
to Jev and no API quota is used to choose a settled planning activity.

## Project Structure

### Documentation (this feature)

```text
specs/008-sentence-coverage/
├── spec.md                         # Approved input
├── plan.md                         # This design
├── research.md                     # Decisions and live-source limits
├── data-model.md                   # Source/context/work/result invariants
├── quickstart.md                   # Proposed acceptance run guide
├── checklists/requirements.md      # Spec quality review
└── contracts/
    ├── segmentation.md             # Vietnamese profile and reference cases
    └── cli.md                      # Input/output, scheduling and compatibility
```

`tasks.md` is deliberately left to `speckit-tasks` after plan review.

### Source Code (proposed affected paths; not edited in this phase)

```text
jev/
├── __main__.py                     # prepare + versioned input/mode dispatch
├── preparation.py                  # proposed source/structure/sentence/context preparation
├── coverage.py                     # proposed compact work manifest and reconciliation
├── core.py                         # ledger-driven scheduler and legacy aggregates
├── transport.py                    # preserve fixed origin/model, cancellation and deadlines
└── registry.json                   # recipes/scopes unchanged; verify source parity
scripts/
├── validate-package.py             # tracked runtime inventory for new modules
├── package-skill.sh                # verify all runtime files ship
└── package-plugin.py               # verify identical public payload
tests/
├── test_preparation.py             # proposed independent source/boundary oracles
├── test_coverage.py                # proposed matrix, batching and failure oracles
├── fixtures/segmentation/          # proposed annotated synthetic cases and provenance
├── test_jev.py                     # affected semantic scheduling/legacy aggregates
├── test_jev_transport.py           # unchanged contracts/regressions
└── test_distribution.py            # runtime inventory/archive/install parity
```

**Structure Decision**: Keep one small stdlib runtime, with preparation and accounting responsibilities
separate from transport. Exact file count is subordinate to these responsibilities. Update canonical
`SKILL.md`, `references/typesafe-advisor.md`, README/AGENTS and public CLI guidance together in a later
implementation phase. New runtime modules require updating the current five-file allowlist and
archive extraction tests, not merely copying files into the source checkout.

## Phase 0 — Research decisions

Completed design research in [research.md](research.md): layout versus soft wrapping, source-preserving
Vietnamese boundaries, context review, compact ledger, bounded packing, compatibility and stricter
completion semantics. Live TypeSafe State/API and parallel-questions cookbook were read successfully;
structure-recovery cookbook remained inaccessible. No new remote API contract is required.

## Phase 1 — Design sequence

### A. Inventory source before evaluation

Validate raw-source v2 or legacy sections; preserve original offsets and protections. Apply layout,
structure and host overrides. Resolve eligible prose sentences or explicit ambiguous regions.
Build parent/context bundles and complete expected work groups before scheduling. Source partition
reconstruction is the initial invariant. Logical detection must not inherit legacy transport caps.

Host-context review is explicit: source-bound reviewed/no-unresolved attestation or unresolved needs.
Default adjacency is assembled automatically but does not certify nonlocal completeness. Known missing
or unauthorized required context blocks affected dispatch. Unreviewed local context can yield
provisional evidence, but never `evaluation_complete=true`.

### B. Schedule from the immutable ledger

Derive recipe sets from the live canonical registry and profile, including explicit exclusions.
Sort by scope/source order as defined in the CLI contract. Build exact-size window payloads from one
parent/context bundle; shrink target membership before declaring impossible size, never parent/context.
Paragraph/document work is counted once; target recipes may cross batches; candidate guard work has
its own keys. Stable check keys are independent of local target indexes and request boundaries.

A deterministic preflight can simulate exact packing/counts and expose a request lower bound, but
cannot promise latency or remote success. If more than 32 requests would be needed, execute only
the permitted prefix and retain the full missing set. One request must not reset another's deadline.
No implicit second run, budget increase or automatic resume is included.

### C. Validate evidence and finalize all work

Preserve strict model/type/distribution/usage validation and atomic response acceptance. Correlate
wire IDs only through their receipt mapping and state binding. On halt, reconcile all expected work,
including parents/sentences not yet visited by scheduling. Aggregate compatibility fields derive
from the ledger rather than independent counters that could disagree.

Completion requires exact segmentation, reviewed sufficient context and all required scoped work.
Valid `insufficient` answers remain evidence but block semantic completion. Evidence-role
`none_fit` is also unresolved; only `sufficient` supports context completion for that role.
Interpretation-role `none_fit` remains a valid no-match outcome, not an automatic blocker. Separate diagnostic success,
all-excluded input, no-key fallback, local preparation and full remote success. No outcome applies edits.

### D. Verification and migration

Create annotated fixtures before heuristics, including explicit expected-unresolved cases. Obtain an
independent annotation pass before accepting corpus results; no reviewer/model is asked to infer a
truth label from the implementation's output. Use exact boundaries plus union/reconstruction oracles,
not only aggregate counts. Preserve current 86-test baseline and extend for v2 and tightened status.

Contract/config version 2 preserves old aggregate fields and v1 inputs while documenting stricter
full-mode semantics and the supplied-sections scope limit. Implementation version bump and release
artifacts are later work; planning neither changes installed behavior nor creates a release.

## Risks and acceptance obligations

- Abbreviation/quotation heuristics can fail unseen Vietnamese. Keep unresolved status and bounded
  host overrides; publish corpus scope and error/abstention metrics, not universal accuracy claims.
- Full context repeats across requests and may dominate cost/bytes. Do not optimize it away silently.
- Long documents can exceed quota despite perfect preparation. An exact missing-work report is a
  required result; remote full completion under the current budget is not guaranteed.
- Tightened completion semantics affect consumers. Versioned output and migration tests are mandatory.
- Offset normalization or redaction before segmentation can corrupt source binding. Original-source
  segmentation, one protected-span policy and archive-installed parity are mandatory.
- No new code, tests, registry edits, network evaluation, release or shared installation was performed
  during this phase. All implementation acceptance obligations remain open.

## Requirement-to-design trace

| Requirements | Owning design | Acceptance evidence to collect later |
|---|---|---|
| FR-001–003 | Segmentation contract; Source/Unit/Sentence/Separator | Independent boundaries, exact reconstruction, unresolved spans |
| FR-004, FR-008–009 | Expected work and reconciliation invariants | Independent check-set oracle, no duplicate/missing credit |
| FR-005–007 | Context bundles and CLI state contract | Full-parent/nonlocal-pair payloads; reviewed/unresolved context |
| FR-010 | Global scheduler/limits contract | Multi-window, impossible state, deadline and 32-call boundary |
| FR-011–012 | Legacy mapping, check identities, manifest bindings | Explicit aliases/diagnostics, stale context/source invalidation |
| FR-013–015 | Protection, no-key dispatch, host editing authority | All derived fields redacted, zero-network fallback, five safeguards |
| FR-016 | Quickstart corpus/fault/package protocol | RED/GREEN seam evidence and separate semantic-quality limits |

## Planning verification receipt

- Spec Kit setup/prerequisites resolved feature 008 and all required Phase 0/1 artifacts.
- Local document checks passed: required files, internal links, balanced code fences, no unresolved
  template markers, and no tasks file. `git diff --check` passed; new files were checked directly.
- Independent read-only design review found one context-role ambiguity: evidence `none_fit` versus
  interpretation `none_fit`. All owning artifacts were updated; the reviewer confirmed it closed.
- No extension hooks are configured. No runtime source, registry, tests, package or shared skill
  changed; no product tests or evaluator calls were run in this documentation-only phase.
