/* ---------------------------------------------------------------------------
   verify_toolkits_offline.mjs — the S3.B check, committed so it stops being
   reinvented every term.

   The UAS Register and the ASDAN Register ship to schools as OFFLINE copies on
   a network share. This proves they actually work that way rather than
   assuming it:

     1. strip the hud.js loader (it only ever loads from the public origin, so
        offline it is dead weight that produces a failed request on every open)
     2. neutralise site-root navigation (href="/" points at the filesystem root
        when a page is opened from a folder rather than a web server)
     3. census every remaining external reference and classify it
     4. open every page from file:// with the network fully blocked and assert
        zero failed requests, zero page errors, and that the app actually boots

   THE CONTROL IS THE POINT, AND IT WAS WRONG THE FIRST TIME.

   The first version of this check counted only NON-file:// failed requests. On
   a file:// page, src="/hud.js" resolves to file:///hud.js — so the very thing
   the check exists to catch was filtered out as "local", and the unstripped
   originals passed exactly like the stripped copies. It counts EVERY failed
   request now, and --self-test proves that by running the same probe against
   the pristine copies and requiring them to go red.

   A check that cannot fail tells you nothing. This one is made to prove it can.

   Usage:
     SITE_DIR=/path/to/site node tools/verify_toolkits_offline.mjs
     SITE_DIR=/path/to/site node tools/verify_toolkits_offline.mjs --self-test
     SITE_DIR=... OUT_DIR=... node tools/verify_toolkits_offline.mjs --emit
        --emit also writes the offline tree to OUT_DIR for zipping.
   --------------------------------------------------------------------------- */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const SITE = process.env.SITE_DIR || '/workspace/site';
const OUT = process.env.OUT_DIR || '/tmp/toolkits-offline';
const SELF_TEST = process.argv.includes('--self-test');
const EMIT = process.argv.includes('--emit');
const TOOLKITS = ['uas', 'asdan'];

let red = 0;
const gate = (n, ok, d) => { if (!ok) red++; console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? `  — ${d}` : ''}`); return ok; };

/* ------------------------------ build the offline tree ------------------- */
function buildOffline() {
  if (fs.existsSync(OUT)) fs.rmSync(OUT, { recursive: true });
  fs.mkdirSync(OUT, { recursive: true });
  const census = { hudStripped: 0, absNavNeutralised: 0, files: 0, remote: {} };
  for (const name of TOOLKITS) {
    const src = path.join(SITE, name);
    if (!fs.existsSync(src)) { console.log(`SKIP: ${src} not present`); continue; }
    fs.cpSync(src, path.join(OUT, name), { recursive: true });
  }
  for (const p of walk(OUT).filter(f => f.endsWith('.html'))) {
    const raw = fs.readFileSync(p, 'utf8');
    let next = raw;
    const hud = (next.match(/<script[^>]*src=["']\/hud\.js["'][^>]*><\/script>/g) || []).length;
    next = next.replace(/<script[^>]*src=["']\/hud\.js["'][^>]*><\/script>/g,
      '<!-- hud.js loader removed for the offline copy: it only loads from the public site -->');
    const nav = (next.match(/href="\/(?:uas\/|asdan\/)?"/g) || []).length;
    next = next.replace(/href="\/(?:uas\/|asdan\/)?"/g,
      'href="#" data-offline-disabled="site navigation unavailable offline"');
    /* The truncation discipline: read fully -> transform -> ASSERT -> write.
       A write handle truncates first, and that destroyed a lesson once. */
    if (!next.trimEnd().endsWith('</html>')) throw new Error(`${p}: output would not end </html>`);
    if (next.length < raw.length * 0.5) throw new Error(`${p}: output shrank more than half`);
    if (next !== raw) fs.writeFileSync(p, next, 'utf8');
    census.hudStripped += hud; census.absNavNeutralised += nav; census.files++;
    for (const u of next.match(/https?:\/\/[^"' )]+/g) || []) census.remote[u] = (census.remote[u] || 0) + 1;
  }
  return census;
}
function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap(e => {
    const p = path.join(dir, e.name);
    return e.isDirectory() ? walk(p) : [p];
  });
}

/* ------------------------------ the offline probe ------------------------ */
async function probe(browser, label, file) {
  const ctx = await browser.newContext();
  /* Block everything that is not the local file itself. */
  await ctx.route('**/*', r => (r.request().url().startsWith('file://') ? r.continue() : r.abort()));
  const page = await ctx.newPage();
  const failed = [], errors = [];
  /* EVERY failed request, not just non-file ones. On file:// a root-absolute
     src="/hud.js" resolves to file:///hud.js, and filtering by scheme made this
     check blind to precisely what it exists to catch. */
  page.on('requestfailed', r => failed.push(r.url()));
  page.on('pageerror', e => errors.push(String(e.message).slice(0, 90)));
  await page.goto('file://' + file, { waitUntil: 'load' });
  await page.waitForTimeout(1200);
  const out = await page.evaluate(() => ({
    title: document.title,
    text: document.body.innerText.trim().length,
    controls: document.querySelectorAll('button, [role=button]').length
  }));
  await ctx.close();
  return { label, file, failed, errors, ...out };
}

/* ------------------------------------------------------------------------- */
const census = buildOffline();
console.log('offline build:', JSON.stringify({ files: census.files, hudStripped: census.hudStripped, absNavNeutralised: census.absNavNeutralised }));
console.log('remaining external references, classified:');
for (const [u, c] of Object.entries(census.remote).sort()) {
  const metaOnly = /og-cover|\/(uas|asdan)(\/app\.html)?\/?$/.test(u);
  console.log(`   ${String(c).padStart(2)}x ${u}  -> ${metaOnly ? 'META/CANONICAL only, not fetched on render' : 'REVIEW'}`);
}

const browser = await chromium.launch();
try {
  const pages = walk(OUT).filter(f => f.endsWith('.html'));
  gate('offline tree contains pages to test', pages.length > 0, `${pages.length} pages`);
  for (const f of pages) {
    const r = await probe(browser, path.relative(OUT, f), f);
    gate(`offline: ${r.label}`,
      r.failed.length === 0 && r.errors.length === 0 && r.text > 100,
      `text=${r.text} controls=${r.controls} failedRequests=${r.failed.length} errors=${r.errors.length}` +
      (r.failed.length ? ` -> ${r.failed.slice(0, 2).join(', ')}` : ''));
  }

  if (SELF_TEST) {
    console.log('\n--- negative control: the SAME probe against the pristine copies ---');
    let caught = 0, tried = 0;
    for (const name of TOOLKITS) {
      const f = path.join(SITE, name, 'app.html');
      if (!fs.existsSync(f)) continue;
      tried++;
      const r = await probe(browser, `pristine ${name}/app.html`, f);
      console.log(`   pristine ${name}/app.html  failedRequests=${r.failed.length}` +
        (r.failed.length ? ` -> ${r.failed.slice(0, 2).join(', ')}` : ''));
      if (r.failed.length > 0) caught++;
    }
    gate('CONTROL: the probe detects a live remote ref on the unstripped originals',
      tried > 0 && caught === tried,
      `${caught}/${tried} pristine copies reported a failed request (expected: all of them)`);
  }
} finally {
  await browser.close();
}

if (EMIT) console.log(`\noffline tree written to ${OUT}`);
console.log(`\n${red === 0 ? 'ALL TOOLKIT OFFLINE GATES GREEN' : `${red} RED`}`);
process.exit(red === 0 ? 0 : 1);
