#!/usr/bin/env node
// The Humanities and RE lesson floor (ruling LAND-A2 R2 H2).
//
// HUM-D5 fixed these on the live lessons; a later pack delivery silently undid every one
// of them and no check noticed. This gate measures each property in Chromium, on every
// Humanities and RE *_Lesson.html in the tree, so the next delivery cannot do it again:
//
//   ribbon   every model-node ribbon item (.step-ribbon > *) has text contrast >= 4.5:1   (D2 B0125)
//   timer    BUILD/GROW: every text in #auto-timer, its buttons included, >= 4.5:1        (H5 B0124)
//   button   LAUNCH: every button painted with the page's --btn-bg token, text >= 4.5:1    (H5 B0123)
//   svg      every svg image or map (role img/group, or holding a focusable control) has an
//            accessible name: aria-label, a resolving aria-labelledby, or a <title>      (H5 B0127/B0128)
//   rank     a rank lesson (config kind 'rank') builds #rank-criterion, and it has a label  (H5 B0129)
//   reminder a "Previous lesson reminder" strip carries the prompt and no answer          (H2 B0002)
//   credit   every picture the page shows (img, svg image, poster, CSS background; data:
//            URIs included) has a row in the page's Sources_and_checks.html naming it by
//            file name, by md5 prefix, or by a data-visual attribute                      (D1 B0004/B0005)
//   arrival  from Week 2 on, no pupil-visible arrival text states the answer to an arrival
//            question (Week 1 word help is exempt: held by design under HUM-D5)    (LAND-A2 R3 a; B0002)
//   brand    every brandline names the lesson's own pathway and week, and every "Word help" line defines
//            one of the lesson's own arrival words -- never another week's             (LAND-A2 R3 b)
//
// Usage: node tools/hum/check_lesson_floor.cjs [--root DIR] [--out DIR] [--json]
// Exit 1 on any failure. Evidence, not proxies: contrast is computed from the rendered
// colours, a name must resolve to text, a credit must match the picture's own bytes.
'use strict';
const fs = require('fs'), path = require('path'), crypto = require('crypto'), cp = require('child_process');
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; };
const ROOT = path.resolve(arg('--root', '.'));
const OUT = arg('--out', '');
const MIN = 4.5;

function lessonPages() {
  let files;
  try {
    files = cp.execFileSync('git', ['-C', ROOT, 'ls-files', '-z', '--', 'Humanities_Teesside'], { encoding: 'utf8', maxBuffer: 1 << 28 }).split('\0');
  } catch (_) { files = []; }
  if (!files.filter(Boolean).length) {
    files = [];
    const walk = d => { for (const e of fs.readdirSync(path.join(ROOT, d), { withFileTypes: true })) {
      const r = path.join(d, e.name); if (e.isDirectory()) walk(r); else files.push(r); } };
    walk('Humanities_Teesside');
  }
  return files.filter(f => /_Lesson\.html$/.test(f) && !f.split('/').some(p => p.startsWith('_') || p.startsWith('.'))).sort();
}

const md5 = b => crypto.createHash('md5').update(b).digest('hex');
function sourcesFor(page) {
  // the page's own folder first, then each parent up to the pack root
  let d = path.dirname(path.join(ROOT, page));
  while (d.startsWith(path.join(ROOT, 'Humanities_Teesside'))) {
    const f = path.join(d, 'Sources_and_checks.html');
    if (fs.existsSync(f)) return f;
    d = path.dirname(d);
  }
  return null;
}
function rowsOf(file) {
  const t = fs.readFileSync(file, 'utf8');
  return [...t.matchAll(/<tr\b[^>]*>[\s\S]*?<\/tr>/gi)].map(m => m[0]);
}

