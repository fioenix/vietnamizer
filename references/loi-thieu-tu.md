# Thiếu từ và cấu trúc cần hoàn chỉnh

Tra khi có nghi vấn đúng nhóm ở bảng của SKILL.md; đọc cả Không flag trước khi sửa.
Cần ví dụ hư từ/loại từ mới tra mục liên quan trong `references/bang-tra-cuu.md`.
Các chốt và quyền sửa do core sở hữu; không đọc tiếp nhóm khác chỉ vì có liên kết.

### V1. Thiếu bổ ngữ kết quả và bổ ngữ hướng

**Dấu hiệu:** câu đang nói đến khả năng, kết quả hoặc hướng của hành động nhưng động từ thiếu từ đi kèm như *được, ra, thấy, xong, hết, nổi, mất, lên, xuống, vào, đi, lại, tới*. Lỗi dễ gặp ở các động từ *tìm, nghe, nhìn, nhớ, hiểu, biết*.
**Vì sao:** trong tiếng Việt, từ đứng sau động từ thường cho biết hành động có đạt kết quả hay không. Bỏ từ đó có thể làm câu đổi nghĩa hoặc dừng trước khi ý được nói hết.
**Sửa:** *"Đã thử ba cách mà vẫn không giải quyết vấn đề"* → *"...vẫn không giải quyết **được** vấn đề"*. *"vẫn không tìm nguyên nhân"* → *"vẫn không tìm **ra** nguyên nhân"*. *"đọc toàn bộ tài liệu"* → *"đọc **hết** tài liệu"*. Chọn từ theo ý câu, không mặc định thêm *được* sau mọi động từ.
**Không flag:** hành động đang diễn ra hoặc lặp lại (*"Tôi đọc tài liệu mỗi sáng"*), mô tả chức năng (*"Hệ thống xử lý yêu cầu HTTP"*), câu lệnh và quy trình từng bước (*"Nhấn nút, chọn tệp, tải lên"*). Giữ câu rút gọn khi ngữ cảnh đủ rõ hoặc mạch văn cho thấy sự bỏ lửng có chức năng. V1 không cho phép tự điền đối tượng của động từ, chọn riêng một đối tượng trong nhiều khả năng hoặc kéo dài câu chỉ để đủ khuôn; đọc mục Phân biệt câu ngắn có chủ ý với câu thiếu từ.

### V2. Cặp liên từ bị thiếu từ ở vế sau

**Dấu hiệu:** câu mở một quan hệ bằng *vì, do, nhờ, tuy, mặc dù, nếu, hễ, càng, không những, vừa* nhưng vế sau thiếu từ nối cần thiết. Các cặp thường gặp: *vì / do... nên*; *nhờ... mà*; *tuy / mặc dù / dù... nhưng / vẫn*; *nếu / hễ / chỉ cần... thì*; *càng... càng*; *không những... mà còn*; *vừa... vừa*.
**Vì sao:** từ ở vế sau giúp người đọc nhận ra quan hệ nhân quả, điều kiện, nhượng bộ hoặc tăng tiến. Khi thiếu nó, hai vế có thể vẫn hiểu được nhưng câu dễ bị hẫng hoặc mơ hồ.
**Sửa:** *"Vì hệ thống chưa có cache, thời gian phản hồi tăng gấp ba"* → *"Vì hệ thống chưa có cache **nên** thời gian phản hồi tăng gấp ba"*. *"Nếu tình trạng kéo dài, chúng tôi phải mở rộng"* → *"Nếu tình trạng kéo dài **thì** chúng tôi phải mở rộng"*. Cũng có thể bỏ từ mở đầu nếu câu vẫn giữ đúng quan hệ; không nhất thiết lúc nào cũng thêm vế hô ứng.
**Không flag:** câu nói tự nhiên đã rõ quan hệ dù lược một đầu của cặp; tít, sapo; cụm nối đứng độc lập như *"Vì thế, chúng tôi dừng dự án."* Không thêm từ chỉ để câu đủ khuôn.

### V3. Thiếu "là" trong câu định nghĩa hoặc lựa chọn

