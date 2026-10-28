"""Sealed per-question recovery for the frozen public-source cohort; caps unchanged."""
import argparse,copy,json
from pathlib import Path
from benchmarks import public_ai as pub,jev_composite as comp
from jev import core
base=pub.base;old=pub.old
FILES=('record.json','request.json','request.body','response.json','response.body','http.json')

def prepare(out):
 m=pub.verify(out)
 a={'schema':'public-recovery-v1','parent_digest':base.digest(m),'source_digest':base.digest(Path(__file__).read_bytes()),'helper_digest':base.digest(Path(comp.__file__).read_bytes()),'caps':{'usd':'2','network_total':640,'network_per_case':32,'codex_starts':80},'policy':'One repair per invalid response, only invalid score/choice distributions; retain valid answers exactly. Original STOP_PAID remains. Budget exhaustion yields explicitly partial advice; any other failure stops.'}
 base.freeze_manifest(out/'recovery-manifest.json',a);return a

def verify(out):
 m=pub.verify(out);a=old.read(out/'recovery-manifest.json')
 if a['parent_digest']!=base.digest(m) or a['source_digest']!=base.digest(Path(__file__).read_bytes()) or a['helper_digest']!=base.digest(Path(comp.__file__).read_bytes()):raise ValueError('recovery amendment drift')
 if (out/'STOP_RECOVERY').exists():raise ValueError('recovery stopped; inspect')
 return a

def network(out,rel):
 r,p,a=comp.source(out,rel);h=old.read((out/rel).parent/'http.json')
 if h.get('credential_redacted') or ((out/rel).parent/'request.body').read_bytes()!=core.encoded(p):raise ValueError('wire drift/redaction')
 return r,p,a

def composite(out,folder):
 r=old.read(folder/'record.json');p=old.read(folder/'request.json');a=old.read(folder/'response.json')
 if (folder/'seal').read_text()!=base.digest(r) or r['amendment_digest']!=base.digest(verify(out)) or r['request_digest']!=core.digest(p) or r['response_digest']!=core.digest(a):raise ValueError('composite seal drift')
 original,op,oa=network(out,r['original']);repair,rp,ra=network(out,r['repair']);good,bad=comp.split_answers(op,oa)
 if original['status']!='invalid_response' or repair['status']!='validated' or original['case']!=r['case'] or repair['case']!=r['case'] or p!=op or rp!=comp.subset(op,oa,bad)[0]:raise ValueError('repair scope drift')
 expected=copy.deepcopy(oa);expected['answers'].update(ra['answers']);expected['usage']={k:oa['usage'][k]+ra['usage'][k] for k in ('input_tokens','output_tokens')}
 if a!=expected or r['answer_sources']!={n:r['original'] if n in good else r['repair'] for n in p['questions']}:raise ValueError('answer/provenance drift')
 if set(r['source_digests'])!={r['original'],r['repair']}:raise ValueError('source inventory drift')
 for rel,hashes in r['source_digests'].items():
  if hashes!={n:base.digest((out/rel).parent.joinpath(n).read_bytes()) for n in FILES}:raise ValueError('raw snapshot drift')
 core.validate_response(p,a);return r,p,a

