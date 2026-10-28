"""Finish the recorded recovery; never classify fallback as Jev completion."""
import argparse,contextlib,io,json,random,time
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from benchmarks import jev_recovery as rec,jev_pilot as old,editorial_pilot as base
from jev import core


def retryable(d):
 return bool(d and (d.get('failure_kind') in ('timeout','deadline','network') or d.get('http_status')==429 or
                    type(d.get('http_status')) is int and 500<=d['http_status']<=599))


def answers_done(r):
 counts=r.get('counts',{})
 return bool(r.get('answers_complete') and r.get('source_accounted') and r.get('segmentation_complete') and counts.get('uncompleted')==0 and counts.get('validated',0)>0)

def require_answers(r):
 if not answers_done(r):raise ValueError('Jev answers incomplete; no fallback completion')


def freeze(out):
 m,origin=rec.validate(out)
 parent=Path(old.read(origin/'manifest.json')['parent'])
 refs={}
 for directory,arms in ((parent,('bare','ordinary')),(origin,('vietnamizer_review',))):
  for cid in m['input_digests']:
   for arm in arms:
    name=f'codex-{cid}-{arm}'
    for file in ('result.json','stdout.txt'):
     path=directory/'attempts'/name/file
     refs[str(path)]=base.digest(path.read_bytes())
 fm={'config_version':'jev-finish-v1','recovery_manifest_digest':base.digest(m),
     'finish_source_digest':base.digest(Path(__file__).read_bytes()),'controls_and_baselines':refs,
     'completion':'all required answers received; semantic context uncertainty preserved, never rerolled',
     'max_new_codex_starts':20,'max_case_passes':3,'retryable':'timeout/deadline/network/HTTP429/5xx only',
     'max_network_requests_total':640,'max_network_requests_per_case_total':32,'cash_cap_usd':'2',
     'reused_controls':str(origin),'reused_baselines':str(parent),'policy_version':None}
 base.freeze_manifest(out/'finish-manifest.json',fm)
 return fm


def verify(out):
 m,origin=rec.validate(out);fm=old.read(out/'finish-manifest.json')
 if fm['recovery_manifest_digest']!=base.digest(m) or fm['finish_source_digest']!=base.digest(Path(__file__).read_bytes()):raise ValueError('finish source/manifest drift')
 for file,digest in fm['controls_and_baselines'].items():
  if base.digest(Path(file).read_bytes())!=digest:raise ValueError('control/baseline drift')
 return m,origin,fm


def passes(out,cid):
 rows=[]
 for path in sorted((out/'evaluations'/cid).glob('pass-*.json')):
  r=old.read(path)
  if not path.with_suffix('.sha256').exists() or path.with_suffix('.sha256').read_text()!=base.digest(r):raise ValueError('unsealed/interrupted pass: inspect before more work')
  rows.append(r)
 return rows


def evidence(out,cid,result):
 m,origin,fm=verify(out);require_answers(result)
 doc=old.read(origin/'inputs.json')[cid]
 if result['manifest_digest']!=base.digest(m) or result['input_digest']!=core.digest(doc):raise ValueError('evaluation binding mismatch')
 store=rec.Store(out,[origin]);store.load_cache(origin)
 checks=[];answers={}
 for receipt in result['receipts']:
  if receipt['status']!='validated':raise ValueError('nonvalidated receipt in full result')
  item=store.cache.get((cid,receipt['request_digest']))
  if not item:raise ValueError('missing exact cache evidence')
  p=Path(item['origin'])
  payload=old.read(p.parent/'request.json') if p.name=='record.json' else old.read(p.with_suffix('.request.json.raw'))
  reply=item['reply'];clean,usage=core.validate_response(payload,reply)
  if core.digest(payload)!=receipt['request_digest'] or core.digest(reply)!=receipt['response_digest'] or receipt['usage']!=usage:raise ValueError('receipt/raw mismatch')
  checks.append({'state':payload['state'],'questions':payload['questions'],'answers':clean})
  for name,value in clean.items():answers[(receipt['request_digest'],name)]=value
 for judgment in result['judgments']:
  if answers.get((judgment['request_digest'],judgment['check']))!=judgment['answer']:raise ValueError('judgment mismatch')
 def replay_only(payload,*_):
  item=store.cache.get((cid,core.digest(payload)))
  if not item:raise ValueError('proof requires missing evidence')
  return item['reply']
 proof=core.evaluate(doc,environ={'TYPESAFE_API_KEY':'offline-proof-only'},transport=replay_only)
 require_answers(proof)
 if proof['counts']!=result['counts']:raise ValueError('coverage proof mismatch')
 return checks


