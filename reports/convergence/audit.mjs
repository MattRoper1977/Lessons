/* Convergence audit harness.
 *
 * Walks every slide of every lesson in a real browser and measures the things
 * the README says to check, plus the element census the evidence pack needs.
 * Run it once before the re-injection and once after; the two JSON files are
 * the before/after deltas.
 *
 *   NODE_PATH=/opt/node22/lib/node_modules node reports/convergence/audit.mjs \
 *     --label before --out reports/convergence/_data/before.json
 *   ... --label after --out reports/convergence/_data/after.json --shots reports/convergence
 *
 * The step audit re-implements the engine's byAttr() target resolution rather
 * than calling it, because byAttr is a closure inside the engine and is not
 * reachable from the page. The copy below is byAttr verbatim, widened to accept
 * either suite's cell class (.ba-cell / .g-cell), so a zero here means the same
 * thing a zero inside the engine would mean: the verb ran and moved nothing.
 */
import { createRequire } from 'module';
/* playwright is installed globally in this environment, and ESM does not read
   NODE_PATH — resolve it the way CommonJS would, with an override for a local
   install if one ever appears. */
const require_ = createRequire(import.meta.url);
const { chromium } = require_(process.env.PLAYWRIGHT_PATH || '/opt/node22/lib/node_modules/playwright');
import { mkdirSync, writeFileSync } from 'fs';
import { dirname, resolve, basename } from 'path';

const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf('--' + k); return i < 0 ? d : argv[i + 1]; };
const LABEL = arg('label', 'run');
const OUT = arg('out', `reports/convergence/_data/${LABEL}.json`);
const SHOTS = arg('shots', null);
const ROOT = process.cwd();

/* The BUILD five, which is what v1 and v2 measured and what the before/after
   comparison depends on. --lessons points the same harness at another set (the
   GROW five) without changing anything it measures; omitting it reproduces v1
   and v2 exactly. */
const LESSONS = (arg('lessons', null) || [
  'Science_Teesside/Build/SCI_B_W3_Backbones.html',
  'Science_Teesside/Build/SCI_B_W4_Muscle_Pairs.html',
  'Science_Teesside/Build/SCI_B_W5_Right_Nutrition.html',
  'Science_Teesside/Build/SCI_B_W6_Balanced_Plate.html',
  'Science_Teesside/Build/SCI_B_W7_Where_Food_Comes_From.html'
].join(',')).split(',').filter(Boolean);

/* Verbs classified by what their targets name. Anything not listed takes no
   part/label target, so a "no match" for it would be meaningless. */
const PART_VERBS = ['draw', 'pop', 'glow', 'unglow', 'hi', 'unhi', 'pulse', 'unpulse',
  'fade', 'dim', 'only', 'morph', 'flow', 'unflow', 'jiggle', 'heat', 'shake', 'bounce',
  'trace', 'untrace', 'zoom', 'show', 'hide', 'spot'];
const LABEL_VERBS = ['label', 'unlabel'];

