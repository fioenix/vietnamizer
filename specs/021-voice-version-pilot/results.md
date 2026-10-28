# Pilot 0.13.0 so với 0.12.1 trên cùng Codex

**0.13.0 có tín hiệu tiến bộ về theo giọng mẫu trên nháp AI trung tính, nhưng chưa tốt hơn chung trên cả tám bản.** Trên bốn nháp trung tính, Codex chọn 0.13.0 thắng/hòa/thua là **2/2/0**, Gemini là **3/1/0**; cả hai không ghi lỗi nghĩa ở bốn bản này. Trên bốn bài vốn có giọng, cả hai chọn **0/2/2**. V1–0.13.0 thêm một chú giải ngữ pháp ngoài nguồn, nên chưa thể kết luận phiên bản mới luôn giữ nghĩa.

Đã chạy đủ **32 đầu ra, 52/52 lượt CLI và 16/16 phiếu chấm hợp lệ**: 80 đánh giá gồm 64 bản sửa và 16 bản gốc, cùng 64 lựa chọn cặp. Không lỗi, không hỏi lại hoặc tạo lại, không phiếu thiếu. Bốn lượt hiệu chuẩn nằm trong trần52; không tạo thêm nguồn.

## So sánh chính: phiên bản mới với phiên bản cũ

D là 0.13.0+mẫu, B là 0.12.1+cùng mẫu. Thắng/hòa/thua chỉ nói về lựa chọn giọng của D so với B; nhãn nghĩa được giữ riêng.

| Giám khảo | Tầng nhiệm vụ | n | Thắng | Hòa | Thua | Chưa rõ | Trung vị điểm giọng D−B |
|---|---|---:|---:|---:|---:|---:|---:|
| Codex | Có giọng sẵn | 4 | 0 | 2 | 2 | 0 | 0 |
| Gemini | Có giọng sẵn | 4 | 0 | 2 | 2 | 0 | 0 |
| Codex | Nháp AI trung tính | 4 | 2 | 2 | 0 | 0 | +0,5 |
| Gemini | Nháp AI trung tính | 4 | 3 | 1 | 0 | 0 | +1 |
| Codex | Tất cả | 8 | 2 | 4 | 2 | 0 | 0 |
| Gemini | Tất cả | 8 | 3 | 3 | 2 | 0 | 0 |

Trung bình chênh lệch điểm giọng trên tám bản là 0 theo Codex và +0,375 theo Gemini. Điểm 1–5 là thang thứ bậc; các phép tính này chỉ mô tả dữ liệu, không có CI, p-value hoặc kết luận hiệu ứng đã xác nhận.

## Từng bản: được gì và còn lỗi gì?

Điểm ghi theo **0.12.1 → 0.13.0**, không phải hai bước biên tập nối tiếp. “Không thấy lỗi” là nhãn model; không bảo đảm mọi nghĩa đều đúng.

| Bản | Điểm giọng Codex | Điểm giọng Gemini | Lựa chọn Codex / Gemini | Nghĩa của 0.13.0: Codex / Gemini |
|---|---|---|---|---|
| V1 · Git | 5 → 3 | 3 → 2 | Thua / Thua | Lỗi nhỏ / Lỗi nhỏ |
| V2 · DNS | 4 → 4 | 3 → 3 | Hòa / Hòa | Không thấy lỗi / Không thấy lỗi |
| V3 · Sublime Text | 3 → 3 | 3 → 3 | Hòa / Hòa | Không thấy lỗi / Không thấy lỗi |
| V4 · Ubuntu | 3 → 3 | 3 → 3 | Thua / Thua | Không thấy lỗi / Lỗi nhỏ |
| N1 · Theo dõi công việc | 4 → 4 | 3 → 4 | Hòa / Thắng | Không thấy lỗi / Không thấy lỗi |
| N2 · Thử thư viện | 3 → 4 | 2 → 4 | Thắng / Thắng | Không thấy lỗi / Không thấy lỗi |
| N3 · Dấu trang | 4 → 4 | 4 → 4 | Hòa / Hòa | Không thấy lỗi / Không thấy lỗi |
| N4 · Gỡ lỗi | 3 → 4 | 3 → 4 | Thắng / Thắng | Không thấy lỗi / Không thấy lỗi |

Hai giám khảo đồng ý lựa chọn chính ở 7/8 bản; N1 là hòa/thắng. V4 cho thấy điểm bằng nhau vẫn có thể đi kèm ưu tiên cặp: giữ cả hai tín hiệu, không sửa điểm cho khớp lựa chọn. Mức đồng ý này không xác nhận giám khảo chấm đúng bản sắc tác giả.

## Ví dụ tiến bộ: N2 và N4

**N2:** 0.12.1 giữ năm đoạn văn liền. 0.13.0 thêm các đề mục “Phiên bản và môi trường”, “Hướng dẫn thiết lập”, “Chạy một ví dụ nhỏ”, “Kết quả cho biết điều gì?”, đồng thời tách thông tin ghi chép thành ba bullet:

