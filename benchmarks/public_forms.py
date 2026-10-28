"""New independent human Forms for the provenance-pinned public AI cohort."""
from pathlib import Path
import argparse,base64,json,random
from benchmarks import public_ai as pub,simple_forms as simple
base=pub.base;old=pub.old
RUNTIME=Path(__file__).with_suffix('.gs')

def build_contract(cases,outputs,who,seed):
 rng=random.Random(seed);order=list(cases);rng.shuffle(order);packet=[];key={}
 for n,c in enumerate(order,1):
  arms=list(pub.ARMS);rng.shuffle(arms);qid=f'Q{n:03}';packet.append({'id':qid,**{k:c[k] for k in ('source','audience','purpose')},'outputs':{l:{'text':outputs[f'codex/{c["id"]}/{a}']} for l,a in zip('ABCD',arms)}});key[qid]={l:{'arm':a,'source_case_id':c['id']} for l,a in zip('ABCD',arms)}
 return simple.contract({'cases':packet,'reviewer':who}),key

def expected(origin):
 if pub.report(origin)['completed']!=80:raise ValueError('benchmark incomplete')
 cases=old.read(origin/'frozen-corpus.json')['cases'];outputs={r['cell']:r['text'] for r in base.records(origin)}
 return {w:build_contract(cases,outputs,w,s) for w,s in [('A',25031),('B',25032)]}

def prepare(origin,out):
 cs=expected(origin)
 if (out/'manifest.json').exists():return verify(out)
 out.mkdir(parents=True,exist_ok=True);images={}
 for who,(c,key) in cs.items():
  old.save(out/f'{who}-contract.json',c);old.save(out/'private'/f'{who}-key.json',key);images[who]={}
  for g in c['groups']:
   images[who][g['id']]={}
   for l,t in g['outputs'].items():
    path=out/'images'/who/f'{g["id"]}-{l}.png';meta=simple.render_pair(g['source'],t,path)
    if not meta['rendered_text_lossless']:raise ValueError('render omission')
    images[who][g['id']][l]={'path':str(path.resolve()),**meta}
 old.save(out/'images.json',images)
 m={'schema':'public-ai-human-v1','origin':str(origin.resolve()),'parent_digest':base.digest(pub.verify(origin)),'contract_digests':{w:base.digest(c) for w,(c,k) in cs.items()},'images_digest':base.digest(images),'driver_digest':base.digest(Path(__file__).read_bytes()),'runtime_digest':base.digest(RUNTIME.read_bytes()),'item_count_per_form':162,'planned_output_reviews':160,'human_submissions':0}
 base.freeze_manifest(out/'manifest.json',m);return m

def verify(out):
 m=old.read(out/'manifest.json');origin=Path(m['origin']);cs=expected(origin)
 if m['parent_digest']!=base.digest(pub.verify(origin)) or m['driver_digest']!=base.digest(Path(__file__).read_bytes()) or m['runtime_digest']!=base.digest(RUNTIME.read_bytes()):raise ValueError('Forms code/origin drift')
 for w,(c,k) in cs.items():
  if old.read(out/f'{w}-contract.json')!=c or old.read(out/'private'/f'{w}-key.json')!=k or base.digest(c)!=m['contract_digests'][w]:raise ValueError('assignment drift')
 images=old.read(out/'images.json')
 if base.digest(images)!=m['images_digest']:raise ValueError('image inventory drift')
 for w,(c,k) in cs.items():
  for g in c['groups']:
   for l,t in g['outputs'].items():
    meta=images[w][g['id']][l]
    if meta['source_digest']!=base.digest(g['source'].encode()) or meta['edited_digest']!=base.digest(t.encode()) or meta['sha256']!=base.digest(Path(meta['path']).read_bytes()):raise ValueError('image text binding drift')
 return m

def batch(out,mode,who=None,start=0,count=2):
 m=verify(out);payload={'schema':m['schema'],'cohort':base.digest(m),'mode':mode,'contract_digests':m['contract_digests'],'questions':simple.QUESTIONS}
 if who:payload['who']=who
 if mode=='append':
  c=old.read(out/f'{who}-contract.json');im=old.read(out/'images.json');payload.update(start=start,groups=[])
  for g in c['groups'][start:start+count]:
   row={**g,'images':{}}
   for l,meta in im[who][g['id']].items():row['images'][l]={'base64':base64.b64encode(Path(meta['path']).read_bytes()).decode(),'sha256':meta['sha256']}
   payload['groups'].append(row)
 path=out/'batches'/f'{mode}-{who or "both"}-{start:02}.gs';path.parent.mkdir(exist_ok=True)
 path.write_text(RUNTIME.read_text().replace('/*__BATCH_DATA__*/',json.dumps(payload,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e')))
 old.save(path.with_suffix('.json'),{'payload_digest':base.digest(payload),'script_digest':base.digest(path.read_bytes())});return path

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=('prepare','batch','verify'));p.add_argument('--origin',type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--mode',choices=('initialize','append','finish','audit'));p.add_argument('--who',choices=('A','B'));p.add_argument('--start',type=int,default=0);p.add_argument('--count',type=int,default=2);a=p.parse_args();print(prepare(a.origin,a.output) if a.command=='prepare' else verify(a.output) if a.command=='verify' else batch(a.output,a.mode,a.who,a.start,a.count))
