/* ==========================================================================
   LAUNCH Science (Edexcel GCSE Biology 1BI0 Foundation · Paper 1 · Topic 1)
   Per-lesson scientific payloads for the observation layer.
   --------------------------------------------------------------------------
   Each entry is PURE JSON — no functions — because the injector serialises it
   straight into the lesson file. Anything that needs code lives in the engine.

   Placement convention across the whole suite, so pupils learn the rhythm:

     I Do 1    the observation or discovery engine   (observe / discover)
     We Do 1   the thing they can drive              (model / method)
     I Do 2    scale, reasoning or data              (zoom / graph)
     We Do 2   comparison or the evidence chain      (compare / chain)

   Every teacherAsk is a question the adult says out loud. Every `reveal`,
   `explanation` and `closing` is withheld until the pupil has acted.
   ========================================================================== */

module.exports = {

/* ======================================================================= W3 */

'SCI_L_W3_L1_Microscopy': { components: [

  { key: 'obs-cell', type: 'observe', slide: 'I Do 1', anchor: '.ilm',
    title: 'Before anyone says a word — look',
    sub: 'plant cells, ×400, unlabelled',
    spine: 'Evidence',
    teacherAsk: 'What do you notice? Not what it is called — what you can actually see.',
    scene: 'plantCell',
    alt: 'A plant cell with no labels. A thick outer wall, a large central space, a round dark body near one edge, and small green ovals around the outside.',
    noticeTarget: 3, holdSeconds: 20,
    hint: 'Tap the picture wherever you notice something.',
    hotspots: [
      { x: 50, y: 10, r: 54, label: 'cell wall',
        note: 'The thick outer edge. It is rigid — it holds the shape. Only plant cells have one.' },
      { x: 50, y: 86, r: 48, label: 'cell membrane',
        note: 'The dashed line just inside the wall. It controls what gets in and out — the wall does not.' },
      { x: 24, y: 33, r: 44, label: 'nucleus',
        note: 'The round purple body. It controls the cell and holds the DNA.' },
      { x: 50, y: 50, r: 72, label: 'vacuole',
        note: 'The large space in the middle, full of cell sap. It keeps the cell firm.' },
      { x: 83, y: 50, r: 40, label: 'chloroplast',
        note: 'The small green ovals around the edge. Green because of chlorophyll — this is where photosynthesis happens.' }
    ],
    closing: 'Compare the names with the marks you made. Which of your noticings turned out to matter — and did anyone mark something that has no name yet?'
  },

  { key: 'mic-build', type: 'discover', slide: 'We Do 1',
    title: 'Build the microscope, one part at a time',
    sub: 'the labels come last',
    spine: 'Evidence',
    teacherAsk: 'Look at what is on screen. What is missing that the light would have to pass through next?',
    scene: 'microscope',
    alt: 'A light microscope assembled part by part: base and arm, lamp, stage, focus wheels, objective lenses, eyepiece.',
    steps: [
      { name: 'Base and arm', parts: ['ms-base'],
        ask: 'Nothing else exists yet. What has to be there before anything can be held steady?',
        options: ['Something to stand on', 'The lenses first', 'The slide first'] },
      { name: 'Light source', parts: ['ms-light'],
        ask: 'You are going to look THROUGH a specimen, not at it. What does that need?',
        options: ['Light from underneath', 'Light from above', 'No light at all'] },
      { name: 'Stage', parts: ['ms-stage'],
        ask: 'Where does the slide sit so the light goes through it?',
        options: ['On a flat platform above the lamp', 'Held in your hand', 'Inside the eyepiece'] },
      { name: 'Focus wheels', parts: ['ms-focus'],
        ask: 'The image will not be sharp by luck. What has to move?',
        options: ['The distance between lens and slide', 'The brightness only', 'Nothing — it is automatic'] },
      { name: 'Objective lenses', parts: ['ms-objectives'],
        ask: 'Three lenses on a turret, different lengths. Why three rather than one?',
        options: ['So you can change magnification', 'Spares in case one breaks', 'One for each colour'] },
      { name: 'Eyepiece', parts: ['ms-eyepiece'],
        ask: 'One lens left. Where does it have to go?',
        options: ['At the top, where your eye is', 'Under the stage', 'Beside the lamp'] }
    ],
    labels: [
      { x: 41, y: 22, label: 'eyepiece ×10' },
      { x: 53, y: 44, label: 'objective lenses' },
      { x: 58, y: 63, label: 'stage + slide' },
      { x: 17, y: 59, label: 'light' },
      { x: 22, y: 78, label: 'focus wheels' }
    ]
  },

  { key: 'mic-sim', type: 'model', slide: 'I Do 2', sim: 'microscope',
    title: 'Microscope simulator — bigger is not the same as better',
    sub: 'change one thing at a time',
    spine: 'Explanation',
    teacherAsk: 'Set it to ×400 and leave the focus wrong. Is that image better than a sharp ×40?',
    alt: 'A live view down the eyepiece. Cells fill more of the circle as magnification rises, and the scale bar shrinks.',
    start: { obj: 4, focus: 6, bright: 60 },
    opening: 'Light first, then the lowest objective, then focus. Same order as the real bench.',
    tradeOff: {
      ask: 'Switch ×4 → ×40. The image gets bigger. What do you LOSE at the same moment?',
      options: ['How much of the slide you can see', 'Nothing — it is just better', 'The colour'],
      after: 'Now do it and watch the scale bar and the field of view together.'
    },
    caveat: 'This is a model, not a real microscope. Real specimens are also thicker than the lens can hold in focus all at once — on a real slide, some cells sharpen while others blur.'
  },

  { key: 'light-v-electron', type: 'compare', slide: 'We Do 2',
    title: 'Two microscopes, one specimen',
    sub: 'find every difference before anyone explains one',
    spine: 'Pattern',
    teacherAsk: 'Same cells, two instruments. What is different — and which differences are about SIZE and which are about DETAIL?',
    panels: [
      { label: 'LIGHT MICROSCOPE ×400', scene: 'field', sceneOpts: { mag: 400, focus: 1, bright: 60, detail: 'light' },
        alt: 'A light microscope view: cells visible, edges soft, nothing resolved inside them.' },
      { label: 'ELECTRON MICROSCOPE ×400', scene: 'field', sceneOpts: { mag: 400, focus: 0, bright: 92, detail: 'electron' },
        alt: 'An electron microscope view at the same magnification: the same cells, crisp edges, and structures resolved inside each one.' }
    ],
    prompt: 'Tap each difference as the class agrees it is real.',
    differences: [
      { spot: 'Same magnification', note: 'Both are ×400 — so magnification is NOT the difference here.' },
      { spot: 'Edges are sharper on the right', note: 'That is resolution.' },
      { spot: 'You can see structures INSIDE the cells on the right', note: 'The light view cannot resolve them at all — they are not smaller on the left, they are simply not separable.' },
      { spot: 'The left view is slightly soft everywhere', note: 'A light microscope is limited by the wavelength of light. No amount of focusing fixes it.' },
      { spot: 'Field of view is the same size', note: 'Field of view follows magnification, and magnification has not changed.' }
    ],
    explanation: 'At the SAME magnification the electron image is clearer. So the two words are not the same thing: magnification is how much bigger, resolution is how much detail. An electron microscope wins on both — but the reason it shows sub-cellular structures is resolution, not magnification.',
    caveat: 'Drawn to make the comparison readable. A real electron micrograph has no colour — the colours you see in textbooks are added afterwards.'
  }
]},

'SCI_L_W3_L2_Magnification': { components: [

  { key: 'mag-sim', type: 'model', slide: 'I Do 1', anchor: '.ilm', sim: 'magnification',
    title: 'The equation, as a thing you can move',
    sub: 'magnification = image size ÷ real size',
    spine: 'Explanation',
    teacherAsk: 'Change ONLY the real size. Which number in the equation moves, and which two stay put?',
    alt: 'A microscope field of view with a live readout of magnification, real size and image size.',
    start: { obj: 10, real: 50 },
    opening: 'Three numbers. Fix any two and the third is decided for you.',
    tradeOff: {
      ask: 'A cell is 50 µm. You double the magnification. What happens to the IMAGE size?',
      options: ['It doubles', 'It halves', 'It stays the same'],
      after: 'Do it on the model. Watch the image-size readout, not the picture.'
    },
    caveat: 'Magnification has no unit. If your answer has mm or µm on the end, you have calculated a size, not a magnification.'
  },

  { key: 'unit-chain', type: 'chain', slide: 'We Do 1',
    title: 'Getting the units right before the arithmetic',
    sub: 'the mark is lost here, not in the division',
    spine: 'Pattern',
    teacherAsk: 'Most lost marks in this question are not maths mistakes. Where do you think they are?',
    stages: [
      { title: 'Observe — read both numbers off the question',
        body: 'Image size 20 mm. Real size 50 µm. Two different units.',
        prompt: 'Say both numbers aloud with their units before you write anything.',
        action: 'We have both numbers and their units — unlock the next step' },
      { title: 'Evidence — they are not in the same unit',
        body: 'You cannot divide millimetres by micrometres. One of them has to change.',
        prompt: 'Which one will you convert, and why that one?',
        action: 'We have agreed a conversion — unlock the next step' },
      { title: 'Pattern — 1 mm = 1000 µm',
        body: '20 mm = 20 × 1000 = 20 000 µm. Same length, written in the other unit.',
        prompt: 'Bigger unit to smaller unit means a BIGGER number. Check yours got bigger.',
        action: 'The conversion is done and checked — unlock the next step' },
      { title: 'Conclusion — now divide',
        body: '20 000 µm ÷ 50 µm = 400.',
        prompt: 'Write the four lines: equation, conversion, substitution, answer.',
        action: 'We have the number — unlock the last step' },
      { title: 'Explanation — and no unit on the answer',
        body: 'Magnification = ×400. The units cancelled when you divided µm by µm, so there is nothing left to write.',
        prompt: 'If you wrote ×400 µm, cross out the µm. That is the difference between two marks and one.' }
    ]
  },

  { key: 'mag-fov-graph', type: 'graph', slide: 'I Do 2',
    title: 'What magnification costs you',
    sub: 'field of view against total magnification',
    spine: 'Pattern',
    plot: 'line',
    teacherAsk: 'Before the last point goes on — is this line heading for zero, or does it flatten out?',
    xLabel: 'Total magnification (×)', yLabel: 'Field of view (mm)',
    points: [
      { x: 40, y: 4.5, label: '×40' },
      { x: 100, y: 1.8, label: '×100' },
      { x: 200, y: 0.9, label: '×200' },
      { x: 400, y: 0.45, label: '×400' },
      { x: 1000, y: 0.18, label: '×1000' }
    ],
    predictBefore: {
      ask: 'At ×1000, how much of the slide will you be able to see at once?',
      options: ['Less than a quarter of a millimetre', 'About 1 mm', 'About the same as ×400']
    },
    opening: 'No data yet. Plot one magnification at a time.',
    closing: 'Describe the pattern in one sentence using two numbers from the table. Then answer: why do you always start on the ×4 objective?',
    caveat: 'Typical school-microscope values, rounded. Your own microscope will differ a little — the shape of the relationship will not.'
  },

  { key: 'mag-check', type: 'pause', slide: 'We Do 2',
    title: 'One prediction before you write',
    spine: 'Application',
    teacherAsk: 'Commit to an answer before you see anyone else\'s.',
    ask: 'Eyepiece ×10, objective ×40. A pupil writes ×50. What have they done?',
    options: ['Added instead of multiplied', 'Divided the wrong way round', 'Forgotten the eyepiece'],
    after: 'Hold that. Now check it against the rule.',
    reveal: 'Total magnification = eyepiece × objective = 10 × 40 = ×400. They added. Adding is the single most common error on this question — and it is easy to spot, because adding always gives a suspiciously small number.'
  }
]},

'SCI_L_W3_L3_ExamSkills': { components: [

  { key: 'working-chain', type: 'chain', slide: 'I Do 1', anchor: '.ilm',
    title: 'Four lines of working — and what each one is worth',
    sub: 'a calculate question is marked in stages',
    spine: 'Pattern',
    teacherAsk: 'If you got the final number wrong, could you still earn marks? What would have to be on the page?',
    stages: [
      { title: 'Observe — what is the command word?',
        body: '"Calculate" means: use numbers, show working, give an answer.',
        prompt: 'Underline the command word before you do anything else.',
        action: 'We have named the command word — unlock the next step' },
      { title: 'Evidence — line 1: write the equation',
        body: 'magnification = image size ÷ real size',
        prompt: 'This line is worth a mark on its own, even if everything after it is wrong.',
        action: 'The equation is written — unlock the next step' },
      { title: 'Pattern — line 2: make the units match',
        body: 'Convert so both sizes are in the same unit. Show the conversion.',
        prompt: 'Write the conversion out. Do not do it in your head.',
        action: 'Units match and it is written down — unlock the next step' },
      { title: 'Conclusion — line 3: substitute',
        body: 'Put your numbers into the equation, in the right places.',
        prompt: 'Numbers in, nothing calculated yet.',
        action: 'Substituted — unlock the last step' },
      { title: 'Explanation — line 4: answer, with the right unit or none',
        body: 'Magnification has NO unit. A size has one. Check which you were asked for.',
        prompt: 'Circle your answer. Then check the unit one more time.' }
    ]
  },

  { key: 'command-compare', type: 'compare', slide: 'We Do 1',
    title: 'Two answers, same question',
    sub: 'one earns three marks, one earns one',
    spine: 'Pattern',
    teacherAsk: 'Both pupils got the right final number. Why is one of these worth more?',
    panels: [
      { label: 'ANSWER A — four lines of working', scene: 'field', sceneOpts: { mag: 400, focus: 0, bright: 70, detail: 'electron' },
        alt: 'A sharp, fully resolved field of view, standing for a complete answer.' },
      { label: 'ANSWER B — the number only', scene: 'field', sceneOpts: { mag: 400, focus: 6, bright: 60, detail: 'light' },
        alt: 'A blurred field of view, standing for an answer with the working missing.' }
    ],
    prompt: 'A wrote four lines. B wrote "×400". Tap each difference the class can justify.',
    differences: [
      { spot: 'A wrote the equation', note: 'Worth a mark on its own.' },
      { spot: 'A showed the unit conversion', note: 'The most commonly credited line.' },
      { spot: 'A substituted before calculating', note: 'Shows the method even if the arithmetic slips.' },
      { spot: 'Both got ×400', note: 'The final number is only one of the marks.' }
    ],
    explanation: 'B has one mark: the answer. A has all of them, and would still have most of them if the final division went wrong. Working is not politeness — it is where most of the marks physically are.',
    caveat: 'Mark allocations vary between papers. The principle — method marks exist independently of the answer — does not.'
  },

  { key: 'unit-pause', type: 'pause', slide: 'I Do 2',
    title: 'The unit trap',
    spine: 'Application',
    teacherAsk: 'Everyone commit before we check.',
    ask: 'A question says: "Calculate the real width of the cell. Give your answer in micrometres." A pupil answers "×250". What went wrong?',
    options: ['They calculated magnification, not a size', 'They used the wrong equation', 'They forgot to convert'],
    after: 'Now read the question again and find the word that decides it.',
    reveal: 'The question asked for a SIZE in micrometres, so the equation had to be rearranged: real size = image size ÷ magnification. The pupil calculated magnification instead. The command word tells you what to calculate; the unit tells you whether you calculated it.'
  }
]},

/* ======================================================================= W4 */

'SCI_L_W4_L1_Diffusion': { components: [

  { key: 'diff-obs', type: 'observe', slide: 'I Do 1', anchor: '.ilm',
    title: 'Watch the box before anyone defines anything',
    sub: 'particles, one moment in time',
    spine: 'Evidence',
    teacherAsk: 'What do you notice about WHERE the particles are? Do not use the word diffusion yet.',
    scene: 'diffusionBox', sceneOpts: { spread: 0.15, temp: 1 },
    alt: 'A box with more particles crowded on the left and few on the right.',
    noticeTarget: 2, holdSeconds: 15,
    hotspots: [
      { x: 25, y: 45, r: 70, label: 'more particles here',
        note: 'Crowded. This is the high-concentration side.' },
      { x: 76, y: 45, r: 70, label: 'fewer particles here',
        note: 'Spread out. This is the low-concentration side.' },
      { x: 50, y: 20, r: 55, label: 'a concentration gradient',
        note: 'The DIFFERENCE between the two sides is the gradient. No difference, no gradient.' }
    ],
    closing: 'Every single particle is moving in a random direction. So why is anything going to happen at all? That is the question the next model answers.'
  },

  { key: 'diff-sim', type: 'model', slide: 'We Do 1', sim: 'diffusion',
    title: 'Run it — and watch what "net movement" means',
    sub: 'the two words that carry the mark',
    spine: 'Explanation',
    teacherAsk: 'Drag time to the end. Have the particles stopped moving?',
    alt: 'Particles spreading from the crowded side until they are evenly spread.',
    start: { spread: 0, temp: 1 },
    opening: 'Drag time forward slowly. Say what is happening as it happens.',
    tradeOff: {
      ask: 'When the particles are evenly spread, what is true?',
      options: ['They have stopped moving', 'They still move, but there is no net movement', 'They all move the same way'],
      after: 'Set time to 100 and read the readout carefully.'
    },
    caveat: 'The particles here drift smoothly so you can follow them. Real particles move in fast, random, jerky paths — the spreading is the same, the individual journeys are not.'
  },

  { key: 'diff-rate-graph', type: 'graph', slide: 'I Do 2',
    title: 'What makes diffusion faster?',
    sub: 'one factor at a time',
    spine: 'Pattern',
    plot: 'bar',
    teacherAsk: 'Before the last bar — which of these three would speed diffusion up the most in a person with a fever?',
    xLabel: 'Condition', yLabel: 'Rate of diffusion (arbitrary units)',
    points: [
      { x: 1, label: 'cold', y: 4, colour: '#60a5fa' },
      { x: 2, label: 'room', y: 8, colour: '#7A5C9E' },
      { x: 3, label: 'warm', y: 14, colour: '#f97316' },
      { x: 4, label: 'warm + steep gradient', y: 22, colour: '#dc2626' }
    ],
    predictBefore: {
      ask: 'Warm AND a steeper concentration gradient together. Higher than warm alone, or about the same?',
      options: ['Higher', 'About the same', 'Lower']
    },
    opening: 'Four conditions. Plot one at a time and say what changed.',
    closing: 'Name the three factors from the bars: temperature, concentration gradient, and — from the last lesson — surface area. Each one, on its own, changes the rate.',
    caveat: 'Arbitrary units on a made-up scale. The bars show the direction and rough size of each effect, not measurements from a real experiment.'
  },

  { key: 'sa-vol', type: 'model', slide: 'We Do 2', sim: 'surfaceArea',
    title: 'Why size decides whether diffusion is enough',
    sub: 'surface area to volume ratio',
    spine: 'Application',
    teacherAsk: 'Make the block bigger. The surface gets bigger too — so why is that a problem?',
    alt: 'A cube that grows, with its surface area, volume and ratio recalculated each time.',
    start: { size: 1 },
    tradeOff: {
      ask: 'A bigger organism has MORE surface area. So why can it not rely on diffusion alone?',
      options: ['Its volume grows faster than its surface', 'Its surface stops working', 'Diffusion only works in small things by law'],
      after: 'Drag the size from 1 to 5 and watch the ratio, not the areas.'
    }
  }
]},

'SCI_L_W4_L2_GasExchange': { components: [

  { key: 'alv-discover', type: 'discover', slide: 'I Do 1', anchor: '.ilm',
    title: 'Build the exchange surface',
    sub: 'each part is there for a reason',
    spine: 'Evidence',
    teacherAsk: 'Air on one side, blood on the other. What has to be true of the wall between them?',
    scene: 'alveolus', sceneOpts: { gradient: 1 },
    alt: 'An air sac beside a blood capillary, with oxygen particles crossing between them.',
    steps: [
      { name: 'The air sac', parts: ['alv-sac'],
        ask: 'Why are lungs made of millions of tiny sacs rather than two big bags?',
        options: ['Far more surface area', 'They are easier to grow', 'To make room for the ribs'] },
      { name: 'The blood supply', parts: ['alv-blood'],
        ask: 'Blood is kept flowing past constantly. What does moving the blood away do to the concentration gradient?',
        options: ['Keeps it steep', 'Flattens it', 'Has no effect'] },
      { name: 'The wall between', parts: ['alv-wall'],
        ask: 'The wall is one cell thick. Why not thicker and stronger?',
        options: ['Short distance to diffuse', 'To save material', 'So it can stretch'] },
      { name: 'Oxygen crossing', parts: ['alv-cross'],
        ask: 'All three adaptations are now in place. Which way will the oxygen go?',
        options: ['Air sac into the blood', 'Blood into the air sac', 'Both ways equally'] }
    ],
    labels: [
      { x: 26, y: 64, label: 'large surface area' },
      { x: 68, y: 15, label: 'good blood supply — keeps the gradient steep' },
      { x: 52, y: 92, label: 'thin wall — short diffusion distance' }
    ]
  },

  { key: 'gas-predict', type: 'pause', slide: 'We Do 1',
    title: 'Predict, then run the test',
    spine: 'Question',
    teacherAsk: 'Everyone commits now — before a single bubble goes through the limewater.',
    ask: 'You breathe through limewater for 20 seconds. What will happen — and how fast compared with air pushed through by a syringe?',
    options: ['Turns cloudy quickly', 'Turns cloudy slowly', 'Stays clear'],
    after: 'Written down? Now run it — and time it.',
    reveal: 'Breathed-out air turns limewater cloudy within seconds; ordinary air takes far longer, because it contains far less carbon dioxide. The cloudiness is the evidence; carbon dioxide is the explanation. Say them in that order.'
  },

  { key: 'alv-adapt-graph', type: 'graph', slide: 'I Do 2',
    title: 'Three adaptations, three effects',
    sub: 'how much each one buys you',
    spine: 'Pattern',
    plot: 'bar',
    teacherAsk: 'If you could only fix ONE of these in a damaged lung, which would you fix?',
    xLabel: 'Alveolus', yLabel: 'Relative rate of gas exchange',
    points: [
      { x: 1, label: 'thick wall,\nsmall area', y: 3, colour: '#94a3b8' },
      { x: 2, label: '+ thin wall', y: 9, colour: '#60a5fa' },
      { x: 3, label: '+ large area', y: 17, colour: '#22c55e' },
      { x: 4, label: '+ good blood\nsupply', y: 24, colour: '#7A5C9E' }
    ],
    predictBefore: {
      ask: 'Adding a good blood supply on top of the other two — big jump, or small one?',
      options: ['Big jump', 'Small jump', 'No change']
    },
    closing: 'Now write the sentence three times, once per adaptation: "___ means ___, which increases the rate of diffusion."',
    caveat: 'Relative values on an invented scale, to show that the three adaptations stack. Real rates depend on many more variables than these three.'
  },

  { key: 'lung-compare', type: 'compare', slide: 'We Do 2',
    title: 'A healthy alveolus and a damaged one',
    sub: 'one control, both pictures',
    spine: 'Application',
    teacherAsk: 'Move the slider. Which picture changes more, and what does that tell you?',
    panels: [
      { label: 'HEALTHY', scene: 'alveolus', sceneOpts: { gradient: 1 }, syncScale: 1,
        alt: 'A healthy air sac with many oxygen particles crossing to the blood.' },
      { label: 'DAMAGED — thicker wall', scene: 'alveolus', sceneOpts: { gradient: 0.35 }, syncScale: 0.35,
        alt: 'A damaged air sac with far fewer oxygen particles crossing.' }
    ],
    sync: { key: 'gradient', label: 'Concentration gradient (how hard you breathe)', min: 0.2, max: 1.4, step: 0.1, value: 1, unit: '' },
    prompt: 'Tap each difference once the class agrees it is real.',
    differences: [
      { spot: 'Fewer particles cross on the right' },
      { spot: 'Breathing harder helps both — but not equally' },
      { spot: 'The damaged one never catches up' }
    ],
    explanation: 'Breathing harder makes the gradient steeper, which raises the rate in BOTH. But the damaged alveolus starts from a thicker wall, so the diffusion distance is longer whatever you do. That is why effort cannot fully compensate for lung damage.',
    caveat: 'A simplified model of one kind of damage (a thickened wall). Real lung disease also destroys surface area, which this model does not show.'
  }
]},

'SCI_L_W4_L3_ExamSkills': { components: [

  { key: 'describe-explain', type: 'chain', slide: 'I Do 1', anchor: '.ilm',
    title: 'Building a 3-mark "explain" — one point at a time',
    sub: 'three marks means three separate things',
    spine: 'Pattern',
    teacherAsk: 'Count the marks first. How many separate points does this answer need?',
    stages: [
      { title: 'Observe — read the command word and the marks',
        body: '"Explain how oxygen moves from the alveolus into the blood. [3]"',
        prompt: '"Explain" needs reasons, not just what happens. And 3 marks means 3 points.',
        action: 'We have the command word and the number of points — unlock the next step' },
      { title: 'Evidence — point 1: the direction',
        body: 'Oxygen moves from the alveolus into the blood.',
        prompt: 'This is DESCRIBE. On its own it is one mark of three.',
        action: 'Direction is stated — unlock the next step' },
      { title: 'Pattern — point 2: the reason',
        body: 'Because there is a higher concentration of oxygen in the alveolus than in the blood — it moves down the concentration gradient by diffusion.',
        prompt: 'The word "because" is doing the work here. That is what turns describe into explain.',
        action: 'The reason is given — unlock the next step' },
      { title: 'Conclusion — point 3: the adaptation',
        body: 'The wall is one cell thick, so the diffusion distance is short and the rate is high.',
        prompt: 'Name the adaptation AND what it does. A named part with no effect earns nothing.',
        action: 'Adaptation and its effect are both there — unlock the last step' },
      { title: 'Explanation — check it back against the marks',
        body: 'Three sentences, three marks: direction, reason, adaptation.',
        prompt: 'Read your answer and point at each mark. If you cannot point at three, you have not written three.' }
    ]
  },

  { key: 'de-compare', type: 'compare', slide: 'We Do 1',
    title: '"Describe" and "explain" are not the same question',
    sub: 'same topic, different job',
    spine: 'Pattern',
    teacherAsk: 'Both answers are true. Only one answers the question asked. Which, and why?',
    panels: [
      { label: 'DESCRIBE — what happens', scene: 'diffusionBox', sceneOpts: { spread: 1, temp: 1 },
        alt: 'Particles evenly spread — the outcome.' },
      { label: 'EXPLAIN — why it happens', scene: 'diffusionBox', sceneOpts: { spread: 0.2, temp: 1.6 },
        alt: 'Particles still crowded on one side and moving fast — the cause.' }
    ],
    prompt: 'Tap what belongs to each command word.',
    differences: [
      { spot: '"The particles spread out" → describe' },
      { spot: '"Because they move randomly" → explain' },
      { spot: '"Down the concentration gradient" → explain' },
      { spot: '"They end up evenly spread" → describe' }
    ],
    explanation: 'Describe says WHAT. Explain says WHY. An explain answer normally contains a describe answer plus a reason — so if you have written only what happens, you have half an explain answer and half the marks.',
    caveat: 'Exam boards do use these words consistently, but always check the mark allocation too — it tells you how many points to make.'
  },

  { key: 'marks-pause', type: 'pause', slide: 'I Do 2',
    title: 'How many points?',
    spine: 'Application',
    teacherAsk: 'Look at the marks in brackets before you look at anything else.',
    ask: 'A question is worth 4 marks. A pupil writes one long, correct sentence. What is the most they can get?',
    options: ['Usually 1 or 2', 'All 4 if it is good enough', 'Nothing'],
    after: 'Think about how a marker works through an answer.',
    reveal: 'A marker is looking for four separate creditable points. One sentence, however good, usually contains one or two. Writing more words does not help — writing more POINTS does. Number them on the page if it helps you count.'
  }
]},

/* ======================================================================= W5 */

'SCI_L_W5_L1_Osmosis': { components: [

  { key: 'mem-zoom', type: 'zoom', slide: 'I Do 1', anchor: '.ilm',
    title: 'From a leaf to the molecules — one continuous journey',
    sub: 'we are not changing picture, we are going further in',
    spine: 'Evidence',
    factor: 7,
    teacherAsk: 'Stop me whenever you can name what you are looking at. What is getting smaller — the object, or how much of it we can see?',
    alt: 'A continuous zoom from a whole leaf, to its cells, to a chloroplast, to the membrane, to water molecules.',
    levels: [
      { name: 'a leaf', scale: '≈ 5 cm', scene: 'leaf',
        note: 'A whole leaf. Everything after this is inside the dotted box.',
        ask: 'If we go one step further in, what will we see?',
        options: ['Cells', 'Smaller leaves', 'Nothing — it is solid'] },
      { name: 'leaf cells', scale: '≈ 50 µm', scene: 'leafCells',
        note: 'Cells, packed together. Each green oval is a chloroplast.',
        ask: 'Inside one of those cells — what are the green ovals made of?',
        options: ['More layers inside them', 'Solid green colour', 'Water only'] },
      { name: 'a chloroplast', scale: '≈ 5 µm', scene: 'chloroplast',
        note: 'One chloroplast. Stacked membranes — surface area again.',
        ask: 'Those stacks are membranes. What is a membrane actually made of?',
        options: ['Two layers of molecules', 'A solid sheet', 'Nothing — it is a gap'] },
      { name: 'the membrane', scale: '≈ 10 nm', scene: 'membrane',
        note: 'Two layers of molecules with proteins through them. There are gaps — this is why it is PARTIALLY permeable.',
        ask: 'Water gets through here. Big sugar molecules do not. Why?',
        options: ['Water molecules are small enough', 'Water is stronger', 'Sugar is heavier'] },
      { name: 'water molecules', scale: '≈ 0.3 nm', scene: 'molecules',
        note: 'Water molecules — small, and moving all the time. Osmosis is nothing more than these getting through a membrane that sugar cannot.' }
    ]
  },

  { key: 'osm-sim', type: 'model', slide: 'We Do 1', sim: 'osmosis',
    title: 'Osmosis simulator — reframe everything by WATER',
    sub: 'water moves from dilute to concentrated',
    spine: 'Explanation',
    teacherAsk: 'Find the concentration where nothing happens. What does that tell you about the inside of the cell?',
    alt: 'A potato chip in solution, changing length as the outside concentration changes, with water arrows.',
    start: { conc: 0 },
    inside: 0.3,
    opening: 'Start at 0.00 — pure water. Then raise it slowly.',
    tradeOff: {
      ask: 'The chip is in 0.5 mol/dm³ and shrinks. In terms of WATER, why?',
      options: ['More water inside than outside, so water leaves',
                'More sugar inside, so sugar leaves',
                'The chip is dissolving'],
      after: 'Set the slider to 0.50 and read the arrows.'
    },
    caveat: 'A model. Real potato cells vary between potatoes and even within one — which is why the core practical repeats and averages.'
  },

  { key: 'osm-vs-diff', type: 'compare', slide: 'We Do 2',
    title: 'Osmosis is a special case of diffusion',
    sub: 'same idea, one extra condition',
    spine: 'Pattern',
    teacherAsk: 'What do these two have in common — and what is the one thing osmosis adds?',
    panels: [
      { label: 'DIFFUSION', scene: 'diffusionBox', sceneOpts: { spread: 0.5, temp: 1 },
        alt: 'Particles spreading from crowded to less crowded.' },
      { label: 'OSMOSIS', scene: 'membrane', sceneOpts: {},
        alt: 'A partially permeable membrane with water molecules crossing it.' }
    ],
    prompt: 'Tap each statement that the class agrees is true of BOTH, or of only one.',
    differences: [
      { spot: 'Both: high to low concentration' },
      { spot: 'Both: no energy needed' },
      { spot: 'Only osmosis: it is WATER that moves' },
      { spot: 'Only osmosis: through a partially permeable membrane' }
    ],
    explanation: 'Osmosis is diffusion, with two extra conditions attached: it is water, and it goes through a partially permeable membrane. If your definition of osmosis would also be true of a smell crossing a room, you have defined diffusion.',
    caveat: 'The membrane drawing shows gaps large enough to see. Real gaps are far smaller relative to the molecules — the principle of size selection is what matters here.'
  }
]},

'SCI_L_W5_L2_OsmosisCP': { components: [

  { key: 'cp-method', type: 'method', slide: 'I Do 1', anchor: '.ilm',
    title: 'Watch the practical happen',
    sub: 'including the bit that goes wrong',
    spine: 'Evidence',
    teacherAsk: 'Watch the order. Which step could you NOT swap with the one before it?',
    scene: 'osmosisPractical',
    alt: 'An animated method: equal potato chips cut, blotted and weighed, placed into six sugar concentrations, reweighed, then percentage change calculated.',
    opening: 'Press play and watch. Do not write yet.',
    steps: [
      { label: 'Cut equal potato chips', parts: ['op-chips'],
        note: 'Same length, same width. If they are not equal, the percentage change is meaningless.',
        ask: 'Why does every chip have to be the same size to start with?',
        options: ['So the change can be compared fairly', 'So they fit in the tube', 'It does not matter'] },
      { label: 'Blot and weigh — record the starting mass', parts: ['op-balance'],
        note: 'Blot to remove surface water. Water clinging to the outside is not water that moved.' },
      { label: 'Into the solutions, all at once', parts: ['op-tubes'],
        note: 'Same time, same temperature, same volume. Only the concentration is allowed to differ.',
        ask: 'One chip goes in five minutes late. What does that do to the result?',
        options: ['Makes it unfair — time is not controlled', 'No effect', 'Makes it more accurate'] },
      { label: 'Remove, blot again, reweigh', parts: ['op-reweigh'],
        note: 'Blot exactly the same way as before. Different blotting is the biggest source of error in this practical.' },
      { label: 'Calculate percentage change', parts: ['op-calc'],
        note: '(change in mass ÷ starting mass) × 100. Percentage, not raw grams — that is what makes different chips comparable.' }
    ],
    closing: 'Now write the method in your own words, in the order you just saw. Then name the three control variables.'
  },

  { key: 'cp-predict', type: 'pause', slide: 'We Do 1',
    title: 'Commit before you weigh',
    spine: 'Question',
    teacherAsk: 'Everybody writes a prediction now. Wrong predictions are useful — they are what the evidence has to explain.',
    ask: 'The chip in pure water and the chip in 1.0 mol/dm³ sugar. What will each do?',
    options: ['Pure water gains, strong sugar loses',
              'Both gain', 'Both lose', 'Pure water loses, strong sugar gains'],
    after: 'Recorded. Now weigh them and find out.',
    reveal: 'In pure water there is more water outside than inside, so water enters and the chip gains mass. In strong sugar there is less water outside, so water leaves and the chip loses mass. Somewhere between the two is a concentration where nothing changes — and that concentration is what the graph will tell you.'
  },

  { key: 'cp-graph', type: 'graph', slide: 'I Do 2',
    title: 'Plot your results as they come in',
    sub: 'percentage change against concentration',
    spine: 'Pattern',
    plot: 'line',
    teacherAsk: 'Before the last point — where does this line cross zero, and what does the crossing point mean?',
    xLabel: 'Sugar concentration (mol/dm³)', yLabel: 'Percentage change in mass (%)',
    zeroLine: true, fixedAxis: false,
    points: [
      { x: 0, y: 9.4, label: '0.0' },
      { x: 0.2, y: 3.6, label: '0.2' },
      { x: 0.4, y: -2.1, label: '0.4' },
      { x: 0.6, y: -7.8, label: '0.6' },
      { x: 0.8, y: -12.0, label: '0.8' },
      { x: 1.0, y: -15.3, label: '1.0' }
    ],
    predictBefore: {
      ask: 'At 1.0 mol/dm³ — will the loss be bigger than at 0.8, or has it flattened off?',
      options: ['Bigger loss', 'About the same', 'Starts gaining again']
    },
    opening: 'No data yet. Plot one concentration at a time and say what it means.',
    closing: 'Find where your line crosses zero. That concentration is the concentration INSIDE the potato cells — because that is where there is no net movement of water.',
    caveat: 'Typical class results. Yours will not match exactly — and where they do not, that is data about your method, not a mistake to hide.'
  }
]},

'SCI_L_W5_L3_Evaluate': { components: [

  { key: 'zero-graph', type: 'graph', slide: 'I Do 1', anchor: '.ilm',
    title: 'Reading the zero-change point',
    sub: 'the number the graph is actually for',
    spine: 'Pattern',
    plot: 'line',
    teacherAsk: 'The question does not ask you to describe the line. It asks for ONE number. Which one?',
    xLabel: 'Sugar concentration (mol/dm³)', yLabel: 'Percentage change in mass (%)',
    zeroLine: true,
    points: [
      { x: 0, y: 11.2, label: '0.0' },
      { x: 0.2, y: 5.1, label: '0.2' },
      { x: 0.4, y: -1.4, label: '0.4' },
      { x: 0.6, y: -8.9, label: '0.6' },
      { x: 0.8, y: -13.7, label: '0.8' },
      { x: 1.0, y: -17.1, label: '1.0' }
    ],
    predictBefore: {
      ask: 'Between which two concentrations does this line cross zero?',
      options: ['0.2 and 0.4', '0.0 and 0.2', '0.6 and 0.8']
    },
    closing: 'It crosses at about 0.35 mol/dm³. That is the concentration inside the potato cells — read it off the x-axis where y = 0, and say why: at that point there is no net movement of water.',
    caveat: 'Reading between plotted points is an estimate. Quote it to a sensible precision — "about 0.35", not "0.3512".'
  },

  { key: 'eval-chain', type: 'chain', slide: 'We Do 1',
    title: 'Evaluate — and it is not "it went well"',
    sub: 'evidence, then judgement, then improvement',
    spine: 'Evaluation',
    teacherAsk: 'An evaluation that names no evidence is an opinion. What evidence have we actually got?',
    stages: [
      { title: 'Observe — look at the spread of the repeats',
        body: 'Three repeats at 0.4 mol/dm³ gave −1.4%, −2.9% and −0.2%.',
        prompt: 'Say the range out loud. Is that spread small or large next to the values themselves?',
        action: 'We have looked at the spread — unlock the next step' },
      { title: 'Evidence — that spread is large relative to the readings',
        body: 'A range of 2.7 percentage points, around values of about 1–3%. The repeats disagree by roughly as much as the effect itself.',
        prompt: 'That is the evidence. Not a feeling that it was messy.',
        action: 'We have quantified it — unlock the next step' },
      { title: 'Pattern — where could that variation come from?',
        body: 'Blotting is done by hand and differs every time. Potato cells also differ between chips.',
        prompt: 'Name the source, not just "human error". "Human error" earns nothing on its own.',
        action: 'We have named a real source — unlock the next step' },
      { title: 'Conclusion — is the result still usable?',
        body: 'Yes — the trend is far larger than the scatter, so the zero-crossing is still meaningful, but should be quoted as "about", not to two decimal places.',
        prompt: 'A good evaluation can conclude that the data IS good enough. That is a judgement, not a dodge.',
        action: 'We have judged the data — unlock the last step' },
      { title: 'Explanation — one improvement, with a reason',
        body: 'Blot each chip a fixed number of times with fresh paper, so surface water is removed consistently.',
        prompt: 'An improvement must say WHAT to change and WHY it would reduce the variation you named. "Be more careful" is neither.' }
    ]
  },

  { key: 'anomaly-pause', type: 'pause', slide: 'I Do 2',
    title: 'What do you do with the odd one out?',
    spine: 'Evaluation',
    teacherAsk: 'Nobody touches their results until we have agreed the rule.',
    ask: 'One repeat is wildly different from the other two. What should you do with it?',
    options: ['Identify it as anomalous and leave it out of the mean',
              'Delete it quietly', 'Include it in the mean anyway', 'Change it to fit'],
    after: 'Think about what a reader of your work needs to be able to see.',
    reveal: 'Identify it, say it is anomalous, exclude it from the mean — and say that you did. An anomaly you never mention is data you hid; an anomaly you name is evidence that you checked. Changing a reading is not an option in either case.'
  }
]},

/* ======================================================================= W6 */

'SCI_L_W6_L1_ActiveTransport': { components: [

  { key: 'at-obs', type: 'observe', slide: 'I Do 1', anchor: '.ilm',
    title: 'Something here breaks the rule you have learnt',
    sub: 'look before you judge it',
    spine: 'Evidence',
    teacherAsk: 'For two weeks everything has moved high to low. Look at this. What do you notice?',
    scene: 'activeTransport', sceneOpts: { energy: 100 },
    alt: 'Particles being moved from a region where there are few, into a region where there are already many, through a carrier protein.',
    noticeTarget: 2, holdSeconds: 18,
    hotspots: [
      { x: 50, y: 12, r: 60, label: 'few particles OUTSIDE',
        note: 'Low concentration out here.' },
      { x: 50, y: 88, r: 60, label: 'many particles INSIDE',
        note: 'High concentration in here. Already crowded.' },
      { x: 50, y: 50, r: 50, label: 'carrier protein',
        note: 'A protein in the membrane that picks particles up and moves them across.' },
      { x: 50, y: 26, r: 46, label: 'against the gradient — uphill',
        note: 'Low to HIGH. This is the opposite of diffusion, and it is the thing that costs energy.' }
    ],
    closing: 'Diffusion is free because it happens on its own. This does not happen on its own — so something has to pay for it. What, and where from?'
  },

  { key: 'at-sim', type: 'model', slide: 'We Do 1', sim: 'activeTransport',
    title: 'Turn the energy off',
    sub: 'the single experiment that separates the three processes',
    spine: 'Explanation',
    teacherAsk: 'Take the energy to 0%. Which processes stop, and which carry on?',
    alt: 'A carrier protein moving particles uphill, powered by energy from respiration.',
    start: { energy: 100 },
    opening: 'Start at 100%, then bring it down slowly.',
    tradeOff: {
      ask: 'A cell is poisoned so it cannot respire. What happens to diffusion?',
      options: ['Nothing — diffusion needs no energy', 'It stops too', 'It speeds up'],
      after: 'Set energy to 0% and read the third line of the readout.'
    },
    caveat: 'Simplified: real carrier proteins change shape to move particles, and each carries a specific substance. The energy dependence shown here is the part the exam tests.'
  },

  { key: 'three-chain', type: 'chain', slide: 'I Do 2',
    title: 'Three processes, three questions',
    sub: 'you can identify any of them with these three answers',
    spine: 'Pattern',
    teacherAsk: 'We are going to build a test that works on anything. What is the first question you would ask?',
    stages: [
      { title: 'Observe — what is moving?',
        body: 'Water? Then it is osmosis. Anything else? Diffusion or active transport.',
        prompt: 'This one question already separates osmosis from the other two.',
        action: 'We have asked what moves — unlock the next question' },
      { title: 'Evidence — which way, relative to the gradient?',
        body: 'High to low is downhill. Low to high is uphill.',
        prompt: 'Only active transport goes uphill.',
        action: 'We have asked about direction — unlock the next question' },
      { title: 'Pattern — does it need energy?',
        body: 'Diffusion and osmosis: no. Active transport: yes, from respiration.',
        prompt: 'Energy and direction always agree. Uphill always costs.',
        action: 'We have asked about energy — unlock the conclusion' },
      { title: 'Conclusion — the three answers identify it every time',
        body: 'Diffusion: any particle, downhill, no energy. Osmosis: water, downhill, no energy, through a partially permeable membrane. Active transport: any particle, uphill, energy from respiration.',
        prompt: 'Say all three definitions in one line each, without looking.',
        action: 'We can state all three — unlock the last step' },
      { title: 'Explanation — why uphill costs and downhill does not',
        body: 'Downhill movement happens by itself: random motion plus more particles on one side does it for free. Uphill movement will never happen by itself, so a cell has to spend energy to force it.',
        prompt: 'That sentence is the answer to almost every "why does active transport need energy" question.' }
    ]
  },

  { key: 'three-compare', type: 'compare', slide: 'We Do 2',
    title: 'Diffusion and active transport, side by side',
    sub: 'one control, both pictures',
    spine: 'Application',
    teacherAsk: 'Drop the energy. Watch which picture stops.',
    panels: [
      { label: 'DIFFUSION — downhill', scene: 'diffusionBox', sceneOpts: { spread: 0.6, temp: 1 }, syncScale: 0,
        alt: 'Particles spreading out on their own.' },
      { label: 'ACTIVE TRANSPORT — uphill', scene: 'activeTransport', sceneOpts: { energy: 100 }, syncScale: 1,
        alt: 'Particles being carried against the gradient.' }
    ],
    sync: { key: 'energy', label: 'Energy available from respiration', min: 0, max: 100, step: 10, value: 100, unit: '%' },
    prompt: 'Tap each difference the class can defend.',
    differences: [
      { spot: 'Only one of them stops when energy hits 0' },
      { spot: 'Left goes high → low' },
      { spot: 'Right goes low → high' },
      { spot: 'Both move particles across a membrane' }
    ],
    explanation: 'Cutting the energy stops active transport and leaves diffusion untouched. That is not a detail — it is the definition, demonstrated. Anything that keeps going without energy is going downhill.',
    caveat: 'The left panel is not driven by the energy slider at all. That is the point of the comparison, not a bug — check it yourself before you accept it.'
  }
]},

'SCI_L_W6_L2_RootAndGut': { components: [

  { key: 'root-obs', type: 'observe', slide: 'I Do 1', anchor: '.ilm',
    title: 'One cell, an odd shape',
    sub: 'why is it stretched out like that?',
    spine: 'Evidence',
    teacherAsk: 'This is a single cell. What do you notice about its shape — and what might that shape be for?',
    scene: 'rootHair',
    alt: 'A root hair cell: a rectangular cell with a long thin projection reaching out into the soil, and mineral ions around it.',
    noticeTarget: 2, holdSeconds: 16,
    hotspots: [
      { x: 70, y: 44, r: 60, label: 'the hair — a huge surface area',
        note: 'One long projection. It multiplies the surface in contact with the soil water.' },
      { x: 22, y: 50, r: 44, label: 'nucleus',
        note: 'Still an ordinary cell in every other way.' },
      { x: 78, y: 40, r: 50, label: 'mineral ions in the soil — very dilute',
        note: 'There are FEWER mineral ions in the soil than inside the cell. Remember which side has more.' }
    ],
    closing: 'Fewer ions outside, more inside — and the plant still takes them in. Which of the three processes can do that, and what does it cost?'
  },

  { key: 'root-gut-compare', type: 'compare', slide: 'We Do 1',
    title: 'A root hair and a gut lining — the same problem twice',
    sub: 'plant and animal, one mechanism',
    spine: 'Application',
    teacherAsk: 'Different organism, different substance. What is identical about the problem each one faces?',
    panels: [
      { label: 'ROOT HAIR — mineral ions', scene: 'rootHair', sceneOpts: {},
        alt: 'A root hair cell absorbing mineral ions from dilute soil water.' },
      { label: 'GUT LINING — glucose', scene: 'activeTransport', sceneOpts: { energy: 100 },
        alt: 'A gut lining cell absorbing glucose into blood that already contains more.' }
    ],
    prompt: 'Tap each thing that is TRUE OF BOTH.',
    differences: [
      { spot: 'Fewer particles outside than inside' },
      { spot: 'Moving against the gradient' },
      { spot: 'Needs energy from respiration' },
      { spot: 'Large surface area to speed it up' }
    ],
    explanation: 'A root hair takes mineral ions from soil that is more dilute than the cell. The gut takes glucose into blood that already has more glucose than the gut. Different organisms, different substances — the same uphill problem, solved by the same process. That is why one explanation answers both questions.',
    caveat: 'The gut also absorbs a great deal by diffusion when the gradient runs the other way, straight after a meal. Active transport is what lets it finish the job.'
  },

  { key: 'oxygen-graph', type: 'graph', slide: 'I Do 2',
    title: 'The evidence that active transport needs respiration',
    sub: 'ion uptake against oxygen available',
    spine: 'Pattern',
    plot: 'line',
    teacherAsk: 'This graph is the proof, not the illustration. Before the last point — what happens when the oxygen runs out?',
    xLabel: 'Oxygen concentration (%)', yLabel: 'Rate of ion uptake (arbitrary units)',
    points: [
      { x: 0, y: 1, label: '0' },
      { x: 5, y: 8, label: '5' },
      { x: 10, y: 15, label: '10' },
      { x: 15, y: 20, label: '15' },
      { x: 20, y: 22, label: '20' },
      { x: 25, y: 22.5, label: '25' }
    ],
    predictBefore: {
      ask: 'Past 20% oxygen — does uptake keep climbing, or level off?',
      options: ['Levels off', 'Keeps climbing', 'Falls']
    },
    opening: 'No data yet. Plot one oxygen level at a time.',
    closing: 'Near zero oxygen, uptake almost stops — because without oxygen there is no aerobic respiration and no energy. It then levels off, because something else has become the limiting factor. Both halves of that sentence are creditable.',
    caveat: 'Arbitrary units. The shape of the curve is what carries the argument — the exact numbers would differ with species and temperature.'
  }
]},

'SCI_L_W6_L3_Compare': { components: [

  { key: 'compare-chain', type: 'chain', slide: 'I Do 1', anchor: '.ilm',
    title: 'What "compare" actually asks for',
    sub: 'both sides, every time',
    spine: 'Pattern',
    teacherAsk: 'A pupil writes three true sentences about diffusion and stops. How many compare marks is that worth?',
    stages: [
      { title: 'Observe — read the command word',
        body: '"Compare diffusion and active transport. [4]"',
        prompt: 'Compare means BOTH sides in the same sentence — not one paragraph each.',
        action: 'We have named what compare requires — unlock the next step' },
      { title: 'Evidence — pick your points of comparison',
        body: 'Direction. Energy. What moves. Those three work for any pair of these processes.',
        prompt: 'Choose the points first. Then you cannot run out halfway.',
        action: 'We have chosen our points — unlock the next step' },
      { title: 'Pattern — write each point about BOTH',
        body: '"Diffusion moves particles down the gradient, WHEREAS active transport moves them against it."',
        prompt: 'The words whereas / but / both are what make it a comparison. Use them deliberately.',
        action: 'Each point covers both sides — unlock the next step' },
      { title: 'Conclusion — include a similarity, not only differences',
        body: '"Both move substances across a cell membrane."',
        prompt: 'Compare questions credit similarities too, and most pupils forget them entirely.',
        action: 'We have a similarity as well — unlock the last step' },
      { title: 'Explanation — check the marks against the points',
        body: 'Four marks: three differences and one similarity, each mentioning both processes.',
        prompt: 'Count your "whereas"es. If there are none, you have written two descriptions, not a comparison.' }
    ]
  },

  { key: 'compare-3', type: 'compare', slide: 'We Do 1',
    title: 'Any two of the three',
    sub: 'the same three questions work every time',
    spine: 'Application',
    teacherAsk: 'Pick any two. Which of the three questions separates them?',
    panels: [
      { label: 'OSMOSIS', scene: 'membrane', sceneOpts: {},
        alt: 'Water crossing a partially permeable membrane.' },
      { label: 'ACTIVE TRANSPORT', scene: 'activeTransport', sceneOpts: { energy: 100 },
        alt: 'Particles carried against the gradient.' }
    ],
    prompt: 'Tap each point of comparison as the class states it about BOTH.',
    differences: [
      { spot: 'What moves: water / any particle' },
      { spot: 'Direction: downhill / uphill' },
      { spot: 'Energy: none / from respiration' },
      { spot: 'Similarity: both cross a membrane' }
    ],
    explanation: 'Three differences and one similarity — four points, four marks, each one mentioning both processes. Swap either panel for diffusion and the same three questions still produce the answer.',
    caveat: 'Marks vary by paper. What does not vary is that a compare answer must address both sides of each point.'
  },

  { key: 'compare-pause', type: 'pause', slide: 'I Do 2',
    title: 'Spot the answer that is not a comparison',
    spine: 'Evaluation',
    teacherAsk: 'Read it twice before you decide.',
    ask: '"Diffusion is the movement of particles from high to low concentration. It does not need energy. Active transport needs energy." Is that a comparison?',
    options: ['Partly — only the last point compares', 'Yes, fully', 'No, not at all'],
    after: 'Look for the word that links the two sides.',
    reveal: 'Partly. The first two sentences describe diffusion alone. Only the third mentions both, and even that does not say what diffusion does differently in the same sentence. Rewritten: "Diffusion needs no energy, whereas active transport needs energy from respiration." One sentence, both sides, one clear mark.'
  }
]},

/* ======================================================================= W7 */

'SCI_L_W7_L1_RoundUp': { components: [

  { key: 'topic-zoom', type: 'zoom', slide: 'I Do 1', anchor: '.ilm',
    title: 'The whole topic, at every scale',
    sub: 'everything you have learnt lives somewhere on this journey',
    spine: 'Evidence',
    factor: 7,
    teacherAsk: 'At each level, tell me which part of Topic 1 belongs there.',
    alt: 'A continuous zoom from a leaf, through cells and a chloroplast, to the membrane and water molecules.',
    levels: [
      { name: 'a leaf', scale: '≈ 5 cm', scene: 'leaf',
        note: 'Whole organism. Too big for diffusion alone — this is why exchange surfaces exist.',
        ask: 'Which Topic 1 idea belongs at THIS scale?',
        options: ['Surface area to volume ratio', 'Magnification', 'Osmosis'] },
      { name: 'cells', scale: '≈ 50 µm', scene: 'leafCells',
        note: 'Cells. This is the scale you actually see down a light microscope — and where magnification calculations live.',
        ask: 'What do you need to state the size of anything at this scale?',
        options: ['Magnification and a unit', 'A ruler', 'Nothing'] },
      { name: 'a chloroplast', scale: '≈ 5 µm', scene: 'chloroplast',
        note: 'Sub-cellular. A light microscope can just about show one; an electron microscope shows its structure — resolution, not magnification.',
        ask: 'Why can a light microscope not show the layers inside?',
        options: ['Not enough resolution', 'Not enough magnification', 'They are invisible'] },
      { name: 'the membrane', scale: '≈ 10 nm', scene: 'membrane',
        note: 'Partially permeable. Diffusion, osmosis and active transport ALL happen here.',
        ask: 'Which of the three transport processes happen at this membrane?',
        options: ['All three', 'Only osmosis', 'Only diffusion'] },
      { name: 'molecules', scale: '≈ 0.3 nm', scene: 'molecules',
        note: 'Random movement. Diffusion and osmosis need nothing but this. Active transport needs this PLUS energy.' }
    ]
  },

  { key: 'topic-chain', type: 'chain', slide: 'We Do 1',
    title: 'One line each — no notes',
    sub: 'if you cannot say it in a line, you do not have it yet',
    spine: 'Explanation',
    teacherAsk: 'Say it before you unlock it. Then check what you said against what appears.',
    stages: [
      { title: 'Magnification',
        body: 'magnification = image size ÷ real size. It has no unit.',
        prompt: 'Say it, then unlock.',
        action: 'We said it — unlock the next one' },
      { title: 'Resolution',
        body: 'How much detail you can see — the ability to tell two close things apart. Not the same as magnification.',
        prompt: 'Say it, then unlock.',
        action: 'We said it — unlock the next one' },
      { title: 'Diffusion',
        body: 'The net movement of particles from a higher to a lower concentration, down a concentration gradient. No energy needed.',
        prompt: '"Net movement" is worth a mark on its own.',
        action: 'We said it — unlock the next one' },
      { title: 'Osmosis',
        body: 'The net movement of WATER from a dilute to a concentrated solution through a partially permeable membrane. No energy needed.',
        prompt: 'Water, and a partially permeable membrane. Both must be there.',
        action: 'We said it — unlock the last one' },
      { title: 'Active transport',
        body: 'The movement of particles AGAINST the concentration gradient, using energy from respiration.',
        prompt: 'Against, and energy from respiration. Both, every time.' }
    ]
  },

  { key: 'roundup-sim', type: 'model', slide: 'I Do 2', sim: 'microscope',
    title: 'One last look down the eyepiece',
    sub: 'can you still explain what every control does?',
    spine: 'Evaluation',
    teacherAsk: 'Change one control. Before the picture updates, say what will happen and why.',
    alt: 'The microscope simulator, revisited for the round-up.',
    start: { obj: 10, focus: 0, bright: 60 },
    tradeOff: {
      ask: 'Two weeks on: what does turning the fine focus change — magnification, or resolution?',
      options: ['Neither — it changes whether you achieve the resolution',
                'Magnification', 'Resolution'],
      after: 'Then explain your answer to your partner in one sentence.'
    }
  }
]},

'SCI_L_W7_L2_CommandWords': { components: [

  { key: 'cw-chain', type: 'chain', slide: 'I Do 1', anchor: '.ilm',
    title: 'Four command words, four shapes of answer',
    sub: 'the command word tells you the shape before you know the content',
    spine: 'Pattern',
    teacherAsk: 'Cover the topic. Just from the command word, what shape does the answer have to be?',
    stages: [
      { title: 'Describe — say WHAT',
        body: 'State what happens or what you can see. No reasons required.',
        prompt: 'A describe answer that gives reasons has not lost marks — but it has spent time it did not need to.',
        action: 'We can shape a describe answer — unlock the next' },
      { title: 'Explain — say WHY',
        body: 'Give the reason. Usually: what happens, BECAUSE ___.',
        prompt: 'If your answer contains no "because" or "so", check it is really an explanation.',
        action: 'We can shape an explain answer — unlock the next' },
      { title: 'Calculate — show WORKING',
        body: 'Equation, conversion, substitution, answer, unit. Marks live in the lines, not just the number.',
        prompt: 'Never write only the answer, however confident you are.',
        action: 'We can shape a calculate answer — unlock the next' },
      { title: 'Compare — BOTH sides',
        body: 'Every point mentions both things. Use whereas, but, both.',
        prompt: 'Two separate descriptions is the most common way to lose all four marks.',
        action: 'We can shape a compare answer — unlock the last step' },
      { title: 'And the number in brackets tells you how many points',
        body: '3 marks means three separate creditable points, not one long sentence.',
        prompt: 'Read the command word, then the marks, then start writing. In that order.' }
    ]
  },

  { key: 'cw-pause', type: 'pause', slide: 'We Do 1',
    title: 'Which command word is this answer shaped for?',
    spine: 'Evaluation',
    teacherAsk: 'Do not say the topic. Say the shape.',
    ask: '"Water moves into the potato, because there is a higher concentration of water outside the cell than inside." Which command word does this answer fit?',
    options: ['Explain', 'Describe', 'Compare', 'Calculate'],
    after: 'Find the word in the answer that decides it.',
    reveal: 'Explain — the word "because" carries the reason. Strip that clause out and you are left with "water moves into the potato", which is a describe answer. The same knowledge, two different questions; the command word decides which one you are answering.'
  },

  { key: 'cw-compare', type: 'compare', slide: 'I Do 2',
    title: 'Same content, two command words',
    sub: 'the marker is looking for different things',
    spine: 'Application',
    teacherAsk: 'Both answers are true and both are about osmosis. Which one answers "explain"?',
    panels: [
      { label: 'ANSWER 1', scene: 'osmosisChip', sceneOpts: { conc: 0, inside: 0.3 },
        alt: 'A potato chip that has gained mass in pure water.' },
      { label: 'ANSWER 2', scene: 'osmosisChip', sceneOpts: { conc: 0.8, inside: 0.3 },
        alt: 'A potato chip that has lost mass in strong sugar solution.' }
    ],
    prompt: 'Tap each feature the class can find in an answer.',
    differences: [
      { spot: 'States what happened → describe' },
      { spot: 'Gives a concentration comparison → explain' },
      { spot: 'Uses "because" → explain' },
      { spot: 'Quotes a number from the results → describe, with data' }
    ],
    explanation: 'Describe reports the change. Explain gives the concentration comparison that caused it. Quoting a figure from your results strengthens a describe answer; it does not turn it into an explanation.',
    caveat: 'These two pictures are the same model at two concentrations — they stand for the two answers rather than being the answers themselves.'
  }
]},

'SCI_L_W7_L3_ExamPractice': { components: [

  { key: 'exam-chain', type: 'chain', slide: 'I Do 1', anchor: '.ilm',
    title: 'Answering a 3-mark "explain" under exam conditions',
    sub: 'the same four checks, every time',
    spine: 'Pattern',
    teacherAsk: 'Before you write anything: what are the first two things you look at on the question?',
    stages: [
      { title: 'Observe — command word and marks, in that order',
        body: '"Explain why a root hair cell needs energy to take up mineral ions. [3]"',
        prompt: 'Explain. Three marks. Three reasons.',
        action: 'We have the command word and the mark count — unlock the next step' },
      { title: 'Evidence — point 1: the concentrations',
        body: 'There are fewer mineral ions in the soil than inside the root hair cell.',
        prompt: 'Say which side has more. Vague answers lose this mark.',
        action: 'Point 1 is down — unlock the next step' },
      { title: 'Pattern — point 2: the direction',
        body: 'So the ions have to move against the concentration gradient.',
        prompt: '"Against the gradient" is the phrase the mark scheme is looking for.',
        action: 'Point 2 is down — unlock the next step' },
      { title: 'Conclusion — point 3: the cost',
        body: 'Movement against a gradient cannot happen on its own, so it needs energy from respiration.',
        prompt: '"From respiration" — not just "energy".',
        action: 'Point 3 is down — unlock the last step' },
      { title: 'Explanation — read it back and count',
        body: 'Three sentences, three marks, in a logical order.',
        prompt: 'Point at each mark on the page. If you cannot point at three, add the missing one now.' }
    ]
  },

  { key: 'exam-calc', type: 'model', slide: 'We Do 1', sim: 'magnification',
    title: 'Check your calculation against the model',
    sub: 'work it out first — then set the model and see',
    spine: 'Test',
    teacherAsk: 'Work it out on paper BEFORE you touch the sliders. Then set them and check.',
    alt: 'The magnification model, used as a self-check after working on paper.',
    start: { obj: 40, real: 25 },
    opening: 'Paper first. The model is the marker, not the method.',
    tradeOff: {
      ask: 'A cell is 25 µm across, viewed with a ×10 eyepiece and a ×40 objective. How wide is the image?',
      options: ['10 mm', '1 mm', '100 mm'],
      after: 'Now set the model to ×40 and 25 µm and read the image size.'
    },
    caveat: 'The model rounds its readouts. If your paper answer differs in the last digit, check your rounding before assuming you are wrong.'
  },

  { key: 'weak-answer', type: 'pause', slide: 'I Do 2',
    title: 'What is missing from this answer?',
    spine: 'Evaluation',
    teacherAsk: 'It is not wrong. It is incomplete. Find what is missing.',
    ask: '"Active transport moves particles into the cell and it needs energy." Worth 3 marks?',
    options: ['No — the direction relative to the gradient is missing',
              'Yes, it says everything', 'No — energy is wrong'],
    after: 'Compare it with the three points you built earlier.',
    reveal: 'Two of three at best. It says particles move in, and that energy is needed — but it never says AGAINST the concentration gradient, and it does not say the energy comes from respiration. Those are the two phrases the mark scheme is actually looking for.'
  }
]}

};
