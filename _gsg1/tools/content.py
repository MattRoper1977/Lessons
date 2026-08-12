# -*- coding: utf-8 -*-
"""GSG-1 per-lesson content table.

Every retrieval prompt below derives from the taught lessons' own LO/KO text
in this suite. Nothing reaches for content that has not been taught; where the
history is too thin, the slide DECLARES the substitution rather than inventing
a prior topic. W1-W2 are baseline and are never named or linked.

Carrier sentences are written at the simplest level the science allows
(A2/A3 rule) with protected vocabulary kept verbatim.
"""

# Protected vocabulary — must survive verbatim through every edit (A3 gate).
PROTECTED = [
    "friction", "surface", "resistance", "force", "grip",
    "mechanism", "lever", "pulley", "gear", "pivot", "effort", "load",
    "variable", "fair test", "control", "measure", "unit", "mean", "evidence",
    "orbit", "gravity", "planet", "Solar System", "phase", "eclipse",
    "model", "predict", "prediction", "observation",
]

L = {}

L["W3A"] = dict(
    file="SCI_G_W3A_Friction_Explore.html", topic="friction",
    declare="<b>Weeks 1 and 2 were baseline.</b> No science has been taught yet, "
            "so all three retrieval prompts ask what you already know from outside "
            "school. Nothing before this lesson is being recalled.",
    r=[
        dict(badge="R1", when="What you already know",
             sup="Point to something here that would be hard to slide along the floor.",
             std="Name one thing that is hard to push along the floor. Say why you think it is hard.",
             stg="Name one everyday job that would be impossible if nothing gripped anything."),
        dict(badge="R2", when="What you already know",
             sup="Point or say: which is easier to walk on, wet ice or a dry path?",
             std="Which is easier to walk on, wet ice or a dry path? Say what makes the difference.",
             stg="The same shoes feel different on ice and on a dry path. Explain why."),
        dict(badge="R3", when="What you already know",
             sup="Show with your hands what happens when you rub them together fast.",
             std="Rub your hands together. Say what you can feel changing.",
             stg="Your hands warm up when you rub them. Where do you think that heat comes from?"),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="Look at the two soles. Point to the one that grips.",
              std="Trainers have patterned soles. An ice rink is kept smooth. Both are on purpose. Why?",
              stg="Trainers grip and ice rinks slide, both by design. What is being controlled in each case?"),
    helps="shows that friction acts against the direction of motion, and that grip "
          "comes from the pair of surfaces touching, not from one of them alone",
    hides="the size of the force, the heat it produces, and the tiny roughness that "
          "is doing the actual work",
    words=[("friction", "the rub that slows things down"),
           ("surface", "the outside face that touches"),
           ("resistance", "pushing back against movement")],
    commit=dict(q="Before we test: which sole will grip more?",
                opts=["The patterned sole", "The smooth sole", "They will grip the same"]),
)

L["W3B"] = dict(
    file="SCI_G_W3B_Friction_Do.html", topic="friction on surfaces",
    declare="<b>Week 3 is the first taught week.</b> R1 recalls last lesson. R2 and "
            "R3 have no earlier taught science to reach, so they ask what you "
            "already know. This is declared, not hidden.",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to a surface here where friction is high.",
             std="Last lesson you decided when friction helps. Give one place it helps.",
             stg="Last lesson you found friction can be a problem too. Give one place a designer would want less of it."),
        dict(badge="R2", when="What you already know",
             sup="Point or say: which slides further on a smooth floor, a sock or a rubber shoe?",
             std="Which would slide further on a smooth floor, a sock or a rubber shoe? Say why.",
             stg="Predict which slides further, then say what you would keep the same to be sure."),
        dict(badge="R3", when="What you already know",
             sup="Show how you would make a toy car go further along the floor.",
             std="How would you make a toy car travel further along the floor?",
             stg="A toy car stops sooner than you expected. Name two things that could explain it."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="We test surfaces today. Point to the one you think will grip most.",
              std="Today we test surfaces. Which surface will grip most, and how will we know?",
              stg="Today we test surfaces. What would make our answer trustworthy to someone who was not here?"),
    helps="lets you compare surfaces side by side when every surface gets the same "
          "release, so the surface is the only thing you changed",
    hides="how evenly each surface was laid, the friction inside the wheels, and the "
          "air pushing back on the car",
    words=[("evidence", "what you found out, written down"),
           ("observation", "what you saw, recorded carefully"),
           ("repeat", "doing it again the same way")],
    commit=dict(q="Before we test: which surface will grip most?",
                opts=["Carpet", "Wood", "Smooth plastic"]),
)

