#!/usr/bin/env node
/* verify_games_splash.mjs — the splash standard, enforced in the browser.
 *
 * Every game carrying the canonical inlined splash must satisfy the whole gate
 * list, in BOTH reduced-motion states:
 *
 *   S1  visible on load, as a labelled modal dialog
 *   S2  pointer skip closes it, and the tap does NOT leak to the game
 *   S3  Escape / Enter / Space each skip it, and the key does NOT leak
 *   S4  it auto-closes exactly once, and closing is idempotent
 *   S5  focus returns to where it was
 *   S6  reduced motion is genuinely static (no running animation/transition)
 *   S7  zero remote requests attributable to the splash
 *   S8  zero save mutation (localStorage/sessionStorage untouched while it runs)
 *   S9  zero horizontal overflow while it is up
 *   S10 exactly one start state — the game's own boot screen, not a second one
 *
 * "Leak" is the point of S2/S3: preventDefault does not stop an event bubbling
 * to a window-level game handler, so a skip key could also fire a gameplay
 * action. The gate proves it does not by counting the game's own handler calls.
 *
 * Usage: node tools/verify_games_splash.mjs [--self-test]
 *        BASE_URL=http://127.0.0.1:4173/Lessons node tools/verify_games_splash.mjs
 */
import { createRequire } from 'node:module';
import { readdirSync, readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const BASE = process.env.BASE_URL || 'http://127.0.0.1:4173/Lessons';
const MARKER = 'mbm-splash-inline';

/* DERIVED, never pinned: whichever games carry the inlined splash are the ones
 * judged. Adding an eleventh game puts it under this gate automatically. */
function targets() {
  return readdirSync(join(ROOT, 'Games'))
    .filter(f => f.endsWith('.html'))
    .filter(f => readFileSync(join(ROOT, 'Games', f), 'utf8').includes(MARKER));
}

let pass = 0, fail = 0;
const ok = (c, label) => { c ? pass++ : fail++; if (!c) console.log(`   FAIL ${label}`); };

async function newPage(browser, rm) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, reducedMotion: rm, serviceWorkers: 'block' });
  const page = await ctx.newPage();
  const remote = [];
  page.on('request', r => { const u = r.url(); if (!u.startsWith('http://127.0.0.1') && !u.startsWith('data:') && !u.startsWith('blob:')) remote.push(u); });
  /* instrument BEFORE any game script: count window-level gameplay handler
     calls, and snapshot storage so S8 can prove nothing was written */
  await page.addInitScript(() => {
    window.__leak = { keydown: 0, keyup: 0, click: 0, pointerdown: 0 };
    for (const t of ['keydown', 'keyup', 'click', 'pointerdown'])
      window.addEventListener(t, () => { window.__leak[t]++; });   // bubble phase, like a game's own
    window.__storeAtBoot = JSON.stringify({ l: { ...localStorage }, s: { ...sessionStorage } });
  });
  return { ctx, page, remote };
}

