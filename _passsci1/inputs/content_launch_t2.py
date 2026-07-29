# -*- coding: utf-8 -*-
"""
LAUNCH science — Topic 2 (SoW W4 Diffusion), 3-lesson arc: Discover -> Use -> Master.
L1 Discover is the authored seed. L2 Use applies diffusion to gas exchange and uses the
breath/limewater CO2 evidence (from the read-only biology/ reference), upgraded so pupils
record and the TA runs a defined station. L3 Master is exam technique for diffusion.
No mark schemes / grade descriptors (UAS). Real command words. Icon+label+colour.
"""

STRAND = "Science"
PATHWAY = "LAUNCH"
COLOUR = "#7A5C9E"
SPINE = "Edexcel GCSE Biology 1BI0 Foundation · Paper 1 · Topic 1"
AWARD = ("Pearson Edexcel GCSE (9–1) Biology 1BI0 (Foundation, grades 1–5); "
         "GCSE Combined Science 1SC0 F where appropriate; AQA UAS science units")
THEME = "Identity &amp; Belonging"
SLOT_WEEKS = 7
SENSORY = ("Breath and exercise work can be personal and physical. Nobody is made to exercise or "
           "to talk about their breathing. A pupil who times, records or reads the limewater is "
           "doing the assessed science — the star jumps are not the science.")

