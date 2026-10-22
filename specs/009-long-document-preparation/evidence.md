# Evidence — feature 009

All runs are local, network-free and use synthetic text. No key was read and TypeSafe was not
contacted. Raw prose of the private reported note is never recorded here.

## Authority

The owner authorized implementation of T001–T007 (Setup, Foundational, US1) on 2026-10-22, without
commit or push. US2, US3, Polish, commits, push, merge and release remain unauthorized.

## T001 — starting state

- Revision: `8a698e8` (spec commit on `feed64d`), branch `codex/009-long-document-preparation`.
- Environment: Python 3.15.0, Apple M1 Pro, Darwin 25.6.0.
- Runner: `jev-1.14.0`, segmentation profile `vi-spans-1`, work budgets 4,096 (metadata and scan).
- Full suite, `python3 -B -m unittest discover -s tests -t .`: `Ran 184 tests in 103.122s`, `OK`.
- RED baseline, quickstart section 1: `Ran 4 tests`, `FAILED (failures=4)`. Recorded output in
  [baseline/red-output.txt](baseline/red-output.txt):
  - `test_bullet_with_relative_link_and_trailing_colon_is_exact`: unresolved `unsafe_boundary` region.
  - `test_long_markdown_crosses_scan_budget_without_preparation_limit`: `preparation_limit` found.
  - `test_many_short_units_do_not_exhaust_metadata_budget`: `0 not greater than 0` units.
  - `test_quoted_question_followed_by_comma_is_not_a_boundary`: unresolved `unsafe_boundary` region.

## T002–T003 — explicit inventory cap

- T002 added `test_inventory_cap_keeps_prefix_and_reports_remainder` to `tests/test_structure.py`
  (50 paragraphs × 100 sentences, 5,050 items). Before T003 it passed only because the scan budget
  stopped scanning at 1,024 sentences. This is a guard, not a behavioral RED.
- T003 added `WORK_LIMIT = 4096` (both work budgets) and an inventory counter of
  `MAX_INVENTORY - len(sections)` slots charged per emitted span in `jev/preparation.py`. The guard
  now patches `WORK_LIMIT` to `2**20`, so only the cap can stop it.
- Counter disabled by a local patch (`_scan` called with `inventory=None`):
  `AssertionError: 5050 not less than or equal to 4096`, `FAILED (failures=1)`.
- Counter enabled: `OK`; 50 units + 4,046 sentences = 4,096.
- Full suite after T003: `Ran 185 tests in 86.127s`, `OK`. Behavior unchanged at 4,096 work.

## T004–T005 — US1 tests

- T004 added `LongDocumentTest` to `tests/test_preparation_limits.py`: the two baseline cases
  moved from `baseline/test_red_baseline.py`, plus `test_ten_thousand_word_note_is_fully_prepared`
  (121 sections, 10,052 words, 48,761 code points; `#`–`###` headings, bullets nested three levels,
  a `|`-table per section, absolute links, the token set `p50/p95`, `1.000`, `±10%`, `v0.4.19`,
  `91,4%`, `Recall@k`, and one fenced block annotated as protected). Counts fixed from the generator:
  7 units per section + title + fence = 849 units; 6 sentences per section = 726.
- Deviation, recorded deliberately: the note's relative link is `[ghi chú](ghi-chu-{n})`, without a
  dot. A dotted relative destination (`ghi-chu.md`) is US2 behavior and would make this US1 test
  depend on US2. Dotted relative links are covered by T008.
- RED before T006: `Ran 3 tests`, `FAILED (failures=3)`:
  - long note: `'preparation_limit' unexpectedly found`;
  - ~480 units: `0 not greater than 0` (metadata exhaustion, zero units);
  - 10,000-word note: `'preparation_incomplete' != 'prepared'` (metadata exhaustion, zero units).
- T005 grew the fixture of `test_scan_limit_keeps_classified_exact_prefix_and_context` in
  `tests/test_review_boundaries.py` from `'Tôi về. '*1100` to `'Tôi về. '*4200` and asserted the
  `preparation_limit` reason. It passes before T006 too (scan budget limit), as expected.

## T006 — work bound raised to 32,768

- `jev/preparation.py`: `WORK_LIMIT = 32768`; no length term; `MAX_INVENTORY = 4096` unchanged.
- T004 and T005 tests, plus `MetadataLimitTest`: `Ran 6 tests in 2.366s`, `OK`.
- Corpus after T006 and before any US2 change: `tests/test_preparation`, `Ran 1 test`, `OK`
  (54 cases, identical spans; US3 scenario 2).

## T007 — verification: BLOCKED, time margin insufficient