**Dấu hiệu:** một danh ngữ nêu khái niệm, phương án hoặc lựa chọn nối thẳng với phần giải thích mà thiếu *là*: *"Cách xử lý đơn giản nhất tăng số worker"*.
**Vì sao:** *là* cho biết phần sau đang định nghĩa hoặc xác định phần trước. Thiếu nó khiến hai cụm dính vào nhau và quan hệ trong câu không rõ.
**Sửa:** *"Cách xử lý đơn giản nhất tăng số worker"* → *"Cách xử lý đơn giản nhất **là** tăng số worker"*. *"Mục tiêu của bước này loại bỏ bản ghi trùng"* → *"Mục tiêu của bước này **là** loại bỏ bản ghi trùng"*.
**Không flag:** tính từ làm vị ngữ không cần *là*: *"Cô ấy đẹp"* là câu đúng. Cũng không thêm *là* vào câu chỉ trạng thái hoặc hành động. Không áp dụng pattern này cho tiêu đề, nhãn, mục lục hoặc ô bảng.

### V4. Thiếu hoặc lạm dụng từ chỉ thời gian và trạng thái

**Dấu hiệu:** câu cần phân biệt việc đã xong, đang diễn ra, vẫn tiếp tục hoặc chưa xảy ra nhưng thiếu các từ như *đã, đang, rồi, vẫn, còn, mới, sắp, từng, chưa*. Chiều ngược lại là lặp *đã, đang, sẽ* dù mốc thời gian đã rõ.
**Vì sao:** tiếng Việt chỉ đánh dấu thời gian hoặc trạng thái khi ngữ cảnh cần. Bỏ hết làm chuỗi sự việc khó theo dõi; thêm vào mọi động từ lại tạo ra sự lặp không cần thiết.
**Sửa:** *"Năm 2019, công ty đã mở chi nhánh đầu tiên"* → *"Năm 2019, công ty mở chi nhánh đầu tiên"*. *"Lúc tôi gọi, đội chuẩn bị tài liệu bàn giao"* → *"Lúc tôi gọi, đội **đang** chuẩn bị tài liệu bàn giao"*. Thêm hoặc bỏ từ dựa trên mốc thời gian và trạng thái thật của câu.
**Không flag:** *đã* là dấu hiệu duy nhất cho biết sự việc thuộc quá khứ; định nghĩa, thông số và mô tả chức năng không gắn với thời điểm; đoạn đã nêu mốc thời gian rõ và các câu sau không cần nhắc lại.

### V5. Thiếu hoặc sai loại từ

**Dấu hiệu:** danh từ chỉ một vật hoặc con vật cụ thể đã được đếm, chỉ định nhưng thiếu loại từ cần thiết; hoặc loại từ không hợp với danh từ trong văn bản chuẩn. Ví dụ rõ là *"nuôi ba mèo"* hoặc *"hai cái sách"*.
**Vì sao:** loại từ cho biết danh từ đang được nói đến như một cá thể thuộc nhóm nào. Thiếu hoặc dùng sai loại từ có thể khiến câu nghe như bản dịch từng từ.
**Sửa:** *"Cô ấy nuôi ba mèo"* → *"Cô ấy nuôi ba **con** mèo"*. *"Tôi mang theo hai cái sách"* → *"Tôi mang theo hai **quyển** sách"*. Chọn loại từ theo danh từ và theo cách dùng quen thuộc trong ngữ cảnh.
**Không flag:** danh từ mang nghĩa khái quát (*"Xe là phương tiện chủ yếu ở đô thị"*), danh từ khối hoặc trừu tượng, thuật ngữ kỹ thuật, tiêu đề, bảng biểu và lối nói rút gọn đã rõ nghĩa. Không sửa cách dùng loại từ ổn định của vùng miền nếu người dùng muốn giữ giọng đó.

### V6. Câu hỏi hoặc lời nhờ không đúng ý định giao tiếp

