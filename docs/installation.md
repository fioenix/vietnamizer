# Cài đặt Vietnamizer

[← README](../README.md)

## Cài nhanh

Tên mới từ bản **0.9.7**: Vietnamizer, định danh `vietnamizer` (trước đây là
`vi-humanizer`). Bản hiện tại là **0.13.3**, giữ nghĩa trước rồi chọn nét giọng theo chức năng từng phần; câu hỏi, đề mục, đại từ và danh sách được chọn theo việc chúng giúp người đọc làm gì. Các chốt giữ ý định, đối tượng lược, nhịp dấu câu, vùng bảo toàn và tư vấn Jev vẫn áp dụng. Runner Jev đọc trọn ghi chú Markdown dài, dùng
số lượt gọi theo thứ tự ưu tiên và không hỏi những câu mà chính quy tắc đã trả lời. Jev vẫn chỉ chạy
khi host cấp key và quyền gửi dữ liệu. Phát hành trên GitHub không có nghĩa là Directory đã chấp thuận.
Asset của các release trước 0.9.7 vẫn mang tên
`vi-humanizer.*` và chứa định danh cũ.
Xem [hướng dẫn chuyển tên](../docs/rename-vietnamizer-2026-10-03.md).

**OpenAI Marketplace, cập nhật 23/10/2026:** owner báo portal hiển thị “We are not accepting more
skills-only submissions at this time.” Vietnamizer giữ gói skills-only; việc chuẩn bị gửi OpenAI
đang tạm dừng theo bằng chứng intake này. Tài liệu OpenAI vẫn hỗ trợ định dạng skills-only nhưng
không chứng minh tài khoản được nhận hồ sơ hoặc plugin được Directory chấp thuận. Chưa kiểm độc
lập thông báo trên portal; không suy thành chính sách toàn cầu hoặc vĩnh viễn. Các đường cài từ
repo và gói riêng vẫn tách biệt với việc duyệt Directory. Xem
[bằng chứng, điều kiện tiếp tục và đánh giá MCP](../docs/openai-marketplace-assessment-2026-10-23.md).

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
[checklist gửi Anthropic](../docs/claude-marketplace-checks.md) để dùng khi tiếp tục.

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

Catalog Codex dùng chung của Finolabs đặt tại nguồn `fioenix/agybird` với tên máy
(`marketplace.name`) phân biệt hoa–thường là `Finolabs` và `displayName` là `Finolabs` (đã hiệu
chỉnh từ bản catalog dùng chung đầu tiên ở `agybird` `v0.2.1` vốn đặt tên máy là `agybird`).
Catalog này gồm ba mục `agybird@Finolabs`, `vietnamizer@Finolabs` và `markmap-skills@Finolabs`.

Với máy **chưa từng đăng ký** nguồn `agybird` cũ, có thể đăng ký trực tiếp từ GitHub rồi cài
`vietnamizer@Finolabs`:

```bash
codex plugin marketplace add fioenix/agybird
codex plugin add vietnamizer@Finolabs
```

Hoặc đăng ký từ một bản checkout/clone cục bộ của `fioenix/agybird` đã có `"name": "Finolabs"`:

```bash
codex plugin marketplace add /path/to/finolabs-catalog
codex plugin add vietnamizer@Finolabs
```

Repo này vẫn giữ `.agents/plugins/marketplace.json` độc lập (tên máy `vietnamizer`,
`displayName` là `Vietnamizer`) để tương thích ngược và phục vụ kiểm tra gói tại chỗ:

```bash
codex plugin marketplace add fioenix/vietnamizer
codex plugin add vietnamizer@vietnamizer
```

