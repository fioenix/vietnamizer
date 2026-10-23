"""Feature 011: per-group subjects, the T4 sign gate and structure exclusions."""
import collections
import hashlib
import time
import unittest
import unicodedata

from jev.core import MODEL, _eligible_sentences, _protect_identifiers, editable_text, evaluate, load_registry, prepare
from jev.coverage import Ledger, expand_records
from jev.preparation import prepare_document
from tests.test_jev import response
from tests.test_preparation_limits import SECTION, markdown


def note(sections=10):
    return markdown(''.join(SECTION.format(n=i) for i in range(sections)))


def ledger(doc):
    prepared = prepare_document(doc, deadline=time.monotonic() + 60)
    for s in prepared['sections']:
        s['editable'] = bool(editable_text(s).strip())
    _eligible_sentences(prepared); _protect_identifiers(prepared)
    return prepared, Ledger(prepared, load_registry(), MODEL)


def run(doc):
    sent = []
    def fake(payload, *_):
        sent.append(payload)
        return response(payload)
    return evaluate(doc, environ={'TYPESAFE_API_KEY': 'fake'}, transport=fake), sent


def asked(report, section_id):
    """Patterns asked about a unit, and the excluded subjects each coverage entry records."""
    patterns = {j['coverage_key'] for j in report['judgments'] if j['section'] == section_id}
    excluded = {e['pattern']: e.get('excluded_subjects', []) for e in expand_records(report['coverage'])
                if e['section'] == section_id}
    return patterns, excluded


class PerGroupSubjectGuard(unittest.TestCase):
    """Pinned check order and counts for the ~1,000-word note.

    T002 pinned 86/222 checks, 7,381 required and 68 per sentence before per-group subjects (T003
    kept them). The T4 gate (T007) removes T4 from every subject without `, và`: 84/216, 7,201, 66.
    Heading exclusions (T013) remove V2, V3, V5 and V14 from heading units: 76/216, 7,121.
    V11 (T019) leaves headings and field-list label items: 73/216, 7,001.
    """
    def test_required_counts_and_check_order(self):
        prepared, led = ledger(note())
        secs = prepared['sections']
        def digest(keys):
            return hashlib.sha256(repr(keys).encode()).hexdigest()[:16]
        heading = list(led.checks(secs[0]['id'])); prose = list(led.checks(secs[1]['id']))
        self.assertEqual((len(heading), len(prose)), (73, 216))
        self.assertEqual((digest(heading), digest(prose)), (GUARD_HEADING, GUARD_PROSE))
        report = prepare(note())
        self.assertEqual(report['counts']['required'], 7001)
        self.assertEqual(collections.Counter(s['required'] for s in report['sentences']), {66: 50, 63: 30})


class SignGateTest(unittest.TestCase):
    """User Story 1: T4 is asked only where its canonical sign `,\\s+và\\s` occurs in editable text."""
    def t4_by_sentence(self, text):
        report, _ = run(markdown(text))
        entries = [e for e in expand_records(report['coverage']) if e['pattern'] == 'T4']
        asked_ids = {j['check'].split('_')[1] + '_' + j['check'].split('_')[2]
                     for j in report['judgments'] if j['coverage_key'] == 'T4'}
        return report, entries, asked_ids

    def test_sentence_without_sign_gets_no_t4(self):
        report, entries, _ = self.t4_by_sentence('Tôi về nhà sớm. Bạn ở lại làm tiếp.\n')
        self.assertFalse([j for j in report['judgments'] if j['coverage_key'] == 'T4'])
        self.assertEqual(entries[0]['status'], 'excluded')
        self.assertEqual(entries[0]['reason'], 'sign_absent')
        self.assertEqual({x['reason'] for x in entries[0]['excluded_subjects']}, {'sign_absent'})
        self.assertEqual(len(entries[0]['excluded_subjects']), 2)

    def test_sentence_with_sign_still_gets_t4(self):
        report, entries, _ = self.t4_by_sentence('Nhóm kiểm tra dữ liệu, và gửi báo cáo. Tôi về.\n')
        t4 = [j for j in report['judgments'] if j['coverage_key'] == 'T4']
        self.assertEqual(len(t4), 2)
        self.assertEqual([x['reason'] for x in entries[0]['excluded_subjects']], ['sign_absent'])

    def test_whitespace_forms(self):
        report, _, _ = self.t4_by_sentence('Tôi về,và bạn ở lại.\n')
        self.assertFalse([j for j in report['judgments'] if j['coverage_key'] == 'T4'], '`,và` has no whitespace')
        report, _, _ = self.t4_by_sentence('Tôi về,\nvà bạn ở lại.\n')
        self.assertTrue([j for j in report['judgments'] if j['coverage_key'] == 'T4'], 'a line break is whitespace')

    def test_decomposed_va_still_opens_t4(self):
        text = unicodedata.normalize('NFD', 'Nhóm kiểm tra dữ liệu, và gửi báo cáo.\n')
        report, _, _ = self.t4_by_sentence(text)
        self.assertTrue([j for j in report['judgments'] if j['coverage_key'] == 'T4'])

    def test_sign_inside_inline_code_does_not_open_t4(self):
        report, _, _ = self.t4_by_sentence('Chạy lệnh `a, và b` rồi về.\n')
        self.assertFalse([j for j in report['judgments'] if j['coverage_key'] == 'T4'])

    def test_heading_and_label_item_get_no_t4(self):
        text = '# Kế hoạch đo hiệu năng\n\n- Ngày: 22/10/2026 (Asia/Ho_Chi_Minh)\n- Người viết: Fio\n'
        report, _ = run(markdown(text))
        self.assertFalse([j for j in report['judgments'] if j['coverage_key'] == 'T4'])

    def test_excluded_subjects_are_not_required(self):
        with_sign, _ = run(markdown('Nhóm kiểm tra dữ liệu, và gửi báo cáo.\n'))
        without, _ = run(markdown('Nhóm kiểm tra dữ liệu và gửi báo cáo.\n'))
        self.assertEqual(with_sign['counts']['required'] - without['counts']['required'], 2)


