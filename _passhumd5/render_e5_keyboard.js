// HUM-D5 A3 E5 - keyboard-only, on the sampled lessons (one match, sort, decision, sequence,
// source and editor lesson per pathway where the pathway has that kind). Per lesson:
//  (1) every stage: Tab from the top until focus returns to the first stop or 80 presses;
//      record the number of stops, whether every stop shows a visible focus indicator
//      (outline-style != none with width > 0, or a box-shadow), whether the stage's Next
//      control was reached, and a TRAP (activeElement unchanged over 3 presses while more
//      than one focusable exists, or focus left the document);
//  (2) the activity board stage: reach the board's first button by Tab and act on it and the
//      next with Enter/Space; a round counts when the board's feedback/status text or any
//      innerHTML/text/select state changes (a source board opens an inspect panel; a sequence
//      board reorders its list - neither touches a class, so the signature is the board content);
//  (3) the starter block (#vary-starter / #re-starter) and #vary-exit: reach a chip by Tab,
//      Enter; state change recorded;
//  (4) modals: the tools nav buttons that open a <dialog> (data-action tools/ta/organiser/
//      words/pause): Enter opens, Escape closes, focus returns to the opener.
const {chromium}=require('playwright'); const fs=require('fs'), path=require('path');
const ROOT=process.argv[2], OUT=process.argv[3], SAMPLE=process.argv[4]?JSON.parse(fs.readFileSync(process.argv[4],'utf8')):null;
const CHROME='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
function lessons(dir,acc=[]){for(const e of fs.readdirSync(dir,{withFileTypes:true})){const p=path.join(dir,e.name);
 if(fs.statSync(p).isDirectory())lessons(p,acc); else if(e.name.endsWith('_Lesson.html'))acc.push(p);} return acc;}
const NEXT='#next-slide, [data-action="next"]';
const FOCUSINFO=()=>{const a=document.activeElement; if(!a||a===document.body)return {tag:'body',key:'body'};
 const cs=getComputedStyle(a); const vis=(cs.outlineStyle!=='none'&&parseFloat(cs.outlineWidth)>0)||(cs.boxShadow&&cs.boxShadow!=='none');
 return {tag:a.tagName.toLowerCase(),id:a.id,cls:(typeof a.className==='string'?a.className.split(' ')[0]:''),text:(a.textContent||a.value||'').trim().slice(0,24),visible_indicator:vis,key:a.tagName+'#'+a.id+'.'+(typeof a.className==='string'?a.className.split(' ')[0]:'')+'|'+(a.textContent||'').trim().slice(0,24),isNext:!!a.closest('#next-slide,[data-action="next"]'),inActive:!!a.closest('section[id^="slide-"].active')};};
