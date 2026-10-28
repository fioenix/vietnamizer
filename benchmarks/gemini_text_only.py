"""Separate, owner-approved text-only Gemini epoch; historical runs are read-only."""
from pathlib import Path
import argparse
import json
import os
import random
import shutil
import signal
import subprocess
import sys
import tempfile
import time
if not __package__:sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from benchmarks import gemini_manual as g

AGENT='vietnamizer-benchmark-text-only'
BASE=g.ROOT/'artifacts/014-gemini-text-only-20261026'
DEFAULT=BASE/'epoch-v3'
AGENT_PATH=Path.home()/'.gemini/config/agents'/f'{AGENT}.md'
DIAGNOSTICS=g.ROOT/'artifacts/014-gemini-capability-diagnosis-20261026'

def check_history(snapshot):
    for name,h in snapshot.items():
        if g.sha(g.ROOT/name)!=h:raise ValueError('Protected historical file changed: '+name)

def validate_init(e,contract=None):
    x=e.get('init',{})
    if (e.get('event',e.get('type'))!='init' or x.get('agent')!=AGENT or x.get('model')!=g.MODEL or
        not isinstance(x.get('tools'),list) or x.get('permission_mode')!='request-review'):
        raise ValueError('Native CLI did not apply the text-only agent/model/tools/permissions')
    if contract:
        if (contract['schema']!='verified-registry-v1' or contract['agent']!=AGENT or contract['model']!=g.MODEL or
            contract['effective_agent_tools']!=['finish'] or sorted(x['tools'])!=sorted(contract['advertised_registry'])):raise ValueError('Unverified native tool registry')
    elif any(n!='finish' for n in x['tools']):raise ValueError('Capability contract required for global tool registry')

def capability_contract():
    """Deterministic paired-control validation, no model requests."""
    negative=DIAGNOSTICS;positive=DIAGNOSTICS/'read-file-control';rows=[]
    for p in (negative,positive):
        finish=g.read(p/'native/finish.json');wrapper=g.read(p/'wrapper.stdout.bin')
        if finish['exitCode']!=0 or finish['timedOut'] or finish.get('signal') or finish.get('spawnError') or wrapper['status']!='success' or wrapper.get('permission_requests') or wrapper.get('subagents') or wrapper['evidence']['session_resumed']:raise ValueError('Incomplete capability diagnostic')
        for name,item in finish['streams'].items():
            if g.sha(p/'native'/name)!=item['sha256']:raise ValueError('Diagnostic raw drift')
        events=[json.loads(l) for l in (p/'native/stdout.bin').read_text().splitlines() if l.strip()]
        parsed=g.parse_events(events)
        if parsed['errors'] or parsed['text']!=wrapper.get('structured_output',{}).get('text'):raise ValueError('Diagnostic native/wrapper mismatch')
        init=next(e['init'] for e in events if e.get('event')=='init')
        if init['model']!=g.MODEL or wrapper['evidence']['agy_version']!='1.4.7':raise ValueError('Capability runtime mismatch')
        rows.append((wrapper,init,events))
    n,ni,_=rows[0];p,pi,pe=rows[1]
    if ni['agent']!=AGENT or pi['agent']!='vietnamizer-benchmark-read-file-control' or sorted(ni['tools'])!=sorted(pi['tools']):raise ValueError('Not a matched registry comparison')
    if n['structured_output']!={'text':'UNAVAILABLE'} or any(x['name']!='finish' for x in n['tool_calls']):raise ValueError('Negative control could use a tool')
    expected=(negative/'expected-fixture.txt').read_text()
    if p['structured_output']['text']!=expected.removesuffix('\n'):raise ValueError('Positive control did not recover fixture token absent from prompt')
    names=[x['name'] for x in p['tool_calls']]
    if names.count('read_file')!=1 or any(name not in ('finish','read_file') for name in names):raise ValueError('Unexpected positive-control tools')
    reads=[e['step_update'] for e in pe if e.get('step_update',{}).get('tool_name')=='read_file']
    target=g.read(negative/'plan.json')['read_target']
    if not reads or not any(s['state']=='DONE' for s in reads) or any(s['tool_info']['parameters'].get('Path')!=target for s in reads):raise ValueError('Positive-control target/completion mismatch')
    if (negative/'prompt.txt').read_bytes()!=(positive/'prompt.txt').read_bytes():raise ValueError('Control prompts differ')
    definition=AGENT_PATH.read_text();control=(positive/'agent.md').read_text()
    if g.sha(AGENT_PATH)!=g.read(BASE/'native-capability-blocker.json')['definition_sha256']:raise ValueError('Tested benchmark agent definition changed')
    if control!=definition.replace('name: '+AGENT,'name: vietnamizer-benchmark-read-file-control').replace('tools:\n  - finish','tools:\n  - finish\n  - read_file'):raise ValueError('Control has additional differences')
    return {'schema':'verified-registry-v1','agent':AGENT,'model':g.MODEL,'cli_version':'1.4.7','effective_agent_tools':['finish'],
            'agent_definition_sha256':g.sha(AGENT_PATH),'advertised_registry':ni['tools'],
            'evidence_fingerprints':{str((q/name).resolve()):g.sha(q/name) for q in (negative,positive) for name in ('prompt.txt','wrapper.stdout.bin','native/stdout.bin','native/stderr.bin','native/finish.json')},
            'finding':'init.tools is a shared advertised registry; actual read_file availability follows custom-agent whitelist',
            'scope':'Matched public-file read negative/positive controls; not exhaustive testing of every tool or an OS sandbox','fixture_comparison':'exact token; one terminal LF removed'}

