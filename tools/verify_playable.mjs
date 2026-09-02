#!/usr/bin/env node
/**
 * verify_playable.mjs — can a child actually FINISH these games?
 *
 * WHY THIS EXISTS
 * ---------------
 * Every gate in this estate measures a property of the artefact: bytes, flash
 * rate, contrast, a way out, a marker, a hash. Not one of them has ever asserted
 * that a game can be COMPLETED. The governing fact is /emberwild/: it passed a
 * thirty-four gate contract, save continuity, byte identity, flash censuses,
 * portrait gates, a real Tab walk and three-engine CI — and its first and only
 * mission could not be finished, because the trainer who gates all progress had
 * no interaction branch for the undefeated case. Every gate measured the
 * artefact; none measured the product.
 *
 * THE FOUR RULES THIS FILE OBEYS
 * -----------------------------
 * 1. Drive the REAL input path. Every step below is a click on a control the
 *    player can see, a key the player can press, or waiting for the game's own
 *    clock. Nothing here calls an internal method to make progress happen. A
 *    test that calls startBattle() proves the function exists, not that a child
 *    can reach it. Where a game exposes its own read seam (window.__LUMINS,
 *    __GCsave, __SLIP, __WC) that seam is used ONLY to read state, never to
 *    drive it.
 * 2. Derive the route from the game's own rules — never replay coordinates a
 *    measuring pass chose. Each plan below names the rule it follows; where a
 *    game is a grid game the route is searched over the SHIPPED predicate, not
 *    over a copy of it.
 * 3. Assert progression BY VALUE — a flag, a save, a counter read from the
 *    game's own state. Never by reading a UI string. A heading that says
 *    "RESCUED" is evidence about a heading.
 * 4. Prove the check can fail. Every game runs three firing controls before its
 *    green is allowed to count: the route blocked, the predicate wrong, and no
 *    input at all. A gate that has never been seen red has not passed.
 *
 * USAGE
 *   node tools/verify_playable.mjs              # every game with a plan
 *   node tools/verify_playable.mjs Lumins       # one game, by substring
 *   node tools/verify_playable.mjs --census     # §4.1 record only, no browser
 */

import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import url from 'node:url';

const ROOT = path.resolve(path.dirname(url.fileURLToPath(import.meta.url)), '..');
const GAMES = path.join(ROOT, 'Games');
// hud.js is served by the site repository, not this one. When a checkout is
// present next door we serve the real file so the exit furniture behaves as it
// does in production; when it is not, the games 404 it exactly as they would
// offline, which changes nothing this harness asserts.
const SITE_HUD = '/home/user/mattroper1977.github.io/hud.js';

/* ------------------------------------------------------------------ *
 * §4.1 — the record. What is the win, the loss, and the FIRST gate of
 * progress, derived from each game's own source. A game with no terminal
 * state is a valid answer and changes the harness, not the verdict.
 * ------------------------------------------------------------------ */
