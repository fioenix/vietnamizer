# Implementation evidence — feature 008

Scope: local implementation authorized 2026-10-16 after approved spec/plan/tasks and read-only
analysis. This initial phase did not authorize push, merge, release, shared-skill installation or live evaluator spending.
The subsequent 2026-10-17 review request authorizes fixes, commit, push and a draft PR only.
Baseline main/tag v0.10.0: `a4e61bf0d5453be5a346c031bdecb68ae79933b3`; working branch
`codex/008-sentence-coverage`. The following entries preserve local implementation checkpoints; the final external-review section supersedes their current-state claims.

## Baseline and analysis

- Python 3.12 full baseline: `python3.12 -B -m unittest discover -s tests -p 'test_*.py'` →
  86 tests OK, 24.437s (`/private/tmp/008-baseline.log`, local scratch, not public corpus data).
- `speckit-analyze`: 16 FR +6 SC mapped, 45 tasks, no critical/constitution finding. U1/U2
  clarified concrete host fields and behavioral RED evidence; see analysis.md. No extension hooks.
- Requirements checklist: all 16 entries checked; no unchecked gate was bypassed. Existing
  `.gitignore` already covers Python cache, environment files, dist and local tool state.

## Corpus annotation

Independent corpus author produced 54 synthetic cases (42 determinate, 12 unresolved) without
reading scanner output. Parent reviewed original source/slices before accepting labels, including
`TS. Hôm nay chốt.`, ambiguous URL closers and opaque protected endpoints. The conservative
unresolved labels are accepted as profile limitations, not asserted universal linguistic truth.
Corpus version/provenance: tests/fixtures/segmentation/{cases.json,README.md}. No user article copied.

## Behavioral RED receipts

- Existing core on raw v2: `tests.test_coverage` showed `invalid_input` instead of evaluated input,
  three behavioral failures plus missing-new-field errors. Missing imports/fields alone are not
  credited as RED. Captured before changing core in `/private/tmp/008-core-red.log`.
- Batch/fault/context-role assertions on baseline: failures captured in
  `/private/tmp/008-batches-red.log`; no network or credentials used (fake injected strings only).
- CLI prepare before wiring: nonzero unsupported command rather than prepared output,
  `/private/tmp/008-cli-red.log`; no-key early return already passed and remains a regression.
- Context/cancellation follow-up: fake KeyboardInterrupt escaped before final accounting,
  `/private/tmp/008-model-red.log`; after correction, 11 model/core tests passed in 0.059s.
- First integrated coverage/batch/fault/role/CLI checkpoint: 22 tests OK, 10.261s after manifest
  metadata binding and fully protected exclusions were corrected. A lowercase boundary fixture
  was corrected to an uppercase new-sentence case to match the approved profile rather than
  forcing uncertain segmentation to count as exact success.

## Current proof status

The initial checkpoint left preparation receipts, full integrated checks, stress bounds, legacy
migration, package parity and review pending; the final section below records their closure. No task completion
is inferred solely from this evidence document or a worker report.

## Architecture checkpoint and integration

The same preparation-performance invariant failed independent stress checks after local corrections.
Product scanner edits were paused for an architecture checkpoint. Root causes were repeated
unanchored lexical searches over long no-marker tokens and growing-prefix copies during punctuation
scanning. The accepted replacement uses one linear nonwhitespace token traversal, marker-conditional
anchored recognition, bounded initials lookahead and one shared 4096 work budget. No acceptance
threshold or external budget was raised. Disallowed continued suffix scanning was removed rather
than hidden by longer timeouts. Unprocessed spans remain explicit and counts provisional.

Independent 8-second watchdog reproduced the old hang; it was terminated without affecting other
sessions. Subsequent implementation test `tests.test_coverage_scaling` passed at 0.077s and
2,567,854 traced peak bytes on Python 3.12.2 / macOS 26.7.2 arm64. This is Python allocation tracking,
not a measurement of total process RSS; incremental RSS acceptance remains separately assessed.
The fixture is 750 kB and adversarial high-sentence-count, under the 1 MiB input limit.

Preparation owner reported 31 tests (including root scaling) passing on Python 3.12/3.15 with
all 54 corpus subcases run. Parent full integration confirmed 148 tests OK in 21.762s on 3.12.
These are offline structural/runtime checks, not live semantic-quality or Vietnamese holdout proof.

The corpus override fixture was corrected from an inclusive annotation object to endpoint `[14]`
through independent original-string length/slicing, not scanner tuning. The final suite skips no
corpus case. Broader/custom explicit targets and context records changed only as documented v2
migration; original protected-value/sentinel tests remain active.

