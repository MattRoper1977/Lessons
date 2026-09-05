/* Supplemental GROW acceptance; the existing CI harness owns the browser,
 * reviewed routing, original lesson checks, errors and artifact directory.
 * Never launches its own browser. Video outage tests are not playback claims.
 */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const digest=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
const origin='http://science-original.test';
const firstSentence=text=>text.match(/^[\s\S]*?[.!?](?:\s|$)/)?.[0].trim()||text;

async function run({browser,root,out,configure,measured,report}){
  const targets=JSON.parse(fs.readFileSync(path.join(root,'tools/grow_resources/BROWSER_TARGETS.json'),'utf8'));
  const content=JSON.parse(fs.readFileSync(path.join(root,'tools/grow_resources/CONTENT.json'),'utf8'));
  const result={schema:'grow-resource-browser-review-v1',inputs:targets,scope:'Rendered desktop and phone checks using the existing reviewed CI browser. Videos are deliberately blocked in outage cases; no playback claim. PDF page-image review remains a human/agent release step.',cases:[],routes:[],pdfs:[],images:[]};
  const check=async(name,fn)=>{try{await measured('grow-resources/'+name,fn);result.cases.push({name,passed:true});}catch(e){result.cases.push({name,passed:false,error:e.message});throw e;}};
  const snapshot=async(page,name)=>{const file=name+'.png';await page.screenshot({path:path.join(out,file),fullPage:true});result.images.push(file);};
  const reject=async(fn)=>{let fired=false;try{await fn();}catch(e){fired=true;}assert.ok(fired,'The planted defect must be detected');};
  const noOverflow=async(page)=>{const size=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));assert.ok(size.scroll<=size.width+2,'No document horizontal overflow');};
  const loadedImage=async(locator)=>{await locator.scrollIntoViewIfNeeded();await locator.waitFor({state:'visible'});await locator.evaluate(image=>image.decode());assert.equal(await locator.evaluate(image=>image.complete&&image.naturalWidth>0),true);};
  const targetSize=async(locator,viewport)=>{await locator.scrollIntoViewIfNeeded();const box=await locator.boundingBox();assert.ok(box&&box.width>=43.5&&box.height>=43.5&&box.x>=0&&box.x+box.width<=viewport.width+1,'Touch target is at least44px and stays on screen');};
  const navigationClear=async(page)=>{
    await page.locator('#mbmhud-pill').waitFor({state:'visible'});
    const overlaps=await page.evaluate(()=>{
      const visible=n=>{const r=n.getBoundingClientRect();return r.width&&r.height&&getComputedStyle(n).visibility!=='hidden';};
      const hud=[...document.querySelectorAll('#mbmhud-back,#mbmhud-home,#mbmhud-pill')].filter(visible);
      return [...document.querySelectorAll('.controls button')].filter(visible).flatMap(button=>hud.flatMap(item=>{
        const a=button.getBoundingClientRect(),b=item.getBoundingClientRect();
        return Math.min(a.right,b.right)>Math.max(a.left,b.left)&&Math.min(a.bottom,b.bottom)>Math.max(a.top,b.top)?[{button:button.textContent.trim(),hud:item.id}]:[];
      }));
    });
    assert.deepEqual(overlaps,[],'Native lesson controls must not overlap the shared HUD');
  };
  const verifyInputs=()=>{
    assert.equal(targets.schema,'grow-resource-browser-targets-v1');
    assert.equal(targets.pages.length,10);assert.equal(targets.lessons.length,5);
    assert.deepEqual(targets.pages.map(p=>p.id).sort(),content.map(c=>c.id).sort());
    for(const row of targets.files)assert.equal(digest(fs.readFileSync(path.join(root,row.path))),row.sha256,'Source identity: '+row.path);
  };
  try{
    await check('input-identities',async()=>verifyInputs());
    const pairPaths=new Set(targets.lessons.map(x=>x.path));
    assert.equal(pairPaths.size,5);assert.ok(content.every(c=>pairPaths.has(c.online_path)));
    for(const viewport of targets.viewports){
      const mobile=viewport.width<600;
      for(const target of targets.lessons){
        const id=path.basename(target.path,'.html')+'-grow-links-'+viewport.width;
        const context=await browser.newContext({viewport,hasTouch:mobile,reducedMotion:'reduce'});await configure(context);const page=await context.newPage();page.setDefaultTimeout(10000);
        const before={errors:report.errors.length,missing:report.missingLocal.length,external:report.external.length};
        try{
          await check(id,async()=>{
            const url=origin+'/Lessons/'+target.path;
            for(const period of ['A','B']){
              await page.goto(url,{waitUntil:'domcontentloaded'});
              const expected=content.find(c=>c.online_path===target.path&&c.period===period);assert.ok(expected);
              const link=page.locator('.slide.active a[href="resources/'+expected.id+'.html"]');assert.equal(await link.count(),1);
              await navigationClear(page);
              if(mobile)await targetSize(link,viewport);
              else{await link.focus();assert.equal(await link.evaluate(n=>document.activeElement===n),true);}
              await snapshot(page,id+'-'+period);
              if(mobile)await link.tap();else await link.press('Enter');
              await page.waitForURL(origin+'/Lessons/Science_Teesside/Grow/resources/'+expected.id+'.html');
              assert.equal((await page.locator('.hero h1').innerText()).trim(),expected.title);
              await page.getByRole('link',{name:'Return to the lesson',exact:true}).click();
              await page.waitForURL(url);assert.equal(await page.locator('.slide.active').getAttribute('data-title'),'Title');
            }
            await noOverflow(page);
            assert.equal(report.errors.length,before.errors);assert.equal(report.missingLocal.length,before.missing);assert.equal(report.external.length,before.external);
          });
          result.routes.push({file:target.path,viewport:viewport.width,result:'PASS'});
        }catch(e){result.routes.push({file:target.path,viewport:viewport.width,result:'FAIL',error:e.message});await snapshot(page,id+'-failure').catch(()=>{});}
        finally{await context.close();}
      }
      for(const target of targets.pages){
        const c=content.find(c=>c.id===target.id),id=c.id+'-resource-'+viewport.width;
        const context=await browser.newContext({viewport,hasTouch:mobile,reducedMotion:'reduce'});await configure(context);const page=await context.newPage();page.setDefaultTimeout(10000);
        const before={errors:report.errors.length,missing:report.missingLocal.length,external:report.external.length};
        const url=origin+'/Lessons/'+target.path;
        try{
          await check(id+'/screen-model-and-navigation',async()=>{
            await page.goto(url,{waitUntil:'domcontentloaded'});await page.locator('html.js').waitFor();
            assert.equal((await page.locator('.hero h1').innerText()).trim(),c.title);
            assert.equal(await page.locator('.period-nav [aria-current="page"]').getAttribute('href'),c.id+'.html');
            assert.equal(await page.locator('.print-title').isVisible(),false);
            await noOverflow(page);await loadedImage(page.locator('.model img'));
            for(const link of await page.locator('.period-nav a,.downloads a').all())if(mobile)await targetSize(link,viewport);
            const pdf=await page.locator('.downloads a').getAttribute('href');assert.equal(pdf,c.worksheet_pdf);
            assert.ok(fs.statSync(path.join(root,'Science_Teesside/Grow/resources',pdf)).size>0);
            await snapshot(page,id+'-screen');
          });
          await check(id+'/keyboard-first-reason-and-answer',async()=>{
            const first=page.locator('.task textarea').nth(0),repair=page.locator('.task textarea').nth(1),answer=page.locator('.task details.answer');
            assert.equal(await answer.getAttribute('open'),null);
            await first.fill('Our first explanation');await first.press('Tab');
            assert.equal(await answer.locator(':scope > summary').evaluate(n=>n===document.activeElement),true,'Tab reaches the native answer disclosure');
            await page.keyboard.press('Enter');assert.equal(await answer.locator('p').isVisible(),true);
            assert.equal((await answer.locator('p').innerText()).trim(),c.activity.answer);
            await page.keyboard.press('Tab');assert.equal(await repair.evaluate(n=>n===document.activeElement),true,'Tab continues to the repaired explanation');
            await repair.fill('Keep the evidence and improve one reason');
            assert.equal(await first.inputValue(),'Our first explanation');
            await answer.locator(':scope > summary').press('Enter');assert.equal(await answer.getAttribute('open'),null);
          });
          await check(id+'/video-outage-and-matched-still',async()=>{
            const fallback=page.locator('.media img');await loadedImage(fallback);assert.equal(await fallback.getAttribute('src'),c.video.fallback_image);
            const mediaText=await page.locator('.media').innerText();assert.ok(mediaText.includes(c.video.prompt));assert.ok(mediaText.includes(c.video.fallback_text));
            if(c.week===7)assert.equal(await fallback.getAttribute('src'),'assets/Moon_rotation_fallback.png');
            if(c.video.local_file){
              const video=page.locator('video');assert.equal(await video.getAttribute('preload'),'none');assert.equal(await video.getAttribute('autoplay'),null);assert.notEqual(await video.getAttribute('controls'),null);
              const fixtureUrl=new URL(c.video.local_file,url);
              fixtureUrl.searchParams.set('mbm-outage',String(viewport.width));
              const videoUrl=fixtureUrl.href;let blocked=0;
              await page.route(videoUrl,async route=>{blocked++;await route.abort('failed');});
              // A failed child <source> emits a request/source error without
              // consistently setting HTMLMediaElement.error. Measure the
              // actual blocked request instead of that optional video state.
              const failedRequest=page.waitForEvent('requestfailed',{predicate:request=>request.url()===videoUrl});
              // Isolate the deliberately failed load from a pending media
              // request that load() may cancel itself on a phone viewport.
              await video.evaluate((v,src)=>{v.querySelector('source').src=src;v.preload='auto';v.load();},videoUrl);
              const failed=await failedRequest;
              assert.ok(failed.failure()?.errorText,'The browser reports the failed media request');
              assert.ok(blocked>0,'The local-media failure fixture actually ran');
              assert.equal(await video.evaluate(v=>v.readyState),0,'The blocked clip supplies no playable media');
              assert.equal(await fallback.isVisible(),true);assert.ok((await page.locator('.media').innerText()).includes(c.video.fallback_text));
            }else{
              const link=page.locator('.media a[target="_blank"]');assert.equal(await link.getAttribute('href'),c.video.url);assert.ok((await link.getAttribute('rel')).includes('noopener'));
            }
            await snapshot(page,id+'-video-fallback');
          });
          if(!mobile)await check(id+'/pupil-and-answer-print',async()=>{
            // Fresh page removes the deliberately broken media fixture from
            // this print case; the routed video remains preload=none.
            await page.goto(url,{waitUntil:'domcontentloaded'});await page.locator('html.js').waitFor();
            const answer=page.locator('.task details.answer'),first=page.locator('.task textarea').first();
            await first.fill('Our first explanation stays available');
            const printBefore=await page.evaluate(()=>window.__printRequests);await page.locator('[data-print-task]').click();assert.equal(await page.evaluate(()=>window.__printRequests),printBefore+1);
            for(const includeAnswers of [false,true]){
              await page.locator('[data-print-answers]').setChecked(includeAnswers);
              await page.evaluate(()=>window.dispatchEvent(new Event('beforeprint')));await page.emulateMedia({media:'print'});
              assert.equal(await page.locator('header').isVisible(),false);assert.equal(await page.locator('.print-actions').isVisible(),false);assert.equal(await page.locator('.media').isVisible(),false);assert.equal(await page.locator('.print-title').isVisible(),true);
              assert.equal(await answer.locator('p').isVisible(),includeAnswers,'Answer visibility follows the explicit print choice');
              // Complete the explicit DOM-state probe before Chrome's own print
              // lifecycle fires for the PDF export, avoiding nested beforeprint.
              await page.evaluate(()=>window.dispatchEvent(new Event('afterprint')));
              const file=c.id+'-'+(includeAnswers?'answer-key':'pupil-task')+'.pdf';
              await page.pdf({path:path.join(out,file),format:'A4',printBackground:true});
              const record={file,lesson:target.path,level:includeAnswers?'grow-answer-key':'grow-pupil-task',requiredText:c.activity.title};
              report.pdfs.push(record);result.pdfs.push({...record,answerFragment:firstSentence(c.activity.answer),includeAnswers});
              await page.emulateMedia({media:'screen'});await page.evaluate(()=>window.dispatchEvent(new Event('afterprint')));
              assert.equal(await answer.getAttribute('open'),null,'Printing restores the original closed answer state');assert.equal(await first.inputValue(),'Our first explanation stays available');
            }
          });
          await check(id+'/no-script-fallback',async()=>{
            const noJs=await browser.newContext({viewport,javaScriptEnabled:false,reducedMotion:'reduce'});await configure(noJs);const plain=await noJs.newPage();plain.setDefaultTimeout(10000);
            try{await plain.goto(url,{waitUntil:'domcontentloaded'});assert.equal(await plain.locator('.js-only').isVisible(),false);const answer=plain.locator('.task details.answer');await answer.locator(':scope > summary').click();assert.equal(await answer.locator('p').isVisible(),true);await loadedImage(plain.locator('.media img'));assert.equal(await plain.locator('.downloads a').getAttribute('href'),c.worksheet_pdf);}
            finally{await noJs.close();}
          });
          await check(id+'/no-unexpected-resource-errors',async()=>{assert.equal(report.errors.length,before.errors);assert.equal(report.missingLocal.length,before.missing);assert.equal(report.external.length,before.external);});
          result.routes.push({file:target.path,viewport:viewport.width,result:'PASS'});
        }catch(e){result.routes.push({file:target.path,viewport:viewport.width,result:'FAIL',error:e.message});await snapshot(page,id+'-failure').catch(()=>{});}
        finally{await context.close();}
      }
    }
    for(const target of targets.lessons){
      const context=await browser.newContext({viewport:{width:840,height:720},hasTouch:true,reducedMotion:'reduce'});await configure(context);const page=await context.newPage();
      try{await check(path.basename(target.path,'.html')+'/tablet-hud-clearance',async()=>{
        await page.goto(origin+'/Lessons/'+target.path,{waitUntil:'domcontentloaded'});
        await navigationClear(page);
        await page.locator('.controls button[onclick="nextSlide()"]').click();
        await navigationClear(page);
        await snapshot(page,path.basename(target.path,'.html')+'-grow-navigation-840');
      });}finally{await context.close();}
    }
    const collisionContext=await browser.newContext({viewport:{width:390,height:844},reducedMotion:'reduce'});await configure(collisionContext);const collisionPage=await collisionContext.newPage();
    try{
      await collisionPage.goto(origin+'/Lessons/'+targets.lessons[0].path,{waitUntil:'domcontentloaded'});
      await navigationClear(collisionPage);
      await collisionPage.addStyleTag({content:'.controls{bottom:10px!important}'});
      await check('negative-controls/hud-overlap',()=>reject(()=>navigationClear(collisionPage)));
    }finally{await collisionContext.close();}
    const controlContext=await browser.newContext();await configure(controlContext);const page=await controlContext.newPage();
    try{
      await check('negative-controls/wrong-source-hash',()=>reject(async()=>assert.equal(digest(fs.readFileSync(path.join(root,targets.pages[0].path))),'0'.repeat(64))));
      await page.goto(origin+'/Lessons/'+targets.pages[0].path);await page.locator('.media img').evaluate(n=>n.remove());
      await check('negative-controls/missing-video-fallback',()=>reject(async()=>assert.equal(await page.locator('.media img').count(),1)));
      await page.goto(origin+'/Lessons/'+targets.pages[0].path);await page.locator('.task details.answer').evaluate(n=>n.open=true);
      await check('negative-controls/premature-answer',()=>reject(async()=>assert.equal(await page.locator('.task details.answer').getAttribute('open'),null)));
    }finally{await controlContext.close();}
    assert.ok(result.routes.every(r=>r.result==='PASS'),'One or more supplemental GROW routes failed');result.result='PASS';
  }catch(e){result.result='FAIL';result.error=e.message;throw e;}
  finally{fs.writeFileSync(path.join(out,'grow-resource-browser.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({scope:'grow-resources',result:result.result,cases:result.cases.length,passed:result.cases.filter(c=>c.passed).length,routes:result.routes.length,pdfs:result.pdfs.length,failedCases:result.cases.filter(c=>!c.passed),failedRoutes:result.routes.filter(r=>r.result!=='PASS')}));}
}
module.exports={run};
