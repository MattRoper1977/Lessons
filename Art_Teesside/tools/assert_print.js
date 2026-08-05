#!/usr/bin/env node
/**
 * AT-INST-03 - Art Teesside print-overflow assertion.
 *
 * WHY. min-height: 277mm was proposed to stop sheets reflowing. It could not:
 * @media print already sets .a4{min-height:0;height:auto}, so no min-height
 * change reaches the printed page. What actually stops reflow is knowing, at
 * authoring time, that a sheet has grown past the page. That is a measurement,
 * not a stylesheet, so it is an instrument.
 *
 * MEASURES AT TRUE A4 CONTENT WIDTH - 718 x 1047px, being 210x297mm at 96dpi
 * less 10mm @page margins. Standing rule 10. A print measurement taken at screen
 * width is not a print measurement: at 1280px this same check reported zero
 * overflows on a pack that was printing 9 pages for 8 sheets.
 *
 * WHAT IT STRUCTURALLY CANNOT DETECT
 *  - Renderer disagreement. It measures in the Chromium build on this machine.
 *    A different font stack or a school print driver can differ by a few px,
 *    which is why sheets are expected to clear the limit with headroom rather
 *    than by 1px.
 *  - Content that is wrong rather than tall. A sheet can fit perfectly and say
 *    nothing useful.
 *  - Packs that render nothing. A pack whose render() throws reports 0 sheets
 *    and 0 overflows, which looks identical to a clean pass. Sheet COUNT is
 *    therefore asserted too, against EXPECT_SHEETS.
 *
 * Usage:  node Art_Teesside/tools/assert_print.js [--verbose]
 * Exit 0 = every sheet fits and counts match. Exit 1 = otherwise.
 */
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');

const ROOT = process.env.ART_PRINT_ROOT ? path.resolve(process.env.ART_PRINT_ROOT) : path.resolve(__dirname, '..');
const LIMIT_PX = 1047;                 // 297mm - 20mm margins, at 96dpi
const VIEW = { width: 718, height: 1047 };
const EXPECT_SHEETS = Number(process.env.ART_PRINT_EXPECT_SHEETS || 55); // 8 packs; also expected page total
const EXPECT_PAGES = Number(process.env.ART_PRINT_EXPECT_PAGES || 55);
const WARN_PX = 50;   // clearance below which a sheet is one edit from failing

function packs(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap(e => {
    const p = path.join(dir, e.name);
    return e.isDirectory() ? packs(p) : (/Pack.*\.html$/.test(e.name) ? [p] : []);
  });
}

(async () => {
  const verbose = process.argv.includes('--verbose');
  const files = packs(ROOT).sort();
  const legacyChromium = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
  const executablePath = process.env.ART_CHROMIUM_EXECUTABLE || (fs.existsSync(legacyChromium) ? legacyChromium : null);
  const b = await chromium.launch(executablePath ? { executablePath } : {});
  const pg = await b.newPage({ viewport: VIEW });
  let sheets = 0, pages = 0, over = [], warn = [];

  for (const f of files) {
    await pg.goto('file://' + f);
    await pg.evaluate(() => { const s = document.getElementById('wk'); if (s) s.value = 'all'; render(); });
    await pg.emulateMedia({ media: 'print' });
    await pg.waitForTimeout(200);
    const r = await pg.evaluate(limit => [...document.querySelectorAll('.a4')].map((s, i) => {
      const h = Math.round(s.getBoundingClientRect().height);
      const wk = s.querySelector('.wk');
      return { i: i + 1, h, over: h - limit, label: (wk ? wk.textContent : '').trim().slice(0, 20) };
    }), LIMIT_PX);
    const pdf = await pg.pdf({ format: 'A4', printBackground: true,
      margin: { top: '10mm', bottom: '10mm', left: '10mm', right: '10mm' } });
    const n = (pdf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;
    sheets += r.length; pages += n;
    for (const s of r) {
      if (s.over > 0) over.push({ file: path.basename(f), ...s });
      else if (LIMIT_PX - s.h < WARN_PX) warn.push({ file: path.basename(f), ...s });
    }
    if (verbose) console.log(`${path.basename(f).slice(0, 44).padEnd(46)} sheets=${String(r.length).padStart(2)} pages=${String(n).padStart(2)} tallest=${Math.max(...r.map(x => x.h))}px headroom=${LIMIT_PX - Math.max(...r.map(x => x.h))}px`);
  }
  await b.close();

  const ok = over.length === 0 && sheets === EXPECT_SHEETS && pages === EXPECT_PAGES;
  for (const w of warn) console.log(`   WARN  ${w.file} sheet ${w.i} "${w.label}"  ${w.h}px  clears by only ${LIMIT_PX - w.h}px`);
  console.log(`\nsheets ${sheets}/${EXPECT_SHEETS}   pages ${pages}/${EXPECT_PAGES}   overflowing ${over.length}   limit ${LIMIT_PX}px @ ${VIEW.width}x${VIEW.height}`);
  for (const s of over) console.log(`   OVER  ${s.file} sheet ${s.i} "${s.label}"  ${s.h}px  +${s.over}px`);
  console.log(ok ? `PRINT ASSERTION PASS - every sheet fits, one page per sheet${warn.length ? ` (${warn.length} within ${WARN_PX}px of the limit)` : ''}`
                 : 'PRINT ASSERTION FAILED - read above');
  process.exit(ok ? 0 : 1);
})();
