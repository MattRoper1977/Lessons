/* Virtual Chemistry Lab — matched-pair controls.
 *
 * Every assertion runs against BOTH trees: it must FAIL on release/ and PASS on
 * staging/. A control that passes on both is decoration.
 *
 * Everything here drives the page through its OWN DOM and real events. The
 * page's `state` is a script-level lexical binding and is not reachable from an
 * injected evaluate, which is a feature here rather than an obstacle: a harness
 * that reaches past the interface can prove things a pupil could never do.
 */
import fs from 'node:fs'; import path from 'node:path';
const _pwPath = process.env.VCL_PLAYWRIGHT || '/opt/node22/lib/node_modules/playwright/index.js';
const _pw = await import(_pwPath).catch(() => import('playwright'));
const chromium = _pw.chromium || _pw.default.chromium;
const ROOT = process.env.VCL_ROOT || path.dirname(new URL(import.meta.url).pathname);
const STAGING = process.env.VCL_STAGING || 'staging';
const FILE = 'Virtual_Chemistry_Lab_PRO_Spatial_v0_3.html';
const TREES = ['release', STAGING];
const [T_REL, T_PAT] = TREES;

const rows = [];
const pair = (id, what, relOk, patOk, detail = '', bothTrue = 'NOT A CONTROL') =>
  rows.push({ id, what, release: relOk, patched: patOk,
    verdict: (relOk === 'UNREACHABLE' || patOk === 'UNREACHABLE') ? 'UNREACHABLE'
           : (!relOk && patOk) ? 'MATCHED PAIR'
           : (relOk && patOk) ? bothTrue
           : (relOk && !patOk) ? 'REGRESSION'
           : 'NOT A CONTROL', detail });
const note = (id, what, verdict, detail) => rows.push({ id, what, release: null, patched: null, verdict, detail });

const browser = await chromium.launch();
async function open(tree, opts = {}) {
  const ctx = await browser.newContext(Object.assign({ viewport: { width: 1440, height: 900 } }, opts));
  const pg = await ctx.newPage();
  const errs = []; pg.on('pageerror', e => errs.push(String(e).slice(0, 160)));
  const cons = []; pg.on('console', m => { if (/error|warning/.test(m.type())) cons.push(m.type() + ': ' + m.text().slice(0, 120)); });
  await pg.addInitScript(() => {
    window.__blobs = [];
    const orig = URL.createObjectURL.bind(URL);
    URL.createObjectURL = b => { window.__blobs.push(b); return orig(b); };
  });
  await pg.goto('file://' + path.resolve(ROOT, tree, FILE), { waitUntil: 'domcontentloaded', timeout: 45000 });
  await pg.waitForTimeout(1200);
  return { ctx, pg, errs, cons };
}
const toMicro = pg => pg.evaluate(async () => {
  const s = document.getElementById('benchSelect');
  s.value = 'microscale'; s.dispatchEvent(new Event('change', { bubbles: true }));
  await new Promise(r => setTimeout(r, 400));
});

/* =====================================================================
 * V1 — does the bench reward the procedure it teaches against?
 * Driven exactly as a pupil would: pick a dropper, click a well, repeat.
 * ===================================================================== */