(async()=>{
 let files=lessons(ROOT).sort(); if(SAMPLE){const want=new Set(Object.values(SAMPLE).flat().map(x=>x.lesson)); files=files.filter(f=>want.has(path.basename(f).replace(/_Lesson\.html$/,'')));}
 const b=await chromium.launch({executablePath:CHROME}); const R=[];
 for(const f of files){
  const id=path.basename(f).replace(/_Lesson\.html$/,''); const rec={lesson_id:id,stages:[],activity:null,starter:null,exit:null,modals:[],not_run:[]};
  const ctx=await b.newContext({viewport:{width:1280,height:720}}); const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e.message).slice(0,120)));
  try{
   await p.goto('file://'+f,{waitUntil:'load',timeout:45000}); await p.waitForTimeout(300);
   rec.kind=await p.evaluate(()=>window.CLASSIC_LESSON&&window.CLASSIC_LESSON.kind);
   const nst=await p.evaluate(()=>document.querySelectorAll('section[id^="slide-"]').length); const seen=new Set();
   for(let i=0;i<nst;i++){ if(i>0){await p.evaluate(sel=>{const b=document.querySelector(sel); if(b)b.click();},NEXT); await p.waitForTimeout(120);}
    const sid=await p.evaluate(()=>{const a=document.querySelector('section[id^="slide-"].active');return a?a.id:null;}); if(!sid||seen.has(sid))break; seen.add(sid);
    await p.evaluate(()=>{document.activeElement&&document.activeElement.blur(); window.scrollTo(0,0);});
    const stops=[]; let first=null; let trap=null; let same=0; let last=null;
    for(let k=0;k<80;k++){ await p.keyboard.press('Tab'); const fi=await p.evaluate(FOCUSINFO);
      if(fi.key===last){same++; if(same>=3){trap={at:fi.key,press:k};break;}} else same=0; last=fi.key;
      if(fi.key==='body'){ if(k>0){/* wrapped through the document */ break;} continue; }
      if(!first)first=fi.key; else if(fi.key===first){break;}
      stops.push(fi); }
    const focusables=await p.evaluate(()=>[...document.querySelectorAll('section[id^="slide-"].active button, section[id^="slide-"].active a[href], section[id^="slide-"].active input, section[id^="slide-"].active textarea, section[id^="slide-"].active select, section[id^="slide-"].active summary, section[id^="slide-"].active [tabindex="0"]')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&!e.closest('[hidden],[inert]');}).length);
    rec.stages.push({stage:sid,stops:stops.length,focusables_in_stage:focusables,stops_in_active_stage:stops.filter(s=>s.inActive).length,without_indicator:stops.filter(s=>!s.visible_indicator).map(s=>s.tag+(s.id?'#'+s.id:'')+(s.cls?'.'+s.cls:'')).slice(0,6),without_indicator_count:stops.filter(s=>!s.visible_indicator).length,reached_next:stops.some(s=>s.isNext),trap});
   }
   // (2) activity board: find the stage that holds #activity-board with buttons
   const boardStage=await p.evaluate(()=>{const b=document.getElementById('activity-board'); const s=b&&b.closest('section[id^="slide-"]'); return s?s.id:null;});
   if(boardStage){
    await p.goto('file://'+f,{waitUntil:'load',timeout:45000}); await p.waitForTimeout(300);
    for(let i=0;i<12;i++){const cur=await p.evaluate(()=>{const a=document.querySelector('section[id^="slide-"].active');return a?a.id:null;}); if(cur===boardStage)break; await p.evaluate(sel=>{const b=document.querySelector(sel); if(b)b.click();},NEXT); await p.waitForTimeout(100);}
    const before=await p.evaluate(()=>{const b=document.getElementById('activity-board'); const fb=document.getElementById('activity-feedback'); return {buttons:b?b.querySelectorAll('button').length:0,feedback:fb?fb.textContent.trim():'',state:b?(b.innerHTML.length+'|'+b.textContent.replace(/\s+/g,' ').slice(0,4000)+'|'+[...b.querySelectorAll('[aria-pressed],select')].map(e=>e.getAttribute('aria-pressed')+'|'+(e.value||'')).join(';')):''};});
    await p.evaluate(()=>{document.activeElement&&document.activeElement.blur();});
    let reached=false, presses=0; for(let k=0;k<80;k++){ await p.keyboard.press('Tab'); presses++; const inBoard=await p.evaluate(()=>{const a=document.activeElement; return !!(a&&a.closest('#activity-board')&&a.tagName==='BUTTON');}); if(inBoard){reached=true;break;} }
    let acted=0; if(reached){ await p.keyboard.press('Enter'); acted++; await p.waitForTimeout(150); await p.keyboard.press('Tab'); const stillBoard=await p.evaluate(()=>{const a=document.activeElement; return !!(a&&a.closest('#activity-board')&&a.tagName==='BUTTON');}); if(stillBoard){await p.keyboard.press('Space'); acted++; await p.waitForTimeout(150);} }
    const after=await p.evaluate(()=>{const b=document.getElementById('activity-board'); const fb=document.getElementById('activity-feedback'); return {feedback:fb?fb.textContent.trim():'',state:b?(b.innerHTML.length+'|'+b.textContent.replace(/\s+/g,' ').slice(0,4000)+'|'+[...b.querySelectorAll('[aria-pressed],select')].map(e=>e.getAttribute('aria-pressed')+'|'+(e.value||'')).join(';')):''};});
    rec.activity={stage:boardStage,board_buttons:before.buttons,reached_by_tab:reached,tab_presses:presses,key_actions:acted,feedback_before:before.feedback.slice(0,80),feedback_after:after.feedback.slice(0,80),state_changed:before.state!==after.state||before.feedback!==after.feedback};
   } else rec.activity={stage:null,note:'no #activity-board in this lesson'};
   // (3) starter + exit chips
   for(const [name,sel] of [['starter','#vary-starter, #re-starter'],['exit','#vary-exit']]){
    const st=await p.evaluate(sel=>{const b=document.querySelector(sel); const s=b&&b.closest('section[id^="slide-"]'); return s?{stage:s.id,buttons:b.querySelectorAll('button').length}:null;},sel);
    if(!st){rec[name]={present:false};continue;}
    await p.goto('file://'+f,{waitUntil:'load',timeout:45000}); await p.waitForTimeout(300);
    for(let i=0;i<12;i++){const cur=await p.evaluate(()=>{const a=document.querySelector('section[id^="slide-"].active');return a?a.id:null;}); if(cur===st.stage)break; await p.evaluate(sel=>{const b=document.querySelector(sel); if(b)b.click();},NEXT); await p.waitForTimeout(100);}
    const before=await p.evaluate(sel=>{const b=document.querySelector(sel); return b.innerHTML.length+'|'+[...b.querySelectorAll('[aria-pressed]')].map(e=>e.getAttribute('aria-pressed')).join('');},sel);
    await p.evaluate(()=>{document.activeElement&&document.activeElement.blur();});
    let reached=false; for(let k=0;k<80;k++){ await p.keyboard.press('Tab'); if(await p.evaluate(sel=>{const a=document.activeElement; return !!(a&&a.closest(sel)&&(a.tagName==='BUTTON'||a.tagName==='INPUT'||a.tagName==='TEXTAREA'));},sel)){reached=true;break;} }
    if(reached){ const tag=await p.evaluate(()=>document.activeElement.tagName); if(tag==='BUTTON')await p.keyboard.press('Enter'); else await p.keyboard.type('keyboard entry'); await p.waitForTimeout(200); }
    const after=await p.evaluate(sel=>{const b=document.querySelector(sel); return b.innerHTML.length+'|'+[...b.querySelectorAll('[aria-pressed]')].map(e=>e.getAttribute('aria-pressed')).join('');},sel);
    rec[name]={present:true,stage:st.stage,buttons:st.buttons,reached_by_tab:reached,state_changed:before!==after};
   }
   // (4) modals via the tools nav
   await p.goto('file://'+f,{waitUntil:'load',timeout:45000}); await p.waitForTimeout(300);
   const openers=await p.evaluate(()=>[...document.querySelectorAll('nav.review-top button, [data-action="tools"], [data-action="ta"], [data-action="organiser"], [data-action="words"], [data-action="pause"]')].filter(b=>{const r=b.getBoundingClientRect();return r.width>0&&r.height>0;}).map(b=>b.id||('[data-action="'+b.getAttribute('data-action')+'"]')).filter((v,i,a)=>a.indexOf(v)===i).slice(0,6));
   for(const op of openers){
    try{
     const sel=op.startsWith('[')?op:'#'+op;
     await p.focus(sel); await p.keyboard.press('Enter'); await p.waitForTimeout(250);
     const opened=await p.evaluate(()=>{const d=[...document.querySelectorAll('dialog[open], [role="dialog"]:not([hidden])')].filter(x=>{const r=x.getBoundingClientRect();return r.width>0&&r.height>0;}); return d.length?(d[0].id||d[0].className):null;});
     const focusInside=await p.evaluate(()=>{const a=document.activeElement; return !!(a&&a.closest('dialog[open], [role="dialog"]'));});
     await p.keyboard.press('Escape'); await p.waitForTimeout(250);
     const closed=await p.evaluate(()=>![...document.querySelectorAll('dialog[open]')].some(x=>{const r=x.getBoundingClientRect();return r.width>0&&r.height>0;}));
     const returned=await p.evaluate(sel=>document.activeElement===document.querySelector(sel),sel);
     rec.modals.push({opener:op,opened,focus_inside_on_open:focusInside,closed_on_escape:closed,focus_returned:returned});
    }catch(e){rec.modals.push({opener:op,error:String(e.message).split('\n')[0].slice(0,100)});}
   }
   rec.pageerrors=errs.slice(0,2);
  }catch(e){rec.not_run.push(String(e.message).split('\n')[0].slice(0,140));}
  await ctx.close(); R.push(rec); console.error('  done',id);
  fs.writeFileSync(OUT,JSON.stringify({scope:{root:ROOT,sample:SAMPLE,lessons:files.length},results:R},null,1));
 }
 await b.close(); console.log('lessons',R.length);
})();
