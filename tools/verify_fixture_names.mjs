/* A TEST FIXTURE IN A PUBLIC REPOSITORY IS PUBLISHED DATA.
 *
 * Canaries, samples and placeholder names are real content to every reader who
 * finds them. This check fails when a fixture string is shaped like a person.
 *
 * PROVENANCE. The estate shipped `CANARY_PUPIL_Jamie_Roper` — a plausible
 * first name, carrying the repository owner's surname, in a PUBLIC repo, inside
 * the file whose whole subject is not leaving pupil names where they do not
 * belong. It was self-found and replaced with a string nobody can mistake for a
 * person, and the gates were re-run at 6 red / 7 green. This check exists so
 * the next one is caught by a mechanism rather than by noticing.
 *
 * THE PREDICATE, stated so it can be argued with:
 *   take each fixture-marker token, strip the marker, split on _ / space,
 *   and count TITLECASE words — ^[A-Z][a-z]{2,}$.
 *     two or more  -> PERSON-SHAPED   (Jamie Roper, John Smith)
 *     one or none  -> SYNTHETIC       (NOT_A_REAL_PERSON, SAMPLE_RATE, TEST_0001)
 *   plus a surname list, which is PERSON-SHAPED whatever the case.
 *
 * WHAT IT DOES NOT CATCH, said plainly rather than left to be discovered.
 * It detects person-shaped NAMES, not plausible pupil PROSE. The sibling canary
 * `CANARY_NOTES_felt_anxious_during_the_practical` is all lower case and passes
 * this check, yet reads as something a real child wrote about themselves. It
 * was replaced by hand for that reason. A check that claimed to cover it would
 * be claiming to judge whether a sentence sounds like a child, which this does
 * not do. The gap is real and is recorded rather than papered over.
 *
 *   node tools/verify_fixture_names.mjs            check the tree
 *   node tools/verify_fixture_names.mjs --self-test
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const SELFTEST = process.argv.includes('--self-test');

const MARKER = /(CANARY|FIXTURE|PLACEHOLDER|DUMMY|MOCK|STUB|SAMPLE|TESTNAME|TEST_NAME)/i;
/* The leading run is ZERO-or-more, and that is not a detail. It was written as
   `[A-Za-z_][A-Za-z0-9_]*` — requiring at least one character BEFORE the marker
   — which meant a token STARTING with the marker never matched. That is the
   exact shape of `CANARY_PUPIL_Jamie_Roper`: this check would have reported the
   tree clean while the string it was written for sat in it. Caught by the
   seeded-file control below, which is the reason that control exists rather
   than testing judge() alone: judging a string correctly proves the predicate,
   not the check. */
const TOKEN = /[A-Za-z0-9_]*(?:CANARY|FIXTURE|PLACEHOLDER|DUMMY|MOCK|STUB|SAMPLE|TESTNAME|TEST_NAME)[A-Za-z0-9_]*/gi;

/* Real surnames that must never appear in a fixture, whatever the casing.
   Short and specific on purpose: a long guessy list would red the estate on
   ordinary words and be deleted within the week. */
const SURNAMES = ['roper'];

/* Directories that are not this estate's content. Vendored libraries carry
   their authors' real names and emails as package metadata — that is their
   provenance, not our fixture, and rewriting it would be false attribution. */
const SKIP_DIRS = new Set(['.git', 'node_modules', 'vendor', 'audit-output']);

/* NARROW allowlist: exact string, exact file, with a reason. The rule this
   check enforces requires its own provenance to be quotable — scrubbing the
   record of what was found would destroy the evidence the rule rests on, and
   would rewrite rather than supersede. Entries are per-file so this cannot
   become a blanket excuse. */
