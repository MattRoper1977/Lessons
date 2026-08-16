/* P2 controls. Every fix assertion runs against BOTH trees: it must FAIL on
 * release/ and PASS on patched/. A control that passes on both is not a control
 * — it is decoration, which is this session's whole subject.
 *
 * Two things this file will not do:
 *   - substitute a stand-in when its subject is unreachable (R0.9). An
 *     unreachable subject reports UNREACHABLE and the run is inconclusive.
 *   - report a band a pupil cannot reach as though a pupil could reach it
 *     (R0.10). The Wilton set is split: reachable-through-the-buttons, and
 *     unit-level.
 */
import fs from 'node:fs'; import path from 'node:path';
const _pwPath = process.env.P2_PLAYWRIGHT || '/opt/node22/lib/node_modules/playwright/index.js';
const _pw = await import(_pwPath).catch(() => import('playwright'));
const ROOT = process.env.P2_ROOT || path.dirname(new URL(import.meta.url).pathname);
const PATCHED = process.env.P2_PATCHED || 'staging';
const chromium = _pw.chromium || _pw.default.chromium;

const LABS = ['01_Newport_Bridge_Lift_Permit_Lab.html', '02_Tees_Estuary_Field_Investigation_Lab.html',
              '03_Wilton_Carbon_Process_Control_Lab.html', '04_Tees_Bay_Wind_Operations_Lab.html'];
const WILTON = '03_Wilton_Carbon_Process_Control_Lab.html';
const STUDIO = '00_BUILD_FieldOps_Teacher_Studio.html';
const TREES = ['release', PATCHED];
const [T_REL, T_PAT] = TREES;

const rows = [];
/* bothTrue: for the per-feed rows only. Release gets some feeds right already —
   that is the measurement, not a broken control, and calling it NOT A CONTROL
   would misreport a correct result. Every row where release is ALSO wrong must
   still come out as a matched pair. */
const pair = (id, what, relOk, patOk, detail = '', bothTrue = 'NOT A CONTROL', declared = false) =>
  rows.push({ id, what, release: relOk, patched: patOk, declared,
              verdict: (relOk === 'UNREACHABLE' || patOk === 'UNREACHABLE') ? 'UNREACHABLE'
                     : (!relOk && patOk) ? 'MATCHED PAIR'
                     : (relOk && patOk) ? bothTrue
                     : (relOk && !patOk) ? 'REGRESSION'   /* release passed, patched does not */
                     : 'NOT A CONTROL', detail });
const note = (id, what, verdict, detail) => rows.push({ id, what, release: null, patched: null, verdict, detail });

const browser = await chromium.launch();
async function evalIn(tree, file, fn, arg, opts = {}) {
  const ctx = await browser.newContext(Object.assign({ viewport: { width: 1280, height: 900 }, hasTouch: true }, opts));
  const pg = await ctx.newPage();
  const errs = []; pg.on('pageerror', e => errs.push(String(e).slice(0, 120)));
  await pg.goto('file://' + path.resolve(ROOT, tree, file), { waitUntil: 'domcontentloaded', timeout: 45000 });
  await pg.waitForTimeout(900);
  const out = await pg.evaluate(fn, arg);
  await ctx.close();
  return { out, errs };
}

/* =====================================================================
 * §A  WILTON — REACHABLE SET
 * Driven through the real feed buttons, the real furnace slider and the
 * real "Run distillation" button, then read from what the lab TELLS the
 * pupil (#wTrayRead), not from wTray().
 * ===================================================================== */
const CORRECT = { 6: 'petrol', 10: 'petrol', 14: 'kerosene', 18: 'diesel', 20: 'diesel', 21: 'fuel-oil', 24: 'fuel-oil' };
const REACHABLE = [6, 10, 14, 18, 20, 21, 24];
/* C24 is UNREACHABLE BY DESIGN, not by oversight: it boils at 430C and this
   column's furnace stops at 390C. Ruling A keeps it selectable and keeps this
   line reporting UNREACHABLE. C21's arrival must not quietly convert it to a
   pass — the declaration is the teaching point. */
const UNREACHABLE_BY_DESIGN = new Set([24]);

for (const tree of TREES) {
  const { out, errs } = await evalIn(tree, WILTON, async (feeds) => {
    const res = {};
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    const furn = document.getElementById('wFurnace');
    for (const n of feeds) {
      const btn = document.querySelector(`.feedW[data-feed="${n}"]`);
      if (!btn) { res[n] = { button: false }; continue; }
      btn.click();
      furn.value = furn.max;
      furn.dispatchEvent(new Event('input', { bubbles: true }));
      await sleep(60);
      document.getElementById('runDistil').click();
      await sleep(80);
      const ev = typeof getAppEvidence === 'function' ? getAppEvidence() : null;
      res[n] = {
        button: true,
        furnaceMax: +furn.max,
        told: (document.getElementById('wTrayRead').textContent || '').trim(),
        notice: (document.getElementById('wDistilResult').textContent || '').trim(),
        distilled: !!(ev && ev.current && ev.current.distilled),
        zone: ev ? ev.condensationZone : null,
        markerY: +document.getElementById('condenseW').getAttribute('cy'),
      };
    }
    return res;
  }, REACHABLE);
  if (errs.length) note('ERR', `page errors in ${tree}/${WILTON}`, 'PAGE ERROR', errs.join(' | '));
  globalThis['reach_' + tree] = out;
}
const RR = globalThis['reach_' + T_REL], RP = globalThis['reach_' + T_PAT];

