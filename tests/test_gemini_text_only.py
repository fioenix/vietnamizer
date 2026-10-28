from pathlib import Path
import tempfile
import unittest
import json
from unittest.mock import patch
from benchmarks import gemini_text_only as t
from benchmarks import gemini_manual as g

class TextOnlyTests(unittest.TestCase):
    def test_init_is_mandatory_and_tools_cannot_be_inherited(self):
        good={'event':'init','init':{'agent':t.AGENT,'model':g.MODEL,'tools':['finish'],'permission_mode':'request-review'}}
        t.validate_init(good)
        for patch in ({'agent':'default'},{'tools':['finish','read_file']},{'tools':None},{'model':'other'}):
            with self.assertRaises(ValueError):t.validate_init({'event':'init','init':{**good['init'],**patch}})

    def test_new_workspace_contains_only_frozen_agent_definition(self):
        with tempfile.TemporaryDirectory() as s:
            out=Path(s)/'out';out.mkdir();definition=out/'agent.md';definition.write_text('public definition')
            cwd=t.make_workspace(Path(s)/'work','R001-bare',definition)
            self.assertEqual([str(p.relative_to(cwd)) for p in cwd.rglob('*') if p.is_file()],['.agents/agents/'+t.AGENT+'.md'])
            with self.assertRaises(FileExistsError):t.make_workspace(Path(s)/'work','R001-bare',definition)

    def test_history_check_rejects_modified_diagnostic_evidence(self):
        with tempfile.TemporaryDirectory() as s:
            p=Path(s)/'history';p.write_text('old raw');snapshot={str(p):g.sha(p)}
            t.check_history(snapshot)
            p.write_text('changed')
            with self.assertRaises(ValueError):t.check_history(snapshot)

    def test_matched_capability_contract_requires_recovered_nonce_and_sealed_streams(self):
        with tempfile.TemporaryDirectory() as s:
            root=Path(s);negative=root/'diag';positive=negative/'read-file-control';positive.mkdir(parents=True)
            agent=root/'agent.md';definition='---\nname: '+t.AGENT+'\ntools:\n  - finish\n---\nSame body\n';agent.write_text(definition)
            (positive/'agent.md').write_text(definition.replace('name: '+t.AGENT,'name: vietnamizer-benchmark-read-file-control').replace('tools:\n  - finish','tools:\n  - finish\n  - read_file'))
            (negative/'expected-fixture.txt').write_text('PUBLIC_TOKEN\n');g.save(negative/'plan.json',{'read_target':'/public/fixture.txt'})
            meta=root/'meta';g.save(meta/'native-capability-blocker.json',{'definition_sha256':g.sha(agent)})
            for p,who,text,tools in [(negative,t.AGENT,'UNAVAILABLE',[{'name':'finish'}]),(positive,'vietnamizer-benchmark-read-file-control','PUBLIC_TOKEN',[{'name':'read_file'},{'name':'finish'}])]:
                (p/'prompt.txt').write_text('same public task')
                raw=p/'native';raw.mkdir()
                events=[{'event':'init','init':{'agent':who,'model':g.MODEL,'tools':['view_file','finish']}}]
                if p==positive:events.append({'event':'step_update','step_update':{'tool_name':'read_file','state':'DONE','tool_info':{'parameters':{'Path':'/public/fixture.txt'}}}})
                events.append({'event':'result','result':{'status':'SUCCESS','structured_output':{'text':text}}})
                (raw/'stdout.bin').write_text('\n'.join(json.dumps(e) for e in events)+'\n');(raw/'stderr.bin').write_bytes(b'')
                g.save(raw/'finish.json',{'exitCode':0,'timedOut':False,'streams':{n:{'sha256':g.sha(raw/n)} for n in ('stdout.bin','stderr.bin')}})
                g.save(p/'wrapper.stdout.bin',{'status':'success','structured_output':{'text':text},'tool_calls':tools,'evidence':{'session_resumed':False,'agy_version':'1.4.7'}})
            with patch.object(t,'DIAGNOSTICS',negative),patch.object(t,'AGENT_PATH',agent),patch.object(t,'BASE',meta):
                contract=t.capability_contract();self.assertEqual(contract['advertised_registry'],['view_file','finish'])
                (negative/'expected-fixture.txt').write_text('OTHER_TOKEN\n')
                with self.assertRaises(ValueError):t.capability_contract()
                (negative/'expected-fixture.txt').write_text('PUBLIC_TOKEN\n')
                (positive/'native/stdout.bin').write_bytes(b'tampered')
                with self.assertRaises(ValueError):t.capability_contract()

    def test_fake_native_trial_verifies_init_and_persists_raw_outside_workspace(self):
        with tempfile.TemporaryDirectory() as s:
            out=Path(s)/'epoch';out.mkdir();g.save(out/'manifest.json',{});(out/'agent.md').write_text('public agent')
            (out/'inputs/prompts').mkdir(parents=True);(out/'inputs/prompts/R001-bare.txt').write_text('public prompt')
            m={'workspace_root':str(Path(s)/'work'),'node':'fake','wrapper':'fake'}
            class Fake:
                def __init__(self,args,stdout,stderr,cwd,env,**kw):
                    raw=Path(env['VIETNAMIZER_RAW_DIR']);raw.mkdir()
                    self.pid=999999999
                    init={'event':'init','init':{'agent':t.AGENT,'model':g.MODEL,'tools':['finish'],'permission_mode':'request-review'}}
                    result={'event':'result','result':{'status':'SUCCESS','structured_output':{'text':'Bản sửa'}}}
                    (raw/'stdout.bin').write_text(json.dumps(init)+'\n'+json.dumps(result)+'\n');(raw/'stderr.bin').write_bytes(b'')
                    g.save(raw/'init.json',init);g.save(raw/'finish.json',{'exitCode':0,'timedOut':False,'guard_ok':True,'streams':{n:{'sha256':g.sha(raw/n)} for n in ('stdout.bin','stderr.bin')}})
                    stdout.write(json.dumps({'status':'success','structured_output':{'text':'Bản sửa'}}).encode())
                    assert not raw.is_relative_to(cwd)
                def wait(self,timeout):return 0
            with patch.object(g,'credit_check',return_value={}),patch.object(t.subprocess,'Popen',Fake):r=t.trial(out,m,'R001-bare')
            self.assertEqual(r['status'],'completed');self.assertEqual(t.done_cells(out),{'R001-bare'})
            self.assertTrue((out/'capability-verification.json').exists())

if __name__=='__main__':unittest.main()
