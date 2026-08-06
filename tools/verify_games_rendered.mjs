/* Band-1 rendered regression: overflow + accessible names at 390x844.
 * Run with OLD=1 against a pristine checkout to see it FAIL (negative control). */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const targets = ['Trail_Runner.html','Trekkers_Trail_Runner_Tees_Coast.html','Wrecking_Crew.html',
  'Globe_Snake (1).html','Grapple.html','Marble.html','Neon_Siege.html','Orbital.html','Prism.html',
  'Vortex.html','Neon_Snake_Overdrive.html','OneGuy.html'];
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true });
  let fail = 0;
  for (const t of targets) {
    const pg = await ctx.newPage();
    await pg.goto('http://127.0.0.1:4173/Lessons/Games/' + encodeURIComponent(t), { waitUntil: 'load', timeout: 20000 });
    await pg.waitForTimeout(1800);
    const r = await pg.evaluate(() => {
      const doc = document.documentElement;
      const unnamed = [...document.querySelectorAll('input,select,textarea,button,[role="button"]')]
        .filter(el => { const b = el.getBoundingClientRect(); return b.width > 0 && b.height > 0; })
        .filter(el => !((el.getAttribute('aria-label') || el.textContent || (el.labels && el.labels[0] && el.labels[0].textContent) || '').trim() || el.getAttribute('aria-labelledby')))
        .map(el => el.tagName.toLowerCase() + '#' + (el.id || '?'));
      return { over: doc.scrollWidth - doc.clientWidth, unnamed };
    });
    const ok = r.over <= 0 && r.unnamed.length === 0;
    if (!ok) fail++;
    console.log(`${ok ? 'PASS' : 'FAIL'} ${t} overflow=${r.over}px unnamed=${JSON.stringify(r.unnamed)}`);
    await pg.close();
  }
  await b.close();
  console.log(fail ? `${fail} FILE(S) FAILED` : 'ALL BAND-1 RENDERED CHECKS PASSED');
  process.exit(fail ? 1 : 0);
})();
