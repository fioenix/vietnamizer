# Bổ sung chế độ Vietnamizer + Jev

Ngày 25/10/2026, owner yêu cầu thêm chế độ thứ tư và ưu tiên Codex. Việc bổ sung phạm vi
đã được duyệt; owner đã chốt trần Jev **2 USD** và yêu cầu chạy Codex trước.
Runner riêng đã được triển khai, đang kiểm chứng và review trước lệnh gọi thật. Các kết quả ba chế độ trước vẫn giữ nguyên.

## Phép so sánh

Giữ 20 văn bản giả lập đã đóng băng. Với mỗi văn bản, dùng bản Vietnamizer từ đợt Codex
đã chạy làm bản nháp chung, rồi tạo hai bản cuối trong hai cuộc hội thoại mới:

- Vietnamizer tự rà: nhận nguồn, ngữ cảnh và bản nháp, có một lượt sửa tiếp.
- Vietnamizer + Jev: nhận cùng dữ liệu, thêm phán đoán Jev đã kiểm tra hợp lệ, có một lượt sửa tiếp.

Hai nhánh dùng cùng prompt nền, model và cấu hình; phần khác biệt là dữ liệu tư vấn Jev.
Đây là đối chứng cho việc bổ sung Jev vào bước rà bản nháp. Nó không đo một workflow tương tác
nhiều vòng tùy ý. Jev chỉ tư vấn; Codex giữ quyền biên tập, không tự áp hoặc chặn sửa theo điểm số.
Nguồn, ngữ cảnh và đề xuất sửa phải được chuẩn bị theo hợp đồng hiện hành của runner.

Đợt bổ sung cần tối đa 40 lượt Codex: 20 bản tự rà và 20 bản có Jev. Bản tự rà thay vị trí
Vietnamizer trong bảng so sánh bốn chế độ của đợt bổ sung; bản nháp cũ vẫn là bằng chứng riêng.
Bảng này có 80 bản cuối: 40 bản không skill/prompt thường đã có, 20 bản tự rà và 20 bản có Jev.
Phải công bố việc hai baseline cũ được tái sử dụng và số lượt biên tập khác nhau giữa các chế độ.
Chỉ cặp tự rà/có Jev có số lượt tương ứng; không gọi toàn bảng là thí nghiệm kiểm soát số lượt.

Đóng băng manifest mới, liên kết digest tới nguồn/bản nháp cũ; không sửa manifest đã chạy.
Kiểm tra model/runtime có thay đổi trước lượt mới; nếu có, tách đợt và giới hạn kết luận tương ứng.
Trần 132 lần thử của đợt cũ không tự mở rộng: đề xuất mới có sổ riêng, tối đa 40 lần thử Codex,
640 request Jev, không tự retry. Quota Codex vẫn dùng gói hiện có, không bật tuyến API trả tiền.

## Ngân sách Jev đã được duyệt: trần 2 USD

