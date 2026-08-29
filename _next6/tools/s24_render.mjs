#!/usr/bin/env node
/**
 * ORDER N6-I · I1/I2 — s24-print-renders, render half.
 *
 * Produces a REAL print output for every named surface: Chromium, print media
 * emulation, A4, `page.pdf()`. No element-presence check happens here and none
 * should — this half only makes the artefact. `s24_print_renders.py` measures it.
 *
 * Why per-route variants. BUILD_ASDAN's 24 decks gate their printable pack on
 * `body[data-print-route=...]`: with the attribute unset, all three
 * `.print-route` blocks are `display:none`. The real pathway is the deck's own
 * `printSelectedRoute()`, which reads `#printRoute` and calls `window.print()`.
 * So we stub `window.print`, call the deck's OWN function once per selectable
 * option, and render each resulting state. A surface with no such control is
 * rendered once, bare. Anything less renders a state no teacher ever prints.
 *
 * --a11y renders the same set under the estate's accessibility invariants —
 * prefers-reduced-motion: reduce, dark scheme, and the deck's own Calm Mode and
 * High Contrast classes applied. Those modes are authoritative on this estate, so
 * a print gate that only measures the default appearance is half a gate: a theme
 * or contrast rule that reflows the printable pack would be invisible to it.
 *
 * Usage: node s24_render.mjs --out <dir> <file.html> [file.html ...]
 *        node s24_render.mjs --out <dir> --list <paths.txt>
 *        node s24_render.mjs --out <dir> --a11y --list <paths.txt>
 */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const argv = process.argv.slice(2);
let out = null, listFile = null, settle = 400, a11y = false;
const files = [];
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === '--out') out = argv[++i];
  else if (argv[i] === '--list') listFile = argv[++i];
  else if (argv[i] === '--settle') settle = Number(argv[++i]);
  else if (argv[i] === '--a11y') a11y = true;
  else files.push(argv[i]);
}
if (listFile) {
  for (const l of fs.readFileSync(listFile, 'utf8').split('\n')) {
    const t = l.trim(); if (t && !t.startsWith('#')) files.push(t);
  }
}
if (!out || !files.length) {
  console.error('usage: s24_render.mjs --out <dir> <file.html>...');
  process.exit(2);
}
fs.mkdirSync(out, { recursive: true });

const slug = (p) => p.replace(/^\.\//, '').replace(/[^A-Za-z0-9._-]/g, '_');

const browser = await chromium.launch();
const index = [];
let n = 0;
for (const f of files) {
  const abs = path.resolve(f);
  const page = await browser.newPage(a11y
    ? { viewport: { width: 1280, height: 900 }, reducedMotion: 'reduce', colorScheme: 'dark' }
    : { viewport: { width: 1280, height: 900 } });
  const consoleErrors = [];
  page.on('pageerror', (e) => consoleErrors.push(String(e && e.message || e)));
  try {
    await page.goto('file://' + abs, { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(settle);
    if (a11y) {
      // The deck's own switches, not a simulation of them.
      await page.evaluate(() => {
        document.body.classList.add('calm', 'hc');
        document.documentElement.classList.add('hc');
      });
      await page.waitForTimeout(80);
    }
    // Print media for anything the page's own JS asks about it.
    await page.emulateMedia({ media: 'print' });

    // What does the DOCUMENT ITSELF say it will print? Counted in print media,
    // with checkVisibility() so a unit hidden by an ancestor is not counted.
    //
    // This is the honest source for "page count within a sane band". A band
    // hard-coded per pack rots the moment a pack is renamed or moved, and it
    // rotted during this very order's red-proof: a perturbed copy sitting at a
    // different path fell through to a permissive default and let a deck that
    // collapsed from ten printed pages to two pass as green. A count the file
    // declares about itself cannot fall through.
    const declared = await page.evaluate(() => {
      const vis = (e) => (e.checkVisibility ? e.checkVisibility() : true);
      const pack = document.querySelector('.print-pack');
      const printPages = pack
        ? [...pack.querySelectorAll('.print-page')].filter(vis).length : 0;
      const slides = [...document.querySelectorAll('.slide')].filter(vis).length;
      const lc = [...document.querySelectorAll('.n6-lc, .n6-lc-page')].filter(vis).length;
      return {
        printPages, slides, lcBlocks: lc,
        // The units the print stylesheet promises to put on their own sheets.
        units: printPages > 0 ? printPages : slides,
        unitKind: printPages > 0 ? 'print-page' : (slides > 0 ? 'slide' : 'none'),
        printTextLen: (document.body.innerText || '').replace(/\s+/g, '').length,
      };
    });

    // Does this surface carry the estate's route-gated print control?
    const routes = await page.evaluate(() => {
      const sel = document.getElementById('printRoute');
      if (!sel || typeof window.printSelectedRoute !== 'function') return null;
      return Array.from(sel.options).map((o) => ({
        value: o.value, selected: o.defaultSelected || o.selected,
      }));
    });

    const variants = routes
      ? routes.map((r) => ({ id: 'route-' + r.value, route: r.value, deflt: r.selected }))
      : [{ id: 'bare', route: null, deflt: true }];

    for (const v of variants) {
      if (v.route !== null) {
        // Drive the deck's OWN print path, with window.print neutralised so the
        // headless run does not block. This sets body[data-print-route].
        await page.evaluate((val) => {
          window.print = () => {};
          document.getElementById('printRoute').value = val;
          window.printSelectedRoute();
        }, v.route);
        await page.waitForTimeout(60);
      }
      const name = slug(f) + '__' + v.id + '.pdf';
      const buf = await page.pdf({
        path: path.join(out, name),
        format: 'A4',
        printBackground: true,
        margin: { top: '0', right: '0', bottom: '0', left: '0' },
      });
      // Re-read the declared units per variant: a route toggle changes which
      // print pages are visible, so the promise changes with it.
      const perVariant = await page.evaluate(() => {
        const vis = (e) => (e.checkVisibility ? e.checkVisibility() : true);
        const pack = document.querySelector('.print-pack');
        const printPages = pack
          ? [...pack.querySelectorAll('.print-page')].filter(vis).length : 0;
        const slides = [...document.querySelectorAll('.slide')].filter(vis).length;
        return { printPages, slides, units: printPages > 0 ? printPages : slides };
      });
      index.push({
        file: f, variant: (a11y ? 'a11y-' : '') + v.id, route: v.route,
        isDefault: !!v.deflt, a11y,
        declared: { ...declared, ...perVariant },
        pdf: name, bytes: buf.length,
        sha256: crypto.createHash('sha256').update(buf).digest('hex'),
        pageErrors: consoleErrors.slice(),
      });
    }
  } catch (e) {
    index.push({ file: f, variant: 'ERROR', route: null, isDefault: true,
                 pdf: null, error: String(e && e.message || e) });
  } finally {
    await page.close();
  }
  if (++n % 10 === 0) console.error(`  rendered ${n}/${files.length}`);
}
await browser.close();
fs.writeFileSync(path.join(out, 'index.json'), JSON.stringify(index, null, 1));
console.error(`rendered ${index.length} PDFs from ${files.length} surfaces -> ${out}`);