**Chuyển từ `@agybird` (`vietnamizer@agybird`) hoặc `vietnamizer@vietnamizer` sang `vietnamizer@Finolabs` và hoàn tác (rollback):**
trong Codex (`marketplace_upgrade.rs`), lệnh `upgrade` sẽ báo lỗi khi `marketplace.name` tải về
(`Finolabs`) khác với tên đã cấu hình (`agybird`), còn chạy lại `marketplace add` cùng URL Git
`fioenix/agybird` trước khi gỡ đăng ký cũ có thể tái sử dụng lại nguồn `agybird` cũ. Vì vậy,
không dùng lệnh `upgrade` trên `agybird` để đổi tên marketplace và không thêm đè cùng URL Git khi
nguồn `agybird` cũ vẫn còn. Hãy làm theo thứ tự song song (side-by-side) sau:

1. Sao lưu cấu hình và trạng thái đăng ký plugin/marketplace hiện tại của Codex.
2. Chuẩn bị một bản clone/checkout cục bộ riêng của `fioenix/agybird` đã cập nhật (ví dụ
   `git clone https://github.com/fioenix/agybird.git /path/to/finolabs-catalog`), kiểm tra
   `.agents/plugins/marketplace.json` tại đó có `"name": "Finolabs"`, rồi đăng ký đường dẫn cục bộ
   này để tạo marketplace `Finolabs` song song với `agybird` cũ:
   ```bash
   codex plugin marketplace add /path/to/finolabs-catalog
   codex plugin add vietnamizer@Finolabs
   ```
   (Nếu máy đang dùng cả bộ ba trong catalog dùng chung, cài luôn `agybird@Finolabs` và
   `markmap-skills@Finolabs` ở bước này.)
3. Xác nhận `vietnamizer@Finolabs` (cùng các plugin `@Finolabs` liên quan) đã cài và nạp đúng
   trước khi dọn nguồn cũ.
4. Dùng lệnh CLI được hỗ trợ để gỡ các selector `@agybird` cũ (`vietnamizer@agybird`, v.v.) và gỡ
   marketplace `agybird` cũ (hoặc `vietnamizer@vietnamizer` / marketplace `vietnamizer` nếu chuyển
   từ bản độc lập). Giữ nguyên đăng ký từ bản clone cục bộ là đủ để sử dụng; không giả định cơ chế
   thay thế tại chỗ sang URL Git từ xa nếu client chưa hỗ trợ.

Nếu cần hoàn tác (rollback), khôi phục từ bản sao lưu ban đầu, hoặc checkout `fioenix/agybird` tại
tag cố định `v0.2.1` (nơi `marketplace.name` vẫn là `agybird`) để đăng ký lại `vietnamizer@agybird`,
hoặc dùng nguồn độc lập `fioenix/vietnamizer` với `vietnamizer@vietnamizer`.

Khả năng hiển thị tên nguồn `Finolabs` hoặc `Vietnamizer` và cách gom nhóm trong trang Plugins
phụ thuộc từng bản client Codex; tài liệu này không khẳng định client đã tự gom nhóm trên UI
hoặc đã cài đặt thực tế. Skills CLI ở trên vẫn là đường cài độc lập. Catalog của repo không đồng
nghĩa plugin đã được duyệt vào directory chính thức của OpenAI hoặc Anthropic.

Xem [hướng dẫn phân phối và kiểm thử](../docs/plugin-distribution.md),
[quyền riêng tư](../PRIVACY.md) và [điều kiện sử dụng](../TERMS.md).

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
Đây là gói để cài và kiểm tra riêng, không phải xác nhận OpenAI đang nhận submission.
Trước khi dựng lại, giữ bản sao và SHA-256 của archive bị thay thế; không dùng candidate local
cùng version để ghi đè asset đã phát hành. Xem [quy trình đóng gói](../docs/plugin-distribution.md).

### Cài thủ công

Chép `LICENSE`, `SKILL.md` cùng `profiles/`, `references/`, `calibration/`, `agents/`, `assets/` và `jev/` vào
thư mục skill của agent:

```bash
git clone https://github.com/fioenix/vietnamizer.git /duong/dan/toi/skills/vietnamizer
```
