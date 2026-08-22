// §9.3b — the two measurements that decide how the UAS Register ships.
//
// 1. STORAGE-ORIGIN GATE. The Register keeps everything in IndexedDB, which Chrome
//    blocks or gives an opaque origin on file:// and on many UNC/network-share
//    paths. Probed the way staff will actually open it: double-click from the
//    share. Write, RELOAD, read back - a write that succeeds and does not survive
//    a reload is the failure that silently discards pupil evidence.
//
// 2. OFFLINE-CAPABILITY CENSUS. Measured at RUNTIME with the network blocked, not
//    by grepping <script src>: that misses the wasm, the worker and the language
//    data, which is most of what the OCR path actually loads.
import { chromium } from 'playwright';
import path from 'path';
import { pathToFileURL } from 'url';

const target = process.argv[2];
if (!target) { console.error('usage: uas_probe.mjs PATH_TO_app.html'); process.exit(2); }
const url = pathToFileURL(path.resolve(target)).href;

const browser = await chromium.launch();
const ctx = await browser.newContext();

// Block every non-file request and record what was attempted.
const external = [];
await ctx.route('**/*', (route) => {
  const u = route.request().url();
  if (u.startsWith('file://') || u.startsWith('data:') || u.startsWith('blob:')) return route.continue();
  external.push(u);
  return route.abort();
});

const page = await ctx.newPage();
const errs = [];
// A local asset that fails to load is NOT an external origin, so the census above
// reports a clean zero whether or not the vendored libraries actually shipped.
// That is exactly how the register was first packed without its vendor/ folder.
const failedLocal = [];
page.on('requestfailed', r => {
  const u = r.url();
  if (u.startsWith('file://')) failedLocal.push(`${r.failure()?.errorText}  ${u}`);
});
page.on('pageerror', e => errs.push('pageerror: ' + e.message));
page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });

await page.goto(url, { waitUntil: 'load', timeout: 45000 });
await page.waitForTimeout(2500);

// --- storage-origin gate ---------------------------------------------------
const origin = await page.evaluate(() => location.origin);
const idb = await page.evaluate(async () => {
  const r = { available: typeof indexedDB !== 'undefined', opened: false, wrote: false, error: null };
  if (!r.available) return r;
  try {
    const db = await new Promise((res, rej) => {
      const q = indexedDB.open('__probe__', 1);
      q.onupgradeneeded = () => q.result.createObjectStore('s');
      q.onsuccess = () => res(q.result);
      q.onerror = () => rej(q.error || new Error('open failed'));
      setTimeout(() => rej(new Error('open timed out')), 5000);
    });
    r.opened = true;
    await new Promise((res, rej) => {
      const tx = db.transaction('s', 'readwrite');
      tx.objectStore('s').put({ probe: 'peq-year-3' }, 'k');
      tx.oncomplete = res; tx.onerror = () => rej(tx.error);
    });
    r.wrote = true;
  } catch (e) { r.error = String(e && e.message || e); }
  return r;
});

// reload, then read back: a write that does not survive is worse than a failed one
await page.reload({ waitUntil: 'load' });
await page.waitForTimeout(1200);
const persisted = await page.evaluate(async () => {
  try {
    const db = await new Promise((res, rej) => {
      const q = indexedDB.open('__probe__', 1);
      q.onsuccess = () => res(q.result);
      q.onerror = () => rej(q.error);
      setTimeout(() => rej(new Error('timeout')), 5000);
    });
    if (!db.objectStoreNames.contains('s')) return { survived: false, why: 'store gone' };
    const v = await new Promise((res, rej) => {
      const g = db.transaction('s').objectStore('s').get('k');
      g.onsuccess = () => res(g.result); g.onerror = () => rej(g.error);
    });
    return { survived: !!(v && v.probe === 'peq-year-3'), value: v || null };
  } catch (e) { return { survived: false, why: String(e && e.message || e) }; }
});

// --- what the packed copy holds -------------------------------------------
const records = await page.evaluate(async () => {
  const out = {};
  try {
    const names = (await indexedDB.databases?.()) || [];
    out.databases = names.map(d => d.name);
    for (const d of names) {
      if (!d.name || d.name === '__probe__') continue;
      const db = await new Promise((res, rej) => {
        const q = indexedDB.open(d.name);
        q.onsuccess = () => res(q.result); q.onerror = () => rej(q.error);
        setTimeout(() => rej(new Error('timeout')), 4000);
      });
      out[d.name] = {};
      for (const s of Array.from(db.objectStoreNames)) {
        const n = await new Promise((res) => {
          const c = db.transaction(s).objectStore(s).count();
          c.onsuccess = () => res(c.result); c.onerror = () => res('err');
        });
        out[d.name][s] = n;
      }
    }
  } catch (e) { out.error = String(e && e.message || e); }
  try {
    out.localStorageKeys = Object.keys(localStorage).length;
    out.localStorageSample = Object.keys(localStorage).slice(0, 12);
  } catch (e) { out.localStorageKeys = 'blocked'; }
  return out;
});

await browser.close();

console.log('URL                ', url);
console.log('location.origin    ', JSON.stringify(origin));
console.log('');
console.log('STORAGE-ORIGIN GATE');
console.log('  indexedDB present', idb.available);
console.log('  opened           ', idb.opened);
console.log('  wrote            ', idb.wrote);
console.log('  error            ', idb.error);
console.log('  survived reload  ', persisted.survived, persisted.why ? `(${persisted.why})` : '');
console.log('');
console.log('OFFLINE-CAPABILITY CENSUS (network blocked)');
console.log('  external origins attempted at runtime:', external.length);
[...new Set(external)].slice(0, 20).forEach(u => console.log('    ', u));
console.log('  local assets that FAILED to load:', failedLocal.length);
[...new Set(failedLocal)].slice(0, 10).forEach(f => console.log('    ', f));
console.log('');
console.log('EMPTY-REGISTER PROOF (read by LOADING the copy, not by reading its source)');
console.log('  ', JSON.stringify(records));
console.log('');
console.log('page errors:', errs.length);
errs.slice(0, 8).forEach(e => console.log('   ', e.slice(0, 160)));

const verdict = {
  storage_ok: idb.available && idb.opened && idb.wrote && persisted.survived,
  offline_ok: external.length === 0 && failedLocal.length === 0,
  empty: true,
};
console.log('');
console.log('VERDICT storage_ok=%s offline_ok=%s', verdict.storage_ok, verdict.offline_ok);
