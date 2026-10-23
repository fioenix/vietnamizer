# Feature Specification: Label lines recognized by position

**Feature Branch**: `codex/012-standalone-label-lines`

**Created**: 2026-10-23

**Status**: Draft. On 2026-10-23 the owner reviewed the feature 011 label fixtures (011 task T023,
part b), stated a native-speaker rule on colons by position, and authorized `speckit-specify` for
this feature, with the rule and the review recorded in `calibration/LOG.md` first. The branch starts
from `main` at `abedaad` (feature 011 merged as PR #21). The owner answered Q1 on 2026-10-23
(option A). No open decisions. Implemented on the short path the owner chose (plan, tasks,
evidence); review finding 1 extended FR-001 to bold labels on any line. Not committed.

**Input**: Run speckit-specify for feature 012: a line with a colon that stands alone as a paragraph,
or as a list item of one sentence, is a label; record the rule and the T023 part b results in
`calibration/LOG.md` first. Record the colon after a connective only as a new phenomenon.

## Background

Feature 011 made V11 skip label–value lines, because a label such as `Ngày:` is the name of a field,
not a lead-in before information. Research R3 of 011 recognized only two forms, chosen to avoid any
tuned threshold: a bold label (`**Nhãn:** giá trị`), and plain label items in a list of at least two
adjacent label items with the same marker kind and indent. A lone plain `Nhãn: giá trị` line stays
prose.

On 2026-10-23 the owner rated 28 synthetic colon lines, shown without context and without the
runner's classification (`calibration/LOG.md`, entry "dấu hai chấm trong dòng nhãn và giữa đoạn
văn"). Two results conflict with R3:

- Lone lines the owner rates as labels, such as `Trạng thái: đang xử lý`, `- Người phụ trách: chị
  Lan` and `Kết luận: tao sai.`, are prose for the runner, so V11 is asked about them.
- Two lead-ins the owner rates as wrong, such as `Tóm lại: chưa nên phát hành.` and `Vậy thì sao:
  chẳng ai đọc cả.`, become labels for the runner when they stand next to each other in a list.

The owner then stated the rule this feature applies (native-speaker rule, `AGENTS.md` evidence
source 4): a sentence with a colon that stands alone as a paragraph has the form of a listing, so
the part before the colon is a label; a sentence with a colon inside a paragraph is mostly not a
label. By this rule the R3 forms remain labels, and position, not a list of two items, decides plain
labels.

The owner's second observation, that a colon inside a paragraph is mostly wrong unless it introduces
an inline enumeration separated by semicolons, is stricter than the common school norm (a colon may
also introduce an explanation). It is recorded in the log as a new phenomenon and is out of scope
here, as is the colon after a connective (`Tóm lại:` where a comma belongs).

Only V11 reads the label–value structure (`jev/registry.json`, exclusion `label_value: V11`), so this
feature changes which subjects V11 is asked about and nothing else.

## Clarifications

### Session 2026-10-23

- Q: Does "stands alone as a paragraph" mean a source line on its own, or only a paragraph separated
  by blank lines (Q1)? → A: A source line. A standalone sentence starts at the start of a line, ends
  at the end of a line and shares its lines with no other sentence. Fields written one per line
  without blank lines are therefore label lines.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A colon line standing alone is a label (Priority: P1)

A host evaluates a note whose fields are written one per line or one per paragraph, without bold and
without a run of list items: `Trạng thái: đang xử lý` on its own, or a single list item
`- Người phụ trách: chị Lan`. Each such line is recognized as a label–value line, so V11 is not asked
about it; every other pattern is asked as today.

**Why this priority**: It removes V11 questions whose answer the owner has given in advance, on the
most common way notes write a field, and it applies the rule the owner stated.

**Independent Test**: Prepare synthetic documents with each owner-rated line standing alone, as a
paragraph and as a single list item; check the structure recorded on the line's sentence and the
patterns asked about it with a fake transport.

**Acceptance Scenarios**:

1. **Given** a paragraph whose only sentence is `Trạng thái: đang xử lý`, **When** the host
   evaluates, **Then** the sentence is a label–value line and V11 is not asked about it.
2. **Given** a list item whose only sentence is `- Ghi chú: chưa tính phí.`, with no other label item
   next to it, **When** the host evaluates, **Then** the sentence is a label–value line.
3. **Given** a bold label or a field list of at least two label items, as recognized by feature 011,
   **When** the host evaluates, **Then** recognition is unchanged.
4. **Given** a lone line whose label is not letters and spaces only (`- Bộ 3: chạy lại`,
   ``- Lệnh `jev`: chạy prepare``, `Lúc 9 giờ sáng: hệ thống báo lỗi.`), ends in *rằng* or *là*, or
   has no value after the colon (`Nhóm đã thử ba cách sau:`), **When** the host evaluates, **Then**
   it stays prose, as in feature 011.
5. **Given** a lone line that shows one of V11's canonical signs (`Điều quan trọng cần lưu ý là: hệ
   thống chỉ đồng bộ 15 phút một lần.`), **When** the host evaluates, **Then** V11 is still asked.

---

### User Story 2 - A colon inside running prose stays prose (Priority: P1)

A host evaluates running prose in which a colon sentence shares a line with another sentence, such
as `Tao chạy lại phép đo. Kết luận: tao sai.` on one line. The colon sentence is not a label, so V11
is asked as today.

**Why this priority**: It is the half of the owner's rule that keeps V11 where the owner says a colon
is mostly not a label, and it guards against the wider recognition of User Story 1 reaching into
prose.

**Independent Test**: Prepare synthetic paragraphs that put each owner-rated line on the same line
as another sentence, before and after it, in prose and in list items; check that no sentence is
recognized as a label–value line unless a feature 011 form applies.

**Acceptance Scenarios**:

1. **Given** a line with two or more sentences where one starts with a plain label and a colon,
   **When** the host evaluates, **Then** neither sentence is a label–value line.
2. **Given** a list item whose plain-label sentence is followed on the same line by another sentence,
   not part of a field list of at least two label items, **When** the host evaluates, **Then** it
   stays prose.
3. **Given** a list item whose first sentence has a bold label, or one inside a field list of at least
   two label items, followed by another sentence, **When** the host evaluates, **Then** its first
   sentence is a label–value line, as in feature 011.
4. **Given** prose hard-wrapped across lines, where a plain-label sentence starts in the middle of a
   line, **When** the host evaluates, **Then** it stays prose.

---

### Edge Cases

- A lead-in that stands alone, such as `Tóm lại: chưa nên phát hành.` or `Lý do rất đơn giản: hệ
  thống chạy chậm hơn dự kiến.`: by the owner's rule it has the form of a listing, so it is a label
  and V11 is not asked. Its punctuation problem is the new phenomenon in the log, not V11. Recorded as
  a consequence of the rule, not a defect.
- A full clause before the colon, with letters and spaces only, standing alone (`Nhóm rút ra một bài
  học: phải đo trên dữ liệu thật.`): a label by the same rule; V11 is not asked. A clause with a comma
  or a digit before the colon stays prose.
- Several label lines in one paragraph separated by single line breaks (`Ngày: 22/10/2026.` then
  `Trạng thái: xong.` on the next line): each sentence stands alone on its line, so each is a label
  line (Q1).
- Lines without a final period (`Ngày: 22/10/2026` then `Trạng thái: xong`) that segmentation joins
  into one sentence across two lines: that sentence starts at a line start, ends at a line end and
  shares no line, so it is one label line, and V11 is not asked about either line.
- Prose hard-wrapped at a fixed width, where a plain-label sentence happens to fill whole lines: it
  is a label line by the rule. This is rare and costs only the V11 question.
- A list item: the line start is the first character after the list marker; a continuation line of
  the same item starts after its indentation.
- A one-sentence line inside a blockquote, a table cell, a heading or a protected span: unchanged;
  quoted text, tables and headings keep their current handling.
- A sentence whose segmentation boundary is not exact: never a label–value line, as in feature 011.
- `--scope selected`: explicit targets are evaluated as given, without structure exclusions, as in
  feature 011.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The runner MUST recognize as a label–value line a sentence that starts with a plain
  or bold label followed by a colon and a value, when that sentence stands alone: it starts at the start of a
  line (after any list marker or indentation), ends at the end of a line and shares its lines with no
  other sentence.
- **FR-002**: The runner MUST keep recognizing the feature 011 forms unchanged: a bold label, and the
  first sentence of each plain label item in a list of at least two adjacent label items with the
  same marker kind and indent.
- **FR-003**: The runner MUST NOT recognize as a label–value line a plain-label sentence that shares
  a line with another sentence, unless FR-002 applies.
- **FR-004**: The label conditions of feature 011 MUST stay: a label is letters and single spaces
  only, does not end in *rằng* or *là*, and is followed by a value on the same line.
- **FR-005**: A label–value line that shows one of V11's canonical signs MUST still receive V11, as in
  feature 011.
- **FR-006**: Recognition MUST rest on structure only, with no tuned numeric threshold (constitution
  IV); the only count used is the existing "at least two items" of FR-002.
- **FR-007**: Recognition MUST change the subjects only of patterns whose exclusions name the
  label–value structure; today that is V11 alone. Checks for every other pattern MUST be unchanged.
- **FR-008**: The host-facing contract (`references/typesafe-advisor.md`) MUST describe the forms of
  FR-001 to FR-004 and no longer state that a lone `Nhãn: giá trị` line stays prose.
- **FR-009**: Every recognized line MUST keep being reported as today: the excluded V11 check appears
  in coverage with reason `structure_excluded` and the structure kind.

### Key Entities

- **Label–value line**: a sentence whose text before the first colon is a label naming a field and
  whose text after it is the field's value. Recognized by form and by position; it carries the
  structure kind `label_value`.
- **Standalone sentence**: a sentence that starts at the start of a line, ends at the end of a line
  and shares its lines with no other sentence (Q1).
- **Owner-rated colon lines**: the 28 synthetic lines and ratings in the calibration entry of
  2026-10-23; the reference for acceptance.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Of the owner-rated lines rated *Được* that satisfy the label conditions of FR-004, every
  one is recognized as a label–value line when it stands alone: as a paragraph, as a single list item
  and as one of several lines separated by single line breaks.
- **SC-002**: The text of every owner-rated line, without its list marker and placed on the same line
  as another sentence, is recognized as a label–value line in 0 cases unless it has a bold label.
- **SC-003**: Every owner-rated line that shows a canonical V11 sign keeps its V11 question in every
  position.
- **SC-004**: On the synthetic ~1,000-word technical note used by feature 011, checks for every
  pattern except V11 are unchanged, and any change in V11 checks is listed with its cause.
- **SC-005**: The existing suite passes, apart from fixtures whose expected recognition changes by
  this rule; each such change is listed with the rule that changes it.
- **SC-006**: The calibration entry with the owner's rule is committed before the runner change, and
  the package validator passes.

## Assumptions

- The owner's rule is a native-speaker rule with examples (`AGENTS.md` evidence source 4), recorded in
  `calibration/LOG.md` on 2026-10-23 before any runner change.
- No rule text changes: V11's **Không flag** already names label–value lines. The feature changes how
  the runner recognizes them, not what the rule says.
- The label conditions of feature 011 stay, so some lines the owner rates as labels stay prose for the
  runner (digits, code). That errs in the safe direction: V11 is asked once more than needed.
- Out of scope: the colon after a connective, the colon inside a paragraph without an enumeration,
  and lead-ins missing from V11's **Dấu hiệu** (all recorded in the log as observations), headings,
  tables, quotes, and feature 010.
- Tests use synthetic text only; no key, network or live service is needed.
- A release and version bump are separate owner decisions.
