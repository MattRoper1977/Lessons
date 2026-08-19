/* P2 build: release/ -> patched/ as a stated list of transforms.
 *
 * Every transform is an exact-string swap that MUST match exactly once. A miss
 * throws. That is the "prove the graft landed" rule made mechanical: a harness
 * that silently fails to apply its own change measures a clean tree and reports
 * success, so nothing here is allowed to fail quietly.
 *
 * Usage: node build.mjs [--drop=T7,T8 ...]
 *   --drop removes a transform from the build. That is how each negative
 *   control is produced: drop the fix, the gate must go red.
 */
import fs from 'node:fs';
import path from 'node:path';
const ROOT = process.env.P2_ROOT || path.dirname(new URL(import.meta.url).pathname);
const PATCHED = process.env.P2_PATCHED || 'staging';

const DROP = new Set(
  (process.argv.find(a => a.startsWith('--drop=')) || '').replace('--drop=', '')
    .split(',').filter(Boolean));
const OUT = (process.argv.find(a => a.startsWith('--out=')) || '--out=staging').slice(6);

const SRC = path.join(ROOT, 'release');
const DST = path.resolve(ROOT, OUT);
const LABS = ['01_Newport_Bridge_Lift_Permit_Lab.html', '02_Tees_Estuary_Field_Investigation_Lab.html',
              '03_Wilton_Carbon_Process_Control_Lab.html', '04_Tees_Bay_Wind_Operations_Lab.html'];
const STUDIO = '00_BUILD_FieldOps_Teacher_Studio.html';
const ALL = [STUDIO, ...LABS];

const files = Object.fromEntries(ALL.map(f => [f, fs.readFileSync(path.join(SRC, f), 'utf8')]));
const applied = [];

function swap(id, file, from, to) {
  if (DROP.has(id)) { applied.push(`${id} DROPPED`); return; }
  const s = files[file];
  const n = s.split(from).length - 1;
  if (n !== 1) throw new Error(`${id}: expected exactly 1 occurrence in ${file}, found ${n}\n  ${from.slice(0, 120)}`);
  files[file] = s.replace(from, to);
  applied.push(`${id} ${file}`);
}
/* Injects a real <script> immediately before </body>. NOT an append to the end
   of the file: the first cut of T4 appended the seed after </html>, where it is
   inert text. It looked applied in every diff and never ran once — which is the
   defect class this whole pass exists to catch, so it is worth a comment. */
function inject(id, file, js) {
  if (DROP.has(id)) { applied.push(`${id} DROPPED`); return; }
  /* Anchor on the file's OWN closing tags — the last ones — not the first
     match. The Studio builds four printable HTML documents as strings, so
     "</body></html>" occurs five times and only the last is this file's. */
  const anchor = '</body></html>';
  const at = files[file].trimEnd().lastIndexOf(anchor);
  if (at < 0 || at + anchor.length !== files[file].trimEnd().length)
    throw new Error(`${id}: ${file} does not end with ${anchor}`);
  files[file] = files[file].slice(0, at) + `<script>${js}</script>` + files[file].slice(at);
  applied.push(`${id} ${file}`);
}

/* ---------------- T1-T3  no pupil data at rest ---------------------------
   The FieldOps ruling is memory-only. These three are the whole surface: the
   boot read, the write, and the explicit clear. */
for (const f of LABS) {
  swap('T1', f,
    `const saved=JSON.parse(localStorage.getItem(storageKey)||'null')`,
    `const saved=JSON.parse(null||'null')`);
  swap('T2', f,
    `function save(){try{localStorage.setItem(storageKey,JSON.stringify(state))}catch(e){}}`,
    `function save(){try{void 0&&localStorage.setItem(storageKey,JSON.stringify(state))}catch(e){}}`);
  swap('T3', f,
    `return;localStorage.removeItem(storageKey);location.reload()`,
    `return;void 0;location.reload()`);
}

/* ---------------- T4  reduced motion seeds calm at boot ------------------ */
const CALM = `try{if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)document.body.classList.add('calm')}catch(e){}`;
for (const f of ALL) inject('T4', f, CALM);

