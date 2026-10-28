# Plan: paired MR version comparison

## Routing and design
Spec Kit018; tasks/implement because runtime/quota, source-isolation and evidence
contracts need ordering. Canonical workflow read successfully via explicit Obsidian
CLI escalation (review-by2026-10-21 expired). Orrery tools unavailable. No KB writes.
Reuse read-only helpers from benchmarks/mindfio_pilot.py for strict native stream
parsing and binary subprocess capture, and editorial_pilot.py for fixed Codex argv.
Add benchmarks/mr_compare.py and targeted offline tests only; never edit old runners.

## Sources and pairing
0.12.0 SKILL comes from calibration/source-before; verify SHA against its receipt
and the Mindfio run's frozen source.0.12.1 comes from source-after/root and its receipt.
Common resolver/references/profile/card are byte-verified against prior frozen0.12.0
copies and current source. No calibration LOG/case solutions or owner voice profile
are loaded into model prompts. Include only the applicable compatible profile/card;
limited-typography scenarios do not get prose profiles. Both versions see identical
source,context and request. Construct concrete MR inputs from the frozen article
excerpts or synthetic counterexamples, pin exact source spans and document deviations
from the earlier full-article protocol. It is a focused regression probe, not a rerun
of the original Mindfio articles or historical quality grades.

## Rubric and collection
14scenarios×2versions;28total starts, one per cell, fixed shuffled order. Single writer
lock, fail closed on any incomplete/failed attempt and no retries. Restore nothing from
old model outputs. Requested gpt-6.1-sol/medium and ChatGPT subscription; remove API-key
route variables, no Jev. Fresh read-only ephemeral temporary workspace for each cell.
Expected dispositions remain in rubric.json outside prompts; do not score stylistic
alternatives by raw byte equality. Mechanical checks are evidence signals; host reviews
all scenario pairs for semantic acceptance, with uncertainty and optional opportunities
separate. A second static reviewer audits evidence/score reasoning, not new generations.

## Verification and limits
Tests cover expected-field omission, same-case payload parity, snapshots/fingerprints,
exact28cell inventory, raw tool/schema rejection, no-retry reservation and mixed optional
case aggregation. Capture RED before module implementation. Native helper tests already
exist; run them as traced consumers with new tests. Review preflight before inference.
After completion verify distinct native IDs/raw/input/schema/config/usage and hashes;
report per-scenario/per-case transitions with examples and descriptive resources, not
p-values or efficacy rates generalizing beyond this development suite. Pin preservation
baseline over all existing artifact/benchmark/history files; no olddata or Forms mutations.
