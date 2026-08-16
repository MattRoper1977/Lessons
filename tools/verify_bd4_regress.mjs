#!/usr/bin/env node
/*
 * Backbone Detectives v4 — the regression harness, RE-EXPRESSED.
 *
 * WHAT THE PACK SHIPPED, AND WHY IT COULD NOT SURVIVE DEPLOYMENT
 *
 * The pack's regress.mjs reads both builds and PRINTS a JSON metric block. It
 * asserts nothing. Among the metrics is `MadeByMatt: g('Made by Matt')`, which
 * reads 0 on the release bytes — and the moment the estate's splash is added at
 * deploy time that number becomes 1. Anyone reading the harness as a pass/fail
 * would see the splash as a regression, and the tempting "fix" is to drop the
 * splash to keep the number at 0. That would be deleting a house requirement to
 * satisfy a measurement of its absence.
 *
 * So the expectation is re-expressed rather than removed, in two named limbs:
 *
 *   BASELINE   the RELEASE build carries 0 splashes
 *   DEPLOYED   the DEPLOYED artefact carries exactly 1
 *
 * Neither is deleted. They are different claims about different artefacts, and
 * conflating them is what made the original fragile.
 *
 * THE BASELINE LIMB IS STUBBED, AND SAYS SO
 *
 * It needs the ORIGINAL:
 *     Backbone_Detectives_Skeleton_Engineering_Workbench_PRO_v4_0.html
 *     220,845 B   sha256 89dfa6b1…
 * which has now been swept for FOUR times across three uploads, by size and by
 * hash, with zero hits. It shipped only in the 2026-08-15 seven-file pack. Until
 * it arrives this limb reports AWAITING and the harness is NOT complete — it
 * does not pass, and it must not be read as passing.
 *
 * THE DEPLOYED LIMB IS LIVE NOW
 *
 * "Exactly one splash on the deployed artefact" is a property of the deployed
 * build alone. It needs no baseline, and its control fires on real bytes: run
 * against the PATCHED release build as delivered it FAILS, because that build
 * carries 0 splashes — measured, 223,831 B / 2d65bb77.
 *
 * EXITS  0 every live limb passed · 1 a live limb failed · 2 INCONCLUSIVE
 *
 * Usage:
 *   node tools/verify_bd4_regress.mjs --artefact <path/to/deployed.html>
 *   node tools/verify_bd4_regress.mjs --artefact <path> --self-test
 */
import fs from 'node:fs';
import path from 'node:path';

const argv = process.argv.slice(2);
const arg = n => { const i = argv.indexOf(n); return i >= 0 ? argv[i + 1] : null; };
const SELFTEST = argv.includes('--self-test');

const ORIGINAL = { bytes: 220845, sha256: '89dfa6b1' };

function inconclusive(why, ...more) {
  console.error(`INCONCLUSIVE: ${why}`);
  for (const m of more) console.error(`  ${m}`);
  console.error('  This gate did not judge anything. That is not a pass.');
  process.exit(2);
}

let failed = 0, awaiting = 0;
const check = (ok, what, detail = '') => {
  console.log(`  [${ok ? 'PASS' : 'FAIL'}] ${what}${detail ? '  ·  ' + detail : ''}`);
  if (!ok) failed++;
};
const awaitingLimb = (what, why) => {
  console.log(`  [AWAITING] ${what}\n             ${why}`);
  awaiting++;
};

/* Counted on the source text, deliberately. The splash is a house marker in the
   markup; this limb is about whether the artefact CARRIES it, not about what a
   browser does with it. The rendered questions — 44 px, keyboard reach — belong
   to verify_inline_exit.mjs, which drives a real browser. */
const countSplash = src => (src.match(/Made by Matt/gi) || []).length;

