# Pilot Data Model

Case: unique id, source, family, audience, purpose, draft expected issues/invariants, provenance.
All cases are synthetic host-authored development data; none qualifies as holdout.
Attempt: unique cell (runtime, case, arm), monotonically numbered attempt, config/source/prompt
and bundle digests, requested/observed model, session, exit status, duration, usage, output,
raw artifact paths and failure/contamination reason. Never overwrite a finished attempt.
Manifest: frozen cases and bundle digest, common request, baseline, schema/config versions,
120 intended cells, max attempts 132 and policy_version=null. Drift blocks resume.
Report: intended/completed/failed/missing/contaminated counts, latency, usage, monetary cost
unknown, semantic review pending. No quality percentages until independent review.
Blinded packet: case context/source and random public output id, output; separate private key
maps public id to runtime/arm. Host draft labels are supplied separately, not to generation.

Fourth-arm extension (implemented; operational execution recorded in codex-jev-results.md): separate epoch id and immutable parent
manifest/source/draft digests; matched core revision and Jev-assisted revision records;
requested/observed Codex and Jev model versions; Jev request reservations, actual usage/cost,
reply digests, distributions, coverage/missing checks and elapsed time. Preserve unknown
billing after failed calls as reserved, not zero. Count source documents, final arm cells,
Codex attempts and Jev requests separately. No retroactive mutation of the original manifest.

Archival snapshot and chart-ready table definitions: see [data-archive.md](data-archive.md).
Raw epochs remain immutable; analysis tables deduplicate inherited Jev evidence and distinguish
planned cells, attempts, final comparison cells, requests and individual judgments. Missing human
labels remain missing. Archive SHA-256 and raw-reply/source-history gaps are recorded explicitly.


## Quality assessment amendment

Canonical population:20 sources ×4 frozen final outputs =80 outputs. Each judge gets its own
balanced Q-ID/A–D mapping and private coordinator key. Frozen manifest binds all 80 raw/final
records, assignment packet/key digests, rubric, drivers and protocol. Source-only inventory
precedes all outputs; issues carry exact source quotes and independent per-judge IDs.

Model attempt: source-only inventory or one four-output group, exact prompt/schema, raw
stdout/stderr, requested model, observed model unavailable, usage, elapsed time, validation
status and decoded labels. Invalid response is a failed attempt, never a valid partial grade.
The enum amendment retains one failed four-output group as missing and includes both old
starts in the same 42 start cap. Amendments bind driver/note/inherited bytes separately.

Human submission: kind=human, reviewer A/B, frozen packet digest, experience/conflicts and
independence declaration, source-only inventory+lock timestamp/digest/event, full 80 output
labels, ranks/tie/abstention and evidence notes. Lock hash detects accidental changes; it is
not authenticated identity or proof against intentional early inspection. Ingestion verifies
canonical coordinator packet and all label identities; original submission saved by digest.
UI QA fixtures carry qa_only=true and are rejected by human ingestion.

Edit unit: deterministic token-diff block with exact source/output character offsets and
before/after strings. Undefined precision/recall stays null. Uncertain safety remains null;
counts and label distributions retain uncertainty and missing slots. Document-cluster
bootstrap retains both judges and compared arms together; incomplete clusters are excluded
with explicit counts. Model and human labels are never pooled. Forms drafts require raw
exports and reviewer-approved source-inventory transcription; no automatic Forms-to-human
JSON conversion or cloud execution is claimed.

## Human simple v2 — owner amendment 25/10/2026

`human-simple-v2` supersedes human-v1 collection for the current A/B Google Forms only.
Frozen model-v1 packets, submissions and metrics remain unchanged. Canonical assignments
must match the frozen packet before rendering. Each reviewer has 20 groups, four neutral
original/edited comparison images per group, two required four-row grids and one required
notes field. Provider item IDs, exact sequence, input/provider image hashes, contract digests,
raw execution receipts and old form snapshots are retained. No human label exists yet.
`preservation`: preserved/changed/uncertain; `readability`: better/equivalent/worse/uncertain.
Absent answers remain null. Notes retain original text. Do not derive edit-level precision,
recall, separate voice metrics or four-way rankings from this schema. See human-simple-protocol.md.
