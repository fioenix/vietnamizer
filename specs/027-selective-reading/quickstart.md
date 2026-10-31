# Validation

1. Run python3 -B -m unittest tests.test_selective_reading tests.test_registry_exclusions tests.test_registry_signals -v.
2. Run scripts/build-jev-registry.py --check and scripts/validate-package.py; run relevant distribution/package/runtime tests recorded in verification.md.
3. Read measurements.json and verification.md: counts include specified full files, triggered completion lookup separately, not user text or billing tokens.
4. Inspect labelled Unreleased archives and SHA-256 receipts; verify default dist hashes against saved baseline.
5. Behavioral checks: a missing được; intentional ellipsis; protected quotation; modal/causal limits; supplied-sample content leakage; no-key route. Automated package tests do not prove those semantic outcomes; keep A/B pending unless actually run.
