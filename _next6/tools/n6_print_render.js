#!/usr/bin/env node
/* N6 · s24-print-renders — stage 1: render each surface through real Chromium
 * print pagination to A4 PDF.
 *
 * Why a PDF and not an element check: the two defects this gate exists for are
 * both invisible to the DOM. A learner-confirmation block sitting outside
 * `.print-pack` is present in the document and absent from the paper; a slide
 * left at `height:91%` is present, styled, and prints as a blank sheet. Only
 * the paginated output distinguishes those from a working surface.
 *
 * Usage: node n6_print_render.js <outdir> <file.html> [file.html ...]
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const [outdir, ...files] = process.argv.slice(2);
  if (!outdir || !files.length) { console.error('usage: n6_print_render.js <outdir> <files...>'); process.exit(2); }
  fs.mkdirSync(outdir, { recursive: true });

  const browser = await chromium.launch({ args: ['--font-render-hinting=none'] });
  const ctx = await browser.newContext();
  const manifest = [];
  let n = 0;

  for (const f of files) {
    const abs = path.resolve(f);
    const key = abs.replace(/[/\\]/g, '__').replace(/^_+/, '');
    const pdf = path.join(outdir, key + '.pdf');
    const page = await ctx.newPage();
    // Offline packs: nothing external may be fetched. Fail loudly if one tries.
    const external = [];
    page.on('request', r => { if (!/^(file|data|about|blob):/.test(r.url())) external.push(r.url()); });
    let err = null;
    try {
      await page.goto('file://' + abs, { waitUntil: 'load', timeout: 45000 });
      await page.emulateMedia({ media: 'print' });
      // let any deck bootstrap settle under print media
      await page.waitForTimeout(250);
      await page.pdf({ path: pdf, format: 'A4', printBackground: true,
                       margin: { top: '0mm', bottom: '0mm', left: '0mm', right: '0mm' } });
    } catch (e) { err = String(e).split('\n')[0]; }
    await page.close();
    manifest.push({ src: abs, pdf, error: err, external });
    if (++n % 10 === 0) console.error('  rendered ' + n + '/' + files.length);
  }
  await browser.close();
  fs.writeFileSync(path.join(outdir, 'render_manifest.json'), JSON.stringify(manifest, null, 1));
  console.error('rendered ' + n + ' surfaces -> ' + outdir);
})();