def make_workspace(root,cell,definition):
    if cell not in g.CELLS:raise ValueError('Unknown cell')
    cwd=root/cell;cwd.mkdir(parents=True,exist_ok=False)
    p=cwd/'.agents/agents';p.mkdir(parents=True)
    shutil.copyfile(definition,p/f'{AGENT}.md')
    return cwd

def prepare(out):
    if (out/'manifest.json').exists():return verify(out)
    if out.exists() and any(out.iterdir()):raise ValueError('Use a new output directory')
    check_history(g.read(BASE/'preservation-before.json'))
    if not AGENT_PATH.is_file() or g.sha(AGENT_PATH)!=g.sha(g.ROOT/'benchmarks/gemini-text-only-agent.md'):raise ValueError('Approved native agent definition missing or changed')
    out.mkdir(parents=True,exist_ok=True)
    frozen=g.read(g.FROZEN/'prepared-manifest.json')
    for name,h in frozen['fingerprints'].items():
        src=g.FROZEN/'inputs'/name
        if g.sha(src)!=h:raise ValueError('Frozen public input drift')
        dst=out/'inputs'/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
    if {p.stem for p in (out/'inputs/prompts').glob('*.txt')}!=g.CELLS:raise ValueError('Need exact 80 prompts')
    shutil.copyfile(g.ROOT/'benchmarks/gemini-text-only-agent.md',out/'agent.md')
    shutil.copyfile(BASE/'preservation-before.json',out/'preservation-before.json')
    g.save(out/'preflight-history.json',{str(p.resolve()):g.sha(p) for name in ('epoch','epoch-v2') for p in (BASE/name).rglob('*') if p.is_file()})
    g.save(out/'diagnostic-history.json',{str(p.resolve()):g.sha(p) for p in DIAGNOSTICS.rglob('*') if p.is_file()})
    (out/'capture').mkdir();shutil.copyfile(g.ROOT/'benchmarks/gemini_boundary.mjs',out/'capture/gemini_boundary.mjs')
    binary=shutil.which('agy');node=shutil.which('node')
    if not binary or not node:raise ValueError('Official agy and Node required')
    shim=(g.ROOT/'benchmarks/gemini_text_guard.mjs').read_text().replace("const binary='/usr/local/bin/agy'",'const binary='+json.dumps(str(Path(binary).resolve())))
    (out/'capture/agy').write_text('#!/usr/bin/env node\n'+shim);(out/'capture/agy').chmod(0o755)
    g.save(out/'capture/capability-contract.json',capability_contract())
    order=sorted(g.CELLS);random.Random(25034).shuffle(order)
    code=[Path(__file__),Path(g.__file__),g.ROOT/'benchmarks/gemini_text_guard.mjs',g.ROOT/'benchmarks/gemini_boundary.mjs',g.ROOT/'benchmarks/gemini-text-only-agent.md',AGENT_PATH,g.WRAPPER,Path(binary).resolve()]
    m={'schema':'gemini-text-only-v1','agent':AGENT,'model':g.MODEL,'order':order,'max_starts':80,'historical_starts':2,'capability_diagnostic_model_starts':3,'max_total_model_starts':85,
       'node':str(Path(node).resolve()),'agy':str(Path(binary).resolve()),'wrapper':str(g.WRAPPER),
       'workspace_root':tempfile.mkdtemp(prefix='vietnamizer-text-only-',dir='/tmp'),
       'code_fingerprints':{str(p.resolve()):g.sha(p) for p in code},
       'input_fingerprints':{str(p.relative_to(out)):g.sha(p) for p in out.rglob('*') if p.is_file()},
       'cash_cap_usd':0,'new_jev_calls':0,'prior_capability_preflight':{'cli_starts':2,'turns':0,'tokens':0,'model_generation_starts':0},'native_http_bodies':'not exposed by CLI',
       'limitations':['custom agent instructions are constant across four arms','CLI advertised capabilities verified; not an OS sandbox','backend model attestation limited to native init','human quality not scored']}
    g.save(out/'manifest.json',m);return m

