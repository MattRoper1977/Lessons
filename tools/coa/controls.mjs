/* Class of Ashes — matched-pair controls, driven entirely through the DOM.
 *
 * C3 removes window.__COA_QA, so there is no back door left and none is
 * reinstated "just for the gate". Everything below clicks the same buttons a
 * pupil would.
 */
import fs from 'node:fs'; import path from 'node:path';
const _pwPath = process.env.COA_PLAYWRIGHT || '/opt/node22/lib/node_modules/playwright/index.js';
const _pw = await import(_pwPath).catch(() => import('playwright'));
const chromium = _pw.chromium || _pw.default.chromium;
const ROOT = process.env.COA_ROOT || path.dirname(new URL(import.meta.url).pathname);
const STAGING = process.env.COA_STAGING || 'staging';
const FILE = 'Class_of_Ashes_Zero_Period_PRO.html';
const TREES = ['release', STAGING];
const [T_REL, T_PAT] = TREES;
const KEYS = ['coa.zeroPeriod.pro.settings.v1', 'coa.zeroPeriod.pro.profile.v1', 'coa.zeroPeriod.pro.activeRun.v1'];
const SHAPES = ['null', '[]', '{bad', '"x"', '7', 'true', '""'];

const rows = [];
const pair = (id, what, relOk, patOk, detail = '', bothTrue = 'NOT A CONTROL') =>
  rows.push({ id, what, release: relOk, patched: patOk,
    verdict: (!relOk && patOk) ? 'MATCHED PAIR' : (relOk && patOk) ? bothTrue
           : (relOk && !patOk) ? 'REGRESSION' : 'NOT A CONTROL', detail });
const note = (id, what, verdict, detail) => rows.push({ id, what, release: null, patched: null, verdict, detail });

const browser = await chromium.launch();
const url = tree => 'file://' + path.resolve(ROOT, tree, FILE);

