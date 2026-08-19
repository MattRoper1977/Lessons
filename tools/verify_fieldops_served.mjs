/* THE FIELDOPS DECLARATION CHECK.  Offline only, and deliberately so.
 *
 * SUPERSEDED IN PART, 2026-08-17. This began as the FieldOps serve proof. The
 * estate-wide tools/verify_served.mjs now covers all 29 routes — the 23 the
 * site's own P0 deriver emits, these four labs, their hub and the Studio — and
 * it does the network legs correctly, which THIS FILE DID NOT:
 *
 *   it treated any 3xx as a FAIL. On the first live run that called the Teacher
 *   Studio a failure for answering 301, when the 301 is simply the user Pages
 *   site redirecting github.io to the custom domain and the bytes at the far end
 *   are identical. A redirect is not a failure; it is a thing that must never be
 *   silent (the order's words). verify_served.mjs follows it, NAMES the chain,
 *   and compares bytes at the destination — which it did, and the Studio passed.
 *
 * Its network legs are removed rather than fixed, because two tools fetching the
 * same routes with different opinions about redirects is how an estate ends up
 * with a verdict that depends on which gate you ask. The file is kept, not
 * deleted, because its reader census is not empty (R0.16) and because ONE THING
 * HERE IS NOT DUPLICATED ANYWHERE:
 *
 *   D1 — the builder's LABS[] and the placed directory name the same files. A
 *   lab declared and not placed, or placed and not declared, is red before a
 *   single byte is fetched, and that is a check the serve proof cannot make
 *   against itself. Since FieldOps FIX-1 the placed directory also carries an
 *   authored hub the builder does not emit; it is named in PLACED_NON_LAB and
 *   REQUIRED there, so D1 reds if it goes missing as well as if a file the
 *   allowance does not name appears.
 *
 * R0.4 for these routes now lives in tools/verify_served.mjs. So do the base
 * URLs: they were declared here as overridable constants, and they are gone
 * with the fetches, because a URL sitting in a file that never requests it is
 * the next reader's false lead.
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
 * WHAT IS ASSERTED, NOW THAT NOTHING IS FETCHED
 *   the subject set derives from build.mjs rather than a hand-list · every
 *   declared subject has a blob in this checkout · D1, the builder and the
 *   placed directory naming the same files · an empty LABS array is
 *   INCONCLUSIVE and not an empty green pass · the byte comparison can tell one
 *   appended byte apart. That last one is the control on the comparison itself,
 *   kept even though the comparison's only remaining caller is the control.
 *
 *   Three of those are proven by mutation rather than observed passing: a lab
 *   declared and never placed, a file placed and declared nowhere, and the hub
 *   removed — each must red D1 BY NAME. The first rewrites build.mjs, the other
 *   two write and delete inside the placed directory; both records are hashed
 *   before and after and the equality is asserted, never assumed (R0.14).
 *
 * EXITS
 *   0  the declarations agree and the controls fired
 *   1  a subject is declared and not placed, placed and not declared, or has no
 *      blob here to compare against; or the authored hub PLACED_NON_LAB names is
 *      gone from the placed directory
 *   2  INCONCLUSIVE — a record that could not be read, or a subject set that
 *      derived to nothing. Never green: a derivation that yields nothing must
 *      not read as nothing wrong.
 *
 *   node tools/verify_fieldops_served.mjs
 *   node tools/verify_fieldops_served.mjs --self-test   (an alias; identical, and
 *                                                        kept so callers survive)
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const HERE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ARGS = new Set(process.argv.slice(2));

const PLACED = 'Science_Teesside/Build/v4_fieldops';
const STUDIO_REF = 'tools/fieldops/staging/00_BUILD_FieldOps_Teacher_Studio.html';

/* The placed directory also carries one authored file the builder does not emit.
   GitHub Pages serves no directory listing, so until FieldOps FIX-1 (2026-08-19)
   the bare directory URL was a 404 by construction while every lab beneath it
   served — which is how the owner came to have four labs he could not reach.
   index.html is the hub that closes that, and it is REQUIRED rather than merely
   tolerated: delete it and the directory URL 404s again, so D1 names it missing.
   Everything else in this directory is still red, which C4 below proves. */
