# Pilot 0.13.2 so với 0.13.1 trên cùng Codex

**N2 có tín hiệu cải thiện về tổ chức nội dung và giọng, đồng thời hai giám khảo đều ghi nghĩa được giữ.** So với 0.13.1, Codex cho hòa 4→4, Gemini nâng 4→5 và chọn 0.13.2. Cả hai chọn 0.13.2 hơn prompt+cùng mẫu ở N2. **Kết quả toàn bộ pilot chưa chứng minh 0.13.2 là nâng cấp chất lượng đồng đều so với 0.13.1.**

Đã sinh đủ **32/32 bản** và thực hiện **52/52 lượt CLI**: 4 hiệu chuẩn, 32 sinh, 16 lượt chấm chính. Có **15/16 phiếu chính hợp lệ**; phiếu V2–Gemini bị loại vì trích dẫn không tồn tại trong ứng viên. Không hỏi lại, không sửa điểm hoặc cứu một phần phiếu. Dữ liệu hợp lệ gồm **75 đánh giá** (60 bản sửa và 15 bản gốc), **60 lựa chọn cặp**; raw của phiếu lỗi vẫn được giữ.

## Thiết kế và phạm vi so sánh

Tám nguồn, task, ba mẫu generator, hai mẫu riêng giám khảo và thứ tự/nhãn giống giao thức 023:

- A/C: hai lượt sinh độc lập, input prompt+mẫu giống hệt byte, không có skill.
- B: 0.13.1+cùng mẫu, archive đóng băng từ 023.
- D: 0.13.2+cùng mẫu, archive đã kiểm ở 024.
- Tất cả 32 bản do cùng Codex CLI 0.164.0, yêu cầu gpt-6.1-sol/medium, mỗi ô một phiên mới. Cùng 15 đường dẫn thư viện, root chọn phần áp dụng; không dùng Jev/tool/memory trong tác vụ con.

D−B là đối chiếu phiên bản, D−C đối chiếu bản mới với prompt+mẫu đồng thời. B−A và C−A là phụ. Không dùng điểm các lượt 021/023 làm đối chứng trực tiếp hoặc cộng gộp thành cỡ mẫu mới.

Codex và Gemini 3.8 Flash medium chấm riêng với nhãn/vị trí đảo; không nhận tên phiên bản, skill hoặc lời chấm nhau. Agy hiện là **1.4.9**, khác 1.4.8 của 023; model alias giám khảo không đổi. Đây là thay đổi runtime được ghi nhận, không tự cập nhật/hạ cấp hoặc đổi cài đặt dùng chung. Backend chính xác không được chứng thực độc lập.

## N2: tốt hơn chỗ nào, và giới hạn nào còn nguyên?

| Tiêu chí | Codex: 0.13.1 → 0.13.2 | Gemini: 0.13.1 → 0.13.2 |
|---|---|---|
| Giọng | 4 → 4, hòa | 4 → 5, chọn bản mới |
| Dễ đọc | 4 → 4 | 5 → 5 |
| Nghĩa | clear → clear | clear → clear |
| So 0.13.2 với prompt C+mẫu | Thắng, 4 so với 3 | Thắng, 5 so với 3 |

**Phần ghi chép và thiết lập được phân biệt rõ hơn.** B đặt cả đoạn ghi phiên bản/môi trường lẫn đọc hướng dẫn dưới `Cần ghi lại những gì?`. D vẫn giữ câu hỏi ấy nhưng tách đoạn sau bằng đề mục:

> Đọc hướng dẫn thiết lập

Nhờ vậy phần đầu hỏi về thông tin cần ghi, còn phần sau dẫn tới thao tác đọc/xác định bước thiết lập. Đây là khác biệt quan sát được ở đầu ra, không phải thí nghiệm tách riêng tác động của từng câu chỉ dẫn.

**Đối chiếu trạng thái được làm nổi mà giữ tình thái.** B viết:

> Khi ghi lại quá trình, nên phân biệt bước đã làm với bước còn thiếu hoặc chưa xác định được.

D viết:

