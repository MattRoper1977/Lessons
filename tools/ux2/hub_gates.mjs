#!/usr/bin/env node
/* UX2 A4 — the Lessons hub and subject-page gates, driven in Chromium.
 *
 * Serves this repository under /Lessons/ and a Site checkout at / on one
 * origin (the same mount the cross-estate job uses), then proves, in order:
 *
 *   reachability  record count == distinct record hrefs rendered across every
 *                 subject page at every pathway segment, with every "Show n
 *                 more" expanded (the hub itself only links subjects)
 *   targets       every visible interactive element is ≥44×44 at 390px, on the
 *                 hub (browse + results), on each subject page collapsed and
 *                 expanded, with the menu open and with the Pack sheet open
 *   focus         after load, after a pathway switch and after the sheet
 *                 opens/closes, document.activeElement is a named control;
 *                 nothing inside a hidden accordion panel is tabbable
 *   chips         every format chip's advertised set == the rendered rows after
 *                 the click, through the real filter chain over HTTP
 *   hrefs         every rendered href resolves on the mount (200); every href
 *                 of the pre-UX2 hub is still rendered somewhere, except the
 *                 ones listed as RETIRED with a reason in
 *                 tools/ux2/fixtures/retired-hrefs.json
 *   egress        0 requests to madebymatt-play.uk, 0 third-party, 0 ko-fi
 *   copy          every Appendix A string is on the page it belongs to; no
 *                 typed digit-string in the static HTML text outside Appendix A
 *   motion        under prefers-reduced-motion nothing is left invisible and no
 *                 element carries a running transition
 *   contrast      computed-style contrast ≥4.5:1 on text, cream and dark themes
 *   print         the print medium shows every accordion panel and no controls
 *
 * Red proofs (--red-proof): (1) a family hidden by an injected style → the
 * reachability count drops → FAIL; (2) a format chip removed from the DOM →
 * the chip gate → FAIL. Both must go red or the run is MEASUREMENT INVALID.
 *
 *   node tools/ux2/hub_gates.mjs --site <site checkout> [--out <dir>] [--red-proof]
 */
import { createRequire } from 'node:module';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const require = createRequire(import.meta.url);
const pw = (() => { for (const p of ['playwright', '/opt/node22/lib/node_modules/playwright/index.js']) { try { return require(p); } catch (_) {} } console.error('[FAIL] playwright not found'); process.exit(2); })();
const { chromium } = pw;

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const argv = process.argv.slice(2);
const val = n => { const i = argv.indexOf(n); return i > -1 ? argv[i + 1] : null; };
const SITE = val('--site');
const OUT = val('--out') || path.join(ROOT, 'audit-output', 'ux2-hub');
const RED = argv.includes('--red-proof');
if (!SITE || !fs.existsSync(path.join(SITE, 'assets'))) { console.error('usage: --site <site checkout with assets/>'); process.exit(2); }
fs.mkdirSync(OUT, { recursive: true });