const ALLOW = [
  { file: 'RELEASE_LEDGER_2026-08-16.md', text: 'CANARY_PUPIL_Jamie_Roper',
    why: 'the dated record of what was planted, and the provenance the fixture-naming rule rests on' },
  /* This checker's own test vectors. A detector for person-shaped strings has
     to contain person-shaped strings, or its reds are untested. Declared token
     by token rather than by exempting the file, so a real fixture added here
     later is still caught — an allowlist that covers a whole file is an excuse
     with a filename. */
  { file: 'tools/verify_fixture_names.mjs', text: 'CANARY_PUPIL_Jamie_Roper',
    why: "this check's own red vector — the string that actually shipped" },
  { file: 'tools/verify_fixture_names.mjs', text: 'FIXTURE_John_Smith',
    why: "this check's own red vector — a plain first name + surname" },
  { file: 'tools/verify_fixture_names.mjs', text: 'SAMPLE_roper',
    why: "this check's own red vector — a listed surname in lower case" },
  { file: 'tools/verify_fixture_names.mjs', text: 'CANARY_PUPIL_Alice_Roper',
    why: "the seeded string the self-test writes and deletes, quoted here to assert on it" },
  /* Order N6, 2026-08-28. "Mock interview" is standard careers vocabulary and this is a
     real LAUNCH ASDAN W11 lesson, not a fixture. It trips the predicate only because MOCK
     is a fixture marker and the surrounding words are ordinary titlecase — the check reads
     Mock/Interview/Answer/Evidence/Improve as >=2 titlecase words and calls it person-shaped.
     No person is named. Listed per file, as the allowlist requires, so any OTHER
     person-shaped string in these same files is still caught. */
  { file: 'LAUNCH_ASDAN/W7-W12_2026-27/manifest.json',
    text: 'CAREERS_W11_Mock_Interview_Answer_Evidence_Improve_LAUNCH',
    why: 'real careers lesson title; MOCK is a fixture marker but this names no person' },
  { file: 'LAUNCH_ASDAN/W7-W12_2026-27/START_HERE.html',
    text: 'CAREERS_W11_Mock_Interview_Answer_Evidence_Improve_LAUNCH',
    why: 'real careers lesson title; MOCK is a fixture marker but this names no person' },
  { file: 'LAUNCH_ASDAN/W7-W12_2026-27/SHA256SUMS.txt',
    text: 'CAREERS_W11_Mock_Interview_Answer_Evidence_Improve_LAUNCH',
    why: 'real careers lesson title; MOCK is a fixture marker but this names no person' },
  /* This checker quotes that lesson title three times above, so it now trips its own
     predicate — the same recursion the red-vector entries above solve. Declared once:
     the matcher is (file, text), so one entry covers all occurrences in this file. */
  { file: 'tools/verify_fixture_names.mjs',
    text: 'CAREERS_W11_Mock_Interview_Answer_Evidence_Improve_LAUNCH',
    why: "this file's own allowlist entries for that lesson title" },
  /* Order OM3, 2026-08-29. The same real lesson title, in the five N6-M SoW and
     evidence records that also carry it. The four entries above were written when the
     title lived only in the LAUNCH_ASDAN pack; the reconcile puts it in the SoW data too,
     and the matcher is (file, text), so each file needs saying. Same reasoning as above:
     MOCK is a fixture marker, the neighbouring words are ordinary titlecase, and no person
     is named. Per file, so any OTHER person-shaped string in these files is still caught. */
  { file: '_next6/SOW_MATRIX.md',
    text: 'CAREERS_W11_Mock_Interview_Answer_Evidence_Improve_LAUNCH',
    why: 'real careers lesson title; MOCK is a fixture marker but this names no person' },
  { file: '_next6/evidence/S24_EVIDENCE_SURFACES.txt',
    text: 'CAREERS_W11_Mock_Interview_Answer_Evidence_Improve_LAUNCH',
    why: 'real careers lesson title; MOCK is a fixture marker but this names no person' },
  { file: '_next6/sow/groups/10_LAUNCH_ASDAN__W7-W12_2026-27.json',
    text: 'CAREERS_W11_Mock_Interview_Answer_Evidence_Improve_LAUNCH',
    why: 'real careers lesson title; MOCK is a fixture marker but this names no person' },
  { file: '_next6/sow/lessons.json',
    text: 'CAREERS_W11_Mock_Interview_Answer_Evidence_Improve_LAUNCH',
    why: 'real careers lesson title; MOCK is a fixture marker but this names no person' },
  { file: '_next6/sow/worklist.json',
    text: 'CAREERS_W11_Mock_Interview_Answer_Evidence_Improve_LAUNCH',
    why: 'real careers lesson title; MOCK is a fixture marker but this names no person' },
];

function titlecaseCount(tok) {
  return tok.split(/[_\s-]+/).filter(w => /^[A-Z][a-z]{2,}$/.test(w)).length;
}

export function judge(tok) {
  const low = tok.toLowerCase();
  if (SURNAMES.some(s => low.includes(s))) return 'PERSON-SHAPED';
  if (titlecaseCount(tok) >= 2) return 'PERSON-SHAPED';
  return 'SYNTHETIC';
}

function* walk(dir) {
  let entries;
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return; }
  for (const e of entries) {
    if (e.isDirectory()) {
      if (SKIP_DIRS.has(e.name)) continue;
      yield* walk(path.join(dir, e.name));
    } else if (e.isFile()) {
      yield path.join(dir, e.name);
    }
  }
}

