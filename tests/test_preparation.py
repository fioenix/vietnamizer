import json
from pathlib import Path
import unittest
from jev.preparation import prepare_document

class CorpusTests(unittest.TestCase):
    def test_independently_annotated_cases(self):
        corpus=json.loads(Path('tests/fixtures/segmentation/cases.json').read_text())
        for case in corpus['cases']:
            with self.subTest(case=case['id']):
                doc={'schema_version':2,'source':{'id':'article','layout':case['layout'],'text':case['text']},'defaults':{'profile':'blog'},'annotations':[{'start':a,'end':b,'protected':True} for a,b in case.get('protected_spans',[])],'boundary_overrides':case.get('boundary_overrides',[])}
                got=prepare_document(doc)
                exact=[[s['source_start']+t['start'],s['source_start']+t['end']] for s in got['sections'] for t in s['sentences'] if t['boundary_status']=='exact']
                self.assertEqual(case['sentences'],exact)
                self.assertEqual(case['unresolved'],not got['segmentation_complete'])
                self.assertEqual(case['text'],''.join(case['text'][p['start']:p['end']] for p in got['partition']))
                parents=[[s['source_start'],s['source_end']] for s in got['sections'] if s['kind'] in ('prose','list')]
                self.assertEqual(case['parents'],parents)


def segments(text, layout='markdown'):
    got=prepare_document({'schema_version':2,'source':{'id':'article','layout':layout,'text':text},'defaults':{'profile':'technical'}})
    exact=[text[s['source_start']+t['start']:s['source_start']+t['end']] for s in got['sections'] for t in s['sentences'] if t['boundary_status']=='exact']
    return exact,sorted({u['reason'] for u in got['unresolved']})


class SegmentationDeltaTests(unittest.TestCase):
    """Reference cases of specs/009-long-document-preparation/contracts/segmentation-delta.md."""
    def test_rows_that_stay_whole(self):
        cases={
            '- Quy ước đặt tên, giống ghi chú [so-sanh-ban-cu.md](so-sanh-ban-cu.md):\n  - Nhãn thứ nhất dùng cho bản cũ.\n':
                ['- Quy ước đặt tên, giống ghi chú [so-sanh-ban-cu.md](so-sanh-ban-cu.md):','- Nhãn thứ nhất dùng cho bản cũ.'],
            '- **thời gian**: "tuần trước ai đổi lịch họp?", có đích là bản ghi mới nhất.\n':
                ['- **thời gian**: "tuần trước ai đổi lịch họp?", có đích là bản ghi mới nhất.'],
            '- [Đố vui!, bản 2025](https://example.org/x): bài về RAG.\n':['- [Đố vui!, bản 2025](https://example.org/x): bài về RAG.'],
            'Xem [A](Ghi.Chu.md) rồi báo tôi.\n':['Xem [A](Ghi.Chu.md) rồi báo tôi.'],
            'Xem [b](../a/b.md) rồi báo tôi.\n':['Xem [b](../a/b.md) rồi báo tôi.'],
            'Anh hỏi "ai không muốn họp?". Tôi im.\n':['Anh hỏi "ai không muốn họp?".','Tôi im.'],
            'Mở README.md rồi chạy jev.core nhé.\n':['Mở README.md rồi chạy jev.core nhé.'],
            'Xem example.dev. Tôi về.\n':['Xem example.dev.','Tôi về.'],
        }
        for text,expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual((expected,[]),segments(text))

    def test_missing_separator_stays_unresolved_with_its_own_reason(self):
        for text,layout in (('Tôi về.bạn ở lại.\n','markdown'),('Done.Next step.\n','markdown'),('Tôi về.Bạn ở lại.','paragraph-lines')):
            with self.subTest(text=text):
                self.assertEqual(([],['ambiguous_separator']),segments(text,layout))

    def test_single_letter_dotted_abbreviation_stays_ambiguous(self):
        # Like v.v. and v.d., e.g./i.e. before an uppercase word may or may not end the sentence.
        for text in ('Dùng e.g. Python rồi chạy.\n','Nghĩa là i.e. Tôi về.\n'):
            with self.subTest(text=text):
                self.assertEqual(([],['ambiguous_abbreviation']),segments(text))

    def test_parenthesis_inside_destination_keeps_url_closer_rule(self):
        self.assertEqual(([],['ambiguous_url_closer']),segments('Xem [a](b(c).md) nhé.\n'))
