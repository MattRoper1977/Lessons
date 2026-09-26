#!/usr/bin/env node
// DLG-1: no visible control opens a hidden dialog (ruling LAND-A2 R5 §2).
//
// A dialog tagged data-mbm-guide="staff" is display:none!important on screen while the staff guide is
// off. If its button is not tagged too, the button shows, showModal() makes the whole page inert behind
// a dialog nobody can see, and the lesson freezes until someone thinks to press Escape.
//
// Measured in Chromium, on every served Humanities, RE and Science page that has a dialog, in BOTH
// staff-guide states (html.mbm-guide-on off and on; the page's own toggle is not needed, so a page with
// no toggle is still held to the "on" state it would reach the day one is added):
//
//   hidden   every visible control that opens a dialog opens a VISIBLE one: non-zero box, and neither it
//            nor an ancestor is display:none, visibility:hidden or opacity 0
//   focus    the opened dialog takes focus (the active element is the dialog or inside it)
//   escape   Escape closes it, and focus returns to the control that opened it
//   close    its own Close button closes it, and focus returns to the control that opened it
//
// A control is "visible" when checkVisibility() holds with opacity and visibility checked and its box is
// non-zero, with every slide laid out so a control on any slide is measured. Controls are clicked with a
// real pointer-free .click(); navigation, print, window.open and downloads are neutralised so a click can
// only change the page itself.
//
// THE ONE EXCEPTION (ruling LAND-A2 R8 §1). SCI_B_W8B is fenced by _sx3/FENCE.json (ORDER SX3-M4 §1(b)),
// so DLG-1 lands on the other 173 pages and W8B keeps its two freezing controls until its fallback limb
// lands. dialog_audience_exceptions.json (next to this file) names it, with the exact failures the probe
// measured on Lessons main c527b7c1, the ruling, the date it was added and the date it expires. RULED
// below is the ceiling that file may never exceed, and the list can only shrink:
//   - the listed page must fail with EXACTLY the listed controls: any other failure on it, or a listed
//     control that no longer fails, FAILS (remove what was fixed; nothing may be added);
//   - a listed page that passes FAILS as a stale exception: remove it;
//   - on or after the expiry date (16 Oct 2026; W8B is a return-week lesson for 19 Oct) the exception is
//     not honoured, and the guard FAILS telling the reader to STOP and ask for a release ruling;
//   - an entry for any other page, a second entry, a control or field beyond RULED, a later expiry, or a
//     malformed list FAILS, and then no entry is honoured;
//   - any unlisted failing page FAILS as it always did.
// A missing list file means no exceptions. "Today" is the real UTC date. --today may move it FORWARD only,
// to rehearse the expiry; an earlier date is refused, so it can never keep an expired exception alive.
//
// Usage: node check_dialog_audience.cjs [--root DIR] [--only SUBSTR] [--json FILE] [--exceptions FILE] [--today YYYY-MM-DD]
//        node check_dialog_audience.cjs --self-test     pure: the exception rules on fixture rows, no browser
//   --only SUBSTR  measure only the served pages whose repository path contains SUBSTR (e.g. SCI_B_W8B);
//                  an exception whose page lies outside that scope is not judged
//   --json FILE    write every measured row (the fixer, fix_dialog_audience.py, reads it)
// Exit 1 on any failure, 2 if the probe itself cannot run.
'use strict';
const fs = require('fs'), path = require('path'), cp = require('child_process');
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; };
const ROOT = path.resolve(arg('--root', '.'));
const ONLY = arg('--only', '');
const JSON_OUT = arg('--json', '');
const EXCEPTIONS = path.resolve(arg('--exceptions', path.join(__dirname, 'dialog_audience_exceptions.json')));
const TREES = ['Humanities_Teesside', 'Science_Teesside'];

// ---------------------------------------------------------------------------------------- the exception

