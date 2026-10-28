"""Continue only unattempted planned judgments; sealed rejected judgments stay missing.
No inference prompt, validation rule, model, generation or planned-ID change.
"""
from benchmarks.voice_pilot import *

def check_binding(packet,mapping,stored,stdin):
    if stored!={'packet':packet,'mapping':mapping} or judge_prompt(packet).encode()!=stdin:raise ValueError('blind mapping/input binding drift')

def rejected_assessment(packet,r):
    if not r['id'].startswith('judge-') or r.get('status')!='failed':raise ValueError('not a rejected main judgment')
    try:validate_assessment(packet,json.loads(r['text']))
    except (ValueError,TypeError,KeyError) as e:
        if r.get('error')!=type(e).__name__+': '+str(e):raise ValueError('failure is not reproducible schema/evidence rejection')
        return True
    raise ValueError('failed judgment unexpectedly validates')

def audit_history(out,m):
    sessions=set();rows=[]
    for p in sorted((out/'attempts').glob('*')):
        if p.name not in plan_ids() or not (p/'result.json').exists() or not (p/'seal.json').exists():raise ValueError('unfinished/unplanned reservation')
        r=read(p/'result.json')
        if r.get('status') not in ('completed','failed') or r.get('id')!=p.name:raise ValueError('failed/mismatched attempt')
        for n,h in read(p/'seal.json').items():
            if sha((p/n).read_bytes())!=h:raise ValueError('raw seal drift')
        if r['session'] in sessions:raise ValueError('session reused')
        sessions.add(r['session'])
        if r['manifest_sha256']!=sha((out/'manifest.json').read_bytes()) or r['stdin_sha256']!=sha((p/'stdin.txt').read_bytes()) or read(p/'response-schema.json')!=base.SCHEMA:raise ValueError('input/config binding drift')
        if r['provider']=='codex':
            x=native.parse((p/'stdout.txt').read_text())
            if any(r[k]!=x[k] for k in ('text','session','usage')) or r['argv']!=base.codex_args(Path(r['cwd'])):raise ValueError('Codex raw/result mismatch')
        else:
            f=read(p/'native/finish.json');init=read(p/'native/init.json')['init'];w=read(p/'wrapper.stdout.bin')
            x=gem.parse_events([json.loads(z) for z in (p/'native/stdout.bin').read_text().splitlines() if z.strip()])
            if not f['guard_ok'] or f['exitCode']!=0 or f['timedOut'] or init['agent']!=AGENT or init['model']!=MODEL or init['permission_mode']!='request-review' or x['status']!='completed' or r['text']!=x['text'] or r['text']!=w.get('structured_output',{}).get('text') or w.get('status')!='success' or w.get('evidence',{}).get('session_resumed') is not False or w.get('evidence',{}).get('agy_version')!=m['agy_version']:raise ValueError('Gemini raw/result mismatch')
        if p.name.startswith('judge-'):
            _,cid,provider=p.name.split('-');texts={a:read(out/'attempts'/f'edit-{cid}-{a}'/'result.json')['text'] for a in ARMS}
            packet,mapping=blind_packet(cid,(out/'corpus'/f'{cid}.txt').read_text(),texts,[(out/'corpus'/f'H{i}.txt').read_text() for i in (1,2)],provider=='gemini')
            check_binding(packet,mapping,read(out/'blind'/f'{cid}-{provider}.json'),(p/'stdin.txt').read_bytes())
            if r['status']=='failed':rejected_assessment(packet,r)
        elif r['status']=='failed':raise ValueError('failed non-judgment blocks continuation')
        if 'assessment' in r:
            packet=read(out/'calibration'/f'{p.name[4:]}.json')['packet'] if p.name.startswith('cal-') else read(out/'blind'/f'{p.name[6:]}.json')['packet']
            validate_assessment(packet,r['assessment'])
            if json.loads(r['text'])!=r['assessment']:raise ValueError('assessment binding drift')
        rows.append(r)
    return rows

def continue_judges(out):
    m=verify(out)
    with (out/'writer.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        records=audit_history(out,m)
        if sum(r['id'].startswith('edit-') and r['status']=='completed' for r in records)!=32:raise ValueError('require all32 original edits')
        for ident in (i for i in m['plan_ids'] if i.startswith('judge-')):
            if (out/'attempts'/ident).exists():continue
            _,cid,provider=ident.split('-');texts={a:read(out/'attempts'/f'edit-{cid}-{a}'/'result.json')['text'] for a in ARMS}
            packet,mapping=blind_packet(cid,(out/'corpus'/f'{cid}.txt').read_text(),texts,[(out/'corpus'/f'H{i}.txt').read_text() for i in (1,2)],provider=='gemini')
            save(out/'blind'/f'{cid}-{provider}.json',{'packet':packet,'mapping':mapping})
            try:job(out,ident,provider,judge_prompt(packet),packet)
            except ValueError:
                # Only a fully sealed, transport-valid, reproducibly invalid assessment may be skipped.
                audit_history(out,m)
            audit_history(out,m)
    return {'reserved':len(records:=audit_history(out,m)),'completed':sum(r['status']=='completed' for r in records),'missing_judgments':[r['id'] for r in records if r['status']=='failed']}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args();print(json.dumps(continue_judges(a.output.resolve())))
