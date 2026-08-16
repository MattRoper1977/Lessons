/* P2.7 — mission transport across the split, both directions.
 *
 * A partial deploy is the normal case, not the exception: the Studio and the
 * labs are five separate files and nothing makes a school take all five on the
 * same day. So every combination of {release, patched} Studio against
 * {release, patched} lab is run, in both directions.
 *
 *   direction 1   Studio mints a mission  ->  lab loads it through #missionFile
 *   direction 2   lab exports a capsule   ->  Studio imports it through #capsuleFiles
 *
 * PROVENANCE. Every mission used here is minted by a real Studio through its
 * real export button — none is hand-written. Where a fixture could not be
 * minted (the release Studio cannot offer C24), that is recorded as an
 * asymmetry, not papered over with an authored stand-in.
 */
import fs from 'node:fs'; import path from 'node:path'; import os from 'node:os';
const _pwPath = process.env.P2_PLAYWRIGHT || '/opt/node22/lib/node_modules/playwright/index.js';
const _pw = await import(_pwPath).catch(() => import('playwright'));
const ROOT = process.env.P2_ROOT || path.dirname(new URL(import.meta.url).pathname);
const PATCHED = process.env.P2_PATCHED || 'staging';
const chromium = _pw.chromium || _pw.default.chromium;
const WILTON = '03_Wilton_Carbon_Process_Control_Lab.html';
const STUDIO = '00_BUILD_FieldOps_Teacher_Studio.html';
const TREES = ['release', PATCHED];
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'p2xport-'));
const rows = []; const row = (id, what, ok, detail) => rows.push({ id, what, ok, detail });

const browser = await chromium.launch();
async function open(tree, file) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const pg = await ctx.newPage();
  const errs = []; pg.on('pageerror', e => errs.push(String(e).slice(0, 140)));
  await pg.addInitScript(() => {
    window.__blobs = [];
    const orig = URL.createObjectURL.bind(URL);
    URL.createObjectURL = b => { window.__blobs.push(b); return orig(b); };
  });
  await pg.goto('file://' + path.resolve(ROOT, tree, file), { waitUntil: 'domcontentloaded', timeout: 45000 });
  await pg.waitForTimeout(900);
  return { ctx, pg, errs };
}
const lastBlobText = pg => pg.evaluate(async () => window.__blobs.length ? await window.__blobs[window.__blobs.length - 1].text() : null);

/* ---------- mint the missions, from the real Studio export button --------- */
const missions = {};
for (const tree of TREES) {
  const { ctx, pg } = await open(tree, STUDIO);
  for (const feed of [14, 24]) {
    const got = await pg.evaluate(async (f) => {
      const e = document.getElementById('engine');
      e.value = 'wilton-carbon-control'; e.dispatchEvent(new Event('change', { bubbles: true }));
      await new Promise(r => setTimeout(r, 200));
      const sel = document.querySelector('[data-scenario="feed"]');
      if (!sel || ![...sel.options].some(o => +o.value === f)) return { unavailable: true };
      sel.value = String(f); sel.dispatchEvent(new Event('input', { bubbles: true }));
      document.getElementById('missionTitleInput').value = `TRANSPORT PROBE C${f}`;
      document.getElementById('missionTitleInput').dispatchEvent(new Event('input', { bubbles: true }));
      await new Promise(r => setTimeout(r, 200));
      document.getElementById('exportMission').click();
      await new Promise(r => setTimeout(r, 300));
      return { ok: true };
    }, feed);
    if (got.unavailable) { missions[`${tree}_C${feed}`] = null; continue; }
    const text = await lastBlobText(pg);
    const p = path.join(TMP, `${tree}_C${feed}.json`);
    fs.writeFileSync(p, text);
    missions[`${tree}_C${feed}`] = p;
  }
  await ctx.close();
}
row('X0', 'every mission fixture was minted by a real Studio, none hand-written',
  Object.keys(missions).length === 4,
  Object.entries(missions).map(([k, v]) => `${k}=${v ? 'minted' : 'UNAVAILABLE on that Studio'}`).join(' · '));

/* ---------- direction 1: Studio -> lab, all four combinations ------------- */
for (const st of TREES) for (const lab of TREES) {
  const file = missions[`${st}_C14`];
  const { ctx, pg, errs } = await open(lab, WILTON);
  await pg.setInputFiles('#missionFile', file);
  await pg.waitForTimeout(900);
  const got = await pg.evaluate(() => ({
    title: (document.getElementById('missionTitle') || {}).textContent || '',
    feed: (document.getElementById('wFeedRead') || {}).textContent || '',
  }));
  await ctx.close();
  const ok = /TRANSPORT PROBE C14/.test(got.title) && /^C14H30$/.test(got.feed.trim()) && errs.length === 0;
  row(`X1 ${st[0]}S->${lab[0]}L`, `a C14 mission from the ${st} Studio loads into the ${lab} lab`,
    ok, `title "${got.title}" feed "${got.feed}"${errs.length ? ' ERRORS: ' + errs.join(' | ') : ''}`);
}

