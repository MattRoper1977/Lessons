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

const zeroes = rows.filter(r => r.zero);
let gated = zeroes.filter(r => !r.draft);
let stale = [];
if (BASELINE) {
  const fs = await import('node:fs');
  let known;
  try { known = JSON.parse(fs.readFileSync(BASELINE, 'utf8')).known || []; }
  catch (e) {
    console.log(`[INCONCLUSIVE] the baseline at ${BASELINE} could not be read: ${e.message}`);
    console.log('Running without one would silently widen the gate to "anything goes".');
    process.exit(2);
  }
  const key = r => `${r.repo}#${r.number}`;
  const declared = new Set(known.map(k => `${k.repo.split('/').pop()}#${k.pr}`));
  stale = known.filter(k => {
    const row = rows.find(r => key(r) === `${k.repo.split('/').pop()}#${k.pr}`);
    return row && !row.zero;   // listed as zero-check, now has checks
  });
  gated = gated.filter(r => !declared.has(key(r)));
}
console.log(`\n${rows.length} open PR(s) · ${zeroes.length} with zero check runs ` +
            `(${zeroes.length - gated.length} draft, ${gated.length} not)`);
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
