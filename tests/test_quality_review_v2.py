import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from benchmarks import quality_review_v2 as v
from benchmarks import quality_review as q

class AmendmentTest(unittest.TestCase):
 def setUp(self):
  if self._testMethodName != 'test_new_prompt_only_adds_serialization_contract':
   from tests.quality_fixture import quality_cohort
   self.enterContext(quality_cohort(inherited=True))
 def test_inherits_exact_valid_inventory_and_failed_group_without_new_start(self):
  with tempfile.TemporaryDirectory() as t:
   out=Path(t);v.prepare(out);v.verify(out)
   packet=q.read(out/'packets/M1.json');r=q.call_model(out,'M1','sources',q.inventory_prompt(packet),lambda x:q.validate_inventory(packet,x))
   self.assertEqual(len(r['sources']),20)
   self.assertEqual(q.read(out/'model-attempts/M1-Q001/result.json')['status'],'failed')
   with patch.object(q,'call_model',side_effect=[r,RuntimeError('stop before dispatch')]) as call:
    with self.assertRaisesRegex(RuntimeError,'stop before dispatch'):v.run(out,'M1',1)
    self.assertEqual(call.call_args_list[1].args[2],'Q002')
 def test_original_raw_change_is_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   out=Path(t);v.prepare(out);p=out/'model-attempts/M1-Q001/stdout.jsonl';p.write_text('changed')
   with self.assertRaisesRegex(ValueError,'inherited raw drift'):v.verify(out)
 def test_existing_labels_not_rescored_and_missingness_is_retained(self):
  with tempfile.TemporaryDirectory() as t:
   out=Path(t);v.prepare(out)
   with patch.object(q.base,'execute',side_effect=AssertionError('no model dispatch')):r=v.report(out)
   self.assertEqual(r['missing_output_reviews'],160)
   self.assertEqual(len(r['failed_attempts']),1)
   for c in r['comparisons']:self.assertEqual(c['votes'],{'missing':40})
 def test_new_failure_stops_cross_judge_inventory_dispatch(self):
  with tempfile.TemporaryDirectory() as t:
   out=Path(t);v.prepare(out);q.save(out/'model-attempts/M1-Q002/result.json',{'status':'failed','unit':'Q002'})
   with patch.object(q,'call_model',side_effect=AssertionError('must not dispatch')) as call:
    with self.assertRaisesRegex(ValueError,'new failure'):v.run(out,'M2',1)
    call.assert_not_called()
 def test_new_prompt_only_adds_serialization_contract(self):
  packet={'id':'Q001'};inventory={'id':'Q001','issues':[]}
  self.assertTrue(v.grade_prompt(packet,inventory).startswith(v.original_grade_prompt(packet,inventory)))
  self.assertIn('"clear", "violation", "uncertain"',v.grade_prompt(packet,inventory))
if __name__=='__main__':unittest.main()
