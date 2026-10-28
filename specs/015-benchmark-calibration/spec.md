# Feature 015: Calibrate editing safeguards from benchmark evidence

**Created**: 2026-10-26 · **Status**: owner authorized implementation.
**Input**: owner accepted improvements for meaning/action preservation, punctuation,
community terminology and advisory Jev use. No new benchmark generation or paid calls.

## User Scenarios & Testing

### US1 — Preserve intended action and scope (P1)
A reader receives copyedits without a newly invented procedural instruction.
Given an ambiguous original, when its wording is edited, then the host preserves the
ambiguity or asks, rather than choosing an unsupported actor/object/action grouping.
R020 motivates a regression case; its preferred rewrite is a host judgment, not a human gold label.

### US2 — Avoid style-driven overediting (P2)
A reader keeps established terminology and voice unless an identifiable error requires change.
Given T2 punctuation or V19 terminology, edits must respect the five safeguards and
genre/audience evidence; an English equivalent alone does not authorize translation.
T2's existing em-dash trigger remains unchanged: observed replacements follow that rule
and are not themselves demonstrated false positives.

### US3 — Keep Jev advisory (P2)
A host independently scans core patterns even when first-pass source judgments are low,
missing or acceptable. Those judgments are not candidate-specific acceptance decisions.
No inferred runtime veto bug, numerical edit threshold or provider change is authorized.

## Requirements

- FR001 Record exact original/output excerpts, source IDs/hashes, context, classification,
  existing rules and uncertainty in calibration LOG before changing the shared instructions.
- FR002 Strengthen existing safeguard2/3/4, V19 and T2 only; do not introduce patterns.
- FR003 Add positive and anti-overediting cases with explicit expected behavior and basis.
- FR004 Trace R001 advice/prompt evidence; distinguish observed facts from causal hypotheses.
- FR005 Mark all20public benchmark sources as development/calibration data for future versions;
  freeze historical outputs/Forms/manifests and retain the old rules for reconstruction.
- FR006 Synchronize patch metadata and canonical Jev registry; check package and affected
  registry consumers offline, without presenting checks as proof of editorial improvement.

## Edge Cases

Unknown audience; deliberately colloquial jargon; allowed en-dash ranges/dialogue;
protected literal punctuation; punctuation edits that change grouping; source-only vs
candidate judgments; incomplete advice; already-natural original; future holdout contamination.

## Key Entities

Calibration observation, original/output excerpt, expected contrast, source SHA, rule
mapping, manual regression case, advisory trace and development-set designation.

## Success Criteria

Every change traces to a named existing safeguard/rule and a recorded observation.
All listed counterexamples have reviewable expectations; pattern inventory remains55.
Registry/version checks pass and archived data remain byte-identical. Live model efficacy
remains untested; no quality superiority, release, installation or publication claim.

## Assumptions

Owner approval authorizes calibration maintenance and the bounded source patch, not
independent gold labels or broad anti-em-dash rule reversal. Existing T2 policy is retained.
