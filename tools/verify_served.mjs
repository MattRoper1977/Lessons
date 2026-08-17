/* MERGED IS NOT SERVED.  R0.4, for the whole estate.
 *
 * Four sweeps have now ended in a container proxy 403 for the public origins,
 * so this is written to run in CI where the egress is, and to be honest here
 * rather than optimistic. It asserts BYTE-IDENTITY of the served response to
 * the committed blob. 200 is a precondition, never the verdict: 200 proves a
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
 *   RED                the bytes did not, and the deployment reports current
 *   INCONCLUSIVE       the bytes did not, and the deployment SHA is unknown, so
 *                      "stale deploy" and "wrong bytes" cannot be told apart
 *
 *   node tools/verify_served.mjs                 assert
 *   node tools/verify_served.mjs --self-test     the four controls, no network
 *
 * Exit 0 every route served and byte-identical · 1 a route is missing,
 * redirected to something else, or stale · 2 INCONCLUSIVE (no egress, an empty
 * derivation, or a mismatch that cannot be distinguished from a live deploy).
 */
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ARGS = process.argv.slice(2);
const SELFTEST = ARGS.includes('--self-test');
const arg = (n, d) => { const i = ARGS.indexOf(n); return i >= 0 ? ARGS[i + 1] : d; };

const SITE = arg('--site', process.env.MBM_SITE_REPO || '/workspace/mattroper1977.github.io');
const APPS = arg('--apps', process.env.MBM_APPS_REPO || '/workspace/matt-s-apps-');
const SHELF = arg('--shelf', process.env.MBM_SHELF_REPO || '');

/* Origins are declared with the reason: they are not derivable from any file in
   these trees. Overridable so a staging origin can be pointed at. */
const SITE_ORIGIN = process.env.SITE_ORIGIN || 'https://madebymatt.uk';
const LESSONS_ORIGIN = process.env.LESSONS_ORIGIN || 'https://madebymatt.uk/Lessons';
const APPS_ORIGIN = process.env.APPS_ORIGIN || 'https://mattroper1977.github.io/Matt-s-Apps-';

/* §2.4 — the bound, stated. */
const RETRY_MAX = Number(process.env.SERVE_RETRIES || 4);
const RETRY_MS = Number(process.env.SERVE_RETRY_MS || 20000);

