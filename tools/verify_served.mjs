/* MERGED IS NOT SERVED. Source-bound split-publication proof.
 *
 * Four sweeps have now ended in a container proxy 403 for the public origins,
 * so this is written to run in CI where the egress is, and to be honest here
 * rather than optimistic. It asserts BYTE-IDENTITY of the served response to
 * the successful publication artifact. 200 is a precondition, never the verdict: 200 proves a
 * server answered, not that it answered with this build, and every serve
 * failure this estate has actually had — the parked shelf entry, the 42 hidden
 * games, the stale route list — would have passed a 200-only check.
 *
 * THE ROUTE SET IS COMPOSED, NOT RE-DERIVED
 * Three estates, each read through its own canonical record, and no hand list
 * anywhere:
 *
 *   site      tools/derive_live_routes.mjs in the SITE repo, INVOKED, not
 *             reimplemented — it derives every game the site serves from the
 *             canonical shelf (the MattRoper1977/Games repo) and ships seven
 *             controls of its own. Writing a second site-route deriver here is
 *             exactly the species it was built to kill.
 *   lessons   tools/fieldops/build.mjs LABS[] — the builder cannot emit a lab
 *             it does not name — plus the hub those labs' NAV-1 link resolves
 *             to, taken from the link rather than assumed.
 *   apps      the same builder's STUDIO.
 *
 * A group that yields nothing is INCONCLUSIVE for that group and the run exits
 * 2. A derivation that silently produced zero routes would turn this gate green
 * by checking nothing, which is how the last four instruments in this estate
 * failed.
 *
 * DEPLOY TIMING IS STATED, NOT ASSUMED
 * Pages publishes asynchronously. A byte mismatch is retried on a bounded
 * schedule, and the verdict distinguishes:
 *   RETRY -> RESOLVED  the bytes caught up within the bound
 *   RED                the successful exact-source publication still differs
 *   INCONCLUSIVE       source-bound deployment/artifact evidence is absent,
 *                      or a request/overall time bound prevents assessment
 *
 * A REDIRECT IS FOLLOWED, AND ITS DESTINATION IS ASSERTED
 * Permitting a chain is not the same as saying where it may end. The permitted
 * terminus is derived from the site repo's CNAME and its own remote, and a
 * chain ending anywhere else is RED naming both origins — checked BEFORE the
 * bytes, because a mirror is precisely where the bytes would match.
 *
 *   node tools/verify_served.mjs --publications <record>  assert
 *   node tools/verify_served.mjs --self-test        controls (c)(d)(e), no network
 *   node tools/verify_served.mjs --controls-only    all five controls, no verdict —
 *                                                   safe on a PR, whose branch is
 *                                                   not deployed
 *
 * Exit 0 every route served and byte-identical · 1 a route is missing,
 * redirected to something else, or stale · 2 INCONCLUSIVE (no egress, an empty
 * derivation, or assessment prevented by a request/deadline bound).
 * Expected bytes belong to the checked-out source's successful deployment,
 * never a rebuilt current tree or the legacy /pages/builds/latest endpoint.
 */
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const TOOL_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ARGS = process.argv.slice(2);
const SELFTEST = ARGS.includes('--self-test');
const arg = (n, d) => { const i = ARGS.indexOf(n); return i >= 0 ? ARGS[i + 1] : d; };
const HERE = path.resolve(arg('--lessons', TOOL_ROOT));

const SITE = arg('--site', process.env.MBM_SITE_REPO || '/workspace/mattroper1977.github.io');
const APPS = arg('--apps', process.env.MBM_APPS_REPO || '/workspace/matt-s-apps-');
const SHELF = arg('--shelf', process.env.MBM_SHELF_REPO || '');
const PUBLICATIONS = arg('--publications', '');

/* The origins a request STARTS at are declared, and overridable so a staging
   origin can be pointed at.

   An earlier version of this comment said they "are not derivable from any file
   in these trees". That was false, and the falsehood mattered: the site repo's
   CNAME holds the canonical domain, and the site repo's own name is the Pages
   host. Where a request is allowed to END is therefore derived, not declared —
   see expectedHosts(). */
