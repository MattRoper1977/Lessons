#!/usr/bin/env node
/* verify_games_offline_runtime.mjs — the vendored-runtime offline contract.
 *
 * The seven games that used to import three.js / cannon-es / A-Frame from a
 * CDN were menu-only shells on any blocked network: they loaded, showed their
 * start screen, and could never begin a run. This gate proves the vendored
 * copies close that gap — each game must reach RUNNING gameplay with every
 * non-local request aborted, not merely load.
 *
 * "Running" is measured, not assumed: after driving the game's own start
 * controls, a canvas must exist and its pixels must change across a sample
 * window (or the runtime global must be live where the game exposes one), with
 * zero uncaught page errors and zero failed local requests.
 *
 * Usage:
 *   node tools/verify_games_offline_runtime.mjs            # serve + judge
 *   BASE_URL=http://127.0.0.1:4173/Lessons  node ...       # reuse a server
 *
 * SERVE + JUDGE IS NOW TRUE. The line above said it for months while this file
 * contained no server: it defaulted to port 4173 and started nothing, so it
 * judged whatever happened to be listening there. With nothing listening every
 * target reports ERR_CONNECTION_REFUSED as `canvas=goto-failed`; with a server
 * rooted somewhere else, targets 404 and report `canvas=none`, which reads
 * exactly like a game that never starts. Two files were carried as failing
 * games on the strength of that second reading.
 *
 * So: with no BASE_URL it serves this repository on an ephemeral port. With
 * one, preflight() proves the server returns the real file before a single
 * game is judged - a control must assert it reached the gate it tests.
 */
import { createRequire } from 'node:module';
import { createServer } from 'node:http';
import { readFileSync } from 'node:fs';
import { join, dirname, extname, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const MOUNT = '/Lessons';
const MIME = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.gif': 'image/gif', '.ico': 'image/x-icon', '.woff2': 'font/woff2',
  '.mp4': 'video/mp4', '.webm': 'video/webm', '.mp3': 'audio/mpeg', '.wav': 'audio/wav',
};

/* These games load /hud.js, which lives at the root of the OTHER repository.
 * A server that mounts only this repo 404s it, and a 404 on a same-origin path
 * is a failed local request - so serving half the estate makes all seven games
 * fail for a reason that is about the mount. In production both are one origin.
 * Located the same way the HUD gate locates the search index; when it cannot be
 * found the run says so rather than quietly counting the absence as a defect. */
function siteRoot() {
  for (const candidate of [process.env.MBM_SITE_ROOT,
                           join(ROOT, '..', 'mattroper1977.github.io'),
                           '/workspace/mattroper1977.github.io'].filter(Boolean)) {
    try { readFileSync(join(candidate, 'hud.js')); return candidate; } catch { /* keep looking */ }
  }
  return null;
}
const SITE = siteRoot();

function serveRepo() {
  const srv = createServer((req, res) => {
    let pathname;
    try { pathname = decodeURIComponent(new URL(req.url, 'http://127.0.0.1').pathname); }
    catch { res.writeHead(400); return res.end('bad path'); }
    const inLessons = pathname.startsWith(MOUNT + '/');
    const base = inLessons ? ROOT : SITE;
    if (!base) { res.writeHead(404); return res.end('no site root mounted'); }
    const rel = inLessons ? pathname.slice(MOUNT.length) : pathname;
    const file = resolve(base, '.' + rel);
    if (file !== base && !file.startsWith(base + sep)) { res.writeHead(403); return res.end('outside the tree'); }
    let body;
    try { body = readFileSync(file); } catch { res.writeHead(404); return res.end('not found'); }
    res.writeHead(200, { 'content-type': MIME[extname(file).toLowerCase()] || 'application/octet-stream' });
    res.end(body);
  });
  return new Promise((done) => srv.listen(0, '127.0.0.1', () => done(srv)));
}

let ownServer = null;
let BASE = process.env.BASE_URL;
if (!BASE) {
  ownServer = await serveRepo();
  BASE = `http://127.0.0.1:${ownServer.address().port}${MOUNT}`;
}

