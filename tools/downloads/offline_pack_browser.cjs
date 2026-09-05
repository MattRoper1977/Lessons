/* Real extracted-file acceptance. No local server, request fulfilment or fake
 * lesson content. Install playwright; use installed Chrome in CI.
 * node offline_pack_browser.cjs --manifest manifest.json --packs-dir extracted
 *   --report acceptance.json [--channel chrome]
 */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {pathToFileURL,fileURLToPath}=require('node:url');
const {chromium}=require('playwright');
const args={};
for(let i=2;i<process.argv.length;i+=2){
  assert.ok(['--manifest','--packs-dir','--report','--channel','--artifacts'].includes(process.argv[i]),'Unknown argument');
  assert.ok(process.argv[i+1],'Missing argument value');args[process.argv[i].slice(2)]=process.argv[i+1];
}
for(const key of ['manifest','packs-dir','report'])assert.ok(args[key],'Required: --'+key);
const manifest=JSON.parse(fs.readFileSync(args.manifest,'utf8'));
assert.equal(manifest.schema,'lesson-offline-browser-manifest-v1');
assert.equal(manifest.packs.length,12,'The release gate covers twelve explicit packs');
const base=path.resolve(args['packs-dir']);
if(args.artifacts)fs.mkdirSync(args.artifacts,{recursive:true});
function inside(root,member){
  assert.ok(typeof member==='string' && !path.isAbsolute(member),'Relative member required');
  const target=path.resolve(root,member);
  assert.ok(target.startsWith(root+path.sep),'Member escaped extraction directory');
  assert.ok(fs.existsSync(target)&&fs.statSync(target).isFile(),'Missing extracted member: '+member);
  return target;
}
const report={schema:'lesson-offline-browser-acceptance-v1',status:'RUNNING',
  browser:'Chromium via Playwright; file:// with offline network context',
  scope:manifest.scope,packagedLessonFiles:manifest.packagedLessonFiles,
  packs:[],representatives:[],guidanceNavigation:[],negativeControls:[],failures:[],
  limitations:['Representative interactions only; not every lesson activity tested.',
    'Print invocation and print-media contents checked; no physical printer or page-pagination claim.',
    'Microphone permission/capture and external video sites are not exercised.']};
