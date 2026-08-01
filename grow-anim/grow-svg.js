/* ============================================================================
   GROW ANIMATION FRAMEWORK · Phase 2 — SVG SCIENCE LIBRARY (core)
   ---------------------------------------------------------------------------
   This file is the registry and the drawing kit. The actual science assets live
   in grow-svg-bio.js, grow-svg-phy.js and grow-svg-chem.js, each of which calls
   GrowSVG.register().

   THE RULE THAT MAKES EVERYTHING ELSE POSSIBLE
     Nothing is a picture. Everything is LAYERS.
     Every structure a teacher might want to draw, glow, fade, morph, trace or
     zoom on its own is its own <g data-part="name">. That single decision is
     what turns a diagram into a teaching instrument, and it is why this phase
     is worth more than any of the animation code.

   PORTABLE PART NAMES
     Scripts should be readable across assets, so parts reuse names wherever the
     science allows:
       body scene ground object      the physical situation
       label-*                       a <g data-label="x"> that starts hidden
       force friction gravity        invisible-science overlay layers
       energy heat particle field    (as data-overlay="…", not data-part)
       current pressure light air

   EACH ASSET DECLARES
     title    what to call it on screen
     alt      a real description, for a pupil using a screen reader
     tags     subject + topic, for the demo page and for search
     svg()    the layered markup
     teach    the full I-Do sequence          (@teach)
     reveal   the short We-Do answer          (@reveal)
     process  the scientific process running  (@process)   — Phase 5
     wrong    the misconception, animated     (@wrong)     — Phase 10
     right    the same scene, corrected       (@right)     — Phase 10
     retrieve the recall sequence             (@retrieve)  — Phase 9

   USAGE
     GrowSVG.render('circuit')             -> '<svg …>…</svg>'
     GrowSVG.script('circuit', 'teach')    -> the teaching script
     GrowSVG.list('physics')               -> ['circuit', 'friction', …]
   ========================================================================== */