Ghim `jev-1.14.0`. Theo [bảng giá chính thức](https://docs.typesafe.ai/models), kiểm tra ngày
25/10/2026, giá là 0,042 USD/triệu input token, output miễn phí; context mặc định tối đa 64k
token mỗi request. Không bật long context. Runner hiện giới hạn 32 request cho mỗi lần đánh giá.

Cho phép một lần đánh giá mỗi văn bản: 20 × 32 = tối đa 640 request. Dự phòng 65.536 input
token cho từng request, kể cả request lỗi chưa rõ billing: 640 × 65.536 × 0,042 / 1.000.000
= 1,76160768 USD. Làm tròn trần thành **2 USD**. Đây là dự phòng theo giới hạn context được
công bố, không phải lượng token đã đo trên corpus hay cam kết mức nạp tiền tối thiểu của tài khoản.
Chưa kiểm tra số dư, thuế hay yêu cầu nạp tiền của tài khoản. Phần dự phòng còn lại không dùng
để tự thêm request, retry hoặc gọi evaluator khác.

Trước mỗi request, giữ khoản dự phòng 65.536 token; chỉ giải phóng phần chênh khi có usage
hợp lệ. Request lỗi không rõ billing giữ nguyên dự phòng. Dừng nếu không còn ngân sách,
rate limit, hết deadline, phản hồi không hợp lệ hoặc tuyến tài khoản không đúng; không tự
chuyển provider, model, long context hay mua thêm credit. Ghi chi phí tính từ usage tách với
hóa đơn thực tế nếu chưa đối soát được. Xác minh giá và giới hạn còn đúng trước khi chạy.

32 request là trần, không phải chỉ tiêu cần dùng hết hay bằng chứng đã kiểm tra đầy đủ.
Smoke một văn bản trước, kiểm tra coverage, trường hợp thiếu/không chắc và chi phí thực.
Coverage thiếu phải được báo; không đổi thành pass và không tự tăng ngân sách để làm đầy.
Jev không được làm giám khảo duy nhất cho chế độ có chính nó; vẫn cần hai người chấm độc lập,
ẩn tên chế độ. 20 văn bản này là tập phát triển, chưa đủ cho tuyên bố thắng trên văn bản mới.

## Antigravity

CLI trên máy hiện vẫn bị chặn bởi automatic approval review; chưa chạy tiếp. Có 10 bản Gemini
hợp lệ và một lần thử bị cách ly; chưa biết phạm vi file đã đọc trong lần đó.
[Phương án Docker cách ly](isolation-gate.md) chưa được duyệt, dựng hay kiểm chứng đăng nhập.
Không chạy lại lệnh bị từ chối hoặc cấp quyền `git status` để vượt chặn. Chỉ nối lại khi owner
duyệt phương án cách ly và kiểm tra thực tế đạt; khi đó chạy lại trọn bộ Gemini trong đợt riêng.
Ngân sách Jev 2 USD ở đây chỉ dành cho Codex, không bao gồm Jev trên Gemini.


## Điều chỉnh protocol v2 sau smoke, trước đầu ra Codex mới

Smoke v1 thu 21 phản hồi hợp lệ ở P01 rồi gặp một lỗi request; P02 lỗi ngay request đầu.
Tổng 23 request đã được giữ nguyên, gồm hai request chưa rõ billing. Chưa có bản Codex nào
được tạo ở thời điểm điều chỉnh này. Endpoint liệt kê model trả HTTP 200, nhưng bằng chứng
đó chưa xác định nguyên nhân lỗi endpoint inference. Không gọi lại hai lần đánh giá này.

Harness còn có lỗi so digest: digest input của core giữ thứ tự trường JSON, còn digest trong
manifest sắp xếp khóa. V2 kiểm từng loại theo đúng encoding của nó; không sửa digest hay seal
của kết quả cũ. Một test end-to-end giả lập đã kiểm prepare, tiếp nhận bằng chứng cũ, sửa bản
nháp, báo cáo và resume mà không gọi lại evaluator hoặc reset ngân sách.

Đợt v2 dùng manifest/thư mục mới; giữ bản chụp source v1 và đóng băng digest các file gốc.
Nó tiếp nhận nguyên byte ledger, raw request/response và evaluation/seal cũ, đối soát cả
request lỗi. Chỉ checks được core xác nhận hợp lệ và đối chiếu raw response mới được gửi cho
Codex. Giữ nguyên bản nháp, prompt chung, model và cấu hình. Không chọn lại đầu ra cho đẹp.

Bảng tổng giữ đủ 20 văn bản theo phạm vi dự định, đồng thời tách mức tiếp nhận tư vấn:

- `full`: Jev đã hoàn tất phạm vi kiểm tra được runner xác nhận.
- `partial`: Có tư vấn hợp lệ, nhưng còn checks thiếu hoặc lỗi dịch vụ.
- `unavailable`: Đã thử nhưng không có tư vấn hợp lệ; Codex nhận trạng thái thiếu tư vấn.
- `not_attempted`: Chưa gọi Jev vì circuit breaker đã dừng dịch vụ.

Hai nhánh Codex vẫn có cùng một lượt sửa từ chung bản nháp. Nhánh thứ tư có thể trả bản
fallback khi không có tư vấn, nhưng phải ghi đúng là **không nhận treatment Jev**. Payload
báo thiếu tư vấn cũng có thể ảnh hưởng cách sửa; không quy khác biệt đó cho phán đoán Jev.
Phân tích tác dụng Jev chỉ dùng các cặp thực sự nhận tư vấn và vẫn công bố bảng tổng cùng lỗi.
Đây là điều chỉnh pilot phát triển, chưa phải thí nghiệm holdout đã đăng ký trước.

Circuit breaker: nếu thêm một văn bản gặp request lỗi sau P01/P02, ngừng Jev cho mọi văn bản
còn lại và ghi `not_attempted_service_stop`. Không retry hoặc mua thêm credit. Tổng chi phí
được cộng xuyên đợt v1/v2; trần 640 request và 40 Codex starts không được reset khi chuyển đợt.


**Giới hạn chẩn đoán:** wrapper hiện gom lỗi transport, validation và lưu artifact thành
`service_failed`; raw reply lỗi chưa được giữ đủ để phân biệt ba nhóm đó. Vì vậy chỉ kết luận
được request không được xác thực, chưa xác định nguyên nhân. Ba khoản dự phòng vẫn giữ đủ.
Những phản hồi hợp lệ còn raw payload/reply và được đối soát lại; thiếu chẩn đoán ở request
lỗi không biến các phản hồi hợp lệ ấy thành một lượt đánh giá đã hoàn tất.
