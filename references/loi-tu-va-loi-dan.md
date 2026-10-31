# Thuật ngữ, lời dẫn và tàn dư trợ lý

Tra khi có nghi vấn đúng nhóm ở bảng của SKILL.md; đọc cả Không flag trước khi sửa.
Các chốt và quyền sửa do core sở hữu; không đọc tiếp nhóm khác chỉ vì có liên kết.

### V19. Chêm tiếng Anh không hợp người đọc hoặc lĩnh vực

**Dấu hiệu:** phải xét người đọc, lĩnh vực và mẫu văn trước khi kết luận. Trong tài liệu nội bộ của một ngành thường dùng thuật ngữ tiếng Anh, việc dịch toàn bộ thuật ngữ sang những cụm tiếng Việt xa lạ có thể làm câu thiếu tự nhiên. Ngược lại, trong giáo trình, đề án hoặc văn bản viết cho người đọc ngoài ngành, chêm tiếng Anh không giải thích có thể làm sai giọng văn. Cũng cần xem lại khi từ tiếng Anh được in nghiêng, dịch trong ngoặc hoặc chèn theo cùng một khuôn ở mọi lần xuất hiện dù không cần thiết.

**Vì sao:** thuật ngữ là quy ước của một cộng đồng sử dụng, không phải phép thay từ cố định giữa tiếng Anh và tiếng Việt. Cùng một từ có thể tự nhiên trong chat nội bộ nhưng không phù hợp với giáo trình. Việc có hoặc không có tiếng Anh tự nó không chứng minh văn bản do người hay AI viết.

**Sửa:** với tài liệu nội bộ, giữ hoặc trả lại thuật ngữ tiếng Anh khi mẫu văn, tài liệu cùng repo hoặc cách dùng ổn định của ngành cho thấy đó là tên gọi quen thuộc: *deploy, cloud, endpoint, benchmark, deadline*. Với nội dung học thuật hoặc viết cho người ngoài ngành, dùng từ tiếng Việt đã phổ biến; nếu cần giữ thuật ngữ tiếng Anh thì giải thích ở lần xuất hiện đầu. Không tự thêm tiếng Anh chỉ vì văn bản thuộc ngành kỹ thuật. Khi chưa rõ người đọc hoặc giọng cần đổi, giữ cách dùng thuật ngữ ổn định trong nguồn; không suy yêu cầu thuần Việt từ riêng nhãn thể loại. Có từ tiếng Việt tương đương chưa đủ để dịch đồng loạt; cần chỉ ra vấn đề với người đọc, cách dùng hoặc yêu cầu hiện tại.

**Không flag:** người viết chủ động thuần Việt hoá nhất quán; văn bản dành cho người đọc ngoài ngành; thuật ngữ chưa có từ tiếng Việt tương đương; cách chêm tiếng Anh xuất hiện ổn định trong mẫu văn của người dùng. Không sửa khi chưa biết cộng đồng đó thực sự gọi thuật ngữ như thế nào.

### V21. Tàn dư lượt hội thoại của trợ lý

**Dấu hiệu:** lời chào, lời khen, lời mời làm tiếp hoặc câu kết của một lượt trả lời còn nằm trong văn bản đáng lẽ phải tự đứng được: *Chắc chắn rồi!*, *Câu hỏi hay!*, *Dưới đây là...*, *Hy vọng nội dung này hữu ích*, *Bạn có muốn tôi viết thêm phần...*, *Bạn cần chỉnh gì nữa không?*, *Chúc bạn thành công!*
**Vì sao:** những câu này nói với người đặt yêu cầu chứ không nói với người đọc tài liệu. Chúng dễ lọt qua vì thường ôm lấy phần nội dung thật ở giữa, nên người đọc lướt qua mà không thấy chỗ nối.
**Sửa:** bỏ phần vỏ, giữ nguyên nội dung bên trong. *"Chắc chắn rồi! Dưới đây là ba bước triển khai: ..."* → *"Ba bước triển khai: ..."*. Nếu câu hỏi ở cuối chứa một việc cần người đặt yêu cầu quyết, hãy chuyển nó sang lượt trả lời trong hội thoại thay vì xoá.
**Không flag:** hội thoại được trích lại làm ví dụ hoặc dữ liệu; kịch bản trợ lý ảo, nội dung mẫu và tài liệu đang bàn về chính những câu đó; lời chào, lời chúc và câu kết trong thư, email hoặc tin nhắn, vì đó là quy ước thư từ có trước chatbot.

### V22. Rào trước về nguồn rồi đưa phỏng đoán

**Dấu hiệu:** một câu nêu giới hạn của nguồn hoặc của người viết, chẳng hạn *tính đến thời điểm hiện tại*, *theo thông tin hiện có*, *thông tin về X không được công bố rộng rãi*, *hồ sơ công khai không nêu*; rồi câu sau vẫn đưa ra một chi tiết cụ thể bằng *có thể đã*, *nhiều khả năng*, *được cho là*, *thường thì*, trong khi văn bản không có nguồn nào cho chi tiết ấy.
**Vì sao:** hai vế cộng lại tạo cảm giác thận trọng nhưng vẫn đưa một dữ kiện không kiểm chứng được vào văn bản. Người đọc thường nhớ chi tiết và quên lời rào đứng trước nó.
**Sửa:** giữ điều nguồn nói, bỏ phần phỏng đoán. *"Thông tin về năm thành lập không được công bố. Công ty nhiều khả năng bắt đầu hoạt động từ đầu những năm 2000."* → *"Tài liệu hiện có không nêu năm thành lập."*. Nếu bản gốc có nguồn thì nêu nguồn đó; không tự thêm nguồn, theo quy tắc chốt chặn 2.
**Không flag:** dự báo, kịch bản, phân tích rủi ro và đề xuất, nơi phỏng đoán chính là nội dung được yêu cầu và đã ghi rõ là phỏng đoán. Câu nêu mốc dữ liệu thật như *"số liệu cập nhật đến 30/06/2026"*. Phần giới hạn nghiên cứu trong bài khoa học. Ước lượng có nêu cơ sở tính.

### V23. Phản biện một ý không có đối tượng

**Dấu hiệu:** câu dùng *không phải, không ai phủ nhận, đừng hiểu lầm, một cách dễ nghĩ tới là... nhưng* để bác bỏ hoặc tự bảo vệ trước một ý không xuất hiện trong câu hỏi, phần trước, trích dẫn hay các phương án đang xét. Bỏ vỏ phản biện thì khẳng định còn lại vẫn trọn ý và không đổi dữ kiện.
**Vì sao:** câu dựng thêm một lập trường rồi mới bác bỏ nó, khiến người đọc phải theo dõi một cuộc tranh luận không tồn tại trong mạch văn. Lỗi nằm ở đối tượng phản biện bị thiếu, không nằm ở bản thân cấu trúc phủ định.
**Sửa:** cắt vỏ phản biện và nói thẳng khẳng định thật. *"Không ai phủ nhận tốc độ là quan trọng. Lỗi hiện tại nằm ở hàng đợi bị khóa."* → *"Lỗi hiện tại nằm ở hàng đợi bị khóa."* Không tự bổ sung người hoặc ý kiến để làm đối tượng tranh luận.
**Không flag:** câu đang trả lời một câu hỏi, phản hồi một trích dẫn hoặc ý kiến đã nêu, so sánh phương án trong ADR/FAQ, phân biệt hai khái niệm dễ nhầm đã được định nghĩa, hoặc giữ một đối lập có thông tin thật. Với khuôn song hành chỉ nâng giọng hoặc lặp ý, xem B5.
