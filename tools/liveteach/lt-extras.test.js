/* lt-extras — the LT8 classroom-extras suite (spec Phase 7, X1–X4).
   The spec names two gates for this phase; both are here on evidence:

   AUDIO DEFAULTS (X3)  nothing makes a sound until a teacher says so, and the
       choice does NOT survive a reload. In an SEMH room a toggle that
       remembers "on" from last lesson is the surprise the rule exists to
       prevent, so this suite proves the absence of persistence, not just the
       initial value. Live oscillator counting distinguishes a silent-but-
       wired path from a working one (the gc-music lesson, applied here).
   REDUCED-MOTION BELL (X2)  under prefers-reduced-motion the bell must be a
       STATIC banner, not a flash — the house rule's named substitution. The
       check reads the computed animation, not a class name.

   Plus X1 (counts only, anonymous, both directions, reset, shown in text) and
   X4 (a real SVG built from the recorded series, with the clipboard-blocked
   fallback exercised).

     NODE_PATH=$(npm root -g) node tools/liveteach/lt-extras.test.js */
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

/* Count LIVE oscillators, not "did we call a function". A wired-but-silent
   audio path and a working one are indistinguishable without this. */
const AUDIO_PROBE = `() => {
  window.__osc = { started: 0, peakGain: 0, stopped: 0 };
  const AC = window.AudioContext || window.webkitAudioContext;
  if (!AC) return;
  const realOsc = AC.prototype.createOscillator;
  const realGain = AC.prototype.createGain;
  AC.prototype.createOscillator = function () {
    const o = realOsc.call(this);
    const start = o.start.bind(o), stop = o.stop.bind(o);
    o.start = function (t) { window.__osc.started++; return start(t); };
    o.stop = function (t) { window.__osc.stopped++; return stop(t); };
    return o;
  };
  AC.prototype.createGain = function () {
    const g = realGain.call(this);
    const ramp = g.gain.exponentialRampToValueAtTime.bind(g.gain);
    g.gain.exponentialRampToValueAtTime = function (v, t) {
      window.__osc.peakGain = Math.max(window.__osc.peakGain, v);
      return ramp(v, t);
    };
    return g;
  };
  window.__speech = [];
  if (window.speechSynthesis) {
    const realSpeak = window.speechSynthesis.speak.bind(window.speechSynthesis);
    window.speechSynthesis.speak = function (u) { window.__speech.push(u.text); return realSpeak(u); };
  }
}`;

