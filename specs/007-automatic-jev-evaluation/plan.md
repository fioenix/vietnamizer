# Implementation Plan: Automatic Jev Evaluation

**Checkout branch**: `codex/007-automatic-jev-evaluation` | **Feature**: `007-automatic-jev-evaluation` | **Date**: 2026-10-16 | **Spec**: [spec.md](spec.md)

**Input**: Owner-approved specification and shadow-clause amendment authorization. Plan preparation followed by inline implementation is explicitly authorized.

## Summary

Ship a standard-library evaluator with a prebuilt 55-pattern registry. An injected key activates permitted Jev evaluation by default; absent keys retain core editing without HTTP. Typed judgments inform the host LLM while the five editing safeguards remain authoritative. No automatic patch application or numerical edit policy is introduced.

## Technical Context

**Language/Version**: Python 3.12+; actual local test interpreter is recorded in evidence.\
**Primary Dependencies**: Standard library; existing Python/ZIP packaging tooling. No SDK or new dependency.\
**Storage**: No runtime persistence; JSON results to stdout, no raw prose/secret telemetry.\
**Testing**: unittest, transport doubles only at the HTTP boundary, extracted-package CLI tests, bounded synthetic live smoke.\
**Target Platform**: Hosts able to run Python with an injected environment key; no-key and unsupported-host core fallback.\
**Project Type**: Markdown skill plus advisory CLI.\
**Performance Goals**: Bounded work and explicit incomplete coverage; no unmeasured latency/quality target.\
**Constraints**: 1 MiB input/response, 48,000-byte requests, 48 questions per request, 32 requests, 120-second deadline, 15-second request timeout, no retries or cross-invocation cache bypass.\
**Scale/Scope**: 55 canonical pattern IDs; blog/technical/typography-only/protected routing; per-candidate judgments.

## Constitution Check

Before research: all principles apply. Owner approval explicitly permits active advisory use and authorizes amending the shadow clause. No automatic numerical edit decisions are introduced. Core remains standalone on absent key or service errors.

After design: preserve canonical rule ownership and exclusions, source-bound generated definitions, exact input/model/rubric binding and minimal permitted context. Mechanical checks stay in code. Holdout evidence remains mandatory before numerical automatic acceptance/rejection/reversion. Network errors are never pass. No threshold is being fit or claimed valid in this implementation.

## Project Structure

```text
specs/007-automatic-jev-evaluation/
  spec.md
  plan.md
  research.md
  data-model.md
  contracts/cli.md
  quickstart.md
  tasks.md
  evidence.md
jev/
  __init__.py
  __main__.py
  core.py
  transport.py
  registry.json
scripts/build-jev-registry.py
tests/test_jev.py
```

**Structure Decision**: Keep transport, planning/validation and CLI separate. Store recipes in the generator; copy the canonical No flag exclusions into generated registry data. Package exactly the runtime files, not generator/tests/feature docs. Shared code serves all patterns; an individual-pattern diagnostic does not claim complete coverage.

## Review Focus

1. Absent keys and denied transmission cause zero HTTP requests.
2. Protected spans, candidate edits and related context cannot leak through alternate fields, error messages or output.
3. Batching/size/deadline limits preserve complete accounting of scheduled, attempted and validated checks.
4. Wrong model, IDs, types, distributions, nonfinite values and echoed source are rejected before use.
5. Extracted archives retain runtime/registry parity and the source security allowlist.

The matching tests and implementation steps are in tasks.md. Each task uses RED → GREEN; owner authorization selects inline execution. No commit, shared installation or publication is authorized.

## Complexity Tracking

No unresolved constitutional exception. The explicitly approved governance amendment is recorded in the constitution and spec. Quality calibration remains separate from implementation/transport validation.

## Workflow provenance and correction

The initial task-oriented plan used writing-plans granularity and was reconciled to the Spec Kit plan template after owner feedback. The owner subsequently authorized project-local Codex integration bootstrap. The installed speckit-implement and speckit-tasks instructions now own execution and the reconciled task list; accepted requirements and approvals are retained. Bootstrap preserved all twelve existing shared infrastructure files. No extension hook configuration or requirements checklist directory exists. No shared/global skill installation or release is authorized.
