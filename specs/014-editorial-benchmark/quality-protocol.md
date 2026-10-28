# Protocol chấm chất lượng 80 bản — v1

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: plan, followed by authorized implementation
- Origin Date: 2026-10-25
- Verification Status: PLANNED; human judgments not collected
- Version Label: editorial-quality-v1

Owner yêu cầu tiếp tục chấm chất lượng, chạy bộ model chấm và chuẩn bị bộ giao hai người
chấm thuận tiện; Google Forms là lựa chọn giao diện. Không gửi lời mời hoặc tự công bố.

## Thiết kế đã chọn

Đóng băng bộ `finish-blinded-review.json` và key của đợt phục hồi. Giữ nguyên 80 bản cuối,
20 nguồn × 4 chế độ. Mỗi người chấm đọc đủ 80 bản; không chia mỗi người 40 bản. Hai người
không xem nhãn của nhau hoặc nhãn model. Hướng dẫn và các ví dụ tập chấm dùng ngoài 20 nguồn.

Hai model giám khảo: GPT-6.1 Sol và GPT-6 Astra qua Codex CLI, medium, quota subscription
hiện có, không API trả tiền, không Jev và không chuyển sang Gemini đang bị chặn. Cùng nhà
cung cấp và một model trùng model sinh bản nháp là giới hạn phải công bố. Đây là hai lượt
model riêng biệt, không thay cho hai lượt người chấm. Mỗi giám khảo trước tiên nhận nguồn
mà không có bản biên tập để ghi lỗi cần sửa; sau đó mỗi nguồn/bốn bản được chấm ở phiên mới.
Tối đa 42 lần bắt đầu: hai lần lập nhãn nguồn + 40 lần chấm nhóm bản; không tự retry hoặc
thay output đã chấm. Timeout 180 giây/lần, tối đa hai tiến trình. Smoke một nguồn/model
trước batch còn lại. Raw, source, prompt/schema, flags, nhãn và usage được giữ đầy đủ.

Mã bản A–D được đổi riêng theo người/model và nguồn, cân bằng vị trí 5 lần/chế độ/vị trí.
Ẩn tên chế độ, model sinh, pattern, expected/clean do host gán, advice Jev và kết quả cũ.
Key chỉ ở gói điều phối riêng, không nằm trong HTML/Forms gửi người chấm.

## Hai lượt người chấm

1. A và B mỗi người đọc 20 nguồn trước khi xem bất kỳ bản biên tập nào. Ghi lỗi bắt buộc,
   trích đoạn làm mốc, điều cần bảo toàn và trường hợp không đủ ngữ cảnh. Xuất/khóa nhãn
   nguồn với thời điểm và digest trước khi mở 80 bản. Nhãn clean của host chỉ là dự kiến.
2. Mỗi người chấm 20 nhóm, mỗi nhóm bốn bản. Chia bốn phiên, mỗi phiên năm nguồn/20 bản;
   lưu tiến độ tại máy và xuất JSON để gửi Fio. Có thể dừng giữa phiên.
3. Xét riêng giữ nghĩa, giọng, vùng bảo toàn; phân loại từng diff block; đánh dấu mỗi lỗi
   nguồn đã được sửa/được sửa một phần/chưa sửa/chưa đủ cơ sở. Xếp thứ tự bốn bản với hạng
   bằng nhau khi tương đương; cho phép chưa thể xếp, không ép chọn người thắng.
4. Khóa hai lượt trước khi mở key. Lưu nhãn gốc A/B và đo agreement trước đối soát. Lập
   danh sách bất đồng; người thứ ba ưu tiên xử lý khi vẫn ẩn chế độ. Nếu chỉ có A/B, họ
   đối soát bằng lý do và giữ unresolved khi không thống nhất; không ép đồng thuận.

Mỗi người nên thạo tiếng Việt và có kinh nghiệm biên tập loại tài liệu tương ứng; người
không tham gia phát triển skill là lựa chọn tốt hơn. Ghi kinh nghiệm và xung đột lợi ích.
Dự trù ban đầu 5–7 giờ/người và 1–2 giờ đối soát, tổng 11–16 giờ; đây là ước lượng công
việc cần hiệu chỉnh sau tập chấm thử, không phải thời gian đã đo. Thù lao theo mức Fio chốt.

## Quy tắc nhãn và mẫu số

- Giữ nghĩa/giọng/vùng bảo toàn: clear, violation hoặc uncertain. Vi phạm phải có bằng chứng
  cụ thể; uncertain không được đổi thành đạt. Câu trôi chảy không bù được đổi nghĩa.
- Đơn vị edit: khối khác biệt liên tiếp do diff token khoảng trắng/dấu câu sinh ra, giữ
  offset nguồn/đích. Đây là diff block, không phải phép đếm lỗi ngôn ngữ độc lập. Cho phép
  nhận xét một lỗi trải qua nhiều block; không cộng nó nhiều lần vào required-fix recall.