def verify(out):
    m=g.read(out/'manifest.json')
    if m['agent']!=AGENT or m['model']!=g.MODEL or len(m['order'])!=80 or set(m['order'])!=g.CELLS:raise ValueError('Epoch contract drift')
    for name,h in m['input_fingerprints'].items():
        if g.sha(out/name)!=h:raise ValueError('Input drift: '+name)
    for name,h in m['code_fingerprints'].items():
        if g.sha(name)!=h:raise ValueError('Reviewed code drift: '+name)
    check_history(g.read(out/'preservation-before.json'))
    check_history(g.read(out/'preflight-history.json'))
    check_history(g.read(out/'diagnostic-history.json'))
    if g.read(out/'capture/capability-contract.json')!=capability_contract():raise ValueError('Capability proof no longer matches current runtime')
    return m

def done_cells(out):
    done=set()
    for start in (out/'attempts').glob('*/start.json'):
        d=start.parent
        if not (d/'seal.json').is_file() or not (d/'result.json').is_file():raise ValueError('Unfinished attempt: '+d.name)
        for name,h in g.read(d/'seal.json').items():
            if g.sha(d/name)!=h:raise ValueError('Raw seal drift')
        if g.read(d/'result.json')['status']!='completed':raise ValueError('Failed attempt retained: '+d.name)
        contract=g.read(out/'capture/capability-contract.json') if (out/'capture/capability-contract.json').exists() else None
        validate_init(g.read(d/'native/init.json'),contract)
        if not g.read(d/'native/finish.json')['guard_ok']:raise ValueError('Guard did not accept native init')
        done.add(d.name)
    return done