const SEQ = [
  { id: 'chloride', sample: 'sample_kcl', acid: 'reagent_hno3', test: 'reagent_agno3', positive: /white silver chloride/i },
  { id: 'bromide',  sample: 'sample_kbr', acid: 'reagent_hno3', test: 'reagent_agno3', positive: /cream silver bromide/i },
  { id: 'iodide',   sample: 'sample_ki',  acid: 'reagent_hno3', test: 'reagent_agno3', positive: /yellow silver iodide/i },
  { id: 'sulfate',  sample: 'sample_al',  acid: 'reagent_hcl',  test: 'reagent_bacl2', positive: /barium sulfate/i },
];
for (const tree of TREES) {
  const { ctx, pg, errs } = await open(tree);
  await toMicro(pg);
  const out = await pg.evaluate(async (seq) => {
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    const drop = async (key, well) => {
      const b = document.querySelector(`[data-action="micro-select"][data-key="${key}"]`);
      if (!b) throw new Error('no dropper ' + key);
      b.click(); await sleep(80);
      const w = document.querySelector(`[data-action="micro-well"][data-index="${well}"]`);
      if (!w) throw new Error('no well ' + well);
      w.click(); await sleep(120);
    };
    const read = () => {
      const o = document.querySelector('.micro-observation');
      return { observation: (o ? o.textContent : '').replace(/\s+/g, ' ').trim(),
               warning: !!document.querySelector('.micro-observation .feedback.warn') };
    };
    const res = {};
    let well = 0;
    for (const s of seq) {
      await drop(s.sample, well); await drop(s.acid, well); await drop(s.test, well);
      res[s.id + ':correct'] = read();
      well++;
      await drop(s.sample, well); await drop(s.test, well); await drop(s.acid, well);
      res[s.id + ':reversed'] = read();
      well++;
    }
    return res;
  }, SEQ);
  await ctx.close();
  if (errs.length) note('ERR', `page errors in ${tree}`, 'PAGE ERROR', errs.join(' | '));
  globalThis['v1_' + tree] = out;
}
for (const s of SEQ) {
  const R = globalThis['v1_' + T_REL], P = globalThis['v1_' + T_PAT];
  /* the correct order must still give the clean positive, with no warning */
  const okCorrect = x => s.positive.test(x[s.id + ':correct'].observation) && !x[s.id + ':correct'].warning;
  pair(`V1 ${s.id} correct`, `${s.id}: acid then reagent still gives the clean positive`,
    okCorrect(R), okCorrect(P),
    `release "${R[s.id + ':correct'].observation.slice(0, 90)}" -> staging "${P[s.id + ':correct'].observation.slice(0, 90)}"`,
    'ALREADY CORRECT ON RELEASE');
  /* the reversed order must NOT give the clean positive, and MUST warn */
  const okRev = x => !s.positive.test(x[s.id + ':reversed'].observation) && x[s.id + ':reversed'].warning;
  pair(`V1 ${s.id} reversed`, `${s.id}: reagent BEFORE the acid is not rewarded, and is warned about`,
    okRev(R), okRev(P),
    `release "${R[s.id + ':reversed'].observation.slice(0, 110)}" (warned ${R[s.id + ':reversed'].warning}) -> ` +
    `staging "${P[s.id + ':reversed'].observation.slice(0, 110)}" (warned ${P[s.id + ':reversed'].warning})`);
}

/* =====================================================================
 * V2 — is the pupil's name in the URL?
 * ===================================================================== */
