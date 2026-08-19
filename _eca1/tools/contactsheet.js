#!/usr/bin/env node
// ECA-1 PART B contact sheets: 3 slides × before/after (G off/on) × 390 & 1440 px.
// Usage: contactsheet.js <outdir> <file> <slideTitle1,slideTitle2,slideTitle3>
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path'), fs = require('fs');

(async () => {
  const [outdir, file, slidesArg] = process.argv.slice(2);
  const slideTitles = slidesArg.split(',');
  fs.mkdirSync(outdir, { recursive: true });
  const browser = await chromium.launch();
  for (const w of [390, 1440]) {
    const page = await browser.newPage({ viewport: { width: w, height: w < 500 ? 844 : 900 } });
    await page.goto('file://' + path.resolve(file), { waitUntil: 'load' });
    await page.waitForTimeout(300);
    for (const t of slideTitles) {
      await page.evaluate(title => {
        const slides = [...document.querySelectorAll('.slide')];
        slides.forEach(s => s.classList.remove('active'));
        const hit = slides.find(s => (s.dataset.title || '').includes(title)) || slides[0];
        hit.classList.add('active');
        window.scrollTo(0, 0);
      }, t);
      await page.waitForTimeout(150);
      for (const on of [false, true]) {
        await page.evaluate(v => {
          document.documentElement.classList.toggle('mbm-guide-on', v);
        }, on);
        await page.waitForTimeout(100);
        const name = `${t.replace(/\W+/g, '')}_${on ? 'revealed' : 'default'}_${w}.png`;
        await page.screenshot({ path: path.join(outdir, name) });
      }
    }
    await page.close();
  }
  await browser.close();
  console.log('contact sheet →', outdir);
})();
