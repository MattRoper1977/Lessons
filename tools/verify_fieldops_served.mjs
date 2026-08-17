/* MERGED IS NOT SERVED.  R0.4, applied to the FieldOps P2 placement.
 *
 * Two merges landed and nothing had confirmed the Pages build serves them. The
 * development container's proxy answers 403 on CONNECT to madebymatt.uk and to
 * github.io, so serving cannot be proven from there — and asking a human to tap
 * a URL is not a gate, because it does not run again next month. This runs in
 * CI, where egress works.
 *
 * WHY THIS TOOL AND NOT derive_live_routes.mjs
 * That instrument derives the route set from the canonical shelf and is correct
 * for what it covers: games the SITE serves. It classifies anything under
 * /Lessons/ as another estate and does not fetch it — deliberately, because
 * neither repository contains the other's files. The four labs are Lessons
 * files and the Studio is an Apps file, so they are invisible to it, and always
 * were. Extending it would mean teaching a site-repo tool to reach into two
 * other estates. The derivation belongs on this side instead.
 *
 * THE SOURCE OF TRUTH, AND WHY IT IS CANONICAL
 * tools/fieldops/build.mjs declares LABS and STUDIO. That is canonical in the
 * strong sense rather than by convention: the builder cannot emit a lab it does
 * not name, and assert_unchanged's U1 pins that dropping all transforms
 * reproduces release byte for byte — so the list is already load-bearing for
 * the build. No manifest anywhere in the estate lists these files (resources.json
 * does not, and the site's shelf holds games), so the builder is not merely the
 * best record available, it is the only one, and it is the one that cannot
 * silently disagree with what shipped.
 *
 * It is then cross-checked against the placed directory. Two independent records
 * that must agree: a lab added to the builder and not placed, or placed and not
 * declared, is red before a single byte is fetched. That is the check a hand-list
 * cannot make against itself.
 *
 * WHAT IS ASSERTED PER SUBJECT
 *   HTTP 200 · no redirect chain · sha256 of the served body identical to the
 *   blob in this checkout. 200 alone is not the assertion; a stale deploy
 *   answers 200 all day.
 *
 * EXITS
 *   0  every subject served, unredirected and byte-identical, both controls fired
 *   1  a subject is missing, redirected, or stale
 *   2  INCONCLUSIVE — egress blocked, or a record that could not be read. Never
 *      green: a derivation that yields nothing must not read as nothing wrong.
 *
 *   node tools/verify_fieldops_served.mjs
 *   node tools/verify_fieldops_served.mjs --self-test   (controls only, no network)
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const HERE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ARGS = new Set(process.argv.slice(2));

/* Bases are declared, with the reason, because they are not derivable from any
   file in this tree. Overridable so a fork or a staging origin can be pointed
   at without editing the tool. */
const LESSONS_BASE = process.env.LESSONS_BASE || 'https://madebymatt.uk/Lessons';
const APPS_BASE = process.env.APPS_BASE || 'https://mattroper1977.github.io/Matt-s-Apps-';

const PLACED = 'Science_Teesside/Build/v4_fieldops';
const STUDIO_REF = 'tools/fieldops/staging/00_BUILD_FieldOps_Teacher_Studio.html';

const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const rows = [];
const row = (id, verdict, what, detail) => { rows.push({ id, verdict, what, detail }); return verdict; };

class Inconclusive extends Error {}

/* ------------------------------------------------------- the derivation */
/* Evaluate build.mjs's declaration prologue rather than grepping it. Everything
   up to its first side-effecting call is plain const declarations; running that
   much gives the real values, so a rename or a reformat cannot quietly change
   what this tool believes without changing what the builder believes too. */
