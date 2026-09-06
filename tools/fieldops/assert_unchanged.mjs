/* §2.4 assert-unchanged, re-run against the new build.
 *
 * The question this answers is not "did the fixes work" — the control set
 * answers that. It is the other half: did anything ELSE move. Two content
 * changes are authorised in P2 (the C24 feed, the residue relabel). Everything
 * else a pupil or a teacher can see must be the same as release.
 */
import fs from 'node:fs'; import path from 'node:path'; import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
const _pwPath = process.env.P2_PLAYWRIGHT || '/opt/node22/lib/node_modules/playwright/index.js';
const _pw = await import(_pwPath).catch(() => import('playwright'));
const ROOT = process.env.P2_ROOT || path.dirname(new URL(import.meta.url).pathname);
const PATCHED = process.env.P2_PATCHED || 'staging';
const chromium = _pw.chromium || _pw.default.chromium;

const ALL = ['00_BUILD_FieldOps_Teacher_Studio.html', '01_Newport_Bridge_Lift_Permit_Lab.html',
             '02_Tees_Estuary_Field_Investigation_Lab.html', '03_Wilton_Carbon_Process_Control_Lab.html',
             '04_Tees_Bay_Wind_Operations_Lab.html'];
const WILTON = '03_Wilton_Carbon_Process_Control_Lab.html';
const STUDIO = '00_BUILD_FieldOps_Teacher_Studio.html';
const TRANSFORMS = ['T1','T2','T3','T4','T5a','T5b','T6a','T6b','T7','T8a','T8b','T8c','T9','T10','T11','T12','T13','T14','T15','T16'];
const rows = [];
const row = (id, what, ok, detail) => rows.push({ id, what, ok, detail });
const sha = s => crypto.createHash('sha256').update(s).digest('hex').slice(0, 16);

/* -- U1  the build is release plus exactly the named transforms ------------
   Drop them all and the builder must hand back release, byte for byte.
   Nothing else the builder does can then be hiding in the shipped tree. */
execFileSync('node', ['build.mjs', `--drop=${TRANSFORMS.join(',')}`, '--out=work/nulltree'],
  { cwd: ROOT, stdio: 'pipe' });
{
  const bad = ALL.filter(f =>
    fs.readFileSync(path.join(ROOT,'release',f), 'utf8') !== fs.readFileSync(path.join(ROOT,'work','nulltree',f), 'utf8'));
  row('U1', `with all ${TRANSFORMS.length} transforms dropped the builder reproduces release byte for byte`,
    bad.length === 0, bad.length ? `differs: ${bad}` : `all ${ALL.length} files identical, ${TRANSFORMS.length} transforms dropped`);
}

/* -- U2  no transform touched a file it was not declared against ----------- */
{
  const touched = {}, dependent = {};
  for (const T of TRANSFORMS) {
    try {
      execFileSync('node', ['build.mjs', `--drop=${TRANSFORMS.filter(x => x !== T).join(',')}`, `--out=work/only_${T}`],
        { cwd: ROOT, stdio: 'pipe' });
    } catch (e) {
      /* A transform whose anchor is text ANOTHER transform introduces cannot be
         built alone. That is a real dependency, not a defect, and it is the same
         distinction R0.11 draws about reds: report it, do not crash on it, and do
         not fold the two transforms together merely to make this loop succeed. */
      dependent[T] = 'cannot build in isolation';
      fs.rmSync(path.join(ROOT, 'work', 'only_' + T), { recursive: true, force: true });
      continue;
    }
    touched[T] = ALL.filter(f =>
      fs.readFileSync(path.join(ROOT,'release',f), 'utf8') !== fs.readFileSync(path.join(ROOT,'work','only_'+T,f), 'utf8'));
    fs.rmSync(path.join(ROOT,'work','only_'+T), { recursive: true, force: true });
  }
  const DECLARED = {
    T1: 4, T2: 4, T3: 4, T4: 5, T5a: 1, T5b: 1, T6a: 1, T6b: 1, T7: 1, T8a: 1, T8b: 1, T8c: 1, T9: 1,
    T10: 1, T11: 1, T12: 1, T13: 4, T14: 5, T15: 1,
    /* T16 rewrites the four engine entries in the Studio, so it applies four
       times against ONE file — the same shape as T13, which swaps twice per lab
       under a single id. Declared by files touched, not by applications. */
    T16: 1,
  };
  const buildable = TRANSFORMS.filter(T => !(T in dependent));
  const wrong = buildable.filter(T => touched[T].length !== DECLARED[T]);
  row('U2', 'each independently-buildable transform changes exactly the files it is declared against',
    wrong.length === 0,
    (wrong.length ? wrong.map(T => `${T} touched ${touched[T].length}, declared ${DECLARED[T]}`).join(' · ')
                  : buildable.map(T => `${T}:${touched[T].length}`).join(' ')) +
    (Object.keys(dependent).length
      ? ` · DEPENDENT, not measured alone: ${Object.keys(dependent).join(', ')}`
      : ''));
  row('U2b', 'every dependent transform is one whose anchor another transform introduces',
    Object.keys(dependent).every(T => T === 'T15'),
    Object.keys(dependent).length
      ? `${Object.keys(dependent).join(', ')} — T15's anchor is the caption T12 adds, so it cannot be built alone. Declared, not folded into T12: they are separate rulings and folding them would cost the ability to test them apart.`
      : 'none');
}

