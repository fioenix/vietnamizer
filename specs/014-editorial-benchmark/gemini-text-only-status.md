# Agent riêng cho benchmark Gemini — 26/10/2026

**Đã đối soát đủ 80/80 bản trong epoch-v3.** CLI ghi nhận gemini-3.8-flash-medium;
80 hội thoại riêng, chỉ gọi finish, không có tool thực thi. Raw/seal hợp lệ; chưa có
nhãn chất lượng. Bộ này dùng để đánh giá trước/sau trong cùng agent, giữ riêng bộ
Codex và hai Forms đang chấm; không xếp hạng runtime. Không chạy thêm benchmark.
Biên bản: `artifacts/014-gemini-text-only-20261026/epoch-v3/completion-audit-20261026.json`.

## Lịch sử kiểm chứng trước khi hoàn tất

Xem [lệnh chạy hiện hành](gemini-text-only-runbook.md). Các dòng bên dưới giữ diễn biến hai preflight trước; nguyên nhân đã được giải quyết: registry chung khác capability thực tế.

Fio đã duyệt agent riêng không có tool thực thi, giữ hai lượt host cũ làm chẩn đoán
và tạo đợt 80 đầu ra mới. Mã đã chuẩn bị trong `benchmarks/gemini_text_only.py`,
`gemini_text_guard.mjs` và `gemini-text-only-agent.md`. Raw được ghi ngoài workspace;
mỗi lượt dùng cùng 80 prompt công khai và được kiểm agent/model/tool từ native init.

Đã thêm đúng một file agent ở `~/.gemini/config/agents/`, whitelist chỉ có `finish`
để trả JSON. Không đổi agent mặc định, shared permissions, sandbox, credit hoặc token.
Native catalog discovery được đúng tên. Tuy nhiên cả hai lần kiểm chứng trên CLI1.4.7
đều quảng bá 60 tool trong init, gồm đọc file/chạy lệnh/web. Guard chặn cả hai lần;
terminal native ghi 0 turn, 0 token. Không đưa các probe này vào 80 đầu ra chất lượng.

Chưa biết chắc init đang liệt kê registry chung hay CLI bỏ qua giới hạn tool cho
custom primary agent. Vì vậy chưa có bằng chứng đủ để gọi runtime là text-only.
Sau hai lần kiểm chứng không đạt, dừng chỉnh code để kiểm tra kiến trúc và ranh giới
áp dụng cấu hình; không thử thêm cờ, nới guard hoặc coi tên agent là chứng minh.

Bằng chứng nằm ở `artifacts/014-gemini-text-only-20261026/`: native raw/seal hai probe,
`native-capability-blocker.json`, bản issue nháp chưa gửi và snapshot đối soát 4.451 file.
Hai lượt host cũ, toàn bộ Codex và local Forms giữ nguyên byte; không gọi API Forms.

Mười bốn test Python và bốn test Node đã qua, review độc lập đã xử lý thiếu sót
về nhận diện các dạng tool event. Đây là kiểm chứng code; gate CLI live vẫn chưa đạt.

## Kết quả đối soát cuối

Agent finish-only trả UNAVAILABLE trước yêu cầu đọc fixture giả; clone cùng body
được cấp `read_file` thực sự đọc đúng token chưa có trong prompt. Clone `view_file`
không đọc được. Cả ba có cùng registry60mục. Guard được sửa theo evidence-bound
registry, vẫn từ chối mọi operational call/subagent. Live R002-bare ở epoch-v3 đã
hoàn tất đúng agent/model, không có operational call; tính là1/80mới. Giữ nguyên
4.451file lịch sử gồm Codex/Forms/hailượtcũ. Không gửi Jev mới.

Phạm vi: đối chứng đọc file + whitelist đã pin + giám sát từng stream; không tuyên
bố kiểm vét cạn60tool hay cô lậpOS. Raw/proof/source/hash đầy đủ trong artifact.
