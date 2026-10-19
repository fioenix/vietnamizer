# Vietnamizer

![Vietnamizer — Giúp AI viết tiếng Việt giống con người hơn.](assets/wordmark.svg#gh-light-mode-only)
![Vietnamizer — Giúp AI viết tiếng Việt giống con người hơn.](assets/wordmark-dark.svg#gh-dark-mode-only)

> **Giúp AI viết tiếng Việt giống con người hơn.**

Vietnamizer là skill dành cho Claude, Codex và các agent hỗ trợ Skills CLI. Skill xác định thể
loại cùng người đọc trước, gọi tên lỗi rồi chỉ sửa phần thực sự có vấn đề. Blog vẫn giữ cá tính;
README vẫn giữ thuật ngữ kỹ thuật; báo cáo doanh nghiệp không bị kéo thành lời trò chuyện.

Skill dùng được cho bản nháp do AI tạo, bản dịch sát tiếng Anh, nội dung do người viết song ngữ soạn
hoặc bất kỳ đoạn tiếng Việt nào đọc chưa thuận miệng. Đây không phải công cụ phát hiện AI và không
dùng lỗi ngôn ngữ để đoán tác giả.

## Ba ví dụ đã được hiệu chỉnh

| Mục tiêu | Trước | Sau khi biên tập |
|---|---|---|
| Hoàn chỉnh ý | *Đã thử ba cách mà vẫn không giải quyết vấn đề.* | *Đã thử ba cách mà vẫn không giải quyết **được** vấn đề.* |
| Khôi phục từ bị thiếu | *Câu này đúng ngữ pháp nhưng đọc lên thấy hụt.* | *Câu này đúng ngữ pháp nhưng đọc lên thấy **hụt hẫng**.* |
| Giữ đúng giọng công việc | *Đội kỹ thuật đã triển khai hệ thống quản lý kho mới để vận hành gọn hơn.* | *Nhằm mục đích nâng cao hiệu quả vận hành kho, **team dev** đã triển khai hệ thống quản lý kho mới.* |

Các cặp trên lấy từ [nhật ký hiệu chuẩn](calibration/LOG.md) và những ví dụ đã khóa trong
`SKILL.md`. Đây không phải bảng tìm–thay cố định: skill chỉ sửa khi ngữ cảnh, thể loại và mẫu giọng
cho thấy bản gốc thật sự có vấn đề.

## Cài nhanh

Tên mới từ bản **0.9.7**: Vietnamizer, định danh `vietnamizer` (trước đây là
`vi-humanizer`). Bản hiện tại là **0.10.6**, đồng bộ hướng dẫn cài đặt với catalog Codex dùng
chung của Finolabs tại `fioenix/agybird` và giữ nguyên tách câu, coverage trên nền Jev tự động khi host cấp key và quyền gửi
dữ liệu; phát hành GitHub không đồng nghĩa được Directory chấp thuận.
Asset của các release trước 0.9.7 vẫn mang tên
`vi-humanizer.*` và chứa định danh cũ.
Xem [hướng dẫn chuyển tên](docs/rename-vietnamizer-2026-10-03.md).

### Codex và các agent dùng Skills CLI

```bash
npx --yes skills@1.5.20 add fioenix/vietnamizer --global
```

Cài cho mọi agent mà Skills CLI hỗ trợ:

```bash
npx --yes skills@1.5.20 add fioenix/vietnamizer \
  --skill vietnamizer \
  --agent '*' \
  --global \
  --yes
```

Bỏ `--global` nếu muốn cài trong phạm vi dự án. Có thể xem skill mà CLI tìm được trước khi cài:

```bash
npx --yes skills@1.5.20 add fioenix/vietnamizer --list
```

Skills CLI nhận repository, URL hoặc đường dẫn cục bộ làm nguồn. Cờ `--agent '*'` chọn mọi agent được hỗ trợ; cờ `--copy` buộc CLI sao chép file thay vì tạo liên kết tượng trưng.

### Claude Code plugin

```text
/plugin marketplace add fioenix/vietnamizer
/plugin install vietnamizer@vietnamizer
```

Đây là marketplace của repo, không cần chờ Anthropic duyệt directory. Sau khi cài, gọi skill
bằng `/vietnamizer:vietnamizer` kèm đoạn cần biên tập. Nếu chưa thấy skill, mở phiên mới.

### Claude web và Claude Desktop: thêm marketplace

1. Mở **Customize → Plugins → Add → Add marketplace**.
2. Chọn **Add from a repository**, nhập `fioenix/vietnamizer` hoặc
   `https://github.com/fioenix/vietnamizer`.
3. Trong **Discover**, chọn **Vietnamizer → Add**, rồi kiểm plugin đã bật.
4. Trong cuộc trò chuyện, gõ `/` hoặc bấm `+`, chọn skill **Vietnamizer** và gửi đoạn cần sửa.

Theo [hướng dẫn của Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude),
plugin trên web/Desktop dành cho các gói Pro, Max, Team và Enterprise. Nếu không thấy tùy chọn,
kiểm tra gói và chính sách của tổ chức; cài riêng không bỏ qua các giới hạn này.

Có thể tải `vietnamizer-plugin.zip` từ
[Releases](https://github.com/fioenix/vietnamizer/releases/latest) để upload plugin thay vì thêm
repo. Không dùng `vietnamizer.skill` hoặc `vietnamizer-claude-org.zip` ở bước upload plugin:
hai file đó là gói skill riêng.

Vietnamizer chưa được Anthropic duyệt vào directory; việc gửi duyệt đang tạm dừng. Các đường
cài riêng ở trên không phụ thuộc việc niêm yết. Maintainer giữ
[checklist gửi Anthropic](docs/claude-marketplace-checks.md) để dùng khi tiếp tục.

### Marketplace plugin cho tổ chức Claude

Owner của tổ chức Team/Enterprise có thể tải `vietnamizer-plugin.zip` từ Releases, mở
**Organization settings → Plugins & skills → Add → Upload a plugin**, chọn marketplace mới
hoặc có sẵn rồi upload. Thành viên cài plugin từ **Discover** theo quyền được cấp.

Đừng nhầm với **Sync from GitHub** của marketplace tổ chức: đường sync này yêu cầu repo
GitHub private/internal, không nhận trực tiếp repo public `fioenix/vietnamizer`. Dùng upload
ZIP cho trường hợp đó. Xem
[hướng dẫn quản trị plugin](https://support.claude.com/en/articles/13837433-manage-plugins-for-your-organization)
về quyền, bật Cowork/Skills và chính sách phân phối.

### Codex plugin và Marketplace

Catalog Codex dùng chung của Finolabs được công bố tại `fioenix/agybird` từ bản `v0.2.1`
(tên máy `agybird`, `displayName` là `Finolabs`), gồm ba mục `agybird@agybird`,
`vietnamizer@agybird` và `markmap-skills@agybird`:

```bash
codex plugin marketplace add fioenix/agybird
codex plugin add vietnamizer@agybird
```

Khi kiểm thử từ bản clone cục bộ của `agybird`, có thể đăng ký bằng đường dẫn thư mục:

```bash
codex plugin marketplace add /duong/dan/toi/agybird
codex plugin add vietnamizer@agybird
```

Repo này vẫn giữ `.agents/plugins/marketplace.json` độc lập (tên máy `vietnamizer`,
`displayName` là `Vietnamizer`) để tương thích ngược và phục vụ kiểm tra gói tại chỗ:

```bash
codex plugin marketplace add fioenix/vietnamizer
codex plugin add vietnamizer@vietnamizer
```

**Chuyển từ `vietnamizer@vietnamizer` sang `vietnamizer@agybird` và hoàn tác (rollback):**
sao lưu cấu hình plugin/marketplace hiện tại của Codex trước khi đổi nguồn, sau đó thêm catalog
`agybird`, cài `vietnamizer@agybird` và xác nhận skill nạp đúng rồi mới gỡ hoặc tắt đăng ký
`vietnamizer@vietnamizer` cũ; không xóa thẳng dữ liệu khi chưa có bản sao lưu và chưa kiểm tra
xong bản thay thế. Nếu cần quay lại đường cũ, khôi phục từ bản sao lưu hoặc đăng ký lại nguồn
độc lập `fioenix/vietnamizer` (hoặc bản clone cục bộ của repo này) và cài lại
`vietnamizer@vietnamizer`.

Khả năng hiển thị tên nguồn `Finolabs` hoặc `Vietnamizer` và cách gom nhóm trong trang Plugins
phụ thuộc từng bản client Codex; tài liệu này không khẳng định client đã tự gom nhóm trên UI
hoặc đã cài đặt thực tế. Skills CLI ở trên vẫn là đường cài độc lập. Catalog của repo không đồng
nghĩa plugin đã được duyệt vào directory chính thức của OpenAI hoặc Anthropic.

Xem [hướng dẫn phân phối và kiểm thử](docs/plugin-distribution.md),
[quyền riêng tư](PRIVACY.md) và [điều kiện sử dụng](TERMS.md).

### Claude web và Claude Desktop: chỉ cài skill

[Tải gói skill từ trang Releases](https://github.com/fioenix/vietnamizer/releases/latest),
mở **Customize → Skills → + Create skill → Upload a skill**, chọn file vừa tải rồi bật skill.
Claude cần bật **Code execution and file creation** để dùng custom skill. Xem thêm
[hướng dẫn chính thức của Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

### Claude Org: chỉ cài skill

[Tải gói Claude Org từ trang Releases](https://github.com/fioenix/vietnamizer/releases/latest),
mở **Organization settings → Plugins & skills → Add → Upload a skill**, rồi chọn file ZIP. Gói này
đặt `SKILL.md` và `LICENSE` ở thư mục gốc, cùng các file cần khi skill chạy.

### Đóng gói từ source

Người bảo trì repo có thể tự tạo lại cả hai artifact:

```bash
./scripts/package-skill.sh
```

Kết quả nằm ở `dist/vietnamizer.skill` và `dist/vietnamizer-claude-org.zip`.

Để tạo gói plugin chung cho Codex và Claude Code:

```bash
python3 scripts/package-plugin.py
```

Kết quả là `dist/vietnamizer-plugin.zip`, có hai manifest và một skill trong
`skills/vietnamizer/`. Script tạo gói từ source chuẩn; không bảo trì bản Markdown thứ hai.

### Cài thủ công

Chép `LICENSE`, `SKILL.md` cùng `profiles/`, `references/`, `calibration/`, `agents/`, `assets/` và `jev/` vào
thư mục skill của agent:

```bash
git clone https://github.com/fioenix/vietnamizer.git /duong/dan/toi/skills/vietnamizer
```

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
Xem [quyền riêng tư](PRIVACY.md) và [điều kiện sử dụng](TERMS.md).

Khi host cấp key và đã có quyền gửi dữ liệu, Vietnamizer tự động thử đánh giá qua TypeSafe;
đoạn gốc, candidate và ngữ cảnh liên quan được gửi tới dịch vụ đó. Không có key thì core không
gọi dịch vụ. Xem [quyền riêng tư](PRIVACY.md) và [hợp đồng Jev](references/typesafe-advisor.md).

- **Không thấy skill:** kiểm plugin đã bật, rồi mở phiên mới. Trong Claude Code kiểm đúng
  marketplace `vietnamizer` và lời gọi `/vietnamizer:vietnamizer`.
- **Mô tả hoặc phiên bản chưa đổi:** cập nhật đúng plugin cùng tên từ nguồn đã cài; tránh cài
  thêm bản review trùng tên. ZIP upload riêng không tự cập nhật từ GitHub.
- **Icon mặc định:** manifest có icon, nhưng kết quả CLI validator không chứng minh client
  hiển thị nó. Kiểm preview listing; không coi icon mặc định là lỗi của quy trình biên tập.
- **Sửa sai hoặc sửa quá tay:** gửi ca giả lập/đã ẩn danh cùng kết quả mong đợi qua
  [GitHub Issues](https://github.com/fioenix/vietnamizer/issues) theo mẫu báo lỗi. Đọc
  [hướng dẫn đóng góp](CONTRIBUTING.md) trước; không gửi toàn bộ prompt, log hay tài liệu.
- **Lỗi bảo mật:** dùng [kênh báo riêng](SECURITY.md), không đăng lên Issues công khai.
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
ngữ cảnh, candidate và bảo toàn nằm trong [hợp đồng Jev](references/typesafe-advisor.md).
Các nghiên cứu 001/002/005 vẫn là lịch sử, không phải runtime mới hoặc bằng chứng hiệu quả.

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
| [`ke-trai-nghiem`](profiles/blog-ca-nhan/styles/ke-trai-nghiem.md) | Blog, bài kể có người viết hiện diện | `blog-ca-nhan` |
| [`phoi-hop-cong-viec`](profiles/blog-ca-nhan/styles/phoi-hop-cong-viec.md) | Chat, bình luận và lời nhờ trong công việc | `blog-ca-nhan` |
| [`chuyen-mon-cong-khai`](profiles/blog-ca-nhan/styles/chuyen-mon-cong-khai.md) | LinkedIn, bài quan điểm hoặc chia sẻ chuyên môn | `blog-ca-nhan` |
| [`marketing-thuyet-phuc`](profiles/blog-ca-nhan/styles/marketing-thuyet-phuc.md) | Nội dung giới thiệu có mục tiêu và CTA thật | `blog-ca-nhan` |
| [`huong-dan-ky-thuat`](profiles/ky-thuat-doanh-nghiep/styles/huong-dan-ky-thuat.md) | README, văn xuôi API và hướng dẫn xử lý lỗi | `ky-thuat-doanh-nghiep` |
| [`van-hanh-doanh-nghiep`](profiles/ky-thuat-doanh-nghiep/styles/van-hanh-doanh-nghiep.md) | SOP, báo cáo, biên bản và bàn giao | `ky-thuat-doanh-nghiep` |
| [`hoc-thuat-phan-tich`](profiles/ky-thuat-doanh-nghiep/styles/hoc-thuat-phan-tich.md) | Giáo trình, đề án và nghiên cứu | `ky-thuat-doanh-nghiep` |

Card không phải khuôn để “làm màu” và không tự tạo lý do sửa. Yêu cầu hiện tại được ưu tiên;
ràng buộc thể loại và năm quy tắc chốt chặn vẫn giới hạn mọi thay đổi; mẫu/hồ sơ chỉ được dùng khi
đúng người, đúng phạm vi và có đặc tính ổn định. Chi tiết chuẩn nằm trong
`references/bo-giai-phong-cach.md`.

## Kiến trúc

`SKILL.md` là nguồn chuẩn. Các file còn lại bổ sung quy tắc theo thể loại, ví dụ hoặc dữ liệu bảo trì:

```text
SKILL.md                                      quy trình, V1–V25, T1–T6 và cách trả kết quả
profiles/blog-ca-nhan/rules.md                B1–B17 cho văn bản có giọng cá nhân
profiles/blog-ca-nhan/styles/                 bốn style card có tác giả hiện diện
profiles/ky-thuat-doanh-nghiep/rules.md       K1–K7 và giới hạn của văn kỹ thuật, học thuật
profiles/ky-thuat-doanh-nghiep/styles/        ba style card kỹ thuật, vận hành và học thuật
references/han-viet-thuan-viet.md             bảng tra và điều kiện phải giữ thuật ngữ
references/bang-tra-cuu.md                    bảng tra hư từ, loại từ, tiểu từ và câu hỏi chẩn đoán
references/bo-giai-phong-cach.md              bộ giải ngữ cảnh, precedence và registry đường dẫn
references/typesafe-advisor.md                workflow tự động, input và ranh giới Jev
calibration/LOG.md                            bằng chứng dùng để sửa quy tắc chung
calibration/ca-kiem-thu.md                    ca kiểm thử chạy tay cho từng pattern
agents/openai.yaml                            tên hiển thị và lời gọi mặc định
assets/                                       icon và wordmark SVG sáng/tối
.codex-plugin/plugin.json                     manifest và nhận diện plugin Codex
.plugin-skills/vietnamizer/SKILL.md          adapter source, nạp root SKILL.md; không sao chép rule
.claude-plugin/                              manifest và catalog Claude Code
.agents/plugins/marketplace.json             catalog Codex được track, không phải tooling sinh local
scripts/validate-package.py                   kiểm tra tính đồng bộ của gói
scripts/package-skill.sh                      tạo hai artifact cài đặt
scripts/package-plugin.py                     kiểm metadata và tạo ZIP plugin hai nền tảng
docs/plugin-distribution.md                   đường cài, kiểm thử và giới hạn publication
scripts/scan-tells.sh                         tìm những chỗ có thể rà bằng biểu thức chính quy
jev/                                         runner Python và registry 55 pattern
scripts/build-jev-registry.py                 sinh/kiểm registry từ nguồn canonical
.specify/                                     constitution, template và script của Spec Kit
specs/                                        đặc tả, checklist, plan và task theo từng feature
eval/guard/                                   hồ sơ corpus/config lịch sử đã ngừng dùng
```

Ngoài các file từ `.specify/` trở xuống, `docs/`, manifest source và adapter discovery
cũng phục vụ source hoặc phát triển, không nằm trong gói `vietnamizer.skill`.

Generated agent skills, Spec Kit integration state, raw run và scratch output được giữ local.
Xem [hướng dẫn đóng góp](CONTRIBUTING.md) để cài tooling maintainer và chạy kiểm tra offline.

Bộ giải phong cách dùng đúng bảy card trong bảng cách dùng ở trên. Nội dung chuẩn của từng card nằm
trong thư mục `styles/` của profile tương thích; `references/bo-giai-phong-cach.md` chỉ sở hữu cách
chọn card, thứ tự ưu tiên và registry đường dẫn.

Trước khi chạy pattern, skill kiểm tra thể loại. Pháp quy, hợp đồng, thơ, văn cổ phong và nghi lễ chỉ
được rà T1–T6. Code, schema, dữ liệu có cấu trúc, bảng tham số, trích dẫn nguyên văn, tên riêng và ví
dụ đang được bàn tới là vùng bảo toàn từng byte. Xem danh sách và ngoại lệ đầy đủ trong `SKILL.md`.

## Danh mục pattern

### Cách dùng từ và cấu trúc câu (V1–V25)

| # | Pattern | Ví dụ hoặc phép kiểm tra |
|---|---|---|
| V1 | Thiếu bổ ngữ kết quả và bổ ngữ hướng | *không giải quyết vấn đề* → *không giải quyết **được** vấn đề* khi ý là chưa thành công |
| V2 | Cặp liên từ bị thiếu từ ở vế sau | *Vì A, B* → *Vì A **nên** B* nếu câu cần nói rõ quan hệ nhân quả |
| V3 | Thiếu "là" trong câu định nghĩa hoặc lựa chọn | *Cách đơn giản nhất tăng worker* → *Cách đơn giản nhất **là** tăng worker* |
| V4 | Thiếu hoặc lạm dụng từ chỉ thời gian và trạng thái | Xem câu có cần *đã, đang, rồi, vẫn, chưa* để phân biệt diễn biến hay không |
| V5 | Thiếu hoặc sai loại từ | *nuôi ba mèo* → *nuôi ba **con** mèo* |
| V6 | Câu hỏi hoặc lời nhờ không đúng ý định giao tiếp | Phân biệt câu hỏi có hoặc không với câu hỏi cần nội dung cụ thể |
| V7 | "của" thừa trong cụm danh từ | *hiệu suất của hệ thống* → *hiệu suất hệ thống* nếu không có quan hệ sở hữu |
| V8 | "các" và "những" được thêm theo dấu số nhiều | Bỏ khi số nhiều đã rõ và phạm vi không đổi |
| V9 | Cụm giới từ dài do dịch sát | *trong quá trình kiểm tra* → *khi kiểm tra* nếu nghĩa giữ nguyên |
| V10 | Trạng ngữ đặt ở vị trí gây khó hiểu | Chuyển vị trí khi người đọc không biết trạng ngữ bổ nghĩa cho hành động nào |
| V11 | Câu dẫn không mang thêm thông tin | Bỏ *Điều quan trọng cần lưu ý là* nếu phần sau tự đứng được |
| V12 | Lặp từ nối ở đầu câu | Xem lại chuỗi câu cùng mở bằng *Ngoài ra, Tuy nhiên, Do đó* |
| V13 | Đoạn văn lặp cứng một kiểu mở câu | Chỉ sửa ở cấp đoạn khi khuôn lặp làm đứt mạch thông tin |
| V14 | Danh ngữ đứng riêng như một câu | *Một giải pháp linh hoạt cho nhiều kho.* → viết thành câu hoặc dùng làm heading đúng chức năng |
| V15 | Danh hoá thừa và động từ ít nội dung | *tiến hành thực hiện việc rà soát* → *rà soát* |
| V16 | Câu bị động dịch sát "được / bị ... bởi" | *được hoàn thành bởi phòng kế toán* → *phòng kế toán hoàn thành* khi tác nhân là trọng tâm |
| V17 | Dùng cụm dài thay cho "là" hoặc "có" | *đóng vai trò là trung tâm* → *là trung tâm* nếu không cần nhấn chức năng |
| V18 | Câu lồng nhiều tầng, "mà" và "điều này" không rõ | Tách câu nhưng giữ nguyên chủ thể và quan hệ nhân quả |
| V19 | Chêm tiếng Anh không hợp người đọc hoặc lĩnh vực | Giữ thuật ngữ theo cách dùng thật của cộng đồng, không tự thêm hoặc xoá đồng loạt |
| V20 | Từ hoặc cụm từ bị thiếu một tiếng | *đọc lên thấy hụt* → *đọc lên thấy **hụt hẫng*** khi đúng với ý câu |
| V21 | Tàn dư lượt hội thoại của trợ lý | *Chắc chắn rồi! Dưới đây là ba bước...* → *Ba bước triển khai...* |
| V22 | Rào trước về nguồn rồi đưa phỏng đoán | *Không có thông tin công bố. Nhiều khả năng công ty bắt đầu từ đầu những năm 2000.* → giữ điều nguồn nói, bỏ phần đoán |
| V23 | Phản biện một ý không có đối tượng | Bỏ vỏ *không ai phủ nhận...* khi mạch văn không có ý nào cần phản biện |
| V24 | Chồng từ chỉ khả năng cùng chức năng | *có khả năng có thể* → giữ một mức khả năng; không đụng các từ có phạm vi nghĩa khác nhau |
| V25 | Làm mơ hồ quan hệ đã có trong nguồn | Khôi phục *phụ thuộc ở runtime* thay vì *có quan hệ* khi nguồn trong phạm vi đã nêu rõ |

### Typography (T1–T6)

| # | Pattern |
|---|---|
| T1 | Viết hoa theo kiểu tiêu đề tiếng Anh |
| T2 | Em dash và gạch ngang chú thích giữa câu |
| T3 | Ngoặc kép không nhất quán |
| T4 | Dấu phẩy đứng trước "và" |
| T5 | Định dạng thay cho cấu trúc câu |
| T6 | Emoji |

Với văn xuôi thông thường, typography chỉ được sửa khi văn bản đồng thời có ít nhất một pattern
V1–V25. Thể loại được cổng đầu vào giới hạn ở T1–T6 là ngoại lệ; vùng bảo toàn vẫn giữ nguyên từng byte.

### Blog, bài cá nhân, nội dung công việc và marketing (B1–B17)

| # | Pattern |
|---|---|
| B1 | Sáo ngữ tôn vinh tầm quan trọng |
| B2 | Ẩn dụ có sẵn và thành ngữ dịch sát từ tiếng Anh |
| B3 | Mở bài dẫn dắt vòng vo |
| B4 | Kết bài lạc quan sáo rỗng |
| B5 | Song hành phủ định "không chỉ... mà còn" |
| B6 | Nghi vấn tu từ mở đoạn kiểu SEO |
| B7 | Tụng ca địa phương và doanh nghiệp |
| B8 | Danh xưng và thẩm quyền phóng đại |
| B9 | Hán-Việt hoá tên gọi đời thường |
| B10 | Thành ngữ dùng lệch và mật độ thành ngữ bất thường |
| B11 | Nhịp ba cân âm tiết và biền ngẫu giả |
| B12 | Cụm bốn âm tiết Hán-Việt tự chế |
| B13 | Nhịp câu đều đặn bất thường |
| B14 | Rụng tiểu từ tình thái cuối câu |
| B15 | Xưng hô lơ lửng và phẳng |
| B16 | Giả thân mật |
| B17 | Trộn mức độ trang trọng không chủ đích |

### Tài liệu kỹ thuật, doanh nghiệp và học thuật (K1–K7)

| # | Pattern |
|---|---|
| K1 | Viết theo diff thay vì mô tả hiện trạng |
| K2 | Sáo ngữ thể chế rỗng ngoài văn bản pháp quy |
| K3 | Bộ đề mục Hán-Việt đối xứng rỗng |
| K4 | Mô tả hiện tượng mà không đưa hiện tượng ra |
| K5 | Câu dẫn nhập rỗng sau đề mục |
| K6 | Siêu dữ liệu về quá trình tạo ra văn bản |
| K7 | Dẫn uy tín vô danh thay cho bằng chứng |

Profile này còn yêu cầu không thêm tiểu từ, ý kiến hoặc ngôi thứ nhất; không thay thuật ngữ chỉ để tránh lặp; không thuần Việt hoá thuật ngữ đã được định nghĩa.

## Những điểm khác với skill humanizer tiếng Anh

**Lặp từ không tự động là lỗi.** Trong tài liệu kỹ thuật, một thuật ngữ cần được gọi nhất quán. Ở văn xuôi, việc lặp danh từ cũng có thể giúp người đọc biết câu sau vẫn nói về cùng đối tượng. Chỉ thay khi bản thân từ đang sai hoặc chuỗi đồng nghĩa làm đối tượng bị đổi tên liên tục.

**En dash không bị cấm.** Dấu `–` có những chức năng hợp lệ trong tiếng Việt, như lời thoại, gạch đầu dòng, quan hệ giữa hai tên riêng và khoảng thời gian. T2 chỉ xem xét em dash `—` cùng các dấu ngang được dùng để chèn chú thích giữa câu.

**Ngoặc kép không bị ép về một hình dạng duy nhất.** Word, Google Docs và hệ điều hành có thể tự chuyển ngoặc thẳng thành ngoặc cong. T3 kiểm tra sự nhất quán trong cùng văn bản, không sửa theo sở thích của công cụ.

## Những khác biệt chính tả không dùng để suy đoán tác giả

Skill không tự động chọn giữa dấu thanh kiểu cũ và mới, như *hòa / hoà*, hoặc giữa *i / y*, như *kĩ / kỹ*. Đây là khác biệt chuẩn chính tả và quy ước xuất bản. Skill chỉ giữ cách viết nhất quán trong phạm vi văn bản, trừ khi người dùng yêu cầu theo một chuẩn cụ thể.

Khoảng trắng trước dấu câu, lỗi gõ và biến thể chính tả cũng không được dùng làm bằng chứng về tác giả. Có thể sửa chúng khi người dùng yêu cầu làm sạch văn bản, nhưng không suy ra ai đã viết.

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

## Mức độ tin cậy và nguồn

Mỗi quy tắc phải chỉ rõ nó dựa trên tài liệu, quan sát có bản đối chiếu trong `calibration/LOG.md` hay suy luận từ khác biệt giữa tiếng Anh và tiếng Việt. Repo chưa có bộ ngữ liệu đủ để đặt ngưỡng tần suất, nên số lần xuất hiện chỉ giúp tìm chỗ cần đọc lại.

### Nguồn quy phạm và học thuật

| Nguồn | Nội dung được dùng |
|---|---|
| [Nghị định 30/2020/NĐ-CP, Phụ lục II](https://thuvienphapluat.vn/chinh-sach-phap-luat-moi/vn/bieu-mau/55095/tong-hop-cac-phu-luc-ve-van-ban-hanh-chinh-moi-nhat-ban-hanh-kem-theo-nghi-dinh-30-2020) | Cách viết hoa tên cơ quan trong văn bản hành chính, dùng cho T1 |
| [Quyết định 1989/QĐ-BGDĐT năm 2018](https://thuvienphapluat.vn/van-ban/Giao-duc/Quyet-dinh-1989-QD-BGDDT-2018-quy-dinh-chinh-ta-Chuong-trinh-sach-giao-khoa-giao-duc-pho-thong-445355.aspx) | Điều 8 và 9, dùng để xác định phạm vi của dấu thanh và i/y |
| [ViDetect, arXiv:2405.03206](https://arxiv.org/abs/2405.03206) | Nghiên cứu phát hiện văn bản AI tiếng Việt; không dùng làm danh sách pattern ngôn ngữ |
| [VietBinoculars, arXiv:2509.26189](https://arxiv.org/abs/2509.26189) | Nghiên cứu phát hiện văn bản AI tiếng Việt; không dùng làm danh sách pattern ngôn ngữ |
| [A Survey on Zero Pronoun Translation, arXiv:2305.10196](https://arxiv.org/abs/2305.10196) | Tham khảo về lược đại từ và dịch thuật |
| [Nghiên cứu dịch câu bị động Anh–Việt](https://i-jte.org/index.php/journal/article/view/90) | Tham khảo cho V16; đối tượng nghiên cứu là người dịch |
| [Danh hoá động từ trong danh ngữ](https://tcgd.tapchigiaoduc.edu.vn/index.php/tapchi/article/view/4322) | Tham khảo cho V15 |
| [Cú pháp tiếng Việt nhìn từ ngữ pháp chức năng](https://vjol.info.vn/index.php/tdm/article/download/93747/79245/) | Tham khảo cho cấu trúc đề–thuyết ở V13 |
| [Tình thái từ](https://voer.edu.vn/c/tinh-thai-tu/4491bb06/712ccc96) và [tiểu từ tình thái trong hành động ngỏ lời](https://vusta.vn/mot-so-tieu-tu-tinh-thai-bieu-dat-tinh-lich-su-trong-hanh-dong-ngo-loi-bang-tieng-viet-p72715.html) | Tham khảo cho B14 |
| [Loại từ CON và CÁI](http://ngonngu.org/Con_Cai.htm) | Tham khảo cho V5 |

### Nguồn trình bày lại và nguồn cộng đồng

Những nguồn dưới đây giúp tìm thuật ngữ hoặc ghi nhận hiện tượng, không được dùng riêng làm căn cứ quy phạm:

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Wikipedia: Loại từ](https://vi.wikipedia.org/wiki/Lo%E1%BA%A1i_t%E1%BB%AB)
- [Wikipedia: Dấu gạch ngang](https://vi.wikipedia.org/wiki/D%E1%BA%A5u_g%E1%BA%A1ch_ngang)
- [Wikipedia: Dấu ngoặc kép](https://vi.wikipedia.org/wiki/D%E1%BA%A5u_ngo%E1%BA%B7c_k%C3%A9p)
- [Phân biệt gạch ngang và gạch nối, Giáo dục TP.HCM](https://giaoduc.edu.vn/phan-biet-dau-gach-ngang-va-gach-noi/)
- [Brands Vietnam: dấu hiệu nội dung viết bởi AI](https://help.brandsvietnam.com/vi/article/dau-hieu-nhan-biet-noi-dung-duoc-viet-boi-ai-3zy07d/)
- [Cặp quan hệ từ, HOCMAI](https://hoctot.hocmai.vn/dau-hieu-nhan-biet-quan-he-tu-va-cap-quan-he-tu.html)
- [Đề–thuyết, Ngày ngày viết chữ](https://ngayngayvietchu.com/thu-phan-tich-cau-tieng-viet-theo-cau-truc-de-thuyet/)

### Nguồn gợi ý giả thuyết

- [`blader/humanizer` 3.0.0](https://github.com/blader/humanizer/tree/v3.0.0) chỉ được dùng để nêu
  giả thuyết cho V23–V25, phần mở rộng B8 và K7. Quyết định tiếng Việt dựa trên các ca dương/âm và
  bằng chứng ghi ngày 28/09/2026 trong `calibration/LOG.md`; repo upstream không được coi là nguồn
  quy phạm tiếng Việt.

### Nguồn còn thiếu

- V3 và V13 cần thêm nguồn gốc về lý thuyết đề–thuyết thay cho các bài trình bày lại.
- V16 cần thêm nghiên cứu công bố trực tiếp về đối chiếu câu bị động Anh–Việt.

## Tác giả và ghi nhận

`vietnamizer` do Fioenix thiết kế và duy trì. Codex và Claude Code được dùng làm agent kỹ thuật để
hỗ trợ nghiên cứu, triển khai, kiểm thử và review.

Cách đóng gói và khung **Dấu hiệu / Vì sao / Sửa / Không flag** tham khảo
[blader/humanizer](https://github.com/blader/humanizer) cùng hướng dẫn của WikiProject AI Cleanup.
Các pattern tiếng Việt được xây dựng riêng cho repo này.

## Lịch sử phiên bản

- **0.10.6** (19/10/2026) – Cập nhật hướng dẫn cài đặt, kiểm thử và chuyển đổi hoặc hoàn tác sang
  catalog Codex dùng chung của Finolabs tại `fioenix/agybird` (`vietnamizer@agybird`, công bố từ
  `agybird` v0.2.1), đồng thời giữ catalog độc lập `vietnamizer@vietnamizer` để tương thích ngược.
  Không đổi quy tắc biên tập hay hành vi runtime.

- **0.10.5** – Tự tách đoạn/câu từ input nguồn, giữ vị trí và nguyên đoạn/ngữ cảnh;
  đối soát từng câu, pattern và rubric qua nhiều batch. CLI có `prepare` offline, contract v2 phân biệt
  đủ câu trả lời với đủ ngữ cảnh và kiểm đầy đủ; input `sections` cũ vẫn dùng được. Phần mơ hồ hoặc
  vượt giới hạn cục bộ/dịch vụ được báo riêng; không tăng quota hay tự quyết định edit.

- **0.10.0** – Thêm runner Jev 1.14 và registry 55 pattern: tự động thử khi host cấp key và quyền gửi,
  core độc lập khi không có key hoặc dịch vụ lỗi. Kiểm tra riêng từng candidate, giữ năm chốt chặn,
  coverage và trạng thái lỗi trung thực; không tự quyết định edit theo điểm số. Gói cài chứa cùng runtime.

- **0.9.8** – Chuẩn hóa base listing Codex bằng tiếng Anh, giữ bản dịch tiếng Việt và bổ sung
  liên kết hỗ trợ. Làm rõ workflow theo thể loại, ranh giới dữ liệu bị hạn chế và quyền riêng tư;
  phản hồi biên tập không tự cấp quyền ghi nhật ký hiệu chuẩn hoặc sửa skill. Thêm gate metadata
  chặn URL hỗ trợ không an toàn, nội dung vượt giới hạn và bản dịch không hợp lệ. Giữ branding,
  pattern và TypeSafe tùy chọn; phát hành gói không thay thế xét duyệt của Directory.
- **0.9.7** – Đưa `LICENSE` vào cả hai archive, giữ MIT notice cho tooling Spec Kit và chuyển
  generated Codex integration cùng state từng checkout ra khỏi Git tracking. Bổ sung ignore
  hẹp cho tooling local, environment, scratch output và cache; thêm hướng dẫn contributor cùng
  gate CI chặn file tracked bị ignore. Thêm icon SVG sáng/tối, metadata UI, catalog Codex và ZIP plugin chung với
  Claude Code; cả hai dùng một nguồn skill chuẩn. Bổ sung thông tin quyền riêng tư, điều kiện
  sử dụng và kiểm tra asset/metadata trước đóng gói.
  Đổi thương hiệu từ vi-humanizer sang Vietnamizer, đồng bộ định danh skill/plugin/catalog,
  repo và tên gói tải thành `vietnamizer`. Quy tắc biên tập giữ nguyên. Loại CLI advisor khỏi
  ba archive và repo, cùng harness, kiểm thử và dependency SDK của nó; TypeSafe chỉ được tận
  dụng qua skill chính chủ đã có khi hữu ích và người dùng đồng ý gửi dữ liệu. Bỏ tự truy xuất/lưu hồ sơ memory; ảnh README
  dùng Markdown, giữ SVG nền trong suốt và hai biến thể violet/mint đã duyệt.
- **0.9.6** – Đóng gói optional TypeSafe advisor CLI cho host local: probe thật mới xác nhận
  readiness, assess/rank chỉ trả typed signal cho lát cắt V20, còn host Agent giữ quyền quyết định
  và viết câu cuối. Core vẫn chạy không key, không mạng và không SDK; cả `.skill` lẫn ZIP Claude
  Org chứa adapter nhưng không chứa secret hoặc mạo nhận capability của host. README đưa ba ví dụ
  đã hiệu chỉnh và các đường cài trực tiếp từ artifact phát hành lên đầu trang.
- **0.9.5** – Tổ chức hai base profile thành thư mục cha–con: `rules.md` giữ B/K pattern, còn bảy
  style card nằm trong `styles/` của profile tương thích. Gói Claude Org nay hiển thị riêng từng
  phong cách; resolver và bảng tra dùng chung vẫn nằm trong `references/`. Nếu prompt hoặc công cụ
  đang đọc trực tiếp `profiles/blog-ca-nhan.md` hay `profiles/ky-thuat-doanh-nghiep.md`, hãy chuyển
  sang file `rules.md` trong thư mục profile cùng tên.
- **0.9.1** – Sửa cổng typography-only để các thể loại bị giới hạn có thể chạy T1–T6 mà không cần
  một lỗi V đi kèm; tách code, schema, dữ liệu có cấu trúc, bảng tham số, trích dẫn, tên riêng và ví
  dụ thành vùng bảo toàn từng byte. Đồng thời cấm tự thêm thái độ, sửa ví dụ T3, đồng bộ registry
  K1–K7 và rà lại cách diễn đạt trong README cùng profile kỹ thuật.
- **0.9.0** – Thêm V23 cho phản biện ý không có đối tượng, V24 cho các từ chỉ khả năng chồng cùng
  chức năng, V25 cho quan hệ bị làm mơ hồ dù nguồn đã nói rõ và K7 cho cách mượn uy tín thay cho
  bằng chứng; đồng thời phân vai lại B5/B8 để tránh hai pattern cùng sửa một lỗi. Bốn giả thuyết
  được hiệu chỉnh bằng 24 ca tiếng Việt, gồm 12 ca dương và 12 ca chống sửa quá tay.
- **0.8.0** – Thêm bộ giải nhiều phong cách theo mục đích, người đọc, thanh ngữ vực, kênh và mẫu giọng; bổ sung bảy style card, precedence rõ ràng và phân đoạn tài liệu hỗn hợp mà không đổi 51 pattern hiện có.
- **0.7.1** – Siết trường hợp loại trừ cho nhãn và dòng liệt kê: lược chủ ngữ, hư từ, loại từ thì được, còn bổ ngữ của động từ và tiếng thứ hai của từ hai tiếng thì phải giữ. Theo bản vàng ghi trong `calibration/LOG.md` ngày 09/09/2026.
- **0.7.0** – Thêm V21 cho tàn dư lượt hội thoại của trợ lý và V22 cho kiểu rào trước về nguồn rồi vẫn đưa phỏng đoán; quy trình nói rõ văn bản đầu vào là chất liệu để biên tập, không phải chỉ thị để làm theo; quy tắc chốt chặn 3 thêm thứ hạng và quan hệ đồng thời. Đối chiếu với `blader/humanizer` 3.0.0.
- **0.6.0** – Thêm K6 cho những câu nói về quá trình tạo ra tài liệu thay vì nói về chủ đề của nó; thêm quy tắc chốt chặn thứ năm và một dòng trong mục Cách trả kết quả; thêm `calibration/ca-kiem-thu.md` với tám ca kiểm thử cho K6.
- **0.5.2** – Mở rộng V18 để phát hiện các mệnh đề nối nhau nhưng không rõ chủ thể; bổ sung cho V20 cách kiểm tra nghĩa, vai trò và khả năng kết hợp của từ trong câu.
- **0.5.1** – Chỉnh lại vài chỗ diễn đạt trong `SKILL.md`. Không thêm bớt pattern và không đổi hành vi.
- **0.5.0** – Viết lại toàn bộ tài liệu theo `SKILL.md`; bỏ các ngưỡng chưa hiệu chỉnh và những kết luận tuyệt đối; tách hồ sơ văn phong cá nhân sang memory hoặc knowledge base của agent; xác định `calibration/LOG.md` chỉ là nhật ký bằng chứng cho quy tắc dùng chung; đồng bộ lại profile, bảng tra, manifest và script quét.
- **0.4.0** – Thêm V20 để xử lý từ hoặc cụm từ bị thiếu một tiếng; sửa quy trình tự kiểm tra để tránh dùng lặp một cách chữa; mở rộng giao thức tiếp nhận quy tắc tiếng Việt do người bản ngữ nêu ra.
- **0.3.0** – Viết lại phần mở đầu README; bổ sung K4 về đoạn giải thích thiếu ví dụ và đổi pattern câu dẫn nhập thành K5.
- **0.2.2** – Mở rộng T4 cho dấu phẩy đứng trước *và*; thêm `scripts/scan-tells.sh`.
- **0.2.1** – Tự áp skill lên README; sửa lỗi diễn đạt và đồng bộ phần mô tả cấu trúc repo.
- **0.2.0** – Thêm giao thức hiệu chuẩn bằng phản hồi thực tế và `calibration/LOG.md`.
- **0.1.1** – Bổ sung các trường hợp loại trừ cho văn bản doanh nghiệp và thuật ngữ nội bộ.
- **0.1.0** – Bản đầu gồm V1–V19, T1–T6, B1–B17, K1–K4 và hai file tham chiếu.

## Giấy phép

MIT
