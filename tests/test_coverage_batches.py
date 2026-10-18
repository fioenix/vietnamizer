import unittest
from unittest.mock import patch
from tests.test_coverage import EvaluationCase, raw
from jev import core


class BatchTest(EvaluationCase):
    def test_40_sentences_detected_despite_16_target_window(self):
        text=' '.join(f'Câu số {i}.' for i in range(40))
        with patch('jev.core.MAX_QUESTIONS',3):
            r=self.evaluate(raw(text),only_pattern='V1')
        self.assertEqual(r['counts']['sentences'],40)
        self.assertEqual(r['counts']['required'],80)
        self.assertEqual(r['counts']['validated'],80)
        self.assertTrue(all(len(p['questions'])<=3 and len(p['state']['targets'])<=16 for p in self.calls))
        self.assertTrue(all(p['state']['paragraph']==text for p in self.calls))

    def test_more_than_32_paragraphs_inventory_survives_budget(self):
        text='\n'.join(f'Câu số {i}.' for i in range(40))
        r=self.evaluate(raw(text),only_pattern='V1')
        self.assertEqual(r['counts']['sentences'],40)
        self.assertEqual(len(self.calls),32)
        self.assertEqual(r['counts']['validated'],64)
        self.assertEqual(r['counts']['uncompleted'],16)
        self.assertEqual(r['status'],'incomplete')
        self.assertTrue(r['missing'])

    def test_question_recipes_cross_batches(self):
        with patch('jev.core.MAX_QUESTIONS',1):
            r=self.evaluate(only_pattern='V1')
        self.assertEqual(len(self.calls),4)
        self.assertEqual(r['counts']['validated'],4)
        self.assertTrue(all(s['answers_complete'] for s in r['sentences']))

    def test_too_large_required_context_is_visible(self):
        r=self.evaluate(raw('a'*49000),only_pattern='V1')
        self.assertEqual(self.calls,[])
        self.assertEqual(r['counts']['uncompleted'],2)
        self.assertEqual(r['missing'][0]['reason'],'context_too_large')

    def test_32_call_budget_not_reset(self):
        with patch('jev.core.MAX_QUESTIONS',1):
            r=self.evaluate(raw(' '.join('Tôi về.' for _ in range(40))),only_pattern='V1')
        self.assertEqual(len(self.calls),32)
        self.assertEqual(r['counts']['validated'],32)
        self.assertEqual(r['counts']['uncompleted'],48)
        self.assertFalse(r['evaluation_complete'])
        self.assertEqual(sum(s['validated'] for s in r['sentences']),32)

    def test_target_window_shrinks_without_chopping_parent(self):
        # One target+question can fit; all 16 duplicate target strings cannot.
        text=' '.join(('A'*500+'.') for _ in range(16))
        with patch('jev.core.MAX_REQUEST',12000):
            r=self.evaluate(raw(text),only_pattern='V1')
        self.assertEqual(r['status'],'evaluated')
        self.assertTrue(all(p['state']['paragraph']==text for p in self.calls))
        self.assertTrue(all(len(core.encoded(p))<=12000 for p in self.calls))
