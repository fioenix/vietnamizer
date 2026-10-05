# Phân phối plugin vietnamizer

Bằng chứng kiểm tên mới: [rename-vietnamizer-2026-10-03.md](rename-vietnamizer-2026-10-03.md).
Báo cáo [plugin-readiness-2026-10-03.md](plugin-readiness-2026-10-03.md) ghi snapshot tên cũ trước migration.

## Một nội dung, nhiều đường cài

Root `SKILL.md` là nguồn chuẩn. Manifest source của Codex và Claude Code trỏ tới adapter mỏng
trong `.plugin-skills/`; adapter nạp file chuẩn và resolve resource từ root plugin. Gói plugin
được sinh với layout `skills/vietnamizer/`, manifest trỏ tới `./skills/`. Không commit bản skill
thứ hai. Các file trong `agents/` và `assets/` đi cùng skill để UI không mất icon khi cài riêng.

| Artifact | Mục đích | Layout |
|---|---|---|
| `vietnamizer.skill` | Custom skill và cài skill thông thường | `vietnamizer/SKILL.md` |
| `vietnamizer-claude-org.zip` | Upload skill vào Claude Org | `SKILL.md` ở root |
| `vietnamizer-plugin.zip` | Gói plugin Codex/Claude Code | Hai manifest, một `skills/vietnamizer/SKILL.md` |

Tạo cả ba artifact bằng `python3 scripts/package-plugin.py`. `dist/` là output sinh ra, không
commit. Plugin ZIP chỉ chứa public payload, MIT notice, nhận diện và manifest; không chứa Spec
Kit, generated maintainer skills, CLI advisor, corpus evaluation hoặc credential.

Từ v0.9.7, repo cũng không còn advisor, SDK hoặc evaluation harness TypeSafe. Hướng dẫn
được đóng gói chỉ mô tả cách tận dụng skill chính chủ đã có khi hữu ích và có quyền gửi dữ liệu.

Catalog source trỏ tới root repo, vẫn gồm tooling maintainer và hồ sơ lịch sử. Validator local
và inventory ZIP không thay thế portal Validate cho commit GitHub thực tế; không suy ra directory
approval hoặc bắt buộc tách repo chỉ từ kết quả đóng gói.

## Kiểm từ clone trước khi phát hành

```bash
python3 scripts/validate-package.py
python3 scripts/package-plugin.py --check
python3 scripts/package-plugin.py
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json --strict
npx --yes skills@1.5.20 add . --list
```

`--check` không dựng archive. Cần kiểm thêm đường cài trên profile tạm: thêm marketplace từ
clone, cài `vietnamizer@vietnamizer`, kiểm plugin cache có manifest đúng version và skill nạp
đúng tên. Với Codex có thể dùng app-server `skills/list` để kiểm discovery mà không gọi model.
Với Claude Code, cài xong mở session mới và kiểm `/vietnamizer:vietnamizer`; metadata validator
hoặc thông báo install thành công không tự chứng minh UI đã hiển thị hay invocation chạy được.

Không đưa credential hoặc raw input của người dùng vào log kiểm. Profile thật của maintainer
không phải fixture kiểm thử. Không gọi dịch vụ TypeSafe chỉ để kiểm plugin packaging.

## Nhận diện và listing

