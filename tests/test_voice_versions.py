import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from benchmarks import voice_versions as v

class VoiceVersionTests(unittest.TestCase):
 def test_exact52ids_and_no_retry(self):
  ids=v.plan_ids();self.assertEqual((len(ids),len(set(ids))),(52,52))
  self.assertEqual(sum(x.startswith('edit-') for x in ids),32)
  with TemporaryDirectory() as t:
   p=Path(t);v.reserve(p,ids[0])
   with self.assertRaises(ValueError):v.reserve(p,ids[0])
   with self.assertRaises(ValueError):v.reserve(p,'draft-N1')
 def test_explicit_task_and_identical_control_inputs(self):
  with TemporaryDirectory() as t:
   p=Path(t);(p/'corpus').mkdir();v.save(p/'bundle-files.json',['SKILL.md'])
   (p/'common.txt').write_text(v.COMMON)
   for n in (*v.CASES,'R1','R2','R3'):(p/'corpus'/f'{n}.txt').write_text(n+' source')
   for version in ('0.12.1','0.13.0'):
    d=p/'libraries'/version;d.mkdir(parents=True);(d/'SKILL.md').write_text('version '+version)
   for cid in v.CASES:
    a=v.edit_prompt(p,cid,'A');c=v.edit_prompt(p,cid,'C');self.assertEqual(a,c)
    self.assertIn('Adapt this Vietnamese draft toward the voice',a)
    b=v.edit_prompt(p,cid,'B');d=v.edit_prompt(p,cid,'D')
    self.assertEqual(b.replace('version 0.12.1','version X'),d.replace('version 0.13.0','version X'))
    self.assertEqual(b[b.index('<editing_input>'):],a[a.index('<editing_input>'):])
 def test_full_blind_mapping_stays_version_hidden(self):
  p,m=v.blind_packet('V1','source',dict(zip(v.ARMS,['a','b','c','d'])),['ref'],False)
  self.assertNotIn('0.13.0',v.judge_prompt(p));self.assertEqual(m['pairs']['p3']['contrast'],'D-B')
  assessment=v.fixture_assessment(p);v.validate_assessment(p,assessment)
 def test_zip_path_rejects_traversal(self):
  self.assertTrue(v.safe_member('vietnamizer/profiles/blog-ca-nhan/rules.md'))
  for n in ('vietnamizer/../../bad.md','/tmp/SKILL.md','vietnamizer/a\\b.md'):
   self.assertFalse(v.safe_member(n))
