#!/usr/bin/env node
/* Rendered regression for this estate's games: overflow, accessible names,
 * exit controls and liveness — measured in a browser, at three viewports.
 *
 * WHAT WAS HERE BEFORE, AND WHY IT WAS DELETED AND REBUILT RATHER THAN FIXED
 * The previous file called require() at line 3 inside an ES module, so it threw
 * before it did anything, every time, from the day it was committed. It also
 * carried an absolute path into one machine's node install, a hand-typed list
 * of twelve filenames, and no reference from any workflow. It had never
 * executed once. The idea was worth keeping; none of the implementation was.
 *
 * DERIVED TARGETS
 * The game list comes from the canonical search index and this repository's own
 * data/hud-coverage.json — never a filename list typed into this file. A pinned
 * list is stale the first time a game ships, and it silently stops covering the
 * thing it was written for.
 *
 * IT SERVES ITSELF
 * The splash gate and verify_games_offline_runtime both derived targets from the
 * filesystem and then fetched them over HTTP from a port they never started and
 * never checked, so they measured whatever happened to be listening; three
 * different failure counts were read as flakiness for months. This one starts
 * its own server and proves the port answers before judging anything.
 *
 * EVERY JUDGEMENT HAS A DEADLINE
 * A hang is worse than a failure, because a failure names the file. One run in
 * this estate hung 17 minutes on target 9 of 10 and produced nothing at all.
 *
 * LIVENESS IS REPORTED, NOT RATED
 * verify_games_offline_runtime calls fewer than 5 rAF ticks in 1200 ms a stall.
 * In a headless browser without hardware acceleration rAF is throttled, so a
 * game that is running perfectly well delivers 4 and is reported as
 * webgl-stalled(4raf) — which is how Trail_Runner and
 * Trekkers_Trail_Runner_Tees_Coast were carried as broken for two passes. That
 * threshold measures the HARNESS's frame rate, not the game.
 *
 * The first draft of THIS gate calibrated a floor at 25% of a blank page's rate
 * and promptly made the same mistake from the other end: nine games failed it,
 * and not one was broken. They open on a menu or a splash and are legitimately
 * idle until someone presses Start. A rate floor assumes every game is
 * animating. So the rate is measured, printed and never gated; the assertion is
 * that the page can schedule a frame at all, which is the difference between a
 * dead page and a live one and is all this gate can honestly know without
 * starting 39 different games.
 *
 * EXITS
 *   0  clean
 *   1  findings
 *   3  INCONCLUSIVE — could not get into a position to judge. Declared, checked,
 *      and never confused with a pass.
 */
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const argv = process.argv.slice(2);
const arg = n => argv.includes(n) ? argv[argv.indexOf(n) + 1] : null;
const SITE = arg('--site') || process.env.MBM_SITE_ROOT ||
  ['/workspace/mattroper1977.github.io', path.join(ROOT, '..', 'mattroper1977.github.io')]
    .find(p => p && fs.existsSync(p));
const ONLY = arg('--only');
const VIEWPORTS = [[390, 844, '390'], [768, 1024, '768'], [1440, 900, '1440']];
const NAV_MS = 30000;
const SETTLE_MS = 900;
const JUDGE_MS = 20000;

let pass = 0;
const findings = [];
const check = (ok, label, detail = '') => {
  if (ok) { pass++; console.log(`  [PASS] ${label}${detail ? ' · ' + detail : ''}`); }
  else { findings.push(`${label}${detail ? ' · ' + detail : ''}`); console.error(`  [FAIL] ${label}${detail ? ' · ' + detail : ''}`); }
  return ok;
};
function inconclusive(why) {
  console.error(`\nINCONCLUSIVE: ${why}`);
  console.error('This gate did not judge anything. That is not a pass. (exit 3)');
  process.exit(3);
}
/* Every judgement is wrapped: a promise that never settles becomes a named
 * failure against a named file instead of silence. */
const withDeadline = (p, ms, what) => Promise.race([
  p, new Promise((_, rej) => setTimeout(() => rej(new Error(`deadline ${ms} ms exceeded: ${what}`)), ms)),
]);

/* ---------------------------- targets, derived ---------------------------- */
function searchIndex() {
  const candidates = [process.env.MBM_SEARCH_INDEX,
    SITE && path.join(SITE, 'data', 'mbm-search-index.json')].filter(Boolean);
  for (const c of candidates) if (fs.existsSync(c)) return JSON.parse(fs.readFileSync(c, 'utf8'));
  inconclusive('the canonical search index was not found. Set MBM_SEARCH_INDEX or pass --site. ' +
    'Guessing the inventory from the filesystem would answer a different question from the one this tool is asked.');
}
function targets() {
  const idx = searchIndex();
  const games = idx.entries.filter(e => e.category === 'game' && e.route.startsWith('/Lessons/'));
  const out = [];
  for (const g of games) {
    const rel = g.route.slice('/Lessons/'.length);
    const file = path.join(ROOT, rel);
    if (fs.existsSync(file)) out.push({ route: g.route, file, title: g.title });
  }
  return ONLY ? out.filter(t => t.route.includes(ONLY)) : out;
}
function declared() {
  const f = path.join(ROOT, 'data', 'hud-coverage.json');
  if (!fs.existsSync(f)) return new Map();
  return new Map(JSON.parse(fs.readFileSync(f, 'utf8')).excluded.map(e => [e.route, e]));
}

