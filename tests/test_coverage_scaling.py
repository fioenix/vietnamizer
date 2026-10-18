import json
import time
import tracemalloc
import unittest
from jev.core import prepare
from tests.test_coverage import raw

class ScalingTest(unittest.TestCase):
    def test_large_input_bounded_inventory_and_accounting(self):
        d=raw('Tôi về. '*90000) # 1,080,000 encoded text bytes would exceed input limit; trim below it.
        d['source']['text']='X. '*250000 # 750kB, high sentence count
        tracemalloc.start();start=time.monotonic()
        r=prepare(d);elapsed=time.monotonic()-start
        _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
        self.assertNotEqual(r['status'],'invalid_input')
        self.assertTrue(r['source_accounted'])
        self.assertFalse(r['evaluation_complete'])
        self.assertTrue(r['unresolved'])
        self.assertTrue(r['counts']['provisional'])
        self.assertLess(peak,128*1024*1024)
        self.assertLess(elapsed,2.0)
        print(f'preparation scaling: elapsed={elapsed:.3f}s traced_peak={peak} bytes')

    def test_oversize_parent_does_not_duplicate_for_all_candidates(self):
        from tests.test_coverage import EvaluationCase
        from jev.core import evaluate
        d=raw('a'*100000+'.')
        d['candidates']=[{'id':f'e{i}','start':i,'end':i+1,'replacement':'b'} for i in range(400)]
        tracemalloc.start()
        r=evaluate(d,environ={'TYPESAFE_API_KEY':'fake'},transport=lambda *_:self.fail('oversize state sent'))
        _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
        self.assertEqual(r['status'],'incomplete')
        self.assertTrue(r['missing'])
        self.assertLess(peak,16*1024*1024)

    def test_full_input_bound_preparation_rss(self):
        import subprocess,sys
        script="""import json,resource,sys,time
from jev.core import prepare
from tests.test_coverage import raw
before=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
start=time.monotonic();r=prepare(raw('X. '*340000))
after=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
factor=1 if sys.platform=='darwin' else 1024
print(json.dumps({'elapsed':time.monotonic()-start,'incremental_rss':max(0,after-before)*factor,'accounted':r['source_accounted'],'provisional':r['counts']['provisional']}))
"""
        p=subprocess.run([sys.executable,'-B','-c',script],capture_output=True,text=True,timeout=6,check=True)
        metrics=json.loads(p.stdout)
        self.assertTrue(metrics['accounted']);self.assertTrue(metrics['provisional'])
        self.assertLess(metrics['elapsed'],2)
        self.assertLess(metrics['incremental_rss'],128*1024*1024)
        print('1.02MB preparation:',metrics)
