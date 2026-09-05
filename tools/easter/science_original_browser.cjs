/* Actual original Science pages, reviewed HUD, native navigation and print. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {chromium} = require('playwright');
const args = {};
for (let i=2;i<process.argv.length;i++) {
  const key=process.argv[i];
  assert.ok(['--root','--targets','--site-root','--out','--channel'].includes(key));
  assert.ok(process.argv[i+1]); args[key.slice(2)]=process.argv[++i];
}
const root=fs.realpathSync(args.root||path.join(__dirname,'../..'));
const site=fs.realpathSync(args['site-root']);
const out=path.resolve(args.out); fs.mkdirSync(out,{recursive:true});
const doc=JSON.parse(fs.readFileSync(path.resolve(args.targets),'utf8'));
assert.equal(doc.schema,'original-science-browser-targets-v1');
assert.equal(doc.targets.length,25);
assert.equal(new Set(doc.targets.map(t=>t.path)).size,25);
const sha=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
function source(file,expected) { assert.equal(sha(fs.readFileSync(file)),expected,'Source identity: '+file); }
source(path.join(site,'hud.js'),doc.reviewedHud.sha256);
for(const t of doc.targets) source(path.join(root,t.path),t.expectedPatchedSha256);
const report={schema:'original-science-browser-report-v1',inputs:doc,startedAt:new Date().toISOString(),cases:[],routes:[],errors:[],missingLocal:[],external:[],pdfs:[],
  scope:'Installed Chromium, original lesson interactions and actual print CSS. PDF pages receive separate visual review. No physical classroom duration, practical completion or external media playback claim.'};
const origin='http://science-original.test';
let active='',browser;
const measured=async(name,fn)=>{active=name;try{await fn();report.cases.push({name,passed:true});}catch(e){report.cases.push({name,passed:false,error:e.message});throw e;}};
const rejects=async(name,fn)=>{let fired=false;try{await fn();}catch(e){fired=true;}assert.ok(fired,name+' must catch the planted defect');};
const slide=page=>page.locator('.slide.active');
const current=page=>page.locator('.slide').evaluateAll(nodes=>nodes.findIndex(n=>n.classList.contains('active')));
const next=page=>page.locator('.controls button[onclick="nextSlide()"]');
const previous=page=>page.locator('.controls button[onclick="prevSlide()"]');
async function title(page){assert.equal(await page.locator('.slide.active').count(),1);assert.equal(await slide(page).getAttribute('data-title'),'Title');assert.equal(await slide(page).locator('h1').count(),1);assert.ok((await slide(page).locator('h1').innerText()).trim());assert.equal(await slide(page).locator('.main-session-meta').isVisible(),true);}
async function minutes(page,t){
  const rows=await page.locator('.slide').evaluateAll(nodes=>nodes.map(n=>({name:n.dataset.title,time:Number(n.dataset.timer)})));
  assert.equal(rows.length,t.expectedStageCount); assert.ok(rows.every(r=>Number.isFinite(r.time)&&r.time>=0));
  const index=rows.findIndex(r=>r.name==='Independent Work');assert.ok(index>0);
  assert.equal(rows[index].time,t.independentMinutes);
  const sum=items=>items.reduce((n,r)=>n+r.time,0);
  assert.deepEqual(t.sessionCount===2?[sum(rows.slice(0,index)),sum(rows.slice(index))]:[sum(rows)],t.periodMinutes);
  return index;
}
async function move(page,index){
  for(let n=0;n<15&&await current(page)!==index;n++) {
    const at=await current(page);
    if(at<index) await advanceStage(page,at+1);
    else await previous(page).click();
  }
  assert.equal(await current(page),index);
}
async function advanceStage(page,index){
  // The original reveal framework deliberately uses Next for each diagram
  // step before it leaves that stage. Exercise those real clicks too.
  const from=await current(page);assert.equal(index,from+1);
  let clicks=0;
  for(;clicks<80&&await current(page)===from;clicks++) await next(page).click();
  assert.equal(await current(page),index,'Next must finish the reveals and reach the next stage');
  report.navigationSteps ||= [];
  report.navigationSteps.push({case:active,from,to:index,clicks});
}
async function periodBoundary(page,t,index){
  const boundary=page.locator('.slide').nth(index-1).locator('.period-break');
  assert.equal(await boundary.count(),1,'Period 1 has its own visible stop instruction');
  const text=await boundary.innerText();assert.match(text,/STOP for today/);assert.ok(text.includes(t.periodDays[1]));
}
async function clock(page){
  assert.equal(await slide(page).getAttribute('data-title'),'Independent Work');
  assert.equal(await page.locator('.timer-widget').isVisible(),true);
  assert.equal(await page.locator('#auto-timer').isVisible(),false);
  assert.equal((await page.locator('#auto-timer-display').innerText()).trim(),'00:00');
}
async function selectedPrint(page,level){
  assert.ok((await page.locator('body').getAttribute('class')).split(/\s+/).includes('print-'+level));
  for(const tier of ['supported','standard','stretch'])for(const kind of ['scaffold','worksheet'])
    assert.equal(await page.locator('#print-'+kind+'-'+tier).isVisible(),tier===level,'Only chosen '+kind+' tier prints');
  for(const selector of ['.controls','.timer-widget','#auto-timer','#mbm-hud'])
    assert.equal(await page.locator(selector+':visible').count(),0,selector+' must not print');
}
async function configure(context){
  await context.addInitScript(()=>{window.__printRequests=0;window.print=()=>{window.__printRequests++;};});
  context.on('page',page=>page.on('pageerror',e=>report.errors.push({case:active,message:e.message})));
  await context.route('**/*',async route=>{
    const u=new URL(route.request().url());
    if(u.origin!==origin){report.external.push({case:active,url:u.href});return route.abort('blockedbyclient');}
    const owner=u.pathname.startsWith('/Lessons/')?root:site;
    let f;try{
      f=path.resolve(owner,'.'+decodeURIComponent(u.pathname.replace(/^\/Lessons/,'')));
      assert.ok(f.startsWith(owner+path.sep));f=fs.realpathSync(f);assert.ok(f.startsWith(owner+path.sep));assert.ok(fs.statSync(f).isFile());
    }catch(e){report.missingLocal.push({case:active,path:u.pathname});return route.fulfill({status:404,body:'Missing reviewed local asset'});}
    const types={'.js':'application/javascript','.css':'text/css','.html':'text/html; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.json':'application/json'};
    return route.fulfill({contentType:types[path.extname(f)]||'application/octet-stream',body:fs.readFileSync(f)});
  });
}
async function load(page,t){await page.emulateMedia({media:'screen'});await page.goto(origin+'/Lessons/'+t.path,{waitUntil:'domcontentloaded'});await slide(page).waitFor();}
async function snap(page,name){
  await slide(page).evaluate(el=>Promise.all(el.getAnimations().filter(a=>Number.isFinite(a.effect.getComputedTiming().endTime)).map(a=>a.finished.catch(()=>{}))));
  await page.screenshot({path:path.join(out,name+'.png'),fullPage:true});
}
const value=async page=>(await page.locator('#timerDisplay').innerText()).trim();
const seconds=v=>v.split(':').reduce((a,b)=>a*60+Number(b),0);
async function exercise(t,viewport={width:1280,height:800},responsive=false){
  const id=path.basename(t.path,'.html')+(responsive?'-'+viewport.width:'');
  const context=await browser.newContext({viewport,reducedMotion:responsive?'reduce':'no-preference',hasTouch:responsive});
  await configure(context);const page=await context.newPage();let independent;
  const before={errors:report.errors.length,missing:report.missingLocal.length,external:report.external.length};
  try{
    await measured(id+'/load-title-periods',async()=>{await load(page,t);await title(page);independent=await minutes(page,t);await snap(page,id+'-title');});
    if(!responsive)await measured(id+'/all-stages-through-real-navigation',async()=>{
      for(let i=1;i<t.expectedStageCount;i++){await advanceStage(page,i);assert.equal(await page.locator('.slide.active').count(),1);assert.ok((await slide(page).locator('h1,h2').first().innerText()).trim());}
      await move(page,0);
    });
    await measured(id+'/independent-restart',async()=>{
      if(t.sessionCount===2){
        await slide(page).getByRole('button',{name:/Resume period 2/i}).click();assert.equal(await current(page),independent);
        const text=await slide(page).innerText();assert.ok(text.includes(t.periodDays[1]));
        await periodBoundary(page,t,independent);
      }else await move(page,independent);
      await clock(page);assert.equal(await value(page),t.independentMinutes+':00');
    });
    if(!responsive)await measured(id+'/one-manual-clock-and-navigation-pause',async()=>{
      const start=page.locator('.timer-widget button[onclick="startTimer()"]');
      const began=Date.now();await start.click();await start.click();await page.waitForTimeout(2200);
      const elapsed=(Date.now()-began)/1000,used=t.independentMinutes*60-seconds(await value(page));
      assert.ok(used>=1&&used<=Math.ceil(elapsed)+1,'Two Start clicks must not create duplicate intervals');await clock(page);
      await advanceStage(page,independent+1);const paused=await value(page);await page.waitForTimeout(1150);assert.equal(await value(page),paused);
      await previous(page).click();assert.equal(await current(page),independent);await page.waitForTimeout(1150);assert.equal(await value(page),paused);await clock(page);
      await page.locator('.timer-widget button[onclick="resetTimer()"]').click();assert.equal(await value(page),t.independentMinutes+':00');
    });
    await measured(id+'/independent-visible-layout',async()=>{
      if(responsive){
        const size=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));assert.ok(size.scroll<=size.width+2,'No document horizontal overflow');
        for(const button of [previous(page),next(page)]){const r=await button.boundingBox();assert.ok(r&&r.height>=43.5&&r.x>=0&&r.x+r.width<=viewport.width+1,'Navigation remains reachable at touch size');}
        for(const model of await slide(page).locator('svg,img,canvas').all())if(await model.isVisible()){const r=await model.boundingBox();assert.ok(r.width>0&&r.height>0,'Visible model has real dimensions');}
      }
      await snap(page,id+'-independent');
      await slide(page).evaluate(el=>{el.scrollTop=el.scrollHeight;});
      const bounds=await slide(page).boundingBox(),bar=await page.locator('.controls').boundingBox();
      assert.ok(bounds.y+bounds.height<=bar.y+1,'Lesson scroll area ends above the fixed navigation');
      await snap(page,id+'-independent-end');
    });
    if(!responsive)await measured(id+'/three-real-print-selections',async()=>{
      await move(page,0);
      for(const level of ['supported','standard','stretch']){
        const beforePrint=await page.evaluate(()=>window.__printRequests);
        await slide(page).locator('button[onclick="printPack(\''+level+'\')"]').click();
        assert.equal(await page.evaluate(()=>window.__printRequests),beforePrint+1);
        await page.emulateMedia({media:'print'});await selectedPrint(page,level);
        if(t.workshopHeading)assert.ok((await page.locator('#print-worksheet-'+level).innerText()).includes(t.workshopHeading));
        if(t.printRepresentative){const file=id+'-'+level+'.pdf';await page.pdf({path:path.join(out,file),format:'A4',printBackground:true});report.pdfs.push({file,lesson:t.path,level,requiredText:t.workshopHeading||t.printRequiredText});}
        await page.emulateMedia({media:'screen'});
      }
    });
    await measured(id+'/no-runtime-or-unreviewed-resource-errors',async()=>{
      assert.equal(report.errors.length,before.errors);assert.equal(report.missingLocal.length,before.missing);assert.equal(report.external.length,before.external);
    });
    report.routes.push({file:t.path,viewport,result:'PASS'});
  }catch(e){report.routes.push({file:t.path,viewport,result:'FAIL',error:e.message});await snap(page,id+'-failure').catch(()=>{});}
  finally{await context.close();}
}
async function negativeControls(){
  const t=doc.targets.find(t=>t.pathway==='LAUNCH'),context=await browser.newContext();await configure(context);const page=await context.newPage();
  try{
    await measured('negative-controls/source-hash',()=>rejects('Forged hash',async()=>source(path.join(root,t.path),'0'.repeat(64))));
    await load(page,t);await page.locator('.slide.active h1').evaluate(n=>n.remove());
    await measured('negative-controls/missing-title',()=>rejects('Missing title',()=>title(page)));
    await load(page,t);await page.locator('.slide').nth(1).evaluate(n=>n.dataset.timer='41');
    await measured('negative-controls/41-minute-stage',()=>rejects('Wrong period sum',()=>minutes(page,t)));
    await load(page,t);await move(page,await minutes(page,t));await page.locator('#auto-timer').evaluate(n=>n.style.display='flex');
    await measured('negative-controls/two-visible-clocks',()=>rejects('Competing clocks',()=>clock(page)));
    await load(page,t);await slide(page).locator('button[onclick="printPack(\'standard\')"]').click();await page.emulateMedia({media:'print'});
    await measured('negative-controls/wrong-print-tier',()=>rejects('Wrong print selection',()=>selectedPrint(page,'supported')));
    const two=doc.targets.find(t=>t.sessionCount===2);await load(page,two);const index=await minutes(page,two);
    await page.locator('.slide').nth(index-1).locator('.period-break').evaluate(n=>n.remove());
    await measured('negative-controls/missing-period-stop',()=>rejects('Missing period stop',()=>periodBoundary(page,two,index)));
  }finally{await context.close();}
}
(async()=>{
  try{
    browser=await chromium.launch({headless:true,channel:args.channel||(process.env.CI?'chrome':undefined)});
    await negativeControls();
    for(const t of doc.targets)await exercise(t);
    for(const t of doc.targets.filter(t=>t.responsiveRepresentative))for(const viewport of [{width:390,height:844},{width:840,height:720}])await exercise(t,viewport,true);
    assert.ok(report.routes.every(r=>r.result==='PASS'),'One or more authored routes failed');report.result='PASS';
  }catch(e){report.result='FAIL';report.error=e.stack;process.exitCode=1;}
  finally{if(browser)await browser.close();report.finishedAt=new Date().toISOString();fs.writeFileSync(path.join(out,'science-browser.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({result:report.result,cases:report.cases.length,passed:report.cases.filter(c=>c.passed).length,routes:report.routes.length,pdfs:report.pdfs.length,error:report.error}));}
})();
