# Nhận và phân tích phiếu Google Forms

Phần mềm này dành riêng cho bộ 20 nguồn công khai đang chấm, với hai câu hỏi nền đã bỏ.
Không dùng log hoặc khóa ghép từ pilot giả lập cũ. Người chấm tiếp tục dùng hai link đã
giao; các bước dưới đây dành cho người điều phối sau khi họ hoàn tất.

## 1. Xuất dữ liệu và giữ nguyên raw

Workspace mới `artifacts/014-within-agent-amendment-20261026/workspace-v5` chứa `export-A.gs` và `export-B.gs`. Mỗi file có hàm
`runBatch`, chỉ đọc đúng một form. Nó đối chiếu ID, ngữ cảnh, ảnh và câu hỏi với bản đã
đóng băng trước khi xuất các phiếu. Không sửa form, gửi thư hay nộp phiếu thử.

Chạy từng file trong dự án Apps Script đã dùng; chờ thực thi xong rồi lưu toàn bộ
Execution log thành `A.log` và `B.log` trong một thư mục mới. Không bỏ những dòng chunk
hoặc dòng `public_human_export_done`. Bộ nhập sẽ ghép Unicode và kiểm SHA-256 UTF-8;
log thiếu, lẫn lần xuất, lỗi thực thi hoặc sai bộ dữ liệu sẽ bị từ chối. Giữ nguyên
hai log đầu vào, kể cả khi có nhiều phiếu hoặc phiếu thiếu.

Tham chiếu API: [FormResponse](https://developers.google.com/apps-script/reference/forms/form-response),
[GridItem](https://developers.google.com/apps-script/reference/forms/grid-item) và
[Utilities](https://developers.google.com/apps-script/reference/utilities/utilities).
Các hàm xuất dựa vào ID và dữ liệu trả lời của provider; link mở công khai không tự
xác thực danh tính người chấm.

## 2. Chọn đúng phiếu trước khi mở khóa chế độ

Từ thư mục repo, thay đường dẫn log bằng vị trí đã lưu:

```bash
python3 -B -m benchmarks.public_human inventory \
  --workspace artifacts/014-within-agent-amendment-20261026/workspace-v5 \
  --logs A.log B.log
```

Lệnh này chỉ liệt kê ID, thời gian và số mục đã trả lời. Fio đối chiếu với hai người
được giao form, rồi tạo `selection.json`, chẳng hạn:

```json
{"A":"ID_PHIEU_A_DA_XAC_NHAN","B":"ID_PHIEU_B_DA_XAC_NHAN"}
```

Không mặc định chọn phiếu mới nhất, đầy đủ nhất hoặc thuận lợi nhất. Kể cả mỗi form chỉ
có một phiếu, vẫn phải chỉ rõ ID. Trước khi có cả hai ID, công cụ không giải mã chất
lượng. Mọi phiếu không được chọn vẫn được giữ trong raw.

## 3. Phân tích trong một thư mục mới

```bash
python3 -B -m benchmarks.public_human analyze \
  --workspace artifacts/014-within-agent-amendment-20261026/workspace-v5 \
  --logs A.log B.log --selection selection.json \
  --output artifacts/014-public-human-results-NEW
```

Đầu ra có JSON đầy đủ, `before-after.csv` cho tỷ lệ so với bản gốc, CSV nhãn/nhận xét, phân bố nhãn, chênh lệch ghép cặp bổ sung, ma trận
đồng thuận và receipt gắn hash raw, binding, code. Thư mục đã tồn tại không bị ghi đè.
Nếu lỗi giữa chừng, giữ thư mục lỗi làm bằng chứng và dùng thư mục mới sau khi xử lý
nguyên nhân. Thay đổi code phân tích cần review và workspace mới; không lặng lẽ dùng
cấu hình khác với binding đã đóng băng.

Hai bảng hỏi tạo tối đa **320 nhãn phân loại**, tương ứng **160 lượt đánh giá bản sửa**
từ hai người. Đơn vị độc lập vẫn là **20 nguồn**. “Chưa rõ” và thiếu được giữ riêng;
không biến thành sửa đúng, không sửa hoặc thất bại. Nhận xét thuộc nhóm bốn bản A–D;
công cụ không tự suy nhận xét nhắc tới chế độ nào.

## 4. Dựng hình khi đã có nhãn thật

Thêm `--charts` vào lệnh phân tích, chạy bằng Python có ReportLab đã cài. Môi trường
đóng gói của Codex hiện có ReportLab; không cần cài thêm package. Python standard
library vẫn đủ để nhập và phân tích, chỉ phần vẽ cần thư viện này.

Tám hình SVG/PDF gồm hai phân bố nhãn, hai biểu đồ tỷ lệ trước/sau với CI, hai biểu đồ chênh lệch giữa chế độ bổ sung và hai ma trận
đồng thuận. Đổi SVG sang PNG 300 DPI bằng runtime Node/Sharp đã có:

```bash
node benchmarks/render_quality_charts.mjs PATH_TO_RESULTS/charts EXISTING_NODE_RUNTIME_ROOT
```

Lệnh render ghi kích thước, DPI và phiên bản renderer. Giữ CSV, summary, raw, selection
và manifest cùng hình. Không dùng các hình trong thư mục `qa/` cho README: đó là dữ
liệu kiểm thử giả lập, luôn mang nhãn `SYNTHETIC TEST DATA`.

Chưa có nhãn thật thì lệnh phân tích báo `awaiting_human`; yêu cầu vẽ chất lượng bị
từ chối. Bản readiness hiện có 0 nhãn đã nhập; đây không phải lần kiểm đếm phiếu live.

## 5. Cập nhật README

Dùng [mẫu báo cáo](human-results-template.md) sau khi kiểm phiếu. Báo đủ mẫu số, thiếu,
chưa rõ, CI theo nguồn và kết quả từng người. Kết quả chính là Vietnamizer so với bản gốc trên cùng agent: phân bố dễ đọc hơn / tương đương / khó hơn, báo riêng giữ đúng / có chỗ bị đổi và thiếu/chưa rõ. `before-after.csv` chứa tỷ lệ xác định với CI theo nguồn cho từng chế độ, từng người và trung bình hai người cố định. So sánh giữa các chế độ là bổ sung, không phải so Codex với Gemini.
Khi CI chứa 0, không kết luận hai cách tương đương. Không suy kết quả ra mọi văn bản
AI hoặc mọi người đọc tiếng Việt. Giữ riêng hạn chế Jev chỉ đủ phạm vi ở 1/20 nguồn.

Workspace-v2 và gói readiness cũ giữ nguyên để tái lập phương pháp cũ. Workspace-v5
đóng băng code/protocol mới, giữ đúng form, item, ảnh và khóa ghép cũ. Dùng hai file
export mới để log có binding tương ứng; chúng chỉ đọc, không sửa Forms. Không dùng
log có binding v2/v3/v4 cho v5, không sửa hash để ép nhập. Bộ Gemini chưa có phiếu trong
hai Forms này; không gán các nhãn Codex sang Gemini.
