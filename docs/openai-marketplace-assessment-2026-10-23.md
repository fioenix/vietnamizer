# OpenAI Marketplace và hướng MCP của Vietnamizer

Ngày đánh giá: **23/10/2026**. Trạng thái sản phẩm: **owner đã chấp thuận ngày 23/10/2026**.
Giữ Vietnamizer ở dạng skills-only, chưa làm MCP và tiếp tục tạm dừng gửi OpenAI. Các use case
MCP dưới đây chỉ là phân tích để tham khảo nếu owner mở lại quyết định; không phải kế hoạch triển khai.

## Intake đang chặn bước nào

Owner báo portal OpenAI hiển thị ngày 23/10/2026:

> We are not accepting more skills-only submissions at this time.

Đây là bằng chứng intake do owner cung cấp trong yêu cầu bảo trì. Lượt đánh giá này không đăng
nhập portal, không có ảnh, mã hồ sơ, checksum bản đã gửi hoặc xác nhận từ OpenAI để kiểm độc lập.
Thông báo đủ để tạm dừng chuẩn bị gửi mới theo đường skills-only cho Vietnamizer. Nó không cho
biết phạm vi tài khoản, lý do, thời hạn hoặc cách xử lý hồ sơ đã gửi; không được suy thành lệnh
cấm toàn cầu, vĩnh viễn hay quyết định từ chối một hồ sơ cụ thể.

