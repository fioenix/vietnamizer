"""Audited per-question recovery: no resampling of a valid semantic answer."""
import argparse,contextlib,copy,json,sys
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from benchmarks import jev_finish as finish,jev_recovery as rec
from jev import core
old=finish.old;base=finish.base;OriginalStore=rec.Store


def subset(payload,reply,names):
 p={**payload,'questions':{n:payload['questions'][n] for n in names}}
 r={**reply,'answers':{n:reply['answers'][n] for n in names}}
 return p,r


def split_answers(payload,reply):
 # Envelope/model/usage/IDs must be sound before any per-question salvage.
 if not isinstance(reply,dict) or reply.get('model')!=core.MODEL or not isinstance(reply.get('answers'),dict) or set(reply['answers'])!=set(payload['questions']):raise ValueError('unsalvageable envelope')
 core.validate_response(*subset(payload,reply,[]))
 valid=[];invalid=[]
 for name in payload['questions']:
  try:core.validate_response(*subset(payload,reply,[name]));valid.append(name)
  except core.InvalidResponse as e:
   if e.diagnostic['reason'] not in ('score_distribution','choice_distribution'):raise ValueError('unsupported invalid answer') from e
   invalid.append(name)
 if not invalid:raise ValueError('no invalid answers to repair')
 return valid,invalid


def amendment(out):
 fm=old.read(out/'finish-manifest.json')
 data={'version':'per-question-recovery-v1','source_digest':base.digest(Path(__file__).read_bytes()),
  'finish_manifest_digest':base.digest(fm),'allowed_failure':['score_distribution','choice_distribution'],
  'policy':'retain valid answers; request invalid questions only, same full state/model/question; at most one repair network attempt per original invalid response',
  'accounting':'composite replies are derived artifacts, never additional network requests; sum distinct real source usage, ledger billed once',
  'caps':'unchanged cumulative USD2 / 640 network / 32 per case / 3 passes / 20 Codex starts'}
 base.freeze_manifest(out/'composite-manifest.json',data);return data


def verify_amendment(out):
 expected=old.read(out/'composite-manifest.json')
 if expected['source_digest']!=base.digest(Path(__file__).read_bytes()) or expected['finish_manifest_digest']!=base.digest(old.read(out/'finish-manifest.json')):raise ValueError('composite adapter drift')
 finish.verify(out);return expected


def source(out,relative):
 path=out/relative
 if Path(relative).is_absolute() or '..' in Path(relative).parts or path.name!='record.json' or path.parent.parent!=out/'requests':raise ValueError('source outside network ledger')
 record=old.read(path);payload=old.read(path.parent/'request.json');reply=old.read(path.parent/'response.json');http=old.read(path.parent/'http.json')
 if not http.get('body_complete') or http.get('http_status')!=200 or base.digest((path.parent/'response.body').read_bytes())!=http['stored_body_digest'] or json.loads((path.parent/'response.body').read_bytes())!=reply:raise ValueError('source body drift/incomplete')
 if core.digest(payload)!=record['request_digest'] or record.get('actual_usd') is None:raise ValueError('source binding/usage missing')
 if any(record.get(k)!=reply.get('usage',{}).get(k) for k in ('input_tokens','output_tokens')) or type(record.get('input_tokens')) is not int or not 0<=record['input_tokens']<=65536 or Decimal(record['actual_usd'])!=Decimal(record['input_tokens'])*old.PRICE:raise ValueError('source ledger usage mismatch')
 if json.loads((path.parent/'request.body').read_bytes())!=payload:raise ValueError('request wire drift')
 return record,payload,reply


def validate_composite(out,folder):
 verify_amendment(out)
 record=old.read(folder/'record.json');payload=old.read(folder/'request.json');reply=old.read(folder/'response.json')
 if (folder/'record.sha256').read_text()!=base.digest(record) or record['amendment_digest']!=base.digest(old.read(out/'composite-manifest.json')):raise ValueError('composite seal drift')
 if record['kind']!='composite_evidence' or record['request_digest']!=core.digest(payload) or record['response_digest']!=core.digest(reply) or set(record['answer_sources'])!=set(payload['questions']):raise ValueError('composite binding drift')
 cache={};used=set()
 expected_sources=set(record['answer_sources'].values())
 if set(record['source_digests'])!=expected_sources:raise ValueError('source inventory mismatch')
 for relative,bindings in record['source_digests'].items():
  if set(bindings)!=set(('record.json','request.json','request.body','response.json','response.body','http.json')):raise ValueError('source file inventory mismatch')
  for name,digest in bindings.items():
   if base.digest((out/relative).parent.joinpath(name).read_bytes())!=digest:raise ValueError('source snapshot drift')
 for name,relative in record['answer_sources'].items():
  if relative not in cache:cache[relative]=source(out,relative)
  r,p,a=cache[relative];used.add(relative)
  if r['case']!=record['case'] or p.get('state')!=payload.get('state') or p['model']!=payload['model'] or p['questions'].get(name)!=payload['questions'][name]:raise ValueError('per-question source mismatch')
  core.validate_response(*subset(p,a,[name]))
  if reply['answers'][name]!=a['answers'][name]:raise ValueError('answer rewritten')
 if reply['usage']!={k:sum(cache[x][2]['usage'][k] for x in used) for k in ('input_tokens','output_tokens')}:raise ValueError('composite usage drift')
 core.validate_response(payload,reply)
 return record,payload,reply


