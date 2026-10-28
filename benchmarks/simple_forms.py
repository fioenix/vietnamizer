"""Prepare direct blinded human comparisons; preserve model-v1 evidence unchanged."""
from pathlib import Path
import argparse,base64,hashlib,json,re
from benchmarks import quality_review as q
FORM_IDS={'A':'1V_gzac9YcCHQ4dXJkRFuY4aJqoMMhgt__-wxSDShOVs','B':'1t1l4bIcoNTQIdBC_56mK0m_koTZHfUK0hLZHonYHGqg'}
QUESTIONS=[{'key':'preservation','kind':'grid','title':'1. Bản sửa có giữ đúng ý, số liệu và giọng người viết không?','choices':['Giữ đúng','Có chỗ bị đổi','Chưa rõ']},{'key':'readability','kind':'grid','title':'2. Bản sửa đọc thế nào so với bản gốc?','choices':['Tự nhiên, rõ ràng hơn','Tương đương','Khó đọc hơn','Chưa rõ']},{'key':'notes','kind':'paragraph','title':'3. Có chỗ nào sửa sai, sửa thừa hoặc vẫn khó hiểu không?','help':'Ghi bản A/B/C/D, trích đoạn và lý do. Nếu không có thì ghi “Không có”.'}]
LABELS={'preservation':dict(zip(QUESTIONS[0]['choices'],['preserved','changed','uncertain'])),'readability':dict(zip(QUESTIONS[1]['choices'],['better','equivalent','worse','uncertain']))}

def contract(packet):
 groups=[];seen=set()
 for c in packet['cases']:
  if c['id'] in seen or set(c['outputs'])!=set('ABCD'):raise ValueError('comparison identity')
  seen.add(c['id']);groups.append({**{k:c[k] for k in ('id','source','audience','purpose')},'outputs':{k:c['outputs'][k]['text'] for k in 'ABCD'}})
 return {'schema':'human-simple-v2','reviewer':packet['reviewer'],'packet_digest':q.digest(packet['cases']),'questions':QUESTIONS,'groups':groups}

def decode(c,itemmap,raw):
 data={}
 for row in raw:
  ident=row['item_id']
  if ident in data:raise ValueError('duplicate provider item')
  data[ident]=row['response']
 rows=[]
 for group in c['groups']:
  ids=itemmap[group['id']];outputs={k:{} for k in 'ABCD'}
  for key in ('preservation','readability'):
   answers=data.get(ids[key])
   if answers is not None and (not isinstance(answers,list) or len(answers)!=4):raise ValueError('grid cardinality')
   for i,k in enumerate('ABCD'):
    answer=answers[i] if answers is not None else None
    if answer in (None,''):label=None
    elif answer in LABELS[key]:label=LABELS[key][answer]
    else:raise ValueError('unknown answer label')
    outputs[k][key]=label
  note=data.get(ids['notes'])
  if note is not None and not isinstance(note,str):raise ValueError('note structure')
  rows.append({'id':group['id'],'outputs':outputs,'notes':note})
 return rows

def wrap_text(text,font,width):
 # Preserve every character; wrapping only adds presentation line breaks.
 lines=[]
 for paragraph in text.split('\n'):
  if not paragraph:lines.append('');continue
  line=''
  for token in re.findall(r'\S+|\s+',paragraph):
   if line and font.getlength(line+token)>width:lines.append(line);line=''
   if font.getlength(token)>width:
    for ch in token:
     if line and font.getlength(line+ch)>width:lines.append(line);line=''
     line+=ch
   else:line+=token
  lines.append(line)
 return lines