class Store(pub.PublicBudget):
 def __init__(self,out,m):
  super().__init__(out,m['prior_budget']['reserved_or_actual_usd'],prior_count=m['prior_budget']['requests']);self.trace=[];self.cache={}
  for folder in sorted((out/'composites').glob('*/*')):
   r,p,a=composite(out,folder);self.cache[(r['case'],core.digest(p))]=(str((folder/'record.json').relative_to(out)),p,a)
  for path in sorted((out/'requests').glob('*/record.json')):
   r=old.read(path)
   if r['status']!='validated':continue
   r,p,a=network(out,str(path.relative_to(out)));core.validate_response(p,a)
   if r.get('response_digest')!=core.digest(a):raise ValueError('network response digest drift')
   key=(r['case'],core.digest(p))
   if key in self.cache:raise ValueError('duplicate accepted network request')
   self.cache[key]=(str(path.relative_to(out)),p,a)
 def repair(self,cid,rel,key,timeout):
  r,p,a=network(self.out,rel);good,bad=comp.split_answers(p,a);ticket=self.out/'repair-attempts'/f'{cid}-{Path(rel).parent.name}.json'
  if ticket.exists():raise ValueError('repair already attempted; no reroll')
  rp,_=comp.subset(p,a,bad);old.save(ticket,{'status':'started','original':rel,'invalid_questions':bad,'request_digest':core.digest(rp)})
  ra=super().send(cid,rp,key,timeout);rr=f'requests/{len(self.entries()):04d}/record.json'
  merged=copy.deepcopy(a);merged['answers'].update(ra['answers']);merged['usage']={k:a['usage'][k]+ra['usage'][k] for k in ('input_tokens','output_tokens')};core.validate_response(p,merged)
  folder=self.out/'composites'/cid/core.digest(p);folder.mkdir(parents=True,exist_ok=False)
  proof={'case':cid,'amendment_digest':base.digest(verify(self.out)),'original':rel,'repair':rr,'request_digest':core.digest(p),'response_digest':core.digest(merged),'answer_sources':{n:rel if n in good else rr for n in p['questions']},'source_digests':{x:{n:base.digest((self.out/x).parent.joinpath(n).read_bytes()) for n in FILES} for x in (rel,rr)}}
  old.save(folder/'request.json',p);old.save(folder/'response.json',merged);old.save(folder/'record.json',proof);(folder/'seal').write_text(base.digest(proof));composite(self.out,folder)
  old.save(ticket,{**old.read(ticket),'status':'completed','composite':str(folder.relative_to(self.out))});return str((folder/'record.json').relative_to(self.out)),p,merged
 def dispatch(self,cid,p,key,timeout):
  digest=core.digest(p);cached=self.cache.get((cid,digest))
  if cached:rel,original,a=cached
  else:
   matches=[x for x in sorted((self.out/'requests').glob('*/record.json')) if old.read(x)['case']==cid and old.read(x)['request_digest']==digest]
   if matches:
    if len(matches)!=1:raise ValueError('ambiguous failed request')
    path=matches[0];r=old.read(path)
    if r['status']!='invalid_response' or r.get('diagnostic',{}).get('reason') not in ('score_distribution','choice_distribution'):raise ValueError('unsupported previous failure')
    rel,original,a=self.repair(cid,str(path.relative_to(self.out)),key,timeout)
   else:
    try:
     a=super().send(cid,p,key,timeout);rel=f'requests/{len(self.entries()):04d}/record.json';original=p
    except pub.rec.RecordedFailure:
     rows=self.entries();r=rows[-1] if rows else {}
     if self.last_failure.get('phase')=='budget':raise
     if r.get('case')!=cid or r.get('request_digest')!=digest or r.get('diagnostic',{}).get('reason') not in ('score_distribution','choice_distribution'):raise
     rel,original,a=self.repair(cid,f'requests/{len(rows):04d}/record.json',key,timeout)
   self.cache[(cid,digest)]=(rel,original,a)
  if original!=p:raise ValueError('cached payload drift')
  core.validate_response(p,a);self.trace.append(rel);return a

