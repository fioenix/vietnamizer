"""Feature 010: tier 3 signals come from scan-tells.sh, kept only where the canonical section supports them."""
import json
import re
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def registry():
    return {p['id']: p for p in json.loads((ROOT / 'jev/registry.json').read_text())['patterns']}


def scan_expressions():
    found = {}
    for line in (ROOT / 'scripts/scan-tells.sh').read_text(encoding='utf-8').splitlines():
        m = re.match(r'''scan "([VTBK]\d+) [^"]*" '([^']*)''', line.strip())
        if m:
            found[m.group(1)] = m.group(2).replace('[[:space:]]', r'\s')
    return found


def section(pid):
    text = (ROOT / registry()[pid]['source']).read_text(encoding='utf-8')
    return re.search(r'^### ' + pid + r'\..*?(?=^### |\Z)', text, re.M | re.S).group(0)


def literal(signal):
    # Strip anchors and the non-capturing wrappers the generator adds when it splits a group.
    return re.sub(r'\(\?:([^()]*)\)', r'\1', signal).lstrip('^')


class RegistrySignalTest(unittest.TestCase):
    def test_signals_are_grounded_alternatives_of_scan_tells(self):
        reg = registry(); scans = scan_expressions()
        self.assertEqual(set(scans), {'T2', 'T4', 'T5', 'V9', 'V11', 'V12', 'V15', 'V16', 'V18'})
        for pid, entry in reg.items():
            for signal in entry.get('signals', []):
                with self.subTest(pattern=pid, signal=signal):
                    self.assertIn(pid, scans)
                    self.assertTrue(re.search(literal(signal), section(pid), re.I),
                                    'a signal must match its own canonical section')
                    # Escapes such as \\n or \\t are not words of the expression.
                    for word in re.findall(r'[^\W\d_]+', re.sub(r'\\.', '', literal(signal))):
                        self.assertIn(word, scans[pid], 'a signal may only use words of its scan-tells expression')

    def test_expected_kept_and_dropped_alternatives(self):
        reg = registry()
        kept = {pid: {literal(s) for s in e.get('signals', [])} for pid, e in reg.items()}
        self.assertEqual(set(p for p, s in kept.items() if s), {'T2', 'T4', 'T5', 'V9', 'V11', 'V12', 'V15'})
        self.assertNotIn(r'\*{0,2}Thông qua', kept['V9'])
        self.assertIn(r'\*{0,2}Trong quá trình', kept['V9'])
        self.assertFalse({'Thêm vào đó,', 'Chính vì thế,'} & kept['V12'])
        self.assertIn('Hơn nữa,', kept['V12'])
        self.assertNotIn('triển khai thực hiện', kept['V15'])
        self.assertEqual(kept['V16'], set()); self.assertEqual(kept['V18'], set())
        self.assertEqual(kept['T4'], {', và '})

    def test_signals_compile_and_stay_linear(self):
        adversarial = ('**' * 50000 + ' ' * 50000 + ', ' * 100000 + '#' * 100000 + '\n' * 500000)[:1 << 20]
        for pid, entry in registry().items():
            for signal in entry.get('signals', []):
                with self.subTest(pattern=pid, signal=signal):
                    compiled = re.compile(signal, re.M)
                    start = time.monotonic()
                    compiled.search(adversarial)
                    self.assertLess(time.monotonic() - start, 1)

    def test_signals_keep_grep_line_semantics(self):
        # scan-tells.sh runs grep, which never matches across a line break; signals must not either.
        reg = registry()
        for pid, entry in reg.items():
            for signal in entry.get('signals', []):
                with self.subTest(pattern=pid, signal=signal):
                    self.assertNotIn(r'\s', signal)
                    self.assertFalse(re.search(r'\[\^(?![^\]]*\\n)', signal), 'negated classes must exclude newlines')
        t5 = [re.compile(x, re.M) for x in reg['T5']['signals']]
        self.assertFalse(any(c.search('- **Nhãn\nvẫn chưa đóng:** giá trị') for c in t5))
        self.assertTrue(any(c.search('  - **Nhãn:** giá trị') for c in t5))


if __name__ == '__main__':
    unittest.main()
