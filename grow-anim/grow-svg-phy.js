/* ============================================================================
   GROW ANIMATION FRAMEWORK · Phase 2 — PHYSICS SVG LIBRARY
   ---------------------------------------------------------------------------
   Forces, friction, mechanisms, fair testing, circuits, light, waves, particles,
   Earth and the Moon.

   Physics is the subject where the important thing is nearly always the thing
   you cannot see, so most of these assets carry Phase 6 overlay layers
   (data-overlay="force" and friends). The scene is drawn once; the teacher
   switches on what pupils cannot see. Nothing physically changes — they simply
   see more, which is exactly the experience we want them to have.

   Requires grow-svg.js.
   ========================================================================== */
(function (global) {
  'use strict';
  var S = global.GrowSVG; if (!S) { return; }
  var C = S.C, g = S.g, ov = S.ov, n = S.n;
  var shape = S.shape, stroke = S.stroke, dot = S.dot, circ = S.circ, rect = S.rect;
  var txt = S.txt, arrow = S.arrow, label = S.label, particles = S.particles, wave = S.wave;

  var GROUND_Y = 232;

  function ground(y, colour) {
    y = y || GROUND_Y;
    return g('ground', colour || C.soft,
      stroke('M 8 ' + y + ' L 392 ' + y, 4, C.ink) +
      '<rect x="8" y="' + n(y) + '" width="384" height="' + n(292 - y) + '" fill="currentColor" opacity=".22"/>');
  }

  /* a simple crate — the box in every forces question ever written */
  function crate(x, y, w, h, colour) {
    return rect(x, y, w, h, 4) +
      stroke('M ' + n(x) + ' ' + n(y + h / 2) + ' L ' + n(x + w) + ' ' + n(y + h / 2), 1.4, C.ink) +
      stroke('M ' + n(x + w / 2) + ' ' + n(y) + ' L ' + n(x + w / 2) + ' ' + n(y + h), 1.4, C.ink);
  }

  /* the sawtooth that makes friction visible when you zoom in on a surface */
  function teeth(x1, x2, y, h, step, colour) {
    var d = 'M ' + n(x1) + ' ' + n(y), x = x1, up = true;
    while (x < x2) {
      x += step;
      d += ' L ' + n(x) + ' ' + n(up ? y - h : y);
      up = !up;
    }
    return stroke(d, 2.4, colour || 'currentColor');
  }

  S.register({

  /* =======================================================================
     FORCES — the flagship Phase 6 asset.
     A person pushes a box. Nothing on screen changes when the overlays come
     on; the pupil simply starts to see what was there all along.
     ==================================================================== */
  forces: {
    title: 'Pushing a box', tags: ['physics', 'forces', 'invisible'],
    alt: 'A person pushing a wooden box along the floor. Force arrows can be switched on to show the push, the friction, the weight and the support from the floor.',
    svg: function () {
      var bx = 175, by = 182, bw = 74, bh = 50;
      return ground() +
        g('person', C.soft,
          circ(96, 150, 15) +
          stroke('M 96 165 L 96 205', 7, C.ink) +
          stroke('M 96 205 L 82 232 M 96 205 L 114 232', 6, C.ink) +
          stroke('M 96 176 L 132 196 M 96 176 L 128 186', 6, C.ink)) +
        g('box', '#C9803B', crate(bx, by, bw, bh)) +

        /* --- the invisible science, all present from the start ----------
           Each arrow is given its own lane so that switching every layer on
           at once still reads from the back of the room. Four overlapping
           arrows would teach nothing. */
        ov('force', C.force,
          arrow(124, by + 24, bx - 5, by + 24, C.force, 5) +
          txt(146, by + 14, 'PUSH', 12, C.force)) +
        ov('friction', '#7c3aed',
          teeth(bx - 4, bx + bw + 4, GROUND_Y, 5, 9, '#7c3aed') +
          arrow(bx + bw - 6, 252, bx + 6, 252, '#7c3aed', 5) +
          txt(bx + bw / 2, 270, 'FRICTION', 12, '#7c3aed')) +
        ov('gravity', '#0f172a',
          arrow(288, 162, 288, 214, '#0f172a', 5) +
          txt(288, 252, 'WEIGHT', 11, '#0f172a')) +
        ov('reaction', C.field,
          arrow(350, 214, 350, 162, C.field, 5) +
          txt(350, 252, 'FLOOR UP', 11, C.field)) +
        ov('energy', C.energy,
          wave(20, 104, 92, 3, 3, 2.6, C.energy) +
          txt(56, 122, 'heat', 11, C.energy)) +

        label('push', 20, 62, 'A force is a push or a pull', C.force) +
        label('pair', 12, 268, 'Two surfaces rubbing', '#7c3aed', 176, GROUND_Y + 2);
    },
    teach:
      'observe: show ground, person, box               :: Watch. Somebody pushing a box. Nothing unusual.\n' +
      'think: pause "How many forces are acting on that box right now?" :: Hold up fingers. How many forces?\n' +
      'notice: overlay force + pulse box               :: One. The push.\n' +
      'notice: overlay friction                        :: But there is a second one, pushing back. Friction.\n' +
      'notice: overlay gravity, reaction               :: And two more you have never been shown. Weight down, floor up.\n' +
      'explain: label push                             :: Four forces. Not one. They were always there.\n' +
      'label: label pair + glow friction               :: Friction happens wherever two surfaces rub.',
    reveal:
      'show ground, person, box :: The push.\n' +
      'overlay force, friction  :: Push forward. Friction backward.\n' +
      'label pair               :: Two surfaces rubbing.',
    process:
      'observe: show ground, person, box :: The box starts still.\n' +
      'notice: overlay force             :: Push harder than friction — it moves.\n' +
      'notice: overlay friction          :: Friction always acts the other way.\n' +
      'explain: overlay energy           :: And the rubbing makes heat. Every single time.',
    wrong:
      'show ground, person, box + overlay force :: Most people say: one force. The push.\n' +
      'shake box                                :: So the box should just keep speeding up for ever.',
    right:
      'show ground, person, box + overlay force :: The push is real.\n' +
      'overlay friction + bounce box            :: So is friction, pushing back.\n' +
      'overlay gravity, reaction                :: And weight down, floor up. Four forces, always.\n' +
      'label pair                               :: Nothing changed. You can just see more of it.'
  },

  /* =======================================================================
     FRICTION — GROW Science Week 3.  Rough grips, smooth slides.
     ==================================================================== */
  friction: {
    title: 'Rough and smooth', tags: ['physics', 'forces', 'friction'],
    alt: 'Two ramps side by side. A block on a rough carpet ramp barely moves; an identical block on a smooth ice ramp slides away. Zooming in shows the bumps on each surface.',
    svg: function () {
      /* Two identical rigs, side by side, filling the frame — the comparison
         only works if a pupil at the back can see both at once. */
      return g('scene', C.soft,
          stroke('M 20 196 L 390 196', 3.5, C.ink) +
          stroke('M 30 72 L 190 196 M 30 72 L 30 196', 3, C.ink) +
          stroke('M 222 72 L 382 196 M 222 72 L 222 196', 3, C.ink) +
          txt(110, 218, 'ROUGH \u00b7 carpet', 12.5, C.ink) +
          txt(302, 218, 'SMOOTH \u00b7 ice', 12.5, C.ink)) +
        g('rough', '#C9803B', teeth(0, 202, 4, 5, 8, '#C9803B'),
          ' transform="translate(30 72) rotate(37.8)"') +
        g('smooth', C.water, stroke('M 222 72 L 382 196', 7, C.water)) +
        g('blockA', '#4E7A9B', crate(46, 56, 34, 26)) +
        g('blockB', '#4E7A9B', crate(238, 56, 34, 26)) +

        ov('friction', '#7c3aed',
          arrow(112, 138, 74, 108, '#7c3aed', 4.5) + txt(60, 148, 'LOTS', 12, '#7c3aed') +
          arrow(292, 128, 268, 110, '#7c3aed', 3) + txt(320, 132, 'a little', 11, '#7c3aed')) +
        ov('heat', C.energy,
          wave(96, 172, 168, 3, 3, 2.4, C.energy) + txt(132, 190, 'heat', 11, C.energy)) +

        label('grip', 14, 240, 'Rough = more friction', '#C9803B') +
        label('slide', 208, 240, 'Smooth = less friction', C.water) +
        label('why', 60, 268, 'More bumps to catch on', C.ink);
    },
    teach:
      'observe: show scene, blockA, blockB   :: Same block. Same slope. Two surfaces.\n' +
      'think: pause "Which block slides further — and why?" :: Predict. Then tell me WHY.\n' +
      'notice: zoom rough + show rough       :: Go in close on the carpet. Look at all those bumps.\n' +
      'notice: unzoom + zoom smooth + show smooth :: Now the ice. Almost nothing to catch on.\n' +
      'explain: unzoom + overlay friction    :: More bumps to catch = more friction.\n' +
      'explain: overlay heat                 :: And where there is friction there is always heat.\n' +
      'label: label grip, slide, why         :: Rough grips. Smooth slides.',
    reveal:
      'show scene, blockA, blockB, rough, smooth :: Carpet and ice.\n' +
      'overlay friction + bounce blockB          :: Less friction — it slides.\n' +
      'label grip, slide                         :: Rough grips. Smooth slides.',
    process:
      'observe: show scene, blockA, blockB :: Two identical blocks let go together.\n' +
      'notice: zoom rough + show rough     :: Bumps on one surface catching bumps on the other.\n' +
      'explain: unzoom + overlay heat      :: The catching turns movement into heat.\n' +
      'label: label grip                   :: That is friction.',
    retrieve:
      'observe: show scene              :: Two ramps. One rough, one smooth.\n' +
      'show blockA, blockB              :: Same block on each.\n' +
      'notice: show rough               :: This side is the carpet.\n' +
      'notice: show smooth              :: This side is the ice.\n' +
      'explain: overlay friction        :: Where is there MORE friction?\n' +
      'label: label grip, slide         :: Rough grips. Smooth slides.',
    wrong:
      'show scene, blockA, blockB :: Most people say friction is just "a thing that slows you down".\n' +
      'shake blockA               :: Something bad. Something to get rid of.',
    right:
      'show scene, blockA, blockB, rough :: Without friction you could not walk.\n' +
      'overlay friction + bounce blockA  :: Your shoe grips the floor BECAUSE of friction.\n' +
      'label grip                        :: Friction is not the enemy. It is the grip.'
  },

  /* =======================================================================
     MECHANISMS — GROW Science Week 4.  Levers, pulleys, gears.
     ==================================================================== */
  lever: {
    title: 'Lever', tags: ['physics', 'mechanisms'],
    alt: 'A lever: a beam balanced on a triangular pivot, with a heavy load close to the pivot and a small effort pushing down at the far end.',
    svg: function () {
      return ground() +
        g('pivot', '#64748b', shape('M 168 216 L 200 168 L 232 216 Z')) +
        g('beam', '#C9803B', ' ') +
        g('bar', '#C9803B', rect(56, 160, 300, 14, 6),
          ' transform="rotate(-6 200 167)"') +
        g('load', '#4E7A9B', crate(112, 118, 44, 34)) +
        g('hand', C.soft, circ(336, 150, 12)) +

        ov('force', C.force,
          arrow(336, 128, 336, 168, C.force, 5, 'small effort') +
          arrow(134, 108, 134, 78, C.force, 5, 'big load lifted')) +
        ov('pressure', C.field,
          arrow(200, 240, 200, 216, C.field, 4, 'pivot takes it')) +

        label('pivot', 176, 254, 'PIVOT', '#64748b') +
        label('rule', 40, 84, 'Far from the pivot = less effort needed', '#C9803B');
    },
    teach:
      'observe: show ground, pivot, bar, load :: A heavy load, and a bar resting on a pivot.\n' +
      'think: pause "Where should you push to lift it most easily?" :: Point at the spot. Then I will show you.\n' +
      'notice: show hand + overlay force      :: Push right at the far end. A small push.\n' +
      'notice: pulse load                     :: And the big load comes up.\n' +
      'explain: overlay pressure + label pivot :: The pivot takes the difference.\n' +
      'label: label rule                      :: The further from the pivot, the less effort you need.',
    reveal:
      'show ground, pivot, bar, load, hand :: Load near the pivot, effort far away.\n' +
      'overlay force + bounce load         :: Small push, big lift.\n' +
      'label pivot, rule                   :: That is a lever.',
    process:
      'observe: show ground, pivot, bar, load :: Nothing is moving yet.\n' +
      'notice: show hand + overlay force      :: Effort goes down at one end…\n' +
      'notice: pulse load                     :: …load comes up at the other.\n' +
      'explain: label rule                    :: A lever swaps a long small push for a short big one.',
    retrieve:
      'observe: show ground :: The floor.\n' +
      'show pivot           :: What is the triangle called?\n' +
      'show bar             :: And the bar across it?\n' +
      'show load, hand      :: Where does the effort go?\n' +
      'label pivot, rule    :: Pivot, effort, load.'
  },

  pulley: {
    title: 'Pulley', tags: ['physics', 'mechanisms'],
    alt: 'A pulley wheel fixed to a beam with a rope over it. Pulling down on one side of the rope lifts a load on the other side.',
    svg: function () {
      return g('beam', '#64748b', rect(40, 40, 320, 14, 4)) +
        g('wheel', '#C9803B', circ(200, 82, 26) + circ(200, 82, 6, 1.2)) +
        g('rope', C.ink,
          '<path id="ropepath" d="M 174 82 L 174 200" fill="none" stroke="' + C.ink + '" stroke-width="3"/>' +
          stroke('M 226 82 L 226 176', 3, C.ink) +
          stroke('M 200 56 A 26 26 0 0 1 226 82', 3, C.ink) +
          stroke('M 200 56 A 26 26 0 0 0 174 82', 3, C.ink)) +
        g('load', '#4E7A9B', crate(150, 200, 48, 38)) +
        g('hand', C.soft, circ(226, 190, 12)) +

        ov('force', C.force,
          arrow(250, 176, 250, 226, C.force, 5, 'pull DOWN') +
          arrow(126, 214, 126, 168, C.force, 5, 'load goes UP')) +
        ov('energy', C.energy, wave(180, 116, 222, 3, 3, 2.2, C.energy)) +

        label('swap', 34, 262, 'A pulley changes the DIRECTION of your effort', '#C9803B');
    },
    teach:
      'observe: show beam, wheel, rope, load :: A wheel, a rope and something heavy.\n' +
      'think: pause "Which way do you pull to make the load go UP?" :: Show me with your hand.\n' +
      'notice: show hand + overlay force     :: You pull DOWN…\n' +
      'notice: pulse load                    :: …and the load goes UP.\n' +
      'explain: glow wheel                   :: The wheel turns your pull around a corner.\n' +
      'label: label swap                     :: A pulley changes the direction of your effort.',
    reveal:
      'show beam, wheel, rope, load, hand :: Rope over a wheel.\n' +
      'overlay force + bounce load        :: Pull down, load goes up.\n' +
      'label swap                         :: It changes the direction.',
    process:
      'observe: show beam, wheel, rope, load :: Still.\n' +
      'notice: show hand + flow rope         :: The rope runs over the wheel.\n' +
      'explain: overlay force + pulse load   :: Down here becomes up there.\n' +
      'label: label swap                     :: Same effort. Better direction.'
  },

  gears: {
    title: 'Gears', tags: ['physics', 'mechanisms'],
    alt: 'Two gear wheels with interlocking teeth. Turning the big gear one way makes the small gear turn the other way, and faster.',
    svg: function () {
      function cog(cx, cy, r, teethN, colour) {
        var out = '', i, a, r2 = r + 9;
        for (i = 0; i < teethN; i++) {
          a = (i / teethN) * Math.PI * 2;
          out += '<rect x="' + n(cx + Math.cos(a) * r - 5) + '" y="' + n(cy + Math.sin(a) * r2 - 5) +
            '" width="10" height="12" rx="2" fill="' + colour + '" stroke="' + C.ink + '" stroke-width="1.2" ' +
            'transform="rotate(' + n(a * 180 / Math.PI + 90) + ' ' + n(cx + Math.cos(a) * r) + ' ' + n(cy + Math.sin(a) * r) + ')"/>';
        }
        return out + '<circle cx="' + n(cx) + '" cy="' + n(cy) + '" r="' + n(r) + '" fill="' + colour +
          '" stroke="' + C.ink + '" stroke-width="1.8"/><circle cx="' + n(cx) + '" cy="' + n(cy) +
          '" r="6" fill="#fff" stroke="' + C.ink + '" stroke-width="1.5"/>';
      }
      return g('bigcog', '#C9803B', cog(150, 150, 52, 14, '#C9803B'),
          ' data-flow-orbit="150 150 9"') +
        g('smallcog', '#4E7A9B', cog(272, 150, 30, 8, '#4E7A9B'),
          ' data-flow-orbit="272 150 5"') +
        ov('force', C.force,
          arrow(150, 76, 196, 96, C.force, 4, 'turn this way') +
          arrow(272, 106, 236, 122, C.force, 4, 'other way')) +
        label('dir', 26, 250, 'Meshed gears turn OPPOSITE ways', C.ink) +
        label('speed', 214, 250, 'Small gear turns FASTER', '#4E7A9B');
    },
    teach:
      'observe: show bigcog, smallcog :: Two gears, teeth locked together.\n' +
      'think: pause "If the big one turns clockwise, which way does the small one go?" :: Decide before I click.\n' +
      'notice: flow bigcog, smallcog + overlay force :: Opposite ways. Every time.\n' +
      'notice: glow smallcog          :: And count it — the small one goes round more often.\n' +
      'explain: label dir             :: Meshed gears always turn opposite ways.\n' +
      'label: label speed             :: Fewer teeth means faster turning.',
    reveal:
      'show bigcog, smallcog + flow bigcog, smallcog :: Locked teeth.\n' +
      'overlay force                                 :: Opposite directions.\n' +
      'label dir, speed                              :: Opposite, and the small one is faster.',
    process:
      'observe: show bigcog, smallcog :: Still.\n' +
      'notice: flow bigcog            :: Turn the big one.\n' +
      'notice: flow smallcog          :: The teeth push the small one round the other way.\n' +
      'label: label dir, speed        :: Opposite direction, higher speed.',
    retrieve:
      'observe: show bigcog   :: One gear.\n' +
      'show smallcog          :: And a second one, teeth locked in.\n' +
      'flow bigcog            :: I turn this one clockwise. Which way does the other go?\n' +
      'flow smallcog + label dir :: Opposite.\n' +
      'glow smallcog + label speed :: And which one turns FASTER?',
    wrong:
      'show bigcog, smallcog :: Most people expect meshed gears to turn the same way.\n' +
      'shake smallcog        :: Both clockwise, like a conveyor belt.',
    right:
      'show bigcog, smallcog + flow bigcog :: Watch one tooth.\n' +
      'flow smallcog + overlay force       :: It pushes the next gear\u2019s tooth the OTHER way round.\n' +
      'bounce smallcog + label dir, speed  :: Meshed gears always turn in opposite directions.'
  },

  /* =======================================================================
     FAIR TEST — GROW Science Week 5.  One thing changed, everything else same.
     ==================================================================== */
  fairtest: {
    title: 'Fair test', tags: ['physics', 'enquiry', 'fairtest'],
    alt: 'Three ramp-and-car experiments side by side. In the fair test only the ramp surface is changed; in the unfair test the ramp height and the car have both been changed too.',
    svg: function () {
      function rig(x, h, carColour, surf) {
        return stroke('M ' + n(x) + ' ' + n(220 - h) + ' L ' + n(x + 84) + ' 220', 3, C.ink) +
          stroke('M ' + n(x) + ' ' + n(220 - h) + ' L ' + n(x) + ' 220', 2, C.ink) +
          (surf ? teeth(x, x + 84, 0, 4, 7, surf) : '') +
          rect(x + 6, 220 - h - 14, 26, 14, 3) +
          '<circle cx="' + n(x + 12) + '" cy="' + n(220 - h) + '" r="4" fill="' + C.ink + '"/>' +
          '<circle cx="' + n(x + 26) + '" cy="' + n(220 - h) + '" r="4" fill="' + C.ink + '"/>';
      }
      return ground(220) +
        g('rigA', '#4E7A9B', rig(20, 62)) +
        g('rigB', '#4E7A9B', rig(150, 62)) +
        g('rigC', '#4E7A9B', rig(286, 96)) +
        g('surfB', '#C9803B', teeth(150, 234, 158, 5, 7, '#C9803B'),
          ' transform="rotate(-36.4 150 158)"') +
        g('varsame', C.neutral,
          txt(62, 250, 'same height', 10, C.neutral) + txt(192, 250, 'same height', 10, C.neutral)) +
        g('varchange', C.energy,
          txt(328, 250, 'DIFFERENT height', 10, C.force) + txt(328, 264, 'AND surface', 10, C.force)) +

        ov('force', C.force, arrow(300, 120, 340, 160, C.force, 3, 'more slope')) +

        label('fair', 16, 30, 'FAIR: change ONE thing', C.neutral) +
        label('unfair', 250, 30, 'UNFAIR: two things changed', C.force);
    },
    teach:
      'observe: show ground, rigA, rigB     :: Two ramps. Same height, same car.\n' +
      'notice: show surfB, varsame          :: Only ONE thing is different — the surface.\n' +
      'explain: label fair + bounce rigB    :: That is a fair test. Any difference must be the surface.\n' +
      'observe: show rigC, varchange        :: Now this one. Rougher AND steeper.\n' +
      'think: pause "If this car goes further, what caused it?" :: Talk to your partner.\n' +
      'explain: shake rigC + label unfair   :: You cannot tell. Two things changed at once.',
    reveal:
      'show ground, rigA, rigB, surfB, varsame :: One thing changed.\n' +
      'label fair + bounce rigB                :: Fair test.\n' +
      'show rigC, varchange + shake rigC       :: Two things changed.\n' +
      'label unfair                            :: Not a fair test.',
    retrieve:
      'observe: show ground, rigA :: One ramp, one car.\n' +
      'show rigB, surfB           :: A second ramp. What has been changed?\n' +
      'show varsame               :: And what has been kept the SAME?\n' +
      'label fair                 :: So is this a fair test?\n' +
      'show rigC, varchange + label unfair :: And this one — why not?',
    wrong:
      'show ground, rigA, rigC, varchange :: Most people think a fair test just means "being fair to everybody".\n' +
      'shake rigC                         :: Taking turns. Not arguing.',
    right:
      'show ground, rigA, rigB, surfB :: In science it means something exact.\n' +
      'bounce rigB + label fair       :: Change ONE thing. Keep everything else the same.\n' +
      'show rigC + shake rigC + label unfair :: Change two, and you learn nothing.'
  },

  /* =======================================================================
     EARTH AND PLANETS — GROW Science Week 6.
     ==================================================================== */
  solarsystem: {
    title: 'The Solar System', tags: ['physics', 'space'],
    alt: 'The Sun at the centre with the eight planets on their orbits. The inner rocky planets are close together; the outer gas giants are much further out.',
    svg: function () {
      /* radii chosen so the outermost orbit still clears the 300-high frame */
      var P = [
        ['Mercury', 26, 4, '#9ca3af'], ['Venus', 39, 7, '#d9a441'], ['Earth', 53, 8, '#3b82f6'],
        ['Mars', 67, 6, '#c2544d'], ['Jupiter', 88, 13, '#c98a4b'], ['Saturn', 106, 11, '#d8c07a'],
        ['Uranus', 121, 9, '#7dd3fc'], ['Neptune', 134, 9, '#4f6ff0']
      ];
      var orbits = '', planets = '';
      /* Circles, not ellipses: the planets travel by rotation, so an elliptical
         ring would leave them drifting off their own orbit as they went round. */
      P.forEach(function (p, i) {
        orbits += '<circle cx="200" cy="150" r="' + p[1] +
          '" fill="none" stroke="' + C.soft + '" stroke-width="1.2" opacity=".7"/>';
        planets += '<g data-part="' + p[0].toLowerCase() + '" style="color:' + p[3] + '"' +
          ' data-flow-orbit="200 150 ' + (6 + i * 3) + '">' +
          '<circle cx="' + n(200 + p[1]) + '" cy="150" r="' + p[2] + '" fill="' + p[3] +
          '" stroke="' + C.ink + '" stroke-width="1.2"/></g>';
      });
      return g('orbits', C.soft, orbits) +
        g('sun', C.energy, circ(200, 150, 16) +
          '<circle cx="200" cy="150" r="21" fill="none" stroke="' + C.energy + '" stroke-width="2" opacity=".5"/>') +
        planets +
        ov('gravity', C.field,
          '<circle cx="200" cy="150" r="45" fill="none" stroke="' + C.field + '" stroke-width="1.4" stroke-dasharray="4 4"/>' +
          '<circle cx="200" cy="150" r="82" fill="none" stroke="' + C.field + '" stroke-width="1.4" stroke-dasharray="4 4"/>' +
          '<circle cx="200" cy="150" r="126" fill="none" stroke="' + C.field + '" stroke-width="1.4" stroke-dasharray="4 4"/>' +
          txt(200, 292, 'gravity holds them in orbit', 11, C.field)) +
        label('star', 10, 14, 'The Sun is a STAR, not a planet', C.energy) +
        label('rocky', 10, 274, 'Rocky planets', '#c2544d') +
        label('gas', 288, 274, 'Gas giants', '#c98a4b');
    },
    teach:
      'observe: show sun + glow sun          :: Start in the middle. This is the Sun.\n' +
      'explain: label star                   :: Not a planet. A star. The only one in our Solar System.\n' +
      'observe: show orbits                  :: Eight paths around it. Orbits.\n' +
      'notice: pop mercury, venus, earth, mars + label rocky :: Four small rocky ones first.\n' +
      'think: pause "Which one is ours?"     :: Point at it. Then I will show you.\n' +
      'notice: glow earth + bounce earth     :: Third from the Sun. That is us.\n' +
      'notice: pop jupiter, saturn, uranus, neptune + label gas :: Then four huge gas ones.\n' +
      'explain: flow earth, mars, jupiter + overlay gravity :: Gravity is what keeps them going round.',
    reveal:
      'show sun, orbits, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune :: Eight planets.\n' +
      'glow earth + bounce earth :: Ours is third.\n' +
      'label star, rocky, gas    :: A star, four rocky, four gas.',
    retrieve:
      'observe: show sun :: The Sun.\n' +
      'show orbits       :: Eight orbits. Name them in order as they appear.\n' +
      'pop mercury       :: First?\n' +
      'pop venus         :: Second?\n' +
      'pop earth + bounce earth :: Third?\n' +
      'pop mars          :: Fourth?\n' +
      'pop jupiter, saturn, uranus, neptune :: And the four giants.',
    wrong:
      'show sun, orbits, earth + glow earth :: Most people picture the Sun going round the Earth.\n' +
      'shake sun                            :: Because that is exactly what it LOOKS like from here.',
    right:
      'show sun, orbits + glow sun    :: The Sun stays put.\n' +
      'flow earth, mars, venus, mercury :: The Earth is the one moving.\n' +
      'bounce earth + label star      :: We are on a spinning planet going round a star.'
  },

  earthspin: {
    title: 'Day and night', tags: ['physics', 'space'],
    alt: 'The Sun on the left shining on the Earth. The half facing the Sun is in daylight; the half facing away is in night. The Earth spins once every twenty-four hours.',
    svg: function () {
      return g('sun', C.energy, circ(52, 150, 30) +
          stroke('M 88 150 L 118 150 M 82 118 L 106 100 M 82 182 L 106 200', 3, C.energy)) +
        g('earth', '#3b82f6',
          '<circle cx="256" cy="150" r="62" fill="#3b82f6" stroke="' + C.ink + '" stroke-width="1.8"/>' +
          '<path d="M 214 108 q 26 10 34 34 q -18 24 -6 46" fill="#3F7D6E" opacity=".85"/>') +
        g('night', '#0f172a',
          '<path d="M 256 88 A 62 62 0 0 1 256 212 Z" fill="#0f172a" opacity=".72"/>') +
        g('you', C.force, dot(300, 122, 5, C.force), ' data-flow-orbit="256 150 8"') +
        ov('light', C.energy,
          arrow(112, 120, 190, 130, C.energy, 3) +
          arrow(112, 150, 190, 150, C.energy, 3) +
          arrow(112, 180, 190, 170, C.energy, 3)) +
        label('day', 190, 246, 'DAY — facing the Sun', C.energy) +
        label('night', 262, 274, 'NIGHT — facing away', '#0f172a') +
        label('spin', 190, 30, 'The Earth spins once every 24 hours', '#3b82f6');
    },
    teach:
      'observe: show sun, earth        :: The Sun, and the Earth.\n' +
      'notice: overlay light           :: Light only travels one way — outwards.\n' +
      'think: pause "So what happens to the far side of the Earth?" :: Say it before I show you.\n' +
      'notice: show night              :: It is in shadow. That is night.\n' +
      'explain: label day, night       :: Not "the Sun going out". Just facing the other way.\n' +
      'explain: show you + flow you + label spin :: You are on a planet turning once a day.',
    reveal:
      'show sun, earth, night + overlay light :: Lit side and shadow side.\n' +
      'label day, night                       :: Day and night.\n' +
      'show you + flow you + label spin       :: Because the Earth spins.',
    process:
      'observe: show sun, earth :: Midday. Your side is facing the Sun.\n' +
      'notice: overlay light    :: Sunlight only ever travels outwards, in straight lines.\n' +
      'notice: show night       :: The far side is in shadow the whole time.\n' +
      'notice: show you + flow you :: Now watch yourself being carried round.\n' +
      'explain: label day       :: Morning \u2192 midday \u2192 evening, as you turn towards and away.\n' +
      'label: label night, spin :: One turn = one day and one night. Twenty-four hours.',
    wrong:
      'show sun, earth :: Most people say night happens because the Sun goes down.\n' +
      'shake sun       :: As if the Sun moved.',
    right:
      'show sun, earth + glow sun :: The Sun does not move.\n' +
      'show night, you + flow you :: You are the one being carried round.\n' +
      'label spin, night          :: The Earth spins. That is all night is.'
  },

  /* =======================================================================
     THE MOON — GROW Science Week 7.
     ==================================================================== */
  moonphases: {
    title: 'Phases of the Moon', tags: ['physics', 'space', 'moon'],
    alt: 'The Earth in the centre with the Moon on its orbit around it and the Sun shining from the left. Below, the eight phases the Moon appears to show from Earth, from new moon to full moon and back.',
    svg: function () {
      var ph = '', i, cx;
      var names = ['New', '', 'First qtr', '', 'Full', '', 'Last qtr', ''];
      for (i = 0; i < 8; i++) {
        cx = 32 + i * 48;
        ph += '<g data-part="p' + i + '">' +
          '<circle cx="' + n(cx) + '" cy="248" r="17" fill="#1e293b" stroke="' + C.ink + '" stroke-width="1.2"/>' +
          (i === 0 ? '' :
            '<path d="M ' + n(cx) + ' 231 A 17 17 0 ' + (i < 4 ? '1 1' : '1 0') + ' ' + n(cx) + ' 265 A ' +
            n(Math.abs(17 - i * 4.25)) + ' 17 0 ' + (i < 4 ? '1 0' : '1 1') + ' ' + n(cx) + ' 231 Z" fill="#e8eef7"/>') +
          (names[i] ? txt(cx, 280, names[i], 9, C.ink) : '') + '</g>';
      }
      return g('sun', C.energy, circ(28, 100, 22) + stroke('M 54 100 L 78 100', 3, C.energy)) +
        g('orbit', C.soft, '<circle cx="230" cy="100" r="66" fill="none" stroke="' + C.soft +
          '" stroke-width="1.4" stroke-dasharray="5 5"/>') +
        g('earth', '#3b82f6', circ(230, 100, 22)) +
        g('moon', '#cbd5e1', circ(296, 100, 12), ' data-flow-orbit="230 100 10"') +
        g('phases', C.ink, ph) +
        ov('light', C.energy,
          arrow(84, 78, 150, 84, C.energy, 3) + arrow(84, 100, 150, 100, C.energy, 3) +
          arrow(84, 122, 150, 116, C.energy, 3)) +
        ov('field', C.field,
          '<circle cx="230" cy="100" r="66" fill="none" stroke="' + C.field + '" stroke-width="1.6"/>' +
          txt(230, 192, 'gravity keeps the Moon in orbit', 10, C.field)) +
        label('lit', 96, 40, 'The Moon makes NO light of its own', C.energy) +
        label('half', 250, 152, 'Half is always lit — we just see it side-on', '#cbd5e1');
    },
    teach:
      'observe: show sun, earth       :: The Sun on one side. The Earth here.\n' +
      'observe: show orbit, moon      :: And the Moon, going round us. About once a month.\n' +
      'think: pause "Does the Moon make its own light?" :: Hands up for yes.\n' +
      'notice: overlay light + label lit :: No. It is a rock. The Sun lights it, like it lights you.\n' +
      'notice: glow moon + flow moon  :: Half of it is lit ALL the time. That never changes.\n' +
      'explain: pop p0, p1, p2, p3, p4, p5, p6, p7 :: What changes is how much of the lit half we can see.\n' +
      'label: label half              :: Phases are an angle, not a shadow.',
    reveal:
      'show sun, earth, orbit, moon + overlay light :: Sunlight from one side.\n' +
      'pop p0, p1, p2, p3, p4, p5, p6, p7           :: Eight phases, one month.\n' +
      'label lit, half                              :: Same lit half — different view.',
    process:
      'observe: show sun, earth, orbit, moon :: The Moon sets off round the Earth.\n' +
      'notice: flow moon + overlay light     :: The Sun keeps lighting the same half.\n' +
      'notice: pop p0, p2, p4, p6            :: New… first quarter… full… last quarter.\n' +
      'explain: label half                   :: One trip round = one full set of phases.',
    retrieve:
      'observe: show sun, earth, orbit :: The Sun, the Earth, the Moon’s path.\n' +
      'show moon                       :: The Moon.\n' +
      'pop p0                          :: Name this phase.\n' +
      'pop p2                          :: And this one.\n' +
      'pop p4                          :: And this one.\n' +
      'pop p6 + label half             :: And the last one.',
    wrong:
      'show sun, earth, orbit, moon :: Nearly everybody thinks phases are the Earth’s shadow on the Moon.\n' +
      'shake earth                  :: Earth in the way. Moon goes dark.',
    right:
      'show sun, earth, orbit, moon + overlay light :: The Sun lights half the Moon, always.\n' +
      'flow moon + pop p0, p2, p4, p6               :: As it goes round, we see that lit half from a new angle.\n' +
      'label half                                   :: Earth’s shadow IS a real thing — but that is an eclipse, and it is rare.'
  },

  /* =======================================================================
     CIRCUITS, LIGHT, WAVES, PARTICLES — the rest of the physics core
     ==================================================================== */
  circuit: {
    title: 'Simple circuit', tags: ['physics', 'electricity'],
    alt: 'A simple circuit: a cell, wires forming a loop, a switch and a lamp. When the switch is closed the current flows all the way round and the lamp lights.',
    svg: function () {
      var loop = 'M 90 200 L 90 100 L 200 100 L 310 100 L 310 200 L 200 200 Z';
      return g('wire', C.metal,
          '<path id="loop" d="' + loop + '" fill="none" stroke="' + C.metal + '" stroke-width="5"/>') +
        g('cell', '#C9803B',
          rect(78, 186, 26, 28, 3) +
          stroke('M 84 178 L 84 186 M 98 172 L 98 186', 4, C.ink) +
          txt(120, 208, '+  −', 12, C.ink, 'start')) +
        g('switch', '#64748b',
          dot(178, 100, 5, C.ink) + dot(222, 100, 5, C.ink) +
          stroke('M 178 100 L 218 84', 4, C.metal)) +
        g('switchclosed', C.neutral,
          dot(178, 100, 5, C.ink) + dot(222, 100, 5, C.ink) +
          stroke('M 178 100 L 222 100', 4, C.neutral)) +
        g('lamp', C.energy,
          circ(310, 150, 20) + stroke('M 296 136 L 324 164 M 324 136 L 296 164', 2.4, C.ink)) +
        g('shine', C.energy,
          stroke('M 336 150 L 356 150 M 330 128 L 346 114 M 330 172 L 346 186', 3, C.energy)) +

        '<g data-part="current" data-overlay="current" data-flow-along="#loop" style="color:' + C.field + '">' +
          dot(90, 200, 6, C.field) + '</g>' +
        ov('energy', C.energy, wave(258, 236, 356, 3, 3, 2.4, C.energy) +
          txt(308, 254, 'light + heat', 10, C.energy)) +

        label('loop', 118, 244, 'Current needs a COMPLETE loop', C.field) +
        label('cellsrc', 20, 60, 'The cell pushes the current', '#C9803B');
    },
    teach:
      'observe: show wire, cell, lamp :: A cell, some wire, a lamp.\n' +
      'observe: show switch           :: And a switch. Open — there is a gap.\n' +
      'think: pause "Will the lamp light?" :: Everybody decide.\n' +
      'notice: hide switch + show switchclosed :: Close the switch.\n' +
      'notice: overlay current + flow current  :: NOW the current can go all the way round.\n' +
      'explain: show shine + glow lamp + bounce lamp :: And the lamp lights.\n' +
      'label: label loop, cellsrc     :: No complete loop, no current, no light.',
    reveal:
      'show wire, cell, lamp, switchclosed :: Complete loop.\n' +
      'overlay current + flow current      :: Current all the way round.\n' +
      'show shine + bounce lamp + label loop :: Lamp lights.',
    process:
      'observe: show wire, cell, switchclosed, lamp :: A complete circuit.\n' +
      'notice: overlay current + flow current       :: The cell pushes current round the loop.\n' +
      'notice: glow lamp + show shine               :: The lamp turns that into light…\n' +
      'explain: overlay energy                      :: …and heat. Always some heat.\n' +
      'label: label cellsrc                         :: Energy from the cell, out at the lamp.',
    wrong:
      'show wire, cell, lamp, switchclosed :: Most people think current gets "used up" by the lamp.\n' +
      'shake lamp                          :: So less comes back than went out.',
    right:
      'show wire, cell, switchclosed, lamp + overlay current :: Watch the current itself.\n' +
      'flow current + bounce lamp                            :: The same amount goes all the way round.\n' +
      'overlay energy + label loop                           :: ENERGY is transferred at the lamp. Current is not eaten.'
  },

  rays: {
    title: 'Light and shadow', tags: ['physics', 'light'],
    alt: 'A torch shining straight lines of light at an object, which blocks some of the light and casts a shadow on a screen behind it.',
    svg: function () {
      return g('torch', '#64748b', rect(20, 132, 44, 34, 5) + shape('M 64 138 L 82 128 L 82 170 L 64 160 Z')) +
        g('object', '#4E7A9B', rect(178, 106, 26, 90, 3)) +
        g('screen', C.soft, rect(320, 56, 12, 200, 3)) +
        g('rayline', C.energy,
          stroke('M 82 149 L 320 90', 2.5, C.energy) + stroke('M 82 149 L 320 210', 2.5, C.energy) +
          stroke('M 82 149 L 178 130', 2.5, C.energy) + stroke('M 82 149 L 178 176', 2.5, C.energy)) +
        g('shadow', '#0f172a', '<path d="M 204 118 L 320 96 L 320 206 L 204 186 Z" fill="#0f172a" opacity=".55"/>') +
        ov('light', C.energy,
          arrow(96, 118, 170, 106, C.energy, 2.5, 'light travels STRAIGHT')) +
        label('straight', 92, 34, 'Light travels in straight lines', C.energy) +
        label('block', 210, 268, 'A shadow is where light was BLOCKED', '#0f172a');
    },
    teach:
      'observe: show torch, screen  :: A torch and a screen.\n' +
      'notice: draw rayline + overlay light :: Light goes out in straight lines. Never round corners.\n' +
      'observe: show object         :: Now something solid in the way.\n' +
      'think: pause "What appears on the screen?" :: Draw it in the air with your finger.\n' +
      'notice: show shadow + glow shadow :: A shadow. The same shape as the object.\n' +
      'label: label straight, block :: A shadow is not a thing. It is an absence of light.',
    reveal:
      'show torch, screen, rayline, object :: Straight light, something in the way.\n' +
      'show shadow + bounce shadow         :: Shadow.\n' +
      'label straight, block               :: Light blocked, in straight lines.',
    wrong:
      'show torch, screen, object, shadow :: Most people think a shadow is made BY the object.\n' +
      'shake object                       :: Something the object gives off.',
    right:
      'show torch, screen, object + draw rayline :: Watch the light, not the object.\n' +
      'show shadow + label block                 :: The shadow is simply where light could not reach.\n' +
      'label straight                            :: Which is why it is always the shape of the blocker.'
  },

  waves: {
    title: 'Waves spreading', tags: ['physics', 'waves', 'sound'],
    alt: 'A source at the left sending out curved wavefronts that spread outwards and get further apart as they travel.',
    svg: function () {
      var w = '', i;
      for (i = 0; i < 6; i++) {
        w += '<g data-part="w' + i + '"><path d="M ' + n(70 + i * 46) + ' 66 A ' + n(60 + i * 46) +
          ' ' + n(60 + i * 46) + ' 0 0 1 ' + n(70 + i * 46) + ' 234" fill="none" stroke="' +
          C.field + '" stroke-width="' + n(3.4 - i * 0.35) + '" opacity="' + n(1 - i * 0.13) + '"/></g>';
      }
      return g('source', C.force, circ(46, 150, 16)) + w +
        g('ear', C.soft, shape('M 350 132 q 22 0 22 22 q 0 20 -18 22 q -8 1 -8 -8') ) +
        ov('energy', C.energy, arrow(80, 262, 330, 262, C.energy, 3, 'energy travels — the air does not')) +
        label('spread', 106, 26, 'Waves spread OUT from the source', C.field) +
        label('quiet', 250, 274, 'Further away = spread thinner = quieter', C.soft);
    },
    teach:
      'observe: show source + pulse source :: Something vibrating.\n' +
      'notice: pop w0, w1, w2              :: It sends waves out in every direction.\n' +
      'notice: pop w3, w4, w5 + show ear   :: They keep going until something stops them.\n' +
      'think: pause "Why is it quieter further away?" :: Talk it through.\n' +
      'explain: overlay energy + label spread :: The same energy is spread over a bigger and bigger circle.\n' +
      'label: label quiet                  :: Thinner, not slower.',
    reveal:
      'show source + pop w0, w1, w2, w3, w4, w5 :: Waves spread out.\n' +
      'show ear + overlay energy                :: Energy travels, not the air itself.\n' +
      'label spread, quiet                      :: Thinner further out.'
  },

  states: {
    title: 'Solid, liquid, gas', tags: ['physics', 'chemistry', 'particles'],
    alt: 'A particle model of the same substance three times: packed in a regular pattern as a solid, close but disordered as a liquid, and far apart as a gas.',
    svg: function () {
      return g('boxes', C.soft,
          rect(14, 84, 116, 116, 8, 2) + rect(142, 84, 116, 116, 8, 2) + rect(270, 84, 116, 116, 8, 2)) +
        g('solid', C.particle, particles(22, 92, 100, 100, 5, 5, 8, C.particle, false)) +
        g('liquid', C.water, particles(150, 108, 100, 84, 5, 4, 8, C.water, true)) +
        g('gas', '#94a3b8', particles(278, 92, 100, 100, 3, 3, 8, '#94a3b8', true)) +
        g('labels', C.ink,
          txt(72, 220, 'SOLID', 13) + txt(200, 220, 'LIQUID', 13) + txt(328, 220, 'GAS', 13)) +
        ov('energy', C.energy,
          arrow(132, 250, 268, 250, C.energy, 4, 'heating — more energy →')) +
        ov('particle', C.particle, txt(200, 282, 'the particles themselves never change', 11, C.particle)) +
        label('fixed', 16, 42, 'Solid: fixed places, only vibrate', C.particle) +
        label('free', 268, 42, 'Gas: far apart, fly anywhere', C.soft);
    },
    teach:
      'observe: show boxes, solid, labels + jiggle solid :: A solid. The particles are stuck in place — they can only vibrate.\n' +
      'explain: label fixed             :: Fixed places. That is why a solid keeps its shape.\n' +
      'observe: show liquid + jiggle liquid :: A liquid. Just as close together, but able to slide past each other.\n' +
      'think: pause "So what changes when it becomes a gas?" :: Predict it.\n' +
      'observe: show gas + jiggle gas + heat gas 2.6 :: Far apart. Flying about. Filling whatever it is in.\n' +
      'explain: overlay energy          :: Heating gives them more energy, so they move more.\n' +
      'label: overlay particle + label free :: The PARTICLES never change. Only how they move.',
    process:
      'observe: show boxes, solid, labels + jiggle solid + heat solid 0.6 :: Cold solid. Slow vibration.\n' +
      'notice: heat solid 1.8           :: Heat it. Same particles, moving more.\n' +
      'notice: morph solid>liquid + jiggle liquid :: They break out of their places. It melts.\n' +
      'notice: heat liquid 2.6          :: Keep heating.\n' +
      'explain: morph liquid>gas + jiggle gas + heat gas 3 :: They escape completely. It boils.\n' +
      'label: overlay particle          :: Nothing was created or destroyed. Only spacing and speed.',
    wrong:
      'show boxes, solid, labels :: Most people think the particles themselves melt.\n' +
      'shake solid               :: That they go soft, or change into something else.',
    right:
      'show boxes, solid, labels + jiggle solid + heat solid 0.6 :: Look at ONE particle.\n' +
      'morph solid>liquid + jiggle liquid + heat liquid 2        :: It is exactly the same particle.\n' +
      'overlay particle + label free                             :: What changed is how fast it moves and how far apart they are.'
  },

  heating: {
    title: 'Heat spreading', tags: ['physics', 'energy', 'heat'],
    alt: 'A metal bar with one end in a flame. The particles nearest the flame vibrate fastest, and the vibration passes along the bar so the far end warms up too.',
    svg: function () {
      return g('bar', C.metal, rect(70, 130, 280, 40, 5)) +
        g('flame', C.force, shape('M 84 196 q -14 -22 0 -38 q 8 12 14 0 q 12 16 -2 38 Z', 1.2)) +
        g('phot', C.force, particles(76, 136, 80, 28, 4, 2, 6, C.force, false)) +
        g('pwarm', C.energy, particles(160, 136, 90, 28, 4, 2, 6, C.energy, false)) +
        g('pcold', C.field, particles(256, 136, 88, 28, 4, 2, 6, C.field, false)) +
        ov('energy', C.energy,
          arrow(110, 108, 320, 108, C.energy, 4, 'energy passes along')) +
        ov('heat', C.force,
          wave(78, 214, 340, 3, 6, 2.4, C.force)) +
        label('hotend', 60, 250, 'HOT end — fastest', C.force) +
        label('coldend', 246, 250, 'COOL end — slowest', C.field) +
        label('pass', 92, 34, 'Vibration passes particle to particle', C.energy);
    },
    teach:
      'observe: show bar + jiggle phot, pwarm, pcold + heat phot 0.8 + heat pwarm 0.8 + heat pcold 0.8 :: A metal bar. All the particles vibrating gently.\n' +
      'observe: show flame + glow flame :: Now hold one end in a flame.\n' +
      'notice: heat phot 3 + show phot  :: The particles right there vibrate much faster.\n' +
      'think: pause "What happens to the particles next to them?" :: Say what you think.\n' +
      'notice: heat pwarm 2             :: They knock into their neighbours, and pass it on.\n' +
      'notice: heat pcold 1.4 + overlay energy :: And on. And on. Right along the bar.\n' +
      'explain: label pass, hotend, coldend :: Heat is not a substance travelling. It is vibration being passed on.',
    process:
      'observe: show bar + jiggle phot, pwarm, pcold :: Cold bar.\n' +
      'notice: show flame + heat phot 3 :: One end heated.\n' +
      'notice: heat pwarm 2             :: Passed along.\n' +
      'notice: heat pcold 1.4           :: And further.\n' +
      'explain: overlay energy + label pass :: Conduction.',
    wrong:
      'show bar, flame + jiggle phot :: Most people think heat is a substance that flows, like a liquid.\n' +
      'shake bar                     :: Something pouring down the bar.',
    right:
      'show bar, flame + jiggle phot, pwarm, pcold + heat phot 3 :: Watch what actually moves.\n' +
      'heat pwarm 2 + heat pcold 1.4 + overlay energy            :: Nothing travels along. Each particle just knocks the next one.\n' +
      'label pass                                                :: Heat is energy being passed on, not stuff moving.'
  }

  });
})(typeof window !== 'undefined' ? window : this);
