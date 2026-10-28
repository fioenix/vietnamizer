# Thử giữ giọng trên bài Mindfio

Ngày 27/10/2026. Đây là phần chuẩn bị đánh giá tiếp nối feature 016, không phải kết
quả benchmark mới. Mã nguồn giữ ở 0.12.0; không thay quy tắc từ bài của một cá nhân.

**Cập nhật cùng ngày:** chủ nhân đã duyệt nguyên bản mô tả giọng và giao chạy 12
đầu ra. Các mục mô tả trạng thái chuẩn bị dưới đây được giữ làm lịch sử thiết kế;
trạng thái thực thi và kết quả được ghi riêng trong `mindfio-results.md`. Hồ sơ
được duyệt lưu đúng byte kèm biên nhận; không viết đè bản nháp và archive chuẩn bị.
M01 được xác định trước lúc sinh là lời tựa văn chương có nhịp/ẩn dụ chủ ý; cả ba
prompt đều nhận ghi chú giới hạn biên tập typography để giữ thể loại.

## Hai nhánh đã giao

1. Kiểm tra lại phần tích hợp phương pháp cộng đồng trong mã nguồn hiện hành.
2. Lưu nguồn Mindfio, tách mẫu tham chiếu khỏi bài đánh giá và soạn mô tả giọng để
   chủ nhân xem trước khi dùng cho lượt biên tập có đo lường.

Không cài hoặc phát hành bản mới. Không sửa các bộ Codex/Gemini lịch sử, không truy
cập hoặc đổi hai Forms. Không dùng lại kết quả benchmark cũ để xác nhận tính năng mới.

## Nguồn và cách chia

Snapshot local: `artifacts/017-mindfio-voice-20261027/manifest.json`. RSS công khai
trả HTTP 200, có tám mục chứa `content:encoded`. Giữ XML nhận được, metadata HTTP,
HTML từng bài, bản chữ và hash. Chưa đối chiếu từng bài với trang đọc; chưa chứng
minh RSS bao trùm toàn bộ lịch sử xuất bản.

Trước khi đọc phần thân trong lượt này, cố định nhóm theo URL:

- Tham chiếu: bài nghỉ ngơi M03 và ba phần AI-First M06–M08.
- Dành để đánh giá: lời tựa M01, bài buông/giữ M02, quẻ bói M04, tập trung M05.

M03 đã từng được đọc trong lần kiểm tra truy cập, nên không xếp vào nhóm đánh giá.
Ba phần AI-First cùng nhóm tham chiếu; chúng thuộc một chuỗi, không phải ba bằng
chứng độc lập. Người rút hồ sơ chỉ được đọc bốn bài tham chiếu. Việc chia này là
chọn có chủ đích để chuẩn bị một pilot nhỏ, không phải lấy mẫu ngẫu nhiên hay holdout
đại diện cho người viết tiếng Việt.

Theo xác nhận của chủ nhân, tất cả bài đã được AI biên tập. Không có bản trước khi
AI tham gia hoặc log sinh bài. Vì vậy chỉ gọi đây là phong cách Mindfio đã được
chọn đăng; không khẳng định tái dựng giọng viết không có AI.

## Mô tả giọng

`profile-draft.md` là bản nháp riêng trong artifact local, chưa được chủ nhân xác
nhận. Mỗi đặc tính có trích đoạn ngắn và phạm vi, không chứa tiểu sử hoặc suy đoán
tính cách. `profile-observations.json` giữ vị trí ký tự để kiểm tra nguồn.

Không đưa nội dung hay sở thích này vào gói Vietnamizer, calibration log, memory
hoặc quy tắc dùng chung. Không dùng bài dành đánh giá để sửa mô tả trước lượt thử.
Nếu chủ nhân chỉnh hồ sơ, lưu revision mới và đóng băng revision đó trước khi chạy.

## Lượt thử sau khi hồ sơ được xem lại

