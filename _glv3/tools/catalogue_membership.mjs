import assert from 'node:assert/strict';
import { pathToFileURL } from 'node:url';

// The hub loads resources plus lesson-order supplements absent from resources.
// These gates cover exact record subjects, with no format/year/saved filters.
export function expectedSubjectRows(resources, order, subject) {
  assert(resources.some(r => !r._shelfPathway && r.subject === subject), `unknown record subject: ${subject}`);
  const known = new Set(resources.map(r => r.file || r.url));
  const rows = [...resources, ...(order.supplements || []).filter(r => !known.has(r.file))]
    .filter(r => r.subject === subject);
  const paths = rows.map(r => r.file || r.url);
  assert(paths.every(p => typeof p === 'string' && p.length), `${subject}: empty resource path`);
  assert.equal(new Set(paths).size, paths.length, `${subject}: duplicate expected resource path`);
  return rows;
}

export function verifySubjectCards({ subject, expected, advertised, cards, base }) {
  assert.equal(advertised, expected.length, `${subject}: advertised count`);
  assert.equal(cards.length, expected.length, `${subject}: rendered count`);
  const wanted = new Map(expected.map(r => [r.file || r.url, r]));
  assert.equal(wanted.size, expected.length, `${subject}: duplicate expected path`);
  const seen = new Set();
  for (const card of cards) {
    assert(wanted.has(card.path), `${subject}: unexpected card path: ${card.path}`);
    assert(!seen.has(card.path), `${subject}: duplicate rendered path: ${card.path}`);
    seen.add(card.path);
    assert(card.href, `${subject}: missing link: ${card.path}`);
    const expectedURL = new URL(encodeURI(card.path), base.replace(/\/$/, '') + '/').href;
    const actualURL = new URL(card.href, base.replace(/\/$/, '') + '/').href;
    assert.equal(actualURL, expectedURL, `${subject}: incorrect link: ${card.path}`);
  }
  assert.equal(seen.size, wanted.size, `${subject}: missing resource paths`);
}

export function catalogueMembershipControls() {
  const subject = 'Fixture';
  const resources = [{subject, file:'base lesson.html'}, {subject:'Other', file:'other.html'}];
  const order = {supplements:[{subject, file:'base lesson.html'}, {subject, file:'extra.html#task'}]};
  const expected = expectedSubjectRows(resources, order, subject);
  assert.deepEqual(expected.map(r => r.file), ['base lesson.html', 'extra.html#task']);
  const fixture = {subject, expected, advertised:2, base:'http://127.0.0.1:8123', cards:expected.map(r => ({path:r.file, href:encodeURI(r.file)}))};
  verifySubjectCards(fixture);
  let rejected = 0;
  for (const plant of [
    f => { f.advertised = 1; },
    f => { f.cards.pop(); },
    f => { f.cards.push(f.cards[0]); },
    f => { f.cards[1] = {...f.cards[0]}; },
    f => { f.cards[1].path = 'unexpected.html'; },
    f => { f.cards[1].href = 'wrong.html'; },
    f => { f.cards[1].href = ''; },
    f => { f.cards[1].href = 'https://elsewhere.invalid/extra.html#task'; },
    f => { f.cards[1].href = 'extra.html#wrong'; },
    f => { f.cards[1].href = 'extra.html?wrong=1#task'; },
  ]) {
    const f = structuredClone(fixture); plant(f);
    assert.throws(() => verifySubjectCards(f)); rejected++;
  }
  assert.throws(() => expectedSubjectRows(resources, {supplements:[...order.supplements, order.supplements[1]]}, subject));
  assert.throws(() => expectedSubjectRows(resources, order, 'Unknown'));
  return {positive:'resource plus supplemental union, deduplication and exact links', negative_controls:rejected + 2, passed:true};
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  console.log(JSON.stringify(catalogueMembershipControls(), null, 2));
}
