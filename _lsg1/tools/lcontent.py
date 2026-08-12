# -*- coding: utf-8 -*-
"""LSG-1 per-lesson content table (LAUNCH GCSE Biology, Topic 1).

Every retrieval prompt derives from the taught lessons' own LO text in this
suite. Nothing reaches for science that has not been taught; where the history
is too thin the slide DECLARES the substitution. W1-W2 are baseline and are
never named as a topic or linked.

LAUNCH's three-lesson weekly arc gives a richer spine than the A/B suites:
L2 retrieves L1, L3 retrieves L2 then L1, and the next week's L1 retrieves the
prior week's arc.

Carriers are written at the simplest level the Biology allows. Protected
vocabulary survives verbatim.
"""

PROTECTED = [
    "magnification", "resolution", "eyepiece", "objective", "micrometre",
    "diffusion", "osmosis", "active transport", "concentration gradient",
    "partially permeable", "membrane", "net movement", "respiration",
    "alveoli", "root hair", "percentage change", "gradient", "energy",
    "describe", "explain", "evaluate", "calculate", "compare",
    "evidence", "method", "variable",
]

L = {}

L["W3L1"] = dict(
    file="SCI_L_W3L1_Microscopy_Introduce.html",
    declare="<b>Weeks 1 and 2 were baseline.</b> No Biology has been taught yet, so all "
            "three retrieval prompts ask what you already know from outside this room. "
            "Nothing before this lesson is being recalled.",
    r=[
        dict(badge="R1", when="What you already know",
             sup="Point to something in this room you would need to look at very closely to see properly.",
             std="Name one thing too small to see clearly with just your eyes.",
             stg="Name something scientists need to see that no eye could ever resolve unaided."),
        dict(badge="R2", when="What you already know",
             sup="Say or point: does a magnifying glass make things bigger, or clearer?",
             std="A magnifying glass makes things look bigger. Does bigger always mean you can see more detail?",
             stg="Zooming a phone photo makes it bigger but not clearer. Say what that tells you about size and detail."),
        dict(badge="R3", when="What you already know",
             sup="Show with your hands how close you would hold something small to see it.",
             std="Why do things look blurred when you bring them too close to your eyes?",
             stg="Your eye has a limit on the fine detail it can separate. What would you need to get past it?"),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="Look at the microscope. Point to the eyepiece — the part you look through.",
              std="A microscope has two lenses, not one. Why do you think it needs both?",
              stg="A microscope multiplies the eyepiece by the objective. Predict what that does to the image, and what it cannot fix."),
    helps="shows how light passes through the specimen and both lenses to build the image you see",
    hides="the limit set by the wavelength of light, which is what finally stops a light "
          "microscope resolving finer detail no matter how much you magnify",
    words=[("magnification", "how many times bigger the image looks"),
           ("resolution", "how much fine detail you can still tell apart"),
           ("objective", "the lens closest to the specimen")],
    commit=dict(q="Two images are the same size. One shows two close points as separate. What is better about it?",
                opts=["It has better resolution", "It has more magnification",
                      "Size and detail are the same thing"]),
)

L["W3L2"] = dict(
    file="SCI_L_W3L2_Calculating_Magnification_Explore.html",
    declare="<b>Week 3 is the first taught week.</b> R1 recalls last lesson. R2 and R3 "
            "have no earlier taught Biology to reach, so they ask what you already know. "
            "Declared, not hidden.",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to the eyepiece on the microscope diagram.",
             std="Last lesson you separated magnification from resolution. Say what each one means.",
             stg="Last lesson: a bigger image is not automatically more useful. Explain why."),
        dict(badge="R2", when="What you already know",
             sup="Which is longer: 1 millimetre or 1 centimetre? Point to the longer one.",
             std="How many millimetres are there in one centimetre?",
             stg="Why does a calculation go wrong if two measurements are in different units?"),
        dict(badge="R3", when="What you already know",
             sup="Say or point: if something is 10 times bigger, is it larger or smaller?",
             std="If a picture is 10 times bigger than the real object, how do you get back to the real size?",
             stg="Name the operation that undoes multiplying, and say when you would need it here."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="Look at the drawing and the real cell. Point to the bigger one.",
              std="A drawn cell is far bigger than the real one. How could we work out how much bigger?",
              stg="You have a drawing and the real size. Predict which calculation gives magnification."),
    helps="shows the three quantities together, so you can see which one you are solving for",
    hides="that the units must match before you divide — the triangle looks the same "
          "whether your numbers are in millimetres or micrometres",
    words=[("magnification", "how many times bigger the image is than the real thing"),
           ("micrometre", "one thousandth of a millimetre"),
           ("calculate", "work it out with numbers, showing the steps")],
    commit=dict(q="An image is 40 mm across. The real object is 0.5 mm. Before calculating: what will magnification be?",
                opts=["Bigger than 1", "Smaller than 1", "Exactly 1"]),
)

