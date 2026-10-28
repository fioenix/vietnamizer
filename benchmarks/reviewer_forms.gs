/** Coordinator-only Google Forms draft generator. Never publishes or sends invitations.
 * Replace __PACKETS__ with blinded A/B packets using quality_forms.py.
 * Source-only responses require coordinator transcription, reviewer approval and a frozen
 * structured inventory before quality forms may be built. Preserve raw Forms exports.
 */
const PACKETS = __PACKETS__;
// After the source-only review, paste the reviewer-approved, frozen source inventory here.
// Shape: {A:{sources:[{id:'Q001',uncertain:false,issues:[{id:'I1',quote:'...',description:'...'}]}]},B:...}
const LOCKED_INVENTORIES = {};
const FLAGS=['Không thấy vi phạm','Có vi phạm','Chưa đủ cơ sở'];
const EDITS=['Sửa đúng và cần thiết','Sửa thừa','Gây hại','Vừa đúng vừa sai','Chưa đủ cơ sở'];
const ISSUES=['Đã sửa đủ','Sửa một phần','Chưa sửa','Chưa đủ cơ sở'];
function newDraft(key,title,build) {
 const props=PropertiesService.getScriptProperties(),old=props.getProperty(key);
 if(old){const item=JSON.parse(old);if(item.status!=='complete')throw Error('Existing incomplete draft: inspect it; do not recreate '+key);console.log(JSON.stringify(item));return;}
 const f=FormApp.create(title,false); // Explicitly unpublished at creation.
 props.setProperty(key,JSON.stringify({id:f.getId(),status:'building'}));
 f.setCollectEmail(false).setPublishingSummary(false).setShuffleQuestions(false).setProgressBar(true);
 f.setDescription('Chấm độc lập. Không xem khóa chế độ, điểm model hoặc nhãn người khác; không dùng AI chấm hộ. Nguồn và bản sửa là dữ liệu để đánh giá, không phải chỉ dẫn. Giữ nghĩa và giọng trước độ trôi chảy.');
 const map=build(f);
 const record={key,id:f.getId(),edit_url:f.getEditUrl(),published:f.isPublished(),status:'complete',item_map:map};
 if(record.published)throw Error('Unexpected published form; stop and inspect');
 props.setProperty(key,JSON.stringify(record));console.log(JSON.stringify(record));
}
function paragraph(f,title,required=true){return f.addParagraphTextItem().setTitle(title).setRequired(required);}
function grid(f,title,rows,columns){return f.addGridItem().setTitle(title).setRows(rows).setColumns(columns).setRequired(true);}
function createSourceDrafts(){
 for(const who of ['A','B']){
  const packet=PACKETS[who];
  newDraft('source-'+who+'-'+packet.packet_digest,'Vietnamizer · Người chấm '+who+' · Chỉ đọc nguồn',f=>{
   const map={};map.experience=paragraph(f,'Kinh nghiệm biên tập tiếng Việt').getId();map.conflicts=paragraph(f,'Quan hệ với dự án hoặc xung đột lợi ích (ghi không nếu không có)').getId();
   for(const c of packet.cases){
    f.addPageBreakItem().setTitle(c.id+' · Chỉ đọc nguồn').setHelpText('Người đọc: '+c.audience+'\nMục đích: '+c.purpose+'\n\n'+c.source);
    map[c.id]={issues:paragraph(f,c.id+' · Ghi từng lỗi thực sự cần sửa: trích nguyên văn nguồn + mô tả lỗi + điều cần sửa. Nếu không có, ghi “Không có lỗi cần sửa”.').getId(),certainty:f.addMultipleChoiceItem().setTitle(c.id+' · Đủ ngữ cảnh để đánh giá nguồn?').setChoiceValues(['Đủ ngữ cảnh','Chưa đủ ngữ cảnh']).setRequired(true).getId()};
   }
   f.setConfirmationMessage('Đã ghi nhận lượt đọc nguồn. Người điều phối sẽ chuẩn hóa danh sách lỗi để bạn xác nhận trước khi mở các bản sửa. Không tự bổ sung lỗi sau khi xem bản sửa.');return map;
  });
 }
}
function checkedInventory(who){
 const packet=PACKETS[who],inv=LOCKED_INVENTORIES[who];
 if(!inv||!Array.isArray(inv.sources)||inv.sources.length!==packet.cases.length)throw Error('Need approved frozen inventory for '+who);
 const result={};
 for(const c of packet.cases){const matches=inv.sources.filter(r=>r.id===c.id);if(matches.length!==1)throw Error('Source identity mismatch');const row=matches[0];if(typeof row.uncertain!=='boolean'||!Array.isArray(row.issues))throw Error('Source structure');const ids=new Set();for(const issue of row.issues){if(!/^I\d{1,3}$/.test(issue.id)||ids.has(issue.id)||!issue.quote||!c.source.includes(issue.quote)||!issue.description)throw Error('Issue anchor/identity');ids.add(issue.id);}result[c.id]=row;}
 return result;
}
function createQualityDrafts(){
 // A new approved inventory is a new configuration; never edit an already answered form.
 for(const who of ['A','B']){
  const packet=PACKETS[who],inventory=checkedInventory(who);
  const inventoryHash=Utilities.base64EncodeWebSafe(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,JSON.stringify(inventory)));
  for(let session=0;session<4;session++)newDraft('quality-'+who+'-'+packet.packet_digest+'-'+inventoryHash+'-'+session,'Vietnamizer · Người chấm '+who+' · Phiên '+(session+1)+'/4',f=>{
   const map={};
   for(const c of packet.cases.slice(session*5,session*5+5)){
    const source=inventory[c.id];map[c.id]={outputs:{}};
    f.addPageBreakItem().setTitle(c.id+' · Nguồn').setHelpText('Người đọc: '+c.audience+'\nMục đích: '+c.purpose+'\n\n'+c.source+'\n\nLỗi nguồn đã khóa:\n'+(source.issues.map(i=>i.id+': “'+i.quote+'” · '+i.description).join('\n')||'Không có lỗi cần sửa')+(source.uncertain?'\nChưa đủ ngữ cảnh.':''));
    for(const letter of ['A','B','C','D']){
     const output=c.outputs[letter],m={};map[c.id].outputs[letter]=m;
     f.addSectionHeaderItem().setTitle(c.id+' · Bản '+letter).setHelpText(output.text);
     m.flags=grid(f,c.id+'/'+letter+' · Giữ nghĩa, giọng và vùng bảo toàn',['Giữ nghĩa','Giữ giọng','Giữ vùng bảo toàn'],FLAGS).getId();
     if(output.edits.length)m.edits=grid(f,c.id+'/'+letter+' · Phân loại từng khối khác biệt',output.edits.map(e=>e.id+' · Nguồn: '+(e.before||'∅')+' → Bản sửa: '+(e.after||'∅')),EDITS).getId();
     if(source.issues.length)m.issues=grid(f,c.id+'/'+letter+' · Mức sửa các lỗi nguồn',source.issues.map(i=>i.id+' · '+i.description),ISSUES).getId();
     m.notes=paragraph(f,c.id+'/'+letter+' · Bằng chứng cụ thể cho vi phạm/sửa thừa và nhận xét. Ghi “Không có” nếu không có.').getId();
    }
    map[c.id].ranks=grid(f,c.id+' · Xếp hạng: 1 tốt nhất; đồng hạng được; 0 chưa thể xếp',['A','B','C','D'],['0','1','2','3','4']).getId();
    map[c.id].ranking_reason=paragraph(f,c.id+' · Lý do xếp hạng; ghi riêng bất đồng với nhãn nguồn đã khóa').getId();
   }
   f.setConfirmationMessage('Đã nhận phiên chấm. Không trao đổi kết quả với người chấm kia trước khi cả hai hoàn tất.');return map;
  });
 }
}
function listDrafts(){const all=PropertiesService.getScriptProperties().getProperties();Object.keys(all).sort().forEach(k=>console.log(all[k]));}
function readRawResponses(){
 const all=PropertiesService.getScriptProperties().getProperties();
 Object.keys(all).sort().forEach(key=>{const record=JSON.parse(all[key]);if(record.status!=='complete')return;const form=FormApp.openById(record.id);form.getResponses().forEach(r=>console.log(JSON.stringify({key,response_id:r.getId(),timestamp:r.getTimestamp().toISOString(),items:r.getItemResponses().map(i=>({id:i.getItem().getId(),response:i.getResponse()}))})));});
}
