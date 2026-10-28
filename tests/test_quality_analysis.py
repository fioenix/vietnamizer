import unittest
class AnalysisTest(unittest.TestCase):
 def api(self):
  try:from benchmarks import quality_analysis as a
  except ImportError:self.fail('Analysis implementation missing')
  return a
 def test_zero_observed_errors_still_has_nonzero_upper_interval(self):
  a=self.api();r=a.wilson(0,20);self.assertAlmostEqual(r['low'],0);self.assertGreater(r['high'],0)
 def test_partial_paired_source_does_not_become_two_independent_samples(self):
  a=self.api();r=a.difference_clusters([{'case_id':'P01','judge':'M1','arm':'a','precision':1},{'case_id':'P01','judge':'M1','arm':'b','precision':0}],['P01','P02'],'a','b','precision')
  self.assertEqual(r,[[1,None],[None,None]])
 def test_complete_pair_retains_judges_within_one_source(self):
  a=self.api();rows=[{'case_id':'P01','judge':j,'arm':arm,'recall':v} for j in ('M1','M2') for arm,v in [('a',1),('b',.5)]]
  self.assertEqual(a.difference_clusters(rows,['P01'],'a','b','recall'),[[.5,.5]])
if __name__=='__main__':unittest.main()
