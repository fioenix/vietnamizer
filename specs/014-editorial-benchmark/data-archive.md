# Lưu trữ dữ liệu pilot để phân tích và dựng chart

## Snapshot phục hồi đã chốt

Đợt mới giữ đủ 20 bản Codex + Jev và 80 bản cuối trong bộ so sánh. Có raw JSON body của
402 request/response HTTP mới, kể cả sáu response tự mâu thuẫn; giữ cả reply gốc, repair
và nguồn từng câu trong composite. Các đợt gốc/v1/v2 và snapshot trước vẫn giữ nguyên.

- [Gói dữ liệu mới](../../artifacts/014-research-archive-20261025T082946Z.tar.gz), 15.078.132 byte.
- [Data dictionary](../../artifacts/014-research-archive-20261025T082946Z/DATA_DICTIONARY.md) và [bảng phân tích](../../artifacts/014-research-archive-20261025T082946Z/tables/).
- [Danh mục file](../../artifacts/014-research-archive-20261025T082946Z/file-inventory.json) và [checksum archive](../../artifacts/014-research-archive-20261025T082946Z.tar.gz.sha256).
- SHA-256: `da74e94fa40a773d11987e316791065f779d0259a484aa0ccd5b238f95a2fe05`.

Đã đối soát 3.556 payload file theo digest, tính lại độc lập checksum của tar.gz và đọc
các bảng ngay từ archive để kiểm số dòng. Gói lưu cả mã exporter, snapshot working tree
chưa commit, manifest/receipt, raw, pass seals, bảng xác suất và log 50 test liên quan.
Chỉ mục này, dấu hoàn tất task và ghi nhận review cuối được bổ sung sau snapshot; không
chỉnh bytes của archive.
Đây vẫn là lưu trữ local, chưa phải backup ngoài máy hoặc gói bằng chứng công khai.

| Bảng hiện tại | Số dòng | Vai trò |
|---|---:|---|
| cases.csv | 20 | Đơn vị lấy mẫu và ghép cặp |
| attempts.csv | 131 | Mọi lần thử generation, kể cả một Gemini bị cách ly |
| planned_cells.csv | 180 | Ô kế hoạch qua các đợt, gồm 49 ô Gemini chưa thử |
| comparison_cells.csv | 80 | Bộ so sánh hiện tại, đủ 20 bản mỗi chế độ |
| jev_requests.csv | 435 | Request mạng thực; kế thừa chỉ tính một lần |
| jev_evaluations.csv | 20 | Lượt cuối mỗi văn bản, tách đủ phản hồi và đủ ngữ cảnh |
| jev_judgments.jsonl | 15.449 | Câu trả lời hợp lệ và phân bố xác suất |
| jev_composites.jsonl | 6 | Nguồn từng câu trả lời trong bằng chứng ghép |
| human_reviews.csv | 160 | Nhãn phân tích chưa chấm, không đổi thành 0 |
| reviewer-a-blinded.csv, reviewer-b-blinded.csv | 80 mỗi file | Phiếu chấm riêng, không chứa khóa chế độ |

Các pass và lượt tái sử dụng có bảng riêng; không tính chúng thành request mới hoặc mẫu
độc lập. `historical-v2-tables/` giữ nguyên góc nhìn partial/fallback trước đây. Nếu judgment
trỏ tới composite, dùng `answer_sources[check]` để tìm response mạng thực; không lấy câu lỗi
trong reply gốc thay cho câu đã phục hồi. Gói dữ liệu giữ trạng thái thiếu ngữ cảnh native:
chỉ 3/20 văn bản đầy đủ ngữ cảnh dù cả 20 đều nhận đủ phản hồi.

Tổng Jev từ usage là 0,192088554 USD; cộng ba khoản dự phòng hóa đơn là 0,200346090 USD.
Đơn vị lấy mẫu vẫn là 20 văn bản giả lập. Chưa có nhãn người chấm, holdout hay ước lượng
hiệu quả chất lượng. Ba raw reply lỗi lịch sử không thể phục hồi; nguyên nhân vẫn chưa rõ.
Các đối chứng được dùng lại qua các đợt và backend Codex/Gemini chưa được xác nhận. Những
giới hạn này phải đi cùng chart. Xem [báo cáo phục hồi](recovery-results.md).

## Snapshot lịch sử trước phục hồi

Đã tạo snapshot local ngày 25/10/2026, không gọi lại model. Dữ liệu gốc và bảng dẫn xuất
được giữ riêng; chưa công bố raw data hay sao lưu sang thiết bị/dịch vụ khác.

