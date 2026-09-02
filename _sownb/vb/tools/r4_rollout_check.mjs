// light R4 check for the rollout: cold text == standard text, and each route's print text identical to the unpatched copy
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'node:fs'; import path from 'node:path'; import crypto from 'node:crypto';
const files = fs.readFileSync(process.argv[2], 'utf8').trim().split('\n');
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const out = {};
async function txt(file, arm) { const page = await browser.newPage({ viewport: { width: 1365, height: 800 } }); await page.addInitScript(() => { window.print = () => {}; }); await page.goto('file://' + path.resolve(file)); await page.waitForTimeout(250); if (arm) await page.evaluate(`printPack('${arm}')`); await page.emulateMedia({ media: 'print' }); const t = await page.evaluate(() => Array.from(document.querySelectorAll('#print-area .print-section')).filter(e => getComputedStyle(e).display !== 'none').map(e => e.innerText).join('\n').replace(/\s+/g, ' ').trim()); await page.close(); return t; }
for (const f of files) {
  const before = path.join(path.dirname(f), '.r4b_' + path.basename(f)); const r = {};
  try {
    const after = { cold: await txt(f, null), supported: await txt(f, 'supported'), standard: await txt(f, 'standard'), stretch: await txt(f, 'stretch') };
    const bef = { supported: await txt(before, 'supported'), standard: await txt(before, 'standard'), stretch: await txt(before, 'stretch'), cold: await txt(before, null) };
    r.coldBefore = bef.cold.length; r.coldAfter = after.cold.length; r.standard = after.standard.length;
    r.coldEqualsStandard = after.cold === after.standard; r.routesIdentical = ['supported', 'standard', 'stretch'].every(t => bef[t] === after[t]);
    r.status = (r.coldAfter > 0 && r.coldEqualsStandard && r.routesIdentical) ? 'PASS' : 'RED';
  } catch (e) { r.status = 'ERR'; r.err = String(e).slice(0, 120); }
  out[f] = r; console.log(r.status, f, r.coldBefore, '->', r.coldAfter, r.coldEqualsStandard, r.routesIdentical);
}
await browser.close(); fs.writeFileSync(process.argv[3], JSON.stringify(out, null, 1));
