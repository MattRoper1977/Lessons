// HUM-D5 A3 E3 - on-screen answer visibility, DEFAULT state, per stage.
// Correction #11: the text index force-reveals every panel, so a hit there is
// "present in the DOM", not "visible on screen". This instrument answers the
// narrower question the check actually asks: with the lesson opened as a
// pupil would see it - nothing clicked except the stage Next button - is any
// check-question answer visible on any stage?
// Visible = Chromium checkVisibility (display, visibility, opacity, closed
// details) AND a non-zero box AND no [hidden]/[inert]/[aria-hidden=true]
// ancestor. Answer strings come from CLASSIC_LESSON q/a + mq/ma (E3_ANSWERS).
// Positive control per lesson: press #arrival-reveal on its stage and prove
// the same instrument then SEES the answers; a lesson whose control fails is
// NOT RUN (instrument blind), never PASS.
const {chromium}=require('playwright');
const fs=require('fs'), path=require('path');
const ROOT=process.argv[2], ANSWERS=process.argv[3], OUT=process.argv[4];
const CHROME='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

function lessons(dir,acc=[]){for(const e of fs.readdirSync(dir,{withFileTypes:true})){
 const p=path.join(dir,e.name);
 if(e.isDirectory())lessons(p,acc); else if(e.name.endsWith('_Lesson.html'))acc.push(p);} return acc;}

// Runs in the page: which of `answers` are visible right now, and where.
const MEASURE=(answers)=>{
 const norm=s=>String(s||'').replace(/\s+/g,' ').trim();
 const visible=el=>{
  if(!el.isConnected)return false;
  if(el.closest('[hidden],[inert],[aria-hidden="true"]'))return false;
  if(typeof el.checkVisibility==='function'&&!el.checkVisibility({checkOpacity:true,checkVisibilityCSS:true}))return false;
  const r=el.getBoundingClientRect(); if(!(r.width>0&&r.height>0))return false;
  return true;
 };
 const active=document.querySelector('section.slide.active, section[id^="slide-"].active');
 const out=[];
 for(const a of answers){
  const na=norm(a); if(!na)continue;
  // innermost elements whose text contains the answer
  const holders=[...document.querySelectorAll('body *')].filter(el=>{
   if(['SCRIPT','STYLE','TEMPLATE','NOSCRIPT'].includes(el.tagName))return false;
   if(!norm(el.textContent).includes(na))return false;
   return ![...el.children].some(c=>norm(c.textContent).includes(na));
  });
  const vis=holders.filter(visible);
  out.push({answer:na,in_dom:holders.length,visible:vis.length,
   where:vis.slice(0,5).map(el=>{const s=el.closest('section[id^="slide-"]');
     return (s?('#'+s.id):'(no stage)')+' > '+el.tagName.toLowerCase()+(el.id?'#'+el.id:'')+(el.hasAttribute('data-arrival-answer')?'[data-arrival-answer]':'');})});
 }
 return {stage:active?active.id:null,rows:out};
};

