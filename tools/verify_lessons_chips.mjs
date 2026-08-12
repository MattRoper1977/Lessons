#!/usr/bin/env node
/* The chip-count gate: every number the Lessons hub ADVERTISES equals what the
 * real filter chain RETURNS, in a real browser over HTTP.
 *
 * Three advertised surfaces, one contract each:
 *   - subject chips  "Physics (15)"  → click it, count the rendered cards
 *   - year tabs      "513 resources" → click it, count the rendered cards
 *   - the #count line "N of M"       → N == cards on screen, M == entries in
 *                                      resources.json fetched over the same origin
 *
 * Clicking is the point: a chip whose count came from the same broken filter
 * would agree with itself, so the card count is taken from the DOM the click
 * produced, and the catalogue total is fetched independently. Library chips
 * (subjects with nothing in the current collection) advertise their all-years
 * total and legitimately widen the year — the gate restores the collection
 * through the year tab afterwards, the same control a person would use.
 *
 *   node tools/verify_lessons_chips.mjs --base http://127.0.0.1:PORT/
 */
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const pw = (() => {
  for (const p of ['playwright', '/opt/node22/lib/node_modules/playwright/index.js']) {
    try { return require(p); } catch (_) {}
  }
  console.error('[FAIL] playwright not found'); process.exit(2);
})();
const { chromium } = pw;

const argv = process.argv.slice(2);
const val = (n) => { const i = argv.indexOf(n); return i > -1 ? argv[i + 1] : null; };
const BASE = (val('--base') || process.env.MBM_BASE_URL || '').replace(/\/?$/, '/');
if (!BASE) { console.error('usage: --base <site root url>'); process.exit(2); }

const results = [];
const check = (limb, ok, detail) => {
  results.push({ limb, ok });
  console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${String(limb).padEnd(46)} ${detail}`);
  return ok;
};

const manifest = await (await fetch(new URL('Lessons/resources.json', BASE))).json();
if (!Array.isArray(manifest)) { console.error('[FAIL] resources.json is not an array'); process.exit(1); }
console.log(`resources.json over HTTP: ${manifest.length} entries`);

const browser = await chromium.launch({
  args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
});
const page = await (await browser.newContext({ viewport: { width: 1280, height: 1000 } })).newPage();
const errs = [];
page.on('console', (m) => { if (m.type() === 'error') errs.push(m.text()); });
page.on('pageerror', (e) => errs.push('pageerror: ' + e.message));
await page.goto(new URL('Lessons/', BASE).href, { waitUntil: 'domcontentloaded' });
await page.waitForSelector('#quicknav .chip', { timeout: 15000 });

const cardsOnScreen = () => page.evaluate(() => document.querySelectorAll('#cards article.card').length);
const countLine = () => page.evaluate(() => document.getElementById('count').textContent);

console.log('\nthe #count line vs the catalogue');
{
  const m = (await countLine()).match(/^(\d+) of (\d+) resources/);
  check('#count advertises the catalogue total', !!m && Number(m[2]) === manifest.length,
    `${m ? m[0] : '(unparsed)'} vs manifest ${manifest.length}`);
}

console.log('\nyear tabs — advertised == returned');
const ytabs = await page.evaluate(() => [...document.querySelectorAll('.ytab')].map((b) => ({
  year: b.dataset.year, label: b.querySelector('[data-count]').textContent })));
for (const yt of ytabs) {
  const adv = Number((yt.label.match(/^(\d+) resources/) || [])[1]);
  await page.click(`.ytab[data-year="${yt.year}"]`);
  await page.waitForTimeout(350);
  const got = await cardsOnScreen();
  check(`ytab ${yt.year || 'all years'}`, Number.isFinite(adv) && got === adv, `advertises ${adv}, returns ${got}`);
}
// back to the default collection before the chips, through the real control
await page.click('.ytab[data-year="2026-27"]');
await page.waitForTimeout(350);

console.log('\nsubject chips — advertised == returned, every chip');
const chips = await page.evaluate(() => [...document.querySelectorAll('#quicknav .chip')].map((b) => ({
  sub: b.dataset.sub, label: b.textContent, lib: b.classList.contains('lib') })));
for (const c of chips) {
  if (!c.sub) continue; // "All subjects" carries no number; the ytab rows covered the unfiltered counts
  const adv = Number((c.label.match(/\((\d+)\)\s*$/) || [])[1]);
  await page.click(`#quicknav .chip[data-sub="${c.sub.replace(/"/g, '\\"')}"]`);
  await page.waitForTimeout(350);
  const got = await cardsOnScreen();
  const line = (await countLine()).match(/^(\d+) of/);
  const lineN = line ? Number(line[1]) : NaN;
  check(`chip ${c.sub}${c.lib ? ' (library)' : ''}`, Number.isFinite(adv) && got === adv && lineN === got,
    `advertises ${adv}, returns ${got}, #count says ${lineN}`);
  if (c.lib) { // a library chip widened the year; restore the collection as a person would
    await page.click('.ytab[data-year="2026-27"]');
    await page.waitForTimeout(350);
  }
  await page.click('#quicknav .chip[data-sub=""]'); // back to All subjects
  await page.waitForTimeout(250);
}

console.log('\nconsole');
check('zero console errors', errs.length === 0, errs.length ? errs.slice(0, 3).join(' | ') : 'clean');

await browser.close();
const failed = results.filter((r) => !r.ok);
console.log(`\n${failed.length ? '[FAIL]' : '[PASS]'} chip-count gate: ${results.length - failed.length}/${results.length} limbs`);
process.exit(failed.length ? 1 : 0);
