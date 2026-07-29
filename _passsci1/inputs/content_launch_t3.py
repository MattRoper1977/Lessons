# -*- coding: utf-8 -*-
"""
LAUNCH science — Topic 3 (SoW W5 Osmosis core practical), 3-lesson arc.
L1 Discover: define osmosis + partially permeable membrane. L2 Use: the authored core-practical
seed. L3 Master: analyse and EVALUATE the practical (graph, isotonic point, method) — exam skills.
No mark schemes (UAS). Real command words. Icon+label+colour. Maths scaffolds at every tier.
"""

STRAND = "Science"
PATHWAY = "LAUNCH"
COLOUR = "#7A5C9E"
SPINE = "Edexcel GCSE Biology 1BI0 Foundation · Paper 1 · Topic 1"
AWARD = ("Pearson Edexcel GCSE (9–1) Biology 1BI0 (Foundation, grades 1–5); "
         "GCSE Combined Science 1SC0 F where appropriate; AQA UAS science units")
THEME = "Identity &amp; Belonging"
SLOT_WEEKS = 7
SENSORY = ("Core-practical work involves glassware, cork borers and a 30-minute wait. Agree who "
           "handles blades before the lesson. A pupil who weighs, records, calculates or plots is "
           "doing the assessed science — cutting the potato is not the science.")

