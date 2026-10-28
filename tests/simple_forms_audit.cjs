// Targeted provider-free audit regressions. No cloud calls or labels.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const questions=[{key:'preservation',kind:'grid',title:'preservation',choices:['yes']},{key:'readability',kind:'grid',title:'readability',choices:['yes']},{key:'notes',kind:'paragraph',title:'notes',help:'help'}];
const job={form_ids:{A:'form'},contract_digests:{A:'contract'},questions};
const state={profile:{experience:1,conflicts:2},completed:1,status:'building',contract_digest:'contract'};
const map={id:'Q001',page:3,page_title:'page',page_help:'context',images:{A:{item_id:4,provider_sha256:'hash'},B:{item_id:5,provider_sha256:'hash'},C:{item_id:6,provider_sha256:'hash'},D:{item_id:7,provider_sha256:'hash'}},preservation:8,readability:9,notes:10};
const titles=['','Kinh nghiệm biên tập tiếng Việt','Quan hệ với dự án hoặc xung đột lợi ích (nếu không có, ghi “Không”)','page','Bản A','Bản B','Bản C','Bản D','preservation','readability','notes'];
const items=titles.map((title,id)=>({title,id,help:id===3?'context':id===10?'help':'',getId(){return this.id},getTitle(){return this.title},getHelpText(){return this.help},isRequired(){return true},asParagraphTextItem(){return this},asPageBreakItem(){return this},asImageItem(){return this},asGridItem(){return this},getImage(){return {getBytes(){return []}}},getRows(){return ['Bản A','Bản B','Bản C','Bản D']},getColumns(){return ['yes']}}));
let sequence=items.slice(1);
const form={getItemById:id=>items[id],getItems:()=>sequence,isPublished:()=>true,isAcceptingResponses:()=>false,getResponses:()=>[],getPublishedUrl:()=> 'url'};
const context={FormApp:{openById:()=>form},PropertiesService:{getScriptProperties:()=>({getProperty:key=>JSON.stringify(key.endsWith('Q001')?map:state)})}};
vm.createContext(context);vm.runInContext(fs.readFileSync('benchmarks/simple_forms.gs','utf8').replace('/*__BATCH_DATA__*/',JSON.stringify(job)),context);context.hashText=()=> 'hash';
assert.equal(context.auditOne('A').item_count,10);
[sequence[3],sequence[4]]=[sequence[4],sequence[3]];assert.throws(()=>context.auditOne('A'),/sequence drift/);
sequence=items.slice(1);items[3].help='wrong case';assert.throws(()=>context.auditOne('A'),/Page readback drift/);
items[3].help='context';items[1].title='wrong profile';assert.throws(()=>context.auditOne('A'),/Profile readback drift/);
console.log('4 Apps Script readback audit checks passed');