for (const tree of TREES) {
  const { ctx, pg } = await open(tree);
  const out = await pg.evaluate(async () => {
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    const set = (id, v) => { const e = document.getElementById(id); e.value = v;
      e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); };
    set('pupilName', 'AVA-CANARY-NAME');
    set('reflectionNotes', 'NOTE-CANARY-TEXT');
    document.getElementById('shareBtn').click();
    await sleep(500);
    const decode = h => { try {
      let s = h.replace(/^#s=/, '').replace(/-/g, '+').replace(/_/g, '/');
      while (s.length % 4) s += '=';
      return decodeURIComponent(escape(atob(s)));
    } catch (e) { return 'DECODE FAILED: ' + e.message; } };
    const hashPlain = decode(location.hash);
    document.getElementById('exportBtn').click();
    await sleep(500);
    const exported = window.__blobs.length ? await window.__blobs[window.__blobs.length - 1].text() : '';
    document.getElementById('printBtn').click();
    await sleep(400);
    const sheet = document.getElementById('printSheet');
    const printed = sheet ? sheet.textContent : (document.querySelector('.print-sheet') || {}).textContent || '';
    return {
      nameInHash: /AVA-CANARY-NAME/.test(hashPlain),
      noteInHash: /NOTE-CANARY-TEXT/.test(hashPlain),
      nameInExport: /AVA-CANARY-NAME/.test(exported),
      nameInPrint: /AVA-CANARY-NAME/.test(printed),
      caption: (document.getElementById('pupilName') || {}).placeholder || '',
      hashLen: location.hash.length,
      decodeOk: !/^DECODE FAILED/.test(hashPlain),
    };
  });
  await ctx.close();
  globalThis['v2_' + tree] = out;
}
{
  const R = globalThis['v2_' + T_REL], P = globalThis['v2_' + T_PAT];
  pair('V2a', 'the pupil name is absent from the state URL, as its caption promises',
    R.decodeOk && !R.nameInHash, P.decodeOk && !P.nameInHash,
    `caption "${P.caption}" · release name-in-hash=${R.nameInHash} -> staging name-in-hash=${P.nameInHash}`);
  pair('V2b', 'the name is still in print and in Export JSON, which is what the caption offers',
    R.nameInExport && R.nameInPrint, P.nameInExport && P.nameInPrint,
    `release export=${R.nameInExport} print=${R.nameInPrint} -> staging export=${P.nameInExport} print=${P.nameInPrint}`,
    'ALREADY CORRECT ON RELEASE — asserted so the V2 fix cannot quietly take it away');
  note('V2c', 'the evidence note is deliberately KEPT in the hash', 'MEASURED',
    `release note-in-hash=${R.noteInHash} -> staging note-in-hash=${P.noteInHash}. ` +
    `This app has zero localStorage, so the hash is its only persistence: dropping the note would destroy pupil writing on reload. ` +
    `The Share help card and the note's own label are corrected instead (X2b, X2c).`);
}

/* V2 continued — the captions. The one thing V2 says must not survive this
   patch is a caption that lies, so the captions are asserted, not assumed. The
   removal matrix caught these: both caption transforms were UNWATCHED. */
for (const tree of TREES) {
  const { ctx, pg } = await open(tree);
  const out = await pg.evaluate(() => {
    const help = [...document.querySelectorAll('.help-card')].find(h => /Share/.test(h.textContent || ''));
    const lbl = document.querySelector('label[for="reflectionNotes"]');
    return { share: help ? help.textContent.replace(/\s+/g, ' ').trim() : null,
             notesLabel: lbl ? lbl.textContent.replace(/\s+/g, ' ').trim() : null,
             nameCaption: (document.getElementById('pupilName') || {}).placeholder || null };
  });
  await ctx.close();
  globalThis['cap_' + tree] = out;
}
{
  const R = globalThis['cap_' + T_REL], P = globalThis['cap_' + T_PAT];
  const shareHonest = x => !!x.share && /not/i.test(x.share) && /name/i.test(x.share) && /note/i.test(x.share);
  pair('V2d', 'the Share help card says the link carries the note and NOT the name',
    shareHonest(R), shareHonest(P),
    `release "${(R.share || '').slice(0, 110)}" -> staging "${(P.share || '').slice(0, 150)}"`);
  const notesHonest = x => !!x.notesLabel && /shared link|address bar/i.test(x.notesLabel);
  pair('V2e', 'the evidence-note label says the note travels in the URL and in a shared link',
    notesHonest(R), notesHonest(P),
    `release "${R.notesLabel}" -> staging "${P.notesLabel}"`);
  note('V2f', 'the name caption is unchanged — the patch makes it true rather than rewriting it', 'MEASURED',
    `release "${R.nameCaption}" -> staging "${P.nameCaption}"`);
}

/* =====================================================================
 * V3 — the state URL length
 * ===================================================================== */