const SITE_ORIGIN = process.env.SITE_ORIGIN || 'https://madebymatt.uk';
const LESSONS_ORIGIN = process.env.LESSONS_ORIGIN || 'https://madebymatt.uk/Lessons';
const APPS_ORIGIN = process.env.APPS_ORIGIN || 'https://mattroper1977.github.io/Matt-s-Apps-';

/* §2.4 — the bound, stated. */
const RETRY_MAX = Number(process.env.SERVE_RETRIES || 4);
const RETRY_MS = Number(process.env.SERVE_RETRY_MS || 20000);
const REQUEST_MS = Number(process.env.SERVE_REQUEST_MS || 12000);
const DEADLINE_MS = Number(process.env.SERVE_DEADLINE_MS || 240000);
const CONCURRENCY = Number(process.env.SERVE_CONCURRENCY || 8);
let deadline = Infinity;
let publicationProof = null;

for (const [label, value, min, max] of [
  ['retries', RETRY_MAX, 0, 4], ['retry interval', RETRY_MS, 0, 20000],
  ['request timeout', REQUEST_MS, 1, 30000], ['overall deadline', DEADLINE_MS, 1, 300000],
  ['concurrency', CONCURRENCY, 1, 12]]) {
  if (!Number.isInteger(value) || value < min || value > max)
    throw new Error(`Invalid ${label}: ${value}; expected ${min}–${max}`);
}

const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const sleep = ms => new Promise(r => setTimeout(r, ms));
class Inconclusive extends Error {}

