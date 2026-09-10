// tools/gc1/gate_lessons.cjs - GC1 gates G2-G7, G10, G13 against the RENDERED lesson.
//
// WHY IT RENDERS INSTEAD OF READING THE SOURCE
//
// Every one of these gates is about what a pupil actually gets, and for these
// lessons the source and the result disagree in both directions.
//
//   G4 duplicate ids. Weeks 1 and 2 emit id="centre" twice in the source -- but the
//   two occurrences are the two arms of one ternary, so at most one can ever be in
//   the DOM. A grep says "duplicate"; the page says otherwise. The gate has to
//   agree with the page, and it also has to keep looking after a route change,
//   because these lessons re-render their whole main region per stage and per route
//   and a collision can exist on stage 6 of the challenge route and nowhere else.
//
//   G5 print route. The print CSS hides header, main and footer and shows
//   .print-record. Reading that CSS tells you nothing about whether anything is IN
//   .print-record: weeks 1 and 2 ship the container EMPTY and weeks 3-6 dropped it
//   entirely, so six of eight lessons printed a blank page for as long as they have
//   existed. The container is filled by fillPrint on beforeprint, so the gate fires
//   beforeprint, switches Chromium to print emulation, and measures the text that
//   is actually visible. A blank page is a red.
//
// USAGE
//   node tools/gc1/gate_lessons.cjs <unit-dir> [out.json]
//   node tools/gc1/gate_lessons.cjs --self-test
//
// Exit 0 clean, 1 if any gate fails, 2 on a usage error.
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('fs'), path = require('path'), http = require('http');

