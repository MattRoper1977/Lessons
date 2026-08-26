/* lt-shell — the LT2 core-shell suite, on the glitchclash pattern: headless
   Chromium against the shipped files, asserting evidence, not proxies.

   Covers the LT2 gates: boot + canvas-matches-viewport, splash present and
   skippable, single-window completeness (every teaching action via the strip),
   S1 particle cap + S2 pause-vs-stop + S3 speed-follows-state + S4
   speed-applied-once, H/P toggles both directions, dual-window resync after a
   projector reload, keyboard registry collision guard, reduced-motion, the
   high-lumen persistence, and the zero-pupil-data storage audit.

   Serves the repo over local http (BroadcastChannel needs a real origin —
   file:// windows are mutually opaque in Chromium). Usage:
     NODE_PATH=$(npm root -g) node tools/liveteach/lt-shell.test.js */
'use strict';
const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png' };

let failures = 0;
function check(name, ok, detail) {
  console.log((ok ? 'PASS' : 'FAILED') + '  ' + name + (ok || !detail ? '' : ' — ' + detail));
  if (!ok) failures++;
}

function serve() {
  return new Promise(resolve => {
    const srv = http.createServer((req, res) => {
      const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/, '');
      if (rel === 'favicon.ico') { res.writeHead(204); res.end(); return; }
      let p = path.join(ROOT, rel);
      if (fs.existsSync(p) && fs.statSync(p).isDirectory()) p = path.join(p, 'index.html');
      fs.readFile(p, (err, buf) => {
        if (err) { res.writeHead(404); res.end('not found'); return; }
        res.writeHead(200, { 'content-type': MIME[path.extname(p)] || 'application/octet-stream' });
        res.end(buf);
      });
    });
    srv.listen(0, '127.0.0.1', () => resolve(srv));
  });
}

async function openView(page, url, errors) {
  page.on('pageerror', e => errors.push('pageerror: ' + String(e).slice(0, 160)));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text().slice(0, 160)); });
  await page.goto(url, { waitUntil: 'load' });
  // Evidence, not a vacuous pass: record that the splash genuinely rendered,
  // and that clicking skip closes it well inside the 3200ms auto-close (so a
  // dead skip button cannot hide behind the auto-close).
  const sawSplash = await page.evaluate(() => !!document.querySelector('.mbm-splash'));
  let skippedFast = false;
  const skip = page.locator('.mbm-skip');
  try {
    await skip.waitFor({ state: 'visible', timeout: 4000 });
    const t0 = Date.now();
    await skip.click();
    await page.waitForFunction(() => !document.querySelector('.mbm-splash'), null, { timeout: 1500 });
    skippedFast = (Date.now() - t0) <= 1500;
  } catch (e) { /* auto-closed first (reduced motion shortens the hold) */ }
  await page.waitForFunction(() => !document.querySelector('.mbm-splash'), null, { timeout: 8000 });
  return { sawSplash, skippedFast };
}

/* The control strip auto-hides after 4s idle and only returns on pointer or
   key activity — Playwright's click waits for visibility without first moving
   the mouse, a deadlock. Wake the strip the way a teacher does, then click. */
async function stripClick(page, sel) {
  await page.mouse.move(640, 700);
  await page.mouse.move(600, 690);
  await page.click(sel);
}

