# Pilot giữ giọng tham chiếu trên cùng Codex

**Pilot chưa chứng minh Vietnamizer giúp bắt chước giọng tốt hơn khi đã có cùng mẫu.** Trên bốn nháp AI trung tính, cả Codex và Gemini đều ưu tiên prompt + mẫu hơn Vietnamizer + cùng mẫu, ở cả bốn trường hợp. Với bài có sẵn giọng, lợi thế thêm của skill cũng chưa xuất hiện rõ. Kết quả phù hợp với cách hoạt động thận trọng của bundle hiện tại, nhưng chưa chứng minh vì sao có khác biệt hoặc áp dụng cho tác giả khác.

Đã sinh **32/32 đầu ra** và dùng **56/56 lượt CLI theo kế hoạch**, không hỏi lại hay tạo lại. Có 15/16 phiếu chấm chính hợp lệ: 8 Codex và 7 Gemini, tạo 60 đánh giá bản sửa, 15 đánh giá bản gốc và 60 lựa chọn cặp. Phiếu Gemini–V4 bị loại toàn bộ vì trích dẫn mẫu không nguyên văn; raw vẫn được giữ. Bốn lượt hiệu chuẩn và bốn lượt tạo nháp được tính trong cùng trần 56.

## Khi đã có mẫu, thêm Vietnamizer cho kết quả gì?

D là Vietnamizer + mẫu; B là prompt + **cùng mẫu**. Thắng/hòa/thua dưới đây là lựa chọn về giọng của D so với B, không phải kết luận chung về chất lượng.

| Giám khảo | Tầng nhiệm vụ | Phiếu hợp lệ / dự kiến | D thắng | Hòa | D thua | Chưa rõ | Trung vị điểm giọng D−B |
|---|---|---:|---:|---:|---:|---:|---:|
| Codex | Bài có giọng sẵn | 4/4 | 0 | 4 | 0 | 0 | 0 |
| Gemini | Bài có giọng sẵn | 3/4 | 0 | 1 | 2 | 0 | 0 |
| Codex | Nháp AI trung tính | 4/4 | 0 | 0 | 4 | 0 | −1 |
| Gemini | Nháp AI trung tính | 4/4 | 0 | 0 | 4 | 0 | −1 |
| Codex | Tất cả | 8/8 | 0 | 4 | 4 | 0 | −0,5 |
| Gemini | Tất cả | 7/8 | 0 | 1 | 6 | 0 | −1 |

Các phép so sánh phụ, ghi theo **thắng / hòa / thua / chưa rõ** của vế trước:

| Phép so sánh | Codex, 8 phiếu | Gemini, 7 phiếu |
|---|---|---|
| B với A: thêm mẫu, chưa có skill | 5 / 3 / 0 / 0 | 6 / 0 / 1 / 0 |
| C với A: thêm skill, chưa có mẫu | 1 / 7 / 0 / 0 | 1 / 3 / 3 / 0 |
| D với C: thêm mẫu, đã có skill | 1 / 7 / 0 / 0 | 1 / 5 / 1 / 0 |

Riêng nháp AI trung tính, **B thắng A 4/4 ở cả hai giám khảo**; C không thắng A ở trường hợp nào; D không thắng B ở trường hợp nào. Tín hiệu tăng mức tương thích với mẫu tập trung ở nhánh chỉ thêm mẫu. Không được quy tín hiệu đó thành thành tích của Vietnamizer.

Trung vị tương tác điểm giọng `(D−C)−(B−A)` là −1 ở cả hai giám khảo, với 8/7 trường hợp tương ứng. Đây chỉ là phép tính mô tả trên thang thứ bậc; không suy ra một hiệu ứng tương tác có ý nghĩa thống kê hoặc cơ chế của skill.

## Trước và sau ở từng bản

Mỗi ô ghi điểm giọng **gốc / B / D**, thang 1–5. B và D là hai nhánh độc lập cùng sửa bản gốc, không phải hai bước nối tiếp.

