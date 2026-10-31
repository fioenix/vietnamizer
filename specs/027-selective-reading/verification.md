# Verification: selective reading (Unreleased)

Date: 2026-10-31. Branch `codex/readme-evidence`, HEAD unchanged `7a6b07a2460560ce010fb13706c8ae95c8519cee`.
Metadata remains 0.13.2; this is not the original release payload. Existing README is preserved byte-for-byte
(SHA-256 `14443f027bb3d7d317f11533cf7b4c7b4f46b8d25903f440459c4c3f59be3a6e`).

## Route measurements (refreshed for PR28 follow-up)

Method and exact mandatory/conditional file sets: [measurements.json](measurements.json). Full UTF-8 files
counted once, Unicode codepoints and splitlines; excludes user prose, tool output, hidden model scaffolding
and cache. Before uses the saved incoming Unreleased worktree, not HEAD. No model tokenizer download,
context trace, billing-token saving or semantic-quality gain is claimed.

| Route | Before files/lines/chars | After required files/lines/chars |
|---|---|---|
| Core | 1 / 543 / 63,401 | 1 / 135 / 9,699 |
| Local work sentence | 5 / 1,118 / 114,233 | 1 / 135 / 9,699 |
| Professional article | 5 / 1,118 / 114,389 | 3 / 189 / 13,788 |
| New article with supplied samples | 6 / 1,342 / 131,978 | 4 / 249 / 18,099 |

The realistic local missing-complement correction triggers the completion catalog: **2 files / 221 lines /
21,294 chars**, a 81.36% reduction against the same incoming sentence route. Other error families,
profile diagnoses, mixed-context resolver, evaluator contract and lexical details remain conditional and
add their own file sizes when triggered; the table does not pretend they are free. Detailed lookups can
read heading ranges when supported, but these measurements conservatively count whole files.

## Initial modularization checks (before Matt follow-up)

- Saved incoming source/README/registry and default dist archives under output/simplification-20261031/.
- Red check: tests.test_selective_reading failed while registry builder still expected patterns in core;
  output/simplification-20261031/red-relocated.log records the missing relocation binding assertion.
- After update: 60 tests in 23.354s, OK: distribution, selective reading, registry exclusions/signals and
  package security. output/simplification-20261031/package-tests.log.
- 50 tests in 1.287s, OK: test_jev, context protection, structure protection and registry exclusions/signals.
  output/simplification-20261031/runtime-tests.log. Seven registry cases overlap; not 110 independent cases.
- All 55 full pattern bodies compare equal to incoming, excluding only surrounding section separators/
  blank space. All generated registry fields compare equal except canonical source paths; order unchanged.
- scripts/build-jev-registry.py --check: 55 definitions match. Existing unsupported scanner alternatives
  remain excluded, not new exceptions or signals. No runtime recipe/schema/authority changes.
- scripts/validate-package.py, package-plugin.py --check, skill-creator quick_validate.py and git diff --check pass.
- Both Claude CLI validators pass, with five pre-existing untracked .DS_Store warnings; no OS/cache files
  enter the archives. No cleanup of user files. Logs under output/simplification-20261031/.
- Three archives generated and all payload bytes checked against source, including new catalogs; plugin
  manifest `skills` path has only the intended source-to-package layout transformation. Retained under
  output/simplification-20261031/unreleased-0.13.2/ with an explicit non-release manifest and SHA-256.
  Default dist names restored byte-for-byte to incoming baseline; no released archive is overwritten.

## Independent review and corrections

A separately delegated read-only reviewer checked core, routes/catalogs, profiles and package/registry
bindings against the incoming snapshot. Findings addressed: restore the four-question intentional-ellipsis
prerequisite beside V1/V20; retain technical-register restrictions in always-read core; retain the no-key
prohibition on API calls/key requests/setup suggestions; correct adapter ownership wording. Reviewer
read back all four and reported no remaining guard/routing findings in that scope. No edits by reviewer.
Self-review also removed an installed-payload reference to source-only docs from the core route.

## Workflow and remaining limits

Installed Spec Kit specify/plan/tasks/implement route used. All five spec-quality checklist items are met;
no extension hooks are configured. The owner's explicit catalog relocation request supersedes only the
legacy physical V/T-in-core wording; linguistic principles/safeguards are retained, no constitution/version
amendment. The delegated complete-brief exception skips the Vault workflow read; no alternate generic
process workflow substitutes for Spec Kit.

No full historical suite rerun. The previously observed seven artifact-drift errors are not fixed or
relabelled. Historical drivers, manifests/raw and old benchmark runs are untouched; relocating current
registry source paths is expected to differ from their frozen fingerprints. Do not revise those manifests
to hide drift. No external model/paid API or new CLI generation runs, install, commit, push or release.

Controlled behavioral A/B remains **pending**. To test later: freeze the incoming and current libraries,
use identical user tasks/samples/model settings, independent sessions and actual file-read traces rather
than injecting every file. Compare missing-complement, deliberate ellipsis, scoped edits, quantities/
negation/modality/causal ambiguity, protected bytes, technical register and sample-content leakage. Use
fresh texts for semantic evaluation and blinded human/source-linked judgments; report errors/missing
runs and latency/actual provider token usage where available, not character counts as bills. Character
reduction is established; preserving or improving semantic quality remains an empirical question.


## PR28 Matt-research follow-up

[matt-followup.md](matt-followup.md) records pinned provenance, selected gaps, exact-packet/trace limitations, six development cases and the separate empty heldout plan. Core now has 135 lines/9,699 characters; required file sets remain unchanged on the original three routes. The report has separate meaning/style conclusions and cannot silently summarize issue findings as clear/not_assessed. New tests cover stale uncommitted candidates and supplied read-event order, not actual agent execution. The original archive and test receipts above are historical; new follow-up validation and CI are reported on the current PR head, without claiming old archive bytes cover new text. No behavioral A/B or actual-read trace has been executed.

Latest bounded local follow-up run: 66 tests, OK, 21.982s; package validator, registry --check and diff check pass. This is mechanical/contract verification, not a new semantic or actual-routing benchmark.
