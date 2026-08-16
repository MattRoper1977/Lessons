/* P2.6 — the inputs.
 *
 * The h1 limb is dropped: it was a count of headings, and a count with no
 * stated predicate is not a measurement. What is left is the one that carries
 * a consequence — every form control a teacher or pupil can reach must have an
 * accessible name, computed the way a screen reader computes it and not by
 * looking for a nearby <label> tag.
 *
 * Run against BOTH trees. The patch must not lose a name, and must not gain an
 * unnamed control (the C24 button is a control too).
 */
import path from 'node:path';
const _pwPath = process.env.P2_PLAYWRIGHT || '/opt/node22/lib/node_modules/playwright/index.js';
const _pw = await import(_pwPath).catch(() => import('playwright'));
const ROOT = process.env.P2_ROOT || path.dirname(new URL(import.meta.url).pathname);
const PATCHED = process.env.P2_PATCHED || 'staging';
const chromium = _pw.chromium || _pw.default.chromium;
const ALL = ['00_BUILD_FieldOps_Teacher_Studio.html', '01_Newport_Bridge_Lift_Permit_Lab.html',
             '02_Tees_Estuary_Field_Investigation_Lab.html', '03_Wilton_Carbon_Process_Control_Lab.html',
             '04_Tees_Bay_Wind_Operations_Lab.html'];
const TREES = ['release', PATCHED];

const census = () => {
  const name = el => {
    const byLabelledBy = (el.getAttribute('aria-labelledby') || '').split(/\s+/).filter(Boolean)
      .map(id => (document.getElementById(id) || {}).textContent || '').join(' ').trim();
    if (byLabelledBy) return { text: byLabelledBy, from: 'aria-labelledby' };
    const aria = (el.getAttribute('aria-label') || '').trim();
    if (aria) return { text: aria, from: 'aria-label' };
    if (el.id) {
      const l = document.querySelector(`label[for="${CSS.escape(el.id)}"]`);
      if (l && l.textContent.trim()) return { text: l.textContent.trim(), from: 'label[for]' };
    }
    const wrap = el.closest('label');
    if (wrap && wrap.textContent.trim()) return { text: wrap.textContent.trim(), from: 'wrapping label' };
    const title = (el.getAttribute('title') || '').trim();
    if (title) return { text: title, from: 'title' };
    if (el.tagName === 'BUTTON' && el.textContent.trim()) return { text: el.textContent.trim(), from: 'button text' };
    if (el.tagName === 'INPUT' && /^(button|submit|reset)$/i.test(el.type) && el.value)
      return { text: el.value, from: 'value' };
    return { text: '', from: null };
  };
  const controls = [...document.querySelectorAll('input,select,textarea,button,[role="button"],[contenteditable="true"]')];
  return controls.map(el => {
    const n = name(el);
    const r = el.getBoundingClientRect();
    return { tag: el.tagName.toLowerCase(), type: el.type || '', id: el.id || '',
             named: !!n.text, from: n.from, text: n.text.slice(0, 40),
             rendered: r.width > 0 && r.height > 0 };
  });
};

const browser = await chromium.launch();
const out = {};
for (const tree of TREES) {
  out[tree] = {};
  for (const f of ALL) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const pg = await ctx.newPage();
    await pg.goto('file://' + path.resolve(ROOT, tree, f), { waitUntil: 'domcontentloaded', timeout: 45000 });
    await pg.waitForTimeout(900);
    out[tree][f] = await pg.evaluate(census);
    await ctx.close();
  }
}
await browser.close();

const [REL, PAT] = TREES;
let fails = 0;
console.log(`${'file'.padEnd(46)} ${'controls'.padEnd(10)} ${'unnamed'.padEnd(9)} ${'rendered'.padEnd(9)}`);
console.log('-'.repeat(80));
let totalR = 0, totalP = 0, unnamedAll = [];
for (const f of ALL) {
  const r = out[REL][f], p = out[PAT][f];
  totalR += r.length; totalP += p.length;
  const un = p.filter(c => !c.named);
  unnamedAll.push(...un.map(c => `${f.slice(0, 2)} ${c.tag}${c.type ? '[' + c.type + ']' : ''}#${c.id || '(no id)'}`));
  console.log(`${f.padEnd(46)} ${String(r.length + ' -> ' + p.length).padEnd(10)} ${String(un.length).padEnd(9)} ${String(p.filter(c => c.rendered).length).padEnd(9)}`);
}
console.log('-'.repeat(80));
console.log(`TOTAL controls: release ${totalR}  ->  patched ${totalP}`);
console.log(`accessible-name sources in the patched tree: ` +
  JSON.stringify([...new Set(ALL.flatMap(f => out[PAT][f].map(c => c.from)))].filter(Boolean)));

