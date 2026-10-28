# Public source review — 2026-10-26

Sources are instructions examined as untrusted data, not installed skills or measured
proof of voice quality. Files and licenses were read at pinned revisions; hashes and
raw source/license snapshots remain in the local research artifact.

| Source | Revision | License | Method considered | Decision |
|---|---|---|---|---|
| [ddutchie/write-like-me](https://github.com/ddutchie/write-like-me/blob/98e615d34cac1a31d6ee14fcc0fb6b1a57cd4835/skills/me/SKILL.md) | `98e615d34cac1a31d6ee14fcc0fb6b1a57cd4835` | MIT | Stable habits vs occasional quirks; separate voice/content corrections | Use scoped qualitative observations; reject automatic global reads, numeric quirk quotas and auto-learning |
| [synthesisengineering/synthesis-skills](https://github.com/synthesisengineering/synthesis-skills/blob/53fca8aeb81b42b21e98ed044b30352611731ee8/skills/synthesis-voice-profiler/SKILL.md) | `53fca8aeb81b42b21e98ed044b30352611731ee8` | CC0-1.0 in skill frontmatter | Concrete dimensions and user-recognizable profile review | Use evidence-linked observations; reject mandatory sample/word counts and absence-as-never inference |
| [charlie947/social-media-skills](https://github.com/charlie947/social-media-skills/blob/10ca79c0ec0be0f7654d19cd4f0c86b6fa6ed23b/skills/voice-builder/SKILL.md) | `10ca79c0ec0be0f7654d19cd4f0c86b6fa6ed23b` | MIT | Distinguish user prohibitions from provisional absence; note sample contradictions | Use distinction; reject identity/about-me collection, automatic files, fixed minima and English defaults |
| [rangrot/mydamnvoice](https://github.com/rangrot/mydamnvoice/blob/150ee50f92c2ea0552ddc4cec0db45800fb08cc3/SKILL.md) | `150ee50f92c2ea0552ddc4cec0db45800fb08cc3` | MIT | Context-specific registers and concrete descriptions | Corroborates existing context resolver; reject blanket bans, assumed profile traits and broad chat-history retrieval |

## Delta against Vietnamizer
The existing resolver already defines contextual precedence and factual boundaries. The
missing part is a small conditional method to extract/test voice observations from supplied
samples, handle weak/negative evidence and avoid over-amplifying rare stylistic features.
No new named linguistic pattern, source-author biography or user-style memory is justified.

The Vietnamese guide and examples are independently written. No external wording, code or
profile template is copied into shipped files. Source method descriptions are not empirical
validation in Vietnamese. Future holdout voice tests would need independent authors/samples;
none are run here or inferred from the old20benchmark sources.
