/* Reviewed media equivalence: a local clip or its working subject model, with
 * the same loaded still, question and paper scenario. No playback claim.
 * Earth_rotation_clip.mp4 is the expected CONTENT identity, not observed HTML.
 */
'use strict';
const assert=require('node:assert/strict');

function hasModelContract(c){return c.video.url==='Earth_rotation_clip.mp4';}

async function assertEarthRotationModel(page,{advanceStage,current}){
  const host=page.locator('[data-science-return="earth"]');
  assert.equal(await host.count(),1,'The replacement must contain one Earth rotation/orbit model');
  const targetStage=await host.evaluate(node=>[...document.querySelectorAll('.slide')].indexOf(node.closest('.slide')));
  assert.ok(targetStage>=0,'The replacement model must belong to a lesson stage');
  const from=await current(page);assert.ok(from>=0&&from<=targetStage,'The replacement starts at or before its model stage');
  // Use the original browser runner's reviewed navigation: Next can reveal
  // several diagram steps before advancing. Never bypass those real clicks.
  for(let at=from;at<targetStage;at++)await advanceStage(page,at+1);
  assert.equal(await current(page),targetStage,'Native Next navigation must reach the model stage');
  assert.equal(await host.isVisible(),true,'The replacement model must be reachable through lesson navigation');
  const mode=host.locator('select[data-sr="mode"]'),step=host.locator('button[data-sr="step"]'),reset=host.locator('button[data-sr="reset"]');
  for(const [name,control] of [['Focus',mode],['Next position',step],['Reset',reset]]){
    assert.equal(await control.count(),1,'The replacement requires the '+name+' control');
    assert.equal(await control.isVisible(),true,'The replacement '+name+' control must be visible');
    assert.equal(await control.isEnabled(),true,'The replacement '+name+' control must be enabled');
  }
  assert.deepEqual(await mode.locator('option').evaluateAll(nodes=>nodes.map(n=>n.value)),['day','year'],'Focus must offer rotation/day and orbit/year');
  const geometry=async()=>{
    const svg=host.locator('.sr-diagram svg');
    assert.equal(await svg.count(),1,'The replacement must render one SVG diagram');
    assert.equal(await svg.isVisible(),true,'The replacement SVG must be visible');
    const box=await svg.boundingBox();assert.ok(box&&box.width>0&&box.height>0,'The replacement SVG must occupy screen space');
    return svg.evaluate(node=>{
      const painted=n=>{for(let p=n;p&&p instanceof Element;p=p.parentElement){const style=getComputedStyle(p);if(style.display==='none'||style.visibility==='hidden'||Number(style.opacity)===0)return false;}return true;};
      const point=radius=>{const n=node.querySelector('circle[r="'+radius+'"]');if(!n||!painted(n))return null;const b=n.getBBox();return b.width>0&&b.height>0?{x:n.cx.baseVal.value,y:n.cy.baseVal.value}:null;};
      return {sun:point(27),earth:point(33),observer:point(6)};
    });
  };
  const requireBodies=s=>{assert.ok(s.sun&&s.earth,'The replacement SVG must contain the Sun and Earth');};
  // Inspect the initial SVG before touching controls: a missing diagram must
  // fail, rather than be silently rebuilt by a select/reset interaction.
  const initial=await geometry();requireBodies(initial);
  await mode.selectOption('day');await reset.click();
  const day=await geometry();requireBodies(day);assert.ok(day.observer,'The rotation diagram must contain an observer');
  await step.click();
  const nextDay=await geometry();requireBodies(nextDay);assert.ok(nextDay.observer,'The stepped rotation diagram must contain an observer');
  assert.deepEqual(nextDay.sun,day.sun,'Rotation keeps the model Sun fixed');
  assert.deepEqual(nextDay.earth,day.earth,'Rotation turns Earth without advancing its orbit');
  assert.notDeepEqual(nextDay.observer,day.observer,'Next position must move the observer around Earth');
  await reset.click();assert.deepEqual(await geometry(),day,'Reset must restore the initial rotation geometry');
  await mode.selectOption('year');await reset.click();
  const year=await geometry();requireBodies(year);
  assert.notDeepEqual(year,day,'Focus must switch from rotation to an orbit view');
  await step.click();const nextYear=await geometry();requireBodies(nextYear);
  assert.deepEqual(nextYear.sun,year.sun,'The model Sun stays fixed while Earth orbits');
  assert.notDeepEqual(nextYear.earth,year.earth,'Next position must move Earth around the Sun');
  const radius=s=>Math.hypot(s.earth.x-s.sun.x,s.earth.y-s.sun.y);
  assert.ok(Math.abs(radius(nextYear)-radius(year))<0.01,'The schematic orbit retains its radius');
  await reset.click();assert.deepEqual(await geometry(),year,'Reset must restore the initial orbit geometry');
}

async function assertMediaResource({page,c,url,viewport,loadedImage,advanceStage,current}){
  const fallback=page.locator('.media img');await loadedImage(fallback);assert.equal(await fallback.getAttribute('src'),c.video.fallback_image);
  const mediaText=await page.locator('.media').innerText();assert.ok(mediaText.includes(c.video.prompt));assert.ok(mediaText.includes(c.video.fallback_text));
  if(c.week===7)assert.equal(await fallback.getAttribute('src'),'assets/Moon_rotation_fallback.png');
  const video=page.locator('video');
  if(c.video.local_file&&await video.count()===0){
    assert.ok(hasModelContract(c),'A missing local video requires an explicit equivalent-model contract');
    const link=page.locator('.media a');
    assert.equal(await link.count(),1,'The replacement requires one model link in the media panel');
    const target=new URL('/Lessons/'+c.online_path,url).href;
    assert.equal(new URL(await link.getAttribute('href'),url).href,target,'The replacement must link to the expected source lesson');
    assert.equal(await link.isVisible(),true,'The replacement model link must be visible');
    try{
      await link.click();await page.waitForURL(target);
      await assertEarthRotationModel(page,{advanceStage,current});
    }finally{await page.goto(url,{waitUntil:'domcontentloaded'});await page.locator('html.js').waitFor();}
  }else if(c.video.local_file){
    assert.equal(await video.getAttribute('preload'),'none');assert.equal(await video.getAttribute('autoplay'),null);assert.notEqual(await video.getAttribute('controls'),null);
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
}

module.exports={hasModelContract,assertEarthRotationModel,assertMediaResource};
