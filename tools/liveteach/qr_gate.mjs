/* The Q1 gate: a QR that has not been machine-decoded does not ship.

   Encodes representative share-URLs at EVERY allowed version (1–6), rasterizes
   the matrix, and decodes it with the vendored jsQR — an independent decoder
   that shares nothing with the encoder. Exact string match required.

     node tools/liveteach/qr_gate.mjs             gate the encoder
     node tools/liveteach/qr_gate.mjs --self-test prove the gate can fail

   The self-test's red vectors are the point: (a) a corrupted matrix must not
   decode to the payload, and (b) the ORIGINAL FRAGMENT'S BUG — one RS block,
   no interleaving, at a multi-block version — is rebuilt here and shown to be
   undecodable, proving this gate would have caught the defect Q1 documents. */
import { createRequire } from 'node:module';
import path from 'node:path';
const require = createRequire(import.meta.url);
const HERE = path.dirname(new URL(import.meta.url).pathname);
const LTQR = require(path.join(HERE, 'qr_source.js'));
const jsQR = require(path.join(HERE, 'vendor', 'jsQR.js'));

const SCALE = 8, QUIET = 4;
function rasterize(code) {
  const dim = (code.size + QUIET * 2) * SCALE;
  const data = new Uint8ClampedArray(dim * dim * 4).fill(255);
  for (let y = 0; y < code.size; y++) {
    for (let x = 0; x < code.size; x++) {
      if (code.modules[y * code.size + x] !== 1) continue;
      for (let dy = 0; dy < SCALE; dy++) {
        for (let dx = 0; dx < SCALE; dx++) {
          const px = ((y + QUIET) * SCALE + dy) * dim + (x + QUIET) * SCALE + dx;
          data[px * 4] = 0; data[px * 4 + 1] = 0; data[px * 4 + 2] = 0;
        }
      }
    }
  }
  return { data, dim };
}

function decode(code) {
  const { data, dim } = rasterize(code);
  const hit = jsQR(data, dim, dim);
  return hit ? hit.data : null;
}

// Realistic share URLs sized to force each version (byte-mode ECC-M capacities:
// 14 / 26 / 42 / 62 / 84 / 106).
const BASE = 'https://madebymatt.uk/Lessons/liveteach/projector.html';
const PAYLOADS = [
  { want: 1, text: 'liveteach v1' },                                     // 12B
  { want: 2, text: 'madebymatt.uk/liveteach' },                          // 23B
  { want: 3, text: 'madebymatt.uk/Lessons/liveteach/?stage=4' },         // 40B
  { want: 4, text: BASE.slice(0, 54) + '?s=2' },                         // 58B
  { want: 5, text: BASE + '?lesson=waves_v1&stage=3' },                  // 78B
  { want: 6, text: BASE + '?lesson=waves_v1&stage=3&speed=2&hl=1&tag=y10' }, // 97B
];

const MODE = process.argv[2] || '';
let bad = 0;
const say = (ok, label, detail) => {
  console.log((ok ? 'PASS' : 'FAILED') + '  ' + label + (ok || !detail ? '' : ' — ' + detail));
  if (!ok) bad++;
};

