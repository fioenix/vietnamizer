# Verification: source0.13.1

Date:2026-10-28. Disposition: implemented in current dirty checkout and verified offline; not released, installed globally or tested through a new model run. Existing owner WIP preserved.

## Acceptance / proof

| Requirement | Disposition | Evidence / limit |
|---|---|---|
| FR-001/002 meaning-first source support | Implemented; manually reviewed | Root chốt2 and steps6/7; guide references root; MS01/MS16. No model-behavior claim. |
| FR-003 safe examples | Implemented; manually reviewed | B1/B2/B3/B4/B5/B6/B7/B11/B16 displayed examples; B8/B10 deletion guidance aligned. B7 review correction preserves aesthetic assessment. |
| FR-004/005 scoped reference voice | Implemented; manually reviewed | Guide numeral/pronoun/functional-heading rules; B6/B15. MS05 corrected to preserve metaphor emphasis. |
| FR-006 selective loading | Implemented as instruction | Root owns loading; resolver/guide subordinate; mixed-function, typography-only and inline/tool-unavailable cases covered. No automatic loader or context unloading claim. |
| FR-007 regressions |16documented manual cases | MS01–MS16, artifacts/022-meaning-first-20261028/regression-review.json; no new generated outputs or automated semantic judge. |
| FR-008 source/package parity | PASS |0.13.1metadata,55patterns, all three archives equal canonical payload bytes. Only no_flag changed for B6/B11/B15; question recipes/runtime/schema untouched. |
| FR-009 preservation | PASS local hash verification |25784pre-existing files in artifacts/benchmarks/specs rehashed,0changed; no Forms tool/browser interaction. Hash proof is local-file integrity, not a cloud Forms readback. |

## Commands actually run

- `python3 scripts/build-jev-registry.py`, then `python3 scripts/build-jev-registry.py --check`: PASS,55definitions match. Generator reports seven excluded pre-existing regex signals absent from canonical sections; none newly shipped.
- `python3 scripts/validate-package.py`: PASS, source0.13.1and55patterns; root532/550lines, blog156/320, unchanged K within budget.
- `bash scripts/package-skill.sh`: PASS; both skill layouts built and validated. `python3 scripts/package-plugin.py` and `--check`: PASS distribution metadata and plugin build.
- `PYTHONPATH=tests python3 -m unittest` with seven named PackageSecurityTest cases plus JevTest.test_registry_covers_exact_ids_and_canonical_exclusions: **8passed**,4.017seconds. Exact command/results are in artifacts/022-meaning-first-20261028/targeted-tests.log and execution trace. Scope: recipe-drift guard, style-registry/card gates, regular payload, ClaudeOrglayout, card inclusion, staged-archive bytes and canonical registry. Full suite not run.
- `claude plugin validate .` and `claude plugin validate .claude-plugin/plugin.json --strict`: exit0, validation passed. Both report three existing local .DS_Store directory warnings. Canonical archives contain none. No directory approval/publication claim; directory scan itself covers first20000entries and32levels.
- `npm_config_offline=true npx skills add . --list`: **unavailable**, ENOTCACHED for skills registry package. No dependency/network install attempted; Skills CLI discovery remains unverified.
- Host offline verification: compared every canonical payload byte in all three archives; exactly one SKILL.md each; compared registry objects and all historical hashes; source digest matches reviewed delta. Output: artifacts/022-meaning-first-20261028/final-verification.json.
- `git diff --check`: PASS, including pre-existing tracked WIP. New delta separately captured from pre-edit before/ snapshot in implementation.patch, rather than claiming whole working diff belongs to022.

## Independent review

One scoped reviewer examined source snapshot delta and instruction contracts. Two P2findings: B7deleted distinct aesthetic assessment; MS05could weaken metaphor emphasis. Both corrected and reviewer re-read exact amendments, reporting no remaining findings. Final source manifest refreshed after those amendments. Review covers instruction semantics; package parity is separate host proof. Review is not new benchmark generation/scoring.

## Provenance / remaining limits

Spec Kit specify/plan/tasks/implement used; all required hooks absent (.specify/extensions.yml does not exist). Requirements checklist6/6before implementation. User approved P0/P1; no constitution amendment or new product decision needed.

Zero new benchmark generation/evaluation/Jev calls, no rescore and no Forms changes. No new evaluator budget consumed. Model efficacy on0.13.1remains **not run**; old model findings are retained verbatim as historical evidence. No claim the additions are now empirically eliminated or that0.13.1beats prompt+samples. No commit, publish or global installation.

Canonical workflow read through supported Obsidian CLI after one escalation retry. Its review-by2026-10-21is expired; source unchanged. Orrery found workflow and older VietnamizerT016memories but no current pilot state; local accepted specs govern this change. No knowledge-base write requested or performed.
