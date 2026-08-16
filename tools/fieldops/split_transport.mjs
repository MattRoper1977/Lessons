/* §5 — mission transport proven ACROSS THE SPLIT, both directions.
 *
 * The pack's best feature is that a Teacher Studio mints a mission and a lab
 * consumes it. The split is the likeliest thing to break that, because after it
 * the two halves live in different repositories at different depths:
 *
 *   labs   ->  Lessons        Science_Teesside/Build/v4_fieldops/
 *   Studio ->  Matt-s-Apps-   FieldOps_Teacher_Studio.html   (repo root)
 *
 * PROVENANCE, and this is the single most important honesty requirement in P2:
 * all twelve of the pack's own .buildmission.json samples were NEVER SHIPPED —
 * they are among the 28 absent files. So every fixture here is AUTHORED BY THIS
 * HARNESS and is declared as such in its own filename and in the report. None
 * of them is presented as the pack's own sample.
 */
import fs from 'node:fs'; import path from 'node:path'; import os from 'node:os';
const _pwPath = process.env.P2_PLAYWRIGHT || '/opt/node22/lib/node_modules/playwright/index.js';
const _pw = await import(_pwPath).catch(() => import('playwright'));
const chromium = _pw.chromium || _pw.default.chromium;

const LESSONS = process.env.P2_LESSONS || '/home/user/Lessons';
const APPS = process.env.P2_APPS || '/workspace/matt-s-apps-';
const LAB_DIR = path.join(LESSONS, 'Science_Teesside/Build/v4_fieldops');
const STUDIO = path.join(APPS, 'FieldOps_Teacher_Studio.html');
const WILTON = path.join(LAB_DIR, '03_Wilton_Carbon_Process_Control_Lab.html');
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'p2split-'));

const rows = [];
const row = (id, what, ok, detail) => rows.push({ id, what, ok, detail });

/* R0.7 — assert both halves are where the split says, before measuring across it */
for (const [id, p] of [['S0a', STUDIO], ['S0b', WILTON]])
  row(id, `subject present at its post-split path: ${p.replace(/^.*(matt-s-apps-|Lessons)/, '$1')}`,
    fs.existsSync(p), fs.existsSync(p) ? `${fs.statSync(p).size} bytes` : 'ABSENT — the split did not place it');
if (rows.some(r => !r.ok)) { report(); process.exit(1); }

const browser = await chromium.launch();
async function open(file) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const pg = await ctx.newPage();
  const errs = []; pg.on('pageerror', e => errs.push(String(e).slice(0, 140)));
  await pg.addInitScript(() => {
    window.__blobs = [];
    const orig = URL.createObjectURL.bind(URL);
    URL.createObjectURL = b => { window.__blobs.push(b); return orig(b); };
  });
  await pg.goto('file://' + file, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await pg.waitForTimeout(900);
  return { ctx, pg, errs };
}
const lastBlob = pg => pg.evaluate(async () =>
  window.__blobs.length ? await window.__blobs[window.__blobs.length - 1].text() : null);

/* ---- DIRECTION 1: Studio (Apps repo) -> lab (Lessons repo) --------------- */
const FEEDS = [14, 21, 24];
const minted = {};
{
  const { ctx, pg, errs } = await open(STUDIO);
  for (const feed of FEEDS) {
    const got = await pg.evaluate(async (f) => {
      const sleep = ms => new Promise(r => setTimeout(r, ms));
      const e = document.getElementById('engine');
      e.value = 'wilton-carbon-control'; e.dispatchEvent(new Event('change', { bubbles: true }));
      await sleep(250);
      const sel = document.querySelector('[data-scenario="feed"]');
      if (!sel || ![...sel.options].some(o => +o.value === f)) return { unavailable: true };
      sel.value = String(f); sel.dispatchEvent(new Event('input', { bubbles: true }));
      const t = document.getElementById('missionTitleInput');
      t.value = `AUTHORED SPLIT FIXTURE C${f}`; t.dispatchEvent(new Event('input', { bubbles: true }));
      await sleep(250);
      document.getElementById('exportMission').click();
      await sleep(350);
      return { ok: true };
    }, feed);
    if (got.unavailable) { minted[feed] = null; continue; }
    const text = await lastBlob(pg);
    /* the filename says what it is, so it can never be mistaken for a shipped sample */
    const p = path.join(TMP, `AUTHORED-BY-HARNESS_not-a-pack-sample_C${feed}.buildmission.json`);
    fs.writeFileSync(p, text);
    minted[feed] = p;
  }
  await ctx.close();
  row('S1a', 'the Studio, at its Matt-s-Apps- path, mints missions for every new feed',
    FEEDS.every(f => minted[f]) && errs.length === 0,
    FEEDS.map(f => `C${f}=${minted[f] ? path.basename(minted[f]) : 'UNAVAILABLE'}`).join(' · '));
}