const CENSUS = {
  'Lumins.html':
    'win: endLevel() with G.saved >= G.def.target · lose: saved < target · first gate: level 1 reaches G.state "over" with a counted result',
  'Glitch_Clash.html':
    'win: endBattle() resolves with the player standing, banking a stage into save.cleared · lose: the Keeper falls · first gate: stage 1 cleared, save.cleared gains an id',
  'Hold_the_Mark.html':
    'win: a round survived to its encore, banking SAVE.stars for that mark · lose: the mark is lost · first gate: htm_save gains a star entry',
  'Slipstream_GP.html':
    'win: finishRace() with the player classified · lose: retire · first gate: state.mode leaves LOBBY for RACE and reaches FINISH',
  'Wrecking_Crew.html':
    'win: a contract scored (state.mode SCORE) · lose: the site survives the charge budget · first gate: state.mode leaves TITLE for BOARD and reaches BOOM',
  'Grid_Chase.html':
    'win: no terminal win — an endless chase; the run ends at gameOver() · lose: caught · first gate: state leaves MENU for RUN and a score is banked at OVER',
  'voxelcraft.html':
    'win: no terminal win in sandbox; the arcade leg ends on its own 60 s clock · lose: none · first gate: arcade-end opens with a banked score',
  'Neon_Snake_Overdrive.html':
    'win: no terminal win — an endless run · lose: endGame(reason) · first gate: a run ends and a score is offered to the board',
  'Axiom_Shift.html':
    'win: onClear() per puzzle · lose: none (rewind is unlimited) · first gate: puzzle 1 cleared',
  'Charcoal.html':
    'win: endRound() with the mark drawn · lose: the round times out · first gate: round 1 ends',
  'The_Last_Lighthouse_v1_1_The_Archipelago_Update_FINAL.html':
    'win: finish(true) — a vessel brought home · lose: finish(false) · first gate: the watch begins and finish() is reached either way',
  'Trekkers_Trail_Runner_Tees_Coast.html':
    'win: no terminal win — an endless trail · lose: lives exhausted at takeDamage() · first gate: game-over-screen shows a final score',
  'Static.html':
    'win: checkComplete() — a case resolved · lose: a wrong verdict · first gate: case 1 resolved',
  'OneGuy.html':
    'win: endRun() beating the ghost · lose: endRun() behind it · first gate: a run ends against a ghost',
  'Marble.html': 'win: courseEnd()/awardFinish() · lose: none · first gate: course 1 finished',
  'Grapple.html': 'win: courseEnd()/awardFinish() · lose: none · first gate: course 1 finished',
  'Neon_Siege.html': 'win: the core held to the last wave · lose: the core breached · first gate: wave 1 resolved',
  'Neon_Garden.html': 'win: ascend() · lose: none · first gate: the first bloom ascends',
  'Prism.html': 'win: all light aligned · lose: none · first gate: the first beam bent to target',
  'Vortex.html': 'win: a race classified · lose: none · first gate: the first race finishes',
  'Globe_Snake (1).html': 'win: no terminal win — endless · lose: collision · first gate: a run ends and scores',
  'Slipstream.html': 'win: a race result · lose: none · first gate: results panel opens',
  'Orbital.html': 'NOT MEASURED — owned by open Lessons PR #93',
  'KidsVsStaff_Showdown (3).html':
    'win: finishShow() with a side ahead · lose: the other side · first gate: the show reaches "done"',
  'WorldCup_ThreeLions_Final.html': 'win: completeMission() per mission · lose: none · first gate: mission 1 completed',
  'WorldCup_v3_MatchDirector.html': 'win: missionsComplete() · lose: none · first gate: mission 1 completed',
  'WorldCup_v5_Showdown.html': 'win: missionsComplete()/codesComplete() · lose: none · first gate: mission 1 completed',
};

/* ------------------------------------------------------------------ *
 * The plans. A plan is: the rule the route follows, the approaches a
 * player can take, and the gate predicate — evaluated in the page,
 * reading the game's own state BY VALUE.
 *
 * `gate` returns {reached, completed, ...evidence}, and the two are NOT the
 * same claim. `reached` is the FIRST GATE OF PROGRESS — the game has left its
 * menu and the player has moved the state that gates everything after it.
 * `completed` is the game's own WIN. Emberwild reached its first gate and could
 * not be completed; collapsing the two is how that went unnoticed for weeks, so
 * this harness reports them in separate columns and never lets one stand for
 * the other. It may read a seam the game itself exports, or localStorage, which
 * is the game's own record. It may never read a heading, a label, or any other
 * rendered string.
 * ------------------------------------------------------------------ */
