#!/usr/bin/env node
/**
 * ORDER N6-Z · Z3 — choose WHICH elements get data-mbm-guide, in a real DOM.
 *
 * Selection is done in the browser and application is done in the source, because
 * three of the tests that matter cannot be done on the source text:
 *
 *  1. IS IT VISIBLE AT ALL? Half the candidates in GROW_ASDAN sit inside the TA
 *     briefing overlay, which is already hidden and which this order says to
 *     leave alone. Tagging them is churn at best; at worst it puts a second
 *     hiding mechanism on top of the estate's TA layer.
 *  2. IS IT INSIDE A LUNDY ZONE BOX? The zone strip stays visible. A source-side
 *     proximity window cannot answer this — a first attempt using a 2500-character
 *     window blocked 100% of candidates in three packs, because these decks carry
 *     `.lundy` containers throughout. `closest()` answers it exactly.
 *  3. WHO IS THE TEXT TALKING TO? Needs rendered textContent, not markup.
 *
 * Emits {file: [openTagIndex, ...]} where openTagIndex counts occurrences of that
 * element's tag+class signature in source order, so the Python side can apply the
 * attribute to exactly the right occurrence without re-deriving the judgement.
 */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const RULES = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const files = fs.readFileSync(process.argv[3], 'utf8').split('\n').map((s) => s.trim()).filter(Boolean);
const OUT = process.argv[4];

const browser = await chromium.launch();
const selection = {};
let n = 0;
for (const f of files) {
  const rule = RULES[Object.keys(RULES).find((k) => f.startsWith(k))];
  if (!rule) continue;
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  try {
    await page.goto('file://' + path.resolve(f), { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(220);
    const picked = await page.evaluate((R) => {
      const STAFF = new RegExp(R.staff);
      const NOTG = new RegExp(R.notGuidance);
      const out = [];
      // Walk every slide so an element on slide 4 is not judged invisible.
      const slides = [...document.querySelectorAll('.slide')];
      const visibleSomewhere = new Set();
      const mark = () => {
        for (const e of document.querySelectorAll('*')) {
          if (e.checkVisibility && e.checkVisibility()) visibleSomewhere.add(e);
        }
      };
      if (slides.length > 1) {
        const prev = slides.map((s) => s.className);
        for (const s of slides) {
          slides.forEach((x) => x.classList.remove('active'));
          s.classList.add('active'); s.removeAttribute('hidden');
          mark();
        }
        slides.forEach((s, i) => { s.className = prev[i]; });
      }
      mark();

      const sig = (e) => e.tagName.toLowerCase() + '|' + (e.getAttribute('class') || '');
      const counters = {};
      const indexOf = (e) => {
        const k = sig(e);
        const all = [...document.querySelectorAll('*')].filter((x) => sig(x) === k);
        return all.indexOf(e);
      };

      for (const spec of R.rules) {
        for (const e of document.querySelectorAll(spec.sel)) {
          const t = (e.textContent || '').replace(/\s+/g, ' ').trim();
          if (!t) continue;
          if (!visibleSomewhere.has(e)) continue;             // (1)
          if (e.closest('.lundy, .lundy-grid, .lundy-strip, .lundy-note')) continue;  // (2)
          if (NOTG.test(t)) continue;
          if (spec.label) {
            const b = e.querySelector('strong, b');
            const lab = b ? b.textContent.trim() : '';
            if (!spec.label.some((L) => lab.startsWith(L.replace(/:$/, '')))) continue;
          } else if (spec.startsWith) {
            if (!spec.startsWith.some((L) => t.startsWith(L))) continue;
          } else if (!STAFF.test(t)) continue;                 // (3)
          out.push({ sig: sig(e), idx: indexOf(e), role: spec.role,
                     text: t.slice(0, 90), sel: spec.sel });
        }
      }
      return out;
    }, rule);
    if (picked.length) selection[f] = picked;
  } catch (e) {
    selection[f] = { error: String(e && e.message || e) };
  }
  await page.close();
  if (++n % 25 === 0) console.error(`  ${n}/${files.length}`);
}
await browser.close();
fs.writeFileSync(OUT, JSON.stringify(selection, null, 1));
const tot = Object.values(selection).reduce((a, v) => a + (Array.isArray(v) ? v.length : 0), 0);
console.error(`selected ${tot} elements across ${Object.keys(selection).length} files`);