Package RED rejected two new modules missing from the canonical runtime allowlist. After updating
inventory, all three extracted archives ran local prepare plus no-key evaluation and every shipped
runtime file matched source. Main package validators, registry --check (55 unchanged patterns),
Skills CLI 1.5.20 listing and both Claude validators passed. No shared profile was installed.

Review snapshot `/private/tmp/vietnamizer008-review` has immutable file manifest SHA256
`2f0060d80fbdf515d0a5ad6ac85c8aebf0984294ff8b5a3442ba239073877754`. Its source/test bytes matched
working-tree bytes when dispatched. Independent review is pending; changed source requires delta
re-review and invalidated tests. Runtime version metadata is 0.11.0 **unreleased source only**;
no Git tag/release/cache/shared installation was created.

## Metadata identity checkpoint

Independent review confirmed alias identity confusion and protected data in dynamic context metadata.
Two corrections still left the same tainted-ID invariant red in selected diagnostics. Metadata edits
were paused to map provenance: full targets have source-derived identity, selected targets copied
host aliases, and protected exclusions were derived before sanitization. The accepted boundary is
uniform source-bound identity for every evaluated target in both modes; supplied IDs are aliases
only, protected before local reporting. This is a provenance correction, not another field-only
redaction patch. Candidate/section host identifiers retain guarded compatibility via the centralized
identifier-protection routine and collision rejection. Regression covers full, selected and excluded
paths; exact source offsets remain authoritative.

## Final local acceptance — 2026-10-16

- Final runtime/test bytes match independent r3 snapshot (28 runtime/test/fixture files). All three
  code/security findings closed by independent bounded repros; see review.md. No blocker remains
  in that reviewed scope. No formal scanner or live Jev quality claim is made.
- Python 3.12.2: 154/154 offline tests OK, 27.529s. Python 3.15: 154/154 OK, 29.587s.
  Final logs: local `/private/tmp/008-final-r3-312.log` and `008-final-r3-315.log`.
- 1.02 MB synthetic preparation: 0.0311s and 9,961,472 incremental RSS bytes on 3.12;
  0.0339s and 4,177,920 incremental RSS bytes on 3.15. Both below 2s/128 MiB engineering targets.
  The 750 kB pathological fixture also passed; these are local machine results, not universal SLOs.
- Candidate allocation regression: 400 candidates on a 100,001-character parent now respects
  a 16 MiB traced-memory bound, emits zero requests and preserves explicit impossible-state gaps.
- Final registry --check: 55 definitions synchronized, registry bytes unchanged from v0.10.0.
  Transport bytes unchanged. No new language pattern or numeric edit-acceptance policy.
- Final package build/validation and both Claude manifest validators passed. Full-suite extraction
  tests verify all seven runtime files match source in all three archives, local prepare works and
  no-key evaluate calls no network. Skills CLI 1.5.20 listing passed and was reused after runtime-only
  fixes because skill discovery metadata did not change. New archives are ignored local test output.
- Codex/Claude shared cache 0.10.0 SKILL metadata read back unchanged. No install/update command,
  push, merge, tag or release was executed. Current branch remains codex/008-sentence-coverage;
  implementation is delivered as uncommitted local source, version 0.11.0 unreleased.
- All 45 tasks have evidence-backed local dispositions. Full FR/SC trace below establishes tested
  structural behavior; it does not prove future model judgments, universal Vietnamese segmentation,
  hidden provider capability or native UI invocation in every host. Owner integration/publication
  decision remains pending and outside authorized scope. No extension hooks configured.

### Acceptance trace

| Requirements / outcomes | Verified evidence |
|---|---|
| FR-001–003 / SC-001 | Independent 54-case corpus; source partitions and parent/Unicode/CRLF/override tests; no skipped corpus case |
| FR-004,008,009 / SC-002 | Coverage model/oracle, distinct occurrences, atomic bad-response handling, exact pending recipe sets and independent scoped work |
| FR-005–007 / SC-003 | Complete adjacent/structural/nonlocal context, reviewed/unresolved/permission fixtures, explicit evidence-role versus interpretation gates |
| FR-010 / SC-004,005 | >16 sentences, >32 paragraphs, recipe splitting, exact byte/48-question/32-request ceilings, late/cancelled results and absolute preparation-aware deadline |
| FR-011,012 / SC-005 | Legacy aliases/custom diagnostics/candidates, canonical source identity, source/config binding, partial supplied-sections scope |
| FR-013–015 / SC-004,006 | Protected fields and metadata in full/selected/excluded modes, source-offset fidelity, no-key zero-network early return, host-only edits and independent candidate guards |
| FR-016 / all SC | Behavioral RED receipts, independent corpus labels, 154-test suite on both runtimes, adversarial timing/RSS and three-archive parity; exact-byte independent review |

