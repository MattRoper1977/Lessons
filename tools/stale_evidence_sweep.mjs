/* THE STALE-EVIDENCE SWEEP.  R0.13 generalised from the T10b case, R0.14 and
 * R0.15 written into it after its own first two versions each failed in a
 * different direction.
 *
 * Evidence outlives its subject and looks identical to evidence that has not.
 * Two tracked files recorded per-transform verdicts for T10b — a transform
 * merged into T10 several commits earlier and non-existent since. They were
 * correctly formatted, internally consistent, and describing nothing.
 *
 * TWO DIRECTIONS, and the second is the more dangerous one:
 *   FORWARD  evidence naming a subject -> does that subject still exist?
 *   INVERSE  a subject the ledger implies has evidence -> does any exist?
 *
 * ---------------------------------------------------------------------------
 * WHY THIS FILE HAS BEEN WRITTEN THREE TIMES
 *
 * v1 matched any token SHAPED like a transform id. It reported T10a, T10b, X0
 * and X1c as stale. All four exist: T10a/T10b are CONTROL ids and X0/X1c are
 * ROW ids in a report. A sweep whose --apply would have deleted live evidence,
 * because it matched an identifier's shape rather than the claim. (R0.14.)
 *
 * v2 narrowed to removal-matrix rows only. That made the four false positives
 * go away and made the sweep incapable of firing at all: the tracked corpus
 * contains no matrix row, so both evidence files returned NOT APPLICABLE and
 * the headline read FORWARD 0 stale. Narrowing a predicate until the false reds
 * disappear is indistinguishable, from the outside, from breaking the check.
 * (R0.15.)
 *
 * v3 — this one — matches the CLAIM. A claim is a (form, subject, resolver)
 * triple read from the row's own grammar, and every form is grounded in a shape
 * that actually occurs in tracked evidence:
 *
 *   FORM                 shape                            subject, and what would make it stale
 *   transform-applied    "  T8a  03_Wilton….html"         the id is not declared in build.mjs,
 *                        inside a "== build" section      or the file is not in release/
 *   transform-watched    "  T8a  watched  P2.4->…"        the id is not declared in build.mjs
 *   control-exercised    the control name in that row     the control is not in controls.mjs
 *   path-named           "tools/….mjs", "…/x.html"        no such file
 *   route-named          '"/relicforge/"'                 no index.html at that route
 *   report-row           "X1c  PASS  the release Studio…" NOTHING. The id is a row label; the
 *                                                         subject is what the row names, and it
 *                                                         is resolved on its own.
 *
 * report-row is the rescue: it is why X0 and X1c are not stale, and the same
 * distinction — id in the label column versus id in the subject position —
 * is why T10a and T10b are not either.
 *
 * ---------------------------------------------------------------------------
 * R0.14: DRY RUN BY DEFAULT. The default run reports candidates and exits 0.
 * --apply is the only path that deletes, it deletes only a file in which EVERY
 * claim is stale, and it refuses anything outside evidence/ or qa/. A removal
 * you cannot show the subject is absent for is worse than keeping stale
 * evidence.
 *
 * R0.15: --self-test authors three genuinely-stale fixtures, of three different
 * shapes, and requires the narrowed sweep to catch all three by name; and it
 * replays T10a, T10b, X0 and X1c and requires all four not stale, each with its
 * reason. Neither half is optional: without the fixtures this is v2 again.
 *
 *   node tools/stale_evidence_sweep.mjs             report, change nothing
 *   node tools/stale_evidence_sweep.mjs --self-test positive and regression controls
 *   node tools/stale_evidence_sweep.mjs --apply     delete wholly-stale files
 */
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import os from 'node:os';

const ARGS = new Set(process.argv.slice(2));
const APPLY = ARGS.has('--apply');
const SELFTEST = ARGS.has('--self-test');

const REPOS = [
  { name: 'Lessons', root: '/home/user/Lessons' },
  { name: 'mattroper1977.github.io', root: '/workspace/mattroper1977.github.io' },
  { name: 'Matt-s-Apps-', root: '/workspace/matt-s-apps-' },
];

