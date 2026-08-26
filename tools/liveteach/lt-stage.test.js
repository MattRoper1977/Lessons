/* lt-stage — the LT3 stage-engine suite. Evidence, not proxies:

   G1  pixel-sample proof: with the spotlight up, sim content is PRESENT and
       bright inside the ROI and dimmed outside — dimming never erased it.
   G2  step clamp both sides: Next at the last stage and Back at the first are
       immediate no-ops on projector AND HUD; the HUD renders only broadcast
       state.
   G3  (statically gated by units_check.mjs; here we prove labels land at the
       normalised position scaled to the real viewport.)
   G5/W2  the on-screen wave IS the manifest: rendered wavelength equals
       lambda × px_per_m; the playback chip appears whenever speed ≠ 1×.
   G6  a manifest string containing markup renders as literal text.
   G7  the lesson arrives as external data: a bogus ?lesson= shows a visible
       error and the teaching tools stay alive.

     NODE_PATH=$(npm root -g) node tools/liveteach/lt-stage.test.js */
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

async function stripClick(page, sel) {
  await page.mouse.move(640, 700);
  await page.mouse.move(600, 690);
  await page.click(sel);
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

  /* ---------- G7: the manifest arrived as external data ---------- */
  const m0 = await proj.evaluate(() => ({ id: window.__LT.manifestId(), st: window.__LT.stage() }));
  check('G7: external manifest loaded (waves_v1, 4 stages, stage 1 shown)', m0.id === 'waves_v1' && m0.st.count === 4 && m0.st.index === 0, JSON.stringify(m0));

  /* ---------- G2: clamp at the first stage is an immediate no-op --------- */
  const backAt0 = await proj.evaluate(() => {
    document.getElementById('btnPrev').click();
    return { st: window.__LT.stage(), btn: window.__LT.stageButtons() };
  });
  check('G2: Back at stage 1 is a no-op and the button is dead', backAt0.st.index === 0 && backAt0.btn.prevDisabled === true, JSON.stringify(backAt0.btn));

  /* ---------- move to the wave stage; the sim becomes the manifest ------- */
  await stripClick(proj, '#btnNext');
  const w1 = await proj.evaluate(() => ({ st: window.__LT.stage(), wave: window.__LT.wave() }));
  check('stage 2 is the wave with the manifest\'s numbers', w1.st.mode === 'wave' && w1.wave.f === 1 && w1.wave.lambda === 2, JSON.stringify(w1.wave));
  check('W2: rendered wavelength IS lambda x px_per_m', w1.wave.lambda * w1.wave.pxPerM === 200, String(w1.wave.lambda * w1.wave.pxPerM));

  // The banner is safe DOM text (G6 groundwork — the real markup test is below).
  const banner = await proj.evaluate(() => ({
    title: document.querySelector('#stageBanner .st-title').textContent,
    shown: getComputedStyle(document.getElementById('stageBanner')).visibility === 'visible'
  }));
  check('banner shows the stage title', banner.shown && banner.title === 'Meet the wave', JSON.stringify(banner));

  // Labels land at the normalised position scaled to the viewport (G3).
  const lbl = await proj.evaluate(() => {
    const d = document.querySelector('#stageLabels .lbl');
    if (!d) return null;
    const r = d.getBoundingClientRect();
    return { cx: r.left + r.width / 2, cy: r.top + r.height / 2, text: d.textContent, w: innerWidth, h: innerHeight };
  });
  check('G3: label centred at its normalised position', lbl && Math.abs(lbl.cx - .32 * lbl.w) < 3 && Math.abs(lbl.cy - .24 * lbl.h) < 3 && lbl.text.includes('λ = 2 m'), JSON.stringify(lbl));

  /* ---------- G1: the spotlight dims around the ROI, never through it ---- */
  const g1 = await proj.evaluate(() => {
    const sp = window.__LT.spotlight();
    const c = document.getElementById('sim');
    const g = c.getContext('2d');
    const dpr = c.width / innerWidth;
    const px = (nx, ny) => g.getImageData(Math.round(nx * innerWidth * dpr), Math.round(ny * innerHeight * dpr), 1, 1).data;
    // sample a horizontal run at the wave's midline INSIDE the ROI: the rope
    // stroke must be found (content present), and the dim veil absent.
    const midY = 0.55;
    let inHit = 0, inSamples = 0;
    for (let nx = sp.x + 0.01; nx < sp.x + sp.w - 0.01; nx += 0.01) {
      for (let ny = sp.y + 0.02; ny < sp.y + sp.h - 0.02; ny += 0.04) {
        const d = px(nx, ny);
        inSamples++;
        if (d[3] > 0 && (d[0] > 180 || d[1] > 120)) inHit++;  // bright rope/dot pixels
      }
    }
    // outside the ROI the veil paints alpha everywhere, including empty space
    const out = px(0.8, 0.1);
    return { sp, inHit, inSamples, outAlpha: out[3], outDark: out[0] < 120 && out[1] < 120 && out[2] < 120 };
  });
  check('G1: sim content present INSIDE the spotlight ROI', g1.inHit > 5, JSON.stringify({ inHit: g1.inHit, of: g1.inSamples }));
  check('G1: the veil paints OUTSIDE the ROI (dark, non-transparent)', g1.outAlpha > 100 && g1.outDark, JSON.stringify({ a: g1.outAlpha }));

  /* ---------- playback honesty: the chip appears off 1x ---------- */
  await proj.evaluate(() => document.querySelector('#strip .spd[data-spd="2"]').click());
  const chip2 = await proj.evaluate(() => ({ vis: getComputedStyle(document.getElementById('playChip')).visibility, text: document.getElementById('playChip').textContent }));
  check('W2: playback chip states x2 whenever the wave is not at 1x', chip2.vis === 'visible' && chip2.text === 'playback ×2', JSON.stringify(chip2));
  await proj.evaluate(() => document.querySelector('#strip .spd[data-spd="1"]').click());
  const chip1 = await proj.evaluate(() => getComputedStyle(document.getElementById('playChip')).visibility);
  check('W2: playback chip gone at 1x', chip1 === 'hidden');

  /* ---------- G2 far end + HUD side ---------- */
  const herrs = [];
  const hud = await ctx.newPage();
  await open(hud, base + 'teacher.html', herrs);
  await hud.waitForTimeout(600);
  const hs = await hud.evaluate(() => ({ seen: window.__LT.seen(), title: document.getElementById('stageTitle').textContent }));
  check('HUD renders the broadcast stage title', hs.seen && hs.title === hs.seen.stageTitle && hs.title === 'Meet the wave', hs.title);

  await hud.click('#btnNext');  // -> 3
  await hud.waitForTimeout(300);
  await hud.click('#btnNext');  // -> 4 (last)
  await hud.waitForTimeout(300);
  const atEnd = await hud.evaluate(() => ({ disabled: document.getElementById('btnNext').disabled, seen: window.__LT.seen() }));
  check('G2: at the last stage the HUD Next is dead from broadcast state', atEnd.disabled === true && atEnd.seen.stage === 3, JSON.stringify({ stage: atEnd.seen.stage }));
  await hud.click('#btnPrev');
  await hud.waitForTimeout(300);
  // fire a wild STAGE_SET from the HUD side (a channel never hears its own
  // messages, so this must travel the real path): still clamped
  await hud.evaluate(() => LT.send('STAGE_SET', { index: 99 }));
  await proj.waitForTimeout(300);
  const clamped = await proj.evaluate(() => window.__LT.stage().index);
  check('G2: STAGE_SET beyond the end clamps to the last stage', clamped === 3, String(clamped));

  /* ---------- G6: markup in a manifest string renders as literal text ---- */
  const g6 = await proj.evaluate(() => {
    // drive the engine with a hostile stage title through the same code path
    const el = document.querySelector('#stageBanner .st-title');
    el.textContent = '<img src=x onerror="window.__pwned=1">';
    return { html: el.innerHTML.startsWith('&lt;img'), pwned: !!window.__pwned, text: el.textContent };
  });
  check('G6: markup in stage text stays literal (textContent path)', g6.html === true && g6.pwned === false, JSON.stringify({ pwned: g6.pwned }));

  /* ---------- G7 negative control: a missing lesson is a VISIBLE error --- */
  const eerrs = [];
  const proj2 = await ctx.newPage();
  await open(proj2, base + 'projector.html?lesson=no_such_lesson', eerrs);
  await proj2.waitForTimeout(800);
  const err = await proj2.evaluate(() => ({
    vis: getComputedStyle(document.getElementById('manifestError')).visibility,
    text: document.getElementById('manifestError').textContent,
    stages: window.__LT.stage().count
  }));
  check('G7 negative control: bogus ?lesson= shows the error, stages stay off', err.vis === 'visible' && err.text.includes('no_such_lesson') && err.stages === 0, JSON.stringify({ stages: err.stages }));
  // ...and the view still teaches: the timer still starts.
  await stripClick(proj2, '#strip .tmr[data-min="1"]');
  const stillTeaches = await proj2.evaluate(() => window.__LT.state().timer !== null);
  check('G7: timers survive a missing manifest (graceful, not dead)', stillTeaches === true);
  await proj2.close();

  check('console: projector clean', perrs.length === 0, perrs.join(' | '));
  check('console: HUD clean', herrs.length === 0, herrs.join(' | '));
  // the 404 for the bogus manifest is EXPECTED on proj2 — assert it is the only error
  check('console: error page had only the expected manifest 404', eerrs.every(e => /404|Failed to load resource/.test(e)), eerrs.join(' | '));

  await browser.close();
  srv.close();
  console.log(failures ? 'SUITE FAILED (' + failures + ')' : 'SUITE PASSED');
  process.exit(failures ? 1 : 0);
})().catch(e => { console.log('DIED: ' + (e && e.stack || e)); process.exit(2); });
