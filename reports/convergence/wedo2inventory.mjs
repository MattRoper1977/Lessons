/* JOB 2 — quantify the scaled-viewport finding so it can be decided.
 *
 * The cause is content volume, not layout: at 614px of viewport height the
 * We Do 2 slide does not fit. This inventories exactly what is on it and how
 * tall each piece measures, then bisects the viewport height at which it first
 * fits as authored.
 *
 * Reports only. Changes nothing, chooses nothing.
 *
 *   node reports/convergence/wedo2inventory.mjs
 */
import { createRequire } from 'module';
const require_ = createRequire(import.meta.url);
const { chromium } = require_(process.env.PLAYWRIGHT_PATH || '/opt/node22/lib/node_modules/playwright');
import { writeFileSync } from 'fs';
import { resolve } from 'path';

const ROOT = process.cwd();
const DECKS = ['SCI_B_W3_Backbones', 'SCI_B_W4_Muscle_Pairs', 'SCI_B_W5_Right_Nutrition',
               'SCI_B_W6_Balanced_Plate', 'SCI_B_W7_Where_Food_Comes_From'];

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
  /* every direct child of the slide, in document order, with its measured height */
  const parts = [...slide.children].map(el => {
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    return {
      tag: el.tagName.toLowerCase(),
      cls: (el.getAttribute('class') || '').split(/\\s+/)[0] || '',
      text: (el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 44),
      height: Math.round(r.height),
      margin: Math.round(parseFloat(cs.marginTop || 0) + parseFloat(cs.marginBottom || 0))
    };
  }).filter(p => p.height > 0);
  const c = st.querySelector('.g-canvas') || st;
  const cr = c.getBoundingClientRect();
  return {
    viewportH: window.innerHeight,
    slideTop: Math.round(slideR.top), slideHeight: Math.round(slideR.height),
    usableBottom: Math.round(usable), navTop: Math.round(nav.top),
    contentBottom: Math.round(slide.scrollHeight + slideR.top),
    scrollHeight: slide.scrollHeight, clientHeight: slide.clientHeight,
    overflow: slide.scrollHeight - slide.clientHeight,
    clearance: Math.round(usable - cr.bottom),
    fit: st.style.getPropertyValue('--g-fit') || '(none)',
    parts
  };
})`;

const b = await chromium.launch();

/* 1 · inventory at 819x614 */
console.log('=== wedo2-rule slide inventory at 819x614 (1024x768 @125%) ===\n');
const ctx = await b.newContext({ viewport: { width: 819, height: 614 } });
const p = await ctx.newPage();
const inventories = {};
for (const d of DECKS) {
  await p.goto('file://' + resolve(ROOT, `Science_Teesside/Build/${d}.html`), { waitUntil: 'load' });
  await p.waitForTimeout(700);
  inventories[d] = await p.evaluate(new Function('return ' + PROBE)());
}
await ctx.close();

const ref = inventories['SCI_B_W7_Where_Food_Comes_From'];
console.log(`slide box: top ${ref.slideTop}px, height ${ref.slideHeight}px · usable bottom ${ref.usableBottom}px (nav top ${ref.navTop}px)`);
console.log(`slide scrollHeight ${ref.scrollHeight}px vs clientHeight ${ref.clientHeight}px — overflow ${ref.overflow}px\n`);
console.log('W7, every element the slide renders:');
console.log('  ' + 'height'.padStart(7) + '  ' + 'margin'.padStart(6) + '  element');
let total = 0;
ref.parts.forEach(x => { total += x.height + x.margin;
  console.log(`  ${String(x.height).padStart(7)}  ${String(x.margin).padStart(6)}  ${x.tag}.${x.cls} — "${x.text}"`); });
console.log(`  ${String(total).padStart(7)}  ${''.padStart(6)}  TOTAL content height (vs ${ref.clientHeight}px of slide)\n`);

console.log('all five decks at 819x614:');
DECKS.forEach(d => { const v = inventories[d];
  console.log(`  ${d.replace('SCI_B_', '').padEnd(24)} clearance ${String(v.clearance).padStart(5)}px  ` +
    `overflow ${String(v.overflow).padStart(4)}px  --g-fit ${v.fit}  elements ${v.parts.length}`); });

/* 2 · bisect the viewport height at which it fits as authored */
console.log('\n=== minimum viewport height at which each fits as authored (width 819) ===\n');
const mins = {};
for (const d of DECKS) {
  let lo = 500, hi = 1400;
  while (lo < hi) {
    const mid = Math.floor((lo + hi) / 2);
    const c2 = await b.newContext({ viewport: { width: 819, height: mid } });
    const p2 = await c2.newPage();
    await p2.goto('file://' + resolve(ROOT, `Science_Teesside/Build/${d}.html`), { waitUntil: 'load' });
    await p2.waitForTimeout(450);
    const r = await p2.evaluate(new Function('return ' + PROBE)());
    await c2.close();
    if (r && r.clearance >= 8) hi = mid; else lo = mid + 1;
  }
  mins[d] = lo;
  console.log(`  ${d.replace('SCI_B_', '').padEnd(24)} fits at ${lo}px  —  614px is ${lo - 614}px short`);
}
await b.close();
writeFileSync(resolve(ROOT, 'reports/convergence/_data/wedo2-inventory.json'),
  JSON.stringify({ inventories, minimumViewportHeight: mins }, null, 1));
