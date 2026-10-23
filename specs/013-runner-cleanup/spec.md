# Feature Specification: Runner cleanup — link parentheses, unreadable input, one editable text

**Feature Branch**: `codex/013-runner-cleanup`

**Created**: 2026-10-23

**Status**: Draft. On 2026-10-23 the owner asked to clear the small technical debt left by features
009–011 and chose the short path used for 012 (spec, plan and tasks in one pass, no
`speckit-analyze`, test-first implementation, short independent review). The branch starts from
`main` at `abedaad`; it is independent of feature 012 (PR #22). Revised during implementation: the annotated fixture
`url-ambiguous-closer` keeps bare URLs with parentheses ambiguous (scenario 6, FR-002). Implemented on the
short path; review findings on escaped parentheses and a closed standard input fixed. Not committed.

**Input**: Clear the runner's small technical debt: one editable-text helper, URLs with parentheses,
and an unreadable input file. The 0.025 score tolerance is not debt: feature 007's review kept strict
validation on purpose.

## Background

- **Link parentheses.** A Markdown link or bare URL whose address contains parentheses, such as
  `[bài](https://vi.wikipedia.org/wiki/Foo_(bar))`, makes preparation mark the whole unit
  `ambiguous_url_closer`, so none of its sentences is evaluated. The same happens to a bare URL in
  prose parentheses, `Xem tài liệu (https://example.org/a) nhé.`, a very common form. Feature 009
  observed one such region on a real note and left it out of scope.
  Prior art settles both cases without a threshold: CommonMark allows balanced parentheses inside a
  link destination, and GitHub Flavored Markdown's extended autolink rule drops trailing `)` that
  have no matching `(` inside the URL.
- **Unreadable input.** `python3 -B -m jev evaluate --input <path>` reports `invalid_input` when the
  file cannot be opened, the same status as a malformed document (observed in feature 009 when a
  scratch file had been removed). A host cannot tell "fix the document" from "the file is not there".
- **Two editable-text helpers.** `jev/coverage.py` keeps its own copy of `core.editable_text` and
  recomputes it for every structure-excluded or gated pattern of a unit. Measured on 2,100 units, the
  ledger takes 0.164 s to build, so the cost is not material; the duplicate is a maintenance risk
  only.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Links and URLs with parentheses are evaluated (Priority: P1)

A host evaluates a note that cites a page whose address has parentheses, or puts a URL inside prose
parentheses. The sentences around the link are segmented and evaluated like any other sentence.

**Why this priority**: Today the whole unit is lost to evaluation for an address form that Markdown
defines exactly.

**Independent Test**: Prepare synthetic paragraphs with each form; check that their sentences are
exact and that the address stays protected from boundary search.

**Acceptance Scenarios**:

1. **Given** `Xem [bài](https://vi.wikipedia.org/wiki/Foo_(bar)) để biết thêm. Câu sau.`, **When**
   the host prepares it, **Then** it yields two exact sentences and no `ambiguous_url_closer`.
2. **Given** `(xem [bài](https://x.org/a_(b))). Câu sau.`, **Then** two exact sentences; the link
   closes at its balanced `)` and the last `)` closes the prose parenthesis.
3. **Given** `Xem tài liệu (https://example.org/a) nhé. Câu sau.`, **Then** two exact sentences; the
   `)` closes the prose parenthesis, not the URL.
4. **Given** a relative destination with balanced parentheses, `Xem [a](b(c).md) nhé.`, **Then** one
   exact sentence.
5. **Given** an address whose parentheses do not balance, such as `[bài](https://x.org/a(b)` or
   `https://x.org/a(b`, **Then** the unit stays `ambiguous_url_closer`, as today.
6. **Given** a bare URL that keeps a parenthesis, `Xem https://vi.wikipedia.org/wiki/Foo_(bar) để biết
   thêm.`, **Then** the unit stays `ambiguous_url_closer`, as the independently annotated fixture
   `url-ambiguous-closer` (`Xem https://example.org/a(b). Mai tính.`) labels it. Written as a
   Markdown link, the same address is settled by scenario 1.

---

### User Story 2 - An unreadable input file has its own status (Priority: P2)

A host runs the CLI with an input path that does not exist or cannot be read. The report's status is
`input_unreadable`, exit code 2, and a malformed but readable document still reports `invalid_input`.

**Why this priority**: The host can tell a missing file from a bad document without reading logs.

**Independent Test**: Run the CLI as a subprocess on a missing path and on a malformed file.

**Acceptance Scenarios**:

1. **Given** a key and `--input` naming a missing file, **When** the host runs `evaluate` or
   `prepare`, **Then** the report is `{"status": "input_unreadable"}` and the exit code is 2.
2. **Given** a readable file that is not valid JSON or not a valid document, **Then** the status stays
   `invalid_input`.
3. **Given** no key, **When** the host runs `evaluate`, **Then** the status stays `key_absent`, as
   today; the file is not read.

---

### User Story 3 - One editable-text definition (Priority: P3)

The coverage ledger reads a unit's editable text from the same helper as the rest of the runner, once
per unit.

**Why this priority**: Removes a duplicate that could drift; no visible behavior change.

**Independent Test**: The existing suite, including the check-order guard on the ~1,000-word note,
passes unchanged.

**Acceptance Scenarios**:

1. **Given** the existing suite, **When** it runs after the change, **Then** every test passes with the
   same expected counts and check order.

### Edge Cases

- A bare URL inside prose parentheses with its own parentheses, `(xem https://x.org/a_(b)).`: the URL
  keeps a parenthesis, so the unit stays `ambiguous_url_closer` (scenario 6).
- A link destination that contains a space or a title (`[a](url "tiêu đề")`): handled as today.
- A very long token of parentheses: scanning charges the preparation work budget and stays linear.
- Parentheses inside inline code or another protected span: unchanged; protected text is opaque.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A Markdown link destination MUST end at the `)` that balances the parentheses opened
  inside it (CommonMark). When such a `)` exists, the destination MUST NOT make the unit
  `ambiguous_url_closer`.
- **FR-002**: A bare `http://` or `https://` URL MUST exclude trailing `)` that have no matching `(`
  inside the URL, together with trailing punctuation (GFM extended autolink). A URL left with no
  parenthesis MUST NOT make the unit `ambiguous_url_closer`; one that keeps a parenthesis MUST keep it,
  as the annotated fixture `url-ambiguous-closer` requires.
- **FR-003**: A destination or URL whose parentheses cannot be balanced MUST keep
  `ambiguous_url_closer`.
- **FR-004**: The address text MUST stay opaque to sentence-boundary search, so a `.` or `)` inside it
  never ends a sentence or changes the prose parenthesis depth.
- **FR-005**: Parenthesis scanning MUST charge the preparation work budget and MUST NOT loop per
  character in Python over text without parentheses.
- **FR-006**: The CLI MUST report `input_unreadable` with exit code 2 when the input file or standard
  input cannot be read, and MUST keep `invalid_input` for readable input that is not a valid document.
- **FR-007**: The host contract (`references/typesafe-advisor.md`) MUST list `input_unreadable` and
  describe how link and URL parentheses are read.
- **FR-008**: The coverage ledger MUST use the runner's single editable-text helper, computed at most
  once per unit, with no change to coverage results.

### Key Entities

- **Link destination**: the address inside `[text](…)`; opaque to sentence-boundary search.
- **Bare URL**: an `http://` or `https://` token in prose; opaque to sentence-boundary search.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The four resolvable forms of User Story 1 prepare with 0 `ambiguous_url_closer` regions
  and the expected number of exact sentences; the unbalanced forms and the bare URL keeping a
  parenthesis keep it, and the annotated segmentation fixtures pass unchanged.
- **SC-002**: A missing input path reports `input_unreadable` in 100% of runs of `evaluate` and
  `prepare` with a key; malformed input keeps `invalid_input`.
- **SC-003**: The existing suite passes; the only expected-value changes are the feature 009 test that
  pinned `[a](b(c).md)` as ambiguous, listed with its cause.
- **SC-004**: The check-order guard on the ~1,000-word note is unchanged (7,001 checks, same digests).
- **SC-005**: Preparing a 400,000-character token of parentheses finishes within 5 seconds, and
  text without parentheses in its addresses spends exactly the same preparation work as before.

## Assumptions

- Only `http://` and `https://` addresses are bare URLs, as today; other schemes are unchanged.
- No rule text, registry or report field changes besides the new CLI status.
- Tests use synthetic text only; no key, network or live service.
- A release and version bump are separate owner decisions.
