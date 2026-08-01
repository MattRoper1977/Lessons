/* ============================================================================
   BUILD Animation Framework — food, nutrition and the balanced plate
   ---------------------------------------------------------------------------
   Registers into the BioSVG library (see bio-svg.js), so data-ba-asset="plate"
   works exactly like data-ba-asset="fish".

   Week 5, "What a Body Needs", and Week 6, "Building a Balanced Plate".

   Two rules govern everything in this file, because food is the one subject
   where a careless graphic does harm:

     1. Sorting is always by JOB or by GROUP — never by good food and bad food.
        The tick means "right column". It never means "good choice". No food in
        here ever gets a cross.
     2. The only ✖ in this file lands on a false STATEMENT ("every animal eats
        the same"), never on a food and never on an animal.

   Foods are drawn, not written. A word under an icon is a label; a word on its
   own is reading, and reading is the thing this framework exists to reduce.
   Food colour is identity rather than meaning — a grey apple is not an apple —
   so it sits outside the framework's motion palette by design.
   ========================================================================== */
/* ============================================================================
   BUILD Animation Framework — FOOD & NUTRITION SVG asset library
   ---------------------------------------------------------------------------
   Serves two lessons:

     WEEK 5  "What a Body Needs"     — three JOBS food does
     WEEK 6  "Building a Balanced Plate" — five GROUPS on the plate

   THE RULE THIS FILE OBEYS
     Pupils sort BY THE JOB or BY THE GROUP. Never by good food / bad food.
     So: no red cross ever lands on a food, and a green tick never means
     "healthy" — it means "right group". The narration says so out loud.

   Registers into the shared BioSVG library, so data-ba-asset="plate" works
   exactly like data-ba-asset="fish".

   PARTS
     plate       rim  seg-fruitveg seg-starchy seg-protein seg-dairy seg-oils
                 sizekey  drop-apple drop-pasta drop-chicken drop-yoghurt drop-oil
     jobs        job-energy job-growth job-working
                 food-bread food-protein food-fruitveg food-water
                 link-cow link-owl link-caterpillar link-goldfish
     <15 foods>  food            (one shared part name, so scripts port)

   AUTHOR NOTE — parts named drop-* food-* link-* start INVISIBLE via the css
   below, not via the engine's hidden-parts scan. That is deliberate: a short
   reveal script only names ONE of them, and the rest must not be sitting on
   screen giving the answer away. Those parts must therefore be switched on
   with `show` (which adds .ba-fadein) — never with a bare `pop` or `draw`.
   `show X + pop X` is fine and is what the scripts use.
   ========================================================================== */
