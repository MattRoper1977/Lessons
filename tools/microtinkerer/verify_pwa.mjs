#!/usr/bin/env node
/* Micro-Tinkerer: the PWA gate.
 *
 * WHY THIS EXISTS
 * v1.2.0 shipped `navigator.serviceWorker.register('./sw.js')` against a file
 * that did not exist, and no manifest at all. The registration rejected on
 * every load into a .catch that logged a warning, so the failure was invisible
 * and the Install button — which only unhides on `beforeinstallprompt` — could
 * never appear. An install button that appears but cannot install is worse than
 * no button, so the button's gate is left exactly as it was and this gate
 * proves the two things underneath it instead.
 *
 * IT SERVES ITSELF
 * The splash and offline-runtime gates in this repo derived targets from the
 * filesystem and then fetched them from a port they never started, so they
 * measured whatever happened to be listening. This one starts its own server,
 * proves the port answers, and tears it down.
 *
 * ASSERT ON EVIDENCE, NOT ON PROXIES
 * `registration.active` being non-null proves a worker installed, not that the
 * game survives losing the network. So the offline leg reloads the page with
 * the browser genuinely offline and asserts the game reaches its own
 * ready flag, that the document was served BY the worker, and that the title is
 * the game rather than a browser error page.
 *
 * EXITS
 *   0  clean
 *   1  findings
 *   3  INCONCLUSIVE — could not get into a position to judge. Never a pass.
 */
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const argv = process.argv.slice(2);
const arg = (n) => (argv.includes(n) ? argv[argv.indexOf(n) + 1] : null);

// The manifest's icons are site-repo assets served from the same origin in
// production. Without a site tree there is nothing to resolve them against, and
// a gate that quietly skips its own assertion is the thing this estate keeps
// finding. So: declared, checked, and INCONCLUSIVE rather than green.
const SITE =
  arg('--site') ||
  process.env.MBM_SITE_ROOT ||
  ['/workspace/mattroper1977.github.io', path.join(ROOT, '..', 'mattroper1977.github.io')].find(
    (p) => p && fs.existsSync(p)
  );

const GAME_DIR = path.join(ROOT, 'Games', 'microtinkerer');
const ROUTE = '/Games/microtinkerer/';

const findings = [];
let passes = 0;
const check = (ok, label, detail = '') => {
  if (ok) { passes++; console.log(`  [PASS] ${label}${detail ? ' · ' + detail : ''}`); }
  else { findings.push(`${label}${detail ? ' · ' + detail : ''}`); console.error(`  [FAIL] ${label}${detail ? ' · ' + detail : ''}`); }
  return ok;
};
const inconclusive = (why) => {
  console.error(`\nINCONCLUSIVE: ${why}`);
  console.error('This gate did not judge anything. That is not a pass. (exit 3)');
  process.exit(3);
};

for (const f of ['index.html', 'sw.js', 'manifest.webmanifest']) {
  if (!fs.existsSync(path.join(GAME_DIR, f))) inconclusive(`Games/microtinkerer/${f} is missing — nothing to judge`);
}
if (!SITE) inconclusive('no site tree found; pass --site <path to mattroper1977.github.io> so the manifest icons can be resolved');
// A --site that does not exist is not a red manifest, it is a gate that cannot
// see the assets it is meant to judge. Saying so beats reporting four 404s as
// if the manifest were at fault.
if (!fs.existsSync(SITE) || !fs.statSync(SITE).isDirectory())
  inconclusive(`the site tree "${SITE}" is not a directory — the manifest's icons are served from it, so there is nothing to resolve them against`);

let chromium;
try { ({ chromium } = await import('playwright')); }
catch { inconclusive('playwright is not installed — npm i -D playwright && npx playwright install chromium'); }

/* ---------------------------------------------------------------- server */
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.webmanifest': 'application/manifest+json', '.json': 'application/json', '.png': 'image/png',
  '.svg': 'image/svg+xml', '.css': 'text/css' };

// Production serves the site repo at / and this repo at /Lessons/. The game is
// reached either way; what matters here is that /assets/ and the game share one
// origin, because the manifest's icon paths are absolute.
const resolve = (urlPath) => {
  const clean = decodeURIComponent(urlPath.split('?')[0]);
  const base = clean.startsWith('/Lessons/') ? [ROOT, clean.slice('/Lessons/'.length)] : null;
  const candidates = base ? [path.join(...base)] : [path.join(ROOT, clean.slice(1)), path.join(SITE, clean.slice(1))];
  for (let p of candidates) {
    try {
      if (fs.existsSync(p) && fs.statSync(p).isDirectory()) p = path.join(p, 'index.html');
      if (fs.existsSync(p) && fs.statSync(p).isFile()) return p;
    } catch { /* keep looking */ }
  }
  return null;
};

