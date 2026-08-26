/* Live-Teach QR encoder — byte mode, ECC level M, versions 1–6 ONLY.
   ONE SOURCE, MANY COPIES: stamped into the views by stamp_qr.mjs (the
   pinned-region pattern) and require()d by the node gate.

   WHY THIS EXISTS AT ALL (spec Q1): the reviewed fragment's QR engine had a
   WRONG block structure for versions 4 and 6 — ECC-M v4/v6 need multiple
   interleaved Reed–Solomon blocks and it computed one, so codes above ~44
   bytes could not scan. This implementation carries the standard per-version
   block table WITH interleaving, evaluates all eight masks by the four
   penalty rules, and is allowed to ship only while tools/liveteach/qr_gate.mjs
   proves an INDEPENDENT decoder (vendored jsQR) round-trips every allowed
   version. A QR that has not been machine-decoded in CI does not ship.
   Payloads longer than version 6's 106 bytes throw an honest Error — the
   serializer's default-omission keeps share URLs short instead. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.LTQR = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /* Version geometry + ECC-M block structure (ISO/IEC 18004 table 9):
     [totalSize, ecPerBlock, blockCount, dataPerBlock] */
  var VER = {
    1: { size: 21, ec: 10, blocks: 1, dataPer: 16 },
    2: { size: 25, ec: 16, blocks: 1, dataPer: 28 },
    3: { size: 29, ec: 26, blocks: 1, dataPer: 44 },
    4: { size: 33, ec: 18, blocks: 2, dataPer: 32 },
    5: { size: 37, ec: 24, blocks: 2, dataPer: 43 },
    6: { size: 41, ec: 16, blocks: 4, dataPer: 27 }
  };

  /* --- GF(256), polynomial 0x11d --- */
  var EXP = new Uint8Array(512), LOG = new Uint8Array(256);
  (function () {
    var x = 1;
    for (var i = 0; i < 255; i++) {
      EXP[i] = x; LOG[x] = i;
      x <<= 1;
      if (x & 0x100) x ^= 0x11d;
    }
    for (var j = 255; j < 512; j++) EXP[j] = EXP[j - 255];
  })();
  function gmul(a, b) { return (a === 0 || b === 0) ? 0 : EXP[LOG[a] + LOG[b]]; }

  function rsGenerator(degree) {
    var g = [1];
    for (var d = 0; d < degree; d++) {
      var next = new Array(g.length + 1).fill(0);
      for (var i = 0; i < g.length; i++) {
        next[i] ^= gmul(g[i], EXP[d]);
        next[i + 1] ^= g[i];
      }
      g = next;
    }
    return g.reverse(); // highest-degree first
  }

  function rsEncode(data, ecLen) {
    var gen = rsGenerator(ecLen);
    var rem = new Uint8Array(ecLen);
    for (var i = 0; i < data.length; i++) {
      var factor = data[i] ^ rem[0];
      rem.copyWithin(0, 1);
      rem[ecLen - 1] = 0;
      if (factor !== 0) {
        for (var j = 0; j < ecLen; j++) rem[j] ^= gmul(gen[j + 1], factor);
      }
    }
    return rem;
  }

  function utf8Bytes(str) {
    var out = [];
    for (var i = 0; i < str.length; i++) {
      var c = str.codePointAt(i);
      if (c > 0xffff) i++;
      if (c < 0x80) out.push(c);
      else if (c < 0x800) out.push(0xc0 | (c >> 6), 0x80 | (c & 63));
      else if (c < 0x10000) out.push(0xe0 | (c >> 12), 0x80 | ((c >> 6) & 63), 0x80 | (c & 63));
      else out.push(0xf0 | (c >> 18), 0x80 | ((c >> 12) & 63), 0x80 | ((c >> 6) & 63), 0x80 | (c & 63));
    }
    return out;
  }

  function pickVersion(byteLen) {
    for (var v = 1; v <= 6; v++) {
      var cap = VER[v].blocks * VER[v].dataPer - 2; // mode nibble + 8-bit count + terminator fit in the 2 spare bytes
      if (byteLen <= cap) return v;
    }
    throw new Error('LTQR: payload of ' + byteLen + ' bytes exceeds version 6 (106) — shorten the URL');
  }

  function buildCodewords(bytes, v) {
    var info = VER[v];
    var totalData = info.blocks * info.dataPer;
    // bit stream: mode 0100, count (8 bits for v1-9 byte mode), data, terminator
    var bits = [];
    function push(val, n) { for (var i = n - 1; i >= 0; i--) bits.push((val >> i) & 1); }
    push(4, 4);
    push(bytes.length, 8);
    for (var i = 0; i < bytes.length; i++) push(bytes[i], 8);
    var capBits = totalData * 8;
    push(0, Math.min(4, capBits - bits.length)); // terminator
    while (bits.length % 8 !== 0) bits.push(0);
    var data = [];
    for (var b = 0; b < bits.length; b += 8) {
      var byte = 0;
      for (var k = 0; k < 8; k++) byte = (byte << 1) | bits[b + k];
      data.push(byte);
    }
    var pads = [0xec, 0x11], p = 0;
    while (data.length < totalData) data.push(pads[p++ % 2]);

    /* Split into the version's RS blocks, then INTERLEAVE — the exact step
       the broken fragment skipped. */
    var blocks = [], ecs = [];
    for (var bi = 0; bi < info.blocks; bi++) {
      var chunk = data.slice(bi * info.dataPer, (bi + 1) * info.dataPer);
      blocks.push(chunk);
      ecs.push(rsEncode(chunk, info.ec));
    }
    var out = [];
    for (var di = 0; di < info.dataPer; di++) {
      for (var bj = 0; bj < info.blocks; bj++) out.push(blocks[bj][di]);
    }
    for (var ei = 0; ei < info.ec; ei++) {
      for (var bk = 0; bk < info.blocks; bk++) out.push(ecs[bk][ei]);
    }
    return out;
  }

  /* --- matrix construction --- */
  function newMatrix(size) {
    return { size: size, m: new Int8Array(size * size).fill(-1) }; // -1 unset, 0 light, 1 dark
  }
  function set(mx, x, y, v) { mx.m[y * mx.size + x] = v; }
  function get(mx, x, y) { return mx.m[y * mx.size + x]; }

  function placeFinder(mx, x0, y0) {
    for (var y = -1; y <= 7; y++) {
      for (var x = -1; x <= 7; x++) {
        var xx = x0 + x, yy = y0 + y;
        if (xx < 0 || yy < 0 || xx >= mx.size || yy >= mx.size) continue;
        var dark = (x >= 0 && x <= 6 && (y === 0 || y === 6)) ||
          (y >= 0 && y <= 6 && (x === 0 || x === 6)) ||
          (x >= 2 && x <= 4 && y >= 2 && y <= 4);
        set(mx, xx, yy, dark ? 1 : 0);
      }
    }
  }

  function placeFixed(mx, v) {
    var size = mx.size;
    placeFinder(mx, 0, 0);
    placeFinder(mx, size - 7, 0);
    placeFinder(mx, 0, size - 7);
    // timing
    for (var i = 8; i < size - 8; i++) {
      if (get(mx, i, 6) === -1) set(mx, i, 6, i % 2 === 0 ? 1 : 0);
      if (get(mx, 6, i) === -1) set(mx, 6, i, i % 2 === 0 ? 1 : 0);
    }
    // one alignment pattern for v2-6 at (size-7, size-7)
    if (v >= 2) {
      var cx = size - 7, cy = size - 7;
      for (var ay = -2; ay <= 2; ay++) {
        for (var ax = -2; ax <= 2; ax++) {
          var dark = Math.max(Math.abs(ax), Math.abs(ay)) !== 1;
          set(mx, cx + ax, cy + ay, dark ? 1 : 0);
        }
      }
    }
    // format info areas reserved (filled later); dark module
    for (var f = 0; f <= 8; f++) {
      if (get(mx, f, 8) === -1) set(mx, f, 8, 0);
      if (get(mx, 8, f) === -1) set(mx, 8, f, 0);
      if (f < 8 && get(mx, size - 1 - f, 8) === -1) set(mx, size - 1 - f, 8, 0);
      if (f < 7 && get(mx, 8, size - 1 - f) === -1) set(mx, 8, size - 1 - f, 0);
    }
    set(mx, 8, size - 8, 1); // the always-dark module
  }

  function functionMask(v) {
    // a matrix marking which modules are functional (true) vs data (false)
    var size = VER[v].size;
    var mx = newMatrix(size);
    placeFixed(mx, v);
    var fn = new Uint8Array(size * size);
    for (var i = 0; i < size * size; i++) fn[i] = mx.m[i] === -1 ? 0 : 1;
    return fn;
  }

  function placeData(mx, fn, codewords) {
    var size = mx.size;
    var bitIdx = 0;
    var total = codewords.length * 8;
    var upward = true;
    for (var col = size - 1; col > 0; col -= 2) {
      if (col === 6) col--; // skip the timing column
      for (var i = 0; i < size; i++) {
        var y = upward ? size - 1 - i : i;
        for (var c = 0; c < 2; c++) {
          var x = col - c;
          if (fn[y * size + x]) continue;
          var bit = 0;
          if (bitIdx < total) {
            bit = (codewords[bitIdx >> 3] >> (7 - (bitIdx & 7))) & 1;
          }
          set(mx, x, y, bit);
          bitIdx++;
        }
      }
      upward = !upward;
    }
  }

  var MASKS = [
    function (x, y) { return (x + y) % 2 === 0; },
    function (x, y) { return y % 2 === 0; },
    function (x, y) { return x % 3 === 0; },
    function (x, y) { return (x + y) % 3 === 0; },
    function (x, y) { return (Math.floor(y / 2) + Math.floor(x / 3)) % 2 === 0; },
    function (x, y) { return (x * y) % 2 + (x * y) % 3 === 0; },
    function (x, y) { return ((x * y) % 2 + (x * y) % 3) % 2 === 0; },
    function (x, y) { return ((x + y) % 2 + (x * y) % 3) % 2 === 0; }
  ];

  function applyMask(mx, fn, mask) {
    var size = mx.size;
    for (var y = 0; y < size; y++) {
      for (var x = 0; x < size; x++) {
        if (fn[y * size + x]) continue;
        if (MASKS[mask](x, y)) mx.m[y * size + x] ^= 1;
      }
    }
  }

  function placeFormat(mx, mask) {
    var size = mx.size;
    var fmt = (0 /* ECC M = 00 */ << 3) | mask;
    var rem = fmt << 10;
    for (var i = 14; i >= 10; i--) {
      if ((rem >> i) & 1) rem ^= 0x537 << (i - 10);
    }
    var bits = ((fmt << 10) | rem) ^ 0x5412;
    for (var b = 0; b <= 5; b++) set(mx, 8, b, (bits >> b) & 1);
    set(mx, 8, 7, (bits >> 6) & 1);
    set(mx, 8, 8, (bits >> 7) & 1);
    set(mx, 7, 8, (bits >> 8) & 1);
    for (var b2 = 9; b2 <= 14; b2++) set(mx, 14 - b2, 8, (bits >> b2) & 1);
    for (var c = 0; c <= 7; c++) set(mx, size - 1 - c, 8, (bits >> c) & 1);
    for (var c2 = 8; c2 <= 14; c2++) set(mx, 8, size - 15 + c2, (bits >> c2) & 1);
  }

  /* The four penalty rules (N1=3, N2=3, N3=40, N4=10-step). */
  function penalty(mx) {
    var size = mx.size, score = 0, x, y;
    // N1: runs of same colour >= 5, rows and columns
    for (y = 0; y < size; y++) {
      var run = 1;
      for (x = 1; x <= size; x++) {
        if (x < size && get(mx, x, y) === get(mx, x - 1, y)) run++;
        else { if (run >= 5) score += 3 + (run - 5); run = 1; }
      }
    }
    for (x = 0; x < size; x++) {
      var runc = 1;
      for (y = 1; y <= size; y++) {
        if (y < size && get(mx, x, y) === get(mx, x, y - 1)) runc++;
        else { if (runc >= 5) score += 3 + (runc - 5); runc = 1; }
      }
    }
    // N2: 2x2 blocks of one colour
    for (y = 0; y < size - 1; y++) {
      for (x = 0; x < size - 1; x++) {
        var v = get(mx, x, y);
        if (v === get(mx, x + 1, y) && v === get(mx, x, y + 1) && v === get(mx, x + 1, y + 1)) score += 3;
      }
    }
    // N3: 1011101 with 0000 on either side, rows and columns
    var pat1 = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0], pat2 = [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1];
    function scan(getter, major) {
      for (var a = 0; a < size; a++) {
        for (var b = 0; b <= size - 11; b++) {
          var hit1 = true, hit2 = true;
          for (var k = 0; k < 11; k++) {
            var cell = getter(a, b + k);
            if (cell !== pat1[k]) hit1 = false;
            if (cell !== pat2[k]) hit2 = false;
          }
          if (hit1) score += 40;
          if (hit2) score += 40;
        }
      }
    }
    scan(function (a, i) { return get(mx, i, a); });
    scan(function (a, i) { return get(mx, a, i); });
    // N4: dark proportion
    var dark = 0;
    for (var i = 0; i < size * size; i++) if (mx.m[i] === 1) dark++;
    var pct = (dark * 100) / (size * size);
    score += Math.floor(Math.abs(pct - 50) / 5) * 10;
    return score;
  }

  function encode(text) {
    var bytes = utf8Bytes(String(text));
    var v = pickVersion(bytes.length);
    var codewords = buildCodewords(bytes, v);
    var fn = functionMask(v);
    var best = null, bestScore = Infinity, bestMask = 0;
    for (var mask = 0; mask < 8; mask++) {
      var mx = newMatrix(VER[v].size);
      placeFixed(mx, v);
      placeData(mx, fn, codewords);
      applyMask(mx, fn, mask);
      placeFormat(mx, mask);
      var s = penalty(mx);
      if (s < bestScore) { bestScore = s; best = mx; bestMask = mask; }
    }
    return { version: v, size: best.size, mask: bestMask, modules: Uint8Array.from(best.m) };
  }

  return { encode: encode, MAX_BYTES: 106 };
});
