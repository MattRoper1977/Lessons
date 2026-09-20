// HUM-D5 A0 - rendered-DOM text index.
// One Chromium page per lesson. Captures the surfaces the order names:
// every stage, every route panel, every <details>, every modal, every print
// section, plus the starter/exit blocks. Text is read from the RENDERED DOM.
const {chromium}=require('playwright');
const fs=require('fs'), path=require('path');
const ROOT=process.argv[2], OUT=process.argv[3];
const CHROME='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

function lessons(dir,acc=[]){for(const e of fs.readdirSync(dir,{withFileTypes:true})){
 const p=path.join(dir,e.name);
 if(e.isDirectory())lessons(p,acc); else if(e.name.endsWith('_Lesson.html'))acc.push(p);} return acc;}

(async()=>{
 const files=lessons(ROOT).sort();
 const b=await chromium.launch({executablePath:CHROME});
 const out=fs.createWriteStream(OUT), nr=[];
 let n=0;
 for(const f of files){
  const id=path.basename(f).replace(/_Lesson\.html$/,'');
  const pack=path.relative(ROOT,f).split(path.sep)[0];
  const ctx=await b.newContext({viewport:{width:1280,height:720}});
  const p=await ctx.newPage();
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  try{
   await p.goto('file://'+f,{waitUntil:'load',timeout:45000});
   await p.waitForTimeout(400);
   const rows=await p.evaluate(()=>{
    const out=[];
    const push=(surface,locator,text)=>{const t=(text||'').replace(/\s+/g,' ').trim(); if(t)out.push({surface,locator,text:t});};
    const q=s=>[...document.querySelectorAll(s)];
    // reveal everything: route panels, details, modals, print sections
    q('details').forEach(d=>d.open=true);
    q('[hidden]').forEach(e=>e.removeAttribute('hidden'));
    q('dialog').forEach(d=>{try{d.setAttribute('open','')}catch(e){}});
    const show=e=>{e.style.display='block';e.style.visibility='visible';e.style.opacity='1';};
    q('.modal,[role=dialog],[data-route-panel]').forEach(show);
    // stages
    q('section[id^="slide-"]').forEach(s=>push('rendered:stage',`#${s.id}`,s.innerText));
    // route panels
    q('[data-route-panel]').forEach((s,i)=>push('rendered:route',`[data-route-panel="${s.getAttribute('data-route-panel')}"][${i}]`,s.innerText));
    // print sections
    q('section[id^="print-"]').forEach(s=>push('rendered:print',`#${s.id}`,s.innerText));
    // details
    q('details').forEach((d,i)=>{const sm=d.querySelector('summary');
      push('rendered:details',`details[${i}]/summary`,sm?sm.textContent:'');
      push('rendered:details',`details[${i}]/body`,d.innerText);});
    // modals
    q('dialog,.modal,[role=dialog]').forEach((d,i)=>push('rendered:modal',d.id?`#${d.id}`:`modal[${i}]`,d.innerText));
    // starter + exit
    ['#vary-starter','#re-starter','#vary-exit'].forEach(sel=>{const e=document.querySelector(sel);
      if(e)push('rendered:block',sel,e.innerText);});
    return out;
   });
   for(const r of rows) out.write(JSON.stringify({lesson_id:id,pack,...r})+'\n');
   if(errs.length) nr.push({lesson_id:id,pack,surface:'rendered',reason:'pageerror: '+errs.join(' | ').slice(0,200)});
  }catch(e){
   nr.push({lesson_id:id,pack,surface:'rendered',reason:`render failed: ${e.message.split('\n')[0].slice(0,160)}`});
  }
  await ctx.close();
  if(++n%20===0) console.error(`  ${n}/${files.length}`);
 }
 out.end(); await b.close();
 fs.writeFileSync(OUT.replace('.jsonl','_NOT_RUN.jsonl'), nr.map(r=>JSON.stringify(r)).join('\n')+(nr.length?'\n':''));
 console.log(`lessons rendered: ${files.length}`);
 console.log(`NOT RUN / pageerror entries: ${nr.length}`);
 nr.slice(0,10).forEach(r=>console.log('  ',r.lesson_id,r.reason));
})();
