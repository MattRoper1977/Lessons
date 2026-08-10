// Gate 11 — contact sheets, so a reviewer can commit without opening 35 files.
//
// Per lesson: one PNG showing the title slide, one interactive slide, and print
// page 1 as it prints with NO tier chosen (i.e. the A1 fix visible).
// Per pack: one combined sheet.
//
// Usage: node contact_sheet.mjs <outRoot> <pack> <file...>
import { chromium } from 'playwright';
import { pathToFileURL } from 'url';
import { resolve, basename } from 'path';
import { mkdirSync, writeFileSync, readFileSync } from 'fs';

const [outRoot, pack, ...files] = process.argv.slice(2);
const dir = `${outRoot}/${pack}`;
mkdirSync(dir, { recursive: true });

const browser = await chromium.launch();
const shots = [];

const panelPage = await browser.newPage({ viewportSize: { width: 1280, height: 300 } });

for (const f of files) {
  const page = await browser.newPage({ viewportSize: { width: 1280, height: 800 } });
  await page.goto(pathToFileURL(resolve(f)).href, { waitUntil: 'load' });
  await page.waitForTimeout(150);

  const b64 = [];
  // 1 · title slide
  b64.push((await page.screenshot()).toString('base64'));

  // 2 · an interactive slide — the We Do 2 / widget slide
  const idx = await page.evaluate(() => {
    const s = [...document.querySelectorAll('.slide')];
    let i = s.findIndex(x => x.querySelector('.widget,.soft-check,.microfilm,input,button[onclick]')
                             && x.dataset.type !== 'title');
    return i < 0 ? Math.min(5, s.length - 1) : i;
  });
  await page.evaluate(i => (window.show ? window.show(i) : null), idx);
  await page.waitForTimeout(120);
  b64.push((await page.screenshot()).toString('base64'));

  // 3 · print page 1 under the print default (no tier selected)
  await page.emulateMedia({ media: 'print' });
  await page.evaluate(() => {
    const pk = document.querySelector('.print-pack,.printpack');
    document.querySelectorAll('.slide-container,.deck,.controls,.prog,.progress-wrap')
      .forEach(x => x.style.display = 'none');
    pk.style.display = 'block';
    pk.style.background = '#fff';
    window.scrollTo(0, 0);
  });
  await page.waitForTimeout(120);
  b64.push((await page.screenshot({ fullPage: false })).toString('base64'));
  await page.close();

  const name = basename(f).replace('.html', '');
  const html = `<body style="margin:0;background:#0f172a;font:13px system-ui;color:#fff">
  <div style="padding:10px 14px;font-weight:800;font-size:17px">${pack.toUpperCase()} · ${name}</div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;padding:0 8px 10px">
   ${['title slide', 'interactive slide', 'print page 1 · no tier chosen (all three routes)']
      .map((cap, i) => `<figure style="margin:0"><img src="data:image/png;base64,${b64[i]}"
        style="width:100%;border:2px solid #334155;border-radius:6px;background:#fff">
        <figcaption style="padding:4px 2px;color:#cbd5e1">${cap}</figcaption></figure>`).join('')}
  </div></body>`;
  await panelPage.setContent(html);
  await panelPage.waitForTimeout(80);
  const out = `${dir}/${name}.png`;
  writeFileSync(out, await panelPage.screenshot({ fullPage: true }));
  shots.push({ name, out });
  console.log('  ' + out);
}

// combined sheet for the pack
const grid = shots.map(s => {
  const b = readFileSync(s.out).toString('base64');
  return `<figure style="margin:0"><img src="data:image/png;base64,${b}" style="width:100%">
   </figure>`;
}).join('');
const combined = `<body style="margin:0;background:#0f172a">
 <div style="padding:12px 16px;font:800 20px system-ui;color:#fff">
   ${pack.toUpperCase()} · v3 40-minute route · ${shots.length} lessons</div>
 <div style="display:grid;grid-template-columns:1fr;gap:6px;padding:0 8px 12px">${grid}</div></body>`;
await panelPage.setContent(combined);
await panelPage.waitForTimeout(120);
writeFileSync(`${outRoot}/${pack}-combined.png`,
              await panelPage.screenshot({ fullPage: true }));
console.log(`  ${outRoot}/${pack}-combined.png  (${shots.length} lessons)`);
await browser.close();
