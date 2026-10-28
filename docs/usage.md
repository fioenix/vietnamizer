# Sử dụng, phạm vi và dữ liệu

[← README](../README.md)

## Dùng ngay

```text
/vietnamizer

[văn bản cần biên tập]
```

Khi cần sửa file, nêu rõ phạm vi:

```text
Dùng vietnamizer để sửa phần văn xuôi trong docs/bai-viet.md.
Giữ nguyên code, bảng tham số và các trích dẫn.
```

### Ba prompt dùng thử trên Claude

Dán từng prompt bên dưới sau khi chọn skill Vietnamizer. Với Claude Code, thêm
`/vietnamizer:vietnamizer` trước prompt. Đây là mẫu thử và tiêu chí mong đợi, không phải cam kết
mọi lần chạy model sẽ trả cùng một câu.

1. **Hoàn chỉnh ý:** “Sửa câu sau trong bài kể trải nghiệm; chỉ trả câu cuối: Đã thử ba cách mà
   vẫn không giải quyết vấn đề.” Kết quả mong đợi thêm “được” sau “giải quyết”, giữ “ba cách”.
2. **Giữ câu vốn tự nhiên:** “Rà câu sau trong chat công việc; nếu đã tự nhiên thì giữ nguyên.
   Chỉ trả câu cuối: Tôi rời công ty lúc sáu giờ.” Kết quả mong đợi giữ nguyên câu.
3. **Giữ code trong README:** dùng mẫu dưới đây. Kết quả mong đợi thêm “là” sau “đơn giản nhất”
   và giữ nguyên khối code từng byte.

````text
Biên tập phần văn xuôi sau trong README; giữ nguyên khối code từng byte:
Cách xử lý đơn giản nhất tăng số worker.

```bash
WORKERS=3 ./run-worker.sh --dry-run
```
````

### Cách hoạt động, dữ liệu và hỗ trợ

Plugin nạp hướng dẫn Markdown, profile và bảng tra đi kèm; không có MCP server, hook, bước
cài dependency hoặc chương trình chạy nền. Chỉ phần văn bản người dùng giao để biên tập được
xử lý; không tự tìm mẫu giọng trong memory hoặc lịch sử hội thoại. Agent có thể đọc hay sửa
file được người dùng giao trong phạm vi cụ thể, theo quyền và cơ chế xác nhận của host.
Đó không phải quyền quét các file khác để thu thập dữ liệu.

Maintainer không có máy chủ nhận văn bản hay telemetry của plugin. Claude vẫn xử lý và có thể
lưu hội thoại theo chính sách của nền tảng; plugin không biến việc biên tập thành xử lý hoàn
toàn trên máy. Không gửi credential, định danh chính phủ, dữ liệu thẻ thanh toán hoặc PHI.
Xem [quyền riêng tư](../PRIVACY.md) và [điều kiện sử dụng](../TERMS.md).

Khi host cấp key và đã có quyền gửi dữ liệu, Vietnamizer tự động thử đánh giá qua TypeSafe;
đoạn gốc, candidate và ngữ cảnh liên quan được gửi tới dịch vụ đó. Không có key thì core không
gọi dịch vụ. Xem [quyền riêng tư](../PRIVACY.md) và [hợp đồng Jev](../references/typesafe-advisor.md).

- **Không thấy skill:** kiểm plugin đã bật, rồi mở phiên mới. Trong Claude Code kiểm đúng
  marketplace `vietnamizer` và lời gọi `/vietnamizer:vietnamizer`.
- **Mô tả hoặc phiên bản chưa đổi:** cập nhật đúng plugin cùng tên từ nguồn đã cài; tránh cài
  thêm bản review trùng tên. ZIP upload riêng không tự cập nhật từ GitHub.
- **Icon mặc định:** manifest có icon, nhưng kết quả CLI validator không chứng minh client
  hiển thị nó. Kiểm preview listing; không coi icon mặc định là lỗi của quy trình biên tập.
