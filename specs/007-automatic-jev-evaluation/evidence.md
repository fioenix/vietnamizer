# Implementation evidence — feature 007

Initial implementation verification, 2026-10-16. The later owner-authorized Claude Code/Antigravity review, fixes and PR verification are recorded in review.md; hashes and counts below bind the earlier snapshot. This is a local delivery, not a release or a shared-runtime installation.

## Workflow and authority

- Owner approved spec 007, the active-advisory/shadow-clause amendment, implementation and the later project-local Codex integration bootstrap.
- Canonical coding workflow was read through approved Obsidian CLI, explicitly targeting Fioenix Vault. Installed speckit-implement owns execution; installed speckit-tasks reconciled the earlier task checklist to story phases and IDs. Accepted design/approval was retained.
- `specify integration install codex --script sh --integration-options='--skills'` initially hit sandbox EPERM in `.agents/skills`; supported escalation then exited 0. The twelve existing shared infrastructure files were preserved. Generated skills/local state remain ignored. No global tooling, shared skill, commit, push, merge or release was performed.
- No extension hook file or requirements-checklist directory exists, so those gates require no dispatch/marker changes.
- Installed speckit-converge found one remaining documentation gap (FR-035), appended T021 and returned execution to implement. The obsolete no-runtime distribution statement was then corrected.

## Deliverables and safeguards

- Python 3.12+ standard-library `jev` package and CLI, fixed endpoint and pinned actual-model validation for jev-1.14.0.
- Source-bound generated registry: exactly V1–V25, T1–T6, B1–B17 and K1–K7; English recipes retain canonical Vietnamese No flag exclusions.
- Injected key activates permitted evaluation; absent key causes zero evaluation requests. Permission/capability failures remain distinct. No credential discovery or endpoint override.
- Full paragraph and supplied related paragraphs retained; explicit target spans and protected-only exclusion/redaction. T3 is document-wide and respects nested quotation styles.
- Every Score has a separate evidence Choice. Scores with missing/unresolved evidence are explicitly ignored while their distributions remain inspectable. No calibrated threshold or automatic edit acceptance/rejection/reversion.
- Candidate-specific meaning/new-claim/improvement/voice judgments inform the host LLM; all five canonical editing safeguards remain authoritative.
- Bounded sizes/questions/attempts; killable child bounds full HTTP I/O including stalled/drip-fed response; late replies cannot supply evidence. Shared serialization binds planner limits to actual wire bytes.

## Observed RED → GREEN and final offline checks

Initial runtime RED: 15 tests failed because the runner did not exist. The extracted-plugin test later failed because the runtime registry was not packaged. Both became GREEN after their corresponding implementations. Quote and malformed-JSON classifications also had observed RED/GREEN regressions.

Review fixes: protected-only default target, cross-paragraph/nested T3, late-reply rejection, Score evidence/disposition and shared wire serialization each failed before the fix and passed after it. The absolute deadline regression exercises real stalled and drip-producing child processes, confirms return within the test bound and confirms child collection. Invalid-response diagnostics failed before the fixed-reason/requested-ID receipt was added.

Final source checks:

| Check | Observed result |
|---|---|
| Python 3.15.0 full unittest discovery | 72 tests, OK |
| Python 3.12 runtime/transport tests | 29 tests, OK |
| Python 3.12 full discovery | 72 tests, OK (17.245 seconds) |
| registry `--check` | 55 definitions match canonical sources |
| `python3 scripts/validate-package.py` | Version 0.10.0 valid, 55 patterns |
| `python3 scripts/package-plugin.py` | All three archives generated and validated |
| pinned Skills 1.5.20 listing, temporary cache, `--offline ... --list` | Exit 0, one vietnamizer skill discovered; no installation |
| `claude plugin validate .` | Passed |
| `claude plugin validate .claude-plugin/plugin.json --strict` | Passed |
| `git diff --check` | Passed at runtime/package review; repeated after final docs |

## Historical invalid_response — exact field unknown

The first installed-artifact smoke returned one validated receipt followed by invalid_response (overall incomplete, exit 2). Its first receipt used actual jev-1.14.0 and 11,192 input / 1,632 output tokens. Coverage was 20 jev_evaluated, 27 invalid_response, one mechanically_checked and seven excluded. This failure is retained; it has not been relabeled as success.

One bounded diagnostic reconstructed the exact failed synthetic payload, digest
`1e9b0ffcad00ecf4e0ea07172ea28a8f39ffb86b048b02e0b3fe060f52d1b0cb`.
The digest matches the failed receipt. The diagnostic received a valid response from jev-1.14.0 with 11,571 input / 1,914 output tokens. It did not reproduce the schema error. No user article was sent and validation was not weakened.

The bad original field cannot be recovered because unvalidated bodies were intentionally not retained. Therefore no root-cause/fix claim is made for that historical provider response. Current invalid responses include a safe `validation_error.reason` and, where applicable, the requested check ID. Reasons distinguish model, IDs, answer type, Noul range, probability keys/range/sum, confidence, Choice/distribution, Score range/distribution and usage. Provider strings/prose/error bodies are never copied into diagnostics.

## Final shipped-artifact smoke — evaluated

Local evidence directory: `/private/tmp/vietnamizer-final-z2gcrmbb`.
The final plugin archive was extracted and invoked from `skills/vietnamizer` through existing approved credential injection. Input was the synthetic “Tao hiểu. Mày cứ nói tiếp.” paragraph and its invented work-conversation context, not an article or private-source export.

