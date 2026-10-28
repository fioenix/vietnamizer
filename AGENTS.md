# AGENTS.md

Hướng dẫn dành cho agent làm việc trong repo này.

## Repo này chứa gì

Đây là một agent skill viết bằng Markdown, không có bước build. `SKILL.md` là tài liệu điều khiển chính; các profile và bảng tra bổ sung quy tắc theo thể loại hoặc cung cấp ví dụ chi tiết.

Skill được viết riêng cho tiếng Việt, không phải bản dịch của một skill tiếng Anh. Nhiều lỗi trong repo xuất hiện khi cấu trúc tiếng Anh được giữ nguyên rồi thay bằng từ tiếng Việt. Vì vậy, đừng nhập một quy tắc từ skill tiếng Anh vào đây nếu chưa kiểm tra xem nó có đúng với tiếng Việt hay không.

## Vai trò của từng file

| File | Vai trò |
|---|---|
| `SKILL.md` | Kiểm tra thể loại, quy trình, V1–V25, T1–T6 và cách trả kết quả. **Đây là nguồn chuẩn.** |
| `profiles/blog-ca-nhan/rules.md` | B1–B17 cho blog, bài cá nhân, nội dung công việc và marketing |
| `profiles/blog-ca-nhan/styles/` | Bốn style card tương thích với profile có tác giả hiện diện |
| `profiles/ky-thuat-doanh-nghiep/rules.md` | K1–K7 cùng các giới hạn riêng của tài liệu kỹ thuật, doanh nghiệp và học thuật |
| `profiles/ky-thuat-doanh-nghiep/styles/` | Ba style card cho hướng dẫn kỹ thuật, vận hành và học thuật |
| `references/han-viet-thuan-viet.md` | Bảng tra Hán-Việt và thuần Việt, kèm điều kiện phải giữ nguyên thuật ngữ |
| `references/bang-tra-cuu.md` | Bảng tra hư từ, loại từ, tiểu từ và câu hỏi chẩn đoán |
| `references/bo-giai-phong-cach.md` | Năm chiều ngữ cảnh, thứ tự ưu tiên và registry trỏ tới bảy style card; không sở hữu pattern |
| `references/giu-giong-tu-mau.md` | Cách rút đặc tính và điều chỉnh cấu trúc theo mẫu trong chế độ do `SKILL.md` chọn; kiểm nghĩa/giọng riêng, không sở hữu precedence, pattern hay lưu hồ sơ |
| `references/typesafe-advisor.md` | Input, authority, coverage và fallback của runner Jev tự động |
| `calibration/LOG.md` | Nhật ký bằng chứng dùng để sửa quy tắc chung; không lưu hồ sơ văn phong cá nhân |
| `calibration/ca-kiem-thu.md` | Ca kiểm thử chạy tay cho từng pattern, gồm cả ca chống sửa quá tay |
| `README.md` | Hướng dẫn cài đặt, mô tả kiến trúc, danh mục pattern, nguồn và lịch sử phiên bản |
| `CONTRIBUTING.md` | Hướng dẫn góp ca sửa sai, kiểm offline, bootstrap tooling và ranh giới source/local |
| `LICENSE` | MIT notice của sản phẩm, bắt buộc có trong cả hai archive |
| `agents/openai.yaml` | Tên hiển thị và lời gọi mặc định trên các nền tảng tương thích |
| `assets/` | Icon và wordmark SVG sáng/tối, nền trong suốt; chữ ă violet ở bản sáng, mint ở bản tối; được đóng gói cùng metadata UI |
| `.codex-plugin/plugin.json` | Manifest và metadata hiển thị của plugin Codex |
| `.plugin-skills/vietnamizer/SKILL.md` | Adapter discovery cho plugin source, nạp root `SKILL.md`; không sở hữu quy tắc biên tập |
| `.agents/plugins/marketplace.json` | Catalog phân phối Codex được track, không phải tooling sinh local |
| `.claude-plugin/plugin.json` | Manifest của plugin Claude Code |
| `.claude-plugin/marketplace.json` | Manifest marketplace của repo |
| `scripts/validate-package.py` | Kiểm tra version, số hiệu pattern, bảng README và giới hạn dòng |
| `scripts/package-skill.sh` | Đóng gói `dist/vietnamizer.skill` và `dist/vietnamizer-claude-org.zip` |
| `scripts/package-plugin.py` | Kiểm metadata/asset và tạo ZIP plugin hai nền tảng từ cùng public payload |
| `docs/plugin-distribution.md` | Hướng dẫn kiểm cài đặt và ranh giới repo marketplace với directory chính thức |
| `docs/openai-marketplace-assessment-2026-10-23.md` | Quyết định owner ngày 23/10/2026: giữ skills-only, chưa làm MCP, tạm dừng gửi OpenAI; bằng chứng và điều kiện xét lại |
| `PRIVACY.md`, `TERMS.md` | Thông tin dữ liệu và điều kiện dùng gói mã nguồn mở |
| `SECURITY.md` | Ranh giới bảo mật và kênh báo lỗi riêng, không dùng Issues công khai |
| `.github/ISSUE_TEMPLATE/` | Mẫu báo lỗi tối thiểu đã ẩn dữ liệu và đường dẫn báo bảo mật riêng |
| `jev/` | Runner, transport, CLI và registry được đóng gói |
| `scripts/build-jev-registry.py` | Sinh/kiểm định nghĩa 55 pattern từ nguồn canonical, kèm tín hiệu ưu tiên lấy từ `scripts/scan-tells.sh` |
| `scripts/scan-tells.sh` | Tìm những dấu hiệu có thể quét bằng biểu thức chính quy để người biên tập xem lại; biểu thức nào khớp với mục pattern trong `SKILL.md` cũng thành tín hiệu xếp thứ tự chấm trong `jev/registry.json` |
| `.specify/` | Cấu hình, template và script của Spec Kit; constitution trong `.specify/memory/constitution.md` chi phối spec, plan và implementation |
| `.specify/LICENSE` | MIT notice của GitHub Spec Kit được vendor trong repo |
| `specs/` | Đặc tả, checklist, plan và task của từng feature; Spec Kit là nguồn chuẩn cho các artifact này |
| `.agents/skills/` | Generated Codex tooling local, bị gitignore; bootstrap theo `CONTRIBUTING.md` |
| `benchmarks/` | Corpus giả lập và runner pilot biên tập; kết quả raw giữ local trong `artifacts/`, không phải tập holdout hoặc bằng chứng chất lượng đã chấm độc lập |
| `benchmarks/mr_compare.py` | Đối chiếu đóng băng MR01–MR12 giữa 0.12.0/0.12.1 trên cùng Codex: 14 tình huống × 2 phiên bản, raw riêng, không chạy lại mẫu; nhãn agent là kiểm tra hồi quy trên tập phát triển |
| `benchmarks/simple_forms.py`, `benchmarks/simple_forms.gs` | Bộ chấm người đọc trực tiếp: ảnh gốc/sửa hai cột, ba câu hỏi, ghép item ID và kiểm tra thứ tự; dữ liệu model lịch sử giữ nguyên |
| `benchmarks/gemini_text_only.py`, `benchmarks/gemini_text_guard.mjs`, `benchmarks/gemini-text-only-agent.md` | Đợt Gemini dùng agent riêng, guard đối soát registry theo capability proof và chặn tool call thực tế; raw ngoài workspace, live smoke 1/80 |
| `benchmarks/gemini_manual.py` | Script để owner tự chạy 80 đầu ra Gemini qua Agybird trong terminal; prepare/test offline, giữ raw và trần lượt, không thay Forms |
| `benchmarks/gemini_boundary.mjs`, `benchmarks/gemini_capture_cli.mjs` | Proxy egress Google HTTPS và bộ ghi raw theo byte cho runtime Gemini riêng; chưa nghiệm thu tích hợp/inference |
| `benchmarks/public_ai.py` | Bộ nguồn AI công khai có revision/provenance, bốn nhánh cùng một lượt tạo bản cuối; raw và manifest giữ local |
| `benchmarks/public_final.py` | Một pass đối soát riêng R020: dùng lại raw hợp lệ trả muộn, chỉ hỏi phần chưa hỏi trong trần; giữ riêng pass lỗi và pass đối soát |
| `benchmarks/public_availability.py` | Kết thúc tư vấn khi cặp timeout đã hết lượt; giữ tiền dự phòng, tách thiếu dữ liệu do deadline với lỗi schema |
| `benchmarks/public_abstention.py` | Kết thúc tư vấn khi phục hồi schema đã hết lượt; chỉ nhận prefix hợp lệ, giữ batch lỗi là chưa chấm, không gọi lần ba |
| `benchmarks/public_deadline.py` | Phục hồi một lần cho request Jev timeout trước HTTP/response; giữ lượt chưa rõ tiền và mọi trần, không lấy mẫu lại câu hợp lệ |
| `benchmarks/public_recovery.py` | Phục hồi riêng câu Jev sai phân phối, giữ câu hợp lệ, seal nguồn từng câu và trần chi phí/request của đợt công khai |
| `benchmarks/public_forms.py`, `benchmarks/public_forms.gs` | Tạo hai Forms mới cho đợt công khai, xáo nhãn độc lập, kiểm ảnh/thứ tự/item; không thay Forms pilot |
| `benchmarks/public_human.py`, `benchmarks/public_human.gs` | Xuất chỉ đọc và nhập phiếu đợt công khai theo item ID, binding và raw UTF-8; chọn hai phiếu rõ ràng trước khi mở khóa chế độ |
| `benchmarks/public_human_charts.py` | Vẽ SVG/PDF từ nhãn người đã chọn; bootstrap theo nguồn, giữ thiếu/chưa rõ; hình kiểm thử giả lập luôn được ghi nhãn riêng |
| `benchmarks/execution_report.py` | Phân tích chỉ đọc 160 đầu ra công khai: thay đổi ký tự/độ dài, thời gian/token, đối soát raw và chart SVG/PDF; không gọi model hoặc suy chất lượng |
| `benchmarks/mindfio_pilot.py` | Pilot giữ giọng riêng: bốn bài Mindfio, ba chế độ trên cùng Codex; hồ sơ được chủ nhân duyệt, tối đa 12 lượt sinh, raw CLI và đối chiếu trước/sau giữ local; không thay các đợt cũ hoặc Forms |
| `benchmarks/voice_pilot.py`, `benchmarks/voice_guard.mjs`, `benchmarks/voice_continue.py`, `benchmarks/voice_analysis.py` | Pilot giữ giọng tham chiếu 2×2 trên cùng Codex: mẫu và skill là hai yếu tố riêng, 32 đầu ra trong 56 lượt; chấm ẩn nhãn Codex/Gemini, giữ phiếu lỗi là thiếu, đối soát raw/mapping và phân tích offline riêng; không thay các benchmark cũ hoặc Forms |
| `benchmarks/voice_versions.py`, `benchmarks/voice_version_analysis.py` | Pilot021so0.12.1/0.13.0:32đầu ra trên cùng Codex, prompt theo mẫu rõ, hai đối chứng cùng input;52lượt tối đa gồm calibration/judge, raw riêng và tái dựng offline, không dùng điểm lịch sử làm đối chứng trực tiếp |
| `benchmarks/voice_patch_versions.py`, `benchmarks/voice_patch_analysis.py` | Pilot023so0.13.0/0.13.1 trên cùng Codex:32đầu ra, hai đối chứng prompt+mẫu;52lượt tối đa, raw riêng và kiểm V1thêm mệnh đề; không chạy lại/sửa các đợt cũ hoặc Forms |
| `benchmarks/voice_section_versions.py`, `benchmarks/voice_section_analysis.py` | Pilot025so0.13.1/0.13.2 trên cùng Codex,32đầu ra và52lượt tối đa; nguồn/task/đối chứng như023, kiểm riêng N2giọng/nghĩa/chức năng phần; raw và tái dựng riêng, không sửa đợt cũ/Forms |
| `benchmarks/jev_pilot.py` | Pilot Codex + Jev riêng, giữ dự phòng chi phí và đối soát bằng chứng; không thay runner phát hành |
| `benchmarks/quality_review.py`, `benchmarks/quality_review_v2.py` | Bộ chấm model ẩn chế độ và bản bổ sung enum; giữ raw, lỗi và mẫu thiếu, không thay chấm người |
| `benchmarks/reviewer.html`, `benchmarks/quality_human.py` | Giao diện chấm offline, ZIP riêng A/B và kiểm nhận JSON theo packet đã đóng băng |
| `benchmarks/reviewer_forms.gs`, `benchmarks/quality_forms.py` | Sinh Apps Script form nháp cho người điều phối; chưa nghiệm thu cloud, không tự công khai/gửi lời mời |
| `benchmarks/quality_analysis.py` | Phân tích model thăm dò, bootstrap theo nguồn và chart có mẫu số/giới hạn |
| `benchmarks/jev_capture.py`, `benchmarks/jev_recovery.py`, `benchmarks/jev_finish.py` | Phục hồi benchmark riêng: lưu raw HTTP, tái sử dụng bằng chứng đúng payload, cộng dồn chi phí và tạo bản cuối khi nhận đủ câu trả lời; giữ riêng trạng thái thiếu ngữ cảnh |
| `benchmarks/jev_composite.py` | Chỉ hỏi lại câu trả lời có lỗi phân bố đã quan sát, giữ câu hợp lệ và niêm phong nguồn từng câu trong bằng chứng tổng hợp |
| `eval/guard/` | Hồ sơ corpus và cấu hình thí nghiệm lịch sử đã ngừng dùng; không có harness thực thi |

