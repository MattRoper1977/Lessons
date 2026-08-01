/* ============================================================================
   BUILD Animation Framework — Biology SVG asset library
   ---------------------------------------------------------------------------
   Every asset is LAYERED. Each layer is a <g data-part="name"> so the animation
   engine can draw, glow, recolour, fade or zoom any single structure on its own.

   Standard part names (use these so scripts are portable between assets):
     body     the outside shape / silhouette      (soft grey)
     skull    the head bones                       (bone blue)
     spine    the chain of vertebrae               (bone blue)  <- the teaching point
     ribs     the rib pairs                        (bone blue)
     pelvis   the hip bones                        (bone blue)
     limbs    arm / leg / wing bones               (bone blue)
     shell    hard case on the OUTSIDE             (shell orange)
     legs     jointed outside legs                 (shell orange)
     soft     soft body with no hard parts         (soft grey)
     nobone   dashed line where a backbone would be — deliberately empty

   Each asset also carries:
     kind    'vertebrate' | 'invertebrate'
     teach   a full I-Do teaching sequence  (referenced as @teach)
     reveal  a short We-Do answer sequence  (referenced as @reveal)

   Usage:  BioSVG.render('fish')            -> '<svg …>…</svg>'
           BioSVG.script('fish','teach')    -> the teaching script string
           BioSVG.list()                    -> ['bird','crab', …]
   ========================================================================== */