if (MODE === '--self-test') {
  // (a) heavy corruption must not decode back to the payload
  const c = LTQR.encode(PAYLOADS[3].text);
  for (let i = 0; i < c.modules.length; i += 3) c.modules[i] ^= 1;
  const corrupt = decode(c);
  say(corrupt !== PAYLOADS[3].text, 'RED: a corrupted matrix does not decode to the payload', String(corrupt));
  // (b) the fragment's own defect — single block, no interleave, at v4 —
  // must be undecodable, so this gate would have caught it.
  const text = PAYLOADS[3].text;
  const good = LTQR.encode(text);
  say(good.version === 4, 'setup: the probe payload really is version 4', 'got v' + good.version);
  // rebuild v4 the WRONG way: treat data as ONE RS block (the fragment's bug)
  const brokenModules = buildSingleBlockV4(text);
  const broken = { version: 4, size: 33, modules: brokenModules };
  const brokenOut = decode(broken);
  say(brokenOut !== text, 'RED: the fragment\'s single-block v4 (the Q1 defect) fails the decode gate', String(brokenOut));
  console.log(bad ? '[SELF-TEST] FAIL' : '[SELF-TEST] PASS');
  process.exit(bad ? 1 : 0);
} else {
  const masksSeen = new Set();
  for (const p of PAYLOADS) {
    let code;
    try { code = LTQR.encode(p.text); }
    catch (e) { say(false, 'v' + p.want + ' encodes', e.message); continue; }
    masksSeen.add(code.mask);
    say(code.version === p.want, 'v' + p.want + ': payload lands on the intended version', 'got v' + code.version);
    const out = decode(code);
    say(out === p.text, 'v' + p.want + ' (mask ' + code.mask + '): jsQR round-trips the exact string', JSON.stringify({ want: p.text.slice(0, 30), got: out && out.slice(0, 30) }));
  }
  /* The registry asks explicitly for mask verification, not assumption: prove
     that output at EVERY mask decodes, not just at whichever mask the penalty
     rules happened to pick above (mask 0 included — the fragment emitted
     mask-0-only output, which is spec-non-compliant but usually scannable;
     "usually" is not evidence). Two versions, one single-block and one
     interleaved, × all 8 masks. */
  for (const p of [PAYLOADS[1], PAYLOADS[5]]) {
    for (let m = 0; m < 8; m++) {
      const forced = LTQR.encodeWithMask(p.text, m);
      const out = decode(forced);
      say(forced.mask === m && out === p.text, 'v' + p.want + ' forced to mask ' + m + ': jsQR still round-trips the exact string', JSON.stringify({ mask: forced.mask, got: out && out.slice(0, 24) }));
    }
  }
  /* And the chooser must actually be choosing: the mask it picks has to be
     the lowest-penalty one, or the penalty rules are decorative. */
  for (const p of [PAYLOADS[2], PAYLOADS[5]]) {
    const chosen = LTQR.encode(p.text);
    let bestM = 0, bestS = Infinity;
    for (let m = 0; m < 8; m++) {
      const s = LTQR.encodeWithMask(p.text, m).penalty;
      if (s < bestS) { bestS = s; bestM = m; }
    }
    say(chosen.mask === bestM && chosen.penalty === bestS, 'v' + p.want + ': the shipped mask is the lowest-penalty one (the rules are live, not decorative)', JSON.stringify({ chose: chosen.mask, best: bestM }));
  }

  // over-capacity is an honest error, never a silent truncation
  let threw = false;
  try { LTQR.encode('x'.repeat(107)); } catch (e) { threw = /shorten/.test(e.message); }
  say(threw, 'over-capacity payloads throw the honest shorten-the-URL error');
  /* Capacity boundaries: the last byte that fits a version must stay on it,
     and one more must step up — an off-by-one here ships codes that overflow
     their block table. */
  const CAP = { 1: 14, 2: 26, 3: 42, 4: 62, 5: 84, 6: 106 };
  for (const v of [1, 2, 3, 4, 5]) {
    const atCap = LTQR.encode('x'.repeat(CAP[v]));
    const overCap = LTQR.encode('x'.repeat(CAP[v] + 1));
    say(atCap.version === v && overCap.version === v + 1, 'capacity boundary at v' + v + ': ' + CAP[v] + 'B fits, ' + (CAP[v] + 1) + 'B steps up', JSON.stringify({ at: atCap.version, over: overCap.version }));
    const back = decode(atCap);
    say(back === 'x'.repeat(CAP[v]), 'v' + v + ' at exactly full capacity still decodes');
  }
  console.log('masks exercised across payloads: ' + [...masksSeen].sort().join(','));
  console.log(bad ? 'QR GATE FAILED (' + bad + ')' : 'QR GATE PASSED');
  process.exit(bad ? 1 : 0);
}

/* Rebuild version 4 with the fragment's bug: all 64 data codewords fed to ONE
   RS(…,36-ish) computation and appended, no per-block split, no interleave.
   Everything else (masking, format, placement) uses the correct pipeline so
   the ONLY defect is the block structure — isolating what Q1 describes. */
function buildSingleBlockV4(text) {
  const src = require('node:fs').readFileSync(path.join(HERE, 'qr_source.js'), 'utf8');
  // re-evaluate the module with its interleaver swapped for a passthrough
  const patched = src.replace(
    /var out = \[\];\s*\n\s*for \(var di = 0[\s\S]*?return out;/,
    'var out = [];\n' +
    '    var one = data.slice();\n' +
    '    var oneEc = rsEncode(one, info.ec * info.blocks);\n' +
    '    out = one.concat(Array.from(oneEc));\n' +
    '    return out;'
  );
  if (patched === src) throw new Error('self-test patch failed to apply');
  const mod = { exports: {} };
  new Function('module', 'exports', 'self', patched)(mod, mod.exports, undefined);
  return mod.exports.encode(text).modules;
}
