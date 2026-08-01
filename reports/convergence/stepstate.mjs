/* Step-by-step state comparison — the teaching path, not the Show-all path.
 *
 * For every stage in every lesson, press Next once per step and record what the
 * class would actually see: which parts carry which motion, which labels are
 * up, what narration the bar prints. Motion classes are normalised across the
 * two engines so the two runs are comparable at all — build-anim kept the
 * class names from the original brief (glow-path, highlight-region, fade-rest,
 * pulse-answer, reveal-label), grow-anim renamed them (g-glow, g-hi, g-fade,
 * g-pulse, g-labelled). Anything not in the map is reported verbatim, so an
 * unmapped class shows up as a difference rather than being silently dropped.
 *
 *   node reports/convergence/stepstate.mjs --out FILE
 */
import { createRequire } from 'module';
const require_ = createRequire(import.meta.url);
const { chromium } = require_(process.env.PLAYWRIGHT_PATH || '/opt/node22/lib/node_modules/playwright');
import { mkdirSync, writeFileSync } from 'fs';
import { dirname, resolve, basename } from 'path';

const argv = process.argv.slice(2);
const OUT = argv[argv.indexOf('--out') + 1];
const ROOT = process.cwd();
const LESSONS = [
  'Science_Teesside/Build/SCI_B_W3_Backbones.html',
  'Science_Teesside/Build/SCI_B_W4_Muscle_Pairs.html',
  'Science_Teesside/Build/SCI_B_W5_Right_Nutrition.html',
  'Science_Teesside/Build/SCI_B_W6_Balanced_Plate.html',
  'Science_Teesside/Build/SCI_B_W7_Where_Food_Comes_From.html'
];

const WALK = `(function () {
  var MAP = {
    'glow-path': 'GLOW', 'g-glow': 'GLOW',
    'highlight-region': 'HI', 'g-hi': 'HI',
    'fade-rest': 'FADE', 'g-fade': 'FADE',
    'pulse-answer': 'PULSE', 'g-pulse': 'PULSE',
    'reveal-label': 'LABELLED', 'g-labelled': 'LABELLED',
    'ba-fadein': 'IN', 'g-in': 'IN',
    'ba-drew': 'DRAWN', 'g-draw': 'DRAWN',
    'ba-hidden': 'HIDDEN', 'g-hidden': 'HIDDEN',
    'ba-bounce': 'BOUNCE', 'g-bounce': 'BOUNCE',
    'ba-shake': 'SHAKE', 'g-shake': 'SHAKE',
    'trace-line': 'TRACE', 'g-trace': 'TRACE',
    'ba-label': '', 'g-label': ''
  };
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function marks(el) {
    var cls = (el.getAttribute('class') || '').split(/\\s+/).filter(Boolean);
    var out = [];
    cls.forEach(function (c) {
      var m = MAP.hasOwnProperty(c) ? MAP[c] : ('?' + c);
      if (m) out.push(m);
    });
    return out.sort().join('+');
  }
  function snapshot(stage) {
    var st = {};
    $$('[data-part]', stage).forEach(function (e) {
      var m = marks(e);
      if (m) st['part:' + e.getAttribute('data-part')] = m;
    });
    $$('[data-label]', stage).forEach(function (e) {
      var m = marks(e);
      if (m) st['label:' + e.getAttribute('data-label')] = m;
    });
    var say = stage.querySelector('.g-say, .ba-say');
    st['_say'] = say ? (say.textContent || '').trim() : null;
    st['_pose'] = stage.getAttribute('data-pose') || null;
    st['_verdict'] = $$('.g-verdict, .ba-verdict', stage).map(function (e) { return e.textContent; }).join('');
    st['_spot'] = $$('.g-spot, .focus-circle', stage).length;
    st['_think'] = $$('.g-think, .think-delay', stage).length;
    st['_followers'] = $$('.g-shown, .ba-shown', stage.closest('.slide') || document).length;
    return st;
  }
  var API = window.BuildAnim || window.GrowAnim;
  var out = {};
  $$('.slide').forEach(function (s) { s.classList.add('active'); });
  $$('.g-stage, .ba-stage').forEach(function (stage, i) {
    var slide = stage.closest('.slide');
    var key = (slide ? (slide.getAttribute('data-title') || 'slide') : '-') + ' / ' + (stage.id || ('stage' + i));
    var st = stage._g || stage._ba;
    if (!st) { out[key] = ['NOT BUILT']; return; }
    API.reset(stage);
    var seq = [JSON.stringify(snapshot(stage))];
    for (var n = 0; n < st.steps.length; n++) {
      API.next(stage);
      if ((stage._g || stage._ba).paused) { (stage._g || stage._ba).paused = false; }
      seq.push(JSON.stringify(snapshot(stage)));
    }
    out[key] = seq;
  });
  return out;
})()`;

const b = await chromium.launch();
const report = {};
for (const rel of LESSONS) {
  const ctx = await b.newContext({ viewport: { width: 1280, height: 720 } });
  const p = await ctx.newPage();
  await p.goto('file://' + resolve(ROOT, rel), { waitUntil: 'load' });
  await p.waitForTimeout(900);
  report[basename(rel, '.html')] = await p.evaluate(WALK);
  await ctx.close();
}
await b.close();
mkdirSync(dirname(resolve(ROOT, OUT)), { recursive: true });
writeFileSync(resolve(ROOT, OUT), JSON.stringify(report, null, 1));
console.log('wrote ' + OUT);