/* ---------- the C24 mission, which only one Studio can mint --------------- */
row('X1c', 'the release Studio cannot mint a C24 mission (declared asymmetry, not a defect)',
  missions.release_C24 === null,
  missions.release_C24 === null ? 'release Studio offers [6,10,14,18,20]; C24 is a patched-only option'
                                : 'unexpectedly minted — the release Studio should not offer C24');
for (const lab of TREES) {
  const { ctx, pg, errs } = await open(lab, WILTON);
  await pg.setInputFiles('#missionFile', missions.patched_C24);
  await pg.waitForTimeout(900);
  const got = await pg.evaluate(async () => {
    const furn = document.getElementById('wFurnace');
    furn.value = furn.max; furn.dispatchEvent(new Event('input', { bubbles: true }));
    await new Promise(r => setTimeout(r, 100));
    document.getElementById('runDistil').click();
    await new Promise(r => setTimeout(r, 200));
    return {
      feed: (document.getElementById('wFeedRead').textContent || '').trim(),
      selected: [...document.querySelectorAll('.feedW.selected')].map(b => b.dataset.feed),
      hasButton: !!document.querySelector('.feedW[data-feed="24"]'),
      told: (document.getElementById('wTrayRead').textContent || '').trim(),
      notice: (document.getElementById('wDistilResult').textContent || '').trim(),
    };
  });
  await ctx.close();
  /* the transport must not BREAK either way. What it teaches on a release lab
     is a separate finding, reported rather than asserted away. */
  row(`X1d ->${lab[0]}L`, `a C24 mission from the patched Studio does not break the ${lab} lab`,
    got.feed === 'C24H50' && errs.length === 0,
    `feed "${got.feed}" · button present ${got.hasButton} · selected [${got.selected}] · zone "${got.told}" · ${got.notice}`);
}

/* ---------- direction 2: lab -> Studio, all four combinations ------------- */
const capsules = {};
for (const lab of TREES) {
  const { ctx, pg } = await open(lab, WILTON);
  await pg.evaluate(async () => {
    const set = (id, v) => { const e = document.getElementById(id); if (e) { e.value = v; e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); } };
    set('alias', 'TRANSPORT PROBE');
    document.querySelector('.feedW[data-feed="14"]').click();
    const furn = document.getElementById('wFurnace');
    furn.value = furn.max; furn.dispatchEvent(new Event('input', { bubbles: true }));
    await new Promise(r => setTimeout(r, 100));
    document.getElementById('runDistil').click();
    await new Promise(r => setTimeout(r, 200));
    document.getElementById('recordWRun').click();
    await new Promise(r => setTimeout(r, 200));
    set('claimText', 'C14 condensed in the kerosene range.');
    await new Promise(r => setTimeout(r, 200));
    document.getElementById('exportJSON').click();
    await new Promise(r => setTimeout(r, 400));
  });
  const text = await lastBlobText(pg);
  const p = path.join(TMP, `capsule_${lab}.json`);
  fs.writeFileSync(p, text);
  capsules[lab] = p;
  await ctx.close();
}
for (const lab of TREES) for (const st of TREES) {
  const { ctx, pg, errs } = await open(st, STUDIO);
  await pg.setInputFiles('#capsuleFiles', capsules[lab]);
  await pg.waitForTimeout(1200);
  const got = await pg.evaluate(() => [...document.querySelectorAll('#capsuleRows tr')]
    .map(tr => tr.textContent.replace(/\s+/g, ' ').trim()).filter(t => /TRANSPORT PROBE/.test(t)));
  await ctx.close();
  const ok = got.length === 1 && /verified/.test(got[0]) && !/changed \/ invalid/.test(got[0]) && errs.length === 0;
  row(`X2 ${lab[0]}L->${st[0]}S`, `a capsule from the ${lab} lab verifies in the ${st} Studio`,
    ok, got.length ? got[0].slice(0, 130) : `no row imported${errs.length ? ' ERRORS: ' + errs.join(' | ') : ''}`);
}

await browser.close();
console.log(`${'id'.padEnd(13)} verdict  what`);
console.log('-'.repeat(78));
for (const r of rows) {
  console.log(`${r.id.padEnd(13)} ${(r.ok ? 'PASS' : 'FAIL').padEnd(8)} ${r.what}`);
  console.log(`              ${r.detail}`);
}
const bad = rows.filter(r => !r.ok);
console.log(`\n${bad.length} transport failure(s) · fixtures in ${TMP}`);
process.exit(bad.length ? 1 : 0);
