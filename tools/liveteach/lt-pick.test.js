/* lt-pick — the LT7 cold-call suite (spec Phase 6, P1–P5), in the browser.
   The engine's statistics are proven at scale by picker_gate.mjs; this suite
   proves the parts only a real page can show:

   D2  the roster is SESSION-ONLY — loading a class list writes no storage
       key, puts no name in the address, and a reload comes back empty.
   P3  rows are built with createElement/textContent: a name containing
       markup renders as literal text, and no element in the card carries it
       as HTML.
   P4  attendance is a real control — marking someone away removes them from
       the draw and states it in text, not by tint alone.
   P5  history is not broadcast, and NO name crosses the bus until the
       teacher presses Show on projector (the Q2 opt-in). Every message is
       captured and searched.
   Plus: N/M keys in both views, the projector's own picker for single-window
   teaching, Escape order, blackout stand-down, honest small-room copy.

     NODE_PATH=$(npm root -g) node tools/liveteach/lt-pick.test.js */
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

/* A tap on the bus that records EVERY message this context sees, so the
   no-names promise is checked against real traffic rather than against the
   handful of sends the suite happens to know about. */
const BUS_TAP = `() => {
  window.__busLog = [];
  const ch = new BroadcastChannel('mbm_liveteach_v1');
  ch.addEventListener('message', e => { try { window.__busLog.push(JSON.stringify(e.data)); } catch (x) {} });
  window.__busChan = ch;
}`;

/* Distinctive names: a substring search for these must be conclusive. */
const ROSTER = ['Zarnok', 'Quibbly', 'Vexlin', 'Marrowe', 'Thistlebee'];
/* Kept under the engine's 32-character clamp on purpose: a truncated probe
   would prove nothing about how the surviving characters are rendered. */
