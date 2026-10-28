# MR01–MR12: so sánh 0.12.0 và 0.12.1 trên cùng Codex

Ngày 27/10/2026. Hoàn tất **28/28 đầu ra**, từ 14 tình huống cho hai phiên bản;
MR10 và MR11 có hai nhánh nên được gộp về **12 ca hồi quy**. Theo tiêu chí khóa
trước khi chạy, **0.12.0 đạt 10/12 ca; 0.12.1 đạt 12/12 ca**. MR05 và MR12
chuyển từ chưa đạt sang đạt. Không có ca chuyển từ đạt sang chưa đạt trong lượt này.

Đây là kiểm tra trên tập phát triển đã dùng để sửa skill, mỗi điều kiện chỉ có
một đầu ra. Nhãn do agent đọc và đối chiếu với tiêu chí đề xuất, có kiểm tra chéo
bằng một reviewer riêng; không phải nhãn tác giả, chấm người độc lập hay bằng
chứng rằng mọi lỗi lịch sử đã được khắc phục ổn định. “Đạt” chỉ nói về yêu cầu
hồi quy của ca đó, không chứng nhận mọi lựa chọn biên tập trong đầu ra đều tối ưu.

| Ca | Nội dung kiểm tra | 0.12.0 | 0.12.1 | Quan sát |
| --- | --- | --- | --- | --- |
| MR01 | Không tự điền một nỗi sợ vào câu rút gọn | Đạt | Đạt | Cả hai giữ “Mà chạy để tránh đối diện.”; lỗi cũ không tái hiện |
| MR02 | Không đổi ý muốn thành khả năng | Đạt | Đạt | Cả hai giữ tiêu đề chứa “cái gì cũng muốn làm” |
| MR03 | Giữ phạm vi lượng | Đạt | Đạt | Giữ “một số đầu việc” |
| MR04 | Bổ sung bổ ngữ thật sự cần | Đạt | Đạt | Cả hai sửa thành “không tìm thấy chìa khóa” |
| MR05 | Giữ điểm ngắt có chức năng | **Chưa đạt** | **Đạt** | Bản cũ đổi dash sau “Tất cả” thành dấu phẩy; bản mới giữ dash |
| MR06 | Không thêm quan hệ giải thích bằng dấu câu | Đạt | Đạt | Bản cũ bỏ dash nhưng còn dấu chấm; bản mới giữ nguyên. Không bản nào đổi thành dấu hai chấm |
| MR07 | Áp quy chuẩn không dùng em dash | Đạt | Đạt | Cả hai tách thành hai câu, giữ mốc tuần sau |
| MR08 | Giữ khoảng năm, lời thoại, mã và code | Đạt | Đạt | Toàn bộ đầu vào được giữ nguyên byte |
| MR09 | Phân biệt nhấn thuật ngữ với trích nguyên văn | Đạt | Đạt | Giữ nội dung; cả hai chưa thống nhất ngoặc, vốn là lựa chọn tùy ngữ cảnh |
| MR10 | Giữ trích dẫn đã xác nhận hoặc chưa rõ | Đạt | Đạt | Nhánh đã xác nhận giữ nguyên; nhánh chưa rõ: bản cũ hỏi, bản mới giữ nguyên |
| MR11 | Tách nhận xét khỏi bài; giữ sắc thái riêng | Đạt | Đạt | Cả hai nhánh đều đạt; cả hai bản nhận ra chỗ gần lặp khi được giao nhận xét |
| MR12 | Không lặp lại đối tượng đã lược hợp lệ | **Chưa đạt** | **Đạt** | Bản cũ thêm “bản hướng dẫn”; bản mới giữ câu ngắn |

## Hai thay đổi quan sát được

**MR05 — giữ điểm ngắt.**

- Gốc: `Tất cả – chỉ khác là gắn thêm một chiếc nhãn thông minh hơn để cảm thấy yên tâm rằng mình đã đơn giản hoá.`
- 0.12.0: `Tất cả, chỉ khác là gắn thêm một chiếc nhãn thông minh hơn để cảm thấy yên tâm rằng mình đã đơn giản hoá.`
- 0.12.1: giữ nguyên câu gốc.

Không có quy chuẩn buộc đổi dấu trong ngữ cảnh này. Nhãn chưa đạt bám tiêu chí
giữ điểm ngắt của ca MR05; không có nghĩa dấu phẩy luôn sai trong tiếng Việt.

**MR12 — giữ đối tượng lược và nhịp câu.**

