# Offline validation

1. Read MS01–MS16 in calibration/ca-kiem-thu.md. Walk allowed/rejected examples against root and profile. Record as manual contract review; do not generate new outputs.
2. Run python3 scripts/build-jev-registry.py and --check; python3 scripts/validate-package.py.
3. Run existing targeted PackageSecurityTest cases for registry drift, style registry/card and both package layouts; test_jev canonical exclusion test. No full suite.
4. Build scripts/package-skill.sh and scripts/package-plugin.py; compare every packaged instruction/registry byte against source. Validate Claude metadata with both prescribed CLI forms. Skills discovery via npm offline only; missing cache is a limitation, not permission to install/network.
5. Rehash artifacts/022-meaning-first-20261028/history-before.json; expect all historical paths unchanged. No Forms interactions.
6. Independent source review followed by final package proof after any fixes. Record all commands/results and pending behavioral verification in verification.md.