| Bản thử | Codex: gốc / B / D | Gemini: gốc / B / D | D so với B: Codex / Gemini |
|---|---|---|---|
| V1 · Git | 4 / 5 / 5 | 3 / 4 / 4 | Hòa / Hòa |
| V2 · DNS | 4 / 4 / 4 | 3 / 4 / 3 | Hòa / Thua |
| V3 · Sublime Text | 3 / 3 / 3 | 2 / 2 / 2 | Hòa / Thua |
| V4 · Ubuntu | 4 / 4 / 4 | Thiếu phiếu | Hòa / Thiếu |
| N1 · Theo dõi công việc | 3 / 4 / 3 | 3 / 4 / 3 | Thua / Thua |
| N2 · Thử thư viện | 3 / 4 / 3 | 3 / 4 / 3 | Thua / Thua |
| N3 · Dấu trang | 3 / 4 / 3 | 2 / 4 / 2 | Thua / Thua |
| N4 · Gỡ lỗi | 3 / 4 / 3 | 3 / 4 / 3 | Thua / Thua |

D tăng điểm so với bản gốc ở V1 theo cả hai model; các trường hợp còn lại không tăng điểm giọng. Giữ nguyên câu đúng hoặc điểm không tăng không tự động là biên tập thất bại. N3–C giữ nguyên toàn bộ bản gốc; ô này vẫn được giữ trong dữ liệu.

Hai giám khảo đồng ý lựa chọn D:B ở 5/7 bản có đủ hai phiếu. Hai bất đồng là V2/V3: Codex cho hòa, Gemini ưu tiên B. V3 còn cho thấy lựa chọn cặp không luôn trùng chênh lệch điểm: Gemini cho B và D cùng 2 điểm nhưng vẫn ưu tiên B. Giữ cả hai tín hiệu, không sửa điểm cho khớp lựa chọn.

## Giữ nghĩa: kết quả và giới hạn của nhãn

Mỗi ô theo thứ tự **không thấy lỗi / lỗi nhỏ / sai ý / chưa rõ**. Đây là nhãn model, chưa có xác nhận tác giả/người đọc.

| Nhánh | Codex, 8 phiếu | Gemini, 7 phiếu |
|---|---|---|
| A | 6 / 1 / 1 / 0 | 5 / 2 / 0 / 0 |
| B | 6 / 1 / 1 / 0 | 5 / 2 / 0 / 0 |
| C | 7 / 0 / 1 / 0 | 6 / 1 / 0 / 0 |
| D | 8 / 0 / 0 / 0 | 7 / 0 / 0 / 0 |

D không bị hai model gắn lỗi nghĩa trong các phiếu hợp lệ. Tuy nhiên, **cả ba nhãn sai ý của Codex đều tập trung ở một nguồn N2**, nơi A/B/C bỏ “năm” khỏi câu “Quy trình gồm năm bước”. Gemini chỉ coi cùng thay đổi đó là lỗi nhỏ. Nguồn đã mơ hồ về cách đếm bước; không được gọi đây là ba lỗi độc lập, hoặc dùng nó để tuyên bố D đã được chứng minh an toàn hơn. D giữ số lượng gốc, đồng thời giữ cả điểm mơ hồ của nguồn.

Ngoài N2, Codex ghi lỗi nhỏ ở V1–A và V2–B; Gemini ghi lỗi nhỏ ở V1–A và N3–B. Nhãn và lý do đầy đủ nằm trong ratings.csv. Các ví dụ này nhắc rằng một bản được thích hơn về giọng vẫn có thể thay sắc thái; hai chiều được giữ riêng.

## Ví dụ: sửa vừa đủ và thích nghi giọng là hai việc khác nhau