Machine load during these runs: load average 60–109 on 10 cores (other processes, not this
session's tests). Research R2 measured 0.90 s for the tracemalloc pathological case on an idle
machine and assumed a 2× margin. Under this load:

- Subprocess timing of `X. ` × 250,000 under tracemalloc, five runs each, same load window:
  - `WORK_LIMIT = 4096`: 0.206–0.320 s.
  - `WORK_LIMIT = 16384`: 1.16–1.89 s.
  - `WORK_LIMIT = 32768`: 2.134–3.763 s.
- Repeating `test_huge_tokens_have_linear_marker_dispatch` and
  `test_large_input_bounded_inventory_and_accounting` six times: 6 of 6 runs failed at least one
  assertion (`3.09 not less than 2`, `4.72 not less than 2.0`, one `TimeoutExpired` after 4 s).
- Full suite after T006: `Ran 188 tests in 100.802s`, `FAILED (failures=1)`:
  `test_large_input_bounded_inventory_and_accounting`, `4.180941459024325 not less than 2.0`.
- One earlier run of `tests.test_structure tests.test_coverage_scaling tests.test_preparation_limits`
  passed (`Ran 18 tests`, `OK`, scaling elapsed 1.791 s), so the result is load-dependent, not a
  deterministic failure.

Per T007, the time assertions were not loosened. SC-003 is not met on a loaded machine. Owner
decision needed before continuing (see the session report): reduce the pathological cost per work
unit, change the bound, or accept the assertions as load-sensitive.

## T006a — charge the work actually done (R2 addendum, owner-accepted)

- RED first: `WorkChargeTest.test_initials_and_punctuation_cost_more_than_plain_words` in
  `tests/test_preparation_limits.py` measures scan work charged inside `_scan`.
  Before: `AssertionError: 3001 not greater than or equal to 8004` (`X. ` × 1,000: 3,001 units;
  `chữ ` × 1,000: 2,001 units; 1.5×).
- Change in `jev/preparation.py`: `_WorkBudget.take(amount=1)`; one unit per initials lookahead step;
  three extra units (four in total) per terminal-punctuation event, charged after the `inside()` and
  parenthesis checks. `WORK_LIMIT = 32768` and the quarter-of-remaining token allowance unchanged.
- After: 9,995 versus 2,001 units (4.99×). The test threshold is 4× (task T006a records why).
- Also restored `ID = re.compile(...)` in `jev/preparation.py`: the T003 edit had dropped the
  space after `=`. Whitespace only.
- `tests.test_preparation_limits`, the T005 fixture test and `tests.test_preparation` (54 corpus
  cases): `Ran 8 tests in 2.498s`, `OK`.

## T007 rerun after T006a

- Full suite: `Ran 189 tests in 132.702s`, `OK`; scaling test elapsed 0.403 s. Load average 50–60.
- Corpus after T006/T006a, before any US2 change: 54 cases, identical spans (part of the full suite).
- Tracemalloc subprocess timings, maximum of three runs each (load average about 60 rising to 115):
  `a`×49,000 0.009 s; `7`×49,000 0.033 s; `X. `×250,000 0.413 s (was 3.174 s after T006 alone);
  `A. `×330,000 0.331 s. Peak memory at most 2.5 MiB.
- Six-repeat loop of `test_huge_tokens_have_linear_marker_dispatch` and
  `test_large_input_bounded_inventory_and_accounting`, run as load average jumped from about 60 to
  115: the first three runs failed (`2.14 not less than 2.0`, `5.95 not less than 2.0`, and a run
  with `4.87 not less than 2.0` plus a 4 s `TimeoutExpired`); the last three passed (0.31–0.50 s).
  The old code was not measured during that spike, so these failures cannot be attributed.
- Interleaved comparison right after, eight rounds, load average 99–115, code at `feed64d` and the
  current branch run back to back each round: both 8 of 8 passed. Scaling test elapsed: old
  0.150–0.330 s, current 0.229–0.738 s (about 1.4–2.2× the old code).

Status at that point: SC-003 assertions passed in the full suite and in every interleaved round;
three failures occurred during a load spike with no baseline measured. Per T007's stop rule this was
reported, not waived, and the owner asked for confirmation on an idle machine.

### T007 confirmation on an idle machine (owner-requested)

The owner reduced machine load. A wait loop held the run until the 1-minute load average fell below
8 on this 8-core machine (reached 7.91 after 790 s). The earlier notes in this file said 10 cores;
`hw.ncpu` reports 8.

- Six-repeat loop of both 008 time tests, load average 7.5–7.6: 6 of 6 `OK`; scaling test elapsed
  0.202–0.298 s.
- Interleaved comparison, eight rounds, load average 7.0–7.6: old code 8 of 8 `OK` (0.116–0.201 s),
  current branch 8 of 8 `OK` (0.198–0.224 s).
- Tracemalloc subprocess timings, maximum of three runs, current versus old code:
  `a`×49,000 0.010 vs 0.010 s; `7`×49,000 0.009 vs 0.009 s; `X. `×250,000 0.212 vs 0.112 s;
  `A. `×330,000 0.232 vs 0.196 s. Peak memory 2.3–2.5 MiB versus 1.5–2.0 MiB, far under 128 MiB.
- The unresolved reason for `X. `×250,000 and `A. `×330,000 changed from `ambiguous_abbreviation`
  to `preparation_limit`: the lookahead charge now exhausts the work bound before the boundary pass.
  Both are unresolved regions; no assertion depends on the reason, and the new one names the cause.
- Full suite: `Ran 189 tests in 47.089s`, `OK`; scaling test elapsed 0.209 s.

T007 passes: every feature 008 time and memory assertion holds unchanged, with the current branch
at 0.2–0.3 s against a 2 s limit. The load-spike failures above remain recorded as a risk on heavily
loaded machines.
