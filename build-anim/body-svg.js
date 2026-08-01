/* ============================================================================
   BUILD Animation Framework — muscles and the moving skeleton
   ---------------------------------------------------------------------------
   Registers into the BioSVG library (see bio-svg.js), so data-ba-asset="arm"
   works exactly like data-ba-asset="fish".

   These are the assets for Week 4, "Muscles Work in Pairs". That lesson is
   about a CHANGE OF STATE, not a set of parts, so all three assets are
   poseable: one click swings the forearm, fattens the muscle that is pulling
   and flattens the one that has let go. A pupil who cannot read the words can
   still see that the two muscles are taking turns.

   COLOUR LANGUAGE — the same in all three, so the model maps onto the arm:
     bone   #4E7A9B   bone · card strip · lever    (the thing that MOVES)
     muscle #C9803B   muscle · elastic band · string (the thing that PULLS)
     skin   #94a3b8   the outline you can see from outside
   The muscle that is CONTRACTING also turns gold via the framework's `hi` verb.

   Pose rules are scoped by [data-ba-asset="…"] because these three assets
   deliberately share part names (`forearm`) and pose names (`bend`).
   ========================================================================== */
(function (global) {
  'use strict';

  var H = global.BioSVG.helpers;
  var g = H.g, shape = H.shape, stroke = H.stroke, label = H.label, n = H.n;
  var BONE = H.BONE, MUSCLE = H.SHELL, SKIN = H.SOFT, INK = H.INK;

  var CARD = '#B07C46';        /* corrugated card, for the classroom model */

  /* a long bone: a shaft with a knobbly end at each side */
  function longBone(x1, y1, x2, y2, w) {
    var r = w * 0.86;
    return stroke('M ' + n(x1) + ' ' + n(y1) + ' L ' + n(x2) + ' ' + n(y2), w) +
      '<circle cx="' + n(x1) + '" cy="' + n(y1) + '" r="' + n(r) + '" fill="currentColor" stroke="' + INK + '" stroke-width="1.4"/>' +
      '<circle cx="' + n(x2) + '" cy="' + n(y2) + '" r="' + n(r) + '" fill="currentColor" stroke="' + INK + '" stroke-width="1.4"/>';
  }

  /* A muscle belly: a lens sitting ON a baseline and bulging away from it.
     dir -1 bulges up, +1 bulges down.  The pose CSS scales it FROM that
     baseline, so contracting always reads as "shorter and fatter" and
     relaxing as "longer and flatter". */
  function belly(x1, x2, base, dir, bulge) {
    var mid = (x1 + x2) / 2;
    return '<path d="M ' + n(x1) + ' ' + n(base) +
      ' Q ' + n(mid) + ' ' + n(base + dir * bulge) + ' ' + n(x2) + ' ' + n(base) +
      ' Q ' + n(mid) + ' ' + n(base + dir * bulge * 0.2) + ' ' + n(x1) + ' ' + n(base) + ' Z"' +
      ' fill="currentColor" fill-opacity="0.62" stroke="' + INK + '" stroke-width="2" stroke-linejoin="round" pathLength="1"/>';
  }

  var A = {};

  /* ------------------------------------------------------------- THE ARM */
  A.arm = {
    title: 'Arm — the muscle pair',
    alt: 'A side view of an arm. Inside it: the upper arm bone, the elbow, the two ' +
         'forearm bones, and two muscles — the biceps on top and the triceps ' +
         'underneath. When the arm bends the biceps goes short and fat and the ' +
         'triceps goes long and thin.',
    css:
      '[data-asset="arm"] [data-part="forearm"]{transform-box:view-box;transform-origin:196px 186px}' +
      '[data-asset="arm"] [data-part="biceps"]{transform-box:view-box;transform-origin:88px 174px}' +
      '[data-asset="arm"] [data-part="triceps"]{transform-box:view-box;transform-origin:88px 198px}' +
      /* BENT — the biceps has pulled the forearm up; the triceps has let go */
      '[data-pose="bend"] [data-asset="arm"] [data-part="forearm"]{transform:rotate(-68deg)}' +
      '[data-pose="bend"] [data-asset="arm"] [data-part="biceps"]{transform:scale(.74,1.95)}' +
      '[data-pose="bend"] [data-asset="arm"] [data-part="triceps"]{transform:scale(1.06,.42)}' +
      /* STRAIGHT — the two jobs swap over */
      '[data-pose="straight"] [data-asset="arm"] [data-part="forearm"]{transform:rotate(0)}' +
      '[data-pose="straight"] [data-asset="arm"] [data-part="biceps"]{transform:scale(1.06,.42)}' +
      '[data-pose="straight"] [data-asset="arm"] [data-part="triceps"]{transform:scale(.74,1.95)}',
    svg: function () {
      /* Drawn as a diagram, not a portrait: the skin is a faint rounded
         silhouette and the bones and muscles are bold bars and bands, well
         separated, so the shape change is the most salient thing on screen. */
      function skin(x, y, w, h, r) {
        return '<rect x="' + n(x) + '" y="' + n(y) + '" width="' + n(w) + '" height="' + n(h) +
          '" rx="' + n(r) + '" fill="currentColor" fill-opacity="0.17" stroke="currentColor" stroke-width="2.4"/>';
      }
      function blob(cx, cy, r) {
        return '<circle cx="' + n(cx) + '" cy="' + n(cy) + '" r="' + n(r) +
          '" fill="currentColor" fill-opacity="0.17" stroke="currentColor" stroke-width="2.4"/>';
      }
      return g('body', SKIN,
          skin(4, 108, 94, 158, 26) +          /* a bit of chest */
          blob(72, 186, 44) +                  /* the shoulder    */
          skin(56, 150, 146, 72, 34)) +        /* the upper arm   */

        g('forearm', SKIN,
          skin(188, 156, 124, 60, 28) +
          blob(332, 186, 27) +
          '<g style="color:' + BONE + '">' +
            longBone(214, 176, 292, 174, 8) +
            longBone(214, 197, 292, 199, 8) +
          '</g>') +

        g('humerus', BONE, longBone(80, 186, 188, 186, 15)) +

        g('triceps', MUSCLE, belly(88, 186, 198, 1, 40)) +
        g('biceps',  MUSCLE, belly(88, 186, 174, -1, 40)) +

        g('joint', BONE,
          '<circle cx="196" cy="186" r="13" fill="currentColor" stroke="' + INK + '" stroke-width="2"/>' +
          '<circle cx="196" cy="186" r="4.5" fill="#ffffff"/>') +

        label('biceps',   14,  12, 'BICEPS',      MUSCLE, 137, 146) +
        label('contract', 140, 12, 'SHORT + FAT', MUSCLE, 162, 142) +
        label('triceps',  14, 258, 'TRICEPS',     MUSCLE, 137, 228) +
        label('relax',    140, 258, 'LONG + THIN', MUSCLE, 162, 232) +
        label('pair',     292, 258, 'A PAIR',     BONE,   196, 202);
    },
    teach:
      'show body                            :: An arm. Yours. Put your hand on the top of it.\n' +
      'draw humerus,forearm                 :: Bones inside. One up here, two down there.\n' +
      'show joint                           :: And a joint at the elbow, so it can move.\n' +
      'show biceps + label biceps           :: The one on TOP is the biceps.\n' +
      'show triceps + label triceps         :: The one UNDERNEATH is the triceps.\n' +
      'pose bend + glow biceps + hi biceps  :: Watch it. Short. Fat. It is pulling — and the arm comes up.\n' +
      'label contract                       :: Short and fat means pulling.\n' +
      'unglow biceps + glow triceps + label relax :: Now look underneath. Long and thin. That one let go.\n' +
      'unhi biceps + unlabel contract,relax + pose straight + hi triceps :: Other way now. Watch them swap. The triceps pulls; the arm goes down.\n' +
      'glow triceps + unglow biceps + label pair :: Two muscles, taking turns. Neither one ever pushed.',
    reveal:
      'pose bend + glow biceps + hi biceps  :: The biceps is short and fat — that one is pulling.\n' +
      'label contract + label relax + tick  :: One contracts, the other relaxes.',
    revealBend:
      'pose bend                            :: Bending up.\n' +
      'glow biceps + hi biceps + label biceps :: Short and fat. The biceps is doing the pulling.\n' +
      'glow triceps + label relax + tick    :: And the triceps went long and thin. It let go.',
    revealStraight:
      'pose straight                        :: Straightening back down.\n' +
      'glow triceps + hi triceps + label triceps :: Now the TRICEPS is the short fat one.\n' +
      'glow biceps + label relax + tick     :: The biceps let go. The jobs swapped over.',
    revealHold:
      'pose bend                            :: Held still, halfway. So which one is working now?\n' +
      'glow biceps + glow triceps + hi biceps :: Both. One holds the weight up…\n' +
      'label pair + tick                    :: …the other stops it dropping. Still a pair. Nothing is resting.'
  };

  /* --------------------------------------------------- THE CARDBOARD MODEL */
  A.armmodel = {
    title: 'The card arm model',
    alt: 'The model the class builds: two strips of card joined by a split pin, ' +
         'with an elastic band along the top and another underneath. Pulling the ' +
         'top band bends the model, and the bottom band goes long and loose.',
    css:
      '[data-asset="armmodel"] [data-part="forearm"]{transform-box:view-box;transform-origin:212px 144px}' +
      '[data-asset="armmodel"] .slack{opacity:0;transition:opacity .45s}' +
      '[data-asset="armmodel"] .taut{opacity:1;transition:opacity .45s}' +
      '[data-pose="bend"] [data-asset="armmodel"] [data-part="forearm"]{transform:rotate(-70deg)}' +
      '[data-pose="bend"] [data-asset="armmodel"] [data-part="bandbottom"] .taut{opacity:0}' +
      '[data-pose="bend"] [data-asset="armmodel"] [data-part="bandbottom"] .slack{opacity:1}' +
      '[data-pose="straight"] [data-asset="armmodel"] [data-part="forearm"]{transform:rotate(0)}' +
      '[data-pose="straight"] [data-asset="armmodel"] [data-part="bandtop"] .taut{opacity:0}' +
      '[data-pose="straight"] [data-asset="armmodel"] [data-part="bandtop"] .slack{opacity:1}',
    svg: function () {
      function card(x1, x2, y1, y2) {
        return '<rect x="' + n(x1) + '" y="' + n(y1) + '" width="' + n(x2 - x1) + '" height="' + n(y2 - y1) +
          '" rx="9" fill="currentColor" fill-opacity="0.32" stroke="currentColor" stroke-width="2.8"/>' +
          stroke('M ' + n(x1 + 12) + ' ' + n((y1 + y2) / 2) + ' L ' + n(x2 - 12) + ' ' + n((y1 + y2) / 2), 1.5);
      }
      return g('upper', CARD, card(52, 212, 124, 166) +
          '<circle cx="72" cy="118" r="5.5" fill="' + INK + '"/><circle cx="72" cy="172" r="5.5" fill="' + INK + '"/>') +

        g('forearm', CARD, card(212, 350, 126, 164) +
          '<circle cx="246" cy="120" r="5.5" fill="' + INK + '"/><circle cx="246" cy="170" r="5.5" fill="' + INK + '"/>') +

        g('bandtop', MUSCLE,
          '<path class="taut" d="M 72 118 L 246 120" fill="none" stroke="currentColor" stroke-width="8" stroke-linecap="round" pathLength="1"/>' +
          '<path class="slack" d="M 72 118 Q 159 78 246 120" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" pathLength="1"/>') +

        g('bandbottom', MUSCLE,
          '<path class="taut" d="M 72 172 L 246 170" fill="none" stroke="currentColor" stroke-width="8" stroke-linecap="round" pathLength="1"/>' +
          '<path class="slack" d="M 72 172 Q 159 214 246 170" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" pathLength="1"/>') +

        g('pin', BONE,
          '<circle cx="212" cy="144" r="12" fill="currentColor" stroke="' + INK + '" stroke-width="2"/>' +
          '<circle cx="212" cy="144" r="4" fill="#ffffff"/>') +

        label('bandtop',    14,  12, 'TOP = BICEPS',     MUSCLE, 150, 119) +
        label('bandbottom', 14, 258, 'BOTTOM = TRICEPS', MUSCLE, 150, 171) +
        label('pin',       240, 258, 'PIN = ELBOW',      BONE,   212, 156) +
        label('pull',      200,  12, 'ONLY PULLED',      MUSCLE, 120, 119);
    },
    teach:
      'show upper,forearm,pin              :: Two bits of card and a split pin. That is the whole model.\n' +
      'show bandtop + label bandtop        :: One elastic band along the top.\n' +
      'show bandbottom + label bandbottom  :: One underneath.\n' +
      'pose bend + glow bandtop            :: I pull the TOP one. The model bends.\n' +
      'glow bandbottom                     :: Look at the bottom band. Long and loose. I never touched it.\n' +
      'pose straight + unglow bandtop      :: Now the BOTTOM one. It straightens — and the top goes loose.\n' +
      'unglow bandbottom + label pull      :: I pulled both times. I never once pushed. Neither can a muscle.',
    reveal:
      'pose bend + glow bandtop            :: The top band pulled.\n' +
      'glow bandbottom + label pull + tick :: The bottom one just went loose.'
  };

  /* --------------------------------------------- THE MISCONCEPTION KILLER */
  A.pullpush = {
    title: 'Can a string push?',
    alt: 'A lever on a pivot with a string tied to the top. Pulling the string ' +
         'moves the lever. Pushing it makes the string buckle in the middle and ' +
         'nothing moves at all.',
    css:
      '[data-asset="pullpush"] [data-part="lever"]{transform-box:view-box;transform-origin:296px 230px}' +
      '[data-asset="pullpush"] [data-part="hand"]{transform-box:view-box;transform-origin:70px 112px}' +
      '[data-asset="pullpush"] .buckle{opacity:0;transition:opacity .4s}' +
      '[data-pose="pull"] [data-asset="pullpush"] [data-part="lever"]{transform:rotate(-32deg)}' +
      '[data-pose="pull"] [data-asset="pullpush"] [data-part="hand"]{transform:translateX(-30px)}' +
      '[data-pose="push"] [data-asset="pullpush"] [data-part="lever"]{transform:rotate(0)}' +
      '[data-pose="push"] [data-asset="pullpush"] [data-part="hand"]{transform:translateX(92px)}' +
      '[data-pose="push"] [data-asset="pullpush"] [data-part="string"] .straight{opacity:0}' +
      '[data-pose="push"] [data-asset="pullpush"] [data-part="string"] .buckle{opacity:1}',
    svg: function () {
      return g('stand', SKIN,
          shape('M 256 230 L 336 230 L 348 256 L 244 256 Z', 0.26) +
          stroke('M 226 256 L 366 256', 4)) +

        g('lever', BONE,
          stroke('M 296 230 L 296 100', 15) +
          '<circle cx="296" cy="100" r="11" fill="currentColor" stroke="' + INK + '" stroke-width="1.6"/>') +

        g('string', MUSCLE,
          '<path class="straight" d="M 100 108 L 288 100" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" pathLength="1"/>' +
          '<path class="buckle" d="M 186 106 Q 210 50 234 108 Q 258 160 282 100" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" pathLength="1"/>') +

        g('hand', SKIN,
          shape('M 30 92 Q 88 82 102 108 Q 90 132 30 124 Z', 0.32) +
          stroke('M 48 102 L 82 100', 3) + stroke('M 48 116 L 82 114', 3)) +

        g('pivot', BONE,
          '<circle cx="296" cy="230" r="12" fill="currentColor" stroke="' + INK + '" stroke-width="2"/>' +
          '<circle cx="296" cy="230" r="4" fill="#ffffff"/>') +

        label('pull', 14,  12, 'PULL — IT MOVES', BONE,     190, 102) +
        label('push', 14, 210, 'PUSH — NOTHING',  '#dc2626', 234, 136) +
        label('rule', 14, 258, 'A MUSCLE CAN ONLY PULL', MUSCLE, 296, 200);
    },
    teach:
      'show stand,pivot,lever,string,hand     :: A lever on a pin, and a string tied to the top of it.\n' +
      'pose pull + glow string + trace string :: I PULL the string. The lever comes over. Easy.\n' +
      'label pull                             :: Pulling works.\n' +
      'pose push + shake string               :: Now I PUSH the same string. Watch what it does.\n' +
      'cross + label push                     :: It folds up in the middle. The lever has not moved at all.\n' +
      'label rule                             :: A string cannot push. Neither can a muscle. That is why they come in pairs.',
    reveal:
      'pose pull + glow string                :: Pull — it moves.\n' +
      'pose push + shake string + cross       :: Push — the string buckles and nothing happens.\n' +
      'label rule                             :: A muscle can only pull.',
    revealPush:
      'think                                  :: Can a muscle push? Everybody decide.\n' +
      'pose push + shake string + cross       :: No. Push a string and it just folds up.\n' +
      'label push + label rule                :: A muscle can only ever PULL. That is why it needs a partner.'
  };

  global.BioSVG.register(A);

})(typeof window !== 'undefined' ? window : this);
