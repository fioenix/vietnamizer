# Validation Quickstart

Run offline checks from repository root:

```bash
python3 -B -m unittest tests.test_jev -v
python3 -B scripts/build-jev-registry.py --check
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/validate-package.py
python3 scripts/package-plugin.py
```

The registry check must report 55 synchronized definitions. Tests must establish zero outbound requests without a key or permission, bounded and non-pass errors, candidate-specific guards and extracted archive execution. Package checks must prove byte parity; source-only success is insufficient.

For a permitted live smoke, supply an existing approved credential injection to the CLI and use only the synthetic input in contracts/cli.md. Check model_actual is jev-1.14.0 in validated receipts. Never print the key or treat smoke success as Vietnamese editing accuracy. No global/shared installation is part of this task.

Final actual results and missing environmental checks belong in evidence.md.
