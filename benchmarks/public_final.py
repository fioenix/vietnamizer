"""R020-only, single cache-reconciliation pass after a validated late raw response."""
import argparse,json
from pathlib import Path
from benchmarks import public_recovery as r,public_deadline as d
pub=r.pub;old=r.old;base=r.base;core=r.core
MANIFESTS=('manifest.json','recovery-manifest.json','deadline-manifest.json','abstention-manifest.json','availability-manifest.json')

def prepare(out):
 pub.verify(out)
 paths=[Path(__file__),Path(r.__file__),Path(d.__file__),Path(r.comp.__file__),*sorted(out.glob('STOP_*')),out/'evaluations/R020/recovered.json',out/'evaluations/R020/recovered.seal.json',*sorted((out/'requests').glob('054[89]/*')),*sorted((out/'requests/0550').glob('*')),*sorted((out/'deadline-attempts').glob('R020-*'))]
 m={'schema':'public-final-case-reconciliation-v1','case':'R020','parents':{n:base.digest(old.read(out/n)) for n in MANIFESTS},'fingerprints':{str(p.resolve()):base.digest(p.read_bytes()) for p in paths},'policy':'One new R020core pass only; replay validated548/550raw, no network resampling; only unasked tail payloads, no transport retry, unchanged32case/640new/USD2/80Codex starts. Recognized schema/availability/budget errors remain partial; integrity/auth/other failures stop. Original failed pass unchanged; late550was not accepted there.'}
 base.freeze_manifest(out/'final-case-manifest.json',m);return m

def verify(out):
 pub.verify(out);m=old.read(out/'final-case-manifest.json')
 for n,h in m['parents'].items():
  p=old.read(out/n)
  if base.digest(p)!=h:raise ValueError('parent manifest drift')
  for name,digest in p.get('fingerprints',{}).items():
   if base.digest(Path(name).read_bytes())!=digest:raise ValueError('ancestor source/evidence drift')
 for name,digest in m['fingerprints'].items():
  if base.digest(Path(name).read_bytes())!=digest:raise ValueError('final-case source/evidence drift')
 if (out/'STOP_FINAL_CASE').exists():raise ValueError('final reconciliation stopped; inspect')
 return old.read(out/'recovery-manifest.json')

def source(out,rel):
 if rel.startswith('composites/'):return r.composite(out,(out/rel).parent)
 record,p,a=r.network(out,rel)
 if record['status']!='validated' or record.get('response_digest')!=core.digest(a):raise ValueError('not accepted network raw')
 core.validate_response(p,a);return record,p,a

def late_proof(out):
 p=old.read(out/'requests/0550/request.json');ticket=old.read(out/'deadline-attempts'/f'R020-{core.digest(p)}.json');rec,p,a=source(out,'requests/0550/record.json')
 if ticket!={'status':'completed','case':'R020','request_digest':core.digest(p),'original':'requests/0549/record.json','original_record_digest':base.digest(old.read(out/'requests/0549/record.json')),'amendment_digest':base.digest(old.read(out/'deadline-manifest.json')),'retry':'requests/0550/record.json'} or not d.eligible(out,ticket['original'],'R020',p):raise ValueError('late retry proof drift')
 return ticket

def accepted(out,result):
 checks=[];answers={};used=[]
 for receipt in result['receipts']:
  if receipt['status']!='validated':continue
  matches=[]
  for rel in result['raw_callback_trace']:
   record,p,a=source(out,rel)
   if core.digest(p)==receipt['request_digest'] and core.digest(a)==receipt['response_digest']:matches.append((rel,record,p,a))
  if len(matches)!=1:raise ValueError('accepted receipt trace mismatch')
  rel,record,p,a=matches[0];clean,usage=core.validate_response(p,a)
  if record['case']!='R020' or receipt['usage']!=usage:raise ValueError('receipt usage/case drift')
  used.append(rel);checks.append({'state':p.get('state',{}),'questions':p['questions'],'answers':clean});answers.update({(receipt['request_digest'],n):v for n,v in clean.items()})
 for j in result['judgments']:
  if answers.get((j['request_digest'],j['check']))!=j['answer']:raise ValueError('unaccepted judgment')
 for rel in result['raw_callback_trace']:
  _,p,_=source(out,rel)
  if not any(x['request_digest']==core.digest(p) for x in result['receipts']):raise ValueError('orphan callback trace')
 return checks,used

