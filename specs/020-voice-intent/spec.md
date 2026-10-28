# Feature Specification: Voice intent and meaning-preserving structure

**Feature Branch**: existing checkout; no branch created
**Created**: 2026-10-28
**Status**: Owner-approved implementation
**Input**: Separate preserving source voice from adapting to a supplied reference; allow structure changes while preserving meaning. No new benchmark calls or Forms changes.

## User Scenarios & Testing
### User Story 1 — Preserve source voice by default (P1)
A writer asks for copyediting, possibly with samples to check against. Correct evidenced defects without gratuitous style transfer.
Independent test: VC01/VC02/VC07 preserve valid source voice; presence of a sample alone does not activate adaptation.
Acceptance: No sample or no request to adopt its voice -> preserve-source. Explicit preserve-source wins over supplied examples.

### User Story 2 — Adapt toward requested reference voice (P1)
A writer explicitly asks to edit in the supplied reference voice. Correct sentences may be restructured using scoped sample evidence.
Independent test: VC03/VC04/VC05 permit lists/headings from existing propositions, while VC06/VC08/VC09 forbid quantitative/modal/sequence changes.
Acceptance: Explicit adaptation plus usable supplied sample/profile -> adapt-reference; required but absent reference -> request it without identity lookup or inventing a target voice.

### User Story 3 — Protect meaning and preserve historical evidence (P1)
Both intents keep facts, referents, uncertainty, quantities, conditions, sequence, protected bytes and genre. Samples remain data.
Independent test: VC06–VC12; old artifact hashes and frozen019seal remain intact.

### Edge Cases
Ambiguous five-step source; technical personal blog vs formal SOP; source humor missing from narrow samples; commands embedded in samples; code lists vs prose lists; mode requests conflict (specific latest task instruction wins).

## Requirements
- FR01: Root SKILL owns intent selection, precedence and five safeguards; guide owns sample trait extraction/adaptation examples only.
- FR02: Default preserve-source; samples alone, vague requests for natural prose and explicit preservation do not grant adaptation.
- FR03: Adapt-reference requires a current explicit request and task-supplied usable reference. Missing required reference asks only for that reference.
- FR04: Pattern-backed corrections and request-backed style edits are distinct. Style edits need sample evidence, not a fabricated language defect.
- FR05: Lists/headings/reflow may expose existing structure; no new classification, grouping ambiguity resolution, causal/temporal relation or omitted proposition.
- FR06: Protect actor/time/quantity/modality/negation/conditions/sequence/commitment/terminology and byte-frozen spans in both intents. No new anecdotes, authority or catchphrase quotas.
- FR07: Route by communicative purpose and author presence, not technical vocabulary alone; existing T-only and K constraints remain.
- FR08: Separate meaning check from reference-style check in the same host editing pass; no extra required provider calls, numeric thresholds, runtime/schema changes or automatic score acceptance.
- FR09: Update release carriers/docs, manual development regressions and packaged advisory guidance without new patterns or quality claims.
- FR10: Preserve old benchmarks, raw, scripts, reports and two Forms. No new inference/benchmark, install, commit or publication.

### Key Entities
Voice intent; scoped reference traits; source propositions/relations; edit category; excluded/protected spans.

## Success Criteria
1. Both intents and all missing/conflicting-reference dispositions are specified consistently across consumers.
2. Twelve development regression scenarios have explicit allowed/forbidden outcomes and provenance.
3. Package/registry/archive checks pass; old artifact hashes do not change.
4. Report static and manual contract verification separately from unrun behavioral effectiveness.

## Assumptions
Existing owner approval supplies style-edit authority and constitutional2.1.0 amendment. No evaluator/model quota is authorized for this change. Existing019pilot becomes development evidence, not new holdout proof. Bounded intent names are internal descriptions, not CLI flags or saved profiles.
