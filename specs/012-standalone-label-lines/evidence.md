# Evidence — feature 012

Authority: on 2026-10-23 the owner chose the short path (plan and tasks in one pass, no
`speckit-analyze`, test-first implementation, short independent review, verified findings fixed, no
commit). No key, network, live service or real user text is used.

## T001 — starting state

- Branch `codex/012-standalone-label-lines` from `main` at `abedaad` (feature 011 merged as PR #21),
  with the uncommitted calibration entry of 2026-10-23 and the 011 T023 part b record.
- Python 3.15.0 on Darwin arm64.
- `python3 -B -m unittest discover -s tests -t .`: `Ran 253 tests`, `OK`.

## T002–T004 — tests first

- RED, `tests/test_label_value.py` (User Story 1): 25 failures, every one because the standalone line
  was recognized as prose (`None` instead of `label_value`): the eight owner-rated `STANDALONE` lines
  as a paragraph, as a single list item and between other paragraphs, and lines separated by single
  line breaks.
- RED, `tests/test_structural_exclusions.py`: 3 failures for the intended reasons. `V11RuleTest` still
  asked V11 about the lone date line; the mixed-list block yielded `[[None], [None]]`; the standalone
  `Lưu ý: Điều này có nghĩa là …` line was not a label.
- Guards that passed before the change (User Story 2): each standalone line placed on the same line
  as another sentence (32 cases, prose and list items), a hard-wrapped sentence starting mid-line and
  a blockquote stay prose. The feature 011 forms and form-based rejections kept passing.
- Seven lines moved from `NOT_LABEL` to `STANDALONE` by design (plan, expected changes).

## T003 — implementation

`jev.preparation._standalone` and a second pass in `_mark_label_values`: a sentence of a prose or list
section that starts at a line start (after the list marker for the item's first sentence, or after
indentation), ends at a line end and starts with a plain label (`PLAIN_LABEL`, not `LEAD_IN`) is a
label–value line. The feature 011 pass runs first and is unchanged.

- `python3 -B -m unittest tests.test_label_value tests.test_structural_exclusions`: `Ran 27 tests`,
  `OK`.

## T005 — contract

`references/typesafe-advisor.md` now names the standalone form with one example of each side and no
longer says a lone `Nhãn: giá trị` line stays prose.

## T007 — short independent review

A separate agent reviewed the diff against the spec and plan (read-only, offline). It found no
blocking bug and confirmed CRLF endings, continuation lines, nested and ordered lists, hard-wrapped
prose, `>` lines, code fences, missing values, `rằng`/`là` and the boundary with the 011 forms. Each
finding was reproduced before acting.

| # | Finding | Disposition |
|---|---|---|
| 1 | should-fix: a standalone bold label on a later line (`Ngày: hôm nay.` / `**Trạng thái:** xong.`) or a continuation line was prose, so the bold form lost to the plain one | Fixed test-first: `test_standalone_bold_label_after_the_first_line` failed (`[label_value, None, label_value]`), then passed after the standalone pass also reads `BOLD_LABEL`, with the same `LEAD_IN` check (a bold `Cần lưu ý rằng:` stays prose) |
| 2 | note: a blockquote's lazy continuation line without `>` is labelled, which the contract did not say | Contract corrected: a line starting with `>` is never a label line; a lazy continuation line is read as prose by segmentation. Behaviour kept |
| 3 | note: an indented code block and setext headings, which segmentation already reads as prose, can now be labelled | Kept: segmentation behaviour from before 012; only removes a V11 question; headings skip V11 anyway |
| 4 | note: one over-long line in the contract paragraph | Fixed |
| — | cost: `_standalone` is quadratic on one long line, but sentences are capped; 850 KB single line, 3,276 sentences: 0.135 s | No action |

## T006 — checks

- `python3 -B -m unittest discover -s tests -t .` after the T003 change: `Ran 258 tests`, `OK`.
  The ~1,000-word guard (`test_required_counts_and_check_order`) still requires 7,001 checks with the
  same check order, so no pattern changed on that note (SC-004).
- After the review fix: `Ran 259 tests`, `OK`; `build-jev-registry.py --check`, `validate-package.py`
  and `package-plugin.py` exit 0; `git diff --check` clean. Nothing is committed.
