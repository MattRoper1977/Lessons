# -*- coding: utf-8 -*-
"""
BUILD science — Autumn 1, weeks 3-7 (post-baseline).
Spine: White Rose Science Year 3 · Pearson Entry Level Science 8939 (E1->E3) · AQA UAS.
Theme: Identity & Belonging.

HOUSE RULES BAKED IN (do not "improve" these away):
  * Never code meaning by colour alone -> every classification carries ICON + LABEL + colour.
  * Body/food content is taught on MODELS AND DIAGRAMS, never on the pupils themselves.
    No comment on any pupil's body, size, weight or what they eat.
  * FoodWise framing only: Eatwell "everyday / sometimes". ZERO calorie, weight,
    restriction or "good vs bad food" language anywhere, at any tier.
  * Match pills may include DELIBERATE WRONG ANSWERS - they are classification items,
    never model answers, and must never be printed as advice.
  * Answer keys are STAFF-SIDE. Exit answers never appear on a pupil surface.
  * TA brief opens with ONE rule. (T4 audit: packs that open with one rule are the
    self-sufficient ones; most of the estate's packs don't.)
"""

STRAND = "Science"
PATHWAY = "BUILD"
COLOUR = "#4E7A9B"          # BUILD science steel-blue; distinct from Community #4E8093
SPINE = "White Rose Science Year 3"
AWARD = "Pearson Entry Level Science 8939 (E1\u2192E3); AQA UAS science units"
THEME = "Identity &amp; Belonging"
SLOT_WEEKS = 7
SENSORY = ("Bodies and food are personal. Teach every idea on the model, the diagram or "
           "the picture card \u2014 never on a pupil's own body, and never on what a pupil "
           "has eaten. If a pupil steps out, the diagram waits for them.")

