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


def segments(text, layout='markdown', overrides=None):
    doc={'schema_version':2,'source':{'id':'article','layout':layout,'text':text},'defaults':{'profile':'technical'}}
    if overrides: doc['boundary_overrides']=overrides
    got=prepare_document(doc)
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
            'Mở README.md rồi chạy main.py nhé.\n':['Mở README.md rồi chạy main.py nhé.'],
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
        # The inner dot reports the missing separator first; the final dot must stay ambiguous too,
        # or the following sentence would be certified.
        for text in ('Dùng e.g. Python rồi chạy.\n','Nghĩa là i.e. Tôi về.\n'):
            with self.subTest(text=text):
                self.assertEqual(([],['ambiguous_separator']),segments(text))

    def test_parenthesis_inside_destination_keeps_url_closer_rule(self):
        self.assertEqual(([],['ambiguous_url_closer']),segments('Xem [a](b(c).md) nhé.\n'))

    def test_plain_ascii_words_with_missing_space_stay_unresolved(self):
        # Only allowlisted file extensions and TLDs make a dotted token lexical.
        for text in ('Tôi gặp anh.con mèo chạy.\n','Năm 2025.sau đó tôi về.\n','Mở jev.core nhé.\n'):
            with self.subTest(text=text):
                exact,reasons=segments(text)
                self.assertEqual([],exact)
                self.assertTrue(reasons)

    def test_abbreviations_never_get_a_certified_boundary(self):
        for text in ('Dùng E.g. Python rồi chạy.\n','Gọi I.e. Tôi về.\n','Ví dụ:e.g. Python chạy.\n',"Dùng 'e.g. Python rồi.\n"):
            with self.subTest(text=text):
                exact,reasons=segments(text)
                self.assertFalse([t for t in exact if '.g.' in t or '.e.' in t])
                self.assertTrue(reasons)

    def test_host_override_wins_inside_identifier_and_link_destination(self):
        text='Tôi đọc README.md rồi về.\n'
        self.assertEqual((['Tôi đọc README.','md rồi về.'],[]),segments(text,overrides=[text.index('.')+1]))
        text='Xem [a](b.md) nhé. Tôi về.\n'
        self.assertEqual((['Xem [a](b.','md) nhé.','Tôi về.'],[]),segments(text,overrides=[10]))