L["W3L3"] = dict(
    file="SCI_L_W3L3_Magnification_Lab_Do.html",
    declare="<b>Week 3 has no taught week behind it.</b> R3 is a second Week 3 retrieval, "
            "declared here rather than reaching for Biology that has not been taught.",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to the magnification formula on the card.",
             std="Last lesson you calculated magnification. Say what you divide by what.",
             stg="Last lesson: explain why the units must match before you divide."),
        dict(badge="R2", when="Week 3 · lesson 1",
             sup="Say which lens you look through.",
             std="What is the difference between magnification and resolution?",
             stg="Past a microscope's resolution, more magnification adds no new detail. Explain why."),
        dict(badge="R3", when="Week 3 again — declared",
             sup="Point to the millimetre marks on a ruler.",
             std="How many micrometres are there in one millimetre?",
             stg="Explain why cell sizes are usually quoted in micrometres rather than millimetres."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="You will solve problems on your own today. Point to the first question.",
              std="Today you work independently. What would make your method clear to someone reading it?",
              stg="An answer with the right number but no method loses more than marks. Say what it loses scientifically."),
    helps="shows a worked method laid out step by step, so the reasoning is visible and checkable",
    hides="whether you could have caught your own error — a worked example never shows "
          "you the check you did not run",
    words=[("method", "the steps you took, written so another person could repeat them"),
           ("magnification", "how many times bigger the image is than the real thing"),
           ("calculate", "work it out with numbers, showing the steps")],
    commit=dict(q="Before you start: what makes an answer easy for another person to check?",
                opts=["The working is shown step by step", "The answer is written large",
                      "The answer is given without units"]),
)

L["W4L1"] = dict(
    file="SCI_L_W4L1_Diffusion_Introduce.html", declare="",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to the units you wrote in your answer.",
             std="Last lesson you solved magnification problems. Why did the units have to match?",
             stg="Last lesson: explain how you checked whether your answer was sensible."),
        dict(badge="R2", when="Week 3",
             sup="Say which lens is closest to the specimen.",
             std="Week 3: what is the difference between magnification and resolution?",
             stg="Week 3: a light microscope has a limit. Explain why magnification cannot get past it."),
        dict(badge="R3", when="Week 3",
             sup="Point to something you could only see with a microscope.",
             std="Week 3: why do we measure cells in micrometres?",
             stg="Week 3: cells are small. Say why that matters for how substances get in and out."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="Someone opens perfume at the front. Point to where you would smell it first.",
              std="Perfume opened at the front of the room reaches the back with nobody fanning it. How?",
              stg="Particles move randomly in all directions, yet the smell spreads one way overall. Explain how both can be true."),
    helps="shows particles moving randomly and still producing a net movement from high to low concentration",
    hides="that individual particles keep moving both ways the whole time — net movement is "
          "a balance, not a one-way march",
    words=[("diffusion", "spreading out from where there is more to where there is less"),
           ("concentration gradient", "the difference between a crowded area and an empty one"),
           ("net movement", "the overall direction once both ways are counted")],
    commit=dict(q="Before we model it: once the smell has spread evenly, what are the particles doing?",
                opts=["Still moving, both ways", "They have stopped", "Moving one way only"]),
)

