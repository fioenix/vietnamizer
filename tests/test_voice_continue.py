import unittest
from benchmarks import voice_continue as c
from benchmarks import voice_pilot as v
class ContinuationTests(unittest.TestCase):
 def test_only_evidence_invalid_main_judgment_can_be_terminal_missing(self):
  p,_=v.calibration(0,False);a=v.fixture_assessment(p);a['assessments'][0]['reference_evidence']='fabricated'
  import json
  r={'id':'judge-V4-gemini','status':'failed','error':'ValueError: unsupported reference quote','text':json.dumps(a)}
  self.assertTrue(c.rejected_assessment(p,r))
  for field,value in [('id','cal-0-gemini'),('error','ValueError: Gemini native/wrapper mismatch')]:
   wrong=dict(r);wrong[field]=value
   with self.assertRaises(ValueError):c.rejected_assessment(p,wrong)
 def test_wrong_blind_mapping_rejected(self):
  p,m=v.blind_packet('V1','source',dict.fromkeys(v.ARMS,'text'),['ref'],False)
  with self.assertRaises(ValueError):c.check_binding(p,m,{'packet':p,'mapping':{}},v.judge_prompt(p).encode())
  c.check_binding(p,m,{'packet':p,'mapping':m},v.judge_prompt(p).encode())
