# Segmentation contract delta: `vi-spans-1` → `vi-spans-2`

This document amends `specs/008-sentence-coverage/contracts/segmentation.md`. Every rule not listed
here is unchanged. The precedence table rows referred to are those of the 008 contract.

## Row 1 — lexical tokens (extended)

Add two token kinds whose internal punctuation is never a sentence boundary:

| Token | Shape | Examples | Not matched |
|---|---|---|---|
| Dotted ASCII identifier | ASCII letters, digits, `_` or `-`, then one or more `.` segments, each starting with a lowercase ASCII letter or digit; not touching another word character on either side | `so-sanh-ban-cu.md`, `example.dev`, `jev.core`, `README.md` | `Tôi về.Bạn`, `về.bạn`, `Done.Next` |
| Markdown link destination | text directly after `](` up to the first `)`, any scheme including relative paths; not the `<...>` or quoted form | `(ghi-chu.md)`, `(../a/b.md)`, `(Ghi.Chu.md)` | — |

A `(` inside a link destination keeps the existing whole-unit `ambiguous_url_closer` reason. A final
`.` that ends an identifier at a real sentence end (`Xem example.dev. Tôi về.`) is still a candidate
boundary, because the identifier stops before it.

## Row 2 — abbreviations (extended during implementation, 2026-10-22)

The dotted-identifier token also matches single-letter abbreviations such as `e.g` and `i.e`. Before
this feature their internal dot left the region unresolved; with the token alone, `Dùng e.g. Python`
would gain a false exact boundary after `e.g.`. A standalone run of single lowercase letters joined
by dots and ending in `.` (`e.g.`, `i.e.`, `a.b.`) is therefore an ambiguous abbreviation at a
possible sentence end, like `v.v.` and `v.d.`. "Standalone" means it follows whitespace, an opening
bracket or quote, or the start of the scanned window, so a URL path such as
`https://example.org/a.b.` keeps its existing boundary (corpus case `url-terminal-period`).

## Row 5 — terminal punctuation (narrowed exemption)

After the punctuation run and any attached closing quotes or brackets:

| Next character | Disposition |
|---|---|
| whitespace | as in 008 |
| end of unit | as in 008 |
| `,` `;` `:` or another terminal punctuation mark (`.` `!` `?` `…`) | **not a boundary**; continue scanning (`?",`, `!,`, `?".`) |
| any other character outside a recognized token | **unresolved**, reason `ambiguous_separator` (008's missing-space rule, reason renamed) |

`unsafe_boundary` is used only when a boundary would split a user-perceived character.

## Reference cases added to the RED baseline or tests

| Case | Layout | Expected |
|---|---|---|
| `- Quy ước đặt tên, giống ghi chú [so-sanh-ban-cu.md](so-sanh-ban-cu.md):` + nested item | markdown | prepared, no unresolved region |
| `- **thời gian**: "tuần trước ai đổi lịch họp?", có đích là bản ghi mới nhất.` | markdown | one exact sentence |
| `- [Đố vui!, bản 2025](https://example.org/x): bài về RAG.` | markdown | one exact sentence |
| `Xem [A](Ghi.Chu.md) rồi báo tôi.` | markdown | one exact sentence |
| `Anh hỏi "ai không muốn họp?". Tôi im.` | markdown | two exact sentences |
| `Mở README.md rồi chạy jev.core nhé.` | markdown | one exact sentence |
| `Xem example.dev. Tôi về.` | markdown | two exact sentences |
| `Tôi về.bạn ở lại.` | markdown | unresolved, `ambiguous_separator` |
| `Done.Next step.` | markdown | unresolved, `ambiguous_separator` |
| `Dùng e.g. Python rồi chạy.` | markdown | unresolved, `ambiguous_abbreviation` |
| `Nghĩa là i.e. Tôi về.` | markdown | unresolved, `ambiguous_abbreviation` |
| `Xem [b](../a/b.md) rồi báo tôi.` | markdown | one exact sentence |
| `Xem [a](b(c).md) nhé.` | markdown | unresolved, `ambiguous_url_closer` |
| corpus `missing-period-space` (`Tôi về.Bạn ở lại.`) | paragraph-lines | unresolved, as before |

The original rows were observed on the planning prototype; the four rows added during implementation were observed on the branch. The corpus keeps its 54 cases; only its `profile`
field changes.
