# Validation guide — feature 010

Run every command from the repository root. No key or network is needed: evaluation tests use the
fake transports in `tests/`. Nothing here contacts TypeSafe; a live run needs the owner's spend
approval and synthetic text only.

## 1. RED before the change

Each acceptance scenario in [spec.md](spec.md) gets a synthetic test before the code it covers.
Before implementation they fail for the intended reason:

- plan fields absent from `prepare` (User Story 2);
- depth-first order reaches 9 units in the ~1,000-word note (User Story 1, SC-004);
- the run stops at the first invalid reply (User Story 4);
- an `evaluation.previous` block is ignored (User Story 3).

Record the failing output in `evidence.md` with the commit it ran on.

## 2. Full suite

```bash
python3 -B -m unittest discover -s tests -t .
```

Expected: every test passes. Two pre-existing tests change with the contract, and no other:
`tests/test_coverage_faults.py` (continue after an invalid reply, research R6) and the
`limit_exceeded` assertion in `tests/test_jev.py` (now `budget_exhausted`, research R7). Time,
memory, privacy and limit assertions keep their thresholds.

## 3. Plan equals run (SC-001) — deferred with User Story 2

For the ~1,000, ~6,000 and ~12,100-word synthetic notes, each with no `evaluation` object, with a
budget of 8, and with focus spans plus candidate edits: compare `prepare`'s `priority.plan` with the
receipts of `evaluate` under an always-valid fake transport. Requests, units and per-tier counts
must be identical.

## 4. Ordering and spread (SC-002 to SC-004)

- Candidate edits in the last unit and two focus spans, budget 8: no request opened for tier 3 or 4
  before every tier 1 and tier 2 check is sent.
- Signal text (for example `, và ` in some units only), no candidates or focus: the T4 checks of
  those units are sent before any tier 4 request.
- No `evaluation` object, ~1,000-word note: validated answers in at least 30 units.

## 5. Chained runs and invalid replies (SC-005, SC-006)

The chained-run and previous-block items are deferred with User Story 3; until then any
`evaluation.previous` is `invalid_input`. The invalid-reply items apply.

- Two runs, the second given the first report's `answered_checks`: no reuse key in both runs' `own`
  lists; the second report counts only its own answers and lists skipped checks as
  `answered_previously`.
- Without focus or candidates, the second run's tier 4 requests go to units the first run did not
  reach before any unit it reached.
- A previous block with a changed model, registry digest, profile, scope, an `own` key missing from
  `receipts`, a malformed or duplicate key, a receipt index out of range, or more than 1,536 `own`
  keys: `invalid_input`, zero transport calls.
- An expired deadline during planning: no request is sent and the plan is reported with
  `deadline_exceeded` (research R1).
- Invalid reply at request 2: at least 30 further requests. Invalid replies at requests 2, 5 and 9:
  exactly 9 requests sent.

## 6. Registry, packaging and docs

```bash
python3 -B scripts/build-jev-registry.py --check
python3 scripts/validate-package.py
python3 scripts/package-plugin.py
```

Expected: exit 0. `jev/registry.json` carries `signals` only for alternatives of
`scripts/scan-tells.sh` that match their pattern's `SKILL.md` section (research R4), and `--check`
fails if `scan-tells.sh`, `SKILL.md` or the registry is edited alone. `AGENTS.md` and `README.md`
describe `scan-tells.sh` as a source of the shipped registry. The rebuilt archives
hold byte-identical copies of the changed `jev/` files and `references/typesafe-advisor.md`. Do not
commit `dist/`.

Read `references/typesafe-advisor.md` for exit codes 0 and 2, the `evaluation` object, the plan and
the partial-run report (SC-008).