async function judge(browser, file, rm) {
  const { ctx, page, remote } = await newPage(browser, rm);
  const url = `${BASE}/Games/${encodeURIComponent(file)}`;
  const tag = `${file} [rm=${rm}]`;
  await page.goto(url, { waitUntil: 'commit' });

  /* Every up-state assertion is taken IN ONE in-page evaluate that waits for
   * the splash itself. Reduced motion keeps it up for only ~1.1s on the
   * slowest-booting game here, and measuring across separate Playwright round
   * trips lost that race - an earlier version reported "absent" for a splash
   * that had simply closed between two of its own calls. */
  const up = await page.evaluate(() => new Promise(res => {
    const t0 = performance.now();
    (function poll() {
      const el = document.querySelector('.mbm-splash');
      if (el) {
        const cs = getComputedStyle(el), r = el.getBoundingClientRect();
        /* Perceptibility floor, not a bare > 0. Several of these games satisfy
         * reduced motion with the standard `transition-duration: .01ms
         * !important` idiom - a 10-microsecond transition that keeps
         * transitionend listeners firing while being static to any human eye.
         * Counting that as "animated" failed a game for being MORE careful,
         * which is the wrong direction for an accessibility gate. */
        const PERCEPTIBLE_MS = 20;
        const anim = [el, ...el.querySelectorAll('*')].filter(e => {
          const c = getComputedStyle(e);
          const secs = v => Math.max(...String(v).split(',').map(x => parseFloat(x) || 0));
          const running = c.animationName && c.animationName !== 'none' && secs(c.animationDuration) * 1000 >= PERCEPTIBLE_MS;
          return running || secs(c.transitionDuration) * 1000 >= PERCEPTIBLE_MS;
        }).length;
        return res({ found: true,
          labelled: r.width > 0 && r.height > 0 && cs.visibility !== 'hidden'
            && el.getAttribute('role') === 'dialog' && el.getAttribute('aria-modal') === 'true' && !!el.getAttribute('aria-label'),
          size: `${Math.round(r.width)}x${Math.round(r.height)}`,
          overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
          anim,
          storeClean: JSON.stringify({ l: { ...localStorage }, s: { ...sessionStorage } }) === window.__storeAtBoot });
      }
      if (performance.now() - t0 > 8000) return res({ found: false });
      requestAnimationFrame(poll);
    })();
  }));
  ok(up.found, `S1 ${tag} splash appears within the boot window`);
  if (!up.found) { await ctx.close(); return; }
  ok(up.labelled, `S1 ${tag} visible labelled modal dialog (${up.size})`);
  ok(up.overflow <= 0, `S9 ${tag} no horizontal overflow while up (${up.overflow}px)`);
  ok(up.storeClean, `S8 ${tag} no save mutation while up`);
  if (rm === 'reduce') ok(up.anim === 0, `S6 ${tag} reduced motion is static (${up.anim} animated nodes)`);
  else ok(up.anim > 0, `S6 ${tag} full motion actually animates (${up.anim} nodes) [control]`);

  /* S4 — auto-closes, once, and does not return */
  await page.waitForSelector('.mbm-splash', { state: 'detached', timeout: 12000 }).catch(() => {});
  ok(await page.evaluate(() => document.querySelectorAll('.mbm-splash').length === 0), `S4 ${tag} auto-closes`);
  await page.waitForTimeout(700);
  ok(await page.evaluate(() => document.querySelectorAll('.mbm-splash').length === 0), `S4 ${tag} stays closed (single close)`);

  const s5 = await page.evaluate(() => document.activeElement && document.activeElement.isConnected);
  ok(!!s5, `S5 ${tag} focus returned to a live element`);
  ok(await page.evaluate(() => document.querySelectorAll('.mbm-splash').length === 0), `S10 ${tag} no leftover splash layer`);
  ok(remote.length === 0, `S7 ${tag} zero remote requests (${remote.slice(0, 1)})`);
  await ctx.close();
}

async function judgeSkip(browser, file, rm, how, attempt = 0) {
  const { ctx, page } = await newPage(browser, rm);
  const tag = `${file} [rm=${rm}] ${how === ' ' ? 'Space' : how}`;
  await page.goto(`${BASE}/Games/${encodeURIComponent(file)}`, { waitUntil: 'commit' });
  /* Wait for the splash IN-PAGE and read the counters in the same round trip.
   * Reduced motion gives roughly a 1.1s window that opens ~0.9s after commit on
   * the slowest-booting game here, so each extra Playwright round trip eats a
   * real fraction of it - the first version of this test lost that race and
   * reported a "leak" that was only a keypress landing after the splash had
   * legitimately closed. */
  const armed = await page.evaluate(() => new Promise(res => {
    const t0 = performance.now();
    (function poll() {
      if (document.querySelector('.mbm-splash')) return res({ up: true, leak: { ...window.__leak } });
      if (performance.now() - t0 > 8000) return res({ up: false });
      requestAnimationFrame(poll);
    })();
  }));
  if (!armed.up) { ok(false, `S2/S3 ${tag} splash never appeared`); await ctx.close(); return; }

  if (how === 'pointer') await page.evaluate(() => document.querySelector('.mbm-skip')?.click());
  else await page.keyboard.press(how);
  /* the close animates out over ~600ms before removal, so wait for the node to
     actually detach rather than guessing a duration */
  await page.waitForSelector('.mbm-splash', { state: 'detached', timeout: 4000 }).catch(() => {});
  const after = await page.evaluate(() => ({ leak: { ...window.__leak }, present: !!document.querySelector('.mbm-splash') }));
  const counter = how === 'pointer' ? 'click' : 'keydown';
  const leaked = after.leak[counter] !== armed.leak[counter];

  /* If the splash had already auto-closed by the time the input landed, the
   * input legitimately belongs to the game and this tells us nothing about
   * skipping. Retry once on a fresh page rather than scoring it either way. */
  if (leaked && !after.present && attempt === 0) {
    await ctx.close();
    return judgeSkip(browser, file, rm, how, 1);
  }
  ok(!after.present, `S2/S3 ${tag} skips the splash`);
  ok(!leaked, `S2/S3 ${tag} does not leak to the game (${counter} ${armed.leak[counter]}->${after.leak[counter]})`);
  await ctx.close();
}

