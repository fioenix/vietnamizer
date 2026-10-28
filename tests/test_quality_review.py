import copy,json,tempfile,unittest
from pathlib import Path

class QualityTest(unittest.TestCase):
 def setUp(self):
  if self._testMethodName in {
   'test_replacing_blind_packet_and_sidecar_cannot_change_frozen_assignments',
   'test_report_rejects_valid_looking_inventory_changed_after_raw_model_response',
   'test_manifest_binds_execution_transport_source',
   'test_empty_report_accounts_for_all_40_planned_pair_votes',
  }:
   from tests.quality_fixture import quality_cohort
   self.enterContext(quality_cohort())
 def api(self):
  try:from benchmarks import quality_review
  except ImportError:self.fail("Quality review implementation is missing")
  return quality_review
 def test_diff_keeps_exact_offsets_and_unchanged_has_no_edits(self):
  q=self.api();a='Tôi đã đi.';b='Tôi đã đến.';r=q.diff_blocks(a,b)
  self.assertEqual([(x['before'],x['after']) for x in r],[('đi','đến')])
  for x in r:self.assertEqual(a[x['source_start']:x['source_end']],x['before']);self.assertEqual(b[x['output_start']:x['output_end']],x['after'])
  self.assertEqual(q.diff_blocks(a,a),[])
 def test_blinding_balances_positions_and_contains_no_arm_key(self):
  q=self.api();cases=[{'id':f'P{i:02}','source':'Nguồn','audience':'Bạn đọc','purpose':'Báo cáo'} for i in range(20)]
  records={c['id']:{a:'Bản '+str(i) for i,a in enumerate(q.ARMS)} for c in cases}
  packet,key=q.blind(cases,records,12)
  self.assertEqual(len(packet),20)
  for arm in q.ARMS:
   for letter in 'ABCD':self.assertEqual(sum(key[c['id']][letter]['arm']==arm for c in packet),5)
  self.assertNotIn('arm',json.dumps(packet));self.assertNotIn('epoch',json.dumps(packet))
 def test_inventory_rejects_hallucinated_quote_and_duplicate_source(self):
  q=self.api();p=[{'id':'Q01','source':'Tôi đã đi.','audience':'a','purpose':'p'}]
  r={'sources':[{'id':'Q01','uncertain':False,'issues':[{'id':'I1','quote':'Tôi đã đi.','description':'Lý do'}]}]}
  q.validate_inventory(p,r)
  bad=copy.deepcopy(r);bad['sources'][0]['issues'][0]['quote']='Không có'
  with self.assertRaises(ValueError):q.validate_inventory(p,bad)
  bad=copy.deepcopy(r);bad['sources']*=2
  with self.assertRaises(ValueError):q.validate_inventory(p,bad)
 def fixture(self):
  p={'id':'Q01','source':'Tôi đã đi.','outputs':{k:{'text':'Tôi đã đi.','edits':[]} for k in 'ABCD'}}
  inv={'id':'Q01','uncertain':False,'issues':[]}
  r={'id':'Q01','outputs':{k:{'meaning':'clear','voice':'clear','protected':'clear','notes':'','edits':{},'issues':{}} for k in 'ABCD'},'ranks':{'A':1,'B':1,'C':2,'D':0},'ranking_reason':'D chưa rõ'}
  return p,inv,r
 def test_grade_rejects_missing_or_orphan_labels(self):
  q=self.api();p,i,r=self.fixture();q.validate_grade(p,i,r)
  bad=copy.deepcopy(r);del bad['outputs']['A']
  with self.assertRaises(ValueError):q.validate_grade(p,i,bad)
  bad=copy.deepcopy(r);bad['outputs']['A']['edits']['E999']='harmful'
  with self.assertRaises(ValueError):q.validate_grade(p,i,bad)
 def test_violation_requires_evidence_note_and_cannot_be_numeric_pass(self):
  q=self.api();p,i,r=self.fixture();r['outputs']['A']['meaning']='violation'
  with self.assertRaises(ValueError):q.validate_grade(p,i,r)
  r['outputs']['A']['notes']='Đổi chủ thể của câu.';q.validate_grade(p,i,r)
  r['outputs']['A']['meaning']=0
  with self.assertRaises(ValueError):q.validate_grade(p,i,r)
 def test_zero_edits_and_zero_issues_are_undefined_not_perfect(self):
  q=self.api();m=q.metrics({'meaning':'uncertain','voice':'clear','protected':'clear','edits':{},'issues':{}})
  self.assertIsNone(m['precision']);self.assertIsNone(m['recall']);self.assertIsNone(m['meaning_violation'])
 def test_partial_and_uncertain_stay_in_denominators(self):
  q=self.api();m=q.metrics({'meaning':'violation','voice':'clear','protected':'clear','edits':{'e1':'justified_successful','e2':'uncertain','e3':'mixed'},'issues':{'i1':'resolved','i2':'partial'}})
  self.assertAlmostEqual(m['precision'],1/3);self.assertEqual(m['recall'],.5)
 def test_uncertain_edit_is_not_a_clean_safety_label(self):
  q=self.api();r={'meaning':'clear','voice':'clear','protected':'clear','edits':{'e1':'uncertain'},'issues':{}}
  self.assertIsNone(q.metrics(r)['unnecessary_edit'])
  r['edits']['e2']='unnecessary';self.assertEqual(q.metrics(r)['unnecessary_edit'],1)
 def test_rank_tie_and_abstention_are_distinct(self):
  q=self.api();self.assertEqual(q.preference(1,1),'tie');self.assertEqual(q.preference(1,2),'win');self.assertEqual(q.preference(0,2),'uncertain')
 def test_paired_bootstrap_uses_source_clusters_and_keeps_reviewer_pair(self):
  q=self.api();r=q.paired_interval([[1,1],[0,0]],seed=12,draws=1000)
  self.assertEqual(r['n_sources'],2);self.assertEqual(r['estimate'],.5);self.assertEqual(r['low'],0);self.assertEqual(r['high'],1)
 def test_kappa_undefined_for_constant_agreement(self):
  q=self.api();r=q.agreement(['clear']*4,['clear']*4);self.assertEqual(r['agreement'],1);self.assertIsNone(r['kappa'])
 def test_tool_calls_quarantine_model_labels(self):
  q=self.api();raw=json.dumps({'type':'turn.completed'})+'\n'+json.dumps({'type':'item.completed','item':{'type':'command_execution','command':'ls'}})+'\n'+json.dumps({'type':'item.completed','item':{'type':'agent_message','text':'{"sources":[]}'}})
  with self.assertRaises(ValueError):q.parse_model(raw)
 def test_empty_or_unfinished_model_output_is_not_a_review(self):
  q=self.api()
  for raw in ('','{"type":"turn.started"}'):
   with self.assertRaises(ValueError):q.parse_model(raw)

 def test_replacing_blind_packet_and_sidecar_cannot_change_frozen_assignments(self):
  q=self.api()
  with tempfile.TemporaryDirectory() as t:
   out=Path(t);q.prepare(out);p=q.read(out/'packets/M1.json');p[0]['source']='Nguồn đã thay đổi';q.save(out/'packets/M1.json',p)
   binding=q.read(out/'private/M1-packet-binding.json');binding['packet_digest']=q.digest(p);q.save(out/'private/M1-packet-binding.json',binding)
   with self.assertRaises(ValueError):q.verify(out)
 def test_report_rejects_valid_looking_inventory_changed_after_raw_model_response(self):
  from unittest.mock import patch
  from types import SimpleNamespace
  q=self.api()
  with tempfile.TemporaryDirectory() as t:
   out=Path(t);q.prepare(out);packet=q.read(out/'packets/M1.json');inventory={'sources':[{'id':p['id'],'uncertain':False,'issues':[]} for p in packet]}
   text=json.dumps({'payload':json.dumps(inventory)})
   raw=json.dumps({'type':'item.completed','item':{'type':'agent_message','text':text}})+'\n'+json.dumps({'type':'turn.completed','usage':{}})
   with patch.object(q.base,'execute',return_value=SimpleNamespace(stdout=raw,stderr='',returncode=0)):
    q.call_model(out,'M1','sources',q.inventory_prompt(packet),lambda r:q.validate_inventory(packet,r))
   inventory['sources'][0]['uncertain']=True;q.save(out/'model-attempts/M1-sources/labels.json',inventory)
   with self.assertRaises(ValueError):q.report(out)

 def test_manifest_binds_execution_transport_source(self):
  q=self.api()
  with tempfile.TemporaryDirectory() as t:
   manifest=q.prepare(Path(t));self.assertIn(str(Path(q.base.__file__)),manifest['fingerprints'])
 def test_empty_report_accounts_for_all_40_planned_pair_votes(self):
  q=self.api()
  with tempfile.TemporaryDirectory() as t:
   out=Path(t);q.prepare(out);r=q.report(out)
   for comparison in r['comparisons']:self.assertEqual(comparison['votes'],{'missing':40})

if __name__=='__main__':unittest.main()
