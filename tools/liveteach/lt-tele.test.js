/* lt-tele — the LT5 telestrator suite (spec Phase 4, T1–T5). Evidence from
   pixels on both canvases:

   T2  one stroke type both directions: projector ink appears on the mini-pad,
       pad ink appears on the projector — same message, same renderer.
   T3  normalised both ways: a stroke drawn at the pad's centre lands at the
       projector's centre although the canvases differ in size; the pad
       letterboxes to the projector's broadcast aspect.
   T4  resize replays vectors: shrink the projector window and the ink is
       still there, at the same normalised position (a getImageData backup
       would have lost or misplaced it).
   T5  draw mode freezes the sim, reversibly, synced to the HUD.
   Plus: D/C in both views, malformed strokes ignored, TELE_SYNC repopulates
   a reloaded HUD.

     NODE_PATH=$(npm root -g) node tools/liveteach/lt-tele.test.js */
'use strict';
const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json' };

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

async function open(page, url, errors) {
  page.on('pageerror', e => errors.push('pageerror: ' + String(e).slice(0, 160)));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text().slice(0, 160)); });
  await page.goto(url, { waitUntil: 'load' });
  try { await page.locator('.mbm-skip').click({ timeout: 4000 }); } catch (e) {}
  await page.waitForFunction(() => !document.querySelector('.mbm-splash'), null, { timeout: 8000 });
}