def recognized(result):
 failed=[x for x in result['receipts'] if x['status']!='validated'];diag=result.get('stop_diagnostic') or {}
 if not failed:return True
 if len(failed)!=1:return False
 if diag.get('phase')=='budget' or diag.get('reason') in ('score_distribution','choice_distribution'):return True
 if diag.get('failure_kind')=='deadline' and diag.get('http_status') is None and diag.get('stored_body_bytes')==0:return True
 return failed[0]['status']=='deadline_exceeded' and bool(result['raw_callback_trace']) and not diag

def advice(out,result):
 verify(out);p=out/'evaluations/R020/reconciled.json';m=pub.verify(out)
 if old.read(p.with_suffix('.seal.json'))['digest']!=base.digest(result) or result['input_digest']!=core.digest(old.read(out/'inputs.json')['R020']) or result['manifest_digest']!=base.digest(m) or result['reconciliation_digest']!=base.digest(old.read(out/'final-case-manifest.json')):raise ValueError('reconciled result binding drift')
 late_proof(out)
 if not recognized(result):raise ValueError('unsupported final-pass failure')
 checks,used=accepted(out,result)
 if used!=result['accepted_trace']:raise ValueError('accepted trace drift')
 a=old.advice_for(result,[],checks);a.update(service_disposition='reconciled_after_late_response',coverage_origin='new single reconciliation pass; original failed pass preserved');return a

def evaluate(out):
 verify(out);target=out/'evaluations/R020/reconciled.json'
 if target.exists():result=old.read(target);advice(out,result);return result
 ticket=target.with_suffix('.started.json')
 if ticket.exists():raise ValueError('single reconciliation pass already started; no repeat')
 late_proof(out);m=pub.verify(out);store=r.Store(out,m);doc=old.read(out/'inputs.json')['R020'];old.save(ticket,{'case':'R020','reconciliation_digest':base.digest(old.read(out/'final-case-manifest.json')),'existing_network_requests':len(store.entries())})
 result=core.evaluate(doc,transport=lambda p,k,t:store.dispatch('R020',p,k,t));result.update(case='R020',input_digest=core.digest(doc),manifest_digest=base.digest(m),reconciliation_digest=base.digest(old.read(out/'final-case-manifest.json')),original_failed_result_digest=base.digest(old.read(out/'evaluations/R020/recovered.json')),raw_callback_trace=store.trace,stop_diagnostic=store.last_failure)
 old.save(target.parent/'reconciled-core-raw.json',result)
 _,result['accepted_trace']=accepted(out,result);old.save(target,result);old.save(target.with_suffix('.seal.json'),{'digest':base.digest(result)});advice(out,result)
 print(json.dumps({'case':'R020','new_pass_status':result['status'],'scope_complete':result['scope_complete'],'counts':result['counts'],'budget':store.summary()}),flush=True);return result

def run(out):
 previous=r.verify;r.verify=verify
 try:
  with old.writer(out):
   verify(out);cells=[f'codex/R020/{a}' for a in pub.ARMS];existing={x['cell']:x for x in base.records(out)}
   if any(c in existing for c in cells):raise ValueError('R020 already attempted; no reroll')
   result=evaluate(out);a=advice(out,result);c=next(c for c in old.read(out/'frozen-corpus.json')['cases'] if c['id']=='R020');bundle=old.read(out/'bundles.json')['R020']
   for arm in pub.ARMS:
    prompt=pub.prompt_for(c,arm,bundle,a if arm=='vietnamizer_jev' else None);p=out/'prompts'/f'R020-{arm}.txt'
    if p.exists() and p.read_text()!=prompt:raise ValueError('prompt drift')
    p.write_text(prompt)
   if len(existing)+4>80:raise ValueError('Codex start cap')
   rows=base.run_batch(out,cells,4)
   if any(x['status']!='completed' for x in rows):raise ValueError('Codex failure')
   return pub.report(out)
 except BaseException:
  (out/'STOP_FINAL_CASE').write_text('Final-case failure; preserve all evidence, no further dispatch.\n');raise
 finally:r.verify=previous

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=('prepare','run'));p.add_argument('--output',type=Path,required=True);a=p.parse_args();print(json.dumps(prepare(a.output) if a.command=='prepare' else run(a.output)))
