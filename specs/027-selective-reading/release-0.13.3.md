# Release preparation: 0.13.3

## Source and scope

PR28 is merged into main as bed5aaa2e5a34abc451db6ed295691a2ea1f16c2, verified through PR state and main SHA/tree. This preparation branches from that merged commit. The owner authorized releasing a new version and explicitly authorized admin merge for PR28 only; that exceptional grant does not apply to the release-preparation PR. No ruleset, approval or OAuth permissions are changed.

Patch 0.13.3 is selected after inspecting compatibility: Python runtime/CLI/input contract, model, 55 pattern IDs/bodies/recipes, registry schema and judgments are unchanged; feature PR28 relocates canonical source paths and instruction routing. The preparation changes only version metadata and current-version documentation/release notes. Source paths consumed by internal packaging/registry tools were updated in PR28; arbitrary external parsers of old SKILL.md headings are not certified. No new quality, billing-token or actual-read claim is made.

## Validation completed locally

- 66 related tests passed in 22.097s: distribution, selective reading, review evidence and package security.
- Package validator and registry --check pass; no registry regeneration diff is needed for the version-only change.
- Three candidate archives built with package-plugin.py; CRC and every payload byte match source (plugin manifest skills-path layout transformation excepted).
- Every extracted archive passed offline jev status/evaluate with key absent and prepare on synthetic text. Child environment has no service key; no external evaluator call.
- Both Claude validators and offline/no-install Skills CLI discovery pass. No runtime installation.
- The original dirty README in the initial checkout retains SHA256 14443f027bb3d7d317f11533cf7b4c7b4f46b8d25903f440459c4c3f59be3a6e. This release branch changes only two README version/history lines against merged main, without importing that dirty rewrite.

## Unpublished candidate assets

These local hashes describe preparation artifacts, not a tag, published release or immutable expected hashes for a later rebuild. Existing v0.13.2 assets are untouched. Final release assets must be built/verified against the actually merged release-preparation commit, then uploaded and downloaded for hash verification.

| Candidate | Bytes | SHA-256 |
|---|---:|---|
| vietnamizer.skill | 172554 | `894502571cd9a66397560074738f124e01de748101049f7e93bda6a464964faf` |
| vietnamizer-claude-org.zip | 171298 | `ceb3376324416a07d28d6467db3b902cd457f0a3ace461431b0505f76226a159` |
| vietnamizer-plugin.zip | 174565 | `9af646a994e9a0946db4368f2a421539a6afb0ac38dceb55d76d160ea4f83c99` |

## Remaining external gates

Push the release-preparation branch and follow its CI to terminal. Merge it only with the required latest-push approval, unless the owner explicitly grants a separate admin-merge exception for that PR. Never push main directly to avoid review. Before publication recheck v0.13.3 tag/release absence or reconcile any existing result; tag the verified merged commit, publish the three assets and verify target/asset hashes. Do not publish from an unmerged branch or install runtime copies. Semantic/style A/B and authenticated actual-read traces remain pending, independent of release checks.
