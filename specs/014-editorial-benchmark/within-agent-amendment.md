# Trước và sau khi dùng Vietnamizer trên cùng agent

Fio chốt lại mục tiêu ngày 26/10/2026: đánh giá bản biên tập so với bản AI gốc khi dùng
Vietnamizer trên một cấu hình agent/model cố định. Các bộ Codex và Gemini là hai lần
thực hiện riêng của cùng thiết kế, không phải cuộc thi giữa các agent.

## Đơn vị và kết quả cần đọc

“Trước” là toàn bộ câu trả lời AI công khai đã đóng băng. “Sau” là một trong bốn bản
biên tập từ chính nguồn đó: yêu cầu cơ bản, prompt thường, Vietnamizer, Vietnamizer +
Jev. Nhánh yêu cầu cơ bản vẫn là bản đã biên tập; không dùng nó thay cho nguyên bản.
Không tạo lại nguồn hoặc đầu ra để phục vụ cách phân tích mới.

Kết quả chính là nhận xét trước/sau của người đọc: tự nhiên, rõ ràng hơn; tương đương;
khó đọc hơn. Báo riêng giữ đúng ý, số liệu và giọng; có chỗ bị đổi. Giữ phần chưa rõ
và thiếu. Không chuyển các câu hỏi này thành điểm số trước/sau giả định, precision,
recall hoặc khả năng phát hiện tác giả AI.

`before-after.csv` có năm tỷ lệ xác định cho mỗi chế độ: better, equivalent, worse,
preserved, changed; theo A, B và trung bình hai người cố định. Mỗi chiều loại riêng
nhãn thiếu/chưa rõ khỏi ước lượng, nhưng bảng số đếm luôn giữ chúng trên tổng 20 nguồn.
Bản gộp chỉ dùng nguồn có nhãn xác định ở cả hai người cho cùng chế độ/chiều; không
bắt cả bốn chế độ phải đầy đủ mới báo được một chế độ. Một nguồn có hai người được
lấy trung bình trong nguồn, không coi là hai mẫu độc lập.

CI 95% dùng10.000 lượt bootstrap nguồn, seed 25033. Không dựng CI nếu dưới hai nguồn
đủ nhãn; CI suy biến vẫn phải mang cảnh báo. Hai người cố định không đại diện cho
quần thể người đọc;20 nguồn cùng một nhà phát hành không đại diện cho mọi văn bản AI.

So sánh giữa chế độ là phân tích bổ sung trong cùng agent, trên các cặp đủ nhãn:
Vietnamizer–prompt thường, Vietnamizer–yêu cầu cơ bản, Vietnamizer+Jev–Vietnamizer.
Cải thiện so với gốc có thể đến từ việc agent được yêu cầu biên tập; chỉ xem trước/sau
chưa đủ quy phần cải thiện riêng cho skill. Đối chứng bổ sung giúp kiểm tra điều này.
Không dùng kiểm định xác nhận hoặc chọn subset Jev thuận lợi sau khi xem kết quả.

## Dữ liệu và ranh giới

- Codex:80 bản hợp lệ, bốn chế độ ×20 nguồn; hai Forms A/B đang giao chấm bộ này.
- Gemini:80 bản hợp lệ đã đối soát raw, CLI ghi nhận gemini-3.8-flash-medium;
  80 hội thoại riêng, finish-only, chưa có nhãn người. Không suy nhãn Codex sang Gemini.
- Không gộp nhãn, tính chênh lệch hay vẽ bảng xếp hạng Codex–Gemini. Khi có đánh giá
  riêng cho Gemini, báo trước/sau trong bộ đó, với ranh giới runtime riêng.
- Giữ raw, manifest, hai lượt host cũ, bộ Codex và mọi ảnh/item/khóa ghép Forms.
  Không gọi thêm model/Jev hoặc sửa Forms trong lần thay đổi này.

Đây là sửa mục tiêu phân tích sau khi đã tạo đầu ra. Không có nhãn người được chọn nào
được đọc để chọn chỉ số trong lần sửa này; không kiểm đếm lại phiếu live. Không gọi
phương pháp mới là đăng ký trước khi sinh dữ liệu. Phương pháp cũ từng ưu tiên
Vietnamizer–prompt thường; workspace-v2 và archive cũ vẫn giữ để tái lập.

Workspace-v5 được prepare offline với code/protocol mới và cùng form/item/ảnh/khóa
ghép. Hai exporter mới chỉ đọc Forms; không thực thi cloud trong lần sửa này. Không
lặng lẽ sửa manifest/hash của workspace-v2. Bản phân tích mới cần dùng log xuất có
binding v5 và selection ID được Fio xác nhận.

Workspace-v3 và workspace-v4 là các bản prepare trước khi review hoàn tất, giữ riêng
để đối soát và không dùng cho phân tích hiện hành. Review sửa chú thích mẫu số và
cảnh báo CI suy biến trên cả hình trước/sau lẫn hình chênh lệch bổ sung.
Workspace-v5 pin phiên bản sau sửa. Không nhập nhãn thật hoặc chạy exporter cloud.
