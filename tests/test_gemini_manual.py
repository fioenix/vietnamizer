import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from benchmarks import gemini_manual as g


class ManualTests(unittest.TestCase):
    def test_protected_hashes_resolve_from_repo_when_terminal_is_elsewhere(self):
        with tempfile.TemporaryDirectory() as t:
            base=Path(t);repo=base/'repo';out=base/'out';elsewhere=base/'terminal'
            target=repo/'artifacts/codex/STOP_ABSTENTION';target.parent.mkdir(parents=True);target.write_text('frozen')
            out.mkdir();elsewhere.mkdir();wrapper=base/'wrapper.mjs';wrapper.write_text('// offline fixture')
            manifest={'model_requested':g.MODEL,'order':sorted(g.CELLS),'input_fingerprints':{},'driver_sha256':g.sha(g.__file__),'wrapper':str(wrapper),'wrapper_sha256':g.sha(wrapper)}
            g.save(out/'manifest.json',manifest)
            original=g.os.getcwd()
            try:
                g.os.chdir(elsewhere)
                with patch.object(g,'ROOT',repo):
                    for name in ('artifacts/codex/STOP_ABSTENTION',str(target)):
                        (out/'protected-codex.json').write_text(json.dumps({name:g.sha(target)}))
                        self.assertEqual(g.verify(out),manifest)
                    target.write_text('changed')
                    with self.assertRaisesRegex(ValueError,'Protected Codex data changed'):g.verify(out)
            finally:g.os.chdir(original)

    def test_start_cap_and_no_silent_retry(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            g.reserve(root,'R001-bare',{'public':True})
            with self.assertRaises(FileExistsError):g.reserve(root,'R001-bare',{})
            with self.assertRaises(ValueError):g.reserve(root,'../../private',{})
            for n in range(2,81):g.reserve(root,f'R{(n-1)//4+1:03}-{g.ARMS[(n-1)%4]}',{})
            with self.assertRaises(ValueError):g.reserve(root,'R001-ordinary',{})

    def test_native_tools_or_missing_terminal_are_not_completed(self):
        good=[{'type':'result','status':'SUCCESS','response':'{"text":"Bản sửa"}','usage':{'input_tokens':3,'output_tokens':2}}]
        self.assertEqual(g.parse_events(good)['status'],'completed')
        self.assertNotEqual(g.parse_events(good+[{'type':'step_update','step':{'type':'tool','name':'read_file'}}])['status'],'completed')
        self.assertNotEqual(g.parse_events(good[:-1])['status'],'completed')
        self.assertNotEqual(g.parse_events([{'type':'result','status':'SUCCESS','response':'not json'}])['status'],'completed')
        self.assertNotEqual(g.parse_events([{'type':'result','status':'SUCCESS','structured_output':{'text':'ok','extra':'no'}}])['status'],'completed')

    def test_raw_parser_fails_closed_on_unknown_or_malformed_events(self):
        self.assertNotEqual(g.parse_events([{'type':'surprise'}])['status'],'completed')
        self.assertNotEqual(g.parse_events([{'type':'result','status':'SUCCESS','structured_output':{'text':'ok'},'denied_actions':[{'kind':'read'}]}])['status'],'completed')
        self.assertNotEqual(g.parse_events([{'type':'result','status':'SUCCESS','structured_output':{'text':'ok'},'subagents':[{'id':'x'}]}])['status'],'completed')

    def test_native_event_key_and_nested_terminal_match_real_cli(self):
        events=[{'event':'init','conversation_id':'id','init':{'model':g.MODEL}},
                {'event':'step_update','step_update':{'step_type':'tool','tool_name':'finish'}},
                {'event':'result','result':{'status':'SUCCESS','conversation_id':'id','structured_output':{'text':'Bản sửa'},'usage':{'input_tokens':4}}}]
        result=g.parse_events(events)
        self.assertEqual(result['status'],'completed');self.assertEqual(result['usage'],{'input_tokens':4})
        events[1]['step_update']['tool_name']='read_file'
        self.assertNotEqual(g.parse_events(events)['status'],'completed')
        self.assertNotEqual(g.parse_events([{'type':'result','event':'error','status':'SUCCESS','structured_output':{'text':'ok'}}])['status'],'completed')

    def test_parser_reconciliation_keeps_original_failure_and_stop_and_checks_bindings(self):
        with tempfile.TemporaryDirectory() as t:
            out=Path(t);g.save(out/'manifest.json',{})
            d=g.reserve(out,'R001-bare',{});raw=d/'native';raw.mkdir()
            events=[{'event':'result','result':{'status':'SUCCESS','structured_output':{'text':'Bản sửa'}}}]
            (raw/'stdout.bin').write_bytes((json.dumps(events[0])+'\n').encode());(raw/'stderr.bin').write_bytes(b'')
            g.save(raw/'finish.json',{'exitCode':0,'timedOut':False,'streams':{n:{'sha256':g.sha(raw/n)} for n in ('stdout.bin','stderr.bin')}})
            g.save(d/'wrapper.stdout.bin',{'status':'success','structured_output':{'text':'Bản sửa'}})
            g.save(d/'result.json',{'status':'failed','tools':[],'errors':['unknown_event']})
            g.save(d/'seal.json',{str(p.relative_to(d)):g.sha(p) for p in d.rglob('*') if p.is_file()})
            g.save(out/'STOP.json',{'cell':d.name})
            original=g.sha(d/'result.json');stop=g.sha(out/'STOP.json')
            with self.assertRaises(ValueError):g.completed(out)
            parsed=g.checked_reparse(d)
            proof={'original_seal_sha256':g.sha(d/'seal.json'),'manifest_sha256':g.sha(out/'manifest.json'),'parser_sha256':g.sha(g.__file__),'parsed_result':parsed,'stop_sha256':stop}
            q=out/'reconciliations'/f'{d.name}.json';g.save(q,proof)
            self.assertEqual(g.completed(out),{d.name});g.check_stops(out,{d.name})
            self.assertEqual(g.sha(d/'result.json'),original);self.assertEqual(g.sha(out/'STOP.json'),stop)
            g.save(out/'STOP-R002-bare.json',{'cell':'R002-bare'})
            with self.assertRaises(ValueError):g.check_stops(out,{d.name})
            proof['parsed_result']['text']='changed';q.write_text(json.dumps(proof))
            with self.assertRaisesRegex(ValueError,'Reconciliation result drift'):g.completed(out)

    def test_credit_guard_rejects_paid_routes_without_mutating_settings(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'settings.json'
            p.write_text('{"useG1Credits":true}')
            original=p.read_bytes()
            with self.assertRaises(ValueError):g.credit_check(p)
            self.assertEqual(p.read_bytes(),original)
            p.write_text('{"modelProvider":"gemini"}')
            with self.assertRaises(ValueError):g.credit_check(p)
            p.write_text('{}')
            self.assertEqual(g.credit_check(p)['route'],'subscription_default')

    def test_resume_accepts_only_sealed_success(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);cell=g.reserve(root,'R001-bare',{})
            with self.assertRaises(ValueError):g.completed(root)
            (cell/'result.json').write_text(json.dumps({'status':'failed'}))
            with self.assertRaises(ValueError):g.completed(root)

    def test_fake_process_retains_both_layers_and_resumes_only_unstarted_cells(self):
        with tempfile.TemporaryDirectory() as t:
            out=Path(t);(out/'manifest.json').write_text('{}');(out/'inputs/prompts').mkdir(parents=True)
            for c in ('R001-bare','R001-ordinary'):(out/'inputs/prompts'/f'{c}.txt').write_text('public prompt')
            manifest={'order':['R001-bare','R001-ordinary'],'node':'fake-node','wrapper':'fake-wrapper'}
            starts=[]
            class FakeProcess:
                pid=999999999
                def __init__(self,args,stdin,stdout,stderr,cwd,env,**kw):
                    starts.append(args);raw=cwd/'.native-raw';raw.mkdir()
                    event={'type':'result','status':'SUCCESS','structured_output':{'text':'Bản sửa'},'usage':{'input_tokens':3}}
                    (raw/'stdout.bin').write_bytes((json.dumps(event)+'\n').encode());(raw/'stderr.bin').write_bytes(b'raw diagnostic\xff')
                    g.save(raw/'finish.json',{'streams':{n:{'sha256':g.sha(raw/n)} for n in ('stdout.bin','stderr.bin')},'exitCode':0,'timedOut':False})
                    stdout.write(b'{"status":"success","evidence":{"session_resumed":false}}');stderr.write(b'normalized diagnostic')
                def wait(self,timeout):return 0
            with patch.object(g,'verify',return_value=manifest),patch.object(g,'credit_check',return_value={'route':'subscription_default'}),patch.object(g.subprocess,'Popen',FakeProcess):
                g.run(out,1);g.run(out,1);g.run(out,1)
            self.assertEqual(len(starts),2)
            self.assertEqual(len(g.completed(out)),2)
            self.assertEqual((out/'attempts/R001-bare/native/stderr.bin').read_bytes(),b'raw diagnostic\xff')
            (out/'attempts/R001-bare/native/stderr.bin').write_bytes(b'tampered')
            with self.assertRaises(ValueError):g.completed(out)

    def test_interruption_kills_remaining_group_before_sealing_partial_raw(self):
        with tempfile.TemporaryDirectory() as t:
            out=Path(t);(out/'manifest.json').write_text('{}');(out/'inputs/prompts').mkdir(parents=True)
            (out/'inputs/prompts/R001-bare.txt').write_text('public prompt')
            manifest={'order':['R001-bare'],'node':'fake','wrapper':'fake'}
            class Interrupted:
                pid=999999998
                def __init__(self,args,cwd,**kw):
                    self.calls=0;raw=cwd/'.native-raw';raw.mkdir();(raw/'stdout.bin').write_bytes(b'partial')
                def wait(self,timeout):
                    self.calls+=1
                    if self.calls==1:raise KeyboardInterrupt()
                    return 0
            with patch.object(g,'verify',return_value=manifest),patch.object(g,'credit_check',return_value={}),patch.object(g.subprocess,'Popen',Interrupted),patch.object(g.os,'killpg') as kill:
                with self.assertRaises(ValueError):g.run(out,1)
                self.assertEqual([c.args[1] for c in kill.call_args_list],[g.signal.SIGTERM,g.signal.SIGKILL])
            self.assertTrue((out/'STOP.json').is_file())
            self.assertFalse((out/'RUNNING.lock').exists())
            self.assertEqual((out/'attempts/R001-bare/native/stdout.bin').read_bytes(),b'partial')


if __name__=='__main__':unittest.main()
