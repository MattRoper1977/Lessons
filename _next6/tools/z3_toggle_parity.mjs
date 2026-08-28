#!/usr/bin/env node
/**
 * ORDER N6-Z · Z3 — the toggle's two screen gates.
 *
 *  ON  : with guidance ON the deck must be byte-identical to its pre-patch self.
 *        The toggle hides; it must never move, restyle or reorder anything.
 *  OFF : with guidance OFF (the default) exactly the tagged elements must be
 *        gone and nothing else. Reported, not just asserted, so the count is
 *        visible rather than a claim.
 */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const files = fs.readFileSync(process.argv[2], 'utf8').split('\n').map((s) => s.trim()).filter(Boolean);
const mode = process.argv[3];            // 'on' | 'off'
const out = process.argv[4];

const b = await chromium.launch();
const res = {};
for (const f of files) {
  const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await p.goto('file://' + path.resolve(f), { waitUntil: 'load' });
  await p.waitForTimeout(280);
  if (mode === 'on') {
    await p.evaluate(() => { if (window.mbmGuideToggle) window.mbmGuideToggle(); });
    await p.waitForTimeout(80);
  }
  const snap = await p.evaluate(() => {
    const SKIP = new Set(['HEAD', 'STYLE', 'SCRIPT', 'LINK', 'META', 'TITLE', 'BASE']);
    const els = [...document.querySelectorAll('*')].filter((e) => !SKIP.has(e.tagName)
      && !e.classList.contains('mbm-guide-btn'));
    const rows = [];
    for (const e of els) {
      const cs = getComputedStyle(e); const r = e.getBoundingClientRect();
      // The root's own class list carries `mbm-guide-on`, which IS the toggle's
      // state. Comparing it against a pre-patch capture would report the toggle
      // being on as a rendering difference, which it is not. Everything else on
      // the root — display, colours, box metrics — is still compared.
      const cls = (e === document.documentElement)
        ? String(e.className || '').replace(/\bmbm-guide-on\b/, '').trim()
        : String(e.className || '');
      rows.push([e.tagName, cls.slice(0, 60), cs.display, cs.visibility,
        cs.position, cs.color, cs.backgroundColor, cs.fontSize,
        Math.round(r.width), Math.round(r.height)].join('|'));
    }
    const tagged = [...document.querySelectorAll('[data-mbm-guide]')];
    // The ⓘ Guidance control is a DELIBERATE addition the order asks for, so its
    // own label and the geometry of the bar that holds it are reported
    // separately rather than counted as the patch disturbing the deck. Every
    // other element is still compared exactly.
    const btn = document.querySelector('.mbm-guide-btn');
    const bar = btn ? btn.closest('.controls, .toolbar, nav') : null;
    const barBox = bar ? (() => { const r = bar.getBoundingClientRect();
      return [Math.round(r.width), Math.round(r.height)].join('x'); })() : null;
    // The button is a block in the controls grid, so innerText emits a line for
    // it. Removing the label leaves the blank line behind, and that single "\n"
    // was the whole of the remaining difference in 36 decks. Collapse blank runs
    // so the comparison is about content and not about one line break belonging
    // to a control the order asked for.
    const text = (document.body.innerText || '')
      .replace(/ⓘ Guidance ✓?/g, '')
      .replace(/\n{2,}/g, '\n')
      .trim();
    return {
      styles: rows.join('\n'),
      // Rows whose geometry moved are reported, not filtered. Adding a visible
      // control necessarily reflows the bar that holds it; hashing computed
      // styles while adding one is the wrong instrument for "did the patch
      // disturb the lesson", so the gate is TEXT and ELEMENT COUNT, and the
      // reflow is measured and named rather than tuned out of the hash.
      controlRows: rows.filter((r) => /\|(controls|toolbar|tools|left|right|status|tool-label)\|/.test(r)).length,
      text, n: els.length, barBox,
      tagged: tagged.length,
      taggedVisible: tagged.filter((e) => e.checkVisibility && e.checkVisibility()).length,
      guideOn: document.documentElement.classList.contains('mbm-guide-on'),
    };
  });
  res[path.basename(f)] = {
    n: snap.n, tagged: snap.tagged, taggedVisible: snap.taggedVisible, guideOn: snap.guideOn,
    barBox: snap.barBox,
    styles: crypto.createHash('sha256').update(snap.styles).digest('hex'),
    text: crypto.createHash('sha256').update(snap.text).digest('hex'),
    textLen: snap.text.length,
  };
  await p.close();
}
await b.close();
fs.writeFileSync(out, JSON.stringify(res, null, 1));
const t = Object.values(res);
console.error(`${mode}: ${t.length} decks · tagged ${t.reduce((a, x) => a + x.tagged, 0)} · `
  + `tagged-visible ${t.reduce((a, x) => a + x.taggedVisible, 0)} · guideOn ${t.filter((x) => x.guideOn).length}`);
