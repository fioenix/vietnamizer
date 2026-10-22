# Implementation Plan: Prioritized evaluation within a request budget

**Branch**: `codex/010-long-document-evaluation` | **Date**: 2026-10-22 | **Spec**: [spec.md](spec.md)

**Input**: Spec 010 with all clarifications answered by the owner on 2026-10-22 (budget X, priority
order 1→4, previous report only to avoid repeats, stop after 3 invalid replies). The owner authorized
`speckit-plan`, accepted the R5 deviation and authorized `speckit-tasks` on 2026-10-22.
Implementation, merge and release are not authorized.

## Summary

One invocation reaches 9 units of a long note in document order and stops at the first invalid
reply. The plan:

1. Build the whole request plan before sending, with one function used by both `prepare` and
   `evaluate`, so the plan a host reads is the run it gets ([research R1](research.md)).
2. Take the budget, focus spans and previous block from a new optional `evaluation` object in the
   input document ([R2](research.md)).
3. Order work by tier (candidate, focus, signal, spread), opening each request for the unit with the
   highest-tier unplanned check and filling it with that unit's next checks ([R3](research.md)).
4. Generate tier 3 signals into the registry from `scripts/scan-tells.sh`, keeping only the
   alternatives that match their pattern's own `SKILL.md` section. At `5420c8c` that gives signals
   for T2, T4, T5, V9, V11, V12 and V15; V16 and V18 have none, because their expressions do not
   match their canonical sections ([R4](research.md)). `AGENTS.md` and `README.md` are updated to say
   that `scan-tells.sh` now feeds the shipped registry (task T024).
5. Skip checks answered in an accepted previous block, matched by per-check reuse keys
   ([R5](research.md)).
6. Drop an invalid batch and continue, stopping at the third invalid reply ([R6](research.md)).
7. Report `priority`, `answered_checks`, `missing_by_reason` and `budget_exhausted`; document exit
   codes and the long-note procedure ([R7, R8](research.md)).

Unlike feature 009, this design was not prototyped end to end. The pieces with performance risk
were measured: signal matching (1.8 ms on 847 units; 0.01 s on 1 MiB adversarial text), reuse-key
hashing (0.15 s for 89,299 keys) and key-block size (30,720 bytes per full run). The claim that
reordering inside a unit leaves existing small-input request counts unchanged (R3) is unverified
until the suite runs on the implementation.

Design artifacts: [research](research.md), [data model](data-model.md),
[contract delta](contracts/evaluation-contract.md), [validation guide](quickstart.md).

## Technical Context

**Language/Version**: Python 3.12+ standard library, unchanged.

**Primary Dependencies**: None added. Model `jev-1.14.0`, transport and endpoint are unchanged.
`jev/registry.json` gains a generated `signals` field, so its digest changes.

**Storage**: N/A. The runner stays stateless; the host chooses whether to keep a report and pass its
`answered_checks` block back.

**Testing**: `unittest` (`python3 -B -m unittest discover -s tests -t .`) with synthetic notes and
fake transports; `scripts/build-jev-registry.py --check`; package validation and archive parity.

**Target Platform**: Existing Python-capable Codex, Claude Code and custom-skill hosts.

**Project Type**: Markdown skill with an optional Python advisory CLI and generated archives.

**Performance Goals**: Planning adds well under 1 s to the ~12,100-word synthetic note (measured
pieces, R4–R5); the 120 s deadline still covers preparation, planning and requests. Existing time
and memory assertions pass unchanged.

**Constraints**: Request, invocation, input and response limits unchanged (FR-016). No extra source
or context text in any request (FR-017). No retry, no automatic second run.

**Scale/Scope**: `jev/core.py` (planner, builder extraction, reply handling), `jev/coverage.py`
(tiers, reuse keys, report fields), `scripts/build-jev-registry.py` and `jev/registry.json`
(signals filtered against `SKILL.md`), `references/typesafe-advisor.md`, the `scan-tells.sh` and
`build-jev-registry.py` rows in `AGENTS.md` and the matching tree lines in `README.md`, new and two
changed tests. No pattern, `SKILL.md`, profile or `scripts/scan-tells.sh` change; `SKILL.md` and
`scan-tells.sh` become generator inputs that `--check` watches, and dropping the ungrounded
alternatives (no V16 or V18 signal) needs no edit to either.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Pre-research gate against constitution 2.0.0: **PASS.**

| Principle / gate | Assessment |
|---|---|
| I. Vietnamese evidence before convention | No editing rule changes. Signals reuse the maintainer's existing regex list; they reorder work and never decide a judgment or exclude a check. |
| II. Meaning and voice | Not affected. The runner still never edits, accepts or rejects text. |
| III. General rules vs profiles | Not affected. Profile and genre gates run before tiers; no pattern moves. |
| IV. Calibration from labelled evidence | No numerical threshold on Vietnamese judgments. The priority order is an owner decision and is reported as such, not as a measured optimum; the stop after 3 invalid replies is a spend guard. |
| V. Standalone Markdown skill | Not affected. Without a key the core runs as before; `prepare` stays local. |
| Data: send only what is needed | Requests carry the same unit state as today. Focus spans and reuse keys stay local or in the report; no answer text is fed back in. |
| Data: no prose in telemetry or reports | Plan, priority summary and answered-checks block hold IDs, offsets, counts and digests only. |
| Gate 1: start from a red test | Planned: quickstart section 1 lists the RED cases, recorded before code. |
| Gate 2: one reviewable deliverable per task | Left to `speckit-tasks`. |
| Gate 3: behavioral eval metrics | Not applicable: no guard or judgment changes, and no live run. Recorded so the omission is explicit. |
| Gate 5: release checks | Not a release. Registry check, validation and packaging run because runtime files change. |

Post-design re-check: **PASS.** Research R5 accepts a previous block for a changed document and
re-plans only the changed units; the owner accepted this deviation on 2026-10-22 and the spec was
reworded (FR-011, User Story 3, SC-005, edge case). No dependency, service or edit policy is added. Two tested contracts
change on purpose: stopping at the first invalid reply (owner decision Q2, R6) and the
`limit_exceeded` reason (R7). Both are listed for tasks and review. The previous block cannot be
authenticated (R5); this only lets a host skip its own checks and never inflates a report.

## Project Structure

### Documentation (this feature)

```text
specs/010-long-document-evaluation/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── evaluation-contract.md
├── checklists/
│   └── requirements.md
└── tasks.md             # speckit-tasks, not created here
```

### Source Code (repository root)

```text
jev/
├── core.py              # request plan, payload builder, reply handling, evaluation input
├── coverage.py          # tiers, reuse keys, priority summary, answered-checks block, missing reasons
└── registry.json        # generated; gains signals
scripts/
└── build-jev-registry.py  # reads signals from scan-tells.sh; --check covers them
references/
└── typesafe-advisor.md  # exit codes, evaluation object, plan, partial-run report
tests/
├── test_evaluation_priority.py   # new: tiers, ordering, spread, plan equality
├── test_evaluation_previous.py   # new: reuse keys, chained runs, rejection
├── test_coverage_faults.py       # changed: continue after invalid replies
└── test_jev.py                   # changed: budget_exhausted
```

**Structure Decision**: Keep the existing single-package layout. The planner sits in `jev/core.py`
next to the scheduler it replaces; tier and key bookkeeping sit in `jev/coverage.py` with the ledger
they extend. New tests follow the existing one-concern-per-file pattern.

## Complexity Tracking

No constitution violation to justify.
