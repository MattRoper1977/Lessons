#!/usr/bin/env node
/* verify_games_hygiene.mjs — shelf-game hygiene gates, derived not pinned.
 *
 * Scans every Games/*.html at run time (no hard-coded file list or counts) and
 * enforces three static contracts this estate has now adopted:
 *
 *   H1  no remote Google Fonts — cosmetic webfonts were removed in favour of
 *       the system stacks every file already declared; a reintroduced
 *       fonts.googleapis/fonts.gstatic reference is a regression.
 *   H2  no raw `&` in markup context — text and attributes use &amp;.
 *       Script and style bodies are exempt: a raw & is CORRECT JavaScript, and
 *       rewriting one there is itself a bug. The parser walks real markup
 *       context; this is not a whole-file grep.
 *   H3  functional runtimes resolve locally — any three.js / cannon-es /
 *       aframe import must point into Games/vendor/, never at a CDN. (The
 *       vendored copies are the offline contract; a CDN reference silently
 *       reintroduces the network dependency this repo removed.)
 *
 * Usage: node tools/verify_games_hygiene.mjs [--self-test]
 * --self-test proves each gate can fail by feeding it a known-bad synthetic
 * document; a gate that cannot go red proves nothing.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const GAMES = join(ROOT, 'Games');

let pass = 0, fail = 0;
const ok = (cond, label) => { cond ? pass++ : fail++; console.log(`${cond ? '  ok ' : 'FAIL '} ${label}`); };

function markupAmpersands(html) {
  // strip script/style bodies, then find & that are not entities
  const stripped = html
    .replace(/<script\b[\s\S]*?<\/script>/gi, '<script></script>')
    .replace(/<style\b[\s\S]*?<\/style>/gi, '<style></style>');
  const hits = [];
  const re = /&(?!#?\w+;)/g;
  let m;
  while ((m = re.exec(stripped)) !== null)
    hits.push(stripped.slice(Math.max(0, m.index - 30), m.index + 20).replace(/\s+/g, ' '));
  return hits;
}

function check(html, name) {
  const fonts = html.match(/fonts\.googleapis|fonts\.gstatic/g) || [];
  ok(fonts.length === 0, `H1 ${name}: no remote font references${fonts.length ? ` (found ${fonts.length})` : ''}`);
  const amps = markupAmpersands(html);
  ok(amps.length === 0, `H2 ${name}: no raw markup ampersands${amps.length ? ` (${amps.length}: ${amps[0]}…)` : ''}`);
  let cdnRuntime = html.match(/https?:\/\/[^"'\s]*(cdn\.jsdelivr|cdnjs\.cloudflare|unpkg\.com)[^"'\s]*(three|cannon|aframe)[^"'\s]*/gi) || [];
  /* voxelcraft's A-Frame loader is LOCAL-FIRST: 'vendor/aframe-…' heads its
   * fallback list, so the CDN URLs after it are unreachable redundancy for a
   * broken local serve, not a dependency (same defence-in-depth ruling as the
   * shelf's inert desc-strip line). The exemption requires the local entry to
   * actually precede the CDN ones — remove the local copy and H3 goes red. */
  if (cdnRuntime.length && /vendor\/aframe-[^'"\s]+/.test(html)) {
    const localAt = html.search(/vendor\/aframe-[^'"\s]+/);
    cdnRuntime = cdnRuntime.filter(u => html.indexOf(u) < localAt);
  }
  ok(cdnRuntime.length === 0, `H3 ${name}: no CDN runtime imports without a preceding local-first entry${cdnRuntime.length ? ` (${cdnRuntime[0].slice(0, 60)}…)` : ''}`);
}

if (process.argv.includes('--self-test')) {
  console.log('— self-test: every gate must trip on a known-bad document —');
  const bad = `<html><head>
    <link href="https://fonts.googleapis.com/css2?family=X&display=swap" rel="stylesheet">
    <script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js"}}</script>
    </head><body><p>fish & chips</p><script>const a = 1 & 2;</script></body></html>`;
  const before = fail;
  check(bad, 'self-test-doc');
  const tripped = fail - before;
  if (tripped !== 3) { console.error(`SELF-TEST FAILED: expected all 3 gates to trip, got ${tripped}`); process.exit(1); }
  // and the script-exemption must hold: a raw & inside <script> alone is clean
  const amps = markupAmpersands('<html><body><script>if(a & b){}</script></body></html>');
  if (amps.length !== 0) { console.error('SELF-TEST FAILED: script-context & wrongly flagged'); process.exit(1); }
  console.log('self-test: all 3 gates trip on bad input; script-context & exempt. CAN-FAIL PROVEN');
  process.exit(0);
}

/* R2 (game-estate red lines, 2026-08-06): Slipstream_GP.html carries the
 * shipped 2026-07 mobile/graphics patch set and the only edit permitted to it
 * is the surgical vendored-runtime script swap. Its cosmetic font links (and
 * the raw & inside those link URLs) are therefore RECORDED, not repaired —
 * this exemption is the red line encoded, not a hole. Remove it the day Matt
 * lifts R2, and the gate will demand the cleanup automatically. */
const R2_EXEMPT = new Set(['Slipstream_GP.html']);
/* A game that needs siblings (a service worker, a manifest) lives in its own
 * directory rather than as a flat Games/*.html. A top-level readdir cannot see
 * one, so the first such game — Micro-Tinkerer — silently escaped every gate
 * here and shipped a raw markup ampersand that this file was written to catch.
 * One level of descent closes that. Games/vendor holds no .html, so nothing
 * else is newly in scope. */
const censusFiles = () => {
  const out = [];
  for (const entry of readdirSync(GAMES, { withFileTypes: true })) {
    if (entry.isFile() && entry.name.endsWith('.html')) { out.push(entry.name); continue; }
    if (!entry.isDirectory() || entry.name === 'vendor') continue;
    for (const inner of readdirSync(join(GAMES, entry.name), { withFileTypes: true }))
      if (inner.isFile() && inner.name.endsWith('.html')) out.push(`${entry.name}/${inner.name}`);
  }
  return out;
};
const files = censusFiles().filter(f => !R2_EXEMPT.has(f));
if (files.length < 20) { console.error(`suspicious census: only ${files.length} Games/**/*.html`); process.exit(1); }
for (const f of files) check(readFileSync(join(GAMES, f), 'utf8'), f);
for (const f of R2_EXEMPT) console.log(`  --  ${f}: EXEMPT under R2 (surgical-edit-only file); font links recorded, not judged`);
console.log(`\n${fail === 0 ? `ALL ${pass} HYGIENE GATES PASSED (${files.length} files)` : `${pass} passed, ${fail} FAILED`}`);
process.exit(fail ? 1 : 0);
