/* §3 — THE STALE-EVIDENCE SWEEP.  R0.13, generalised from the T10b case.
 *
 * Evidence outlives its subject and looks identical to evidence that has not.
 * Two tracked files recorded per-transform verdicts for T10b — a transform
 * merged into T10 several commits earlier and non-existent since. They were
 * correctly formatted, internally consistent, and describing nothing.
 *
 * READ-ONLY. This reports; it removes nothing. A removal you cannot show the
 * subject is absent for is worse than keeping stale evidence.
 *
 * TWO DIRECTIONS, and the second is the more dangerous one:
 *   FORWARD  evidence naming a subject -> does that subject still exist?
 *   INVERSE  a subject the ledger implies has evidence -> does any exist?
 *
 * PREDICATE, stated so the counts can be re-derived (R0.8):
 *   "evidence" = a git-TRACKED file under evidence/ or qa/ whose content
 *   records a verdict, a count or a pass/fail. Untracked scratch is excluded
 *   by construction — that is the evidence/ versus work/ distinction.
 *   "subject" = a transform id, a gate script path, or a site route named
 *   inside such a file.
 */
import fs from 'node:fs'; import path from 'node:path';
import { execFileSync } from 'node:child_process';

const REPOS = [
  { name: 'Lessons', root: '/home/user/Lessons' },
  { name: 'mattroper1977.github.io', root: '/workspace/mattroper1977.github.io' },
  { name: 'Matt-s-Apps-', root: '/workspace/matt-s-apps-' },
];
const rows = [];
const row = (dir, repo, subject, where, verdict, detail) =>
  rows.push({ dir, repo, subject, where, verdict, detail });

const tracked = root => {
  try { return execFileSync('git', ['-C', root, 'ls-files'], { encoding: 'utf8' }).split('\n').filter(Boolean); }
  catch (e) { return []; }
};

