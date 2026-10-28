import copy,json,shutil,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from benchmarks import public_recovery as r
O=Path('artifacts/014-public-ai-benchmark-20261025-v2')
@unittest.skipUnless((O/'manifest.json').exists(), 'Local frozen research raw evidence is not bundled with the source repository')
class RecoveryTest(unittest.TestCase):
 def setUp(self):
  # Offline historical raw validation remains testable after a later operational stop.
  self.proof_patch=patch.object(r,'verify',return_value=r.old.read(O/'recovery-manifest.json'));self.proof_patch.start();self.addCleanup(self.proof_patch.stop)
 def test_real_invalid_is_single_question(self):
  p=r.old.read(O/'requests/0016/request.json');a=r.old.read(O/'requests/0016/response.json');good,bad=r.comp.split_answers(p,a)
  self.assertEqual((len(good),len(bad)),(33,1));rp,_=r.comp.subset(p,a,bad);self.assertEqual(rp['state'],p['state']);self.assertEqual(list(rp['questions']),bad)
 def test_valid_prefix_reused_without_transport(self):
  m=r.pub.verify(O);s=r.Store(O,m);p=r.old.read(O/'requests/0001/request.json')
  with patch.object(r.pub.rec.Store,'send',side_effect=AssertionError('network')):
   self.assertEqual(s.dispatch('R001',p,'unused',15),r.old.read(O/'requests/0001/response.json'))
  self.assertEqual(s.trace,['requests/0001/record.json'])
 def test_observed_composite_rejects_rewritten_valid_answer(self):
  folder=next((O/'composites/R001').glob('*'));proof=r.old.read(folder/'record.json');am=r.verify(O)
  with tempfile.TemporaryDirectory() as d:
   out=Path(d);dest=out/folder.relative_to(O);shutil.copytree(folder,dest)
   for rel in (proof['original'],proof['repair']):shutil.copytree((O/rel).parent,(out/rel).parent)
   with patch.object(r,'verify',return_value=am):
    r.composite(out,dest)
    reply=r.old.read(dest/'response.json');name=next(n for n,src in proof['answer_sources'].items() if src==proof['original']);reply['answers'][name]['confidence']=0.01
    r.old.save(dest/'response.json',reply);proof['response_digest']=r.core.digest(reply);r.old.save(dest/'record.json',proof);(dest/'seal').write_text(r.base.digest(proof))
    with self.assertRaisesRegex(ValueError,'answer/provenance drift'):r.composite(out,dest)
 def test_repair_ticket_blocks_a_second_network_attempt(self):
  with tempfile.TemporaryDirectory() as d:
   out=Path(d);rel='requests/0016/record.json';shutil.copytree((O/rel).parent,(out/rel).parent)
   r.old.save(out/'repair-attempts/R001-0016.json',{'status':'started'})
   store=r.Store(out,r.pub.verify(O))
   with patch.object(r.pub.rec.Store,'send',side_effect=AssertionError('network')):
    with self.assertRaisesRegex(ValueError,'already attempted'):store.repair('R001',rel,'unused',15)
 def test_unsupported_failure_not_salvaged(self):
  p=r.old.read(O/'requests/0016/request.json');a=r.old.read(O/'requests/0016/response.json');a['model']='invented'
  with self.assertRaises(ValueError):r.comp.split_answers(p,a)
 def test_original_caps_preserved(self):
  with tempfile.TemporaryDirectory() as d:
   s=r.pub.PublicBudget(Path(d),'1.999')
   with patch.object(r.pub.capture,'request',side_effect=AssertionError('network')):
    with self.assertRaises(r.pub.rec.RecordedFailure):s.send('R001',{'model':r.core.MODEL,'questions':{}},'unused',15)
if __name__=='__main__':unittest.main()
