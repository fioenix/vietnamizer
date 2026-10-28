# Bộ chấm đơn giản — human-simple-v2

Fio yêu cầu ngày 25/10/2026: xem bản gốc cạnh bản sửa, ba câu dễ hiểu, ẩn bốn chế độ;
bỏ bước đọc riêng và khóa lỗi của bản gốc. Đây là thay đổi được owner duyệt, thay quy trình
chấm người cũ; không sửa lại kết quả model hoặc coi hai schema là tương đương.

Mỗi người chấm đủ 20 đoạn, mỗi đoạn bốn bản A–D, tổng 80 bản. Giữ packet và mã hóa đã đóng băng
riêng A/B. Mỗi cặp được hiển thị bằng ảnh hai cột trung tính: trái là bản gốc, phải là bản sửa.
Google Forms chỉ có một cột; ảnh cung cấp cách xem cạnh nhau. Giữ nguyên nội dung, không tô
màu sửa đúng/sai hoặc hiện tên chế độ. Không lấy ảnh từ dịch vụ ngoài; PNG tạo local, gửi
trực tiếp vào form qua Apps Script đã được cấp quyền Forms. Không thêm Drive scope.

Mỗi đoạn chỉ hỏi:

1. **Bản sửa có giữ đúng ý, số liệu và giọng người viết không?** Chọn riêng A/B/C/D:
   Giữ đúng / Có chỗ bị đổi / Chưa rõ.
2. **Bản sửa đọc thế nào so với bản gốc?** Chọn riêng A/B/C/D:
   Tự nhiên, rõ ràng hơn / Tương đương / Khó đọc hơn / Chưa rõ.
3. **Có chỗ nào sửa sai, sửa thừa hoặc vẫn khó hiểu không?** Ghi A/B/C/D, trích đoạn và lý do;
   nếu không có thì ghi “Không có”. Một câu trả lời chung có thể ghi nhiều bản.

Hai câu đầu dùng bảng chọn bốn hàng, không chọn sẵn. Câu ba là nhận xét tự do bắt buộc.
Mỗi người điền kinh nghiệm và quan hệ với dự án một lần. Đọc/chấm độc lập, không xem nhãn
model hoặc trao đổi đáp án. Có thanh tiến độ; Google tự lưu theo khả năng tài khoản/trình duyệt.
Không khẳng định mọi người dùng ẩn danh đều được lưu tiến độ khi đóng trang.

Dữ liệu: form ID + schema version + packet digest + reviewer + response ID/timestamp,
provider item-ID map, raw response values và note nguyên văn. Q1 là tiêu chí gộp bảo toàn;
không tự đổi thành nhãn nghĩa/giọng riêng. Q2 là so với bản gốc, không phải xếp hạng bốn bản.
Không suy ra precision/recall hay wins/ties/losses từ ba câu này. Báo tỷ lệ từng lựa chọn,
unknown/missing, agreement trước đối soát và CI ghép cặp theo 20 văn bản khi đã đủ nhãn người.
Không gộp nhãn model vào nhãn người; chưa có nhãn thật thì không xuất chart chất lượng người.

Form cũ đang có 0 phản hồi theo UI. Trong lúc dựng lại phải tạm dừng nhận bài và kiểm lại
phản hồi ở server trước thao tác xóa câu hỏi, giữ snapshot cũ. Có phản hồi thì dừng thay
nội dung, bảo toàn dữ liệu. Ghi raw log/batch/item mapping; batch dở không tự chạy lại.
Giữ link A/B cũ, kiểm toàn bộ nội dung và quyền ai có link trước khi bật nhận bài lại.
