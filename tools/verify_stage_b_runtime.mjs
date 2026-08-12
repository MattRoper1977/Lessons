#!/usr/bin/env node
/*
 * Stage B runtime gate — the newly-covered decks, driven in a real browser.
 *
 * The include is proven inert by tools/stage_b_announcer.py --prove (exact
 * diff). This asserts the other half: that mounting the HUD on a deck that
 * never carried it does what it should and nothing it should not.
 *
 * Per deck, at a phone and a desktop viewport:
 *   1. the HUD mounts and the deck still boots with no page errors
 *   2. advancing a slide produces EXACTLY ONE polite announcement
 *   3. loading the deck produces ZERO announcements
 *   4. a running countdown produces ZERO announcements
 *   5. typing in the HUD does not move the deck (the guard is live here too)
 *   6. the deck's own controls are not duplicated by the HUD
 *   7. the deck's own keyboard handlers still work outside the HUD
 *   8. rendered print text is IDENTICAL to the same deck served without the
 *      include — this is the dialect nprint.js cannot reach, because it runs
 *      from file:// where hud.js 404s and therefore never mounts
 *
 * Served over HTTP with /hud.js mounted at the domain root, which is the only
 * condition under which any of this is true in a classroom.
 *
 *   node tools/verify_stage_b_runtime.mjs <population-dir> [more...]
 *   node tools/verify_stage_b_runtime.mjs --files a.html b.html
 *   SITE=/path/to/site node tools/verify_stage_b_runtime.mjs ...
 */
import { createRequire } from 'node:module';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';

const require = createRequire(import.meta.url);
function loadPlaywright() {
  for (const p of ['playwright', '/opt/node22/lib/node_modules/playwright']) {
    try { return require(p); } catch (_) { /* keep looking */ }
  }
  console.error('playwright not found. Install it with:  npm i -g playwright');
  process.exit(2);
}
const { chromium } = loadPlaywright();

const LESSONS = '/home/user/Lessons';
const SITE = process.env.SITE || '/workspace/mattroper1977.github.io';
const BASE_REF = process.env.BASE_REF || 'origin/main';
const MAX = Number(process.env.MAX_PER_POP || 4);   // decks sampled per population

const argv = process.argv.slice(2);
let FILES = [];
if (argv[0] === '--files') {
  FILES = argv.slice(1);
} else {
  for (const dir of argv) {
    const abs = path.join(LESSONS, dir);
    const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).flatMap((e) =>
      e.isDirectory() ? walk(path.join(d, e.name))
        : (e.name.endsWith('.html') ? [path.join(d, e.name)] : []));
    // Only decks THIS pass newly covered. Sampling files that already loaded
    // hud.js would prove nothing about the change being made here.
    const changed = new Set(execSync(`git -C ${LESSONS} diff --name-only ${BASE_REF} -- '*.html'`,
      { encoding: 'utf8' }).split('\n').filter(Boolean));
    const all = walk(abs).map((f) => path.relative(LESSONS, f)).filter((f) => changed.has(f));
    // first, middle and last of the population, plus one more — a sample that
    // straddles the ends rather than four neighbours from the same folder
    const pick = [];
    if (all.length) {
      const idx = [0, Math.floor(all.length / 3), Math.floor((2 * all.length) / 3), all.length - 1];
      for (const i of [...new Set(idx)].slice(0, MAX)) pick.push(all[i]);
    }
    FILES.push(...pick);
  }
}
if (!FILES.length) { console.error('no files selected'); process.exit(2); }

const MIME = { '.html':'text/html', '.js':'text/javascript', '.css':'text/css',
               '.json':'application/json', '.svg':'image/svg+xml', '.png':'image/png',
               '.webp':'image/webp', '.jpg':'image/jpeg', '.gif':'image/gif', '.mp3':'audio/mpeg' };

/* Serves the Lessons tree at /Lessons/ (where the domain mounts it, and what
   hud.js keys its lesson mode off) with /hud.js from the site repo. */