(function (global) {
  'use strict';

  var A = {};

  /* --------------------------------------------------------- house palette
     Chosen so that GLOW (which uses currentColor) reads clearly on every one,
     and so the three subjects are distinguishable at a glance from the back of
     a classroom. Assets set colour per LAYER, never per shape. */
  var C = {
    bone:    '#4E7A9B',   /* skeleton, hard structure                 */
    soft:    '#94a3b8',   /* body outline, soft tissue, neutral scene */
    ink:     '#1f2937',   /* outline ink — keeps shapes legible       */
    organ:   '#c2544d',   /* organs, blood, muscle                    */
    plant:   '#3F7D6E',   /* plants, producers, chlorophyll           */
    force:   '#dc2626',   /* forces — always red, in every subject    */
    energy:  '#d97706',   /* energy and heat — always amber           */
    particle:'#7c3aed',   /* particles and models — always violet     */
    field:   '#0891b2',   /* fields, waves, current                   */
    metal:   '#64748b',   /* metals, apparatus, wires                 */
    water:   '#38bdf8',   /* water, liquids, solutions                */
    acid:    '#e11d48',   /* acids                                    */
    alkali:  '#2563eb',   /* alkalis                                  */
    neutral: '#16a34a',   /* neutral / correct                        */
    white:   '#ffffff'
  };

  /* ------------------------------------------------------- small builders */

  function n(v) { return (Math.round(v * 10) / 10).toString(); }

  /* a layer — the unit the animation engine addresses */
  function g(part, colour, inner, extra) {
    return '<g data-part="' + part + '" style="color:' + (colour || C.ink) + '"' +
      (extra || '') + '>' + inner + '</g>';
  }

  /* An invisible-science overlay layer: present in the DOM from the start,
     switched on by the teacher. The scene never changes — only what can be
     seen of it.

     It carries data-part as well as data-overlay, so once a layer is on, the
     teacher can glow it, pulse it or fade it like anything else. Being
     invisible to begin with should not make a thing second-class. */
  function ov(name, colour, inner) {
    return '<g data-overlay="' + name + '" data-part="' + name + '" style="color:' +
      (colour || C.force) + '">' + inner + '</g>';
  }

  function shape(d, sw) {
    return '<path d="' + d + '" fill="currentColor" stroke="' + C.ink +
      '" stroke-width="' + (sw == null ? 1.6 : sw) + '" stroke-linejoin="round"/>';
  }
  function stroke(d, sw, colour, cap) {
    return '<path d="' + d + '" fill="none" stroke="' + (colour || 'currentColor') +
      '" stroke-width="' + (sw || 3) + '" stroke-linecap="' + (cap || 'round') + '" stroke-linejoin="round"/>';
  }
  function dot(x, y, r, colour) {
    return '<circle cx="' + n(x) + '" cy="' + n(y) + '" r="' + n(r) + '" fill="' + (colour || 'currentColor') + '"/>';
  }
  function circ(x, y, r, sw) {
    return '<circle cx="' + n(x) + '" cy="' + n(y) + '" r="' + n(r) +
      '" fill="currentColor" stroke="' + C.ink + '" stroke-width="' + (sw == null ? 1.6 : sw) + '"/>';
  }
  function rect(x, y, w, h, r, sw) {
    return '<rect x="' + n(x) + '" y="' + n(y) + '" width="' + n(w) + '" height="' + n(h) +
      '" rx="' + n(r || 0) + '" fill="currentColor" stroke="' + C.ink +
      '" stroke-width="' + (sw == null ? 1.6 : sw) + '"/>';
  }
  function txt(x, y, s, size, colour, anchor) {
    return '<text x="' + n(x) + '" y="' + n(y) + '" font-size="' + (size || 12) +
      '" font-weight="800" fill="' + (colour || C.ink) + '" text-anchor="' + (anchor || 'middle') + '">' +
      s + '</text>';
  }

  /* An arrow. Forces are ALWAYS drawn like this, in every subject, so that a
     pupil meeting force arrows in chemistry recognises them from physics. */
  function arrow(x1, y1, x2, y2, colour, sw, label) {
    var dx = x2 - x1, dy = y2 - y1, L = Math.sqrt(dx * dx + dy * dy) || 1;
    var ux = dx / L, uy = dy / L, hx = x2 - ux * 11, hy = y2 - uy * 11;
    var px = -uy * 6.5, py = ux * 6.5;
    return '<g>' +
      stroke('M ' + n(x1) + ' ' + n(y1) + ' L ' + n(hx) + ' ' + n(hy), sw || 4, colour || 'currentColor') +
      '<path d="M ' + n(x2) + ' ' + n(y2) + ' L ' + n(hx + px) + ' ' + n(hy + py) +
        ' L ' + n(hx - px) + ' ' + n(hy - py) + ' Z" fill="' + (colour || 'currentColor') + '"/>' +
      (label ? txt((x1 + x2) / 2 + px * 1.9, (y1 + y2) / 2 + py * 1.9 + 4, label, 11, colour || C.force) : '') +
      '</g>';
  }

  /* A label that starts hidden and lands only after the picture has made the
     point. This is the framework's whole pedagogy in one helper.

     x and y are a REQUEST, not a command: the pill is clamped to stay inside
     the 400x300 frame. An author placing a long label near the right edge gets
     it nudged back rather than clipped, and the leader line still points at
     whatever it was pointing at — so nobody has to count characters to work
     out where a label will fit. */
  function label(name, x, y, text, colour, lx, ly) {
    var w = Math.max(56, text.length * 7.4 + 16);
    x = Math.max(4, Math.min(x, 400 - w - 4));
    y = Math.max(5, Math.min(y, 300 - 24));
    return '<g data-label="' + name + '">' +
      (lx != null ? stroke('M ' + n(lx) + ' ' + n(ly) + ' L ' + n(x + w / 2) + ' ' + n(y + 9), 2, colour || C.ink) : '') +
      '<rect x="' + n(x) + '" y="' + n(y - 1) + '" width="' + n(w) + '" height="20" rx="7" fill="' +
        (colour || C.ink) + '" opacity=".95"/>' +
      txt(x + w / 2, y + 13.5, text, 11, C.white) +
      '</g>';
  }

  /* a scatter of particles, addressable as one layer.  cols x rows in a box. */
  function particles(x, y, w, h, cols, rows, r, colour, jitter) {
    var out = '', i, j, jx, jy;
    for (j = 0; j < rows; j++) {
      for (i = 0; i < cols; i++) {
        jx = jitter ? ((i * 37 + j * 71) % 11) - 5 : 0;
        jy = jitter ? ((i * 53 + j * 29) % 11) - 5 : 0;
        out += '<circle cx="' + n(x + (i + .5) * (w / cols) + jx) + '" cy="' + n(y + (j + .5) * (h / rows) + jy) +
          '" r="' + n(r || 5) + '" fill="' + (colour || 'currentColor') + '" stroke="' + C.ink + '" stroke-width="1"/>';
      }
    }
    return out;
  }

  /* wavy line — waves, heat, sound, light */
  function wave(x1, y, x2, amp, cycles, sw, colour) {
    var d = 'M ' + n(x1) + ' ' + n(y), step = (x2 - x1) / (cycles * 2), i, up = -1;
    for (i = 0; i < cycles * 2; i++) {
      d += ' q ' + n(step / 2) + ' ' + n(up * amp * 2) + ' ' + n(step) + ' 0';
      up = -up;
    }
    return stroke(d, sw || 3, colour);
  }

  /* ============================================================ public API */

  function register(map) {
    Object.keys(map).forEach(function (k) { A[k] = map[k]; });
  }

  function render(name) {
    var a = A[name];
    if (!a) {
      return '<svg class="g-svg" data-asset="' + name + '" viewBox="0 0 400 300" role="img" aria-label="Missing asset">' +
        '<text x="200" y="150" text-anchor="middle" font-size="15" fill="#dc2626">' +
        'no GROW asset: ' + name + '</text></svg>';
    }
    return '<svg class="g-svg" data-asset="' + name + '" viewBox="0 0 400 300" role="img" aria-label="' + (a.alt || a.title || name) +
      '" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,Segoe UI,sans-serif">' +
      (a.css ? '<style>' + a.css + '</style>' : '') +
      '<g class="g-zoom-layer">' + a.svg() + '</g></svg>';
  }

  global.GrowSVG = {
    /* the kit, exported so subject files and lessons can build their own */
    C: C, g: g, ov: ov, n: n,
    shape: shape, stroke: stroke, dot: dot, circ: circ, rect: rect, txt: txt,
    arrow: arrow, label: label, particles: particles, wave: wave,

    register: register,
    render: render,
    asset:  function (name) { return A[name]; },
    title:  function (name) { return (A[name] && A[name].title) || name; },
    alt:    function (name) { return (A[name] && A[name].alt) || ''; },
    tags:   function (name) { return (A[name] && A[name].tags) || []; },
    script: function (name, which) { return (A[name] && A[name][which || 'teach']) || ''; },
    has:    function (name, which) { return !!(A[name] && A[name][which]); },
    list:   function (tag) {
      var keys = Object.keys(A);
      if (!tag) return keys;
      return keys.filter(function (k) { return (A[k].tags || []).indexOf(tag) >= 0; });
    }
  };
})(typeof window !== 'undefined' ? window : this);
