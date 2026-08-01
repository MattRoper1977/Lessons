/* JOB 4 — how much smaller the explanation is, for Matt to judge.
 *
 * Both READMEs open with "the animation is the explanation". This pass makes
 * every picture on a stage smaller. That is a pedagogy question, not a layout
 * detail, so the numbers and the pair of renders go in front of him rather than
 * being left to inference. Nothing is adjusted to compensate.
 *
 *   node reports/convergence/pictureheight.mjs <label> <outdir>
 */
import { createRequire } from 'module';
const require_ = createRequire(import.meta.url);
const { chromium } = require_(process.env.PLAYWRIGHT_PATH || '/opt/node22/lib/node_modules/playwright');
import { mkdirSync, writeFileSync } from 'fs';
import { resolve } from 'path';

const LABEL = process.argv[2] || 'after';
const OUT = process.argv[3] || 'reports/convergence/_pictures';
const ROOT = process.cwd();
mkdirSync(resolve(ROOT, OUT), { recursive: true });

/* one plain stage and one comparison rail, the two shapes a lesson uses most */
const CASES = [
  { key: 'W4-arm',  lesson: 'SCI_B_W4_Muscle_Pairs', stage: 'ido1-arm',     slide: 5 },
  { key: 'W4-rail', lesson: 'SCI_B_W4_Muscle_Pairs', stage: 'wedo1b-rail',  slide: 7 },
  { key: 'W6-plate', lesson: 'SCI_B_W6_Balanced_Plate', stage: 'ido1-plate', slide: 4 }
];
const VIEWPORTS = [[1280, 720], [1366, 768]];

const b = await chromium.launch();
const rows = [];
for (const c of CASES) {
  for (const [w, h] of VIEWPORTS) {
    const ctx = await b.newContext({ viewport: { width: w, height: h } });
    const p = await ctx.newPage();
    await p.goto('file://' + resolve(ROOT, `Science_Teesside/Build/${c.lesson}.html`), { waitUntil: 'load' });
    await p.waitForTimeout(900);
    const m = await p.evaluate((stageId) => {
      const st = document.getElementById(stageId);
      document.querySelectorAll('.slide').forEach(s => s.classList.remove('active'));
      st.closest('.slide').classList.add('active');
      try { (window.BuildAnim || window.GrowAnim).all(st); } catch (e) {}
      const svg = st.querySelector('svg').getBoundingClientRect();
      return { h: Math.round(svg.height), w: Math.round(svg.width) };
    }, c.stage);
    await p.waitForTimeout(600);
    const f = `${OUT}/${c.key}--${w}x${h}--${LABEL}.png`;
    await p.screenshot({ path: resolve(ROOT, f) });
    rows.push({ case: c.key, viewport: `${w}x${h}`, pictureH: m.h, pictureW: m.w, png: f });
    console.log(`${c.key.padEnd(9)} ${String(w) + 'x' + h}  picture ${m.w}x${m.h}  -> ${f}`);
    await ctx.close();
  }
}
await b.close();
writeFileSync(resolve(ROOT, `reports/convergence/_data/pictures-${LABEL}.json`), JSON.stringify(rows, null, 1));
