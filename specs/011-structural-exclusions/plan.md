# Implementation Plan: Structural exclusions and the T4 sign gate

**Branch**: `codex/011-structural-exclusions` | **Date**: 2026-10-22 | **Spec**: [spec.md](spec.md)

**Input**: Spec 011 with Q1 answered (option B). The owner authorized rule maintenance for V11 and
`speckit-plan` on 2026-10-22. The owner accepted the research R3 deviation and authorized `speckit-tasks` on 2026-10-22.
Implementation, merge and release are not authorized.

## Summary

Sentence-level questions reach headings and label lines whose answer the rules already fix, and T4
is asked about text that cannot show its sign. The plan:

1. Gate T4 on its canonical sign `,\s+và\s` in the subject's editable text ([research R4](research.md)).
2. Exclude, per subject, only the (pattern, structure) pairs whose canonical **Không flag** excludes
   the structure as a whole: headings for V2, V3, V5, V14 now and V11 after the rule change;
   label–value lines for V11 only. T5, T6, K3, V6 and V20 keep running ([R1](research.md)).
3. Generate the exclusions and the gate into the registry from a table of quoted canonical phrases;
   `--check` fails when the rule text and the table disagree ([R2](research.md)).
4. Recognize label–value lines from explicit structure only (bold label, or plain labels in a field
   list of at least two items), with no tuned threshold ([R3](research.md)).
5. Give each pattern group its own subject list and record excluded subjects with reasons
   ([R4](research.md)).
6. Rule maintenance: calibration entry, then V11's **Không flag**, manual cases and registry
   regeneration ([R5](research.md)).

Estimated effect on the ~1,000-word synthetic note: about 380 of 7,381 checks removed (5.1%),
computed from recipe counts, not measured. The value is fewer known-false questions, not cost.

**Spec deviation (R3)**: a lone plain `Nhãn: giá trị` line is treated as prose. A syllable-cap rule
reached full recall on synthetic sets but recognized prose such as `Kết luận: tao sai.` and
`Vậy thì sao: …`, and its holdout was not independent. User Story 2 scenario 2 and SC-001 would use
the recognized forms (bold label, or a field list starting with `- Ngày: …`). A lone plain line keeps
its V11 question, and the model reads V11's new rule text.

Design artifacts: [research](research.md), [data model](data-model.md),
[contract delta](contracts/exclusion-contract.md), [validation guide](quickstart.md).

## Technical Context

**Language/Version**: Python 3.12+ standard library, unchanged.

**Primary Dependencies**: None added. Model `jev-1.14.0` and transport unchanged. `jev/registry.json`
gains `excluded_structures` and `gate`, and V11's `no_flag` text changes, so the registry digest
and manifests change.

**Storage**: N/A.

**Testing**: `unittest` with synthetic fixtures and fake transports; registry `--check`, including a
negative check on a temporary copy of `SKILL.md`; package validation.

**Target Platform**: Existing Python-capable Codex, Claude Code and custom-skill hosts.

**Project Type**: Markdown skill with an optional Python advisory CLI and generated archives.

**Performance Goals**: Label recognition and the gate are one linear pass per unit; existing time and
memory assertions pass unchanged.

**Constraints**: No new rule beyond V11's **Không flag**; no pattern renumbering; `SKILL.md` stays
under 550 lines (486 now); no request carries more text (FR-014).

**Scale/Scope**: `jev/coverage.py` (per-group subjects, exclusions, records), `jev/preparation.py` or
`jev/coverage.py` (label–value recognition; decided in tasks by where unit layout is available),
`scripts/build-jev-registry.py` and `jev/registry.json`, `SKILL.md` (V11 **Không flag** only),
`calibration/LOG.md`, `calibration/ca-kiem-thu.md`, `references/typesafe-advisor.md` (exclusion
reasons), new tests and updated check counts in existing tests.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Pre-research gate against constitution 2.0.0: **PASS.**

| Principle / gate | Assessment |
|---|---|
| I. Vietnamese evidence before convention | The V11 change rests on two observed false positives (titles, label–value lines) and, for four structures, native-speaker rules with one synthetic example each (`AGENTS.md` evidence source 4), confirmed by the owner before the rule edit (analysis finding C1). Exclusions for V2, V3, V5, V14 apply text the rules already state. |
| II. Meaning and voice | Not affected; the runner never edits. Removing known-false questions reduces pressure toward wrong edits. |
| III. General rules vs profiles | V11 stays a general rule; titles and labels exist in every genre, as V14 already states. K3 is untouched. |
| IV. Calibration from labelled evidence | The calibration entry is recorded before the rule edit. No numeric threshold is introduced: R3 rejects the syllable cap because it could not be validated on an independent labeled set. |
| V. Standalone Markdown skill | `SKILL.md` stays usable without the runner; the new V11 text guides the host LLM directly. |
| Package constraints | Numbering unchanged; README pattern table unchanged; registry regenerated with `--check`; line limit kept. |
| Gate 1: start from a red test | Planned per story (quickstart section 1). |
| Gate 3: behavioral eval metrics | Not applicable: no guard or scoring change and no live run; exclusions are deterministic and tested on fixtures. |
| Gate 5: release checks | Not a release. Validation and packaging run because runtime and rule files change. |

Post-design re-check: **PASS.** The owner accepted the R3 deviation on 2026-10-22; User Story 2
scenario 2 and SC-001 were reworded. Removing V11 from a
lone plain label line is not done, by design; the owner may later supply real label lines from
their notes to justify a broader rule.

## Project Structure

### Documentation (this feature)

```text
specs/011-structural-exclusions/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── exclusion-contract.md
├── checklists/
│   └── requirements.md
└── tasks.md             # speckit-tasks, not created here
```

### Source Code (repository root)

```text
jev/
├── coverage.py          # per-group subjects, structure exclusions, T4 gate, excluded_subjects
├── preparation.py       # label–value recognition if done at unit layout time
└── registry.json        # generated: excluded_structures, gate, new V11 no_flag
scripts/
└── build-jev-registry.py  # exclusion table with quoted canonical phrases; --check
SKILL.md                 # V11 Không flag only
calibration/
├── LOG.md               # entry before the rule edit
└── ca-kiem-thu.md       # V11 cases
references/
└── typesafe-advisor.md  # sign_absent, structure_excluded
tests/
├── test_structural_exclusions.py  # new
└── test_label_value.py            # new: SC-003 fixtures
```

**Structure Decision**: Keep the existing layout; exclusions live with the ledger that owns
applicability, and the canonical mapping lives with the registry generator.

## Complexity Tracking

No constitution violation to justify.
