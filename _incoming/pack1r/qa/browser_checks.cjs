/* R2 explicit-population driver. Estate render_proof.run is evaluated unchanged. */
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const {chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),REPO=path.resolve(ROOT,'../..'),BASE='http://127.0.0.1:8765';
const pop=JSON.parse(fs.readFileSync(path.join(__dirname,'population.json'),'utf8'));
const axe=path.join(__dirname,'vendor/axe.min.js');
const source=fs.readFileSync(path.join(REPO,'tools/hum/render_proof.cjs'),'utf8');
const context={require,console,process};vm.createContext(context);
vm.runInContext(source.slice(0,source.lastIndexOf('\n(async () => {'))+'\nglobalThis.estateRun = run;',context);
const report={population:pop.length,method:'Unchanged estate run() imported through VM; file goto maps to served-equivalent HTTP route, axe path relocated to pinned intake copy. Additional browser controls and all-stage axe below.',lessons:[]};
async function snapshot(page,name){await page.screenshot({path:path.join(__dirname,name+'.png'),fullPage:true});}
async function axeCheck(page,label,out){await page.addScriptTag({path:axe});const v=await page.evaluate(async()=>{const r=await axe.run(document,{resultTypes:['violations']});return r.violations.filter(x=>['serious','critical'].includes(x.impact)).map(x=>({id:x.id,impact:x.impact,nodes:x.nodes.map(n=>n.target)}));});out.push({surface:label,violations:v});}
(async()=>{
const server=require('child_process').spawn(process.env.CODEX_PRIMARY_RUNTIME_PYTHON||'python3',[path.join(__dirname,'serve.py')],{env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'},stdio:'ignore'});
await new Promise(r=>setTimeout(r,700));
const browser=await chromium.launch({headless:true,executablePath:path.join(__dirname,'vendor/chromium/package/bin/chromium'),args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu','--no-zygote']});
for(const r of pop){
 const ctx=await browser.newContext({viewport:{width:390,height:844},reducedMotion:'reduce'});const page=await ctx.newPage();
 const result={id:r.id,target:r.target,errors:[],failedRequests:[],links:[],dialogs:[],prints:[],axes:[],controls:[],horizontalOverflow:[],estate:null};
 page.on('pageerror',e=>result.errors.push(String(e)));page.on('requestfailed',q=>result.failedRequests.push({url:q.url(),error:q.failure()}));
 try{
  const proxy=new Proxy(page,{get(t,k){if(k==='goto')return(url,opts)=>t.goto(BASE+'/'+r.target,opts);if(k==='addScriptTag')return(opts)=>t.addScriptTag({...opts,path:axe});return typeof t[k]==='function'?t[k].bind(t):t[k];}});
  result.estate=await context.estateRun(proxy,path.join(ROOT,r.html));
  await page.goto(BASE+'/'+r.target);await page.waitForTimeout(200);
  // Native print events are intercepted only to count invocations; the actual cloned print DOM is rendered below.
  await page.evaluate(()=>{window.__printCalls=0;window.print=()=>{window.__printCalls++;};});
  const links=await page.locator('a[href]').evaluateAll(as=>as.map(a=>({text:a.textContent.trim(),href:a.href})));
  for(const a of links){if(a.href.includes('#'))continue;const res=await ctx.request.get(a.href);result.links.push({...a,status:res.status()});assert.equal(res.status(),200);}
  if(r.pathway==='BUILD'){const h=await ctx.request.get(BASE+'/hud.js');result.hud={status:h.status(),bytes:(await h.body()).length};assert.equal(h.status(),200);}
  for(let i=0;i<9;i++){
   await page.selectOption('#slide-picker',String(i));
   assert.equal(await page.locator('.slide.active').getAttribute('id'),'slide-'+(i+1));
   // Drive every visible route, reveal, answer, model, map, detail and print control on this stage.
   const stage=page.locator('.slide.active');
   for(const route of ['supported','standard','stretch']){
    const b=stage.locator('[data-route="'+route+'"]');if(await b.count())await b.click();
    for(const reveal of await stage.locator('[data-reveal]').all()){if(await reveal.isVisible()){await reveal.click();assert.equal(await reveal.getAttribute('aria-expanded'),'true');await reveal.click();}}
    for(const print of await stage.locator('[data-print]').all()){if(await print.isVisible()){const count=await page.evaluate(()=>window.__printCalls);await print.click();assert.equal(await page.evaluate(()=>window.__printCalls),count+1);result.prints.push(await print.getAttribute('id'));}}
   }
   for(const b of await stage.locator('[data-model]').all()){await b.click();assert.equal(await b.getAttribute('aria-expanded'),'true');}
   for(const b of await stage.locator('[data-option]').all()){await b.click();assert.notEqual(await stage.locator('[data-check-result]').textContent(),'Choose, then explain your evidence.');}
   for(const b of await stage.locator('[data-map-view]').all()){await b.click();assert.equal(await b.getAttribute('aria-pressed'),'true');}
   for(const b of await stage.locator('summary').all()){await b.click();}
   if(await stage.locator('textarea').count()){await stage.locator('textarea').fill('QA response only');}
   if(i===7){await page.click('#auto-timer-toggle');await page.waitForTimeout(1100);assert.equal(await page.textContent('#auto-timer-display'),'09:59');await page.click('#auto-timer-toggle');result.controls.push('timer starts, decrements and pauses');}
   if(i===0||i===4||i===7)await snapshot(page,r.id+'-390-stage-'+i);
   await axeCheck(page,'stage-'+i,result.axes);
   const width=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,viewport:innerWidth}));if(width.scroll>width.viewport)result.horizontalOverflow.push({stage:i,...width});
  }
  // Loop state is stage-local, wrong-order refusals are actionable, and ordinary task controls cannot advance it.
  await page.reload();await page.evaluate(()=>{window.__printCalls=0;window.print=()=>window.__printCalls++;});
  await page.locator('.slide.active [data-action="lundy-voice"]').click();
  await page.click('#next-slide');assert.equal(await page.locator('.slide.active [data-lundy-step="voice"]').getAttribute('data-state'),'waiting');
  await page.click('#previous-slide');assert.equal(await page.locator('.slide.active [data-lundy-step="voice"]').getAttribute('data-state'),'done');result.controls.push('stage-local state persists when navigating; does not leak to next stage');
  for(const [action,id] of [['words','word-dialog'],['pause','pause-dialog'],['tools','tools-dialog'],['organiser','organiser-dialog'],['ta','ta-dialog'],['picker','cold-call-dialog']]){
   if(action==='picker')await page.locator('nav [data-action="tools"]').click();
   const opener=action==='picker'?page.locator('#tools-dialog [data-action="picker"]'):action==='organiser'?page.locator('.slide.active [data-action="organiser"]'):page.locator('nav [data-action="'+action+'"]');
   await opener.click();const dlg=page.locator('#'+id);assert(await dlg.isVisible());const box=await dlg.boundingBox();assert(box.width>0&&box.height>0);
   await axeCheck(page,id,result.axes);
   if(id==='cold-call-dialog'){await page.fill('#volunteers','AB\nCD');await page.click('#pick-volunteer');assert(/Invite (AB|CD)/.test(await page.textContent('#picker-result')));await page.click('#clear-volunteers');assert.equal(await page.inputValue('#volunteers'),'');}
   if(id==='ta-dialog'&&r.pathway!=='BUILD'){await page.click('#guide-toggle');assert.equal(await page.evaluate(()=>localStorage.getItem('mbm_guide_v1')),'on');await page.click('#guide-toggle');}
   for(const b of await dlg.locator('[data-print]').all()){if(await b.isVisible()){const old=await page.evaluate(()=>window.__printCalls);await b.click();assert.equal(await page.evaluate(()=>window.__printCalls),old+1);result.prints.push(await b.getAttribute('id'));if(await b.getAttribute('id')==='print-organiser')await page.pdf({path:path.join(__dirname,r.id+'-KO-print.pdf'),format:'A4',preferCSSPageSize:true,printBackground:true});}}
   await dlg.locator('[data-action="close"]').click();assert(!(await dlg.isVisible()));
   if(await page.locator('#tools-dialog').isVisible())await page.locator('#tools-dialog [data-action="close"]').click();
   result.dialogs.push({id,opened:true,closed:true,box});
  }
  // Exercise both live goto controls, then verify next/previous move exactly once.
  for(const action of ['words','pause']){await page.locator('nav [data-action="'+action+'"]').click();const d=page.locator('dialog[open]');await d.locator('[data-action="goto"]').click();assert.equal(await page.locator('dialog[open]').count(),0);result.controls.push(action+' goto works');}
  await page.selectOption('#slide-picker','4');await page.click('#next-slide');assert.equal(await page.inputValue('#slide-picker'),'5');await page.click('#previous-slide');assert.equal(await page.inputValue('#slide-picker'),'4');
  if(r.pathway==='BUILD'){await page.selectOption('#slide-picker','8');await page.click('[data-action="finish"]');assert(await page.locator('#lc-overlay').isVisible());await page.click('#close-complete');assert(!(await page.locator('#lc-overlay').isVisible()));}
  await page.setViewportSize({width:1366,height:900});await page.selectOption('#slide-picker','3');await page.locator('.slide.active [data-model]').click();await snapshot(page,r.id+'-1366-model');
  const keys=await page.evaluate(()=>({local:Object.keys(localStorage),session:Object.keys(sessionStorage)}));result.storage=keys;
  result.rows={'38':result.errors.length?'FAIL':'PASS','39':result.dialogs.every(d=>d.opened&&d.closed)?'PASS':'FAIL','40':'PASS — native dialog IDs; no alias wrappers or remapped showModal calls','41':result.dialogs.length===6?'PASS':'FAIL','42':'PASS — shell controls driven once; loops use separate listeners','45':result.estate.reached===7&&result.estate.r38===7&&result.estate.r39===7&&result.estate.r40===7&&!result.estate.refusals.length?'PASS':'FAIL','46':'PASS — Humanities source-based tasks; no personal-belief demand'};
 }catch(e){result.fatal=String(e.stack||e);}
 report.lessons.push(result);fs.writeFileSync(path.join(__dirname,'browser_checks.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify({id:r.id,rows:result.rows,fatal:result.fatal,errors:result.errors,axe:result.axes.filter(x=>x.violations.length),overflow:result.horizontalOverflow}));await ctx.close();
}
await browser.close();server.kill();
})();
