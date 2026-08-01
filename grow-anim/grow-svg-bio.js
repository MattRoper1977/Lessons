/* ============================================================================
   GROW ANIMATION FRAMEWORK · Phase 2 — BIOLOGY SVG LIBRARY
   ---------------------------------------------------------------------------
   Skeleton, cell, heart, circulation, lungs, digestion, food chain, plant, DNA.

   Biology's problem is the opposite of physics'. Here the structures are real
   and visible — but they are inside something, and they are all happening at
   once. So these assets are built to be taken apart: one system at a time, one
   organ at a time, and the labels last.

   Requires grow-svg.js.
   ========================================================================== */
(function (global) {
  'use strict';
  var S = global.GrowSVG; if (!S) { return; }
  var C = S.C, g = S.g, ov = S.ov, n = S.n;
  var shape = S.shape, stroke = S.stroke, dot = S.dot, circ = S.circ, rect = S.rect;
  var txt = S.txt, arrow = S.arrow, label = S.label, particles = S.particles, wave = S.wave;

  /* one vertebra sitting square across the line of the spine */
  function vert(x, y, w, h, rot) {
    return '<rect x="' + n(x - w / 2) + '" y="' + n(y - h / 2) + '" width="' + w + '" height="' + h +
      '" rx="' + Math.max(2, Math.round(Math.min(w, h) / 3)) +
      '" transform="rotate(' + n(rot || 0) + ' ' + n(x) + ' ' + n(y) + ')"' +
      ' fill="currentColor" stroke="' + C.ink + '" stroke-width="1.1"/>';
  }
  function spineChain(pts, w, h) {
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
  function ribPairs(cx, ys, len) {
    return ys.map(function (y, i) {
      var L = len - Math.abs(i - ys.length / 2) * 2;
      return stroke('M ' + n(cx - 5) + ' ' + n(y) + ' q ' + n(-L) + ' 4 ' + n(-L * 0.86) + ' ' + n(L * 0.5), 3.4) +
             stroke('M ' + n(cx + 5) + ' ' + n(y) + ' q ' + n(L) + ' 4 ' + n(L * 0.86) + ' ' + n(L * 0.5), 3.4);
    }).join('');
  }

  S.register({

  /* ======================================================== SKELETON ==== */
  skeleton: {
    title: 'The human skeleton', tags: ['biology', 'body', 'skeleton'],
    alt: 'A human skeleton: the skull, the chain of vertebrae forming the backbone, the rib cage, the pelvis and the limb bones.',
    svg: function () {
      var sp = [[200, 96], [200, 110], [200, 124], [200, 138], [200, 152], [200, 166], [200, 180]];
      return g('body', C.soft,
          shape('M 200 34 q 44 0 44 44 q 0 30 -14 44 q 34 16 34 62 l -6 66 q -2 34 -18 44 l -8 -2 l 4 -46 l -12 -40 l -12 40 l 4 46 l -8 2 q -16 -10 -18 -44 l -6 -66 q 0 -46 34 -62 q -14 -14 -14 -44 q 0 -44 44 -44 Z', 0) ) +
        g('skull', C.bone,
          shape('M 200 30 q 32 0 32 34 q 0 22 -12 30 l -40 0 q -12 -8 -12 -30 q 0 -34 32 -34 Z') +
          '<circle cx="188" cy="60" r="6" fill="' + C.ink + '"/><circle cx="212" cy="60" r="6" fill="' + C.ink + '"/>' +
          stroke('M 190 82 L 210 82', 2, C.ink)) +
        g('spine', C.bone, spineChain(sp, 15, 12)) +
        g('ribs', C.bone, ribPairs(200, [116, 130, 144, 158], 34)) +
        g('pelvis', C.bone,
          shape('M 168 184 q 32 -8 64 0 q 4 26 -12 32 l -14 -14 l -14 14 q -16 -6 -12 -32 Z')) +
        g('limbs', C.bone,
          stroke('M 178 112 q -30 22 -32 62', 6) + stroke('M 222 112 q 30 22 32 62', 6) +
          stroke('M 186 214 L 180 274', 6) + stroke('M 214 214 L 220 274', 6)) +
        g('nobone', C.force, stroke('M 200 96 L 200 186', 3, C.force)) +

        ov('force', C.force, arrow(140, 150, 176, 150, C.force, 3, 'protects')) +
        ov('energy', C.energy, txt(200, 292, '206 bones · support · protect · move', 11, C.energy)) +

        label('spinelbl', 246, 132, 'BACKBONE', C.bone, 214, 140) +
        label('skulllbl', 250, 44, 'SKULL protects the brain', C.bone, 226, 54) +
        label('riblbl', 24, 122, 'RIBS protect the heart and lungs', C.bone, 168, 132);
    },
    teach:
      'observe: show body           :: A person. From the outside, one solid shape.\n' +
      'think: pause "What is holding all that up?"  :: Say it before I show you.\n' +
      'notice: draw skull + label skulllbl :: The skull. A helmet for the brain.\n' +
      'notice: pop spine            :: Then this — a chain of small bones. Count them as they land.\n' +
      'notice: glow spine + label spinelbl :: Not one bone. Thirty-three. That is why you can bend.\n' +
      'notice: draw ribs + label riblbl :: A cage round the heart and lungs.\n' +
      'notice: draw pelvis, limbs   :: Hips, arms, legs.\n' +
      'explain: fade body + glow spine :: Support. Protection. Movement. All three at once.',
    reveal:
      'show body + draw skull, ribs, pelvis, limbs + pop spine :: The skeleton.\n' +
      'glow spine + label spinelbl :: The backbone down the middle.',
    process:
      'observe: show body, skull, spine, ribs, pelvis, limbs :: The whole skeleton.\n' +
      'notice: glow limbs + overlay force :: Bones cannot move on their own — muscles pull them.\n' +
      'notice: pulse spine        :: Joints are where two bones meet.\n' +
      'explain: overlay energy    :: Support, protection, movement.',
    retrieve:
      'observe: show body      :: The outside.\n' +
      'draw skull              :: What is this bone called?\n' +
      'pop spine               :: And this chain?\n' +
      'draw ribs               :: And this cage?\n' +
      'draw pelvis, limbs      :: Finish it off.\n' +
      'label skulllbl, spinelbl, riblbl :: Skull, backbone, ribs.',
    wrong:
      'show body + show nobone :: A lot of people picture the backbone as ONE long bone.\n' +
      'shake nobone            :: A single rod down your back.',
    right:
      'show body + hide nobone + pop spine :: Watch it build.\n' +
      'glow spine + bounce spine           :: Thirty-three separate bones, stacked.\n' +
      'label spinelbl                      :: Which is exactly why you can bend down and tie your shoe.'
  },

  /* ============================================================ CELL ==== */
  cell: {
    title: 'Animal and plant cell', tags: ['biology', 'cells'],
    alt: 'A cell with its membrane, cytoplasm, nucleus and mitochondria. A plant cell adds a rigid cell wall, a large vacuole and chloroplasts.',
    svg: function () {
      return g('wall', C.plant, rect(46, 56, 308, 188, 10, 3)) +
        g('membrane', C.organ,
          '<rect x="58" y="68" width="284" height="164" rx="34" fill="#fdf2f2" stroke="' + C.organ + '" stroke-width="4"/>') +
        g('cytoplasm', '#fde8e8',
          '<rect x="66" y="76" width="268" height="148" rx="30" fill="#fdf0ee" opacity=".8"/>') +
        g('nucleus', C.particle, circ(198, 150, 34) + circ(198, 150, 12, 1.2)) +
        g('mito', '#c2544d',
          shape('M 108 108 q 26 -12 30 8 q 4 18 -20 20 q -22 2 -10 -28 Z') +
          shape('M 262 194 q 26 -12 30 8 q 4 18 -20 20 q -22 2 -10 -28 Z')) +
        g('vacuole', C.water,
          '<ellipse cx="286" cy="120" rx="42" ry="30" fill="' + C.water + '" opacity=".45" stroke="' + C.water + '" stroke-width="2"/>') +
        g('chloro', C.plant,
          '<ellipse cx="108" cy="188" rx="17" ry="10" fill="' + C.plant + '" stroke="' + C.ink + '" stroke-width="1.2"/>' +
          '<ellipse cx="146" cy="204" rx="17" ry="10" fill="' + C.plant + '" stroke="' + C.ink + '" stroke-width="1.2"/>' +
          '<ellipse cx="248" cy="88" rx="17" ry="10" fill="' + C.plant + '" stroke="' + C.ink + '" stroke-width="1.2"/>') +

        ov('energy', C.energy, arrow(120, 84, 150, 112, C.energy, 3, 'energy released here')) +
        ov('particle', C.particle, arrow(60, 150, 96, 150, C.particle, 3, 'things pass in and out')) +

        label('nuc', 236, 260, 'NUCLEUS — the instructions', C.particle, 214, 182) +
        label('mem', 24, 34, 'MEMBRANE — controls what gets in', C.organ, 118, 70) +
        label('wal', 210, 32, 'CELL WALL — plants only', C.plant, 300, 58) +
        label('chl', 24, 268, 'CHLOROPLASTS — make food from light', C.plant, 116, 198);
    },
    teach:
      'observe: show membrane, cytoplasm :: Every living thing is made of these. A cell.\n' +
      'notice: glow membrane + overlay particle + label mem :: The membrane decides what gets in and out.\n' +
      'observe: show nucleus + zoom nucleus :: In the middle — the nucleus.\n' +
      'explain: unzoom + label nuc      :: The instructions for the whole organism, in every single cell.\n' +
      'notice: show mito + overlay energy :: These release the energy.\n' +
      'think: pause "What would a PLANT cell have that this one does not?" :: Three things. Discuss.\n' +
      'notice: show wall + label wal    :: A rigid wall, so the plant can stand up.\n' +
      'notice: show vacuole             :: A big bag of water in the middle.\n' +
      'label: show chloro + label chl   :: And chloroplasts, to make food out of light.',
    reveal:
      'show membrane, cytoplasm, nucleus, mito :: Animal cell.\n' +
      'show wall, vacuole, chloro              :: Plant cell adds wall, vacuole, chloroplasts.\n' +
      'label nuc, wal, chl                     :: Those three are the difference.',
    retrieve:
      'observe: show membrane, cytoplasm :: A cell.\n' +
      'show nucleus                      :: What is this called?\n' +
      'show mito                         :: And these?\n' +
      'show wall                         :: What does this tell you about the cell?\n' +
      'show vacuole, chloro + label wal, chl :: Plant cell.'
  },

  /* =========================================================== HEART ==== */
  heart: {
    title: 'The heart pumping', tags: ['biology', 'body', 'circulation'],
    alt: 'A heart with four chambers. Blue blood arrives from the body on the right side and is pumped to the lungs; red blood returns from the lungs and is pumped out to the body.',
    svg: function () {
      return g('outline', C.organ,
          shape('M 200 250 q -84 -58 -84 -118 q 0 -44 42 -44 q 30 0 42 30 q 12 -30 42 -30 q 42 0 42 44 q 0 60 -84 118 Z', 2.4)) +
        g('rightside', C.field,
          '<path d="M 200 118 q -50 0 -56 46 q -4 40 56 74 Z" fill="' + C.field + '" opacity=".55"/>') +
        g('leftside', C.acid,
          '<path d="M 200 118 q 50 0 56 46 q 4 40 -56 74 Z" fill="' + C.acid + '" opacity=".55"/>') +
        g('wall', C.ink, stroke('M 200 106 L 200 240', 3, C.ink)) +
        g('valves', C.white,
          stroke('M 158 172 L 186 172 M 214 172 L 242 172', 4, '#ffffff')) +
        g('vessels', C.metal,
          stroke('M 158 96 L 158 46 M 242 96 L 242 46', 9, C.field) +
          stroke('M 178 92 L 178 40 M 222 92 L 222 40', 9, C.acid)) +

        '<g data-part="bluecells" data-overlay="particle" style="color:' + C.field + '">' +
          '<g data-flow-item="">' + dot(158, 60, 6, C.field) + '</g>' +
          '<g data-flow-item="">' + dot(170, 140, 6, C.field) + '</g></g>' +
        '<g data-part="redcells" data-overlay="particle" style="color:' + C.acid + '">' +
          '<g data-flow-item="">' + dot(230, 150, 6, C.acid) + '</g>' +
          '<g data-flow-item="">' + dot(222, 60, 6, C.acid) + '</g></g>' +

        ov('force', C.force, arrow(276, 150, 320, 150, C.force, 4, 'squeeze!')) +
        ov('energy', C.energy, txt(200, 288, 'about 100,000 beats every day', 11, C.energy)) +

        label('rt', 22, 210, 'RIGHT — blood to the LUNGS', C.field, 150, 200) +
        label('lf', 244, 210, 'LEFT — blood to the BODY', C.acid, 240, 200) +
        label('pump', 130, 22, 'The heart is a MUSCLE that squeezes', C.organ);
    },
    teach:
      'observe: show outline + pulse outline :: This is a muscle. It never stops.\n' +
      'explain: label pump            :: Not a shape on a card. A pump made of muscle.\n' +
      'observe: show wall, rightside, leftside :: A wall straight down the middle. Two pumps, not one.\n' +
      'notice: show vessels, bluecells + flow bluecells + glow rightside :: Blue blood comes back from the body, tired.\n' +
      'think: pause "Where does it go next — the body, or the lungs?" :: Decide.\n' +
      'notice: label rt               :: The lungs. To pick up oxygen.\n' +
      'notice: show redcells + flow redcells + glow leftside + label lf :: It comes back red, and THEN goes out to the body.\n' +
      'explain: overlay force + show valves :: Squeeze. Valves shut. One way only.',
    reveal:
      'show outline, wall, rightside, leftside, vessels :: Four chambers, two sides.\n' +
      'show bluecells, redcells + flow bluecells, redcells :: Blue in from the body, red out to the body.\n' +
      'label rt, lf :: Right side to the lungs, left side to the body.',
    process:
      'observe: show outline, wall, rightside, leftside, vessels :: The heart at rest.\n' +
      'notice: show bluecells + flow bluecells :: Blood in from the body.\n' +
      'notice: overlay force + pulse outline   :: Squeeze — out to the lungs.\n' +
      'notice: show redcells + flow redcells   :: Back from the lungs, full of oxygen.\n' +
      'explain: pulse outline + overlay energy :: Squeeze again — out to the whole body. About once a second, for ever.',
    wrong:
      'show outline :: Most people think the heart is one bag that squeezes.\n' +
      'shake outline :: In, then out.',
    right:
      'show outline, wall + glow wall :: There is a solid wall down the middle.\n' +
      'show rightside, leftside + bounce wall :: Two separate pumps, side by side, beating together.\n' +
      'label rt, lf :: One sends blood to the lungs. One sends it everywhere else.'
  },

  /* ==================================================== CIRCULATION ==== */
  circulation: {
    title: 'Blood around the body', tags: ['biology', 'body', 'circulation'],
    alt: 'A simplified body showing the heart, the lungs and the rest of the body, with blood travelling in a double loop: heart to lungs and back, then heart to body and back.',
    svg: function () {
      return g('body', C.soft, shape('M 200 24 q 30 0 30 30 q 0 20 -10 30 q 40 14 40 60 l -6 100 q 0 20 -12 26 l -6 -2 l 4 -60 l -10 -30 l -10 30 l 4 60 l -6 2 q -12 -6 -12 -26 l -6 -100 q 0 -46 40 -60 q -10 -10 -10 -30 q 0 -30 30 -30 Z', 0)) +
        g('lungs', '#f4b8b8',
          shape('M 176 106 q -22 4 -22 30 q 0 24 20 26 q 8 -26 2 -56 Z') +
          shape('M 224 106 q 22 4 22 30 q 0 24 -20 26 q -8 -26 -2 -56 Z')) +
        g('heart', C.organ, shape('M 200 176 q -18 -14 -18 -26 q 0 -10 9 -10 q 7 0 9 8 q 2 -8 9 -8 q 9 0 9 10 q 0 12 -18 26 Z')) +
        g('vesselsblue', C.field,
          '<path id="toLung" d="M 194 168 q -30 -12 -26 -40" fill="none" stroke="' + C.field + '" stroke-width="5"/>' +
          '<path id="fromBody" d="M 196 186 q -34 30 -30 74" fill="none" stroke="' + C.field + '" stroke-width="5"/>') +
        g('vesselsred', C.acid,
          '<path id="fromLung" d="M 206 168 q 30 -12 26 -40" fill="none" stroke="' + C.acid + '" stroke-width="5"/>' +
          '<path id="toBody" d="M 204 186 q 34 30 30 74" fill="none" stroke="' + C.acid + '" stroke-width="5"/>') +
        g('bloodblue', C.field, dot(0, 0, 6, C.field), ' data-flow-along="#fromBody" class="g-hidden"') +
        g('bloodred', C.acid, dot(0, 0, 6, C.acid), ' data-flow-along="#toBody" class="g-hidden"') +

        ov('particle', C.field, txt(200, 292, 'red blood cells carry the oxygen', 11, C.field)) +
        ov('energy', C.energy, arrow(250, 240, 288, 226, C.energy, 3, 'oxygen delivered')) +

        label('dbl', 20, 34, 'A DOUBLE loop — lungs, then body', C.organ) +
        label('lung', 250, 96, 'Pick up oxygen', '#f4b8b8', 234, 116) +
        label('bod', 246, 264, 'Drop oxygen off', C.acid, 232, 250);
    },
    teach:
      'observe: show body, heart + pulse heart :: One pump, in the middle.\n' +
      'observe: show lungs                     :: Lungs above it.\n' +
      'notice: show vesselsblue + trace vesselsblue :: Blue tubes carry blood that has NO oxygen left.\n' +
      'notice: show bloodblue + flow bloodblue :: Back from the body — used up.\n' +
      'think: pause "Where must it go before it can be used again?" :: Talk to your partner.\n' +
      'notice: show vesselsred, bloodred + flow bloodred + label lung :: To the lungs. It comes back RED.\n' +
      'explain: overlay energy + label bod     :: Then out to every part of you, dropping oxygen off.\n' +
      'label: label dbl + overlay particle     :: Two loops, not one. That is why it is called a double circulation.',
    reveal:
      'show body, heart, lungs, vesselsblue, vesselsred :: Heart, lungs, body.\n' +
      'show bloodblue, bloodred + flow bloodblue, bloodred :: Blue back, red out.\n' +
      'label dbl, lung, bod :: A double loop.',
    process:
      'observe: show body, heart, lungs, vesselsblue, vesselsred :: The system at rest.\n' +
      'notice: show bloodblue + flow bloodblue :: Blood returns with no oxygen.\n' +
      'notice: pulse heart                     :: The heart pushes it to the lungs.\n' +
      'notice: show bloodred + flow bloodred + label lung :: Oxygen loaded on.\n' +
      'explain: overlay energy + label bod     :: And out to every cell in your body.',
    retrieve:
      'observe: show body :: A body.\n' +
      'show heart         :: What is in the middle?\n' +
      'show lungs         :: And above it?\n' +
      'show vesselsblue + flow bloodblue :: What colour is blood with NO oxygen on our diagrams?\n' +
      'show vesselsred + flow bloodred + label dbl :: And with oxygen?'
  },

  /* ========================================================== LUNGS ==== */
  lungs: {
    title: 'Breathing', tags: ['biology', 'body', 'respiration'],
    alt: 'The lungs with the windpipe branching into smaller tubes ending in tiny air sacs, where oxygen passes into the blood and carbon dioxide passes out.',
    svg: function () {
      return g('trachea', C.metal, rect(192, 34, 16, 58, 6) +
          stroke('M 200 92 L 164 118 M 200 92 L 236 118', 8, C.metal)) +
        g('lunga', '#f4b8b8', shape('M 164 112 q -50 8 -50 68 q 0 56 46 62 q 20 -60 12 -130 Z', 2.4)) +
        g('lungb', '#f4b8b8', shape('M 236 112 q 50 8 50 68 q 0 56 -46 62 q -20 -60 -12 -130 Z', 2.4)) +
        g('tubes', C.metal,
          stroke('M 164 118 q -20 22 -24 52 M 164 118 q -6 30 -2 60 M 236 118 q 20 22 24 52 M 236 118 q 6 30 2 60', 3, C.metal)) +
        g('sacs', '#fecaca',
          dot(138, 178, 8, '#fecaca') + dot(160, 186, 8, '#fecaca') + dot(262, 178, 8, '#fecaca') + dot(240, 186, 8, '#fecaca')) +
        g('diaphragm', C.organ, stroke('M 108 250 q 92 -22 184 0', 6, C.organ)) +

        ov('particle', C.field,
          arrow(138, 210, 172, 226, C.field, 3, 'O₂ in') +
          arrow(262, 226, 228, 210, '#7c3aed', 3, 'CO₂ out')) +
        ov('air', C.soft, arrow(200, 12, 200, 40, C.soft, 4, 'air in')) +
        ov('force', C.force, arrow(200, 274, 200, 254, C.force, 4, 'diaphragm pulls DOWN')) +

        label('gas', 16, 292, 'Gas exchange happens in the tiny air sacs', C.field) +
        label('big', 226, 60, 'Millions of sacs = a huge surface', '#f4b8b8');
    },
    teach:
      'observe: show trachea, lunga, lungb :: Two lungs and the tube down to them.\n' +
      'notice: overlay air + show tubes    :: Air comes in and splits again and again.\n' +
      'notice: zoom sacs + show sacs       :: Right at the end — tiny air sacs. Millions of them.\n' +
      'explain: unzoom + label big         :: Which gives an enormous surface inside your chest.\n' +
      'think: pause "What has to get from the air into your blood?" :: Say it.\n' +
      'notice: overlay particle + label gas :: Oxygen in, carbon dioxide out. Right there at the sacs.\n' +
      'explain: show diaphragm + overlay force :: And this muscle underneath does the pulling.',
    reveal:
      'show trachea, lunga, lungb, tubes, sacs :: Lungs and air sacs.\n' +
      'overlay air, particle                   :: Oxygen in, carbon dioxide out.\n' +
      'label gas, big                          :: Gas exchange, over a huge surface.',
    process:
      'observe: show trachea, lunga, lungb, diaphragm :: Resting.\n' +
      'notice: overlay force                          :: The diaphragm pulls down.\n' +
      'notice: overlay air + show tubes               :: Air rushes in to fill the space.\n' +
      'notice: show sacs + overlay particle           :: At the sacs, oxygen crosses into the blood.\n' +
      'explain: label gas                             :: And carbon dioxide crosses out. Then you breathe out.'
  },

  /* ====================================================== DIGESTION ==== */
  digestion: {
    title: 'The digestive system', tags: ['biology', 'body', 'digestion'],
    alt: 'The digestive system: mouth, gullet, stomach, small intestine and large intestine, with food travelling all the way through and nutrients passing into the blood.',
    svg: function () {
      return g('body', C.soft, shape('M 200 16 q 34 0 34 32 q 0 22 -12 32 q 44 16 44 66 l -8 120 l -116 0 l -8 -120 q 0 -50 44 -66 q -12 -10 -12 -32 q 0 -32 34 -32 Z', 0)) +
        g('mouth', C.organ, shape('M 186 52 q 14 10 28 0 q -4 12 -14 12 q -10 0 -14 -12 Z')) +
        g('gullet', C.organ, rect(193, 68, 14, 52, 6)) +
        g('stomach', C.organ, shape('M 207 120 q 44 4 44 40 q 0 30 -34 32 q -30 2 -30 -22 q 0 -18 12 -22 q -12 -14 8 -28 Z', 2.4)) +
        g('smallint', '#e8a87c',
          '<path id="gut" d="M 190 190 q -40 6 -34 30 q 6 22 44 14 q 40 -8 46 14 q 6 22 -34 26 q -38 4 -38 20" fill="none" stroke="#e8a87c" stroke-width="12" stroke-linecap="round"/>') +
        g('largeint', '#c98a4b',
          stroke('M 136 264 q -14 -70 6 -100 q 20 -30 118 -22 q 20 44 4 122', 13, '#c98a4b')) +
        g('food', '#7c3aed', dot(0, 0, 7, '#7c3aed'), ' data-flow-along="#gut" class="g-hidden"') +

        ov('particle', C.field,
          arrow(258, 214, 296, 200, C.field, 3, 'nutrients into the blood')) +
        ov('energy', C.energy, txt(200, 292, 'about 7 metres, coiled up inside you', 11, C.energy)) +

        label('brk', 254, 132, 'STOMACH — breaks food down', C.organ, 240, 148) +
        label('abs', 20, 214, 'SMALL INTESTINE — absorbs the goodness', '#e8a87c', 176, 210) +
        label('wtr', 20, 264, 'LARGE INTESTINE — takes the water back', '#c98a4b', 140, 254);
    },
    teach:
      'observe: show body, mouth      :: It starts here. Chewing is already digestion.\n' +
      'notice: show gullet + trace gullet :: Down the gullet. Muscles squeeze it along — it is not falling.\n' +
      'observe: show stomach + pulse stomach + label brk :: The stomach churns it and adds acid.\n' +
      'think: pause "Where does the goodness actually get INTO you?" :: Predict.\n' +
      'notice: show smallint + show food + flow food :: Here. Seven metres of small intestine.\n' +
      'explain: overlay particle + label abs :: Nutrients pass through the wall into your blood.\n' +
      'notice: show largeint + label wtr :: And the last part takes the water back.',
    reveal:
      'show body, mouth, gullet, stomach, smallint, largeint :: Mouth to end.\n' +
      'show food + flow food + overlay particle :: Food through, nutrients out into the blood.\n' +
      'label brk, abs, wtr :: Break down, absorb, take back the water.',
    process:
      'observe: show body, mouth :: Food goes in.\n' +
      'notice: show gullet + trace gullet :: Squeezed down the gullet.\n' +
      'notice: show stomach + pulse stomach :: Churned with acid until it is a soup.\n' +
      'notice: show smallint, food + flow food :: Through seven metres of small intestine.\n' +
      'explain: overlay particle :: Nutrients cross into the blood.\n' +
      'label: show largeint + label wtr :: Water taken back. The rest leaves.',
    retrieve:
      'observe: show body, mouth :: Start at the top.\n' +
      'show gullet   :: What is this tube called?\n' +
      'show stomach  :: And this?\n' +
      'show smallint :: This is the longest part — name it.\n' +
      'show largeint + label brk, abs, wtr :: And the last part.',
    wrong:
      'show body, gullet, stomach :: Most people think food FALLS down to your stomach.\n' +
      'shake gullet               :: Straight down, like a drainpipe.',
    right:
      'show body, gullet + trace gullet :: Muscles squeeze in a wave behind the food.\n' +
      'show stomach + bounce gullet     :: Which is why an astronaut can eat upside down.\n' +
      'label brk                        :: It is pushed, not dropped.'
  },

  /* ===================================================== FOOD CHAIN ==== */
  foodchain: {
    title: 'Food chain', tags: ['biology', 'ecology'],
    alt: 'A food chain: the Sun, then grass, then a rabbit, then a fox, with arrows showing which way the energy travels.',
    svg: function () {
      function creature(x, y, body, colour, legs) {
        return shape(body) + (legs || '');
      }
      return g('sun', C.energy, circ(46, 62, 22) + stroke('M 46 30 L 46 18 M 76 62 L 90 62 M 68 40 L 78 30', 3, C.energy)) +
        g('grass', C.plant,
          stroke('M 116 214 q 4 -40 -6 -56 M 126 214 q 0 -46 8 -60 M 136 214 q 6 -38 20 -50', 5, C.plant) +
          stroke('M 100 214 L 160 214', 4, C.plant)) +
        g('rabbit', '#a8a29e',
          creature(0, 0, 'M 214 214 q -22 0 -22 -22 q 0 -22 24 -22 q 22 0 24 20 q 12 -30 16 -2 q 2 20 -10 26 Z') +
          dot(240, 182, 3, C.ink)) +
        g('fox', '#c2724a',
          creature(0, 0, 'M 318 214 q -26 0 -26 -26 q 0 -24 28 -24 q 16 0 22 12 l 16 -14 l -2 20 q 8 8 4 20 q -4 12 -20 12 Z') +
          dot(346, 186, 3, C.ink)) +
        g('a1', C.ink, S.arrow(168, 196, 190, 196, C.ink, 4)) +
        g('a2', C.ink, S.arrow(266, 196, 288, 196, C.ink, 4)) +
        g('a0', C.energy, S.arrow(74, 92, 112, 152, C.energy, 4)) +

        ov('energy', C.energy,
          txt(200, 288, 'the arrows show which way the ENERGY goes', 11, C.energy)) +

        label('prod', 82, 246, 'PRODUCER — makes its own food', C.plant) +
        label('prey', 182, 130, 'PRIMARY CONSUMER', '#a8a29e', 216, 168) +
        label('pred', 268, 130, 'PREDATOR', '#c2724a', 320, 164) +
        label('start', 18, 24, 'All the energy starts at the Sun', C.energy);
    },
    teach:
      'observe: show sun + glow sun   :: Every food chain starts in the same place.\n' +
      'explain: label start           :: Not with an animal. With the Sun.\n' +
      'notice: show grass + show a0 + label prod :: Grass catches that light and makes its own food.\n' +
      'think: pause "What eats the grass?"  :: Say it before I click.\n' +
      'notice: show rabbit, a1 + label prey :: The rabbit. It cannot make food — it has to eat.\n' +
      'think: pause "And what eats the rabbit?" :: Predict.\n' +
      'notice: show fox, a2 + label pred :: The fox.\n' +
      'explain: trace a0, a1, a2 + overlay energy :: The arrows point the way the ENERGY travels. Not "who eats who".',
    reveal:
      'show sun, grass, rabbit, fox, a0, a1, a2 :: Sun, grass, rabbit, fox.\n' +
      'trace a0, a1, a2 + overlay energy        :: The arrows follow the energy.\n' +
      'label prod, prey, pred                   :: Producer, consumer, predator.',
    retrieve:
      'observe: show sun    :: Where does every food chain begin?\n' +
      'show grass, a0       :: What comes first — and what is it called?\n' +
      'show rabbit, a1      :: Next?\n' +
      'show fox, a2         :: And next?\n' +
      'label prod, prey, pred :: Producer, primary consumer, predator.',
    wrong:
      'show sun, grass, rabbit, fox, a1, a2 :: Most people read the arrows as "eats".\n' +
      'shake a1                             :: Rabbit → eats → grass. Backwards.',
    right:
      'show sun, grass, rabbit, fox, a0, a1, a2 :: Follow the arrow, not the animal.\n' +
      'trace a0, a1, a2 + overlay energy        :: Grass → rabbit means the ENERGY goes that way.\n' +
      'bounce a1 + label start                  :: The arrow always points at the eater.'
  },

  /* ========================================================== PLANT ==== */
  plant: {
    title: 'Photosynthesis', tags: ['biology', 'plants'],
    alt: 'A plant with roots, stem and leaves. Light comes in from the Sun, water comes up from the roots, carbon dioxide comes in at the leaf, and the plant makes glucose and gives off oxygen.',
    svg: function () {
      return g('soil', '#8b6f47', rect(20, 224, 360, 60, 0) ) +
        g('roots', '#a1887f', stroke('M 200 226 L 200 262 M 200 240 q -30 8 -44 26 M 200 244 q 30 10 46 24', 4, '#a1887f')) +
        g('stem', C.plant, rect(194, 120, 12, 106, 5)) +
        g('leaves', C.plant,
          shape('M 194 148 q -56 -24 -70 12 q 34 26 70 -12 Z') +
          shape('M 206 176 q 56 -24 70 12 q -34 26 -70 -12 Z')) +
        g('sun', C.energy, circ(50, 54, 20) + stroke('M 50 26 L 50 16 M 78 54 L 90 54', 3, C.energy)) +

        g('lightin', C.energy, S.arrow(72, 74, 130, 138, C.energy, 3.4, 'LIGHT')) +
        g('waterin', C.water, S.arrow(200, 262, 200, 200, C.water, 3.4, 'WATER')) +
        g('co2in', C.particle, S.arrow(316, 200, 268, 188, C.particle, 3.4, 'CO₂')) +
        g('o2out', C.neutral, S.arrow(122, 168, 74, 190, C.neutral, 3.4, 'O₂')) +
        g('glucose', '#d97706', dot(200, 160, 9, '#d97706') + txt(200, 164, 'G', 9, '#fff')) +

        ov('energy', C.energy, txt(200, 292, 'light energy → stored as food', 11, C.energy)) +
        ov('particle', C.particle, txt(200, 22, 'carbon dioxide + water → glucose + oxygen', 11, C.particle)) +

        label('leaf', 236, 122, 'The LEAF is the factory', C.plant, 238, 176) +
        label('root', 226, 262, 'ROOTS take up water', '#a1887f', 214, 250);
    },
    teach:
      'observe: show soil, roots, stem, leaves :: A plant. It has never eaten anything.\n' +
      'think: pause "So where does a plant get its food from?" :: This one catches people out.\n' +
      'notice: show sun, lightin :: Light. That is the energy.\n' +
      'notice: show waterin + label root :: Water, pulled up from the roots.\n' +
      'notice: show co2in       :: And carbon dioxide, straight out of the air.\n' +
      'explain: show glucose + bounce glucose + label leaf :: The leaf puts them together and MAKES food.\n' +
      'notice: show o2out       :: And gives off oxygen as a leftover — which is the air you are breathing.\n' +
      'label: overlay particle, energy :: Carbon dioxide and water in. Glucose and oxygen out.',
    reveal:
      'show soil, roots, stem, leaves, sun :: A plant in the light.\n' +
      'show lightin, waterin, co2in        :: Light, water, carbon dioxide in.\n' +
      'show glucose, o2out + overlay particle :: Glucose made, oxygen given off.\n' +
      'label leaf, root                    :: Photosynthesis.',
    process:
      'observe: show soil, roots, stem, leaves, sun :: The plant in daylight.\n' +
      'notice: show lightin + glow leaves           :: Light lands on the leaf.\n' +
      'notice: show waterin + trace roots           :: Water arrives from the roots.\n' +
      'notice: show co2in                           :: Carbon dioxide arrives from the air.\n' +
      'explain: show glucose + bounce glucose       :: Glucose is made. That is the plant\'s food.\n' +
      'label: show o2out + overlay energy           :: Oxygen leaves. Every breath you take came from this.',
    wrong:
      'show soil, roots, stem, leaves :: Most people say a plant gets its food from the soil.\n' +
      'shake roots                    :: Sucked up through the roots, like a drink.',
    right:
      'show soil, roots, stem, leaves, sun, waterin :: Water, yes — the roots really do that.\n' +
      'show lightin, co2in + glow leaves            :: But the FOOD is made in the leaf, out of air and light.\n' +
      'show glucose + bounce glucose + label leaf   :: A tree is mostly built out of thin air. Genuinely.'
  },

  /* ============================================================ DNA ==== */
  dna: {
    title: 'DNA', tags: ['biology', 'genetics'],
    alt: 'A DNA double helix: two twisted strands joined by pairs of bases, like a twisted ladder.',
    svg: function () {
      var rungs = '', i, y, w;
      for (i = 0; i < 11; i++) {
        y = 44 + i * 20;
        w = Math.abs(Math.sin(i * 0.55)) * 52 + 8;
        rungs += '<g data-part="r' + i + '">' +
          '<line x1="' + n(200 - w) + '" y1="' + n(y) + '" x2="' + n(200 + w) + '" y2="' + n(y) +
          '" stroke="' + (i % 2 ? C.particle : C.energy) + '" stroke-width="6" stroke-linecap="round"/></g>';
      }
      return g('strand1', C.field,
          stroke('M 148 40 q 104 30 0 60 q -104 30 0 60 q 104 30 0 60 q -104 30 0 40', 6, C.field)) +
        g('strand2', C.acid,
          stroke('M 252 40 q -104 30 0 60 q 104 30 0 60 q -104 30 0 60 q 104 30 0 40', 6, C.acid)) +
        g('rungs', C.particle, rungs) +
        ov('particle', C.particle, txt(200, 292, 'the order of the pairs IS the instruction', 11, C.particle)) +
        label('lad', 12, 24, 'A twisted ladder — the double helix', C.field) +
        label('pair', 268, 150, 'Bases always pair up', C.particle, 250, 144);
    },
    teach:
      'observe: show strand1 + draw strand1 :: One long strand.\n' +
      'observe: show strand2 + draw strand2 :: And a second one, twisted round it.\n' +
      'explain: label lad :: A twisted ladder. The double helix.\n' +
      'notice: pop rungs + label pair :: The rungs are pairs of bases, joining the two sides.\n' +
      'think: pause "Where is the actual information?" :: Not the shape. Where?\n' +
      'explain: glow rungs + overlay particle :: In the ORDER of those pairs. That order is the instruction.',
    reveal:
      'show strand1, strand2 + draw strand1, strand2 :: Two strands, twisted.\n' +
      'pop rungs + label lad, pair :: Joined by paired bases.'
  }

  });
})(typeof window !== 'undefined' ? window : this);
