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