- **Sửa sai hoặc sửa quá tay:** gửi ca giả lập/đã ẩn danh cùng kết quả mong đợi qua
  [GitHub Issues](https://github.com/fioenix/vietnamizer/issues) theo mẫu báo lỗi. Đọc
  [hướng dẫn đóng góp](../CONTRIBUTING.md) trước; không gửi toàn bộ prompt, log hay tài liệu.
- **Lỗi bảo mật:** dùng [kênh báo riêng](../SECURITY.md), không đăng lên Issues công khai.
  Không gửi API key, token, dữ liệu cá nhân, tài liệu nội bộ hoặc nội dung nhạy cảm.

## Phạm vi

Skill xử lý ba lớp:

- V1–V25 kiểm tra cách dùng từ và cấu trúc câu, chẳng hạn thiếu bổ ngữ kết quả, thiếu loại từ, dịch sát giới từ, đặt trạng ngữ gây mơ hồ hoặc để sót lời chào của trợ lý trong tài liệu.
- B1–B17 và K1–K7 kiểm tra sự phù hợp với thể loại. Blog, tin nhắn, README và bài nghiên cứu không dùng cùng một giọng.
- T1–T6 kiểm tra typography. Với văn xuôi thông thường, chỉ áp dụng khi đồng thời có ít nhất một lỗi
  V1–V25; với thể loại được giới hạn ở typography-only thì không cần lỗi V đi kèm.

Trước khi sửa, skill xác định thể loại, đọc profile phù hợp và dùng mẫu văn hoặc hồ sơ phong cách
người dùng chủ động cung cấp. Skill không tự truy xuất memory hay lịch sử hội thoại để tìm mẫu.

Skill không dùng kết quả rà soát để xác định tác giả. Người viết song ngữ cũng có thể giữ cấu trúc tiếng Anh trong câu tiếng Việt; LLM cũng có thể tạo ra câu hoàn toàn tự nhiên.

### Jev tự động khi có key

Từ 0.10.0, mỗi lượt Vietnamizer kiểm tra key được host cấp. Không có key thì Agent dùng core
Markdown, không gọi API hoặc yêu cầu thiết lập. Có `TYPESAFE_API_KEY`, script execution và quyền
gửi dữ liệu thì Agent phải thử runner `python3 -B -m jev evaluate --input /absolute/workspace/input.json` từ skill root.
Runner dùng Python 3.12+ standard library, không SDK; gửi nguyên đoạn cùng ngữ cảnh cần thiết tới
TypeSafe, model pin `jev-1.14.0`. Key không thay thế quyền truyền dữ liệu hoặc giới hạn của host.
Từ v0.10.5, runner tự tách câu với input v2; `prepare` chạy offline để xem các span và phần chưa rõ.
Host chọn layout, đánh dấu vùng bảo toàn và rà phụ thuộc ngữ cảnh; chỉ dữ liệu được phép mới gửi.
Coverage tách nguồn/ranh giới/ngữ cảnh/câu hỏi. Hết batch vẫn liệt kê phần chưa kiểm; không phải
bài dài nào cũng hoàn tất trong 32 request. Input cũ chỉ chứng minh coverage các section đã cung cấp.

Gói chứa định nghĩa chuẩn bị sẵn cho đủ V1–V25, T1–T6, B1–B17, K1–K7. Mỗi phần chỉ dùng
pattern phù hợp thể loại/profile; kiểm cơ học nằm trong mã. Kết quả có coverage và phân bố,
không phải chứng nhận câu đúng. LLM viết candidate/bản cuối, dùng tín hiệu Jev dưới năm chốt chặn;
runner không tự áp hoặc quyết định edit bằng ngưỡng số. Chất lượng tiếng Việt chưa được xác nhận
bởi test schema hay transport.

Key hỏng, quyền bị chặn, timeout hoặc vượt giới hạn thì tiếp tục core và nêu đúng phần Jev chưa
hoàn tất. Không có capability script thì không mạo nhận đã kiểm key. Hướng dẫn input, status,
ngữ cảnh, candidate và bảo toàn nằm trong [hợp đồng Jev](../references/typesafe-advisor.md).
Các nghiên cứu 001/002/005 vẫn là lịch sử, không phải runtime mới hoặc bằng chứng hiệu quả.
