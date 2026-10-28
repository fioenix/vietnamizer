# Pilot Run Guide

Run targeted tests with `python3 -B -m unittest tests.test_editorial_pilot`.
Prepare with `python3 -B benchmarks/editorial_pilot.py prepare --output artifacts/014-editorial-pilot-20261025`.
Run only after preflight/review: `python3 -B benchmarks/editorial_pilot.py run --output artifacts/014-editorial-pilot --limit 6`.
Inspect raw output, tool usage and quota, then repeat bounded runs; completed cells are skipped.
Create report/review packets with `python3 -B benchmarks/editorial_pilot.py report --output artifacts/014-editorial-pilot-20261025`.
Do not interpret 120 generated outputs as 120 good edits; independent semantic review is pending.

Further host Antigravity execution is currently BLOCKED by automatic approval review; these
commands are not authorization to resume it. See isolation-gate.md and pilot-results.md.

## Codex + Jev extension (USD 2 owner-approved)

Use a separate directory; never prepare the extension over the original run.

```bash
python3 -B -m unittest tests.test_jev_pilot tests.test_editorial_pilot
python3 -B benchmarks/jev_pilot.py prepare --output artifacts/014-codex-jev-20261025-v2 --prior artifacts/014-codex-jev-20261025
# After independent review: one-case smoke, then bounded batches of at most four cases.
python3 -B benchmarks/jev_pilot.py run --output artifacts/014-codex-jev-20261025-v2 --limit 1
python3 -B benchmarks/jev_pilot.py report --output artifacts/014-codex-jev-20261025-v2
```

Do not delete a writer lock left by a crash without first checking for a surviving process.
An attempted incomplete/failed cell or evaluation is not automatically retried. A source digest
change blocks resume. Raw request/response artifacts contain authorized synthetic text only;
credentials are passed in memory to the fixed-origin transport and never written to artifacts.
Report billed token-cost estimates separately from actual invoices.

The v1 epoch contains two service-failed evaluations and no Codex starts. V2 inherits every
request/reservation and seal; it never retries those evaluations. Three failed evaluations
trip the global Jev circuit. Codex fallback remains available but is not Jev treatment.
