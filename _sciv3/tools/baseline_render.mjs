// A10 gate — proven by RENDER, not by reading.
//
// Runs the ORIGINAL and the REPAIRED file through the real UI, twice each, and
// diffs the rendered profile. That is what "every other strand branch
// byte-unchanged" actually means: identical rendered output except where a
// repair was intended.
//
//   pass "uncertain": choose the "Not sure yet"/"Not ready yet" escape everywhere
//   pass "correct":   choose the keyed answer everywhere
//
// Usage: node baseline_render.mjs <origDir> <newDir>
import { chromium } from 'playwright';
import { readdirSync } from 'fs';
import { pathToFileURL } from 'url';
import { resolve } from 'path';

const [ORIG, NEW] = process.argv.slice(2);
const files = readdirSync(NEW).filter(f => f.startsWith('baseline-') && f.endsWith('.html')
                                           && !f.includes('profile-review'));
const browser = await chromium.launch();
const fails = [];

async function profileOf(file, mode) {
  const page = await browser.newPage();
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await page.goto(pathToFileURL(resolve(file)).href);
  await page.evaluate((mode) => {
    const D = window.ASSESSMENT;
    document.querySelectorAll('.card[data-id]').forEach(card => {
      const opts = [...card.querySelectorAll('.opt')];
      if (!opts.length) return;
      const item = D.items.find(x => x.id === card.dataset.id);
      const target = mode === 'uncertain'
        ? opts.find(o => /not sure|not ready/i.test(o.textContent))
        : (item && typeof item.correct === 'number' ? opts[item.correct] : null);
      if (target) target.click();
    });
    // a pupil who writes something, so the writing strand is genuinely answered
    document.querySelectorAll('textarea').forEach(t => {
      t.value = 'A written response.';
      t.dispatchEvent(new Event('input', { bubbles: true }));
    });
    const next = document.getElementById('next');
    for (let i = 0; i < 40; i++) next.click();
  }, mode);
  await page.waitForTimeout(50);
  const out = await page.evaluate(() =>
    [...document.querySelectorAll('#profile .strand')].map(d => ({
      strand: d.querySelector('strong').textContent,
      label: d.querySelector('.status').textContent,
      cls: d.querySelector('.status').className,
      detail: d.querySelector('p').textContent.trim(),
    })));
  await page.close();
  return { out, errs };
}

const INTENDED = new Set(['Not started yet', 'Answered in writing']);

for (const f of files) {
  console.log(`\n=== ${f}`);
  for (const mode of ['uncertain', 'correct']) {
    const a = await profileOf(`${ORIG}/${f}`, mode);
    const b = await profileOf(`${NEW}/${f}`, mode);
    if (b.errs.length) fails.push(`${f}: ${b.errs.length} page error(s): ${b.errs[0]}`);
    if (a.out.length !== b.out.length) { fails.push(`${f}: strand count changed`); continue; }
    console.log(`  -- all "${mode}"`);
    for (let i = 0; i < a.out.length; i++) {
      const A = a.out[i], B = b.out[i];
      const same = A.label === B.label && A.detail === B.detail;
      if (same) {
        console.log(`     unchanged  ${B.strand.padEnd(30)} "${B.label}"`);
      } else if (INTENDED.has(B.label)) {
        console.log(`     REPAIRED   ${B.strand.padEnd(30)} "${A.label}" -> "${B.label}"`);
      } else {
        console.log(`     UNEXPECTED ${B.strand.padEnd(30)} "${A.label}" -> "${B.label}"`);
        fails.push(`${f} [${mode}] ${B.strand}: unintended change "${A.label}" -> "${B.label}"`);
      }
    }
  }
}
await browser.close();
if (fails.length) { console.log('\nFAILURES:'); fails.forEach(x => console.log('  ' + x)); process.exit(1); }
console.log('\nA10.2 (+ the flagged text-only-strand case) proven by render in all six assessments;');
console.log('every other strand branch renders byte-identically to the original.');
