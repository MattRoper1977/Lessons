/* lt-share — the LT6 serializer + QR suite (spec Phase 5, U1–U3, Q1–Q2).

   U1  the tag round-trips raw → URL → raw: URLSearchParams encodes exactly
       once (the fragment stored encodeURIComponent output and encoded again;
       the in-suite red control shows that double-encode NOT round-tripping).
   U2  walking a lesson uses replaceState — history.length never grows — and
       the ONE pushState is the Bookmark button, after which the browser back
       button genuinely restores the bookmarked state (popstate re-applies).
   Q1  the QR canvas is checked module-for-module against LTQR.encode of the
       exact address shown — pure black on pure white whatever the theme.
       (The decode half of Q1 lives in qr_gate.mjs against vendored jsQR.)
   Q2  the address is a selectable readonly input, pre-selected on open, and
       stays available when the address outgrows the QR's 106-byte ceiling.
   Plus: the five-key whitelist is the privacy boundary (hint prose never
   serializes), hostile boot params are clamped or dropped, the Esc order is
   blackout → share modal, and the HUD builds the projector's address from
   broadcast state with honest no-projector copy.

     NODE_PATH=$(npm root -g) node tools/liveteach/lt-share.test.js */
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

/* Compare a rendered share-QR canvas against LTQR.encode of the shown
   address, module for module, demanding PURE black or white pixels. Runs in
   the page; `flip` poisons one expected module to prove the comparator can
   fail (the suite's own red control). */
