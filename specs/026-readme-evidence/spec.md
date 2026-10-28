# Feature Specification: Concise README with inspectable evidence

**Feature Branch**: `codex/readme-evidence`
**Created**: 2026-10-28
**Status**: Ready for planning
**Input**: Owner requests a concise README, visible benchmark charts establishing bounded practical value, and detailed material moved into supporting docs.

## User Scenarios & Testing

### User Story 1 - Understand the value and its limits (Priority: P1)
A reader can find purpose, concrete before/after examples, visible benchmark figures, and the supported conclusion without navigating a long reference manual.
**Independent Test**: Read the main page without expanding details; identify the use case, evidence provenance and quality limitations.
**Acceptance Scenarios**:
1. Given a first-time reader, when opening README, then purpose/examples/two scientific figures and a quick install command are visible.
2. Given the historical regression and current voice pilot, when reading the figures, then the compared versions, same-generator design, model-judge identities, denominators and missing results are explicit.
3. Given mixed findings, when interpreting the page, then no universal quality, independent-human or holdout benefit is implied.

### User Story 2 - Find advanced documentation (Priority: P2)
An advanced user can reach the complete installation, usage, voice/style, architecture, pattern inventory, sources and changelog from a compact navigation table.
**Independent Test**: Follow each navigation link and locate the original information with working relative paths.
**Acceptance Scenarios**:
1. Given any moved section, when following its README link, then detailed content remains available with preserved facts and valid links.
2. Given release/profile links to important README headings, when following them, then useful installation/evidence/changelog entry points remain.

### User Story 3 - Maintain the documentation contract (Priority: P2)
Contributors can verify all 55 documented patterns, seven style cards and the latest version after the split without restoring the long README.
**Independent Test**: Run existing packaging checks against the reorganized sources; deliberately remove a pattern or change the detailed changelog version and confirm rejection.

### Edge Cases
- Missing Gemini V2 judgment remains missing, never a tie/loss/clear result.
- Codex/Gemini in voice charts denote judges, not different editor agents.
- Development regressions do not establish population accuracy or current-version perfect behavior.
- Figures stay legible in GitHub light/dark themes and at narrow widths.
- Archived raw, source reports, Forms and released packages are unchanged.

## Requirements

### Functional Requirements
- FR-001: Main README must be at most 220 lines, with purpose, examples, quick installation and documentation navigation.
- FR-002: At least two inline benchmark figures must show available quality-related evidence and its limits; text-change volume must not be used as quality proof.
- FR-003: Figures must use only existing frozen results, retain all planned units/missing judgments, identify development status and link to source reports.
- FR-004: Detailed information removed from README must remain available in focused docs; instructions, public citations and historical caveats must not be lost.
- FR-005: Documentation checks must continue enforcing version, complete pattern and style-card inventories at their new locations.
- FR-006: No skill behavior/version, model/provider calls, protected payload, release artifact, benchmark raw or Forms changes.
- FR-007: Figures must have reusable data/provenance and a documented repeatable rendering command; optional rendering tooling must not become a core install dependency.

### Key Entities
- Evidence figure: source report/hash, comparison, outcome counts, planned/observed units and interpretation limits.
- Detail guide: moved section ownership and relative-link mapping.

## Success Criteria
- SC-001: README shrinks from 936 to no more than 220 lines, with two visible figures and no collapsed research archive.
- SC-002: Every displayed quantitative result agrees with the existing source reports; planned/missing denominators reconcile.
- SC-003: All moved guidance and README/document links resolve; all 55 patterns, seven cards and source version remain validated.
- SC-004: Named preserved files have zero hash changes; only targeted tests/checks are run.

## Assumptions
The deliverable is a reviewable repository change, not a new benchmark or release. Reuse existing data. Keep source0.13.2 and released artifacts unchanged. Publication/merge remains a separate action after the result is reviewable.
