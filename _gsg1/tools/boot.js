// GSG-1 gate 3 — boot every changed surface in REAL Chromium.
// Real browser, so no jsdom shims are involved and none need declaring.
// Fails on any console error, page error, or failed request.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const DIR = '/home/user/Lessons/Science_Teesside/Grow/v3_40min';

(async () => {
  const files = process.argv.slice(2);
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });
  let bad = 0;
  for (const f of files) {
    const full = path.isAbsolute(f) ? f : path.join(DIR, f);
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    const errs = [];
    page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
    page.on('pageerror', e => errs.push('pageerror: ' + e.message));
    page.on('requestfailed', r => {
      // file:// favicon misses are not a page defect
      if (!/favicon/.test(r.url())) errs.push('requestfailed: ' + r.url());
    });
    await page.goto('file://' + full, { waitUntil: 'load' });
    await page.waitForTimeout(450);

    // exercise the grafted interactions so their handlers actually run
    const probe = await page.evaluate(() => {
      const out = { clicked: [], fail: [] };
      try {
        const c = document.querySelector('.commit-opt');
        if (c) { c.click(); out.clicked.push('commit'); }
        const w = document.querySelector('.wh-btn');
        if (w) { w.click(); w.click(); out.clicked.push('wordhelp'); }
        const t = document.querySelector('.tier-btn');
        if (t) { t.click(); out.clicked.push('tier'); }
        // speech button: click must not throw even when synthesis is absent
        const s = document.querySelector('.speak-btn');
        if (s && !s.hidden) { s.click(); out.clicked.push('speak'); }
      } catch (e) { out.fail.push(String(e)); }
      return out;
    });
    await page.waitForTimeout(200);
    if (probe.fail.length) errs.push('probe threw: ' + probe.fail.join('; '));

    const name = path.basename(full);
    if (errs.length) {
      bad++;
      console.log('FAIL  ' + name);
      errs.slice(0, 6).forEach(e => console.log('        ' + e));
    } else {
      console.log('ok    ' + name + '   [exercised: ' + probe.clicked.join(',') + ']');
    }
    await ctx.close();
  }
  await browser.close();
  console.log(bad === 0
    ? '\nBOOT GATE PASS — ' + files.length + '/' + files.length + ' surfaces, zero console/page errors'
    : '\nBOOT GATE FAIL — ' + bad + ' of ' + files.length);
  process.exit(bad ? 1 : 0);
})();