Generated integration files, raw runs, scratch output, environment files và cache được giữ local
theo `.gitignore`. Khi contributor cần Spec Kit, dùng bootstrap trong `CONTRIBUTING.md`; constitution,
template, scripts, workflows, specs và evidence đã duyệt vẫn là source public được track.

## Runtime Jev và coverage

`jev/preparation.py` sở hữu phân đoạn nguồn/ngữ cảnh; `jev/coverage.py` sở hữu manifest công việc
và đối soát; `jev/core.py` lập lịch, `jev/transport.py` giữ origin/model và deadline I/O.
Khi sửa source spans, context, batch hoặc kết quả, đối chiếu hợp đồng hiện hành trong
`references/typesafe-advisor.md` và test nguồn/câu/context/coverage; không suy coverage từ số pattern.

## TypeSafe và hồ sơ lịch sử

Vietnamizer có runner Python standard library trong `jev/`, tự động thử khi host cấp key và
quyền gửi dữ liệu; không có key thì core chạy độc lập. Hợp đồng nằm trong
`references/typesafe-advisor.md`. Jev hỗ trợ LLM, không tự áp hoặc quyết định edit bằng điểm số.
`jev/registry.json` là output được track; sửa recipe ở `scripts/build-jev-registry.py`, chạy sinh
và `--check` khi thay nguồn canonical hoặc `scripts/scan-tells.sh`. Giữ parity runtime trong mọi archive.

