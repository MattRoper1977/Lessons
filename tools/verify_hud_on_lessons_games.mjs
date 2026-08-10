/**
 * Every Lessons game carries the estate HUD, and the HUD works where it landed.
 *
 * hud.js is served from the site origin at an absolute path, and 248 files in
 * this repository already load it — Games/Glitch_Clash.html among them. Thirteen
 * games in the canonical search index did not, so a pupil in one of them had the
 * browser Back button and nothing else, and a teacher had no dock.
 *
 * Two forms land here, decided by hud.js from the path alone:
 *
 *   /Lessons/Games/*        IS_GAME  — the back circle, plus the chosen-homepage
 *                                      circle beside it when a homepage is stored
 *   /Lessons/<anything>/*   IS_LESSON — the same two controls in pill form AND the
 *                                      full teacher dock: timer, name picker,
 *                                      noise meter, calm reset
 *
 * The second is a bigger change than "a back button", and it is the established
 * behaviour for every other lesson page in this estate rather than anything new.
 *
 * What is asserted, by observing the page rather than reading the markup:
 *
 *   - the file carries the HUD script exactly once
 *   - the back control renders, and with a homepage chosen so does the home one
 *   - both are hit-testable ON TOP where a finger would land. These games paint
 *     their own splash and menu overlays, and a control underneath one is not a
 *     control
 *   - the two never overlap each other, nor the teacher pill on lesson pages
 *   - clicking home leaves the game for the chosen homepage
 *   - the page reports no errors with the HUD present
 *
 * Needs the estate served on one origin, because hud.js lives at /hud.js on the
 * site and these pages live under /Lessons/. That is how it is served in
 * production and how the cross-estate workflow assembles it.
 *
 * Usage:
 *   MBM_BASE_URL=http://127.0.0.1:4175/ node tools/verify_hud_on_lessons_games.mjs
 *   node tools/verify_hud_on_lessons_games.mjs --self-test
 */
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const HUD_TAG = /<script\b[^>]*\bsrc="\/hud\.js"[^>]*>/g;
const VIEWPORTS = [[320, 640, '320'], [768, 1024, '768'], [1440, 900, '1440']];
const KEY = 'mbm_audience_view';
// Not a route the back control would reach anyway, so a click that fell through
// to the page's own navigation cannot be mistaken for a pass.
const CHOICE = 'teachers';
const CHOICE_ROUTE = '/for/teachers/';
const MIN_CONTROL = 24;

// A real function, not a string. Playwright's Node API evaluates a string as an
// EXPRESSION and ignores the argument, so the string form silently returned
// undefined for every probe - green by never asserting anything. The Python
// binding accepts a function source string; this one does not.
const ON_TOP = (id) => {
  const e = document.getElementById(id);
  if (!e) return 'MISSING';
  const b = e.getBoundingClientRect();
  const t = document.elementFromPoint(b.x + b.width / 2, b.y + b.height / 2);
  if (!t) return 'NOTHING AT THAT POINT';
  if (t === e || e.contains(t)) return 'ON TOP';
  return 'COVERED by ' + t.tagName.toLowerCase() + (t.id ? '#' + t.id : '');
};

const BOXES = () => {
  const r = id => { const e = document.getElementById(id); if (!e) return null;
    const b = e.getBoundingClientRect();
    return {x: b.x, y: b.y, width: b.width, height: b.height}; };
  return {home: r('mbmhud-home'), back: r('mbmhud-back'), pill: r('mbmhud-pill')};
};

/** The canonical inventory, read from the site repo when it is beside us and
 *  from a committed copy otherwise. Never a list typed into this file. */
function lessonsGameRoutes() {
  const candidates = [
    process.env.MBM_SEARCH_INDEX,
    path.join(ROOT, '..', 'mattroper1977.github.io', 'data', 'mbm-search-index.json'),
    '/workspace/mattroper1977.github.io/data/mbm-search-index.json',
  ].filter(Boolean);
  for (const candidate of candidates) {
    if (!fs.existsSync(candidate)) continue;
    const index = JSON.parse(fs.readFileSync(candidate, 'utf8'));
    return [...new Set(index.entries
      .filter(e => e.category === 'game' && e.route.startsWith('/Lessons/'))
      .map(e => e.route))].sort();
  }
  throw new Error(
    'the canonical search index was not found. Set MBM_SEARCH_INDEX, or place the site repository ' +
    'beside this one. Guessing the inventory from the filesystem would answer a different question ' +
    'from the one this tool is asked.'
  );
}