async function open(page, url, errors, opts) {
  page.on('pageerror', e => errors.push('pageerror: ' + String(e).slice(0, 160)));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text().slice(0, 160)); });
  if (opts && opts.probe) await page.addInitScript(eval(AUDIO_PROBE));
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
  const browser = await chromium.launch({ executablePath: exe, args: ['--no-sandbox', '--autoplay-policy=no-user-gesture-required'] });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 720 } });

  const perrs = [];
  const proj = await ctx.newPage();
  await open(proj, base + 'projector.html', perrs, { probe: true });
  await proj.waitForFunction(() => window.__LT.manifestId() !== null, null, { timeout: 5000 });
  const herrs = [];
  const hud = await ctx.newPage();
  await open(hud, base + 'teacher.html', herrs);
  await hud.waitForTimeout(500);
  await proj.bringToFront();

  /* ================= X3: audio is off, and stays off ================= */
  const audio0 = await proj.evaluate(() => ({
    state: window.__LT.extras().audio,
    pressed: document.getElementById('btnAudio').getAttribute('aria-pressed'),
    label: document.getElementById('btnAudio').textContent,
    started: window.__osc.started
  }));
  check('X3: sound is OFF at load, and the button says so', audio0.state === false && audio0.pressed === 'false' && /off/i.test(audio0.label), JSON.stringify(audio0));

  // Everything that CAN make a sound, fired with audio off: nothing sounds.
  await proj.evaluate(() => document.activeElement && document.activeElement.blur());
  await proj.keyboard.press('Digit7');
  await proj.keyboard.press('Digit8');
  await stripClick(proj, '#btnBell');
  await proj.waitForTimeout(400);
  const silent = await proj.evaluate(() => ({ started: window.__osc.started, spoke: window.__speech.length }));
  check('X3: with sound off, three sound-capable actions start ZERO oscillators and speak nothing', silent.started === 0 && silent.spoke === 0, JSON.stringify(silent));

  // Turn it on: now it really is audible — live oscillators at a modest gain.
  await stripClick(proj, '#btnAudio');
  await proj.waitForTimeout(150);
  await proj.evaluate(() => document.activeElement && document.activeElement.blur());
  await proj.keyboard.press('Digit9');
  await proj.waitForTimeout(400);
  const loud = await proj.evaluate(() => ({
    started: window.__osc.started, stopped: window.__osc.stopped, peak: window.__osc.peakGain,
    state: window.__LT.extras().audio, label: document.getElementById('btnAudio').textContent
  }));
  check('X3: with sound on, a tally press starts a REAL oscillator (not a silent code path)', loud.started >= 1 && loud.state === true && /on/i.test(loud.label), JSON.stringify(loud));
  check('X3: the earcon is quiet (peak gain well under a tenth) and is scheduled to STOP — no ringing alarm', loud.peak > 0 && loud.peak <= 0.1 && loud.stopped >= 1, JSON.stringify({ peak: loud.peak, stopped: loud.stopped }));

  // TTS speaks a cold-called name, but only with sound on.
  await proj.evaluate(() => { window.__speech.length = 0; });
  await hud.bringToFront();
  await hud.fill('#pickRoster', 'Wilhelmina');
  await hud.click('#btnPickLoad');
  await hud.click('#btnPickNext');
  await hud.click('#btnPickProject');
  await hud.waitForTimeout(500);
  const spoke = await proj.evaluate(() => window.__speech.slice());
  check('X3: a projected cold-call name is spoken when sound is on', spoke.includes('Wilhelmina'), JSON.stringify(spoke));
  await hud.click('#btnPickHide');

  /* THE persistence gate: the choice must NOT come back after a reload. */
  await proj.bringToFront();
  const storedAudio = await proj.evaluate(() => JSON.stringify(Object.keys(localStorage).map(k => localStorage.getItem(k))));
  check('X3: turning sound on writes nothing to storage', !/audio|sound/i.test(storedAudio), storedAudio.slice(0, 90));
  await proj.reload({ waitUntil: 'load' });
  try { await proj.locator('.mbm-skip').click({ timeout: 4000 }); } catch (e) {}
  await proj.waitForFunction(() => !document.querySelector('.mbm-splash'), null, { timeout: 8000 });
  await proj.waitForFunction(() => window.__LT.manifestId() !== null, null, { timeout: 5000 });
  const afterReload = await proj.evaluate(() => ({ audio: window.__LT.extras().audio, label: document.getElementById('btnAudio').textContent }));
  check('X3: sound is OFF again after a reload — the toggle deliberately does not persist', afterReload.audio === false && /off/i.test(afterReload.label), JSON.stringify(afterReload));

  /* ================= X1: the tally counts, and only counts ============= */
  await proj.evaluate(() => document.activeElement && document.activeElement.blur());
  for (const k of ['Digit7', 'Digit7', 'Digit8', 'Digit9', 'Digit9', 'Digit9']) await proj.keyboard.press(k);
  await proj.waitForTimeout(400);
  const tally = await proj.evaluate(() => window.__LT.extras());
  check('X1: 7/8/9 count Red / Amber / Green', tally.rag.r === 2 && tally.rag.a === 1 && tally.rag.g === 3, JSON.stringify(tally.rag));
  check('X1: the first vote shows the panel (a counter nobody can see is a counter nobody trusts)', tally.ragShow === true && tally.ragVisible === true, JSON.stringify({ show: tally.ragShow, vis: tally.ragVisible }));
  const readout = await proj.evaluate(() => [...document.querySelectorAll('#ragPanel .rrow')].map(r => ({
    word: r.querySelector('.word').textContent, n: r.querySelector('.n').textContent, glyph: r.querySelector('.glyph').textContent
  })));
  check('X1: each row is readable WITHOUT colour — a word, a shape and a number',
    readout.length === 3 && readout.every(r => r.word && r.n && r.glyph) && readout[0].n === '2' && readout[2].n === '3',
    JSON.stringify(readout));
  const totalText = await proj.evaluate(() => document.querySelector('#ragPanel .total').textContent);
  check('X1: the total is stated in words', /6 responses/.test(totalText), totalText);
  const anon = await proj.evaluate(() => document.getElementById('ragPanel').textContent);
  check('X1: the panel contains no name — counts only, anonymous by construction', !/Wilhelmina/.test(anon), anon.slice(0, 60));

  // Both directions over the bus, and the HUD mirrors without its own counter.
  await hud.bringToFront();
  await hud.click('#btnRagA');
  await hud.waitForTimeout(400);
  const hudSees = await hud.evaluate(() => window.__LT.extras());
  const projHas = await proj.evaluate(() => window.__LT.extras().rag);
  check('X1: a HUD press lands on the projector and reflects back (no HUD-side counter)', hudSees.rag.a === 2 && projHas.a === 2, JSON.stringify({ hud: hudSees.rag, proj: projHas }));
  const hudInd = await hud.evaluate(() => ({ r: document.getElementById('indRagR').textContent, g: document.getElementById('indRagG').textContent }));
  check('X1: the HUD indicators render the projector\'s numbers', hudInd.r === '2' && hudInd.g === '3', JSON.stringify(hudInd));

  /* ================= X4: a real SVG, from the real series ============== */
  const svg = await proj.evaluate(() => window.__LT.extras().svg);
  check('X4: the sparkline is well-formed standalone SVG with the xmlns a paste needs', /^<svg xmlns="http:\/\/www\.w3\.org\/2000\/svg"/.test(svg) && /<\/svg>$/.test(svg), String(svg).slice(0, 70));
  const paths = (svg.match(/<path /g) || []).length;
  check('X4: it draws one line per colour actually recorded', paths === 3, 'paths=' + paths);
  check('X4: it carries its own text labels and an aria-label, so it reads outside this page', /Stuck 2/.test(svg) && /Got it 3/.test(svg) && /aria-label=/.test(svg), svg.slice(0, 120));
  check('X4: no pupil name is anywhere in the exported graph', !/Wilhelmina/.test(svg));
  // It must parse as XML — a paste target will reject anything less.
  const parses = await proj.evaluate(s => {
    const d = new DOMParser().parseFromString(s, 'image/svg+xml');
    return { err: !!d.querySelector('parsererror'), tag: d.documentElement.tagName, paths: d.querySelectorAll('path').length };
  }, svg);
  check('X4: it parses as real SVG (a paste target would reject anything less)', parses.err === false && parses.tag === 'svg' && parses.paths === 3, JSON.stringify(parses));

  // The clipboard-blocked path is the real one on school machines.
  await proj.evaluate(() => {
    window.__dl = null;
    Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText: () => Promise.reject(new Error('blocked')) } });
    const realClick = HTMLAnchorElement.prototype.click;
    HTMLAnchorElement.prototype.click = function () {
      if (this.download) { window.__dl = { name: this.download, href: this.href.slice(0, 5) }; return; }
      return realClick.call(this);
    };
  });
  await stripClick(proj, '#btnSpark');
  await proj.waitForTimeout(400);
  const blocked = await proj.evaluate(() => ({ dl: window.__dl, toast: document.getElementById('toast').textContent, op: getComputedStyle(document.getElementById('toast')).opacity }));
  check('X4: when the clipboard is blocked the graph DOWNLOADS instead', blocked.dl && blocked.dl.name === 'class-confidence.svg' && blocked.dl.href === 'blob:', JSON.stringify(blocked.dl));
  check('X4: and it says what actually happened rather than claiming a copy', /downloaded/i.test(blocked.toast) && blocked.op === '1', blocked.toast.slice(0, 70));

  // Reset clears the counts AND the recorded series behind the graph.
  await stripClick(proj, '#btnRagReset');
  await proj.waitForTimeout(300);
  const reset = await proj.evaluate(() => window.__LT.extras());
  check('X1: reset zeroes the counts and empties the series behind the graph', reset.rag.r === 0 && reset.rag.a === 0 && reset.rag.g === 0 && reset.series === 0 && reset.svg === null, JSON.stringify(reset.rag));

  /* ================= X2: the bell, and its reduced-motion form ========= */
  await proj.evaluate(() => document.activeElement && document.activeElement.blur());
  await stripClick(proj, '#btnBell');
  await proj.waitForTimeout(200);
  const bell = await proj.evaluate(() => window.__LT.extras());
  check('X2: the bell shows the glow and the banner together', bell.bellOn === true && bell.bannerOn === true, JSON.stringify({ glow: bell.bellOn, banner: bell.bannerOn }));
  check('X2: normally it BREATHES (a named animation, not a strobe)', bell.bellAnim === 'bellBreath', bell.bellAnim);
  const said = await proj.evaluate(() => document.getElementById('bellSaid').textContent);
  check('X2: it is announced, so a screen-reader user gets the same cue', /eyes this way/i.test(said), said);
  const keymapHasBell = await proj.evaluate(() => window.__LT.keymap().map(k => k[0]));
  check('X2: the bell is button-only — B stays blackout and nothing else (the spec retired the pulse key)',
    keymapHasBell.includes('KeyB') && !keymapHasBell.includes('KeyL'), JSON.stringify(keymapHasBell.filter(k => /Key[BL]/.test(k))));

  /* THE reduced-motion gate, on a page booted with the OS setting. */
  const rerrs = [];
  const rm = await ctx.newPage();
  await rm.emulateMedia({ reducedMotion: 'reduce' });
  await open(rm, base + 'projector.html', rerrs);
  await rm.waitForFunction(() => window.__LT.manifestId() !== null, null, { timeout: 5000 });
  await stripClick(rm, '#btnBell');
  await rm.waitForTimeout(300);
  const rmBell = await rm.evaluate(() => {
    const b = document.getElementById('bell'), banner = document.getElementById('bellBanner');
    const cs = getComputedStyle(b);
    return {
      anim: cs.animationName, dur: cs.animationDuration, opacity: cs.opacity,
      bannerVisible: getComputedStyle(banner).visibility === 'visible',
      bannerText: banner.textContent.trim(),
      reduceClass: document.body.classList.contains('reduce')
    };
  });
  check('X2 GATE: under prefers-reduced-motion the page is in reduced mode', rmBell.reduceClass === true);
  check('X2 GATE: the bell does NOT animate — no breath, no flash', rmBell.anim === 'none' || parseFloat(rmBell.dur) <= 0.001, JSON.stringify({ anim: rmBell.anim, dur: rmBell.dur }));
  check('X2 GATE: the cue survives as a STATIC banner plus a held tint — the signal is not lost with the motion',
    rmBell.bannerVisible === true && /eyes this way/i.test(rmBell.bannerText) && parseFloat(rmBell.opacity) > 0,
    JSON.stringify({ banner: rmBell.bannerText, opacity: rmBell.opacity }));
  const rmAudio = await rm.evaluate(() => window.__LT.extras().audio);
  check('X3: a reduced-motion boot is also silent by default', rmAudio === false);
  check('no console or page errors under reduced motion', rerrs.length === 0, rerrs.join(' | '));
  await rm.close();

  check('no console or page errors on the projector', perrs.length === 0, perrs.join(' | '));
  check('no console or page errors on the HUD', herrs.length === 0, herrs.join(' | '));

  await browser.close();
  srv.close();
  console.log(failures ? 'LT-EXTRAS: ' + failures + ' FAILURE(S)' : 'LT-EXTRAS: all checks passed');
  process.exit(failures ? 1 : 0);
})().catch(e => { console.error('DIED: ' + e.stack); process.exit(1); });
