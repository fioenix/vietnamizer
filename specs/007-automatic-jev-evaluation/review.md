# Independent review and PR verification — feature 007

## Authority and branch scope

Owner authorized branch separation, independent Claude Code/Antigravity reviews, finding fixes, tests and a draft PR on 2026-10-16. No merge authority.

`origin/main` was refreshed and verified at `4337469cfb8f97d12c765681cbc034ef64980bfd`. PR #9 for the old support/security branch is merged. Feature changes were committed separately and replayed onto main without modifying the old branch or including its unrelated skills.sh README section. Reviewed feature head: `e1f66d6e3772c888a7fdd288bd7b21ec4eb36e15`, the sole feature commit above that base.

The initial broad staging attempt was rejected by automatic approval review over possible unrelated README inclusion. Before retry, the exact README feature patch was verified to apply cleanly to main without that section. Staging/replay then succeeded through supported approval. No denial was bypassed.

## Independent reviewers

Both reviewers received the same exact base/head and read-only scope. Root checked the working tree remained clean through both initial reviews. Neither executed tests, modified source or called Jev.

- Claude Code 2.1.301, session `3549cd37-933b-403e-90e0-c09af020831a`, actual modelUsage `claude-opus-5-5`. Runtime/security/package focus. Five actionable findings and one unconfirmed numeric-tolerance question. The reviewer read source directly and did not independently verify Git HEAD; host bound source to the frozen commit. Package-plugin internals/distribution tests were not fully examined by this reviewer.
- Antigravity via Agybird, session `b72ccd84-e61d-4162-865e-5888d3b05859`. Spec/rubric/context/overediting focus. Six findings. Initial envelope partial because it guessed nonexistent tests/test_plugin_distribution.py. Same-session follow-up succeeded and confirmed no missing feature scope; registry read truncation was covered by the generator and canonical rules. Exact underlying model ID was unavailable; reviewer reported UI label Gemini 4 Argon (Medium), not independently verified. Adapter observed agy 1.3.3 initially and 1.4.0 on follow-up; no model/effort/credit or CLI update was performed by this task. No evidence of Agybird skill incompatibility was found, so the conditional repair of its separate repository was not triggered.

Raw responses are task-local under `/private/tmp/vietnamizer-review-007`, not a package dependency. This report summarizes findings without transcripts, private prose or credentials.

## Dispositions

| Finding | Disposition |
|---|---|
| C1 protected-string overlap and sliced fields | Fixed: primary/derived text is masked from validated source offsets; alternate unstructured context uses merged full-string intervals from original text. Placeholders are never recursively remasked. Arbitrary unmarked partial copies remain a host-classification obligation, now explicit in the contract. |
| C2 relative input path from installed root | Fixed: absolute workspace path or stdin in public examples/contracts; installed skill cache is not the input destination. |
| C3 child import injection | Fixed: child uses Python isolated mode before inserting the trusted package root; hostile-CWD import regression. |
| C4 interruption/orphan lifetime | Fixed: BaseException kills/collects child; independent worker watchdog bounds full I/O even after parent termination; stalled/drip/cancellation/watchdog tests. |
| C5 manually drifted recipe passes source gate | Fixed: source package validator runs the existing generator --check; mutated-registry fixture fails release gate. Extracted public payloads intentionally omit generator tooling. |
| A1 inline protection suppresses editable target/paragraph/T3 | Fixed: mixed targets are masked, empty editable targets excluded; paragraph/document checks depend on their own editable scope. |
| A2 short-token placeholder/prose corruption | Fixed with C1: primary spans are authoritative and fallback literals are not scanned as user text. Repeated unmarked prose stays intact; related context still requires host redaction and conservative full-string masking. |
| A3 mismatched/low quotation and unclosed cross-paragraph state | Fixed: mismatched closing cues and low quotes are visible, unclosed stack flushes at paragraph boundaries while document style observations persist; valid nested fixture retained. Mechanical findings still need canonical exception review. |
| A4 ambiguous Choice labels | Clarified six recipes with explicit target-function/source-support criteria, legitimate genre/topic focus, complete-clause/fragment and intentional capitalization outcomes. Noul independently judges defects; a function label alone never authorizes an edit. No language-accuracy claim from this change. |
| A5 deadline category and partial judgments | Deadline expiry between batches now reports deadline_exceeded. Retaining already validated partial judgments is intentional under US3.3/FR-030; each now exposes coverage_status and host must inspect coverage. Atomic grouping/removal of valid raw evidence was not adopted; Score without evidence remains ignored. |
| A6 README version/manual copy and terms | Fixed current version, include jev/ in manual copy, align terms with automatic permitted evaluation; source validator also checks README current-version statement. |

Unconfirmed numeric-tolerance concern: no evidence justifies widening validation or retrospectively diagnosing the old invalid_response. Score's weighted-position contract was checked against primary TypeSafe documentation earlier in this task. Keep strict validation and safe diagnostic reasons; no favorable reroll or threshold claim.

## Verification in progress

Behavioral regressions observed RED before fixes: overlapping/short-token masks, protected-target scope, mismatched quotes, recipe drift, hostile-CWD import, interruption cleanup and worker self-deadline. Deterministic old-code probe confirmed between-section expiry previously returned limit_exceeded. Focused current runtime/transport/security tests pass; final full suite, archives, re-review binding and PR state follow below.

