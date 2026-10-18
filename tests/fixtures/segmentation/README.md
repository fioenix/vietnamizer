# Independent synthetic segmentation corpus

`cases.json` is an annotated acceptance seed for `vi-spans-1`, authored on 2026-10-16
from `specs/008-sentence-coverage/contracts/segmentation.md`. It contains 54 cases:
42 designated resolvable and 12 deliberately unresolved. The ellipsis override case is
resolvable only with its supplied source-bound override. This is synthetic editorial
prose, not an exported user article or a sample of Vietnamese usage frequencies.

## Annotation procedure and independence

The fixture author read the segmentation contract, wrote contrast examples and selected
intended source slices before consulting or running any scanner. An authoring helper
used Python substring lookup to calculate offsets from those chosen phrases. It did
not predict boundaries or import runtime code. Repeated phrases use increasing lookup
positions, so identical text at different positions has distinct source coordinates.
The helper checked span bounds, ordering and sentence containment; structural slices
were also read back manually. These checks establish annotation consistency only.

An independent annotation check is still required before acceptance. The parent reviewer
must check these intended slices against the contract without treating scanner output
as an oracle. No claim of completed second annotation or measured boundary accuracy is
made here. In particular, `abbreviation-no-continuation`, `url-ambiguous-closer` and
`protected-endpoint-unresolved` are deliberately conservative contrast labels for review;
if the contract does not settle them, record a disagreement rather than silently changing
labels to fit a scanner. Any adjudication must record its reason in the case and this
file. Never delete a failing case to improve a reported score.

## Schema

The root contains `version: "1"`, `profile`, `provenance` and `cases`. Every case has
`id`, original `text`, `layout`, `sentences`, `parents` and `unresolved`.

- Every span is `[start, end]`, half-open, in Python Unicode code points of the exact
  decoded `text`. Keep CRLF, decomposed accents, emoji and whitespace unchanged.
- `parents` inventories only prose/list/blockquote parents. Structural-only regions are
  listed separately in `structural_units`; their absence from `parents` does not authorize
  dropping source text. Separators are the original complement of these spans.
- `sentences` contains only certified sentence/fragment slices, including list or quote
  markers present at that location. Exclude surrounding separator whitespace. A fragment
  without punctuation remains a target.
- `unresolved_regions` records exact intervals that must not count as certified sentences.
  They coexist with independently clear sentence spans in `ellipsis-minimal-region`.
  `reason` describes why host resolution is needed.
- `structural_units` records `kind` and exact `span`; headings, code and table blocks are
  not ordinary prose sentences. A code span ends after its closing fence, before the newline.
- `protected_spans` supplies host-opaque intervals; it is annotation input, not scanner
  output. Sentence inventory must not reveal punctuation inside protected content.
- Optional `boundary_overrides` uses the concrete CLI schema: a list of integer,
  half-open sentence endpoints in the exact source. For `ellipsis-override-two`,
  `len("Tôi chưa biết…") == 14`; `[14]` splits immediately after the ellipsis.
  `boundary_override_reason` records the host annotation rationale; runtime source
  identity must still bind the exact UTF-8 source before applying the override.

The sentence fixtures cover all required reference examples and contrasts: abbreviation
continuations and ambiguous endings, initials, decimals/thousands, versions/dates,
URL/email punctuation, internal/final/ambiguous ellipsis, source-bound override,
quotation attribution, multi-sentence dialogue, nested closers, repeated/mixed punctuation,
lowercase and missing-space ambiguity, unmatched delimiters and trailing fragments.
Structure fixtures contrast physical-line parents with Markdown wrapping, blank lines,
list continuations, ordered lists, headings, code, blockquotes and tables. Character
fixtures preserve decomposed Vietnamese vowels, CRLF, emoji modifiers, ZWJ families
and regional-indicator flags.

## Limits

These 54 cases are small, contract-derived and not a blind real-world holdout. Their
pass rate cannot establish Vietnamese boundary precision/recall on general text,
Jev judgment quality, editing quality or authorship. Future held-out corpus expansion
and independent annotation remain separate work. This corpus does not certify a
lexical or grammatical rule about Vietnamese.

Parent annotation review (2026-10-16): original source and intended slices for all 54 cases were
reviewed independently of scanner output. The three conservative unresolved labels above are
accepted for this bounded profile; they are not claims that a human cannot interpret the text.

## Annotation correction

The ellipsis override initially used an annotation object with offset 13, the index
of the ellipsis character. Independent exact-slice verification corrected this to
the CLI integer endpoint `[14]`, matching the already annotated first sentence
span `[0, 14]`. This correction used Python string length and source slicing only,
without scanner output. Other labels were unchanged.