def render_pair(source,edited,path):
 from PIL import Image,ImageDraw,ImageFont
 font_path='/System/Library/Fonts/Supplemental/Arial.ttf';font=ImageFont.truetype(font_path,40);bold=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',38)
 width=1600;padding=45;gap=70;col=(width-2*padding-gap)//2;line_height=53
 left=wrap_text(source,font,col);right=wrap_text(edited,font,col);height=145+line_height*max(len(left),len(right))+40
 im=Image.new('RGB',(width,height),'white');draw=ImageDraw.Draw(im)
 draw.text((padding,30),'BẢN GỐC',font=bold,fill='black');draw.text((padding+col+gap,30),'BẢN SỬA',font=bold,fill='black');draw.line((width//2,25,width//2,height-25),fill=(190,190,190),width=2)
 for x,lines in ((padding,left),(padding+col+gap,right)):
  for i,line in enumerate(lines):draw.text((x,112+i*line_height),line,font=font,fill='black')
 path.parent.mkdir(parents=True,exist_ok=True);im.save(path,format='PNG',optimize=True)
 return {'sha256':q.digest(path.read_bytes()),'width':width,'height':height,'source_digest':q.digest(source.encode()),'edited_digest':q.digest(edited.encode()),'font':font_path,'font_size':40,'left':'original','right':'edited','rendered_text_lossless':''.join(left)==source.replace('\n','') and ''.join(right)==edited.replace('\n','')}

def prepare(origin,out):
 q.verify(origin);contracts={};images={};packets={}
 for who in ('A','B'):
  cases=q.read(origin/'packets'/f'{who}.json');packet={'version':'editorial-quality-v1','reviewer':who,'packet_digest':q.digest(cases),'cases':cases}
  if q.read(origin/'human-handoff'/f'reviewer-{who}'/'packet.json')!=packet:raise ValueError('handoff packet differs from frozen assignment')
  packets[who]=packet
 out.mkdir(parents=True,exist_ok=True)
 for who,packet in packets.items():
  c=contract(packet)
  if len(c['groups'])!=20:raise ValueError('expected20documents')
  contracts[who]=c;q.save(out/f'{who}-contract.json',c);images[who]={}
  for group in c['groups']:
   images[who][group['id']]={}
   for letter,text in group['outputs'].items():
    p=out/'images'/who/f'{group["id"]}-{letter}.png';meta=render_pair(group['source'],text,p)
    if not meta['rendered_text_lossless']:raise ValueError('render text omission')
    images[who][group['id']][letter]={'path':str(p.resolve()),**meta}
 q.save(out/'images.json',images)
 q.base.freeze_manifest(out/'manifest.json',{'schema':'human-simple-v2','origin':str(origin.resolve()),'form_ids':FORM_IDS,'contract_digests':{w:q.digest(c) for w,c in contracts.items()},'questions':QUESTIONS,'images_digest':q.digest(images),'driver_digest':q.digest(Path(__file__).read_bytes()),'runtime_digest':q.digest((q.ROOT/'benchmarks/simple_forms.gs').read_bytes()),'item_count_per_form':162,'planned_output_reviews':160,'human_submissions':0})
 return out

def batch(out,mode,who=None,start=0,count=5):
 m=q.read(out/'manifest.json')
 if q.digest(Path(__file__).read_bytes())!=m['driver_digest'] or q.digest((q.ROOT/'benchmarks/simple_forms.gs').read_bytes())!=m['runtime_digest']:raise ValueError('driver drift')
 payload={'schema':m['schema'],'mode':mode,'form_ids':FORM_IDS,'contract_digests':m['contract_digests'],'questions':QUESTIONS}
 if who:
  c=q.read(out/f'{who}-contract.json')
  if q.digest(c)!=m['contract_digests'][who]:raise ValueError('contract drift')
  payload.update(who=who,packet_digest=c['packet_digest'])
 if mode=='append':
  image_map=q.read(out/'images.json')
  if q.digest(image_map)!=m['images_digest']:raise ValueError('image map drift')
  payload['groups']=[]
  for group in c['groups'][start:start+count]:
   row={**group,'images':{}}
   for letter,meta in image_map[who][group['id']].items():
    raw=Path(meta['path']).read_bytes()
    if q.digest(raw)!=meta['sha256']:raise ValueError('image drift')
    row['images'][letter]={'base64':base64.b64encode(raw).decode(),'sha256':meta['sha256']}
   payload['groups'].append(row)
  payload['start']=start
 name=f'{mode}-{who or "both"}-{start:02}-{count}';path=out/'batches'/f'{name}.gs';path.parent.mkdir(exist_ok=True)
 encoded=json.dumps(payload,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e');source=(q.ROOT/'benchmarks/simple_forms.gs').read_text().replace('/*__BATCH_DATA__*/',encoded)
 path.write_text(source);q.save(path.with_suffix('.json'),{'payload_digest':q.digest(payload),'script_digest':q.digest(path.read_bytes()),'mode':mode,'who':who,'start':start,'count':len(payload.get('groups',[]))});return path

def main():
 p=argparse.ArgumentParser();p.add_argument('command',choices=('prepare','batch'));p.add_argument('--origin',type=Path,default=q.ROOT/'artifacts/014-quality-assessment-20261025-v3');p.add_argument('--output',type=Path,required=True);p.add_argument('--mode',choices=('initialize','append','finish','audit'));p.add_argument('--who',choices=('A','B'));p.add_argument('--start',type=int,default=0);p.add_argument('--count',type=int,default=5);a=p.parse_args()
 if a.command=='prepare':print(prepare(a.origin,a.output))
 else:print(batch(a.output,a.mode,a.who,a.start,a.count))
if __name__=='__main__':main()
