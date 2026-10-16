# Independent code/security review — feature 008

Scope: immutable local source, tests, approved spec/plan/contracts and package consumers. Review
performed by a separate Codex subagent using inherited runtime settings; no hard model override
or provider identity claim. This was manual code/security review with bounded offline repros,
not a formal Codex Security scanner run, live Jev assessment or publication approval.

## Artifact bindings

| Pass | Snapshot | Manifest SHA256 | Disposition |
|---|---|---|---|
| Initial | local frozen source snapshot | `2f0060d80fbdf515d0a5ad6ac85c8aebf0984294ff8b5a3442ba239073877754` | Three reproduced findings |
| r2 | fixes plus targeted tests | `d8a0b25d6eb4ffadebe4715286d6e88e7b49005cb8ffb37383e70dd111436c94` | F1/F3 closed; selected metadata path still open |
| r3 | source-bound selected identity delta | `33e8fce8194ac37cfcaef0ac87bf768f965a19cfd787deb4f899e23cf5f64fa2` | All findings closed; no new blocker in delta |

Snapshots are local scratch under `/private/tmp`, not public deliverables. Runtime hashes in
`evidence.md` bind the delivered working source; historical snapshot line numbers are not presented
as current source locations. Parent verified findings before fixing them and ran regression tests.

## Findings and closure

| ID | Severity | Failure | Correction / evidence | State |
|---|---|---|---|---|
| F1 | P1 | Supplied alias can equal another auto sentence ID, bind a check to the wrong target and falsely certify completion; V1 diagnostic can crash | Full sentence occurrence IDs always source-derived; supplied IDs are separate aliases. Independent full repro returns distinct IDs and 82/82 checks per sentence; no mismatched target mapping | CLOSED |
| F2 | P1 | Protected source value can recur in context ID/role, then selected target IDs, and reach wire/output despite prose redaction | Context ID hash, shared role redaction; protected host identifiers centralized; every full/selected target gets a source-derived identity before alias reporting. Independent r3 repro verifies no protected value in full/selected wire or output, stable diagnostic identity after alias rename, and safe wholly protected exclusion | CLOSED |
| F3 | P2 | Eager revised-paragraph copy for every candidate causes large allocations before even checking an impossible shared state | Shared-state byte preflight before candidates, lazy per-batch candidate projection, constant-time numeric-review lookup. Independent 400-candidate repro peak fell from 41,677,393 to 1,387,536 traced bytes with zero requests and truthful `context_too_large` | CLOSED |

Original failures and subsequent assertion-based regressions are recorded in evidence.md. The
metadata protection issue required a provenance checkpoint after field-level corrections left
selected mode red. The final architecture separates source identities from supplied aliases.

## Prior local review acceptance and limits

At the historical r3 checkpoint, no blocking finding remained in the reviewed scope. Runtime source/test bytes at r3 are the reviewed
bytes; documentation/evidence status updates afterward do not change executable behavior. Parent
owns final suite, archive and contract checks. Review does not establish semantic quality, absence
of every vulnerability, safe handling of all possible languages/markup or remote provider readiness.
No network/evaluator calls, user-owned thread messages, shared installs, commits, pushes, merges,
tags or releases were performed by the reviewer.

## External-review architecture checkpoint (2026-10-17, in progress)

Both independent reviewers found concrete additional cases after the historical r3 checkpoint.
The metadata work guard initially shared the scanner counter; later context construction could
throw away a safely classified source after scanning exhausted it. Before another local guard,
the owning boundary is now explicit: complete structure/protection/context classification first
under one invocation-local 4,096-operation metadata budget, then scan sentences under a separate
invocation-local 4,096-operation scan budget. Neither resets per parent; both share the original
absolute deadline. Classification failure leaves the whole source unknown and sends nothing;
scan exhaustion preserves classified parents/context, exact prefix and unresolved remainder.
This corrects local execution accounting, not API quotas or linguistic thresholds.

### External reviewers and immutable snapshots

