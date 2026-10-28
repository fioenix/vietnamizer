import copy,tempfile,unittest
from pathlib import Path
class SimpleFormsTest(unittest.TestCase):
 def api(self):
  try:from benchmarks import simple_forms as s
  except ImportError:self.fail('Simple Forms implementation missing')
  return s
 def packet(self):return {'reviewer':'A','version':'editorial-quality-v1','cases':[{'id':'Q001','source':'Tôi có 80 phiếu.','audience':'Bạn đọc','purpose':'Báo cáo','outputs':{k:{'text':'Tôi có 80 phiếu.','edits':[]} for k in 'ABCD'}}]}
 def test_contract_has_three_questions_and_all_four_blinded_outputs(self):
  s=self.api();p=self.packet();r=s.contract(p)
  self.assertEqual(len(r['questions']),3);self.assertEqual(r['groups'][0]['source'],p['cases'][0]['source']);self.assertEqual(set(r['groups'][0]['outputs']),set('ABCD'))
  self.assertEqual([x['kind'] for x in r['questions']],['grid','grid','paragraph']);self.assertNotIn('issues',r['groups'][0]);self.assertEqual(r['schema'],'human-simple-v2')
 def test_source_output_and_order_are_lossless_and_no_arm_key(self):
  s=self.api();p=self.packet();p['cases'][0]['outputs']['D']['text']='Tôi có 81 phiếu.';r=s.contract(p)
  self.assertEqual(r['groups'][0]['outputs']['D'],'Tôi có 81 phiếu.');self.assertNotIn('arm',r['groups'][0]);self.assertEqual(r['packet_digest'],s.q.digest(p['cases']))
 def test_incomplete_output_identity_is_rejected(self):
  s=self.api();p=self.packet();del p['cases'][0]['outputs']['D']
  with self.assertRaises(ValueError):s.contract(p)
 def test_import_maps_only_known_answers_and_preserves_unknown_and_notes(self):
  s=self.api();c=s.contract(self.packet());items={'Q001':{'preservation':1,'readability':2,'notes':3}}
  raw=[{'item_id':1,'response':['Giữ đúng','Có chỗ bị đổi','Chưa rõ','Giữ đúng']},{'item_id':2,'response':['Tự nhiên, rõ ràng hơn','Tương đương','Khó đọc hơn','Chưa rõ']},{'item_id':3,'response':'B: đổi số liệu.'}]
  r=s.decode(c,items,raw);self.assertEqual(r[0]['outputs']['C']['preservation'],'uncertain');self.assertEqual(r[0]['outputs']['D']['readability'],'uncertain');self.assertEqual(r[0]['notes'],'B: đổi số liệu.')
  raw[0]['response'][0]='Như cũ'
  with self.assertRaises(ValueError):s.decode(c,items,raw)
 def test_prepare_rejects_changed_handoff_even_with_new_claimed_digest(self):
  from unittest.mock import patch
  s=self.api()
  for refresh in (False,True):
   with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);cases=self.packet()['cases'];packet={**self.packet(),'packet_digest':s.q.digest(cases)}
    s.q.save(root/'packets/A.json',cases)
    changed=copy.deepcopy(packet);changed['cases'][0]['source']='Sai nguồn.'
    if refresh:changed['packet_digest']=s.q.digest(changed['cases'])
    s.q.save(root/'human-handoff/reviewer-A/packet.json',changed)
    with patch.object(s.q,'verify'),patch.object(s,'render_pair') as render:
     with self.assertRaisesRegex(ValueError,'frozen assignment'):s.prepare(root,root/'out')
     render.assert_not_called()
 def test_missing_response_does_not_become_pass(self):
  s=self.api();c=s.contract(self.packet());r=s.decode(c,{'Q001':{'preservation':1,'readability':2,'notes':3}},[])
  self.assertIsNone(r[0]['outputs']['A']['preservation']);self.assertIsNone(r[0]['outputs']['A']['readability'])
if __name__=='__main__':unittest.main()
