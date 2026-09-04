/* The real reader, exercised in Chromium. No event is booked by this test. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require('playwright');
const reader = fs.readFileSync(path.join(__dirname, 'slot_reader.js'), 'utf8');
const base = {schema:'arts-award-slots-v1',slots:{EVENT_SLOT:{entries:[]}}};
const confirmed = structuredClone(base);
confirmed.slots.EVENT_SLOT.entries.push({name:'Fixture event',route:'R3',status:'CONFIRMED'});
const html = '<!doctype html><html><body><section data-min="0"></section><script>' + reader
  + '</script><script>MBMArtsSlots.mount({required:["EVENT_SLOT"],url:"/SLOTS.json"});</script></body></html>';

(async () => {
  const browser = await chromium.launch({headless:true, channel:process.env.CI ? 'chrome' : undefined});
  const page = await browser.newPage();
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  let current=base;
  await page.route('http://award.test/**',route => {
    if (route.request().url().endsWith('/SLOTS.json')) {
      // Playwright-intercepted fetches need not expose a Cache-Control header.
      // The source-reader control checks cache:'no-store'; this checks fresh UI data.
      return route.fulfill({contentType:'application/json',body:JSON.stringify(current)});
    }
    return route.fulfill({contentType:'text/html',body:html});
  });
  await page.goto('http://award.test/fixture');
  await page.getByRole('status').filter({hasText:'Unconfirmed'}).waitFor();
  assert.match(await page.locator('#award-slot-panel li').innerText(),/no confirmed entry/);
  current=confirmed;
  await page.reload();
  await page.getByRole('status').filter({hasText:'A confirmed route'}).waitFor();
  assert.match(await page.locator('#award-slot-panel li').innerText(),/Fixture event/);
  const local=structuredClone(confirmed);local.slots.EVENT_SLOT.entries[0].name='<b>Local fixture</b>';
  await page.locator('input[type=file]').setInputFiles({name:'SLOTS.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(local))});
  await page.getByText('EVENT_SLOT: <b>Local fixture</b> · R3',{exact:true}).waitFor();
  assert.equal(await page.locator('#award-slot-panel li b').count(),0);
  await page.locator('input[type=file]').setInputFiles({name:'SLOTS.json',mimeType:'application/json',buffer:Buffer.from('{bad')});
  await page.getByRole('status').filter({hasText:'could not be read'}).waitFor();
  assert.equal(await page.locator('#award-slot-panel li').count(),0);
  assert.deepEqual(errors,[]);
  console.log('PASS: hosted refresh, offline file selection, safe text display and invalid-file fallback in Chromium.');
  await browser.close();
})().catch(error=>{console.error(error);process.exit(1);});
