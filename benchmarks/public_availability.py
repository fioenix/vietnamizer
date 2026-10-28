"""Availability abstention for an exhausted empty-body deadline pair; no new retries."""
import argparse,json
from pathlib import Path
from benchmarks import public_abstention as a
r=a.r;d=a.d;pub=a.pub;old=a.old;base=a.base;core=a.core
OriginalCertificate=a.certificate;OriginalAdvice=a.advice

def prepare(out):
 m=pub.verify(out);paths=[Path(__file__),out/'STOP_ABSTENTION',out/'evaluations/R019/recovered.json',out/'evaluations/R019/recovered.seal.json',*sorted((out/'requests/0546').glob('*')),*sorted((out/'requests/0547').glob('*')),*sorted((out/'deadline-attempts').glob('R019-*'))]
 m4={'schema':'public-availability-abstention-v1','parent_digest':base.digest(m),'schema_parent_digest':base.digest(old.read(out/'abstention-manifest.json')),'fingerprints':{str(p.resolve()):base.digest(p.read_bytes()) for p in paths},'policy':'After exactly one exhausted empty opening-deadline retry, preserve both unknown reservations, terminally abstain for that source, no further case dispatch. Retain only validated prefix. Other failures still stop. All caps/models/source/arms unchanged.','deadline_interpretation':'R019attempts ended around1.1s under remaining overall120s evaluation budget; not demonstrated service outage.','authority':'Owner-authorized bounded partial/fallback benchmark completion; independently reviewed architecture and implementation before execution.'}
 base.freeze_manifest(out/'availability-manifest.json',m4);return m4

def verify(out):
 m=pub.verify(out);m4=old.read(out/'availability-manifest.json')
 if m4['parent_digest']!=base.digest(m) or m4['schema_parent_digest']!=base.digest(old.read(out/'abstention-manifest.json')):raise ValueError('availability parent drift')
 for doc in (m4,old.read(out/'abstention-manifest.json'),old.read(out/'deadline-manifest.json')):
  if doc['parent_digest']!=base.digest(m):raise ValueError('parent binding drift')
  for name,h in doc['fingerprints'].items():
   if base.digest(Path(name).read_bytes())!=h:raise ValueError('source/evidence drift')
 previous=old.read(out/'recovery-manifest.json')
 if old.read(out/'deadline-manifest.json')['previous_digest']!=base.digest(previous) or previous['source_digest']!=base.digest(Path(r.__file__).read_bytes()) or previous['helper_digest']!=base.digest(Path(r.comp.__file__).read_bytes()):raise ValueError('recovery ancestor drift')
 if (out/'STOP_AVAILABILITY').exists():raise ValueError('unreviewed availability failure; stop')
 return previous

def certificate(out,cid,result):
 diag=result.get('stop_diagnostic') or {}
 if diag.get('failure_kind')!='deadline':return OriginalCertificate(out,cid,result)
 failed=[x for x in result['receipts'] if x['status']!='validated']
 if len(failed)!=1 or result['scope_complete'] or result['evaluation_complete']:raise ValueError('not terminal deadline partial')
 receipt=failed[0];paths=[p for p in sorted((out/'requests').glob('*/record.json')) if old.read(p)['case']==cid and old.read(p)['request_digest']==receipt['request_digest']]
 if len(paths)!=2:raise ValueError('not exactly two deadline attempts')
 p=old.read(paths[0].parent/'request.json');rels=[str(x.relative_to(out)) for x in paths]
 if receipt['question_ids']!=list(p['questions']) or receipt['status']!='service_failed' or not all(d.eligible(out,rel,cid,p) for rel in rels):raise ValueError('deadline scope mismatch')
 records=[old.read(x) for x in paths]
 if any('actual_usd' in x or x['reserve_usd']!=str(old.RESERVE) for x in records):raise ValueError('unknown reservations changed')
 for x in paths:
  if old.read(x.parent/'http.json')['stored_body_digest']!=base.digest(b''):raise ValueError('empty-body digest drift')
 ticket=out/'deadline-attempts'/f'{cid}-{core.digest(p)}.json';t=old.read(ticket)
 if t!={'status':'started','case':cid,'request_digest':core.digest(p),'original':rels[0],'original_record_digest':base.digest(records[0]),'amendment_digest':base.digest(old.read(out/'deadline-manifest.json'))}:raise ValueError('deadline retry ticket drift')
 if any(int(x.parent.name)>int(paths[-1].parent.name) and old.read(x)['case']==cid for x in (out/'requests').glob('*/record.json')):raise ValueError('continued after terminal availability abstention')
 if (out/'composites'/cid/core.digest(p)).exists():raise ValueError('transport failure promoted to composite')
 return {'case':cid,'status':'service_partial','kind':'terminal_availability_abstention','result_digest':base.digest(result),'amendment_digest':base.digest(old.read(out/'availability-manifest.json')),'original':rels[0],'repair':rels[1],'omitted_question_ids':receipt['question_ids'],'invalid_question_ids':[],'unknown_billing_attempts':2,'observed_attempt_elapsed_seconds':[x['elapsed_seconds'] for x in records],'interpretation':'No response under remaining evaluation deadline; no demonstrated service outage.','policy':'failed batch unavailable; validated prefix only; no further case dispatch','fingerprints':{str(x.relative_to(out)):base.digest(x.read_bytes()) for x in [ticket,*sorted(paths[0].parent.glob('*')),*sorted(paths[1].parent.glob('*'))]}}

def advice(out,cid,result):
 result_advice=OriginalAdvice(out,cid,result)
 if (result.get('stop_diagnostic') or {}).get('failure_kind')=='deadline' and any(x['status']!='validated' for x in result['receipts']):result_advice['service_disposition']='terminal_availability_abstention'
 return result_advice

def run(out,limit):
 pv,pc,pa=a.verify,a.certificate,a.advice;a.verify=verify;a.certificate=certificate;a.advice=advice
 try:return a.run(out,limit)
 except BaseException:
  (out/'STOP_AVAILABILITY').write_text('Failure outside reviewed final availability disposition; preserve evidence and stop.\n');raise
 finally:a.verify=pv;a.certificate=pc;a.advice=pa

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=('prepare','run'));p.add_argument('--output',type=Path,required=True);p.add_argument('--limit',type=int,default=1);t=p.parse_args();print(json.dumps(prepare(t.output) if t.command=='prepare' else run(t.output,t.limit)))