- CLI exit 0, overall evaluated.
- Coverage: 47 jev_evaluated, one mechanically_checked (T3), seven excluded (inactive K profile): all 55 IDs accounted for.
- 118 validated judgments across capacity-bounded requests. This count is accounting, not a language-quality metric.
- Every validated receipt reports requested/actual jev-1.14.0 and request/response SHA-256 bindings.
- Actual usage totals: 31,940 input / 4,995 output tokens. Billed currency cost unavailable; no zero-cost claim.
- Approximate external smoke interval: 10.695 seconds, measured from redirected output-file creation to final modification; this includes injection/CLI startup and is not per-request API latency or a benchmark.
- No retry within the invocation and no unvalidated/limit-exceeded remainder.

All three archives were separately extracted. Each of the five runtime files byte-matched source in each archive (15 comparisons); every extracted no-key CLI returned key_absent. The final live smoke ran the plugin copy; no claim is made that every host UI discovered or invoked the skill.

## Independent code/security review

Initial review against HEAD baseline b6e3ba7 covered tracked changes plus new runtime/generator/tests/spec files. It found no Critical, four Important and one Minor. Follow-up independently rechecked all five findings and the affected subprocess/privacy/deadline/Score boundaries: no actionable regression found. Reviewer ran 29 runtime/transport tests, registry check and diff hygiene independently, without network or credentials.

| Finding | Disposition and regression |
|---|---|
| HTTP inactivity timeout/late evidence | Resolved: bounded worker kill/collection and post-response deadline; real stalled/drip worker and fake late-evidence tests |
| Entirely protected default target | Resolved: no editable non-whitespace content → excluded/no requests |
| T3 local scope/nested false flag | Resolved: document-wide outer quotation stack, nested-style fixture |
| Score forced context uncertainty | Resolved: independent evidence Choice and ignored-score dispositions |
| Planner/wire byte mismatch | Resolved: same serializer, direct request-data parity fixture |

Review binding (SHA-256):

```text
jev/core.py 3b50b85b96c938af1533dbeae0e3e223fbe48633556215734a2ac3860b513e7d
jev/transport.py a6cf94c358d05163bdce69ef1288b785ec3f7c6562da6e23f728c7fcdaf39403
jev/registry.json 4a82769d30831b566085835ea8c12735f6c3bce4bd4c1b9840896098f543fb2f
scripts/build-jev-registry.py 2fefbac22de5db122192bd5f635336a768a8113d36aa61d24242d1c2d2fbfe32
tests/test_jev.py 3b6e0d580a7cebb37c8c2fe356d4bd709ed99128529228b710414d6c5f9d0ca6
tests/test_jev_transport.py 424511d3707ac8480257bbd5cc4a8bd70c5cdfcc906d897bef8a404d7752676d
references/typesafe-advisor.md 8620807d8b768aa03d37a41eeb0174278dff8818458300b55bef1685ca78e682
```

This was independent manual code/security review, not a Codex Security scan. Review did not establish Vietnamese accuracy/calibration, provider retention, the host's consent decisions, client UI discovery or release readiness. Domain harmful-edit recall/false-block/review rates remain unmeasured: this feature ships advisory primitives and a transport smoke, not a labeled behavioral evaluation or automatic numerical editing policy.

## Spec alignment and convergence inventory

Checked 36 FRs, eight SCs, 14 user-story acceptance scenarios, seven plan decisions (stdlib/shared runner/source ownership/pinned endpoint and model/full context/bounds/archive parity) and five constitutional principles. Evidence is bounded to implementation contracts; no model-accuracy outcome is inferred.

| Requirement group | Implementation/verification |
|---|---|
| FR-001–005, US2, SC-001 | injected-key-only branch, no-key and permission fixtures, extracted CLI |
| FR-006–016, US1, SC-002/004 | 55 registry IDs, per-section coverage/exclusions, batching/mechanical scope, error/budget fixtures |
| FR-017–024 | full-context construction, offset/protected tests, independent types/evidence outcomes, canonical exclusions |
| FR-025–028, US4, SC-005 | per-candidate guards, numeric/protected checks, no automatic decision field, host five-safeguard instructions |
| FR-029–031, US3, SC-003 | strict model/schema/numeric validation, safe diagnostics, error/late-reply tests and current payload bindings |
| FR-032–036, SC-006 | package allowlists/security tests, extracted parity, docs/version sync; historical runtime not reused |
| SC-007/008 | synthetic installed-copy receipts/usage/interval and explicit quality/cost limits |

Convergence found one partial FR-035 gap: stale distribution runtime claims. T021 corrected it in docs/plugin-distribution.md; no application change was needed. No expansion into retired studies or deployment was introduced.

## Archive bindings

```text
vietnamizer.skill 8b7081bba4a32d9b501c7d7b7d1af82700f87a7328183ee35ee1efd24b132a3c
vietnamizer-claude-org.zip 06639a4c4b2199d21ae0f02884ff2fb22e8d66f58f55ee3259fa3caff0589ecb
vietnamizer-plugin.zip e9f9b6c2f98558941388bfeefb59b8a1b460b4402f577565bfa43247a882906d
```

## Final verification

- Python 3.12 full discovery completed: 72 tests, OK. Python 3.15 full discovery: 72 tests, OK. No code changed after those runs.
- Final package validator and plugin metadata `--check` passed after the distribution-doc correction.
- Final tracked diff hygiene passed; new source/spec files checked separately for whitespace and included in the local source binding.
- Staged diff is empty. Generated Codex skills/integration state, feature-local state and dist are ignored; no incidental tooling files are included in the deliverable change.
- All 21 tasks are checked with this evidence. Final Spec Kit convergence found no remaining buildable gap in the approved scope; no new task was appended on that pass.
- Release/shared-runtime installation, UI-native invocation on all clients, Vietnamese holdout calibration and the historical response's exact invalid field remain outside the established proof. None is claimed complete.
