/* LSG-1C lab boot: real Chromium, zero console/page errors, the lab driven
   end to end (predict -> all three tests -> frozen list -> glitch repair),
   fixtures marker read, contrast probed by computed style at render. */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');
const DIR = '/home/user/Lessons/Science_Teesside/Launch/v3_40min';
(async () => {
  const files = process.argv.slice(2);
  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--disable-dev-shm-usage']
  });
  let bad = 0;
  for (const f of files) {
    const full = path.isAbsolute(f) ? f : path.join(DIR, f);
    const ctx = await b.newContext();
    const p = await ctx.newPage();
    const errs = [];
    p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
    p.on('pageerror', e => errs.push('pageerror: ' + e.message));
    p.on('requestfailed', r => { if (!/favicon|thenational\.academy/.test(r.url())) errs.push('reqfail: ' + r.url()); });
    await p.goto('file://' + full, { waitUntil: 'load' });
    await p.waitForTimeout(400);
    const probe = await p.evaluate(() => {
      const out = { did: [], fail: [], contrast: [], frozen: 0, fixtures: null, say: '', glitch: '' };
      try {
        const box = document.querySelector('.sclab');
        if (!box) { out.fail.push('no .sclab present'); return out; }
        out.fixtures = box.getAttribute('data-fixtures');
        const pr = box.querySelector('.sc-predict .sc-btn');
        pr.click(); out.did.push('predict');
        if (pr.getAttribute('aria-pressed') !== 'true') out.fail.push('aria-pressed not set');
        out.say = document.getElementById('sc-say').textContent;
        box.querySelectorAll('.sc-row:not(.sc-predict) .sc-btn[data-i]').forEach(t => t.click());
        out.did.push('test x3');
        out.frozen = box.querySelectorAll('#sc-list li').length;
        const fix = box.querySelector('.sc-btn[data-fix="1"]');
        fix.click(); out.did.push('repair');
        out.glitch = document.getElementById('sc-glitch-result').textContent;
        box.querySelectorAll('.sc-btn').forEach(el => {
          const cs = getComputedStyle(el);
          if (cs.color === cs.backgroundColor) out.contrast.push((el.textContent || '').trim().slice(0, 18));
          if (cs.color === 'rgb(255, 255, 255)' && /255, 255, 255|246, 243|236, 230/.test(cs.backgroundColor))
            out.contrast.push('white-on-light: ' + (el.textContent || '').trim().slice(0, 18));
        });
      } catch (e) { out.fail.push(String(e)); }
      return out;
    });
    await p.waitForTimeout(120);
    if (probe.fail.length) errs.push('probe: ' + probe.fail.join('; '));
    if (probe.contrast.length) errs.push('CONTRAST: ' + probe.contrast.join(', '));
    if (probe.frozen !== 3) errs.push('frozen list ' + probe.frozen + '/3');
    if (!/Prediction received/.test(probe.say)) errs.push('predict text missing');
    if (!/^Repaired\./.test(probe.glitch)) errs.push('repair text missing');
    if (probe.fixtures !== null && !/^(\d+)\/\1$/.test(probe.fixtures)) errs.push('fixtures ' + probe.fixtures);
    const nm = path.basename(full);
    if (errs.length) { bad++; console.log('FAIL  ' + nm); errs.slice(0, 6).forEach(e => console.log('        ' + e)); }
    else console.log('ok    ' + nm + '   [driven: ' + probe.did.join(',') + '; frozen 3/3; fixtures ' + (probe.fixtures || 'n/a') + ']');
    await ctx.close();
  }
  await b.close();
  console.log(bad ? ('\nLAB BOOT FAIL — ' + bad + ' of ' + files.length)
    : ('\nLAB BOOT PASS — ' + files.length + '/' + files.length + ' labs driven end to end, zero errors, contrast probed'));
  process.exit(bad ? 1 : 0);
})();
