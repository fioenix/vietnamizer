import tempfile,unittest,shutil
from pathlib import Path
from unittest.mock import patch
from benchmarks import public_deadline as d
O=Path('artifacts/014-public-ai-benchmark-20261025-v2')
@unittest.skipUnless((O/'manifest.json').exists(), 'Local frozen research raw evidence is not bundled with the source repository')
class DeadlineTest(unittest.TestCase):
 def test_observed_deadline_is_narrowly_eligible(self):
  p=d.old.read(O/'requests/0202/request.json');self.assertTrue(d.eligible(O,'requests/0202/record.json','R007',p));self.assertFalse(d.eligible(O,'requests/0202/record.json','R008',p))
  with tempfile.TemporaryDirectory() as tmp:
   out=Path(tmp);shutil.copytree(O/'requests/0202',out/'requests/0202');(out/'requests/0202/response.body').write_bytes(b'x');self.assertFalse(d.eligible(out,'requests/0202/record.json','R007',p))
 def test_ticket_blocks_unknown_response_resampling(self):
  p=d.old.read(O/'requests/0202/request.json')
  with tempfile.TemporaryDirectory() as tmp:
   out=Path(tmp);shutil.copytree(O/'requests/0202',out/'requests/0202');d.old.save(out/'deadline-attempts'/f'R007-{d.core.digest(p)}.json',{'status':'started'});s=d.Store(out,d.pub.verify(O))
   with patch.object(d.pub.PublicBudget,'send',side_effect=AssertionError('network')):
    with self.assertRaisesRegex(ValueError,'already attempted'):s.retry('R007',p,'unused',15,'requests/0202/record.json')
 def test_valid_cache_does_not_retry(self):
  with patch.object(d.r,'verify',return_value=d.old.read(O/'recovery-manifest.json')):
   s=d.Store(O,d.pub.verify(O));p=d.old.read(O/'requests/0001/request.json')
   with patch.object(d.pub.PublicBudget,'send',side_effect=AssertionError('network')):s.dispatch('R001',p,'unused',15)
   self.assertEqual(s.deadline_retries,[])
if __name__=='__main__':unittest.main()
