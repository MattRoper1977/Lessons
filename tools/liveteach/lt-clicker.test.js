/* lt-clicker — the LT4 clicker-bridge suite (spec Phase 3, C1–C4).

   Simulated keydown proofs for EVERY clicker key in BOTH views; proof that B
   fires exactly one action per press (the C1 double-fire class); the honest
   fullscreen story (C2): F5 is prevented and answered with advice in both
   views, the HUD cannot make the projector fullscreen, and the projector's
   own button — a real user gesture — genuinely can; the blackout curtain
   covers the teaching surfaces but never the way back out.

     NODE_PATH=$(npm root -g) node tools/liveteach/lt-clicker.test.js */
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

  const stage = () => proj.evaluate(() => window.__LT.stage().index);
  const black = () => proj.evaluate(() => window.__LT.state().blackout);

  /* ---------- clicker keys on the PROJECTOR view ---------- */
  await proj.bringToFront();
  await proj.keyboard.press('PageDown');
  check('projector key: PageDown advances the stage', await stage() === 1);
  await proj.keyboard.press('PageUp');
  check('projector key: PageUp goes back', await stage() === 0);
  await proj.keyboard.press('ArrowRight');
  check('projector key: ArrowRight advances', await stage() === 1);
  await proj.keyboard.press('ArrowLeft');
  check('projector key: ArrowLeft goes back', await stage() === 0);
  await proj.keyboard.press('KeyB');
  check('projector key: B blacks out', await black() === true);
  await proj.keyboard.press('KeyB');
  check('projector key: B again restores', await black() === false);
  await proj.keyboard.press('Period');
  check('projector key: full stop blacks out (clicker variant)', await black() === true);
  await proj.keyboard.press('Escape');
  check('projector key: Esc clears blackout FIRST', await black() === false);

  /* B fires exactly one action per press: two presses must land on the same
     state, never race an even number of toggles into an odd one. The counter
     counts blackout TRANSITIONS, not raw broadcasts — the HUD's 3 s
     heartbeat re-broadcasts the same state and made a raw count flaky. */
  const bCount = await proj.evaluate(async () => {
    let flips = 0;
    let lastSeen = window.__LT.state().blackout;
    const before = lastSeen;
    const bus = new BroadcastChannel('mbm_liveteach_v1');
    bus.addEventListener('message', ev => {
      if (ev.data && ev.data.type === 'PROJECTOR_STATE' && ev.data.payload.blackout !== lastSeen) {
        lastSeen = ev.data.payload.blackout;
        flips++;
      }
    });
    document.dispatchEvent(new KeyboardEvent('keydown', { code: 'KeyB', bubbles: true }));
    await new Promise(r => setTimeout(r, 250));
    const mid = window.__LT.state().blackout;
    document.dispatchEvent(new KeyboardEvent('keydown', { code: 'KeyB', bubbles: true }));
    await new Promise(r => setTimeout(r, 250));
    bus.close();
    return { before, mid, after: window.__LT.state().blackout, transitions: flips };
  });
  check('C1: B fires exactly one action per press (state + transition count)', bCount.before === false && bCount.mid === true && bCount.after === false && bCount.transitions === 2, JSON.stringify(bCount));

  /* SEMH guard: key auto-repeat must never strobe the curtain. */
  const strobe = await proj.evaluate(() => {
    const before = window.__LT.state().blackout;
    for (let i = 0; i < 20; i++) document.dispatchEvent(new KeyboardEvent('keydown', { code: 'KeyB', bubbles: true, repeat: true }));
    return { before, after: window.__LT.state().blackout };
  });
  check('a11y: held-key auto-repeat cannot strobe the blackout', strobe.before === strobe.after, JSON.stringify(strobe));

  /* Blackout is announced, not just shown. */
  await proj.keyboard.press('KeyB');
  const said = await proj.evaluate(() => document.getElementById('blackoutSaid').textContent);
  await proj.keyboard.press('KeyB');
  const saidOff = await proj.evaluate(() => document.getElementById('blackoutSaid').textContent);
  check('a11y: blackout announces both states politely', said.includes('blacked out') && saidOff === 'Screen restored', JSON.stringify({ said, saidOff }));

  /* F5 on the projector: default prevented, honest toast, no fullscreen. */
  const f5p = await proj.evaluate(() => {
    const ev = new KeyboardEvent('keydown', { code: 'F5', bubbles: true, cancelable: true });
    document.dispatchEvent(ev);
    return { prevented: ev.defaultPrevented, fs: !!document.fullscreenElement };
  });
  await proj.waitForTimeout(100);
  const f5toast = await proj.evaluate(() => ({ op: getComputedStyle(document.getElementById('toast')).opacity, text: document.getElementById('toast').textContent }));
  check('C2: F5 on the projector is prevented and answered with the button advice', f5p.prevented === true && f5p.fs === false && f5toast.op === '1' && f5toast.text.includes('Fullscreen'), JSON.stringify(f5toast.text.slice(0, 40)));

  /* F5 must be dead even while typing a hint — an unprevented F5 there
     reloads the projector mid-lesson (the review's live repro). */
  const f5input = await proj.evaluate(() => {
    document.getElementById('hintInput').focus();
    const ev = new KeyboardEvent('keydown', { code: 'F5', bubbles: true, cancelable: true });
    document.getElementById('hintInput').dispatchEvent(ev);
    const prevented = ev.defaultPrevented;
    document.getElementById('hintInput').blur();
    return prevented;
  });
  check('C2: F5 is prevented even with focus in a text input', f5input === true);

  /* The toast live region stays in the accessibility tree while unseen —
     hidden by opacity, never visibility (the announced-from-hidden trap). */
  const toastTree = await proj.evaluate(() => getComputedStyle(document.getElementById('toast')).visibility);
  check('a11y: the toast region is never visibility-hidden', toastTree === 'visible');

  /* The projector's own fullscreen button IS a real gesture and works. */
  await proj.evaluate(() => new Promise(r => { document.getElementById('strip').classList.remove('hidden'); r(); }));
  await proj.mouse.move(640, 700);
  await proj.click('#fsBtn');
  await proj.waitForTimeout(300);
  const fsNow = await proj.evaluate(() => !!document.fullscreenElement);
  check('C2: the projector-side fullscreen button genuinely works (real click)', fsNow === true);
  await proj.keyboard.press('F11').catch(() => {});
  await proj.evaluate(() => document.exitFullscreen().catch(() => {}));

  /* Blackout covers the teaching content but never the way out: the curtain
     sits above the banner/overlays and below the strip. */
  await proj.keyboard.press('KeyB');
  const cover = await proj.evaluate(() => {
    const z = id => Number(getComputedStyle(document.getElementById(id)).zIndex);
    return { curtain: z('blackout'), strip: z('strip'), banner: z('stageBanner'), vis: getComputedStyle(document.getElementById('blackout')).visibility };
  });
  check('blackout: curtain above the lesson, below the strip', cover.vis === 'visible' && cover.curtain > cover.banner && cover.curtain < cover.strip, JSON.stringify(cover));
  await proj.keyboard.press('KeyB');

  /* ---------- clicker keys on the HUD view (C4: focus-loss survival) ----- */
  await hud.bringToFront();
  await hud.keyboard.press('PageDown');
  await hud.waitForTimeout(300);
  check('HUD key: PageDown advances the projector stage', await stage() === 1);
  await hud.keyboard.press('PageUp');
  await hud.waitForTimeout(300);
  check('HUD key: PageUp goes back', await stage() === 0);
  await hud.keyboard.press('ArrowRight');
  await hud.waitForTimeout(300);
  check('HUD key: ArrowRight advances', await stage() === 1);
  await hud.keyboard.press('ArrowLeft');
  await hud.waitForTimeout(300);
  check('HUD key: ArrowLeft goes back', await stage() === 0);
  await hud.keyboard.press('KeyB');
  await hud.waitForTimeout(300);
  check('HUD key: B blacks the projector out over the bus', await black() === true);
  const hudInd = await hud.evaluate(() => document.getElementById('indBlackout').textContent);
  check('HUD indicator follows blackout', hudInd === 'ON');
  await hud.keyboard.press('Period');
  await hud.waitForTimeout(300);
  check('HUD key: full stop restores', await black() === false);

  /* The HUD blackout BUTTON sends an idempotent SET from seen state: two fast
     presses cannot cross a toggle in flight and land inverted. */
  await hud.evaluate(() => { document.getElementById('btnBlackout').click(); document.getElementById('btnBlackout').click(); });
  await hud.waitForTimeout(400);
  check('C3-live: BLACKOUT_SET is real, exercised, and idempotent (two fast presses = ON)', await black() === true);
  await hud.click('#btnBlackout');
  await hud.waitForTimeout(300);
  check('C3-live: the SET path also restores', await black() === false);

  /* F5 on the HUD: prevented, and the advice is HONEST — the projector does
     NOT go fullscreen, because a bus message is not a user gesture. */
  const f5h = await hud.evaluate(() => {
    const ev = new KeyboardEvent('keydown', { code: 'F5', bubbles: true, cancelable: true });
    document.dispatchEvent(ev);
    return ev.defaultPrevented;
  });
  await hud.waitForTimeout(200);
  const f5hToast = await hud.evaluate(() => ({ op: getComputedStyle(document.getElementById('toast')).opacity, text: document.getElementById('toast').textContent }));
  const projFs = await proj.evaluate(() => !!document.fullscreenElement);
  check('C2: HUD F5 prevented + advice shown + projector NOT fullscreened', f5h === true && f5hToast.op === '1' && f5hToast.text.includes('F11') && projFs === false, JSON.stringify({ projFs }));
  const fsBtnHud = await hud.evaluate(() => { document.getElementById('btnFsHelp').click(); return true; });
  await hud.waitForTimeout(100);
  const projFs2 = await proj.evaluate(() => !!document.fullscreenElement);
  check('C2: the HUD fullscreen button also only advises', fsBtnHud && projFs2 === false);

  /* Registry integrity: every clicker key is registered in both views, once. */
  const maps = {
    proj: await proj.evaluate(() => window.__LT.keymap().map(k => k[0])),
    hud: await hud.evaluate(() => window.__LT.keymap().map(k => k[0])),
  };
  const CLICKER = ['PageUp', 'PageDown', 'ArrowLeft', 'ArrowRight', 'KeyB', 'Period', 'F5'];
  const both = CLICKER.every(k => maps.proj.includes(k) && maps.hud.includes(k));
  const once = CLICKER.every(k => maps.proj.filter(x => x === k).length === 1 && maps.hud.filter(x => x === k).length === 1);
  check('C4: every clicker key registered in BOTH views, exactly once', both && once, JSON.stringify(maps.hud));

  /* The splash gate: clicker presses during the boot splash do nothing. */
  const serrs = [];
  const sp = await ctx.newPage();
  sp.on('pageerror', e => serrs.push(String(e).slice(0, 120)));
  await sp.goto(base + 'projector.html', { waitUntil: 'load' });
  await sp.locator('.mbm-splash').waitFor({ state: 'visible', timeout: 4000 });
  await sp.keyboard.press('PageDown');
  await sp.keyboard.press('KeyB');
  try { await sp.locator('.mbm-skip').click({ timeout: 4000 }); } catch (e) {}
  await sp.waitForFunction(() => !document.querySelector('.mbm-splash'), null, { timeout: 8000 });
  await sp.waitForFunction(() => window.__LT.manifestId() !== null, null, { timeout: 5000 });
  const afterSplash = await sp.evaluate(() => ({ stage: window.__LT.stage().index, blackout: window.__LT.state().blackout }));
  check('splash gate: remote presses during the splash change nothing', afterSplash.stage === 0 && afterSplash.blackout === false && serrs.length === 0, JSON.stringify(afterSplash));

  /* Honest failure when the platform refuses fullscreen. */
  await sp.evaluate(() => {
    Object.defineProperty(document.documentElement, 'requestFullscreen', { value: function () { return Promise.reject(new Error('policy')); } });
  });
  await sp.mouse.move(640, 700);
  await sp.click('#fsBtn');
  await sp.waitForTimeout(200);
  const refused = await sp.evaluate(() => ({ op: getComputedStyle(document.getElementById('toast')).opacity, text: document.getElementById('toast').textContent, fs: !!document.fullscreenElement }));
  check('C2: a refused fullscreen gets an honest toast, not silence', refused.op === '1' && refused.text.includes('refused') && refused.fs === false, JSON.stringify(refused.text.slice(0, 40)));
  await sp.close();

  check('console: projector clean', perrs.length === 0, perrs.join(' | '));
  check('console: HUD clean', herrs.length === 0, herrs.join(' | '));

  await browser.close();
  srv.close();
  console.log(failures ? 'SUITE FAILED (' + failures + ')' : 'SUITE PASSED');
  process.exit(failures ? 1 : 0);
})().catch(e => { console.log('DIED: ' + (e && e.stack || e)); process.exit(2); });
