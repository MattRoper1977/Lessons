/* THE ZERO-CHECK CENSUS.
 *
 * PR #120 ran ZERO checks, from two causes stacked: it was conflicted against
 * main, so GitHub could not build a merge ref and nothing could fire however
 * its filters were written; and underneath that, no `paths:` filter on any of
 * ten workflows matched a single file it touched. Both were fixed on that PR.
 * Neither fix generalises, and a green tick on a PR nobody checked looks
 * exactly like a green tick on a PR that passed.
 *
 * So: for every open pull request across the estate, report mergeable_state,
 * the number of check runs on its HEAD SHA, and which workflows ran. An open
 * non-draft PR with zero check runs is a finding, whatever its state, and
 * --gate turns that into a red.
 *
 * The cause is reported per PR, because the four causes need different repairs:
 *   conflicted        rebase or merge the base in; no filter can save it
 *   filter miss       the workflows exist and none matched the paths touched
 *   draft             expected; drafts are excluded from --gate, and counted
 *   no applicable     the repo has no workflow that could run on this PR
 *
 * Needs a token with read access to the three repositories: GITHUB_TOKEN in CI.
 * Without egress it exits 2 rather than reporting an empty census as clean.
 *
 *   node tools/pr_check_census.mjs            report
 *   node tools/pr_check_census.mjs --gate     exit 1 if any open non-draft PR has 0 checks
 */
const REPOS = (process.env.CENSUS_REPOS ||
  'MattRoper1977/Lessons,MattRoper1977/mattroper1977.github.io,MattRoper1977/Matt-s-Apps-').split(',');
const GATE = process.argv.includes('--gate');
/* A gate that is red on every run is not a gate - it is deleted within the week.
   The twelve PRs measured on 2026-08-16 are DECLARED in a baseline file, each an
   open finding in the ledger rather than an exemption, and the gate's job is to
   stop the thirteenth. The baseline is held to being current in both directions:
   an entry that has since acquired checks reds the run too, because a baseline
   nobody prunes is stale evidence with a filename. */
const BASELINE = (() => {
  const i = process.argv.indexOf('--baseline');
  return i >= 0 ? process.argv[i + 1] : null;
})();
const TOKEN = process.env.GITHUB_TOKEN || process.env.GH_TOKEN || '';

const api = async p => {
  const r = await fetch(`https://api.github.com${p}`, {
    headers: {
      Accept: 'application/vnd.github+json',
      ...(TOKEN ? { Authorization: `Bearer ${TOKEN}` } : {}),
      'User-Agent': 'mbm-pr-check-census',
    },
  });
  if (!r.ok) throw new Error(`GET ${p} -> ${r.status}`);
  return r.json();
};

/* The split, as one function, so the report and the control cannot drift apart.
   Returns the three populations by NAME rather than by subtraction — the defect
   this replaces was built entirely out of one subtraction. */
function splitZeroes(all, declaredKeys) {
  const declared = new Set(declaredKeys || []);
  const key = r => `${r.repo}#${r.number}`;
  const zero = all.filter(r => r.zero);
  const draft = zero.filter(r => r.draft);
  const nonDraft = zero.filter(r => !r.draft);
  return { zero, draft, nonDraft,
           declaredNonDraft: nonDraft.filter(r => declared.has(key(r))),
           undeclared: nonDraft.filter(r => !declared.has(key(r))) };
}

/* R0.15 — the control for the report that was wrong, and it runs with no token
   and no network, so it fires on every event. The fixture is the exact census
   that misreported: 3 drafts and 9 declared non-drafts, all zero-check. */
