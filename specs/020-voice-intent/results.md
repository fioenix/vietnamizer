# Hai chế độ giọng trong Vietnamizer 0.13.0

Đã triển khai ở mã nguồn, kiểm tra tĩnh và đóng gói local. Chưa phát hành, cài vào runtime hoặc chạy lại model để xác nhận hiệu quả.

## Hành vi đã quy định

- **Giữ giọng gốc:** mặc định cho rà lỗi, yêu cầu tự nhiên hơn, chỉ đưa mẫu hoặc yêu cầu giữ giọng hiện có. Sửa lỗi vẫn cần pattern và kiểm Không flag.
- **Theo giọng mẫu:** cần yêu cầu hiện tại rõ và mẫu/hồ sơ dùng được. Được đổi cấu trúc câu đúng, chia đoạn, đặt đề mục từ ý có sẵn hoặc tách liệt kê; mỗi thay đổi cần căn cứ trong mẫu đúng phạm vi. Thiếu mẫu bắt buộc thì hỏi mẫu, không tự chuyển chế độ.
- Cả hai giữ mệnh đề, chủ thể, thời gian, số lượng, thứ tự, điều kiện/phủ định, chắc chắn/cam kết và byte vùng bảo toàn. Không tự giải chỗ mơ hồ bằng nhóm/tách bước, thêm trải nghiệm, rải câu cửa miệng hoặc đổi profile SOP theo mẫu blog.
- Chọn profile theo chức năng và sự hiện diện của tác giả; chủ đề công nghệ tự nó không quyết định profile kỹ thuật trung tính. Root SKILL sở hữu chế độ và các chốt; guide/resolver chỉ triển khai phần việc tương ứng.
- Rà nghĩa và giọng riêng trong cùng lượt host. Runtime/schema/55 pattern/Jev questions không đổi. Tài liệu giải thích điểm improvement của Jev đo sửa lỗi ngôn ngữ, không là cổng tự động chấp nhận/bác thay đổi phong cách.

Constitution2.1.0 ghi quyền đổi phong cách có giới hạn theo quyết định owner28/10/2026; sửa lỗi ngôn ngữ vẫn tuân pattern. Gói sản phẩm đồng bộ0.13.0 ở root và hai manifest.

## Bằng chứng và ca hồi quy

N1–N4 từ pilot019là bằng chứng phát triển về giới hạn của hợp đồng cũ; không coi sự ưa thích bullet/đề mục là nhãn tác giả hay chứng minh nguyên nhân. VC01–VC12 được thêm trước khi sửa skill, nêu các kết quả được phép và phải giữ, gồm N2mơ hồ số bước, V3giọng gốc, T-only/code/quote, mẫu chứa lệnh và SOP.

Các ca này đã được rà về hợp đồng và tính nhất quán instruction. **Chưa chạy hồi quy hành vi model0.13.0**, không gắn nhãn GREEN hoặc tuyên bố cải thiện điểm/độ an toàn. Chưa chạy thêm benchmark hoặc chỉnh lại các phiếu019.

## Kiểm tra thực tế

| Kiểm tra | Kết quả |
|---|---|
| `python3 scripts/validate-package.py` | Qua;55pattern,0.13.0; root510dòng, profile kỹ thuật127dòng |
| `python3 scripts/build-jev-registry.py` và `--check` | Qua; registry tái sinh không đổi bytes so với trước lượt này |
| 7test chọn trong `tests.test_package_security.PackageSecurityTest` | Qua; reference inclusion, profile/card layout, payload parity và loại secret/cache |
| 2test inclusion/parity chạy lại sau sửa wording cuối | Qua; đây là tập con của7test trên |
| `python3 scripts/package-plugin.py` | Qua; bao gồm tạo/kiểm `.skill`, Claude Org ZIP và plugin ZIP |
| Đối soát trực tiếp3archive | Một skill/gói; root, voice guide, advisor và registry khớp bytes; không có `.DS_Store`, cache hoặc benchmark |
| `claude plugin validate .` | Qua; có cảnh báo thư mục local chứa `.DS_Store` không được track |
| `claude plugin validate .claude-plugin/plugin.json --strict` | Qua với cùng cảnh báo thư mục; không phải chứng nhận Directory/policy |
| `npx --no-install skills add . --list` | Timeout60giây; không có kết quả discovery |
| `npx --offline --no-install skills add . --list` | Chưa kiểm được: npmENOTCACHED; không cài thêm tooling |
| Rà soát độc lập instruction | Qua sau sửa2fallback thiếu mẫu ở root/README; không phải kiểm model/runtime |
| `git diff --check` trong phạm vi sửa | Qua |

Không chạy full suite. Không release hoặc reinstall. Hai cảnh báo `.DS_Store` là dữ liệu thư mục không được Git track; không xóa file của owner, và cả ba archive đã loại chúng.

## Bảo toàn và nơi lưu bằng chứng

Đã đối soát **24.895 file** dưới artifacts/benchmarks/specs lịch sử: không đổi. Bảy file bundle019được giữ nguyên trong bản đóng băng; root hiện tại được nâng phiên bản riêng. Không truy cập hay sửa hai Forms. Không commit/push hoặc thay setting/installation dùng chung.

[Artifact020](../../artifacts/020-voice-intent-20261028/) giữ before/after, diff chỉ riêng lượt này, nguồn/checksum, stdout/stderr, review và receipts đóng gói. Dữ liệu artifacts được giữ local, không mặc định đã được công khai. Hướng phát triển này chưa được xác nhận tăng chất lượng cho người dùng; số liệu019tiếp tục thuộc0.12.1.