const PLACED_NON_LAB = ['index.html'];

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

  const required = [...LABS, ...PLACED_NON_LAB];
  const missing = required.filter(l => !placed.includes(l));
  const extra = placed.filter(p => !required.includes(p));
  row('D1', missing.length || extra.length ? 'FAIL' : 'PASS',
      'the builder\'s LABS and the placed directory name the same files',
      `declared ${LABS.length} lab(s) + ${PLACED_NON_LAB.length} authored ` +
      `(${PLACED_NON_LAB.join(', ')}), placed ${placed.length}` +
      (missing.length ? ` · required but not placed: ${missing.join(', ')}` : '') +
      (extra.length ? ` · placed but not declared: ${extra.join(', ')}` : ''));

  const list = LABS.map(name => ({
    name, kind: 'lab', local: path.join(HERE, PLACED, name),
  }));
  /* The Studio's bytes live in the Apps repository, which this checkout does
     not contain. The blob named here is the staging build, which the merge
     proved byte-identical to the placed file — so the Studio is still a
     declared subject with something local to stand behind it. */
  list.push({ name: STUDIO, kind: 'studio', local: path.join(HERE, STUDIO_REF) });
  return list;
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

  /* Two mutations, both against build.mjs, both restored in a finally.
     R0.15: D1 is now the only thing this file checks that nothing else checks,
     and until August 2026 the only evidence for it was that it said PASS. A
     check observed passing has not been shown able to fail. */
  const BUILD = path.join(HERE, 'tools/fieldops/build.mjs');
  const saved = fs.readFileSync(BUILD, 'utf8');
  /* R0.14 applied to this harness. Both mutations below rewrite a shipped file
     and restore it in a `finally` — and a `finally` that is believed rather
     than measured is the same species as every other unfired check in this
     ledger. The builder is hashed before and after, and the equality is
     asserted, not assumed. */
  const buildShaBefore = sha(Buffer.from(saved));
  const withBuild = (src, fn) => {
    try { fs.writeFileSync(BUILD, src); return fn(); }
    finally { fs.writeFileSync(BUILD, saved); }
  };

  /* A derivation that yields nothing must be INCONCLUSIVE, not green. */
  withBuild("const LABS = [];\nconst STUDIO = 'x';\nswap('T1');\n", () => {
    let fired = false;
    try { subjects(); } catch (e) { fired = e instanceof Inconclusive; }
    check('an empty LABS array is INCONCLUSIVE, never an empty green pass', fired);
  });

  /* CONTROL — declare a lab that was never placed. D1 must name it. Mutating
     the builder rather than the directory is deliberate: deleting a placed lab
     to prove a point is a destructive check on a shipped file (R0.14), and this
     reaches the same verdict without touching one. */
  withBuild(saved.replace(/(const LABS\s*=\s*\[)/,
                          "$1\n  'ZZ_declared_and_never_placed.html',"), () => {
    const before = rows.length;
    let d1;
    try { subjects(); d1 = rows.slice(before).find(r => r.id === 'D1'); }
    catch (_) { /* leave d1 undefined: an exception is not the verdict D1 owes */ }
    check('CONTROL: a lab declared and not placed reds D1, by name',
          d1?.verdict === 'FAIL' && /ZZ_declared_and_never_placed\.html/.test(d1.detail),
          d1 ? d1.detail : 'D1 produced no row at all — the mutation was inert');
    rows.length = before;                 // the control's rows are not findings
  });

  /* R0.1 for the widening FieldOps FIX-1 made. D1 stopped being "LABS equals the
     directory" the moment an authored hub was placed beside the labs, and a
     tolerance that has only ever been observed passing is the exact species of
     unfired check this ledger exists to catch. Both limbs of the new rule are
     mutated here — a stray file the allowance does not name, and the allowance's
     own file removed — against the placed directory rather than the builder,
     because that is the record each limb is about. R0.14: the directory is
     hashed by name and bytes before and after, and the equality is asserted. */
  const PDIR = path.join(HERE, PLACED);
  const dirState = () => fs.readdirSync(PDIR).sort()
    .map(f => `${f}:${sha(fs.readFileSync(path.join(PDIR, f)))}`).join('\n');
  const dirBefore = dirState();
  const withPlaced = (mutate, restore, fn) => {
    try { mutate(); return fn(); } finally { restore(); }
  };
  const d1After = () => {
    const before = rows.length;
    let d1;
    try { subjects(); d1 = rows.slice(before).find(r => r.id === 'D1'); } catch (_) {}
    rows.length = before;                   // the control's rows are not findings
    return d1;
  };

  /* CONTROL C4 — a file placed and named by neither record. The allowance names
     index.html and nothing else, so this must still be red, by name. */
  const STRAY = path.join(PDIR, 'ZZ_placed_and_never_declared.html');
  withPlaced(() => fs.writeFileSync(STRAY, '<!doctype html><title>stray</title>'),
             () => { if (fs.existsSync(STRAY)) fs.unlinkSync(STRAY); }, () => {
    const d1 = d1After();
    check('CONTROL: a file placed and declared nowhere still reds D1, by name',
          d1?.verdict === 'FAIL' && /ZZ_placed_and_never_declared\.html/.test(d1.detail),
          d1 ? d1.detail : 'D1 produced no row at all — the mutation was inert');
  });

  /* CONTROL C5 — the hub removed. PLACED_NON_LAB is a requirement, not a
     tolerance: without index.html the directory URL 404s again, which is the
     defect FIX-1 closed, so D1 owes a red naming it. */
  const HUB = path.join(PDIR, PLACED_NON_LAB[0]);
  const hubBytes = fs.existsSync(HUB) ? fs.readFileSync(HUB) : null;
  withPlaced(() => { if (hubBytes) fs.unlinkSync(HUB); },
             () => { if (hubBytes) fs.writeFileSync(HUB, hubBytes); }, () => {
    const d1 = d1After();
    check('CONTROL: the hub removed reds D1 — it is required, not tolerated',
          hubBytes !== null && d1?.verdict === 'FAIL' &&
          new RegExp(`required but not placed: .*${PLACED_NON_LAB[0].replace('.', '\\.')}`).test(d1.detail),
          hubBytes === null ? `${PLACED_NON_LAB[0]} is not placed at all — nothing to remove`
                            : (d1 ? d1.detail : 'D1 produced no row at all — the mutation was inert'));
  });

  const dirAfter = dirState();
  check('the placed directory is byte-identical after the mutations that wrote it',
        dirAfter === dirBefore,
        dirAfter === dirBefore ? `${fs.readdirSync(PDIR).length} file(s), unchanged`
                               : 'THE PLACED DIRECTORY WAS LEFT MUTATED');

  /* And the hash comparison itself, exercised without a server. */
  const a = fs.readFileSync(list[0].local);
  check('the byte comparison distinguishes one appended byte',
        sha(a) !== sha(Buffer.concat([a, Buffer.from('x')])));

  /* The restore, measured. This runs LAST, after every mutation above, and it
     is the check that makes the two destructive controls safe to ship. */
  const buildShaAfter = sha(fs.readFileSync(BUILD));
  check('the builder is byte-identical after the mutations that rewrote it',
        buildShaAfter === buildShaBefore,
        `before ${buildShaBefore.slice(0, 12)} · after ${buildShaAfter.slice(0, 12)}` +
        (buildShaAfter === buildShaBefore ? '' : ' — A SHIPPED FILE WAS LEFT MUTATED'));

  console.log(`\n[OFFLINE] ${fails === 0 ? 'PASS' : 'FAIL'} — ${fails} check(s) failed`);
  return fails === 0 ? 0 : 1;
}

/* ------------------------------------------------------------------ main */
/* There is no network path any more. Running this bare runs the declaration
   checks; --self-test is kept as an alias so existing callers do not break. */
try {
  const code = selfTest();
  console.log('\nThe live serve proof for these routes is tools/verify_served.mjs,');
  console.log('which follows redirects, names the chain and compares bytes at the');
  console.log('destination. This file no longer fetches anything.');
  process.exit(code);
} catch (e) {
  if (e instanceof Inconclusive) { console.log(`[INCONCLUSIVE] ${e.message}`); process.exit(2); }
  throw e;
}
