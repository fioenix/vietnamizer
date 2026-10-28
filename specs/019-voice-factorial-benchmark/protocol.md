# Benchmark giữ giọng: tách mẫu giọng và Vietnamizer

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent, plan mode.
- Origin Date: 2026-10-27.
- Verification Status: public-author pilot đang chạy; cổng nguồn Mindfio dừng trước đây được giữ ở source-readiness.md.
- Version Label: voice-factorial-public-author-v2; manifest thực thi là nguồn chuẩn cho prompt/schema/config.
- Workflow owner: Spec Kit 019; ARS chỉ hỗ trợ phương pháp nghiên cứu.

## 1. Câu hỏi chính

**Khi đã có cùng mẫu giọng, thêm Vietnamizer có giúp bản sửa giữ đúng giọng tham chiếu hơn prompt biên tập thường, đồng thời giữ nghĩa không?** So sánh chính là D với B. Không quy lợi ích vốn đến từ việc thêm mẫu thành lợi ích riêng của skill.

Ba câu hỏi phụ: mẫu giúp gì khi không có skill; skill giúp gì khi không có mẫu; hai yếu tố kết hợp có tác động khác tổng từng phần không. Không đặt trước giả thuyết Vietnamizer chắc chắn thắng.

## 2. Bốn nhánh trên cùng agent

| Nhánh | Mẫu giọng | Vietnamizer | Nội dung agent nhận |
|---|---|---|---|
| A | Không | Không | Prompt chung + bản nháp/ngữ cảnh |
| B | Có | Không | Như A + bộ mẫu thô đã khóa |
| C | Không | Có | Như A + đầy đủ instruction bundle Vietnamizer |
| D | Có | Có | Như C + **đúng mẫu và byte của B** |

Không tạo hồ sơ bằng model khác hoặc cho riêng D thêm bản phân tích giọng. Không dùng Jev. Skill treatment gồm resolver, profile/card và hướng dẫn đọc mẫu hiện hành; phép đo đánh giá cả gói, chưa tách riêng voice guide với từng quy tắc. Đo hồ sơ thay mẫu thô là thí nghiệm tiếp theo.

Khóa source 0.12.1, cùng Codex/model/effort/schema/giới hạn đầu ra. Phiên mới mỗi ô, không tool hoặc memory; đảo thứ tự trong block bản nháp và khóa seed. Cấu hình cụ thể chốt sau kiểm tra runtime/quota; alias không chứng thực backend thực. Không sửa skill giữa các nhánh.

Prompt chung dự kiến cho cả bốn nhánh; chỉ hai yếu tố thí nghiệm được bổ sung:

```text
Copyedit this Vietnamese draft for the stated channel and reader.
Preserve meaning, facts, uncertainty, commitments and protected material.
If writing samples are supplied, use them as voice references within this
editing task. Otherwise preserve the voice already present in the draft.
Do not invent experiences or insert catchphrases merely to imitate a writer.
Return only the final edited text.
```

Đây là biên tập có kiểm soát, không phải viết bài mới từ đầu. Không mặc định giữ nguyên câu đúng là lỗi hoặc viết lại mạnh là thành công; chấm theo phạm vi yêu cầu thực tế.

## 3. Quy mô tối thiểu và bộ nguồn

**Đề xuất bắt đầu: một người × tám bản nháp × bốn nhánh = 32 đầu ra.** Một lần sinh mỗi ô. Đây là tối thiểu khả thi để khảo sát một giọng, chưa phải cỡ mẫu đã đủ power; 32 đầu ra không phải 32 nguồn độc lập.

| Tầng nhiệm vụ | Số bản | Câu hỏi |
|---|---:|---|
| Bản đã có giọng người viết | 4 | Agent giữ hay làm mất nét đã có? |
| Bản AI có giọng trung tính | 4 | Mẫu/skill giúp tiến gần giọng tham chiếu trong phạm vi biên tập không? |

Đề xuất mỗi bản 200–400 từ, cùng kênh blog cá nhân; độ dài là giới hạn vận hành, không là ngưỡng tiếng Việt đã kiểm chứng. Không trộn blog, email và báo cáo thành giọng trung bình.