for (const n of REACHABLE) {
  const want = CORRECT[n];
  const r = RR[n], p = RP[n];
  /* Two different things, and collapsing them cost the C21 row its verdict:
     NO BUTTON is a plain fail — the fraction cannot be taught because nothing
     selects it, and a patch that adds the button is a matched pair against it.
     BUTTON BUT WILL NOT DISTIL is genuinely unreachable — the subject is there
     and cannot be reached, which is C24 and is never scored as a pass. */
  const scoreOf = x => {
    if (!x || !x.button) return false;                   // no way to select it at all
    if (!x.distilled) return 'UNREACHABLE';              // selectable, lab refuses to separate it
    return new RegExp(want).test(x.told);
  };
  const sr = scoreOf(r), sp = scoreOf(p);
  const dr = r && r.button ? (r.distilled ? `told "${r.told}"` : `NOT DISTILLED at ${r.furnaceMax}°C max`) : 'no button';
  const dp = p && p.button ? (p.distilled ? `told "${p.told}"` : `NOT DISTILLED at ${p.furnaceMax}°C max`) : 'no button';
  pair(`W-R-C${n}`, `C${n} is taught as ${want} through the real buttons`, sr, sp,
    `release: ${dr}  ->  patched: ${dp}`, 'ALREADY CORRECT ON RELEASE', UNREACHABLE_BY_DESIGN.has(n));
}

/* the headline figure, computed rather than asserted */
const scoreTree = R => REACHABLE.filter(n => R[n] && R[n].button && R[n].distilled && new RegExp(CORRECT[n]).test(R[n].told)).length;
const selectable = R => REACHABLE.filter(n => R[n] && R[n].button).length;
const undistillable = R => REACHABLE.filter(n => R[n] && R[n].button && !R[n].distilled);
note('W-SCORE', 'selectable feeds taught in the chemically correct band',
  'MEASURED',
  `release ${scoreTree(RR)} of ${selectable(RR)} selectable  ->  patched ${scoreTree(RP)} of ${selectable(RP)} selectable ` +
  `(${undistillable(RP).map(n => 'C' + n).join(', ') || 'none'} selectable but cannot be distilled at the ceiling)`);
/* Ruling A's headline, stated so it cannot be quoted loose */
{
  const declared = undistillable(RP).every(n => UNREACHABLE_BY_DESIGN.has(n))
                && [...UNREACHABLE_BY_DESIGN].every(n => undistillable(RP).includes(n));
  note('W-DESIGN', 'every feed that cannot be distilled is one declared unreachable by design',
    declared ? 'ASSERTED' : 'UNDECLARED FEED',
    `undistillable at the ceiling: [${undistillable(RP).map(n => 'C' + n)}] · declared: [${[...UNREACHABLE_BY_DESIGN].map(n => 'C' + n)}] · ` +
    `headline: ${scoreTree(RP)} of ${selectable(RP)} reachable, C24 declared unreachable by design`);
}

/* =====================================================================
 * §B  WILTON — UNIT-LEVEL SET.  NOT USER-REACHABLE.
 * C11, C15 and C16 cannot be chosen: the feed set is a closed list. These
 * call wTray() directly and are labelled so nobody reads them as pupil
 * experience.
 * ===================================================================== */
const UNIT = { 11: 'kerosene', 15: 'kerosene', 16: 'kerosene' };
for (const tree of TREES) {
  const { out } = await evalIn(tree, WILTON, (ns) => {
    if (typeof wTray !== 'function' || typeof wBoil !== 'function') return { unreachable: true };
    const o = {}; for (const n of ns) o[n] = { bp: wBoil(n), label: wTray(n).label }; return o;
  }, Object.keys(UNIT).map(Number));
  globalThis['unit_' + tree] = out;
}
const UR = globalThis['unit_' + T_REL], UP = globalThis['unit_' + T_PAT];
if (UR.unreachable || UP.unreachable) {
  note('W-U', 'UNIT-LEVEL — NOT USER-REACHABLE: wTray/wBoil not reachable from the page', 'UNREACHABLE',
    'no substitution was made; this limb is inconclusive');
} else {
  for (const n of Object.keys(UNIT).map(Number)) {
    pair(`W-U-C${n}`, `UNIT-LEVEL — NOT USER-REACHABLE: wTray(${n}) is ${UNIT[n]}`,
      new RegExp(UNIT[n]).test(UR[n].label), new RegExp(UNIT[n]).test(UP[n].label),
      `bp ${UP[n].bp}°C · release "${UR[n].label}" -> patched "${UP[n].label}"`, 'ALREADY CORRECT ON RELEASE');
  }
}

/* =====================================================================
 * §C  the boundaries themselves
 * ===================================================================== */
