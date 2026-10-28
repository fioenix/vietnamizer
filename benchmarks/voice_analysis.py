"""Offline, evidence-bound exploratory tables/figures for voice_pilot; no provider calls."""
import argparse
import csv
import difflib
import html
import json
from pathlib import Path
import statistics
from benchmarks import voice_pilot as v
from benchmarks import voice_continue as continuation

def normalized_preferences(assessment,mapping):
    rows=[]
    for r in assessment['preferences']:
        p=mapping['pairs'][r['id']];target=p['contrast'].split('-')[0]
        winner=p.get(r['preference']+'_arm') if r['preference'] in ('left','right') else None
        outcome=('win' if winner==target else 'loss') if winner else r['preference']
        rows.append({'contrast':p['contrast'],'outcome':outcome,'reason':r['reason']})
    return rows

def write_csv(path,rows):
    if not rows:return
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def verify_archive(out):
    m=v.read(out/'manifest.json')
    if m['cap']!=56 or m['plan_ids']!=v.plan_ids():raise ValueError('archive plan/cap drift')
    seal=v.read(out/'final-seal.json')['sha256']
    actual={str(f.relative_to(out)) for f in out.rglob('*') if f.is_file() and f.name!='final-seal.json'}
    if actual!=set(seal):raise ValueError('archive file inventory drift')
    for name,h in seal.items():
        if v.sha((out/name).read_bytes())!=h:raise ValueError('archive payload drift: '+name)
    for name,h in m['fingerprints'].items():
        if v.sha((out/name).read_bytes())!=h:raise ValueError('frozen archive input drift')
    for name,h in m['code'].items():
        if v.sha((out/'runner-source'/Path(name).name).read_bytes())!=h:raise ValueError('captured inference code drift')
    return m

def analyze(out,portable=False):
    m=verify_archive(out) if portable else v.verify(out);records=continuation.audit_history(out,m);byid={r['id']:r for r in records if r['status']=='completed'}
    rows=[];contrasts=[];panels=[]
    for cid in v.CASES:
        source=(out/'corpus'/f'{cid}.txt').read_text();texts={a:byid[f'edit-{cid}-{a}']['text'] for a in v.ARMS}
        for a in v.ARMS:
            (out/'outputs').mkdir(exist_ok=True);(out/'outputs'/f'{cid}-{a}.txt').write_text(texts[a])
            (out/'outputs'/f'{cid}-{a}.diff').write_text(''.join(difflib.unified_diff(source.splitlines(True),texts[a].splitlines(True),fromfile='original',tofile=f'{cid}-{a}')))
            panels.append('<h2>'+cid+' · '+a+'</h2>'+difflib.HtmlDiff(wrapcolumn=80).make_table(source.splitlines(),texts[a].splitlines(),context=True,numlines=2,fromdesc='Bản gốc',todesc=html.escape(a)))
        for judge in ('codex','gemini'):
            ident=f'judge-{cid}-{judge}';r=byid.get(ident)
            if not r:continue
            blind=v.read(out/'blind'/f'{cid}-{judge}.json');packet=blind['packet'];mapping=blind['mapping'];v.validate_assessment(packet,r['assessment'])
            inverse={alias:a for a,alias in mapping['aliases'].items()};inverse['original']='original';scores={}
            for a in r['assessment']['assessments']:
                arm=inverse[a['id']];text=source if arm=='original' else texts[arm];scores[arm]=a
                rows.append({'case':cid,'stratum':'native' if cid.startswith('V') else 'neutral','judge':judge,'arm':arm,'voice':a['voice'],'readability':a['readability'],'meaning':a['meaning'],'evidence':a['evidence'],'reference_evidence':a['reference_evidence'],'reason':a['reason'],'output_sha256':v.sha(text.encode()),'judge_input_sha256':v.sha((out/'attempts'/ident/'stdin.txt').read_bytes())})
            prefs={r['contrast']:r for r in normalized_preferences(r['assessment'],mapping)}
            for target,control in (('B','A'),('C','A'),('D','C'),('D','B')):
                label=target+'-'+control;p=prefs[label]
                contrasts.append({'case':cid,'stratum':'native' if cid.startswith('V') else 'neutral','judge':judge,'contrast':label,'voice_delta':scores[target]['voice']-scores[control]['voice'],'readability_delta':scores[target]['readability']-scores[control]['readability'],'preference':p['outcome'],'target_meaning':scores[target]['meaning'],'control_meaning':scores[control]['meaning'],'reason':p['reason']})
    summary=[]
    for judge in ('codex','gemini'):
        for stratum in ('native','neutral','all'):
            for contrast in ('B-A','C-A','D-C','D-B'):
                x=[r for r in contrasts if r['judge']==judge and r['contrast']==contrast and (stratum=='all' or r['stratum']==stratum)]
                expected=8 if stratum=='all' else 4
                summary.append({'judge':judge,'stratum':stratum,'contrast':contrast,'expected':expected,'rated':len(x),'missing':expected-len(x),**{k:sum(r['preference']==k for r in x) for k in ('win','tie','loss','uncertain')},'median_voice_delta':statistics.median(r['voice_delta'] for r in x) if x else None,'mean_voice_delta':statistics.mean(r['voice_delta'] for r in x) if x else None,'target_major':sum(r['target_meaning']=='major' for r in x),'control_major':sum(r['control_meaning']=='major' for r in x),'target_uncertain':sum(r['target_meaning']=='uncertain' for r in x)})
    interactions=[]
    for cid in v.CASES:
        for judge in ('codex','gemini'):
            x={r['contrast']:r for r in contrasts if r['case']==cid and r['judge']==judge}
            if len(x)==4:interactions.append({'case':cid,'judge':judge,'ordinal_voice_interaction':x['D-C']['voice_delta']-x['B-A']['voice_delta']})
    data={'schema':'voice-analysis-v1','request_cap':56,'reserved_starts':len(records),'editing_outputs':sum(r['id'].startswith('edit-') for r in records),'main_judgments':sum(r['id'].startswith('judge-') and r['status']=='completed' for r in records),'rejected_judgments':[{'id':r['id'],'error':r.get('error')} for r in records if r['status']=='failed'],'unique_sessions':len({r['session'] for r in records}),'operational_tool_calls':0,'summary':summary,'interactions':interactions,'limits':['model-assessed/exploratory, single historical reference author','ordinal score arithmetic is descriptive','8drafts,4native source articles from3topic families,1generation/cell','two judges not independent human ground truth','same-provider bias possible; no population/power claim','public/pretraining exposure unknown','some native intros109/123words, disclosed before run','provider HTTP retries/billing not observable']}
    v.save(out/'analysis.json',data);write_csv(out/'ratings.csv',rows);write_csv(out/'contrasts.csv',contrasts);write_csv(out/'summary.csv',summary)
    (out/'before-after.html').write_text('<!doctype html><meta charset="utf-8"><title>Voice pilot: trước và sau</title><style>body{font:16px system-ui;margin:24px}table{font:13px monospace;width:100%;border-collapse:collapse}td{white-space:pre-wrap;padding:3px}.diff_add{background:#def0e2}.diff_sub{background:#f5dedd}.diff_chg{background:#f8efcf}</style><h1>32 bản biên tập trên cùng Codex</h1><p>A: prompt; B: prompt + mẫu; C: Vietnamizer; D: Vietnamizer + cùng mẫu. Phiếu chấm lỗi được giữ là thiếu; không sửa hoặc hỏi lại.</p>'+''.join(panels))
    return data,rows,contrasts