Ngoài tám bản nháp, cần **ba mẫu cho generator và hai mẫu riêng cho judge**, cùng kênh nhưng khác chủ đề. Đây là cấu hình đề xuất, không phải số mẫu tối ưu đã đo. Ba nhóm rời nhau ở cấp bài/chuỗi bài; kiểm cả đoạn gần trùng. Không chia một bài rồi tính thành nhiều bài độc lập. Không đưa bài gốc của chính bản nháp cho judge làm đáp án phong cách.

Bản AI trung tính phải có sẵn hoặc tạo riêng từ brief dữ kiện được chủ nhân duyệt, không thấy mẫu giọng; lưu source/raw nếu có. **32 chỉ tính lượt biên tập**, chưa gồm tối đa bốn lượt tạo nháp. Nếu cần tạo, báo riêng và xin chốt trước; không tự phát sinh lượt gọi.

“Trung tính” ở đây chỉ có nghĩa vận hành là nháp chưa được cấp mẫu/hồ sơ cá nhân,
không khẳng định văn bản hoàn toàn không có nét giống người viết. Dùng ID ẩn danh
thay tên publication để tránh model dựa vào danh tính có sẵn; giữ nguyên dữ kiện
và tên riêng trong phần văn bản phải bảo toàn. Các chủ đề giữa bộ mẫu và bộ thử
khác nhau, để từ vựng chủ đề không thay thế bằng chứng về giọng.

Bản có giọng có thể tự viết hoặc do người dùng biên tập AI rồi chọn làm chuẩn. Gắn provenance từng nguồn. Chưa có mẫu tự viết không AI thì chỉ kết luận về **giọng tham chiếu đã chọn**, không về giọng nguyên bản không AI. Mindfio/MR đã dùng chỉnh 0.12.1 chỉ dùng thiết kế/hiệu chuẩn, không tái gọi holdout. Chưa giả định đã có đủ nguồn mới.

Muốn khảo sát nhiều người: đề xuất mở rộng **sáu người × bốn bản × bốn nhánh = 96 đầu ra**, hai bản mỗi tầng/người. Đây vẫn là mức thăm dò theo độ phủ và khả năng tổ chức, không là cỡ mẫu xác nhận thống kê. Sau pilot nhiều người, dùng biến thiên theo tác giả, mức tác động đáng quan tâm và mô phỏng/power để chốt đợt xác nhận mới. Một người không đủ ước lượng biến thiên giữa tác giả.

## 4. Ba câu chấm dễ hiểu

Mỗi điểm phải có trích đoạn hỗ trợ, hoặc ghi chưa đủ bằng chứng. Độ nổi tiếng, chủ đề quen thuộc và cụm từ sao chép không đủ chứng minh đúng giọng.

| Câu hỏi | Thang dự kiến | Mốc chấm |
|---|---|---|
| Đoạn này có giống cách viết trong mẫu không? | Giọng 1–5/chưa rõ | 1: lệch rõ xưng hô, từ hoặc nhịp; 3: tương thích nhưng chung chung/trộn nét; 5: nét phù hợp có bằng chứng, không diễn quá tay; 2/4 ở giữa |
| Có đổi ý, thêm chuyện hoặc mất chi tiết không? | Không thấy lỗi / lỗi nhỏ / lỗi làm sai ý / chưa rõ | Chỉ đúng thay đổi chủ thể, lượng, thời gian, nhân quả, chắc chắn, trải nghiệm, thuật ngữ; không nhầm đổi cách nói với đổi nghĩa |
| Đọc có tự nhiên, rõ ràng không? | Dễ đọc 1–5/chưa rõ | 1: khó hiểu hoặc lỗi rõ; 3: hiểu được nhưng có chỗ gượng; 5: tự nhiên, mạch rõ; không mặc định câu ngắn/dài hay hơn |

Kiểm cả nét được giữ và nét bị cài quá mức: câu cửa miệng, tiểu từ, xưng hô. Không dùng độ sửa ký tự, độ dài câu hoặc AI detector làm điểm khớp giọng. Thang model chưa tự xác nhận tác giả cũng đánh giá như vậy.