**Dấu hiệu:** ngữ cảnh cần một câu hỏi mở nhưng câu chỉ hỏi có hoặc không; hoặc lời nhờ giữa người với người dùng nguyên mẫu *Vui lòng + động từ* dù giọng văn xung quanh thân mật. Câu lệnh trơ cũng cần xem lại nếu nó vô tình tạo giọng ra lệnh.
**Vì sao:** câu hỏi và lời nhờ tiếng Việt thường cho biết người nói muốn loại câu trả lời nào và quan hệ giữa hai bên ra sao. Dùng sai khung có thể làm đổi ý định hoặc làm giọng câu lệch khỏi cuộc hội thoại.
**Sửa:** nếu muốn hỏi nội dung kế hoạch, *"Bạn có kế hoạch cho tuần sau?"* → *"Tuần sau bạn có kế hoạch **gì chưa**?"*. Với lời nhờ, chọn cách xưng hô và tiểu từ đã có trong cuộc hội thoại; nếu chưa biết quan hệ giữa hai bên thì giữ câu trung tính hoặc hỏi người dùng, không tự gán *anh, chị, em*.
**Không flag:** câu hỏi có hoặc không vốn đúng ý định; câu hỏi tu từ; tiêu đề dạng câu hỏi; biểu mẫu, giao diện và thông báo hệ thống như *"Vui lòng nhập mật khẩu"*. *Vui lòng* cũng hợp lệ trong thư từ hoặc thông báo trang trọng.

### V7. "của" thừa trong cụm danh từ

**Dấu hiệu:** nhiều cụm *danh từ + của + danh từ* xuất hiện gần nhau, trong đó *của* chỉ quan hệ thuộc tính hoặc phân loại chứ không làm rõ chủ thể, nguồn gốc hay sở hữu.
**Vì sao:** tiếng Việt thường ghép trực tiếp hai danh từ khi quan hệ đã rõ, chẳng hạn *hiệu suất hệ thống* hoặc *cấu hình máy chủ*. Giữ mọi *của* theo cấu trúc tiếng Anh làm câu dài và nặng.
**Sửa:** *"Hiệu suất của hệ thống phụ thuộc vào cấu hình của máy chủ"* → *"Hiệu suất hệ thống phụ thuộc vào cấu hình máy chủ"*. Xét từng chữ *của*: bỏ khi quan hệ chỉ là thuộc tính hoặc phân loại; giữ khi nó xác định người, tổ chức, nguồn gốc hoặc quyền sở hữu.
**Không flag:** bỏ *của* làm câu mơ hồ hoặc tạo chuỗi danh từ khó đọc; văn bản pháp lý cần nêu rõ chủ thể quyền; các cụm sở hữu thật như *xe của tôi* và *quyết định của ban giám đốc*. Hai chữ *của* trong cùng một cụm không tự động là lỗi.

### V8. "các" và "những" được thêm theo dấu số nhiều

**Dấu hiệu:** *các* hoặc *những* được lặp trước nhiều danh từ dù số nhiều đã rõ từ ngữ cảnh; hoặc dùng trước danh từ khối, danh từ trừu tượng mà câu không chia chúng thành từng loại hay từng trường hợp.
**Vì sao:** tiếng Việt không bắt buộc đánh dấu số nhiều ở mọi danh từ. *Các* thường chỉ toàn bộ một tập đã xác định, còn *những* thường chỉ một phần hoặc một nhóm chưa liệt kê hết; dùng hai từ mà không xét phạm vi có thể làm đổi nghĩa.
**Sửa:** *"Các nhà nghiên cứu phân tích các mẫu dữ liệu và phát hiện các bất thường trong các kết quả"* → *"Các nhà nghiên cứu phân tích mẫu dữ liệu và phát hiện bất thường trong kết quả"*. Bỏ từng từ một rồi kiểm tra xem phạm vi còn rõ không; không xoá đồng loạt.
**Không flag:** *các* hoặc *những* đang phân biệt rõ phạm vi; cụm như *các thông tin sau, các bên, các cấp, các loại*; văn bản pháp quy và danh sách đối tượng áp dụng. Không đặt giới hạn cứng về số lần xuất hiện trong một câu.

### V20. Từ hoặc cụm từ bị thiếu một tiếng

**Dấu hiệu:** một tiếng đứng riêng nhưng ý câu cần một từ hoặc cụm hai tiếng đầy đủ. Có ba trường hợp:

1. Tiếng đang dùng hầu như không đứng riêng với nghĩa đó: *rườm* thay cho *rườm rà*, *bỡ* thay cho *bỡ ngỡ*, *chới* thay cho *chới với*.
2. Tiếng có thể đứng riêng nhưng mang nghĩa khác trong câu: *hụt* thay cho *hụt hẫng*.
3. Tiếng có nghĩa gần đúng nhưng không kết hợp tự nhiên với những từ xung quanh trong nghĩa đang dùng. Trong hướng dẫn biên tập, *"Chỉ được rà typography"* cần thành *"Chỉ được rà soát typography"* nếu ý là kiểm tra kỹ từng chi tiết. Nếu muốn nói các đầu việc thiếu liên kết với nhau, *"danh sách việc rời"* cần thành *"danh sách các đầu việc rời rạc"*.