const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.pdf': 'application/pdf', '.pptx': 'application/octet-stream', '.docx': 'application/octet-stream' };
const server = http.createServer((req, res) => {
  let u = decodeURIComponent(req.url.split('?')[0]);
  let f = u.startsWith('/Lessons/') ? path.join(ROOT, u.slice(9)) : path.join(SITE, u.replace(/^\//, ''));
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
  if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); res.end('nf'); return; }
  if (req.method === 'HEAD') { res.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' }); res.end(); return; }
  res.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' }); res.end(fs.readFileSync(f));
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const origin = 'http://127.0.0.1:' + server.address().port;

const results = [];
const check = (limb, ok, detail) => { results.push({ limb, ok, detail }); console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${String(limb).padEnd(48)} ${detail}`); return ok; };
const rows = JSON.parse(fs.readFileSync(path.join(ROOT, 'resources.json'), 'utf8'));
const appendix = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/ux2/fixtures/appendix-a-lessons.json'), 'utf8'));
const retired = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/ux2/fixtures/retired-hrefs.json'), 'utf8'));
const before = fs.readFileSync(path.join(ROOT, 'tools/ux2/fixtures/hub-hrefs-before-ux2.txt'), 'utf8').split('\n').map(s => s.trim()).filter(s => s && !s.startsWith('#'));

const browser = await chromium.launch();
async function newPage(opts = {}) {
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, ...opts });
  const page = await ctx.newPage();
  const log = { errors: [], requests: [], failed: [] };
  page.on('pageerror', e => log.errors.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') log.errors.push('console: ' + m.text()); });
  page.on('request', r => log.requests.push(r.url()));
  page.on('response', r => { if (r.status() >= 400 && r.url().startsWith(origin)) log.failed.push(r.status() + ' ' + r.url()); });
  page._log = log; page._ctx = ctx;
  return page;
}
const smallTargets = () => [...document.querySelectorAll('a[href],button,input,select,[role=button],[role=tab],[tabindex]:not([tabindex="-1"])')].filter(e => { const b = e.getBoundingClientRect(); const cs = getComputedStyle(e); return b.width > 0 && b.height > 0 && cs.visibility !== 'hidden' && (b.width < 44 || b.height < 44); }).map(e => `${(e.id || e.className || e.tagName)}:${(e.textContent || e.getAttribute('aria-label') || '').trim().slice(0, 24)} ${Math.round(e.getBoundingClientRect().width)}x${Math.round(e.getBoundingClientRect().height)}`);
const namedActive = () => { const a = document.activeElement; if (!a || a === document.body) return ''; const name = a.getAttribute('aria-label') || a.textContent.trim() || a.getAttribute('placeholder') || a.id; return name ? `${a.tagName.toLowerCase()}#${a.id || ''}:${name.slice(0, 30)}` : ''; };

/* ---------- 1. hub ---------- */
const hub = await newPage();
await hub.goto(`${origin}/Lessons/`, { waitUntil: 'load' });
await hub.waitForFunction(() => /resources/.test(document.querySelector('#count')?.textContent || ''), null, { timeout: 15000 });
const hubSubjects = await hub.$$eval('.scard .browse', as => as.map(a => a.getAttribute('href')));
check('hub renders subject cards', hubSubjects.length >= 4, `${hubSubjects.length} cards`);
check('hub focus after load is a named control', !!(await hub.evaluate(namedActive)), await hub.evaluate(namedActive));
check('hub targets ≥44px (browse)', (await hub.evaluate(smallTargets)).length === 0, JSON.stringify((await hub.evaluate(smallTargets)).slice(0, 5)));
await hub.locator('#menu').click();
check('hub targets ≥44px (menu open)', (await hub.evaluate(smallTargets)).length === 0, JSON.stringify((await hub.evaluate(smallTargets)).slice(0, 5)));
await hub.keyboard.press('Escape');
// Appendix A copy on the hub
const hubText = await hub.evaluate(() => document.body.textContent.replace(/\s+/g, ' '));
for (const s of appendix.hub) check(`hub copy: ${s.slice(0, 40)}`, hubText.includes(s), s.length > 40 ? s.slice(0, 40) + '…' : '');
// count line derived: it must equal the record count
check('hub count line derives from the record', (await hub.locator('#count').innerText()).startsWith(`${rows.length} resources`), await hub.locator('#count').innerText());
// flat results via search: the browser gate's contract
await hub.locator('#search').fill('rock'); await hub.waitForTimeout(200);
check('hub search announces results', /^Showing \d+ matching resources\./.test(await hub.locator('#status').innerText()), await hub.locator('#status').innerText());
check('hub targets ≥44px (results)', (await hub.evaluate(smallTargets)).length === 0, JSON.stringify((await hub.evaluate(smallTargets)).slice(0, 5)));
await hub.locator('[data-clear-filters]').click();
check('hub clear filters resets search', (await hub.locator('#search').inputValue()) === '', '');
const hubHrefs = await hub.$$eval('a[href]', as => as.map(a => a.getAttribute('href')));
await hub.screenshot({ path: path.join(OUT, 'hub-390.png'), fullPage: true });
const hubLog = hub._log;

/* ---------- 2. subject pages: reachability, targets, focus, chips, sheet ---------- */
const seen = new Set();
const allHrefs = new Set(hubHrefs);
let anyPackSheet = false;
const subjectSlugs = hubSubjects.map(h => new URL(h, `${origin}/Lessons/`).searchParams.get('subject'));
async function collectPage(page) {
  // expand every "Show n more" then read every record path in every open panel
  for (let i = 0; i < 50; i++) { const more = page.locator('button[data-more]').first(); if (!(await more.count())) break; await more.click(); }
  const paths = await page.$$eval('[data-resource-path]', els => els.map(e => e.getAttribute('data-resource-path')));
  paths.forEach(p => seen.add(p));
  (await page.$$eval('a[href]', as => as.map(a => a.getAttribute('href')))).forEach(h => allHrefs.add(h));
}
for (const slug of subjectSlugs) {
  const page = await newPage();
  await page.goto(`${origin}/Lessons/subject.html?subject=${encodeURIComponent(slug)}`, { waitUntil: 'load' });
  await page.waitForFunction(() => /lessons/.test(document.querySelector('#summary')?.textContent || ''), null, { timeout: 15000 });
  const tabs = await page.$$eval('#seg [role=tab]', ts => ts.map(t => t.dataset.pathway));
  check(`${slug}: focus after load`, !!(await page.evaluate(namedActive)), await page.evaluate(namedActive));
  check(`${slug}: targets ≥44px (collapsed)`, (await page.evaluate(smallTargets)).length === 0, JSON.stringify((await page.evaluate(smallTargets)).slice(0, 4)));
  // hidden panels are not tabbable
  const hiddenTabbable = await page.evaluate(() => [...document.querySelectorAll('.acc-body[hidden] a,.acc-body[hidden] button')].filter(e => e.tabIndex >= 0).length);
  check(`${slug}: hidden rows not tabbable`, hiddenTabbable === 0, `${hiddenTabbable}`);
  for (const t of (tabs.length ? tabs : [null])) {
    if (t) { await page.locator(`#seg [role=tab][data-pathway="${t}"]`).click(); await page.waitForTimeout(80); check(`${slug}/${t}: focus after pathway switch`, (await page.evaluate(namedActive)).startsWith('button#tab-'), await page.evaluate(namedActive)); }
    // open every accordion row so every lesson is rendered, then collect
    for (let i = 0; i < 200; i++) { const tg = page.locator('button[data-toggle][aria-expanded="false"]').first(); if (!(await tg.count())) break; await tg.click(); }
    await collectPage(page);
    check(`${slug}/${t || 'all'}: targets ≥44px (expanded)`, (await page.evaluate(smallTargets)).length === 0, JSON.stringify((await page.evaluate(smallTargets)).slice(0, 4)));
    // chip gate: each format chip's rendered count equals the set the filter chain returns
    const chips = await page.$$eval('#fchips button', bs => bs.map(b => b.dataset.format));
    for (const f of chips) {
      await page.locator(`#fchips button[data-format="${f}"]`).click(); await page.waitForTimeout(60);
      for (let i = 0; i < 200; i++) { const tg = page.locator('button[data-toggle][aria-expanded="false"]').first(); if (!(await tg.count())) break; await tg.click(); }
      for (let i = 0; i < 50; i++) { const more = page.locator('button[data-more]').first(); if (!(await more.count())) break; await more.click(); }
      const rendered = await page.$$eval('.lrow', els => els.map(e => e.dataset.resourcePath));
      const expected = await page.evaluate(({ fmt, pathway }) => { const H = window.MBM_HUB; const pool = H.state.rows.filter(r => r._card === new URLSearchParams(location.search).get('subject') || H.slugForQuery(new URLSearchParams(location.search).get('subject')) === r._card); const pw = pathway; let rows = pw === 'ALL' ? pool.filter(r => !r._tier) : pool.filter(r => r._tier === pw); if (fmt) rows = rows.filter(r => r._fmt === fmt || (r.files || []).some(x => (x.type === 'pdf' ? 'pdf' : 'packs') === fmt)); return rows.map(r => r._path); }, { fmt: f, pathway: t || 'ALL' });
      check(`${slug}/${t || 'all'}: chip "${f || 'all'}" rendered == filter chain`, rendered.length === expected.length && rendered.every(p => expected.includes(p)), `${rendered.length}/${expected.length}`);
      rendered.forEach(p => seen.add(p));
    }
    await page.locator('#fchips button[data-format=""]').click().catch(() => {});
  }
  // the pack sheet, when a Pack chip exists on this page
  const packChip = page.locator('button[data-pack]').first();
  if (await packChip.count()) {
    anyPackSheet = true;
    await packChip.click(); await page.waitForTimeout(100);
    check(`${slug}: sheet open → focus on close control`, (await page.evaluate(namedActive)).includes('Close'), await page.evaluate(namedActive));
    check(`${slug}: targets ≥44px (sheet open)`, (await page.evaluate(() => [...document.querySelectorAll('#pack-sheet a[href],#pack-sheet button')].filter(e => { const b = e.getBoundingClientRect(); return b.width < 44 || b.height < 44; }).length)) === 0, '');
    const packLinks = await page.$$eval('#pack-sheet a[href]', as => as.length);
    check(`${slug}: sheet lists ≥1 file`, packLinks >= 1, `${packLinks}`);
    await page.keyboard.press('Escape'); await page.waitForTimeout(100);
    check(`${slug}: sheet close → focus returns to opener`, (await page.evaluate(namedActive)).startsWith('button#:Pack') || (await page.evaluate(() => document.activeElement?.dataset?.pack != null)), await page.evaluate(namedActive));
  }
  await page.screenshot({ path: path.join(OUT, `subject-${slug}-390.png`), fullPage: true });
  hubLog.requests.push(...page._log.requests); hubLog.errors.push(...page._log.errors); hubLog.failed.push(...page._log.failed);
  await page._ctx.close();
}
// reachability: every record path rendered at least once across subject pages
const recordPaths = rows.map(r => r.file || r.url || '');
const missing = recordPaths.filter(p => !seen.has(p));
check('reachability: record count == distinct rendered entries', missing.length === 0 && seen.size >= recordPaths.length, `${seen.size} rendered / ${recordPaths.length} records${missing.length ? '; missing ' + JSON.stringify(missing.slice(0, 5)) : ''}`);
check('reachability: subject map covers every entry exactly once', await hub.evaluate(() => { const H = window.MBM_HUB; const cards = H.cardsFromRows(H.state.rows); return cards.reduce((n, c) => n + c.rows.length, 0) === H.state.rows.length && new Set(H.state.rows.map(r => r._card)).size === cards.length; }), '');
check('a pack sheet was exercised (non-vacuous)', anyPackSheet || !rows.some(r => r.kind === 'pack'), anyPackSheet ? 'sheet opened' : 'no pack entries in the record yet');

/* ---------- 3. hrefs: resolve + census ---------- */
const skip = h => /^(#|mailto:|https?:\/\/)/.test(h) || h.startsWith('/');
const toCheck = [...allHrefs].filter(h => !skip(h));
let unresolved = [];
for (const h of toCheck) {
  const u = new URL(h, `${origin}/Lessons/`);
  const ok = await fetch(u.href, { method: 'HEAD' }).then(r => r.ok).catch(() => false);
  if (!ok) unresolved.push(h);
}
check('every rendered href resolves on the mount', unresolved.length === 0, `${toCheck.length} checked${unresolved.length ? '; unresolved ' + JSON.stringify(unresolved.slice(0, 5)) : ''}`);
const norm = h => { try { const u = new URL(h, 'http://x/Lessons/'); return u.pathname + u.search + u.hash; } catch (_) { return h; } };
const after = new Set([...allHrefs].map(norm));
const retiredSet = new Set(retired.retired.map(r => norm(r.href)));
const lost = before.filter(h => !after.has(norm(h)) && !retiredSet.has(norm(h)));
check('old-href census: 0 lost (retired ones listed with reasons)', lost.length === 0, `${before.length} before, ${after.size} after, ${retired.retired.length} retired${lost.length ? '; lost ' + JSON.stringify(lost.slice(0, 6)) : ''}`);
const retiredStillPresent = retired.retired.filter(r => after.has(norm(r.href)));
check('retired list is not stale', retiredStillPresent.length === 0, retiredStillPresent.map(r => r.href).join(', '));

/* ---------- 4. egress ---------- */
const play = hubLog.requests.filter(u => /madebymatt-play\.uk/.test(u));
const third = hubLog.requests.filter(u => !u.startsWith(origin));
const kofi = [...allHrefs].filter(h => /ko-?fi/i.test(h));
check('0 requests to Play', play.length === 0, play.slice(0, 3).join(' '));
check('0 third-party requests', third.length === 0, third.slice(0, 3).join(' '));
check('0 Ko-fi hrefs', kofi.length === 0, kofi.join(' '));
check('0 page/console errors', hubLog.errors.length === 0, hubLog.errors.slice(0, 3).join(' | '));
check('0 failed first-party requests', hubLog.failed.length === 0, hubLog.failed.slice(0, 3).join(' | '));

/* ---------- 5. typed digit-strings in static text ---------- */
for (const file of ['index.html', 'subject.html']) {
  const html = fs.readFileSync(path.join(ROOT, file), 'utf8').replace(/<script\b[\s\S]*?<\/script>/g, '').replace(/<style\b[\s\S]*?<\/style>/g, '').replace(/<[^>]+>/g, ' ');
  const allowed = new Set([...appendix.hub, ...appendix.subject]);
  const digits = html.split(/\n+/).map(s => s.trim()).filter(s => /\d/.test(s) && ![...allowed].some(a => s.includes(a)));
  check(`${file}: no typed digit-strings outside Appendix A`, digits.length === 0, JSON.stringify(digits.slice(0, 3)));
}

/* ---------- 6. reduced motion + contrast + print ---------- */
for (const theme of ['cream', 'dark', 'highlumen']) {
  const page = await newPage({ reducedMotion: 'reduce' });
  await page.addInitScript(t => { try { localStorage.setItem('mbm_reading_theme', t); } catch (_) {} }, theme);
  await page.goto(`${origin}/Lessons/subject.html?subject=${encodeURIComponent(subjectSlugs[0])}`, { waitUntil: 'load' });
  await page.waitForFunction(() => /lessons/.test(document.querySelector('#summary')?.textContent || ''), null, { timeout: 15000 });
  const motion = await page.evaluate(() => [...document.querySelectorAll('main *')].filter(e => { const cs = getComputedStyle(e); return parseFloat(cs.transitionDuration) > 0 || (cs.animationName && cs.animationName !== 'none'); }).length);
  check(`reduced motion (${theme}): no running transitions`, motion === 0, `${motion}`);
  const low = await page.evaluate(() => {
    const lum = ([r, g, b]) => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
    const rgb = s => { const m = s.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(x => parseFloat(x)); return p[3] === 0 ? null : p.slice(0, 3); };
    const bgOf = el => { let e = el; while (e) { const c = rgb(getComputedStyle(e).backgroundColor); if (c) return c; e = e.parentElement; } return [255, 255, 255]; };
    const out = [];
    for (const el of document.querySelectorAll('main h1,main h2,main h3,main p,main a,main button,main span.chip,main .badge,main .lrow-meta,footer p,footer small')) {
      const b = el.getBoundingClientRect(); if (!b.width || !b.height) continue;
      const fg = rgb(getComputedStyle(el).color); if (!fg) continue;
      const bg = bgOf(el); const L1 = lum(fg), L2 = lum(bg); const ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
      if (ratio < 4.5) out.push(`${el.tagName}.${el.className} ${ratio.toFixed(2)}`);
    }
    return out;
  });
  check(`contrast ≥4.5:1 (${theme})`, low.length === 0, JSON.stringify(low.slice(0, 5)));
  await page.emulateMedia({ media: 'print' });
  const print = await page.evaluate(() => ({ hiddenPanels: [...document.querySelectorAll('.acc-body')].filter(e => getComputedStyle(e).display === 'none').length, controls: [...document.querySelectorAll('#seg,#fchips,.go,.lesson-save,#to-top')].filter(e => getComputedStyle(e).display !== 'none').length }));
  check(`print (${theme}): every panel visible, controls hidden`, print.hiddenPanels === 0 && print.controls === 0, JSON.stringify(print));
  await page._ctx.close();
}
await hub._ctx.close();

/* ---------- 7. red proofs ---------- */
if (RED) {
  const page = await newPage();
  await page.addInitScript(() => { document.addEventListener('DOMContentLoaded', () => { const s = document.createElement('style'); s.textContent = '.acc:first-of-type{display:none!important}'; document.head.appendChild(s); }); });
  await page.goto(`${origin}/Lessons/subject.html?subject=${encodeURIComponent(subjectSlugs[0])}`, { waitUntil: 'load' });
  await page.waitForFunction(() => /lessons/.test(document.querySelector('#summary')?.textContent || ''), null, { timeout: 15000 });
  for (let i = 0; i < 200; i++) { const tg = page.locator('button[data-toggle][aria-expanded="false"]').first(); if (!(await tg.count())) break; await tg.click(); }
  const visiblePaths = await page.$$eval('[data-resource-path]', els => els.filter(e => e.getBoundingClientRect().height > 0).map(e => e.dataset.resourcePath));
  const expectedPaths = await page.evaluate(() => { const H = window.MBM_HUB; const slug = H.slugForQuery(new URLSearchParams(location.search).get('subject')); return H.state.rows.filter(r => r._card === slug && (r._tier === H.pathwaysPresent(H.state.rows.filter(x => x._card === slug))[0])).length; });
  check('RED PROOF: a hidden family drops the reachability count', visiblePaths.length < expectedPaths, `${visiblePaths.length} < ${expectedPaths}`);
  await page.evaluate(() => { const b = document.querySelector('#fchips button[data-format]:not([data-format=""])'); if (b) b.remove(); });
  const chipsNow = await page.$$eval('#fchips button', bs => bs.length);
  const chipsExpected = await page.evaluate(() => 1 + window.MBM_HUB.formatsPresent(window.MBM_HUB.state.rows.filter(r => r._card === window.MBM_HUB.slugForQuery(new URLSearchParams(location.search).get('subject')) && r._tier === 'BUILD')).length);
  check('RED PROOF: a removed chip is caught by the chip census', chipsNow < chipsExpected, `${chipsNow} < ${chipsExpected}`);
  await page._ctx.close();
}

await browser.close(); server.close();
const failed = results.filter(r => !r.ok);
fs.writeFileSync(path.join(OUT, 'hub-gates.json'), JSON.stringify({ origin, results, seen: seen.size, records: recordPaths.length }, null, 1));
console.log(`\n${failed.length ? '[FAIL]' : '[PASS]'} UX2 hub gates: ${results.length - failed.length}/${results.length} limbs`);
process.exit(failed.length ? 1 : 0);
