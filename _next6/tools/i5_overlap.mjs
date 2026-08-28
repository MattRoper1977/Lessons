#!/usr/bin/env node
/**
 * ORDER N6-I · I5 — the overlap risk, measured in the DOM.
 *
 * A hide-set is only safe if the selectors it targets carry staff text and
 * nothing else. This asks, for every class in every deck, how many of its
 * instances carry a staff string in their OWN text.
 *
 * Read the two buckets carefully, because neither means "safe":
 *
 *   ALWAYS — every instance of the class carries a staff string. That is
 *            necessary for a hide candidate and NOT sufficient: the same
 *            element's own text may also carry pupil content. `.hero` in
 *            BUILD_ASDAN is 24/24 and still holds the lesson's <h1>.
 *   MIXED  — some instances carry one and some do not, so the class cannot be
 *            hidden without taking pupil content with it. `.chip` is 24 of 96:
 *            one chip per deck is "Estate sequence W9" and three are the lane,
 *            unit and week a pupil reads.
 *
 * The risk this exists to price: the patcher's own comments record an incident
 * where mis-tagging left 140 of 175 decks showing "a heading and nothing else"
 * in front of a class.
 *
 * Measured in a real DOM, not by regex over the source. A regex that matches
 * `<tag class="…">…</tag>` consumes nested children inside the first match and
 * silently skips them — an earlier pass of this check missed `.chip` entirely
 * for exactly that reason. Element.textContent on the live tree cannot.
 *
 * Usage: node i5_overlap.mjs <paths.txt> [out.json]
 */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const STAFF = /Estate sequence|Exact SOW outcome|Inherited (mapping|evidence)|AQA UAS|'[A-Za-z ]+ (Weekly - )?(Autumn|Spring|Summer)'![A-Z]\d/;
const files = fs.readFileSync(process.argv[2], 'utf8').split('\n').map((s) => s.trim()).filter(Boolean);
const b = await chromium.launch();
const per = {};
for (const f of files) {
  const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  try {
    await p.goto('file://' + path.resolve(f), { waitUntil: 'load' });
    await p.waitForTimeout(250);
    const rows = await p.evaluate((src) => {
      const rx = new RegExp(src);
      const out = [];
      for (const e of document.querySelectorAll('[class]')) {
        // Own text only — text in this element that is not inside a nested
        // element that also carries a class. Otherwise every ancestor inherits
        // its descendants' staff strings and everything looks mixed.
        let own = '';
        for (const n of e.childNodes) {
          if (n.nodeType === 3) own += n.nodeValue;
          else if (n.nodeType === 1 && !n.getAttribute('class')) own += n.textContent;
        }
        if (!own.trim()) continue;
        out.push([String(e.className).split(/\s+/).filter(Boolean), rx.test(own)]);
      }
      return out;
    }, STAFF.source);
    const k = f.split('/').slice(0, 2).join('/');
    per[k] ??= {};
    for (const [classes, isStaff] of rows) {
      for (const c of classes) {
        per[k][c] ??= [0, 0];
        per[k][c][1]++;
        if (isStaff) per[k][c][0]++;
      }
    }
  } catch (e) { /* a deck that will not load is a separate problem */ }
  await p.close();
}
await b.close();
for (const k of Object.keys(per).sort()) {
  const mixed = Object.entries(per[k]).filter(([, v]) => v[0] > 0 && v[0] < v[1]);
  const pure = Object.entries(per[k]).filter(([, v]) => v[0] > 0 && v[0] === v[1]);
  console.log(`${k}`);
  console.log(`   ALWAYS staff-bearing (necessary, NOT sufficient — may also hold pupil text): ${pure.length ? pure.map(([c, v]) => `.${c} ${v[1]}`).join(', ') : 'none'}`);
  console.log(`   MIXED — hiding these takes pupil content with them: ${mixed.length ? mixed.map(([c, v]) => `.${c} ${v[0]}/${v[1]}`).join(', ') : 'none'}`);
}
if (process.argv[3]) fs.writeFileSync(process.argv[3], JSON.stringify(per, null, 1));