**Vì sao:** câu có thể vẫn đúng cấu trúc dù thiếu một tiếng, nên lỗi này dễ lọt qua kiểm tra chính tả. Một tiếng có thể là từ độc lập trong cấu trúc này nhưng không dùng được với cùng nghĩa hoặc cùng vai trò trong cấu trúc khác. Vì vậy, việc từ đó có tồn tại khi đứng riêng chưa đủ để kết luận cách dùng hiện tại là đúng.

**Sửa:** *"Câu này đúng ngữ pháp nhưng đọc lên thấy hụt"* → *"...thấy **hụt hẫng**"*. *"Quy trình còn rườm"* → *"...còn **rườm rà**"*. Trước khi thêm tiếng, kiểm tra lần lượt: tiếng hiện tại có dùng độc lập với cùng nghĩa và cùng vai trò trong câu không; nó có kết hợp tự nhiên với những từ đứng cạnh không; thêm tiếng có hoàn chỉnh đúng ý hay chỉ đổi phong cách; văn bản có đang cố ý viết rút gọn không. Không chắc thì để nguyên.

**Không flag:** từ đơn hợp lệ đúng nghĩa (*đi, ăn, vui, buồn, đẹp, sạch*). Giữ *rời* trong *rời công ty, rời vị trí, tách rời, bộ phận rời*; giữ *rà* trong *rà lại tài liệu, rà kỹ, rà một lượt, rà kế hoạch một lần nữa*; các nghĩa chuyên biệt như *rà mìn, rà sóng, rà kim, máy bay rà thấp*; và cách nói nội bộ như *rà code, rà log* khi mẫu giọng cho phép. Với các cặp như *đẹp / đẹp đẽ, sạch / sạch sẽ*, thêm tiếng thứ hai chỉ là lựa chọn phong cách. Thuật ngữ rút gọn theo quy ước ngành và văn phong tối giản có chủ ý cũng không flag; riêng với dòng liệt kê và nhãn, đọc mục *Phân biệt câu ngắn có chủ ý với câu thiếu từ* trước khi bỏ qua, vì tối giản không cho phép bỏ thành phần mà ý câu thực sự cần hoặc cắt tiếng bắt buộc của một từ hai tiếng.

## Phân biệt câu ngắn có chủ ý với câu thiếu từ

Câu ngắn không tự động là câu cụt. Trước khi thêm *là, thì, được, nên, rồi* hoặc một loại từ, hãy kiểm tra:

1. Người đọc có xác định được quan hệ giữa các thành phần và hiểu đúng ý câu không?
2. Từ định thêm có hoàn chỉnh một cấu trúc đang thiếu hay chỉ làm câu mềm và dài hơn?
3. Thể loại có chủ động dùng câu rút gọn không, chẳng hạn tin nhắn, hướng dẫn thao tác, ghi chú vận hành hoặc tài liệu kỹ thuật?
4. Thành phần bị lược là loại nào? Đối tượng đã rõ từ ngữ cảnh có thể lược; không ép *"Soạn xong rồi dừng"* phải nêu lại đối tượng khi đoạn trước đã nói rõ đang soạn tài liệu nào. Giữ sự bỏ lửng có chức năng, không tự chọn một đối tượng trong nhiều khả năng. Ngược lại, vẫn phải giữ tiếng bắt buộc của một từ hai tiếng và bổ ngữ kết quả/hướng mà ý câu thực sự cần; V1/V20 sở hữu các lỗi đó. *"Đã tìm khắp nhà nhưng vẫn không tìm chìa khóa"* cần *"...không tìm thấy chìa khóa"* khi ngữ cảnh nói tìm không ra, không phải không muốn tìm.

Khi kiểm câu thiếu từ, câu đã rõ nghĩa và phù hợp với thể loại thì để nguyên; chỉ bổ sung thành phần khi pattern chỉ ra được chỗ thiếu và từ thêm vào không làm đổi ý. Điều chỉnh phong cách có yêu cầu riêng vẫn theo chốt 1, không dùng nhu cầu đổi giọng để kết luận câu thiếu từ.