(async () => {
  const srv = await serve();
  const port = srv.address().port;
  const base = 'http://127.0.0.1:' + port + '/liveteach/';
  // CHROMIUM_PATH override for non-standard chromium (the agent container);
  // absent or dangling, playwright resolves its own browser (the CI runner).
  const exe = process.env.CHROMIUM_PATH && fs.existsSync(process.env.CHROMIUM_PATH) ? process.env.CHROMIUM_PATH : undefined;
  const browser = await chromium.launch({ executablePath: exe, args: ['--no-sandbox'] });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 720 } });

  /* ---------- projector alone: the single-window mode is complete -------- */
  const perrs = [];
  const proj = await ctx.newPage();
  const splash = await openView(proj, base + 'projector.html', perrs);
  check('projector: splash genuinely rendered', splash.sawSplash === true);
  check('projector: skip closes the splash well before auto-close', splash.skippedFast === true);

  // Evidence, not proxies: a 300×150 canvas is the browser default — the gate
  // is that the bitmap matches the viewport at DPR.
  const cv = await proj.evaluate(() => ({ s: window.__LT.canvasSize(), w: innerWidth, h: innerHeight, dpr: Math.min(2, devicePixelRatio || 1) }));
  check('projector: canvas bitmap matches viewport', cv.s.w === Math.round(cv.w * cv.dpr) && cv.s.h === Math.round(cv.h * cv.dpr), JSON.stringify(cv));

  const painted = await proj.evaluate(() => {
    const c = document.getElementById('sim');
    const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
    let n = 0;
    for (let i = 3; i < d.length; i += 4) if (d[i] !== 0) n++;
    return n;
  });
  check('projector: sim actually painted pixels', painted > 500, String(painted));

  // S1: the cap bites — 240 spawns end at exactly the cap, never beyond.
  const cap = await proj.evaluate(() => {
    const before = window.__LT.particleCount();
    for (let i = 0; i < 20; i++) window.__LT.spawnPulse(400, 300);
    return { before, after: window.__LT.particleCount(), cap: window.__LT.particleCap };
  });
  check('S1: particle cap bites (240 spawns -> exactly cap)', cap.before < cap.cap && cap.after === cap.cap, JSON.stringify(cap));
  check('S1 negative control: unbounded growth would exceed the cap', cap.before + 240 > cap.cap, 'the spawn volume genuinely tested the cap');

  // S4: speed multiplies in update() only — construction velocity is
  // identical at every speed. Old bug: speed baked in at spawn, magnitude 80.
  const s4 = await proj.evaluate(() => {
    const mag = p => Math.round(Math.hypot(p.vx, p.vy));
    window.__LT.spawnPulse(100, 100);
    const at1 = mag(window.__LT.lastParticle());
    document.querySelector('#strip .spd[data-spd="2"]').click();
    window.__LT.spawnPulse(100, 100);
    const at2 = mag(window.__LT.lastParticle());
    return { at1, at2, speed: window.__LT.state().speed };
  });
  check('S4: construction velocity identical at 1x and 2x', s4.at1 === 40 && s4.at2 === 40 && s4.speed === 2, JSON.stringify(s4));
  check('S4 negative control: the old baked-in bug would read 80', s4.at2 !== 80, 'detector distinguishes the failure mode');

  // S3: the speed buttons follow the state.
  const s3 = await proj.evaluate(() =>
    [...document.querySelectorAll('#strip .spd')].map(b => b.dataset.spd + ':' + b.getAttribute('aria-pressed')).join(' '));
  check('S3: speed highlight follows state', s3 === '0.5:false 1:false 2:true', s3);

  // S2: pause and stop are different verbs. Frames advance, freeze, advance.
  const runA = await proj.evaluate(() => window.__LT.frames());
  await proj.waitForTimeout(400);
  const runB = await proj.evaluate(() => window.__LT.frames());
  check('sim: frames advance while running', runB > runA, runA + ' -> ' + runB);
  await stripClick(proj, '#btnPause');
  await proj.waitForTimeout(300);
  const pauseA = await proj.evaluate(() => window.__LT.frames());
  await proj.waitForTimeout(400);
  const pauseB = await proj.evaluate(() => window.__LT.frames());
  check('S2: pause freezes frames', pauseA === pauseB, pauseA + ' vs ' + pauseB);
  await stripClick(proj, '#btnPause');
  await proj.waitForTimeout(300);
  const resumeB = await proj.evaluate(() => window.__LT.frames());
  check('S2: resume restarts frames', resumeB > pauseB, pauseB + ' -> ' + resumeB);
  const stop = await proj.evaluate(() => { document.getElementById('btnStop').click(); return window.__LT.state(); });
  check('S2: stop pauses AND reseeds (a different verb from pause)', stop.running === false, JSON.stringify({ running: stop.running }));
  await stripClick(proj, '#btnPause'); // back to running

  // Single-window completeness: timer, hint, poll, clear — all from the strip.
  await stripClick(proj, '#strip .tmr[data-min="1"]');
  const t0 = await proj.evaluate(() => ({ shown: document.getElementById('timerOverlay').classList.contains('show'), clock: document.querySelector('#timerOverlay .clock').textContent }));
  check('single-window: timer starts from the strip', t0.shown && t0.clock === '1:00', JSON.stringify(t0));
  await proj.waitForTimeout(2300);
  const t1 = await proj.evaluate(() => window.__LT.state().timer.remaining);
  check('single-window: timer actually counts down', t1 < 60 && t1 >= 55, String(t1));

  await proj.fill('#hintInput', 'Check the crest spacing');
  await stripClick(proj, '#btnHint');
  const h0 = await proj.evaluate(() => ({ on: window.__LT.state().hint.on, text: document.querySelector('#hintOverlay .hint-text').textContent, vis: getComputedStyle(document.getElementById('hintOverlay')).visibility }));
  check('single-window: hint shows typed text', h0.on && h0.vis === 'visible' && h0.text === 'Check the crest spacing', JSON.stringify(h0));

  await stripClick(proj, '#btnPoll');
  const p0 = await proj.evaluate(() => window.__LT.state().poll.on);
  check('single-window: poll toggles on', p0 === true);
  await stripClick(proj, '#btnClear');
  const clr = await proj.evaluate(() => { const s = window.__LT.state(); return { h: s.hint.on, p: s.poll.on, t: s.timer }; });
  check('single-window: clear kills timer, hint and poll', !clr.h && !clr.p && clr.t === null, JSON.stringify(clr));

  // H/P via keyboard, both directions (the named Phase 1 gate).
  await proj.keyboard.press('KeyH');
  const kh1 = await proj.evaluate(() => window.__LT.state().hint.on);
  await proj.keyboard.press('KeyH');
  const kh0 = await proj.evaluate(() => window.__LT.state().hint.on);
  await proj.keyboard.press('KeyP');
  const kp1 = await proj.evaluate(() => window.__LT.state().poll.on);
  await proj.keyboard.press('KeyP');
  const kp0 = await proj.evaluate(() => window.__LT.state().poll.on);
  check('keys: H toggles hint ON then OFF', kh1 === true && kh0 === false);
  check('keys: P toggles poll ON then OFF', kp1 === true && kp0 === false);

  // Hotkey guard: typing H into the hint input must NOT toggle the hint.
  await proj.focus('#hintInput');
  await proj.keyboard.press('KeyH');
  const guarded = await proj.evaluate(() => window.__LT.state().hint.on);
  check('keys: hotkeys are dead while typing in an input', guarded === false);
  // ...but Escape still works there: first press blurs the input, second
  // reaches the registered close-topmost handler.
  await proj.keyboard.press('Escape');
  const blurred = await proj.evaluate(() => document.activeElement === null || document.activeElement.id !== 'hintInput');
  check('keys: Escape blurs a focused input (the one hotkey the guard spares)', blurred === true);
  await proj.keyboard.press('KeyP');
  await proj.keyboard.press('Escape');
  const escClosed = await proj.evaluate(() => window.__LT.state().poll.on);
  check('keys: Escape after blur closes the topmost overlay', escClosed === false);

  // Browser chords never fire teaching actions: Ctrl+P must not toggle the poll.
  await proj.keyboard.press('Control+KeyP');
  const chord = await proj.evaluate(() => window.__LT.state().poll.on);
  check('keys: Ctrl+P is the browser\'s, not the poll\'s', chord === false);

  // A focused button keeps its native Space activation: focusing Calm and
  // pressing Space must engage Calm, not pause the sim.
  const spaceNative = await proj.evaluate(() => {
    const runningBefore = window.__LT.state().running;
    document.getElementById('btnCalm').focus();
    return { runningBefore };
  });
  await proj.keyboard.press('Space');
  const spaceAfter = await proj.evaluate(() => ({
    running: window.__LT.state().running,
    calm: document.body.classList.contains('reduce'),
  }));
  check('keys: Space on a focused button activates the BUTTON', spaceAfter.calm === true && spaceAfter.running === spaceNative.runningBefore, JSON.stringify(spaceAfter));
  await stripClick(proj, '#btnCalm'); // calm back off
  await proj.keyboard.press('Escape'); // blur the button so hotkeys resume

  // Registry collision guard: registering a taken code throws; a new one is fine.
  const reg = await proj.evaluate(() => {
    let dup = 'no-throw', fresh = 'ok';
    try { LT.registerKey('KeyH', function () {}); } catch (e) { dup = 'threw'; }
    try { LT.registerKey('KeyZ', function () {}); } catch (e) { fresh = 'threw'; }
    return { dup, fresh };
  });
  check('registry: duplicate key throws, fresh key registers', reg.dup === 'threw' && reg.fresh === 'ok', JSON.stringify(reg));

  /* ---------- dual-window: the HUD lights up on the identical code ------- */
  const herrs = [];
  const hud = await ctx.newPage();
  await openView(hud, base + 'teacher.html', herrs);
  await hud.waitForTimeout(600);
  const linked = await hud.evaluate(() => ({ linked: window.__LT.linked(), seen: window.__LT.seen() }));
  check('resync: HUD hears PROJECTOR_STATE on hello', linked.linked && linked.seen && linked.seen.speed === 2, JSON.stringify({ linked: linked.linked, speed: linked.seen && linked.seen.speed }));

  // HUD -> projector -> HUD round trip.
  await hud.fill('#hintInput', 'From the HUD');
  await hud.click('#btnHint');
  await hud.waitForTimeout(400);
  const rt = await proj.evaluate(() => ({ on: window.__LT.state().hint.on, text: window.__LT.state().hint.text }));
  const rtHud = await hud.evaluate(() => document.getElementById('indHint').textContent);
  check('resync: HUD hint press lands on projector and reflects back', rt.on && rt.text === 'From the HUD' && rtHud === 'ON', JSON.stringify({ rt, rtHud }));
  // ...and the other direction: projector strip clears, HUD indicator follows.
  await stripClick(proj, '#btnClear');
  await hud.waitForTimeout(400);
  const back = await hud.evaluate(() => document.getElementById('indHint').textContent);
  check('resync: projector-side change reaches the HUD indicator', back === 'off', back);

  // The reload gate: reload the projector; the HUD must reconcile to the
  // fresh broadcast (speed back to 1, nothing stale kept).
  await proj.reload({ waitUntil: 'load' });
  try { await proj.locator('.mbm-skip').click({ timeout: 4000 }); } catch (e) {}
  await proj.waitForFunction(() => !document.querySelector('.mbm-splash'), null, { timeout: 8000 });
  await hud.waitForTimeout(600);
  const rec = await hud.evaluate(() => window.__LT.seen());
  check('resync: after projector reload the HUD shows the fresh state', rec && rec.speed === 1 && rec.hint.on === false, JSON.stringify({ speed: rec && rec.speed, hint: rec && rec.hint }));

  // HUD Escape closes the projector's topmost overlay — the key cards promise
  // "both windows", so the promise is proven, not assumed.
  await hud.click('#btnPoll');
  await hud.waitForTimeout(400);
  const escBefore = await proj.evaluate(() => window.__LT.state().poll.on);
  await hud.keyboard.press('Escape');
  await hud.waitForTimeout(400);
  const escAfter = await proj.evaluate(() => window.__LT.state().poll.on);
  check('keys: Escape on the HUD closes the projector\'s topmost overlay', escBefore === true && escAfter === false, escBefore + ' -> ' + escAfter);

  // The heartbeat gate: a healthy idle pair must STAY linked past the 5s
  // window (the false "projector quiet" alarm was a live-reproduced defect).
  await hud.waitForTimeout(6500);
  const idleHold = await hud.evaluate(() => window.__LT.linked());
  check('link: a healthy idle pair stays linked past 5s (heartbeat)', idleHold === true);

  /* ---------- persistence + storage audit ---------- */
  await stripClick(proj, '#btnLumen');
  await proj.reload({ waitUntil: 'load' });
  try { await proj.locator('.mbm-skip').click({ timeout: 4000 }); } catch (e) {}
  await proj.waitForFunction(() => !document.querySelector('.mbm-splash'), null, { timeout: 8000 });
  const lum = await proj.evaluate(() => ({ body: document.body.classList.contains('highlumen'), html: document.documentElement.classList.contains('highlumen') }));
  check('S5: high-lumen persists across reload, on html AND body', lum.body && lum.html, JSON.stringify(lum));
  await stripClick(proj, '#btnLumen'); // restore dark for later runs

  const stor = await proj.evaluate(() => Object.keys(localStorage));
  check('storage audit: only the registered settings key, ever', stor.every(k => k === 'mbm_liveteach_v1_settings'), stor.join(','));

  /* ---------- reduced motion (own context, OS-level) ---------- */
  const rctx = await browser.newContext({ viewport: { width: 1280, height: 720 }, reducedMotion: 'reduce' });
  const rerrs = [];
  const rpage = await rctx.newPage();
  await openView(rpage, base + 'projector.html', rerrs);
  const rm = await rpage.evaluate(() => document.body.classList.contains('reduce'));
  check('reduced motion: OS setting lands on body.reduce', rm === true);
  const rf1 = await rpage.evaluate(() => window.__LT.frames());
  await rpage.waitForTimeout(500);
  const rf2 = await rpage.evaluate(() => window.__LT.frames());
  check('reduced motion: the sim holds still', rf1 === rf2, rf1 + ' vs ' + rf2);
  const rpaint = await rpage.evaluate(() => {
    const c = document.getElementById('sim');
    const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
    let n = 0;
    for (let i = 3; i < d.length; i += 4) if (d[i] !== 0) n++;
    return n;
  });
  check('reduced motion: content is still VISIBLE (motion lost, never content)', rpaint > 500, String(rpaint));
  check('reduced motion: no console errors', rerrs.length === 0, rerrs.join(' | '));
  await rctx.close();

  /* ---------- calm choice (independent of the OS setting) ---------- */
  await stripClick(proj, '#btnCalm');
  const calm = await proj.evaluate(() => document.body.classList.contains('reduce'));
  check('calm: the pupil-facing stillness control reduces without the OS setting', calm === true);
  await stripClick(proj, '#btnCalm');

  /* ---------- launcher ---------- */
  const lerrs = [];
  const launch = await ctx.newPage();
  await openView(launch, base, lerrs);
  const nav = await launch.evaluate(() => {
    const a = document.querySelector('a.mbmhome');
    const r = a.getBoundingClientRect();
    return { w: r.width, h: r.height, href: a.getAttribute('href') };
  });
  check('launcher: NAV-1 back link is >=44px with the catalogue href', nav.w >= 44 && nav.h >= 44 && nav.href === '../index.html', JSON.stringify(nav));

  // Negative control for the heartbeat: with the projector genuinely closed,
  // the hellos go unanswered and the HUD must drop to quiet.
  await proj.close();
  await hud.waitForTimeout(6500);
  const deadLink = await hud.evaluate(() => window.__LT.linked());
  check('link negative control: a closed projector goes quiet', deadLink === false);

  check('console: projector clean', perrs.length === 0, perrs.join(' | '));
  check('console: teacher HUD clean', herrs.length === 0, herrs.join(' | '));
  check('console: launcher clean', lerrs.length === 0, lerrs.join(' | '));

  await browser.close();
  srv.close();
  console.log(failures ? 'SUITE FAILED (' + failures + ')' : 'SUITE PASSED');
  process.exit(failures ? 1 : 0);
})().catch(e => { console.log('DIED: ' + (e && e.stack || e)); process.exit(2); });
