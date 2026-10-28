/** Exact bounded payload; executed only through the authenticated Apps Script UI. */
const JOB = /*__BATCH_DATA__*/;
function runBatch(){
 const lock=LockService.getScriptLock();if(!lock.tryLock(1000))throw Error('Another mutation is running');
 try{
  if(JOB.mode==='initialize')initializeForms();
  else if(JOB.mode==='append')appendGroups();
  else if(JOB.mode==='finish')finishForms();
  else if(JOB.mode==='audit')auditForms();
  else throw Error('Unknown job');
 }finally{lock.releaseLock();}
}
function hashText(value){return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,value).map(b=>('0'+((b+256)%256).toString(16)).slice(-2)).join('');}
function stateKey(who){return 'simple-v2-'+JOB.form_ids[who];}
function getState(who){const raw=PropertiesService.getScriptProperties().getProperty(stateKey(who));if(!raw)throw Error('Not initialized');const s=JSON.parse(raw);if(s.contract_digest!==JOB.contract_digests[who])throw Error('Contract drift');return s;}
function putState(who,s){PropertiesService.getScriptProperties().setProperty(stateKey(who),JSON.stringify(s));}
function unchangedEmpty(f){if(f.getResponses().length!==0)throw Error('Live responses exist: preserve them; stop replacement');}
function initializeForms(){
 const props=PropertiesService.getScriptProperties();
 // Check BOTH forms before pausing/mutating either; existing state never authorizes reset.
 for(const who of ['A','B']){if(props.getProperty(stateKey(who)))throw Error('Already started; do not reset');unchangedEmpty(FormApp.openById(JOB.form_ids[who]));}
 for(const who of ['A','B']){const f=FormApp.openById(JOB.form_ids[who]);f.setAcceptingResponses(false);unchangedEmpty(f);}
 for(const who of ['A','B']){
  const f=FormApp.openById(JOB.form_ids[who]);unchangedEmpty(f);
  const old=f.getItems().map(i=>({id:i.getId(),type:String(i.getType()),title:i.getTitle(),help:i.getHelpText()}));
  const encoded=Utilities.base64Encode(JSON.stringify({form_id:f.getId(),zero_responses:true,items:old,at:new Date().toISOString()}),Utilities.Charset.UTF_8);
  const chunks=Math.ceil(encoded.length/7500);for(let n=0;n<chunks;n++)props.setProperty(stateKey(who)+'-old-'+n,encoded.slice(n*7500,(n+1)*7500));
  const s={schema:JOB.schema,form_id:f.getId(),contract_digest:JOB.contract_digests[who],status:'initializing',snapshot_chunks:chunks,completed:0};putState(who,s);
  for(let n=f.getItems().length-1;n>=0;n--)f.deleteItem(n);
  f.setTitle('Đánh giá văn bản tiếng Việt · Người chấm '+who).setDescription('Xem 20 đoạn, mỗi đoạn có bốn bản sửa A–D. Trong ảnh: bản gốc bên trái, bản sửa bên phải. Đánh giá riêng từng bản ở hai bảng chọn và ghi nhận xét ở câu 3. Không cần tìm lỗi trong bản gốc trước. Chấm độc lập, không dùng AI chấm hộ hoặc trao đổi đáp án với người chấm kia. Có thể mở lớn ảnh nếu chữ nhỏ.');
  f.setCollectEmail(false).setPublishingSummary(false).setShuffleQuestions(false).setProgressBar(true).setShowLinkToRespondAgain(false);
  const profile={experience:f.addParagraphTextItem().setTitle('Kinh nghiệm biên tập tiếng Việt').setRequired(true).getId(),conflicts:f.addParagraphTextItem().setTitle('Quan hệ với dự án hoặc xung đột lợi ích (nếu không có, ghi “Không”)').setRequired(true).getId()};
  s.status='building';s.profile=profile;putState(who,s);console.log(JSON.stringify({kind:'initialized',who,...s,old_items:old.length}));
 }
}
function appendGroups(){
 const who=JOB.who,f=FormApp.openById(JOB.form_ids[who]),s=getState(who),props=PropertiesService.getScriptProperties();
 unchangedEmpty(f);if(f.isAcceptingResponses())throw Error('Form must remain paused');
 if(s.status!=='building'||s.completed!==JOB.start||!JOB.groups.length||JOB.groups.length>5)throw Error('Partial/repeated/out-of-order batch; no automatic retry');
 const batchKey=stateKey(who)+'-batch-'+JOB.start;if(props.getProperty(batchKey))throw Error('Batch already started');
 props.setProperty(batchKey,JSON.stringify({status:'started',at:new Date().toISOString(),start:JOB.start}));
 const result=[];
 for(const g of JOB.groups){
  const map={id:g.id,images:{},page_title:'Đoạn '+g.id.slice(1)+' · Đánh giá bốn bản sửa',page_help:'Người đọc: '+g.audience+'\nMục đích: '+g.purpose};
  map.page=f.addPageBreakItem().setTitle(map.page_title).setHelpText(map.page_help).getId();
  for(const letter of ['A','B','C','D']){
   const bytes=Utilities.base64Decode(g.images[letter].base64);if(hashText(bytes)!==g.images[letter].sha256)throw Error('Image digest mismatch');
   const image=f.addImageItem().setTitle('Bản '+letter).setImage(Utilities.newBlob(bytes,'image/png','comparison.png')).setWidth(620).setHelpText('Bản gốc ở cột trái; bản sửa ở cột phải.');
   map.images[letter]={item_id:image.getId(),input_sha256:g.images[letter].sha256,provider_sha256:hashText(image.getImage().getBytes())};
  }
  for(const question of JOB.questions){
   if(question.kind==='grid')map[question.key]=f.addGridItem().setTitle(question.title).setRows(['Bản A','Bản B','Bản C','Bản D']).setColumns(question.choices).setRequired(true).getId();
   else map[question.key]=f.addParagraphTextItem().setTitle(question.title).setHelpText(question.help).setRequired(true).getId();
  }
  props.setProperty(stateKey(who)+'-'+g.id,JSON.stringify(map));result.push(map);
 }
 s.completed+=JOB.groups.length;putState(who,s);props.setProperty(batchKey,JSON.stringify({status:'completed',start:JOB.start,count:JOB.groups.length,ids:result.map(r=>r.id)}));console.log(JSON.stringify({kind:'batch_completed',who,completed:s.completed,groups:result,items:f.getItems().length}));
}
function auditOne(who){
 const f=FormApp.openById(JOB.form_ids[who]),s=getState(who),props=PropertiesService.getScriptProperties();
 const groups=[],sequence=[s.profile.experience,s.profile.conflicts];
 for(const [key,title] of Object.entries({experience:'Kinh nghiệm biên tập tiếng Việt',conflicts:'Quan hệ với dự án hoặc xung đột lợi ích (nếu không có, ghi “Không”)'})){const item=f.getItemById(s.profile[key]).asParagraphTextItem();if(item.getTitle()!==title||!item.isRequired())throw Error('Profile readback drift');}
 for(let n=1;n<=s.completed;n++){
  const id='Q'+String(n).padStart(3,'0'),m=JSON.parse(props.getProperty(stateKey(who)+'-'+id));
  const page=f.getItemById(m.page).asPageBreakItem();if(page.getTitle()!==m.page_title||page.getHelpText()!==m.page_help)throw Error('Page readback drift');sequence.push(m.page);
  for(const letter of ['A','B','C','D']){sequence.push(m.images[letter].item_id);const image=f.getItemById(m.images[letter].item_id).asImageItem();if(image.getTitle()!=='Bản '+letter||hashText(image.getImage().getBytes())!==m.images[letter].provider_sha256)throw Error('Image readback drift');}
  for(const question of JOB.questions){sequence.push(m[question.key]);const item=f.getItemById(m[question.key]);if(item.getTitle()!==question.title)throw Error('Question drift');if(question.kind==='grid'){const grid=item.asGridItem();if(JSON.stringify(grid.getRows())!==JSON.stringify(['Bản A','Bản B','Bản C','Bản D'])||JSON.stringify(grid.getColumns())!==JSON.stringify(question.choices)||!grid.isRequired())throw Error('Grid readback drift');}else if(item.getHelpText()!==question.help||!item.asParagraphTextItem().isRequired())throw Error('Notes requirement drift');}
  groups.push(m);
 }
 if(JSON.stringify(f.getItems().map(i=>i.getId()))!==JSON.stringify(sequence))throw Error('Form item sequence drift');
 return {who,status:s.status,completed:s.completed,item_count:f.getItems().length,published:f.isPublished(),accepting_responses:f.isAcceptingResponses(),responses:f.getResponses().length,responder_url:f.getPublishedUrl(),groups};
}
function finishForms(){
 const who=JOB.who,f=FormApp.openById(JOB.form_ids[who]),s=getState(who);unchangedEmpty(f);
 if(s.completed!==20||s.status!=='building'||f.getItems().length!==162)throw Error('Incomplete form');
 const audit=auditOne(who);f.setConfirmationMessage('Cảm ơn bạn đã chấm. Vui lòng không trao đổi đáp án với người chấm kia trước khi cả hai hoàn tất.');
 // Existing owner-approved anyone-with-link responder permissions remain unchanged.
 f.setAcceptingResponses(true);s.status='complete';putState(who,s);console.log(JSON.stringify({kind:'finished',...audit,status:'complete',accepting_responses:f.isAcceptingResponses()}));
}
function auditForms(){for(const who of ['A','B'])console.log(JSON.stringify({kind:'audit',...auditOne(who)}));}
