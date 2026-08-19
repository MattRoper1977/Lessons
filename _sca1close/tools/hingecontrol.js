#!/usr/bin/env node
// SCA-1 CLOSE v2 §1 controls, run in headless Chromium on the real files.
//   first-button   : click the first rendered option; report correct/total (35/35 before, chance after)
//   position       : over N loads per deck, where does the correct option render? (uniformity)
//   identity       : click the button whose data-i/data-index equals the wrapper key -> must be correct
//   index-variant  : score by DOM POSITION instead of identity -> must go RED once shuffled
// Usage: hingecontrol.js <mode> [loads] < list of files on argv or --list file
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path'), fs = require('fs');

const MODE = process.argv[2];
let rest = process.argv.slice(3);
let LOADS = 1;
if (/^\d+$/.test(rest[0] || '')) { LOADS = parseInt(rest.shift(), 10); }
let files = rest;
if (files[0] === '--list') files = fs.readFileSync(files[1], 'utf8').trim().split('\n');

// In-page probe. Returns per-hinge facts for the CURRENT rendered order.
const PROBE = () => {
  const out = [];
  document.querySelectorAll('.soft, .soft-check').forEach(w => {
    const isG = w.classList.contains('soft-check');
    const key = Number(isG ? w.dataset.correct : w.dataset.c);
    const box = w.querySelector('.options');
    if (!box) return;
    const btns = [...box.querySelectorAll('button')];
    const ids = btns.map(b => Number(isG ? b.dataset.index : b.dataset.i));
    out.push({ key, ids, correctPos: ids.indexOf(key), n: btns.length, exempt: w.getAttribute('data-shuffle') === 'off' });
  });
  return out;
};

// Click a button by rendered position, then read the feedback class.
const CLICK = (pos) => {
  const res = [];
  document.querySelectorAll('.soft, .soft-check').forEach(w => {
    const box = w.querySelector('.options');
    if (!box) return;
    const btns = [...box.querySelectorAll('button')];
    const b = btns[pos];
    if (!b) return;
    b.click();
    const fb = w.querySelector('.feedback');
    const cls = fb ? fb.className : '';
    res.push({ correct: /\b(correct|good)\b/.test(cls), cls });
  });
  return res;
};

(async () => {
  const browser = await chromium.launch();
  let hit = 0, tot = 0;
  const posHist = {};
  let idOK = 0, idTot = 0, idxRed = 0, idxTot = 0;
  for (const f of files) {
    for (let L = 0; L < LOADS; L++) {
      const page = await browser.newPage();
      await page.goto('file://' + path.resolve(f), { waitUntil: 'load' });
      await page.waitForTimeout(120);
      if (MODE === 'first-button') {
        const r = await page.evaluate(CLICK, 0);
        r.forEach(x => { tot++; if (x.correct) hit++; });
      } else if (MODE === 'position') {
        const p = await page.evaluate(PROBE);
        p.forEach(x => { posHist[x.correctPos] = (posHist[x.correctPos] || 0) + 1; });
      } else if (MODE === 'identity') {
        const p = await page.evaluate(PROBE);
        for (const x of p) {
          const r = await page.evaluate(CLICK, x.correctPos);
          idTot++; if (r.length && r[0].correct) idOK++;
        }
      } else if (MODE === 'index-variant') {
        // Simulate an index-keyed scorer: "the correct answer is whatever sits at
        // position === wrapper key". Correct only when the shuffle happened to leave it there.
        const p = await page.evaluate(PROBE);
        p.forEach(x => { idxTot++; if (x.correctPos !== x.key) idxRed++; });
      }
      await page.close();
    }
  }
  if (MODE === 'first-button') console.log(`first-button: ${hit}/${tot} correct (${(100 * hit / tot).toFixed(1)}%)`);
  if (MODE === 'position') {
    const total = Object.values(posHist).reduce((a, b) => a + b, 0);
    console.log('correct-option rendered position histogram:', JSON.stringify(posHist),
      '=> ' + Object.entries(posHist).map(([k, v]) => `pos${k} ${(100 * v / total).toFixed(1)}%`).join(', '));
  }
  if (MODE === 'identity') console.log(`identity-keyed scoring after shuffle: ${idOK}/${idTot} correct`);
  if (MODE === 'index-variant') console.log(`index-keyed variant would MISSCORE ${idxRed}/${idxTot} (>0 = the variant is red, as required)`);
  await browser.close();
})();
