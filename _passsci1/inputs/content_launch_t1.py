# -*- coding: utf-8 -*-
"""
LAUNCH science — Topic 1 (SoW W3 Magnification), expanded to the 3-lesson arc
(Block-2 §4): Discover -> Use -> Master. LAUNCH gets 3 periods/week, so one lesson per
period. Lesson 2 (Use) is the authored seed from content_launch.py, kept as the arc's spine.

Edexcel GCSE (9-1) Biology 1BI0 FOUNDATION (grades 1-5) / Combined 1SC0 F.
Pitched from the read-only biology/ reference: the predict -> measure -> close-the-loop
evidence mechanic, upgraded so PUPILS do the recording and TAs have a defined job.

HOUSE RULES: no mark schemes / grade descriptors (UAS route); model answers & WAGOLLs are
fine. Icon+label+colour. Answers staff-side. TA brief opens with ONE rule. Maths scaffolds
at every tier. Real GCSE command words.
"""

STRAND = "Science"
PATHWAY = "LAUNCH"
COLOUR = "#7A5C9E"
SPINE = "Edexcel GCSE Biology 1BI0 Foundation · Paper 1 · Topic 1"
AWARD = ("Pearson Edexcel GCSE (9–1) Biology 1BI0 (Foundation, grades 1–5); "
         "GCSE Combined Science 1SC0 F where appropriate; AQA UAS science units")
THEME = "Identity &amp; Belonging"
SLOT_WEEKS = 7
SENSORY = ("Microscope work means close focus, glassware and queueing for equipment. Agree who "
           "handles glass before the lesson. A pupil who records, calculates or photographs the "
           "result is doing assessed work — handling the slide is not the science.")

