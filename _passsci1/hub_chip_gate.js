#!/usr/bin/env node
// SUPERSEDED 2026-08-10 — this gate hard-asserts Science · Teesside at 25/25 and now fails
// by design: the chip legitimately moved to 63 in the sci-v3 install. Logic left untouched
// as a sealed record of that run. Current equivalent: _sciv3/tools/chip_gate.mjs, which
// drives the real index.html in a browser rather than replicating its filter chains.
// Hub chip-count gate (SCI-3F §3.5). Replicates index.html buildQuicknav()/render()
// filter chains against the MERGED resources.json and asserts, per subject, that the
// chip's advertised in-collection count equals the number of cards render() returns
// when that chip is the only filter. YEAR fixed to the active collection.
const fs = require('fs');
const YEAR = "2026-27";
const ALL = JSON.parse(fs.readFileSync(process.argv[2] || 'resources.json', 'utf8'));

// buildQuicknav(): total across all years; inCol within active YEAR (index.html:378)
const total = {}, inCol = {};
ALL.forEach(r => {
  total[r.subject] = (total[r.subject] || 0) + 1;
  if (!YEAR || r.year === YEAR) inCol[r.subject] = (inCol[r.subject] || 0) + 1;
});

// render(): with only the subject chip active (q="", t="", TIER="", y=YEAR) (index.html:338-340)
function renderCount(su) {
  return ALL.filter(r =>
    (!su || r.subject === su) && (!YEAR || r.year === YEAR)
  ).length;
}

let fail = 0, checked = 0;
const rows = [];
Object.keys(total).sort().forEach(su => {
  const n = inCol[su] || 0;                 // index.html:382  const n=inCol[su]||0
  const advertised = n || total[su];        // index.html:383  ${n||total[su]}
  const isLib = n === 0;                     // lib chip => advertises all-year total by design
  const returned = renderCount(su);          // cards render() actually returns for this chip
  checked++;
  // For in-collection chips the advertised number MUST equal render()'s returned count.
  // Lib chips (n===0) deliberately advertise the all-year total and render the empty-in-collection
  // state; that is designed behaviour, not the bug — assert render returns 0 for them.
  let ok;
  if (isLib) ok = (returned === 0);
  else ok = (advertised === returned);
  if (!ok) fail++;
  if (!ok || /Science/.test(su)) rows.push({su, total: total[su], inCol: n, advertised, returned, isLib, ok});
});

console.log(`# Hub chip gate — YEAR=${YEAR} — subjects checked: ${checked}`);
console.log(`# columns: subject | total(all yrs) | inCol | advertised | render-returned | lib? | OK`);
rows.forEach(r => console.log(
  `  ${r.ok ? 'PASS' : 'FAIL'} | ${r.su} | total=${r.total} | inCol=${r.inCol} | adv=${r.advertised} | ret=${r.returned} | lib=${r.isLib}`));
const sci = rows.find(r => r.su === 'Science · Teesside');
console.log(`\n# Science · Teesside: advertised=${sci ? sci.advertised : 'MISSING'} returned=${sci ? sci.returned : 'MISSING'} (expect 25/25)`);
console.log(fail === 0 ? '\nHUB CHIP GATE: PASS (every in-collection chip advertises what render returns)'
                       : `\nHUB CHIP GATE: FAIL (${fail} subject chips diverge)`);
process.exit(fail === 0 && sci && sci.advertised === 25 && sci.returned === 25 ? 0 : 1);
