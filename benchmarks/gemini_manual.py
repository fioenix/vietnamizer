"""User-operated host benchmark. Offline prepare/tests never invoke Antigravity.

The Codex tool execution denial is NOT cleared by this script. run is for the
owner's terminal only; no permission grants, sandbox override or credit changes.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import random
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parents[1]
FROZEN=ROOT/'artifacts/014-gemini-isolated-20261026'
WRAPPER=Path('/Users/fioenix/.codex/plugins/cache/Finolabs/agybird/0.3.0/scripts/agybird.mjs')
MODEL='gemini-3.8-flash-medium'
ARMS=('bare','ordinary','vietnamizer','vietnamizer_jev')
CELLS={f'R{i:03}-{a}' for i in range(1,21) for a in ARMS}
DEFAULT=ROOT/'artifacts/014-gemini-manual-20261026'
SCHEMA={'type':'object','properties':{'text':{'type':'string'}},'required':['text'],'additionalProperties':False}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def save(p,v):
    Path(p).parent.mkdir(parents=True,exist_ok=True)
    with Path(p).open('x') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())

def credit_check(path=None):
    p=path or Path.home()/'.gemini/antigravity-cli/settings.json'
    d=read(p) if p.exists() else {}
    if not isinstance(d,dict) or d.get('useG1Credits',False) is not False or d.get('modelProvider','')!='':
        raise ValueError('Subscription-only route required; settings were not changed')
    if path is None and any(os.environ.get(k) for k in ('AGY_ADC_AUTH','GOOGLE_GEMINI_BASE_URL','GOOGLE_CLOUD_QUOTA_PROJECT')):
        raise ValueError('Alternate auth/provider environment detected; refuse inference')
    return {'route':'subscription_default','credits':False,'settings_changed':False,'checked_at':time.time()}

def prepare(out):
    if (out/'manifest.json').exists():return verify(out)
    if out.exists() and any(out.iterdir()):raise ValueError('Output directory must be new or a prepared epoch')
    frozen=read(FROZEN/'prepared-manifest.json')
    out.mkdir(parents=True,exist_ok=True)
    for name,h in frozen['fingerprints'].items():
        src=FROZEN/'inputs'/name
        if sha(src)!=h:raise ValueError('Frozen public input drift: '+name)
        dst=out/'inputs'/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
    if {p.stem for p in (out/'inputs/prompts').glob('*.txt')}!=CELLS:raise ValueError('Need exact 80 public prompts')
    # Only public experiment code is copied. No tokens, credential stores or host rules.
    (out/'capture').mkdir()
    shutil.copyfile(ROOT/'benchmarks/gemini_boundary.mjs',out/'capture/gemini_boundary.mjs')
    binary=shutil.which('agy');node=shutil.which('node')
    if not binary or not node or not WRAPPER.is_file():raise ValueError('Install/authenticate official agy and Agybird first')
    shim=(ROOT/'benchmarks/gemini_capture_cli.mjs').read_text().replace("binary='/usr/local/bin/agy'",'binary='+json.dumps(str(Path(binary).resolve())))
    (out/'capture/agy').write_text(shim);(out/'capture/agy').chmod(0o755)
    shutil.copyfile(FROZEN/'protected-codex-before.json',out/'protected-codex.json')
    order=sorted(CELLS);random.Random(25034).shuffle(order)
    workspace_root=tempfile.mkdtemp(prefix='vietnamizer-public-manual-',dir='/tmp')
    m={'schema':'gemini-manual-public-v1','model_requested':MODEL,'editing_passes':1,'max_starts':80,'order':order,'workspace_root':workspace_root,
       'node':str(Path(node).resolve()),'agy':str(Path(binary).resolve()),'wrapper':str(WRAPPER),'wrapper_sha256':sha(WRAPPER),
       'driver_sha256':sha(__file__),'cash_cap_usd':0,'new_jev_calls':0,
       'input_fingerprints':{str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*')) if p.is_file()},
       'limitations':['host global context not isolated or attested','requested model may lack backend attestation',
                      'native HTTP bodies not exposed by CLI','no human quality result','raw under same user is not tamper-proof'],
       'operator':'Human terminal only; not executed by Codex tools; does not clear prior tool-review denial'}
    save(out/'manifest.json',m);return m

def verify(out):
    m=read(out/'manifest.json')
    if m['model_requested']!=MODEL or set(m['order'])!=CELLS or len(m['order'])!=80:raise ValueError('Invalid epoch')
    for n,h in m['input_fingerprints'].items():
        if sha(out/n)!=h:raise ValueError('Prepared input drift: '+n)
    if sha(__file__)!=m['driver_sha256'] or sha(m['wrapper'])!=m['wrapper_sha256']:raise ValueError('Driver/wrapper drift: prepare a reviewed new epoch')
    for n,h in read(out/'protected-codex.json').items():
        if sha(ROOT/n)!=h:raise ValueError('Protected Codex data changed: '+n)
    return m

def reserve(out,cell,record):
    if cell not in CELLS:raise ValueError('Unknown cell')
    attempts=out/'attempts';attempts.mkdir(parents=True,exist_ok=True)
    if len(list(attempts.glob('*/start.json')))>=80:raise ValueError('80-start ceiling reached')
    p=attempts/cell;p.mkdir(exist_ok=False);save(p/'start.json',dict(record,cell=cell,started_at=time.time()));return p

def parse_events(events):
    tools=[];errors=[];term=[];models=[]
    def walk(v):
        if isinstance(v,dict):
            if v.get('denied_actions') or v.get('subagents'):errors.append('denied_or_subagent')
            name=v.get('tool_name') or v.get('toolName')
            if v.get('type')=='tool':name=name or v.get('name') or 'unknown'
            if name and name!='finish':tools.append(name)
            for k in ('model','model_id'):
                if isinstance(v.get(k),str):models.append(v[k])
            for x in v.values():walk(x)
        elif isinstance(v,list):
            for x in v:walk(x)
    for e in events:
        walk(e)
        kind=e.get('event',e.get('type'))
        if e.get('type') and e.get('event') and e['type']!=e['event']:errors.append('conflicting_event')
        if kind not in ('init','step_update','result','system','message','assistant','user','error'):errors.append('unknown_event')
        if kind=='error':errors.append('native_error')
        if kind=='result':term.append(e.get('result',e))
    r=term[-1] if len(term)==1 else {};value=r.get('structured_output')
    if value is None:
        try:value=json.loads(r.get('response',''))
        except (TypeError,ValueError):value=None
    text=value.get('text','') if isinstance(value,dict) else ''
    good=isinstance(value,dict) and set(value)=={'text'} and isinstance(text,str) and bool(text.strip()) and str(r.get('status','')).upper()=='SUCCESS'
    return {'status':'completed' if good and not tools and not errors else 'failed','text':text if isinstance(text,str) else '',
            'tools':tools,'errors':errors,'usage':r.get('usage'),'models_observed':sorted(set(models)),
            'conversation_id':r.get('conversation_id')}

def completed(out):
    done=set()
    for p in (out/'attempts').glob('*/start.json'):
        d=p.parent
        if not (d/'result.json').exists() or not (d/'seal.json').exists():raise ValueError('Unfinished attempt; inspect raw, no automatic retry: '+d.name)
        for n,h in read(d/'seal.json').items():
            if sha(d/n)!=h:raise ValueError('Attempt seal drift: '+d.name)
        if read(d/'result.json')['status']!='completed':
            q=out/'reconciliations'/f'{d.name}.json'
            if not q.exists():raise ValueError('Failed attempt; inspect raw, no automatic retry: '+d.name)
            proof=read(q)
            if proof['original_seal_sha256']!=sha(d/'seal.json') or proof['manifest_sha256']!=sha(out/'manifest.json') or proof['parser_sha256']!=sha(__file__):raise ValueError('Reconciliation binding drift')
            if checked_reparse(d)!=proof['parsed_result']:raise ValueError('Reconciliation result drift')
        done.add(d.name)
    return done

def checked_reparse(d):
    """Accept a parser-only correction from sealed bytes; never call the model."""
    original=read(d/'result.json')
    if original.get('tools') or set(original.get('errors',[]))!={'unknown_event'}:raise ValueError('Not a parser-only failure')
    for n,h in read(d/'seal.json').items():
        if sha(d/n)!=h:raise ValueError('Original attempt changed')
    raw=d/'native';finish=read(raw/'finish.json');envelope=read(d/'wrapper.stdout.bin')
    if finish['exitCode']!=0 or finish.get('signal') or finish['timedOut'] or finish.get('spawnError') or envelope.get('status')!='success' or envelope.get('permission_requests') or envelope.get('subagents') or envelope.get('evidence',{}).get('session_resumed') or any(t.get('name')!='finish' for t in envelope.get('tool_calls',[])):raise ValueError('Native/wrapper did not complete cleanly')
    for n,item in finish['streams'].items():
        if sha(raw/n)!=item['sha256']:raise ValueError('Native stream hash drift')
    result=parse_events([json.loads(l) for l in (raw/'stdout.bin').read_bytes().decode('utf-8').splitlines() if l.strip()])
    if result['status']!='completed' or result['text']!=envelope.get('structured_output',{}).get('text'):raise ValueError('Corrected parser/wrapper disagree')
    return result

def check_stops(out,done):
    for stop in [out/'STOP.json',*out.glob('STOP-*.json')]:
        if not stop.exists():continue
        cell=read(stop)['cell'];proof=out/'reconciliations'/f'{cell}.json'
        if cell not in done or not proof.exists() or read(proof).get('stop_sha256')!=sha(stop):raise ValueError('Stopped epoch; inspect '+stop.name+', no automatic retry')

def run(out,limit):
    m=verify(out);done=completed(out)
    check_stops(out,done)
    lock=out/'RUNNING.lock'
    with lock.open('x') as f:f.write(str(os.getpid()))
    try:
        for cell in [c for c in m['order'] if c not in done][:limit]:
            credit=credit_check();attempt=reserve(out,cell,{'credit':credit,'manifest_sha256':sha(out/'manifest.json')})
            shutil.copyfile(out/'inputs/prompts'/f'{cell}.txt',attempt/'prompt.txt')
            cwd=Path(m.get('workspace_root',str(out/'workspaces')))/cell;cwd.mkdir(parents=True,exist_ok=False)
            args=[m['node'],m['wrapper'],'--category','general','--cwd',str(cwd),'--mode','read','--new-session',
                  '--model',MODEL,'--timeout','5m','--json-schema',json.dumps(SCHEMA)]
            env=os.environ.copy()
            for key in ('TYPESAFE_API_KEY','OPENAI_API_KEY','GEMINI_API_KEY','GOOGLE_API_KEY'):env.pop(key,None)
            env['PATH']=str(out/'capture')+os.pathsep+env.get('PATH','')
            env['AGYBIRD_STATE_DIR']=str(out/'agybird-state');env['AGYBIRD_PROJECTS_DIR']=str(out/'agybird-projects')
            save(attempt/'invocation.json',{'args':args,'stdin_sha256':sha(attempt/'prompt.txt'),'environment':'scoped PATH capture; fresh epoch state/projects; API keys removed; native settings unchanged'})
            print(f'[{len(done)+1}/80] {cell}',flush=True)
            begin=time.monotonic();proc=None
            try:
                with (attempt/'prompt.txt').open('rb') as inp,(attempt/'wrapper.stdout.bin').open('xb') as stdout,(attempt/'wrapper.stderr.bin').open('xb') as stderr:
                    proc=subprocess.Popen(args,stdin=inp,stdout=stdout,stderr=stderr,cwd=cwd,env=env,start_new_session=True)
                    code=proc.wait(timeout=330)
                raw=cwd/'.native-raw';finish=read(raw/'finish.json')
                for n,item in finish['streams'].items():
                    if sha(raw/n)!=item['sha256']:raise ValueError('Native stream hash mismatch')
                events=[json.loads(l) for l in (raw/'stdout.bin').read_bytes().decode('utf-8').splitlines() if l.strip()]
                result=parse_events(events);envelope=json.loads((attempt/'wrapper.stdout.bin').read_bytes())
                if code!=0 or finish['exitCode']!=0 or finish['timedOut'] or envelope.get('status')!='success' or envelope.get('subagents') or envelope.get('evidence',{}).get('session_resumed') or any(t.get('name')!='finish' for t in envelope.get('tool_calls',[])):
                    result['status']='failed';result['errors'].append('wrapper_or_process_failed')
                result.update(exit_code=code,elapsed_seconds=time.monotonic()-begin,model_requested=MODEL)
            except BaseException as exc:
                if proc is not None:
                    try:os.killpg(proc.pid,signal.SIGTERM)
                    except ProcessLookupError:pass
                    try:proc.wait(timeout=4)
                    except subprocess.TimeoutExpired:pass
                    # Native CLI and shim share the wrapper group. Kill remaining
                    # descendants even if the wrapper itself already exited.
                    try:os.killpg(proc.pid,signal.SIGKILL)
                    except ProcessLookupError:pass
                result={'status':'failed','error_type':type(exc).__name__,'error':str(exc),'elapsed_seconds':time.monotonic()-begin}
            if (cwd/'.native-raw').is_dir():shutil.copytree(cwd/'.native-raw',attempt/'native')
            save(attempt/'result.json',result)
            save(attempt/'seal.json',{str(p.relative_to(attempt)):sha(p) for p in sorted(attempt.rglob('*')) if p.is_file()})
            if result['status']!='completed':
                stop=out/'STOP.json'
                if stop.exists():stop=out/f'STOP-{cell}.json'
                save(stop,{'cell':cell,'reason':'Failed/denied/tool/subagent/timeout/schema; preserve raw and inspect; no retries'})
                raise ValueError('Stopped at '+cell+'; raw preserved')
            done.add(cell)
            verify(out)
            report={'planned':80,'completed':len(done),'requested_model':MODEL,'human_quality':'not scored','new_jev_calls':0,'invoice_cost':None}
            temp=out/'report.tmp';temp.write_text(json.dumps(report,indent=2)+'\n');temp.replace(out/'report.json')
        print(f'Completed {len(done)}/80; data: {out}',flush=True)
    finally:lock.unlink(missing_ok=True)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['prepare','run','status']);p.add_argument('--out',type=Path,default=DEFAULT);p.add_argument('--limit',type=int,default=80);a=p.parse_args();a.out=a.out.resolve()
    if not 1<=a.limit<=80:p.error('--limit must be1–80')
    if a.action=='prepare':prepare(a.out);print(a.out)
    elif a.action=='status':verify(a.out);print(f'{len(completed(a.out))}/80')
    else:
        if not sys.stdin.isatty():raise ValueError('run requires the owner interactive terminal; Codex tools must not execute this host job')
        prepare(a.out);run(a.out,a.limit)

if __name__=='__main__':
    try:main()
    except (ValueError,OSError) as exc:print('STOP: '+str(exc),file=sys.stderr);sys.exit(2)
