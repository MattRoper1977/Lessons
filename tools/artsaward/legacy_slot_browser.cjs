/* Run against the real legacy HTML. Fixture entries exist only in intercepted test responses. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require('playwright');
const deckPath = process.argv[2] || path.resolve(__dirname,'../../Art_Teesside/Grow/GROW_ART_W4_Arts_Event_Attend_Capture_and_Review.html');
const html = fs.readFileSync(deckPath,'utf8');
const baselinePath = process.argv[3];
assert.ok(baselinePath, 'Supply the retained pre-correction baseline.');
const baseline = fs.readFileSync(baselinePath,'utf8');
assert.equal(require('node:crypto').createHash('sha256').update(baseline).digest('hex'), '7e7e84b3b4aea825ce9c832819250753212f4bdf612f4eebc210bd067a22a4cb');
const route = '/Art_Teesside/Grow/GROW_ART_W4_Arts_Event_Attend_Capture_and_Review.html';
const base = {schema:'arts-award-slots-v1',slots:{ORG_SLOT:{entries:[]},EVENT_SLOT:{entries:[]}}};
const fixture = (org,event) => ({schema:base.schema,slots:{
  ORG_SLOT:{entries:org?[{name:org,route:'R3',status:'CONFIRMED'}]:[]},
  EVENT_SLOT:{entries:event?[{name:event,route:'R3',status:'CONFIRMED'}]:[]},
}});

(async () => {
  const browser = await chromium.launch({headless:true, channel:process.env.CI ? 'chrome' : undefined});
  const page = await browser.newPage({viewport:{width:1440,height:1000}});
  let current = base;
  let served = html;
  let errors = [];
  page.on('pageerror',error=>errors.push(error.message));
  const requested = [];
  await page.route('http://legacy-award.test/**',async request => {
    const url = new URL(request.request().url());
    if (url.pathname === '/tools/artsaward/SLOTS.json') {
      requested.push(url.pathname);
      return request.fulfill({contentType:'application/json',body:JSON.stringify(current)});
    }
    if (url.pathname === route) return request.fulfill({contentType:'text/html; charset=utf-8',body:served});
    return request.fulfill({status:404,body:''});
  });
  const go = async () => {
    await page.goto('http://legacy-award.test'+route);
    await page.waitForFunction(()=>{
      const text=document.getElementById('award-slot-status')?.textContent || '';
      return text.startsWith('No confirmed event route') || text.startsWith('A confirmed event route');
    });
  };
  await go();
  assert.equal(await page.locator('.slide').count(),10);
  assert.equal(await page.locator('section[data-min]').count(),0);
  assert.equal(await page.locator('#award-slot-panel').isVisible(),false);
  assert.match(await page.locator('#award-slot-status').textContent(),/No confirmed event route.*preparation only/);
  assert.equal(await page.locator('#award-slot-rows li').count(),2);
  await page.getByRole('button',{name:'ⓘ Guidance',exact:true}).click();
  await page.locator('#award-slot-panel summary').click();
  assert.equal(await page.locator('#award-slot-file').isVisible(),true);

  current=fixture('Organisation reference only',null);
  await go();
  assert.match(await page.locator('#award-slot-status').textContent(),/No confirmed event route/);
  assert.match(await page.locator('#award-slot-rows li').nth(0).textContent(),/Organisation reference only/);

  current=fixture(null,'Event without organisation entry');
  await go();
  assert.match(await page.locator('#award-slot-status').textContent(),/^A confirmed event route/);
  assert.match(await page.locator('#award-slot-rows li').nth(0).textContent(),/no confirmed entry/);

  current=fixture('Organisation changed in source','Event changed in source');
  await go();
  assert.match(await page.locator('#award-slot-rows li').nth(0).textContent(),/Organisation changed in source/);
  const input=page.locator('#award-slot-file');
  await input.setInputFiles({name:'SLOTS.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(fixture('<b>Local organisation</b>','Local event')))});
  await page.waitForFunction(()=>document.getElementById('award-slot-rows').textContent.includes('<b>Local organisation</b>'));
  assert.equal(await page.locator('#award-slot-rows li b').count(),0);
  await input.setInputFiles({name:'SLOTS.json',mimeType:'application/json',buffer:Buffer.from('{bad')});
  await page.waitForFunction(()=>document.getElementById('award-slot-status').textContent.includes('could not be read'));
  assert.equal(await page.locator('#award-slot-rows li').count(),0);

  await page.setViewportSize({width:390,height:844});
  if (!await page.locator('#award-slot-panel').isVisible()) await page.getByRole('button',{name:'ⓘ Guidance',exact:true}).click();
  if (!await input.isVisible()) await page.locator('#award-slot-panel summary').click();
  assert.equal(await input.isVisible(),true);
  assert.ok((await page.locator('#award-slot-panel').boundingBox()).width > 100);
  const overflow=await page.locator('#award-slot-panel').evaluate(node=>node.scrollWidth>node.clientWidth+2);
  assert.equal(overflow,false);
  assert.ok(requested.length>=4);
  const draftErrors=[...new Set(errors)];
  served=baseline;errors=[];
  await page.goto('http://legacy-award.test'+route);
  const baselineErrors=new Set(errors);
  assert.deepEqual(draftErrors.filter(error=>!baselineErrors.has(error)),[]);
  await browser.close();
  process.stdout.write('PASS: real div.slide deck; Guidance access; ORG reference and independent EVENT readiness; current-source reload; file override; safe text; invalid-file fallback; narrow panel; no new script errors.\n');
})().catch(error=>{console.error(error);process.exit(1);});
