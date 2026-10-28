"""Recorded, budget-cumulative repair of the 20-document editorial Jev pilot."""
from __future__ import annotations
import argparse,contextlib,io,json,os,random,sys,time
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from benchmarks import jev_pilot as old,editorial_pilot as base,jev_capture as capture
from jev import core
from jev.transport import ServiceError

class RecordedFailure(ServiceError):
 def __init__(self,diagnostic):self.diagnostic=diagnostic;super().__init__('service_failed')

class Store:
 def __init__(self,out,origins,cap=old.CAP,max_new=32):
  self.out=out;self.origins=origins;self.cap=cap;self.cache={};self.replayed=[];self.max_new=max_new;self.last_failure=None
  (out/'requests').mkdir(parents=True,exist_ok=True)
  self.initial_new_count=len(self.entries())
 def entries(self):return [old.read(p) for p in sorted((self.out/'requests').glob('*/record.json'))]
 def inherited(self):
  return [old.read(p) for origin in self.origins for p in sorted((origin/'requests').glob('*.json'))]
 def summary(self):
  rows=self.inherited()+self.entries()
  for r in rows:
   if 'actual_usd' in r:
    if type(r.get('input_tokens')) is not int or not 0<=r['input_tokens']<=65536 or Decimal(r['actual_usd'])!=Decimal(r['input_tokens'])*old.PRICE:raise ValueError('billing ledger integrity')
  known=sum((Decimal(r.get('actual_usd','0')) for r in rows),Decimal(0))
  total=sum((Decimal(r.get('actual_usd',str(old.RESERVE))) for r in rows),Decimal(0))
  return {'requests':len(rows),'new_requests':len(self.entries()),'known_usage_cost_usd':str(known),
          'reserved_or_actual_usd':str(total),'unknown_billing_requests':sum('actual_usd' not in r for r in rows),
          'input_tokens':sum(r.get('input_tokens',0) for r in rows),'cap_usd':str(self.cap),'invoice_reconciled':False}
 def load_cache(self,origin):
  # Strictly reconcile original core receipts/raw evidence before reuse.
  with contextlib.redirect_stdout(io.StringIO()):old.validate_epoch(origin)
  rows={r['request_digest']:p for p in sorted((origin/'requests').glob('*.json')) if (r:=old.read(p))['status']=='validated'}
  for path in sorted((origin/'evaluations').glob('*/result.json')):
   result=old.read(path);cid=path.parent.name
   old.verify_binding(old.read(origin/'manifest.json'),cid,old.read(origin/'inputs.json')[cid],result)
   old.verified_checks(origin,cid,result)
   for receipt in result.get('receipts',[]):
    if receipt['status']!='validated':continue
    p=rows[receipt['request_digest']];payload=old.read(p.with_suffix('.request.json.raw'));reply=old.read(p.with_suffix('.response.json.raw'))
    core.validate_response(payload,reply)
    self.cache[(cid,core.digest(payload))]={'reply':reply,'origin':str(p)}
  # New accepted records are admitted by their enclosing evaluated/diagnostic receipt only.
  for path in sorted((self.out/'evaluations').glob('*/*.json')):
   result=old.read(path)
   if not path.with_suffix('.sha256').exists() or path.with_suffix('.sha256').read_text()!=base.digest(result):raise ValueError('evaluation seal mismatch')
   manifest=old.read(self.out/'manifest.json')
   doc=old.read(origin/'inputs.json')[result['case']]
   if result.get('manifest_digest')!=base.digest(manifest) or result.get('input_digest')!=core.digest(doc):raise ValueError('new cache evaluation binding mismatch')
   for receipt in result.get('receipts',[]):
    if receipt['status']!='validated':continue
    match=[p for p in (self.out/'requests').glob('*/record.json') if old.read(p)['request_digest']==receipt['request_digest'] and old.read(p)['case']==result['case']]
    if not match:continue  # Legacy cache hits are already loaded above.
    p=match[-1];r=old.read(p);payload=old.read(p.parent/'request.json');reply=old.read(p.parent/'response.json')
    clean,usage=core.validate_response(payload,reply)
    if r['status']!='validated' or r['response_digest']!=core.digest(reply) or r['request_digest']!=core.digest(payload):raise ValueError('new cache drift')
    self.cache[(result['case'],core.digest(payload))]={'reply':reply,'origin':str(p)}
 def send(self,cid,payload,key,timeout):
  digest=core.digest(payload);cached=self.cache.get((cid,digest))
  if cached:
   core.validate_response(payload,cached['reply'])
   self.replayed.append({'case':cid,'request_digest':digest,'origin':cached['origin']});return cached['reply']
  rows=self.inherited()+self.entries();summary=self.summary()
  if (payload.get('model')!=core.MODEL or len(core.encoded(payload))>core.MAX_REQUEST or
      len(self.entries())-self.initial_new_count>=self.max_new or len(rows)>=640 or sum(r['case']==cid for r in rows)>=32 or Decimal(summary['reserved_or_actual_usd'])+old.RESERVE>self.cap):
   self.last_failure={'phase':'budget','reason':'new_request_limit' if len(self.entries())-self.initial_new_count>=self.max_new else 'cap_reached'}
   raise RecordedFailure(self.last_failure)
  target=self.out/'requests'/f'{len(self.entries())+1:04d}';target.mkdir(exist_ok=False)
  old.save(target/'request.json',payload)
  record={'case':cid,'status':'reserved','request_digest':digest,'reserve_usd':str(old.RESERVE),'started_at':time.time(),
          'driver_digest':base.digest(Path(__file__).read_bytes()),'capture_digest':base.digest(Path(capture.__file__).read_bytes())}
  old.save(target/'record.json',record);start=time.monotonic();phase='transport'
  try:
   reply=capture.request(payload,key,timeout,target)
   phase='response_artifact';old.save(target/'response.json',reply)  # BEFORE validation, including invalid responses.
   if isinstance(reply,dict) and reply.get('model')==core.MODEL:
    usage=reply.get('usage',{})
    if all(type(usage.get(k)) is int and 0<=usage[k]<=65536 for k in ('input_tokens','output_tokens')):
     record.update(input_tokens=usage['input_tokens'],output_tokens=usage['output_tokens'],actual_usd=str(Decimal(usage['input_tokens'])*old.PRICE))
   phase='validation';core.validate_response(payload,reply)
   if time.monotonic()-start>=timeout:raise capture.CaptureError({'phase':'validation','failure_kind':'deadline'})
   record.update(status='validated',response_digest=core.digest(reply),model_actual=reply['model'],elapsed_seconds=time.monotonic()-start)
   old.save(target/'record.json',record)
   return reply
  except core.InvalidResponse as error:
   record.update(status='invalid_response',diagnostic={'phase':'validation',**error.diagnostic})
  except capture.CaptureError as error:
   record.update(status='transport_failed',diagnostic=error.diagnostic)
  except (OSError,ValueError,TypeError,KeyError) as error:
   record.update(status='artifact_failed' if 'artifact' in phase else 'internal_failed',diagnostic={'phase':phase,'error_type':type(error).__name__})
  except BaseException:
   record.update(status='interrupted',diagnostic={'phase':phase});old.save(target/'record.json',record);raise
  finally:
   record['elapsed_seconds']=time.monotonic()-start
  old.save(target/'record.json',record)
  self.last_failure=record['diagnostic']
  raise RecordedFailure(record['diagnostic'])

