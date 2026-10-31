# PR28 follow-up: review evidence without a larger runtime

## Pinned design source and scope

The owner's completed research used [mattpocock/skills at a496f5513d4a4cf889bc48e189e579f4b0bdf6aa](https://github.com/mattpocock/skills/tree/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa). Its lessons motivate explicit dependency reading before review, independent content/style verdicts, missing-input examples and exact-current-artifact review. This is community workflow research, not a Vietnamese benchmark. No upstream source code, course text or substantial template passage is copied/adapted here; the Vietnamese instructions and Python harness are original. Historical wrapper-loading problems are not asserted to be current upstream defects.

Selected gaps: adapter said only “before editing”; review-only had no explicit route; current five gates already contain the meaning rubric, so reuse them rather than add another runtime reference. Core adds four lines, from 131/9189 characters to 135/9699 characters. Whole-article/sample review uses the same explicit files as that task even without edits. Meaning and style get independent conclusions; source attribution stays explicit. The writing workflow adds only a missing reader-concept/example check, with no forced paragraph approvals or invented personal experiences.

## Offline evidence contract

`benchmarks/review_contract.py` is benchmark tooling, outside the shipped skill payload. It has no Git, model, network, evaluator or credential lookup. `prepare(case, root, candidate_bytes)` hashes the current bytes and explicit expected instruction files, embeds source/task/candidate and excludes semantic expected answers. `check(packet, report, current_candidate_bytes, trace=None)` verifies that exact packet/candidate, quote membership and two independent verdict fields are structurally consistent. A changed uncommitted candidate invalidates an old report even if HEAD stayed fixed. No combined quality score can replace the two verdicts.

Report shape: packet_sha256, candidate_sha256 and two objects meaning/style, each with status (clear/issue/uncertain/not_assessed) and findings. Issue needs findings; clear/not_assessed must not contain findings. A finding anchors candidate_quote and optional source_quote in packet text and carries a reason. Quote existence and consistent labels do not prove the reason is true.

Expected routing and observed execution are distinct. Optional trace events read(path, sha256) must precede the one review(candidate_sha256) event and match the packet's required files. The harness checks those supplied receipts but does not authenticate their origin. Even a matching trace returns actual_agent_reads=not_attested and semantic_correctness=not_evaluated. A report's claimed_reads alone is ignored as execution evidence. Actual host-tool read traces and semantic A/B remain pending; there are no new model calls or sharing permissions.

## Cases and separation

Six original public-safe development cases live in tests/fixtures/review_contract/development.json: review-only scope/modality, supplied-sample article review, sparse brief without a personal sample, missing reader example under pressure to invent experience, attribution and exact-candidate drift. Their expected semantics are design labels, not observed outputs or independent human judgments. Mechanical tests prepare packets and validate paths; they do not prove the agent followed the route.

Heldout collection is separately declared in heldout-plan.json, currently empty/pending. It cannot be reported as blind evaluation. Fresh texts and labels must be fixed separately; neither these development cases nor the five professional style sources already used in design may become the independent heldout set.

## Validation and review

The new module initially failed import because absent; after implementation its 12 initial checks passed. Independent read-only review found that clear/not_assessed verdicts could carry findings and be summarized as clear. A regression test reproduced both contradictions before the fix; all 13 harness tests then passed. No semantic correctness claim follows. The existing packet binding, trace-attestation limits and explicit runtime routes had no other concrete findings in that review.

Ran `python3 -B -m unittest tests.test_review_contract tests.test_distribution tests.test_selective_reading tests.test_package_security -v`: **66 tests, OK, 21.982s**. Package validator and registry --check pass; git diff --check is clean. This covers the bounded follow-up. Registry/pattern bodies, metadata0.13.2 and the user's original dirty README remain unchanged. Full CI, head and required-review status are verified after push. No approve, bypass, tag, release or install is authorized by this research.
