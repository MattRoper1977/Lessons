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
import { writeFileSync } from 'fs';

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

/* The clearance matrix is 75 page loads. Contexts are the expensive part, so it
   reuses one context per (fixture, viewport) and navigates between lessons. */
async function viewportRun(w, h, fn) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h } });
  const p = await ctx.newPage();
  for (const n of LESSONS) {
    await p.goto(f(L(n)), { waitUntil: 'load' });
    await p.waitForTimeout(550);
    await fn(p, n);
  }
  await ctx.close();
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
   Nothing a stage draws may sit under the lesson's fixed navigation, and nothing
   may be clipped by the foot of the slide either. v2 tested one stage at three
   viewports, which is the same one-slide tuning problem at a larger scale, so
   this runs EVERY stage in every lesson at every viewport the school's rooms
   actually use, and reports the worst clearance anywhere in the set.

   Two adversarial fixtures are forced on top of the captions that happen to
   exist today: a caption long enough to wrap to two lines, and a heading long
   enough to push the whole stage down. Both must hold the same two conditions. */
/* Nominal viewports, plus the ones Windows display scaling actually produces —
   scaling changes the CSS viewport, so a room running 1024x768 at 125% is a
   819x614 page, which is not any of the nominal cells. 1024x768 at 150% is the
   pessimal realistic classroom. */
const VIEWPORTS = [
  [1280, 720], [1366, 768], [1920, 1080], [1024, 768], [390, 844],
  [819, 614],    /* 1024x768  @125% */
  [1093, 614],   /* 1366x768  @125% */
  [1536, 864],   /* 1920x1080 @125% */
  [683, 512]     /* 1024x768  @150% — pessimal */
];
const SCALED = ['819x614', '1093x614', '1536x864', '683x512'];
const MATRIX = [];
let worst = { px: Infinity };

const PROBE = `(function (fixture) {
  const $$ = (s, r) => [...(r || document).querySelectorAll(s)];
  const vh = window.innerHeight;
  const nav = document.querySelector('.controls');
  const navRect = nav ? nav.getBoundingClientRect() : null;
  const out = [];
  $$('.slide').forEach(sl => sl.classList.remove('active'));
  $$('.g-stage, .ba-stage').forEach((stage, i) => {
    const slide = stage.closest('.slide');
    if (!slide) return;
    $$('.slide').forEach(s => s.classList.remove('active'));
    slide.classList.add('active');
    if (fixture === 'wrap') {
      $$('.g-cell > span, .ba-cell > span', stage).forEach(c => {
        c.textContent = c.textContent + ' — and this is the sort of caption a teacher writes when one word will not do';
      });
    }
    if (fixture === 'bigfont') {
      document.documentElement.style.fontSize = '20px';   /* container default is 16px */
    }
    if (fixture === 'heading') {
      const h = slide.querySelector('h2');
      if (h) h.textContent = h.textContent + ' — with a much longer title of the kind that wraps onto a second and even a third line on a projector at the back of a classroom';
    }
    if (window.GrowAnim && window.GrowAnim.fit) window.GrowAnim.fit(stage);
    try { (window.BuildAnim || window.GrowAnim).all(stage); } catch (e) {}
    const slideR = slide.getBoundingClientRect();
    const slideBottom = slideR.bottom - parseFloat(getComputedStyle(slide).paddingBottom || 0);
    /* everything the stage actually draws: the picture, its captions, its notes */
    const drawn = [stage.querySelector('.g-canvas, .ba-canvas') || stage]
      .concat($$('.g-cell > span, .ba-cell > span, .g-dual figcaption', stage));
    let minClear = Infinity, offender = null;
    drawn.forEach(e => {
      const r = e.getBoundingClientRect();
      if (!r.height) return;
      const clearNav = (navRect && r.right > navRect.left) ? navRect.top - r.bottom : Infinity;
      const clearSlide = slideBottom - r.bottom;
      const c = Math.min(clearNav, clearSlide);
      if (c < minClear) { minClear = c; offender = (e.className || e.tagName) + ''; }
    });
    out.push({
      stage: stage.id || ('stage' + (i + 1)),
      slide: slide.getAttribute('data-title') || '?',
      clearance: Math.round(minClear), offender,
      svgH: Math.round((stage.querySelector('svg') || { getBoundingClientRect: () => ({ height: 0 }) }).getBoundingClientRect().height),
      fit: stage.style.getPropertyValue('--g-fit') || '(none)'
    });
  });
  return { navTop: navRect ? Math.round(navRect.top) : null, vh, stages: out };
})`;

