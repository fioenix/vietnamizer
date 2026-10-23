# Data model: Structural exclusions and the T4 sign gate

All entities are local and rebuilt per invocation, except the generated registry fields.

## Registry pattern entry (generated, extended)

| Field | Type | Rule |
|---|---|---|
| `excluded_structures` | list of `heading`, `label_value` | from the generator table (research R1); each pair carries a canonical phrase that `--check` finds in the pattern's **Không flag** |
| `gate` | regex string | T4 only: `,\s+và\s`, checked against T4's **Dấu hiệu**; matched on the NFC form of the subject's editable text |

Absent fields mean no exclusion and no gate. The registry digest changes, so manifests change.

## Structure kind (per subject)

| Kind | Source |
|---|---|
| `heading` | unit `kind == "heading"` from Markdown layout or a host `kind` annotation; the subject is the whole unit |
| `label_value` | first sentence of a list item or line recognized by research R3: bold label, or plain label in a run of at least two adjacent label items |
| none | everything else |

## Pattern group (existing, extended)

Each target-scope group owns its subject list after filtering. Filtering order: existing gates
(protected, typography-only, inactive profile) → structure exclusion → T4 gate.

## Coverage entry (existing, extended)

| Field | Meaning |
|---|---|
| `excluded_subjects` | `[{subject, reason, structure?}]`; `reason` is `structure_excluded` or `sign_absent`; `structure` only for the former |
| `status`, `reason` | `excluded` with the shared reason when every subject of the group is excluded; otherwise unchanged |

Excluded subjects do not count in `scheduled`, `required` or `uncompleted`. Candidate review
entries never carry exclusions.

## Sentence record (existing, changed)

`required` becomes the sum of recipes over the groups that include the sentence, instead of one
per-section total; `excluded` stays true only when no group includes it.

## Calibration entry (documentation)

`calibration/LOG.md` section with date, genre, source note (private, replaced by synthetic text),
before text, comparison text (the line kept unchanged), observed scores, named difference, pattern
V11, classification, decision, and, for table cells, captions, tables of contents and checklist
items, a native-speaker rule (`AGENTS.md` evidence source 4) with one synthetic example each,
confirmed by the owner before the rule edit.