- Diff block: justified_successful / unnecessary / harmful / mixed / uncertain. Báo đủ các
  nhóm, không xoá mixed/uncertain khỏi mẫu số tổng. Precision theo block = số justified /
  tổng block; bản không đổi có mẫu số 0 → N/A, không phải 100%.
- Recall theo issue nguồn: resolved / partial / unresolved / uncertain. Mỗi issue tính một
  lần cho mỗi bản; resolved mới vào tử số chính. Báo partial riêng và cả số issue/mẫu số.
  Nhãn nguồn của hai người có thể khác; giữ kết quả từng người và mapping khi đối soát.
- Sửa thừa ở nguồn sạch: dùng nhãn nguồn đã khóa trước khi mở output, báo riêng từng người
  và sau đối soát. Không âm thầm loại ca host gọi là clean vì kết quả bất lợi.
- Thứ hạng A–D là lựa chọn trực tiếp của người chấm, cho phép ties; suy ra wins/ties/losses
  từng cặp và ghi rõ xuất phát từ một xếp hạng chung, không phải sáu phiếu độc lập.

## Câu hỏi và phân tích chốt trước nhãn

Chính: thêm Jev vào cùng bước rà từ chung draft có cải thiện lựa chọn bản cuối hay không?
Phụ: Vietnamizer tự rà so với prompt thường và không skill. Hai baseline chạy trước và ít
lượt sửa hơn: kết quả là so workflow quan sát được, không phải tác động thuần của skill.
Backend Codex chưa được attestation; không gọi đây là thử nghiệm bốn nhánh đồng thời.

Đơn vị lấy mẫu là 20 nguồn. Gộp nhãn hai người trong từng nguồn rồi paired bootstrap theo
nguồn (giữ các chế độ và cả hai người cùng nhau), 10.000 lần, seed đóng băng, CI 95%.
Báo raw counts, mẫu số, missing/unresolved, kết quả A/B riêng và sau đối soát. Chênh lệch
an toàn báo theo điểm phần trăm, không lấy tỷ lệ tương đối khi đối chứng bằng 0.
Bootstrap không suy ra rủi ro bằng 0 khi không thấy lỗi; tỷ lệ lỗi hiếm cần interval phù
hợp và nêu số nguồn nhỏ. Nguồn là tập giả lập tiện dụng, CI không chứng minh đại diện cho
mọi văn bản tiếng Việt. Không dùng 80 outputs, 160 nhãn hay 15.449 câu Jev làm cỡ mẫu độc lập.

Agreement: percent agreement và Cohen's kappa cho các nhãn danh nghĩa trên cùng đơn vị;
báo N/A khi kappa không xác định, phân bố nhãn và số đơn vị đủ cả hai nhãn. Không đặt ngưỡng
kappa tùy ý để ép đạt. Bất đồng lớn cần giải thích tiêu chí, không chỉ lấy trung bình.
Không sửa rubric sau khi thấy điểm; nếu buộc sửa, tạo version mới và chấm lại phạm vi bị ảnh hưởng.

## Chart và điều kiện đưa vào README

1. Wins/ties/losses cho ba phép so sánh đã chốt, kèm số nguồn và phần chưa quyết định.
2. Forest plot chênh lệch ghép cặp và CI 95%, tách giữ nghĩa/sửa thừa/lựa chọn; đường 0 rõ.
3. Tỷ lệ lỗi giữ nghĩa/giọng/vùng bảo toàn từng chế độ, số đếm và interval, tách người/model.
4. Ma trận A/B và các bất đồng trước đối soát. Phân tầng thể loại chỉ mô tả vì mỗi nhóm nhỏ.

Xuất SVG, PNG 300 DPI và bảng số đứng sau mỗi chart. Nhãn model có tiêu đề MODEL-ASSESSED /
EXPLORATORY, không ghép với human hoặc đổi thành human-approved. Human chart chỉ có khi đủ
160 lượt chấm, trace được nguồn/phiên bản, xử lý missing và giữ bất đồng gốc. README có thể
công bố pilot với giới hạn; tuyên bố hiệu quả trên văn bản mới vẫn cần holdout chưa dùng để
chỉnh skill/prompt/rubric. Không dùng radar hoặc một điểm tổng che mất thay đổi nghĩa.

## Cơ sở phương pháp

Các lựa chọn cụ thể ở đây là thiết kế cho pilot này, không phải quy định nguyên văn từ nguồn.
- [van der Lee et al., 2019](https://aclanthology.org/W19-8643/): thiết kế và báo cáo human evaluation.
- [Koehn, 2004](https://aclanthology.org/W04-3250/): paired bootstrap trong đánh giá NLP; ở đây lấy mẫu theo văn bản.
- [Ethayarajh & Jurafsky, 2022](https://aclanthology.org/2022.emnlp-main.406/): giới hạn của việc gộp điểm cảm nhận thành ranking.
