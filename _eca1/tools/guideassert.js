#!/usr/bin/env node
// ECA-1 PART B §9 gates, per file (headless Chromium):
//  - default state on first load = hidden: every [data-mbm-guide] display:none,
//    button present with aria-pressed=false
//  - G toggles all tagged elements visible + button pressed; localStorage persists
//  - print output identical: emulateMedia('print') text vs the pre-patch snapshot
//    (pass --print-base <dir> of pre-patch print texts to compare; else records them)
// Usage: guideassert.js [--record-print dir|--print-base dir] file...
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path'), fs = require('fs');

(async () => {
  const argv = process.argv.slice(2);
  let mode = null, dir = null;
  if (argv[0] === '--record-print' || argv[0] === '--print-base') { mode = argv.shift(); dir = argv.shift(); fs.mkdirSync(dir, { recursive: true }); }
  const files = argv;
  const browser = await chromium.launch();
  let bad = 0;
  for (const f of files) {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    const errs = [];
    page.on('pageerror', e => errs.push(e.message));
    await page.goto('file://' + path.resolve(f), { waitUntil: 'load' });
    await page.waitForTimeout(300);

    // print text snapshot (independent of screen state)
    await page.emulateMedia({ media: 'print' });
    const printText = await page.evaluate(() => document.body.innerText.replace(/\s+/g, ' ').trim());
    await page.emulateMedia({ media: 'screen' });
    const key = f.replace(/[\/']/g, '_') + '.txt';
    if (mode === '--record-print') fs.writeFileSync(path.join(dir, key), printText);
    if (mode === '--print-base') {
      const want = fs.readFileSync(path.join(dir, key), 'utf8');
      if (want !== printText) { console.log(`FAIL print-diff ${f}`); bad++; }
    }

    const r = await page.evaluate(() => {
      const tagged = [...document.querySelectorAll('[data-mbm-guide]')];
      const hiddenAtLoad = tagged.every(el => getComputedStyle(el).display === 'none');
      const btn = document.querySelector('.mbm-guide-btn');
      const pressed0 = btn && btn.getAttribute('aria-pressed');
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'g', bubbles: true }));
      const shownAfterG = tagged.every(el => getComputedStyle(el).display !== 'none');
      const pressed1 = btn && btn.getAttribute('aria-pressed');
      const store = localStorage.getItem('mbm_guide_v1');
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'G', bubbles: true }));
      const hiddenAgain = tagged.every(el => getComputedStyle(el).display === 'none');
      const store2 = localStorage.getItem('mbm_guide_v1');
      return { n: tagged.length, hiddenAtLoad, btn: !!btn, pressed0, shownAfterG, pressed1, store, hiddenAgain, store2 };
    });
    const ok = r.n > 0 && r.hiddenAtLoad && r.btn && r.pressed0 === 'false' && r.shownAfterG
      && r.pressed1 === 'true' && r.store === '1' && r.hiddenAgain && r.store2 === '0' && !errs.length;
    if (!ok) { console.log(`FAIL assert ${f}: ${JSON.stringify(r)} errs=${errs.slice(0, 2)}`); bad++; }
    await page.close();
  }
  console.log(bad ? `guideassert: ${bad} FAIL` : `guideassert: all pass (${files.length} files)`);
  await browser.close();
  process.exit(bad ? 1 : 0);
})();
