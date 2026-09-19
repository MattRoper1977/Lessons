// HUM-D5 A2 - re-render the PDFs of the lessons apply_proof.py touched. PDFs are never
// edited: Pupil_Resources.pdf and Knowledge_Organiser.pdf are printed again from their
// (now proofed) HTML with Chromium (A4, backgrounds on); Teacher_Notes.pdf is converted
// again from the proofed DOCX by LibreOffice (run by the caller). Input: APPLY_PLAN.json.
const {chromium}=require('playwright'); const fs=require('fs'), path=require('path');
const ROOT=process.argv[2], PLAN=JSON.parse(fs.readFileSync(process.argv[3],'utf8')), OUT=process.argv[4];
const CHROME='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
(async()=>{
 const targets=new Set();
 // every file the map edits (PLANNED on the first write, ALREADY_APPLIED on any later run) is a target
 const touched=PLAN.plan.filter(f=>f.edits.some(e=>e.status==='PLANNED'||e.status==='ALREADY_APPLIED')).map(f=>f.file);
 for(const rel of touched){ const bn=path.basename(rel); const dir=path.join(ROOT,path.dirname(rel));
  const m=bn.match(/^(.*?)_(Lesson|Pupil_Resources|Knowledge_Organiser|Editable_Pack|Teacher_Notes)\.(html|docx)$/); if(!m)continue; const id=m[1];
  if(m[2]==='Pupil_Resources'||m[2]==='Lesson'||m[2]==='Editable_Pack')targets.add(JSON.stringify([dir,id,'Pupil_Resources']));
  if(m[2]==='Knowledge_Organiser'||m[2]==='Lesson')targets.add(JSON.stringify([dir,id,'Knowledge_Organiser'])); }
 const b=await chromium.launch({executablePath:CHROME}); const ctx=await b.newContext({viewport:{width:794,height:1123}}); const R=[];
 for(const t of [...targets].sort()){ const [dir,id,kind]=JSON.parse(t); const html=path.join(dir,`${id}_${kind}.html`); const pdf=path.join(dir,`${id}_${kind}.pdf`);
  if(!fs.existsSync(html)||!fs.existsSync(pdf)){R.push({id,kind,skipped:'no html/pdf pair'});continue;}
  const before=fs.statSync(pdf).size; const p=await ctx.newPage();
  try{ await p.goto('file://'+html,{waitUntil:'load',timeout:45000}); await p.waitForTimeout(200); await p.emulateMedia({media:'print'}); await p.pdf({path:pdf,format:'A4',printBackground:true,preferCSSPageSize:true}); R.push({id,kind,bytes_before:before,bytes_after:fs.statSync(pdf).size}); }
  catch(e){R.push({id,kind,error:String(e.message).split('\n')[0].slice(0,120)});}
  await p.close(); }
 await b.close(); fs.writeFileSync(OUT,JSON.stringify({root:ROOT,rendered:R},null,1));
 console.log('re-rendered',R.filter(x=>x.bytes_after).length,'errors',R.filter(x=>x.error).length,'skipped',R.filter(x=>x.skipped).length);
})();
