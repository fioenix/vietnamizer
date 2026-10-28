#!/usr/bin/env node
// PATH adapter for the unchanged Agybird wrapper; never used for authentication.
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { capture, validatePrintArgs } from './gemini_boundary.mjs';
const args=process.argv.slice(2),binary='/usr/local/bin/agy';
if(args.length===1&&args[0]==='--version'){
  const r=spawnSync(binary,args,{stdio:'inherit',timeout:5000});process.exit(r.status??1);
}
const timeoutMs=validatePrintArgs(args);
const dir=path.join(process.cwd(),'.native-raw');
// Stay in the wrapper's process group so the outer supervisor can terminate all.
const r=await capture(binary,args,{dir,timeoutMs:timeoutMs+1000,ownGroup:false});
process.stdout.write(fs.readFileSync(path.join(dir,'stdout.bin')));
process.stderr.write(fs.readFileSync(path.join(dir,'stderr.bin')));
process.exitCode=r.exitCode??1;
