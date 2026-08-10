// Gate — chip-count, run against the REAL index.html in a real browser.
//
// The known bug's trigger shape is "advertised ≠ returned": the chip label is
// computed by buildQuicknav() from one filter chain and the cards by render()
// from another. Replicating the chains in Node would re-implement the bug's
// blind spot, so this drives the actual hub over http and counts actual cards.
//
// Usage: node chip_gate.mjs <base-url>
import { chromium } from 'playwright';

const BASE = process.argv[2] || 'http://127.0.0.1:8765';
const WANT = JSON.parse(process.argv[3] || '{"Science · Teesside":63,"Baseline":8}');

const browser = await chromium.launch();
const page = await browser.newPage();
const errs = [];
page.on('pageerror', e => errs.push(e.message));
await page.goto(BASE + '/index.html', { waitUntil: 'networkidle' });
await page.waitForSelector('#quicknav .chip');

const chips = await page.evaluate(() =>
  [...document.querySelectorAll('#quicknav .chip')].map(c => ({
    label: c.textContent, sub: c.dataset.sub, lib: c.classList.contains('lib') })));

const activeYear = await page.evaluate(() =>
  document.querySelector('.ytab[aria-pressed="true"]').dataset.year);
console.log(`active year collection: ${activeYear}`);

let fails = [];
for (const [sub, want] of Object.entries(WANT)) {
  const chip = chips.find(c => c.sub === sub);
  if (!chip) { fails.push(`no chip for "${sub}"`); continue; }
  const advertised = Number((chip.label.match(/\((\d+)\)\s*$/) || [])[1]);
  if (chip.lib) fails.push(`"${sub}" chip is a lib chip — not in the active collection`);
  await page.click(`#quicknav .chip[data-sub="${sub}"]`);
  await page.waitForTimeout(150);
  const returned = await page.evaluate(() => document.querySelectorAll('#cards article.card').length);
  const ok = advertised === want && returned === want;
  console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${sub.padEnd(20)} advertised=${advertised}  returned=${returned}  expected=${want}`);
  if (!ok) fails.push(`${sub}: advertised=${advertised} returned=${returned} expected=${want}`);
  // reset
  await page.click('#quicknav .chip[data-sub=""]');
  await page.waitForTimeout(80);
}

// every new file reachable from the active collection
const files = await page.evaluate(() =>
  window.ALL ? window.ALL.filter(r => r.year === '2026-27').map(r => r.file) : null);
if (files) {
  console.log(`  files in the active 2026-27 collection: ${files.length}`);
} else {
  const j = await (await fetch(BASE + '/resources.json')).json();
  const act = j.filter(r => r.year === '2026-27');
  console.log(`  entries in the active 2026-27 collection: ${act.length}`);
}

// reachability: each of the 46 new files must appear as a card href under its chip
for (const [sub, want] of Object.entries(WANT)) {
  await page.click(`#quicknav .chip[data-sub="${sub}"]`);
  await page.waitForTimeout(150);
  const hrefs = await page.evaluate(() =>
    [...document.querySelectorAll('#cards article.card a')].map(a =>
      decodeURIComponent(a.getAttribute('href'))));
  const j = await (await fetch(BASE + '/resources.json')).json();
  const want_files = j.filter(r => r.subject === sub && r.year === '2026-27').map(r => r.file);
  const missing = want_files.filter(f => !hrefs.some(h => h.endsWith(f)));
  console.log(`  ${missing.length ? 'FAIL' : 'PASS'}  ${sub}: ${want_files.length - missing.length}/${want_files.length} reachable as card links`);
  if (missing.length) fails.push(`${sub}: unreachable ${missing.slice(0, 4)}`);
  await page.click('#quicknav .chip[data-sub=""]');
  await page.waitForTimeout(80);
}

if (errs.length) fails.push(`hub page errors: ${errs[0]}`);
await browser.close();
if (fails.length) { console.log('\nFAILURES:'); fails.forEach(f => console.log('  ' + f)); process.exit(1); }
console.log('\nCHIP GATE: PASS — advertised === returned, and every new file is reachable.');
