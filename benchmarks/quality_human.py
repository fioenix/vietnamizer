"""Package private offline reviewer bundles and validate returned human submissions."""
from pathlib import Path
import argparse,hashlib,json,shutil,zipfile
from datetime import datetime
from benchmarks import quality_review as q

def embed(value):return json.dumps(value,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
def source_digest(rows):return hashlib.sha256(json.dumps(rows,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def validate(packet,submission):
 s=submission;p=packet;cases=p['cases']
 if q.digest(cases)!=p['packet_digest']:raise ValueError('human packet content digest mismatch')
 if any(s.get(k)!=v for k,v in {'kind':'human','version':p['version'],'reviewer':p['reviewer'],'packet_digest':p['packet_digest'],'submission':'final'}.items()):raise ValueError('human packet/submission binding')
 profile=s.get('profile',{})
 if profile.get('independent') is not True or any(not isinstance(profile.get(k),str) or not profile[k].strip() for k in ('experience','conflicts')):raise ValueError('reviewer declaration missing')
 if not isinstance(s.get('sources'),dict) or not isinstance(s.get('grades'),dict) or set(s['sources'])!={c['id'] for c in cases} or set(s['grades'])!={c['id'] for c in cases}:raise ValueError('human label cardinality')
 rows=[s['sources'][c['id']] for c in cases];q.validate_inventory(cases,{'sources':rows})
 if any(r.get('reviewed') is not True for r in rows):raise ValueError('source not reviewed')
 lock=s.get('source_lock',{})
 if lock.get('digest')!=source_digest(rows):raise ValueError('source lock digest mismatch')
 try:datetime.fromisoformat(lock['at'].replace('Z','+00:00'))
 except (ValueError,KeyError,TypeError):raise ValueError('source lock timestamp')
 if not any(e.get('type')=='source_locked' and e.get('digest')==lock['digest'] and e.get('at')==lock['at'] for e in s.get('events',[])):raise ValueError('source lock event missing')
 for c,r in zip(cases,rows):q.validate_grade(c,r,s['grades'][c['id']])
 return s

def bundle(out):
 q.verify(out);root=q.ROOT/'benchmarks';design=Path('/Users/fioenix/Projects/finolabs/design-system')
 index={}
 for who in ('A','B'):
  folder=out/'human-handoff'/f'reviewer-{who}';folder.mkdir(parents=True,exist_ok=True)
  cases=q.read(out/'packets'/f'{who}.json');p={'version':'editorial-quality-v1','reviewer':who,'packet_digest':q.digest(cases),'cases':cases}
  (folder/'review.html').write_text((root/'reviewer.html').read_text().replace('__REVIEW_DATA__',embed(p)))
  q.save(folder/'packet.json',p)
  d=folder/'design';d.mkdir(exist_ok=True)
  for path in ('packages/tokens/theme.css','packages/tokens/base.css','packages/tokens/fino-brand.css','utilities.css','LICENSE','THIRD_PARTY_NOTICES.md'):
   dest=d/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(design/path,dest)
  (d/'styles.css').write_text('\n'.join(line for line in (design/'styles.css').read_text().splitlines() if 'fonts.googleapis.com' not in line)+'\n')
  (folder/'HUONG-DAN.txt').write_text('Giải nén toàn bộ gói. Mở review.html bằng Chrome mới. Không cần cài đặt hay đăng nhập.\nRà đủ 20 nguồn, trích nguyên văn từng lỗi cần sửa; nguồn tốt có thể không có lỗi. Khóa nguồn rồi chấm 80 bản.\nChia bốn phiên, mỗi phiên năm nguồn; xuất bản nháp JSON sau mỗi phiên. Nhập lại JSON nếu đổi máy.\nChỉ nhận gói của mình; không xem điểm model, khóa chế độ hoặc nhãn người kia. Không dùng AI chấm hộ.\nXuất bản cuối khi đủ nhãn rồi gửi file reviewer-'+who+'-final.json cho Fio. Không gửi ảnh chụp thay cho JSON.\nTự lưu chỉ nằm trên trình duyệt/máy hiện tại; luôn giữ file JSON dự phòng.\n')
  q.save(folder/'checksums.json',{str(p.relative_to(folder)):q.digest(p.read_bytes()) for p in sorted(folder.rglob('*')) if p.is_file() and p.name!='checksums.json'})
  target=out/'human-handoff'/f'reviewer-{who}.zip'
  with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
   for file in sorted(folder.rglob('*')):
    if file.is_file():z.write(file,str(Path(f'reviewer-{who}')/file.relative_to(folder)))
  index[who]={'path':str(target),'sha256':q.digest(target.read_bytes()),'packet_digest':p['packet_digest']}
 q.save(out/'human-handoff/manifest.json',{'reviewer_bundles':index,'distribution':'one bundle per reviewer; do not send coordinator keys or model labels','fonts':'Offline bundle omits remote font import; canonical FINOLABS tokens/styles copied with notices. Internal review use only.','human_submissions_received':0})
 return index

def ingest(out,submission_path):
 q.verify(out)
 s=json.loads(Path(submission_path).read_text(),object_pairs_hook=q.unique_pairs);who=s.get('reviewer')
 if who not in ('A','B'):raise ValueError('reviewer identity')
 if s.get('qa_only'):raise ValueError('synthetic UI test is not a human submission')
 cases=q.read(out/'packets'/f'{who}.json');packet={'version':'editorial-quality-v1','reviewer':who,'packet_digest':q.digest(cases),'cases':cases}
 if q.read(out/'human-handoff'/f'reviewer-{who}'/'packet.json')!=packet:raise ValueError('handoff packet differs from frozen assignment')
 validate(packet,s)
 target=out/'human-submissions'/f'{who}-{q.digest(Path(submission_path).read_bytes())}.json'
 if not target.exists():target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(submission_path,target)
 return target

def main():
 p=argparse.ArgumentParser();p.add_argument('command',choices=('bundle','ingest'));p.add_argument('--output',type=Path,required=True);p.add_argument('--submission',type=Path);a=p.parse_args()
 if a.command=='bundle':print(json.dumps(bundle(a.output.resolve()),ensure_ascii=False))
 else:
  if not a.submission:raise ValueError('submission required')
  print(ingest(a.output.resolve(),a.submission))
if __name__=='__main__':main()
