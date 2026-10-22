# Validation guide — feature 009

Run every command from the repository root. No key or network is needed; nothing here contacts
TypeSafe.

## 1. RED before the change

```bash
PYTHONPATH=. python3 -B -m unittest discover -s specs/009-long-document-preparation/baseline -p 'test_red_baseline.py' -t specs/009-long-document-preparation/baseline -v
```

Expected before implementation: 4 tests, 4 failures, matching `baseline/red-output.txt`.
Expected after implementation: 4 passes. The same cases also run from `tests/`.

## 2. Full suite and corpus

```bash
python3 -B -m unittest discover -s tests -t .
```

Expected: all tests pass, including `tests/test_preparation.py` (54 corpus cases),
`tests/test_structure.py` and `tests/test_coverage_scaling.py` time and memory assertions, with no
change to their limits. The only changed pre-existing fixture is listed in [research R5](research.md).

## 3. Segmentation delta cases

Each row of [segmentation-delta.md](contracts/segmentation-delta.md) has a test with its expected
outcome. Check the reason codes: no `unsafe_boundary` for a missing separator, and
`ambiguous_separator` where a missing space stays unresolved.

## 4. Package checks

```bash
python3 scripts/validate-package.py
```

```bash
python3 scripts/package-plugin.py
```

Expected: valid package; archives contain `jev/preparation.py` and `jev/coverage.py` identical to the
source tree. `jev/registry.json` is unchanged, so `scripts/build-jev-registry.py --check` passes
without regeneration.

## 5. Owner-only check on the reported note (SC-005)

The owner rebuilds the schema 2 input for the private note locally and runs `prepare` only. Record
counts and reason codes, never text:

```bash
python3 -B -m jev prepare --input /absolute/workspace/input.json
```

Expected: no `preparation_limit` and no `unsafe_boundary` regions. On the planning prototype this
note gave 270 units, 363 sentences and one `ambiguous_url_closer` region.
