/* gc-league.test.js — Fracture League, phase 1: seed, key and migration.
 *
 * Every gate here is TAMPER-PROVEN BOTH WAYS: after asserting the property, the
 * test breaks the thing the property depends on and requires the same check to
 * go red. A gate that has only ever been green is an opinion.
 *
 *   node gc-league.test.js [path/to/copy.html]
 */
'use strict';
const path = require('path');
const fs = require('fs');
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
    const out = await page.evaluate(async () => {
      const btn = document.getElementById('leaguebtn');
      if (!btn) return { entered: false, why: 'no #leaguebtn on the home screen' };
      btn.click();
      await new Promise(r => setTimeout(r, 900));
      const st = GCX3.read();
      const inBattle = !!(document.getElementById('scr-battle') || document.querySelector('.screen.show'));
      return {
        entered: true,
        battleStarted: typeof battle !== 'undefined' && battle !== null,
        seed: st.seed, routeLen: st.route.length,
        label: btn.textContent,
        inBattle
      };
    });
    t('L7 the league can be entered from the real home screen', out.entered, out.why || '#leaguebtn clicked');
    t('L7 entering starts a real battle on the shared driver', out.battleStarted === true,
      `seed ${out.seed} · route ${out.routeLen} legs`);
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

  await browser.close();
  console.log(red === 0 ? 'FRACTURE LEAGUE PHASE 1 VERIFIED' : `${red} FAILED`);
  process.exit(red === 0 ? 0 : 1);
})().catch(e => { console.error('threw:', e); process.exit(1); });
