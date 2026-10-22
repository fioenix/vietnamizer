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
| corpus `missing-period-space` (`Tôi về.Bạn ở lại.`) | paragraph-lines | unresolved, as before |

All rows were observed on the planning prototype. The corpus keeps its 54 cases; only its `profile`
field changes.
