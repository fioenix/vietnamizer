# Feature Specification: Complete preparation of long Markdown documents

**Feature Branch**: `codex/009-long-document-preparation`

**Created**: 2026-10-22

**Status**: Draft. Owner approved starting the specification on 2026-10-22 for two fixes only: length-scaled preparation budgets and in-token punctuation/relative link destinations. Revised during planning on 2026-10-22: planning research (R1–R2) showed that a purely length-scaled budget breaks the existing time bounds, so FR-001–FR-003 and FR-014 now describe a raised absolute work bound plus an explicit inventory cap. Research R3 showed that the first boundary rule contradicted feature 008's missing-space contract, so FR-005–FR-007 were narrowed. Owner accepted research R2 and R3 on 2026-10-22 and authorized task generation. Not implemented.

**Input**: Start a Spec Kit feature for fix 1 (length-scaled preparation budgets) and fix 2 (in-token punctuation and relative link destinations), using the scratchpad tests as the RED baseline.

## Background

A host ran the shipped runner on a 477-line, ~8,600-word Vietnamese technical design note in
Markdown. Local preparation stopped at source offset 12,359 of 48,400 code points: 168 of 270
units were reported as `preparation_limit`, and one bullet ending in a relative link was reported
as `unsafe_boundary`. Remote evaluation could therefore cover at most the first quarter of the
document before any request was sent. The reproduction and root-cause analysis were done in the
session that opened this feature. The source document is private and is not part of this feature.

Observed causes, recorded at commit `feed64d` with runner `jev-1.14.0`:

- One fixed scan budget of 4,096 work units is shared by every unit in a document. Scanning costs
  about two units per whitespace-separated token, so preparation stops after roughly 2,000 tokens
  (about 12k code points), whatever the input size.
- A separate fixed metadata budget of 4,096 units covers lines, units, annotations and context
  links. The reported note used 3,069 of it. A synthetic note of about 480 units (~6k code points)
  exhausts it, and the whole source is then returned as one unprocessed span with zero units.
- Terminal punctuation that is not followed by whitespace is marked `unsafe_boundary`, the same
  reason used for unsafe grapheme breaks. Filenames inside link labels (`ghi-chu.md](`), a quoted
  question followed by a comma (`?",`) and `!,` inside a link label all trigger it. Link
  destinations are skipped as opaque only for `http://` and `https://`.

- The scan budget also acts, implicitly, as the cap on how many units and sentences one invocation
  inventories (tests in feature 008 require at most 4,096). That cap limits ledger size, not text
  quality, and is a different concern from work.

Both budgets were accepted in feature 008 as execution bounds, not language thresholds
(`specs/008-sentence-coverage/contracts/segmentation.md`, `evidence.md`). This feature keeps that
purpose, raises the work bound so ordinary long notes fit, and makes the inventory cap explicit.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Prepare a whole long technical note (Priority: P1)

A host runs local preparation on an ordinary long Markdown document (5,000–10,000 words, with
headings, nested lists, tables, links, numbers and one code block). Every unit is inventoried and
every sentence the segmentation profile can resolve is segmented. Only regions with a real boundary
ambiguity stay unresolved.

**Why this priority**: Today preparation stops at about 2,000 tokens, so nothing after that point can
ever be evaluated, and a host cannot tell users more than "Jev was incomplete". Every later
improvement to coverage or scheduling depends on the document being prepared first.

**Independent Test**: Run network-free preparation on synthetic long Markdown notes and check that no
unresolved region carries `preparation_limit` and that unit and sentence counts match an independent
count. No key or network is needed.

**Acceptance Scenarios**:

1. **Given** a synthetic Markdown note of about 23,600 code points and 5,000 tokens (baseline case
   `test_long_markdown_crosses_scan_budget_without_preparation_limit`), **when** preparation runs,
   **then** the status is `prepared` and no region is unresolved for `preparation_limit`.
2. **Given** a synthetic note of about 480 short units under 7,000 code points (baseline case
   `test_many_short_units_do_not_exhaust_metadata_budget`), **when** preparation runs, **then** every
   unit is inventoried and no region is unresolved for `preparation_limit`.
3. **Given** a synthetic note of 10,000 words, **when** preparation runs, **then** it is fully
   prepared. **Given** a note whose units and sentences together exceed the inventory cap, **when**
   preparation runs, **then** the inventoried prefix is kept and the remainder is reported as
   `preparation_limit`, as today.
4. **Given** the existing preparation deadline expires during preparation, **when** preparation
   stops, **then** the already classified prefix is kept and the remainder is reported as
   `preparation_deadline`, exactly as today.

---

### User Story 2 — Keep sentences whole around filenames, links and quoted questions (Priority: P1)

Inside a technical sentence, file names, domains, relative link destinations and punctuation followed
directly by a comma or colon do not end the sentence. A relative link such as
`[ghi-chu.md](ghi-chu.md)`, a quoted question followed by a comma, or `!` inside a link label leaves the
sentence segmented as one exact sentence. A real missing space between two sentences stays unresolved.