Chấm bản gốc cùng bốn bản sau để có mốc trước/sau; không yêu cầu thích bản đã sửa. Sau chấm riêng, chọn trái/phải/hòa/chưa rõ cho bốn cặp B:A, C:A, D:C, D:B. Ghi lựa chọn giọng và lỗi nghĩa riêng; không cộng thành điểm để giọng hay bù sai nghĩa. Chuỗi giống hệt phải hòa về phần chữ, vẫn giữ đủ ô thực thi.

## 5. Hai lượt chấm độc lập

Giai đoạn chưa khảo sát người: **hai model khác họ** làm giám khảo; các bản biên tập vẫn cùng Codex. Phải xác minh/chốt model, quota và quyền nhận chính bộ dữ liệu đó. Không tự dùng lại API budget cũ. Hai lần cùng model chỉ độc lập về phiên/thứ tự, không là hai model độc lập.

Cả hai nhận cùng hai mẫu judge-only, nguồn/ngữ cảnh, bốn ứng viên ẩn nhánh. Không nhận skill, profile, đáp án ca hoặc nhận xét nhau. Cho biết đâu là bản gốc để kiểm giữ nghĩa; ứng viên dùng mã ngẫu nhiên, cân bằng vị trí giữa judge và block. Mapping ở ngoài prompt. Model vẫn có thể đoán nhánh từ văn bản, nên chỉ gọi ẩn nhãn, không khẳng định mù hoàn toàn hay hết thiên lệch nhà cung cấp.

Một request/block/judge: **2 × 8 = 16 request chấm**, cho 64 đánh giá đầu ra, 16 đánh giá nguồn và 64 lựa chọn ghép cặp. Các phán đoán trong request có tương quan. Khả năng đọc block/schema cần kiểm offline/smoke trước khi chạy; chưa có runner.

Hiệu chuẩn trước khi khóa bằng nguồn ngoài tám ca: cặp giống hệt để thử hòa, bản trôi chảy nhưng đổi dữ kiện, nét giọng có bằng chứng và ca nhồi câu cửa miệng. Chưa có nhãn tác giả thì chỉ kiểm nhất quán/lỗi rõ, chưa xác nhận judge biết đúng giọng. **Đề xuất hai block hiệu chuẩn × hai judge = bốn request riêng**, nằm ngoài 16 request chấm chính. Khóa hai block trước khi gọi; không hiệu chuẩn lại nhiều lần để chọn kết quả đẹp. Nếu không qua kiểm tra nhất quán/schema hoặc chưa đủ bằng chứng giọng, dừng chấm chính và ghi đúng giới hạn. Chưa được duyệt thì không chạy và không gọi judge là đã hiệu chuẩn. Chấm model trên ca host tạo không tự biến chúng thành nhãn tác giả.

Không gọi lại lỗi/chọn lượt thuận lợi; giữ parse lỗi, thiếu và chưa rõ trong mẫu số. Dừng trước vượt trần, không âm thầm thay judge. Không coi hai model đồng ý là nhãn đúng.

Nếu tác giả muốn xác nhận sau này, chỉ cần xem **tám cặp D:B** kèm nguồn và mẫu, trả ba câu ở mục 4. Không có form kinh nghiệm/xung đột lợi ích; không sửa hai Forms cũ. Đây là nhãn chủ nhân cho tám cặp, không phải chấm người độc lập cả 32 bản. Không có bước này thì chỉ báo **model-assessed/exploratory**.

## 6. Cách phân tích để tách tác động

Với điểm giọng S cùng bản nháp/giám khảo:

| Chênh lệch | Ý nghĩa |
|---|---|
| B−A | Tác động mẫu khi không skill |
| C−A | Tác động skill khi không mẫu |
| D−C | Tác động mẫu khi có skill |
| **D−B — chính** | Tác động thêm của skill khi đã có cùng mẫu |
| (D−C)−(B−A) | Tương tác trên thang điểm đã chọn |

