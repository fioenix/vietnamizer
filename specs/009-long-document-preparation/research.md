# Research — feature 009

Status: design decisions, 2026-10-22. No repository runtime changes and no live evaluator calls in
this phase. Baseline: `origin/main` at `feed64d`, runner `jev-1.14.0`, segmentation profile
`vi-spans-1`.

Measurements were taken on an Apple M1 Pro with Python 3.15.0, using a throwaway prototype copy of
`jev/` in session scratch space. The prototype is not committed; its purpose was to test the design
against the full existing suite before planning. Numbers are single local measurements, not
performance guarantees. The reported private note was used only for counts and reason codes; no
source text appears here.

## R1. What a work bound has to protect

**Finding:** Pathological inputs cost about as much work per code point as ordinary notes, so the
time limit cannot be protected by a bound proportional to input length.

| Input (Markdown unless noted) | Code points | Metadata work / cp | Scan work / cp |
|---|---:|---:|---:|
| Reported private note | 48,400 | 0.06 | 0.31 |
| Synthetic long note (baseline) | 23,592 | 0.15 | 0.46 |
| ~480 short units (baseline) | 6,155 | 0.78 | 0.51 |
| `a\n` × 20,000 (paragraph-lines) | 40,000 | 3.50 | 1.50 |
| `Ab. ` × 20,000 | 80,000 | ~0 | 1.00 |
| `A. ` × 20,000 (initials) | 60,000 | ~0 | 1.00 |

Without any bound, 1 MiB of `A. ` took 2.80 s, the slowest of five worst-case shapes.
Feature 008 also runs `X. ` × 250,000 under `tracemalloc` and requires it to finish in under 2 s
(`tests/test_structure.py:47`, `tests/test_coverage_scaling.py:9`). Under tracemalloc the same
input took 0.48 s, 0.90 s, 2.01 s and 3.80 s with scan ceilings of 2¹⁴, 2¹⁵, 2¹⁶ and 2¹⁷ units.

**Consequence:** A length-scaled bound `base + k × length` has to be capped to keep those assertions.
With k = 8 and a 2¹⁵ cap, the cap governs every input above about 3,600 code points, so the length
term changes nothing for the documents this feature targets.

## R2. Work bound value and shape

**Decision:** Replace the shared 4,096 work count with one absolute bound of 32,768 (2¹⁵) units,
used separately for the metadata phase and the scan phase, as today. Do not add a length term.

**Rationale:** 2¹⁵ is the largest power of two that keeps the pathological tracemalloc case under
1 s, giving 2× margin against the 2 s assertion on slower machines. It fits the reported note (14,881
scan units) with 2.2× headroom and a synthetic 10,000-word note (47,195 code points, about 21,700
scan units). At the measured 0.31–0.46 scan units per code point, notes up to roughly 70,000–100,000
code points (about 12,000–17,000 words) prepare fully. Adversarial metadata, such as feature 008's
19,000 explicit parents, still stops because its work is quadratic.

**Alternatives considered:**
- `min(2¹⁵, 4096 + 8 × length)`, which was prototyped: same test results, more code, and no behavioural
  difference above 3,600 code points. Rejected under the constitution's rule that complexity must trace
  to an outcome.
- 2¹⁶ or larger: breaks or nearly breaks the existing 2 s tracemalloc assertions.
- Speeding up the scanner so a full 1 MiB fits in time: a different feature, with its own risk.

**Owner decision:** accepted on 2026-10-22, together with R3. This replaces the requested
"length-scaled" wording with a raised absolute bound.

### R2 addendum — charge the work that is actually done (proposed, 2026-10-22)

**Status:** proposed after T007 was blocked; accepted by the owner on 2026-10-22 and implemented as T006a.

**Finding:** T006 (`WORK_LIMIT = 32768`) left the two feature 008 tracemalloc assertions without
margin on a loaded machine (evidence.md, T007: 6 of 6 repeat runs failed at least once, full suite
`4.18 not less than 2.0`). R2's margin rested on one idle measurement (0.90 s). Profiling the
`X. ` × 250,000 case without tracemalloc (24,577 scan units, 0.36 s) shows that the bound counts
operations unevenly:

- Each initial token such as `X.` is charged 1 unit in the second token pass, but its lookahead calls
  `fullmatch` up to four more times (40,955 calls for 8,192 tokens).
- Each terminal-punctuation event is charged 1 unit, but runs three anchored matches, two `_safe`
  checks, a 64-character tail slice and up to two regex searches.

