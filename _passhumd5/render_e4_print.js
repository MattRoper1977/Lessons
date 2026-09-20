// HUM-D5 A3 E4 - print routes. For each lesson and each of Supported / Standard / Stretch,
// drive the lesson's OWN print arming (printArm(level), the function its route buttons call)
// with window.print stubbed, emulate print media, and save a PDF; separately drive
// printSection('organiser') for the A4 organiser. Per PDF: pages > 0, blank pages (no text
// and no drawings), clipped text (elements in print sections whose box extends past the A4
// printable width under print media), zero answers (no a / ma / arrival answer string in the
// PDF text), screen-only .vary-box absent (computed display none under print media).
// PDF text/blank analysis is done in Python afterwards (pymupdf); this script writes the PDFs
// and the DOM-side facts.
const {chromium}=require('playwright'); const fs=require('fs'), path=require('path');
const ROOT=process.argv[2], OUTDIR=process.argv[3], OUT=process.argv[4];
const CHROME='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
function lessons(dir,acc=[]){for(const e of fs.readdirSync(dir,{withFileTypes:true})){const p=path.join(dir,e.name);
 if(fs.statSync(p).isDirectory())lessons(p,acc); else if(e.name.endsWith('_Lesson.html'))acc.push(p);} return acc;}
const A4W=794; // px at 96 dpi, portrait
(async()=>{
 fs.mkdirSync(OUTDIR,{recursive:true});
 const files=lessons(ROOT).sort(); const b=await chromium.launch({executablePath:CHROME}); const R=[]; let n=0;
 for(const f of files){
  const id=path.basename(f).replace(/_Lesson\.html$/,''); const pack=path.relative(ROOT,f).split(path.sep)[0];
  const rec={lesson_id:id,pack,routes:{},not_run:[]};
  const ctx=await b.newContext({viewport:{width:794,height:1123}}); // A4 portrait at 96 dpi, so the clipped-text measure is taken at the printed width
  const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e.message).slice(0,120)));
  try{
   await p.goto('file://'+f,{waitUntil:'load',timeout:45000}); await p.waitForTimeout(300);
   const api=await p.evaluate(()=>({printArm:typeof window.printArm,printSection:typeof window.printSection,print_buttons:[...document.querySelectorAll('[onclick*="print"]')].map(b=>b.getAttribute('onclick')).slice(0,8)}));
   rec.api=api;
   for(const route of ['supported','standard','stretch','organiser']){
    try{
     await p.emulateMedia({media:'screen'});
     const armed=await p.evaluate((route)=>{let calls=[]; window.print=()=>{calls.push('print')};
       if(route==='organiser'){ if(typeof printSection==='function')printSection('organiser'); else return {error:'no printSection'}; }
       else { if(typeof printArm==='function')printArm(route); else return {error:'no printArm'}; }
       return {print_calls:calls.length,body_class:document.body.className,html_class:document.documentElement.className,armed_route:[...document.querySelectorAll('[data-print-route]')].filter(e=>getComputedStyle(e).display!=='none').length};},route);
     await p.emulateMedia({media:'print'}); await p.waitForTimeout(100);
     const dom=await p.evaluate((A4W)=>{
       const vis=el=>{const cs=getComputedStyle(el); if(cs.display==='none'||cs.visibility==='hidden')return false; let e=el.parentElement; while(e){const c=getComputedStyle(e); if(c.display==='none'||c.visibility==='hidden')return false; e=e.parentElement;} return true;};
       const secs=[...document.querySelectorAll('.print-section, [id^="print-"]')]; const shown=secs.filter(vis).map(s=>s.id||s.className);
       const vary=[...document.querySelectorAll('.vary-box')]; const varyShown=vary.filter(vis).length;
       const answers=[...document.querySelectorAll('[data-arrival-answer], .answers, .answer')].filter(vis).length;
       let clipped=[]; for(const s of secs.filter(vis)){ for(const el of s.querySelectorAll('p, li, td, th, h1, h2, h3, h4, label, div, span, img, table')){ if(!vis(el))continue; const r=el.getBoundingClientRect(); if(r.width>0&&r.right>A4W+2&&clipped.length<8)clipped.push({el:el.tagName.toLowerCase()+(el.id?'#'+el.id:'')+(typeof el.className==='string'&&el.className?'.'+el.className.split(' ')[0]:''),right:Math.round(r.right),text:(el.textContent||'').trim().slice(0,40)}); } }
       return {sections_shown:shown,vary_boxes:vary.length,vary_shown:varyShown,answer_elements_visible:answers,clipped_candidates:clipped,body_scrollWidth:document.body.scrollWidth};},A4W);
     const pdfPath=path.join(OUTDIR,`${id}__${route}.pdf`);
     await p.pdf({path:pdfPath,format:'A4',printBackground:true,preferCSSPageSize:true});
     rec.routes[route]={armed,dom,pdf:path.basename(pdfPath),pdf_bytes:fs.statSync(pdfPath).size};
    }catch(e){rec.routes[route]={error:String(e.message).split('\n')[0].slice(0,140)};}
   }
   rec.pageerrors=errs.slice(0,2);
  }catch(e){rec.not_run.push(String(e.message).split('\n')[0].slice(0,140));}
  await ctx.close(); R.push(rec); if(++n%10===0)console.error(`  ${n}/${files.length}`);
  fs.writeFileSync(OUT,JSON.stringify({scope:{root:ROOT,lessons:files.length,done:R.length,outdir:OUTDIR},results:R}));
 }
 await b.close(); fs.writeFileSync(OUT,JSON.stringify({scope:{root:ROOT,lessons:files.length,done:R.length,outdir:OUTDIR},results:R},null,1));
 console.log('lessons',files.length,'done',R.length,'not_run',R.reduce((t,r)=>t+r.not_run.length,0));
 console.log('pdfs',R.reduce((t,r)=>t+Object.values(r.routes).filter(x=>x.pdf).length,0),'route errors',R.reduce((t,r)=>t+Object.values(r.routes).filter(x=>x.error).length,0));
})();
