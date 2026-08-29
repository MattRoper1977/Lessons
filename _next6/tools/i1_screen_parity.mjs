#!/usr/bin/env node
/**
 * ORDER N6-I · I1 — screen-parity witness for a print-only change.
 *
 * A change confined to `@media print` cannot affect screen rendering. That is
 * true by construction, and this proves it rather than asserting it: every
 * element's computed display/visibility/position/colour/background/font-size/
 * box metrics AND the deck's full `innerText` are hashed before and after.
 * `orphans`, `widows` and `break-inside` are in the captured set precisely
 * because they are what the fix sets — if they leaked to screen, this catches it.
 *
 * Usage: node i1_screen_parity.mjs <paths.txt> <out.json>
 *        node i1_screen_parity.mjs --compare <before.json> <after.json>
 */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

if (process.argv[2] === '--compare') {
  const a = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
  const b = JSON.parse(fs.readFileSync(process.argv[4], 'utf8'));
  const keys = [...new Set([...Object.keys(a), ...Object.keys(b)])].sort();
  let same = 0; const diffs = [];
  for (const k of keys) {
    if (!a[k] || !b[k]) { diffs.push([k, 'missing on one side']); continue; }
    const d = [];
    if (a[k].styles !== b[k].styles) d.push('computed styles');
    if (a[k].text !== b[k].text) d.push('body text');
    if (a[k].n !== b[k].n) d.push(`element count ${a[k].n}->${b[k].n}`);
    if (d.length) diffs.push([k, d.join(', ')]); else same++;
  }
  console.log(`screen parity: ${same}/${keys.length} identical`);
  for (const [k, d] of diffs) console.log(`  DIFF ${k}: ${d}`);
  process.exit(diffs.length ? 1 : 0);
}

const files = fs.readFileSync(process.argv[2], 'utf8').split('\n').map(s => s.trim()).filter(Boolean);
const b = await chromium.launch();
const out = {};
for (const f of files) {
  const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await p.goto('file://' + path.resolve(f), { waitUntil: 'load' });
  await p.waitForTimeout(400);
  const snap = await p.evaluate(() => {
    // Only elements that can render. A <style>/<script>/<meta> in <head> paints
    // nothing, so counting it would report a diff for the fix's own style tag —
    // a false positive that says nothing about what a teacher sees on screen.
    const SKIP = new Set(['HEAD', 'STYLE', 'SCRIPT', 'LINK', 'META', 'TITLE', 'BASE']);
    const els = [...document.querySelectorAll('*')].filter((e) => !SKIP.has(e.tagName));
    const rows = [];
    for (const e of els) {
      const cs = getComputedStyle(e);
      const r = e.getBoundingClientRect();
      rows.push([e.tagName, e.className && String(e.className).slice(0, 60),
        cs.display, cs.visibility, cs.position, cs.color, cs.backgroundColor,
        cs.fontSize, cs.height, cs.width, cs.orphans, cs.widows, cs.breakInside,
        Math.round(r.width), Math.round(r.height)].join('|'));
    }
    return { styles: rows.join('\n'), text: document.body.innerText, n: els.length };
  });
  out[path.basename(f)] = {
    n: snap.n,
    styles: crypto.createHash('sha256').update(snap.styles).digest('hex'),
    text: crypto.createHash('sha256').update(snap.text).digest('hex'),
    textLen: snap.text.length,
  };
  await p.close();
}
await b.close();
fs.writeFileSync(process.argv[3], JSON.stringify(out, null, 1));
console.error(`snapped ${files.length} -> ${process.argv[3]}`);
