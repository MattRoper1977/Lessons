// R4 proof triple for one deck, before (a copy) vs after (the patched file):
// 1 cold print >= default print (chars/ink/blocks); 2 each route's print TEXT identical before/after; 3 screen unchanged at 390/1365.
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'node:fs'; import path from 'node:path'; import crypto from 'node:crypto';
const [before, after, out] = process.argv.slice(2);
const abs = p => 'file://' + path.resolve(p);
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
async function measure(file, arm) {
  const page = await browser.newPage({ viewport: { width: 1365, height: 800 } });
  await page.addInitScript(() => { window.print = () => { window.__printed = (window.__printed || 0) + 1; }; });
  await page.goto(abs(file)); await page.waitForTimeout(300);
  if (arm) await page.evaluate(`printPack('${arm}')`);
  await page.emulateMedia({ media: 'print' });
  const r = await page.evaluate(() => {
    const vis = e => { const cs = getComputedStyle(e); return cs.display !== 'none' && cs.visibility !== 'hidden'; };
    const secs = Array.from(document.querySelectorAll('#print-area .print-section')).filter(vis);
    const text = secs.map(e => e.innerText).join('\n').replace(/\s+/g, ' ').trim();
    return { text, blocks: secs.length, bodyClass: document.body.className };
  });
  const pdf = `${out}_${path.basename(file, '.html').slice(0, 30)}_${arm || 'cold'}.pdf`;
  await page.pdf({ path: pdf, format: 'A4', printBackground: true });
  await page.close();
  return { chars: r.text.length, blocks: r.blocks, ink: fs.statSync(pdf).size, sha: crypto.createHash('sha256').update(r.text).digest('hex').slice(0, 16), bodyClass: r.bodyClass };
}
async function screen(file, w) {
  const page = await browser.newPage({ viewport: { width: w, height: w < 500 ? 844 : 768 } });
  await page.emulateMedia({ reducedMotion: 'reduce' }); await page.goto(abs(file)); await page.waitForTimeout(600);
  const fp = await page.evaluate(() => { const els = Array.from(document.querySelectorAll('body *')).filter(e => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden' && r.top < innerHeight; }); return { visibleCount: els.length, sig: els.slice(0, 400).map(e => e.tagName + (e.id ? '#' + e.id : '') + '.' + (typeof e.className === 'string' ? e.className.split(' ').slice(0, 2).join('.') : '')).join(','), pos: els.slice(0, 400).map(e => [Math.round(e.getBoundingClientRect().top), Math.round(e.getBoundingClientRect().left)]), printAreaHidden: (() => { const p = document.getElementById('print-area'); return !p || getComputedStyle(p).display === 'none'; })() }; });
  await page.screenshot({ path: `${out}_${path.basename(file, '.html').slice(0, 30)}_${w}.png` }); await page.close();
  return { visibleCount: fp.visibleCount, sigSha: crypto.createHash('sha256').update(fp.sig).digest('hex').slice(0, 16), pos: fp.pos, printAreaHidden: fp.printAreaHidden };
}
const rec = { file: after, subject: 'R4 proof triple: cold >= default print; each route print text identical before/after; screen unchanged at 390 and 1365', before: {}, after: {}, screen: {} };
for (const arm of [null, 'supported', 'standard', 'stretch']) { rec.before[arm || 'cold'] = await measure(before, arm); rec.after[arm || 'cold'] = await measure(after, arm); }
for (const w of [390, 1365]) rec.screen[w] = { before: await screen(before, w), after: await screen(after, w) };
await browser.close();
const c1 = rec.after.cold.chars >= rec.after.standard.chars && rec.after.cold.ink >= rec.after.standard.ink * 0.98 && rec.after.cold.blocks >= rec.after.standard.blocks && rec.after.cold.chars > 0;
const c2 = ['supported', 'standard', 'stretch'].every(t => rec.before[t].sha === rec.after[t].sha);
const maxShift = w => Math.max(0, ...rec.screen[w].before.pos.map((p, i) => rec.screen[w].after.pos[i] ? Math.max(Math.abs(p[0] - rec.screen[w].after.pos[i][0]), Math.abs(p[1] - rec.screen[w].after.pos[i][1])) : 999));
for (const w of [390, 1365]) { rec.screen[w].maxShiftPx = maxShift(w); delete rec.screen[w].before.pos; delete rec.screen[w].after.pos; }
const c3 = [390, 1365].every(w => rec.screen[w].before.sigSha === rec.screen[w].after.sigSha && rec.screen[w].before.visibleCount === rec.screen[w].after.visibleCount && rec.screen[w].maxShiftPx <= 3 && rec.screen[w].after.printAreaHidden);
rec.clauses = { coldGeDefault: c1, routeTextIdentical: c2, screenUnchanged: c3 }; rec.coldBefore = rec.before.cold.chars;
rec.status = (c1 && c2 && c3) ? 'PASS' : 'RED';
fs.writeFileSync(`${out}_r4.json`, JSON.stringify(rec, null, 1));
console.log(rec.status, 'cold before', rec.before.cold.chars, '-> after', rec.after.cold.chars, '| std', rec.after.standard.chars, '| c1', c1, 'c2', c2, 'c3', c3);
