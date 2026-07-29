# -*- coding: utf-8 -*-
"""
LAUNCH science — Topic 5 (SoW W7 Topic 1 review), 3-lesson arc.
L1 Discover: a knowledge round-up across the whole of Topic 1. L2 Use: command words applied to
mixed Topic 1 questions. L3 Master: independent exam practice (the authored seed), pointing at
the separate PythonAnywhere assessment. No mark schemes / grade descriptors (UAS). Real command
words; model answers/WAGOLLs only.
"""

STRAND = "Science"
PATHWAY = "LAUNCH"
COLOUR = "#7A5C9E"
SPINE = "Edexcel GCSE Biology 1BI0 Foundation · Paper 1 · Topic 1"
AWARD = ("Pearson Edexcel GCSE (9–1) Biology 1BI0 (Foundation, grades 1–5); "
         "GCSE Combined Science 1SC0 F where appropriate; AQA UAS science units")
THEME = "Identity &amp; Belonging"
SLOT_WEEKS = 7
SENSORY = ("Review and exam-style work can raise anxiety. This is practice, not the assessment. A "
           "pupil who retrieves, applies a command word or checks working is doing the assessed "
           "science; nobody is timed against anybody else.")

LESSONS = [

# ============================================================ W7 · L1 · DISCOVER
dict(
  week=7, slug="SCI_L_W7_L1_RoundUp",
  title="Discover: Topic 1 Knowledge Round-Up",
  sow="Aut1·W7 (Discover) — Retrieve and connect the whole of Topic 1.",
  lo="I can recall and connect the key ideas of Topic 1: magnification, diffusion, osmosis and active transport.",
  sc=[
    "I can state the magnification equation and what resolution means.",
    "I can define diffusion, osmosis and active transport in one line each.",
    "I can say which processes need energy and which move against the gradient.",
  ],
  ko_vocab=[
    ("magnification", "How many times bigger the image is: image size ÷ actual size."),
    ("diffusion", "Net movement of particles from high to low concentration, no energy."),
    ("osmosis", "Net movement of water from dilute to concentrated through a partially permeable membrane."),
    ("active transport", "Movement against the gradient, using energy from respiration."),
    ("resolution", "The smallest gap that can still be seen as two separate things."),
  ],
  ko_facts=[
    "magnification = image size ÷ actual size; it has no units. 1 mm = 1000 µm.",
    "Diffusion and osmosis are passive (no energy); active transport needs energy from respiration.",
    "Osmosis moves water only, and only through a partially permeable membrane.",
    "Active transport is the only one that moves substances AGAINST the concentration gradient.",
    "All four ideas connect through cells: how we see them, and how substances move in and out.",
  ],
  misconceptions=[
    ("Osmosis and diffusion are unrelated.",
     "Osmosis is a special case of diffusion — of water, through a membrane."),
    ("Everything that moves into a cell needs energy.",
     "Only active transport needs energy. Diffusion and osmosis are free."),
    ("Magnification has units.",
     "It is a ratio, so the units cancel. Write ×400, never 400 mm."),
  ],
  arrival=dict(
    supported="From the word bank, write the magnification equation.",
    standard="Write a one-line definition of diffusion AND osmosis.",
    stretch="Write one-line definitions of diffusion, osmosis and active transport.",
  ),
  glance=["Retrieve the four ideas", "Passive vs energy", "Connect them through the cell"],
  ido1=dict(
    heading="Watch me connect the topic",
    think=("Four ideas, one thread: the cell. Magnification is how we SEE the cell. Then three ways "
           "things move in and out: diffusion (down the gradient, free), osmosis (water only, "
           "through a membrane, free), active transport (up the gradient, needs energy). If I can "
           "place each one on that thread, I can answer almost anything Topic 1 asks."),
    illuminator=("A Topic 1 knowledge map: a central cell, with four labelled boxes around it — "
                 "'● MAGNIFICATION: image ÷ actual', '↓ DIFFUSION: high→low, no energy', "
                 "'○ OSMOSIS: water, membrane, no energy', '↑ ACTIVE TRANSPORT: up, needs energy'. "
                 "Lines connect each box to the cell. Labels horizontal, icon + word."),
  ),
  wedo1=dict(
    heading="Retrieve it — say it before you tap",
    prompt="Answer from memory, then check.",
    items=[
      ("The magnification equation", "magnification = image size ÷ actual size"),
      ("Which two processes need NO energy?", "Diffusion and osmosis"),
      ("Which process moves water only?", "Osmosis"),
      ("Which moves against the gradient?", "Active transport"),
      ("1 mm = how many µm?", "1000 µm"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("You build the map, not me. In the centre write 'cell'. Around it, write the four ideas "
           "with a one-line definition each, and draw a line from each to the cell. Then say the "
           "thread out loud: 'Magnification is how we see it; diffusion, osmosis and active "
           "transport are how things move in and out.' Your map is the evidence."),
    capture="Photograph the pupil's own Topic 1 knowledge map with all four ideas connected to the cell.",
  ),
  wedo2=dict(
    heading="Match the idea to its one-line fact",
    pills=[
      ("Magnification", "image size ÷ actual size — no units"),
      ("Diffusion", "high to low concentration — no energy"),
      ("Osmosis", "water only, through a partially permeable membrane"),
      ("Active transport", "against the gradient — needs energy from respiration"),
      ("Resolution", "the smallest gap seen as two separate things"),
      ("Only one of these needs energy", "Active transport"),
    ],
    wagoll=("Magnification is how many times bigger the image is (image ÷ actual). Diffusion and "
            "osmosis move substances down a gradient with no energy — osmosis moves water through a "
            "membrane. Active transport is the only one that moves against the gradient, using "
            "energy from respiration."),
  ),
  independent=dict(
    supported="Complete the Topic 1 knowledge map from the word bank, matching each idea to its one-line fact.",
    standard="Build the knowledge map unaided, then write which processes are passive and which needs energy.",
    stretch="Build the map, then write a short paragraph connecting all four ideas through the cell.",
  ),
  lundy=dict(
    space="Retrieval can feel exposing when you are not sure. A blank you notice today is a blank you can fix before the assessment — that is the point.",
    voice="If two ideas keep getting muddled for you, say which — the class probably shares it, and we will separate them.",
    audience="Your knowledge map goes into the Topic 1 folder as the revision anchor.",
    influence="The class decides which idea gets the most practice in the next two lessons.",
  ),
  exit=dict(
    supported="Which two processes need no energy?",
    standard="Write a one-line definition of osmosis.",
    stretch="Explain how osmosis and active transport differ.",
  ),
  exit_key=["diffusion and osmosis",
            "The net movement of water from a dilute to a concentrated solution through a partially permeable membrane.",
            "Osmosis moves water down its gradient with no energy; active transport moves substances up the gradient using energy from respiration."],
  witness=[
    "Recalled the magnification equation and resolution.",
    "Defined diffusion, osmosis and active transport.",
    "Identified which processes need energy and which go against the gradient.",
  ],
  ta_rule="ONE RULE: only active transport needs energy and goes against the gradient. Everything else is passive.",
  ta_notes=[
    "Your job is the retrieval station: prompt from the map, never give the answer. A remembered answer is worth more than a copied one.",
    "A blank is useful information, not a failure. Note which ideas need more practice and tell the teacher.",
  ],
  coldcall=[
    ("Watch me connect the topic", "What is the single thread connecting all four ideas?"),
    ("Retrieve it — say it before you tap", "Which two processes need no energy?"),
    ("Match the idea to its one-line fact", "Which one moves water only?"),
  ],
  uas="AQA UAS: 'Cells and transport'; retrieval and consolidation.",
),

# ============================================================ W7 · L2 · USE
dict(
  week=7, slug="SCI_L_W7_L2_CommandWords",
  title="Use: Command Words Across Topic 1",
  sow="Aut1·W7 (Use) — Apply describe, explain, calculate and compare to Topic 1 questions.",
  lo="I can choose what a Topic 1 question wants from its command word and answer to it.",
  sc=[
    "I can say what describe, explain, calculate and compare each require.",
    "I can answer a Topic 1 question in the shape its command word asks for.",
    "I can spot when an answer does not match its command word.",
  ],
  ko_vocab=[
    ("describe", "Say what happens. No reason needed."),
    ("explain", "Say WHY it happens — 'because' usually belongs."),
    ("calculate", "Work out a number, show working, give the unit (or × for magnification)."),
    ("compare", "Similarities AND differences, both sides named."),
    ("command word", "The word that tells you what kind of answer to give."),
  ],
  ko_facts=[
    "Read the command word FIRST — it decides the shape of the answer.",
    "'Describe' = what; 'explain' = why. Different questions, different answers.",
    "'Calculate' needs working and the right unit — magnification has none.",
    "'Compare' needs both sides — a one-sided answer scores half at best.",
    "Marks usually match points: a 3-mark question wants three separate points.",
  ],
  misconceptions=[
    ("Describe and explain are interchangeable.",
     "Describe = what happens; explain = why. Answering the wrong one loses the marks."),
    ("Compare means write about each in turn.",
     "Compare means side by side — the SAME and the DIFFERENT, named."),
    ("You can ignore the command word and just write everything.",
     "The command word is the instruction. Answer it exactly, no more, no less."),
  ],
  arrival=dict(
    supported="Match the command word to its demand: describe / explain / calculate.",
    standard="Write what 'explain' needs that 'describe' does not.",
    stretch="Write what describe, explain, calculate and compare each require.",
  ),
  glance=["Command word first", "Answer to its shape", "Spot the mismatch"],
  ido1=dict(
    heading="Watch me match answers to command words",
    think=("Same topic, four command words. 'Describe what happens to a potato in pure water' — I "
           "say it gains mass, no reason. 'Explain why' — now I add the osmosis reason. 'Calculate "
           "the percentage change' — working and a number. 'Compare diffusion and active transport' "
           "— both sides. Same knowledge, four different answer shapes. You try the next set."),
    illuminator=("A command-word reference card: DESCRIBE (what happens), EXPLAIN (why, because…), "
                 "CALCULATE (number + working + unit), COMPARE (both sides). Each with a one-line "
                 "Topic 1 example. Labels horizontal, icon + word."),
  ),
  wedo1=dict(
    heading="What does the question want?",
    prompt="Name the command word's demand before you tap.",
    items=[
      ("Describe what happens to the potato. [2]", "What happens — no reason needed"),
      ("Explain why it gains mass. [3]", "Reasons — osmosis, water concentration, membrane"),
      ("Calculate the magnification. [2]", "Number + working, no unit"),
      ("Compare diffusion and active transport. [4]", "Both sides — similarities and differences"),
      ("State the osmosis definition. [1]", "One line, no explanation needed"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("You answer three Topic 1 questions, each a different command word, and mark your OWN "
           "answers against the board: did the answer match the command word? For 'explain', is "
           "there a because? For 'compare', are both sides there? Tick the ones that match. You are "
           "checking the SHAPE, never awarding a grade."),
    capture="Photograph the pupil's three answers with the command word circled on each — the match is the evidence.",
  ),
  wedo2=dict(
    heading="Does the answer match the command word?",
    pills=[
      ("'It gains mass.' for 'Describe'", "MATCHES — describe wants what happens"),
      ("'It gains mass.' for 'Explain [3]'", "DOES NOT MATCH — explain needs the reason"),
      ("'×400' with working for 'Calculate'", "MATCHES — number and working"),
      ("Only about diffusion for 'Compare'", "DOES NOT MATCH — compare needs both sides"),
      ("A three-line answer for a 1-mark 'State'", "OVER-ANSWERED — state wants one line"),
      ("'Because osmosis, water moves in through the membrane' for 'Explain'", "MATCHES — a reason is given"),
    ],
    wagoll=("Explain why the potato gains mass in pure water. [3] — The water concentration is "
            "higher outside the cells than inside (1), so water moves in by osmosis (1) through the "
            "partially permeable cell membranes (1)."),
  ),
  independent=dict(
    supported="Six Topic 1 questions with the command word highlighted and a sentence starter for each.",
    standard="Eight Topic 1 questions across all four command words, answered to the correct shape.",
    stretch="Eight questions including a calculate and a compare, then review two answers and correct any command-word mismatch.",
  ),
  lundy=dict(
    space="Switching command words quickly is a real load. The reference card stays on the board — you are not tested on remembering the words today.",
    voice="If a question feels like it is asking two things at once, say so — sometimes it is, and that is worth naming.",
    audience="Your answers go into the Topic 1 folder and feed straight into next lesson's exam practice.",
    influence="The class chooses which command word gets one more worked example before the exam practice.",
  ),
  exit=dict(
    supported="What does 'explain' ask for that 'describe' does not?",
    standard="A question says 'Compare'. What two things must your answer include?",
    stretch="Rewrite 'It gains mass.' so it answers a 3-mark 'explain why the potato gains mass in water'.",
  ),
  exit_key=["a reason — why it happens",
            "similarities AND differences (both sides)",
            "It gains mass because the water concentration is higher outside than inside, so water moves in by osmosis through the partially permeable membrane."],
  witness=[
    "Stated what each command word requires.",
    "Answered Topic 1 questions to the correct shape.",
    "Spotted an answer that did not match its command word.",
  ],
  ta_rule="ONE RULE: read the command word first, then give exactly what it asks — no more, no less.",
  ta_notes=[
    "No mark schemes or grade descriptors. Feedback is 'this does not match the command word', never a predicted grade.",
    "Circle the command word on each question before the pupil answers. Half the errors vanish once it is circled.",
  ],
  coldcall=[
    ("Watch me match answers to command words", "Same fact, how many answer shapes?"),
    ("What does the question want?", "What does 'compare' need that 'describe' does not?"),
    ("Does the answer match the command word?", "Why does 'it gains mass' fail a 3-mark explain?"),
  ],
  uas="AQA UAS: 'Cells and transport'; exam technique.",
),

# ============================================================ W7 · L3 · MASTER (seed-based)
dict(
  week=7, slug="SCI_L_W7_L3_ExamPractice",
  title="Master: Topic 1 Exam Practice",
  sow="Aut1·W7 (Master) — Independent exam-style questions on Topic 1.",
  lo="I can answer exam-style questions across Topic 1 independently, matching each to its command word.",
  sc=[
    "I can answer a calculation question showing full working.",
    "I can answer an 'explain' question with the right number of points.",
    "I can identify what is missing from a weak answer.",
  ],
  ko_vocab=[
    ("describe", "Say what happens. No reason needed."),
    ("explain", "Say WHY it happens. 'Because' usually belongs in your answer."),
    ("calculate", "Work out a number. Show your working and give the unit (× for magnification)."),
    ("compare", "Give similarities AND differences, both sides named."),
    ("point", "One separate idea that earns one mark."),
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
           "thick so the distance is short and the rate is high. Three points, three marks. I did "
           "not write a paragraph, I wrote three reasons. Now the paper is yours."),
    illuminator=("A command-word reference card drawn as a table: each command word with icon + "
                 "word + what the answer must contain + a one-line worked example. A second panel "
                 "shows a 3-mark answer with each scoring point bracketed and numbered 1, 2, 3."),
  ),
  wedo1=dict(
    heading="What does the question want?",
    prompt="Name the command word's demand before you tap.",
    items=[
      ("Describe what happens to a potato in pure water. [2]", "What happens — no reason required"),
      ("Explain why it gains mass. [3]", "Reasons — three of them"),
      ("Calculate the percentage change. [2]", "Working plus answer"),
      ("Compare diffusion and active transport. [4]", "Both sides — similarities and differences"),
      ("State the magnification equation. [1]", "One line, no explanation needed"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("This is the show-me lesson: you work independently, then repair a weak answer against "
           "the board. 'It goes in because of osmosis' names the process but gives no reason, so it "
           "scores one at most. Add the water-concentration comparison and the membrane, and the "
           "same sentence reaches three. Mark your own METHOD, never a grade."),
    capture="Photograph the pupil's improved version alongside the original weak answer — the pair shows the progress.",
  ),
  wedo2=dict(
    heading="What is missing?",
    pills=[
      ("'It spreads out.' (Explain diffusion, 3 marks)", "MISSING: net movement, gradient, direction"),
      ("'400' (Calculate magnification, 2 marks)", "MISSING: working — and check whether a unit is needed"),
      ("'Active transport is different.' (Compare, 4 marks)", "MISSING: both sides, named, with detail"),
      ("'Water moves in.' (Explain mass gain, 3 marks)", "MISSING: why — water concentration comparison and the membrane"),
      ("A neat three-paragraph answer to a 1-mark 'state'", "NOT MISSING ANYTHING — but it cost time it did not need"),
      ("'×400' with equation and substitution shown (Calculate)", "COMPLETE — method and answer"),
    ],
    wagoll=("Explain why oxygen diffuses into the blood at the alveoli. [3] — The concentration of "
            "oxygen is higher in the alveolus than in the blood (1), so oxygen diffuses down the "
            "concentration gradient (1). The alveolus wall is one cell thick, so the diffusion "
            "distance is short and the rate is high (1)."),
  ),
  independent=dict(
    supported="Six exam-style questions with the command word highlighted and sentence starters provided.",
    standard="Eight exam-style questions across Topic 1, including one calculation and one 'explain'.",
    stretch="Eight exam-style questions including a 4-mark compare, then review two of your own answers and state what would gain the missing mark.",
  ),
  lundy=dict(
    space="Exam-style work raises the temperature for some people. This is practice, it is not the assessment — the assessment is separate and you will know when it is happening.",
    voice="Challenge a question that seems unfair. Sometimes the question is the problem.",
    audience="Your improved answers go into the Topic 1 folder and are the revision set before the assessment.",
    influence="The class chooses which two question types get retaught before the Topic 1 assessment.",
  ),
  exit=dict(
    supported="What does 'calculate' ask you to show as well as the answer?",
    standard="What must an 'explain' answer contain that a 'describe' answer does not?",
    stretch="A 4-mark 'compare' question — describe the structure of a full-mark answer.",
  ),
  exit_key=["your working",
            "a reason — why it happens, not just what happens",
            "Both processes named, at least one similarity and differences addressed on both sides, roughly four distinct points."],
  witness=[
    "Distinguished describe, explain and calculate.",
    "Showed full working on a calculation question.",
    "Identified the missing element in a weak answer.",
  ],
  ta_rule="ONE RULE: count the marks, then find that many separate points. Length is not the target.",
  ta_notes=[
    "NO mark schemes or grade descriptors are used or displayed. Feedback is 'this point is missing', never a predicted grade.",
    "The Topic 1 assessment is on PythonAnywhere and is separate from this lesson. Say so plainly — pupils manage practice better when they know it is not the real thing.",
  ],
  coldcall=[
    ("Watch me answer a 3-mark 'explain'", "How many separate points was I hunting?"),
    ("What does the question want?", "What does 'compare' need that 'describe' does not?"),
    ("What is missing?", "What is missing from 'it spreads out'?"),
  ],
  uas="AQA UAS: 'Cells and transport'; revision and exam technique.",
),
]