def complete(out,cid):
 m,origin,fm=verify(out)
 rows=passes(out,cid)
 while not rows or not answers_done(rows[-1]):
  if rows:
   d=rows[-1].get('stop_diagnostic')
   if d and d.get('reason')!='new_request_limit' and not retryable(d):raise ValueError('nonretryable failure: inspect raw evidence and correct offline')
   if retryable(d):
    delay=min(60,max(2,d.get('retry_after_seconds',2)))
    print(json.dumps({'case':cid,'retry_wait_seconds':delay,'cause':d}),flush=True)
    time.sleep(delay)
  if len(rows)>=3:raise ValueError('bounded recovery pass cap reached')
  rec.diagnostic(out,cid,32);rows=passes(out,cid)
 result=rows[-1];checks=evidence(out,cid,result)
 target=out/'attempts'/f'codex-{cid}-vietnamizer_jev'
 if target.exists():
  if old.read(target/'result.json')['status']!='completed':raise ValueError('Codex cell already attempted; no automatic generation retry')
  return
 if len(list((out/'attempts').glob('*/result.json')))>=20:raise ValueError('new Codex start cap')
 case=next(c for c in old.read(origin/'frozen-corpus.json')['cases'] if c['id']==cid)
 prompt=old.revision_prompt(old.read(origin/'prefixes.json')[cid],case,old.read(origin/'drafts.json')[cid],
     dict(old.advice_for(result,old.read(origin/'candidate-omissions.json')[cid],checks),
          answers_complete=result['answers_complete'],context_complete=result['context_complete'],
          evaluation_complete=result['evaluation_complete'],
          semantic_uncertainty=[{'section':j['section'],'check':j['check'],'disposition':j['disposition']} for j in result['judgments'] if j.get('disposition','').startswith('ignore_')]))
 if len(prompt.encode())>1000000:raise ValueError('prompt too large')
 path=out/'prompts'/f'{cid}-vietnamizer_jev.txt'
 if path.exists() and path.read_text()!=prompt:raise ValueError('prompt drift')
 path.write_text(prompt)
 r=base.run_one(out,f'codex/{cid}/vietnamizer_jev')
 r.update(finish_manifest_digest=base.digest(fm),evaluation_digest=base.digest(result))
 old.save(target/'result.json',r)
 if r['status']!='completed':raise ValueError('Codex generation incomplete; inspect raw output')


def report(out):
 m,origin,fm=verify(out);rs=base.records(out)
 for r in rs:
  _,cid,arm=r['cell'].split('/');path=out/'attempts'/f'codex-{cid}-{arm}'
  if r['manifest_digest']!=base.digest(m) or r['finish_manifest_digest']!=base.digest(fm):raise ValueError('generation binding drift')
  if r['prompt_digest']!=base.digest((out/'prompts'/f'{cid}-{arm}.txt').read_bytes()) or r['stdout_digest']!=base.digest((path/'stdout.txt').read_bytes()):raise ValueError('generation raw drift')
  if r['status']=='completed':
   parsed=base.parse_codex((path/'stdout.txt').read_text())
   if parsed['status']!='completed' or parsed['text']!=r['text'] or r.get('exit_code')!=0:raise ValueError('generation result mismatch')
   result=passes(out,cid)[-1]
   if r['evaluation_digest']!=base.digest(result):raise ValueError('generation/evaluation drift')
 full=[]
 for cid in m['input_digests']:
  rows=passes(out,cid)
  if rows and answers_done(rows[-1]):
   evidence(out,cid,rows[-1]);full.append(cid)
 stats=base.summarize(rs,m['cells']);stats.update(answered_jev_cases=len(full),answered_jev_case_ids=full,semantic_scope_complete_cases=sum(passes(out,cid)[-1].get('scope_complete',False) for cid in full),
    budget=rec.Store(out,[origin]).summary(),finish_manifest_digest=base.digest(fm),recovery_manifest_digest=base.digest(m),
    quality_status='pending two independent human reviews; development-only synthetic corpus')
 old.save(out/'finish-report.json',stats)
 selected=[]
 parent=Path(fm['reused_baselines'])
 for directory,arms in ((parent,('bare','ordinary')),(origin,('vietnamizer_review',)),(out,('vietnamizer_jev',))):
  for r in base.records(directory):
   if r['cell'].startswith('codex/') and r['cell'].split('/')[2] in arms and r['status']=='completed':selected.append((str(directory),r))
 random.Random(1404).shuffle(selected)
 cases={c['id']:c for c in old.read(origin/'frozen-corpus.json')['cases']};packet=[];key={}
 for i,(epoch,r) in enumerate(selected,1):
  rid=f'F{i:03d}';cid=r['cell'].split('/')[1];c=cases[cid]
  packet.append({'review_id':rid,**{k:c[k] for k in ('source','audience','purpose')},'output':r['text'],
     'review':{'meaning_violation':None,'voice_violation':None,'unnecessary_edit':None,'required_fixes_resolved':None,'notes':''}})
  key[rid]={'epoch':epoch,'cell':r['cell']}
 old.save(out/'finish-blinded-review.json',packet);old.save(out/'finish-review-key.json',key)
 print(json.dumps({'completed_codex_finals':stats['completed'],'answered_jev_cases':len(full),'review_packet':len(packet),'budget':stats['budget']}),flush=True)
 return stats


def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('command',choices=('prepare','run','report'));ap.add_argument('--output',required=True,type=Path);ap.add_argument('--limit',type=int,default=1)
 a=ap.parse_args();out=a.output.resolve()
 if not 1<=a.limit<=4:raise ValueError('limit1..4')
 with old.writer(out):
  if a.command=='prepare':freeze(out);print('Frozen finish manifest');return
  if a.command=='report':report(out);return
  m,_,_=verify(out);done={r['cell'].split('/')[1] for r in base.records(out) if r['status']=='completed'}
  pending=[cid for cid in m['input_digests'] if cid not in done]
  try:
   for cid in pending[:a.limit]:complete(out,cid)
  finally:report(out)
if __name__=='__main__':main()
