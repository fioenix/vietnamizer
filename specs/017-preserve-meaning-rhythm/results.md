# Giữ nghĩa và nhịp: thay đổi đã triển khai

**Ngày 27/10/2026 · source/gói local 0.12.1 · Chưa cài hoặc phát hành.**

Đã triển khai hướng hiệu chỉnh được chủ nhân duyệt từ phân tích Mindfio. Mục tiêu
là ngăn biên tập tự chọn một ý mới hoặc làm mất nhịp; không dùng các quan sát này
để bổ sung sở thích cá nhân vào quy tắc chung hoặc tuyên bố chất lượng đã tăng.

## Quy tắc đã đổi

- Chốt giữ nghĩa đối chiếu thêm ý muốn/khả năng/nghĩa vụ, phạm vi lượng và đối tượng
  được thêm vào. Câu sau trôi chảy hơn không cho phép giải mơ hồ thay tác giả.
- V1 và mục phân biệt câu ngắn giữ đối tượng lược đã rõ hoặc bỏ lửng có chức năng.
  Đã bỏ mâu thuẫn yêu cầu mọi câu `soạn xong rồi dừng` phải nhắc lại đối tượng.
  V20 vẫn giữ yêu cầu hoàn chỉnh từ hai tiếng và thành phần thực sự cần cho ý câu.
- T2 xét chức năng dấu, quan hệ ý và quy chuẩn đã giao; không tự coi `—` là lỗi.
  Thay dấu phải giữ điểm ngắt/quan hệ; không tự ghép cụm kết vào quan hệ giải thích.
  Các trường hợp lời thoại, khoảng, tên riêng, code và vùng bảo toàn vẫn được giữ.
- Làm rõ trích dẫn nguyên văn khác thuật ngữ chỉ đặt trong ngoặc để nhấn. Phần
  chưa rõ có phải nguyên văn hay không vẫn giữ byte; T3 chỉ thống nhất dấu trong
  phần được phép, không cho đổi chữ hoặc thực thi chỉ thị trong nguồn.
- Thêm bước rà mạch đoạn để nhận ra ứng viên gần lặp ý, tách phần nghĩa riêng và
  chỉ nêu đề xuất cần tác giả quyết định trong đúng phạm vi rà/nhận xét. Không tự
  xóa hoặc chèn ghi chú vào tác vụ chỉ yêu cầu bản cuối.

Root `SKILL.md` vẫn canonical. Bảng T2, changelog và hai plugin manifest đồng bộ
0.12.1. Câu hỏi English V1/T2/T3 cập nhật theo cùng điều kiện, registry sinh lại qua
script chuẩn; thay đổi định nghĩa giới hạn ở V1/V20/T2/T3. Giữ 55 ID, loại câu hỏi,
Choice criteria, runtime, transport và ngưỡng như cũ; scanner chỉ là tín hiệu xem lại.

## Ca hồi quy và mức bằng chứng

[MR01–MR12](../../calibration/ca-kiem-thu.md) gồm ca từ Mindfio, ca tổng hợp và một
ca lai có điều kiện giả lập được ghi rõ. Có ca bảo toàn câu ngắn, ý muốn, phạm vi
lượng, dấu ngắt, quan hệ giải thích, trích dẫn; có ca dương sửa bổ ngữ và quy chuẩn
trình bày cụ thể. TO01/BC05 cũ được làm rõ điều kiện để không còn ép sửa vì mã dấu.

Bằng chứng đã ghi trong `calibration/LOG.md` trước khi đổi quy tắc. Hash nguồn,
candidate, vị trí ký tự và ánh xạ đầy đủ 12 ca lưu trong `observations.json` của
đợt hiệu chỉnh. Nhãn kỳ vọng do host đề xuất; việc chủ nhân duyệt hướng triển khai
không được trình bày như chấm từng câu hoặc viết lại bản vàng.

Các nguồn Mindfio đã được dùng để hiệu chỉnh trở thành dữ liệu phát triển/hồi quy
cho các bản sửa theo chúng. Không dùng lại làm holdout độc lập để quảng bá bản mới.
Không thay source, prompt, output, chart hoặc biên nhận của các đợt benchmark cũ.

## Kiểm chứng đã chạy

| Mục | Kết quả và giới hạn |
| --- | --- |
| Parity RED | Source validator exit1 sau khi sửa recipe/canonical nhưng chưa sinh lại registry; raw lỗi được lưu. Đây là lỗi parity được tái hiện, không phải phép đo sửa nghĩa |
| Test mục tiêu trên source cuối | 41/41 đạt: 33 test Jev offline với transport giả lập; 8 test source-gate/package liên quan. Không gọi API thật hoặc chạy full suite |
| Validator/registry | Source v0.12.1 hợp lệ, 55 định nghĩa khớp canonical; các cảnh báo scanner cũ vẫn được giữ và loại khỏi payload tín hiệu như trước |
| Đóng gói | Script plugin build thành công; kiểm thực tế cả ba ZIP: đúng một skill, SKILL/registry/LOG/cases trùng byte với source, không có benchmark/hồ sơ riêng trong payload |
| Review độc lập | Không có finding còn mở về nghĩa, câu ngắn, T2/T3, bảo toàn dữ liệu, output contract, recipe/case parity; chỉ review tĩnh, không chấm model |
| Bảo toàn | 23.469 file artifact/benchmark/spec lịch sử được đối soát SHA256: không mất hoặc đổi file nào. Hai Forms không được truy cập/sửa |
| Dòng source | SKILL.md 498 dòng, dưới giới hạn 550; số pattern không đổi |

Không chạy lại benchmark, Jev API hoặc model để kiểm hành vi sau sửa. Vì vậy không
có tỷ lệ sửa đúng, tỷ lệ sửa quá tay, nhãn tác giả mới hoặc bằng chứng định lượng
rằng 0.12.1 tốt hơn 0.12.0. MR01–MR12 là kỳ vọng hồi quy được review tĩnh, chưa phải
12 ca model đạt. Không cài runtime, chạy cổng release ngoài, commit, push hoặc phát hành.

## Dữ liệu bàn giao

`artifacts/017-meaning-rhythm-calibration-20261027/` giữ source trước/sau, patch chỉ
phần thay đổi trong lượt này, ánh xạ ca/ngữ cảnh/hash, raw lệnh RED/green, package
bytes và biên nhận review/bảo toàn. Gói dữ liệu có manifest kiểm hash riêng để xem
lại mà không dùng quota. Các gói skill/plugin local nằm trong `dist/`.

Workflow: Spec Kit017, tasks/implement vì có ranh giới quote/registry/distribution;
đã đọc canonical Vault qua Obsidian CLI. Mốc review-by của workflow đã hết từ21/10;
Orrery không có callable tool trong phiên để đối chiếu. Không có ghi chú Vault hoặc
Orrery được tạo/sửa và không có extension hook được cấu hình cho đợt này.
