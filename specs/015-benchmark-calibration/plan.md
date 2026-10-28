# Plan: benchmark-driven calibration safeguards

## Scope and workflow
Owner approval resumes implementation; canonical coding-workflow.md already read via
Obsidian CLI in this session. Review-by2026-10-21 expired, guidance unchanged. Spec Kit
owns routing. Tasks/implement path because shared editing/advisory contracts and the
tracked registry change. No deployment, install, new benchmark/model/Jev calls or Forms edits.

## Technical context
Markdown rules; Python stdlib registry builder and validators;55existing patterns.
Canonical consumers: rootSKILL → registry builder → jev/registry.json → packaged payloads.
References/typesafe-advisor.md is host guidance, not a scoring/transport implementation.
Patch0.11.1 synchronizes both plugin manifests and README, without a release action.

## Constitution check
Existing named-error, preservation and minimal-scope principles are strengthened.
No new pattern or numerical edit policy; record evidence before edits. AI-origin
benchmark examples are not native-authored gold or proof of a general language rule.
T2 trigger is retained; wording scopes replacements rather than inferring a new norm.
All20public originals become development/calibration data for subsequent versions.

## Implementation
1. Preserve old canonical source and record LOG + machine-readable observation hashes.
2. Add manual positive/counterexample cases; mark expected labels host-reviewed, not a live model pass.
3. Clarify safeguard2, V19, T2 and source-first-pass advisory use; no runner code change.
4. Regenerate canonical registry and synchronize patch metadata; validate affected consumers.
5. Independent scoped review, compare unchanged historical data and deliver evidence/limits.

## Verification
python3 scripts/build-jev-registry.py; --check; python3 scripts/validate-package.py;
python3 -B -m unittest tests.test_jev (affected registry consumer only). No full suite.
Manual case review is not rerunning models. Packaging/install/release acceptance is out
of scope. Keep source-before snapshot for old benchmark fingerprint reconstruction.

## Open obligations
Determine exact historical cause of differing Jev final remains unproven; inspect raw
facts and leave that causal claim open rather than editing thresholds. New instructions
are not evidence of improved model outputs; future fresh holdout needed for that claim.