- Gốc: `Tôi đang soạn hướng dẫn bàn giao. Soạn xong rồi dừng.`
- 0.12.0: `Tôi đang soạn hướng dẫn bàn giao. Soạn xong bản hướng dẫn rồi dừng.`
- 0.12.1: giữ nguyên câu gốc.

Đối tượng của “soạn” đã rõ từ câu trước. Cùng lúc đó, ca dương MR04 vẫn được
cả hai phiên bản sửa đúng; bản mới không giữ nguyên mọi câu ngắn một cách máy móc.

## Những gì chưa chứng minh được

MR01, MR02 và cách thêm dấu hai chấm ở MR06 từng được quan sát trong bài đầy đủ,
nhưng không tái hiện ở nhánh 0.12.0 của lượt trích đoạn này. Vì vậy không tính ba
ca đó là lỗi vừa được sửa thành công. MR06 cho thấy bản mới giữ nhịp sát nguồn
hơn, nhưng cả hai vẫn đạt yêu cầu bắt buộc không tự thêm quan hệ giải thích.

MR09 không bắt buộc phải thống nhất ngoặc. MR11 chỉ cho phép nêu ứng viên gộp
khi được giao nhận xét; cả hai bản đều làm được, không tạo thêm một “chiến thắng”
cho 0.12.1. Ở MR10 chưa rõ, câu hỏi của bản cũ là cách xử lý an toàn nhưng chưa
phải bản bài hoàn chỉnh; bản mới giữ nguyên chuỗi chưa rõ chức năng.

Có lựa chọn ngoài trọng tâm ca cần người viết cân nhắc: nhận xét MR11 của
0.12.1 dùng đại từ “mày” dù đầu vào không quy định xưng hô với người giao việc.
Điều này không thuộc tiêu chí hồi quy bắt buộc đã khóa, nên không đổi nhãn sau
khi xem kết quả và không coi 12/12 là chứng nhận toàn bộ đầu ra hoàn hảo.

Không lấy chênh lệch này làm mức cải thiện chất lượng chung, không kiểm định
ý nghĩa thống kê, không so Codex với Gemini và không suy luận hiệu quả Jev.
Ngữ cảnh trích đoạn và yêu cầu cụ thể có thể giúp cả hai bản tránh lỗi tốt hơn
khi xử lý bài dài; biến thiên giữa các lần sinh chưa được đo.

## Cấu hình và bằng chứng

- Cùng CLI `codex 0.164.0`, yêu cầu `gpt-6.1-sol`, effort `medium`, đăng nhập
  ChatGPT; backend thực tế không được CLI chứng thực độc lập.
- Hai snapshot đầy đủ cho phạm vi đã chọn; trong mỗi cặp chỉ `SKILL.md` khác
  phiên bản. Profile, card, tài liệu tra, nguồn, ngữ cảnh và yêu cầu giống nhau.
- Câu trả lời kỳ vọng, nhãn, ID ca và candidate lỗi cũ không nằm trong prompt.
- 28 phiên mới độc lập, thứ tự khóa bằng seed, tối đa hai lượt đồng thời;
  không gọi tool, Jev, chạy lại hay chọn mẫu đẹp.
- Raw là stdin/stdout/stderr CLI theo byte, schema, argv, session, usage,
  thời gian và trạng thái. Không có raw HTTP của nhà cung cấp; không suy chi phí
  tiền từ token dùng qua subscription.
- 15 test offline của runner và helper liên quan đã qua. Không chạy full suite.
- Đối soát **23.538 file lịch sử: không có file đổi hash hoặc bị mất**.
  Source skill vẫn 0.12.1; benchmark cũ không bị sửa. Hai Forms không được truy cập hoặc sửa.

Dữ liệu local: `artifacts/018-mr-version-comparison-20261027-v1/` gồm
`manifest.json`, `scenarios.json`, `rubric.json`, `sources/`, `prompts/`,
`attempts/`, `ratings.json`, `case-results.csv`, `summary.json` và
`before-after.html`. Mỗi nhãn gắn hash nguồn/đầu ra và trích bằng chứng.

Tái đối soát raw, bảng nhãn đã lưu và dữ liệu lịch sử, không gọi model:

```sh
python3 -B artifacts/018-mr-version-comparison-20261027-v1/reproduce.py
```

Lệnh tái lập tổng hợp từ nhãn đã lưu, không tự tái tạo phán đoán ngữ nghĩa.
Chi tiết protocol nằm trong [plan](plan.md), tiêu chí gốc nằm trong
[bảng MR01–MR12](../../calibration/ca-kiem-thu.md#mr01mr12--giữ-nghĩa-và-nhịp-sau-rà-mindfio).
