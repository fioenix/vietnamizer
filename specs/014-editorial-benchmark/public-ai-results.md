# Benchmark từ nguồn AI công khai — 25/10/2026

Đã tạo **80/80 bản Codex cho 20 nguồn × 4 chế độ**, mỗi nhánh một lượt tạo bản cuối.
Chưa có nhãn chất lượng của người thật. Hai Forms mới đang được dựng và nghiệm thu;
không dùng kết quả pilot giả lập hoặc điểm model cũ làm kết quả của đợt này.

## Nguồn và tính đối chiếu

Nguồn là [TTP01/Vietverse-SFT-Preview](https://huggingface.co/datasets/TTP01/Vietverse-SFT-Preview/tree/6b4e4a86e3b399318ac4fe91b2bbe64501037f40), revision
`6b4e4a86e3b399318ac4fe91b2bbe64501037f40`. Bên phát hành ghi `synthetic_llm` và giữ
pipeline trace; giấy phép Apache 2.0 theo thẻ dữ liệu. Chưa có API gốc/model sinh nguồn
được đối soát. Không dùng bộ phát hiện AI hoặc xác suất văn phong làm nhãn nguồn gốc.

Giữ đủ 100 dòng JSONL nguyên bản (SHA-256
`ae0660fa99b8df2e2f78e4a3698e64865754d620d3a8b5e6e139c545955db11c`), metadata,
thẻ dữ liệu, câu hỏi gốc và toàn bộ quyết định tuyển/loại. Chọn 20 câu trả lời nguyên văn
đầu tiên đạt điều kiện theo thứ tự gốc, 120–550 đơn vị cách nhau bằng khoảng trắng,
không code/đa lượt và không thuộc các phạm vi đã loại trong protocol. Không chọn theo
đầu ra biên tập hoặc điểm chất lượng của nhà phát hành.

Một bên phát hành, dữ liệu đã tuyển cho huấn luyện hội thoại, chưa rõ trùng dữ liệu
huấn luyện của model biên tập. Kết quả không đại diện cho bài đăng mạng xã hội hoặc mọi
thể loại. Các bundle có profile kỹ thuật/học thuật, đồng thời yêu cầu giữ dạng giải thích
đối thoại và xưng hô của bản gốc; không suy kết quả sang marketing/blog cá nhân.

## Thực thi

Cấu hình yêu cầu Codex `gpt-6.1-sol`, effort `medium`, CLI 0.164.0; chưa attestation
model backend. Dùng quyền ChatGPT subscription hiện có, không chuyển sang API key trả
phí. Mỗi nhánh nhận cùng nguồn/người đọc/mục đích; Jev tư vấn trên bản gốc trước bản cuối.
Các trial dùng workspace tạm, cấu hình bỏ qua discovery skill host; không ghi nhận tool
ở cả 80 stdout. Mọi đầu ra hợp lệ giữ từ lượt đầu, không gọi lại để chọn bản đẹp hơn.

| Chế độ | Hoàn tất | Trùng nguyên văn bản gốc |
|---|---:|---:|
| Yêu cầu cơ bản | 20 | 0 |
| Prompt thường | 20 | 0 |
| Vietnamizer | 20 | 1 |
| Vietnamizer + Jev | 20 | 2 |

Đổi khoảng trắng cũng tính là khác; chỉ số này không đo chất lượng. Chưa có điểm giữ
nghĩa, giữ giọng, dễ đọc, precision/recall hoặc kết luận hơn đối chứng của bộ mới.

## Jev: bằng chứng, phần thiếu và chi phí

576 request mạng mới: 548 response validated, 23 response sai schema, 5 timeout không
có response. 19 composite giữ nguyên câu hợp lệ và nguồn từng câu, chỉ ghép câu được
phục hồi theo đúng payload. Không sửa điểm/phân phối để ép hợp lệ. Mỗi response lỗi chỉ
được phục hồi một lần; lỗi lặp lại kết thúc tư vấn, không lấy mẫu lần ba.

- Phạm vi hoàn tất theo hợp đồng: 1/20 nguồn (R017). 19 nguồn có tư vấn thiếu vì trần
  request/thời gian, ngữ cảnh/phân đoạn hoặc dịch vụ. Đủ phản hồi cho những câu đã lên
  lịch chưa đồng nghĩa đã kiểm hết nguồn.
- R013/R014 kết thúc sau lỗi schema ở cả lượt phục hồi: chỉ dùng prefix hợp lệ, batch
  lỗi là không chấm được. R019 hết thời gian ở cặp request cuối; không coi là bằng chứng
  dịch vụ ngừng hoạt động, không hỏi lần ba.
- R020 giữ nguyên pass thất bại do callback quá deadline dù raw trả muộn hợp lệ. Pass
  đối soát riêng dùng lại raw hợp lệ, chỉ hỏi phần chưa hỏi trong trần, không retry
  transport mới. Coverage chính của R020 lấy từ pass đối soát; hai pass giữ riêng.
- Tối đa 32 request mới/nguồn, 640 mới toàn đợt, trần 2 USD cộng dồn. Các lượt sửa lỗi
  và chưa rõ tiền vẫn tính vào trần; không đặt lại bộ đếm.

| Chi phí Jev theo usage/dự phòng | USD |
|---|---:|
| Usage đã biết của đợt mới | 0.242259906 |
| Đợt mới, gồm dự phòng 5 lượt chưa rõ tiền | 0.256022466 |
| Đợt trước, gồm dự phòng | 0.200346090 |
| Tổng cộng dồn | **0.456368556 / 2** |

Tổng có 1.011 request gồm 435 lượt trước. Có 8 lượt chưa rõ tiền trên cả hai đợt, 5
trong đợt mới. Đây là đối soát ledger theo giá input 0.042 USD/triệu token, không phải
hóa đơn nhà cung cấp. Không cộng usage lặp của cache/core-pass thành tiền mạng mới.

Không diễn giải kết quả của nhánh có Jev thành hiệu quả khi Jev luôn sẵn sàng hoặc kiểm
đầy đủ. Mọi nguồn, gồm ca tư vấn thiếu, vẫn nằm trong phép so sánh chính.

## Người chấm và dữ liệu phân tích

[Protocol](public-ai-human-protocol.md) đã chốt: hai người chấm độc lập, mỗi người đủ
20 × 4 bản; ảnh gốc/sửa hai cột, hai bảng chọn và một câu nhận xét. Xáo nhãn và thứ tự
riêng, khóa ghép giữ ngoài form. Đơn vị thống kê là 20 nguồn; CI bootstrap theo nguồn,
không xem 160 phiếu đầu ra là 160 mẫu độc lập. Báo riêng thiếu/chưa rõ và đồng thuận.

Raw và dữ liệu dựng lại biểu đồ giữ local trong
`artifacts/014-public-ai-benchmark-20261025-v2` và
`artifacts/014-public-ai-human-20261025-v1`. Có bảng `outputs.csv`, `jev-requests.csv`,
`jev-coverage.csv`, `evaluation-passes.csv`, đối soát tiền, source hashes, toàn bộ prompt/
stdout, raw HTTP, composite, lỗi, pass gốc/pass đối soát và ảnh/contract A/B. Script xuất
CSV chạy offline, không gọi model. Form ID, khóa ghép và link người chấm giữ local.

Hai Forms đã được đối chiếu đủ 160 ảnh với dữ liệu đóng băng, đúng 162 mục/form và mở nhận phiếu với quyền ai có link. Không thu email, không công khai kết quả; 0 phiếu ở lần đọc lại ngày 25/10/2026 lúc 23:58 giờ Việt Nam. Link thật đã mở trong phiên đăng nhập của chủ form; chưa kiểm bằng phiên ẩn danh. Bằng chứng provider/UI và khóa ghép giữ local. Archive được giao riêng sau khi đọc lại toàn bộ checksum.

Cập nhật 26/10/2026: đã gỡ hai câu hỏi về người chấm trước khi có phiếu. Mỗi form còn
160 mục, giữ nguyên phần đánh giá và link trả lời. Dữ liệu schema mới được lưu trong
`artifacts/014-public-ai-forms-no-background-20261026`; archive ban đầu giữ nguyên.