/* -- U3  every file still parses and boots without a page error ------------ */
const browser = await chromium.launch();
async function boot(tree, file, fn) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const pg = await ctx.newPage();
  const errs = []; pg.on('pageerror', e => errs.push(String(e).slice(0, 140)));
  await pg.goto('file://' + path.resolve(ROOT, tree, file), { waitUntil: 'domcontentloaded', timeout: 45000 });
  await pg.waitForTimeout(900);
  const out = fn ? await pg.evaluate(fn) : null;
  await ctx.close();
  return { out, errs };
}
{
  const errs = [];
  for (const f of ALL) {
    const r = await boot(PATCHED, f);
    if (r.errs.length) errs.push(`${f}: ${r.errs.join(' | ')}`);
  }
  row('U3', 'all five files boot with no page error', errs.length === 0, errs.length ? errs.join(' || ') : 'clean');
}

/* -- U4  the visible taught text, word for word ---------------------------
   Only the two authorised content changes may appear in this delta. */
const visible = () => {
  const walk = document.body;
  const t = [];
  for (const n of walk.querySelectorAll('*')) {
    if (/^(SCRIPT|STYLE)$/.test(n.tagName)) continue;
    for (const c of n.childNodes)
      if (c.nodeType === 3 && c.textContent.trim()) t.push(c.textContent.trim().replace(/\s+/g, ' '));
  }
  return t;
};
/* The Studio's mission card prints a digest taken over an object that carries
   created: new Date().toISOString(). It therefore differs between any two page
   loads, release against release included — measured, not assumed. Masking the
   digest only; the mission id in front of it is NOT masked, and U5 asserts that
   id separately, so a real transport change still shows. */