L["W4A"] = dict(
    file="SCI_G_W4A_Mechanisms_Explore.html", topic="levers, pulleys and gears",
    declare="<b>Week 4 has one taught week behind it.</b> R3 is a second Week 3 "
            "retrieval. That is declared here rather than reaching for science "
            "that has not been taught.",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to the surface from last lesson that gripped the most.",
             std="Last lesson you tested surfaces. Which gave the most friction, and how did you know?",
             stg="Last lesson you used results as evidence. What made one result more trustworthy than another?"),
        dict(badge="R2", when="Week 3",
             sup="Say one place friction helps.",
             std="In Week 3 you decided friction can help or get in the way. Give one example of each.",
             stg="Week 3: explain why the same force can be useful in one design and a problem in another."),
        dict(badge="R3", when="Week 3 again — declared",
             sup="Show with your hands what friction does to something sliding.",
             std="What does friction do to an object that is trying to slide?",
             stg="Friction acts against sliding. Name something else it produces that you could feel."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="Point to the door handle. It helps you push.",
              std="Some tools let a small push do a big job. How do you think a door handle helps?",
              stg="A small effort can move a big load. What do you think is being given up to get that?"),
    helps="shows where the effort, the pivot and the load sit, and that the mechanism "
          "changes the force you need",
    hides="the friction in the joint, the weight of the mechanism itself, and how far "
          "your hand has to travel",
    words=[("mechanism", "a part that changes a force"),
           ("pivot", "the point it turns around"),
           ("effort", "the push or pull you supply")],
    commit=dict(q="Before we look: what does a lever change?",
                opts=["How big the force needs to be", "Which direction the force acts",
                      "Both of those"]),
)

L["W4B"] = dict(
    file="SCI_G_W4B_Mechanisms_Do.html", topic="lever investigation",
    declare="",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to a lever in this room.",
             std="Last lesson you found levers, pulleys and gears. Name one and say what it changes.",
             stg="Last lesson: explain what a mechanism changes about a force, and what it leaves alone."),
        dict(badge="R2", when="Week 3",
             sup="Say which surface gripped most in the surface test.",
             std="In Week 3 you tested surfaces. What did you keep the same so the test was fair?",
             stg="Week 3: why does keeping everything else the same make a comparison trustworthy?"),
        dict(badge="R3", when="Week 3",
             sup="Point to something that needs grip.",
             std="Week 3: give one place friction helps and one place it gets in the way.",
             stg="Week 3: friction and levers both change how hard a job feels. Say how they differ."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="Watch the seesaw. Point to where you would sit to lift a heavy friend.",
              std="On a seesaw, where would you sit to lift someone heavier than you?",
              stg="Moving the pivot makes lifting easier. Predict what gets harder at the same time."),
    helps="shows how moving the pivot changes the effort needed to lift the load",
    hides="the friction at the pivot, the bending of a real beam, and the extra "
          "distance your hand must move",
    words=[("load", "the thing being lifted"),
           ("pivot", "the point it turns around"),
           ("effort", "the push or pull you supply")],
    commit=dict(q="Before we test: where should the pivot go to lift most easily?",
                opts=["Near the load", "In the middle", "Near your hands"]),
)

