#!/usr/bin/env node
// Headless Chromium boot check: each file at 390/768/1440, collect console errors +
// pageerrors. /hud.js 404 is a known site-repo caveat, not a gap (filtered but counted).
// Usage: boot.js <file...>   or   boot.js --list listfile
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path'), fs = require('fs');

(async () => {
  let files = process.argv.slice(2);
  if (files[0] === '--list') files = fs.readFileSync(files[1], 'utf8').trim().split('\n');
  const browser = await chromium.launch();
  let anyBad = false;
  for (const f of files) {
    for (const w of [390, 768, 1440]) {
      const page = await browser.newPage({ viewport: { width: w, height: w < 500 ? 844 : 900 } });
      const errs = [], hud404 = [];
      page.on('console', m => {
        if (m.type() !== 'error') return;
        const loc = (m.location() && m.location().url) || '';
        ((m.text().includes('hud.js') || loc.includes('hud.js')) ? hud404 : errs).push(m.text() + ' @' + loc);
      });
      page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
      page.on('requestfailed', r => { if (!r.url().includes('hud.js')) errs.push('REQFAIL: ' + r.url()); });
      try { await page.goto('file://' + path.resolve(f), { waitUntil: 'load', timeout: 20000 }); await page.waitForTimeout(400); }
      catch (e) { errs.push('NAV: ' + e.message); }
      if (errs.length) { anyBad = true; console.log(`FAIL ${f} @${w}: ${errs.slice(0, 3).join(' | ').slice(0, 300)}`); }
      await page.close();
    }
    if (!anyBad) process.stdout.write('.');
  }
  console.log(anyBad ? '\nboot: FAIL' : '\nboot: all clean');
  await browser.close();
  process.exit(anyBad ? 1 : 0);
})();
