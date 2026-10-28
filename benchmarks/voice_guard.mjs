// Task-local native Gemini guard; registry advertising is not capability proof.
import fs from 'node:fs';
import path from 'node:path';
import {spawn,spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {StringDecoder} from 'node:string_decoder';
import {fileURLToPath} from 'node:url';
import {validatePrintArgs} from './gemini_boundary.mjs';
export function checkInit(e,agent,model){
  const x=e.init;
  if((e.event||e.type)!=='init'||!x||x.agent!==agent||x.model!==model||!Array.isArray(x.tools)||x.permission_mode!=='request-review')throw Error('native_init_mismatch');
}
export function checkActivity(v){
  if(!v||typeof v!=='object')return;
  if(Array.isArray(v)){v.forEach(checkActivity);return;}
  if(v.subagents?.length||v.denied_actions?.length)throw Error('denied_or_subagent');
  const kind=String(v.step_type||v.event||v.type||'').toLowerCase();
  const name=v.tool_name||v.toolName||v.tool_info?.name||(kind.includes('tool')?v.name||'unknown':null);
  if((name&&name!=='finish')||kind.includes('subagent')||kind==='error')throw Error('operational_activity');
  Object.values(v).forEach(checkActivity);
}
export async function capture(command,args,{dir,cwd,agent,model,timeoutMs}){
  dir=path.resolve(dir);cwd=path.resolve(cwd);const rel=path.relative(cwd,dir);
  if(!rel||(!rel.startsWith('..'+path.sep)&&rel!=='..'&&!path.isAbsolute(rel)))throw Error('raw_inside_workspace');
  fs.mkdirSync(dir,{recursive:true});
  const save=(n,v)=>fs.writeFileSync(path.join(dir,n),JSON.stringify(v,null,2)+'\n',{flag:'wx'});
  save('start.json',{command,args,cwd,agent,model,timeoutMs,at:new Date().toISOString()});
  const out=fs.openSync(path.join(dir,'stdout.bin'),'wx'),err=fs.openSync(path.join(dir,'stderr.bin'),'wx');
  const child=spawn(command,args,{cwd,shell:false,stdio:['ignore','pipe','pipe']});
  let buffer='',seen=false,guardError=null,timedOut=false,spawnError=null,killTimer;const decoder=new StringDecoder('utf8');
  const stop=()=>{child.kill('SIGTERM');killTimer??=setTimeout(()=>child.kill('SIGKILL'),1500);};
  const line=s=>{if(!s.trim()||guardError)return;try{const e=JSON.parse(s);if(!seen){checkInit(e,agent,model);seen=true;save('init.json',e);}else if((e.event||e.type)==='init')throw Error('duplicate_init');checkActivity(e);}catch(e){guardError=e.message;stop();}};
  child.stdout.on('data',b=>{fs.writeSync(out,b);buffer+=decoder.write(b);let i;while((i=buffer.indexOf('\n'))>=0){line(buffer.slice(0,i));buffer=buffer.slice(i+1);}});
  child.stderr.on('data',b=>fs.writeSync(err,b));child.on('error',e=>{spawnError=e.code;});
  const cancel=()=>{guardError??='interrupted';stop();};process.on('SIGTERM',cancel);process.on('SIGINT',cancel);
  const timer=setTimeout(()=>{timedOut=true;stop();},timeoutMs);
  return await new Promise(resolve=>child.on('close',(exitCode,signal)=>{
    clearTimeout(timer);clearTimeout(killTimer);buffer+=decoder.end();if(buffer.trim())line(buffer);clearTimeout(killTimer);
    process.off('SIGTERM',cancel);process.off('SIGINT',cancel);fs.fsyncSync(out);fs.fsyncSync(err);fs.closeSync(out);fs.closeSync(err);
    const r={exitCode,signal,timedOut,spawnError,guard_ok:seen&&!guardError,guard_error:guardError,
      streams:Object.fromEntries(['stdout.bin','stderr.bin'].map(n=>{const b=fs.readFileSync(path.join(dir,n));return[n,{bytes:b.length,sha256:createHash('sha256').update(b).digest('hex')}];}))};
    save('finish.json',r);resolve(r);
  }));
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  const binary='__AGY_BINARY__',agent='voice-pilot-judge',model='gemini-3.8-flash-medium',args=process.argv.slice(2);
  if(args.length===1&&args[0]==='--version'){const r=spawnSync(binary,args,{stdio:'inherit',timeout:5000});process.exit(r.status??1);}
  const i=args.indexOf('--agent');if(i<0||args[i+1]!==agent||args.lastIndexOf('--agent')!==i)throw Error('judge_agent_required');
  const timeoutMs=validatePrintArgs([...args.slice(0,i),...args.slice(i+2)])+1000;
  const dir=process.env.VIETNAMIZER_RAW_DIR;const r=await capture(binary,args,{dir,cwd:process.cwd(),agent,model,timeoutMs});
  process.stdout.write(fs.readFileSync(path.join(dir,'stdout.bin')));process.stderr.write(fs.readFileSync(path.join(dir,'stderr.bin')));process.exitCode=r.guard_ok?(r.exitCode??1):2;
}