const BOUND = 2048;
for (const tree of TREES) {
  const { ctx, pg } = await open(tree);
  const out = await pg.evaluate(async () => {
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    const go = async b => { const s = document.getElementById('benchSelect'); s.value = b;
      s.dispatchEvent(new Event('change', { bubbles: true })); await sleep(400); return location.hash.length; };
    const res = { fresh: location.hash.length, benches: {} };
    for (const b of ['spatial', 'microscale', 'rates', 'titration', 'gastest']) res.benches[b] = await go(b);
    /* a realistic 40-minute microscale session: four tests, three drops each,
       plus a name, a note and three written answers */
    await go('microscale');
    const drop = async (key, well) => {
      document.querySelector(`[data-action="micro-select"][data-key="${key}"]`).click(); await sleep(40);
      document.querySelector(`[data-action="micro-well"][data-index="${well}"]`).click(); await sleep(60);
    };
    let w = 0;
    for (const [smp, acid, test] of [['sample_kcl', 'reagent_hno3', 'reagent_agno3'],
                                     ['sample_kbr', 'reagent_hno3', 'reagent_agno3'],
                                     ['sample_ki', 'reagent_hno3', 'reagent_agno3'],
                                     ['sample_al', 'reagent_hcl', 'reagent_bacl2']]) {
      await drop(smp, w); await drop(acid, w); await drop(test, w); w++;
    }
    const set = (id, v) => { const e = document.getElementById(id); if (!e) return; e.value = v;
      e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); };
    set('pupilName', 'A Pupil Name Of Realistic Length');
    set('reflectionNotes', 'The halide tests gave white, cream and yellow precipitates in order, which matches chloride, bromide and iodide. The sulfate test gave a dense white precipitate after acidifying with hydrochloric acid.');
    for (let i = 0; i < 3; i++) set(`phase-microscale-${i}`, 'A written answer of the length a pupil would actually type in a lesson, with a reason attached.');
    document.getElementById('shareBtn').click();
    await sleep(400);
    res.session = location.hash.length;
    return res;
  });
  await ctx.close();
  globalThis['v3_' + tree] = out;
}
{
  const R = globalThis['v3_' + T_REL], P = globalThis['v3_' + T_PAT];
  pair('V3', `a realistic 40-minute session URL stays under the ${BOUND}-character ceiling`,
    R.session < BOUND, P.session < BOUND,
    `realistic session: release ${R.session} chars -> staging ${P.session} chars (bound ${BOUND})`);
  note('V3-detail', 'hash length, fresh and per untouched bench', 'MEASURED',
    `fresh: release ${R.fresh} -> staging ${P.fresh} · ` +
    Object.keys(P.benches).map(b => `${b} ${R.benches[b]}->${P.benches[b]}`).join(' · '));
}

/* V3 round-trip. Shrinking the encoding is worthless if the link no longer
   restores the session, and the compact form drops fields that are rebuilt
   rather than stored — so this is the assertion that matters most. */
for (const tree of TREES) {
  const { ctx, pg } = await open(tree);
  await toMicro(pg);
  const url = await pg.evaluate(async () => {
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    const drop = async (k, w) => {
      document.querySelector(`[data-action="micro-select"][data-key="${k}"]`).click(); await sleep(40);
      document.querySelector(`[data-action="micro-well"][data-index="${w}"]`).click(); await sleep(70);
    };
    await drop('sample_kcl', 2); await drop('reagent_hno3', 2); await drop('reagent_agno3', 2);
    await drop('sample_fe3', 5); await drop('reagent_naoh', 5);
    const set = (id, v) => { const e = document.getElementById(id); if (!e) return; e.value = v;
      e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); };
    set('reflectionNotes', 'ROUNDTRIP-NOTE');
    set('phase-microscale-0', 'ROUNDTRIP-ANSWER');
    document.getElementById('shareBtn').click();
    await sleep(400);
    return location.href;
  });
  await ctx.close();
  const { ctx: c2, pg: p2, errs } = await open(tree);
  await p2.goto(url, { waitUntil: 'domcontentloaded' });
  await p2.waitForTimeout(1400);
  const back = await p2.evaluate(() => {
    const wells = [...document.querySelectorAll('[data-action="micro-well"]')].map(w => w.getAttribute('aria-label'));
    const rows = [...document.querySelectorAll('.table-wrap tbody tr')].map(r => r.textContent.replace(/\s+/g, ' ').trim());
    return {
      bench: (document.getElementById('benchSelect') || {}).value,
      wellC1: wells[2] || '', wellB2: wells[5] || '',
      note: (document.getElementById('reflectionNotes') || {}).value || '',
      answer: (document.getElementById('phase-microscale-0') || {}).value || '',
      eventRows: rows.length,
      eventsHaveObservation: rows.some(r => /precipitate/i.test(r)),
      /* per-moment fidelity: the row for the sample drop happened BEFORE any
         silver went in, so it must not claim a silver chloride precipitate */
      perMoment: !rows.some(r => /Potassium chloride/.test(r) && /silver chloride/i.test(r)),
    };
  });
  await c2.close();
  globalThis['rt_' + tree] = { back, errs, urlLen: url.length };
}
{
  const ok = x => /silver chloride/i.test(x.back.wellC1) && /red-brown/i.test(x.back.wellB2)
              && x.back.note === 'ROUNDTRIP-NOTE' && x.back.answer === 'ROUNDTRIP-ANSWER'
              && x.back.bench === 'microscale' && x.back.eventRows >= 5 && x.back.eventsHaveObservation && x.back.perMoment
              && x.errs.length === 0;
  const R = globalThis['rt_' + T_REL], P = globalThis['rt_' + T_PAT];
  pair('V3-roundtrip', 'a shared link restores wells, observations, the event log, the note and the written answer',
    ok(R), ok(P),
    `release url ${R.urlLen} chars ${JSON.stringify(R.back)} -> staging url ${P.urlLen} chars ${JSON.stringify(P.back)}`,
    'ALREADY CORRECT ON RELEASE — asserted so the V3 shrink cannot silently break resume');
}

