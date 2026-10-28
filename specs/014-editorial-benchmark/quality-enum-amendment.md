# Quality v1 enum serialization amendment — 2026-10-25

The first source-only inventory completed and passed validation. Its first output-group
response used `damaged` for one meaning flag, where the frozen machine contract accepts
`clear`, `violation`, or `uncertain`. The original rubric described damage and gave clear
examples but did not explicitly enumerate all three flag spellings in the grading prompt.
The entire output-group response is retained as invalid/missing, with no alias conversion
and no rerun of this group/model pair. This is a protocol failure, not a quality outcome.

The separate v2 adapter appends explicit serialized enums to future grading prompts.
Substantive criteria, source inventories, randomized assignment and analysis do not change.
The original driver/protocol/epoch remain immutable. The successor manifest is identical
for the underlying v1 evidence, while a separate immutable amendment binds the v2 driver,
this note, inherited raw files and the designated failed unit `M1-Q001`.

Exactly two original starts count against the same total cap of 42. Reuse the validated
source-only inventory only after verifying its identical source prompt/raw/labels and
manifest binding. Preserve the failed group as four missing output reviews (one pair vote
per comparison). Run the other 19 M1 groups, M2 source inventory and 20 M2 groups: 40 new
starts maximum, with no automatic retries. A new failure stops dependent continuation.
Report protocol amendment, failure counts, all missing slots and unequal coverage.
A changed serialization prompt is a limitation, not a hidden seamless completion.

Human instructions enumerate every allowed label and remain a separate assessment.