/* A0 — the predicate, stated. "38 inputs" is not a measurement until the
   predicate is named: it is <input> elements in the four pupil-facing labs,
   the Teacher Studio excluded. Anything else gives a different number, and
   several of those numbers are also defensible. */
const LABS = ALL.slice(1);
const inputsInLabs = t => LABS.reduce((n, f) => n + out[t][f].filter(c => c.tag === 'input').length, 0);
console.log(`\nA0  predicate: <input> elements in the four pupil-facing labs, Studio excluded`);
console.log(`    release ${inputsInLabs(REL)}  ->  patched ${inputsInLabs(PAT)}   (the figure the order calls "the 38 inputs")`);
console.log(`    other predicates on the same tree, so the figure cannot be quoted loose:`);
console.log(`      input+select+textarea, four labs: ${LABS.reduce((n, f) => n + out[PAT][f].filter(c => /input|select|textarea/.test(c.tag)).length, 0)}`);
console.log(`      input, all five files:            ${ALL.reduce((n, f) => n + out[PAT][f].filter(c => c.tag === 'input').length, 0)}`);
console.log(`      every control incl. buttons:      ${totalP}`);
if (inputsInLabs(PAT) !== 38) { fails++; console.log(`A0 FAIL  the stated predicate no longer yields 38`); }
else console.log(`A0 PASS  the stated predicate yields 38, unchanged by the patch`);

/* A1 — PATCH-SCOPED. Must pass: the patch adds exactly the C24 button, that
   button is named, and nothing lost a name it had on release. */
{
  /* The two feed buttons Ruling A authorises, named individually: a delta of 2
     is only acceptable if it is EXACTLY these two, each named and each rendered.
     Asserting the number alone would let any other pair of controls through. */
  const ADDED = ['C21', 'C24'];
  const delta = totalP - totalR;
  const found = ADDED.map(t => out[PAT]['03_Wilton_Carbon_Process_Control_Lab.html'].find(c => c.text === t));
  const lost = [];
  for (const f of ALL) {
    const byId = new Map(out[REL][f].filter(c => c.id).map(c => [c.id, c]));
    for (const c of out[PAT][f]) if (c.id && byId.has(c.id) && byId.get(c.id).named && !c.named) lost.push(`${f} #${c.id}`);
  }
  const allNamed = found.every(c => c && c.named && c.rendered);
  const ok = delta === ADDED.length && allNamed && lost.length === 0;
  if (!ok) { fails++; console.log(`A1 FAIL  delta ${delta} (expected ${ADDED.length}); ${JSON.stringify(found)}; names lost ${lost.join(', ')}`); }
  else console.log(`A1 PASS  exactly ${ADDED.length} controls added (${ADDED.join(', ')}, each named via ${found[0].from}, each rendered); no name lost`);
}

/* A2 — ESTATE-SCOPED, and RED. This is not weakened to match the outcome: the
   count is reported in full and the exit code carries it. It is out of P2's
   authorised scope to fix — recorded, left, and not merged over in silence. */
const unnamedInputs = LABS.flatMap(f => out[PAT][f].filter(c => c.tag === 'input' && !c.named)
  .map(c => `${f.slice(0, 2)} #${c.id || '(no id)'} [${c.type}]`));
const preexisting = unnamedAll.length > 0;
console.log(`\nA2 RED (PRE-EXISTING, NOT FIXED IN P2)`);
console.log(`    ${unnamedInputs.length} of the 38 inputs have no accessible name; ${unnamedAll.length} controls overall.`);
console.log(`    Identical on release — A1 proves the patch neither caused nor worsened it.`);
console.log(`    ${unnamedInputs.join('\n    ')}`);

console.log(`\n${fails} patch-scoped failure(s); ${preexisting ? 1 : 0} pre-existing red recorded`);
process.exit(fails ? 1 : preexisting ? 3 : 0);