const DIGEST = / · [0-9a-f]{12}$/;
for (const f of ALL) {
  const mask = s => s.replace(DIGEST, ' · <load-dependent digest>');
  const a = (await boot('release', f, visible)).out.map(mask);
  const b = (await boot(PATCHED, f, visible)).out.map(mask);
  const ca = new Map(), cb = new Map();
  for (const s of a) ca.set(s, (ca.get(s) || 0) + 1);
  for (const s of b) cb.set(s, (cb.get(s) || 0) + 1);
  const added = [...cb].filter(([s, n]) => (ca.get(s) || 0) !== n).map(([s]) => s);
  const removed = [...ca].filter(([s, n]) => (cb.get(s) || 0) !== n).map(([s]) => s);
  /* Everything a pupil can read that the patch is allowed to change, itemised
     against the ruling that authorised it. Anything else in this delta is an
     unauthorised content change and this gate says so. */
  const AUTHORISED = {
    [WILTON]: {
      added: [
        /* R-Wilton-4 §1 — residue relabelled so its non-selectability reads as chemistry */
        'residue — what stays', 'in the column',
        /* Ruling A — C21 is the taught fuel-oil feed; C24 stays, unable to vaporise */
        'C21', 'C24',
        /* Ruling B — the five corrected tray temperatures */
        'below 25°C · gases', '110°C · petrol range', '220°C · kerosene range',
        '320°C · diesel range', '400°C · fuel oils',
        /* Ruling B — the caption that makes those numbers understood, not just consistent */
        /* T15 — the model-scale disclosure. T13 and T14 are added below, for
           every file, because they are not Wilton-specific. */
        'These temperatures are model values, not measurements.',
                /* Plain spaces, not \u00a0. The source writes &nbsp; so the numbers do not
           wrap away from their units, but visible() collapses runs of \s — which
           in JS includes U+00A0 — to a single ordinary space. Declaring the
           source form made this row fail on a character nobody can see. */
        "This column uses a straight-line rule so the pattern is visible; a real one is not straight. Real fractions are roughly: gases below 25 °C, petrol 25–175 °C, kerosene 150–260 °C, diesel 250–350 °C, fuel oils 300–500 °C, bitumen above that. Those ranges",
        'overlap', "— C14 to C16 sit in both kerosene and diesel in real refining, and which one you call them depends on what the refinery is cutting for that day.",
        'Tray temperature', 'is where a fraction condenses in this column.',
        'Boiling range',
        "is a property of the molecules themselves. Related, but not the same number — which is why a tray label and a feed's boiling point do not have to match.",
      ],
      removed: [
        'residue',
        '25°C · gases', '80°C · petrol range', '150°C · kerosene range',
        '230°C · diesel range', '300°C · fuel oils',
      ],
    },
  };
  /* T13 (NAV-1) and T14 (the branding line) apply across the family, so every
     file gets its own entry rather than a wildcard: the kicker text differs per
     lab and the Studio takes no NAV-1 at all. Measured from the delta, then
     declared — the gate caught these before they were declared, which is the
     order it should happen in. */
  const KICKER = {
    '00_BUILD_FieldOps_Teacher_Studio.html': 'Science Teesside · BUILD v4 FieldOps · Professional Offline Suite',
    '01_Newport_Bridge_Lift_Permit_Lab.html': 'Science Teesside · BUILD v4 FieldOps · Physics',
    '02_Tees_Estuary_Field_Investigation_Lab.html': 'Science Teesside · BUILD v4 FieldOps · Biology',
    '03_Wilton_Carbon_Process_Control_Lab.html': 'Science Teesside · BUILD v4 FieldOps · Chemistry',
    '04_Tees_Bay_Wind_Operations_Lab.html': 'Science Teesside · BUILD v4 FieldOps · Physics',
  };
  for (const [file, kicker] of Object.entries(KICKER)) {
    const e = AUTHORISED[file] || (AUTHORISED[file] = { added: [], removed: [] });
    e.added.push('Made by Matt · ' + kicker);
    e.removed.push(kicker);
    if (file !== STUDIO) e.added.push('← Lessons');
  }
  const exp = AUTHORISED[f] || { added: [], removed: [] };
  /* Report the DIFFERENCE, not the whole delta. The first version printed every
     authorised string alongside the one unauthorised one, so the offender was
     buried in a screenful of expected text — a true report you cannot act on. */
  const unauthorisedAdd = added.filter(v => !exp.added.includes(v));
  const unauthorisedRem = removed.filter(v => !exp.removed.includes(v));
  const missingAdd = exp.added.filter(v => !added.includes(v));
  const missingRem = exp.removed.filter(v => !removed.includes(v));
  const ok = !unauthorisedAdd.length && !unauthorisedRem.length && !missingAdd.length && !missingRem.length;
  row(`U4 ${f.slice(0, 2)}`, `visible text in ${f} changes only where authorised`, ok,
    ok ? `${added.length} added / ${removed.length} removed, every one declared`
       : `UNAUTHORISED added ${JSON.stringify(unauthorisedAdd)} · UNAUTHORISED removed ${JSON.stringify(unauthorisedRem)}` +
         ` · DECLARED BUT ABSENT added ${JSON.stringify(missingAdd)} removed ${JSON.stringify(missingRem)}`);
}

/* -- U5  mission transport digests are unchanged for identical inputs ------
   The Studio mints an id from a sha256 over the mission object. If the C24
   option shifted anything in that object for a mission that does not use C24,
   every mission card printed before today would stop verifying. */