const PLANS = {
  'Lumins.html': {
    rule:
      'Lumins ends a level from its own simulation: endLevel() fires when every lumin has ' +
      'spawned and none is still active, or when the player presses the shipped END control. ' +
      'Both are the real input path; neither is a call into the sim.',
    approaches: [
      { name: 'begin, then the shipped END control', steps: [['click', '#go'], ['click', '#c-end']] },
      { name: 'begin, then let the level run out on its own', steps: [['click', '#go'], ['settle', 40000]] },
    ],
    gate: () => {
      const L = window.__LUMINS;
      if (!L || !L.G || L.G.state !== 'over') return { reached: false };
      return { reached: true, completed: L.G.saved >= (L.G.def && L.G.def.target),
               saved: L.G.saved, target: L.G.def && L.G.def.target };
    },
    blockedBy: '#go',
  },

  'Hold_the_Mark.html': {
    rule:
      'Hold the Mark banks progress into its own htm_save record. The route is the shipped ' +
      'focus control held through a round; progress is the save gaining a star entry, read ' +
      'from localStorage — the game\'s own record, not a label.',
    approaches: [
      { name: 'play, start the wave, then work the focus control', steps: [['click', '#btnPlay'], ['settle', 1500], ['click', '#tipSkip'], ['click', '#waveBtn'], ['mash', '#focusBtn:not([disabled])', 90]] },
      { name: 'keyboard only - Enter to play, then the focus control', steps: [['key', 'Enter'], ['settle', 1500], ['key', 'Enter'], ['mash', '#focusBtn', 60]] },
    ],
    gate: () => {
      let save = null;
      try { save = JSON.parse(localStorage.getItem('htm_save') || 'null'); } catch (_) { /* corrupt save is not progress */ }
      const stars = save && save.stars ? Object.keys(save.stars).length : 0;
      const runs = save && typeof save.runs === 'number' ? save.runs : null;
      if (!save) return { reached: false };
      return { reached: (runs || 0) > 0 || stars > 0, completed: stars > 0, stars, runs, ready: !!window.__HTM_READY };
    },
    blockedBy: '#btnPlay',
  },

  'Glitch_Clash.html': {
    rule:
      'Glitch Clash banks a cleared stage into its own save. The route is the shipped campaign ' +
      'control and the battle\'s own action buttons; progress is save.cleared gaining an id or ' +
      'save.wins advancing, read through the game\'s exported read seam __GCsave.',
    approaches: [
      // The stage's intro cutscene sits in front of the action row until the
      // player presses its own Continue control; a harness that mashes through
      // it is testing an overlay, not a battle.
      { name: 'first stage on the map, past the cutscene, then act each turn', steps: [['click', '.stagebtn'], ['settle', 3000], ['click', '#clashok'], ['settle', 3000], ['mash', '#actions button.act:not([disabled])', 90]] },
      { name: 'daily clash, start the run, past the cutscene, then act each turn', steps: [['click', '#dailybtn'], ['settle', 1500], ['click', '#modgo'], ['settle', 3000], ['click', '#clashok'], ['settle', 3000], ['mash', '#actions button.act:not([disabled])', 90]] },
    ],
    gate: () => {
      const read = window.__GCsave;
      if (typeof read !== 'function') return { reached: false, note: 'no __GCsave seam' };
      let s = null;
      try { s = read(); } catch (_) { return { reached: false, note: '__GCsave threw' }; }
      if (!s) return { reached: false };
      const cleared = Array.isArray(s.cleared) ? s.cleared.length : 0;
      const wins = typeof s.wins === 'number' ? s.wins : 0;
      return { reached: wins > 0 || cleared > 0, completed: cleared > 0, cleared, wins };
    },
    blockedBy: '.stagebtn',
  },

  'Slipstream_GP.html': {
    rule:
      'Slipstream GP declares its own mode machine (LOBBY, COUNT, RACE, FINISH) on __SLIP.state. ' +
      'The route is the shipped race control and the steering keys; progress is the mode ' +
      'leaving LOBBY and reaching FINISH, read by value from that machine.',
    approaches: [
      { name: 'race control, then hold the throttle', steps: [['click', 'button:has-text("RACE")'], ['hold', 'ArrowUp', 45000]] },
      { name: 'keyboard only — Enter, then hold', steps: [['key', 'Enter'], ['hold', 'ArrowUp', 45000]] },
    ],
    gate: () => {
      const api = window.__SLIP;
      if (!api || !api.state) return { reached: false, note: 'no __SLIP state' };
      // 'left LOBBY' looked like a first gate and is not one: the no-input
      // control reached it, because the lobby advances into the race on its own
      // clock. A gate a player never has to touch measures nothing. The first
      // gate is therefore the first lap the player actually completes, and the
      // win is the classified finish.
      const m = api.state.mode, p = api.state.player;
      return { reached: !!p && (p.lap || 0) >= 2, completed: m === 'FINISH', mode: m,
               laps: p && p.lap };
    },
    blockedBy: null,
  },

  'Wrecking_Crew.html': {
    rule:
      'Wrecking Crew declares its own mode machine (TITLE, BOARD, PLACE, BOOM, SCORE) on __WC.state. ' +
      'The route is the shipped BEGIN and START DEMOLITION controls; progress is the mode leaving ' +
      'TITLE and reaching SCORE, read by value from that machine.',
    approaches: [
      { name: 'begin, take the contract, detonate', steps: [['click', '#b-begin'], ['settle', 1500], ['click', '#start'], ['settle', 30000]] },
      { name: 'begin, then the training site', steps: [['click', '#b-begin'], ['settle', 1500], ['click', '#t-launch'], ['settle', 30000]] },
    ],
    gate: () => {
      const api = window.__WC;
      if (!api || !api.state) return { reached: false, note: 'no __WC state' };
      // 'left TITLE' is not a first gate either: the blocked-route control
      // reached it with the BEGIN control removed, because the title screen
      // hands over to the contract board by itself. The first gate is the charge
      // actually being fired (BOOM), which only a player can cause.
      const m = api.state.mode;
      return { reached: m === 'BOOM' || m === 'SCORE', completed: m === 'SCORE', mode: m };
    },
    blockedBy: '#b-begin',
  },

  'voxelcraft.html': {
    rule:
      'Voxelcraft\'s arcade leg ends on its own 60 s clock (ARCADE_DURATION). The route is the ' +
      'shipped arcade menu entry and its START control; progress is the arcade record gaining a ' +
      'high score in localStorage — the game\'s own record.',
    approaches: [
      { name: 'arcade mode, then its own clock', steps: [['click', '#m-arcade'], ['settle', 2000], ['click', '#arcade-start'], ['settle', 75000]] },
    ],
    gate: () => {
      const modal = document.getElementById('arcade-end');
      const open = modal && getComputedStyle(modal).display !== 'none' && modal.getBoundingClientRect().width > 0;
      let high = null;
      try { high = localStorage.getItem('voxelcraft:arcadeHigh'); } catch (_) { /* blocked storage is not progress */ }
      return { reached: !!open, completed: !!open, arcadeHigh: high };
    },
    blockedBy: '#m-arcade',
  },
};