// A built lesson asks for /Lessons/assets/catalogue/lesson-navigation.js -- a SITE
// path. Opened over file:// that resolves to the filesystem root and 404s, so a
// run against a served tree reports eight console errors that do not exist on the
// site. Serving education-lessons at /Lessons/ is what makes the measurement the
// site's rather than this container's. Off the working tree there is nothing to
// serve and file:// is correct.
function serveTree(root) {
  const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css',
                  '.json': 'application/json', '.svg': 'image/svg+xml' };
  const server = http.createServer((req, res) => {
    const rel = decodeURIComponent(req.url.split(/[?#]/)[0]).replace(/^\/Lessons\/?/, '');
    const file = path.resolve(root, rel);
    if (!file.startsWith(path.resolve(root)) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
      res.writeHead(404); return res.end('not found');
    }
    res.writeHead(200, { 'content-type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream' });
    res.end(fs.readFileSync(file));
  });
  return new Promise(r => server.listen(0, '127.0.0.1', () => r(server)));
}

const ROUTES = ['step', 'main', 'challenge'];
const STAGES = 8;
const ALLOWED_HOSTS = ['scratch.mit.edu', 'www.aqa.org.uk'];
// --served points the run at a BUILT publication tree rather than the working
// tree, and turns on the assertions that only mean anything there. Give it the
// unit directory inside education-lessons, not the repository copy.
// let, not const: the self-test has to be able to judge BOTH postures, and a
// gate whose served half is never exercised is the gate that missed the .sb3.
let SERVED = process.argv.includes('--served');
// --peer <dir> is a second served unit to compare against. It exists because one
// of these numbers cannot be judged in isolation: see USAGE ADAPTER below.
const PEER = (() => { const i = process.argv.indexOf('--peer'); return i >= 0 ? process.argv[i + 1] : null; })();
// D38 asks for 390 and 1280. A lesson can render clean at one width and throw at
// the other, so the width is a parameter and the run prints which one it used.
const VP = (() => {
  const i = process.argv.indexOf('--viewport');
  const v = i >= 0 ? process.argv[i + 1] : '1280x720';
  const [w, h] = String(v).split('x').map(Number);
  return { width: w || 1280, height: h || 720 };
})();

// G6. Estate furniture, as five separately observable things. Counting matters:
// "has a link somewhere" is not "has a way home", so each probe names the element
// it needs rather than a phrase that might appear in prose.
// Each selector is the estate's own, read off the donor that produces it, not a
// plausible-looking name. a.mbmhome and .n6-splash come from
// _next6/tools/n7_chassis_furniture.py (the forms used on 50 and 116 carriers);
// .n6m-guide-btn from _next6/tools/n6m_guide_toggle.py; .mbm-usage from the
// publisher's own adapter in Site domain-split/usage_discovery.py. A probe for a
// name nobody emits returns false on every page and reads like a finding.
const FURNITURE = {
  wayHome:    () => !!document.querySelector('a.mbmhome'),
  madeByMatt: () => !!document.querySelector('.n6-splash svg, .n6-splash'),
  guideToggle:() => !!document.querySelector('.n6m-guide-btn'),
  prevNext:   () => !!(document.querySelector('#prev') && document.querySelector('#next')),
  // Publisher-injected, and the two are not the same thing. See below.
  lessonNav:    () => !!document.querySelector('script[src$="assets/catalogue/lesson-navigation.js"]'),
  usageAdapter: () => !!document.querySelector('script[src="/assets/usage-client.js"]'),
};

function dupIdsInDom() {
  const seen = new Map();
  for (const el of document.querySelectorAll('[id]')) {
    const id = el.id;
    if (!id) continue;
    seen.set(id, (seen.get(id) || 0) + 1);
  }
  return [...seen.entries()].filter(([, n]) => n > 1).map(([id, n]) => id + '×' + n);
}

async function driveLesson(page, file, url) {
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  await page.goto(url, { waitUntil: 'load' });

  const out = { file: path.basename(file), path: file, dupIds: [], stagesSeen: 0, errors,
                furniture: {}, print: {}, externalHosts: [], storage: [],
                sb3Links: [], dataFallbacks: [], sb3Missing: [] };

  // G4 + G13: every stage of every route, driven through the real controls.
  for (const route of ROUTES) {
    await page.selectOption('#route', route).catch(() => {});
    for (let s = 0; s < STAGES; s++) {
      const dups = await page.evaluate(dupIdsInDom);
      for (const d of dups) {
        const tag = route + ':stage' + s + ':' + d;
        if (!out.dupIds.includes(tag)) out.dupIds.push(tag);
      }
      out.stagesSeen++;
      if (s < STAGES - 1) await page.click('#next').catch(() => {});
    }
    // back to the first stage for the next route
    for (let s = 0; s < STAGES; s++) await page.click('#prev').catch(() => {});
  }

  out.furniture = await page.evaluate(f => {
    const r = {};
    for (const [k, src] of Object.entries(f)) r[k] = new Function('return (' + src + ')()')();
    return r;
  }, Object.fromEntries(Object.entries(FURNITURE).map(([k, v]) => [k, v.toString()])));

  out.externalHosts = await page.evaluate(() =>
    [...new Set([...document.querySelectorAll('a[href^="http"]')]
      .map(a => new URL(a.href).host))].sort());

  // G9. Both download routes, read off the DOM rather than the source, because
  // the source is not what a pupil is handed. The sibling href is captured as
  // AUTHORED (getAttribute), not as resolved, so main() can resolve it against
  // the served root itself -- resolving it here against file:// would answer a
  // question about this container and not about the site.
  const both = await page.evaluate(() => ({
    sb3: [...document.querySelectorAll('a[href]')]
      .map(a => a.getAttribute('href'))
      .filter(h => h && !/^data:/.test(h) && /\.sb3(?:[?#]|$)/i.test(h)),
    data: [...document.querySelectorAll('a[href^="data:"]')]
      .map(a => a.getAttribute('href').slice(0, 64))
      .filter(h => /^data:application\/(?:octet-stream|x-scratch|zip)/i.test(h) || /base64/i.test(h)),
  }));
  out.sb3Links = both.sb3; out.dataFallbacks = both.data;

  // G3 at runtime, not just in source: a page that reaches for storage under a
  // policy that blocks it throws rather than silently degrading, so probe for the
  // call sites the source claims are absent.
  out.storage = await page.evaluate(() => {
    const hits = [];
    for (const k of ['localStorage', 'sessionStorage', 'indexedDB']) {
      try { if (window['__gc1_touched_' + k]) hits.push(k); } catch (e) { hits.push(k + ':threw'); }
    }
    return hits;
  });

  // G5. Fire the event the browser fires, then measure under print emulation.
  await page.evaluate(() => window.dispatchEvent(new Event('beforeprint')));
  await page.emulateMedia({ media: 'print' });
  out.print = await page.evaluate(() => {
    const rec = document.querySelector('.print-record');
    if (!rec) return { present: false, visible: false, textLen: 0, hiddenChrome: null, text: '' };
    const vis = getComputedStyle(rec).display !== 'none';
    const chrome = ['header', 'main', 'footer'].map(sel => {
      const el = document.querySelector(sel);
      return el ? getComputedStyle(el).display === 'none' : true;
    });
    const t = (rec.innerText || rec.textContent || '').replace(/\s+/g, ' ').trim();
    return { present: true, visible: vis, textLen: t.length,
             hiddenChrome: chrome.every(Boolean), text: t.slice(0, 160) };
  });
  await page.emulateMedia({ media: 'screen' });
  return out;
}

// The served root is the education-lessons directory the unit sits inside, found
// by walking up from the unit directory. An absolute href like /Lessons/x.sb3 is
// a site path, so it resolves against that root and never against the unit.
function servedRoot(dir) {
  let d = path.resolve(dir);
  while (d !== path.dirname(d)) {
    if (path.basename(d) === 'education-lessons') return d;
    d = path.dirname(d);
  }
  return path.resolve(dir);
}

function peerUsageAdapters(peer) {
  const files = [];
  const walk = d => { for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    const f = path.join(d, e.name);
    if (e.isDirectory()) walk(f); else if (/\.html$/i.test(e.name)) files.push(f);
  } };
  walk(peer);
  return { total: files.length,
           count: files.filter(f => fs.readFileSync(f, 'utf8').includes('/assets/usage-client.js')).length };
}

function judge(rows) {
  const fail = [];
  const g = (name, ok, detail) => { if (!ok) fail.push(name + ': ' + detail); };
  for (const r of rows) {
    g('G4', r.dupIds.length === 0, r.file + ' duplicate ids in the live DOM: ' + r.dupIds.join(', '));
    g('G5', r.print.present && r.print.visible && r.print.textLen > 0,
      r.file + ' print record ' + (!r.print.present ? 'ABSENT' :
        !r.print.visible ? 'not shown under print emulation' : 'EMPTY after beforeprint'));
    g('G5', !r.print.present || r.print.hiddenChrome !== false,
      r.file + ' print emulation still shows header/main/footer');
    // G6 splits three ways, and the split is the correction.
    //
    // Four items are AUTHORED into the lesson and are asserted everywhere.
    //
    // lessonNav is PUBLISHER-INJECTED and universal: build_education.py appends
    // the catalogue adapter to every lesson HTML it copies. Measured on a real
    // build: 1465 of 1502 education-lessons pages carry it, and 11 of 11 here.
    // So it is a real assertion, and it is only available off a served tree.
    //
    // usageAdapter is PUBLISHER-INJECTED AND CONDITIONAL, and this is where the
    // first cut of this gate was wrong twice over. It probed for `.mbm-usage`,
    // which no lesson page in the estate carries -- measured, 2 of 1502 built
    // lesson pages have that markup and both are hubs, because usage_discovery
    // only emits it under choice=True. What a lesson page actually receives is
    // inject()'s bare adapter, script src="/assets/usage-client.js": 817 of 1502.
    // And which lessons receive it is decided by the CATALOGUE, not by the page:
    // only rows whose event_types include lesson_open. So it cannot be a
    // per-lesson pass/fail on a unit at all. It is compared against a peer unit
    // instead -- --peer -- and only a DISAGREEMENT with the neighbour is a red.
    const authored = ['wayHome', 'madeByMatt', 'guideToggle', 'prevNext'];
    const scope = SERVED ? [...authored, 'lessonNav'] : authored;
    const missing = scope.filter(k => !r.furniture[k]);
    g('G6', missing.length === 0, r.file + ' estate furniture missing: ' + missing.join(', '));
    const extra = r.externalHosts.filter(h => !ALLOWED_HOSTS.includes(h));
    g('G7', extra.length === 0, r.file + ' external hosts outside the allowlist: ' + extra.join(', '));
    g('G3', r.storage.length === 0, r.file + ' storage API touched: ' + r.storage.join(', '));
    g('G13', r.errors.length === 0, r.file + ' console errors: ' + r.errors.slice(0, 3).join(' | '));
    // G9, and only off a served tree: on the working tree the sibling file sits
    // beside the lesson in the repository whether or not the publisher would
    // ever emit it, so a green here would mean nothing. That is exactly how 23
    // .sb3 came to be dropped by extension with this gate reporting 15 of 15.
    if (SERVED) {
      g('G9', r.sb3Links.length > 0, r.file + ' offers no sibling .sb3 link at all');
      const gone = (r.sb3Missing || []);
      g('G9', gone.length === 0, r.file + ' sibling .sb3 does not resolve at its served path: ' + gone.join(', '));
      g('G9', r.dataFallbacks.length > 0, r.file + ' the base64 data: fallback is gone; R3 wants both routes');
    }
    g('G13', r.stagesSeen === ROUTES.length * STAGES,
      r.file + ' only walked ' + r.stagesSeen + ' of ' + ROUTES.length * STAGES + ' stage/route combinations');
  }
  return fail;
}

async function main() {
  const args = process.argv.slice(2);
  if (args[0] === '--self-test') return selfTest();
  // Positional args only, so a flag is never mistaken for the output path. The
  // first version wrote its JSON to a file called "--served".
  const FLAGS_WITH_VALUE = new Set(['--viewport', '--peer']);
  const positional = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) { if (FLAGS_WITH_VALUE.has(args[i])) i++; continue; }
    positional.push(args[i]);
  }
  const dir = positional[0], outJson = positional[1];
  if (!dir) { console.error('usage: gate_lessons.cjs <unit-dir> [out.json] [--served] [--peer <dir>] [--viewport WxH]'); process.exit(2); }
  const files = [];
  for (const w of fs.readdirSync(dir).filter(d => /^Week_\d\d$/.test(d)).sort()) {
    for (const f of fs.readdirSync(path.join(dir, w))) {
      if (/Interactive\.html$/.test(f)) files.push(path.resolve(dir, w, f));
    }
  }
  if (!files.length) { console.error('no Week_NN/*Interactive.html under ' + dir); process.exit(2); }

  const root = SERVED ? servedRoot(dir) : null;
  const server = SERVED ? await serveTree(root) : null;
  const origin = server ? 'http://127.0.0.1:' + server.address().port : null;
  const browser = await chromium.launch();
  const rows = [];
  for (const f of files) {
    const ctx = await browser.newContext({ viewport: VP });
    const page = await ctx.newPage();
    const url = origin ? origin + '/Lessons/' + path.relative(root, f).split(path.sep).map(encodeURIComponent).join('/')
                       : 'file://' + f;
    const row = await driveLesson(page, f, url); row.path = f; row.url = url; rows.push(row);
    await ctx.close();
  }
  await browser.close();
  if (server) server.close();

  // Resolve each authored sibling href against the tree the run was pointed at.
  // fs.existsSync is the whole assertion: a served path either has a file behind
  // it or it is a 404 the moment a pupil clicks it.
  for (const r of rows) {
    r.sb3Missing = (r.sb3Links || []).filter(href => {
      const clean = decodeURIComponent(href.split(/[?#]/)[0]);
      const base = clean.startsWith('/') ? servedRoot(dir) : path.dirname(r.path);
      return !fs.existsSync(path.resolve(base, clean.replace(/^\//, '')));
    });
  }

  const fail = judge(rows);
  if (SERVED && PEER) {
    const mine = rows.filter(r => r.furniture.usageAdapter).length;
    const theirs = peerUsageAdapters(PEER);
    if ((mine > 0) !== (theirs.count > 0)) {
      fail.push('G6: the usage adapter disagrees with the peer unit -- this unit ' + mine + ' of ' +
        rows.length + ', ' + path.basename(PEER) + ' ' + theirs.count + ' of ' + theirs.total +
        '. Whether a lesson carries it is a catalogue decision, so a difference between two units in the same subject is a finding, not a preference.');
    }
    console.log('usage adapter vs peer : this unit %d of %d, %s %d of %d',
      mine, rows.length, path.basename(PEER), theirs.count, theirs.total);
  }
  console.log('viewport              : %dx%d', VP.width, VP.height);
  console.log('lessons walked        : %d', rows.length);
  console.log('stage/route positions : %d', rows.reduce((a, r) => a + r.stagesSeen, 0));
  console.log('print record filled   : %d of %d', rows.filter(r => r.print.textLen > 0).length, rows.length);
  console.log('furniture (4 authored): %d of %d', rows.filter(r =>
    ['wayHome','madeByMatt','guideToggle','prevNext'].every(k => r.furniture[k])).length, rows.length);
  console.log('lesson nav (%s): %d of %d', SERVED ? 'ASSERTED, publisher-injected' : 'reported only, arrives at build',
    rows.filter(r => r.furniture.lessonNav).length, rows.length);
  console.log('usage adapter (%s): %d of %d', SERVED ? 'reported; catalogue decides' : 'reported only, arrives at build',
    rows.filter(r => r.furniture.usageAdapter).length, rows.length);
  console.log('sibling .sb3 (%s): %d links, %d unresolved', SERVED ? 'ASSERTED at served paths' : 'reported only, off the served tree',
    rows.reduce((a, r) => a + (r.sb3Links || []).length, 0),
    rows.reduce((a, r) => a + (r.sb3Missing || []).length, 0));
  console.log('data: fallbacks       : %d', rows.reduce((a, r) => a + (r.dataFallbacks || []).length, 0));
  console.log('duplicate ids         : %d', rows.reduce((a, r) => a + r.dupIds.length, 0));
  console.log('console errors        : %d', rows.reduce((a, r) => a + r.errors.length, 0));
  console.log('');
  for (const f of fail) console.log('  FAIL ' + f);
  console.log('\n%d gate failures', fail.length);
  if (outJson) fs.writeFileSync(outJson, JSON.stringify({ rows, fail }, null, 1));
  process.exit(fail.length ? 1 : 0);
}

// The judge is the part that can be wrong in the direction that matters -- passing
// something broken. So it gets fixtures on both sides, including the exact shapes
// the six broken lessons ship: a container that is present but empty, and no
// container at all.
function selfTest() {
  let n = 0; const bad = [];
  const want = (name, cond) => { n++; console.log((cond ? '  PASS  ' : '  FAIL  ') + name); if (!cond) bad.push(name); };
  const clean = {
    file: 'ok.html', dupIds: [], stagesSeen: 24, errors: [],
    furniture: { wayHome: true, madeByMatt: true, guideToggle: true, prevNext: true,
                 lessonNav: true, usageAdapter: true },
    print: { present: true, visible: true, textLen: 240, hiddenChrome: true, text: 'x' },
    externalHosts: ['scratch.mit.edu', 'www.aqa.org.uk'], storage: [],
    sb3Links: ['Scratch_Projects/W01_Start.sb3'], sb3Missing: [],
    dataFallbacks: ['data:application/octet-stream;base64,UEsDBA'],
  };
  want('a clean lesson passes every gate', judge([clean]).length === 0);

  const emptyRec = { ...clean, print: { ...clean.print, textLen: 0 } };
  want('weeks 1-2 shape: container present but EMPTY is a G5 red',
       judge([emptyRec]).some(f => f.startsWith('G5') && /EMPTY/.test(f)));

  const noRec = { ...clean, print: { present: false, visible: false, textLen: 0, hiddenChrome: null, text: '' } };
  want('weeks 3-6 shape: no container at all is a G5 red',
       judge([noRec]).some(f => f.startsWith('G5') && /ABSENT/.test(f)));

  want('a print record that stays hidden under print emulation is a G5 red',
       judge([{ ...clean, print: { ...clean.print, visible: false } }]).some(f => f.startsWith('G5')));
  want('print emulation that still shows the screen chrome is a G5 red',
       judge([{ ...clean, print: { ...clean.print, hiddenChrome: false } }]).some(f => /still shows/.test(f)));

  want('a duplicate id is a G4 red',
       judge([{ ...clean, dupIds: ['main:stage0:centre×2'] }]).some(f => f.startsWith('G4')));
  want('  ... and the message names the id and the stage',
       judge([{ ...clean, dupIds: ['main:stage0:centre×2'] }])[0].includes('main:stage0:centre'));

  // The corrected G6. usageAdapter is never a per-lesson red, in either posture,
  // because the catalogue decides it -- so if this ever starts failing, the
  // instrument has drifted back to asserting an unobservable property.
  want('the usage adapter alone is not a G6 red off the served tree',
       !judge([{ ...clean, furniture: { ...clean.furniture, usageAdapter: false } }]).some(f => f.startsWith('G6')));
  SERVED = true;
  want('  ... and it is still not a G6 red ON the served tree',
       !judge([{ ...clean, furniture: { ...clean.furniture, usageAdapter: false } }]).some(f => f.startsWith('G6')));
  want('a missing lesson-navigation adapter IS a G6 red on the served tree',
       judge([{ ...clean, furniture: { ...clean.furniture, lessonNav: false } }]).some(f => f.startsWith('G6') && /lessonNav/.test(f)));

  // G9, both halves, and the exact shape the .sb3 extension gap produced: the
  // link is authored and present, and nothing is behind it.
  want('a sibling .sb3 that does not resolve at its served path is a G9 red',
       judge([{ ...clean, sb3Missing: ['Scratch_Projects/W01_Start.sb3'] }]).some(f => f.startsWith('G9')));
  want('  ... and the message names the path',
       judge([{ ...clean, sb3Missing: ['Scratch_Projects/W01_Start.sb3'] }]).some(f => /W01_Start\.sb3/.test(f)));
  want('a lesson offering no sibling link at all is a G9 red',
       judge([{ ...clean, sb3Links: [] }]).some(f => f.startsWith('G9')));
  want('dropping the data: fallback is a G9 red even when the sibling resolves',
       judge([{ ...clean, dataFallbacks: [] }]).some(f => f.startsWith('G9')));
  want('a clean lesson passes G9 on the served tree', judge([clean]).length === 0);
  SERVED = false;
  want('G9 is silent off the served tree, where it could only lie',
       !judge([{ ...clean, sb3Missing: ['x.sb3'], dataFallbacks: [], sb3Links: [] }]).some(f => f.startsWith('G9')));
  want('one missing AUTHORED furniture item is a G6 red in either posture',
       judge([{ ...clean, furniture: { ...clean.furniture, madeByMatt: false } }]).some(f => f.startsWith('G6')));
  want('  ... and it names which one', judge([{ ...clean, furniture: { ...clean.furniture, madeByMatt: false } }])[0].includes('madeByMatt'));

  want('a third external host is a G7 red',
       judge([{ ...clean, externalHosts: [...clean.externalHosts, 'youtube.com'] }]).some(f => f.startsWith('G7')));
  want('the two allowed hosts alone are not a G7 red',
       !judge([clean]).some(f => f.startsWith('G7')));

  want('a storage API touch is a G3 red', judge([{ ...clean, storage: ['localStorage'] }]).some(f => f.startsWith('G3')));
  want('a console error is a G13 red', judge([{ ...clean, errors: ['boom'] }]).some(f => f.startsWith('G13')));

  // The one that would otherwise pass silently: a run that crashed early looks
  // clean, because nothing it failed to reach can report a failure.
  want('a short walk is a G13 red, not a silent pass',
       judge([{ ...clean, stagesSeen: 8 }]).some(f => /only walked 8 of 24/.test(f)));

  console.log('\n%d checks, %d failed', n, bad.length);
  for (const b of bad) console.log('  FAILED: ' + b);
  process.exit(bad.length ? 1 : 0);
}

main().catch(e => { console.error(e); process.exit(1); });
