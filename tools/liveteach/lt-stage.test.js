/* lt-stage — the LT3 stage-engine suite. Evidence, not proxies (each canvas
   claim is measured from pixels, each safety claim driven through the real
   code path — the first draft of this suite failed that bar three times and
   the fixes are pinned here):

   G1  pixel proof: sim content present inside the spotlight ROI, veil outside.
   G2  clamp both ends, both windows; wild and fractional STAGE_SET ignored.
   G3  label centred at its normalised position.
   G5/W2  crest spacing MEASURED from the canvas equals λ×px_per_m; the scale
       bar's painted length equals px_per_m; the playback chip appears off 1×
       and never covers the banner title.
   G6  a HOSTILE manifest (served by this suite's own server, never on disk)
       travels the real loader→applyStage path and renders as literal text.
   G7  external load, plus TWO honest failure modes: missing file vs broken
       content — and Escape dismisses the error.

     NODE_PATH=$(npm root -g) node tools/liveteach/lt-stage.test.js */
'use strict';
const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json' };

// Synthetic manifests served by the suite's server only — they exercise the
// engine's real loader without ever entering liveteach/manifests/ on disk.
const HOSTILE = 'window.LT_MANIFEST = { id: "g6_hostile", title: "x", units: { px_per_m: 100 }, stages: [' +
  '{ title: "<img src=x onerror=\\"window.__pwned=1\\">", mode: "wave", params: { f: 1, lambda: 2, A: 0.5 },' +
  ' copy: "<script>window.__pwned=2</scr" + "ipt>", labels: [{ x: 0.5, y: 0.5, text: "<b onclick=x>bold?</b>" }] } ] };';