(async () => {
  const srv = await serve();
  const port = srv.address().port;
  const base = 'http://127.0.0.1:' + port + '/liveteach/';
  const exe = process.env.CHROMIUM_PATH && fs.existsSync(process.env.CHROMIUM_PATH) ? process.env.CHROMIUM_PATH : undefined;
  const browser = await chromium.launch({ executablePath: exe, args: ['--no-sandbox'] });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 720 } });

  const perrs = [];
  const proj = await ctx.newPage();
  await open(proj, base + 'projector.html', perrs);
  await proj.waitForFunction(() => window.__LT.manifestId() !== null, null, { timeout: 5000 });
  const herrs = [];
  const hud = await ctx.newPage();
  await open(hud, base + 'teacher.html', herrs);
  await hud.waitForTimeout(500);

  /* ---------- T5: D freezes the sim, synced ---------- */
  await proj.bringToFront();
  await proj.keyboard.press('KeyD');
  await hud.waitForTimeout(400);
  const on = await proj.evaluate(() => ({ tele: window.__LT.tele().active, running: window.__LT.state().running }));
  const f1 = await proj.evaluate(() => window.__LT.frames());
  await proj.waitForTimeout(400);
  const f2 = await proj.evaluate(() => window.__LT.frames());
  const hudSeesOn = await hud.evaluate(() => ({ tele: window.__LT.seen().telestrator, pressed: document.getElementById('btnDraw').getAttribute('aria-pressed') }));
  check('T5: D turns draw mode on and freezes the sim', on.tele === true && on.running === false && f1 === f2, JSON.stringify(on));
  check('T5: the HUD sees draw mode on (state + button)', hudSeesOn.tele === true && hudSeesOn.pressed === 'true', JSON.stringify(hudSeesOn));

  /* ---------- draw on the projector; ink lands on both canvases ---------- */
  await proj.mouse.move(300, 260);
  await proj.mouse.down();
  await proj.mouse.move(420, 320, { steps: 8 });
  await proj.mouse.up();
  await hud.waitForTimeout(400);
  const midN = { x: 360 / 1280, y: 290 / 720 };
  const projInk = await proj.evaluate(n => ({ count: window.__LT.tele().strokes, at: window.__LT.inkAt(n.x, n.y) }), midN);
  const padInk = await hud.evaluate(n => ({ count: window.__LT.pad().strokes, at: window.__LT.padInkAt(n.x, n.y) }), midN);
  check('T2/T3: projector stroke lands as ink on the projector', projInk.count === 1 && projInk.at === true, JSON.stringify(projInk));
  check('T2/T3: the SAME stroke message paints the mini-pad at the same normalised spot', padInk.count === 1 && padInk.at === true, JSON.stringify(padInk));

  /* ---------- draw on the pad; ink lands on the (bigger) projector ------- */
  await hud.locator('#pad').scrollIntoViewIfNeeded();
  const padBox = await hud.evaluate(() => {
    const r = document.getElementById('pad').getBoundingClientRect();
    return { x: r.left, y: r.top, w: r.width, h: r.height };
  });
  await hud.mouse.move(padBox.x + padBox.w * 0.5, padBox.y + padBox.h * 0.5);
  await hud.mouse.down();
  await hud.mouse.move(padBox.x + padBox.w * 0.7, padBox.y + padBox.h * 0.5, { steps: 6 });
  await hud.mouse.up();
  await proj.waitForTimeout(400);
  const crossInk = await proj.evaluate(() => ({ count: window.__LT.tele().strokes, at: window.__LT.inkAt(0.6, 0.5) }));
  check('T3: a pad stroke renders at its normalised position on the different-sized projector', crossInk.count === 2 && crossInk.at === true, JSON.stringify(crossInk));

  /* ---------- T3: the pad letterboxes to the projector aspect ------------ */
  const aspect = await hud.evaluate(() => ({ pad: window.__LT.pad().aspect, seen: window.__LT.seen().aspect }));
  check('T3: mini-pad aspect equals the broadcast projector aspect', Math.abs(aspect.pad - aspect.seen) / aspect.seen < 0.03, JSON.stringify(aspect));

  /* ---------- T4: resize replays the vectors ---------- */
  await proj.setViewportSize({ width: 1000, height: 600 });
  await proj.waitForTimeout(400);
  const resized = await proj.evaluate(n => ({ at: window.__LT.inkAt(n.x, n.y), count: window.__LT.tele().strokes }), midN);
  check('T4: after a resize the ink is still there, at the same normalised spot', resized.at === true && resized.count === 2, JSON.stringify(resized));
  await proj.setViewportSize({ width: 1280, height: 720 });
  await proj.waitForTimeout(300);

  /* ---------- malformed strokes are ignored silently ---------- */
  await hud.evaluate(() => {
    LT.send('TELE_STROKE', { pts: [[0.5, 0.5]], color: 'red', width: 0.01 });
    LT.send('TELE_STROKE', { pts: 'nonsense', color: '#ff0000', width: 0.01 });
    LT.send('TELE_STROKE', { pts: [[0.5, 0.5]], color: '#ff0000', width: 99 });
  });
  await proj.waitForTimeout(300);
  const afterBad = await proj.evaluate(() => window.__LT.tele().strokes);
  check('bus posture: malformed strokes are ignored, count unchanged', afterBad === 2, String(afterBad));

  /* ---------- TELE_SYNC repopulates a reloaded HUD ---------- */
  await hud.reload({ waitUntil: 'load' });
  try { await hud.locator('.mbm-skip').click({ timeout: 4000 }); } catch (e) {}
  await hud.waitForFunction(() => !document.querySelector('.mbm-splash'), null, { timeout: 8000 });
  await hud.waitForTimeout(700);
  const resynced = await hud.evaluate(() => window.__LT.pad().strokes);
  check('resync: a reloaded HUD gets the full ink back (TELE_SYNC)', resynced === 2, String(resynced));

  /* ---------- C clears everywhere; D off resumes the sim ---------- */
  await hud.bringToFront();
  await hud.keyboard.press('KeyC');
  await proj.waitForTimeout(300);
  const cleared = await proj.evaluate(n => ({ count: window.__LT.tele().strokes, at: window.__LT.inkAt(n.x, n.y) }), midN);
  const padCleared = await hud.evaluate(() => window.__LT.pad().strokes);
  check('C on the HUD clears the ink on both screens', cleared.count === 0 && cleared.at === false && padCleared === 0, JSON.stringify(cleared));

  await hud.keyboard.press('KeyD');   // TELE_SET off (from seen: on)
  await proj.waitForTimeout(400);
  const off = await proj.evaluate(() => ({ tele: window.__LT.tele().active, running: window.__LT.state().running }));
  await proj.bringToFront();          // a backgrounded page throttles rAF — front it before counting frames
  const f3 = await proj.evaluate(() => window.__LT.frames());
  await proj.waitForTimeout(400);
  const f4 = await proj.evaluate(() => window.__LT.frames());
  check('T5: draw mode off restores the sim, reversibly', off.tele === false && off.running === true && f4 > f3, JSON.stringify(off));

  /* ---------- storage audit still holds: ink persists nowhere ------------ */
  const stor = await proj.evaluate(() => Object.keys(localStorage));
  check('storage audit: the telestrator writes no storage', stor.every(k => k === 'mbm_liveteach_v1_settings'), stor.join(','));

  check('console: projector clean', perrs.length === 0, perrs.join(' | '));
  check('console: HUD clean', herrs.length === 0, herrs.join(' | '));

  await browser.close();
  srv.close();
  console.log(failures ? 'SUITE FAILED (' + failures + ')' : 'SUITE PASSED');
  process.exit(failures ? 1 : 0);
})().catch(e => { console.log('DIED: ' + (e && e.stack || e)); process.exit(2); });