def figures(out,rows,contrasts,data):
    from reportlab.graphics.shapes import Drawing,Rect,String,Line,Circle,Polygon
    from reportlab.graphics import renderSVG,renderPDF
    from reportlab.lib.colors import HexColor,white
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    import reportlab
    font=next((p for p in (Path('/System/Library/Fonts/Supplemental/Arial Unicode.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')) if p.exists()),Path(reportlab.__file__).parent/'fonts/Vera.ttf')
    pdfmetrics.registerFont(TTFont('VoiceFont',str(font)))
    dest=out/'figures';dest.mkdir(exist_ok=True);files=[]
    def text(d,x,y,s,size=11):d.add(String(x,y,str(s),fontName='VoiceFont',fontSize=size,fillColor=HexColor('#202B33')))
    def frame(title):
        d=Drawing(1000,610);d.add(Rect(0,0,1000,610,fillColor=white,strokeColor=None));text(d,35,575,title,17)
        text(d,35,550,'MODEL-ASSESSED · 1 tác giả tham chiếu · 8 bản nháp · 1 lượt sinh/ô · 2 model chấm ẩn nhãn',11)
        text(d,35,25,'Thăm dò, không có nhãn tác giả/người chấm độc lập; không phải so sánh agent biên tập.',10);return d
    def store(d,n):
        for ext,renderer in [('svg',renderSVG),('pdf',renderPDF)]:
            f=dest/(n+'.'+ext);renderer.drawToFile(d,str(f))
            if ext=='svg':f.write_text(f.read_text().replace('font-family: VoiceFont','font-family: Arial Unicode MS, DejaVu Sans, sans-serif'))
            files.append({'path':str(f.relative_to(out)),'sha256':v.sha(f.read_bytes())})
    colors={'codex':HexColor('#225A81'),'gemini':HexColor('#A46A23')}
    d=frame('Chênh lệch giọng khi thêm Vietnamizer với cùng mẫu — D trừ B')
    scale=lambda value:220+(value+4)*80
    for n in range(-4,5):
        x=scale(n);d.add(Line(x,110,x,495,strokeWidth=1 if n==0 else .4,strokeColor=HexColor('#829099' if n==0 else '#DDE2E5')));text(d,x-4,87,n)
    for i,cid in enumerate(v.CASES):
        y=470-i*44;text(d,40,y-3,cid+(' · có giọng sẵn' if cid.startswith('V') else ' · nháp AI'))
        for j,judge in enumerate(('codex','gemini')):
            r=next((r for r in contrasts if r['case']==cid and r['judge']==judge and r['contrast']=='D-B'),None)
            if r is None:
                text(d,880,y-5,'Thiếu '+judge,8);continue
            x=scale(r['voice_delta']);yy=y+(5 if j==0 else -5);c=colors[judge]
            d.add(Circle(x,yy,4,fillColor=c,strokeColor=c) if j==0 else Polygon([x,yy+5,x-4,yy-4,x+4,yy-4],fillColor=c,strokeColor=c));text(d,x+8,yy-3,f'{r["voice_delta"]:+d}',9)
    text(d,220,60,'Chênh lệch điểm giọng (thang thứ bậc 1–5; không có CI hoặc kiểm định)',11)
    text(d,655,518,'● Giám khảo Codex   ▲ Giám khảo Gemini',10);store(d,'voice-primary-delta')
    palette={'win':'#5486A2','tie':'#CFD4D7','loss':'#B87963','uncertain':'#E7D9AA'}
    d=frame('Bốn phép so sánh — lựa chọn về giọng, giữ nguyên hòa/chưa rõ')
    for i,contrast in enumerate(('B-A','C-A','D-C','D-B')):
        for j,judge in enumerate(('codex','gemini')):
            y=470-(i*2+j)*44;group=next(r for r in data['summary'] if r['judge']==judge and r['stratum']=='all' and r['contrast']==contrast);text(d,40,y+3,f'{contrast} · {judge}')
            x=225
            for kind in ('win','tie','loss','uncertain'):
                n=group[kind]
                if n:
                    d.add(Rect(x,y,n*65,24,fillColor=HexColor(palette[kind]),strokeColor=None));text(d,x+n*65/2-3,y+7,n,10);x+=n*65
            text(d,775,y+7,f'n = {group["rated"]}/8 bản nháp',10)
    for i,(k,label) in enumerate([('win','Thắng'),('tie','Hòa'),('loss','Thua'),('uncertain','Chưa rõ')]):
        d.add(Rect(225+i*155,80,14,14,fillColor=HexColor(palette[k]),strokeColor=None));text(d,245+i*155,82,label,10)
    text(d,225,52,'Thắng/thua là vế trước so với vế sau; giọng và lỗi nghĩa được báo riêng.',10);store(d,'voice-contrasts')
    d=frame('Giữ nghĩa — đánh giá từng bản biên tập, không bù bằng điểm giọng')
    status={'clear':('#E0E9E7','0'),'minor':('#E5CE9D','n'),'major':('#C9796F','L'),'uncertain':('#CDD3DF','?')}
    for j,judge in enumerate(('codex','gemini')):
        left=180+j*405;text(d,left,515,'Giám khảo '+judge,12)
        for a,arm in enumerate(v.ARMS):text(d,left+a*70+20,485,arm,12)
        for i,cid in enumerate(v.CASES):
            y=430-i*38
            if j==0:text(d,60,y+12,cid)
            for a,arm in enumerate(v.ARMS):
                r=next((r for r in rows if r['case']==cid and r['judge']==judge and r['arm']==arm),None)
                color,label=status[r['meaning']] if r else ('#F2F2F2','—')
                d.add(Rect(left+a*70,y,58,30,fillColor=HexColor(color),strokeColor=None));text(d,left+a*70+25,y+10,label,11)
    text(d,180,108,'N2: nguồn đếm bước mơ hồ; hai model bất đồng về mức lỗi nghĩa.',10)
    text(d,180,82,'0: không thấy lỗi   n: lỗi nhỏ   L: sai ý/dữ kiện   ?: chưa rõ · —: thiếu phiếu (theo model)',11)
    text(d,180,57,'A prompt · B prompt+mẫu · C Vietnamizer · D Vietnamizer+cùng mẫu',10);store(d,'voice-meaning')
    v.save(dest/'manifest.json',{'renderer':'ReportLab '+reportlab.Version,'font':str(font),'files':files});return files

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--figures',action='store_true');a=p.parse_args();out=a.output.resolve();data,rows,contrasts=analyze(out)
    if a.figures:figures(out,rows,contrasts,data)
    print(json.dumps({'starts':data['reserved_starts'],'editing_outputs':data['editing_outputs'],'main_judgments':data['main_judgments'],'ratings':len(rows),'contrasts':len(contrasts)},ensure_ascii=False))

if __name__=='__main__':main()
