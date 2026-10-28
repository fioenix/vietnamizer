// Provider-free executable contract for the read-only Apps Script export.
const fs=require('fs'),vm=require('vm'),assert=require('assert'),crypto=require('crypto');
const source=fs.readFileSync(process.argv[2],'utf8');
function fixture(change=()=>{}){
 const logs=[],ctx={console:{log:s=>logs.push(JSON.parse(s))},Utilities:{DigestAlgorithm:{SHA_256:'sha256'},Charset:{UTF_8:'UTF-8'},computeDigest:(a,b,c)=>{if(typeof b==='string')assert.equal(c,'UTF-8');return [...crypto.createHash(a).update(typeof b==='string'?b:Buffer.from(b)).digest()];}},LockService:{getScriptLock:()=>({tryLock:()=>true,releaseLock:()=>{}})}};
 vm.createContext(ctx);vm.runInContext(source,ctx);const j=vm.runInContext('JOB',ctx),items=new Map(),answers=[];
 for(const g of j.groups){
  const page={getId:()=>g.page,getTitle:()=>g.page_title,getHelpText:()=>g.page_help};page.asPageBreakItem=()=>page;items.set(g.page,page);
  for(const l of 'ABCD'){
   const im={getId:()=>g.images[l].item_id,getTitle:()=> 'Bản '+l,getHelpText:()=> 'Bản gốc ở cột trái; bản sửa ở cột phải.',getWidth:()=>620,getImage:()=>({getBytes:()=>[1,2,3]})};im.asImageItem=()=>im;items.set(im.getId(),im);
  }
  for(const q of j.questions){
   const it={getId:()=>g[q.key],getTitle:()=>q.title,getHelpText:()=>q.help,isRequired:()=>true,getRows:()=>['Bản A','Bản B','Bản C','Bản D'],getColumns:()=>q.choices};it.asGridItem=()=>it;it.asParagraphTextItem=()=>it;items.set(it.getId(),it);
   answers.push({getItem:()=>it,getResponse:()=>q.kind==='grid'?Array(4).fill(q.choices[0]):'Tiếng Việt 👋\n'.repeat(100)});
  }
 }
 let ids=[...j.item_ids];const state={form_id:j.form_id,contract_digest:j.contract_digest,ui_revision:j.ui_revision,status:'complete',completed:20};
 const form={getId:()=>j.form_id,getItems:()=>ids.map(id=>items.get(id)),getItemById:id=>items.get(id),getResponses:()=>[{getId:()=> 'fixture-response',getTimestamp:()=>new Date('2026-10-26T00:00:00Z'),getItemResponses:()=>answers}]};
 ctx.PropertiesService={getScriptProperties:()=>({getProperty:()=>JSON.stringify(state)})};ctx.FormApp={openById:id=>{assert.equal(id,j.form_id);return form;}};
 change({items,j,state,setIds:v=>ids=v});return {ctx,logs};
}
let x=fixture();x.ctx.runBatch();assert.equal(x.logs.at(-1).kind,'public_human_export_done');assert(x.logs.every(x=>Buffer.byteLength(JSON.stringify(x),'utf8')<8192));
for(const change of [({state})=>state.form_id='foreign',({state})=>state.profile={experience:1},({setIds})=>setIds([]),({items,j})=>items.get(j.groups[0].readability).getColumns=()=>['changed'],({items,j})=>items.get(j.groups[0].images.A.item_id).getImage=()=>({getBytes:()=>[4,5,6]})]){const f=fixture(change);assert.throws(()=>f.ctx.runBatch());assert.equal(f.logs.length,0);}
for(const row of x.logs)process.stdout.write(JSON.stringify(row)+'\n');