(function (global) {
  'use strict';

  var BONE  = '#4E7A9B';   /* brand blue  — bone / internal skeleton        */
  var SHELL = '#C9803B';   /* brand amber — hard case on the outside        */
  var SOFT  = '#94a3b8';   /* soft grey   — body outline, soft bodies       */
  var INK   = '#1f2937';   /* outline ink — keeps shapes legible on glow    */

  /* ---------- small builders ------------------------------------------- */

  function g(part, colour, inner) {
    return '<g data-part="' + part + '" style="color:' + colour + '">' + inner + '</g>';
  }

  function n(v) { return (Math.round(v * 10) / 10).toString(); }

  /* one vertebra: a block sitting square across the line of the spine */
  function vert(x, y, w, h, rot) {
    return '<rect x="' + n(x - w / 2) + '" y="' + n(y - h / 2) + '" width="' + w +
      '" height="' + h + '" rx="' + Math.max(2, Math.round(Math.min(w, h) / 3)) +
      '" transform="rotate(' + n(rot || 0) + ' ' + n(x) + ' ' + n(y) + ')"' +
      ' fill="currentColor" stroke="' + INK + '" stroke-width="1.1"/>';
  }

  /* a chain of vertebrae following a list of points */
  function spine(pts, w, h) {
    var out = '', i, p, a, b, rot;
    for (i = 0; i < pts.length; i++) {
      p = pts[i];
      a = pts[Math.max(0, i - 1)];
      b = pts[Math.min(pts.length - 1, i + 1)];
      rot = Math.atan2(b[1] - a[1], b[0] - a[0]) * 180 / Math.PI;
      out += vert(p[0], p[1], w || 13, h || 20, rot);
    }
    return out;
  }

  /* rib pairs hanging off a line of points. side: 0 both, 1 one side, -1 other */
  function ribs(pts, len, every, side, from, to) {
    var out = '', i;
    from = from == null ? 1 : from;
    to = to == null ? pts.length - 1 : to;
    for (i = from; i < to; i += (every || 1)) {
      var p = pts[i], a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)];
      var th = Math.atan2(b[1] - a[1], b[0] - a[0]);
      [1, -1].forEach(function (sg) {
        if (side === 1 && sg < 0) return;
        if (side === -1 && sg > 0) return;
        var nx = Math.cos(th + sg * Math.PI / 2), ny = Math.sin(th + sg * Math.PI / 2);
        var tx = Math.cos(th), ty = Math.sin(th);
        var x0 = p[0] + nx * 6, y0 = p[1] + ny * 6;
        var x1 = p[0] + nx * len + tx * len * 0.42, y1 = p[1] + ny * len + ty * len * 0.42;
        var cx = p[0] + nx * len * 0.72, cy = p[1] + ny * len * 0.72;
        out += path('M ' + n(x0) + ' ' + n(y0) + ' Q ' + n(cx) + ' ' + n(cy) + ' ' + n(x1) + ' ' + n(y1), 3);
      });
    }
    return out;
  }

  function path(d, w, cap) {
    return '<path d="' + d + '" fill="none" stroke="currentColor" stroke-width="' + (w || 3) +
      '" stroke-linecap="' + (cap || 'round') + '" stroke-linejoin="round" pathLength="1"/>';
  }

  function shape(d, opacity) {
    return '<path d="' + d + '" fill="currentColor" fill-opacity="' + (opacity == null ? 0.28 : opacity) +
      '" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round" pathLength="1"/>';
  }

  function stroke(d, w) {
    return '<path d="' + d + '" fill="none" stroke="currentColor" stroke-width="' + w +
      '" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/>';
  }

  function ell(cx, cy, rx, ry, opacity) {
    return '<ellipse cx="' + n(cx) + '" cy="' + n(cy) + '" rx="' + n(rx) + '" ry="' + n(ry) +
      '" fill="currentColor" fill-opacity="' + (opacity == null ? 0.28 : opacity) +
      '" stroke="currentColor" stroke-width="2.6"/>';
  }

  function dot(cx, cy, r) {
    return '<circle cx="' + n(cx) + '" cy="' + n(cy) + '" r="' + n(r) + '" fill="' + INK + '"/>';
  }

  /* a pointer label: rounded chip + dotted leader line back to the structure */
  function label(key, x, y, text, colour, ax, ay) {
    var w = Math.max(96, text.length * 10.6 + 26);
    var leader = '';
    if (ax != null) {
      var lx = (ax < x) ? x : x + w;
      leader = '<path class="ba-leader" d="M ' + n(ax) + ' ' + n(ay) + ' L ' + n(lx) + ' ' + n(y + 15) +
        '" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="5 5"/>' +
        '<circle cx="' + n(ax) + '" cy="' + n(ay) + '" r="4.5" fill="currentColor"/>';
    }
    return '<g class="ba-label" data-label="' + key + '" style="color:' + colour + '">' + leader +
      '<rect x="' + n(x) + '" y="' + n(y) + '" width="' + n(w) + '" height="30" rx="9" fill="#ffffff" stroke="currentColor" stroke-width="2.4"/>' +
      '<text x="' + n(x + w / 2) + '" y="' + n(y + 20.5) + '" text-anchor="middle" font-size="15.5" font-weight="800" fill="currentColor" font-family="system-ui,sans-serif">' + text + '</text></g>';
  }

  /* the deliberately-empty midline for invertebrates */
  function nobone(x1, y1, x2, y2) {
    return g('nobone', '#dc2626',
      '<path d="M ' + n(x1) + ' ' + n(y1) + ' L ' + n(x2) + ' ' + n(y2) +
      '" fill="none" stroke="currentColor" stroke-width="3.6" stroke-dasharray="9 7" stroke-linecap="round"/>' +
      '<circle cx="' + n((x1 + x2) / 2) + '" cy="' + n((y1 + y2) / 2) + '" r="17" fill="none" stroke="currentColor" stroke-width="2.4" stroke-dasharray="4 5"/>' +
      '<text x="200" y="292" text-anchor="middle" font-size="16" font-weight="800" fill="currentColor" font-family="system-ui,sans-serif">nothing down the middle</text>');
  }

  /* sample a parametric curve into a point list */
  function curve(f, count) {
    var a = [], i;
    for (i = 0; i < count; i++) a.push(f(count === 1 ? 0 : i / (count - 1)));
    return a;
  }

  function poly(pts) {
    return 'M ' + pts.map(function (p) { return n(p[0]) + ' ' + n(p[1]); }).join(' L ');
  }

  /* =========================================================================
     ASSETS
     ====================================================================== */

  var A = {};

  /* ---------------------------------------------------------------- FISH */
  A.fish = {
    title: 'Fish', kind: 'vertebrate',
    alt: 'A fish. Inside it, a skull, curved ribs and a line of small bones down the middle of its back.',
    svg: function () {
      var sp = curve(function (t) { return [128 + t * 172, 150]; }, 10);
      return g('body', SOFT,
          shape('M 72 150 C 96 92 252 84 306 150 C 252 216 96 208 72 150 Z') +
          shape('M 302 150 L 366 106 L 366 194 Z') +
          stroke('M 182 96 Q 210 60 242 100', 4) +
          stroke('M 178 204 Q 202 238 228 202', 4) +
          dot(102, 138, 6)) +
        g('skull', BONE, shape('M 126 150 Q 100 116 74 150 Q 100 184 126 150 Z', 0.35) + dot(96, 142, 5)) +
        g('ribs', BONE, ribs(sp, 40, 1, 0, 1, 9)) +
        g('spine', BONE, spine(sp, 14, 21)) +
        label('spine', 116, 60, 'BACKBONE', BONE, 214, 140) +
        label('kind', 246, 244, 'VERTEBRATE', BONE, 268, 172);
    },
    teach:
      'show body                          :: A fish. Just the outside shape.\n' +
      'draw skull,ribs                    :: Now look INSIDE. Bones.\n' +
      'pop spine                          :: A line of small bones down the middle. Bump… bump… bump.\n' +
      'glow spine + hi spine              :: Not the ribs. They curve round the side. THIS line.\n' +
      'label spine                        :: That line is the backbone.\n' +
      'only spine                         :: Forget everything else. The backbone is the whole test.\n' +
      'label kind + tick                  :: Backbone inside → vertebrate.',
    reveal:
      'draw skull,ribs                    :: Look inside.\n' +
      'pop spine + glow spine + hi spine  :: There it is — the line down the middle.\n' +
      'tick + label kind                  :: Backbone → VERTEBRATE.'
  };

  /* --------------------------------------------------------------- HUMAN */
  A.human = {
    title: 'Human', kind: 'vertebrate',
    alt: 'A person. Inside them, a skull, a stack of vertebrae, ribs, hips and limb bones.',
    svg: function () {
      var sp = curve(function (t) { return [200, 78 + t * 122]; }, 12);
      return g('body', SOFT,
          '<circle cx="200" cy="46" r="26" fill="currentColor" fill-opacity="0.28" stroke="currentColor" stroke-width="2.6"/>' +
          stroke('M 200 76 L 200 208', 48) + stroke('M 176 102 L 142 162 L 134 212', 18) +
          stroke('M 224 102 L 258 162 L 266 212', 18) + stroke('M 186 206 L 178 290', 22) +
          stroke('M 214 206 L 222 290', 22)) +
        g('skull', BONE, '<circle cx="200" cy="46" r="24" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="2.6"/>' +
          shape('M 182 56 Q 200 76 218 56 Z', 0.35) + dot(190, 44, 4) + dot(210, 44, 4)) +
        g('ribs', BONE, ribs(sp, 42, 1, 0, 1, 7)) +
        g('pelvis', BONE, shape('M 172 208 Q 200 198 228 208 L 236 236 Q 200 252 164 236 Z', 0.32)) +
        g('limbs', BONE, stroke('M 160 96 L 240 96', 4) + path('M 166 98 L 144 158 L 136 210', 4) +
          path('M 234 98 L 256 158 L 264 210', 4) + path('M 182 240 L 176 268 L 172 290', 4.5) +
          path('M 218 240 L 224 268 L 228 290', 4.5)) +
        g('spine', BONE, spine(sp, 14, 22)) +
        label('spine', 246, 96, 'BACKBONE', BONE, 206, 140) +
        label('kind', 36, 246, 'VERTEBRATE', BONE, 190, 210);
    },
    teach:
      'show body                    :: A person. You. Me.\n' +
      'draw skull                   :: Skull — the head bones.\n' +
      'pop spine                    :: Now the line down the middle, one bone at a time.\n' +
      'draw ribs                    :: Ribs come off the sides.\n' +
      'draw pelvis,limbs            :: Hips and limbs.\n' +
      'glow spine + hi spine        :: Same line as the fish. Same place. Down the middle.\n' +
      'label spine + label kind + tick :: Backbone inside → vertebrate. You are one.',
    reveal:
      'draw skull,ribs,pelvis,limbs      :: Look inside.\n' +
      'pop spine + glow spine + hi spine :: The line down the middle.\n' +
      'tick + label kind                 :: Backbone → VERTEBRATE.'
  };

  /* --------------------------------------------------------------- SNAKE */
  A.snake = {
    title: 'Snake', kind: 'vertebrate',
    alt: 'A snake. Inside it, one very long line of small bones with ribs all the way down.',
    svg: function () {
      var f = function (t) { return [64 + t * 268, 150 + 62 * Math.sin(t * Math.PI * 2.1)]; };
      var sp = curve(f, 26), body = curve(f, 60);
      return g('body', SOFT, stroke(poly(body), 44) + dot(72, 132, 5)) +
        g('skull', BONE, shape('M 84 ' + n(f(0)[1]) + ' Q 62 ' + n(f(0)[1] - 16) + ' 52 ' + n(f(0)[1]) + ' Q 62 ' + n(f(0)[1] + 16) + ' 84 ' + n(f(0)[1]) + ' Z', 0.35)) +
        g('ribs', BONE, ribs(sp, 26, 1, 0, 1, 25)) +
        g('spine', BONE, spine(sp, 9, 17)) +
        label('spine', 140, 36, 'BACKBONE', BONE, 176, 96) +
        label('kind', 246, 252, 'VERTEBRATE', BONE, 268, 206);
    },
    teach:
      'show body                    :: A snake. No legs at all.\n' +
      'draw skull,ribs              :: Bones inside — look how many ribs.\n' +
      'pop spine                    :: And the line down the middle, all the way to the tail.\n' +
      'glow spine + hi spine        :: No legs. Still a backbone.\n' +
      'label spine + label kind + tick :: Backbone inside → vertebrate.',
    reveal:
      'draw skull,ribs                   :: Look inside.\n' +
      'pop spine + glow spine + hi spine :: One very long line of bones.\n' +
      'tick + label kind                 :: Backbone → VERTEBRATE.'
  };

  /* ---------------------------------------------------------------- BIRD */
  A.bird = {
    title: 'Bird', kind: 'vertebrate',
    alt: 'A bird. Inside it, a skull, a curved neck of small bones, ribs, hips and wing bones.',
    svg: function () {
      var sp = [[118, 76], [126, 90], [136, 103], [148, 114], [163, 122], [179, 128],
                [196, 128], [212, 126], [228, 125], [244, 124], [260, 124], [276, 125]];
      return g('body', SOFT,
          ell(232, 146, 74, 54) + '<circle cx="116" cy="72" r="27" fill="currentColor" fill-opacity="0.28" stroke="currentColor" stroke-width="2.6"/>' +
          stroke('M 130 92 Q 152 112 176 124', 30) + shape('M 92 70 L 60 78 L 92 88 Z') +
          shape('M 300 132 L 376 106 L 368 158 Z') + stroke('M 236 198 L 240 244', 6) +
          stroke('M 262 198 L 268 244', 6) + stroke('M 226 246 L 254 246', 6) + stroke('M 254 246 L 282 246', 6) +
          dot(108, 66, 5)) +
        g('skull', BONE, shape('M 132 72 Q 116 52 98 72 Q 116 92 132 72 Z', 0.35) + shape('M 98 70 L 74 76 L 98 84 Z', 0.35)) +
        g('ribs', BONE, ribs(sp, 40, 1, 1, 6, 11)) +
        g('pelvis', BONE, shape('M 262 116 Q 288 112 300 126 Q 292 142 264 138 Z', 0.32)) +
        g('limbs', BONE, path('M 206 124 L 258 92 L 320 104', 4.5) + path('M 286 136 L 292 178 L 276 210', 4.5) +
          path('M 276 210 L 300 216', 3.5)) +
        g('spine', BONE, spine(sp, 11, 18)) +
        label('spine', 92, 214, 'BACKBONE', BONE, 172, 128) +
        label('kind', 14, 12, 'VERTEBRATE', BONE, 240, 122);
    },
    teach:
      'show body                    :: A bird.\n' +
      'draw skull                   :: Skull.\n' +
      'pop spine                    :: Bones down the neck AND along the back — one line.\n' +
      'draw ribs,pelvis,limbs       :: Ribs, hips, wing bones.\n' +
      'glow spine + hi spine        :: Wings instead of arms — but the same line down the middle.\n' +
      'label spine + label kind + tick :: Backbone inside → vertebrate.',
    reveal:
      'draw skull,ribs,pelvis,limbs      :: Look inside.\n' +
      'pop spine + glow spine + hi spine :: Line down the middle — neck to tail.\n' +
      'tick + label kind                 :: Backbone → VERTEBRATE.'
  };

  /* ----------------------------------------------------------- DOG (MAMMAL) */
  A.dog = {
    title: 'Dog', kind: 'vertebrate',
    alt: 'A dog. Inside it, a skull, a line of small bones along the back, ribs, hips and leg bones.',
    svg: function () {
      var sp = [[112, 122], [128, 114], [146, 108], [166, 106], [188, 105], [210, 104],
                [232, 104], [254, 104], [276, 105], [298, 107]];
      return g('body', SOFT,
          shape('M 132 128 Q 152 84 232 84 Q 302 86 314 124 Q 318 156 300 158 L 152 158 Q 128 156 132 128 Z') +
          '<circle cx="86" cy="126" r="30" fill="currentColor" fill-opacity="0.28" stroke="currentColor" stroke-width="2.6"/>' +
          shape('M 62 128 L 34 134 L 62 144 Z') + stroke('M 108 116 L 132 122', 22) +
          stroke('M 160 156 L 158 218', 16) + stroke('M 194 156 L 196 218', 16) +
          stroke('M 282 156 L 292 200 L 278 220', 16) + stroke('M 246 156 L 254 200 L 242 220', 16) +
          stroke('M 314 118 Q 348 96 356 62', 9) + dot(78, 116, 5)) +
        g('skull', BONE, shape('M 104 124 Q 84 100 62 118 Q 52 132 66 142 Q 88 148 104 124 Z', 0.35) + dot(80, 118, 4.5)) +
        g('ribs', BONE, ribs(sp, 44, 1, 1, 3, 8)) +
        g('pelvis', BONE, shape('M 284 92 Q 312 90 320 108 Q 312 126 286 120 Z', 0.32)) +
        g('limbs', BONE, path('M 168 114 L 162 168 L 158 216', 4.5) + path('M 200 114 L 198 168 L 196 216', 4.5) +
          path('M 296 116 L 300 164 L 280 214', 4.5) + path('M 262 116 L 262 164 L 244 214', 4.5)) +
        g('spine', BONE, spine(sp, 13, 21)) +
        label('spine', 150, 34, 'BACKBONE', BONE, 210, 100) +
        label('kind', 246, 250, 'VERTEBRATE', BONE, 274, 190);
    },
    teach:
      'show body                    :: A dog. Four legs, fur.\n' +
      'draw skull,ribs,pelvis,limbs :: Bones inside.\n' +
      'pop spine                    :: And the line down the middle of the back.\n' +
      'glow spine + hi spine        :: Fur is not the test. THIS is the test.\n' +
      'label spine + label kind + tick :: Backbone inside → vertebrate.',
    reveal:
      'draw skull,ribs,pelvis,limbs      :: Look inside.\n' +
      'pop spine + glow spine + hi spine :: The line down the back.\n' +
      'tick + label kind                 :: Backbone → VERTEBRATE.'
  };

  /* ---------------------------------------------------------------- FROG */
  A.frog = {
    title: 'Frog', kind: 'vertebrate',
    alt: 'A frog. Inside it, a wide skull, a short line of small bones, hips and long back leg bones.',
    svg: function () {
      var sp = curve(function (t) { return [200, 108 + t * 58]; }, 6);
      return g('body', SOFT,
          shape('M 200 72 Q 262 72 268 118 Q 302 132 302 162 Q 302 210 200 214 Q 98 210 98 162 Q 98 132 132 118 Q 138 72 200 72 Z') +
          '<circle cx="172" cy="82" r="15" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="2.4"/>' +
          '<circle cx="228" cy="82" r="15" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="2.4"/>' +
          stroke('M 118 190 Q 74 216 96 250 Q 110 268 84 274', 15) +
          stroke('M 282 190 Q 326 216 304 250 Q 290 268 316 274', 15) +
          stroke('M 140 140 Q 112 172 122 196', 11) + stroke('M 260 140 Q 288 172 278 196', 11) +
          dot(172, 82, 5) + dot(228, 82, 5)) +
        g('skull', BONE, shape('M 200 78 Q 246 78 250 104 Q 226 118 200 118 Q 174 118 150 104 Q 154 78 200 78 Z', 0.35)) +
        g('ribs', BONE, ribs(sp, 26, 1, 0, 1, 5)) +
        g('pelvis', BONE, shape('M 172 168 Q 200 160 228 168 L 234 190 Q 200 202 166 190 Z', 0.32)) +
        g('limbs', BONE, path('M 178 188 L 130 214 L 160 244 L 132 262', 4.5) +
          path('M 222 188 L 270 214 L 240 244 L 268 262', 4.5) +
          path('M 168 124 L 140 164 L 148 192', 4) + path('M 232 124 L 260 164 L 252 192', 4)) +
        g('spine', BONE, spine(sp, 15, 22)) +
        label('spine', 254, 96, 'BACKBONE', BONE, 208, 136) +
        label('kind', 34, 250, 'VERTEBRATE', BONE, 176, 186);
    },
    teach:
      'show body                    :: A frog. Soft, wet skin — no shell anywhere.\n' +
      'draw skull,ribs,pelvis,limbs :: Bones inside.\n' +
      'pop spine                    :: A short line of small bones down the middle.\n' +
      'glow spine + hi spine        :: Short — but still a backbone.\n' +
      'label spine + label kind + tick :: Backbone inside → vertebrate.',
    reveal:
      'draw skull,ribs,pelvis,limbs      :: Look inside.\n' +
      'pop spine + glow spine + hi spine :: Short line of bones down the middle.\n' +
      'tick + label kind                 :: Backbone → VERTEBRATE.'
  };

  /* ---------------------------------------------------------------- CRAB */
  A.crab = {
    title: 'Crab', kind: 'invertebrate',
    alt: 'A crab. A hard case on the outside, jointed legs, and nothing down the middle inside.',
    svg: function () {
      var legs = '';
      [[-1, 0], [1, 0]].forEach(function (s) {
        var d = s[0];
        [0, 1, 2, 3].forEach(function (i) {
          var y = 132 + i * 22, x = 200 + d * 84;
          legs += stroke('M ' + n(x) + ' ' + n(y) + ' L ' + n(x + d * 44) + ' ' + n(y + 12) +
            ' L ' + n(x + d * 62) + ' ' + n(y + 42), 6);
        });
      });
      return g('shell', SHELL,
          ell(200, 148, 92, 62, 0.34) + stroke('M 122 128 Q 200 108 278 128', 3) +
          shape('M 118 112 L 66 78 L 40 96 L 62 116 L 40 128 L 70 132 Z', 0.34) +
          shape('M 282 112 L 334 78 L 360 96 L 338 116 L 360 128 L 330 132 Z', 0.34)) +
        g('legs', SHELL, legs) +
        g('body', SOFT, stroke('M 176 92 L 170 66', 4) + stroke('M 224 92 L 230 66', 4) + dot(170, 62, 7) + dot(230, 62, 7)) +
        nobone(200, 108, 200, 192) +
        label('shell', 10, 18, 'HARD CASE OUTSIDE', SHELL, 244, 112) +
        label('kind', 24, 246, 'INVERTEBRATE', SHELL, 126, 178);
    },
    teach:
      'show body,shell,legs         :: A crab.\n' +
      'glow shell + hi shell        :: Feel where the hard bit is. It is on the OUTSIDE.\n' +
      'label shell                  :: Hard case outside.\n' +
      'show nobone + cross          :: Now look down the middle inside. Nothing. No line of bones.\n' +
      'label kind                   :: No backbone → invertebrate.',
    reveal:
      'show nobone                  :: Look down the middle. Nothing there.\n' +
      'glow shell + hi shell + cross :: The hard bit is OUTSIDE.\n' +
      'label kind                   :: No backbone → INVERTEBRATE.'
  };

  /* -------------------------------------------------------------- SPIDER */
  A.spider = {
    title: 'Spider', kind: 'invertebrate',
    alt: 'A spider. A hard case on the outside, eight jointed legs, and nothing down the middle inside.',
    svg: function () {
      var legs = '';
      [-1, 1].forEach(function (d) {
        [0, 1, 2, 3].forEach(function (i) {
          var y = 122 + i * 18, x = 170 + d * 36;
          var up = (i < 2) ? -1 : 1;
          legs += stroke('M ' + n(x) + ' ' + n(y) + ' L ' + n(x + d * 52) + ' ' + n(y + up * 34) +
            ' L ' + n(x + d * 92) + ' ' + n(y + up * 10), 5.5);
        });
      });
      return g('shell', SHELL, ell(172, 150, 46, 40, 0.34) + ell(262, 152, 62, 52, 0.34) +
          stroke('M 232 128 Q 262 152 232 176', 2.6)) +
        g('legs', SHELL, legs) +
        g('body', SOFT, dot(150, 136, 5) + dot(162, 130, 4) + dot(140, 148, 4)) +
        nobone(214, 152, 312, 152) +
        label('shell', 10, 16, 'HARD CASE OUTSIDE', SHELL, 268, 106) +
        label('kind', 24, 240, 'INVERTEBRATE', SHELL, 150, 180);
    },
    teach:
      'show body,shell,legs          :: A spider. Eight legs.\n' +
      'show nobone                   :: Look down the middle. No line of bones.\n' +
      'cross                         :: No backbone.\n' +
      'glow shell + hi shell + label shell :: The hard bit is the case on the outside.\n' +
      'label kind                    :: No backbone → invertebrate.',
    reveal:
      'show nobone                   :: Look down the middle. Nothing there.\n' +
      'glow shell + hi shell + cross :: Hard case OUTSIDE.\n' +
      'label kind                    :: No backbone → INVERTEBRATE.'
  };

  /* --------------------------------------------------------------- WORM */
  A.worm = {
    title: 'Earthworm', kind: 'invertebrate',
    alt: 'An earthworm. A soft ringed body with no hard parts and nothing down the middle.',
    svg: function () {
      var f = function (t) { return [58 + t * 288, 150 + 40 * Math.sin(t * Math.PI * 1.7)]; };
      var body = curve(f, 50), rings = '';
      curve(f, 16).forEach(function (p, i, arr) {
        var a = arr[Math.max(0, i - 1)], b = arr[Math.min(arr.length - 1, i + 1)];
        var th = Math.atan2(b[1] - a[1], b[0] - a[0]) + Math.PI / 2;
        rings += stroke('M ' + n(p[0] - Math.cos(th) * 16) + ' ' + n(p[1] - Math.sin(th) * 16) +
          ' L ' + n(p[0] + Math.cos(th) * 16) + ' ' + n(p[1] + Math.sin(th) * 16), 2.2);
      });
      return g('soft', SOFT, stroke(poly(body), 36) + rings + dot(66, 138, 5)) +
        nobone(126, 118, 296, 140) +
        label('soft', 10, 20, 'SOFT — NO HARD PARTS', SOFT, 202, 122) +
        label('kind', 24, 244, 'INVERTEBRATE', SHELL, 132, 176);
    },
    teach:
      'show soft                     :: An earthworm. Squeeze it gently — it is soft everywhere.\n' +
      'show nobone                   :: Nothing down the middle.\n' +
      'cross + label soft            :: No hard case outside either. Just rings of muscle.\n' +
      'label kind                    :: No backbone → invertebrate.',
    reveal:
      'show nobone                   :: Look down the middle. Nothing.\n' +
      'cross + label soft            :: Soft all the way through.\n' +
      'label kind                    :: No backbone → INVERTEBRATE.'
  };

  /* --------------------------------------------------------------- SNAIL */
  A.snail = {
    title: 'Snail', kind: 'invertebrate',
    alt: 'A snail. A hard spiral shell on the outside, a soft body, and nothing down the middle.',
    svg: function () {
      var d = 'M 236 128', i;
      for (i = 0; i <= 80; i++) {
        var th = i / 80 * Math.PI * 5.2, r = 8 + i / 80 * 62;
        d += ' L ' + n(236 + Math.cos(th) * r) + ' ' + n(128 + Math.sin(th) * r * 0.92);
      }
      return g('shell', SHELL, '<circle cx="236" cy="128" r="72" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="2.8"/>' +
          '<path d="' + d + '" fill="none" stroke="currentColor" stroke-width="3.4" stroke-linecap="round" pathLength="1"/>') +
        g('soft', SOFT, shape('M 178 178 Q 120 176 96 196 Q 78 212 104 218 L 240 218 Q 268 214 258 190 Z') +
          stroke('M 104 194 L 88 158', 4) + stroke('M 122 190 L 112 156', 4) + dot(88, 152, 6) + dot(112, 150, 6)) +
        nobone(120, 204, 244, 204) +
        label('shell', 10, 16, 'HARD SHELL OUTSIDE', SHELL, 258, 64) +
        label('kind', 24, 240, 'INVERTEBRATE', SHELL, 152, 212);
    },
    teach:
      'show soft,shell               :: A snail.\n' +
      'glow shell + hi shell + label shell :: The hard bit is the shell. On the OUTSIDE.\n' +
      'show nobone + cross           :: Inside the soft part — no line of bones.\n' +
      'label kind                    :: No backbone → invertebrate.',
    reveal:
      'show nobone                   :: No line of bones inside.\n' +
      'glow shell + hi shell + cross :: The hard bit is the shell — OUTSIDE.\n' +
      'label kind                    :: No backbone → INVERTEBRATE.'
  };

  /* ----------------------------------------------------------- JELLYFISH */
  A.jellyfish = {
    title: 'Jellyfish', kind: 'invertebrate',
    alt: 'A jellyfish. A soft bell with trailing tentacles, no hard parts at all.',
    svg: function () {
      var tent = '', i;
      for (i = 0; i < 7; i++) {
        var x = 116 + i * 28;
        tent += stroke('M ' + n(x) + ' 168 q ' + (i % 2 ? 16 : -16) + ' 34 ' + (i % 2 ? -6 : 6) +
          ' 62 q ' + (i % 2 ? -18 : 18) + ' 26 ' + (i % 2 ? 8 : -8) + ' 44', 4.5);
      }
      return g('soft', SOFT, shape('M 92 172 Q 92 66 200 66 Q 308 66 308 172 Q 268 158 238 174 Q 200 156 162 174 Q 132 158 92 172 Z') +
          tent + '<ellipse cx="200" cy="122" rx="44" ry="30" fill="none" stroke="currentColor" stroke-width="2.4" stroke-dasharray="5 5"/>') +
        nobone(200, 84, 200, 168) +
        label('soft', 10, 16, 'NO HARD PARTS AT ALL', SOFT, 200, 96) +
        label('kind', 24, 240, 'INVERTEBRATE', SHELL, 130, 172);
    },
    teach:
      'show soft                     :: A jellyfish. Almost all water.\n' +
      'show nobone                   :: Nothing down the middle.\n' +
      'cross + label soft            :: And no hard case outside either.\n' +
      'label kind                    :: No backbone → invertebrate.',
    reveal:
      'show nobone + cross           :: No bones anywhere.\n' +
      'label soft + label kind       :: No backbone → INVERTEBRATE.'
  };

  /* -------------------------------------------------------------- BEETLE */
  A.beetle = {
    title: 'Beetle', kind: 'invertebrate',
    alt: 'A beetle. A hard wing case on the outside, six jointed legs, and nothing down the middle.',
    svg: function () {
      var legs = '';
      [-1, 1].forEach(function (d) {
        [0, 1, 2].forEach(function (i) {
          var y = 128 + i * 32, x = 200 + d * 50;
          legs += stroke('M ' + n(x) + ' ' + n(y) + ' L ' + n(x + d * 40) + ' ' + n(y + 14) +
            ' L ' + n(x + d * 58) + ' ' + n(y + 44), 5.5);
        });
      });
      return g('shell', SHELL, ell(200, 168, 54, 78, 0.34) + ell(200, 96, 34, 22, 0.34) +
          stroke('M 200 96 L 200 244', 2.8)) +
        g('legs', SHELL, legs) +
        g('body', SOFT, '<circle cx="200" cy="66" r="16" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="2.4"/>' +
          stroke('M 190 56 Q 176 40 160 42', 3.4) + stroke('M 210 56 Q 224 40 240 42', 3.4)) +
        nobone(200, 116, 200, 236) +
        label('shell', 8, 14, 'HARD CASE OUTSIDE', SHELL, 240, 130) +
        label('kind', 22, 240, 'INVERTEBRATE', SHELL, 154, 192);
    },
    teach:
      'show body,shell,legs          :: A beetle.\n' +
      'glow shell + hi shell + label shell :: Tap it and it clicks — hard case on the OUTSIDE.\n' +
      'show nobone + cross           :: Inside, down the middle — nothing.\n' +
      'label kind                    :: No backbone → invertebrate.',
    reveal:
      'show nobone                   :: Nothing down the middle.\n' +
      'glow shell + hi shell + cross :: Hard case OUTSIDE.\n' +
      'label kind                    :: No backbone → INVERTEBRATE.'
  };

  /* ------------------------------------------------------------- OCTOPUS */
  A.octopus = {
    title: 'Octopus', kind: 'invertebrate',
    alt: 'An octopus. A soft bag of a body with eight soft arms and no bones at all.',
    svg: function () {
      var arms = '', i;
      for (i = 0; i < 8; i++) {
        var x = 118 + i * 24, sw = (i % 2 ? 1 : -1);
        arms += stroke('M ' + n(x) + ' 172 q ' + (sw * 22) + ' 36 ' + (sw * 4) + ' 62 q ' +
          (-sw * 26) + ' 26 ' + (-sw * 34) + ' 34', 9);
      }
      return g('soft', SOFT, shape('M 200 58 Q 272 58 272 130 Q 272 172 200 178 Q 128 172 128 130 Q 128 58 200 58 Z') +
          arms + '<circle cx="176" cy="118" r="13" fill="#ffffff" stroke="currentColor" stroke-width="2.4"/>' +
          '<circle cx="224" cy="118" r="13" fill="#ffffff" stroke="currentColor" stroke-width="2.4"/>' +
          dot(176, 118, 6) + dot(224, 118, 6)) +
        nobone(200, 72, 200, 174) +
        label('soft', 10, 16, 'SOFT ALL THROUGH', SOFT, 206, 92) +
        label('kind', 22, 240, 'INVERTEBRATE', SHELL, 136, 152);
    },
    teach:
      'show soft                     :: An octopus. Big, clever, strong.\n' +
      'think                         :: Vertebrate or invertebrate? Say it before I click.\n' +
      'show nobone                   :: Look down the middle. Nothing.\n' +
      'cross + label soft            :: It can squeeze through a gap the size of its eye. Nothing hard to stop it.\n' +
      'label kind                    :: No backbone → invertebrate. Big does NOT mean backbone.',
    reveal:
      'show nobone + cross           :: No line of bones — anywhere.\n' +
      'label soft + label kind       :: No backbone → INVERTEBRATE.'
  };

  /* =========================================================================
     PUBLIC API
     ====================================================================== */

  function render(name, opts) {
    var a = A[name];
    if (!a) return '<svg viewBox="0 0 400 300"><text x="200" y="150" text-anchor="middle" font-size="16" fill="#dc2626">no asset: ' + name + '</text></svg>';
    opts = opts || {};
    return '<svg class="ba-svg" data-asset="' + name + '" viewBox="0 0 400 300" role="img" aria-label="' + a.alt +
      '" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,sans-serif">' +
      (a.css ? '<style>' + a.css + '</style>' : '') +
      '<g class="ba-zoom">' + a.svg() + '</g></svg>';
  }

  /* Other asset files (body-svg.js, food-svg.js, chain-svg.js …) register into
     this same library, so data-ba-asset="plate" works exactly like "fish".
     They build their shapes with the helpers exposed below. */
  function register(assets) {
    Object.keys(assets).forEach(function (k) { A[k] = assets[k]; });
    return Object.keys(assets);
  }

  global.BioSVG = {
    register: register,
    helpers: {
      g: g, n: n, vert: vert, spine: spine, ribs: ribs, path: path, shape: shape,
      stroke: stroke, ell: ell, dot: dot, label: label, nobone: nobone,
      curve: curve, poly: poly,
      BONE: BONE, SHELL: SHELL, SOFT: SOFT, INK: INK
    },
    render: render,
    asset: function (name) { return A[name]; },
    kind: function (name) { return A[name] && A[name].kind; },
    title: function (name) { return (A[name] && A[name].title) || name; },
    script: function (name, which) { return (A[name] && A[name][which || 'teach']) || ''; },
    list: function () { return Object.keys(A); },
    vertebrates: function () { return Object.keys(A).filter(function (k) { return A[k].kind === 'vertebrate'; }); },
    invertebrates: function () { return Object.keys(A).filter(function (k) { return A[k].kind === 'invertebrate'; }); }
  };
})(typeof window !== 'undefined' ? window : this);