So one unit costs far more on punctuation-dense input than on prose, and a bound sized for prose
lets pathological input run 8× longer than before.

**Proposal:** keep `WORK_LIMIT = 32768` and the token allowance of a quarter of the remaining budget,
and charge:

1. one extra unit per initials lookahead step (at most four per initial token);
2. four units, instead of one, per terminal-punctuation event outside a lexical span (the
   charge falls after the `inside()` and parenthesis checks, so dots inside URLs, numbers and,
   after US2, dotted identifiers cost nothing extra).

Exhaustion still reports `preparation_limit` with the classified prefix kept. This only changes
how quickly hostile inputs reach the existing limit; no boundary decision changes.

**Measurements** (prototype of the current branch plus this change, Apple M1 Pro, Python 3.15.0,
load average 55–72; CPU seconds under tracemalloc, median of 3 interleaved rounds, so contention
affects them less than wall time):

| Input (one paragraph) | 4,096 (old) | 32,768, no charges | lookahead 1, event 2 | **lookahead 1, event 4** | lookahead 1, event 8 |
|---|---:|---:|---:|---:|---:|
| `X. ` × 250,000 | 0.123 | 0.993 | 0.226 | **0.250** | 0.228 |
| `A. ` × 330,000 | 0.121 | 1.002 | 0.235 | **0.232** | 0.247 |
| `Ab. ` × 240,000 | 0.218 | 0.931 | 0.899 | **0.746** | 0.473 |
| `1.2/3,4 ` × 120,000 | 0.065 | 0.347 | 0.363 | **0.363** | 0.359 |
| `ab.cd ` × 160,000 | 0.122 | 0.806 | 0.802 | **0.457** | 0.316 |

Scan work used by ordinary inputs, as a share of 32,768 (none reach `preparation_limit`):

| Input | No charges | Lookahead 1, event 4 | Lookahead 1, event 8 |
|---|---:|---:|---:|
| Reported private note (counts only) | 45% | 48% | 52% |
| Synthetic long note (baseline) | 33% | 36% | 41% |
| 10,000-word note (T004) | 55% | 62% | 71% |
| One paragraph of 1,500 short sentences | 46% | 60% | 78% |

A variant that also halved the token allowance (divisor 8) cut the 1,500-sentence paragraph off at
1,025 sentences, so the allowance stays as it is.

Feature 008 time tests, six repeats each in the same load window (wall time of the scaling test):

- Code at `feed64d` (4,096): 6 of 6 passed, 0.16–0.35 s.
- Proposal: 11 of 12 passed, 0.40–0.92 s; one run hit 3.33 s during a load spike.
- Full suite on the proposal: `Ran 188 tests in 130.235s`, `OK` (scaling 0.436 s).

**Why event cost 4:** the lookahead charge alone fixes the two 008 shapes (event cost 2 already gives
0.23 s). Event cost 4 also cuts punctuation-dense lowercase input (`ab.cd`) by 43%, keeps the
10,000-word note at 62% and the dense paragraph at 60%. Event cost 8 leaves only 22% headroom on the
dense paragraph for a small further gain.

**Residual risk, stated plainly:**
- The two 008 shapes now cost about 2× the old code, not 1×. On a heavily loaded machine an
  occasional run can still exceed 2 s (1 of 12 here); the old code never did in the same window.
- `Ab. ` × 240,000 stays near 0.75 s CPU under tracemalloc. Its cost comes from the 4,096-item
  inventory cap (one digest per sentence), not from work, and no feature 008 assertion covers it.
- Idle-machine figures were not re-measured; the load during this session could not be controlled.

**Rejected alternatives:**
- Lowering `WORK_LIMIT` to 16,384: the 10,000-word note needs about 18,000–20,000 scan units, so SC-002 fails.
- Halving the token allowance: breaks dense paragraphs (above).
- Speeding up the scanner (precompiled patterns, fewer slices): useful, but a larger change to
  hand-tuned code that feature 008 reviewed; it can follow separately.
- Loosening the 2 s assertions: excluded by T007 and SC-003.

**Proposed task changes if accepted:**
- New T006a [US1] after T006: a deterministic RED test in `tests/test_preparation_limits.py` that the
  charged scan work for 1,000 initial tokens (`X. `) is at least 4× that for 1,000 plain words
  (implemented: 9,995 versus 2,001 units, 4.99×; before: 3,001 versus 2,001, 1.5×); then
  add `_WorkBudget.take(amount)` and the two charges in `_scan` in `jev/preparation.py`.
- T007 unchanged, rerun after T006a; record the full suite, the six-repeat timing loop for both
  feature 008 time tests, and the load average.

