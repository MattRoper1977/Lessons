/* JOB 3(b) — the one call made on Matt's behalf, rendered both ways.
 *
 * The frame factors live in four CSS custom properties. This renders the same
 * slide with GROW's numbers (the default adopted here) and with BUILD's, by
 * overriding those four properties at run time — which is exactly what changing
 * them in grow-anim.css would do. If Matt prefers BUILD's, the revert is those
 * four values and nothing else.
 *
 *   node reports/convergence/framecompare.mjs
 */
import { createRequire } from 'module';
const require_ = createRequire(import.meta.url);
const { chromium } = require_(process.env.PLAYWRIGHT_PATH || '/opt/node22/lib/node_modules/playwright');
import { mkdirSync } from 'fs';
import { resolve } from 'path';

const ROOT = process.cwd();
const OUT = 'reports/convergence/_frames';
mkdirSync(resolve(ROOT, OUT), { recursive: true });

/* one slide per frame size actually used in the unit */
const SHOTS = [
  { name: 'tall-rail', lesson: 'SCI_B_W4_Muscle_Pairs', stage: 'wedo1b-rail' },
  { name: 'tall-rail-w3', lesson: 'SCI_B_W3_Backbones', stage: 'wedo1b-rail' },
  { name: 'default-frame', lesson: 'SCI_B_W6_Balanced_Plate', stage: 'ido1-plate' }
];
const SETS = {
  /* adopted here */
  'grow': { '--g-frame-default': '.46', '--g-frame-wide': '.34', '--g-frame-mini': '.20', '--g-frame-tall': '.58' },
  /* BUILD's factors on the new basis — same proportions, still clears the nav */
  'build': { '--g-frame-default': '.46', '--g-frame-wide': '.34', '--g-frame-mini': '.24', '--g-frame-tall': '.44' },
  /* build-anim's ORIGINAL absolute sizes: BUILD's factors with the chrome
     reserve switched off, i.e. 44vh of the whole viewport. Included because
     "revert to BUILD's numbers" could mean either, and they are not the same
     picture — this one is the bigger of the two and puts the caption back
     under the navigation. */
  'build-absolute': { '--g-chrome-reserve': '0px', '--g-frame-default': '.46',
                      '--g-frame-wide': '.34', '--g-frame-mini': '.24', '--g-frame-tall': '.44' }
};

const b = await chromium.launch();
for (const s of SHOTS) {
  for (const [set, vars] of Object.entries(SETS)) {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 720 } });
    const p = await ctx.newPage();
    await p.goto('file://' + resolve(ROOT, `Science_Teesside/Build/${s.lesson}.html`), { waitUntil: 'load' });
    await p.waitForTimeout(900);
    const geom = await p.evaluate(([stageId, vars]) => {
      Object.entries(vars).forEach(([k, v]) => document.documentElement.style.setProperty(k, v));
      const st = document.getElementById(stageId);
      document.querySelectorAll('.slide').forEach(x => x.classList.remove('active'));
      st.closest('.slide').classList.add('active');
      try { (window.BuildAnim || window.GrowAnim).all(st); } catch (e) {}
      const nav = document.querySelector('.controls').getBoundingClientRect();
      const svg = st.querySelector('svg').getBoundingClientRect();
      const cap = st.querySelector('.g-cell > span, .ba-cell > span');
      return { svgH: Math.round(svg.height), stageBottom: Math.round(st.getBoundingClientRect().bottom),
               slideBottom: Math.round(st.closest('.slide').getBoundingClientRect().bottom),
               navTop: Math.round(nav.top),
               capBottom: cap ? Math.round(cap.getBoundingClientRect().bottom) : null };
    }, [s.stage, vars]);
    await p.waitForTimeout(700);
    const f = `${OUT}/${s.name}--${set}.png`;
    await p.screenshot({ path: resolve(ROOT, f) });
    console.log(`${s.name.padEnd(16)} ${set.padEnd(6)} svgH=${String(geom.svgH).padStart(4)}` +
      ` stageBottom=${String(geom.stageBottom).padStart(4)} capBottom=${String(geom.capBottom).padStart(4)}` +
      ` navTop=${geom.navTop} slideBottom=${geom.slideBottom}  -> ${f}`);
    await ctx.close();
  }
}
await b.close();