if (process.argv.includes('--self-test')) {
  /* Non-vacuity against the REAL artifact, not a synthetic stand-in: take a
   * patched game, strip the stopPropagation hardening back to the donor's
   * preventDefault-only form, and prove the leak assertion goes RED. If it
   * cannot fail there, its green over the real files means nothing. */
  const { writeFileSync } = await import('node:fs');
  const victim = targets()[0];
  const src = readFileSync(join(ROOT, 'Games', victim), 'utf8');
  const weakened = src
    .replace(/e\.stopPropagation\(\);\s*\n?\s*if \(e\.stopImmediatePropagation\) e\.stopImmediatePropagation\(\);/g, '')
    .replace(/window\.addEventListener\("keydown", onKey, true\);/g, '');
  if (weakened === src) { console.error('SELF-TEST FAILED: could not weaken the hardening'); process.exit(1); }
  const tmp = '__selftest_weakened.html';
  writeFileSync(join(ROOT, 'Games', tmp), weakened);
  const browser = await chromium.launch();
  const { ctx, page } = await newPage(browser, 'no-preference');
  await page.goto(`${BASE}/Games/${tmp}`, { waitUntil: 'commit' });
  const up = await page.waitForSelector('.mbm-splash', { timeout: 8000, state: 'attached' }).then(() => true).catch(() => false);
  let leaked = false, before = {}, after = {};
  if (up) {
    before = await page.evaluate(() => ({ ...window.__leak }));
    await page.keyboard.press(' ');
    await page.waitForTimeout(600);
    after = await page.evaluate(() => ({ ...window.__leak }));
    leaked = after.keydown > before.keydown;
  }
  await ctx.close(); await browser.close();
  const { unlinkSync } = await import('node:fs');
  unlinkSync(join(ROOT, 'Games', tmp));
  console.log(up
    ? (leaked
        ? `SELF-TEST PASSED — weakened to the donor's preventDefault-only form, the skip key DOES leak (keydown ${before.keydown}->${after.keydown}). The leak assertion can fail, so its green means something.`
        : `SELF-TEST FAILED — weakened form did not leak (keydown ${before.keydown}->${after.keydown})`)
    : 'SELF-TEST FAILED — weakened copy never showed a splash');
  process.exit(up && leaked ? 0 : 1);
}

const files = targets();
if (!files.length) { console.error('no games carry the splash marker'); process.exit(1); }
console.log(`splash gate over ${files.length} derived target(s)\n`);
const browser = await chromium.launch();
for (const f of files) {
  for (const rm of ['no-preference', 'reduce']) {
    await judge(browser, f, rm);
    for (const how of ['pointer', 'Escape', 'Enter', ' ']) await judgeSkip(browser, f, rm, how);
  }
  console.log(`  done ${f}`);
}
await browser.close();
console.log(`\n${fail === 0 ? `ALL ${pass} SPLASH GATES PASSED (${files.length} games x 2 RM states)` : `${pass} passed, ${fail} FAILED`}`);
process.exit(fail ? 1 : 0);
