# Feature Specification: Select voice traits by section function
**Created**:2026-10-28
**Status**: Accepted; owner requests implementation from N2diagnosis, no new benchmark.

## User Scenarios & Testing
### User Story1 — Select suitable voice (P1)
A user requests reference-voice editing. Each section uses a form compatible with both the samples and its actual purpose; legal questions/direct address are not automatically preferred or banned.
**Independent test**: manually trace N2and contrasting question/direct-address fixtures against instructions; no new generated output.
**Acceptance**: procedural phases remain distinguishable; headings cover all subordinate content; direct address and questions may be kept/introduced when they serve the section and supplied reference. Valid impersonal prose is not changed merely to install a trait.
### User Story2 — Preserve meaning and useful structure (P1)
Facts, qualifiers, protected spans and useful contrasts survive stylistic restructuring; structure is not frozen globally.
**Independent test**: source/candidate examples include setup done/missing distinction, generic quantity, modality, legitimate merge/split and mixed section functions.
**Acceptance**: format may change while preserving relations and function; no invented step/count, blanket noun-heading rule, global ban on bạn or forced bullet retention.

## Requirements
- FR-001: Distinguish permitted form, evidenced reference compatibility and suitability at the actual section position. Meaning gates precede style choice.
- FR-002: Identify rhetorical role within existing profile/card scope; no new profile for every paragraph, author or heading.
- FR-003: Choose heading/question, address and contrast/list form for the reader task; missing evidence retains a suitable current form without forced interviews.
- FR-004: Check heading coverage and contrast/navigation after semantic verification; allow warranted structural adaptation, do not freeze source layout.
- FR-005: Numeral notation must not create an explicit count absent from source; existing approved count-notation and idiom/protected-byte rules remain.
- FR-006: Record N2observed failure and manual positive/negative regressions before changing rules. Sample/reference mismatch is a benchmark limitation, not a new language prohibition.
- FR-007: Update source patch0.13.2, documentation and all archive layouts; retain55patterns, Jev/questions/schema/security and core fallback.
- FR-008: Preserve all historical benchmark files and two Forms, no new inference/Jev/scoring calls, no release/install/commit.

## Success Criteria
- SC-001: Every new regression has source/context, permissible behavior, rejected behavior and manual/not-run status.
- SC-002: Every instruction decision maps to an accepted requirement and existing authority owner; no contradictory examples or arbitrary frequency thresholds.
- SC-003: Targeted package/registry checks and byte parity for3archives pass; independent patch review findings disposed.
- SC-004: All historical hashes unchanged; no benchmark or Forms calls.

## Assumptions / edge cases
N2voice4→3from both model judges, meaning clear, is development evidence; not human gold or proof of isolated causal mechanism. Generator samples include legitimate questions/you while judge-only references favor topic headings. Do not fit rules to hidden references or author quirks. Existing owner approval settles scope; no evaluator budget or new source research required.
