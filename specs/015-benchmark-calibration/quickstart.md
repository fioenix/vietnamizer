# Offline verification

Run registry generation/check, package validator and affected tests from plan.md.
Read new calibration cases as a manual contract; do not invoke a provider. Compare
old benchmark file hashes against the preserved receipt. Old benchmark source-pins
will deliberately differ after the patch: use old bundled rules and source-before
snapshot, never rebind historical manifests to the new revision.