L["W5A"] = dict(
    file="SCI_G_W5A_Fair_Test_Explore.html", topic="planning a fair test",
    declare="",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to where the pivot was when lifting was easiest.",
             std="Last lesson you moved the pivot. What happened to the effort needed?",
             stg="Last lesson: explain the trade you found when the pivot moved nearer the load."),
        dict(badge="R2", when="Week 4",
             sup="Name one machine that helps you lift.",
             std="Week 4: name a lever, a pulley or a gear and say what it changes.",
             stg="Week 4: explain why a mechanism cannot give you something for nothing."),
        dict(badge="R3", when="Week 3",
             sup="Say one place friction helps.",
             std="Week 3: what does friction do to a sliding object?",
             stg="Week 3: you compared surfaces. What made that comparison believable?"),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="Look at the test. Point to the one thing that should change.",
              std="If two things change at once in a test, why can we not tell which one mattered?",
              stg="A test changes two things at once. Say exactly what it can no longer prove."),
    helps="shows one deliberate change set against the variables you decided to control",
    hides="how much error there is in each measurement, and the judgement about how "
          "big a difference has to be before it counts",
    words=[("variable", "a thing that can change"),
           ("control", "keep it the same on purpose"),
           ("fair test", "only one thing changed on purpose")],
    commit=dict(q="Before we repair it: this test changes surface AND ramp height. Can it answer the question?",
                opts=["Yes", "No", "Not sure yet"]),
)

L["W5B"] = dict(
    file="SCI_G_W5B_Fair_Test_Do.html", topic="running and concluding a fair test",
    declare="",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to the thing we change in our test.",
             std="Last lesson you named the variable to change, the one to measure, and the ones to keep the same. Name each for our test.",
             stg="Last lesson: explain why the controlled variables decide whether the result means anything."),
        dict(badge="R2", when="Week 4",
             sup="Name one machine that makes lifting easier.",
             std="Week 4: what does moving a lever's pivot change?",
             stg="Week 4: a mechanism trades force for distance. Explain that trade in your own words."),
        dict(badge="R3", when="Week 3",
             sup="Say which surface gripped most.",
             std="Week 3: which surface gave the most friction, and how did you know?",
             stg="Week 3: what would you repeat before trusting a single surface result?"),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="We measure today. Point to the ruler.",
              std="Today we record results with units. Why does a number with no unit tell us nothing?",
              stg="Two groups get different results for the same test. Name two honest reasons that could happen."),
    helps="shows the pattern across your repeats once each set is averaged",
    hides="how carefully each reading was taken, and whether the difference is bigger "
          "than the error in your measuring",
    words=[("mean", "the middle value of your repeats"),
           ("unit", "what the number is measured in"),
           ("evidence", "what you found out, written down")],
    commit=dict(q="Before we start: how many times should we repeat each surface?",
                opts=["Once", "Three times", "As many as time allows"]),
)

L["W6A"] = dict(
    file="SCI_G_W6A_Earth_And_Planets_Explore.html", topic="Earth and the planets",
    declare="",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to the units we wrote next to our numbers.",
             std="Last lesson you recorded results with units. Why did you repeat the readings?",
             stg="Last lesson: explain how repeats changed how much you trusted the evidence."),
        dict(badge="R2", when="Week 5",
             sup="Say the one thing we change in a fair test.",
             std="Week 5: what must stay the same in a fair test, and why?",
             stg="Week 5: explain why a fair test is about the claim you want to make, not the equipment."),
        dict(badge="R3", when="Week 4",
             sup="Point to something that turns.",
             std="Week 4: what does a gear change about a turning force?",
             stg="Week 4: a force can be redirected or changed in size. Give one example of each."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="Look at the Solar System picture. Point to Earth.",
              std="The planets do not fly off into space. What do you think holds them on their paths?",
              stg="A planet moves forward and is pulled inward at the same time. What shape does that make?"),
    helps="shows the order of the planets and that each orbit is a closed path around the Sun",
    hides="the true sizes and distances, and the fact that a real orbit is a stretched "
          "circle rather than a perfect one",
    words=[("orbit", "the path one object takes around another"),
           ("gravity", "the pull between masses"),
           ("Solar System", "the Sun and everything going round it")],
    commit=dict(q="Before we look: what holds the planets on their paths?",
                opts=["Gravity", "Air", "Nothing — they just keep moving"]),
)

