# Pilot 0.13.1 so với 0.13.0 trên cùng Codex

**V1 của0.13.1không lặp lại chú giải số nhiều ngoài nguồn. So với prompt+cùng mẫu,0.13.1thắng nhiều hơn thua trong lượt này, nhưng chưa đủ bằng chứng kết luận vượt trội hoặc đã chữa lỗi ổn định.** So phiên bản, Codex chủ yếu cho hòa, Gemini nghiêng về bản mới. N2 là ca cả hai cùng chọn bản cũ hơn.

Đã hoàn tất **32/32 đầu ra,52/52lượt CLI và16/16phiếu chấm chính hợp lệ**, không lỗi, không hỏi lại hoặc tạo lại. Có80đánh giá gồm64bản sửa và16bản gốc, cùng64lựa chọn cặp. Bốn lượt hiệu chuẩn nằm trong52; không tạo thêm nguồn.

## Thiết kế và hai câu hỏi chính

Tám nguồn phát triển giữ nguyên:V1–V4là bốn đoạn có giọng sẵn,N1–N4là bốn nháp AI trung tính đã tạo trước khi tiếp xúc mẫu. Tất cả đầu ra sinh bằng cùng CodexCLI0.164.0, yêu cầu gpt-6.1-sol/medium, cùng task/source/ba mẫu và mỗi ô một phiên mới:

- A/C: hai lượt sinh độc lập với **input prompt+mẫu giống hệt byte**, không có skill.
- B:0.13.0+cùng mẫu; D:0.13.1+cùng mẫu. Hai gói được đóng băng từ archive đã kiểm; cùng15đường dẫn thư viện, root chọn phần áp dụng.
- D−B: tác động phiên bản trong thiết kế này. D−C: giá trị so prompt+mẫu đồng thời. B−A và C−A là đối chiếu phụ; không coi A/C là hai phiên bản.

Codex và Gemini3.8Flashmedium chấm riêng, nhãn ứng viên ngẫu nhiên/vị trí đảo; không nhận version/skill hay lời chấm của nhau. Chấm giọng và nghĩa riêng. Không đổi rubric sau khi xem kết quả.

## Kết quả về giọng

| So sánh | Giám khảo | Thắng | Hòa | Thua | Trung vị chênh điểm giọng |
|---|---|---:|---:|---:|---:|
| D-B | Codex | 2 | 5 | 1 | +0 |
| D-B | Gemini | 6 | 1 | 1 | +1 |
| D-C | Codex | 4 | 2 | 2 | +0 |
| D-C | Gemini | 5 | 0 | 3 | +0.5 |
| C-A | Codex | 2 | 5 | 1 | +0 |
| C-A | Gemini | 3 | 1 | 4 | +0 |

Mỗi hàng có8bản, đủ phiếu; không có nhãn chưa rõ. D−B theo Codex là2/5/1, nhưng trung bình chênh điểm giọng là−0,125; Gemini là6/1/1và+0,5. D−C tương ứng4/2/2và5/0/3, trung bình+0,25/+0,125. Lựa chọn cặp và thang điểm1–5không đồng nhất: ưu tiên nhẹ có thể đi cùng điểm bằng nhau. Đây là thống kê mô tả trên thang thứ bậc, không có CI,p-value hoặc xác nhận độ lớn hiệu ứng.

Tách tầng cho D−B: bốn bài có giọng sẵn,Codex0/4/0,Gemini3/1/0; bốn nháp trung tính,Codex2/1/1,Gemini3/0/1. Hai giám khảo đồng ý lựa chọn D−Bở4/8bản và D−Cở3/8bản. Không gộp họ thành16người chấm; mức bất đồng là giới hạn thực tế của bằng chứng.

| Bản | Giọng Codex B→D | Giọng Gemini B→D | D:B Codex / Gemini | D:C Codex / Gemini |
|---|---|---|---|---|
| V1 | 5→5 | 4→4 | Hòa / Hòa | Thắng / Thua |
| V2 | 4→4 | 3→4 | Hòa / Thắng | Thắng / Thắng |
| V3 | 3→3 | 3→3 | Hòa / Thắng | Thua / Thắng |
| V4 | 4→4 | 3→4 | Hòa / Thắng | Hòa / Thua |
| N1 | 4→4 | 3→4 | Thắng / Thắng | Hòa / Thua |
| N2 | 4→3 | 4→3 | Thua / Thua | Thua / Thắng |
| N3 | 4→4 | 3→4 | Thắng / Thắng | Thắng / Thắng |
| N4 | 4→4 | 3→4 | Hòa / Thắng | Thắng / Thắng |

## V1: không thêm chú giải, chưa chứng minh sửa ổn định

