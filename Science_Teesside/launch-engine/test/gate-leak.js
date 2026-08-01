#!/usr/bin/env node
/* ==========================================================================
   GATE LEAK INSTRUMENT — is anything the layer withholds actually readable?

     node test/gate-leak.js            all fifteen decks
     node test/gate-leak.js W3_L1      one deck, by substring

   Requires playwright-core and a Chromium. Set SCI_CHROMIUM to override the
   browser path.

   WHY IT MEASURES THE WAY IT DOES — two rules, both learned the hard way.

   1. MEASURE THE RENDERED PROPERTY, NOT THE BOOKKEEPING.
      The first version of this check counted `.sci-label[data-shown="1"]`.
      A build that held every label at computed opacity 1 — via a shared class
      whose animation carries `fill-mode: both` — never touched that attribute,
      so the instrument reported green straight through the fault it existed to
      detect. Attributes say what the code MEANT. Computed style says what the
      pupil SEES. Only the second one is the claim.

   2. MEASURE ON THE SLIDE, NOT AT LOAD.
      The repair for (1) still passed, because it measured after `goto` while
      every component sat on an inactive `display:none` slide — and Chromium
      does not start animations inside a `display:none` subtree, so everything
      read as hidden whether it was gated or not. This walks to each slide and
      measures there, after waiting out the longest fill-mode animation.

   If you add a gate to the layer, add it to GATES below. A gate this file does
   not know about is a gate nothing is watching.
   ========================================================================== */

'use strict';
const fs = require('fs');
const path = require('path');

const { HOLD_MS } = require('./measure.js');   /* standing rule 13 */
const DECKS = path.join(__dirname, '..', '..', 'Launch');
const EXEC = process.env.SCI_CHROMIUM || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const FILTER = process.argv[2] || '';

/* Every mechanism this layer uses to withhold something, and the act that is
   supposed to release it. `sel` selects elements that are STILL GATED. */
const GATES = [
  { name: 'observation label',
    sel: '.sci-label:not([data-shown="1"])',
    earnedBy: 'marking what you notice, then spotlighting a part' },
  { name: 'locked explanation',
    sel: '.sci-link[data-open="0"] .sci-link-body',
    earnedBy: 'completing the previous stage of the evidence chain' },
  { name: 'unbuilt diagram part',
    sel: '.sci-part[data-built="0"]',
    earnedBy: 'answering the question that precedes that build step' },
  /* The spotlight is a gate too: it dims the specimen and rings one region. If
     it paints before the teacher has chosen a part, the picture arrives
     pre-annotated and "what do you notice?" is already answered. */
  { name: 'spotlight overlay',
    sel: '.sci-spotmove:not([data-on="1"])',
    earnedBy: 'pressing "spotlight the next part" after observing' }
];

function legible(el) {
  const cs = getComputedStyle(el);
  return cs.display !== 'none' &&
         cs.visibility !== 'hidden' &&
         parseFloat(cs.opacity) > 0.05;
}

(async () => {
  let chromium;
  try { ({ chromium } = require('playwright-core')); }
  catch (e) {
    console.error('playwright-core not installed. npm install --no-save playwright-core');
    process.exit(2);
  }
  if (!fs.existsSync(EXEC)) {
    console.error('No Chromium at ' + EXEC + ' — set SCI_CHROMIUM.');
    process.exit(2);
  }

  const files = fs.readdirSync(DECKS)
    .filter(f => /^SCI_L_.*\.html$/.test(f) && f.includes(FILTER)).sort();
  if (!files.length) { console.error('no decks matched ' + FILTER); process.exit(2); }

  const browser = await chromium.launch({ executablePath: EXEC, args: ['--no-sandbox'] });
  const leaks = [];
  let slidesWalked = 0;

  for (const file of files) {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const page = await ctx.newPage();
    await page.goto('file://' + path.join(DECKS, file));
    const n = await page.evaluate(() => document.querySelectorAll('.slide').length);

    for (let i = 0; i < n; i++) {
      await page.evaluate(j => window.showSlide && window.showSlide(j), i);
      /* the wait lives in measure.js so no instrument re-derives it */
      await page.waitForTimeout(HOLD_MS);
      slidesWalked++;
      const found = await page.evaluate(({ GATES, legibleSrc }) => {
        const legible = eval('(' + legibleSrc + ')');
        const out = [];
        document.querySelectorAll('.slide.active .sci').forEach(c => {
          const key = c.getAttribute('data-sci-key') || c.getAttribute('data-sci');
          GATES.forEach(g => {
            const bad = [...c.querySelectorAll(g.sel)].filter(legible);
            if (bad.length) out.push({
              key, gate: g.name, count: bad.length, earnedBy: g.earnedBy,
              sample: (bad[0].textContent || '').trim().slice(0, 48) || '(no text)'
            });
          });
        });
        return out;
      }, { GATES, legibleSrc: legible.toString() });
      found.forEach(f => leaks.push(Object.assign({ file, slide: i }, f)));
    }
    await ctx.close();
  }
  await browser.close();

  console.log(`gate-leak: ${files.length} deck(s), ${slidesWalked} slides walked, ` +
              `${GATES.length} gate types, measuring computed style on the live slide`);
  if (!leaks.length) { console.log('no leaks — nothing gated is readable before it is earned'); return; }

  console.log('\nLEAKS:');
  leaks.forEach(l => console.log(
    `  ${l.file} · slide ${l.slide} · ${l.key}\n` +
    `    ${l.count} × ${l.gate} readable — should be earned by ${l.earnedBy}\n` +
    `    e.g. "${l.sample}"`));
  console.log(`\n${leaks.length} leak(s)`);
  process.exit(1);
})();