Các feature nghiên cứu 001, 002 và 005 cùng `eval/guard/` là hồ sơ lịch sử đã ngừng triển khai.
Chúng không phải hướng dẫn chạy, không chứng minh hiệu quả cho workflow hiện hành và không
được dùng để tự khôi phục dependency hoặc tiêu quota.

## Ranh giới giữa quy tắc chung và profile

Đây là quyết định kiến trúc quan trọng nhất của repo.

- V1–V25 trong `SKILL.md` kiểm tra cách dùng từ và cấu trúc câu. Chúng chỉ chạy trên các thể loại được phép biên tập, đồng thời phải tuân theo mục **Không flag** của từng pattern.
- B1–B17 và K1–K7 phụ thuộc vào thể loại, người đọc và giọng văn. Chúng nằm trong `profiles/`.

Nếu một cách viết tự nhiên trong công văn nhưng dễ thành sáo ngữ trong blog, hãy xử lý nó ở profile. Không đưa vào V1–V25 như một lỗi áp dụng cho mọi văn bản.

Style card không phải tầng pattern thứ năm. Nó chỉ giải các lựa chọn đều hợp lệ sau khi cổng thể loại
đã chọn đúng profile; quyền sửa lỗi hoặc điều chỉnh theo mẫu do chế độ trong `SKILL.md` quyết định. Mỗi profile family giữ pattern trong `rules.md` và card tương thích trong
`styles/`; không sao chép nội dung card vào rules. `references/bo-giai-phong-cach.md` là nguồn chuẩn
cho resolver và registry, còn `SKILL.md` sở hữu thứ tự gọi.