/* ---------------- T5  no inline handler in generated markup -------------- */
swap('T5a', STUDIO,
  `class="mini" onclick="viewCapsule(\${i})">View</button>`,
  `class="mini" type="button" data-view="\${i}">View</button>`);
swap('T5b', STUDIO,
  `el('demoData').onclick=demo;el('exportRouter')`,
  `el('demoData').onclick=demo;el('capsuleRows').addEventListener('click',e=>{const b=e.target.closest('[data-view]');if(b)viewCapsule(+b.dataset.view)});el('exportRouter')`);

/* ---------------- T6  CSV formula injection ------------------------------
   Module scope, not inside csv(): a control has to be able to reach it. */
swap('T6a', STUDIO,
  `\nfunction csv(){`,
  `\nfunction csvCell(v){var t=String(v==null?'':v);/* Excel and Sheets evaluate a cell beginning = + - @ TAB or CR. Quoting alone does not stop it: the value is unquoted before evaluation. Prefix an apostrophe so the cell is text. Alias and Mission title are free pupil/teacher input. */if(/^[=+\\-@\\t\\r]/.test(t))t="'"+t;return '"'+t.replace(/"/g,'""')+'"'}\nfunction csv(){`);
swap('T6b', STUDIO,
  `const text=rows.map(r=>r.map(v=>'"'+String(v).replace(/"/g,'""')+'"').join(',')).join('\\n');download('BUILD_FieldOps_class_evidence.csv'`,
  `const text=rows.map(r=>r.map(csvCell).join(',')).join('\\n');download('BUILD_FieldOps_class_evidence.csv'`);

/* ---------------- T7  R-Wilton-3 band boundaries -------------------------
   wBoil is untouched. Only the tray cut-offs move, and every one of them sits
   in a gap: wBoil(n) = -50+20n is always == 10 (mod 20), and 25/160/280/360/960
   are none of them, so no integer carbon number can ever land ON a boundary.
   All comparisons stay strict <. The residue band stays, as the else. */
swap('T7', '03_Wilton_Carbon_Process_Control_Lab.html',
  `function wTray(n){const bp=wBoil(n);if(bp<25)return{y:120,label:'top gases'};if(bp<100)return{y:190,label:'petrol range'};if(bp<180)return{y:270,label:'kerosene range'};if(bp<260)return{y:350,label:'diesel range'};if(bp<330)return{y:430,label:'fuel-oil range'};return{y:525,label:'residue / too heavy'}}`,
  `function wTray(n){const bp=wBoil(n);if(bp<25)return{y:120,label:'top gases'};if(bp<160)return{y:190,label:'petrol range'};if(bp<280)return{y:270,label:'kerosene range'};if(bp<360)return{y:350,label:'diesel range'};if(bp<960)return{y:430,label:'fuel-oil range'};return{y:525,label:'residue — what stays in the column'}}`);

/* ---------------- T8  the C21 and C24 feeds, in all three places ---------
   RULING A. C21 is the taught fuel-oil feed: it boils at 370C, needs 390C, and
   the furnace ceiling IS 390C, so it distils without anyone inventing a
   temperature. It is also the ONLY carbon number that does — C22 needs 410C
   and every heavier one needs more, measured, not assumed.
   C24 stays selectable and stays unable to vaporise. That is the teaching
   point, handled by T10, not a gap to be closed. */
swap('T8a', '03_Wilton_Carbon_Process_Control_Lab.html',
  `<button class="btn feedW" data-feed="20">C20</button>`,
  `<button class="btn feedW" data-feed="20">C20</button><button class="btn feedW" data-feed="21">C21</button><button class="btn feedW" data-feed="24">C24</button>`);
swap('T8b', '03_Wilton_Carbon_Process_Control_Lab.html',
  `W.feed=[6,10,14,18,20][Math.floor(Math.random()*5)]`,
  `W.feed=[6,10,14,18,20,21,24][Math.floor(Math.random()*7)]`);
