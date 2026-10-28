import io,json,tempfile,unittest,urllib.error
from pathlib import Path
from unittest.mock import patch
from benchmarks import jev_capture as capture

class CaptureTest(unittest.TestCase):
 def test_success_body_persisted_before_json_validation(self):
  with tempfile.TemporaryDirectory() as t:
   target=Path(t);reply=io.BytesIO(b'{not JSON');reply.status=200;reply.headers={}
   with patch.object(capture,'open_response',return_value=reply):
    meta=capture.exchange({'state':'synthetic'},'fake-test-key',1,target)
   self.assertTrue(meta['body_complete'])
   self.assertEqual((target/'response.body').read_bytes(),b'{not JSON')
   with self.assertRaises(capture.CaptureError):capture.decode(target,meta)
   self.assertEqual((target/'response.body').read_bytes(),b'{not JSON')
 def test_http_error_keeps_body_and_status_without_auth(self):
  with tempfile.TemporaryDirectory() as t:
   error=urllib.error.HTTPError('https://api.typesafe.ai/v1/systemone',429,'limited',{'Retry-After':'2'},io.BytesIO(b'{"error":"rate_limit"}'))
   with patch.object(capture,'open_response',side_effect=error):meta=capture.exchange({},'fake-test-key',1,Path(t))
   self.assertEqual(meta['http_status'],429);self.assertEqual(meta['retry_after_seconds'],2)
   self.assertIn(b'rate_limit',(Path(t)/'response.body').read_bytes())
   with self.assertRaises(capture.CaptureError) as c:capture.decode(Path(t),meta)
   self.assertEqual(c.exception.diagnostic['http_status'],429)
 def test_credential_echo_redacted_and_request_has_no_headers(self):
  with tempfile.TemporaryDirectory() as t:
   reply=io.BytesIO(b'{"echo":"fake-test-key"}');reply.status=200;reply.headers={}
   with patch.object(capture,'open_response',return_value=reply):meta=capture.exchange({'a':1},'fake-test-key',1,Path(t))
   self.assertTrue(meta['credential_redacted'])
   for p in Path(t).iterdir():self.assertNotIn(b'fake-test-key',p.read_bytes())
 def test_network_failure_retains_empty_body_and_phase(self):
  with tempfile.TemporaryDirectory() as t:
   with patch.object(capture,'open_response',side_effect=TimeoutError):meta=capture.exchange({},'fake-test-key',1,Path(t))
   self.assertFalse(meta['body_complete']);self.assertEqual(meta['failure_kind'],'timeout')
   self.assertEqual((Path(t)/'response.body').read_bytes(),b'')
 def test_interrupted_echo_never_persists_credential_prefix(self):
  secret='fake-long-test-secret'
  class Interrupted(io.BytesIO):
   status=200;headers={}
   def __init__(self):self.n=0
   def read1(self,n):
    self.n+=1
    if self.n==1:return b'prefix:'+secret.encode()+b'x'*(len(secret)-1)
    raise KeyboardInterrupt
   def close(self):pass
  with tempfile.TemporaryDirectory() as t:
   with patch.object(capture,'open_response',return_value=Interrupted()):
    with self.assertRaises(KeyboardInterrupt):capture.exchange({},secret,1,Path(t))
   raw=(Path(t)/'response.body').read_bytes()
   self.assertNotIn(secret[:-1].encode(),raw)
 def test_parent_deadline_records_surviving_partial_digest(self):
  import subprocess,hashlib
  with tempfile.TemporaryDirectory() as t:
   target=Path(t);(target/'response.body').write_bytes(b'partial')
   capture.save(target/'http.json',{'phase':'reading','http_status':200,'body_complete':False})
   class Child:
    returncode=None
    def __init__(self):self.n=0
    def __enter__(self):return self
    def __exit__(self,*_):pass
    def kill(self):pass
    def communicate(self,*_,**kwargs):
     self.n+=1
     if self.n==1:raise subprocess.TimeoutExpired('fake',1)
     return b'',b''
   with patch.object(capture.subprocess,'Popen',return_value=Child()):
    with self.assertRaises(capture.CaptureError) as ctx:capture.request({},'fake',1,target)
   self.assertEqual(ctx.exception.diagnostic['stored_body_bytes'],7)
   self.assertEqual(ctx.exception.diagnostic['stored_body_digest'],hashlib.sha256(b'partial').hexdigest())

 def test_oversize_capture_keeps_withheld_secret_suffix(self):
  secret='fake-long-test-secret'
  with tempfile.TemporaryDirectory() as t:
   reply=io.BytesIO(b'x'*11+secret.encode());reply.status=200;reply.headers={}
   with patch.object(capture,'open_response',return_value=reply),patch.object(capture,'MAX_RESPONSE',30):
    meta=capture.exchange({},secret,1,Path(t))
   self.assertFalse(meta['body_complete'])
   self.assertEqual(meta['failure_kind'],'response_too_large')
   self.assertNotIn(secret[:-1].encode(),(Path(t)/'response.body').read_bytes())

if __name__=='__main__':unittest.main()
