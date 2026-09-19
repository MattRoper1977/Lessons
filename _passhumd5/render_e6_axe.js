// HUM-D5 A3 E6 - accessibility. axe-core 4.10.2 on EVERY stage of EVERY lesson at two
// viewports (1280x720 desktop, 390x844 phone/touch); only serious/critical impacts are
// reported (moderate/minor counted, not listed). axe is SCOPED to the active stage plus
// the fixed chrome (tools nav, progress bar, prev/next, timer): the whole document holds
// nine stages and every print section, and a whole-document run took ~7 s per stage.
// MEASURED: every axe.run cost a flat ~10 s whatever the scope or rule set - axe's default
// asset PRELOAD (cross-origin CSSOM fetch, 10 s timeout) on a file:// page. preload:false and
// iframes:false bring a run to ~0.1-0.2 s; the full rule set including color-contrast is on. Contrast leg: for every VISIBLE
// <button> and every .brandline on each stage, the text colour against the resolved
// background (walk up through transparent ancestors) as a WCAG contrast ratio; below
// 4.5:1 is reported per pathway colour (R6: report, do not recolour).
const {chromium}=require('playwright'); const fs=require('fs'), path=require('path');
const ROOT=process.argv[2], OUT=process.argv[3];
const CHROME='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const AXE=fs.readFileSync(process.argv[4]||'/tmp/claude-0/humd5/node/node_modules/axe-core/axe.min.js','utf8');
function lessons(dir,acc=[]){for(const e of fs.readdirSync(dir,{withFileTypes:true})){const p=path.join(dir,e.name);
 if(fs.statSync(p).isDirectory())lessons(p,acc); else if(e.name.endsWith('_Lesson.html'))acc.push(p);} return acc;}
const NEXT='#next-slide, [data-action="next"]';
const CONTRAST=()=>{
 const lum=([r,g,b])=>{const f=c=>{c/=255;return c<=0.03928?c/12.92:Math.pow((c+0.055)/1.055,2.4);};return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b);};
 const parse=s=>{const m=s&&s.match(/rgba?\(([^)]+)\)/); if(!m)return null; const p=m[1].split(',').map(x=>parseFloat(x)); return {rgb:p.slice(0,3),a:p.length>3?p[3]:1};};
 const bg=el=>{let e=el; while(e&&e!==document.documentElement){const c=parse(getComputedStyle(e).backgroundColor); if(c&&c.a>0.99)return c.rgb; e=e.parentElement;} const c=parse(getComputedStyle(document.body).backgroundColor); return c&&c.a>0.99?c.rgb:[255,255,255];};
 const vis=el=>{if(el.closest('[hidden],[inert],[aria-hidden="true"]'))return false; if(el.checkVisibility&&!el.checkVisibility({checkOpacity:true,checkVisibilityCSS:true}))return false; const r=el.getBoundingClientRect(); return r.width>0&&r.height>0&&(el.textContent||'').trim().length>0;};
 const out=[]; const toHex=rgb=>'#'+rgb.map(x=>Math.round(x).toString(16).padStart(2,'0')).join('');
 for(const el of document.querySelectorAll('button, .brandline')){ if(!vis(el))continue; const fg=parse(getComputedStyle(el).color); if(!fg)continue; const b=bg(el); const L1=lum(fg.rgb),L2=lum(b); const ratio=(Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
  out.push({el:el.tagName.toLowerCase()+(el.id?'#'+el.id:'')+(typeof el.className==='string'&&el.className?'.'+el.className.split(' ')[0]:''),text:(el.textContent||'').trim().slice(0,24),fg:toHex(fg.rgb),bg:toHex(b),ratio:Math.round(ratio*100)/100,size:parseFloat(getComputedStyle(el).fontSize),bold:parseInt(getComputedStyle(el).fontWeight)>=700}); }
 return out; };