def advice(out,cid,r):
 target=out/'evaluations'/cid/'recovered.json';m=pub.verify(out)
 if old.read(target.with_suffix('.seal.json'))['digest']!=base.digest(r) or r['manifest_digest']!=base.digest(m) or r['input_digest']!=core.digest(old.read(out/'inputs.json')[cid]) or r['recovery_digest']!=base.digest(verify(out)):raise ValueError('result binding drift')
 if len(r['evidence_trace'])!=sum(x['status']=='validated' for x in r['receipts']):raise ValueError('trace count drift')
 checks=[];answers={};trace=iter(r['evidence_trace'])
 for receipt in r['receipts']:
  if receipt['status']!='validated':
   if receipt.get('diagnostic',{}).get('phase')!='budget' and r.get('stop_diagnostic',{}).get('phase')!='budget':raise ValueError('unresolved service failure')
   continue
  rel=next(trace)
  if rel.startswith('composites/'):record,p,a=composite(out,(out/rel).parent)
  else:
   record,p,a=network(out,rel)
   if record['status']!='validated':raise ValueError('unvalidated advice')
  clean,usage=core.validate_response(p,a)
  if record['case']!=cid or receipt['request_digest']!=core.digest(p) or receipt['response_digest']!=core.digest(a) or receipt['usage']!=usage:raise ValueError('receipt proof mismatch')
  checks.append({'state':p.get('state',{}),'questions':p['questions'],'answers':clean})
  answers.update({(receipt['request_digest'],n):v for n,v in clean.items()})
 for j in r['judgments']:
  if answers.get((j['request_digest'],j['check']))!=j['answer']:raise ValueError('judgment mismatch')
 return old.advice_for(r,[],checks)

def evaluate(out,cid):
 am=verify(out);m=pub.verify(out);target=out/'evaluations'/cid/'recovered.json'
 if target.exists():r=old.read(target);advice(out,cid,r);return r
 started=target.with_suffix('.started.json')
 if started.exists():raise ValueError('evaluation interrupted; inspect')
 store=Store(out,m);doc=old.read(out/'inputs.json')[cid];old.save(started,{'input_digest':core.digest(doc),'recovery_digest':base.digest(am)})
 try:
  r=core.evaluate(doc,transport=lambda p,k,t:store.dispatch(cid,p,k,t));r.update(case=cid,manifest_digest=base.digest(m),input_digest=core.digest(doc),recovery_digest=base.digest(am),evidence_trace=store.trace,stop_diagnostic=store.last_failure)
  failed=[x for x in r.get('receipts',[]) if x['status']!='validated']
  if failed and (not store.last_failure or store.last_failure.get('phase')!='budget'):raise ValueError('unresolved service error')
  old.save(target,r);old.save(target.with_suffix('.seal.json'),{'digest':base.digest(r)});advice(out,cid,r)
 except BaseException:
  (out/'STOP_RECOVERY').write_text('Preserve all evidence; inspect failure before further dispatch.\n');raise
 print(json.dumps({'case':cid,'status':r['status'],'scope_complete':r['scope_complete'],'requests':len(store.entries()),'budget':store.summary()},ensure_ascii=False),flush=True);return r

def run(out,limit):
 verify(out);cases=old.read(out/'frozen-corpus.json')['cases'];bundles=old.read(out/'bundles.json');done=0
 with old.writer(out):
  for c in cases:
   existing={r['cell']:r for r in base.records(out)};cells=[f'codex/{c["id"]}/{a}' for a in pub.ARMS]
   if all(x in existing and existing[x]['status']=='completed' for x in cells):continue
   if any(x in existing and existing[x]['status']!='completed' for x in cells):raise ValueError('failed Codex cell; no retry')
   r=evaluate(out,c['id']);a=advice(out,c['id'],r)
   for arm in pub.ARMS:
    prompt=pub.prompt_for(c,arm,bundles[c['id']],a if arm=='vietnamizer_jev' else None);p=out/'prompts'/f'{c["id"]}-{arm}.txt';p.parent.mkdir(exist_ok=True)
    if p.exists() and p.read_text()!=prompt:raise ValueError('prompt drift')
    p.write_text(prompt)
   pending=[x for x in cells if x not in existing]
   if len(existing)+len(pending)>80:raise ValueError('Codex cap')
   rows=base.run_batch(out,pending,len(pending))
   if any(x['status']!='completed' for x in rows):raise ValueError('Codex failure')
   print(json.dumps(pub.report(out)),flush=True);done+=1
   if done>=limit:break
 return pub.report(out)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=('prepare','run'));p.add_argument('--output',type=Path,required=True);p.add_argument('--limit',type=int,default=1);a=p.parse_args();print(json.dumps(prepare(a.output) if a.command=='prepare' else run(a.output,a.limit)))
