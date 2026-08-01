/* PHASE A3 — the display gate.
 *
 * The deck hides every slide but one with `.slide { display: none }` and shows
 * the current one with `.slide.active`. That is a GATE, and this estate has now
 * been bitten three times by the same family: a new rule landing at higher
 * specificity than an existing gate defeats the gate silently.
 *
 *   .g-in's held keyframe            beat  opacity: 0
 *   a private class                  shadowed a shared verb
 *   .slide.wedo2-layout { display: grid }  beat  .slide { display: none }
 *
 * The third one was measured: every other slide's width halved from 742px to
 * 403px because two slides shared the flex row, and every picture collapsed to
 * its 96px floor. The overflow numbers being optimised at the time IMPROVED.
 *
 * This is the direct analogue of the opacity-gate check: no rule may leave a
 * non-active slide laid out. It asserts on computed style, so it catches any
 * selector at any specificity, not just the one that caused it.
 *
 *   node reports/convergence/tests/displaygate.mjs
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
/* the short viewport is the one where a height-scoped rule can fire */
const VIEWPORTS = [[1280, 720], [819, 614], [683, 512]];

const b = await chromium.launch();
const leaks = [];
let checked = 0, slidesSeen = 0;
for (const [w, h] of VIEWPORTS) {
  const ctx = await b.newContext({ viewport: { width: w, height: h } });
  const p = await ctx.newPage();
  for (const rel of DECKS) {
    await p.goto('file://' + resolve(ROOT, rel), { waitUntil: 'load' });
    await p.waitForTimeout(400);
    const r = await p.evaluate(() => {
      const $$ = s => [...document.querySelectorAll(s)];
      const slides = $$('.slide');
      const out = { total: slides.length, checks: 0, leaked: [] };
      /* walk every slide into the active position in turn, so every slide is
         seen both active and inactive at least once */
      slides.forEach((target, i) => {
        slides.forEach(s => s.classList.remove('active'));
        target.classList.add('active');
        slides.forEach((s, j) => {
          if (j === i) return;
          out.checks++;
          const d = getComputedStyle(s).display;
          if (d !== 'none') {
            out.leaked.push({ index: j + 1,
              title: s.getAttribute('data-title') || '(untitled)',
              cls: (s.getAttribute('class') || '').trim(), display: d,
              width: Math.round(s.getBoundingClientRect().width) });
          }
        });
      });
      /* one entry per offending slide, not per pairing */
      const seen = new Set();
      out.leaked = out.leaked.filter(l => { const k = l.index; if (seen.has(k)) return false; seen.add(k); return true; });
      return out;
    });
    checked += r.checks; slidesSeen += r.total;
    r.leaked.forEach(l => leaks.push({ deck: rel.split('/').pop(), viewport: `${w}x${h}`, ...l }));
  }
  await ctx.close();
}
await b.close();

console.log(`slides walked: ${slidesSeen} across ${DECKS.length} decks × ${VIEWPORTS.length} viewports`);
console.log(`inactive-slide display assertions: ${checked}`);
if (!checked) { console.log('FAIL — the input set was empty; the check proved nothing'); process.exit(1); }
if (leaks.length) {
  console.log(`\n  SLIDES LAID OUT WHILE NOT ACTIVE: ${leaks.length}`);
  leaks.forEach(l => console.log(`    ${l.deck} @${l.viewport}  slide ${l.index} "${l.title}"` +
    `  display=${l.display}  width=${l.width}px  class="${l.cls}"`));
}
console.log(`\n${leaks.length ? 'FAIL' : 'PASS'} — no rule leaves a non-active slide laid out`);
process.exit(leaks.length ? 1 : 0);
