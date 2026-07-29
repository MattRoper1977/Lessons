# -*- coding: utf-8 -*-
"""
GROW science — Autumn 1, weeks 3-7 (post-baseline).
Spine: White Rose Science Year 5/6 · Pearson Entry Level Science 8939 (E1->E3) · AQA UAS.
Diagnostic-led: Y3/4 for gap-fill, KS3 for stretch. Theme: Identity & Belonging.

REUSE FLAG (raised for Matt, not acted on):
  W6 (Earth & planets round the Sun) and W7 (Moon round Earth) overlap directly with the
  EXISTING primary Space block already live on the site -- Lesson1_TheSolarSystem.html and
  Lesson2_ThePlanets.html. Those sit on the PRIMARY chassis (9 slides, Seedling/Sapling/Oak
  tiers, tap-to-sort .sorter), NOT v5, so they cannot be dropped in as-is. Their CONTENT is
  harvestable: the eight-planet order, the mnemonic, rocky-vs-gas grouping and the Sun ~109
  Earths figure are all authored and checked. Decision for Matt: harvest content into these
  v5 decks (recommended) or cross-link the pathways to the primary lessons.

HOUSE RULES BAKED IN:
  * Icon + label + colour on every classification. Never colour alone.
  * Fair-test work is the assessed spine here -- ELC 8939 rewards working scientifically.
  * Answer keys STAFF-SIDE. Exit answers never on a pupil surface.
  * TA brief opens with ONE rule.
  * No leaderboards, no timed competition between pupils.
"""

STRAND = "Science"
PATHWAY = "GROW"
COLOUR = "#3F7D6E"          # GROW science teal-green; distinct from GROW Community #2F8F6B
SPINE = "White Rose Science Year 5/6"
AWARD = "Pearson Entry Level Science 8939 (E1\u2192E3); AQA UAS science units"
THEME = "Identity &amp; Belonging"
SLOT_WEEKS = 7
SENSORY = ("Forces work is noisy and physical \u2014 trolleys, ramps, dropped masses. Agree the "
           "noise signal before equipment comes out, and offer ear defenders without making it "
           "a conversation. A pupil may record data instead of running the trial and still be "
           "doing the science.")

