# Research: Structural exclusions and the T4 sign gate

Measurements were taken on branch `codex/011-structural-exclusions` at `2670959` (runner
`jev-1.14.0`, profile `vi-spans-2`). The label–value fixtures are synthetic and were written and
labeled in this session by the agent, not by a native-speaker annotator; they are evidence for the
rule's shape, not for its accuracy on real notes.

## R1. Which patterns exclude which structure

**Decision**: Classify each canonical **Không flag** mention by whether it excludes the structure as
a whole (FR-006):

| Pattern | Canonical phrase | Heading | Label–value line |
|---|---|---|---|
| V2 | "tít, sapo" | excluded | — |
| V3 | "Không áp dụng pattern này cho tiêu đề, nhãn, mục lục hoặc ô bảng" | excluded | — (names labels, not label–value lines) |
| V5 | "tiêu đề, bảng biểu" | excluded | — |
| V6 | "tiêu đề dạng câu hỏi" | — (one form only) | — |
| V14 | "tít, sapo, chú thích ảnh, nhãn nút, mục lục, ô bảng, checklist" | excluded | — (button labels only) |
| V20 | "riêng với dòng liệt kê và nhãn, đọc mục … trước khi bỏ qua" | — | — (explicitly keeps checking) |
| T5 | "nhãn–giá trị (*Trạng thái: đang xử lý*)" | — (targets headings) | — (see below) |
| T6 | "bảng" (emoji with meaning) | — (targets headings) | — |
| V11 (after User Story 3) | new phrase, owner decision Q1: B | excluded | excluded |

T5 is not excluded from label–value lines even though its **Không flag** names them. T5's error
form is itself a label line (`- **Hiệu quả vận hành:** …`); telling a real label–value line from a
decorative label is T5's semantic question. Excluding it would remove the pattern's whole subject,
so T5 counts as a pattern that targets the structure (FR-009).

**Consequence**: before User Story 3, the label–value structure excludes nothing; after it, only V11.
Headings lose V2, V3, V5 and V14 now, and V11 after User Story 3.

**Measured effect** (synthetic ~1,000-word note: 70 units, 10 headings, 80 sentences, no `, và`):
heading exclusions remove 10 × (2 + 2 + 2 + 2) = 80 checks, V11 on headings and on the 30 label
bullets of the template (three per section, in field lists) another 10 × 3 + 30 × 3 = 120, and the
T4 gate 90 subjects × 2 = 180; about 380 of 7,381 checks (5.1%), computed from registry recipe
counts, not yet measured on an implementation. The feature's value is removing questions with a known answer, not cost.

**Alternatives considered**: excluding every pattern that mentions a structure. Rejected: V6, V20,
T5 and T6 would lose checks their own text keeps.

## R2. Exclusions and the gate are generated into the registry

**Decision**: `scripts/build-jev-registry.py` holds a small table: for each excluded
(pattern, structure) pair, the canonical phrase from the table in R1; for T4, the gate expression
`,\s+và\s`. The generator writes `excluded_structures` and `gate` into the pattern's registry entry
and fails `--check` when a quoted phrase no longer appears in that pattern's **Không flag** (or, for
the gate, in T4's **Dấu hiệu**) or when the registry differs. This satisfies FR-003 and FR-007.

**Alternatives considered**: parse **Không flag** text automatically. Rejected: R1 shows the same
words mean different scopes (V3 "nhãn" vs T5 "nhãn–giá trị"; V6 one form of title), so a parser
would encode the misreadings R1 avoids.

## R3. Label–value recognition without an untested threshold

**Decision**: Recognize a label–value line only from explicit structure:

1. a bold label at the start of a list item or line: `**Nhãn:** giá trị` or `**Nhãn**: giá trị`; or
2. a plain label `Nhãn: giá trị` at the start of a list item, when the item belongs to a run of at
   least two adjacent items of the same list that all have the plain or bold label form.

A plain label is text before the first `: ` with letters and spaces only (no digits, comma,
terminal punctuation, link, code or emphasis), followed by a non-empty value. Everything else,
including a single plain `Nhãn: giá trị` paragraph, is prose (FR-005). The structure covers the
item's first sentence only.

**Measured alternatives** (prototype `label011.py`, synthetic dev and holdout sets of 20 label–value
and 20 prose or lead-in lines each):

| Rule | Dev recall | Dev false | Holdout recall | Holdout false |
|---|---|---|---|---|
| plain label ≤ 2 syllables + lead-in word list | 17/20 | 0/20 | 14/20 | 1/20 |
| plain label ≤ 3 syllables + list | 19/20 | 0/20 | 20/20 | 2/20 |
| plain label ≤ 4 syllables + list | 20/20 | 0/20 | 20/20 | 2/20 |
| plain label ≤ 5 syllables + list | 20/20 | 4/20 | 20/20 | 2/20 |