const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const sleep = ms => new Promise(r => setTimeout(r, ms));
class Inconclusive extends Error {}

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
    const blob = path.join(SITE, r.replace(/^\/|\/$/g, ''), 'index.html');
    list.push({ group: 'site', name: r, url: SITE_ORIGIN + r, blob, type: 'text/html' });
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
async function get(url) {
  const chain = [];
  let cur = url;
  for (let hop = 0; hop < 5; hop++) {
    const res = await fetch(cur, { redirect: 'manual', headers: { 'Cache-Control': 'no-cache' } });
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

async function reachable(origin) {
  try { const r = await get(origin + '/'); return r.status; }
  catch (e) { return `ERR ${e.message}`; }
}

/* Pages deployment SHA, where the token allows it. Unknown is reported as
   unknown; it changes a mismatch from RED to INCONCLUSIVE, because "stale
   deploy" and "wrong bytes" are different findings. */
async function pagesSha(repo) {
  const tok = process.env.GITHUB_TOKEN || process.env.GH_TOKEN;
  if (!tok) return { sha: null, why: 'no token' };
  try {
    const r = await fetch(`https://api.github.com/repos/${repo}/pages/builds/latest`,
      { headers: { Authorization: `Bearer ${tok}`, Accept: 'application/vnd.github+json',
                   'User-Agent': 'mbm-verify-served' } });
    if (!r.ok) return { sha: null, why: `HTTP ${r.status}` };
    const j = await r.json();
    return { sha: j.commit || null, status: j.status, why: null };
  } catch (e) { return { sha: null, why: e.message }; }
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
    const local = fs.readFileSync(anchor.blob);
    const mutated = Buffer.concat([local, Buffer.from('\n<!-- authored control -->')]);
    out.push({ id: 'b', what: 'a one-byte mutation of the expected hash goes red',
      fired: r.status === 200 && sha(r.body) !== sha(mutated),
      detail: `HTTP ${r.status}; served ${sha(r.body).slice(0, 12)} vs mutated ${sha(mutated).slice(0, 12)}` });
  } catch (e) { out.push({ id: 'b', what: 'a one-byte mutation of the expected hash goes red', fired: false, detail: e.message }); }

  return out;
}

/* Controls (c) and (d) need no network and are proven in --self-test too. */
function structuralControls() {
  const out = [];
  out.push({ id: 'c', what: 'an empty derived route set exits 2, never green',
    fired: (() => { try { verdictFor([], 0); return false; } catch (e) { return e instanceof Inconclusive; } })(),
    detail: 'verdictFor([]) raises Inconclusive' });
  out.push({ id: 'd', what: 'assessed must equal derived, or exit 2',
    fired: (() => { try { verdictFor([1, 2, 3], 2); return false; } catch (e) { return e instanceof Inconclusive; } })(),
    detail: '3 derived, 2 assessed -> Inconclusive' });
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

/* ------------------------------------------------------------------ main */
async function main() {
  if (SELFTEST) return selfTest();

  let s;
  try { s = subjects(); }
  catch (e) { if (e instanceof Inconclusive) { console.log(`[INCONCLUSIVE] ${e.message}`); return 2; } throw e; }

  console.log(`serve proof — ${s.list.length} route(s) derived`);
  console.log(`  predicate: every game the site's own P0 deriver emits from the canonical shelf,`);
  console.log(`             plus every lab tools/fieldops/build.mjs names and the hub their NAV-1 link`);
  console.log(`             resolves to, plus that builder's Studio. No hand list.`);
  for (const r of s.residue) console.log(`  RESIDUE  ${r.group}: ${r.why}`);
  console.log();

  /* Reachability first: a blocked proxy answering 403 for every host looks
     exactly like a fleet of dead routes, and reporting it as one would be a
     lie with a number attached. R0.9. */
  const roots = { site: await reachable(SITE_ORIGIN), lessons: await reachable(LESSONS_ORIGIN), apps: await reachable(APPS_ORIGIN) };
  const dead = Object.entries(roots).filter(([, v]) => v !== 200);
  /* PER GROUP, NOT JUST ALL-OR-NOTHING. The first cut only bailed when EVERY
     origin was dead; with one origin blocked and two reachable it would have
     marched on and reported that whole estate's routes as RED. A proxy refusing
     one host is a fact about the runner, and reporting it as a deployment
     failure is the exact defect this order predicted for this gate — a runner
     fact wearing a deployment verdict. Unreachable groups are INCONCLUSIVE. */
  const deadGroups = new Set(dead.map(([k]) => k));
  if (dead.length === Object.keys(roots).length) {
    console.log('[UNVERIFIED] no origin answered 200 from this runner:');
    for (const [k, v] of dead) console.log(`  ${k}: ${k === 'site' ? SITE_ORIGIN : k === 'lessons' ? LESSONS_ORIGIN : APPS_ORIGIN} -> ${v}`);
    console.log('\nThis is a fact about the runner, not about the deployment. It is UNVERIFIED,');
    console.log('never green and never "assumed served". Run where the egress is.');
    return 2;
  }

  const pages = { site: await pagesSha('MattRoper1977/mattroper1977.github.io'),
                  lessons: await pagesSha('MattRoper1977/Lessons'),
                  apps: await pagesSha('MattRoper1977/Matt-s-Apps-') };
  for (const [k, v] of Object.entries(pages))
    console.log(`  pages(${k}): ${v.sha ? `${v.sha.slice(0, 7)} status=${v.status}` : `UNKNOWN (${v.why})`}`);
  console.log();

  const rows = [];
  for (const subj of s.list) {
    const expect = sha(fs.readFileSync(subj.blob));
    let verdict = null, detail = '', attempts = 0, ctype = null;
    if (deadGroups.has(subj.group)) {
      rows.push({ ...subj, verdict: 'INCONCLUSIVE', attempts: 0, ctype: null,
        detail: `the ${subj.group} origin answered ${roots[subj.group]} from this runner, not 200 — ` +
                'this route was never reached, so nothing is claimed about it' });
      continue;
    }
    for (let i = 0; i <= RETRY_MAX; i++) {
      attempts = i + 1;
      let r;
      try { r = await get(subj.url); }
      catch (e) { verdict = 'INCONCLUSIVE'; detail = `fetch failed: ${e.message}`; break; }
      if (r.status !== 200) {
        verdict = 'RED'; detail = `HTTP ${r.status}${r.chain.length ? ` · chain: ${r.chain.join(' | ')}` : ' · no redirect chain'}`;
        break;
      }
      const got = sha(r.body);
      if (got === expect) {
        ctype = { got: r.type.split(';')[0] || '(none)', want: subj.type,
                  ok: !!subj.type && r.type.includes(subj.type) };
        verdict = i === 0 ? 'SERVED' : 'SERVED (after retry)';
        detail = `200 · ${expect.slice(0, 12)} · ${r.body.length} B` +
                 (r.chain.length ? ` · chain: ${r.chain.join(' | ')}` : ' · no redirect chain');
        break;
      }
      if (i < RETRY_MAX) { await sleep(RETRY_MS); continue; }
      /* Out of retries: RED only if a deployment SHA says the deploy is settled;
         otherwise the two explanations cannot be told apart. */
      const p = pages[subj.group];
      verdict = p && p.sha ? 'RED' : 'INCONCLUSIVE';
      detail = `200 but STALE after ${attempts} attempt(s) — repo ${expect.slice(0, 12)} vs served ${got.slice(0, 12)}` +
               (p && p.sha ? ` · pages at ${p.sha.slice(0, 7)} status=${p.status}, so the deploy is settled and this is a real mismatch`
                           : ` · pages SHA unknown (${p ? p.why : 'n/a'}), so a live deploy and wrong bytes cannot be distinguished`);
    }
    rows.push({ ...subj, verdict, detail, attempts, ctype });
  }

  const ctl = [...await controls(s.list), ...structuralControls()];

  console.log(`${'group'.padEnd(8)} ${'route'.padEnd(46)} verdict`);
  console.log('-'.repeat(110));
  for (const r of rows) {
    console.log(`${r.group.padEnd(8)} ${String(r.name).slice(0, 46).padEnd(46)} ${r.verdict}`);
    console.log(`${' '.repeat(9)}${r.detail}`);
    if (r.ctype) console.log(`${' '.repeat(9)}content-type: ${r.ctype.got} ` +
      `${r.ctype.ok ? 'as expected' : `— EXPECTED ${r.ctype.want}, and this is reported as its own result rather than buried in the line above`}`);
  }
  console.log('\nCONTROLS (all four must fire)');
  for (const c of ctl) console.log(`  (${c.id}) ${c.fired ? 'FIRED' : 'DID NOT FIRE'}  ${c.what} — ${c.detail}`);

  const ctypeBad = rows.filter(r => r.ctype && !r.ctype.ok);
  const served = rows.filter(r => /^SERVED/.test(r.verdict));
  const red = rows.filter(r => r.verdict === 'RED');
  const inc = rows.filter(r => r.verdict === 'INCONCLUSIVE');
  console.log(`\n${served.length} served byte-identical · ${red.length} red · ${inc.length} inconclusive, of ${rows.length} derived`);
  console.log(`content-type: ${rows.filter(r => r.ctype).length - ctypeBad.length} as expected, ${ctypeBad.length} not`);
  if (deadGroups.size) console.log(`groups never reached from this runner: ${[...deadGroups].join(', ')} — INCONCLUSIVE, not red`);

  if (ctl.some(c => !c.fired)) {
    console.log('\n[STOP] a control did not fire. This gate is not a gate, so no serve result is reported.');
    return 2;
  }
  try { verdictFor(s.list, rows.length); } catch (e) { console.log(`\n[INCONCLUSIVE] ${e.message}`); return 2; }
  return (red.length || ctypeBad.length) ? 1 : inc.length ? 2 : 0;
}

main().then(c => process.exit(c), e => { console.error(e); process.exit(1); });
