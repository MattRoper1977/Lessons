/* NOTHING WAS WATCHING MAIN.  R0.22.
 *
 * Two push-to-main runs went red in this arc — 32017557268 at 7efbf22 and
 * 32018424063 at b6f92ca, both the same defect — and the only reason either is
 * known is that someone went and looked. A red that nobody is told about is a
 * red nobody has. This is the mechanism.
 *
 * THREE CATEGORIES, NOT TWO
 * A run is PASS, FAIL, or NO VERDICT. The third exists because of the
 * inline-exit job this arc: `cancel-in-progress` killed it, the surrounding
 * jobs were green, and those greens looked exactly like coverage. Cancelled,
 * skipped, timed out, stale, action_required — none of them is a result, and
 * NO VERDICT never counts as covered. The reader should not have to know that.
 *
 * A MISSING RUN AND A FAILED RUN ARE DIFFERENT FINDINGS
 * A workflow that never started produces no red anywhere. It is derived from
 * .github/workflows/ and reported as NEVER STARTED, separately, because the
 * repair is different: a failing gate needs a fix, a silent one needs a trigger.
 *
 * R0.23 — every pattern-driven step names the tree it is scoped to and prints
 * what it matched BEFORE acting on it. Provenance: a filtered grep that
 * under-reported a removal census by one; `git tag -l` run in the wrong repo
 * and reported absent; `pkill -f "sleep 180"` matching its own wrapper.
 *
 *   node tools/watch_main_runs.mjs               report and gate
 *   node tools/watch_main_runs.mjs --self-test   the controls, no network
 *   node tools/watch_main_runs.mjs --verify-trigger-list   the workflow_run list
 *                                                 matches the derived set
 *   node tools/watch_main_runs.mjs --window N    how many recent runs to read
 *
 * Exit 0 every derived workflow has a PASS on the default branch · 1 a FAIL, a
 * NO VERDICT, or a workflow that never started · 2 INCONCLUSIVE (no token, no
 * egress, or an empty run list — an empty list must never read as nothing wrong).
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ARGS = process.argv.slice(2);
const SELFTEST = ARGS.includes('--self-test');
const arg = (n, d) => { const i = ARGS.indexOf(n); return i >= 0 ? ARGS[i + 1] : d; };
const REPO = process.env.WATCH_REPO || 'MattRoper1977/Lessons';
const BRANCH = process.env.WATCH_BRANCH || 'main';
const WINDOW = Number(arg('--window', process.env.WATCH_WINDOW || 40));
const TOKEN = process.env.GITHUB_TOKEN || process.env.GH_TOKEN || '';
const WORKFLOW_DIR = path.join(HERE, '.github/workflows');

class Inconclusive extends Error {}

/* Anything that is not a completed success and not a completed failure. Listed
   by name rather than caught by an `else`, so a conclusion GitHub adds later
   shows up as unknown instead of being silently sorted into a bucket. */
const NO_VERDICT = new Set(['cancelled', 'skipped', 'timed_out', 'stale', 'action_required', 'neutral', null]);

/* A WATCH CANNOT BE ITS OWN WITNESS.
   Its own run is necessarily still in progress while it is asking, so it would
   classify itself as NO VERDICT and go red on every single execution — a gate
   that is always red is deleted within the week, which is the failure mode this
   file is supposed to prevent rather than demonstrate. It is excluded by path,
   and the exclusion is PRINTED rather than silent (R0.23): an exclusion nobody
   can see is indistinguishable from a blind spot. */
const SELF = process.env.WATCH_SELF_PATH || '.github/workflows/watch-main.yml';