L["W6B"] = dict(
    file="SCI_G_W6B_Earth_And_Planets_Do.html", topic="building the orbit model",
    declare="",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to the planet closest to the Sun.",
             std="Last lesson you put the planets in order. Which one is third from the Sun?",
             stg="Last lesson: explain how gravity keeps a planet in orbit instead of moving in a straight line."),
        dict(badge="R2", when="Week 5",
             sup="Say the one thing we change in a fair test.",
             std="Week 5: name what to change, what to measure and what to keep the same.",
             stg="Week 5: explain why a model, like a test, has to be honest about its limits."),
        dict(badge="R3", when="Week 3",
             sup="Point to a surface that grips.",
             std="Week 3: what does friction do to a moving object?",
             stg="Week 3: there is almost no friction in space. Say what that changes about motion."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="We build a model today. Point to what it should show.",
              std="Our model cannot show the right size and the right distance at once. Which should we choose?",
              stg="Every model gets something wrong on purpose. What must ours get right to be useful?"),
    helps="shows the order of the planets and the direction they travel around the Sun",
    hides="scale — a model that is honest about distance cannot be honest about size "
          "on the same page",
    words=[("model", "something built to stand for the real thing"),
           ("orbit", "the path one object takes around another"),
           ("represent", "stand for something real")],
    commit=dict(q="Before we build: should our model be true to size or true to distance?",
                opts=["True to size", "True to distance", "It cannot be both"]),
)

L["W7A"] = dict(
    file="SCI_G_W7A_The_Moon_Explore.html", topic="the Moon's journey",
    declare="",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to the part of your model that was accurate.",
             std="Last lesson you built a Solar System model. Name one thing it showed well and one it could not show.",
             stg="Last lesson: explain how you decided what your model was allowed to get wrong."),
        dict(badge="R2", when="Week 6",
             sup="Point to Earth in the picture.",
             std="Week 6: what holds the planets on their orbits around the Sun?",
             stg="Week 6: explain how movement and gravity together produce an orbit."),
        dict(badge="R3", when="Week 5",
             sup="Say the one thing we change in a fair test.",
             std="Week 5: why do we repeat measurements?",
             stg="Week 5: explain how you would check an observation you could not repeat."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="Look at the Moon pictures. Point to the fullest one.",
              std="The Moon looks a different shape each week. Does the Moon itself really change?",
              stg="The Sun always lights half the Moon. So why do we see different shapes?"),
    helps="shows that the lit half always faces the Sun while the part we can see changes",
    hides="the tilt of the Moon's orbit, which is why we do not get an eclipse every month",
    words=[("phase", "the shape of the Moon we can see"),
           ("orbit", "the path one object takes around another"),
           ("observer", "the person looking")],
    commit=dict(q="Before we look: does the Moon itself change shape?",
                opts=["Yes", "No", "Only part of it does"]),
)

L["W7B"] = dict(
    file="SCI_G_W7B_The_Moon_Do.html", topic="modelling Moon phases",
    declare="",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to the Full Moon picture.",
             std="Last lesson you explained why the Moon seems to change shape. What is really changing?",
             stg="Last lesson: explain why the lit half of the Moon stays the same even though our view does not."),
        dict(badge="R2", when="Week 6",
             sup="Point to the Sun in the model.",
             std="Week 6: what keeps the Moon travelling around Earth?",
             stg="Week 6: explain why an orbit needs motion and gravity acting together."),
        dict(badge="R3", when="Week 4",
             sup="Point to something that turns.",
             std="Week 4: what does a mechanism change about a force?",
             stg="Week 4: explain what a model of a mechanism can show and what it hides."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="We make the phases with a ball and a lamp. Point to the lamp.",
              std="Today you make the phases appear on command. What will the lamp stand for?",
              stg="A phase and an eclipse look related but are not the same. What must your model separate?"),
    helps="lets you produce each phase on demand and see the positions that cause it",
    hides="the tilt of the Moon's orbit and the real distances, which is why eclipses "
          "are rare rather than monthly",
    words=[("phase", "the shape of the Moon we can see"),
           ("eclipse", "one object blocking light to another"),
           ("model", "something built to stand for the real thing")],
    commit=dict(q="Before we model it: what makes a phase?",
                opts=["Earth's shadow on the Moon", "Which lit part we can see", "Clouds"]),
)