const nextSelector='button[data-nav="next"], button#next, button[onclick="nextSlide()"]';
const prevSelector='button[data-nav="previous"], button#prev, button[onclick="prevSlide()"]';
function clean(text){return String(text||'').replace(/\s+/g,' ').trim();}
async function active(page){return page.locator('.slide').evaluateAll(nodes=>{
  const all=nodes.map((n,index)=>({index,active:n.classList.contains('active'),
    visible:getComputedStyle(n).display!=='none'&&n.getBoundingClientRect().width>0,
    title:(n.querySelector('h1,h2,h3')?.textContent||n.dataset.title||'').replace(/\s+/g,' ').trim()}));
  return all.filter(x=>x.active&&x.visible);
});}
async function stage(page){const a=await active(page);assert.equal(a.length,1,'Exactly one active visible teaching slide');assert.ok(a[0].title,'Teaching slide heading');return a[0];}
async function findVisible(page,selector){const loc=page.locator(selector);for(let i=0;i<await loc.count();i++)if(await loc.nth(i).isVisible())return loc.nth(i);return null;}
async function advanceTo(page,selector){
  const count=await page.locator('.slide').count();
  for(let i=0;i<count;i++){
    const button=await findVisible(page,selector);if(button)return button;
    const next=await findVisible(page,nextSelector);assert.ok(next,'Actual next control required');await next.click();
  }throw Error('No reachable visible control: '+selector);
}
async function clickFileLink(page,absolute){
  const target=pathToFileURL(absolute).href;
  const links=page.locator('a[href]');
  for(let i=0;i<await links.count();i++){
    const link=links.nth(i);if(await link.evaluate(n=>n.href)===target){
      await Promise.all([page.waitForURL(target),link.click()]);return;
    }
  }throw Error('No visible pack link to '+path.basename(absolute));
}
async function inspectPrint(page,row){
  const specific='button[onclick="printPack(\'supported\')"], button[data-tool="2"]:has-text("print"), button#printCurrent, button[data-print-tier="Supported"]';
  const has=await page.locator(specific).count();
  if(has){
    const button=await advanceTo(page,specific);
    const before=await page.evaluate(()=>window.__offlinePrintCalls);
    await button.click();
    await page.waitForFunction(n=>window.__offlinePrintCalls>n,before);
    row.printButtonInvoked=true;
  }
  await page.emulateMedia({media:'print'});
  const printed=await page.locator('#print-area,.print-pack,.printpack').evaluateAll(nodes=>nodes.map(n=>({
    visible:getComputedStyle(n).display!=='none'&&n.getBoundingClientRect().width>0,
    text:(n.innerText||'').replace(/\s+/g,' ').trim(),headings:n.querySelectorAll('h1,h2,h3').length})));
  assert.ok(printed.some(n=>n.visible&&n.text.length>200&&n.headings>=2),'Printable learning content must be present and visible');
  row.printMediaContents=true;
  await page.emulateMedia({media:'screen'});
}
async function inspectHud(page,row){
  await page.locator('#mbmhud-pill').waitFor({state:'visible'});
  await page.locator('#mbmhud-pill').click();
  await page.locator('#mbmhud-dock').waitFor({state:'visible'});
  await page.locator('#mbmhud-dock button[data-min="1"]').click();
  assert.equal(await page.locator('#mbmhud-time').textContent(),'1:00');
  await page.waitForFunction(()=>document.querySelector('#mbmhud-time')?.textContent==='0:59',null,{timeout:3500});
  await page.locator('#mbmhud-tpause').click();
  const frozen=await page.locator('#mbmhud-time').textContent();
  await page.waitForTimeout(1100);
  assert.equal(await page.locator('#mbmhud-time').textContent(),frozen,'HUD pause freezes displayed timer');
  await page.locator('#mbmhud-tstop').click();
  await page.locator('#mbmhud-calmbtn').click();
  await page.locator('#mbmhud-calm').waitFor({state:'visible'});
  assert.ok(await page.locator('#mbmhud-calmtext').isVisible());
  await page.locator('#mbmhud-calmexit').click();
  await page.locator('#mbmhud-calm').waitFor({state:'hidden'});
  const close=page.locator('#mbmhud-close');if(await close.isVisible())await close.click();
  row.hud={timerStartsAndTicks:true,pauseFreezes:true,calmOpensAndReturns:true};
}
async function inspectAward(page,row,root,slotsRequired){
  assert.equal(await page.locator('main.deck>.slide').count(),9,'Award lesson has nine teaching stages');
  await page.locator('[data-tool="1"]').click();
  await page.locator('#taOverlay').waitFor({state:'visible'});
  assert.ok(clean(await page.locator('#taOverlay').innerText()).length>80,'Teacher guidance contains actual text');
  if(slotsRequired){
    const input=page.locator('#award-slot-panel input[type="file"]');
    assert.ok(await input.isVisible(),'Staff can reach the offline slot file selector');
    await input.setInputFiles(inside(root,'tools/artsaward/SLOTS.json'));
    await page.waitForFunction(()=>document.querySelector('#award-slot-panel [role="status"]')?.textContent.includes('Complete the actual experience'));
    const status=await page.locator('#award-slot-panel [role="status"]').innerText();
    assert.match(status,/Unconfirmed.*preparation only/i);
    row.offlineSlots={fileSelected:true,unconfirmedPreserved:true};
  }
  await page.locator('#taOverlay [data-close-overlay]').click();
  await page.locator('#taOverlay').waitFor({state:'hidden'});
  const calm=page.locator('[data-tool="3"]');
  assert.equal(await calm.getAttribute('aria-pressed'),'false');await calm.click();
  assert.equal(await calm.getAttribute('aria-pressed'),'true');await calm.click();
  assert.equal(await calm.getAttribute('aria-pressed'),'false');
  row.awardTeacherTools=true;row.awardCalmToggle=true;
}

