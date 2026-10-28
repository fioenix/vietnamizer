import json
from pathlib import Path
import tempfile
import unittest
from benchmarks import mr_compare as m


class MRCompareTest(unittest.TestCase):
    def test_expected_rubric_and_case_identity_never_enter_generation_payload(self):
        scenario = {'id': 'MR99', 'mr_id': 'MR99', 'source': 'Văn bản.',
                    'request': 'Edit.', 'context': 'Blog.', 'family': 'blog',
                    'expected': 'SECRET_EXPECTATION', 'old_bad_candidate': 'SECRET_BAD'}
        prompt = m.prompt_for(scenario, 'RULE_BYTES')
        for hidden in ('MR99', 'SECRET_EXPECTATION', 'SECRET_BAD', 'expected', 'old_bad_candidate'):
            self.assertNotIn(hidden, prompt)
        self.assertIn('Văn bản.', prompt)
        self.assertIn('RULE_BYTES', prompt)

    def test_version_changes_only_instruction_bundle(self):
        scenario = {'source': 'Nội dung.', 'request': 'Edit.', 'context': 'Blog.'}
        a = m.prompt_for(scenario, 'OLD_RULES')
        b = m.prompt_for(scenario, 'NEW_RULES')
        self.assertEqual(a.replace('OLD_RULES', ''), b.replace('NEW_RULES', ''))

    def test_exact_28_cell_inventory_includes_all_branches(self):
        self.assertEqual(len(m.SCENARIOS), 14)
        cells = m.cells()
        self.assertEqual(len(cells), 28)
        m.validate_order(cells)
        for invalid in (cells[:-1], cells+[cells[0]], [cells[0]]*28):
            with self.assertRaises(ValueError):
                m.validate_order(invalid)
        self.assertIn('MR10-known/0.12.0', cells)
        self.assertIn('MR11-final/0.12.1', cells)

    def test_frozen_file_tamper_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'x').write_bytes(b'original')
            manifest={'fingerprints':{'x':m.sha(b'original')}}
            m.verify_files(p,manifest)
            (p/'x').write_bytes(b'changed')
            with self.assertRaises(ValueError):m.verify_files(p,manifest)

    def test_attempt_is_never_retried_and_cap_is_conservative(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            m.reserve(p,'MR01/0.12.0')
            with self.assertRaises(ValueError):m.reserve(p,'MR01/0.12.0')
            for n in range(27):(p/'attempts'/f'other-{n}').mkdir()
            with self.assertRaises(ValueError):m.reserve(p,'MR02/0.12.0')

    def test_optional_opportunity_does_not_convert_safe_case_to_failure(self):
        rows=[{'scenario':'MR11-review','version':'0.12.1','status':'passed','opportunity':False},
              {'scenario':'MR11-final','version':'0.12.1','status':'passed'}]
        self.assertEqual(m.combine(rows,'MR11','0.12.1'),'passed')
        rows[1]['status']='failed'
        self.assertEqual(m.combine(rows,'MR11','0.12.1'),'failed')
        rows[1]['status']='insufficient'
        self.assertEqual(m.combine(rows,'MR11','0.12.1'),'insufficient')
        self.assertEqual(m.combine(rows[:1],'MR11','0.12.1'),'insufficient')


if __name__ == '__main__':unittest.main()