LESSONS = [

# ============================================================ W3 · L1 · DISCOVER
dict(
  week=3, slug="SCI_L_W3_L1_Microscopy",
  title="Discover: Cells Under the Microscope",
  sow="Aut1·W3 (Discover) — Why we magnify, and what a microscope actually does.",
  lo="I can describe how a light microscope magnifies cells, and why resolution matters as well as magnification.",
  sc=[
    "I can name the two lenses that do the magnifying.",
    "I can state that magnification makes the image bigger and resolution makes it clearer.",
    "I can explain why a bigger magnification is not always a better image.",
  ],
  ko_vocab=[
    ("microscope", "An instrument that makes very small things look much bigger."),
    ("magnification", "How many times bigger the image is than the real object."),
    ("resolution", "The smallest gap that can still be seen as two separate things."),
    ("eyepiece lens", "The lens you look through, usually ×10."),
    ("objective lens", "The lens near the slide; you choose ×4, ×10 or ×40."),
  ],
  ko_facts=[
    "Cells are far too small to see with the naked eye — we need a microscope.",
    "Total magnification = eyepiece lens × objective lens. ×10 with ×40 = ×400.",
    "Magnification makes the image BIGGER; resolution makes it CLEARER. They are not the same.",
    "A light microscope magnifies to about ×1500; an electron microscope reaches far higher AND has better resolution.",
    "Blowing an image up past the resolution limit just gives a bigger blur, not more detail.",
  ],
  misconceptions=[
    ("A bigger magnification is always a better image.",
     "Only if the resolution can keep up. Past the limit you get a bigger blur, not more detail."),
    ("Magnification and resolution are the same thing.",
     "Magnification is how much bigger; resolution is how much detail. A phone can zoom (magnify) a blurry photo without adding detail."),
    ("One lens does the magnifying.",
     "Two lenses multiply together — the eyepiece and the objective."),
  ],
  arrival=dict(
    supported="From the word bank, label the lens you look through and the lens near the slide.",
    standard="Name the two lenses on a microscope and say which one you look through.",
    stretch="Name the two lenses, and work out the total magnification of a ×10 eyepiece with a ×40 objective.",
  ),
  glance=["Name the lenses", "Magnify vs resolve", "Why bigger isn't always better"],
  ido1=dict(
    heading="Watch me set the microscope up",
    think=("Slide on the stage, clip it down, lowest objective first — the ×4. I look through the "
           "eyepiece and use the coarse focus to bring the cells in, then switch to ×10 for more "
           "magnification. Every time I change the objective I ask the same question: is the image "
           "bigger AND clearer, or just bigger? If it is just bigger and blurry, I have run past the "
           "resolution."),
    illuminator=("Labelled light microscope on the bench: eyepiece lens tagged '● EYEPIECE ×10', "
                 "the revolving objectives tagged '■ OBJECTIVE ×4/×10/×40', the stage with a "
                 "slide clipped on, the focus wheel and the light. Beside it, two small image circles: "
                 "one 'BIGGER · CLEARER' and one 'BIGGER · BLURRY' so magnification and resolution "
                 "read apart. Labels horizontal, icon + word."),
  ),
  wedo1=dict(
    heading="Bigger, clearer, or both?",
    prompt="Decide before you tap.",
    items=[
      ("Switching from ×4 to ×10 objective", "BIGGER — more magnification"),
      ("An electron microscope vs a light one", "BIGGER AND CLEARER — more magnification and better resolution"),
      ("Zooming a blurry photo on a phone", "BIGGER ONLY — no extra detail, resolution unchanged"),
      ("Eyepiece ×10 with objective ×40", "Total ×400"),
      ("Which lens do you look through?", "The eyepiece"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("You run the loop, not me. Focus the slide, then DRAW what you actually see in a circle "
           "— not what the textbook shows — and label it with the total magnification you used. "
           "The drawing plus the magnification is the evidence. Say the sentence as you write it: "
           "'I used a total magnification of ____ and I could see ____.'"),
    capture="Photograph the pupil's own labelled drawing with the magnification recorded — their record, in their hand.",
  ),
  wedo2=dict(
    heading="Light or electron?",
    pills=[
      ("Magnifies to about ×1500", "LIGHT MICROSCOPE"),
      ("Reaches far higher magnification", "ELECTRON MICROSCOPE"),
      ("Better resolution, finer detail", "ELECTRON MICROSCOPE"),
      ("Uses two glass lenses and light", "LIGHT MICROSCOPE"),
      ("Found in most school labs", "LIGHT MICROSCOPE"),
      ("Makes the image bigger but no clearer", "NOT A MICROSCOPE JOB — that is magnification without resolution"),
    ],
    wagoll=("A light microscope uses two lenses and light to magnify cells to about ×1500. An "
            "electron microscope gives both higher magnification and better resolution, so it shows "
            "much finer detail."),
  ),
  independent=dict(
    supported="Label a microscope diagram from the word bank, then write which lens you look through and what magnification does.",
    standard="Label the microscope, calculate three total magnifications, and write one sentence on the difference between magnification and resolution.",
    stretch="Label the microscope, calculate the magnifications, and explain why an electron microscope shows detail a light microscope cannot, using the word resolution.",
  ),
  lundy=dict(
    space="Close focus and queueing for the microscope can be a lot. You can be the one who records and draws while a partner focuses — the drawing is the assessed part.",
    voice="If your image will not come clear, say so — blurry might mean you have run past the resolution, and that is worth knowing.",
    audience="Your labelled drawing goes into your Topic 1 folder and is revisited at W7.",
    influence="The class decides which specimen slide we all look at next lesson.",
  ),
  exit=dict(
    supported="Name the lens you look through on a microscope.",
    standard="What is the difference between magnification and resolution?",
    stretch="Explain why a bigger magnification is not always a better image.",
  ),
  exit_key=["the eyepiece (lens)",
            "Magnification makes the image bigger; resolution makes it clearer / shows finer detail.",
            "Past the resolution limit the extra magnification only enlarges the blur, so no new detail appears."],
  witness=[
    "Named the eyepiece and objective lenses.",
    "Distinguished magnification from resolution.",
    "Produced a labelled drawing with the magnification recorded.",
  ],
  ta_rule="ONE RULE: magnification makes it BIGGER, resolution makes it CLEARER. Keep the two words apart.",
  ta_notes=[
    "Your job this lesson is the drawing station: make sure every pupil draws what THEY see and writes the magnification — not a copied textbook image. That record is the evidence.",
    "Glass slides and focus: agree who handles the slide. A pupil who draws and records has met the outcome without touching glass.",
  ],
  coldcall=[
    ("Watch me set the microscope up", "What question do I ask every time I change the objective?"),
    ("Bigger, clearer, or both?", "Does zooming a blurry photo add detail?"),
    ("Light or electron?", "Which one gives better resolution?"),
  ],
  uas="AQA UAS: 'Using a microscope'.",
),

# ============================================================ W3 · L2 · USE (seed)
dict(
  week=3, slug="SCI_L_W3_L2_Magnification",
  title="Use: Calculating Magnification",
  sow="Aut1·W3 (Use) — Calculate magnification (links Maths; record in spreadsheet).",
  lo="I can calculate magnification, image size and actual size, and convert between mm and µm.",
  sc=[
    "I can state the magnification equation and rearrange it.",
    "I can convert between millimetres and micrometres correctly.",
    "I can calculate total magnification from the two lenses.",
  ],
  ko_vocab=[
    ("magnification", "How many times bigger the image is than the real object."),
    ("image size", "The size of the object as it appears (measured on the picture)."),
    ("actual size", "The real size of the object."),
    ("micrometre (µm)", "One thousandth of a millimetre. 1 mm = 1000 µm."),
    ("resolution", "The smallest gap that can still be seen as two separate things."),
  ],
  ko_facts=[
    "magnification = image size ÷ actual size",
    "Rearranged: actual size = image size ÷ magnification; image size = actual size × magnification.",
    "Total magnification = eyepiece lens × objective lens. ×10 eyepiece with ×40 objective = ×400.",
    "1 mm = 1000 µm. 1 µm = 0.001 mm.",
    "Magnification has NO units — it is a ratio. Write ×400, not 400 mm.",
  ],
  misconceptions=[
    ("Magnification has units.",
     "It is a ratio of two lengths, so the units cancel. ×400, never 400 mm."),
    ("Bigger magnification always means a better image.",
     "Not without resolution. Blow up a blurred photo and you get a bigger blur."),
    ("You can mix mm and µm in one calculation.",
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
           "units the same? Yes, both millimetres, so I can divide. 40 ÷ 0.1 = 400. Magnification "
           "×400. No units on the answer. If they had NOT matched, converting would have been "
           "step one, before anything else."),
    illuminator=("Formula triangle drawn with IMAGE SIZE on top, MAGNIFICATION and ACTUAL SIZE "
                 "below, each labelled in full words plus a symbol tag. Beside it, a conversion "
                 "ladder: 'mm —×1000→ µm' and 'µm —÷1000→ mm', "
                 "with the direction written out. All labels horizontal, no colour-only coding."),
  ),
  wedo1=dict(
    heading="Work it out before you tap",
    prompt="Pen down, answer in your head, then check.",
    items=[
      ("Image 30 mm, actual 0.15 mm. Magnification?", "×200"),
      ("Magnification ×500, image 25 mm. Actual size?", "0.05 mm (= 50 µm)"),
      ("Eyepiece ×10, objective ×40. Total?", "×400"),
      ("Convert 0.02 mm to µm", "20 µm"),
      ("Convert 750 µm to mm", "0.75 mm"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("Set every calculation out the same way, because the method carries marks even when "
           "the answer slips: equation, then units check, then substitution, then answer with "
           "the multiplication sign. Four lines, every time. You write them, not me."),
    capture="Photograph the pupil's four-line working for one calculation — the layout is the evidence, not just the answer.",
  ),
  wedo2=dict(
    heading="Spot the error",
    pills=[
      ("Magnification = ×400", "CORRECT"),
      ("Magnification = 400 mm", "ERROR — magnification has no units"),
      ("40 mm ÷ 100 µm = 0.4", "ERROR — units not converted first"),
      ("Actual = image ÷ magnification", "CORRECT"),
      ("Actual = image × magnification", "ERROR — rearranged the wrong way"),
      ("Total mag = eyepiece × objective", "CORRECT"),
    ],
    wagoll=("magnification = image size ÷ actual size. Both in mm: 40 ÷ 0.1. "
            "magnification = ×400."),
  ),
  independent=dict(
    supported="Six calculations with the equation and a worked example printed on the sheet. Units already matched.",
    standard="Eight calculations including two that need unit conversion first, plus one rearrangement.",
    stretch="Eight calculations including conversions and rearrangements, then record your results in the spreadsheet and add a column showing total magnification for each lens pair.",
  ),
  lundy=dict(
    space="Calculation under pressure is its own barrier. The equation stays on the board all lesson — you are not being tested on remembering it today.",
    voice="If you think my worked example is wrong, stop me. Twice a year somebody is right.",
    audience="Your spreadsheet goes into your Topic 1 folder and is revisited at W7.",
    influence="The class decides which calculation type gets extra practice before the assessment.",
  ),
  exit=dict(
    supported="Write the magnification equation.",
    standard="A cell is 0.2 mm. The image is 60 mm. Calculate the magnification.",
    stretch="An image is 45 mm wide at ×900. Give the actual size in µm.",
  ),
  exit_key=["magnification = image size ÷ actual size",
            "×300",
            "45 ÷ 900 = 0.05 mm = 50 µm"],
  witness=[
    "Stated and rearranged the magnification equation.",
    "Converted correctly between mm and µm.",
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

# ============================================================ W3 · L3 · MASTER
dict(
  week=3, slug="SCI_L_W3_L3_ExamSkills",
  title="Master: Magnification Exam Questions",
  sow="Aut1·W3 (Master) — Answer exam-style magnification questions independently.",
  lo="I can answer exam-style magnification questions independently, showing full working and the correct units.",
  sc=[
    "I can read the command word and give exactly what it asks for.",
    "I can show four-line working on a calculation.",
    "I can check my answer has the right unit, or no unit for magnification.",
  ],
  ko_vocab=[
    ("calculate", "Work out a number. Show your working; give the unit (or × for magnification)."),
    ("describe", "Say what you see or what happens. No reason needed."),
    ("explain", "Say WHY. The word 'because' usually belongs in the answer."),
    ("estimate", "Give a sensible value from the scale bar or the information given."),
    ("scale bar", "A line on an image labelled with the real length it represents."),
  ],
  ko_facts=[
    "Calculations: show the equation and substitute even if the final number slips — method carries marks.",
    "Magnification has no unit; every other quantity (mm, µm) does. Check before you write the answer.",
    "A scale bar lets you find actual size: measure the bar, then use its real length to scale.",
    "Convert mm and µm to match BEFORE dividing — the most common dropped mark.",
    "Read the command word first: 'calculate' wants a number and working; 'describe' wants what, not why.",
  ],
  misconceptions=[
    ("If I cannot finish the calculation, I leave it blank.",
     "Write the equation and substitute. Method marks are real marks you can still get."),
    ("A neat long answer scores more.",
     "Marks follow the command word and the points, not length. Give exactly what is asked."),
    ("The scale bar is decoration.",
     "The scale bar is the data — it is how you get the actual size."),
  ],
  arrival=dict(
    supported="Match the command word to what it asks: calculate / describe / explain.",
    standard="Write what 'calculate' asks you to show as well as the final number.",
    stretch="Write what 'calculate', 'describe' and 'estimate' each require in a magnification question.",
  ),
  glance=["Read the command word", "Four-line working", "Check the unit"],
  ido1=dict(
    heading="Watch me answer a 'calculate'",
    think=("'A cell image is 60 mm wide. The real cell is 0.15 mm. Calculate the magnification. [2]' "
           "Command word is calculate — number plus working. Line one: equation. Line two: units "
           "match? Both mm, yes. Line three: 60 ÷ 0.15. Line four: ×400, no unit. Two marks: one "
           "for the method, one for the answer. Now you run the loop on your own questions."),
    illuminator=("A worked exam answer shown as four numbered lines — EQUATION, UNITS CHECK, "
                 "SUBSTITUTE, ANSWER (×, no unit) — each line tagged. Beside it a command-word "
                 "card: 'CALCULATE → number + working', 'DESCRIBE → what you see', "
                 "'ESTIMATE → use the scale bar'. Labels horizontal, icon + word."),
  ),
  wedo1=dict(
    heading="What does the question want?",
    prompt="Name the demand before you tap.",
    items=[
      ("Calculate the magnification. [2]", "A number, with working shown"),
      ("Describe what the cell looks like. [2]", "What you see — no reason needed"),
      ("Give the actual size in µm. [2]", "Convert the units, then answer with µm"),
      ("Estimate the width using the scale bar. [1]", "Read the scale bar for the real length"),
      ("Magnification = 400. Correct? ", "Add the × and drop any unit — ×400"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("This is the show-me lesson, so the working IS the witness evidence. Answer three "
           "exam-style questions with the four-line layout, then mark your OWN working against the "
           "board: did the equation appear? did the units match? is the unit right? Tick each line "
           "you completed. You are marking method, never awarding a grade."),
    capture="Photograph one full four-line answer the pupil completed unaided — the independent working is the strongest evidence in the topic.",
  ),
  wedo2=dict(
    heading="What is missing?",
    pills=[
      ("'400' (Calculate magnification, 2 marks)", "MISSING: working — and check no unit is needed"),
      ("'It is round and purple.' (Describe, 2 marks)", "NOT MISSING ANYTHING — describe wants what you see"),
      ("'40 mm ÷ 100 µm' (Calculate, 2 marks)", "MISSING: convert the units first"),
      ("A full page for a 1-mark 'state'", "NOT MISSING — but it cost time it did not need"),
      ("'Actual = image × magnification'", "WRONG REARRANGEMENT — it should be ÷ magnification"),
      ("'×400' with equation and substitution shown", "COMPLETE — method and answer both there"),
    ],
    wagoll=("Calculate the magnification. [2] — magnification = image size ÷ actual size (1). "
            "Units match (mm): 60 ÷ 0.15 = ×400 (1). No unit on magnification."),
  ),
  independent=dict(
    supported="Four exam-style questions with the command word highlighted and the four-line layout printed to fill in.",
    standard="Six exam-style questions across magnification, including one conversion and one scale-bar estimate, four-line working throughout.",
    stretch="Six exam-style questions including a scale-bar calculation, then review two of your own answers and write which line would gain the missing method mark.",
  ),
  lundy=dict(
    space="Exam-style work raises the temperature. This is practice — the real Topic 1 assessment is separate and you will know when it happens.",
    voice="Challenge any question that seems unfair. Sometimes the question is the problem, not you.",
    audience="Your independent answers go into the Topic 1 folder and are the revision set before the assessment.",
    influence="The class chooses which question type gets one more worked example before moving on.",
  ),
  exit=dict(
    supported="What does 'calculate' ask you to show as well as the answer?",
    standard="An image is 50 mm; the real object is 0.1 mm. Calculate the magnification.",
    stretch="An image is 36 mm wide at ×600. Give the actual size in µm, showing your working.",
  ),
  exit_key=["your working (the method)",
            "×500",
            "36 ÷ 600 = 0.06 mm = 60 µm"],
  witness=[
    "Read the command word and answered to it.",
    "Showed four-line working on a calculation.",
    "Checked the unit (or no unit for magnification) before finishing.",
  ],
  ta_rule="ONE RULE: read the command word first, then give exactly what it asks — no more, no less.",
  ta_notes=[
    "This is the show-me lesson: pupils work independently and mark their own METHOD against the board. Never a predicted grade — 'this line is missing', not 'this is a grade 3'.",
    "The Topic 1 assessment is separate (on PythonAnywhere). Say so plainly — pupils manage practice better knowing it is not the real thing.",
  ],
  coldcall=[
    ("Watch me answer a 'calculate'", "How many marks, and what does each one need?"),
    ("What does the question want?", "Does 'describe' need a reason?"),
    ("What is missing?", "What is missing from just writing '400'?"),
  ],
  uas="AQA UAS: 'Using a microscope'; 'Scientific calculations'; exam technique.",
),
]
