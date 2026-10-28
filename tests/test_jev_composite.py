import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from benchmarks import jev_composite as c
from tests.test_jev import response

class CompositeTest(unittest.TestCase):
 def payload(self):return {'model':c.core.MODEL,'state':{'text':'Một câu nguyên vẹn.'},'questions':{'good':{'type':'noul'},'bad':{'type':'score','criteria':['a','b','c','d']}}}
 def test_split_keeps_valid_answers_without_resampling(self):
  p=self.payload();r=response(p);r['answers']['bad'].update(score=.51,probabilities={'0':.6,'1':.32,'2':.08,'3':0})
  self.assertEqual(c.split_answers(p,r),(['good'],['bad']))
 def test_choice_inconsistency_and_bad_envelope(self):
  p={'model':c.core.MODEL,'questions':{'q':{'type':'choice','criteria':{'a':'x','b':'y'}}}}
  r=response(p);r['answers']['q'].update(choice='a',probabilities={'a':.4,'b':.6})
  self.assertEqual(c.split_answers(p,r),([],['q']))
  r['model']='other'
  with self.assertRaises(ValueError):c.split_answers(p,r)
 def test_no_repair_of_valid_or_unsupported_answers(self):
  p=self.payload();r=response(p)
  with self.assertRaises(ValueError):c.split_answers(p,r)
  r['answers']['good']['noul']=2
  with self.assertRaises(ValueError):c.split_answers(p,r)
 def test_composite_retains_valid_answers_and_exact_provenance(self):
  with tempfile.TemporaryDirectory() as t:
   out=Path(t);p=self.payload();r=response(p);r['answers']['bad'].update(score=.51,probabilities={'0':.6,'1':.32,'2':.08,'3':0})
   def write_source(ident,payload,reply,status):
    folder=out/'requests'/ident;folder.mkdir(parents=True)
    raw=json.dumps(reply).encode();(folder/'response.body').write_bytes(raw)
    c.old.save(folder/'request.json',payload);(folder/'request.body').write_bytes(c.core.encoded(payload));c.old.save(folder/'response.json',reply)
    c.old.save(folder/'http.json',{'http_status':200,'body_complete':True,'stored_body_digest':c.base.digest(raw)})
    rec={'case':'P05','status':status,'request_digest':c.core.digest(payload),'actual_usd':'0.000000504','input_tokens':12,'output_tokens':4,'diagnostic':{'reason':'score_distribution'}}
    c.old.save(folder/'record.json',rec)
   write_source('0001',p,r,'invalid_response');c.old.save(out/'composite-manifest.json',{'fake':'offline'})
   original_record=c.old.read(out/'requests/0001/record.json')
   c.old.save(out/'requests/0001/record.json',{**original_record,'input_tokens':0,'output_tokens':0,'actual_usd':'0'})
   with self.assertRaises(ValueError):c.source(out,'requests/0001/record.json')
   c.old.save(out/'requests/0001/record.json',original_record)
   calls=[]
   def fake_send(store,cid,payload,key,timeout):
    calls.append(payload);a=response(payload);write_source('0002',payload,a,'validated');return a
   with patch.object(c,'verify_amendment',return_value={'fake':'offline'}),patch.object(c.rec,'validate',return_value=({},out/'prior')),patch.object(c.CompositeStore,'send',new=fake_send),patch.dict('os.environ',{'TYPESAFE_API_KEY':'offline'}):
    record,_,answer=c.repair(out,'P05','0001')
    self.assertEqual(list(calls[0]['questions']),['bad']);self.assertEqual(calls[0]['state'],p['state'])
    self.assertEqual(answer['answers']['good'],r['answers']['good'])
    self.assertEqual(record['kind'],'composite_evidence')
    self.assertEqual(answer['usage']['input_tokens'],24)
    c.repair(out,'P05','0001');self.assertEqual(len(calls),1)
    folder=out/'composites'/'P05'/c.core.digest(p)
    a=c.old.read(folder/'response.json');a['answers']['good']['noul']=.9;c.old.save(folder/'response.json',a)
    with self.assertRaises(ValueError):c.validate_composite(out,folder)

 def test_live_failure_recovery_and_full_evidence_offline(self):
  import shutil
  live=c.ROOT/'artifacts/014-jev-recovery-20261025'
  if not (live/'requests/0092/record.json').exists():self.skipTest('local failure fixture unavailable')
  with tempfile.TemporaryDirectory() as t:
   out=Path(t)/'recovery';out.mkdir()
   for name in ('manifest.json','finish-manifest.json'):shutil.copyfile(live/name,out/name)
   for folder in ('requests','evaluations','prompts','attempts'):(out/folder).mkdir()
   for item in (live/'requests').iterdir():
    if item.name.isdigit() and int(item.name)<=154:shutil.copytree(item,out/'requests'/item.name)
   for item in (live/'evaluations').iterdir():
    if item.name in ('P01','P02','P03','P04','P05','P06','P07','P08','P09'):shutil.copytree(item,out/'evaluations'/item.name)
   for cid in ('P05','P07','P09'):
    for item in (out/'evaluations'/cid).iterdir():
     if item.name not in ('pass-1.json','pass-1.sha256'):item.unlink()
   for item in (live/'attempts').iterdir():
    if item.name in ('codex-P01-vietnamizer_jev','codex-P02-vietnamizer_jev','codex-P03-vietnamizer_jev','codex-P04-vietnamizer_jev','codex-P06-vietnamizer_jev','codex-P08-vietnamizer_jev'):shutil.copytree(item,out/'attempts'/item.name)
   for item in (live/'prompts').iterdir():shutil.copyfile(item,out/'prompts'/item.name)
   (out/'prompts/P05-vietnamizer_jev.txt').unlink(missing_ok=True)
   c.amendment(out);calls=[]
   _,payload,reply=c.source(out,'requests/0092/record.json')
   good,bad=c.split_answers(payload,reply);self.assertEqual((len(good),len(bad)),(39,1))
   def fake_http(payload,key,timeout,target):
    calls.append(payload);reply=response(payload);raw=json.dumps(reply).encode()
    (target/'request.body').write_bytes(c.core.encoded(payload))
    (target/'response.body').write_bytes(raw)
    c.old.save(target/'http.json',{'http_status':200,'body_complete':True,'stored_body_digest':c.base.digest(raw)})
    return reply
   def fake_codex(out,cell):
    path=out/'attempts'/'codex-P05-vietnamizer_jev';path.mkdir()
    text='Bản thử offline.';raw=json.dumps({'type':'item.completed','item':{'type':'agent_message','text':json.dumps({'text':text})}})+'\n'+json.dumps({'type':'turn.completed','usage':{}})
    (path/'stdout.txt').write_text(raw)
    r={'cell':cell,'status':'completed','text':text,'exit_code':0,'seconds':0,
     'manifest_digest':c.base.digest(c.old.read(out/'manifest.json')),'prompt_digest':c.base.digest((out/'prompts/P05-vietnamizer_jev.txt').read_bytes()),'stdout_digest':c.base.digest(raw.encode())}
    c.old.save(path/'result.json',r);return r
   with patch.dict('os.environ',{'TYPESAFE_API_KEY':'offline'}),patch.object(c.rec.capture,'request',side_effect=fake_http),patch.object(c.base,'run_one',side_effect=fake_codex),c.installed(out):
    c.repair(out,'P05','0092');self.assertEqual(len(calls[0]['questions']),1)
    result=c.rec.diagnostic(out,'P05',32);c.finish.require_answers(result)
    c.finish.complete(out,'P05');report=c.finish.report(out)
    self.assertEqual(report['answered_jev_cases'],7)
    c.finish.evidence(out,'P05',result)

if __name__=='__main__':unittest.main()