/* an old whole-tree link, minted by the release build, must still open in the
   patched build. Same reason: shrinking an encoding is where links die. */
{
  const { ctx, pg } = await open(T_REL);
  await toMicro(pg);
  const oldUrl = await pg.evaluate(async () => {
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    const drop = async (k, w) => {
      document.querySelector(`[data-action="micro-select"][data-key="${k}"]`).click(); await sleep(40);
      document.querySelector(`[data-action="micro-well"][data-index="${w}"]`).click(); await sleep(70);
    };
    await drop('sample_kcl', 1); await drop('reagent_hno3', 1); await drop('reagent_agno3', 1);
    document.getElementById('shareBtn').click(); await sleep(400);
    return location.hash;
  });
  await ctx.close();
  const { ctx: c2, pg: p2, errs } = await open(T_PAT);
  await p2.goto('file://' + path.resolve(ROOT, T_PAT, FILE) + oldUrl, { waitUntil: 'domcontentloaded' });
  await p2.waitForTimeout(1400);
  const back = await p2.evaluate(() => ({
    bench: (document.getElementById('benchSelect') || {}).value,
    well: ([...document.querySelectorAll('[data-action="micro-well"]')][1] || {}).getAttribute
      ? [...document.querySelectorAll('[data-action="micro-well"]')][1].getAttribute('aria-label') : '',
  }));
  await c2.close();
  note('V3-legacy', 'a link minted by the RELEASE build still opens in the patched build',
    (/silver chloride/i.test(back.well) && back.bench === 'microscale' && errs.length === 0) ? 'ASSERTED' : 'BROKEN',
    `old-format hash ${oldUrl.length} chars -> ${JSON.stringify(back)} errs ${errs.length}`);
}

/* =====================================================================
 * V4 — .drop-pill has no CSS rule at all
 * ===================================================================== */