- [Gói tar.gz](../../artifacts/014-research-archive-20261025T065920Z.tar.gz), 5.523.099 byte.
- [Snapshot và bảng dữ liệu](../../artifacts/014-research-archive-20261025T065920Z/DATA_DICTIONARY.md).
- [Danh mục file và digest](../../artifacts/014-research-archive-20261025T065920Z/file-inventory.json).
- [Checksum của archive](../../artifacts/014-research-archive-20261025T065920Z.tar.gz.sha256).
- SHA-256 tar.gz: `a8fd94b93145df231a4da266404293bcb6de90592c28258f0ce29c303bf9022b`.

## Nội dung đã giữ

Raw của ba đợt gốc/v1/v2 được chụp nguyên file: nguồn, bản nháp, prompt, response/stdout/stderr,
manifest, metadata runtime, ledger, lỗi, coverage, judgments, bộ chấm và khóa chế độ. Có bản
chụp mã và tài liệu trong working tree, kể cả phần chưa commit, cùng source v1 hiện có.
HEAD chỉ là mốc tham chiếu; không đồng nhất HEAD với toàn bộ snapshot.

Các bảng CSV/JSONL được xuất ở tables/, UTF-8, giữ text và cấu trúc gốc khi cần:

| Bảng | Số dòng | Đơn vị |
|---|---:|---|
| cases.csv | 20 | Văn bản giả lập |
| attempts.csv | 111 | Lần thử generation; 110 hoàn tất và một bị cách ly |
| planned_cells.csv | 160 | Ô generation dự định; giữ cả 49 ô chưa thử |
| comparison_cells.csv | 80 | Bản cuối trong bộ chấm bốn chế độ |
| jev_evaluations.csv | 20 | Trạng thái Jev theo văn bản, gồm cả chưa gọi |
| jev_requests.csv | 33 | Request thực, loại đếm trùng bằng chứng kế thừa v1/v2 |
| jev_judgments.jsonl | 1.145 | Check hợp lệ, giữ nguyên answer/distribution |
| human_reviews.csv | 160 | Hai người chấm × 80 bản; toàn bộ chưa có nhãn |

Giữ case_id để ghép cặp, epoch/attempt_id để phân biệt lần chạy, review_id để nối nhãn và
request_digest để truy tới question/criteria và raw reply. Có data dictionary về đơn vị thời
gian/token/tiền, giá trị thiếu và quy tắc đếm. Không đổi thiếu dữ liệu thành 0; không cộng
bản sao v1/v2 như request độc lập; không xem fallback là treatment Jev.

Đã đọc lại archive và đối chiếu đủ **937 payload file** bằng SHA-256; đọc lại các CSV để kiểm
số dòng. SHA-256 của chính archive cũng được tính lại độc lập và khớp sidecar. Snapshot
không ghi đè raw runs. Gói này nằm trong artifacts/ bị gitignore; đây là lưu trữ local,
chưa phải backup ngoài máy hoặc evidence bundle đã phát hành.

## Giới hạn khi phân tích

Đơn vị lấy mẫu là 20 văn bản, không phải 80 đầu ra hay 1.145 judgments độc lập. Chỉ cặp tự rà/
có Jev được kiểm soát số lượt sửa từ chung bản nháp; hai baseline cũ được tái sử dụng.
Chưa có nhãn người chấm, không có ước lượng hiệu quả chất lượng. Chỉ hai mẫu nhận tư vấn Jev
một phần, không mẫu nào hoàn tất phạm vi; phải giữ bảng tổng và phân tầng mức nhận tư vấn.

Ba raw reply lỗi chưa được lưu tại thời điểm chạy nên không có trong archive; nguyên nhân
vẫn chưa xác định. Backend model thực của Codex/Gemini chưa được xác nhận. Không bảo đảm có
bytes của mọi revision driver lịch sử; các digest, prompt đóng băng và source v1 hiện có đã
được giữ. Các giới hạn này phải đi cùng chart, không được che bằng cách bỏ dòng thiếu/lỗi.

Các nhận xét và quyết định sau snapshot tiếp tục ghi trong specs; snapshot này giữ nguyên.
Khi có nhãn hoặc đợt chạy mới, tạo version archive mới, giữ cả bản chấm gốc và adjudication.


## Quality-assessment successor — 2026-10-25T09:35:28Z