(async()=>{
 const answers=JSON.parse(fs.readFileSync(ANSWERS,'utf8'));
 const files=lessons(ROOT).sort();
 const b=await chromium.launch({executablePath:CHROME});
 const results=[], not_run=[];
 let n=0;
 for(const f of files){
  const id=path.basename(f).replace(/_Lesson\.html$/,'');
  const pack=path.relative(ROOT,f).split(path.sep)[0];
  const strings=answers[id]||[];
  const ctx=await b.newContext({viewport:{width:1280,height:720}});
  const p=await ctx.newPage();
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  try{
   await p.goto('file://'+f,{waitUntil:'load',timeout:45000});
   await p.waitForTimeout(400);
   if(errs.length)throw new Error('pageerror: '+errs.join(' | ').slice(0,200));
   if(!strings.length){not_run.push({lesson_id:id,pack,reason:'no answer strings in E3_ANSWERS for this lesson'});await ctx.close();continue;}
   const nStages=await p.evaluate(()=>document.querySelectorAll('section[id^="slide-"]').length);
   const hasNext=await p.$('#next-slide, [data-action="next"]');
   if(!hasNext)throw new Error('no Next control (#next-slide / [data-action=next])');
   // DEFAULT-STATE sweep: stage by stage, only Next is pressed.
   const perStage=[]; const seenStages=new Set();
   for(let i=0;i<nStages;i++){
    if(i>0){await p.click('#next-slide, [data-action="next"]');await p.waitForTimeout(120);}
    const m=await p.evaluate(MEASURE,strings);
    if(!m.stage||seenStages.has(m.stage))break; // Next stopped advancing
    seenStages.add(m.stage);
    perStage.push(m);
   }
   const visibleHits=[];
   for(const m of perStage)for(const r of m.rows)if(r.visible>0)visibleHits.push({stage:m.stage,answer:r.answer,where:r.where});
   const inDomAny=new Set(); for(const m of perStage)for(const r of m.rows)if(r.in_dom>0)inDomAny.add(r.answer);
   const notInDom=strings.map(s=>s.replace(/\s+/g,' ').trim()).filter(s=>s&&!inDomAny.has(s));
   // POSITIVE CONTROL: reveal on the arrival stage, same instrument must now see answers.
   let control={ran:false,visible_after_reveal:0,stage:null};
   const reveal=await p.$('#arrival-reveal');
   if(reveal){
    const revealStage=await p.evaluate(()=>{const b=document.getElementById('arrival-reveal');const s=b&&b.closest('section[id^="slide-"]');return s?s.id:null;});
    // go back to that stage: reload to default, press Next until it is active
    await p.goto('file://'+f,{waitUntil:'load',timeout:45000});await p.waitForTimeout(300);
    for(let i=0;i<nStages;i++){const cur=await p.evaluate(()=>{const a=document.querySelector('section[id^="slide-"].active');return a?a.id:null;});
     if(cur===revealStage)break; await p.click('#next-slide, [data-action="next"]');await p.waitForTimeout(100);}
    await p.click('#arrival-reveal');await p.waitForTimeout(150);
    const m=await p.evaluate(MEASURE,strings);
    control={ran:true,stage:m.stage,visible_after_reveal:m.rows.reduce((t,r)=>t+(r.visible>0?1:0),0)};
   }
   const controlOk=!control.ran||control.visible_after_reveal>0;
   results.push({lesson_id:id,pack,answers:strings.length,stages_walked:perStage.length,stages_in_dom:nStages,
     visible_default:visibleHits,not_in_dom:notInDom,control,
     verdict: controlOk ? (visibleHits.length?'VISIBLE_IN_DEFAULT_STATE':'HIDDEN_UNTIL_REVEAL') : 'NOT_RUN_CONTROL_BLIND'});
   if(!controlOk)not_run.push({lesson_id:id,pack,reason:'positive control blind: reveal pressed on '+control.stage+' but instrument saw 0 answers'});
  }catch(e){
   not_run.push({lesson_id:id,pack,reason:String(e.message).split('\n')[0].slice(0,200)});
  }
  await ctx.close();
  if(++n%20===0)console.error(`  ${n}/${files.length}`);
 }
 await b.close();
 fs.writeFileSync(OUT,JSON.stringify({scope:{root:ROOT,answers:ANSWERS,lessons:files.length,pattern:'*_Lesson.html'},results,not_run},null,1));
 const c={};for(const r of results)c[r.verdict]=(c[r.verdict]||0)+1;
 console.log('lessons:',files.length,'measured:',results.length,'not_run:',not_run.length);
 console.log('verdicts:',JSON.stringify(c));
 for(const r of results)if(r.visible_default.length)console.log(' VISIBLE',r.lesson_id,r.visible_default.map(h=>h.stage+' '+JSON.stringify(h.answer.slice(0,60))).join(' | '));
 for(const r of not_run)console.log(' NOT RUN',r.lesson_id,r.reason);
})();
