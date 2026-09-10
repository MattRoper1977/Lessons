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
      return { sections: secs.length, visibleOnScreen: visible.length,
               printAreaDisplay: area ? getComputedStyle(area).display : 'absent',
               metaOnScreen: [...document.querySelectorAll('.science-meta')]
                 .filter(e => e.getBoundingClientRect().height > 0).length };
    });
    console.log('%s  print sections %d · VISIBLE ON SCREEN %d · #print-area display %s · science-meta boxes on screen %d',
      path.basename(f).slice(0, 34), r.sections, r.visibleOnScreen, r.printAreaDisplay, r.metaOnScreen);
    await ctx.close();
  }
  await b.close();
})();
