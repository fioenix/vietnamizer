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
