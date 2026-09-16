/* EDU-D2: exercise the real hub with current catalogue, supplement and title map. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '../..');
const read = p => fs.readFileSync(path.join(root, p), 'utf8');
const map = JSON.parse(read('assets/catalogue/display-titles.json'));
async function hub(mode) {
  const context = { console, URLSearchParams, Date, document: {}, fetch: async url => {
    if (url.endsWith('display-titles.json')) {
      if (mode === 'missing') return {ok: false, status: 404};
      const value = structuredClone(map);
      if (mode === 'stale') Object.values(value.entries).forEach(e => { e.originalTitle += ' obsolete'; });
      return {ok: true, json: async () => value};
    }
    try { const value = JSON.parse(read(url)); return {ok: true, json: async () => value}; }
    catch (_) { return {ok: false, status: 404}; }
  }};
  context.window = context;
  vm.runInNewContext(read('assets/catalogue/hub.js'), context);
  await context.MBM_HUB.loadAll();
  return context.MBM_HUB;
}
(async () => {
  const H = await hub('current');
  // Two guarded entries per reviewed companion pair, derived from the placement manifest
  // (116 pairs at EDU-D2; 118 after the EDU-Q1 companions of CX2 §5.3), never a typed count.
  const pairs = JSON.parse(read('data/companion-packs.json')).packs.length;
  assert.equal(Object.keys(map.entries).length, 2 * pairs);
  for (const [file, entry] of Object.entries(map.entries)) {
    const row = H.state.rows.find(r => r._path === file);
    assert.ok(row, file);
    assert.equal(H.displayTitle(row), entry.displayTitle, file);
    assert.equal(row.title, entry.originalTitle, 'Original title must survive');
    for (const q of [entry.displayTitle, entry.originalTitle, file]) {
      assert.ok(H.flatFilter(new URLSearchParams({q}), H.state.rows).some(r => r._path === file), q);
    }
    if (entry.displayTitle !== entry.originalTitle) assert.ok(H.referenceDetail(row).includes(H.esc(entry.originalTitle)));
    assert.ok(H.lessonRow(row).includes(H.esc(H.safeHref(file))), 'Canonical target must survive');
  }
  for (const mode of ['missing', 'stale']) {
    const fallback = await hub(mode);
    for (const r of fallback.state.rows) assert.equal(fallback.displayTitle(r), r.title || '', mode);
  }
  assert.equal(H.flatFilter(new URLSearchParams({q:'edud2-no-such-topic-9af68'}), H.state.rows).length, 0);
  console.log('PASS: ' + Object.keys(map.entries).length + ' titles for ' + pairs + ' companion pairs, topic/original/path search, canonical links, reference details, missing/stale map fallback and empty results.');
})().catch(e => { console.error(e); process.exitCode = 1; });
