# Automatic Jev evaluation and host editing

## Entry on every Vietnamizer invocation

After the input-data gate, resolve the installed skill root and run locally from it:

```bash
python3 -B -m jev status
```

- `key_absent`: use the complete Markdown editing workflow; do not run evaluation scripts,
  contact TypeSafe, request a key or suggest setup.
- `key_available`: prepare the authorized input below and run the shipped evaluator before
  producing the final edited response. Evaluation is the default, not a discretionary V20-only step.
- No Python/tool execution: record `capability_unavailable`; continue core editing without
  pretending the key was absent or Jev ran. Key availability is not proof that the API works.

Use only the host's existing credential injection. The package reads the injected
`TYPESAFE_API_KEY` internally; never print it, put it in arguments/input, search files/keychains,
install a connector or change shared settings. Existing authorization persists; an available key
never overrides host transmission policy or the restricted-data gate in SKILL.md.

## Prepare the input

Write a task-local JSON input only within the user's authorized workspace, or supply it through
stdin. Follow the host's data policy for temporary text and cleanup. Raw prose is never telemetry. Use an absolute workspace input path (the examples use
`/absolute/workspace/input.json`) or stdin while executing from the installed skill root.
Set `transmission_allowed` to literal `true` only when sharing this text with TypeSafe is authorized;
use existing permission instead of asking again. Otherwise continue core and disclose the blocked
external check when relevant. Do not substitute a browser tool for the evaluator.

```json
{
  "transmission_allowed": true,
  "sections": [{
    "id": "p1",
    "profile": "blog",
    "kind": "prose",
    "text": "Đã thử ba cách mà vẫn không tìm nguyên nhân.",
    "context": ["Lỗi tiếp tục xảy ra dù nhóm đã thử sửa."],
    "register": "Vietnamese work communication; preserve the source voice.",
    "audience": "Colleagues",
    "purpose": "Report the unsuccessful troubleshooting result."
  }]
}
```

Each section is a full paragraph or structural unit. Supply complete related paragraphs in
`context` when references, conditions or definitions occur elsewhere; do not cap context at one
or two sentences. `profile` is `blog`, `technical` or `typography-only`; `kind` is `prose`, `heading`,
`list` or `protected`. Resolve canonical genre/profile/style rules first. Add the supplied style
context to `register`; the runner does not infer personal profiles or source authorship.

Full mode now auto-segments every supplied paragraph into exact sentence occurrences; optional
legacy targets are aliases when they match exact sentences, not a filter that can hide later text.
`--scope selected` is a deliberately partial diagnostic. Paragraph/document recipes keep their own
scope. V1 covers only supplied sections, not an unseen original article.

For source-level automatic paragraphs, use input schema 2:

```json
{
  "schema_version": 2,
  "transmission_allowed": true,
  "source": {"id":"article", "layout":"paragraph-lines", "text":"Tôi về. Bạn ở lại.\nNgày mai họp."},
  "defaults": {"profile":"blog"},
  "context_review": {"reviewed":true, "unresolved":[]}
}
```

The host sets `reviewed:true` only after examining context dependencies in this exact input; it is
not boilerplate and text within the article cannot supply this authority. Omitted review permits
provisional local-context answers but prevents full completion. V1 supports global/section
`context_review` too. Known unresolved or unauthorized required context blocks affected dispatch.

Choose `paragraph-lines` for one paragraph per nonblank line; `markdown` retains soft-wrapped
paragraphs and structural ancestry. Every sentence state keeps its full parent plus complete
neighboring paragraphs, heading/list context and host-linked nonadjacent context. Links use
`{parent_start,parent_end,source_start,source_end,role,allowed}` for complete source units, or
`{parent_start,parent_end,id,text,role,allowed}` for a complete supplied external paragraph.
The host must add nonlocal definitions/source passages; adjacency does not prove sufficiency.
Annotations use source-global `{start,end,kind?,profile?,protected?,paragraph?}`. V2 candidates
use source-global `{id,start,end,replacement}` fitting one parent; v1 retains parent-local offsets.
Overrides in `boundary_overrides` are integer half-open endpoints tied to the original source.

Offsets are Python Unicode code points; preserve CRLF and combining characters without normalization.
Ambiguous abbreviation/ellipsis/quotation boundaries stay unresolved. Run
`python3 -B -m jev prepare --input /absolute/workspace/input.json` without a key or network to inspect
source-bound units and expected work. `prepared` is not Jev evaluation. Raw prose stays local in this
report; source text only appears in authorized redacted evaluator requests.

