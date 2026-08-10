// Gate 2 + Gate A1, run in real headless Chromium against the shipped files.
//
// Two things this proves that a text scan cannot:
//   * the page boots with zero console errors and zero page errors;
//   * under `@media print` with NO tier chosen, all three tier routes are
//     actually laid out — measured as rendered text length, not as CSS text.
//
// Usage: node boot.mjs <file.html> [...]
import { chromium } from 'playwright';
import { pathToFileURL } from 'url';
import { resolve } from 'path';

const files = process.argv.slice(2);
let bad = 0;
const rows = [];

const browser = await chromium.launch();
for (const f of files) {
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  const errs = [];
  page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  page.on('pageerror', e => errs.push('pageerror: ' + e.message));
  await page.goto(pathToFileURL(resolve(f)).href, { waitUntil: 'load' });
  await page.waitForTimeout(120);

  const isLesson = /\/SCI_/.test(f);
  let row = { file: f.split('/').slice(-2).join('/'), errs: errs.length };

  if (isLesson) {
    const grow = await page.evaluate(() => !!document.querySelector('.print-pack'));
    const routeSel = grow ? '.print-route' : '.proute';
    const attr = grow ? 'printTier' : 'tier';

    // 1. tier attribute must be undefined on load
    row.tierOnLoad = await page.evaluate(a => document.body.dataset[a], attr);

    // 2. print default: every route laid out
    await page.emulateMedia({ media: 'print' });
    const dflt = await page.evaluate(sel => {
      const out = {};
      for (const t of ['supported', 'standard', 'stretch']) {
        const el = document.querySelector(sel + '.' + t);
        out[t] = el ? { shown: el.getClientRects().length > 0, chars: el.innerText.trim().length }
                    : null;
      }
      const pk = document.querySelector('.print-pack,.printpack');
      out.packChars = pk ? pk.innerText.replace(/\s+/g, ' ').trim().length : 0;
      return out;
    }, routeSel);
    row.printDefault = dflt;

    // 3. each button-selected tier shows exactly one route
    const perTier = {};
    for (const T of ['Supported', 'Standard', 'Stretch']) {
      await page.evaluate(([a, t]) => { document.body.dataset[a] = t; }, [attr, T]);
      perTier[T] = await page.evaluate(sel => {
        const shown = ['supported', 'standard', 'stretch'].filter(t => {
          const el = document.querySelector(sel + '.' + t);
          return el && el.getClientRects().length > 0;
        });
        const pk = document.querySelector('.print-pack,.printpack');
        return { shown, packChars: pk ? pk.innerText.replace(/\s+/g, ' ').trim().length : 0 };
      }, routeSel);
    }
    await page.evaluate(a => { delete document.body.dataset[a]; }, attr);
    row.perTier = perTier;

    // 4. afterprint teardown actually fires
    await page.evaluate(([a, t]) => { document.body.dataset[a] = t; }, [attr, 'Stretch']);
    await page.evaluate(() => window.dispatchEvent(new Event('afterprint')));
    row.afterTeardown = await page.evaluate(a => document.body.dataset[a], attr);
    await page.emulateMedia({ media: 'screen' });
  }

  rows.push(row);
  if (errs.length) { bad++; console.log('  ERRORS', row.file, errs.slice(0, 3)); }
  await ctx.close();
}
await browser.close();

// ---- assertions
let fails = [];
for (const r of rows) {
  if (r.errs) fails.push(`${r.file}: ${r.errs} console/page error(s)`);
  if (!r.printDefault) continue;
  if (r.tierOnLoad !== undefined) fails.push(`${r.file}: tier attribute set on load (${r.tierOnLoad})`);
  for (const t of ['supported', 'standard', 'stretch']) {
    const d = r.printDefault[t];
    if (!d) { fails.push(`${r.file}: no ${t} route`); continue; }
    if (!d.shown) fails.push(`${r.file}: ${t} route NOT rendered under the print default`);
    if (d.chars < 20) fails.push(`${r.file}: ${t} route rendered but empty (${d.chars} chars)`);
  }
  for (const T of ['Supported', 'Standard', 'Stretch']) {
    const s = r.perTier[T].shown;
    if (s.length !== 1 || s[0] !== T.toLowerCase())
      fails.push(`${r.file}: tier ${T} showed [${s}]`);
  }
  if (r.afterTeardown !== undefined) fails.push(`${r.file}: afterprint did not clear the attribute`);
}

console.log('\n--- printable characters: print default (all routes) vs one selected tier ---');
console.log('file'.padEnd(46), 'default', ' Supp', ' Std', ' Str');
for (const r of rows.filter(x => x.printDefault)) {
  const p = r.perTier;
  console.log(r.file.padEnd(46),
    String(r.printDefault.packChars).padStart(7),
    String(p.Supported.packChars).padStart(5),
    String(p.Standard.packChars).padStart(5),
    String(p.Stretch.packChars).padStart(5));
}
console.log(`\n${rows.length} files booted, ${rows.filter(r => r.printDefault).length} lessons probed`);
if (fails.length) { console.log('\nFAILURES:'); fails.forEach(x => console.log('  ' + x)); process.exit(1); }
console.log('boot + A1 runtime assertions: PASS');
