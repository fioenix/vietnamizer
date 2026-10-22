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

## T008–T013 — US2 boundary exemptions

Machine idle during these runs (load average 6–7 on 8 cores).

- T008 RED: `SegmentationDeltaTests` in `tests/test_preparation.py`, one case per contract row, with
  expected sentence texts written from the contract (not read from the scanner). Before any change:
  `Ran 4 tests`, `FAILED (failures=12)`; every failure reported `unsafe_boundary` (for example
  `(['Xem example.dev.', 'Tôi về.'], []) != (['Tôi về.'], ['unsafe_boundary'])`). The corpus passed.
  The two baseline cases from `baseline/test_red_baseline.py` are rows of this test.
- T009: `test_dotted_identifier_tokens_stay_linear` in `tests/test_structure.py` (`'a'*500000+'.b'+'é'`
  and `'ab.'*200000+'abé'`, tracemalloc, 2 s limit). It passed before T011 because no recognizer
  existed, so it is a guard. Proof that it detects a regression: with a deliberately naive pattern
  without the lookbehind, preparation took 3.58 s at 20,003 code points and 13.92 s at 40,003
  (quadratic); the guard's 500,002-code-point input would fail. With the real pattern: `OK`.
- T010: missing separator now reports `ambiguous_separator`; `,` `;` `:` and further terminal
  punctuation after the closers are not a boundary. The exemption sits after the boundary-override
  check, so an explicit override at that endpoint still wins. After T010: 6 failures left, all
  needing T011–T012.
- T011: `DOTTED_IDENTIFIER` lexical token, one work unit per match.
- Regression found and fixed during T011, with a test first: the token made `Dùng e.g. Python rồi
  chạy.` split into two exact sentences, where `HEAD` left it unresolved (`unsafe_boundary`, checked
  by running the `HEAD` module). New test `test_single_letter_dotted_abbreviation_stays_ambiguous`
  failed (`(['Dùng e.g.', 'Python rồi chạy.'], [])`). Fix: a standalone run of single lowercase letters
  joined by dots (`e.g.`, `i.e.`) is `ambiguous_abbreviation`, like `v.v.`/`v.d.`. A first version also
  matched the URL path in corpus case `url-terminal-period` (`[[0, 28], [29, 38]] != []`); requiring
  the abbreviation to follow whitespace or an opener fixed it. Recorded in
  `contracts/segmentation-delta.md` (row 2). This extends the accepted contract; the owner accepted it on 2026-10-22.
- T012: Markdown link destinations of any scheme are opaque; a `(` inside keeps `ambiguous_url_closer`.
- T013: `tests.test_preparation`: `Ran 5 tests`, `OK` (54 corpus cases, no label changed).
  Full suite: `Ran 194 tests in 36.681s`, `OK`. RED baseline file: `Ran 4 tests`, `OK`.
  008 time tests plus the new guard, three repeats: all `OK`, scaling 0.281–0.318 s (0.198–0.224 s
  before US2; the identifier search on dotted tokens adds about 40% on `X. `×250,000, still far under 2 s).
- Not yet done: US3 (profile `vi-spans-2`) must land before integration, because boundary decisions
  changed under the `vi-spans-1` name.

## T014–T016 — US3 profile `vi-spans-2`

- The owner accepted the single-letter abbreviation extension (contract delta, row 2) on 2026-10-22.
- T014 RED: `ProfileBindingTest` in `tests/test_coverage_model.py`. Before the change:
  `AssertionError: 'vi-spans-1' != 'vi-spans-2'`, and the manifest digest stayed identical when
  `jev.preparation.PROFILE_VERSION` was patched (`'7b5d4dc3…' == '7b5d4dc3…'`), because
  `jev/coverage.py` hard-coded `'vi-spans-1'`.
- T015: `PROFILE_VERSION = 'vi-spans-2'` and docstring in `jev/preparation.py`. `jev/coverage.py`
  now binds `prepared['segmentation_profile']`. Deviation from the task wording: importing the
  constant into `coverage.py` would copy it at import time, so the manifest would not follow the
  profile actually used. Both `Ledger(...)` call sites in `jev/core.py` pass `prepare_document` output,
  which always carries `segmentation_profile`. `tests.test_coverage_model`: `Ran 5 tests`, `OK`.