**V3, câu có giọng sẵn.** Gốc có cụm “giúp bạn đỡ bớt phần nhàm chán khi Code quanh năm với cái giao diện cũ òm :))”. D sửa thành “giúp bạn bớt nhàm chán khi code quanh năm với cái giao diện cũ òm :))”. Phần thừa được rút, nét nói vui và emoticon còn nguyên. A/B/C cũng giữ nét này, nên không thể lấy ví dụ đó làm lợi thế riêng của Vietnamizer.

Gemini ưu tiên B hơn D ở V3 chủ yếu vì viết hoa “Python”, “Sublime Text”; hai bản vẫn cùng điểm giọng. Đây là dấu hiệu phép chấm bị lẫn tính chỉn chu với giọng. V3 gốc cũng chỉ đạt 2/3 điểm theo Gemini/Codex dù chính là bài của tác giả được chọn. Hai mẫu riêng của giám khảo chưa bao phủ hết mức thân mật trong các bài thử. Do đó phép đo gần với **tương thích hai mẫu tham chiếu** hơn một phép đo đã xác thực về giữ bản sắc tác giả.

**N3, nháp AI trung tính.** Gốc mở bằng “Một quy trình quản lý dấu trang có thể gồm bốn việc: lưu URL kèm giải thích ngắn, nhóm theo chủ đề, loại bỏ mục trùng và xem lại những liên kết đã lỗi thời.” D chủ yếu thêm “phần” trước “giải thích ngắn”, giữ dạng văn xuôi. B đổi thành “Một quy trình quản lý dấu trang (bookmark) có thể gồm 4 việc:” rồi tách bốn bullet, thêm các đề mục như “Lưu URL kèm giải thích”. C giữ nguyên văn bản.

Cả hai model thích B hơn D ở N3, lý do chủ yếu là đề mục/danh sách/chữ số tương thích mẫu. Gemini cũng ghi B có lỗi nghĩa nhỏ do thêm cách gọi “bạn”; Codex không ghi lỗi đó. Kết quả cho thấy các model thưởng cho cấu trúc trình bày dễ nhận biết. Nó chưa chứng minh B tái hiện đầy đủ nhịp, lựa chọn từ và giọng riêng của tác giả. D giữ gần nguồn hơn nhưng chưa chuyển nháp trung tính tới nét mẫu được các model nhận ra.

**N2, nguồn đếm bước mơ hồ.** Gốc và D giữ “Quy trình gồm năm bước”; A/B/C bỏ con số. Đây là chỗ cần quyết định của người biên tập/tác giả về cách nhóm bước. Không có nhãn con người để kết luận bên sửa hay bên giữ đúng hơn trong tác vụ thực tế.

## Kết luận trong phạm vi pilot

Dữ liệu này **không hỗ trợ quảng bá Vietnamizer là công cụ bắt chước giọng tốt hơn prompt đã có mẫu**. Với nháp trung tính, thêm mẫu trực tiếp cho tín hiệu mạnh hơn; bundle hiện hành thường giữ văn xuôi và chỉ sửa nhỏ. Nhận định “giữ gần nguồn hơn” có bằng chứng từ diff; nhận định “các chốt chặn gây ra kết quả này” mới là giả thuyết, vì chưa tách các thành phần bundle hoặc lặp lại việc sinh.

Với văn bản đã có giọng, D có ví dụ sửa gọn mà giữ nét sẵn có, nhưng chưa thể hiện lợi thế giọng rõ trước B. Nhãn nghĩa của D khá thuận lợi trong bộ nhỏ này, song bị giới hạn bởi ca N2, hai model và thiếu xác nhận con người. Kết quả này không phủ định hoặc thay thế benchmark biên tập tiếng Việt trước đây; nó khảo sát một năng lực khác.

