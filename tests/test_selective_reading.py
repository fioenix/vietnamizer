"""Selective catalogs remain canonical inputs to actual package/registry consumers."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from tests import test_distribution as distribution

ROOT = Path(__file__).resolve().parents[1]
CATALOGS = {
    'references/loi-thieu-tu.md': [f'V{i}' for i in range(1, 9)] + ['V20'],
    'references/loi-cau-va-quan-he.md': [f'V{i}' for i in range(9, 19)] + ['V24', 'V25'],
    'references/loi-tu-va-loi-dan.md': ['V19', 'V21', 'V22', 'V23'],
    'references/typography.md': [f'T{i}' for i in range(1, 7)],
}


class SelectiveReadingTest(unittest.TestCase):
    def test_registry_binds_each_relocated_pattern_to_its_catalog(self):
        spec = importlib.util.spec_from_file_location('selective_generator', ROOT / 'scripts/build-jev-registry.py')
        generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator)
        patterns = {p['id']: p for p in generator.build()['patterns']}
        self.assertEqual(len(patterns), 55)
        for path, ids in CATALOGS.items():
            for pid in ids:
                with self.subTest(pattern=pid):
                    self.assertEqual(patterns[pid]['source'], path)

    def test_missing_canonical_catalog_prevents_packaging(self):
        helper = distribution.DistributionTest()
        with tempfile.TemporaryDirectory() as tmp:
            repo = helper.fixture(Path(tmp))
            catalog = repo / 'references/loi-thieu-tu.md'
            self.assertTrue(catalog.is_file(), 'completion catalog must be shipped')
            catalog.unlink()
            result = helper.package(repo)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((repo / 'dist/vietnamizer-plugin.zip').exists())

    def test_duplicate_pattern_in_another_catalog_prevents_packaging(self):
        helper = distribution.DistributionTest()
        with tempfile.TemporaryDirectory() as tmp:
            repo = helper.fixture(Path(tmp))
            source = repo / 'references/loi-thieu-tu.md'
            self.assertTrue(source.is_file(), 'completion catalog must be shipped')
            target = repo / 'references/loi-tu-va-loi-dan.md'
            target.write_text(target.read_text() + '\n' + source.read_text())
            self.assertNotEqual(helper.package(repo).returncode, 0)
