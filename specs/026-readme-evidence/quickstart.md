# Verification quickstart

1. Run targeted documentation-negative and distribution/package-security tests; missing pattern row and wrong detailed version must fail validation.
2. Run python3 scripts/validate-package.py and python3 scripts/package-plugin.py --check.
3. Run renderer --check-data without optional plotting dependencies; regenerate SVGs with the documented pinned isolated environment, then compare bytes.
4. Inspect PNG exports at desktop and narrow width; verify Vietnamese text, direct labels, zero-based count scales and missing/caveat visibility.
5. Audit local links/headings, moved-section mapping and immutable payload/raw/archive hashes. Do not run benchmark/model calls or the full test suite.