for (const feed of FEEDS) {
  if (!minted[feed]) continue;
  const { ctx, pg, errs } = await open(WILTON);
  await pg.setInputFiles('#missionFile', minted[feed]);
  await pg.waitForTimeout(900);
  const got = await pg.evaluate(() => ({
    title: (document.getElementById('missionTitle') || {}).textContent || '',
    feed: (document.getElementById('wFeedRead').textContent || '').trim(),
    selected: [...document.querySelectorAll('.feedW.selected')].map(b => b.dataset.feed),
  }));
  await ctx.close();
  row(`S1b C${feed}`, `a mission minted in Matt-s-Apps- loads into the lab in Lessons`,
    got.title === `AUTHORED SPLIT FIXTURE C${feed}` && got.feed === `C${feed}H${2 * feed + 2}` && errs.length === 0,
    `title "${got.title}" feed "${got.feed}" selected [${got.selected}]`);
}

/* ---- DIRECTION 2: lab (Lessons repo) -> Studio (Apps repo) --------------- */
let capsule = null;
{
  const { ctx, pg, errs } = await open(WILTON);
  await pg.evaluate(async () => {
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    const set = (id, v) => { const e = document.getElementById(id); if (!e) return; e.value = v;
      e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); };
    set('alias', 'SPLIT PROBE');
    document.querySelector('.feedW[data-feed="21"]').click();
    const furn = document.getElementById('wFurnace');
    furn.value = furn.max; furn.dispatchEvent(new Event('input', { bubbles: true }));
    await sleep(120);
    document.getElementById('runDistil').click(); await sleep(250);
    document.getElementById('recordWRun').click(); await sleep(250);
    set('claimText', 'C21 condensed in the fuel-oil range.');
    await sleep(200);
    document.getElementById('exportJSON').click(); await sleep(400);
  });
  const text = await lastBlob(pg);
  capsule = path.join(TMP, 'AUTHORED-BY-HARNESS_not-a-pack-sample_capsule.json');
  if (text) fs.writeFileSync(capsule, text);
  await ctx.close();
  row('S2a', 'the lab, at its Lessons path, exports an evidence capsule',
    !!text && errs.length === 0, text ? `${text.length} bytes` : 'no blob captured');
}
if (capsule && fs.existsSync(capsule)) {
  const { ctx, pg, errs } = await open(STUDIO);
  await pg.setInputFiles('#capsuleFiles', capsule);
  await pg.waitForTimeout(1200);
  const got = await pg.evaluate(() => [...document.querySelectorAll('#capsuleRows tr')]
    .map(tr => tr.textContent.replace(/\s+/g, ' ').trim()).filter(t => /SPLIT PROBE/.test(t)));
  await ctx.close();
  row('S2b', 'a capsule from the lab in Lessons verifies in the Studio in Matt-s-Apps-',
    got.length === 1 && /verified/.test(got[0]) && !/changed \/ invalid/.test(got[0]) && errs.length === 0,
    got.length ? got[0].slice(0, 130) : 'no row imported');
}

/* ---- the NAV-1 link, resolved against the real Lessons tree -------------- */
{
  const src = fs.readFileSync(WILTON, 'utf8');
  const m = src.match(/<a class="mbmhome" href="([^"]+)"/);
  const target = m ? path.resolve(LAB_DIR, m[1]) : null;
  row('S3', 'NAV-1 from the placed lab resolves to a file that exists in Lessons',
    !!target && fs.existsSync(target),
    target ? `${m[1]} -> ${target.replace(LESSONS + '/', '')} (exists: ${fs.existsSync(target)})` : 'no NAV-1 link found');
  /* and it is the same target the eleven neighbours point at */
  const nb = path.join(LESSONS, 'Science_Teesside/Build/v3_40min/SCI_B_W3A_Backbones_Explore.html');
  const nm = fs.existsSync(nb) ? (fs.readFileSync(nb, 'utf8').match(/<a class="mbmhome" href="([^"]+)"/) || [])[1] : null;
  row('S3b', 'and it is the identical href its co-located neighbours use',
    !!nm && !!m && nm === m[1], `neighbour "${nm}" vs placed "${m && m[1]}"`);
}

await browser.close();
function report() {
  console.log(`${'id'.padEnd(11)} verdict  what`);
  console.log('-'.repeat(78));
  for (const r of rows) {
    console.log(`${r.id.padEnd(11)} ${(r.ok ? 'PASS' : 'FAIL').padEnd(8)} ${r.what}`);
    console.log(`            ${r.detail}`);
  }
  const bad = rows.filter(r => !r.ok);
  console.log(`\n${bad.length} split-transport failure(s)`);
  console.log(`\nEVERY FIXTURE ABOVE IS AUTHORED BY THIS HARNESS. The pack's own twelve`);
  console.log(`.buildmission.json samples were never shipped, so none was available to use.`);
  console.log(`Fixtures in ${TMP}, named AUTHORED-BY-HARNESS_not-a-pack-sample_*.`);
  return bad.length;
}
process.exit(report() ? 1 : 0);
