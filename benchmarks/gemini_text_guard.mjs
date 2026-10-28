// Native stream guard for the owner-approved text-only agent; no TLS/auth access.
import fs from 'node:fs';
import path from 'node:path';
import {spawn,spawnSync} from 'node:child_process';
import {StringDecoder} from 'node:string_decoder';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {validatePrintArgs} from './gemini_boundary.mjs';
export function checkInit(e,agent,model,contract=null){
  if((e.event||e.type)!=='init')throw Error('missing_initial_init');
  const x=e.init;
  if(!x||x.agent!==agent)throw Error('wrong_agent');
  if(x.model!==model)throw Error('wrong_model');
  if(!Array.isArray(x.tools))throw Error('missing_tool_registry');
  if(contract){
    if(contract.schema!=='verified-registry-v1'||contract.agent!==agent||contract.model!==model||JSON.stringify(contract.effective_agent_tools)!=='["finish"]'||
       JSON.stringify([...x.tools].sort())!==JSON.stringify([...contract.advertised_registry].sort()))throw Error('unverified_registry');
  }else if(x.tools.some(t=>t!=='finish'))throw Error('unexpected_tools');
  if(x.permission_mode!=='request-review')throw Error('unexpected_permissions');
  return true;
}
export async function guardedCapture(command,args,{dir,cwd,agent,model,timeoutMs,contract=null}){
  dir=path.resolve(dir);cwd=path.resolve(cwd);
  const rel=path.relative(cwd,dir);
  if(!rel||(!rel.startsWith('..'+path.sep)&&rel!=='..'&&!path.isAbsolute(rel)))throw Error('raw_inside_workspace');
  fs.mkdirSync(dir,{recursive:true});
  const write=(n,v)=>fs.writeFileSync(path.join(dir,n),JSON.stringify(v,null,2)+'\n',{flag:'wx'});
  write('start.json',{command,args,cwd,agent,model,started_at:new Date().toISOString(),timeoutMs});
  const out=fs.openSync(path.join(dir,'stdout.bin'),'wx'),err=fs.openSync(path.join(dir,'stderr.bin'),'wx');
  const started=Date.now(),decoder=new StringDecoder('utf8');let buffer='',seen=false,guardError=null,timedOut=false,spawnError=null,cancelTimer;
  const child=spawn(command,args,{cwd,shell:false,stdio:['ignore','pipe','pipe'],detached:false});
  const kill=s=>{try{child.kill(s);}catch{}};
  const stop=()=>{kill('SIGTERM');cancelTimer??=setTimeout(()=>kill('SIGKILL'),2000);};
  const reject=reason=>{guardError??=reason;stop();};
  const line=s=>{
    if(!s.trim()||guardError)return;
    try{
      const e=JSON.parse(s);
      if(!seen){checkInit(e,agent,model,contract);seen=true;write('init.json',e);}
      else if((e.event||e.type)==='init')reject('duplicate_init');
      const scan=v=>{
        if(!v||typeof v!=='object')return;
        if(Array.isArray(v)){for(const x of v)scan(x);return;}
        if(v.subagents?.length||v.denied_actions?.length)reject('subagent_or_denied_activity');
        const kind=String(v.step_type||v.type||v.event||'');
        const name=v.tool_name||v.toolName||v.tool_info?.name||(kind.includes('tool')?v.name||'unknown':null);
        if(name&&name!=='finish')reject('unexpected_tool_call');
        if(kind.includes('subagent'))reject('unexpected_subagent');
        for(const x of Object.values(v))scan(x);
      };
      scan(e);
    }catch(e){reject(e instanceof SyntaxError?'malformed_stream':e.message);}
  };
  child.stdout.on('data',b=>{fs.writeSync(out,b);buffer+=decoder.write(b);let i;while((i=buffer.indexOf('\n'))>=0){line(buffer.slice(0,i));buffer=buffer.slice(i+1);}});
  child.stderr.on('data',b=>fs.writeSync(err,b));
  child.on('error',e=>{spawnError=e.code;});
  const cancel=()=>{guardError??='interrupted';stop();};process.on('SIGTERM',cancel);process.on('SIGINT',cancel);
  const timer=setTimeout(()=>{timedOut=true;stop();},timeoutMs);
  return await new Promise(resolve=>child.on('close',(exitCode,signal)=>{
    clearTimeout(timer);clearTimeout(cancelTimer);process.off('SIGTERM',cancel);process.off('SIGINT',cancel);
    buffer+=decoder.end();if(buffer.trim())line(buffer);
    if(!seen)guardError??='missing_init';
    // line() can request cancellation after EOF; no child remains at this point.
    clearTimeout(cancelTimer);fs.fsyncSync(out);fs.fsyncSync(err);fs.closeSync(out);fs.closeSync(err);
    const r={exitCode,signal,timedOut,spawnError,elapsed_ms:Date.now()-started,guard_ok:seen&&!guardError,guard_error:guardError,
      streams:Object.fromEntries(['stdout.bin','stderr.bin'].map(n=>{const b=fs.readFileSync(path.join(dir,n));return[n,{bytes:b.length,sha256:createHash('sha256').update(b).digest('hex')}];}))};
    write('finish.json',r);resolve(r);
  }));
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  const binary='/usr/local/bin/agy',agent='vietnamizer-benchmark-text-only',model='gemini-3.8-flash-medium',args=process.argv.slice(2);
  if(args.length===1&&args[0]==='--version'){const r=spawnSync(binary,args,{stdio:'inherit',timeout:5000});process.exit(r.status??1);}
  const ix=args.indexOf('--agent');
  if(ix<0||args[ix+1]!==agent||args.lastIndexOf('--agent')!==ix)throw Error('text_only_agent_required');
  const timeoutMs=validatePrintArgs([...args.slice(0,ix),...args.slice(ix+2)]);
  const contract=JSON.parse(fs.readFileSync(new URL('./capability-contract.json',import.meta.url),'utf8'));
  const r=await guardedCapture(binary,args,{dir:process.env.VIETNAMIZER_RAW_DIR,cwd:process.cwd(),agent,model,timeoutMs:timeoutMs+1000,contract});
  process.stdout.write(fs.readFileSync(path.join(process.env.VIETNAMIZER_RAW_DIR,'stdout.bin')));
  process.stderr.write(fs.readFileSync(path.join(process.env.VIETNAMIZER_RAW_DIR,'stderr.bin')));
  process.exitCode=r.guard_ok?(r.exitCode??1):2;
}
