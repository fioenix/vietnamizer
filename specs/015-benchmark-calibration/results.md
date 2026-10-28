# Hiệu chỉnh Vietnamizer từ benchmark — 26/10/2026

**Đã sửa mã nguồn 0.11.1; chưa phát hành hoặc cài vào runtime.** Không chạy lại
benchmark, model chấm hoặc Jev. Hai Forms và dữ liệu lịch sử giữ nguyên.

## Những thay đổi đã làm

- Chốt2: khi nguồn mơ hồ, giữ phần chưa rõ hoặc hỏi; không tự quyết định thêm người,
  đối tượng, thứ tự hay cách nhóm làm đổi hành động. Gợi từ R020, chưa có nhãn ý định
  của tác giả nên ghi là rủi ro, không giả thành lỗi nghĩa đã được xác nhận.
- V19: khi chưa rõ người đọc/giọng cần đổi, giữ cách dùng thuật ngữ ổn định trong
  nguồn. Có từ tiếng Việt tương đương không đủ để dịch đồng loạt. Yêu cầu thuần Việt
  hoặc người đọc ngoài ngành đã rõ vẫn được xử lý theo quy tắc hiện hành.
- T2: thay dấu/cấu trúc tối thiểu và giữ quan hệ ý; thay từ phải có lý do riêng.
  Sửa ví dụ cũ không có em dash thành một cặp chỉ thay dấu. Không bỏ trigger em dash
  hiện hành từ quan sát benchmark: những thay thế đó đang phù hợp quy tắc hiện có.
- Jev: host vẫn rà core ở chỗ không flag, điểm thấp hoặc chưa kiểm; phán đoán trên
  nguồn không kết luận một bản sửa chưa được chấm. Không thay transport, recipe,
  lịch gọi hoặc threshold. R001 chưa chứng minh runtime có veto số.

Thêm BC01–BC10 trong calibration/ca-kiem-thu.md gồm ca dương và ca chống sửa quá tay.
Bảng này là kỳ vọng để kiểm bằng tay, chưa phải kết quả chạy model sau sửa. Bằng chứng
được ghi trong calibration/LOG.md trước khi sửa chỉ dẫn; nguồn/đầu ra là AI, nhãn là
nhận xét host, không phải bản vàng hoặc đánh giá độc lập của người bản ngữ.

## Kiểm chứng đã thực hiện

| Kiểm tra | Kết quả và phạm vi |
|---|---|
| build-jev-registry.py --check | 55 định nghĩa khớp; registry sinh lại giữ nguyên byte vì chỉ dẫn host sửa ở đây không đổi recipe phán đoán |
| validate-package.py | Hợp lệ v0.11.1, 55 pattern; SKILL488dòng, trong giới hạn550 |
| python3 -B -m unittest tests.test_jev | 33/33 test đạt; chỉ nhóm consumer registry/runner bị ảnh hưởng, không chạy toàn suite |
| Review độc lập | Không còn blocker về hợp đồng, phiên bản, mức bằng chứng và ca đối chiếu; review tĩnh, không phải chất lượng đầu ra |
| Bảo toàn lịch sử | 5.719 file dữ liệu benchmark/Forms/readiness giữ SHA256 như trước |
| git diff --check | Đạt trên thay đổi hiện hành |

Builder vẫn báo các regex lịch sử không có trong mục canonical tương ứng và không
đóng gói chúng; đây không phải lỗi mới hoặc pattern bị mất trong bản sửa này.

## Giới hạn còn lại

Chưa đo hiệu quả, tỷ lệ sửa đúng/sai, giữ giọng hoặc lợi ích vượt prompt thường sau
bản sửa. Cần tập nguồn mới độc lập để chứng minh chất lượng bản mới. Cả20nguồn
public-ai-v1 đã dùng cho hiệu chuẩn, nên là tập phát triển/hồi quy cho các phiên bản
sửa theo chúng; các kết quả0.11.0 giữ đúng phiên bản lịch sử, không gán sang0.11.1.

Source-before và observations.json nằm ở artifacts/015-benchmark-calibration-20261026.
Khi trình kiểm epoch cũ phát hiện canonical source đổi phiên bản, dùng snapshot/bundle
quy tắc0.11.0 để dựng lại; không đổi manifest cũ để hợp thức hóa nguồn mới.

Chưa chạy cổng phát hành, đóng gói sản phẩm, cài runtime, commit, push hay publish.
Đây là bản sửa nguồn có thể review, không phải một release đã được nghiệm thu.
