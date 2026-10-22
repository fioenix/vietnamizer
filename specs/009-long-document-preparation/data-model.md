# Data model — feature 009

No public data shape changes. This feature changes how two existing internal limits are counted
and adds one reason code. Field names below refer to the preparation result described in
`specs/008-sentence-coverage/data-model.md`.

## Work bound (internal, per phase)

| Attribute | Before | After |
|---|---|---|
| Metadata phase limit | 4,096 work units | 32,768 work units |
| Scan phase limit | 4,096 work units, shared by all units | 32,768 work units, shared by all units |
| Counts | lines, units, annotations, context members, tokens, numeric runs, punctuation events, emitted spans | unchanged |
| Exhaustion | remainder reported as `preparation_limit` | unchanged |

Validation: exhaustion during metadata still returns the whole source as one unprocessed span with
zero units (no partially classified source is ever evaluated).

## Inventory cap (internal, per invocation)

| Attribute | Value |
|---|---|
| Limit | 4,096 units plus emitted sentence spans (`MAX_INVENTORY`) |
| Counted when | a unit is inventoried; a sentence span (exact or unresolved) is emitted |
| Exhaustion | remainder of the current unit and every later unit reported as `preparation_limit` |
| Before this feature | enforced for units explicitly; for sentences only as a side effect of the scan budget |

## Unresolved region reasons

| Reason | Meaning | Change |
|---|---|---|
| `unsafe_boundary` | a boundary would split a grapheme cluster, CRLF pair, combining or emoji sequence | narrowed: no longer used for a missing separator |
| `ambiguous_separator` | terminal punctuation directly followed by a letter outside a recognized token | **new** |
| `preparation_limit` | work bound or inventory cap reached | unchanged meaning, reached far later |
| others (`ambiguous_period`, `ambiguous_ellipsis`, `ambiguous_abbreviation`, `ambiguous_parenthesis`, `ambiguous_url_closer`, `unmatched_delimiter`, `protected_boundary`, `preparation_deadline`, `unsupported_structure`) | as in feature 008 | unchanged |

## Segmentation profile

| Attribute | Before | After |
|---|---|---|
| Identifier | `vi-spans-1` | `vi-spans-2` |
| Bound into | sentence IDs, coverage manifest binding, corpus metadata | same; manifest reads the constant |
| Rule changes | — | [segmentation delta](contracts/segmentation-delta.md) |
