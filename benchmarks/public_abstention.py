"""Terminal abstention after an exhausted schema repair, never a third semantic draw."""
import argparse,json
from pathlib import Path
from benchmarks import public_deadline as d
r=d.r;pub=d.pub;old=d.old;base=d.base;core=d.core
OriginalEvaluate=d.evaluate
OriginalAdvice=d.advice

def prepare(out):
 m=pub.verify(out);paths=[Path(__file__),Path(d.__file__),out/'STOP_DEADLINE',out/'deadline-manifest.json',out/'evaluations/R013/recovered.json',out/'evaluations/R013/recovered.seal.json',*sorted((out/'requests/0404').glob('*')),*sorted((out/'requests/0405').glob('*')),*sorted((out/'repair-attempts').glob('R013-0404.json'))]
 a={'schema':'public-terminal-schema-abstention-v1','parent_digest':base.digest(m),'fingerprints':{str(p.resolve()):base.digest(p.read_bytes()) for p in paths},'policy':'After exactly one failed score/choice distribution repair, accept only validated prefix, keep failed batch unavailable, no further Jev calls for that source; never third semantic draw. Other failures still stop. Existing caps/models/sources/arms unchanged.','authority':'Owner-authorized partial/fallback benchmark completion, architecture checkpoint and independent implementation review before execution.'}
 base.freeze_manifest(out/'abstention-manifest.json',a);return a

def verify(out):
 a=old.read(out/'abstention-manifest.json');m=pub.verify(out)
 if a['parent_digest']!=base.digest(m):raise ValueError('abstention parent drift')
 for name,h in a['fingerprints'].items():
  if base.digest(Path(name).read_bytes())!=h:raise ValueError('abstention source/evidence drift')
 dm=old.read(out/'deadline-manifest.json');previous=old.read(out/'recovery-manifest.json')
 if dm['parent_digest']!=base.digest(m) or dm['previous_digest']!=base.digest(previous):raise ValueError('deadline parent drift')
 for name,h in dm['fingerprints'].items():
  if base.digest(Path(name).read_bytes())!=h:raise ValueError('deadline frozen evidence drift')
 if previous['source_digest']!=base.digest(Path(r.__file__).read_bytes()) or previous['helper_digest']!=base.digest(Path(r.comp.__file__).read_bytes()):raise ValueError('recovery source drift')
 if (out/'STOP_ABSTENTION').exists():raise ValueError('unreviewed terminal failure; stop')
 return previous

def certificate(out,cid,result):
 failed=[x for x in result['receipts'] if x['status']!='validated']
 if len(failed)!=1 or result.get('scope_complete') or result.get('evaluation_complete'):raise ValueError('not terminal partial schema failure')
 receipt=failed[0];matches=[p for p in sorted((out/'requests').glob('*/record.json')) if old.read(p)['case']==cid and old.read(p)['request_digest']==receipt['request_digest']]
 if len(matches)!=1:raise ValueError('ambiguous original failure')
 path=matches[0];rel=str(path.relative_to(out));record,p,a=r.network(out,rel)
 if record['status']!='invalid_response' or record.get('diagnostic',{}).get('reason') not in ('score_distribution','choice_distribution'):raise ValueError('unsupported terminal failure')
 good,bad=r.comp.split_answers(p,a)
 if receipt['question_ids']!=list(p['questions']) or receipt['status']!='service_failed':raise ValueError('failed receipt scope drift')
 ticket=out/'repair-attempts'/f'{cid}-{path.parent.name}.json';t=old.read(ticket);repair_payload,_=r.comp.subset(p,a,bad)
 if t.get('status')!='started' or t.get('original')!=rel or t.get('invalid_questions')!=bad or t.get('request_digest')!=core.digest(repair_payload):raise ValueError('not exactly one attempted repair')
 matches=[x for x in sorted((out/'requests').glob('*/record.json')) if old.read(x)['case']==cid and old.read(x)['request_digest']==core.digest(repair_payload)]
 if len(matches)!=1:raise ValueError('repair request count drift')
 retry=str(matches[0].relative_to(out));rr,rp,ra=r.network(out,retry)
 if rp!=repair_payload or rr['status']!='invalid_response' or rr.get('diagnostic',{}).get('reason') not in ('score_distribution','choice_distribution'):raise ValueError('repair did not end in eligible schema failure')
 r.comp.split_answers(rp,ra)
 if any(int(x.parent.name)>int(matches[0].parent.name) and old.read(x)['case']==cid for x in (out/'requests').glob('*/record.json')):raise ValueError('network continued after terminal abstention')
 if (out/'composites'/cid/core.digest(p)).exists():raise ValueError('invalid response promoted to composite')
 return {'case':cid,'status':'service_partial','result_digest':base.digest(result),'amendment_digest':base.digest(old.read(out/'abstention-manifest.json')),'original':rel,'repair':retry,'omitted_question_ids':receipt['question_ids'],'invalid_question_ids':bad,'policy':'failed batch unavailable; valid prefix only; no further Jev dispatch','fingerprints':{str(x.relative_to(out)):base.digest(x.read_bytes()) for x in [ticket,*sorted(path.parent.glob('*')),*sorted(matches[0].parent.glob('*'))]}}

