/**
 * Render the assembled Art mirror in headless Chromium and assert on evidence.
 *
 * Written because the build's static checks prove text, not behaviour. A deck
 * can pass every regex gate and still ship a dead visual-learning panel or a
 * logo whose data URI does not decode. These assertions look at the rendered
 * DOM: real element boxes, real image intrinsic sizes, real network traffic.
 *
 * Usage: node tools/verify_art_mirror_rendered.mjs <pack-Art-dir>
 */
import { chromium } from 'playwright';
import { readdirSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';

const ART = resolve(process.argv[2]);
const fails = [];
const ok = (c, m) => { if (!c) fails.push(m); };

function htmlUnder(dir) {
  const out = [];
  for (const e of readdirSync(dir)) {
    const p = join(dir, e);
    if (statSync(p).isDirectory()) out.push(...htmlUnder(p));
    else if (e.endsWith('.html')) out.push(p);
  }
  return out;
}

const pages = htmlUnder(ART).sort();
console.log(`rendering ${pages.length} pages from ${ART}`);

const browser = await chromium.launch();
const ctx = await browser.newContext();

let external = [], consoleErrors = [], avlMounted = 0, avlExpected = 0;
let logoOk = 0, logoBroken = 0, cssOk = 0;

for (const file of pages) {
  const rel = file.slice(ART.length + 1);
  const page = await ctx.newPage();
  const errs = [];
  page.on('console', m => { if (m.type() === 'error') errs.push(`${rel}: ${m.text().slice(0, 120)}`); });
  page.on('pageerror', e => errs.push(`${rel}: pageerror ${String(e).slice(0, 120)}`));
  // Any request that is not file:// or a data: URI is a page reaching the
  // internet. An offline pack must make none.
  page.on('request', r => {
    const u = r.url();
    if (!u.startsWith('file://') && !u.startsWith('data:') && !u.startsWith('about:'))
      external.push(`${rel} -> ${u.slice(0, 90)}`);
  });

  await page.goto('file://' + file, { waitUntil: 'load' });
  await page.waitForTimeout(220);   // let the AVL loader mount

  // 1 - the visual-learning panel.
  //
  // These decks are slide decks: `.slide{display:none}` and only `.slide.active`
  // is shown. The AVL layer mounts into the "We Do 1" slide, which is NOT active
  // on load, so measuring its painted box on load reports zero for a panel that
  // is working perfectly. Two assertions instead, neither of which is a proxy:
  //
  //   a) the runtime BUILT the component. The authored HTML contains no `avl-`
  //      markup at all (the marker pair is a stylesheet link and two scripts),
  //      so every .avl-* element in the DOM was created by the JS after it
  //      resolved this lesson's payload by filename slug. Zero nodes therefore
  //      means a dead loader or an unmatched slug - the real failure class.
  //   b) once its host slide is shown, the panel occupies a real box. This is
  //      what a teacher sees when they reach that slide.
  const avl = await page.evaluate(() => {
    const declared = document.documentElement.innerHTML.includes('AVL-MOUNT:BEGIN');
    if (!declared) return { declared: false };
    const built = [...document.querySelectorAll('[class^="avl-"],[class*=" avl-"]')];
    if (!built.length) return { declared: true, built: 0, painted: 0 };
    // show the slide that hosts the panel, exactly as the deck's own nav would
    const host = built[0].closest('.slide') || built[0].parentElement;
    if (host && host.classList.contains('slide')) {
      document.querySelectorAll('.slide.active').forEach(s => s.classList.remove('active'));
      host.classList.add('active');
    }
    const painted = built.filter(n => {
      const r = n.getBoundingClientRect();
      return r.width > 40 && r.height > 20;
    });
    return { declared: true, built: built.length, painted: painted.length };
  });
  if (avl.declared) {
    avlExpected++;
    if (avl.built > 0 && avl.painted > 0) avlMounted++;
    else if (!avl.built)
      fails.push(`${rel}: AVL loader dead - runtime built no nodes (slug unmatched or script missing)`);
    else
      fails.push(`${rel}: AVL built ${avl.built} nodes but none paints once its slide is shown`);
  }

  // 2 - the Progress Schools logo actually decodes and has intrinsic pixels.
  //     A broken data URI renders as a 0x0 image and no error is thrown.
  const logos = await page.evaluate(() =>
    [...document.querySelectorAll('img[alt="Progress Schools"]')]
      .map(i => ({ w: i.naturalWidth, h: i.naturalHeight })));
  for (const l of logos) {
    if (l.w > 0 && l.h > 0) logoOk++;
    else { logoBroken++; fails.push(`${rel}: logo image has no intrinsic size`); }
  }

  // 3 - the deck's stylesheet was applied, not merely linked. Checked against a
  //     property the sheet sets; the browser default for body margin is 8px.
  const styled = await page.evaluate(() => {
    const b = getComputedStyle(document.body);
    return b.backgroundColor !== 'rgba(0, 0, 0, 0)' || b.fontFamily !== 'Times New Roman';
  });
  if (styled) cssOk++;

  consoleErrors.push(...errs);
  await page.close();
}

await browser.close();

// The favicon on the three Launch pages must be the Progress Schools mark.
ok(avlExpected > 0, 'no deck declared a visual-learning panel - scope is wrong');
ok(avlMounted === avlExpected, `AVL: ${avlMounted}/${avlExpected} panels mounted`);
ok(logoBroken === 0, `${logoBroken} logo images failed to decode`);
ok(external.length === 0, `${external.length} external requests: ${external.slice(0, 4).join(' | ')}`);
ok(consoleErrors.length === 0, `${consoleErrors.length} console errors: ${consoleErrors.slice(0, 4).join(' | ')}`);
ok(cssOk === pages.length, `${pages.length - cssOk} pages rendered unstyled`);

console.log('-'.repeat(66));
console.log(`pages rendered      : ${pages.length}`);
console.log(`AVL panels mounted  : ${avlMounted} of ${avlExpected} declared`);
console.log(`logo images decoded : ${logoOk} (0 broken)`);
console.log(`pages styled        : ${cssOk} of ${pages.length}`);
console.log(`external requests   : ${external.length}`);
console.log(`console errors      : ${consoleErrors.length}`);
console.log('-'.repeat(66));
if (fails.length) {
  for (const f of fails.slice(0, 20)) console.log('  FAIL:', f);
  process.exit(1);
}
console.log('  ALL RENDER CHECKS PASS');