class CompositeStore(OriginalStore):
 def load_cache(self,origin):
  # Same checks as the frozen store; explicitly resolve composite receipts first.
  composites={}
  for folder in sorted((self.out/'composites').glob('*/*')):
   r,p,a=validate_composite(self.out,folder)
   composites[(r['case'],core.digest(p))]={'reply':a,'origin':str(folder/'record.json')}
  with contextlib.redirect_stdout(__import__('io').StringIO()):old.validate_epoch(origin)
  rows={r['request_digest']:p for p in sorted((origin/'requests').glob('*.json')) if (r:=old.read(p))['status']=='validated'}
  for path in sorted((origin/'evaluations').glob('*/result.json')):
   r=old.read(path);cid=path.parent.name
   old.verify_binding(old.read(origin/'manifest.json'),cid,old.read(origin/'inputs.json')[cid],r);old.verified_checks(origin,cid,r)
   for receipt in r.get('receipts',[]):
    if receipt['status']!='validated':continue
    p=rows[receipt['request_digest']];payload=old.read(p.with_suffix('.request.json.raw'));reply=old.read(p.with_suffix('.response.json.raw'));core.validate_response(payload,reply)
    self.cache[(cid,core.digest(payload))]={'reply':reply,'origin':str(p)}
  self.cache.update(composites)
  for path in sorted((self.out/'evaluations').glob('*/*.json')):
   r=old.read(path);cid=r['case']
   if path.with_suffix('.sha256').read_text()!=base.digest(r) or r['manifest_digest']!=base.digest(old.read(self.out/'manifest.json')) or r['input_digest']!=core.digest(old.read(origin/'inputs.json')[cid]):raise ValueError('evaluation seal/binding drift')
   for receipt in r.get('receipts',[]):
    if receipt['status']!='validated':continue
    key=(cid,receipt['request_digest'])
    if key in composites:
     a=composites[key]['reply']
     if core.digest(a)!=receipt['response_digest'] or core.validate_response(old.read(Path(composites[key]['origin']).parent/'request.json'),a)[1]!=receipt['usage']:raise ValueError('composite receipt drift')
     continue
    match=[p for p in (self.out/'requests').glob('*/record.json') if old.read(p)['case']==cid and old.read(p)['request_digest']==receipt['request_digest']]
    if not match:continue
    p=match[-1];record=old.read(p);payload=old.read(p.parent/'request.json');reply=old.read(p.parent/'response.json');_,usage=core.validate_response(payload,reply)
    if record['status']!='validated' or record['response_digest']!=core.digest(reply) or core.digest(payload)!=receipt['request_digest'] or receipt['response_digest']!=core.digest(reply) or receipt['usage']!=usage:raise ValueError('network receipt drift')
    self.cache[key]={'reply':reply,'origin':str(p)}


def repair(out,cid,request_id):
 am=verify_amendment(out);relative=f'requests/{request_id}/record.json';record,payload,reply=source(out,relative)
 if record['case']!=cid or record['status']!='invalid_response' or record.get('diagnostic',{}).get('reason') not in ('score_distribution','choice_distribution'):raise ValueError('not eligible for per-question repair')
 good,bad=split_answers(payload,reply);folder=out/'composites'/cid/core.digest(payload)
 if folder.exists():return validate_composite(out,folder)
 ticket=out/'repair-attempts'/f'{cid}-{request_id}.json'
 if ticket.exists():raise ValueError('repair already attempted; inspect, never reroll')
 p,_=subset(payload,reply,bad)
 ticket.parent.mkdir(parents=True,exist_ok=True)
 old.save(ticket,{'original':relative,'invalid_questions':bad,'request_digest':core.digest(p),'status':'started','amendment_digest':base.digest(am)})
 _,origin=rec.validate(out);store=CompositeStore(out,[origin],max_new=1)
 # Repair is a fresh bounded call only for invalid checks, not a replay of valid answers.
 a=store.send(cid,p,__import__('os').environ['TYPESAFE_API_KEY'],15)
 fresh=store.entries()[-1];new_relative=f'requests/{len(store.entries()):04d}/record.json'
 if fresh['request_digest']!=core.digest(p):raise ValueError('repair evidence mismatch')
 answers=copy.deepcopy(reply['answers']);answers.update(a['answers'])
 composite={'model':core.MODEL,'answers':answers,'usage':{k:reply['usage'][k]+a['usage'][k] for k in ('input_tokens','output_tokens')}}
 core.validate_response(payload,composite)
 folder.mkdir(parents=True,exist_ok=False)
 old.save(folder/'request.json',payload);old.save(folder/'response.json',composite)
 proof={'kind':'composite_evidence','case':cid,'amendment_digest':base.digest(am),'request_digest':core.digest(payload),'response_digest':core.digest(composite),
  'original_request':relative,'repair_request':new_relative,'invalid_questions':bad,
  'answer_sources':{name:relative if name in good else new_relative for name in payload['questions']},
  'source_digests':{rel:{name:base.digest((out/rel).parent.joinpath(name).read_bytes()) for name in ('record.json','request.json','request.body','response.json','response.body','http.json')} for rel in (relative,new_relative)}}
 old.save(folder/'record.json',proof);(folder/'record.sha256').write_text(base.digest(proof))
 old.save(ticket,{**old.read(ticket),'status':'completed','composite':str(folder.relative_to(out))})
 return validate_composite(out,folder)


@contextlib.contextmanager
def installed(out):
 verify_amendment(out);previous=rec.Store;rec.Store=CompositeStore
 try:yield
 finally:rec.Store=previous


def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('command',choices=('prepare','repair','report'));ap.add_argument('--output',type=Path,required=True);ap.add_argument('--case');ap.add_argument('--request-id')
 a=ap.parse_args();out=a.output.resolve()
 with old.writer(out):
  if a.command=='prepare':amendment(out);return
  with installed(out):
   if a.command=='repair':
    repair(out,a.case,a.request_id);rec.diagnostic(out,a.case,32);finish.complete(out,a.case)
   finish.report(out)
if __name__=='__main__':main()