class StructureExclusionTest(unittest.TestCase):
    """User Story 2: patterns skip structures their own **Không flag** excludes as a whole."""
    TEXT = ('## Kế hoạch đo hiệu năng\n\n- Ngày: 22/10/2026 (Asia/Ho_Chi_Minh)\n- Người viết: Fio\n\n'
            'Tao chạy lại phép đo trên bộ dữ liệu mới.\n')

    def units(self, text):
        return prepare(markdown(text))['units']

    def test_heading_skips_v2_v3_v5_v14(self):
        report, _ = run(markdown(self.TEXT))
        heading = self.units(self.TEXT)[0]['id']
        patterns, excluded = asked(report, heading)
        self.assertFalse({'V2', 'V3', 'V5', 'V14'} & patterns)
        for pid in ('V2', 'V3', 'V5', 'V14'):
            self.assertEqual(excluded[pid], [{'subject': 'unit', 'reason': 'structure_excluded', 'structure': 'heading'}])
        self.assertTrue({'T1', 'T5', 'T6', 'K3', 'V6', 'V20'} <= patterns)

    def test_heading_by_host_annotation(self):
        text = 'Kế hoạch đo hiệu năng\n\nTao chạy lại phép đo.\n'
        doc = markdown(text, annotations=[{'start': 0, 'end': len('Kế hoạch đo hiệu năng'), 'kind': 'heading'}])
        report, _ = run(doc)
        patterns, _ = asked(report, self.units(text)[0]['id'])
        self.assertFalse({'V2', 'V3', 'V5', 'V14'} & patterns)
        self.assertIn('T1', patterns)

    def test_label_item_loses_only_v11(self):
        # Before User Story 3 a label item lost nothing; V11's Không flag now names label–value lines.
        report, _ = run(markdown(self.TEXT))
        patterns, _ = asked(report, self.units(self.TEXT)[1]['id'])
        self.assertNotIn('V11', patterns)
        self.assertTrue({'T5', 'V3', 'V14'} <= patterns)

    def test_candidate_on_excluded_subject_is_still_reviewed(self):
        heading = self.units(self.TEXT)[0]
        doc = markdown(self.TEXT, candidates=[{'id': 'e1', 'start': heading['start'] + 3,
                                               'end': heading['start'] + 11, 'replacement': 'Lịch đo'}])
        report, _ = run(doc)
        patterns, _ = asked(report, heading['id'])
        self.assertIn('edit_e1', patterns)
        self.assertFalse({'V2', 'V3', 'V5', 'V14'} & patterns)

    def test_typography_only_keeps_genre_gate(self):
        text = '| Cột | Giá trị |\n|---|---|\n| Tôi | về |\n\nTao chạy lại phép đo.\n'
        report, _ = run(markdown(text))
        table = self.units(text)[0]['id']
        reasons = {e['pattern']: e.get('reason') for e in expand_records(report['coverage']) if e['section'] == table}
        self.assertEqual(reasons['V14'], 'genre_gate')