## Hợp đồng bảo trì

- **Số hiệu pattern:** bốn tiền tố `V`, `T`, `B`, `K` đều bắt đầu từ 1 và tăng liên tục. `V` và `T` thuộc `SKILL.md`; `B` thuộc profile blog; `K` thuộc profile kỹ thuật. Khi thêm, bỏ hoặc đổi số, phải cập nhật bảng pattern trong `README.md` cùng lúc.
- **Ngưỡng thêm pattern:** một dấu hiệu chỉ được thành pattern riêng khi không pattern nào hiện có ngụ ý nó. Còn lại thì mở rộng mục **Dấu hiệu** của pattern gần nhất. Khi hai pattern chạm nhau, pattern hẹp hơn phải có một câu phân vai trỏ sang pattern kia, như K6 trỏ sang V21 cho phần lời chào và lời mời làm tiếp.
- **Version:** `metadata.version` trong `SKILL.md`, mục mới nhất của phần Lịch sử phiên bản trong `README.md` và `version` trong `.claude-plugin/plugin.json` phải giống nhau. Giữ version bên trong `metadata`; không đặt khoá `version` ở cấp cao nhất của frontmatter vì một số nền tảng không nhận khoá này. `marketplace.json` không có version để tránh hai nguồn dữ liệu.
- **Giới hạn dòng:** `SKILL.md` tối đa 550 dòng, profile blog tối đa 320 dòng, profile kỹ thuật tối đa 220 dòng. Các file trong `references/` không bị giới hạn.
- **Nguồn:** khi thêm pattern dựa trên tài liệu bên ngoài, phải thêm nguồn vào `README.md` và ghi đúng mức độ tin cậy. Nếu chỉ là suy luận, phải nói rõ là suy luận. Không tự tạo nguồn hoặc số liệu tần suất.
- **Kiểm tra trước khi phát hành:** chạy `python3 scripts/validate-package.py`, `python3 scripts/package-plugin.py`, `npx skills add . --list`, `claude plugin validate .` và `claude plugin validate .claude-plugin/plugin.json --strict`. Plugin ZIP phải chứa đúng một skill; icon và manifest phải resolve trong gói. Giữ root `SKILL.md` canonical, chỉ đổi layout trong output sinh ra.

