import unittest
from benchmarks.voice_patch_analysis import normalized_preferences

class VoiceAnalysisTests(unittest.TestCase):
 def test_position_reversal_preserves_normalized_winner(self):
  a={'preferences':[{'id':'p','preference':'left','reason':'x'}]};m={'pairs':{'p':{'contrast':'D-B','left_arm':'D','right_arm':'B'}}}
  b={'preferences':[{'id':'p','preference':'right','reason':'x'}]};n={'pairs':{'p':{'contrast':'D-B','left_arm':'B','right_arm':'D'}}}
  self.assertEqual(normalized_preferences(a,m),normalized_preferences(b,n));self.assertEqual(normalized_preferences(a,m)[0]['outcome'],'win')
 def test_tie_and_uncertainty_not_forced_winners(self):
  for k in ('tie','uncertain'):
   a={'preferences':[{'id':'p','preference':k,'reason':'x'}]};m={'pairs':{'p':{'contrast':'B-A','left_arm':'A','right_arm':'B'}}}
   self.assertEqual(normalized_preferences(a,m)[0]['outcome'],k)
 def test_rejected_block_is_missing_not_partially_salvaged(self):
  from pathlib import Path
  from tempfile import TemporaryDirectory
  from unittest.mock import patch
  from benchmarks import voice_patch_analysis as a
  from benchmarks import voice_patch_versions as v
  records=[{'id':f'edit-{cid}-{arm}','status':'completed','text':'edited','session':f'{cid}-{arm}'} for cid in v.CASES for arm in v.ARMS]
  records.append({'id':'judge-V4-gemini','status':'failed','error':'unsupported quote','session':'failed-judge'})
  with TemporaryDirectory() as tmp:
   out=Path(tmp);(out/'corpus').mkdir()
   for cid in v.CASES:(out/'corpus'/f'{cid}.txt').write_text('original')
   with patch.object(v,'verify',return_value={}),patch.object(v,'audit_history',return_value=records):data,rows,contrasts=a.analyze(out)
   self.assertEqual((len(rows),len(contrasts),data['main_judgments']),(0,0,0));self.assertEqual(data['editing_outputs'],32)
   self.assertEqual(data['rejected_judgments'][0]['id'],'judge-V4-gemini')
   self.assertTrue(all(r['rated']==0 and r['missing']==r['expected'] for r in data['summary']))

 def test_portable_audit_rejects_tampered_sealed_file(self):
  from pathlib import Path
  from tempfile import TemporaryDirectory
  from benchmarks import voice_patch_analysis as a
  from benchmarks import voice_patch_versions as v
  with TemporaryDirectory() as tmp:
   p=Path(tmp);v.save(p/'manifest.json',{'cap':52,'plan_ids':v.plan_ids(),'fingerprints':{},'code':{}});(p/'data.txt').write_text('frozen')
   v.save(p/'final-seal.json',{'sha256':{f.name:v.sha(f.read_bytes()) for f in p.iterdir()}})
   self.assertEqual(a.verify_archive(p)['cap'],52)
   (p/'data.txt').write_text('changed')
   with self.assertRaises(ValueError):a.verify_archive(p)
