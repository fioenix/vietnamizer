import tempfile,unittest,shutil
from pathlib import Path
from benchmarks import public_availability as a
O=Path('artifacts/014-public-ai-benchmark-20261025-v2')
@unittest.skipUnless((O/'manifest.json').exists(),'Local raw research evidence is not bundled')
class AvailabilityTest(unittest.TestCase):
 def fixture(self,out):
  for n in ('0546','0547'):shutil.copytree(O/'requests'/n,out/'requests'/n)
  a.old.save(out/'deadline-manifest.json',a.old.read(O/'deadline-manifest.json'));a.old.save(out/'availability-manifest.json',{'policy':'fixture'})
  for p in (O/'deadline-attempts').glob('R019-*'):a.old.save(out/'deadline-attempts'/p.name,a.old.read(p))
  return a.old.read(O/'evaluations/R019/recovered.json')
 def test_deadline_pair_is_unavailable_not_semantic_failure(self):
  with tempfile.TemporaryDirectory() as d:
   out=Path(d);r=self.fixture(out);c=a.certificate(out,'R019',r);self.assertEqual(c['unknown_billing_attempts'],2);self.assertEqual(c['invalid_question_ids'],[]);self.assertTrue(all(x<2 for x in c['observed_attempt_elapsed_seconds']))
 def test_third_attempt_is_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   out=Path(d);r=self.fixture(out);a.old.save(out/'requests/0548/record.json',a.old.read(out/'requests/0547/record.json'))
   with self.assertRaisesRegex(ValueError,'exactly two'):a.certificate(out,'R019',r)
 def test_erased_reservation_is_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   out=Path(d);r=self.fixture(out);p=out/'requests/0547/record.json';rec=a.old.read(p);rec['reserve_usd']='0';a.old.save(p,rec)
   with self.assertRaisesRegex(ValueError,'reservations'):a.certificate(out,'R019',r)
if __name__=='__main__':unittest.main()