const W8B_HIDDEN = (control, dialog) => `hidden: "${control}" opens #${dialog}, which does not show (display none, visibility visible, opacity 1, 0x0)`;
const RULED = Object.freeze({
  path: 'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8B_Autumn_Science_Checkpoint_Do.html',
  reason: 'fenced by _sx3/FENCE.json (ORDER SX3-M4 §1(b)); held out of DLG-1 by LAND-A2 R8 §1',
  ruling: 'LAND-A2 R8 §1',
  added: '2026-09-26',
  expires: '2026-10-16',
  leaves_when: 'its fallback limb lands',
  controls: [
    { state: 'guide-off', check: 'hidden', control: 'TA Brief', action: 'ta', dialog: 'ta-dialog', failure: W8B_HIDDEN('TA Brief', 'ta-dialog') },
    { state: 'guide-off', check: 'hidden', control: 'Question', action: 'cold-call', dialog: 'cold-call-dialog', failure: W8B_HIDDEN('Question', 'cold-call-dialog') },
  ],
});
const ENTRY_KEYS = ['added', 'controls', 'expires', 'leaves_when', 'path', 'reason', 'ruling'];
const CONTROL_KEYS = ['action', 'check', 'control', 'dialog', 'failure', 'state'];
const PINNED = ['path', 'reason', 'ruling', 'added', 'leaves_when'];
const ISO = /^\d{4}-\d{2}-\d{2}$/;
const validDate = s => { if (typeof s !== 'string' || !ISO.test(s)) return false; const d = new Date(s + 'T00:00:00Z'); return !isNaN(d) && d.toISOString().slice(0, 10) === s; };
const sameKeys = (o, keys) => o && typeof o === 'object' && !Array.isArray(o) && JSON.stringify(Object.keys(o).sort()) === JSON.stringify(keys);
const key = c => [c.state, c.check, c.control, c.action, c.dialog, c.failure].join('\u0001');
const RULED_KEYS = new Set(RULED.controls.map(key));
const describe = c => `${c.state} ${c.failure}`;

// text of the list file (or null when there is none) -> { entries: honoured entries by path, problems: [] }
function readExceptions(text, name) {
  if (text === null) return { entries: new Map(), problems: [] };
  const bad = m => ({ entries: new Map(), problems: [`malformed exception list ${name}: ${m}`] });
  let doc;
  try { doc = JSON.parse(text); } catch (e) { return bad('not JSON (' + e.message + ')'); }
  if (!doc || typeof doc !== 'object' || Array.isArray(doc) || !Array.isArray(doc.exceptions)
      || Object.keys(doc).some(k => k !== 'about' && k !== 'exceptions')) return bad('want an object with "exceptions": [...] and at most an "about"');
  const problems = [];
  if (doc.exceptions.length > 1) problems.push(`exception list grows: ${doc.exceptions.length} entries; ${RULED.ruling} ruled one (${RULED.path}) and the list may only shrink`);
  const entries = new Map();
  doc.exceptions.forEach((e, i) => {
    const at = `${name} entry ${i}`;
    if (!sameKeys(e, ENTRY_KEYS)) return problems.push(`malformed exception list ${at}: want exactly the fields ${ENTRY_KEYS.join(', ')}`);
    if (e.path !== RULED.path) return problems.push(`exception list grows: ${e.path} is not the page ${RULED.ruling} ruled (${RULED.path})`);
    const off = PINNED.filter(k => e[k] !== RULED[k]);
    if (off.length) return problems.push(`malformed exception list ${at}: ${off.map(k => `${k} must be "${RULED[k]}"`).join('; ')}`);
    if (!validDate(e.expires)) return problems.push(`malformed exception list ${at}: expires must be a date YYYY-MM-DD`);
    if (e.expires > RULED.expires) return problems.push(`exception extended: ${e.path} expires ${e.expires}, later than the ruled ${RULED.expires}; ${RULED.ruling} does not allow it`);
    if (!Array.isArray(e.controls) || !e.controls.length) return problems.push(`malformed exception list ${at}: controls must be a non-empty list (remove the entry when nothing fails)`);
    const seen = new Set();
    for (const c of e.controls) {
      if (!sameKeys(c, CONTROL_KEYS) || CONTROL_KEYS.some(k => typeof c[k] !== 'string')) return problems.push(`malformed exception list ${at}: each control wants exactly the string fields ${CONTROL_KEYS.join(', ')}`);
      if (!RULED_KEYS.has(key(c))) return problems.push(`exception list grows: ${e.path} lists a control ${RULED.ruling} did not rule: ${describe(c)}`);
      if (seen.has(key(c))) return problems.push(`malformed exception list ${at}: a control is listed twice: ${describe(c)}`);
      seen.add(key(c));
    }
    entries.set(e.path, e);
  });
  return problems.length ? { entries: new Map(), problems } : { entries, problems };
}