/* ---------------- FORWARD: evidence -> does its subject exist? ------------- */
for (const { name, root } of REPOS) {
  const files = tracked(root).filter(f => /(^|\/)(evidence|qa)\//.test(f) && /\.(out|json|txt|md|log)$/.test(f));
  if (!files.length) { row('forward', name, '—', '—', 'NO EVIDENCE FILES', 'no tracked file under evidence/ or qa/'); continue; }

  for (const f of files) {
    const abs = path.join(root, f);
    let text; try { text = fs.readFileSync(abs, 'utf8'); } catch (e) { continue; }

    /* -- transform ids. Their existence is decided by the sibling build.mjs,
          which is the only place a transform can be declared. */
    const dir = path.dirname(abs);
    const build = [path.join(dir, '..', 'build.mjs'), path.join(dir, 'build.mjs')].find(p => fs.existsSync(p));
    if (build) {
      const declared = new Set([...fs.readFileSync(build, 'utf8').matchAll(/swap\('([A-Za-z0-9]+)'/g)].map(m => m[1]));
      /* MATCH THE CLAIM, NOT THE SHAPE. The first cut matched any id shaped like
         a transform and flagged four rows as stale: T10a and T10b, which are
         CONTROL ids in the controls table, and X0 and X1c, which are row ids in
         the split-transport report. All four describe subjects that exist. A
         sweep built to catch stale evidence was one step from deleting live
         evidence, because it matched an identifier's shape rather than the claim
         being made about it.
         Only a removal-matrix row asserts "this TRANSFORM is watched", and those
         lines carry the verdict word. That is the claim; nothing else is one. */
      const named = new Set([...text.matchAll(/^\s{2,}([TXY]\d+[a-z]?)\s+(?:watched|LOAD-BEARING|UNWATCHED|DROPPED)/gm)].map(m => m[1]));
      for (const id of named) {
        row('forward', name, id, f,
          declared.has(id) ? 'SUBJECT EXISTS' : 'STALE — SUBJECT ABSENT',
          declared.has(id) ? `declared in ${path.relative(root, build)}`
                           : `no swap('${id}' in ${path.relative(root, build)} — this row records a verdict on a transform that no longer exists`);
      }
      if (!named.size) row('forward', name, '(no transform verdicts)', f, 'NOT APPLICABLE',
        'this file contains no removal-matrix row, so it asserts nothing about any transform. ' +
        'Control ids and report row ids share the shape and are NOT claims about transforms.');
    }

    /* -- gate scripts named inside the evidence */
    for (const m of new Set([...text.matchAll(/tools\/[A-Za-z0-9_\/-]+\.(?:mjs|py|sh)/g)].map(x => x[0]))) {
      row('forward', name, m, f,
        fs.existsSync(path.join(root, m)) ? 'SUBJECT EXISTS' : 'STALE — SUBJECT ABSENT',
        fs.existsSync(path.join(root, m)) ? 'file present' : 'named as a gate, no such file');
    }

    /* -- site routes named inside the evidence */
    for (const m of new Set([...text.matchAll(/"\/([a-z0-9-]{3,})\/"/g)].map(x => x[1]))) {
      const p = path.join(root, m, 'index.html');
      row('forward', name, `/${m}/`, f,
        fs.existsSync(p) ? 'SUBJECT EXISTS' : 'STALE — SUBJECT ABSENT',
        fs.existsSync(p) ? 'route has an index.html' : 'route named, no index.html at that path');
    }
  }
}

/* ---------------- INVERSE: a subject with no evidence --------------------- */
/* hud-coverage.json's scriptLine is the standing candidate: a canonical string
   with no consumer, against N hand-maintained copies of that literal. */
{
  const root = '/workspace/mattroper1977.github.io';
  const covPath = path.join(root, 'data', 'hud-coverage.json');
  if (!fs.existsSync(covPath)) {
    row('inverse', 'mattroper1977.github.io', 'data/hud-coverage.json', '—', 'SUBJECT ABSENT', 'cannot assess');
  } else {
    const cov = JSON.parse(fs.readFileSync(covPath, 'utf8'));
    const canonical = cov.scriptLine;

    /* who reads it? */
    let consumers = [];
    try {
      consumers = execFileSync('grep', ['-rl', '--include=*.py', '--include=*.mjs', '--include=*.js',
        '--include=*.sh', '--include=*.yml', 'scriptLine', root], { encoding: 'utf8' }).split('\n').filter(Boolean);
    } catch (e) { consumers = []; }
    row('inverse', 'mattroper1977.github.io', 'hud-coverage.json .scriptLine', 'data/hud-coverage.json',
      consumers.length ? 'HAS A CONSUMER' : 'NO CONSUMER — DECORATION',
      consumers.length ? consumers.map(c => path.relative(root, c)).join(', ')
        : `the canonical string ${JSON.stringify(canonical)} is read by no code in this repo`);

    /* and what would the assertion have found, had it existed? Derive the
       routes that DO carry a hud script, and compare each literal. */
    const idx = JSON.parse(fs.readFileSync(path.join(root, 'data', 'mbm-search-index.json'), 'utf8'));
    const ROOT_ROUTE = /^\/[a-z0-9-]+\/$/;
    const routes = [...new Set(idx.entries.filter(e => e.category === 'game' && ROOT_ROUTE.test(e.route || ''))
      .map(e => e.route))].sort();
    const TAG = /<script\b[^>]*\bsrc="\/hud\.js"[^>]*><\/script>/;
    let carry = 0, divergent = [];
    for (const r of routes) {
      const p = path.join(root, r.replace(/^\/|\/$/g, ''), 'index.html');
      if (!fs.existsSync(p)) continue;
      const m = fs.readFileSync(p, 'utf8').match(TAG);
      if (!m) continue;
      carry++;
      if (m[0] !== canonical) divergent.push(`${r} has ${JSON.stringify(m[0])}`);
    }
    row('inverse', 'mattroper1977.github.io', 'the assertion that does not exist', 'derived here',
      divergent.length === 0 ? 'WOULD PASS TODAY' : 'WOULD ALREADY BE RED',
      `${carry} of ${routes.length} root game routes carry a hud script tag; ` +
      (divergent.length ? `${divergent.length} diverge from the canonical string: ${divergent.join(' · ')}`
                        : `all ${carry} are byte-identical to .scriptLine. Nothing enforces that, so it is true by hand and stays true by luck.`));
  }
}

/* ---------------- the .gitignore shape, every repo ------------------------ */
for (const { name, root } of REPOS) {
  const transient = ['audit-output', 'work', 'drop_T1', 'staging'];
  const found = transient.filter(d => fs.existsSync(path.join(root, d)));
  const ignoredTop = fs.existsSync(path.join(root, '.gitignore'))
    ? fs.readFileSync(path.join(root, '.gitignore'), 'utf8') : '';
  const trackedTransient = tracked(root).filter(f => /^(audit-output|.*\/work)\//.test(f));
  row('gitignore', name, transient.join('|'), '.gitignore',
    trackedTransient.length === 0 ? 'NO TRANSIENT TRACKED' : 'TRANSIENT STILL TRACKED',
    `present on disk: [${found}] · tracked transient files: ${trackedTransient.length}` +
    (trackedTransient.length ? ` — ${trackedTransient.slice(0, 4).join(', ')}` : '') +
    ` · top-level .gitignore mentions audit-output: ${/audit-output/.test(ignoredTop)}`);
}

/* ---------------------------------------------------------------- report */
const W = [9, 24, 40, 34];
console.log(`${'direction'.padEnd(W[0])} ${'repo'.padEnd(W[1])} ${'subject'.padEnd(W[2])} verdict`);
console.log('-'.repeat(110));
for (const r of rows) {
  console.log(`${r.dir.padEnd(W[0])} ${r.repo.padEnd(W[1])} ${String(r.subject).slice(0, 40).padEnd(W[2])} ${r.verdict}`);
  console.log(`${' '.repeat(W[0] + 1)}in ${r.where} — ${r.detail}`);
}
const stale = rows.filter(r => /^STALE/.test(r.verdict));
const decor = rows.filter(r => r.verdict === 'NO CONSUMER — DECORATION');
const dirty = rows.filter(r => r.verdict === 'TRANSIENT STILL TRACKED');
console.log(`\nFORWARD  ${stale.length} stale evidence row(s) — evidence naming a subject that no longer exists`);
console.log(`INVERSE  ${decor.length} declaration(s) with no consumer`);
console.log(`IGNORE   ${dirty.length} repo(s) still tracking transient output`);
console.log(`\nThis sweep REMOVES NOTHING. Each row above names the file and the subject so a`);
console.log(`removal can be justified individually — removing real evidence is worse than`);
console.log(`keeping stale evidence.`);
process.exit(stale.length || decor.length || dirty.length ? 1 : 0);
