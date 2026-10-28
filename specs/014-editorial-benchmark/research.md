# Research Decisions

- Use CLI subscriptions, not APIs. Codex forced_login_method=chatgpt prevents API-key billing.
  Antigravity settings has useG1Credits and modelProvider unset. Official settings documentation
  states AI credits are off by default; no settings changed. Stop on quota errors.
  Source: https://antigravity.google/docs/settings?tab=cli .
- Use fresh task-specific empty directories outside the repo. Freeze all editing instruction
  bodies in prompts; do not rely on installed skill discovery. Codex supports invocation-only
  project_doc_max_bytes=0 and skip_host_skill_discovery; no shared settings are modified.
- Antigravity has no supported no-skills flag in Agybird. Use a narrowly scoped standalone text
  task expressly prohibiting tools/skill loads, with the owner-authorized three-arm experiment
  taking precedence over optional editing workflows. Its metadata cannot prove absence of
  injected global rules. Preserve that limitation; never claim pure model or integration parity.
  Reject observed tool/subagent calls as contaminated; do not silently include them as valid.
- Agybird forwards requested model but does not attest backend model or injected system context.
  Store requested model and actual_model=null when not observed. Generation is a pilot under
  the existing harness, with no cross-runtime base-model superiority claim.
- Agybird creates a local project and session record. Use supported AGYBIRD_STATE_DIR and
  AGYBIRD_PROJECTS_DIR for task-local records; do not alter shared settings or auth.
- Standalone core comparison: provide canonical SKILL, selected profile/card, resolver and two
  language references in the Vietnamizer prompt. No script/key capability is offered and no
  TypeSafe key is forwarded. This measures supplied instruction bundles, not auto-discovery.
- Original synthetic sources remove redistribution uncertainty; they provide diagnostic
  coverage only, not a representative corpus or independently labeled quality benchmark.
- No hooks configured. No package changes, external dependencies or new installation.

## Smoke findings

Codex CLI authenticated with ChatGPT. Invocation-level controls disable project AGENTS bytes,
host skill discovery, apps, remote plugins and shell tool; no shared configuration changed.
Antigravity defaults selectors were checked before every attempt; the native `finish` marker
is schema completion, not external tool use. Startup diagnostics in Codex similarly are not
tool actions. Both behaviors have regression coverage. The first two raw records retain their
initial conservative classification; current reports include explicit deterministic
normalization receipts, using only exit-0 complete outputs with unchanged text. No model
output was regenerated to improve a result. Profiles/cards were selected by the host and
included in the supplied bundle; automatic genre/profile selection is not measured here.
