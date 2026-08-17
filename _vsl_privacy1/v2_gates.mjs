/* §3 GATES — every one fired in BOTH directions, each red named.
 *
 * Reads location.hash, never the clipboard: a headless clipboard permission
 * must not be able to fake a pass.
 *
 * NAMED MUTANTS, one per gate that needs its own:
 *   M0  the original, unpatched file            -> reds gates 1, 2
 *   M1  strip inside serialisableState()        -> reds gate 3 (export)
 *   M2  print handler clears notes              -> reds gate 4 (print)
 *   M3  patched but WITHOUT change 2            -> reds gate 6 (legacy link)
 *   M4  corrupted token (not a file mutant)     -> reds gate 5 (round trip)
 *
 * The order proposed "strip from serialisableState() instead" as the red for
 * BOTH the export and print gates. It does not fire for print: preparePrint()
 * reads state.notes directly and never goes through serialisableState(), so
 * that mutant leaves the print gate green. A control that cannot fire is not a
 * control, so print gets M2 of its own.
 */
import { chromium } from 'playwright';
import fs from 'node:fs';

const ORIG = process.argv[2];
const PATCHED = process.argv[3];
const TMP = process.argv[4];

const PUPIL = 'CANARY_PUPIL_Jamie_Roper';
const NOTES = 'CANARY_NOTES_felt_anxious_during_the_practical';

let reds = 0, greens = 0;
const failures = [];

function record(gate, direction, ok, detail) {
  if (direction === 'red') reds++; else greens++;
  const tag = ok ? 'OK  ' : 'FAIL';
  console.log(`  [${tag}] ${direction.toUpperCase().padEnd(5)} ${gate}${detail ? ' — ' + detail : ''}`);
  if (!ok) failures.push(`${gate} [${direction}]: ${detail}`);
}

/* ---------------------------------------------------------------- mutants */
function mutant(name, from, fn) {
  const p = `${TMP}/${name}.html`;
  fs.writeFileSync(p, fn(fs.readFileSync(from, 'utf8')));
  return p;
}
function must(s, old, neu, label) {
  if (s.split(old).length - 1 !== 1) throw new Error(`mutant ${label}: anchor not unique`);
  return s.replace(old, neu);
}

const M1 = mutant('M1_strip_in_serialisableState', PATCHED, s =>
  must(s, 'copy.bioRespirometer.running=false;return copy;',
          'copy.bioRespirometer.running=false;delete copy.pupil;delete copy.notes;return copy;', 'M1'));

const M2 = mutant('M2_print_clears_notes', PATCHED, s =>
  must(s, 'dom.print.addEventListener("click",()=>{state.pupil=dom.pupil.value.trim();state.notes=dom.notes.value.trim();',
          'dom.print.addEventListener("click",()=>{state.pupil=dom.pupil.value.trim();state.notes="";', 'M2'));

const M3 = mutant('M3_no_change_2', PATCHED, s =>
  must(s, 'delete incoming.pupil;delete incoming.notes;', '', 'M3'));

/* ---------------------------------------------------------------- helpers */
const browser = await chromium.launch();

async function withPage(file, hash, fn) {
  const page = await browser.newPage();
  const errs = [];
  page.on('pageerror', e => errs.push(String(e)));
  await page.goto('file://' + file + (hash || ''));
  const out = await fn(page, errs);
  await page.close();
  return out;
}