| Pass | Snapshot manifest SHA256 | Reviewer evidence | Result |
|---|---|---|---|
| External initial | `1341f7e4df6260cf9ba45abe0a278e45b3e373f1bf7cfae2bd4fe4310df8a8e1` | Claude Code 2.1.301, session `c3cbe44c-07ec-4609-9a81-ea57038fc1e9`; observed modelUsage `claude-opus-5-5` | Blocking cases reproduced by parent before fixes |
| External initial | same snapshot | Antigravity CLI 1.4.0 via Agybird, conversation `d6d605db-9c45-47bc-b4a9-897f848ca283` | Static independent discovery; parent verified actionable cases |
| External r2 | `dee48d3ba43ca8fe06e3002369f34c2726279eb8852032ecb375d86ae04f8a81` | Same sessions, independently resumed | Antigravity reported no blocker plus residual suggestions; Claude identified a preparation regression and privacy/over-redaction edge cases |
| External r3 | `f65bb7f6ed05b588655b616b72e48b62ad9313e161d451492e2efccf571052b7` | Same sessions, bounded final-delta review | Both reported no blocker in delta; Claude residual escaped multi-run privacy case fixed and re-reviewed below |

Antigravity was used through the installed Agybird skill without model, effort, sandbox,
credit or permission overrides. An optional Python command was permission-blocked; it was
not granted, and the reviewer continued static inspection. Its underlying model ID was not
independently established. Claude's initial long-running adversarial repro was terminated by
parent after over three minutes; bounded parent subprocess tests now verify that input in seconds.
Claude's r2 used read-only shell commands despite a no-command instruction; no Python repro or
source change occurred in that pass. Snapshot source digests were verified unchanged. Reports
are review evidence, not test receipts, formal security-scanner output or live Jev validation.

### Verified finding dispositions

| Group | Correction and regression evidence | Disposition |
|---|---|---|
| Fenced/inline code can leak through annotation, unequal backticks, soft wraps, escapes or unclosed code | Immutable fence protection, equal-length run parser with escaped-opener handling; `test_external_review`, `test_review_boundaries` | Fixed |
| Unclassified tails/oversized metadata escape local work/deadline limits | Metadata-first classification; unknown source never transmitted; linked unknown context rejected; 19,000-annotation watchdog tests | Fixed |
| Scan exhaustion discards classified source | Separate global classification/scan counters, lexer reserves boundary work; 2,200-token classified-prefix regression | Fixed |
| Unrelated overrides erase ambiguity; ellipsis/Unicode/absent separators falsely certify sentences | Preserve whole-parent/earlier uncertainty, safe endpoints and nonlowercase ellipsis continuations | Fixed |
| Context flags ignore missing evidence, unsendable state, unreviewed mechanical-only scope | Explicit evidence-role and host-review gates; separate source/answer/context completion | Fixed |
| Empty selected input and unrelated structural work; distant protection disappears | Require explicit legacy targets, schedule only selected parents, preserve full protection inventory and source context before filtering | Fixed |
| Short secret corrupts generated enums/source context or revised prose; candidate seam recreates protected content | Span-backed source rendering, stable generated roles, bounded matching cache, replacement-overlap seam protection | Fixed |
| Source occurrence ID lacks actual source bytes; non-sentence aliases disappear | Source digest/role-bound IDs; explicit supplemental diagnostic disposition | Fixed |
| Generic halt overwrites specific permission/context reason | Preserve first block reason; permission checked before generic context gap | Fixed |
| Large output/validation-key accounting duplicates work | Lossless `templates-v1`, exact expansion/count tests; validated keys indexed by group | Fixed |
| Parenthesis continuations, Markdown links and quoted title false abstentions | Update delimiter depth before continuation; bounded link destination/title recognizers | Fixed |
| Quoted initials, Markdown emphasis closers, ambiguous parenthesized URL endings | Retain conservative abstention; outside the verified resolvable corpus; never credited as exact completion | Documented non-blocking profile limits |
| Typical long article cannot finish within existing API budget | Preserve truthful missing checks; no quota increase, chained calls or auto retry | Accepted existing contract limit |

Offline coverage and typed-response tests do not establish live Vietnamese judgment quality.
All five host editing safeguards and existing API quotas remain authoritative.

### Final closure

Claude's R4 reviewed only the final escaped-multi-run patch, SHA256
`4264ddffcd35cd5cd48cf616d0698b9193b707a7f9ab5031bf1594d1fd741e12`,
and closed that reproduced privacy case with no regression in changed lines. Its R3 findings
remain closed. Antigravity R3 completed successfully in the same conversation with
`session_resumed:true`, no permission requests and no blocking correctness/security findings.
The final single-parser delta was independently reviewed by Claude; Antigravity's verdict binds
the preceding R3 snapshot. Parent reran all offline tests and package checks on final bytes.
No unresolved blocking finding remains in the reviewed scope. Conservative profile limits and
live semantic calibration are explicit limits, not failed checks silently waived.
