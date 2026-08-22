#!/usr/bin/env node
// l2k_partb_gate.mjs — pass PEQ-L2K PART B tag gates on the six live LAUNCH PEQ
// decks, in headless Chromium at three viewports (390 / 768 / 1440):
//   1. the L2 route panel is display:none at load (default-hidden)
//   2. the (i) Guidance toggle reveals it; aria-pressed flips; localStorage
//      mbm_guide_v1 persists; a reload with the key set shows the panel
//   3. print emulation, toggle OFF: no #print-l2route in the visible print set
//      (the three standard packs stay free of the route mirror)
//   4. print emulation, toggle ON: printPack marks #print-l2route visible
//   5. zero page errors / console errors
// Run: node _passpq/tools/l2k_partb_gate.mjs
import { chromium } from 'playwright';
import { fileURLToPath, pathToFileURL } from 'url';
import path from 'path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const DECKS = [
  'PEQ_W1_Intro_and_Choosing_My_Level.html',
  'PEQ_W2_What_Makes_Communication_Effective.html',
  'PEQ_W3_Active_Listening_and_Giving_Feedback.html',
  'PEQ_W4_Plan_a_Communication_Activity.html',
  'PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html',
  'PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html',
];
const VIEWPORTS = [{ width: 390, height: 844 }, { width: 768, height: 1024 }, { width: 1440, height: 900 }];

const fails = [];
const browser = await chromium.launch();
for (const deck of DECKS) {
  const url = pathToFileURL(path.join(ROOT, 'LAUNCH_ASDAN', 'PEQ', deck)).href;
  for (const vp of VIEWPORTS) {
    const ctx = await browser.newContext({ viewport: vp });
    const page = await ctx.newPage();
    const errs = []; const missed = [];
    page.on('pageerror', e => errs.push(String(e)));
    page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    page.on('requestfailed', r => missed.push(r.url()));
    await page.goto(url, { waitUntil: 'load' });

    const hidden = await page.$eval('[data-l2route="1"]', el => getComputedStyle(el).display === 'none');
    if (!hidden) fails.push(`${deck} @${vp.width}: L2 panel visible at load`);

    await page.click('.mbm-guide-btn');
    const state = await page.evaluate(() => ({
      shown: getComputedStyle(document.querySelector('[data-l2route="1"]')).display !== 'none',
      pressed: document.querySelector('.mbm-guide-btn').getAttribute('aria-pressed'),
      stored: localStorage.getItem('mbm_guide_v1'),
    }));
    if (!state.shown) fails.push(`${deck} @${vp.width}: toggle did not reveal the L2 panel`);
    if (state.pressed !== 'true') fails.push(`${deck} @${vp.width}: aria-pressed not true`);
    if (state.stored !== '1') fails.push(`${deck} @${vp.width}: mbm_guide_v1 not persisted`);

    // print with toggle ON: the mirror joins the pack
    const onPack = await page.evaluate(() => {
      window.print = () => {};
      printPack('standard');
      return [...document.querySelectorAll('.print-section.visible')].map(el => el.id);
    });
    if (!onPack.includes('print-l2route')) fails.push(`${deck} @${vp.width}: toggle-on print pack lacks print-l2route`);

    // reload persists; then toggle OFF: default packs carry no route mirror
    await page.reload({ waitUntil: 'load' });
    const persisted = await page.$eval('[data-l2route="1"]', el => getComputedStyle(el).display !== 'none');
    if (!persisted) fails.push(`${deck} @${vp.width}: reveal did not survive reload`);
    await page.click('.mbm-guide-btn'); // back off
    const offState = await page.evaluate(() => {
      window.print = () => {};
      printPack('supported'); const sup = [...document.querySelectorAll('.print-section.visible')].map(el => el.id);
      printPack('standard'); const std = [...document.querySelectorAll('.print-section.visible')].map(el => el.id);
      printPack('stretch'); const str = [...document.querySelectorAll('.print-section.visible')].map(el => el.id);
      return { sup, std, str, stored: localStorage.getItem('mbm_guide_v1'),
               hidden: getComputedStyle(document.querySelector('[data-l2route="1"]')).display === 'none' };
    });
    for (const [k, pack] of Object.entries({ sup: offState.sup, std: offState.std, str: offState.str }))
      if (pack.includes('print-l2route')) fails.push(`${deck} @${vp.width}: default ${k} pack carries print-l2route`);
    if (offState.stored !== '0') fails.push(`${deck} @${vp.width}: toggle-off not persisted`);
    if (!offState.hidden) fails.push(`${deck} @${vp.width}: panel still visible after toggle off`);

    // /hud.js 404 is the documented known caveat (see _eca1/tools/boot.js);
    // "Failed to load resource" console lines are counted via the failed-request URLs
    const realMissed = missed.filter(u => !/\/hud\.js$/.test(u));
    if (realMissed.length) fails.push(`${deck} @${vp.width}: failed loads: ${realMissed.join(' | ').slice(0, 200)}`);
    const realErrs = errs.filter(e => !/hud\.js/.test(e) && !/Failed to load resource/.test(e));
    if (realErrs.length) fails.push(`${deck} @${vp.width}: page errors: ${realErrs.join(' | ').slice(0, 200)}`);
    await ctx.close();
  }
  console.log(`checked ${deck} at 390/768/1440`);
}
await browser.close();
if (fails.length) { console.log('\nPART B GATE FAIL:'); fails.forEach(f => console.log('  ' + f)); process.exit(1); }
console.log('\nPART B gate: 6 decks x 3 viewports — default-hidden · toggle · persistence · print packs · zero errors: ALL GREEN');