for (const tree of TREES) {
  const src = fs.readFileSync(path.join(ROOT, tree, WILTON), 'utf8');
  const m = src.match(/function wTray\(n\)\{[^\n]*?\n/) || src.match(/function wTray\(n\)\{.{0,400}?\}\n/s);
  const decl = (src.split('function wTray(n){')[1] || '').split('\n')[0];
  globalThis['tray_' + tree] = decl;
  globalThis['boil_' + tree] = (src.match(/function wBoil\(n\)\{[^\n]*/) || [''])[0];
}
pair('W-STRICT', 'every band comparison in wTray is strict <, never <=',
  !/<=/.test(globalThis['tray_' + T_REL]) && false,   // release is already strict; see note below
  !/<=/.test(globalThis['tray_' + T_PAT]),
  `release has <= : ${/<=/.test(globalThis['tray_' + T_REL])} · patched has <= : ${/<=/.test(globalThis['tray_' + T_PAT])}`);
rows.pop();  /* release is strict too, so this cannot be a matched pair. State it as what it is. */
note('W-STRICT', 'every band comparison in wTray is strict <, never <=',
  (!/<=/.test(globalThis['tray_' + T_PAT])) ? 'ASSERTED' : 'FAILED',
  `patched wTray contains "<=" : ${/<=/.test(globalThis['tray_' + T_PAT])} (the earlier <= build is reverted)`);

note('W-BOIL', 'wBoil is untouched',
  globalThis['boil_' + T_REL] === globalThis['boil_' + T_PAT] ? 'ASSERTED UNCHANGED' : 'CHANGED — HARD STOP',
  globalThis['boil_' + T_PAT].trim());

{ /* no integer carbon number can land ON a boundary, for any n, not just the six */
  const bounds = [...globalThis['tray_' + T_PAT].matchAll(/bp<(\d+)/g)].map(m => +m[1]);
  const wBoil = n => -50 + 20 * n;
  const collisions = [];
  for (let n = 1; n <= 200; n++) if (bounds.includes(wBoil(n))) collisions.push(`C${n}=${wBoil(n)}`);
  const gaps = bounds.map(b => { const below = Math.floor((b + 50) / 20), above = below + 1;
    return `${b} lies in (C${below}=${wBoil(below)}, C${above}=${wBoil(above)})`; });
  note('W-GAP', 'no boundary sits on a wBoil value — every one is in a gap',
    collisions.length === 0 ? 'ASSERTED' : 'COLLISION',
    `boundaries [${bounds}] · collisions [${collisions}] · ${gaps.join(' · ')}`);
}

note('W-RES', 'the residue band still exists, as the else, relabelled as chemistry',
  /residue — what stays in the column/.test(globalThis['tray_' + T_PAT]) && /return\{y:525/.test(globalThis['tray_' + T_PAT])
    ? 'ASSERTED' : 'FAILED',
  `release "${(globalThis['tray_' + T_REL].match(/label:'residue[^']*'/) || [''])[0]}" -> patched "${(globalThis['tray_' + T_PAT].match(/label:'residue[^']*'/) || [''])[0]}"`);

/* the residue label a pupil actually sees, on the column, in the running page */
for (const tree of TREES) {
  const { out } = await evalIn(tree, WILTON, () =>
    [...document.querySelectorAll('#towerW text')].map(t => t.textContent.trim()));
  globalThis['cols_' + tree] = out;
}
pair('W-RES-UI', 'the column\'s residue label reads as chemistry, not as a missing button',
  globalThis['cols_' + T_REL].some(t => /what stays/.test(t)),
  globalThis['cols_' + T_PAT].some(t => /what stays/.test(t)),
  `release [${globalThis['cols_' + T_REL].join(' | ')}] -> patched [${globalThis['cols_' + T_PAT].join(' | ')}]`);

/* =====================================================================
 * §C2  the column diagram's own temperatures, against the code
 *
 * The column prints five tray temperatures. Those are a FOURTH set of numbers
 * about the same chemistry — after wBoil, the band cut-offs, and the feed set —
 * and nothing has ever checked them against the other three. This measures
 * each printed temperature against the band wTray puts that temperature in.
 * ===================================================================== */
for (const tree of TREES) {
  const { out } = await evalIn(tree, WILTON, () => {
    if (typeof wTray !== 'function') return { unreachable: true };
    /* recover the band for a raw boiling point by inverting wBoil: bp = -50+20n.
       wTray takes a carbon number, so a fractional n reaches any bp we like. */
    const bandOf = bp => wTray((bp + 50) / 20).label;
    return [...document.querySelectorAll('#towerW text')]
      .map(t => t.textContent.trim())
      .filter(s => /°C/.test(s))
      .map(s => { const bp = +s.match(/(-?\d+)°C/)[1];
                  const below = /^below/i.test(s);
                  const named = s.replace(/^[^·]*·\s*/, '').trim();
                  /* "below 25°C · gases" is a boundary marker, not a tray
                     temperature: the claim is that everything under 25 is gases
                     AND that 25 itself is not. Both limbs are checked, so the
                     word "below" cannot be used to dodge the assertion. */
                  return { label: s, bp, named, below,
                           codeBand: bandOf(below ? bp - 1 : bp),
                           bandAtMark: bandOf(bp) }; });
  });
  globalThis['diag_' + tree] = out;
}
{
  /* Both sides name the same six fractions in slightly different words —
     "fuel oils" on the column, "fuel-oil range" in the code. Reduce each to
     one keyword rather than pattern-matching one string against the other:
     the first cut of this comparator scored "fuel oils" against "fuel-oil
     range" as a disagreement and made release look worse than it is. */
  const KEY = [[/gas/i, 'gases'], [/petrol/i, 'petrol'], [/kerosene/i, 'kerosene'],
               [/diesel/i, 'diesel'], [/fuel.?oil/i, 'fuel-oil'], [/residue/i, 'residue']];
  const key = s => (KEY.find(([re]) => re.test(s)) || [null, '?' + s])[1];
  /* A "below N" label makes two claims and both are checked: N-1 IS the named
     fraction, and N itself is NOT. A plain "N°C" label makes one. */
  const agree = r => r.below ? (key(r.named) === key(r.codeBand) && key(r.named) !== key(r.bandAtMark))
                             : (key(r.named) === key(r.codeBand));
  const summarise = t => (globalThis['diag_' + t] || []).map(r =>
    `${r.below ? 'below ' : ''}${r.bp}°C says "${r.named}", code says "${r.codeBand}"${r.below ? ` (and ${r.bp} itself is "${r.bandAtMark}")` : ''}${agree(r) ? '' : '  <-- disagree'}`);
  const okCount = t => (globalThis['diag_' + t] || []).filter(agree).length;
  const n = (globalThis['diag_' + T_PAT] || []).length;
  /* RULING B. This is no longer "did the patch make it worse" — the five tray
     temperatures were corrected, so the check is now absolute: every printed
     temperature must fall in the band its own label names. Release fails it,
     the fixed build must pass it, and it is the same comparator that caught the
     regression in the first place. */
  pair('W-DIAG', 'every temperature printed on the column falls in the band its own label names',
    okCount(T_REL) === n, okCount(T_PAT) === n,
    `release ${okCount(T_REL)}/${n} agree · patched ${okCount(T_PAT)}/${n} agree`);
  note('W-DIAG-rel', 'the printed temperatures against the RELEASE bands', 'MEASURED', summarise(T_REL).join(' · '));
  note('W-DIAG-pat', 'the printed temperatures against the PATCHED bands', 'MEASURED', summarise(T_PAT).join(' · '));
}

/* Ruling B asks for this limb by name: run the comparison across all
   SELECTABLE FEEDS, not just the five trays. This is the agreement a pupil
   actually sees — the marker lands on a tray, that tray carries a printed
   label, and the readout names a fraction. All three must say one thing. */
for (const tree of TREES) {
  const { out } = await evalIn(tree, WILTON, async (feeds) => {
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    const furn = document.getElementById('wFurnace');
    const labels = [...document.querySelectorAll('#towerW text')]
      .map(t => ({ y: +t.getAttribute('y'), text: t.textContent.trim() }));
    const res = {};
    for (const n of feeds) {
      const btn = document.querySelector(`.feedW[data-feed="${n}"]`);
      if (!btn) { res[n] = { button: false }; continue; }
      btn.click();
      furn.value = furn.max; furn.dispatchEvent(new Event('input', { bubbles: true }));
      await sleep(50);
      document.getElementById('runDistil').click();
      await sleep(80);
      const cy = +document.getElementById('condenseW').getAttribute('cy');
      /* the printed label for the tray the marker is standing on: the nearest
         label at or below the marker, within one tray's spacing */
      const near = labels.filter(l => l.y >= cy - 6 && l.y - cy < 40).sort((a, b) => a.y - b.y)[0];
      res[n] = { button: true, cy, markerLabel: near ? near.text : null,
                 readout: (document.getElementById('wTrayRead').textContent || '').trim(),
                 distilled: /condensed in the/.test(document.getElementById('wDistilResult').textContent || '') };
    }
    return res;
  }, REACHABLE);
  globalThis['mk_' + tree] = out;
}
{
  const KEY = [[/gas/i, 'gases'], [/petrol/i, 'petrol'], [/kerosene/i, 'kerosene'],
               [/diesel/i, 'diesel'], [/fuel.?oil/i, 'fuel-oil'], [/residue/i, 'residue']];
  const key = s => (KEY.find(([re]) => re.test(s || '')) || [null, '?'])[1];
  const judged = t => REACHABLE.map(n => {
    const r = (globalThis['mk_' + t] || {})[n];
    if (!r || !r.button) return { n, verdict: 'no button' };
    if (!r.distilled) return { n, verdict: 'not distilled' };
    const ok = key(r.markerLabel) === key(r.readout);
    return { n, ok, verdict: `marker on "${r.markerLabel}" / readout "${r.readout}"${ok ? '' : '  <-- disagree'}` };
  });
  const scored = t => judged(t).filter(j => j.ok !== undefined);
  const okOf = t => scored(t).filter(j => j.ok).length;
  pair('W-DIAG-MARK', 'for every distillable feed, the tray the marker lands on and the readout name the same fraction',
    scored(T_REL).length > 0 && okOf(T_REL) === scored(T_REL).length,
    scored(T_PAT).length > 0 && okOf(T_PAT) === scored(T_PAT).length,
    `release ${okOf(T_REL)}/${scored(T_REL).length} agree · patched ${okOf(T_PAT)}/${scored(T_PAT).length} agree`,
    'ALREADY CONSISTENT ON RELEASE');
  note('W-DIAG-MARK-rel', 'marker vs readout, per feed, on RELEASE', 'MEASURED',
    judged(T_REL).map(j => `C${j.n}: ${j.verdict}`).join(' · '));
  note('W-DIAG-MARK-pat', 'marker vs readout, per feed, on the fixed build', 'MEASURED',
    judged(T_PAT).map(j => `C${j.n}: ${j.verdict}`).join(' · '));
}

/* T10 — the refusal message. Two situations, two sentences, and the wrong
   sentence in the wrong place would be a false statement to a pupil. */
for (const tree of TREES) {
  const { out } = await evalIn(tree, WILTON, async () => {
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    const furn = document.getElementById('wFurnace');
    const run = async (feed, furnace) => {
      const b = document.querySelector(`.feedW[data-feed="${feed}"]`);
      if (!b) return null;
      b.click();
      furn.value = String(furnace); furn.dispatchEvent(new Event('input', { bubbles: true }));
      await sleep(50);
      document.getElementById('runDistil').click();
      await sleep(80);
      return (document.getElementById('wDistilResult').textContent || '').trim();
    };
    return { ceiling: await run(24, +furn.max), lowFurnace: await run(14, +furn.min), furnMax: +furn.max, furnMin: +furn.min };
  });
  globalThis['msg_' + tree] = out;
}
{
  const R = globalThis['msg_' + T_REL], P = globalThis['msg_' + T_PAT];
  const teaches = m => !!m && /never enters the vapour stream/.test(m) && /residue/.test(m) && /430/.test(m) && /390/.test(m);
  pair('T10a', 'a feed this column can never boil is told why, and where it goes instead',
    R.ceiling === null ? false : teaches(R.ceiling), teaches(P.ceiling),
    `release ${JSON.stringify(R.ceiling)} -> patched ${JSON.stringify(P.ceiling)}`);
  /* the guard against over-applying the new sentence */
  const honest = m => !!m && !/never enters the vapour stream/.test(m) && /raise it/i.test(m);
  pair('T10b', 'a furnace merely turned down is told to turn it up, NOT that the column can never do it',
    honest(R.lowFurnace), honest(P.lowFurnace),
    `at furnace ${P.furnMin}°C on C14 — release ${JSON.stringify(R.lowFurnace)} -> patched ${JSON.stringify(P.lowFurnace)}`);
}

/* T12 — the caption Ruling B calls not optional */
for (const tree of TREES) {
  const { out } = await evalIn(tree, WILTON, () => {
    const c = document.getElementById('wTrayCaption');
    if (!c) return { present: false };
    const r = c.getBoundingClientRect();
    return { present: true, rendered: r.width > 0 && r.height > 0,
             text: c.textContent.replace(/\s+/g, ' ').trim() };
  });
  globalThis['cap_' + tree] = out;
}
{
  const ok = c => !!c.present && c.rendered && /Tray temperature/.test(c.text) && /Boiling range/.test(c.text);
  pair('T12', 'the column carries a rendered caption separating tray temperature from boiling range',
    ok(globalThis['cap_' + T_REL]), ok(globalThis['cap_' + T_PAT]),
    `release ${JSON.stringify(globalThis['cap_' + T_REL])} -> patched present=${globalThis['cap_' + T_PAT].present} rendered=${globalThis['cap_' + T_PAT].rendered}`);
}

/* =====================================================================
 * §D  three-way feed identity
 * ===================================================================== */
for (const tree of TREES) {
  const { out: fromLab } = await evalIn(tree, WILTON, () =>
    [...document.querySelectorAll('.feedW')].map(b => +b.dataset.feed));
  /* the Random array, exercised rather than read: click it enough times that
     omitting a member would be a 1-in-10^30 accident */
  const { out: fromRandom } = await evalIn(tree, WILTON, () => {
    const seen = new Set();
    for (let i = 0; i < 400; i++) { document.getElementById('randomFeed').click(); seen.add(document.getElementById('wFeedRead').textContent); }
    return [...seen].map(s => +String(s).match(/^C(\d+)/)[1]).sort((a, b) => a - b);
  });
  const { out: fromStudio } = await evalIn(tree, STUDIO, () => {
    const e = document.getElementById('engine');
    e.value = 'wilton-carbon-control'; e.dispatchEvent(new Event('change', { bubbles: true }));
    const sel = document.querySelector('[data-scenario="feed"]');
    return sel ? [...sel.options].map(o => +o.value) : null;
  });
  globalThis['id_' + tree] = { lab: fromLab, random: fromRandom, studio: fromStudio };
}
const eq = (a, b) => a && b && a.length === b.length && a.every((x, i) => x === b[i]);
const IR = globalThis['id_' + T_REL], IP = globalThis['id_' + T_PAT];
const three = I => eq(I.lab, I.random) && eq(I.lab, I.studio);
const inAllThree = (I, n) => I.lab.includes(n) && I.random.includes(n) && (I.studio || []).includes(n);
pair('W-ID24', 'both new feeds, C21 and C24, are present in all three feed lists',
  inAllThree(IR, 21) && inAllThree(IR, 24),
  inAllThree(IP, 21) && inAllThree(IP, 24),
  `release buttons[${IR.lab}] random[${IR.random}] studio[${IR.studio}] -> patched buttons[${IP.lab}] random[${IP.random}] studio[${IP.studio}]`);
note('W-ID3', 'the three feed lists are the same set (identity re-asserted)',
  three(IP) ? 'ASSERTED' : 'DIVERGED',
  `patched buttons[${IP.lab}] == random[${IP.random}] == studio[${IP.studio}] · release was ${three(IR) ? 'also identical' : 'DIVERGENT'}`);

/* =====================================================================
 * §E  the rest of P2, unchanged in intent from the earlier pass
 * ===================================================================== */
for (const tree of TREES) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const pg = await ctx.newPage();
  await pg.goto('file://' + path.resolve(ROOT, tree, LABS[0]), { waitUntil: 'domcontentloaded', timeout: 45000 });
  await pg.waitForTimeout(800);
  const typed = await pg.evaluate(() => {
    const t = document.querySelector('textarea'); if (!t) return null;
    t.value = 'PUPIL-DATA-CANARY';
    t.dispatchEvent(new Event('input', { bubbles: true }));
    t.dispatchEvent(new Event('change', { bubbles: true }));
    return t.id || t.className || 'textarea';
  });
  await pg.waitForTimeout(700);
  await pg.reload({ waitUntil: 'domcontentloaded' });
  await pg.waitForTimeout(900);
  const back = await pg.evaluate(() => [...document.querySelectorAll('textarea')].some(t => /PUPIL-DATA-CANARY/.test(t.value)));
  const keys = await pg.evaluate(() => { try { return Object.keys(localStorage); } catch (e) { return ['(blocked)']; } });
  globalThis['p_' + tree] = { typed, back, keys };
  await ctx.close();
}
pair('P2.2a', 'pupil text does NOT survive a reload (memory-only ruling)',
  !globalThis['p_' + T_REL].back, !globalThis['p_' + T_PAT].back,
  `release returned=${globalThis['p_' + T_REL].back} -> patched returned=${globalThis['p_' + T_PAT].back} (field ${globalThis['p_' + T_REL].typed})`);
note('P2.2b', 'localStorage keys after a session', 'MEASURED',
  `release [${globalThis['p_' + T_REL].keys}] -> patched [${globalThis['p_' + T_PAT].keys}]`);

/* P2.2c  the storage surface, call by call.
 * "Nothing came back after a reload" is one control watching three separate
 * removals: the boot read, the write, and the explicit clear mask each other,
 * so any one of them could be reverted with that control still green. This
 * records every localStorage call the page makes instead, which distinguishes
 * them. A full session is driven, including the Reset button, so the clear
 * path is exercised rather than assumed. */
for (const tree of TREES) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const pg = await ctx.newPage();
  /* Records are collected OUTSIDE the page. The first cut kept them in a page
     global and lost the whole clear path: resetSession() ends in
     location.reload(), which replaced the document and took the array with it.
     The removeItem had happened; the evidence of it had not survived. */
  const calls = [];
  await pg.exposeFunction('__rec', s => { calls.push(s); });
  await pg.addInitScript(() => {
    const real = window.localStorage;
    const rec = (op, key) => { try { window.__rec(op + ':' + key); } catch (e) {} };
    Object.defineProperty(window, 'localStorage', { configurable: true, value: {
      getItem(k) { rec('get', k); return real.getItem(k); },
      setItem(k, v) { rec('set', k); return real.setItem(k, v); },
      removeItem(k) { rec('remove', k); return real.removeItem(k); },
      clear() { rec('clear', '*'); return real.clear(); },
      key(i) { return real.key(i); },
      get length() { return real.length; },
    }});
    window.confirm = () => true;                       // resetSession asks first
  });
  await pg.goto('file://' + path.resolve(ROOT, tree, LABS[0]), { waitUntil: 'domcontentloaded', timeout: 45000 });
  await pg.waitForTimeout(800);
  await pg.evaluate(() => {
    const t = document.querySelector('textarea');
    if (t) { t.value = 'PUPIL-DATA-CANARY'; t.dispatchEvent(new Event('input', { bubbles: true })); t.dispatchEvent(new Event('change', { bubbles: true })); }
  });
  await pg.waitForTimeout(500);
  const marker = calls.length;
  await pg.evaluate(() => { const b = document.getElementById('resetSession'); if (b) b.click(); });
  await pg.waitForTimeout(1200);                       // resetSession reloads; let the new document boot
  globalThis['ls_' + tree] = calls.slice();
  globalThis['lsReset_' + tree] = calls.slice(marker);
  await ctx.close();
}
{
  const kinds = (c, op) => c.filter(x => x.startsWith(op + ':') && !/:mbm_/.test(x));
  const r = globalThis['ls_' + T_REL], p = globalThis['ls_' + T_PAT];
  for (const [op, tid] of [['get', 'T1'], ['set', 'T2'], ['remove', 'T3']]) {
    pair(`P2.2c-${op}`, `no localStorage.${op}Item under this lab's own key, across a full session (${tid})`,
      kinds(r, op).length === 0, kinds(p, op).length === 0,
      `release [${kinds(r, op)}] -> patched [${kinds(p, op)}]`);
  }
  note('P2.2c-all', 'every localStorage call recorded, both trees', 'MEASURED',
    `release [${r}] -> patched [${p}]`);
}

/* The subject is the EXPORTED FILE, not csvCell. csvCell exists only on the
   patched side — measuring it would make the release limb "unreachable" and the
   pair would compare nothing. The .csv a teacher opens in Excel exists on both
   trees, so that is what gets measured, through the real export button. */
for (const tree of TREES) {
  const { out } = await evalIn(tree, STUDIO, async () => {
    const grab = [];
    const orig = URL.createObjectURL.bind(URL);
    URL.createObjectURL = b => { grab.push(b); return orig(b); };
    document.getElementById('demoData').click();
    await new Promise(r => setTimeout(r, 400));
    if (typeof S === 'undefined' || !S.capsules || !S.capsules.length) return { unreachable: 'no capsules to export' };
    S.capsules[0].learner = Object.assign({}, S.capsules[0].learner, { alias: '=1+1' });
    S.capsules[1].learner = Object.assign({}, S.capsules[1].learner, { alias: '@SUM(A1)' });
    document.getElementById('exportCSV').click();
    await new Promise(r => setTimeout(r, 400));
    if (!grab.length) return { unreachable: 'export produced no blob' };
    const text = await grab[grab.length - 1].text();
    const cells = text.split('\n').flatMap(l => l.split(','));
    return { formulaLive: cells.filter(c => /^"[=+\-@]/.test(c)), inert: cells.filter(c => /^"'[=+\-@]/.test(c)) };
  });
  globalThis['c_' + tree] = out;
}
const CRel = globalThis['c_' + T_REL], CPat = globalThis['c_' + T_PAT];
/* "export produced no blob" is not an unreachable subject — it is a broken
   export, which is a failure. Only "no capsules to export" would leave the
   subject genuinely out of reach. */
const safeCsv = o => o.unreachable === 'no capsules to export' ? 'UNREACHABLE'
                   : o.unreachable ? false
                   : (o.formulaLive.length === 0 && o.inert.length >= 2);
pair('P2.3', 'the exported .csv carries no cell that Excel would evaluate',
  safeCsv(CRel), safeCsv(CPat),
  `release live${JSON.stringify(CRel.formulaLive || CRel)} inert${JSON.stringify(CRel.inert || [])} -> patched live${JSON.stringify(CPat.formulaLive || CPat)} inert${JSON.stringify(CPat.inert || [])}`);

for (const tree of TREES) {
  const { out } = await evalIn(tree, LABS[0], () =>
    ({ seeded: document.body.classList.contains('calm'), toggle: !!document.getElementById('calmToggle') }),
    null, { reducedMotion: 'reduce' });
  globalThis['m_' + tree] = out;
}
pair('P2.4', 'body.calm is seeded from prefers-reduced-motion at boot',
  globalThis['m_' + T_REL].seeded, globalThis['m_' + T_PAT].seeded,
  `manual toggle still present: release ${globalThis['m_' + T_REL].toggle} / patched ${globalThis['m_' + T_PAT].toggle}`);

for (const tree of TREES) {
  const src = fs.readFileSync(path.join(ROOT, tree, STUDIO), 'utf8');
  globalThis['h_' + tree] = (src.match(/ on(click|change|input|submit|keydown)=/g) || []).length;
}
pair('P2.5a', 'zero inline handlers in the Studio source',
  globalThis['h_' + T_REL] === 0, globalThis['h_' + T_PAT] === 0,
  `release ${globalThis['h_' + T_REL]} -> patched ${globalThis['h_' + T_PAT]}`);

for (const tree of TREES) {
  const { out } = await evalIn(tree, STUDIO, async () => {
    document.getElementById('demoData').click();
    await new Promise(r => setTimeout(r, 400));
    const b = document.querySelector('#capsuleRows button');
    if (!b) return { rows: 0, opened: false };
    b.click();
    await new Promise(r => setTimeout(r, 300));
    return { rows: document.querySelectorAll('#capsuleRows tr').length,
             opened: document.getElementById('detailContent').style.display === 'block' };
  });
  globalThis['v_' + tree] = out;
}
note('P2.5b', 'View still opens the capsule detail after rebinding',
  globalThis['v_' + T_PAT].opened ? 'BEHAVIOUR PRESERVED' : 'BROKEN',
  `release opened=${globalThis['v_' + T_REL].opened} rows=${globalThis['v_' + T_REL].rows} -> patched opened=${globalThis['v_' + T_PAT].opened} rows=${globalThis['v_' + T_PAT].rows}`);

/* =====================================================================
 * §F  ESTATE INTEGRATION — T13, T14, T15
 * ===================================================================== */
for (const tree of TREES) {
  const { out } = await evalIn(tree, WILTON, () => {
    const nav = document.querySelector('a.mbmhome');
    const note = document.getElementById('wModelNote');
    const r = nav && nav.getBoundingClientRect();
    return {
      navHref: nav ? nav.getAttribute('href') : null,
      navLabel: nav ? nav.getAttribute('aria-label') : null,
      navText: nav ? nav.textContent.trim() : null,
      /* NOT "has a non-zero box". An unstyled inline link has one of those, which
         is how the first cut of this control passed on a NAV-1 that had the
         markup and none of the rule that makes it usable. */
      navBox: r ? { w: Math.round(r.width), h: Math.round(r.height) } : null,
      navTarget44: !!(r && r.width >= 44 && r.height >= 44),
      navPrintHidden: (() => {
        if (!nav) return null;
        for (const sheet of document.styleSheets) {
          let rules; try { rules = sheet.cssRules; } catch (e) { continue; }
          for (const rule of rules)
            if (rule.media && /print/.test(rule.conditionText || rule.media.mediaText || '') &&
                [...(rule.cssRules || [])].some(r2 => /\.mbmhome/.test(r2.selectorText || '') && /none/.test(r2.style.display)))
              return true;
        }
        return false;
      })(),
      navFocusRing: (() => {
        for (const sheet of document.styleSheets) {
          let rules; try { rules = sheet.cssRules; } catch (e) { continue; }
          for (const rule of rules) if (/\.mbmhome:focus-visible/.test(rule.selectorText || '')) return true;
        }
        return false;
      })(),
      navRendered: !!(r && r.width > 0 && r.height > 0),
      modelNote: note ? note.textContent.replace(/\s+/g, ' ').trim() : null,
      modelRendered: !!(note && note.getBoundingClientRect().height > 0),
    };
  });
  globalThis['est_' + tree] = out;
  const srcs = [STUDIO, ...LABS].map(f => fs.readFileSync(path.join(ROOT, tree, f), 'utf8'));
  globalThis['brand_' + tree] = srcs.map(s2 => (s2.match(/Made by Matt/g) || []).length);
  globalThis['nav_' + tree] = LABS.map(f =>
    (fs.readFileSync(path.join(ROOT, tree, f), 'utf8').match(/<a class="mbmhome"[^>]*>/g) || []).length);
}
{
  const R = globalThis['est_' + T_REL], P = globalThis['est_' + T_PAT];
  /* byte-identical to the eleven lessons it co-locates with, not merely present */
  const HREF = '../../../index.html', LABEL = 'Back to the Lessons catalogue';
  const navOk = x => x.navHref === HREF && x.navLabel === LABEL && x.navRendered
                  && x.navTarget44 && x.navPrintHidden === true && x.navFocusRing === true;
  pair('T13', 'NAV-1 matches the eleven neighbours: same href and label, a 44px target, a focus ring, and gone from print',
    navOk(R), navOk(P),
    `release ${JSON.stringify({ href: R.navHref })} -> staging href "${P.navHref}" label "${P.navLabel}" ` +
    `box ${JSON.stringify(P.navBox)} 44px=${P.navTarget44} focus-ring=${P.navFocusRing} print-hidden=${P.navPrintHidden}`);
  note('T13-scope', 'the Studio is deliberately excluded from NAV-1', 'ASSERTED',
    `it deploys to Matt-s-Apps-, not Lessons, so a link to the Lessons catalogue would be wrong from it. ` +
    `labs carrying NAV-1: release [${globalThis['nav_' + T_REL]}] -> staging [${globalThis['nav_' + T_PAT]}]`);

  /* THE REGRESS TRAP, re-expressed rather than deleted. The release build has
     zero "Made by Matt"; the deployed build must have exactly one per page.
     Neither figure is hardcoded as "the answer" — both are asserted. */
  const allZero = a => a.every(n => n === 0);
  const allOne = a => a.every(n => n === 1);
  pair('T14', 'exactly one "Made by Matt" per page — release baseline 0, deployed expectation 1',
    allZero(globalThis['brand_' + T_REL]) && false, allOne(globalThis['brand_' + T_PAT]),
    `release per-page counts [${globalThis['brand_' + T_REL]}] · staging [${globalThis['brand_' + T_PAT]}]`);
  rows.pop();
  note('T14', 'exactly one "Made by Matt" per page — the regress trap, re-expressed not deleted',
    allZero(globalThis['brand_' + T_REL]) && allOne(globalThis['brand_' + T_PAT]) ? 'BOTH LIMBS ASSERTED' : 'FAILED',
    `release per-page counts [${globalThis['brand_' + T_REL]}] (baseline, all 0) · ` +
    `staging [${globalThis['brand_' + T_PAT]}] (deployed, all 1). ` +
    `Any harness asserting "Made by Matt" == 0 must be re-expressed against the deployed build, not satisfied by dropping the branding.`);
  if (!(allZero(globalThis['brand_' + T_REL]) && allOne(globalThis['brand_' + T_PAT]))) rows[rows.length - 1].verdict = 'FAILED';

  const discloses = x => !!x.modelNote && /model values, not measurements/i.test(x.modelNote)
    && /overlap/i.test(x.modelNote) && /C14 to C16/i.test(x.modelNote) && x.modelRendered;
  pair('T15', 'the lab says its temperature scale is a model, gives the real overlapping ranges, and names the C14–C16 overlap',
    discloses(R), discloses(P),
    `release ${R.modelNote === null ? 'no such note' : 'present'} -> staging "${(P.modelNote || '').slice(0, 150)}…"`);
}

await browser.close();

/* ---------------------------------------------------------------- report */
const W = [9, 12, 12];
console.log(`${'id'.padEnd(W[0])} ${'release'.padEnd(W[1])} ${'patched'.padEnd(W[2])} verdict`);
console.log('-'.repeat(78));
for (const r of rows) {
  console.log(`${r.id.padEnd(W[0])} ${String(r.release).padEnd(W[1])} ${String(r.patched).padEnd(W[2])} ${r.verdict}`);
  console.log(`          ${r.what}`);
  if (r.detail) console.log(`          ${r.detail}`);
}
const bad = rows.filter(r => ['NOT A CONTROL', 'BROKEN', 'FAILED', 'CHANGED — HARD STOP', 'COLLISION',
                              'DIVERGED', 'PAGE ERROR', 'REGRESSION'].includes(r.verdict));
const unreachable = rows.filter(r => r.verdict === 'UNREACHABLE');
/* An unreachable subject is inconclusive ONLY when nobody accounted for it.
   C24 is unreachable BY DESIGN and W-DESIGN asserts the declared set is exactly
   the undistillable set, so it stays reported as UNREACHABLE without holding
   the suite at exit 2 forever — a gate that can never go green stops being a
   signal. An unreachable row nobody declared still exits 2. */
const declaredU = unreachable.filter(r => r.declared);
const undeclaredU = unreachable.filter(r => !r.declared);
console.log(`\n${bad.length} failure(s); ${undeclaredU.length} undeclared unreachable; ` +
  `${declaredU.length} declared unreachable by design [${declaredU.map(r => r.id).join(', ') || 'none'}]`);
process.exit(bad.length ? 1 : undeclaredU.length ? 2 : 0);