function serve() {
  return new Promise((resolve) => {
    const s = http.createServer((req, res) => {
      let rel = decodeURIComponent(req.url.split('?')[0]);
      if (rel.endsWith('/')) rel += 'index.html';
      const file = rel === '/hud.js' ? path.join(SITE, 'hud.js')
                 : path.join(LESSONS, rel.replace(/^\/Lessons\//, '/'));
      if (!fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); res.end(); return; }
      res.writeHead(200, { 'content-type': MIME[path.extname(file)] || 'application/octet-stream' });
      fs.createReadStream(file).pipe(res);
    });
    s.listen(0, '127.0.0.1', () => resolve(s));
  });
}

const failures = [];
const rows = [];
const assert = (c, m) => { if (!c) failures.push(m); return !!c; };

/* Record every write into a polite live region as an assistive technology
   would receive it, rather than reading the DOM once at the end. */
const RECORDER = () => {
  window.__spoken = [];
  window.__watch = (n) => new MutationObserver(() => {
    const t = (n.textContent || '').trim();
    if (t) window.__spoken.push({ id: n.id || 'anon', text: t });
  }).observe(n, { childList: true, characterData: true, subtree: true });
  document.querySelectorAll('[aria-live="polite"],[aria-live="assertive"]').forEach(window.__watch);
};

const slideIndex = (p) => p.evaluate(() => {
  const all = document.querySelectorAll('.slide');
  for (let i = 0; i < all.length; i++) {
    if (all[i].classList.contains('active') || all[i].classList.contains('show')
        || getComputedStyle(all[i]).display !== 'none') return i;
  }
  return -1;
});

async function printText(page, url) {
  await page.emulateMedia({ media: 'print' });
  await page.goto(url, { waitUntil: 'load' });
  await page.waitForTimeout(400);
  const t = await page.evaluate(() => document.body.innerText);
  await page.emulateMedia({ media: null });
  return t;
}

const server = await serve();
const BASEURL = `http://127.0.0.1:${server.address().port}`;
const browser = await chromium.launch();

/* A second tree holding each file exactly as it is at the base ref, served the
   same way, so print can be compared WITH the HUD available on both sides. */
const baseDir = fs.mkdtempSync(path.join(process.env.TMPDIR || '/tmp', 'stageb-base-'));
for (const rel of FILES) {
  const dst = path.join(baseDir, rel);
  fs.mkdirSync(path.dirname(dst), { recursive: true });
  try { fs.writeFileSync(dst, execSync(`git -C ${LESSONS} show ${BASE_REF}:'${rel}'`, { maxBuffer: 1 << 28 })); }
  catch (_) { /* new file at this ref; skipped below */ }
}
const baseServer = http.createServer((req, res) => {
  let rel = decodeURIComponent(req.url.split('?')[0]);
  /* Only the file under test is pinned at the base ref. Everything else — the
     sibling *-svg.js an animation demo loads, images, shared CSS — is identical
     on both sides and is served from the live tree.
     Not doing this is a real trap, and it caught the reused nprint.js: that
     instrument copies the base file alone into /tmp, where its siblings do not
     exist, so the base never initialises and prints SHORTER text. It reported
     build-anim/demo.html and grow-anim/demo.html as print regressions when
     rendering the same base copy in its own directory gives byte-identical
     output (5751 = 5751, 9136 = 9136, zero page errors on both sides). */
  let file = rel === '/hud.js' ? path.join(SITE, 'hud.js')
           : path.join(baseDir, rel.replace(/^\/Lessons\//, '/'));
  if (!fs.existsSync(file)) {
    file = rel === '/hud.js' ? file : path.join(LESSONS, rel.replace(/^\/Lessons\//, '/'));
  }
  if (!fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { 'content-type': MIME[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});
await new Promise((r) => baseServer.listen(0, '127.0.0.1', r));
const BASEURL2 = `http://127.0.0.1:${baseServer.address().port}`;

const VIEWPORTS = [
  { name: 'phone',   width: 390,  height: 844 },
  { name: 'desktop', width: 1280, height: 800 },
];

try {
  for (const rel of FILES) {
    const url = `${BASEURL}/Lessons/${rel.split(path.sep).map(encodeURIComponent).join('/')}`;
    for (const vp of VIEWPORTS) {
      const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
      const page = await ctx.newPage();
      const errs = [];
      page.on('pageerror', (e) => errs.push(e.message));
      await page.goto(url, { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(1000);

      const tag = `${vp.name} ${path.basename(rel)}`;
      // 1. HUD mounted, deck alive
      const mounted = await page.evaluate(() => ({
        dock: !!document.getElementById('mbmhud-dock'),
        say: !!document.getElementById('mbmhud-say'),
        slides: document.querySelectorAll('.slide').length,
      }));
      if (!assert(mounted.dock, `${tag}: the HUD did not mount`)) { await ctx.close(); continue; }
      assert(mounted.slides > 1, `${tag}: only ${mounted.slides} slide(s) found`);
      assert(mounted.say, `${tag}: no live region — the announcer did not arm`);

      // 6. the HUD must not duplicate the deck's own chassis controls
      const dupes = await page.evaluate(() => {
        const ids = ['mbmhud-dock', 'mbmhud-pill', 'mbmhud-timerbox', 'mbmhud-calm', 'mbmhud-say'];
        return ids.map((i) => [i, document.querySelectorAll('#' + i).length])
                  .filter(([, n]) => n !== 1);
      });
      assert(dupes.length === 0, `${tag}: duplicated HUD controls ${JSON.stringify(dupes)}`);

      // 3. arriving announces nothing
      await page.evaluate(RECORDER);
      await page.waitForTimeout(600);
      assert(await page.evaluate(() => window.__spoken.length) === 0,
        `${tag}: announced on first load without a slide change`);

      // 2 + 7. one announcement per change, and the deck's own keys still work
      await page.evaluate(() => { window.__spoken.length = 0; });
      const before = await slideIndex(page);
      await page.evaluate(() => { const s = document.querySelector('.slide');
        if (s) { s.setAttribute('tabindex', '-1'); s.focus(); } });
      await page.keyboard.press('ArrowRight');
      await page.waitForTimeout(900);
      const after = await slideIndex(page);
      const spoken = await page.evaluate(() =>
        window.__spoken.filter((s) => s.id === 'mbmhud-say'));
      assert(after === before + 1,
        `${tag}: ArrowRight outside the HUD moved the deck ${before} -> ${after}`);
      assert(spoken.length === 1,
        `${tag}: ${spoken.length} announcement(s) for one slide change ` +
        `(${JSON.stringify(spoken.map((s) => s.text).slice(0, 2))})`);

      // 5. typing in the HUD must not move the deck
      await page.evaluate(() => {
        document.getElementById('mbmhud-pill').click();
        const ta = document.getElementById('mbmhud-names'); if (ta) ta.style.display = 'block';
      });
      await page.waitForTimeout(250);
      const beforeType = await slideIndex(page);
      await page.focus('#mbmhud-names');
      await page.keyboard.type('Ada');
      for (let i = 0; i < 3; i++) await page.keyboard.press('ArrowRight');
      await page.keyboard.press(' ');
      await page.waitForTimeout(350);
      assert(await slideIndex(page) === beforeType,
        `${tag}: typing in the HUD moved the deck`);
      assert((await page.inputValue('#mbmhud-names')).startsWith('Ada'),
        `${tag}: the name list lost its text`);

      // 4. a running countdown announces nothing
      await page.evaluate(() => { window.__spoken.length = 0; });
      const timerLive = await page.evaluate(() => {
        const t = document.getElementById('mbmhud-timerbox');
        return t ? t.getAttribute('aria-live') : null;
      });
      assert(timerLive === 'off', `${tag}: countdown is aria-live="${timerLive}"`);
      await page.evaluate(() => {
        const b = document.querySelector('#mbmhud-dock [data-min="5"]'); if (b) b.click();
        document.querySelectorAll('[aria-live]').forEach((n) => {
          if (n.getAttribute('aria-live') !== 'off' && window.__watch) window.__watch(n);
        });
      });
      await page.waitForTimeout(3200);
      assert(await page.evaluate(() =>
        window.__spoken.filter((s) => /time/i.test(s.id)).length) === 0,
        `${tag}: the running countdown announced`);

      assert(errs.length === 0, `${tag}: page errors: ${errs.slice(0, 2).join(' | ')}`);
      if (vp.name === 'desktop') {
        rows.push({ rel, slides: mounted.slides,
                    said: spoken.length ? spoken[0].text.slice(0, 46) : '(none)' });
      }
      await ctx.close();
    }

    // 8. print WITH the HUD mounted, both sides over HTTP
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await ctx.newPage();
    const relUrl = rel.split(path.sep).map(encodeURIComponent).join('/');
    const now = await printText(page, `${BASEURL}/Lessons/${relUrl}`);
    const was = await printText(page, `${BASEURL2}/Lessons/${relUrl}`);
    assert(now === was,
      `print text changed with the HUD mounted: ${path.basename(rel)} ` +
      `(${was.length} -> ${now.length} chars)`);
    await ctx.close();
  }
} finally {
  await browser.close();
  server.close();
  baseServer.close();
  fs.rmSync(baseDir, { recursive: true, force: true });
}

for (const r of rows) {
  console.log(`  ${String(r.slides).padStart(3)} slides  said ${JSON.stringify(r.said)}  ${r.rel}`);
}
if (failures.length) {
  console.error(`\n[FAIL] Stage B runtime — ${failures.length} finding(s):`);
  for (const f of failures.slice(0, 20)) console.error('   - ' + f);
  process.exit(1);
}
console.log(`\n[PASS] Stage B runtime: ${FILES.length} deck(s) x ${VIEWPORTS.length} viewports — ` +
            'HUD mounts, one announcement per slide change, none on load, none from the ' +
            'countdown, typing safe, deck keys intact, print identical with the HUD mounted');