function scan(root) {
  const hits = [];
  let files = 0;
  for (const f of walk(root)) {
    files++;
    let text;
    try { text = fs.readFileSync(f, 'utf8'); } catch { continue; }
    if (!MARKER.test(text)) continue;
    const rel = path.relative(root, f);
    for (const m of text.matchAll(TOKEN)) {
      const tok = m[0];
      const verdict = judge(tok);
      if (verdict !== 'PERSON-SHAPED') continue;
      const allowed = ALLOW.find(a => a.file === rel && a.text === tok);
      hits.push({ file: rel, token: tok, allowed: !!allowed, why: allowed?.why });
    }
  }
  return { files, hits };
}

if (SELFTEST) {
  let bad = 0;
  const say = (ok, label, detail) => {
    console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${label}${detail ? ` — ${detail}` : ''}`);
    if (!ok) bad++;
  };

  /* RED — the string that actually shipped, and the shapes like it. */
  say(judge('CANARY_PUPIL_Jamie_Roper') === 'PERSON-SHAPED',
      'RED: the canary that actually shipped is person-shaped', 'CANARY_PUPIL_Jamie_Roper');
  say(judge('FIXTURE_John_Smith') === 'PERSON-SHAPED',
      'RED: a plain first-name + surname fixture is caught', 'FIXTURE_John_Smith');
  say(judge('SAMPLE_roper') === 'PERSON-SHAPED',
      'RED: a real surname is caught whatever the casing', 'SAMPLE_roper');

  /* GREEN — the replacement, and the estate's ordinary technical fixtures.
     A check that reds these would be deleted within the week. */
  say(judge('CANARY_NAMEFIELD_NOT_A_REAL_PERSON') === 'SYNTHETIC',
      'GREEN: the replacement passes', 'CANARY_NAMEFIELD_NOT_A_REAL_PERSON');
  say(judge('SAMPLE_ALPHA_TO_COVERAGE') === 'SYNTHETIC',
      'GREEN: a real technical constant is not a person', 'SAMPLE_ALPHA_TO_COVERAGE');
  say(judge('HALF_SAMPLE_RATE') === 'SYNTHETIC', 'GREEN: HALF_SAMPLE_RATE');
  say(judge('FIXTURE_deleted') === 'SYNTHETIC', 'GREEN: FIXTURE_deleted');
  say(judge('PLACEHOLDER') === 'SYNTHETIC', 'GREEN: bare PLACEHOLDER');

  /* The gate must go red on a SEEDED file, not only on a string in isolation —
     otherwise it proves the predicate and not the check. */
  const seeded = path.join(ROOT, '.fixture-selftest-seed.md');
  fs.writeFileSync(seeded, 'a seeded fixture: CANARY_PUPIL_Alice_Roper\n');
  const after = scan(ROOT).hits.filter(h => !h.allowed);
  fs.unlinkSync(seeded);
  say(after.some(h => h.token === 'CANARY_PUPIL_Alice_Roper'),
      'RED: a seeded person-shaped fixture reds the real tree', `${after.length} unallowed hit(s) while seeded`);

  const clean = scan(ROOT).hits.filter(h => !h.allowed);
  say(clean.length === 0,
      'GREEN: the real corpus, with the seed removed, is clean',
      `${clean.length} unallowed hit(s)`);

  console.log(`\n[SELF-TEST] ${bad === 0 ? 'PASS' : 'FAIL'} — ${bad} check(s) failed`);
  process.exit(bad === 0 ? 0 : 1);
}

const { files, hits } = scan(ROOT);
const live = hits.filter(h => !h.allowed);
const allowed = hits.filter(h => h.allowed);

console.log(`SCOPE: ${ROOT}`);
console.log(`  ${files} file(s), no path filter and no type filter; skipped: ${[...SKIP_DIRS].join(', ')}`);
console.log(`  predicate: a fixture-marker token with >=2 Titlecase words, or containing a listed surname`);
console.log('');
if (allowed.length) {
  console.log('ALLOWED, each with its reason:');
  const seen = new Map();
  for (const h of allowed) {
    const k = `${h.file} ${h.token}`;
    seen.set(k, { ...h, n: (seen.get(k)?.n || 0) + 1 });
  }
  for (const h of seen.values()) {
    console.log(`  ${h.file}: ${h.token}${h.n > 1 ? ` (×${h.n})` : ''}`);
    console.log(`     ${h.why}`);
  }
  console.log('');
}
if (live.length) {
  console.log('PERSON-SHAPED FIXTURES — a reader cannot tell these from a real person:');
  for (const h of live) console.log(`  ${h.file}: ${h.token}`);
  console.log('\nReplace them with something nobody could mistake for a person.');
  process.exit(1);
}
console.log('No person-shaped fixture strings. Clean, with the scope printed above.');
console.log('NOTE: this catches person-shaped NAMES, not plausible pupil PROSE — see the header.');
process.exit(0);
