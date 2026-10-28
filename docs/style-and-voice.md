# Giọng gốc, giọng mẫu và phong cách

[← README](../README.md)

## Giữ giọng và chọn phong cách

### Giữ giọng của một người cụ thể

Có thể đưa mẫu văn ngay trong yêu cầu:

```text
Đây là hai đoạn tôi tự viết:
[mẫu văn]

Hãy sửa đoạn dưới theo cùng cách xưng hô, nhịp câu và mức độ trang trọng:
[văn bản cần sửa]
```

Mẫu văn chỉ được ưu tiên đối với thói quen xuất hiện nhất quán, như cách xưng hô, nhịp câu, cách chêm tiếng Anh hoặc dùng dấu câu. Nó không hợp thức hoá lỗi ngôn ngữ rõ ràng và không vượt qua năm quy tắc chốt chặn trong `SKILL.md`.

Có thể dán một hồ sơ phong cách ngắn trong yêu cầu thay cho mẫu văn. Hồ sơ chỉ dùng cho đúng người
và phạm vi đã nêu; yêu cầu hiện tại được ưu tiên. Skill không tự tìm hay lưu hồ sơ ngoài tác vụ.

### Chọn phong cách theo mục đích

`vietnamizer` không còn gom mọi văn bản vào hai giọng *cá nhân* và *trung tính*. Hai profile đó vẫn
giữ vai trò cổng pattern, còn bộ giải phong cách chọn một card theo mục đích, người đọc, quan hệ,
thanh ngữ vực, kênh và mẫu giọng. Một phần văn bản chỉ dùng tối đa một card; file pha nhiều chức
năng được chia theo phần, không ép chung một giọng.

| Style card | Dùng cho | Base profile |
|---|---|---|
| [`ke-trai-nghiem`](../profiles/blog-ca-nhan/styles/ke-trai-nghiem.md) | Blog, bài kể có người viết hiện diện | `blog-ca-nhan` |
| [`phoi-hop-cong-viec`](../profiles/blog-ca-nhan/styles/phoi-hop-cong-viec.md) | Chat, bình luận và lời nhờ trong công việc | `blog-ca-nhan` |
| [`chuyen-mon-cong-khai`](../profiles/blog-ca-nhan/styles/chuyen-mon-cong-khai.md) | LinkedIn, bài quan điểm hoặc chia sẻ chuyên môn | `blog-ca-nhan` |
| [`marketing-thuyet-phuc`](../profiles/blog-ca-nhan/styles/marketing-thuyet-phuc.md) | Nội dung giới thiệu có mục tiêu và CTA thật | `blog-ca-nhan` |
| [`huong-dan-ky-thuat`](../profiles/ky-thuat-doanh-nghiep/styles/huong-dan-ky-thuat.md) | README, văn xuôi API và hướng dẫn xử lý lỗi | `ky-thuat-doanh-nghiep` |
| [`van-hanh-doanh-nghiep`](../profiles/ky-thuat-doanh-nghiep/styles/van-hanh-doanh-nghiep.md) | SOP, báo cáo, biên bản và bàn giao | `ky-thuat-doanh-nghiep` |
| [`hoc-thuat-phan-tich`](../profiles/ky-thuat-doanh-nghiep/styles/hoc-thuat-phan-tich.md) | Giáo trình, đề án và nghiên cứu | `ky-thuat-doanh-nghiep` |

Card không phải khuôn để “làm màu” và không tự tạo lý do sửa. Yêu cầu hiện tại được ưu tiên;
ràng buộc thể loại và năm quy tắc chốt chặn vẫn giới hạn mọi thay đổi; mẫu/hồ sơ chỉ được dùng khi
đúng người, đúng phạm vi và có đặc tính ổn định. Chi tiết chuẩn nằm trong
`references/bo-giai-phong-cach.md`.

## Giữ giọng khi có mẫu

**Đã có cơ chế giúp agent biên tập theo giọng tham chiếu của người dùng.** Gửi bản
nháp cùng mẫu tự viết, bản đã sửa từ nháp AI hoặc hồ sơ phong cách được chủ động
cung cấp. Skill dùng mẫu để chọn cách sửa phù hợp, không viết lại mọi câu cho
giống một khuôn giọng.

[Hướng dẫn đọc mẫu](../references/giu-giong-tu-mau.md) yêu cầu rút đặc tính có ví dụ
và phạm vi: đại từ làm chức năng gì, dùng thuật ngữ và cách viết số nào, nhịp câu/dấu ngắt,
đề mục và mở/kết ra sao. Có thể theo cách dùng chữ số cho lượng cụ thể, giữ đề mục hỏi có
chức năng và dùng nhiều đại từ theo vai trò; không thay toàn cục hoặc đưa dữ kiện của mẫu vào bài. Agent đối chiếu bản sửa với mẫu cùng kênh và mục đích; không suy tính
cách, không rải câu cửa miệng hoặc tự thêm trải nghiệm. Một mẫu ngắn vẫn giúp
giữ đặc tính hẹp; không đặt số bài tối thiểu chưa được kiểm chứng.

