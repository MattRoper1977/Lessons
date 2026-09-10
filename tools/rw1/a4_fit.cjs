// RW1 §4.5 / GW1 §A5 · does each staff card fit ONE A4 side?
//
// Measured, not estimated: render under print emulation at A4 portrait, make the
// card's print section the visible one exactly as printSection() does, and read
// its scrollHeight against the printable area.
//
// A4 portrait is 210 x 297 mm. At 96 CSS px per inch that is 794 x 1123 px. The
// pack's print CSS sets #print-area padding, so the printable box is the page
// less the margins the print CSS actually applies -- read from the element, not
// assumed.
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const path = require('path');

const A4_H = 1123, A4_W = 794;

(async () => {
  const files = process.argv.slice(2).filter(a => !a.startsWith('--'));
  const browser = await chromium.launch();
  let bad = 0;
  for (const f of files) {
    const ctx = await browser.newContext({ viewport: { width: A4_W, height: A4_H } });
    const page = await ctx.newPage();
    await page.goto('file://' + path.resolve(f), { waitUntil: 'load' });
    await page.emulateMedia({ media: 'print' });
    const cards = await page.evaluate(() => [...document.querySelectorAll('.print-section')]
      .filter(s => /marking|first-back/.test(s.id)).map(s => s.id));
    for (const id of cards) {
      const r = await page.evaluate((sid) => {
        document.querySelectorAll('.print-section,.print-resource,.print-sheet')
          .forEach(s => s.classList.toggle('visible', s.id === sid));
        const el = document.getElementById(sid);
        const area = document.getElementById('print-area');
        const cs = area ? getComputedStyle(area) : null;
        const padY = cs ? parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom) : 0;
        return { h: el.scrollHeight, w: el.scrollWidth, padY,
                 tables: el.querySelectorAll('table').length,
                 avoid: [...el.querySelectorAll('*')].filter(e =>
                   /avoid/.test(getComputedStyle(e).breakInside + getComputedStyle(e).pageBreakInside)).length };
      }, id);
      const printable = A4_H - r.padY;
      const fits = r.h <= printable;
      if (!fits) bad++;
      console.log('%s %s height %dpx / printable %4dpx (A4 %d less %dpx padding)  %s',
        path.basename(f).slice(0, 32), id, r.h, printable, A4_H, r.padY,
        fits ? 'FITS' : 'OVERFLOWS by ' + (r.h - printable) + 'px');
      console.log('%s %s width %dpx / %dpx · tables %d · break-inside:avoid nodes %d',
        '', '', r.w, A4_W, r.tables, r.avoid);
    }
    await ctx.close();
  }
  await browser.close();
  process.exit(bad ? 1 : 0);
})();