const MARKUP_NAME = '<img src=x>Ophira';

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

  // A third page that only listens: it hears everything either view sends.
  const tap = await ctx.newPage();
  await tap.goto(base + 'index.html', { waitUntil: 'load' });
  await tap.evaluate(eval(BUS_TAP));

  /* ================= D2: loading a list writes nothing ================= */
  await hud.bringToFront();
  const storeBefore = await hud.evaluate(() => JSON.stringify(Object.keys(localStorage).sort()));
  await hud.fill('#pickRoster', ROSTER.join('\n'));
  await hud.click('#btnPickLoad');
  await hud.waitForTimeout(200);
  const afterLoad = await hud.evaluate(() => ({
    keys: Object.keys(localStorage).sort(),
    blob: Object.keys(localStorage).map(k => localStorage.getItem(k)).join(' '),
    textarea: document.getElementById('pickRoster').value,
    url: location.href,
    loaded: window.__LT.pick() && window.__LT.pick().names.length,
    liveShown: !document.getElementById('pickLive').hidden
  }));
  check('D2: loading a class list adds no storage key', JSON.stringify(afterLoad.keys) === storeBefore, JSON.stringify(afterLoad.keys));
  check('D2: no name appears anywhere in localStorage', !ROSTER.some(n => afterLoad.blob.includes(n)), afterLoad.blob.slice(0, 80));
  check('D2: no name appears in the address', !ROSTER.some(n => afterLoad.url.includes(n)), afterLoad.url);
  check('D2: the textarea is emptied once loaded (nothing lingers in a form field)', afterLoad.textarea === '');
  check('the picker goes live with the whole list', afterLoad.loaded === ROSTER.length && afterLoad.liveShown, JSON.stringify(afterLoad.loaded));

  /* ================= P5 / Q2: drawing broadcasts NO name ================= */
  await hud.evaluate(() => { window.__LTbusSeen = null; });
  for (let i = 0; i < 12; i++) { await hud.click('#btnPickNext'); }
  await hud.click('#btnPickPass');
  /* Past one full heartbeat interval, so the tap has definitely heard live
     traffic — an empty log would make the no-names search below vacuous. */
  await hud.waitForTimeout(3600);
  const drawn = await hud.evaluate(() => window.__LT.pick());
  check('the HUD really drew (a name is showing and history is filling)', ROSTER.includes(drawn.shown) && drawn.history.length >= 12, JSON.stringify({ shown: drawn.shown, hist: drawn.history.length }));
  const tapLog = await tap.evaluate(() => window.__busLog.join(' || '));
  const leaked = ROSTER.filter(n => tapLog.includes(n));
  check('P5/Q2: after 13 draws NOT ONE name has crossed the bus', leaked.length === 0, 'leaked: ' + leaked.join(','));
  check('P5: the traffic is real (the tap heard live messages), so the search above is conclusive', /HUD_HELLO|PROJECTOR_STATE/.test(tapLog), 'log length ' + tapLog.length);
  const projSees = await proj.evaluate(() => ({ pick: window.__LT.state().pick, visible: window.__LT.pick().visible }));
  check('Q2: the projector shows nothing until asked', projSees.pick === '' && projSees.visible === false, JSON.stringify(projSees));

  /* ================= the Q2 opt-in: one name, on purpose ================= */
  await hud.click('#btnPickProject');
  await hud.waitForTimeout(400);
  const shown = await hud.evaluate(() => window.__LT.pick().shown);
  const onWall = await proj.evaluate(() => ({
    text: window.__LT.pick().shown, visible: window.__LT.pick().visible, state: window.__LT.state().pick
  }));
  check('Q2: Show on projector puts the picked name — and only that name — on the class screen', onWall.text === shown && onWall.visible === true && onWall.state === shown, JSON.stringify(onWall));
  const tapLog2 = await tap.evaluate(() => window.__busLog.filter(s => s.includes('PICK_SHOW')).join(' || '));
  const payload = JSON.parse(tapLog2.split(' || ')[0] || '{}');
  check('Q2: the sanctioned message carries the name and nothing else — no list, no history, no odds',
    payload.type === 'PICK_SHOW' && JSON.stringify(Object.keys(payload.payload)) === '["name"]' && payload.payload.name === shown,
    JSON.stringify(payload));
  await hud.click('#btnPickHide');
  await hud.waitForTimeout(400);
  const cleared = await proj.evaluate(() => ({ text: window.__LT.pick().shown, visible: window.__LT.pick().visible }));
  check('Q2: Clear projector takes the name back off the class screen', cleared.text === '' && cleared.visible === false, JSON.stringify(cleared));

  /* ================= P4: attendance is a real control ================= */
  const away = await hud.evaluate(() => {
    const rows = [...document.querySelectorAll('#pickRows .pickrow')];
    const target = rows[2];
    const name = target.querySelector('.nm').textContent;
    target.querySelector('button.att').click();
    return name;
  });
  await hud.waitForTimeout(200);
  const awayRow = await hud.evaluate(nm => {
    const row = [...document.querySelectorAll('#pickRows .pickrow')].find(r => r.querySelector('.nm').textContent === nm);
    return { status: row.querySelector('.status').textContent, odds: row.querySelector('.odds').textContent, cls: row.className };
  }, away);
  check('P4: an away pupil says so IN TEXT and is shown at 0%, not merely greyed', awayRow.status === 'away' && awayRow.odds === '0%' && /away/.test(awayRow.cls), JSON.stringify(awayRow));
  for (let i = 0; i < 40; i++) await hud.click('#btnPickNext');
  await hud.waitForTimeout(200);
  const hist = await hud.evaluate(() => window.__LT.pick().history.map(h => h.name));
  check('P4: 40 further draws never land on the away pupil', !hist.includes(away), away);
  const oddsSum = await hud.evaluate(() => window.__LT.pick().rows.reduce((a, r) => a + r.p, 0));
  check('P4: the displayed odds still sum to 1 across the pupils who are here', Math.abs(oddsSum - 1) < 1e-9, String(oddsSum));

  /* ================= P2 in the page: cooldown is visible ================= */
  const cooled = await hud.evaluate(() => {
    const rows = window.__LT.pick().rows;
    const shown = window.__LT.pick().shown;
    const me = rows.find(r => r.name === shown);
    return { cooldownCount: rows.filter(r => r.cooldown).length, mine: me && me.cooldown, myOdds: me && me.p };
  });
  check('P2: the pupil just asked is shown on cooldown at 0% — the guarantee is visible, not just internal', cooled.cooldownCount === 1 && cooled.mine === true && cooled.myOdds === 0, JSON.stringify(cooled));
  const statusText = await hud.evaluate(() => [...document.querySelectorAll('#pickRows .status')].map(s => s.textContent).join(','));
  check('P2: "just asked" is stated in text', /just asked/.test(statusText), statusText.slice(0, 60));

  /* ================= P3: a name is text, never markup ================= */
  await hud.click('#btnPickClear');
  await hud.waitForTimeout(150);
  await hud.fill('#pickRoster', MARKUP_NAME + '\nBenedikt');
  await hud.click('#btnPickLoad');
  await hud.waitForTimeout(200);
  const safe = await hud.evaluate(nm => {
    const row = [...document.querySelectorAll('#pickRows .pickrow')].find(r => r.querySelector('.nm').textContent.includes('Ophira'));
    return {
      rendersLiterally: row.querySelector('.nm').textContent === nm,
      noImg: document.querySelectorAll('#pickRows img').length,
      cardHasNoMarkup: !/<img/i.test(document.getElementById('pickRows').innerHTML.replace(/&lt;img/gi, ''))
    };
  }, MARKUP_NAME);
  check('P3: a name containing markup renders as literal text', safe.rendersLiterally === true, JSON.stringify(safe));
  check('P3: no element was created from it — textContent all the way down', safe.noImg === 0 && safe.cardHasNoMarkup === true, JSON.stringify(safe));
  await hud.click('#btnPickClear');
  await hud.waitForTimeout(150);

  /* ================= D2: a reload forgets everything ================= */
  await hud.fill('#pickRoster', ROSTER.join(', '));   // commas, as a register paste
  await hud.click('#btnPickLoad');
  await hud.waitForTimeout(150);
  const beforeReload = await hud.evaluate(() => window.__LT.pick().names.length);
  await hud.reload({ waitUntil: 'load' });
  try { await hud.locator('.mbm-skip').click({ timeout: 4000 }); } catch (e) {}
  await hud.waitForFunction(() => !document.querySelector('.mbm-splash'), null, { timeout: 8000 });
  await hud.waitForTimeout(300);
  const afterReload = await hud.evaluate(() => ({
    pick: window.__LT.pick(),
    emptyShown: !document.getElementById('pickEmpty').hidden,
    store: Object.keys(localStorage).map(k => localStorage.getItem(k)).join(' ')
  }));
  check('D2: the class list dies with the page — a reload comes back empty', beforeReload === 5 && afterReload.pick === null && afterReload.emptyShown, JSON.stringify({ beforeReload, after: afterReload.pick }));
  check('D2: and nothing was left behind in storage to restore it from', !ROSTER.some(n => afterReload.store.includes(n)));

  /* ================= N / M keys, both views ================= */
  await hud.fill('#pickRoster', ROSTER.join('\n'));
  await hud.click('#btnPickLoad');
  await hud.evaluate(() => document.activeElement && document.activeElement.blur());
  await hud.keyboard.press('KeyN');
  await hud.waitForTimeout(150);
  const byKeyN = await hud.evaluate(() => window.__LT.pick().shown);
  check('N picks from the keyboard on the HUD', ROSTER.includes(byKeyN), byKeyN);
  await hud.keyboard.press('KeyM');
  await hud.waitForTimeout(150);
  const byKeyM = await hud.evaluate(() => ({ shown: window.__LT.pick().shown, hist: window.__LT.pick().history.slice(0, 2) }));
  check('M bounces to someone else, and the pass is recorded', byKeyM.shown !== byKeyN && byKeyM.hist[1] && byKeyM.hist[1].passed === true, JSON.stringify(byKeyM));
  const keymaps = {
    proj: await proj.evaluate(() => window.__LT.keymap().map(k => k[0])),
    hud: await hud.evaluate(() => window.__LT.keymap().map(k => k[0]))
  };
  check('N and M are registered in BOTH views, exactly once each',
    ['KeyN', 'KeyM'].every(k => keymaps.proj.filter(x => x === k).length === 1 && keymaps.hud.filter(x => x === k).length === 1),
    JSON.stringify(keymaps.hud));

  /* ================= the projector's own picker (D1) ================= */
  await proj.bringToFront();
  await stripClick(proj, '#btnPick');
  await proj.waitForTimeout(150);
  const panelOpen = await proj.evaluate(() => ({
    open: window.__LT.pick().open,
    emptyShown: !document.getElementById('pickEmpty').hidden,
    focus: document.activeElement && document.activeElement.id,
    /* Normalised: the copy wraps across source lines, so textContent carries
       newlines mid-sentence. */
    saysVisible: document.getElementById('pickSub').textContent.replace(/\s+/g, ' ').trim()
  }));
  check('D1: the projector has its own picker, empty (rosters do not travel between windows)', panelOpen.open && panelOpen.emptyShown, JSON.stringify(panelOpen));
  check('honest copy: it says the class can see this screen', /class can see/i.test(panelOpen.saysVisible), panelOpen.saysVisible.slice(0, 60));
  await proj.fill('#pickRoster', 'Solo');
  await proj.click('#btnPickLoad');
  await proj.click('#btnPickNext');
  await proj.waitForTimeout(150);
  const firstSolo = await proj.evaluate(() => document.getElementById('pickNote').textContent);
  check('D1: the FIRST draw needs no fallback, so it claims none (nobody had been called yet)', firstSolo === '', JSON.stringify(firstSolo));
  /* The second draw is the one the guarantee genuinely cannot cover. */
  await proj.click('#btnPickNext');
  await proj.waitForTimeout(200);
  const soloDraw = await proj.evaluate(() => ({
    shown: window.__LT.pick().shown, visible: window.__LT.pick().visible,
    note: document.getElementById('pickNote').textContent
  }));
  check('D1: a draw made on the projector shows on the projector', soloDraw.shown === 'Solo' && soloDraw.visible === true, JSON.stringify(soloDraw));
  check('honest copy: with one pupil present it SAYS the no-repeat guard cannot apply', /cannot apply/i.test(soloDraw.note), soloDraw.note);

  /* Escape ladder: the panel, then the name on the wall. */
  await proj.evaluate(() => document.activeElement && document.activeElement.blur());
  await proj.keyboard.press('Escape');
  await proj.waitForTimeout(150);
  const esc1 = await proj.evaluate(() => ({ open: window.__LT.pick().open, visible: window.__LT.pick().visible }));
  check('Esc: the first press closes the picker panel, the name stays up', esc1.open === false && esc1.visible === true, JSON.stringify(esc1));
  await proj.keyboard.press('Escape');
  await proj.waitForTimeout(150);
  const esc2 = await proj.evaluate(() => ({ visible: window.__LT.pick().visible, state: window.__LT.state().pick }));
  check('Esc: the next press takes the name off the wall', esc2.visible === false && esc2.state === '', JSON.stringify(esc2));

  /* Blackout owns the screen here too. */
  await stripClick(proj, '#btnPick');
  await proj.evaluate(() => document.activeElement && document.activeElement.blur());
  await proj.keyboard.press('KeyB');
  await proj.waitForTimeout(150);
  const blacked = await proj.evaluate(() => ({ open: window.__LT.pick().open, blackout: window.__LT.state().blackout }));
  check('blackout: blacking out stands the picker panel down (focus is never buried)', blacked.open === false && blacked.blackout === true, JSON.stringify(blacked));
  await proj.keyboard.press('KeyQ');   // and Q is refused while blacked out
  await proj.waitForTimeout(100);
  await proj.keyboard.press('Escape');
  await proj.waitForTimeout(150);

  /* A name on the wall survives a HUD reload via the resync contract. */
  await proj.evaluate(() => document.activeElement && document.activeElement.blur());
  await stripClick(proj, '#btnPick');
  await proj.click('#btnPickNext');
  await proj.waitForTimeout(200);
  await proj.click('#btnPickClose2');
  const persisted = await proj.evaluate(() => window.__LT.state().pick);
  await hud.reload({ waitUntil: 'load' });
  try { await hud.locator('.mbm-skip').click({ timeout: 4000 }); } catch (e) {}
  await hud.waitForFunction(() => !document.querySelector('.mbm-splash'), null, { timeout: 8000 });
  await hud.waitForTimeout(600);
  const hudSees = await hud.evaluate(() => window.__LT.seen() && window.__LT.seen().pick);
  check('resync: a name already on the wall reaches a freshly reloaded HUD (it is public by then)', hudSees === persisted && persisted === 'Solo', JSON.stringify({ hudSees, persisted }));

  /* ================= no errors anywhere ================= */
  check('no console or page errors on the projector', perrs.length === 0, perrs.join(' | '));
  check('no console or page errors on the HUD', herrs.length === 0, herrs.join(' | '));

  await browser.close();
  srv.close();
  console.log(failures ? 'LT-PICK: ' + failures + ' FAILURE(S)' : 'LT-PICK: all checks passed');
  process.exit(failures ? 1 : 0);
})().catch(e => { console.error('DIED: ' + e.stack); process.exit(1); });
