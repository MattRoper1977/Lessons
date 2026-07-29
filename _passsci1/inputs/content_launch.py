# -*- coding: utf-8 -*-
"""
LAUNCH science — Autumn 1, weeks 3-7 (post-baseline).
Spine: Edexcel GCSE (9-1) Biology 1BI0 FOUNDATION tier (grades 1-5), Paper 1,
Topic 1 'Key concepts in biology'. Combined Science 1SC0 F route where appropriate.
Theme: Identity & Belonging.

SCOPE DECISIONS TAKEN, FLAGGED FOR MATT:
  * CORE ROUTE ONLY. The SoW carries a SECOND science column -- the optional IGCSE
    4BI1/4CH1/4PH1 route, "eligible students only, confirmed by science lead + SENCo".
    Its Aut1 W3-W7 is a chemistry chain (separation, ionic bonding, covalent bonding,
    formulae & reacting masses, the mole). That is a fifth and sixth suite, not part of
    "three pathways", and it is gated on an eligibility decision that has not been made.
    NOT BUILT. Raised as a decision.
  * NO MARK SCHEMES, NO BAND DESCRIPTORS. Standing estate rule. W7 carries exam-style
    questions with mark allocations (which appear on the paper itself) and STAFF-SIDE
    indicative answers. It does not author grade boundaries or level descriptors.
  * ASSESSMENT LIVES ON PYTHONANYWHERE. Per the Pass SL ruling, this year's LAUNCH
    science assessments are built there. W7 revises and points at that assessment;
    it does not embed a summative test.

HOUSE RULES BAKED IN:
  * Icon + label + colour on every classification. Never colour alone.
  * Answer keys STAFF-SIDE. Exit answers never on a pupil surface.
  * TA brief opens with ONE rule.
  * Maths scaffolds are provided at every tier -- the SoW names this explicitly.
"""

STRAND = "Science"
PATHWAY = "LAUNCH"
COLOUR = "#7A5C9E"          # LAUNCH science violet; distinct from BUILD LI #7E6BA6
SPINE = "Edexcel GCSE Biology 1BI0 Foundation \u00b7 Paper 1 \u00b7 Topic 1"
AWARD = "Pearson Edexcel GCSE (9\u20131) Biology 1BI0 (Foundation, grades 1\u20135); GCSE Combined Science 1SC0 F where appropriate; AQA UAS science units"
THEME = "Identity &amp; Belonging"
SLOT_WEEKS = 7
SENSORY = ("Microscope and core-practical work involves close focus, glassware and sometimes "
           "queueing for equipment. Agree who handles glass before the lesson. A pupil who "
           "records, calculates or photographs the result is doing assessed work \u2014 handling "
           "the scalpel is not the science.")

