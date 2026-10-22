# Segmentation contract delta: `vi-spans-1` → `vi-spans-2`

This document amends `specs/008-sentence-coverage/contracts/segmentation.md`. Every rule not listed
here is unchanged. The precedence table rows referred to are those of the 008 contract.

## Row 1 — lexical tokens (extended)

Add two token kinds whose internal punctuation is never a sentence boundary:

| Token | Shape | Examples | Not matched |
|---|---|---|---|
| Dotted ASCII identifier | ASCII letters, digits, `_` or `-`, then zero or more `.` segments starting with a lowercase ASCII letter or digit, then a final `.` segment from the suffix allowlist below; not touching another word character on either side | `so-sanh-ban-cu.md`, `example.dev`, `README.md`, `main.py`, `a.b.vn` | `Tôi về.Bạn`, `về.bạn`, `Done.Next`, `anh.con`, `2025.sau`, `jev.core`, `e.g`, `E.g` |
| Markdown link destination | text directly after `](` up to the first `)`, any scheme including relative paths; not the `<...>` or quoted form | `(ghi-chu.md)`, `(../a/b.md)`, `(Ghi.Chu.md)` | — |

Suffix allowlist (owner decision on review finding S1, 2026-10-22): file extensions `md`, `txt`,
`py`, `js`, `ts`, `json`, `yaml`, `yml`, `toml`, `csv`, `html`, `css`, `sh`, `sql`, `xml`, `pdf`,
`png`, `jpg`, `svg`, `ipynb`, and domain suffixes `dev`, `com`, `org`, `net`, `io`, `vn`. Many
Vietnamese words are plain ASCII (`anh`, `con`, `sau`), so a broader shape certified real missing
spaces as one sentence. Module paths such as `jev.core` are no longer recognized. `com` and `net`
can also be unaccented Vietnamese (`cơm`, `nét`); the risk is accepted with the list.

A `(` inside a link destination keeps the existing whole-unit `ambiguous_url_closer` reason. A final
`.` that ends an identifier at a real sentence end (`Xem example.dev. Tôi về.`) is still a candidate
boundary, because the identifier stops before it.

## Row 2 — abbreviations (extended during implementation, 2026-10-22)

Single-letter abbreviations such as `e.g.`, `E.g.` and `i.e.` never match the identifier token, so
their inner dot stays a missing separator (`ambiguous_separator`). Their final dot must also stay
ambiguous, or the next sentence would be certified: a standalone run of single lowercase letters
joined by dots and ending in `.` (`e.g.`, `i.e.`, `a.b.`) is an ambiguous abbreviation at a possible
sentence end, like `v.v.` and `v.d.`. "Standalone" means it follows whitespace, an opening bracket or
quote, or the start of the scanned window, so a URL path such as `https://example.org/a.b.` keeps
its existing boundary (corpus case `url-terminal-period`).

## Host boundary overrides (review finding S1, 2026-10-22)

Dotted-identifier and link-destination spans are opaque to the scanner's own boundary search, but a
host `boundary_overrides` endpoint inside them is honoured and splits there. An override inside
any other lexical span (protected text, URL, email, number, place name, abbreviation, initials,
ordinal) is still rejected as `invalid_input`, as in `vi-spans-1`. Override validation is a binary
search over strictly overlapping spans merged together, charges one work unit and checks the
deadline per override (review finding S2). Sentence identities bind one digest of the override list
instead of the list itself; the binding is equivalent and costs one hash per invocation.

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
| `Mở README.md rồi chạy main.py nhé.` | markdown | one exact sentence |
| `Mở jev.core nhé.` | markdown | unresolved |
| `Tôi gặp anh.con mèo chạy.` | markdown | unresolved |
| `Năm 2025.sau đó tôi về.` | markdown | unresolved |
| `Xem example.dev. Tôi về.` | markdown | two exact sentences |
| `Tôi về.bạn ở lại.` | markdown | unresolved, `ambiguous_separator` |
| `Done.Next step.` | markdown | unresolved, `ambiguous_separator` |
| `Dùng e.g. Python rồi chạy.` | markdown | unresolved (`ambiguous_separator`, final dot ambiguous) |
| `Nghĩa là i.e. Tôi về.` | markdown | unresolved (`ambiguous_separator`, final dot ambiguous) |
| `Dùng E.g. Python rồi chạy.`, `Gọi I.e. Tôi về.`, `Ví dụ:e.g. Python chạy.`, `Dùng 'e.g. Python rồi.` | markdown | no exact sentence for the abbreviation |
| `Tôi đọc README.md rồi về.` with override after `README.` | markdown | two exact sentences split at the override |
| `Xem [a](b.md) nhé. Tôi về.` with override `[10]` | markdown | `Xem [a](b.`, `md) nhé.`, `Tôi về.`, all exact |
| `Xem [b](../a/b.md) rồi báo tôi.` | markdown | one exact sentence |
| `Xem [a](b(c).md) nhé.` | markdown | unresolved, `ambiguous_url_closer` |
| corpus `missing-period-space` (`Tôi về.Bạn ở lại.`) | paragraph-lines | unresolved, as before |

The original rows were observed on the planning prototype; rows added during implementation and after review were observed on the branch. The corpus keeps its 54 cases; only its `profile`
field changes.
