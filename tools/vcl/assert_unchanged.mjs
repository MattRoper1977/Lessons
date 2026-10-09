/* The other half of the control set: did anything move that was not declared.
 *
 * V0 freezes the reaction engine, the pH model, the mystery hash and the
 * teaching copy. This proves it mechanically rather than by inspection. */
import fs from 'node:fs'; import path from 'node:path';
import { execFileSync } from 'node:child_process';
const ROOT = process.env.VCL_ROOT || path.dirname(new URL(import.meta.url).pathname);
const FILE = 'Virtual_Chemistry_Lab_PRO_Spatial_v0_3.html';
const STAGING = process.env.VCL_STAGING || 'staging';
const TRANSFORMS = ['X1a','X1b','X1c','X2a','X2b','X2c','X2d','X3a','X3c','X3d','X3e','X4','X5a','X5b','X6c','X6d1','X6d2','X6d3'];
const rows = []; const row = (id, what, ok, detail) => rows.push({ id, what, ok, detail });

/* U1 — drop everything and the builder hands back release, byte for byte */
execFileSync('node', ['build.mjs', `--drop=${TRANSFORMS.join(',')}`, '--out=work_null'], { cwd: ROOT, stdio: 'pipe' });
row('U1', 'with all transforms dropped the builder reproduces release byte for byte',
  fs.readFileSync(path.join(ROOT, 'release', FILE), 'utf8') === fs.readFileSync(path.join(ROOT, 'work_null', FILE), 'utf8'),
  `${TRANSFORMS.length} transforms dropped`);
fs.rmSync(path.join(ROOT, 'work_null'), { recursive: true, force: true });

const REL = fs.readFileSync(path.join(ROOT, 'release', FILE), 'utf8');
const PAT = fs.readFileSync(path.join(ROOT, STAGING, FILE), 'utf8');

/* U2 — the frozen regions, named individually */
const FROZEN = [
  ['pH model (both passes)', /let H=pool\.H\|\|0[\s\S]*?w\.pH=7;/g],
  ['deterministic mystery hash', /function microMystery\([\s\S]{0,700}?return [^\n]*?;?\n?}/],
  ['hydroxide chain Cu/Fe2/Fe3/Al3/Ca2', /if\(has\("Cu2"\)&&oh>0\)[\s\S]*?remains in excess sodium hydroxide\.";}/],
  ['carbonate effervescence', /if\(has\("CO3"\)&&H>0\)\{[\s\S]{0,200}?LabAudio\.fizz\(\);}/],
  ['sequencing teaching copy', /<strong>Halides:<\/strong>[\s\S]{0,240}?interference\./],
  ['safety / virtual-practical boundary', /Simulation evidence supports scientific reasoning[\s\S]{0,120}?competency\./],
];
/* The existing observation and warning strings are asserted INDIVIDUALLY. The
   first cut spanned them as one region, which the V1 fix legitimately splits by
   inserting new branches between them — so the span differed and the assertion
   reported MOVED without anything frozen having been touched. Presence of each
   exact string is the claim that actually matters. */
const FROZEN_STRINGS = [
  /* the 40-minute arc: five benches x three phases, asserted by their own
     time bands rather than by a span pattern that a nearby edit can break */
  'time:"0\u201310"', 'time:"10\u201325"', 'time:"25\u201340"',
  'title:"Introduce', 'title:"Explore', 'title:"Do ',
  'A white silver chloride precipitate forms.',
  'A cream silver bromide precipitate forms.',
  'A yellow silver iodide precipitate forms.',
  'A dense white barium sulfate precipitate forms.',
  'A pale yellow carbonate interference forms because the sample was not acidified with nitric acid first.',
  'Acidify a fresh portion with nitric acid before adding silver nitrate.',
  'The halide test should use a fresh portion acidified with dilute nitric acid before silver nitrate is added.',
  'For the sulfate test, acidify a fresh portion with dilute hydrochloric acid before adding barium chloride.',
  'A light blue precipitate forms.',
  'A dirty green precipitate forms; it may brown slowly in air.',
  'A red-brown precipitate forms.',
  'The white precipitate redissolves in excess sodium hydroxide to give a colourless solution.',
  'A white precipitate forms and remains in excess sodium hydroxide.',
  'Effervescence: bubbles of carbon dioxide are released.',
];
for (const [name, re] of FROZEN) {
  const a = (REL.match(re) || []).join('\n'), b = (PAT.match(re) || []).join('\n');
  row(`U2 ${name}`, `frozen: ${name}`, a.length > 0 && a === b,
    a.length === 0 ? 'REGION NOT FOUND — the assertion proves nothing, fix the pattern' : `${a.length} chars identical`);
}

for (const str of FROZEN_STRINGS) {
  const a = REL.split(str).length - 1, b = PAT.split(str).length - 1;
  row(`U2s "${str.slice(0, 44)}"`, 'frozen observation/warning string survives verbatim, same count',
    a > 0 && a === b, `release ${a} -> staging ${b}`);
}

/* U3 — the file is still self-contained: no external host, no CDN */
{
  const ext = [...PAT.matchAll(/(?:src|href)\s*=\s*["'](https?:\/\/[^"']+)/g)].map(m => m[1])
    .filter(u => !/^https?:\/\/www\.w3\.org\//.test(u));
  row('U3', 'no external subresource was introduced', ext.length === 0,
    ext.length ? ext.join(' · ') : 'the only absolute URLs are the XHTML and SVG namespace URIs, as on release');
}

/* U4 — storage stays at zero: this app deliberately has none */
for (const [id, re, label] of [['U4a', /localStorage/g, 'localStorage'], ['U4b', /sessionStorage/g, 'sessionStorage'],
                               ['U4c', /indexedDB/gi, 'indexedDB']]) {
  const a = (REL.match(re) || []).length, b = (PAT.match(re) || []).length;
  row(id, `${label} usage is unchanged (release ${a})`, a === b, `release ${a} -> staging ${b}`);
}

/* U5 — the viewport was already correct and must be left alone */
{
  const grab = s => (s.match(/<meta name="viewport"[^>]*>/) || [''])[0];
  row('U5', 'the viewport meta is untouched (it was already correct)', grab(REL) === grab(PAT), grab(PAT));
}

console.log(`${'id'.padEnd(46)} verdict`);
console.log('-'.repeat(78));
for (const r of rows) {
  console.log(`${r.id.padEnd(46)} ${r.ok ? 'UNCHANGED' : 'MOVED'}`);
  console.log(`    ${r.what}`);
  console.log(`    ${r.detail}`);
}
const bad = rows.filter(r => !r.ok);
console.log(`\n${bad.length} unexpected change(s)`);
process.exit(bad.length ? 1 : 0);
