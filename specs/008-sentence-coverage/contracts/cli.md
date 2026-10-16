# CLI and evaluation contract — proposed version 2

Design only: commands/fields below are not implemented by v0.10.0.

## Entry points

- `python3 -B -m jev status`: unchanged; key availability only, no input read or network.
- `python3 -B -m jev prepare --input input.json`: local validation, segmentation, context assembly
  and expected-work manifest; never reads a credential or calls the evaluator. Emits spans/IDs,
  context links, exact counts or explicit unresolved ranges; no source prose in ordinary output.
- `python3 -B -m jev evaluate --input input.json`: prepares automatically, then bounded evaluation
  when key and transmission authority are present. No intermediate manual `prepare` step required.
- `--pattern V20`: unchanged selected-pattern diagnostic, explicitly partial scope.
- `--scope selected`: explicit selected-target diagnostic for supplied target spans. Full is default.

No-key `evaluate` retains the early return before input read; it does not produce a false prepared
manifest. Users needing offline preparation choose `prepare`. Permission denial never sends source.

## Raw-source input

Illustrative input, with all offsets interpreted as half-open Unicode-code-point positions:

```json
{
  "schema_version": 2,
  "transmission_allowed": true,
  "source": {"id":"article","layout":"paragraph-lines","text":"Tôi về. Bạn ở lại.\nNgày mai họp."},
  "defaults": {"profile":"blog","register":"Vietnamese personal writing; preserve voice."},
  "annotations": [],
  "context_links": [],
  "context_review": {"reviewed":false,"unresolved":[]}
}
```

`source.layout` is required (`paragraph-lines` or `markdown`); raw text resides in `source.text`.
`defaults.profile` is host-resolved (`blog`, `technical`, `typography-only`). Other existing metadata
remain optional with noninventive defaults. Annotations give valid source spans with kind/profile,
protection or paragraph-boundary overrides. Code/explicit protection takes precedence over an
editable default. Invalid conflicting annotations are rejected before dispatch.

`context_links` associate a parent source span with complete source paragraph spans or explicitly
supplied external paragraphs. Target and linked IDs/spans must resolve exactly; missing links stay
unresolved, never silently ignored. Each link declares its role and approved transmission scope.
`context_review` can be global for the bound source/links or per-parent; host review affirms that
required nonlocal dependencies were examined and lists any unresolved ones. A global attestation
applies only to that exact input digest, never a future edited source. Missing/false review permits
provisional local-context evaluation but blocks full completion. Known missing required members
block affected checks before dispatch rather than spending quota on obviously incomplete state.

Boundary overrides cite parent/source spans and exact endpoints. They can resolve segmentation
uncertainty but cannot change source, cross protected interiors or override the genre gate.
All annotation/link/review fields are host data, never instructions taken from article text.

## Legacy prepared input

V1 `sections` input remains accepted within its existing validity limits. Each section's full
`text` is automatically segmented in full mode. Coverage scope is `provided_sections`: it cannot
prove the host supplied every paragraph from an unseen article. Existing context strings remain
complete supplied external context units with stable identities and inherited redaction/permission.

Exact sentence targets are aliases, not extra occurrences. Partial or multi-sentence custom spans
are retained as supplemental diagnostics if explicitly requested; canonical full-mode sentence
checks are still generated. Duplicates/overlaps between explicit targets are rejected; explicit
protected targets follow existing exclusion behavior. Missing targets are filled automatically.
Candidates remain source-parent-local; automatic children do not shift their original offsets.

Raw-source automatic preparation is not constrained to 16 detected sentences or 32 detected units.
Legacy input validity caps are not repurposed as automatic detection caps. Entire input remains
bounded by 1 MiB; malformed/oversize input is `invalid_input`, never certified partial success.

## State and transport windows

Each request belongs to one immutable parent/context bundle and carries:

- `paragraph`: full parent original text after authorized redaction;
- `targets`: up to 16 source-bound sentence/diagnostic entries with stable IDs and redacted slices;
- `related_paragraphs`: complete redacted context members with IDs/roles and source order;
- existing profile, kind, register, audience and purpose;
- authorized candidate data only for requests reviewing those candidates.

Keep structured context records in v2; migrate prompt references explicitly. Ordinary prose
instructions are in questions, never extracted from content. All questions in one request share
this state. A question explicitly references its current target path and scope; its wire ID is
not the only place that identifies the task. Canonical check identities survive target-index/window
changes. Parent-scoped recipes may share a request with targets but occur once per parent.

Scheduling order: local document checks, then parents in source order; within a parent, paragraph
recipes once, sentence occurrences in source order with canonical pattern/recipe order, then candidate
guards. The manifest is established first; batching is only a transport projection.

Pack deterministically using exact post-redaction UTF-8 JSON bytes and at most 48 questions. Shrink
optional target-window membership when necessary; never shrink required parent/context text. One
sentence's recipes may span requests. If no single-question payload fits, mark its checks
`context_too_large`; try independent later bundles only while the same global budget remains.

