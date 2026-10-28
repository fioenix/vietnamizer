# Pilot Vietnamizer ngày 25/10/2026

**Chưa đạt mục tiêu 120 đầu ra.** Hiện có 70 bản biên tập để xem và chấm:
60 bản từ Codex, 10 bản từ Gemini 3.8 Flash. Một trial Gemini bị cách ly;
49 trial còn lại chưa chạy. Chưa có kết luận về chất lượng biên tập.

| Runtime | Không skill | Prompt thường | Vietnamizer | Tổng bản biên tập | Trial bị cách ly |
|---|---:|---:|---:|---:|---:|
| Codex, yêu cầu `gpt-6.1-sol`, medium | 20 | 20 | 20 | 60 | 0 |
| Antigravity qua Agybird, yêu cầu `gemini-3.8-flash-medium` | 3 | 4 | 3 | 10 | 1 |

Tập pilot gồm 20 văn bản giả lập, mỗi văn bản 156–194 tiếng, phủ bảy nhóm phong cách
và cổng typography-only. Tất cả đều là dữ liệu phát triển; nhãn kỳ vọng do agent soạn,
chưa được hai người đọc tiếng Việt chấm độc lập. Không dùng chúng làm tập holdout.

## Vì sao phần Gemini dừng

Trong ô `agy/P04/bare`, Antigravity đã gọi command và đọc file, rồi xin chạy `git status`,
trái với yêu cầu chỉ xử lý văn bản trong prompt. Chính sách Antigravity từ chối lệnh đó.
Không có bản biên tập cuối hợp lệ cho ô này. Envelope chỉ ghi tên tool, chưa cho biết
đầy đủ đường dẫn và nội dung của các lần đọc trước đó; chưa xác định có dữ liệu riêng
nào bị đọc hoặc gửi đi.

Automatic approval review sau đó từ chối chạy các trial Gemini còn lại vì chưa có cách ly
được xác minh, có nguy cơ gửi dữ liệu riêng từ repo sang dịch vụ ngoài phạm vi đã cho phép.
Lệnh bị từ chối không được thực hiện. Không cấp quyền bổ sung hoặc đổi settings để đi tiếp.
[Phương án cách ly cần phê duyệt](isolation-gate.md) mô tả môi trường Docker riêng và các cổng
kiểm chứng trước khi gọi model. Chưa tạo môi trường đó.

## Số liệu vận hành đã ghi nhận

| Runtime | Trung vị thời gian mỗi trial | Input tokens do CLI báo | Output tokens do CLI báo |
|---|---:|---:|---:|
| Codex, 60 trial | 10.713 giây | 2,112,812 | 18,942 |
| Antigravity, 11 trial, gồm ô bị cách ly | 58.665 giây | 204,372 | 86,674 |

Đây là usage theo từng CLI, chưa quy đổi thành chi phí và chưa chuẩn hóa cách tính token giữa
hai nhà cung cấp. Output tokens của Antigravity có phần thinking; không dùng bảng này để kết
luận model nào rẻ hơn. Các lượt chạy dùng route thuê bao hiện có; không mua credit, bật overage
hoặc dùng API key. CLI không trả chi phí tiền tệ cho từng trial, nên chi phí đó được ghi là chưa rõ.

Snapshot Codex trước lượt chạy chính báo dùng 37% quota tuần; snapshot sau các lô báo dùng 41%.
Đây là quota dùng chung của tài khoản, không thể quy phần chênh lệch hoàn toàn cho pilot.
Lệnh `/usage` chính thức của Antigravity báo khoảng 88% quota Gemini tuần và 98% cửa sổ 5 giờ
còn lại tại thời điểm kiểm. Lệnh này dùng 0 token. Không chạy Claude.

## Bằng chứng và bộ chấm

Toàn bộ dữ liệu chạy giữ local trong `artifacts/014-editorial-pilot-20261025/`, bị gitignore:

- `manifest.json`, `frozen-corpus.json` và `prompts/`: phiên bản, nguồn và bộ hướng dẫn đã khóa.
- `attempts/`: raw stdout/stderr, kết quả, usage, thời gian, digest và kiểm tra route/credit.
- `report.json`: đối soát 120 ô, gồm ô hoàn tất, ô bị cách ly và ô chưa chạy.
- `outputs/`: 70 bản biên tập riêng, xếp theo runtime, văn bản và chế độ.
- `blinded-review.md`, `blinded-review.json`: bộ chấm mù cho 70 bản, chưa có điểm.
- `review-key.json`: khóa đối chiếu, tách khỏi bộ chấm.

Hai record đầu tiên vẫn giữ cách phân loại bảo thủ ban đầu. Report có receipt chuẩn hóa lại:
cảnh báo startup của Codex và marker `finish` của schema Antigravity không phải thao tác tool
ngoài phạm vi. Việc chuẩn hóa chỉ áp dụng khi exit code bằng 0, lượt kết thúc hợp lệ và text
không đổi. Không gọi lại model để lấy một bản biên tập khác.

## Phạm vi đã kiểm và còn thiếu

16 test riêng của runner đã pass; kiểm tra package 0.11.0 với 55 pattern và `git diff --check`
đều pass. Không chạy full suite. Review code đã xử lý các blocker về cleanup cả cây tiến trình,
kiểm route/credit trước mỗi lượt và tránh nâng lượt lỗi thành hoàn tất khi chuẩn hóa.

Các bản biên tập hiện có chỉ xác nhận model đã trả kết quả theo giao diện. Việc giữ nghĩa, giữ
giọng, sửa đúng và sửa quá tay vẫn chờ chấm độc lập. Mỗi ô chỉ có một lần sinh; bộ hướng dẫn
Vietnamizer được cung cấp trong prompt, gồm profile/card do host chọn. Pilot chưa đo cơ chế
tự phát hiện skill hoặc tự chọn profile. Backend model và toàn bộ system context không được
metadata CLI xác nhận độc lập. Kết quả không chứng minh parity giữa hai runtime.

Không có phát hành, push, merge hoặc gửi dữ liệu chạy lên repo public.


## Đợt Codex + Jev tiếp theo

Đợt mở rộng đã tạo 40 bản Codex mới, xuất bộ chấm 80 bản cuối và giữ nguyên bằng chứng pilot
ba chế độ ở trên. Jev chỉ cung cấp tư vấn một phần cho hai văn bản; chưa có lượt nào hoàn tất
coverage. Xem [báo cáo Codex + Jev](codex-jev-results.md); không dùng tổng đầu ra để suy ra
số văn bản đã nhận tư vấn hoặc kết luận hiệu quả Jev.
