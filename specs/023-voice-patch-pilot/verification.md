# Verification023 — completed pilot

Date:2026-10-28. Delivered:32outputs,52/52nativeCLIstarts,16/16validmainjudgments,80ratingrows and64pairpreferences. No failed/retried/resampled calls.52unique sessions, no observed operational toolcalls. No model/Jev calls beyond the approved experiment; no credits/settings/product changes or Forms interactions.

## Binding / source

A/Cidentical prompt+sample bytes; B0.13.0andD0.13.1differ only supplied library; same corpus/task/order/rubric/model/effort as021. Both15libraryfiles available inline. Old package verified through021seal, new through022archivehash. Runtimeobserved Codex0.164.0/requestedgpt-6.1-solmedium and Agy1.4.8/Gemini3.8Flashmedium. Native model backend not independently attested; CLI start count is not hidden HTTP/billing count.

## Commands and outcomes

- New offline tests written first: initial import failures captured before new derivative existed. Two later preflight regressions also failed before fix. Final `PYTHONPATH=tests python3 -m unittest test_voice_patch_versions test_voice_patch_analysis`:10passed, also independently rerun by reviewer. No full suite.
- `node --test tests/test_voice_guard.mjs`:1passed,0failed; actual toolactivity rejection/capture guards exercised offline.
- `python3 -m benchmarks.voice_patch_versions prepare --output artifacts/023-voice-patch-pilot-20261028-v1`: PASS. One superseded no-inference preparation retained intact at preflight/preparation-v1-no-inference. No paid/model starts in it.
- `python3 -u -m benchmarks.voice_patch_versions run --output artifacts/023-voice-patch-pilot-20261028-v1`:52completed,missing[]. Existing subscription used; no key discovery or shared settings edits. Quota checked before start.
- Bundled Python3.12.14/ReportLab4.4.9: `-m benchmarks.voice_patch_analysis --output artifacts/023-voice-patch-pilot-20261028-v1 --figures`:52starts/32outputs/16judgments/80ratings/64contrasts. No package installation. All3SVG/PDFcharts rendered toPNGwithpdftoppm and visually inspected.
- `v.verify()` / `v.audit_history()`: current code/input/raw/schema/session/seals/mapping all pass. Codex and Gemini native/wrapper bindings inspected by helper; operational toolcall activity not observed. Guard is not an OSsandbox.
- `reproduce.py --destination /private/tmp/vietnamizer-023-offline-reproduction --figures`:0provider calls; analysis.json/ratings.csv/contrasts.csv/summary.csvbyte-for-byte equal; SVGmatches recorded; PDFs regenerated. Reproduction ran on a copy, not source evidence.
- Final `verify_archive()` passed; gzip tar inventory exactly equals763sealedfiles plus final-seal.json; every archived file hash checked against seal.
- Historical hash check: **25819pre-existing files,0changes**, covering artifact/benchmark/spec history. Two Forms not read or mutated; this is no-interaction assurance rather than cloud readback.
- `git diff --check`: PASS. Existing dirty owner work preserved; no commits,push,release or global installation.

## Review

Independent preflight found missing runtimecodecapture and unhandled nested-schema AttributeError. Both fixed and red/green tested before any inference. Capture now includes all8runtimecodefiles; schema-only rejection can remain missing without accepting transport errors. Code frozen before first start, unchanged during run.

Independent final reviewer verified52raw/session/inputbindings,32outputs,80ratings,64comparisons; numerical summaries/tables/examples/report claims all matched, no unresolved findings. Agreement D−B4/8,D−C3/8. Raw labels unchanged; host N4modality concern and weak Gemini meaning reasons disclosed. No extra scoring/provider calls by reviewer.

## Archive

Path:`/Users/fioenix/Projects/vietnamizer/artifacts/023-voice-patch-pilot-20261028-v1.tar.gz`
SHA-256:`2d88a89eb362429c1f3285c9fb927b5b4a1c0dd1e965a25278771c4b23131a44`
Bytes:2627102
Payload files:763plus seal.

Sidecar receipt:`artifacts/023-voice-patch-pilot-20261028-v1.receipt.json`. Archive contains prompts/schema/native/wrapperstreams,52attempts,rawjudgments/blinding,source/provenance and historical neutral-generation raw,capturedcode/packages,rubric,resourceledger,report,charts and offline reproduction. Localignored output, not publication.

## Scientific limits / disposition

V1Ddoes not add historical pluralgloss, but fresh Bdoes not either; no deterministic cure claim. D:C4/2/2(Codex),5/0/3(Gemini) is favorable exploratory evidence, not superiority proof. N2both preferoldrelease. Oneauthor,eightdevelopmentdrafts,1generation/cell,modeljudges not humangold; context-loadingbenefit untested because all15docs inline. Source0.13.1rules were not modified after results.

Spec Kit specify/plan/tasks/implement used. Checklist4/4 before implementation; no extension hooks configured. Existing owner-selected protocol reused, no unresolved routing or new Jev budget. Source canonical workflow read via approved Obsidian CLI, expired review-by noted. New runner inventory added to AGENTS; READMEgeneric benchmark/source descriptions checked, current scientific findings delivered in results.md.
