import unittest
from tests.test_coverage import EvaluationCase, raw
from jev.core import prepare

class ModelTest(EvaluationCase):
    def test_compact_missing_manifest_expands_exact_gaps(self):
        from unittest.mock import patch
        with patch('jev.core.MAX_REQUESTS',1),patch('jev.core.MAX_QUESTIONS',1):
            r=self.evaluate(only_pattern='V1')
        self.assertEqual(r['counts']['required'],4)
        self.assertEqual(r['counts']['validated'],1)
        gap=0
        for group in r['missing']:
            keys={(n,k) for n in range(*group['subject_range']) for k in group['recipe_keys']}
            keys-=set(map(tuple,group['validated_keys']))
            self.assertEqual(len(keys),group['missing']);gap+=len(keys)
        self.assertEqual(gap,3)
    def test_unresolved_region_not_certified_sentence(self):
        r=prepare(raw('Tôi chưa biết… Có lẽ mai.'))
        self.assertEqual(r['counts']['sentences'],0)
        self.assertTrue(r['counts']['provisional'])
        self.assertTrue(r['unresolved'])
    def test_cancel_produces_incomplete_without_echo(self):
        def fake(*_):raise KeyboardInterrupt()
        r=self.evaluate(transport=fake,only_pattern='V1')
        self.assertEqual(r['status'],'incomplete')
        self.assertEqual(r['receipts'][0]['status'],'cancelled')
        self.assertEqual(r['counts']['validated'],0)