const IN_PAGE = `(function () {
  var PART_VERBS = ${JSON.stringify(PART_VERBS)};
  var LABEL_VERBS = ${JSON.stringify(LABEL_VERBS)};

  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }

  /* byAttr, verbatim from the engine, widened to either suite's cell class. */
  function byAttr(stage, attr, nm) {
    var h = nm.indexOf('#'), sel;
    if (h > 0) {
      var i = parseInt(nm.slice(h + 1), 10), base = nm.slice(0, h);
      sel = '.g-cell:nth-of-type(' + i + ') [' + attr + '="' + base + '"],' +
            '.g-dual > figure:nth-of-type(' + i + ') [' + attr + '="' + base + '"],' +
            '.ba-cell:nth-of-type(' + i + ') [' + attr + '="' + base + '"]';
    } else {
      sel = '[' + attr + '="' + nm + '"]';
    }
    return $$(sel, stage);
  }

  var stages = $$('.g-stage, .ba-stage');
  var steps = [], zero = [], byName = {};

  function audit(stage, where) {
    var st = stage._g || stage._ba;
    if (!st) { zero.push({ where: where, verb: '(stage)', target: '(never built)', n: 0 }); return; }
    (st.steps || []).forEach(function (s, si) {
      (s.acts || []).forEach(function (a) {
        var kind = PART_VERBS.indexOf(a.verb) >= 0 ? 'data-part'
                 : LABEL_VERBS.indexOf(a.verb) >= 0 ? 'data-label' : null;
        if (!kind) return;
        var ts = (a.targets && a.targets.length) ? a.targets : ['*'];
        ts.forEach(function (t) {
          var n = t === '*' ? $$('[' + kind + ']', stage).length
                            : byAttr(stage, kind, t.split('>')[0].trim()).length;
          var rec = { where: where, step: si + 1, verb: a.verb, target: t, kind: kind, n: n };
          steps.push(rec);
          var key = kind + '|' + t;
          byName[key] = (byName[key] || 0) + n;
          if (n === 0) zero.push(rec);
        });
      });
    });
  }

  stages.forEach(function (stage, i) {
    var slide = stage.closest('.slide');
    var where = (slide ? (slide.getAttribute('data-title') || 'slide') : 'no-slide') +
                ' / ' + (stage.id || ('stage' + (i + 1)));
    audit(stage, where);
  });

  /* Prediction cards only build when a card is tapped, so their scripts would
     never be audited otherwise. Tap every card, then audit the stage it made. */
  $$('.g-predict, .ba-predict').forEach(function (panel, pi) {
    var slide = panel.closest('.slide');
    var base = (slide ? (slide.getAttribute('data-title') || 'slide') : 'no-slide') +
               ' / predict' + (pi + 1);
    var cards = $$('.g-pc, .ba-pc', panel);
    cards.forEach(function (c, ci) {
      c.click();
      $$('.g-stage, .ba-stage', panel).forEach(function (s) {
        audit(s, base + ' / card' + (ci + 1) + ' ' + (c.textContent || '').trim().slice(0, 28));
      });
    });
  });

  return {
    stageCount: stages.length,
    predictCount: $$('.g-predict, .ba-predict').length,
    stepChecks: steps.length,
    zero: zero,
    byName: byName,
    steps: steps
  };
})()`;

const CENSUS = `(function () {
  function $$(s) { return Array.prototype.slice.call(document.querySelectorAll(s)); }
  var ids = $$('[id]').map(function (e) { return e.id; });
  return {
    slides: $$('.slide').length,
    slideTitles: $$('.slide').map(function (s) { return s.getAttribute('data-title') || ''; }),
    ids: ids.length,
    idsDuplicated: ids.filter(function (v, i) { return ids.indexOf(v) !== i; }),
    scripts: $$('script').length,
    styles: $$('style').length,
    svgs: $$('svg').length,
    svgParts: $$('svg [data-part]').length,
    svgLabels: $$('svg [data-label]').length,
    printSections: $$('.print-section').length,
    matchPills: $$('.match-pill').length,
    /* The lesson's own glue counts .ba-pc to award XP for the prediction
       cards. The compat shim translates markup that is IN the file at load;
       cards the engine BUILDS afterwards are born .g-pc and never carry the
       old class, so this is where a one-way translation shows up. */
    baPredictCards: $$('.ba-pc').length,
    growPredictCards: $$('.g-pc').length,
    baStages: $$('.ba-stage').length,
    growStages: $$('.g-stage').length,
    xpTotal: (document.getElementById('xpTotal') || {}).textContent || null,
    engines: {
      BuildAnim: typeof window.BuildAnim,
      GrowAnim: typeof window.GrowAnim,
      BioSVG: typeof window.BioSVG,
      GrowSVG: typeof window.GrowSVG,
      GrowPolish: typeof window.GrowPolish
    },
    assets: (function () {
      try { return (window.BioSVG.list() || []).length; } catch (e) { return -1; }
    })()
  };
})()`;

const PRINTPACK = `(function () {
  var out = {};
  var realPrint = window.print;
  window.print = function () {};
  ['supported', 'standard', 'stretch'].forEach(function (lvl) {
    try { window.printPack(lvl); } catch (e) { out[lvl] = { error: String(e) }; return; }
    var vis = Array.prototype.slice.call(document.querySelectorAll('.print-section.visible'));
    out[lvl] = {
      visible: vis.length,
      empty: vis.filter(function (e) { return (e.textContent || '').trim().length < 12; })
                .map(function (e) { return e.id; }),
      chars: vis.reduce(function (a, e) { return a + (e.textContent || '').trim().length; }, 0),
      bodyClass: document.body.className
    };
  });
  window.print = realPrint;
  ['print-supported', 'print-standard', 'print-stretch'].forEach(function (c) {
    document.body.classList.remove(c);
  });
  document.querySelectorAll('.print-section').forEach(function (e) { e.classList.remove('visible'); });
  return out;
})()`;

