# Implementation Plan: Complete preparation of long Markdown documents

**Branch**: `codex/009-long-document-preparation` | **Date**: 2026-10-22 | **Spec**: [spec.md](spec.md)

**Input**: Spec 009, revised during planning. The owner authorized specification and planning on
2026-10-22. Research R2 replaces the requested length-scaled budget with a raised absolute bound.
The owner accepted R2 and R3 on 2026-10-22 and authorized `speckit-tasks`. Implementation, merge and
release are not authorized.

## Summary

Local preparation stops after about 2,000 tokens because one fixed 4,096-unit budget covers work and,
implicitly, inventory. Boundary rules also mark file names, relative links and `?",` as unsafe. The
plan:

1. Raise each phase's work bound to an absolute 32,768 units and enforce the 4,096 unit-plus-sentence
   inventory cap with its own counter ([research R1, R2, R5](research.md)).
2. Add two narrow boundary exemptions (punctuation followed by `,;:` or more terminal punctuation,
   and dotted ASCII identifiers) plus opaque relative link destinations. Feature 008's missing-space
   rule stays in force ([R3, R4](research.md)).
3. Rename the segmentation profile to `vi-spans-2` and bind the coverage manifest to it ([R6](research.md)).
4. Update host documentation ([R7](research.md)).

A throwaway prototype of exactly this design passed 183 of 184 existing tests unchanged (the one
failure is a fixture that relied on the old bound, R5), the 54 corpus cases, and the 4 RED baseline
tests. It prepared the reported note with no `preparation_limit` or `unsafe_boundary`.

Design artifacts: [research](research.md), [data model](data-model.md),
[segmentation delta](contracts/segmentation-delta.md), [validation guide](quickstart.md).

## Technical Context

**Language/Version**: Python 3.12+ standard library, unchanged.

**Primary Dependencies**: None added. Transport, model `jev-1.14.0`, registry and request limits are
unchanged.

**Storage**: N/A. No persistent state.

**Testing**: `unittest` (`python3 -B -m unittest discover -s tests -t .`), the segmentation corpus,
existing time/memory assertions, and the RED baseline moved into `tests/`.

**Target Platform**: Existing Python-capable Codex, Claude Code and custom-skill hosts.

**Project Type**: Markdown skill with an optional Python advisory CLI and generated archives.

**Performance Goals**: Every existing feature 008 time and memory assertion passes unchanged
(pathological 750 kB inputs under 2 s with tracemalloc; prototype 0.90 s). Ordinary notes up to
10,000 words prepare fully.

**Constraints**: Request limits, the 120 s deadline, input size limit and inventory cap stay as they
are. No change to evaluation scheduling, gating or transmission.

**Scale/Scope**: Two files in `jev/`, one fixture, three test files added or moved, corpus metadata,
one reference document. No pattern, registry, SKILL.md or profile change.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Pre-research gate against constitution 2.0.0: **PASS.**

| Principle / gate | Assessment |
|---|---|
| I. Vietnamese evidence before convention | No editing rule changes. The boundary exemptions are segmentation engineering, checked against the annotated corpus; R3 records why `,;:` cannot start a sentence and states the typo trade-off as accepted inference, not evidence. |
| II. Meaning and voice | Not affected. Preparation decides what is checked, never edits text. |
| III. General rules vs profiles | Not affected. No V/T/B/K pattern moves. |
| IV. Calibration from labelled evidence | No numeric threshold on Vietnamese judgments is introduced. The work bound is an execution bound, chosen from timing measurements (R1–R2), not a language threshold. |
| V. Standalone Markdown skill | Not affected. The skill runs without Python, keys or network; preparation stays local and optional. |
| Data: send only what is needed | More of a long document becomes eligible for evaluation, but within the same request limits, protection rules and host authorization. No new field is transmitted. |
| Gate 1: start from a red test | Satisfied: four RED cases recorded in `baseline/red-output.txt`; two more acceptance forms (`!,` in a label, uppercase dotted destination) become RED tests first. |
| Gate 2: one reviewable deliverable per task | Left to `speckit-tasks`. |
| Gate 5: release checks | Not a release. Validation and packaging checks run because runtime files change (quickstart). |

Post-design re-check: **PASS.** The design adds no dependency, no new service and no policy. The
owner accepted the R2 bound shape and the R3 boundary exemptions on 2026-10-22. The R5 fixture
change is listed in tasks and reviewed with the implementation.

## Project Structure

### Documentation (this feature)

```text
specs/009-long-document-preparation/
├── spec.md
├── plan.md                         # this file
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── segmentation-delta.md       # changes to 008's segmentation contract
├── checklists/
│   └── requirements.md
├── baseline/
│   ├── test_red_baseline.py        # RED evidence, not shipped
│   └── red-output.txt
└── tasks.md                        # speckit-tasks output, not created here
```

### Source Code (repository root)

```text
jev/
├── preparation.py      # work bound, inventory counter, boundary exemptions, identifiers, profile name
└── coverage.py         # manifest binds the profile constant instead of a literal

tests/
├── test_preparation_limits.py   # + long note, many-units metadata, inventory-cap cases
├── test_preparation.py          # + boundary exemption and identifier cases
├── test_review_boundaries.py    # fixture grows from 1,100 to 4,200 sentences (R5)
└── fixtures/segmentation/
    ├── cases.json               # profile field -> vi-spans-2; no case changes
    └── README.md

references/typesafe-advisor.md   # limits paragraph and reason code (R7)
```

**Structure Decision**: Change existing modules in place. Preparation owns segmentation and limits
(AGENTS.md, "Runtime Jev và coverage"); coverage only consumes the profile name. `jev/registry.json`
does not change, so no registry rebuild is needed. Archive parity is checked through the existing
packaging scripts.

## Consumers to check

- `jev/core.py` `prepare`/`evaluate` read `unresolved`, `segmentation_complete` and sentence lists;
  their shape is unchanged. A new reason string appears in `unresolved`.
- Hosts following `references/typesafe-advisor.md` see fewer `preparation_limit` regions and more
  units scheduled. Request limits are unchanged, so evaluation of a long note is still incomplete.
- Sentence identities change for every document, because the profile name is in their hash. Results
  from `vi-spans-1` runs cannot be compared directly.
- `scripts/validate-package.py`, `scripts/package-skill.sh` and `scripts/package-plugin.py` ship
  `jev/` unchanged in layout. The quickstart re-runs them.

## Complexity Tracking

No constitution violations to justify.