// every measured failure on a row, with its state
const failuresOf = row => Object.entries(row.states).flatMap(([state, v]) => (v.failures || []).map(f => ({ state, ...f })));

// one measured row against its exception (or none) -> { lines: [FAIL text], excepted: bool }
function judgeRow(row, entry, today) {
  const got = failuresOf(row);
  const plain = () => [`${row.page}\n  ${[...new Set(got.map(describe))].join('\n  ')}`];
  if (!entry) return { lines: got.length ? plain() : [], excepted: false };
  if (!got.length) return { lines: [`stale exception: ${row.page} passes in both staff-guide states; remove it from the exception list (${entry.ruling}: it leaves when ${entry.leaves_when})`], excepted: false };
  if (today >= entry.expires) {
    return { lines: [`exception expired: ${row.page} was excepted by ${entry.ruling} until ${entry.expires} and still fails on ${today}. `
      + `STOP: ask for a release ruling (${entry.ruling}: it leaves when ${entry.leaves_when}, or by ${entry.expires} at the latest)`, ...plain()], excepted: false };
  }
  const listed = new Map(entry.controls.map(c => [key(c), c]));
  const measured = new Map(got.map(f => [key(f), f]));
  const extra = [...measured.keys()].filter(k => !listed.has(k)).map(k => measured.get(k));
  const gone = [...listed.keys()].filter(k => !measured.has(k)).map(k => listed.get(k));
  if (!extra.length && !gone.length) return { lines: [], excepted: true };
  return { lines: [`exception does not match: ${row.page} must fail with exactly the ${listed.size} listed control(s) (${entry.ruling})`
    + extra.map(f => `\n  unlisted failure: ${describe(f)}`).join('')
    + gone.map(c => `\n  listed control no longer fails, remove it from the exception: ${describe(c)}`).join('')], excepted: false };
}

// all rows -> { lines, excepted: [pages] }; `inScope(path)` says whether a page was eligible for measuring
function judge(rows, list, today, inScope) {
  const lines = [...list.problems], excepted = [];
  const measured = new Set(rows.map(r => r.page));
  for (const row of rows) {
    const v = judgeRow(row, list.entries.get(row.page), today);
    lines.push(...v.lines);
    if (v.excepted) excepted.push(row.page);
  }
  for (const [p, e] of list.entries) {
    if (!measured.has(p) && inScope(p)) lines.push(`stale exception: ${p} is not a served page with a dialog; remove it from the exception list (${e.ruling})`);
  }
  return { lines, excepted };
}

function utcToday() { return new Date().toISOString().slice(0, 10); }

// ---------------------------------------------------------------------------------------- the probe