Local archive: `artifacts/014-quality-research-archive-20261025T093528Z.tar.gz`.
SHA-256: `5ff8694ba76568da63f07da187b66b969bafb6d64877777f52cf5431abe50c6f`.
Size 17,583,400 bytes; 513 payloads checked against hashes during packaging and tar readback.
The nested operational archive retains its previous 3556 payload snapshot and verified
SHA-256 `da74e94fa40a773d11987e316791065f779d0259a484aa0ccd5b238f95a2fe05`.

Canonical quality epoch is `014-quality-assessment-20261025-v3`: 42 unique starts, 2 source-only
inventories, 39 valid output groups, 1 failed group, 156/160 valid output reviews and 0 actual human
submissions. Earlier snapshots duplicate inherited raw; do not add them to canonical counts.
UI fixtures are explicitly synthetic and rejected by human ingestion. Forms are prepared
local generator code, not verified cloud forms. Coordinator archive contains private keys
and model grades; send only the respective reviewer ZIP to each human reviewer.

Five figures are preserved as SVG/PDF and PNG 300 DPI with render manifests; CSV, summary,
all raw prompt/schema/requested-model/usage/error/label files, source snapshots and targeted
test logs are included. Full raw replay currently binds absolute paths; archived chart
summaries can regenerate figures without inference. This index was updated after archival
and therefore is newer than its source snapshot inside that archive. Independent read-only review also verified all 513 tar payloads, canonical counts,
reviewer ZIP separation, QA exclusion, nested archive hash and tar paths; no blocker.
The final verification receipt is local and newer than this archive snapshot.


## Google Forms source-only drafts — later same-day snapshot

`artifacts/014-google-forms-source-drafts-20261025.tar.gz` retains the exact uploaded code,
raw execution log, provider item IDs, edit URLs, source/order comparison and screenshots.
SHA-256: `2edd6ae59b83c606554ebe8ca85873f165319838dffb17f53326faeaaf431bb7`.
Two source-only forms were created and verified: 20 sources/42 questions per form, unpublished,
no email collection, no response-summary sharing, 0 responses. No publication/invitations;
quality-stage forms await reviewer-approved source inventories. This successor is separate
from the immutable quality archive above, whose no-cloud-execution statement was accurate
at its capture time. Raw human response exports/normalization have not yet been tested.


### Cập nhật quyền trả lời ngày 25/10/2026

Fio đã cho phép và cả hai form nguồn đã bật **ai có link có thể trả lời**, đang nhận bài.
Đã kiểm trang trả lời đúng A/B; không gửi lời mời hoặc nộp bài thử.

- Người chấm A — liên kết riêng được giữ local
- Người chấm B — liên kết riêng được giữ local

Đây là bước đọc 20 nguồn; form chấm bản sửa vẫn chờ inventory đã được từng người duyệt.
Các ghi nhận “chưa công khai” phía trên mô tả trạng thái trước lần cập nhật này.

## Human simple v2 — hai Google Forms trực tiếp, 25/10/2026

Đợt local `artifacts/014-human-simple-v2-reviewed-20261025` giữ 160 ảnh gốc/sửa,
contracts A/B, nguồn và payload Apps Script, raw log từng batch, snapshot 62 mục của
mỗi form cũ, mapping 40 nhóm/160 bản, ảnh chụp và cấu trúc UI, biên bản review,
kiểm tra và trạng thái cuối. Hai form cùng link cũ, mỗi form 20 đoạn/80 bản sửa;
đã bật nhận bài và xác minh quyền ai có link lúc 17:39:58. Khi bàn giao có 0 phản hồi thật.
Không gọi lại model/Jev và không sửa dữ liệu đánh giá model cũ.

Archive: `artifacts/014-human-simple-v2-reviewed-20261025.tar.gz` — **57.433.581 byte**,
265 payload files cùng `SHA256SUMS`. SHA-256:
`528bf0dab1a1adb4faa92c6ca3ff3aa95b0ebae256c3b141fb2edb236db561a5`.
Đã đọc lại archive và kiểm toàn bộ 265 digest. Link người chấm chỉ giữ local và gửi
riêng, không đưa vào tài liệu public. Archive nối với bộ model trước qua digest trong README.json.

Google cắt mỗi dòng audit/finish dài ở 8.192 ký tự. Giữ nguyên raw đã bị cắt, không xem
đó là lỗi chấm nội dung; các hàm kiểm tra đã hoàn tất trước khi ghi log. Mapping đầy đủ
được xuất riêng từng nhóm, snapshot cũ xuất theo chunk; trạng thái cuối có log ngắn riêng.
Không coi nhãn thiếu là đạt, không tạo chart người đọc khi chưa có phản hồi thật.