L["W4L2"] = dict(
    file="SCI_L_W4L2_Diffusion_Lungs_Explore.html", declare="",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to the crowded side of the diagram.",
             std="Last lesson you defined diffusion. Which way is the net movement?",
             stg="Last lesson: name two factors that change how fast diffusion happens, and say why."),
        dict(badge="R2", when="Week 3",
             sup="Say what a microscope helps you see.",
             std="Week 3: why do we measure cells in micrometres?",
             stg="Week 3: explain how a microscope let biologists see the structures we are about to explain."),
        dict(badge="R3", when="Week 3",
             sup="Point to the eyepiece.",
             std="Week 3: what is the difference between magnification and resolution?",
             stg="Week 3: resolution decides what detail you can report, not magnification. Explain why."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="Look at the lung diagram. Point to the air sacs.",
              std="Your lungs hold millions of tiny air sacs instead of two big bags. Why so many small ones?",
              stg="Predict which features of an exchange surface would make diffusion fastest, and say why for each."),
    helps="shows the alveolus and the capillary side by side, so the gradient and the short "
          "distance are visible at once",
    hides="the scale — a real alveolar wall is a fraction of the thickness this drawing "
          "can show, and that thinness is doing much of the work",
    words=[("alveoli", "the tiny air sacs in the lungs"),
           ("diffusion", "spreading out from where there is more to where there is less"),
           ("concentration gradient", "the difference between a crowded area and an empty one")],
    commit=dict(q="Before we look: what would speed up diffusion at an exchange surface?",
                opts=["A bigger surface area", "A thicker wall", "A smaller gradient"]),
)

L["W4L3"] = dict(
    file="SCI_L_W4L3_Diffusion_Explanation_Do.html", declare="",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to the air sac on the diagram.",
             std="Last lesson you applied diffusion to the lungs. Name one adaptation and what it does.",
             stg="Last lesson: explain how three alveolar adaptations act together on the rate."),
        dict(badge="R2", when="Week 4 · lesson 1",
             sup="Say which way particles move overall in diffusion.",
             std="Week 4: define diffusion using the words net movement and gradient.",
             stg="Week 4: explain why diffusion needs no energy from the cell."),
        dict(badge="R3", when="Week 3",
             sup="Point to something too small to see without a microscope.",
             std="Week 3: why are cells measured in micrometres?",
             stg="Week 3: explain why small size and short distances matter for exchange."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="Today you write the explanation. Point to the first sentence starter.",
              std="Today you build a full explanation. What has to be in it besides the word diffusion?",
              stg="An explanation that names a process but never links it to evidence is incomplete. Say what is missing."),
    helps="shows the shape of a complete explanation: direction, then gradient, then adaptation",
    hides="whether your own sentence actually links the parts — a frame can be filled in "
          "and still not explain anything",
    words=[("explain", "say how or why, linking cause to effect"),
           ("diffusion", "spreading out from where there is more to where there is less"),
           ("evidence", "the observation or data your claim rests on")],
    commit=dict(q="Before you write: what turns a description into an explanation?",
                opts=["It links cause to effect", "It is longer", "It uses more key words"]),
)

L["W5L1"] = dict(
    file="SCI_L_W5L1_Osmosis_Introduce.html", declare="",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to the word diffusion on the card.",
             std="Last lesson you wrote diffusion explanations. What must a good explanation link?",
             stg="Last lesson: an answer needs direction, gradient and adaptation. Explain how they combine."),
        dict(badge="R2", when="Week 4",
             sup="Say which way particles spread.",
             std="Week 4: define diffusion, and name one factor that changes its rate.",
             stg="Week 4: explain why a thin, large exchange surface speeds diffusion up."),
        dict(badge="R3", when="Week 3",
             sup="Point to the lens you look through.",
             std="Week 3: what does resolution mean?",
             stg="Week 3: explain why we needed microscopy before we could explain membranes at all."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="Look at the two sides of the bag. Point to the side with more water.",
              std="A membrane lets water through but blocks sugar. Predict which way the water moves.",
              stg="If only water can cross, explain what happens to the concentrations on both sides over time."),
    helps="shows a membrane that lets water through and holds larger molecules back, so the "
          "direction of water movement follows from the picture",
    hides="that the membrane is not a simple sieve — it is a living structure, and the model "
          "makes it look like a fixed mesh",
    words=[("osmosis", "water moving across a membrane towards the stronger solution"),
           ("partially permeable", "lets some things through but not others"),
           ("membrane", "the thin layer around a cell")],
    commit=dict(q="Before we test: water can cross, sugar cannot. Which way does water move overall?",
                opts=["Towards the stronger sugar solution", "Towards the weaker solution",
                      "It does not move"]),
)

