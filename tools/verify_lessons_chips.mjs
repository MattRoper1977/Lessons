#!/usr/bin/env node
/* The chip-count gate, re-pointed by UX2 A4 (2026-09-08): every format chip on the
 * subject page returns exactly the rows the real filter chain returns, in a real
 * browser over HTTP.
 *
 * The old hub advertised counts on subject chips and year tabs; UX2 retired those
 * chips. The subject page's format chips ("All formats · Interactive · Editable
 * packs · PDF") are single-select and carry no number, so "advertised == returned"
 * becomes: for every subject × pathway × chip, the rows rendered after the click
 * (every accordion row opened, every "Show n more" expanded) equal the set an
 * INDEPENDENT Node-side evaluation of the same rules returns from resources.json
 * fetched over the same origin. Clicking is the point: the count comes from the
 * DOM the click produced, and the expectation comes from the catalogue, not from
 * the page's own state.
 *
 *   node tools/verify_lessons_chips.mjs --base http://127.0.0.1:PORT/
 *   node tools/verify_lessons_chips.mjs --base https://madebymatt.uk/      (production)
 *   … --red-proof   hides one row after the click and requires the gate to go red
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
const RED = argv.includes('--red-proof');
if (!BASE) { console.error('usage: --base <site root url>'); process.exit(2); }

const results = [];
const check = (limb, ok, detail) => {
  results.push({ limb, ok });
  console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${String(limb).padEnd(56)} ${detail}`);
  return ok;
};

/* ---- the rules, re-stated here independently of the page (same strings, no shared code) ---- */
const PATHWAYS = ['BUILD', 'GROW', 'LAUNCH'];
function cardOf(row) {
  const s = String(row.subject || ''), f = String(row.family || '');
  if (/science|biology|chemistry|physics/i.test(s)) return 'science';
  if (/humanities|religio|\bRE\b|history|geography/i.test(s)) return 'humanities-re';
  if (/\bart\b|arts award/i.test(s)) return 'art-studio';
  if (/ASDAN|PSHE|FoodWise|D&T|life ?skills|Vocational|PfA/i.test(s + ' ' + f)) return 'lifeskills';
  return 'x-' + String(s).toLowerCase().replace(/&/g, ' and ').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}
function tierOf(r) {
  const f = r.file || r.url || '';
  if (/(?:^|\/)Build\//.test(f)) return 'BUILD';
  if (/(?:^|\/)Grow\//.test(f)) return 'GROW';
  if (/(?:^|\/)Launch\//.test(f)) return 'LAUNCH';
  const base = f.split('/').pop().toUpperCase(), first = (f.split('/')[0] || '').toUpperCase();
  for (const t of PATHWAYS) { if (base.indexOf(t + '_') === 0 || first.indexOf(t + '_') === 0) return t; }
  const m = (r.title || '').match(/^(BUILD|GROW|LAUNCH)(?![A-Za-z])/); if (m) return m[1];
  if (/^BUILD(?![A-Za-z])/.test(r.subject || '')) return 'BUILD';
  return null;
}
function ext(p) { const m = String(p || '').split('?')[0].split('#')[0].match(/\.([a-z0-9]+)$/i); return m ? m[1].toLowerCase() : ''; }
function formatOf(r) { if (r.kind === 'pack') return 'packs'; const e = ext(r.file || r.url); if (e === 'pdf') return 'pdf'; if (e === 'pptx' || e === 'docx') return 'packs'; return 'html'; }
function matchesFormat(r, fmt) { return !fmt || formatOf(r) === fmt || (r.files || []).some(x => (x.type === 'pdf' ? 'pdf' : 'packs') === fmt); }

const manifest = await (await fetch(new URL('Lessons/resources.json', BASE))).json();
if (!Array.isArray(manifest)) { console.error('[FAIL] resources.json is not an array'); process.exit(1); }
console.log(`resources.json over HTTP: ${manifest.length} entries`);

const browser = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await (await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true })).newPage();
const errs = [];
page.on('console', (m) => { if (m.type() === 'error') errs.push(m.text()); });
page.on('pageerror', (e) => errs.push('pageerror: ' + e.message));

await page.goto(new URL('Lessons/', BASE).href, { waitUntil: 'domcontentloaded' });
await page.waitForSelector('.scard .browse', { timeout: 20000 });
const slugs = await page.$$eval('.scard .browse', as => as.map(a => new URL(a.href).searchParams.get('subject')));
console.log(`subject cards on the hub: ${slugs.length}`);
check('#count line advertises the catalogue total', (await page.locator('#count').innerText()).startsWith(`${manifest.length} resources`), await page.locator('#count').innerText());

async function expandAll() {
  for (let i = 0; i < 300; i++) { const t = page.locator('button[data-toggle][aria-expanded="false"]').first(); if (!(await t.count())) break; await t.click(); }
  for (let i = 0; i < 300; i++) { const m = page.locator('button[data-more]').first(); if (!(await m.count())) break; await m.click(); }
}
let redFired = false;
for (const slug of slugs) {
  const pool = manifest.filter(r => cardOf(r) === slug);
  const segs = [...PATHWAYS.filter(p => pool.some(r => tierOf(r) === p)), ...(pool.some(r => !tierOf(r)) ? ['ALL'] : [])];
  for (const seg of segs) {
    await page.goto(new URL(`Lessons/subject.html?subject=${encodeURIComponent(slug)}&pathway=${seg}`, BASE).href, { waitUntil: 'domcontentloaded' });
    await page.waitForFunction(() => /lessons/.test(document.querySelector('#summary')?.textContent || ''), null, { timeout: 20000 });
    const segRows = seg === 'ALL' ? pool.filter(r => !tierOf(r)) : pool.filter(r => tierOf(r) === seg);
    const chips = await page.$$eval('#fchips button', bs => bs.map(b => b.dataset.format));
    const expectedChips = ['', ...['html', 'packs', 'pdf'].filter(f => segRows.some(r => matchesFormat(r, f)))];
    check(`${slug}/${seg}: chips present == formats present`, JSON.stringify(chips) === JSON.stringify(expectedChips), `${JSON.stringify(chips)} vs ${JSON.stringify(expectedChips)}`);
    for (const f of chips) {
      await page.locator(`#fchips button[data-format="${f}"]`).click();
      await page.waitForTimeout(80);
      await expandAll();
      if (RED && !redFired) { await page.evaluate(() => { const row = document.querySelector('.lrow'); if (row) row.remove(); }); redFired = true; }
      const got = (await page.$$eval('.lrow', els => els.map(e => e.dataset.resourcePath))).sort();
      const want = segRows.filter(r => matchesFormat(r, f)).map(r => r.file || r.url || '').sort();
      const same = got.length === want.length && got.every((x, i) => x === want[i]);
      check(`${slug}/${seg}: chip "${f || 'All formats'}" returned == filter chain`, same, `${got.length} rendered, ${want.length} expected`);
    }
  }
}
check('zero console errors', errs.length === 0, errs.length ? errs.slice(0, 3).join(' | ') : 'clean');
await browser.close();
const failed = results.filter((r) => !r.ok);
if (RED) {
  const red = failed.length >= 1;
  console.log(`\n${red ? '[PASS]' : '[FAIL]'} red proof: a removed row ${red ? 'was' : 'was NOT'} caught (${failed.length} red limb${failed.length === 1 ? '' : 's'})`);
  process.exit(red ? 0 : 1);
}
console.log(`\n${failed.length ? '[FAIL]' : '[PASS]'} chip-count gate: ${results.length - failed.length}/${results.length} limbs`);
process.exit(failed.length ? 1 : 0);
