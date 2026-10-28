# Antigravity Isolation Gate

**Status**: BLOCKED before further inference in the current host CLI.
**Observed**: 2026-10-25; P04/bare tried run_command and read_file, then requested git status.
The normalized envelope does not reveal the targets/results of the earlier successful reads.
No private-data disclosure is established from this evidence; its possibility is unresolved.

## Approval review outcome

The host automatic approval reviewer rejected the request to run remaining independent Gemini
trials. Its reason: Antigravity had already used commands/read files outside the text-only trial;
without verified isolation it could expose private repository data to the external service,
which the pilot approval did not authorize. No rejected command was executed. No permission
was granted, settings changed, or alternate invocation used to bypass that rejection.

## Candidate requiring owner approval

Use a dedicated local Docker environment for the official Antigravity CLI. Docker CLI 29.8.2 is
installed; daemon readiness and a supported CLI installation/auth flow inside Linux are NOT yet
verified. No container, image pull, dependency installation or credential transfer was performed.
The installed Python module named antigravity is the standard-library Easter egg, not the SDK;
it was located via module metadata and was never imported.

1. Prepare a container with a pinned official CLI version and Node runtime. Resolve and record
   image/package digests before execution. No host installation or shared plugin changes.
2. Mount only the synthetic corpus, frozen public instruction bundles and response schema
   read-only; give the container a separate empty output directory. Do not mount the host HOME,
   repository, Vault, .git, runtime settings, credential stores or other project directories.
3. Authenticate through the official user-operated flow inside this separate runtime. Do not
   read, export or copy existing host tokens. Pause for any sign-in step requiring the owner.
4. Inspect native settings/rule discovery after authentication. Included subscription route only;
   paid credits off, no API provider, no inherited host rules/skills or connectors. Preserve
   runtime safety and permission enforcement; do not weaken a denial.
5. Verify isolation with fake canaries outside mounted inputs and inspect native trace metadata.
   Failed isolation is a blocker. All model content must be attributable to mounted public inputs.
6. Run all 60 Gemini cells as one new isolated epoch. Keep the existing 10 valid Gemini outputs
   and one quarantined attempt as historical diagnostics; do not mix host-global and isolated
   contexts in a single within-Gemini comparison. Existing 60 Codex outputs remain unchanged.
7. Count all 71 prior attempts plus 60 candidate attempts: 131 total, within the originally proposed
   132-attempt ceiling, leaving one attempt only. This is a count bound, not proof of sufficient
   quota. Recheck quotas and the USD 0 route before any additional inference.

This is a reviewable recovery design, not a verified runnable environment. The approval needed
is to provision/install and authenticate the isolated runtime, then execute only after the above
checks pass. It is not approval to continue the rejected host CLI or grant git status access.

## Official route references

- [CLI installation/auth](https://antigravity.google/docs/cli/install/): official documentation
  lists Linux support and user-operated OAuth for remote sessions. This does not establish
  that authentication/keyring works in a container; verify it before inference.
- [CLI settings](https://antigravity.google/docs/settings?tab=cli): credit/provider selectors.
- [Rules](https://antigravity.google/docs/rules): global rules and continuously active GEMINI.md.

No host credentials may be copied to make container authentication work. If the official flow
requires owner interaction or additional setup, stop at that boundary instead of inventing a
provider interface or switching to paid API billing.


## Follow-up preflight on 2026-10-25

Native `/usage` metadata returned zero inference turns/tokens and approximately 87.65% Gemini
weekly quota and 98.02% five-hour quota remaining. Gemini 3.8 Flash remains the chosen model;
quota is not the observed isolation blocker. A read-only Docker daemon check succeeded through
supported escalation and returned server 29.8.2. No image pull, container, install, login or
inference was performed. Authentication and isolation acceptance remain unverified.


## Owner-authorized provisioning — 2026-10-26

Owner authorized the isolated runtime and selected a new epoch of 80 outputs from the same
20 public sources and four arms as the frozen Codex cohort. Do not resume the rejected host
CLI. Historical 60-output Gemini pilot stays partial. No change to live Forms or Codex outputs.

Provisioning completed: official Linux ARM64 CLI1.4.7 matches publisher manifest SHA512,
Node22.16.0 image pinned to sha256:048ed02c5fd52e86fda6fbd2f6a76cf0d4492fd6c6fee9e2c463ed5108da0e34.
Container `vietnamizer-gemini-20261026` has zero host mounts, no published ports, uid1000,
cap-dropALL and no-new-privileges. Native --version/--help and fake host-canary/socket probes
passed. Raw provisioning evidence is in artifacts/014-gemini-isolated-20261026/provision/.

Official Google OAuth login is awaiting owner interaction in the container. Authentication,
native rule/config/credit/quota checks, capture-driver verification and execution review remain
gates. Filesystem probes alone do not prove containment of every tool or network behavior.
No inference or Jev request has been sent. Never archive credential state.

Network follow-up: default bridge was removed from the runtime. A separate nonroot proxy
bridges an internal Docker network to public Google HTTPS only, without TLS interception.
Saved probes: direct Google ENETUNREACH; proxy Google200; host/private/other403. Endpoint
oauth2.googleapis.com TLS validated; unauthenticated GET /token404. Owner reported DNS failure
from the earlier login invocation; the replacement command injects HTTPS_PROXY/HTTP_PROXY.
Native OAuth completion remains unverified. Five helper tests pass; deployed capture integration,
80-start ledger and native auth/config/model/quota audits remain gates. No inference started.


## Explicit host resubmission — 2026-10-26

Owner explicitly authorized direct host Agybird using only public benchmark data and asked
for approval review again, with80outputsconditionalonapproval. A public-only staging area
was prepared under /private/tmp/vietnamizer-public-gemini-20261026, retaining exact frozen
80prompts and reviewed raw-capture helpers. No private inputs or credential copies included.
The supported approval mechanism rejected the native quota preflight `agy -p /usage` before
execution: reviewer treated it as potentially model-invoking headless input with host-wide
access rather than a proven read-only native operation. No alternative host invocation was
attempted. Thus the80-outputrunhasnotstarted; no additional owner approval is being inferred.
Decision and unchanged4,323-fileCodexcheck: artifacts/014-gemini-host-resubmission-20261026/.