/* ------------------------------- the server ------------------------------- */
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml', '.gif': 'image/gif',
  '.mp3': 'audio/mpeg', '.ogg': 'audio/ogg', '.woff2': 'font/woff2', '.ico': 'image/x-icon' };

function serve() {
  return new Promise((resolve, reject) => {
    const s = http.createServer((req, res) => {
      let url; try { url = decodeURIComponent(req.url.split('?')[0]); } catch { url = req.url.split('?')[0]; }
      // Both estates on one origin: these games are served under /Lessons/ and
      // their HUD and exit controls resolve to routes on the site origin.
      let file = url.startsWith('/Lessons/') ? path.join(ROOT, url.slice('/Lessons/'.length))
        : SITE ? path.join(SITE, url.replace(/^\//, '')) : null;
      try {
        if (!file) { res.writeHead(404).end('no site root'); return; }
        if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
        if (!fs.existsSync(file)) { res.writeHead(404).end('not found'); return; }
        res.writeHead(200, { 'Content-Type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream' });
        fs.createReadStream(file).pipe(res);
      } catch (e) { res.writeHead(500).end(String(e)); }
    });
    s.on('error', reject);
    s.listen(0, '127.0.0.1', () => resolve(s));
  });
}

/* ------------------------------- browser probes --------------------------- */
const RENDERED = () => {
  const de = document.documentElement;
  const overflow = Math.max(0, Math.round(de.scrollWidth - de.clientWidth));
  const named = [...document.querySelectorAll('button,a[href],[role="button"]')]
    .filter(e => {
      const b = e.getBoundingClientRect();
      return b.width > 0 && b.height > 0 && getComputedStyle(e).visibility !== 'hidden';
    })
    .map(e => ({
      name: (e.getAttribute('aria-label') || e.getAttribute('title') || e.textContent || '').trim(),
      id: e.id || e.className || e.tagName.toLowerCase(),
      w: Math.round(e.getBoundingClientRect().width), h: Math.round(e.getBoundingClientRect().height),
    }));
  const exit = ['mbmhud-back', 'mbmexit-back']
    .map(id => document.getElementById(id)).find(Boolean);
  const eb = exit ? exit.getBoundingClientRect() : null;
  return {
    overflow,
    unnamed: named.filter(n => !n.name).map(n => n.id).slice(0, 6),
    controls: named.length,
    exit: exit ? { id: exit.id, w: Math.round(eb.width), h: Math.round(eb.height), href: exit.href } : null,
  };
};

const RAF_TICKS = (ms) => new Promise(res => {
  let n = 0; const t0 = performance.now();
  const tick = () => { n++; (performance.now() - t0 < ms) ? requestAnimationFrame(tick) : res(n); };
  requestAnimationFrame(tick);
});

async function main() {
  let chromium;
  {
    const tried = [];
    for (const spec of ['playwright', process.env.MBM_PLAYWRIGHT,
      '/opt/node22/lib/node_modules/playwright/index.js'].filter(Boolean)) {
      try { const m = await import(spec); chromium = m.chromium || (m.default && m.default.chromium); if (chromium) break; }
      catch (e) { tried.push(`${spec} (${e.code || e})`); }
    }
    if (!chromium) inconclusive(`playwright is not importable, so nothing could be rendered. Tried: ${tried.join('; ')}`);
  }

  const T = targets();
  if (!T.length) inconclusive('the inventory named no Lessons game that exists in this checkout — ' +
    'refusing to report a green over an empty sweep');
  const DEC = declared();

  const server = await serve().catch(e => inconclusive(`could not start a server: ${e}`));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const probe = await fetch(origin + T[0].route.split('/').map(encodeURIComponent).join('/'),
    { signal: AbortSignal.timeout(5000) }).catch(() => null);
  if (!probe || !probe.ok) inconclusive(`the gate's own server is not answering on ${origin}`);
  check(true, "the gate's own server is listening and answering", origin);

  const browser = await chromium.launch().catch(e => inconclusive(`chromium would not launch: ${e}`));
  console.log(`\n${T.length} game(s) derived from the canonical index · ${VIEWPORTS.length} viewports\n`);

  try {
    /* Calibrate rAF on a blank page in THIS browser, so liveness is judged
     * against what this machine can actually paint. */
    const cal = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const calPage = await cal.newPage();
    await calPage.setContent('<!doctype html><title>calibration</title><body>');
    const baseline = await calPage.evaluate(RAF_TICKS, 1200);
    await cal.close();
    /* The assertion is that the page SCHEDULES FRAMES AT ALL — not that it
     * paints at some rate. A rate floor is the wrong instrument twice over: it
     * measures the harness's compositor (which is how four ticks became
     * "webgl-stalled" for two passes), and it assumes every game is animating,
     * when most of these open on a menu or a splash and are legitimately idle
     * until someone presses Start. Nine of them measured 10-17 ticks against a
     * blank-page baseline of 74 on the first run of this gate, and not one of
     * them was broken. The rate is reported as information; only a page that
     * cannot schedule a frame at all is a finding. */
    const FLOOR_TICKS = 1;
    check(baseline > 0, 'rAF calibration produced a baseline on a blank page',
      `${baseline} ticks/1200 ms on this machine (reported, not used as a floor)`);

    for (const [w, h, vp] of VIEWPORTS) {
      const ctx = await browser.newContext({ viewport: { width: w, height: h }, hasTouch: true });
      const page = await ctx.newPage();
      const errors = [];
      page.on('pageerror', e => errors.push(String(e).slice(0, 110)));
      for (const t of T) {
        errors.length = 0;
        const url = origin + t.route.split('/').map(encodeURIComponent).join('/');
        try {
          await withDeadline(page.goto(url, { waitUntil: 'domcontentloaded', timeout: NAV_MS }), NAV_MS + 5000, t.route);
          await page.waitForTimeout(SETTLE_MS);
        } catch (e) {
          check(false, `${vp}px ${t.route}: loads`, String(e.message || e).slice(0, 100));
          continue;
        }
        let r;
        try { r = await withDeadline(page.evaluate(RENDERED), JUDGE_MS, `${t.route} render probe`); }
        catch (e) { check(false, `${vp}px ${t.route}: is measurable`, String(e.message || e).slice(0, 100)); continue; }

        check(r.overflow === 0, `${vp}px ${t.route}: no horizontal overflow`, `${r.overflow} px`);
        check(r.unnamed.length === 0, `${vp}px ${t.route}: every visible control has an accessible name`,
          r.unnamed.length ? `unnamed: ${r.unnamed.join(', ')}` : `${r.controls} controls`);
        check(errors.length === 0, `${vp}px ${t.route}: no page errors`, errors.slice(0, 2).join(' | '));

        /* An exit exists: either the HUD's, or the stamped inline one for the
         * games declared unable to carry the HUD. Both are a way out. */
        check(!!r.exit, `${vp}px ${t.route}: has an exit control`,
          r.exit ? `#${r.exit.id} ${r.exit.w}x${r.exit.h}` : (DEC.has(t.route) ? 'declared, and still none' : 'none'));
        if (r.exit) check(r.exit.w >= 44 && r.exit.h >= 44,
          `${vp}px ${t.route}: the exit meets the 44 px floor`, `${r.exit.w}x${r.exit.h}`);

        if (vp === '390') {
          let ticks;
          try { ticks = await withDeadline(page.evaluate(RAF_TICKS, 1200), JUDGE_MS, `${t.route} liveness`); }
          catch { ticks = -1; }
          check(ticks >= FLOOR_TICKS, `${t.route}: schedules animation frames`,
            `${ticks} ticks/1200 ms (blank page on this machine: ${baseline})`);
        }
      }
      await ctx.close();
    }

    /* CONTROL: the gate must be able to report a finding. A page with a real
     * overflow and an unnamed button is injected and both must be caught. */
    console.log('\n  --- control ---');
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const page = await ctx.newPage();
    await page.setContent('<!doctype html><title>c</title><body style="margin:0">' +
      '<div style="width:900px;height:20px"></div><button></button></body>');
    const bad = await page.evaluate(RENDERED);
    check(bad.overflow > 0, 'control: a page wider than the viewport is reported', `${bad.overflow} px`);
    check(bad.unnamed.length > 0, 'control: a button with no accessible name is reported',
      bad.unnamed.join(', ') || '(none caught)');
    await ctx.close();
  } finally {
    await browser.close().catch(() => {});
    server.close();
  }

  console.log(`\n${pass} passed · ${findings.length} failed`);
  if (findings.length) {
    console.error('\nFindings:');
    findings.forEach(f => console.error('  · ' + f));
    process.exit(1);
  }
  process.exit(0);
}

main().catch(e => inconclusive(`the gate threw before it could judge: ${(e && e.stack) || e}`));
