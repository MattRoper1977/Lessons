import fs from 'node:fs/promises';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { FileBlob, Presentation, PresentationFile } from '@oai/artifact-tool';
import { createCanvas } from '@napi-rs/canvas';
import { finalizePresentation } from '/root/.codex/skills/builtins/presentations/container_tools/artifact_tool_utils.mjs';
const ROOT='/workspace/scratch/53a97a57d058/science_next24';
const SKILL='/root/.codex/skills/builtins/presentations';
process.env.RUNTIME_NODE=process.env.CODEX_PRIMARY_RUNTIME_NODE;
process.env.RUNTIME_NODE_MODULES=process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
process.env.RUNTIME_BIN_DIR=process.env.CODEX_PRIMARY_RUNTIME_ROOT+'/dependencies/bin/override';
process.env.RUNTIME_PYTHON=process.env.CODEX_PRIMARY_RUNTIME_PYTHON;
const PY=process.env.CODEX_PRIMARY_RUNTIME_PYTHON;
const FONT='Nimbus Sans';
const manifest=JSON.parse(await fs.readFile(path.join(ROOT,'chassis/chassis_manifest.json'),'utf8'));
const ctx=createCanvas(10,10).getContext('2d');
const fitIssues=[];
function wrap(text,width,size,bold=false){
  ctx.font=`${bold?'bold ':''}${size}px "${FONT}"`;
  return String(text).split('\n').flatMap(para=>{
    const words=para.split(/\s+/);const out=[];let line='';
    for(const word of words){ const s=line?line+' '+word:word;
      if(ctx.measureText(s).width>width&&line){out.push(line);line=word;}else line=s;
    }
    out.push(line);return out;
  }).join('\n');
}
function rect(slide,x,y,w,h,fill,stroke='none',sw=0,name='surface'){
 return slide.shapes.add({geometry:'rect',name,position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width:sw}});
}
function text(slide,str,x,y,w,h,size=28,bold=false,color='#1f2937',align='left',opts={}){
 const sh=rect(slide,x,y,w,h,'none','none',0,opts.name||String(str).slice(0,64));
 const txt=opts.nowrap?String(str):wrap(str,w-4,size,bold);
 sh.text=txt;sh.text.style={typeface:FONT,fontSize:size,bold,color,alignment:align,verticalAlignment:opts.middle?'middle':'top',autoFit:'none',wrap:'none',insets:{top:0,right:0,bottom:0,left:0},lineSpacing:1.08};
 const lines=txt.split('\n').length;
 if(lines*size*1.08>h+5)fitIssues.push({slide:slide.__n,text:String(str),height:h,required:lines*size*1.08});
 ctx.font=`${bold?'bold ':''}${size}px "${FONT}"`;
 const widest=Math.max(...txt.split('\n').map(line=>ctx.measureText(line).width));
 if(widest>w+5)fitIssues.push({slide:slide.__n,type:'text-width',text:String(str),width:w,required:widest});
 return sh;
}
function stagePalette(d,stage){
 const t=manifest.donors.find(x=>x.family===d.pathway+' Science').tokens;
 if(stage==='I do')return[t['--ido-border'],t['--ido-bg']];
 if(stage==='We do'||stage==='Hinge')return[t['--wedo-border'],t['--wedo-bg']];
 if(stage==='You do')return[t['--task-border'],t['--task-bg']];
 return[t['--lo-border'],t['--lo-bg']];
}
function shell(p,d,s,n,total,answer=false){
 const slide=p.slides.add();slide.__n=n;slide.background.fill='#ffffff';
 const [accent,bg]=stagePalette(d,s.stage);
 rect(slide,0,0,1280,16,accent);rect(slide,48,42,1184,51,bg);rect(slide,48,42,7,51,accent);
 text(slide,`${d.pathway} SCIENCE`,72,53,450,34,24,true,accent);
 text(slide,s.stage+(answer?' • Feedback':''),624,53,394,34,24,true,accent,'right');
 if(s.minutes&&!answer)text(slide,`${s.minutes} min`,1053,53,153,34,23,false,'#465465','right');
 const title=answer?`${s.title}: feedback`:s.title;
 const titleSize=wrap(title,1168,40,true).split('\n').length>1?36:40;
 text(slide,title,56,112,1168,90,titleSize,true);
 rect(slide,48,682,1184,1,'#d8dde2');
 text(slide,d.title,56,693,1110,22,15,false,'#64748b');
 text(slide,`${n} / ${total}`,1150,693,72,22,15,false,'#64748b','right');
 return slide;
}
function bodyLines(slide,lines,x,y,w,h,size=29,gap=18){
 if(!lines?.length)return;
 const heights=lines.map(l=>wrap(l,w,size).split('\n').length*size*1.1);
 const sum=heights.reduce((a,b)=>a+b,0)+gap*(heights.length-1);
 if(sum>h+8)fitIssues.push({slide:slide.__n,type:'body',height:h,required:sum,lines});
 lines.forEach((l,i)=>{text(slide,l,x,y,w,heights[i]+4,size);y+=heights[i]+gap;});
}
function diagram(slide,vis,x,y,w,h){
 const scale=Math.min(w/(vis.width||1000),h/(vis.height||560));
 const ox=x+(w-(vis.width||1000)*scale)/2,oy=y+(h-(vis.height||560)*scale)/2;
 for(const e of vis.elements||[]){
  if(e.type==='text'){
   text(slide,e.text,ox+e.x*scale,oy+e.y*scale,(e.w||150)*scale,(e.h||50)*scale,(e.size||28)*scale,!!e.bold,e.color||'#1f2937',e.align||'left',{nowrap:true,name:`Diagram label: ${e.text}`});
  }else if(e.type==='line'){
   const ax=ox+e.x*scale,ay=oy+e.y*scale,bx=ox+e.x2*scale,by=oy+e.y2*scale;
   const ang=Math.atan2(by-ay,bx-ax),len=Math.max(14,(e.strokeWidth||3)*2.8)*scale;
   const ex=e.arrow?bx-Math.cos(ang)*len*.75:bx,ey=e.arrow?by-Math.sin(ang)*len*.75:by;
   slide.shapes.add({geometry:'line',name:'Diagram line',position:{left:Math.min(ax,ex),top:Math.min(ay,ey),width:Math.max(.1,Math.abs(ex-ax)),height:Math.max(.1,Math.abs(ey-ay)),horizontalFlip:ex<ax,verticalFlip:ey<ay},fill:'none',line:{fill:e.stroke||'#1f2937',width:(e.strokeWidth||3)*scale}});
   if(e.arrow){
    const cx=bx-Math.cos(ang)*len/2,cy=by-Math.sin(ang)*len/2;
    slide.shapes.add({geometry:'triangle',name:'Diagram arrowhead',position:{left:cx-len/2,top:cy-len/2,width:len,height:len,rotation:ang*180/Math.PI+90},fill:e.stroke||'#1f2937',line:{fill:'none',width:0}});
   }
  }else if(['rect','ellipse'].includes(e.type)){
   slide.shapes.add({geometry:e.type,name:'Editable scientific diagram',position:{left:ox+e.x*scale,top:oy+e.y*scale,width:e.w*scale,height:e.h*scale},fill:e.fill||'none',line:{fill:e.stroke||'none',width:(e.strokeWidth||0)*scale}});
  }
 }
}
function nativeTable(slide,t,x,y,w,h,accent){
 const values=[t.headers,...t.rows].map(r=>r.map(v=>String(v??'')));
 const cols=t.headers.length,rows=values.length;
 const maxPerCol=Array.from({length:cols},(_,c)=>Math.max(...values.map(row=>String(row[c]||'').length)));
 const weights=maxPerCol.map(v=>Math.min(2.4,Math.max(1,Math.sqrt(v/9))));const sum=weights.reduce((a,b)=>a+b,0);
 const widths=weights.map(v=>w*v/sum);
 let size=27;
 for(;size>=22;size--){
  const rh=values.map(row=>Math.max(...row.map((v,c)=>wrap(v,widths[c]-22,size).split('\n').length))*size*1.15+22);
  if(rh.reduce((a,b)=>a+b,0)<=h)break;
 }
 const rowHeights=values.map(row=>Math.max(...row.map((v,c)=>wrap(v,widths[c]-22,size).split('\n').length))*size*1.15+22);
 const height=rowHeights.reduce((a,b)=>a+b,0);
 if(height>h+8)fitIssues.push({slide:slide.__n,type:'table',height:h,required:height});
 const table=slide.tables.add({rows,columns:cols,left:x,top:y,width:w,height:height,columnWidths:widths,values});
 table.styleOptions={headerRow:true,bandedRows:false};table.borders.assign({fill:'#ccd5db',width:1,style:'solid'});
 table.cells.block({row:0,column:0,rowCount:rows,columnCount:cols}).assign({textStyle:{fontSize:size,typeface:FONT,color:'#1f2937'},margins:{top:10,right:10,bottom:10,left:10},anchor:'center'});
 for(let r=0;r<rows;r++){
  table.rows[r].height=rowHeights[r];
  for(let c=0;c<cols;c++){
   const cell=table.getCell(r,c);cell.fill=r===0?accent:(r%2?'#f4f7f9':'#ffffff');
   cell.text.style={typeface:FONT,fontSize:size,bold:r===0,color:r===0?'#ffffff':'#1f2937',alignment:'left',verticalAlignment:'middle',insets:{top:10,right:10,bottom:10,left:10}};
  }
 }
 return height;
}
function notes(d,s,answer=false){
 return [answer?'Feedback slide. Use within the preceding activity time.':'',s.minutes?`Stage allocation: ${s.minutes} minutes.`:'Continue within the time allocated to this stage.',s.notes||'',s.reveal?`REVEAL / MODEL ANSWER\n${s.reveal}`:'',...(s.options||[]).map((o,i)=>`${String.fromCharCode(65+i)}. ${o.text}\n${o.correct?'Correct. ':''}${o.feedback}`),s.visual?`DIAGRAM DESCRIPTION\n${s.visual.description}`:'',`LESSON REFERENCES\n${(d.sources||[]).map(a=>`${a.title}\n${a.url}\n${a.note||''}`).join('\n\n')}`].filter(Boolean).join('\n\n');
}
function normalSlide(p,d,s,n,total){
 const slide=shell(p,d,s,n,total);const [accent,bg]=stagePalette(d,s.stage);const body=s.body||[];
 if(s.visual){
  const caption=[...body,s.prompt||''].filter(Boolean).join('  ');
  const capLines=wrap(caption,1160,24).split('\n').length;
  const capH=caption?capLines*27+6:0;
  const diagTop=194,diagH=472-capH;
  diagram(slide,s.visual,56,diagTop,1168,diagH);
  if(caption)text(slide,caption,56,diagTop+diagH+6,1168,capH,24);
 }else if(s.table){
  const bodyText=body.join(' ');const bh=bodyText?wrap(bodyText,1168,26).split('\n').length*30+12:0;
  if(bodyText)text(slide,bodyText,56,199,1168,bh,26);
  const caption=s.table.caption||'';const prompt=s.prompt||'';
  const captionH=caption?wrap(caption,1168,20).split('\n').length*22+5:0;
  const promptH=prompt?wrap(prompt,1168,27,true).split('\n').length*30+5:0;
  const tailH=12+captionH+(caption&&prompt?10:0)+promptH;
  const used=nativeTable(slide,s.table,56,199+bh,1168,467-bh-tailH,accent);
  let ty=199+bh+used+12;
  if(caption){text(slide,caption,56,ty,1168,captionH,20);ty+=captionH+(prompt?10:0);}
  if(prompt)text(slide,prompt,56,ty,1168,promptH,27,true,accent);
 }else if(s.options?.length){
  const lead=[...body,s.prompt||''].filter(Boolean).join(' ');
  const leadH=lead?wrap(lead,1168,29).split('\n').length*33+18:0;
  if(lead)text(slide,lead,56,196,1168,leadH,29);
  let y=196+leadH;
  const count=s.options.length;const boxH=Math.min(112,(462-leadH-(count-1)*12)/count);
  s.options.forEach((o,i)=>{
   rect(slide,56,y,1168,boxH,bg);rect(slide,56,y,6,boxH,accent);
   text(slide,String.fromCharCode(65+i),77,y+15,50,boxH-20,30,true,accent);
   text(slide,o.text.replace(/^[A-Z][.)]\s+/,''),133,y+15,1065,boxH-22,28);y+=boxH+12;
  });
 }else{
  const size=d.pathway==='BUILD'?33:31;
  let by=213,bh=s.prompt?335:420;
  if(s.stage==='Opening'&&d.objective&&!body.join(' ').includes(d.objective)){
   const oh=wrap(d.objective,1110,29,true).split('\n').length*33+65;
   rect(slide,56,198,1168,oh,bg);rect(slide,56,198,7,oh,accent);
   text(slide,'Learning intention',80,212,1110,30,22,true,accent);
   text(slide,d.objective,80,248,1110,oh-48,29,true);
   by=198+oh+24;bh=(s.prompt?552:666)-by;
  }
  if(body.length)bodyLines(slide,body,80,by,1120,bh,size,24);
  if(s.prompt){
   const lines=wrap(s.prompt,1090,29,true).split('\n').length;const ph=Math.max(78,lines*33+28);
   rect(slide,56,666-ph,1168,ph,bg);rect(slide,56,666-ph,7,ph,accent);
   text(slide,s.prompt,80,680-ph,1120,ph-20,29,true,accent);
  }
 }
 slide.speakerNotes.textFrame.setText(notes(d,s));
 return slide;
}
function feedbackSlide(p,d,s,n,total){
 const slide=shell(p,d,s,n,total,true);const [accent,bg]=stagePalette(d,s.stage);
 const points=[];
 if(s.reveal)points.push(s.reveal);
 if(s.options?.length){for(const [i,o]of s.options.entries())points.push(`${String.fromCharCode(65+i)}. ${o.feedback}`);}
 const words=points.join(' ').split(/\s+/).length;
 bodyLines(slide,points,80,208,1120,452,words>110?25:28,15);
 slide.speakerNotes.textFrame.setText(notes(d,s,true));
}
function useFeedback(s){return false;}
async function build(file){
 const raw=await fs.readFile(file,'utf8');const d=JSON.parse(raw);
 for(const [i,s] of d.slides.entries())for(const [j,e] of (s.visual?.elements||[]).entries())for(const key of ['fill','stroke','color']){
  const value=e[key];
  if(typeof value==='string'&&value.startsWith('#')&&!/^#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?([0-9a-fA-F]{2})?$/.test(value))throw new Error(`Invalid diagram ${key}: ${d.id} slide ${i+1} element ${j}: ${value}`);
 }
 const p=Presentation.create({slideSize:{width:1280,height:720}});
 const outDir=path.join(ROOT,'output',d.id),qa=path.join(ROOT,'qa/ppt',d.id),staging=path.join(ROOT,'build/ppt',d.id);
 await Promise.all([fs.mkdir(outDir,{recursive:true}),fs.mkdir(qa,{recursive:true}),fs.mkdir(staging,{recursive:true})]);
 const total=d.slides.length+d.slides.filter(useFeedback).length;const tableOwners=[];let i=1;
 for(const s of d.slides){normalSlide(p,d,s,i,total);if(s.table)tableOwners.push(i);i++;if(useFeedback(s)){feedbackSlide(p,d,s,i,total);i++;}}
 const rev=Date.now(),candidate=path.join(staging,`candidate-${rev}.pptx`),final=path.join(staging,`final-${rev}`,'Lesson.pptx');
 await fs.mkdir(path.dirname(final),{recursive:true});
 await(await PresentationFile.exportPptx(p)).save(candidate);
 const result=await finalizePresentation({workspaceDir:ROOT,candidatePath:candidate,finalPath:final,pythonExecutable:PY,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...tableOwners.flatMap(n=>['--require-native-table-slide',String(n)])],explicitTotalSlideCount:total,requiredNativeTableOwnerSlides:tableOwners,fontPolicy:{basis:'design',families:[FONT]},verifyArtifactToolImport:true,receiptPath:path.join(staging,`validation-${rev}.json`)});
 await fs.copyFile(final,path.join(outDir,'Lesson.pptx'));
 const rendered=await PresentationFile.importPptx(await FileBlob.load(final));
 for(const [n,s]of rendered.slides.items.entries()){
  const blob=await rendered.export({slide:s,format:'png',scale:1});await fs.writeFile(path.join(qa,`slide-${n+1}.png`),Buffer.from(await blob.arrayBuffer()));
  const lb=await s.export({format:'layout'});await fs.writeFile(path.join(qa,`slide-${n+1}.layout.json`),await lb.text());
 }
 const pdfDir=path.join(staging,`pdf-${rev}`);await fs.mkdir(pdfDir,{recursive:true});
 execFileSync(process.env.RUNTIME_BIN_DIR+'/soffice',['--headless','--convert-to','pdf','--outdir',pdfDir,final],{stdio:'pipe',timeout:120000});
 await fs.copyFile(path.join(pdfDir,'Lesson.pdf'),path.join(outDir,'Slides.pdf'));
 await fs.writeFile(path.join(qa,'build-fit.json'),JSON.stringify(fitIssues,null,2));
 await fs.writeFile(path.join(qa,'source-snapshot.json'),raw);
 await fs.writeFile(path.join(qa,'build-manifest.json'),JSON.stringify({id:d.id,sourcePath:file,sourceSha256:createHash('sha256').update(raw).digest('hex'),pptxSha256:createHash('sha256').update(await fs.readFile(path.join(outDir,'Lesson.pptx'))).digest('hex'),slideCount:total,nativeTableSlides:tableOwners,revision:rev,font:FONT,fitIssues:fitIssues.length},null,2));
 console.log(JSON.stringify({id:d.id,slides:total,nativeTables:tableOwners,output:path.join(outDir,'Lesson.pptx'),qa,fitIssues:fitIssues.length}));
}
const args=process.argv.slice(2);let files=[];
for(const a of args){if(a==='--all')files.push(...(await fs.readdir(path.join(ROOT,'content'))).filter(x=>x.endsWith('.json')).map(x=>path.join(ROOT,'content',x)));else files.push(path.resolve(a));}
if(!files.length)throw new Error('Pass JSON files or --all');
for(const file of files){fitIssues.length=0;await build(file);}