> Khi ghi lại quá trình, nên phân biệt rõ:
>
> - Bước đã thực hiện.
> - Bước còn thiếu hoặc chưa xác định được.

Từ **nên**, trạng thái **chưa xác định** và đối chiếu hai nhóm vẫn còn; không đổi thành mệnh lệnh hoặc tự thêm trạng thái thứ ba.

**Không phải cấm câu hỏi hay bạn.** Cả B và D đều giữ hai đề mục hỏi, gồm `Cần ghi lại những gì?` và `Kết quả này cho biết điều gì?`. D có thêm đề mục đọc hướng dẫn phù hợp phần thiết lập, không ép mọi mục thành danh từ hoặc nghi vấn. Cả hai bản trong cặp mới đều không dùng bạn; vì thế không quy riêng việc bỏ đại từ cho 0.13.2. Các bài khác của D vẫn có bạn trong ngữ cảnh hướng dẫn.

**Các chốt nghĩa chính của N2 được giữ:** thay đổi phiên bản/môi trường phải được phản ánh trong ghi chép; phân biệt bước đã làm/còn thiếu/chưa rõ; giữ thông báo lỗi quan sát được; tách nguyên nhân chưa được xác nhận; giữ `nếu có`; một ví dụ thành công chỉ xác nhận lần thử; không so hiệu năng hoặc kết luận sẵn sàng vận hành. Host đã đối chiếu hai chiều và hiện chưa thấy mệnh đề thực tế mới rõ ràng trong D. Đây là rà thủ công, không bảo đảm tương đương nghĩa đầy đủ.

Nguồn nói **năm bước** nhưng cách nhóm chưa rõ. D đổi cách viết thành **5 bước**, không tự chia lại để làm đủ năm; **không coi đây là bằng chứng đã xác minh số bước đúng**. Không sửa mơ hồ của nguồn bằng suy đoán.

Kết luận hẹp cho N2: Gemini ưu tiên bản mới, Codex chưa thấy khác biệt giọng đủ rõ so bản cũ; cả hai thích bản mới hơn prompt C. Dễ đọc không tăng điểm ở cả hai. Không lấy điểm 3 của 0.13.1 ở 023 so với điểm 4/5 hiện tại để tuyên bố mức tăng: bản cũ mới sinh ở đây cũng đạt 4.

## Toàn bộ pilot: chưa đủ bằng chứng nâng cấp đồng đều

| So sánh | Giám khảo | Đủ phiếu / dự kiến | Thắng | Hòa | Thua | Trung vị chênh điểm giọng |
|---|---|---:|---:|---:|---:|---:|
| D-B | Codex | 8/8 | 0 | 6 | 2 | +0 |
| D-B | Gemini | 7/8 | 4 | 0 | 3 | +0 |
| D-C | Codex | 8/8 | 5 | 3 | 0 | +1 |
| D-C | Gemini | 7/8 | 3 | 1 | 3 | +0 |
| C-A | Codex | 8/8 | 1 | 4 | 3 | +0 |
| C-A | Gemini | 7/8 | 4 | 0 | 3 | +0 |

Không có nhãn uncertain trong các phiếu hợp lệ. Gemini thiếu V2, nên tổng hợp là **7/8 nguồn**, không phải tám; missing không được tính thành hòa/thua hoặc điền bằng phiếu cũ. Thiếu này có thể làm lệch tổng hợp, không chứng minh missing-at-random.

Codex chấm B và D bằng điểm giọng ở cả tám nguồn, nhưng thích B hơn ở N1/N3 và hòa sáu ca. Gemini chọn D ở bốn trong bảy ca, song trung bình chênh điểm giọng D−B là khoảng−0,286 vì N3 giảm 5→3 và V3 giảm 3→2; N2 tăng 4→5. Lựa chọn cặp và điểm thang 1–5 là hai tín hiệu khác nhau, không sửa chúng cho khớp. Codex có trung bình D−B=0; D−C có trung bình+0,625, Gemini khoảng+0,714 trên các phiếu có. Các phép tính trên thang thứ bậc chỉ mô tả, không có CI/p-value hoặc xác nhận hiệu ứng quần thể.

