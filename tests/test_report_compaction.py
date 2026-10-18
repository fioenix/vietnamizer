import copy
from unittest.mock import patch
from tests.test_coverage import EvaluationCase,raw
from jev import core
from jev.transport import encoded

class CompactReportTest(EvaluationCase):
    def test_large_matrix_roundtrips_exactly(self):
        from jev.coverage import compact_report, expand_records
        r=self.evaluate(raw('\n'.join('Tôi về.' for _ in range(300))))
        self.assertEqual(r.get('ledger_encoding'),'templates-v1')
        self.assertLess(len(encoded(r)),3*1024*1024)
        for key in ('coverage','work_groups','missing'):
            expanded=expand_records(r[key])
            self.assertTrue(expanded)
            compressed=copy.deepcopy({key:expanded})
            compact_report(compressed,force=True)
            self.assertEqual(expand_records(compressed[key]),expanded)
        self.assertEqual(sum(x['missing'] for x in expand_records(r['missing'])),r['counts']['uncompleted'])
        self.assertEqual(len(expand_records(r['coverage'])),300*55)
    def test_small_reports_keep_flat_contract(self):
        r=self.evaluate()
        self.assertIsInstance(r['coverage'],list)
        self.assertIsInstance(r['missing'],list)
    def test_supplemental_span_has_explicit_disposition(self):
        d={'transmission_allowed':True,'context_review':{'reviewed':True},'sections':[{'id':'p','kind':'prose','profile':'blog','text':'Tôi về.','targets':[{'id':'custom','start':0,'end':3}]}]}
        r=self.evaluate(d,only_pattern='V1')
        self.assertEqual(r['diagnostic_targets'][0]['disposition'],'not_checked_in_full_scope')
        self.assertEqual(r['diagnostic_targets'][0]['id'],'custom')