LESSONS = [

# ---------------------------------------------------------------- W3
dict(
  week=3, slug="SCI_B_W3_Backbones",
  title="Backbones and No Backbones",
  sow="Aut1\u00b7W3 \u2014 Compare animals with and without a backbone (vertebrates and invertebrates).",
  lo="I can sort animals into those with a backbone and those without.",
  sc=[
    "I can find the backbone on a skeleton picture.",
    "I can name two animals with a backbone and two without.",
    "I can say one way an animal without a backbone is held up.",
  ],
  ko_vocab=[
    ("backbone", "A line of small bones down the middle of the back."),
    ("vertebrate", "An animal that HAS a backbone."),
    ("invertebrate", "An animal that has NO backbone."),
    ("skeleton", "All the bones in a body, working together."),
    ("support", "Holding something up so it keeps its shape."),
  ],
  ko_facts=[
    "A backbone is not one bone. It is many small bones in a line.",
    "Fish, birds, frogs, lizards and mammals are vertebrates.",
    "Insects, worms, snails, crabs and spiders are invertebrates.",
    "No backbone does not mean no support. A snail has a shell. A crab has a hard case. A worm is held up by the liquid inside it.",
  ],
  misconceptions=[
    ("Big animals have backbones, small ones don't.",
     "Size is not the test. A mouse is tiny and has a backbone. A lobster is big and has none."),
    ("Invertebrates are soft and floppy.",
     "Many are hard on the OUTSIDE instead \u2014 beetle, crab, snail."),
    ("The backbone is one long bone.",
     "Run a finger down the model: you feel bump, bump, bump. Many bones."),
  ],
  arrival=dict(
    supported="Point to the backbone on the skeleton picture on your desk.",
    standard="Write one animal you think has a backbone.",
    stretch="Write one animal you think has a backbone and one you think does not.",
  ),
  glance=["Find the backbone", "Sort eight animals", "Prove one of them"],
  ido1=dict(
    heading="Watch me find the backbone",
    think=("I am looking for a LINE of small bones down the middle of the back. "
           "Not the ribs \u2014 they curve round the side. Not the legs. The line down the middle. "
           "Bump, bump, bump. Found it. So this animal is a vertebrate."),
    illuminator=("Two side-by-side skeleton diagrams, labelled with word AND icon: "
                 "left = fish skeleton with the vertebral column picked out and tagged "
                 "'\u25cf BACKBONE'; right = beetle with hard outer case tagged "
                 "'\u25a0 HARD CASE OUTSIDE'. Labels horizontal, no colour-only coding."),
  ),
  wedo1=dict(
    heading="Backbone or no backbone?",
    prompt="Tap each animal. Say your answer BEFORE the card turns over.",
    items=[
      ("Robin", "Backbone \u2014 vertebrate"),
      ("Earthworm", "No backbone \u2014 invertebrate"),
      ("Frog", "Backbone \u2014 vertebrate"),
      ("Snail", "No backbone \u2014 invertebrate (shell on the outside)"),
      ("Trout", "Backbone \u2014 vertebrate"),
      ("Spider", "No backbone \u2014 invertebrate"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("I will show you my proof out loud so you can copy the shape: "
           "'The robin is a vertebrate BECAUSE I can see the line of small bones down its back.' "
           "Because. That word is where the evidence goes."),
    capture="Photograph the pupil's sorted card mat before it is cleared.",
  ),
  wedo2=dict(
    heading="Sort these into the right column",
    pills=[
      ("Bat", "Vertebrate"),
      ("Crab", "Invertebrate"),
      ("Snake", "Vertebrate"),
      ("Jellyfish", "Invertebrate"),
      ("It is furry", "NOT A TEST \u2014 fur tells you nothing about the backbone"),
      ("It is small", "NOT A TEST \u2014 size tells you nothing about the backbone"),
    ],
    wagoll=("The crab is an invertebrate because it has no line of bones down its back. "
            "It is held up by a hard case on the outside instead."),
  ),
  independent=dict(
    supported="Cut and stick eight animal cards onto the two-column mat. Word bank on the sheet.",
    standard="Sort the eight cards, then write one sentence: '____ is a vertebrate because ____.'",
    stretch="Sort the eight cards, write two 'because' sentences, and add one animal of your own to each column.",
  ),
  lundy=dict(
    space="Sorting cards means moving. If standing at the table helps you think, stand.",
    voice="If you disagree with where a card went, say so \u2014 that is science, not arguing.",
    audience="Two adults will read your 'because' sentence today.",
    influence="Your sorted mat goes on the Living Things Wall and stays up for the unit.",
  ),
  exit=dict(
    supported="Circle the vertebrate: worm / cat",
    standard="Name one vertebrate and one invertebrate.",
    stretch="Explain how you can tell an invertebrate without cutting it open.",
  ),
  exit_key=["cat", "any correct pair, e.g. cat / worm",
            "Look for a hard case or shell outside, or a soft body with no line of bones down the back."],
  witness=[
    "Located the backbone on a diagram unaided.",
    "Sorted animals into vertebrate / invertebrate.",
    "Gave a reason using the word 'because'.",
  ],
  ta_rule="ONE RULE: the test is the line of bones down the back \u2014 not size, not fur, not legs.",
  ta_notes=[
    "If a pupil is stuck, hand them the fish and the beetle only. Two cards, one difference.",
    "Do not ask pupils to feel their own or each other's spines. Use the model.",
  ],
  coldcall=[
    ("Watch me find the backbone", "What am I looking for \u2014 ribs or the line down the middle?"),
    ("Backbone or no backbone?", "Give me one animal with no backbone."),
    ("Sort these into the right column", "Why is 'it is furry' not a test?"),
  ],
  uas="AQA UAS: 'Grouping living things'.",
),

# ---------------------------------------------------------------- W4
dict(
  week=4, slug="SCI_B_W4_Muscle_Pairs",
  title="Muscles Work in Pairs",
  sow="Aut1\u00b7W4 \u2014 Explain how muscles work in pairs with bones to make the body move.",
  lo="I can explain that muscles work in pairs to move a bone.",
  sc=[
    "I can name the two muscles in the arm pair.",
    "I can say what happens to each muscle when the arm bends.",
    "I can show the pair working on a model.",
  ],
  ko_vocab=[
    ("muscle", "A soft part of the body that pulls."),
    ("contract", "The muscle gets shorter and tighter. It PULLS."),
    ("relax", "The muscle gets longer and softer. It stops pulling."),
    ("pair", "Two muscles that work together, taking turns."),
    ("joint", "The place where two bones meet and can move."),
  ],
  ko_facts=[
    "A muscle can only PULL. It can never push.",
    "That is why muscles come in pairs \u2014 one pulls the bone one way, the other pulls it back.",
    "Arm bends: biceps contracts, triceps relaxes.",
    "Arm straightens: triceps contracts, biceps relaxes.",
    "Bones do not move themselves. The muscle pulls the bone.",
  ],
  misconceptions=[
    ("Muscles push bones.",
     "Model it: string can pull a lever, it cannot push it. Muscles are the same."),
    ("One muscle does the whole job.",
     "If only one worked, the arm would bend and stay bent forever."),
    ("Relax means doing nothing.",
     "Relax means it is not pulling right now. It is still there, still attached, waiting its turn."),
  ],
  arrival=dict(
    supported="Bend your arm. Which side goes hard \u2014 top or underneath?",
    standard="Bend your arm and write which muscle you think is pulling.",
    stretch="Bend your arm, then straighten it. Write what changed.",
  ),
  glance=["Meet the pair", "Make the model move", "Explain the swap"],
  ido1=dict(
    heading="Watch me move the model arm",
    think=("Here is my cardboard arm with two elastic bands. I pull the TOP band \u2014 the arm bends. "
           "Notice the bottom band went long and loose. Now I pull the BOTTOM band \u2014 it straightens, "
           "and the top one goes long and loose. Neither band ever pushed. They took turns pulling."),
    illuminator=("Cardboard-arm model diagram, two frames side by side. Frame 1 'ARM BENDS': "
                 "top band drawn short and thick, tagged '\u25b2 BICEPS \u00b7 CONTRACTS \u00b7 PULLING'; "
                 "bottom band long and thin, tagged '\u25bd TRICEPS \u00b7 RELAXES'. Frame 2 'ARM "
                 "STRAIGHTENS': labels swapped. Icon + word on every tag."),
  ),
  wedo1=dict(
    heading="Which one is pulling?",
    prompt="Tap to check. Say it before the card turns.",
    items=[
      ("Arm bending up", "Biceps contracts \u00b7 triceps relaxes"),
      ("Arm straightening down", "Triceps contracts \u00b7 biceps relaxes"),
      ("Arm held still, bent", "Both doing a little \u2014 holding is work too"),
      ("Can a muscle push?", "No. Only pull. Ever."),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("Sentence shape for today: 'When the arm bends, the biceps CONTRACTS and the triceps "
           "RELAXES.' Two muscles, two jobs, one sentence."),
    capture="Photograph the pupil's model arm mid-bend with their label cards on it.",
  ),
  wedo2=dict(
    heading="True or not true?",
    pills=[
      ("Muscles pull", "TRUE"),
      ("Muscles push", "NOT TRUE \u2014 they only pull"),
      ("Muscles work in pairs", "TRUE"),
      ("Bones move on their own", "NOT TRUE \u2014 a muscle has to pull them"),
      ("Biceps and triceps take turns", "TRUE"),
    ],
    wagoll=("When I bend my arm the biceps contracts and pulls the bone up. "
            "At the same time the triceps relaxes so it does not fight it."),
  ),
  independent=dict(
    supported="Build the cardboard arm from the kit. Stick on the two labels: CONTRACTS / RELAXES.",
    standard="Build the arm, label it, and write the bending sentence underneath.",
    stretch="Build the arm, label it, write both sentences (bending and straightening), and explain why one muscle alone would not work.",
  ),
  lundy=dict(
    space="Split pins and elastic bands are fiddly. Ask for the pre-assembled kit if that is the bit that gets in the way \u2014 the science is the labels, not the fixing.",
    voice="Tell me if your model works differently from mine. Models are allowed to disagree.",
    audience="Your model goes on the bench for the next class to try.",
    influence="The class chooses which model goes in the photo for the wall.",
  ),
  exit=dict(
    supported="Fill the gap: muscles work in a ______.",
    standard="When the arm bends, what does the triceps do?",
    stretch="Explain why a muscle that could push would not need a partner.",
  ),
  exit_key=["pair", "relaxes",
            "If it could push it could move the bone both ways by itself, so no second muscle would be needed."],
  witness=[
    "Named biceps and triceps as a working pair.",
    "Stated that muscles pull and never push.",
    "Demonstrated contract / relax on a model.",
  ],
  ta_rule="ONE RULE: a muscle can only PULL. Every answer today comes back to that.",
  ta_notes=[
    "Pre-assemble two spare arms before the lesson. Fine-motor difficulty must not become a science barrier.",
    "Keep the demo on the model. Do not ask pupils to squeeze each other's arms.",
  ],
  coldcall=[
    ("Watch me move the model arm", "Did either band push?"),
    ("Which one is pulling?", "Arm straightening \u2014 which muscle contracts?"),
    ("True or not true?", "Why is 'bones move on their own' not true?"),
  ],
  uas="AQA UAS: 'The human body'.",
),

# ---------------------------------------------------------------- W5
dict(
  week=5, slug="SCI_B_W5_Right_Nutrition",
  title="What a Body Needs",
  sow="Aut1\u00b7W5 \u2014 Identify that humans and animals need the right types and amount of nutrition.",
  lo="I can name what a body needs from food and why.",
  sc=[
    "I can name three things food gives a body.",
    "I can match a job to the food that helps it.",
    "I can say why 'the right types' matters, not just 'lots'.",
  ],
  ko_vocab=[
    ("nutrition", "What a body takes from food so it can work."),
    ("energy", "What a body uses to move, play and stay warm."),
    ("growth", "Getting bigger and repairing after a cut or a break."),
    ("variety", "Eating different types, not the same thing every time."),
  ],
  ko_facts=[
    "Food does three big jobs: gives energy, helps growth and repair, keeps the body working.",
    "No single food does every job. That is why variety matters.",
    "Animals need different food from us \u2014 a cow needs grass, a cat needs meat.",
    "Water is not a food but a body cannot work without it.",
  ],
  misconceptions=[
    ("One 'super' food can do everything.",
     "Nothing does all three jobs. Show the job-cards: each food covers some, none covers all."),
    ("Animals eat what we eat.",
     "Match the animal to its food \u2014 cow/grass, owl/mouse, caterpillar/leaf."),
  ],
  arrival=dict(
    supported="Point to the picture of something that gives a body energy.",
    standard="Write one job that food does for a body.",
    stretch="Write two different jobs that food does for a body.",
  ),
  glance=["Three jobs of food", "Match animal to food", "Say why variety wins"],
  ido1=dict(
    heading="Watch me match a job to a food",
    think=("Job card says GROWTH AND REPAIR. I am not asking 'is this a nice food' \u2014 "
           "I am asking 'what job does it do'. Eggs, beans, fish: these are the building ones. "
           "So the eggs card goes under GROWTH AND REPAIR."),
    illuminator=("Three job-columns as a diagram, each with icon + word: "
                 "'\u26a1 ENERGY', '\u25b2 GROWTH &amp; REPAIR', '\u2699 KEEPS THE BODY WORKING'. "
                 "Food cards drawn beneath. No colour-only grouping; every column headed in words."),
  ),
  wedo1=dict(
    heading="Which job?",
    prompt="Tap to check.",
    items=[
      ("Bread and rice", "\u26a1 Energy"),
      ("Eggs, beans, fish", "\u25b2 Growth and repair"),
      ("Fruit and vegetables", "\u2699 Keeps the body working"),
      ("Water", "Not a food \u2014 but the body cannot work without it"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("Today's sentence shape: 'A body needs ____ because it helps with ____.' "
           "The BECAUSE is the science."),
    capture="Photograph the completed animal-and-food matching strip.",
  ),
  wedo2=dict(
    heading="Match the animal to what it needs",
    pills=[
      ("Cow", "Grass"),
      ("Owl", "Mouse"),
      ("Caterpillar", "Leaves"),
      ("Goldfish", "Fish flakes"),
      ("Every animal eats the same", "NOT TRUE \u2014 different bodies need different food"),
    ],
    wagoll=("A body needs different types of food because each type does a different job. "
            "Bread gives energy but it cannot do the repairing."),
  ),
  independent=dict(
    supported="Match six food cards to the three job columns. Word bank on the sheet.",
    standard="Match the cards, then write one 'because' sentence.",
    stretch="Match the cards, write two 'because' sentences, and explain what might happen if a body only ever got one type.",
  ),
  lundy=dict(
    space="Food is a personal subject. You never have to talk about what you eat at home \u2014 the cards do the talking today.",
    voice="If a card feels wrong to you, say so and we will look at it together.",
    audience="Your job-sort goes to the FoodWise wall, shared with the Foodwise group.",
    influence="Your matched strip is the one the class uses next week to build the plate.",
  ),
  exit=dict(
    supported="Circle the job bread does: energy / repair",
    standard="Name one food and the job it does.",
    stretch="Explain why eating only one type of food would be a problem.",
  ),
  exit_key=["energy", "any correct pair from the job columns",
            "It would only do one of the three jobs, so the other jobs would be missed."],
  witness=[
    "Named at least two jobs that food does.",
    "Matched foods to jobs on the sort.",
    "Explained why variety matters using 'because'.",
  ],
  ta_rule="ONE RULE: we talk about what food DOES, never about what anybody ate or how they look.",
  ta_notes=[
    "Zero calorie, weight or 'good food / bad food' language. If a pupil uses it, redirect to the job: 'what job does that one do?'",
    "Check the allergy list before any food packaging comes out. Packaging only \u2014 nothing is opened or tasted.",
  ],
  coldcall=[
    ("Watch me match a job to a food", "Am I asking if it is tasty, or what job it does?"),
    ("Which job?", "Which job do eggs help with?"),
    ("Match the animal to what it needs", "Why does an owl not eat grass?"),
  ],
  uas="AQA UAS: 'Healthy eating'.",
),

# ---------------------------------------------------------------- W6
dict(
  week=6, slug="SCI_B_W6_Balanced_Plate",
  title="Building a Balanced Plate",
  sow="Aut1\u00b7W6 \u2014 Sort foods into groups and describe a balanced diet (links PSHE / FoodWise).",
  lo="I can sort foods into groups and describe what balance means.",
  sc=[
    "I can name the food groups on the plate.",
    "I can place eight foods into the right group.",
    "I can describe a balanced plate in one sentence.",
  ],
  ko_vocab=[
    ("food group", "A set of foods that do a similar job."),
    ("balanced", "Having some from each group, not all from one."),
    ("everyday", "Foods we can have most days."),
    ("sometimes", "Foods we have less often. Still allowed. Still fine."),
  ],
  ko_facts=[
    "The plate has groups: fruit and vegetables; starchy foods; protein foods; dairy or alternatives; oils and spreads.",
    "Balanced means SOME FROM EACH, not none from any.",
    "'Sometimes' foods are not bad foods. They are just the smaller part of the plate.",
    "The plate is a guide for the whole day and week, not a rule for one meal.",
  ],
  misconceptions=[
    ("Some foods are bad foods.",
     "There are no bad foods on this plate. There are everyday ones and sometimes ones."),
    ("Balanced means equal amounts of everything.",
     "Look at the plate: fruit and veg take the biggest part. Balance is not five equal slices."),
    ("A balanced plate must be every single meal.",
     "It is a picture of a whole day, and of a week."),
  ],
  arrival=dict(
    supported="Point to the biggest section on the plate picture.",
    standard="Name one food group you can see on the plate.",
    stretch="Name two food groups and say which section is biggest.",
  ),
  glance=["Name the groups", "Sort eight foods", "Describe balance"],
  ido1=dict(
    heading="Watch me place a food on the plate",
    think=("Rice. I am asking which GROUP, not whether I like it. Rice is starchy \u2014 "
           "it belongs in the starchy foods section, and that is a big section, so rice "
           "is an everyday one. Placing it now."),
    illuminator=("Eatwell-style plate divided into five sections, each labelled with icon + "
                 "word + a size note in words ('BIGGEST SECTION' / 'SMALL SECTION'), so the "
                 "proportions are readable without relying on colour or area alone."),
  ),
  wedo1=dict(
    heading="Which section?",
    prompt="Tap to check.",
    items=[
      ("Apple", "Fruit and vegetables \u2014 biggest section"),
      ("Pasta", "Starchy foods \u2014 big section"),
      ("Chicken", "Protein foods"),
      ("Yoghurt", "Dairy or alternatives"),
      ("Olive oil", "Oils and spreads \u2014 small section"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("Sentence shape: 'A balanced plate has ____ from every group, with the biggest "
           "part being ____.' Say it, then write it."),
    capture="Photograph the pupil's completed plate before it is cleared.",
  ),
  wedo2=dict(
    heading="Sort the statements",
    pills=[
      ("Some from every group", "BALANCED"),
      ("All from one group", "NOT BALANCED"),
      ("Fruit and veg is the biggest part", "TRUE"),
      ("Sometimes foods are banned", "NOT TRUE \u2014 they are the smaller part, not banned"),
      ("Chips are a bad food", "NOT TRUE \u2014 no food on this plate is a bad food"),
    ],
    wagoll=("A balanced plate has something from every group. The biggest part is fruit and "
            "vegetables, and the smallest part is oils and spreads."),
  ),
  independent=dict(
    supported="Stick eight food cards onto the plate mat in the right sections. Word bank provided.",
    standard="Place the eight cards, then write your balance sentence underneath.",
    stretch="Place the cards, write your balance sentence, and build a second plate for a day when someone does not eat meat.",
  ),
  lundy=dict(
    space="You never have to say what is in your lunchbox. This is about the cards on the plate.",
    voice="If a food you eat is not on a card, tell me and we will make a card for it.",
    audience="Your plate joins the Balanced-Plate Gallery in the corridor.",
    influence="The class votes on which three plates go into the FoodWise display.",
  ),
  exit=dict(
    supported="Circle the biggest section: fruit and veg / oils",
    standard="Name two food groups on the plate.",
    stretch="Describe a balanced plate without using the word 'healthy'.",
  ),
  exit_key=["fruit and veg", "any two of the five groups",
            "Something from each group, with fruit and vegetables the biggest part and oils the smallest."],
  witness=[
    "Named at least two food groups.",
    "Sorted eight foods into correct groups.",
    "Described balance in their own words.",
  ],
  ta_rule="ONE RULE: no food is a bad food. We sort by GROUP, never by good or bad.",
  ta_notes=[
    "Absolutely no calorie, weight, portion-restriction or body-size language, at any tier, in any conversation around this lesson.",
    "If a pupil discloses something about eating at home, do not pursue it in the room \u2014 log it and pass to the safeguarding lead.",
    "Allergy list checked. Packaging only, nothing opened, nothing tasted.",
  ],
  coldcall=[
    ("Watch me place a food on the plate", "Am I asking if I like it, or which group it is in?"),
    ("Which section?", "Which section is the biggest?"),
    ("Sort the statements", "Is a sometimes food a banned food?"),
  ],
  uas="AQA UAS: 'Healthy eating'; ASDAN FoodWise link.",
),

# ---------------------------------------------------------------- W7
dict(
  week=7, slug="SCI_B_W7_Where_Food_Comes_From",
  title="Animals Cannot Make Their Own Food",
  sow="Aut1\u00b7W7 \u2014 Explain that animals cannot make their own food; they get it from what they eat.",
  lo="I can explain that animals get their food by eating, and plants do not.",
  sc=[
    "I can say that plants make their own food.",
    "I can say that animals must eat to get theirs.",
    "I can put a simple food chain in the right order.",
  ],
  ko_vocab=[
    ("food chain", "A picture of who eats what, in order."),
    ("producer", "A plant. It MAKES its own food."),
    ("consumer", "An animal. It EATS to get food."),
    ("energy", "What passes along the chain when something is eaten."),
  ],
  ko_facts=[
    "Plants make their own food using light. Animals cannot do this.",
    "Every food chain starts with a plant.",
    "The arrow in a food chain means 'is eaten by' and points the way the energy travels.",
    "Grass \u2192 rabbit \u2192 fox. The grass made its own; the rabbit and the fox had to eat.",
  ],
  misconceptions=[
    ("The arrow points to who does the eating.",
     "The arrow means IS EATEN BY. Grass \u2192 rabbit: the grass is eaten by the rabbit."),
    ("Plants get their food from the soil.",
     "They take water and minerals from soil, but they MAKE their food using light."),
    ("A food chain can start with an animal.",
     "Trace it back \u2014 you always end up at a plant."),
  ],
  arrival=dict(
    supported="Point to the plant in the food chain picture.",
    standard="Write what a rabbit eats.",
    stretch="Write a two-step chain: something eats something.",
  ),
  glance=["Producer or consumer", "Read the arrow", "Build a chain"],
  ido1=dict(
    heading="Watch me read a food chain",
    think=("Grass, arrow, rabbit, arrow, fox. The arrow does NOT mean 'eats'. It means "
           "'IS EATEN BY'. So: grass is eaten by the rabbit; the rabbit is eaten by the fox. "
           "And notice where it starts \u2014 a plant. It always starts with a plant."),
    illuminator=("Horizontal three-step chain diagram: grass \u2192 rabbit \u2192 fox. Each arrow "
                 "carries the words 'IS EATEN BY' printed along it. Each organism tagged "
                 "'\u25a0 PRODUCER \u00b7 MAKES ITS OWN' or '\u25cf CONSUMER \u00b7 MUST EAT'. "
                 "Labels horizontal, icon + word on every tag."),
  ),
  wedo1=dict(
    heading="Producer or consumer?",
    prompt="Tap to check.",
    items=[
      ("Oak tree", "\u25a0 Producer \u2014 makes its own"),
      ("Squirrel", "\u25cf Consumer \u2014 must eat"),
      ("Grass", "\u25a0 Producer"),
      ("Fox", "\u25cf Consumer"),
      ("Can a fox make its own food?", "No. No animal can."),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("Sentence shape: 'The fox is a consumer because it cannot make its own food, "
           "so it has to eat.' Because, so. Two joining words, one clear reason."),
    capture="Photograph the pupil's completed chain strip with arrows drawn in.",
  ),
  wedo2=dict(
    heading="Put it right",
    pills=[
      ("Grass \u2192 rabbit \u2192 fox", "CORRECT"),
      ("Fox \u2192 rabbit \u2192 grass", "WRONG WAY \u2014 arrows point to who does the eating"),
      ("Every chain starts with a plant", "TRUE"),
      ("Animals make their own food", "NOT TRUE"),
    ],
    wagoll=("Every food chain starts with a plant because plants are the only ones that can "
            "make their own food. Animals are consumers, so they have to eat."),
  ),
  independent=dict(
    supported="Order three cards into a chain and draw the arrows. Word bank on the sheet.",
    standard="Build the chain, draw the arrows, and label producer and consumer.",
    stretch="Build the chain, label it, and write why removing the grass would affect the fox.",
  ),
  lundy=dict(
    space="Arrows are easy to draw the wrong way round. Getting it wrong first is part of the method here.",
    voice="Argue your chain. If you can justify it, I will listen.",
    audience="Your chain goes into the class food-chain display.",
    influence="The class picks one local Teesside chain to build for the wall next term.",
  ),
  exit=dict(
    supported="Circle the producer: grass / fox",
    standard="What does the arrow in a food chain mean?",
    stretch="Explain why every food chain has to start with a plant.",
  ),
  exit_key=["grass", "is eaten by",
            "Only plants can make their own food, so the energy has to enter the chain there."],
  witness=[
    "Identified producer and consumer correctly.",
    "Read the arrow as 'is eaten by'.",
    "Built a correctly ordered food chain.",
  ],
  ta_rule="ONE RULE: the arrow means IS EATEN BY. Every wrong chain today is fixed with that one line.",
  ta_notes=[
    "This lesson closes the Aut1 block \u2014 the Entry Level / UAS evidence review is Aut2\u00b7W7, not here.",
    "Some pupils find predator content upsetting. The fox card is a drawing, not a photograph.",
  ],
  coldcall=[
    ("Watch me read a food chain", "What does the arrow mean?"),
    ("Producer or consumer?", "Can any animal make its own food?"),
    ("Put it right", "Why does a chain always start with a plant?"),
  ],
  uas="AQA UAS: 'Living things and their habitats'.",
),
]
