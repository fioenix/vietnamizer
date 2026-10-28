"""Scientific SVG/PDF charts from precomputed public-human labels; optional ReportLab."""
from pathlib import Path
import json
from benchmarks import public_human as h

ARM_LABELS = {'bare':'Basic request','ordinary':'Ordinary prompt',
              'vietnamizer':'Vietnamizer','vietnamizer_jev':'Vietnamizer + Jev'}


def charts(folder):
    folder = Path(folder); r = h.read(folder/'summary.json')
    if not r['quality_chart_allowed'] or r['status'] not in ('synthetic_test_only','two_selected_human_reviews'):
        raise ValueError('No selected human labels: quality charts withheld')
    from reportlab.graphics.shapes import Drawing,Rect,String,Line,Circle
    from reportlab.graphics import renderPDF,renderSVG
    from reportlab.lib.colors import HexColor,white,black
    out = folder/'charts'; out.mkdir(exist_ok=False)
    palette = {'preserved':'#1B7862','better':'#1B7862','changed':'#B34F53',
               'worse':'#B34F53','equivalent':'#76759C','uncertain':'#C9A448','missing':'#D5D7DB'}
    label = 'SYNTHETIC TEST DATA — NOT BENCHMARK RESULTS' if r['is_fixture'] else 'HUMAN RATINGS · PUBLIC AI COHORT'
    records = []
    def text(d,x,y,value,size=10,color=black):
        d.add(String(x,y,str(value),fontName='Helvetica',fontSize=size,fillColor=color))
    def frame(title,height=570):
        d=Drawing(1100,height);d.add(Rect(0,0,1100,height,fillColor=white,strokeColor=None))
        text(d,35,height-30,title,18);text(d,35,height-52,label,11)
        return d
    def footer(d,extra):
        text(d,35,25,'20 source clusters; fixed reviewers A/B; one curated public SFT publisher; generator model unattested.',9)
        text(d,35,11,extra,9)
    def save(d,name):
        for suffix,renderer in [('svg',renderSVG),('pdf',renderPDF)]:
            path=out/(name+'.'+suffix);renderer.drawToFile(d,str(path))
            records.append({'file':path.name,'sha256':h.digest(path.read_bytes())})
    for dimension in ('preservation','readability'):
        d=frame('Label distribution · '+dimension)
        text(d,35,480,'Each bar = 20 planned sources; missing and uncertain remain visible. Counts, not independent label trials.',10)
        for n,row in enumerate(x for x in r['rates'] if x['dimension']==dimension):
            y=435-n*42;text(d,35,y+8,row['reviewer']+' · '+ARM_LABELS[row['arm']],11);x=300
            for category in h.CATEGORIES[dimension]:
                count=row['counts'][category];width=count/20*650
                if width:
                    d.add(Rect(x,y,width,25,fillColor=HexColor(palette[category]),strokeColor=white))
                    text(d,x+5,y+8,count,10,black if category in ('missing','uncertain') else white)
                x+=width
            text(d,970,y+8,'defined '+str(row['determinate'])+'/20',10)
        x=35
        for category in h.CATEGORIES[dimension]:
            d.add(Rect(x,67,12,12,fillColor=HexColor(palette[category]),strokeColor=None));text(d,x+17,69,category,10);x+=180
        footer(d,'Same source and two fixed raters across four modes. No superiority or population-reader claim from counts alone.')
        save(d,'labels-'+dimension)
    for metric in ('better','changed'):
        d=frame('Before / after on the same agent · '+metric,760)
        text(d,35,675,'Reference = frozen original AI text. Codex cohort only; no cross-agent comparison.',10)
        text(d,35,657,'Rate among determinate ratings; pooled rows keep both fixed raters within source clusters.',10)
        scale=lambda v:560+v*230
        for value in (0,.25,.5,.75,1):
            d.add(Line(scale(value),105,scale(value),630,strokeColor=HexColor('#D5D7DB')))
            text(d,scale(value)-5,85,int(value*100),9)
        for n,row in enumerate(x for x in r['before_after'] if x['metric']==metric):
            y=610-n*42
            text(d,35,y,ARM_LABELS[row['arm']]+' vs original · '+row['reviewer'],10)
            if row['estimate'] is not None:
                if row['low'] is not None:
                    d.add(Line(scale(row['low']),y+3,scale(row['high']),y+3,strokeColor=HexColor('#1B7862'),strokeWidth=2))
                d.add(Circle(scale(row['estimate']),y+3,3,fillColor=HexColor('#1B7862'),strokeColor=None))
            else:text(d,650,y,'N/A',10)
            text(d,820,y,'n='+str(row['n_sources'])+'/20; excluded='+str(row['excluded_sources'])+(' *' if row['degenerate'] else ''),10)
        text(d,560,58,'Original-relative rate (%)',10)
        text(d,35,40,'* Identical observed source values: bootstrap may have zero width; this is not population certainty. No CI below 2 sources.',9)
        footer(d,'10,000 source-cluster draws; seed 25033. Unknown/missing excluded from estimates and CIs. Preservation separate.')
        save(d,'before-after-'+metric)
    for metric in ('better','changed'):
        d=frame('Secondary within-agent mode contrasts · '+metric,650)
        text(d,35,565,'a minus b; percentile bootstrap 10,000 draws, seed 25033; source clusters keep fixed raters together.',10)
        text(d,35,547,'Pooled rows require determinate labels for both modes and both raters; exclusions reported.',10)
        scale=lambda v:480+(v+1)/2*360
        for value in (-1,-.5,0,.5,1):
            d.add(Line(scale(value),100,scale(value),515,strokeColor=HexColor('#D5D7DB')));text(d,scale(value)-8,80,int(value*100),9)
        for n,row in enumerate(x for x in r['comparisons'] if x['metric']==metric):
            y=495-n*43
            text(d,35,y,ARM_LABELS[row['a']]+' - '+ARM_LABELS[row['b']]+' · '+row['reviewer'],10)
            if row['estimate'] is not None:
                if row['low'] is not None:d.add(Line(scale(row['low']),y+3,scale(row['high']),y+3,strokeColor=HexColor('#1B7862'),strokeWidth=2))
                d.add(Circle(scale(row['estimate']),y+3,3,fillColor=HexColor('#1B7862'),strokeColor=None))
            else:text(d,620,y,'N/A',10)
            text(d,865,y,'n='+str(row['n_sources'])+'/20; excluded='+str(row['excluded_sources'])+(' *' if row['degenerate'] else ''),10)
        text(d,480,58,'Difference (percentage points)',10)
        text(d,35,40,'* Identical observed differences: bootstrap may have zero width; this is not population certainty.',9)
        footer(d,'CI conditional on sampled sources; no CI below 2 complete clusters. Secondary comparisons exploratory; no p-values.')
        save(d,'paired-'+metric)
    for dimension in ('preservation','readability'):
        d=frame('Reviewer agreement · '+dimension,590);cats=h.CATEGORIES[dimension];a=r['agreement'][dimension]
        text(d,35,510,'Counts across 80 paired outputs; descriptive dependent pairs. Missing/uncertain categories included.',10)
        size=62;left=340;top=435
        for i,ca in enumerate(cats):
            text(d,left-115,top-i*size+10,ca,10);text(d,left+i*size,top+55,ca,9)
            for j,cb in enumerate(cats):
                count=a['matrix'][ca][cb];shade=255-int(160*count/80);color=HexColor(f'#{shade:02x}{shade:02x}ff')
                d.add(Rect(left+j*size-5,top-i*size-8,size,size-5,fillColor=color,strokeColor=white));text(d,left+j*size+15,top-i*size+12,count,12)
        text(d,35,100,'Determinate pairs: '+str(a['determinate_pairs'])+'/80; missing: '+str(a['missing_pairs'])+'; uncertain: '+str(a['uncertain_pairs']),11)
        exact='N/A' if a['exact_agreement'] is None else f"{a['exact_agreement']:.3f}"
        kappa='N/A' if a['kappa'] is None else f"{a['kappa']:.3f}"
        text(d,35,80,'Exact agreement / nominal kappa on determinate pairs: '+exact+' / '+kappa,11)
        footer(d,'Rows = reviewer A; columns = reviewer B. Kappa undefined for zero/degenerate determinate marginals. No pair-level CI.')
        save(d,'agreement-'+dimension)
    h.save(out/'figure-manifest.json',{'is_fixture':r['is_fixture'],'result_sha256':h.digest((folder/'summary.json').read_bytes()),
                                     'formats':['SVG','PDF'],'figures':records})
    return records