LESSONS = [

# ---------------------------------------------------------------- W3
dict(
  week=3, slug="SCI_G_W3_Friction",
  title="Friction: Friend and Enemy",
  sow="Aut1\u00b7W3 \u2014 Explore friction and how it can be helpful or unhelpful.",
  lo="I can explain what friction does and give examples where it helps and where it hinders.",
  sc=[
    "I can state that friction acts between two surfaces that rub.",
    "I can give one example where friction is helpful and one where it is unhelpful.",
    "I can predict which surface will produce more friction, and say why.",
  ],
  ko_vocab=[
    ("friction", "A force between two surfaces that are rubbing or trying to slide."),
    ("surface", "The outside face of an object, where the touching happens."),
    ("grip", "Useful friction \u2014 stops slipping."),
    ("wear", "Damage caused over time by friction."),
    ("lubricant", "Something (like oil) that reduces friction."),
  ],
  ko_facts=[
    "Friction always acts AGAINST the direction of movement. It slows things down.",
    "Friction needs two surfaces in contact. No contact, no friction.",
    "Rougher surfaces generally produce more friction than smooth ones.",
    "Friction is not always bad: brakes, shoe soles, tyres and door handles all rely on it.",
    "Friction turns movement energy into heat \u2014 that is why rubbing hands warms them.",
  ],
  misconceptions=[
    ("Friction is always a nuisance.",
     "Ask what happens on ice. No friction means no walking, no stopping, no steering."),
    ("Heavy things have more friction because they are heavy.",
     "Weight matters, but so does the surface pair. Test both and separate them."),
    ("Smooth always means frictionless.",
     "Glass on glass is smooth and still grips. Frictionless does not exist in the classroom."),
  ],
  arrival=dict(
    supported="Rub your hands together for five seconds. What do you notice?",
    standard="Rub your hands together. Write what you feel and name the force.",
    stretch="Rub your hands together. Explain where the heat came from.",
  ),
  glance=["Define friction properly", "Helpful vs unhelpful", "Predict and test two surfaces"],
  ido1=dict(
    heading="Watch me test two surfaces",
    think=("Same block, same ramp, same angle. I change ONE thing: the surface. Carpet first "
           "\u2014 it barely moves. Now the same block on the smooth board \u2014 straight down. "
           "One variable changed, so the difference must be the surface. That is the whole logic "
           "of a fair test, and we will use it again in week 5."),
    illuminator=("Ramp diagram, two frames. Frame 1 tagged '\u25a0 ROUGH SURFACE \u00b7 MORE FRICTION' "
                 "with a short movement arrow; frame 2 tagged '\u25ad SMOOTH SURFACE \u00b7 LESS FRICTION' "
                 "with a long arrow. A friction arrow opposing motion is drawn and labelled "
                 "'FRICTION ACTS THIS WAY' in words. All labels horizontal."),
  ),
  wedo1=dict(
    heading="Helpful or unhelpful?",
    prompt="Decide before you tap.",
    items=[
      ("Bike brakes", "HELPFUL \u2014 friction is doing the stopping"),
      ("Trainers on a wet floor", "HELPFUL \u2014 grip stops the slip"),
      ("Engine parts rubbing", "UNHELPFUL \u2014 causes wear and wasted heat"),
      ("Pushing a heavy box across carpet", "UNHELPFUL \u2014 makes the job harder"),
      ("A door handle", "HELPFUL \u2014 without grip your hand would slide"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("The sentence shape that earns marks: 'Friction is helpful HERE because ____, "
           "but unhelpful HERE because ____.' Same force, two verdicts. That contrast is the answer."),
    capture="Photograph the pupil's surface-test results table with their prediction still visible.",
  ),
  wedo2=dict(
    heading="Sort the claims",
    pills=[
      ("Friction acts against movement", "TRUE"),
      ("Friction only happens with rough surfaces", "FALSE \u2014 smooth surfaces have it too, just less"),
      ("Oil reduces friction", "TRUE"),
      ("Without friction we could not walk", "TRUE"),
      ("Friction is a bad force", "NOT A SCIENTIFIC CLAIM \u2014 depends entirely on the job"),
    ],
    wagoll=("Friction is helpful on a bike brake because it converts the movement into heat and "
            "stops the wheel, but it is unhelpful inside the engine because the same rubbing "
            "wears the parts down."),
  ),
  independent=dict(
    supported="Test three surfaces with the ramp. Record distance travelled in the prepared table.",
    standard="Test three surfaces, record distances, and write which had most friction and how you know.",
    stretch="Test three surfaces, record distances, then explain what you would change to make the test fairer, and why.",
  ),
  lundy=dict(
    space="Ramps clatter. If the noise is the problem, you can be the recorder and still be doing the science.",
    voice="Your prediction counts even when the result disagrees with it. Write it before you test, not after.",
    audience="Your results table goes to the Forces Board and is used in week 5.",
    influence="The class agrees which three surfaces the whole group tests next.",
  ),
  exit=dict(
    supported="Name one place friction helps.",
    standard="Explain why a car needs friction to stop.",
    stretch="Explain why the same force can be a design problem and a design solution.",
  ),
  exit_key=["brakes / shoes / tyres / handles",
            "The brake pads rub the disc; friction converts movement energy to heat and slows the wheel.",
            "Because friction always resists motion \u2014 that resistance is wanted at the brake and unwanted in the engine."],
  witness=[
    "Defined friction as a force between rubbing surfaces.",
    "Gave one helpful and one unhelpful example.",
    "Predicted, tested and recorded a surface comparison.",
  ],
  ta_rule="ONE RULE: friction always pushes back against the movement. Every answer starts there.",
  ta_notes=[
    "Predictions get written BEFORE the ramp is released. A prediction written afterwards is not a prediction.",
    "Do not let this become a race between pupils. Same block, same ramp, different surfaces.",
  ],
  coldcall=[
    ("Watch me test two surfaces", "How many things did I change?"),
    ("Helpful or unhelpful?", "Give me a case where friction saves your life."),
    ("Sort the claims", "Why is 'friction is a bad force' not a scientific claim?"),
  ],
  uas="AQA UAS: 'Forces'.",
),

# ---------------------------------------------------------------- W4
dict(
  week=4, slug="SCI_G_W4_Mechanisms",
  title="Levers, Pulleys and Gears",
  sow="Aut1\u00b7W4 \u2014 Investigate mechanisms: levers, pulleys and gears.",
  lo="I can explain how a mechanism lets a smaller force do a bigger job.",
  sc=[
    "I can name the three mechanisms and point to one example of each.",
    "I can identify the pivot on a lever.",
    "I can explain what a mechanism gives you and what it costs you.",
  ],
  ko_vocab=[
    ("mechanism", "A part that changes a force \u2014 its size, its direction, or both."),
    ("lever", "A rigid bar that turns around a pivot."),
    ("pivot", "The fixed point a lever turns around."),
    ("pulley", "A wheel with a rope over it; changes the direction of a pull."),
    ("gear", "A toothed wheel that turns another toothed wheel."),
  ],
  ko_facts=[
    "A mechanism does not create energy. It trades distance for force.",
    "Move the pivot closer to the load and the lever gets easier \u2014 but you move the other end further.",
    "A single fixed pulley changes direction only. Adding pulleys shares the load.",
    "A small gear driving a big gear turns slower but with more turning force.",
    "Scissors, wheelbarrows, spanners and door handles are all levers.",
  ],
  misconceptions=[
    ("A mechanism gives you free force.",
     "Measure the distance moved at each end. You pay in distance for every bit of force you gain."),
    ("The pivot is always in the middle.",
     "Wheelbarrow: pivot at the wheel, at one end. Scissors: pivot in the middle. Both levers."),
    ("Bigger gear always means faster.",
     "Bigger gear means slower turning and more force. Count the teeth and watch."),
  ],
  arrival=dict(
    supported="Open the scissors on your desk. Point to the part that everything turns around.",
    standard="Name the part of the scissors that everything turns around.",
    stretch="Name the pivot on the scissors, and on the wheelbarrow picture.",
  ),
  glance=["Find the pivot", "Move it and feel the difference", "Say what it costs"],
  ido1=dict(
    heading="Watch me move the pivot",
    think=("Ruler, pencil underneath as the pivot, load on the end. Pivot in the middle \u2014 "
           "I am working hard. Now I slide the pivot close to the load. Much easier. But watch my "
           "hand: it is travelling much further than before. I did not get something for nothing. "
           "I traded distance for force."),
    illuminator=("Lever diagram, two frames. Each shows bar, load, and a triangle pivot tagged "
                 "'\u25b2 PIVOT'. Frame 1: pivot central, tagged 'EFFORT: HARDER \u00b7 HAND MOVES LESS'. "
                 "Frame 2: pivot near load, tagged 'EFFORT: EASIER \u00b7 HAND MOVES FURTHER'. "
                 "Distance arrows labelled in words."),
  ),
  wedo1=dict(
    heading="Which mechanism?",
    prompt="Name it before you tap.",
    items=[
      ("Wheelbarrow", "Lever \u2014 pivot at the wheel"),
      ("Flagpole rope over a wheel at the top", "Pulley \u2014 changes direction of the pull"),
      ("Bicycle chain and cogs", "Gears"),
      ("Scissors", "Lever \u2014 pivot in the middle"),
      ("Spanner on a tight bolt", "Lever \u2014 longer handle, more turning force"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("Answer shape: 'This is a ____ because it turns around a ____ / changes the ____. "
           "It makes the job easier by ____, but you have to ____.' Gain and cost, both stated."),
    capture="Photograph the pupil's lever set-up at both pivot positions, with the load visible.",
  ),
  wedo2=dict(
    heading="Gain or cost?",
    pills=[
      ("Less force needed", "GAIN"),
      ("Hand travels further", "COST"),
      ("Pull down instead of up", "GAIN \u2014 direction change"),
      ("Mechanism creates extra energy", "NEITHER \u2014 this is not true of any mechanism"),
      ("Slower turning, more turning force", "GAIN AND COST TOGETHER \u2014 that is the trade"),
    ],
    wagoll=("The wheelbarrow is a lever because it turns around a pivot at the wheel. Putting the "
            "load near the wheel means I lift with less force, but I have to lift the handles "
            "through a bigger distance."),
  ),
  independent=dict(
    supported="Set up the lever at two pivot positions. Tick which was easier on the prepared sheet.",
    standard="Test both pivot positions, record the effort, and write which was easier and why.",
    stretch="Test both positions, record the effort AND the distance your hand moved, then explain the trade-off using both numbers.",
  ),
  lundy=dict(
    space="Loads and masses get dropped. Feet clear of the bench, and tell me if the weight is too much to handle safely.",
    voice="If your result contradicts mine, we test mine again. That is the deal.",
    audience="Your lever results feed the D&T Upcycling group's build next term.",
    influence="The class chooses which mechanism gets built full-size for the corridor display.",
  ),
  exit=dict(
    supported="Name the point a lever turns around.",
    standard="Explain why moving the pivot closer to the load makes lifting easier.",
    stretch="Explain why no mechanism can give you force without a cost.",
  ),
  exit_key=["pivot",
            "The effort arm becomes longer relative to the load arm, so less force is needed.",
            "Energy in must equal energy out; extra force is always paid for with extra distance."],
  witness=[
    "Named lever, pulley and gear with one example each.",
    "Identified the pivot correctly.",
    "Stated both the gain and the cost of a mechanism.",
  ],
  ta_rule="ONE RULE: a mechanism never gives something for nothing \u2014 always ask what it cost.",
  ta_notes=[
    "Masses on a bench are a foot hazard. Trays down, feet back, before anything is loaded.",
    "The stretch tier needs a ruler and two measurements \u2014 have them out before the lesson starts.",
  ],
  coldcall=[
    ("Watch me move the pivot", "What did I pay for the easier lift?"),
    ("Which mechanism?", "Where is the pivot on a wheelbarrow?"),
    ("Gain or cost?", "Can a mechanism create energy?"),
  ],
  uas="AQA UAS: 'Forces'; 'Simple machines'.",
),

# ---------------------------------------------------------------- W5
dict(
  week=5, slug="SCI_G_W5_Fair_Test",
  title="Planning a Fair Test",
  sow="Aut1\u00b7W5 \u2014 Plan and carry out a fair test about forces; record results.",
  lo="I can plan a fair test, carry it out, and record my results clearly.",
  sc=[
    "I can name the one thing I will change and the things I will keep the same.",
    "I can record results in a table with units.",
    "I can say whether my results answer my question.",
  ],
  ko_vocab=[
    ("variable", "Anything in a test that could change."),
    ("independent variable", "The ONE thing you deliberately change."),
    ("control variable", "Everything you deliberately keep the same."),
    ("dependent variable", "The thing you measure."),
    ("repeat", "Doing the same trial again to check the result."),
  ],
  ko_facts=[
    "A fair test changes ONE thing and keeps everything else the same.",
    "If two things change at once, you cannot tell which one caused the difference.",
    "Every measurement needs a unit. A number on its own is not a result.",
    "Repeating a trial three times shows whether a result is reliable or a one-off.",
    "An unexpected result is data, not a mistake. Record it.",
  ],
  misconceptions=[
    ("A fair test means everyone gets a turn.",
     "Fair here is a technical word. It means one variable changed, not equal turns."),
    ("If the result is not what I predicted, I did it wrong.",
     "Not necessarily. Check the method; if the method held, the prediction was wrong, and that is a finding."),
    ("One trial is enough.",
     "Run it three times. Watch how much the numbers wander."),
  ],
  arrival=dict(
    supported="Read the question on the board. Circle the ONE thing we will change.",
    standard="Write the one thing we will change in today's test.",
    stretch="Write the one thing we will change and two things we must keep the same.",
  ),
  glance=["Name the variables", "Run three trials", "Judge your own data"],
  ido1=dict(
    heading="Watch me spoil a test on purpose",
    think=("Question: does surface affect how far the trolley rolls? Watch \u2014 I change the "
           "surface AND I push harder. Trolley goes further. So what caused it? I have no idea. "
           "The test is worthless, and it took one careless push to ruin it. Now again, properly: "
           "same release point, same trolley, same slope. Only the surface changes."),
    illuminator=("Fair-test planning frame drawn as a three-box diagram: "
                 "'\u25c6 I CHANGE (one only)', '\u25a0 I KEEP THE SAME (list)', "
                 "'\u25b6 I MEASURE (with units)'. Icon + word on each box. A results table "
                 "with three repeat columns and a mean column sits below."),
  ),
  wedo1=dict(
    heading="Which kind of variable?",
    prompt="Decide, then tap.",
    items=[
      ("The surface we roll on", "\u25c6 Independent \u2014 the one we change"),
      ("Distance the trolley travels", "\u25b6 Dependent \u2014 the thing we measure"),
      ("Height of the ramp", "\u25a0 Control \u2014 must stay the same"),
      ("Which trolley we use", "\u25a0 Control \u2014 must stay the same"),
      ("How hard we push", "\u25a0 Control \u2014 and the easiest one to get wrong"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("Write it as one planning sentence before you touch equipment: 'I will change ____, "
           "keep ____ and ____ the same, and measure ____ in ____.' If you cannot finish that "
           "sentence, you are not ready to test."),
    capture="Photograph the completed planning frame AND the results table together \u2014 the pair is the evidence.",
  ),
  wedo2=dict(
    heading="Fair or not fair?",
    pills=[
      ("Same ramp height, different surfaces", "FAIR"),
      ("Different ramp heights, different surfaces", "NOT FAIR \u2014 two variables changed"),
      ("Three repeats of each surface", "FAIR \u2014 and more reliable"),
      ("Ignoring a result you did not like", "NOT SCIENCE \u2014 record it and say so"),
      ("Measuring in 'about a ruler'", "NOT A UNIT \u2014 use centimetres"),
    ],
    wagoll=("I changed the surface only. I kept the ramp height, the trolley and the release point "
            "the same. I measured the distance in centimetres and repeated each surface three times. "
            "Carpet gave the shortest distance every time, so carpet produced the most friction."),
  ),
  independent=dict(
    supported="Complete the planning frame from the word bank, then run three trials and fill the table.",
    standard="Write your own planning frame, run three trials per surface, and complete the table with units.",
    stretch="Plan, run three trials per surface, calculate the mean, and write a conclusion that states whether the data answers the question.",
  ),
  lundy=dict(
    space="This lesson has a lot of waiting between trials. Waiting is part of it, not wasted time.",
    voice="Tell me if you think my method is flawed. You will sometimes be right.",
    audience="Your planning frame and table go into the Entry Level Science evidence folder.",
    influence="The class agrees the one variable the whole group investigates next.",
  ),
  exit=dict(
    supported="How many things do you change in a fair test?",
    standard="Name one control variable from today's test.",
    stretch="Explain why three repeats are better than one.",
  ),
  exit_key=["one",
            "ramp height / trolley / release point / push force",
            "Repeats show whether a result is consistent or a one-off, so you can judge reliability."],
  witness=[
    "Identified independent, dependent and control variables.",
    "Recorded results in a table with correct units.",
    "Judged whether the data answered the question.",
  ],
  ta_rule="ONE RULE: change one thing only. If two things changed, the test proves nothing.",
  ta_notes=[
    "This is the assessed working-scientifically lesson of the block \u2014 the planning frame and the table are the ELC evidence. Collect both.",
    "A pupil who plans well but cannot run the trial has still met the outcome. Let them direct a partner.",
  ],
  coldcall=[
    ("Watch me spoil a test on purpose", "How many things did I change the first time?"),
    ("Which kind of variable?", "Which variable is easiest to get wrong by accident?"),
    ("Fair or not fair?", "What do we do with a result we did not expect?"),
  ],
  uas="AQA UAS: 'Scientific enquiry'; 'Recording results'.",
),

# ---------------------------------------------------------------- W6
dict(
  week=6, slug="SCI_G_W6_Earth_And_Planets",
  title="Earth and the Planets",
  sow="Aut1\u00b7W6 \u2014 Describe the movement of the Earth and other planets around the Sun.",
  lo="I can describe how the Earth and the other planets move around the Sun.",
  sc=[
    "I can name the eight planets in order from the Sun.",
    "I can state that the planets orbit the Sun, and that the orbits are nearly circular.",
    "I can explain what keeps a planet in orbit.",
  ],
  ko_vocab=[
    ("orbit", "The curved path one object takes around another."),
    ("Solar System", "The Sun and everything that orbits it."),
    ("gravity", "The force pulling objects towards each other."),
    ("year", "The time a planet takes to complete one orbit of the Sun."),
    ("spherical", "Ball-shaped."),
  ],
  ko_facts=[
    "Order from the Sun: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune.",
    "Mnemonic: My Very Easy Method Just Speeds Up Naming Planets.",
    "The four inner planets are rocky. The four outer planets are gas or ice giants.",
    "Gravity from the Sun is what holds every planet in its orbit.",
    "The further out the planet, the longer its year. Neptune's year is about 165 Earth years.",
    "The Sun is about 109 times the diameter of Earth.",
  ],
  misconceptions=[
    ("Orbits are big ovals like a running track.",
     "Most planetary orbits are very close to circular. Show the scale drawing."),
    ("The Sun goes round the Earth.",
     "It looks that way because the Earth spins. Model it with the torch and the globe."),
    ("Planets stay up because space has no gravity.",
     "Space has plenty of gravity \u2014 that is exactly what is holding them in the curve."),
  ],
  arrival=dict(
    supported="Put the four planet cards in order from the Sun.",
    standard="Write the first four planets in order from the Sun.",
    stretch="Write all eight planets in order from the Sun.",
  ),
  glance=["Get the order right", "Model the orbit", "Explain what holds it"],
  ido1=dict(
    heading="Watch me model an orbit",
    think=("Sun in the middle. I walk the Earth around it \u2014 nearly a circle, not an oval. "
           "Now, why does it not fly off in a straight line? Because the Sun is pulling it. "
           "Gravity is not stopping the Earth moving, it is constantly bending its path into a curve. "
           "Take gravity away and the Earth goes straight on, out into space."),
    illuminator=("Scale-ordered Solar System diagram: Sun at left, eight planets in order, each "
                 "tagged with name + '\u25cf ROCKY' or '\u25cb GAS/ICE GIANT'. A separate inset shows "
                 "one orbit with a gravity arrow pointing at the Sun labelled 'GRAVITY PULLS INWARD' "
                 "and a motion arrow labelled 'MOTION GOES SIDEWAYS'. Labels horizontal."),
  ),
  wedo1=dict(
    heading="Rocky or giant?",
    prompt="Decide, then tap.",
    items=[
      ("Mercury", "\u25cf Rocky \u2014 inner"),
      ("Mars", "\u25cf Rocky \u2014 inner"),
      ("Jupiter", "\u25cb Gas giant \u2014 outer"),
      ("Neptune", "\u25cb Ice giant \u2014 outer"),
      ("Which has the longest year?", "Neptune \u2014 furthest out, longest orbit"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("Answer shape: 'The Earth orbits the Sun because the Sun's gravity pulls it inward, "
           "which bends its path into a curve instead of a straight line.' Force, then effect."),
    capture="Photograph the pupil's ordered planet strip with their orbit annotation.",
  ),
  wedo2=dict(
    heading="True or false?",
    pills=[
      ("Planets orbit the Sun", "TRUE"),
      ("The Sun orbits the Earth", "FALSE \u2014 the Earth's spin makes it look that way"),
      ("Gravity holds planets in orbit", "TRUE"),
      ("There is no gravity in space", "FALSE \u2014 gravity is what makes orbits happen"),
      ("Further out means a longer year", "TRUE"),
    ],
    wagoll=("Neptune has a longer year than Earth because it is much further from the Sun, so its "
            "orbit is far bigger and it takes about 165 Earth years to complete one."),
  ),
  independent=dict(
    supported="Order the eight planet cards and label rocky or giant using the word bank.",
    standard="Order the planets, label rocky/giant, and write what keeps them in orbit.",
    stretch="Order and label the planets, explain the gravity-and-motion balance, and predict which planet has the shortest year with a reason.",
  ),
  lundy=dict(
    space="Modelling an orbit means walking a circle in front of others. You can model it with counters on the desk instead.",
    voice="Scale here is genuinely hard to picture. Say so if a number sounds wrong \u2014 they often do.",
    audience="Your planet strip goes on the Space Board for the Aut2 block.",
    influence="The class picks which planet gets the detailed research page next term.",
  ),
  exit=dict(
    supported="Which planet is third from the Sun?",
    standard="What force keeps a planet in orbit?",
    stretch="Explain why a planet does not fall into the Sun.",
  ),
  exit_key=["Earth", "gravity",
            "It is moving sideways fast enough that the inward pull curves its path instead of pulling it in."],
  witness=[
    "Named the eight planets in order.",
    "Classified planets as rocky or giant.",
    "Explained gravity's role in maintaining an orbit.",
  ],
  ta_rule="ONE RULE: gravity does not hold planets still \u2014 it bends a straight line into a circle.",
  ta_notes=[
    "Content overlaps the existing Y5 Space lessons on the site. If a pupil has met them, push them to the stretch tier rather than repeating the order work.",
    "Avoid darkened-room demos without warning; sudden lighting changes unsettle several pupils.",
  ],
  coldcall=[
    ("Watch me model an orbit", "What happens if I switch gravity off?"),
    ("Rocky or giant?", "Which planet has the longest year, and why?"),
    ("True or false?", "Is there gravity in space?"),
  ],
  uas="AQA UAS: 'Earth &amp; space'.",
),

# ---------------------------------------------------------------- W7
dict(
  week=7, slug="SCI_G_W7_The_Moon",
  title="The Moon's Journey",
  sow="Aut1\u00b7W7 \u2014 Describe the movement of the Moon around the Earth.",
  lo="I can describe how the Moon moves around the Earth and why it looks different each week.",
  sc=[
    "I can state that the Moon orbits the Earth, roughly once a month.",
    "I can explain that the Moon does not make its own light.",
    "I can describe why the Moon appears to change shape.",
  ],
  ko_vocab=[
    ("satellite", "An object that orbits a planet. The Moon is Earth's natural satellite."),
    ("phase", "The shape of the lit part of the Moon that we can see."),
    ("reflect", "To bounce light off a surface."),
    ("crescent", "A thin curved phase."),
    ("full moon", "The phase where we see the whole lit face."),
  ],
  ko_facts=[
    "The Moon orbits the Earth in roughly 28 days \u2014 about a month.",
    "The Moon makes no light of its own. We see sunlight reflected off it.",
    "Half the Moon is always lit. We just see different amounts of that lit half.",
    "The phases are caused by our viewing angle changing as the Moon orbits, not by Earth's shadow.",
    "The Moon keeps the same face towards Earth as it orbits.",
  ],
  misconceptions=[
    ("Phases are the Earth's shadow falling on the Moon.",
     "That is an eclipse, and it is rare. Phases happen every month and are about viewing angle."),
    ("The Moon makes its own light.",
     "Torch and ball model: switch the torch off and the ball disappears."),
    ("The Moon only comes out at night.",
     "It is often visible in daylight. Ask who has seen it in the morning."),
  ],
  arrival=dict(
    supported="Point to the full moon on the phase strip.",
    standard="Write how long you think the Moon takes to go round the Earth.",
    stretch="Write how long the Moon takes to orbit Earth, and where its light comes from.",
  ),
  glance=["Orbit and time", "Where the light comes from", "Model the phases"],
  ido1=dict(
    heading="Watch me make the phases happen",
    think=("Torch is the Sun, ball is the Moon, my head is the Earth. Half the ball is lit \u2014 "
           "always, the whole time. Watch what changes as I move it round: not the lighting, "
           "MY ANGLE. When the lit side faces me, full moon. When it faces away, new moon. "
           "The shadow of the Earth never comes into it."),
    illuminator=("Phase diagram: Earth centred, eight Moon positions around the orbit circle, "
                 "sunlight arrows from one side. Each position shows the half-lit ball AND the "
                 "phase we see from Earth, tagged in words ('NEW', 'CRESCENT', 'HALF', 'FULL'). "
                 "A note reads 'HALF IS ALWAYS LIT \u2014 OUR ANGLE CHANGES'. Labels horizontal."),
  ),
  wedo1=dict(
    heading="What causes it?",
    prompt="Decide, then tap.",
    items=[
      ("Moon looks like a crescent", "Our viewing angle \u2014 we see a sliver of the lit half"),
      ("Moon looks full", "Lit half facing us directly"),
      ("Moon disappears (new moon)", "Lit half facing away from us"),
      ("Moon goes dark red during an eclipse", "Earth's shadow \u2014 this one IS a shadow, and it is rare"),
    ],
  ),
  ido2=dict(
    heading="Evidence loop",
    model=("Answer shape: 'The Moon appears to change shape because it orbits the Earth, so we "
           "see different amounts of its lit half.' Cause, then what we observe."),
    capture="Photograph the pupil's completed phase wheel with the sunlight direction marked.",
  ),
  wedo2=dict(
    heading="Sort the statements",
    pills=[
      ("The Moon reflects sunlight", "TRUE"),
      ("The Moon glows by itself", "FALSE"),
      ("Phases are caused by Earth's shadow", "FALSE \u2014 that is an eclipse"),
      ("The Moon orbits Earth in about a month", "TRUE"),
      ("The Moon is only visible at night", "FALSE \u2014 often visible by day"),
    ],
    wagoll=("The Moon does not make light. Sunlight reflects off it, and because the Moon orbits "
            "the Earth roughly once a month, we see different amounts of the lit half. That is "
            "what makes the phases."),
  ),
  independent=dict(
    supported="Build the phase wheel from the kit and label full, new and crescent using the word bank.",
    standard="Build and label the phase wheel, then write why the shape appears to change.",
    stretch="Build and label the wheel, explain the phases, and explain how a lunar eclipse is different.",
  ),
  lundy=dict(
    space="The torch model needs low light. You will get a warning before the lights change, every time.",
    voice="If the model does not convince you, say so and we will re-run it from your seat's angle.",
    audience="Your phase wheel goes into the Entry Level Science evidence folder and onto the Space Board.",
    influence="This lesson closes the Autumn 1 block \u2014 the class chooses the Aut2 space question.",
  ),
  exit=dict(
    supported="Does the Moon make its own light? Yes / No",
    standard="How long does the Moon take to orbit the Earth?",
    stretch="Explain why phases are not caused by the Earth's shadow.",
  ),
  exit_key=["No",
            "About 28 days, roughly a month.",
            "Phases happen every month and depend on viewing angle; Earth's shadow only reaches the Moon during a rare eclipse."],
  witness=[
    "Stated that the Moon orbits Earth in about a month.",
    "Explained that moonlight is reflected sunlight.",
    "Modelled or described the cause of the phases.",
  ],
  ta_rule="ONE RULE: half the Moon is always lit. What changes is where we are looking from.",
  ta_notes=[
    "Warn before dimming the lights. Every time, not just the first.",
    "This closes Autumn 1. The Entry Level / UAS evidence review is scheduled at Aut2\u00b7W7, not in this lesson.",
  ],
  coldcall=[
    ("Watch me make the phases happen", "What is actually changing \u2014 the light or my angle?"),
    ("What causes it?", "Which one of these IS a shadow?"),
    ("Sort the statements", "Can you see the Moon in the daytime?"),
  ],
  uas="AQA UAS: 'Earth &amp; space'.",
),
]