## R3. Boundary rule for punctuation not followed by whitespace

**Finding:** The first draft of FR-005 (any non-uppercase character after the punctuation is not a
boundary) contradicts feature 008's segmentation contract, priority row 5: a missing space after `.`
and a lowercase continuation after a period leave the interval unresolved.

**Decision:** Keep the 008 rule, and add two narrow exemptions that cannot hide a real boundary:

1. After the punctuation run and any closing quotes or brackets, a comma, semicolon, colon or further
   terminal punctuation means the position is not a boundary. A sentence cannot begin with these.
   This covers `?",`, `!,` and `?".`.
2. Dotted ASCII identifiers are lexical tokens, like URLs and decimals: a run of ASCII letters,
   digits, `_` or `-`, then one or more `.segment` parts, each starting with a lowercase ASCII letter
   or digit, not touching another word character. This covers `so-sanh-ban-cu.md`, `example.dev` and
   `jev.core`. It does not match `Tôi về.Bạn`, `về.bạn` or `Done.Next`, which stay unresolved.

Every other case of punctuation followed directly by a letter keeps an unresolved region, now with
the reason `ambiguous_separator` instead of `unsafe_boundary` (FR-006, FR-008).

**Rationale:** The prototype passed the 54-case corpus and the four RED baseline cases. On the
reported note it left one unresolved region (`ambiguous_url_closer`, out of scope), down from five
when fully scanned under the old rules. Real Vietnamese words carry diacritics, so the ASCII-only
identifier shape rarely touches prose. The accepted trade-off is an unaccented typo such as `ve.ban`,
which becomes part of one sentence instead of an unresolved region; no text is lost.

**Alternatives considered:** the broad rule (rejected, see the finding above); a Markdown-only rule
inside link labels (does not cover `?",`, and file names occur outside links too); a host boundary
override for each case (already possible, but impractical for every file name in a technical note).

## R4. Relative link destinations

**Decision:** Treat the destination of `[label](destination)` as an opaque lexical span whatever its
scheme, when it starts directly after `](` and has no angle-bracket or quoted form. A `(` inside the
destination still sets the existing `ambiguous_url_closer` whole-unit reason, as for absolute URLs.
The rule depends on the token shape, not on the declared layout.

**Rationale:** `](` only occurs in Markdown link syntax, and paragraph-lines text can carry Markdown
links too. Keeping the existing parenthesis-ambiguity rule avoids silently guessing where a
destination ends.

## R5. Inventory cap separated from work

**Finding:** The fixed scan budget also, implicitly, limited the number of units and sentences.
`tests/test_structure.py:36` requires at most 4,096 units plus sentences.

**Decision:** Keep `MAX_INVENTORY = 4096` as an explicit counter shared by units and emitted sentence
spans, separate from the work bounds. Exceeding it produces `preparation_limit` for the remainder,
with the classified prefix kept.

**Fixtures that relied on the old bound:** `tests/test_review_boundaries.py:49`
(`test_scan_limit_keeps_classified_exact_prefix_and_context`) uses `'Tôi về. '*1100`, 1,100 sentences;
today the scan budget stops it after 513. Under the new bound it completes, so it fails. A fixture of
`'Tôi về. '*2100` would also complete (prototype: 2,100 sentences, complete). The fixture grows to
`'Tôi về. '*4200`, 4,200 sentences, which reaches the inventory cap (prototype: 4,094 sentences kept
with the fenced block, then `preparation_limit`), and keeps its assertions:
the prefix stays exact and protected text after the limit is never sent. No other existing test
changes: 183 of 184 passed on the prototype unchanged, including every time and memory assertion.

## R6. Segmentation profile version

**Decision:** Rename the profile to `vi-spans-2`. Bind the coverage manifest to the profile
constant instead of the literal string in `jev/coverage.py:23`. Update the corpus file's `profile`
field and its README, because the corpus is the acceptance seed for the profile in force. No corpus
case changes its expected spans.

**Rationale:** Sentence identities hash the profile name. R3 and R4 change boundary decisions, so
results from the two rule sets must not look comparable.

## R7. Host documentation

**Decision:** Update the limits paragraph of `references/typesafe-advisor.md` to say that each
preparation phase has an absolute work bound (not tied to paragraph count), that one invocation
inventories at most 4,096 units and sentences, and that notes of about 12,000–17,000 words or more
may still report `preparation_limit`. Name the new `ambiguous_separator` reason. Do not promise full
remote evaluation of a long document.