const BROKEN = 'window.LT_MANIFEST = { id: "broken_v1", units: { px_per_m: 100 }, stages: [] };';

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
      if (rel === 'liveteach/manifests/g6_hostile.js') { res.writeHead(200, { 'content-type': 'text/javascript' }); res.end(HOSTILE); return; }
      if (rel === 'liveteach/manifests/broken_v1.js') { res.writeHead(200, { 'content-type': 'text/javascript' }); res.end(BROKEN); return; }
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

  /* ---------- G2: clamp at the first stage ---------- */
  const backAt0 = await proj.evaluate(() => {
    document.getElementById('btnPrev').click();
    return { st: window.__LT.stage(), btn: window.__LT.stageButtons() };
  });
  check('G2: Back at stage 1 is a no-op and the button is dead', backAt0.st.index === 0 && backAt0.btn.prevDisabled === true, JSON.stringify(backAt0.btn));
  const disStyle = await proj.evaluate(() => {
    const d = getComputedStyle(document.getElementById('btnPrev'));
    const e = getComputedStyle(document.getElementById('btnNext'));
    return { prevOpacity: Number(d.opacity), nextOpacity: Number(e.opacity) };
  });
  check('a11y: a dead stage button LOOKS dead (opacity)', disStyle.prevOpacity < 0.6 && disStyle.nextOpacity === 1, JSON.stringify(disStyle));

  /* ---------- the wave stage ---------- */
  await stripClick(proj, '#btnNext');
  const w1 = await proj.evaluate(() => ({ st: window.__LT.stage(), wave: window.__LT.wave() }));
  check('stage 2 is the wave with the manifest\'s numbers', w1.st.mode === 'wave' && w1.wave.f === 1 && w1.wave.lambda === 2, JSON.stringify(w1.wave));

  const banner = await proj.evaluate(() => ({
    title: document.querySelector('#stageBanner .st-title').textContent,
    shown: getComputedStyle(document.getElementById('stageBanner')).visibility === 'visible'
  }));
  check('banner shows the stage title', banner.shown && banner.title === 'Meet the wave', JSON.stringify(banner));

  /* ---------- W2 MEASURED: crest spacing and scale bar, from pixels ------ */
  const measured = await proj.evaluate(() => {
    const c = document.getElementById('sim');
    const g = c.getContext('2d');
    const dpr = c.width / innerWidth;
    const img = g.getImageData(0, 0, c.width, c.height).data;
    const bright = (x, y) => {
      const i = ((Math.round(y * dpr) * c.width) + Math.round(x * dpr)) * 4;
      return img[i + 3] > 80 && (img[i] > 150 || img[i + 1] > 110);
    };
    const midY = innerHeight * 0.55;
    const Atop = midY - 0.6 * 100;                  // crest line for A=0.6, px_per_m=100
    // crest tips: columns INSIDE the spotlight ROI (the undimmed hole — the
    // veil outside drops the rope below the brightness threshold) with a
    // bright pixel within 7 px of the crest line; cluster, take centres.
    const sp = window.__LT.spotlight();
    const x0 = Math.round((sp.x) * innerWidth) + 10;
    const x1 = Math.round((sp.x + sp.w) * innerWidth) - 10;
    const runs = [];
    let run = null;
    for (let x = x0; x < x1; x++) {
      let hit = false;
      for (let y = Atop - 7; y <= Atop + 7; y++) if (bright(x, y)) { hit = true; break; }
      if (hit) { if (!run) run = { a: x }; run.b = x; }
      else if (run) { runs.push((run.a + run.b) / 2); run = null; }
    }
    if (run) runs.push((run.a + run.b) / 2);
    const spacings = [];
    for (let i = 1; i < runs.length; i++) spacings.push(runs[i] - runs[i - 1]);
    // the scale bar: painted run length on its row
    const barY = innerHeight - 150;
    let barLen = 0, inBar = false, barStart = 0;
    for (let x = 10; x < 300; x++) {
      const hit = bright(x, barY);
      if (hit && !inBar) { inBar = true; barStart = x; }
      if (!hit && inBar) { inBar = false; barLen = Math.max(barLen, x - barStart); }
    }
    return { crests: runs.length, spacings, barLen, pxPerM: window.__LT.wave().pxPerM };
  });
  const spacingOK = measured.spacings.length >= 1 && measured.spacings.every(s => Math.abs(s - 200) <= 10);
  check('W2 measured: crest spacing on screen = λ × px_per_m (200 px ±10)', spacingOK, JSON.stringify(measured.spacings));
  check('W2 measured: the painted 1 m scale bar is px_per_m long (±6)', Math.abs(measured.barLen - measured.pxPerM) <= 6, String(measured.barLen));

  /* ---------- G1: the spotlight dims around the ROI, never through it ---- */
  const g1 = await proj.evaluate(() => {
    const sp = window.__LT.spotlight();
    const c = document.getElementById('sim');
    const g = c.getContext('2d');
    const dpr = c.width / innerWidth;
    const px = (nx, ny) => g.getImageData(Math.round(nx * innerWidth * dpr), Math.round(ny * innerHeight * dpr), 1, 1).data;
    let inHit = 0, inSamples = 0;
    for (let nx = sp.x + 0.01; nx < sp.x + sp.w - 0.01; nx += 0.01) {
      for (let ny = sp.y + 0.02; ny < sp.y + sp.h - 0.02; ny += 0.04) {
        const d = px(nx, ny);
        inSamples++;
        if (d[3] > 0 && (d[0] > 180 || d[1] > 120)) inHit++;
      }
    }
    const out = px(0.8, 0.1);
    return { inHit, inSamples, outAlpha: out[3], outDark: out[0] < 120 && out[1] < 120 && out[2] < 120 };
  });
  check('G1: sim content present INSIDE the spotlight ROI', g1.inHit > 5, JSON.stringify({ inHit: g1.inHit, of: g1.inSamples }));
  check('G1: the veil paints OUTSIDE the ROI (dark, non-transparent)', g1.outAlpha > 100 && g1.outDark, JSON.stringify({ a: g1.outAlpha }));

  /* ---------- playback honesty ---------- */
  await proj.evaluate(() => document.querySelector('#strip .spd[data-spd="2"]').click());
  const chip2 = await proj.evaluate(() => {
    const chip = document.getElementById('playChip');
    const title = document.querySelector('#stageBanner .st-title');
    const a = chip.getBoundingClientRect(), b = title.getBoundingClientRect();
    const overlap = a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom;
    return { vis: getComputedStyle(chip).visibility, text: chip.textContent, overlap };
  });
  check('W2: playback chip states ×2 whenever the wave is off 1×', chip2.vis === 'visible' && chip2.text === 'playback ×2', JSON.stringify(chip2));
  check('a11y: the chip never covers the stage title', chip2.overlap === false);
  await proj.evaluate(() => document.querySelector('#strip .spd[data-spd="1"]').click());
  const chip1 = await proj.evaluate(() => getComputedStyle(document.getElementById('playChip')).visibility);
  check('W2: playback chip gone at 1×', chip1 === 'hidden');

  /* ---------- HUD side: stage sync, label stage, far-end clamps ---------- */
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

  // G3: stage 4's label sits at its normalised position.
  const lbl = await proj.evaluate(() => {
    const d = document.querySelector('#stageLabels .lbl');
    if (!d) return null;
    const r = d.getBoundingClientRect();
    return { cx: r.left + r.width / 2, cy: r.top + r.height / 2, text: d.textContent, w: innerWidth, h: innerHeight };
  });
  check('G3: label centred at its normalised position (stage 4)', lbl && Math.abs(lbl.cx - .62 * lbl.w) < 3 && Math.abs(lbl.cy - .3 * lbl.h) < 3 && lbl.text.includes('amplitude'), JSON.stringify(lbl));

  const atEnd = await hud.evaluate(() => ({ disabled: document.getElementById('btnNext').disabled, seen: window.__LT.seen() }));
  check('G2: at the last stage the HUD Next is dead from broadcast state', atEnd.disabled === true && atEnd.seen.stage === 3, JSON.stringify({ stage: atEnd.seen.stage }));

  await hud.evaluate(() => LT.send('STAGE_SET', { index: 99 }));
  await proj.waitForTimeout(300);
  const clamped = await proj.evaluate(() => window.__LT.stage().index);
  check('G2: STAGE_SET beyond the end clamps to the last stage', clamped === 3, String(clamped));

  await hud.evaluate(() => LT.send('STAGE_SET', { index: 1.5 }));
  await hud.evaluate(() => LT.send('STAGE_SET', { index: 'nonsense' }));
  await proj.waitForTimeout(300);
  const fracSafe = await proj.evaluate(() => window.__LT.stage().index);
  check('G2: fractional and malformed STAGE_SET are ignored, not coerced', fracSafe === 3, String(fracSafe));

  /* ---------- G6 through the REAL path: a hostile manifest ---------- */
  const g6errs = [];
  const g6 = await ctx.newPage();
  await open(g6, base + 'projector.html?lesson=g6_hostile', g6errs);
  await g6.waitForFunction(() => window.__LT.manifestId() !== null, null, { timeout: 5000 });
  const hostile = await g6.evaluate(() => ({
    titleHtml: document.querySelector('#stageBanner .st-title').innerHTML,
    copyText: document.querySelector('#stageBanner .st-copy').textContent,
    lblHtml: (document.querySelector('#stageLabels .lbl') || {}).innerHTML,
    pwned: window.__pwned || null,
    imgs: document.querySelectorAll('#stageBanner img, #stageLabels img, #stageBanner b, #stageLabels b').length
  }));
  check('G6: hostile manifest title renders as literal text via the real path', hostile.titleHtml.startsWith('&lt;img') && hostile.pwned === null, JSON.stringify({ pwned: hostile.pwned }));
  check('G6: hostile copy and label stay literal (no elements created)', hostile.imgs === 0 && hostile.copyText.includes('<script>') && hostile.lblHtml.startsWith('&lt;b'), JSON.stringify({ imgs: hostile.imgs }));
  await g6.close();

  /* ---------- G7: two honest failure modes ---------- */
  const eerrs = [];
  const proj2 = await ctx.newPage();
  await open(proj2, base + 'projector.html?lesson=no_such_lesson', eerrs);
  await proj2.waitForTimeout(800);
  const err = await proj2.evaluate(() => ({
    vis: getComputedStyle(document.getElementById('manifestError')).visibility,
    text: document.getElementById('manifestError').textContent,
    stages: window.__LT.stage().count,
    pe: getComputedStyle(document.getElementById('manifestError')).pointerEvents
  }));
  check('G7 negative control: bogus ?lesson= shows the address-bar error, stages off', err.vis === 'visible' && err.text.includes('no_such_lesson') && err.text.includes('address bar') && err.stages === 0, JSON.stringify({ stages: err.stages }));
  check('a11y: the error informs but never intercepts taps', err.pe === 'none');
  await stripClick(proj2, '#strip .tmr[data-min="1"]');
  const stillTeaches = await proj2.evaluate(() => window.__LT.state().timer !== null);
  check('G7: timers survive a missing manifest (graceful, not dead)', stillTeaches === true);
  await proj2.keyboard.press('Escape');
  const escd = await proj2.evaluate(() => getComputedStyle(document.getElementById('manifestError')).visibility);
  check('a11y: Escape dismisses the manifest error first', escd === 'hidden');
  await proj2.close();

  const berrs = [];
  const proj3 = await ctx.newPage();
  await open(proj3, base + 'projector.html?lesson=broken_v1', berrs);
  await proj3.waitForTimeout(500);
  const berr = await proj3.evaluate(() => document.getElementById('manifestError').textContent);
  check('G7: a loaded-but-broken manifest blames the FILE, not the address bar', berr.includes('manifests/broken_v1.js') && berr.includes('broken'), berr.slice(0, 80));
  await proj3.close();

  /* ---------- a tap answers even under reduced motion ---------- */
  const rctx = await browser.newContext({ viewport: { width: 1280, height: 720 }, reducedMotion: 'reduce' });
  const rerrs = [];
  const rpage = await rctx.newPage();
  await open(rpage, base + 'projector.html', rerrs);
  await rpage.waitForFunction(() => window.__LT.manifestId() !== null, null, { timeout: 5000 });
  const tap = await rpage.evaluate(() => {
    const c = document.getElementById('sim');
    const g = c.getContext('2d');
    const count = () => {
      const d = g.getImageData(0, 0, c.width, c.height).data;
      let n = 0;
      for (let i = 3; i < d.length; i += 4) if (d[i] !== 0) n++;
      return n;
    };
    const before = count();
    c.dispatchEvent(new PointerEvent('pointerdown', { clientX: 640, clientY: 200, bubbles: true }));
    return { before, after: count(), reduced: document.body.classList.contains('reduce') };
  });
  check('a11y: a tap paints its pulse even under reduced motion', tap.reduced === true && tap.after > tap.before, JSON.stringify(tap));
  await rctx.close();

  check('console: projector clean', perrs.length === 0, perrs.join(' | '));
  check('console: HUD clean', herrs.length === 0, herrs.join(' | '));
  check('console: hostile-manifest page clean', g6errs.length === 0, g6errs.join(' | '));
  check('console: missing-manifest page had only the expected 404', eerrs.every(e => /404|Failed to load resource/.test(e)), eerrs.join(' | '));
  check('console: broken-manifest page clean', berrs.length === 0, berrs.join(' | '));

  await browser.close();
  srv.close();
  console.log(failures ? 'SUITE FAILED (' + failures + ')' : 'SUITE PASSED');
  process.exit(failures ? 1 : 0);
})().catch(e => { console.log('DIED: ' + (e && e.stack || e)); process.exit(2); });