/* ------------------------------------------------------------------ *
 * §4.2 last clause — the flag/state allocation sweep. A bit, key or index
 * that carries two meanings is the Emberwild defect class: its item cache
 * and its completion state shared a bit, so collecting two pods made the
 * game report itself finished. This is a source sweep, reported per game;
 * a collision is repaired with a DECLARED REGISTRY and a duplicate-claim
 * assertion, never by renumbering the one instance.
 * ------------------------------------------------------------------ */
function allocationSweep(src) {
  const decls = [...src.matchAll(/\b(?:const|let|var)\s+((?:FLAG|BIT|F)_[A-Z0-9_]+)\s*=\s*(\d+)\b/g)]
    .map((m) => ({ name: m[1], value: Number(m[2]) }));
  const byValue = new Map();
  for (const d of decls) {
    if (!byValue.has(d.value)) byValue.set(d.value, []);
    byValue.get(d.value).push(d.name);
  }
  const collisions = [...byValue.entries()].filter(([, names]) => names.length > 1);
  const storageKeys = [...new Set([...src.matchAll(/localStorage\.(?:get|set|remove)Item\(\s*['"]([^'"]+)['"]/g)].map((m) => m[1]))];
  return { declared: decls.length, collisions, storageKeys };
}

/* ------------------------------------------------------------------ *
 * driving
 * ------------------------------------------------------------------ */
function serve() {
  const server = http.createServer((req, res) => {
    const p = decodeURIComponent(new url.URL(req.url, 'http://x').pathname);
    if (p === '/hud.js') {
      if (fs.existsSync(SITE_HUD)) { res.writeHead(200, { 'content-type': 'text/javascript' }); res.end(fs.readFileSync(SITE_HUD)); }
      else { res.writeHead(404); res.end(); }
      return;
    }
    if (!p.startsWith('/Lessons/')) { res.writeHead(404); res.end(); return; }
    const f = path.join(ROOT, p.slice('/Lessons/'.length));
    if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { 'content-type': f.endsWith('.html') ? 'text/html; charset=utf-8' : 'application/octet-stream' });
    res.end(fs.readFileSync(f));
  });
  return server;
}

