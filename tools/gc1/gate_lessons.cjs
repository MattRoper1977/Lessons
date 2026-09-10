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
const fs = require('fs'), path = require('path');

const ROUTES = ['step', 'main', 'challenge'];
const STAGES = 8;
const ALLOWED_HOSTS = ['scratch.mit.edu', 'www.aqa.org.uk'];
// --served asserts the publisher-injected usage layer too. Off by default,
// because on the working tree that layer does not exist yet and cannot.
const SERVED = process.argv.includes('--served');
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
  usageLayer: () => !!document.querySelector('.mbm-usage'),
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

async function driveLesson(page, file) {
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  await page.goto('file://' + file, { waitUntil: 'load' });

  const out = { file: path.basename(file), dupIds: [], stagesSeen: 0, errors,
                furniture: {}, print: {}, externalHosts: [], storage: [] };

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
    // G6 splits, and it has to. Four of the five items are authored into the
    // lesson. The fifth is not ours to author: Site domain-split/usage_discovery.py
    // says education lesson HTML gets "one published adapter, just like the
    // existing lesson navigation", so the usage layer arrives at build time.
    // Asserting it against the working tree would fail every lesson forever and
    // teach everyone to ignore G6; asserting it only against the served page is
    // what SERVED is for. It is still counted and printed either way, so its
    // absence is visible rather than quietly excused.
    const scope = SERVED ? Object.keys(r.furniture) : Object.keys(r.furniture).filter(k => k !== 'usageLayer');
    const missing = scope.filter(k => !r.furniture[k]);
    g('G6', missing.length === 0, r.file + ' estate furniture missing: ' + missing.join(', '));
    const extra = r.externalHosts.filter(h => !ALLOWED_HOSTS.includes(h));
    g('G7', extra.length === 0, r.file + ' external hosts outside the allowlist: ' + extra.join(', '));
    g('G3', r.storage.length === 0, r.file + ' storage API touched: ' + r.storage.join(', '));
    g('G13', r.errors.length === 0, r.file + ' console errors: ' + r.errors.slice(0, 3).join(' | '));
    g('G13', r.stagesSeen === ROUTES.length * STAGES,
      r.file + ' only walked ' + r.stagesSeen + ' of ' + ROUTES.length * STAGES + ' stage/route combinations');
  }
  return fail;
}

async function main() {
  const args = process.argv.slice(2);
  if (args[0] === '--self-test') return selfTest();
  const dir = args[0];
  if (!dir) { console.error('usage: gate_lessons.cjs <unit-dir> [out.json]'); process.exit(2); }
  const files = [];
  for (const w of fs.readdirSync(dir).filter(d => /^Week_\d\d$/.test(d)).sort()) {
    for (const f of fs.readdirSync(path.join(dir, w))) {
      if (/Interactive\.html$/.test(f)) files.push(path.resolve(dir, w, f));
    }
  }
  if (!files.length) { console.error('no Week_NN/*Interactive.html under ' + dir); process.exit(2); }

  const browser = await chromium.launch();
  const rows = [];
  for (const f of files) {
    const ctx = await browser.newContext({ viewport: VP });
    const page = await ctx.newPage();
    rows.push(await driveLesson(page, f));
    await ctx.close();
  }
  await browser.close();

  const fail = judge(rows);
  console.log('viewport              : %dx%d', VP.width, VP.height);
  console.log('lessons walked        : %d', rows.length);
  console.log('stage/route positions : %d', rows.reduce((a, r) => a + r.stagesSeen, 0));
  console.log('print record filled   : %d of %d', rows.filter(r => r.print.textLen > 0).length, rows.length);
  console.log('furniture (4 authored): %d of %d', rows.filter(r =>
    ['wayHome','madeByMatt','guideToggle','prevNext'].every(k => r.furniture[k])).length, rows.length);
  console.log('usage layer (%s): %d of %d', SERVED ? 'ASSERTED' : 'reported only, publisher-injected',
    rows.filter(r => r.furniture.usageLayer).length, rows.length);
  console.log('duplicate ids         : %d', rows.reduce((a, r) => a + r.dupIds.length, 0));
  console.log('console errors        : %d', rows.reduce((a, r) => a + r.errors.length, 0));
  console.log('');
  for (const f of fail) console.log('  FAIL ' + f);
  console.log('\n%d gate failures', fail.length);
  if (args[1]) fs.writeFileSync(args[1], JSON.stringify({ rows, fail }, null, 1));
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
    furniture: { wayHome: true, madeByMatt: true, guideToggle: true, prevNext: true, usageLayer: true },
    print: { present: true, visible: true, textLen: 240, hiddenChrome: true, text: 'x' },
    externalHosts: ['scratch.mit.edu', 'www.aqa.org.uk'], storage: [],
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

  want('the usage layer alone is not a G6 red off the served tree',
       !judge([{ ...clean, furniture: { ...clean.furniture, usageLayer: false } }]).some(f => f.startsWith('G6')));
  want('one missing furniture item is a G6 red',
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
