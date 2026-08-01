#!/usr/bin/env node
/* ==========================================================================
   PRINT PACK — does each tier actually produce a handout?

       node test/print-pack.js            all Science_Teesside decks

   WHY THIS SHAPE, AND NOT THE OBVIOUS ONE
   The previous attempt measured the rendered height of #print-area under print
   media. It fired on 25 decks of 25, 24 untouched, because
   `.print-section{display:none}` with `.visible` added by `printPack(level)`
   means the pack is LEGITIMATELY empty until a tier is chosen. Measuring it at
   rest asks a question the subsystem never claimed to answer.

   REGISTER R-E05 closes the print subsystem to pattern-matching instruments —
   chain 691 -> 12 -> 4 -> 7 -> 0, five alarms and zero real defects, because
   "a subsystem with many valid designs generates false positives in proportion
   to its variety". So this does not pattern-match. It DRIVES the subsystem the
   way a teacher does — stub window.print, call printPack(tier), then count —
   reusing the method already proven in reports/convergence/audit.mjs.

   It asserts counts and character totals, never "did not throw".
   ========================================================================== */
'use strict';
const fs = require('fs');
const path = require('path');
const { HOLD_MS } = require('./measure.js');

const ROOT = path.join(__dirname, '..', '..');
const EXEC = process.env.SCI_CHROMIUM || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const TIERS = ['supported', 'standard', 'stretch'];
const MIN_CHARS = 200;      /* a tier producing less than this is not a handout */

(async () => {
  let chromium;
  try { ({ chromium } = require('playwright-core')); }
  catch (e) { console.error('playwright-core not installed.'); process.exit(2); }

  const decks = [];
  for (const p of ['Build', 'Grow', 'Launch']) {
    const d = path.join(ROOT, p);
    if (!fs.existsSync(d)) continue;
    fs.readdirSync(d).filter(f => f.endsWith('.html')).sort()
      .forEach(f => decks.push({ pathway: p, file: f, full: path.join(d, f) }));
  }

  const browser = await chromium.launch({ executablePath: EXEC, args: ['--no-sandbox'] });
  const problems = [];
  let noPack = 0, checked = 0;

  for (const d of decks) {
    const page = await browser.newPage();
    await page.goto('file://' + d.full);
    await page.waitForTimeout(HOLD_MS);

    const r = await page.evaluate((tiers) => {
      if (typeof window.printPack !== 'function') return { hasPack: false };
      const realPrint = window.print;
      window.print = function () {};
      const out = {};
      tiers.forEach(function (lvl) {
        try { window.printPack(lvl); } catch (e) { out[lvl] = { error: String(e) }; return; }
        const vis = Array.prototype.slice.call(document.querySelectorAll('.print-section.visible'));
        out[lvl] = {
          visible: vis.length,
          chars: vis.reduce((a, e) => a + (e.textContent || '').trim().length, 0),
          empty: vis.filter(e => (e.textContent || '').trim().length < 12).map(e => e.id)
        };
        document.querySelectorAll('.print-section').forEach(e => e.classList.remove('visible'));
      });
      window.print = realPrint;
      return { hasPack: true, tiers: out };
    }, TIERS);

    await page.close();

    if (!r.hasPack) { noPack++; continue; }   /* R-A06: print-light by design */
    checked++;
    for (const t of TIERS) {
      const v = r.tiers[t];
      if (!v) { problems.push(`${d.pathway}/${d.file} · ${t}: not reported`); continue; }
      if (v.error) { problems.push(`${d.pathway}/${d.file} · ${t}: printPack threw ${v.error}`); continue; }
      if (v.visible === 0) problems.push(`${d.pathway}/${d.file} · ${t}: 0 sections visible after printPack("${t}") — that tier prints nothing`);
      else if (v.chars < MIN_CHARS) problems.push(`${d.pathway}/${d.file} · ${t}: ${v.visible} section(s) but only ${v.chars} chars (floor ${MIN_CHARS})`);
      if (v.empty && v.empty.length) problems.push(`${d.pathway}/${d.file} · ${t}: empty section(s) ${v.empty.join(', ')}`);
    }
  }
  await browser.close();

  console.log(`print-pack: ${decks.length} deck(s) · ${checked} with a pack driven across ${TIERS.length} tiers · ` +
              `${noPack} print-light by design (R-A06)`);
  if (problems.length) {
    console.log('\n' + problems.map(p => '  ✗ ' + p).join('\n'));
    console.log(`\n${problems.length} problem(s)`);
    process.exit(1);
  }
  console.log('every tier of every pack produces a handout');
})();
