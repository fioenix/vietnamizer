"""Feature 011 SC-003: label–value lines are recognized only from explicit structure.

Labels were assigned by the agent, not a native-speaker annotator (task T023 asks the owner to
review them). Recognized: bold labels, and plain labels inside a field list of at least two adjacent
label items. Everything else is prose, including a lone plain `Nhãn: giá trị` line.
"""
import time
import unittest

from jev.preparation import prepare_document

FIELD_LIST_A = """- Ngày: 22/10/2026 (Asia/Ho_Chi_Minh)
- Trạng thái: đang xử lý
- Người viết: Fio
- Phiên bản: v0.4.19
- Mục tiêu: giảm thời gian xử lý đơn
- Phạm vi: chỉ các cửa hàng ở Hà Nội
- Liên hệ: nhóm vận hành
- Hạn chót: 30/11/2026
- Độ ưu tiên: cao
- Người duyệt: trưởng nhóm dữ liệu"""

FIELD_LIST_B = """* Môi trường: staging
* Chi phí: khoảng 1.200.000 đồng mỗi tháng
* Tần suất: 15 phút một lần
* Nguồn: báo cáo tuần 42
* Trạng thái hiện tại: chờ duyệt
* Ghi chú: chưa tính phí vận chuyển"""

BOLD = [
    '- **Cách chấm:** dùng cùng một giám khảo cho mọi hệ thống',
    '**Đầu vào:** file CSV xuất từ hệ thống kho',
    '- **Kết quả**: p95 giảm từ 800 ms xuống 450 ms',
    '**Rủi ro:** dữ liệu cũ chưa được làm sạch',
]

NOT_LABEL = [
    'Trạng thái: đang xử lý',
    '- Người phụ trách: chị Lan',
    'Kết quả lệch khoảng ±10% so với bản cũ: mày đừng so trực tiếp.',
    'Kết luận: tao sai.',
    'Điều quan trọng cần lưu ý là: hệ thống chỉ đồng bộ 15 phút một lần.',
    'Lý do rất đơn giản: hệ thống chạy chậm hơn dự kiến.',
    'Nhóm đã thử ba cách sau:',
    '- Quy ước nhãn, giống ghi chú [a.md](a.md):',
    'Tóm lại: chưa nên phát hành.',
    'Nói cách khác: hệ thống chưa ổn định.',
    'Vậy thì sao: chẳng ai đọc cả.',
    'Lúc 9 giờ sáng: hệ thống báo lỗi.',
    'Tôi đã chạy lại phép đo trên bộ dữ liệu 3: kết quả không đổi.',
    'Sau ba lần thử, nhóm rút ra một bài học: phải đo trên dữ liệu thật.',
]

NOT_LABEL_IN_LISTS = """- Bộ 3: chạy lại
- Giờ, phút: 15
- Xem [mục](a.md): chưa xong
- Lệnh `jev`: chạy prepare
- *Nhãn*: giá trị nghiêng
- Có hai việc cần làm trước:"""


def first_sentence_structures(text):
    doc = {'schema_version': 2, 'transmission_allowed': True,
           'source': {'id': 'n', 'layout': 'markdown', 'text': text + '\n'},
           'defaults': {'profile': 'technical'}, 'context_review': {'reviewed': True, 'unresolved': []}}
    prepared = prepare_document(doc, deadline=time.monotonic() + 30)
    return [(s['text'], [t.get('structure') for t in s['sentences']]) for s in prepared['sections']]


class LabelValueRecognitionTest(unittest.TestCase):
    def test_field_lists_are_recognized(self):
        recognized = 0
        for block in (FIELD_LIST_A, FIELD_LIST_B):
            for text, structures in first_sentence_structures(block):
                with self.subTest(text=text):
                    self.assertEqual(structures[0], 'label_value')
                    recognized += 1
        self.assertGreaterEqual(recognized, 16)

    def test_bold_labels_are_recognized_alone(self):
        for line in BOLD:
            with self.subTest(line=line):
                [(_, structures)] = first_sentence_structures(line)
                self.assertEqual(structures[0], 'label_value')

    def test_prose_lone_lines_and_lead_ins_are_not(self):
        cases = 0
        for line in NOT_LABEL:
            with self.subTest(line=line):
                for _, structures in first_sentence_structures(line):
                    self.assertNotIn('label_value', structures)
                    cases += 1
        for text, structures in first_sentence_structures(NOT_LABEL_IN_LISTS):
            with self.subTest(text=text):
                self.assertNotIn('label_value', structures)
                cases += 1
        self.assertGreaterEqual(cases, 20)

    def test_only_the_first_sentence_is_labelled(self):
        [(_, structures)] = first_sentence_structures('- **Cách chấm:** dùng cùng một giám khảo. Thêm câu.')
        self.assertEqual(structures, ['label_value', None])


if __name__ == '__main__':
    unittest.main()