> - Ví dụ đã chạy
> - Kết quả nhận được
> - Lỗi xuất hiện, nếu có

Ba mục lấy từ câu gốc “Ghi chép cần nêu ví dụ đã chạy, kết quả nhận được và lỗi xuất hiện, nếu có.” Điều kiện **nếu có**, phân biệt quan sát với nguyên nhân chưa xác nhận và giới hạn chưa có cơ sở kết luận sẵn sàng vận hành vẫn còn. Cả hai giám khảo thích giọng của 0.13.0 hơn và không ghi lỗi nghĩa. Trong lượt rà thủ công nguồn/B/D, không thấy mệnh đề thực tế mới ở đoạn này.

Cả hai phiên bản đều giữ “năm bước”. Nguồn gốc mơ hồ ở cách nhóm phiên bản/môi trường; giữ số không chứng minh số đó đã đúng. Đây vẫn là giới hạn của nguồn, không được gọi là bài kiểm numeracy độc lập đã qua.

**N4:** 0.12.1 đã tách ba phần tái hiện/kỳ vọng/thực tế thành bullet. 0.13.0 tiếp tục tổ chức thành các đề mục và hai dòng đối chiếu:

> - Triệu chứng cho biết đã xảy ra điều gì.
> - Giả thuyết đưa ra một cách giải thích cần kiểm tra.

Bản mới giữ điều kiện giả thuyết chưa xác nhận, yêu cầu chỉ thay đổi một yếu tố và kết luận chưa thể khẳng định lỗi đã xử lý. Hai model đều nâng điểm giọng 3→4 và không ghi lỗi nghĩa. Tín hiệu tiến bộ nằm ở cấu trúc hướng dẫn có trong mẫu, chưa chứng minh mọi chiều của giọng riêng đã được học.

**N3 là đối chứng cần giữ:** cả 0.12.1 và 0.13.0 trong đợt này đều dùng danh sách và đề mục; hai model cho hòa. Không được chỉ so bản mới với 0.12.1 lịch sử vốn sửa ít hơn để quy toàn bộ cấu trúc mới thành tác dụng của phiên bản.

## Ví dụ chưa đạt: V1 thêm thông tin ngoài nguồn

Nguồn có “Mỗi nơi lưu source sẽ đc gọi là repositories”. 0.12.1 sửa thành:

> Mỗi nơi lưu source được gọi là repository.

0.13.0 viết:

> Mỗi nơi lưu source được gọi là repository, số nhiều là repositories.

Phần **“số nhiều là repositories”** là một mệnh đề chú giải nguồn không nêu. Dù đúng về ngữ pháp và hai model xếp “lỗi nhỏ”, đây vẫn là **vi phạm chốt không thêm dữ kiện** của chính skill, không được bù bằng độ trôi chảy. Bản dữ liệu được giữ nguyên, không sửa tay để làm đẹp benchmark.

Cùng bản này, 0.13.0 dùng “bạn” nhiều hơn và chuyển một số chữ số thành “một”; giám khảo thích cách thuyết minh và chữ số của 0.12.1 hơn. V4 cũng bị ưu tiên thấp hơn dù điểm bằng nhau, phần lớn do đổi cách gọi “chúng ta” sang “bạn có thể”. Các lý do này có giới hạn: có phần là khác biệt giọng/quan hệ, có phần dễ bị lẫn với đánh giá nghĩa hoặc hình thức; chưa có tác giả xác nhận.

## Giữ nghĩa và giá trị so với prompt thường

| Nhánh | Codex: không thấy lỗi / nhỏ / sai ý / chưa rõ | Gemini: không thấy lỗi / nhỏ / sai ý / chưa rõ |
|---|---|---|
| A · prompt+mẫu, lượt 1 | 6 / 2 / 0 / 0 | 6 / 2 / 0 / 0 |
| B · 0.12.1+mẫu | 7 / 1 / 0 / 0 | 8 / 0 / 0 / 0 |
| C · cùng prompt+mẫu, lượt 2 | 7 / 1 / 0 / 0 | 4 / 4 / 0 / 0 |
| D · 0.13.0+mẫu | 7 / 1 / 0 / 0 | 6 / 2 / 0 / 0 |

Tất cả nhãn nghĩa của D trên bốn nháp trung tính là không thấy lỗi. Rà thủ công 16 bản B/D thấy các điều kiện và giới hạn quan sát của bốn D trung tính được giữ, chưa thấy mệnh đề thực tế mới; đây không phải xác minh đầy đủ mọi tương đương nghĩa. V1 đã có phản ví dụ rõ cho an toàn nghĩa trên toàn bộ tập. B–N2 chỉ bị Codex ghi lỗi nhỏ vì đổi mức phủ định từ “không cung cấp cơ sở” sang “không đủ làm cơ sở”.

So sánh phụ trên tám bản, ghi **thắng / hòa / thua / chưa rõ** của vế trước:

| Phép so sánh | Codex | Gemini |
|---|---|---|
| D với C · 0.13.0 so prompt+mẫu | 1 / 1 / 6 / 0 | 2 / 0 / 6 / 0 |
| B với A · 0.12.1 so prompt+mẫu | 2 / 1 / 5 / 0 | 1 / 0 / 7 / 0 |
| C với A · hai lượt sinh cùng prompt | 1 / 5 / 2 / 0 | 4 / 3 / 1 / 0 |

Riêng nháp trung tính, D:C là 0/1/3 theo Codex và 2/0/2 theo Gemini. **Tiến bộ so 0.12.1 chưa đồng nghĩa tốt hơn prompt+mẫu.** Hai model còn có lựa chọn khác nhau giữa A/C dù input giống hệt. Đây là quan sát về độ nhạy của một lượt sinh/ô và phép chấm; không đủ ước lượng độ ổn định hoặc độ lớn hiệu ứng phiên bản trong quần thể.

## Thiết kế và giới hạn

Chủ nhân chọn 8 nguồn × 2 slot phiên bản × 2 nhánh có mẫu =32. A/C là hai lượt sinh độc lập cùng input, không có phiên bản skill trong hai nhánh này; B/D khác duy nhất nội dung instruction library của hai phiên bản. Tất cả nhận cùng nguồn, ba mẫu, ngữ cảnh và yêu cầu tiếng Anh rõ: “Adapt this Vietnamese draft toward the voice of the supplied writing samples…”. Mỗi ô dùng phiên mới, cùng CodexCLI0.164.0, yêu cầu gpt-6.1-sol/medium, không tool/memory/Jev. Backend thật không được chứng thực độc lập.

Hai bundle cùng15đường dẫn root/reference/profile/card từ archive đóng băng0.12.1/0.13.0. Root của từng phiên bản chọn phần áp dụng; không cố định chỉ profile K như019. Vì prompt, tài liệu được cấp và lượt sinh khác019, không gộp điểm lịch sử làm đối chứng trực tiếp. Đây là so cả gói, chưa tách riêng đóng góp mode/router/guide.

Nguồn là cùng9bài công khai quy cho Van-Duyet Le, revision397efbf471b958e65eeecb87eba913d0a1f99620:3mẫu generator,2mẫu judge-only,4bản có giọng; cộng4nháp AI giả lập từ019, không tạo lại. Vai trò tách theo bài/họ chủ đề;4bản có giọng thuộc3họ. Đây đã là **tập phát triển** dùng sửa0.13.0, không phải holdout mới. Hai đoạn thử ngắn109/123từ, nguồn lịch sử2015–2016, chưa chứng thực viết không AI hoặc giọng hiện tại; khả năng có trong pretraining chưa biết.

Codex/Gemini3.8Flashmedium chấm riêng source+4ứng viên với nhãn ngẫu nhiên, vị trí đảo và bốn cặp định trước; không nhận version/skill hoặc lời chấm nhau. Chỉ kiểm có quote nguyên văn chưa bảo đảm lý do chấm được quote hỗ trợ. Bốn calibration qua kiểm đảo dữ kiện/tie/schema, không xác nhận giám khảo hiểu giọng tác giả. Cùng họ Codex vừa sinh vừa chấm có nguy cơ thiên lệch; hai model không là hai người chấm độc lập. Không có tác giả/người chấm xác nhận.

Tất cả52lượt hợp lệ,52session riêng và không ghi nhận operational tool trong native streams. Raw là CLI/wrapper, không phải HTTP/billing nội bộ hoặc bằng chứng cách ly ở cấp hệ điều hành. Trần52tính lượt CLI theo ledger, không chứng thực số request HTTP ẩn. Seed chỉ khóa thứ tự/nhãn, không khóa ngẫu nhiên sinh văn bản. Không retry, đổi model, tạo nháp, chạm Forms hoặc sửa skill trong đợt này.

## Dữ liệu và hình

- [Chênh lệch 0.13.0−0.12.1](../../artifacts/021-voice-version-pilot-20261028-v1/figures/voice-primary-delta.svg).
- [So phiên bản, prompt và hai lượt sinh cùng input](../../artifacts/021-voice-version-pilot-20261028-v1/figures/voice-contrasts.svg).
- [Nhãn nghĩa từng bản, không bù bằng điểm giọng](../../artifacts/021-voice-version-pilot-20261028-v1/figures/voice-meaning.svg).
- [32 đối chiếu trước/sau](../../artifacts/021-voice-version-pilot-20261028-v1/before-after.html).
- [Ratings và quote](../../artifacts/021-voice-version-pilot-20261028-v1/ratings.csv), [cặp so sánh](../../artifacts/021-voice-version-pilot-20261028-v1/contrasts.csv), [tổng hợp theo tầng/giám khảo](../../artifacts/021-voice-version-pilot-20261028-v1/summary.csv).

SVG/PDF và PNG xem nhanh giữ từng ca, từng model và mẫu số. Artifacts là dữ liệu local bị gitignore, chưa được công khai. Gói raw kèm code/phương pháp/nguồn/giấy phép và script tái dựng offline được cung cấp cùng báo cáo. Không dùng kết quả này làm tuyên bố đã vượt prompt thường hoặc an toàn nghĩa toàn diện.