def trial(out,m,cell):
    credit=g.credit_check();d=g.reserve(out,cell,{'manifest_sha256':g.sha(out/'manifest.json'),'credit':credit,'agent':AGENT})
    cwd=make_workspace(Path(m['workspace_root']),cell,out/'agent.md')
    shutil.copyfile(out/'inputs/prompts'/f'{cell}.txt',d/'prompt.txt')
    args=[m['node'],m['wrapper'],'--category','general','--cwd',str(cwd),'--mode','read','--new-session',
          '--agent',AGENT,'--model',g.MODEL,'--timeout','5m','--json-schema',json.dumps(g.SCHEMA)]
    env=os.environ.copy()
    for key in ('TYPESAFE_API_KEY','OPENAI_API_KEY','GEMINI_API_KEY','GOOGLE_API_KEY'):env.pop(key,None)
    env.update(PATH=str(out/'capture')+os.pathsep+env.get('PATH',''),AGYBIRD_STATE_DIR=str(out/'agybird-state'),
               AGYBIRD_PROJECTS_DIR=str(out/'agybird-projects'),VIETNAMIZER_RAW_DIR=str(d/'native'))
    g.save(d/'invocation.json',{'args':args,'stdin_sha256':g.sha(d/'prompt.txt'),'raw_outside_workspace':True,'native_permissions':'unchanged; request-review required'})
    proc=None;begin=time.monotonic()
    try:
        with (d/'prompt.txt').open('rb') as inp,(d/'wrapper.stdout.bin').open('xb') as stdout,(d/'wrapper.stderr.bin').open('xb') as stderr:
            proc=subprocess.Popen(args,stdin=inp,stdout=stdout,stderr=stderr,cwd=cwd,env=env,start_new_session=True)
            code=proc.wait(timeout=330)
        raw=d/'native';finish=g.read(raw/'finish.json')
        contract=g.read(out/'capture/capability-contract.json') if (out/'capture/capability-contract.json').exists() else None
        validate_init(g.read(raw/'init.json'),contract)
        for name,item in finish['streams'].items():
            if g.sha(raw/name)!=item['sha256']:raise ValueError('Native stream hash drift')
        events=[json.loads(line) for line in (raw/'stdout.bin').read_text().splitlines() if line.strip()]
        r=g.parse_events(events);envelope=g.read(d/'wrapper.stdout.bin')
        if (code!=0 or finish['exitCode']!=0 or finish['timedOut'] or finish.get('signal') or finish.get('spawnError') or not finish['guard_ok'] or
            envelope.get('status')!='success' or envelope.get('subagents') or envelope.get('permission_requests') or envelope.get('evidence',{}).get('session_resumed') or
            any(x.get('name')!='finish' for x in envelope.get('tool_calls',[])) or r['text']!=envelope.get('structured_output',{}).get('text') or
            (contract and envelope.get('evidence',{}).get('agy_version')!=contract['cli_version'])):
            raise ValueError('Native/wrapper/guard mismatch; inspect raw')
        if r['status']!='completed':raise ValueError('Invalid output or tool activity')
        r.update(agent=AGENT,model_requested=g.MODEL,exit_code=code,elapsed_seconds=time.monotonic()-begin)
    except BaseException as exc:
        if proc is not None:
            try:os.killpg(proc.pid,signal.SIGTERM)
            except ProcessLookupError:pass
            try:proc.wait(timeout=4)
            except subprocess.TimeoutExpired:pass
            try:os.killpg(proc.pid,signal.SIGKILL)
            except ProcessLookupError:pass
        r={'status':'failed','error_type':type(exc).__name__,'error':str(exc),'elapsed_seconds':time.monotonic()-begin}
    g.save(d/'result.json',r)
    g.save(d/'seal.json',{str(p.relative_to(d)):g.sha(p) for p in d.rglob('*') if p.is_file()})
    if r['status']!='completed':
        g.save(out/'STOP.json',{'cell':cell,'reason':r.get('error','Invalid output'),'retry':False})
        raise ValueError('Stopped at '+cell+'; raw preserved at '+str(d))
    if not (out/'capability-verification.json').exists():g.save(out/'capability-verification.json',{'cell':cell,'manifest_sha256':g.sha(out/'manifest.json'),'init_sha256':g.sha(d/'native/init.json'),'finish_sha256':g.sha(d/'native/finish.json'),'agent':AGENT,'tools':g.read(d/'native/init.json')['init']['tools'],'status':'verified_from_live_native_stream'})
    return r

def run(out,limit):
    m=verify(out);done=done_cells(out)
    if (out/'STOP.json').exists():raise ValueError('Stopped epoch; no automatic retries')
    lock=out/'RUNNING.lock'
    with lock.open('x') as f:f.write(str(os.getpid()))
    try:
        for cell in [c for c in m['order'] if c not in done][:limit]:
            print(f'[{len(done)+1}/80] {cell} · {AGENT}',flush=True)
            trial(out,m,cell);done.add(cell);verify(out)
            report={'planned':80,'completed':len(done),'new_epoch_starts':len(list((out/'attempts').glob('*/start.json'))),'historical_starts':2,'agent':AGENT,'model_requested':g.MODEL,'human_quality':'pending','new_jev_calls':0,'invoice_cost':None}
            temp=out/'report.tmp';temp.write_text(json.dumps(report,indent=2)+'\n');temp.replace(out/'report.json')
        print(f'{len(done)}/80; {out}',flush=True)
    finally:lock.unlink(missing_ok=True)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['prepare','probe','run','status']);p.add_argument('--out',type=Path,default=DEFAULT);p.add_argument('--limit',type=int,default=80);a=p.parse_args();out=a.out.resolve()
    if not 1<=a.limit<=80:p.error('--limit must be1–80')
    if a.action=='prepare':prepare(out);print(out)
    elif a.action=='status':verify(out);print(f'{len(done_cells(out))}/80')
    elif a.action=='probe':prepare(out);run(out,1)
    else:
        if not sys.stdin.isatty():raise ValueError('Run from owner terminal')
        prepare(out);run(out,a.limit)
if __name__=='__main__':
    try:main()
    except (ValueError,OSError) as e:print('STOP: '+str(e),file=sys.stderr);sys.exit(2)
