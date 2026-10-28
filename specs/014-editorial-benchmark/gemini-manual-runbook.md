# Bộ Gemini host cũ — giữ làm chẩn đoán

**Dừng dùng lệnh bên dưới:** R011 đã gọi tool và đợt cũ giữ làm chẩn đoán. Xem [trạng thái agent riêng](gemini-text-only-status.md); CLI mới chưa nghiệm thu.

Đây là script để Fio tự chạy trên host qua Agybird. Codex chỉ chuẩn bị và kiểm thử
offline; không khởi chạy Antigravity, không gỡ hoặc thay đổi quyết định duyệt công cụ.

## Một lệnh để chạy

```sh
python3 /Users/fioenix/Projects/vietnamizer/benchmarks/gemini_manual.py run
```

Cần có `python3`, Node, Agybird 0.3.0 ở đường dẫn đã cài và CLI `agy` đã đăng nhập.
Script dùng Gemini 3.8 Flash medium, một phiên mới cho mỗi đoạn/chế độ, tối đa 80 lượt.
Thứ tự 80 lượt được xáo bằng seed 25034. Cùng 20 nguồn công khai và đúng 80 prompt
của bộ Codex được giữ nguyên từng byte, bao gồm advice Jev đã có. Không gọi Jev thêm.

Kết quả được lưu bền vững tại:

```text
/Users/fioenix/Projects/vietnamizer/artifacts/014-gemini-manual-20261026/
```

Thư mục làm việc của model nằm riêng trong `/private/tmp`, chứa dữ liệu của đúng
lượt đang chạy; không nằm dưới repo. Đây không phải sandbox. Ngữ cảnh global do
Antigravity tự nạp chưa được cô lập hay xác thực. Script giữ quyền native hiện có,
không tự cấp quyền, thay sandbox hoặc bật credit.

## Khi chạy lại hoặc gặp lỗi

Chạy lại cùng lệnh chỉ tiếp tục các lượt chưa bắt đầu. Lượt đã hoàn tất phải có seal
và checksum hợp lệ. Nếu có lỗi, hết quota, từ chối quyền, tool, subagent hoặc timeout,
script lưu raw và dừng. Lượt dở dang không được tự gọi lại; giữ nguyên `STOP.json`,
`RUNNING.lock` còn sót hoặc dữ liệu lỗi để kiểm tra. Không tự xóa chúng để chạy lại.
Script không tự đổi model hoặc chuyển sang API/credit trả phí.

Xem tiến độ bằng lệnh không gọi model:

```sh
python3 /Users/fioenix/Projects/vietnamizer/benchmarks/gemini_manual.py status
```

## Dữ liệu được giữ

- Manifest, bản gốc, provenance, 80 prompt và hash công cụ.
- Mỗi lượt: prompt gửi vào wrapper, argv thực tế của native CLI, stdout/stderr nguyên
  byte của native và wrapper, thời gian, exit/signal/timeout, usage và model nếu có.
- Kết quả đã parse, seal checksum và số lượt hoàn tất trong `report.json`.
- Bản đối soát 4.323 file Codex trước khi chạy và sau mỗi lượt thành công.

CLI không cung cấp HTTP body nội bộ của provider; không mô tả stream CLI thành raw
HTTP. Script không sao chép credential, keyring hay token và không dump môi trường.
Raw cùng UID không chống được sửa giả có chủ đích; checksum dùng để phát hiện thay đổi.

Script không gọi Google Forms/Apps Script, không sửa bộ Codex hoặc ảnh/ID đang chấm.
Kết quả Gemini giữ thành đợt riêng. Chưa có nhãn chất lượng hay kết luận Gemini tốt hơn.

## Phạm vi kiểm chứng

Bảy kiểm thử Python dùng tiến trình giả lập kiểm tra giới hạn, resume, schema, credit,
thu raw, seal và ngắt giữa chừng. Sáu kiểm thử Node kiểm raw theo byte, timeout,
validation và process group; phép thử process group cần quyền chạy `ps`. Review độc
lập đã xử lý hai lỗi về ngắt tiến trình và schema. Chưa chạy thử với provider thật.

### Sửa lỗi thư mục terminal — 26/10/2026

Phần đối soát đường dẫn tương đối đã được sửa để luôn lấy gốc repo, không phụ thuộc
thư mục terminal. Tám test Python qua; lệnh status chạy từ `/private/tmp` trả 0/80.
Chưa có lượt nào bắt đầu nên manifest chuẩn bị được cập nhật riêng hash driver; bản
cũ giữ ở `manifest.before-cwd-fix.json`, chi tiết ở `cwd-fix-receipt.json`. 85 file
đầu vào và 4.323 file Codex giữ nguyên hash. Không thay Forms hay gọi provider.

### Đối soát stream native — 26/10/2026

Lượt đầu R002-bare do Fio chạy đã trả SUCCESS, exit 0, không timeout và chỉ có bước
finish. Parser cũ chỉ đọc khóa `type`, trong khi CLI 1.4.7 trả khóa `event`; kết quả
bị gắn nhầm là unknown_event. Parser đã hỗ trợ cả hai, từ chối khóa xung đột.

Đã đối soát raw có seal với kết quả wrapper, nhận lại 1/80 mà không gọi model lần nữa.
Raw, result lỗi, seal và STOP gốc giữ nguyên. Bản đối soát nằm trong
`reconciliations/R002-bare.json`; manifest cũ và biên bản sửa được giữ riêng. Chạy lại
cùng lệnh sẽ bỏ qua R002-bare và bắt đầu R011-ordinary, không yêu cầu xóa STOP.
Mười test Python qua; review độc lập kiểm tra lại cả raw thật. Codex và Forms giữ nguyên.
