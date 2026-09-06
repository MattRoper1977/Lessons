#!/usr/bin/env node
// SCA-1 CLOSE v2 §1 — order-dependent hinge detector, with calibration.
// An option set is EXEMPT from shuffling only when position carries meaning:
//   (a) an option refers to the OPTION LIST itself ("all of the above", "none of these",
//       "both of the above", "options 1 and 2", "the first option", "A and B"), or
//   (b) the whole set is a pure monotonic numeric ladder in one unit (a sequence, so
//       reordering would destroy the ladder the question is testing).
// Domain-language "both" ("Both muscles push" — both of the two muscles in the STEM) is
// NOT option-referential and is NOT exempt: shuffling such a set is safe.
const fs = require('fs');

const LIST_REF = new RegExp([
  /\ball of the (above|below)\b/, /\bnone of (the above|these|the below)\b/,
  /\bboth of the above\b/, /\ball three of the above\b/, /\bany of the above\b/,
  /\bneither of the above\b/, /\bthe (first|second|third|last) (option|answer|one above)\b/,
  /\boptions? \d\b/, /\b[A-D] and [A-D]\b/, /\ball of these\b/,
].map(r => r.source).join('|'), 'i');

function pureNumber(o) {
  const m = String(o).trim().match(/^[×x]?\s*[-+]?\d[\d,]*(\.\d+)?\s*([a-zA-Z°µ%]{0,4})$/);
  return m ? { v: parseFloat(m[0].replace(/[×x,\s]/g, '')), unit: (m[2] || '').toLowerCase() } : null;
}
function numericLadder(opts) {
  const ns = opts.map(pureNumber);
  if (ns.some(x => !x)) return false;
  const units = new Set(ns.map(x => x.unit));
  if (units.size !== 1) return false;              // mixed units = candidate values, not a ladder
  const vs = ns.map(x => x.v);
  const asc = vs.every((v, i) => i === 0 || v > vs[i - 1]);
  const desc = vs.every((v, i) => i === 0 || v < vs[i - 1]);
  return asc || desc;
}
function classify(opts) {
  const reasons = [];
  for (const o of opts) if (LIST_REF.test(o)) reasons.push(`list-referential option: "${o}"`);
  if (numericLadder(opts)) reasons.push(`monotonic numeric ladder in one unit: ${opts.join(' | ')}`);
  return reasons;
}

// ---- calibration: the instrument is proven on known cases before it is trusted ----
const CAL = [
  { name: 'POS all-of-the-above', opts: ['Oxygen', 'Carbon dioxide', 'All of the above'], want: true },
  { name: 'POS none-of-these', opts: ['Water', 'Sugar', 'None of these'], want: true },
  { name: 'POS both-of-the-above', opts: ['It contracts', 'It relaxes', 'Both of the above'], want: true },
  { name: 'POS options-1-and-2', opts: ['Options 1 and 2', 'Only diffusion', 'Neither'], want: true },
  { name: 'POS monotonic ladder', opts: ['1 N', '2 N', '3 N'], want: true },
  { name: 'NEG domain-both (muscles)', opts: ['Biceps contracts and triceps relaxes', 'Both muscles push', 'Triceps contracts to bend'], want: false },
  { name: 'NEG domain-both (processes)', opts: ['Both processes with similarities/differences', 'Only diffusion', 'A calculation'], want: false },
  { name: 'NEG unordered values', opts: ['0.05 mm', '8000 mm', '20.4 mm'], want: false },
  { name: 'NEG mixed units', opts: ['×200', '×4.5', '200 mm'], want: false },
  { name: 'NEG plain prose', opts: ['A line of bones down the back', 'It is big', 'It has fur'], want: false },
];

if (process.argv[2] === 'calibrate') {
  let bad = 0;
  for (const c of CAL) {
    const got = classify(c.opts).length > 0;
    const ok = got === c.want;
    if (!ok) bad++;
    console.log(`${ok ? 'PASS' : 'FAIL'}  ${c.name}  (fired=${got}, want=${c.want})`);
  }
  console.log(bad ? `calibration: ${bad} FAIL` : `calibration: all ${CAL.length} controls pass`);
  process.exit(bad ? 1 : 0);
}

const rows = JSON.parse(fs.readFileSync('_sca1close/tables/hinges.json', 'utf8'));
let n = 0;
for (const r of rows) {
  const reasons = classify(r.opts);
  r.exempt = reasons.length > 0;
  r.exempt_reason = reasons.join('; ');
  if (r.exempt) { n++; console.log(`EXEMPT ${r.file} :: ${r.exempt_reason}`); }
}
fs.writeFileSync('_sca1close/tables/hinges.json', JSON.stringify(rows, null, 1));
console.log(`exemptions: ${n} of ${rows.length} hinge questions are order-dependent`);