LESSONS = [

# ---------------------------------------------------------------- W3
dict(
  week=3, slug="SCI_L_W3_Magnification",
  title="Calculating Magnification",
  sow="Aut1\u00b7W3 \u2014 Calculate magnification (links Maths; record in spreadsheet).",
  lo="I can calculate magnification, image size and actual size, and convert between mm and \u00b5m.",
  sc=[
    "I can state the magnification equation and rearrange it.",
    "I can convert between millimetres and micrometres correctly.",
    "I can calculate total magnification from the two lenses.",
  ],
  ko_vocab=[
    ("magnification", "How many times bigger the image is than the real object."),
    ("image size", "The size of the object as it appears (measured on the picture)."),
    ("actual size", "The real size of the object."),
    ("micrometre (\u00b5m)", "One thousandth of a millimetre. 1 mm = 1000 \u00b5m."),
    ("resolution", "The smallest gap that can still be seen as two separate things."),
  ],
  ko_facts=[
    "magnification = image size \u00f7 actual size",
    "Rearranged: actual size = image size \u00f7 magnification; image size = actual size \u00d7 magnification.",
    "Total magnification = eyepiece lens \u00d7 objective lens. \u00d710 eyepiece with \u00d740 objective = \u00d7400.",
    "1 mm = 1000 \u00b5m. 1 \u00b5m = 0.001 mm.",
    "Magnification has NO units \u2014 it is a ratio. Write \u00d7400, not 400 mm.",
    "Light microscopes magnify to about \u00d71500; electron microscopes reach far higher and also give better resolution.",
  ],
  misconceptions=[
    ("Magnification has units.",
     "It is a ratio of two lengths, so the units cancel. \u00d7400, never 400 mm."),
    ("Bigger magnification always means a better image.",
     "Not without resolution. Blow up a blurred photo and you get a bigger blur."),
    ("You can mix mm and \u00b5m in one calculation.",
     "Convert first, every time. This is where most marks are lost on this topic."),
  ],
  arrival=dict(
    supported="Write the magnification equation from the word bank.",
    standard="Write the magnification equation and rearrange it for actual size.",
    stretch="Convert 0.05 mm into micrometres, and state the equation you would use to find magnification.",
  ),
  glance=["Equation and rearrangement", "Unit conversion", "Total magnification"],
  ido1=dict(
    heading="Watch me work through one",
    think=("Image is 40 mm across. Actual cell is 0.1 mm. First question I always ask: are the "
           "units the same? Yes, both millimetres, so I can divide. 40 \u00f7 0.1 = 400. Magnification "
           "\u00d7400. No units on the answer. If they had NOT matched, converting would have been "
           "step one, before anything else."),
    illuminator=("Formula triangle drawn with IMAGE SIZE on top, MAGNIFICATION and ACTUAL SIZE "
                 "below, each labelled in full words plus a symbol tag. Beside it, a conversion "
                 "ladder: 'mm \u2014\u00d71000\u2192 \u00b5m' and '\u00b5m \u2014\u00f71000\u2192 mm', "
                 "with the direction written out. All labels horizontal, no colour-only coding."),
  ),
  wedo1=dict(
    heading="Work it out before you tap",
    prompt="Pen down, answer in your head, then check.",
    items=[
      ("Image 30 mm, actual 0.15 mm. Magnification?", "\u00d7200"),
      ("Magnification \u00d7500, image 25 mm. Actual size?", "0.05 mm (= 50 \u00b5m)"),
      ("Eyepiece \u00d710, objective \u00d740. Total?", "\u00d7400"),
      ("Convert 0.02 mm to \u00b5m", "20 \u00b5m"),
      ("Convert 750 \u00b5m to mm", "0.75 mm"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("Set every calculation out the same way, because the method carries marks even when "
           "the answer slips: equation, then units check, then substitution, then answer with "
           "the multiplication sign. Four lines, every time."),
    capture="Photograph the pupil's four-line working for one calculation \u2014 the layout is the evidence, not just the answer.",
  ),
  wedo2=dict(
    heading="Spot the error",
    pills=[
      ("Magnification = \u00d7400", "CORRECT"),
      ("Magnification = 400 mm", "ERROR \u2014 magnification has no units"),
      ("40 mm \u00f7 100 \u00b5m = 0.4", "ERROR \u2014 units not converted first"),
      ("Actual = image \u00f7 magnification", "CORRECT"),
      ("Actual = image \u00d7 magnification", "ERROR \u2014 rearranged the wrong way"),
    ],
    wagoll=("magnification = image size \u00f7 actual size. Both in mm: 40 \u00f7 0.1. "
            "magnification = \u00d7400."),
  ),
  independent=dict(
    supported="Six calculations with the equation and a worked example printed on the sheet. Units already matched.",
    standard="Eight calculations including two that need unit conversion first, plus one rearrangement.",
    stretch="Eight calculations including conversions and rearrangements, then record your results in the spreadsheet and add a column showing total magnification for each lens pair.",
  ),
  lundy=dict(
    space="Calculation under pressure is its own barrier. The equation stays on the board all lesson \u2014 you are not being tested on remembering it today.",
    voice="If you think my worked example is wrong, stop me. Twice a year somebody is right.",
    audience="Your spreadsheet goes into your Topic 1 folder and is revisited at W7.",
    influence="The class decides which calculation type gets extra practice before the assessment.",
  ),
  exit=dict(
    supported="Write the magnification equation.",
    standard="A cell is 0.2 mm. The image is 60 mm. Calculate the magnification.",
    stretch="An image is 45 mm wide at \u00d7900. Give the actual size in \u00b5m.",
  ),
  exit_key=["magnification = image size \u00f7 actual size",
            "\u00d7300",
            "45 \u00f7 900 = 0.05 mm = 50 \u00b5m"],
  witness=[
    "Stated and rearranged the magnification equation.",
    "Converted correctly between mm and \u00b5m.",
    "Calculated total magnification from two lenses.",
  ],
  ta_rule="ONE RULE: check the units match BEFORE dividing. That single check is most of the marks on this topic.",
  ta_notes=[
    "Calculators out from the start. Withholding them does not build fluency here, it builds avoidance.",
    "The four-line layout is the habit being built. Praise the layout even when the arithmetic is wrong.",
  ],
  coldcall=[
    ("Watch me work through one", "What was my first check, before any dividing?"),
    ("Work it out before you tap", "Convert 0.02 mm to micrometres."),
    ("Spot the error", "Why is '400 mm' wrong?"),
  ],
  uas="AQA UAS: 'Using a microscope'; 'Scientific calculations'.",
),

# ---------------------------------------------------------------- W4
dict(
  week=4, slug="SCI_L_W4_Diffusion",
  title="Diffusion",
  sow="Aut1\u00b7W4 \u2014 Explain diffusion.",
  lo="I can explain diffusion and the factors that affect its rate.",
  sc=[
    "I can define diffusion using the words 'net movement' and 'concentration gradient'.",
    "I can name three factors that change the rate of diffusion.",
    "I can apply diffusion to a real example in the body.",
  ],
  ko_vocab=[
    ("diffusion", "The net movement of particles from a higher to a lower concentration."),
    ("concentration gradient", "The difference in concentration between two areas."),
    ("net movement", "The overall movement, once movement in both directions is counted."),
    ("passive", "Requiring no energy from the cell."),
    ("surface area", "The total area available for particles to cross."),
  ],
  ko_facts=[
    "Diffusion is the net movement of particles from high to low concentration, DOWN the gradient.",
    "It is passive \u2014 it needs no energy from the cell.",
    "Rate increases with: a steeper concentration gradient, higher temperature, larger surface area.",
    "Rate decreases with: a longer diffusion distance (thicker membrane or barrier).",
    "Particles still move both ways. 'Net' means the overall balance is one way.",
    "Examples: oxygen into the blood in the alveoli; carbon dioxide out; urea into the blood.",
  ],
  misconceptions=[
    ("Particles only move one way in diffusion.",
     "They move randomly in all directions. The NET result is down the gradient."),
    ("Diffusion needs energy.",
     "No. That is active transport, which is week 6. Diffusion is free."),
    ("Diffusion stops when it is done.",
     "Movement continues at equilibrium; there is simply no net change."),
  ],
  arrival=dict(
    supported="Complete from the word bank: diffusion is the net movement of particles from ____ to ____ concentration.",
    standard="Write a definition of diffusion using the words 'net movement'.",
    stretch="Write a definition of diffusion and name one factor that speeds it up.",
  ),
  glance=["Define it precisely", "Three rate factors", "Apply it to the lungs"],
  ido1=dict(
    heading="Watch me define it properly",
    think=("Weak version: 'diffusion is when things spread out'. That earns very little. "
           "Now the marking version: 'the NET movement of particles from an area of HIGHER "
           "concentration to an area of LOWER concentration, DOWN a concentration gradient'. "
           "Three technical phrases. Every one of them is doing work."),
    illuminator=("Two-chamber diagram separated by a membrane. Left chamber densely dotted, "
                 "tagged '\u25cf HIGH CONCENTRATION'; right chamber sparsely dotted, tagged "
                 "'\u25cb LOW CONCENTRATION'. Arrows both directions, the net arrow drawn thicker "
                 "and labelled 'NET MOVEMENT'. Below, three rate-factor tags: "
                 "'\u2191 STEEPER GRADIENT', '\u2191 HIGHER TEMPERATURE', '\u2191 MORE SURFACE AREA'."),
  ),
  wedo1=dict(
    heading="Faster or slower?",
    prompt="Decide before you tap.",
    items=[
      ("Steeper concentration gradient", "FASTER"),
      ("Higher temperature", "FASTER \u2014 particles have more kinetic energy"),
      ("Thicker membrane", "SLOWER \u2014 longer distance to travel"),
      ("Larger surface area", "FASTER \u2014 more room to cross"),
      ("Adding energy from the cell", "NO EFFECT \u2014 diffusion is passive"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("Applying it is where the marks are. Alveoli: 'Oxygen diffuses from the alveolus into "
           "the blood because oxygen concentration is higher in the alveolus. The wall is one cell "
           "thick, so the diffusion distance is short, which increases the rate.' "
           "Direction, reason, adaptation."),
    capture="Photograph the pupil's annotated alveolus diagram with all three adaptations labelled.",
  ),
  wedo2=dict(
    heading="Diffusion or not?",
    pills=[
      ("Oxygen into the blood at the alveoli", "DIFFUSION"),
      ("Carbon dioxide out of a cell", "DIFFUSION"),
      ("Smell spreading across a room", "DIFFUSION"),
      ("Glucose pumped into a root hair against the gradient", "NOT DIFFUSION \u2014 that is active transport"),
      ("Water across a partially permeable membrane", "OSMOSIS \u2014 a special case, next week"),
    ],
    wagoll=("Oxygen diffuses from the alveolus into the blood because there is a higher "
            "concentration of oxygen in the alveolus than in the blood. The alveolus wall is one "
            "cell thick, so the diffusion distance is short and the rate is high."),
  ),
  independent=dict(
    supported="Label the alveolus diagram and complete three gap-fill definition sentences from the word bank.",
    standard="Label and annotate the alveolus diagram, then answer three application questions on rate factors.",
    stretch="Annotate the diagram, answer the application questions, and explain why a person with damaged alveoli has reduced gas exchange, referring to surface area and distance.",
  ),
  lundy=dict(
    space="Lung and breathing content can land close to home for some pupils. You can work from the diagram and skip the discussion.",
    voice="If a definition on the board does not make sense, say so \u2014 precision is the whole point of today.",
    audience="Your annotated diagram goes into the Topic 1 folder for the W7 review.",
    influence="The class picks the real-world example we use for the exam-style practice at W7.",
  ),
  exit=dict(
    supported="Diffusion moves particles from ____ to ____ concentration.",
    standard="Name two factors that increase the rate of diffusion.",
    stretch="Explain why a thin membrane increases the rate of diffusion.",
  ),
  exit_key=["high, low",
            "any two of: steeper gradient, higher temperature, larger surface area",
            "A shorter distance means particles cross in less time, so the rate is higher."],
  witness=[
    "Defined diffusion using 'net movement' and 'concentration gradient'.",
    "Named three factors affecting rate.",
    "Applied diffusion to gas exchange in the alveoli.",
  ],
  ta_rule="ONE RULE: the words 'net movement' and 'down the concentration gradient' are what earn the mark. Insist on them.",
  ta_notes=[
    "'Things spread out' is not a definition. Push every pupil to the technical phrasing at their tier.",
    "Do not preview active transport today \u2014 W6 lands better if diffusion is secure as the free, passive one first.",
  ],
  coldcall=[
    ("Watch me define it properly", "Which three phrases were doing the work?"),
    ("Faster or slower?", "Does adding energy speed diffusion up?"),
    ("Diffusion or not?", "Why is the root hair example not diffusion?"),
  ],
  uas="AQA UAS: 'Cells and transport'.",
),

# ---------------------------------------------------------------- W5
dict(
  week=5, slug="SCI_L_W5_Osmosis_CP",
  title="Osmosis \u2014 Core Practical",
  sow="Aut1\u00b7W5 \u2014 Explain osmosis (core practical; data-logging).",
  lo="I can define osmosis and investigate it using the core practical.",
  sc=[
    "I can define osmosis, including 'partially permeable membrane'.",
    "I can calculate percentage change in mass.",
    "I can explain my results in terms of water concentration.",
  ],
  ko_vocab=[
    ("osmosis", "The net movement of WATER from a dilute solution to a concentrated solution through a partially permeable membrane."),
    ("partially permeable", "Lets some particles through but not others."),
    ("dilute", "More water, less solute."),
    ("concentrated", "Less water, more solute."),
    ("percentage change", "(change \u00f7 original) \u00d7 100."),
  ],
  ko_facts=[
    "Osmosis is diffusion of WATER only, and only through a partially permeable membrane.",
    "Water moves from where there is MORE water to where there is LESS water.",
    "percentage change in mass = (final mass \u2212 initial mass) \u00f7 initial mass \u00d7 100",
    "Potato in pure water: gains mass. Potato in concentrated sugar solution: loses mass.",
    "The concentration where mass does not change is the concentration inside the potato cells.",
    "A negative percentage change means the sample lost mass. Report it as negative; do not drop the sign.",
  ],
  misconceptions=[
    ("Osmosis moves sugar.",
     "Osmosis moves WATER. The sugar cannot cross the membrane, which is why water does."),
    ("Water moves to where there is more sugar because sugar attracts it.",
     "Reframe by water: water moves from where water is plentiful to where it is scarce."),
    ("A mass loss means the experiment failed.",
     "A loss is a valid result and tells you the solution outside was more concentrated than inside."),
  ],
  arrival=dict(
    supported="Complete from the word bank: osmosis is the movement of ____ through a ____ membrane.",
    standard="Write a definition of osmosis.",
    stretch="Write a definition of osmosis and state how it differs from diffusion.",
  ),
  glance=["Define osmosis", "Run the core practical", "Calculate % change"],
  ido1=dict(
    heading="Watch me set the practical up",
    think=("Same potato, same corer, same length, blotted the same way \u2014 all controls. "
           "The ONE thing changing is the sugar concentration. Initial mass recorded to two "
           "decimal places BEFORE anything goes in the tube, because I cannot get it back "
           "afterwards. Then thirty minutes. Then blot identically and re-weigh."),
    illuminator=("Core-practical set-up diagram: five labelled tubes across the concentration "
                 "range, potato cylinder in each, each tube tagged with its concentration in words. "
                 "Beside it a results table with columns 'INITIAL MASS (g)', 'FINAL MASS (g)', "
                 "'CHANGE (g)', '% CHANGE'. A tag reads 'BLOT THE SAME WAY EVERY TIME \u2014 "
                 "THIS IS THE BIGGEST SOURCE OF ERROR'."),
  ),
  wedo1=dict(
    heading="Predict the direction",
    prompt="Say gain, lose or no change before you tap.",
    items=[
      ("Potato in pure water", "GAINS mass \u2014 water moves in"),
      ("Potato in very concentrated sugar solution", "LOSES mass \u2014 water moves out"),
      ("Potato in a solution matching its own cells", "NO CHANGE \u2014 no net movement"),
      ("Does sugar cross the membrane?", "No \u2014 it is partially permeable"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("The calculation, out loud: initial 4.20 g, final 4.62 g. Change = +0.42 g. "
           "Percentage = 0.42 \u00f7 4.20 \u00d7 100 = +10%. Divide by the INITIAL mass, not the final. "
           "That is the classic dropped mark."),
    capture="Photograph the pupil's completed results table with the % change column filled in.",
  ),
  wedo2=dict(
    heading="Explain the result",
    pills=[
      ("Gained mass in pure water", "Water moved IN \u2014 higher water concentration outside"),
      ("Lost mass in strong sugar solution", "Water moved OUT \u2014 lower water concentration outside"),
      ("Dividing by final mass", "ERROR \u2014 always divide by the initial mass"),
      ("Dropping the minus sign", "ERROR \u2014 a loss must be reported as negative"),
      ("Sugar moved into the potato", "NOT TRUE \u2014 the membrane does not let sugar through"),
    ],
    wagoll=("The potato in pure water gained mass because the water concentration outside the "
            "cells was higher than inside, so water moved in by osmosis through the partially "
            "permeable cell membranes. Percentage change = (4.62 \u2212 4.20) \u00f7 4.20 \u00d7 100 = +10%."),
  ),
  independent=dict(
    supported="Run two concentrations with the table pre-drawn and the percentage formula printed. Complete the calculation with the worked example alongside.",
    standard="Run the full concentration range, complete the table, calculate percentage change for each.",
    stretch="Run the full range, calculate percentage change, plot the results, and use the graph to estimate the concentration inside the potato cells.",
  ),
  lundy=dict(
    space="This practical has a thirty-minute wait built in. The wait is not empty time \u2014 the calculation practice happens in it.",
    voice="If your result disagrees with the class trend, we look at your method before we look at your number.",
    audience="Your results table is core-practical evidence and goes into the Topic 1 folder.",
    influence="The class agrees the blotting protocol \u2014 and everyone then has to follow it.",
  ),
  exit=dict(
    supported="Osmosis is the movement of ______.",
    standard="A cylinder goes from 5.00 g to 4.50 g. Calculate the percentage change.",
    stretch="Explain why a potato in concentrated sugar solution loses mass.",
  ),
  exit_key=["water (through a partially permeable membrane)",
            "\u221210%",
            "Water concentration outside is lower than inside, so water leaves the cells by osmosis through the partially permeable membrane."],
  witness=[
    "Defined osmosis including 'partially permeable membrane'.",
    "Carried out the core practical following the agreed controls.",
    "Calculated percentage change in mass correctly.",
  ],
  ta_rule="ONE RULE: divide by the INITIAL mass. That is the single most-dropped mark in this practical.",
  ta_notes=[
    "Cork borers and scalpels: agree who handles them before the lesson. A pupil who weighs, records and calculates has met the outcome without touching a blade.",
    "Initial masses must be recorded before anything enters a tube. Once it is in, that data is gone.",
    "Blotting technique is the dominant error source. Demonstrate it once, agree it, hold everyone to it.",
  ],
  coldcall=[
    ("Watch me set the practical up", "Which mass do I record first, and why does it matter?"),
    ("Predict the direction", "What happens in pure water?"),
    ("Explain the result", "Do we divide by initial or final mass?"),
  ],
  uas="AQA UAS: 'Cells and transport'; 'Carrying out a practical investigation'.",
),

# ---------------------------------------------------------------- W6
dict(
  week=6, slug="SCI_L_W6_Active_Transport",
  title="Active Transport",
  sow="Aut1\u00b7W6 \u2014 Explain active transport.",
  lo="I can explain active transport and distinguish it from diffusion and osmosis.",
  sc=[
    "I can state that active transport moves substances AGAINST the concentration gradient.",
    "I can state that it requires energy from respiration.",
    "I can compare all three transport processes.",
  ],
  ko_vocab=[
    ("active transport", "Movement of substances against the concentration gradient, using energy."),
    ("against the gradient", "From lower concentration to higher concentration."),
    ("carrier protein", "A protein in the membrane that moves the substance across."),
    ("respiration", "The reaction that releases the energy active transport needs."),
    ("mitochondria", "Where respiration happens; cells doing lots of active transport have many."),
  ],
  ko_facts=[
    "Active transport moves substances from LOW to HIGH concentration \u2014 against the gradient.",
    "It requires energy released by respiration.",
    "It uses carrier proteins in the cell membrane.",
    "Root hair cells absorb mineral ions from dilute soil water by active transport.",
    "The small intestine absorbs glucose into the blood by active transport when blood glucose is already higher.",
    "Cells specialised for active transport contain many mitochondria.",
  ],
  misconceptions=[
    ("Active transport is just fast diffusion.",
     "Direction is the difference, not speed. Diffusion goes down the gradient; this goes up it."),
    ("Active transport needs energy because it is hard work.",
     "It needs energy because it goes AGAINST the natural direction of movement."),
    ("Any cell can do active transport at any rate.",
     "It depends on respiration. No oxygen or no glucose means the rate falls."),
  ],
  arrival=dict(
    supported="Complete from the word bank: active transport moves substances ____ the concentration gradient and needs ____.",
    standard="Write one difference between diffusion and active transport.",
    stretch="Write two differences between diffusion and active transport.",
  ),
  glance=["Against the gradient", "Energy from respiration", "Compare all three"],
  ido1=dict(
    heading="Watch me compare the three",
    think=("Three columns, three questions each time. Which way relative to the gradient? "
           "Does it need energy? What is moving? Diffusion: down, no, any particle. "
           "Osmosis: down, no, water only, and it needs the partially permeable membrane. "
           "Active transport: UP, yes, and it needs carrier proteins. Fill that table and "
           "you can answer any comparison question they ask."),
    illuminator=("Three-column comparison diagram, each column headed with icon + word: "
                 "'\u2193 DIFFUSION', '\u2193 OSMOSIS (WATER)', '\u2191 ACTIVE TRANSPORT'. Rows: "
                 "direction, energy needed, what moves, membrane needed. Beside it a root hair "
                 "cell with mitochondria labelled 'ENERGY FROM RESPIRATION'. Labels horizontal."),
  ),
  wedo1=dict(
    heading="Which process?",
    prompt="Decide before you tap.",
    items=[
      ("Oxygen into the blood at the alveoli", "\u2193 Diffusion"),
      ("Water into a root hair cell", "\u2193 Osmosis"),
      ("Mineral ions into a root hair from dilute soil", "\u2191 Active transport"),
      ("Glucose from the small intestine into higher-concentration blood", "\u2191 Active transport"),
      ("Carbon dioxide out of a cell", "\u2193 Diffusion"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("Answer shape for the classic question: 'Mineral ions move into the root hair cell by "
           "active transport because their concentration is HIGHER inside the cell than in the "
           "soil water. Moving against the gradient requires energy, which is released by "
           "respiration in the mitochondria.' Direction, then why energy is needed, then source."),
    capture="Photograph the pupil's completed three-column comparison table.",
  ),
  wedo2=dict(
    heading="True or false?",
    pills=[
      ("Active transport needs energy", "TRUE"),
      ("Diffusion needs energy", "FALSE"),
      ("Active transport moves substances up the gradient", "TRUE"),
      ("Active transport is just faster diffusion", "FALSE \u2014 the direction is what differs"),
      ("Cells doing active transport have many mitochondria", "TRUE"),
    ],
    wagoll=("Root hair cells absorb mineral ions by active transport because the concentration of "
            "ions is already higher inside the cell than in the soil. Moving them against the "
            "concentration gradient requires energy released by respiration, which is why root "
            "hair cells contain many mitochondria."),
  ),
  independent=dict(
    supported="Complete the three-column comparison table from the word bank, then label the root hair cell.",
    standard="Complete the comparison table unaided, label the root hair cell, and answer two application questions.",
    stretch="Complete the table, answer the application questions, and explain what would happen to mineral uptake if a plant's roots were waterlogged and short of oxygen.",
  ),
  lundy=dict(
    space="Three processes at once is a genuine memory load. The comparison table stays visible all lesson \u2014 that is deliberate.",
    voice="If you can defend a different answer on the sorting task, defend it. Some of these are genuinely close.",
    audience="Your comparison table goes into the Topic 1 folder and is the core revision tool at W7.",
    influence="The class decides which of the three processes gets the extra practice next lesson.",
  ),
  exit=dict(
    supported="Active transport moves substances ______ the concentration gradient.",
    standard="Why does active transport need energy?",
    stretch="Explain why root hair cells contain many mitochondria.",
  ),
  exit_key=["against / up",
            "Because it moves substances against the concentration gradient, which does not happen naturally.",
            "They carry out a lot of active transport, which needs energy from respiration, and mitochondria are where respiration happens."],
  witness=[
    "Stated that active transport works against the concentration gradient.",
    "Linked the energy requirement to respiration.",
    "Compared diffusion, osmosis and active transport correctly.",
  ],
  ta_rule="ONE RULE: the difference is DIRECTION, not speed. Against the gradient means energy is needed.",
  ta_notes=[
    "This is the lesson where the three processes get confused. The comparison table is the intervention \u2014 keep it in front of every pupil.",
    "The waterlogging question in the stretch tier links to respiration, which is not taught until later. Accept 'no oxygen means less energy' as the reasoning.",
  ],
  coldcall=[
    ("Watch me compare the three", "Which one moves water only?"),
    ("Which process?", "Why is the mineral ion example not diffusion?"),
    ("True or false?", "Is active transport just faster diffusion?"),
  ],
  uas="AQA UAS: 'Cells and transport'.",
),

# ---------------------------------------------------------------- W7
dict(
  week=7, slug="SCI_L_W7_Topic1_Review",
  title="Topic 1 Review and Exam Technique",
  sow="Aut1\u00b7W7 \u2014 Topic 1 review &amp; exam-style questions.",
  lo="I can answer exam-style questions on Topic 1 using the correct command word.",
  sc=[
    "I can say what 'describe', 'explain' and 'calculate' each require.",
    "I can answer a calculation question showing full working.",
    "I can identify what is missing from a weak answer.",
  ],
  ko_vocab=[
    ("describe", "Say what happens. No reason needed."),
    ("explain", "Say WHY it happens. The word 'because' usually belongs in your answer."),
    ("calculate", "Work out a number. Show your working and give the unit."),
    ("state", "Give a short fact. One line is enough."),
    ("compare", "Give similarities AND differences, both sides named."),
  ],
  ko_facts=[
    "Marks usually match the number of points needed. A 3-mark question wants three separate points.",
    "'Explain' answers without a reason score low no matter how neat they are.",
    "Calculations: show working. Method marks survive an arithmetic slip.",
    "Magnification has no unit. Every other quantity does.",
    "'Compare' means both sides. Writing only about one scores half at best.",
  ],
  misconceptions=[
    ("A longer answer scores more.",
     "Marks follow points, not length. Three clear points beat a paragraph of restatement."),
    ("If you cannot finish a calculation, leave it blank.",
     "Write the equation and substitute. Method marks are real marks."),
    ("Describe and explain mean the same thing.",
     "Describe = what. Explain = why. Different questions, different marks."),
  ],
  arrival=dict(
    supported="Match the command word to what it asks: describe / explain / calculate.",
    standard="Write what 'explain' requires that 'describe' does not.",
    stretch="Write what 'describe', 'explain' and 'compare' each require.",
  ),
  glance=["Command words", "Working earns marks", "Fix a weak answer"],
  ido1=dict(
    heading="Watch me answer a 3-mark 'explain'",
    think=("'Explain why oxygen diffuses into the blood at the alveoli. [3]' Three marks, so I am "
           "hunting three points. One: higher oxygen concentration in the alveolus than the blood. "
           "Two: so oxygen diffuses down the concentration gradient. Three: the wall is one cell "
           "thick so the distance is short and the rate is high. Three points, three marks. "
           "I did not write a paragraph, I wrote three reasons."),
    illuminator=("Command-word reference card drawn as a table: each command word with icon + "
                 "word + what the answer must contain + a one-line worked example. A second panel "
                 "shows a 3-mark answer with each scoring point bracketed and numbered 1, 2, 3."),
  ),
  wedo1=dict(
    heading="What does the question want?",
    prompt="Name the command word's demand before you tap.",
    items=[
      ("Describe what happens to a potato in pure water. [2]", "What happens \u2014 no reason required"),
      ("Explain why it gains mass. [3]", "Reasons \u2014 three of them"),
      ("Calculate the percentage change. [2]", "Working plus answer"),
      ("Compare diffusion and active transport. [4]", "Both sides \u2014 similarities and differences"),
      ("State the magnification equation. [1]", "One line, no explanation needed"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("Take a weak answer and repair it in front of the class. 'It goes in because of osmosis' "
           "\u2014 that names the process but gives no reason, so it scores one at most. Add the "
           "water-concentration comparison and the membrane, and the same sentence reaches three."),
    capture="Photograph the pupil's improved version alongside the original weak answer \u2014 the pair shows the progress.",
  ),
  wedo2=dict(
    heading="What is missing?",
    pills=[
      ("'It spreads out.' (Explain diffusion, 3 marks)", "MISSING: net movement, gradient, direction"),
      ("'400' (Calculate magnification, 2 marks)", "MISSING: working \u2014 and check whether a unit is needed"),
      ("'Active transport is different.' (Compare, 4 marks)", "MISSING: both sides, named, with detail"),
      ("'Water moves in.' (Explain mass gain, 3 marks)", "MISSING: why \u2014 water concentration comparison and the membrane"),
      ("A neat three-paragraph answer to a 1-mark 'state'", "NOT MISSING ANYTHING \u2014 but it cost time it did not need to"),
    ],
    wagoll=("Explain why oxygen diffuses into the blood at the alveoli. [3] \u2014 "
            "The concentration of oxygen is higher in the alveolus than in the blood (1), "
            "so oxygen diffuses down the concentration gradient (1). The alveolus wall is one "
            "cell thick, so the diffusion distance is short and the rate is high (1)."),
  ),
  independent=dict(
    supported="Six exam-style questions with the command word highlighted and sentence starters provided.",
    standard="Eight exam-style questions across Topic 1, including one calculation and one 'explain'.",
    stretch="Eight exam-style questions including a 4-mark compare, then review two of your own answers and state what would gain the missing mark.",
  ),
  lundy=dict(
    space="Exam-style work raises the temperature for some people. This is practice, it is not the assessment \u2014 the assessment is separate and you will know when it is happening.",
    voice="Challenge a question that seems unfair. Sometimes the question is the problem.",
    audience="Your improved answers go into the Topic 1 folder and are the revision set before the assessment.",
    influence="The class chooses which two question types get retaught before the Topic 1 assessment.",
  ),
  exit=dict(
    supported="What does 'calculate' ask you to show as well as the answer?",
    standard="What must an 'explain' answer contain that a 'describe' answer does not?",
    stretch="A 4-mark 'compare' question \u2014 describe the structure of a full-mark answer.",
  ),
  exit_key=["your working",
            "a reason \u2014 why it happens, not just what happens",
            "Both processes named, at least one similarity and differences addressed on both sides, roughly four distinct points."],
  witness=[
    "Distinguished describe, explain and calculate.",
    "Showed full working on a calculation question.",
    "Identified the missing element in a weak answer.",
  ],
  ta_rule="ONE RULE: count the marks, then find that many separate points. Length is not the target.",
  ta_notes=[
    "NO mark schemes or grade descriptors are used or displayed. Feedback is 'this point is missing', never a predicted grade.",
    "The Topic 1 assessment is on PythonAnywhere and is separate from this lesson. Say so plainly \u2014 pupils manage practice better when they know it is not the real thing.",
    "Indicative answers for all eight questions are in the staff section of the print pack.",
  ],
  coldcall=[
    ("Watch me answer a 3-mark 'explain'", "How many separate points was I hunting?"),
    ("What does the question want?", "What does 'compare' need that 'describe' does not?"),
    ("What is missing?", "What is missing from 'it spreads out'?"),
  ],
  uas="AQA UAS: 'Cells and transport'; revision and exam technique.",
),
]
