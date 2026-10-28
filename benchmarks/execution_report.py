"""Offline descriptive report of frozen outputs. No inference, grading or Forms calls."""
from pathlib import Path
import argparse
import csv
import difflib
import hashlib
import json
import math
import statistics
from collections import defaultdict
from benchmarks import editorial_pilot as pilot
from benchmarks import gemini_manual as gemini

ROOT=Path(__file__).resolve().parents[1]
CODEX=ROOT/'artifacts/014-public-ai-benchmark-20261025-v2'
GEMINI=ROOT/'artifacts/014-gemini-text-only-20261026/epoch-v3'
ARMS=('bare','ordinary','vietnamizer','vietnamizer_jev')
LABELS=('Yêu cầu cơ bản','Prompt thường','Vietnamizer','Vietnamizer + Jev')
COLORS=('#777D88','#697A9E','#187B72','#9A659D')
INPUTS={}

def raw(p):
    p=Path(p); data=p.read_bytes();INPUTS[str(p.relative_to(ROOT))]=hashlib.sha256(data).hexdigest();return data

def read(p):return json.loads(raw(p))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')

def change_label(value):
    return '<0,1%' if 0<value<.001 else f'{value*100:.1f}%'

def metrics(source,output):
    if not source.strip() or not output.strip():raise ValueError('Empty document')
    a=' '.join(source.split());b=' '.join(output.split())
    return {'source_chars':len(source),'output_chars':len(output),
            'unchanged_raw':source==output,'unchanged_whitespace_collapsed':a==b,
            'length_change_pct':100*(len(output)/len(source)-1),
            'character_change':1-difflib.SequenceMatcher(None,source,output,autojunk=False).ratio(),
            'character_change_whitespace_collapsed':1-difflib.SequenceMatcher(None,a,b,autojunk=False).ratio()}

def quantile(values,q):
    v=sorted(values);i=(len(v)-1)*q;lo=math.floor(i);hi=math.ceil(i)
    return v[lo]+(v[hi]-v[lo])*(i-lo)

def summarize(rows):
    grouped=defaultdict(list)
    for r in rows:grouped[(r['runtime'],r['arm'])].append(r)
    summary=[]
    for (runtime,arm),items in grouped.items():
        if len(items)!=20 or len({r['source_id'] for r in items})!=20:raise ValueError('Need20distinct sources per arm')
        s={'runtime':runtime,'arm':arm,'n_sources':20,
           'unchanged_raw':sum(r['unchanged_raw'] for r in items),
           'unchanged_whitespace_collapsed':sum(r['unchanged_whitespace_collapsed'] for r in items)}
        for metric in ('length_change_pct','character_change','character_change_whitespace_collapsed','seconds','input_tokens','output_tokens','reasoning_tokens'):
            v=[r[metric] for r in items]
            s[metric]={'median':statistics.median(v),'q1':quantile(v,.25),'q3':quantile(v,.75),'min':min(v),'max':max(v),'sum':sum(v)}
        summary.append(s)
    return summary

def verify_corpus(corpus,manifest,replica):
    if pilot.digest(corpus)!=manifest['corpus_digest'] or corpus!=replica:
        raise ValueError('Canonical original-source drift')

