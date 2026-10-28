import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from benchmarks import voice_section_versions as v

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
   for version in ('0.13.1','0.13.2'):
    d=p/'libraries'/version;d.mkdir(parents=True);(d/'SKILL.md').write_text('version '+version)
   for cid in v.CASES:
    a=v.edit_prompt(p,cid,'A');c=v.edit_prompt(p,cid,'C');self.assertEqual(a,c)
    self.assertIn('Adapt this Vietnamese draft toward the voice',a)
    b=v.edit_prompt(p,cid,'B');d=v.edit_prompt(p,cid,'D')
    self.assertEqual(b.replace('version 0.13.1','version X'),d.replace('version 0.13.2','version X'))
    self.assertEqual(b[b.index('<editing_input>'):],a[a.index('<editing_input>'):])
 def test_full_blind_mapping_stays_version_hidden(self):
  p,m=v.blind_packet('V1','source',dict(zip(v.ARMS,['a','b','c','d'])),['ref'],False)
  self.assertNotIn('0.13.1',v.judge_prompt(p));self.assertEqual(m['pairs']['p3']['contrast'],'D-B')
  assessment=v.fixture_assessment(p);v.validate_assessment(p,assessment)
 def test_zip_path_rejects_traversal(self):
  self.assertTrue(v.safe_member('vietnamizer/profiles/blog-ca-nhan/rules.md'))
  for n in ('vietnamizer/../../bad.md','/tmp/SKILL.md','vietnamizer/a\\b.md'):
   self.assertFalse(v.safe_member(n))

class PreflightRepairTests(unittest.TestCase):
 def test_capture_every_runtime_source_and_reject_name_collisions(self):
  with TemporaryDirectory() as t:
   root=Path(t);files=[]
   for i,name in enumerate(('runner.py','guard.mjs','boundary.mjs','agybird.mjs')):
    p=root/'source'/name;p.parent.mkdir(exist_ok=True);p.write_bytes(f'code{i}'.encode());files.append(p)
   out=root/'out';v.capture_code(out,files)
   for p in files:self.assertEqual((out/'runner-source'/p.name).read_bytes(),p.read_bytes())
   duplicate=root/'elsewhere/guard.mjs';duplicate.parent.mkdir();duplicate.write_text('other')
   with self.assertRaises(ValueError):v.capture_code(root/'out2',files+[duplicate])
 def test_actual_audit_keeps_bad_nested_schema_missing_but_rejects_transport_failure(self):
  import json
  from unittest.mock import patch
  with TemporaryDirectory() as t:
   out=Path(t);v.save(out/'manifest.json',{})
   packet,mapping=v.blind_packet('V1','source',dict(zip(v.ARMS,['a','b','c','d'])),['ref'],False)
   bad=v.fixture_assessment(packet);bad['assessments']=['invalid']*5
   prompt=v.judge_prompt(packet);ident='judge-V1-codex';p=out/'attempts'/ident;p.mkdir(parents=True)
   (p/'stdin.txt').write_text(prompt);v.save(p/'response-schema.json',v.base.SCHEMA);(p/'stdout.txt').write_text('synthetic raw')
   v.save(out/'blind/V1-codex.json',{'packet':packet,'mapping':mapping})
   parsed={'text':json.dumps(bad),'session':'fresh-synthetic','usage':{}}
   r={**parsed,'id':ident,'provider':'codex','status':'failed','error':'ValueError: assessment nested shape','cwd':str(out),'argv':v.base.codex_args(out),'manifest_sha256':v.sha((out/'manifest.json').read_bytes()),'stdin_sha256':v.sha(prompt.encode())}
   def seal():
    v.save(p/'result.json',r);v.save(p/'seal.json',{f.name:v.sha(f.read_bytes()) for f in p.iterdir() if f.name!='seal.json'})
   seal()
   with patch.object(v,'main_packet',return_value=(packet,mapping)),patch.object(v.native,'parse',return_value=parsed):
    rows=v.audit_history(out,{})
    self.assertEqual((len(rows),rows[0]['status']),(1,'failed'))
    r['error']='ValueError: nonzero Codex exit';seal()
    with self.assertRaises(ValueError):v.audit_history(out,{})
