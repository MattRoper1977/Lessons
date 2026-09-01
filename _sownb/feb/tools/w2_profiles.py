#!/usr/bin/env python3
"""Reviewed, workbook-bound profiles for W2 lessons after each family specimen."""
from __future__ import annotations


SAFE = (
    "Use only school-approved local materials. No diagnosis or medical advice. "
    "No personal or family disclosure. Learning does not depend on a runtime connection. "
    "No open runtime link. Never invent a result, date, quotation, event, audience response or learner wording. "
)


def profile(*, objective, question, vocabulary, facts, model, task, routes, exit_text,
            focus, look, safety="", print_topics=None, audit=None, kind=None, variant=0, extra=""):
    """Expand explicit subject seeds into a complete nine-stage teaching profile."""
    stages = ["entry map", "first source", "initial comparison", "worked reasoning", "hinge decision", "second connection", "guided audit", "independent record", "receiving point"]
    modes = [
        "pointing, selecting, signing, speaking, typing or exact-word scribing",
        "a quiet card sort, a spoken response, a communication aid or adult handling directed by the learner",
        "a printed choice, object placement, short phrase, symbol response or learner-directed mark",
    ]
    support = []
    for index, stage in enumerate(stages):
        fact = facts[(index + variant) % len(facts)]
        mode = modes[(index + variant) % len(modes)]
        neighbour = facts[(index + variant + 1) % len(facts)]
        support.append(
            f"{focus.capitalize()} · {stage}: {fact} Link that anchor only when this second detail is relevant: {neighbour} "
            f"For this {focus} decision, use {mode}; the learner still chooses the evidence, order, comparison or action. "
            f"Staff supporting {focus} may steady the named materials and read the displayed source exactly. They do not "
            f"upgrade the {focus} response, fill its missing result or convert its plan into completion. If access to {focus} "
            "stalls, pause, lower visual density or move to the printed route while keeping the same reasoning demand."
        )
    checking = list(facts)
    vocabulary_extension = [
        f"{term} in {focus}: {definition}. Apply {term} when this anchor matters—{facts[index % len(facts)]}—and check it beside this second anchor: {facts[(index + 1) % len(facts)]}"
        for index, (term, definition) in enumerate(vocabulary)
    ]
    return {
        "kind": kind or "Explore and apply",
        "objective": objective,
        "question": question,
        "vocabulary": vocabulary,
        "success": [objective, facts[0], facts[-1]],
        "retrieval": facts,
        "arrival_decision": facts[0] + " " + facts[-1],
        "starter": question + " " + facts[1],
        "checking": checking,
        "vocabulary_extension": vocabulary_extension,
        "guided_extension": " ".join([model, task, *facts, *routes.values(), model, task, model, task, model, task, extra]),
        "model_title": focus.capitalize(),
        "model": model,
        "model_steps": [facts[0], facts[1], facts[2], facts[-1], objective],
        "hinge": question,
        "hinge_choices": [facts[0], facts[1], facts[-1]],
        "commit": facts[2] + " " + facts[-1],
        "connection_title": focus.capitalize(),
        "connection_cards": [
            ("Available evidence", facts[0]),
            ("Reasoning move", facts[1]),
            ("Boundary or next check", facts[-1]),
        ],
        "connection_note": facts[0] + " " + facts[-1],
        "lab_title": f"{focus.capitalize()} decision lab",
        "lab": task,
        "independent_title": f"Independent record · {focus.capitalize()}",
        "independent": task,
        "independent_checks": [
            ("Trace", facts[0]),
            ("Demand", facts[2]),
            ("Truth", facts[-1]),
        ],
        "safety": SAFE + safety + " A learner may pause, use a private route, observe, or direct an adult without losing the learning entitlement.",
        "routes": routes,
        "exit": exit_text,
        "print_title": f"{focus.capitalize()} working record",
        "print_prompt": f"Use each row to show the supplied evidence or genuine action, the response about {focus}, and one explanation, boundary or authorised next check.",
        "print_topics": print_topics or ["Supplied evidence", "Reasoning or action", "Boundary and next check"],
        "audit_items": audit or ["Source, material or action locator visible", "Reasoning can be checked", "Safety and missing status honest", "Learner's next action received exactly"],
        "support": support,
        "look": look,
    }


def routes(supported, standard, stretch):
    return {"Supported": supported, "Standard": standard, "Stretch": stretch}