if (process.argv.includes('--self-test')) {
  let bad = 0;
  const say = (ok, label, detail) => { console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${label}${detail ? ` — ${detail}` : ''}`); if (!ok) bad++; };
  const mk = (repo, number, draft) => ({ repo, number, draft, zero: true });
  const fixture = [
    ...[1, 2, 3].map(n => mk('Lessons', n, true)),
    ...[9, 17, 35, 43, 116, 117, 118].map(n => mk('Lessons', n, false)),
    mk('Matt-s-Apps-', 2, false), mk('mattroper1977.github.io', 25, false),
    { repo: 'Lessons', number: 999, draft: false, zero: false },
  ];
  const declared = ['Lessons#9', 'Lessons#17', 'Lessons#35', 'Lessons#43', 'Lessons#116',
                    'Lessons#117', 'Lessons#118', 'Matt-s-Apps-#2', 'mattroper1977.github.io#25'];
  const s = splitZeroes(fixture, declared);

  say(s.zero.length === 12, 'twelve zero-check rows in the fixture', `${s.zero.length}`);
  say(s.draft.length === 3, 'exactly three are drafts — draftness is read, not inferred', `${s.draft.length}`);
  say(s.nonDraft.length === 9, 'exactly nine are NOT drafts', `${s.nonDraft.length}`);
  say(s.declaredNonDraft.length === 9 && s.undeclared.length === 0,
      'all nine non-drafts are baseline-declared, and none is undeclared',
      `declared ${s.declaredNonDraft.length}, undeclared ${s.undeclared.length}`);
  /* THE REGRESSION ITSELF. The old line read `zeroes - gated` for the draft
     count, where gated had already had the baseline subtracted. Recompute that
     and require it to differ from the truth, or this control is decoration. */
  const oldDraftCount = s.zero.length - s.undeclared.length;
  say(oldDraftCount === 12 && s.draft.length === 3,
      'the retired arithmetic is reproduced here and disagrees with the rows',
      `retired formula says ${oldDraftCount} drafts, the rows say ${s.draft.length}`);
  /* And the gate's own behaviour must be unchanged by the reporting fix. */
  say(s.undeclared.length === 0, 'an all-declared census still gates green');
  const withNew = splitZeroes([...fixture, mk('Lessons', 124, false)], declared);
  say(withNew.undeclared.length === 1, 'a thirteenth, undeclared zero-check PR is still caught',
      withNew.undeclared.map(r => `${r.repo}#${r.number}`).join(', '));

  console.log(`\n[SELF-TEST] ${bad === 0 ? 'PASS' : 'FAIL'} — ${bad} check(s) failed`);
  process.exit(bad === 0 ? 0 : 1);
}

const rows = [];
let unreachable = null;

for (const repo of REPOS) {
  let prs;
  try { prs = await api(`/repos/${repo}/pulls?state=open&per_page=100`); }
  catch (e) { unreachable = `${repo}: ${e.message}`; break; }

  for (const pr of prs) {
    let checks = { total_count: 0, check_runs: [] }, workflows = [];
    try {
      checks = await api(`/repos/${repo}/commits/${pr.head.sha}/check-runs?per_page=100`);
      workflows = [...new Set(checks.check_runs.map(c => c.name))];
    } catch { /* leave at zero and let the cause line say why */ }

    /* mergeable_state is only populated on the single-PR endpoint. */
    let state = '?';
    try { state = (await api(`/repos/${repo}/pulls/${pr.number}`)).mergeable_state || '?'; } catch {}

    const zero = checks.total_count === 0;
    const cause = !zero ? '—'
      : pr.draft ? 'draft'
      : state === 'dirty' ? 'conflicted — no merge ref, so no workflow could fire'
      : 'filter miss or no applicable workflow — the merge ref exists and nothing ran';

    rows.push({ repo: repo.split('/')[1], number: pr.number, title: pr.title,
                draft: pr.draft, state, checks: checks.total_count, workflows, zero, cause });
  }
}

if (unreachable) {
  console.log(`[INCONCLUSIVE] the GitHub API is unreachable from here — ${unreachable}`);
  console.log('An empty census is not a clean census. Run this in CI.');
  process.exit(2);
}
if (!rows.length) {
  console.log('[INCONCLUSIVE] no open pull requests were returned at all, across every repo.');
  console.log('That is more likely a token scope than an empty estate.');
  process.exit(2);
}

console.log(`${'repo'.padEnd(24)} ${'PR'.padEnd(5)} ${'mergeable'.padEnd(11)} ${'checks'.padEnd(7)} workflows`);
console.log('-'.repeat(118));
for (const r of rows.sort((a, b) => a.repo.localeCompare(b.repo) || a.number - b.number)) {
  console.log(`${r.repo.padEnd(24)} #${String(r.number).padEnd(4)} ${r.state.padEnd(11)} ` +
              `${String(r.checks).padEnd(7)} ${r.workflows.slice(0, 3).join(', ') || '—'}` +
              `${r.workflows.length > 3 ? ` (+${r.workflows.length - 3})` : ''}`);
  console.log(`${' '.repeat(25)}${r.draft ? '[draft] ' : ''}${r.title.slice(0, 78)}`);
  if (r.zero) console.log(`${' '.repeat(25)}ZERO CHECK RUNS — ${r.cause}`);
}

/* THE SPLIT IS COMPUTED FROM THE ROWS, NOT FROM WHAT SURVIVED THE GATE.
   This line reported "12 draft, 0 not" on 2026-08-17 over a census whose own
   rows showed at most three drafts. The cause was arithmetic, not counting: the
   baseline subtraction below reassigned `gated`, and the label was derived as
   `zeroes - gated`, so every baseline-declared NON-draft was silently added to
   the draft count. Nine PRs recorded as known findings were reported as an
   expected state instead. The gate itself was right throughout — it is the
   sentence describing it that was false, which is the R0.12 species and the
   harder one to notice.

   Draftness is a property of a PR. It is read from the PR, once, here. */
let declaredKeys = null, stale = [];
if (BASELINE) {
  const fs = await import('node:fs');
  let known;
  try { known = JSON.parse(fs.readFileSync(BASELINE, 'utf8')).known || []; }
  catch (e) {
    console.log(`[INCONCLUSIVE] the baseline at ${BASELINE} could not be read: ${e.message}`);
    console.log('Running without one would silently widen the gate to "anything goes".');
    process.exit(2);
  }
  declaredKeys = known.map(k => `${k.repo.split('/').pop()}#${k.pr}`);
  stale = known.filter(k => {
    const row = rows.find(r => `${r.repo}#${r.number}` === `${k.repo.split('/').pop()}#${k.pr}`);
    return row && !row.zero;   // listed as zero-check, now has checks
  });
}
const split = splitZeroes(rows, declaredKeys);
const zeroes = split.zero, drafts = split.draft, nonDrafts = split.nonDraft;
const gated = BASELINE ? split.undeclared : split.nonDraft;
console.log(`\n${rows.length} open PR(s) · ${zeroes.length} with zero check runs ` +
            `(${drafts.length} draft, ${nonDrafts.length} not)`);
if (BASELINE)
  console.log(`  of the ${nonDrafts.length} non-draft: ${nonDrafts.length - gated.length} declared in the baseline ` +
              `as open findings, ${gated.length} undeclared. A declared finding is recorded, not excused, and ` +
              `it is never a draft.`);
if (gated.length) {
  console.log('\nEvery line below is a PR whose green tick means nothing was asked:');
  for (const r of gated) console.log(`  ${r.repo} #${r.number} — ${r.cause}`);
}
if (BASELINE) {
  console.log(`\nBASELINE  ${gated.length} zero-check PR(s) NOT declared in ${BASELINE} · ` +
              `${stale.length} declared entr(ies) that now have checks and should be pruned`);
  for (const s of stale) console.log(`  prune: ${s.repo} #${s.pr} — it has check runs now`);
}
if (GATE && (gated.length || stale.length)) process.exit(1);
process.exit(0);