function servedPages() {
  let files = [];
  try {
    files = cp.execFileSync('git', ['-C', ROOT, 'ls-files', '-z', '--', ...TREES], { encoding: 'utf8', maxBuffer: 1 << 28, stdio: ['ignore', 'pipe', 'ignore'] }).split('\0');
  } catch (_) { files = []; }
  if (!files.filter(Boolean).length) {
    const walk = d => { if (!fs.existsSync(path.join(ROOT, d))) return; for (const e of fs.readdirSync(path.join(ROOT, d), { withFileTypes: true })) {
      const r = path.join(d, e.name); if (e.isDirectory()) walk(r); else files.push(r); } };
    TREES.forEach(walk);
  }
  // served = what the publisher copies: no path part starting with _ or .
  return files.filter(f => /\.html?$/.test(f) && !f.split('/').some(p => p.startsWith('_') || p.startsWith('.')))
    .filter(f => !ONLY || f.includes(ONLY))
    .filter(f => /<dialog\b/i.test(fs.readFileSync(path.join(ROOT, f), 'utf8')))
    .sort();
}

const NEUTRALISE = () => {
  // an svg role=button has no .click(); a dispatched click reaches the same listeners
  // Inactive slides are inert. A control is only ever used while its own slide is the active one, so the
  // control being measured has the inert lifted from its own ancestors, and everything else keeps it.
  window.__dlgWake = el => { window.__dlgInert = []; for (let a = el; a; a = a.parentElement) if (a.inert) { a.inert = false; window.__dlgInert.push(a); } };
  window.__dlgSleep = () => { (window.__dlgInert || []).forEach(a => { a.inert = true; }); window.__dlgInert = []; };
  window.__dlgPress = el => { if (el.focus) el.focus(); if (typeof el.click === 'function') el.click(); else el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true })); };
  window.print = () => {};
  window.open = () => null;
  window.alert = () => {}; window.confirm = () => false; window.prompt = () => null;
  // every dialog opening is recorded, whatever opens it
  const log = window.__dlgOpened = [];
  for (const m of ['showModal', 'show']) {
    const orig = HTMLDialogElement.prototype[m];
    HTMLDialogElement.prototype[m] = function () { log.push(this); return orig.apply(this, arguments); };
  }
  // a download link click must not leave the page
  document.addEventListener('click', e => { const a = e.target.closest && e.target.closest('a[download]'); if (a) e.preventDefault(); }, true);
};

// Served over a local HTTP origin, as the site is: Playwright cannot intercept a file:// navigation,
// so a page that sets location.href would otherwise leave mid-measurement.
function serve(root) {
  const http = require('http');
  const types = { '.html': 'text/html; charset=utf-8', '.htm': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript',
    '.mjs': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.gif': 'image/gif', '.mp4': 'video/mp4', '.woff2': 'font/woff2', '.pdf': 'application/pdf' };
  const server = http.createServer((req, res) => {
    const rel = decodeURIComponent(new URL(req.url, 'http://x').pathname).replace(/^\/+/, '');
    const abs = path.join(root, rel);
    if (!abs.startsWith(root) || !fs.existsSync(abs) || !fs.statSync(abs).isFile()) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'content-type': types[path.extname(abs).toLowerCase()] || 'application/octet-stream' });
    fs.createReadStream(abs).pipe(res);
  });
  return new Promise(ok => server.listen(0, '127.0.0.1', () => ok(server)));
}