def collect():
    corpus=read(CODEX/'frozen-corpus.json')
    manifest=read(CODEX/'manifest.json')
    verify_corpus(corpus,manifest,read(GEMINI/'inputs/frozen-corpus.json'))
    if manifest!=read(GEMINI/'inputs/manifest.json'):raise ValueError('Manifest lineage drift')
    sources={c['id']:c['source'] for c in corpus['cases']}
    if set(sources)!={f'R{i:03}' for i in range(1,21)}:raise ValueError('Source set')
    rows=[];sessions=set();gmanifest=read(GEMINI/'manifest.json')
    for name,digest in gmanifest['input_fingerprints'].items():
        if hashlib.sha256(raw(GEMINI/name)).hexdigest()!=digest:raise ValueError('Frozen input drift: '+name)
    for runtime in ('codex','gemini'):
        for cid,source in sources.items():
            for arm in ARMS:
                cell=f'{cid}-{arm}';prompt=raw(CODEX/'prompts'/f'{cell}.txt')
                if runtime=='codex':
                    d=CODEX/'attempts'/('codex-'+cell);r=read(d/'result.json');stdout=raw(d/'stdout.txt');raw(d/'stderr.txt')
                    parsed=pilot.parse_codex(stdout.decode())
                    if (r['cell']!=f'codex/{cid}/{arm}' or r['status']!='completed' or r['exit_code']!=0 or r['stdout_digest']!=hashlib.sha256(stdout).hexdigest() or
                        parsed['status']!='completed' or parsed['text']!=r['text'] or r['tool_calls'] or parsed['tool_calls'] or
                        r['prompt_digest']!=hashlib.sha256(prompt).hexdigest() or r['usage']!=parsed['usage'] or r['session']!=parsed['session'] or not r['session'] or r['requested_model']!='gpt-6.1-sol'):
                        raise ValueError('Codex raw/prompt/usage mismatch: '+cell)
                    seconds=r['seconds'];session=r['session'];u=r['usage'];reasoning=u.get('reasoning_output_tokens',0)
                else:
                    d=GEMINI/'attempts'/cell;r=read(d/'result.json')
                    for name,digest in read(d/'seal.json').items():
                        if hashlib.sha256(raw(d/name)).hexdigest()!=digest:raise ValueError('Gemini seal drift: '+cell)
                    native=read(d/'native/finish.json');init=read(d/'native/init.json')['init'];w=read(d/'wrapper.stdout.bin')
                    parsed=gemini.parse_events([json.loads(l) for l in raw(d/'native/stdout.bin').decode().splitlines() if l.strip()])
                    for name,info in native['streams'].items():
                        if hashlib.sha256(raw(d/'native'/name)).hexdigest()!=info['sha256']:raise ValueError('Native digest')
                    if (r['status']!='completed' or parsed['status']!='completed' or parsed['tools'] or parsed['errors'] or
                        r['text']!=parsed['text'] or r['text']!=w['structured_output']['text'] or r['usage']!=parsed['usage'] or
                        r['conversation_id']!=parsed['conversation_id'] or not r['conversation_id'] or r['models_observed']!=[gemini.MODEL] or init['model']!=gemini.MODEL or init['agent']!=gmanifest['agent'] or
                        w['status']!='success' or w.get('subagents') or w.get('permission_requests') or w['evidence']['session_resumed'] or
                        any(x['name']!='finish' for x in w['tool_calls']) or native['exitCode']!=0 or native['timedOut'] or
                        native.get('signal') or native.get('spawnError') or not native['guard_ok']):raise ValueError('Gemini raw mismatch: '+cell)
                    if raw(d/'prompt.txt')!=prompt:raise ValueError('Unequal frozen prompts')
                    seconds=r['elapsed_seconds'];session=r['conversation_id'];u=r['usage'];reasoning=u.get('thinking_tokens',0)
                if (runtime,session) in sessions:raise ValueError('Reused conversation')
                sessions.add((runtime,session))
                rows.append({'runtime':runtime,'source_id':cid,'arm':arm,**metrics(source,r['text']),
                             'seconds':seconds,'input_tokens':u['input_tokens'],'output_tokens':u['output_tokens'],
                             'reasoning_tokens':reasoning,'source_sha256':hashlib.sha256(source.encode()).hexdigest(),
                             'output_sha256':hashlib.sha256(r['text'].encode()).hexdigest()})
    return rows