Chưa chỉnh quy tắc, hồ sơ hoặc version theo kết quả pilot. Chưa đưa kết quả thành tuyên bố mới trong README. Nếu nghiên cứu tiếp, cần tách tương thích hình thức với đặc tính giọng, bổ sung nhãn giữ giọng trên chính bài của tác giả, và phân biệt biên tập giữ giọng với viết lại theo giọng được chọn. Đây là hướng đề xuất, không phải một đợt chạy mới đã được duyệt.

## Chart và dữ liệu để kiểm lại

Ba hình được xuất SVG/PDF cùng PNG xem nhanh, giữ từng ca và từng giám khảo, không tạo CI hoặc p-value. Phiếu thiếu hiển thị riêng, không bị tính thành hòa hoặc chưa rõ.

- [Chênh lệch D−B](../../artifacts/019-public-author-pilot-20261027-v2/figures/voice-primary-delta.svg).
- [Bốn phép so sánh](../../artifacts/019-public-author-pilot-20261027-v2/figures/voice-contrasts.svg).
- [Nhãn giữ nghĩa từng bản](../../artifacts/019-public-author-pilot-20261027-v2/figures/voice-meaning.svg).
- [Toàn bộ 32 đối chiếu trước/sau](../../artifacts/019-public-author-pilot-20261027-v2/before-after.html).
- [Điểm và trích dẫn](../../artifacts/019-public-author-pilot-20261027-v2/ratings.csv), [lựa chọn cặp](../../artifacts/019-public-author-pilot-20261027-v2/contrasts.csv), [tổng hợp theo tầng/model](../../artifacts/019-public-author-pilot-20261027-v2/summary.csv).

Các liên kết artifacts là dữ liệu local bị gitignore. Gói lưu trữ kèm raw/code/provenance được cung cấp cùng báo cáo; không mặc định dữ liệu đã được công khai lên repository.


## Nguồn và phạm vi

