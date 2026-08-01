/* JOB 2 — the failing test is a design limit, so find where the limit actually is.
 *
 * Projector + long-heading is red because a heading long enough to wrap pushes a
 * We Do 2 stage off the foot of the slide, and the picture is already at its
 * floor so nothing in the layout can absorb it. That is only a problem if a real
 * heading can reach that length. This bisects the threshold: the shortest
 * heading, in characters, at which the tightest stage in the unit drops below
 * 8px of clearance.
 *
 *   node reports/convergence/headingthreshold.mjs
 */
import { createRequire } from 'module';
const require_ = createRequire(import.meta.url);
const { chromium } = require_(process.env.PLAYWRIGHT_PATH || '/opt/node22/lib/node_modules/playwright');
import { writeFileSync } from 'fs';
import { resolve } from 'path';

const ROOT = process.cwd();
/* the three cells that go red under the long-heading fixture, at the viewport
   where each of them does it */
const CASES = [
  { lesson: 'SCI_B_W5_Right_Nutrition', stage: 'wedo2-rule', w: 1280, h: 720 },
  { lesson: 'SCI_B_W6_Balanced_Plate', stage: 'wedo2-rule', w: 1280, h: 720 },
  { lesson: 'SCI_B_W7_Where_Food_Comes_From', stage: 'wedo2-rule', w: 1024, h: 768 }
];
const WORD = 'word ';

const b = await chromium.launch();
const out = [];
for (const c of CASES) {
  const ctx = await b.newContext({ viewport: { width: c.w, height: c.h } });
  const p = await ctx.newPage();
  await p.goto('file://' + resolve(ROOT, `Science_Teesside/Build/${c.lesson}.html`), { waitUntil: 'load' });
  await p.waitForTimeout(900);
  const clearanceAt = (len) => p.evaluate(([stageId, len, word]) => {
    const st = document.getElementById(stageId);
    const slide = st.closest('.slide');
    document.querySelectorAll('.slide').forEach(s => s.classList.remove('active'));
    slide.classList.add('active');
    const h = slide.querySelector('h2');
    if (!h) return null;
    if (h.dataset.orig === undefined) h.dataset.orig = h.textContent;
    let t = h.dataset.orig;
    while (t.length < len) t += ' ' + word.repeat(1).trim();
    h.textContent = t.slice(0, len);
    if (window.GrowAnim && window.GrowAnim.fit) window.GrowAnim.fit(st);
    try { (window.BuildAnim || window.GrowAnim).all(st); } catch (e) {}
    const nav = document.querySelector('.controls').getBoundingClientRect();
    const slideBottom = slide.getBoundingClientRect().bottom -
      parseFloat(getComputedStyle(slide).paddingBottom || 0);
    const els = [st.querySelector('.g-canvas') || st]
      .concat([...st.querySelectorAll('.g-cell > span')]);
    let min = Infinity;
    els.forEach(e => {
      const r = e.getBoundingClientRect();
      if (!r.height) return;
      const cn = r.right > nav.left ? nav.top - r.bottom : Infinity;
      min = Math.min(min, cn, slideBottom - r.bottom);
    });
    return { clearance: Math.round(min), headingLen: h.textContent.length,
             headingLines: Math.round(h.getBoundingClientRect().height / parseFloat(getComputedStyle(h).lineHeight)) };
  }, [c.stage, len, WORD]);

  /* bisect on heading length between the real longest (52) and the fixture's */
  let lo = 20, hi = 220, first = null;
  const base = await clearanceAt(lo);
  while (lo < hi) {
    const mid = Math.floor((lo + hi) / 2);
    const r = await clearanceAt(mid);
    if (r.clearance < 8) { hi = mid; first = r; } else { lo = mid + 1; }
  }
  const at = await clearanceAt(lo);
  out.push({ ...c, baseClearance: base.clearance, thresholdChars: lo,
             clearanceAtThreshold: at.clearance, linesAtThreshold: at.headingLines });
  console.log(`${c.lesson.replace('SCI_B_', '').padEnd(24)} ${c.stage} @${c.w}x${c.h}  ` +
    `clear at 20 chars = ${base.clearance}px  ·  first drops below 8px at ` +
    `${lo} chars (${at.clearance}px, heading ${at.headingLines} lines)`);
  await ctx.close();
}
await b.close();
writeFileSync(resolve(ROOT, 'reports/convergence/_data/heading-threshold.json'), JSON.stringify(out, null, 1));
const t = Math.min(...out.map(o => o.thresholdChars));
console.log(`\nthreshold (tightest of the three): ${t} characters`);
console.log(`longest real heading in the ten decks: 52 characters — margin ${t - 52} characters`);
