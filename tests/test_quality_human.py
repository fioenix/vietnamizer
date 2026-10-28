import copy,hashlib,json,unittest
from benchmarks import quality_review as q

class HumanImportTest(unittest.TestCase):
 def api(self):
  try:from benchmarks import quality_human as h
  except ImportError:self.fail('Human import contract missing')
  return h
 def fixture(self):
  packet=[{'id':'Q001','source':'Tôi đi.','audience':'Bạn đọc','purpose':'Kể chuyện','outputs':{k:{'text':'Tôi đi.','edits':[]} for k in 'ABCD'}}]
  sources={'Q001':{'id':'Q001','issues':[],'uncertain':False,'reviewed':True}}
  digest=hashlib.sha256(json.dumps(list(sources.values()),ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
  grade={'id':'Q001','outputs':{k:{'meaning':'clear','voice':'clear','protected':'clear','notes':'','edits':{},'issues':{}} for k in 'ABCD'},'ranks':{k:1 for k in 'ABCD'},'ranking_reason':'Giống nhau.'}
  data={'version':'editorial-quality-v1','reviewer':'A','packet_digest':q.digest(packet),'cases':packet}
  submission={'version':data['version'],'kind':'human','reviewer':'A','packet_digest':data['packet_digest'],'submission':'final','profile':{'experience':'Biên tập','conflicts':'Không','independent':True},'sources':sources,'grades':{'Q001':grade},'source_lock':{'digest':digest,'at':'2026-10-25T10:00:00.000Z'},'events':[{'type':'source_locked','digest':digest,'at':'2026-10-25T10:00:00.000Z'}]}
  return data,submission
 def test_complete_human_submission_round_trips_and_preserves_original(self):
  h=self.api();p,s=self.fixture();before=copy.deepcopy(s);h.validate(p,s);self.assertEqual(s,before)
 def test_other_packet_and_missing_labels_are_rejected(self):
  h=self.api();p,s=self.fixture();s['packet_digest']='wrong'
  with self.assertRaises(ValueError):h.validate(p,s)
  p,s=self.fixture();del s['grades']['Q001']['outputs']['A']
  with self.assertRaises(ValueError):h.validate(p,s)
 def test_changed_source_inventory_after_lock_is_rejected(self):
  h=self.api();p,s=self.fixture();s['sources']['Q001']['uncertain']=True
  with self.assertRaisesRegex(ValueError,'lock'):h.validate(p,s)
 def test_changed_packet_content_cannot_reuse_claimed_digest(self):
  h=self.api();p,s=self.fixture();p['cases'][0]['outputs']['A']['text']='Nội dung khác'
  with self.assertRaisesRegex(ValueError,'packet'):h.validate(p,s)
 def test_human_handoff_escapes_script_termination(self):
  h=self.api();s=h.embed({'source':'</script><img onerror=alert(1)> & text'})
  self.assertNotIn('</script>',s);self.assertEqual(json.loads(s)['source'],'</script><img onerror=alert(1)> & text')
if __name__=='__main__':unittest.main()
