/* JOB 1 — derive the height breakpoint from measurement.
 *
 * For each viewport WIDTH that actually occurs in the matrix, bisect the
 * viewport HEIGHT at which the We Do 2 slide's single-column arrangement stops
 * fitting, for each of the five decks. The breakpoint has to sit above every
 * height where the single column fails and below every height where it works,
 * or it will either fire on a viewport that is fine or fail to fire on one that
 * is not. The measurement says whether such a value exists.
 *
 *   node reports/convergence/breakpoint.mjs
 */
import { createRequire } from 'module';
const require_ = createRequire(import.meta.url);
const { chromium } = require_(process.env.PLAYWRIGHT_PATH || '/opt/node22/lib/node_modules/playwright');
import { writeFileSync } from 'fs';
import { resolve } from 'path';

const ROOT = process.cwd();
const DECKS = ['SCI_B_W3_Backbones', 'SCI_B_W4_Muscle_Pairs', 'SCI_B_W5_Right_Nutrition',
               'SCI_B_W6_Balanced_Plate', 'SCI_B_W7_Where_Food_Comes_From'];
const WIDTHS = [1920, 1536, 1366, 1280, 1093, 1024, 819, 683];

const PROBE = `(function () {
  const $$ = (s, r) => [...(r || document).querySelectorAll(s)];
  const st = document.getElementById('wedo2-rule');
  if (!st) return null;
  const slide = st.closest('.slide');
  $$('.slide').forEach(s => s.classList.remove('active'));
  slide.classList.add('active');
  try { window.GrowAnim.all(st); } catch (e) {}
  const nav = document.querySelector('.controls').getBoundingClientRect();
  const slideR = slide.getBoundingClientRect();
  const usable = Math.min(nav.top, slideR.bottom - parseFloat(getComputedStyle(slide).paddingBottom || 0));
  const last = slide.children[slide.children.length - 1].getBoundingClientRect();
  return { clearance: Math.round(usable - last.bottom),
           overflow: slide.scrollHeight - slide.clientHeight };
})`;

const b = await chromium.launch();
const grid = {};
for (const w of WIDTHS) {
  grid[w] = {};
  for (const d of DECKS) {
    let lo = 420, hi = 1200;
    while (lo < hi) {
      const mid = Math.floor((lo + hi) / 2);
      const ctx = await b.newContext({ viewport: { width: w, height: mid } });
      const p = await ctx.newPage();
      await p.goto('file://' + resolve(ROOT, `Science_Teesside/Build/${d}.html`), { waitUntil: 'load' });
      await p.waitForTimeout(380);
      const r = await p.evaluate(new Function('return ' + PROBE)());
      await ctx.close();
      if (r && r.clearance >= 8 && r.overflow <= 0) hi = mid; else lo = mid + 1;
    }
    grid[w][d] = lo;
  }
  const vals = DECKS.map(d => grid[w][d]);
  console.log(`width ${String(w).padStart(4)}  min-fit height per deck: ${vals.map(v => String(v).padStart(4)).join(' ')}   worst ${Math.max(...vals)}`);
}
await b.close();

const worstPerWidth = Object.fromEntries(WIDTHS.map(w => [w, Math.max(...DECKS.map(d => grid[w][d]))]));
writeFileSync(resolve(ROOT, 'reports/convergence/_data/breakpoint-derivation.json'),
  JSON.stringify({ grid, worstPerWidth }, null, 1));

/* Which real viewports does the single column already serve, and which not? */
const REAL = [[1280,720],[1366,768],[1920,1080],[1024,768],[1536,864],[819,614],[1093,614],[683,512],[390,844]];
console.log('\nreal viewports against the worst deck at their own width:');
const works = [], fails = [];
REAL.forEach(([w, h]) => {
  const need = worstPerWidth[w];
  if (need === undefined) { console.log(`  ${w}x${h}  (width not measured)`); return; }
  const ok = h >= need;
  (ok ? works : fails).push(h);
  console.log(`  ${String(w)+'x'+h}`.padEnd(12) + `needs ${String(need).padStart(4)}px  ->  ${ok ? 'single column FITS' : 'single column FAILS'}`);
});
console.log(`\n  heights where the single column fails: ${fails.sort((a,b)=>a-b).join(', ')}`);
console.log(`  heights where it works:               ${works.sort((a,b)=>a-b).join(', ')}`);
if (fails.length && works.length) {
  const lo = Math.max(...fails), hi = Math.min(...works);
  console.log(`\n  a single max-height breakpoint must satisfy  ${lo} < T <= ${hi - 1}` +
    `   (fires below ${hi}, never on ${hi} or above)`);
}
