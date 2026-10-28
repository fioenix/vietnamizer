# Implementation Plan: README evidence

**Branch**: `codex/readme-evidence` | **Date**: 2026-10-28 | **Spec**: [spec.md](spec.md)

## Summary
Replace the 936-line README with a <=220-line introduction, two visible scientific figures, before/after examples, short install/use instructions and navigation. Preserve detailed material in focused docs and preserve important existing anchor entry points. Reuse only existing frozen outcomes; no new provider calls or benchmark runs.

## Technical Context
- Markdown docs; existing Python standard-library package validator/tests remain offline.
- Scientific figures rendered by Matplotlib3.10.8 in an isolated task environment, with pinned/hash-locked optional maintainer requirements. No dependency added to the shipped skill or core validation/test environment.
- Public figure data regenerated deterministically from unchanged source reports018/025 with report SHA256 provenance. Counts, planned units and missing records are arithmetic, not model judgments.
- Output: inline SVG figures; local PNG/PDF exports for visual inspection/sharing. Stable SVG metadata and hash salt.
- Platform: GitHub Markdown light/dark, desktop/mobile widths; white plot surface ensures text contrast in both themes.

## Constitution Check
PASS: source reports and limitations retained; meaning/voice findings separated; development evidence never relabeled holdout or human. No canonical rules/profile/runtime/version changes. Exactly55patterns/seven cards still checked after moving detailed tables. No API calls/spend; no raw/Forms/package mutation.

## Depth Gate
Tasks/implement path selected: the split changes the documentation-location contract consumed by validate-package.py and its fixture builders, and requires ordered documentation, evidence rendering and parity checks. Not eligible for the direct seam exception. Spec/plan/contract/tasks are scoped to this reorganization, not a new benchmark feature.

## Project Structure
- README.md: concise value/evidence/install/use/index; retain useful evidence/install/history anchor entry points.
- docs/installation.md, usage.md, style-and-voice.md, architecture.md, patterns.md, benchmarks.md, sources.md, changelog.md: moved material with rebased links.
- docs/figures/: renderer, frozen plotting data/theme export, two SVGs, pinned optional rendering requirements and lock.
- scripts/validate-package.py: validate relocated docs plus concise root version/link contract.
- tests/test_distribution.py, tests/test_package_security.py: include docs in package fixtures; retain/add meaningful negative tests for relocated inventory/version checks.
- AGENTS.md: reflect file ownership and new documentation pointers without weakening editing/package rules.

## Phase0 Research
See research.md for evidence selection, chart semantics, document map, current validator coupling and immutable-state boundary.

## Phase1 Design
See data-model.md, contracts/documentation.md and quickstart.md. Re-evaluated constitution: PASS; release payload and55IDs remain unchanged.

## Verification
Run negative documentation-contract tests first, then relevant distribution/package-security tests, validator and metadata check; no full suite or model calls. Verify generated data/source hashes, all documentation links/anchors, rendered charts at desktop/narrow width, payload/historical raw and existing release archives byte parity. Record actual results/limits in verification.md before delivery.

## Source and Open Obligations
Canonical workflow read via approved Obsidian CLI, source updated2026-10-23; review-by2026-10-21 is expired. Orrery note_search found its mirror; no Orrery error. No knowledge writes requested. TypeSafe citation cookbook retrieval failed; no new API budget was authorized, so factual source/arithmetic checks stay with host/code and any independent semantic evaluator is not claimed. A publication permission does not follow from local verification.
