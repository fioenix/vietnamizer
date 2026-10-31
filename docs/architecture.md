# Kiến trúc và cây nguồn

[← README](../README.md)

## Kiến trúc

`SKILL.md` là nguồn chuẩn về điều phối và chốt; từng catalog sở hữu duy nhất nội dung pattern được core uỷ quyền. Đây là cấu trúc source 0.13.3:

```text
SKILL.md                                      core gọn: phạm vi, chốt, tuyến đọc và trả kết quả
references/loi-thieu-tu.md                    V1–V8,V20
references/loi-cau-va-quan-he.md               V9–V18,V24–V25
references/loi-tu-va-loi-dan.md                V19,V21–V23
references/typography.md                      T1–T6
references/quy-trinh-viet.md                  workflow bài, không nạp khi sửa nhỏ
references/nguon-van-phong.md                 nguồn mẫu chuyên môn, không nạp khi đã có mẫu
profiles/blog-ca-nhan/rules.md                B1–B17 cho văn bản có giọng cá nhân
profiles/blog-ca-nhan/styles/                 bốn style card có tác giả hiện diện
profiles/ky-thuat-doanh-nghiep/rules.md       K1–K7 và giới hạn của văn kỹ thuật, học thuật
profiles/ky-thuat-doanh-nghiep/styles/        ba style card kỹ thuật, vận hành và học thuật
references/han-viet-thuan-viet.md             bảng tra và điều kiện phải giữ thuật ngữ
references/bang-tra-cuu.md                    bảng tra hư từ, loại từ, tiểu từ và câu hỏi chẩn đoán
references/bo-giai-phong-cach.md              bộ giải ngữ cảnh, precedence và registry đường dẫn
references/giu-giong-tu-mau.md                đọc mẫu được giao, rút đặc tính giọng có phạm vi và kiểm bản sửa
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
README.md                                    giới thiệu ngắn, bằng chứng trực quan và điều hướng
docs/installation.md, docs/usage.md           cài đặt, cách dùng, phạm vi và dữ liệu
docs/style-and-voice.md                       hướng dẫn giọng mẫu và phong cách
docs/patterns.md, docs/changelog.md           danh mục đầy đủ và lịch sử phiên bản
docs/benchmarks.md, docs/figures/             bằng chứng, hình README và tooling vẽ tùy chọn
docs/sources.md                              nguồn và mức độ tin cậy
docs/plugin-distribution.md                   đường cài, kiểm thử và giới hạn publication
docs/openai-marketplace-assessment-2026-10-23.md  bằng chứng intake OpenAI và đề xuất sản phẩm MCP
scripts/scan-tells.sh                         tìm những chỗ có thể rà bằng biểu thức chính quy; nguồn tín hiệu ưu tiên của registry
jev/                                         runner Python và registry 55 pattern
scripts/build-jev-registry.py                 sinh/kiểm registry và tín hiệu ưu tiên từ nguồn canonical
.specify/                                     constitution, template và script của Spec Kit
specs/                                        đặc tả, checklist, plan và task theo từng feature
benchmarks/                                   corpus, runner pilot/Jev, chấm model/người và phân tích; raw giữ local
eval/guard/                                   hồ sơ corpus/config lịch sử đã ngừng dùng
```

Ngoài các file từ `.specify/` trở xuống, `docs/`, manifest source và adapter discovery
cũng phục vụ source hoặc phát triển, không nằm trong gói `vietnamizer.skill`.

Generated agent skills, Spec Kit integration state, raw run và scratch output được giữ local.
Xem [hướng dẫn đóng góp](../CONTRIBUTING.md) để cài tooling maintainer và chạy kiểm tra offline.

Bộ giải phong cách dùng đúng bảy card trong [hướng dẫn phong cách](style-and-voice.md). Nội dung chuẩn của từng card nằm
trong thư mục `styles/` của profile tương thích; `references/bo-giai-phong-cach.md` chỉ sở hữu cách
chọn card, thứ tự ưu tiên và registry đường dẫn.

Trước khi chạy pattern, skill kiểm tra thể loại. Pháp quy, hợp đồng, thơ, văn cổ phong và nghi lễ chỉ
được rà T1–T6. Code, schema, dữ liệu có cấu trúc, bảng tham số, trích dẫn nguyên văn, tên riêng và ví
dụ đang được bàn tới là vùng bảo toàn từng byte. Xem danh sách và ngoại lệ đầy đủ trong `SKILL.md`.


Từ source 0.13.3, root điều khiển cùng quy trình lập ý → chọn giọng → khai triển → review cho
viết mới và biên tập. Brief hoặc bản gốc đầy đủ là nguồn đối chiếu; outline không thay nguồn.
Guide mẫu giữ chi tiết cách dùng bằng chứng giọng cá nhân/tham chiếu chuyên môn, không sở hữu
quy trình riêng. Không đổi 55 pattern, schema, request hay runtime Jev; kiểm nghĩa với brief
khi viết mới vẫn do host thực hiện. Ca EW01–EW16 là kỳ vọng thủ công, chưa phải pilot chất lượng.


Tuyến mặc định không nạp catalog, resolver hoặc schema evaluator. Sửa nhỏ chỉ tra nghi vấn;
làm bài thêm workflow và một card; có mẫu thêm guide. Resolver chỉ khi mâu thuẫn/pha chức năng,
guide nguồn chỉ khi chọn nguồn. Trạng thái key/capability kiểm từ core trước; đầy đủ điều kiện
mới đọc hợp đồng Jev. Tiết kiệm ký tự hướng dẫn chưa chứng minh giảm billing token hoặc tăng chất lượng.
