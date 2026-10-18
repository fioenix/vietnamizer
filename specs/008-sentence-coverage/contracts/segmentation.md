# Segmentation contract — proposed profile `vi-spans-1`

Design only. This is a conservative source-preserving profile, not UAX #29 conformance or a
claim that Vietnamese punctuation has no ambiguity. A lexical rule is a segmentation aid, not
an editing pattern or a claim about grammatical correctness.

## Coordinates and invariant

Offsets are half-open Python Unicode-code-point positions in the decoded source string, never
UTF-8 byte or JavaScript UTF-16 indexes. Keep original text, CR/LF sequences and combining marks;
no Unicode normalization. Offsets cannot split CRLF, a base/combining-mark sequence, a recognized
emoji sequence or a protected token. Source identity binds exact UTF-8 encoding of that string,
not the JSON file's choice of escapes. Host-provided offsets are validated before use.

Ordered disjoint source regions plus separator spans must cover `[0, len(source))` exactly.
Parent spans may contain children; siblings cannot overlap. Repeated words at other positions
have different occurrence identities. Sentence spans exclude surrounding separator whitespace
but include terminal punctuation and attached closing quotes/brackets. Openers belong to the
following sentence. All preserved separators are independently recoverable.

## Structural pass, before sentence boundaries

1. Apply explicit valid paragraph boundaries, structure annotations and protection first. Reject
   crossing/overlapping incompatible annotations rather than guessing. An annotation cannot shrink
   a protected region or change source text. Explicit blocks and scanner blocks must reconcile.
2. `paragraph-lines`: every nonblank physical line is a parent prose paragraph unless host structural
   annotations say otherwise. Blank lines and line endings remain source separators. A physically
   hard-wrapped article must declare paragraph-span overrides or use Markdown layout; do not infer
   that a newline is a soft wrap because a sentence seems unfinished.
3. `markdown`: recognize blank-line paragraph boundaries, ATX headings, fenced code, blockquote
   markers, bullet/numbered item boundaries and their indented continuation lines. Ordinary single
   line breaks remain inside a paragraph. A list-item paragraph retains its enclosing list and lead-in
   heading as context. Blockquote text is not automatically protected unless host genre/protection
   requires it. Sentence text is an exact source slice, including markup inside that slice.
4. Tables and unsupported HTML/Markdown blocks are recorded as structural units. Default to
   typography-only checks when host allows that genre; ambiguous block boundaries are unresolved.
   Do not silently parse table delimiters as sentence prose or flatten cells into invented sentences.
5. Fenced/inline code and host-protected spans are opaque to punctuation scanning. A fully protected
   unit is excluded; a partly protected prose sentence is still inventoried using surrounding
   boundaries. If a sentence endpoint lies inside opaque protected content, retain a boundary-unresolved
   region instead of exposing or guessing protected punctuation. No re-segmentation after redaction.
6. Headings and punctuation-free structural fragments remain units with their applicable scoped
   checks; they are not silently dropped or counted as ordinary prose sentences. A punctuation-free
   prose paragraph/list item has one trailing sentence/fragment target.

## Sentence pass, ordered precedence

Scan each editable prose parent from left to right. Use original spans and bounded lexical
recognizers, avoiding catastrophic regex backtracking. Boundary overrides from the host must cite
source binding and cannot cross the parent or protected token interiors.

| Priority | Condition | Disposition |
|---|---|---|
| 1 | Inside an opaque span or recognized URL/email, date, decimal/version or list ordinal | Do not use internal punctuation as a sentence boundary. A URL recognizer excludes an unattached trailing sentence period/closer. Ambiguous trailing punctuation becomes unresolved. |
| 2 | Recognized nonterminal abbreviation followed by its expected continuation | Suppress that boundary; preserve characters. Initial inventory includes `TS.`, `ThS.`, `PGS.`, `GS.`, `TP.` before a name; multi-period forms such as `TP.HCM` are one lexical span. `v.v.`/`v.d.` at a possible sentence end are ambiguous unless an explicit rule/override resolves them. |
| 3 | Initials such as `N. V. An` | Retain the recognized name span. An initial without a determinate continuation stays unresolved. |
| 4 | A run of `...` or `…` inside prose | Do not treat every dot as an endpoint. Internal ellipsis between continuing words is nonterminal; ellipsis at parent end closes the trailing target. An ellipsis before a potentially new sentence is unresolved unless overridden. |
| 5 | `.`, `!`, `?` or their mixed repeated runs outside the above exclusions | Propose one boundary after the full punctuation run and immediately attached closing delimiters. A missing space after `.`, a lowercase continuation after a period, unmatched delimiters or quoted attribution ambiguity leaves the affected interval unresolved. `!`/`?` may precede a lowercase new sentence unless a recognized quote-attribution continuation applies. |
| 6 | Quoted speech with attribution, e.g. `"Xong chưa?" cô hỏi.` | Keep the lowercase attribution in the same sentence. Do not suppress every boundary inside quotes: `"Đi thôi. Trễ rồi."` contains two sentences. Nested quote closers attach to the preceding sentence. Punctuation inside parentheses that could separate independent sentences is unresolved unless a documented fixture rule/override resolves it. |
| 7 | Clear terminal punctuation plus whitespace and a new sentence candidate | Accept the boundary. Uppercase is supporting evidence, not sufficient to override abbreviation/token rules and not a universal sentence requirement. |
| 8 | Nonempty remainder at parent end | Emit one target, even without terminal punctuation. If earlier unresolved boundary candidates occur inside it, label the region unresolved rather than certifying one sentence. |