const QR_COMPARE = `(args) => {
  const code = window.LTQR.encode(args.url);
  const cv = document.getElementById('shareQR');
  if (cv.width !== code.size || cv.height !== code.size)
    return { ok: false, why: 'canvas ' + cv.width + 'px vs matrix ' + code.size };
  const d = cv.getContext('2d').getImageData(0, 0, code.size, code.size).data;
  const expected = Array.from(code.modules);
  if (typeof args.flip === 'number') expected[args.flip] ^= 1;
  for (let i = 0; i < expected.length; i++) {
    const dark = d[i * 4] === 0 && d[i * 4 + 1] === 0 && d[i * 4 + 2] === 0;
    const light = d[i * 4] === 255 && d[i * 4 + 1] === 255 && d[i * 4 + 2] === 255;
    if (!dark && !light) return { ok: false, why: 'module ' + i + ' impure: rgb(' + d[i * 4] + ',' + d[i * 4 + 1] + ',' + d[i * 4 + 2] + ')' };
    if ((expected[i] === 1) !== dark) return { ok: false, why: 'module ' + i + ' mismatch' };
  }
  return { ok: true };
}`;

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
  await proj.bringToFront();

  /* ================= U2: replaceState while teaching ================= */
  const hist0 = await proj.evaluate(() => history.length);
  await proj.keyboard.press('PageDown');
  await proj.keyboard.press('PageDown');
  await proj.keyboard.press('PageDown');
  await stripClick(proj, '#strip .spd[data-spd="2"]');
  await proj.waitForTimeout(200);
  const walked = await proj.evaluate(() => ({
    len: history.length, search: location.search, stage: window.__LT.stage().index, speed: window.__LT.state().speed
  }));
  check('U2: walking to stage 4 at 2× leaves history.length untouched', walked.len === hist0 && walked.stage === 3 && walked.speed === 2, JSON.stringify(walked));
  const wq = new URLSearchParams(walked.search);
  check('U2: the address bar mirrors the walked state', wq.get('stage') === '4' && wq.get('speed') === '2', walked.search);

  /* ================= the share modal (Q2 mechanics) ================= */
  await proj.keyboard.press('KeyQ');
  const opened = await proj.evaluate(() => ({
    shown: getComputedStyle(document.getElementById('shareOverlay')).visibility === 'visible',
    focusIsBox: document.activeElement === document.getElementById('shareURLBox'),
    selAll: document.getElementById('shareURLBox').selectionStart === 0 &&
            document.getElementById('shareURLBox').selectionEnd === document.getElementById('shareURLBox').value.length &&
            document.getElementById('shareURLBox').value.length > 0,
    boxMatchesSeam: document.getElementById('shareURLBox').value === window.__LT.share().url,
    readonly: document.getElementById('shareURLBox').readOnly
  }));
  check('Q2: Q opens the modal with the address pre-selected in a readonly box', opened.shown && opened.focusIsBox && opened.selAll && opened.readonly, JSON.stringify(opened));
  check('Q2: the box shows exactly the serializer\'s address', opened.boxMatchesSeam);

  /* ================= Q1: the canvas IS the encoded matrix ================= */
  const shownURL = await proj.evaluate(() => document.getElementById('shareURLBox').value);
  const qrOK = await proj.evaluate(eval(QR_COMPARE), { url: shownURL });
  check('Q1: every canvas module matches LTQR.encode of the shown address, pure black on white', qrOK.ok === true, qrOK.why);
  const qrRed = await proj.evaluate(eval(QR_COMPARE), { url: shownURL, flip: 200 });
  check('Q1-red: the comparator reports a single flipped module (it can fail)', qrRed.ok === false, 'comparator blind');

  /* black-on-white must survive the light theme (a scanner needs contrast) */
  await stripClick(proj, '#btnLumen');
  await proj.waitForTimeout(150);
  const shownURL2 = await proj.evaluate(() => document.getElementById('shareURLBox').value);
  const qrLight = await proj.evaluate(eval(QR_COMPARE), { url: shownURL2 });
  check('Q1: under high-lumen the QR still paints pure black-on-white (and hl=1 joined the address)', qrLight.ok === true && new URLSearchParams(shownURL2.split('?')[1]).get('hl') === '1', JSON.stringify({ why: qrLight.why, url: shownURL2 }));
  await stripClick(proj, '#btnLumen');
  await proj.waitForTimeout(150);

  /* ================= Esc order: blackout closes FIRST ================= */
  await proj.evaluate(() => document.activeElement.blur());
  await proj.keyboard.press('KeyB');
  await proj.waitForTimeout(100);
  await proj.keyboard.press('Escape');
  await proj.waitForTimeout(100);
  const esc1 = await proj.evaluate(() => ({
    blackout: window.__LT.state().blackout,
    modal: getComputedStyle(document.getElementById('shareOverlay')).visibility === 'visible'
  }));
  check('Esc order: first Escape lifts the blackout, the share modal stays', esc1.blackout === false && esc1.modal === true, JSON.stringify(esc1));
  await proj.keyboard.press('Escape');
  await proj.waitForTimeout(100);
  const esc2 = await proj.evaluate(() => getComputedStyle(document.getElementById('shareOverlay')).visibility);
  check('Esc order: second Escape closes the share modal', esc2 === 'hidden');

  /* focus returns to the opener */
  await stripClick(proj, '#btnShare');
  await proj.evaluate(() => document.activeElement.blur());
  await proj.click('#btnShareClose');
  const focusBack = await proj.evaluate(() => document.activeElement && document.activeElement.id);
  check('a11y: closing the modal hands focus back to the Share button', focusBack === 'btnShare', String(focusBack));

  /* ================= U1: tag round-trip, encoded exactly once ============ */
  const RAW_TAG = 'y10 & β 50%';
  await stripClick(proj, '#btnShare');
  await proj.fill('#shareTagInput', RAW_TAG);
  await proj.waitForTimeout(150);
  const tagged = await proj.evaluate(() => ({
    url: window.__LT.share().url,
    chip: document.getElementById('tagChip').textContent,
    chipShown: getComputedStyle(document.getElementById('tagChip')).visibility === 'visible'
  }));
  const parsedTag = new URLSearchParams(tagged.url.split('?')[1] || '').get('tag');
  check('U1: the raw tag survives URL → parse intact (one encode, one decode)', parsedTag === RAW_TAG, JSON.stringify({ parsedTag }));
  check('U1: the tag chip mirrors the raw tag via textContent', tagged.chip === RAW_TAG && tagged.chipShown, JSON.stringify(tagged.chip));
  check('U1: the address itself carries the tag percent-encoded (no raw &/β in the query value)', /tag=y10\+%26\+%CE%B2\+50%25$/.test(tagged.url), tagged.url);
  /* red control: the fragment's double-encode (encodeURIComponent stored,
     URLSearchParams encoding it AGAIN) does not round-trip */
  const doubled = new URLSearchParams();
  doubled.set('tag', encodeURIComponent(RAW_TAG));
  const doubledBack = new URLSearchParams(doubled.toString()).get('tag');
  check('U1-red: the fragment\'s double-encode would NOT round-trip', doubledBack !== RAW_TAG, doubledBack);

  /* ================= whitelist = privacy boundary ================= */
  await proj.fill('#hintInput', 'crestwatch prose never travels');
  await stripClick(proj, '#btnHint');    // hint ON, carrying the typed prose
  await proj.keyboard.press('KeyP');
  await proj.keyboard.press('Digit1');
  await proj.waitForTimeout(300);
  const busy = await proj.evaluate(() => ({
    url: window.__LT.share().url,
    hintOn: window.__LT.state().hint.on,
    hintText: window.__LT.state().hint.text,
    pollOn: window.__LT.state().poll.on,
    timer: window.__LT.state().timer !== null
  }));
  const busyKeys = [...new URLSearchParams(busy.url.split('?')[1] || '').keys()];
  const WHITELIST = ['lesson', 'stage', 'speed', 'hl', 'tag'];
  check('whitelist setup: hint (with prose), poll and timer really are live', busy.hintOn && busy.hintText.includes('crestwatch') && busy.pollOn && busy.timer, JSON.stringify(busy));
  check('whitelist: with hint+poll+timer live, only the five allowed keys appear', busyKeys.every(k => WHITELIST.includes(k)), JSON.stringify(busyKeys));
  check('whitelist: the hint prose is nowhere in the address', !busy.url.includes('crestwatch'), busy.url);
  await proj.keyboard.press('Digit0');   // clear overlays again

  /* ================= too-long: honest failure, address survives ========== */
  const BIGTAG = '€€€€€€€€€€€€€€€€€€€€€€€€';   // 24 chars → 216 percent-encoded bytes
  await proj.fill('#shareTagInput', BIGTAG);
  await proj.waitForTimeout(150);
  const tooLong = await proj.evaluate(() => ({
    msg: !document.getElementById('shareTooLong').hidden,
    qrGone: document.getElementById('shareQRBox').style.display === 'none',
    boxVal: document.getElementById('shareURLBox').value,
    selectable: (function () { var b = document.getElementById('shareURLBox'); b.focus(); b.select(); return b.selectionEnd - b.selectionStart; })()
  }));
  check('Q2: an over-capacity address shows the honest too-long line and drops the QR', tooLong.msg && tooLong.qrGone, JSON.stringify({ msg: tooLong.msg, qrGone: tooLong.qrGone }));
  check('Q2: the too-long address itself stays shown and selectable', tooLong.boxVal.includes('tag=') && tooLong.selectable === tooLong.boxVal.length, String(tooLong.selectable));
  await proj.fill('#shareTagInput', '');
  await proj.waitForTimeout(150);
  const recovered = await proj.evaluate(() => ({
    msg: !document.getElementById('shareTooLong').hidden,
    qrBack: document.getElementById('shareQRBox').style.display !== 'none',
    chipGone: getComputedStyle(document.getElementById('tagChip')).visibility === 'hidden'
  }));
  check('Q2: clearing the tag brings the QR back and retires the chip', !recovered.msg && recovered.qrBack && recovered.chipGone, JSON.stringify(recovered));
  await proj.evaluate(() => document.activeElement.blur());
  await proj.keyboard.press('Escape');   // close the modal

  /* ================= U2: Bookmark = the one pushState ================= */
  const histA = await proj.evaluate(() => history.length);
  await stripClick(proj, '#btnShare');
  await proj.click('#btnBookmark');
  await proj.waitForTimeout(150);
  const histB = await proj.evaluate(() => history.length);
  check('U2: Bookmark pushes exactly one history entry', histB === histA + 1, histA + ' -> ' + histB);
  await proj.evaluate(() => document.activeElement.blur());
  await proj.keyboard.press('Escape');
  await proj.keyboard.press('PageUp');   // move OFF the bookmarked state (4 -> 3)
  await proj.waitForTimeout(200);
  const moved = await proj.evaluate(() => ({ len: history.length, stage: window.__LT.stage().index, search: location.search }));
  check('U2: teaching on after a bookmark still adds no history', moved.len === histB && moved.stage === 2, JSON.stringify(moved));
  await proj.evaluate(() => { window.__ltNoReload = true; });
  await proj.goBack();
  await proj.waitForTimeout(300);
  const back = await proj.evaluate(() => ({
    stage: window.__LT.stage().index, speed: window.__LT.state().speed,
    search: location.search, sameDoc: window.__ltNoReload === true
  }));
  check('U2: the back button restores the bookmarked STATE (stage 4 at 2×), not just the URL', back.stage === 3 && back.speed === 2 && back.sameDoc === true, JSON.stringify(back));

  /* hotkeys stay dead inside inputs: Q types, it does not open the modal */
  await stripClick(proj, '#hintInput');
  await proj.evaluate(() => { document.getElementById('hintInput').value = ''; });
  await proj.keyboard.press('KeyQ');
  const qTyped = await proj.evaluate(() => ({
    val: document.getElementById('hintInput').value,
    modal: getComputedStyle(document.getElementById('shareOverlay')).visibility === 'visible'
  }));
  check('core guard: Q inside an input types q, never opens the modal', qTyped.val === 'q' && qTyped.modal === false, JSON.stringify(qTyped));
  await proj.keyboard.press('Escape');   // blur the input

  /* ================= hostile boot params ================= */
  const hp = [];
  const hostile = await ctx.newPage();
  await open(hostile, base + 'projector.html?stage=99&speed=7&hl=2&junk=1&lesson=waves_v1&tag=period%203', hp);
  await hostile.waitForFunction(() => window.__LT.manifestId() !== null, null, { timeout: 5000 });
  await hostile.waitForTimeout(300);
  const cleaned = await hostile.evaluate(() => ({
    search: location.search, stage: window.__LT.stage().index, speed: window.__LT.state().speed,
    chip: document.getElementById('tagChip').textContent
  }));
  const cq = new URLSearchParams(cleaned.search);
  check('boot: stage=99 clamps to the last stage; speed=7 and hl=2 fall to defaults', cleaned.stage === 3 && cleaned.speed === 1, JSON.stringify(cleaned));
  check('boot: junk params and the explicit default lesson are dropped from the address', !cq.has('junk') && !cq.has('lesson') && !cq.has('speed') && !cq.has('hl') && cq.get('stage') === '4', cleaned.search);
  check('boot: ?tag= lands in the chip raw, via textContent', cleaned.chip === 'period 3' && cq.get('tag') === 'period 3', JSON.stringify(cleaned.chip));
  check('boot: no console/page errors under hostile params', hp.length === 0, hp.join(' | '));
  await hostile.close();

  /* ================= the HUD builds the projector's address ============== */
  await proj.bringToFront();
  await proj.keyboard.press('PageUp');       // stage 4 -> 3, speed stays 2×
  await proj.waitForTimeout(300);
  await hud.bringToFront();
  await hud.keyboard.press('KeyQ');
  await hud.waitForTimeout(150);
  const hudShare = await hud.evaluate(() => ({
    shown: getComputedStyle(document.getElementById('shareOverlay')).visibility === 'visible',
    url: document.getElementById('shareURLBox').value,
    noProj: !document.getElementById('shareNoProj').hidden
  }));
  const hq = new URLSearchParams(hudShare.url.split('?')[1] || '');
  check('HUD: Q opens its modal with a PROJECTOR address built from broadcast state', hudShare.shown && /\/liveteach\/projector\.html\?/.test(hudShare.url) && hq.get('stage') === '3' && hq.get('speed') === '2', hudShare.url);
  check('HUD: with a live projector the no-projector line stays hidden', hudShare.noProj === false);
  const hudQR = await hud.evaluate(eval(QR_COMPARE), { url: hudShare.url });
  check('Q1: the HUD\'s QR canvas matches LTQR.encode of its address too', hudQR.ok === true, hudQR.why);

  /* live tracking: the projector moves, the open modal follows */
  await proj.bringToFront();
  await proj.keyboard.press('PageDown');     // 3 -> 4
  await hud.bringToFront();
  await hud.waitForTimeout(400);
  const followed = await hud.evaluate(() => new URLSearchParams(document.getElementById('shareURLBox').value.split('?')[1] || '').get('stage'));
  check('HUD: an open modal tracks the projector live (stage follows to 4)', followed === '4', String(followed));
  await hud.keyboard.press('Escape');        // Esc #1 — but focus sits in the box: blurs
  await hud.keyboard.press('Escape');        // Esc #2 closes the modal locally
  await hud.waitForTimeout(100);
  const hudEsc = await hud.evaluate(() => getComputedStyle(document.getElementById('shareOverlay')).visibility);
  check('HUD: Escape closes its own modal before deferring to the projector', hudEsc === 'hidden');

  /* ================= quiet projector: honest copy, state kept ============ */
  await proj.close();
  await hud.waitForTimeout(5300);            // past the 5 s liveness window
  await hud.keyboard.press('KeyQ');
  await hud.waitForTimeout(150);
  const stale = await hud.evaluate(() => ({
    noProj: !document.getElementById('shareNoProj').hidden,
    msg: document.getElementById('shareNoProj').textContent,
    stage: new URLSearchParams(document.getElementById('shareURLBox').value.split('?')[1] || '').get('stage')
  }));
  check('HUD honest copy: a remembered-but-silent projector says so and keeps the recovery address', stale.noProj && stale.msg.includes('last seen') && stale.stage === '4', JSON.stringify(stale));

  /* never-heard case: a lone fresh HUD shares a genuinely fresh lesson */
  const lerrs = [];
  const lonely = await ctx.newPage();
  await open(lonely, base + 'teacher.html', lerrs);
  await lonely.waitForTimeout(400);
  await lonely.keyboard.press('KeyQ');
  await lonely.waitForTimeout(150);
  const fresh = await lonely.evaluate(() => ({
    noProj: !document.getElementById('shareNoProj').hidden,
    msg: document.getElementById('shareNoProj').textContent,
    url: document.getElementById('shareURLBox').value
  }));
  check('HUD honest copy: never-heard shares a bare fresh-lesson address and says so', fresh.noProj && fresh.msg.includes('fresh') && /\/liveteach\/projector\.html$/.test(fresh.url), JSON.stringify(fresh));
  await lonely.close();

  check('no console or page errors on the projector throughout', perrs.length === 0, perrs.join(' | '));
  check('no console or page errors on the HUD throughout', herrs.length === 0, herrs.join(' | '));
  check('no console or page errors on the lone HUD', lerrs.length === 0, lerrs.join(' | '));

  await browser.close();
  srv.close();
  console.log(failures ? 'LT-SHARE: ' + failures + ' FAILURE(S)' : 'LT-SHARE: all checks passed');
  process.exit(failures ? 1 : 0);
})().catch(e => { console.error('DIED: ' + e.stack); process.exit(1); });