(async () => {
  const { chromium } = require('playwright');
  const browser = await chromium.launch({ executablePath: process.env.MBM_CHROMIUM_PATH || undefined });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const pages = lessonPages();
  const results = [];
  for (const rel of pages) {
    const abs = path.join(ROOT, rel);
    const id = path.basename(rel).replace(/_Lesson\.html$/, '');
    const pathway = (id.match(/^(BUILD|GROW|LAUNCH)/) || [])[1] || '';
    const fails = [];
    await page.goto('file://' + abs);
    await page.waitForTimeout(80);
    // every slide laid out, so off-slide content is measured too; [hidden] stays hidden
    await page.addStyleTag({ content: 'section{display:block!important;visibility:visible!important;opacity:1!important}' });
    const m = await page.evaluate(({ pathway }) => {
      const rgba = c => { const v = (c.match(/[\d.]+/g) || []).map(Number); return { r: v[0], g: v[1], b: v[2], a: v.length > 3 ? v[3] : 1 }; };
      const lum = ({ r, g, b }) => { const f = x => { x /= 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
      const bgOf = el => { for (let e = el; e; e = e.parentElement) { const c = rgba(getComputedStyle(e).backgroundColor); if (c.a > 0.5) return c; } return { r: 255, g: 255, b: 255, a: 1 }; };
      const ratio = el => { const a = lum(rgba(getComputedStyle(el).color)), b = lum(bgOf(el)); return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05); };
      const owns = el => [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
      const texty = root => [root, ...root.querySelectorAll('*')].filter(e => owns(e) && getComputedStyle(e).display !== 'none' && !e.closest('[hidden]'));
      const tag = el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).join('.') : '');
      const out = { ribbon: [], timer: [], button: [], svg: [], rank: null, reminder: [], visuals: [], counts: {} };
      const ribbon = [...document.querySelectorAll('.step-ribbon > *')];
      out.counts.ribbon = ribbon.length;
      for (const r of ribbon) for (const e of texty(r)) { const v = ratio(e); if (v < 4.5) out.ribbon.push({ at: tag(e), text: e.textContent.trim().slice(0, 40), ratio: +v.toFixed(2) }); }
      const timer = document.getElementById('auto-timer');
      out.counts.timer = timer ? 1 : 0;
      if (timer && (pathway === 'BUILD' || pathway === 'GROW')) for (const e of texty(timer)) { const v = ratio(e); if (v < 4.5) out.timer.push({ at: tag(e), text: e.textContent.trim().slice(0, 30), ratio: +v.toFixed(2) }); }
      if (pathway === 'LAUNCH') {
        const probe = document.createElement('i'); probe.style.backgroundColor = 'var(--btn-bg)'; document.body.appendChild(probe);
        const token = getComputedStyle(probe).backgroundColor; probe.remove();
        const btns = [...document.querySelectorAll('button')].filter(b => getComputedStyle(b).backgroundColor === token && token !== 'rgba(0, 0, 0, 0)');
        out.counts.button = btns.length; out.counts.btnToken = token;
        for (const b of btns) { const v = ratio(b); if (v < 4.5) out.button.push({ at: tag(b), text: b.textContent.trim().slice(0, 30), ratio: +v.toFixed(2), token }); }
      }
      const hiddenFromAT = el => !!el.closest('[aria-hidden="true"]');
      const svgs = [...document.querySelectorAll('svg')].filter(s => !hiddenFromAT(s) && (/^(img|group)$/.test(s.getAttribute('role') || '') || s.querySelector('button,a[href],[tabindex]:not([tabindex="-1"]),input,select,textarea')));
      out.counts.svg = svgs.length;
      for (const s of svgs) {
        const label = (s.getAttribute('aria-label') || '').trim();
        const by = (s.getAttribute('aria-labelledby') || '').split(/\s+/).filter(Boolean).map(i => (document.getElementById(i) || {}).textContent || '').join(' ').trim();
        const title = [...s.children].find(c => c.tagName.toLowerCase() === 'title');
        if (!label && !by && !(title && title.textContent.trim())) out.svg.push({ at: tag(s), role: s.getAttribute('role') || '(none)', viewBox: s.getAttribute('viewBox') || '' });
      }
      const rank = document.getElementById('rank-criterion');
      if (rank) {
        const named = (rank.labels && [...rank.labels].some(l => l.textContent.trim())) || (rank.getAttribute('aria-label') || '').trim() ||
          (rank.getAttribute('aria-labelledby') || '').split(/\s+/).some(i => ((document.getElementById(i) || {}).textContent || '').trim());
        out.rank = { present: true, labelled: !!named };
      } else out.rank = { present: false, builds: ((window.CLASSIC_LESSON || {}).kind === 'rank') };
      for (const e of document.querySelectorAll('body *')) {
        if (e.children.length || e.closest('script,style,noscript,template')) continue;
        const t = e.textContent.replace(/\s+/g, ' ').trim();
        const i = t.search(/Previous lesson reminder/i);
        if (i < 0) continue;
        const rest = t.slice(i).replace(/^Previous lesson reminder\s*:?/i, '').trim();
        if (rest) out.reminder.push({ at: tag(e), text: t.slice(0, 160) });
      }
      const add = (kind, src, el) => { if (src) out.visuals.push({ kind, src, at: tag(el), hidden: !!el.closest('[hidden]') }); };
      for (const i of document.querySelectorAll('img')) add('img', i.getAttribute('src'), i);
      for (const s of document.querySelectorAll('picture source[srcset]')) add('source', s.getAttribute('srcset').split(',')[0].trim().split(/\s+/)[0], s);
      for (const v of document.querySelectorAll('video[poster]')) add('poster', v.getAttribute('poster'), v);
      for (const i of document.querySelectorAll('svg image')) add('svg-image', i.getAttribute('href') || i.getAttribute('xlink:href'), i);
      for (const e of document.querySelectorAll('body *')) { const b = getComputedStyle(e).backgroundImage; const u = b && b.match(/url\("?(.*?)"?\)/); if (u) add('css-bg', u[1], e); }
      return out;
    }, { pathway });

    // LAND-A2 R3 (a) and (b): the arrival strip and the brandlines, read from the rendered page
    const ar = await page.evaluate(() => {
      const cfg = window.CLASSIC_LESSON || {};
      const norm = s => (s || '').toLowerCase().replace(/[\u2018\u2019`]/g, "'").replace(/[^a-z0-9' ]+/g, ' ').replace(/\s+/g, ' ').trim();
      // a slide's own aria-hidden is the deck showing one slide at a time, not a hidden element: every slide is
      // laid out above, so only [hidden], staff-guide nodes, collapsed <details> and aria-hidden BELOW the slide count
      const shown = el => { const ah = el.closest('[aria-hidden="true"]');
        return !el.closest('[hidden],[data-mbm-guide],script,style,template,noscript,details:not([open])') && !(ah && ah.tagName !== 'SECTION') && getComputedStyle(el).display !== 'none'; };
      const out = { week: Number(cfg.week) || null, strip: [], answers: [], ownWords: [], brandlines: [], wordHelp: [] };
      const secs = [...document.querySelectorAll('section')].filter(s => /arrival/i.test((s.querySelector('.slide-tag') || {}).textContent || '') && /Arrival task/i.test(s.textContent));
      for (const s of secs) {
        for (const q of s.querySelectorAll('.question-card h3')) {
          const m = q.textContent.match(/Which meaning fits ([^?]+)\?|What does ([^?]+?) mean\?/i);
          if (m) out.ownWords.push(norm(m[1] || m[2]));
        }
        for (const a of s.querySelectorAll('[data-arrival-answer]')) if (norm(a.textContent).split(' ').length >= 2) out.answers.push(norm(a.textContent));
        for (const e of s.querySelectorAll('p, .brandline, li, span')) {
          if (e.closest('.question-card, [data-route-panel]') || !shown(e)) continue;
          if ([...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) out.strip.push(e.textContent.replace(/\s+/g, ' ').trim());
        }
      }
      for (const b of document.querySelectorAll('.brandline')) out.brandlines.push(b.textContent.replace(/\s+/g, ' ').trim());
      for (const e of document.querySelectorAll('body *')) {
        if (e.closest('script,style,template,noscript') || ![...e.childNodes].some(n => n.nodeType === 3 && /Word help/i.test(n.textContent))) continue;
        for (const m of e.textContent.matchAll(/Word help\s*(?:[:\u2014\u2013-])\s*(.+?)(?:\s+means\b|\s*:)/gi)) out.wordHelp.push({ term: norm(m[1]), text: e.textContent.replace(/\s+/g, ' ').trim().slice(0, 140), shown: shown(e) });
      }
      out.stripNorm = out.strip.map(norm);
      return out;
    });
    if (ar.week && ar.week >= 2) {
      for (const [i, s] of ar.stripNorm.entries()) {
        const hit = ar.answers.find(a => s.includes(a));
        if (hit) fails.push({ limb: 'arrival', detail: `Week ${ar.week}: pupil-visible arrival text "${ar.strip[i].slice(0, 110)}" states an arrival answer ("${hit}")` });
      }
    }
    if (ar.week) {
      for (const b of ar.brandlines) if (!new RegExp(`\\bWeek\\s*0?${ar.week}\\b`).test(b)) fails.push({ limb: 'brand', detail: `brandline "${b.slice(0, 110)}" does not name this lesson's week (${ar.week})` });
    }
    // LAND-A2 R5 §1: and its own pathway, by name
    if (pathway) {
      for (const b of ar.brandlines) if (!new RegExp(`\\b${pathway}\\b`).test(b)) fails.push({ limb: 'brand', detail: `brandline "${b.slice(0, 110)}" does not name this lesson's pathway (${pathway})` });
    }
    for (const w of ar.wordHelp) if (!ar.ownWords.includes(w.term)) fails.push({ limb: 'brand', detail: `word help for "${w.term}" is not one of this lesson's arrival words (${ar.ownWords.join(', ') || 'none'}): "${w.text}"` });

    const visuals = [];
    const src = sourcesFor(rel);
    const rows = src ? rowsOf(src) : [];
    const folder = path.dirname(abs);
    const folderByMd5 = {};
    for (const f of fs.readdirSync(folder)) if (/\.(png|jpe?g|gif|webp|svg)$/i.test(f)) folderByMd5[md5(fs.readFileSync(path.join(folder, f)))] = f;
    for (const v of m.visuals) {
      let bytes = null, name = null;
      if (/^data:/.test(v.src)) {
        const [head, body] = v.src.split(',', 2);
        bytes = /;base64/.test(head) ? Buffer.from(body, 'base64') : Buffer.from(decodeURIComponent(body));
      } else if (!/^(https?:)?\/\//.test(v.src)) {
        const f = path.resolve(folder, decodeURIComponent(v.src.split(/[?#]/)[0]));
        if (fs.existsSync(f)) { bytes = fs.readFileSync(f); name = path.basename(f); }
        else { fails.push({ limb: 'credit', detail: `${v.at} shows ${v.src}, which is not in the tree` }); continue; }
      } else { name = v.src; }
      const h = bytes ? md5(bytes) : '';
      name = name || folderByMd5[h] || null;
      const keys = [name, h && h.slice(0, 8)].filter(Boolean);
      const row = rows.find(r => keys.some(k => r.includes(k)) || (h && new RegExp(`data-visual(-md5)?="${h.slice(0, 8)}`).test(r)));
      visuals.push({ kind: v.kind, name, md5: h.slice(0, 8), row: !!row });
      if (!row) fails.push({ limb: 'credit', detail: `${v.at} shows ${name || 'an embedded picture'} (md5 ${h.slice(0, 8)}) with no row in ${src ? path.relative(ROOT, src) : 'any Sources_and_checks.html'}` });
    }
    for (const x of m.ribbon) fails.push({ limb: 'ribbon', detail: `${x.at} "${x.text}" ${x.ratio}:1` });
    for (const x of m.timer) fails.push({ limb: 'timer', detail: `${x.at} "${x.text}" ${x.ratio}:1` });
    for (const x of m.button) fails.push({ limb: 'button', detail: `${x.at} "${x.text}" ${x.ratio}:1 on ${x.token}` });
    for (const x of m.svg) fails.push({ limb: 'svg', detail: `${x.at} role=${x.role} viewBox="${x.viewBox}" has no accessible name` });
    if (m.rank && m.rank.present && !m.rank.labelled) fails.push({ limb: 'rank', detail: '#rank-criterion has no label' });
    if (m.rank && !m.rank.present && m.rank.builds) fails.push({ limb: 'rank', detail: 'the lesson is a rank activity but #rank-criterion was never built' });
    for (const x of m.reminder) fails.push({ limb: 'reminder', detail: `${x.at} "${x.text}"` });
    results.push({ page: rel, pathway, counts: m.counts, rank: m.rank, visuals, sources: src ? path.relative(ROOT, src) : null, fails });
  }
  await browser.close();

  // Known red on main today (tools/hum/lesson_floor_known_red.json): each listed page must STILL fail every limb it
  // lists (a fixed page goes red until its entry is removed), and it may fail no limb that is not listed.
  const knownPath = path.join(__dirname, 'lesson_floor_known_red.json');
  const known = fs.existsSync(knownPath) && !process.argv.includes('--no-known-red') ? JSON.parse(fs.readFileSync(knownPath, 'utf8')).entries : [];
  const knownFor = Object.fromEntries(known.map(e => [e.page, new Set(e.limbs)]));
  // RULING LAND-A2 R5 §4 (Claude, 25 September 2026): exactly these 19 paths, each with the limbs it failed that day,
  // taken on Lessons main 55eb2bd1. The list only shrinks: an entry leaves when its pack is rebuilt, and a path or a
  // limb that is not in this dated baseline fails here however the JSON is edited.
  const KNOWN_RED_BASELINE = {
    "Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W01/BUILD_SU1_W01_Lesson.html": ["ribbon", "timer"],
    "Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W02/BUILD_SU1_W02_Lesson.html": ["ribbon", "timer"],
    "Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W03/BUILD_SU1_W03_Lesson.html": ["ribbon", "timer"],
    "Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W04/BUILD_SU1_W04_Lesson.html": ["ribbon", "timer"],
    "Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/BUILD_SU1_W05_Lesson.html": ["arrival", "ribbon", "timer"],
    "Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W06/BUILD_SU1_W06_Lesson.html": ["ribbon", "timer"],
    "Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W01/GROW_SU1_W01_Lesson.html": ["ribbon", "svg", "timer"],
    "Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W02/GROW_SU1_W02_Lesson.html": ["ribbon", "svg", "timer"],
    "Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Lesson.html": ["ribbon", "svg", "timer"],
    "Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W04/GROW_SU1_W04_Lesson.html": ["ribbon", "svg", "timer"],
    "Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W05/GROW_SU1_W05_Lesson.html": ["ribbon", "svg", "timer"],
    "Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W06/GROW_SU1_W06_Lesson.html": ["ribbon", "svg", "timer"],
    "Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/LAUNCH_SU1_W01_Lesson.html": ["button", "ribbon"],
    "Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/LAUNCH_SU1_W02_Lesson.html": ["button", "ribbon"],
    "Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/LAUNCH_SU1_W03_Lesson.html": ["button", "ribbon"],
    "Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/LAUNCH_SU1_W04_Lesson.html": ["button", "ribbon"],
    "Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/LAUNCH_SU1_W05_Lesson.html": ["button", "ribbon"],
    "Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/LAUNCH_SU1_W06_Lesson.html": ["button", "ribbon"],
    "Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W04/BUILD_A1_W04_Lesson.html": ["credit"]
  };
  const listGrew = [];
  for (const e of known) {
    const allowed = KNOWN_RED_BASELINE[e.page];
    if (!allowed) listGrew.push(`"${e.page}" is not on the dated list of 19 (R5 §4): the list only shrinks`);
    else for (const limb of e.limbs) if (!allowed.includes(limb)) listGrew.push(`"${e.page}" lists limb "${limb}", which it did not fail on 25 September 2026: the list only shrinks`);
    if (!e.reason) listGrew.push(`"${e.page}" has no reason`);
  }
  const measuredPages = new Set(results.map(r => r.page));
  for (const r of results) {
    const listed = knownFor[r.page];
    if (!listed) continue;
    const failing = new Set(r.fails.map(f => f.limb));
    r.known = r.fails.filter(f => listed.has(f.limb));
    r.fails = r.fails.filter(f => !listed.has(f.limb));
    for (const limb of listed) if (!failing.has(limb)) r.fails.push({ limb: 'known-red', detail: `listed as known red on "${limb}", but it now passes: remove it from lesson_floor_known_red.json` });
  }
  const knownCount = results.reduce((s, r) => s + (r.known ? r.known.length : 0), 0);
  const failed = results.filter(r => r.fails.length);
  const byLimb = {};
  for (const r of failed) for (const f of r.fails) byLimb[f.limb] = (byLimb[f.limb] || 0) + 1;
  const measured = {
    pages: results.length,
    ribbonItems: results.reduce((s, r) => s + (r.counts.ribbon || 0), 0),
    timers: results.filter(r => r.counts.timer && /BUILD|GROW/.test(r.pathway)).length,
    launchButtons: results.reduce((s, r) => s + (r.counts.button || 0), 0),
    svgs: results.reduce((s, r) => s + (r.counts.svg || 0), 0),
    rankSelects: results.filter(r => r.rank && r.rank.present).length,
    visuals: results.reduce((s, r) => s + r.visuals.length, 0),
  };
  const report = { root: ROOT, measured, failedPages: failed.length, failuresByLimb: byLimb, results };
  if (OUT) { fs.mkdirSync(OUT, { recursive: true }); fs.writeFileSync(path.join(OUT, 'lesson-floor.json'), JSON.stringify(report, null, 1)); }
  console.log(`Humanities and RE lesson floor: ${results.length} lesson pages measured`);
  console.log(`  measured: ${JSON.stringify(measured)}`);
  if (known.length) console.log(`  known red on main, named in lesson_floor_known_red.json: ${known.filter(e => measuredPages.has(e.page)).length} page(s), ${knownCount} failure(s) held; each must still fail`);
  if (process.argv.includes('--json')) console.log(JSON.stringify(report, null, 1));
  for (const g of listGrew) console.log(`FAIL [known-red list] ${g}`);
  if (!failed.length && !listGrew.length) { console.log('PASS: every limb holds on every page'); return; }
  if (!failed.length) { process.exitCode = 1; return; }
  console.log(`FAIL: ${failed.length} page(s); failures by limb ${JSON.stringify(byLimb)}`);
  for (const r of failed) { console.log(`  ${r.page}`); for (const f of r.fails.slice(0, 6)) console.log(`    [${f.limb}] ${f.detail}`); if (r.fails.length > 6) console.log(`    ... ${r.fails.length - 6} more`); }
  process.exitCode = 1;
})().catch(e => { console.error(e); process.exit(2); });