Rejected: every cap produced false recognitions on prose (`Vậy thì sao: …`, `Kết luận: tao sai.`,
`Lý do rất đơn giản: …`), and the holdout is not independent: the lead-in word list was written
with the holdout lines in view. A syllable cap tuned this way is the untested numeric threshold
that the constitution (principle IV) and `AGENTS.md` forbid. The adopted rule has no tunable
number; "at least two adjacent items" is what makes a list of fields.

**Trade-off and spec deviation (accepted by the owner on 2026-10-22)**: the conservative rule does not recognize
a lone plain line. Spec User Story 2 scenario 2 (`Trạng thái: đang xử lý` alone) and SC-001 (the
date line) assume it would. Proposed: scenario 2 and SC-001 use the forms R3 recognizes (bold label,
or a plain label inside a field list such as `- Ngày: 22/10/2026 (Asia/Ho_Chi_Minh)` followed by
`- Người viết: Fio`). A lone plain line keeps its V11 question and relies on V11's new rule text,
which the model receives. Whether the private note's date line sat in such a list is unknown here;
the owner can check it without sharing the note. SC-003 is then measured on fixtures in the forms
R3 accepts, plus lone plain lines and prose that must not be recognized.

## R4. Applying exclusions per subject

**Decision**: Today every target pattern in a section shares one subject list
(`jev/coverage.py:28–31`, and `Ledger.checks` assumes equal counts). Each pattern group gets its own
subject list, filtered by the T4 gate and by structure; excluded subjects are kept on the coverage
entry as `excluded_subjects: [{subject, reason, structure?}]`. A group whose subjects are all excluded
becomes `status: excluded` with reason `sign_absent` or `structure_excluded`. Per-sentence
`required` counts in the report become per-subject sums over the groups that include the subject.
Exclusions apply to pattern groups only; candidate review groups are unchanged (FR-008).

The T4 gate reads the subject's editable text (protected spans blanked), the same text a request
would carry, so `, và` inside code or a protected span never opens T4. The gate matches on
`unicodedata.normalize("NFC", text)`: the runner keeps source text unnormalized for exact offsets,
and on decomposed *và* (NFD) the raw expression does not match (checked at `2670959`:
`re.search(r',\s+và\s', normalize('NFD', 'A, và B'))` is `None`), which would silently drop real T4
checks (analysis finding F2). Normalization affects only the gate decision, never offsets or
requests.

**Rationale**: excluded checks must stay enumerable (FR-013) and must not count as required
(FR-002, FR-008). Filtering subjects removes only questions; request state is unchanged (FR-014).

## R5. Rule maintenance order

**Decision**: In User Story 3, first add the `calibration/LOG.md` entry (synthetic before text
equivalent to the private H1 and date line, observed scores, V11, classification "pattern sửa nhầm",
decision; the four structures beyond titles and label–value lines recorded as native-speaker rules,
`AGENTS.md` evidence source 4, each with one synthetic example: table cell: column header `| Hạng mục | Điểm cần lưu ý |`; caption: `*Hình 3. Những điểm cần
lưu ý trong quy trình nhập kho*`; table of contents: the entry `4. Những điều cần lưu ý khi chạy lại
phép đo`; checklist item: `- [ ] Cần lưu ý: sao lưu dữ liệu trước khi chạy lại`). The owner confirms the
four rules and examples before the rule edit (analysis finding C1, constitution IV). The entry also
gives the comparison text: the line kept unchanged, because it is correct (finding F3). Then edit V11's **Không flag** in `SKILL.md`, add the
manual cases to `calibration/ca-kiem-thu.md`, regenerate the registry and run `--check`. Pattern
numbering and the README table do not change. `SKILL.md` stays under 550 lines.

**Wording draft for V11** (for owner review during implementation, in the style of V14 and T5):
*Không áp dụng cho tít và heading, dòng nhãn–giá trị (*Trạng thái: đang xử lý*), ô bảng, chú thích
ảnh, mục lục và mục checklist.* The final text must pass the skill's own review (`AGENTS.md`).

## R6. Verification

- RED first for each story: T4 asked on a subject without `, và`; V2/V3/V5/V14 asked on a heading;
  V11 asked on a heading and a recognized label–value line.
- Fixtures for R3: recognized forms, lone plain lines, prose with a colon, lead-ins ending in `:`.
- Registry `--check` fails when a quoted phrase is edited out of `SKILL.md` (tested on a temporary
  copy).
- Full suite: tests whose required-check counts change are listed with their cause (SC-005).
