import json
from pathlib import Path
import tempfile
import unittest
from benchmarks import voice_pilot as v

class VoicePilotTests(unittest.TestCase):
 def test_exact_plan_and_cap(self):
  x=v.plan_ids();self.assertEqual(len(x),56);self.assertEqual(len(set(x)),56)
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)
   for i in x:v.reserve(p,i)
   with self.assertRaises(ValueError):v.reserve(p,x[0])
   with self.assertRaises(ValueError):v.reserve(p,'extra')
 def test_factorial_parity(self):
  case={'source':'Bản gốc.','context':'Blog kỹ thuật.'};refs=['mẫu một','mẫu hai','mẫu ba']
  a=v.edit_input(case,'A',refs);b=v.edit_input(case,'B',refs);c=v.edit_input(case,'C',refs);d=v.edit_input(case,'D',refs)
  self.assertEqual(a,c);self.assertEqual(b,d);self.assertEqual(b['writing_samples'],refs)
  self.assertNotIn('writing_samples',a)
 def test_blind_packet_and_evidence(self):
  refs=['Tôi viết gọn.','Tôi giữ ý.'];texts={a:'Bản '+a for a in 'ABCD'}
  packet,mapping=v.blind_packet('V1','Nguồn.',texts,refs,1)
  raw=json.dumps(packet,ensure_ascii=False)
  self.assertNotIn('Vietnamizer',raw);self.assertNotIn('condition',raw);self.assertEqual(len(mapping['aliases']),4)
  result=v.fixture_assessment(packet)
  v.validate_assessment(packet,result)
  result['assessments'][1]['evidence']='trích dẫn không tồn tại'
  with self.assertRaises(ValueError):v.validate_assessment(packet,result)
 def test_calibration_uses_separate_checks(self):
  packet,expected=v.calibration(0,1);a=v.fixture_assessment(packet)
  for r in a['assessments']:
   if r['id'] in expected['major']:r['meaning']='major'
  v.validate_calibration(packet,a,expected)
  for r in a['assessments']:r['meaning']='clear'
  with self.assertRaises(ValueError):v.validate_calibration(packet,a,expected)
 def test_no_retry_and_missing_not_pass(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);cell=v.plan_ids()[0];a=v.reserve(p,cell)
   (a/'result.json').write_text('{"status":"failed"}')
   with self.assertRaises(ValueError):v.reserve(p,cell)
 def test_incomplete_history_stops_before_next_start(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);v.reserve(p,v.plan_ids()[0])
   with self.assertRaises(ValueError):v.audit_history(p,{})
 def test_wrong_pairs_and_duplicate_ratings_rejected(self):
  packet,_=v.blind_packet('V1','Nguồn.',{a:'Bản '+a for a in 'ABCD'},['Mẫu.','Mẫu khác.'],1)
  a=v.fixture_assessment(packet);a['assessments'][1]=dict(a['assessments'][0])
  with self.assertRaises(ValueError):v.validate_assessment(packet,a)
