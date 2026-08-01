/* Convergence fix pass — the test suite.
 *
 * Every fix in this pass has a test here, and every test was seen failing on the
 * unfixed tree before the fix went in. Run it against either engine by checking
 * out the lessons you want to measure; it reads the lessons as they are on disk.
 *
 *   node reports/convergence/tests/run.mjs
 *
 * Exit 0 only if every test passes.
 */
import { createRequire } from 'module';
const require_ = createRequire(import.meta.url);
const { chromium } = require_(process.env.PLAYWRIGHT_PATH || '/opt/node22/lib/node_modules/playwright');
import { resolve } from 'path';

const ROOT = process.cwd();
const f = p => 'file://' + resolve(ROOT, p);
const L = n => `Science_Teesside/Build/SCI_B_${n}.html`;

/* lesson -> the XP total the lesson showed before convergence */
const XP = { 'W3_Backbones': 13, 'W4_Muscle_Pairs': 9, 'W5_Right_Nutrition': 9,
             'W6_Balanced_Plate': 10, 'W7_Where_Food_Comes_From': 10 };
const LESSONS = Object.keys(XP);

const results = [];
const t = (name, pass, detail) => { results.push({ name, pass, detail }); 
  console.log(`${pass ? 'PASS' : 'FAIL'}  ${name}  ${detail}`); };

const browser = await chromium.launch();

async function page(rel, opts) {
  const ctx = await browser.newContext(Object.assign({ viewport: { width: 1280, height: 720 } }, opts || {}));
  const p = await ctx.newPage();
  await p.goto(f(rel), { waitUntil: 'load' });
  await p.waitForTimeout(1000);
  return { p, ctx };
}

/* ---------------------------------------------------------------- TEST 1
   A hide-gated part revealed by `draw` must be visible. food-svg.js's HIDE_CSS
   lists .g-draw as a reveal class; grow's draw must therefore put it on the
   part, not only on the part's child shapes. */
{
  const html = '<div class="slide active"><div class="ba-stage" id="t" data-ba-asset="plate"' +
    ' data-ba-script="\n  draw drop-apple :: drawn\n  show drop-pasta :: shown\n"></div></div>' +
    ['grow-anim/grow-motion.css', 'grow-anim/grow-anim.css'].map(c => `<link rel="stylesheet" href="${f(c)}">`).join('') +
    ['grow-anim/grow-svg.js', 'grow-anim/grow-svg-bio-animals.js', 'grow-anim/grow-anim.js',
     'grow-anim/compat-build-anim.js', 'build-anim/food-svg.js'].map(j => `<script src="${f(j)}"></script>`).join('');
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 720 } });
  const p = await ctx.newPage();
  await p.goto(f('grow-anim/grow-anim.css'), { waitUntil: 'load' }).catch(() => {});
  await p.setContent(html, { waitUntil: 'load' });
  await p.waitForTimeout(1200);
  const r = await p.evaluate(async () => {
    const st = document.getElementById('t'), API = window.BuildAnim || window.GrowAnim;
    if (!API) return { err: 'no engine' };
    API.reset(st); API.next(st); API.next(st);
    await new Promise(r => setTimeout(r, 1500));
    const g = n => { const e = st.querySelector(`[data-part="${n}"]`);
      return e ? { opacity: getComputedStyle(e).opacity, c: (e.getAttribute('class') || '').trim() } : null; };
    return { drawn: g('drop-apple'), shown: g('drop-pasta') };
  });
  await ctx.close();
  t('hide-gated part revealed by `draw`', r.drawn && r.drawn.opacity === '1',
    `drop-apple opacity=${r.drawn && r.drawn.opacity} classes="${r.drawn && r.drawn.c}" (control: drop-pasta via \`show\` = ${r.shown && r.shown.opacity})`);
}

/* ---------------------------------------------------------------- TEST 2
   The injected engine must survive the HTML parser: no source may close its own
   <script> block. Measured on the lessons as inlined, not on the sources. */
for (const n of LESSONS) {
  const { p, ctx } = await page(L(n));
  const r = await p.evaluate(() => ({
    engine: typeof (window.GrowAnim || window.BuildAnim),
    stages: document.querySelectorAll('.g-stage, .ba-stage').length,
    parts: document.querySelectorAll('svg [data-part]').length,
    stray: [...document.querySelectorAll('script[src]')].map(s => s.getAttribute('src'))
             .filter(s => /grow-anim|build-anim/.test(s))
  }));
  await ctx.close();
  t(`inline survives the parser · ${n}`,
    r.engine === 'object' && r.stages > 0 && r.parts > 0 && r.stray.length === 0,
    `engine=${r.engine} stages=${r.stages} parts=${r.parts} strayScriptSrc=${JSON.stringify(r.stray)}`);
}

/* ---------------------------------------------------------------- TEST 3
   XP parity. The lesson glue counts prediction cards to award XP; the engine
   builds those cards, so the count must not depend on which engine built them. */