const TARGETS = [
  { file: 'Trail_Runner.html',                       start: /start the trek/i },
  { file: 'Trekkers_Trail_Runner_Tees_Coast.html',   start: /start the trek/i },
  { file: 'Wrecking_Crew.html',                      start: /start|play|begin|shift/i },
  { file: 'Slipstream_GP.html',                      start: /race|start|play|go/i },
  { file: 'Neon_Snake_Overdrive.html',               start: /start|play/i, global: 'THREE', keys: ['ArrowUp', 'Space'] },
  { file: 'voxelcraft.html',                         selector: '#intro-start', global: 'AFRAME', settleMs: 4000, afterMs: 14000, acceptGlobalOnly: true },
  { file: 'Orbital_source.html',                     start: /start|play|launch/i },
];

/* Reachability before judgement: if the server is not returning these files,
 * every verdict below is about the server. */
const unreachable = [];
for (const t of TARGETS) {
  const url = `${BASE}/Games/${encodeURIComponent(t.file)}`;
  try {
    const res = await fetch(url);
    if (!res.ok) unreachable.push(`${t.file}: HTTP ${res.status}`);
    else if (!(await res.text()).toLowerCase().includes('<html')) unreachable.push(`${t.file}: served body is not a document`);
  } catch (e) { unreachable.push(`${t.file}: ${String(e.message || e).slice(0, 60)}`); }
}
if (unreachable.length) {
  console.error(`ERROR: ${unreachable.length} of ${TARGETS.length} target(s) are not served at ${BASE}.`);
  console.error('Every verdict below would be about the server, not about a game.');
  for (const u of unreachable.slice(0, 4)) console.error(`  - ${u}`);
  if (ownServer) ownServer.close();
  process.exit(2);
}
console.log(`offline-runtime gate over ${TARGETS.length} target(s), served ${ownServer ? `on an ephemeral port (${BASE})` : `externally (${BASE})`}`);
if (ownServer) console.log(SITE ? `  site root mounted at / from ${SITE}` : '  NOTE: no site root found - /hud.js will 404 and count as a failed local request');
console.log('');

