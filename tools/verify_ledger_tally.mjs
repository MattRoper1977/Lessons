/* THE LEDGER'S TALLY IS DERIVED FROM ITS OWN TABLE, OR IT IS NOT A MEASUREMENT.
 *
 * R0.8: a count without a stated predicate is not a measurement.
 * R0.12: read the artefact, not its summary — and the tally sentence IS a
 * summary, sitting directly above the table it summarises.
 *
 * This has now gone wrong twice in the same file. PR #120 existed because a
 * count said nine while its table listed ten. The repair landed, and the next
 * reading found the prose saying twelve above a table of thirteen rows. A
 * number fixed by hand drifts by hand again a fortnight later, so the number
 * stops being written down and starts being derived.
 *
 * WHAT IT PARSES
 *   the predicate sentence   "Counted as one row per check that could not fire,
 *                             where it was found; two such defects in one commit
 *                             count twice."
 *   the derivation sentence  "The table below has N rows: a in these gates,
 *                             b Matt-side, c found by re-reading an artefact
 *                             (a + b + c = N)."
 *   the table                every pipe-row under the named header
 *   the adjacent list        the reporting-defects list and its own count
 *
 * WHAT IT ASSERTS
 *   N (prose) == rows counted in the table
 *   a + b + c == N, arithmetic done here rather than trusted
 *   the reporting-defects count == rows in that list
 *   the predicate sentence is present at all — a derivation with no predicate
 *   is the exact defect this file is about, so its absence is a failure and
 *   not a warning.
 *
 *   node tools/verify_ledger_tally.mjs [path]
 *   node tools/verify_ledger_tally.mjs --self-test
 *
 * Exit 0 green · 1 the prose and the table disagree · 2 INCONCLUSIVE (the
 * ledger, the table or the sentence could not be found — never green, because
 * a parser that finds nothing must not report nothing wrong).
 */
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

const HERE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ARGS = process.argv.slice(2);
const SELFTEST = ARGS.includes('--self-test');
const LEDGER = ARGS.find(a => !a.startsWith('--')) ||
  path.join(HERE, 'RELEASE_LEDGER_2026-08-16.md');

const TABLE_HEADER = '| what was wrong with the check |';
const REPORT_HEADER = '| the report that was true and buried it |';
const PREDICATE = /Counted as one row per check that could not fire/;
const DERIVATION = /The table below has (\d+) rows?: (\d+) in these gates, (\d+) Matt-side, (\d+) found by re-reading an artefact \(\2 \+ \3 \+ \4 = \1\)/;
const REPORT_COUNT = /(\d+) reporting defects? of the same family/;

class Inconclusive extends Error {}

/* Count the data rows of the markdown table whose header line starts with
   `header`. The separator row is not data; a blank line or a non-pipe line
   ends the table. */
function tableRows(text, header) {
  const lines = text.split('\n');
  const i = lines.findIndex(l => l.startsWith(header));
  if (i < 0) return null;
  const rows = [];
  for (const l of lines.slice(i + 1)) {
    if (!l.startsWith('|')) break;
    if (/^\|[\s|:-]*\|$/.test(l)) continue;      // the |---|---| separator
    rows.push(l);
  }
  return rows;
}

function check(file) {
  let text;
  try { text = fs.readFileSync(file, 'utf8'); }
  catch (e) { throw new Inconclusive(`cannot read ${file}: ${e.message}`); }

  /* Prose is matched against a whitespace-normalised copy, because markdown
     wraps a sentence wherever the column runs out and the claim does not
     change with the wrap point. The TABLE is counted on the raw text, where
     line breaks are structural. Matching prose on raw text made this checker
     red on a correct ledger the first time it ran — a false positive in the
     tool written to catch a miscount, which would have taught the next reader
     to distrust it. */
  const flat = text.replace(/\s+/g, ' ');
  const fails = [];
  const note = [];

  const rows = tableRows(text, TABLE_HEADER);
  if (rows === null) throw new Inconclusive(`no table found under "${TABLE_HEADER}…"`);

  if (!PREDICATE.test(flat))
    fails.push('the predicate sentence is absent — a derivation with no predicate is R0.8, ' +
               'and it is the defect this check exists for');

  const d = flat.match(DERIVATION);
  if (!d) {
    fails.push('the derivation sentence is absent or does not match the required shape: ' +
               '"The table below has N rows: a in these gates, b Matt-side, c found by ' +
               're-reading an artefact (a + b + c = N)"');
  } else {
    const [, N, a, b, c] = d.map(Number);
    note.push(`prose: N=${N} (${a} gates + ${b} Matt-side + ${c} re-read)`);
    note.push(`table: ${rows.length} data row(s)`);
    if (N !== rows.length)
      fails.push(`the prose says ${N} and the table has ${rows.length} rows`);
    if (a + b + c !== N)
      fails.push(`the sub-counts do not sum: ${a} + ${b} + ${c} = ${a + b + c}, stated as ${N}`);
  }

  /* The adjacent list is optional in shape but, if present, is held to the same
     rule: its stated count must equal its rows. */
  const rrows = tableRows(text, REPORT_HEADER);
  const rc = flat.match(REPORT_COUNT);
  if (rrows !== null || rc) {
    if (rrows === null) fails.push('a reporting-defects count is stated but no such table exists');
    else if (!rc) fails.push('a reporting-defects table exists but states no count');
    else {
      note.push(`reporting defects: prose ${Number(rc[1])}, table ${rrows.length}`);
      if (Number(rc[1]) !== rrows.length)
        fails.push(`reporting defects: prose says ${rc[1]}, table has ${rrows.length}`);
    }
  }

  return { fails, note, rows: rows.length };
}