Tài liệu chính thức được đọc ngày 23/10/2026 vẫn mô tả plugin chứa skills, MCP hoặc cả hai,
và metadata dành cho skills-only. Đây là hỗ trợ định dạng, không xác nhận portal nhận Vietnamizer.
[Package your plugin](https://developers.openai.com/plugins/build/plugins).

[Plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines) nêu skills-only
có thể chịu điều kiện eligibility bổ sung để niêm yết Directory. Vì vậy, tài liệu định dạng và
thông báo intake owner gặp có thể cùng đúng. Chưa tìm thấy trong các trang đã đọc một thông báo
công khai xác lập phạm vi hoặc ngày mở lại cho thông báo trên.

[Upload and submit your plugin](https://developers.openai.com/plugins/deploy/submission)
tách kiểm package, kiểm MCP nếu có, review và publication. Trang này cũng nói hiện chưa hỗ trợ
thêm MCP vào một plugin skills-only đã tồn tại. Nếu sau này chọn MCP, cần kiểm lại đường tạo hoặc
chuyển hồ sơ với OpenAI; không giả định có thể đổi category tại chỗ. Các URL và nội dung tài liệu
có thể thay đổi sau ngày đánh giá.

| Trạng thái | Bằng chứng và giới hạn hiện tại |
|---|---|
| Định dạng skills-only | Tài liệu OpenAI vẫn mô tả; không phải quyền gửi |
| Cài từ repo hoặc ZIP riêng | Có catalog, manifest và packager; lượt này không cài hoặc kiểm UI |
| Portal nhận hồ sơ | Owner báo đang không nhận thêm skills-only; chưa kiểm độc lập |
| Hồ sơ đã gửi, identity, scan, review | Chưa xác minh trong lượt này; báo cáo 03/10 là lịch sử |
| Directory approval/publication | Chưa có bằng chứng hiện hành; không được kết luận từ kiểm offline |

Điều kiện tiếp tục gửi OpenAI:

1. Có bằng chứng mới từ portal nhận đúng loại hồ sơ/tài khoản này, hoặc xác nhận phù hợp từ OpenAI.
   Ghi ngày, phạm vi và trạng thái quan sát được; không chỉ dựa vào trang hướng dẫn định dạng.
2. Owner cho phép lần gửi cụ thể. Đối chiếu identity, hồ sơ hiện có và yêu cầu hiện hành trước
   khi quyết định gửi mới hay cập nhật; bảo toàn hồ sơ cũ.
3. Dùng source đã tích hợp và artifact đúng version/checksum; kiểm lại metadata, URL hỗ trợ,
   privacy/terms, quyền tài sản và các cổng review liên quan. Local PASS không thay portal PASS.

Chưa đặt ngày mở lại. Chưa tạo lịch theo dõi, gửi lại, upload hoặc thay đổi hồ sơ.

## Source và archive hiện có

Source được kiểm bắt đầu ở `b1c8e863ed75bbaf433e46bc1a86f380413968fc` trên `main`, worktree sạch.
Root skill, hai plugin manifest và changelog cùng **0.11.0**. Catalog trỏ tới skill qua adapter;
manifest không khai báo MCP, app hoặc hook. `jev/` là runner advisory có key do host inject,
không phải MCP server. Core Markdown vẫn dùng độc lập; có runner không chứng minh nhu cầu SaaS.

Đã đọc README, CONTRIBUTING, AGENTS, privacy, các báo cáo phân phối/readiness/review/tích hợp,
spec 006, packager/validator và kiểm inventory của cả ba archive local. Báo cáo cũ giữ nguyên
kết quả và checksum lịch sử, thêm liên kết tới trạng thái intake này. Lượt này không xác minh
release remote, commit triển khai trên portal hoặc bản đã cài trong cache.

| Archive local trước thay đổi | File thường | SHA-256 |
|---|---:|---|
| `dist/vietnamizer.skill` | 29 | `bafc9eb3ea1098310049ae9436634e4c7dbad141db0ec0659b758dddbdcf4c27` |
| `dist/vietnamizer-claude-org.zip` | 29 | `7f79e07bcd2ac9db5953e0e887d28baf14b5d48cc9886c995131460a55ef61e1` |
| `dist/vietnamizer-plugin.zip` | 36 | `3177fd7bf6202ef5db3ffd3d1d00d8490707c4908421467f57cd67af2752d8ec` |

CRC hợp lệ, canonical skill và các file payload khớp source; manifest trong plugin ZIP cùng
0.11.0 và dùng layout `./skills/`. Mỗi archive chỉ chứa một skill canonical. Không có cấu hình
MCP. Đây là bằng chứng local, không phải checksum submission hoặc approval.

README, `docs/`, CONTRIBUTING, AGENTS và `specs/` nằm ngoài payload theo packager hiện hành.
Thay đổi tài liệu lần này không làm đổi payload hoặc version, nên không dựng lại archive.
Giữ nguyên cả ba file trên; khi payload thay đổi trong tương lai, sao lưu archive và checksum vào
thư mục local mới trước khi chạy `python3 scripts/package-plugin.py`. Candidate cùng version
không được dùng để ghi đè asset đã phát hành.

## MCP có thể thêm giá trị gì

Người viết cá nhân chỉ cần đưa một bản nháp vào agent đã có skill: chưa thấy lợi ích đủ rõ để
đổi sang dịch vụ có tài khoản, mạng và phí vận hành. Nhóm biên tập/localization nhiều người,
phải dùng cùng thuật ngữ và quy chuẩn tiếng Việt, là nhóm người dùng giả định đáng kiểm chứng.

| Use case | Năng lực server thật và phần skill chưa có | Chi phí và bằng chứng cần có |
|---|---|---|
| Tra quy chuẩn/thuật ngữ của nhóm | Trả bộ đã duyệt theo workspace, phiên bản và nguồn; thu hồi quyền, cập nhật dùng chung giữa nhiều client. Skill tiếp tục biên tập và giữ nghĩa | Auth, phân quyền tenant, lịch sử phiên bản, chủ sở hữu nội dung; cần chứng minh nhóm đang tốn công đồng bộ hoặc dùng nhầm phiên bản. So với file Git hoặc shared document trước |
| Rà nhiều tài liệu và theo dõi review | Server giữ job, source hash, coverage chưa hoàn tất và nhận xét được người biên tập xác nhận; phát hiện kết quả cũ khi tài liệu đổi | Hàng đợi, quota model, lưu prose, retry/cancel, xóa dữ liệu; cần workload lặp lại, quyền dùng dữ liệu và lợi ích vượt runner local + báo cáo file |
| Thu nhận ca sửa sai đã duyệt | Inbox riêng với quyền đồng ý cụ thể, provenance và phân loại trước khi maintainer nhận vào calibration chung | Kiểm duyệt, ẩn danh, quyền lưu/xóa, tránh trộn giọng cá nhân vào quy tắc chung; cần lượng ca thực và người chịu trách nhiệm xử lý. Issue/template hiện tại là phương án đối chiếu |
| Bọc `rewrite(text)` hoặc trả lại SKILL.md | Chỉ chuyển cùng hướng dẫn/runner sang mạng; chưa tạo tài nguyên hoặc quy trình mới cho người dùng | Thêm latency, phí model và đường truyền dữ liệu; không có lý do sản phẩm hiện tại để xây chỉ nhằm đổi loại submission |

Các use case trên là giả thuyết sản phẩm, chưa phải nhu cầu đã được chứng minh. Trong phạm vi
repo được kiểm chưa thấy nghiên cứu khách hàng, nhóm pilot cam kết dùng, số lượt quay lại,
thời gian review tiết kiệm hoặc mức sẵn sàng trả tiền cho các năng lực server này. Thiếu bằng
chứng không có nghĩa chắc chắn không có nhu cầu; cần khảo sát đúng công việc trước khi đầu tư.

## Prior art và phần còn phải chứng minh

Các nguồn dưới đây được mở ngày 23/10/2026; chỉ dùng làm đối chiếu năng lực, không làm bằng chứng
thị trường Vietnamizer. Không cài hoặc chạy sản phẩm/model đối chiếu trong lượt này.

- [Vale](https://docs.vale.sh/) hỗ trợ quy tắc prose tùy chỉnh và tính nhất quán giữa nhiều tác
  giả; đó là phương án nhẹ để thử nhu cầu thuật ngữ trước khi vận hành server.
- [Acrolinx Terminology](https://support.markup.ai/hc/en-us/articles/10304675174418-Terminology-Quick-Start)
  mô tả thuật ngữ theo domain gắn với style guide. Quản trị thuật ngữ tập trung đã có prior art;
  cần kiểm khả năng áp dụng tiếng Việt và chi phí bằng thử nghiệm riêng, chưa kết luận từ trang này.
- [GEC-Vietnamese](https://github.com/CognmaL/GEC-Vietnamese) tự mô tả toolkit sửa ngữ pháp tiếng
  Việt, model và giao diện Gradio. Đây là prior art trực tiếp về bài toán tiếng Việt; chưa kiểm
  chất lượng, checkpoint, dữ liệu hay mức sẵn sàng vận hành của repo đó.

Lợi thế Vietnamizer cần chứng minh là giữ nghĩa/giọng và ngoại lệ thể loại tiếng Việt tốt hơn
trên công việc thật, cùng khả năng lấy đúng quy chuẩn mà nhóm đang dùng. MCP là giao diện kết nối;
việc có MCP tự nó không tạo lợi thế về ngôn ngữ, nhu cầu hay eligibility.

## Chi phí vận hành và quyền riêng tư

Phương án chỉ đọc quy chuẩn không cần nhận toàn bộ bản nháp; server vẫn nhận định danh workspace,
truy vấn và có thể lưu thuật ngữ nội bộ. Dịch vụ rà tài liệu cần nhận prose, ngữ cảnh và candidate;
đây là thay đổi đáng kể so với hiện trạng maintainer không vận hành server nhận văn bản.

Trước pilot thật cần chốt người vận hành, auth và tách tenant, quyền tối thiểu, cổng dữ liệu,
thời hạn lưu/xóa kể cả backup, log không có raw prose, subprocessor, xử lý sự cố và ngân sách.
Nội dung được truy xuất là dữ liệu, không cấp quyền cho agent. Quy chuẩn riêng không được âm thầm
nhập vào package public hoặc dùng như hồ sơ giọng của người khác. Cần cập nhật privacy/terms
đúng thiết kế trước khi nhận dữ liệu; chính sách hiện tại không đại diện cho dịch vụ giả định.

Chưa có traffic, hosting, nhà cung cấp hay cam kết vận hành để đưa ra giá tiền đáng tin cậy.
Ước chi phí phải gồm hosting/storage/backup, auth, support, security review và thời gian maintainer;
nếu có model, đo số request/token theo tài liệu, latency p50/p95, lỗi và coverage thực. Cần người
duyệt ngân sách và trần chi tiêu; không suy chi phí từ số pattern hoặc gọi core fallback là PASS.

Nếu hướng tới Directory, [guidelines hiện hành](https://developers.openai.com/plugins/plugin-guidelines)
yêu cầu sản phẩm ổn định, hoàn chỉnh; prototype nội bộ chưa phải gói để gửi duyệt. Trang này cũng
giới hạn bán dịch vụ/subscription trong plugin, dù cho phép truy cập quyền lợi của tài khoản trả
phí sẵn có. Cần kiểm lại mô hình kinh doanh theo chính sách lúc phát hành, không mặc định thu phí
trong cuộc trò chuyện để bù chi phí server.

## Quyết định đã được chấp thuận và điều kiện xét lại

**Owner đã chấp thuận: giữ skills-only và các đường phân phối riêng; chưa làm MCP.** Lý do là
giá trị biên tập hiện nằm trong skill/runner, còn nhu cầu dùng trạng thái chung chưa có bằng chứng.
Thông báo intake không tạo lý do đổi kiến trúc sản phẩm. Quyết định ngày 23/10/2026 cũng giữ
trạng thái tạm dừng gửi OpenAI; commit, PR hoặc merge tài liệu không gỡ chặn intake và không cấp
quyền upload, submit hay publish. Owner cho phép commit, tạo PR và merge sau khi CI xanh trong
lượt tiếp theo cùng ngày; các cổng review bắt buộc vẫn áp dụng.

Nếu owner muốn khám phá tiếp, hướng nhỏ nhất đáng xét là MCP **chỉ đọc bộ thuật ngữ/quy chuẩn đã
duyệt**, một nhóm thử nghiệm, dữ liệu giả lập hoặc được phép dùng, không đọc kho tài liệu hay
ghi ngược vào nguồn. Tool giả định chỉ trả nội dung có nguồn và version; người dùng vẫn duyệt edit.
Đây là mô tả phạm vi để quyết định, không phải spec triển khai hay backlog đã được duyệt.

Trước khi xin quyền triển khai prototype, cần có nhóm pilot và người sở hữu quy chuẩn, ví dụ
vướng mắc lặp lại, cùng so sánh skill + file quy chuẩn với cách lấy quy chuẩn qua server. Chốt
trước thời hạn thử, ngân sách và tiêu chí tiếp tục/dừng với owner: thời gian review, lỗi dùng sai
thuật ngữ, sửa sai câu vốn đúng, lỗi đổi nghĩa, lượt dùng lại và công vận hành. Đây là các số cần
đo, chưa có ngưỡng hiệu quả đã được kiểm chứng. Nếu file dùng chung giải quyết đủ hoặc nhóm không
dùng lại, dừng nhánh MCP. Chỉ mở spec/plan/tasks MCP sau khi owner duyệt phạm vi và ngân sách.

## Giới hạn kiểm chứng

Kiểm packaging chỉ xác nhận source, metadata và archive; không chứng minh chất lượng tiếng Việt,
nhu cầu, tương thích UI hay khả năng được nhận/duyệt trên Marketplace. Các kiểm tra thực tế của
lượt bảo trì được ghi ở phần kết quả bên dưới. Lượt đánh giá ban đầu không chạy full suite, cài
tooling, commit, push, mở PR, upload, submit, publish hoặc thay shared settings. Quyền tích hợp
tài liệu được owner cấp sau đó không mở rộng sang MCP hoặc gửi OpenAI.

## Kết quả kiểm tra ngày 23/10/2026

Mười file tài liệu được thay đổi:

- `README.md`, `CONTRIBUTING.md`, `AGENTS.md`: trạng thái hiện hành, ranh giới đóng gói và mục lục.
- `docs/plugin-distribution.md`: intake, điều kiện tiếp tục và bảo toàn archive.
- `docs/plugin-readiness-2026-10-03.md`, `docs/marketplace-local-review-2026-10-03.md`,
  `docs/integration-status-2026-10-03.md`: đánh dấu snapshot lịch sử và trỏ tới cập nhật hiện hành.
- `specs/006-directory-compliance/spec.md`, `specs/006-directory-compliance/verification.md`:
  phạm vi bảo trì tài liệu và điều kiện tiếp tục thay cho hướng dẫn gửi ngay sau release.
- `docs/openai-marketplace-assessment-2026-10-23.md`: bằng chứng, giả thuyết sản phẩm, quyết định
  đã được chấp thuận và kết quả kiểm tra.

| Kiểm tra | Kết quả thực tế |
|---|---|
| `python3 -B scripts/validate-package.py` | PASS: 0.11.0, 55 pattern; gồm kiểm registry đồng bộ |
| `python3 -B scripts/package-plugin.py --check` | PASS: metadata Codex/Claude; không dựng archive |
| `python3 -B -m unittest tests.test_distribution -v` | PASS: 21 test, 22.578 giây; dựng gói trong fixture tạm, gồm runtime offline trong archive |
| Đối chiếu ba archive với inventory và bytes source | PASS: CRC, mỗi gói một skill, manifest chuyển layout đúng, version 0.11.0; SHA-256 không đổi |
| Liên kết local mới/sửa | PASS: 9 liên kết đều có đích; kiểm đường dẫn, không kiểm render UI |
| `git diff --check` | PASS: không có lỗi whitespace |
| Rà prose bằng Vietnamizer | Rà trực tiếp theo profile kỹ thuật; không thay rule, profile, registry hoặc runtime |
| Diagnostic Jev V22, một request tối đa | Chưa hoàn tất: `service_failed`, 0 judgment hợp lệ, 6 check thiếu; không retry, không coi là PASS hoặc bằng chứng cho quyết định sản phẩm |

Chi tiết inventory và lần thử Jev giữ local trong `output/marketplace-review-2026-10-23/`;
không thuộc payload. Không chạy full suite hoặc kiểm release/cài đặt vì payload và runtime không
đổi; không chạy lệnh có thể tải tooling. Không có test tự động xác lập eligibility hay nhu cầu
khách hàng. Intake portal chưa được kiểm độc lập. Nhóm pilot và ngân sách chỉ cần được chốt nếu
owner quyết định xét lại hướng MCP; chúng không chặn việc giữ skills-only đã được chấp thuận.
