/* Additional acceptance for the real Science resource controls.
 * Called by the existing original-Science CI harness and its reviewed router.
 * Optional video transport is a fixture; this is not a playback claim.
 */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');

async function exercise({page,root,out,measured,move,current,id,viewport,responsive,report,t}){
  const content=JSON.parse(fs.readFileSync(path.join(root,'tools/science_pack/RESOURCE_CONTENT.json'),'utf8'));
  const lesson=content.find(c=>c.online_path===t.path);
  assert.ok(lesson,'Every original LAUNCH route has a declared resource lesson');
  const dialog=page.locator('#mbm-science-pack');
  let opener,resourceUrl;
  const navigationClear=async()=>{
    await page.locator('#mbmhud-pill').waitFor({state:'visible'});
    const overlaps=await page.evaluate(()=>{
      const visible=n=>{const r=n.getBoundingClientRect();return r.width&&r.height&&getComputedStyle(n).visibility!=='hidden';};
      const hud=[...document.querySelectorAll('#mbmhud-back,#mbmhud-home,#mbmhud-pill')].filter(visible);
      return [...document.querySelectorAll('.controls button')].filter(visible).flatMap(button=>hud.flatMap(item=>{
        const a=button.getBoundingClientRect(),b=item.getBoundingClientRect();
        return Math.min(a.right,b.right)>Math.max(a.left,b.left)&&Math.min(a.bottom,b.bottom)>Math.max(a.top,b.top)?[{button:button.textContent.trim(),hud:item.id}]:[];
      }));
    });
    assert.deepEqual(overlaps,[],'Native stage controls must remain separate from shared tools');
  };
  await measured(id+'/native-navigation-hud-clearance',navigationClear);
  await measured(id+'/resources-open-focus-and-reason',async()=>{
    await move(page,0);
    opener=page.locator('.slide.active [data-open-science-pack]').first();
    assert.equal(await opener.count(),1);
    resourceUrl=new URL(await opener.getAttribute('href'),page.url()).href;
    assert.equal(await page.locator('iframe').count(),0,'No unsolicited video frame');
    if(responsive)await opener.tap();else await opener.click();
    assert.equal(await dialog.isVisible(),true);
    assert.equal(await dialog.evaluate(el=>el.contains(document.activeElement)),true);
    const stage=await current(page);
    const first=dialog.locator('textarea').first();
    await first.fill('Keep our first reason');
    await first.press('Space');await first.press('ArrowRight');
    assert.equal(await current(page),stage,'Resource typing cannot advance the lesson');
    const answer=dialog.locator('.mbm-sp-answer');
    assert.equal(await answer.getAttribute('open'),null);
    await answer.locator('summary').click();
    assert.equal(await answer.locator('p').isVisible(),true);
    assert.ok((await answer.locator('p').innerText()).trim().length>15);
    await dialog.locator('textarea').nth(1).fill('Use the evidence in our explanation');
    for(let n=0;n<8;n++){
      await page.keyboard.press('Tab');
      assert.equal(await dialog.evaluate(el=>el.contains(document.activeElement)),true,'Tab stays inside native dialog');
    }
    await page.keyboard.press('Escape');
    assert.equal(await dialog.isVisible(),false);
    assert.equal(await opener.evaluate(el=>document.activeElement===el),true,'Escape returns focus to the trigger');
  });
  await measured(id+'/resources-video-action-and-fallback',async()=>{
    await opener.click();
    assert.ok((await dialog.locator('textarea').first().inputValue()).startsWith('Keep our first reason'));
    assert.equal(await dialog.locator('textarea').nth(1).inputValue(),'Use the evidence in our explanation');
    const section=dialog.locator('.mbm-sp-section').nth(2);
    await section.locator(':scope > summary').click();
    const model=section.locator('img');
    await model.scrollIntoViewIfNeeded();
    assert.equal(await model.isVisible(),true);
    assert.equal(await model.evaluate(n=>n.complete&&n.naturalWidth>0),true,'Embedded no-video model loads');
    assert.equal(await dialog.locator('iframe').count(),0);
    let fixtureRequests=0;
    const handler=async route=>{fixtureRequests++;await route.fulfill({contentType:'text/html',body:'<!doctype html><title>Video transport fixture</title><p>Video playback is outside this acceptance.</p>'});};
    await page.route('https://www.youtube-nocookie.com/**',handler);
    const play=section.locator('[data-play-video]');
    if(responsive)await play.tap();else await play.click();
    const frame=section.locator('iframe');
    await frame.waitFor();
    assert.equal(await frame.getAttribute('src'),'https://www.youtube-nocookie.com/embed/'+lesson.video.id+'?rel=0');
    assert.ok((await frame.getAttribute('title')).includes(lesson.video.title));
    assert.equal(await play.isVisible(),false);
    await dialog.locator('form[method="dialog"] button').click();
    assert.equal(await dialog.isVisible(),false);
    // HTML dispatches the dialog close event as a queued task. Wait for that
    // event's media cleanup, then assert the actual final DOM state.
    await frame.waitFor({state:'detached'});
    assert.equal(await dialog.locator('iframe').count(),0,'Close removes media');
    assert.equal(await play.getAttribute('hidden'),null);
    await page.unroute('https://www.youtube-nocookie.com/**',handler);
    report.resourceVideoFixtures ||= [];
    report.resourceVideoFixtures.push({lesson:lesson.id,viewport:viewport.width,requests:fixtureRequests,scope:'Native button and frame creation only; no video playback'});
  });
  await measured(id+'/resources-layout-print-and-file-fallback',async()=>{
    await page.goto(resourceUrl,{waitUntil:'domcontentloaded'});
    assert.equal(await page.locator('.mbm-sp-page').count(),1);
    await page.locator('#mbmhud-pill').waitFor({state:'visible'});
    for(const tool of await page.locator('#mbmhud-back,#mbmhud-home,#mbmhud-pill').all())
      assert.equal(await tool.evaluate(n=>getComputedStyle(n).position),'static','Standalone shared tools stay after the teaching content');
    assert.equal(await page.getByRole('link',{name:'Return to the lesson',exact:true}).count(),1);
    assert.equal(await page.locator('.mbm-sp-answer').getAttribute('open'),null,'A fresh print route does not expose the answer');
    const size=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));
    assert.ok(size.scroll<=size.width+2,'Resource page stays within the viewport');
    for(const el of await page.locator('.mbm-sp-files a').all()){
      const fileUrl=new URL(await el.getAttribute('href'),resourceUrl);
      const local=path.join(root,decodeURIComponent(fileUrl.pathname.replace(/^\/Lessons\//,'')));
      assert.ok(fs.statSync(local).isFile(),'Printable resource exists');
      if(responsive){const box=await el.boundingBox();assert.ok(box&&box.height>=43.5,'File button is a usable touch target');}
    }
    await page.screenshot({path:path.join(out,id+'-resource-task.png'),fullPage:true});
    await page.emulateMedia({media:'print'});
    assert.equal(await page.locator('nav').isVisible(),false);
    assert.equal(await page.locator('.mbm-sp-files').isVisible(),false);
    assert.equal(await page.locator('.mbm-sp-answer p').isVisible(),false,'Hidden answer remains hidden on paper');
    if(!responsive){
      const file=id+'-resource-task.pdf';
      await page.pdf({path:path.join(out,file),format:'A4',printBackground:true});
      report.pdfs.push({file,lesson:t.path,level:'resource-task',requiredText:lesson.activity.title});
    }
    await page.emulateMedia({media:'screen'});
    const modelSection=page.locator('.mbm-sp-section').nth(1);
    await modelSection.locator(':scope > summary').click();
    const image=modelSection.locator('img');await image.scrollIntoViewIfNeeded();
    assert.equal(await image.evaluate(n=>n.complete&&n.naturalWidth>0),true);
    await page.screenshot({path:path.join(out,id+'-resource-model.png'),fullPage:true});
    await page.goto('http://science-original.test/Lessons/'+t.path,{waitUntil:'domcontentloaded'});
  });
}
module.exports={exercise};
