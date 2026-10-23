"""Feature 011: the T4 gate and structure exclusions are generated from quoted canonical text."""
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def generator():
    spec = importlib.util.spec_from_file_location('build_jev_registry', ROOT / 'scripts/build-jev-registry.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def registry():
    return {p['id']: p for p in json.loads((ROOT / 'jev/registry.json').read_text())['patterns']}


class RegistryExclusionTest(unittest.TestCase):
    def build_with(self, old, new):
        """Build the registry from a copy of the canonical sources with one SKILL.md edit."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            shutil.copytree(ROOT / 'profiles', tmp / 'profiles')
            (tmp / 'scripts').mkdir(); shutil.copy(ROOT / 'scripts/scan-tells.sh', tmp / 'scripts')
            text = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
            self.assertEqual(text.count(old), 1, old)
            (tmp / 'SKILL.md').write_text(text.replace(old, new), encoding='utf-8')
            return generator().build(tmp)

    def test_t4_gate_comes_from_its_sign(self):
        self.assertEqual(registry()['T4'].get('gate'), r',\s+và\s')
        self.assertNotIn('gate', registry()['V11'])
        with self.assertRaises(ValueError):
            self.build_with('quét bằng `,\\s+và\\s` chưa đủ', 'quét chưa đủ')

    def test_heading_exclusions_trace_to_quoted_phrases(self):
        reg = registry()
        excluded = {pid: p.get('excluded_structures') for pid, p in reg.items() if p.get('excluded_structures')}
        self.assertEqual(excluded, {'V2': ['heading'], 'V3': ['heading'], 'V5': ['heading'], 'V14': ['heading'],
                                    'V11': ['heading', 'label_value']})
        for phrase in ('tít, sapo; cụm nối', 'Không áp dụng pattern này cho tiêu đề, nhãn, mục lục hoặc ô bảng',
                       'tiêu đề, bảng biểu', 'tít, sapo, chú thích ảnh, nhãn nút, mục lục, ô bảng, checklist',
                       'Không áp dụng pattern này cho tiêu đề, dòng nhãn–giá trị (*Ngày: 22/10/2026*)'):
            with self.subTest(phrase=phrase), self.assertRaises(ValueError):
                self.build_with(phrase, 'đã bị sửa')


if __name__ == '__main__':
    unittest.main()
