# Tái dựng hình trong README

Hai hình dùng lại báo cáo đã có, không gọi model hoặc sửa dữ liệu nghiên cứu:

- `regression-cases.svg`: MR01–MR12, so 0.12.0 với 0.12.1 trên cùng Codex.
- `reference-voice.svg`: lựa chọn cặp D–C của pilot 0.13.2; cùng Codex biên tập, Codex/Gemini là giám khảo.

`evidence.json` chứa nhãn/count được trích từ hai báo cáo và SHA-256 của báo cáo. Các tổng
được tính từ từng ca hoặc hàng kết quả; phiếu thiếu được giữ riêng. `brand-tokens.json`
là bản xuất token màu FINOLABS, giúp người dựng lại không cần repo thiết kế local.

## Kiểm dữ liệu, không cần thư viện vẽ

Chạy từ root repo:

```bash
python3 docs/figures/render.py --check-data
```

Nếu báo cáo thay đổi, lệnh sẽ báo lệch. Đọc lại bằng chứng và lý do thay đổi trước khi dùng
`--refresh-data`; thao tác này chỉ trích lại dữ liệu từ báo cáo, không chấm lại hoặc chạy benchmark.

## Dựng SVG và bản xuất PDF/PNG

Bộ vẽ tùy chọn cho maintainer dùng Python 3.12 và Matplotlib 3.10.8, với dependency đã pin/hash-lock.
Nó không nằm trong payload, dependency hoặc bước cài của người dùng Vietnamizer.

```bash
uv venv output/readme-figures-venv --python python3.12
uv pip install --python output/readme-figures-venv/bin/python --require-hashes -r docs/figures/requirements.lock
MPLCONFIGDIR=output/readme-figure-cache output/readme-figures-venv/bin/python docs/figures/render.py --export-dir output/readme-figure-exports
```

Mỗi hình có bản ngang và bản `-mobile` cho màn hình hẹp; cả hai được nhúng bằng `picture` trong README.
Các SVG được ghi tại đây; PDF và PNG 300 DPI nằm trong thư mục xuất được chỉ định.
Dùng cùng lockfile và môi trường để so bytes SVG; metadata thời gian được tắt, hash salt được cố định.
Matplotlib dùng font DejaVu Sans có hỗ trợ tiếng Việt và chuyển glyph thành vector trong SVG.

## Cách đọc

Hình hồi quy không phải độ chính xác trên quần thể và không đo lại bản 0.13.2. Hình giọng mẫu
không so hai agent biên tập; hai hàng là model chấm cùng đầu ra Codex. Hình giữ đủ tám nguồn
dự kiến ở mỗi hàng, kể cả phiếu Gemini bị loại. Không dựng CI hoặc p-value từ các ca phát triển
này. Các giới hạn đầy đủ nằm trong [tài liệu benchmark](../benchmarks.md) và báo cáo gốc.
