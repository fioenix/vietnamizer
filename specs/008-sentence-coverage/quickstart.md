# Validation quickstart — feature 008

This is the proposed implementation acceptance guide. New commands/test modules below do not exist
in released v0.10.0 and were not executed during planning. Do not interpret it as test evidence.

## Prerequisites and fixtures

Use Python 3.12+ and a checkout implementing contract v2. The offline suite uses stdlib `unittest`
and a fake transport/clock; no API key or network is required. Put synthetic fixtures with independent
annotations/provenance under `tests/fixtures/segmentation/`. Do not reuse the user's pasted articles
as public fixtures or live payloads without authority.

Fixture families:

1. Exact Vietnamese boundaries from [segmentation contract](contracts/segmentation.md), plus
   independent counterexamples and expected-unresolved cases. Include decomposed accents and CRLF.
2. Same target words/different complete contexts; nonadjacent definitions; missing/unreviewed context;
   same words repeated at different offsets; protected neighboring/linked paragraphs.
3. One parent with >16 sentences, >32 auto-detected paragraphs, a sentence whose recipes span batches,
   and a payload fitting only after reducing target-window membership.
4. Impossible single-question state >48,000 bytes; exact 48-question and 32-request edges; absolute
   deadline/cancellation; malformed/missing/extra answers; context `insufficient`; evidence-role `none_fit` versus interpretation-role `none_fit`; late/stale results.
5. V1 sections/targets/candidates: exact aliases, missing targets, duplicates/overlaps, broad custom
   spans, protected targets and supplied-sections scope. Keep paragraph/document check counts separate.

## Local preparation

After implementation, provide a v2 JSON fixture following [CLI contract](contracts/cli.md), then run:

```bash
python3.12 -B -m jev prepare --input tests/fixtures/segmentation/article.json
```

Expected: zero evaluator calls, exact source partition and parent bindings, every sentence or unresolved
span visible, separate context-review state. `prepared` does not mean Jev evaluated it. Unresolved
boundaries return exit 2 and explicit spans; host overrides resolve them without rewriting text.
Do not use the no-key `evaluate` early return as a segmentation test; it intentionally reads no input.

## Deterministic runtime checks

Proposed commands once the corresponding tests are implemented:

```bash
python3.12 -B -m unittest tests.test_preparation tests.test_coverage -v
python3.12 -B -m unittest discover -s tests -p 'test_*.py' -v
python3.12 -B scripts/build-jev-registry.py --check
python3.12 scripts/validate-package.py
```

The fake transport must record complete redacted parent/context and exact question/check bindings.
Use an independent oracle to compute expected scope/pattern/recipe sets. Assert each required key
is credited at most once and final missing sets equal the set difference, including never-scheduled
late sentences/paragraphs. A repeated sentence or successful paragraph result cannot fill another key.

Measure the documented 1 MiB preparation target on a recorded machine, separately from remote
latency. Include a high-sentence-count stress fixture to detect Cartesian-product memory growth;
report actual time/peak memory and exact unresolved remainder if the local deadline is hit.

## Package and consumer parity

After code verification, run existing repository packaging gates:

```bash
python3.12 scripts/package-plugin.py
npx --yes skills@1.5.20 add . --list
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json --strict
```

Extract all three archives to temporary directories, compare every shipped runtime/module/registry
and canonical skill resource against source, and run network-free preparation plus no-key evaluation
from each extracted root. Include new modules in the validator's runtime inventory. Test old aggregate
consumers against schema v2 and verify source-scope/status migration. Do not install into shared user
profiles as a test fixture or publish a version without separate authority.

## Optional semantic/live evaluation — separate authority

Offline success proves preparation and accounting, not Jev judgment quality. A later authorized
synthetic smoke must record actual model, payload/config/corpus bindings, coverage, service failures,
latency and token usage. Context-pair semantic trials need independent expected judgments and must
report error/uncertainty rather than a universal numeric edit policy. If behavioral editing accuracy
is claimed, report harmful-edit recall, valid-edit false-block rate and review rate on a separate
labeled evaluation. No such accuracy claim or live run is part of this plan.