Keep accepted boundaries on either side of a minimal ambiguous region; retain all text in that
region and its candidate boundary positions with reasons. Never call an uncertain merged region
an exact sentence. Its safe provisional checks, if any, cannot satisfy sentence coverage. Host
boundary overrides can resolve it before evaluation; source/context bindings then change.

The abbreviation list is explicit, case-sensitive and versioned with the profile. Any addition
needs an annotated positive and a contrast case; it cannot be borrowed as a grammar rule.

## Required reference cases

All examples below are synthetic. Expected boundaries are an acceptance corpus seed, not proof
of general language accuracy. Add independent contrast cases before implementation acceptance.

| Source | Expected |
|---|---|
| `Tôi về. Bạn ở lại.` | Two sentences. |
| `Tôi về.\r\nBạn ở lại.` | Two parents in paragraph-lines; one parent/two sentences in Markdown; preserve CRLF. |
| `TS. Lan đã đến. Cuộc họp bắt đầu.` | Two sentences; no split after `TS.`. |
| `Tỷ lệ là 99,17%. Số lượng là 1.000 người.` | Two sentences; preserve decimal/thousands tokens. |
| `Bản 1.14.0 chạy từ 16/10/2026. Đã xong.` | Two sentences. |
| `Xem https://example.org/a.b. Đọc tiếp.` | Two sentences; URL excludes terminal period. |
| `Tôi... chưa biết.` | One sentence. |
| `Tôi chưa biết… Có lẽ mai.` | Unresolved ellipsis boundary; no false exact-sentence success. |
| `Anh nói: "Đi thôi. Trễ rồi."` | Two sentences with exact source slices; closing quote on second. |
| `"Xong chưa?" cô hỏi.` | One sentence. |
| `Được?! Đi thôi!` | Two sentences; mixed punctuation stays attached. |
| `Tôi về` | One trailing target. |
| `Danh sách gồm A, B, v.v. Hôm nay chốt.` | Unresolved abbreviation/end boundary until host override. |
| A list item wrapping onto indented continuation lines | One logical item parent; split sentences within it, preserve markers/line breaks. |
| A decomposed Vietnamese vowel or emoji adjacent to punctuation | Identical source reconstruction and no endpoint inside its character sequence. |

Corpus acceptance distinguishes exact boundary precision/recall, unresolved-region rate, parent
accuracy and reconstruction equality. SC-001 requires every reference case designated resolvable
for the approved profile to match exactly; reference-unresolved cases must stay unresolved or be
resolved through validated host overrides. Do not remove failing cases from the corpus to claim
success. Record annotations and profile revisions independently from heuristic tuning.

## Implemented local work bound

The implementation uses separate invocation-local `_WorkBudget(4096)` counters for metadata
classification and sentence scanning. Complete structural/protection/context classification precedes
scanning; the scanner counter is shared across lexical recognition and boundary/emission work. This is an execution safety bound, not a linguistic
threshold. A token lexer visits nonwhitespace chunks once; marker-conditional anchored recognizers
and at most four initial/name tokens avoid repeated full-suffix regex searches. Deadline checks
cover both lexical and boundary phases. Work exhaustion preserves exact source partition plus an
unresolved/unprocessed remainder; it does not certify that all sentences in that region were found.

Review hardening adds a separate metadata work budget under the same absolute deadline for validation, annotation
intersection/overlay, inventories and context construction before scanning. Exhaustion before complete
classification returns the exact whole source as unprocessed, with zero scheduled transmission;
it never bypasses annotations to evaluate a partially classified source. Fences cannot be
made editable by a paragraph/kind annotation. Inline backtick spans match equal-length delimiter
runs across soft line breaks; unmatched openers protect the remainder and remain unresolved.
Overrides resolve their own endpoint only; unrelated ambiguity and whole-parent uncertainty
remain. All automatic endpoints must preserve Unicode character sequences, and missing
separators after any terminal punctuation remain uncertain. Occurrence identities bind the
actual UTF-8 source digest, structural role, coordinates, profile and override set.

The lexer reserves scan work for recognition and boundary emission. Token exhaustion stops
recognition at a known prefix; only that prefix can produce exact sentences, and the remaining
source is unresolved. Classification and scan counters never reset per paragraph.
