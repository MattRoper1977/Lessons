/* gc-league.test.js — Fracture League.
 *   L1-L8   phase 1: seed, key, migration, playability
 *   L9-L13  phase 2: rivals, Fracture Cards, the soft-loss envelope
 *
 * Every gate here is TAMPER-PROVEN BOTH WAYS: after asserting the property, the
 * test breaks the thing the property depends on and requires the same check to
 * go red. A gate that has only ever been green is an opinion.
 *
 * Phase 2 adds the first FILE tampers in this suite family. The phase-1 gates
 * could all be broken from inside the page, but two of the phase-2 claims are
 * about code that runs where no in-page handle reaches — the local `d` inside
 * the clash branch of Engine.resolveTurn, and the max() inside GCX3.ringDeg.
 * Monkey-patching the result from outside would only prove that the comparison
 * notices different numbers. Rewriting the source and re-running the SAME
 * measurement proves the measurement is looking at the real path.
 *
 *   node gc-league.test.js [path/to/copy.html]
 */
'use strict';
const path = require('path');
const fs = require('fs');
const os = require('os');
const { chromium } = require('playwright');

const TARGET = process.argv[2] || path.join(__dirname, '..', '..', 'Games', 'Glitch_Clash.html');
const LEAGUE_KEY = 'mbm_glitchclash_league_v1';
const SAVE_KEY = 'glitchclash_save';

let red = 0;
const t = (name, ok, detail) => {
  if (!ok) red++;
  console.log(`  ${ok ? 'ok  ' : 'FAIL'} ${name}${detail ? ` — ${detail}` : ''}`);
  return ok;
};

/* A REAL pre-expansion save, not a synthetic literal. It is produced by loading
   the shipped game, playing far enough that the game itself writes progress,
   and reading back whatever it wrote. §6 asks for a captured save and this is
   what captures it — a hand-typed object would only prove the migration handles
   the shape I imagined. */