/* ------------------------------------------------- the derived workflow set */
/* R0.23: the scope is named and the match set printed by the caller. */
function discoverWorkflows(dir = WORKFLOW_DIR) {
  if (!fs.existsSync(dir)) throw new Inconclusive(`no workflow directory at ${dir} — the subject set cannot be derived`);
  const files = fs.readdirSync(dir).filter(f => /\.ya?ml$/.test(f)).sort();
  if (!files.length) throw new Inconclusive(`${dir} contains no .yml/.yaml — an empty subject set asserts nothing`);
  const all = files.map(f => {
    const src = fs.readFileSync(path.join(dir, f), 'utf8');
    const m = src.match(/^name:\s*(.+?)\s*$/m);
    /* Which triggers it has, and whether any of them fires without a person.
       A workflow_dispatch-only file CANNOT have an automatic run, so reporting
       it as "never started" is wrong by construction rather than a finding. */
    const on = (src.match(/^on:[\s\S]*?(?=^\w|^$)/m) || [''])[0];
    const auto = /^\s*(push|pull_request|schedule|workflow_run):/m.test(on);
    const triggers = ['push', 'pull_request', 'schedule', 'workflow_run', 'workflow_dispatch']
      .filter(t => new RegExp(`^\\s*${t}:`, 'm').test(on));
    const pathFiltered = /^\s*paths:/m.test(on);
    return { file: f, path: `.github/workflows/${f}`, auto, triggers, pathFiltered,
             name: m ? m[1].replace(/^['"]|['"]$/g, '') : f };
  });
  return { all, judged: all.filter(w => w.path !== SELF), excluded: all.filter(w => w.path === SELF) };
}

/* ------------------------------------- the trigger list cannot drift silently */
/* `workflow_run` has no wildcard — GitHub requires the watched workflows to be
   named. A hand-maintained list is precisely how PR #114 came to run zero
   checks, so naming them is acceptable only with this check attached: the list
   in watch-main.yml must equal the set derived from .github/workflows/, minus
   the watch itself. Add a workflow and forget the list, and this goes red. */
function verifyTriggerList() {
  const selfFile = path.join(HERE, SELF);
  if (!fs.existsSync(selfFile)) throw new Inconclusive(`the watch workflow is not at ${SELF} — the trigger list cannot be read`);
  const src = fs.readFileSync(selfFile, 'utf8');
  const block = src.match(/workflows:\s*\n((?:\s*-\s*.+\n)+)/);
  if (!block) throw new Inconclusive('watch-main.yml has no workflow_run `workflows:` list to check');
  const listed = [...block[1].matchAll(/^\s*-\s*(?:"([^"]*)"|'([^']*)'|(.+?))\s*$/gm)]
    .map(m => (m[1] ?? m[2] ?? m[3]).trim()).filter(Boolean);

  const { judged, excluded, all } = discoverWorkflows();
  const derived = judged.map(w => w.name);

  console.log('trigger-list control');
  console.log(`  scope: ${WORKFLOW_DIR} · ${all.length} workflow file(s), ${excluded.length} excluded as self`);
  console.log(`  listed in ${SELF}: ${listed.length}`);
  for (const n of listed) console.log(`    listed   ${n}`);
  for (const n of derived) console.log(`    derived  ${n}`);

  const missing = derived.filter(n => !listed.includes(n));
  const extra = listed.filter(n => !derived.includes(n));
  for (const n of missing) console.log(`  [FAIL] derived but NOT listed — this workflow's completion would never wake the watch: ${n}`);
  for (const n of extra) console.log(`  [FAIL] listed but not derived — renamed or deleted, so this entry watches nothing: ${n}`);
  if (!missing.length && !extra.length)
    console.log(`\n  PASS  the trigger list is exactly the derived set (${derived.length} workflow(s)).`);
  return (missing.length || extra.length) ? 1 : 0;
}

/* ------------------------------------------------------- the classification */
function classify(runs) {
  const pass = [], fail = [], noVerdict = [];
  for (const r of runs) {
    if (r.status !== 'completed') { noVerdict.push({ ...r, why: `status=${r.status}, never completed` }); continue; }
    if (r.conclusion === 'success') pass.push(r);
    else if (r.conclusion === 'failure') fail.push(r);
    else noVerdict.push({ ...r, why: `conclusion=${r.conclusion === null ? 'null' : r.conclusion}` });
  }
  return { pass, fail, noVerdict };
}

/* A workflow present in the tree with no run in the window. Keyed on the
   workflow FILE PATH, not its display name: a rename of `name:` would otherwise
   read as a workflow that stopped running. */
function neverStarted(workflows, runs) {
  const seen = new Set(runs.map(r => r.path));
  return workflows.filter(w => !seen.has(w.path));
}

/* IS THE CURRENT HEAD TESTED AT ALL?
   The watch judges the latest run PER WORKFLOW, which answers "is each gate
   passing" and NOT "was this commit checked". Those come apart completely when a
   push produces no runs: the newest runs still belong to the previous commit,
   every workflow reports PASS, and main's actual head was never tested.

   That is not hypothetical. It happened to the commit that landed this file:
   the squash message DESCRIBED the ledger-append guard and included the literal
   CI-skip token while doing so, GitHub honoured it, and the push to main ran
   nothing at all — including this watch, which is why the schedule leg exists.
   A skip token silences every event-driven trigger, so only the cron can catch
   it. A description of a mechanism invoked the mechanism. */
function headCoverage(headSha, runs) {
  if (!headSha) return null;
  const on = runs.filter(r => r.sha && headSha.startsWith(r.sha));
  return { headSha: headSha.slice(0, 7), tested: on.length > 0, runs: on.length };
}

/* The verdict. An empty run list is INCONCLUSIVE and never green — this whole
   file exists because silence read as health. */
function verdictFor(runs, workflows, cls, missing, head) {
  if (!runs.length)
    throw new Inconclusive(`no runs returned for ${REPO}@${BRANCH} — a watch that sees nothing must not report nothing wrong`);
  if (!workflows.length)
    throw new Inconclusive('no workflows derived — nothing could be judged missing');
  const headUntested = head && !head.tested;
  /* DORMANCY IS NOT A FAILURE, and treating it as one made this gate red on its
     very first execution with nothing wrong: 6 PASS, 0 FAIL, 0 NO VERDICT, and
     six workflows reported "never started" that were three workflow_dispatch-only
     files and three path-filtered ones the commit did not touch. It then wrote a
     false "main was red" line into the ledger and pushed it.

     Deciding whether a path-filtered workflow SHOULD have run on a given commit
     means matching its filters against that commit's changed files. This tool
     does not do that, so it does not pronounce on it — the absence is reported,
     with each workflow's triggers named, and it does not colour the verdict.
     A stated limitation beats a confident wrong answer. */
  return (cls.fail.length || cls.noVerdict.length || headUntested) ? 1 : 0;
}

/* ------------------------------------------------------------------- the API */
async function api(p) {
  if (!TOKEN) throw new Inconclusive('no GITHUB_TOKEN — the run list cannot be read, and an unread list is not an empty one');
  const r = await fetch(`https://api.github.com${p}`, {
    headers: { Accept: 'application/vnd.github+json', Authorization: `Bearer ${TOKEN}`,
               'User-Agent': 'mbm-watch-main' } });
  if (!r.ok) throw new Inconclusive(`GitHub API ${r.status} for ${p}`);
  return r.json();
}

/* Only the LATEST run per workflow is judged. An older red that a later green
   superseded is history, not a live finding. */
function latestPerWorkflow(runs) {
  const byPath = new Map();
  for (const r of runs) if (!byPath.has(r.path)) byPath.set(r.path, r);   // API returns newest first
  return [...byPath.values()];
}

/* ------------------------------------------------------------------ soak */
/* A SAMPLE OF TWO IS NOT A TRACK RECORD.
   This watch has produced exactly two live verdicts: one false red and one true
   green. Until it has run clean for a declared number of consecutive executions
   it is on probation, and the countdown is printed in every run rather than kept
   in someone's head. Derived from the watch's own run history, not stored. */
const SOAK_TARGET = Number(process.env.WATCH_SOAK || 10);

async function soak() {
  try {
    const d = await api(`/repos/${REPO}/actions/workflows/${encodeURIComponent(path.basename(SELF))}/runs?per_page=40`);
    const runs = (d.workflow_runs || []).filter(r => r.status === 'completed');
    let greens = 0;
    for (const r of runs) { if (r.conclusion === 'success') greens++; else break; }
    return { greens, target: SOAK_TARGET, total: runs.length };
  } catch (e) { return { greens: null, target: SOAK_TARGET, why: e.message }; }
}

/* --------------------------------------------------------------- self-test */
function selfTest() {
  let bad = 0;
  const say = (ok, label, detail) => { console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${label}${detail ? ` — ${detail}` : ''}`); if (!ok) bad++; };
  console.log('CONTROLS — no token, no network, so these fire on every event\n');

  const wf = [
    { file: 'a.yml', path: '.github/workflows/a.yml', name: 'A' },
    { file: 'b.yml', path: '.github/workflows/b.yml', name: 'B' },
    { file: 'never.yml', path: '.github/workflows/never.yml', name: 'Never Started' },
  ];
  const runs = [
    { id: 1, name: 'A', path: '.github/workflows/a.yml', status: 'completed', conclusion: 'success' },
    { id: 2, name: 'B', path: '.github/workflows/b.yml', status: 'completed', conclusion: 'failure' },
  ];

  /* (a) a synthetic failed run must be DETECTED AND NAMED. Named matters: a
         count of failures nobody can act on is the reporting defect this estate
         has already recorded twice. */
  {
    const c = classify(runs);
    const named = c.fail.map(r => `${r.name} (run ${r.id})`);
    say(c.fail.length === 1 && named[0] === 'B (run 2)',
        '(a) a failed run is detected AND named', named.join(', ') || 'nothing named');
  }

  /* (b) an empty run list must exit 2, never green. */
  {
    let fired = false, why = '';
    try { verdictFor([], wf, classify([]), []); }
    catch (e) { fired = e instanceof Inconclusive; why = e.message; }
    say(fired, '(b) an empty run list is INCONCLUSIVE, never green', why.slice(0, 80));
  }

  /* (c) a cancelled run is NO VERDICT, not PASS. The inline-exit job that
         prompted this rule was cancelled by cancel-in-progress and its
         neighbours were green. */
  {
    const cancelled = [{ id: 3, name: 'C', path: '.github/workflows/c.yml', status: 'completed', conclusion: 'cancelled' }];
    const c = classify(cancelled);
    say(c.noVerdict.length === 1 && c.pass.length === 0 && c.fail.length === 0,
        '(c) a cancelled run reports NO VERDICT, and is not counted as covered',
        c.noVerdict.map(r => `${r.name}: ${r.why}`).join(', '));
  }

  /* (d) a workflow in the tree with no run at all is NEVER STARTED — a separate
         finding from a failure, because the repair is different. */
  {
    const missing = neverStarted(wf, runs);
    say(missing.length === 1 && missing[0].file === 'never.yml',
        '(d) a workflow present in the tree but absent from the run set is NEVER STARTED',
        missing.map(m => m.file).join(', ') || 'nothing reported missing');
  }

  /* And the composite: all three findings together must still gate red. */
  {
    const c = classify(runs);
    const code = verdictFor(runs, wf, c, neverStarted(wf, runs));
    say(code === 1, 'a run set carrying a failure exits 1', `exit ${code}`);
    const clean = [{ id: 9, name: 'A', path: '.github/workflows/a.yml', status: 'completed', conclusion: 'success' }];
    const okCode = verdictFor(clean, [wf[0]], classify(clean), neverStarted([wf[0]], clean));
    say(okCode === 0, 'and an all-green run set exits 0 — the gate is not stuck red', `exit ${okCode}`);
  }

  /* (e) the watch must exclude itself, or it reports NO VERDICT on its own
         in-progress run every time and is red forever. Derived from the real
         directory so a rename of the watch file is caught here. */
  {
    const d = discoverWorkflows();
    const selfSeen = d.all.some(w => w.path === SELF);
    say(selfSeen ? d.excluded.length === 1 && !d.judged.some(w => w.path === SELF) : true,
        '(e) the watch excludes itself from what it judges',
        selfSeen ? `excluded ${d.excluded.map(w => w.file).join(', ')}, judging ${d.judged.length}`
                 : `${SELF} is not present yet — nothing to exclude, ${d.judged.length} judged`);
  }

  /* (g) DORMANCY ALONE MUST NOT RED. This is the regression guard for the
         watch's first live execution, which went red with 6 PASS, 0 FAIL and
         0 NO VERDICT because six workflows had no run in the window — three
         dispatch-only, three path-filtered on files the commit never touched —
         and then wrote a false "main was red" line into the ledger and pushed it. */
  {
    const wfd = [
      { file: 'a.yml', path: '.github/workflows/a.yml', name: 'A', auto: true, triggers: ['push'], pathFiltered: false },
      { file: 'manual.yml', path: '.github/workflows/manual.yml', name: 'M', auto: false, triggers: ['workflow_dispatch'], pathFiltered: false },
      { file: 'paths.yml', path: '.github/workflows/paths.yml', name: 'P', auto: true, triggers: ['pull_request'], pathFiltered: true },
    ];
    const only = [{ id: 1, name: 'A', path: '.github/workflows/a.yml', status: 'completed', conclusion: 'success', sha: 'ccccccc' }];
    const c = classify(only);
    const miss = neverStarted(wfd, only);
    const head = headCoverage('cccccccdeadbeef', only);
    const code = verdictFor(only, wfd, c, miss, head);
    say(miss.length === 2, 'precondition: two workflows have no run in the window', miss.map(w => w.file).join(', '));
    say(code === 0, '(g) dormant and dispatch-only workflows alone do NOT red the verdict', `exit ${code}`);
    say(miss.filter(w => !w.auto).length === 1,
        '...and a dispatch-only workflow is distinguished from a dormant one', 'manual.yml is dispatch-only');
  }

  /* (f) a head with no runs of its own must be reported UNTESTED and must red
         the verdict, even when every workflow's latest run is green. This is the
         case that actually occurred: the commit landing this file carried a
         CI-skip token in its squash message, nothing ran, and every gate would
         still have reported PASS on the previous commit. */
  {
    const green = [
      { id: 1, name: 'A', path: '.github/workflows/a.yml', status: 'completed', conclusion: 'success', sha: 'aaaaaaa' },
      { id: 2, name: 'B', path: '.github/workflows/b.yml', status: 'completed', conclusion: 'success', sha: 'aaaaaaa' },
    ];
    const wf2 = [wf[0], wf[1]];
    const c = classify(green);
    say(c.fail.length === 0 && c.noVerdict.length === 0 && neverStarted(wf2, green).length === 0,
        'precondition: every workflow is green on the previous commit');

    const untested = headCoverage('bbbbbbbdeadbeef', green);
    say(untested && untested.tested === false,
        '(f) a head with no runs of its own is reported UNTESTED', `head ${untested.headSha}, ${untested.runs} run(s)`);
    const code = verdictFor(green, wf2, c, neverStarted(wf2, green), untested);
    say(code === 1, '...and it reds the verdict despite every gate passing', `exit ${code}`);

    const tested = headCoverage('aaaaaaadeadbeef', green);
    const okCode = verdictFor(green, wf2, c, neverStarted(wf2, green), tested);
    say(tested.tested === true && okCode === 0,
        '...while a head that WAS tested stays green — not stuck red', `head ${tested.headSha}, ${tested.runs} run(s), exit ${okCode}`);
  }

  console.log(`\n[SELF-TEST] ${bad === 0 ? 'PASS' : 'FAIL'} — ${bad} control(s) failed`);
  return bad === 0 ? 0 : 1;
}

/* ------------------------------------------------------------------- report */
async function main() {
  if (SELFTEST) return selfTest();
  if (ARGS.includes('--verify-trigger-list')) return verifyTriggerList();

  /* R0.23 — scope named and match set printed BEFORE anything is judged. */
  console.log(`watch — ${REPO} @ ${BRANCH}`);
  console.log(`  scope: ${WORKFLOW_DIR}`);
  const disc = discoverWorkflows();
  const workflows = disc.judged;
  console.log(`  predicate: every file matching /\\.ya?ml$/ directly in that directory — ${disc.all.length} matched, ` +
              `${disc.excluded.length} excluded as self, ${workflows.length} judged:`);
  for (const w of workflows) console.log(`    JUDGED    ${w.file.padEnd(38)} ${w.name}`);
  for (const w of disc.excluded)
    console.log(`    EXCLUDED  ${w.file.padEnd(38)} ${w.name} — this watch cannot witness itself; its own run is still in progress while it asks`);
  console.log(`  run window: the ${WINDOW} most recent ${BRANCH} runs, reduced to the LATEST per workflow`);
  console.log();

  const data = await api(`/repos/${REPO}/actions/runs?branch=${BRANCH}&per_page=${WINDOW}`);
  const all = (data.workflow_runs || []).map(r => ({
    id: r.id, name: r.name, path: r.path, status: r.status, conclusion: r.conclusion,
    sha: (r.head_sha || '').slice(0, 7), url: r.html_url, at: r.created_at }))
    .filter(r => r.path !== SELF);
  const runs = latestPerWorkflow(all);
  console.log(`  read ${all.length} run(s) after excluding self; ${runs.length} distinct workflow(s) have run\n`);

  const cls = classify(runs);
  const missing = neverStarted(workflows, runs);

  /* The head, and whether anything tested it. */
  let head = null;
  try {
    const ref = await api(`/repos/${REPO}/commits/${BRANCH}`);
    head = headCoverage(ref.sha, all);
    const msg = (ref.commit && ref.commit.message || '').split('\n')[0];
    if (head && !head.tested) {
      const skip = /\[(skip ci|ci skip|no ci|skip actions|actions skip)\]/i.exec(ref.commit && ref.commit.message || '');
      console.log(`  HEAD ${head.headSha} HAS NO RUNS AT ALL — this commit was never tested by anything.`);
      console.log(`    subject: ${msg.slice(0, 90)}`);
      if (skip) console.log(`    cause: its message carries ${skip[0]}, which silences every event-driven trigger. Only the schedule can catch this.`);
      else console.log(`    cause: not a CI-skip token — the push produced no run for another reason.`);
      console.log();
    }
  } catch (e) { console.log(`  head coverage UNKNOWN (${e.message})\n`); }

  console.log(`${'category'.padEnd(12)} ${'workflow'.padEnd(46)} detail`);
  console.log('-'.repeat(104));
  for (const r of cls.pass) console.log(`${'PASS'.padEnd(12)} ${String(r.name).slice(0, 46).padEnd(46)} ${r.sha} · run ${r.id}`);
  for (const r of cls.fail) console.log(`${'FAIL'.padEnd(12)} ${String(r.name).slice(0, 46).padEnd(46)} ${r.sha} · run ${r.id} · ${r.url}`);
  for (const r of cls.noVerdict) console.log(`${'NO VERDICT'.padEnd(12)} ${String(r.name).slice(0, 46).padEnd(46)} ${r.sha} · run ${r.id} · ${r.why}`);
  for (const w of missing) console.log(`${(w.auto ? 'DORMANT' : 'MANUAL').padEnd(12)} ${String(w.name).slice(0, 46).padEnd(46)} ` +
    `no run in the window · triggers: ${w.triggers.join(', ') || 'none parsed'}` +
    (w.pathFiltered ? ' · path-filtered' : '') +
    (w.auto ? '' : ' — dispatch-only, so it CANNOT have an automatic run'));

  const manual = missing.filter(w => !w.auto), dormant = missing.filter(w => w.auto);
  console.log(`\n${cls.pass.length} PASS · ${cls.fail.length} FAIL · ${cls.noVerdict.length} NO VERDICT · ` +
              `${dormant.length} dormant · ${manual.length} dispatch-only, of ${workflows.length} derived`);
  console.log('LIMITATION, STATED HERE AND NOT ONLY IN THE LEDGER: dormant and dispatch-only');
  console.log('workflows do NOT colour the verdict. Deciding whether a path-filtered workflow');
  console.log('SHOULD have run on this commit means matching its filters against the commit\'s');
  console.log('changed files. This tool does not do that, so a workflow that has silently');
  console.log('STOPPED running is NOT distinguishable here from one correctly dormant.');
  console.log('Reported, never pronounced on. UNDETERMINED is the honest word.');
  console.log(head ? (head.tested
    ? `head ${head.headSha}: tested by ${head.runs} run(s)`
    : `head ${head.headSha}: TESTED BY NOTHING — every gate above passed on an EARLIER commit`)
    : 'head coverage: unknown');
  console.log('NO VERDICT is not coverage. A cancelled or skipped run says nothing about the commit it was asked to judge.');

  const sk = await soak();
  if (sk.greens === null) console.log(`\nsoak: UNKNOWN (${sk.why})`);
  else if (sk.greens >= sk.target)
    console.log(`\nsoak: ${sk.greens}/${sk.target} consecutive green — probation served.`);
  else
    console.log(`\nsoak: ${sk.greens}/${sk.target} consecutive green — ${sk.target - sk.greens} to go. ` +
                `This watch has produced ${sk.total} live verdict(s) in total, one of which was a FALSE RED ` +
                `(run 32029976055). A sample this small is not a track record, and the write leg stays dry until it is.`);

  const code = verdictFor(runs, workflows, cls, missing, head);
  if (code === 0) console.log(`\nEvery derived workflow has a completed, successful latest run on ${BRANCH}.`);
  else {
    console.log(`\n[RED] ${cls.fail.length} failing · ${cls.noVerdict.length} without a verdict` +
      `${head && !head.tested ? ' · the head was tested by nothing' : ''}.`);
    console.log('This check fails so the failure is visible on the default branch rather than');
    console.log('waiting to be discovered by someone going and looking.');
  }
  return code;
}

main().then(c => process.exit(c),
  e => { if (e instanceof Inconclusive) { console.log(`[INCONCLUSIVE] ${e.message}`); process.exit(2); } console.error(e); process.exit(1); });
