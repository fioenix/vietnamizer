"""Adversarial metadata must share the source-preparation work/deadline bound."""
import json
import subprocess
import sys
import unittest

class MetadataLimitTest(unittest.TestCase):
    def run_repro(self, expired=False):
        script=r'''
import json,time
from jev.core import prepare, evaluate
from jev.preparation import prepare_document
N=19000
text='a\n'*N
ann=[{'start':2*i,'end':2*i+1,'paragraph':True} for i in range(N)]
d={'schema_version':2,'transmission_allowed':True,'source':{'id':'article','layout':'paragraph-lines','text':text},'defaults':{'profile':'blog'},'annotations':ann,'context_review':{'reviewed':True,'unresolved':[]}}
assert len(json.dumps(d,ensure_ascii=False).encode())<1048576
start=time.monotonic()
if EXPIRED:
 p=prepare_document(d,deadline=start-1)
 result={'source_accounted':p['source_accounted'],'segmentation_complete':p['segmentation_complete'],'unresolved':p['unresolved']}
else:
 calls=[]
 result=evaluate(d,environ={'TYPESAFE_API_KEY':'fake'},transport=lambda *args:calls.append(args))
 result={k:result[k] for k in ('source_accounted','segmentation_complete','unresolved','counts','status')}
 result['calls']=len(calls)
result['elapsed']=time.monotonic()-start
print(json.dumps(result))
'''.replace('EXPIRED','True' if expired else 'False')
        p=subprocess.run([sys.executable,'-B','-c',script],capture_output=True,text=True,timeout=3,check=True)
        return json.loads(p.stdout)
    def test_many_explicit_parents_cannot_bypass_work_inventory(self):
        r=self.run_repro()
        self.assertEqual(r['status'],'incomplete')
        self.assertTrue(r['source_accounted'])
        self.assertFalse(r['segmentation_complete'])
        self.assertTrue(r['counts']['provisional'])
        self.assertEqual(r['calls'],0)
        self.assertLess(r['elapsed'],1)
    def test_expired_deadline_applies_before_annotation_overlay(self):
        r=self.run_repro(True)
        self.assertFalse(r['segmentation_complete'])
        self.assertLess(r['elapsed'],1)
        self.assertTrue(any(x['reason']=='preparation_deadline' for x in r['unresolved']))


def markdown(text, profile='technical', **extra):
    return dict({'schema_version':2,'transmission_allowed':True,
                 'source':{'id':'note','layout':'markdown','text':text},
                 'defaults':{'profile':profile},
                 'context_review':{'reviewed':True,'unresolved':[]}}, **extra)


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

# Seven units and six sentences per section. The relative link has no dot: dotted
# file names are feature 009's boundary change, not part of the work bound.
NOTE_SECTION = (
    '## Mục {n}. Đo độ trễ\n\n### Cách đo {n}\n\n'
    'Tao chạy lại phép đo {n}, với p50/p95 lấy từ 1.000 lượt gọi. '
    'Kết quả lệch ±10% so với v0.4.19 nên mày đừng so trực tiếp. '
    'Recall@k đạt 91,4% khi cùng giám khảo chấm.\n\n'
    '- Bộ dữ liệu: xem [ghi chú](ghi-chu-{n}) và [nguồn](https://example.org/{n}).\n'
    '  - Ý con thứ nhất của mục {n}.\n'
    '    - Ý cháu dùng để kiểm tra lồng ba cấp.\n\n'
    '| Hệ thống | Điểm |\n|---|---|\n| A | 91,4% |\n\n'
)


class LongDocumentTest(unittest.TestCase):
    def test_long_markdown_crosses_scan_budget_without_preparation_limit(self):
        from jev.core import prepare
        text='# Kế hoạch đo thử\n\n'+''.join(SECTION.format(n=n) for n in range(1,51))
        self.assertGreater(len(text),20000)
        r=prepare(markdown(text))
        self.assertNotIn('preparation_limit',{u['reason'] for u in r['unresolved']})
        self.assertEqual(r['status'],'prepared')

    def test_many_short_units_do_not_exhaust_metadata_budget(self):
        from jev.core import prepare
        text='# Tiêu đề\n\n'+''.join(f'## Mục {n}\n\nĐoạn {n} ngắn.\n\n- Ý {n}: một.\n  - Ý con.\n\n' for n in range(120))
        self.assertLess(len(text),7000)
        r=prepare(markdown(text))
        self.assertGreater(len(r['units']),0)
        self.assertNotIn('preparation_limit',{u['reason'] for u in r['unresolved']})

    def test_ten_thousand_word_note_is_fully_prepared(self):
        from jev.core import prepare
        sections=121
        text='# Kế hoạch đo thử\n\n'+''.join(NOTE_SECTION.format(n=n) for n in range(1,sections+1))
        fence=len(text); text+='```text\nlệnh chạy\n```\n'
        self.assertGreaterEqual(len(text.split()),10000)
        r=prepare(markdown(text,annotations=[{'start':fence,'end':len(text)-1,'protected':True}]))
        self.assertEqual(r['status'],'prepared')
        self.assertEqual(r['unresolved'],[])
        self.assertEqual(len(r['units']),7*sections+2) # plus title and fence
        self.assertEqual(r['counts']['sentences'],6*sections)