(async()=>{
 const files=lessons(ROOT).sort(); const b=await chromium.launch({executablePath:CHROME}); const R=[]; let n=0;
 for(const f of files){
  const id=path.basename(f).replace(/_Lesson\.html$/,''); const pack=path.relative(ROOT,f).split(path.sep)[0];
  const rec={lesson_id:id,pack,pathway:id.split('_')[0],viewports:{},not_run:[]};
  for(const [vname,vp] of [['desktop',{viewport:{width:1280,height:720}}],['phone',{viewport:{width:390,height:844},deviceScaleFactor:3,isMobile:true,hasTouch:true}]]){
   const ctx=await b.newContext(vp); const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e.message).slice(0,120)));
   try{
    await p.goto('file://'+f,{waitUntil:'load',timeout:45000}); await p.waitForTimeout(800);
    await p.addScriptTag({content:AXE});
    const nst=await p.evaluate(()=>document.querySelectorAll('section[id^="slide-"]').length); const stages=[]; const seen=new Set();
    for(let i=0;i<nst;i++){ if(i>0){await p.evaluate(sel=>{const b=document.querySelector(sel); if(b)b.click();},NEXT); await p.waitForTimeout(800);} // the stage fades in; axe sampled mid-fade reads blended colours (measured: .brandline #96a6b3 at 150 ms vs rgb(47,80,104) settled)
     const sid=await p.evaluate(()=>{const a=document.querySelector('section[id^="slide-"].active');return a?a.id:null;}); if(!sid||seen.has(sid))break; seen.add(sid);
     const ax=await p.evaluate(async()=>{const act=document.querySelector('section[id^="slide-"].active'); const ctxSel={include:[['section[id^="slide-"].active'],['nav.review-top'],['#classic-progress'],['#next-slide'],['#previous-slide'],['#auto-timer']]}; const r=await axe.run(ctxSel,{preload:false,iframes:false,resultTypes:['violations'],rules:{'region':{enabled:false}}}); return r.violations.map(v=>({id:v.id,impact:v.impact,help:v.help,nodes:v.nodes.length,targets:v.nodes.slice(0,3).map(nd=>nd.target.join(' ').slice(0,90))}));});
     const contrast=await p.evaluate(CONTRAST);
     stages.push({stage:sid,serious_critical:ax.filter(v=>['serious','critical'].includes(v.impact)),moderate_minor:ax.filter(v=>!['serious','critical'].includes(v.impact)).length,contrast_below:contrast.filter(c=>c.ratio<4.5),contrast_min:contrast.length?Math.min(...contrast.map(c=>c.ratio)):null,contrast_checked:contrast.length});
    }
    rec.viewports[vname]={stages,pageerrors:errs.slice(0,2),sc_total:stages.reduce((t,s)=>t+s.serious_critical.reduce((u,v)=>u+v.nodes,0),0),below_total:stages.reduce((t,s)=>t+s.contrast_below.length,0)};
   }catch(e){rec.not_run.push(vname+': '+String(e.message).split('\n')[0].slice(0,140));}
   await ctx.close();
  }
  R.push(rec); if(++n%10===0)console.error(`  ${n}/${files.length}`);
  fs.writeFileSync(OUT,JSON.stringify({scope:{root:ROOT,lessons:files.length,done:R.length,axe:'4.10.2',viewports:['1280x720','390x844 touch']},results:R}));
 }
 await b.close(); fs.writeFileSync(OUT,JSON.stringify({scope:{root:ROOT,lessons:files.length,done:R.length,axe:'4.10.2',viewports:['1280x720','390x844 touch']},results:R},null,1));
 const agg={}; for(const r of R)for(const v of Object.values(r.viewports))for(const s of v.stages)for(const x of s.serious_critical){agg[x.id]=(agg[x.id]||0)+x.nodes;}
 console.log('lessons',files.length,'done',R.length,'not_run',R.reduce((t,r)=>t+r.not_run.length,0));
 console.log('serious/critical nodes by rule:',JSON.stringify(agg));
 console.log('lessons with any serious/critical (desktop/phone):',R.filter(r=>r.viewports.desktop&&r.viewports.desktop.sc_total).length,R.filter(r=>r.viewports.phone&&r.viewports.phone.sc_total).length);
 console.log('contrast below 4.5 (lessons desktop/phone):',R.filter(r=>r.viewports.desktop&&r.viewports.desktop.below_total).length,R.filter(r=>r.viewports.phone&&r.viewports.phone.below_total).length);
})();