Nguồn chuẩn: [Plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines)
và [Submit plugins](https://developers.openai.com/plugins/deploy/submission).

Base subtitle và description Codex dùng tiếng Anh theo hướng dẫn submission. Bản dịch tiếng
Việt nằm trong `extensions.com.openai.publication.translations`; importer hiện giữ bản dịch
nhưng chưa dùng chúng để đổi nội dung Directory hiển thị. Skill và listing Claude vẫn dùng
tiếng Việt. Giữ category `Productivity`: mô tả rõ biên tập tài liệu, tin nhắn và bản dịch theo
thể loại, không chỉ nêu một lời hứa “tự nhiên hơn”. Không bảo đảm category sẽ được chấp thuận.

Gate riêng của repo yêu cầu đủ URL website, hỗ trợ, privacy và terms với HTTPS, không chứa
credential. Đây là tiêu chuẩn phân phối của Vietnamizer; không phải khẳng định schema bắt
buộc cả bốn URL đối với mọi skills-only plugin. Kiểm riêng nội dung tiếng Anh và quyền sử dụng
tài sản khi review; validator không suy ra được hai điều này từ định dạng.

Không ghi đè gói 0.9.7 đã công bố bằng candidate 0.9.8. Kiểm gói mới, tích hợp source và phát
hành phiên bản mới trước khi dùng nó để cập nhật listing. Scan, publisher verification và
eligibility trên portal là các cổng riêng, không được thay bằng kết quả kiểm offline.

Icon là chữ `ă` vẽ bằng hình học SVG, không phụ thuộc font hoặc ảnh bên ngoài. Bản sáng/tối có
viewBox vuông 128×128; wordmark dùng cho README/giới thiệu, không thay icon listing vuông.
Màu dùng các token FINOLABS đã duyệt: `fn-violet` (`#9750C4`), `fn-mint` (`#7FE2CE`),
`ink-900` (`#0B0B17`), `ink-50` (`#F7F7FB`), `ink-300` (`#BCBCD0`) và `ink-500` (`#5B5B79`).
Icon có nền trong suốt: bản sáng dùng violet, bản tối dùng mint. Metadata Codex dùng violet
cho `brandColor` và mint cho `brandColorDark`; skill UI dùng violet cho trường màu duy nhất. SVG/JSON/YAML
chứa giá trị token được xuất cố định để gói cài không phụ thuộc CSS hoặc repo FINOLABS bên ngoài.
Hai wordmark `assets/wordmark.svg` và `assets/wordmark-dark.svg` có nền trong suốt;
chữ `ă` dùng violet FINOLABS `#9750C4` ở bản sáng và mint `#7FE2CE` ở bản tối,
không dùng gradient ở cả hai chế độ.
Tên và tagline dùng màu chữ trung tính phù hợp từng chế độ. SVG không tải tài nguyên bên ngoài.
Metadata Codex có logo, composer icon, màu và starter prompts; metadata Claude có icon cùng
đường dẫn tài liệu, hỗ trợ, quyền riêng tư và điều kiện sử dụng. Các URL `main` chỉ có nội dung
public sau khi thay đổi tương ứng đã merge.

## Repo marketplace không phải directory chính thức

### Mở đường hỗ trợ trước khi đón người dùng

Hai manifest dùng cùng URL hỗ trợ `https://github.com/fioenix/vietnamizer/issues`. Không thay
URL này bằng email hoặc địa chỉ chưa xác minh. Tại lần kiểm tra ngày 05/10/2026, GitHub API trả
`has_issues: true`; Private Vulnerability Reporting trả `enabled: true` và trang Advisories
hiển thị **Report a vulnerability**. Đây là trạng thái tại thời điểm kiểm, cần đọc lại trước
khi công bố tài liệu hỗ trợ.

Chủ repo cần thực hiện:

1. Giữ **Issues** bật trong **Settings → General → Features** của `fioenix/vietnamizer`.
2. Sau khi thay đổi tài liệu/template được tích hợp, mở **Issues → New issue** và kiểm mẫu
   báo lỗi; kiểm link support của cả hai manifest tới đúng repo. `config.yml` chỉ cấu hình
   mẫu và đường báo riêng, không bật tính năng Issues.
3. Giữ Private Vulnerability Reporting đang bật. Trong **Security → Advisories**, kiểm
   **Report a vulnerability**. Nếu bị tắt, chủ repo mở **Settings → Advanced Security →
   Private vulnerability reporting → Enable** trước khi công bố kênh đó.
4. Kiểm người chịu trách nhiệm nhận báo cáo và cấu hình **Watch → Custom → Security alerts**
   cùng tùy chọn thông báo của tài khoản. Việc bật kênh không chứng minh thông báo đã tới người
   phụ trách; không gửi báo cáo giả chỉ để kiểm. Không cam kết SLA khi chưa có quyết định.

Xem [SECURITY.md](../SECURITY.md) và
[hướng dẫn GitHub về báo lỗi riêng](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository).
Các bước này không cấp quyền cho agent đổi settings, push hay submit lại plugin.

Tài liệu và template hỗ trợ không nằm trong payload do scripts đóng gói hiện tại tạo ra.
Đối chiếu ZIP public/local không chứng minh đó là đúng byte của submission OpenAI; cần bản
submit hoặc checksum từ nguồn được xác nhận mới kết luận được. Không suy ra thiếu đường hỗ trợ
là nguyên nhân chậm duyệt.

`.agents/plugins/marketplace.json` và `.claude-plugin/marketplace.json` là catalog do maintainer
kiểm soát. Người dùng có thể đăng ký repo và cài plugin; đây không phải dấu hiệu OpenAI hoặc
Anthropic đã review hay bảo chứng plugin.

Gửi vào directory chính thức là bước riêng, cần quyền tài khoản publisher, kiểm lại yêu cầu
submission tại thời điểm gửi và owner duyệt trước khi nộp. Không tạo MCP server, auth flow,
screenshots giả hoặc capability không có thật chỉ để lấp trường metadata.

Việc gửi Anthropic đang tạm dừng theo quyết định của owner ngày 04/10/2026. Người dùng vẫn có
thể [tự thêm marketplace của repo hoặc upload plugin](../README.md#claude-web-và-claude-desktop-thêm-marketplace)
theo gói và chính sách của Claude; không cần chờ listing chính thức.

Khi tiếp tục gửi Anthropic, dùng [developer portal](https://claude.ai/directory/manage) và chọn
**Plugin bundle** từ repository GitHub; ZIP ở Releases chỉ phục vụ cài/review riêng.
Directory đọc README ở root plugin làm mô tả listing. Chọn đúng tổ chức sở hữu trước khi tạo
hồ sơ; không suy ra publisher từ tài khoản đang đăng nhập. Rà
[checklist Claude](claude-marketplace-checks.md) để chuẩn bị dữ liệu, prompt và cổng xác nhận.

Nguồn định dạng:

- [OpenAI: plugin package và marketplace](https://developers.openai.com/plugins/build/plugins).
- [OpenAI: listing metadata và icon](https://developers.openai.com/plugins/deploy/submission).
- [Claude Code: plugin manifest](https://code.claude.com/docs/en/plugins-reference).