- T016: `tests/fixtures/segmentation/cases.json` `profile` set to `vi-spans-2`; the README describes
  the delta. No case text, span or label changed (54 cases).
- US3 independent test, current branch versus the `HEAD` module on one Markdown input: profiles
  `vi-spans-1` → `vi-spans-2`; the two unaffected sentences keep spans (11, 18) and (19, 29) and both
  get new IDs; the list item with `[ghi chú](ghi-chu.md)` changes from `unresolved` to `exact`, which is
  where the US2 rules apply.
- Full suite: `Ran 196 tests in 65.231s`, `OK` (load average about 14; scaling 0.321 s).
  `python3 scripts/validate-package.py`: valid, 55 patterns.

## T017–T019 — documentation, baseline and package checks

- T017: `references/typesafe-advisor.md` limits paragraph now states the absolute work bound per
  preparation phase, the 4,096 units-plus-sentences cap, that ordinary notes of up to 10,000 words
  prepare fully while notes of roughly 12,000–17,000 words or more (or punctuation-dense text) may
  still hit `preparation_limit`, that full preparation does not mean full evaluation, and the
  `ambiguous_separator` reason.
- T018: RED baseline command (quickstart section 1): `Ran 4 tests`, `OK`. The baseline file's
  docstring now says it is superseded by `LongDocumentTest` and `SegmentationDeltaTests`.
- T019 (load average about 13):
  - Full suite: `Ran 196 tests in 43.169s`, `OK`; scaling 0.285 s.
  - `python3 scripts/validate-package.py`: exit 0, "Gói vietnamizer v0.10.6 hợp lệ, gồm 55 pattern".
  - `python3 -B scripts/build-jev-registry.py --check`: exit 0, "55 pattern definitions match
    canonical sources" (registry unchanged, no regeneration).
  - `python3 scripts/package-plugin.py`: exit 0, "Plugin archive validated" and "Distribution
    metadata valid for Codex and Claude Code". It rebuilt all three archives in the git-ignored
    `dist/`, replacing the local builds from 2026-10-19; nothing in `dist/` is committed.
  - Archive parity: `jev/preparation.py`, `jev/coverage.py`, `jev/registry.json` and
    `references/typesafe-advisor.md` are byte-identical (SHA-256) to the source in
    `vietnamizer.skill`, `vietnamizer-claude-org.zip` and `vietnamizer-plugin.zip`; none of the
    archives contains `tests/` or `specs/`.
  - Smoke test from the extracted `vietnamizer.skill`: `python3 -B -m jev prepare` on a synthetic
    Markdown note with `README.md`, `jev.core`, a relative link and `"xong chưa?",` returned
    `prepared`, 2 sentences, no unresolved region, exit 0.

## T020 — independent code and security review

Reviewer: a separate read-only agent, given `git diff feed64d..HEAD -- jev/`, the tests, spec,
research and both segmentation contracts; it worked in a throwaway copy, contacted no service and
read no credentials. Every finding below was reproduced again in this session before recording.

