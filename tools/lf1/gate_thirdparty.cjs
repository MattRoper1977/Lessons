// tools/lf1/gate_thirdparty.cjs - the amended sec 8a gate (D24), in a browser.
//
// Usage: PLAYWRIGHT_MODULE=<path> node tools/lf1/gate_thirdparty.cjs <file-list> <out.json>
// Exit 1 if any page shows a third-party URL in pupil-visible text.
//
// "zero third-party URLs in pupil-visible text. Cited third-party URLs are
//  permitted inside staff asides."
//
// A source scan cannot decide this: every deck carries its citations in a DATA
// payload, and the page renders them INTO <aside class="staff" hidden>. What
// matters is what a pupil can read, so this walks all 8 stages and all 3 task
// routes with the staff aside in its default state, and reads textContent only --
// never an href. A link whose visible text is "Open Scratch" shows no URL.
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('fs'), path = require('path');
const URLTXT = /https?:\/\/[^\s<>"')]+/gi;
const OWN = /^https?:\/\/(?:www\.)?(?:madebymatt\.uk|localhost|127\.0\.0\.1)/i;

(async () => {
  const files = fs.readFileSync(process.argv[2], 'utf8').split('\n').map(s=>s.trim()).filter(Boolean);
  const out = {};
  const browser = await chromium.launch();
  for (const f of files) {
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    const errs = [];
    page.on('pageerror', e => errs.push('page: ' + e.message));
    page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
    await page.goto('file://' + path.resolve(f));
    const seen = new Set(), staffSeen = new Set();
    for (const route of ['step', 'main', 'challenge']) {
      await page.evaluate(r => {
        const s = document.querySelector('#route');
        if (s) { s.value = r; s.dispatchEvent(new Event('change')); }
      }, route);
      for (let i = 0; i < 8; i++) {
        await page.evaluate(i => {
          const b = document.querySelector(`[data-section="${i}"]`);
          if (b) b.click();
        }, i);
        const t = await page.evaluate(() => {
          const staff = document.querySelector('aside.staff');
          const hidden = staff ? staff.hasAttribute('hidden') : true;
          const clone = document.body.cloneNode(true);
          // A DETACHED clone has no layout, so innerText degrades to textContent and
          // would swallow every <script> body -- including the DATA payload that holds
          // the citations. Strip the non-rendered elements explicitly, then read
          // textContent so that text inside a COLLAPSED <details> still counts: a pupil
          // can open a disclosure, which is not what "inside a staff aside" means.
          clone.querySelectorAll('script,style,template,aside.staff').forEach(n => n.remove());
          return {pupil: clone.textContent || '', staff: staff ? staff.textContent || '' : '', hidden};
        });
        (t.pupil.match(URLTXT) || []).forEach(u => { if (!OWN.test(u)) seen.add(u); });
        (t.staff.match(URLTXT) || []).forEach(u => { if (!OWN.test(u)) staffSeen.add(u); });
      }
    }
    out[path.basename(f)] = {pupilVisible: [...seen].sort(), inStaffAside: [...staffSeen].sort(), errors: errs};
    await ctx.close();
  }
  await browser.close();
  fs.writeFileSync(process.argv[3], JSON.stringify(out, null, 1));
  let bad = 0, errFiles = 0;
  for (const [k, v] of Object.entries(out)) {
    if (v.pupilVisible.length) { bad++; console.log(`  PUPIL-VISIBLE  ${k}`); v.pupilVisible.forEach(u => console.log(`      ${u}`)); }
    if (v.errors.length) { errFiles++; console.log(`  JS ERRORS      ${k}: ${v.errors.slice(0,2).join(' | ')}`); }
  }
  console.log(`\n${bad} of ${files.length} decks show a third-party URL in pupil-visible text`);
  console.log(`${errFiles} of ${files.length} decks logged a console/page error`);
  process.exit(bad ? 1 : 0);
})();