/* prefers-reduced-motion: content must still be REVEALED, just not animated.
   Measured on the hardest case in the deck — a stage reset to step 0, where
   everything a script draws is hidden until a click. */
const REDUCED = `(function () {
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  var out = { stages: 0, hiddenParts: 0, invisibleLabels: 0, animatedParts: 0, checked: 0 };
  $$('.slide').forEach(function (sl) { sl.classList.add('active'); });
  $$('.g-stage, .ba-stage').forEach(function (stage) {
    out.stages++;
    try { (window.BuildAnim || window.GrowAnim).all(stage); } catch (e) {}
    $$('[data-part]', stage).forEach(function (p) {
      out.checked++;
      var cs = getComputedStyle(p);
      if (cs.visibility === 'hidden' || cs.opacity === '0' || cs.display === 'none') out.hiddenParts++;
      if (cs.animationName && cs.animationName !== 'none' && cs.animationDuration !== '0s') out.animatedParts++;
    });
    $$('[data-label]', stage).forEach(function (l) {
      var cs = getComputedStyle(l);
      if (cs.visibility === 'hidden' || cs.opacity === '0') out.invisibleLabels++;
    });
  });
  return out;
})()`;

async function run() {
  const browser = await chromium.launch();
  const report = { label: LABEL, lessons: {} };

  for (const rel of LESSONS) {
    const name = basename(rel, '.html');
    const url = 'file://' + resolve(ROOT, rel);
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 720 } });
    const page = await ctx.newPage();
    const errors = [], failed = [];
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 240)); });
    page.on('pageerror', e => errors.push('PAGEERROR ' + String(e).slice(0, 240)));
    page.on('requestfailed', r => failed.push(r.url().slice(0, 200) + ' :: ' + (r.failure()?.errorText || '')));

    await page.goto(url, { waitUntil: 'load' });
    await page.waitForTimeout(900);

    const census = await page.evaluate(CENSUS);
    const audit = await page.evaluate(IN_PAGE);
    const printpack = await page.evaluate(PRINTPACK);

    /* Screenshots: one per slide, every stage on it driven to its last step so
       the picture shows what the class would see at the end of the sequence. */
    const shots = [];
    if (SHOTS) {
      const dir = resolve(ROOT, SHOTS, name);
      mkdirSync(dir, { recursive: true });
      for (let i = 0; i < census.slides; i++) {
        await page.evaluate(n => {
          const s = document.querySelectorAll('.slide');
          s.forEach((el, j) => el.classList.toggle('active', j === n));
          if (typeof window.currentSlide === 'number') window.currentSlide = n;
          try { window.updateProgress && window.updateProgress(); } catch (e) {}
          s[n].querySelectorAll('.g-stage, .ba-stage').forEach(st => {
            try { (window.BuildAnim || window.GrowAnim).all(st); } catch (e) {}
          });
        }, i);
        await page.waitForTimeout(650);
        const f = `${dir}/slide-${String(i + 1).padStart(2, '0')}.png`;
        await page.screenshot({ path: f });
        shots.push(f.replace(ROOT + '/', ''));
      }
    }
    await ctx.close();

    /* Reduced motion runs in its own context so the emulation is real. */
    const rctx = await browser.newContext({ viewport: { width: 1280, height: 720 }, reducedMotion: 'reduce' });
    const rpage = await rctx.newPage();
    const rerr = [];
    rpage.on('pageerror', e => rerr.push(String(e).slice(0, 200)));
    await rpage.goto(url, { waitUntil: 'load' });
    await rpage.waitForTimeout(900);
    const reduced = await rpage.evaluate(REDUCED);
    reduced.errors = rerr;
    await rctx.close();

    report.lessons[name] = { path: rel, census, audit, printpack, reduced, errors, failed, shots };
    console.log(`${LABEL} · ${name}: slides=${census.slides} stages=${audit.stageCount} ` +
      `stepChecks=${audit.stepChecks} zero=${audit.zero.length} svg=${census.svgs} ` +
      `parts=${census.svgParts} errors=${errors.length} 404s=${failed.length}`);
    if (audit.zero.length) {
      audit.zero.slice(0, 12).forEach(z =>
        console.log(`    ZERO  ${z.where}  step ${z.step}  ${z.verb} ${z.target}`));
    }
  }

  await browser.close();
  mkdirSync(dirname(resolve(ROOT, OUT)), { recursive: true });
  writeFileSync(resolve(ROOT, OUT), JSON.stringify(report, null, 1));
  console.log('wrote ' + OUT);
}

run().catch(e => { console.error(e); process.exit(1); });