def table(path,rows):
    with Path(path).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def figures(out,rows,summary,coverage,cost):
    from reportlab.graphics.shapes import Drawing,Rect,String,Line,Circle
    from reportlab.graphics import renderPDF,renderSVG
    from reportlab.lib.colors import HexColor,white,black
    out.mkdir();records=[]
    def text(d,x,y,s,size=10):d.add(String(x,y,str(s),fontName='DejaVuSans',fontSize=size))
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    import reportlab
    font=Path(reportlab.__file__).parent/'fonts/Vera.ttf'
    # Vera lacks Vietnamese; use the installed Unicode font, without downloading fonts.
    candidates=[ROOT/'assets/DejaVuSans.ttf',Path('/System/Library/Fonts/Supplemental/Arial Unicode.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')]
    font=next((p for p in candidates if p.exists()),font)
    pdfmetrics.registerFont(TTFont('DejaVuSans',str(font)))
    def frame(title,sub,height=640):
        d=Drawing(1120,height);d.add(Rect(0,0,1120,height,fillColor=white,strokeColor=None))
        text(d,35,height-35,title,18);text(d,35,height-58,sub,10)
        text(d,35,25,'Mô tả thực thi · 20 nguồn công khai · 1 lượt tạo bản cuối/nguồn/chế độ · Chưa đo chất lượng biên tập.',9)
        return d
    def store(d,name):
        for ext,renderer in [('svg',renderSVG),('pdf',renderPDF)]:
            p=out/(name+'.'+ext);renderer.drawToFile(d,str(p));records.append({'file':p.name,'sha256':sha(p)})
    def axis(d,x,y,width,low,high,label):
        scale=lambda v:x+(v-low)/(high-low)*width
        for n in range(5):
            v=low+(high-low)*n/4;xx=scale(v);d.add(Line(xx,y,xx,y+265,strokeColor=HexColor('#E1E5EA')));text(d,xx-12,y-20,f'{v:.1f}',8)
        text(d,x,y-48,label,10);return scale
    for runtime,name in [('codex','Codex · gpt-6.1-sol / medium (yêu cầu)'),('gemini','Gemini · gemini-3.8-flash-medium (CLI ghi nhận)')]:
        data=[r for r in rows if r['runtime']==runtime]
        d=frame(name+' — mức thay đổi so với bản gốc','Mỗi ô = một nguồn × một chế độ. Thứ tự R001–R020 giữ nguyên; không sắp theo kết quả.',790)
        for j,label in enumerate(LABELS):text(d,265+j*195,690,label,11)
        by={(r['source_id'],r['arm']):r for r in data}
        for i in range(20):
            cid=f'R{i+1:03}';y=650-i*27;text(d,120,y+5,cid,10)
            for j,arm in enumerate(ARMS):
                value=by[(cid,arm)]['character_change'];shade=int(245-value*180)
                d.add(Rect(255+j*195,y,178,23,fillColor=HexColor(f'#{shade:02x}{min(255,shade+8):02x}ff'),strokeColor=white))
                text(d,270+j*195,y+6,change_label(value),9)
        text(d,35,78,'1 − SequenceMatcher ratio trên ký tự Unicode, autojunk=False; 0% = giữ nguyên, 100% = không có khối khớp.',10)
        text(d,35,58,'Có tính khoảng trắng/Markdown; <0,1% vẫn là đã thay đổi. Màu đậm không có nghĩa tốt hơn hoặc sai hơn.',10)
        store(d,runtime+'-source-changes')
        d=frame(name+' — trước/sau: độ dài và mức thay đổi','Mỗi chấm = một văn bản; vạch đen = trung vị; đoạn đen = Q1–Q3 (n=20/chế độ).')
        for panel,(metric,label) in enumerate([('length_change_pct','Thay đổi độ dài ký tự (%)'),('character_change_whitespace_collapsed','Mức thay đổi ký tự sau gộp khoảng trắng (%)')]):
            x=240+panel*450;width=360
            vals=[r[metric]*(100 if metric.startswith('character') else 1) for r in data]
            low=min(0,math.floor(min(vals)/10)*10);high=max(10,math.ceil(max(vals)/10)*10)
            scale=axis(d,x,180,width,low,high,label)
            for j,arm in enumerate(ARMS):
                y=420-j*62
                if panel==0:text(d,30,y,LABELS[j],10)
                points=[r for r in data if r['arm']==arm]
                for k,r in enumerate(points):
                    v=r[metric]*(100 if metric.startswith('character') else 1)
                    d.add(Circle(scale(v),y+(k%5-2)*4,2.8,fillColor=HexColor(COLORS[j]),strokeColor=None))
                values=[r[metric]*(100 if metric.startswith('character') else 1) for r in points]
                d.add(Line(scale(quantile(values,.25)),y-16,scale(quantile(values,.75)),y-16,strokeColor=black,strokeWidth=2))
                d.add(Line(scale(statistics.median(values)),y-21,scale(statistics.median(values)),y-11,strokeColor=black,strokeWidth=2))
        text(d,35,80,'Không chuẩn hóa Unicode hoặc bỏ Markdown. Bảng CSV giữ cả chỉ số ký tự nguyên trạng và gộp khoảng trắng.',10)
        store(d,runtime+'-text-distributions')
        d=frame(name+' — tài nguyên của lượt tạo bản cuối','20 chấm/chế độ; đen = trung vị và Q1–Q3. Thời gian CLI không gồm thời gian tư vấn Jev.',700)
        for panel,(metric,label) in enumerate([('seconds','Thời gian CLI (giây)'),('input_tokens','Input token (nghìn)'),('output_tokens','Output token (nghìn)')]):
            x=220+panel*290;width=240;factor=1000 if 'tokens' in metric else 1
            high=max(r[metric]/factor for r in data)*1.08
            scale=axis(d,x,220,width,0,max(1,high),label)
            for j,arm in enumerate(ARMS):
                y=460-j*62
                if panel==0:text(d,25,y,LABELS[j],10)
                values=[r[metric]/factor for r in data if r['arm']==arm]
                for k,v in enumerate(values):d.add(Circle(scale(v),y+(k%5-2)*4,2.7,fillColor=HexColor(COLORS[j]),strokeColor=None))
                d.add(Line(scale(quantile(values,.25)),y-16,scale(quantile(values,.75)),y-16,strokeColor=black,strokeWidth=2))
                d.add(Line(scale(statistics.median(values)),y-21,scale(statistics.median(values)),y-11,strokeColor=black,strokeWidth=2))
        text(d,35,100,'Token theo CLI từng runtime; reasoning/thinking được lưu riêng, không cộng lần nữa vào output.',10)
        text(d,35,78,'Không quy quota thuê bao thành USD; không dùng biểu đồ này để xếp hạng hai agent.',10)
        store(d,runtime+'-resources')
    d=frame('Jev — phạm vi tư vấn và tiền ghi nhận','Tư vấn của cùng 20 nguồn được dùng lại cho Gemini; không có lời gọi Jev mới trong đợt Gemini.')
    complete=sum(r['scope_complete'] for r in coverage['cases'])
    for j,(label,value,color) in enumerate([('Đủ phạm vi',complete,'#187B72'),('Thiếu phạm vi',20-complete,'#9A659D')]):
        y=430-j*65;text(d,45,y+8,label,12);d.add(Rect(260,y,value/20*600,30,fillColor=HexColor(color),strokeColor=None));text(d,880,y+8,f'{value}/20',12)
    known=float(cost['total_known_usage_usd']);reserved=float(cost['total_reserved_or_actual_usd']);cap=float(cost['cash_cap_usd'])
    text(d,45,285,'USD cộng dồn, gồm pilot trước; không phải chi phí riêng của 80 bản công khai.',11)
    for j,(label,value) in enumerate([('Usage đã biết',known),('Usage + dự phòng',reserved),('Trần được duyệt',cap)]):
        y=220-j*48;text(d,45,y+7,label,11);d.add(Rect(260,y,value/cap*600,23,fillColor=HexColor('#697A9E'),strokeColor=None));text(d,880,y+7,f'{value:.6f} USD',11)
    text(d,35,65,f"{cost['total_requests']} request cộng dồn; {cost['total_unknown_billing_requests']} lượt chưa rõ tiền. Chưa đối soát hóa đơn. Phạm vi không phải chất lượng.",10)
    store(d,'jev-coverage-cost')
    save(out/'figure-manifest.json',{'formats':['SVG','PDF'],'figures':records,
         'renderer':'ReportLab','renderer_version':reportlab.Version,
         'font_path':str(font),'font_sha256':sha(font)})
    return records

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--charts',action='store_true');a=p.parse_args()
    if a.output.exists():raise ValueError('Output must be new')
    rows=collect();s=summarize(rows);coverage=read(CODEX/'evidence-verification.json');cost=read(CODEX/'cost-reconciliation.json')
    a.output.mkdir(parents=True);table(a.output/'cells.csv',rows);save(a.output/'summary.json',{'design':'within-agent original/edited; descriptive only','quality_assessed':False,'rows':s,'jev_coverage':coverage,'jev_cost':cost})
    flat=[]
    for item in s:
        r={k:v for k,v in item.items() if not isinstance(v,dict)}
        for k,v in item.items():
            if isinstance(v,dict):r.update({k+'_'+key:value for key,value in v.items()})
        flat.append(r)
    table(a.output/'summary.csv',flat)
    save(a.output/'input-manifest.json',INPUTS)
    if a.charts:figures(a.output/'charts',rows,s,coverage,cost)
    save(a.output/'receipt.json',{'analysis_code_sha256':sha(__file__),'input_count':len(INPUTS),'output_cells':len(rows),'new_inference':0,'new_jev_calls':0,'human_data_accessed':0,'forms_accessed':0})
    print(json.dumps({'cells':len(rows),'input_files':len(INPUTS),'summary':str(a.output/'summary.json')}))

if __name__=='__main__':main()
