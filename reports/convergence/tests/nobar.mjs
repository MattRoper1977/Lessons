/* JOB 1 — the --g-fit patch, brought up to the standard the rest of the work met.
 *
 * The claim: every stage gets fitted, whether or not it renders a control bar.
 * Before the patch, paint() opened with `if (!st || !bar) return;` and the fit()
 * call at its tail was unreachable for any stage carrying data-grow-nobar.
 *
 * This enumerates every stage in all ten Autumn 1 decks, records whether it
 * carries the attribute, drives it, and asserts --g-fit was set. Run it against
 * the reverted guard to see it fail and name the stages; against the patch to
 * see it pass.
 *
 *   node reports/convergence/tests/nobar.mjs
 */
import { createRequire } from 'module';
const require_ = createRequire(import.meta.url);
const { chromium } = require_(process.env.PLAYWRIGHT_PATH || '/opt/node22/lib/node_modules/playwright');
import { resolve } from 'path';

const ROOT = process.cwd();
const DECKS = [
  'Science_Teesside/Build/SCI_B_W3_Backbones.html',
  'Science_Teesside/Build/SCI_B_W4_Muscle_Pairs.html',
  'Science_Teesside/Build/SCI_B_W5_Right_Nutrition.html',
  'Science_Teesside/Build/SCI_B_W6_Balanced_Plate.html',
  'Science_Teesside/Build/SCI_B_W7_Where_Food_Comes_From.html',
  'Science_Teesside/Grow/SCI_G_W3_Friction.html',
  'Science_Teesside/Grow/SCI_G_W4_Mechanisms.html',
  'Science_Teesside/Grow/SCI_G_W5_Fair_Test.html',
  'Science_Teesside/Grow/SCI_G_W6_Earth_And_Planets.html',
  'Science_Teesside/Grow/SCI_G_W7_The_Moon.html'
];

const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1280, height: 720 } });
const p = await ctx.newPage();
const rows = [];
for (const rel of DECKS) {
  await p.goto('file://' + resolve(ROOT, rel), { waitUntil: 'load' });
  await p.waitForTimeout(700);
  const r = await p.evaluate(() => {
    const $$ = (s, r) => [...(r || document).querySelectorAll(s)];
    const out = [];
    $$('.g-stage').forEach((st, i) => {
      const slide = st.closest('.slide');
      if (!slide) return;
      $$('.slide').forEach(s => s.classList.remove('active'));
      slide.classList.add('active');
      /* drive it exactly as the lesson would, with no explicit fit() nudge */
      try { window.GrowAnim.all(st); } catch (e) {}
      out.push({
        stage: st.id || ('stage' + (i + 1)),
        slideTitle: slide.getAttribute('data-title') || '?',
        nobar: st.hasAttribute('data-grow-nobar') || st.hasAttribute('data-ba-nobar'),
        hasBar: !!st.querySelector('.g-bar'),
        pictures: st.querySelectorAll('.g-svg').length,
        laidOut: st.getBoundingClientRect().height > 0,
        frame: st.getAttribute('data-grow-frame') || '(default)',
        fit: st.style.getPropertyValue('--g-fit') || ''
      });
    });
    /* A prediction panel's stage renders nothing until a card is tapped, so it
       has no picture to fit and is correctly skipped. Tap one and check the
       stage it builds — that is the sibling path, and missing it would be the
       same family of bug as the one being fixed. */
    $$('.g-predict').forEach((panel, pi) => {
      const slide = panel.closest('.slide');
      if (!slide) return;
      $$('.slide').forEach(s => s.classList.remove('active'));
      slide.classList.add('active');
      const card = $$('.g-pc', panel)[0];
      if (!card) return;
      card.click();
      $$('.g-stage', panel).forEach(st => {
        try { window.GrowAnim.all(st); } catch (e) {}
        out.push({
          stage: (st.id || 'predict' + (pi + 1)) + ' (after card tap)',
          slideTitle: slide.getAttribute('data-title') || '?',
          nobar: st.hasAttribute('data-grow-nobar'),
          hasBar: !!st.querySelector('.g-bar'),
          pictures: st.querySelectorAll('.g-svg').length,
          laidOut: st.getBoundingClientRect().height > 0,
          frame: st.getAttribute('data-grow-frame') || '(default)',
          fit: st.style.getPropertyValue('--g-fit') || ''
        });
      });
    });
    return out;
  });
  r.forEach(x => rows.push({ deck: rel.split('/').pop().replace('.html', ''), ...x }));
}
await b.close();

const nobar = rows.filter(r => r.nobar);
const withBar = rows.filter(r => !r.nobar);
/* The claim is about stages that have a picture AND are on screen. A stage
   rendering no picture has nothing to fit; a stage inside a collapsed We Do
   panel has a zero-height box and cannot be measured at all, so asserting on
   either would be a test of the wrong thing. Both are counted, not hidden. */
const withPicture = rows.filter(r => r.pictures > 0 && r.laidOut);
const noPicture = rows.filter(r => r.pictures === 0);
const notLaidOut = rows.filter(r => r.pictures > 0 && !r.laidOut);
const unfitted = withPicture.filter(r => !r.fit);

console.log(`stages driven across ten decks: ${rows.length}`);
console.log(`  visible and rendering a picture: ${withPicture.length}` +
  `   rendering none: ${noPicture.length}   inside a collapsed panel: ${notLaidOut.length}`);
console.log(`  carrying data-*-nobar: ${nobar.length}   rendering a control bar: ${withBar.length}`);
console.log(`  picture-bearing stages left with no --g-fit: ${unfitted.length}`);
if (unfitted.length) {
  console.log('\n  UNFITTED:');
  unfitted.forEach(r => console.log(`    ${r.deck} / ${r.stage.padEnd(16)} slide "${r.slideTitle}"` +
    `  nobar=${r.nobar}  bar=${r.hasBar}  frame=${r.frame}`));
}
console.log('\n  nobar stage types (distinct id + frame across the ten decks):');
[...new Set(nobar.map(r => `${r.stage}  frame=${r.frame}`))].sort()
  .forEach(k => console.log(`    ${k}  ×${nobar.filter(r => `${r.stage}  frame=${r.frame}` === k).length} decks`));

const pass = unfitted.length === 0;
console.log(`\n  bar-carrying stages fitted: ` +
  `${withBar.filter(r => r.pictures > 0 && r.fit).length}/${withBar.filter(r => r.pictures > 0).length}` +
  `   nobar stages fitted: ${nobar.filter(r => r.pictures > 0 && r.fit).length}/${nobar.filter(r => r.pictures > 0).length}`);
console.log(`\n${pass ? 'PASS' : 'FAIL'} — every picture-bearing stage fitted, with or without a control bar`);
process.exit(pass ? 0 : 1);
