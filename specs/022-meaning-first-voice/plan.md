# Implementation Plan: Meaning-first reference voice

**Branch**: `main` (existing; setup's022label is a feature-resolution label, no branch switch) | **Date**:2026-10-28 | **Spec**:[spec.md](spec.md)

## Summary
Implement accepted P0/P1 as source0.13.1. Root owns bidirectional source support checks and selective loading. Blog profile owns safe example repairs and B6/B15 exceptions; voice guide owns scoped trait extraction. Record evidence before rules; use manual regression specifications and existing offline package tests, no new inference.

## Technical Context
- Language: Markdown instructions; Python standard-library generators/validators unchanged.
- Dependencies/storage: existing tooling and ignored local artifacts; no new packages or services.
- Platform: installed skill consumers, Claude/Codex archives; no global install or release.
- Testing: source/package validators, targeted existing package and canonical-registry tests, offline manual regression walk-through and three-archive byte parity.
- Performance goals: load relevant documents on demand; no unmeasured latency/quality claim.
- Constraints: root≤550lines; blog≤320; K≤220;55patterns remain unchanged; historical files/Forms immutable.
- Scope: root, voice guide, resolver, blog rules/card, calibration, README, metadata and generated registry. No benchmark runner or production Jev logic changes.

## Constitution Check
Pre-design PASS: evidence021 and explicit owner approval; no language pattern added; meaning/style distinction remains; offline-first and data/protected-byte guards unchanged. Known V1 candidate and profile examples provide observed red semantic cases, not a claimed model rerun.
Post-design PASS: proof level remains manual/static; no policy thresholds, fabricated labels or new API calls. Constitution amendment unnecessary: this enforces existing principleII.

## Source / routing / depth receipt
Canonical source: Obsidian CLI, Fioenix Vault,04-PROCEDURAL/Workflows/coding-workflow.md; read succeeded after one supported escalation retry. Review-by2026-10-21 is expired; no source update made. Orrery search found workflow; returned Vietnamizer memories concern older T016 and do not supply current pilot decisions. Current repository/owner instruction is authoritative for this work.
Route: Spec Kit specify→plan→tasks→implement. NORMAL, serial implementation. Direct-depth exception does not apply because root/profile/guide instruction contracts cross ownership boundaries. No unsettled activity-selection ambiguity; no Jev call needed. Citation cookbook live fetch failed; no evaluator integration added or API contract inferred. No approved new evaluator spend; manual judgment is disclosed.
Supporting skills: skill-creator/writing-for-agents for instruction design; verification-before-completion; requesting-code-review for independent patch review only. No new generation/evaluation benchmark via subagents.

## Project Structure
- Root workflow: SKILL.md.
- Profile/card: profiles/blog-ca-nhan/rules.md and styles/chuyen-mon-cong-khai.md.
- References: references/giu-giong-tu-mau.md and bo-giai-phong-cach.md.
- Evidence/regressions: calibration/LOG.md and ca-kiem-thu.md.
- Consumers: README, source metadata, generated jev/registry.json and all three distribution archives.
- This feature: spec, requirements checklist, research, data-model, contracts, quickstart, tasks and verification.

## Execution path / ordering
Evidence snapshot→regression red examples→root safety→safe profile examples→voice traits/exceptions→loading→metadata/registry regeneration→targeted tests/package parity→independent review→final proof. P0 is prerequisite for P1 acceptance. Existing WIP preserved; no commit/push.

## Complexity Tracking
No constitutional exception. New tests would only mirror prose; use existing structural/parity tests and explicitly manual semantic cases. Model behavior remains pending owner-authorized future runs.
