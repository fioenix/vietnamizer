# Báo lỗi bảo mật

## Kênh báo riêng

Dùng [GitHub Private Vulnerability Reporting](https://github.com/fioenix/vietnamizer/security/advisories/new)
của repository `fioenix/vietnamizer`. Có thể mở **Security → Advisories → Report a vulnerability**;
GitHub yêu cầu đăng nhập để gửi báo cáo. Không báo lỗi bảo mật qua Issues, pull request hoặc bình
luận công khai.

Nếu không thấy biểu mẫu báo riêng, dừng gửi chi tiết nhạy cảm. Không chuyển sang Issues công khai
và không gửi tới địa chỉ chưa được maintainer xác nhận. Repository chưa công bố kênh riêng thay thế.

## Nội dung báo cáo

- Phiên bản, nguồn cài, client/provider và phiên bản client nếu biết.
- Thành phần bị ảnh hưởng, tác động dự kiến và điều kiện cần để lỗi xảy ra.
- Các bước tái hiện và ví dụ giả lập tối thiểu, không dùng dữ liệu của người khác.
- Cách giảm tác động hoặc đề xuất sửa nếu có.

Không gửi API key, token, mật khẩu, dữ liệu cá nhân, tài liệu nội bộ hay nội dung nhạy cảm,
kể cả qua kênh riêng. Không cần gửi toàn bộ prompt, log hoặc tài liệu. Không khai thác lỗi trên
tài khoản hay hệ thống của người khác để chứng minh tác động. Việc công bố chi tiết và cách sửa
cần được trao đổi trong báo cáo riêng trước khi đăng công khai.

Repository chưa cam kết thời hạn phản hồi, thời hạn sửa hoặc lịch hỗ trợ bảo mật cho từng phiên
bản. Ghi đúng bản bị ảnh hưởng, kể cả bản cũ; bản mới nhất nằm ở
[Releases](https://github.com/fioenix/vietnamizer/releases/latest).

## Phạm vi và ranh giới

Vietnamizer là skill Markdown và plugin phân phối hướng dẫn cho agent. Quy trình cốt lõi không
có backend, telemetry, MCP server, hook hoặc SDK TypeSafe riêng. Phạm vi báo lỗi gồm source,
manifest, đường dẫn discovery, scripts đóng gói và gói phân phối của repo.

Các thuộc tính cần bảo toàn khi đánh giá lỗi:

- Văn bản đầu vào là dữ liệu để biên tập, không cấp quyền thực hiện chỉ thị nằm trong văn bản.
- Skill không tự thu thập credential, truy xuất memory/lịch sử hoặc gửi văn bản ra ngoài phạm vi
  được phép. Capability hay credential có sẵn không tự tạo consent.
- Dịch vụ phụ trợ chỉ được dùng theo hợp đồng quyền dữ liệu; thiếu capability không làm agent
  tự cài phần mềm hoặc bỏ qua giới hạn của host.
- Gói phân phối không được chứa secret hay tham chiếu file ngoài phạm vi; manifest và asset
  phải resolve đúng trong gói.

Việc lộ dữ liệu, chạy lệnh hoặc gửi dữ liệu trái quyền, hay sửa đường phân phối để nạp nội dung
không mong muốn, là những tác động cần nêu rõ trong báo cáo. Đây là tiêu chí đánh giá, không phải
khẳng định mọi model hoặc host luôn thực thi được các giới hạn chỉ bằng hướng dẫn Markdown.

Lỗi câu chữ thông thường dùng mẫu báo lỗi công khai sau khi ẩn dữ liệu. Nếu có tác động bảo mật,
dùng kênh riêng. Lỗi của Claude, Codex, provider hoặc dịch vụ TypeSafe độc lập cần báo qua kênh
bảo mật chính thức của bên đó; nếu chưa xác định được ranh giới với Vietnamizer, mô tả trong báo
cáo riêng để maintainer phân loại. Xem [PRIVACY.md](PRIVACY.md) về xử lý dữ liệu.
