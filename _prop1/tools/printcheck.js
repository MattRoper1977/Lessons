#!/usr/bin/env node
// PROP-1 A-48 / XP26 gate: prove the Lundy (and feedback) print sections actually
// reach print output, rather than trusting that the id array now lists them.
//
// Method: stub window.print, call printPack(level) for each tier, then read which
// .print-section ids carry .visible AND compute non-zero rendered height under
// print media. A section listed but hidden by CSS would pass a grep and fail here.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const files = process.argv.slice(2);
  const browser = await chromium.launch();
  let bad = 0;
  for (const f of files) {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    const errs = []; page.on('pageerror', e => errs.push(e.message));
    await page.goto('file://' + path.resolve(f), { waitUntil: 'load' });
    await page.emulateMedia({ media: 'print' });
    const r = await page.evaluate(() => {
      window.print = () => {};
      const out = {};
      const has = id => !!document.getElementById('print-' + id);
      for (const level of ['supported', 'standard', 'stretch']) {
        try { printPack(level); } catch (e) { return { err: String(e) }; }
        const vis = [...document.querySelectorAll('.print-section.visible')].map(el => el.id);
        const lundy = document.getElementById('print-lundy');
        const fb = document.getElementById('print-feedback');
        out[level] = {
          visible: vis,
          lundyVisible: !!(lundy && lundy.classList.contains('visible')),
          lundyHeight: lundy ? Math.round(lundy.getBoundingClientRect().height) : null,
          feedbackVisible: !!(fb && fb.classList.contains('visible')),
          feedbackHeight: fb ? Math.round(fb.getBoundingClientRect().height) : null,
        };
      }
      out.hasLundy = has('lundy'); out.hasFeedback = has('feedback');
      return out;
    });
    if (r.err) { console.log(`FAIL ${f} :: ${r.err}`); bad++; await page.close(); continue; }
    const tiers = ['supported', 'standard', 'stretch'];
    const ok = tiers.every(t =>
      (!r.hasLundy || (r[t].lundyVisible && r[t].lundyHeight > 0)) &&
      (!r.hasFeedback || (r[t].feedbackVisible && r[t].feedbackHeight > 0))) && !errs.length;
    if (!ok) bad++;
    console.log(`${ok ? 'PASS' : 'FAIL'} ${f}`);
    for (const t of tiers)
      console.log(`      ${t.padEnd(9)} lundy ${r[t].lundyVisible ? 'visible' : 'HIDDEN'} h=${r[t].lundyHeight} · feedback ${r[t].feedbackVisible ? 'visible' : 'HIDDEN'} h=${r[t].feedbackHeight} · sections=${r[t].visible.length}`);
    if (errs.length) console.log('      PAGEERRORS ' + errs.join(' | '));
    await page.close();
  }
  await browser.close();
  console.log(bad ? `\nprintcheck: ${bad} FAILED` : `\nprintcheck: all ${files.length} decks print the Lundy and feedback sheets at every tier`);
  process.exit(bad ? 1 : 0);
})();