L["W5L2"] = dict(
    file="SCI_L_W5L2_Osmosis_Core_Practical_Explore.html", declare="",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to the membrane in the diagram.",
             std="Last lesson you defined osmosis. Which way does water move, and what must the membrane be?",
             stg="Last lesson: explain osmosis. Use the words partially permeable and concentration."),
        dict(badge="R2", when="Week 4",
             sup="Say which way particles spread in diffusion.",
             std="Week 4: what is the difference between diffusion and osmosis?",
             stg="Week 4: explain why osmosis is a special case of diffusion rather than a separate idea."),
        dict(badge="R3", when="Week 3",
             sup="Point to the millimetre marks on the ruler.",
             std="Week 3: why must units match before you calculate?",
             stg="Week 3: explain why percentage change is used instead of raw mass change."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="You will weigh potato pieces today. Point to the balance.",
              std="Today you measure mass before and after. Why would we use percentage change rather than grams?",
              stg="Different pieces start at different masses. Explain how percentage change makes them comparable."),
    helps="shows the whole practical in order, so the controls and the one deliberate change stay visible",
    hides="the everyday things that ruin the result — uneven blotting, pieces cut at "
          "different lengths, and time in solution varying between tubes",
    words=[("osmosis", "water moving across a membrane towards the stronger solution"),
           ("percentage change", "the change compared with what you started with, as a percentage"),
           ("variable", "something that can change; here, only the concentration should")],
    commit=dict(q="Before we start: why weigh each piece BEFORE it goes in the tube?",
                opts=["You cannot get the starting mass back afterwards",
                      "It makes the pieces the same size", "It speeds up osmosis"]),
)

L["W5L3"] = dict(
    file="SCI_L_W5L3_Osmosis_Data_Do.html", declare="",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to the balance you used.",
             std="Last lesson you ran the osmosis practical. Which variable did you change, and which did you keep the same?",
             stg="Last lesson: explain why percentage change was the right measure for comparing pieces."),
        dict(badge="R2", when="Week 5 · lesson 1",
             sup="Say which way water moves in osmosis.",
             std="Week 5: define osmosis using the words membrane and concentration.",
             stg="Week 5: explain what happens to a cell placed in pure water, and why."),
        dict(badge="R3", when="Week 4",
             sup="Point to the crowded side of the diagram.",
             std="Week 4: define diffusion and name one factor affecting its rate.",
             stg="Week 4: explain how diffusion and osmosis are related but not identical."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="Look at the graph. Point to where the line crosses zero.",
              std="Somewhere between your concentrations, the potato neither gains nor loses mass. How would you find it?",
              stg="Explain what the crossing point tells you about the solution inside the potato cells."),
    helps="shows the trend across all concentrations, including the point where the change is zero",
    hides="the uncertainty in every plotted point — a smooth line through scattered "
          "results looks more certain than the data actually is",
    words=[("percentage change", "the change compared with what you started with, as a percentage"),
           ("evaluate", "judge how good the method or evidence was, and say why"),
           ("evidence", "the data your conclusion rests on")],
    commit=dict(q="Before we plot: what would the zero-change concentration tell you?",
                opts=["It matches the concentration inside the cells",
                      "The potato has stopped working", "The balance is broken"]),
)

L["W6L1"] = dict(
    file="SCI_L_W6L1_Active_Transport_Introduce.html", declare="",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to the zero line on the graph.",
             std="Last lesson you analysed osmosis data. What did the zero-change point tell you?",
             stg="Last lesson: explain one weakness in the method and how you would reduce it."),
        dict(badge="R2", when="Week 5",
             sup="Say which way water moves across a membrane.",
             std="Week 5: define osmosis, and say what the membrane must be.",
             stg="Week 5: explain why osmosis needs no energy from the cell."),
        dict(badge="R3", when="Week 4",
             sup="Point to the side with more particles.",
             std="Week 4: which way is the net movement in diffusion?",
             stg="Week 4: explain what diffusion and osmosis have in common about direction."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="Look at the root hair. Point to the soil side.",
              std="A root takes in minerals even when the soil has fewer than the root does. How can that work?",
              stg="Moving something against its gradient cannot happen for free. Predict what the cell must supply."),
    helps="shows the gradient and the direction of movement together, so it is clear the "
          "movement is running the wrong way up the gradient",
    hides="the carrier proteins doing the actual work, and the respiration supplying them "
          "with energy — the arrow makes it look effortless",
    words=[("active transport", "moving substances against the gradient, using energy"),
           ("concentration gradient", "the difference between a crowded area and an empty one"),
           ("respiration", "the reaction in cells that releases energy")],
    commit=dict(q="Before we look: what must a cell supply to move minerals against the gradient?",
                opts=["Energy from respiration", "More water", "Nothing — it happens by itself"]),
)