for (const n of LESSONS) {
  const { p, ctx } = await page(L(n));
  const r = await p.evaluate(() => ({
    xp: (document.getElementById('xpTotal') || {}).textContent,
    ba: document.querySelectorAll('.ba-pc').length,
    g: document.querySelectorAll('.g-pc').length
  }));
  await ctx.close();
  t(`XP total · ${n}`, String(r.xp) === String(XP[n]),
    `xpTotal=${r.xp} expected=${XP[n]}  (.ba-pc=${r.ba} .g-pc=${r.g})`);
}

/* ---------------------------------------------------------------- TEST 4
   Nothing a stage draws may sit under the lesson's fixed navigation. Checked at
   three real viewports, on the slide that carries the comparison rail. */
for (const [w, h] of [[1280, 720], [1024, 768], [390, 844]]) {
  const { p, ctx } = await page(L('W4_Muscle_Pairs'), { viewport: { width: w, height: h } });
  const r = await p.evaluate(() => {
    const st = document.getElementById('wedo1b-rail');
    document.querySelectorAll('.slide').forEach(s => s.classList.remove('active'));
    st.closest('.slide').classList.add('active');
    const nav = document.querySelector('.controls');
    const navTop = nav ? nav.getBoundingClientRect().top : Infinity;
    const caps = [...st.querySelectorAll('.g-cell > span, .ba-cell > span')];
    return {
      navTop, navRect: nav ? JSON.stringify(nav.getBoundingClientRect()) : null,
      scrolled: st.closest('.slide').scrollTop,
      slideBottom: Math.round(st.closest('.slide').getBoundingClientRect().bottom),
      caps: caps.map(c => { const r = c.getBoundingClientRect();
        return { text: c.textContent.trim().slice(0, 22), bottom: Math.round(r.bottom),
                 left: Math.round(r.left), right: Math.round(r.right) }; })
    };
  });
  await ctx.close();
  const nav = r.navTop;
  const navBox = JSON.parse(r.navRect || '{}');
  /* a caption clears the nav if it ends above it, or is entirely to its left */
  const underNav = r.caps.filter(c => c.bottom > nav && c.right > navBox.left);
  /* a caption that has slipped below the slide's own box is clipped by the
     slide's overflow — invisible, which is not "clear of the nav" either */
  const clipped = r.caps.filter(c => c.bottom > r.slideBottom);
  t(`rail caption clears the nav · ${w}x${h}`,
    underNav.length === 0 && clipped.length === 0 && r.caps.length > 0,
    `navTop=${Math.round(nav)} navLeft=${Math.round(navBox.left)} slideBottom=${r.slideBottom}` +
    ` underNav=${underNav.length} clipped=${clipped.length} captions=${JSON.stringify(r.caps)}`);
}

/* ---------------------------------------------------------------- TEST 5
   `all()` — the Show-all button — must leave the narration on screen, the same
   as pressing Next to the end does. */
for (const n of LESSONS) {
  const { p, ctx } = await page(L(n));
  const r = await p.evaluate(async () => {
    const API = window.BuildAnim || window.GrowAnim;
    let withSay = 0, narrating = 0, blank = [];
    for (const st of document.querySelectorAll('.g-stage, .ba-stage')) {
      const say = st.querySelector('.g-say, .ba-say');
      const state = st._g || st._ba;
      /* a prediction panel's stage carries no script until a card is tapped;
         it has nothing to say and is not part of this claim */
      if (!say || !state || !state.steps.length) continue;
      withSay++;
      API.reset(st); API.all(st);
      await new Promise(r => setTimeout(r, 120));
      const txt = (say.textContent || '').trim();
      if (txt) narrating++; else blank.push(st.id || '?');
    }
    return { withSay, narrating, blank };
  });
  await ctx.close();
  t(`all() narrates · ${n}`, r.withSay > 0 && r.narrating === r.withSay,
    `${r.narrating}/${r.withSay} stages narrating after all()${r.blank.length ? ' blank=' + r.blank.join(',') : ''}`);
}

/* ---------------------------------------------------------------- TEST 6
   BioSVG.list() must report every registered asset, not only the 13 animals —
   the subject libraries register into the same registry. */
const EXPECT_LIST = { 'W3_Backbones': 13, 'W4_Muscle_Pairs': 16, 'W5_Right_Nutrition': 16,
                      'W6_Balanced_Plate': 16, 'W7_Where_Food_Comes_From': 20 };
for (const n of LESSONS) {
  const { p, ctx } = await page(L(n));
  const r = await p.evaluate(() => {
    try {
      return { n: window.BioSVG.list().length, v: window.BioSVG.vertebrates().length,
               i: window.BioSVG.invertebrates().length };
    } catch (e) { return { n: -1, err: String(e) }; }
  });
  await ctx.close();
  t(`BioSVG.list() sees subject assets · ${n}`, r.n === EXPECT_LIST[n],
    `list()=${r.n} expected=${EXPECT_LIST[n]} (vertebrates=${r.v} invertebrates=${r.i})`);
}

await browser.close();
const failed = results.filter(r => !r.pass);
console.log(`\n${results.length - failed.length}/${results.length} passed` +
  (failed.length ? `, ${failed.length} FAILED:\n  ` + failed.map(r => r.name).join('\n  ') : ''));
process.exit(failed.length ? 1 : 0);
