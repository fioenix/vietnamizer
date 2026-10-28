# Giao bộ chấm cho hai người đọc

Theo yêu cầu của Fio ngày 25/10/2026, bộ hiện hành dùng cách chấm trực tiếp
`human-simple-v2`: xem bản gốc cạnh bản sửa rồi trả lời ba câu cho mỗi đoạn.
Không còn lượt “chỉ đọc nguồn”, liệt kê lỗi hay khóa nhận xét trước.


Fio gửi riêng link A hoặc B cho đúng người chấm. Link thực tế được giữ trong bản ghi local
`artifacts/014-human-simple-v2-reviewed-20261025/cloud-acceptance.json`, không công khai
trong tài liệu repo để tránh phản hồi ngoài bộ chấm.

## Cách chấm

Mỗi người chấm đủ 20 đoạn, mỗi đoạn có bốn bản sửa A–D (80 bản/người).
Trong mỗi ảnh, bản gốc ở bên trái và bản sửa ở bên phải. Chữ A–D chỉ là ký hiệu;
thứ tự đã được xáo riêng cho từng người và từng đoạn, không cho biết chế độ biên tập.

1. **Bản sửa có giữ đúng ý, số liệu và giọng người viết không?** Chọn riêng cho A–D:
   Giữ đúng / Có chỗ bị đổi / Chưa rõ.
2. **Bản sửa đọc thế nào so với bản gốc?** Chọn riêng cho A–D:
   Tự nhiên, rõ ràng hơn / Tương đương / Khó đọc hơn / Chưa rõ.
3. **Có chỗ nào sửa sai, sửa thừa hoặc vẫn khó hiểu không?** Ghi bản A/B/C/D,
   trích đoạn và lý do. Nếu không có thì ghi “Không có”.

Điền kinh nghiệm và quan hệ với dự án ở đầu form. Chấm độc lập, không dùng AI chấm hộ
hoặc trao đổi đáp án với người kia. Không cần sửa lại văn bản. Bản gốc vốn tự nhiên có
thể không cần thay đổi; hai bản giống nhau có thể được chấm “Giữ đúng” và “Tương đương”.

## Giữ bằng chứng

Chưa có phản hồi người chấm thật. Giữ raw response, item ID, thứ tự A–D và bản chụp nội dung
form theo từng đợt. Khóa cả hai bản chấm trước khi mở khóa ghép chế độ. Đo mức đồng thuận
trước khi đối soát; giữ cả nhãn gốc, lý do và những chỗ chưa thống nhất.

Xem [hợp đồng chấm trực tiếp](human-simple-protocol.md). Nhãn này đo giữ đúng và độ dễ đọc;
không suy ra precision/recall của từng lần sửa hoặc thứ hạng bốn bản. Điểm model vẫn theo
[protocol riêng đã đóng băng](quality-protocol.md), không trộn với điểm người đọc.
Bộ HTML và form “chỉ đọc nguồn” trước đây là [hồ sơ lịch sử](human-handoff-v1-history.md),
không phải hướng dẫn giao người chấm hiện hành. Hai form đã được kiểm tra và bật nhận bài lại lúc 17:39:58 ngày 25/10/2026,
cùng link A/B cũ; quyền ai có link có thể trả lời. Biên bản nằm trong đợt
`014-human-simple-v2-reviewed-20261025`. Khi bàn giao có 0 phản hồi thật.