Mỗi bài có bản trước là nguyên văn đã đăng. Trên cùng một model/agent, cùng mức
reasoning và cùng nguyên bản, tạo từng bản cuối trong phiên tách biệt:

| Nhánh | Dữ liệu được nhận | Mục đích |
| --- | --- | --- |
| Prompt biên tập thường | Bản gốc và cùng hồ sơ đã xác nhận | Đối chứng cho việc chỉ thêm chỉ dẫn biên tập |
| Vietnamizer core | Bản gốc, source 0.12.0; không có hồ sơ | Quan sát việc biên tập khi giữ giọng từ bản gốc |
| Vietnamizer kèm hồ sơ | Bản gốc, cùng source 0.12.0 và hồ sơ đã xác nhận | Kiểm tra đóng góp của mẫu giọng |

Bốn bài × ba nhánh = 12 đầu ra dự kiến; đây chưa phải lượt chạy được hoàn thành.
Core không có hồ sơ là phép loại bỏ thành phần, còn nhánh prompt thường nhận cùng
hồ sơ giúp phân biệt lợi ích của skill với lợi ích đơn thuần của việc có mẫu.
Không dùng model/agent khác làm đối thủ. Không đưa đầu ra nhánh trước vào nhánh sau.
Không thêm Jev hoặc chi phí API từ trần benchmark lịch sử vào pilot này.

Trước khi chạy: đối chiếu nội dung RSS với trang công khai, đóng băng input/prompt,
source, profile, thứ tự chạy và cấu hình runtime. Ghi riêng sai khác HTML/bản chữ;
giữ trích dẫn, code và URL. Có thể giữ nguyên toàn bộ bài nếu không có lỗi cần sửa.

Lưu raw stdin/stdout/stderr, yêu cầu/cấu hình khả dụng, lỗi và retry, thời gian,
usage, ID phiên và model quan sát được; phân biệt raw CLI với raw HTTP. Không nhận
kết quả chỉ vì process exit 0. Không tuyên bố model backend nếu runtime không chứng thực.

## Đánh giá và cách kết luận

Đối chiếu trước/sau từng bài: thay đổi có sửa lỗi cụ thể không, có mất ý/dữ kiện/
mức chắc chắn không, cách đọc có tốt hơn không, và những nét đã xác nhận có được
giữ không. Mỗi nhận xét trỏ vào đoạn thay đổi. Chủ nhân quyết định mức phù hợp giọng;
chấm của model chỉ là thăm dò, phải tách khỏi nhận xét chủ nhân và tự rà của agent.

Với bốn bài liên quan của một publication, báo số bài và các ca cụ thể; không đặt
ngưỡng phần trăm khớp giọng, không suy độ thay ký tự thành chất lượng, không tạo
p-value hoặc biểu đồ khẳng định cải thiện khi chưa có nhãn. Không tự tạo Forms mới.

## Trạng thái đã xác minh

- Tám bản nguồn đã lưu; bốn tham chiếu, bốn dành đánh giá.
- Mã nguồn 0.12.0: sáu test package consumer, validator và registry check đạt ở lượt
  kiểm tra ngày 27/10; raw bằng chứng nằm trong `source-verification/`.
- VG01–VG08 mới là ca kỳ vọng được rà tĩnh, chưa là tám lượt model đạt.
- Chưa có nhãn chủ nhân, bản biên tập hoặc kết luận hiệu quả giữ giọng từ pilot này.

Workflow: đã đọc đúng coding-workflow qua Obsidian CLI; mốc review-by 21/10 đã qua.
Tiếp tục feature 016 đã có spec/plan/tasks hoàn tất; đợt này xác minh lại và chuẩn
bị dữ liệu nghiên cứu local, không thay hợp đồng sản phẩm hoặc thêm runner phát hành.
Đã đọc TypeSafe citation-check cookbook để tách kiểm trích đoạn tất định khỏi
phán đoán ngữ nghĩa. Không gọi Jev; không coi kiểm substring là xác nhận ngữ nghĩa.
