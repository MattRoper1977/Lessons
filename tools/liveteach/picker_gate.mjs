/* The P2 gate: the no-immediate-repeat guarantee is structural, so prove it
   at scale rather than sampling it. 10,000 draws, zero repeats, and a
   long-run call balance inside tolerance — plus the red controls that show
   this gate would have caught the fragment's min-weight floor.

     node tools/liveteach/picker_gate.mjs             gate the engine
     node tools/liveteach/picker_gate.mjs --self-test prove the gate can fail */
import { createRequire } from 'node:module';
import path from 'node:path';
const require = createRequire(import.meta.url);
const HERE = path.dirname(new URL(import.meta.url).pathname);
const LTPick = require(path.join(HERE, 'picker_source.js'));

let bad = 0;
const say = (ok, label, detail) => {
  console.log((ok ? 'PASS' : 'FAILED') + '  ' + label + (ok || !detail ? '' : ' — ' + detail));
  if (!ok) bad++;
};

/* A seeded PRNG: the run must be reproducible, so a failure can be examined
   rather than chased. (mulberry32) */
function rng(seed) {
  let a = seed >>> 0;
  return function () {
    a = (a + 0x6D2B79F5) >>> 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const ROSTER = Array.from({ length: 12 }, (_, i) => 'Pupil ' + String.fromCharCode(65 + i));
const DRAWS = 10000;

function run(roster, draws, seed, mode) {
  const st = LTPick.create(roster);
  const r = rng(seed);
  const counts = new Map(roster.map(n => [n, 0]));
  let repeats = 0, prev = null, fellBack = 0;
  for (let i = 0; i < draws; i++) {
    const got = mode === 'pass' && i % 4 === 3 ? LTPick.pass(st, r) : LTPick.pick(st, r);
    if (!got) break;
    if (got.fellBack) fellBack++;
    if (prev !== null && got.name === prev) repeats++;
    counts.set(got.name, counts.get(got.name) + 1);
    prev = got.name;
  }
  return { counts, repeats, fellBack, st };
}

if (process.argv[2] === '--self-test') {
  /* RED 1 — the fragment's own defect, rebuilt: a minimum weight floor lets
     the pupil who just answered come straight back up. If this gate cannot
     see that, it is not a gate. */
  const MIN_W = 0.05;
  const names = ROSTER.slice();
  const since = names.map(() => 1);
  const r = rng(7);
  let repeats = 0, prev = null;
  for (let i = 0; i < DRAWS; i++) {
    const w = since.map(s => Math.max(MIN_W, s));   // <- the floor, exactly as reviewed
    const total = w.reduce((a, b) => a + b, 0);
    let t = r() * total, idx = w.length - 1;
    for (let j = 0; j < w.length; j++) { t -= w[j]; if (t < 0) { idx = j; break; } }
    for (let m = 0; m < since.length; m++) since[m]++;
    since[idx] = 0;
    if (prev === names[idx]) repeats++;
    prev = names[idx];
  }
  say(repeats > 0, 'RED: a min-weight floor DOES produce immediate repeats, and this gate counts them', 'repeats=' + repeats);
  console.log('        (the reviewed fragment\'s floor gave ' + repeats + ' back-to-back calls in ' + DRAWS + ' draws — ' + (100 * repeats / DRAWS).toFixed(2) + '%)');

  /* RED 2 — a deliberately biased engine must fail the balance tolerance,
     so a passing balance check means something. */
  const biased = new Map(ROSTER.map(n => [n, 0]));
  const rb = rng(3);
  for (let i = 0; i < DRAWS; i++) {
    const k = rb() < 0.5 ? ROSTER[0] : ROSTER[1 + Math.floor(rb() * (ROSTER.length - 1))];
    biased.set(k, biased.get(k) + 1);
  }
  const bVals = [...biased.values()];
  const bExpect = DRAWS / ROSTER.length;
  const bWorst = Math.max(...bVals.map(v => Math.abs(v - bExpect) / bExpect));
  say(bWorst > 0.15, 'RED: a biased draw blows the balance tolerance this gate applies', 'worst deviation ' + (bWorst * 100).toFixed(1) + '%');

  /* RED 3 — the attendance hole itself, rebuilt. Re-introduce BOTH halves of
     the original defect (clear `last` when a pupil is marked away, and let a
     returning pupil keep a frozen zero) and demand the churn fuzz catches
     it. Without this the churn checks could be passing for the wrong reason. */
  const brokenSrc = require('node:fs').readFileSync(path.join(HERE, 'picker_source.js'), 'utf8')
    .replace(/if \(st\.present\[i\] && !was && st\.since\[i\] < 1\) st\.since\[i\] = 1;/,
             'if (!st.present[i] && st.last === i) st.last = -1;')
    .replace(/var eligible = present\.filter\(function \(i\) \{ return i !== st\.last && i !== st\.justPassed; \}\);/,
             'var eligible = present.slice();');
  const bmod = { exports: {} };
  new Function('module', 'exports', 'self', brokenSrc)(bmod, bmod.exports, undefined);
  const BROKEN = bmod.exports;
  say(BROKEN !== LTPick && typeof BROKEN.pick === 'function', 'setup: the broken engine rebuilt for the control');
  let brokenAvoidable = 0;
  {
    const st = BROKEN.create(ROSTER.slice(0, 3));
    const r = rng(4245);
    let prev = null;
    for (let i = 0; i < 4000; i++) {
      if (r() < 0.34) {
        const who = r() < 0.5 && st.last >= 0 ? st.last : Math.floor(r() * 3);
        BROKEN.setPresent(st, who, !st.present[who]);
      }
      if (!st.present.some(Boolean)) BROKEN.setPresent(st, Math.floor(r() * 3), true);
      const others = st.present.filter((p, idx) => p && st.names[idx] !== prev).length;
      const got = BROKEN.pick(st, r);
      if (!got) continue;
      if (prev !== null && got.name === prev && others > 0) brokenAvoidable++;
      prev = got.name;
    }
  }
  say(brokenAvoidable > 0, 'RED: the ORIGINAL attendance hole produces avoidable repeats, and the churn fuzz counts them', 'avoidable=' + brokenAvoidable);
  console.log('        (the pre-fix engine repeated an already-answered pupil ' + brokenAvoidable + ' times in 4000 churned draws)');

  /* RED 4 — absence must actually remove someone from the draw. */
  const st = LTPick.create(ROSTER);
  LTPick.setPresent(st, 3, false);
  const rr = rng(11);
  let sawAbsent = false;
  for (let i = 0; i < 500; i++) { const g = LTPick.pick(st, rr); if (g && g.index === 3) sawAbsent = true; }
  say(!sawAbsent, 'RED control: an absent pupil is never drawn in 500 draws');

  console.log(bad ? '[SELF-TEST] FAIL' : '[SELF-TEST] PASS');
  process.exit(bad ? 1 : 0);
}

/* ---- the gate proper ---- */
const main = run(ROSTER, DRAWS, 20260826, 'pick');
say(main.repeats === 0, 'P2: zero immediate repeats across ' + DRAWS + ' draws (12 present)', 'repeats=' + main.repeats);
say(main.fellBack === 0, 'P2: the guarantee never had to degrade with a full room', 'fellBack=' + main.fellBack);

const vals = [...main.counts.values()];
const expect = DRAWS / ROSTER.length;
const worst = Math.max(...vals.map(v => Math.abs(v - expect) / expect));
/* 8%, not 15%. The engine's own spread across seeds measures under ~4.5%, so
   a 15% band sat about five times above the noise it was meant to police and
   would have passed a real weighting bias. And one seed is not a
   distribution: the same shape runs across six. */
const TOL = 0.08;
say(worst <= TOL, 'long-run balance: every pupil called within 8% of an even share', 'worst deviation ' + (worst * 100).toFixed(2) + '% (min ' + Math.min(...vals) + ', max ' + Math.max(...vals) + ', even ' + expect + ')');
console.log('        call spread: min ' + Math.min(...vals) + ' / max ' + Math.max(...vals) + ' / even ' + expect + ' — worst deviation ' + (worst * 100).toFixed(2) + '%');
let worstAcross = 0;
for (const seed of [1, 7, 101, 5150, 90210, 31337]) {
  const s2 = run(ROSTER, 6000, seed, 'pick');
  const v2 = [...s2.counts.values()];
  const e2 = 6000 / ROSTER.length;
  const w2 = Math.max(...v2.map(v => Math.abs(v - e2) / e2));
  worstAcross = Math.max(worstAcross, w2);
  if (s2.repeats) say(false, 'seed ' + seed + ': zero repeats', 'repeats=' + s2.repeats);
}
say(worstAcross <= TOL, 'balance holds across six independent seeds, not just the one', 'worst across seeds ' + (worstAcross * 100).toFixed(2) + '%');

/* Passing must not become an escape route: a pupil who passes every time
   should still be asked about as often as everyone else. */
const withPass = run(ROSTER, DRAWS, 555, 'pass');
say(withPass.repeats === 0, 'P2: zero immediate repeats when a quarter of turns are passed', 'repeats=' + withPass.repeats);
const pVals = [...withPass.counts.values()];
const pWorst = Math.max(...pVals.map(v => Math.abs(v - DRAWS / ROSTER.length) / (DRAWS / ROSTER.length)));
say(pWorst <= 0.15, 'passing is a scaffold, not an exit: balance holds with passes mixed in', 'worst deviation ' + (pWorst * 100).toFixed(2) + '%');

/* Small rooms: the SEMH reality is four pupils some days. The guarantee must
   hold down to two, and degrade openly at one. */
for (const n of [2, 3, 4, 6]) {
  const small = run(ROSTER.slice(0, n), 2000, 99 + n, 'pick');
  say(small.repeats === 0, 'P2 holds in a room of ' + n, 'repeats=' + small.repeats);
}
const solo = run(ROSTER.slice(0, 1), 50, 5, 'pick');
/* The very first draw needs no fallback (nobody has been called yet), so 49
   of 50 are flagged — every draw where the guarantee genuinely could not
   hold, and none where it could. */
say(solo.repeats === 49 && solo.fellBack === 49, 'one pupil present: the guard degrades OPENLY (flagged on every draw it could not cover) rather than pretending', JSON.stringify({ repeats: solo.repeats, fellBack: solo.fellBack }));

/* THE ATTENDANCE HOLE (found by review, reproduced, fixed). `since` only
   advances for pupils who are here, so a pupil marked away just after being
   called kept since=0 — and a frozen zero never expires. Returning with it
   made them weightless, which in a small room emptied the pool into the
   uniform fallback and let the pupil who had just answered be drawn again.
   Attendance churn is now fuzzed hard, in the small rooms where it bites. */
for (const n of [2, 3, 4, 8]) {
  const st = LTPick.create(ROSTER.slice(0, n));
  const r = rng(4242 + n);
  let prev = null, avoidable = 0, churns = 0, conceded = 0, lied = 0;
  for (let i = 0; i < 4000; i++) {
    // flip somebody's attendance about a third of the time, including the
    // pupil who has just been called — the exact move that broke it.
    if (r() < 0.34) {
      const who = r() < 0.5 && st.last >= 0 ? st.last : Math.floor(r() * n);
      LTPick.setPresent(st, who, !st.present[who]);
      churns++;
    }
    if (!st.present.some(Boolean)) { LTPick.setPresent(st, Math.floor(r() * n), true); }
    /* Work out, BEFORE the draw, whether a repeat was avoidable: was anyone
       other than the pupil who just answered actually in the room? That is
       the true invariant — a repeat is a defect only when someone else
       could have been asked. */
    const others = st.present.filter((p, idx) => p && st.names[idx] !== prev).length;
    const got = LTPick.pick(st, r);
    if (!got) continue;
    if (got.fellBack) {
      conceded++;
      if (others > 0) lied++;      // claimed it had no choice while it did
    }
    if (prev !== null && got.name === prev && others > 0) avoidable++;
    prev = got.name;
  }
  say(avoidable === 0, 'P2 survives attendance churn in a room of ' + n + ': no AVOIDABLE repeat in 4000 draws (' + churns + ' flips)', 'avoidable=' + avoidable);
  say(lied === 0, 'and it never claims it had no choice while someone else was in the room (room of ' + n + ')', 'false concessions=' + lied + ' of ' + conceded);
}

/* A returning pupil must come back into the pool, not sit weightless. */
const ret = LTPick.create(ROSTER.slice(0, 4));
const rr2 = rng(77);
LTPick.pick(ret, rr2);
const justCalled = ret.last;
LTPick.setPresent(ret, justCalled, false);
LTPick.setPresent(ret, justCalled, true);
say(ret.since[justCalled] >= 1, 'a pupil marked away and straight back re-enters the pool rather than carrying a frozen zero', 'since=' + ret.since[justCalled]);
let sawReturner = false;
for (let i = 0; i < 400; i++) { const g = LTPick.pick(ret, rr2); if (g && g.index === justCalled) sawReturner = true; }
say(sawReturner, 'and they are actually called again afterwards');

/* Attendance mid-lesson: a pupil marked absent stops being drawn from that
   moment, and marking them back present returns them to the room. */
const att = LTPick.create(ROSTER);
const ra = rng(42);
for (let i = 0; i < 200; i++) LTPick.pick(att, ra);
LTPick.setPresent(att, 5, false);
let drewAbsent = 0;
for (let i = 0; i < 2000; i++) { const g = LTPick.pick(att, ra); if (g && g.index === 5) drewAbsent++; }
say(drewAbsent === 0, 'P4: a pupil marked absent mid-lesson is never drawn again', 'drew ' + drewAbsent);
LTPick.setPresent(att, 5, true);
let drewBack = 0;
for (let i = 0; i < 2000; i++) { const g = LTPick.pick(att, ra); if (g && g.index === 5) drewBack++; }
say(drewBack > 0, 'P4: marking them present again returns them to the draw', 'drew ' + drewBack);

/* The probability view must sum to 1 over eligible pupils and report absent
   pupils at zero — the numbers the teacher reads have to be the numbers the
   engine uses. */
const pst = LTPick.create(ROSTER);
LTPick.setPresent(pst, 2, false);
LTPick.pick(pst, rng(8));
const rows = LTPick.probabilities(pst);
const sum = rows.reduce((a, r) => a + r.p, 0);
say(Math.abs(sum - 1) < 1e-9, 'P3/P4: displayed probabilities sum to exactly 1', String(sum));
say(rows[2].p === 0 && rows[2].present === false, 'P4: the absent pupil is listed at zero, not silently dropped');
say(rows.filter(r => r.cooldown).length === 1, 'P2: exactly one pupil is shown on cooldown after a draw');

/* Roster parsing: a paste from a register, however it is shaped. */
const parsed = LTPick.parseRoster(' Ana ,Ben\nCharlie\n\n Ana \n' + 'x'.repeat(60));
say(parsed.length === 4 && parsed[0] === 'Ana' && parsed[3].length === 32, 'roster parse: commas and newlines both work, duplicates drop, long names clamp', JSON.stringify(parsed.slice(0, 4).map(s => s.slice(0, 8))));
/* DISTINCT names: the old probe pasted the same name eighty times, which the
   dedupe collapsed to one entry before the cap was ever consulted — the
   assertion was 1 <= 40 and passed with the cap deleted. */
const runaway = LTPick.parseRoster(Array.from({ length: 80 }, (_, i) => 'Name' + i).join(','));
say(runaway.length === LTPick.MAX_NAMES, 'roster parse: 80 DISTINCT names are capped at exactly the class-sized limit', 'got ' + runaway.length);

/* Nothing in the engine may reach for storage, the bus, the URL or the log. */
const src = require('node:fs').readFileSync(path.join(HERE, 'picker_source.js'), 'utf8');
/* Comments are stripped first: the file DISCUSSES localStorage in its header
   (to say it never touches it), and a grep that matched prose would go green
   on a promise instead of on the code. */
const code = src.replace(/\/\*[\s\S]*?\*\//g, '').replace(/^\s*\/\/.*$/gm, '');
const forbidden = /localStorage|sessionStorage|BroadcastChannel|postMessage|console\.|location\.|document\./.exec(code);
say(!forbidden, 'D2: the engine CODE touches no storage, no bus, no URL, no console', forbidden && forbidden[0]);
/* And the stripper must be doing real work, or the check above is a tautology
   waiting to happen. */
const canary = /\/\*[\s\S]*?\*\//.test(src) && !/localStorage/.test(code) && /localStorage/.test(src);
say(canary, 'the forbidden-API scan runs on stripped CODE, not on prose that merely mentions the APIs');

console.log(bad ? 'PICKER GATE FAILED (' + bad + ')' : 'PICKER GATE PASSED');
process.exit(bad ? 1 : 0);
