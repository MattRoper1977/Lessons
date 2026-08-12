#!/usr/bin/env node
/* The deck's browser leg, on the built bytes over HTTP — B3.3.
 *
 * The deck is one file that mounts two embedded apps in Blob iframes. Static
 * gates already proved the embeds decode byte-equal to the PUBLISHED
 * standalones; this proves the assembled thing BEHAVES: four task cards
 * including the Wheatstone extension, both frames boot the real apps, the
 * splash fires once at deck level and the framed copies' guard keeps them
 * quiet, and "Collect evidence now" round-trips the postMessage protocol to
 * BOTH tools. Zero console errors tolerated, in the deck or in either frame.
 *
 * Run against a mount shaped like the real origin (site at /, this repo at
 * /Lessons/) because the deck loads /hud.js from the site root:
 *
 *   node tools/verify_wave_ohm_deck.mjs --base http://127.0.0.1:PORT/
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
const DECK = 'Lessons/Physics_WaveOhm/made-by-matt-wave-ohm-complete-offline-lesson-v2-3.html';

const results = [];
const check = (limb, ok, detail) => {
  results.push({ limb, ok });
  console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${String(limb).padEnd(52)} ${detail}`);
  return ok;
};

const browser = await chromium.launch({
  args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
});
const ctx = await browser.newContext({ viewport: { width: 1280, height: 1000 } });
const page = await ctx.newPage();
const errs = [];
// One listener catches the deck AND both frames — console events bubble to the page.
page.on('console', (m) => { if (m.type() === 'error') errs.push(m.text()); });
page.on('pageerror', (e) => errs.push('pageerror: ' + e.message));

await page.goto(new URL(DECK, BASE).href, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1500);

console.log('\nsplash — once, at deck level only');
{
  const n = await page.evaluate(() => document.querySelectorAll('.mbm-splash').length);
  check('splash overlay present at deck level', n === 1, `count ${n} (want 1)`);
  const t = await page.evaluate(() => (document.querySelector('.mbm-splash') || {}).textContent || '');
  check('splash carries the deck title', t.includes('WAVE & OHM INVESTIGATION'), JSON.stringify(t.trim().slice(0, 48)));
  const skip = page.locator('.mbm-splash .mbm-skip');
  const box = await skip.boundingBox().catch(() => null);
  check('Skip visible and >=44px tall', !!box && box.height >= 44, box ? `${Math.round(box.width)}x${Math.round(box.height)}` : 'no box');
  await skip.click();
  await page.waitForTimeout(700);
  const gone = await page.evaluate(() => document.querySelectorAll('.mbm-splash').length);
  check('Skip dismisses the splash', gone === 0, `count after ${gone}`);
}

console.log('\nhud + frames');
{
  const chip = page.locator('#mbmhud-back, #mbmhud-home, #mbmhud-pill').first();
  const cb = await chip.boundingBox().catch(() => null);
  check('hud chip mounted from /hud.js', !!cb && cb.width > 0 && cb.height > 0, cb ? `${Math.round(cb.width)}x${Math.round(cb.height)}` : 'no box');
  const metas = await page.evaluate(() => [...document.querySelectorAll('.tool-frame')].map((f) => ({
    id: f.dataset.id, tool: f.dataset.tool, blob: f.src.startsWith('blob:'),
  })));
  check('two tool frames, both from Blob URLs', metas.length === 2 && metas.every((m) => m.blob),
    metas.map((m) => `${m.id}:${m.tool}${m.blob ? '' : ' NOT-BLOB'}`).join(' · '));
  // The frames are same-origin blob documents — reach inside each one.
  await page.waitForTimeout(2000); // let both apps finish booting
  for (const f of page.frames()) {
    if (f === page.mainFrame()) continue;
    const r = await f.evaluate(() => ({
      title: document.title,
      splashes: document.querySelectorAll('.mbm-splash').length,
      // The guard's whole job: framed start() is a no-op, not the builder.
      start: window.MadeByMattSplash ? String(window.MadeByMattSplash.start) : '(no module)',
    })).catch((e) => ({ title: 'EVAL FAILED: ' + e.message, splashes: -1, start: '' }));
    const name = r.title.includes('Iridescence') ? 'wave' : r.title.includes('Fault-Finder') ? 'ohm' : '?';
    check(`frame boots the published app (${name})`, r.title.endsWith('— Made by Matt'), JSON.stringify(r.title.slice(0, 56)));
    check(`no splash inside the ${name} frame`, r.splashes === 0, `overlays ${r.splashes}`);
    // Assert the guard's EXACT replacement — the no-op the build tool installs
    // — not a length guess. A first draft guessed "< 40 chars" and reddened on
    // the real 51-char no-op: the instrument was wrong, not the guard.
    const NOOP = 'function(){return{close:function(){},element:null}}';
    check(`${name} frame guard replaced start() with the no-op`,
      r.start === NOOP, r.start === NOOP ? 'source identical' : JSON.stringify(r.start.slice(0, 60)));
  }
}

console.log('\ntask cards');
{
  await page.click('#tasksBtn');
  await page.waitForTimeout(400);
  const cards = await page.evaluate(() => [...document.querySelectorAll('#taskList article.task')].map(
    (c) => (c.querySelector('h3') || {}).textContent || ''));
  check('four task cards render', cards.length === 4, `count ${cards.length}: ${cards.map((c) => c.slice(0, 24)).join(' | ')}`);
  check('the Wheatstone extension is one of them',
    cards.some((c) => c.includes('Wheatstone Bridge Balance Extension')), cards[3] || '(none)');
}

console.log('\nevidence collection — the postMessage round-trip, both tools');
{
  await page.click('#evidenceBtn');
  await page.waitForTimeout(400);
  await page.click('#collectBtn');
  await page.waitForTimeout(1600); // collect() closes its listener window at 1100ms
  const items = await page.evaluate(() => [...document.querySelectorAll('#evidenceList .evidence-item')].map(
    (d) => (d.querySelector('b') || {}).textContent || d.textContent));
  const tools = new Set(items.map((t) => String(t).trim()));
  check('both tools answered mbm-export-results', items.length === 2 && tools.size === 2,
    `${items.length} record(s): ${[...tools].join(' · ')}`);
  const status = await page.evaluate(() => (document.getElementById('status') || {}).textContent || '');
  check('deck announces the collection', /2 results collected/.test(status), JSON.stringify(status.trim()));
}

console.log('\nconsole');
check('zero console errors across deck and frames', errs.length === 0, errs.length ? errs.slice(0, 3).join(' | ') : 'clean');

await browser.close();
const failed = results.filter((r) => !r.ok);
console.log(`\n${failed.length ? '[FAIL]' : '[PASS]'} deck browser leg: ${results.length - failed.length}/${results.length} limbs`);
process.exit(failed.length ? 1 : 0);