/* ------------------------------------------------------------- self-test */
/* R0.15 and the three-mutations rule: one mutation proves the harness can go
   red once. Three prove that each of the three things it claims to compare is
   actually compared. */
function selfTest() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'tally-'));
  const copy = path.join(tmp, 'ledger.md');
  fs.copyFileSync(LEDGER, copy);
  const pristine = fs.readFileSync(copy, 'utf8');
  let fails = 0;
  const say = (label, ok, detail) => {
    console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${label}${detail ? ` — ${detail}` : ''}`);
    if (!ok) fails++;
  };

  const baseline = check(copy);
  say('the unmutated ledger is green', baseline.fails.length === 0,
      baseline.fails.join(' · ') || baseline.note.join(' · '));

  /* Every mutation operates on the RAW text, because that is what a person or a
     bad merge would edit. The first cut wrote (a) and (b) against the
     whitespace-normalised form and against a reconstructed header line; both
     matched nothing and changed nothing, and the run reported two inert
     mutations rather than two passes. That guard is why they are correct now,
     and it stays. */
  const rowAt = t => {
    const l = t.split('\n');
    const i = l.findIndex(x => x.startsWith(TABLE_HEADER));
    return { l, sep: i + 1 };            // header, then the |---|---| separator
  };
  const mutations = [
    ['(a) the prose number is changed',
      t => t.replace(/has (\d+) rows:/, (s, n) => `has ${+n + 1} rows:`)],
    ['(b) a row is added to the table',
      t => { const { l, sep } = rowAt(t);
             l.splice(sep + 1, 0, '| AUTHORED BY --self-test | not a real finding |');
             return l.join('\n'); }],
    ['(c) a row is removed from the table',
      t => { const { l, sep } = rowAt(t); l.splice(sep + 1, 1); return l.join('\n'); }],
  ];

  for (const [label, mutate] of mutations) {
    const mutated = mutate(pristine);
    if (mutated === pristine) { say(label, false, 'the mutation changed nothing — it proves nothing'); continue; }
    fs.writeFileSync(copy, mutated);
    let red = false, why = '';
    try { const r = check(copy); red = r.fails.length > 0; why = r.fails.join(' · '); }
    catch (e) { red = true; why = `INCONCLUSIVE: ${e.message}`; }
    say(label, red, why || 'NO FAILURE REPORTED');
    fs.writeFileSync(copy, pristine);
  }

  const restored = check(copy);
  say('restored: green again', restored.fails.length === 0, restored.fails.join(' · '));

  fs.rmSync(tmp, { recursive: true, force: true });
  console.log(`\n[SELF-TEST] ${fails === 0 ? 'PASS' : 'FAIL'} — ${fails} check(s) failed`);
  return fails === 0 ? 0 : 1;
}

/* -------------------------------------------------------------------- main */
try {
  if (SELFTEST) process.exit(selfTest());
  const { fails, note } = check(LEDGER);
  console.log(`ledger tally — ${path.relative(HERE, LEDGER)}`);
  for (const n of note) console.log(`  ${n}`);
  for (const f of fails) console.log(`  [FAIL] ${f}`);
  console.log(fails.length
    ? `\n${fails.length} disagreement(s) between the prose and the table it summarises.`
    : '\nthe stated count is the counted count, and the sub-counts sum.');
  process.exit(fails.length ? 1 : 0);
} catch (e) {
  if (e instanceof Inconclusive) {
    console.log(`[INCONCLUSIVE] ${e.message}`);
    console.log('A parser that finds nothing must not report nothing wrong.');
    process.exit(2);
  }
  throw e;
}