L["W6L2"] = dict(
    file="SCI_L_W6L2_Root_Hairs_And_Gut_Explore.html", declare="",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to the word energy on the card.",
             std="Last lesson you met active transport. What makes it different from diffusion?",
             stg="Last lesson: explain why active transport stops if respiration stops."),
        dict(badge="R2", when="Week 5",
             sup="Say which way water moves in osmosis.",
             std="Week 5: define osmosis using the word membrane.",
             stg="Week 5: explain why osmosis and active transport move things for different reasons."),
        dict(badge="R3", when="Week 4",
             sup="Point to the air sac in the lung diagram.",
             std="Week 4: name one adaptation that speeds up diffusion.",
             stg="Week 4: explain how a large surface area helps any exchange process."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="Look at the root hair cell. Point to its long thin shape.",
              std="A root hair cell is long and thin. How does that shape help it take in minerals?",
              stg="Predict what an experiment would show if you deprived root cells of oxygen, and say why."),
    helps="shows the same process in two very different places, so the pattern is separable "
          "from the particular cell",
    hides="the rate — the diagram cannot show how much slower uptake becomes when "
          "respiration is limited",
    words=[("root hair", "a long thin outgrowth of a root cell that increases surface area"),
           ("active transport", "moving substances against the gradient, using energy"),
           ("respiration", "the reaction in cells that releases energy")],
    commit=dict(q="Before we look at the data: what happens to mineral uptake if oxygen is removed?",
                opts=["It falls", "It rises", "It stays the same"]),
)

L["W6L3"] = dict(
    file="SCI_L_W6L3_Compare_Transport_Do.html", declare="",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to the root hair on the diagram.",
             std="Last lesson you applied active transport to root hairs and gut. What did the evidence link it to?",
             stg="Last lesson: uptake fell without oxygen. Explain how that supports active transport rather than diffusion."),
        dict(badge="R2", when="Week 6 · lesson 1",
             sup="Say what active transport needs that diffusion does not.",
             std="Week 6: define active transport using the words gradient and energy.",
             stg="Week 6: explain why active transport is the only one of the three that can run uphill."),
        dict(badge="R3", when="Week 5",
             sup="Point to the membrane.",
             std="Week 5: define osmosis.",
             stg="Week 5: explain what osmosis and diffusion share, and where they differ."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="Three processes, one table. Point to the column for energy.",
              std="Today you compare all three processes. What questions would separate them?",
              stg="Given an unfamiliar example, name the two questions that decide which process it is."),
    helps="puts the three processes side by side, so the deciding differences stand out",
    hides="the messy reality that a real cell runs all three at once, and the table makes "
          "them look like separate compartments",
    words=[("active transport", "moving substances against the gradient, using energy"),
           ("compare", "say what is the same and what is different, on stated points"),
           ("concentration gradient", "the difference between a crowded area and an empty one")],
    commit=dict(q="Before we build the table: which question best separates the three processes?",
                opts=["Does it need energy from the cell?", "Does it happen in plants?",
                      "Is it fast or slow?"]),
)

