import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { guardedCapture, checkInit } from '../benchmarks/gemini_text_guard.mjs';
const agent='vietnamizer-benchmark-text-only',model='gemini-3.8-flash-medium';
const event={event:'init',init:{agent,model,tools:['finish'],permission_mode:'request-review'}};
test('init requires exact agent/model and no executable tools',()=>{
  assert.equal(checkInit(event,agent,model),true);
  for(const patch of [{agent:'default'},{model:'other'},{tools:['finish','read_file']},{tools:undefined},{permission_mode:'always-proceed'}])assert.throws(()=>checkInit({...event,init:{...event.init,...patch}},agent,model));
});
test('registry requires verified paired-capability contract, not agent-name alone',()=>{
  const expanded={...event,init:{...event.init,tools:['finish','view_file','run_command']}};
  assert.throws(()=>checkInit(expanded,agent,model));
  const contract={schema:'verified-registry-v1',agent,model,effective_agent_tools:['finish'],advertised_registry:expanded.init.tools};
  assert.equal(checkInit(expanded,agent,model,contract),true);
  assert.throws(()=>checkInit({...expanded,init:{...expanded.init,tools:[...expanded.init.tools,'extra']}},agent,model,contract));
  assert.throws(()=>checkInit(expanded,agent,model,{...contract,effective_agent_tools:['read_file']}));
});
test('guard retains bytes and rejects default agent immediately',async()=>{
  const base=fs.mkdtempSync(path.join(os.tmpdir(),'vietnamizer-guard-')),cwd=path.join(base,'work');fs.mkdirSync(cwd);
  const dir=path.join(base,'raw');
  const fake={...event,init:{...event.init,tools:['run_command']}};
  const r=await guardedCapture(process.execPath,['-e',`process.stdout.write(${JSON.stringify(JSON.stringify(fake)+'\n')});setInterval(()=>{},1000)`],{dir,cwd,agent,model,timeoutMs:3000});
  assert.equal(r.guard_ok,false);assert.match(r.guard_error,/tools/);
  assert.ok(fs.readFileSync(path.join(dir,'stdout.bin')).includes(Buffer.from('run_command')));
});
test('valid stream preserves split UTF8 and stderr, native raw cannot be in cwd',async()=>{
  const base=fs.mkdtempSync(path.join(os.tmpdir(),'vietnamizer-guard-')),cwd=path.join(base,'work');fs.mkdirSync(cwd);
  const dir=path.join(base,'raw');const text=JSON.stringify(event)+'\n';
  const r=await guardedCapture(process.execPath,['-e',`process.stdout.write(${JSON.stringify(text)});process.stderr.write(Buffer.from([255]));`],{dir,cwd,agent,model,timeoutMs:3000});
  assert.equal(r.guard_ok,true);assert.equal(fs.readFileSync(path.join(dir,'stdout.bin'),'utf8'),text);
  assert.deepEqual(fs.readFileSync(path.join(dir,'stderr.bin')),Buffer.from([255]));
  await assert.rejects(()=>guardedCapture(process.execPath,[],{dir:path.join(cwd,'raw'),cwd,agent,model,timeoutMs:1000}));
});
test('guard immediately rejects alternate native tool and subagent event shapes',async()=>{
  const activities=[{event:'step_update',step:{type:'tool',name:'run_command'}},
    {event:'step_update',step_update:{toolName:'read_file'}},
    {event:'step_update',step_update:{tool_info:{name:'read_file'}}},
    {event:'tool_call',name:'run_command'},
    {event:'step_update',subagents:[{id:'x'}]}];
  for(const activity of activities){
    const base=fs.mkdtempSync(path.join(os.tmpdir(),'vietnamizer-shape-')),cwd=path.join(base,'work');fs.mkdirSync(cwd);
    const stream=JSON.stringify(event)+'\n'+JSON.stringify(activity)+'\n';
    const r=await guardedCapture(process.execPath,['-e',`process.stdout.write(${JSON.stringify(stream)});setTimeout(()=>{},100)`],{dir:path.join(base,'raw'),cwd,agent,model,timeoutMs:1500});
    assert.equal(r.guard_ok,false,JSON.stringify(activity));
  }
});