Nguồn: `Mỗi nơi lưu source sẽ đc gọi là repositories`. Trong lượt021lịch sử,0.13.0từng thêm `số nhiều là repositories`. Ở **lượt023mới**, cả B0.13.0vàD0.13.1đều viết:

> Mỗi nơi lưu source được gọi là repositories.

Không có chú giải mới về số ít/số nhiều, không chèn định nghĩa Git mới. Rà nguồn→bản sửa và bản sửa→nguồn hiện không thấy mệnh đề thực tế mới rõ ràng trong D; những khẳng định lịch sử, ba người, mô hình repository và khả năng share trực tiếp được giữ. Đây là rà thủ công của host, không phải chứng minh tương đương nghĩa đầy đủ.

Điểm cần giữ trung thực: **bản cũ ở lượt sinh mới cũng không lặp lỗi chú giải**, nên không thể lấy việc câu đó biến mất làm bằng chứng nhân quả chắc chắn của bản vá. D vẫn giữ cách dùng `repositories` và đoạn ví dụ `nếu… . Thì…`; không gọi đây là bản đã sửa hết lỗi câu.

Codex ghi Bminor vì câu `server sẽ hiện cảnh báo lúc upload` nêu rõ chủ thể/nơi hiện cảnh báo trong khi nguồn để ngỏ về ngữ pháp. Dviết `thì lúc upload lên server sẽ có cảnh báo`, không chốt chủ thể ấy; cả hai giám khảo ghi Dclear. Giữ đây là một nhận xét có căn cứ câu chữ, chưa xác nhận bản mới luôn giữ mơ hồ đúng trên nguồn khác.

Về giọng,V1D:Bđược cả hai chấm hòa. D:C,Codex chọn D,Gemini chọn C. Hết một câu bổ sung không đồng nghĩa đã vượt prompt+mẫu ở V1.

## Tiến bộ nhìn thấy và ca chưa đạt

**N3:** Bviết `Một quy trình quản lý dấu trang có thể gồm bốn việc`, Dviết `Quản lý dấu trang có thể gồm 4 việc`. Bđặt đề mục `Lưu URL và lý do lưu`, Dcó `Lưu URL kèm giải thích để làm gì?`. Dgiữ đủ bốn việc, điều kiện đối chiếu URL+lý do trước khi bỏ mục trùng và giới hạn không gắn với mức tiết kiệm thời gian cụ thể. Cả hai chọn Dso Bvà C. Đây là ví dụ nét mẫu được vận dụng cùng nội dung sẵn có, không phải quy tắc rằng chữ số/câu hỏi luôn tốt hơn.

**N2 là phản ví dụ quan trọng:** Bcó các mục `Phiên bản và môi trường`, `Hướng dẫn thiết lập`, `Chạy một ví dụ nhỏ`, `Kết quả của lần thử`. Dđổi sang các câu hỏi như `Cần ghi lại những gì trước khi thử?`, `Kết quả này cho biết điều gì?` và thêm cách gọi `bạn`. Cả hai hạ điểm4→3và chọn B. Lý do chấm nói đề mục gọi tên nội dung cùng nhịp thuyết minh phù hợp hơn. Các điều kiện về lỗi chưa rõ nguyên nhân, hiệu năng và môi trường vận hành vẫn được giữ. Kết luận hẹp: theo nét mẫu cần chọn đúng vị trí, không tăng câu hỏi chỉ để thể hiện giọng.

**N4:** Dgiữ giới hạn chưa xác nhận nguyên nhân/chưa kết luận đã xử lý lỗi, đồng thời đổi sang chữ số và đối chiếu bullet. Codex cho D:Bhoà,Gemini chọn D. Tuy nhiên nguồn nói `Các bước tái hiện nên nêu thứ tự thao tác và điều kiện xảy ra lỗi`, Dviết `Các bước tái hiện: nêu thứ tự thao tác và điều kiện xảy ra lỗi`. Lược `nên` có thể được đọc như tăng sắc thái chỉ dẫn hoặc chỉ là nhãn mô tả trường; báo đây là **điểm cần kiểm về tình thái**, dù hai model ghi clear. Không sửa tay đầu ra để làm đẹp dữ liệu.

## Giữ nghĩa: giữ nguyên nhãn và đọc giới hạn của chúng

| Nhánh | Codex: clear / minor / major / uncertain | Gemini: clear / minor / major / uncertain |
|---|---|---|
| A | 8 / 0 / 0 / 0 | 4 / 4 / 0 / 0 |
| B | 7 / 1 / 0 / 0 | 7 / 1 / 0 / 0 |
| C | 8 / 0 / 0 / 0 | 3 / 5 / 0 / 0 |
| D | 8 / 0 / 0 / 0 | 6 / 2 / 0 / 0 |

