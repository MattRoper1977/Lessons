/* Regression controls for the actual served-byte predicates and time bounds. */
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
// Only this isolated harness skips the wait between retries; production bounds
// and the number of attempts are unchanged. The actual assess() path still runs.
const savedRetryInterval = process.env.SERVE_RETRY_MS;
process.env.SERVE_RETRY_MS = '0';
let verifier;
try { verifier = await import('./verify_served.mjs'); }
finally {
  if (savedRetryInterval === undefined) delete process.env.SERVE_RETRY_MS;
  else process.env.SERVE_RETRY_MS = savedRetryInterval;
}
const { Inconclusive, get, mapLimit, responseVerdict, verdictFor, publicationSubjects,
  launchSubjects, subjects, assess } = verifier;

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

  const lessonRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
  const launchManifest = 'Science_Teesside/Launch/manifest.json';
  const declaredLaunch = JSON.parse(fs.readFileSync(path.join(lessonRoot, launchManifest), 'utf8')).lessons;
  let selectedLaunch;
  await check('S1-M every real LAUNCH manifest member is in the composed serve set', () => {
    const actual = subjects().list.filter(entry => entry.source_manifest === launchManifest);
    const expected = declaredLaunch.map(entry => `Science_Teesside/Launch/${entry.file}`);
    assert(expected.length > 0);
    assert.equal(actual.length, expected.length);
    assert.deepEqual(new Set(actual.map(entry => entry.name)), new Set(expected));
    for (const entry of actual) {
      assert.equal(entry.group, 'lessons');
      assert(fs.existsSync(entry.blob), entry.blob);
    }
    selectedLaunch = actual[0];
    console.log(`S1-M actual manifest membership: ${actual.length} routes; selected ${selectedLaunch.url}`);
  });
  const declarationRoot = path.join(temp, 'launch-declaration');
  const declarationFile = path.join(declarationRoot, launchManifest);
  fs.mkdirSync(path.dirname(declarationFile), { recursive: true });
  await check('S1-M the next declared lesson is included and its URL is component-encoded', () => {
    const extra = { file: 'future lesson & (class)/new lesson.html' };
    fs.writeFileSync(declarationFile, JSON.stringify({ lessons: [...declaredLaunch, extra] }));
    const derived = launchSubjects(declarationRoot, 'https://madebymatt.uk/Lessons');
    assert.equal(derived.length, declaredLaunch.length + 1);
    assert.equal(derived.at(-1).url, 'https://madebymatt.uk/Lessons/Science_Teesside/Launch/future%20lesson%20%26%20(class)/new%20lesson.html');
  });
  await check('S1-M empty, malformed, duplicate and escaping LAUNCH declarations fail closed', () => {
    const invalid = [null, {}, { lessons: [] }, { lessons: [null] },
      { lessons: [{ file: '../escape.html' }] }, { lessons: [{ file: '/escape.html' }] },
      { lessons: [{ file: 'bad\\path.html' }] }, { lessons: [{ file: 'nested//empty.html' }] },
      { lessons: [{ file: './relative.html' }] }, { lessons: [{ file: 'image.svg' }] },
      { lessons: [declaredLaunch[0], declaredLaunch[0]] }];
    for (const value of invalid) {
      fs.writeFileSync(declarationFile, JSON.stringify(value));
      assert.throws(() => launchSubjects(declarationRoot), Inconclusive);
    }
    fs.writeFileSync(declarationFile, '{broken JSON');
    assert.throws(() => launchSubjects(declarationRoot), Inconclusive);
    fs.unlinkSync(declarationFile);
    assert.throws(() => launchSubjects(declarationRoot), Inconclusive);
  });
  await check('S1-M one newly covered LAUNCH route uses published bytes and reds on a served-byte mismatch', async () => {
    const relative = path.relative(lessonRoot, selectedLaunch.blob);
    const sourceFile = path.join(roots.lessons, relative);
    const publishedFile = path.join(publications.lessons.root, relative);
    const sourceBytes = fs.readFileSync(selectedLaunch.blob);
    const publishedBytes = Buffer.concat([sourceBytes, Buffer.from('\n<!-- S1-M published-tree control fixture -->\n')]);
    fs.mkdirSync(path.dirname(sourceFile), { recursive: true });
    fs.mkdirSync(path.dirname(publishedFile), { recursive: true });
    fs.writeFileSync(sourceFile, sourceBytes);
    fs.writeFileSync(publishedFile, publishedBytes);
    execFileSync('git', ['-C', roots.lessons, 'add', '.']);
    execFileSync('git', ['-C', roots.lessons, '-c', 'user.name=Serve Control', '-c', 'user.email=serve-control@example.invalid', 'commit', '-qm', 'actual LAUNCH subject fixture']);
    const revision = execFileSync('git', ['-C', roots.lessons, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
    publications.lessons.source_sha = revision;
    publications.lessons.publication_sha = revision;
    write(proof);
    const launchPopulation = { list: [{ ...selectedLaunch, blob: sourceFile }], residue: [], missing: [] };
    const remapped = publicationSubjects(launchPopulation, record, roots).list[0];
    assert.equal(remapped.blob, publishedFile);
    assert.equal(remapped.url, selectedLaunch.url);
    assert.equal(remapped.source_group, 'lessons');
    assert.equal(remapped.publication_run, publications.lessons.run_id);
    const savedFetch = globalThis.fetch;
    let servedBytes = publishedBytes;
    let calls = 0;
    globalThis.fetch = async url => {
      assert.equal(url, selectedLaunch.url);
      calls++;
      return new Response(servedBytes, { status: 200, headers: { 'content-type': 'text/html' } });
    };
    try {
      const permitted = [new URL(selectedLaunch.url).host];
      const run = () => assess(remapped, permitted, new Set(), {});
      assert.equal((await run()).verdict, 'SERVED');
      servedBytes = Buffer.concat([publishedBytes, Buffer.from([0])]);
      const mismatch = await run();
      assert.equal(mismatch.verdict, 'RED');
      assert.match(mismatch.detail, /HTTP 200: expected .* vs served/);
      servedBytes = publishedBytes;
      assert.equal((await run()).verdict, 'SERVED');
      console.log(`S1-M newly covered ${selectedLaunch.url}: SERVED -> RED -> SERVED; HTTP 200 throughout; ${calls} fixture responses; ${mismatch.detail}`);
    } finally { globalThis.fetch = savedFetch; }
  });
} finally { fs.rmSync(temp, { recursive: true, force: true }); }
console.log(`PASS: ${passed} served-proof regression controls`);
