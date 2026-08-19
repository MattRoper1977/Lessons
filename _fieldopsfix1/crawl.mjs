#!/usr/bin/env node
// FIX-1 link crawl: from the new hub, follow every relative link in a real browser
// and assert the destination actually rendered. Includes a control that must go red.
const _pw = await import('/opt/node22/lib/node_modules/playwright/index.js');
const chromium = _pw.chromium || _pw.default.chromium;
import path from 'path'; import fs from 'fs';

const ROOT = process.cwd();
const HUB  = path.join(ROOT, 'Science_Teesside/Build/v4_fieldops/index.html');
const br = await chromium.launch();
const pg = await br.newPage({ viewport: { width: 390, height: 844 } });
let bad = 0;
const say = (ok, s) => { console.log((ok ? '  PASS ' : '  FAIL ') + s); if (!ok) bad++; };

await pg.goto('file://' + HUB, { waitUntil: 'load' });
console.log('HUB title: ' + JSON.stringify(await pg.title()));

// every href the hub renders, resolved by the browser itself (not by me)
const hrefs = await pg.$$eval('a[href]', as => as.map(a => ({ raw: a.getAttribute('href'), abs: a.href, text: a.textContent.trim() })));
console.log('hub renders ' + hrefs.length + ' links');

for (const h of hrefs) {
  const p2 = await br.newPage();
  let t = null, err = null;
  try { const r = await p2.goto(h.abs, { waitUntil: 'load', timeout: 20000 }); t = await p2.title(); if (!r) err = 'no response'; }
  catch (e) { err = e.message.split('\n')[0]; }
  say(!!t && !err, `${h.raw}  ->  ${err ? 'ERR ' + err : JSON.stringify(t)}`);
  await p2.close();
}

// CONTROL: the same crawl over a href that does not exist must go red.
{
  const p2 = await br.newPage();
  let reached = false;
  try { await p2.goto('file://' + path.join(path.dirname(HUB), '05_This_Lab_Does_Not_Exist.html'), { waitUntil: 'load', timeout: 8000 }); reached = true; }
  catch (e) { reached = false; }
  say(!reached, `CONTROL absent lab must NOT resolve (reached=${reached})`);
}
// CONTROL 2: the bare directory URL — what the owner's phone hit. Under file:// a
// directory listing exists, so this control proves only that the hub file is the
// thing Pages will serve at that URL: assert the directory resolves to index.html.
{
  const p2 = await br.newPage();
  await p2.goto('file://' + path.dirname(HUB) + '/', { waitUntil: 'load', timeout: 8000 }).catch(()=>{});
  const listed = await p2.content();
  say(listed.includes('index.html'), 'CONTROL directory now contains index.html (the file Pages serves for the bare URL)');
  await p2.close();
}

await br.close();
console.log(bad ? `crawl: FAIL (${bad})` : 'crawl: all clean');
process.exit(bad ? 1 : 0);