### Historical r3 runtime SHA256 (superseded by external review fixes)

- `jev/__init__.py`: `2e7dcf0438ffb749ff5e9eac5fd9bce7c32aa5cfd7aa7b6794a1d4b565888f17`
- `jev/__main__.py`: `89756ba09eb764b000ddef68dad022d4ec4aece99917c5d60867722dc1706e2e`
- `jev/core.py`: `586fbd41333f7764f2d01f8188a2d10f83466a4cccbb0141a4145eb397eda958`
- `jev/coverage.py`: `41784b6ee2d92eb2a60d00214193fa98b76a771258e996683ca82e5185321828`
- `jev/preparation.py`: `353b6d191e08484aab832e7703278323bcf6e52307ff4af829873309873e7797`
- `jev/registry.json`: `e7b012701835ff5f3678b70c154765228742ec00e677c1e3ec870c640663af21`
- `jev/transport.py`: `e60866e50134bd225863609a72572c1fb1c1dd04222b6d650ac671d1784afded`

## External-review remediation and final local verification (2026-10-17)

This section supersedes the historical r3 source/test hashes and uncommitted-only disposition.
The owner explicitly requested independent Claude Code + Antigravity review, verified fixes,
related tests, commit, push and a draft PR. Merge, release and shared-skill update remain excluded.

- Behavioral regressions established before corrections in `test_external_review`,
  `test_preparation_limits`, `test_report_compaction`, and `test_review_boundaries`. Synthetic
  secrets/fake transport only. Reports and raw model transcripts remain local scratch.
- Metadata-first classification and separate invocation-local scan work prevent metadata blowups
  without discarding a classified prefix. Both counters are 4,096, never reset per paragraph,
  and share the existing absolute deadline; this is an execution bound, not a language threshold.
- A 300-paragraph all-pattern fixture retained 35,401 required units (including one mechanical
  check), 1,261 validated responses and exactly 34,139 missing checks. Lossless report compaction
  reduced its JSON from 7,861,783 to 1,232,145 bytes on the pre-final runtime checkpoint. The
  final regression expands every compact record and reconciles exact missing totals.
- Final Python 3.12.2: 184 tests OK in 24.661s; Python 3.15: 184 tests OK in 24.658s.
  Logs are local `/private/tmp/008-final-r5-312.log` and `008-final-r5-315.log`.
- 1.02 MB synthetic preparation: 0.0478s / 12,353,536 incremental RSS bytes (3.12),
  0.0264s / 5,177,344 bytes (3.15). Local machine observations, not universal performance SLOs.
- Final package build/validation passed; full suite verifies exact seven-file runtime parity,
  offline prepare/no-key execution in all three extracted archives. Registry --check passes:
  55 patterns, registry and transport unchanged from main.
- Both Claude plugin validators passed. Pinned Skills CLI 1.5.20 discovery listing passed after
  sandbox DNS/cache failures were resolved using supported escalation; listing does not install.
- No live Jev call, API key discovery, shared-skill installation, merge, tag or release performed.
  External-review closure and current runtime digests follow below.

### Final reviewed runtime SHA256

- `jev/__init__.py`: `2e7dcf0438ffb749ff5e9eac5fd9bce7c32aa5cfd7aa7b6794a1d4b565888f17`
- `jev/__main__.py`: `89756ba09eb764b000ddef68dad022d4ec4aece99917c5d60867722dc1706e2e`
- `jev/core.py`: `d00c09ed40c98d4248f570bcaf9a6837a1bc8d13b7fc9e0e16e2a96458a8343f`
- `jev/coverage.py`: `b4913e87e97808415f209173446a1e66cc7575e7781e34f28340566a99405785`
- `jev/preparation.py`: `cd998a967b723e00ab13595ddb42d76782f239e450fe1a4d22ba74f99769d5a1`
- `jev/registry.json`: `e7b012701835ff5f3678b70c154765228742ec00e677c1e3ec870c640663af21`
- `jev/transport.py`: `e60866e50134bd225863609a72572c1fb1c1dd04222b6d650ac671d1784afded`
