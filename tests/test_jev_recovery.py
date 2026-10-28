import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from benchmarks import jev_recovery as recovery
from benchmarks import jev_pilot as old
from jev import core
from tests.test_jev import response

class RecoveryTest(unittest.TestCase):
 def test_raw_invalid_reply_kept_and_validation_reason_classified(self):
  with tempfile.TemporaryDirectory() as t:
   store=recovery.Store(Path(t),origins=[])
   payload={'model':core.MODEL,'state':{},'questions':{'x':{'type':'noul'}}}
   def fake(payload,key,timeout,target):
    r=response(payload);r['answers']['x']['noul']=2
    (target/'response.body').write_text(json.dumps(r));old.save(target/'http.json',{'http_status':200,'body_complete':True})
    return r
   with patch.object(recovery.capture,'request',side_effect=fake):
    with self.assertRaises(recovery.RecordedFailure):store.send('P01',payload,'fake',1)
   record=store.entries()[0]
   self.assertEqual(record['status'],'invalid_response')
   self.assertEqual(record['diagnostic']['reason'],'noul_range')
   self.assertTrue((Path(t)/'requests/0001/response.json').exists())
   self.assertTrue((Path(t)/'requests/0001/response.body').exists())
   self.assertEqual(store.summary()['requests'],1)
 def test_global_budget_includes_inherited_unknown_reservations(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);origin=root/'prior';(origin/'requests').mkdir(parents=True)
   old.save(origin/'requests/0001.json',{'case':'P01','status':'billing_unknown','reserve_usd':str(old.RESERVE),'request_digest':'x'})
   s=recovery.Store(root/'new',origins=[origin],cap=old.RESERVE)
   with patch.object(recovery.capture,'request',side_effect=AssertionError('sent over cap')):
    with self.assertRaises(recovery.RecordedFailure):s.send('P02',{'model':core.MODEL,'questions':{}},'fake',1)
   self.assertEqual(s.summary()['requests'],1)
   self.assertEqual(s.summary()['reserved_or_actual_usd'],str(old.RESERVE))
 def test_request_cache_never_retries_validated_answer(self):
  with tempfile.TemporaryDirectory() as t:
   s=recovery.Store(Path(t),origins=[]);p={'model':core.MODEL,'questions':{'x':{'type':'noul'}}}
   r=response(p);s.cache[('P01',core.digest(p))]={'reply':r,'origin':'test-cache'}
   with patch.object(recovery.capture,'request',side_effect=AssertionError('cache resent')):
    self.assertEqual(s.send('P01',p,'fake',1),r)
   self.assertEqual(s.summary()['requests'],0)
   self.assertEqual(len(s.replayed),1)
if __name__=='__main__':unittest.main()