Hai giám khảo đồng ý D−B ở **1/7** nguồn cùng có phiếu; D−C ở **4/7**. Không gộp thành hai người chấm độc lập hoặc bỏ các ca trái chiều.

| Bản | Giọng Codex B→D | Giọng Gemini B→D | D:B Codex / Gemini | D:C Codex / Gemini |
|---|---|---|---|---|
| V1 | 5→5 | 4→4 | Hòa / Thắng | Thắng / Thua |
| V2 | 4→4 | Thiếu→Thiếu | Hòa / Thiếu | Thắng / Thiếu |
| V3 | 3→3 | 3→2 | Hòa / Thua | Hòa / Thua |
| V4 | 4→4 | 4→4 | Hòa / Thắng | Hòa / Thua |
| N1 | 4→4 | 4→4 | Thua / Thắng | Hòa / Hòa |
| N2 | 4→4 | 4→5 | Hòa / Thắng | Thắng / Thắng |
| N3 | 4→4 | 5→3 | Thua / Thua | Thắng / Thắng |
| N4 | 4→4 | 4→4 | Hòa / Thua | Thắng / Thắng |

**N3 là phản ví dụ cần giữ:** cả hai thích B hơn D. B dùng các đề mục gọi tên công việc; D thêm `Quản lý dấu trang gồm những việc gì?` và `Liên kết đã lỗi thời thì sao?`. Các việc và giới hạn tiết kiệm thời gian còn được giữ, nhưng hai giám khảo thích nhịp thuyết minh của B hơn. Không suy thành luật cấm câu hỏi: đây là ưu tiên trong cặp và phạm vi mẫu cụ thể.

## Giữ nghĩa và chất lượng nhãn

| Nhánh | Codex: clear / minor / major / uncertain · n=8 | Gemini: clear / minor / major / uncertain · n=7 |
|---|---|---|
| A | 6 / 2 / 0 / 0 | 4 / 3 / 0 / 0 |
| B | 7 / 1 / 0 / 0 | 6 / 1 / 0 / 0 |
| C | 7 / 1 / 0 / 0 | 4 / 3 / 0 / 0 |
| D | 8 / 0 / 0 / 0 | 6 / 1 / 0 / 0 |

clear=không thấy lỗi, minor=lỗi nhỏ, major=sai ý/dữ kiện, uncertain=chưa rõ theo model. D có 8 clear theo Codex, 6 clear/1 minor theo Gemini trên bảy phiếu có; không nhãn major. **Không có phiếu V2–Gemini**, không được suy nó là clear.

V1B đổi `rất vất vả` thành `khá vất vả`; Codex nêu đây là giảm nhẹ sắc thái và gán minor. D giữ rất và không thêm chú giải số nhiều; hai model ghi Dclear. Đây là một cặp cụ thể, không chứng minh mọi dữ kiện/sắc thái của D đều được giữ.

Gemini gán N3Dminor nhưng lý do chỉ nói câu hỏi, từ đệm và phân cấp đề mục, chưa chỉ rõ mệnh đề đổi nghĩa. Tương tự, một số nhãn minor của prompt control gắn với đại từ/giọng. Giữ nguyên nhãn, không coi đó là lỗi dữ kiện đã được xác nhận hay tự đổi thành clear. Quote tồn tại chưa đủ chứng minh lý do được quote hỗ trợ.

Host đã đọc 16 bản B/D cạnh nguồn. Ngoài N2, có điểm cần giữ bất định ở V3D: `plugin hữu ích mà bạn có thể cài trực tiếp` gắn rõ khả năng cài đặt với plugin, trong khi câu nguồn ít tường minh hơn; ngữ cảnh Package Control có thể hỗ trợ nhưng không được gọi là tương đương nghĩa tuyệt đối. Không sửa tay đầu ra. N4 giữ nên trong cả B/D của lượt này; không quy hết việc giữ ấy cho bản vá.

## Phiếu bị loại và raw đầy đủ

