/* ============================================================================
   GROW ANIMATION FRAMEWORK · Phase 2 — CHEMISTRY SVG LIBRARY
   ---------------------------------------------------------------------------
   Atoms, ions, bonding, reactions, dissolving, combustion, neutralisation and
   electrolysis.

   Chemistry is taught almost entirely in models, and pupils routinely mistake
   the model for the thing. So every asset here is built to be run as a MORPH:
   the same particles, rearranged. Nothing appears from nowhere and nothing
   vanishes — because that is the one idea the whole subject rests on.

   Requires grow-svg.js.
   ========================================================================== */
(function (global) {
  'use strict';
  var S = global.GrowSVG; if (!S) { return; }
  var C = S.C, g = S.g, ov = S.ov, n = S.n;
  var shape = S.shape, stroke = S.stroke, dot = S.dot, circ = S.circ, rect = S.rect;
  var txt = S.txt, arrow = S.arrow, label = S.label, particles = S.particles, wave = S.wave;

  /* a labelled atom — one consistent way of drawing an atom across the suite */
  function atom(x, y, r, colour, sym, symColour) {
    return '<circle cx="' + n(x) + '" cy="' + n(y) + '" r="' + n(r) + '" fill="' + colour +
      '" stroke="' + C.ink + '" stroke-width="1.6"/>' +
      (sym ? txt(x, y + r * 0.36, sym, r * 0.95, symColour || '#fff') : '');
  }
  function bond(x1, y1, x2, y2, colour) {
    return stroke('M ' + n(x1) + ' ' + n(y1) + ' L ' + n(x2) + ' ' + n(y2), 5, colour || C.ink);
  }
  function beaker(x, y, w, h, colour) {
    return stroke('M ' + n(x) + ' ' + n(y) + ' L ' + n(x) + ' ' + n(y + h) + ' q 0 10 12 10 L ' +
      n(x + w - 12) + ' ' + n(y + h + 10) + ' q 12 0 12 -10 L ' + n(x + w) + ' ' + n(y), 3.4, colour || C.metal);
  }

  S.register({

  /* ========================================================== ATOM ==== */
  atom: {
    title: 'Inside an atom', tags: ['chemistry', 'atoms'],
    alt: 'An atom: a small central nucleus containing protons and neutrons, with electrons in shells around it. Almost all of the atom is empty space.',
    svg: function () {
      var sh = '<circle cx="200" cy="150" r="52" fill="none" stroke="' + C.soft + '" stroke-width="1.6"/>' +
               '<circle cx="200" cy="150" r="94" fill="none" stroke="' + C.soft + '" stroke-width="1.6"/>';
      return g('shells', C.soft, sh) +
        g('nucleus', C.force,
          dot(196, 146, 9, C.force) + dot(206, 152, 9, C.force) +
          dot(198, 158, 9, C.soft) + dot(208, 142, 9, C.soft)) +
        g('inner', C.field, dot(252, 150, 7, C.field) + dot(148, 150, 7, C.field),
          ' data-flow-orbit="200 150 7"') +
        g('outer', C.field,
          dot(294, 150, 7, C.field) + dot(106, 150, 7, C.field) +
          dot(200, 56, 7, C.field) + dot(200, 244, 7, C.field),
          ' data-flow-orbit="200 150 14"') +
        ov('field', C.field, txt(200, 292, 'if the nucleus were a pea, the atom would be a football pitch', 11, C.field)) +
        ov('particle', C.particle,
          txt(96, 40, 'protons +', 11, C.force) + txt(96, 56, 'neutrons 0', 11, C.soft) +
          txt(310, 40, 'electrons −', 11, C.field)) +
        label('nuc', 218, 106, 'NUCLEUS', C.force, 208, 140) +
        label('empt', 14, 262, 'Nearly all of it is EMPTY SPACE', C.soft) +
        label('out', 236, 240, 'The OUTER shell does the chemistry', C.field, 244, 224);
    },
    teach:
      'observe: show shells :: Two rings. Hold that thought.\n' +
      'notice: pop nucleus + zoom nucleus :: Right in the middle — the nucleus. Protons and neutrons.\n' +
      'explain: unzoom + label nuc + overlay particle :: Protons are positive. Neutrons are nothing. That is the mass.\n' +
      'notice: show inner, outer + flow inner, outer :: Electrons, out here, negative.\n' +
      'think: pause "How much of this atom is actually solid?" :: Have a guess out loud.\n' +
      'explain: overlay field + label empt :: Almost none of it. You are mostly empty space.\n' +
      'label: glow outer + label out :: And it is the outer electrons that decide everything chemical.',
    reveal:
      'show shells, nucleus, inner, outer + flow inner, outer :: Nucleus in, electrons out.\n' +
      'label nuc, out :: Protons and neutrons in the middle, electrons in shells.',
    wrong:
      'show shells, nucleus, inner, outer :: Most people picture an atom as a solid little ball.\n' +
      'shake nucleus :: Packed full, all the way through.',
    right:
      'show shells, nucleus + zoom nucleus :: The nucleus is tiny.\n' +
      'unzoom + show inner, outer + flow inner, outer :: The electrons are a long way out.\n' +
      'overlay field + label empt :: Everything in between is empty. Including you.'
  },

  /* =========================================================== ION ==== */
  ion: {
    title: 'Making an ion', tags: ['chemistry', 'atoms', 'ions'],
    alt: 'A neutral sodium atom loses its single outer electron and becomes a positive sodium ion.',
    svg: function () {
      return g('shells', C.soft,
          '<circle cx="140" cy="150" r="46" fill="none" stroke="' + C.soft + '" stroke-width="1.6"/>' +
          '<circle cx="140" cy="150" r="76" fill="none" stroke="' + C.soft + '" stroke-width="1.6"/>') +
        g('core', '#C9803B', atom(140, 150, 22, '#C9803B', 'Na')) +
        g('inner', C.field, dot(186, 150, 7, C.field) + dot(94, 150, 7, C.field)) +
        g('outerelec', C.field, dot(140, 74, 8, C.field)) +
        g('freeelec', C.field, dot(300, 74, 8, C.field) + txt(300, 56, 'e⁻', 11, C.field), ' class="g-hidden"') +
        g('charge', C.force, txt(176, 116, '+', 24, C.force), ' class="g-hidden"') +
        g('neutral', C.neutral, txt(140, 250, 'ATOM · no overall charge', 12, C.neutral)) +
        g('ionised', C.force, txt(140, 250, 'ION · positive', 12, C.force), ' class="g-hidden"') +
        g('arrowout', C.ink, arrow(164, 82, 274, 76, C.ink, 3.4, 'loses one electron'), ' class="g-hidden"') +
        ov('field', C.field, txt(200, 292, 'protons unchanged — only an electron has left', 11, C.field)) +
        label('why', 210, 156, 'One electron in the outer shell — easy to lose', C.field) +
        label('res', 210, 200, 'Fewer electrons than protons → positive', C.force);
    },
    teach:
      'observe: show shells, core, inner, outerelec, neutral :: A sodium atom. Perfectly balanced.\n' +
      'notice: glow outerelec + label why :: Look at the outer shell. One lone electron.\n' +
      'think: pause "What happens if it loses that one?" :: Predict the charge.\n' +
      'notice: show arrowout + morph outerelec>freeelec :: It goes.\n' +
      'explain: morph neutral>ionised + show charge :: Now there are more protons than electrons.\n' +
      'label: label res + overlay field :: A positive ion. The nucleus never changed at all.',
    reveal:
      'show shells, core, inner, outerelec :: Sodium atom.\n' +
      'morph outerelec>freeelec + show charge, ionised :: Loses one electron.\n' +
      'label res :: Positive ion.',
    wrong:
      'show shells, core, inner, outerelec, neutral :: Most people think an ion is a different ELEMENT.\n' +
      'shake core :: That the middle has changed.',
    right:
      'show shells, core, inner, outerelec + glow core :: Watch the nucleus.\n' +
      'morph outerelec>freeelec + show charge, ionised :: The electron left. The nucleus did not move.\n' +
      'overlay field + label res :: Still sodium. Just charged.'
  },

  /* ======================================================= BONDING ==== */
  bonding: {
    title: 'Bonding', tags: ['chemistry', 'bonding'],
    alt: 'Two hydrogen atoms and one oxygen atom joining together to make a water molecule.',
    svg: function () {
      return g('sep', C.ink,
          atom(70, 150, 20, C.field, 'H') + atom(200, 150, 32, C.acid, 'O') + atom(330, 150, 20, C.field, 'H') +
          txt(200, 250, 'separate atoms', 12, C.soft)) +
        g('joined', C.ink,
          bond(174, 164, 138, 188) + bond(226, 164, 262, 188) +
          atom(200, 150, 32, C.acid, 'O') + atom(130, 194, 20, C.field, 'H') + atom(270, 194, 20, C.field, 'H') +
          txt(200, 258, 'one water molecule', 12, C.water), ' class="g-hidden"') +
        g('formula', C.water, txt(200, 44, 'H₂O', 30, C.water), ' class="g-hidden"') +
        ov('energy', C.energy, txt(200, 288, 'making bonds gives energy out', 11, C.energy)) +
        ov('particle', C.particle, txt(200, 22, 'the atoms are the same — only the joins are new', 11, C.particle)) +
        label('mol', 250, 96, 'A MOLECULE — atoms joined together', C.water) +
        label('same', 20, 96, 'Same three atoms, before and after', C.particle);
    },
    teach:
      'observe: show sep :: Three atoms. Two hydrogen, one oxygen. Loose.\n' +
      'think: pause "What do you get if these join up?" :: You already know this one.\n' +
      'notice: morph sep>joined :: They bond.\n' +
      'explain: show formula + bounce formula + label mol :: Water. H₂O.\n' +
      'label: overlay particle + label same :: Count them. Same three atoms. Only the joins are new.',
    reveal:
      'show sep :: Three loose atoms.\n' +
      'morph sep>joined + show formula :: Bonded into water.\n' +
      'label mol, same :: A molecule.',
    process:
      'observe: show sep :: Separate atoms.\n' +
      'notice: morph sep>joined :: Bonds form.\n' +
      'explain: overlay energy + show formula :: Making bonds releases energy.\n' +
      'label: label same :: Nothing was created. Nothing destroyed.'
  },

  /* ====================================================== REACTION ==== */
  reaction: {
    title: 'A chemical reaction', tags: ['chemistry', 'reactions'],
    alt: 'Reactant molecules rearranging into product molecules. The same atoms appear on both sides, joined up differently.',
    svg: function () {
      return g('react', C.ink,
          atom(60, 110, 17, C.field, 'H') + atom(94, 110, 17, C.field, 'H') + bond(60, 110, 94, 110) +
          atom(60, 190, 17, C.field, 'H') + atom(94, 190, 17, C.field, 'H') + bond(60, 190, 94, 190) +
          atom(150, 150, 21, C.acid, 'O') + atom(190, 150, 21, C.acid, 'O') + bond(150, 150, 190, 150) +
          txt(120, 250, 'REACTANTS', 12, C.soft)) +
        g('prod', C.ink,
          atom(290, 112, 21, C.acid, 'O') + atom(262, 142, 15, C.field, 'H') + atom(318, 142, 15, C.field, 'H') +
          bond(276, 128, 290, 112) + bond(304, 128, 290, 112) +
          atom(290, 200, 21, C.acid, 'O') + atom(262, 230, 15, C.field, 'H') + atom(318, 230, 15, C.field, 'H') +
          bond(276, 216, 290, 200) + bond(304, 216, 290, 200) +
          txt(290, 268, 'PRODUCTS', 12, C.water), ' class="g-hidden"') +
        g('arrow', C.ink, arrow(210, 150, 244, 150, C.ink, 5)) +
        g('eqn', C.ink, txt(200, 36, '2H₂  +  O₂  →  2H₂O', 20, C.ink), ' class="g-hidden"') +
        ov('energy', C.energy, wave(120, 284, 290, 4, 4, 2.6, C.energy) + txt(200, 296, 'energy out', 10, C.energy)) +
        ov('particle', C.particle, txt(200, 60, '6 atoms before · 6 atoms after', 12, C.particle)) +
        label('cons', 14, 84, 'Atoms are never made or destroyed', C.particle) +
        label('new', 236, 84, 'A NEW substance is formed', C.water);
    },
    teach:
      'observe: show react :: Hydrogen and oxygen, sitting there.\n' +
      'notice: show arrow  :: Give them a spark…\n' +
      'think: pause "How many atoms will there be afterwards?" :: Count them first. Commit to a number.\n' +
      'notice: morph react>prod :: …and they rearrange.\n' +
      'explain: show eqn + overlay particle + label cons :: Six before. Six after. Not one atom made or lost.\n' +
      'label: bounce prod + label new :: But it is water now. A completely new substance.',
    reveal:
      'show react, arrow :: Reactants.\n' +
      'morph react>prod + show eqn :: Rearranged into products.\n' +
      'label cons, new :: Same atoms, new substance.',
    process:
      'observe: show react :: The reactants.\n' +
      'notice: show arrow + overlay energy :: The reaction happens.\n' +
      'notice: morph react>prod :: Bonds break, new bonds form.\n' +
      'explain: show eqn + overlay particle :: Which is why the equation has to balance.\n' +
      'label: label cons, new :: Conservation of mass.',
    wrong:
      'show react, arrow :: Most people think a reaction makes matter "disappear" or "appear".\n' +
      'shake react :: Something is used up and gone.',
    right:
      'show react, arrow + overlay particle :: Count the atoms before.\n' +
      'morph react>prod + bounce prod :: Count them again after. Six, and six.\n' +
      'show eqn + label cons :: They were only ever rearranged.'
  },

  /* ==================================================== DISSOLVING ==== */
  dissolving: {
    title: 'Dissolving', tags: ['chemistry', 'solutions'],
    alt: 'A sugar lump in a beaker of water breaks up into individual particles that spread evenly through the water. The sugar has not disappeared — it is still there.',
    svg: function () {
      return g('beaker', C.metal, beaker(104, 70, 192, 150)) +
        g('water', C.water, '<rect x="107" y="112" width="186" height="112" fill="' + C.water + '" opacity=".28"/>' +
          stroke('M 107 112 L 293 112', 2.4, C.water)) +
        g('lump', '#C9803B', rect(176, 132, 48, 40, 4)) +
        g('spread', '#C9803B', particles(114, 118, 172, 96, 8, 5, 4.5, '#C9803B', true), ' class="g-hidden"') +
        g('scaleA', C.ink, txt(340, 150, '50 g', 15, C.ink)) +
        g('scaleB', C.ink, txt(340, 150, '50 g', 15, C.neutral), ' class="g-hidden"') +
        ov('particle', C.particle, txt(200, 292, 'the particles are still there — just spread out', 11, C.particle)) +
        ov('energy', C.energy, arrow(200, 254, 200, 232, C.energy, 3, 'stirring speeds it up')) +
        label('sol', 14, 44, 'The sugar is the SOLUTE', '#C9803B') +
        label('gone', 216, 44, 'Dissolved ≠ disappeared', C.neutral);
    },
    teach:
      'observe: show beaker, water, lump, scaleA + label sol :: A sugar lump in water. Fifty grams altogether.\n' +
      'think: pause "After it dissolves, will it weigh MORE, LESS or the SAME?" :: Commit. Hands up.\n' +
      'notice: morph lump>spread + jiggle spread :: The lump breaks into single particles and spreads out.\n' +
      'explain: show scaleB + bounce scaleB :: Still fifty grams. Exactly.\n' +
      'label: overlay particle + label gone :: Dissolved does not mean gone. It means too small to see.',
    reveal:
      'show beaker, water, lump :: Sugar in water.\n' +
      'morph lump>spread + jiggle spread :: It spreads out through the water.\n' +
      'label gone :: Still there — just invisible.',
    process:
      'observe: show beaker, water, lump :: The lump sits on the bottom.\n' +
      'notice: jiggle water + overlay energy :: Water particles knock into it constantly.\n' +
      'notice: morph lump>spread + jiggle spread :: They knock particles off the edge, one at a time.\n' +
      'explain: overlay particle :: Until the sugar is spread evenly all through.\n' +
      'label: label gone :: That is a solution.',
    wrong:
      'show beaker, water, lump, scaleA :: Almost everybody thinks dissolving destroys the sugar.\n' +
      'shake lump :: You cannot see it, so it has gone.',
    right:
      'show beaker, water, lump, scaleA :: Weigh it first. Fifty grams.\n' +
      'morph lump>spread + jiggle spread + show scaleB :: Weigh it after. Fifty grams.\n' +
      'overlay particle + label gone :: Taste it if you like. It is definitely still there.'
  },

  /* =================================================== COMBUSTION ==== */
  combustion: {
    title: 'Burning', tags: ['chemistry', 'reactions', 'energy'],
    alt: 'A candle burning. Fuel and oxygen react to give carbon dioxide, water vapour, light and heat. Covering the candle removes the oxygen and the flame goes out.',
    svg: function () {
      return g('candle', '#f5e6c8', rect(178, 150, 44, 96, 4) + stroke('M 200 150 L 200 132', 3, C.ink)) +
        g('flame', C.energy,
          shape('M 200 128 q -18 -22 0 -48 q 10 16 18 0 q 14 22 -4 48 Z', 1.4) +
          shape('M 200 122 q -8 -12 0 -26 q 8 14 0 26 Z', 0)) +
        g('cover', C.metal, '<rect x="150" y="52" width="100" height="120" rx="8" fill="none" stroke="' + C.metal + '" stroke-width="4"/>', ' class="g-hidden"') +
        g('out', '#64748b', shape('M 200 128 q -10 -14 0 -28 q 8 14 0 28 Z', 1) +
          stroke('M 200 100 q -8 -16 4 -30 M 200 100 q 10 -14 2 -30', 2.4, '#64748b'), ' class="g-hidden"') +
        g('o2in', C.field, arrow(140, 116, 178, 108, C.field, 3.2, 'O₂') + arrow(260, 116, 222, 108, C.field, 3.2, 'O₂')) +
        g('co2out', C.particle, arrow(214, 74, 250, 44, C.particle, 3.2, 'CO₂ + H₂O')) +
        ov('energy', C.energy,
          wave(120, 210, 280, 4, 4, 2.6, C.energy) + txt(200, 230, 'light + heat out', 11, C.energy)) +
        ov('particle', C.particle, txt(200, 292, 'fuel + oxygen → carbon dioxide + water', 11, C.particle)) +
        label('need', 12, 40, 'Burning NEEDS oxygen', C.field) +
        label('mass', 236, 274, 'The gases still weigh something', C.particle);
    },
    teach:
      'observe: show candle, flame + glow flame :: A candle. Wax and a flame.\n' +
      'notice: show o2in + label need :: Burning is a reaction — and it needs oxygen from the air.\n' +
      'notice: show co2out + overlay energy :: Carbon dioxide and water vapour go up. Light and heat come out.\n' +
      'think: pause "What happens if I put a jar over it?" :: Predict, and say WHY.\n' +
      'notice: show cover + morph flame>out :: The oxygen runs out. The flame dies.\n' +
      'explain: overlay particle + label mass :: The wax did not vanish. It left as gas.',
    reveal:
      'show candle, flame, o2in, co2out :: Fuel plus oxygen.\n' +
      'overlay energy, particle :: Carbon dioxide and water out, energy released.\n' +
      'label need, mass :: Burning needs oxygen.',
    process:
      'observe: show candle, flame :: Alight.\n' +
      'notice: show o2in :: Oxygen goes in.\n' +
      'notice: show co2out + overlay particle :: New gases come off.\n' +
      'explain: overlay energy :: Energy is released as light and heat.\n' +
      'label: show cover + morph flame>out + label need :: Take the oxygen away and it stops.',
    wrong:
      'show candle, flame :: Most people think burning DESTROYS the wax.\n' +
      'shake candle :: It gets shorter, so it must be disappearing.',
    right:
      'show candle, flame, o2in :: Oxygen joins in from the air.\n' +
      'show co2out + overlay particle :: The wax leaves as carbon dioxide and water vapour.\n' +
      'label mass :: Weigh the gases and it all adds up. Nothing was destroyed.'
  },

  /* ================================================ NEUTRALISATION ==== */
  neutralisation: {
    title: 'Neutralisation', tags: ['chemistry', 'acids'],
    alt: 'Acid in a beaker with an indicator turning it red. Alkali is added drop by drop until the indicator turns green, showing the mixture is neutral.',
    svg: function () {
      var scale = '', i, cols = ['#e11d48', '#f97316', '#eab308', '#16a34a', '#0891b2', '#2563eb', '#6d28d9'];
      for (i = 0; i < 7; i++) {
        scale += '<rect x="' + n(28 + i * 22) + '" y="252" width="22" height="18" fill="' + cols[i] + '"/>' +
          txt(39 + i * 22, 288, String(i * 2 + 1), 10, C.ink);
      }
      return g('beaker', C.metal, beaker(118, 96, 164, 116)) +
        g('acid', C.acid, '<rect x="121" y="132" width="158" height="82" fill="' + C.acid + '" opacity=".55"/>') +
        g('mid', '#eab308', '<rect x="121" y="132" width="158" height="82" fill="#eab308" opacity=".55"/>', ' class="g-hidden"') +
        g('neutral', C.neutral, '<rect x="121" y="132" width="158" height="82" fill="' + C.neutral + '" opacity=".55"/>', ' class="g-hidden"') +
        g('pipette', C.metal, rect(192, 20, 16, 62, 6) + shape('M 192 82 L 200 100 L 208 82 Z')) +
        g('drop', C.alkali, dot(0, 0, 7, C.alkali), ' data-flow-along="#dropfall" class="g-hidden"') +
        '<path id="dropfall" d="M 200 104 L 200 138" fill="none" stroke="none"/>' +
        g('scale', C.ink, scale + txt(200, 240, 'pH scale', 11, C.ink)) +
        ov('particle', C.particle, txt(200, 22, 'H⁺ from the acid + OH⁻ from the alkali → water', 11, C.particle)) +
        label('acidlbl', 300, 130, 'ACID · low pH', C.acid, 276, 150) +
        label('neut', 288, 172, 'NEUTRAL · pH 7', C.neutral, 274, 186);
    },
    teach:
      'observe: show beaker, acid, scale + label acidlbl :: Acid, with indicator in it. Red.\n' +
      'notice: show pipette, drop + flow drop :: Now add alkali. One drop at a time.\n' +
      'notice: morph acid>mid :: Watch the colour.\n' +
      'think: pause "What colour tells you it is neutral?" :: Look at the scale and decide.\n' +
      'notice: morph mid>neutral + bounce neutral :: Green. pH 7.\n' +
      'explain: overlay particle + label neut :: The acid and the alkali have cancelled each other out — and made water.',
    reveal:
      'show beaker, acid, scale, pipette :: Acid plus indicator.\n' +
      'show drop + flow drop + morph acid>neutral :: Add alkali until it turns green.\n' +
      'label neut :: Neutral, pH 7.',
    process:
      'observe: show beaker, acid, scale :: Strong acid. pH 1.\n' +
      'notice: show pipette, drop + flow drop :: Alkali added.\n' +
      'notice: morph acid>mid :: The pH climbs.\n' +
      'explain: morph mid>neutral + overlay particle :: Until H⁺ and OH⁻ have exactly cancelled.\n' +
      'label: label neut :: Neutralisation makes water and a salt.',
    wrong:
      'show beaker, acid, scale :: Most people think "neutral" means nothing is in there.\n' +
      'shake acid :: Empty. Plain. Nothing left.',
    right:
      'show beaker, acid, pipette, drop + flow drop :: Both substances are still in the beaker.\n' +
      'morph acid>neutral + overlay particle :: They have reacted to make water and a salt.\n' +
      'label neut :: Neutral means balanced, not empty.'
  },

  /* ==================================================== ELECTROLYSIS ==== */
  electrolysis: {
    title: 'Electrolysis', tags: ['chemistry', 'electricity'],
    alt: 'Two electrodes in a beaker of solution connected to a cell. Positive ions travel to the negative electrode and negative ions to the positive electrode, and gas bubbles form on each.',
    svg: function () {
      return g('beaker', C.metal, beaker(92, 96, 216, 120)) +
        g('solution', C.water, '<rect x="95" y="124" width="210" height="92" fill="' + C.water + '" opacity=".3"/>') +
        g('cell', '#C9803B', rect(178, 24, 44, 26, 4) + stroke('M 186 16 L 186 24 M 214 10 L 214 24', 4, C.ink)) +
        g('wires', C.metal, stroke('M 178 38 L 140 38 L 140 96 M 222 38 L 260 38 L 260 96', 4, C.metal)) +
        g('cathode', C.field, rect(133, 96, 14, 100, 3) + txt(140, 88, '−', 18, C.field)) +
        g('anode', C.force, rect(253, 96, 14, 100, 3) + txt(260, 88, '+', 18, C.force)) +
        g('posions', C.force,
          '<g data-flow-item="">' + dot(210, 156, 7, C.force) + '</g>' +
          '<g data-flow-item="">' + dot(190, 184, 7, C.force) + '</g>') +
        g('negions', C.field,
          '<g data-flow-item="">' + dot(196, 140, 7, C.field) + '</g>' +
          '<g data-flow-item="">' + dot(216, 190, 7, C.field) + '</g>') +
        g('bubblesA', C.soft, dot(126, 138, 4, C.soft) + dot(122, 122, 3, C.soft) + dot(128, 108, 3.4, C.soft)) +
        g('bubblesB', C.soft, dot(272, 140, 4, C.soft) + dot(276, 124, 3, C.soft) + dot(270, 110, 3.4, C.soft)) +
        ov('current', C.field, arrow(150, 60, 250, 60, C.field, 3, 'current')) +
        ov('particle', C.particle, txt(200, 292, 'opposite charges attract — that is the whole mechanism', 11, C.particle)) +
        label('cat', 12, 244, 'POSITIVE ions go to the NEGATIVE electrode', C.force) +
        label('an', 228, 244, 'and vice versa', C.field);
    },
    teach:
      'observe: show beaker, solution, cell, wires, cathode, anode :: A solution, and two electrodes.\n' +
      'notice: overlay current :: Switch it on. Current flows.\n' +
      'observe: show posions, negions :: In the solution there are charged particles. Ions.\n' +
      'think: pause "Which electrode will the POSITIVE ions go to?" :: Think about charges.\n' +
      'notice: flow posions, negions + overlay particle :: Opposites attract. Positive goes to negative.\n' +
      'explain: show bubblesA, bubblesB + glow bubblesA :: And they turn into something new at the electrode.\n' +
      'label: label cat, an :: Electricity has split the compound up.',
    reveal:
      'show beaker, solution, cell, wires, cathode, anode, posions, negions :: Ions in solution.\n' +
      'flow posions, negions + show bubblesA, bubblesB :: They move to the opposite electrode.\n' +
      'label cat, an :: Electrolysis.',
    process:
      'observe: show beaker, solution, cathode, anode :: Electrodes in solution.\n' +
      'notice: show cell, wires + overlay current :: Current on.\n' +
      'notice: show posions, negions + flow posions, negions :: Ions move to the opposite electrode.\n' +
      'explain: show bubblesA, bubblesB + overlay particle :: New substances form at each one.\n' +
      'label: label cat, an :: The compound has been split by electricity.'
  }

  });
})(typeof window !== 'undefined' ? window : this);
