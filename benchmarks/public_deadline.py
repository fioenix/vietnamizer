"""Reviewed one-time empty-body transport deadline recovery; immutable prior evidence."""
import argparse,json
from pathlib import Path
from benchmarks import public_recovery as r
pub=r.pub;old=r.old;base=r.base;core=r.core
OriginalAdvice=r.advice

def prepare(out):
 m=pub.verify(out);previous=old.read(out/'recovery-manifest.json')
 paths=[Path(r.__file__),Path(__file__),out/'recovery-manifest.json',out/'STOP_RECOVERY',out/'evaluations/R007/recovered.started.json',*sorted((out/'requests/0202').glob('*'))]
 a={'schema':'public-empty-deadline-v1','parent_digest':base.digest(m),'previous_digest':base.digest(previous),'fingerprints':{str(p.resolve()):base.digest(p.read_bytes()) for p in paths},'authority':'Owner-authorized benchmark continuation and bounded repair; independent implementation review before dispatch. Same data, models, arms and caps.','policy':'Exactly one fresh network attempt per exact payload after HTTP-none, zero-body, opening deadline. Original unknown bill fully reserved; both attempts count. No valid semantic answer resampling. Any second failure stops.','allowed_interrupted_case':'R007','caps':{'usd':'2','network_per_case':32,'new_network_total':640,'codex_starts':80}}
 base.freeze_manifest(out/'deadline-manifest.json',a);return a

def verify(out):
 a=old.read(out/'deadline-manifest.json');m=pub.verify(out);previous=old.read(out/'recovery-manifest.json')
 if a['parent_digest']!=base.digest(m) or a['previous_digest']!=base.digest(previous):raise ValueError('deadline parent drift')
 for name,d in a['fingerprints'].items():
  if base.digest(Path(name).read_bytes())!=d:raise ValueError('deadline source/evidence drift')
 if previous['source_digest']!=base.digest(Path(r.__file__).read_bytes()) or previous['helper_digest']!=base.digest(Path(r.comp.__file__).read_bytes()):raise ValueError('original recovery drift')
 if (out/'STOP_DEADLINE').exists():raise ValueError('deadline recovery stopped; inspect')
 return previous

def eligible(out,rel,cid,p):
 path=out/rel;record=old.read(path);http=old.read(path.parent/'http.json')
 return (record['case']==cid and record['request_digest']==core.digest(p) and record['status']=='transport_failed' and record.get('diagnostic',{}).get('failure_kind')=='deadline' and http.get('http_status') is None and http.get('phase')=='opening' and not http.get('body_complete') and http.get('stored_body_bytes')==0 and http.get('body_bytes_received')==0 and (path.parent/'response.body').read_bytes()==b'' and not (path.parent/'response.json').exists() and (path.parent/'request.body').read_bytes()==core.encoded(p) and old.read(path.parent/'request.json')==p)

class Store(r.Store):
 def __init__(self,out,m):super().__init__(out,m);self.deadline_retries=[]
 def retry(self,cid,p,key,timeout,rel):
  if not eligible(self.out,rel,cid,p):raise ValueError('not eligible empty opening deadline')
  ticket=self.out/'deadline-attempts'/f'{cid}-{core.digest(p)}.json'
  if ticket.exists():raise ValueError('deadline retry already attempted; no reroll')
  info={'status':'started','case':cid,'request_digest':core.digest(p),'original':rel,'original_record_digest':base.digest(old.read(self.out/rel)),'amendment_digest':base.digest(old.read(self.out/'deadline-manifest.json'))}
  old.save(ticket,info)
  a=pub.PublicBudget.send(self,cid,p,key,timeout) # One attempt; any failure propagates.
  new=f'requests/{len(self.entries()):04d}/record.json';self.trace.append(new);self.cache[(cid,core.digest(p))]=(new,p,a)
  info.update(status='completed',retry=new);old.save(ticket,info);self.deadline_retries.append(info);self.last_failure=None;return a
 def dispatch(self,cid,p,key,timeout):
  if (cid,core.digest(p)) not in self.cache:
   rows=[x for x in sorted((self.out/'requests').glob('*/record.json')) if old.read(x)['case']==cid and old.read(x)['request_digest']==core.digest(p)]
   if len(rows)==1 and old.read(rows[0])['status']=='transport_failed':return self.retry(cid,p,key,timeout,str(rows[0].relative_to(self.out)))
  try:return super().dispatch(cid,p,key,timeout)
  except pub.rec.RecordedFailure:
   rows=sorted((self.out/'requests').glob('*/record.json'))
   if rows and eligible(self.out,str(rows[-1].relative_to(self.out)),cid,p):return self.retry(cid,p,key,timeout,str(rows[-1].relative_to(self.out)))
   raise