for (const tree of TREES) {
  for (const width of [390, 1440]) {
    const { ctx, pg } = await open(tree, { viewport: { width, height: 900 } });
    await toMicro(pg);
    const out = await pg.evaluate(async () => {
      const sleep = ms => new Promise(r => setTimeout(r, ms));
      for (const k of ['sample_fe3', 'reagent_naoh']) {
        document.querySelector(`[data-action="micro-select"][data-key="${k}"]`).click(); await sleep(50);
        document.querySelector('[data-action="micro-well"][data-index="0"]').click(); await sleep(90);
      }
      const pills = [...document.querySelectorAll('.drop-pill')].map(p => p.getBoundingClientRect());
      let minGap = Infinity;
      for (let i = 1; i < pills.length; i++) {
        const a = pills[i - 1], b = pills[i];
        const gap = (Math.abs(b.top - a.top) > 4) ? Infinity : b.left - a.right;   // wrapped rows do not count
        if (gap < minGap) minGap = gap;
      }
      return { count: pills.length, minGap: minGap === Infinity ? null : Math.round(minGap * 100) / 100,
               text: [...document.querySelectorAll('.drop-pill')].map(p => p.textContent).join('|') };
    });
    await ctx.close();
    globalThis[`v4_${tree}_${width}`] = out;
  }
}
for (const width of [390, 1440]) {
  const R = globalThis[`v4_${T_REL}_${width}`], P = globalThis[`v4_${T_PAT}_${width}`];
  const ok = x => x.count >= 2 && x.minGap !== null && x.minGap > 0;
  pair(`V4 @${width}px`, `adjacent drop pills are separated by a non-zero horizontal gap at ${width}px`,
    ok(R), ok(P),
    `release ${R.count} pills, min gap ${R.minGap} -> staging ${P.count} pills, min gap ${P.minGap} · "${P.text}"`);
}

/* =====================================================================
 * V5 — answer marking is negation-blind
 * Six items the order names, plus two written a different way with the same
 * defect. Each gets a correct answer and a negated near-miss.
 * ===================================================================== */
const V5 = [
  { bench: 'titration', i: 0, right: 'water left in the burette would dilute the titrant and change its concentration',
                              negated: "water left in the burette would not dilute the titrant, so concentration doesn't change" },
  { bench: 'gastest', i: 0, right: 'a glowing splint relights in oxygen',
                            negated: 'the glowing splint does not relight' },
  { bench: 'gastest', i: 2, right: 'the gas is oxygen because the glowing splint relit',
                            negated: 'the gas is not oxygen because the glowing splint did not relight' },
  { bench: 'spatial', i: 0, right: 'close the air hole to light it with a visible yellow safety flame',
                            negated: 'do not close the air hole and never light it with a yellow safety flame' },
  { bench: 'spatial', i: 2, right: 'it cannot certify real hands-on glassware and safety competence',
                            negated: 'it can certify real hands-on glassware and safety competence' },
  { bench: 'microscale', i: 0, right: 'a red-brown precipitate of iron(III) hydroxide forms',
                               negated: 'no red-brown iron hydroxide precipitate forms' },
  { bench: 'microscale', i: 2, right: 'hydrochloric acid adds chloride ions and gives a false silver chloride precipitate, nitric acid does not',
                               negated: 'hydrochloric acid does not add chloride ions and cannot give a false silver chloride precipitate, unlike nitric acid' },
  { bench: 'rates', i: 0, right: 'the rate increases because more particles per volume means more frequent successful collisions',
                          negated: 'the rate does not increase and collisions are not more frequent' },
];
for (const tree of TREES) {
  const { ctx, pg } = await open(tree);
  const out = await pg.evaluate(async (items) => {
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    const res = {};
    for (const it of items) {
      const s = document.getElementById('benchSelect');
      s.value = it.bench; s.dispatchEvent(new Event('change', { bubbles: true }));
      await sleep(350);
      for (const variant of ['right', 'negated']) {
        const input = document.getElementById(`phase-${it.bench}-${it.i}`);
        const fb = document.getElementById(`phase-fb-${it.bench}-${it.i}`);
        if (!input || !fb) { res[`${it.bench}-${it.i}-${variant}`] = { missing: true }; continue; }
        input.value = it[variant];
        input.dispatchEvent(new Event('input', { bubbles: true }));
        const btn = input.closest('.answer-row').querySelector('[data-action="phase-check"]');
        btn.click();
        await sleep(200);
        res[`${it.bench}-${it.i}-${variant}`] = {
          cls: fb.className, text: fb.textContent.replace(/\s+/g, ' ').trim().slice(0, 160),
          button: btn.textContent.trim(),
        };
      }
    }
    return res;
  }, V5);
  await ctx.close();
  globalThis['v5_' + tree] = out;
}
{
  const R = globalThis['v5_' + T_REL], P = globalThis['v5_' + T_PAT];
  /* "called correct" means either the green tone or the tick */
  const calledCorrect = c => !!c && !c.missing && (/\bgood\b/.test(c.cls) || /^✓/.test(c.text));
  const failing = t => V5.filter(it => calledCorrect(globalThis['v5_' + t][`${it.bench}-${it.i}-negated`]));
  pair('V5', 'no negated near-miss is called correct',
    failing(T_REL).length === 0, failing(T_PAT).length === 0,
    `release marks ${failing(T_REL).length}/${V5.length} negated answers CORRECT [${failing(T_REL).map(i => i.bench + '-' + i.i)}] -> ` +
    `staging marks ${failing(T_PAT).length}/${V5.length}`);
  /* option (a): these items stop claiming a verdict at all, either way */
  const claimsVerdict = t => V5.filter(it => ['right', 'negated'].some(v => {
    const c = globalThis['v5_' + t][`${it.bench}-${it.i}-${v}`];
    return !!c && !c.missing && (/\b(good|bad)\b/.test(c.cls) || /^[✓→]/.test(c.text));
  }));
  pair('V5b', 'the keyword items pronounce no verdict at all, right answer or wrong',
    claimsVerdict(T_REL).length === 0, claimsVerdict(T_PAT).length === 0,
    `release: ${claimsVerdict(T_REL).length}/${V5.length} still pronounce · staging: ${claimsVerdict(T_PAT).length}/${V5.length}`);
  note('V5-detail', 'one item, both variants, both trees', 'MEASURED',
    `release negated gastest-0: [${R['gastest-0-negated'].cls}] "${R['gastest-0-negated'].text}" || ` +
    `staging negated gastest-0: [${P['gastest-0-negated'].cls}] "${P['gastest-0-negated'].text}"`);
  note('V5-button', 'the button label', 'MEASURED',
    `release "${R['gastest-0-right'].button}" -> staging "${P['gastest-0-right'].button}"`);
}

