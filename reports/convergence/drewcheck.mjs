/* JOB 0 — settle the ba-drew judgement per instance, not in aggregate.
 *
 * The prep pass called the draw-verb class-placement difference cosmetic on the
 * strength of an aggregate visibility census. An aggregate cannot clear a
 * per-part claim. This walks each affected part through every step of its own
 * stage and records, at each step:
 *
 *   partClasses    what the PART element carries
 *   kidClasses     what its child shapes carry
 *   opacity/vis    computed style ON THE PART
 *   inkedPx        a paint measurement: the part's own bounding box area in CSS
 *                  pixels, which is 0 if it is not laid out at all
 *
 * Run once per engine and diff. A difference in partClasses that comes with an
 * identical opacity/visibility/inkedPx at every step is genuinely cosmetic; a
 * difference in any of the latter three is not.
 */
import { createRequire } from 'module';
const require_ = createRequire(import.meta.url);
const { chromium } = require_(process.env.PLAYWRIGHT_PATH || '/opt/node22/lib/node_modules/playwright');
import { mkdirSync, writeFileSync } from 'fs';
import { dirname, resolve, basename } from 'path';

const OUT = process.argv[process.argv.indexOf('--out') + 1];
const ROOT = process.cwd();

/* The 13 affected part instances, from the v1 step-state diff. */
const TARGETS = {
  'SCI_B_W3_Backbones': { 'ido1-fish': ['ribs', 'skull'],
                          'ido2-say': ['limbs', 'pelvis', 'ribs', 'skull'],
                          'wedo1b-rail': ['limbs', 'pelvis', 'ribs', 'skull'] },
  'SCI_B_W4_Muscle_Pairs': { 'ido1-arm': ['forearm', 'humerus'] },
  'SCI_B_W6_Balanced_Plate': { 'ido1-plate': ['rim'] }
};
const LESSONS = {
  'SCI_B_W3_Backbones': 'Science_Teesside/Build/SCI_B_W3_Backbones.html',
  'SCI_B_W4_Muscle_Pairs': 'Science_Teesside/Build/SCI_B_W4_Muscle_Pairs.html',
  'SCI_B_W6_Balanced_Plate': 'Science_Teesside/Build/SCI_B_W6_Balanced_Plate.html'
};

const b = await chromium.launch();
const out = {};
for (const [name, rel] of Object.entries(LESSONS)) {
  const ctx = await b.newContext({ viewport: { width: 1280, height: 720 } });
  const p = await ctx.newPage();
  await p.goto('file://' + resolve(ROOT, rel), { waitUntil: 'load' });
  await p.waitForTimeout(900);
  out[name] = await p.evaluate(async (spec) => {
    const $$ = (s, r) => [...(r || document).querySelectorAll(s)];
    const API = window.BuildAnim || window.GrowAnim;
    document.querySelectorAll('.slide').forEach(s => s.classList.add('active'));
    const res = {};
    for (const [stageId, parts] of Object.entries(spec)) {
      const stage = document.getElementById(stageId);
      if (!stage) { res[stageId] = 'MISSING STAGE'; continue; }
      const st = stage._g || stage._ba;
      API.reset(stage);
      const rows = {};
      parts.forEach(pn => { rows[pn] = []; });
      const sample = () => {
        parts.forEach(pn => {
          /* a rail has the same part name in several cells; take them all */
          const els = $$(`[data-part="${pn}"]`, stage);
          rows[pn].push(els.map(e => {
            const cs = getComputedStyle(e);
            const r = e.getBoundingClientRect();
            const kids = $$('path,line,polyline,polygon,rect,circle,ellipse', e);
            const kidcls = [...new Set(kids.map(k => (k.getAttribute('class') || '').trim()).filter(Boolean))].sort();
            return {
              partClasses: (e.getAttribute('class') || '').trim(),
              kidClasses: kidcls.join('|'),
              opacity: cs.opacity, visibility: cs.visibility, display: cs.display,
              inkedPx: Math.round(r.width * r.height)
            };
          }));
        });
      };
      /* settle each step so a running animation is not mistaken for a hidden part */
      sample();
      for (let n = 0; n < st.steps.length; n++) {
        API.next(stage);
        const s2 = stage._g || stage._ba; if (s2.paused) s2.paused = false;
        await new Promise(r => setTimeout(r, 1400));
        sample();
      }
      res[stageId] = rows;
    }
    return res;
  }, TARGETS[name]);
  await ctx.close();
}
await b.close();
mkdirSync(dirname(resolve(ROOT, OUT)), { recursive: true });
writeFileSync(resolve(ROOT, OUT), JSON.stringify(out, null, 1));
console.log('wrote ' + OUT);