swap('T8c', STUDIO,
  `{k:'feed',l:'Feed chain',type:'select',options:[6,10,14,18,20]}`,
  `{k:'feed',l:'Feed chain',type:'select',options:[6,10,14,18,20,21,24]}`);

/* ---------------- T10  the refusal teaches instead of dead-ending --------
   RULING A, second content addition. The old line said only "too low". It has
   to distinguish two different situations, because one sentence cannot be true
   of both: a furnace the pupil has not turned up yet, and a fraction this
   column can never boil. Saying "the furnace reaches 390C so it never
   vaporises" to someone sitting at 200C on a C14 feed would be false. */
swap('T10', '03_Wilton_Carbon_Process_Control_Lab.html',
  `function runDistil(){const eff=wEffectiveFurnace(),need=Math.max(120,wBoil(W.feed)+20);if(eff<need){W.distilled=false;W.tray=null;wEl('wDistilResult').className='notice warn';wEl('wDistilResult').textContent=\`Effective furnace \${eff}°C is too low for this teaching feed to enter the vapour stream.\`;ST.log('distillation_failed',{effective:eff,needed:need})}`,
  `function runDistil(){const eff=wEffectiveFurnace(),need=Math.max(120,wBoil(W.feed)+20);const ceiling=wEffectiveCeiling();if(eff<need){W.distilled=false;W.tray=null;const reachable=ceiling>=need;wEl('wDistilResult').className='notice warn';wEl('wDistilResult').textContent=reachable?\`\${wFormula(W.feed)} boils at \${wBoil(W.feed)}°C, so it needs about \${need}°C to enter the vapour stream. The furnace is at \${eff}°C — raise it.\`:\`\${wFormula(W.feed)} boils at \${wBoil(W.feed)}°C. This column's furnace only reaches \${ceiling}°C, so \${wFormula(W.feed)} never enters the vapour stream — it leaves at the bottom as residue.\`;ST.log('distillation_failed',{effective:eff,needed:need,reachable})}`);
/* Same transform, second anchor: the helper and its only caller land or fall
   together. Splitting them made a configuration where the page simply threw,
   and a control that goes red because nothing loads is not really watching the
   change — it is watching the crash. */
swap('T10', '03_Wilton_Carbon_Process_Control_Lab.html',
  `function wEffectiveFurnace(){return W.furnace-(W.fault==='sensor'?35:0)}`,
  `function wEffectiveFurnace(){return W.furnace-(W.fault==='sensor'?35:0)}\nfunction wEffectiveCeiling(){const s=document.getElementById('wFurnace');return (s?+s.max:390)-(W.fault==='sensor'?35:0)}`);

/* ---------------- T11  the column's printed tray temperatures ------------
   RULING B. These five numbers were consistent with the OLD bands and are the
   fourth set of numbers in this lab about the same chemistry. Corrected to
   <25 / 110 / 220 / 320 / 400, each of which falls inside the band its own
   label names under 25/160/280/360/960. "below 25" rather than "<25" so the
   marker does not need an HTML entity inside SVG text. */
swap('T11', '03_Wilton_Carbon_Process_Control_Lab.html',
  `<text x="220" y="120">25°C · gases</text><text x="220" y="200">80°C · petrol range</text><text x="220" y="280">150°C · kerosene range</text><text x="220" y="360">230°C · diesel range</text><text x="220" y="440">300°C · fuel oils</text>`,
  `<text x="220" y="120">below 25°C · gases</text><text x="220" y="200">110°C · petrol range</text><text x="220" y="280">220°C · kerosene range</text><text x="220" y="360">320°C · diesel range</text><text x="220" y="440">400°C · fuel oils</text>`);

/* ---------------- T12  the caption that makes T11 understood -------------
   RULING B says this is not optional: corrected numbers that nobody can
   place are merely consistent. A tray temperature and a boiling range are
   different quantities, and the column now prints one of each. */
