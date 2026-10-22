"""RED baseline for feature 009, recorded before any runtime change (synthetic text only).

Run from the repository root:
  PYTHONPATH=. python3 -B -m unittest discover -s specs/009-long-document-preparation/baseline -p 'test_red_baseline.py' -t specs/009-long-document-preparation/baseline -v

All four tests fail on v0.10.6 / jev-1.14.0. Implementation tasks move each case into
`tests/` before changing `jev/`. This file is evidence, not part of the shipped suite.
"""
import unittest

from jev import core


def markdown(text, profile='technical'):
    return {'schema_version':2,'transmission_allowed':True,
            'source':{'id':'note','layout':'markdown','text':text},
            'defaults':{'profile':profile},
            'context_review':{'reviewed':True,'unresolved':[]}}


SECTION = (
    '## Mục {n}. Đo độ trễ của bộ nhớ\n\n'
    'Tao chạy lại phép đo trên bộ dữ liệu {n}, với p50/p95 lấy từ 1.000 lượt gọi. '
    'Kết quả lệch khoảng ±10% so với bản v0.4.19 nên mày đừng so trực tiếp. '
    'Recall@k chỉ có ý nghĩa khi cùng một giám khảo chấm.\n\n'
    '- Bộ dữ liệu: 91,4% câu hỏi có đáp án rõ.\n'
    '- Cách chấm: dùng cùng một giám khảo cho mọi hệ thống.\n'
    '- Ghi chú: xem [ghi chú gốc](https://example.com/ghi-chu-{n}).\n\n'
    '1. Chạy bản cũ trước rồi ghi lại số liệu.\n'
    '2. Chạy bản mới với cùng cấu hình.\n\n'
)


def long_note(sections=50):
    return '# Kế hoạch đo thử\n\n' + ''.join(SECTION.format(n=n) for n in range(1, sections+1))


class RedBaseline(unittest.TestCase):
    def test_long_markdown_crosses_scan_budget_without_preparation_limit(self):
        # ~50 sections, ~5,000 tokens, ~23.6k code points: an ordinary long technical note.
        text = long_note()
        self.assertGreater(len(text), 20000)
        r = core.prepare(markdown(text))
        self.assertNotIn('preparation_limit', {u['reason'] for u in r['unresolved']})
        self.assertEqual(r['status'], 'prepared')

    def test_many_short_units_do_not_exhaust_metadata_budget(self):
        # ~480 units (~6k code points) of headings, prose and nested bullets: today zero units
        # and one unprocessed span covering the whole source.
        text = '# Tiêu đề\n\n' + ''.join(
            f'## Mục {n}\n\nĐoạn {n} ngắn.\n\n- Ý {n}: một.\n  - Ý con.\n\n' for n in range(120))
        self.assertLess(len(text), 7000)
        r = core.prepare(markdown(text))
        self.assertGreater(len(r['units']), 0)
        self.assertNotIn('preparation_limit', {u['reason'] for u in r['unresolved']})

    def test_bullet_with_relative_link_and_trailing_colon_is_exact(self):
        text = ('- Quy ước đặt tên, giống ghi chú [so-sanh-ban-cu.md](so-sanh-ban-cu.md):\n'
                '  - Nhãn thứ nhất dùng cho bản cũ.\n')
        r = core.prepare(markdown(text))
        self.assertEqual(r['unresolved'], [])
        self.assertEqual(r['status'], 'prepared')

    def test_quoted_question_followed_by_comma_is_not_a_boundary(self):
        text = '- **thời gian**: "tuần trước ai đổi lịch họp?", có đích là bản ghi mới nhất.\n'
        r = core.prepare(markdown(text))
        self.assertEqual(r['unresolved'], [])
        self.assertEqual(r['counts']['sentences'], 1)


if __name__ == '__main__':
    unittest.main()
