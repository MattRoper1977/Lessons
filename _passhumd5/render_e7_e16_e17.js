// HUM-D5 A3 - one Chromium pass per lesson for E7, E16, E17 and the E9 graph leg.
// E7  reduced motion: context with reduceMotion:'reduce'; on EVERY stage list running
//     animations (document.getAnimations) whose effect duration > 10 ms, and any VISIBLE
//     element whose computed animation/transition duration > 0.01 s; the memory-flash
//     starter (.vary-flash, chips "Show the words"/"Check the words") must still hide its
//     words after the show (polled up to 15 s).
// E16 Save my responses: type into the visible route's first textarea, press
//     #save-independent, capture the download; the .txt must carry title, outcome, the
//     visible route's labels and the typed text; afterwards localStorage/sessionStorage/
//     cookies/indexedDB must be empty and no non-file network request may have fired
//     (requests are recorded from page load).
// E17 phone reality: 390x844, touch, DPR 3; on every stage every VISIBLE interactive
//     control must have a box >= 44x44; no control may sit under a position:fixed bar at
//     scroll top / middle / bottom; the stage's primary action (#next-slide) must be
//     reachable without horizontal scroll (scrollWidth <= clientWidth).
// E9g graph leg: on kind=graph/fieldwork lessons find the numeric inputs, set blank then
//     0, and prove no pageerror and #chart still renders.
const {chromium}=require('playwright');
const fs=require('fs'), path=require('path');
const ROOT=process.argv[2], OUT=process.argv[3];
const CHROME='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
function lessons(dir,acc=[]){for(const e of fs.readdirSync(dir,{withFileTypes:true})){const p=path.join(dir,e.name);
 if(fs.statSync(p).isDirectory())lessons(p,acc); else if(e.name.endsWith('_Lesson.html'))acc.push(p);} return acc;}
const NEXT='#next-slide, [data-action="next"]';
async function walk(p,fn){const n=await p.evaluate(()=>document.querySelectorAll('section[id^="slide-"]').length);
 const seen=new Set(); const out=[];
 for(let i=0;i<n;i++){ if(i>0){await p.evaluate(sel=>{const b=document.querySelector(sel); if(b)b.click();},NEXT);await p.waitForTimeout(150);}
  const id=await p.evaluate(()=>{const a=document.querySelector('section[id^="slide-"].active');return a?a.id:null;});
  if(!id||seen.has(id))break; seen.add(id); out.push(await fn(id,i)); }
 return out;}