All requests share the invocation's 32-call and 120-second budget, including preparation time;
per-call timeout ≤15 seconds and body ≤48,000 bytes, response ≤1 MiB. No resets at paragraph/window
boundaries and no automatic retry or chained invocation. A transport/invalid-response halt leaves
all remaining work with explicit reasons. Request-count/time exhaustion marks pending work before
return. Whole-response validation remains atomic: a missing/invalid answer credits none of that
response, while previously validated batches retain their evidence.

## Outputs and exits

Keep old aggregate fields; add `schema_version:2`, `config_version:"2"`, `manifest_digest`,
`source_scope`, segmentation/context/check summaries, sparse outcomes and compact missing groups.
Receipts bind wire-ID mappings to canonical checks, exact state and request digests. No raw prose,
API credentials or hidden protected content appears in health/coverage diagnostics.

Expose separate `source_accounted`, `segmentation_complete`, `answers_complete`,
`context_complete`, `evaluation_complete`, `all_excluded` and `coverage_mode`. Counts distinguish
sentences, unresolved regions, exclusions, required recipes, validated recipes and network requests.
Expanded missing-group views can identify every affected source span/pattern/recipe without
materializing redundant full-prose records. Pending work is never omitted merely to shorten output.

- `prepare`: exit 0 / `prepared` only for complete segmentation/valid manifest; exit 2 /
  `preparation_incomplete` for unresolved boundaries or local preparation limits. Context review can
  still be pending and is separately reported. Invalid input exits 2.
- `evaluate`: exit 0 / `evaluated` only under the new completion invariant, or unchanged
  `key_absent` early return. Other noncompleted/denied/invalid states exit 2. All-excluded inputs
  retain explicit exclusions and do not claim remote evaluation.
- Diagnostic success is explicitly selected-scope success; it cannot certify full-document work.

Version 2 strengthens completion semantics. Consumers must not equate exit 0 on `key_absent`,
`prepared` or a diagnostic with full Jev evaluation. Evidence-role Choice must select `sufficient`; `insufficient`, `none_fit` or a missing answer
blocks affected completion. Interpretation-role `none_fit` is a valid no-match outcome and does
not alone block completion. Classify by explicit recipe role, not a suffix heuristic.
Candidate evidence never automatically applies
an edit; the host retains all five safeguards.

## Analysis remediation: concrete host fields

V2 annotations use `{start,end,kind?,profile?,protected?,paragraph?}`; `protected:true` denotes
an opaque source span, while `paragraph:true` declares an explicit parent override. Source-global
spans are code-point coordinates. Incompatible overlaps are invalid; a protection-only span may
be nested inside an explicit parent. `boundary_overrides` is a list of source-global integer
sentence endpoints within parent bounds (never inside protected spans/character sequences).

A context link is `{parent_start,parent_end,source_start?,source_end?,text?,id?,role?,allowed?}`.
Supply exactly one of a source span pair or an external `text` plus `id`. Source-span links must
match one complete paragraph or structural unit. Missing/unresolvable targets are explicit
unresolved dependencies; malformed coordinate types are invalid input. `allowed:false` prevents
transmission; it never licenses dropping a required dependency to claim success.

`context_review` uses `{reviewed:bool,unresolved:[string,...]}`. Per-parent overrides may be supplied
as `context_reviews:[{start,end,reviewed,unresolved}]` matched to exact parent spans. Reviews bind
the actual input digest, not an article-provided instruction. V1 accepts the same global review
and section-level `context_review`; absence remains unreviewed. Raw v2 candidate edits use
`candidates:[{id,start,end,replacement}]` in source-global coordinates and must fit exactly one parent;
normalization maps them to existing parent-local offsets without altering content.

Recipe roles are explicit config mappings: `evidence` checks sufficiency, `interpretation` checks
interpretation, `violation` is Noul and `degree` is Score. Validate this finite mapping against the
registry on load; unknown roles fail closed. Candidate `meaning` has its separate interpretation
role and `insufficient` disposition. No suffix-only heuristic or probability threshold grants fit.

## Review hardening: large reports and diagnostic scope

Large `coverage`, `work_groups` or `missing` arrays (over 8,192 records) use a lossless
`templates-v1` object in that field, with top-level `ledger_encoding:"templates-v1"`.
The object contains `encoding`, `varying`, `sections`, `templates` and `rows`. Each row is
`[template_index, ...varying_values]`; copy that template and overlay values in `varying`
order. A `section` value indexes the object's `sections`; other values are literal. The
`jev.coverage.expand_records` helper performs this expansion. Fields below the threshold
remain flat lists. This output-size threshold changes representation only; no check,
reason, validated key or receipt is dropped. Consumers must decode before counting records.

Selected scope accepts legacy sections with at least one explicit target; targetless/raw-v2
selected requests are invalid. Unselected parents remain available as context but have no
scheduled checks. Full scope exposes non-sentence legacy targets as `diagnostic_targets`
with `not_checked_in_full_scope`; they do not replace automatically inventoried sentences.
Missing evidence-role answers and unsendable context keep `context_complete:false`.
Unclassified source is unresolved work, never a protected exclusion. Specific first blocking
reasons survive a later global request/deadline halt.