**Why this priority**: These forms are common in technical notes and are not real boundary
ambiguities. Marking them unresolved silently removes their sentences from evaluation.

**Independent Test**: Run preparation on short synthetic sentences containing each form and compare
with independently annotated expected spans, plus the existing segmentation corpus.

**Acceptance Scenarios**:

1. **Given** the bullet `- Quy ước đặt tên, giống ghi chú [so-sanh-ban-cu.md](so-sanh-ban-cu.md):`
   (baseline case `test_bullet_with_relative_link_and_trailing_colon_is_exact`), **when** preparation
   runs, **then** nothing is unresolved and the status is `prepared`.
2. **Given** `- **thời gian**: "tuần trước ai đổi lịch họp?", có đích là bản ghi mới nhất.` (baseline
   case `test_quoted_question_followed_by_comma_is_not_a_boundary`), **when** preparation runs,
   **then** exactly one sentence is segmented and nothing is unresolved.
3. **Given** a link label containing `!,` such as `[Đố vui!, bản 2025](https://example.org/x)`,
   **when** preparation runs, **then** the label does not create a boundary.
4. **Given** `Tôi về.Bạn ở lại.` (an uppercase letter directly after a period), **when** preparation
   runs, **then** the region stays unresolved, as the existing corpus case `missing-period-space`
   requires.

---

### User Story 3 — Know which segmentation rules produced a result (Priority: P2)

A host or maintainer comparing two runs can tell whether sentence identities came from the old or the
new boundary rules.

**Why this priority**: Sentence identities are bound to the segmentation profile. Changing boundary
decisions under the same profile name would let results from different rules look comparable.

**Independent Test**: Prepare the same input before and after the change and check that the reported
segmentation profile differs, that every sentence identity changes (the profile name is part of each
identity), and that sentence spans change only where the delta rules of User Story 2 apply.

**Acceptance Scenarios**:

1. **Given** the boundary rules of User Story 2 are in place, **when** preparation reports its
   segmentation profile, **then** the profile identifier differs from `vi-spans-1`.
2. **Given** a change that only alters budgets (User Story 1), **when** a document that was already
   fully prepared before is prepared again, **then** its sentence spans are unchanged.

---

### Edge Cases

- One very long token without whitespace (for example a 1 MiB string) must remain linear in work
  and must not exceed the time bound.
- A document consisting only of very short sentences (`Ab. Ab. Ab. …`) up to the input size limit
  is the worst case for scan work and must still finish within SC-003.
- Many annotations, context links or candidates in the input still share the absolute metadata work bound,
  so metadata cannot be used to bypass the work limit (feature 008 test
  `test_many_explicit_parents_cannot_bypass_work_inventory` keeps passing).
- A relative link destination containing a period followed by uppercase text (`[A](Ghi.Chu.md)`)
  must not create a boundary inside the destination.
- A URL whose parentheses are ambiguous (`https://example.org/a(b).`) keeps its current
  `ambiguous_url_closer` treatment; this feature does not change it.
- Punctuation followed directly by a comma, semicolon, colon or more terminal punctuation does not
  end a sentence. Punctuation followed directly by a letter outside a recognized token stays
  ambiguous, whether the letter is uppercase or lowercase.
- An unaccented typo such as `Tôi ve.ban` matches the dotted-identifier shape and becomes part of
  one sentence instead of an unresolved region. No text is lost; this trade-off is accepted.
- Ellipsis and abbreviation rules (`...`, `…`, `v.v.`, `TS.`) keep their current decisions.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Local preparation MUST complete scanning of every unit of any ordinary Markdown or
  paragraph-lines document of up to 10,000 words whose units and sentences fit within the inventory
  cap (FR-014), unless the existing preparation deadline expires first.
- **FR-002**: Metadata-phase work (lines, units, annotations, context links, reviews, candidates)
  MUST complete for the same documents. If the metadata phase still runs out of work, the whole source
  MUST be returned unprocessed and nothing evaluated, as today. This is distinct from the inventory
  cap (FR-014), where the classified prefix stays eligible for evaluation.
- **FR-003**: Each preparation phase MUST keep an absolute work bound, so a crafted input of any size
  within the input limit stops with `preparation_limit` instead of running long. The bound MUST keep
  every existing time and memory assertion of feature 008 passing unchanged.
- **FR-004**: When the deadline stops preparation, the classified prefix and the exact unprocessed
  remainder MUST be reported as they are today; no text may be dropped or certified.
- **FR-005**: Terminal punctuation (`.`, `!`, `?`, `…`) followed, after any closing quotes or brackets,
  directly by a comma, semicolon, colon or further terminal punctuation MUST NOT be treated as a
  sentence boundary and MUST NOT make its sentence unresolved for that reason (`?",`, `!,`, `?".`).
