# Offline verification

Run existing tests.test_jev and the selected package/source-gate test methods recorded
in results.md. Run source validator, registry generation and --check, then the plugin
packager. Inspect actual ZIPs for updated SKILL/registry/calibration bytes and exactly
one skill, and compare protected historical hashes. Review MR01–MR12 against canonical
rules with static evidence only. No command here should invoke benchmark generation,
Jev API, install, native client reconfiguration or Forms. Run logs bind final bytes.