swap('T12', '03_Wilton_Carbon_Process_Control_Lab.html', `\n</svg>\n`,
  `\n</svg>\n<div id="wTrayCaption" style="position:absolute;left:10px;bottom:10px;width:min(400px,46%);background:#05101bdd;border:1px solid #35536d;border-radius:12px;padding:9px;font-size:.72rem;line-height:1.4;color:#9ab3c7"><b style="color:#38bdf8">Tray temperature</b> is where a fraction condenses in this column. <b style="color:#38bdf8">Boiling range</b> is a property of the molecules themselves. Related, but not the same number — which is why a tray label and a feed's boiling point do not have to match.</div>\n`);

/* ---------------- T9  residue reads as chemistry on the column ----------- */
swap('T9', '03_Wilton_Carbon_Process_Control_Lab.html',
  `<text x="220" y="535">residue</text>`,
  `<text x="220" y="528" font-size="12">residue — what stays</text><text x="220" y="544" font-size="12">in the column</text>`);

/* =====================================================================
 * T13 — NAV-1, the way back to the Lessons catalogue.
 *
 * DERIVED, not invented. The eleven lesson files in the co-location target
 * (Science_Teesside/Build/v3_40min, merged at dcc23dc) carry this line
 * byte-identically; the four that do not are the matrix, the guide and the
 * reflection window, which are not lessons. Same directory depth, so the same
 * relative href resolves.
 *
 * The Studio is excluded on purpose: it goes to Matt-s-Apps-, not to Lessons,
 * so a link to the Lessons catalogue would be wrong from there.
 * ===================================================================== */
const NAV1 = `<a class="mbmhome" href="../../../index.html" aria-label="Back to the Lessons catalogue">← Lessons</a>`;
/* The MARKUP alone is not the convention. The neighbours ship this rule with it,
   and it is what makes the control a 44px target, gives it a focus ring, and
   removes it from print. Lifted verbatim from
   Science_Teesside/Build/v3_40min/SCI_B_W3A_Backbones_Explore.html — except
   position, which is `fixed; top:6px; right:10px` there because those pages have
   no toolbar. These labs do, so the link sits inside it and keeps every other
   declaration byte-identical. That deviation is deliberate and declared. */
const NAV1CSS = `/* ===== NAV-1: way home — chrome only, teaching surfaces untouched ===== */
.mbmhome{position:static;display:inline-flex;align-items:center;justify-content:center;gap:6px;min-height:44px;min-width:44px;padding:8px 14px;background:#161D3D;color:#FFF6E8;border-radius:999px;font-weight:800;font-size:.85rem;letter-spacing:.03em;text-decoration:none;box-shadow:0 2px 10px rgba(15,23,42,.3)}
.mbmhome:hover{background:#232C55}
.mbmhome:focus-visible{outline:3px solid #E08A2E;outline-offset:2px}
@media print{.mbmhome{display:none!important}}
`;
for (const f of LABS) {
  swap('T13', f,
    `<div class="tools"><span class="timer" id="timerDisplay">40:00</span>`,
    `<div class="tools">${NAV1}<span class="timer" id="timerDisplay">40:00</span>`);
  /* The page's OWN stylesheet, not the first </style> in the file: each lab
     builds a printable document as a string and that carries a second <style>
     block. The generated one opens `<style>body{`; the page's own opens with a
     newline, which makes it the unique anchor. Same trap as the Studio's five
     </body></html>, caught the same way — by the exactly-once guard. */
  swap('T13', f, `<style>\n`, `<style>\n${NAV1CSS}`);
}

/* =====================================================================
 * T14 — the branding line, in the form the target family actually uses.
 *
 * MEASURED: the co-location target carries ZERO splash overlays and ZERO
 * mbm_reading_theme. "Made by Matt" appears there as a header, footer or
 * comment line — eleven of fifteen files, exactly once each. Landing a
 * games-style splash overlay here would make these the only lesson files in
 * the estate with one, which is divergence dressed as conformance.
 *
 * So: one line, in the family's own shape. The regress trap is re-expressed
 * with it — baseline 0 on the release build, exactly 1 once deployed.
 * ===================================================================== */
for (const f of ALL) {
  swap('T14', f,
    `<div class="kicker">Science Teesside · BUILD v4 FieldOps`,
    `<div class="kicker">Made by Matt · Science Teesside · BUILD v4 FieldOps`);
}

