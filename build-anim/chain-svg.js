/* ============================================================================
   BUILD Animation Framework — producers, consumers and food chains
   ---------------------------------------------------------------------------
   Registers into the BioSVG library (see bio-svg.js), so data-ba-asset="foodchain"
   works exactly like data-ba-asset="fish".

   Week 7, "Animals Cannot Make Their Own Food". The whole lesson turns on one
   sentence, and it is a sentence pupils get wrong every single year:

       THE ARROW DOES NOT MEAN "EATS". IT MEANS "IS EATEN BY".

   So the arrow is not decoration here — it is the teaching point. It is its own
   layer, it is traced in the direction of travel, and the label that lands on it
   never says "eats".

   COLOUR LANGUAGE
     plant  #5B9E5B   a producer — it MAKES its own food
     animal #C9803B   a consumer — it has to EAT
     sun    #D8A63B   where the energy comes into the chain
     ink    #1f2937   outlines, so shapes stay legible when a fill changes
   ========================================================================== */
(function (global) {
  'use strict';

  var H = global.BioSVG.helpers;
  var g = H.g, label = H.label, n = H.n;
  var INK = H.INK;

  var PLANT = '#5B9E5B', ANIMAL = '#C9803B', SUN = '#D8A63B', DEAD = '#dc2626';

  /* ---------- small builders ------------------------------------------- */

  function fp(d, op, col) {
    return '<path d="' + d + '" fill="' + (col || 'currentColor') + '" fill-opacity="' +
      (op == null ? 0.34 : op) + '" stroke="' + INK + '" stroke-width="2.6" ' +
      'stroke-linejoin="round" pathLength="1"/>';
  }
  function fe(cx, cy, rx, ry, op, rot) {
    return '<ellipse cx="' + n(cx) + '" cy="' + n(cy) + '" rx="' + n(rx) + '" ry="' + n(ry) +
      '" fill="currentColor" fill-opacity="' + (op == null ? 0.34 : op) + '" stroke="' + INK +
      '" stroke-width="2.6"' + (rot ? ' transform="rotate(' + n(rot) + ' ' + n(cx) + ' ' + n(cy) + ')"' : '') + '/>';
  }
  function ln(d, w, col) {
    return '<path d="' + d + '" fill="none" stroke="' + (col || INK) + '" stroke-width="' + (w || 3) +
      '" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/>';
  }
  function dot(cx, cy, r) {
    return '<circle cx="' + n(cx) + '" cy="' + n(cy) + '" r="' + n(r) + '" fill="' + INK + '"/>';
  }
  function txt(x, y, s, size, fill) {
    return '<text x="' + n(x) + '" y="' + n(y) + '" text-anchor="middle" font-size="' + size +
      '" font-weight="800" fill="' + (fill || INK) + '" font-family="system-ui,sans-serif">' + s + '</text>';
  }

  /* THE ARROW. Its own layer, always, so it can be traced on its own. */
  function arrow(x1, x2, y) {
    return ln('M ' + n(x1) + ' ' + n(y) + ' L ' + n(x2 - 16) + ' ' + n(y), 6, 'currentColor') +
      '<path d="M ' + n(x2 - 18) + ' ' + n(y - 11) + ' L ' + n(x2) + ' ' + n(y) + ' L ' +
      n(x2 - 18) + ' ' + n(y + 11) + ' Z" fill="currentColor" stroke="currentColor" stroke-width="2"/>';
  }

  /* ---------- the organisms, drawn around a centre ---------------------- */

  var SHAPE = {};

  SHAPE.grass = function (cx, cy, s) {
    var o = '', i, blades = [[-26, -30], [-14, -44], [0, -50], [14, -44], [26, -30]];
    for (i = 0; i < blades.length; i++) {
      o += ln('M 0 26 Q ' + n(blades[i][0] * 0.35) + ' 0 ' + n(blades[i][0]) + ' ' + n(blades[i][1]), 7, PLANT);
    }
    return wrap(cx, cy, s, o + ln('M -30 26 L 30 26', 5, '#8a6a4a'));
  };

  SHAPE.tree = function (cx, cy, s) {
    return wrap(cx, cy, s,
      fp('M -9 40 L -6 -6 L 6 -6 L 9 40 Z', 0.5, '#8a6a4a') +
      fp('M 0 -58 C 30 -58 44 -40 40 -22 C 52 -12 44 6 22 6 L -22 6 C -44 6 -52 -12 -40 -22 C -44 -40 -30 -58 0 -58 Z', 0.42, PLANT) +
      ln('M 0 20 L -14 -2 M 0 8 L 14 -12', 3, '#8a6a4a'));
  };

  SHAPE.rabbit = function (cx, cy, s) {
    return wrap(cx, cy, s,
      '<g style="color:' + ANIMAL + '">' +
      fe(6, 12, 30, 22) +                                   /* body        */
      fe(-24, -4, 17, 15) +                                 /* head        */
      fe(-32, -34, 6.5, 22, 0.34, -12) + fe(-16, -36, 6.5, 22, 0.34, 10) + /* ears */
      fe(34, 6, 10, 10) +                                   /* tail        */
      '</g>' + dot(-32, -6, 3.4) +
      ln('M -38 -2 L -30 0 M -38 4 L -30 3', 2) +
      ln('M -2 32 L -2 38 M 16 32 L 16 38', 5, INK));
  };

  SHAPE.fox = function (cx, cy, s) {
    return wrap(cx, cy, s,
      '<g style="color:' + ANIMAL + '">' +
      fp('M 24 4 C 50 8 70 -12 64 -40 C 82 -16 62 18 26 14 Z', 0.42) + /* brush tail, attached */
      fe(4, 10, 34, 16) +                                    /* long low body   */
      fe(-26, 2, 16, 13) +                                   /* head            */
      fp('M -38 4 L -64 11 L -38 18 Z', 0.42) +              /* long snout      */
      fp('M -38 -4 L -30 -26 L -16 -6 Z', 0.42) +            /* broad ear       */
      fp('M -14 -6 L -4 -26 L 4 -4 Z', 0.42) +               /* broad ear       */
      '</g>' +
      '<circle cx="68" cy="-34" r="7" fill="#ffffff" stroke="' + INK + '" stroke-width="2.4"/>' +
      dot(-32, 1, 3.4) +
      ln('M -14 25 L -14 34 M 6 25 L 6 34 M 24 23 L 24 33', 5, INK));
  };

  SHAPE.squirrel = function (cx, cy, s) {
    return wrap(cx, cy, s,
      '<g style="color:' + ANIMAL + '">' +
      fe(-4, 12, 22, 20) +
      fe(-22, -14, 15, 14) +
      fp('M 16 22 C 44 18 50 -14 26 -30 C 40 -8 32 8 12 8 Z', 0.34) +
      fp('M -30 -26 L -24 -38 L -16 -26 Z', 0.34) +
      '</g>' + dot(-28, -16, 3.2));
  };

  SHAPE.sun = function (cx, cy, s) {
    var o = '', i, a;
    for (i = 0; i < 8; i++) {
      a = i * Math.PI / 4;
      o += ln('M ' + n(Math.cos(a) * 30) + ' ' + n(Math.sin(a) * 30) + ' L ' +
        n(Math.cos(a) * 44) + ' ' + n(Math.sin(a) * 44), 5, SUN);
    }
    return wrap(cx, cy, s,
      '<circle cx="0" cy="0" r="26" fill="' + SUN + '" fill-opacity="0.5" stroke="' + INK + '" stroke-width="2.6"/>' + o);
  };

  function wrap(cx, cy, s, inner) {
    return '<g transform="translate(' + n(cx) + ' ' + n(cy) + ') scale(' + (s || 1) + ')">' + inner + '</g>';
  }

  /* sunlight arriving — the reason a chain has to start with a plant */
  function sunbeam(x1, y1, x2, y2) {
    return ln('M ' + n(x1) + ' ' + n(y1) + ' L ' + n(x2) + ' ' + n(y2), 5, SUN) +
      '<path d="M ' + n(x2 - 13) + ' ' + n(y2 - 9) + ' L ' + n(x2) + ' ' + n(y2) + ' L ' +
      n(x2 - 4) + ' ' + n(y2 - 15) + ' Z" fill="' + SUN + '"/>';
  }

  var A = {};

  /* ------------------------------------------------------- THE FOOD CHAIN */
  A.foodchain = {
    title: 'Grass → rabbit → fox',
    alt: 'A food chain. The sun shines on grass; an arrow points from the grass to a ' +
         'rabbit; a second arrow points from the rabbit to a fox. Each arrow means ' +
         '"is eaten by", not "eats".',
    svg: function () {
      return g('sun', SUN, SHAPE.sun(48, 52, 0.8)) +
        g('beam', SUN, sunbeam(56, 88, 64, 142)) +
        g('grass', PLANT, SHAPE.grass(64, 186, 1) + txt(64, 232, 'GRASS', 13)) +
        g('arrow1', INK, arrow(104, 158, 178)) +
        g('rabbit', ANIMAL, SHAPE.rabbit(200, 180, 0.86) + txt(200, 232, 'RABBIT', 13)) +
        g('arrow2', INK, arrow(244, 298, 178)) +
        g('fox', ANIMAL, SHAPE.fox(342, 180, 0.86) + txt(342, 232, 'FOX', 13)) +
        label('eaten',     92,  96, 'IS EATEN BY', INK,    130, 178) +
        label('producer',  10, 256, 'PRODUCER', PLANT,  64, 206) +
        label('consumer1', 150, 256, 'CONSUMERS — THEY EAT', ANIMAL, 270, 206) +
        label('start',     10,  14, 'STARTS WITH A PLANT', PLANT, 64, 150);
    },
    teach:
      'show sun                                  :: Start with the sun. Every chain starts here.\n' +
      'show grass + show beam + glow grass       :: Sunlight lands on the grass. The grass MAKES its own food out of it.\n' +
      'label producer                            :: That is what a producer is. A plant. It makes its own food.\n' +
      'unglow grass + show arrow1 + glow arrow1  :: Now the arrow. Careful here — everybody gets this one wrong.\n' +
      'trace arrow1 + label eaten                :: It does not mean EATS. It means IS EATEN BY. The grass is eaten by…\n' +
      'show rabbit + unglow arrow1               :: …the rabbit. Grass, is eaten by, rabbit.\n' +
      'show arrow2 + trace arrow2 + show fox     :: And the rabbit is eaten by the fox. Same arrow, same meaning.\n' +
      'label consumer1                           :: Neither of those two can make food. They have to eat. Consumers.\n' +
      'only grass,sun + pulse grass              :: Now take the grass away. Watch what is left.\n' +
      'undim + label start                       :: Nothing. No plant, no chain. That is why it always starts with one.',
    revealArrow:
      'show sun,grass,arrow1,rabbit + think      :: Which does the arrow mean? Grass EATS rabbit, or grass IS EATEN BY rabbit?\n' +
      'unthink + glow arrow1 + trace arrow1      :: Follow it. It goes FROM the grass TO the rabbit.\n' +
      'label eaten + tick                        :: IS EATEN BY. The grass is eaten by the rabbit.',
    revealStart:
      'show sun,grass,arrow1,rabbit,arrow2,fox + think :: Does every food chain have to start with a plant?\n' +
      'only grass,sun                            :: Take the plant out and nothing is left to start it.\n' +
      'undim + label start + tick                :: Yes. Only a plant can make its own food, so the chain begins there.',
    reveal:
      'show sun,grass,arrow1,rabbit,arrow2,fox   :: Grass, rabbit, fox.\n' +
      'trace arrow1 + trace arrow2 + label eaten :: Each arrow means IS EATEN BY.\n' +
      'label producer + label consumer1 + tick   :: One producer, two consumers.'
  };

  /* --------------------------------------------------- THE REVERSED CHAIN */
  A.chainwrong = {
    title: 'The chain the wrong way round',
    alt: 'A food chain written backwards: fox, arrow, rabbit, arrow, grass. Read properly ' +
         'the arrows say the fox is eaten by the rabbit and the rabbit is eaten by the grass.',
    svg: function () {
      return g('fox', ANIMAL, SHAPE.fox(60, 172, 0.86) + txt(60, 224, 'FOX', 13)) +
        g('arrow1', INK, arrow(112, 166, 170)) +
        g('rabbit', ANIMAL, SHAPE.rabbit(206, 172, 0.86) + txt(206, 224, 'RABBIT', 13)) +
        g('arrow2', INK, arrow(252, 306, 170)) +
        g('grass', PLANT, SHAPE.grass(344, 178, 1) + txt(344, 224, 'GRASS', 13)) +
        label('read', 10,  14, 'READ IT PROPERLY', INK,   139, 170) +
        label('why',  10, 256, 'GRASS CANNOT EAT', DEAD, 330, 200) +
        label('fix',  10, 256, 'START WITH THE PLANT', PLANT, 344, 200);
    },
    teach:
      'show fox,rabbit,grass,arrow1,arrow2       :: Somebody has written this chain out. Fox, arrow, rabbit, arrow, grass.\n' +
      'glow arrow1 + trace arrow1 + label read   :: Read it the way we learned. The arrow means IS EATEN BY.\n' +
      'shake fox                                 :: So this says the FOX is eaten by the rabbit. Is it?\n' +
      'trace arrow2 + cross + label why          :: And the rabbit is eaten by the grass. Grass does not eat anything.\n' +
      'unlabel why + label fix                   :: Turn it round. It has to start with the plant.',
    reveal:
      'show fox,rabbit,grass,arrow1,arrow2 + think :: Is this chain right or wrong?\n' +
      'unthink + trace arrow1 + trace arrow2 + label read :: Read the arrows properly — IS EATEN BY.\n' +
      'cross + shake fox,rabbit,grass + label why :: Wrong way round. A grass plant cannot eat a rabbit.\n' +
      'unlabel why + label fix                   :: Start with the plant and it works.'
  };

  /* ------------------------------------- PRODUCER OR CONSUMER? one at a time */
  var ORGANISMS = [
    { key: 'oaktree',    shape: 'tree',     title: 'Oak tree', kind: 'producer',
      word: 'AN OAK TREE', s: 1.5, y: 168 },
    { key: 'grassplant', shape: 'grass',    title: 'Grass',    kind: 'producer',
      word: 'GRASS',       s: 1.7, y: 178 },
    { key: 'squirrel',   shape: 'squirrel', title: 'Squirrel', kind: 'consumer',
      word: 'A SQUIRREL',  s: 1.5, y: 168 },
    { key: 'foxanimal',  shape: 'fox',      title: 'Fox',      kind: 'consumer',
      word: 'A FOX',       s: 1.5, y: 168 }
  ];

  ORGANISMS.forEach(function (o) {
    var producer = o.kind === 'producer';
    A[o.key] = {
      title: o.title,
      kind: o.kind,
      alt: o.word + ' standing in sunlight. ' + (producer
        ? 'It makes its own food, so it is a producer.'
        : 'Nothing happens — it cannot make food, so it has to eat. It is a consumer.'),
      svg: function () {
        return g('sun', SUN, SHAPE.sun(52, 54, 0.8)) +
          g('beam', SUN, sunbeam(80, 86, 156, 138)) +
          g('body', producer ? PLANT : ANIMAL, SHAPE[o.shape](200, o.y, o.s) + txt(200, 250, o.word, 14)) +
          (producer ? '' :
            g('nofood', DEAD,
              ln('M 250 108 L 300 150', 4, DEAD) + ln('M 300 108 L 250 150', 4, DEAD) +
              txt(275, 98, 'CANNOT MAKE FOOD', 11, DEAD)) +
            g('eats', ANIMAL, arrow(308, 360, 200) + txt(340, 232, 'FOOD', 12))) +
          label('kind', 12, 12, producer ? 'PRODUCER' : 'CONSUMER', producer ? PLANT : ANIMAL, 200, o.y) +
          label('why', 12, 258, producer ? 'MAKES ITS OWN FOOD' : 'HAS TO EAT', producer ? PLANT : ANIMAL, 200, 218);
      },
      teach: producer
        ? 'show body                     :: ' + o.word + '.\n' +
          'show beam + glow body         :: Sunlight lands on it. Watch what it does with it.\n' +
          'hi body + label why           :: It makes its own food. Out of light. Nothing has to be eaten.\n' +
          'label kind                    :: That is a producer.'
        : 'show body                     :: ' + o.word + '.\n' +
          'show beam                     :: Sunlight lands on it too. Now watch.\n' +
          'show nofood + cross           :: Nothing. It cannot do a single thing with the light.\n' +
          'show eats + label why         :: So it has to get its food by eating something else.\n' +
          'label kind                    :: That is a consumer.',
      reveal: producer
        ? 'think                         :: Producer or consumer? Everybody decide.\n' +
          'unthink + show beam + glow body + hi body :: Sunlight in — and it makes its own food.\n' +
          'label kind + label why + tick :: A plant. A producer.'
        : 'think                         :: Producer or consumer? Everybody decide.\n' +
          'unthink + show beam + show nofood + cross :: Sunlight in — and nothing happens.\n' +
          'show eats + label kind + label why :: It has to eat. A consumer.'
    };
  });

  /* the challenge card — a big clever animal is still a consumer */
  A.foxquestion = {
    title: 'Can a fox make its own food?',
    kind: 'consumer',
    alt: 'A fox standing in bright sunlight. Nothing happens: it cannot make food from ' +
         'light, so it has to hunt.',
    svg: function () {
      return g('sun', SUN, SHAPE.sun(52, 54, 0.9)) +
        g('beam', SUN, sunbeam(82, 90, 152, 146)) +
        g('body', ANIMAL, SHAPE.fox(196, 176, 1.5) + txt(196, 254, 'A FOX', 14)) +
        g('nofood', DEAD, ln('M 250 88 L 312 138', 4, DEAD) + ln('M 312 88 L 250 138', 4, DEAD)) +
        g('eats', ANIMAL, SHAPE.rabbit(340, 190, 0.6) + arrow(276, 306, 190)) +
        label('kind', 12, 12, 'CONSUMER', ANIMAL, 196, 176) +
        label('why', 12, 258, 'CLEVER — STILL HAS TO EAT', ANIMAL, 300, 214);
    },
    teach:
      'show body                       :: A fox. Fast, clever, good at hunting.\n' +
      'show beam                       :: Put it in bright sunlight all day. Watch.\n' +
      'show nofood + cross             :: Nothing. Being clever makes no difference at all.\n' +
      'show eats + label why           :: It still has to catch something and eat it.\n' +
      'label kind                      :: Consumer. Every animal is.',
    reveal:
      'show body + think               :: Can a fox make its own food? Decide.\n' +
      'unthink + show beam + show nofood + cross :: No. Sunlight does nothing for it.\n' +
      'show eats + label kind + label why :: It has to eat. Clever does not help.'
  };

  global.BioSVG.register(A);

})(typeof window !== 'undefined' ? window : this);