async function main() {
  let today = utcToday();
  const asked = arg('--today', '');
  if (asked) {
    if (!validDate(asked)) { console.error(`--today wants a date YYYY-MM-DD, not "${asked}"`); process.exit(2); }
    if (asked < today) { console.error(`--today ${asked} is earlier than today (${today} UTC): it may only move the clock forward, to rehearse an expiry`); process.exit(2); }
    today = asked;
  }
  const list = readExceptions(fs.existsSync(EXCEPTIONS) ? fs.readFileSync(EXCEPTIONS, 'utf8') : null, path.basename(EXCEPTIONS));

  const { chromium } = require('playwright');
  const server = await serve(ROOT);
  const ORIGIN = 'http://127.0.0.1:' + server.address().port + '/';
  const browser = await chromium.launch({ executablePath: process.env.MBM_CHROMIUM_PATH || undefined });
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, acceptDownloads: false });
  await context.addInitScript(NEUTRALISE);
  const page = await context.newPage();
  page.on('dialog', d => d.dismiss().catch(() => {}));
  // once a page has loaded, no click may navigate it: not away, and not a reload of itself either
  let loaded = false;
  await page.route('**/*', route => {
    const r = route.request();
    // a 204 keeps the current document; an abort would swap in Chromium's error page
    if (loaded && r.isNavigationRequest() && r.frame() === page.mainFrame()) return route.fulfill({ status: 204 });
    return route.continue();
  });

  const pages = servedPages();
  const results = [];
  const printed = [];
  let failures = 0;
  let retried = 0;
  for (const rel of pages) {
    const row = { page: rel, states: {} };
    for (const on of [false, true]) {
      const fails = [];
      let n = 0;
      const opened = [];
      const load = async () => {
        loaded = false;
        await page.goto(ORIGIN + rel.split('/').map(encodeURIComponent).join('/'));
        await page.waitForTimeout(60);
        loaded = true;
        await page.evaluate(on => document.documentElement.classList.toggle('mbm-guide-on', on), on);
        // every slide laid out, so a control on any slide is measured; [hidden] stays hidden
        await page.addStyleTag({ content: '.slide,section.slide{display:block!important;visibility:visible!important;opacity:1!important}' });
        return page.evaluate(() => {
          const vis = el => el.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true }) && el.getBoundingClientRect().width > 0 && el.getBoundingClientRect().height > 0;
          // the staff-guide toggle itself is the state under test, not a control that opens anything
          const ctl = [...document.querySelectorAll('button,[role="button"]')].filter(b => !b.closest('dialog') && !b.disabled && vis(b)
            && !b.matches('.n6m-guide-btn,.mbm-guide-btn,[data-n6m-guide-control]'));
          window.__dlgCtl = ctl;
          return ctl.length;
        });
      };
      const measure = async i => {
        const out = [];
        const r = await page.evaluate(([i, on]) => {
          document.querySelectorAll('dialog[open]').forEach(d => d.close());
          // an earlier click may have moved the guide (a close handler that strips it); hold the state under test
          document.documentElement.classList.toggle('mbm-guide-on', on);
          const b = window.__dlgCtl[i];
          if (!b || !b.isConnected) return null;
          const vis = el => el.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true }) && el.getBoundingClientRect().width > 0 && el.getBoundingClientRect().height > 0;
          if (!vis(b)) return null; // an earlier click hid it (a reveal, a route); it was measured while it showed
          window.__dlgOpened.length = 0;
          window.__dlgSleep(); window.__dlgWake(b);
          window.__dlgPress(b); // as a pointer or keyboard user does: the control holds focus when it acts
          const d = window.__dlgOpened.filter(x => x.open).pop();
          if (!d) return null;
          const cs = getComputedStyle(d), box = d.getBoundingClientRect();
          const label = (b.getAttribute('aria-label') || b.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40);
          const res = { i, control: label, action: b.dataset.action || b.getAttribute('onclick') || b.id || '', dialog: d.id || d.className,
            visible: vis(d), display: cs.display, visibility: cs.visibility, opacity: cs.opacity, w: Math.round(box.width), h: Math.round(box.height),
            focus: d === document.activeElement || d.contains(document.activeElement) };
          if (!res.visible) d.close(); // otherwise the page stays inert for the next control
          return res;
        }, [i, on]);
        if (!r) return { r, out };
        // every failure names its check and the control, action and dialog it was measured on, so the
        // exception can be matched exactly rather than by a substring of its text
        const fail = (check, failure) => out.push({ check, control: r.control, action: r.action, dialog: String(r.dialog), failure });
        if (!r.visible) {
          fail('hidden', `hidden: "${r.control}" opens #${r.dialog}, which does not show (display ${r.display}, visibility ${r.visibility}, opacity ${r.opacity}, ${r.w}x${r.h})`);
          return { r, out };
        }
        if (!r.focus) fail('focus', `focus: #${r.dialog} opened by "${r.control}" does not take focus`);
        // Escape closes, focus returns to the control that opened it
        await page.keyboard.press('Escape');
        const esc = await page.evaluate(i => { const d = window.__dlgOpened.slice(-1)[0]; return { closed: !d.open, back: document.activeElement === window.__dlgCtl[i] }; }, i);
        if (!esc.closed) fail('escape', `escape: Escape does not close #${r.dialog} ("${r.control}")`);
        else if (!esc.back) fail('escape', `escape: focus does not return to "${r.control}" after #${r.dialog} closes`);
        // its own Close button closes, focus returns
        const cl = await page.evaluate(([i, on]) => {
          document.querySelectorAll('dialog[open]').forEach(d => d.close());
          document.documentElement.classList.toggle('mbm-guide-on', on);
          window.__dlgOpened.length = 0;
          window.__dlgPress(window.__dlgCtl[i]);
          const d = window.__dlgOpened.filter(x => x.open).pop();
          if (!d) return { reopened: false };
          const vis = el => el.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true }) && el.getBoundingClientRect().width > 0;
          const c = [...d.querySelectorAll('button,[role="button"]')].filter(vis)
            .find(x => x.dataset.action === 'close' || /^(close\b|done$|×$|✕$|x$)/i.test((x.textContent || '').trim())
              || /close/i.test(x.getAttribute('aria-label') || '') || x.value === 'cancel' || !!x.closest('form[method="dialog"]'));
          if (!c) { d.close(); return { reopened: true, has: false }; }
          window.__dlgPress(c);
          return { reopened: true, has: true, closed: !d.open, back: document.activeElement === window.__dlgCtl[i] };
        }, [i, on]);
        if (cl.reopened && !cl.has) fail('close', `close: #${r.dialog} has no visible Close button`);
        else if (cl.reopened && !cl.closed) fail('close', `close: Close does not close #${r.dialog}`);
        else if (cl.reopened && !cl.back) fail('close', `close: focus does not return to "${r.control}" after Close`);
        return { r, out };
      };
      try {
      n = await load();
      for (let i = 0; i < n; i++) {
        let { r, out } = await measure(i);
        if (!r) continue;
        if (r.visible && out.length) {
          // A focus, Escape or Close failure is measured again on a freshly loaded page: an earlier control's
          // deferred work (a slide transition, a timer) can land mid-check, and only a repeat is the page's own.
          await load();
          const again = await measure(i);
          out = again.r ? again.out : [];
          if (!out.length) retried++;
        }
        fails.push(...out);
        opened.push(r);
      }
      } catch (e) {
        // a page the probe cannot drive is a failure to look at, never a silent pass
        fails.push({ check: 'error', control: '', action: '', dialog: '', failure: 'error: ' + String(e.message || e).split('\n')[0] });
      }
      row.states[on ? 'guide-on' : 'guide-off'] = { controls: n, opens: opened.map(o => ({ control: o.control, action: o.action, dialog: o.dialog, visible: o.visible })),
        fails: fails.map(f => f.failure), failures: fails };
      failures += fails.length;
    }
    // judged as each page finishes, so a long run shows its failures as it goes
    const v = judgeRow(row, list.entries.get(rel), today);
    if (v.excepted) {
      const e = list.entries.get(rel);
      row.exception = { ruling: e.ruling, expires: e.expires, leaves_when: e.leaves_when };
      console.log(`EXCEPTED ${rel}: fails with exactly the ${e.controls.length} listed control(s); ${e.ruling}, until ${e.expires} (it leaves when ${e.leaves_when})`);
    }
    v.lines.forEach(l => console.log('FAIL ' + l));
    printed.push(...v.lines);
    results.push(row);
  }
  await browser.close();
  server.close();
  if (JSON_OUT) fs.writeFileSync(JSON_OUT, JSON.stringify(results, null, 1));
  // the per-page verdicts are printed above; what is left is the list itself and any listed page not measured
  const all = judge(results, list, today, p => !ONLY || p.includes(ONLY));
  const rest = all.lines.filter(l => !printed.includes(l));
  rest.forEach(l => console.log('FAIL ' + l));
  const failing = results.filter(r => failuresOf(r).length).length;
  console.log(`dialog audience: ${results.length} served pages with a dialog${ONLY ? ` (--only ${ONLY})` : ''}, ${failing} failing, ${all.excepted.length} of them excepted `
    + `(${RULED.ruling}, today ${today}); ${failures} failures (both staff-guide states); ${retried} focus/Escape/Close check(s) passed only on a fresh page; `
    + `${list.problems.length} exception-list problem(s)`);
  console.log(all.lines.length ? `FAIL: ${all.lines.length} failure(s)` : 'PASS');
  process.exit(all.lines.length ? 1 : 0);
}

