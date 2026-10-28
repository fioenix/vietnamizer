"""Offline contracts for the paid fourth-arm extension; no real credentials/network."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tests.test_jev import response
from jev import core
from jev.transport import ServiceError
from benchmarks import jev_pilot as pilot


class ExtensionTest(unittest.TestCase):
    def test_budget_reserves_before_io_and_survives_failure_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)
            def failed(payload, key, timeout):
                self.assertEqual(json.loads(next(path.glob('*.json')).read_text())['status'],'reserved')
                raise ServiceError('service_failed')
            budget=pilot.Budget(path,transport=failed,cap=pilot.RESERVE)
            with self.assertRaises(ServiceError): budget.send('P01',{'model':core.MODEL,'questions':{}},'fake',1)
            again=pilot.Budget(path,transport=lambda *_:self.fail('sent beyond cap'),cap=pilot.RESERVE)
            with self.assertRaises(ServiceError): again.send('P02',{'model':core.MODEL,'questions':{}},'fake',1)
            self.assertEqual(again.summary()['reserved_or_actual_usd'],str(pilot.RESERVE))

    def test_validated_usage_releases_reserve_wrong_model_does_not(self):
        payload={'model':core.MODEL,'questions':{'x':{'type':'noul'}}}
        with tempfile.TemporaryDirectory() as tmp:
            b=pilot.Budget(Path(tmp),transport=lambda p,*_:response(p))
            b.send('P01',payload,'fake',1)
            self.assertEqual(b.summary()['input_tokens'],12)
            bad=response(payload);bad['model']='other'
            b.transport=lambda *_:bad
            with self.assertRaises(ServiceError):b.send('P01',payload,'fake',1)
            self.assertEqual(b.summary()['unknown_billing_requests'],1)
            self.assertEqual(b.summary()['requests'],2)

    def test_request_count_cap_and_model_rejected_before_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            b=pilot.Budget(Path(tmp),transport=lambda p,*_:response(p))
            for _ in range(32): b.send('P01',{'model':core.MODEL,'questions':{}},'fake',1)
            with self.assertRaises(ServiceError): b.send('P01',{'model':core.MODEL,'questions':{}},'fake',1)
            with self.assertRaises(ServiceError): b.send('P02',{'model':'other','questions':{}},'fake',1)
            self.assertEqual(b.summary()['requests'],32)

    def test_candidate_mapping_protects_quote_and_inline_code(self):
        case={'id':'P20','family':'huong-dan-ky-thuat','audience':'Maintainer','purpose':'Instructions',
              'source':'## Hướng dẫn\n\nTao thử cách này. Giữ `field_id`.\n\n> Đã thử mà vẫn không tìm nguyên nhân.'}
        draft=case['source'].replace('Tao thử','Tao đã thử')
        doc,omitted=pilot.make_document(case,draft)
        self.assertTrue(doc['context_review']['reviewed'])
        p=core.prepare(doc)
        self.assertNotEqual(p['status'],'invalid_input')
        calls=[]
        def fake(payload,*_):calls.append(payload);return response(payload)
        r=core.evaluate(doc,environ={'TYPESAFE_API_KEY':'fake'},transport=fake)
        self.assertTrue(r['candidate_reviews'])
        self.assertNotIn('field_id',json.dumps(calls,ensure_ascii=False))
        self.assertNotIn('Đã thử mà vẫn không tìm nguyên nhân',json.dumps(calls,ensure_ascii=False))
        self.assertEqual(omitted,[])

    def test_cross_parent_changes_are_explicit_not_silently_reviewed(self):
        case={'id':'P01','family':'ke-trai-nghiem','source':'Tôi về.\n\nBạn ở lại.', 'audience':'Bạn','purpose':'Kể'}
        doc,omitted=pilot.make_document(case,'Tôi về cùng bạn.')
        self.assertTrue(omitted)
        self.assertNotEqual(core.prepare(doc)['status'],'invalid_input')

    def test_matched_prompt_and_advice_is_data(self):
        source={'source':'Tôi về.','audience':'Bạn','purpose':'Kể'}
        prefix='FROZEN RULES\n'
        a=pilot.revision_prompt(prefix,source,'Tôi về.',None)
        b=pilot.revision_prompt(prefix,source,'Tôi về.',{'status':'incomplete','judgments':[]})
        self.assertEqual(a.split('<revision_input>')[0],b.split('<revision_input>')[0])
        self.assertIn('never automatically accept',b)
        self.assertIn('incomplete',b)

    def test_evaluation_seal_and_request_reconciliation_reject_tampering(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);payload={'model':core.MODEL,'questions':{'x':{'type':'noul'}}}
            b=pilot.Budget(out/'requests',transport=lambda p,*_:response(p))
            b.send('P01',payload,'fake',1)
            ledger=b.entries()[0]
            result={'manifest_digest':'m','input_digest':'i','receipts':[{
                'status':'validated','request_digest':core.digest(payload),
                'response_digest':ledger['response_digest'],'model_actual':core.MODEL,
                'usage':{'input_tokens':12,'output_tokens':4}}],
                'judgments':[{'request_digest':core.digest(payload),'check':'x','answer':{'type':'noul','noul':.1}}]}
            target=out/'evaluations/P01';pilot.save(target/'result.json',result)
            pilot.save(target/'seal.json',{'result_digest':pilot.base.digest(result)})
            self.assertEqual(len(pilot.verified_checks(out,'P01',result)),1)
            result['judgments'][0]['answer']['noul']=.9
            pilot.save(target/'seal.json',{'result_digest':pilot.base.digest(result)})
            with self.assertRaises(ValueError):pilot.verified_checks(out,'P01',result)

    def test_prompt_advice_contains_exact_question_semantics_and_target_mapping(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);q={'type':'noul','instructions':'Does this edit change meaning?'}
            payload={'model':core.MODEL,'state':{'candidate':{'id':'e1','replacement':'Tôi đã về.'}},'questions':{'edit_e1_meaning':q}}
            b=pilot.Budget(out/'requests',transport=lambda p,*_:response(p));b.send('P01',payload,'fake',1)
            ledger=b.entries()[0]
            result={'status':'incomplete','judgments':[],'candidate_reviews':[], 'receipts':[{
                'status':'validated','request_digest':core.digest(payload),'response_digest':ledger['response_digest'],
                'model_actual':core.MODEL,'usage':{'input_tokens':12,'output_tokens':4}}]}
            pilot.save(out/'evaluations/P01/seal.json',{'result_digest':pilot.base.digest(result)})
            advice=pilot.advice_for(result,[],pilot.verified_checks(out,'P01',result))
            ref=advice['checks'][0]['questions']['edit_e1_meaning']
            self.assertEqual(advice['question_templates'][ref['template']],q)
            self.assertEqual(advice['states'][advice['checks'][0]['state']]['candidate']['id'],'e1')

    def test_compact_advice_is_lossless_for_question_semantics(self):
        checks=[]
        for i in range(12):
            ident='s_'+format(i,'024x')
            checks.append({'state':{'targets':[{'id':ident,'text':'Tôi về.'}]},
                'questions':{'q_'+ident:{'type':'noul','instructions':'Check target '+ident+' for changed meaning.'}},
                'answers':{'q_'+ident:{'type':'noul','noul':.2}}})
        result={'status':'evaluated','judgments':[],'candidate_reviews':[]}
        advice=pilot.advice_for(result,[],checks)
        self.assertEqual(len(advice['question_templates']),1)
        for original,compact in zip(checks,advice['checks']):
            self.assertEqual(advice['states'][compact['state']],original['state'])
            for name,ref in compact['questions'].items():
                serialized=json.dumps(advice['question_templates'][ref['template']],ensure_ascii=False)
                for placeholder,value in ref['variables'].items():serialized=serialized.replace(placeholder,value)
                self.assertEqual(json.loads(serialized),original['questions'][name])
            self.assertEqual(compact['answers'],original['answers'])

    def test_parent_baseline_changes_invalidate_epoch(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'epoch';parent=Path(tmp)/'parent';out.mkdir();parent.mkdir()
            pilot.save(parent/'manifest.json',{'frozen':True})
            pilot.save(out/'frozen-corpus.json',{});pilot.save(out/'candidate-omissions.json',{})
            original={'cell':'codex/P01/bare','text':'Tôi về.'}
            manifest={'source_fingerprints':pilot.source_fingerprints(), 'corpus_digest':pilot.base.digest({}),
                'omissions_digest':pilot.base.digest({}),'parent':str(parent),
                'parent_manifest_digest':pilot.base.digest({'frozen':True}), 'bindings':{},'max_codex_attempts':40,
                'parent_codex_records':{original['cell']:pilot.base.digest(original)}}
            pilot.save(out/'manifest.json',manifest)
            with patch.object(pilot.base,'report'),patch.object(pilot.base,'records',return_value=[original]):
                pilot.validate_epoch(out)
            changed=dict(original,text='Tôi đã về.')
            with patch.object(pilot.base,'report'),patch.object(pilot.base,'records',return_value=[changed]):
                with self.assertRaisesRegex(ValueError,'parent attempt drift'):pilot.validate_epoch(out)
            pilot.save(parent/'manifest.json',{'frozen':False})
            with patch.object(pilot.base,'report'):
                with self.assertRaisesRegex(ValueError,'parent manifest drift'):pilot.validate_epoch(out)

    def test_all_frozen_case_advice_prompts_fit_before_paid_inference(self):
        parent=pilot.ROOT/'artifacts/014-editorial-pilot-20261025'
        if not (parent/'manifest.json').exists():self.skipTest('local historical artifacts unavailable')
        for case in pilot.read(parent/'frozen-corpus.json')['cases']:
            with self.subTest(case=case['id']):
                draft=(parent/'outputs/codex'/case['id']/'vietnamizer.md').read_text().rstrip('\n')
                doc,omitted=pilot.make_document(case,draft);checks=[]
                def fake(payload,*_):
                    reply=response(payload)
                    checks.append({'state':payload['state'],'questions':payload['questions'],'answers':reply['answers']})
                    return reply
                result=core.evaluate(doc,environ={'TYPESAFE_API_KEY':'offline-only'},transport=fake)
                prefix=(parent/'prompts'/f'{case["id"]}-vietnamizer.txt').read_text().split('<editing_input>')[0]
                advice=pilot.advice_for(result,omitted,checks)
                self.assertLess(len(pilot.revision_prompt(prefix,case,draft,advice).encode()),1000000)
                self.assertEqual(omitted,[])

    def test_core_input_binding_uses_its_own_encoding(self):
        doc={'z':1,'a':2};m={'bindings':{'P01':{'input_digest':pilot.base.digest(doc)}}}
        self.assertNotEqual(core.digest(doc),pilot.base.digest(doc))
        result={'input_digest':core.digest(doc),'manifest_digest':pilot.base.digest(m)}
        pilot.verify_binding(m,'P01',doc,result)
        with self.assertRaises(ValueError):pilot.verify_binding(m,'P01',{'z':2,'a':2},result)

    def test_partial_failure_preserves_valid_advice_and_failed_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);payload={'model':core.MODEL,'state':{},'questions':{'x':{'type':'noul'}}}
            b=pilot.Budget(out/'requests',transport=lambda p,*_:response(p))
            b.send('P01',payload,'fake',1);row=b.entries()[0]
            b.transport=lambda *_:(_ for _ in ()).throw(ServiceError('service_failed'))
            with self.assertRaises(ServiceError):b.send('P01',dict(payload,state={'next':True}),'fake',1)
            rows=b.entries();result={'status':'incomplete','judgments':[],'candidate_reviews':[], 'receipts':[
                {'status':'validated','request_digest':row['request_digest'],'response_digest':row['response_digest'],
                 'model_actual':core.MODEL,'usage':{'input_tokens':12,'output_tokens':4}},
                {'status':'service_failed','request_digest':rows[1]['request_digest']}]}
            pilot.save(out/'evaluations/P01/seal.json',{'result_digest':pilot.base.digest(result)})
            checks=pilot.verified_checks(out,'P01',result)
            self.assertEqual(len(checks),1)
            self.assertEqual(pilot.treatment_status(result),'partial')
            self.assertEqual(pilot.treatment_status({'status':'incomplete','receipts':[]}), 'unavailable')
            self.assertEqual(pilot.treatment_status({'status':'not_attempted','receipts':[]}), 'not_attempted')

    def test_inherited_partial_and_unavailable_end_to_end_without_new_network(self):
        parent=pilot.ROOT/'artifacts/014-editorial-pilot-20261025'
        prior=pilot.ROOT/'artifacts/014-codex-jev-20261025'
        if not (prior/'manifest.json').exists():self.skipTest('local historical artifacts unavailable')
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'v2';pilot.prepare(out,parent,prior)
            budget_before=pilot.Budget(out/'requests').summary()
            def fake_codex(out,cell):
                rt,cid,arm=cell.split('/');text='Tôi về.'
                raw=json.dumps({'type':'item.completed','item':{'type':'agent_message','text':json.dumps({'text':text})}})+'\n'+json.dumps({'type':'turn.completed','usage':{}})
                path=out/'attempts'/f'{rt}-{cid}-{arm}';path.mkdir(parents=True)
                (path/'stdout.txt').write_text(raw)
                row={'cell':cell,'status':'completed','text':text,'seconds':0,'exit_code':0,
                    'manifest_digest':pilot.base.digest(pilot.read(out/'manifest.json')),
                    'prompt_digest':pilot.base.digest((out/'prompts'/f'{cid}-{arm}.txt').read_bytes()),
                    'stdout_digest':pilot.base.digest(raw.encode())}
                pilot.save(path/'result.json',row);return row
            with patch.object(core,'evaluate',side_effect=AssertionError('inherited evaluation retried')),patch.object(pilot.base,'run_one',side_effect=fake_codex):
                pilot.run_case(out,'P01');pilot.run_case(out,'P02')
                report=pilot.report(out)
                pilot.run_case(out,'P01')  # Completed cells skip; no generation or paid retry.
            self.assertEqual(report['completed'],4)
            self.assertEqual(report['jev_treatment_counts']['partial'],1)
            self.assertEqual(report['jev_treatment_counts']['unavailable'],1)
            self.assertEqual(pilot.Budget(out/'requests').summary(),budget_before)
            for cid in ('P01','P02'):
                self.assertEqual((out/'evaluations'/cid/'result.json').read_bytes(),(prior/'evaluations'/cid/'result.json').read_bytes())

    def test_circuit_stops_new_jev_after_three_failed_cases(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            for cid in ('P01','P02','P03'):
                pilot.save(out/'evaluations'/cid/'result.json',{'receipts':[{'status':'service_failed'}]})
            doc={'z':1,'a':2};pilot.save(out/'inputs.json',{'P04':doc})
            with patch.object(core,'key_available',return_value=True),patch.object(pilot,'validate_epoch',return_value={}),patch.object(core,'evaluate',side_effect=AssertionError('circuit dispatched network')):
                result=pilot.evaluate_case(out,'P04')
            self.assertEqual(result['status'],'not_attempted_service_stop')
            self.assertEqual(result['receipts'],[])
            self.assertEqual(result['input_digest'],core.digest(doc))
            self.assertFalse((out/'requests').exists())

    def test_single_writer_and_started_evaluation_are_not_retried(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            with pilot.writer(out):
                with self.assertRaises(FileExistsError):
                    with pilot.writer(out):pass
            (out/'evaluations/P01').mkdir(parents=True)
            (out/'evaluations/P01/result.json').write_text('{"status":"started"}')
            with patch.object(core,'evaluate',side_effect=AssertionError('retry')):
                with self.assertRaises(ValueError): pilot.evaluate_case(out,'P01')

if __name__=='__main__':unittest.main()
