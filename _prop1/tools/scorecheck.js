#!/usr/bin/env node
// PROP-1 §1 scored-control gate.
//
// Rows that re-key a scored match (A-3, A-P22, A-P109, A-P110, A-P12 …) must be proven
// end to end in a real browser, not by reading the markup: all-correct must score full
// marks, and one-wrong must score n-1. Reading data-correct only proves the file says
// the right thing; it does not prove the counter agrees.
//
// Usage: scorecheck.js <file...>
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const files = process.argv.slice(2);
  const browser = await chromium.launch();
  let bad = 0;

  for (const f of files) {
    const url = 'file://' + path.resolve(f);
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    const errs = [];
    page.on('pageerror', e => errs.push(e.message));
    await page.goto(url, { waitUntil: 'load' });

    // discover the control
    const info = await page.evaluate(() => {
      const targets = [...document.querySelectorAll('[data-correct]')];
      const pills = [...document.querySelectorAll('.match-pill')];
      return { n: targets.length, pills: pills.length,
               keys: targets.map(t => t.getAttribute('data-correct')) };
    });
    if (!info.n || !info.pills) { console.log(`SKIP ${f} (no scored match found)`); await page.close(); continue; }

    // helper the page runs for us: click pill with id, then target index
    const play = async (order) => page.evaluate(async (order) => {
      const fresh = () => [...document.querySelectorAll('[data-correct]')];
      const pillFor = id => [...document.querySelectorAll('.match-pill')]
        .find(p => (p.getAttribute('onclick') || '').includes(`'${id}'`) && !p.classList.contains('placed'));
      for (const step of order) {
        const t = fresh()[step.target];
        const want = step.wrongId !== undefined ? step.wrongId : t.getAttribute('data-correct');
        const p = pillFor(want);
        if (p) p.click();
        t.click();
      }
      const ms = document.getElementById('match-score');
      return ms ? ms.textContent.trim() : null;
    }, order);

    // 1. all correct -> full marks
    const allCorrect = await play([...Array(info.n).keys()].map(i => ({ target: i })));

    // 2. reload, one deliberately wrong -> n-1
    await page.goto(url, { waitUntil: 'load' });
    const keys = info.keys;
    const wrongId = keys.find(k => k !== keys[0]);           // any key that is not target 0's
    const oneWrong = await play([
      { target: 0, wrongId },                                 // deliberate miss
      ...[...Array(info.n).keys()].slice(1).map(i => ({ target: i })),
    ]);

    const wantFull = String(info.n), wantMinus = String(info.n - 1);
    const ok = allCorrect === wantFull && oneWrong === wantMinus && !errs.length;
    if (!ok) bad++;
    console.log(`${ok ? 'PASS' : 'FAIL'} ${f}`);
    console.log(`      n=${info.n} keys=[${keys.join(',')}] pills=${info.pills}`);
    console.log(`      all-correct -> ${allCorrect} (want ${wantFull}) · one-wrong -> ${oneWrong} (want ${wantMinus})`);
    if (errs.length) console.log(`      PAGEERRORS: ${errs.join(' | ')}`);
    await page.close();
  }
  await browser.close();
  console.log(bad ? `\nscorecheck: ${bad} FAILED` : `\nscorecheck: all ${files.length} scored controls prove full marks and n-1`);
  process.exit(bad ? 1 : 0);
})();
