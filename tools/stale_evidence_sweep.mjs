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
import { fileURLToPath } from 'node:url';

const ARGS = new Set(process.argv.slice(2));
const APPLY = ARGS.has('--apply');
const SELFTEST = ARGS.has('--self-test');
/* R0.17 in practice, and §5 of the residue order: an honest INCONCLUSIVE that
   nothing ever resolves is a check that cannot fire, dressed politely. It fails
   in the friendliest possible way, because every run looks green and every
   verdict is true. In CI the number of roots is knowable, so it is asserted:
   --require-roots=3 exits 2 unless three roots were actually assessed. */
const REQUIRE_ROOTS = (() => {
  const a = [...ARGS].find(x => x.startsWith('--require-roots='));
  return a ? Number(a.split('=')[1]) : null;
})();

/* THE ROOTS ARE DERIVED, AND AN ABSENT ONE IS SAID SO.
 *
 * The first CI run of this sweep printed "FORWARD 0 stale" over THREE
 * repositories it could not see: the roots were absolute paths from the
 * container this was written in, none of which exist on a runner. The
 * self-test still bit - it builds its own fixture - but the sweep's own line
 * read clean while asserting nothing, which is the failure this whole tool
 * exists to find, shipped inside it.
 *
 * So: this repository is located from the script's own path, the siblings are
 * looked for and MAY BE OVERRIDDEN, and a root that is not a git repository is
 * reported as NOT ASSESSED - a verdict of its own, never folded into "no
 * evidence files found". */
const HERE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const isRepo = r => { try { return fs.statSync(path.join(r, '.git')) && true; } catch { return false; } };
const sibling = (env, ...guesses) =>
  process.env[env] || guesses.find(g => isRepo(g)) || guesses[0];
const REPOS = [
  { name: 'Lessons', root: HERE },
  { name: 'mattroper1977.github.io',
    root: sibling('MBM_SITE_REPO', '/workspace/mattroper1977.github.io',
                  path.join(HERE, '..', 'mattroper1977.github.io')) },
  { name: 'Matt-s-Apps-',
    root: sibling('MBM_APPS_REPO', '/workspace/matt-s-apps-',
                  path.join(HERE, '..', 'matt-s-apps-')) },
].map(r => ({ ...r, present: isRepo(r.root) }));

