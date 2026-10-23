# Evidence — feature 013

Authority: on 2026-10-23 the owner asked to clear the small technical debt and chose the short path
(as for 012). No key, network, live service or real user text is used; CLI tests set a placeholder
key value only so the input path is read.

## T001 — starting state

- Worktree `.claude/worktrees/013-runner-cleanup`, branch `codex/013-runner-cleanup` from `main` at
  `abedaad`. Python 3.15.0 on Darwin arm64.
- `python3 -B -m unittest discover -s tests -t .`: `Ran 253 tests`, `OK`.
- Ledger build on 2,100 units (`note(300)` from `tests/test_structural_exclusions.py`): 45,271 groups,
  0.16–0.20 s; 1,094 sentences prepared, 983 `preparation_limit` regions.

## T002–T003 — links and URLs with parentheses (User Story 1)

- RED: 5 failures, each `ambiguous_url_closer` instead of exact sentences: the Wikipedia link, the
  bare Wikipedia URL, `(https://example.org/a)`, `(xem https://x.org/a_(b)).` and the feature 009 test
  case `Xem [a](b(c).md) nhé.` (renamed `test_balanced_parenthesis_inside_destination_is_exact`). The
  unbalanced forms and the 400,000-character parenthesis tokens passed before the change (guards).
- First GREEN attempt also settled bare URLs that keep balanced parentheses (GFM). The annotated
  fixture `url-ambiguous-closer` (`Xem https://example.org/a(b). Mai tính.`) then failed. Its
  README forbids changing a label to fit the scanner, so the scanner was narrowed instead: a bare URL
  that keeps a parenthesis stays ambiguous; only an unmatched trailing `)` is settled. The bare
  Wikipedia URL and `(xem https://x.org/a_(b)).` moved to the ambiguous expectations; the link form
  `(xem [bài](https://x.org/a_(b))). Câu sau.` replaced the latter as a resolvable case and fails on
  the pre-change code (`([], ['ambiguous_url_closer'])`). Spec scenario 6, FR-002 and SC-001 record
  the narrowing.
- Work budget: charging every address changed preparation on 2,100 units (1,090 sentences instead
  of 1,094). A no-parenthesis fast path charges nothing extra; parity restored (1,094 sentences,
  45,271 groups).
- `python3 -B -m unittest tests.test_preparation`: `Ran 11 tests`, `OK`.

## T004–T005 — unreadable input (User Story 2)

- RED: `test_cli_unreadable_input_has_its_own_status` failed for `evaluate` and `prepare` on a
  missing path (`{'status': 'invalid_input'}`); malformed input and the no-key case passed (guards).
- GREEN: `jev/__main__.py` reports `{"status": "input_unreadable"}`, exit 2, for an `OSError` while
  opening or reading input. `python3 -B -m unittest tests.test_jev`: `Ran 33 tests`, `OK`.

## T006 — one editable-text helper (User Story 3)

`jev/coverage.py` imports `core.editable_text` and computes it at most once per unit; `_editable` is
removed. Ledger build on 2,100 units: 45,271 groups, 0.16–0.25 s on both `main` and this branch,
so there is no measurable speed change; the gain is one definition instead of two.

## T007 — contract

`references/typesafe-advisor.md` describes link and bare-URL parentheses and lists `input_unreadable`.

## T008 — short independent review

A separate agent reviewed the worktree read-only and compared 41 inputs against `origin/main`. Each
finding was reproduced before acting; fixes were test-first.

| # | Finding | Disposition |
|---|---|---|
| 1 | should-fix: `_closing_parenthesis` ignored backslash escapes, so `\)` closed a destination; `Xem [a](https://x.org/a\)b.) Nam nói vậy.` became two exact sentences (main: `ambiguous_parenthesis`) | Fixed: `test_escaped_parentheses_do_not_close_a_destination` failed on three inputs, then passed after escapes are consumed whole (CommonMark); the fast path now also requires no backslash. The relative-destination form had the same fault on `main` and is fixed too |
| 2 | should-fix: with standard input closed, `sys.stdin` is `None` and the CLI crashed (exit 1, traceback); present on `main` but inside FR-006 | Fixed: the CLI test failed with `(1, None)`, then reported `input_unreadable`, exit 2 |
| 3 | note: in a token holding two links, only the first destination is opaque; the second is read as prose. No wrong exact boundary was reproduced: results are `ambiguous_parenthesis` or `ambiguous_separator` (main: `ambiguous_url_closer` for the whole unit) | Kept: errs toward unresolved; noted for later |
| 4 | note: an image `![ảnh](https://x.org/a.png) nhé.` stays `ambiguous_separator` because of the `!` before `[`; unchanged from `main` | Kept: out of scope |

Verified without finding (reviewer): the six scenarios, nested, title and angle-bracket destinations,
links in prose parentheses, GFM trailing mixes (`).`, `.)`, `)]`, `”)`, `))`), bare URLs keeping a
parenthesis, budget parity on text without parentheses, missing file, directory and `chmod 000`
input, oversized and malformed input, no key, and editable-text parity in the ledger.

## T009 — checks

- `python3 -B -m unittest discover -s tests -t .` after T003–T006: `Ran 257 tests`, `OK`, including the
  check-order guard (7,001 checks) and the annotated segmentation corpus.
- After the review fixes: `Ran 258 tests`, `OK`; 2,100 units prepare 1,094 sentences and build 45,271
  groups, as on `main`; `build-jev-registry.py --check`, `validate-package.py` and
  `package-plugin.py` exit 0; `git diff --check` clean. Nothing is committed.
