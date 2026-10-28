# Verification
Read VC01–VC12 in calibration/ca-kiem-thu.md with the task intent, source and sample. Check the current instruction contract permits valid candidates and rejects invariant violations; this is manual contract inspection, not an executed LLM regression.

Run `python3 scripts/build-jev-registry.py --check`, `python3 scripts/validate-package.py`, and selected tests in tests/test_package_security.py for voice-reference packaging/style layout. Generate local archives via scripts/package-plugin.py and scripts/package-skill.sh; inspect contents and source parity. Use already-installed discovery/Claude validators without installing tools. Historical019can be audited offline using its captured code rather than current root version. No benchmark command is authorized.
