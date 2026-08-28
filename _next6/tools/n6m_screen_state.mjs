// ORDER N6-M §M3 — capture the SCREEN state of a set of surfaces.
//
// Used twice: once before the guidance patch, once after with the toggle ON.
// The two must agree, which is what "toggle on restores the pre-patch screen"
// means in a form that can be asserted rather than argued.
//
// The toggle's own control is excluded. It is a new affordance the page did not
// have before; including it would make the assertion impossible to pass by
// definition and would say nothing about whether the guidance came back.
// Everything else — every element's tag, class, text length and layout box — is
// compared.
//
// Keyed by FULL PATH, not basename: START_HERE.html, index.html and friends
// repeat across packs, and keying by name silently compared 148 of 159 surfaces
// while reporting itself complete.
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const [outFile, guideOnFlag, ...files] = process.argv.slice(2);
const guideOn = guideOnFlag === '--guide-on';

const b = await chromium.launch();
const c = await b.newContext({ viewport: { width: 1280, height: 900 } });
const out = {};
let n = 0;
for (const f of files) {
  const p = await c.newPage();
  try {
    await p.goto('file://' + path.resolve(f), { waitUntil: 'load', timeout: 45000 });
    if (guideOn) {
      await p.evaluate(() => document.documentElement.classList.add('mbm-guide-on'));
    }
    await p.waitForTimeout(120);
    out[path.resolve(f)] = await p.evaluate(() => {
      const rows = [];
      for (const e of document.body.querySelectorAll('*')) {
        if (e.hasAttribute('data-n6m-guide-control')) continue;
        if (e.id === 'n6m-guide-css' || e.id === 'n6m-guide-js') continue;
        const r = e.getBoundingClientRect();
        const cls = (typeof e.className === 'string') ? e.className : '';
        rows.push([e.tagName, cls, (e.textContent || '').trim().length,
                   Math.round(r.x), Math.round(r.y),
                   Math.round(r.width), Math.round(r.height)].join('|'));
      }
      return rows.join('\n');
    });
  } catch (e) { out[path.resolve(f)] = 'ERROR ' + String(e).split('\n')[0]; }
  await p.close();
  if (++n % 40 === 0) console.error('  captured ' + n + '/' + files.length);
}
await b.close();
fs.writeFileSync(outFile, JSON.stringify(out));
console.error('captured ' + n + ' surfaces -> ' + outFile);