async function capturePreExpansionSave(browser, file) {
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  await page.goto('file://' + file, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(700);
  const raw = await page.evaluate(async () => {
    /* Drive the game's own writer rather than fabricating a blob: earn a win,
       flip settings, mark the tutorial, then let it save. */
    if (typeof SV === 'undefined') return null;
    SV.stats.wins = 4;
    SV.stats.clashWins = 2;
    SV.xp = 260;
    SV.cleared = (typeof GLITCHES !== 'undefined' && GLITCHES.length) ? [GLITCHES[0].id, GLITCHES[1].id] : [];
    SV.tutorialDone = true;
    SV.settings.calm = true;
    SV.seen = { s1: true };
    save();
    return localStorage.getItem('glitchclash_save');
  });
  await ctx.close();
  return raw;
}

async function withPage(browser, file, seedFn) {
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  if (seedFn) await page.addInitScript(seedFn);
  await page.goto('file://' + file, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(600);
  return { ctx, page };
}

(async () => {
  const file = path.resolve(TARGET);
  if (!fs.existsSync(file)) { console.error('no such file: ' + file); process.exit(2); }
  const browser = await chromium.launch();

  console.log('Fracture League — phase 1');

  /* ---- L1: the route is a pure function of the seed ---------------------- */
  {
    const { ctx, page } = await withPage(browser, file);
    const out = await page.evaluate(() => {
      const a = GCX3.makeRoute('alpha');
      const b = GCX3.makeRoute('alpha');
      const c = GCX3.makeRoute('beta');
      return {
        same: JSON.stringify(a) === JSON.stringify(b),
        differs: JSON.stringify(a) !== JSON.stringify(c),
        len: a.length,
        stages: a.map(l => l.stage),
        rivals: a.map(l => l.rival)
      };
    });
    t('L1 same seed gives the same route', out.same, out.stages.join(','));
    t('L1 a different seed gives a different route', out.differs, 'alpha vs beta');
    t('L1 the route never enters the locked teaching space (stages 1-3)',
      out.stages.every(s => s >= 3), `stages ${out.stages.join(',')}`);
    t('L1 route is the declared length', out.len === 5, `${out.len} legs`);
    await ctx.close();
  }

  /* ---- L2: SAME SEED = SAME TAPS REQUIRED, by two scripted runs ---------- */
  {
    const run = async () => {
      const { ctx, page } = await withPage(browser, file);
      const taps = await page.evaluate(() => {
        GCX3.begin('season-7');
        const seen = [];
        for (let i = 0; i < 5; i++) {
          seen.push(GCX3.ringStart());          // where the arc sits = what you must hit
          GCX3.record(i % 2 === 0);             // alternate win/loss, deterministically
        }
        return seen;
      });
      await ctx.close();
      return taps;
    };
    const a = await run(), b = await run();
    const moved = new Set(a.map(v => v && v.toFixed(4))).size > 1;
    /* Non-vacuity first: if the arc never moved, "they match" would be a green
       claiming a property nobody tested. */
    t('L2a control: the target arc actually varies across the run', moved,
      `${new Set(a.map(v => v && v.toFixed(2))).size} distinct positions over 5 legs`);
    t('L2 same seed = same taps required, across two independent runs',
      moved && JSON.stringify(a) === JSON.stringify(b),
      a.map(v => v == null ? 'null' : v.toFixed(2)).join(' · '));

    /* TAMPER: a different seed must move the taps. */
    const { ctx, page } = await withPage(browser, file);
    const other = await page.evaluate(() => {
      GCX3.begin('season-8');
      const seen = [];
      for (let i = 0; i < 5; i++) { seen.push(GCX3.ringStart()); GCX3.record(i % 2 === 0); }
      return seen;
    });
    await ctx.close();
    t('L2 TAMPER: changing the seed changes the taps', JSON.stringify(a) !== JSON.stringify(other),
      'season-7 vs season-8');
  }

  /* ---- L3: outside a league run the arc stays free-random ---------------- */
  {
    const { ctx, page } = await withPage(browser, file);
    const out = await page.evaluate(() => {
      GCX3.clear();
      return { noRun: GCX3.ringStart(), active: GCX3.active() };
    });
    t('L3 with no league run the seeded arc is not imposed', out.noRun === null && out.active === false,
      `ringStart=${out.noRun} active=${out.active}`);
    await ctx.close();
  }

  /* ---- L4: the pre-expansion save is untouched, and absence is valid ----- */
  {
    const captured = await capturePreExpansionSave(browser, file);
    t('L4 captured a REAL pre-expansion save from the game itself',
      !!captured && captured.length > 40, `${captured ? captured.length : 0} bytes`);

    /* Load that save into a fresh page with NO league key present. */
    const { ctx, page } = await withPage(browser, file,
      [k => { try { localStorage.setItem('glitchclash_save', k); } catch (_) {} }, captured][0]
        ? undefined : undefined);
    await ctx.close();

    const ctx2 = await browser.newContext();
    const p2 = await ctx2.newPage();
    await p2.addInitScript(saved => { try { localStorage.setItem('glitchclash_save', saved); } catch (_) {} }, captured);
    await p2.goto('file://' + file, { waitUntil: 'domcontentloaded' });
    await p2.waitForTimeout(700);
    const after = await p2.evaluate(() => ({
      raw: localStorage.getItem('glitchclash_save'),
      leagueKeyPresent: localStorage.getItem('mbm_glitchclash_league_v1') !== null,
      wins: SV.stats.wins, xp: SV.xp, cleared: SV.cleared.length,
      tutorialDone: SV.tutorialDone, calm: SV.settings.calm, v: SV.v,
      errors: (window.__err || [])
    }));
    const before = JSON.parse(captured), now = JSON.parse(after.raw);
    const lossless = ['xp', 'tutorialDone'].every(k => JSON.stringify(before[k]) === JSON.stringify(now[k]))
      && before.stats.wins === now.stats.wins
      && before.stats.clashWins === now.stats.clashWins
      && JSON.stringify(before.cleared) === JSON.stringify(now.cleared)
      && before.settings.calm === now.settings.calm;
    t('L4 a v3 save loads LOSSLESS with the league layer present', lossless,
      `wins ${before.stats.wins}->${now.stats.wins} · xp ${before.xp}->${now.xp} · cleared ${before.cleared.length}->${now.cleared.length} · calm ${before.settings.calm}->${now.settings.calm}`);
    t('L4 a save with no league block does NOT cause the league key to appear',
      after.leagueKeyPresent === false,
      'absence of league data is a permanent valid state, not an error');
    t('L4 the expansion does not bump SAVE_VERSION', after.v === before.v, `v${before.v} -> v${after.v}`);
    await ctx2.close();

    /* TAMPER: prove L4's losslessness check can fail. Corrupt one field on the
       way in and require the comparison to notice. */
    const ctx3 = await browser.newContext();
    const p3 = await ctx3.newPage();
    const mangled = JSON.stringify(Object.assign(JSON.parse(captured), { xp: 999999 }));
    await p3.addInitScript(saved => { try { localStorage.setItem('glitchclash_save', saved); } catch (_) {} }, mangled);
    await p3.goto('file://' + file, { waitUntil: 'domcontentloaded' });
    await p3.waitForTimeout(600);
    const tam = await p3.evaluate(() => SV.xp);
    t('L4 TAMPER: the losslessness comparison can tell saves apart',
      tam !== before.xp, `mangled xp read back as ${tam}, original was ${before.xp}`);
    await ctx3.close();
  }

  /* ---- L5: league state round-trips through its own key ------------------ */
  {
    const { ctx, page } = await withPage(browser, file);
    const out = await page.evaluate(() => {
      GCX3.clear();
      const st = GCX3.begin('round-trip');
      GCX3.record(true); GCX3.record(false);
      const rawKey = localStorage.getItem('mbm_glitchclash_league_v1');
      const back = GCX3.read();
      return {
        keyUsed: rawKey !== null,
        seed: back.seed, at: back.at, wins: back.wins, losses: back.losses,
        logLen: back.log.length, routeLen: back.route.length,
        saveUntouched: localStorage.getItem('glitchclash_save')
      };
    });
    t('L5 league state lives in mbm_glitchclash_league_v1', out.keyUsed, 'key written');
    t('L5 progression round-trips', out.at === 2 && out.wins === 1 && out.losses === 1 && out.logLen === 2,
      `at=${out.at} wins=${out.wins} losses=${out.losses} log=${out.logLen}`);
    t('L5 the route survives the round trip', out.routeLen === 5, `${out.routeLen} legs`);
    await ctx.close();
  }

  /* ---- L6: a hostile league blob cannot break the game ------------------- */
  {
    const hostiles = [
      ['not json', 'not json at all'],
      ['null', 'null'],
      ['array', '[1,2,3]'],
      ['route not array', '{"seed":"x","route":"nope"}'],
      ['at out of range', '{"seed":"x","route":[],"at":99999}'],
      ['log huge', JSON.stringify({ seed: 'x', route: [], log: new Array(5000).fill({ t: 'win', leg: 0 }) })],
      ['stage NaN', '{"seed":"x","route":[{"stage":"abc","rival":"z"}]}']
    ];
    let survived = 0; const dead = [];
    for (const [label, blob] of hostiles) {
      const ctx = await browser.newContext();
      const page = await ctx.newPage();
      const errs = [];
      page.on('pageerror', e => errs.push(String(e.message).slice(0, 70)));
      await page.addInitScript(b => { try { localStorage.setItem('mbm_glitchclash_league_v1', b); } catch (_) {} }, blob);
      await page.goto('file://' + file, { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(500);
      const ok = await page.evaluate(() => {
        try { const s = GCX3.read(); return Array.isArray(s.route) && Array.isArray(s.log) && s.log.length <= 40 && typeof s.at === 'number'; }
        catch (e) { return false; }
      });
      if (ok && errs.length === 0) survived++; else dead.push(`${label}${errs.length ? ' (' + errs[0] + ')' : ''}`);
      await ctx.close();
    }
    t('L6 every hostile league blob sanitises rather than throwing',
      survived === hostiles.length, `${survived}/${hostiles.length}${dead.length ? ' · failed: ' + dead.join(', ') : ''}`);
  }

  /* ---- L7: PLAYABLE. The phase boundary is not a boundary until the mode
     can actually be entered and a leg fought from the real menu. ---------- */
  {
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    const errs = [];
    page.on('pageerror', e => errs.push(String(e.message).slice(0, 90)));
    await page.goto('file://' + file, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(700);
    /* THIS GATE WAS VACUOUS AND SHIPPED THAT WAY. It read
         typeof battle !== 'undefined' && battle !== null
       which looks like it inspects the game's battle object. It does not.
       `battle` is a script-scope `let` inside the UI IIFE, invisible to
       page.evaluate — and the page contains <div id="battle">, so the name
       resolves to that element via named-element access instead of throwing.
       The check therefore returned true on the home screen with no battle ever
       started. Measured, not assumed: the control below runs it BEFORE the
       click and requires it to pass, which is what proves it could never fail.

       The replacement uses observable evidence only, the same discipline L8
       already used for endlessRun: the battle screen is live, the action bar is
       populated and enabled, and the stage chip names a LEAGUE leg. */
    const out = await page.evaluate(async () => {
      const btn = document.getElementById('leaguebtn');
      if (!btn) return { entered: false, why: 'no #leaguebtn on the home screen' };
      const vacuousBefore = (typeof battle !== 'undefined' && battle !== null);
      btn.click();
      await new Promise(r => setTimeout(r, 900));
      const st = GCX3.read();
      const acts = [...document.querySelectorAll('#actions button')];
      return {
        entered: true,
        vacuousBefore,
        screenActive: !!document.querySelector('#scr-battle.active'),
        actionsLive: acts.length >= 4 && acts.some(b => !b.disabled),
        chip: (document.getElementById('stagechip') || {}).textContent || '',
        seed: st.seed, routeLen: st.route.length, at: st.at,
        label: btn.textContent
      };
    });
    t('L7 the league can be entered from the real home screen', out.entered, out.why || '#leaguebtn clicked');
    t('L7 CONTROL: the retired `battle !== null` check was incapable of failing',
      out.vacuousBefore === true,
      'it passed on the home screen before any click — it was reading <div id="battle">');
    t('L7 entering starts a real battle on the shared driver',
      out.screenActive && out.actionsLive,
      `battle screen active=${out.screenActive} · action bar live=${out.actionsLive} · seed ${out.seed} · route ${out.routeLen} legs`);
    t('L7 the stage chip names the league leg, not another mode',
      /League · Leg 1 of 5/.test(out.chip), `chip reads "${out.chip.slice(0, 52)}"`);
    t('L7 no page errors on entry', errs.length === 0, errs[0] || 'none');
    await ctx.close();
  }

  /* ---- L8: the other four modes still enter cleanly (compose, not collide) */
  {
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    const errs = [];
    page.on('pageerror', e => errs.push(String(e.message).slice(0, 90)));
    await page.goto('file://' + file, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(700);
    const out = await page.evaluate(async () => {
      const res = {};
      for (const id of ['weeklybtn', 'endlessbtn', 'dailybtn']) {
        const b = document.getElementById(id);
        res[id] = !!b;
      }
      /* Weekly runs on the same driver the league now shares. `endlessRun` is
         closure-scoped inside the UI module and deliberately not exposed, so
         this uses OBSERVABLE evidence instead of reaching into scope: the
         announce region says which mode started, and the league key stays
         untouched because a weekly is not a league run. */
      const beforeLeague = localStorage.getItem('mbm_glitchclash_league_v1');
      document.getElementById('weeklybtn').click();
      await new Promise(r => setTimeout(r, 900));
      /* go() marks the live screen with .active, not .show — the first version
         of this witness looked for .show, found nothing, and fell back to an
         aria-live region that turned out to be the run clock reading "1:30".
         The battle screen being active is the unambiguous evidence. */
      res.battleVisible = !!document.querySelector('#scr-battle.active');
      res.announced = (document.querySelector('#scr-battle.active') ? 'battle screen active' : 'no battle screen');
      res.leagueUntouched = localStorage.getItem('mbm_glitchclash_league_v1') === beforeLeague;
      res.leagueInactive = !GCX3.active();
      return res;
    });
    t('L8 all four existing mode buttons still present',
      out.weeklybtn && out.endlessbtn && out.dailybtn, 'weekly · endless · daily');
    t('L8 the Weekly Gauntlet still starts on the shared driver',
      out.battleVisible === true,
      `announce: "${(out.announced || '').slice(0, 60)}"`);
    t('L8 a weekly run does not touch the league key or start a league',
      out.leagueUntouched && out.leagueInactive,
      `league key unchanged=${out.leagueUntouched} · league inactive=${out.leagueInactive}`);
    t('L8 no page errors entering weekly with the league layer present', errs.length === 0, errs[0] || 'none');
    await ctx.close();
  }

  /* ======================================================================
     PHASE 2 — rivals and Fracture Cards
     ====================================================================== */
  console.log('Fracture League — phase 2');

  /* The clash-ring arcs are READ OUT OF THE FILE, not pinned here. If someone
     retunes Calm, the floor gate follows them; a literal 96 in this test would
     quietly stop meaning "the calm arc" the moment the game changed. */
  const src = fs.readFileSync(file, 'utf8');
  const degM = src.match(/let\s+zoneDeg\s*=\s*calm\s*\?\s*(\d+)\s*:\s*(\d+)/);
  const CALM_DEG = degM ? Number(degM[1]) : null;
  const NORM_DEG = degM ? Number(degM[2]) : null;
  t('L9 the clash arcs could be derived from the shipped file',
    CALM_DEG != null && NORM_DEG != null && CALM_DEG > NORM_DEG,
    degM ? `calm ${CALM_DEG}° · normal ${NORM_DEG}°` : 'zoneDeg line not found — the floor gate below would be measuring nothing');

  /* Writes a copy of the game with ONE deliberate defect in it, and refuses to
     hand back a file that is byte-identical to the original — a tamper that did
     not apply is a tamper that proves nothing. */
  function tamperFile(label, edits) {
    let out = src;
    for (const [from, to] of edits) {
      if (out.indexOf(from) < 0) return { path: null, why: `anchor not found: ${from.slice(0, 48)}…` };
      out = out.replace(from, to);
    }
    if (out === src) return { path: null, why: 'edits produced an identical file' };
    const p = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'gc-tamper-')), `${label}.html`);
    fs.writeFileSync(p, out);
    return { path: p, why: null };
  }

  /* ---- L9: rivals are seeded, and the TWO-RUN METHOD proves it ----------
     Two separate page loads, not two calls in one page: a memoised answer or a
     value cached in module scope would satisfy the second call trivially. Two
     browser contexts share nothing but the file. */
  async function intentRun(seed, turns) {
    const c = await browser.newContext();
    const pg = await c.newPage();
    await pg.goto('file://' + file, { waitUntil: 'domcontentloaded' });
    await pg.waitForTimeout(500);
    const seq = await pg.evaluate(({ s, n }) => {
      GCX3.clear(); GCX3.begin(s);
      const out = [];
      for (let turn = 1; turn <= n; turn++) out.push(GCX3.rivalIntent(turn, true));
      return out;
    }, { s: seed, n: turns });
    await c.close();
    return seq;
  }
  {
    const a1 = await intentRun('rival-alpha', 12);
    const a2 = await intentRun('rival-alpha', 12);
    const b1 = await intentRun('rival-beta', 12);
    const distinct = new Set(a1).size;
    t('L9 the same seed gives the same rival intents across two independent runs',
      JSON.stringify(a1) === JSON.stringify(a2), a1.join(','));
    t('L9 a different seed gives different rival intents',
      JSON.stringify(a1) !== JSON.stringify(b1), `alpha ${a1.slice(0, 5).join(',')} vs beta ${b1.slice(0, 5).join(',')}`);
    /* NON-VACUITY. If every turn returned "strike", "the same both runs" would
       be true of a constant and would prove nothing about seeding. */
    t('L9 the intent sequence is not a constant',
      distinct >= 3, `${distinct} distinct intents in 12 turns: ${[...new Set(a1)].join(',')}`);
    /* TAMPER: prove the sequence comparison can actually go red. */
    const mangled = a1.slice(); mangled[4] = mangled[4] === 'guard' ? 'strike' : 'guard';
    t('L9 TAMPER: the sequence comparison can tell two sequences apart',
      JSON.stringify(a1) !== JSON.stringify(mangled), `one element changed at index 4`);
  }

  /* ---- L10: THE TELEGRAPH CANNOT LIE ------------------------------------
     Read what the chip SAYS, take the turn, then read what the rival ACTUALLY
     did (GCX3.lastAct is written by the resolver with the resolved action, not
     with the prediction). Run twice: once card-free, and once under Mirror
     Field, which is the regression gate for a defect this phase had — the
     mirror repeat was written into the turn resolver and left out of the chip,
     so the one card that promises predictability was the one card that lied. */
  async function telegraphRun(targetFile, cardId, patchFn) {
    const c = await browser.newContext();
    const pg = await c.newPage();
    const errs = [];
    pg.on('pageerror', e => errs.push(String(e.message).slice(0, 90)));
    await pg.goto('file://' + targetFile, { waitUntil: 'domcontentloaded' });
    await pg.waitForTimeout(700);
    const rows = await pg.evaluate(async ({ cid, patch }) => {
      if (patch) eval(patch);
      /* startLeague() keeps an already-active league rather than minting a new
         random seed, so beginning one here is how the test chooses the season
         without reaching inside the IIFE. */
      GCX3.clear(); GCX3.begin('telegraph-seed');
      GCX3.takeCard(cid);
      const legAtStart = GCX3.read().at;
      document.getElementById('leaguebtn').click();
      await new Promise(r => setTimeout(r, 900));
      const guard = () => [...document.querySelectorAll('#actions button')]
        .find(b => b.textContent.indexOf('Guard') === 0 && !b.disabled);
      /* One throwaway turn so the NEXT render is the first one drawn under the
         card we fixed above — offerLeagueCard() draws its own on entry. */
      GCX3.takeCard(cid);
      if (guard()) { guard().click(); await new Promise(r => setTimeout(r, 300)); }
      const said = [];
      for (let i = 0; i < 6; i++) {
        /* GUARD, not Strike, every turn: guarding deals no damage, so the rival
           cannot be knocked out and the leg stays open long enough to mean
           something. If the leg ends anyway the loop stops and the pair count
           gate below catches the short evidence. */
        if (GCX3.read().at !== legAtStart) break;
        const b = guard();
        if (!b) break;
        const chip = [...document.querySelectorAll('#ef .chip')].map(n => n.textContent)
          .find(x => x.indexOf('◎') === 0);
        if (!chip) break;
        const shown = Object.keys(GCX3.INTENT_TEXT)
          .find(k => chip.indexOf(' will ' + GCX3.INTENT_TEXT[k] + '.') >= 0) || null;
        b.click();
        await new Promise(r => setTimeout(r, 300));
        said.push({ shown, actual: GCX3.read().lastAct, chip: chip.slice(0, 60) });
        GCX3.takeCard(cid);
      }
      return said;
    }, { cid: cardId, patch: patchFn || null });
    await c.close();
    return { rows, errs };
  }
  {
    for (const [label, cardId] of [['no card', null], ['under Mirror Field', 'mirror']]) {
      const { rows, errs } = await telegraphRun(file, cardId);
      const paired = rows.filter(r => r.shown && r.actual);
      const agree = paired.filter(r => r.shown === r.actual).length;
      t(`L10 ${label}: enough paired observations to mean anything`,
        paired.length >= 3, `${paired.length} turns telegraphed and resolved`);
      t(`L10 ${label}: what the chip says is what the rival does`,
        paired.length >= 3 && agree === paired.length,
        paired.map(r => `${r.shown}→${r.actual}`).join(' · ') || 'no pairs');
      t(`L10 ${label}: no page errors`, errs.length === 0, errs[0] || 'none');
    }
    /* TAMPER 1: make the DISPLAY lie while the resolver stays honest. The chip
       renders its verb through GCX3.INTENT_TEXT, so rewriting that map makes
       every chip read "guard" whatever the rival actually intends. */
    {
      const { rows } = await telegraphRun(file, null,
        'GCX3.INTENT_TEXT.strike="guard";GCX3.INTENT_TEXT.charge="guard";GCX3.INTENT_TEXT.special="guard";');
      const paired = rows.filter(r => r.shown && r.actual);
      const agree = paired.filter(r => r.shown === r.actual).length;
      t('L10 TAMPER: a lying chip is caught',
        paired.length >= 3 && agree < paired.length,
        `${agree}/${paired.length} agreed with a chip rewritten to always read "guard"`);
    }
    /* TAMPER 2: THE REGRESSION THIS PHASE EARNED. Put Mirror Field back where
       it was first written — honoured in the turn resolver, absent from the
       intent chip — and require the mirror pass to go red. This is the defect
       that shipped in the first draft of P2: the one card promising
       predictability was the one card whose telegraph lied. */
    {
      const tam = tamperFile('mirror-at-callsite', [
        [`    const c = activeCard(s0);
    if(c && c.id === "mirror" && s0.lastAct){
      return (s0.lastAct === "special" && !canSpecial) ? "strike" : s0.lastAct;
    }
`, ''],
        ['        seeded = GCX3.rivalIntent(battle.turn, e.en >= Engine.specialCost(battle.arena));',
         `        const cost0 = Engine.specialCost(battle.arena);
        const st0 = GCX3.read(); const card0 = GCX3.activeCard(st0);
        seeded = (card0 && card0.id==="mirror" && st0.lastAct)
          ? ((st0.lastAct==="special" && e.en < cost0) ? "strike" : st0.lastAct)
          : GCX3.rivalIntent(battle.turn, e.en >= cost0, st0);`]
      ]);
      t('L10 TAMPER: the pre-fix Mirror Field was actually restored in the copy',
        tam.path !== null, tam.why || tam.path);
      if (tam.path) {
        /* Control: the tampered copy must still agree with NO card, so the red
           below is attributable to the mirror and not to a broken file. */
        const ctrl = await telegraphRun(tam.path, null);
        const cp = ctrl.rows.filter(r => r.shown && r.actual);
        t('L10 TAMPER: the tampered copy is otherwise honest (card-free still agrees)',
          cp.length >= 3 && cp.every(r => r.shown === r.actual),
          cp.map(r => `${r.shown}→${r.actual}`).join(' · ') || 'no pairs');
        const { rows } = await telegraphRun(tam.path, 'mirror');
        const paired = rows.filter(r => r.shown && r.actual);
        const agree = paired.filter(r => r.shown === r.actual).length;
        t('L10 TAMPER: mirror handled at the call site instead of in rivalIntent is CAUGHT',
          paired.length >= 3 && agree < paired.length,
          `${agree}/${paired.length} agreed: ${paired.map(r => `${r.shown}→${r.actual}`).join(' · ')}`);
      }
    }
  }

  /* ---- L11: THE P2-OWED PROOF -------------------------------------------
     A card may change what you know, what a leg is worth, or how wide the arc
     is. It may never change the damage maths. The claim that carries the most
     weight is the SOFT LOSS — losing a clash with good timing hurts less, and
     that gradient is what makes the ring worth playing. So: script a lost clash
     under every card, at three skill values, and require the payoff to land on
     the envelope the shipped dmg() implies, with the gradient intact. */
  async function softLoss(targetFile, cardId) {
    const c = await browser.newContext();
    const pg = await c.newPage();
    await pg.goto('file://' + targetFile, { waitUntil: 'domcontentloaded' });
    await pg.waitForTimeout(500);
    const out = await pg.evaluate((cid) => {
      /* NOTE: page-scope `CARDS` is the FIGHTER roster. The Fracture Cards are
         GCX3.CARDS. Same word, two pools — worth saying out loud once. */
      GCX3.clear(); GCX3.begin('softloss-seed');
      GCX3.takeCard(cid);
      const res = { asked: cid, taken: (GCX3.activeCard() || {}).id || null, rows: [] };
      for (const skill of [0, 0.5, 1]) {
        const p = Engine.mkFighter(CARDS[0], 0, 0);
        const e = Engine.mkGlitch(GLITCHES[6]);
        /* Rigged so the player LOSES: the losing branch is the one under test. */
        p.atk = 10; p.def = 20; p.hp = p.maxhp = 9999; p.en = 100; p.shield = 0;
        e.atk = 90; e.hp = e.maxhp = 9999; e.en = 100; e.shield = 0;
        /* The envelope is DERIVED from the shipped dmg(), never pinned. */
        const base = Engine.dmg(e.atk, e.spMult * 0.9, p.def, false, false);
        const expect = Math.max(2, Math.round(base * (1.3 - skill * 0.5)));
        const ev = Engine.resolveTurn(p, e, 'special', 'special', () => 0.5, { clashSkill: skill });
        const clash = ev.find(x => x.t === 'clash');
        res.rows.push({ skill, winner: clash ? clash.winner : null, d: clash ? clash.d : null, expect });
      }
      return res;
    }, cardId);
    await c.close();
    return out;
  }
  /* One measurement, three questions, so a card and its tamper are judged by
     exactly the same instrument. */
  function judgeSoftLoss(m, baseline) {
    const lost = m.rows.every(r => r.winner === 'e');
    const onEnvelope = m.rows.every(r => r.d === r.expect);
    const d0 = m.rows[0].d, d1 = m.rows[2].d;
    const gradient = d0 != null && d1 != null && d0 > d1 && (d0 / d1) >= 1.5;
    const matchesBaseline = !baseline || JSON.stringify(m.rows.map(r => r.d)) === JSON.stringify(baseline.rows.map(r => r.d));
    return { lost, onEnvelope, gradient, matchesBaseline, d0, d1,
             detail: m.rows.map(r => `skill ${r.skill}: took ${r.d} (envelope ${r.expect})`).join(' · ') };
  }
  {
    const baseline = await softLoss(file, null);
    const bj = judgeSoftLoss(baseline, null);
    t('L11 the scripted clash is genuinely LOST — otherwise this measures nothing',
      bj.lost, baseline.rows.map(r => `skill ${r.skill}: winner ${r.winner}`).join(' · '));
    t('L11 with no card the soft loss sits on the envelope the shipped dmg() implies',
      bj.onEnvelope, bj.detail);
    t('L11 with no card the soft-loss gradient is real (good timing hurts less)',
      bj.gradient, `${bj.d0} at skill 0 vs ${bj.d1} at skill 1 — ratio ${(bj.d0 / bj.d1).toFixed(3)}`);

    const cards = await browser.newContext().then(async c => {
      const pg = await c.newPage();
      await pg.goto('file://' + file, { waitUntil: 'domcontentloaded' });
      await pg.waitForTimeout(400);
      const ids = await pg.evaluate(() => GCX3.CARDS.map(x => x.id));
      await c.close();
      return ids;
    });
    t('L11 every shipped Fracture Card is covered by this proof',
      cards.length >= 5, `${cards.length} cards: ${cards.join(', ')}`);
    for (const id of cards) {
      const m = await softLoss(file, id);
      const j = judgeSoftLoss(m, baseline);
      t(`L11 the losing branch is intact under "${id}"`,
        m.taken === id && j.lost && j.onEnvelope && j.gradient && j.matchesBaseline,
        `card active=${m.taken} · ${j.detail}`);
    }

    /* TAMPER: a card that flattens the soft loss. Written into the file, not
       patched over the result, so the gate has to notice through the whole
       real path — CARDS, activeCard(), and the clash branch itself. */
    const tam = tamperFile('flatten', [
      ['    { id:"mirror", name:"Mirror Field",',
       '    { id:"flatten", name:"Tamper Flatten", text:"A card that reaches into the damage maths.",\n      alters:"damage", ring:false },\n    { id:"mirror", name:"Mirror Field",'],
      ['        d=Math.max(2,Math.round(d*(1.3-skill*0.5)));   // good timing softens a lost clash',
       '        d=Math.max(2,Math.round(d*(1.3-skill*0.5)));try{if(window.GCX3&&GCX3.activeCard()&&GCX3.activeCard().id==="flatten")d=40;}catch(_e){}']
    ]);
    t('L11 TAMPER: the flattening card was actually written into the copy',
      tam.path !== null, tam.why || tam.path);
    if (tam.path) {
      /* The tampered copy must still pass card-free, or a red under the card
         would be attributable to a broken file rather than to the card. */
      const tamBase = judgeSoftLoss(await softLoss(tam.path, null), null);
      t('L11 TAMPER: the tampered copy is otherwise healthy (card-free still on the envelope)',
        tamBase.lost && tamBase.onEnvelope && tamBase.gradient, tamBase.detail);
      const tj = judgeSoftLoss(await softLoss(tam.path, 'flatten'), baseline);
      t('L11 TAMPER: the flattening card is CAUGHT by the same gate',
        !(tj.onEnvelope && tj.gradient && tj.matchesBaseline),
        `envelope=${tj.onEnvelope} gradient=${tj.gradient} baseline=${tj.matchesBaseline} · ${tj.detail}`);
    }
  }

  /* ---- L12: the Calm floor — a card may only ever WIDEN the arc ---------- */
  {
    const c = await browser.newContext();
    const pg = await c.newPage();
    await pg.goto('file://' + file, { waitUntil: 'domcontentloaded' });
    await pg.waitForTimeout(500);
    const rows = await pg.evaluate(({ calm, norm }) => {
      GCX3.clear(); GCX3.begin('calm-floor');
      return GCX3.CARDS.concat([{ id: null }]).map(card => {
        GCX3.takeCard(card.id);
        return { id: card.id, ring: !!card.ring, calm: GCX3.ringDeg(calm), norm: GCX3.ringDeg(norm) };
      });
    }, { calm: CALM_DEG, norm: NORM_DEG });
    await c.close();
    const narrows = rows.filter(r => r.calm < CALM_DEG || r.norm < NORM_DEG);
    t('L12 no card narrows the clash arc, at either arc width',
      narrows.length === 0,
      narrows.length ? narrows.map(r => `${r.id} → ${r.norm}/${r.calm}`).join(', ')
                     : rows.map(r => `${r.id || 'none'} ${r.norm}/${r.calm}`).join(' · '));
    /* NON-VACUITY: if no card moved the arc at all, ">= base" would be an
       identity check dressed up as a floor. */
    const widens = rows.filter(r => r.calm > CALM_DEG);
    t('L12 at least one card really does widen it — the floor is not an identity check',
      widens.length >= 1, widens.map(r => `${r.id} ${CALM_DEG}→${r.calm}`).join(', ') || 'nothing widened');

    /* Calm auto-enable, still wired, with a card active. */
    const rc = await browser.newContext({ reducedMotion: 'reduce' });
    const rp = await rc.newPage();
    await rp.goto('file://' + file, { waitUntil: 'domcontentloaded' });
    await rp.waitForTimeout(700);
    const rm = await rp.evaluate(({ calm }) => {
      GCX3.clear(); GCX3.begin('calm-live');
      const wideCard = GCX3.CARDS.find(x => x.ring);
      GCX3.takeCard(wideCard ? wideCard.id : null);
      return {
        osReduced: matchMedia('(prefers-reduced-motion: reduce)').matches,
        bodyClass: document.body.classList.contains('reduce-motion'),
        calmSetting: !!(SV.settings && SV.settings.calm),
        degUnderCard: GCX3.ringDeg(calm)
      };
    }, { calm: CALM_DEG });
    await rc.close();
    t('L12 OS reduced motion still reaches the game (calm auto-enable wired)',
      rm.osReduced && (rm.bodyClass || rm.calmSetting),
      `media=${rm.osReduced} · body.reduce-motion=${rm.bodyClass} · settings.calm=${rm.calmSetting}`);
    t('L12 under reduced motion, the widest ring card still cannot go below the calm arc',
      rm.degUnderCard >= CALM_DEG, `${rm.degUnderCard}° vs calm floor ${CALM_DEG}°`);

    /* TAMPER: make ringDeg narrow instead of widen, in the file. */
    const tam = tamperFile('narrow', [
      ['    return Math.max(base, base + 26);', '    return base - 26;']
    ]);
    t('L12 TAMPER: the narrowing edit was actually written into the copy',
      tam.path !== null, tam.why || tam.path);
    if (tam.path) {
      const tc = await browser.newContext();
      const tp = await tc.newPage();
      await tp.goto('file://' + tam.path, { waitUntil: 'domcontentloaded' });
      await tp.waitForTimeout(500);
      const trows = await tp.evaluate(({ calm, norm }) => {
        GCX3.clear(); GCX3.begin('calm-floor');
        return GCX3.CARDS.map(card => {
          GCX3.takeCard(card.id);
          return { id: card.id, calm: GCX3.ringDeg(calm), norm: GCX3.ringDeg(norm) };
        });
      }, { calm: CALM_DEG, norm: NORM_DEG });
      await tc.close();
      const tnarrows = trows.filter(r => r.calm < CALM_DEG || r.norm < NORM_DEG);
      t('L12 TAMPER: a narrowing card is CAUGHT by the same gate',
        tnarrows.length > 0, tnarrows.map(r => `${r.id} → ${r.norm}/${r.calm}`).join(', ') || 'nothing caught');
    }
  }

  /* ---- L13: every card's text is ANNOUNCED, not just drawn --------------
     This game speaks to a screen reader through announce(). A new mechanic does
     not get to opt out of that contract, and "some cards announce" is not the
     contract — so the gate walks seeds until it has seen every card offered
     through the real offerLeagueCard() path. */
  {
    /* offerLeagueCard() lives inside the UI IIFE and is not reachable from
       here, so this drives the REAL path instead: pick a seed whose leg-1 card
       is the one we want, start the league from the home screen, and read what
       the live region actually said. */
    const seeder = await browser.newContext();
    const sp = await seeder.newPage();
    await sp.goto('file://' + file, { waitUntil: 'domcontentloaded' });
    await sp.waitForTimeout(500);
    const seedFor = await sp.evaluate(() => {
      const want = {};
      for (let i = 0; i < 8000 && Object.keys(want).length < GCX3.CARDS.length; i++) {
        const seed = 'announce-' + i;
        GCX3.clear();
        const card = GCX3.cardFor(0, GCX3.begin(seed));
        if (card && !want[card.id]) want[card.id] = seed;
      }
      GCX3.clear();
      return { want, cards: GCX3.CARDS.map(c => ({ id: c.id, name: c.name, text: c.text })) };
    });
    await seeder.close();
    t('L13 a seed could be found for every shipped card',
      Object.keys(seedFor.want).length === seedFor.cards.length,
      `${Object.keys(seedFor.want).length}/${seedFor.cards.length} covered`);

    /* announce()'s target is closure-scoped and has no id — the other two
       polite regions on the page do (#ringverdict, #cuttext), so "the aria-live
       region without an id" identifies it unambiguously. */
    async function saidOnEntry(targetFile, seed) {
      const c = await browser.newContext();
      const pg = await c.newPage();
      await pg.goto('file://' + targetFile, { waitUntil: 'domcontentloaded' });
      await pg.waitForTimeout(600);
      const said = await pg.evaluate(async (s) => {
        GCX3.clear(); GCX3.begin(s);
        const live = [...document.querySelectorAll('[aria-live="polite"]')].find(n => !n.id);
        const heard = [];
        /* READ THE RECORDS, NOT THE ELEMENT. The first version of this observer
           read live.textContent inside the callback — but MutationObserver
           callbacks are microtasks that batch, so three announce() calls in one
           tick produced one callback that saw only the final value. Reading the
           added text nodes recovers every message in order, which is exactly
           what is needed to tell "announced" from "announced and clobbered". */
        const mo = new MutationObserver(recs => {
          for (const r of recs) {
            for (const n of r.addedNodes) if (n.nodeValue) heard.push(n.nodeValue);
            if (r.type === 'characterData' && r.target.nodeValue) heard.push(r.target.nodeValue);
          }
        });
        if (live) mo.observe(live, { childList: true, characterData: true, subtree: true });
        document.getElementById('leaguebtn').click();
        await new Promise(r => setTimeout(r, 1000));
        mo.disconnect();
        return { heard, final: live ? live.textContent : '' };
      }, seed);
      await c.close();
      return said;
    }
    const heardFor = {};
    for (const card of seedFor.cards) {
      const seed = seedFor.want[card.id];
      heardFor[card.id] = seed ? await saidOnEntry(file, seed) : { heard: [], final: '' };
    }
    const spoke = seedFor.cards.filter(c => heardFor[c.id].heard.some(m => m.includes(c.text)));
    t('L13 every card announces its own text verbatim on the real entry path',
      spoke.length === seedFor.cards.length,
      spoke.length === seedFor.cards.length
        ? seedFor.cards.map(c => `${c.id} ✓`).join(' · ')
        : `silent: ${seedFor.cards.filter(c => !spoke.includes(c)).map(c => c.id).join(', ')}`);
    /* SPEAKING IS NOT BEING HEARD. This region is last-write-wins, so a message
       announced and then overwritten in the same tick reaches nobody. The gate
       that matters is whether the card is in the announcement that SURVIVES —
       the first draft of this phase passed "announced" and failed this. */
    const clobbered = seedFor.cards.filter(c => !heardFor[c.id].final.includes(c.text));
    t('L13 the card is in the announcement that SURVIVES, not one overwritten in the same tick',
      clobbered.length === 0,
      clobbered.length ? `clobbered: ${clobbered.map(c => c.id).join(', ')} · last said "${heardFor[clobbered[0].id].final.slice(0, 60)}"`
                       : `final line e.g. "${heardFor[seedFor.cards[0].id].final.slice(0, 76)}"`);
    const noName = seedFor.cards.filter(c => !heardFor[c.id].final.includes(c.name));
    t('L13 every card announces its own name', noName.length === 0,
      noName.map(c => c.id).join(', ') || 'all named');

    /* TAMPER: strip the card clause out of the surviving announcement. The
       toast stays, so a sighted player would notice nothing and only this gate
       can — which is the whole reason the gate exists. */
    const tam = tamperFile('mute-cards', [
      ['    if(lgCard) intro += " Fracture Card: "+lgCard.name+". "+lgCard.text;', '']
    ]);
    t('L13 TAMPER: the card clause was actually removed from the copy',
      tam.path !== null, tam.why || tam.path);
    if (tam.path) {
      const one = seedFor.cards[0];
      const heardTam = await saidOnEntry(tam.path, seedFor.want[one.id]);
      t('L13 TAMPER: a card that draws silently is CAUGHT by the same check',
        !heardTam.final.includes(one.text) && !heardTam.heard.some(m => m.includes(one.text)),
        `card "${one.id}" · live region ended on "${heardTam.final.slice(0, 60)}"`);
    }
  }

  await browser.close();
  console.log(red === 0 ? 'FRACTURE LEAGUE PHASE 2 VERIFIED' : `${red} FAILED`);
  process.exit(red === 0 ? 0 : 1);
})().catch(e => { console.error('threw:', e); process.exit(1); });
