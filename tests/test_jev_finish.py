import unittest,json,shutil,tempfile
from pathlib import Path
from unittest.mock import patch
from tests.test_jev import response
from benchmarks import jev_finish as finish

class FinishTest(unittest.TestCase):
 def test_only_evidenced_transient_errors_are_retryable(self):
  for d in ({'failure_kind':'timeout'},{'failure_kind':'deadline'},{'failure_kind':'network'},{'http_status':429},{'http_status':503}):
   self.assertTrue(finish.retryable(d),d)
  for d in ({'phase':'validation','reason':'score_distribution'},{'http_status':400},{'phase':'budget','reason':'cap_reached'},{'failure_kind':'invalid_json'}):
   self.assertFalse(finish.retryable(d),d)
 def test_no_fallback_counts_as_complete(self):
  with self.assertRaises(ValueError):finish.require_answers({'status':'incomplete','answers_complete':False})
  with self.assertRaises(ValueError):finish.require_answers({'answers_complete':True,'counts':{'uncompleted':1}})
  finish.require_answers({'status':'incomplete','scope_complete':False,'evaluation_complete':False,'context_complete':False,'answers_complete':True,'source_accounted':True,'segmentation_complete':True,'counts':{'uncompleted':0,'validated':1}})
 def test_full_case_cache_recovery_codex_report_and_resume_offline(self):
  live=finish.ROOT/'artifacts/014-jev-recovery-20261025'
  if not (live/'manifest.json').exists():self.skipTest('local diagnostic artifacts unavailable')
  with tempfile.TemporaryDirectory() as t:
   out=Path(t)/'recovery';out.mkdir()
   for name in ('manifest.json','requests','evaluations','prompts'):
    src=live/name;dst=out/name
    if src.is_dir():shutil.copytree(src,dst)
    else:shutil.copyfile(src,dst)
   # Freeze the initial two one-request diagnostics, independent of live progress.
   for request in (out/'requests').iterdir():
    if request.name not in ('0001','0002'):shutil.rmtree(request)
   for case in (out/'evaluations').iterdir():
    if case.name not in ('P01','P02'):shutil.rmtree(case);continue
    for file in case.iterdir():
     if file.name not in ('pass-1.json','pass-1.sha256'):file.unlink()
   for file in (out/'prompts').glob('*'):file.unlink()
   finish.freeze(out);calls=[]
   def fake_http(payload,key,timeout,target):
    calls.append(1);r=response(payload)
    (target/'response.body').write_text(json.dumps(r))
    finish.old.save(target/'http.json',{'http_status':200,'body_complete':True})
    return r
   def fake_codex(out,cell):
    path=out/'attempts'/'codex-P01-vietnamizer_jev';path.mkdir(parents=True)
    text='Tôi về.';raw=json.dumps({'type':'item.completed','item':{'type':'agent_message','text':json.dumps({'text':text})}})+'\n'+json.dumps({'type':'turn.completed','usage':{}})
    (path/'stdout.txt').write_text(raw)
    r={'cell':cell,'status':'completed','text':text,'exit_code':0,'seconds':0,
      'manifest_digest':finish.base.digest(finish.old.read(out/'manifest.json')),
      'prompt_digest':finish.base.digest((out/'prompts/P01-vietnamizer_jev.txt').read_bytes()),
      'stdout_digest':finish.base.digest(raw.encode())}
    finish.old.save(path/'result.json',r);return r
   with patch.dict('os.environ',{'TYPESAFE_API_KEY':'offline-test'}),patch.object(finish.rec.capture,'request',side_effect=fake_http),patch.object(finish.base,'run_one',side_effect=fake_codex):
    finish.complete(out,'P01');r=finish.report(out)
    count=len(calls);finish.complete(out,'P01');self.assertEqual(len(calls),count)
   self.assertEqual(r['answered_jev_cases'],1)
   self.assertEqual(r['completed'],1)
   self.assertEqual(count,2)
   self.assertEqual(len(finish.old.read(out/'finish-blinded-review.json')),61)

if __name__=='__main__':unittest.main()