def fingerprints():
 paths=[Path(__file__),Path(capture.__file__),ROOT/'benchmarks/jev_pilot.py',ROOT/'benchmarks/editorial_pilot.py',*sorted((ROOT/'jev').glob('*.py')),ROOT/'jev/registry.json']
 return {str(p.relative_to(ROOT)):base.digest(p.read_bytes()) for p in paths}

def prepare(out,origin):
 with contextlib.redirect_stdout(io.StringIO()):old.validate_epoch(origin)
 m={'config_version':'jev-recovery-v1','origin':str(origin),'origin_manifest_digest':base.digest(old.read(origin/'manifest.json')),
    'input_digests':{k:base.digest(v) for k,v in old.read(origin/'inputs.json').items()},'source_fingerprints':fingerprints(),
    'origin_evidence':{str(p.relative_to(origin)):base.digest(p.read_bytes()) for folder in ('requests','evaluations') for p in sorted((origin/folder).rglob('*')) if p.is_file()},
    'models':{'codex':base.MODELS['codex'],'jev':core.MODEL},'effort':'medium','cash_cap_usd':'2','policy_version':None,
    'max_network_requests_total':640,'max_network_requests_per_case_total':32,'max_passes_per_case':3,'max_new_codex_starts':20,
    'revision_instruction':old.REVISION,'cells':[f'codex/{cid}/vietnamizer_jev' for cid in old.read(origin/'inputs.json')]}
 out.mkdir(parents=True,exist_ok=True);base.freeze_manifest(out/'manifest.json',m)
 for p in (Path(__file__),Path(capture.__file__)):old.save(out/'source-digests'/f'{p.stem}.json',{'sha256':base.digest(p.read_bytes())});(out/'source-digests'/p.name).write_bytes(p.read_bytes())
 (out/'prompts').mkdir(exist_ok=True)
 return m

