const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.resolve(__dirname, '../..');
const here = __dirname;
const html = fs.readFileSync(path.join(root, 'Art_Teesside/Grow/GROW_ART_W4_Arts_Event_Attend_Capture_and_Review.html'), 'utf8');
const sourceReader = fs.readFileSync(path.join(root, 'tools/artsaward/slot_reader.js'), 'utf8');
const embedded = html.match(/<script data-award-slot-reader[^>]*>\n([\s\S]*?)\n<\/script>/)[1];
const adapter = html.match(/<script data-legacy-award-slots>\n([\s\S]*?)<\/script>/)[1];
assert.equal(embedded, sourceReader);
const base = JSON.parse(fs.readFileSync(path.join(root, 'tools/artsaward/SLOTS.json'), 'utf8'));
const rows = [];

class Element {
  constructor(tag) { this.tagName = tag; this.children = []; this.listeners = {}; this._text = ''; }
  set textContent(value) { this._text = String(value); this.children = []; }
  get textContent() { return this._text + this.children.map(child => child.textContent).join(''); }
  replaceChildren(...children) { this._text = ''; this.children = children; }
  appendChild(child) { this.children.push(child); return child; }
  addEventListener(type, callback) { this.listeners[type] = callback; }
}

const settle = () => new Promise(resolve => setImmediate(resolve));
function setup(fetcher, protocol = 'https:') {
  const nodes = Object.fromEntries(['award-slot-panel', 'award-slot-status', 'award-slot-rows', 'award-slot-file'].map(id => [id, new Element(id === 'award-slot-file' ? 'input' : 'div')]));
  const context = {
    document: {readyState:'complete', getElementById:id=>nodes[id], createElement:tag=>new Element(tag)},
    location:{protocol}, fetch:fetcher,
  };
  context.window = context;
  vm.createContext(context);
  vm.runInContext(embedded, context);
  vm.runInContext(adapter, context);
  return {nodes, status:()=>nodes['award-slot-status'].textContent, items:()=>nodes['award-slot-rows'].children.map(e=>e.textContent),
    async upload(text) { nodes['award-slot-file'].files = [{size:Buffer.byteLength(text), text:async()=>text}]; await nodes['award-slot-file'].listeners.change(); await settle(); }};
}
function fixture(org, event) {
  const doc = structuredClone(base);
  doc.slots.ORG_SLOT.entries = org ? [{name:org,route:'R3',status:'CONFIRMED'}] : [];
  doc.slots.EVENT_SLOT.entries = event ? [{name:event,route:'R3',status:'CONFIRMED'}] : [];
  return doc;
}
function ok(id, fn) { fn(); rows.push({id, verdict:'PASS'}); }

(async () => {
  let calls = [];
  let current = base;
  const fetcher = async (url, options) => { calls.push({url, options}); return {ok:true,json:async()=>structuredClone(current)}; };
  let app = setup(fetcher); await settle();
  ok('actual-current-source-is-unconfirmed', () => {
    assert.match(app.status(), /No confirmed event route.*preparation only/);
    assert.equal(app.items().length, 2);
    assert.match(app.items()[0], /^ORG_SLOT \(organisation reference\): no confirmed entry$/);
    assert.match(app.items()[1], /^EVENT_SLOT \(arts event or experience\): no confirmed entry$/);
  });
  ok('hosted-source-path-and-refresh-options', () => {
    assert.equal(calls[0].url, '../../tools/artsaward/SLOTS.json');
    assert.equal(calls[0].options.cache, 'no-store');
    assert.equal(calls[0].options.credentials, 'same-origin');
    assert.equal(path.resolve(root,'Art_Teesside/Grow',calls[0].url),path.join(root,'tools/artsaward/SLOTS.json'));
  });
  current = fixture('Fixture organisation only', null);
  app = setup(fetcher); await settle();
  ok('organisation-reference-does-not-confirm-attendance', () => {
    assert.match(app.items()[0], /Fixture organisation only/);
    assert.match(app.status(), /No confirmed event route/);
  });
  current = fixture(null, 'Fixture event only');
  app = setup(fetcher); await settle();
  ok('event-readiness-does-not-add-an-organisation-requirement', () => {
    assert.match(app.items()[0], /no confirmed entry/);
    assert.match(app.status(), /^A confirmed event route/);
  });
  current = fixture('Fixture organisation A', 'Fixture event A');
  app = setup(fetcher); await settle();
  ok('both-current-source-rows-render', () => {
    assert.match(app.items()[0], /Fixture organisation A/);
    assert.match(app.items()[1], /Fixture event A/);
  });
  current = fixture('Fixture organisation B', 'Fixture event B');
  app = setup(fetcher); await settle();
  ok('source-changes-without-a-deck-rewrite', () => {
    assert.match(app.items()[0], /Fixture organisation B/);
    assert.match(app.items()[1], /Fixture event B/);
  });
  await app.upload(JSON.stringify(fixture('<b>Local fixture</b>', 'Local event')));
  ok('offline-file-overrides-and-renders-names-as-text', () => {
    assert.match(app.items()[0], /<b>Local fixture<\/b>/);
    assert.equal(app.nodes['award-slot-rows'].children[0].children.length, 0);
  });
  await app.upload('{bad');
  ok('invalid-file-clears-stale-confirmed-rows', () => {
    assert.equal(app.items().length,0);
    assert.match(app.status(), /Unconfirmed.*selected file could not be read/);
  });
  app = setup(async()=>{ throw new Error('offline fixture'); }); await settle();
  ok('network-failure-remains-preparation', () => {
    assert.equal(app.items().length,0);
    assert.match(app.status(), /Unconfirmed.*offline/);
  });
  app = setup(()=>{ throw new Error('file mode must not fetch'); },'file:'); await settle();
  ok('file-protocol-does-not-fetch', () => assert.match(app.status(), /Unconfirmed.*Load the shared slots file/));
  await app.upload(JSON.stringify(fixture('Local-only organisation','Local-only event')));
  ok('file-protocol-has-a-working-local-picker', () => assert.match(app.items()[0], /Local-only organisation/));
  let release;
  const late = new Promise(resolve=>release=resolve);
  app = setup(async()=>late);
  await app.upload(JSON.stringify(fixture('Local wins','Local event wins')));
  release({ok:true,json:async()=>fixture('Late remote','Late event')}); await settle();
  ok('late-hosted-response-does-not-overwrite-a-selected-file', () => assert.match(app.items()[0], /Local wins/));
  const report = {scope:'Node VM integration using exact embedded source and adapter; this is not a Chromium rendering result', controls:rows, passed:rows.length};
  if (process.argv[2]) fs.writeFileSync(process.argv[2],JSON.stringify(report,null,1)+'\n');
  process.stdout.write(JSON.stringify(report,null,1)+'\n');
})().catch(error=>{ console.error(error);process.exit(1); });
