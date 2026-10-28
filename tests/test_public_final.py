import unittest,copy
from pathlib import Path
from unittest.mock import patch
from benchmarks import public_final as f
O=Path('artifacts/014-public-ai-benchmark-20261025-v2')
@unittest.skipUnless((O/'manifest.json').exists(),'Local raw research evidence not bundled')
class FinalTest(unittest.TestCase):
 def test_validated_late_response_is_reusable_without_new_network(self):
  with patch.object(f.r,'verify',return_value=f.old.read(O/'recovery-manifest.json')):
   f.late_proof(O);s=f.r.Store(O,f.pub.verify(O));p=f.old.read(O/'requests/0550/request.json')
   with patch.object(f.pub.PublicBudget,'send',side_effect=AssertionError('network')):self.assertEqual(s.dispatch('R020',p,'unused',15),f.old.read(O/'requests/0550/response.json'))
 def test_failed_old_core_does_not_admit_late_callback(self):
  r=f.old.read(O/'evaluations/R020/recovered.json');r['raw_callback_trace']=r['evidence_trace'];checks,used=f.accepted(O,r);self.assertEqual(used,['requests/0548/record.json']);self.assertEqual(len(checks),1)
 def test_authentication_and_integrity_failures_stop(self):
  for diag in ({'http_status':401},{'error_type':'ValueError','phase':'artifact'}):
   self.assertFalse(f.recognized({'receipts':[{'status':'service_failed'}],'stop_diagnostic':diag,'raw_callback_trace':[]}))
if __name__=='__main__':unittest.main()