(async()=>{
 const files=lessons(ROOT).sort(); const b=await chromium.launch({executablePath:CHROME});
 const R=[]; let n=0;
 for(const f of files){
  const id=path.basename(f).replace(/_Lesson\.html$/,''); const pack=path.relative(ROOT,f).split(path.sep)[0];
  const rec={lesson_id:id,pack,e7:{},e16:{},e17:{},e9g:null,not_run:[]};
  // ---------- E7 + E16 (desktop, reduced motion) ----------
  const ctx=await b.newContext({viewport:{width:1280,height:720},reducedMotion:'reduce',acceptDownloads:true});
  const p=await ctx.newPage(); const errs=[]; const reqs=[];
  p.on('pageerror',e=>errs.push(String(e.message).slice(0,160)));
  p.on('request',r=>{const u=r.url(); if(!u.startsWith('file://')&&!u.startsWith('data:')&&!u.startsWith('blob:'))reqs.push(u.slice(0,120));});
  try{
   await p.goto('file://'+f,{waitUntil:'load',timeout:45000}); await p.waitForTimeout(400);
   const kind=await p.evaluate(()=>window.CLASSIC_LESSON&&window.CLASSIC_LESSON.kind);
   const title=await p.evaluate(()=>window.CLASSIC_LESSON&&window.CLASSIC_LESSON.title);
   const outcome=await p.evaluate(()=>window.CLASSIC_LESSON&&window.CLASSIC_LESSON.outcome);
   // type into first visible textarea on the arrival stage as we pass it; measure animations per stage
   let typed=null;
   const stages=await walk(p,async(sid)=>{
     const m=await p.evaluate(()=>{
       const vis=el=>{if(!el.isConnected)return false; if(el.closest('[hidden],[inert],[aria-hidden="true"]'))return false; if(el.checkVisibility&&!el.checkVisibility({checkOpacity:true,checkVisibilityCSS:true}))return false; const r=el.getBoundingClientRect(); return r.width>0&&r.height>0;};
       const anims=document.getAnimations().filter(a=>a.playState==='running').map(a=>{const t=a.effect&&a.effect.getTiming?a.effect.getTiming():{}; const tgt=a.effect&&a.effect.target; return {type:a.constructor.name,name:a.animationName||a.transitionProperty||'',duration:t.duration,iterations:t.iterations,target:tgt?(tgt.tagName.toLowerCase()+(tgt.id?'#'+tgt.id:'')+(tgt.className&&typeof tgt.className==='string'?'.'+tgt.className.split(' ').slice(0,2).join('.'):'')):null,visible:tgt?vis(tgt):null};}).filter(a=>!(typeof a.duration==='number')||a.duration>10);
       const active=document.querySelector('section[id^="slide-"].active'); const styled=[];
       if(active)for(const el of active.querySelectorAll('*')){ if(!vis(el))continue; const cs=getComputedStyle(el);
         const ad=cs.animationDuration.split(',').map(parseFloat).filter(x=>x>0.01); const td=cs.transitionDuration.split(',').map(parseFloat).filter(x=>x>0.01);
         if((ad.length&&cs.animationName!=='none')||(td.length)){styled.push({el:el.tagName.toLowerCase()+(el.id?'#'+el.id:'')+(typeof el.className==='string'&&el.className?'.'+el.className.split(' ')[0]:''),anim:cs.animationName!=='none'?cs.animationName+' '+cs.animationDuration:'',transition:td.length?cs.transitionProperty.split(',')[0]+' '+cs.transitionDuration:''}); if(styled.length>=12)break;} }
       return {running:anims,styled_over_10ms:styled.length,styled_sample:styled.slice(0,5)};});
     if(!typed){ typed=await p.evaluate(()=>{const ta=[...document.querySelectorAll('section[id^="slide-"].active textarea')].find(t=>{const r=t.getBoundingClientRect();return r.width>0&&r.height>0&&!t.closest('[hidden]');}); if(!ta)return null; ta.value='HUMD5 E16 typed text 7f3a'; ta.dispatchEvent(new Event('input',{bubbles:true})); return ta.id||'textarea';}); }
     return {stage:sid,...m}; });
   rec.e7.stages=stages.map(s=>({stage:s.stage,running:s.running,styled_over_10ms:s.styled_over_10ms,styled_sample:s.styled_sample}));
   rec.e7.running_total=stages.reduce((t,s)=>t+s.running.length,0); rec.e7.styled_total=stages.reduce((t,s)=>t+s.styled_over_10ms,0);
   rec.e16.typed_into=typed;
   // memory flash: the starter box lives on its own stage (measured: slide-3); go there first
   const starterStage=await p.evaluate(()=>{const b=document.querySelector('#vary-starter, #re-starter'); const s=b&&b.closest('section[id^="slide-"]'); return s?s.id:null;});
   if(starterStage){ await p.goto('file://'+f,{waitUntil:'load',timeout:45000}); await p.waitForTimeout(300); for(let i=0;i<12;i++){const cur=await p.evaluate(()=>{const a=document.querySelector('section[id^="slide-"].active');return a?a.id:null;}); if(cur===starterStage)break; await p.evaluate(sel=>{const b=document.querySelector(sel); if(b)b.click();},NEXT); await p.waitForTimeout(100);} }
   const flash=await p.evaluate(async()=>{const box=document.querySelector('#vary-starter, #re-starter'); if(!box)return {present:false,reason:'no starter box'};
     const chips=[...box.querySelectorAll('button')]; const show=chips.find(c=>/show the words/i.test(c.textContent));
     const fl=box.querySelector('.vary-flash');
     if(!show||!fl)return {present:false,reason:'starter variant is not the memory flash',starter_chips:chips.map(c=>c.textContent.trim()).slice(0,6)};
     const words=()=>[...fl.querySelectorAll('span')].filter(sp=>{const r=sp.getBoundingClientRect();return r.width>0&&r.height>0&&(sp.textContent||'').trim();}).length;
     show.click(); await new Promise(r=>setTimeout(r,300)); const shown=words();
     await new Promise(r=>setTimeout(r,10800)); const after=words();
     return {present:true,stage:(box.closest('section[id^="slide-"]')||{}).id,active:(document.querySelector('section[id^="slide-"].active')||{}).id,words_shown_after_click:shown,words_visible_after_10_8s:after,text_after:(fl.textContent||'').slice(0,60),hides:shown>0&&after===0}; });
   rec.e7.memory_flash=flash;
   // E16: find the save control on whichever stage carries it
   const saveStage=await p.evaluate(()=>{const b=document.getElementById('save-independent'); const s=b&&b.closest('section[id^="slide-"]'); return s?s.id:null;});
   if(saveStage){
     // go to that stage
     for(let i=0;i<12;i++){const cur=await p.evaluate(()=>{const a=document.querySelector('section[id^="slide-"].active');return a?a.id:null;}); if(cur===saveStage)break; await p.evaluate(sel=>{const b=document.querySelector(sel); if(b)b.click();},NEXT); await p.waitForTimeout(100);}
     const typedSave=await p.evaluate(()=>{const ta=[...document.querySelectorAll('section[id^="slide-"].active textarea')].find(t=>{const r=t.getBoundingClientRect();return r.width>0&&r.height>0&&!t.closest('[hidden]');}); if(!ta)return null; ta.value='HUMD5 E16 typed text 7f3a'; ta.dispatchEvent(new Event('input',{bubbles:true})); return ta.id||'textarea';});
     rec.e16.typed_on_save_stage=typedSave;
     const before=reqs.length;
     const [dl]=await Promise.all([p.waitForEvent('download',{timeout:8000}).catch(()=>null), p.evaluate(()=>document.getElementById('save-independent').click())]);
     if(dl){ const fp=await dl.path(); const txt=fs.readFileSync(fp,'utf8');
       const labels=await p.evaluate(()=>[...document.querySelectorAll('section[id^="slide-"].active label')].filter(l=>{const r=l.getBoundingClientRect();return r.width>0&&r.height>0&&!l.closest('[hidden]');}).map(l=>l.textContent.replace(/\s+/g,' ').trim()).slice(0,10));
       const norm=x=>x.replace(/\s+/g,' ').trim().toLowerCase(); const ntxt=norm(txt);
       rec.e16.download={name:dl.suggestedFilename(),bytes:txt.length,has_title:!!title&&ntxt.includes(norm(title)),has_outcome:!!outcome&&ntxt.includes(norm(outcome)),has_typed:txt.includes('HUMD5 E16 typed text 7f3a'),labels_checked:labels.length,labels_present:labels.filter(l=>ntxt.includes(norm(l))).length,labels_missing:labels.filter(l=>!ntxt.includes(norm(l))).slice(0,4),head:txt.slice(0,400)};
     } else rec.e16.download=null;
     rec.e16.requests_during_save=reqs.length-before;
     rec.e16.storage=await p.evaluate(async()=>({localStorage:localStorage.length,sessionStorage:sessionStorage.length,cookie:document.cookie.length,indexedDB:(indexedDB.databases?(await indexedDB.databases()).length:'n/a')}));
     rec.e16.status_text=await p.evaluate(()=>{const s=document.getElementById('save-status');return s?s.textContent.trim().slice(0,100):null;});
   } else rec.not_run.push('E16: no #save-independent control');
   rec.e16.network_requests_total=reqs.length; rec.e16.network_sample=reqs.slice(0,3);
   // E9 graph leg
   if(['graph','fieldwork'].includes(kind)){
     rec.e9g=await p.evaluate(async()=>{const errs=[]; window.addEventListener('error',e=>errs.push(String(e.message)));
       const inputs=[...document.querySelectorAll('input[type="number"], input[inputmode="numeric"], input[inputmode="decimal"], input.count, [data-count] input')];
       const chart=document.getElementById('chart'); const before=chart?chart.innerHTML.length:null;
       const set=v=>{for(const i of inputs){i.value=v; i.dispatchEvent(new Event('input',{bubbles:true})); i.dispatchEvent(new Event('change',{bubbles:true}));}};
       set(''); await new Promise(r=>setTimeout(r,200)); const blank=chart?chart.innerHTML.length:null;
       set('0'); await new Promise(r=>setTimeout(r,200)); const zero=chart?chart.innerHTML.length:null;
       return {numeric_inputs:inputs.length,chart_present:!!chart,chart_len_before:before,after_blank:blank,after_zero:zero,errors:errs.slice(0,3)};});
     rec.e9g.pageerrors_after=errs.length;
   }
   rec.pageerrors=errs.slice(0,3);
  }catch(e){rec.not_run.push('E7/E16: '+String(e.message).split('\n')[0].slice(0,160));}
  await ctx.close();
  // ---------- E17 (phone) ----------
  const cm=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:3,isMobile:true,hasTouch:true});
  const q=await cm.newPage(); const errs2=[]; q.on('pageerror',e=>errs2.push(String(e.message).slice(0,160)));
  try{
   await q.goto('file://'+f,{waitUntil:'load',timeout:45000}); await q.waitForTimeout(400);
   const st=await walk(q,async(sid)=>q.evaluate((sid)=>{
     const vis=el=>{if(!el.isConnected)return false; if(el.closest('[hidden],[inert],[aria-hidden="true"]'))return false; if(el.checkVisibility&&!el.checkVisibility({checkOpacity:true,checkVisibilityCSS:true}))return false; const r=el.getBoundingClientRect(); return r.width>0&&r.height>0;};
     const fixedEls=[...document.querySelectorAll('body *')].filter(el=>{const cs=getComputedStyle(el);return (cs.position==='fixed')&&vis(el);});
     const fixed=fixedEls.map(el=>({node:el,el:el.tagName.toLowerCase()+(el.id?'#'+el.id:''),r:el.getBoundingClientRect().toJSON()})).filter(x=>x.r.height>0&&x.r.width>0);
     const bars=fixed.filter(x=>x.r.width>=300);
     const active=document.querySelector('section[id^="slide-"].active');
     const scroller=active; const positions=[0,Math.max(0,(scroller.scrollHeight-scroller.clientHeight)/2),Math.max(0,scroller.scrollHeight-scroller.clientHeight)];
     const small=[]; const under=[];
     const ctrls=()=>[...document.querySelectorAll('button, a[href], input, select, textarea, summary, [role="button"], [tabindex]:not([tabindex="-1"])')].filter(vis);
     for(const c of ctrls()){const r=c.getBoundingClientRect(); if(r.width<44||r.height<44)small.push({el:c.tagName.toLowerCase()+(c.id?'#'+c.id:'')+(c.className&&typeof c.className==='string'?'.'+c.className.split(' ')[0]:''),w:Math.round(r.width),h:Math.round(r.height),text:(c.textContent||c.value||'').trim().slice(0,30)});}
     for(const y of positions){ scroller.scrollTop=y; for(const c of ctrls()){ if(fixedEls.some(fx=>fx===c||fx.contains(c)))continue; const r=c.getBoundingClientRect(); if(r.bottom<0||r.top>window.innerHeight)continue; for(const bx of bars){ const b=bx.r; const ox=Math.min(r.right,b.left+b.width)-Math.max(r.left,b.left), oy=Math.min(r.bottom,b.top+b.height)-Math.max(r.top,b.top); if(ox>4&&oy>2){under.push({el:c.tagName.toLowerCase()+(c.id?'#'+c.id:'')+(typeof c.className==='string'&&c.className?'.'+c.className.split(' ')[0]:''),bar:bx.el,bar_h:Math.round(b.height),scroll:Math.round(y),ox:Math.round(ox),oy:Math.round(oy)}); break;} } } }
     scroller.scrollTop=0;
     const next=document.querySelector('#next-slide, [data-action="next"]'); const nr=next?next.getBoundingClientRect():null;
     return {stage:sid,fixed_bars:bars.map(b=>b.el+' '+Math.round(b.r.top)+'-'+Math.round(b.r.bottom)),fixed_all:fixed.map(b=>b.el+' '+Math.round(b.r.width)+'x'+Math.round(b.r.height)+'@'+Math.round(b.r.top)),small:small.slice(0,8),small_count:small.length,under:under.slice(0,6),under_count:under.length,hscroll:{doc:document.documentElement.scrollWidth>window.innerWidth+1,stage:scroller.scrollWidth>scroller.clientWidth+1,docW:document.documentElement.scrollWidth,stageW:scroller.scrollWidth,clientW:scroller.clientWidth},next_in_viewport:!!nr&&nr.left>=0&&nr.right<=window.innerWidth&&nr.top>=0&&nr.bottom<=window.innerHeight,next_visible:!!next&&vis(next)};},sid));
   rec.e17.stages=st; rec.e17.small_total=st.reduce((t,s)=>t+s.small_count,0); rec.e17.under_total=st.reduce((t,s)=>t+s.under_count,0);
   rec.e17.hscroll_stages=st.filter(s=>s.hscroll.doc||s.hscroll.stage).map(s=>s.stage); rec.e17.next_unreachable=st.filter(s=>!s.next_in_viewport).map(s=>s.stage);
   rec.e17.pageerrors=errs2.slice(0,2);
  }catch(e){rec.not_run.push('E17: '+String(e.message).split('\n')[0].slice(0,160));}
  await cm.close();
  R.push(rec); if(++n%10===0)console.error(`  ${n}/${files.length}`);
  fs.writeFileSync(OUT,JSON.stringify({scope:{root:ROOT,lessons:files.length,done:R.length},results:R}));
 }
 await b.close();
 fs.writeFileSync(OUT,JSON.stringify({scope:{root:ROOT,lessons:files.length,done:R.length},results:R},null,1));
 console.log('lessons',files.length,'done',R.length,'not_run entries',R.reduce((t,r)=>t+r.not_run.length,0));
 console.log('E7 running animations>10ms total',R.reduce((t,r)=>t+(r.e7.running_total||0),0),'styled>0.01s total',R.reduce((t,r)=>t+(r.e7.styled_total||0),0));
 console.log('E7 memory flash present',R.filter(r=>r.e7.memory_flash&&r.e7.memory_flash.present).length,'hides after 10 s',R.filter(r=>r.e7.memory_flash&&r.e7.memory_flash.present&&r.e7.memory_flash.hides).length);
 console.log('E16 downloads',R.filter(r=>r.e16.download).length,'title+outcome+typed all present',R.filter(r=>r.e16.download&&r.e16.download.has_title&&r.e16.download.has_outcome&&r.e16.download.has_typed).length,'storage clean',R.filter(r=>r.e16.storage&&r.e16.storage.localStorage===0&&r.e16.storage.sessionStorage===0&&r.e16.storage.cookie===0&&(r.e16.storage.indexedDB===0||r.e16.storage.indexedDB==='n/a')).length,'network requests>0',R.filter(r=>r.e16.network_requests_total>0).length);
 console.log('E17 small controls total',R.reduce((t,r)=>t+(r.e17.small_total||0),0),'under-bar total',R.reduce((t,r)=>t+(r.e17.under_total||0),0),'hscroll lessons',R.filter(r=>r.e17.hscroll_stages&&r.e17.hscroll_stages.length).length,'next unreachable lessons',R.filter(r=>r.e17.next_unreachable&&r.e17.next_unreachable.length).length);
})();
