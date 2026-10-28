import tempfile,unittest,shutil
from pathlib import Path
from unittest.mock import patch
from benchmarks import public_abstention as a
O=Path('artifacts/014-public-ai-benchmark-20261025-v2')
@unittest.skipUnless((O/'manifest.json').exists(), 'Local frozen research raw evidence is not bundled with the source repository')
class AbstentionTest(unittest.TestCase):
 def fixture(self,out):
  for n in ('0404','0405'):shutil.copytree(O/'requests'/n,out/'requests'/n)
  for p in (O/'repair-attempts').glob('R013-0404.json'):a.old.save(out/'repair-attempts'/p.name,a.old.read(p))
  a.old.save(out/'abstention-manifest.json',{'policy':'fixture'})
  return a.old.read(O/'evaluations/R013/recovered.json')
 def test_exhausted_repair_is_unknown_not_semantic_success(self):
  with tempfile.TemporaryDirectory() as tmp:
   out=Path(tmp);r=self.fixture(out);c=a.certificate(out,'R013',r);self.assertEqual(c['status'],'service_partial');self.assertEqual(len(c['invalid_question_ids']),1);self.assertEqual(c['omitted_question_ids'],r['receipts'][-1]['question_ids']);self.assertNotIn('answers',c)
 def test_no_calls_after_terminal_abstention(self):
  with tempfile.TemporaryDirectory() as tmp:
   out=Path(tmp);r=self.fixture(out);a.old.save(out/'requests/0406/record.json',{'case':'R013','request_digest':'other'})
   with self.assertRaisesRegex(ValueError,'continued after'):a.certificate(out,'R013',r)
 def test_transport_failure_not_accepted(self):
  with tempfile.TemporaryDirectory() as tmp:
   out=Path(tmp);r=self.fixture(out);p=out/'requests/0405/record.json';v=a.old.read(p);v['status']='transport_failed';a.old.save(p,v)
   with self.assertRaisesRegex(ValueError,'eligible schema'):a.certificate(out,'R013',r)
 def test_completed_scope_cannot_be_certified_as_partial(self):
  with tempfile.TemporaryDirectory() as tmp:
   out=Path(tmp);r=self.fixture(out);r['scope_complete']=True
   with self.assertRaisesRegex(ValueError,'terminal partial'):a.certificate(out,'R013',r)
if __name__=='__main__':unittest.main()