Thang 1–5 là thứ bậc; hiệu số/trung bình chỉ là mô tả phụ thuộc mã hóa, không là đơn vị giọng khách quan. Báo phân bố và thắng/hòa/thua/chưa rõ từng judge trước khi tổng hợp. D tốt hơn A không tách được lợi ích skill.

Không loại bản sai nghĩa khỏi phân tích giọng để nhánh trông tốt hơn: báo cả điểm giọng và lỗi nghĩa trên **toàn bộ ô**, kèm bảng giao giữa thích giọng/giữ nghĩa. Không đặt tổng điểm bù trừ. Trường hợp ưu tiên giọng nhưng sai nghĩa phải được trình bày nổi bật.

Tầng giữ giọng: so S(sửa)−S(gốc); gốc có thể đã tốt nên giữ nguyên hợp lệ. Tầng AI trung tính: báo tiến gần giọng và sửa quá tay riêng. Không trộn hai tầng thành tỷ lệ thành công duy nhất.

Một người/tám nguồn: báo tám chênh lệch, trung vị, đếm dấu, độ nhạy khi bỏ từng nguồn. Bootstrap theo nguồn nếu có chỉ là mô tả thăm dò trong một người/kênh, không bảo đảm coverage 95% với mẫu nhỏ hay nói về mọi người dùng. Nhiều người: tính theo người trước, cân bằng trọng số, phân cụm theo tác giả; 96 đầu ra không phải 96 người. Không kiểm định xác nhận hoặc chọn tỷ lệ thắng tối thiểu sau khi thấy dữ liệu.

Báo đồng ý/bất đồng judge, hòa/chưa rõ, không xóa nhãn đầu qua model phân xử. Thiếu mẫu, judge lệch hoặc lỗi làm thiếu dữ liệu có thể dẫn tới chưa rõ. Tín hiệu tích cực cần D:B thuận có bằng chứng qua tầng/judge mà không che lỗi nghĩa; pilot không chứng minh an toàn tương đương hay lợi ích phổ quát. Một lần sinh mỗi ô chưa đo độ ổn định giữa lần sinh.

| Kết quả quan sát | Cách diễn giải được phép |
|---|---|
| B tốt hơn A, D gần B | Mẫu có ích; chưa thấy phần đóng góp thêm rõ của Vietnamizer |
| D tốt hơn B về giọng, các lỗi nghĩa vẫn được báo đầy đủ | Có tín hiệu lợi ích thêm của skill trong phạm vi pilot, cần đọc từng ca và kiểm độ ổn định |
| D tốt hơn A nhưng không tốt hơn B | Chưa tách được lợi ích của skill khỏi việc cấp mẫu |
| D được thích giọng nhưng đổi ý/thêm trải nghiệm | Có đánh đổi, không gọi là thành công biên tập |
| Hai judge bất đồng hoặc thiếu dữ liệu | Chưa rõ; không chọn judge thuận để làm kết luận |

## 7. Chart và raw

1. Ghép cặp từng nguồn: gốc/A/B/C/D, tách tầng và judge, không chỉ cột trung bình.
2. Ma trận bốn contrast: thắng/hòa/thua/chưa rõ, mẫu số đầy đủ.
3. Đồ thị giọng với lỗi nghĩa, thấy cả ca thích giọng nhưng sai ý.
4. Bảng bất đồng và ví dụ trước/sau có ca tốt, không đổi, sửa quá tay.

Giữ UTF-8 gốc, URL/khai báo nguồn/quyền chia sẻ, full prompt/response đúng tầng CLI hoặc HTTP, stderr, schema/argv/config, thời gian/usage/model thực nếu có; hash source/sample/skill/rubric, split, seed, mọi attempt, mapping và điểm/trích bằng chứng. Không gọi raw CLI là raw HTTP, không suy USD từ token thuê bao. Lưu local mặc định; không đưa hồ sơ vào skill hay công bố văn bản nếu chưa được phép.

Lập dữ kiện/chuỗi bảo toàn trước sinh; byte check không thay kiểm nghĩa. Chưa có nhãn từng edit thì harmful-edit recall/valid-edit false-block rate phải ghi chưa đo; báo review rate, lỗi dịch vụ, latency/cost/unknowns phù hợp constitution, không lấy điểm giọng thay các chỉ số đó.