EXTRA_PROFILES = {
    "Science_Teesside/Build/W14-W20_2026-27/SCI_B_W14B_Autumn_Science_Evidence_Do.html": profile(
        objective="Select genuine class records about skeletons, nutrition and rocks, organise them by topic, and add a cautious explanation and evidence limit to each.",
        question="Which existing records best show the Autumn science learning, and what does each record actually support?",
        vocabulary=[("SELECT", "choose for a stated reason"), ("CAPTION", "a short statement tied to the record"), ("LIMIT", "what the record cannot establish")],
        facts=["A skeleton record needs a named structure and a supported function.", "A nutrition comparison keeps the same label basis visible.", "A rock record distinguishes appearance from a controlled property test.", "Existing evidence is used honestly; a missing practical is not restaged for a photograph."],
        model="Take one existing skeleton diagram, one supplied nutrition comparison and one rock observation. For each, retain its label or method, write one caption that says only what is shown, and add a limit. Sort them under the correct topic before choosing the strongest record. A neat page does not strengthen weak evidence, and a photograph without the learner's meaning is not enough.",
        task="Assemble a three-topic evidence page from genuine records already available. Include two records per topic where available, a source or method locator, one bounded caption and one limit. Add a short review naming the strongest record and the record that still needs method detail. If any record is unavailable, leave a marked gap and name the responsible next check instead of recreating the task.",
        routes=routes("Match six supplied records to topic headings and complete one caption frame and limit frame per topic.", "Select and justify two records per topic, then write cautious captions and a method-specific limit.", "Evaluate the strength of the selected records, reject one weak item and defend the final evidence set."),
        exit_text="Present one selected record, its caption and its limit. The adult repeats the evidence claim exactly. Confirm or correct it, then retain, relabel or mark the record for an authorised check.",
        focus="an honest Autumn science evidence set", look="The evidence audit makes selection quality visible without restaging any learning event.", safety="Do not repeat body, food, scratch or water activities simply to fill a portfolio gap.", variant=1),

    "Science_Teesside/Build/W14-W20_2026-27/SCI_B_W15A_Fossil_Formation_Story_Explore.html": profile(
        objective="Sequence the main stages by which remains or traces can become fossils over a very long time and distinguish evidence from a compressed story.",
        question="How can a sequence explain fossil formation without pretending every fossil forms in exactly the same way?",
        vocabulary=[("REMAINS", "parts or traces left by a living thing"), ("SEDIMENT", "loose material that can settle in layers"), ("FOSSIL", "preserved remains, impression or trace from long ago")],
        facts=["Rapid burial can reduce disturbance and place remains beneath sediment.", "Soft material usually changes or decays while harder parts, impressions or traces may remain.", "More layers can build and compact over a very long time as minerals and rock processes preserve evidence.", "Later movement or erosion may expose a fossil; Mary Anning used careful observation of real fossils as evidence about life long ago."],
        model="Order five supplied picture cards: living thing or trace; burial by sediment; change while layers build; preserved fossil in rock; later exposure. Use ‘can’ and ‘may’ because the sequence is a model, not a promise for every organism. Mary Anning is named as a public figure connected with careful fossil finding and study, not as a fictional learner or exemplar.",
        task="Build a fossil-formation strip from the supplied cards. Add a short explanation beneath each stage, include ‘over a very long time’, and place one caution card showing that many remains never become fossils. Finish by identifying which stage is inferred from the model and which clue could be observed in a fossil or rock layer.",
        routes=routes("Order five picture cards and match one prepared explanation to each stage.", "Order and explain the stages using burial, sediment, change, preservation and exposure.", "Explain why fossil formation is uncommon and evaluate where the simple sequence has limits."),
        exit_text="Point to one transition in the sequence and explain what changes. The adult repeats the stage without making it certain for every fossil. Confirm, correct or add the caution card.",
        focus="a fossil-formation sequence", look="The may/can language keeps a memorable story scientifically bounded.", safety="Handle only clean classroom specimens, photographs or replicas; no digging or striking rock is required.", variant=2),

    "Science_Teesside/Build/W14-W20_2026-27/SCI_B_W15B_Fossil_Formation_Evidence_Do.html": profile(
        objective="Use supplied fossil and layer evidence to produce a labelled fossil-formation account with an explicit uncertainty statement.",
        question="Which features in the supplied fossil evidence support each part of a formation account?",
        vocabulary=[("IMPRESSION", "a shape or mark preserved in material"), ("LAYER", "material laid down over or under other material"), ("INFERENCE", "an explanation drawn from evidence rather than seen directly")],
        facts=["A visible shape or trace can be described before its cause is inferred.", "Relative layer position can help organise a formation account but does not supply an exact date here.", "A labelled diagram must keep observed features separate from inferred stages.", "Missing provenance or preparation details remain AWAITING AUTHORISED CHECK."],
        model="Describe the supplied image first: outline, texture and layer position. Then label the possible remains or trace, surrounding sediment and later rock layer. Put observed details in one colour and inferred formation stages in another. Add ‘This model suggests…’ and a limit explaining that the image does not reveal every change or an exact date.",
        task="Create a two-column fossil evidence record. On the left, annotate observable details from the approved specimen, replica or image. On the right, connect each usable detail to one stage in a formation sequence. Finish with a concise account and one uncertainty. Do not identify a species, location or age unless the supplied source explicitly provides it.",
        routes=routes("Match observation cards to three labelled stages and choose one uncertainty frame.", "Annotate four observable details and connect them to a sequenced formation account.", "Evaluate which inferences are strongest, reject one unsupported label and explain the model's limitations."),
        exit_text="Read one observation and the inference connected to it. The adult names which part was seen and which was inferred. Correct the classification or retain it with the stated limit.",
        focus="fossil formation evidence", look="Two colours separate what the source shows from the story used to explain it.", safety="Use approved images, replicas or clean specimens; do not chip, scratch or collect material.", variant=3),

    "Science_Teesside/Build/W14-W20_2026-27/SCI_B_W16A_Fossil_Clues_Explore.html": profile(
        objective="Identify observable fossil features and explain one cautious clue each feature can give about living things from long ago.",
        question="What can a fossil clue tell us about a living thing, and what remains unknown?",
        vocabulary=[("FEATURE", "a detail that can be observed"), ("CLUE", "evidence that helps answer a question"), ("UNCERTAINTY", "what cannot yet be decided")],
        facts=["A preserved shape can suggest body form or movement but may be incomplete or distorted.", "A tooth, shell, leaf impression or track has a different evidence job.", "The surrounding rock or layer can add context when its provenance is supplied.", "One fossil rarely represents every member, behaviour or habitat of a living thing."],
        model="Observe one supplied fossil image without naming it first. List visible features, choose one question each feature can help answer, and write a cautious clue sentence. A track may suggest movement direction; it does not show every behaviour. A tooth shape may support a bounded idea about feeding; it does not reconstruct a whole life by itself.",
        task="Audit three supplied fossil sources. For each, record two observable features, one question, one cautious clue and one uncertainty. Sort the clues under body, movement, food or environment only when the evidence supports that category. Finish by rejecting one over-strong claim and rewriting it with evidence language.",
        routes=routes("Match observed features to prepared clue and uncertainty cards.", "Write a feature, clue and uncertainty for three supplied fossil sources.", "Compare the strength of different fossil clues and defend the most useful source for one question."),
        exit_text="Name one visible feature and one clue it supports. The adult asks what remains unknown. Confirm the boundary or revise the claim.",
        focus="fossil clues about life long ago", look="Every clue is paired with an uncertainty so observation does not become a complete reconstruction.", safety="Use only local approved fossil sources; do not handle unknown or sharp specimens.", variant=4,
        extra="Track shape can be described through length, outline and repeated impressions before movement is inferred. A leaf impression may preserve vein pattern while omitting colour and soft tissue. Shell curvature can provide a body-form clue without showing behaviour. Tooth form can support a cautious feeding question without identifying an entire diet. For each fossil clue, write OBSERVED beside the visible feature, POSSIBLE beside the bounded interpretation and UNKNOWN beside the unanswered part. Then test whether the same clue would still answer the question if the specimen were incomplete, compressed or missing its source label."),

    "Science_Teesside/Build/W14-W20_2026-27/SCI_B_W16B_Fossil_Evidence_Do.html": profile(
        objective="Compare fossil clues from two supplied sources and build an evidence-led explanation about living things from long ago.",
        question="How does using more than one fossil clue strengthen or complicate an explanation?",
        vocabulary=[("COMPARE", "identify a relevant similarity and difference"), ("CORROBORATE", "add evidence that supports the same bounded idea"), ("CONTRADICT", "show that an explanation needs revision")],
        facts=["Two fossil sources can address different questions rather than confirming each other.", "A comparison must retain each source label and observable feature.", "Agreement strengthens only the specific claim both sources can address.", "A difference can reveal variation, preservation limits or an unanswered question."],
        model="Place two approved fossil images side by side. Describe each before comparing. Link only features that address the same question, then label the relation as supports, complicates or unrelated. Write one explanation that uses both sources and one sentence stating what neither source can decide.",
        task="Complete a paired fossil evidence sheet. Record the source labels, observable features, one relevant similarity and one difference. Use the comparison to write a bounded explanation about a living thing from long ago. Add an alternative explanation or preservation limit and identify the next source that would be useful.",
        routes=routes("Sort feature cards for two sources and complete a supports/does-not-show frame.", "Compare two fossil sources and write a two-source explanation with one limit.", "Evaluate whether the sources corroborate, complicate or answer different questions, then defend the classification."),
        exit_text="Show the two-source claim and point to the clue from each source. The adult repeats only that claim. Confirm it or move one clue out of the explanation.",
        focus="a two-source fossil explanation", look="The supports/complicates/unrelated labels prevent any second fossil from being treated as automatic confirmation.", safety="Use only approved local images, replicas or clean specimens; no runtime research is required.", variant=5,
        extra="Build a comparison grid with Source A and Source B kept visible in every row. First ask whether both sources address body form, movement, feeding or environment; do not compare clues serving different questions. Next mark agreement only where the observable features genuinely align. Use COMPLICATES when preservation, scale or feature differences require a narrower account. Use UNRELATED when a second source adds interest but no evidence for the chosen question. Finish by writing the two locators beside the claim and one sentence describing what neither fossil source can establish."),

    "Science_Teesside/Build/W14-W20_2026-27/SCI_B_W17A_Soil_Ingredients_Explore.html": profile(
        objective="Recognise rock-derived particles and organic matter as soil ingredients and explain why different soils can contain different mixtures.",
        question="What is soil made from, and how can supplied observations support that explanation?",
        vocabulary=[("MINERAL PARTICLE", "a small rock-derived part of soil"), ("ORGANIC MATTER", "material from once-living things"), ("MIXTURE", "materials together without all becoming one substance")],
        facts=["Soil can include rock-derived mineral particles of different sizes.", "Organic matter comes from once-living material and may appear as dark fragments.", "Air and water occupy spaces between soil particles.", "A classroom sample is one mixture and cannot represent every soil."],
        model="Use a sealed or tray-contained approved soil sample and a close photograph. Separate observation from ingredient label: gritty grains may support rock-derived particles; dark fibrous fragments may support organic matter. Add air and water as possible contents of spaces, not visible objects in every dry photograph. Finish with ‘This sample contains…’ rather than ‘All soil is…’.",
        task="Sort supplied ingredient cards and sample observations into rock-derived particles, organic matter, air/water spaces and not-supported. Build a labelled soil mixture diagram. Explain two observed ingredients and one expected component that would need a different observation or test. Compare two approved samples without ranking them as good or bad.",
        routes=routes("Match visible sample features to ingredient cards and complete two observation frames.", "Build and explain a soil-mixture diagram using evidence from two approved samples.", "Evaluate how particle size and organic matter vary, and explain why one sample cannot define all soils."),
        exit_text="Point to one ingredient and its evidence in the supplied sample. The adult names the observation back. Confirm or move the card to needs another check.",
        focus="soil as a mixture", look="The diagram separates visible ingredients from components that require another observation.", safety="Do not taste or smell soil. Keep samples contained, cover cuts, wash hands and follow the local risk assessment.", variant=6),

    "Science_Teesside/Build/W14-W20_2026-27/SCI_B_W17B_Build_a_Soil_Explanation_Do.html": profile(
        objective="Construct an evidence-led explanation that soils contain rock-derived material and organic matter in varying mixtures.",
        question="How can a labelled sample record become a clear explanation of soil composition?",
        vocabulary=[("COMPOSITION", "the materials that make something up"), ("PROPORTION", "how much of one part compared with another"), ("EVIDENCE LABEL", "a locator joining a statement to an observation")],
        facts=["An explanation begins with recorded sample features rather than a memorised conclusion alone.", "Particle size, colour and visible fragments can support ingredient descriptions with limits.", "Organic matter is not the same as every dark particle, so source and observation matter.", "Comparing two samples can show variation without declaring one universal composition."],
        model="Take three genuine observation labels from a supplied sample record. Arrange them around a soil-mixture diagram, connect each to rock-derived material, organic matter or an unresolved component, and write a because sentence. Add a comparison with a second sample and a limit saying the diagram represents the supplied samples only.",
        task="Produce a soil explanation panel using two approved sample records. Include a labelled mixture diagram, at least three evidence links, one relevant comparison and one limitation. If an ingredient is inferred rather than observed, label it as an inference. Finish by checking that every arrow leads to a real sample detail.",
        routes=routes("Complete a prepared diagram by matching six evidence and ingredient cards.", "Create a labelled two-sample explanation with because sentences and a limit.", "Evaluate ambiguous observations, justify the strongest evidence links and revise one over-certain ingredient claim."),
        exit_text="Trace one arrow from sample observation to ingredient explanation. The adult repeats the because sentence. Confirm, correct or relabel it as inference.",
        focus="an evidence-led soil composition explanation", look="Evidence arrows make every ingredient claim traceable to the supplied sample record.", safety="Keep soil samples contained, avoid dust, wash hands and use the approved local handling route.", variant=7),

    "Science_Teesside/Build/W14-W20_2026-27/SCI_B_W18A_Soil_Drainage_Explore.html": profile(
        objective="Compare how easily water passes through different soils and identify variables that must be controlled for a fair drainage comparison.",
        question="What must stay the same if drainage observations from different soils are to be compared fairly?",
        vocabulary=[("DRAINAGE", "water passing through a material"), ("VARIABLE", "something that can change in a test"), ("FAIR COMPARISON", "change the soil while keeping relevant conditions the same")],
        facts=["The same starting water volume is needed for a useful comparison.", "Equal soil amount, container route and collection time reduce alternative explanations.", "Collected water and passage time answer related but different drainage questions.", "A prediction is not a result; real observations remain blank until a test occurs."],
        model="Compare two fictional drainage plans. Reject the plan that changes both soil amount and water volume. In the fairer plan, label soil type as the changed variable, then list starting volume, soil amount, container, pour route and time as controls. Predict with a reason but leave the result table empty.",
        task="Design a drainage comparison for two or three approved soil samples. Specify the changed variable, controlled conditions, measurement and safe stop. Sequence the method cards, create an empty results table and write a prediction separately. Audit another plan for one hidden variable. Do not pour water unless the practical is authorised and set up by staff.",
        routes=routes("Choose the fair plan from two cards and sort changed, measured and kept-the-same variables.", "Write a sequenced fair-comparison method and an empty results table.", "Evaluate measurement choices, identify a confound and improve the plan while keeping the original question."),
        exit_text="Name the one changed variable and one condition kept the same. The adult repeats the comparison question. Confirm the plan or move it to AWAITING AUTHORISED CHECK.",
        focus="a fair soil drainage comparison", look="The empty result table protects the boundary between designing a test and claiming it happened.", safety="Water practical work occurs only with staff authorisation, stable equipment, spill control and handwashing; no tasting or smelling samples.", variant=8,
        extra="Audit the drainage plan as a chain: sample label, equal soil amount, matched container, equal starting water, agreed pour, fixed collection interval and one reading rule. Circle the single changed condition. Underline the value that will be compared. Put a stop symbol beside overflow, spill or blocked equipment because those events change the method. Create separate spaces for prediction and observation so a plausible expectation cannot enter the result column. State whether collected volume, drainage time or both answer the chosen question, and keep every unit visible."),

    "Science_Teesside/Build/W14-W20_2026-27/SCI_B_W18B_Soil_Water_Test_Do.html": profile(
        objective="Carry out an authorised fair soil-drainage test, record real measurements, and compare how easily water passes through the supplied samples.",
        question="What do the measured drainage results show about these samples under this method?",
        vocabulary=[("MEASURE", "record a value using the agreed unit"), ("REPEAT", "carry out the same method again"), ("ANOMALY", "a result that differs enough to require checking")],
        facts=["Results are entered only after the authorised observation or measurement occurs.", "Starting volume, soil amount, equipment and collection time stay matched.", "Spill or equipment problems are recorded because they can affect the comparison.", "The conclusion is limited to the supplied samples and stated method."],
        model="Demonstrate one dry run with empty equipment, showing where equal soil and starting water would be placed, how time begins and where collected water is read. Model a fictional sample calculation in a clearly labelled example table, then remove it. The live results table stays blank until the class measurement is genuinely received.",
        task="When authorised, complete the soil drainage test using the approved method. Record each sample label, starting volume, collection time, collected amount and any method issue. Repeat only if planned and safe. Compare the real results and write a bounded conclusion. If the practical cannot run, retain the plan and mark the results MISSING; do not substitute model numbers.",
        routes=routes("Direct or complete one safe test role, enter supplied readings and choose the comparison sentence supported by them.", "Carry out the matched method, record results and write a sample-specific conclusion with one limit.", "Evaluate reliability, explain an anomaly or method issue and propose a justified improvement without rewriting the original values."),
        exit_text="State one recorded value and the comparison it supports. The adult reads the table back exactly. Confirm, correct or flag the reading for an authorised repeat.",
        focus="real soil drainage measurements", look="The blank-live-table rule makes it impossible for the modelled values to masquerade as results.", safety="Run only an authorised local risk-assessed water practical. Use stable trays, manage spills promptly, keep soil contained, wash hands and never taste samples.", variant=9),

    "Science_Teesside/Build/W14-W20_2026-27/SCI_B_W19A_Soil_Water_Holding_Explore.html": profile(
        objective="Plan an investigation of which supplied soil holds the most water and design a traceable digital or paper results record.",
        question="How can collected-water measurements be used to infer water held by each soil sample?",
        vocabulary=[("STARTING VOLUME", "water supplied at the beginning"), ("COLLECTED VOLUME", "water that passed through and was measured"), ("WATER HELD", "starting volume minus collected volume under the stated method")],
        facts=["Water held can be calculated only when starting and collected volumes use the same unit.", "Equal soil amount and collection time support a fair comparison.", "A spreadsheet formula can show the calculation but does not create the observation.", "Predicted rankings remain separate from actual measured results."],
        model="Use a fictional worked row labelled MODEL: 50 ml starting and 32 ml collected gives 18 ml held. Show the subtraction and unit, then test the formula with another fictional row. Remove model numbers from the live table. Label columns for sample, starting volume, collected volume, calculated held amount and method note.",
        task="Plan a water-holding investigation for the approved samples. Define the equal conditions, safe method and result columns. Build a paper table or offline spreadsheet with a subtraction formula and test it only with clearly labelled model data. Make a prediction with a reason. Leave live result cells blank until the authorised practical provides measurements.",
        routes=routes("Complete a prepared variable sort and use a calculator with two labelled model rows.", "Design the fair method and build a traceable table or offline formula for water held.", "Evaluate the indirect calculation, identify uncertainty and propose a repeat strategy linked to the question."),
        exit_text="Explain starting minus collected using the model row, then point to the blank live table. The adult confirms that no result exists yet and records the authorised next check.",
        focus="planning a soil water-holding investigation", look="MODEL and LIVE columns stop a spreadsheet formula from being mistaken for experimental evidence.", safety="Any later water test requires staff authorisation, spill control, contained soil and handwashing; this planning lesson creates no live result.", variant=10,
        extra="Design the offline record so every live row carries sample label, equal soil amount, starting volume, collection interval, collected volume and calculated water held. Protect the original observation columns from formula edits. Test subtraction only in a clearly shaded MODEL row, then clear the live measurement cells. Add a unit check that compares millilitres with millilitres. Add a status field for spill, incomplete collection or unavailable repeat. The planned chart title names the supplied samples and method; it does not announce which soil wins before measurements exist."),

    "Science_Teesside/Build/W14-W20_2026-27/SCI_B_W19B_Soil_Data_and_Conclusion_Do.html": profile(
        objective="Use genuine soil water-holding measurements to calculate results, represent them clearly, and write a sample-specific conclusion with limits.",
        question="Which supplied soil held the most water under the class method, and how secure is that conclusion?",
        vocabulary=[("DATA", "recorded observations or measurements"), ("CALCULATE", "work out a value from recorded numbers"), ("CONCLUSION", "a response to the question supported by results")],
        facts=["Every calculated held amount traces to a real starting and collected volume.", "A chart label, unit and sample name are needed for the comparison to be checkable.", "Repeats can reveal variation; they are not silently averaged without showing the values.", "A conclusion applies to the tested samples and method, not all soil everywhere."],
        model="Take one genuine row only after checking its source. Subtract collected volume from starting volume, retain ml, and place the value beside the sample label. Demonstrate how a bar represents that calculated amount. Write ‘Sample __ held the most water in this test’ and add a method or repeat limit. If no live measurements exist, stop at MISSING.",
        task="Audit the class water-holding record, calculate each held amount and check the arithmetic. Create a clear paper or offline digital comparison with units and sample labels. Identify the largest recorded value, write a bounded conclusion and comment on any repeat spread or method issue. Preserve original values; corrections remain visible and explained.",
        routes=routes("Use supplied checked readings and a calculator to complete held-water rows and choose a supported conclusion.", "Calculate, represent and conclude from the real class data with one reliability limit.", "Analyse repeat variation or anomalies, evaluate confidence and justify one method improvement."),
        exit_text="Show the two numbers behind one calculated result and state the bounded conclusion. The adult reads them back exactly. Confirm or flag the row for checking.",
        focus="soil water-holding data and conclusion", look="Every bar traces back to two genuine measurements, so the visual cannot float free of the evidence.", safety="Use only the completed authorised class record in this data lesson; no practical is repeated solely to improve a chart.", variant=11,
        extra="Run a row-by-row data audit before drawing the comparison. Check that starting and collected values share millilitre units, recalculate held water, and preserve the original entry beside any correction. Give each bar the exact sample label and calculated height. If repeats exist, display every reading before choosing a summary. Mark spill, incomplete drainage or timing variation as method notes rather than deleting them. The conclusion names the largest genuine value under this class method, cites the row that supports it and states why tested samples cannot define every soil."),

    "Science_Teesside/Build/W14-W20_2026-27/SCI_B_W20A_Light_and_Dark_Explore.html": profile(
        objective="Recognise that light is needed for seeing and explain darkness as the absence of light reaching the eye from an object.",
        question="Why can an object be present but not visible when no light reaches our eyes from it?",
        vocabulary=[("LIGHT SOURCE", "an object that produces light"), ("REFLECT", "light changes direction from a surface"), ("DARK", "a condition with no or very little light")],
        facts=["Seeing requires light from a source to reach the eye directly or after reflecting from an object.", "Most classroom objects are visible because they reflect light rather than produce it.", "Darkness is not a material covering the object; it is an absence of sufficient light.", "A safer model uses cards, diagrams or a closed viewing box; eyes are never exposed to intense light."],
        model="Use arrow cards to trace source → object → eye. Remove the source arrow and explain why the object may remain present while the viewing information is absent. Sort a lamp under source and a book under reflector. Use ‘dark means little or no light reaches the eye’ without claiming that objects disappear.",
        task="Complete three source-object-eye diagrams using supplied cards. For each, decide whether the object should be visible and explain the route. Audit six classroom item cards as light source, reflector or insufficient information. Design a safe box observation plan with the lid and torch controlled by staff, but do not shine any light at a face.",
        routes=routes("Build two arrow diagrams and match source/reflector labels.", "Explain three visibility cases using source, reflection and eye, then define dark.", "Evaluate an incorrect ‘darkness covers objects’ model and defend a corrected light-path explanation."),
        exit_text="Trace one complete light path or identify the missing link. The adult repeats the route. Confirm it or move the arrow before stating whether the object is visible.",
        focus="light paths and darkness", look="Removing one arrow shows why presence and visibility are different claims.", safety="Never look at the Sun or a bright lamp, never shine a torch into eyes, and use only staff-approved low-intensity classroom equipment.", variant=12),

    "Science_Teesside/Build/W14-W20_2026-27/SCI_B_W20B_Light_Evidence_Do.html": profile(
        objective="Collect safe observations about light and dark, use a source-object-eye model, and produce evidence for the claim that light is needed to see.",
        question="Which safe observation best supports the claim that we need light to see an object?",
        vocabulary=[("OBSERVATION", "what was genuinely noticed under stated conditions"), ("CONDITION", "the setup in which an observation was made"), ("LIGHT PATH", "the route from source to object to eye")],
        facts=["A comparison needs the same object and viewing route with the light condition changed safely.", "Observation wording records visible detail, not a guessed measurement of brightness.", "Opening a controlled light aperture changes the available light without directing it at eyes.", "The conclusion stays tied to the approved setup and does not claim complete darkness if stray light remains."],
        model="Demonstrate the closed viewing-box route with no learner face at the aperture while staff control the safe light opening. Use clearly labelled model observations first, then remove them. When a genuine observation occurs, record the object, light condition and visible detail. Connect the observation to source → object → eye and state the limit if the box was not fully dark.",
        task="Complete the staff-approved light observation or use the supplied genuine class record. Compare the same object under two safe light conditions, record only what was actually visible, and draw the relevant light-path arrows. Write a conclusion about needing light to see and one limitation. If the practical is unavailable, analyse the approved record and mark live observation MISSING.",
        routes=routes("Direct the safe setup, choose matching observation cards and complete a light-path frame.", "Record two genuine conditions, draw paths and write an evidence-linked conclusion.", "Evaluate stray-light or observer limitations and improve the method without overstating darkness."),
        exit_text="State one real observation, show its light-path diagram and give the claim it supports. The adult repeats it exactly. Confirm or revise the limit.",
        focus="safe evidence that light is needed for seeing", look="Condition cards keep model statements and genuine observations visibly separate.", safety="Use staff-approved low-intensity equipment only; never look at the Sun or a bright lamp and never shine light into eyes.", variant=13),

    "Humanities_Teesside/BUILD_W14-W20_2026-27/BUILD_HUM_W15_My_Week_Timeline_and_Caring_Stories.html": profile(
        objective="Sequence a safe learner-chosen or fictional weekly routine and identify one caring action in a supplied story without requiring personal disclosure.",
        question="How does order help explain a week and a caring story?",
        vocabulary=[("SEQUENCE", "events placed in an order"), ("BEFORE", "earlier in the chosen sequence"), ("CARING ACTION", "an action in the supplied story that responds to another person's need")],
        facts=["A weekly timeline can use school events, fictional events or learner-chosen safe events.", "Before, after and next describe order without proving an exact time.", "A caring action is identified from the supplied story rather than a guessed motive.", "Listening can be shown by selecting, pointing, sequencing or responding to a story detail."],
        model="Order three fictional school-week cards, narrate them with before and after, and leave an unknown time unlabeled. Then read the approved caring story extract, identify what one character noticed and the action taken, and distinguish the action from a guess about feelings. No learner is asked to reveal home routines or personal experience.",
        task="Build a four- or five-event timeline using the fictional school week or safe learner-selected events. Use before, after and next accurately. Listen to or read the supplied caring story and add a separate story strip: need noticed, caring action, response shown in the text, and one unanswered question. Keep personal material optional and private.",
        routes=routes("Order prepared week and story cards, then complete two before/after frames.", "Create both sequences and explain the caring action using a story detail.", "Compare how time order and cause are different, and evaluate an unsupported motive statement."),
        exit_text="Read one before/after link and one caring-action detail. The adult repeats only what the timeline and story show. Confirm or correct the order.",
        focus="sequence in a week and a caring story", look="Two separate strips stop a personal timeline from being treated as evidence about a story character.", safety="No disclosure of home routine, belief, family relationship or personal caring experience is required; fictional and school-only routes stay available.", variant=14),

    "Humanities_Teesside/BUILD_W14-W20_2026-27/BUILD_HUM_W16_Then_and_Now_Right_and_Wrong.html": profile(
        objective="Compare observable features of supplied old and new objects and reason about a simple fictional right-and-wrong choice using stated effects.",
        question="What evidence supports a then-and-now comparison, and what makes a choice fair or harmful in the supplied scenario?",
        vocabulary=[("THEN", "the earlier item or time in the supplied source"), ("NOW", "the later item or time in the supplied source"), ("CONSEQUENCE", "what happens because of an action")],
        facts=["Old and new are established by source labels, not by guessing from appearance alone.", "A comparison names one similarity and one relevant difference.", "Right-and-wrong reasoning uses the fictional action, rule, need and consequence.", "A learner can evaluate a scenario without confessing or discussing personal behaviour."],
        model="Compare two labelled classroom-object images. Record one unchanged purpose and one changed material, shape or operation. Then use a fictional scenario in which a shared object is taken without checking. Identify who is affected, the stated rule and a fair repair. Keep historical evidence and moral reasoning in separate columns.",
        task="Complete a then-and-now comparison using two approved labelled sources. Add one supported similarity, one difference and one question. Analyse a supplied fictional choice: action, effect, relevant rule, safer or fairer alternative. Explain the alternative without labelling a person as good or bad and without importing a personal incident.",
        routes=routes("Match labelled old/new sources and choose an effect-and-repair card for one scenario.", "Write a supported object comparison and explain a fair alternative using consequences.", "Evaluate how source limits affect the comparison and compare two defensible responses to the scenario."),
        exit_text="State one evidence-based change and one scenario consequence. The adult names them back separately. Confirm, correct or leave the question open.",
        focus="then-and-now evidence and simple ethical reasoning", look="Separate evidence and consequence columns prevent moral judgement from contaminating the historical comparison.", safety="Use fictional scenarios and approved object sources; no admission, punishment story, belief statement or family practice is requested.", variant=15),

    "Humanities_Teesside/BUILD_W14-W20_2026-27/BUILD_HUM_W17_Picture_Timeline_and_Saying_Sorry.html": profile(
        objective="Order supplied pictures into a simple timeline and recognise what a sincere repair can include in a fictional saying-sorry scenario.",
        question="How do sequence clues establish order, and what makes an apology more than a word?",
        vocabulary=[("TIMELINE", "events arranged in time order"), ("CLUE", "a source detail that helps place an event"), ("REPAIR", "an action that responds to harm or disruption")],
        facts=["Picture order is supported by visible sequence clues and supplied captions.", "A timeline can mark uncertainty when two pictures cannot be ordered.", "A sincere apology can name the action, its effect and an appropriate repair.", "The recipient may need space; an apology does not demand immediate forgiveness."],
        model="Order four fictional classroom pictures by locating start, change and finish clues. Mark one ambiguous pair with a question symbol until a caption resolves it. Then analyse a fictional damaged-material scenario: state what happened, acknowledge the effect, say sorry and offer a realistic repair. Do not require the recipient to accept immediately.",
        task="Construct a picture timeline from an approved set and justify each transition with a visible or caption clue. Record one uncertainty honestly. For a separate fictional scenario, sort apology statements into names action, acknowledges effect, offers repair and pressures recipient. Build a respectful response and identify the next action.",
        routes=routes("Order four pictures and select a complete apology-repair sequence.", "Justify the picture order and write a fictional apology with effect and repair.", "Evaluate an ambiguous timeline and revise an apology that shifts blame or demands forgiveness."),
        exit_text="Point to one ordering clue and one repair element. The adult repeats them without connecting the scenario to the learner. Confirm or revise.",
        focus="picture sequence and respectful repair", look="The uncertainty marker values honest chronology while the repair cards keep apology separate from forced forgiveness.", safety="All scenarios are fictional; no learner must disclose conflict, wrongdoing, harm, belief or family experience.", variant=16),

    "Humanities_Teesside/BUILD_W14-W20_2026-27/BUILD_HUM_W18_Local_Change_and_Community_Care.html": profile(
        objective="Use approved then-and-now local sources to describe one change and identify evidence of how people care in a community.",
        question="What changed in the supplied local sources, and what evidence shows a caring community action?",
        vocabulary=[("LOCAL SOURCE", "approved material about a named place"), ("CHANGE", "a supported difference across time"), ("COMMUNITY CARE", "an action that responds to a shared or individual need")],
        facts=["Then-and-now claims retain source labels and dates when the approved source supplies them.", "One photograph may show appearance but not every cause or consequence of change.", "Community care is identified through a genuine described action, role or service.", "A local example does not prove that every resident had the same experience."],
        model="Place two approved images of the same named local feature side by side. Describe what is visible, identify one supported change and mark cause as unknown unless a source provides it. Then read a separate approved community-care card, identify the need and action, and avoid claiming how everyone felt or benefited.",
        task="Create a local-change panel using two or more approved sources. Record source labels, one continuity, one change and one unanswered cause question. Add a separate community-care case card naming the need, responsible role, action and evidence status. Do not claim a visit, interview or community response unless a genuine authorised record exists.",
        routes=routes("Match then/now sources and select one care action from approved cards.", "Explain continuity and change, then analyse one community-care action with evidence.", "Evaluate source limitations and compare intended care with evidence of what actually occurred."),
        exit_text="Show one supported local change and one caring action from its source. The adult repeats each with its boundary. Confirm or correct.",
        focus="local change and community care", look="Parallel panels preserve the difference between place evidence and evidence of a caring action.", safety="Use rights-cleared local sources only; no home location, community membership, visit, contact or personal service use is requested.", variant=17),

    "Humanities_Teesside/BUILD_W14-W20_2026-27/BUILD_HUM_W19_Questions_About_the_Past_and_a_Kind_Action.html": profile(
        objective="Form a useful question about the past from an approved source and plan one realistic kind action without claiming it has happened.",
        question="What makes a historical question answerable, and what makes a planned kind action specific and honest?",
        vocabulary=[("HISTORICAL QUESTION", "a question about the past that a source might help answer"), ("EVIDENCE NEED", "the material needed to investigate a question"), ("KIND ACTION", "a chosen action intended to help without taking away another person's choice")],
        facts=["A useful question names a person, place, object, event or change and a time context supplied by the source.", "Different questions need photographs, objects, maps, written accounts or other sources.", "Planning a kind action is not evidence that it happened or was welcomed.", "Kindness respects consent, access and the recipient's stated need rather than assuming it."],
        model="Observe one approved past-source card and turn ‘What is this?’ into a focused question about use, change or experience. Name one source type that could help and one limit. Then choose a fictional classroom need, plan a small action, name who authorises it and leave outcome MISSING. Avoid inventing gratitude or success.",
        task="Write or select two historical questions from an approved source, then rank them by how clearly they identify an evidence need. Choose one for a mini source plan. Separately, create a kind-action plan using need, consent/check, action and honest status. Carry out nothing unless the local adult authorises it; record only genuine action and response.",
        routes=routes("Complete a question frame and sort a fictional kind-action plan into need/check/action.", "Form an answerable past question and justify a specific considerate action plan.", "Evaluate two historical questions and examine whether the planned action could unintentionally remove choice."),
        exit_text="State the historical question and the evidence it needs, then name the planned action's next authorised check. The adult does not claim the action occurred.",
        focus="a question about the past and an honest kind-action plan", look="The MISSING outcome box keeps intention from being reported as completed kindness.", safety="Use approved sources and fictional or school-authorised planning; no personal need, past trauma, family story or public helping action is required.", variant=18),

    "Humanities_Teesside/BUILD_W14-W20_2026-27/BUILD_HUM_W20_Then_and_Now_Record_and_Caring_Response.html": profile(
        objective="Create a sourced then-and-now record with photographs or captions and record a caring response only when it is genuinely received or completed.",
        question="How can captions show change accurately while a caring-response record stays truthful about what happened?",
        vocabulary=[("CAPTION", "a concise source-linked description"), ("CONTINUITY", "something that remains similar"), ("RESPONSE STATUS", "PRESENT, MISSING or AWAITING AUTHORISED CHECK")],
        facts=["Every photograph or image keeps its approved source label and time information where supplied.", "A caption distinguishes visible detail from an explanation of change.", "A caring response records the actual choice, action or reply; planning alone stays labelled as planning.", "No reconstructed quotation or staged photograph can fill an empty response field."],
        model="Caption two approved images of the same local object or place. First describe visible detail, then state one supported continuity or change, and leave cause open. On a separate fictional care record, show PLAN, AUTHORISED ACTION and RESPONSE as different boxes. Fill only the boxes backed by a genuine class record.",
        task="Produce a then-and-now page using approved images or source cards, concise captions, one continuity, one change and one source limit. Complete a separate caring-response record from a genuine authorised classroom action if available: learner choice, action, recipient or responsible adult response, and next decision. If no action or response exists, mark it MISSING without staging one.",
        routes=routes("Match captions to two approved images and sort caring-record fields by status.", "Write sourced then-and-now captions and complete an honest response record from available evidence.", "Evaluate how selection shapes the change story and distinguish intended care from evidenced response."),
        exit_text="Read one caption and point to its source, then state the caring record's current status. The adult repeats both without upgrading MISSING to completed.",
        focus="a sourced then-and-now record and caring-response status", look="Side-by-side source captions and a separate status strip prevent a polished page from staging an outcome.", safety="Use rights-cleared sources and authorised records only; no personal address, family history, public posting, recipient quotation or community contact is required.", variant=19),

    "BUILD_ASDAN/Spring1_W1-W3_2026-27/BUILD_ASDAN_W16_Partner_Dish_and_Seasonal_Goals.html": profile(
        objective="Share a defined role in an approved partner task, solve one practical problem, complete or plan an authorised two- or three-step dish safely, and set a realistic seasonal project goal.",
        question="How can two people share a task safely while keeping each contribution, problem-solving decision and next goal honest?",
        vocabulary=[("ROLE", "a defined responsibility in a shared task"), ("PROBLEM-SOLVE", "identify a barrier, test an option and review"), ("SEASONAL GOAL", "a feasible next aim linked to current local conditions")],
        facts=["A shared task records each learner's genuine decision and action separately from adult support.", "A problem-solving record names the barrier, options tried and current status.", "Food preparation occurs only through the approved local allergy, hygiene, equipment and supervision route.", "A seasonal goal is a future plan and never proof that a dish, garden task or project result exists."],
        model="Use a fictional two-person cold-dish brief. Allocate reader/checker and assembler roles, then switch one bounded responsibility. When an ingredient or approval is missing, move the practical to AWAITING AUTHORISED CHECK and solve the planning problem instead of substituting an unknown item. Set a seasonal goal naming action, responsible role and review point without promising an outcome.",
        task="Complete the approved partner challenge. Agree roles, record one turn or handoff, identify a barrier and choose a safe response. If authorised, follow the local two- or three-step dish method and record only real actions; otherwise complete the sequenced plan and approval check. Finish with one seasonal project goal tied to current school conditions, resources and a responsible next check.",
        routes=routes("Choose one partner role, complete or direct a safe step, and select a next-goal card.", "Share roles, document a problem-solving decision and write a feasible seasonal goal with review point.", "Evaluate the collaboration and practical constraints, improve the solution and justify how the goal adapts to local conditions."),
        exit_text="State one genuine partner contribution, the problem-solving decision and the seasonal next action. The adult repeats them without claiming the dish or future goal succeeded.",
        focus="partner work, safe dish steps and seasonal goals", look="Role, problem and future-goal columns keep collaboration evidence separate from an unverified practical outcome.",
        safety="No food is prepared or tasted unless current staff authorisation, allergy information, hygiene controls, safe equipment and supervision are in place. No learner must disclose diet, allergy, body, health, culture or home practice.",
        print_topics=["Partner role and handoff", "Problem and safe response", "Dish action or authorised-plan status", "Seasonal goal and review point"], variant=20),

    "BUILD_ASDAN/Spring1_W1-W3_2026-27/BUILD_ASDAN_W17_Shared_Role_Evaluation_and_Vocational_Plan.html": profile(
        objective="Share and review a role, complete an approved craft or independence challenge, evaluate genuine food evidence where available, and plan a realistic vocational task without qualification claims.",
        question="What genuine evidence supports the review, and which vocational next task is feasible under current school approval?",
        vocabulary=[("TAKE TURNS", "transfer an agreed action or resource"), ("EVALUATE", "judge using stated evidence and criteria"), ("VOCATIONAL TASK", "a practical work-related activity approved in the local setting")],
        facts=["A shared-role record distinguishes the learner's contribution from preparation and prompting.", "The craft or independence challenge is evidenced only by the action genuinely completed.", "Taste is optional and never required; cost and nutrition evaluation use approved labels or genuine records.", "Garden, café or enterprise examples are possibilities, not placements, registrations or completed events."],
        model="Review a fictional shared task with role cards and a genuine-status grid. Identify who decided, who acted and what support was used. Evaluate a supplied dish record using optional sensory evidence, actual supplied cost and approved nutrition information; write MISSING where evidence is unavailable. Choose a local vocational task idea only after naming approval, equipment and first action.",
        task="Complete or review one approved shared-role and craft/independence challenge. Record the learner's turn, action, reason and adult support separately. Evaluate available dish evidence for taste only if freely chosen and genuinely recorded, cost from supplied figures, and nutrition from approved labels. Build a vocational task plan with context, role, first safe action, resources, authorisation and review point. Do not add a unit, level, award or placement claim.",
        routes=routes("Sort genuine evidence into learner action, adult support and missing, then choose a feasible vocational first step.", "Review the shared challenge, evaluate available food evidence and write an authorised vocational task plan.", "Evaluate evidence strength and trade-offs, reject an unsupported completion claim and defend the most feasible vocational route."),
        exit_text="Show one genuine shared-role record, one bounded evaluation and one planned vocational action. The adult names their statuses exactly. Confirm, correct or request an authorised check.",
        focus="shared-role evidence, evaluation and vocational planning", look="The status grid prevents a possible vocational context or optional taste judgement from becoming a fabricated completion claim.",
        safety="Tasting is optional and occurs only under current allergy, hygiene and consent controls. Use approved labels and local materials. No qualification, registration, placement, health or family disclosure is requested or inferred.",
        print_topics=["Shared role and turn", "Craft or independence action", "Taste/cost/nutrition evidence status", "Vocational plan and authorisation"], variant=21),
}