/** Games declared unable to carry the HUD, and why.
 *  A declared input, not a silent gap: without it the coverage figure quietly
 *  means "the ones it worked on". Three games' own verifiers forbid an external
 *  script or extract their JavaScript by slicing to the file's last </script>. */
function excludedRoutes() {
  const file = path.join(ROOT, 'data', 'hud-coverage.json');
  const data = JSON.parse(fs.readFileSync(file, 'utf8'));
  return new Map(data.excluded.map(entry => [entry.route, entry]));
}

/** The one rule, in one place so a control runs the same code the gate does.
 *  Every inventory game is wired or declared, and nothing in between. */
function classify(route, hasTag, excluded) {
  if (excluded.has(route)) {
    return hasTag ? `${route} is declared unable to carry the HUD but carries the script` : null;
  }
  return hasTag ? null : `${route} carries no HUD script and is not declared in data/hud-coverage.json`;
}

function overlap(a, b) {
  if (!a || !b) return 0;
  const wide = Math.min(a.x + a.width, b.x + b.width) - Math.max(a.x, b.x);
  const high = Math.min(a.y + a.height, b.y + b.height) - Math.max(a.y, b.y);
  return Math.max(0, wide) * Math.max(0, high);
}

const results = [];
const check = (ok, label, detail = '') => {
  results.push({ ok, label, detail });
  if (!ok) console.log(`  FAIL  ${label}${detail ? ' — ' + detail : ''}`);
};

async function selfTest() {
  let failures = 0;
  const browser = await chromium.launch();
  const page = await (await browser.newContext({ viewport: { width: 390, height: 640 } })).newPage();

  await page.setContent(
    "<a id='mbmhud-back' style='position:fixed;left:8px;top:8px;width:44px;height:44px'>x</a>" +
    "<div style='position:fixed;inset:0;z-index:2147483647;background:#000'>splash</div>"
  );
  const buried = await page.evaluate(ON_TOP, 'mbmhud-back');
  if (buried.startsWith('COVERED')) console.log(`  [PASS] control detected: a splash buries the control (${buried})`);
  else { console.error(`  [FAIL] buried-control control did not fire: ${buried}`); failures += 1; }

  await page.setContent(
    "<div style='position:fixed;inset:0;background:#000'>splash</div>" +
    "<a id='mbmhud-back' style='position:fixed;left:8px;top:8px;width:44px;height:44px;z-index:2147483000'>x</a>"
  );
  const clear = await page.evaluate(ON_TOP, 'mbmhud-back');
  if (clear === 'ON TOP') console.log('  [PASS] negative control: a control above the overlay measures ON TOP');
  else { console.error(`  [FAIL] the hit test cannot report ON TOP: ${clear}`); failures += 1; }
  await browser.close();

  const excluded = excludedRoutes();
  const inventory = lessonsGameRoutes();
  const gaps = inventory.filter(route => {
    const file = path.join(ROOT, route.slice('/Lessons/'.length));
    const hasTag = fs.existsSync(file) && new RegExp(HUD_TAG.source).test(fs.readFileSync(file, 'utf8'));
    return classify(route, hasTag, excluded) !== null;
  });
  if (gaps.length) { console.error(`  [FAIL] ${gaps.length} inventory game(s) neither wired nor declared: ${gaps.slice(0, 4)}`); failures += 1; }
  else console.log(`  [PASS] all ${inventory.length} inventory games are wired (${inventory.length - excluded.size}) or declared (${excluded.size}), with nothing in between`);

  // The classification itself, against a game that is bare and undeclared.
  if (classify('/Lessons/Games/a-bare-undeclared-game.html', false, excluded) === null) {
    console.error('  [FAIL] a bare, undeclared game is classified as fine'); failures += 1;
  } else console.log('  [PASS] control: a bare, undeclared game is reported');
  const declared = [...excluded.keys()][0];
  if (classify(declared, false, excluded) !== null) {
    console.error('  [FAIL] a declared exclusion without the script is reported as a problem'); failures += 1;
  } else console.log('  [PASS] negative control: a declared exclusion without the script is not a problem');
  if (classify(declared, true, excluded) === null) {
    console.error('  [FAIL] a declared exclusion that gained the script is not reported'); failures += 1;
  } else console.log('  [PASS] control: a declared exclusion that gained the script is reported');
  const missing = [...excluded.values()].map(e => e.verifier).filter(v => !fs.existsSync(path.join(ROOT, v)));
  if (missing.length) { console.error(`  [FAIL] exclusions cite verifiers that do not exist: ${missing}`); failures += 1; }
  else console.log(`  [PASS] all ${excluded.size} exclusions cite a verifier that exists`);
  return failures;
}