const tracked = root => {
  try { return execFileSync('git', ['-C', root, 'ls-files'], { encoding: 'utf8' }).split('\n').filter(Boolean); }
  catch { return []; }
};
const strip = s => s.replace(/\x1b\[[0-9;]*m/g, '');
const readIf = p => { try { return fs.readFileSync(p, 'utf8'); } catch { return null; } };

/* ------------------------------------------------------------------ forms */
/* Each form returns claims. A claim that no resolver can fail is recorded with
   verdict NOT A CLAIM and the reason, so the report never hides a row it chose
   not to judge — that silence is what v2 shipped. */

const ID = String.raw`[A-Z][0-9]+[a-z]?`;
const BUILD_ROW    = new RegExp(String.raw`^ {2}(${ID}) (\S+\.html)\s*$`);
const MATRIX_ROW   = new RegExp(String.raw`^\s{2,}(${ID})\s+(watched|LOAD-BEARING|UNWATCHED|DROPPED)\b\s*(\S+?)?(?:->|\s|$)`);
const REPORT_ROW   = new RegExp(String.raw`^(${ID})(?:\s+\S+)?\s{2,}(PASS|FAIL|SKIP|ERROR)\s`);
const PATH_NAMED   = /(?:tools|release|staging|Games)\/[A-Za-z0-9_./-]+\.(?:mjs|py|sh|js|html)/g;
const ROUTE_NAMED  = /"\/([a-z0-9-]{3,})\/"/g;
const SECTION      = /^==\s+(.+?)\s*$/;

function claimsFrom(text, ctx) {
  const claims = [];
  let section = '';
  for (const [i, raw] of strip(text).split('\n').entries()) {
    const line = raw.replace(/\s+$/, '');
    const sec = line.match(SECTION);
    if (sec) { section = sec[1]; continue; }

    let m;
    if (section.startsWith('build') && (m = line.match(BUILD_ROW))) {
      claims.push({ form: 'transform-applied', subject: m[1], resolver: 'transform', line: i + 1, ctx });
      claims.push({ form: 'transform-applied', subject: m[2], resolver: 'release-file', line: i + 1, ctx });
      continue;
    }
    if ((m = line.match(MATRIX_ROW))) {
      claims.push({ form: 'transform-watched', subject: m[1], resolver: 'transform', line: i + 1, ctx });
      if (m[3] && /^[A-Za-z][A-Za-z0-9._-]*$/.test(m[3]))
        claims.push({ form: 'control-exercised', subject: m[3], resolver: 'control', line: i + 1, ctx });
      continue;
    }
    if ((m = line.match(REPORT_ROW))) {
      /* THE RESCUE. The id here is a label in the first column of a report; the
         subject is whatever the row goes on to name, and the loop below picks
         that up on its own. Reading this id as a transform is exactly the
         mistake v1 made four times. */
      claims.push({ form: 'report-row', subject: m[1], resolver: 'none', line: i + 1, ctx,
                    why: 'row label in a report; the subject is named in the row text and resolved separately' });
      /* fall through — the row text still carries paths worth resolving */
    }
    for (const p of line.match(PATH_NAMED) || [])
      claims.push({ form: 'path-named', subject: p, resolver: 'path', line: i + 1, ctx });
    for (const r of [...line.matchAll(ROUTE_NAMED)].map(x => x[1]))
      claims.push({ form: 'route-named', subject: `/${r}/`, resolver: 'route', line: i + 1, ctx });
  }
  return claims;
}

/* -------------------------------------------------------------- resolvers */
function resolvers(root, evidenceFile) {
  const dir = path.dirname(path.join(root, evidenceFile));
  const near = name => [path.join(dir, '..', name), path.join(dir, name)].find(p => fs.existsSync(p)) || null;
  const buildPath = near('build.mjs');
  const ctlPath = near('controls.mjs');
  const build = buildPath ? readIf(buildPath) : null;
  const ctl = ctlPath ? readIf(ctlPath) : null;
  const releaseDir = [path.join(dir, '..', 'release'), path.join(dir, 'release')].find(p => fs.existsSync(p)) || null;

  return {
    /* A transform is declared by whichever helper declares it. The first cut of
       this resolver tested for `swap('T4'` and called T4 stale, because T4 is
       declared with inject(). That is R0.14 again, one layer down: it matched
       the SHAPE of a declaration rather than the claim that the id is declared.
       Match the id in a call position and let the helper be whatever it is. */
    transform: id => build === null
      ? [null, 'no sibling build.mjs — cannot judge whether this transform is declared']
      : [new RegExp(String.raw`\b[A-Za-z_$][\w$]*\('${id}'`).test(build),
         `a declaration of '${id}' in ${path.relative(root, buildPath)}`],
    control: id => ctl === null
      ? [null, 'no sibling controls.mjs — cannot judge whether this control is declared']
      : [ctl.includes(id), `'${id}' in ${path.relative(root, ctlPath)}`],
    'release-file': f => releaseDir === null
      ? [null, 'no sibling release/ — cannot judge']
      : [fs.existsSync(path.join(releaseDir, f)), `${path.relative(root, releaseDir)}/${f}`],
    path: p => [fs.existsSync(path.join(root, p)), p],
    route: r => [fs.existsSync(path.join(root, r.replace(/^\/|\/$/g, ''), 'index.html')), `${r}index.html`],
    none: () => [null, null],
  };
}

/* ------------------------------------------------------------------ sweep */
function forward(root, repoName) {
  const rows = [];
  const files = tracked(root).filter(f => /(^|\/)(evidence|qa)\//.test(f) && /\.(out|json|txt|md|log)$/.test(f));
  if (!files.length) {
    rows.push({ dir: 'forward', repo: repoName, file: '—', subject: '—', form: '—',
                verdict: 'NO EVIDENCE FILES', detail: 'no tracked file under evidence/ or qa/' });
    return rows;
  }
  for (const f of files) {
    const text = readIf(path.join(root, f));
    if (text === null) continue;
    const R = resolvers(root, f);
    const claims = claimsFrom(text, f);
    if (!claims.length) {
      rows.push({ dir: 'forward', repo: repoName, file: f, subject: '(nothing)', form: '—',
                  verdict: 'NO CLAIM FOUND',
                  detail: 'this file matched no claim form. That is a finding about the SWEEP as much as ' +
                          'the file — v2 of this tool reported exactly this over the whole corpus and read as green.' });
      continue;
    }
    /* one row per distinct (form, subject) — a transform applied to four files
       is one claim about the transform, not four */
    const seen = new Set();
    for (const c of claims) {
      const key = `${c.form} ${c.subject}`;
      if (seen.has(key)) continue;
      seen.add(key);
      const [ok, where] = R[c.resolver](c.subject);
      rows.push({
        dir: 'forward', repo: repoName, file: f, subject: c.subject, form: c.form, line: c.line,
        verdict: ok === null ? (c.resolver === 'none' ? 'NOT A CLAIM' : 'INCONCLUSIVE')
               : ok ? 'SUBJECT EXISTS' : 'STALE — SUBJECT ABSENT',
        detail: ok === null ? (c.why || where || 'no resolver could judge this')
              : ok ? `found: ${where}`
                   : `this row asserts ${c.form.replace(/-/g, ' ')} for ${c.subject}, and ${where} does not exist`,
      });
    }
  }
  return rows;
}

function inverse() {
  const rows = [];
  const root = '/workspace/mattroper1977.github.io';
  const covPath = path.join(root, 'data', 'hud-coverage.json');
  if (!fs.existsSync(covPath)) {
    rows.push({ dir: 'inverse', repo: 'mattroper1977.github.io', file: '—', subject: 'data/hud-coverage.json',
                form: 'declaration', verdict: 'SUBJECT ABSENT', detail: 'cannot assess' });
    return rows;
  }
  const cov = JSON.parse(fs.readFileSync(covPath, 'utf8'));
  let consumers = [];
  try {
    consumers = execFileSync('grep', ['-rl', '--include=*.py', '--include=*.mjs', '--include=*.js',
      '--include=*.sh', '--include=*.yml', 'scriptLine', root], { encoding: 'utf8' }).split('\n').filter(Boolean);
  } catch { consumers = []; }
  rows.push({
    dir: 'inverse', repo: 'mattroper1977.github.io', file: 'data/hud-coverage.json',
    subject: '.scriptLine', form: 'declaration',
    verdict: consumers.length ? 'HAS A CONSUMER' : 'NO CONSUMER — DECORATION',
    detail: consumers.length ? consumers.map(c => path.relative(root, c)).join(', ')
      : `the canonical string ${JSON.stringify(cov.scriptLine)} is read by no code in this repo`,
  });
  return rows;
}

function gitignoreShape() {
  return REPOS.map(({ name, root }) => {
    const transientTracked = tracked(root).filter(f => /^(audit-output|.*\/work)\//.test(f));
    const ig = readIf(path.join(root, '.gitignore')) || '';
    return {
      dir: 'gitignore', repo: name, file: '.gitignore', subject: 'audit-output/ · */work/', form: 'ignore rule',
      verdict: transientTracked.length === 0 ? 'NO TRANSIENT TRACKED' : 'TRANSIENT STILL TRACKED',
      detail: `tracked under an ignored path: ${transientTracked.length}` +
        (transientTracked.length ? ` — ${transientTracked.slice(0, 3).join(', ')}` : '') +
        ` · .gitignore names audit-output: ${/audit-output/.test(ig)}` +
        (transientTracked.length && /audit-output/.test(ig)
          ? ' — the rule is present AND the files are tracked, which is the ignoring-is-not-untracking case' : ''),
    };
  });
}

/* ----------------------------------------------------------------- report */
function report(rows) {
  const W = [9, 24, 18, 34];
  console.log(`${'direction'.padEnd(W[0])} ${'repo'.padEnd(W[1])} ${'form'.padEnd(W[2])} ${'subject'.padEnd(W[3])} verdict`);
  console.log('-'.repeat(120));
  for (const r of rows) {
    console.log(`${r.dir.padEnd(W[0])} ${r.repo.padEnd(W[1])} ${String(r.form).padEnd(W[2])} ${String(r.subject).slice(0, 34).padEnd(W[3])} ${r.verdict}`);
    console.log(`${' '.repeat(W[0] + 1)}${r.file}${r.line ? `:${r.line}` : ''} — ${r.detail}`);
  }
  const stale = rows.filter(r => /^STALE/.test(r.verdict));
  const decor = rows.filter(r => r.verdict === 'NO CONSUMER — DECORATION');
  const dirty = rows.filter(r => r.verdict === 'TRANSIENT STILL TRACKED');
  const mute = rows.filter(r => r.verdict === 'NO CLAIM FOUND');
  console.log(`\nFORWARD   ${stale.length} stale claim(s) · ${rows.filter(r => r.verdict === 'SUBJECT EXISTS').length} live · ` +
              `${rows.filter(r => r.verdict === 'NOT A CLAIM').length} row label(s) correctly not judged · ${mute.length} file(s) matching no form`);
  console.log(`INVERSE   ${decor.length} declaration(s) with no consumer`);
  console.log(`IGNORE    ${dirty.length} repo(s) tracking output under an ignored path`);
  return { stale, decor, dirty, mute };
}

/* ------------------------------------------------------------------ apply */
function apply(rows) {
  /* Delete only a file in which EVERY judged claim is stale. One live claim and
     the file stays, because the live claim is the thing worth keeping. */
  const byFile = new Map();
  for (const r of rows.filter(x => x.dir === 'forward' && x.file !== '—')) {
    if (!byFile.has(r.file)) byFile.set(r.file, []);
    byFile.get(r.file).push(r);
  }
  let removed = 0;
  for (const [file, rs] of byFile) {
    const judged = rs.filter(r => r.verdict === 'STALE — SUBJECT ABSENT' || r.verdict === 'SUBJECT EXISTS');
    if (!judged.length || judged.some(r => r.verdict === 'SUBJECT EXISTS')) {
      console.log(`KEEP    ${file} — ${judged.filter(r => r.verdict === 'SUBJECT EXISTS').length} live claim(s)`);
      continue;
    }
    if (!/(^|\/)(evidence|qa)\//.test(file)) { console.log(`REFUSE  ${file} — outside evidence/ and qa/`); continue; }
    const repo = REPOS.find(x => x.name === rs[0].repo);
    console.log(`REMOVE  ${file} — every one of its ${judged.length} claim(s) names an absent subject`);
    fs.rmSync(path.join(repo.root, file));
    removed++;
  }
  console.log(`\n--apply removed ${removed} file(s).`);
  return removed;
}

/* -------------------------------------------------------------- self-test */
function selfTest() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'sweep-'));
  const root = path.join(tmp, 'repo');
  fs.mkdirSync(path.join(root, 'tools', 'kit', 'evidence'), { recursive: true });
  fs.mkdirSync(path.join(root, 'tools', 'kit', 'release'), { recursive: true });
  const kit = path.join(root, 'tools', 'kit');
  fs.writeFileSync(path.join(kit, 'build.mjs'),
    // T4 is declared with inject(), not swap(). It is here because a resolver
    // that tests for swap( alone calls T4 stale on the real corpus, and did.
    `swap('T1', 'a.html', 'x', 'y');\nswap('T2', 'a.html', 'x', 'y');\n` +
    `swap('T9renamed', 'a.html', 'x', 'y');\nfor (const f of ALL) inject('T4', f, CALM);\n`);
  fs.writeFileSync(path.join(kit, 'controls.mjs'), `const P2_LIVE = 'P2.4';\n`);
  fs.writeFileSync(path.join(kit, 'release', 'a.html'), '<html></html>');
  fs.writeFileSync(path.join(kit, 'tool_present.mjs'), '');
  execFileSync('git', ['-C', root, 'init', '-q']);
  execFileSync('git', ['-C', root, 'config', 'user.email', 'a@b.c']);
  execFileSync('git', ['-C', root, 'config', 'user.name', 't']);

  const ev = f => path.join(kit, 'evidence', f);

  /* ---- FIXTURE 1: a subject that was DELETED ------------------------------ */
  fs.writeFileSync(ev('AUTHORED-FIXTURE_deleted-subject.out'),
    '== build  release/ -> staging/\n  T1 a.html\n  T4 a.html\n  T7b a.html\n');

  /* ---- FIXTURE 2: a subject that was RENAMED ----------------------------- *
   * The harder case. T9 was renamed to T9renamed; the id still LOOKS live —
   * the string "T9" occurs in build.mjs as a prefix of the new name — and a
   * substring test would call it present. */
  fs.writeFileSync(ev('AUTHORED-FIXTURE_renamed-subject.out'),
    '== build  release/ -> staging/\n  T2 a.html\n  T9 a.html\n');

  /* ---- FIXTURE 3: the subject exists, the CLAIM does not ------------------ *
   * T1 is declared and always will be. The row's claim is that dropping T1
   * moves control P2.9gone, and that control is not in controls.mjs. This is
   * the fixture v2 would have missed twice over: it has a matrix row, so v2
   * would have parsed it, and it would have judged only the transform. */
  fs.writeFileSync(ev('AUTHORED-FIXTURE_claim-without-referent.out'),
    '== removal matrix\n  T1    watched      P2.9gone->CONTROL 1->[X]\n');

  /* ---- REGRESSION: the four v1 destroyed ---------------------------------- */
  fs.writeFileSync(ev('AUTHORED-FIXTURE_regression-four.out'),
    '== removal matrix\n' +
    '  T1    watched      P2.4->CONTROL 1->[W]\n' +
    '                     controls: T10a T10b are the two halves of the merged T10 control\n' +
    '== transport\n' +
    'X0            PASS     the subject is present at tools/kit/release/a.html\n' +
    'X1c           PASS     the release Studio cannot mint a C21 mission (declared asymmetry)\n');

  execFileSync('git', ['-C', root, 'add', '-A']);
  execFileSync('git', ['-C', root, 'commit', '-qm', 'authored fixtures']);

  const rows = forward(root, 'FIXTURE');
  const verdictOf = (file, subject) =>
    rows.find(r => r.file.endsWith(file) && r.subject === subject);

  let fails = 0;
  const check = (label, cond, detail) => {
    console.log(`  ${cond ? 'PASS' : 'FAIL'}  ${label}${detail ? ` — ${detail}` : ''}`);
    if (!cond) fails++;
  };

  console.log('§4.2 POSITIVE CONTROLS — three authored genuinely-stale fixtures, three shapes');
  console.log('     (AUTHORED BY --self-test. Not a real run, not a pack sample.)');
  const f1 = verdictOf('deleted-subject.out', 'T7b');
  check('1. deleted subject   T7b', f1 && /^STALE/.test(f1.verdict), f1 && f1.verdict);
  const f2 = verdictOf('renamed-subject.out', 'T9');
  check('2. renamed subject   T9 (build.mjs now declares T9renamed)', f2 && /^STALE/.test(f2.verdict), f2 && f2.verdict);
  const f3 = verdictOf('claim-without-referent.out', 'P2.9gone');
  check('3. claim without referent  P2.9gone (T1 itself is live)', f3 && /^STALE/.test(f3.verdict), f3 && f3.verdict);
  const t1 = verdictOf('claim-without-referent.out', 'T1');
  check('   ...and T1 on that same row is NOT stale', t1 && t1.verdict === 'SUBJECT EXISTS', t1 && t1.verdict);
  const t4 = verdictOf('deleted-subject.out', 'T4');
  check('   ...and T4, declared with inject() rather than swap(), is NOT stale',
        t4 && t4.verdict === 'SUBJECT EXISTS', t4 && t4.verdict);

  console.log('\n§4.1 REGRESSION — the four subjects v1 called stale must not be');
  for (const [id, why] of [['T10a', 'control id in a control table, not a subject position'],
                           ['T10b', 'control id in a control table, not a subject position'],
                           ['X0', 'row label in a report; the row names its own subject'],
                           ['X1c', 'row label in a report; the row names its own subject']]) {
    const r = rows.find(x => x.subject === id);
    const notStale = !r || !/^STALE/.test(r.verdict);
    check(`${id.padEnd(5)} not stale`, notStale, r ? `${r.verdict} · ${why}` : `not read as a claim at all · ${why}`);
  }

  console.log('\n§4.3 DRY RUN — the default run must leave a known-stale file alone');
  const victim = ev('AUTHORED-FIXTURE_deleted-subject.out');
  const before = fs.readFileSync(victim);
  const stillThere = fs.existsSync(victim) && Buffer.compare(before, fs.readFileSync(victim)) === 0;
  check('file present and byte-identical after a default (no --apply) run', stillThere);
  const dirty = execFileSync('git', ['-C', root, 'status', '--porcelain'], { encoding: 'utf8' }).trim();
  check('git status clean after a default run', dirty === '', dirty || 'clean');

  console.log('\n§4.4 the inverse direction still runs');
  const inv = inverse();
  check('inverse produced a row', inv.length > 0, inv.map(r => `${r.subject}: ${r.verdict}`).join(' · '));

  fs.rmSync(tmp, { recursive: true, force: true });
  console.log(`\n[SELF-TEST] ${fails === 0 ? 'PASS' : 'FAIL'} — ${fails} check(s) failed`);
  return fails === 0 ? 0 : 1;
}

/* -------------------------------------------------------------------- main */
if (SELFTEST) {
  process.exit(selfTest());
} else {
  const rows = [...REPOS.flatMap(r => forward(r.root, r.name)), ...inverse(), ...gitignoreShape()];
  const { stale, decor, dirty, mute } = report(rows);
  if (APPLY) {
    console.log('\n--apply: deleting only files in which EVERY claim names an absent subject.\n');
    apply(rows);
    process.exit(0);
  }
  console.log(`\nDRY RUN. This changed nothing. ${stale.length} candidate(s) for removal are named above with`);
  console.log(`the file, the line and the subject, so each can be ruled on individually; --apply acts on them,`);
  console.log(`and only on a file with no live claim left in it. Removing real evidence is worse than keeping`);
  console.log(`stale evidence, so the default is to report.`);
  if (mute.length) console.log(`\nNOTE: ${mute.length} evidence file(s) matched no claim form. Read that as a gap in this`);
  if (mute.length) console.log(`sweep, not as a clean bill — it is the failure v2 shipped.`);
  process.exit(0);
}
