"""Pilot contracts: never turn missing, contaminated or mismatched evidence into completion."""
import copy
import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class PilotContracts(unittest.TestCase):
    def setUp(self):
        path = ROOT / 'benchmarks/editorial_pilot.py'
        self.assertTrue(path.exists(), 'pilot orchestration is not implemented')
        spec = importlib.util.spec_from_file_location('editorial_pilot', path)
        self.p = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.p)

    def codex(self, *items):
        return '\n'.join(json.dumps(x) for x in [
            {'type':'thread.started','thread_id':'trial-1'},
            *[{'type':'item.completed','item':x} for x in items],
            {'type':'turn.completed','usage':{'input_tokens':123,'output_tokens':12}},
        ])

    def test_codex_requires_terminal_and_nonempty_output(self):
        r=self.p.parse_codex(self.codex({'type':'agent_message','text':'Đã giao hàng.'}))
        self.assertEqual(('completed','Đã giao hàng.'),(r['status'],r['text']))
        self.assertEqual('failed',self.p.parse_codex(self.codex())['status'])
        self.assertEqual('failed',self.p.parse_codex('{"type":"thread.started"}')['status'])

    def test_codex_tool_use_is_contamination_even_with_final_output(self):
        r=self.p.parse_codex(self.codex({'type':'command_execution','command':'cat SKILL.md'},
                                      {'type':'agent_message','text':'Có kết quả.'}))
        self.assertEqual('contaminated',r['status'])

    def test_startup_warning_is_not_a_tool_call(self):
        raw=self.codex({'type':'error','message':'Under-development features enabled'},
                       {'type':'agent_message','text':'Bản cuối.'})
        self.assertEqual('completed',self.p.parse_codex(raw)['status'])

    def test_normalization_never_upgrades_nonzero_exit(self):
        raw=self.codex({'type':'error','message':'startup warning'},
                       {'type':'agent_message','text':'Bản cuối.'})
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp); d=out/'attempts'/'codex-x-bare';d.mkdir(parents=True)
            (d/'stdout.txt').write_text(raw)
            for code,expected in ((0,'completed'),(1,'contaminated'),(None,'contaminated')):
                (d/'result.json').write_text(json.dumps({'cell':'codex/x/bare',
                    'status':'contaminated','text':'Bản cuối.','exit_code':code}))
                self.assertEqual(expected,self.p.records(out)[0]['status'])

    def test_agybird_partial_and_tool_calls_never_complete(self):
        base={'status':'success','response':'Bản cuối.','tool_calls':[], 'subagents':[],
              'evidence':{'session_resumed':False},'conversation_id':'c1','usage':{}}
        self.assertEqual('completed',self.p.parse_agy(json.dumps(base))['status'])
        for change in ({'status':'partial'},{'tool_calls':[{'name':'read_file','status':'completed'}]},
                       {'subagents':[{'role':'writer'}]}, {'evidence':{'session_resumed':True}},
                       {'response':''}):
            d=dict(base,**change)
            self.assertNotEqual('completed',self.p.parse_agy(json.dumps(d))['status'])

    def test_schema_finish_marker_is_not_external_tool_use(self):
        e={'status':'success','structured_output':{'text':'Bản cuối.'},
           'tool_calls':[{'name':'finish','status':'active'}], 'subagents':[],
           'evidence':{'session_resumed':False}}
        self.assertEqual('completed',self.p.parse_agy(json.dumps(e))['status'])
        e['tool_calls'].append({'name':'read_file','status':'completed'})
        self.assertEqual('contaminated',self.p.parse_agy(json.dumps(e))['status'])

    def test_bounded_batch_stops_scheduling_after_failure(self):
        seen=[]
        def failed(out,cell):
            seen.append(cell)
            return {'cell':cell,'status':'failed'}
        with patch.object(self.p,'run_one',side_effect=failed):
            rows=self.p.run_batch(Path('/tmp'),['a','b','c','d'],4)
        self.assertLessEqual(len(seen),2)
        self.assertEqual(len(seen),len(set(seen)))
        self.assertTrue(all(x['status']=='failed' for x in rows))

    def test_recorded_host_approval_block_prevents_provider_start(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            (out/'ANTIGRAVITY_BLOCKED').write_text('automatic approval review: isolation not verified')
            try:
                self.p.run_one(out,'agy/P01/bare')
            except ValueError as exc:
                self.assertIn('blocked',str(exc))
            except FileNotFoundError:
                pass  # No provider can start in this intentionally empty task directory.
            self.assertFalse((out/'attempts').exists(), 'blocked route created an attempt')

    def test_baseline_gets_source_and_context_but_not_skill_or_labels(self):
        c={'id':'x','source':'Nội dung.','audience':'Đồng nghiệp','purpose':'Thông báo',
           'family':'phoi-hop-cong-viec','expected':['PRIVATE_LABEL']}
        for arm in ('bare','ordinary'):
            prompt=self.p.make_prompt(c,arm,'PRIVATE_SKILL')
            self.assertIn('Nội dung.',prompt)
            self.assertIn('Đồng nghiệp',prompt)
            self.assertNotIn('PRIVATE_LABEL',prompt)
            self.assertNotIn('PRIVATE_SKILL',prompt)
        self.assertIn('PRIVATE_SKILL',self.p.make_prompt(c,'vietnamizer','PRIVATE_SKILL'))

    def test_duplicate_cells_rejected_in_report(self):
        rec={'cell':'codex/x/bare','status':'completed','text':'X.'}
        with self.assertRaises(ValueError): self.p.summarize([rec,copy.deepcopy(rec)],['codex/x/bare'])

    def test_missing_and_failed_cells_not_success(self):
        r=self.p.summarize([{'cell':'a','status':'completed','text':'A.'},
                            {'cell':'b','status':'failed','text':''}],['a','b','c'])
        self.assertEqual((1,1,1),(r['completed'],r['failed'],r['missing']))
        self.assertFalse(r['generation_complete'])
        self.assertEqual('pending',r['semantic_review'])

    def test_resume_rejects_manifest_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'manifest.json'
            self.p.freeze_manifest(path,{'corpus':'a','bundle':'x'})
            self.p.freeze_manifest(path,{'corpus':'a','bundle':'x'})
            with self.assertRaises(ValueError): self.p.freeze_manifest(path,{'corpus':'b','bundle':'x'})

    def test_paid_route_or_credits_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'settings.json'
            p.write_text('{}')
            self.assertTrue(self.p.credit_preflight(p)['included_quota_only'])
            for config in ({'useG1Credits':True},{'useG1Credits':'on'},
                           {'modelProvider':'gemini'},{'useG1Credits':None},{'modelProvider':None}):
                p.write_text(json.dumps(config))
                with self.assertRaises(ValueError): self.p.credit_preflight(p)
            p.write_text('broken')
            with self.assertRaises(ValueError): self.p.credit_preflight(p)

    def test_timeout_kills_descendants_holding_pipes(self):
        child="import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);print('CHILD_STARTED',flush=True);time.sleep(30)"
        code="import subprocess,sys;subprocess.run([sys.executable,'-c',"+repr(child)+"])"
        started=time.monotonic()
        with self.assertRaises(subprocess.TimeoutExpired) as caught:
            self.p.execute([sys.executable,'-c',code],'',Path(tempfile.gettempdir()),os.environ.copy(),0.5)
        self.assertIn('CHILD_STARTED',caught.exception.stdout)
        self.assertLess(time.monotonic()-started,3)

    def test_timeout_kills_detached_pipe_descendant(self):
        with tempfile.TemporaryDirectory() as tmp:
            pidfile=Path(tmp)/'child.pid'
            child="import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(30)"
            code=("import subprocess,sys,time;from pathlib import Path;"
                  "p=subprocess.Popen([sys.executable,'-c',"+repr(child)+"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);"
                  "Path("+repr(str(pidfile))+").write_text(str(p.pid));time.sleep(30)")
            with self.assertRaises(subprocess.TimeoutExpired):
                self.p.execute([sys.executable,'-c',code],'',Path(tmp),os.environ.copy(),0.5)
            pid=int(pidfile.read_text())
            stopped=False
            for _ in range(20):
                try: os.kill(pid,0)
                except ProcessLookupError:
                    stopped=True
                    break
                time.sleep(0.05)
            if not stopped:
                import signal
                os.kill(pid,signal.SIGKILL)
            self.assertTrue(stopped, 'descendant PID remains after timeout')

    def test_prompt_injection_is_data_not_a_shell_argument(self):
        c={'id':'x','source':'$(touch /tmp/unsafe) `echo bad`','audience':'Reader',
           'purpose':'Edit','family':'huong-dan-ky-thuat'}
        p=self.p.make_prompt(c,'bare','')
        self.assertIn('$(touch /tmp/unsafe)',p)
        args=self.p.codex_args(Path('/tmp/pilot'))
        self.assertNotIn(p,args)
        self.assertEqual('-',args[-1])
        self.assertIn('forced_login_method="chatgpt"',args)

if __name__=='__main__': unittest.main()
