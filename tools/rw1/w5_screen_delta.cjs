const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  for (const f of process.argv.slice(2)) {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 720 } });
    const p = await ctx.newPage();
    await p.goto('file://' + path.resolve(f), { waitUntil: 'load' });
    const r = await p.evaluate(() => {
      const secs = [...document.querySelectorAll('.print-section')];
      const visible = secs.filter(s => { const b = s.getBoundingClientRect();
        return getComputedStyle(s).display !== 'none' && b.width > 0 && b.height > 0; });
      const area = document.getElementById('print-area');
      const meta = [...document.querySelectorAll('.science-meta')];
      return { sections: secs.length, visibleOnScreen: visible.length,
               printAreaDisplay: area ? getComputedStyle(area).display : 'absent',
               metaTotal: meta.length,
               metaOnScreen: meta.filter(e => e.getBoundingClientRect().height > 0).length,
               elementTotal: document.querySelectorAll('*').length };
    });
    // GW1-B R1: every count carries what it was drawn from.
    console.log('%s  print sections %d · VISIBLE ON SCREEN %d of %d · #print-area display %s · science-meta on screen %d of %d · %d elements examined',
      path.basename(f).slice(0, 34), r.sections, r.visibleOnScreen, r.sections,
      r.printAreaDisplay, r.metaOnScreen, r.metaTotal, r.elementTotal);
    if (!r.sections || !r.metaTotal || !r.elementTotal)
      console.log('   [DENOMINATOR ZERO] sections %d · science-meta %d · elements %d -- nothing was examined',
        r.sections, r.metaTotal, r.elementTotal);
    await ctx.close();
  }
  await b.close();
})();
