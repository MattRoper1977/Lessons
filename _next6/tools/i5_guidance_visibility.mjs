#!/usr/bin/env node
/**
 * ORDER N6-I · I5 — is staff guidance visible to a pupil on the default screen?
 *
 * The tag map is only worth its cost if there is something on the pupil-facing
 * surface to hide. This measures that directly instead of assuming it, and it
 * walks EVERY SLIDE rather than the opening one.
 *
 * That distinction is the whole measurement. These decks hide non-active slides
 * with `.slide{display:none}`, so `document.body.innerText` at load returns the
 * title slide and nothing else — a first pass reported route labels as invisible
 * in BUILD_ASDAN and LAUNCH_ASDAN purely because they sit on slide 4. Each slide
 * is therefore activated in turn and its visible text collected, which is what a
 * class actually sees over forty minutes.
 *
 * `innerText` excludes anything inside a closed <dialog>, a [hidden] element or
 * a display:none subtree, so what it returns is what is on the wall.
 *
 * A deck's staff strings are taken FROM THE DECK: the data-ta1/data-ta2
 * attribute values it carries. No external vocabulary list, so this cannot go
 * quiet on a pack whose wording differs.
 *
 * Usage: node i5_guidance_visibility.mjs <paths.txt> [out.json]
 */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const files = fs.readFileSync(process.argv[2], 'utf8').split('\n').map((s) => s.trim()).filter(Boolean);

// Staff-facing string families that are NOT held in a container — the ones that
// could actually be on the wall. Each is a candidate for the hide set; a family
// that is in the source but never on screen is not.
const PROBES = [
  ['SoW cell reference', /'[A-Za-z ]+ (Weekly - )?(Autumn|Spring|Summer)'![A-Z]\d{1,4}/],
  ['Exact SOW outcome', /Exact SOW outcome/],
  ['Estate sequence', /Estate sequence/],
  ['Inherited mapping/evidence', /Inherited (mapping|evidence)/],
  ['AQA UAS unit title', /AQA UAS/],
  ['route label (pupil-facing)', /(Supported route|Standard route|Stretch route|Optional reach|Secure route|Reach route)/],
];
const b = await chromium.launch();
const rows = [];
for (const f of files) {
  const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  try {
    await p.goto('file://' + path.resolve(f), { waitUntil: 'load' });
    await p.waitForTimeout(350);
    const r = await p.evaluate(() => {
      const vis = (e) => (e.checkVisibility ? e.checkVisibility() : true);
      const slides = [...document.querySelectorAll('[data-ta1]')];
      const probes = [];
      for (const s of slides) {
        for (const k of ['ta1', 'ta2']) {
          const v = s.dataset[k];
          if (v && v.length > 30) probes.push(v.slice(0, 60));
        }
      }
      // Walk every slide. A deck shows one at a time; the pupil sees all of them.
      const all = [...document.querySelectorAll('.slide')];
      let seen = document.body.innerText || '';
      if (all.length > 1) {
        const prev = all.map((s) => s.className);
        for (const s of all) {
          all.forEach((x) => x.classList.remove('active'));
          s.classList.add('active');
          s.removeAttribute('hidden');
          seen += '\n' + (document.body.innerText || '');
        }
        all.forEach((s, i) => { s.className = prev[i]; });
      }
      const leaked = probes.filter((t) => seen.includes(t));
      // Where does the guidance live?
      const holders = ['teacherDialog', 'taOverlay', 'taDialog', 'tool-ta']
        .filter((id) => document.getElementById(id));
      const holderVisible = holders.filter((id) => vis(document.getElementById(id)));
      return { probes: probes.length, leaked: leaked.length,
               sample: leaked[0] || null, holders, holderVisible,
               slides: all.length, bodyTextLen: seen.length,
               visibleText: seen };
    });
    const vt = r.visibleText || ''; delete r.visibleText;
    const src = fs.readFileSync(f, 'utf8').replace(/&#39;/g, "'").replace(/&amp;/g, '&');
    const fam = {};
    for (const [name, rx] of PROBES) fam[name] = { inSource: rx.test(src), onScreen: rx.test(vt) };
    rows.push({ file: f, ...r, visibleTextLen: vt.length, families: fam });
  } catch (e) {
    rows.push({ file: f, error: String(e && e.message || e) });
  }
  await p.close();
}
await b.close();
const withGuidance = rows.filter((r) => r.probes > 0);
const leaking = rows.filter((r) => r.leaked > 0);
console.log(`decks carrying staff guidance strings : ${withGuidance.length}/${rows.length}`);
console.log(`decks where any of it is VISIBLE on the default screen : ${leaking.length}`);
for (const r of leaking.slice(0, 10)) {
  console.log(`   LEAK ${path.basename(r.file)} ${r.leaked}/${r.probes} — ${JSON.stringify(r.sample)}`);
}
const holderCount = {};
for (const r of withGuidance) for (const h of (r.holders || [])) holderCount[h] = (holderCount[h] || 0) + 1;
const visCount = {};
for (const r of withGuidance) for (const h of (r.holderVisible || [])) visCount[h] = (visCount[h] || 0) + 1;
console.log('guidance containers present :', JSON.stringify(holderCount));
console.log('…of which visible at load   :', JSON.stringify(visCount));
console.log();
console.log('STRING FAMILIES — files where present in source / VISIBLE across all slides');
const packs = {};
for (const r of rows) {
  if (!r.families) continue;
  const k = r.file.split('/').slice(0, 2).join('/');
  packs[k] ??= {};
  for (const [n] of PROBES) {
    packs[k][n] ??= { src: 0, scr: 0 };
    if (r.families[n].inSource) packs[k][n].src++;
    if (r.families[n].onScreen) packs[k][n].scr++;
  }
}
const names = PROBES.map((x) => x[0]);
console.log('pack'.padEnd(34) + names.map((n) => n.slice(0, 17).padEnd(19)).join(''));
for (const k of Object.keys(packs).sort())
  console.log(k.slice(0, 33).padEnd(34) +
    names.map((n) => `${packs[k][n].src}/${packs[k][n].scr}`.padEnd(19)).join(''));
if (process.argv[3]) fs.writeFileSync(process.argv[3], JSON.stringify(rows, null, 1));
process.exit(leaking.length ? 1 : 0);