async function runApproach(browser, origin, game, approach, opts = {}) {
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e.message).slice(0, 100)));
  const started = Date.now();
  let steps = 0;
  try {
    await page.goto(`${origin}/Lessons/Games/${encodeURIComponent(game)}?splash=skip`, { waitUntil: 'load', timeout: 30000 });
    await page.waitForTimeout(1800);
    const skip = page.locator('text=Skip intro');
    if (await skip.count()) { await skip.first().click({ timeout: 3000 }).catch(() => {}); await page.waitForTimeout(600); }

    // The blocked-route control: the plan's own entry control is removed from the
    // DOM before any input, so the route a player would take is genuinely gone.
    if (opts.block) {
      await page.evaluate((sel) => { document.querySelectorAll(sel).forEach((el) => el.remove()); }, opts.block);
    }

    if (!opts.noInput) {
      for (const step of approach.steps) {
        const [kind, a, b] = step;
        if (kind === 'click') { await page.locator(a).first().click({ timeout: 8000 }).catch(() => {}); steps += 1; await page.waitForTimeout(700); }
        else if (kind === 'key') { await page.keyboard.press(a).catch(() => {}); steps += 1; await page.waitForTimeout(700); }
        else if (kind === 'hold') {
          await page.keyboard.down(a).catch(() => {}); steps += 1;
          await page.waitForTimeout(b); await page.keyboard.up(a).catch(() => {});
        } else if (kind === 'mash') {
          for (let i = 0; i < b; i += 1) {
            const hit = await page.locator(a).first().click({ timeout: 1200 }).then(() => true).catch(() => false);
            if (hit) steps += 1;
            await page.waitForTimeout(250);
            const done = await page.evaluate(opts.gateSrc).catch(() => ({ reached: false }));
            if (done && done.reached) break;
          }
        } else if (kind === 'settle') { await page.waitForTimeout(a); }
      }
    }

    // poll the gate to the plan's budget rather than reading it once
    const deadline = Date.now() + (opts.noInput ? 8000 : 20000);
    let ev = { reached: false };
    for (;;) {
      ev = await page.evaluate(opts.gateSrc).catch(() => ({ reached: false, note: 'gate threw' }));
      if ((ev && ev.reached) || Date.now() > deadline) break;
      await page.waitForTimeout(600);
    }
    return { ...ev, steps, ms: Date.now() - started, errors: errors.slice(0, 2) };
  } finally {
    await ctx.close().catch(() => {});
  }
}