def validate(out):
 m=old.read(out/'manifest.json')
 if m['source_fingerprints']!=fingerprints():raise ValueError('recovery driver drift')
 origin=Path(m['origin'])
 if base.digest(old.read(origin/'manifest.json'))!=m['origin_manifest_digest']:raise ValueError('origin manifest drift')
 with contextlib.redirect_stdout(io.StringIO()):old.validate_epoch(origin)
 for relative,expected in m['origin_evidence'].items():
  if base.digest((origin/relative).read_bytes())!=expected:raise ValueError('origin evidence drift')
 if {k:base.digest(v) for k,v in old.read(origin/'inputs.json').items()}!=m['input_digests']:raise ValueError('input drift')
 return m,origin

def diagnostic(out,cid,max_new=1):
 m,origin=validate(out);store=Store(out,[origin],max_new=max_new);store.load_cache(origin)
 doc=old.read(origin/'inputs.json')[cid];folder=out/'evaluations'/cid;folder.mkdir(parents=True,exist_ok=True)
 paths=sorted(folder.glob('pass-*.json'))
 if len(paths)>=3:raise ValueError('pass cap')
 target=folder/f'pass-{len(paths)+1}.json'
 old.save(target,{'case':cid,'status':'started','input_digest':core.digest(doc),'manifest_digest':base.digest(m)})
 result=core.evaluate(doc,transport=lambda p,k,t:store.send(cid,p,k,t))
 result.update(case=cid,manifest_digest=base.digest(m),replayed=store.replayed,stop_diagnostic=store.last_failure)
 old.save(target,result)
 target.with_suffix('.sha256').write_text(base.digest(result))
 print(json.dumps({'case':cid,'status':result['status'],'full':result.get('scope_complete'),
  'validated_checks':result.get('counts',{}).get('validated'),'missing':result.get('counts',{}).get('uncompleted'),
  'replayed':len(store.replayed),'budget':store.summary(),'last_new_request':store.entries()[-1] if store.entries() else None},ensure_ascii=False),flush=True)
 return result

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('command',choices=('prepare','evaluate'))
 ap.add_argument('--output',required=True,type=Path);ap.add_argument('--origin',type=Path,default=ROOT/'artifacts/014-codex-jev-20261025-v2');ap.add_argument('--case',default='P01');ap.add_argument('--max-new',type=int,default=1)
 a=ap.parse_args();out=a.output.resolve()
 with old.writer(out):
  if a.command=='prepare':prepare(out,a.origin.resolve());print('Prepared recovery, USD2 cumulative');return
  if not 1<=a.max_new<=32:raise ValueError('max-new must be1..32')
  diagnostic(out,a.case,a.max_new)
if __name__=='__main__':main()