Pilot dùng các bài blog kỹ thuật tiếng Việt được công bố dưới tên **Van-Duyet Le (Duyệt)**, giai đoạn 2015–2016, tại [duyet/blog](https://github.com/duyet/blog/tree/397efbf471b958e65eeecb87eba913d0a1f99620). Nguồn được khóa theo revision, lưu Markdown gốc, URL, metadata và SHA-256. Bài ghi rõ đăng lại từ người khác bị loại. Attribution của nhà xuất bản là căn cứ chọn giọng tham chiếu; không coi đây là chứng nhận tác giả viết hoàn toàn không có trợ giúp hoặc xác nhận giọng hiện tại của tác giả.

Chín bài được chia theo vai trò trước khi gọi model:

| Vai trò | Bài |
|---|---|
| Ba mẫu cho agent | Nodejs là gì; package.json; Docker cơ bản |
| Hai mẫu chỉ cho giám khảo | Columnar/Graph Database; Offline-First |
| Bốn bản có sẵn giọng | Git; DNS; giao diện Sublime Text; giao diện Ubuntu |

Các bài và họ chủ đề không giao nhau giữa ba vai trò. Hai bài về giao diện cùng một họ chủ đề, nên bốn bản có giọng chỉ bao phủ ba họ. Hai bản thử ngắn 123/109 từ và hai mẫu ngắn 199/140 từ được giữ nguyên, không kéo dài bằng nội dung tự tạo. Toàn bộ recipe trích đoạn và nguồn đầy đủ nằm trong `corpus.json` của gói dữ liệu.

Bốn nháp AI trung tính được tạo riêng từ brief giả lập về theo dõi công việc, thử thư viện, quản lý dấu trang và gỡ lỗi. Agent tạo nháp không nhận mẫu tác giả hoặc Vietnamizer. Cả bốn nhánh biên tập nhận cùng một nháp; không sửa tay hoặc tạo lại nháp sau khi xem kết quả. N2 có điểm mơ hồ được ghi nhận trước chấm: nói “năm bước” nhưng ghép phiên bản/môi trường thành một hành động liệt kê. Phải đọc các nhãn nghĩa liên quan số bước với giới hạn này.

## Thiết kế tách tác động của mẫu và skill

| Nhánh | Mẫu giọng | Vietnamizer 0.12.1 |
|---|---|---|
| A | Không | Không |
| B | Có | Không |
| C | Không | Có |
| D | Cùng byte với B | Cùng bundle với C |

Tất cả 32 ô dùng cùng Codex, yêu cầu `gpt-6.1-sol`, effort `medium`, phiên mới và cùng prompt chung. Chỉ hai yếu tố trên thay đổi. Bundle gồm core, resolver, bảng tra, hướng dẫn giữ giọng từ mẫu và profile/card hướng dẫn kỹ thuật phù hợp kênh. Đây là phép đo cả bundle, chưa tách tác động của từng tài liệu.

So sánh chính **D với B** kiểm tra phần tăng thêm của Vietnamizer khi đã có cùng mẫu. B với A đo tác động của mẫu; C với A đo skill khi chưa có mẫu; D với C đo mẫu khi đã có skill. Chênh lệch tương tác `(D−C)−(B−A)` chỉ là mô tả trên điểm thứ bậc, không phải bằng chứng cơ chế hay kiểm định thống kê.

Codex và Gemini `gemini-3.8-flash-medium` chấm các bản gốc và ứng viên ẩn tên nhánh. Họ nhận hai mẫu riêng, không nhận skill, tên tác giả hay đánh giá của nhau. Các ứng viên có mã ngẫu nhiên và đảo vị trí giữa hai model. Hai model chấm **không phải hai agent biên tập đem so chất lượng với nhau**; agent biên tập luôn là Codex.

Giọng và độ dễ đọc dùng điểm 1–5. Nghĩa được báo riêng: không thấy lỗi, lỗi nhỏ, sai ý/dữ kiện, chưa rõ. Mỗi mục phải có trích dẫn nguyên văn từ văn bản và mẫu. Lựa chọn cặp có trái/phải/hòa/chưa rõ; không cộng điểm giọng để bù lỗi nghĩa. Trích dẫn tồn tại chỉ chứng minh quote có trong nguồn, chưa chứng minh lý do chấm đúng.

Bốn lượt hiệu chuẩn kiểm tra đảo dữ kiện rõ và hòa cho hai bản giống hệt. Cả bốn qua cổng này; không có nhãn tác giả để xác nhận khả năng chấm đúng giọng. Schema thực thi buộc điểm giọng/dễ đọc bằng số, nên không được suy mức chắc chắn từ việc model đã cho điểm.

## Giới hạn diễn giải

Một tác giả, tám bản nháp và một lần sinh mỗi ô chỉ đủ khảo sát cách chạy và tìm tín hiệu. Không có người chấm hoặc tác giả xác nhận, không có độ ổn định qua nhiều lần sinh, không có ước lượng biến thiên giữa tác giả. Các điểm trong cùng block và các bài gần chủ đề có tương quan. Không gộp 32 đầu ra hoặc hai model thành số nguồn độc lập, không đưa CI/p-value giả chính xác.

Codex vừa sinh vừa chấm nên có nguy cơ thiên lệch cùng nhà cung cấp; Gemini không tự trở thành chuẩn đúng. Các bài công khai có thể xuất hiện trong dữ liệu huấn luyện. “Mới với dự án” không đồng nghĩa model chưa từng thấy. Nội dung kỹ thuật lịch sử được giữ theo yêu cầu biên tập, không dùng làm hướng dẫn kỹ thuật cập nhật.

Gói dữ liệu lưu native CLI events, stdout/stderr nhị phân, input/schema, cấu hình, usage, session ID, mapping và dấu kiểm toàn vẹn. Đây là raw ở lớp CLI, không phải bản ghi HTTP bên trong nhà cung cấp hoặc chứng thực backend. Task-local agent và guard theo dõi tool thực tế không được gọi là cách ly ở cấp hệ điều hành.
