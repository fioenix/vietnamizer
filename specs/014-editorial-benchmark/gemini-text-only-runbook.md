# Chạy 80 đầu ra Gemini với agent riêng

## Lệnh chạy

```sh
python3 /Users/fioenix/Projects/vietnamizer/benchmarks/gemini_text_only.py run
```

Đã nghiệm thu một cell thật trong đợt mới: R002-bare, đúng Gemini 3.8 Flash medium,
đúng agent riêng, chỉ có bước trả JSON `finish`. Lệnh trên bỏ qua cell này và chạy
79 cell còn lại, bắt đầu R011-ordinary. Không chạy lại script `gemini_manual.py` cũ.

Kết quả lưu tại:

```text
/Users/fioenix/Projects/vietnamizer/artifacts/014-gemini-text-only-20261026/epoch-v3/
```

Dùng đúng 80 prompt đã đóng băng từ bộ Codex: 20 nguồn công khai, bốn chế độ, một
pass tạo bản cuối. Advice Jev dùng lại nguyên bản, không gửi request Jev mới. Mỗi
cell là một phiên mới, thứ tự seed 25034; không đổi model hay dùng API/credit trả phí.

## Nguyên nhân hai probe trước bị chặn

`init.tools` của CLI1.4.7 liệt kê registry chung 60 mục, không phản ánh trực tiếp
whitelist của agent đang chọn. Đối chứng với cùng model/prompt/body/fixture cho thấy:

| Cấu hình | Kết quả | Tool thực tế |
|---|---|---|
| Agent benchmark, whitelist `finish` | Trả `UNAVAILABLE`, không biết token trong fixture | Chỉ `finish` |
| Clone thêm `view_file` theo tên trong registry/tài liệu | Trả `UNAVAILABLE` | Chỉ `finish` |
| Clone thêm `read_file`, tên quan sát trong event runtime | Đọc đúng token trong fixture, không có trong prompt | `read_file` hoàn tất, rồi `finish` |

Cả ba vẫn quảng bá 60 mục. Token được đối chiếu nguyên chuỗi sau khi bỏ một LF cuối
file giả. Các phép thử này là chẩn đoán capability, không phải đầu ra chất lượng.
Hai file agent đối chứng tạm đã được dọn sau khi kiểm byte với bản sao giữ trong
artifact. Agent benchmark giữ riêng; không đổi agent mặc định hay shared permissions.

Guard mới chấp nhận registry chỉ khi khớp bằng chứng đối chứng, agent, model và
phiên bản/binary/definition đã pin. Mọi operational tool call, subagent, từ chối
quyền, lỗi schema hoặc timeout vẫn khiến lượt bị loại và đợt dừng. Đây là kiểm
chứng đọc file có đối chứng cùng giám sát stream, không phải sandbox OS hay phép
thử vét cạn mọi tool. Raw được ghi ngoài workspace của agent.

## Dữ liệu và tiếp tục

Mỗi cell giữ prompt vào wrapper, argv/prompt thực tế native, stdout/stderr nguyên
byte cả hai lớp, init, exit/signal/timeout, usage, conversation ID, kết quả parse
và seal checksum. CLI không cung cấp HTTP body nội bộ của provider.

`source-snapshots/` giữ các bản code thực thi; `capture/capability-contract.json`
trỏ tới bằng chứng đối chứng. `report.json` giữ số hoàn tất; `handoff-receipt.json`
ghi nghiệm thu live smoke. Không gọi Forms/Apps Script; không sửa Codex/ảnh/ID form.

Chạy lại cùng lệnh chỉ tiếp tục cell chưa bắt đầu; không retry cell lỗi/dở dang.
Nếu hết quota hoặc phát sinh lỗi, giữ nguyên STOP/raw để đối soát, không xóa cờ.
Tổng đợt mới tối đa 80 model starts. Hai lượt host cũ, hai preflight 0 turn/0 token
và ba lượt chẩn đoán capability được giữ riêng; không trộn vào 80 đầu ra mới.

15 test Python và 5 test Node đã qua; review độc lập đã đọc raw đối chứng. Status
đã kiểm từ ngoài repo: 1/80. Chưa chạy đủ 80 và chưa có kết luận chất lượng.
