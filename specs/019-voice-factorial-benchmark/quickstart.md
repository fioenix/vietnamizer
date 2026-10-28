# Validation and execution guide

Prerequisites: source-readiness.json/corpus.json reviewed; frozen0.12.1; public data only; Codex subscription auth and Gemini subscription quota; no credentials read or installed. Owner approved32outputs/56requests and dedicated no-tool benchmark agent. No shared settings changed.

Offline: targeted Python and Node tests; prepare freezes corpus/source/rubric/aliases/helper hashes and global56ID inventory without inference. Independent preflight checks input parity, leakage, guard, ledger and runtime scope.

Execution command will use the new voice_pilot CLI only, on its new artifact directory. It first calibrates both judges, then prepares4neutral drafts,32edits and16judge blocks. Provider failures stop the run with raw preserved and no retry. Do not run old benchmark prepare/run commands or modify old input cohorts.

Offline report validates raw/config/source/assessment hashes and produces tables/charts without provider calls. Finally verify historical preservation and archive. Completion requires actual32editing records plus all judge/missing states within cap, not prepared prompts alone.