clear=không thấy lỗi,minor=lỗi nhỏ,major=sai ý/dữ kiện,uncertain=chưa rõ theo model; không phải nhãn người bản ngữ độc lập. Dđược Codex8clear,Gemini6clear/2minor; không model nào ghi major. Gemini ghi minorởN1/N3nhưng lý do kèm chỉ bàn chữ số, danh sách hoặc giọng khách quan, chưa gọi tên một biến đổi nghĩa cụ thể. Không tự xóa hoặc đổi nhãn; cũng không dùng chúng làm bằng chứng hai lỗi dữ kiện đã được xác nhận.

Host đã đọc16bản B/Dcạnh nguồn: hiện chưa thấy mệnh đề thực tế mới rõ ràng trong D, giữ các điều kiện quan trọng của nháp trung tính; N4tình thái được ghi riêng. N2vẫn có chỗ đếm năm bước mơ hồ của nguồn: giữ số không chứng minh đã kiểm numeracy đúng. Đánh giá này không bảo đảm mọi câu tương đương nghĩa.

## Giới hạn để diễn giải kết quả

Một tác giả tham chiếu công khai, nguồn lịch sử2015–2016, không chứng thực viết hoàn toàn không AI hoặc giọng hiện tại; khả năng có trong pretraining chưa biết. Bốn bài có giọng thuộc ba họ chủ đề, có đoạn chỉ109/123từ. Corpus này **đã dùng để sửa0.13.1**, nên đây là kiểm trên tập phát triển, không phải holdout. Hai mẫu judge-only tách khỏi ba mẫu generator nhưng chưa được tác giả xác nhận như chuẩn giọng.

Một lượt sinh/ô không ước lượng độ ổn định. A/Cinputgiống nhau vẫn có lựa chọn khác nhau. Không so trực tiếp các điểm019/021với023để tuyên bố mức tăng phiên bản; lần sinh và model chấm có biến thiên. Chỉ dẫn P1về nạp ít tài liệu có mặt trong gói, nhưng15fileđều được cấp inline để so công bằng với021; **chưa thử lợi ích giảm context của việc nạp chọn lọc**.

Rubric có thiên lệch hình thức: Gemini chọn CởV4một phần vì sửa `Unity Desktop`, trong khi tên riêng/source spelling thuộc vùng cần bảo toàn. Codex cùng họ với model sinh; hai model không thay thế người chấm độc lập. Quote có trong text không tự chứng minh lý do chấm được quote hỗ trợ. Hiệu chuẩn chỉ kiểm đảo dữ kiện/tie/schema, không xác nhận khả năng nhận đúng giọng.

Cấu hình yêu cầu cùng model/effort được lưu; backend chính xác không được chứng thực độc lập. Raw là stdout/stderrnativeCLI và wrapper, không có HTTP/billing nội bộ.52là số lần khởi chạy CLI, không khẳng định số request ẩn. Không ghi nhận operational toolcall; guard không phải sandbox cấp hệ điều hành. Không đổi model, credits, cấu hình dùng chung hoặc product trong đợt chạy.

## Dữ liệu và tái dựng

- [32bản trước/sau](../../artifacts/023-voice-patch-pilot-20261028-v1/before-after.html).
- [Lựa chọn cặp](../../artifacts/023-voice-patch-pilot-20261028-v1/figures/voice-contrasts.svg), [chênh điểm phiên bản](../../artifacts/023-voice-patch-pilot-20261028-v1/figures/voice-primary-delta.svg), [nhãn nghĩa](../../artifacts/023-voice-patch-pilot-20261028-v1/figures/voice-meaning.svg); kèmPDFvàPNG.
- [Ratings/quote](../../artifacts/023-voice-patch-pilot-20261028-v1/ratings.csv), [contrasts](../../artifacts/023-voice-patch-pilot-20261028-v1/contrasts.csv), [summary](../../artifacts/023-voice-patch-pilot-20261028-v1/summary.csv), [resource ledger](../../artifacts/023-voice-patch-pilot-20261028-v1/resource-ledger.csv).
- [Rà nghĩa thủ công](../../artifacts/023-voice-patch-pilot-20261028-v1/host-meaning-review.json), [cách tái dựng offline](../../artifacts/023-voice-patch-pilot-20261028-v1/REPRODUCE.md).

Nguồn, archivehai phiên bản, prompt/schema, native/wrapperraw, toàn bộ52attempt/session, bản đồ nhãn, rubric, code/runtime và các stream kiểm guard đều giữ riêng ở artifact023. Các bước kiểm cuối, tính toàn vẹn lịch sử và archive nằm trong verification.md. Dữ liệu local bịgitignore, chưa công khai. Không dùng kết quả thăm dò này làm lời hứa bản mới luôn tốt hơn prompt+mẫu hoặc không thể thêm dữ kiện.