const tracked = root => {
  try {
    return execFileSync('git', ['-C', root, 'ls-files'],
      { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).split('\n').filter(Boolean);
  } catch { return []; }
};
const strip = s => s.replace(/\x1b\[[0-9;]*m/g, '');

/* Every declaration site in a builder, and the callee that made it. Enumerated
   from the source rather than matched against a list of verbs this tool happens
   to know, so a seventh declaration form is DISCOVERED, not missed. */
const DECL_SITE = /\b([A-Za-z_$][\w$]*)\s*\(\s*'([A-Z][0-9]+[a-z]?)'/g;
const _declCache = new Map();
function declaredIds(src) {
  if (_declCache.has(src)) return _declCache.get(src);
  const m = new Map();
  for (const [, callee, id] of src.matchAll(DECL_SITE)) if (!m.has(id)) m.set(id, callee);
  _declCache.set(src, m);
  return m;
}
const readIf = p => { try { return fs.readFileSync(p, 'utf8'); } catch { return null; } };

/* ------------------------------------------------------------------ forms */
/* Each form returns claims. A claim that no resolver can fail is recorded with
   verdict NOT A CLAIM and the reason, so the report never hides a row it chose
   not to judge — that silence is what v2 shipped. */

const ID = String.raw`[A-Z][0-9]+[a-z]?`;
const BUILD_ROW    = new RegExp(String.raw`^ {2}(${ID}) (\S+\.html)\s*$`);
const MATRIX_ROW   = new RegExp(String.raw`^\s{2,}(${ID})\s+(watched|LOAD-BEARING|UNWATCHED|DROPPED)\b\s*(\S+?)?(?:->|\s|$)`);
/* Two widenings, both made because the NO FORM MATCHED control below reported
   the rows this missed rather than skipping them, which is the whole argument
   for having that control. It required TWO spaces before the verdict, so
   "A0 PASS ..." with one space fell through; and it knew only PASS/FAIL/SKIP/
   ERROR, so assert_unchanged's whole vocabulary - "U3  UNCHANGED ..." - was
   invisible. Twelve real rows in the tracked corpus, silently unjudged. */
/* A report LABEL is not a transform id and does not have to look like one:
   run_all.out labels rows W-BOIL, W-STRICT, W-GAP. Third widening, and the
   third one the NO FORM MATCHED control reported rather than swallowed. */
const ROW_LABEL    = String.raw`[A-Z][A-Za-z0-9-]*`;
const REPORT_ROW   = new RegExp(String.raw`^(${ROW_LABEL})(?:\s+\S+)*?\s+(PASS|FAIL|SKIP|ERROR|UNCHANGED|CHANGED|ASSERTED)\b`);
const PATH_NAMED   = /(?:tools|release|staging|Games)\/[A-Za-z0-9_./-]+\.(?:mjs|py|sh|js|html)/g;
const ROUTE_NAMED  = /"\/([a-z0-9-]{3,})\/"/g;
const SECTION      = /^==\s+(.+?)\s*$/;
/* A row that states a verdict about something. Used only to decide whether a
   line that matched no claim form was a row this sweep should have understood. */
const ASSERTING_ROW = /\b(PASS|FAIL|SKIP|ERROR|UNCHANGED|CHANGED|ASSERTED|watched|UNWATCHED|DROPPED|LOAD-BEARING|STALE)\b/;

/* ------------------------------------------------- form: qa-record (JSON)
   WHY THIS EXISTS. forward() already selects .json under evidence/ and qa/ —
   the sweep intends to judge those files — but every claim form above is
   line-oriented text. REPORT_ROW needs a line to BEGIN with a bare label, so
   `  "boot": "PASS",` can never match it; the row fell to ASSERTING_ROW and was
   booked NO FORM MATCHED. Twenty such rows in Matt-s-Apps- held the sweep at
   exit 2 while naming nothing stale.
   The proof that this is a gap in the GRAMMAR and not evidence about the data:
   MOBILE_QA_RESULTS.json carries twelve records of the identical shape and
   produced zero unparsed rows — only because its records say "ok": true instead
   of the word PASS. Visible or invisible by vocabulary, not by validity.
   This form READS MORE, it does not judge less: a QA record naming a file that
   has since been deleted now returns STALE, which the text grammar could not
   see at all. Files that do not parse as JSON, or that yield no record naming a
   subject, fall through to the text forms untouched — NO FORM MATCHED still
   fires for every shape nobody has taught this tool yet. */
const QA_VERDICT = /^(PASS|FAIL|SKIP|ERROR|UNCHANGED|CHANGED|ASSERTED)$/;

function qaClaimsFrom(text, ctx) {
  let doc;
  try { doc = JSON.parse(text); } catch { return []; }
  if (doc === null || typeof doc !== 'object') return [];
  const claims = [];
  const walk = (node, trail) => {
    if (Array.isArray(node)) { node.forEach((v, i) => walk(v, `${trail}[${i}]`)); return; }
    if (node === null || typeof node !== 'object') return;
    if (typeof node.file === 'string' && node.file)
      claims.push({ form: 'qa-record', subject: node.file, resolver: 'qa-subject', line: 0, ctx,
                    why: 'a QA record naming the file it reports on' });
    for (const [k, v] of Object.entries(node)) {
      if (typeof v === 'string' && QA_VERDICT.test(v) && k !== 'file')
        /* A verdict whose subject is the record it sits in, or the document as a
           whole. Recorded rather than dropped, and marked NOT A CLAIM with the
           reason — the same treatment report-row labels already get, because a
           row this tool chooses not to judge must still be visible. */
        claims.push({ form: 'qa-verdict', subject: `${trail}.${k}`, resolver: 'none', line: 0, ctx,
                      why: `verdict "${v}" on ${trail}.${k}; its subject is the file named by the ` +
                           `enclosing record, which is judged separately` });
      else walk(v, `${trail}.${k}`);
    }
  };
  walk(doc, path.basename(ctx));
  /* Only take the structural route if it actually recognised a subject. A JSON
     file with no record naming anything is not "understood" — it goes back to
     the text forms so it can still be reported. */
  return claims.some(c => c.form === 'qa-record') ? claims : [];
}

function claimsFrom(text, ctx) {
  const structural = qaClaimsFrom(text, ctx);
  if (structural.length) return structural;
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
    /* A row that plainly asserts something and matched no form is a RESULT, not
       a silence. The corpus figure "0 files matching no form" was good evidence
       and was never proof that a seventh row shape would be caught — a row in a
       file with other claims was skipped without a word. */
    if (!m && ASSERTING_ROW.test(line) && !PATH_NAMED.test(line) && !line.trimStart().startsWith('#'))
      claims.push({ form: 'no-form-matched', subject: line.trim().slice(0, 40), resolver: 'unmatched',
                    line: i + 1, ctx, why: 'this row states a verdict and matched none of the claim forms' });
    PATH_NAMED.lastIndex = 0;
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
    /* THE T4 CLASS, CLOSED AT THE CLASS RATHER THAN THE INSTANCE.
       v3 tested for `swap('T4'` and called T4 stale, because T4 is declared with
       inject(). Widening to "any call position" fixed that instance and left the
       class open: the resolver still held a vocabulary, and a transform declared
       in a form nobody had thought of would still come back STALE — the worst
       possible verdict, because it is indistinguishable from a real one and it
       is what --apply acts on.
       So the declaration forms are ENUMERATED from build.mjs rather than known:
       every `<callee>('<ID>'` in the file is a declaration site, whatever the
       callee is called, and declaredIds() below is the set. An id that is not in
       that set and not resolvable is UNRESOLVED — FORM NOT RECOGNISED, never
       STALE. "I cannot see it" and "it is not there" are different answers and
       only one of them justifies a removal. */
    transform: id => {
      if (build === null) return [null, 'no sibling build.mjs — cannot judge whether this transform is declared'];
      const declared = declaredIds(build);
      if (declared.has(id)) return [true, `declared in ${path.relative(root, buildPath)} via ${declared.get(id)}(`];
      /* Not found by any recognised declaration syntax. Two very different
         reasons, and only one of them justifies a removal. */
      if (new RegExp(String.raw`\b${id}\b`).test(build))
        return ['unresolved', `'${id}' occurs in ${path.relative(root, buildPath)} but not in any ` +
          `declaration shape this sweep recognises (found: ${[...new Set(declared.values())].sort().join(', ') || 'none'}). ` +
          `That is a gap in THIS TOOL, not evidence about the transform.`];
      return [false, `no declaration of '${id}' in ${path.relative(root, buildPath)}, and the id ` +
                     `does not occur in that file at all`];
    },
    control: id => ctl === null
      ? [null, 'no sibling controls.mjs — cannot judge whether this control is declared']
      : [ctl.includes(id), `'${id}' in ${path.relative(root, ctlPath)}`],
    'release-file': f => releaseDir === null
      ? [null, 'no sibling release/ — cannot judge']
      : [fs.existsSync(path.join(releaseDir, f)), `${path.relative(root, releaseDir)}/${f}`],
    /* A QA record says "index.html" and means the file beside the qa/ folder
       that reports on it, not <repo root>/index.html. Resolving against the root
       would return STALE — SUBJECT ABSENT for a file that plainly exists, and
       STALE is the verdict --apply acts on. Try the project that owns the qa/
       directory, then the directory itself, then the root, and say which one
       answered. */
    'qa-subject': f => {
      const tries = [[path.join(dir, '..', f), 'project dir'], [path.join(dir, f), 'qa dir'],
                     [path.join(root, f), 'repo root']];
      const hit = tries.find(([p]) => fs.existsSync(p));
      return hit ? [true, `${path.relative(root, hit[0])} (${hit[1]})`]
                 : [false, `no ${f} beside ${path.relative(root, path.join(dir, '..'))}, in ` +
                           `${path.relative(root, dir)}, or at the repository root`];
    },
    path: p => [fs.existsSync(path.join(root, p)), p],
    route: r => [fs.existsSync(path.join(root, r.replace(/^\/|\/$/g, ''), 'index.html')), `${r}index.html`],
    none: () => [null, null],
    unmatched: () => ['unmatched', null],
  };
}

/* ------------------------------------------------------------------ sweep */
function forward(root, repoName, present = true) {
  const rows = [];
  if (!present) {
    rows.push({ dir: 'forward', repo: repoName, file: '—', subject: root, form: '—',
                verdict: 'NOT ASSESSED — REPO ABSENT',
                detail: 'not a git repository at this path, so this sweep saw none of it. ' +
                        'This is NOT the same as finding nothing stale, and is counted separately.' });
    return rows;
  }
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
        verdict: ok === 'unmatched' ? 'NO FORM MATCHED'
               : ok === 'unresolved' ? 'UNRESOLVED — FORM NOT RECOGNISED'
               : ok === null ? (c.resolver === 'none' ? 'NOT A CLAIM' : 'INCONCLUSIVE')
               : ok ? 'SUBJECT EXISTS' : 'STALE — SUBJECT ABSENT',
        detail: ok === 'unmatched' ? c.why
              : ok === 'unresolved' ? where
              : ok === null ? (c.why || where || 'no resolver could judge this')
              : ok ? `found: ${where}`
                   : `this row asserts ${c.form.replace(/-/g, ' ')} for ${c.subject}, and ${where} does not exist`,
      });
    }
  }
  return rows;
}

