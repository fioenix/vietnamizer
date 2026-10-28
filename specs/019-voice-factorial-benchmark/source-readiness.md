# Pilot giữ giọng: dừng ở cổng nguồn

Ngày 27/10/2026. Chủ nhân đã duyệt pilot 32 đầu ra, trần 56 request model,
Codex biên tập và Codex/Gemini chấm ẩn nhãn, với điều kiện kiểm tra đủ nguồn mới.
Sau khi biết nguồn thiếu, chủ nhân yêu cầu tự tìm thêm và dừng nếu không có.

**Kết quả: không có đủ nguồn mới đạt điều kiện; đã dừng, dùng 0/56 request model.**

| Kiểm tra | Quan sát |
|---|---|
| RSS Mindfio | HTTP200, tám bài |
| Archive API, offset0/limit50 | HTTP200, cùng tám bài |
| Archive API, offset8/limit50 | HTTP200, danh sách rỗng |
| Đối soát đợt cũ | Cả tám URL và hash bản chữ đều trùng bài đã dùng |
| About và profile được archive liên kết | HTTP200; About trỏ LinkedIn, profile trỏ lại cùng publication |
| Tìm công khai bổ sung | Chưa xác minh được bộ bài tiếng Việt mới đủ điều kiện; không nhận người trùng tên hoặc bài tiếng Anh làm mẫu thay thế |

Thiết kế cần ba mẫu cho agent, hai mẫu riêng cho giám khảo và bốn bản thử đã
có giọng người viết, tách ở cấp bài/chuỗi bài. Bốn nháp AI trung tính có thể tạo
riêng trong trần đã chốt, nhưng không thay thế các mẫu giọng/bản thử đang thiếu.
Không chia lại tám bài cũ rồi gọi là nguồn holdout mới.

Phạm vi kiểm tra là các endpoint công khai được ghi trong raw và lượt tìm công
khai giới hạn; không kết luận người viết không có tài liệu riêng hoặc bài chưa
được công cụ tìm thấy. LinkedIn/Medium không tải được qua web tool trong lượt
này; không truy cập tài khoản đăng nhập hoặc vượt hạn chế để lấy nội dung.

Không tạo bản AI mới, không gọi Codex/Gemini/Jev để biên tập hoặc chấm, chưa
kiểm quota/model runtime và không xây runner khi điều kiện nguồn chưa đạt.
Thiết kế được giữ lại; không có lịch hoặc tác vụ tự chạy tiếp.

Raw HTTP nguồn, request metadata, inventory, đối soát hash và bản đề xuất trước
khi cập nhật trạng thái giữ riêng tại `artifacts/019-voice-source-audit-20261027/`.
Raw gồm feed, archive HTML/JSON, About/profile và lỗi sitemap404; không có
request/response model vì chưa gọi model. Metadata lượt tìm được ghi riêng,
không gọi nó là raw HTTP của công cụ tìm kiếm.

Benchmark cũ và hai Forms giữ nguyên; không tạo/sửa Forms hoặc gửi lời mời.
