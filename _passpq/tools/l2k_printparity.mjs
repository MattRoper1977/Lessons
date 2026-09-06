#!/usr/bin/env node
// l2k_printparity.mjs — pass PEQ-L2K print-parity proof for the six LAUNCH PEQ decks.
//
// The PART B contract is print-text-identical; this pass's ruled edits (banking
// strings + the witness Level tick) DO change print text, so the gate here is the
// honest version: render the deck at the pre-pass base commit and at HEAD, both in
// print emulation with the route toggle OFF, and assert
//     transform(base print text) === head print text
// where transform is EXACTLY the declared ruled string set — nothing else may move.
//
// Usage: node _passpq/tools/l2k_printparity.mjs [<base-commit>]   (default 2310ea0)
import { chromium } from 'playwright';
import { execFileSync } from 'child_process';
import { fileURLToPath, pathToFileURL } from 'url';
import fs from 'fs';
import os from 'os';
import path from 'path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const BASE = process.argv[2] || '2310ea0';
const DECKS = [
  'PEQ_W1_Intro_and_Choosing_My_Level.html',
  'PEQ_W2_What_Makes_Communication_Effective.html',
  'PEQ_W3_Active_Listening_and_Giving_Feedback.html',
  'PEQ_W4_Plan_a_Communication_Activity.html',
  'PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html',
  'PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html',
];
// the ruled transforms, in RENDERED text space (entities resolved, whitespace normalised)
const TRANSFORMS = [
  ['PEQ Entry 3 (Level 1 stretch)', 'PEQ Entry 3 (Level 1 · Level 2 routes)'],
  ['(ComSkE3 · ComSk1 (stretch)', '(ComSkE3 · ComSk1 · ComSk2 routes'],
  ['ComSkE3 · ComSk1 (stretch), begins', 'ComSkE3 · ComSk1 · ComSk2 routes, begins'],
  ['(Communication, ComSk1, begins)', '(Communication, ComSk1 · ComSk2 routes, begins)'],
  ['☐ Entry 3 ☐ Level 1 A learner', '☐ Entry 3 ☐ Level 1 ☐ Level 2 A learner'],
  ['Entry 3 or Level 1, never both (barred combinations, spec v1.2 §6.5). Supported and Standard evidence Entry 3; Stretch evidences Level 1.',
   'Entry 3, Level 1 or Level 2, never more than one (barred combinations, spec v1.2 §6.5). Supported and Standard evidence Entry 3; Stretch evidences Level 1; the staff-directed Level 2 route evidences Level 2.'],
];

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'l2k-base-'));
const browser = await chromium.launch();
const page = await (await browser.newContext()).newPage();
async function printText(fileUrl) {
  await page.goto(fileUrl, { waitUntil: 'load' });
  await page.emulateMedia({ media: 'print' });
  const t = await page.evaluate(() => document.body.innerText);
  await page.emulateMedia({ media: 'screen' });
  return t.replace(/\s+/g, ' ').trim();
}
const fails = [];
for (const deck of DECKS) {
  const rel = `LAUNCH_ASDAN/PEQ/${deck}`;
  const baseHtml = execFileSync('git', ['show', `${BASE}:${rel}`], { cwd: ROOT, maxBuffer: 1 << 27 });
  const basePath = path.join(tmp, deck);
  fs.writeFileSync(basePath, baseHtml);
  // base deck references ../visual-upgrade.{js,css}; give the temp dir the same view
  for (const a of ['visual-upgrade.js', 'visual-upgrade.css']) {
    const dst = path.join(path.dirname(tmp), a);
    if (!fs.existsSync(dst)) fs.copyFileSync(path.join(ROOT, 'LAUNCH_ASDAN', a), dst);
  }
  let baseText = await printText(pathToFileURL(basePath).href);
  const headText = await printText(pathToFileURL(path.join(ROOT, rel)).href);
  let expected = baseText;
  for (const [o, n] of TRANSFORMS) expected = expected.split(o).join(n);
  if (expected !== headText) {
    let i = 0;
    while (i < expected.length && expected[i] === headText[i]) i++;
    fails.push(`${deck}: print text diverges beyond the ruled transforms at char ${i}:\n` +
               `  expected …${expected.slice(Math.max(0, i - 60), i + 120)}…\n` +
               `  actual   …${headText.slice(Math.max(0, i - 60), i + 120)}…`);
  } else {
    console.log(`${deck}: head print text == base + exactly the ruled transforms`);
  }
}
await browser.close();
if (fails.length) { console.log('\nPRINT PARITY FAIL:'); fails.forEach(f => console.log('  ' + f)); process.exit(1); }
console.log('\nprint parity: 6/6 decks — the only print-text deltas are the ruled strings');