## Khi sửa nội dung

- Giữ YAML frontmatter hợp lệ và đúng thụt lề.
- Mỗi pattern phải có đủ bốn mục: **Dấu hiệu**, **Vì sao**, **Sửa**, **Không flag**. Mục cuối ngăn skill sửa nhầm văn bản vốn đã đúng nên quan trọng ngang phần phát hiện.
- Ví dụ trước và sau khi sửa phải là tiếng Việt tự nhiên. Không dịch nguyên ví dụ từ skill tiếng Anh.
- Không dùng ngưỡng số làm điều kiện kết luận nếu ngưỡng đó chưa được kiểm chứng trên một bộ ngữ liệu phù hợp.
- Không biến lựa chọn phong cách thành lỗi ngôn ngữ. Chỉ đưa một cách viết vào quy tắc chung khi có thể chỉ ra điều gì sai và xác định được trường hợp cần loại trừ.
- Tự rà lại phần vừa viết bằng chính `SKILL.md`. Chú ý câu thiếu từ, câu bị nén thành nhãn cấu hình, thuật ngữ tiếng Anh không cần thiết và cách diễn đạt hạ giọng quá mức.
- Ví dụ minh hoạ không dùng tên đơn vị hành chính đã sáp nhập theo Nghị quyết 202/2025/QH15, có hiệu lực từ ngày 01/07/2025.

## Học từ phản hồi thực tế

Phản hồi của người dùng có thể giúp sửa skill, nhưng không phải khác biệt nào cũng được đưa vào quy tắc chung.

