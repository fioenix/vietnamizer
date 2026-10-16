# Research Decisions

## Evaluator interface

Decision: Python standard-library HTTP client, fixed TypeSafe System One endpoint and pinned jev-1.14.0. Rationale: current primary TypeSafe API documentation and the observed typed 1.14 responses in this session support Choice/Noul/Score. Alternatives: an SDK adds a dependency; moving aliases already returned 1.13 in an earlier experiment. Actual model is validated.

## Pattern dispatch

Decision: generated definitions for all 55 canonical IDs, with recipe-specific types and copied canonical exclusions. Rationale: maintain one transport and preserve canonical ownership. Alternative: 55 separate clients duplicate credential/error handling. Mechanical-only T3 needs no invented semantic call.

## Context and output

Decision: full paragraphs and supplied related context, verified target spans, redacted protected substrings, separate candidate guards. Rationale: earlier paired-context experiments showed distribution changes; an aggregate ALL-candidates guard could not identify which edit changed meaning. Output is metadata and typed answers, not raw prose.

## Failure and quality policy

Decision: fail open to core editing while marking evaluator errors/noncoverage explicitly; no automatic numerical edit policy. Rationale: constitution and user goal require offline usability and retained five safeguards. Score levels are experimental rubrics, not calibrated truth probabilities. No unresolved technical clarification requires additional research delegation.
