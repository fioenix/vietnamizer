# Chấm độc lập bản biên tập từ nguồn AI công khai

Đợt dữ liệu ngày 25/10/2026 dùng 20 câu trả lời nguyên văn từ
[TTP01/Vietverse-SFT-Preview](https://huggingface.co/datasets/TTP01/Vietverse-SFT-Preview),
revision `6b4e4a86e3b399318ac4fe91b2bbe64501037f40`, giấy phép Apache 2.0 theo thẻ dữ liệu.
Bên phát hành ghi `source_type=synthetic_llm` và giữ dấu vết xử lý từng mẫu. Chưa có
raw API, system prompt hoặc tên model sinh nguồn được đối soát. Đây là bằng chứng công bố
của bên phát hành, không phải kết quả phát hiện AI qua văn phong.

Bản gốc là toàn bộ phần trả lời assistant, không phải văn bản được agent soạn lại hoặc
cố tình cài lỗi. Hồ sơ giữ cả câu hỏi gốc, metadata, nguyên bản 100 dòng, thẻ dữ liệu,
revision, SHA-256 và quyết định tuyển/loại cho từng dòng. Lấy 20 mẫu đầu đạt điều kiện theo
thứ tự gốc trước khi biên tập; không chọn theo chất lượng đầu ra. Bộ dữ liệu đã tuyển chọn
để huấn luyện hội thoại, chỉ có một bên phát hành và chưa xác định mức trùng với dữ liệu
huấn luyện model biên tập. Vì vậy, không suy rộng kết quả ra mọi văn bản tiếng Việt.

## Phép so sánh

Mỗi nguồn có bốn bản biên tập bằng cùng cấu hình Codex yêu cầu `gpt-6.1-sol`, effort
`medium`: yêu cầu cơ bản, prompt biên tập thông thường, Vietnamizer, Vietnamizer + Jev.
Mỗi nhánh nhận cùng bản gốc và một lượt tạo bản cuối. Tên model thực ở backend chưa có
bằng chứng độc lập. Không ép thay đổi văn bản vốn đã tự nhiên và không chọn lại bản hợp lệ.

Jev chấm bản gốc trước khi tạo bản cuối; dữ liệu advice giữ rõ phạm vi đã kiểm, chưa kiểm
và lỗi. Trần 32 request mạng/nguồn, 640 request mới, cùng trần 2 USD cộng dồn cả pilot cũ.
Lượt phục hồi chỉ hỏi câu trả lời có phân phối sai định dạng, tối đa một lần cho mỗi
response lỗi, không hỏi lại câu hợp lệ. Giữ raw và nguồn từng câu trong composite riêng.
Một request timeout trước HTTP và không có response được thử lại tối đa một lần theo
phụ lục phục hồi đã rà; vẫn dự phòng tiền lượt cũ và tính cả hai lượt vào trần. Lỗi lần
hai hoặc lỗi transport khác dừng đợt chạy. Không chọn lại câu trả lời hợp lệ.
Nếu lượt phục hồi duy nhất của một câu vẫn sai phân phối, kết thúc tư vấn cho nguồn đó:
chỉ dùng các batch đã xác thực, giữ batch lỗi là không chấm được, không hỏi lần ba.
Đây là workflow dùng dịch vụ với giới hạn thực tế, không phải phép đo Jev luôn sẵn sàng.
Phản hồi đủ cho các câu đã lên lịch vẫn có thể thiếu phạm vi do phân đoạn chưa chắc
chắn hoặc ngữ cảnh chưa đủ. Giữ riêng `source_accounted`, `segmentation_complete`,
`answers_complete`, `context_complete`, phần unresolved và số câu chưa xong. Trường
`stop_diagnostic` raw có thể là lỗi đã phục hồi trước đó, không tự coi là nguyên nhân
kết thúc. Chưa đủ phạm vi thì không được gọi là đã kiểm toàn bộ văn bản.

## Giao cho hai người chấm

Mỗi người nhận một form riêng, chấm độc lập toàn bộ 20 nguồn × 4 bản sửa. Thứ tự nguồn
và nhãn A–D được xáo riêng với seed đóng băng; khóa ghép chế độ giữ ngoài form. Mỗi ảnh
đặt nguyên bản bên trái, bản sửa bên phải. Bốn bản của một nguồn dùng chung nguyên bản.

Ba câu hỏi cho mỗi đoạn:

1. Bản sửa có giữ đúng ý, số liệu và giọng người viết không?
2. Bản sửa đọc thế nào so với bản gốc?
3. Có chỗ nào sửa sai, sửa thừa hoặc vẫn khó hiểu không?

Hai câu đầu là bảng có bốn hàng A–D, câu cuối là nhận xét tự do. Người chấm cần ghi nhãn
bản và trích đoạn khi nhận xét. Không cần tìm lỗi trong nguyên bản trước. Không dùng AI
chấm hộ, xem điểm hoặc trao đổi đáp án với người kia trước khi cả hai hoàn tất. Giữ nhận
xét gốc; không dùng model để thay nhãn người chấm. Theo quyết định ngày 26/10/2026, không hỏi kinh nghiệm biên tập hoặc quan hệ với dự án;
không thu email. Mỗi form dành cho một người được Fio giao riêng; quyền có link
không tự xác thực danh tính hoặc bảo đảm độc lập. Nếu có nhiều phiếu, giữ tất cả raw và
chốt phiếu của đúng người trước khi mở khóa chế độ, không tự gộp thành nhiều người chấm. Form cũ được giữ nguyên; không nộp bài thử vào bộ nghiên cứu.

## Hợp đồng phân tích — sửa mục tiêu ngày 26/10/2026

Phụ lục [trước/sau trong cùng agent](within-agent-amendment.md) thay thứ tự ưu tiên
phân tích trước đây theo yêu cầu của Fio, sau khi sinh đầu ra và trước khi đọc nhãn
người được chọn trong đợt sửa này. Không gọi đây là đăng ký trước khi sinh dữ liệu.
Hai Forms hiện tại chỉ thuộc bộ Codex; bộ Gemini giữ riêng, chưa có nhãn người.

Mẫu độc lập là **20 nguồn**, không phải 80 bản sửa hoặc 160 phiếu. Hai người chấm là hai
người cụ thể; không suy CI thành phân phối của toàn bộ người đọc tiếng Việt.

- Giữ đủ 20 nguồn đã chốt trong phân tích chính, kể cả ca dịch vụ lỗi hoặc advice thiếu.
  Tách mô tả availability/coverage theo nguồn; phân tích phân nhóm chỉ là thăm dò, không
  loại ca lỗi sau khi xem chất lượng bản sửa.
- Báo tỷ lệ giữ đúng và dễ đọc hơn theo từng người, từng chế độ; luôn hiện số đã chấm,
  “Chưa rõ” và phần thiếu trên tổng 20 nguồn/người/chế độ.
- Kết quả chính: Vietnamizer so với bản AI gốc trên cùng cấu hình agent/model.
  Báo phân bố dễ đọc hơn / tương đương / khó hơn và giữ đúng / có chỗ bị đổi, cùng
  phần thiếu/chưa rõ. Báo trước/sau tương tự cho cả bốn chế độ để thấy đối chứng.
  Không tự tạo điểm số cho bản gốc hoặc lấy nhánh yêu cầu cơ bản làm bản gốc.
- Ước lượng trước/sau: với mỗi chế độ và từng loại nhãn xác định, tính tỷ lệ trên
  nguồn có nhãn xác định. Theo từng người hoặc trung bình hai người cố định trong
  mỗi nguồn; bản gộp chỉ dùng nguồn có nhãn xác định ở cả hai người cho chiều đó.
  Bootstrap 10.000 lần theo nguồn, seed 25033; báo CI 95% percentile và số nguồn.
  Các loại nhãn có thể dùng mẫu số khác nhau giữa chế độ/chiều khi thiếu dữ liệu;
  luôn đặt bảng số đếm trên tổng 20 bên cạnh CI, không đổi phần thiếu thành thất bại.
- So sánh bổ sung: Vietnamizer với prompt thường, Vietnamizer với yêu cầu cơ bản,
  Vietnamizer + Jev với Vietnamizer. Tất cả là thăm dò trong cùng agent; không xếp
  hạng Codex/Gemini, không gộp hai runtime. Cải thiện so với gốc tự nó chưa chứng
  minh skill tạo ra lợi ích vượt việc yêu cầu agent biên tập; cần xem cả đối chứng.
- Chênh lệch tỷ lệ dùng cùng nguồn và cùng người chấm. Bootstrap 10.000 lần, seed 25033,
  lấy lại mẫu theo nguồn, giữ nguyên cả bốn chế độ và hai người trong mỗi cụm. CI 95%
  percentile; phân tích gộp hai người chỉ dùng nguồn có đủ nhãn xác định cho cả hai
  nhánh ở cả hai người. Phân tích riêng từng người dùng cặp đủ của người đó. Ghi số
  nguồn ghép đủ và số bị loại vì thiếu/chưa rõ cho từng so sánh.
- “Chưa rõ” không tự chuyển thành đúng hoặc sai. Bảng chính hiển thị riêng; phân tích
  trên nhãn xác định phải ghi mẫu số thực, kèm giới hạn thiếu dữ liệu.
- Đồng thuận: bảng chéo hai người và tỷ lệ đồng thuận đúng nhãn cho hai câu chọn; báo
  số cặp thiếu/chưa rõ. Có thể bổ sung Cohen kappa danh nghĩa, không tự gán thứ bậc cho
  các lựa chọn. Nhận xét dùng để giải thích ca cụ thể, không suy precision/recall sửa lỗi.
- Tỷ lệ giữ nguyên, độ dài, thời gian và token là số mô tả thực thi. Không dùng độ khác
  ký tự hay điểm Jev làm chất lượng biên tập; không gán tiền cho quota Codex khi thiếu giá.

Chart sau khi có phiếu thật: phân bố nhãn theo chế độ/người (có phần thiếu/chưa rõ),
chênh lệch ghép cặp với CI theo nguồn, ma trận đồng thuận và bảng ca sửa sai có trích dẫn.
Mọi chart cần ghi đợt dữ liệu, n nguồn, người chấm, mẫu số, cách tính CI và giới hạn.
Chưa có phiếu người thật thì chỉ công bố tình trạng thu thập và phương pháp.

## Lưu trữ và tái lập

Giữ riêng nguồn/raw nhà phát hành, input và bundle đã đóng băng, toàn bộ prompt/output
Codex, raw HTTP Jev, usage/phân phối/lỗi, composite và ledger cộng dồn; không lưu khóa API.
Bộ Forms giữ 160 ảnh không mất chữ, hai contract, khóa xáo nhãn riêng, ID từng item,
ảnh/hash provider, log đọc lại, quyền trả lời và ảnh preview. Bản xuất phiếu khi có sẽ
được đóng băng riêng theo thời điểm, không ghi đè nguồn hoặc mapping cũ.

Archive có manifest SHA-256 cho từng file, nguồn code và lệnh kiểm tra. Đọc lại archive
và kiểm toàn bộ checksum trước khi giao. Link người chấm và dữ liệu raw giữ local;
README chỉ đưa phương pháp và kết quả đã kiểm chứng, không tự công bố người chấm.

Ngày 26/10/2026, trước khi có phiếu trả lời, đã bỏ hai câu hỏi nền khỏi cả hai form.
Mỗi form còn 160 mục; giữ nguyên ID của toàn bộ phần đánh giá, khóa xáo nhãn, ảnh và
hai link trả lời. Archive ngày 25/10 giữ hiện trạng ban đầu; bản bổ sung riêng lưu
schema trước/sau, thao tác gỡ và bằng chứng kiểm tra. Khi nhập phiếu, dùng schema
không có câu hỏi nền, không yêu cầu hai trường đã bỏ.

Trước khi đọc nhãn người thật, đã chốt cách xử lý biên: nếu có dưới hai nguồn ghép đủ
thì chỉ báo ước lượng quan sát và số nguồn, không dựng khoảng tin cậy bootstrap. Khi
các chênh lệch quan sát đều giống nhau, giữ CI suy biến cùng cảnh báo; không diễn giải
thành chắc chắn về quần thể. Báo riêng số nhãn phân loại và số bản có ít nhất một nhãn.
Phiếu chưa được Fio chọn theo ID không được đưa vào phân tích chất lượng.