**Nguồn bằng chứng, xếp từ mạnh đến yếu:**

1. Bản do người dùng viết lại từ kết quả của skill.
2. Văn bản do người bản ngữ tự viết trong một tình huống sử dụng thật.
3. Nhận xét trực tiếp của người dùng về một pattern.
4. Quy tắc tiếng Việt do người bản ngữ nêu ra, kèm ít nhất một ví dụ và có thể kiểm tra độc lập.

Trước khi sửa skill, phải xếp quan sát vào đúng nhóm:

| Nhóm | Cách nhận biết | Nơi xử lý |
|---|---|---|
| Sở thích cá nhân | Cả hai cách viết đều tự nhiên; khác nhau ở nhịp câu, xưng hô, mức trang trọng hoặc cách dùng từ | Hồ sơ do đúng người dùng chủ động cung cấp cho tác vụ |
| Pattern sửa nhầm hoặc bỏ sót | Quy tắc chung sửa một câu vốn đúng, hoặc bỏ qua một lỗi có thể gọi tên | `calibration/LOG.md`, rồi điều chỉnh **Không flag** hoặc phần phát hiện |
| Hiện tượng mới | Một lỗi chưa có pattern nào mô tả và xuất hiện trong nhiều mẫu độc lập | `calibration/LOG.md`, rồi cân nhắc thêm pattern |

### Hồ sơ văn phong cá nhân

Không ghi sở thích của một người vào `calibration/LOG.md`. Skill dùng mẫu hoặc hồ sơ phong cách
người dùng chủ động cung cấp trong tác vụ; không tự truy xuất hoặc cập nhật memory. Có thể đề xuất
một bản tóm tắt để người dùng tự giữ, gồm cách xưng hô, nhịp câu, thuật ngữ, viết hoa và dấu câu.

Mỗi đặc tính cần có phạm vi áp dụng và một ví dụ ngắn. Không chép nguyên văn bản, không lưu dữ kiện cá nhân không liên quan, không dùng hồ sơ của người này cho người khác. Yêu cầu trong lượt hiện tại luôn được ưu tiên hơn memory cũ.

Không có mẫu hoặc hồ sơ được cung cấp thì tiếp tục theo thể loại và giọng của văn bản, không tự
tìm dữ liệu bên ngoài tác vụ hoặc suy đoán danh tính. Cơ chế memory riêng của maintainer/host không
phải một bước của workflow Vietnamizer.

### Nhật ký hiệu chuẩn dùng chung

`calibration/LOG.md` chỉ ghi bằng chứng có thể làm thay đổi quy tắc dùng chung. Mỗi mục cần có ngày, thể loại, đoạn trước khi sửa, bản đối chiếu, tên khác biệt, pattern liên quan, cách phân loại và quyết định.

Ghi bằng chứng trước khi sửa quy tắc. Một trường hợp sửa nhầm có thể đủ để bổ sung trường hợp loại trừ nếu lỗi được gọi tên rõ và có thể kiểm tra lại. Pattern mới cần nhiều mẫu độc lập, trừ khi người bản ngữ nêu một quy tắc ngôn ngữ có thể kiểm chứng ngay bằng nguồn đáng tin cậy.

Không dùng quan sát của một cá nhân để âm thầm điều chỉnh skill theo giọng của họ hoặc của tổ chức họ. Nếu một bản fork cố ý phục vụ riêng một tổ chức, phải nói rõ phạm vi đó trong changelog và không trình bày nó như quy tắc chung của tiếng Việt.

## Những việc còn thiếu

- Repo chưa có bộ ngữ liệu đủ để đặt ngưỡng tần suất cho các dấu hiệu. Số lần xuất hiện chỉ dùng để tìm chỗ cần đọc kỹ hơn.
- Một số nguồn trong README vẫn là nguồn trình bày lại. Xem mục “Nguồn còn thiếu” trước khi nâng mức độ tin cậy.
- Skill không tự kiểm tra được những phát biểu về cấu trúc repo. Mỗi khi thêm, đổi tên hoặc xoá file, phải đối chiếu lại `README.md` và `AGENTS.md` với cây thư mục thật.
