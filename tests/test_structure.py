import time
import unittest
from jev.preparation import prepare_document

def raw(text,**extra):
    return dict({'schema_version':2,'source':{'id':'doc','layout':'markdown','text':text},'defaults':{'profile':'blog'}},**extra)

class StructureTests(unittest.TestCase):
    def test_more_than_legacy_limits(self):
        got=prepare_document(raw('\n\n'.join('Tôi về.' for _ in range(40))))
        self.assertEqual(40,len(got['sections']))
        many=prepare_document(raw(' '.join('Tôi về.' for _ in range(40))))
        self.assertEqual(40,len(many['sections'][0]['sentences']))
    def test_explicit_parent_preserves_newlines(self):
        text='Tôi về.\nBạn ở lại.'
        doc=raw(text,annotations=[{'start':0,'end':len(text),'paragraph':True}])
        doc['source']['layout']='paragraph-lines'
        got=prepare_document(doc)
        self.assertEqual(text,got['sections'][0]['text'])
        self.assertEqual(2,len(got['sections'][0]['sentences']))
    def test_deadline_never_claims_complete(self):
        got=prepare_document(raw('Tôi về. Bạn ở.'),deadline=time.monotonic()-1)
        self.assertFalse(got['segmentation_complete'])
        self.assertEqual('preparation_deadline',got['unresolved'][0]['reason'])
        self.assertTrue(got['source_accounted'])
    def test_large_source_has_explicit_local_limit(self):
        got=prepare_document(raw('\n\n'.join('Tôi về.' for _ in range(5000))))
        self.assertFalse(got['segmentation_complete'])
        self.assertLessEqual(len(got['sections']),4096)
        self.assertTrue(got['source_accounted'])
    def test_unknown_html_ambiguous(self):
        got=prepare_document(raw('<div>\nTôi về.\n</div>'))
        self.assertFalse(got['segmentation_complete'])
    def test_shared_inventory_budget(self):
        doc=raw('\n\n'.join(' '.join('Đi.' for _ in range(100)) for _ in range(60)))
        got=prepare_document(doc)
        self.assertFalse(got['segmentation_complete'])
        self.assertLessEqual(len(got['sections'])+sum(len(s['sentences']) for s in got['sections']),4096)
    def test_inventory_cap_keeps_prefix_and_reports_remainder(self):
        from unittest.mock import patch
        text='\n\n'.join(' '.join('Đi.' for _ in range(100)) for _ in range(50))
        # Ample work, so only the inventory cap can stop preparation.
        with patch('jev.preparation.WORK_LIMIT',2**20):
            got=prepare_document(raw(text))
        sentences=[t for s in got['sections'] for t in s['sentences']]
        self.assertLessEqual(len(got['sections'])+len(sentences),4096)
        self.assertTrue(any(t['boundary_status']=='exact' for t in sentences))
        self.assertIn('preparation_limit',{u['reason'] for u in got['unresolved']})
        self.assertEqual(len(text),max(u['end'] for u in got['unresolved']))
    def test_whole_unit_ambiguity_spans_count_toward_inventory_cap(self):
        from unittest.mock import patch
        # Each unit returns one whole-unit unresolved span (unmatched quote), not a scanned sentence.
        text='\n\n'.join(['Một "câu hỏi?']*3000)
        with patch('jev.preparation.WORK_LIMIT',2**20):
            got=prepare_document(raw(text))
        sentences=[t for s in got['sections'] for t in s['sentences']]
        self.assertLessEqual(len(got['sections'])+len(sentences),4096)
        self.assertIn('preparation_limit',{u['reason'] for u in got['unresolved']})
        self.assertEqual(len(text),max(u['end'] for u in got['unresolved']))
    def test_open_fence_is_unresolved(self):
        got=prepare_document(raw('```py\nSECRET = 1'))
        self.assertFalse(got['segmentation_complete'])
    def test_pathological_initial_chain_is_bounded(self):
        before=time.monotonic()
        got=prepare_document(raw('X. '*250000),deadline=before+2)
        self.assertLess(time.monotonic()-before,3)
        self.assertFalse(got['segmentation_complete'])
    def test_huge_tokens_have_linear_marker_dispatch(self):
        import json
        import subprocess
        import sys
        child='''import json,sys,time,tracemalloc
from jev.preparation import prepare_document
doc=json.load(sys.stdin)
tracemalloc.start(); start=time.monotonic()
r=prepare_document(doc)
elapsed=time.monotonic()-start
_,peak=tracemalloc.get_traced_memory()
print(json.dumps({'elapsed':elapsed,'peak':peak,'accounted':r['source_accounted']}))
'''
        for text in ['a'*49000,'7'*49000,'X. '*250000]:
            with self.subTest(prefix=text[:5]):
                result=subprocess.run([sys.executable,'-B','-c',child],input=json.dumps(raw(text)),text=True,capture_output=True,timeout=4,check=True)
                measured=json.loads(result.stdout)
                self.assertTrue(measured['accounted'])
                self.assertLess(measured['elapsed'],2)
                self.assertLess(measured['peak'],128*1024*1024)
    def test_many_overrides_validate_quickly(self):
        import json
        import subprocess
        import sys
        # Wall time without tracemalloc: this guards work per override, not allocation.
        child='''import json,sys,time
from jev.preparation import prepare_document
doc=json.load(sys.stdin)
start=time.monotonic()
r=prepare_document(doc)
print(json.dumps({'elapsed':time.monotonic()-start,'accounted':r['source_accounted']}))
'''
        run='x'*20002+'.'
        # Many lexical spans and overrides in one parent; then many parents (and so many sentences)
        # before the overrides, which must not multiply work per sentence.
        for head in ('1.5 '*8000,'1.5\n\n'*1000,'1.5\n\n'*3000):
            text=head+run
            doc=raw(text,boundary_overrides=[len(head)+1+i for i in range(20000)])
            with self.subTest(parents=head.count('\n\n')+1):
                result=subprocess.run([sys.executable,'-B','-c',child],input=json.dumps(doc),text=True,capture_output=True,timeout=10,check=True)
                measured=json.loads(result.stdout)
                self.assertTrue(measured['accounted'])
                self.assertLess(measured['elapsed'],2)
    def test_dotted_identifier_tokens_stay_linear(self):
        import json
        import subprocess
        import sys
        child='''import json,sys,time,tracemalloc
from jev.preparation import prepare_document
doc=json.load(sys.stdin)
tracemalloc.start(); start=time.monotonic()
r=prepare_document(doc)
elapsed=time.monotonic()-start
_,peak=tracemalloc.get_traced_memory()
print(json.dumps({'elapsed':elapsed,'peak':peak,'accounted':r['source_accounted']}))
'''
        # A failed identifier match must not retry every suffix of a giant token.
        for text in ['a'*500000+'.b'+'é','ab.'*200000+'abé']:
            with self.subTest(prefix=text[:5],length=len(text)):
                result=subprocess.run([sys.executable,'-B','-c',child],input=json.dumps(raw(text)),text=True,capture_output=True,timeout=4,check=True)
                measured=json.loads(result.stdout)
                self.assertTrue(measured['accounted'])
                self.assertLess(measured['elapsed'],2)
                self.assertLess(measured['peak'],128*1024*1024)
