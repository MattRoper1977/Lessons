// Tier-print proof (R4 triple) + phone/desktop screenshots. Usage: node tiers.mjs <deck> <outprefix> [beforeDeck]
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'node:fs'; import path from 'node:path';
const [deck, out, before] = process.argv.slice(2);
const abs = p => 'file://' + path.resolve(p);
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const rec = { file: deck, subject: 'R4 tier-print proof: cold print (no button) vs each tier button, rendered to PDF by Chromium; screen at 390 and 1365 before/after', tiers: {} };
async function pdfOf(fn, name) {
  const page = await browser.newPage({ viewport: { width: 1365, height: 800 } });
  await page.addInitScript(() => { window.print = () => { window.__printed = (window.__printed || 0) + 1; }; });
  await page.goto(abs(deck)); await page.waitForTimeout(300);
  if (fn) await page.evaluate(fn);
  await page.emulateMedia({ media: 'print' });
  const text = await page.evaluate(() => Array.from(document.querySelectorAll('#print-area .print-section.visible, .print-pack, .printpack')).map(e => e.innerText).join('\n'));
  const file = `${out}_${name}.pdf`; await page.pdf({ path: file, format: 'A4', printBackground: true });
  const bodyClass = await page.evaluate(() => document.body.className);
  await page.close();
  return { file, chars: text.replace(/\s+/g, ' ').trim().length, bytes: fs.statSync(file).size, bodyClass, text };
}
const cold = await pdfOf(null, 'cold'); rec.cold = { chars: cold.chars, bytes: cold.bytes, bodyClass: cold.bodyClass };
for (const t of ['supported', 'standard', 'stretch']) {
  const r = await pdfOf(`printPack('${t}')`, t); rec.tiers[t] = { chars: r.chars, bytes: r.bytes, bodyClass: r.bodyClass };
  if (t === 'standard') rec.coldEqualsStandardText = (r.text === cold.text);
}
// screen unchanged: screenshots + a DOM fingerprint of the visible slide at both widths
async function shot(file, w, tag) {
  const page = await browser.newPage({ viewport: { width: w, height: w < 500 ? 844 : 768 } });
  await page.goto(abs(file)); await page.waitForTimeout(400);
  const fp = await page.evaluate(() => { const s = document.querySelector('.slide.active, main.deck .slide.active, .slide'); const r = s ? s.getBoundingClientRect() : null; return { vis: !!s, w: r && Math.round(r.width), h: r && Math.round(r.height), printAreaHidden: (() => { const p = document.getElementById('print-area'); return !p || getComputedStyle(p).display === 'none'; })(), text: (s ? s.innerText : '').replace(/\s+/g, ' ').slice(0, 120) } });
  await page.screenshot({ path: `${out}_${tag}_${w}.png`, fullPage: false }); await page.close(); return fp;
}
rec.screen = { after390: await shot(deck, 390, 'after'), after1365: await shot(deck, 1365, 'after') };
if (before) rec.screen.before390 = await shot(before, 390, 'before'), rec.screen.before1365 = await shot(before, 1365, 'before');
await browser.close();
const ok = rec.cold.chars > 0 && rec.cold.chars >= rec.tiers.standard.chars && rec.coldEqualsStandardText && rec.screen.after390.printAreaHidden && rec.screen.after1365.printAreaHidden && ['supported', 'standard', 'stretch'].every(t => rec.tiers[t].chars > 500);
rec.status = ok ? 'PASS' : 'RED';
fs.writeFileSync(`${out}_tiers.json`, JSON.stringify(rec, null, 1));
console.log(rec.status, 'cold', rec.cold.chars, 'sup', rec.tiers.supported.chars, 'std', rec.tiers.standard.chars, 'str', rec.tiers.stretch.chars, 'cold==std', rec.coldEqualsStandardText, 'printHidden', rec.screen.after390.printAreaHidden, rec.screen.after1365.printAreaHidden);