/* =====================================================================
 * V6.4 / V6.5 — reduced-motion seed and accessible names
 * ===================================================================== */
for (const tree of TREES) {
  const { ctx, pg } = await open(tree, { reducedMotion: 'reduce' });
  const seeded = await pg.evaluate(() => {
    const b = document.getElementById('calmBtn');
    return { pressed: b ? (b.getAttribute('aria-pressed') || b.className) : null,
             bodyCalm: document.body.classList.contains('calm') || document.documentElement.classList.contains('calm'),
             matchMediaUsed: null };
  });
  await ctx.close();
  globalThis['v6m_' + tree] = seeded;
}
{
  const srcOf = t => fs.readFileSync(path.join(ROOT, t, FILE), 'utf8');
  const usesMM = t => /matchMedia\s*\(\s*["']\(prefers-reduced-motion: reduce\)["']\s*\)/.test(srcOf(t));
  pair('V6.4a', 'the JS layer reads prefers-reduced-motion, not only the CSS blanket rule',
    usesMM(T_REL), usesMM(T_PAT),
    `matchMedia('(prefers-reduced-motion: reduce)') present: release ${usesMM(T_REL)} -> staging ${usesMM(T_PAT)}`);
  const R = globalThis['v6m_' + T_REL], P = globalThis['v6m_' + T_PAT];
  const calmOn = x => !!x.bodyCalm || /active|on|true/i.test(String(x.pressed));
  pair('V6.4b', 'booting under prefers-reduced-motion seeds calm mode',
    calmOn(R), calmOn(P),
    `release ${JSON.stringify(R)} -> staging ${JSON.stringify(P)}`);
}
for (const tree of TREES) {
  const { ctx, pg } = await open(tree);
  const out = await pg.evaluate(async () => {
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    const nm = el => {
      const lb = (el.getAttribute('aria-labelledby') || '').split(/\s+/).filter(Boolean)
        .map(i => (document.getElementById(i) || {}).textContent || '').join(' ').trim();
      if (lb) return 'aria-labelledby';
      if ((el.getAttribute('aria-label') || '').trim()) return 'aria-label';
      if (el.id) { const l = document.querySelector(`label[for="${CSS.escape(el.id)}"]`); if (l && l.textContent.trim()) return 'label[for]'; }
      const w = el.closest('label'); if (w && w.textContent.trim()) return 'wrapping label';
      if ((el.getAttribute('title') || '').trim()) return 'title';
      if (el.tagName === 'BUTTON' && el.textContent.trim()) return 'button text';
      return null;
    };
    const unnamed = [];
    for (const b of ['spatial', 'microscale', 'rates', 'titration', 'gastest']) {
      const s = document.getElementById('benchSelect');
      s.value = b; s.dispatchEvent(new Event('change', { bubbles: true }));
      await sleep(350);
      for (const el of document.querySelectorAll('input,select,textarea,button,[role="button"]'))
        if (!nm(el)) unnamed.push(`${b}:${el.tagName.toLowerCase()}#${el.id || '(no id)'}`);
    }
    return [...new Set(unnamed)];
  });
  await ctx.close();
  globalThis['v6n_' + tree] = out;
}
{
  const R = globalThis['v6n_' + T_REL], P = globalThis['v6n_' + T_PAT];
  pair('V6.5', 'every control on every bench has an accessible name',
    R.length === 0, P.length === 0,
    `predicate: aria-label / aria-labelledby / label[for] / wrapping label / title / button text; ` +
    `a placeholder is NOT counted. release ${R.length} unnamed [${R.join(', ')}] -> staging ${P.length} unnamed [${P.join(', ')}]`);
}

/* =====================================================================
 * V0 FREEZE — the things that must not have moved
 * ===================================================================== */
{
  const srcOf = t => fs.readFileSync(path.join(ROOT, t, FILE), 'utf8');
  const grab = (s, re) => (s.match(re) || []).join('\n');
  const FROZEN = [
    ['the pH model', /let H=pool\.H\|\|0[\s\S]*?w\.pH=7;/],
    ['the deterministic mystery hash', /function microMystery[\s\S]{0,400}?\n/],
    ['the Cu / Fe2 / Fe3 / Al3 / Ca2 hydroxide chain', /if\(has\("Cu2"\)&&oh>0\)[\s\S]*?remains in excess sodium hydroxide\.";}/],
    ['the sequencing teaching copy', /<strong>Halides:<\/strong>[\s\S]{0,220}?interference\./],
  ];
  const moved = FROZEN.filter(([, re]) => grab(srcOf(T_REL), re) !== grab(srcOf(T_PAT), re)).map(([n]) => n);
  note('V0', 'the frozen engine, pH model, mystery hash and teaching copy are byte-identical',
    moved.length === 0 ? 'ASSERTED UNCHANGED' : 'MOVED — HARD STOP',
    moved.length ? `moved: ${moved.join(' · ')}` : FROZEN.map(([n]) => n).join(' · '));
  if (moved.length) rows[rows.length - 1].verdict = 'MOVED — HARD STOP';
}

await browser.close();
console.log(`${'id'.padEnd(20)} ${'release'.padEnd(9)} ${'staging'.padEnd(9)} verdict`);
console.log('-'.repeat(84));
for (const r of rows) {
  console.log(`${r.id.padEnd(20)} ${String(r.release).padEnd(9)} ${String(r.patched).padEnd(9)} ${r.verdict}`);
  console.log(`    ${r.what}`);
  if (r.detail) console.log(`    ${r.detail}`);
}
const bad = rows.filter(r => ['NOT A CONTROL', 'REGRESSION', 'PAGE ERROR', 'MOVED — HARD STOP', 'BROKEN'].includes(r.verdict));
const un = rows.filter(r => r.verdict === 'UNREACHABLE');
console.log(`\n${bad.length} failure(s); ${un.length} unreachable`);
process.exit(bad.length ? 1 : un.length ? 2 : 0);