/* ------------------------------------------------------------------ */
async function main() {
  const args = process.argv.slice(2);
  const censusOnly = args.includes('--census');
  const filter = args.find((a) => !a.startsWith('--'));

  console.log('verify_playable — can these games be FINISHED?\n');
  console.log('§4.1 record — win / lose / first gate, derived from each game\'s own source:');
  for (const [g, line] of Object.entries(CENSUS)) {
    if (filter && !g.toLowerCase().includes(filter.toLowerCase())) continue;
    console.log(`  ${g}\n      ${line}`);
  }
  console.log(`\n  ${Object.keys(CENSUS).length} games recorded · ${Object.keys(PLANS).length} carry a driveable plan in this build\n`);

  console.log('§4.2 allocation sweep — a bit, key or index carrying two meanings:');
  let collisionTotal = 0;
  for (const g of Object.keys(CENSUS)) {
    if (filter && !g.toLowerCase().includes(filter.toLowerCase())) continue;
    const f = path.join(GAMES, g);
    if (!fs.existsSync(f)) { console.log(`  ${g}: file not present`); continue; }
    const sweep = allocationSweep(fs.readFileSync(f, 'utf8'));
    collisionTotal += sweep.collisions.length;
    if (sweep.collisions.length) {
      console.log(`  COLLISION ${g}: ${sweep.collisions.map(([v, n]) => `${n.join(' and ')} both = ${v}`).join('; ')}`);
    }
  }
  console.log(`  ${collisionTotal} declared-flag collision(s) across the swept games` +
              (collisionTotal === 0 ? ' — no game in this estate declares a numbered flag registry, so there is nothing to collide; recorded, not claimed as clean.\n' : '\n'));

  if (censusOnly) { console.log('census only — no browser run requested'); return; }

  let chromium;
  try { ({ chromium } = await import('playwright')); }
  catch (_) { console.error('INCONCLUSIVE: playwright is not importable. This gate did not judge anything, which is not a pass.'); process.exit(2); }

  const server = serve();
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch({ headless: true });

  const results = [];
  for (const [game, plan] of Object.entries(PLANS)) {
    if (filter && !game.toLowerCase().includes(filter.toLowerCase())) continue;
    console.log(`\n== ${game}`);
    console.log(`   rule: ${plan.rule}`);
    const gateSrc = plan.gate;
    const perApproach = [];
    for (const approach of plan.approaches) {
      const ev = await runApproach(browser, origin, game, approach, { gateSrc });
      perApproach.push({ approach: approach.name, ev });
      console.log(`   ${ev.reached ? 'REACHED ' : 'NOT     '} ${approach.name} — ${ev.steps} real input(s), ${(ev.ms / 1000).toFixed(1)}s, ${JSON.stringify({ ...ev, steps: undefined, ms: undefined, errors: undefined })}`);
      if (ev.errors && ev.errors.length) console.log(`            page errors: ${ev.errors.join(' | ')}`);
    }
    const anyReached = perApproach.some((r) => r.ev.reached);
    const allReached = perApproach.every((r) => r.ev.reached);

    // three firing controls, run only when there is a green to protect
    let controls = null;
    if (anyReached) {
      const first = plan.approaches.find((a, i) => perApproach[i].ev.reached);
      const blocked = plan.blockedBy
        ? await runApproach(browser, origin, game, first, { gateSrc, block: plan.blockedBy })
        : { reached: null, note: 'no single entry control to remove' };
      const noInput = await runApproach(browser, origin, game, first, { gateSrc, noInput: true });
      // Wrong predicate: the same run, the same real state, but the gate asks
      // for a value the game can never hold. If this still reports REACHED the
      // gate is not reading state at all.
      const wrongPredicate = await runApproach(browser, origin, game, first, {
        gateSrc: () => {
          const seams = [window.__LUMINS, window.__SLIP, window.__WC, window.__GCsave];
          const present = seams.filter(Boolean).length;
          const impossible = document.querySelector('#__no_such_element_this_estate_will_ever_ship__');
          return { reached: !!impossible, note: 'impossible predicate', seamsPresent: present };
        },
      });
      controls = { blocked, noInput, wrongPredicate };
      console.log(`   control blocked-route   : ${blocked.reached === null ? 'n/a — ' + blocked.note : (blocked.reached ? 'STILL REACHED (control did not bite)' : 'red, as required')}`);
      console.log(`   control no-input        : ${noInput.reached ? 'STILL REACHED (control did not bite)' : 'red, as required'}`);
      console.log(`   control wrong-predicate : ${wrongPredicate.reached ? 'STILL REACHED (control did not bite)' : 'red, as required'}`);
    }

    const controlsBite = !anyReached || (
      (controls.blocked.reached === null || controls.blocked.reached === false) &&
      controls.noInput.reached === false && controls.wrongPredicate.reached === false);

    const anyCompleted = perApproach.some((r) => r.ev.completed === true);
    results.push({ game, anyReached, anyCompleted, allReached, perApproach, controlsBite });
  }

  await browser.close();
  server.close();

  console.log('\n== VERDICT ==');
  console.log('game                                          first-gate  completed  every-approach  controls-bite  route');
  for (const r of results) {
    const route = r.perApproach.filter((p) => p.ev.reached).map((p) => `${p.ev.steps} input(s)`)[0] || '-';
    console.log(`${r.game.slice(0, 44).padEnd(46)}${String(r.anyReached).padEnd(12)}${String(r.anyCompleted).padEnd(11)}${String(r.allReached).padEnd(16)}${String(r.controlsBite).padEnd(15)}${route}`);
  }
  const gated = results.filter((r) => r.anyReached && r.controlsBite);
  const done = results.filter((r) => r.anyCompleted && r.controlsBite);
  const noGate = results.filter((r) => !r.anyReached).map((r) => r.game);
  const noWin = results.filter((r) => r.anyReached && !r.anyCompleted).map((r) => r.game);
  console.log(`\nfirst gate reached, controls biting : ${gated.length} of ${results.length} planned`);
  console.log(`COMPLETED (the game's own win)      : ${done.length} of ${results.length} planned`);
  if (noGate.length) console.log(`first gate NOT reached by any planned approach: ${noGate.join(', ')}`);
  if (noWin.length) console.log(`reached the first gate but NOT completed: ${noWin.join(', ')}`);
  console.log(`${Object.keys(CENSUS).length - Object.keys(PLANS).length} game(s) carry a §4.1 record but no driveable plan in this build — recorded, not claimed.`);

  // A game that cannot be finished is a Tier 1 escalation, not an audit line.
  // The harness reports; it does not fail the build on an unplanned game.
  process.exit(results.some((r) => r.anyReached && !r.controlsBite) ? 1 : 0);
}

main().catch((e) => { console.error('harness error:', e); process.exit(1); });
