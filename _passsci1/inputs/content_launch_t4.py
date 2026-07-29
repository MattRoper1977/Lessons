# -*- coding: utf-8 -*-
"""
LAUNCH science — Topic 4 (SoW W6 Active transport), 3-lesson arc.
L1 Discover: the authored seed. L2 Use: apply active transport to root hairs and the gut, with
data. L3 Master: 'compare' exam technique across all three transport processes.
No mark schemes (UAS). Real command words. Icon+label+colour.
"""

STRAND = "Science"
PATHWAY = "LAUNCH"
COLOUR = "#7A5C9E"
SPINE = "Edexcel GCSE Biology 1BI0 Foundation · Paper 1 · Topic 1"
AWARD = ("Pearson Edexcel GCSE (9–1) Biology 1BI0 (Foundation, grades 1–5); "
         "GCSE Combined Science 1SC0 F where appropriate; AQA UAS science units")
THEME = "Identity &amp; Belonging"
SLOT_WEEKS = 7
SENSORY = ("This topic is model- and data-based — comparison tables and graphs. A pupil who reads "
           "the data, completes the table or explains the pattern is doing the assessed science.")

LESSONS = [

# ============================================================ W6 · L1 · DISCOVER (seed)
dict(
  week=6, slug="SCI_L_W6_L1_ActiveTransport",
  title="Discover: Active Transport",
  sow="Aut1·W6 (Discover) — Explain active transport and distinguish it from diffusion and osmosis.",
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
    "Active transport moves substances from LOW to HIGH concentration — against the gradient.",
    "It requires energy released by respiration.",
    "It uses carrier proteins in the cell membrane.",
    "Root hair cells absorb mineral ions from dilute soil water by active transport.",
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
    think=("Three columns, three questions each time. Which way relative to the gradient? Does it "
           "need energy? What is moving? Diffusion: down, no, any particle. Osmosis: down, no, water "
           "only, and it needs the partially permeable membrane. Active transport: UP, yes, and it "
           "needs carrier proteins. Fill that table and you can answer any comparison question."),
    illuminator=("Three-column comparison, each headed with icon + word: '↓ DIFFUSION', "
                 "'↓ OSMOSIS (WATER)', '↑ ACTIVE TRANSPORT'. Rows: direction, energy needed, what "
                 "moves, membrane needed. Beside it a root hair cell with mitochondria labelled "
                 "'ENERGY FROM RESPIRATION'. Labels horizontal."),
  ),
  wedo1=dict(
    heading="Which process?",
    prompt="Decide before you tap.",
    items=[
      ("Oxygen into the blood at the alveoli", "↓ Diffusion"),
      ("Water into a root hair cell", "↓ Osmosis"),
      ("Mineral ions into a root hair from dilute soil", "↑ Active transport"),
      ("Glucose from the gut into higher-concentration blood", "↑ Active transport"),
      ("Carbon dioxide out of a cell", "↓ Diffusion"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("You give the answer shape for the classic question: 'Mineral ions move into the root "
           "hair cell by active transport because their concentration is HIGHER inside the cell "
           "than in the soil water. Moving against the gradient requires energy, released by "
           "respiration in the mitochondria.' Direction, then why energy is needed, then source."),
    capture="Photograph the pupil's completed three-column comparison table.",
  ),
  wedo2=dict(
    heading="True or false?",
    pills=[
      ("Active transport needs energy", "TRUE"),
      ("Diffusion needs energy", "FALSE"),
      ("Active transport moves substances up the gradient", "TRUE"),
      ("Active transport is just faster diffusion", "FALSE — the direction is what differs"),
      ("Cells doing active transport have many mitochondria", "TRUE"),
      ("Osmosis moves any particle", "FALSE — osmosis moves water only"),
    ],
    wagoll=("Root hair cells absorb mineral ions by active transport because the concentration of "
            "ions is already higher inside the cell than in the soil. Moving them against the "
            "concentration gradient requires energy released by respiration, which is why root hair "
            "cells contain many mitochondria."),
  ),
  independent=dict(
    supported="Complete the three-column comparison table from the word bank, then label the root hair cell.",
    standard="Complete the comparison table unaided, label the root hair cell, and answer two application questions.",
    stretch="Complete the table, answer the application questions, and explain what would happen to mineral uptake if a plant's roots were waterlogged and short of oxygen.",
  ),
  lundy=dict(
    space="Three processes at once is a genuine memory load. The comparison table stays visible all lesson — that is deliberate.",
    voice="If you can defend a different answer on the sorting task, defend it. Some of these are genuinely close.",
    audience="Your comparison table goes into the Topic 1 folder and is the core revision tool at W7.",
    influence="The class decides which of the three processes gets extra practice next lesson.",
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
    "This is the lesson where the three processes get confused. The comparison table is the intervention — keep it in front of every pupil.",
    "The waterlogging question links to respiration, taught later. Accept 'no oxygen means less energy' as the reasoning.",
  ],
  coldcall=[
    ("Watch me compare the three", "Which one moves water only?"),
    ("Which process?", "Why is the mineral ion example not diffusion?"),
    ("True or false?", "Is active transport just faster diffusion?"),
  ],
  uas="AQA UAS: 'Cells and transport'.",
),

# ============================================================ W6 · L2 · USE
dict(
  week=6, slug="SCI_L_W6_L2_RootAndGut",
  title="Use: Active Transport in Root Hairs and the Gut",
  sow="Aut1·W6 (Use) — Apply active transport to real cells and interpret uptake data.",
  lo="I can apply active transport to root hair and gut cells, and use data to link it to respiration.",
  sc=[
    "I can explain how a root hair cell absorbs mineral ions against the gradient.",
    "I can explain how the gut absorbs glucose when the blood already has more.",
    "I can read a graph to show active transport depends on respiration.",
  ],
  ko_vocab=[
    ("root hair cell", "A plant cell with a long thin hair that absorbs water and minerals."),
    ("mineral ion", "A dissolved nutrient a plant needs, e.g. nitrate, from the soil."),
    ("villi", "Tiny folds in the small intestine that absorb digested food."),
    ("uptake", "The rate at which a cell takes a substance in."),
    ("oxygen", "Needed for respiration, which powers active transport."),
  ],
  ko_facts=[
    "Root hair cells absorb mineral ions from dilute soil, where the ions are LESS concentrated than inside — so it must be active transport.",
    "The gut absorbs glucose into the blood even when blood glucose is already higher — against the gradient, so active transport.",
    "Both root hair and gut cells contain MANY mitochondria to supply the energy.",
    "If oxygen is removed, respiration slows, less energy is made, and the rate of uptake falls.",
    "A graph of uptake against oxygen shows uptake rising as oxygen rises — the link to respiration.",
  ],
  misconceptions=[
    ("Roots suck minerals in like a straw.",
     "There is no suction. Carrier proteins move ions in, powered by respiration — active transport."),
    ("The gut only uses diffusion.",
     "When blood glucose is already higher, diffusion would go the wrong way. The gut uses active transport."),
    ("Oxygen has nothing to do with mineral uptake.",
     "Oxygen powers respiration; respiration powers active transport. Less oxygen, less uptake."),
  ],
  arrival=dict(
    supported="From the word bank, name the part of the plant cell that absorbs mineral ions.",
    standard="Why can a root hair cell not use diffusion to absorb mineral ions?",
    stretch="Explain why a root hair cell must use active transport rather than diffusion for minerals.",
  ),
  glance=["Root hair uptake", "Gut glucose uptake", "Read the oxygen graph"],
  ido1=dict(
    heading="Watch me read the data — then you apply it",
    think=("Graph: rate of mineral uptake up the side, oxygen along the bottom. As oxygen rises, "
           "uptake rises. Why? More oxygen means more respiration, more energy, so more active "
           "transport. Take the oxygen away and the line drops — because active transport runs on "
           "the energy from respiration. Now you apply the same reasoning to the gut."),
    illuminator=("A root hair cell reaching into soil: mineral ions moving IN against the gradient "
                 "through a carrier protein, tagged '↑ AGAINST THE GRADIENT', with mitochondria "
                 "tagged '⚙ ENERGY FROM RESPIRATION'. Beside it a small-intestine villus absorbing "
                 "glucose tagged '↑ GLUCOSE IN'. A mini-graph shows uptake rising with oxygen. "
                 "Labels horizontal."),
  ),
  wedo1=dict(
    heading="Diffusion or active transport?",
    prompt="Decide before you tap.",
    items=[
      ("Mineral ions into a root hair from dilute soil", "Active transport — against the gradient"),
      ("Water into the root hair", "Osmosis — down the water gradient"),
      ("Glucose into blood that already has more glucose", "Active transport — against the gradient"),
      ("Oxygen removed from the roots", "Uptake FALLS — less respiration, less energy"),
      ("Why so many mitochondria?", "To supply the energy for active transport"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("You explain the gut, out loud as you write: 'Glucose is absorbed into the blood by "
           "active transport because its concentration is already higher in the blood than in the "
           "gut. Moving it against the gradient needs energy from respiration, so gut cells have "
           "many mitochondria.' Direction, reason, source. Then read the oxygen graph the same way."),
    capture="Photograph the pupil's annotated graph with their sentence linking uptake to respiration.",
  ),
  wedo2=dict(
    heading="Match the cell feature to its job",
    pills=[
      ("Long thin root hair", "Large surface area for absorption"),
      ("Many mitochondria", "Energy from respiration for active transport"),
      ("Carrier proteins in the membrane", "Move ions against the gradient"),
      ("Villi in the small intestine", "Large surface area to absorb glucose"),
      ("Uptake rises with oxygen", "Shows active transport depends on respiration"),
      ("Minerals sucked in like a straw", "NOT TRUE — carrier proteins move them, using energy"),
    ],
    wagoll=("A root hair cell absorbs mineral ions by active transport because the ions are more "
            "concentrated inside the cell than in the soil. Moving them against the gradient needs "
            "energy from respiration, so the cell has many mitochondria. When oxygen is low, "
            "respiration and uptake both fall."),
  ),
  independent=dict(
    supported="Label the root hair cell, then complete two sentences on why it uses active transport, from the word bank.",
    standard="Explain root hair and gut uptake, then describe what the oxygen–uptake graph shows.",
    stretch="Explain both examples, interpret the oxygen–uptake graph, and predict what happens to uptake if the roots are waterlogged.",
  ),
  lundy=dict(
    space="Reading graphs under time pressure is a barrier for some. The graph stays on the board and you may talk it through with a partner before writing.",
    voice="If the data seems to contradict the idea, say so — checking the claim against the graph is exactly the skill here.",
    audience="Your annotated graph and explanations go into the Topic 1 folder for the W7 review.",
    influence="The class chooses whether we apply this next to a plant example or a human one.",
  ),
  exit=dict(
    supported="Name the part of a root hair cell that supplies energy for active transport.",
    standard="Why does the gut use active transport, not diffusion, to absorb glucose?",
    stretch="Explain why mineral uptake falls when the oxygen around the roots is reduced.",
  ),
  exit_key=["the mitochondria",
            "Blood glucose is already higher, so diffusion would go the wrong way; active transport moves it against the gradient.",
            "Less oxygen means less respiration, so less energy is released for active transport, so the rate of uptake falls."],
  witness=[
    "Explained root hair mineral uptake as active transport.",
    "Explained gut glucose uptake against the gradient.",
    "Used the oxygen graph to link uptake to respiration.",
  ],
  ta_rule="ONE RULE: if it moves AGAINST the gradient, it is active transport and it needs energy from respiration.",
  ta_notes=[
    "Your job at the data station: make sure every pupil reads BOTH axes of the oxygen–uptake graph before explaining it. The reading is the evidence.",
    "Accept 'less oxygen means less energy' for the waterlogging idea; the full respiration link comes later in the course.",
  ],
  coldcall=[
    ("Watch me read the data — then you apply it", "Why does uptake rise as oxygen rises?"),
    ("Diffusion or active transport?", "Why is the glucose example not diffusion?"),
    ("Match the cell feature to its job", "What do the carrier proteins do?"),
  ],
  uas="AQA UAS: 'Cells and transport'.",
),

# ============================================================ W6 · L3 · MASTER
dict(
  week=6, slug="SCI_L_W6_L3_Compare",
  title="Master: Comparing the Three Processes",
  sow="Aut1·W6 (Master) — Answer 'compare' questions on diffusion, osmosis and active transport.",
  lo="I can answer 'compare' exam questions across the three transport processes independently.",
  sc=[
    "I can say what 'compare' asks for — both sides, similarities AND differences.",
    "I can compare any two of the three processes using direction, energy and what moves.",
    "I can write a full-mark compare answer with points on both sides.",
  ],
  ko_vocab=[
    ("compare", "Give similarities AND differences, both sides named."),
    ("similarity", "Something the two processes share."),
    ("difference", "Something that is not the same between them."),
    ("direction", "Down the gradient (diffusion, osmosis) or up it (active transport)."),
    ("energy", "Needed for active transport; not for diffusion or osmosis."),
  ],
  ko_facts=[
    "'Compare' means BOTH sides — a compare answer that talks about only one process scores half at best.",
    "Compare the three on three things: direction, energy needed, and what moves.",
    "Diffusion and active transport share: both move substances across a membrane. They differ in direction and energy.",
    "Osmosis is diffusion of water; active transport moves substances against the gradient using energy.",
    "A 4-mark compare wants about four distinct points, spread across both processes.",
  ],
  misconceptions=[
    ("Compare means describe one, then the other.",
     "Compare means put them side by side — say what is the SAME and what is DIFFERENT."),
    ("You only need the differences.",
     "'Compare' rewards similarities too. Name at least one thing they share."),
    ("Writing more always scores more.",
     "Marks follow distinct points across both sides, not length."),
  ],
  arrival=dict(
    supported="Match the process to its direction: diffusion / active transport → down / up the gradient.",
    standard="Write one similarity and one difference between diffusion and active transport.",
    stretch="Compare diffusion and active transport using direction, energy and what moves.",
  ),
  glance=["What 'compare' asks", "Both sides", "Direction · energy · what moves"],
  ido1=dict(
    heading="Watch me answer a 4-mark 'compare'",
    think=("'Compare diffusion and active transport. [4]' Compare means both sides — similarities "
           "and differences. Similarity: both move substances across the cell membrane. Difference "
           "one: diffusion goes DOWN the gradient, active transport goes UP. Difference two: "
           "diffusion needs no energy, active transport needs energy from respiration. That is four "
           "points, spread across both. Now you run a compare of your own."),
    illuminator=("A two-column compare table for DIFFUSION vs ACTIVE TRANSPORT with rows "
                 "'direction', 'energy?', 'what moves' — both columns filled, the SAME row "
                 "highlighted as a shared similarity. Beside it a command-word card: "
                 "'COMPARE → similarities AND differences, both sides'. Labels horizontal."),
  ),
  wedo1=dict(
    heading="Similarity or difference?",
    prompt="Decide before you tap.",
    items=[
      ("Both move substances across a membrane", "SIMILARITY"),
      ("One goes down the gradient, one up", "DIFFERENCE — direction"),
      ("Only one needs energy", "DIFFERENCE — energy"),
      ("Osmosis and diffusion both need no energy", "SIMILARITY"),
      ("A compare answer about only diffusion", "INCOMPLETE — missing the other side"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("Show-me lesson: you write a full compare answer, then mark your OWN against the board — "
           "did you give a similarity? at least two differences? cover BOTH processes? Tick each. "
           "The independent compare answer is the strongest evidence in this topic. Method, never a grade."),
    capture="Photograph the pupil's independent compare answer with both sides visibly covered.",
  ),
  wedo2=dict(
    heading="What is missing?",
    pills=[
      ("'Active transport is different.' (Compare, 4 marks)", "MISSING: both sides named, with detail"),
      ("Only differences, no similarity (Compare)", "MISSING: at least one similarity"),
      ("'Both cross the membrane; diffusion is down, active is up; only active needs energy.'", "STRONG — similarity + two differences"),
      ("A paragraph only about diffusion (Compare)", "MISSING: the active transport side"),
      ("'Diffusion is passive, active transport uses respiration energy.'", "A valid difference — energy"),
      ("'They are both types of movement.'", "TOO VAGUE — name the shared feature precisely"),
    ],
    wagoll=("Compare diffusion and active transport. [4] — Both move substances across the cell "
            "membrane (1). Diffusion moves them DOWN the concentration gradient, but active "
            "transport moves them UP, against it (1). Diffusion is passive and needs no energy (1), "
            "whereas active transport needs energy from respiration (1)."),
  ),
  independent=dict(
    supported="Complete a two-column compare table for two processes from the word bank, then write one similarity and one difference.",
    standard="Answer two compare questions across the three processes, each with a similarity and two differences.",
    stretch="Answer a 4-mark compare and a 6-mark compare of all three processes, then review one answer for a missing point.",
  ),
  lundy=dict(
    space="Exam-style work raises the temperature. This is practice — the Topic 1 assessment is separate and you will know when it happens.",
    voice="Challenge a question that seems unfair. Sometimes the question is the problem, not you.",
    audience="Your compare answers go into the Topic 1 folder and are the revision set before the assessment.",
    influence="The class chooses which pair of processes we compare together as a final model.",
  ),
  exit=dict(
    supported="What two things must a 'compare' answer include?",
    standard="Write one similarity and one difference between osmosis and active transport.",
    stretch="Compare diffusion and active transport in a full-mark answer.",
  ),
  exit_key=["similarities AND differences (both sides)",
            "Similarity: both move substances in/across cells. Difference: osmosis is passive (water, down gradient); active transport uses energy and goes up the gradient.",
            "Both move substances across the membrane; diffusion goes down the gradient with no energy, active transport goes up the gradient using energy from respiration."],
  witness=[
    "Stated that compare needs similarities and differences.",
    "Compared two processes using direction, energy and what moves.",
    "Wrote a compare answer covering both sides.",
  ],
  ta_rule="ONE RULE: compare = BOTH sides. One similarity, then the differences, across both processes.",
  ta_notes=[
    "No mark schemes or grade descriptors. Feedback names the missing side or point, never a predicted grade.",
    "The Topic 1 assessment is separate (PythonAnywhere). Say so plainly — practice lands better when pupils know it is not the real thing.",
  ],
  coldcall=[
    ("Watch me answer a 4-mark 'compare'", "How many points, and across how many processes?"),
    ("Similarity or difference?", "Name one thing diffusion and active transport share."),
    ("What is missing?", "What is missing from 'active transport is different'?"),
  ],
  uas="AQA UAS: 'Cells and transport'; exam technique.",
),
]