class V11RuleTest(unittest.TestCase):
    """User Story 3: V11 skips titles and label–value lines once its Không flag names them (Q1: B)."""
    TEXT = ('# Kế hoạch đo hiệu năng\n\n- Ngày: 22/10/2026 (Asia/Ho_Chi_Minh)\n- Người viết: Fio\n\n'
            'Ngày: 22/10/2026\n\nĐiều quan trọng cần lưu ý là hệ thống chỉ đồng bộ 15 phút một lần.\n')

    def test_v11_skips_title_and_field_list_but_not_prose(self):
        report, _ = run(markdown(self.TEXT))
        units = prepare(markdown(self.TEXT))['units']
        title, date_item, lone_date, prose = units[0]['id'], units[1]['id'], units[3]['id'], units[4]['id']
        for unit in (title, date_item):
            patterns, excluded = asked(report, unit)
            self.assertNotIn('V11', patterns)
            self.assertEqual([x['reason'] for x in excluded['V11']], ['structure_excluded'])
        patterns, excluded = asked(report, lone_date)
        self.assertNotIn('V11', patterns, 'a plain label line standing alone is a label (feature 012, Q1: A)')
        self.assertEqual([x['reason'] for x in excluded['V11']], ['structure_excluded'])
        self.assertNotIn('T4', patterns)
        self.assertIn('V11', asked(report, prose)[0])


class ReviewFixTest(unittest.TestCase):
    """Feature 011 independent review (T022): verified findings, each RED before its fix."""
    def test_missing_records_use_section_sentence_indexes(self):
        from unittest.mock import patch
        doc = markdown('Tao về. Mày ở lại. Tao mua táo, cam, và lê.\n')
        with patch('jev.core.MAX_REQUESTS', 1), patch('jev.core.MAX_QUESTIONS', 1):
            report = evaluate(doc, environ={'TYPESAFE_API_KEY': 'fake'}, transport=lambda p, *_: response(p),
                              only_pattern='T4')
        [record] = [m for m in expand_records(report['missing']) if m['pattern'] == 'T4']
        self.assertEqual(record['subject_positions'], [2])
        self.assertEqual(record['validated_keys'], [[2, 'violation']])
        keys = {(n, k) for n in record['subject_positions'] for k in record['recipe_keys']}
        self.assertEqual(len(keys - set(map(tuple, record['validated_keys']))), record['missing'])

    def test_v11_sign_inside_a_label_line_is_still_asked(self):
        text = '**Lưu ý:** Điều quan trọng cần lưu ý là hệ thống chỉ đồng bộ 15 phút một lần.\n'
        report, _ = run(markdown(text))
        self.assertIn('V11', {j['coverage_key'] for j in report['judgments']})

    def test_v11_sign_on_a_standalone_plain_label_line_is_still_asked(self):
        # Feature 012 SC-003: the sign override also covers labels recognized by position.
        from tests.test_label_value import sentence_structures
        text = 'Lưu ý: Điều này có nghĩa là số liệu có thể lệch.'
        self.assertEqual(sentence_structures(text), [(text, 'label_value')])
        report, _ = run(markdown(text + '\n'))
        self.assertIn('V11', {j['coverage_key'] for j in report['judgments']})

    def test_every_canonical_v11_sign_keeps_v11_on_a_label_line(self):
        # PR #21 review: the priority signals are a subset; exclusion must use V11's full sign list.
        for value in ('Điều này có nghĩa là số liệu có thể lệch.',
                      'việc kiểm tra lại toàn bộ dữ liệu là điều cần thiết.'):
            with self.subTest(value=value):
                report, _ = run(markdown('**Lưu ý:** ' + value + '\n'))
                self.assertIn('V11', {j['coverage_key'] for j in report['judgments']})

    def test_lead_in_labels_and_mixed_lists_are_not_field_lists(self):
        from tests.test_label_value import first_sentence_structures
        for block in ('- Cần lưu ý rằng: số liệu có thể lệch\n- Có thể thấy rằng: hiệu năng tăng',
                      '- Câu hỏi đặt ra là: đo lại hay không\n- Kết luận là: chưa',
                      '- **Bước 1, 2.:** làm lại\n- **[Ngày](x):** hôm nay'):
            with self.subTest(block=block[:30]):
                for _, structures in first_sentence_structures(block):
                    self.assertNotIn('label_value', structures)
        # Feature 012: items of different list kinds are not one field list, but each stands alone.
        self.assertEqual([s for _, s in first_sentence_structures('- Ngày: 22/10/2026\n\n1. Bước: chạy lại')],
                         [['label_value'], ['label_value']])


GUARD_HEADING = 'c2d015b56141ee79'
GUARD_PROSE = 'f6da94c0367372ab'


if __name__ == '__main__':
    unittest.main()