/* =====================================================================
 * T15 — the disclosure copy.  §4, and it is not optional.
 *
 * The app gives a crisp answer. It may not imply the chemistry is crisp.
 * Three things have to be said and none of them is said anywhere today: the
 * temperature scale is a MODEL, the real ranges are wider and overlapping, and
 * C14–C16 genuinely sit in both kerosene and diesel in real refining.
 *
 * Placed with the tray-temperature caption, because that is where a pupil is
 * already being asked to hold two kinds of number apart.
 * ===================================================================== */
swap('T15', '03_Wilton_Carbon_Process_Control_Lab.html',
  `Related, but not the same number — which is why a tray label and a feed's boiling point do not have to match.</div>`,
  `Related, but not the same number — which is why a tray label and a feed's boiling point do not have to match.` +
  `<div id="wModelNote" style="margin-top:7px;padding-top:7px;border-top:1px solid #35536d;color:#8fa6b8">` +
  `<b style="color:#fbbf24">These temperatures are model values, not measurements.</b> ` +
  `This column uses a straight-line rule so the pattern is visible; a real one is not straight. ` +
  `Real fractions are roughly: gases below 25&nbsp;°C, petrol 25–175&nbsp;°C, kerosene 150–260&nbsp;°C, ` +
  `diesel 250–350&nbsp;°C, fuel oils 300–500&nbsp;°C, bitumen above that. ` +
  `Those ranges <b>overlap</b> — C14 to C16 sit in both kerosene and diesel in real refining, ` +
  `and which one you call them depends on what the refinery is cutting for that day.` +
  `</div></div>`);

/* =====================================================================
 * T16 — the Studio's launch links, rewritten for the split.
 *
 * THE DEFECT. The engine table shipped `file:'01_Newport_Bridge_Lift_Permit_Lab.html'`
 * — a bare filename, correct only while the Studio and the labs sat in one
 * folder. After the split they are in different repositories on different
 * origins, so "Launch mission" on the Apps origin resolves to a path that
 * exists only in Lessons and 404s. The governing prompt called the cross-links
 * "the likeliest thing to break the pack's best feature", and this was it.
 *
 * WHY split_transport.mjs did not catch it: that harness proves the FILE-IMPORT
 * route (setInputFiles on #missionFile) and constructs the lab URL itself. It
 * never reads #launchMission's href, so the one transport that depends on this
 * string was the one transport nothing exercised. S4 there now does.
 *
 * THE PREFIX IS DERIVED, NOT ASSUMED. Two facts already in this repository:
 *   - tools/verify_served.mjs:79  LESSONS_ORIGIN = 'https://madebymatt.uk/Lessons'
 *     (so Lessons is /Lessons-prefixed on the live origin, NOT root-mounted —
 *     corroborated by the recorded live pin of madebymatt.uk/Lessons/resources.json)
 *   - tools/verify_fieldops_served.mjs:74  PLACED = 'Science_Teesside/Build/v4_fieldops'
 * and verify_served.mjs builds exactly `${LESSONS_ORIGIN}/${PLACED}/${lab}`.
 * LAB_ORIGIN below is that concatenation. controls.mjs asserts the two files
 * still agree, so if the origin ever moves in one and not the other, that goes
 * red rather than shipping a second 404.
 *
 * The mission payload is untouched: buildMission() does `info.file + '#mission='
 * + b64url(m)`, and a hash appends to an absolute URL exactly as it does to a
 * bare filename. `.file` has no other reader — grep says one use.
 * ===================================================================== */
const LAB_ORIGIN = 'https://madebymatt.uk/Lessons/Science_Teesside/Build/v4_fieldops';
for (const lab of LABS)
  swap('T16', STUDIO, `{file:'${lab}'`, `{file:'${LAB_ORIGIN}/${lab}'`);

fs.mkdirSync(DST, { recursive: true });
for (const f of ALL) fs.writeFileSync(path.join(DST, f), files[f]);
console.log(`built ${DST}`);
for (const a of applied) console.log('  ' + a);
