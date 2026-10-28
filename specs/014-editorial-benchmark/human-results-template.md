# Mẫu điền sau khi nhận đủ hai phiếu thật

**Chưa có kết quả khảo sát trong tài liệu này. Không thay ô trống bằng số kiểm thử.**

- Cohort và binding SHA-256: `[điền từ receipt]`.
- Hai phiếu đã xác nhận, thời điểm xuất và selection SHA: `[điền]`.
- Tổng số nhãn phân loại có dữ liệu: `[n]/320`; số bản có ít nhất một nhãn: `[n]/160`.
- Nguồn độc lập: 20; hai người chấm cố định. Nguồn tuyển chọn từ một bên phát hành SFT.

| Chế độ | Người chấm | Giữ đúng / đổi ý / chưa rõ / thiếu | Dễ đọc hơn / tương đương / khó hơn / chưa rõ / thiếu |
|---|---|---|---|
| `[bốn chế độ, từng người]` | `[A/B]` | `[tổng 20]` | `[tổng 20]` |

Kết quả chính trên cùng agent `[Codex + model/effort]`: sau Vietnamizer so với bản AI gốc,
`[n]/20` bản được người A đánh giá dễ đọc hơn, `[n]/20` tương đương, `[n]/20` khó hơn,
`[n]/20` chưa rõ và `[n]/20` thiếu. Báo tương tự cho người B và bốn chế độ.
Tỷ lệ dễ đọc hơn trên nhãn xác định `[ước lượng %]`, CI 95% `[cận dưới; cận trên]`,
`[n]/20` cụm nguồn đủ. Báo riêng từng người và trung bình hai người cố định; phần
thiếu/chưa rõ `[điền]`. Không gộp hai người thành 40 nguồn độc lập.

Báo đồng thời giữ đúng / có chỗ bị đổi `[số đếm và tỷ lệ với mẫu số thực]`.
Cải thiện độ dễ đọc không đồng nghĩa giữ nghĩa tốt hơn. So sánh Vietnamizer với prompt
thường / yêu cầu cơ bản và Jev với Vietnamizer là bổ sung trong cùng agent:
`[chênh lệch điểm phần trăm, CI, n ghép đủ và thiếu/chưa rõ]`.
Không xếp hạng runtime hoặc gộp nhãn Codex/Gemini. Không chọn subset Jev thuận lợi.
Phương pháp được sửa ngày26/10/2026 sau khi tạo đầu ra; xem within-agent-amendment.md.

Đồng thuận: `[số cặp đủ]`, `[tỷ lệ trùng nhãn]`, kappa danh nghĩa `[giá trị hoặc N/A]`.
Ma trận có cả thiếu/chưa rõ; các cặp đầu ra phụ thuộc cùng nguồn, không phải 80 mẫu độc lập.

Ca cụ thể: trích nguyên nhận xét và đoạn được nhắc tới, kèm ID nguồn/nhãn A–D/khóa ghép.
Nhận xét của người chấm không tự thành quy tắc tiếng Việt hoặc bằng chứng AI tạo nguồn.

Giới hạn bắt buộc: chỉ 20 nguồn, một bên phát hành, generator model chưa xác thực,
backend Codex chưa có attestation độc lập, hai người chấm cố định, Jev chỉ đủ phạm vi
ở 1/20 nguồn. CI điều kiện trên bộ nguồn này; không có kiểm định xác nhận hoặc bảo đảm
khả năng khái quát. Dữ liệu giả lập dùng kiểm phần mềm không nằm trong kết quả thật.
