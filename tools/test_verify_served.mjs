/* Regression controls for the actual served-byte predicates and time bounds. */
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { Inconclusive, get, mapLimit, responseVerdict, verdictFor, publicationSubjects } from './verify_served.mjs';

let passed = 0;
async function check(label, action) { await action(); passed++; console.log('CONTROL PASS: ' + label); }
const subject = { url: 'https://madebymatt-play.uk/apexkick/', type: 'text/html' };
const body = Buffer.from('<html>Approved publication</html>');
const hash = crypto.createHash('sha256').update(body).digest('hex');
const response = { status: 200, final: subject.url, type: 'text/html; charset=utf-8', body };
const hosts = ['madebymatt-play.uk', 'www.madebymatt-play.uk'];
const result = value => responseVerdict(value, hash, subject, hosts).verdict;
await check('matching bytes and declared HTTPS resource pass', () => assert.equal(result(response), 'SERVED'));
await check('one appended byte fails with HTTP 200', () => assert.equal(result({ ...response, body: Buffer.concat([body, Buffer.from([0])]) }), 'MISMATCH'));
await check('HTTP error never passes matching bytes', () => assert.equal(result({ ...response, status: 404 }), 'RED'));
await check('wrong content type never passes matching bytes', () => assert.equal(result({ ...response, type: 'text/plain' }), 'RED'));
await check('only the exact www resource redirect is allowed', () => {
  assert.equal(result({ ...response, final: 'https://www.madebymatt-play.uk/apexkick/' }), 'SERVED');
  for (const final of ['https://www.madebymatt-play.uk/', 'https://madebymatt-play.uk/apexkick/?elsewhere=1',
    'http://www.madebymatt-play.uk/apexkick/', 'https://mirror.invalid/apexkick/', 'https://user@madebymatt-play.uk/apexkick/',
    'https://madebymatt-play.uk/apexkick/#wrong-target'])
    assert.equal(result({ ...response, final }), 'RED', final);
});
await check('empty and incomplete populations fail closed', () => {
  assert.throws(() => verdictFor([], 0), Inconclusive);
  assert.throws(() => verdictFor([1, 2], 1), Inconclusive);
  assert.equal(verdictFor([1, 2], 2), true);
});
await check('parallel work keeps its bound, order, and complete membership', async () => {
  let active = 0, peak = 0;
  const rows = await mapLimit([0, 1, 2, 3, 4, 5, 6], 3, async i => {
    peak = Math.max(peak, ++active);
    await new Promise(resolve => setTimeout(resolve, 4 + (6-i)));
    active--;
    return i * 2;
  });
  assert.equal(peak, 3);
  assert.deepEqual(rows, [0, 2, 4, 6, 8, 10, 12]);
});
await check('stuck fetch obeys its request bound and expired overall budget rejects', async () => {
  const saved = globalThis.fetch;
  const keepAlive = setInterval(() => {}, 100);
  try {
    globalThis.fetch = (_url, { signal }) => new Promise((_resolve, reject) => signal.addEventListener('abort', () => reject(signal.reason), { once: true }));
    const start = Date.now();
    await assert.rejects(() => get(subject.url, 25, Date.now() + 1000));
    assert(Date.now() - start < 500, 'request timeout did not end the blocked fetch');
    await assert.rejects(() => get(subject.url, 1000, Date.now() - 1), Inconclusive);
  } finally { globalThis.fetch = saved; clearInterval(keepAlive); }
});
await check('a redirect loop is bounded', async () => {
  const saved = globalThis.fetch;
  let calls = 0;
  try {
    globalThis.fetch = async () => { calls++; return { status: 302, headers: new Headers({ location: subject.url }) }; };
    assert.equal((await get(subject.url)).status, 508);
    assert.equal(calls, 5);
  } finally { globalThis.fetch = saved; }
});

const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'served-publication-test-'));
try {
  const roots = {}, publications = {};
  for (const kind of ['site', 'lessons', 'apps', 'games']) {
    roots[kind] = path.join(temp, 'source-' + kind);
    const root = path.join(temp, 'published-' + kind);
    fs.mkdirSync(roots[kind]); fs.mkdirSync(root);
    fs.writeFileSync(path.join(roots[kind], 'identity.txt'), kind);
    execFileSync('git', ['init', '-q', roots[kind]]);
    execFileSync('git', ['-C', roots[kind], 'add', '.']);
    execFileSync('git', ['-C', roots[kind], '-c', 'user.name=Serve Control', '-c', 'user.email=serve-control@example.invalid', 'commit', '-qm', 'fixture']);
    const revision = execFileSync('git', ['-C', roots[kind], 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
    publications[kind] = { root, source_sha: revision, publication_sha: revision, run_id: 123,
      artifact_id: 456, artifact_sha256: 'sha256:' + 'a'.repeat(64), deployment: 'success' };
  }
  fs.writeFileSync(path.join(roots.games, 'play-publication.json'), JSON.stringify({ domain: 'madebymatt-play.uk' }));
  fs.writeFileSync(path.join(roots.games, 'games.json'), JSON.stringify({ games: [{ href: '/apexkick/' }] }));
  fs.mkdirSync(path.join(publications.games.root, 'apexkick'));
  fs.writeFileSync(path.join(publications.games.root, 'apexkick/index.html'), body);
  const record = path.join(temp, 'publications.json');
  const proof = { version: 1, publications, games_origin: 'https://madebymatt-play.uk', canonical_game_routes: ['/apexkick'] };
  const population = { list: [{ group: 'site', name: '/apexkick/', url: 'https://madebymatt.uk/apexkick/',
    blob: path.join(roots.site, 'apexkick/index.html'), type: 'text/html' }], residue: [], missing: [] };
  const write = value => fs.writeFileSync(record, JSON.stringify(value));
  await check('original game is retained and compared to the successful games publication', () => {
    write(proof);
    const remapped = publicationSubjects(population, record, roots).list;
    assert.equal(remapped.length, 1);
    assert.equal(remapped[0].url, subject.url);
    assert.deepEqual(fs.readFileSync(remapped[0].blob), body);
  });
  await check('stale or undeployed source evidence never becomes expected bytes', () => {
    for (const mutation of [{ source_sha: '0'.repeat(40) }, { deployment: 'skipped' }, { artifact_sha256: '' }, { run_id: null }]) {
      const bad = structuredClone(proof); Object.assign(bad.publications.lessons, mutation); write(bad);
      assert.throws(() => publicationSubjects(population, record, roots), Inconclusive);
    }
  });
  await check('same-count substituted canonical membership is rejected', () => {
    write({ ...proof, canonical_game_routes: ['/replacement'] });
    assert.throws(() => publicationSubjects(population, record, roots), Inconclusive);
  });
  await check('missing publication route is inconclusive, never dropped', () => {
    write(proof);
    fs.unlinkSync(path.join(publications.games.root, 'apexkick/index.html'));
    assert.throws(() => publicationSubjects(population, record, roots), Inconclusive);
  });
} finally { fs.rmSync(temp, { recursive: true, force: true }); }
console.log(`PASS: ${passed} served-proof regression controls`);
