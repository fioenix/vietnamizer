# Data model

Corpus row: id,role(sample|judge_reference|voiced), author attribution, title, commit/path/URLs, raw/excerpt hashes, topic_family, words, extraction/provenance/short-excerpt limitation. Role sets3/2/4; no article/family crosses roles.
Manifest: source/config/code fingerprints, ordered IDs56, caps, model/runtime/agent bindings, seeds, no Jev, attestation limits.
Attempt: ID/provider/stage, immutable reserved record before spawn, input/schema/config/manifest hashes, raw CLI/native/wrapper streams, status/session/usage/time/error, final parsed output. reserved→completed|failed only; failed/incomplete never retried.
Judge block: original,4anonymous candidates,2judge-only references,4anonymous comparisons, concealed mapping outside prompts. Same inputs apart from positions/aliases across judges.
Assessment:5scores(voice/readability1–5; meaning clear|minor|major|uncertain), exact evidence quote bindings,4preferences(left|right|tie|uncertain), reasons. Missing/invalid remains visible.
Analysis: per-case/per-stratum/per-judge scores, four paired contrasts, all meaning errors, disagreement, original-to-output shifts, limitations; no summed safety/style score.