(function (global) {
  'use strict';

  var H = global.BioSVG.helpers;
  var g = H.g, label = H.label, n = H.n;
  var BONE = H.BONE, SHELL = H.SHELL, SOFT = H.SOFT, INK = H.INK;

  var RAD = Math.PI / 180;
  function r2(v) { return (Math.round(v * 100) / 100).toString(); }

  /* parts that must start invisible — see AUTHOR NOTE above */
  /* Parts that must start invisible even before any script runs. Scoped to the
     two assets that need it: an unscoped [data-part^="food-"] rule would
     silently hide a similarly-named part in any other library that happened to
     be loaded on the same page. */
  /* Parts that must start invisible even before any script runs. Scoped to the
     two assets that need it: an unscoped [data-part^="food-"] rule would
     silently hide a similarly-named part in any other library loaded on the
     same page.  Both engines' "switched on" classes are listed — .ba-fadein /
     .ba-drew for build-anim, .g-in / .g-draw for grow-anim — so the asset works
     unchanged under either. */
  var ON = ['.ba-fadein', '.ba-drew', '.g-in', '.g-draw'];
  var HIDDEN = [['plate', 'drop-'], ['jobs', 'food-']];
  var HIDE_CSS = (function () {
    var off = [], on = [];
    HIDDEN.forEach(function (h) {
      var base = '[data-asset="' + h[0] + '"] [data-part^="' + h[1] + '"]';
      off.push(base);
      ON.forEach(function (c) { on.push(base + c); });
    });
    return off.join(',') + '{opacity:0}' + on.join(',') + '{opacity:1}' +
      '@media print{' + off.join(',') + '{opacity:1}}';
  })();

  /* ---------- small builders -------------------------------------------- */

  /* filled shape whose stroke-width is inherited from the icon group */
  function fp(d, op) {
    return '<path d="' + d + '" fill="currentColor" fill-opacity="' +
      (op == null ? 0.34 : op) + '" stroke="' + INK + '" pathLength="1"/>';
  }
  /* stroked line, width inherited */
  function ln(d, op) {
    return '<path d="' + d + '" fill="none" stroke="' + INK + '"' +
      (op == null ? '' : ' stroke-opacity="' + op + '"') + ' pathLength="1"/>';
  }
  /* filled circle, width inherited */
  function fc(cx, cy, r, op, fill) {
    return '<circle cx="' + n(cx) + '" cy="' + n(cy) + '" r="' + n(r) + '" fill="' +
      (fill || 'currentColor') + '"' + (fill ? '' : ' fill-opacity="' + (op == null ? 0.34 : op) + '"') +
      ' stroke="' + INK + '"/>';
  }
  function fe(cx, cy, rx, ry, op, rot) {
    return '<ellipse cx="' + n(cx) + '" cy="' + n(cy) + '" rx="' + n(rx) + '" ry="' + n(ry) +
      '" fill="currentColor" fill-opacity="' + (op == null ? 0.34 : op) + '" stroke="' + INK + '"' +
      (rot ? ' transform="rotate(' + n(rot) + ' ' + n(cx) + ' ' + n(cy) + ')"' : '') + '/>';
  }

  /* text. halo=true paints a white outline behind it so a word stays readable
     when the layer underneath changes colour on `hi`. */
  function txt(x, y, s, size, fill, halo, anchor, weight) {
    return '<text x="' + n(x) + '" y="' + n(y) + '" text-anchor="' + (anchor || 'middle') +
      '" font-size="' + size + '" font-weight="' + (weight || 800) + '" fill="' + (fill || INK) + '"' +
      (halo ? ' stroke="#ffffff" stroke-width="3.4" stroke-linejoin="round" paint-order="stroke"' : '') +
      ' font-family="system-ui,sans-serif">' + s + '</text>';
  }

  /* explicit-width plate parts (outside the icon groups) */
  function seg(d, op, w) {
    return '<path d="' + d + '" fill="currentColor" fill-opacity="' + op +
      '" stroke="' + INK + '" stroke-width="' + (w || 2.6) + '" stroke-linejoin="round" pathLength="1"/>';
  }
  function ring(cx, cy, r, col, w, op) {
    return '<circle cx="' + n(cx) + '" cy="' + n(cy) + '" r="' + n(r) + '" fill="none" stroke="' +
      col + '" stroke-width="' + w + '"' + (op ? ' stroke-opacity="' + op + '"' : '') + ' pathLength="1"/>';
  }
  function box(x, y, w, h, r, fill, stroke, sw) {
    return '<rect x="' + n(x) + '" y="' + n(y) + '" width="' + n(w) + '" height="' + n(h) +
      '" rx="' + r + '" fill="' + fill + '" stroke="' + stroke + '" stroke-width="' + sw + '"/>';
  }

  function wedge(cx, cy, r, a0, a1) {
    var x0 = cx + r * Math.cos(a0 * RAD), y0 = cy + r * Math.sin(a0 * RAD);
    var x1 = cx + r * Math.cos(a1 * RAD), y1 = cy + r * Math.sin(a1 * RAD);
    return 'M ' + n(cx) + ' ' + n(cy) + ' L ' + n(x0) + ' ' + n(y0) +
      ' A ' + n(r) + ' ' + n(r) + ' 0 ' + ((a1 - a0) > 180 ? 1 : 0) + ' 1 ' + n(x1) + ' ' + n(y1) + ' Z';
  }
  function polar(cx, cy, r, a) { return [cx + r * Math.cos(a * RAD), cy + r * Math.sin(a * RAD)]; }

  /* =========================================================================
     ICONS — every food and animal is drawn once, in a 64x64 box centred on
     (0,0), and reused at whatever size the lesson needs. Stroke width is set
     on the wrapper group and divided by the scale, so a bread slice has the
     same weight of outline whether it is 30px on a plate or 170px on its own.
     ====================================================================== */

  var ICONS = {};

  ICONS.bread = function () {
    return fp('M -24 20 L -24 -2 C -24 -23 -13 -31 0 -31 C 13 -31 24 -23 24 -2 L 24 20 ' +
      'Q 24 29 15 29 L -15 29 Q -24 29 -24 20 Z', 0.34) +
      ln('M -14 29 L -14 -1 C -14 -16 -8 -22 0 -22 C 8 -22 14 -16 14 -1 L 14 29', 0.55);
  };

  ICONS.rice = function () {
    return fp('M -30 2 L 30 2 A 30 30 0 0 1 -30 2 Z', 0.3) +
      fp('M -25 2 Q 0 -24 25 2 Z', 0.5) +
      '<g stroke-opacity="0.75">' +
      fe(-13, -4, 5, 2.6, 0.9, -28) + fe(-1, -11, 5, 2.6, 0.9, 12) +
      fe(12, -4, 5, 2.6, 0.9, 30) + fe(-6, 0, 5, 2.6, 0.9, -8) + fe(6, -1, 5, 2.6, 0.9, 20) +
      '</g>' +
      ln('M -31 2 L 31 2');
  };

  ICONS.pasta = function () {
    return fp('M -30 4 L 30 4 A 30 30 0 0 1 -30 4 Z', 0.3) +
      '<g fill="none" stroke="currentColor" stroke-opacity="0.95">' +
      '<path d="M -24 3 C -28 -14 -12 -20 -7 -4" pathLength="1"/>' +
      '<path d="M -13 3 C -19 -21 3 -28 6 -7" pathLength="1"/>' +
      '<path d="M -1 3 C -6 -25 15 -25 14 -5" pathLength="1"/>' +
      '<path d="M 11 3 C 6 -17 23 -21 24 -2" pathLength="1"/>' +
      '</g>' + ln('M -31 4 L 31 4');
  };

  ICONS.egg = function () {
    return fp('M 0 -30 C 13 -30 22 -13 22 2 C 22 18 13 29 0 29 C -13 29 -22 18 -22 2 ' +
      'C -22 -13 -13 -30 0 -30 Z', 0.26) + fc(0, 4, 10, 0.85);
  };

  ICONS.beans = function () {
    var bean = function (x, y, rot) {
      return '<path d="M -10 -2 C -11 -9 -2 -12 5 -9 C 11 -6 11 2 4 5 C -3 8 -9 4 -10 -2 Z" ' +
        'fill="currentColor" fill-opacity="0.6" stroke="' + INK + '" pathLength="1" ' +
        'transform="translate(' + n(x) + ' ' + n(y) + ') rotate(' + n(rot) + ')"/>';
    };
    return fp('M -30 6 A 30 26 0 0 0 30 6 Z', 0.28) +
      bean(-14, -4, -18) + bean(4, -8, 22) + bean(18, 0, -8) + bean(-4, 4, 8) + bean(13, 10, 34);
  };

  ICONS.fishfood = function () {
    return fp('M -28 0 C -20 -19 6 -21 17 -3 C 6 17 -20 17 -28 0 Z', 0.34) +
      fp('M 15 -3 L 30 -16 L 30 12 Z', 0.5) +
      fp('M -6 -13 Q 2 -22 10 -12 Z', 0.5) +
      fc(-16, -4, 3.4, 1, INK);
  };

  ICONS.chicken = function () {
    return fp('M -2 -24 C 15 -28 28 -13 24 4 C 20 19 3 26 -8 17 C -18 9 -18 -19 -2 -24 Z', 0.4) +
      '<g fill="none" stroke="' + INK + '" stroke-width="7"><path d="M -8 16 L -19 26"/></g>' +
      '<g fill="none" stroke="currentColor" stroke-width="5"><path d="M -8 16 L -19 26"/></g>' +
      fc(-24, 24, 7, 0.65) + fc(-17, 31, 7, 0.65);
  };

  ICONS.apple = function () {
    return fp('M 0 -13 C -9 -25 -28 -21 -28 -1 C -28 17 -14 29 0 22 C 14 29 28 17 28 -1 ' +
      'C 28 -21 9 -25 0 -13 Z', 0.4) +
      ln('M 0 -15 C 0 -24 2 -29 6 -33') +
      fp('M 7 -27 C 17 -34 27 -27 22 -18 C 13 -14 6 -20 7 -27 Z', 0.65);
  };

  ICONS.carrot = function () {
    return fp('M 0 31 L -13 -6 Q 0 -13 13 -6 Z', 0.45) +
      '<g stroke-opacity="0.6">' + ln('M -8 6 L -4 4') + ln('M 6 6 L 10 4') +
      ln('M -5 18 L -2 16') + '</g>' +
      '<g fill="none" stroke="currentColor">' +
      '<path d="M -3 -9 C -11 -18 -16 -24 -23 -28" pathLength="1"/>' +
      '<path d="M 0 -10 C 0 -21 0 -27 0 -32" pathLength="1"/>' +
      '<path d="M 3 -9 C 11 -18 16 -24 23 -28" pathLength="1"/>' +
      '</g>';
  };

  ICONS.broccoli = function () {
    return fp('M -8 30 L -7 2 L 7 2 L 8 30 Z', 0.5) +
      fp('M -28 0 A 12 12 0 0 1 -18 -15 A 14 14 0 0 1 -2 -25 A 14 14 0 0 1 15 -19 ' +
        'A 13 13 0 0 1 27 -2 A 12 12 0 0 1 18 8 L -18 8 A 12 12 0 0 1 -28 0 Z', 0.34) +
      '<g stroke-opacity="0.5">' + ln('M -13 -6 A 7 7 0 0 1 -2 -9') + ln('M 6 -12 A 7 7 0 0 1 17 -7') + '</g>';
  };

  ICONS.banana = function () {
    return fp('M -27 -18 C -32 -6 -23 15 -5 22 C 12 29 28 20 30 5 C 26 13 12 16 0 11 ' +
      'C -14 5 -21 -6 -21 -19 C -21 -22 -25 -22 -27 -18 Z', 0.42) +
      ln('M 30 5 L 31 -1');
  };

  ICONS.yoghurt = function () {
    return fp('M -21 -11 L 21 -11 L 15 27 Q 15 30 12 30 L -12 30 Q -15 30 -15 27 Z', 0.34) +
      fp('M -25 -20 L 25 -20 L 25 -10 L -25 -10 Z', 0.55) +
      '<g fill="none" stroke="' + INK + '"><path d="M 8 -20 L 19 -38" pathLength="1"/></g>' +
      fe(21, -40, 7, 9, 0.55, 24) +
      '<g stroke-opacity="0.5">' + ln('M -9 2 Q 0 8 9 2') + '</g>';
  };

  ICONS.cheese = function () {
    return fp('M -29 21 L 25 -19 Q 29 -22 29 -16 L 29 17 Q 29 21 25 21 Z', 0.42) +
      fc(8, 6, 5.4, 1, '#ffffff') + fc(19, 13, 3.6, 1, '#ffffff') + fc(15, -3, 4.2, 1, '#ffffff');
  };

  ICONS.oliveoil = function () {
    return fp('M -8 -22 L 8 -22 L 8 -14 Q 13 -9 13 -2 L 13 26 Q 13 30 9 30 L -9 30 ' +
      'Q -13 30 -13 26 L -13 -2 Q -13 -9 -8 -14 Z', 0.42) +
      fp('M -8 -31 L 8 -31 L 8 -23 L -8 -23 Z', 0.65) +
      box(-9, 4, 18, 13, 2, '#ffffff', INK, 0) +
      '<g stroke-width="1.4">' + box(-9, 4, 18, 13, 2, 'none', INK, 1.4) + '</g>' +
      fp('M 25 3 C 19 12 19 20 25 20 C 31 20 31 12 25 3 Z', 0.6);
  };

  ICONS.water = function () {
    return fp('M -18 -13 L 18 -13 L 13 27 Q 13 30 10 30 L -10 30 Q -13 30 -13 27 Z', 0.2) +
      fp('M -15.4 1 Q -7 -5 0 1 Q 7 7 15.4 1 L 12.6 27 Q 12.6 29 10 29 L -10 29 ' +
        'Q -12.6 29 -12.6 27 Z', 0.6) +
      fp('M 0 -33 C 7 -25 8 -19 0 -18 C -8 -19 -7 -25 0 -33 Z', 0.6);
  };

  /* ---- animals + their food (Week 5, We Do 2) --------------------------- */

  ICONS.cow = function () {
    return '<g fill="none" stroke="' + INK + '" stroke-width="6">' +
      '<path d="M -14 16 L -15 29"/><path d="M 2 16 L 2 29"/><path d="M 16 16 L 18 29"/></g>' +
      fp('M -22 -12 L 14 -12 Q 26 -12 26 0 L 26 10 Q 26 18 17 18 L -18 18 Q -26 18 -26 8 ' +
        'L -26 -2 Q -26 -12 -22 -12 Z', 0.34) +
      fp('M -24 -22 Q -14 -26 -8 -20 L -6 -10 Q -16 -6 -24 -10 Z', 0.42) +
      '<g fill="none" stroke="' + INK + '"><path d="M -22 -23 L -27 -30" pathLength="1"/>' +
      '<path d="M -9 -21 L -5 -29" pathLength="1"/></g>' +
      fc(-19, -16, 2.6, 1, INK) +
      fp('M 2 -6 Q 14 -8 16 2 Q 10 8 0 4 Z', 0.7) +
      fp('M -14 4 Q -6 0 -2 8 Q -8 14 -15 10 Z', 0.7) +
      '<g fill="none" stroke="' + INK + '"><path d="M 26 -6 Q 32 2 28 14" pathLength="1"/></g>';
  };

  ICONS.grass = function () {
    return '<g fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round">' +
      '<path d="M -24 28 C -22 8 -20 -4 -26 -18" pathLength="1"/>' +
      '<path d="M -12 28 C -12 6 -8 -8 -2 -22" pathLength="1"/>' +
      '<path d="M 0 28 C 0 8 0 -6 0 -26" pathLength="1"/>' +
      '<path d="M 12 28 C 12 6 8 -8 2 -20" pathLength="1"/>' +
      '<path d="M 24 28 C 22 8 20 -4 26 -16" pathLength="1"/>' +
      '</g>' + '<g fill="none" stroke="' + INK + '"><path d="M -30 29 L 30 29" pathLength="1"/></g>';
  };

  ICONS.owl = function () {
    return fp('M 0 -24 C 19 -24 28 -8 28 8 C 28 24 16 30 0 30 C -16 30 -28 24 -28 8 ' +
      'C -28 -8 -19 -24 0 -24 Z', 0.34) +
      fp('M -19 -18 L -25 -31 L -10 -24 Z', 0.5) + fp('M 19 -18 L 25 -31 L 10 -24 Z', 0.5) +
      fc(-11, -6, 10, 1, '#ffffff') + fc(11, -6, 10, 1, '#ffffff') +
      fc(-11, -6, 4.6, 1, INK) + fc(11, -6, 4.6, 1, INK) +
      fp('M 0 -1 L -5 7 L 5 7 Z', 0.8) +
      '<g fill="none" stroke="' + INK + '" stroke-opacity="0.55">' +
      '<path d="M -22 4 Q -18 18 -10 26" pathLength="1"/>' +
      '<path d="M 22 4 Q 18 18 10 26" pathLength="1"/></g>';
  };

  ICONS.mouse = function () {
    return '<g fill="none" stroke="' + INK + '" stroke-width="3">' +
      '<path d="M 18 14 C 30 14 30 -2 22 -2" pathLength="1"/></g>' +
      fc(-16, -8, 12, 0.5) + fc(10, -10, 11, 0.5) +
      fp('M -22 6 C -22 -8 -6 -16 6 -14 C 20 -12 24 0 20 12 C 16 22 -18 22 -22 6 Z', 0.34) +
      fp('M -22 6 L -32 12 L -22 17 Z', 0.5) +
      fc(-16, 2, 2.8, 1, INK) + fc(-30, 12, 2.6, 1, INK);
  };

  ICONS.caterpillar = function () {
    var s = '';
    [[-24, 6], [-11, 2], [2, 0], [15, 3]].forEach(function (p) { s += fc(p[0], p[1], 11, 0.4); });
    return '<g fill="none" stroke="' + INK + '" stroke-width="3">' +
      '<path d="M 24 -10 L 30 -22" pathLength="1"/><path d="M 30 -8 L 38 -18" pathLength="1"/></g>' +
      s + fc(27, -3, 13, 0.62) +
      fc(31, -7, 3, 1, INK) +
      '<g fill="none" stroke="' + INK + '" stroke-width="3.4">' +
      '<path d="M -22 17 L -24 26" pathLength="1"/><path d="M -9 13 L -10 23" pathLength="1"/>' +
      '<path d="M 4 11 L 4 22" pathLength="1"/><path d="M 17 14 L 18 24" pathLength="1"/></g>';
  };

  ICONS.leaves = function () {
    return '<g fill="none" stroke="' + INK + '" stroke-width="3.4">' +
      '<path d="M 4 30 C 4 14 4 4 4 -6" pathLength="1"/></g>' +
      fp('M 2 4 C -14 4 -26 -6 -26 -18 C -12 -22 2 -14 2 4 Z', 0.4) +
      fp('M 6 -6 C 20 -8 30 -18 28 -30 C 14 -30 4 -20 6 -6 Z', 0.4) +
      '<g stroke-opacity="0.5">' + ln('M 2 2 L -22 -17') + ln('M 6 -8 L 26 -27') + '</g>';
  };

  ICONS.flakes = function () {
    var f = '', pts = [[-20, 12, 20], [-6, 20, -14], [8, 10, 34], [20, 20, -6],
                       [-14, -2, 40], [2, 2, -24], [16, -6, 14]];
    pts.forEach(function (p) {
      f += '<path d="M -6 -3 L 5 -5 L 7 3 L -4 5 Z" fill="currentColor" fill-opacity="0.6" stroke="' +
        INK + '" pathLength="1" transform="translate(' + p[0] + ' ' + p[1] + ') rotate(' + p[2] + ')"/>';
    });
    return fp('M -14 -30 L 14 -30 L 11 -14 L -11 -14 Z', 0.34) +
      '<g stroke-opacity="0.6">' + ln('M -14 -30 L 14 -30') + '</g>' + f;
  };

  ICONS.goldfish = function () {
    return fp('M 12 0 L 30 -16 Q 32 12 12 14 Z', 0.5) +
      fp('M -28 0 C -24 -18 0 -22 14 -6 C 14 10 -12 18 -28 0 Z', 0.34) +
      fp('M -8 -14 Q 0 -24 8 -12 Z', 0.55) +
      fp('M -6 10 Q -2 20 6 12 Z', 0.55) +
      fc(-17, -3, 4, 1, '#ffffff') + fc(-17, -3, 2.2, 1, INK) +
      '<g stroke-opacity="0.45">' + ln('M -6 -8 Q -3 0 -6 8') + '</g>';
  };

  /* ---- the three job marks (⚡ ▲ ⚙ in the lesson's own shorthand) -------- */

  ICONS.bolt = function () {
    return fp('M 8 -30 L -18 4 L -3 4 L -8 30 L 18 -6 L 3 -6 Z', 0.85);
  };
  ICONS.up = function () {
    return fp('M 0 -30 L 28 12 L -28 12 Z', 0.85);
  };
  ICONS.cog = function () {
    var d = '', i, a, r1 = 30, r2 = 21;
    for (i = 0; i < 8; i++) {
      a = i * 45;
      d += (i ? ' L ' : 'M ') + [a - 12, a - 12, a + 12, a + 12].map(function (t, k) {
        var rr = (k === 0 || k === 3) ? r2 : r1;
        return n(rr * Math.cos(t * RAD)) + ' ' + n(rr * Math.sin(t * RAD));
      }).join(' L ');
    }
    return fp(d + ' Z', 0.85) + fc(0, 0, 10, 1, '#ffffff');
  };

  /* wrapper: place an icon at (cx,cy) at scale s with rendered stroke width sw */
  function ic(name, cx, cy, s, sw) {
    if (!ICONS[name]) return '';
    return '<g transform="translate(' + n(cx) + ' ' + n(cy) + ') scale(' + r2(s) + ')" ' +
      'stroke-width="' + r2((sw || 3) / s) + '" stroke-linejoin="round" stroke-linecap="round">' +
      ICONS[name]() + '</g>';
  }
  /* icon with a short word under it — the two together are the label */
  function icw(name, cx, cy, s, word, wordY, size, sw) {
    return ic(name, cx, cy, s, sw) + txt(cx, wordY, word, size || 11, INK, true);
  }

  var A = {};

  /* =========================================================================
     WEEK 6 — THE BALANCED PLATE
     Five sections, biggest to smallest, read by icon + word + SIZE.
     ====================================================================== */

  var P = { x: 176, y: 152, r: 100 };
  var SEGS = [
    { key: 'fruitveg', a0: -140, a1: -10, mid: -75, col: BONE,  op: 0.42, word: 'FRUIT & VEG', fs: 12,   ru: 70, mk: 1,    mark: 'disc',    drop: 34, dscale: 0.5 },
    { key: 'starchy',  a0: -10,  a1: 100, mid: 45,  col: SHELL, op: 0.32, word: 'STARCHY',     fs: 11.5, ru: 68, mk: 1,    mark: 'square',  drop: 34, dscale: 0.5 },
    { key: 'protein',  a0: 100,  a1: 156, mid: 128, col: SOFT,  op: 0.58, word: 'PROTEIN',     fs: 11.5, ru: 64, mk: 0.95, mark: 'tri',     drop: 34, dscale: 0.5 },
    /* The two smallest slices are too narrow to hold a mark AND a word AND a
       food, so their labels sit outside the plate on a dotted leader. That is
       not a compromise — it says out loud which sections are the small ones. */
    { key: 'dairy',    a0: 156,  a1: 194, mid: 175, col: BONE,  op: 0.3,  word: 'DAIRY',       fs: 11,   mk: 0.9,  mark: 'diamond', drop: 70, dscale: 0.42, ddy: 5,
      out: { mx: 30, my: 152, lines: [['DAIRY', 174, 10.5]], leader: [54, 170, 94, 161] } },
    { key: 'oils',     a0: 194,  a1: 220, mid: 207, col: SHELL, op: 0.8,  word: 'OILS',        fs: 10,   mk: 0.85, mark: 'donut',   drop: 80, dscale: 0.5,
      out: { mx: 30, my: 84,  lines: [['OILS &', 106, 10], ['SPREADS', 118, 10]], leader: [54, 112, 96, 126] } }
  ];

  function mark(kind, x, y, k) {
    k = k || 1;
    if (kind === 'disc')    return '<circle cx="' + n(x) + '" cy="' + n(y) + '" r="' + n(8 * k) + '" fill="currentColor" stroke="' + INK + '" stroke-width="1.8"/>';
    if (kind === 'square')  return box(x - 7.5 * k, y - 7.5 * k, 15 * k, 15 * k, 2, 'currentColor', INK, 1.8);
    if (kind === 'tri')     return '<path d="M ' + n(x) + ' ' + n(y - 8.5 * k) + ' L ' + n(x + 8.5 * k) + ' ' + n(y + 6.5 * k) + ' L ' + n(x - 8.5 * k) + ' ' + n(y + 6.5 * k) + ' Z" fill="currentColor" stroke="' + INK + '" stroke-width="1.8" stroke-linejoin="round"/>';
    if (kind === 'diamond') return '<path d="M ' + n(x) + ' ' + n(y - 7 * k) + ' L ' + n(x + 7 * k) + ' ' + n(y) + ' L ' + n(x) + ' ' + n(y + 7 * k) + ' L ' + n(x - 7 * k) + ' ' + n(y) + ' Z" fill="currentColor" stroke="' + INK + '" stroke-width="1.8" stroke-linejoin="round"/>';
    return '<circle cx="' + n(x) + '" cy="' + n(y) + '" r="' + n(6.5 * k) + '" fill="#ffffff" stroke="' + INK + '" stroke-width="2.6"/>';
  }

  var DROPS = { fruitveg: 'apple', starchy: 'pasta', protein: 'chicken', dairy: 'yoghurt', oils: 'oliveoil' };
  var DROPKEY = { fruitveg: 'drop-apple', starchy: 'drop-pasta', protein: 'drop-chicken', dairy: 'drop-yoghurt', oils: 'drop-oil' };

  A.plate = {
    title: 'The balanced plate',
    alt: 'A round plate cut into five sections of different sizes. The biggest is fruit and vegetables, ' +
      'then starchy foods, then protein, then dairy, and the smallest slice is oils and spreads. ' +
      'A size key down the right side lists them biggest to smallest.',
    css: HIDE_CSS,
    svg: function () {
      var out = g('rim', SOFT,
        ring(P.x, P.y, P.r + 6, SOFT, 9) + ring(P.x, P.y, P.r, INK, 3));

      SEGS.forEach(function (s) {
        var d = polar(P.x, P.y, s.drop, s.mid); d[1] += (s.ddy || 0);
        var inner = seg(wedge(P.x, P.y, P.r, s.a0, s.a1), s.op);
        if (s.out) {
          var o = s.out;
          inner += '<path d="M ' + o.leader.slice(0, 2).join(' ') + ' L ' + o.leader.slice(2).join(' ') +
            '" fill="none" stroke="currentColor" stroke-width="2.6" stroke-dasharray="4 4" stroke-linecap="round"/>' +
            mark(s.mark, o.mx, o.my, s.mk);
          o.lines.forEach(function (L) { inner += txt(o.mx, L[1], L[0], L[2], INK, false); });
        } else {
          var u = polar(P.x, P.y, s.ru, s.mid);
          inner += mark(s.mark, u[0], u[1] - 15, s.mk) + txt(u[0], u[1] + 12, s.word, s.fs, INK, true);
        }
        out += g('seg-' + s.key, s.col, inner);
        out += g(DROPKEY[s.key], s.col === SOFT ? BONE : s.col,
          ic(DROPS[s.key], d[0], d[1], s.dscale, 2.4));
      });

      /* the size key: same five marks, bars in strict size order */
      var keyrows = '', ky = 116;
      SEGS.forEach(function (s, i) {
        var len = (s.a1 - s.a0) / 130 * 72;
        keyrows += mark(s.mark, 306, ky + i * 32, 0.8) +
          box(318, ky + i * 32 - 6, len, 12, 3, 'currentColor', INK, 1.6);
      });
      out += g('sizekey', SOFT,
        txt(348, 100, 'BIGGEST', 10, INK, false) + keyrows +
        txt(348, 268, 'SMALLEST', 10, INK, false));

      return out +
        label('answer', 8, 4, 'OILS & SPREADS', INK) +
        label('balance', 8, 266, 'SOME FROM EVERY PART', INK);
    },
    teach:
      'draw rim                                                  :: An empty plate. Nothing on it yet.\n' +
      'show seg-fruitveg + glow seg-fruitveg                     :: Fruit and vegetables. Look how big that piece is. The BIGGEST.\n' +
      'unglow seg-fruitveg + show seg-starchy + glow seg-starchy  :: Starchy foods next — bread, rice, pasta. Nearly as big.\n' +
      'unglow seg-starchy + show seg-protein + glow seg-protein   :: Protein — eggs, beans, fish, chicken. Smaller than those two.\n' +
      'unglow seg-protein + show seg-dairy + glow seg-dairy       :: Dairy — milk, cheese, yoghurt. Smaller again.\n' +
      'unglow seg-dairy + show seg-oils + glow seg-oils           :: Oils and spreads. The smallest piece on the whole plate.\n' +
      'unglow seg-oils + show sizekey                             :: Biggest at the top, smallest at the bottom. The SIZE tells you how much.\n' +
      'label balance                                              :: Balance means some from every part. Not equal slices — some from each.\n' +
      'note "There are no bad foods on this plate. There are everyday ones and sometimes ones." :: Nobody is in trouble for the small sections. Small does not mean bad.',
    revealApple:
      'show drop-apple + pulse drop-apple                        :: An apple. Which part of the plate does it go in?\n' +
      'unpulse drop-apple + glow seg-fruitveg + hi seg-fruitveg  :: Fruit and vegetables — and that is the biggest part.\n' +
      'label answer "FRUIT & VEG" + tick                         :: Right group. The tick means right GROUP — nothing else.',
    revealPasta:
      'show drop-pasta + pulse drop-pasta                        :: Pasta. Which part?\n' +
      'unpulse drop-pasta + glow seg-starchy + hi seg-starchy    :: Starchy foods. Same section as bread and rice.\n' +
      'label answer "STARCHY FOODS" + tick                       :: Right group. Big section — pasta is an everyday one.',
    revealChicken:
      'show drop-chicken + pulse drop-chicken                    :: Chicken. Which part?\n' +
      'unpulse drop-chicken + glow seg-protein + hi seg-protein  :: Protein. It sits with eggs, beans and fish.\n' +
      'label answer "PROTEIN" + tick                             :: Right group. A medium-sized part of the plate.',
    revealYoghurt:
      'show drop-yoghurt + pulse drop-yoghurt                    :: Yoghurt. Which part?\n' +
      'unpulse drop-yoghurt + glow seg-dairy + hi seg-dairy      :: Dairy. Milk, cheese, yoghurt — all in here.\n' +
      'label answer "DAIRY" + tick                               :: Right group. A small part, but still on the plate.',
    revealOil:
      'show drop-oil + pulse drop-oil                            :: Olive oil. Which part?\n' +
      'unpulse drop-oil + glow seg-oils + hi seg-oils            :: Oils and spreads — the smallest piece of all.\n' +
      'label answer "OILS & SPREADS" + tick                      :: Right group. Smallest is still ON the plate. Not banned.',
    reveal:
      'glow seg-fruitveg + hi seg-fruitveg   :: Biggest part — fruit and vegetables.\n' +
      'unglow seg-fruitveg + unhi seg-fruitveg + glow seg-oils + hi seg-oils :: Smallest part — oils and spreads.\n' +
      'unglow seg-oils + show sizekey + label balance + tick :: Some from every part. That is a balanced plate.'
  };

  /* =========================================================================
     WEEK 5 — THE THREE JOBS FOOD DOES
     Three headed cards. Pupils sort by the JOB, never by good food / bad food.
     ====================================================================== */

  var CARD = { y: 90, h: 202, w: 118, head: 58 };
  var JOBS = [
    { key: 'energy',  x: 10,  col: SHELL, icon: 'bolt', lines: ['ENERGY'],
      rows: [{ part: 'food-bread',    col: SHELL, a: [['bread', 'BREAD'], ['rice', 'RICE']], b: [['pasta', 'PASTA']] }] },
    { key: 'growth',  x: 141, col: BONE,  icon: 'up',   lines: ['GROWTH &', 'REPAIR'],
      rows: [{ part: 'food-protein',  col: BONE,  a: [['egg', 'EGGS'], ['beans', 'BEANS']], b: [['fishfood', 'FISH']] }] },
    { key: 'working', x: 272, col: SOFT,  icon: 'cog',  lines: ['KEEPS THE BODY', 'WORKING'],
      rows: [{ part: 'food-fruitveg', col: SOFT,  a: [['apple', 'FRUIT'], ['carrot', 'VEG']] },
             { part: 'food-water',    col: BONE,  b: [['water', 'WATER']] }] }
  ];
  var ROW_A = 190, ROW_B = 252;

  function slot(name, ix, rowY, word) {
    return ic(name, ix, rowY - 10, 0.6, 2.8) + txt(ix, rowY + 24, word, 10.5, INK, false);
  }

  A.jobs = {
    title: 'The three jobs food does',
    alt: 'Three cards side by side. A lightning bolt card headed ENERGY holds bread, rice and pasta. ' +
      'A triangle card headed GROWTH AND REPAIR holds eggs, beans and fish. A cog card headed KEEPS THE ' +
      'BODY WORKING holds fruit, vegetables and water.',
    css: HIDE_CSS,
    svg: function () {
      var out = '';
      JOBS.forEach(function (j) {
        var cx = j.x + CARD.w / 2, hb = CARD.y + CARD.head;
        var head = '<path d="M ' + n(j.x) + ' ' + n(CARD.y + 12) + ' Q ' + n(j.x) + ' ' + n(CARD.y) +
          ' ' + n(j.x + 12) + ' ' + n(CARD.y) + ' L ' + n(j.x + CARD.w - 12) + ' ' + n(CARD.y) +
          ' Q ' + n(j.x + CARD.w) + ' ' + n(CARD.y) + ' ' + n(j.x + CARD.w) + ' ' + n(CARD.y + 12) +
          ' L ' + n(j.x + CARD.w) + ' ' + n(hb) + ' L ' + n(j.x) + ' ' + n(hb) +
          ' Z" fill="currentColor" fill-opacity="0.34" stroke="' + INK + '" stroke-width="2.4"/>';
        var words = '';
        j.lines.forEach(function (L, i) {
          words += txt(cx, j.lines.length === 1 ? 141 : 134 + i * 13, L,
            j.lines.length === 1 ? 13 : 10.5, INK, false);
        });
        out += g('job-' + j.key, j.col,
          box(j.x, CARD.y, CARD.w, CARD.h, 12, '#ffffff', INK, 2.4) + head +
          ic(j.icon, cx, 112, 0.34, 2.4) + words);

        j.rows.forEach(function (r) {
          var inner = '';
          (r.a || []).forEach(function (f, i) { inner += slot(f[0], cx + (i ? 27 : -27), ROW_A, f[1]); });
          (r.b || []).forEach(function (f) { inner += slot(f[0], cx, ROW_B, f[1]); });
          out += g(r.part, r.col, inner);
        });
      });
      return out +
        label('three',  8, 8,  'FOOD DOES THREE JOBS', INK) +
        label('answer', 8, 46, 'KEEPS BODY WORKING', INK);
    },
    teach:
      'show job-energy + glow job-energy                          :: Job one. Food gives a body ENERGY. Running, playing, staying warm.\n' +
      'show food-bread + pop food-bread                           :: Bread. Rice. Pasta. These are the energy ones.\n' +
      'unglow job-energy + show job-growth + glow job-growth      :: Job two. GROWTH and REPAIR. Getting taller. Mending a cut.\n' +
      'show food-protein + pop food-protein                       :: Eggs. Beans. Fish. These are the building ones.\n' +
      'unglow job-growth + show job-working + glow job-working    :: Job three. KEEPING THE BODY WORKING. Eyes, skin, blood, tummy.\n' +
      'show food-fruitveg + pop food-fruitveg                     :: Fruit and vegetables do that job.\n' +
      'show food-water + pop food-water                           :: And water. Water is not a food — but nothing works without it.\n' +
      'unglow job-working + pulse job-energy,job-growth,job-working + label three :: Three jobs. Count them with me. One. Two. Three.\n' +
      'unpulse job-energy,job-growth,job-working + think          :: Now — is there ONE food that can do all three on its own? Have a think.\n' +
      'unthink + note "No single food does all three jobs. That is why we eat different types." :: No. Nothing here does all three. That is why we eat different types.',
    revealBread:
      'show food-bread + pulse food-bread                         :: Bread and rice. What JOB do they do for a body?\n' +
      'unpulse food-bread + glow job-energy + hi job-energy       :: ENERGY. Running, playing, staying warm.\n' +
      'label answer "ENERGY" + tick                               :: Right column. The tick means right JOB — not good food or bad food.',
    revealProtein:
      'show food-protein + pulse food-protein                     :: Eggs, beans and fish. What JOB do they do?\n' +
      'unpulse food-protein + glow job-growth + hi job-growth     :: GROWTH and REPAIR. The building ones.\n' +
      'label answer "GROWTH & REPAIR" + tick                      :: Right column. Tick means right JOB. Nothing else.',
    revealFruitveg:
      'show food-fruitveg + pulse food-fruitveg                   :: Fruit and vegetables. What JOB do they do?\n' +
      'unpulse food-fruitveg + glow job-working + hi job-working  :: They KEEP THE BODY WORKING. Eyes, skin, blood, tummy.\n' +
      'label answer "KEEPS BODY WORKING" + tick                   :: Right column. Tick means right JOB.',
    revealWater:
      'show food-water + pulse food-water                         :: Water. Careful — this one is not really a food.\n' +
      'unpulse food-water + glow job-working + hi job-working     :: It still does a job. It KEEPS THE BODY WORKING.\n' +
      'label answer "KEEPS BODY WORKING" + tick                   :: Right column. A body cannot work at all without water.',
    reveal:
      'glow job-energy + hi job-energy                            :: Job one — energy.\n' +
      'unhi job-energy + unglow job-energy + glow job-growth + hi job-growth :: Job two — growth and repair.\n' +
      'unhi job-growth + unglow job-growth + glow job-working + hi job-working :: Job three — keeping the body working.\n' +
      'unglow job-working + unhi job-working + label three + tick :: Three jobs. No single food does all three.'
  };

  /* =========================================================================
     WEEK 5, WE DO 2 — WHICH ANIMAL EATS WHAT
     The only ✖ in this file lands on the FALSE STATEMENT "every animal eats
     the same" — never on a food and never on an animal.
     ====================================================================== */

  var PAIRS = [
    { key: 'cow',         y: 42,  animal: 'cow',         aw: 'COW',         food: 'grass',  fw: 'GRASS',       ans: 'A COW EATS GRASS' },
    { key: 'owl',         y: 100, animal: 'owl',         aw: 'OWL',         food: 'mouse',  fw: 'MOUSE',       ans: 'AN OWL EATS A MOUSE' },
    { key: 'caterpillar', y: 158, animal: 'caterpillar', aw: 'CATERPILLAR', food: 'leaves', fw: 'LEAVES',      ans: 'A CATERPILLAR EATS LEAVES' },
    { key: 'goldfish',    y: 216, animal: 'goldfish',    aw: 'GOLDFISH',    food: 'flakes', fw: 'FISH FLAKES', ans: 'A GOLDFISH EATS FLAKES' }
  ];


  function arrowTo(x1, x2, y) {
    return '<path d="M ' + n(x1) + ' ' + n(y) + ' L ' + n(x2 - 15) + ' ' + n(y) +
      '" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" pathLength="1"/>' +
      '<path d="M ' + n(x2 - 17) + ' ' + n(y - 10) + ' L ' + n(x2) + ' ' + n(y) + ' L ' +
      n(x2 - 17) + ' ' + n(y + 10) + ' Z" fill="currentColor" stroke="currentColor" stroke-width="2"/>';
  }

  A.animalfood = {
    title: 'Which animal eats what',
    alt: 'Four rows. A cow with an arrow to grass, an owl to a mouse, a caterpillar to ' +
         'leaves, and a goldfish to fish flakes. Every animal is joined to a different food.',
    svg: function () {
      var out = '';
      PAIRS.forEach(function (p, i) {
        var y = 62 + i * 60;
        out += g('animal-' + p.key, BONE,
          ic(p.animal, 52, y, 0.44, 2.6) + txt(88, y + 5, p.aw, 12, INK, true, 'start'));
        out += g('arrow-' + p.key, SHELL, arrowTo(196, 252, y));
        out += g('eat-' + p.key, SHELL,
          ic(p.food, 272, y, 0.44, 2.6) + txt(304, y + 5, p.fw, 11, INK, true, 'start'));
      });
      return out +
        label('same', 12, 8, 'NOT TRUE', '#dc2626') +
        label('diff', 146, 8, 'NOT ALL THE SAME', BONE);
    },
    teach:
      'show animal-cow,animal-owl,animal-caterpillar,animal-goldfish :: Four animals. Nothing alike about them.\n' +
      'show arrow-cow + trace arrow-cow + show eat-cow               :: A cow eats grass. All day.\n' +
      'show arrow-owl + trace arrow-owl + show eat-owl               :: An owl eats a mouse.\n' +
      'show arrow-caterpillar + trace arrow-caterpillar + show eat-caterpillar :: A caterpillar eats leaves.\n' +
      'show arrow-goldfish + trace arrow-goldfish + show eat-goldfish :: A goldfish eats flakes.\n' +
      'think                                                        :: So could you swap them round? Could the goldfish manage the grass?\n' +
      'unthink + label diff                                         :: No. Different bodies need different food.',
    revealCow:
      'show animal-cow + think        :: A cow. What does a cow eat?\n' +
      'unthink + show arrow-cow + trace arrow-cow + show eat-cow + tick :: Grass.',
    revealOwl:
      'show animal-owl + think        :: An owl. What does an owl eat?\n' +
      'unthink + show arrow-owl + trace arrow-owl + show eat-owl + tick :: A mouse. Owls are hunters.',
    revealCaterpillar:
      'show animal-caterpillar + think :: A caterpillar. What does it eat?\n' +
      'unthink + show arrow-caterpillar + trace arrow-caterpillar + show eat-caterpillar + tick :: Leaves. Nothing else.',
    revealGoldfish:
      'show animal-goldfish + think   :: A goldfish. What does it eat?\n' +
      'unthink + show arrow-goldfish + trace arrow-goldfish + show eat-goldfish + tick :: Flakes.',
    revealSame:
      'show animal-cow,animal-goldfish + think :: Every animal eats the same. True or not true?\n' +
      'unthink + cross + label same            :: Not true. Put a goldfish in a field and it would starve.\n' +
      'show arrow-cow,eat-cow,arrow-goldfish,eat-goldfish :: Different bodies. Different food.',
    reveal:
      'show animal-cow,animal-owl,animal-caterpillar,animal-goldfish :: Four animals.\n' +
      'show arrow-cow,arrow-owl,arrow-caterpillar,arrow-goldfish + show eat-cow,eat-owl,eat-caterpillar,eat-goldfish :: Four different foods.\n' +
      'label diff + tick :: Different bodies need different food.'
  };


  global.BioSVG.register(A);
})(typeof window !== 'undefined' ? window : this);