const mint = async tree => (await boot(tree, STUDIO, () => {
  const e = document.getElementById('engine');
  const out = {};
  for (const eng of ['newport-lift-permit', 'tees-estuary-fieldops', 'wilton-carbon-control', 'tees-bay-wind-ops']) {
    e.value = eng; e.dispatchEvent(new Event('change', { bubbles: true }));
    const m = missionObject();
    out[eng] = { id: m.id, scenario: JSON.stringify(m.scenario) };
  }
  return out;
})).out;
{
  const a = await mint('release'), b = await mint(PATCHED);
  const diffs = Object.keys(a).filter(k => a[k].id !== b[k].id);
  row('U5', 'mission ids for the default template of each engine are unchanged',
    diffs.length === 0,
    diffs.length ? diffs.map(k => `${k}: ${a[k].id} -> ${b[k].id}  ${a[k].scenario} -> ${b[k].scenario}`).join(' · ')
                 : Object.keys(a).map(k => `${k}=${a[k].id}`).join(' '));
}

/* -- U6  capsule integrity still verifies -------------------------------- */
{
  const check = async tree => (await boot(tree, STUDIO, async () => {
    document.getElementById('demoData').click();
    await new Promise(r => setTimeout(r, 500));
    return [...document.querySelectorAll('#capsuleRows tr')]
      .map(tr => (tr.textContent.match(/verified|changed \/ invalid/) || [''])[0]);
  })).out;
  const a = await check('release'), b = await check(PATCHED);
  row('U6', 'demonstration capsules still verify identically',
    JSON.stringify(a) === JSON.stringify(b), `release ${JSON.stringify(a)} -> patched ${JSON.stringify(b)}`);
}

/* -- U7  the engine bodies of the three untouched labs ------------------- */
{
  const strip = s => s.replace(/<script>try\{if\(window\.matchMedia[\s\S]*?<\/script>/, '')
                      .replace(/const saved=JSON\.parse\((?:null|localStorage\.getItem\(storageKey\))\|\|'null'\)/, 'SAVEDREAD')
                      .replace(/function save\(\)\{try\{(?:void 0&&)?localStorage\.setItem\(storageKey,JSON\.stringify\(state\)\)\}catch\(e\)\{\}\}/, 'SAVEFN')
                      .replace(/return;(?:void 0|localStorage\.removeItem\(storageKey\));location\.reload\(\)/, 'RESETFN')
                      .replace(/<a class="mbmhome"[^>]*>← Lessons<\/a>/, '')
                      .replace(/\/\* ===== NAV-1:[\s\S]*?@media print\{\.mbmhome\{display:none!important\}\}\n/, '')
                      .replace(/<div class="kicker">(?:Made by Matt · )?/, '<div class="kicker">KICKER');
  const bad = [];
  for (const f of ['01_Newport_Bridge_Lift_Permit_Lab.html', '02_Tees_Estuary_Field_Investigation_Lab.html',
                   '04_Tees_Bay_Wind_Operations_Lab.html']) {
    const a = strip(fs.readFileSync(path.join(ROOT,'release',f), 'utf8'));
    const b = strip(fs.readFileSync(path.join(ROOT,PATCHED,f), 'utf8'));
    if (a !== b) bad.push(`${f} ${sha(a)} != ${sha(b)}`);
  }
  row('U7', 'the three non-Wilton labs differ from release only in the storage, calm, NAV-1 and branding transforms',
    bad.length === 0, bad.length ? bad.join(' · ') : 'Newport, Estuary and Wind all identical once T1-T4, T13 and T14 are normalised');
}

await browser.close();
fs.rmSync(path.join(ROOT, 'work', 'nulltree'), { recursive: true, force: true });

console.log(`${'id'.padEnd(9)} verdict   what`);
console.log('-'.repeat(78));
for (const r of rows) {
  console.log(`${r.id.padEnd(9)} ${(r.ok ? 'UNCHANGED' : 'MOVED').padEnd(9)} ${r.what}`);
  console.log(`          ${r.detail}`);
}
const bad = rows.filter(r => !r.ok);
console.log(`\n${bad.length} unexpected change(s)`);
process.exit(bad.length ? 1 : 0);