async function boot(tree, { seed = null, query = '', viewport = { width: 1440, height: 900 }, opts = {} } = {}) {
  const ctx = await browser.newContext(Object.assign({ viewport }, opts));
  const pg = await ctx.newPage();
  const errs = []; pg.on('pageerror', e => errs.push(String(e).slice(0, 160)));
  if (seed) {
    /* seed the store BEFORE the page's script runs, which is the only way the
       boot path sees it */
    await pg.addInitScript(s => { try { for (const [k, v] of s) window.localStorage.setItem(k, v); } catch (e) {} }, seed);
  }
  await pg.goto(url(tree) + query, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await pg.waitForTimeout(900);
  return { ctx, pg, errs };
}
const screens = () => {
  const vis = id => { const e = document.getElementById(id); if (!e) return false;
    const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== 'hidden'; };
  return { main: vis('mainScreen'), continueText: (document.getElementById('continueText') || {}).textContent || '',
           continueShown: vis('continueBtn'), clears: (document.getElementById('menuClears') || {}).textContent || '' };
};

/* =====================================================================
 * C1 — hostile shapes: 7 shapes x 3 keys = 21 cases per tree
 * ===================================================================== */
for (const tree of TREES) {
  const out = {};
  for (const key of KEYS) for (const shape of SHAPES) {
    const { ctx, pg, errs } = await boot(tree, { seed: [[key, shape]] });
    const s = await pg.evaluate(screens).catch(e => ({ evalFailed: String(e).slice(0, 80) }));
    await ctx.close();
    out[`${key.split('.')[3]}:${shape}`] = { errs, ...s };
  }
  globalThis['c1_' + tree] = out;
}
{
  const bad = t => Object.entries(globalThis['c1_' + t])
    .filter(([, v]) => v.errs.length || v.evalFailed || !v.main)
    .map(([k, v]) => `${k} (${v.errs[0] || v.evalFailed || 'archive screen not painted'})`);
  pair('C1', `all ${KEYS.length * SHAPES.length} hostile shapes boot clean and paint the archive screen`,
    bad(T_REL).length === 0, bad(T_PAT).length === 0,
    `release ${bad(T_REL).length} broken: [${bad(T_REL).join(' · ')}] -> staging ${bad(T_PAT).length} broken: [${bad(T_PAT).join(' · ')}]`);
  const R = globalThis['c1_' + T_REL];
  note('C1-scope', 'the defect scope, measured rather than assumed', 'MEASURED',
    `keys that break on the literal string null: ` +
    KEYS.map(k => `${k.split('.')[3]}=${(R[`${k.split('.')[3]}:null`].errs.length ? 'BREAKS' : 'fine')}`).join(' · '));
  /* Continue must not merely appear — it must be in the right state */
  const cont = t => Object.entries(globalThis['c1_' + t]).filter(([k]) => k.startsWith('activeRun:'))
    .map(([k, v]) => `${k}:${v.continueShown ? 'offered' : 'hidden'}`);
  note('C1-continue', 'Continue state across hostile activeRun payloads', 'MEASURED',
    `staging ${cont(T_PAT).join(' · ')}`);
}

/* =====================================================================
 * C2 — unvalidated URL parameters
 * ===================================================================== */
const BADQ = ['?autostart=1&overclock=bogus', '?autostart=1&mode=bogus', '?autostart=1&class=bogus',
              '?autostart=1&mode=bogus&class=bogus&overclock=bogus', '?autostart=1'];
for (const tree of TREES) {
  const out = {};
  for (const q of BADQ) {
    const { ctx, pg, errs } = await boot(tree, { query: q });
    const s = await pg.evaluate(screens).catch(e => ({ evalFailed: String(e).slice(0, 80) }));
    await ctx.close();
    out[q] = { errs, ...s };
  }
  globalThis['c2_' + tree] = out;
}
{
  const bad = t => Object.entries(globalThis['c2_' + t])
    .filter(([, v]) => v.errs.length || v.evalFailed || !v.main)
    .map(([k, v]) => `${k} (${v.errs[0] || v.evalFailed || 'archive screen not visible'})`);
  pair('C2', 'every bad autostart parameter set boots to a visible archive screen with no error',
    bad(T_REL).length === 0, bad(T_PAT).length === 0,
    `release ${bad(T_REL).length}/${BADQ.length} broken: [${bad(T_REL).join(' · ')}] -> staging ${bad(T_PAT).length}/${BADQ.length}`);
}

/* =====================================================================
 * C3 — the QA hook is gone, and the game still works without it
 * ===================================================================== */
for (const tree of TREES) {
  const s = fs.readFileSync(path.join(ROOT, tree, FILE), 'utf8');
  globalThis['c3src_' + tree] = { qa: (s.match(/__COA_QA/g) || []).length, autostart: (s.match(/autostart/g) || []).length };
  const { ctx, pg } = await boot(tree);
  globalThis['c3live_' + tree] = await pg.evaluate(() => typeof window.__COA_QA);
  await ctx.close();
}
pair('C3a', 'window.__COA_QA is absent from the shipped payload and from the running page',
  globalThis['c3src_' + T_REL].qa === 0 && globalThis['c3live_' + T_REL] === 'undefined',
  globalThis['c3src_' + T_PAT].qa === 0 && globalThis['c3live_' + T_PAT] === 'undefined',
  `release source ${globalThis['c3src_' + T_REL].qa} mentions, live typeof ${globalThis['c3live_' + T_REL]} -> ` +
  `staging source ${globalThis['c3src_' + T_PAT].qa} mentions, live typeof ${globalThis['c3live_' + T_PAT]}`);
pair('C3b', 'the autostart block is gone with it',
  globalThis['c3src_' + T_REL].autostart === 0, globalThis['c3src_' + T_PAT].autostart === 0,
  `release ${globalThis['c3src_' + T_REL].autostart} mentions -> staging ${globalThis['c3src_' + T_PAT].autostart}`);

/* the UI-driven configuration subset: one per mode and one per chassis.
   12 would be every mode x chassis; this runs the union, which covers each
   mode once and each chassis once, and says so rather than implying a full
   cross product was run. */
/* the real ids, read from the payload's own data-mode attributes rather
   than from the mode NAMES in the prose */
const MODES = ['operation', 'lockdown', 'training'];
const CLASSES = ['prefect', 'valedictorian', 'sapper', 'bursar'];
const CONFIGS = [];
for (let i = 0; i < Math.max(MODES.length, CLASSES.length); i++)
  CONFIGS.push({ mode: MODES[i % MODES.length], cls: CLASSES[i % CLASSES.length] });
for (const cls of CLASSES) if (!CONFIGS.some(c => c.cls === cls)) CONFIGS.push({ mode: MODES[0], cls });
for (const mode of MODES) if (!CONFIGS.some(c => c.mode === mode)) CONFIGS.push({ mode, cls: CLASSES[0] });
for (const tree of TREES) {
  const out = {};
  for (const cfg of CONFIGS) {
    const { ctx, pg, errs } = await boot(tree);
    const reached = await pg.evaluate(async (c) => {
      const sleep = ms => new Promise(r => setTimeout(r, ms));
      const vis = id => { const e = document.getElementById(id); if (!e) return false;
        const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
      const modeBtn = document.querySelector(`[data-mode="${c.mode}"]`);
      if (!modeBtn) return { step: 'no mode button', mode: c.mode };
      modeBtn.click(); await sleep(350);
      const card = [...document.querySelectorAll('#classGrid [data-class], #classGrid button, #classGrid .card')]
        .find(el => (el.dataset && el.dataset.class === c.cls) || (el.textContent || '').toLowerCase().includes(c.cls));
      if (!card) return { step: 'no chassis card', cls: c.cls };
      card.click(); await sleep(200);
      document.getElementById('classNext').click(); await sleep(300);
      const oc = document.querySelector('#overclockGrid button, #overclockGrid [data-overclock], #overclockGrid .card');
      if (oc) { oc.click(); await sleep(150); }
      document.getElementById('overclockNext').click(); await sleep(350);
      document.getElementById('deployBtn').click(); await sleep(900);
      return { step: 'deployed', briefing: vis('briefScreen'), main: vis('mainScreen'),
               canvasPainted: (() => { const cv = document.getElementById('game'); if (!cv) return false;
                 const g = cv.getContext('2d'); if (!g) return false;
                 const d = g.getImageData(0, 0, Math.min(cv.width, 400), Math.min(cv.height, 300)).data;
                 let lit = 0; for (let i = 0; i < d.length; i += 4) if (d[i] + d[i + 1] + d[i + 2] > 40) lit++;
                 return lit; })() };
    }, cfg);
    await ctx.close();
    out[`${cfg.mode}/${cfg.cls}`] = { errs, ...reached };
  }
  globalThis['c3ui_' + tree] = out;
}
{
  const bad = t => Object.entries(globalThis['c3ui_' + t])
    .filter(([, v]) => v.errs.length || v.step !== 'deployed' || !(v.canvasPainted > 0))
    .map(([k, v]) => `${k} (${v.errs[0] || v.step || 'canvas not painted'})`);
  pair('C3c', `each mode and each chassis reaches a painting game canvas through the real UI (${CONFIGS.length} configurations, the union not the cross product)`,
    bad(T_REL).length === 0, bad(T_PAT).length === 0,
    `release ${bad(T_REL).length} failed: [${bad(T_REL).join(' · ')}] -> staging ${bad(T_PAT).length} failed: [${bad(T_PAT).join(' · ')}]`,
    'ALREADY CORRECT ON RELEASE — asserted so removing the QA hook cannot break deploy');
}

/* =====================================================================
 * C4 — subtitle / HUD overlap census
 * ===================================================================== */
const VIEWS = [[915, 412], [844, 390], [740, 360], [1280, 600]];
for (const tree of TREES) {
  const out = {};
  for (const [w, h] of VIEWS) for (const largeHud of [false, true]) {
    const { ctx, pg, errs } = await boot(tree, {
      viewport: { width: w, height: h },
      seed: [['coa.zeroPeriod.pro.settings.v1', JSON.stringify({ largeHud, subtitles: true })]],
    });
    const r = await pg.evaluate(async () => {
      const sleep = ms => new Promise(r => setTimeout(r, ms));
      const mb = document.querySelector('[data-mode="operation"]'); if (mb) { mb.click(); await sleep(300); }
      const card = document.querySelector('#classGrid [data-class], #classGrid button, #classGrid .card');
      if (card) { card.click(); await sleep(150); }
      const cn = document.getElementById('classNext'); if (cn) { cn.click(); await sleep(250); }
      const oc = document.querySelector('#overclockGrid button, #overclockGrid [data-overclock], #overclockGrid .card');
      if (oc) { oc.click(); await sleep(120); }
      const on = document.getElementById('overclockNext'); if (on) { on.click(); await sleep(250); }
      const db = document.getElementById('deployBtn'); if (db) { db.click(); await sleep(1200); }
      /* force the longest realistic subtitle and make it visible */
      const sub = document.getElementById('subtitles');
      if (!sub) return { noSubtitles: true };
      sub.textContent = 'MUNITIONS SIPHON ONLINE — THE ARCH-PROVOST IS VENTING MAGMA THROUGH THE FOUNDRY FLOOR, FALL BACK TO THE EAST STAIR';
      sub.style.opacity = '1';
      await sleep(120);
      const sr = sub.getBoundingClientRect();
      /* the drawn HUD band, from the same expression the draw path uses */
      const CW = window.innerWidth, CH = window.innerHeight;
      const compact = CW < 980, vh = compact ? 106 : 118;
      const hud = { top: CH - vh - 16, bottom: CH - 16 };
      const overlap = Math.max(0, Math.min(sr.bottom, hud.bottom) - Math.max(sr.top, hud.top));
      const gap = hud.top - sr.bottom;   // positive = clear air between them
      return { overlap: Math.round(overlap), gap: Math.round(gap),
               sub: { top: Math.round(sr.top), bottom: Math.round(sr.bottom) },
               hud: { top: Math.round(hud.top), bottom: Math.round(hud.bottom) }, compact,
               cssVar: getComputedStyle(document.documentElement).getPropertyValue('--hud-bottom').trim() };
    });
    await ctx.close();
    out[`${w}x${h}/largeHud=${largeHud}`] = { errs, ...r };
  }
  globalThis['c4_' + tree] = out;
}
{
  /* MIN_GAP, not "overlap === 0". Touching is not clearing, and the weaker
     predicate let a fixed 134px pass at wide viewports where the HUD band is
     exactly 134px tall — which is how Y4a came out UNWATCHED. */
  const MIN_GAP = 8;
  const bad = t => Object.entries(globalThis['c4_' + t]).filter(([, v]) => v.noSubtitles || !(v.gap >= MIN_GAP))
    .map(([k, v]) => `${k} gap ${v.gap}px overlap ${v.overlap}px (sub ${v.sub && v.sub.top}-${v.sub && v.sub.bottom}, hud ${v.hud && v.hud.top}-${v.hud && v.hud.bottom})`);
  pair('C4', `the subtitle panel clears the drawn HUD band by at least ${MIN_GAP}px (${VIEWS.length} viewports x largeHud off/on)`,
    bad(T_REL).length === 0, bad(T_PAT).length === 0,
    `release ${bad(T_REL).length}/${VIEWS.length * 2} overlap: [${bad(T_REL).join(' · ')}] -> staging ${bad(T_PAT).length}/${VIEWS.length * 2}: [${bad(T_PAT).join(' · ')}]`);
  note('C4-derivation', 'the clearance is derived, not guessed', 'MEASURED',
    Object.entries(globalThis['c4_' + T_PAT]).map(([k, v]) => `${k}: --hud-bottom=${v.cssVar || 'unset'} gap=${v.gap}px`).join(' · '));
}

/* =====================================================================
 * C5.4 / C5.5 — viewport and reduced motion
 * ===================================================================== */
{
  const vp = t => ((fs.readFileSync(path.join(ROOT, t, FILE), 'utf8').match(/<meta name="viewport"[^>]*>/) || [''])[0]);
  const clean = s => !/user-scalable=no/.test(s) && !/maximum-scale=1/.test(s);
  pair('C5.4', 'the viewport no longer blocks pinch zoom',
    clean(vp(T_REL)), clean(vp(T_PAT)), `release ${vp(T_REL)} -> staging ${vp(T_PAT)}`);
}
for (const tree of TREES) {
  const { ctx, pg } = await boot(tree, { opts: { reducedMotion: 'reduce' } });
  globalThis['c5m_' + tree] = await pg.evaluate(() => ({
    bodyClass: document.body.className,
    reduced: document.body.classList.contains('reducedMotion'),
  }));
  await ctx.close();
  /* and an explicit user choice must still win */
  const { ctx: c2, pg: p2 } = await boot(tree, {
    opts: { reducedMotion: 'reduce' },
    seed: [['coa.zeroPeriod.pro.settings.v1', JSON.stringify({ reducedMotion: false })]],
  });
  globalThis['c5o_' + tree] = await p2.evaluate(() => document.body.classList.contains('reducedMotion'));
  await c2.close();
}
pair('C5.5a', 'booting under prefers-reduced-motion seeds the in-game reduced-motion setting',
  globalThis['c5m_' + T_REL].reduced, globalThis['c5m_' + T_PAT].reduced,
  `release ${JSON.stringify(globalThis['c5m_' + T_REL])} -> staging ${JSON.stringify(globalThis['c5m_' + T_PAT])}`);
note('C5.5b', 'an explicit stored user choice still overrides the OS seed',
  globalThis['c5o_' + T_PAT] === false ? 'ASSERTED' : 'OVERRIDDEN BY THE SEED',
  `stored reducedMotion:false under prefers-reduced-motion → body has the class: staging ${globalThis['c5o_' + T_PAT]}`);

/* =====================================================================
 * C0 — THE SCOPE FENCE.  This one exists to go red if anyone ever places it.
 * ===================================================================== */
{
  const SITE = '/workspace/mattroper1977.github.io';
  /* the canonical shelf record and the two audience pages, at the paths they
     actually occupy in this repo — a fence that cannot find its subject is
     INCONCLUSIVE, never a pass */
  const targets = ['data/source-manifests/games.json', 'games/index.html',
                   'for/pupils/index.html', 'tools/render_audience_homepages.py'];
  const found = [], missing = [], mentions = [];
  for (const rel of targets) {
    const p = path.join(SITE, rel);
    if (!fs.existsSync(p)) { missing.push(rel); continue; }
    found.push(rel);
    const s = fs.readFileSync(p, 'utf8');
    if (/class[_ -]?of[_ -]?ashes|zero[_ -]?period|zeroperiod/i.test(s)) mentions.push(rel);
  }
  note('C0', 'Class of Ashes appears nowhere on the shelf, in either audience page, or in any curation record',
    missing.length ? 'INCONCLUSIVE' : (mentions.length ? 'FENCE BREACHED' : 'ASSERTED'),
    missing.length ? `could not read: ${missing.join(', ')} — the fence is UNPROVEN, not proven` :
      `checked ${found.join(', ')} · mentions: ${mentions.length ? mentions.join(', ') : 'none'}`);
  if (missing.length) rows[rows.length - 1].verdict = 'INCONCLUSIVE';
}

await browser.close();
console.log(`${'id'.padEnd(14)} ${'release'.padEnd(9)} ${'staging'.padEnd(9)} verdict`);
console.log('-'.repeat(84));
for (const r of rows) {
  console.log(`${r.id.padEnd(14)} ${String(r.release).padEnd(9)} ${String(r.patched).padEnd(9)} ${r.verdict}`);
  console.log(`    ${r.what}`);
  if (r.detail) console.log(`    ${r.detail}`);
}
const bad = rows.filter(r => ['NOT A CONTROL', 'REGRESSION', 'FENCE BREACHED', 'OVERRIDDEN BY THE SEED'].includes(r.verdict));
const inc = rows.filter(r => r.verdict === 'INCONCLUSIVE');
console.log(`\n${bad.length} failure(s); ${inc.length} inconclusive`);
process.exit(bad.length ? 1 : inc.length ? 2 : 0);
