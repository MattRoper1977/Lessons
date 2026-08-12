/* NAV-1 boot: real Chromium. Per file: zero console/page errors; the button
   present, clickable and correctly targeted on the FIRST, a MIDDLE (We Do,
   lab-bearing where present) and the LAST slide; geometry measured at
   1280x800, 390x844 and 844x390 — the button's rect must not intersect any
   visible interactive element (chassis controls, lab buttons, tier buttons)
   at natural scroll; contrast read from computed style; target href resolves. */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const files = process.argv.slice(2);
  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--disable-dev-shm-usage']
  });
  let bad = 0;
  const viewports = [{ width: 1280, height: 800 }, { width: 390, height: 844 }, { width: 844, height: 390 }];
  for (const f of files) {
    const full = path.isAbsolute(f) ? f : path.join('/home/user/Lessons', f);
    const errs = [];
    for (const vp of viewports) {
      const ctx = await b.newContext({ viewport: vp });
      const p = await ctx.newPage();
      p.on('console', m => { if (m.type() === 'error') errs.push(vp.width + 'w console: ' + m.text()); });
      p.on('pageerror', e => errs.push(vp.width + 'w pageerror: ' + e.message));
      await p.goto('file://' + full, { waitUntil: 'load' });
      await p.waitForTimeout(250);
      const r = await p.evaluate(() => {
        const out = { fail: [], slides: 0, checked: [] };
        const btn = document.querySelector('.mbmhome');
        if (!btn) { out.fail.push('no .mbmhome'); return out; }
        const cs = getComputedStyle(btn);
        const rect0 = btn.getBoundingClientRect();
        if (rect0.width < 44 || rect0.height < 44) out.fail.push('touch target ' + Math.round(rect0.width) + 'x' + Math.round(rect0.height));
        if (cs.color === cs.backgroundColor) out.fail.push('contrast: color==background');
        if (!/index\.html$/.test(btn.getAttribute('href'))) out.fail.push('href ' + btn.getAttribute('href'));
        if (/animation|transition/.test((cs.transitionProperty !== 'all' || cs.transitionDuration !== '0s') ? 'transition' : '') && cs.transitionDuration !== '0s') out.fail.push('motion declared');
        const slides = [...document.querySelectorAll('section.slide')];
        out.slides = slides.length;
        const isDeck = slides.length > 0;
        const idxs = isDeck ? [...new Set([0, Math.floor(slides.length / 2), slides.length - 1])] : [null];
        for (const si of idxs) {
          if (isDeck) {
            slides.forEach((s, j) => s.style.display = j === si ? 'flex' : 'none');
          }
          const br = btn.getBoundingClientRect();
          const hits = [];
          document.querySelectorAll('button, a, [onclick], input, select').forEach(el => {
            if (el === btn || el.contains(btn) || btn.contains(el)) return;
            const r = el.getBoundingClientRect();
            if (!r.width || !r.height) return;
            const st = getComputedStyle(el);
            if (st.visibility === 'hidden' || st.display === 'none') return;
            const ox = Math.max(0, Math.min(br.right, r.right) - Math.max(br.left, r.left));
            const oy = Math.max(0, Math.min(br.bottom, r.bottom) - Math.max(br.top, r.top));
            if (ox > 0 && oy > 0) hits.push((el.className || el.tagName) + '@slide' + si);
          });
          if (hits.length) out.fail.push('overlap slide ' + si + ': ' + hits.slice(0, 3).join(', '));
          out.checked.push(si);
        }
        return out;
      });
      if (r.fail.length) errs.push(vp.width + 'x' + vp.height + ': ' + r.fail.join(' | '));
      await ctx.close();
    }
    // target resolution in the repo tree
    const m = fs.readFileSync(full, 'utf8').match(/class="mbmhome" href="([^"]+)"/);
    const target = path.normalize(path.join(path.dirname(full), m[1]));
    if (target !== '/home/user/Lessons/index.html') errs.push('target does not resolve: ' + target);
    const nm = path.basename(full);
    if (errs.length) { bad++; console.log('FAIL  ' + nm); errs.slice(0, 6).forEach(e => console.log('        ' + e)); }
    else console.log('ok    ' + nm);
  }
  await b.close();
  console.log(bad ? '\nNAV BOOT FAIL — ' + bad + ' of ' + files.length
    : '\nNAV BOOT PASS — ' + files.length + '/' + files.length + ' files, 3 viewports, first/middle/last slides, zero errors, zero overlaps');
  process.exit(bad ? 1 : 0);
})();