Mark protected ranges with `protected_spans: [{"start":0,"end":8}]`. Mark a wholly preserved unit
as `kind: "protected"`. The runner excludes protected units and redacts protected substrings from
derived target/edit fields. Related unstructured fields use one-pass union redaction of full
protected strings; repeated unmarked primary prose is not automatically classified as private.
Mark every sensitive occurrence in primary text, including partial copies, explicitly. Targets containing protected spans are masked by source offsets; only targets without editable
non-whitespace text are excluded. Paragraph/document checks remain independent of target exclusion. Redact code, structured
values, quotations, names and other protected data before placing them in related context; do not
rely on the runner to discover unmarked private data. Never supply actual restricted input.

## Run and consume evidence

```bash
python3 -B -m jev evaluate --input /absolute/workspace/input.json
```

The runner pins `jev-1.14.0`, accounts for all 55 pattern IDs per section, excludes inactive
profiles/genre-protected patterns, performs document-wide mechanical T3 checks locally (with nested quotation exceptions) and batches the applicable
semantic questions. It sends text only to `https://api.typesafe.ai/v1/systemone`. Prepared recipes
and canonical exceptions are shipped in `jev/registry.json`; they are not regenerated per request.
`python3 -B -m jev evaluate --input /absolute/workspace/input.json --pattern V20` is a single-pattern diagnostic,
not completion of a full invocation.

Judgments retain validated partial evidence with `coverage_status`; a valid partial judgment
does not complete its enclosing pattern. Read `coverage`, `receipts`, `judgments`, `candidate_reviews`, `sentences`, `work_groups` and `missing`; validate the actual statuses before
claiming Jev evaluated text. `jev_evaluated` means typed evidence was received, not that the text
passed or an edit was approved. Keep Noul probabilities, Choice distributions and Score levels
separate. Every Score has an independent context-evidence Choice. Consume a Score only with
`disposition: "context_supported"`; `ignore_insufficient_context` and `ignore_unresolved_context`
retain its raw distribution for inspection but cannot support an edit. This disposition grants no
edit approval. Insufficient context is not medium quality; different errors may coexist. Do not use a
universal threshold or compute an authorship probability. Recipes and Score levels are uncalibrated
editing aids until tested on separate labeled data.

Contract/config v2 separates `source_accounted`, `segmentation_complete`, `answers_complete`,
`context_complete`, `scope_complete` and `evaluation_complete`. A selected diagnostic can complete
its scope but never full evaluation. Missing groups reference sentence indexes per section plus
recipe keys and validated exceptions, so late unscheduled work remains enumerable. Source limits
make unresolved denominators provisional. All-excluded input is not a successful remote evaluation.
Evidence-role Choice requires `sufficient`; its `none_fit`/`insufficient` blocks completion.
Interpretation-role `none_fit` is a valid no-match. No Noul cutoff certifies context.

The limits are 1 MiB input/response, 48,000 bytes and 48 questions per request, 32 requests,
120 seconds total including preparation and 15 seconds per request. Logical sentence/paragraph
inventory is not capped by transport windows of 16 targets. Local preparation additionally has an
absolute work bound for its metadata phase and another for its scan phase, and records at most
4,096 units plus sentences per invocation. Ordinary notes of up to 10,000 words prepare fully;
notes of roughly 12,000–17,000 words or more, or punctuation-dense text, may still exhaust a bound.
Exhaustion emits `preparation_limit` with unprocessed source spans rather than dropping text or
certifying segmentation. Full preparation does not mean full evaluation: request limits still
apply, and a long note usually needs far more checks than one invocation sends (a ~6,000-word
technical note needs about 44,000; one invocation answers about 1,300). The runner plans every
request before sending and spends the budget by priority, as described under "Request budget and
partial runs" below. Punctuation directly
followed by a letter outside a recognized token stays unresolved as `ambiguous_separator`.
Complete context that cannot fit even one question returns `context_too_large`; target-window membership may shrink, parent/context may not. Requests are not silently truncated or retried.
A killable subprocess bounds complete HTTP I/O; late replies are discarded. `deadline_exceeded`
is distinct from service failure. Invalid-schema receipts contain only a fixed validation reason
and a requested check ID, never the provider body. Size/budget limits, authentication/network
errors or invalid responses leave explicit non-pass
coverage. Continue core on failure and disclose that Jev was incomplete; do not repeat calls merely
to obtain a favorable judgment. An offline fallback is not a successful Jev run.