def advice(out,cid,result):
 if 'deadline_manifest_digest' in result and result['deadline_manifest_digest']!=base.digest(old.read(out/'deadline-manifest.json')):raise ValueError('deadline result binding drift')
 for info in result.get('deadline_retries',[]):
  path=out/'deadline-attempts'/f"{cid}-{info['request_digest']}.json"
  record,p,a=r.network(out,info['retry'])
  if old.read(path)!=info or info['case']!=cid or info['status']!='completed' or info['amendment_digest']!=base.digest(old.read(out/'deadline-manifest.json')) or info['original_record_digest']!=base.digest(old.read(out/info['original'])) or not eligible(out,info['original'],cid,p) or record['case']!=cid or record['status']!='validated' or info['request_digest']!=core.digest(p) or info['retry'] not in result['evidence_trace']:raise ValueError('deadline retry proof drift')
 return OriginalAdvice(out,cid,result)

def evaluate(out,cid):
 am=verify(out);m=pub.verify(out);target=out/'evaluations'/cid/'recovered.json'
 if target.exists():result=old.read(target);advice(out,cid,result);return result
 initial=target.with_suffix('.started.json')
 if initial.exists() and cid!='R007':raise ValueError('unreviewed interrupted original evaluation')
 ticket=target.with_suffix('.deadline-started.json')
 if ticket.exists():raise ValueError('deadline evaluation interrupted; inspect')
 store=Store(out,m);doc=old.read(out/'inputs.json')[cid];old.save(ticket,{'case':cid,'input_digest':core.digest(doc),'deadline_manifest_digest':base.digest(old.read(out/'deadline-manifest.json'))})
 try:
  result=core.evaluate(doc,transport=lambda p,k,t:store.dispatch(cid,p,k,t));result.update(case=cid,manifest_digest=base.digest(m),input_digest=core.digest(doc),recovery_digest=base.digest(am),deadline_manifest_digest=base.digest(old.read(out/'deadline-manifest.json')),evidence_trace=store.trace,stop_diagnostic=store.last_failure,deadline_retries=store.deadline_retries)
  # Always preserve failed core result before deciding whether generation may proceed.
  old.save(target,result);old.save(target.with_suffix('.seal.json'),{'digest':base.digest(result)})
  failed=[x for x in result.get('receipts',[]) if x['status']!='validated']
  if failed and (not store.last_failure or store.last_failure.get('phase')!='budget'):raise ValueError('unresolved service failure after bounded deadline recovery')
  advice(out,cid,result)
 except BaseException:
  (out/'STOP_DEADLINE').write_text('Preserve all prior stop markers/raw evidence; inspect before further dispatch.\n');raise
 print(json.dumps({'case':cid,'status':result['status'],'scope_complete':result['scope_complete'],'requests':len(store.entries()),'budget':store.summary(),'deadline_retries':len(store.deadline_retries)},ensure_ascii=False),flush=True);return result

def run(out,limit):
 previous_verify=r.verify;previous_evaluate=r.evaluate;previous_advice=r.advice;r.verify=verify;r.evaluate=evaluate;r.advice=advice
 try:return r.run(out,limit)
 finally:r.verify=previous_verify;r.evaluate=previous_evaluate;r.advice=previous_advice

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=('prepare','run'));p.add_argument('--output',type=Path,required=True);p.add_argument('--limit',type=int,default=1);a=p.parse_args();print(json.dumps(prepare(a.output) if a.command=='prepare' else run(a.output,a.limit)))
