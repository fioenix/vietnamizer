# Nguồn, mức độ tin cậy và ghi nhận

[← README](../README.md)

## Mức độ tin cậy và nguồn

Mỗi quy tắc phải chỉ rõ nó dựa trên tài liệu, quan sát có bản đối chiếu trong `calibration/LOG.md` hay suy luận từ khác biệt giữa tiếng Anh và tiếng Việt. Repo chưa có bộ ngữ liệu đủ để đặt ngưỡng tần suất, nên số lần xuất hiện chỉ giúp tìm chỗ cần đọc lại.

### Nguồn quy phạm và học thuật

| Nguồn | Nội dung được dùng |
|---|---|
| [Nghị định 30/2020/NĐ-CP, Phụ lục II](https://thuvienphapluat.vn/chinh-sach-phap-luat-moi/vn/bieu-mau/55095/tong-hop-cac-phu-luc-ve-van-ban-hanh-chinh-moi-nhat-ban-hanh-kem-theo-nghi-dinh-30-2020) | Cách viết hoa tên cơ quan trong văn bản hành chính, dùng cho T1 |
| [Quyết định 1989/QĐ-BGDĐT năm 2018](https://thuvienphapluat.vn/van-ban/Giao-duc/Quyet-dinh-1989-QD-BGDDT-2018-quy-dinh-chinh-ta-Chuong-trinh-sach-giao-khoa-giao-duc-pho-thong-445355.aspx) | Điều 8 và 9, dùng để xác định phạm vi của dấu thanh và i/y |
| [ViDetect, arXiv:2405.03206](https://arxiv.org/abs/2405.03206) | Nghiên cứu phát hiện văn bản AI tiếng Việt; không dùng làm danh sách pattern ngôn ngữ |
| [VietBinoculars, arXiv:2509.26189](https://arxiv.org/abs/2509.26189) | Nghiên cứu phát hiện văn bản AI tiếng Việt; không dùng làm danh sách pattern ngôn ngữ |
| [A Survey on Zero Pronoun Translation, arXiv:2305.10196](https://arxiv.org/abs/2305.10196) | Tham khảo về lược đại từ và dịch thuật |
| [Nghiên cứu dịch câu bị động Anh–Việt](https://i-jte.org/index.php/journal/article/view/90) | Tham khảo cho V16; đối tượng nghiên cứu là người dịch |
| [Danh hoá động từ trong danh ngữ](https://tcgd.tapchigiaoduc.edu.vn/index.php/tapchi/article/view/4322) | Tham khảo cho V15 |
| [Cú pháp tiếng Việt nhìn từ ngữ pháp chức năng](https://vjol.info.vn/index.php/tdm/article/download/93747/79245/) | Tham khảo cho cấu trúc đề–thuyết ở V13 |
| [Tình thái từ](https://voer.edu.vn/c/tinh-thai-tu/4491bb06/712ccc96) và [tiểu từ tình thái trong hành động ngỏ lời](https://vusta.vn/mot-so-tieu-tu-tinh-thai-bieu-dat-tinh-lich-su-trong-hanh-dong-ngo-loi-bang-tieng-viet-p72715.html) | Tham khảo cho B14 |
| [Loại từ CON và CÁI](http://ngonngu.org/Con_Cai.htm) | Tham khảo cho V5 |

### Nguồn trình bày lại và nguồn cộng đồng

Những nguồn dưới đây giúp tìm thuật ngữ hoặc ghi nhận hiện tượng, không được dùng riêng làm căn cứ quy phạm:

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Wikipedia: Loại từ](https://vi.wikipedia.org/wiki/Lo%E1%BA%A1i_t%E1%BB%AB)
- [Wikipedia: Dấu gạch ngang](https://vi.wikipedia.org/wiki/D%E1%BA%A5u_g%E1%BA%A1ch_ngang)
- [Wikipedia: Dấu ngoặc kép](https://vi.wikipedia.org/wiki/D%E1%BA%A5u_ngo%E1%BA%B7c_k%C3%A9p)
- [Phân biệt gạch ngang và gạch nối, Giáo dục TP.HCM](https://giaoduc.edu.vn/phan-biet-dau-gach-ngang-va-gach-noi/)
- [Brands Vietnam: dấu hiệu nội dung viết bởi AI](https://help.brandsvietnam.com/vi/article/dau-hieu-nhan-biet-noi-dung-duoc-viet-boi-ai-3zy07d/)
- [Cặp quan hệ từ, HOCMAI](https://hoctot.hocmai.vn/dau-hieu-nhan-biet-quan-he-tu-va-cap-quan-he-tu.html)
- [Đề–thuyết, Ngày ngày viết chữ](https://ngayngayvietchu.com/thu-phan-tich-cau-tieng-viet-theo-cau-truc-de-thuyet/)

### Nguồn cộng đồng về giữ giọng theo mẫu

Tham khảo phương pháp từ [write-like-me](https://github.com/ddutchie/write-like-me/blob/98e615d34cac1a31d6ee14fcc0fb6b1a57cd4835/skills/me/SKILL.md), [Synthesis Voice Profiler](https://github.com/synthesisengineering/synthesis-skills/blob/53fca8aeb81b42b21e98ed044b30352611731ee8/skills/synthesis-voice-profiler/SKILL.md) và [Voice Builder](https://github.com/charlie947/social-media-skills/blob/10ca79c0ec0be0f7654d19cd4f0c86b6fa6ed23b/skills/voice-builder/SKILL.md). Đây là thiết kế workflow cộng đồng, chưa phải bằng chứng hiệu quả tiếng Việt. [Hồ sơ đối chiếu](../specs/016-sample-voice-preservation/research.md) ghi revision, giấy phép và phần chọn/loại; không chép template hoặc luật tiếng Anh vào skill.

### Nguồn gợi ý giả thuyết

- [`blader/humanizer` 3.0.0](https://github.com/blader/humanizer/tree/v3.0.0) chỉ được dùng để nêu
  giả thuyết cho V23–V25, phần mở rộng B8 và K7. Quyết định tiếng Việt dựa trên các ca dương/âm và
  bằng chứng ghi ngày 28/09/2026 trong `calibration/LOG.md`; repo upstream không được coi là nguồn
  quy phạm tiếng Việt.

### Nguồn còn thiếu

- V3 và V13 cần thêm nguồn gốc về lý thuyết đề–thuyết thay cho các bài trình bày lại.
- V16 cần thêm nghiên cứu công bố trực tiếp về đối chiếu câu bị động Anh–Việt.

## Tác giả và ghi nhận

`vietnamizer` do Fioenix thiết kế và duy trì. Codex và Claude Code được dùng làm agent kỹ thuật để
hỗ trợ nghiên cứu, triển khai, kiểm thử và review.

Cách đóng gói và khung **Dấu hiệu / Vì sao / Sửa / Không flag** tham khảo
[blader/humanizer](https://github.com/blader/humanizer) cùng hướng dẫn của WikiProject AI Cleanup.
Các pattern tiếng Việt được xây dựng riêng cho repo này.