(async()=>{
  let browser;
  try{
    browser=await chromium.launch({headless:true,channel:args.channel||(process.env.CI?'chrome':undefined)});
    for(const pack of manifest.packs){
      const root=path.resolve(base,pack.root);assert.ok(root.startsWith(base+path.sep));
      const context=await browser.newContext({offline:true,serviceWorkers:'block',viewport:{width:1280,height:800},reducedMotion:'reduce'});
      const observations={pageErrors:[],failedRequests:[],httpErrors:[],networkAttempts:[]};
      await context.route('**/*',route=>/^https?:/.test(route.request().url())?route.abort('internetdisconnected'):route.continue());
      const page=await context.newPage();page.setDefaultTimeout(12000);
      page.on('pageerror',e=>observations.pageErrors.push(e.message));
      page.on('request',r=>{if(/^https?:/.test(r.url()))observations.networkAttempts.push({url:r.url(),type:r.resourceType()});});
      page.on('requestfailed',r=>observations.failedRequests.push({url:r.url(),failure:r.failure()?.errorText,type:r.resourceType()}));
      page.on('response',r=>{if(r.status()>=400)observations.httpErrors.push({url:r.url(),status:r.status()});});
      await page.addInitScript(()=>{window.__offlinePrintCalls=0;window.print=()=>{window.__offlinePrintCalls++;};});
      try{
        await page.goto(pathToFileURL(inside(root,pack.entry)).href);
        assert.ok(clean(await page.locator('h1').first().innerText()).length>5);
        if(args.artifacts)await page.screenshot({path:path.join(args.artifacts,pack.id+'-start.png'),fullPage:true});
        const packRow={id:pack.id,zipSha256:pack.zipSha256,declaredLessonCount:pack.declaredLessonCount,entryOpened:true};
        for(const member of pack.lessons)inside(root,member);
        if(pack.kind==='award'){
          await clickFileLink(page,inside(root,pack.packStart));
          const targets=await page.locator('a[href]').evaluateAll(nodes=>nodes.map(a=>a.href));
          const expected=pack.lessons.map(m=>pathToFileURL(inside(root,m)).href);
          const actual=targets.filter(h=>expected.includes(h));
          assert.equal(actual.length,14,'Published award pack start exposes exactly fourteen lesson links');
          assert.equal(new Set(actual).size,14);assert.deepEqual(actual,expected,'Award lesson order matches explicit definition');
          packRow.actualAwardLinks=14;
        }
        await clickFileLink(page,inside(root,pack.firstLesson));
        packRow.packToLessonClick=true;
        const samples=[pack.firstLesson,...(pack.laterSample?[pack.laterSample]:[])];
        for(let sample=0;sample<samples.length;sample++){
          const member=samples[sample];
          if(sample){
            await page.goto(pathToFileURL(inside(root,pack.packStart)).href);
            await clickFileLink(page,inside(root,member));
          }
          await page.locator('.slide.active').waitFor({state:'visible'});
          const row={packId:pack.id,member,pathway:pack.pathway,role:pack.expectHud?'original-science':pack.kind==='award'?(sample?'award-later-slot-reader':'award-first'):'later-science'};
          const initial=await stage(page);
          await (await findVisible(page,nextSelector)).click();
          const second=await stage(page);assert.notEqual(second.index,initial.index,'Next changes actual slide');
          await (await findVisible(page,prevSelector)).click();assert.equal((await stage(page)).index,initial.index,'Previous restores slide');
          row.mouseStageNavigation=true;
          const brokenImages=await page.locator('img').evaluateAll(nodes=>nodes.filter(n=>n.getAttribute('src')&&(!n.complete||n.naturalWidth===0)).map(n=>n.getAttribute('src')));
          assert.deepEqual(brokenImages,[],'No broken local image');
          if(pack.expectHud)await inspectHud(page,row);
          if(pack.kind==='award')await inspectAward(page,row,root,Boolean(sample));
          await inspectPrint(page,row);
          const home=await findVisible(page,pack.expectHud?'#mbmhud-back':'a.mbmhome');
          assert.ok(home,'Reachable lesson home control');
          const href=await home.getAttribute('href');
          const resolved=new URL(href,page.url());assert.equal(resolved.protocol,'file:','Offline home stays local');
          const target=fileURLToPath(resolved);assert.ok(target.startsWith(root+path.sep)&&fs.existsSync(target));
          await Promise.all([page.waitForURL(resolved.href),home.click()]);
          assert.ok(clean(await page.locator('h1').first().innerText()).length>5);
          row.lessonToPackHomeClick=true;report.representatives.push(row);
        }
        // The first real run found Guidance covering Next. Exercise every
        // repaired source at desktop and touch width, using real pointer clicks.
        for(const member of pack.guidanceNavigationMembers){
          for(const viewport of [{width:1280,height:800},{width:390,height:844}]){
            await page.setViewportSize(viewport);
            await page.goto(pathToFileURL(inside(root,member)).href);
            const initial=await stage(page);
            const guidance=page.locator('.controls .left .n6m-guide-btn');
            assert.equal(await guidance.count(),1,'Guidance shares the actual toolbar');
            assert.ok((await guidance.boundingBox()).height>=44,'Guidance has a 44px target');
            const before=await guidance.getAttribute('aria-pressed');
            await guidance.click();
            assert.notEqual(await guidance.getAttribute('aria-pressed'),before,'Guidance opens with an actual click');
            await guidance.click();
            assert.equal(await guidance.getAttribute('aria-pressed'),before,'Guidance returns to its prior state');
            await (await findVisible(page,nextSelector)).click();
            assert.notEqual((await stage(page)).index,initial.index,'Guidance must not obstruct Next');
            await (await findVisible(page,prevSelector)).click();
            assert.equal((await stage(page)).index,initial.index,'Previous remains reachable');
            report.guidanceNavigation.push({packId:pack.id,member,viewport,actualClicks:true});
            if(args.artifacts&&member===pack.guidanceNavigationMembers[0])
              await page.screenshot({path:path.join(args.artifacts,pack.id+'-guidance-'+viewport.width+'.png'),fullPage:true});
          }
        }
        await page.setViewportSize({width:1280,height:800});
        assert.deepEqual(observations.pageErrors,[],'No unhandled page errors');
        assert.deepEqual(observations.failedRequests,[],'No failed local runtime request');
        assert.deepEqual(observations.httpErrors,[],'No HTTP error response');
        assert.deepEqual(observations.networkAttempts,[],'Lesson UI does not attempt network access');
        packRow.runtime=observations;report.packs.push(packRow);
        if(report.negativeControls.length===0){
          const before=observations.failedRequests.length;
          await page.evaluate(()=>{const s=document.createElement('script');s.src='./missing-offline-control.js';document.body.appendChild(s);});
          const deadline=Date.now()+4000;
          while(observations.failedRequests.length===before&&Date.now()<deadline)await page.waitForTimeout(50);
          assert.ok(observations.failedRequests.slice(before).some(r=>r.url.endsWith('/missing-offline-control.js')),'Planted missing local script must be observed');
          report.negativeControls.push({id:'missing-local-runtime-is-detected',pass:true});
          // The main row was accepted before this deliberate failure; do not
          // quietly erase the evidence or count it as a product failure.
          packRow.runtime={...observations,failedRequests:observations.failedRequests.slice(0,before)};
        }
      }catch(error){report.failures.push({packId:pack.id,message:error.message,runtime:observations});}
      finally{await context.close();}
    }
    assert.equal(report.packs.length,12,'All twelve packs must pass');
    assert.deepEqual(report.failures,[],'No representative or negative-control failure may be hidden');
    assert.equal(report.representatives.length,manifest.interactiveRepresentativeCount);
    assert.equal(report.representatives.length,15,'Explicit representative coverage');
    assert.equal(manifest.guidanceNavigationRoutes,47);
    assert.equal(report.guidanceNavigation.length,94,'All repaired Guidance routes at both viewports');
    assert.equal(report.negativeControls.length,1);
    report.status='PASS';
  }catch(error){report.status='FAIL';report.failures.push({message:error.message});}
  finally{
    if(browser)await browser.close();
    fs.mkdirSync(path.dirname(path.resolve(args.report)),{recursive:true});
    fs.writeFileSync(args.report,JSON.stringify(report,null,2)+'\n');
    console.log(JSON.stringify({status:report.status,packsPassed:report.packs.length,representatives:report.representatives.length,failures:report.failures.length}));
    if(report.status!=='PASS')process.exitCode=1;
  }
})().catch(error=>{console.error(error);process.exitCode=1;});
