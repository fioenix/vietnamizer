# Phục hồi pilot Codex + Jev — 25/10/2026

Đã nhận đủ câu trả lời Jev cho **20/20 văn bản** và tạo đủ **20 bản Codex + Jev mới**.
Bộ chấm hiện tại có **80 bản cuối**, 20 bản mỗi chế độ. Đây là kết quả thực thi và đối soát
dữ liệu; chưa có kết quả chất lượng biên tập được chấm độc lập.

| Chỉ số thực thi | Kết quả |
|---|---:|
| Văn bản đã nhận đủ câu trả lời, đối soát nguồn và phân đoạn | 20/20 |
| Câu trả lời Jev hợp lệ trong các lượt cuối | 15.449 |
| Kiểm tra cơ học riêng | 20 |
| Kiểm tra bắt buộc còn thiếu | 0 |
| Văn bản có cờ ngữ cảnh native đầy đủ | 3/20 |
| Bản Codex mới hoàn tất, không có tool call trong raw được kiểm | 20/20 |
| Request mạng Jev cộng dồn, không đếm trùng kế thừa | 435 |
| Request mới có raw HTTP | 402 |
| Chi phí Jev ghi nhận từ usage, USD | 0.192088554 |
| Usage cộng dự phòng khoản chưa rõ hóa đơn, USD | 0.200346090 / 2 |
| Request lịch sử còn dự phòng hóa đơn | 3 |

Tiền tính từ input token theo giá đã kiểm tra, chưa phải hóa đơn đối soát. Chi phí trên chỉ
là Jev; Codex dùng quota subscription và không trả chi phí tiền mặt theo từng lần chạy.
Model Jev phản hồi được xác nhận là `jev-1.14.0`; Codex yêu cầu `gpt-6.1-sol` ở mức medium,
nhưng raw CLI chưa cung cấp xác nhận phiên bản backend thực tế.

## Lỗi đã quan sát và cách phục hồi

Runner benchmark cũ gộp nhiều loại lỗi thành `service_failed` và chỉ lưu response sau khi
kiểm định. Ba request lỗi trước đây không còn đủ dữ liệu để kết luận nguyên nhân. Hai
payload cũ được gọi lại trong lượt chẩn đoán đã trả HTTP 200 và đạt kiểm định; điều đó
không chứng minh nguyên nhân lỗi cũ đã được tìm ra.

Raw capture mới ghi nhận 6 response HTTP 200 tự mâu thuẫn: Score không khớp trung bình
theo xác suất ở P05; Choice chọn phương án có xác suất thấp hơn phương án khác ở P07, P09, P16, P18. Xem [bằng chứng từng lỗi](recovery-diagnosis.md) và [protocol](recovery-protocol.md).

Adapter đã giữ nguyên **187 câu trả lời hợp lệ**, chỉ hỏi lại **6 câu lỗi** với cùng state,
model và câu hỏi. Bản ghép được ghi rõ là `composite_evidence`, có nguồn và hash của sáu
file cho từng request hỗ trợ. Chi phí tính theo request mạng thực; không tính thêm lần tái
sử dụng hay bản ghép. Không sửa số trong raw response, nới tolerance hoặc gọi lại câu trả
lời hợp lệ để chọn kết quả khác. Các adapter đã qua review độc lập trước khi chạy.

## Nhận đủ phản hồi và ngữ cảnh

Nhận đủ câu trả lời khác với đủ ngữ cảnh để kết luận. Jev có thể trả một câu hợp lệ nhưng
chọn “chưa đủ ngữ cảnh”; các cờ native `context_complete`, `scope_complete` và
`evaluation_complete` vẫn được giữ nguyên. Bản cuối được tạo sau khi nhận đủ câu hỏi bắt
buộc, đối soát nguồn và phân đoạn, rồi tái dựng toàn bộ bằng chứng offline từ raw replies.

