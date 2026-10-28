# Preparation Evidence — 2026-10-25

## Disposition

Spec Kit phase: specify; new feature, normal depth. No accepted plan/tasks or benchmark
implementation. Owner confirmed same-model arms: no skill / ordinary prompt / Vietnamizer.
Working checkout was clean at entry; base revision `9394065c90e13428f42e727d57f9140831bb3e1f`. Changes are local and uncommitted.

Canonical routing source was read through approved Obsidian CLI:
`04-PROCEDURAL/Workflows/coding-workflow.md`, version adaptive-2026-10, updated 2026-10-23.
Its review-by date 2026-10-21 is expired; no Vault changes were made.
Spec template resolved using the installed Spec Kit resolver. No extensions.yml was present.
The new spec/checklist/evidence files fit the existing specs/ entries in README and AGENTS;
no runtime tree or package layout changes were made.

## Current evidence

- `python3 -B -m unittest tests.test_jev tests.test_context_protection tests.test_coverage_faults`
  returned exit 0: 41 tests, 2.086 seconds, OK. Only these targeted modules ran.
- Those tests exercise runner contracts with mock responses and local preparation. They do
  not establish real Jev semantic accuracy or end-to-end editorial quality.
- `python3 scripts/validate-package.py` returned exit 0: Vietnamizer 0.11.0, 55 patterns.
- No representative labeled editorial holdout, blinded human review or controlled model
  comparison was produced in this work. There are no measured editorial improvement claims.

## Presentation reference

[Hindsight overview](https://hindsight.vectorize.io/) places comparative benchmark scores
near the top and links to [benchmark details](https://benchmarks.hindsight.vectorize.io/).
This observation supports the presentation pattern of claim → comparison → evidence.
The published Hindsight scores were not independently reproduced or audited here and
are not evidence for Vietnamizer.

## Vietnamese README review

Used canonical Vietnamizer rules, technical profile and huong-dan-ky-thuat style.
Host review retained the new wording: it distinguishes illustrative examples, regression
checks and controlled outcomes; it preserves technical terms and avoids superiority claims.
Jev cookbook consulted: [citation checks](https://docs.typesafe.ai/cookbooks/citation_check).
Its example policy/thresholds were not adopted.

The authorized existing runner reviewed only the two new prose blocks, with formatting/link
syntax removed; table rows and the command block were checked by the host. An initial sandbox
attempt returned service_failed with zero validated answers. A supported escalated retry
returned four validated receipts using requested model `jev-1.14.0`. Actual validation
is enforced by the runner; no different model was accepted.

- Status: `incomplete`; evaluation_complete: `False`.
- Required checks: 367; validated semantic answers: 156;
  mechanical checks: 1; uncompleted: 210.
- Request cap: 4; reported usage: 44486 input and 8902 output tokens.
- Monetary cost was not returned and is unknown.
- Raw distributions and receipts are retained locally under ignored
  `artifacts/014-editorial-benchmark/`, not included in the public source payload.
- Partial answers are advisory, not an independent editorial benchmark or a complete pass.
  Host inspection found no concrete correction justified by the available signals: T5 had
  no repeating heading/bullet pattern in supplied prose, K4 examples sit immediately below,
  and terms flagged under V19 are appropriate for technical readers. No score automatically
  changed or accepted wording.

## Open prerequisites

- Accept/refine the protocol, then run speckit-plan and the depth gate. Corpus, scoring,
  generation and report contracts require tasks/implement rather than a direct shortcut.
- Choose the authorized generation runtime/model and a live spend cap (asked in chat).
- Obtain redistributable sources and independently labeled development/holdout splits.
- Arrange independent Vietnamese reviewers before claiming editorial quality.
- Implement and verify offline aggregation and failure accounting, then run the controlled
  comparison. Do not restore retired guard experiments or spend their historical budget.
- Release checks, installation verification and publication remain outside this preparation.

## Artifact binding

These digests bind the draft and the scope of this evidence; they are not acceptance proof.

- `README.md`: `fa3d0549c33ae3e72357239e11d400c1e27e395068c321b982170179d234fa7f`
- `SKILL.md`: `245552ff5b4e8d45d21df8d0104927bcca0dfa7142cefb1ab5757b97db1490cf`
- `specs/014-editorial-benchmark/spec.md`: `05dba0e84725cae87197385914705c8bde925c538489b24f312b5047839fabce`

## Runtime proposal follow-up

Owner requested model/runtime and minimum-budget recommendations, prioritizing Codex and
Antigravity with Claude deferred. See runtime-proposal.md for read-only preflight evidence,
proposed trial counts and unapproved configuration/spend. The spec assumptions now include
that direction; its digest above has been refreshed. No quality result was produced.

## Pilot execution authorization

Owner approved 120 outputs on 2026-10-25, gpt-6.1-sol medium through Codex and
gemini-3.8-flash-medium through Antigravity/Agybird, included quota only. The plan, task
list and research now own current execution state; this document's specify-phase receipts
above remain historical preparation evidence. First six cells completed with operational
trace validation. See pilot-results.md when available for final count and limits.
