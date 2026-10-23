# Feature Specification: Structural exclusions and the T4 sign gate

**Feature Branch**: `codex/011-structural-exclusions`

**Created**: 2026-10-22

**Status**: Draft. On 2026-10-22 the owner authorized rule maintenance for item 5 of the reported
bug (sentence-level V11 and T4 questions on a heading and a label line) as a feature separate from
010. The owner answered Q1 the same day (option B). No open decisions. Revised during planning on
2026-10-22: research R3 recognizes label–value lines only as bold labels or plain labels in a field
list of at least two items, so User Story 2 scenario 2 and SC-001 were reworded. The owner accepted
this deviation on 2026-10-22 and authorized `speckit-tasks`. Not implemented. The branch starts from the feature
009 tip `2670959` (PR #19, not merged), because 009 changes the segmentation this feature reads;
it is independent of feature 010.

**Input**: Run speckit-specify for feature 011: structural exclusions for headings and label lines,
and a T4 gate.

## Background

A host ran the runner on a long Vietnamese technical note. The only flags above 0.4 fell on two
lines: the H1 title and the line `- Ngày: 22/10/2026 (Asia/Ho_Chi_Minh)`. Observed in the session
that opened feature 009 (live service, before feature 009):

- H1 title: V11 0.58 and T4 0.58; date line: V11 0.72 and T4 0.50. Neither line contains `, và`.
- In the same run, `T4_interpretation` answered `none_fit` (0.92 on the H1), and T4 scored above
  0.4 on 8 of the 9 units evaluated. The T4 question assumes the text contains `, và`; on text
  without one, its answer carries no information.
- A heading with no sentence becomes one whole-unit subject and receives every target pattern of
  its profile (`jev/coverage.py:29`), 86 checks under the technical profile. The only gates are
  protected regions, typography-only units and inactive profiles. Nothing recognizes a
  `Nhãn: giá trị` line.

What the canonical rules say (`SKILL.md`, read at `2670959`):

- T4's sign is the sequence `, và`, and it states that a hit of `,\s+và\s` is necessary but not
  sufficient. Text without that sequence cannot show the T4 error.
- Eight patterns already name titles, headings, labels, tables or forms in their **Không flag**
  (V2, V3, V5, V6, V14, V20, T5, T6), but the runner still asks every one of them about such text and
  relies on the model to apply the exception. Some mentions cover the whole structure (V14: "tít,
  sapo, chú thích ảnh, nhãn nút, mục lục, ô bảng, checklist"; T5: "nhãn–giá trị"); others cover one
  form only (V6: "tiêu đề dạng câu hỏi").
- V11's **Không flag** does not mention titles or labels. Its sign is a lead-in clause before the
  information, which a title or a `Nhãn: giá trị` line does not have in the observed cases; its sign
  list is open (*Việc X là điều cần thiết*), so a lexical gate for V11 is not sound.
- Heading-specific rules must keep running on headings: T1 (title case), T5, T6 (emoji) and the
  technical profile's balanced-heading pattern.

## Clarifications

### Session 2026-10-22

- Q: Which structures should V11's **Không flag** name (Q1)? → A: B. Titles and headings,
  label–value lines, table cells, captions, tables of contents and checklist items, mirroring V14.
  Titles and label–value lines rest on the observed false positives. The other four have no
  observed case; after analysis finding C1 (constitution IV) each is recorded as a native-speaker
  rule with one synthetic example (`AGENTS.md` evidence source 4), which the owner confirms before
  the rule edit.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - No T4 question where `, và` is absent (Priority: P1)

A host evaluates a note. T4 questions are asked only about subjects that contain the sequence T4's
sign names; every other subject is recorded as excluded for T4 with a reason, without spending a
question.

**Why this priority**: It removes the most frequent false T4 signal in the observed run, follows
directly from T4's canonical sign, changes no rule text and saves two questions per subject.

**Independent Test**: Prepare and evaluate (fake transport) a synthetic note mixing sentences with
and without `, và`; count T4 questions and exclusions.

**Acceptance Scenarios**:

1. **Given** a sentence without `, và` (with any whitespace between the comma and *và*), **When**
   the host evaluates, **Then** no T4 question is asked about it and coverage records T4 as excluded
   for it with reason `sign_absent`.
2. **Given** a sentence containing `, và `, **When** the host evaluates, **Then** T4 is asked as
   today.
3. **Given** `, và` inside protected text only, **When** the host evaluates, **Then** T4 is not asked,
   because protected text is not editable.
4. **Given** an H1 title and a `- Ngày: 22/10/2026 (Asia/Ho_Chi_Minh)` line, **When** the host
   evaluates, **Then** neither receives a T4 question.

---

### User Story 2 - Patterns skip structures their own rules exclude (Priority: P1)

A host evaluates a note with headings, `Nhãn: giá trị` lines and checklist items. A pattern whose
canonical **Không flag** excludes a structure as a whole is not asked about text of that structure;
coverage records the exclusion with a reason. Patterns whose rules target that structure, such as
T1 and T5 on headings, keep running.

**Why this priority**: It turns exceptions the rules already state into deterministic behaviour,
removes questions whose correct answer is known in advance, and changes no rule text.

**Independent Test**: Evaluate (fake transport) a synthetic note with headings, label lines and
prose; compare the patterns asked per subject with the expected list derived from canonical
**Không flag** text.

**Acceptance Scenarios**:

1. **Given** a heading, **When** the host evaluates, **Then** patterns whose **Không flag** excludes
   titles or headings as a whole are not asked about it, and T1, T5, T6 and the technical profile's
   heading pattern still are.
2. **Given** a bold label such as `- **Cách chấm:** dùng cùng một giám khảo`, or a field list of at
   least two adjacent items such as `- Trạng thái: đang xử lý` followed by `- Người duyệt: trưởng
   nhóm`, **When** the host evaluates, **Then** each item is recognized as a label–value line, and
   patterns whose **Không flag** excludes label–value text as a whole are not asked about it. A lone
   plain `Trạng thái: đang xử lý` line is treated as prose.
3. **Given** a prose sentence that contains a colon, such as `Kết quả lệch khoảng ±10% so với bản cũ:
   mày đừng so trực tiếp.`, **When** the host evaluates, **Then** it is not treated as a label–value
   line and every applicable pattern is asked as today.
4. **Given** a mention that excludes only one form of a structure (V6: a title phrased as a
   question), **When** the host evaluates, **Then** that pattern is not excluded from the whole
   structure; the exception stays with the model.
5. **Given** an excluded pattern on a subject, **When** the host reads the report, **Then** coverage
   shows status `excluded` with reason `structure_excluded` and the structure kind, never a
   validated answer.

---

### User Story 3 - V11 names the structures it does not apply to (Priority: P2)

V11's canonical **Không flag** names titles and headings, label–value lines, table cells,
captions, tables of contents and checklist items (owner decision Q1: B), with a calibration log
entry recorded first. The runner then excludes V11 from those structures by the same mechanism as User
Story 2.

**Why this priority**: It fixes the remaining observed false positive (V11 on the H1 and the date
line). It is a canonical rule change, so it needs the calibration entry first and goes after the
two stories that change no rule text.

**Independent Test**: The calibration entry exists before the rule edit; the registry is
regenerated and checked; the H1 and date-line fixtures receive no V11 question.

**Acceptance Scenarios**:

1. **Given** the rule change, **When** a maintainer reads `calibration/LOG.md`, **Then** an entry
   dated before the rule edit records the genre, the before text (synthetic, equivalent to the
   private case), the comparison text (the line kept unchanged, because it is correct), the
   observed scores, the named difference, V11, its classification as a pattern that flags correct
   text, and the decision.
2. **Given** an H1 title and a field list starting `- Ngày: 22/10/2026 (Asia/Ho_Chi_Minh)` followed by
   another label item, **When** the host evaluates, **Then** neither the title nor the date item
   receives a V11 question. A lone plain date line keeps its V11 question (research R3).
3. **Given** a prose sentence `Điều quan trọng cần lưu ý là hệ thống chỉ đồng bộ 15 phút một lần.`,
   **When** the host evaluates, **Then** V11 is still asked.
4. **Given** the structures the runner can recognize (headings and label–value lines; tables are
   already typography-only), **When** the host evaluates, **Then** V11 is excluded from them by the
   User Story 2 mechanism. Captions, tables of contents and checklist items are named in the rule
   for the host LLM and the model; the runner does not detect them in this feature.

---

### Edge Cases

- A heading that is a full sentence (`## Vì sao tao bỏ cách đo cũ`): it stays a heading; only
  patterns whose rules exclude titles as a whole are skipped.
- A label–value line whose value is several sentences: the label–value structure covers only the
  line's first sentence; later sentences are prose and are checked as today.
- A line ending in a colon that introduces a list (`- Quy ước nhãn, giống ghi chú [a.md](a.md):`): a
  lead-in, not a label–value line; checked as today.
- `,và` with no space, or `, và` across a line break: the gate follows the canonical expression
  `,\s+và\s`; `,và` without whitespace does not open T4, and a line break counts as whitespace.
- `, và` inside inline code or another protected span: not editable, so it does not open T4.
- *và* written in decomposed form (NFD, `a` plus a combining grave accent), as text copied from some
  macOS sources is: the gate matches it as `, và`, because runner offsets cannot normalize the source
  but the gate decision can.
- A structure excluded for a pattern inside a typography-only unit: the typography-only gate applies
  first, as today.
- Candidate edits on an excluded subject: candidate review checks are unaffected; exclusions apply
  to pattern checks only.
- A host-supplied `kind` annotation that marks a unit as a heading: treated as a heading.

## Requirements *(mandatory)*

### Functional Requirements

**T4 sign gate (User Story 1)**

- **FR-001**: T4 MUST be asked about a subject only when the subject's editable text, with protected
  text removed, matches the canonical sign `,\s+và\s`. The match MUST be made on the text's canonical
  composition (NFC), so *và* written with a combining grave accent (NFD) still opens T4; offsets and
  request text stay unchanged.
- **FR-002**: A subject without the sign MUST be recorded as excluded for T4 with reason
  `sign_absent`, and MUST NOT count toward checks required.
- **FR-003**: The sign MUST be taken from T4's canonical text, so a change to that text changes the
  gate through the existing registry regeneration and check.

**Structural exclusions (User Story 2)**

- **FR-004**: The runner MUST recognize headings (from layout or a host `kind` annotation) and
  label–value lines.
- **FR-005**: Label–value recognition MUST accept the forms named in the acceptance scenarios and
  MUST NOT classify prose sentences or list lead-ins as label–value lines; when a line is
  ambiguous, it MUST be treated as prose.
- **FR-006**: For each pattern, the structures it is excluded from MUST be derived from that
  pattern's canonical **Không flag** text, and only where the text excludes the structure as a
  whole; a mention limited to one form of the structure MUST NOT create an exclusion.
- **FR-007**: The pattern-to-structure exclusions MUST be generated into the registry and MUST be
  checked against the canonical text, so the build fails when the rule text and the exclusions
  disagree.
- **FR-008**: An excluded pattern on a subject MUST be recorded as `excluded` with reason
  `structure_excluded` and the structure kind, MUST NOT count toward checks required, and MUST NOT
  change candidate review checks.
- **FR-009**: Patterns whose canonical rules target a structure (T1, T5, T6 and the technical
  profile's heading pattern for headings) MUST keep running on it.

**V11 (User Story 3, subject to Q1)**

- **FR-010**: Before V11's rule text changes, `calibration/LOG.md` MUST gain an entry in the format
  `AGENTS.md` prescribes, using synthetic text equivalent to the private case.
- **FR-011**: V11's **Không flag** MUST name titles and headings, label–value lines, table cells,
  captions, tables of contents and checklist items, written in natural Vietnamese and consistent
  with the wording of V14 and T5. The calibration entry MUST record the last four as native-speaker
  rules (`AGENTS.md` evidence source 4), each with one synthetic example that the owner confirms
  before V11's text changes.
- **FR-012**: `calibration/ca-kiem-thu.md` MUST gain a V11 case for each newly named structure and a
  case showing V11 still applies to a lead-in sentence in prose.

**Integrity**

- **FR-013**: An exclusion MUST NOT hide source text from the coverage ledger: every excluded check stays
  enumerable with its reason, and source accounting is unchanged.
- **FR-014**: A request MUST NOT carry more source or context text than today; exclusions only remove
  questions.
- **FR-015**: Pattern numbering, the README pattern table and the version fields MUST stay
  consistent with `AGENTS.md`; no pattern is added, removed or renumbered.

### Key Entities

- **Structure kind**: `heading` or `label_value` for a subject; derived from layout, annotations and
  the label–value rule.
- **Structure exclusion**: a pattern ID with the structure kinds its canonical **Không flag**
  excludes as a whole; generated into the registry.
- **Sign gate**: for T4, the canonical expression a subject's editable text must match before T4 is
  asked.
- **Exclusion record**: coverage status `excluded` with reason `sign_absent` or
  `structure_excluded` and, for the latter, the structure kind.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On a synthetic H1 title and a field list starting `- Ngày: 22/10/2026 (Asia/Ho_Chi_Minh)`
  followed by another label item, no V11 or T4 question is asked about the title or the date item.
  A lone plain date line gets no T4 question and keeps its V11 question.
- **SC-002**: On a synthetic ~1,000-word technical note, T4 questions fall to the number of subjects
  containing `, và`, and total checks required fall by at least the T4 and structure exclusions,
  with each removed check listed with its reason.
- **SC-003**: On a labeled set of at least 20 label–value lines and 20 prose or lead-in lines with a
  colon, label–value recognition makes no false recognition on the prose and lead-in set, and
  recognizes every line of the forms named in the acceptance scenarios.
- **SC-004**: Every exclusion in the registry traces to a quoted phrase in the pattern's canonical
  **Không flag**, and the build check fails when either side changes alone.
- **SC-005**: The existing suite passes, apart from tests whose expected check counts change because
  of the exclusions; each such change is listed with its cause.
- **SC-006**: The calibration entry is dated before the rule edit in history, and the package
  validator passes.

## Assumptions

- The T4 gate and the structural exclusions apply rules the canonical text already states; they are
  runner applicability, not new rules. Only User Story 3 edits a rule (`SKILL.md`, V11), and the
  owner authorized that maintenance on 2026-10-22.
- The private note is not used. Calibration and tests use synthetic text built to reproduce the
  observed structures; the log says that the original case is private.
- One observed false positive is enough to add a named exclusion, per `AGENTS.md` ("Một trường hợp
  sửa nhầm có thể đủ để bổ sung trường hợp loại trừ nếu lỗi được gọi tên rõ và có thể kiểm tra lại").
- Label–value recognition is a structural rule checked against a labeled fixture set (SC-003). It
  must not rest on an untested numeric threshold; if one is needed, the plan states it and the
  fixture set tests it.
- Table cells are already handled: tables become typography-only units today.
- Out of scope: link-only lines, bare-data values, other patterns' rule text, the 0.025 Score
  tolerance, and anything in feature 010 (budget, priorities, invalid replies).
- A release, version bump and archive publication are separate owner decisions.
- No live service run is needed; any live run needs the owner's spend approval and synthetic text.
