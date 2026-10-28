import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { allowedTarget, publicIPv4, capture, validatePrintArgs } from '../benchmarks/gemini_boundary.mjs';

test('capture adapter refuses auth, permission bypass and resumed trials', () => {
  const args=['-p','public prompt','--mode','plan','--output-format','stream-json','--print-timeout','5m','--model','gemini-3.8-flash-medium'];
  assert.equal(validatePrintArgs(args),300000);
  for(const extra of [['--conversation','old'],['--dangerously-skip-permissions'],['--grant','x'],['--model','other']]) assert.throws(()=>validatePrintArgs([...args,...extra]));
  assert.throws(()=>validatePrintArgs(['login']));
});

test('egress permits HTTPS Google domains only', () => {
  for (const h of ['accounts.google.com:443','antigravity.google:443','x.googleapis.com:443']) assert.ok(allowedTarget(h));
  for (const h of ['localhost:443','169.254.169.254:443','host.docker.internal:443','google.com.evil.test:443','google.com:80','user@google.com:443','[::1]:443']) assert.equal(allowedTarget(h),null);
});
test('DNS answers cannot reach host or reserved networks', () => {
  for (const ip of ['127.0.0.1','10.1.2.3','172.17.0.1','192.168.1.2','169.254.1.1','0.0.0.0','100.64.1.1','198.18.0.1','224.1.1.1','::1','203.0.113.1']) assert.equal(publicIPv4(ip),false,ip);
  assert.equal(publicIPv4('142.250.1.1'),true);
});
test('capture retains split UTF-8 and nonzero stderr byte for byte', async () => {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'gemini-raw-'));
  const r=await capture(process.execPath,['-e',"process.stdout.write(Buffer.from([0xe1]));setTimeout(()=>{process.stdout.write(Buffer.from([0xbb,0x87]));process.stderr.write(Buffer.from([0xff,0x00]));process.exitCode=3},10)"],{dir,timeoutMs:2000});
  assert.equal(r.exitCode,3);
  assert.deepEqual(fs.readFileSync(path.join(dir,'stdout.bin')),Buffer.from('ệ'));
  assert.deepEqual(fs.readFileSync(path.join(dir,'stderr.bin')),Buffer.from([255,0]));
  await assert.rejects(()=>capture(process.execPath,['-e',''],{dir,timeoutMs:2000}));
});
test('deadline retains partial bytes and records termination', async () => {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'gemini-timeout-'));
  // A shell emits immediately; Node startup can itself exceed this deadline.
  const r=await capture('/bin/sh',['-c',"printf partial; exec sleep 30"],{dir,timeoutMs:300});
  assert.equal(r.timedOut,true); assert.equal(fs.readFileSync(path.join(dir,'stdout.bin'),'utf8'),'partial');
  assert.ok(r.signal);
});
test('shim mode keeps native child in outer supervisor process group', async () => {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'gemini-group-'));
  const group=spawnSync('/bin/ps',['-o','pgid=','-p',String(process.pid)],{encoding:'utf8'}).stdout.trim();
  await capture('/bin/sh',['-c','/bin/ps -o pgid= -p "$$"'],{dir,timeoutMs:2000,ownGroup:false});
  assert.equal(fs.readFileSync(path.join(dir,'stdout.bin'),'utf8').trim(),group);
});
