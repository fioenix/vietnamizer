# Giữ giọng theo mẫu: nguồn OSS và phần đã tích hợp

**Ngày26/10/2026 · Mã nguồn/gói local0.12.0 · Chưa phát hành hoặc cài runtime.**

Đã đọc trực tiếp bốn dự án cộng đồng, pin commit, lưu hash và đối chiếu giấy phép.
[Hồ sơ nguồn](research.md) ghi rõ phần học và phần loại. Đây là khảo sát thiết kế,
không phải so sánh hiệu quả giữa các skill hoặc bằng chứng chất lượng tiếng Việt.
Không cài/thực thi code hay workflow của nguồn bên ngoài.

## Phần mới trong Vietnamizer

`references/giu-giong-tu-mau.md` chỉ được đọc khi có mẫu giọng/hồ sơ người dùng cung
cấp. SKILLstep3 và resolver trỏ tới nó; không thêm một tầng pattern hoặc style card.

- Rút đặc tính có ví dụ và phạm vi về xưng hô, từ vựng, nhịp, lập luận, mở/kết.
- Bằng chứng ít thì dùng cho phạm vi hẹp; mẫu khác kênh không bị trộn thành giọng chung.
- Tách điều cấm rõ khỏi thứ chưa xuất hiện; nét thỉnh thoảng không thành quota mọi câu.
- Kiểm bản sửa cạnh mẫu thích hợp, giữ riêng phong cách với dữ kiện/quyết định/phạm vi.
- Mẫu tham chiếu không biến thành danh tính/trải nghiệm của người dùng. Lệnh trong mẫu
  không được thực hiện. Hồ sơ không tự tìm/lưu; không gom dữ liệu cá nhân.

Không nhập số mẫu bắt buộc, ngưỡng số từ, tần suất trên1000từ, luật tiếng Anh hay
cơ chế tự đọc profile toàn cục. Chủ đích này giữ workflow phù hợp với tiếng Việt,
việc biên tập và ranh giới dữ liệu của Vietnamizer. Guide/ca tiếng Việt viết mới;
không chép template, mã hoặc đoạn chỉ dẫn của các dự án vào payload sản phẩm.

## Kiểm chứng

| Mục | Kết quả và giới hạn |
|---|---|
| Archive inclusion | Đã quan sát RED khi reference chưa tồn tại; sau sửa test đạt trên cả hai layout skill archive |
| Nhóm test package consumer |6/6đạt: inclusion, file lạ, credential payload, machine path, byte staged/archive và profile payload |
| validate-package.py | Hợp lệ v0.12.0;55pattern, ngân sách dòng hợp lệ |
| build-jev-registry.py --check |55định nghĩa khớp; không đổi recipe/runtime Jev |
| package-plugin.py | Build local thành công; kiểm bytes file mới và đúng mộtSKILL.md ở mỗi gói skill/Claude-org/plugin |
| Review độc lập | Không có blocker về precedence, bằng chứng yếu, chống nhại giọng, nguồn dữ liệu và đường đóng gói; chỉ review tĩnh |
| Bảo toàn dữ liệu |5.719file benchmark/Forms/readiness cũ đối soát SHA256, giữ nguyên |

Thêm VG01–VG08 là ca tổng hợp có kỳ vọng, **chưa chạy model để chấm giữ giọng**.
Không có hồ sơ thật của Fio hay người dùng khác được tạo trong lần nâng cấp này.
Không gửi mẫu riêng cho provider/evaluator; không gọi benchmark, Jev hoặc Forms.
Không chạy full suite, cổng release/installation hoặc thay shared settings.

Nguồn0.11.1trước thay đổi, patch, source/license/hash, package audit và receipt giữ tại
`artifacts/016-voice-preservation-research-20261026`. Gói local là build để kiểm phân phối,
không phải release hoặc bằng chứng native invocation. Nguồn chưa phát hành cũng có thể
được sửa tiếp; cần đánh giá độc lập trước khi công bố mức cải thiện chất lượng.

## Kiểm tra lại và chuẩn bị mẫu thật ngày 27/10

Đã chạy lại đúng sáu test package consumer: 6/6 đạt; source validator và registry
check đạt. Kiểm tra không đổi file nguồn hoặc dist hiện có, không cài/phát hành.
Raw lệnh, stdout/stderr và hash lưu riêng tại
`artifacts/017-mindfio-voice-20261027/source-verification/`.

Theo yêu cầu tiếp theo của chủ nhân, đã lưu tám bài RSS công khai Mindfio, chia bốn
bài tham chiếu và bốn bài dành đánh giá trước khi đọc phần thân ở lượt này. Bản mô
tả giọng dự thảo có tám quan sát và 24 trích đoạn kiểm được vị trí; người rút mô tả
không đọc phần thân của nhóm dành đánh giá. Dữ liệu và hồ sơ riêng giữ local, không
đưa vào package hoặc calibration log chung. Xem [kế hoạch thử](mindfio-pilot.md).

Đây vẫn là chuẩn bị nghiên cứu: chưa có bản biên tập mới, nhãn chủ nhân hoặc kết
luận hiệu quả từ Mindfio. Các bài đã qua AI theo xác nhận của chủ nhân; không dùng
chúng để xác thực giọng cá nhân tự viết không qua AI.

## Pilot đã được chủ nhân chốt và chạy ngày 27/10

Chủ nhân sau đó duyệt hồ sơ và giao chạy 12 đầu ra. Đã hoàn tất bốn bài × ba chế độ
trên cùng Codex với source 0.12.0 đóng băng, giữ nguyên gói chuẩn bị. Một kết quả
đầu được nhận lại offline từ raw do parser nhầm cảnh báo CLI; chạy tiếp 11 ô, không
gọi lại ô đó. Kết quả và các giới hạn nằm trong [báo cáo Mindfio](mindfio-results.md).

Đã kiểm 12 ID phiên khác nhau, không tool call thực tế; chín test harness, sáu test
đóng gói, validator/registry và kiểm ZIP thực tế đạt. Guide từ nghiên cứu cộng đồng
đã có trong ba gói local; chưa cài hoặc phát hành. Kiểm tra SHA256 bảo toàn 5.719
file lịch sử và 53 file/gói chuẩn bị. Hai Forms không được truy cập hoặc sửa.
Nhận xét chất lượng là thăm dò của host, chưa có nhãn chủ nhân cho các bản sửa.