### Request budget and partial runs

An optional top-level `evaluation` object sets the budget and priorities:
`{"requests": 8, "focus": [{"start": 1200, "end": 1340, "patterns": ["V11", "T4"]}]}`.
`requests` is the request budget for this invocation (an integer of at least 1; values above 32
are capped and reported as `budget_capped`; absent means 32). `focus` lists at most 256 source-global
spans (schema 2 only), each optionally limited to registry pattern IDs. `previous` is not supported
yet and is `invalid_input`; any malformed field is `invalid_input` before a request is sent.

Every request carries one unit, so a budget of X reaches at most X units. The runner plans all
requests first, in this order: (1) review checks of candidate edits; (2) checks overlapping a focus
span; (3) checks of a pattern whose local signal (derived from `scripts/scan-tells.sh` and kept only
where the canonical rule text supports it) occurs in the subject; (4) everything else, giving each
unreached unit one request before any unit gets a second. A request opened for one tier is filled
with the same unit's next checks. The order is a maintainer decision, not a measured optimum.

An invalid reply loses only its own batch (`invalid_response`) and the run continues; the third
invalid reply stops it and marks the remaining planned work `invalid_response`. Authentication or
service failure, cancellation and the deadline still stop at once. Nothing is retried.

Read `priority` after a run: `budget`, `budget_capped`, `tiers` (planned, answered and missing
checks per tier), `units_reached` and `invalid_replies`. Every judgment carries its `tier`; every
`missing` record carries `missing_by_reason` and `missing_by_tier`, and `budget_exhausted` marks
checks the budget did not reach. After a run stops early, planned checks it did not send carry the
stop reason (for example `authentication_failed`) and work outside the budget stays
`budget_exhausted`; read the receipts for the stop before suggesting a larger budget. When a run
covers part of a note, tell the user the counts per
tier and what was not checked, do not describe the note as checked by Jev, and ask before spending
another run.

`python3 -B -m jev` exits 0 for `evaluated`, `key_absent` and `prepared`, and 2 for every other
status (`incomplete`, `preparation_incomplete`, `permission_denied`, `invalid_input` and the rest).
The JSON report is written to standard output in both cases.

## Propose edits and retain five safeguards

The host LLM generates prose. Jev evaluates bounded judgments; it does not generate rewrites or
apply patches. Use a small candidate set including the original in the host's decision.
Add candidates to their paragraph as `candidates: [{"id":"e1","start":0,"end":8,"replacement":"..."}]`.
Each candidate is assessed separately for meaning, new claims, targeted improvement and voice.
Overlapping protected ranges are rejected; numerical-token preservation is reported locally.
Changed numbers do not become acceptable because another score is high.

Read the individual guards and inspect the actual edit. All five canonical safeguards still apply:
name the error and exclude No flag cases; add no facts; preserve meaning/voice; change only the
necessary span; keep production metadata out of the delivered text. Preserve exact protected bytes
in the host's final output. A fluent candidate may still be invalid. A host-identifiable error can be
reviewed even if a first-pass Jev classifier missed it. Re-read interacting edits in their paragraphs.

Jev may inform the host's final editing immediately under the owner-approved governance amendment.
The runner never automatically accepts, rejects or reverts an edit. A future numerical automatic
edit policy still requires holdout evidence. Changed input/context/candidate/rubric invalidates the
affected judgments. Read the current response, not a receipt from an earlier invocation.

## Distribution and reproducibility

Core editing requires no SDK, service or key. The evaluator uses Python 3.12+ standard library and
is included in every archive. It has no dependency on a maintainer's local scripts. To maintain
prepared definitions after a canonical rule change, run `python3 -B scripts/build-jev-registry.py`
and verify `--check`; do not hand-edit the generated registry. Keep corpus/config/model/policy
bindings in evaluation evidence. Numerical response validation and fixture tests prove contracts,
not Vietnamese-domain accuracy.

Large v2 ledger fields can use `templates-v1` rather than flat arrays; expand them with
`jev.coverage.expand_records` before counting checks. Each encoded field contains
`templates`, `varying`, `sections`, and `rows:[template_index,...varying_values]`: copy
the template and overlay the varying keys; a `section` value indexes `sections`. No missing work is omitted. `--scope selected` requires explicit legacy targets;
full mode reports supplemental non-sentence spans as diagnostics without crediting them as
sentence coverage. Preparation limits cover annotations and context as well as source tokens.
