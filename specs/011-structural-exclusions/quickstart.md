# Validation guide — feature 011

Run from the repository root. No key or network; evaluation tests use fake transports and synthetic
text only.

## 1. RED before each story

- T4 is asked about a sentence without `, và` and about a heading (User Story 1); the gate test
  with decomposed (NFD) *và* must expect T4 to be asked.
- V2, V3, V5 and V14 are asked about a heading (User Story 2).
- V11 is asked about a heading and a recognized label–value item (User Story 3).

Record the failing output in `specs/011-structural-exclusions/evidence.md` with the revision.

## 2. Registry

```bash
python3 -B scripts/build-jev-registry.py --check
```

Expected: exit 0; `excluded_structures` and `gate` match the table in
[the contract](contracts/exclusion-contract.md). On a temporary copy, deleting a quoted phrase from a
pattern's **Không flag** in `SKILL.md` makes `--check` fail.

## 3. Label–value fixtures (SC-003)

At least 20 recognized items (bold labels and field-list items) and at least 20 lines that must not
be recognized (lone plain labels, prose with a colon, lead-ins ending in `:`, labels with digits or
links). Expected: every recognized form recognized, no false recognition.

## 4. Observed cases (SC-001)

Synthetic H1 title and a field list starting `- Ngày: 22/10/2026 (Asia/Ho_Chi_Minh)`: no T4 and, after
User Story 3, no V11 question. A prose sentence starting `Điều quan trọng cần lưu ý là` still gets V11.

## 5. Full suite and package

```bash
python3 -B -m unittest discover -s tests -t .
python3 scripts/validate-package.py
python3 scripts/package-plugin.py
```

Expected: pass. Tests whose required-check counts change are listed with their cause in
`evidence.md` (SC-005). `SKILL.md` stays under 550 lines; pattern numbering and the README table
are unchanged.

## 6. Rule maintenance order (SC-006)

`git log` shows the `calibration/LOG.md` entry committed before the `SKILL.md` V11 edit, and
`evidence.md` records the owner's confirmation of the four native-speaker rules (T023 part a) before
that edit.
