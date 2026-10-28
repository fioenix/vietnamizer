import json
from pathlib import Path
import tempfile
import sys
import unittest

from benchmarks import mindfio_pilot as m


def events(message=None, extra=None):
    rows = [
        {'type': 'thread.started', 'thread_id': 'fresh-session'},
        {'type': 'item.completed', 'item': {'type': 'agent_message', 'text': message or json.dumps({'text': 'Bản sửa.'})}},
        {'type': 'turn.completed', 'usage': {'input_tokens': 10, 'output_tokens': 3}},
    ]
    if extra:
        rows.insert(1, extra)
    return '\n'.join(json.dumps(x) for x in rows)


class MindfioPilotTest(unittest.TestCase):
    def test_strict_completion_requires_json_text_schema_and_complete_turn(self):
        result = m.parse(events())
        self.assertEqual(result['text'], 'Bản sửa.')
        for raw in (events('Plain prose'), events('{"text":"ok","extra":1}'),
                    events('{"text":""}'), '\n'.join(events().splitlines()[:-1]),
                    events() + '\nnot-json'):
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):
                    m.parse(raw)

    def test_actual_tool_event_rejected_even_if_final_exists(self):
        for row in ({'type': 'item.completed', 'item': {'type': 'command_execution', 'command': 'ls'}},
                    {'type': 'item.started', 'item': {'type': 'mcp_tool_call', 'tool': 'read'}},
                    {'type': 'error', 'message': 'failed'}):
            with self.assertRaises(ValueError):
                m.parse(events(extra=row))

    def test_exact_observed_cli_development_warning_is_not_a_tool_or_turn_failure(self):
        warning = 'Under-development features enabled: skip_host_skill_discovery. Under-development features are incomplete and may behave unpredictably. To suppress this warning, set `suppress_unstable_features_warning = true` in /tmp/codex-test/config.toml.'
        row = {'type': 'item.completed', 'item': {'type': 'error', 'message': warning}}
        self.assertEqual(m.parse(events(extra=row))['native_warnings'], [warning])
        row['item']['message'] = 'Actual tool/transport error'
        with self.assertRaises(ValueError):
            m.parse(events(extra=row))

    def test_profile_only_in_two_designated_arms_and_bundle_only_in_skill_arms(self):
        for arm in m.ARMS:
            prompt = m.prompt_for('NGUON', arm, 'HO_SO_DA_CHOT', 'BO_QUY_TAC')
            self.assertEqual('HO_SO_DA_CHOT' in prompt, arm != 'vietnamizer_core')
            self.assertEqual('BO_QUY_TAC' in prompt, arm != 'ordinary_profile')
            self.assertIn('NGUON', prompt)

    def test_frozen_file_tamper_is_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)
            (p / 'input.txt').write_text('nguồn')
            manifest = {'fingerprints': {'input.txt': m.sha((p/'input.txt').read_bytes())}}
            m.verify_files(p, manifest)
            (p / 'input.txt').write_text('nguồn đổi')
            with self.assertRaises(ValueError):
                m.verify_files(p, manifest)

    def test_planned_cells_are_exactly_twelve_and_reject_duplicates(self):
        cells = [f'{cid}/{arm}' for cid in m.CASES for arm in m.ARMS]
        m.validate_order(cells)
        for bad in (cells + ['M01/ordinary_profile'], cells[:-1], [cells[0]] * 12):
            with self.assertRaises(ValueError):
                m.validate_order(bad)

    def test_diff_metric_orientation_and_unchanged_oracle(self):
        self.assertEqual(m.metrics('abc', 'abc')['character_change_fraction'], 0)
        result = m.metrics('abc', 'abcd')
        self.assertAlmostEqual(result['character_change_fraction'], 1/7)
        self.assertAlmostEqual(result['length_change_fraction'], 1/3)
        self.assertEqual(result['new_chars'], 4)

    def test_resume_never_retries_an_existing_attempt(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)
            (p/'attempts'/'M01--ordinary_profile').mkdir(parents=True)
            with self.assertRaises(ValueError):
                m.reserve_attempt(p, 'M01/ordinary_profile')

    def test_native_capture_preserves_binary_bytes_and_nonzero_exit(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)
            (p/'stdin.txt').write_bytes(b'input\r\n')
            code = m.execute_native([sys.executable, '-c',
                'import sys;sys.stdout.buffer.write(sys.stdin.buffer.read()+b"\\x00\\r\\n");sys.stderr.buffer.write(b"err\\r\\n");sys.exit(7)'],
                p/'stdin.txt', p, {}, p, 5)
            self.assertEqual(code, 7)
            self.assertEqual((p/'stdout.txt').read_bytes(), b'input\r\n\x00\r\n')
            self.assertEqual((p/'stderr.txt').read_bytes(), b'err\r\n')


if __name__ == '__main__':
    unittest.main()
