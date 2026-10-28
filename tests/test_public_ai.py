import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
class PublicAITest(unittest.TestCase):
 def api(self):
  try:from benchmarks import public_ai as m
  except ImportError:self.fail('public AI runner missing')
  return m
 def row(self):return {'id':'VVSFT-00000005','language':'vi','domain':'education','source_type':'synthetic_llm','is_multi_turn':False,'has_code':False,'messages':[{'role':'user','content':'Giải thích giúp mình.'},{'role':'assistant','content':' '.join(['Tiếng Việt tự nhiên.']*50)}],'pipeline_trace':{'output_generation':{'prompt_template':'source-template'}}}
 def test_source_selection_is_whole_exact_assistant_text(self):
  m=self.api();r=self.row();cases,ledger=m.select_sources([r],count=1)
  self.assertEqual(cases[0]['source'],r['messages'][1]['content']);self.assertEqual(cases[0]['provenance']['original_id'],r['id']);self.assertEqual(cases[0]['provenance']['generator_model'],None);self.assertTrue(ledger[0]['selected'])
 def test_selection_rejects_non_ai_multiturn_duplicate_and_scope(self):
  m=self.api();r=self.row()
  for key,value in [('source_type','human'),('is_multi_turn',True),('has_code',True),('domain','healthcare')]:
   bad={**r,key:value}
   with self.assertRaises(ValueError):m.select_sources([bad],count=1)
  with self.assertRaises(ValueError):m.select_sources([r,copy.deepcopy(r)],count=2)
 def test_prompts_have_equal_one_call_design_and_no_upstream_grades(self):
  m=self.api();c=m.select_sources([self.row()],1)[0][0]
  for arm in m.ARMS:
   prompt=m.prompt_for(c,arm,'RULES',{'status':'complete','checks':[]} if arm=='vietnamizer_jev' else None)
   self.assertIn(c['source'],prompt);self.assertNotIn('initial_draft',prompt);self.assertNotIn('quality_score',prompt)
  self.assertNotIn('RULES',m.prompt_for(c,'ordinary','RULES',None));self.assertIn('RULES',m.prompt_for(c,'vietnamizer','RULES',None))
 def test_budget_reserves_cumulatively_before_transport(self):
  m=self.api()
  with tempfile.TemporaryDirectory() as t:
   b=m.PublicBudget(Path(t),prior='1.999',cap='2')
   with patch.object(m.capture,'request') as request:
    with self.assertRaises(Exception):b.send('R001',{'model':m.core.MODEL},'not-a-real-key',1)
    request.assert_not_called()
 def test_missing_billing_keeps_reservation(self):
  m=self.api()
  with tempfile.TemporaryDirectory() as t:
   b=m.PublicBudget(Path(t),prior='0.2',cap='2');m.old.save(Path(t)/'requests/0001/record.json',{'status':'reserved','case':'R001'})
   self.assertEqual(b.summary()['reserved_or_actual_usd'],str(m.Decimal('0.2')+m.old.RESERVE))
 def test_resume_stop_marker_blocks_even_cached_terminal_result(self):
  m=self.api()
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);m.old.save(p/'inputs.json',{'R001':{}});m.old.save(p/'evaluations/R001/result.json',{'status':'service_failed','input_digest':m.base.digest({}),'manifest_digest':m.base.digest({})});(p/'STOP_PAID').write_text('stop')
   with patch.object(m,'verify',return_value={}):
    with self.assertRaisesRegex(ValueError,'stopped'):m.evaluate(p,'R001')
 def test_orphan_advice_record_is_rejected_before_interpretation(self):
  m=self.api()
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);m.old.save(p/'requests/0001/record.json',{'case':'R001','status':'validated'});r={'receipts':[],'judgments':[]};m.old.save(p/'evaluations/R001/seal.json',{'result_digest':m.base.digest(r)})
   with self.assertRaisesRegex(ValueError,'receipt'):m.get_advice(p,'R001',r)
 def test_raw_body_disagreement_and_judgment_changes_are_rejected(self):
  m=self.api()
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);d=p/'requests/0001';payload={'model':m.core.MODEL,'state':'Một đoạn văn.','questions':{'q':{'type':'noul','instructions':'Có lỗi không?'}}};reply={'model':m.core.MODEL,'answers':{'q':{'type':'noul','noul':0.2}},'usage':{'input_tokens':10,'output_tokens':3}};clean,usage=m.core.validate_response(payload,reply)
   record={'case':'R001','status':'validated','request_digest':m.core.digest(payload),'response_digest':m.core.digest(reply),'input_tokens':10,'output_tokens':3};receipt={'status':'validated','request_digest':record['request_digest'],'response_digest':record['response_digest'],'usage':usage,'model_actual':m.core.MODEL};r={'status':'complete','candidate_reviews':[],'receipts':[receipt],'judgments':[{'request_digest':record['request_digest'],'check':'q','answer':clean['q']}]}
   for name,value in [('record.json',record),('request.json',payload),('response.json',reply)]:m.old.save(d/name,value)
   (d/'request.body').write_bytes(m.core.encoded(payload));body=m.core.encoded(reply);(d/'response.body').write_bytes(body);http={'http_status':200,'body_complete':True,'stored_body_digest':m.base.digest(body),'credential_redacted':False};m.old.save(d/'http.json',http);seal=p/'evaluations/R001/seal.json';m.old.save(seal,{'result_digest':m.base.digest(r)})
   self.assertEqual(len(m.get_advice(p,'R001',r)['checks']),1)
   altered={**reply,'answers':{'q':{'type':'noul','noul':0.3}}};body=m.core.encoded(altered);(d/'response.body').write_bytes(body);m.old.save(d/'http.json',{**http,'stored_body_digest':m.base.digest(body)})
   with self.assertRaisesRegex(ValueError,'raw advice'):m.get_advice(p,'R001',r)
   (d/'response.body').write_bytes(m.core.encoded(reply));m.old.save(d/'http.json',http);r['judgments'][0]['answer']={'type':'noul','noul':0.9};m.old.save(seal,{'result_digest':m.base.digest(r)})
   with self.assertRaisesRegex(ValueError,'judgment'):m.get_advice(p,'R001',r)
 def test_source_verification_rejects_corruption(self):
  m=self.api()
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);f=p/'frozen-corpus.json';m.old.save(f,{'cases':[]});m.old.save(p/'manifest.json',{'corpus_digest':'wrong','fingerprints':{}})
   with self.assertRaises(ValueError):m.verify(p)
if __name__=='__main__':unittest.main()
