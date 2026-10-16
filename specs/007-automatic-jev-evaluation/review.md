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
