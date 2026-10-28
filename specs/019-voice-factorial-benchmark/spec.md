# Feature Specification: isolate samples and Vietnamizer for voice editing

Created: 2026-10-27. Status: APPROVED FOR PUBLIC-AUTHOR PILOT. Owner explicitly resumes with any suitable public Vietnamese writer,32editing outputs,56totalmodel-request cap, Codex generator and Codex/Gemini blinded judges. Prior Mindfio source-gate stop is historical; frozen audit remains unchanged.
Feature directory: specs/019-voice-factorial-benchmark/; not a claim of Git branch creation.

## User scenarios and acceptance

### US1 — Identify what produces voice preservation (P1)
Compare the same draft under four conditions so samples and skill do not change together without controls.
Given identical source/context/request/runtime, collect A(no samples/no skill), B(samples/no skill), C(no samples/skill), D(samples/skill). B/D must receive identical raw sample bytes. Keep unchanged, failed and unclear outcomes visible.

### US2 — Separate voice, meaning and readability (P1)
Blind condition identities and separately assess reference-voice fit, meaning preservation and readability, with evidence and insufficient-evidence outcomes. Fluent semantic failures cannot become successes by score averaging. Model preference is not author approval.

### US3 — Approve scale before quota (P1)
Propose one writer × eight drafts × four arms =32 editing outputs, and two judge models × eight blocks =16 judge requests. This yields64 output assessments,16 source assessments and64 pairwise preferences. Propose four additional calibration requests (two blocks × two judges): total52model requests, or at most56if four new neutral drafts are separately approved. No retries. Owner approved the cap and Codex editing plus Codex/Gemini judging on2026-10-27; no call may proceed without the source gate.

### US4 — Preserve and reproduce evidence (P2)
Freeze source, prompts, sample split, rubric, config and seeded order before generation; retain full raw at its actual collection layer. Existing skill, benchmark cohorts, calibration and two Forms remain unchanged.

### Edge cases

- A source already matches the target voice: unchanged output remains eligible, not automatically a failure.
- A supplied sample has AI editing or uncertain authorship: evaluate selected reference voice, not unaided identity.
- A judge cannot distinguish voice from shared topic, or judges disagree: retain insufficient/discordant evidence.
- A generation or judgment fails: keep missing/error status and do not silently retry or change provider.
- Texts overlap the earlier development corpus: exclude from new holdout claims; disclose any unavoidable overlap.

## Requirements

- FR01: Within-draft2×2design; raw samples, no generated profile or extra analysis pass for only D.
- FR02: Freeze current0.12.1 full applicable skill bundle on approval; same generator/model/effort; fresh sessions, no tools/memory/Jev.
- FR03: Separate four native-voice and four neutral-AI drafts; preservation and adaptation are distinct claims.
- FR04: Generation samples, judge-only references and drafts are disjoint at article/series level. Previous Mindfio/MR development cases are not new holdouts.
- FR05: Record self-written/AI-edited/reference-selected provenance; selected reference voice is not evidence of unaided authorship.
- FR06: Judges receive the same references for all arms, blind metadata and balanced positions, no previous judge answers or skill rules.
- FR07: Primary contrast D−B; report B−A, C−A, D−C and interaction separately, with source/stratum/judge breakdowns.
- FR08: Report uncertainty, missingness, agreement, meaning failures and collateral edits. No cherry-picked winners or pooling dependent ratings as independent sources.
- FR09: One generation/cell is a feasibility minimum, not repeat stability or demonstrated statistical power. One author cannot establish population benefit.
- FR10: Conditional owner authorization covers the specified pilot only after source readiness. No Forms/invitations/publication or unrelated spend; source-gate failure stops inference.

## Entities

Writer: anonymous ID, provenance declaration, channel scope.
Sample packet: raw texts/hashes, generation or judge-only role.
Draft: source/context/task stratum, provenance, factual anchors and upstream relation.
Cell: writer/draft/arm/revision/config/attempt bindings.
Assessment: blind order, judge config, three dimensions, four pairwise preferences, evidence/error/uncertainty.

## Design success criteria

1. Four treatments and intended contrasts are unambiguous.
2.32outputs/16judge requests have explicit boundaries and unknowns.
3. Rubric separates voice from meaning/readability and has evidence requirements.
4. Leak prevention, retention, error handling and allowed claims precede execution.
5. Owner can accept/revise scope without authorizing an unbounded run.

## Assumptions and open decisions

Selected writer/channel: Van-Duyet Le (Duyệt), Vietnamese technical blog, historical2015–2016 reference voice. Nine attributed articles, excluding explicitly credited reprints; not attested unaided authorship. Same-topic families stay in one role; four native cases are three topic families.
Model-only judging respects the pause on human surveys; a later short owner check is optional.
Codex generator/Codex+Gemini judges and56-request cap are approved. Runtime model/config/quota still require preflight if the source gate is eventually met. Public-author source gate passed independent preflight in v2; runtime metadata verified Codex0.164.0 and Agy1.4.8. Prior1.4.7capability evidence is not treated as current proof. No claim that eight unused drafts or unaided samples already exist.
See protocol.md and research.md. Spec Kit owns artifacts; academic-research-suite supports methodology only. Plan/tasks/implementation subsequently completed the source and execution gates; see plan.md and tasks.md.

## Source gate disposition

RSS/archive returned8previously used articles, identical text hashes; next archive page empty. Bounded linked-public-source discovery found no sufficient new eligible corpus. That stop was superseded explicitly by the owner’s new request to use another public Vietnamese writer. See [source-readiness.md](source-readiness.md). Earlier proposal bytes preserved separately in the source-audit artifact.

## Public-author execution amendment

Use artifacts/019-public-author-pilot-20261027-v2/corpus.json as source authority. Main counts remain32outputs and56requests, including4neutral drafts and4judge calibration calls. Node/package samples share a family; theme native cases share a family, disclosed rather than counted as independent evidence. Short excerpts109–199words are retained without padding;200–400words was an operational target, not a language threshold. No author identity or version labels in judge prompts. Public source may have been in pretraining; new to this project is not unseen by the model.

Use a fresh task-local finish-only judging agent for Gemini rather than the old editing-only agent. This implements the owner’s prior explicit dedicated no-tool benchmark-agent decision with the now-authorized judging responsibility; no shared agent/settings/defaults change. Runtime init identity, actual tool-event guard and retained native raw are acceptance evidence, not the shared advertised registry.

The first main Gemini assessment failed literal-quote validation; continuation records terminal missingness and only dispatches remaining planned IDs, with no retry. See plan.md and the sealed continuation amendment.