const server = http.createServer((req, res) => {
  const file = resolve(req.url);
  if (!file) { res.writeHead(404, { 'content-type': 'text/plain' }); return res.end('not found'); }
  res.writeHead(200, { 'content-type': TYPES[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const BASE = `http://127.0.0.1:${server.address().port}`;

const probe = await fetch(BASE + ROUTE).then((r) => r.status).catch(() => 0);
if (probe !== 200) { server.close(); inconclusive(`the gate's own server did not answer ${ROUTE} (got ${probe})`); }

/* ------------------------------------------------------------------ run */
console.log(`Micro-Tinkerer PWA gate · ${BASE}${ROUTE}`);
const browser = await chromium.launch({ args: ['--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader'] });
const ctx = await browser.newContext();
const page = await ctx.newPage();
const errors = [];
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });

await page.goto(BASE + ROUTE, { waitUntil: 'load', timeout: 60000 });

// EVERY JUDGEMENT HAS A DEADLINE. A service worker that fails to install never
// settles navigator.serviceWorker.ready, so an unraced await here hangs the
// whole gate instead of naming the file. The first control run did exactly
// that; this race is the only reason it now reports rather than stalls.
const reg = await page.evaluate(async () => {
  const deadline = (p, ms) => Promise.race([p, new Promise((_, rej) => setTimeout(() => rej(new Error('timed out after ' + ms + 'ms')), ms))]);
  try {
    await deadline(navigator.serviceWorker.register('./sw.js', { scope: './' }), 20000);
    const r = await deadline(navigator.serviceWorker.ready, 20000);
    return { ok: true, scope: r.scope };
  } catch (e) { return { ok: false, err: String((e && e.message) || e) }; }
});
check(reg.ok, 'service worker registration resolves', reg.ok ? reg.scope : reg.err);
check(await page.evaluate(async () => (await fetch('./sw.js', { cache: 'no-store' })).status) === 200, 'GET ./sw.js returns 200 on the served path');

const man = await page.evaluate(async () => {
  const link = document.querySelector('link[rel="manifest"]');
  if (!link) return { linked: false };
  const r = await fetch(link.href, { cache: 'no-store' });
  return { linked: true, href: link.href, status: r.status, json: r.ok ? await r.json() : null };
});
check(man.linked, '<link rel="manifest"> is present in <head>', man.href || '');
check(man.status === 200 && !!man.json, 'the manifest fetches 200 and parses', `HTTP ${man.status}`);
if (man.json) {
  const sizes = (man.json.icons || []).map((i) => i.sizes);
  check(man.json.display === 'standalone', 'manifest declares display: standalone', man.json.display);
  check(man.json.theme_color === '#17151c', 'manifest theme_color matches the page', man.json.theme_color);
  check(sizes.includes('192x192') && sizes.includes('512x512'), 'manifest declares 192 and 512 icons', sizes.join(', '));
  const icons = await page.evaluate(async (srcs) => {
    const out = {}; for (const s of srcs) out[s] = (await fetch(s, { cache: 'no-store' })).status; return out;
  }, (man.json.icons || []).map((i) => new URL(i.src, man.href).pathname));
  check(Object.values(icons).every((v) => v === 200), 'every declared icon resolves 200', JSON.stringify(icons));
}

const booted = await page.waitForFunction(() => document.documentElement.dataset.qaReady === '1', null, { timeout: 45000 }).then(() => true).catch(() => false);
const state1 = await page.evaluate(() => ({ ...document.documentElement.dataset }));
check(booted && state1.qaFatal === '0', 'the game boots on a first, online load', JSON.stringify(state1));

// The button gate is the thing that keeps a dead Install button off the menu.
const btn = await page.evaluate(() => { const b = document.querySelector('#btn-install'); return { exists: !!b, hidden: b ? b.hidden : null }; });
check(btn.exists && btn.hidden === true, 'the Install button stays hidden until the browser offers an install', JSON.stringify(btn));

await page.evaluate(() => Promise.race([
  navigator.serviceWorker.ready.then(() => new Promise((r) => setTimeout(r, 1500))),
  new Promise((r) => setTimeout(r, 20000)),
]));
check(await page.evaluate(() => !!navigator.serviceWorker.controller), 'the page is controlled by the service worker');

await ctx.setOffline(true);
const page2 = await ctx.newPage();
const served = [];
page2.on('response', (r) => served.push({ url: r.url(), sw: r.fromServiceWorker(), status: r.status() }));
let navigated = true;
await page2.goto(BASE + ROUTE, { waitUntil: 'load', timeout: 60000 }).catch(() => { navigated = false; });
check(navigated, 'a second load completes with the network offline');

const booted2 = await page2.waitForFunction(() => document.documentElement.dataset.qaReady === '1', null, { timeout: 45000 }).then(() => true).catch(() => false);
const state2 = await page2.evaluate(() => ({ ...document.documentElement.dataset })).catch(() => ({}));
check(booted2 && state2.qaFatal === '0', 'the game BOOTS with the network offline', JSON.stringify(state2));
const doc = served.find((r) => r.url.endsWith(ROUTE));
check(!!doc && doc.sw === true, 'the offline document was served by the service worker, not a cache hit on the wire', JSON.stringify(doc));
check((await page2.title().catch(() => '')).includes('Micro-Tinkerer'), 'the offline page is the game, not a browser error page');

await browser.close();
server.close();

console.log(`\n--- console errors on the online load ---\n${errors.length ? errors.join('\n') : '(none)'}`);
console.log(`\n${passes}/${passes + findings.length} passed`);
if (findings.length) { console.error(`\n${findings.length} finding(s):`); findings.forEach((f) => console.error('  · ' + f)); process.exit(1); }
console.log('PASS: the PWA registers, the manifest resolves, and the game boots offline.');