// ---------------------------------------------------------------------------------------- self-test

function selfTest() {
  const W8B = RULED.path, OTHER = 'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W9A_Fixture_Do.html';
  const f = c => ({ check: c.check, control: c.control, action: c.action, dialog: c.dialog, failure: c.failure });
  const row = (page, offFails = [], onFails = []) => ({ page, states: {
    'guide-off': { failures: offFails.map(f) }, 'guide-on': { failures: onFails.map(f) } } });
  const [ta, q] = RULED.controls;
  const word = { check: 'hidden', control: 'Word help', action: 'words', dialog: 'word-dialog', failure: W8B_HIDDEN('Word help', 'word-dialog') };
  const entry = { path: RULED.path, controls: RULED.controls.map(c => ({ ...c })), reason: RULED.reason, ruling: RULED.ruling,
    added: RULED.added, expires: RULED.expires, leaves_when: RULED.leaves_when };
  const listText = (entries, about = 'fixture') => JSON.stringify({ about, exceptions: entries });
  const good = listText([entry]);
  const everywhere = () => true;
  const cases = [
    // name, list text, rows, today, want failing?, substrings the failure lines must contain, want excepted pages
    ['matched exception passes (both listed controls fail, nothing else)', good, [row(W8B, [ta, q]), row(OTHER)], '2026-09-26', false, [], [W8B]],
    ['the day before expiry still passes', good, [row(W8B, [q, ta])], '2026-10-15', false, [], [W8B]],
    ['an extra failing control on the listed page FAILS', good, [row(W8B, [ta, q, word])], '2026-09-26', true, ['exception does not match', 'unlisted failure: guide-off hidden: "Word help"'], []],
    ['a listed control failing in the other staff-guide state FAILS', good, [row(W8B, [ta], [q])], '2026-09-26', true, ['unlisted failure: guide-on hidden: "Question"', 'listed control no longer fails'], []],
    ['a listed control that no longer fails FAILS (the exception must shrink)', good, [row(W8B, [ta])], '2026-09-26', true, ['listed control no longer fails, remove it from the exception: guide-off hidden: "Question"'], []],
    ['the listed page now passing FAILS as stale', good, [row(W8B)], '2026-09-26', true, ['stale exception: ' + W8B + ' passes in both staff-guide states; remove it'], []],
    ['on the expiry date the exception FAILS: STOP and ask for a release ruling', good, [row(W8B, [ta, q])], '2026-10-16', true, ['exception expired', 'STOP: ask for a release ruling (LAND-A2 R8 §1'], []],
    ['after the expiry date it still FAILS', good, [row(W8B, [ta, q])], '2026-11-02', true, ['exception expired'], []],
    ['an unlisted failing page FAILS as before', good, [row(W8B, [ta, q]), row(OTHER, [q])], '2026-09-26', true, [OTHER + '\n  guide-off hidden: "Question"'], [W8B]],
    ['with no list at all, the W8B failures FAIL', null, [row(W8B, [ta, q])], '2026-09-26', true, [W8B + '\n  guide-off hidden:'], []],
    ['the list shrunk to nothing: W8B fixed passes, nothing excepted', listText([]), [row(W8B), row(OTHER)], '2026-09-26', false, [], []],
    ['a second entry FAILS: the list may only shrink', listText([entry, { ...entry, path: OTHER }]), [row(W8B, [ta, q]), row(OTHER, [q])], '2026-09-26', true, ['exception list grows: 2 entries'], []],
    ['an entry for another page FAILS', listText([{ ...entry, path: OTHER }]), [row(OTHER, [q])], '2026-09-26', true, ['exception list grows: ' + OTHER + ' is not the page'], []],
    ['a control beyond the ruled two FAILS', listText([{ ...entry, controls: [...entry.controls, { state: 'guide-off', ...word }] }]), [row(W8B, [ta, q, word])], '2026-09-26', true, ['lists a control LAND-A2 R8 §1 did not rule'], []],
    ['an expiry later than the ruled 2026-10-16 FAILS', listText([{ ...entry, expires: '2026-10-30' }]), [row(W8B, [ta, q])], '2026-09-26', true, ['exception extended'], []],
    ['a malformed list FAILS', '{"exceptions": [', [row(W8B, [ta, q])], '2026-09-26', true, ['malformed exception list'], []],
    ['a field missing FAILS as malformed', listText([{ ...entry, leaves_when: undefined }]), [row(W8B, [ta, q])], '2026-09-26', true, ['malformed exception list'], []],
    ['a listed page not measured in a full run FAILS as stale', good, [row(OTHER)], '2026-09-26', true, ['stale exception: ' + W8B + ' is not a served page with a dialog'], []],
  ];
  let ok = true;
  for (const [name, text, rows, today, wantFail, want, wantExcepted] of cases) {
    const list = readExceptions(text, 'fixture.json');
    const v = judge(rows, list, today, everywhere);
    const good1 = (v.lines.length > 0) === wantFail && want.every(w => v.lines.some(l => l.includes(w)))
      && JSON.stringify(v.excepted) === JSON.stringify(wantExcepted);
    ok = ok && good1;
    console.log(`  ${good1 ? 'ok    ' : 'FAILED'} ${name}`);
    v.lines.forEach(l => console.log('           -> ' + l.replace(/\n/g, '\n              ')));
  }
  // --only scope: a listed page outside the measured scope is not judged
  {
    const v = judge([row(OTHER)], readExceptions(good, 'fixture.json'), '2026-09-26', p => p.includes('SCI_B_W9A'));
    const good1 = v.lines.length === 0;
    ok = ok && good1;
    console.log(`  ${good1 ? 'ok    ' : 'FAILED'} with --only scoped away from W8B, its exception is not judged`);
  }
  // the committed list is exactly the ruled entry today (it may shrink later; this reports, it does not pin)
  if (fs.existsSync(EXCEPTIONS)) {
    const list = readExceptions(fs.readFileSync(EXCEPTIONS, 'utf8'), path.basename(EXCEPTIONS));
    const good1 = !list.problems.length;
    ok = ok && good1;
    console.log(`  ${good1 ? 'ok    ' : 'FAILED'} the committed ${path.basename(EXCEPTIONS)} is well formed and within ${RULED.ruling}: ${list.entries.size} entr${list.entries.size === 1 ? 'y' : 'ies'}`
      + [...list.entries.values()].map(e => ` (${e.path}, ${e.controls.length} control(s), until ${e.expires})`).join(''));
    list.problems.forEach(l => console.log('           -> ' + l));
  }
  console.log('self-test ' + (ok ? 'PASS' : 'FAIL'));
  process.exit(ok ? 0 : 1);
}

if (process.argv.includes('--self-test')) selfTest();
else main().catch(e => { console.error(e); process.exit(2); });