## Second review checkpoint and authoritative rendering boundary

On 79666a8, Antigravity's targeted re-review returned success/clean for A1–A6. Claude Code accepted C2–C5 but identified a real C1 regression: a protected value newly inserted by a candidate was masked in replacement but not in revised_paragraph. It also found candidate coverage annotated with a generic label and the source recipe gate silently skipped when its generator was missing.

Before another privacy correction, the host recorded the rendering authority: primary offsets classify original text; one protected-match function classifies every replacement/secondary field; revised paragraphs combine translated original spans with those same replacement-match spans. No downstream string replacement or independent mask state is introduced. A deterministic candidate fixture reproduced the leak before this correction. A preexisting manual [PROTECTED] marker fixture also reproduced remasking of marker characters; the shared matcher now excludes reserved markers. Candidate status is bound by the actual planning coverage key, including IDs with underscores. Source mode now requires the generator, while extracted payload validation still exits through its separate mode.

All four added regressions were observed RED before their corresponding fixes. This checkpoint replaces the earlier provisional clean assertion for C1; final verification follows.

## Sentinel containment checkpoint

Claude's narrow re-review of 8165f14 closed R1/R2/R3 and found N1: excluding every match that intersects an existing marker also excludes a larger protected value enclosing that marker. Before a third correction of the masking invariant, the host paused and fixed the authoritative rule: only matches wholly contained in a reserved marker may be ignored; enclosing/crossing protected intervals remain classified as data and must be masked. This is interval containment, not a new heuristic or second redaction state. A fixture with editable prose plus a protected value enclosing a marker reproduced the leak in both context and candidate-derived fields. Source/replacement masking still share one matcher and one renderer. No policy/model/permission change is involved.

## Final closure and verification

- Runtime/test revision: `1e98639e512ac6e47669868708867dd338e03b4f`. Claude Code confirmed R1/R2/R3 closed at 8165f14 and N1 closed at 1e98639, with no new regression in the narrow inspected changes. Antigravity's A1–A6/rubric re-review was clean at 79666a8; no subsequent recipe or transport change invalidates that evidence. Later commits update only this report and task dispositions, not runtime bytes.
- Python 3.12: full discovery 86 tests, OK, 19.225 seconds. Python 3.15: full discovery 86 tests, OK, 19.713 seconds. No code changed after those runs.
- Registry check: all 55 definitions source-bound. Source validator and plugin packaging passed; mutated-recipe and missing-generator gates are tested.
- Final archives separately extracted under `/private/tmp/vietnamizer-final-c84c13fh`: 15/15 runtime file comparisons equal source, and all three no-key CLI runs succeeded. Skills 1.5.20 listing and both Claude plugin validation commands passed.
- Live transport smoke ran the extracted plugin at 79666a8, actual jev-1.14.0: evaluated; 47 semantic + one local mechanical + seven inactive-profile exclusions; 32,870 input and 5,089 output tokens. CLI wall time was 8.67 seconds via /usr/bin/time. Billed currency cost was not available.
- After the candidate/sentinel corrections, a deterministic current-run payload capture exactly matched every HTTP request digest from that validated smoke. The transport bytes are unchanged. This reuses equivalent transport evidence; it is not claimed as a new live invocation of the last archive. Protected/candidate paths are verified with offline wire-capture regressions rather than exporting private data.
- Scoped committed diff hygiene passed and git tracked-ignored check was empty. Reviewers did not modify the repository. No shared skill installation or release was performed.

Final runtime SHA-256:

```text
jev/__init__.py 2e7dcf0438ffb749ff5e9eac5fd9bce7c32aa5cfd7aa7b6794a1d4b565888f17
jev/__main__.py 56473ef75379687509b2f33f7fc36e2daf5355000cd18f9469b98a8b0b564676
jev/core.py 904214ced286db872fe200a98f6e91b614ff2b5436c6df380e9b3a1670629778
jev/transport.py e60866e50134bd225863609a72572c1fb1c1dd04222b6d650ac671d1784afded
jev/registry.json e7b012701835ff5f3678b70c154765228742ec00e677c1e3ec870c640663af21
```

Final archive SHA-256:

```text
vietnamizer.skill 067ca022356dad8f01cd658fc626e009eb498ce99cdb49d1b75a12648a3b807d
vietnamizer-claude-org.zip ce7669d6594797aa21bb675ddd7662c7941b9eafac51fcd6a38d037d19e6d431
vietnamizer-plugin.zip 1f3fa42d7f0a111c334a68319d9d633d99eda42c2f5926dc8abb8cdc0c79d9ca
```

## Draft PR delivery

PR: https://github.com/fioenix/vietnamizer/pull/11

Observed at creation: OPEN, isDraft=true, base main, head codex/007-automatic-jev-evaluation at 1e98639e512ac6e47669868708867dd338e03b4f. Attached to this Codex task. GitHub validate was IN_PROGRESS at that observation; no pass is inferred from local tests. The final chat handoff separately reports the observed check status after pushing this evidence-only commit. No merge was requested or performed.

All owner-authorized branch/review/fix/test/draft-PR tasks are complete. Vietnamese holdout calibration, actual client UI invocation across hosts, shared installation/release and recovering the historical invalid_response field remain explicitly unproven or out of scope.
