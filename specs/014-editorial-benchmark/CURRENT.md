# Trạng thái benchmark hiện hành

**Quyết định hiện hành ngày 26/10/2026:** tạm bỏ người chấm ở giai đoạn này và công bố
[báo cáo mô tả thực thi](execution-report.md), gồm số liệu từng nguồn, 7 hình phân tích
và cách tái lập. Không chạy thêm benchmark hoặc model chấm. Hai Forms giữ nguyên;
không đọc phiếu và không coi việc chờ khảo sát là điều kiện hoàn thành báo cáo này.
Nhãn chất lượng chưa có; chưa kết luận Vietnamizer giúp văn bản tốt hơn.

Ngày 26/10/2026, mục tiêu là **trước và sau khi dùng Vietnamizer trên cùng agent/model**.
[Phụ lục phân tích](within-agent-amendment.md) xác định bản AI gốc là mốc trước, các
bản biên tập là mốc sau; so sánh giữa chế độ chỉ là phân tích bổ sung trong cùng agent.
Không xếp hạng Codex/Gemini và không gộp hai bộ thành một mẫu thống kê.

| Bộ dữ liệu | Thực thi | Chấm chất lượng |
|---|---|---|
| Codex,20 nguồn AI công khai × 4 chế độ |80/80, một bản cuối mỗi chế độ/nguồn |Tạm bỏ chấm người; giữ Forms và dữ liệu cũ |
| Gemini cùng20 nguồn × 4 chế độ |80/80 trong epoch-v3; đã kiểm raw/seal/model/hội thoại/tool |Chưa có nhãn người; không thêm vào Forms Codex |

Bộ Gemini ghi nhận CLI model gemini-3.8-flash-medium,80 hội thoại riêng, chỉ gọi finish,
không có tool thực thi. Biên bản local:
`artifacts/014-gemini-text-only-20261026/epoch-v3/completion-audit-20261026.json`.
Registry 60tool là metadata chung; đối chứng capability và guard thực thi được lưu riêng.
Hai lượt host cũ giữ làm dữ liệu chẩn đoán, không tính vào80 bản mới.

Hai Forms Codex giữ nguyên160 mục mỗi form, ảnh, nhãn ẩn, item ID, thứ tự và link trả lời.
Hai câu hỏi nền đã được bỏ ở lần sửa trước. Nguồn Vietverse có nhãn synthetic_llm theo
nhà phát hành; chưa có bằng chứng độc lập về model sinh nguồn. Jev cộng dồn usage và
dự phòng 0,456368556/2 USD; chỉ 1/20 nguồn đủ phạm vi, các ca thiếu vẫn giữ trong phân tích.

Workspace phân tích mới:
`artifacts/014-within-agent-amendment-20261026/workspace-v5`.
Báo tỷ lệ trước/sau, giữ nghĩa/giọng riêng, thiếu/chưa rõ, CI theo 20 nguồn và đồng thuận.
[Runbook](human-analysis-runbook.md) dùng exporter chỉ đọc mới; workspace-v2 và archive
cũ giữ nguyên. Không đọc phiếu live, chạy model/Jev hoặc sửa Forms trong lần đổi mục tiêu.

T016 tạm dừng theo quyết định bỏ chấm người ở giai đoạn hiện tại; không đánh dấu đã hoàn tất. Bộ Gemini cần nhãn
riêng trước khi có kết luận chất lượng. Kết quả thực thi, độ khác ký tự và test phần
mềm không chứng minh lợi ích biên tập. Không chạy thêm benchmark theo quyết định hiện tại.

Pilot giả lập, lỗi raw Jev cũ, các phương án Docker và lượt host thất bại là hồ sơ
lịch sử riêng. T051–T053 của phương án Docker chưa được nghiệm thu; việc host thành
công không tự hoàn tất chúng. T006 pilot giả lập cũ không phải bộ công khai hiện hành.