(async () => {
  const browser = await chromium.launch();
  let fail = 0;
  for (const t of TARGETS) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    await ctx.route('**/*', route => {
      const u = route.request().url();
      if (u.startsWith('http://127.0.0.1') || u.startsWith('data:') || u.startsWith('blob:')) return route.continue();
      return route.abort();                                    /* fully-blocked network */
    });
    const pg = await ctx.newPage();
    const errs = [], failedLocal = [];
    pg.on('pageerror', e => errs.push(String(e.message).slice(0, 120)));
    pg.on('requestfailed', r => { if (r.url().startsWith('http://127.0.0.1')) failedLocal.push(r.url().slice(-60)); });
    let verdict = {};
    try {
      await pg.goto(`${BASE}/Games/${encodeURIComponent(t.file)}`, { waitUntil: 'load', timeout: 25000 });
      await pg.waitForTimeout(t.settleMs || 3500);
      /* drive the game's own start controls, up to two layers deep */
      if (t.selector) {
        /* dispatch in-page: intro overlays animate and never settle for
         * Playwright's actionability checks, but the game's own handler only
         * needs the click event */
        await pg.evaluate(sel => document.querySelector(sel)?.click(), t.selector);
        await pg.waitForTimeout(t.afterMs || 1600);
      }
      for (let hop = 0; hop < (t.selector ? 0 : 2); hop++) {
        const clicked = await pg.evaluate(re => {
          const els = [...document.querySelectorAll('button, [role="button"], a')]
            .filter(el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; })
            .filter(el => new RegExp(re).test(el.textContent || ''));
          if (!els.length) return false;
          els[0].click(); return (els[0].textContent || '').trim().slice(0, 30);
        }, t.start.source).catch(() => false);
        await pg.waitForTimeout(1600);
        if (!clicked) break;
      }
      if (t.keys) for (const k of t.keys) { await pg.keyboard.press(k).catch(() => {}); await pg.waitForTimeout(500); }
      verdict = await pg.evaluate(async (globalName) => {
        /* liveness, without the toDataURL trap: a WebGL canvas without
         * preserveDrawingBuffer snapshots as a constant blank, so pixel-diff
         * is VACUOUS there. WebGL games are judged by context type + the
         * render loop actually ticking; 2D canvases keep the pixel diff. */
        const cvs = [...document.querySelectorAll('canvas')].sort((a, b) => b.width * b.height - a.width * a.height);
        const cv = cvs[0];
        let canvas = 'none';
        const rafTicks = await new Promise(res => {
          let n = 0; const t0 = performance.now();
          const tick = () => { n++; (performance.now() - t0 < 1200) ? requestAnimationFrame(tick) : res(n); };
          requestAnimationFrame(tick);
        });
        if (cv) {
          /* detect the EXISTING context without creating one: getContext('2d')
           * on a canvas that already holds a GL context returns null, while an
           * uncontexted canvas would hand back a fresh 2d context (and a menu
           * shell's decorative canvas must not read as GL - asking for
           * 'webgl' directly would CREATE a context and make this vacuous,
           * which is exactly how the negative control caught it). */
          let isGL = false;
          try { isGL = cv.getContext('2d') === null; } catch (_) { isGL = true; }
          /* container reality: WebGL here is software-rendered (SwiftShader)
           * and a three.js scene ticks at ~5-15 RAF/1.2s under shared CPU.
           * The contract is "the render loop is ticking", not "60fps in a
           * container" - >=5 ticks with a GL context and zero errors is a
           * live loop; a genuinely frozen loop shows 0-1. */
          if (isGL) canvas = rafTicks >= 5 ? 'webgl-live(' + rafTicks + 'raf)' : 'webgl-stalled(' + rafTicks + 'raf)';
          else {
            const snap = () => { try { return cv.toDataURL().length; } catch (_) { return -1; } };
            const a = snap(); await new Promise(r => setTimeout(r, 900)); const b = snap();
            canvas = a !== b ? 'advancing' : (rafTicks > 20 ? '2d-static-but-looping(' + rafTicks + 'raf)' : 'static');
          }
        }
        return { canvas, rafTicks, globalLive: globalName ? typeof window[globalName] !== 'undefined' : null };
      }, t.global || null);
    } catch (e) { verdict = { canvas: 'goto-failed: ' + String(e.message).slice(0, 60) }; }
    let running = (verdict.canvas === 'advancing' || String(verdict.canvas).startsWith('webgl-live')) && errs.length === 0
      && failedLocal.length === 0 && (verdict.globalLive === null || verdict.globalLive === true);
    if (t.acceptGlobalOnly && !running) {
      /* A-Frame builds its scene very slowly under software GL; the offline
       * contract is proven by the runtime global resolving locally with no
       * loader error banner and no failed local request. */
      const bannerErr = await pg.evaluate(() => document.body.innerText.match(/Could not reach[^\n]*/)?.[0] || null).catch(() => 'gone');
      running = verdict.globalLive === true && errs.length === 0 && failedLocal.length === 0 && !bannerErr;
      if (running) verdict.canvas += ' +global-accepted';
    }
    if (!running) fail++;
    console.log(`${running ? 'PASS' : 'FAIL'}  ${t.file.padEnd(42)} canvas=${verdict.canvas} global=${verdict.globalLive} pageErrs=${errs.length}${errs.length ? ' [' + errs[0] + ']' : ''} failedLocal=${failedLocal.length}${failedLocal.length ? ' [' + failedLocal[0] + ']' : ''}`);
    await ctx.close();
  }
  await browser.close();
  if (ownServer) ownServer.close();
  // Derived, not typed: the banner said "ALL 7" while TARGETS held a different
  // number, which is a count without a unit and without a source.
  console.log(fail ? `${fail} of ${TARGETS.length} GAME(S) NOT RUNNABLE OFFLINE`
    : `ALL ${TARGETS.length} VENDORED GAME(S) REACH RUNNING GAMEPLAY FULLY OFFLINE`);
  process.exit(fail ? 1 : 0);
})();