Hình thức hợp lệ chưa tự là lựa chọn nên dùng: phần giới thiệu khái niệm có thể hợp câu hỏi,
phần thao tác có thể hợp bạn, phần đối chiếu cần làm rõ những trạng thái đã có. Không cấm câu
hỏi/bạn hoặc giữ cứng bố cục nguồn; khi đổi cấu trúc vẫn kiểm phạm vi đề mục, quan hệ và tình thái.

Ví dụ lời yêu cầu, kèm bản nháp và mẫu ngay trong tác vụ:

```text
Use Vietnamizer to edit the draft below for my personal blog.
Adapt the draft toward the supplied reference voice.
You may restructure sentences, paragraphs, headings or existing lists using evidenced sample traits.
Preserve every proposition, condition, quantity, level of certainty and protected span.
Preserve my meaning, level of certainty, terminology and short-sentence rhythm.
Do not invent experiences or repeat catchphrases just to imitate the samples.
Return only the edited article.

<writing_samples>Paste your reference samples here.</writing_samples>
<draft>Paste your draft here.</draft>
```

**Hai chế độ:** yêu cầu rà lỗi, viết tự nhiên hơn hoặc chỉ đưa mẫu vẫn mặc định **giữ giọng gốc**.
Mẫu giúp đối chiếu, không tự bật chuyển giọng. Ví dụ trên chủ động chọn **theo giọng mẫu**;
chế độ này cần mẫu/hồ sơ dùng được và cho phép đổi cấu trúc câu đúng có căn cứ. Có thể tách
các định nghĩa đã có thành bullet hoặc đặt đề mục từ ý sẵn có; không thêm bước, đổi cách nhóm
mơ hồ, bỏ điều kiện hoặc sửa số liệu để giống mẫu. Nếu cần mẫu mà chưa có thì chỉ hỏi mẫu còn thiếu.

Để giữ giọng gốc dù có mẫu, dùng yêu cầu:

```text
Copyedit this draft while preserving its existing voice.
Use the supplied samples only to check consistency, not to transfer their voice.
```

Blog công nghệ có người viết hiện diện được chọn profile theo mục đích blog; README/SOP vẫn
giữ profile kỹ thuật cùng các giới hạn riêng. Không dùng giọng mẫu để đổi thể loại hoặc vùng bảo toàn.

Mẫu được khai báo đã qua AI là giọng tham chiếu người dùng chọn, chưa chứng minh
giọng tự viết không có AI. Không có mẫu và không yêu cầu theo mẫu thì giữ giọng bản gốc và thể loại, không
khẳng định đã bắt chước đúng người. Workflow hiện tại tập trung vào **biên tập
bản nháp theo mẫu**, chưa chứng minh khả năng viết bài mới khớp giọng từ đầu.

Không tự truy xuất hoặc cập nhật hồ sơ trong HOME, memory hay nguồn ngoài tác vụ. Chỉ tạo bản tóm tắt giọng để người dùng xem/lưu khi họ yêu cầu; đây vẫn là công cụ biên tập, không tự tạo trải nghiệm hay quan điểm thay người viết. Chưa có benchmark độc lập chứng minh chất lượng giữ giọng của bản hiện tại.

## Hồ sơ phong cách và nhật ký hiệu chuẩn

Hai cơ chế này phục vụ hai mục đích khác nhau.

### Hồ sơ người dùng chủ động cung cấp

Người dùng có thể tự giữ một hồ sơ và dán vào yêu cầu. Hồ sơ nên ngắn, chỉ chứa thông tin giữ giọng:

- cách xưng hô;
- nhịp và độ dài câu thường dùng;
- mức dùng từ Hán-Việt;
- cách chêm tiếng Anh;
- thói quen viết hoa và dấu câu;
- phạm vi áp dụng cùng một ví dụ ngắn.

Skill chỉ dùng hồ sơ được cung cấp trong tác vụ, không tự truy xuất Claude memory, lịch sử chat
hoặc dữ liệu khác, cũng không tự ghi hồ sơ. Không dùng mẫu của người này cho người khác;
yêu cầu hiện tại luôn được ưu tiên.

### `calibration/LOG.md`

Đây là nhật ký bằng chứng dùng để bảo trì quy tắc chung của skill, không phải hồ sơ cá nhân. Chỉ ghi vào log khi phản hồi cho thấy:

- một pattern sửa nhầm câu vốn đúng;
- mục **Không flag** còn thiếu trường hợp loại trừ;
- skill bỏ sót một lỗi có thể gọi tên;
- người bản ngữ nêu một quy tắc tiếng Việt có thể kiểm tra độc lập.

Khác biệt chỉ thuộc sở thích cá nhân không được đưa vào log. Nhờ ranh giới này, skill không âm thầm học giọng của một người rồi áp lên mọi người dùng khác.

Quy trình đầy đủ nằm trong `AGENTS.md`.
