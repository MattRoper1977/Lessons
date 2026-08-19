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

/* ---- S2c: the tamper negative control -----------------------------------
 * S2b proves a good capsule verifies. On its own that is satisfied just as well
 * by a verifier that says "verified" to everything, which is the failure mode
 * an integrity receipt exists to rule out. So: mutate one field of the capsule
 * the lab actually exported and require the Studio to REFUSE it. */
if (capsule && fs.existsSync(capsule)) {
  const doc = JSON.parse(fs.readFileSync(capsule, 'utf8'));
  doc.evidence.claim = 'TAMPERED — this sentence was never written by the pupil';
  const bad = path.join(TMP, 'AUTHORED-BY-HARNESS_not-a-pack-sample_capsule_TAMPERED.json');
  fs.writeFileSync(bad, JSON.stringify(doc, null, 2));
  const { ctx, pg } = await open(STUDIO);
  await pg.setInputFiles('#capsuleFiles', bad);
  await pg.waitForTimeout(1200);
  const got = await pg.evaluate(() => [...document.querySelectorAll('#capsuleRows tr')]
    .map(tr => tr.textContent.replace(/\s+/g, ' ').trim()).filter(t => /SPLIT PROBE/.test(t)));
  await ctx.close();
  row('S2c', 'CONTROL — a tampered capsule is REFUSED by the same import path',
    got.length === 1 && /changed \/ invalid/.test(got[0]),
    got.length ? got[0].slice(0, 130) : 'no row imported');
}

/* ---- S4: THE LAUNCH LINK ITSELF, ACROSS TWO REAL ORIGINS ----------------
 *
 * WHY THIS EXISTS, and why its absence let a 404 ship. Everything above proves
 * the FILE-IMPORT transport: it hands the lab a .buildmission.json through
 * #missionFile and builds the lab's URL itself. So the OTHER transport — the
 * one the Studio's own "Launch mission" anchor uses — was never exercised, and
 * the bare filename in the engine table sat there through a green harness.
 *
 * The two origins are real and different: the Apps tree is served on one port,
 * the Lessons tree on another. The Studio under test is the SHIPPED build,
 * carrying its production absolute URL; requests to that production origin are
 * intercepted and fulfilled from the Lessons server, which is what a browser on
 * madebymatt.uk would get. So this proves the string as shipped, not a rewrite
 * of it invented for the test. */
{
  const http = await import('node:http');
  const serve = root => new Promise(res => {
    const srv = http.createServer((rq, rs) => {
      const rel = decodeURIComponent(rq.url.split('?')[0].split('#')[0]).replace(/^\/+/, '');
      const f = path.join(root, rel);
      if (!f.startsWith(root) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { rs.writeHead(404); return rs.end('no'); }
      rs.writeHead(200, { 'content-type': 'text/html; charset=utf-8' }); rs.end(fs.readFileSync(f));
    }).listen(0, '127.0.0.1', () => res(srv));
  });
  const [sApps, sLessons] = [await serve(APPS), await serve(LESSONS)];
  const [pApps, pLessons] = [sApps.address().port, sLessons.address().port];
  const PROD = 'https://madebymatt.uk/Lessons/';

  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  /* fulfil the production origin from the Lessons server — same bytes, same
     paths, and still a different origin from the Studio's. */
  await ctx.route(u => u.href.startsWith(PROD), async route => {
    const rel = route.request().url().slice(PROD.length).split('#')[0];
    const r = await fetch(`http://127.0.0.1:${pLessons}/${rel}`).catch(() => null);
    if (!r || !r.ok) return route.fulfill({ status: 404, body: 'absent' });
    route.fulfill({ status: 200, contentType: 'text/html; charset=utf-8', body: Buffer.from(await r.arrayBuffer()) });
  });
  const pg = await ctx.newPage();
  const errs = []; pg.on('pageerror', e => errs.push(String(e).slice(0, 140)));
  await pg.goto(`http://127.0.0.1:${pApps}/FieldOps_Teacher_Studio.html`, { waitUntil: 'domcontentloaded' });
  await pg.waitForTimeout(400);

  /* mint an authored mission on the Wilton engine, then read the anchor the
     teacher would actually click */
  await pg.evaluate(() => {
    const set = (id, v) => { const e = document.getElementById(id); e.value = v;
      e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); };
    set('engine', 'wilton-carbon-control');
    document.getElementById('engine').dispatchEvent(new Event('change', { bubbles: true }));
  });
  await pg.waitForTimeout(300);
  await pg.evaluate(() => {
    const set = (id, v) => { const e = document.getElementById(id); e.value = v;
      e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); };
    set('missionTitleInput', 'AUTHORED LAUNCH-LINK FIXTURE');
    set('missionQuestionInput', 'Does the launch link survive the split?');
  });
  await pg.waitForTimeout(400);
  const href = await pg.getAttribute('#launchMission', 'href');
  const sameOrigin = href && href.startsWith(PROD);
  row('S4a', 'the Studio\'s Launch anchor points at the labs\' live Lessons origin, not a bare filename',
    !!sameOrigin && /#mission=/.test(href),
    href ? href.slice(0, 118) + '…' : 'no href');

  /* follow it exactly as a click would, and read what the lab received */
  const lab = await ctx.newPage();
  const labErrs = []; lab.on('pageerror', e => labErrs.push(String(e).slice(0, 140)));
  let status = 'no navigation';
  if (href) {
    const resp = await lab.goto(href, { waitUntil: 'domcontentloaded' }).catch(e => { status = String(e).slice(0, 90); return null; });
    if (resp) status = `HTTP ${resp.status()}`;
    await lab.waitForTimeout(900);
  }
  const got = await lab.evaluate(() => ({
    title: (document.getElementById('missionTitle') || {}).textContent || '',
    q: (document.getElementById('missionQuestion') || {}).textContent || '',
  })).catch(() => ({ title: '', q: '' }));
  row('S4b', 'following that link opens the right lab on the other origin with the mission populated',
    status === 'HTTP 200' && got.title === 'AUTHORED LAUNCH-LINK FIXTURE' && labErrs.length === 0,
    `${status} · title "${got.title}" · question "${(got.q || '').slice(0, 40)}"`);

  /* NEGATIVE CONTROL: the same journey with the pre-T16 bare filename must fail
     on the Apps origin. Without this the row above proves only that some URL
     works, not that the OLD one was broken. */
  const bare = await ctx.newPage();
  const bareResp = await bare.goto(`http://127.0.0.1:${pApps}/03_Wilton_Carbon_Process_Control_Lab.html`,
    { waitUntil: 'domcontentloaded' }).catch(() => null);
  row('S4c', 'CONTROL — the pre-T16 bare filename still 404s on the Apps origin',
    !!bareResp && bareResp.status() === 404, bareResp ? `HTTP ${bareResp.status()}` : 'no response');

  await ctx.close();
  sApps.close(); sLessons.close();
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
