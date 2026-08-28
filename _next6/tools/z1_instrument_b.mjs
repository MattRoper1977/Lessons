#!/usr/bin/env node
/**
 * ORDER N6-Z · Z1 — INSTRUMENT B: each lesson's claimed week and strand, and its
 * own LO/SC, read from the RENDERED DECK.
 *
 * Deliberately never opens the manifest or parses the filename. Instrument A does
 * that; the point of the pair is that they are derived from different places and
 * can therefore disagree. A reader that consulted both would make the comparison
 * meaningless, and an INSTRUMENT-SPLIT row impossible to produce.
 *
 * Every slide is activated in turn before reading, because these decks hide
 * non-active slides with `.slide{display:none}` and the week/term furniture sits
 * on the title slide while the objective may not.
 *
 * Usage: node z1_instrument_b.mjs <paths.txt> <out.json>
 */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const files = fs.readFileSync(process.argv[2], 'utf8').split('\n').map((s) => s.trim()).filter(Boolean);
const browser = await chromium.launch();
const out = [];
let n = 0;
for (const f of files) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  try {
    await page.goto('file://' + path.resolve(f), { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(300);
    const rec = await page.evaluate(() => {
      const slides = [...document.querySelectorAll('.slide')];
      let seen = document.body.innerText || '';
      if (slides.length > 1) {
        const prev = slides.map((s) => s.className);
        for (const s of slides) {
          slides.forEach((x) => x.classList.remove('active'));
          s.classList.add('active');
          s.removeAttribute('hidden');
          seen += '\n' + (document.body.innerText || '');
        }
        slides.forEach((s, i) => { s.className = prev[i]; });
      }
      const T = seen.replace(/ /g, ' ');
      const grab = (rx) => { const m = T.match(rx); return m ? (m[1] || m[0]).trim() : null; };

      return {
        // --- what week does the DECK say it is? four independent readings ---
        b_termLabel:   grab(/((?:Autumn|Spring|Summer)\s*[12]\s*[·.]\s*Week\s*\d+)/i),
        b_estateSeq:   grab(/Estate sequence[:\s]*W?(\d{1,2})/i),
        b_weekOf:      grab(/Week\s*(\d{1,2})\s*of\s*\d{1,2}/i),
        b_sowCell:     grab(/'([A-Za-z ]+(?:Weekly - )?(?:Autumn|Spring|Summer))'!([A-Z]\d{1,4})/),
        b_sowCellFull: grab(/('[A-Za-z ]+(?:Weekly - )?(?:Autumn|Spring|Summer)'![A-Z]\d{1,4}(?:\s*·\s*'[^']+'![A-Z]\d{1,4})?)/),
        b_htwk:        grab(/((?:Aut|Spr|Sum)[12]\s*[·.]\s*W\d+)/i),
        // The BRANDLINE. Three packs state their week only here and nowhere else,
        // in a dot-separated identity strip at the top of the deck:
        //   "GROW ASDAN · PERSONAL EFFECTIVENESS · AUTUMN 2 · W1"
        //   "BUILD · SCIENCE · WEEK 8A · EXPLORE"
        //   "LAUNCH · GCSE Biology · Week 8 · Introduce"
        // A first pass without these read 72 of 132 decks as stating no week at
        // all, which would have produced sixty false SOW-SILENT rows.
        b_brandTerm:   grab(/·\s*((?:AUTUMN|SPRING|SUMMER)\s*[12])\s*·\s*W\d+/i),
        b_brandWeek:   grab(/·\s*(?:AUTUMN|SPRING|SUMMER)\s*[12]\s*·\s*W(\d{1,2})/i),
        b_brandWeekAlt: grab(/·\s*WEEK\s*(\d{1,2})[A-Z]?\d?\s*·/i),
        b_brandline:   grab(/^([A-Z][A-Za-z ]+·[^\n]{4,90})$/m),
        // --- what does the deck say it teaches? ---
        b_exactOutcome: grab(/Exact SOW outcome:\s*([^\n]+)/i),
        b_seqOutcome:   grab(/Sequence outcome:\s*([^\n]+)/i),
        // Two layouts. BUILD_ASDAN and Science write "Learning objective: <text>"
        // on one line; GROW_ASDAN writes "🎯 Learning objective" as a heading with
        // the text on the NEXT line. A colon-only pattern read 18 GROW_ASDAN decks
        // as having no objective at all.
        b_objective:    grab(/(?:Learning objective|Objective)\s*:\s*([^\n]+)/i)
                     || grab(/(?:Learning objective|Objective)\s*\n+\s*([^\n]+)/i),
        b_enquiry:      grab(/Enquiry(?:\s*question)?:\s*([^\n]+)/i),
        b_title: (document.querySelector('h1') || {}).textContent?.trim() || null,
        b_docTitle: document.title || null,
        // success criteria: the list following the SC heading
        // Headings carry emoji and varying case across packs ("✅ Success
        // criteria", "Success Criteria"), so match on containment of the phrase
        // in a leaf element rather than on an exact string. An anchored
        // ^Success criteria$ found 24 of 132.
        b_sc: (() => {
          const h = [...document.querySelectorAll('*')].find(
            (e) => e.children.length === 0
                   && /success criteria/i.test((e.textContent || '').trim())
                   && (e.textContent || '').trim().length < 40);
          if (!h) return null;
          let p = h.parentElement;
          for (let i = 0; i < 3 && p; i++, p = p.parentElement) {
            const li = [...p.querySelectorAll('li')].map((x) => x.textContent.trim()).filter(Boolean);
            if (li.length) return li.slice(0, 6);
          }
          return null;
        })(),
        b_textLen: T.length,
        b_slides: slides.length,
      };
    });
    out.push({ file: f, ...rec });
  } catch (e) {
    out.push({ file: f, error: String(e && e.message || e) });
  }
  await page.close();
  if (++n % 25 === 0) console.error(`  ${n}/${files.length}`);
}
await browser.close();
fs.writeFileSync(process.argv[3], JSON.stringify(out, null, 1));
const wk = out.filter((r) => r.b_termLabel || r.b_estateSeq || r.b_weekOf || r.b_htwk).length;
console.error(`read ${out.length} decks; ${wk} yielded a week from the deck text`);