function inverse() {
  const rows = [];
  const root = REPOS.find(r => r.name === 'mattroper1977.github.io').root;
  const covPath = path.join(root, 'data', 'hud-coverage.json');
  if (!fs.existsSync(covPath)) {
    rows.push({ dir: 'inverse', repo: 'mattroper1977.github.io', file: '—', subject: 'data/hud-coverage.json',
                form: 'declaration', verdict: 'NOT ASSESSED — SUBJECT NOT CHECKED OUT',
                detail: `no ${path.join(root, 'data', 'hud-coverage.json')} here. The inverse direction ` +
                        'needs the site repository present; set MBM_SITE_REPO to point at it.' });
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
  return REPOS.filter(r => r.present).map(({ name, root }) => {
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
  /* Per repo, what was read. A total is not three numbers: a corpus of 24 claims
     is a different thing when one repository contributed all of them. */
  console.log(`\n${'repo'.padEnd(24)} ${'assessed'.padEnd(10)} ${'evidence files'.padEnd(15)} claims judged`);
  for (const { name } of REPOS) {
    const mine = rows.filter(r => r.repo === name && r.dir === 'forward');
    const seen = !mine.some(r => /^NOT ASSESSED/.test(r.verdict));
    const files = new Set(mine.filter(r => r.file && r.file !== '—').map(r => r.file));
    const judged = mine.filter(r => r.verdict === 'SUBJECT EXISTS' || /^STALE/.test(r.verdict)).length;
    console.log(`${name.padEnd(24)} ${(seen ? 'yes' : 'NO').padEnd(10)} ${String(files.size).padEnd(15)} ${judged}`);
  }

  const stale = rows.filter(r => /^STALE/.test(r.verdict));
  const decor = rows.filter(r => r.verdict === 'NO CONSUMER — DECORATION');
  const dirty = rows.filter(r => r.verdict === 'TRANSIENT STILL TRACKED');
  const mute = rows.filter(r => r.verdict === 'NO CLAIM FOUND');
  const unseen = rows.filter(r => /^NOT ASSESSED/.test(r.verdict));
  console.log(`\nFORWARD   ${stale.length} stale claim(s) · ${rows.filter(r => r.verdict === 'SUBJECT EXISTS').length} live · ` +
              `${rows.filter(r => r.verdict === 'NOT A CLAIM').length} row label(s) correctly not judged · ${mute.length} file(s) matching no form`);
  console.log(`INVERSE   ${decor.length} declaration(s) with no consumer`);
  console.log(`IGNORE    ${dirty.length} repo(s) tracking output under an ignored path`);
  if (unseen.length) {
    console.log(`\nNOT ASSESSED  ${unseen.length} subject(s) this run could not see at all:`);
    for (const r of unseen) console.log(`  ${r.repo} — ${r.detail.split('.')[0]}`);
    console.log(`A run that cannot see a repository has not cleared it. The zero above is a`);
    console.log(`statement about what was read, not about what exists.`);
  }
  return { stale, decor, dirty, mute, unseen };
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

  const rows = forward(root, 'FIXTURE', true);
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

  console.log('\n§4.5 THE SEVENTH FORM — an unrecognised declaration must not read as stale');
  /* T20 is declared with DOUBLE quotes. Every declaration in the real builder
     uses single quotes, so this is a shape nobody wrote a rule for - which is
     exactly the point. The wrong answer here is STALE, because that is what
     --apply acts on. */
  const buildPath = path.join(kit, 'build.mjs');
  const pristineBuild = fs.readFileSync(buildPath, 'utf8');
  fs.writeFileSync(buildPath, pristineBuild + '\nswap("T20", "a.html", "x", "y");\n');
  fs.writeFileSync(ev('AUTHORED-FIXTURE_seventh-form.out'),
    '== build  release/ -> staging/\n  T20 a.html\n');
  execFileSync('git', ['-C', root, 'add', '-A']);
  execFileSync('git', ['-C', root, 'commit', '-qm', 'seventh form']);
  const seventh = forward(root, 'FIXTURE', true);
  const t20 = seventh.find(r => r.subject === 'T20');
  check('T20 is UNRESOLVED, not STALE', t20 && t20.verdict === 'UNRESOLVED — FORM NOT RECOGNISED',
        t20 ? t20.verdict : 'no row at all');
  check('the unresolved count is non-zero and reported',
        seventh.filter(r => /^UNRESOLVED/.test(r.verdict)).length === 1);
  check('T20 is NOT among the removal candidates',
        !seventh.some(r => r.subject === 'T20' && /^STALE/.test(r.verdict)));
  fs.rmSync(ev('AUTHORED-FIXTURE_seventh-form.out'));
  fs.writeFileSync(buildPath, pristineBuild);
  execFileSync('git', ['-C', root, 'add', '-A']);
  execFileSync('git', ['-C', root, 'commit', '-qm', 'restore']);
  check('restored: unresolved back to 0',
        forward(root, 'FIXTURE', true).filter(r => /^UNRESOLVED/.test(r.verdict)).length === 0);

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
  const rows = [...REPOS.flatMap(r => forward(r.root, r.name, r.present)), ...inverse(), ...gitignoreShape()];
  const { stale, decor, dirty, mute, unseen } = report(rows);
  const unresolved = rows.filter(r => /^UNRESOLVED/.test(r.verdict));
  const noform = rows.filter(r => r.verdict === 'NO FORM MATCHED');
  if (unresolved.length || noform.length) {
    console.log(`\n[INCONCLUSIVE] ${unresolved.length} subject(s) this sweep could not resolve and ` +
                `${noform.length} row(s) it could not parse.`);
    for (const r of [...unresolved, ...noform]) console.log(`  ${r.file}:${r.line} ${r.subject} — ${r.detail}`);
    console.log('A subject the tool cannot see is not a subject that is gone. The run does not');
    console.log('pass with one outstanding, because the alternative is calling it stale.');
    process.exit(2);
  }
  if (REQUIRE_ROOTS !== null) {
    const assessed = REPOS.filter(r => r.present).length;
    console.log(`\nROOTS  ${assessed} assessed, ${REQUIRE_ROOTS} required.`);
    if (assessed < REQUIRE_ROOTS) {
      console.log(`[INCONCLUSIVE] ${REQUIRE_ROOTS - assessed} root(s) were not assessed:`);
      for (const r of REPOS.filter(x => !x.present)) console.log(`  ${r.name} — nothing at ${r.root}`);
      console.log('NOT ASSESSED is a diagnostic, never a passing state where the count is knowable.');
      process.exit(2);
    }
  }
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