L["W7L1"] = dict(
    file="SCI_L_W7L1_Topic_1_Round_Up_Introduce.html", declare="",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to the column that says energy.",
             std="Last lesson you compared the three transport processes. Which one needs energy?",
             stg="Last lesson: explain how you would decide the process from an unfamiliar example."),
        dict(badge="R2", when="Week 6",
             sup="Say where a root hair is found.",
             std="Week 6: how does a root hair cell take in minerals from dilute soil?",
             stg="Week 6: mineral uptake is linked to respiration. Explain the evidence for that."),
        dict(badge="R3", when="Weeks 3–5",
             sup="Point to the microscope.",
             std="Weeks 3–5: name the three ideas you have met — magnification, diffusion and one more.",
             stg="Weeks 3–5: microscopy came first. Explain how it made the transport explanations possible."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="Today we pull Topic 1 together. Point to the first idea on the map.",
              std="Today we connect the whole topic. Which two ideas do you think link most closely?",
              stg="Knowing facts separately is not the same as connecting them. Say what a connection adds."),
    helps="shows Topic 1 as connected ideas rather than a list, so links become visible",
    hides="which links you can actually make unprompted — a completed map does not show "
          "whether you built it or copied it",
    words=[("diffusion", "spreading out from where there is more to where there is less"),
           ("osmosis", "water moving across a membrane towards the stronger solution"),
           ("active transport", "moving substances against the gradient, using energy")],
    commit=dict(q="Before we map it: what makes knowledge usable in an exam?",
                opts=["Being able to connect ideas", "Remembering more words",
                      "Writing longer answers"]),
)

L["W7L2"] = dict(
    file="SCI_L_W7L2_Command_Words_Explore.html", declare="",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to two ideas that link on the map.",
             std="Last lesson you connected Topic 1. Name two ideas that link, and say how.",
             stg="Last lesson: explain one link across Topic 1 that you could use in an answer."),
        dict(badge="R2", when="Week 6",
             sup="Say which process needs energy.",
             std="Week 6: what makes active transport different from diffusion?",
             stg="Week 6: explain how evidence distinguishes active transport from diffusion."),
        dict(badge="R3", when="Week 5",
             sup="Point to the membrane on the diagram.",
             std="Week 5: define osmosis.",
             stg="Week 5: explain what percentage change let you compare that raw mass could not."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="Look at the two questions. Point to the first word of each.",
              std="Describe, explain and calculate are different instructions. What does each one ask you to do?",
              stg="Two questions on the same Biology can need completely different answers. Say what decides that."),
    helps="separates what the question is asking you to DO from the Biology you already know",
    hides="that more than one clear answer form can be acceptable — a decoder makes it "
          "look like each command word has exactly one shape",
    words=[("describe", "say what is there or what happens, without saying why"),
           ("explain", "say how or why, linking cause to effect"),
           ("evaluate", "weigh it up and reach a judgement you justify")],
    commit=dict(q="Before we decode: what does 'explain' ask for that 'describe' does not?",
                opts=["A reason linking cause to effect", "A longer answer",
                      "More key words"]),
)

L["W7L3"] = dict(
    file="SCI_L_W7L3_Exam_Practice_Do.html", declare="",
    r=[
        dict(badge="R1", when="Last lesson",
             sup="Point to the word explain on the card.",
             std="Last lesson you decoded command words. What does explain ask you to do?",
             stg="Last lesson: explain how the command word changes the shape of your answer."),
        dict(badge="R2", when="Week 7 · lesson 1",
             sup="Say one idea from Topic 1.",
             std="Week 7: name two Topic 1 ideas that connect, and say how.",
             stg="Week 7: explain a link across Topic 1 that an unfamiliar question might need."),
        dict(badge="R3", when="Weeks 3–6",
             sup="Point to the process that needs energy.",
             std="Weeks 3–6: state the magnification equation, and compare active transport with diffusion.",
             stg="Weeks 3–6: a question can ask about magnification or about water crossing a partially permeable membrane. Explain how you would tell which one it is testing."),
    ],
    lead=dict(badge="Lead-in", when="Into today",
              sup="Today you answer on your own, then improve one. Point to the first question.",
              std="Today you write, then improve one answer. What would make an improvement real rather than cosmetic?",
              stg="Rewriting an answer neatly is not improving it. Say what a genuine improvement changes."),
    helps="shows the answer and its improvement side by side, so the change itself is visible",
    hides="whether the improvement came from your own reading of the question or from being "
          "told the answer",
    words=[("explain", "say how or why, linking cause to effect"),
           ("evaluate", "weigh it up and reach a judgement you justify"),
           ("evidence", "the data or observation your answer rests on")],
    commit=dict(q="Before you improve an answer: what makes an improvement genuine?",
                opts=["It answers the command word better", "It is neater",
                      "It is longer"]),
)
