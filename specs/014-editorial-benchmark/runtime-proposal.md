# Runtime and Minimum Budget Proposal

**Date**: 2026-10-25
**Status**: Owner approved the 120-output pilot on 2026-10-25: both proposed models at medium, included quota only, USD 0 incremental. Larger holdout remains proposed.
**Owner direction**: Start with Codex and Antigravity; add Claude after its usage limit clears.

## Runtime choices

| Track | Proposed runtime/model | Reason and verification limit |
|---|---|---|
| Codex | Codex CLI 0.164.0, gpt-6.1-sol, medium effort | Current official documentation identifies this model for Codex; this host exposes it. CLI invocation/model entitlement still needs a smoke run. |
| Antigravity | Antigravity CLI 1.4.7 through Agybird, gemini-3.8-flash-medium | Owner selected Gemini 3.8 Flash on 2026-10-25; medium is retained from the proposal. This exact identifier was returned by authenticated `agy models`. Generation and quota sufficiency remain unverified. |
| Claude | Deferred | Preserve the same frozen protocol and corpus when adding it; record the later run date/model. |

These are two within-runtime experiments, not a controlled comparison of OpenAI versus Google
base models: harnesses, system instructions and available settings differ. Publish each runtime's
three-arm deltas separately. No assumption that matching effort labels yields matching compute.
No per-task overrides or shared configuration changes have been made.

## Proposed two-stage budget

1. Development pilot: 20 source documents, three arms, two runtimes, one generation each =
   120 completed output slots. Use this to validate loading, baseline quality, rubric, timing,
   quota use and variance. These documents never enter independent headline results.
2. Initial holdout: 100 new source documents, three arms, two runtimes, one generation each =
   600 completed output slots. Freeze protocol and source groups first. Target 30 legitimate
   no-edit cases, 50 cases with independently labeled required fixes, and 20 mixed boundary
   cases; these are planning allocations, not validated population weights. Distribute all
   seven style families across the set; publish their actual counts and avoid strong
   per-style conclusions from small strata. Include synthetic/natural-source breakdowns.
3. Total proposed base allocation: 720 output slots, with an attempt cap of 800 including
   failures/retries. Never regenerate a completed output to obtain a more favorable sample.
   Retry only identified operational failures under a predeclared policy; retain all attempts.
4. A repeat on a preregistered 20-document holdout subset would require 120 further outputs.
   It is outside the base cap and must be budgeted separately before evaluation; repeated
   outputs are correlated with their source. Without it, label results single-generation.

A 100-document holdout is a pragmatic initial evidence budget, not a power calculation or
proof of representativeness. For example, observing zero unnecessary edits on 30 clean
independent cases still does not establish a near-zero population error rate. Determine
whether expansion is needed from pilot variability and the predeclared effect of interest,
without tuning on the holdout. Only aggregate claims sufficiently supported by the sample.

## Cash, subscription quota and reviewer effort

- Proposed incremental model cash cap: USD 0 beyond existing included subscription quotas.
  This excludes existing subscription fees and is not a guarantee that the batch fits quota.
  Do not purchase credits, enable overages, use paid-credit fallback or switch to API billing.
- Codex account snapshot: 36% used, approximately 64% remaining in its returned weekly
  window. This is a shared account snapshot, not reserved capacity, CLI authentication proof,
  an inference count or a token-to-dollar conversion. No additional credits were reported.
- Antigravity model availability was verified; remaining quota and existing overage policy
  were not verified. Paid inference must not begin under this proposed USD 0 cap unless a
  supported read-only check establishes that paid-credit fallback cannot be charged. Do not
  alter shared credit settings to achieve this. Pause if the cap cannot be enforced.
- Measure quota before/after the pilot using supported runtime interfaces. Do not project
  exact batch capacity from a single request or assume uniform quota cost. Propose a
  benchmark allocation that leaves at least 20 percentage points of the account quota
  for normal work; this reserve is a planning choice, not a provider limit.
- Review estimate: 600 holdout outputs x two reviewers x 1–2 minutes/output = 20–40 person-hours,
  plus pilot review, source labeling and adjudication. This assumes short 150–300-word
  documents and a prepared rubric; measure actual review time in the pilot. No contractor
  price or reviewer availability has been verified. No external reviewer has been contacted.

## Experiment prerequisites

- Use fresh independent conversations per source/arm/repeat; do not let previous answers,
  ratings, calibration logs, specs or holdout labels enter generation context.
- Establish supported invocation-level instruction/skill isolation before generation. The
  baseline must not auto-load Vietnamizer from global installation or this repository.
  Do not edit shared skills, defaults or authentication to isolate it. Record unavoidable
  harness instructions and stop if they require Vietnamizer in every arm.
- Keep the common editing request, source context, output format, tool access and generation
  settings fixed within each runtime. Pin versions; verify actual loaded skill/profile bytes.
- Primary arms use no Jev calls. Verify supported per-process disabling rather than silently
  hiding Jev use. Core-plus-Jev is a separate, later experiment and budget.
- Agybird model/effort overrides require explicit owner authorization for those exact values.
  The owner selected Gemini 3.8 Flash; medium remains the proposed effort. This document
  does not authorize quota spending or execute the benchmark.
- Resume Spec Kit planning before implementing adapters, fixtures or report aggregation.

## Read-only preflight evidence

- `codex --version` and `codex exec --help`: noninteractive invocation, JSON events,
  schema-constrained final output and ephemeral sessions are exposed in this CLI.
- `agy --version`, `agy --help`, `node --version`: CLI 1.4.7, model inventory command and
  Node v26.12.1 available.
- `agy models` initially could not bind localhost/write its standard logs inside the sandbox.
  A supported escalated retry returned the model list successfully. No settings were changed.
- No benchmark model generation or Agybird delegated task ran for this proposal.

## Primary references

- [OpenAI code generation guide](https://developers.openai.com/api/docs/guides/code-generation)
- [Codex integration surfaces](https://developers.openai.com/blog/codex-as-a-platform)
- [Testing agent skills with evals](https://developers.openai.com/blog/eval-skills)
- [Antigravity quota inspection](https://www.antigravity.google/docs/cli/commands/usage)
- [Antigravity plans and overages](https://antigravity.google/docs/plans)
