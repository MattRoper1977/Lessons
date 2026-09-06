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
  window.__osc = { started: 0, peakGain: 0, stopped: 0, durations: [], reachedOutput: 0 };
  const AC = window.AudioContext || window.webkitAudioContext;
  if (!AC) return;
  const realOsc = AC.prototype.createOscillator;
  const realGain = AC.prototype.createGain;
  /* Counting start() proves a node was told to run, not that anyone can hear
     it. Wrapping connect() as well means a tone routed nowhere — the whole
     chain built and never joined to the speakers — is distinguishable from a
     working earcon. */
  const realConnect = AudioNode.prototype.connect;
  AudioNode.prototype.connect = function (dest) {
    try {
      if (dest === this.context.destination) window.__osc.reachedOutput++;
    } catch (e) {}
    return realConnect.apply(this, arguments);
  };
  AC.prototype.createOscillator = function () {
    const o = realOsc.call(this);
    const start = o.start.bind(o), stop = o.stop.bind(o);
    let t0 = null;
    o.start = function (t) { window.__osc.started++; t0 = (t == null ? o.context.currentTime : t); return start(t); };
    o.stop = function (t) {
      window.__osc.stopped++;
      const t1 = (t == null ? o.context.currentTime : t);
      if (t0 !== null) window.__osc.durations.push(t1 - t0);
      return stop(t);
    };
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
  /* A speech-capable action too: the earlier version fired three things that
     only ever make earcons, so "speak nothing" was true whatever say() did.
     Projecting a name is the path that speaks. */
  /* Sent from the HUD: a BroadcastChannel never delivers a page its own
     messages, so a PICK_SHOW posted by the projector would reach nobody. */
  await hud.evaluate(() => { window.LT.send('PICK_SHOW', { name: 'Quietly' }); });
  await proj.waitForTimeout(600);
  const silent = await proj.evaluate(() => ({
    started: window.__osc.started, spoke: window.__speech.length,
    onWall: window.__LT.state().pick
  }));
  check('X3: with sound off, four sound-capable actions start ZERO oscillators and speak nothing', silent.started === 0 && silent.spoke === 0, JSON.stringify(silent));
  check('setup: one of those actions really was the speaking path', silent.onWall === 'Quietly', silent.onWall);
  await hud.evaluate(() => { window.LT.send('PICK_CLEAR', {}); });
  await proj.waitForTimeout(300);

  // Turn it on: now it really is audible — live oscillators at a modest gain.
  await stripClick(proj, '#btnAudio');
  await proj.waitForTimeout(150);
  await proj.evaluate(() => document.activeElement && document.activeElement.blur());
  await proj.keyboard.press('Digit9');
  await proj.waitForTimeout(400);
  const loud = await proj.evaluate(() => ({
    started: window.__osc.started, stopped: window.__osc.stopped, peak: window.__osc.peakGain,
    durations: window.__osc.durations.slice(), reachedOutput: window.__osc.reachedOutput,
    state: window.__LT.extras().audio, label: document.getElementById('btnAudio').textContent
  }));
  check('X3: with sound on, a tally press starts a REAL oscillator (not a silent code path)', loud.started >= 1 && loud.state === true && /on/i.test(loud.label), JSON.stringify(loud));
  check('X3: and the chain actually REACHES the speakers (a tone routed nowhere would count as started too)', loud.reachedOutput >= 1, 'connections to destination: ' + loud.reachedOutput);
  check('X3: the earcon is quiet (peak gain well under a tenth) and is scheduled to STOP — no ringing alarm', loud.peak > 0 && loud.peak <= 0.1 && loud.stopped >= 1, JSON.stringify({ peak: loud.peak, stopped: loud.stopped }));
  /* The spec's number, asserted rather than assumed: earcons <= 300 ms. */
  check('X3: every earcon is 300 ms or shorter, as the spec requires',
    loud.durations.length >= 1 && loud.durations.every(d => d > 0 && d <= 0.3),
    JSON.stringify(loud.durations.map(d => Math.round(d * 1000) + 'ms')));

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
  const storedAudio = await proj.evaluate(() => JSON.stringify({
    keys: Object.keys(localStorage),
    values: Object.keys(localStorage).map(k => localStorage.getItem(k)),
    session: Object.keys(sessionStorage)
  }));
  /* KEYS as well as values: a page storing lt.audio = "1" leaves a value of
     "1", which matches nothing — the old check would have missed it. */
  check('X3: turning sound on writes nothing to storage (keys or values, local or session)',
    !/audio|sound/i.test(storedAudio) && !/"session":\[.+\]/.test(storedAudio), storedAudio.slice(0, 120));
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
  check('X4: it carries its own text labels and an aria-label, so it reads outside this page', /Stuck \(dotted\) 2/.test(svg) && /Got it \(solid\) 3/.test(svg) && /aria-label=/.test(svg), svg.slice(0, 140));
  /* Colour is never the only cue — including in a file that will be printed
     in black and white. Each series must differ by dash and carry its own
     end label. */
  const dashes = (svg.match(/stroke-dasharray="[^"]+"/g) || []);
  const endLabels = ['Stuck', 'Nearly', 'Got it'].filter(w => new RegExp('>' + w + '</text>').test(svg));
  check('X4: the three series differ by DASH as well as hue, and each is labelled on the line',
    dashes.length === 2 && endLabels.length === 3, JSON.stringify({ dashes, endLabels }));
  /* A single vote used to export a blank graph: one moveto, no lineto, and
     SVG paints nothing at all. Reset FIRST, so this is genuinely one vote. */
  await stripClick(proj, '#btnRagReset');
  await proj.evaluate(() => document.activeElement && document.activeElement.blur());
  await proj.keyboard.press('Digit9');
  await proj.waitForTimeout(200);
  const solo = await proj.evaluate(() => ({ series: window.__LT.extras().series, svg: window.__LT.extras().svg }));
  const soloDrawn = (solo.svg.match(/<path d="M[^"]*L[^"]*"/g) || []).length;
  check('setup: exactly one vote is recorded', solo.series === 1, String(solo.series));
  check('X4: a graph with a single recorded vote still draws something (it used to be blank)', soloDrawn >= 1, 'drawable paths: ' + soloDrawn);
  // restore a fuller series for the checks that follow
  for (const k of ['Digit7', 'Digit7', 'Digit8', 'Digit9', 'Digit9']) await proj.keyboard.press(k);
  await proj.waitForTimeout(200);
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

  /* ====== an explicit hide must survive the next vote ================== */
  await stripClick(proj, '#btnRag');            // hide the tally deliberately
  await proj.waitForTimeout(150);
  const hidden = await proj.evaluate(() => window.__LT.extras());
  check('setup: the teacher has hidden the tally', hidden.ragShow === false && hidden.ragVisible === false, JSON.stringify({ show: hidden.ragShow }));
  await proj.evaluate(() => document.activeElement && document.activeElement.blur());
  await proj.keyboard.press('Digit7');
  await proj.waitForTimeout(200);
  const afterVote = await proj.evaluate(() => window.__LT.extras());
  check('X1: a vote does NOT force the hidden tally back up (an uninfluenced vote stays uninfluenced)',
    afterVote.ragShow === false && afterVote.ragVisible === false && afterVote.rag.r === hidden.rag.r + 1,
    JSON.stringify({ show: afterVote.ragShow, r: afterVote.rag.r }));
  await stripClick(proj, '#btnRag');            // back on for what follows
  await proj.waitForTimeout(150);

  /* ====== "0 clears every overlay" means the tally and the bell too ==== */
  await stripClick(proj, '#btnBell');
  await proj.waitForTimeout(200);
  const beforeSweep = await proj.evaluate(() => window.__LT.extras());
  check('setup: the tally and the bell are both up', beforeSweep.ragVisible === true && beforeSweep.bannerOn === true, JSON.stringify({ tally: beforeSweep.ragVisible, bell: beforeSweep.bannerOn }));
  await proj.evaluate(() => document.activeElement && document.activeElement.blur());
  await proj.keyboard.press('Digit0');
  await proj.waitForTimeout(250);
  const afterSweep = await proj.evaluate(() => window.__LT.extras());
  check('"0 — clear every overlay" retires the tally panel and the bell as well',
    afterSweep.ragVisible === false && afterSweep.bannerOn === false && afterSweep.bellOn === false,
    JSON.stringify({ tally: afterSweep.ragVisible, banner: afterSweep.bannerOn }));
  check('...and the COUNTS survive it — clearing the screen is not throwing the lesson away',
    afterSweep.rag.r === beforeSweep.rag.r && afterSweep.rag.g === beforeSweep.rag.g,
    JSON.stringify({ before: beforeSweep.rag, after: afterSweep.rag }));

  /* ====== the HUD announces the extras, like everything else here ====== */
  await hud.bringToFront();
  await hud.evaluate(() => { document.getElementById('extrasSaid').textContent = ''; });
  await hud.click('#btnRagG');
  await hud.waitForTimeout(1300);
  const hudSaid = await hud.evaluate(() => document.getElementById('extrasSaid').textContent);
  check('a11y: the HUD announces the tally after a vote (it used to change silent spans)', /got it/i.test(hudSaid), hudSaid);
  await hud.click('#btnBell');
  await hud.waitForTimeout(200);
  const bellSaid = await hud.evaluate(() => document.getElementById('extrasSaid').textContent);
  check('a11y: and announces the silent bell', /bell/i.test(bellSaid), bellSaid);
  await proj.bringToFront();
  await proj.evaluate(() => document.activeElement && document.activeElement.blur());
  await proj.keyboard.press('Digit0');

  /* ====== taking a name down stops the speech saying it ================= */
  await stripClick(proj, '#btnAudio');           // sound back on
  await proj.waitForTimeout(150);
  const cancelled = await proj.evaluate(async () => {
    let cancels = 0;
    const real = window.speechSynthesis.cancel.bind(window.speechSynthesis);
    window.speechSynthesis.cancel = function () { cancels++; return real(); };
    window.__LT.state();
    return cancels;
  });
  await hud.evaluate(() => window.LT.send('PICK_SHOW', { name: 'Reginald' }));
  await proj.waitForTimeout(400);
  await hud.evaluate(() => window.LT.send('PICK_CLEAR', {}));
  await proj.waitForTimeout(400);
  const afterClearName = await proj.evaluate(() => ({
    spoke: window.__speech.slice(-1)[0],
    pick: window.__LT.state().pick,
    speaking: window.speechSynthesis.speaking
  }));
  check('X3: clearing the name off the wall also stops it being spoken', afterClearName.pick === '' && afterClearName.speaking === false, JSON.stringify(afterClearName));
  await stripClick(proj, '#btnAudio');           // back off

  /* ================= X2: the bell, and its reduced-motion form ========= */
  await proj.evaluate(() => document.activeElement && document.activeElement.blur());
  await stripClick(proj, '#btnBell');
  await proj.waitForTimeout(200);
  const bell = await proj.evaluate(() => {
    const b = document.getElementById('bell');
    const cs = getComputedStyle(b);
    return Object.assign(window.__LT.extras(), {
      glowVisibility: cs.visibility, glowOpacity: cs.opacity, glowBg: cs.backgroundImage.slice(0, 30)
    });
  });
  check('X2: the bell shows the glow and the banner together', bell.bellOn === true && bell.bannerOn === true, JSON.stringify({ glow: bell.bellOn, banner: bell.bannerOn }));
  /* A class name is a proxy. The glow has to be VISIBLE and actually paint
     something — it ships at visibility:hidden, so every check that read the
     class alone would have passed with nothing on the screen. */
  check('X2: the glow is genuinely visible and painting (not just class-marked)',
    bell.glowVisibility === 'visible' && bell.glowBg.includes('gradient'),
    JSON.stringify({ vis: bell.glowVisibility, bg: bell.glowBg }));
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
