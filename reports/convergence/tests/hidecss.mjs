/* JOB 0, the named suspect — proved or disproved directly, not inferred.
 *
 * food-svg.js's HIDE_CSS hides every [data-part^="drop-"] / [data-part^="food-"]
 * at opacity 0 and un-hides on one of four classes:
 *
 *     ON = ['.ba-fadein', '.ba-drew', '.g-in', '.g-draw']
 *
 * grow-anim's draw verb never puts g-draw on the PART — only on the part's child
 * shapes. If that is right, the .g-draw entry in that list is dead, and a script
 * that reveals a hide-gated part with `draw` alone leaves it invisible under the
 * converged engine while it worked under build-anim.
 *
 * This builds the minimal case on each engine and measures the computed opacity
 * of the part after `draw`. It is a real test: it must FAIL on the unfixed tree.
 *
 *   node reports/convergence/tests/hidecss.mjs <engine-dir>
 *   engine-dir = build-anim | grow-anim
 */
import { createRequire } from 'module';
const require_ = createRequire(import.meta.url);
const { chromium } = require_(process.env.PLAYWRIGHT_PATH || '/opt/node22/lib/node_modules/playwright');
import { resolve } from 'path';

const ENGINE = process.argv[2] || 'grow-anim';
const ROOT = process.cwd();
const f = p => 'file://' + resolve(ROOT, p);

const SRC = ENGINE === 'build-anim'
  ? { css: ['build-anim/build-anim.css'],
      js: ['build-anim/bio-svg.js', 'build-anim/food-svg.js', 'build-anim/build-anim.js'] }
  : { css: ['grow-anim/grow-motion.css', 'grow-anim/grow-anim.css'],
      js: ['grow-anim/grow-svg.js', 'grow-anim/grow-svg-bio-animals.js', 'grow-anim/grow-anim.js',
           'grow-anim/compat-build-anim.js', 'build-anim/food-svg.js'] };

const html = '<div class="slide active">' +
  '<div class="ba-stage" id="t" data-ba-asset="plate" data-ba-script="\n' +
  '  draw drop-apple   :: drawn, not shown\n' +
  '  show drop-pasta   :: shown\n' +
  '"></div></div>' +
  SRC.css.map(c => `<link rel="stylesheet" href="${f(c)}">`).join('') +
  SRC.js.map(j => `<script src="${f(j)}"></script>`).join('');

const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1280, height: 720 } })).newPage();
const errs = [];
p.on('pageerror', e => errs.push(String(e)));
await p.goto(f('build-anim/'), { waitUntil: 'load' }).catch(() => {});
await p.setContent(html, { waitUntil: 'load' });
await p.waitForTimeout(1500);

const r = await p.evaluate(async () => {
  const st = document.getElementById('t');
  const API = window.BuildAnim || window.GrowAnim;
  if (!API) return { error: 'no engine' };
  API.reset(st);
  API.next(st);                                     /* draw drop-apple */
  API.next(st);                                     /* show drop-pasta */
  await new Promise(r => setTimeout(r, 1600));
  const read = n => {
    const e = st.querySelector(`[data-part="${n}"]`);
    if (!e) return { missing: true };
    const cs = getComputedStyle(e);
    return { cls: (e.getAttribute('class') || '').trim(), opacity: cs.opacity,
             kidCls: [...new Set([...e.querySelectorAll('path,circle,ellipse,rect,polygon')]
               .map(k => (k.getAttribute('class') || '').trim()).filter(Boolean))].join('|') };
  };
  return { drawn: read('drop-apple'), shown: read('drop-pasta') };
});
await b.close();

const ok = r.drawn && r.drawn.opacity === '1';
console.log(`${ENGINE.padEnd(11)} draw drop-apple -> opacity ${r.drawn && r.drawn.opacity}` +
  `  partClasses="${r.drawn && r.drawn.cls}"  kidClasses="${r.drawn && r.drawn.kidCls}"`);
console.log(`${''.padEnd(11)} show drop-pasta -> opacity ${r.shown && r.shown.opacity}` +
  `  partClasses="${r.shown && r.shown.cls}"`);
if (errs.length) console.log('  pageerrors: ' + errs.join(' | '));
console.log(ok ? 'PASS — a hide-gated part revealed by `draw` is visible'
                : 'FAIL — `draw` left a hide-gated part at opacity 0');
process.exit(ok ? 0 : 1);