const artefactArg = arg('--artefact');
if (!artefactArg) {
  inconclusive('no --artefact was given.',
    'usage: node tools/verify_bd4_regress.mjs --artefact <path/to/deployed.html>',
    'Backbone Detectives is not deployed in this repository yet, so there is no default.');
}
if (!fs.existsSync(artefactArg)) inconclusive(`the artefact does not exist: ${artefactArg}`);

const src = fs.readFileSync(artefactArg, 'utf8');
const bytes = Buffer.byteLength(src);
console.log(`artefact: ${path.basename(artefactArg)}  ·  ${bytes.toLocaleString('en-GB')} B`);
console.log(`splashes: ${countSplash(src)}\n`);

/* ---------------- BASELINE limb — stubbed, awaiting the ORIGINAL ------------- */
console.log('--- BASELINE limb (the RELEASE build carries 0 splashes) ---');
const originalPath = arg('--original');
if (!originalPath || !fs.existsSync(originalPath)) {
  awaitingLimb('the release build carries 0 "Made by Matt"',
    `needs the ORIGINAL at ${ORIGINAL.bytes.toLocaleString('en-GB')} B / ${ORIGINAL.sha256}…, ` +
    'absent from every upload so far (four sweeps, zero hits). Pass --original when it arrives.');
} else {
  const ob = fs.readFileSync(originalPath);
  const oh = (await import('node:crypto')).createHash('sha256').update(ob).digest('hex');
  if (ob.length !== ORIGINAL.bytes || !oh.startsWith(ORIGINAL.sha256)) {
    inconclusive('the file passed as --original is not the ORIGINAL release build',
      `got ${ob.length} B / ${oh.slice(0, 8)}…, expected ${ORIGINAL.bytes} B / ${ORIGINAL.sha256}…`);
  }
  check(countSplash(ob.toString('utf8')) === 0,
    'the release build carries 0 "Made by Matt"', `${countSplash(ob.toString('utf8'))}`);
}

/* ---------------- DEPLOYED limb — live ------------------------------------- */
console.log('\n--- DEPLOYED limb (the deployed artefact carries exactly 1 splash) ---');
const n = countSplash(src);
check(n === 1,
  'the deployed artefact carries exactly one "Made by Matt" splash',
  `${n} found — the release build carries 0, and the estate requires exactly 1 after integration`);

if (SELFTEST) {
  console.log('\n=== CONTROL ===\n');
  /* Real bytes both ways. Removing the splash from the artefact must red the
     deployed limb; adding a second must red it too. An expectation of "exactly
     one" that only ever tests zero is half a gate. */
  const stripped = src.replace(/Made by Matt/gi, 'REDACTED');
  check(countSplash(stripped) !== 1,
    'CONTROL: with the splash removed from the real artefact, the deployed limb would fail',
    `${countSplash(stripped)} splashes after removal`);
  /* Build a ONE-splash artefact first, then duplicate. The first cut ran the
     duplication straight on `src`, which carries 0 — so `.replace` matched
     nothing, the count stayed 0, and the control passed on `n !== 1` rather
     than on anything to do with duplication. It reported "0 splashes after
     duplication" under a green tick: a control that could not fail, testing a
     mutation it never made. Exactly the species this session is chasing. */
  const one = src.replace('</body>', '<footer>Made by Matt</footer></body>');
  const oneN = countSplash(one);
  check(oneN === 1, 'CONTROL precondition: a one-splash artefact was actually constructed', `${oneN}`);
  const doubled = one.replace('</body>', '<footer>Made by Matt</footer></body>');
  check(countSplash(doubled) === 2 && countSplash(doubled) !== 1,
    'CONTROL: a SECOND splash also fails the limb — "exactly one" is asserted in both directions',
    `one-splash artefact ${oneN} -> duplicated ${countSplash(doubled)}`);
}

console.log(`\n${failed} failed, ${awaiting} awaiting`);
if (awaiting) {
  console.log('HARNESS INCOMPLETE: a limb is awaiting an input that has not arrived.');
  console.log('Do not read this run as a full pass.');
}
process.exit(failed ? 1 : 0);