function revision(root) {
  return execFileSync('git', ['-C', root, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
}

function publicationSubjects(original, record = PUBLICATIONS, sourceRoots = null) {
  if (!record) throw new Inconclusive('live proof requires --publications from prepare_served_publications.py; raw source is not the split publication');
  const proof = JSON.parse(fs.readFileSync(record, 'utf8'));
  if (proof.version !== 1 || !proof.publications || !Array.isArray(proof.canonical_game_routes) || !proof.canonical_game_routes.length)
    throw new Inconclusive('empty or unrecognised publication evidence');
  const roots = sourceRoots || { site: SITE, lessons: HERE, apps: APPS, games: SHELF };
  for (const [kind, root] of Object.entries(roots)) {
    const p = proof.publications[kind];
    if (!p || p.source_sha !== revision(root) || p.deployment !== 'success' ||
        !Number.isSafeInteger(p.run_id) || p.run_id <= 0 ||
        !Number.isSafeInteger(p.artifact_id) || p.artifact_id <= 0 ||
        !/^[a-f0-9]{40}$/.test(p.publication_sha) || !/^sha256:[a-f0-9]{64}$/.test(p.artifact_sha256))
      throw new Inconclusive(`${kind}: publication evidence does not match the checked-out source and successful deployment`);
  }
  const play = JSON.parse(fs.readFileSync(path.join(roots.games, 'play-publication.json'), 'utf8'));
  if (proof.games_origin !== `https://${play.domain}`)
    throw new Inconclusive('games publication origin differs from the committed Games declaration');
  const normal = r => decodeURIComponent(new URL(r, 'https://routes.invalid').pathname).replace(/index\.html$/, '').replace(/\/$/, '') || '/';
  const games = JSON.parse(fs.readFileSync(path.join(roots.games, 'games.json'), 'utf8')).games.map(g => normal(g.href));
  const recorded = proof.canonical_game_routes;
  if (new Set(recorded).size !== recorded.length || games.length !== recorded.length || games.some(g => !recorded.includes(g)))
    throw new Inconclusive('publication membership differs from the canonical Games shelf');
  const list = original.list.map(subj => {
    let kind = subj.group;
    let relative = path.relative(roots[kind], subj.blob);
    let url = subj.url;
    // Keep every original P0 game and infrastructure subject. The Games hub
    // follows the independent publication; education / and site.json stay on
    // their own domain. No game source or baseline is modified.
    if (kind === 'site' && (games.includes(normal(subj.name)) || normal(subj.name) === '/games')) {
      kind = 'games';
      url = proof.games_origin + subj.name;
    }
    const root = path.resolve(proof.publications[kind].root);
    const blob = path.resolve(root, relative);
    if (!blob.startsWith(root + path.sep)) throw new Inconclusive(`escaping publication path: ${relative}`);
    if (!fs.existsSync(blob)) throw new Inconclusive(`${kind}: deployed artifact omits ${relative}`);
    return { ...subj, group: kind, url, blob, source_group: subj.group,
      publication_run: proof.publications[kind].run_id };
  });
  verdictFor(original.list, list.length);
  publicationProof = proof;
  return { ...original, list, missing: [] };
}

/* ------------------------------------------------------- the derivations */
function fieldopsDecls() {
  const src = fs.readFileSync(path.join(HERE, 'tools/fieldops/build.mjs'), 'utf8');
  const end = src.search(/^\s*(?:swap|inject|for\s*\(|await|fs\.)/m);
  if (end < 0) throw new Inconclusive('tools/fieldops/build.mjs has no declaration prologue');
  const prologue = src.slice(0, end)
    .replace(/^\s*import\b[^\n]*$/gm, '')
    .replace(/import\.meta\.url/g, JSON.stringify('file:///dev/null'));
  const out = new Function('fs', 'path', 'process',
    `${prologue}\nreturn { LABS: typeof LABS !== 'undefined' ? LABS : null,` +
    ` STUDIO: typeof STUDIO !== 'undefined' ? STUDIO : null };`)(
      { readFileSync: () => '', existsSync: () => false, readdirSync: () => [] }, path, { env: {}, argv: [] });
  if (!Array.isArray(out.LABS) || !out.LABS.length || typeof out.STUDIO !== 'string')
    throw new Inconclusive('build.mjs declares no LABS or no STUDIO — an empty subject set asserts nothing');
  return out;
}

/* The hub is read off the labs' own NAV-1 link rather than assumed. If the four
   labs disagree about where home is, that is a finding and not a default. */
function hubFrom(labs) {
  const dir = 'Science_Teesside/Build/v4_fieldops';
  const targets = new Set();
  for (const l of labs) {
    const p = path.join(HERE, dir, l);
    if (!fs.existsSync(p)) continue;
    const m = fs.readFileSync(p, 'utf8').match(/class="mbmhome"[^>]*href="([^"]+)"/);
    if (m) targets.add(path.normalize(path.join(dir, m[1])));
  }
  if (targets.size !== 1)
    throw new Inconclusive(`the labs' NAV-1 links resolve to ${targets.size} different hubs: ${[...targets]}`);
  return [...targets][0];
}

function siteRoutes() {
  if (!fs.existsSync(SITE)) return { routes: [], why: `site repo not present at ${SITE}` };
  const deriver = path.join(SITE, 'tools/derive_live_routes.mjs');
  if (!fs.existsSync(deriver)) return { routes: [], why: `the P0 deriver is not at ${deriver}` };
  const shelf = SHELF && fs.existsSync(path.join(SHELF, 'games.json'))
    ? path.join(SHELF, 'games.json') : null;
  if (!shelf) return { routes: [], why: 'the canonical shelf (MattRoper1977/Games games.json) was not supplied — pass --shelf' };
  try {
    const out = execFileSync('node', [deriver, '--canonical', shelf, '--root', SITE, '--emit', 'routes'],
      { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
    return { routes: out.split('\n').map(s => s.trim()).filter(Boolean), why: null };
  } catch (e) {
    return { routes: [], why: `the P0 deriver exited non-zero: ${(e.stderr || e.message || '').toString().split('\n')[0]}` };
  }
}

function subjects() {
  const { LABS, STUDIO } = fieldopsDecls();
  const list = [];
  const residue = [];

  const site = siteRoutes();
  for (const r of site.routes) {
    /* A ROUTE ENDING IN A FILE EXTENSION IS A FILE, NOT A DIRECTORY.
       The deriver now emits the infrastructure routes it used to leave as
       unchecked residue, and one of them — /site.json — is data rather than a
       page. The byte assertion is the same and stays the same; what changes is
       WHERE the blob is. Expecting <r>/index.html behind /site.json would
       compare the served record against a path that does not exist, which is
       not a weaker check, it is a wrong one. */
    const rel = r.replace(/^\/|\/$/g, '');
    const isFile = /\.[a-z0-9]+$/i.test(rel);
    const blob = isFile ? path.join(SITE, rel) : path.join(SITE, rel, 'index.html');
    const type = isFile && /\.json$/i.test(rel) ? 'application/json' : 'text/html';
    list.push({ group: 'site', name: r, url: SITE_ORIGIN + r, blob, type });
  }
  if (site.why) residue.push({ group: 'site', why: site.why });

  for (const l of LABS) {
    list.push({ group: 'lessons', name: l,
      url: `${LESSONS_ORIGIN}/Science_Teesside/Build/v4_fieldops/${encodeURIComponent(l)}`,
      blob: path.join(HERE, 'Science_Teesside/Build/v4_fieldops', l), type: 'text/html' });
  }
  const hub = hubFrom(LABS);
  list.push({ group: 'lessons', name: `hub (${hub})`, url: `${LESSONS_ORIGIN}/`,
    blob: path.join(HERE, hub), type: 'text/html' });

  if (fs.existsSync(APPS)) {
    list.push({ group: 'apps', name: STUDIO, url: `${APPS_ORIGIN}/FieldOps_Teacher_Studio.html`,
      blob: path.join(APPS, 'FieldOps_Teacher_Studio.html'), type: 'text/html' });
  } else {
    /* The Studio's bytes live in the Apps repo. Without it the reference is the
       staging build here, which the merge proved byte-identical — still a byte
       assertion, made against a blob this repository actually holds. */
    list.push({ group: 'apps', name: `${STUDIO} (reference: staging copy)`,
      url: `${APPS_ORIGIN}/FieldOps_Teacher_Studio.html`,
      blob: path.join(HERE, 'tools/fieldops/staging', STUDIO), type: 'text/html' });
    residue.push({ group: 'apps', why: `apps repo not present at ${APPS}; compared against the staging build instead` });
  }

  const missing = list.filter(s => !fs.existsSync(s.blob));
  return { list, residue, missing };
}

/* --------------------------------------------------------------- fetching */
async function get(url, requestMs = REQUEST_MS, requestDeadline = deadline) {
  const chain = [];
  let cur = url;
  const budget = Math.min(requestMs, requestDeadline - Date.now());
  if (budget <= 0) throw new Inconclusive('overall serve deadline reached');
  const signal = AbortSignal.timeout(Math.max(1, Math.ceil(budget)));
  for (let hop = 0; hop < 5; hop++) {
    const res = await fetch(cur, { redirect: 'manual', signal, headers: { 'Cache-Control': 'no-cache' } });
    if (res.status >= 300 && res.status < 400 && res.headers.get('location')) {
      chain.push(`${cur} -> ${res.status} -> ${res.headers.get('location')}`);
      cur = new URL(res.headers.get('location'), cur).toString();
      continue;
    }
    return { status: res.status, chain, type: res.headers.get('content-type') || '',
             body: Buffer.from(await res.arrayBuffer()), final: cur };
  }
  return { status: 508, chain, type: '', body: Buffer.alloc(0), final: cur };
}

/* ------------------------------------------------- where a chain may END */
/* PERMITTING A REDIRECT IS NOT ASSERTING WHERE IT GOES.
   The predecessor to this tool failed the Teacher Studio for answering 301 at
   all. Fixing that — following the chain and comparing bytes at the far end —
   opened a gap in the other direction: a chain that terminated on an origin
   nobody asserted would have had its bytes compared at that origin, and a match
   there would have read as SERVED. A mirror, a parked domain or a hijacked
   CNAME is exactly the case where the bytes plausibly DO match.

   The permitted set is DERIVED, never hand-listed:
     the canonical domain   the site repo's CNAME file, which is the record
                            GitHub Pages itself acts on
     the Pages host         <owner>.github.io, from the site repo's own remote

   Undeliverable derivation is INCONCLUSIVE, not an empty set: an empty
   permitted set would reject every route, and a check that fails everything is
   as useless as one that passes everything. */
function expectedHosts() {
  const cname = path.join(SITE, 'CNAME');
  if (!fs.existsSync(cname))
    throw new Inconclusive(`no CNAME at ${cname} — the canonical domain cannot be derived, and hand-listing it is what this avoids`);
  const domain = fs.readFileSync(cname, 'utf8').split('\n')[0].trim().replace(/^https?:\/\//, '').replace(/\/$/, '');
  if (!domain) throw new Inconclusive('the site repo CNAME is empty');

  let owner = null;
  try {
    const remote = execFileSync('git', ['-C', SITE, 'remote', 'get-url', 'origin'],
      { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim();
    const m = remote.match(/github\.com[:/]+([^/]+)\//i);
    if (m) owner = m[1].toLowerCase();
  } catch (_) { /* fall through to the throw below */ }
  if (!owner)
    throw new Inconclusive(`could not read the site repo's origin remote at ${SITE} — the Pages host cannot be derived`);

  return { hosts: [domain, `${owner}.github.io`], from: `CNAME=${domain}, remote owner=${owner}` };
}

/* The verdict on one terminus. Returns what was reached and what was permitted,
   so a red can name both rather than saying "unexpected". */
function destinationVerdict(finalUrl, hosts, requestedUrl = null) {
  let got;
  let parsed;
  try { parsed = new URL(finalUrl); got = parsed.host.toLowerCase(); }
  catch (e) { return { ok: false, got: `(unparseable: ${finalUrl})`, want: hosts }; }
  const requested = requestedUrl ? new URL(requestedUrl) : null;
  return { ok: hosts.includes(got) && parsed.protocol === 'https:' && !parsed.username && !parsed.password &&
    (!requested || (parsed.pathname === requested.pathname && parsed.search === requested.search && parsed.hash === requested.hash)), got, want: hosts };
}

function subjectHosts(subj, fallback) {
  if (!publicationProof) return fallback;
  const origin = new URL(subj.url);
  if (subj.group === 'games') return [origin.host, `www.${origin.host}`];
  // Project Pages redirects may move from the owner.github.io host to the
  // declared education domain, but must retain the exact resource path.
  return fallback;
}

async function reachable(origin) {
  try { const r = await get(origin + '/'); return r.status; }
  catch (e) { return `ERR ${e.message}`; }
}

/* --------------------------------------------------------------- controls */
async function controls(list) {
  const out = [];
  const anchor = list.find(s => s.group === 'lessons');

  /* (a) a route known absent must answer 404 — not merely "not 200", which
         passes in any environment that blanket-refuses. */
  try {
    const r = await get(`${LESSONS_ORIGIN}/AUTHORED-CONTROL_this-route-is-not-published.html`);
    out.push({ id: 'a', what: 'a route known absent answers 404',
      fired: r.status === 404, detail: `HTTP ${r.status}` });
  } catch (e) { out.push({ id: 'a', what: 'a route known absent answers 404', fired: false, detail: e.message }); }

  /* (b) an expected hash mutated by one byte must go red, with the status
         still 200 — so a status-only check would pass and this must not. */
  try {
    const r = await get(anchor.url);
    // Production is a fixture on PRs, not the unpublished branch. Require the
    // same predicate to accept genuine bytes and reject one appended byte.
    const local = Buffer.from(r.body);
    const mutated = Buffer.concat([local, Buffer.from([0])]);
    const hosts = subjectHosts(anchor, expectedHosts().hosts);
    out.push({ id: 'b', what: 'a one-byte mutation of the expected hash goes red',
      fired: responseVerdict(r, sha(local), anchor, hosts).verdict === 'SERVED' &&
             responseVerdict(r, sha(mutated), anchor, hosts).verdict === 'MISMATCH',
      detail: `HTTP ${r.status}; served ${sha(r.body).slice(0, 12)} vs mutated ${sha(mutated).slice(0, 12)}` });
  } catch (e) { out.push({ id: 'b', what: 'a one-byte mutation of the expected hash goes red', fired: false, detail: e.message }); }

  return out;
}

/* Controls (c), (d) and (e) need no network and are proven in --self-test too. */
function structuralControls() {
  const out = [];

  /* (e) a chain terminating on an origin nobody asserted must go red, and must
         name BOTH origins — the one reached and the ones permitted.

         Matched pair inside one control, deliberately. Asserting only that the
         rogue terminus is rejected would be satisfied by a predicate that
         rejects everything, which is the mirror of the empty-set defect this
         file already guards in (c). So the genuine terminus must be accepted in
         the same breath. */
  let eFired = false, eDetail;
  try {
    const { hosts, from } = expectedHosts();
    const rogue = destinationVerdict('https://mirror.example.invalid/Matt-s-Apps-/FieldOps_Teacher_Studio.html', hosts);
    const real = destinationVerdict(`https://${hosts[0]}/Matt-s-Apps-/FieldOps_Teacher_Studio.html`, hosts);
    const pages = destinationVerdict(`https://${hosts[1]}/Matt-s-Apps-/FieldOps_Teacher_Studio.html`, hosts);
    eFired = !rogue.ok && real.ok && pages.ok &&
             rogue.got.includes('mirror.example.invalid') && rogue.want.length === 2;
    eDetail = `rejected ${rogue.got}, permitted ${hosts.join(' + ')} (derived: ${from})`;
  } catch (err) {
    eDetail = err instanceof Inconclusive
      ? `the permitted set could not be derived: ${err.message}` : String(err && err.message);
  }

  out.push({ id: 'c', what: 'an empty derived route set exits 2, never green',
    fired: (() => { try { verdictFor([], 0); return false; } catch (e) { return e instanceof Inconclusive; } })(),
    detail: 'verdictFor([]) raises Inconclusive' });
  out.push({ id: 'd', what: 'assessed must equal derived, or exit 2',
    fired: (() => { try { verdictFor([1, 2, 3], 2); return false; } catch (e) { return e instanceof Inconclusive; } })(),
    detail: '3 derived, 2 assessed -> Inconclusive' });
  out.push({ id: 'e', what: 'a chain ending on an unexpected origin goes red, naming both', fired: eFired, detail: eDetail });
  return out;
}

function verdictFor(derived, assessed) {
  if (!derived.length) throw new Inconclusive('the derived route set is empty — this gate would have checked nothing');
  if (assessed !== derived.length)
    throw new Inconclusive(`assessed ${assessed} of ${derived.length} derived routes — NOT ASSESSED is a diagnostic, never a pass`);
  return true;
}

/* ------------------------------------------------------------- self-test */
function selfTest() {
  let bad = 0;
  const say = (ok, label, detail) => { console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${label}${detail ? ` — ${detail}` : ''}`); if (!ok) bad++; };
  console.log('OFFLINE CONTROLS — the network legs cannot run here\n');

  let s;
  try { s = subjects(); } catch (e) { say(false, 'the subject set derives', e.message); return 1; }

  const byGroup = g => s.list.filter(x => x.group === g).length;
  say(s.list.length > 0, 'the subject set composes from three canonical records',
      `${s.list.length} routes — site ${byGroup('site')}, lessons ${byGroup('lessons')}, apps ${byGroup('apps')}`);
  say(s.missing.length === 0, 'every subject has a committed blob to compare against',
      s.missing.map(m => m.name).join(', ') || 'all present');
  for (const c of structuralControls()) say(c.fired, `control (${c.id}) ${c.what}`, c.detail);
  say(sha(Buffer.from('a')) !== sha(Buffer.from('ab')), 'the byte comparison distinguishes one appended byte');

  for (const r of s.residue) console.log(`  RESIDUE  ${r.group}: ${r.why}`);
  console.log(`\n[OFFLINE] ${bad === 0 ? 'PASS' : 'FAIL'} — ${bad} check(s) failed`);
  return bad === 0 ? 0 : 1;
}

/* -------------------------------------------------------- controls only */
/* THE CONTROLS DO NOT NEED THE BRANCH TO BE DEPLOYED.
   The live route verdict does: a PR branch is not published, so comparing the
   estate against it would go red for being a PR, which is why the verdict leg
   is skipped there. But (a) and (b) use production as a FIXTURE, not as the
   subject — (a) asks a known-absent route for a 404, (b) asks a real route for
   bytes and asserts they differ from a deliberately mutated hash. Neither claim
   changes with the branch.

   That distinction is worth the mode. Without it the only controls a pull
   request could fire were the offline ones, and this arc exists because of
   gates that never ran where they were needed. */
async function controlsOnly() {
  let s;
  try { s = subjects(); }
  catch (e) { if (e instanceof Inconclusive) { console.log(`[INCONCLUSIVE] ${e.message}`); return 2; } throw e; }

  console.log('CONTROLS ONLY — the instrument, not the deployment.\n');
  const root = await reachable(LESSONS_ORIGIN);
  if (root !== 200) {
    console.log(`[INCONCLUSIVE] the lessons origin answered ${root} from this runner, not 200.`);
    console.log('The network controls need a reachable fixture. This is a fact about the');
    console.log('runner, and it is INCONCLUSIVE rather than a failed control.');
    for (const c of structuralControls())
      console.log(`  (${c.id}) ${c.fired ? 'FIRED' : 'DID NOT FIRE'}  ${c.what} — ${c.detail}`);
    return 2;
  }

  const all = [...await controls(s.list), ...structuralControls()];
  for (const c of all)
    console.log(`  (${c.id}) ${c.fired ? 'FIRED' : 'DID NOT FIRE'}  ${c.what} — ${c.detail}`);
  const dead = all.filter(c => !c.fired);
  console.log(`\n${all.length - dead.length} of ${all.length} controls fired.`);
  if (dead.length) {
    console.log(`[FAIL] did not fire: ${dead.map(c => `(${c.id})`).join(', ')} — the gate cannot be trusted to catch what it claims.`);
    return 1;
  }
  console.log('Every control fired. This says the instrument works; it says NOTHING about');
  console.log('what is served from this branch, which is not deployed.');
  return 0;
}

/* -------------------------------------- byte and resource predicates */
function responseVerdict(response, expectedHash, subject, hosts) {
  if (response.status !== 200)
    return { verdict: 'RED', detail: `HTTP ${response.status}` };
  const dest = destinationVerdict(response.final, hosts, subject.url);
  if (!dest.ok)
    return { verdict: 'RED', detail: `unexpected HTTPS resource: ${response.final}; requested ${subject.url}; permitted hosts ${hosts.join(' or ')}` };
  const actual = sha(response.body);
  if (actual !== expectedHash)
    return { verdict: 'MISMATCH', detail: `HTTP 200: expected ${expectedHash} vs served ${actual} (${response.body.length} B)` };
  const type = response.type.split(';')[0].trim().toLowerCase();
  if (type !== subject.type)
    return { verdict: 'RED', detail: `byte-identical but content-type ${type || '(none)'}; expected ${subject.type}` };
  return { verdict: 'SERVED', detail: `200 · ${actual} · ${response.body.length} B · ${type}` };
}

async function mapLimit(items, limit, action) {
  const results = new Array(items.length);
  let next = 0;
  await Promise.all(Array.from({ length: Math.min(items.length, limit) }, async () => {
    while (next < items.length) {
      const i = next++;
      results[i] = await action(items[i], i);
    }
  }));
  return results;
}

async function assess(subject, hosts, deadGroups, roots) {
  const expected = sha(fs.readFileSync(subject.blob));
  let result = { verdict: 'INCONCLUSIVE', detail: 'not reached before the overall serve deadline', attempts: 0 };
  if (deadGroups.has(subject.group))
    return { ...subject, ...result, detail: `the ${subject.group} origin answered ${roots[subject.group]}; no route verdict is claimed` };
  for (let attempt = 0; attempt <= RETRY_MAX; attempt++) {
    if (Date.now() >= deadline) break;
    try {
      const response = await get(subject.url);
      result = { ...responseVerdict(response, expected, subject, subjectHosts(subject, hosts)), attempts: attempt + 1 };
      if (result.verdict !== 'MISMATCH') break;
      console.log(`RETRY ${subject.group} ${subject.name} attempt ${attempt + 1}: ${result.detail}`);
      if (attempt === RETRY_MAX) {
        result.verdict = 'RED';
        result.detail += `; successful source-bound publication ${subject.publication_run} still differs after ${attempt + 1} attempts`;
        break;
      }
      const remaining = deadline - Date.now();
      if (remaining <= RETRY_MS) {
        result.verdict = 'INCONCLUSIVE';
        result.detail += '; overall serve deadline leaves no complete retry interval';
        break;
      }
      await sleep(RETRY_MS);
    } catch (error) {
      result = { verdict: 'INCONCLUSIVE', attempts: attempt + 1, detail: `request failed within its time bound: ${error.message}` };
      break;
    }
  }
  if (result.verdict === 'MISMATCH') {
    result.verdict = 'INCONCLUSIVE';
    result.detail += '; overall serve deadline reached before completing retries';
  }
  return { ...subject, ...result };
}

/* ------------------------------------------------------------------ main */
async function main() {
  if (SELFTEST) return selfTest();
  deadline = Date.now() + DEADLINE_MS;
  if (ARGS.includes('--controls-only')) return controlsOnly();

  let s;
  try {
    const original = subjects();
    if (original.residue.length)
      throw new Inconclusive(original.residue.map(r => `${r.group}: ${r.why}`).join('; '));
    s = publicationSubjects(original);
  } catch (error) {
    console.log(`[INCONCLUSIVE] ${error.message}`);
    return 2;
  }
  console.log(`serve proof — ${s.list.length} original subjects retained; exact successful publication bytes`);
  console.log(`bounds: ${REQUEST_MS} ms per request, ${CONCURRENCY} concurrent, ${DEADLINE_MS} ms overall, up to ${RETRY_MAX + 1} attempts`);
  for (const [kind, evidence] of Object.entries(publicationProof.publications))
    console.log(`PUBLICATION ${kind}: checked source ${evidence.source_sha}; deployed source ${evidence.publication_sha}; run ${evidence.run_id}; artifact ${evidence.artifact_id} ${evidence.artifact_sha256}`);

  let hosts;
  try { hosts = expectedHosts().hosts; }
  catch (error) { console.log(`[INCONCLUSIVE] ${error.message}`); return 2; }
  const origins = { site: SITE_ORIGIN, lessons: LESSONS_ORIGIN, apps: APPS_ORIGIN, games: publicationProof.games_origin };
  const roots = Object.fromEntries(await Promise.all(Object.entries(origins).map(async ([kind, origin]) => [kind, await reachable(origin)])));
  const deadGroups = new Set(Object.entries(roots).filter(([, status]) => status !== 200).map(([kind]) => kind));
  for (const [kind, status] of Object.entries(roots)) console.log(`ORIGIN ${kind}: ${origins[kind]} -> ${status}`);

  // Fire the controls before retries consume the verdict budget. An exhausted
  // gate must still record why its controls could not be assessed.
  const ctl = [...await controls(s.list), ...structuralControls()];
  for (const c of ctl) console.log(`CONTROL (${c.id}) ${c.fired ? 'FIRED' : 'DID NOT FIRE'} ${c.what} — ${c.detail}`);

  const rows = await mapLimit(s.list, CONCURRENCY, async subject => {
    const row = await assess(subject, hosts, deadGroups, roots);
    // Emit each outcome immediately; even an externally cancelled workflow
    // retains the offending route instead of a ten-minute silent interval.
    console.log(`${row.verdict} ${row.group} ${row.name} — ${row.detail}`);
    return row;
  });
  const served = rows.filter(r => r.verdict === 'SERVED');
  const red = rows.filter(r => r.verdict === 'RED');
  const inc = rows.filter(r => r.verdict === 'INCONCLUSIVE');
  console.log(`\n${served.length} served byte-identical · ${red.length} red · ${inc.length} inconclusive, of ${rows.length} derived`);
  console.log(`${ctl.filter(c => c.fired).length}/5 controls fired`);
  const output = arg('--output', '');
  if (output) fs.writeFileSync(output, JSON.stringify({ version: 1, publications: publicationProof.publications,
    controls: ctl, rows, counts: { derived: s.list.length, served: served.length, red: red.length, inconclusive: inc.length } }, null, 2) + '\n');
  if (ctl.some(c => !c.fired)) {
    console.log('[INCONCLUSIVE] a control did not fire; no successful serve result is reported');
    return 2;
  }
  try { verdictFor(s.list, rows.length); }
  catch (error) { console.log(`[INCONCLUSIVE] ${error.message}`); return 2; }
  return red.length ? 1 : inc.length ? 2 : 0;
}

export { Inconclusive, get, mapLimit, responseVerdict, destinationVerdict, verdictFor, publicationSubjects };
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url))
  main().then(code => process.exit(code), error => { console.error(error); process.exit(error instanceof Inconclusive ? 2 : 1); });