LESSONS = [

# ============================================================ W5 · L1 · DISCOVER
dict(
  week=5, slug="SCI_L_W5_L1_Osmosis",
  title="Discover: Osmosis",
  sow="Aut1·W5 (Discover) — Define osmosis and the partially permeable membrane.",
  lo="I can define osmosis and explain how it differs from diffusion.",
  sc=[
    "I can define osmosis, including 'partially permeable membrane'.",
    "I can state that water moves from a dilute to a concentrated solution.",
    "I can explain why osmosis is a special case of diffusion.",
  ],
  ko_vocab=[
    ("osmosis", "The net movement of WATER from a dilute to a concentrated solution through a partially permeable membrane."),
    ("partially permeable", "Lets some particles (water) through but not others (sugar)."),
    ("dilute", "More water, less solute."),
    ("concentrated", "Less water, more solute."),
    ("solute", "The dissolved substance, e.g. sugar or salt."),
  ],
  ko_facts=[
    "Osmosis is the diffusion of WATER only, and only through a partially permeable membrane.",
    "Water moves from where there is MORE water (dilute) to where there is LESS water (concentrated).",
    "The membrane lets water through but holds the sugar back — that is why only water moves.",
    "Osmosis is a special case of diffusion: same idea (down a gradient), but water and a membrane.",
    "Reframe by water: water moves from where water is plentiful to where water is scarce.",
  ],
  misconceptions=[
    ("Osmosis moves sugar.",
     "Osmosis moves WATER. The sugar cannot cross the membrane, which is why water does."),
    ("Water moves toward more sugar because sugar attracts it.",
     "Reframe by water: it moves from where water is plentiful to where water is scarce."),
    ("Osmosis and diffusion are completely different.",
     "Osmosis IS diffusion — of water, through a partially permeable membrane. Same gradient idea."),
  ],
  arrival=dict(
    supported="Complete from the word bank: osmosis is the movement of ____ through a ____ membrane.",
    standard="Write a definition of osmosis.",
    stretch="Write a definition of osmosis and state one way it differs from diffusion.",
  ),
  glance=["Define osmosis", "Water, not sugar", "Osmosis vs diffusion"],
  ido1=dict(
    heading="Watch me reframe it by water",
    think=("Everyone wants to say 'water moves to the sugar'. Reframe by water instead: on the "
           "dilute side there is LOTS of water; on the concentrated side there is LESS water. Water "
           "moves from lots to less — down its own gradient. The sugar never moves, because the "
           "membrane will not let it through. Only water. That is osmosis."),
    illuminator=("A partially permeable membrane down the middle: small water particles crossing "
                 "both ways with a thick net arrow tagged '● WATER MOVES'; large sugar particles "
                 "stopped at the membrane tagged '✕ SUGAR BLOCKED'. Left side tagged "
                 "'○ DILUTE (more water)', right side '■ CONCENTRATED (less water)'. Labels horizontal."),
  ),
  wedo1=dict(
    heading="Which way does water move?",
    prompt="Decide before you tap.",
    items=[
      ("Dilute solution next to concentrated", "Water moves INTO the concentrated side"),
      ("Does the sugar cross the membrane?", "No — it is partially permeable"),
      ("Pure water next to a sugary cell", "Water moves INTO the cell"),
      ("Two solutions the same concentration", "No net movement"),
      ("Is osmosis a type of diffusion?", "Yes — diffusion of water through a membrane"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("You write the definition to the marking standard: 'Osmosis is the net movement of "
           "WATER from a DILUTE solution to a CONCENTRATED solution through a PARTIALLY PERMEABLE "
           "membrane.' Four phrases underlined. Read it back and check all four are there."),
    capture="Photograph the pupil's own definition with the four key phrases underlined.",
  ),
  wedo2=dict(
    heading="Osmosis or diffusion?",
    pills=[
      ("Water across a partially permeable membrane", "OSMOSIS"),
      ("Oxygen into the blood at the alveoli", "DIFFUSION — a gas, no membrane needed"),
      ("Water from dilute to concentrated", "OSMOSIS"),
      ("A smell spreading across a room", "DIFFUSION"),
      ("Sugar crossing the membrane", "NEITHER — the membrane blocks sugar"),
      ("Net movement of water down its gradient through a membrane", "OSMOSIS"),
    ],
    wagoll=("Osmosis is the net movement of water from a dilute solution to a concentrated solution "
            "through a partially permeable membrane. It is a special case of diffusion because only "
            "water moves, and it moves down its own concentration gradient."),
  ),
  independent=dict(
    supported="Label the osmosis diagram and complete the definition from the word bank.",
    standard="Write the osmosis definition unaided, then explain why the sugar does not move.",
    stretch="Write the definition, explain why sugar does not move, and describe one way osmosis differs from diffusion.",
  ),
  lundy=dict(
    space="This is a definition lesson — precision matters more than speed. The four key phrases stay on the board all lesson.",
    voice="If 'water moves to the sugar' feels more natural to you, say so — then we reframe it by water together.",
    audience="Your definition goes into the Topic 1 folder and is the springboard for next lesson's practical.",
    influence="The class picks the everyday example (a wilting plant, a raisin in water) we open the practical with.",
  ),
  exit=dict(
    supported="Osmosis is the movement of ______.",
    standard="Why does the sugar not move during osmosis?",
    stretch="Explain why osmosis is called a special case of diffusion.",
  ),
  exit_key=["water (through a partially permeable membrane)",
            "The membrane is partially permeable — it lets water through but not the larger sugar.",
            "It is the diffusion of water down its own gradient, but only through a partially permeable membrane."],
  witness=[
    "Defined osmosis including 'partially permeable membrane'.",
    "Stated water moves from dilute to concentrated.",
    "Explained osmosis as a special case of diffusion.",
  ],
  ta_rule="ONE RULE: reframe by WATER — water moves from where there is more water to where there is less.",
  ta_notes=[
    "The four phrases (net movement, water, dilute→concentrated, partially permeable) are the mark. Hold every pupil to their tier's version.",
    "Do not let 'water moves to the sugar' stand uncorrected — reframe it by water every time.",
  ],
  coldcall=[
    ("Watch me reframe it by water", "Where is there more water — the dilute or concentrated side?"),
    ("Which way does water move?", "Does the sugar cross the membrane?"),
    ("Osmosis or diffusion?", "Why is the alveoli example diffusion, not osmosis?"),
  ],
  uas="AQA UAS: 'Cells and transport'.",
),

# ============================================================ W5 · L2 · USE (seed)
dict(
  week=5, slug="SCI_L_W5_L2_OsmosisCP",
  title="Use: Osmosis Core Practical",
  sow="Aut1·W5 (Use) — Investigate osmosis with the core practical; calculate % change.",
  lo="I can carry out the osmosis core practical and calculate the percentage change in mass.",
  sc=[
    "I can name the control variables in the core practical.",
    "I can calculate percentage change in mass.",
    "I can explain my results in terms of water concentration.",
  ],
  ko_vocab=[
    ("core practical", "A required experiment you must be able to describe and analyse."),
    ("control variable", "Something kept the same so the test is fair."),
    ("percentage change", "(change ÷ original) × 100."),
    ("initial mass", "The mass recorded BEFORE the potato goes in the solution."),
    ("blot", "To dab dry the same way every time before weighing."),
  ],
  ko_facts=[
    "percentage change in mass = (final mass − initial mass) ÷ initial mass × 100",
    "Divide by the INITIAL mass, not the final — the classic dropped mark.",
    "Potato in pure water GAINS mass; potato in concentrated sugar solution LOSES mass.",
    "A negative percentage change means the sample lost mass — keep the minus sign.",
    "Controls: same potato, same size cylinder, same time, blotted the same way. Only concentration changes.",
  ],
  misconceptions=[
    ("A mass loss means the experiment failed.",
     "A loss is a valid result — it tells you the outside solution was more concentrated than inside."),
    ("Dividing by the final mass is fine.",
     "Always divide by the INITIAL mass. That single choice is the most-dropped mark here."),
    ("You can weigh the potato wet.",
     "Blot every cylinder the same way first — inconsistent blotting is the biggest error source."),
  ],
  arrival=dict(
    supported="From the word bank, write the one thing we deliberately change in this practical.",
    standard="Name two variables we must keep the same in the osmosis practical.",
    stretch="Write the percentage change equation and state which mass you divide by.",
  ),
  glance=["Set the controls", "Run and weigh", "Calculate % change"],
  ido1=dict(
    heading="Watch me set it up — then you run it",
    think=("Same potato, same corer, same length, blotted the same way — all controls. The ONE "
           "thing that changes is the sugar concentration. Initial mass recorded to two decimal "
           "places BEFORE anything goes in the tube, because I cannot get it back afterwards. Then "
           "thirty minutes. Then blot identically and re-weigh. You take the readings, you do the "
           "maths."),
    illuminator=("Core-practical set-up: five labelled tubes across the concentration range, a "
                 "potato cylinder in each, each tube tagged with its concentration in words. Beside "
                 "it a results table with columns 'INITIAL MASS (g)', 'FINAL MASS (g)', "
                 "'CHANGE (g)', '% CHANGE'. A tag reads 'BLOT THE SAME WAY EVERY TIME — BIGGEST "
                 "SOURCE OF ERROR'. Labels horizontal."),
  ),
  wedo1=dict(
    heading="Predict the direction",
    prompt="Say gain, lose or no change before you tap.",
    items=[
      ("Potato in pure water", "GAINS mass — water moves in"),
      ("Potato in very concentrated sugar solution", "LOSES mass — water moves out"),
      ("Potato in a solution matching its own cells", "NO CHANGE — no net movement"),
      ("Which mass do you divide by?", "The INITIAL mass"),
      ("Result is −8%. Did it gain or lose?", "Lost mass — keep the minus sign"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("You do the calculation out loud as you write it: initial 4.20 g, final 4.62 g. Change "
           "= +0.42 g. Percentage = 0.42 ÷ 4.20 × 100 = +10%. Divide by the INITIAL mass. Say the "
           "answer with its sign. The completed table is your evidence, in your hand."),
    capture="Photograph the pupil's completed results table with the % change column filled in and signed.",
  ),
  wedo2=dict(
    heading="Explain the result",
    pills=[
      ("Gained mass in pure water", "Water moved IN — higher water concentration outside"),
      ("Lost mass in strong sugar solution", "Water moved OUT — lower water concentration outside"),
      ("Dividing by final mass", "ERROR — always divide by the initial mass"),
      ("Dropping the minus sign", "ERROR — a loss must be reported as negative"),
      ("Sugar moved into the potato", "NOT TRUE — the membrane blocks sugar"),
      ("No change at the matching concentration", "CORRECT — no net water movement"),
    ],
    wagoll=("The potato in pure water gained mass because the water concentration outside the cells "
            "was higher than inside, so water moved in by osmosis through the partially permeable "
            "membranes. Percentage change = (4.62 − 4.20) ÷ 4.20 × 100 = +10%."),
  ),
  independent=dict(
    supported="Run two concentrations with the table pre-drawn and the formula printed. Complete the calculation with the worked example alongside.",
    standard="Run the full concentration range, complete the table, and calculate percentage change for each.",
    stretch="Run the full range, calculate percentage change, plot the results, and use the graph to estimate the concentration inside the potato cells.",
  ),
  lundy=dict(
    space="This practical has a thirty-minute wait built in. The wait is not empty time — the calculation practice happens in it.",
    voice="If your result disagrees with the class trend, we look at your method before your number.",
    audience="Your results table is core-practical evidence and goes into the Topic 1 folder.",
    influence="The class agrees the blotting protocol — and everyone then has to follow it.",
  ),
  exit=dict(
    supported="Which mass do you divide by to find percentage change?",
    standard="A cylinder goes from 5.00 g to 4.50 g. Calculate the percentage change.",
    stretch="Explain why a potato in concentrated sugar solution loses mass.",
  ),
  exit_key=["the initial mass",
            "−10%",
            "Water concentration outside is lower than inside, so water leaves the cells by osmosis through the partially permeable membrane."],
  witness=[
    "Named the control variables.",
    "Carried out the core practical and recorded masses.",
    "Calculated percentage change dividing by the initial mass.",
  ],
  ta_rule="ONE RULE: divide by the INITIAL mass. That is the single most-dropped mark in this practical.",
  ta_notes=[
    "Your station job: initial masses recorded before anything enters a tube, and the same blotting technique held for everyone. Once a cylinder is in, that initial data is gone.",
    "Cork borers and scalpels: agree who handles them. A pupil who weighs, records and calculates has met the outcome without touching a blade.",
  ],
  coldcall=[
    ("Watch me set it up — then you run it", "Which mass do I record first, and why does it matter?"),
    ("Predict the direction", "What happens to a potato in pure water?"),
    ("Explain the result", "Do we divide by the initial or final mass?"),
  ],
  uas="AQA UAS: 'Cells and transport'; 'Carrying out a practical investigation'.",
),

# ============================================================ W5 · L3 · MASTER
dict(
  week=5, slug="SCI_L_W5_L3_Evaluate",
  title="Master: Analysing the Osmosis Practical",
  sow="Aut1·W5 (Master) — Plot, analyse and evaluate the osmosis core practical.",
  lo="I can analyse osmosis results with a graph and evaluate the method independently.",
  sc=[
    "I can read the concentration inside the cells from a graph (the zero-change point).",
    "I can calculate percentage change and label the axis correctly.",
    "I can evaluate the method and suggest one improvement.",
  ],
  ko_vocab=[
    ("analyse", "Use the data to find a pattern or a value."),
    ("evaluate", "Judge how good the method or evidence is, and how to improve it."),
    ("anomaly", "A result that does not fit the pattern."),
    ("isotonic point", "The concentration where mass does not change — same as inside the cells."),
    ("repeat", "Doing a concentration again to check reliability."),
  ],
  ko_facts=[
    "On a graph of % change against concentration, the line crosses zero at the cell's own concentration.",
    "Above that concentration the potato loses mass; below it, gains — the line slopes down.",
    "'Evaluate' means say what was good, what limited the result, and how to improve it.",
    "An anomaly is circled and set aside from the trend, not deleted — record it and say so.",
    "More repeats and consistent blotting improve reliability; they do not change the pattern.",
  ],
  misconceptions=[
    ("Evaluate just means say it went well.",
     "Evaluate weighs strengths AND weaknesses, then gives an improvement. Both sides, then a fix."),
    ("An anomaly should be rubbed out.",
     "Circle it, keep it, and say it does not fit. Deleting data is not science."),
    ("A perfect straight line is expected.",
     "Biological data scatters. Look for the trend and the zero-crossing, not a perfect line."),
  ],
  arrival=dict(
    supported="On the graph, point to where the line crosses zero percentage change.",
    standard="What does the point where the line crosses zero tell you about the potato cells?",
    stretch="The line crosses zero at 0.3 mol/dm³. Explain what that value represents.",
  ),
  glance=["Plot and read the graph", "Find the zero-change point", "Evaluate the method"],
  ido1=dict(
    heading="Watch me read the graph — then you evaluate",
    think=("Percentage change up the side, concentration along the bottom. The line slopes down and "
           "crosses zero at one concentration. THAT crossing point is the concentration inside the "
           "potato cells, because there the mass did not change — no net osmosis. Above it, loss; "
           "below it, gain. Now you evaluate: what limited this result, and how would you improve it?"),
    illuminator=("A graph: percentage change in mass (y, positive and negative) against sugar "
                 "concentration (x). A line sloping down through zero, the zero-crossing tagged "
                 "'◆ SAME AS INSIDE THE CELLS'. One point circled tagged '○ ANOMALY — keep it'. "
                 "Beside it three evaluate tags: '■ WHAT WAS GOOD', '■ WHAT LIMITED IT', "
                 "'■ ONE IMPROVEMENT'. Labels horizontal."),
  ),
  wedo1=dict(
    heading="Analyse or evaluate?",
    prompt="Name the skill before you tap.",
    items=[
      ("Read the zero-change concentration off the graph", "ANALYSE — using the data"),
      ("Say the blotting was inconsistent and suggest a fix", "EVALUATE — judging the method"),
      ("Circle a point that does not fit the trend", "ANALYSE — spotting an anomaly"),
      ("Suggest three repeats to improve reliability", "EVALUATE — improving the method"),
      ("Where the line crosses zero", "The concentration inside the cells"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("Show-me lesson: you plot the class data, read the zero-crossing, and write a two-line "
           "evaluation — one strength, one limitation, one improvement. Mark your OWN evaluation "
           "against the board: did you give both sides and a fix? Tick each. Method, never a grade."),
    capture="Photograph the pupil's plotted graph with the zero-crossing marked and their written evaluation.",
  ),
  wedo2=dict(
    heading="Strong or weak evaluation?",
    pills=[
      ("'It went well.'", "WEAK — no limitation, no improvement"),
      ("'Blotting varied, so masses were not fair; blot each the same way.'", "STRONG — limitation + fix"),
      ("'Repeat each concentration three times for reliability.'", "STRONG — a real improvement"),
      ("'I deleted the odd result.'", "WRONG — circle an anomaly, never delete it"),
      ("'The controls were kept the same, which was good.'", "STRONG — a genuine strength"),
      ("'It was a fun experiment.'", "NOT AN EVALUATION — no judgement of the method"),
    ],
    wagoll=("The line crosses zero at about 0.3 mol/dm³, so that is the concentration inside the "
            "potato cells. A limitation was inconsistent blotting, which affected the masses; I "
            "would improve it by blotting each cylinder the same way and repeating each "
            "concentration three times."),
  ),
  independent=dict(
    supported="Plot four given points, mark the zero-crossing, and complete an evaluation sentence from the word bank.",
    standard="Plot the class data, read the cell concentration, and write a strength, a limitation and an improvement.",
    stretch="Plot the data, estimate the cell concentration, identify any anomaly, and write a full evaluation with a justified improvement.",
  ),
  lundy=dict(
    space="Graph work and criticism can feel exposing. Evaluating a method is judging the METHOD, never the person who ran it.",
    voice="If you think the class data is unreliable, say why — a reasoned challenge is exactly what evaluate rewards.",
    audience="Your graph and evaluation go into the Topic 1 folder as core-practical evidence.",
    influence="The class agrees which improvement we would actually make if we ran it again.",
  ),
  exit=dict(
    supported="What does the point where the graph crosses zero tell you?",
    standard="Write one limitation of the osmosis practical and one improvement.",
    stretch="Explain how you would use a graph of the results to find the concentration inside the cells.",
  ),
  exit_key=["the concentration inside the potato cells",
            "e.g. inconsistent blotting affected masses; blot each cylinder the same way / repeat each concentration",
            "Plot % change against concentration; the concentration where the line crosses zero (no mass change) is the concentration inside the cells."],
  witness=[
    "Read the cell concentration from the zero-crossing.",
    "Calculated and plotted percentage change correctly.",
    "Evaluated the method with a strength, a limitation and an improvement.",
  ],
  ta_rule="ONE RULE: evaluate = one strength, one limitation, one improvement. All three, or it is not an evaluation.",
  ta_notes=[
    "No mark schemes or grade descriptors. Feedback names the missing part — 'no improvement given' — never a grade.",
    "An anomaly is circled and kept. Stop any pupil rubbing out a result and praise the honest record.",
  ],
  coldcall=[
    ("Watch me read the graph — then you evaluate", "What does the zero-crossing tell us?"),
    ("Analyse or evaluate?", "Is suggesting repeats analysing or evaluating?"),
    ("Strong or weak evaluation?", "Why is 'I deleted the odd result' wrong?"),
  ],
  uas="AQA UAS: 'Cells and transport'; 'Analysing and evaluating'.",
),
]
