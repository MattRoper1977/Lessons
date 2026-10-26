#!/usr/bin/env node
/* ==========================================================================
   GATE SHAPE — every gate must hide with `visibility`, not `opacity` alone.

       node test/gate-shape.js

   No browser, no dependencies. Scans every tracked .css file in the repo.

   WHY THE RULE EXISTS
   An animation with `fill-mode: both` or `forwards` applies its final keyframe
   in the CSS *animation origin*, which outranks every normal author declaration
   regardless of selector specificity. So a keyframe ending at `opacity: 1`
   defeats `opacity: 0` from any rule, however specific. No keyframe in this
   estate sets `visibility`, so a gate that pairs the two cannot be defeated by
   adopting a shared class.

   This was measured, not reasoned: all 23 fill-mode classes were applied to all
   9 gate styles in a browser. Every GROW and BUILD gate held. The three
   opacity-only gates in launch-engine were defeated by 12 of the 23 — and one
   of them was live, painting a spotlight over the specimen before any pupil act.

   WHY IT IS NOT A BLANKET `opacity:0` SCAN
   Calibrating showed only 5 opacity-only rules in the whole tree, and two of
   them are legitimate transients rather than gates. A check that flagged all of
   them would be the R-E05 mistake — an instrument reporting the designs it does
   not recognise as broken. So this asserts a KNOWN INVENTORY (set invariance)
   and flags anything NEW, which is decidable, rather than guessing from shape.

   IF YOU ADD A GATE: add it to GATES. If you add a transient that is genuinely
   not withholding anything, add it to TRANSIENTS with a reason. Doing neither
   makes this fail, which is the point.
   ========================================================================== */

'use strict';
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const REPO = execSync('git rev-parse --show-toplevel', { encoding: 'utf8' }).trim();

/* The gate inventory. `hides` is what the rule must set BESIDES opacity. */
const GATES = [
  { file: 'grow-anim/grow-motion.css', sel: '[data-part].g-hidden' },
  { file: 'grow-anim/grow-motion.css', sel: '[data-label]' },
  { file: 'grow-anim/grow-anim.css', sel: '[data-grow-step]' },
  { file: 'grow-anim/grow-anim.css', sel: '[data-overlay]' },
  { file: 'build-anim/build-anim.css', sel: '.ba-stage [data-part].ba-hidden' },
  { file: 'build-anim/build-anim.css', sel: '[data-ba-step]' },
  { file: 'build-anim/build-anim.css', sel: '.ba-label' },
  { file: 'Science_Teesside/launch-engine/sci-engine.css', sel: '.sci-label' },
  { file: 'Science_Teesside/launch-engine/sci-engine.css', sel: '.sci-part' },
  { file: 'Science_Teesside/launch-engine/sci-engine.css', sel: '.sci-spotmove' }
];

/* Opacity-only rules that are NOT gates. Each needs a reason, because "it is
   fine" is what the tautology said about itself. */
const TRANSIENTS = {
  '.g-morph-out': 'a hiding animation, not a gate — grow-anim.js adds .g-hidden 850ms later',
  '.sci-beam': 'decorative light beam; withholds no science',
  '.at-reveal': 'BUILD_ASDAN entrance state — FLAGGED, see reports/INSTRUMENT_INDEX.md',
  '.lo-item': 'build-engine list entrance — FLAGGED, see reports/INSTRUMENT_INDEX.md'
};

function stripKeyframes(css) {
  /* opacity:0 inside @keyframes is an intermediate value, never a gate */
  let out = '', i = 0;
  for (;;) {
    const m = /@keyframes[^{]*\{/.exec(css.slice(i));
    if (!m) { out += css.slice(i); break; }
    out += css.slice(i, i + m.index);
    let j = i + m.index + m[0].length, d = 1;
    while (j < css.length && d) { if (css[j] === '{') d++; else if (css[j] === '}') d--; j++; }
    i = j;
  }
  return out;
}

const problems = [];
const files = execSync('git ls-files "*.css"', { cwd: REPO, encoding: 'utf8' }).split('\n').filter(Boolean);

/* --- 1. the inventory must still pair visibility ------------------------- */
for (const g of GATES) {
  const full = path.join(REPO, g.file);
  if (!fs.existsSync(full)) { problems.push(`${g.file}: missing — gate "${g.sel}" cannot be checked`); continue; }
  const css = stripKeyframes(fs.readFileSync(full, 'utf8'));
  const esc = g.sel.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const m = new RegExp('(^|\\})\\s*' + esc + '\\s*\\{([^}]*)\\}', 'm').exec(css);
  if (!m) { problems.push(`${g.file}: gate "${g.sel}" not found — renamed? update GATES`); continue; }
  const decl = m[2];
  if (!/opacity:\s*0/.test(decl)) { problems.push(`${g.file}: gate "${g.sel}" no longer sets opacity:0`); continue; }
  if (!/visibility:\s*hidden|display:\s*none/.test(decl)) {
    problems.push(`${g.file}: GATE "${g.sel}" hides with opacity ALONE.\n` +
      `      Any shared class whose animation carries fill-mode both/forwards and ends at\n` +
      `      opacity:1 will defeat it — 12 of the 23 in this estate do. Pair it with\n` +
      `      visibility:hidden (and visibility:visible on the released state).`);
  }
}

/* --- 2. anything NEW that hides with opacity alone ----------------------- */
const known = new Set(GATES.map(g => g.sel).concat(Object.keys(TRANSIENTS)));
for (const f of files) {
  if (/\/dist\//.test(f)) continue;                    /* generated from source */
  const css = stripKeyframes(fs.readFileSync(path.join(REPO, f), 'utf8'));
  const re = /([^{}]+)\{([^{}]*)\}/g;
  let m;
  while ((m = re.exec(css))) {
    const sel = m[1].replace(/\/\*[^]*?\*\//g, '').trim().split('\n').pop().trim();
    const decl = m[2];
    if (!/opacity:\s*0\s*[;}]|opacity:\s*0\s*$/.test(decl)) continue;
    if (/visibility:\s*hidden|display:\s*none/.test(decl)) continue;
    if (known.has(sel)) continue;
    problems.push(`${f}: "${sel}" hides with opacity alone and is not in GATES or TRANSIENTS.\n` +
      `      If it withholds something, pair visibility:hidden. If it does not, add it to\n` +
      `      TRANSIENTS with the reason.`);
  }
}

console.log(`gate-shape: ${GATES.length} gates in the inventory, ${files.length} stylesheets scanned`);
if (problems.length) {
  console.log('\n' + problems.map(p => '  ✗ ' + p).join('\n'));
  console.log(`\n${problems.length} problem(s)`);
  process.exit(1);
}
console.log('every gate pairs visibility; no unaccounted opacity-only rules');