LESSONS = [

# ============================================================ W4 · L1 · DISCOVER (seed)
dict(
  week=4, slug="SCI_L_W4_L1_Diffusion",
  title="Discover: Diffusion",
  sow="Aut1·W4 (Discover) — Explain diffusion and the factors that affect its rate.",
  lo="I can explain diffusion and the factors that affect its rate.",
  sc=[
    "I can define diffusion using 'net movement' and 'concentration gradient'.",
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
    "It is passive — it needs no energy from the cell.",
    "Rate increases with: a steeper concentration gradient, higher temperature, larger surface area.",
    "Rate decreases with a longer diffusion distance (a thicker barrier).",
    "Particles still move both ways. 'Net' means the overall balance is one way.",
  ],
  misconceptions=[
    ("Particles only move one way in diffusion.",
     "They move randomly in all directions. The NET result is down the gradient."),
    ("Diffusion needs energy.",
     "No. That is active transport, which is Topic W6. Diffusion is free."),
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
    think=("Weak version: 'diffusion is when things spread out'. That earns very little. Marking "
           "version: 'the NET movement of particles from an area of HIGHER concentration to an area "
           "of LOWER concentration, DOWN a concentration gradient'. Three technical phrases, each "
           "doing work."),
    illuminator=("Two-chamber diagram separated by a membrane. Left chamber densely dotted, tagged "
                 "'● HIGH CONCENTRATION'; right chamber sparsely dotted, tagged '○ LOW "
                 "CONCENTRATION'. Arrows both directions, the net arrow drawn thicker and labelled "
                 "'NET MOVEMENT'. Below, three rate-factor tags: '↑ STEEPER GRADIENT', "
                 "'↑ HIGHER TEMPERATURE', '↑ MORE SURFACE AREA'. Labels horizontal."),
  ),
  wedo1=dict(
    heading="Faster or slower?",
    prompt="Decide before you tap.",
    items=[
      ("Steeper concentration gradient", "FASTER"),
      ("Higher temperature", "FASTER — particles have more kinetic energy"),
      ("Thicker membrane", "SLOWER — longer distance to travel"),
      ("Larger surface area", "FASTER — more room to cross"),
      ("Adding energy from the cell", "NO EFFECT — diffusion is passive"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("You apply it, out loud as you write: 'Oxygen diffuses from the alveolus into the blood "
           "because oxygen concentration is higher in the alveolus. The wall is one cell thick, so "
           "the diffusion distance is short, which increases the rate.' Direction, reason, adaptation."),
    capture="Photograph the pupil's annotated alveolus diagram with all three adaptations labelled.",
  ),
  wedo2=dict(
    heading="Diffusion or not?",
    pills=[
      ("Oxygen into the blood at the alveoli", "DIFFUSION"),
      ("Carbon dioxide out of a cell", "DIFFUSION"),
      ("A smell spreading across a room", "DIFFUSION"),
      ("Glucose pumped into a root hair against the gradient", "NOT DIFFUSION — that is active transport"),
      ("Water across a partially permeable membrane", "OSMOSIS — a special case, next topic"),
      ("Net movement down a gradient, no energy used", "DIFFUSION"),
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
    space="Lung and breathing content can land close to home. You can work from the diagram and skip the discussion.",
    voice="If a definition on the board does not make sense, say so — precision is the whole point today.",
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
  ta_rule="ONE RULE: the words 'net movement' and 'down the concentration gradient' earn the mark. Insist on them.",
  ta_notes=[
    "'Things spread out' is not a definition. Push every pupil to the technical phrasing at their tier.",
    "Do not preview active transport today — W6 lands better if diffusion is secure as the free, passive one first.",
  ],
  coldcall=[
    ("Watch me define it properly", "Which three phrases were doing the work?"),
    ("Faster or slower?", "Does adding energy speed diffusion up?"),
    ("Diffusion or not?", "Why is the root hair example not diffusion?"),
  ],
  uas="AQA UAS: 'Cells and transport'.",
),

# ============================================================ W4 · L2 · USE
dict(
  week=4, slug="SCI_L_W4_L2_GasExchange",
  title="Use: Diffusion in the Lungs — Testing Breath",
  sow="Aut1·W4 (Use) — Apply diffusion to gas exchange; evidence with the limewater CO2 test.",
  lo="I can apply diffusion to gas exchange in the alveoli, and use the limewater test as evidence that the body makes carbon dioxide.",
  sc=[
    "I can name the three adaptations of an alveolus and link each to diffusion.",
    "I can predict and record the limewater result for breathed-out air.",
    "I can use the result to explain what gas exchange removes from the body.",
  ],
  ko_vocab=[
    ("alveolus", "A tiny air sac in the lung where gas exchange happens."),
    ("gas exchange", "Oxygen diffusing into the blood and carbon dioxide diffusing out."),
    ("limewater", "A clear liquid that turns cloudy/milky when carbon dioxide bubbles through it."),
    ("adaptation", "A feature that makes a structure better at its job."),
    ("capillary", "The tiniest blood vessel, one cell thick, next to the alveolus."),
  ],
  ko_facts=[
    "Oxygen diffuses from the alveolus (high O2) into the blood (low O2). Carbon dioxide diffuses the other way.",
    "Three alveolus adaptations: large surface area, wall one cell thick (short distance), good blood supply (keeps the gradient steep).",
    "Limewater turns from clear to cloudy when carbon dioxide passes through it.",
    "Breathed-out air turns limewater cloudy faster than breathed-in air — it has more carbon dioxide.",
    "The extra carbon dioxide comes from respiration in the body's cells and is removed by gas exchange.",
  ],
  misconceptions=[
    ("The lungs make oxygen.",
     "They do not make it. Oxygen diffuses IN from the air; the lungs are the exchange surface."),
    ("Cloudy limewater means the experiment went wrong.",
     "Cloudy is the POSITIVE result — it means carbon dioxide is present. That is the evidence."),
    ("Breathing and respiration are the same thing.",
     "Breathing moves air; respiration is the reaction in cells that makes the carbon dioxide."),
  ],
  arrival=dict(
    supported="From the word bank, name the gas that diffuses INTO the blood at the alveolus.",
    standard="Name one adaptation of an alveolus and say how it helps diffusion.",
    stretch="Name two alveolus adaptations and link each one to a factor that speeds up diffusion.",
  ),
  glance=["Three adaptations", "Predict the limewater", "Explain the result"],
  ido1=dict(
    heading="Watch me set the test up — then you run it",
    think=("Two boiling tubes of clear limewater. One I draw room air through, one I breathe out "
           "through — safely, through the tube, never sucking back. I PREDICT first: breathed-out "
           "air has more carbon dioxide, so that tube goes cloudy faster. Then I hand it to you. "
           "You time it, you record it, you say the conclusion. My prediction is on the board so we "
           "can check it against your result."),
    illuminator=("A single alveolus wrapped by a capillary: oxygen arrow tagged '● O2 IN' diffusing "
                 "from air sac to blood, carbon dioxide arrow tagged '○ CO2 OUT' the other way. Three "
                 "adaptation tags: '■ LARGE SURFACE AREA', '■ WALL ONE CELL THICK', "
                 "'■ GOOD BLOOD SUPPLY'. Beside it, two bench tubes of limewater tagged "
                 "'CLEAR = no CO2' and 'CLOUDY = CO2 present'. Labels horizontal."),
  ),
  wedo1=dict(
    heading="Predict, then check",
    prompt="Say your prediction before you tap.",
    items=[
      ("Which gas diffuses INTO the blood?", "Oxygen"),
      ("Which gas diffuses OUT into the alveolus?", "Carbon dioxide"),
      ("Breathed-out air through limewater", "CLOUDY faster — more CO2"),
      ("Room air drawn through limewater", "Stays clearer for longer — less CO2"),
      ("Wall one cell thick", "Short diffusion distance — faster gas exchange"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("You close the loop, not me. Say and write the conclusion as a frame: 'The limewater "
           "went cloudy ____ with breathed-out air, so breathed-out air has ____ carbon dioxide, "
           "because respiration in my cells makes it and gas exchange removes it.' Result, then "
           "reason. A wrong prediction is fine — we record what happened, not what we hoped."),
    capture="Photograph the pupil's own results table (time to go cloudy for each tube) with their written conclusion.",
  ),
  wedo2=dict(
    heading="Match the adaptation to the reason",
    pills=[
      ("Large surface area", "More room for gases to cross — faster diffusion"),
      ("Wall one cell thick", "Short diffusion distance — faster diffusion"),
      ("Good blood supply", "Keeps the concentration gradient steep"),
      ("Moist lining", "Gases dissolve before they diffuse"),
      ("Cloudy limewater", "Carbon dioxide is present — the positive result"),
      ("The lungs make oxygen", "NOT TRUE — oxygen diffuses in from the air"),
    ],
    wagoll=("Breathed-out air turned the limewater cloudy faster than room air, so it contains more "
            "carbon dioxide. The carbon dioxide is made by respiration in the cells and removed at "
            "the alveoli, where it diffuses from the blood into the air because its concentration "
            "is higher in the blood."),
  ),
  independent=dict(
    supported="Run the limewater test with a partner, fill in the pre-drawn results table, and complete the conclusion sentence from the word bank.",
    standard="Run the test, record the times, label the alveolus with its three adaptations, and write the conclusion in your own words.",
    stretch="Run the test, record and compare the times, then explain how each alveolus adaptation increases the rate of gas exchange, using the diffusion factors.",
  ),
  lundy=dict(
    space="You never have to be the one who breathes out or exercises. Timing and recording the limewater is the assessed job, and it is yours if you want it.",
    voice="If your result disagrees with my prediction, say so — we look at the method, then the number. The prediction can be wrong; that is data.",
    audience="Your results table is Topic 1 evidence and goes into your folder for the W7 review.",
    influence="The class agrees the safe breathing-out protocol — and then everyone follows it.",
  ),
  exit=dict(
    supported="What colour does limewater go when carbon dioxide is present?",
    standard="Name one alveolus adaptation and say how it speeds up diffusion.",
    stretch="Explain why breathed-out air turns limewater cloudy faster than room air.",
  ),
  exit_key=["cloudy / milky",
            "e.g. wall one cell thick — short diffusion distance, so faster diffusion",
            "Breathed-out air has more carbon dioxide from respiration, so more CO2 passes through the limewater and turns it cloudy faster."],
  witness=[
    "Linked three alveolus adaptations to diffusion.",
    "Predicted, ran and recorded the limewater test.",
    "Concluded that breathed-out air has more carbon dioxide.",
  ],
  ta_rule="ONE RULE: cloudy limewater is the POSITIVE result — it means carbon dioxide is there. Never call it a fail.",
  ta_notes=[
    "Your station job: safety on the breathing-out step (blow through, never suck back) and making sure each pair records the TIME for both tubes. The timed result is the evidence.",
    "A wrong prediction is not a wrong answer. Record what happened and praise the honest record.",
  ],
  coldcall=[
    ("Watch me set the test up — then you run it", "What do I do before I touch the limewater?"),
    ("Predict, then check", "Which gas diffuses into the blood?"),
    ("Match the adaptation to the reason", "Why does a good blood supply speed up diffusion?"),
  ],
  uas="AQA UAS: 'Cells and transport'; 'Carrying out a practical investigation'.",
),

# ============================================================ W4 · L3 · MASTER
dict(
  week=4, slug="SCI_L_W4_L3_ExamSkills",
  title="Master: Explaining Diffusion in the Exam",
  sow="Aut1·W4 (Master) — Answer 'explain' and 'describe' diffusion questions independently.",
  lo="I can answer exam-style diffusion questions independently, matching my answer to the command word.",
  sc=[
    "I can tell 'describe' and 'explain' apart and answer each correctly.",
    "I can find the number of marks and give that many separate points.",
    "I can build a full 'explain' answer: direction, reason, adaptation.",
  ],
  ko_vocab=[
    ("describe", "Say what happens. No reason needed."),
    ("explain", "Say WHY it happens — 'because' usually belongs in the answer."),
    ("point", "One separate idea that earns one mark."),
    ("gradient", "The difference in concentration that particles diffuse down."),
    ("adaptation", "A feature that makes diffusion faster — surface area, distance, gradient."),
  ],
  ko_facts=[
    "Marks usually match the number of points needed — a 3-mark question wants three separate points.",
    "'Explain' answers without a reason score low no matter how neat they are.",
    "A full 'explain diffusion' answer names the direction, the reason (gradient), and an adaptation.",
    "'Describe' wants what happens; 'explain' wants why. Different questions, different answers.",
    "Length is not the target. Three clear points beat a paragraph that restates the question.",
  ],
  misconceptions=[
    ("A longer answer scores more.",
     "Marks follow points, not length. Three clear points beat a paragraph of restatement."),
    ("Describe and explain mean the same thing.",
     "Describe = what. Explain = why. The word 'because' belongs in an explain answer."),
    ("Naming the process is enough.",
     "'It's diffusion' alone rarely scores. You need the direction, the reason and an adaptation."),
  ],
  arrival=dict(
    supported="Match the command word to what it asks: describe / explain.",
    standard="Write what an 'explain' answer must contain that a 'describe' answer does not.",
    stretch="A 3-mark 'explain why oxygen diffuses into the blood' — list the three points you would make.",
  ),
  glance=["Command word first", "Count the marks", "Direction · reason · adaptation"],
  ido1=dict(
    heading="Watch me answer a 3-mark 'explain'",
    think=("'Explain why oxygen diffuses into the blood at the alveoli. [3]' Three marks, so three "
           "points. One: oxygen concentration is higher in the alveolus than the blood. Two: so it "
           "diffuses down the concentration gradient. Three: the wall is one cell thick, so the "
           "distance is short and the rate is high. Three reasons, not a paragraph. Now you run it."),
    illuminator=("A command-word card: 'DESCRIBE → what happens' and 'EXPLAIN → why, because…'. "
                 "Beside it a 3-mark answer shown with each scoring point bracketed and numbered "
                 "1, 2, 3 — point 1 direction, point 2 gradient, point 3 adaptation. Labels horizontal."),
  ),
  wedo1=dict(
    heading="What does the question want?",
    prompt="Name the demand before you tap.",
    items=[
      ("Describe what happens to the oxygen. [2]", "What happens — no reason needed"),
      ("Explain why it diffuses in. [3]", "Reasons — three of them"),
      ("Explain why a thick wall slows diffusion. [2]", "Why — distance and rate"),
      ("Name the gas that leaves the blood. [1]", "One word: carbon dioxide"),
      ("'It spreads out.' for a 3-mark explain", "Too vague — missing net movement, gradient, direction"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("Show-me lesson: repair a weak answer, then answer your own. 'Oxygen goes in.' scores one "
           "at most. Add the gradient and the thin-wall adaptation and the same idea reaches three. "
           "You mark your OWN answer against the board — is the direction there? the reason? an "
           "adaptation? Tick the points you made. Method, never a grade."),
    capture="Photograph the pupil's improved answer beside their first attempt — the pair shows the progress.",
  ),
  wedo2=dict(
    heading="What is missing?",
    pills=[
      ("'It spreads out.' (Explain diffusion, 3 marks)", "MISSING: net movement, gradient, direction"),
      ("'Oxygen goes in.' (Explain, 3 marks)", "MISSING: the reason — gradient and an adaptation"),
      ("'The wall is thin.' (Explain fast diffusion, 2 marks)", "MISSING: so the distance is short and the rate is higher"),
      ("A neat paragraph for a 1-mark 'name'", "NOT MISSING — but it cost time it did not need"),
      ("'Higher concentration in the alveolus, so it diffuses down the gradient, and the wall is one cell thick.'", "COMPLETE — direction, reason, adaptation"),
      ("'Because.' with no science after it", "MISSING: the actual reason"),
    ],
    wagoll=("Explain why oxygen diffuses into the blood at the alveoli. [3] — The concentration of "
            "oxygen is higher in the alveolus than in the blood (1), so oxygen diffuses down the "
            "concentration gradient (1). The alveolus wall is one cell thick, so the diffusion "
            "distance is short and the rate is high (1)."),
  ),
  independent=dict(
    supported="Four exam-style questions with the command word highlighted and sentence starters for each point.",
    standard="Six exam-style diffusion questions including one describe and one 3-mark explain, points numbered.",
    stretch="Six questions including a 4-mark explain, then review two of your own answers and state which point would gain the missing mark.",
  ),
  lundy=dict(
    space="Exam-style work raises the temperature. This is practice — the Topic 1 assessment is separate and you will know when it happens.",
    voice="Challenge any question that seems unfair. Sometimes the question is the problem.",
    audience="Your improved answers go into the Topic 1 folder as the revision set.",
    influence="The class chooses which question type gets one more worked example.",
  ),
  exit=dict(
    supported="What must an 'explain' answer contain that a 'describe' answer does not?",
    standard="A 3-mark 'explain why oxygen diffuses in' — how many separate points do you need?",
    stretch="Write a full-mark 'explain why a thin alveolus wall speeds up diffusion.'",
  ),
  exit_key=["a reason — why it happens, not just what",
            "three separate points (direction, gradient, adaptation)",
            "A thin wall means a short diffusion distance, so particles cross in less time and the rate of diffusion is higher."],
  witness=[
    "Distinguished describe from explain.",
    "Matched the number of points to the marks.",
    "Built a full explain answer: direction, reason, adaptation.",
  ],
  ta_rule="ONE RULE: count the marks, then find that many separate points. Length is not the target.",
  ta_notes=[
    "No mark schemes or grade descriptors are shown. Feedback is 'this point is missing', never a predicted grade.",
    "The Topic 1 assessment is separate (PythonAnywhere). Say so — pupils manage practice better knowing it is not the real thing.",
  ],
  coldcall=[
    ("Watch me answer a 3-mark 'explain'", "How many points was I hunting?"),
    ("What does the question want?", "What does 'explain' need that 'describe' does not?"),
    ("What is missing?", "What is missing from 'it spreads out'?"),
  ],
  uas="AQA UAS: 'Cells and transport'; exam technique.",
),
]