async function run(base) {
  const origin = base.replace(/\/$/, '');
  const routes = lessonsGameRoutes().filter(r => true);

  const excluded = excludedRoutes();
  for (const route of routes) {
    const file = path.join(ROOT, route.slice('/Lessons/'.length));
    const tags = fs.existsSync(file) ? (fs.readFileSync(file, 'utf8').match(HUD_TAG) || []) : null;
    check(tags !== null, `${route}: the inventory names a file that exists`);
    if (tags === null) continue;
    const problem = classify(route, tags.length > 0, excluded);
    check(problem === null, `${route}: is wired or declared, not neither`, problem || '');
    if (excluded.has(route)) {
      const entry = excluded.get(route);
      check(fs.existsSync(path.join(ROOT, entry.verifier)),
        `${route}: the verifier its exclusion cites still exists`, entry.verifier);
      check(Array.isArray(entry.gates) && entry.gates.length > 0,
        `${route}: the exclusion names the gates that stopped it`);
    } else {
      check(tags.length === 1, `${route}: carries the HUD script exactly once`, `found ${tags.length}`);
    }
  }

  const measurable = routes.filter(route => !excluded.has(route));
  const browser = await chromium.launch();
  for (const [width, height, vp] of VIEWPORTS) {
    const context = await browser.newContext({ viewport: { width, height } });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(String(e).slice(0, 120)));

    for (const route of measurable) {
      errors.length = 0;
      const url = origin + route.split('/').map(encodeURIComponent).join('/');
      try {
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
        await page.evaluate(([k, v]) => localStorage.setItem(k, v), [KEY, CHOICE]);
        await page.reload({ waitUntil: 'domcontentloaded', timeout: 30000 });
        await page.waitForTimeout(900);
      } catch (e) {
        check(false, `${vp}${route}: loads with the HUD present`, String(e).slice(0, 110));
        continue;
      }

      for (const control of ['back', 'home']) {
        const id = `mbmhud-${control}`;
        check(await page.locator('#' + id).count() === 1, `${vp}${route}: the ${control} control renders`);
        const state = await page.evaluate(ON_TOP, id);
        check(state === 'ON TOP', `${vp}${route}: the ${control} control is hit-testable`, state);
      }

      const boxes = await page.evaluate(BOXES);
      check(overlap(boxes.home, boxes.back) === 0, `${vp}${route}: the two controls do not overlap`,
        `${overlap(boxes.home, boxes.back).toFixed(0)}px^2`);
      if (boxes.pill) {
        check(overlap(boxes.home, boxes.pill) === 0, `${vp}${route}: home does not overlap the TEACH pill`,
          `${overlap(boxes.home, boxes.pill).toFixed(0)}px^2`);
      }
      if (boxes.home) {
        check(boxes.home.width >= MIN_CONTROL && boxes.home.height >= MIN_CONTROL,
          `${vp}${route}: the home control has a real hit area`,
          `${boxes.home.width.toFixed(0)}x${boxes.home.height.toFixed(0)}`);
      }
      check(errors.length === 0, `${vp}${route}: no page errors with the HUD present`, errors.slice(0, 2).join(' | '));

      if (vp === '1440') {
        try {
          await page.click('#mbmhud-home', { timeout: 5000 });
          await page.waitForLoadState('domcontentloaded', { timeout: 15000 });
          const landed = page.url().slice(origin.length).split('?')[0];
          check(landed === CHOICE_ROUTE, `${route}: clicking home leaves the game for the chosen homepage`,
            `landed on ${landed}`);
        } catch (e) {
          check(false, `${route}: the home control can be clicked`, String(e).slice(0, 110));
        }
      }
    }
    await context.close();
  }
  await browser.close();
}

const wantsSelfTest = process.argv.includes('--self-test');
if (wantsSelfTest) {
  console.log('HUD-on-Lessons-games controls:');
  process.exit(await selfTest() ? 1 : 0);
}

const base = process.env.MBM_BASE_URL;
if (!base) {
  console.error('MBM_BASE_URL is required — the estate must be served on one origin, because hud.js');
  console.error('lives at /hud.js on the site and these pages live under /Lessons/.');
  process.exit(2);
}
await run(base);
const red = results.filter(r => !r.ok).length;
console.log(`\nHUD on Lessons games against ${base}: ${results.length - red} passed · ${red} failed`);
console.log(`  ${lessonsGameRoutes().length} game(s) x ${VIEWPORTS.length} viewport(s), from the canonical search index`);
process.exit(red ? 1 : 0);
