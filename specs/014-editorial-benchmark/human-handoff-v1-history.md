# Giao bộ chấm cho hai người đọc

Hai gói riêng đã được chuẩn bị trong đợt `014-quality-assessment-20261025-v3`:
`human-handoff/reviewer-A.zip` và `human-handoff/reviewer-B.zip`. Mỗi người chỉ nhận đúng
một gói. Không gửi thư mục `private/`, kết quả model hoặc bản điều phối chung.

## Cách dùng

1. Giải nén toàn bộ ZIP, giữ nguyên thư mục `design/` bên cạnh `review.html`.
2. Mở `review.html` bằng Chrome mới. Không cần cài đặt, tài khoản hoặc máy chủ.
3. Điền kinh nghiệm và quan hệ với dự án. Đọc đủ 20 nguồn, ghi lỗi cần sửa bằng trích đoạn
   nguyên văn; nguồn tốt có thể không có lỗi. Xác nhận đã rà từng nguồn.
4. Xuất bản nháp JSON, rồi bấm khóa nguồn và xác nhận lần nữa. Từ đây các bản A–D mới hiện.
5. Chấm đủ 20 nhóm/bốn bản. Mỗi phiên năm nhóm; có thể nghỉ giữa chừng. Không xem nhãn
   người kia, điểm model hoặc tên chế độ; không dùng AI chấm hộ.
6. Xuất bản nháp JSON sau mỗi phiên. Khi chuyển máy, mở đúng gói rồi nhập JSON để tiếp tục.
7. Xuất bản cuối và gửi file `reviewer-A-final.json` hoặc `reviewer-B-final.json` cho Fio.
   Không gửi ảnh chụp thay cho file nhãn. App chỉ cho xuất bản cuối khi đủ các trường.

Tự lưu nằm trên trình duyệt/máy hiện tại. File JSON là bản sao cần giữ. Nếu trình duyệt
không cho lưu hoặc không hỗ trợ dấu kiểm tra SHA-256, app báo lỗi; không coi nhãn đã khóa
hoặc đã sao lưu khi chưa thấy xác nhận. Dấu kiểm tra phát hiện thay đổi ngoài ý muốn,
không chứng minh danh tính hoặc ngăn một người cố ý mở dữ liệu trong mã nguồn.

## Lịch và đối soát

Mỗi người chấm toàn bộ 80 bản; không chia mỗi người 40 bản. Dự trù ban đầu 5–7 giờ/người và
1–2 giờ đối soát, cần hiệu chỉnh sau phần tập chấm. Dùng một ví dụ tập chấm ngoài bộ 20 nguồn;
không thảo luận đáp án của bộ chính. Lưu riêng kinh nghiệm, thời gian thực tế và xung đột lợi ích.

Fio nhận và khóa cả hai file trước khi mở key. Kiểm tra nhãn bằng:

```bash
python3 -m benchmarks.quality_human ingest \
  --output artifacts/014-quality-assessment-20261025-v3 \
  --submission /absolute/path/to/reviewer-A-final.json
```

Giữ nguyên file gốc theo digest; không sửa đè nhãn A/B. Đo agreement trước đối soát. Lập
bảng bất đồng theo nguồn, trích đoạn và tiêu chí; ưu tiên một người thứ ba khi vẫn ẩn chế độ.
Nếu chỉ có A/B, ghi lý do thống nhất và giữ unresolved ở chỗ chưa thống nhất. Không ép đạt
một ngưỡng kappa hoặc sửa rubric sau khi thấy bên nào thắng.

## Phương án Google Forms

Bộ sinh form dành riêng cho người điều phối nằm trong `forms-coordinator/Code.gs`, kèm
`appsscript.json` và manifest. Bản source ở `benchmarks/reviewer_forms.gs`; tạo lại bằng:

```bash
python3 -m benchmarks.quality_forms --output artifacts/014-quality-assessment-20261025-v3
```

Ngày 25/10/2026 đã chạy `createSourceDrafts` trên Apps Script và tạo hai form chỉ đọc
nguồn, ở trạng thái **chưa công khai**. Đã đối chiếu đủ 20 nguồn và 42 câu hỏi mỗi form;
không thu email, không hiện tổng hợp câu trả lời, hiện có 0 phản hồi.

- Form A — link chỉnh sửa của người điều phối — liên kết riêng được giữ local
- Form B — link chỉnh sửa của người điều phối — liên kết riêng được giữ local

Đây chưa phải link gửi người chấm; chưa công khai hoặc gửi lời mời. Fio chuẩn hóa câu trả lời thành
inventory có trích đoạn/ID rồi để đúng người chấm xác nhận, giữ raw export và thời điểm khóa.
Điền inventory đã duyệt vào `LOCKED_INVENTORIES`; `createQualityDrafts` mới tạo bốn phiên
cho mỗi người. Mỗi phiên gồm năm nguồn/bốn bản, chọn nhãn bằng bảng và ghi bằng chứng.

Script không gửi lời mời hoặc tự công khai. Google yêu cầu scope truy cập Forms; chỉ cấp
sau khi Fio rà đúng code/quyền. Không bật công khai tổng hợp câu trả lời. Chỉ gửi form của
đúng người chấm khi đã sẵn sàng. API tạo form nguồn đã chạy thành công. Tạo form chấm bản sửa, xuất phản hồi thật và
chuyển về hợp đồng JSON chưa được nghiệm thu; bộ HTML là bộ giao nhận đã kiểm thử tại máy. Nếu chọn Forms, lưu
raw CSV/response JSON cùng item-map, inventory và bằng chứng duyệt; kiểm tra đủ nhãn trước
khi đưa vào phân tích. Không coi bản sinh form là lượt người chấm đã hoàn tất.

## Kiểm chứng và giới hạn

Đã kiểm giao diện trên localhost: lưu rồi tải lại; rà và khóa 20 nguồn; chọn nhãn một nhóm;
xuất JSON; nhập fixture giả lập đủ 20 nhóm; xuất bản cuối và kiểm bằng validator phía điều phối.
Fixture được đánh dấu QA, giữ ngoài nhãn nghiên cứu và bị chặn khi ingest. Chưa có người
chấm thật gửi bài, chưa nghiệm thu thời gian 5–7 giờ hoặc mọi trình duyệt/file origin.

Xem [protocol](quality-protocol.md) để biết mẫu số, CI theo nguồn, nhãn uncertain/missing
và điều kiện đưa chart vào README. Điểm model và điểm người đọc luôn báo riêng.


### Cập nhật quyền trả lời ngày 25/10/2026

Fio đã cho phép và cả hai form nguồn đã bật **ai có link có thể trả lời**, đang nhận bài.
Đã kiểm trang trả lời đúng A/B; không gửi lời mời hoặc nộp bài thử.


Đây là bước đọc 20 nguồn; form chấm bản sửa vẫn chờ inventory đã được từng người duyệt.
Các ghi nhận “chưa công khai” phía trên mô tả trạng thái trước lần cập nhật này.