for (const fixture of [null, 'wrap', 'heading', 'bigfont']) {
  for (const [w, h] of VIEWPORTS) {
    await viewportRun(w, h, async (p, n) => {
      const r = await p.evaluate(new Function('return ' + PROBE)(), fixture);
      r.stages.forEach(st => {
        MATRIX.push({ fixture: fixture || 'as-authored', viewport: `${w}x${h}`, lesson: n, ...st });
        if (st.clearance < worst.px) worst = { px: st.clearance, where: `${n} / ${st.stage}`,
          viewport: `${w}x${h}`, fixture: fixture || 'as-authored', offender: st.offender };
      });
    });
  }
}
writeFileSync(resolve(ROOT, 'reports/convergence/_data/clearance-matrix.json'),
  JSON.stringify({ worst, cells: MATRIX }, null, 1));
{
  const measured = MATRIX.filter(m => m.clearance !== null);
  /* A teacher at a projector does not scroll: on those viewports the whole
     stage has to be on screen. A phone scrolls as a matter of course, so the
     claim there is weaker and is asserted separately rather than folded in. */
  /* Nominal and scaled are two different claims and are asserted separately: a
     room at 100% and the same room at 125% are not the same measurement, and
     folding them together hides which one is failing. */
  const NOMINAL = ['1280x720', '1366x768', '1920x1080', '1024x768'];
  const GROUPS = { nominal: NOMINAL, scaled: SCALED };
  for (const [group, vps] of Object.entries(GROUPS)) {
    for (const fixture of ['as-authored', 'wrap', 'heading', 'bigfont']) {
      const set = measured.filter(m => m.fixture === fixture && vps.includes(m.viewport));
      const f = set.filter(m => m.clearance < 8);
      t(`whole stage on screen without scrolling · ${group} · ${fixture}`, f.length === 0,
        `${set.length - f.length}/${set.length} cells clear by >=8px, worst ${Math.min(...set.map(m => m.clearance))}px` +
        (f.length ? '; offenders: ' + f.slice(0, 8).map(m => `${m.lesson}/${m.stage}@${m.viewport}=${m.clearance}px`).join(' ') : ''));
    }
  }
  /* The claim that actually tests the fitting mechanism: when something DOES
     overflow, it must not be the picture. Every failing cell must have the
     picture already shrunk to its floor, which means the engine did everything
     it could and what is overflowing is the text above it. If a cell fails with
     the picture still at its intent cap, the fit is broken. */
  const failing = measured.filter(m => m.clearance < 8);
  const pictureAtFault = failing.filter(m => parseFloat(m.fit) > 96 + 1);
  t('when a slide overflows, the picture is never the offender',
    pictureAtFault.length === 0,
    `${failing.length} cells of ${measured.length} overflow; ${failing.length - pictureAtFault.length} of them ` +
    `have the picture already at its 96px floor` +
    (pictureAtFault.length ? '; picture still oversized in: ' +
      pictureAtFault.map(m => `${m.lesson}/${m.stage}@${m.viewport} fit=${m.fit}`).join(' ') : ''));

  /* the scaled cells reported on their own, because they are the named risk */
  for (const fixture of ['as-authored', 'wrap', 'heading', 'bigfont']) {
    const sc = measured.filter(m => m.fixture === fixture && SCALED.includes(m.viewport));
    const f = sc.filter(m => m.clearance < 8);
    console.log(`      scaled viewports · ${fixture.padEnd(12)} ${sc.length - f.length}/${sc.length} clear` +
      `, worst ${Math.min(...sc.map(m => m.clearance))}px` +
      (f.length ? ' — ' + f.map(m => `${m.lesson}/${m.stage}@${m.viewport}=${m.clearance}px`).join(' ') : ''));
  }
  const phone = measured.filter(m => m.viewport === '390x844');
  const phoneBad = phone.filter(m => m.clearance < 8);
  console.log(`      phone 390x844: ${phone.length - phoneBad.length}/${phone.length} clear; ` +
    `as-authored failures: ` + (phone.filter(m => m.fixture === 'as-authored' && m.clearance < 8)
      .map(m => `${m.lesson}/${m.stage}=${m.clearance}px`).join(' ') || 'none'));
  console.log(`      worst clearance anywhere (all fixtures, all viewports): ${worst.px}px  ` +
    `(${worst.where} @ ${worst.viewport}, fixture=${worst.fixture}, element=${worst.offender})`);
  console.log(`      cells measured: ${measured.length}  under 8px: ${failing.length}`);
  results.matrix = MATRIX;
  results.worst = worst;
}

/* ---------------------------------------------------------------- TEST 4b
   The heading-length guardrail.

   The projector + long-heading test is red on purpose: a heading long enough to
   wrap pushes a We Do 2 stage off the foot of the slide, and the picture is
   already at its floor so nothing in the layout can absorb it. That is a design
   limit, not a bug, and the floor is not moving to hide it.

   What can be prevented is authoring into it by accident. Bisecting the actual
   threshold (reports/convergence/headingthreshold.mjs) puts it at 57 characters
   on the tightest deck-and-viewport pair, W7 at 1024x768. This lints every slide
   heading in all ten Autumn 1 decks against that, with the margin stated, so the
   failing case cannot be written without the harness saying so. */
{
  const THRESHOLD = 57;                 /* measured, see headingthreshold.mjs */
  const DECKS = LESSONS.map(L).concat([
    'Science_Teesside/Grow/SCI_G_W3_Friction.html',
    'Science_Teesside/Grow/SCI_G_W4_Mechanisms.html',
    'Science_Teesside/Grow/SCI_G_W5_Fair_Test.html',
    'Science_Teesside/Grow/SCI_G_W6_Earth_And_Planets.html',
    'Science_Teesside/Grow/SCI_G_W7_The_Moon.html'
  ]);
  const over = [];
  let longest = { len: 0 };
  for (const rel of DECKS) {
    const { p, ctx } = await page(rel);
    const hs = await p.evaluate(() =>
      [...document.querySelectorAll('.slide')].map(s => {
        const h = s.querySelector('h2');
        return { title: s.getAttribute('data-title') || '?',
                 heading: h ? h.textContent.trim() : '',
                 hasStage: !!s.querySelector('.g-stage, .ba-stage') };
      }).filter(r => r.heading));
    await ctx.close();
    hs.forEach(r => {
      if (r.heading.length > longest.len) longest = { len: r.heading.length, deck: rel, ...r };
      if (r.heading.length >= THRESHOLD) over.push(`${rel.split('/').pop()} / ${r.title} (${r.heading.length})`);
    });
  }
  t('no slide heading reaches the overflow threshold',
    over.length === 0,
    `threshold ${THRESHOLD} chars; longest real heading ${longest.len} ` +
    `("${longest.heading}", ${longest.deck.split('/').pop()} / ${longest.title}) — ` +
    `margin ${THRESHOLD - longest.len} chars` + (over.length ? '; over: ' + over.join(', ') : ''));
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
