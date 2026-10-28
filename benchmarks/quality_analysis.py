"""Recompute exploratory model summaries and vector figures from validated raw-bound labels."""
from pathlib import Path
import argparse,collections,csv,math
from benchmarks import quality_review as q
LABELS={'bare':'Bare prompt','ordinary':'Ordinary prompt','vietnamizer_review':'Vietnamizer core','vietnamizer_jev':'Vietnamizer + Jev'}

def wilson(k,n):
 if not n:return {'n':0,'k':k,'estimate':None,'low':None,'high':None}
 z=1.959963984540054;p=k/n;den=1+z*z/n;center=(p+z*z/(2*n))/den;half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
 return {'n':n,'k':k,'estimate':p,'low':max(0,center-half),'high':min(1,center+half)}

def difference_clusters(rows,ids,a,b,metric):
 lookup={(r['case_id'],r['judge'],r['arm']):r for r in rows};result=[]
 for cid in ids:
  block=[]
  for judge in q.JUDGES:
   x=lookup.get((cid,judge,a),{}).get(metric);y=lookup.get((cid,judge,b),{}).get(metric)
   block.append(x-y if x is not None and y is not None else None)
  result.append(block)
 return result

def analyze(out):
 from benchmarks import quality_review_v2 as v
 r=v.report(out);manifest=q.verify(out);ids=manifest['source_ids'];rows=r['rows'];differences=[];rates=[];agreement=[]
 for c in r['comparisons']:
  for metric in ('precision','recall','meaning_violation','unnecessary_edit'):
   clusters=difference_clusters(rows,ids,c['a'],c['b'],metric);ci=q.paired_interval(clusters)
   differences.append({'a':c['a'],'b':c['b'],'metric':metric,**ci,'planned_sources':len(ids),'excluded_sources':len(ids)-ci['n_sources']})
 for judge in q.JUDGES:
  for arm in q.ARMS:
   selected=[x for x in rows if x['judge']==judge and x['arm']==arm]
   for metric in ('meaning_violation','voice_violation','protected_violation','unnecessary_edit'):
    values=[x[metric] for x in selected if x[metric] is not None]
    rates.append({'judge':judge,'arm':arm,'metric':metric,**wilson(sum(values),len(values)),'uncertain':sum(x[metric] is None for x in selected),'missing':len(ids)-len(selected),'interval':'Wilson95%; source-level within one judge; corpus conditional'})
 for dim,record in r['agreement'].items():
  for pair,n in record.get('matrix',{}).items():
   a,b=pair.split(' / ');agreement.append({'dimension':dim,'M1':a,'M2':b,'count':n,'units':'paired output labels; descriptive, not independent samples'})
 result={'label':'MODEL-ASSESSED / EXPLORATORY','report_digest':q.digest(r),'n_documents':len(ids),'completed_output_reviews':r['completed_output_reviews'],'missing_output_reviews':r['missing_output_reviews'],'human_reviews_completed':0,'protocol_amendment':r.get('protocol_amendment'),'failed_attempts':[{'judge':x.get('judge'),'unit':x.get('unit'),'status':x.get('status'),'reason':x.get('reason')} for x in r.get('failed_attempts',[])],'difference_units':'fractions in data; percentage points in paired-difference chart','differences':differences,'rates':rates,'comparisons':r['comparisons'],'agreement':r['agreement'],'limits':r['limitations']+['CI conditional on synthetic corpus and fixed judges','bootstrap incomplete source clusters excluded and counted','Wilson intervals per single judge, no pooled-rater binomial interval','no multiplicity-adjusted confirmatory hypothesis tests']}
 uses=[]
 for path in sorted((out/'model-attempts').glob('*/result.json')):
  attempt=q.read(path)
  try:_,usage=q.parse_model((path.parent/'stdout.jsonl').read_text());available=True
  except (ValueError,KeyError):usage={};available=False
  uses.append({'attempt':path.parent.name,'judge':attempt['judge'],'unit':attempt['unit'],'status':attempt['status'],'seconds':attempt['seconds'],'requested_model':attempt['requested_model'],'actual_model':None,'usage_available':available,**usage})
 result['execution']={'starts':len(uses),'usage_unknown_attempts':sum(not x['usage_available'] for x in uses),**{key:sum(x.get(key,0) for x in uses) for key in ('input_tokens','output_tokens','reasoning_output_tokens','seconds')},'new_paid_api_calls':0,'backend_model_attestation':None}
 q.save(out/'analysis/attempt-usage.json',uses)
 q.save(out/'analysis/summary.json',result)
 for name,data in [('paired-differences',differences),('rates',rates),('agreement-matrix',agreement),('preference-counts',[{'a':c['a'],'b':c['b'],'vote':k,'count':c['votes'].get(k,0)} for c in r['comparisons'] for k in ('win','tie','loss','uncertain','missing')])]:
  if data:
   with (out/'analysis'/f'{name}.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
 return result

def charts(out):
 # ReportLab vector output; optional plotting dependency, never used for labels/inference.
 from reportlab.graphics.shapes import Drawing,Rect,String,Line,Circle
 from reportlab.graphics import renderSVG,renderPDF
 from reportlab.lib.colors import Color,HexColor,white,black
 r=q.read(out/'analysis/summary.json');folder=out/'analysis/charts';folder.mkdir(exist_ok=True)
 colors={'win':HexColor('#156B58'),'tie':HexColor('#858AC2'),'loss':HexColor('#9750C4'),'uncertain':HexColor('#87D3E1'),'missing':Color(.75,.75,.75)}
 def text(d,x,y,t,size=11,color=black):d.add(String(x,y,t,fontName='Helvetica',fontSize=size,fillColor=color))
 def frame(title,subtitle,height=460):
  d=Drawing(960,height);d.add(Rect(0,0,960,height,fillColor=white,strokeColor=None));text(d,35,height-38,title,20);text(d,35,height-60,'MODEL-ASSESSED / EXPLORATORY',12,colors['loss']);text(d,35,height-81,subtitle,10);return d
 def save(d,name):renderSVG.drawToFile(d,str(folder/(name+'.svg')));renderPDF.drawToFile(d,str(folder/(name+'.pdf')))
 def footer(d):text(d,35,24,'20 synthetic documents; fixed Codex judges; human reviews pending. No general superiority claim.',9)
 d=frame('Blinded editing preferences','Each row has 40 planned dependent judge votes; ties, abstentions and missing labels remain visible.')
 for i,c in enumerate(r['comparisons']):
  y=300-i*85;text(d,35,y+30,LABELS[c['a']]+' vs '+LABELS[c['b']],12);x=35
  for label in colors:
   n=c['votes'].get(label,0);width=n/40*880
   if width:d.add(Rect(x,y,width,23,fillColor=colors[label],strokeColor=white));text(d,x+4,y+7,str(n),10,white if label in ('win','tie','loss') else black)
   x+=width
  text(d,35,y-17,' | '.join(label+': '+str(c['votes'].get(label,0)) for label in colors),10)
 x=35
 for label,color in colors.items():d.add(Rect(x,55,12,12,fillColor=color,strokeColor=None));text(d,x+18,57,label,10);x+=150
 footer(d);save(d,'preferences')
 d=frame('Paired preference with document-cluster uncertainty','Win=1, tie=0.5, loss=0; neutral=0.5. Both judges retained per document; incomplete clusters excluded.',380)
 left,right=380,760;scale=lambda x:left+x*(right-left)
 for value in (0,.25,.5,.75,1):d.add(Line(scale(value),85,scale(value),250,strokeColor=Color(.7,.7,.7) if value==.5 else Color(.9,.9,.9)));text(d,scale(value)-10,65,str(value),10)
 for i,c in enumerate(r['comparisons']):
  y=235-i*65;ci=c['paired_preference'];text(d,35,y,LABELS[c['a']]+' vs '+LABELS[c['b']],10)
  if ci['estimate'] is not None:d.add(Line(scale(ci['low']),y+3,scale(ci['high']),y+3,strokeColor=colors['win'],strokeWidth=2));d.add(Circle(scale(ci['estimate']),y+3,3,fillColor=colors['win'],strokeColor=None))
  text(d,785,y,'n='+str(ci['n_sources'])+'/20',10)
 footer(d);save(d,'preference-intervals')
 d=frame('Paired changes relative to comparator','95% document-cluster percentile bootstrap; both judges kept together; undefined/excluded sources counted.',600)
 selected=[x for x in r['differences'] if x['metric'] in ('precision','recall','meaning_violation','unnecessary_edit')]
 left,right=420,810;scale=lambda x:left+(x+1)/2*(right-left)
 for value in (-1,-.5,0,.5,1):d.add(Line(scale(value),75,scale(value),480,strokeColor=Color(.85,.85,.85)));text(d,scale(value)-12,60,str(int(value*100)),9)
 text(d,420,37,'Difference (percentage points; a - b); positive = more of the named metric',9)
 for i,item in enumerate(selected):
  y=472-i*32;text(d,35,y,item['metric']+' | '+LABELS[item['b']],9);text(d,825,y,'n='+str(item['n_sources'])+'/20',9)
  if item['estimate'] is None:text(d,460,y,'N/A',9);continue
  d.add(Line(scale(item['low']),y+3,scale(item['high']),y+3,strokeColor=colors['win'],strokeWidth=2));d.add(Circle(scale(item['estimate']),y+3,3,fillColor=colors['win'],strokeColor=None))
 text(d,35,505,'Top 4 rows: Jev - core; next 4: core - ordinary; final 4: core - bare.',10);footer(d);save(d,'paired-differences')
 d=frame('Observed meaning violations by judge','Points show k/n documents; 95%Wilson interval is per judge. Uncertain/missing are separate.',500)
 x0,x1=310,750;scale=lambda x:x0+x*(x1-x0)
 for v in (0,.25,.5,.75,1):d.add(Line(scale(v),75,scale(v),375,strokeColor=Color(.85,.85,.85)));text(d,scale(v)-8,56,str(int(v*100))+'%',9)
 rate_rows=[x for x in r['rates'] if x['metric']=='meaning_violation']
 for i,item in enumerate(rate_rows):
  y=360-i*36;text(d,35,y,item['judge']+' | '+LABELS[item['arm']],11)
  if item['estimate'] is not None:d.add(Line(scale(item['low']),y+3,scale(item['high']),y+3,strokeColor=colors['loss'],strokeWidth=2));d.add(Circle(scale(item['estimate']),y+3,3,fillColor=colors['loss'],strokeColor=None))
  text(d,770,y,f"{item['k']}/{item['n']}  ?{item['uncertain']}  missing{item['missing']}",10)
 footer(d);save(d,'meaning-safety')
 d=frame('Agreement before adjudication','Meaning labels on matching output cells; descriptive counts, no independence assumption.',480)
 matrix=r['agreement']['meaning'].get('matrix',{});labels=['clear','violation','uncertain'];max_n=max(matrix.values(),default=1)
 for i,a in enumerate(labels):
  text(d,100,315-i*70,'M1 '+a,11)
  for j,b in enumerate(labels):
   n=matrix.get(a+' / '+b,0);x=290+j*160;y=290-i*70;shade=.97-.55*n/max_n;d.add(Rect(x,y,140,55,fillColor=Color(shade,shade,shade),strokeColor=white));text(d,x+60,y+22,str(n),14,white if shade<.55 else black)
 for j,b in enumerate(labels):text(d,290+j*160,365,'M2 '+b,11)
 rec=r['agreement']['meaning'];text(d,100,90,'Matched cells: '+str(rec['n'])+' | agreement: '+str(rec['agreement'])+' | Cohen kappa: '+str(rec['kappa']),10);footer(d);save(d,'agreement')
 return folder

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--charts-only',action='store_true');a=p.parse_args();out=a.output.resolve()
 if a.charts_only:print(charts(out))
 else:print(q.digest(analyze(out)))
if __name__=='__main__':main()
