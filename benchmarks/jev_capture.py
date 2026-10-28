"""Opt-in benchmark-only raw HTTP capture. Production Jev transport is unchanged."""
import hashlib,json,os,subprocess,sys,time,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from jev.transport import ENDPOINT,MAX_RESPONSE,NoRedirect,ServiceError,encoded
from benchmarks.jev_pilot import save,read

class CaptureError(ServiceError):
 def __init__(self,diagnostic):
  self.diagnostic=diagnostic
  super().__init__('deadline_exceeded' if diagnostic.get('failure_kind')=='deadline' else 'service_failed')

def open_response(payload,key,timeout):
 req=urllib.request.Request(ENDPOINT,data=encoded(payload),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'},method='POST')
 return urllib.request.build_opener(NoRedirect()).open(req,timeout=timeout)

def exchange(payload,key,timeout,target):
 """Persist response bytes even for HTTP errors or invalid JSON. Never retain auth headers."""
 target.mkdir(parents=True,exist_ok=True)
 (target/'request.body').write_bytes(encoded(payload))
 (target/'response.body').write_bytes(b'')
 meta={'phase':'opening','http_status':None,'body_complete':False,'body_bytes_received':0,
       'credential_redacted':False,'started_at':time.time(),'endpoint':ENDPOINT,'method':'POST'}
 save(target/'http.json',meta);data=b'';reply=None;started=time.monotonic()
 try:
  try:reply=open_response(payload,key,timeout)
  except urllib.error.HTTPError as error:reply=error
  meta.update(phase='reading',http_status=reply.status if hasattr(reply,'status') else reply.code)
  after=reply.headers.get('Retry-After')
  if after is not None and str(after).isdigit():meta['retry_after_seconds']=min(int(after),60)
  save(target/'http.json',meta)
  while True:
   chunk=(reply.read1 if hasattr(reply,'read1') else reply.read)(min(65536,MAX_RESPONSE+1-len(data)))
   if not chunk:meta['body_complete']=True;break
   data+=chunk;meta['body_bytes_received']=len(data)
   # Keep a credential-sized suffix in memory until EOF to protect split echoes.
   secret=key.encode();safe=data.replace(secret,b'<credential-redacted>') if secret else data
   meta['credential_redacted']=bool(secret and secret in data)
   safe=safe[:max(0,len(safe)-len(secret)+1)] if secret else safe
   (target/'response.body').write_bytes(safe)
   save(target/'http.json',meta)
   if len(data)>MAX_RESPONSE:meta['failure_kind']='response_too_large';break
  meta['credential_redacted']=bool(key and key.encode() in data)
  if meta['body_complete']:
   (target/'response.body').write_bytes(data.replace(key.encode(),b'<credential-redacted>') if key else data)
  meta['phase']='received'
 except (TimeoutError,urllib.error.URLError,OSError) as error:
  meta.update(failure_kind='timeout' if isinstance(error,TimeoutError) else 'network',failure_phase=meta['phase'],phase='transport_error',error_type=type(error).__name__)
  # Retain only the already sanitized safe prefix after an interrupted read.
 finally:
  if reply is not None:reply.close()
  meta['elapsed_seconds']=time.monotonic()-started
  meta['stored_body_bytes']=(target/'response.body').stat().st_size
  meta['stored_body_digest']=hashlib.sha256((target/'response.body').read_bytes()).hexdigest()
  save(target/'http.json',meta)
 return meta

def decode(target,meta):
 if meta.get('failure_kind') or meta.get('http_status')!=200 or not meta.get('body_complete') or meta.get('credential_redacted'):
  raise CaptureError(meta)
 try:return json.loads((target/'response.body').read_bytes())
 except (ValueError,UnicodeError,RecursionError):raise CaptureError(dict(meta,failure_kind='invalid_json',phase='decode')) from None

def request(payload,key,timeout,target):
 """Killable child bounds the entire request. Raw files survive child deadlines/crashes."""
 target=target.resolve();target.mkdir(parents=True,exist_ok=True)
 command=[sys.executable,'-I','-B',str(Path(__file__).resolve()),'worker']
 envelope=encoded({'payload':payload,'key':key,'timeout':timeout,'target':str(target)})
 started=time.monotonic()
 with subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL) as child:
  try:output,_=child.communicate(envelope,timeout=timeout)
  except (subprocess.TimeoutExpired,BaseException) as error:
   child.kill();child.communicate()
   meta=read(target/'http.json') if (target/'http.json').exists() else {'phase':'child_start'}
   body=target/'response.body'
   meta.update(failure_kind='deadline' if isinstance(error,subprocess.TimeoutExpired) else 'cancelled',elapsed_seconds=time.monotonic()-started,stored_body_bytes=body.stat().st_size if body.exists() else 0,stored_body_digest=hashlib.sha256(body.read_bytes()).hexdigest() if body.exists() else None)
   save(target/'http.json',meta)
   if not isinstance(error,subprocess.TimeoutExpired):raise
   raise CaptureError(meta) from None
 if child.returncode:
  meta=read(target/'http.json') if (target/'http.json').exists() else {'phase':'child_start'}
  raise CaptureError(dict(meta,failure_kind='worker_exit',child_exit_code=child.returncode))
 meta=read(target/'http.json')
 return decode(target,meta)

if __name__=='__main__':
 if sys.argv[1:]!=['worker']:raise SystemExit('worker only')
 envelope=json.load(sys.stdin)
 exchange(envelope['payload'],envelope['key'],envelope['timeout'],Path(envelope['target']))