function decode(hash) {
  const m = hash.match(/^#s=(.+)$/);
  if (!m) return null;
  const b64 = m[1].replace(/-/g, '+').replace(/_/g, '/');
  return Buffer.from(b64, 'base64').toString('utf8');
}

/* Types both canaries, then EITHER clicks Share or performs an ordinary bench
   interaction, and returns the decoded token. */
async function hashAfter(file, viaShare) {
  return withPage(file, '', async page => {
    await page.fill('#pupilName', PUPIL);
    await page.fill('#reflectionNotes', NOTES);
    if (viaShare) {
      await page.click('#shareBtn');
    } else {
      await page.click('#calmBtn');            // one of the 119, no Share involved
    }
    await page.waitForTimeout(250);
    return decode(await page.evaluate(() => location.hash));
  });
}

console.log('GATES — both directions, each red named\n');

/* -------- gate 1: canary absent via Share -------------------------------- */
{
  const g = await hashAfter(PATCHED, true);
  const ok = g !== null && !g.includes(PUPIL) && !g.includes(NOTES);
  record('1 canary absent via Share', 'green', ok, ok ? 'neither canary in the token' : 'canary STILL PRESENT');
  const r = await hashAfter(ORIG, true);
  const rok = r !== null && r.includes(PUPIL) && r.includes(NOTES);
  record('1 canary absent via Share', 'red', rok, 'M0 original: ' + (rok ? 'both canaries present, as expected' : 'did not fire'));
}

/* -------- gate A: canary absent WITHOUT Share ---------------------------- */
{
  const g = await hashAfter(PATCHED, false);
  const ok = g !== null && !g.includes(PUPIL) && !g.includes(NOTES);
  record('A canary absent WITHOUT Share', 'green', ok, ok ? 'ordinary bench interaction, neither canary' : 'canary STILL PRESENT');
  const r = await hashAfter(ORIG, false);
  const rok = r !== null && r.includes(PUPIL) && r.includes(NOTES);
  record('A canary absent WITHOUT Share', 'red', rok, 'M0 original: ' + (rok ? 'both canaries in the hash with no Share click' : 'did not fire'));
}

/* -------- gate 3: evidence export still carries the fields --------------- */
async function exportPayload(file) {
  return withPage(file, '', async page => {
    await page.fill('#pupilName', PUPIL);
    await page.fill('#reflectionNotes', NOTES);
    return page.evaluate(() => {
      let captured = null;
      const orig = URL.createObjectURL;
      URL.createObjectURL = b => { captured = b; return 'blob:stub'; };
      document.querySelector('#exportBtn').click();
      URL.createObjectURL = orig;
      return captured ? captured.text() : null;
    });
  });
}
{
  const g = await exportPayload(PATCHED);
  const ok = !!g && g.includes(PUPIL) && g.includes(NOTES);
  record('3 evidence export keeps them', 'green', ok, ok ? 'name and notes present in the export' : 'export LOST them');
  const r = await exportPayload(M1);
  const rok = !!r && !r.includes(PUPIL) && !r.includes(NOTES);
  record('3 evidence export keeps them', 'red', rok, 'M1 strip-in-serialisableState: ' + (rok ? 'export lost them, as expected' : 'did not fire'));
}

/* -------- gate 4: print pack still carries the notes --------------------- */
async function printHTML(file) {
  return withPage(file, '', async page => {
    await page.fill('#pupilName', PUPIL);
    await page.fill('#reflectionNotes', NOTES);
    return page.evaluate(() => {
      const p = window.print; window.print = () => {};
      document.querySelector('#printBtn').click();
      window.print = p;
      return document.querySelector('#printSheet').innerHTML;
    });
  });
}
{
  const g = await printHTML(PATCHED);
  const ok = !!g && g.includes(NOTES);
  record('4 print pack keeps the notes', 'green', ok, ok ? 'notes present in the print sheet' : 'print LOST them');
  const r = await printHTML(M2);
  const rok = !!r && !r.includes(NOTES);
  record('4 print pack keeps the notes', 'red', rok, 'M2 print-clears-notes: ' + (rok ? 'print lost them, as expected' : 'did not fire'));
}

/* -------- gate 5: state round trip --------------------------------------- */
{
  const hash = await withPage(PATCHED, '', async page => {
    await page.selectOption('#disciplineSelect', 'biology');
    await page.selectOption('#benchSelect', 'photosynthesis');
    await page.evaluate(() => {
      const el = document.querySelector('#photoDistance');
      el.value = 65;
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new Event('change', { bubbles: true }));
    });
    await page.waitForTimeout(200);
    return page.evaluate(() => location.hash);
  });
  const restored = await withPage(PATCHED, hash, async page => page.evaluate(() => ({
    bench: document.querySelector('#benchSelect').value,
    dist: document.querySelector('#photoDistance')?.value,
  })));
  const ok = restored.bench === 'photosynthesis' && String(restored.dist) === '65';
  record('5 state round trip', 'green', ok, `restored bench=${restored.bench} distance=${restored.dist}`);

  const corrupt = '#s=' + 'Zm9vYmFy'.repeat(3);
  const bad = await withPage(PATCHED, corrupt, async page => page.evaluate(() => ({
    bench: document.querySelector('#benchSelect').value,
  })));
  const rok = bad.bench !== 'photosynthesis';
  record('5 state round trip', 'red', rok, 'M4 corrupted token: ' + (rok ? `restore refused, fell back to ${bad.bench}` : 'did not fire'));
}

/* -------- gate 6: a legacy link does not repopulate ---------------------- */
{
  const legacy = await withPage(ORIG, '', async page => {
    await page.fill('#pupilName', PUPIL);
    await page.fill('#reflectionNotes', NOTES);
    await page.click('#shareBtn');
    await page.waitForTimeout(250);
    return page.evaluate(() => location.hash);
  });
  const legacyCarries = (decode(legacy) || '').includes(PUPIL);

  const g = await withPage(PATCHED, legacy, async page => page.evaluate(() => ({
    pupil: document.querySelector('#pupilName').value,
    notes: document.querySelector('#reflectionNotes').value,
  })));
  const ok = legacyCarries && g.pupil === '' && g.notes === '';
  record('6 legacy link does not repopulate', 'green', ok,
    `pre-fix link carries the name=${legacyCarries}; patched opens with pupil="${g.pupil}" notes="${g.notes}"`);

  const r = await withPage(M3, legacy, async page => page.evaluate(() => ({
    pupil: document.querySelector('#pupilName').value,
  })));
  const rok = r.pupil === PUPIL;
  record('6 legacy link does not repopulate', 'red', rok, 'M3 no-change-2: ' + (rok ? 'the old link repopulated the name, as expected' : 'did not fire'));
}

/* -------- gate 7: page errors across 13 benches -------------------------- */
{
  const res = await withPage(PATCHED, '', async (page, errs) => {
    const cons = [];
    page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') cons.push(m.text()); });
    const benches = [['chemistry', ['spatial', 'microscale', 'rates', 'titration', 'gastest']],
                     ['biology', ['microscopy', 'enzyme', 'osmosis', 'foodtests', 'photosynthesis', 'microbiology', 'ecology', 'respirometer']]];
    let n = 0;
    for (const [disc, list] of benches) {
      await page.selectOption('#disciplineSelect', disc);
      for (const b of list) { await page.selectOption('#benchSelect', b); await page.waitForTimeout(110); n++; }
    }
    return { n, errs, cons };
  });
  const ok = res.n === 13 && res.errs.length === 0 && res.cons.length === 0;
  record('7 page errors across 13 benches', 'green', ok,
    `${res.n}/13 benches, ${res.errs.length} page errors, ${res.cons.length} console errors+warnings`);
}

await browser.close();

console.log('');
console.log(`CONTROLS: ${reds} red fired, ${greens} green returned`);
if (failures.length) {
  console.log('\nFAILURES — land nothing:');
  failures.forEach(f => console.log('  ' + f));
  process.exit(1);
}
console.log('Every gate fired in both directions.');
