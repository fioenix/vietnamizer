# Hồ sơ đặc tả

`007-automatic-jev-evaluation/spec.md` ghi quyết định owner ngày 16/10/2026, đã triển khai và
phát hành trong v0.10.0: runner Jev advisory tự động thử khi host cấp key và quyền gửi dữ liệu,
giữ nhánh offline và năm chốt chặn. Quyết định này thay thế phần cấm mã tích hợp của 005;
không khôi phục các runtime nghiên cứu cũ.

`008-sentence-coverage/spec.md` là spec mở rộng tách đoạn, tách câu tự động và đối soát coverage,
giữ nguyên đoạn và ngữ cảnh liên quan cho từng câu. Owner đã duyệt spec ngày 16/10/2026;
spec/plan/tasks đã được duyệt; source local đã qua kiểm chứng và review theo evidence/review trong cùng thư mục.
PR #12 đã merge vào main tại `82c826d` ngày 18/10/2026; CI sau merge đã qua.
Owner yêu cầu phát hành phần mở rộng này dưới phiên bản v0.10.5, thay cho nhãn source 0.11.0
chưa công bố. Trạng thái release và bản cài dùng chung được xác minh riêng; không suy từ checkbox.

Quyết định 005 ngày 03/10/2026 bỏ mã TypeSafe là lịch sử. Các feature 001, 002 và phần triển khai
CLI của 005 đã ngừng dùng. Plan, tasks, quickstart,
contract và evidence trong các thư mục đó là hồ sơ lịch sử, không phải backlog đang mở hoặc
hướng dẫn chạy hiện tại. Checkbox cũ chỉ mô tả trạng thái tại thời điểm thực hiện; không chứng
minh mã còn tồn tại hoặc workflow hiện tại đã qua kiểm tra. Không khôi phục mã từ các tài liệu này.

Các feature 003 và 004 cùng quy tắc biên tập hiện hành không thay đổi bởi quyết định này.