function declaredSubjects() {
  const src = fs.readFileSync(path.join(HERE, 'tools/fieldops/build.mjs'), 'utf8');
  const end = src.search(/^\s*(?:swap|inject|for\s*\(|await|fs\.)/m);
  if (end < 0) throw new Inconclusive('tools/fieldops/build.mjs has no recognisable declaration prologue');
  /* Run the prologue whole, with the environment stubbed, rather than filtering
     it line by line — the builder's own declarations span several lines and a
     line filter shreds them. import.meta is the one thing that cannot exist
     outside a module, so it is substituted; fs and process are stubbed because
     they are how the builder finds its own directory and read its inputs, and
     neither contributes to the subject list. Nothing here names LABS or STUDIO,
     so a rename or a reformat of either still resolves. */
  const prologue = src.slice(0, end)
    .replace(/^\s*import\b[^\n]*$/gm, '')
    .replace(/import\.meta\.url/g, JSON.stringify('file:///dev/null'));
  const stubFs = { readFileSync: () => '', existsSync: () => false, readdirSync: () => [] };
  const stubProcess = { env: {}, argv: [] };
  let out;
  try {
    out = new Function('fs', 'path', 'process',
      `${prologue}\nreturn { LABS: typeof LABS !== 'undefined' ? LABS : null,` +
      ` STUDIO: typeof STUDIO !== 'undefined' ? STUDIO : null };`)(stubFs, path, stubProcess);
  } catch (e) {
    throw new Inconclusive(`build.mjs's prologue would not evaluate: ${e.message}`);
  }
  if (!Array.isArray(out.LABS) || !out.LABS.length || typeof out.STUDIO !== 'string')
    throw new Inconclusive('build.mjs declares no LABS array or no STUDIO — an empty subject set asserts nothing');
  return out;
}

function subjects() {
  const { LABS, STUDIO } = declaredSubjects();
  const dir = path.join(HERE, PLACED);
  if (!fs.existsSync(dir)) throw new Inconclusive(`${PLACED} does not exist in this checkout`);
  const placed = fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort();

  const missing = LABS.filter(l => !placed.includes(l));
  const extra = placed.filter(p => !LABS.includes(p));
  row('D1', missing.length || extra.length ? 'FAIL' : 'PASS',
      'the builder\'s LABS and the placed directory name the same files',
      `declared ${LABS.length}, placed ${placed.length}` +
      (missing.length ? ` · declared but not placed: ${missing.join(', ')}` : '') +
      (extra.length ? ` · placed but not declared: ${extra.join(', ')}` : ''));

  const list = LABS.map(name => ({
    name, kind: 'lab',
    url: `${LESSONS_BASE}/${PLACED}/${encodeURIComponent(name)}`,
    local: path.join(HERE, PLACED, name),
  }));
  list.push({
    name: STUDIO, kind: 'studio',
    /* The Studio's bytes live in the Apps repository, which this checkout does
       not contain. The reference is the staging build here, which the merge
       proved byte-identical to the placed file — so this leg is still a byte
       assertion, made against a blob this repository actually holds. */
    url: `${APPS_BASE}/FieldOps_Teacher_Studio.html`,
    local: path.join(HERE, STUDIO_REF),
  });
  return list;
}

/* ------------------------------------------------------------- fetching */
async function get(url) {
  const res = await fetch(url, { redirect: 'manual', headers: { 'Cache-Control': 'no-cache' } });
  const body = Buffer.from(await res.arrayBuffer());
  return { status: res.status, location: res.headers.get('location'), body };
}

async function reachable(base) {
  try { const r = await get(base + '/'); return r.status; } catch (e) { return `ERR ${e.message}`; }
}

/* ------------------------------------------------------------- controls */
/* R0.15: the tool that proves serving must be shown able to say NOT SERVED and
   able to say SERVED BUT STALE, and those are different failures. */
async function controls(list) {
  const anchor = list.find(s => s.kind === 'lab');

  /* C1 — a route known absent must red on status. */
  const absent = `${LESSONS_BASE}/${PLACED}/AUTHORED-CONTROL_this-file-is-not-published.html`;
  try {
    const r = await get(absent);
    /* 404 EXACTLY, not merely "not 200". "Not 200" passes in any environment
       that blanket-refuses, which is how this control first went green against
       a proxy 403 while proving nothing at all. */
    row('C1', r.status === 404 ? 'PASS' : r.status === 200 ? 'FAIL' : 'INCONCLUSIVE',
        'a route known absent answers 404',
        `${absent} -> HTTP ${r.status}` +
        (r.status === 200 ? ' — a 200 here means the base URL resolves to something that answers for everything'
         : r.status === 404 ? '' : ' — neither 404 nor 200, so this control did not judge the origin'));
  } catch (e) { row('C1', 'INCONCLUSIVE', 'a route known absent is not reported served', e.message); }

  /* C2 — served but STALE. The local reference is mutated by one byte and the
     comparison must go red on the HASH while the status stays 200. A tool that
     only ever checks status passes this and should not. */
  try {
    const r = await get(anchor.url);
    const local = fs.readFileSync(anchor.local);
    const mutated = Buffer.concat([local, Buffer.from('\n<!-- authored control -->')]);
    const statusOk = r.status === 200;
    const hashDiffers = sha(r.body) !== sha(mutated);
    row('C2', statusOk && hashDiffers ? 'PASS' : 'FAIL',
        'a served-but-stale subject reds on the hash, not on the status',
        `${anchor.name}: HTTP ${r.status}${statusOk ? ' (200, so status alone would pass)' : ''}, ` +
        `served ${sha(r.body).slice(0, 16)} vs mutated reference ${sha(mutated).slice(0, 16)} — ` +
        `${hashDiffers ? 'difference detected' : 'NOT detected, the hash comparison is inert'}`);
  } catch (e) { row('C2', 'INCONCLUSIVE', 'a served-but-stale subject reds on the hash', e.message); }
}

/* --------------------------------------------------------------- offline */
/* The control logic that needs no network, so the instrument itself can be
   proven in a container where egress is blocked. */
function selfTest() {
  let fails = 0;
  const check = (label, cond, detail) => {
    console.log(`  ${cond ? 'PASS' : 'FAIL'}  ${label}${detail ? ` — ${detail}` : ''}`);
    if (!cond) fails++;
  };
  console.log('OFFLINE CONTROLS (the network legs cannot run here; see the exit note)\n');

  let list;
  try { list = subjects(); } catch (e) { check('the subject set derives', false, e.message); return 1; }
  check('the subject set derives from build.mjs, not a hand-list',
        list.length >= 2, `${list.length} subject(s): ${list.map(s => s.name).join(', ')}`);
  check('every subject has a blob in this checkout to compare against',
        list.every(s => fs.existsSync(s.local)),
        list.filter(s => !fs.existsSync(s.local)).map(s => s.local).join(', ') || 'all present');
  check('the builder and the placed directory agree',
        rows.find(r => r.id === 'D1')?.verdict === 'PASS',
        rows.find(r => r.id === 'D1')?.detail);

  /* A derivation that yields nothing must be INCONCLUSIVE, not green. */
  const saved = fs.readFileSync(path.join(HERE, 'tools/fieldops/build.mjs'), 'utf8');
  try {
    fs.writeFileSync(path.join(HERE, 'tools/fieldops/build.mjs'), "const LABS = [];\nconst STUDIO = 'x';\nswap('T1');\n");
    let fired = false;
    try { subjects(); } catch (e) { fired = e instanceof Inconclusive; }
    check('an empty LABS array is INCONCLUSIVE, never an empty green pass', fired);
  } finally {
    fs.writeFileSync(path.join(HERE, 'tools/fieldops/build.mjs'), saved);
  }

  /* And the hash comparison itself, exercised without a server. */
  const a = fs.readFileSync(list[0].local);
  check('the byte comparison distinguishes one appended byte',
        sha(a) !== sha(Buffer.concat([a, Buffer.from('x')])));

  console.log(`\n[OFFLINE] ${fails === 0 ? 'PASS' : 'FAIL'} — ${fails} check(s) failed`);
  return fails === 0 ? 0 : 1;
}

/* ------------------------------------------------------------------ main */
async function main() {
  if (ARGS.has('--self-test')) return selfTest();

  let list;
  try { list = subjects(); }
  catch (e) {
    if (e instanceof Inconclusive) { console.log(`[INCONCLUSIVE] ${e.message}`); return 2; }
    throw e;
  }

  /* Reachability first, so a blocked proxy or a wrong base is reported as
     INCONCLUSIVE rather than dressed up as a fleet of 404s. R0.9. */
  const lessonsRoot = await reachable(LESSONS_BASE);
  const appsRoot = await reachable(APPS_BASE);
  /* A NUMBER IS NOT REACHABILITY. The first cut accepted any numeric status and
     then reported five FAILs and a passing 404-control against a proxy that
     answers 403 on CONNECT to every host — six verdicts about a deployment it
     had never spoken to. The root must answer 200; anything else is a fact
     about the runner and is INCONCLUSIVE. R0.9. */
  if (lessonsRoot !== 200) {
    console.log(`[INCONCLUSIVE] ${LESSONS_BASE}/ answered ${lessonsRoot}, not 200.`);
    console.log('Nothing below could be judged: a run that cannot reach the origin has not');
    console.log('measured the deployment, and a 403 from a blocking proxy looks identical to');
    console.log('an outage from here. Run this in CI, where egress works.');
    return 2;
  }

  for (const s of list) {
    if (s.kind === 'studio' && typeof appsRoot !== 'number') {
      row(s.name, 'INCONCLUSIVE', 'served and byte-identical',
          `${APPS_BASE}/ is unreachable (${appsRoot}) — the Studio leg cannot be judged`);
      continue;
    }
    let r;
    try { r = await get(s.url); }
    catch (e) { row(s.name, 'INCONCLUSIVE', 'served and byte-identical', `${s.url}: ${e.message}`); continue; }

    if (r.status >= 300 && r.status < 400) {
      row(s.name, 'FAIL', 'served without a redirect chain',
          `${s.url} -> HTTP ${r.status} -> ${r.location}. A redirect is not a serve; the visitor's URL is not the file's.`);
      continue;
    }
    if (r.status !== 200) {
      /* If the estate root itself does not serve, this is not the file's fault. */
      row(s.name, appsRoot === 404 && s.kind === 'studio' ? 'INCONCLUSIVE' : 'FAIL',
          'served', `${s.url} -> HTTP ${r.status}`);
      continue;
    }
    const local = fs.readFileSync(s.local);
    const ls = sha(local), rs = sha(r.body);
    row(s.name, ls === rs ? 'PASS' : 'FAIL', 'byte-identical to the merged blob',
        ls === rs ? `HTTP 200 · ${ls.slice(0, 16)} · ${local.length} B`
                  : `HTTP 200 but STALE — repo ${ls.slice(0, 16)} (${local.length} B) vs served ${rs.slice(0, 16)} (${r.body.length} B)`);
  }

  await controls(list);

  console.log(`FieldOps serve proof — ${LESSONS_BASE} · ${APPS_BASE}\n`);
  console.log(`${'subject'.padEnd(46)} ${'verdict'.padEnd(13)} what`);
  console.log('-'.repeat(110));
  for (const r of rows) {
    console.log(`${String(r.id).slice(0, 46).padEnd(46)} ${r.verdict.padEnd(13)} ${r.what}`);
    console.log(`${' '.repeat(47)}${r.detail}`);
  }
  const fail = rows.filter(r => r.verdict === 'FAIL');
  const inc = rows.filter(r => r.verdict === 'INCONCLUSIVE');
  console.log(`\n${rows.filter(r => r.verdict === 'PASS').length} pass · ${fail.length} fail · ${inc.length} inconclusive`);
  if (inc.length) console.log('An INCONCLUSIVE leg is not a pass. It names its blocker above.');
  return fail.length ? 1 : inc.length ? 2 : 0;
}

main().then(c => process.exit(c), e => { console.error(e); process.exit(1); });
