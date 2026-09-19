// SX3 chassis contract row 41, behavioural: every dialog a deck carries can
// actually be OPENED by something in that deck. A dialog that exists in the
// markup and cannot be reached is a dialog the teacher does not have.
//
// This is measured in a rendered browser and nowhere else. A static parse can
// see that <dialog id="organiser-dialog"> exists; it cannot see whether any
// control opens it. ORDER SX3-GO2b ruling 5 forbids a static parse from
// emitting PASS for this row.
//
//   node tools/sx3/check_dialog_openers.mjs <directory-of-html> [output.json]
//
// The directory is REQUIRED and is validated before any browser starts. An
// earlier version of this harness read a hard-coded /tmp path and ignored its
// argument, and so reported a clean result for 75 decks that were not the ones
// under measurement. A scope that cannot be printed is not a scope, so this
// prints the directory and the file count before it measures anything.
import { chromium } from 'playwright';
import { readdirSync, writeFileSync, statSync } from 'fs';
import { join, resolve } from 'path';

const dir = process.argv[2];
const out = process.argv[3] || 'openers.json';

if (!dir) {
  console.error('FAIL: a directory of .html decks is required.\n' +
                '  usage: node tools/sx3/check_dialog_openers.mjs <directory> [output.json]');
  process.exit(2);
}
let entries;
try {
  if (!statSync(dir).isDirectory()) throw new Error('not a directory');
  entries = readdirSync(dir).filter(f => f.endsWith('.html'));
} catch (error) {
  console.error(`FAIL: cannot read ${resolve(dir)} as a directory of decks: ${error.message}`);
  process.exit(2);
}
if (!entries.length) {
  console.error(`FAIL: ${resolve(dir)} contains no .html deck to measure.`);
  process.exit(2);
}
console.log(`SEARCH SCOPE: ${entries.length} deck(s) in ${resolve(dir)}, rendered in Chromium`);

const browser = await chromium.launch();
const results = {};
for (const file of entries) {
  const context = await browser.newContext();
  const page = await context.newPage();
  // Record every open attempt, including one a deck's own handler swallows.
  await page.addInitScript(() => {
    window.print = () => {};
    window.__opens = [];
    const modal = HTMLDialogElement.prototype.showModal;
    const show = HTMLDialogElement.prototype.show;
    HTMLDialogElement.prototype.showModal = function () {
      window.__opens.push(this.id); try { return modal.call(this); } catch (e) {}
    };
    HTMLDialogElement.prototype.show = function () {
      window.__opens.push(this.id); try { return show.call(this); } catch (e) {}
    };
  });
  const errors = [];
  page.on('pageerror', e => errors.push(String(e.message).slice(0, 60)));
  await page.goto('file://' + resolve(join(dir, file)), { waitUntil: 'load' });
  results[file] = await page.evaluate(async () => {
    const opened = new Set();
    for (const el of Array.from(document.querySelectorAll('button,[data-action],[data-dialog]'))) {
      window.__opens.length = 0;
      try { el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true })); } catch (_) {}
      await new Promise(r => setTimeout(r, 5));
      window.__opens.forEach(id => opened.add(id));
      document.querySelectorAll('dialog[open]').forEach(d => { try { d.close(); } catch (_) {} });
    }
    const all = Array.from(document.querySelectorAll('dialog[id]')).map(d => d.id);
    return { dialogs: all, opened: Array.from(opened), unopenable: all.filter(x => !opened.has(x)) };
  });
  results[file].errors = errors.slice(0, 2);
  await context.close();
}
await browser.close();
writeFileSync(out, JSON.stringify(results, null, 1));

const bad = Object.entries(results).filter(([, v]) => v.unopenable.length);
console.log(`decks: ${entries.length} | all dialogs openable: ${entries.length - bad.length} | with an unopenable dialog: ${bad.length}`);
for (const [k, v] of bad.slice(0, 10)) console.log(`   ${k}  unopenable: ${v.unopenable.join(', ')}`);
process.exit(bad.length ? 1 : 0);
