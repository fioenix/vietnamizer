## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: validate, supporting the accepted Spec Kit 014 implementation
- Origin Date: 2026-10-26
- Verification Status: VERIFIED for the stated software/reproduction checks; human quality pending
- Version Label: public_human_readiness_v1

## Phạm vi đã kiểm chứng

21 kiểm thử có mục tiêu qua: nhập theo form/item ID, bảo toàn Unicode, phiếu trùng,
chọn phiếu rõ ràng, thiếu/chưa rõ, bootstrap ghép cặp, đồng thuận biên suy biến, CSV
an toàn và round-trip exporter giả lập có kiểm lỗi schema/ảnh. Không chạy full suite.
Reviewer độc lập đã rà mã, nguồn và thống kê, xác nhận không còn finding chặn sau sửa.

Hai exporter chỉ đọc đã chạy với Forms thật, kiểm đủ ngữ cảnh, ảnh và câu hỏi. Cả hai
bản xuất có 0 phiếu tại thời điểm đọc; log đã nhập lại và kiểm SHA-256 UTF-8 thành công.
Nhánh có phiếu thật chưa được chạy; round-trip dương hiện được chứng minh bằng fixture.
Không nộp phiếu thử để tạo bằng chứng giả trong nghiên cứu.

Sáu hình QA tạo được SVG/PDF và PNG 300 DPI. Đã kiểm bố cục ba họ hình: phân bố nhãn,
chênh lệch ghép cặp, ma trận đồng thuận. Mọi hình QA đều có nhãn giả lập. Summary QA
khớp hoàn toàn giữa Python 3.12 và 3.15. Lệnh yêu cầu vẽ chất lượng khi không có nhãn
đã bị từ chối trước khi tạo đầu ra. Gói skill v0.11.0 / 55 pattern vẫn qua validator.

Lỗi CSV trộn hai bộ nhãn đã được tái hiện bằng regression test đỏ rồi sửa; thư mục QA
lỗi và workspace trước review được giữ riêng. Workspace dùng hiện tại là `workspace-v2`.

## Rà 11 nguy cơ diễn giải thống kê

Đây là rà thiết kế/phần mềm trước khi có nhãn; không phải 11 kết luận rằng dữ liệu thật
không có vấn đề. Mỗi mục cần đối chiếu lại khi lập báo cáo kết quả.

| Nguy cơ | Cách xử lý hiện tại và phần còn chờ |
|---|---|
| Simpson | Có kết quả riêng A/B và gộp; hướng chênh lệch thực còn chờ nhãn |
| Ecological fallacy | Giới hạn đơn vị suy luận ở 20 nguồn và hai người cố định |
| Berkson / tuyển chọn | Nêu rõ nguồn SFT tuyển chọn từ một bên phát hành; không gọi là holdout đại diện |
| Collider / điều kiện hóa | Không thêm biến kiểm soát hậu nghiệm; báo thiếu và số nguồn bị loại khỏi CI |
| Base rate neglect | Mọi bảng đếm có mẫu số 20; không suy precision/recall từ ba câu hỏi này |
| Regression to mean | Nguồn chốt trước đầu ra, không tuyển theo điểm cực đoan; bốn nhánh cùng nguồn |
| Survivorship | Giữ đủ 20 nguồn trong bảng chính, kể cả ca Jev lỗi/thiếu; CI chỉ dùng cặp đủ và báo số bị loại |
| Look-elsewhere | Một đối chiếu chính đã chốt; so sánh phụ được giữ và ghi là thăm dò, không có sao significance |
| Forking paths | Code, cấu hình và selection được lưu hash; không tự chọn phiếu, ngưỡng hoặc subset thuận lợi |
| Correlation / causation | Chỉ mô tả kết quả pilot ghép cặp; không suy hiệu quả phổ quát hoặc quan hệ nhân quả cho quần thể |
| Reverse causality | Nguồn được chốt trước biên tập; vẫn nêu giới hạn backend, thứ tự sinh và khả năng khái quát |

## Phần còn mở

Chờ hai người hoàn tất, xác nhận đúng ID phiếu, rồi mới nhập nhãn, kiểm chất lượng dữ
liệu và lập kết quả thật. Không có kết luận Vietnamizer thắng đối chứng từ các kiểm
thử này. Gemini thuộc pilot cũ vẫn bị chặn ở runtime host; xem CURRENT.md và isolation-gate.md.
