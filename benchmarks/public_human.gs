/** Read-only export. No form/property/response writes, notifications or network uploads. */
const JOB = /*__EXPORT_JOB__*/;
function hashUtf8(value){return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,value,Utilities.Charset.UTF_8).map(b=>('0'+((b+256)%256).toString(16)).slice(-2)).join('');}
function hashBytes(value){return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,value).map(b=>('0'+((b+256)%256).toString(16)).slice(-2)).join('');}
function exportOne(){
 const f=FormApp.openById(JOB.form_id),props=PropertiesService.getScriptProperties();
 const state=JSON.parse(props.getProperty('public-ai-v1-'+JOB.cohort+'-'+JOB.reviewer));
 if(!state||state.form_id!==JOB.form_id||state.contract_digest!==JOB.contract_digest||state.ui_revision!==JOB.ui_revision||state.status!=='complete'||state.completed!==20||state.profile)throw Error('Frozen cohort/state drift');
 const sequence=f.getItems().map(i=>i.getId());
 if(JSON.stringify(sequence)!==JSON.stringify(JOB.item_ids))throw Error('Item identity/order drift');
 for(const group of JOB.groups){
  const page=f.getItemById(group.page).asPageBreakItem();
  if(page.getTitle()!==group.page_title||page.getHelpText()!==group.page_help)throw Error('Source context drift');
  for(const letter of ['A','B','C','D']){
   const expected=group.images[letter],image=f.getItemById(expected.item_id).asImageItem();
   if(image.getTitle()!=='Bản '+letter||image.getHelpText()!=='Bản gốc ở cột trái; bản sửa ở cột phải.'||image.getWidth()!==620||hashBytes(image.getImage().getBytes())!==expected.provider_sha256)throw Error('Frozen source/edit image drift');
  }
  for(const q of JOB.questions){
   const item=f.getItemById(group[q.key]);
   if(item.getTitle()!==q.title)throw Error('Question title drift');
   if(q.kind==='grid'){
    const grid=item.asGridItem();
    if(JSON.stringify(grid.getRows())!==JSON.stringify(['Bản A','Bản B','Bản C','Bản D'])||JSON.stringify(grid.getColumns())!==JSON.stringify(q.choices)||!grid.isRequired())throw Error('Grid schema drift');
   }else if(item.getHelpText()!==q.help||!item.asParagraphTextItem().isRequired())throw Error('Notes schema drift');
  }
 }
 const responses=f.getResponses().map(r=>({id:r.getId(),timestamp:r.getTimestamp().toISOString(),answers:r.getItemResponses().map(a=>({item_id:a.getItem().getId(),response:a.getResponse()}))}));
 return {schema:'public-human-export-v1',reviewer:JOB.reviewer,form_id:f.getId(),binding_digest:JOB.binding_digest,is_fixture:JOB.is_fixture,audit_complete:true,exported_at:new Date().toISOString(),responses};
}
function emitExport(packet){
 const text=JSON.stringify(packet),chars=Array.from(text),parts=[];
 for(let n=0;n<chars.length;n+=1000)parts.push(chars.slice(n,n+1000).join(''));
 const common={reviewer:JOB.reviewer,binding_digest:JOB.binding_digest,sha256:hashUtf8(text),total:parts.length};
 parts.forEach((data,index)=>console.log(JSON.stringify({kind:'public_human_export_part',...common,index,data})));
 console.log(JSON.stringify({kind:'public_human_export_done',...common}));
}
function runBatch(){const lock=LockService.getScriptLock();if(!lock.tryLock(1000))throw Error('Another operation running');try{emitExport(exportOne());}finally{lock.releaseLock();}}
