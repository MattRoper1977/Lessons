/* EDU-D2: independent source expectations exercised through the real pages. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
exports.verify = async ({page, origin, root, out}) => {
  const read = p => JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
  const rows = read('resources.json');
  const manifest = read('data/companion-packs.json').packs;
  const pair = manifest.find(p => rows.some(r => r.file === p.companionOf && r.unit));
  assert(pair, 'A mapped lesson with verified unit metadata is required');
  const row = rows.find(r => r.file === pair.companionOf);
  // A2-LIST (8 Nov 2026, owner ask): the host lesson card keeps its full pathway title
  // (public pathway words shown); the reviewed topic title heads the pack page and the
  // pack row only, so the host card carries no "Original reference" expander.
  const topic = pair.title.trim();
  const expected = String(row.title).replace(/\b(BUILD|GROW|LAUNCH)\b/g, m => ({BUILD:'BASE',GROW:'TRACK',LAUNCH:'SUMMIT'})[m]);
  assert(row.title.includes(topic), 'topic title is verbatim within the host title');
  // The source catalogue deliberately keeps relative href attributes. Verify
  // both that literal contract and the browser's resolved canonical destination.
  const href = encodeURI(row.file);
  const destination = origin + '/Lessons/' + href;
  for (const width of [320,390,900,1280]) {
    await page.setViewportSize({width,height:900});
    await page.goto(origin+'/Lessons/?q='+encodeURIComponent(row.title));
    const card = page.locator('#cards .card').filter({has:page.locator('h3 a[href="'+href+'"]')});
    await card.waitFor();
    assert.equal(await card.locator('h3 a').evaluate(a=>a.href),destination);
    assert.equal(await card.locator('h3 a').innerText(),expected);
    assert.equal(await card.locator('details.title-reference').count(),0,'host card shows its own title, no reference expander');
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
    fs.mkdirSync(out,{recursive:true});
    await page.screenshot({path:path.join(out,'titles-'+width+'.png'),fullPage:true});
  }
  for (const q of [expected,topic,row.id,row.file]) {
    await page.goto(origin+'/Lessons/?q='+encodeURIComponent(q));
    await page.locator('#cards h3 a[href="'+href+'"]').waitFor();
    assert.equal(await page.locator('#cards h3 a[href="'+href+'"]').evaluate(a=>a.href),destination);
    assert.equal(await page.locator('#cards h3 a[href="'+href+'"]').innerText(),expected);
  }
  // Intersect a unit with its actual subject/pathway, then recover an empty query.
  const unit = row.unit;
  const tier = /\/(Build|Grow|Launch)\//.exec(row.file)?.[1].toUpperCase();
  assert(tier);
  await page.goto(origin+'/Lessons/?'+new URLSearchParams({subject:'science',pathway:tier,unit}));
  await page.locator('#cards .card').first().waitFor();
  const paths = await page.locator('#cards .card').evaluateAll(es=>es.map(e=>e.dataset.resourcePath));
  assert(paths.length && paths.every(file=>rows.some(r=>r.file===file&&r.unit===unit)));
  await page.locator('#search').fill('edud2-no-result-9af68');
  await page.waitForFunction(()=>document.querySelectorAll('#cards .card').length===0);
  await page.locator('[data-clear-filters]').click();
  assert.equal(new URL(page.url()).search,'');
  assert(await page.locator('#search').evaluate(e=>e===document.activeElement));
  await page.goto(origin+'/Lessons/subject.html?'+new URLSearchParams({subject:'science',pathway:tier,unit,q:row.title}));
  await page.locator('.lrow-title[href="'+href+'"]').waitFor({state:'attached'});
  assert.equal(await page.locator('.lrow-title[href="'+href+'"]').evaluate(a=>a.href),destination);
  assert.equal(await page.locator('.lrow-title[href="'+href+'"]').innerText(),expected);
  await page.locator('[data-clear-filters]').click();
  assert.equal(new URL(page.url()).searchParams.get('unit'),null);
  assert(await page.locator('#search').evaluate(e=>e===document.activeElement));
  // The reviewed topic title still heads the pack page (pack.js), independently of the card.
  const packRow = rows.find(r => r.kind === 'pack' && r.companionOf === row.file);
  assert(packRow, 'companion pack row');
  await page.goto(origin+'/Lessons/pack.html?id='+encodeURIComponent(packRow.id));
  await page.waitForFunction(id=>document.querySelector('#pack-content')?.dataset.ready===id,packRow.id);
  assert.equal(await page.locator('#pack-content h1').innerText(),topic);
  return {widths:[320,390,900,1280],lesson:row.file,fullTitleOnCard:true,topicOnPackPage:true,legacySearch:true,unitIntersection:true};
};
