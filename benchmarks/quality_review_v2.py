"""Explicit label-enum amendment; inherit the failed smoke without rerolling it."""
from pathlib import Path
import argparse,json,shutil
from benchmarks import quality_review as q
ORIGIN=q.ROOT/'artifacts/014-quality-assessment-20261025'
NOTE=q.ROOT/'specs/014-editorial-benchmark/quality-enum-amendment.md'
original_grade_prompt=q.grade_prompt

def grade_prompt(packet,inventory):
 return original_grade_prompt(packet,inventory)+'\nEXACT ALLOWED LABELS: meaning, voice, and protected MUST each be one of "clear", "violation", "uncertain". Use "violation" for established damage; "damaged" is not a valid serialized label. Edit values MUST be one of "justified_successful", "unnecessary", "harmful", "mixed", "uncertain". Issue values MUST be one of "resolved", "partial", "unresolved", "uncertain". Do not omit any output, edit ID, or issue ID. These spellings implement the existing rubric; do not change substantive judgments to fit an example.'

def prepare(out):
 q.verify(ORIGIN);q.prepare(out)
 inherited={}
 for p in sorted((ORIGIN/'model-attempts').rglob('*')):
  if p.is_file():inherited[str(p.relative_to(ORIGIN))]=q.digest(p.read_bytes())
 if len(list((ORIGIN/'model-attempts').glob('*/result.json')))!=2:raise ValueError('expected exactly two smoke starts')
 m={'origin':str(ORIGIN),'origin_manifest_digest':q.digest(q.read(ORIGIN/'manifest.json')),'driver':str(Path(__file__).resolve()),'driver_digest':q.digest(Path(__file__).read_bytes()),'note':str(NOTE),'note_digest':q.digest(NOTE.read_bytes()),'inherited':inherited,'failed_units':['M1-Q001'],'total_start_cap':42,'policy':'Failed smoke remains missing; do not retry it. All original bytes retained. New grades clarify serialized enum spellings only.'}
 q.base.freeze_manifest(out/'amendment.json',m)
 for relative,d in inherited.items():
  dest=out/relative;source=ORIGIN/relative
  if dest.exists() and q.digest(dest.read_bytes())!=d:raise ValueError('inheritance drift')
  dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
 shutil.copy2(__file__,out/'source/quality_review_v2.py');shutil.copy2(NOTE,out/'source/quality-enum-amendment.md')
 return m

def verify(out):
 q.verify(out);m=q.read(out/'amendment.json')
 if q.digest(Path(m['driver']).read_bytes())!=m['driver_digest'] or q.digest(Path(m['note']).read_bytes())!=m['note_digest']:raise ValueError('amendment drift')
 if q.digest(q.read(Path(m['origin'])/'manifest.json'))!=m['origin_manifest_digest']:raise ValueError('origin manifest drift')
 for relative,d in m['inherited'].items():
  if q.digest((out/relative).read_bytes())!=d or q.digest((Path(m['origin'])/relative).read_bytes())!=d:raise ValueError('inherited raw drift')
 return m

def run(out,judge,limit):
 m=verify(out);packet=q.read(out/'packets'/f'{judge}.json')
 attempted={q.read(p)['unit'] for p in (out/'model-attempts').glob(f'{judge}-*/result.json')}
 unexpected=[p for p in (out/'model-attempts').glob('*/result.json') if q.read(p)['status']!='completed' and p.parent.name not in m['failed_units']]
 if unexpected:raise ValueError('new failure; stop for diagnosis, no automatic retry')
 inv=q.call_model(out,judge,'sources',q.inventory_prompt(packet),lambda r:q.validate_inventory(packet,r));byid={r['id']:r for r in inv['sources']}
 for p in [p for p in packet if p['id'] not in attempted][:limit]:
  verify(out);q.call_model(out,judge,p['id'],grade_prompt(p,byid[p['id']]),lambda r:q.validate_grade(p,byid[p['id']],r))

def report(out):
 m=verify(out);q.grade_prompt=grade_prompt
 r=q.report(out);r['protocol_amendment']=m;r['failed_attempts']=[{'unit':p.parent.name,**q.read(p)} for p in (out/'model-attempts').glob('*/result.json') if q.read(p)['status']!='completed'];q.save(out/'model-report.json',r);return r

def main():
 p=argparse.ArgumentParser();p.add_argument('command',choices=('prepare','run','report'));p.add_argument('--output',type=Path,required=True);p.add_argument('--judge',choices=q.JUDGES);p.add_argument('--limit',type=int,default=1);a=p.parse_args();out=a.output.resolve()
 if not 1<=a.limit<=4:raise ValueError('batch limit1..4')
 if a.command=='prepare':prepare(out)
 elif a.command=='report':report(out)
 else:
  if not a.judge:raise ValueError('judge required')
  with __import__('benchmarks.jev_pilot',fromlist=['writer']).writer(out):run(out,a.judge,a.limit)
if __name__=='__main__':main()