| Văn bản | Câu trả lời hợp lệ | Cơ học | Còn thiếu | Ngữ cảnh native |
|---|---:|---:|---:|---|
| P01 | 876 | 1 | 0 | có câu chưa đủ ngữ cảnh |
| P02 | 952 | 1 | 0 | có câu chưa đủ ngữ cảnh |
| P03 | 964 | 1 | 0 | có câu chưa đủ ngữ cảnh |
| P04 | 972 | 1 | 0 | có câu chưa đủ ngữ cảnh |
| P05 | 952 | 1 | 0 | có câu chưa đủ ngữ cảnh |
| P06 | 884 | 1 | 0 | có câu chưa đủ ngữ cảnh |
| P07 | 876 | 1 | 0 | có câu chưa đủ ngữ cảnh |
| P08 | 792 | 1 | 0 | có câu chưa đủ ngữ cảnh |
| P09 | 792 | 1 | 0 | có câu chưa đủ ngữ cảnh |
| P10 | 800 | 1 | 0 | đủ |
| P11 | 872 | 1 | 0 | có câu chưa đủ ngữ cảnh |
| P12 | 839 | 1 | 0 | có câu chưa đủ ngữ cảnh |
| P13 | 847 | 1 | 0 | có câu chưa đủ ngữ cảnh |
| P14 | 650 | 1 | 0 | có câu chưa đủ ngữ cảnh |
| P15 | 696 | 1 | 0 | có câu chưa đủ ngữ cảnh |
| P16 | 642 | 1 | 0 | có câu chưa đủ ngữ cảnh |
| P17 | 710 | 1 | 0 | có câu chưa đủ ngữ cảnh |
| P18 | 630 | 1 | 0 | đủ |
| P19 | 58 | 1 | 0 | đủ |
| P20 | 645 | 1 | 0 | có câu chưa đủ ngữ cảnh |

## Thiết kế và giới hạn chất lượng

Bộ so sánh có 20 bản không skill, 20 bản dùng prompt thường, 20 bản Vietnamizer tự rà và
20 bản Vietnamizer + Jev. Hai chế độ cuối dùng chung bản nháp và chỉ dẫn rà một lượt. Ba
nhóm đối chứng được tái sử dụng từ các đợt trước, có khác biệt về thời điểm chạy; đây không
phải thí nghiệm bốn nhóm chạy đồng thời và phân ngẫu nhiên. Các bản fallback/partial cũ
vẫn giữ nguyên trong lịch sử, không dùng làm bản cuối của nhóm Jev hiện tại.

Chưa có hai lượt chấm độc lập hoặc tập holdout. Không có điểm chất lượng, mức cải thiện
hay kết luận Jev giúp biên tập tốt hơn. Đơn vị lấy mẫu là 20 văn bản giả lập; 80 bản cuối
và số câu hỏi không phải các mẫu độc lập. Antigravity vẫn theo gate cách ly riêng; đợt này
không khôi phục các ô Gemini chưa chạy.

Dữ liệu thực thi: `artifacts/014-jev-recovery-20261025/finish-report.json`, raw request/reply,
pass seals, composites, prompt, stdout và khóa bộ chấm trong cùng thư mục local. Xem
[chỉ mục lưu trữ và bảng phân tích](data-archive.md) cho snapshot mới và các giới hạn bằng chứng.

## Kiểm chứng

50 test liên quan đến runner pilot và các adapter phục hồi đã đạt; không chạy toàn suite.
Có test offline từ lỗi thật P05: giữ 39 câu hợp lệ → hỏi riêng câu lỗi → core replay →
đối soát bằng chứng → Codex giả lập → báo cáo. Test giả lập không đo chất lượng tiếng Việt.
Review độc lập đã đối soát đủ 20 bản cuối, raw, nguồn, bộ chấm 80 bản và chi phí.
Archive mới đã đối chiếu 3.556 file theo digest và đọc lại bảng/checksum độc lập.
Ba raw reply lỗi lịch sử vẫn không thể phục hồi.