- **FR-006**: Terminal punctuation followed directly by any other character that is not part of a
  recognized token MUST stay unresolved, as feature 008's segmentation contract requires for a
  missing space (`Tôi về.Bạn`, `về.bạn`, `Done.Next`), with an `ambiguous_*` reason rather than
  `unsafe_boundary`. Today these cases report `unsafe_boundary`; the corpus checks only that they
  stay unresolved.
- **FR-007**: The destination of an inline link `[label](destination)` MUST be treated as opaque for
  boundary decisions, whatever its scheme, including relative paths. Dotted ASCII identifiers such as
  file names, domains and module paths (`so-sanh-ban-cu.md`, `example.dev`, `jev.core`; each segment
  after a dot starts with a lowercase ASCII letter or digit) MUST be recognized as lexical tokens, like
  URLs and decimals already are.
- **FR-008**: The `unsafe_boundary` reason MUST be reserved for boundaries that would split a user-
  perceived character (grapheme cluster, CRLF pair, combining sequence, emoji sequence).
- **FR-009**: Because FR-005 to FR-007 change boundary decisions, the segmentation profile identifier
  MUST change, and sentence identities MUST be bound to the new identifier.
- **FR-010**: All 54 cases of the existing segmentation corpus MUST keep their expected outcome.
  Cases MUST NOT be relabelled or removed to make the change pass; any disagreement is recorded for
  owner adjudication.
- **FR-011**: The four baseline cases in `baseline/test_red_baseline.py` MUST fail before the change
  and pass after it, and MUST be moved into the repository's shipped test suite.
- **FR-012**: Request limits (bytes, questions, request count, total and per-request deadlines) MUST
  NOT change. Hosts MUST still see `preparation_incomplete` or `incomplete` when coverage is partial.
- **FR-013**: Host-facing documentation that states preparation limits
  (`references/typesafe-advisor.md`) MUST describe the absolute work bound and the inventory cap accurately, without promising
  that a long document will be fully evaluated within one invocation.
- **FR-014**: The cap on units plus sentences inventoried by one invocation MUST stay at 4,096 and MUST
  be enforced explicitly, independent of the work bound. Exceeding it MUST report the remainder as
  `preparation_limit`.

### Key Entities

- **Preparation work bound**: the maximum local work one invocation may spend in the metadata phase
  and in the scan phase, each with its own absolute bound. It is not a language threshold.
- **Inventory cap**: the maximum number of units plus sentences one invocation records (4,096). It
  bounds ledger size and is unchanged by this feature.
- **Segmentation profile**: the named, versioned set of boundary rules that sentence identities are
  bound to.
- **Unresolved region**: an exact source span with one reason (`preparation_limit`,
  `preparation_deadline`, `unsafe_boundary`, `ambiguous_*`, …) that is never certified as segmented.
- **RED baseline**: the four synthetic tests and their recorded failing output in `baseline/`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All four baseline cases pass, and the recorded RED output shows that each failed before
  the change for the reason named in its acceptance scenario.
- **SC-002**: A synthetic Markdown note of 10,000 words with headings, nested lists, tables, links,
  numbers and a code block is prepared with zero `preparation_limit` regions.
- **SC-003**: Every existing feature 008 time and memory assertion passes unchanged, including the
  pathological inputs measured under memory tracing (under 2 seconds and 128 MiB each).
- **SC-004**: All 54 segmentation corpus cases keep their expected outcome, and the full existing
  test suite passes, apart from fixtures that relied on the old fixed bound to reach a limit. Each of
  those is listed and justified in the plan before it changes, and still reaches its limit afterwards.
- **SC-005**: On the reported 48,400-code-point note, re-run privately by the owner, no region is
  unresolved for `preparation_limit` or `unsafe_boundary`. Remaining unresolved regions have other
  named reasons. Only counts and reasons are recorded, never source text.

## Assumptions

- The owner asked for length-scaled budgets. Planning measured that pathological inputs of the same
  length as ordinary notes cost about as much work per code point, so only an absolute bound protects
  the existing time assertions; above about 3,600 code points a length-scaled bound with that ceiling
  equals the ceiling. The plan therefore uses a raised absolute bound (research R1–R2). The owner
  accepted this deviation, together with the narrowed boundary rule (R3), on 2026-10-22.
- The existing 120-second deadline remains the only time-based stop besides the work bound.
- Feature 008's time and memory assertions stay unchanged; fixtures that only reached a limit because
  of the old 4,096 work bound may grow so they still reach a limit (research R5).
- No sentence begins with a comma, semicolon, colon or terminal punctuation mark, so FR-005 cannot
  merge two real sentences. FR-006 keeps feature 008's conservative treatment of a missing space.
- Out of scope: breadth-first scheduling, chunked or resumable evaluation, request preflight,
  continuing after an invalid response, structural exclusions for headings and label–value lines,
  the T4 lexical gate, the `ambiguous_url_closer` rule and exit-code documentation. These were found
  in the same investigation and need separate owner decisions.
- No real user text is committed. The reported note is used only for SC-005, run locally by the owner.