| ID | Severity | Finding | Reproduction (old `feed64d` → current branch) | Disposition |
|---|---|---|---|---|
| B1 | Blocking | `DOTTED_IDENTIFIER` swallows single-letter chains, so capitalised or non-standalone abbreviations get a false exact boundary | `Dùng E.g. Python rồi chạy.`: old `ambiguous_abbreviation` → new two exact sentences; same for `Gọi I.e. Tôi về.`, `Ví dụ:e.g. Python chạy.`, `Dùng 'e.g. Python rồi.` | Fix required before merge: exclude chains of single-letter segments from the identifier token, so they keep the conservative path; add these four cases as tests |
| S1 | Should-fix | Plain-ASCII Vietnamese words and digits with a missing space are certified as one merged sentence, and a host boundary override inside an identifier or link destination now fails the whole document with `invalid_input` | `Tôi gặp anh.con mèo chạy.` and `Năm 2025.sau đó tôi về.`: old unresolved → new one exact sentence. Override `[12]` on the first: old two exact sentences → new `invalid_input`; override `[10]` in `Xem [a](b.md) nhé. Tôi về.`: same | Owner decision: R3 accepted merging unaccented typos, but many Vietnamese words are plain ASCII, so the trade-off is broader than recorded. The override regression is a defect either way |
| S2 | Should-fix (robustness) | Override validation `any(a<n<b for a,b in lexical)` is quadratic, uncharged and never checks the deadline; more lexical spans now make it larger | 4,000 overrides: old 0.03 s → new 1.08 s; 8,000: old 0.00 s → new 3.30 s. Reviewer: about 32,000 overrides in a 384 KB input ran 39.4 s, and 14–16 s with a 5 s deadline | Fix required: validate with bisect over sorted spans, charge work and check the deadline per override; precompute section owners |
| N1 | Nit | The 64-character tail window can start mid-run, so very long single-letter chains may be marked ambiguous | conservative only | Accept |
| N2 | Nit | An unclosed destination strips fewer trailing characters than it could | only more lexical, never a false boundary | Accept |

Checked without issue (reviewer and this session): partition reconstruction with quotes, brackets,
emphasis and multiple links per token; overrides still win at both endpoint positions; inventory
cap; no catastrophic backtracking in the new patterns (1 MiB inputs under 0.1 s); only
`invalid_input` escapes; diagnostics carry offsets and reasons, not protected text; `jev/core.py`
has no consumer of the old reason strings and both `Ledger` call sites receive `segmentation_profile`.

Status: review done and recorded. B1 and S2 need fixes; S1 needs an owner decision. Feature 009 is
not ready to merge until B1 and S2 are fixed and S1 is decided.

## T022–T024 — review fixes (owner decision on S1)

The owner chose to narrow the dotted-identifier token to a suffix allowlist and to let host
overrides win inside identifier and link-destination spans, and asked for B1 and S2 to be fixed
test-first.

- T022 RED, `tests/test_preparation.py`: 8 tests, `FAILED (failures=7, errors=1)`:
  `Tôi gặp anh.con mèo chạy.`, `Năm 2025.sau đó tôi về.`, `Mở jev.core nhé.` were certified exact;
  `Dùng E.g.`, `Gọi I.e.`, `Ví dụ:e.g.`, `Dùng 'e.g.` were certified exact; the README.md override
  raised `ValueError: invalid_input`.
- T022 change in `jev/preparation.py`: `DOTTED_IDENTIFIER` now requires a last segment from
  `IDENTIFIER_SUFFIXES` (md, txt, py, js, ts, json, yaml, yml, toml, csv, html, css, sh, sql, xml,
  pdf, png, jpg, svg, ipynb, dev, com, org, net, io, vn). Identifier and link-destination spans go to
  a `soft` list: still opaque for boundary search, but excluded from override validation. B1 is fixed
  by the same narrowing, since single-letter chains no longer match.
- Two existing tests changed as a consequence, both recorded in the contract delta: the `jev.core`
  row became `main.py` (module paths are no longer recognized), and the `e.g.`/`i.e.` test now
  expects `ambiguous_separator` (the inner dot is reported first; still unresolved). The final-dot
  abbreviation rule is still needed: with it removed in a scratch copy, `Python rồi chạy.` after
  `e.g.` was certified exact.
- T023 RED, `test_many_overrides_validate_quickly` in `tests/test_structure.py` (20,000 overrides,
  tracemalloc, 2 s limit): one parent with 8,000 number spans timed out after 10 s
  (`TimeoutExpired`); 3,001 parents took 4.46 s.
- T023 change: override validation merges hard lexical spans on strict overlap only (an endpoint
  shared by adjacent spans stays outside both), finds the candidate span by bisect, and charges one
  work unit and checks the deadline per override. Section ownership and per-section override lists
  use bisect over sorted overrides. After: 0.645 s and 0.531 s; both end in `preparation_limit`
  because overrides are now charged as work. Overrides inside a number (`Bản 1.5 xong.`, override 6)
  or a URL (override 26) still raise `invalid_input`; one inside `a.md` splits there.
