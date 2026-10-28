# Từ điển dữ liệu đánh giá của người đọc

| File / trường | Ý nghĩa |
|---|---|
| `binding.json` | Cohort, nguồn, form, item, câu hỏi và khóa ghép đã đóng băng; không gửi cho người chấm |
| `raw/*.log` | Nguyên bản log provider; không chỉnh Unicode, bỏ chunk hoặc ghi đè |
| `raw/exports.json` | Bản JSON đã giải mã chunk và kiểm hash, giữ mọi phiếu, kể cả phiếu không được chọn |
| `raw/selection.json` | Hai ID phiếu do người điều phối xác nhận trước khi giải mã chế độ |
| `ratings.csv` | Một hàng cho mỗi nguồn × người chấm × chế độ, tối đa 160 hàng |
| `preservation` | `preserved`, `changed`, `uncertain`, `missing`: nhãn từ câu 1, không phải kết luận ngôn ngữ độc lập |
| `readability` | `better`, `equivalent`, `worse`, `uncertain`, `missing`: nhãn từ câu 2 |
| `display_group`, `display_letter` | Giữ Q001–Q020 và A–D của đúng form để đọc nhận xét sau khi ghép chế độ |
| `notes.csv` | Nhận xét nguyên nhóm bốn bản, tối đa 40 hàng; không tự gán một nhận xét cho một chế độ |
| `label-counts.csv` | 16 hàng: hai người × bốn chế độ × hai câu chọn; mỗi hàng có tổng 20 nguồn |
| `answered` | Có nhãn, gồm cả “Chưa rõ”; không gồm `missing` |
| `determinate` | Có nhãn xác định, loại `missing` và `uncertain` |
| Ô count trống trong CSV | Loại nhãn không áp dụng cho câu hỏi đó; không phải một nhãn thiếu của người chấm |
| `paired-differences.csv` | 18 hàng: ba đối chiếu × hai chỉ số × A/B/gộp; đơn vị phân số, hình hiển thị điểm phần trăm |
| `better` | Chênh lệch tỷ lệ được đánh giá dễ đọc hơn; trị dương thiên về nhánh a |
| `changed` | Chênh lệch tỷ lệ được đánh giá có chỗ bị đổi; trị dương không tự là kết quả tốt |
| `n_sources` | Số nguồn ghép đủ cho đúng đối chiếu, chỉ số và tập người chấm; tối đa 20 |
| `excluded_sources` | 20 trừ `n_sources`; giữ riêng lý do thiếu/chưa rõ, hai lý do có thể giao nhau |
| `estimate`, `low`, `high` | Trung bình chênh lệch theo nguồn và CI percentile 95%; CI `null` khi dưới hai nguồn đủ |
| `degenerate` | Mọi chênh lệch quan sát đều giống nhau; không chứng minh chắc chắn về quần thể |
| `agreement.csv` | Ma trận đếm cặp A/B, gồm cả thiếu/chưa rõ; mỗi câu có 80 cặp phụ thuộc cùng nguồn |
| `exact_agreement`, `kappa` | Mô tả trên cặp nhãn xác định; kappa `null` khi không có cặp hoặc biên suy biến |
| `categorical_labels_observed` | Số nhãn không thiếu, tối đa 320; gồm “Chưa rõ”, có thể là dữ liệu QA nếu `is_fixture=true` |
| `human_labels_imported` | Nhãn người thật đã nhập; luôn bằng 0 trong chế độ kiểm thử giả lập |
| `quality_chart_allowed` | Chỉ bật khi có cả hai phiếu đã chọn và ít nhất một nhãn; hình QA vẫn phải mang nhãn giả lập |
| `receipt.json` | Hash code, kết quả, raw và selection của lần phân tích |

CSV thêm dấu nháy đơn trước chuỗi có thể bị spreadsheet thực thi như công thức. JSON
raw vẫn giữ nguyên từng giá trị; dấu bảo vệ trong CSV không phải người chấm sửa lời.

Không dùng file QA hoặc nhãn model của pilot cũ để điền chỗ trống trong phiếu thật.
Người chấm có thể thấy một số bản sửa giống bản gốc; không loại những bản đó vì không
thay đổi và không dùng độ khác ký tự làm điểm chất lượng.
