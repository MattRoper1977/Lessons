/* NAV-1 print gate: rendered print text (print media emulation, body
   innerText) must be IDENTICAL before and after the edit. Baseline = the
   file at the base ref (default origin/main), rendered the same way. */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');
(async () => {
  const base = process.env.NAV_BASE || 'origin/main';
  const files = process.argv.slice(2);
  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--disable-dev-shm-usage']
  });
  async function printText(fullPath) {
    const ctx = await b.newContext();
    const p = await ctx.newPage();
    await p.emulateMedia({ media: 'print' });
    await p.goto('file://' + fullPath, { waitUntil: 'load' });
    await p.waitForTimeout(200);
    const t = await p.evaluate(() => document.body.innerText);
    await ctx.close();
    return t;
  }
  let bad = 0;
  for (const f of files) {
    const full = path.isAbsolute(f) ? f : path.join('/home/user/Lessons', f);
    const rel = path.relative('/home/user/Lessons', full);
    const tmp = path.join(os.tmpdir(), 'navbase-' + path.basename(full));
    execSync(`git -C /home/user/Lessons show ${base}:'${rel}' > '${tmp}'`);
    const [before, after] = [await printText(tmp), await printText(full)];
    fs.unlinkSync(tmp);
    if (before === after) console.log('ok    print-identical  ' + path.basename(full));
    else {
      bad++;
      console.log('FAIL  print text differs ' + path.basename(full)
        + '  (before ' + before.length + ' chars, after ' + after.length + ')');
    }
  }
  await b.close();
  console.log(bad ? '\nPRINT GATE FAIL — ' + bad + ' of ' + files.length
    : '\nPRINT GATE PASS — ' + files.length + '/' + files.length + ' rendered print outputs identical to base');
  process.exit(bad ? 1 : 0);
})();