- T024: contract delta updated (allowlist, host override precedence, changed and added rows); spec
  FR-007 and research R3 note the narrowing. Full suite: `Ran 200 tests in 49.672s`, `OK` (load
  average 14–19; scaling 0.348 s). RED baseline file: `Ran 4 tests`, `OK`. `validate-package.py`,
  `build-jev-registry.py --check` and `package-plugin.py`: exit 0. All three rebuilt archives in the
  git-ignored `dist/` hold byte-identical `jev/preparation.py`, `jev/coverage.py`, `jev/registry.json`
  and `references/typesafe-advisor.md`.
- Open: T021 (owner-only private-note check) should run on this final code, since the allowlist
  changes which tokens in a real note are recognized.

### T023 follow-up found while committing (2026-10-22)

While building the atomic commits, the full suite at the T023 stage failed once under load
(load average about 24–31, other processes using about 270% CPU): `7.09 not less than 2` (1 parent)
and `3.70 not less than 2` (3,001 parents). Run alone it passed. Investigation:

- Timing of the T023 scenarios under tracemalloc, four runs each at load about 25: 0.67–0.99 s
  (1 parent) and 0.65–1.35 s (3,001 parents); a 10,000-override variant took up to 1.35 s. Too
  little margin against 2 s.
- A 1,001-parent scenario exposed a second quadratic cost: with both the old and the T023 code it
  ran over 30 s. Profiling showed `json.dumps` called 4,097 times for 0.78 s of 1.03 s at only 4,000
  overrides: every sentence id hashed the full override list (`_digest([...,overrides])`), so the
  cost was sentences × overrides. Feature 008 had this too, but its 4,096 work bound kept both
  counts small.
- Test first: the 1,001-parent case was added to `test_many_overrides_validate_quickly` and failed
  (`TimeoutExpired` after 10 s). Fix: compute `overrides_digest` once and bind it into each sentence
  id. The binding is equivalent, and sentence ids already change with `vi-spans-2`.
- Without tracemalloc the new code takes 0.04–0.14 s in all three scenarios, against 5.1–10.2 s or
  more than 20 s for the pre-T023 code (load 18–26). With tracemalloc the remaining 1.3–2.6 s for
  1,001 parents was allocation overhead, not override work (0.19 s under cProfile alone). The test
  now measures wall time without tracemalloc, because it guards work per override, not memory;
  the other tracemalloc tests are unchanged.
- At commit `1841b48`: full suite `Ran 200 tests in 78.715s`, `OK`. Afterwards
  `validate-package.py`, `build-jev-registry.py --check` and `package-plugin.py` exited 0, the three
  rebuilt archives hold byte-identical changed files, and the RED baseline file passes (4 tests).

## T021 — owner check on the private reported note (SC-005)

Run by the owner on 2026-10-22 at `c08b438`, local `prepare` only, no key and no network. Only
counts and reason codes are recorded; no text from the note.

- The note has changed since the opening session: 49,602 code points now (48,400 at the start;
  58,567 bytes against 57,110). Counts are therefore not directly comparable with the prototype run.
- Input built as in the opening session (technical profile, the first ```` ```text ```` fence annotated as
  protected, context reviewed).
- First attempt reported `invalid_input` because the session scratchpad, including the old
  `input.json`, had been removed; the CLI reports an unreadable input file as `invalid_input`. Not a
  feature 009 defect; noted as a possible separate improvement.
- Result: `preparation_incomplete`, 281 units, 382 sentences, unresolved reasons
  `{'ambiguous_url_closer': 1}`.
- Before feature 009 (opening session, earlier version of the note): 168 `preparation_limit` regions,
  1 `unsafe_boundary`, 94 sentences.

SC-005 met: no `preparation_limit` and no `unsafe_boundary` region. The remaining
`ambiguous_url_closer` region (a URL containing parentheses) is out of scope for this feature.
`preparation_incomplete` reflects that one region, not a limit.