V2–Gemini trích `là của ai? Đó là công việc` cho ứng viên P9 nhưng chuỗi này không có trong ứng viên. CLI exit0 và stream/guard được đối soát, song phiếu không qua điều kiện bằng chứng. Theo giao thức đóng băng, **cả block năm đánh giá/bốn cặp là thiếu**; không cứu các dòng có vẻ đúng hoặc hỏi lại. Có 52 lần gọi CLI đã thực hiện, 51 record status completed và một record failed vì kiểm quote, không có bản sinh bị thiếu. Toàn bộ text/raw/usage/lỗi của phiếu được lưu.

## Giới hạn diễn giải

Một tác giả tham chiếu lịch sử 2015–2016; bốn đoạn có giọng thuộc ba họ chủ đề, có đoạn109/123từ; bốn nháp AI được tái dùng nguyên bản. Corpus này đã dùng để sửa0.13.2, **không phải holdout**. Không chứng thực giọng hiện tại hay tác giả tự viết hoàn toàn; pretraining exposure chưa biết.

Ba mẫu generator có cả câu hỏi khái niệm và bạn, hai mẫu judge-only thiên về đề mục chủ đề/danh mục. Mismatch vai trò vẫn có thể làm giám khảo thưởng hình thức hơn bản sắc tác giả. Rubric giữ nguyên từ023, không chỉnh để thưởng thiết kế mới. Codex vừa sinh vừa chấm cùng họ; model judges không thay thế tác giả/người bản ngữ. Hiệu chuẩn chỉ kiểm đảo dữ kiện/tie/schema, không xác nhận khả năng nhận giọng.

Một lượt sinh/ô không đo độ ổn định; A/C cùng input vẫn cho đầu ra/lựa chọn khác nhau. Cả15tài liệu đều cấp inline để so công bằng, chưa thử lợi ích giảm context của nạp chọn lọc. Runtime giám khảo Agy đã đổi1.4.8→1.4.9; không gộp điểm023 để suy mức tăng phiên bản. Không thay model, credits hay sản phẩm giữa đợt.

Raw là nativeCLI/wrapper stdout/stderr và stdin/schema, không có HTTP/billing nội bộ.52là số lần khởi chạy CLI, không khẳng định số request ẩn. Không ghi nhận operationaltoolcall; guard không phải sandbox hệ điều hành. Không gọi Jev, không đổi cấu hình dùng chung hoặc hai Forms.

## Dữ liệu và tái dựng

- [32 bản trước/sau](../../artifacts/025-section-voice-pilot-20261028-v1/before-after.html).
- [Lựa chọn cặp](../../artifacts/025-section-voice-pilot-20261028-v1/figures/voice-contrasts.svg), [chênh điểm phiên bản](../../artifacts/025-section-voice-pilot-20261028-v1/figures/voice-primary-delta.svg), [nhãn nghĩa](../../artifacts/025-section-voice-pilot-20261028-v1/figures/voice-meaning.svg); kèmPDF/PNG.
- [Ratings/quote](../../artifacts/025-section-voice-pilot-20261028-v1/ratings.csv), [contrasts](../../artifacts/025-section-voice-pilot-20261028-v1/contrasts.csv), [summary](../../artifacts/025-section-voice-pilot-20261028-v1/summary.csv), [resource ledger](../../artifacts/025-section-voice-pilot-20261028-v1/resource-ledger.csv).
- [Rà riêng N2](../../artifacts/025-section-voice-pilot-20261028-v1/host-n2-review.json), [rà 16 bản](../../artifacts/025-section-voice-pilot-20261028-v1/host-meaning-review.json), [phiếu lỗi](../../artifacts/025-section-voice-pilot-20261028-v1/rejected-judgment-detail.json), [tái dựng offline](../../artifacts/025-section-voice-pilot-20261028-v1/REPRODUCE.md).

Nguồn, hai archive phiên bản, toàn bộ52prompt/schema/native/wrapperstreams và lỗi, blinding, rubric, code/runtime, provenance/usage giữ riêng ở artifact025. Dữ liệu local bịgitignore, chưa công khai. Seal/checksum/tái dựng và kiểm lịch sử báo ở verification.md. Không dùng kết quả này làm tuyên bố bản mới luôn hơn0.13.1hoặc không thể đổi nghĩa.
