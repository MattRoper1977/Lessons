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

/* ---------------- T8  the C24 feed, in all three places ------------------ */
swap('T8a', '03_Wilton_Carbon_Process_Control_Lab.html',
  `<button class="btn feedW" data-feed="20">C20</button>`,
  `<button class="btn feedW" data-feed="20">C20</button><button class="btn feedW" data-feed="24">C24</button>`);
swap('T8b', '03_Wilton_Carbon_Process_Control_Lab.html',
  `W.feed=[6,10,14,18,20][Math.floor(Math.random()*5)]`,
  `W.feed=[6,10,14,18,20,24][Math.floor(Math.random()*6)]`);
swap('T8c', STUDIO,
  `{k:'feed',l:'Feed chain',type:'select',options:[6,10,14,18,20]}`,
  `{k:'feed',l:'Feed chain',type:'select',options:[6,10,14,18,20,24]}`);

/* ---------------- T9  residue reads as chemistry on the column ----------- */
swap('T9', '03_Wilton_Carbon_Process_Control_Lab.html',
  `<text x="220" y="535">residue</text>`,
  `<text x="220" y="528" font-size="12">residue — what stays</text><text x="220" y="544" font-size="12">in the column</text>`);

fs.mkdirSync(DST, { recursive: true });
for (const f of ALL) fs.writeFileSync(path.join(DST, f), files[f]);
console.log(`built ${DST}`);
for (const a of applied) console.log('  ' + a);
