// Benchmark-only boundary helpers. No auth/profile reads and no TLS interception.
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import net from 'node:net';
import dns from 'node:dns/promises';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

export function allowedTarget(authority) {
  if (typeof authority !== 'string' || !/^[a-z0-9.-]+:443$/i.test(authority)) return null;
  const host=authority.slice(0,-4).toLowerCase();
  if (!host.split('.').every(s=>/^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/.test(s))) return null;
  return ['google.com','googleapis.com','googleusercontent.com','gstatic.com','antigravity.google']
    .some(root=>host===root||host.endsWith('.'+root)) ? host : null;
}
export function publicIPv4(ip) {
  if (net.isIP(ip)!==4) return false;
  const [a,b,c]=ip.split('.').map(Number);
  return !(a===0||a===10||a===127||a>=224||(a===100&&b>=64&&b<=127)||
    (a===169&&b===254)||(a===172&&b>=16&&b<=31)||
    (a===192&&(b===168||b===0||b===2))||(a===198&&(b===18||b===19||(b===51&&c===100)))||
    (a===203&&b===0&&c===113));
}
export function startProxy(port=3128) {
  const log=(host,decision)=>console.log(JSON.stringify({at:new Date().toISOString(),host,decision}));
  const server=http.createServer((req,res)=>{res.writeHead(403);res.end();});
  server.on('connect',async(req,client,head)=>{
    const host=allowedTarget(req.url);
    const deny=()=>{log(host||'invalid','deny');client.end('HTTP/1.1 403 Forbidden\r\n\r\n');};
    client.on('error',()=>{}); client.setTimeout(300000,()=>client.destroy());
    if(!host)return deny();
    try {
      const answers=await dns.lookup(host,{family:4,all:true});
      if(!answers.length||answers.some(a=>!publicIPv4(a.address)))return deny();
      // Connect to the validated numeric address; no second DNS lookup/rebinding.
      const upstream=net.connect({host:answers[0].address,port:443});
      upstream.setTimeout(300000,()=>upstream.destroy());
      upstream.on('error',()=>client.destroy()); upstream.on('close',()=>client.destroy());client.on('close',()=>upstream.destroy());
      upstream.on('connect',()=>{log(host,'allow');client.write('HTTP/1.1 200 Connection Established\r\n\r\n');if(head.length)upstream.write(head);client.pipe(upstream);upstream.pipe(client);});
    }catch{deny();}
  });
  server.listen(port,'0.0.0.0');return server;
}

export function validatePrintArgs(args) {
  const allowed=new Set(['-p','--mode','--output-format','--print-timeout','--json-schema','--project','--model','--effort']);
  const values=new Map();
  for(let i=0;i<args.length;i+=2){
    if(!allowed.has(args[i])||typeof args[i+1]!=='string'||values.has(args[i]))throw Error('unsupported or duplicate native argument');
    values.set(args[i],args[i+1]);
  }
  if(!values.get('-p')||values.get('--mode')!=='plan'||values.get('--output-format')!=='stream-json'||
    values.get('--model')!=='gemini-3.8-flash-medium'||(values.has('--effort')&&values.get('--effort')!=='medium'))throw Error('trial configuration mismatch');
  const m=/^([1-5])m$/.exec(values.get('--print-timeout')||'');
  if(!m)throw Error('bounded 1–5 minute timeout required');
  return Number(m[1])*60000;
}

export async function capture(command,args,{dir,timeoutMs,cwd,env=process.env,ownGroup=true}) {
  if(!Number.isFinite(timeoutMs)||timeoutMs<=0)throw Error('explicit positive deadline required');
  fs.mkdirSync(dir,{recursive:true});
  // An existing start receipt forbids rerunning an attempted trial.
  const start={command,args,cwd:cwd||process.cwd(),started_at:new Date().toISOString(),timeout_ms:timeoutMs};
  fs.writeFileSync(path.join(dir,'start.json'),JSON.stringify(start,null,2)+'\n',{flag:'wx'});
  const out=fs.openSync(path.join(dir,'stdout.bin'),'wx'),err=fs.openSync(path.join(dir,'stderr.bin'),'wx');
  const begin=Date.now();let timedOut=false,spawnError=null;
  const child=spawn(command,args,{cwd,env,shell:false,stdio:['ignore','pipe','pipe'],detached:ownGroup});
  const kill=signal=>{try{if(ownGroup)process.kill(-child.pid,signal);else child.kill(signal);}catch{}};
  let cancelTimer;
  const cancel=signal=>{kill(signal);cancelTimer??=setTimeout(()=>kill('SIGKILL'),3000);};
  const onTerm=()=>cancel('SIGTERM'),onInt=()=>cancel('SIGINT');
  process.on('SIGTERM',onTerm);process.on('SIGINT',onInt);
  const timer=setTimeout(()=>{timedOut=true;kill('SIGTERM');},timeoutMs);
  const hard=setTimeout(()=>kill('SIGKILL'),timeoutMs+3000);
  child.stdout.on('data',b=>fs.writeSync(out,b));child.stderr.on('data',b=>fs.writeSync(err,b));
  child.on('error',e=>{spawnError=e.code||'spawn_error';});
  return await new Promise(resolve=>child.on('close',(exitCode,signal)=>{
    clearTimeout(timer);clearTimeout(hard);clearTimeout(cancelTimer);process.off('SIGTERM',onTerm);process.off('SIGINT',onInt);fs.fsyncSync(out);fs.fsyncSync(err);fs.closeSync(out);fs.closeSync(err);
    const r={...start,ended_at:new Date().toISOString(),elapsed_ms:Date.now()-begin,exitCode,signal,timedOut,spawnError,
      streams:Object.fromEntries(['stdout.bin','stderr.bin'].map(n=>{const b=fs.readFileSync(path.join(dir,n));return[n,{bytes:b.length,sha256:createHash('sha256').update(b).digest('hex')}];}))};
    fs.writeFileSync(path.join(dir,'finish.json'),JSON.stringify(r,null,2)+'\n',{flag:'wx'});resolve(r);
  }));
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)&&process.argv[2]==='proxy')startProxy();
