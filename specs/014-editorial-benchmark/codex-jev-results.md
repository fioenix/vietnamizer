# Kết quả pilot Codex + Jev ngày 25/10/2026

**Đã hoàn tất tạo 40 bản Codex mới; phần chứng minh hiệu quả Jev chưa hoàn tất.** Có 80 bản
cuối trong bộ chấm bốn chế độ, nhưng chỉ hai văn bản thực sự nhận tư vấn Jev một phần.
Chưa có chấm chất lượng độc lập; không có kết luận chế độ nào biên tập tốt hơn.

## Đầu ra và phép so sánh

Dùng 20 văn bản giả lập phát triển, không phải holdout. Codex CLI 0.164.0, yêu cầu model
`gpt-6.1-sol`, reasoning medium, forced ChatGPT login, hội thoại mới cho từng bản. CLI chưa
cung cấp xác nhận phiên bản backend thực trả lời; không suy từ tên model được yêu cầu.

| Chế độ trong bộ chấm | Số bản cuối | Nguồn |
|---|---:|---|
| Không skill | 20 | Tái sử dụng đợt gốc |
| Prompt biên tập thông thường | 20 | Tái sử dụng đợt gốc |
| Vietnamizer tự rà | 20 | Một lượt sửa mới từ bản nháp Vietnamizer gốc |
| Vietnamizer + Jev, gồm fallback | 20 | Cùng bản nháp, cùng lượt sửa; mức tư vấn ghi riêng dưới đây |

Cặp tự rà/có Jev được kiểm soát số lượt sửa. Hai baseline cũ có số lượt khác và được tái sử
dụng ở thời điểm trước; toàn bảng không phải thí nghiệm kiểm soát số lượt hay backend snapshot.
20 bản Vietnamizer gốc vẫn được giữ làm bản nháp, không tính thêm vào 80 bản cuối.
Có 40 Codex starts mới, 40 hoàn tất, không lỗi generation hoặc tool contamination được quan sát.

Median thời gian lượt Codex tự rà: 10.508 giây;
nhánh có Jev/fallback: 10.654 giây. Số thứ hai
trộn hai bản có tư vấn một phần với 18 bản không có tư vấn, chưa gồm thời gian gọi Jev;
không dùng nó làm kết luận Jev nhanh/chậm hoặc hiệu quả hơn.

## Jev đã thực sự làm gì

Ghim `jev-1.14.0`. Đã thử ba văn bản, tổng **33 request**, **30 request được xác thực**;
request không đồng nghĩa với một check ngữ nghĩa. P01/P02 của v1 được tiếp nhận nguyên byte
sang v2, không gửi lại. P03 thử một lần rồi circuit breaker dừng mọi lệnh gọi còn lại.

| Mức tiếp nhận tư vấn | Số văn bản | Chi tiết |
|---|---:|---|
| Hoàn tất phạm vi | 0 | Không được suy partial thành pass |
| Một phần | 2 | P01: 21 request hợp lệ; P03: 9 request hợp lệ |
| Đã thử, không có tư vấn hợp lệ | 1 | P02 lỗi request đầu |
| Chưa gọi do circuit breaker | 17 | P04–P20; Codex tạo fallback, không nhận treatment Jev |

Ba request không được xác thực có nguyên nhân **chưa xác định**. Wrapper gom lỗi transport,
validation và ghi artifact vào một nhóm, thiếu raw reply lỗi để phân biệt. Chưa đủ bằng chứng
quy lỗi cho provider. Những raw payload/reply hợp lệ còn đủ và được đối soát lại trước advice.
Không dùng failed, late hoặc missing checks làm bằng chứng đạt. Không có policy số tự áp edit.

Hai cặp có tư vấn một phần chỉ phục vụ quan sát phát triển, chưa đủ cho tuyên bố hiệu quả Jev.
Giữ bảng tổng đủ 20 văn bản; các bản fallback không được trình bày như kết quả nhận tư vấn.
Xem [protocol và điều chỉnh v2](jev-extension.md).

## Chi phí và kiểm chứng

- Trần owner duyệt: **2 USD** cho Jev; không mua thêm credit hoặc chuyển provider.
- Usage được xác thực: **331.356 input token**, chi phí tính theo giá **0,013916952 USD**.
- Giữ ba khoản dự phòng cho request chưa rõ billing: tổng known usage + dự phòng
  **0,022174488 USD**, còn dưới trần. Chưa phải hóa đơn đã đối soát.
- Giá kiểm tra ngày 25/10/2026: 0,042 USD/triệu input token, output miễn phí,
  [nguồn TypeSafe](https://docs.typesafe.ai/models). Codex dùng quota gói hiện có;
  CLI không trả chi phí tiền cho từng lượt, nên báo là chưa biết.
- **32 targeted tests đạt**: `python3 -B -m unittest tests.test_jev_pilot tests.test_editorial_pilot`.
  Gồm test ngân sách, không retry, digest, đối soát raw response, mapping, bảo toàn và circuit breaker.
  Hai test tích hợp dùng artifact lịch sử local; thiếu artifact thì skip, không giả nhận đã kiểm.
- Review code độc lập đã kiểm các sửa v1/v2 trước smoke. Không chạy full suite, chưa phát hành gói.

Bằng chứng local: `artifacts/014-codex-jev-20261025-v2/`, gồm manifest, nguồn/bản nháp,
raw requests/responses, ledger chi phí, 40 Codex raw outputs, report, 80 bản cuối và bộ chấm
ẩn tên chế độ. `reviewer-a.json`/`reviewer-b.json` chưa có nhãn người chấm. Raw runs bị gitignore;
chúng chưa được công bố như một evidence bundle để người ngoài tái kiểm.

Manifest digest v2: `deb8a4e39ff50196e0746890695f9cb22fc32f1e1e1cfe2d6f00d5eb43c5b907`. Source v1 được giữ trong thư mục v1; manifest mới ràng buộc
nguyên byte bằng chứng kế thừa, không sửa manifest/status/seal cũ. Lỗi digest input của harness
v1 được tái hiện, sửa và kiểm bằng fake end-to-end trước khi tạo đầu ra Codex v2.

Còn thiếu: phân loại nguyên nhân request không hợp lệ trước đợt Jev mới; hai lượt chấm độc lập
và đối soát bất đồng theo [hướng dẫn chấm](reviewer-guide.md); holdout độc lập trước tuyên bố
chất lượng trên văn bản mới. Những việc này vẫn mở trong [tasks.md](tasks.md).

## Antigravity

Giữ model Gemini 3.8 Flash. Metadata `/usage` không inference xác nhận nhóm Gemini còn khoảng
88% quota tuần và 98% quota 5 giờ. Docker daemon 29.8.2 phản hồi kiểm tra read-only, nhưng
chưa dựng container, cài CLI hoặc đăng nhập môi trường riêng.

Automatic approval review vẫn chặn chạy tiếp host CLI vì trial trước gọi lệnh/đọc file ngoài
phạm vi và chưa xác minh cách ly dữ liệu. Chưa có thêm Gemini inference. Cần owner duyệt
[phương án cách ly](isolation-gate.md) và đăng nhập riêng trước khi kiểm acceptance rồi chạy.


## Lưu trữ phục vụ phân tích

Đã chụp raw data, mã nguồn và các bảng CSV/JSONL có khóa ghép cặp để dựng chart về sau.
Có archive local, data dictionary và checksum; xem [hồ sơ lưu trữ](data-archive.md).
Giữ nguyên các giá trị thiếu và giới hạn bằng chứng, chưa suy ra chất lượng từ số đầu ra.
