"""Label–value lines are recognized from explicit structure and position.

Feature 011 (SC-003): bold labels, and plain labels inside a field list of at least two adjacent label
items. Feature 012: a plain-label sentence that stands alone on its lines (Q1: A). The owner reviewed
the lines on 2026-10-23 (`calibration/LOG.md`); a colon sentence that shares a line with another
sentence stays prose.
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

# Feature 012: standalone plain-label lines from the owner-rated set. The last four are lead-ins the
# owner rates as wrong; standing alone they still have the form of a listing (LOG, difference 2).
STANDALONE = [
    'Trạng thái: đang xử lý',
    '- Người phụ trách: chị Lan',
    '- Ghi chú: chưa tính phí.',
    'Kết luận: tao sai.',
    'Tóm lại: chưa nên phát hành.',
    'Nói cách khác: hệ thống chưa ổn định.',
    'Vậy thì sao: chẳng ai đọc cả.',
    'Lý do rất đơn giản: hệ thống chạy chậm hơn dự kiến.',
]

# Rejected by form even when they stand alone: digits or punctuation in the label, a lead-in ending
# in `là`, no value after the colon.
NOT_LABEL = [
    'Kết quả lệch khoảng ±10% so với bản cũ: mày đừng so trực tiếp.',
    'Điều quan trọng cần lưu ý là: hệ thống chỉ đồng bộ 15 phút một lần.',
    'Nhóm đã thử ba cách sau:',
    '- Quy ước nhãn, giống ghi chú [a.md](a.md):',
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


def prepared_sections(text):
    doc = {'schema_version': 2, 'transmission_allowed': True,
           'source': {'id': 'n', 'layout': 'markdown', 'text': text + '\n'},
           'defaults': {'profile': 'technical'}, 'context_review': {'reviewed': True, 'unresolved': []}}
    return prepare_document(doc, deadline=time.monotonic() + 30)['sections']


def first_sentence_structures(text):
    return [(s['text'], [t.get('structure') for t in s['sentences']]) for s in prepared_sections(text)]


def sentence_structures(text):
    return [(s['text'][t['start']:t['end']], t.get('structure'))
            for s in prepared_sections(text) for t in s['sentences']]


def body(line):
    return line[2:] if line.startswith('- ') else line


def sentence(line):
    line = body(line)
    return line if line.endswith('.') else line + '.'


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
        self.assertGreaterEqual(cases, 13)

    def test_owner_rated_lines_standing_alone_are_labels(self):
        for line in STANDALONE:
            for text in (line, '- ' + body(line), 'Đoạn trước.\n\n' + line + '\n\nĐoạn sau.'):
                with self.subTest(text=text):
                    self.assertIn((text.split('\n\n')[1] if '\n\n' in text else text, 'label_value'),
                                  [(x, y) for x, y in sentence_structures(text)])

    def test_label_lines_separated_by_single_line_breaks(self):
        self.assertEqual(sentence_structures('Ngày: 22/10/2026.\nTrạng thái: xong.'),
                         [('Ngày: 22/10/2026.', 'label_value'), ('Trạng thái: xong.', 'label_value')])
        [(_, structure)] = sentence_structures('Ngày: 22/10/2026\nTrạng thái: xong')
        self.assertEqual(structure, 'label_value')
        self.assertEqual([y for _, y in sentence_structures('Tao về rồi.\nKết luận: tao sai.')],
                         [None, 'label_value'])
        self.assertEqual([y for _, y in sentence_structures('- Ngày: 22/10/2026.\n  Trạng thái: xong.')],
                         ['label_value', 'label_value'])

    def test_colon_sentence_sharing_a_line_stays_prose(self):
        cases = 0
        for line in STANDALONE:
            for text in ('Tao chạy lại phép đo. ' + sentence(line), sentence(line) + ' Còn lại để sau.',
                         '- ' + sentence(line) + ' Còn lại để sau.',
                         '- Tao chạy lại phép đo. ' + sentence(line)):
                with self.subTest(text=text):
                    self.assertNotIn('label_value', [y for _, y in sentence_structures(text)])
                    cases += 1
        self.assertEqual(cases, 32)

    def test_hard_wrapped_and_quoted_lines_stay_prose(self):
        for text in ('Tao chạy lại phép đo trên bộ dữ liệu cũ. Kết luận: tao\nsai.',
                     '> Ghi chú: trích dẫn.\n> Kết luận: tao sai.'):
            with self.subTest(text=text):
                self.assertNotIn('label_value', [y for _, y in sentence_structures(text)])

    def test_standalone_bold_label_after_the_first_line(self):
        # Feature 012 review: a bold label must not lose to the same label written plain.
        self.assertEqual([y for _, y in sentence_structures('Ngày: hôm nay.\n**Trạng thái:** xong.\nGhi chú: không.')],
                         ['label_value'] * 3)
        self.assertEqual([y for _, y in sentence_structures('- Ngày: x.\n  **Trạng thái:** xong.')],
                         ['label_value'] * 2)
        self.assertEqual([y for _, y in sentence_structures('Tao về.\n**Cần lưu ý rằng:** số liệu lệch.')],
                         [None, None])

    def test_only_the_first_sentence_is_labelled(self):
        [(_, structures)] = first_sentence_structures('- **Cách chấm:** dùng cùng một giám khảo. Thêm câu.')
        self.assertEqual(structures, ['label_value', None])


if __name__ == '__main__':
    unittest.main()
