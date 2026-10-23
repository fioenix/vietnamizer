# Contract delta: structural exclusions and the T4 sign gate

Amends the coverage contract in `references/typesafe-advisor.md` and feature 008. Input schemas,
limits, transport, segmentation and candidate review are unchanged.

## T4 gate

| Subject's editable text | T4 |
|---|---|
| matches `,\s+và\s` after NFC composition (so decomposed *và* counts) | asked as today |
| no match, including `,và` and `, và` only inside protected text or code | excluded, `sign_absent` |

## Structure exclusions

| Structure | Excluded patterns before User Story 3 | After User Story 3 |
|---|---|---|
| `heading` | V2, V3, V5, V14 | V2, V3, V5, V11, V14 |
| `label_value` | none | V11 |

Never excluded by structure: T1, T5, T6, K3 (the technical profile's heading pattern), V6, V20 and every
pattern not in the table. Typography-only, protected and inactive-profile gates apply first.

## Label–value recognition

| Line (after an optional list marker) | Recognized |
|---|---|
| `**Nhãn:** giá trị` or `**Nhãn**: giá trị` | yes |
| `- Nhãn: giá trị` in a run of ≥ 2 adjacent list items that all have a label | yes |
| `Nhãn: giá trị` alone, or a single such list item | no (prose) |
| label containing digits, comma, terminal punctuation, link, code or emphasis | no |
| text ending in `:` with no value (`Nhóm đã thử ba cách sau:`) | no |
| label ending in `rằng` or `là` (`Cần lưu ý rằng:`), bold or plain | no (review finding T022-2) |
| adjacent items with different marker kinds (`-` then `1.`) | not one field list (T022-3) |
| bold label with digits, comma, punctuation or a link | no (T022 note) |

Only the first sentence of a recognized item is `label_value`.

## Report

| Field | Change |
|---|---|
| `coverage[].excluded_subjects` | new: `{subject, reason, structure?}` |
| `coverage[].status`/`reason` | `excluded` with `sign_absent` or `structure_excluded` when every subject is excluded |
| `counts.required`, `uncompleted` | exclude excluded subjects |
| `sentences[].required` | per-sentence sum over including groups |
| `missing[].subject_positions`, `validated_keys` | indexes among the unit's subjects; `subject_range` only when a group covers every subject (T022-1) |

A subject that shows one of the pattern's own canonical signs is not excluded by structure. The full
sign list is generated from **Dấu hiệu** as registry `applicability_signs` (matched case-insensitively);
the priority `signals` are only a subset and are not used for this (PR #21 review). `--scope selected` evaluates the host's explicit targets without structure exclusions.

No new field carries source text.