def dispose(out,cid,result):
 c=certificate(out,cid,result);base.freeze_manifest(out/'evaluations'/cid/'service-abstention.json',c);return c

def advice(out,cid,result):
 verify(out);target=out/'evaluations'/cid/'recovered.json';m=pub.verify(out)
 if old.read(target.with_suffix('.seal.json'))['digest']!=base.digest(result) or result['manifest_digest']!=base.digest(m) or result['input_digest']!=core.digest(old.read(out/'inputs.json')[cid]) or result['recovery_digest']!=base.digest(old.read(out/'recovery-manifest.json')):raise ValueError('result binding drift')
 # Preserve the deadline adapter's provenance contract even on schema-abstaining cases.
 for info in result.get('deadline_retries',[]):
  path=out/'deadline-attempts'/f"{cid}-{info['request_digest']}.json";record,p,a=r.network(out,info['retry'])
  if old.read(path)!=info or info['case']!=cid or info['status']!='completed' or info['amendment_digest']!=base.digest(old.read(out/'deadline-manifest.json')) or info['original_record_digest']!=base.digest(old.read(out/info['original'])) or not d.eligible(out,info['original'],cid,p) or record['case']!=cid or record['status']!='validated' or info['request_digest']!=core.digest(p) or info['retry'] not in result['evidence_trace']:raise ValueError('deadline retry proof drift')
 failed=[x for x in result['receipts'] if x['status']!='validated'];cert=None
 if failed and (result.get('stop_diagnostic') or {}).get('phase')!='budget':
  cert=certificate(out,cid,result)
  if old.read(target.parent/'service-abstention.json')!=cert:raise ValueError('abstention certificate drift')
 # Existing validated-result path also checks transport-retry provenance.
 if cert is None:return OriginalAdvice(out,cid,result)
 if len(result['evidence_trace'])!=sum(x['status']=='validated' for x in result['receipts']):raise ValueError('trace count drift')
 trace=iter(result['evidence_trace']);checks=[];answers={}
 for receipt in result['receipts']:
  if receipt['status']!='validated':continue
  rel=next(trace)
  if rel.startswith('composites/'):record,p,a=r.composite(out,(out/rel).parent)
  else:
   record,p,a=r.network(out,rel)
   if record['status']!='validated':raise ValueError('invalid evidence accepted')
  clean,usage=core.validate_response(p,a)
  if record['case']!=cid or receipt['request_digest']!=core.digest(p) or receipt['response_digest']!=core.digest(a) or receipt['usage']!=usage:raise ValueError('receipt proof mismatch')
  checks.append({'state':p.get('state',{}),'questions':p['questions'],'answers':clean});answers.update({(receipt['request_digest'],n):v for n,v in clean.items()})
 for j in result['judgments']:
  if answers.get((j['request_digest'],j['check']))!=j['answer']:raise ValueError('unverified judgment')
 a=old.advice_for(result,[],checks);a.update(service_disposition='terminal_schema_abstention',service_status='partial',unavailable_question_ids=cert['omitted_question_ids']);return a

def evaluate(out,cid):
 verify(out);target=out/'evaluations'/cid/'recovered.json'
 if target.exists():
  result=old.read(target)
  if any(x['status']!='validated' for x in result['receipts']) and (result.get('stop_diagnostic') or {}).get('phase')!='budget':dispose(out,cid,result)
  advice(out,cid,result);return result
 try:return OriginalEvaluate(out,cid)
 except ValueError:
  try:
   result=old.read(target);dispose(out,cid,result);advice(out,cid,result)
  except BaseException:
   (out/'STOP_ABSTENTION').write_text('Failure outside reviewed terminal-schema abstention; preserve evidence and stop.\n');raise
  print(json.dumps({'case':cid,'service_disposition':'terminal_schema_abstention','no_further_jev_calls_for_case':True}),flush=True);return result

def run(out,limit):
 pv,pe,pa=d.verify,d.evaluate,d.advice;d.verify=verify;d.evaluate=evaluate;d.advice=advice
 try:return d.run(out,limit)
 finally:d.verify=pv;d.evaluate=pe;d.advice=pa

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=('prepare','run'));p.add_argument('--output',type=Path,required=True);p.add_argument('--limit',type=int,default=1);a=p.parse_args();print(json.dumps(prepare(a.output) if a.command=='prepare' else run(a.output,a.limit)))