## 8. Các quyết định trước execution

- Chấp nhận 32 đầu ra hay thêm lần sinh thứ hai thành 64? Phải chốt trước, không sau khi xem kết quả.
- Có đủ ba mẫu generator, hai mẫu judge-only và tám nguồn mới đúng provenance không?
- Hai model chấm nào sẵn quota và được phép nhận bộ dữ liệu này?
- Trần đề xuất đầy đủ: **32 lượt biên tập + bốn lượt hiệu chuẩn judge + 16 lượt chấm chính = 52 request model**. Nếu cần tạo bốn bản AI trung tính mới thì tối đa 56 request, phải được chốt riêng. Không có retry trong trần; offline test không tiêu quota. Chưa có dự toán USD khi runtime chưa chốt.
- Khóa protocol/rubric/source/runtime/split. Nếu dùng kết quả sửa skill, nguồn thành tập phát triển, không còn holdout cho bản sửa.

Hiện chỉ là đề xuất thiết kế: chưa thu corpus mới, tạo runner, gọi model, hiệu chuẩn judge, tạo Forms hoặc tiếp xúc người chấm.

## Quyết định sau khi chủ nhân chốt

Ngày 27/10/2026, chủ nhân chốt 32 đầu ra/trần 56 request model, Codex biên tập và Codex/Gemini chấm ẩn nhãn. Cổng nguồn kiểm tra không đạt. Chủ nhân tiếp tục cho phép tìm công khai và dừng nếu không có đủ nguồn. Đã thực hiện lượt tìm giới hạn và dừng: **0/56 request model**, không xây runner, không khảo sát người hoặc sửa Forms. Xem [bằng chứng kiểm tra nguồn](source-readiness.md). Phần thiết kế bên trên được giữ làm hồ sơ, không là công việc tự động sẽ chạy tiếp.


## Phụ lục thực thi với nguồn công khai

Theo quyết định dùng tác giả khác, pilot dùng 9 bài của Van-Duyet Le tại revision `397efbf471b958e65eeecb87eba913d0a1f99620` của `duyet/blog`: 3 mẫu cho generator, 2 mẫu riêng cho judge và 4 bản thử có giọng. Bốn brief giả lập tạo thêm 4 nháp trung tính, không thêm trải nghiệm cá nhân. Hai bài thử về giao diện cùng một họ chủ đề; bốn bài không được gọi là bốn họ độc lập. Đoạn thử ngắn nhất109/123từ, mẫu ngắn199/140từ; không kéo dài nguồn bằng câu tự tạo. Phạm vi là giọng blog kỹ thuật2015–2016, không đại diện mọi thể loại hoặc giọng hiện tại của tác giả.

Manifest `artifacts/019-public-author-pilot-20261027-v2/manifest.json` khóa32ô,4nháp,4hiệu chuẩn,16block chấm. Hai block hiệu chuẩn chỉ kiểm đảo dữ kiện rõ và hòa cho bản giống hệt; không có nhãn tác giả về giọng. Schema thực thi buộc điểm giọng/dễ đọc nguyên1–5; chỉ quan hệ nghĩa và lựa chọn cặp có trạng thái chưa rõ. Vì vậy không coi điểm giọng là đủ bằng chứng về sự chắc chắn của giám khảo. Prompt yêu cầu nói rõ giới hạn trong lý do.

Lượt chấm chính đầu tiên bị loại vì một trích dẫn không có nguyên văn trong mẫu. Giữ nguyên toàn bộ phiếu là thiếu, không sửa quote hoặc dùng lại từng điểm. Phụ lục tiếp tục chỉ cho các ID chưa chạy trong kế hoạch ban đầu; lỗi transport/config/tool/raw vẫn dừng. Không hỏi lại phiếu lỗi, không đổi prompt/model/tiêu chuẩn. Báo cáo cuối phải ghi số phiếu hợp lệ và mẫu số thật cho từng model/tầng nhiệm vụ.
