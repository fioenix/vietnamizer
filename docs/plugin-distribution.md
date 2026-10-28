# Phân phối plugin vietnamizer

## Trạng thái OpenAI ngày 23/10/2026

Owner báo portal hiển thị “We are not accepting more skills-only submissions at this time.”
Tạm dừng chuẩn bị gửi Vietnamizer theo đường skills-only; thông báo chưa được kiểm độc lập và
không xác lập lệnh cấm toàn cầu hoặc vĩnh viễn. Hỗ trợ định dạng, cài từ catalog riêng, portal
nhận hồ sơ và Directory approval là các trạng thái riêng. Xem
[bằng chứng và điều kiện tiếp tục](openai-marketplace-assessment-2026-10-23.md).

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
Kit, generated maintainer skills, corpus evaluation hoặc credential.

Trước khi chạy script, sao lưu các archive hiện có và SHA-256 vào một thư mục local mới trong
`output/`. Script thay thế các tên cố định trong `dist/`; nó không giữ lịch sử thay cho maintainer.
README và `docs/` không nằm trong payload. Chỉ sửa tài liệu ngoài payload thì giữ archive hiện có;
sửa tài liệu trong payload phải dựng lại rồi đối chiếu inventory, CRC, version và bytes với source.

Từ v0.10.5, runtime có thêm `preparation.py` và `coverage.py`: mọi archive
phải chạy `prepare` offline và có bytes khớp source, ngoài kiểm no-key `evaluate`. Contract v2 giữ
input cũ nhưng full evaluation đòi hỏi ranh giới/ngữ cảnh/công việc hoàn tất; đủ answer không tự
chứng minh đủ context. Thay đổi source không tự cập nhật cache hoặc skill dùng chung.

Từ v0.10.0, cả ba archive chứa cùng runner Python standard library và registry 55 pattern trong
`jev/`. Host có key được inject và quyền gửi dữ liệu thì phải thử đánh giá qua Jev 1.14; không có
key thì giữ workflow Markdown offline. Runner mới không dùng SDK hay mã từ các nghiên cứu
001/002/005 đã dừng. Hợp đồng input, coverage, lỗi và quyền gửi nằm trong
[typesafe-advisor.md](../references/typesafe-advisor.md).

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

`--check` không dựng archive. Cần kiểm thêm đường cài trên profile tạm: với môi trường mới chưa có
đăng ký `agybird` cũ, có thể đăng ký marketplace từ `fioenix/agybird` hoặc bản clone cục bộ đã có
`"name": "Finolabs"` (`displayName` là `Finolabs`) rồi cài `vietnamizer@Finolabs`; với đường tương
thích ngược độc lập tại repo này, đăng ký clone `vietnamizer` và cài `vietnamizer@vietnamizer`. Ở
cả hai đường, kiểm plugin cache có manifest đúng version và skill nạp đúng tên. Khi chuyển từ bản
dùng chung cũ `@agybird` (từ catalog `agybird` `v0.2.1` ban đầu) sang `@Finolabs`, không dùng lệnh
`upgrade` trên `agybird` để đổi tên (vì `marketplace_upgrade.rs` từ chối khi `marketplace.name`
tải về khác tên đã cấu hình) và không chạy lại `marketplace add` cùng URL Git `fioenix/agybird`
trước khi gỡ nguồn cũ (vì có thể tái sử dụng nguồn `agybird` cũ). Thay vào đó, sao lưu cấu
hình/trạng thái đăng ký trước, dùng một bản clone/checkout cục bộ riêng của `fioenix/agybird` đã
cập nhật `"name": "Finolabs"` (ví dụ `git clone https://github.com/fioenix/agybird.git /path/to/finolabs-catalog`)
để đăng ký marketplace `Finolabs` song song (side-by-side) với `agybird` cũ đã đăng ký qua Git, cài
và xác nhận các plugin `@Finolabs` liên quan (`agybird@Finolabs`, `vietnamizer@Finolabs`,
`markmap-skills@Finolabs`) hoạt động trước, rồi mới gỡ các selector `@agybird` cũ và marketplace
`agybird` cũ bằng lệnh CLI được hỗ trợ; giữ đăng ký từ bản clone cục bộ là đủ dùng, không suy đoán
cơ chế thay thế tại chỗ sang URL Git từ xa. Nếu cần rollback thì khôi phục từ bản sao lưu, dùng
checkout `fioenix/agybird` tại tag `v0.2.1` (`@agybird`) hoặc đăng ký lại nguồn độc lập
`vietnamizer` (`vietnamizer@vietnamizer`), không xóa dữ liệu không thể khôi phục. Với Codex có thể
dùng app-server `skills/list` để kiểm discovery mà không gọi model. Với Claude Code, cài xong mở
session mới và kiểm `/vietnamizer:vietnamizer`; metadata validator, việc sửa tài liệu hoặc thông
báo install thành công không tự chứng minh UI đã hiển thị, đã gom nhóm theo `Finolabs` hay
invocation chạy được.

Không đưa credential hoặc raw input của người dùng vào log kiểm. Profile thật của maintainer
không phải fixture kiểm thử. Các lệnh kiểm packaging ở trên chạy offline, không cần gọi TypeSafe.
Live smoke riêng phải có quyền gửi, dùng dữ liệu tổng hợp và credential injection đã được host
cho phép. Chạy từ gói đã giải nén, đối chiếu bytes runtime với source, xác nhận model thực và
coverage. Smoke thành công không chứng minh chất lượng biên tập tiếng Việt hay plugin đã nạp
trong UI của mọi client.

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

Không ghi đè archive của phiên bản đã công bố bằng candidate mới. Kiểm gói mới, tích hợp source và phát
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

Catalog Codex dùng chung của Finolabs nằm tại `fioenix/agybird` với tên máy đúng chữ hoa–thường
`Finolabs` và `displayName` là `Finolabs`, gồm ba mục `agybird@Finolabs`, `vietnamizer@Finolabs`
và `markmap-skills@Finolabs` (hiệu chỉnh từ bản catalog dùng chung đầu tiên ở `agybird` v0.2.1
vốn dùng tên máy `agybird`; có thể đăng ký từ GitHub hoặc bản clone cục bộ). Trong repo này,
`.agents/plugins/marketplace.json` được giữ nguyên làm catalog độc lập một entry (`vietnamizer`,
`displayName` là `Vietnamizer`) để tương thích ngược với `vietnamizer@vietnamizer` và đáp ứng
kiểm tra của `scripts/package-plugin.py`; không đổi tên thành `Finolabs` và không nhân bản
catalog ba mục tại đây. `.claude-plugin/marketplace.json` tiếp tục phục vụ Claude Code. Các
catalog do maintainer kiểm soát giúp người dùng đăng ký nguồn và cài plugin, nhưng không phải
dấu hiệu OpenAI hoặc Anthropic đã review hay bảo chứng plugin.

Gửi vào directory chính thức là bước riêng. Với OpenAI, chỉ tiếp tục sau khi có bằng chứng portal
nhận hồ sơ này hoặc xác nhận phù hợp từ OpenAI, kiểm lại yêu cầu hiện hành, quyền publisher và
owner duyệt lần gửi cụ thể. Local validation không gỡ chặn intake. Không tạo MCP server, auth flow,
screenshots giả hoặc capability không có thật chỉ để lấp trường metadata.

Việc gửi Anthropic đang tạm dừng theo quyết định của owner ngày 04/10/2026. Người dùng vẫn có
thể [tự thêm marketplace của repo hoặc upload plugin](installation.md#claude-web-và-claude-desktop-thêm-marketplace)
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
