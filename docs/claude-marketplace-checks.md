# Kiểm Vietnamizer trước khi gửi directory Claude

**Tạm dừng gửi duyệt theo quyết định của owner ngày 04/10/2026.** Owner không tiếp tục bước
đăng ký gói trả phí để submit lúc này. Tập trung phân phối qua marketplace của repo và gói
upload; xem [hướng dẫn tự cài](../README.md#claude-web-và-claude-desktop-thêm-marketplace).
Checklist dưới đây là tài liệu tham khảo khi mở lại việc gửi duyệt, không phải công việc đang chạy.

Đường cài marketplace riêng không đồng nghĩa được Anthropic niêm yết. Chạy CLI validator,
kiểm archive và cài sạch trước; portal Validate vẫn là cổng riêng cho đúng commit được gửi.

Rà lại ngày 04/10/2026. Lượt này chuẩn bị source và hồ sơ, chưa submit hoặc chấp nhận điều
khoản thay owner. Không thay quy tắc biên tập, manifest hoặc tài sản 0.9.8 đã phát hành.

## Nguồn và quyền sở hữu listing

- Portal: [claude.ai/directory/manage](https://claude.ai/directory/manage).
- Loại: **Plugin bundle**, không phải MCP connector.
- Repository: `https://github.com/fioenix/vietnamizer`.
- Plugin path: để trống vì manifest ở root repo.
- Branch/tag: chọn nguồn đã tích hợp. `v0.9.8` giữ commit phát hành cũ; `main` nhận commit
  mới. Không bật auto-publish hoặc tạo webhook trong lượt chuẩn bị này.
- Chọn tài khoản/tổ chức sở hữu lâu dài trước khi tạo hồ sơ; nối GitHub trong chính tổ chức
  đó với quyền push. Không dùng tổ chức đang đăng nhập làm mặc định.

Theo [publish](https://claude.com/docs/directory/publish) và
[submit](https://claude.com/docs/plugins/submit), directory lấy plugin từ GitHub, không lấy
ZIP release làm nguồn. Kiểm đúng tổ chức trước: tổ chức nộp đầu tiên giữ listing của folder.
Nếu thay payload/manifest/asset, cần release mới; không ghi đè archive đã công bố.

## Trạng thái nguồn

Repo và ba archive 0.9.8 không còn mã advisor, SDK hoặc harness TypeSafe. Root source vẫn có
tooling maintainer và hồ sơ lịch sử; cần review đúng commit GitHub trong portal trước khi gửi.
Không suy ra approval chỉ từ validator CLI hoặc archive đã qua kiểm tra.

Trước Validate, kiểm toàn bộ source được track: tên/kích thước/loại file, symlink/submodule,
file hệ điều hành, `.gitattributes`, credential, component path và README/license. Đây là
kiểm source, khác với inventory ZIP. Chạy và lưu revision, lệnh cùng output:

```bash
python3 scripts/validate-package.py
python3 scripts/package-plugin.py --check
python3 -m unittest discover -s tests -v
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json --strict
npx --yes skills@1.5.20 add . --list
```

README ở root là mô tả dài của listing. Phần đầu giải thích công dụng và demo; phần “Cách
hoạt động, dữ liệu và hỗ trợ” khai báo hành vi và troubleshooting. Giữ tên Vietnamizer,
publisher Fioenix và mô tả tiếng Việt; không thêm category hoặc field màu của Codex vào
schema Claude. Icon và URL listing được CLI hỗ trợ từ 2.1.281; phiên bản cũ có thể cảnh báo.

README dùng ảnh Markdown với biến thể GitHub sáng/tối. Client khác có thể hiển thị cả hai ảnh;
phải xem trực tiếp, không coi fragment GitHub là hỗ trợ dark mode của mọi client. Manifest Claude
hiện trỏ icon violet; khả năng chọn icon tối tùy client, không thêm field chưa được xác nhận.

## Review Desktop ngày 03/10/2026

Ảnh review của maintainer xác nhận Desktop nhận bản 0.9.7, bật plugin và thấy một skill,
nhưng dùng icon mặc định. Mô tả trước đó chỉ có tagline; manifest và catalog đã được sửa
thành mô tả công dụng, phạm vi bảo toàn và yêu cầu tài khoản. Tagline trong README giữ nguyên.

Theo [plugin manifest reference](https://code.claude.com/docs/en/plugins-reference#directory-listing-fields),
`icon` là trường directory listing và Claude Code không đọc nó khi nạp plugin. Tài liệu này
không xác nhận Desktop hiển thị icon từ ZIP tùy chỉnh. Giữ đường dẫn SVG hợp lệ, không thêm
field dark-mode hoặc đổi định dạng ảnh chỉ dựa trên suy đoán. Icon Desktop vẫn chưa được
xác minh; validator đạt không chứng minh icon sẽ hiển thị.

Cập nhật bản upload riêng bằng ZIP cùng tên plugin, không tạo bản Vietnamizer thứ hai.
Chưa có bằng chứng model Claude chạy. Owner đã miễn chạy thêm test model Claude cùng review
light mode/fallback trong đợt này; ghi là **không chạy**, không đổi thành “đã đạt”. Waiver nội
bộ không miễn review của Anthropic hoặc chứng minh hiệu quả so với baseline.

## Prompt và tài khoản thử cho reviewer

[Ba prompt trong README](../README.md#ba-prompt-dùng-thử-trên-claude) là nguồn duy nhất cho
input và tiêu chí mong đợi: hoàn chỉnh ý, giữ câu tự nhiên và giữ byte code. Đây là mẫu thử,
không phải kết quả model. Không cần tài khoản Vietnamizer vì plugin không có backend riêng.
Nếu portal yêu cầu test account, giải thích điều này và cung cấp các prompt giả lập; không
chia sẻ credential Claude của maintainer.

## Cổng dữ liệu và fallback

- Host có skill TypeSafe nhưng chưa có quyền gửi dữ liệu: không gọi dịch vụ, không tìm key.
- Harness không cung cấp skill TypeSafe: core tiếp tục im lặng, không nhắc agent hoặc người dùng
  cài đặt, thiết lập hay tìm key. Không coi việc thiếu TypeSafe là lỗi hoặc thiếu sót.
- Host có skill nhưng thiếu capability TypeSafe: core tiếp tục; không tự cài hoặc dựng connector.
- Thẩm định hữu ích và được cho phép gửi dữ liệu: chỉ thẩm định candidate có trước qua skill chính chủ đã có;
  không tự dựng connector, không gửi toàn văn bản hoặc vùng bảo toàn.
- Cho mẫu phong cách trong yêu cầu: dùng đúng mẫu; không truy xuất/lưu Claude memory.

## Bản nháp khai báo Data handling

Owner đối chiếu các dữ kiện này với câu hỏi thực tế; không tự chọn “No” cho toàn bộ form.

| Chủ đề | Khai báo dựa trên source |
|---|---|
| Đọc dữ liệu cá nhân | Văn bản, yêu cầu, ngữ cảnh và mẫu giọng chủ động cung cấp có thể chứa dữ liệu cá nhân; chỉ dùng phần cần cho biên tập |
| File | Agent có thể sửa file người dùng giao theo phạm vi/quyền host; không tự khai thác memory, lịch sử hoặc file ngoài phạm vi |
| Lưu dữ liệu | Không có backend/telemetry và không tự lưu prose/hồ sơ; ghi file theo yêu cầu hoặc bảo trì được cấp quyền vẫn có thể tạo dữ liệu lưu trên host |
| Retention/deletion | Không nhận prose qua backend maintainer; Claude, file host và issue công khai có cơ chế lưu/xóa riêng, không hứa zero retention cho các bên đó |
| Gửi dịch vụ khác | Core không gửi tới maintainer. TypeSafe tùy chọn có thể nhận đoạn gốc/candidate/ngữ cảnh tối thiểu khi được phép, qua skill chính chủ đã có |
| Dữ liệu bị hạn chế | Dừng đầu vào chứa PCI, PHI, định danh chính phủ hoặc secret xác thực; yêu cầu bản đã che/giả lập |
| Audience dưới 18 | Không có định vị dành riêng cho người dưới 18 trong source; owner xác nhận audience thực tế khi trả lời form |
| Privacy | [Vietnamizer](../PRIVACY.md), [TypeSafe nếu bật](https://typesafe.ai/legal/privacy-policy) và chính sách của Claude/host theo tài khoản |
| Contact/support | GitHub Issues là kênh công khai; owner cung cấp email liên hệ xác minh trong portal, không đăng ca riêng tư hoặc secret vào issue |

TypeSafe không phải connector được Vietnamizer khai báo. Khai báo luồng gửi dữ liệu tùy
chọn này; nếu reviewer hỏi thì trả lời theo source, không đổi thành “không gửi cho dịch vụ
bên ngoài” để qua scan. Có skill không phải consent, và không có skill không phải lỗi.

## Cổng còn cần owner và Anthropic

Directory Policy hạn chế đọc memory, lịch sử và user files. Vietnamizer cấm tự truy xuất
memory/lịch sử nhưng hỗ trợ file người dùng giao rõ. Ghi rõ khác biệt này; chưa khẳng định
Anthropic chấp thuận cách diễn giải đó. Nếu reviewer yêu cầu thu hẹp, cần owner duyệt thay
đổi, không âm thầm đổi workflow.

1. Owner xác nhận tổ chức sở hữu, email contact và kết nối GitHub có quyền push.
2. Tích hợp tài liệu/source, kiểm CI; Validate đúng commit và review README/icon trên preview.
3. Xử lý mọi Blocking; xem Policy hold/Warning cùng khai báo dữ liệu. Kiểm offline không
   chứng minh đạt toàn bộ policy.
4. Owner duyệt các điều khoản/xác nhận pháp lý và cho phép Submit for review.
5. Theo dõi scan/review, rồi publish theo trạng thái portal; approved không tự đồng nghĩa
   đã publish. Không có ETA cố định hoặc bảo đảm được niêm yết.

Push, dùng quota, submit và publish là các hành động riêng; checklist không thực hiện chúng.

Nguồn: [checklist Anthropic](https://claude.com/docs/plugins/pre-submission-checklist),
[chính sách directory](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy),
[quy trình gửi](https://claude.com/docs/plugins/submit).
