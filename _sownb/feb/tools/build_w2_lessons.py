#!/usr/bin/env python3
"""Build W2 lessons from the frozen build set, one explicitly selected surface at a time."""
from __future__ import annotations

import argparse
import html as esc
import json
import re
from pathlib import Path

from w2_profiles import EXTRA_PROFILES


ROOT = Path(__file__).resolve().parents[3]
BUILD_SET = ROOT / "_sownb/w2/BUILD_SET.json"
CONTRACT = ROOT / "_sownb/STYLE_CONTRACT.json"


PROFILES = {
    "Science_Teesside/Build/W14-W20_2026-27/SCI_B_W14A_Autumn_Science_Review_Explore.html": {
        "objective": "Organise previously learned observations about skeletons, nutrition and rocks into an evidence map, then identify what each observation can and cannot support.",
        "question": "How can a review map keep three science topics separate while still showing how evidence supports an explanation?",
        "vocabulary": [("OBSERVATION", "what was seen, measured or recorded"), ("EVIDENCE", "an observation used for a stated question"), ("LIMIT", "what the available record cannot establish")],
        "retrieval": [
            "Skeleton work used named parts and models to connect structure with support, protection or movement.",
            "Nutrition work compared labelled information on the same basis before drawing a conclusion.",
            "Rock work described visible properties and used controlled tests for properties that cannot be judged safely by appearance alone.",
            "A record becomes useful evidence only when its source, question and limit remain clear.",
        ],
        "model": "Place each record under one topic heading first. Name exactly what the record shows. Add the question it can help answer, then add one boundary sentence. A labelled skeleton diagram can support a statement about where a bone is and what it protects or supports; it cannot show how every body moves. A same-basis nutrition label comparison can support a cautious comparison between the supplied labels; it cannot judge a person's diet or health. A recorded rock observation or fair-test result can support a claim about the tested specimens under that method; it cannot identify every rock or promise how it will behave in every use.",
        "hinge": "A learner places ‘Sample B allowed less water through in the stated test’ under rocks. Which follow-up keeps the claim honest?",
        "independent": "Build a three-part review map from the supplied class records. For skeletons, nutrition and rocks, select at least two genuine records already available in the pack or lesson folder. For each record, write or select: the observation; the science question; a cautious claim; and a limit. Add one connection arrow only when the link is scientifically meaningful—for example, both a label comparison and a rock test require a fair basis. Finish with a short evidence audit: identify one strong record, one record that needs its method named, and one question that remains open. Add a reader route through the finished map: begin at a labelled record, follow the evidence arrow to its cautious claim, and finish at the boundary statement. Check that a reader cannot accidentally carry a skeleton conclusion into nutrition or a rock result into body evidence. Where two topics use the same reasoning move, label the move rather than merging their scientific conclusions. Existing work may be pointed to, sorted, spoken, signed, typed or exactly scribed. Do not recreate a practical simply to make a photograph, and do not invent a result that is missing.",
        "guided_extension": "Audit a sample reader route before independent work. Begin with a labelled skeleton record and state whether it shows location, structure or function. Move to a nutrition record and name the comparison basis retained from its label. Move again to a rock record and distinguish a visible description from a property established by a controlled test. At each stop, select the exact observation, connect it to one cautious claim and attach a limit. Reject any arrow that joins topics merely because the same everyday word appears. Finish by rehearsing how a reader will find the source or method without asking the learner to recreate an event or practical.",
        "safety": "Use only existing school-approved local records and clean classroom models. Do not repeat scratch, water, food or body-related activities during this review unless they are separately planned, risk assessed and authorised. No diagnosis or medical advice. No personal or family disclosure. Learning does not depend on a runtime connection. A learner may use the supplied fictional examples, pause, observe, direct an adult, or take the printed route.",
        "routes": {
            "Supported": "Sort nine supplied record cards into the three topic headings. Choose one sentence frame per topic: ‘The record shows __. It can support __. It cannot show __.’ An adult may read each card exactly and place it only as directed.",
            "Standard": "Select two records per topic, write a cautious claim for each topic and add a specific evidence limit. Explain one fair-comparison link between nutrition labels and a rock test without mixing their conclusions.",
            "Stretch": "Evaluate the strength of one record from each topic by considering method, comparison basis and uncertainty. Defend one cross-topic connection and reject one tempting connection that the evidence does not support.",
        },
        "exit": "Choose one topic. State the record, the claim it supports and one limit. The receiving adult repeats the science back without upgrading it. Confirm, correct or point to the part that needs changing. Then choose the next honest action: retain the claim, add the missing method detail, or mark the question as still open.",
        "look": "The three-column evidence map keeps review breadth without turning unrelated observations into one claim.",
    },
    "Humanities_Teesside/BUILD_W14-W20_2026-27/BUILD_HUM_W14_Festivals_Display_and_Reflection.html": {
        "kind": "Integrated Humanities and RE",
        "objective": "Use school-approved festival sources to make a clear display panel and a separate reflection page that identifies the source, representation choice and honest response.",
        "question": "How can a festival display inform an audience without presenting one image, object or viewpoint as the whole festival?",
        "vocabulary": [("SOURCE", "the named material used to learn something"), ("REPRESENTATION", "a selected way of showing a subject"), ("REFLECTION", "a considered response that can include a question or limit")],
        "success": ["Every display statement is traceable to a named school-approved source.", "The panel distinguishes sourced information from the learner's design choice or reflection.", "No personal belief, family practice, attendance or community membership is required or inferred."],
        "retrieval": [
            "A source has a maker, form and purpose; these details help the reader understand what the source can contribute.",
            "A display selects and arranges material, so its layout is a representation rather than a complete account.",
            "A reflection can identify what was learned, what remains uncertain and what the maker chose to emphasise without claiming to speak for other people.",
            "A respectful comparison names the supplied evidence and avoids ranking festivals, beliefs or communities.",
        ],
        "arrival_decision": "Choose one supplied source card and locate its source label before discussing its content. If the label is missing, place the card in AWAITING AUTHORISED CHECK rather than guessing its origin.",
        "starter": "Compare a crowded display panel with a panel that uses one sourced statement, one clearly labelled visual and one question. Commit to the panel that an audience can check. Explain which design choice helps the reader separate information from decoration.",
        "checking": ["Who made or selected this source, and for what purpose?", "Which statement is supported directly by the supplied material?", "What part of the panel is the learner's design or reflection?", "What wording avoids treating one example as every person's experience?"],
        "model_title": "Model source-to-panel decisions",
        "model": "Begin with one approved source card. Copy no long passage. Identify one short factual point that the card can establish, then paraphrase it in accessible wording and retain the source label beside it. Choose a visual only when its rights and classroom use are approved; otherwise use a text label, colour-safe symbol or learner-made shape. Add a boundary such as ‘This source gives one account’ or ‘Other practices and experiences may differ.’ On the reflection page, write what the source helped the maker notice, one choice made in the display and one question still open. A reflection is not a reconstructed quotation from a visitor and is not evidence that an event happened.",
        "model_steps": ["Read the maker, date or status and source label first.", "Select one statement the source can actually support.", "Paraphrase briefly and keep the locator beside the panel text.", "Label the learner's design choice or reflection separately.", "Add a limit, difference or open question before publishing the classroom panel."],
        "hinge": "A panel says, ‘This picture proves everybody celebrates in this way.’ Which revision keeps the representation bounded?",
        "hinge_choices": ["Keep the sentence because the picture is colourful.", "Write that the approved source shows one represented example, retain its label and note that experiences can differ.", "Remove the source label so the panel looks simpler."],
        "commit": "Everyone selects or points before the explanation. Justify the revision by naming the source, the over-strong word and the boundary needed. If the response is mixed, contrast ‘one represented example’ with ‘everybody’, then use a fresh panel card.",
        "connection_title": "Connect display craft and reflection",
        "connection_cards": [("Information panel", "A sourced statement helps the audience learn something that can be checked against the approved card."), ("Design decision", "Colour, order, caption size and grouping shape attention; these choices belong to the display maker and must not masquerade as source facts."), ("Reflection page", "The learner can record what was noticed, one respectful choice and one open question without disclosing a personal belief or family practice.")],
        "connection_note": "Keep the three jobs visible: sourced information, display design and learner reflection. A good panel can contain all three, but it labels them so the audience is not misled.",
        "lab_title": "Panel audit lab",
        "lab": "Use three supplied cards: a source-labelled statement, a possible visual or symbol, and a reflection prompt. Build one small panel. Ask a partner or familiar adult to identify which words come from the source and which are the maker's choices. If they cannot tell, revise the labels. Test the panel against three boundaries: no invented quotation, no claim about everybody, and no unsupported statement that a display, visit or celebration took place. Finish by choosing a title that describes the panel rather than advertising a conclusion.",
        "independent_title": "Festival display and reflection page",
        "independent": "Create one classroom display panel using at least two school-approved source items. Give each item a short locator, add a concise paraphrase and state one limit or difference. Use a learner-made layout, colour-safe symbol or approved image route. Then complete a separate reflection page: identify one thing the sources helped you notice, explain one display choice, and record one respectful question or uncertainty. The response may be pointed, selected, signed, spoken, typed or exactly scribed. Do not write a visitor comment, event date, attendance claim, personal belief or family practice unless a real authorised record exists and the learner has chosen to include it through the approved route. ‘No audience response yet’ is an honest status.",
        "independent_checks": [("Source trail", "Every factual panel statement has a visible card or locator; decoration never acts as evidence."), ("Representation", "The layout does not imply that one source represents every festival participant or every practice."), ("Reflection boundary", "The page records the learner's current response or question without forced personal disclosure or adult-authored pupil wording.")],
        "safety": "Use only school-approved local source cards and rights-cleared classroom materials. No diagnosis or medical advice. No personal or family disclosure. No forced disclosure of religion, belief, family practice, attendance, identity or community membership. Learning does not depend on a runtime connection. No open runtime link. No reconstructed quotation, staged audience response, backdated event or invented display outcome. A learner may pause, work privately, use a fictional panel-design route or direct an adult.",
        "routes": {
            "Supported": "Select two approved source cards, match each to a prepared paraphrase and place a SOURCE or MY REFLECTION label. Choose one colour-safe layout and complete: ‘This source shows __. It does not show __.’",
            "Standard": "Paraphrase two approved sources, build a balanced panel with visible locators and write a reflection that explains one representation choice and one remaining question.",
            "Stretch": "Evaluate how selection and layout shape the audience's understanding, compare what two sources can establish, and revise an over-general statement while preserving respectful uncertainty.",
        },
        "exit": "Point to or read one panel statement and its source label. Explain whether it is sourced information, a design decision or reflection. The adult names that category back exactly. Confirm or correct it, then choose one influence action: keep the panel, improve a label, remove an unsupported statement, or leave a question visibly open.",
        "print_title": "Display and reflection planning record",
        "print_prompt": "Use the source column for a locator and bounded paraphrase, the action column for the planned panel choice, and the final column for reflection or limitation. Nothing on the sheet proves an event or audience response occurred.",
        "print_topics": ["Approved source 1", "Approved source 2", "Display choice"],
        "audit_items": ["Source labels and rights route checked", "Information and maker choice visibly separated", "Reflection contains no forced personal disclosure", "Audience response marked honestly as present or not yet received"],
        "support": [
            "Before the overview, reduce visual density and preview the three labels SOURCE, DESIGN and REFLECTION. The learner may use a private response and does not need to discuss personal belief. Keep the full Humanities demand available through pointing, sorting or exact reading.",
            "At arrival, let the learner inspect the source label before any content discussion. An adult can read the maker and status exactly, then wait. If provenance is absent, moving the card to CHECK is a successful disciplinary decision rather than a failure to participate.",
            "During the starter, protect the first choice and ask what makes the panel checkable. Use a visual cue to compare label placement, not a verbal prompt that supplies the answer. A retry uses a different panel so the reasoning transfers.",
            "While modelling, the teacher owns the explanation and makes every selection decision visible. Staff point to the source, paraphrase and boundary in sequence, then fade. The learner watches, tracks or directs without being asked to disclose a personal connection.",
            "At the hinge, every learner commits through an available mode. Receive the chosen revision before asking why. If language is the barrier, preserve the contrast between one represented example and everybody using two printed cards.",
            "For the second model, keep information, design and reflection as separate movable cards. The learner decides where each belongs. An adult may stabilise materials but does not rewrite a reflection into more polished learner wording.",
            "In the panel audit, use one small layout at a time. The audience role identifies what can be checked and returns one precise ambiguity. Influence means the learner chooses the revision, including declining a suggested decorative addition.",
            "During independent work, offer a prepared source tray, plain layout grid and private reflection route. Reduce quantity before lowering the reasoning demand. Record adult cutting, printing or exact scribing separately from the learner's source and design decisions.",
            "At exit, a familiar adult receives one labelled choice completely and names it back without praise inflation. The learner confirms, corrects or leaves the question open. The selected revision is the only action recorded; no display launch is staged.",
        ],
        "look": "The visible SOURCE / DESIGN / REFLECTION separation prevents a polished panel from blurring evidence and personal response.",
    },
    "BUILD_ASDAN/Spring1_W1-W3_2026-27/BUILD_ASDAN_W15_Choice_Budget_and_Project_Reset.html": {
        "kind": "Cross-strand teaching surface",
        "objective": "Make and justify one choice, check a simple fictional budget, plan a balanced meal from approved options, and use the completed checks to refresh one realistic class-project focus.",
        "question": "Which plan fits the stated needs and budget, and how should that decision change the next class-project step?",
        "vocabulary": [("CHOICE", "one selected option with a reason"), ("BUDGET", "the amount available and the costs checked against it"), ("BALANCE", "planned variety using the approved classroom food-pattern guide")],
        "success": ["The chosen option is linked to a stated need rather than a guessed personal preference.", "Every supplied cost is included and the total is checked against the fictional budget.", "The refreshed project focus names one feasible next action without claiming that food was prepared, bought or delivered."],
        "retrieval": [
            "A useful choice names the options, the stated need and a reason that can be checked.",
            "A budget record keeps the available amount, each supplied cost and the remaining or short amount visible.",
            "A meal plan can be discussed through fictional or class options; nobody has to disclose diet, allergy, body, health, culture or family finances.",
            "A project focus is a next teaching action. It is not evidence that a service, purchase, meal or community outcome has already happened.",
        ],
        "arrival_decision": "Choose the fictional brief card, cost card and project-status card that belong together. If a cost or approval is absent, place the plan in AWAITING AUTHORISED CHECK rather than estimating it.",
        "starter": "A fictional class has £2.00 for one snack plan. The supplied cards show a sandwich at £1.20, fruit at £0.50 and water at £0.30. Commit to whether the set is within budget, then show the calculation and one reason the plan matches the stated brief. This is a number-and-choice model, not a purchase or diet recommendation.",
        "checking": ["What amount is available in the fictional brief?", "Have all supplied costs been included exactly once?", "Which approved option adds variety without judging anybody's eating?", "What project action is feasible now, and what still needs an authorised check?"],
        "model_title": "Model choice, total and project handoff",
        "model": "Read the fictional brief first: choose a simple varied snack plan within £2.00 using the supplied school-approved options. List £1.20, £0.50 and £0.30 in separate rows. Add them to get £2.00, compare total with amount available and write ‘within budget; £0.00 remaining.’ Give a reason tied to the brief, not to a real learner's body, health or home. Move the result into the project-reset board: PRESENT—one costed plan; MISSING—local approval to use any option; NEXT—responsible adult checks the current approved list before a practical session is planned. The model never claims ingredients were bought, food was prepared or an audience agreed.",
        "model_steps": ["Read the fictional need, amount and approved option cards.", "Record every supplied cost once and calculate the total.", "Compare total with amount available and show the difference.", "Explain the choice using the brief and classroom balance guide.", "Transfer only the genuine planning result to PRESENT, MISSING and NEXT project status."],
        "hinge": "The total is exactly £2.00. Which record is honest and useful for the class-project reset?",
        "hinge_choices": ["The plan is within the fictional budget with nothing remaining; practical approval is still awaiting the responsible adult.", "The class bought the food and everyone liked it.", "The plan is over budget because three items always cost too much."],
        "commit": "Everyone shows the total and selects the honest project status before explanation. A calculator, number line, coin cards, pointing, signing, typing or exact scribing are equivalent routes. Retry with a new supplied amount rather than copying the model wording.",
        "connection_title": "Connect budgeting to a realistic project reset",
        "connection_cards": [("Costed choice", "The arithmetic can establish whether the fictional plan fits the stated amount; it cannot establish approval, purchase or outcome."), ("Balanced plan", "The school-approved guide supports variety in the fictional plan without ranking foods, bodies, families or cultures."), ("Project focus", "The class can choose a next planning action and responsible role while leaving real approvals, prices and practical arrangements unchecked until authorised.")],
        "connection_note": "Move only what the completed planning record supports. ‘Within the fictional budget’ can move to PRESENT; ‘ingredients are available’ stays MISSING until checked through the local process.",
        "lab_title": "Budget-and-focus decision lab",
        "lab": "Use two new fictional briefs. For each, sort the need, amount, option costs and approval-status cards. Calculate the total, compare it with the available amount and choose one plan with a reason. Then place the plan on a project-reset strip under PRESENT, MISSING or NEXT. A partner or familiar adult audits one arithmetic step and one truth boundary. If a supplied cost is missing, the correct response is AWAITING AUTHORISED CHECK. Finish by choosing which one planning action the class could genuinely take next: compare approved options, ask the named responsible adult, revise the fictional budget, or pause the plan.",
        "independent_title": "Choice, budget, meal-plan and project-reset record",
        "independent": "Complete one four-part record using the supplied fictional classroom brief. First, select between at least two options and state a reason tied to the stated need. Second, list each supplied cost, calculate the total and show whether it is within the available amount. Third, assemble a balanced meal or snack plan from the school-approved picture/text cards and explain how it meets the class guide without personal diet or health judgement. Fourth, refresh the project focus using PRESENT, MISSING and NEXT: record the genuine plan, identify one approval or information gap, and name one responsible next action. The learner may point, sort, say, sign, type, use a communication aid or direct an adult. No purchase, preparation, taste result, audience response, date or quotation is invented.",
        "independent_checks": [("Maths trail", "Every supplied cost appears once; total and difference are visible so another person can check the arithmetic."), ("Choice and access", "The reason belongs to the fictional brief, and a learner can use a non-disclosure route without losing the planning demand."), ("Project truth", "Only the completed planning action is PRESENT; approval, purchase, preparation and community response remain MISSING until real authorised records exist.")],
        "safety": "Planning only. Use fictional or class options and current school-approved local materials. No diagnosis or medical advice. No food is prepared, tasted, purchased or served in this lesson. No personal or family disclosure. Do not ask about diet, allergy, body, health, culture or finances. Learning does not depend on a runtime connection. No open runtime link. Never invent a price, approval, result, date, quotation, purchase, audience or community outcome. A learner may pause, choose a private route or direct an adult.",
        "routes": {
            "Supported": "Choose between two fictional plans, match supplied cost cards, use a calculator or coin line to total them, and complete ‘I chose __ because the brief says __.’ Sort project status into PRESENT, MISSING and NEXT.",
            "Standard": "Compare at least two fictional plans, calculate total and difference, justify a balanced choice from approved cards, and write a feasible project-reset action with responsible role and unchecked approval named.",
            "Stretch": "Evaluate trade-offs between cost, stated need, variety and feasibility; test how one changed cost affects the plan; and defend a project focus that separates completed planning from unverified practical assumptions.",
        },
        "exit": "Show the chosen plan, total and one project status. The adult repeats the arithmetic and reason exactly without turning planning into a completed event. Confirm or correct it, then choose one influence action: retain the plan, revise a costed option, request an authorised check, or pause the project focus.",
        "print_title": "Choice, budget and project-reset record",
        "print_prompt": "Complete the four rows from the supplied fictional brief. Record real classroom status honestly; this page does not prove a purchase, practical task, approval or outcome.",
        "print_topics": ["Choice and reason", "Budget total and difference", "Balanced plan from approved cards", "Project PRESENT / MISSING / NEXT"],
        "audit_items": ["All supplied costs recorded exactly once", "No personal diet, health or family-finance disclosure", "Planning separated from practical approval and outcome", "Learner's chosen next action received exactly"],
        "support": [
            "At overview, preview the four-part record with icons for choose, total, plan and next. Use fictional examples so no learner has to reveal food, health or money information. Keep the whole planning entitlement available through sorting or adult-directed access.",
            "During arrival, offer only the brief, cost and status cards needed for the first sort. Read numbers exactly and wait. Moving an incomplete plan to AWAITING AUTHORISED CHECK is a correct decision, not an error to be hidden.",
            "At the starter, allow calculator, coin line, written addition or adult-operated input directed by the learner. Receive the within-budget decision before asking for a reason. Do not turn the fictional calculation into advice about a real purchase.",
            "While modelling, point to each cost as it is copied and make the comparison step visible. Separate teacher demonstration from learner work. The model's final handoff names what remains unapproved so polished arithmetic cannot imply a completed practical.",
            "At the hinge, every learner commits to one status. Use three printed response cards if language or motor access is the barrier. The adult asks which words are supported by the calculation and removes any claim about buying or liking food.",
            "For the connection, keep costed choice, classroom balance guide and project status on three separate mats. The learner directs any movement between them. Staff may stabilise cards but do not supply a personal preference or project decision.",
            "In the lab, change one fictional value at a time and preserve the rest of the brief. A partner audits rather than corrects silently. Influence belongs to the learner's next-action choice, including asking for a check or pausing.",
            "During independent work, chunk the four sections and offer a quiet route. Record calculator use, exact scribing and adult handling separately. The learner still selects, calculates or directs, justifies and chooses the project status.",
            "At exit, receive the plan and status privately if preferred. Name back only the supplied amount, calculated total, reason and next action. No praise inflation, completion claim or future promise is added to the record.",
        ],
        "look": "The PRESENT / MISSING / NEXT project strip prevents a correct fictional budget from being mistaken for a completed or approved practical outcome.",
    },
}

PROFILES.update(EXTRA_PROFILES)


FAMILY = {
    "BUILD Science": {
        "tokens": "--grow:#4E7A9B;--navy:#10233f;--text:#1f2937;--muted:#64748b;--bg:#f5f8fa;--lo:#e7d8e9;--purple:#7c3aed;--pink:#db2777;--amber:#eab308;--blue:#3b82f6;--green:#16a34a;--softblue:#e9f4fb;--softamber:#fff7d6;--softgreen:#eaf8ef;--line:#d8e0e8",
        "accent": "var(--grow)", "ink": "var(--navy)", "surface": "#fff", "page": "var(--bg)", "muted": "var(--muted)",
        "home": "../../../index.html", "ladder": "Supported / Standard / Stretch",
        "controls": ["🧑‍🏫 TA Brief", "🔁 Live Loop", "ⓘ Guidance", "🔤 Word help", "☁ Calm view", "⏸ Teacher Freeze"],
        "structures": '<div class="chips"><span>BUILD Science</span><span>40 minutes</span><span>offline</span></div><div class="hero-visual" aria-label="Focus, evidence, limit diagram"><b>FOCUS</b><span>→</span><b>EVIDENCE</b><span>→</span><b>LIMIT</b></div><div class="evidence-gate">Evidence gate: record → question → cautious claim → limit.</div><div class="ladder">wait · self-prompt · visual cue · general verbal · specific verbal · model · direct support · fade</div><div class="ta-card" data-mbm-guide="staff">Staff card: preserve the learning goal; change modality before changing demand.</div><div class="modal" data-mbm-guide="staff">Modal guidance carrier.</div>',
        "route_classes": {"Supported": "s", "Standard": "m", "Stretch": "h"},
        "print_class": "proute",
        "domain": "Science", "soft": "var(--softblue)", "warn": "var(--softamber)",
        "route_colors": ("var(--green)", "var(--blue)", "var(--purple)"), "route_base": "route",
    },
    "BUILD Humanities": {
        "tokens": "--ink:#18233F;--steel:#4F869C;--steel-dark:#356478;--rust:#D06438;--rust-dark:#A94722;--teal:#16877A;--teal-dark:#0E685F;--gold:#E1AB32;--cream:#FAF7EF;--line:#CBD5E1;--muted:#526173;--green:#286E54;--paper:#fffdf8;--focus:#18233F",
        "accent": "var(--steel)", "ink": "var(--ink)", "surface": "var(--paper)", "page": "var(--cream)", "muted": "var(--muted)",
        "home": "../../index.html", "ladder": "Supported / Standard / Stretch",
        "controls": ["🧑‍🏫 TA", "🔎 Read response", "☰ Staff &amp; print", "Calm mode", "◀ Previous", "Next ▶"],
        "structures": '<div class="chips"><span>BUILD Humanities</span><span>40 minutes</span><span>offline sources</span></div><div class="hero-visual" aria-label="Source, account and reflection diagram"><b>SOURCE</b><span>→</span><b>ACCOUNT</b><span>→</span><b>REFLECTION</b></div><div class="drawer" data-mbm-guide="staff">Staff and source drawer: provenance, access route and limitations stay visible to adults.</div><div class="ladder">BUILD entry · place, read, select or state with support · BUILD secure · compare, explain or reflect · GROW reach · evaluate or connect</div><div class="ta-card" data-mbm-guide="staff">Staff card: preserve disciplinary thinking and never require personal belief or family disclosure.</div>',
        "route_classes": {"Supported": "supported", "Standard": "standard", "Stretch": "stretch"},
        "print_class": "proute", "domain": "Humanities", "soft": "var(--cream)", "warn": "#FFF4D6",
        "route_colors": ("var(--green)", "var(--teal)", "var(--rust)"), "route_base": "route",
    },
    "BUILD ASDAN": {
        "tokens": "--ink:#17223B;--paper:#FFFCF5;--soft:#F3F6F8;--line:#CAD5DF;--muted:#526274;--gold:#B57918;--green:#246B55;--slot:#346B7B;--slot-pale:#EAF6F8;--danger:#8A3C2D",
        "accent": "var(--slot)", "ink": "var(--ink)", "surface": "var(--paper)", "page": "var(--soft)", "muted": "var(--muted)",
        "home": "../../index.html", "ladder": "Supported / Standard / Stretch",
        "controls": ["Teacher tools", "Evidence & print", "Calm mode", "Static diagrams", "Previous", "Next"],
        "structures": '<div class="chips"><span>BUILD ASDAN</span><span>40 minutes</span><span>offline</span></div><div class="lundy-strip"><b>SPACE</b><b>VOICE</b><b>AUDIENCE</b><b>INFLUENCE</b></div><div class="prompt-ladder">wait · self-prompt · point / visual · general verbal · specific verbal · model · direct support · fade</div><div class="evidence-gate">Evidence gate: genuine action, pupil meaning, adult support recorded separately, honest status.</div><dialog><p>Teacher tools and approved evidence route.</p></dialog>',
        "route_classes": {"Supported": "supported", "Standard": "standard", "Stretch": "stretch"},
        "print_class": "print-route", "domain": "ASDAN", "soft": "var(--slot-pale)", "warn": "#FFF3D4",
        "route_colors": ("var(--green)", "var(--slot)", "var(--gold)"), "route_base": "route-card",
    },
}


def contract_value(row_id: str) -> str:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    return next(row["value"] for row in contract["rows"] if row["id"] == row_id)


def words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*", text))


def long_support(topic: str, stage: str) -> str:
    return (
        f"At the {stage} stage, keep the current science question visible and use the lightest access route that still lets the learner decide. "
        f"Pointing, selecting, signing, speaking, typing and exact-word scribing are equivalent response routes for {topic}. "
        "A familiar adult may read the displayed wording exactly, but the adult does not supply a pupil decision or turn a partial observation into a stronger claim. "
        "If regulation or access is the barrier, pause, reduce visual density, offer the printed route or let the learner direct an adult. "
        "Nothing is scored, uploaded or saved by this page, and a retry is information rather than a penalty."
    )


def lundy(note: str) -> str:
    return (
        '<div class="lundy" aria-label="Lundy participation strip">'
        '<div class="lundy-grid"><span>SPACE</span><span>VOICE</span><span>AUDIENCE</span><span>INFLUENCE</span></div>'
        f'<p>{esc.escape(note)}</p></div>'
    )


def route_cards(profile: dict, cfg: dict) -> str:
    cards = []
    for label in ("Supported", "Standard", "Stretch"):
        icon = {"Supported": "◆", "Standard": "▲", "Stretch": "★"}[label]
        cls = cfg["route_classes"][label]
        cards.append(f'<article class="{cfg.get("route_base","route")} {cls}"><h3>{icon} {label}</h3><p>{esc.escape(profile["routes"][label])}</p></article>')
    return '<div class="routes">' + "".join(cards) + "</div>"


def slide(index: int, kind: str, title: str, minutes: int, body: str, topic: str, support: str | None = None) -> str:
    active = " active" if index == 0 else ""
    return (
        f'<section class="slide{active}" data-type="{kind}" data-title="{esc.escape(title)}" data-min="{minutes}" '
        f'data-ta1="Wait, receive and use the least prompt needed." data-ta2="Keep adult action separate from pupil authorship.">'
        f'<div class="time">{minutes} min</div><span class="tag">{esc.escape(title)}</span>{body}'
        f'<p class="access" data-mbm-guide="staff">{esc.escape(support or long_support(topic, title))}</p>'
        f'{lundy("SPACE stays available. VOICE is received. AUDIENCE names back exactly. INFLUENCE changes one real next action.")}'
        '</section>'
    )


def build_lesson(item: dict, profile: dict) -> str:
    cfg = FAMILY[item["family"]]
    splash = contract_value("shared.splash.byte-block")
    guide = contract_value("shared.guide.byte-block")
    confirm = contract_value("shared.confirmation.byte-block")
    outcome = " · ".join(item["outcomes"])
    cells = " · ".join(item["cells"])
    title = item["title"]
    kind = profile.get("kind", "Explore" if item["slot"] == "A" else "Do")
    success = profile.get("success", ["Records stay attached to the topic and question they address.", "A claim says no more than the available observation supports.", "At least one limit or honest missing item remains visible."])
    checking = profile.get("checking", ["What can be read directly from the record?", "Which words are interpretation rather than observation?", "What method or comparison basis must be named?", "What would be unsafe or dishonest to infer?"])
    hinge_choices = profile.get("hinge_choices", ["It proves every example behaves the same.", "It supports a bounded response about the supplied record, with limits.", "It should be moved to another topic because one word is shared."])
    connection_cards = profile.get("connection_cards", [("Same reasoning move", "Connect only records that share a named reasoning move."), ("Different evidence job", "Keep each source attached to the question it can address."), ("Honest absence", "Use MISSING or AWAITING AUTHORISED CHECK rather than filling a gap.")])
    supports = profile.get("support", [])
    slides = []
    overview = (
        f'<div class="hero"><div><p class="brandline">BUILD · {cfg["domain"]} · Week {item["week"]}{item["slot"]} · {kind}</p>'
        f'<h1>{esc.escape(title)}</h1><p class="sowline" data-mbm-guide="route"><b>Verbatim workbook outcome:</b> {esc.escape(outcome)} · <b>Trace:</b> {esc.escape(cells)}</p>'
        f'<div class="box lo"><b>Objective:</b> {esc.escape(profile["objective"])}</div>'
        '<div class="box"><b>Success evidence:</b><ul>' + ''.join(f'<li>{esc.escape(value)}</li>' for value in success) + '</ul></div>'
        f'{cfg["structures"]}</div></div>{route_cards(profile,cfg)}'
        f'<p class="truth"><b>Truth boundary:</b> never backdate, never reconstruct a quotation, never stage an event, and never convert adult wording into the learner’s voice. {esc.escape(profile["safety"])}</p>'
    )
    slides.append(slide(0, "title", "Lesson overview", 0, overview, title, supports[0] if len(supports)>0 else None))
    retrieval = '<h2>Retrieve without guessing</h2><div class="grid">' + "".join(f'<div class="box"><p>{esc.escape(x)}</p></div>' for x in profile["retrieval"]) + f'</div><p><b>Arrival decision:</b> {esc.escape(profile.get("arrival_decision", "Choose one available record and identify what it shows. If it is unavailable, mark it MISSING rather than recreating it."))}</p>'
    slides.append(slide(1, "arrival", "Arrival · retrieve", 3, retrieval, title, supports[1] if len(supports)>1 else None))
    starter = f'<h2>{esc.escape(profile["question"])}</h2><div class="hero-visual"><div>1 · notice</div><div>2 · choose</div><div>3 · explain</div></div><p>{esc.escape(profile.get("starter", "Commit before explanation. Use the supplied record, compare the available options and keep any first prediction open to revision."))}</p><div class="box"><b>Checking questions:</b><ul>{"".join(f"<li>{esc.escape(value)}</li>" for value in checking)}</ul></div>'
    slides.append(slide(2, "starter", "Starter · create the need", 3, starter, title, supports[2] if len(supports)>2 else None))
    vocab = ''.join(f'<div class="vterm"><strong>{esc.escape(k)}</strong><span>{esc.escape(v)}</span></div>' for k,v in profile["vocabulary"])
    vocab_extension = ''.join(f'<li>{esc.escape(value)}</li>' for value in profile.get("vocabulary_extension", []))
    model_steps = profile.get("model_steps", ["Read the supplied record without improving it.", "Name the task or question it addresses.", "Make one bounded response.", "Add a limit or checking point.", "Check that no missing detail has been silently supplied."])
    ido = f'<h2>{esc.escape(profile.get("model_title","Model the thinking"))}</h2><div class="vocabrow">{vocab}</div>{f"<div class=\"box\"><h3>Vocabulary in use</h3><ul>{vocab_extension}</ul></div>" if vocab_extension else ""}<div class="box model"><p>{esc.escape(profile["model"])}</p></div><ol>{"".join(f"<li>{esc.escape(value)}</li>" for value in model_steps)}</ol><p data-mbm-guide="staff">Staff-only guidance: model one complete route, remove the model, and receive a fresh learner decision.</p>'
    slides.append(slide(3, "ido", "I Do · model", 4, ido, title, supports[3] if len(supports)>3 else None))
    wedo = f'<h2>{esc.escape(profile["hinge"])}</h2><div class="options">{"".join(f"<button type=\"button\">{esc.escape(value)}</button>" for value in hinge_choices)}</div><p>{esc.escape(profile.get("commit", "Everyone commits through pointing, selecting, saying, signing, typing or directing an adult. Compare the bounded and over-strong responses, then answer a fresh example."))}</p><div class="evidence-gate"><b>Audience check:</b> the adult names back exactly what was received. The learner confirms or corrects before the class moves on.</div>'
    slides.append(slide(4, "wedo", "We Do · everyone commits", 3, wedo, title, supports[4] if len(supports)>4 else None))
    guided_extension = profile.get("guided_extension", "")
    ido2 = f'<h2>{esc.escape(profile.get("connection_title","Connect the second idea"))}</h2><div class="grid">{"".join(f"<div class=\"box\"><h3>{esc.escape(head)}</h3><p>{esc.escape(text)}</p></div>" for head,text in connection_cards)}</div><p>{esc.escape(profile.get("connection_note", "Name the connection explicitly. Remove any link that cannot be explained from the supplied material."))}</p>{f"<div class=\"box\"><p>{esc.escape(guided_extension)}</p></div>" if guided_extension else ""}'
    slides.append(slide(5, "ido2", "I Do 2 · connect", 3, ido2, title, supports[5] if len(supports)>5 else None))
    routes = route_cards(profile,cfg)
    wedo2 = f'<h2>{esc.escape(profile.get("lab_title","Decision lab"))}</h2>{routes}<div class="box"><p>{esc.escape(profile.get("lab", profile["independent"]))}</p></div>'
    slides.append(slide(6, "wedo2", "We Do 2 · lab", 4, wedo2, title, supports[6] if len(supports)>6 else None))
    independent_checks = profile.get("independent_checks", [("Trace", "Keep the source, material or action locator visible."), ("Demand", "Supported, Standard and Stretch change the task demand rather than merely softening a verb."), ("Truth", "Use PRESENT, MISSING or AWAITING AUTHORISED CHECK; never stage a record.")])
    independent = f'<h2>{esc.escape(profile.get("independent_title","Independent evidence"))}</h2><div class="box task"><p>{esc.escape(profile["independent"])}</p></div>{routes}<div class="grid">{"".join(f"<div class=\"box\"><h3>{esc.escape(head)}</h3><p>{esc.escape(text)}</p></div>" for head,text in independent_checks)}</div><p><b>Exit route remains available:</b> pause, use the print pack, reduce visual density or direct an adult. The named learning demand remains available.</p>'
    slides.append(slide(7, "independent", "Independent · evidence", 16, independent, title, supports[7] if len(supports)>7 else None))
    exit_body = f'<h2>Audience receives; Influence changes one next action</h2><div class="box"><p>{esc.escape(profile["exit"])}</p></div><div class="lundy-status"><p><b>SPACE:</b> the learner may pause or choose a private response.</p><p><b>VOICE:</b> the evidence statement remains in the learner’s chosen communication mode.</p><p><b>AUDIENCE:</b> a familiar adult receives and names back exactly what was heard or seen.</p><p><b>INFLUENCE:</b> one real next action is recorded: retain, add method detail, or leave open.</p></div><p><b>Final check:</b> no result, quote, date, event or pupil wording has been created to make the map look complete. The HTML stores no learner response.</p>'
    slides.append(slide(8, "exit", "Exit · Audience and Influence", 4, exit_body, title, supports[8] if len(supports)>8 else None))

    styles = f'''<style>
:root{{{cfg["tokens"]}}}
*{{box-sizing:border-box}}html,body{{margin:0;min-height:100%;font-family:"Segoe UI",Arial,sans-serif;color:{cfg["ink"]};background:{cfg["page"]}}}
body{{overflow:hidden}}a,button{{font:inherit}}button,a.mbmhome{{min-height:44px;min-width:44px}}
.skip{{position:absolute;left:-9999px}}.skip:focus{{left:8px;top:8px;z-index:50;background:#fff;padding:10px}}
.deck{{height:100vh;padding:18px 18px 112px;overflow:auto}}.slide{{display:none;max-width:1120px;min-height:calc(100vh - 145px);margin:auto;background:{cfg["surface"]};border:2px solid var(--line);border-top:10px solid {cfg["accent"]};border-radius:18px;padding:22px;box-shadow:0 8px 30px #10233f18}}.slide.active{{display:block}}
h1{{font-size:clamp(2rem,5vw,3.6rem);line-height:1.04;margin:.35rem 0}}h2{{font-size:clamp(1.5rem,3vw,2.3rem);margin:.4rem 0 1rem}}h3{{margin:.2rem 0 .45rem}}p,li{{line-height:1.5}}.tag,.time,.chips span{{display:inline-block;border-radius:999px;padding:6px 10px;font-weight:800}}.tag{{background:{cfg["soft"]}}}.time{{float:right;background:{cfg["ink"]};color:#fff}}.chips{{display:flex;gap:7px;flex-wrap:wrap;margin:12px 0}}.chips span{{background:{cfg["warn"]}}}
.hero{{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(260px,.7fr);gap:18px}}.hero-visual{{display:grid;gap:10px;align-content:center;background:{cfg["ink"]};color:#fff;border-radius:16px;padding:18px;min-height:150px;text-align:center}}.hero-visual span{{color:{cfg["accent"]}}}
.box,.route,.route-card,.evidence-gate,.lundy,.lundy-strip,.ladder,.prompt-ladder,.ta-card,.modal,.drawer,dialog{{border:2px solid var(--line);border-radius:13px;padding:13px;margin:12px 0;background:#fff}}.lo{{border-left:8px solid {cfg["accent"]}}}.truth{{border-left:8px solid {cfg["route_colors"][2]};background:{cfg["warn"]};padding:12px}}.access{{background:{cfg["soft"]};padding:12px;border-radius:12px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}}.routes{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}}.route.s,.route.supported,.route-card.supported{{border-top:7px solid {cfg["route_colors"][0]}}}.route.m,.route.standard,.route-card.standard{{border-top:7px solid {cfg["route_colors"][1]}}}.route.h,.route.stretch,.route-card.stretch{{border-top:7px solid {cfg["route_colors"][2]}}}.options{{display:grid;gap:9px}}.options button{{text-align:left;padding:12px;border:2px solid var(--line);border-radius:10px;background:#fff}}.vocabrow{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}}.vterm{{border:2px solid var(--line);padding:12px;border-radius:12px}}.vterm span{{display:block;margin-top:5px}}.lundy-grid,.lundy-strip{{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;text-align:center;font-weight:900}}.ladder,.prompt-ladder{{font-weight:700}}.ta-card,.modal,.drawer{{background:{cfg["warn"]}}}
.controls{{position:fixed;left:8px;right:8px;bottom:58px;z-index:20;display:flex;gap:7px;overflow-x:auto;padding:8px;background:{cfg["ink"]};border-radius:14px}}.controls button,.controls a{{flex:0 0 auto;border:2px solid #fff;border-radius:9px;padding:7px 10px;background:#fff;color:{cfg["ink"]};font-weight:800;text-decoration:none}}.prog{{position:fixed;left:12px;right:12px;bottom:46px;height:6px;background:#fff;border:1px solid var(--line);z-index:19}}.prog>span{{display:block;height:100%;width:11.11%;background:{cfg["accent"]}}}
.overlay{{display:none;position:fixed;inset:0;z-index:40;background:#10233fdd;align-items:center;justify-content:center;padding:18px}}.overlay.on{{display:flex}}.overlay-card{{max-width:700px;background:#fff;border-radius:15px;padding:20px}}.overlay-card button{{padding:8px 12px}}
.print-pack{{display:none}}.printpack{{display:none}}@media(prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}}}
@media(max-width:720px){{.deck{{padding:10px 10px 118px}}.slide{{padding:15px}}.hero,.routes,.vocabrow{{grid-template-columns:1fr}}.lundy-grid{{grid-template-columns:1fr 1fr}}}}
@media print{{html,body{{color-scheme:light!important;background:#fff;color:#111;overflow:visible}}body>*:not(.print-pack){{display:none!important}}.print-pack{{display:block!important}}.printpack{{display:block!important}}.print-page{{break-after:page;page-break-after:always;padding:8mm;min-height:255mm}}.print-page:last-child{{break-after:auto;page-break-after:auto}}.print-pack h1{{font-size:20pt;line-height:1.15;margin:0 0 3mm}}.print-pack h2{{font-size:13pt;line-height:1.2;margin:3mm 0 1.5mm}}.print-pack p,.print-pack li{{font-size:10.5pt;line-height:1.35}}.running-head{{font-size:9pt;border-bottom:1px solid #666;margin-bottom:4mm;padding-bottom:2mm}}.proute,.print-route{{display:block;border:1px solid #777;padding:3mm;margin:3mm 0;break-inside:avoid}}@page{{size:A4;margin:10mm}}}}
</style>'''
    nav_style = '<style id="n6-nav1-css">@media print{.mbmhome,.n6-splash{display:none!important}}.mbmhome{display:inline-block;margin:6px 0 0 8px;font:600 .85rem/1.4 "Segoe UI",Arial,sans-serif;color:#1e3a8a;text-decoration:none}.mbmhome:hover,.mbmhome:focus{text-decoration:underline}</style>'
    controls = ''.join(f'<button type="button" data-tool="{i}">{label}</button>' for i,label in enumerate(cfg["controls"],1))
    print_routes = ''.join(f'<div class="{cfg["print_class"]} {cfg["route_classes"][label]}"><h3>{icon} {label}</h3><p>{esc.escape(profile["routes"][label])}</p></div>' for label,icon in (("Supported","◆"),("Standard","▲"),("Stretch","★")))
    print_topics = profile.get("print_topics", ["Topic 1", "Topic 2", "Topic 3"])
    print_rows = ''.join(f'<tr><td style="border:1px solid #777;padding:8px">{esc.escape(value)}</td><td style="border:1px solid #777;padding:8px;height:38mm"></td><td style="border:1px solid #777;padding:8px"></td></tr>' for value in print_topics)
    audit_items = profile.get("audit_items", ["One genuine record or completed action and why it matters", "One support or method detail that must stay separate", "One honest question or missing item", "One next action the learner chose"])
    print_pack = f'''<section class="print-pack printpack" aria-label="Printable lesson pack">
<section class="print-page"><div class="running-head">BUILD {cfg["domain"]} · Week {item["week"]}{item["slot"]} · {esc.escape(title)}</div><h1>{esc.escape(title)}</h1><p><b>Workbook trace:</b> {esc.escape(cells)}</p><p><b>Verbatim outcome:</b> {esc.escape(outcome)}</p><p><b>Objective:</b> {esc.escape(profile["objective"])}</p><h2>{esc.escape(profile.get("print_title","Working record"))}</h2><p>{esc.escape(profile.get("print_prompt","Record the supplied source, chosen action or observation, then add the explanation and an honest limit. Leave unavailable evidence as MISSING or AWAITING AUTHORISED CHECK."))}</p><table style="width:100%;border-collapse:collapse"><tr><th style="border:1px solid #777;padding:6px">Focus</th><th style="border:1px solid #777;padding:6px">Record or action</th><th style="border:1px solid #777;padding:6px">Explanation, response or limit</th></tr>{print_rows}</table></section>
<section class="print-page n6-lc-page"><div class="running-head">BUILD {cfg["domain"]} · route, audit and learner confirmation</div><h2>Choose a route</h2>{print_routes}<h2>Evidence audit</h2><ol>{''.join(f'<li>{esc.escape(value)}:</li>' for value in audit_items)}</ol><div style="height:42mm;border-bottom:1px solid #777"></div><!--n6-learner-confirm:v1-->{confirm}<!--/n6-learner-confirm--></section></section>'''
    config = {
        "id": Path(item["destination"]).stem, "family": item["family"], "week": item["week"], "slot": item["slot"],
        "title": title, "outcomes": item["outcomes"], "cells": item["cells"], "objective": profile["objective"],
        "source": {"workbook": "_passsb/inputs/Build SOW 2026-2027.xlsx", "sheet": item["cells"][0].split("!")[0].strip("'"), "cell": item["cells"][0].split("!")[1], "outcome": item["outcomes"][0]},
        "timings": [0,3,3,4,3,3,4,16,4], "tierLadder": cfg["ladder"],
        "nextFile": "START_HERE.html", "previousFile": "START_HERE.html",
    }
    script = '''<script>(function(){const slides=[...document.querySelectorAll("main.deck>.slide")],bar=document.querySelector(".prog>span");let index=0;function show(next){index=(next+slides.length)%slides.length;slides.forEach((s,i)=>s.classList.toggle("active",i===index));bar.style.width=((index+1)/slides.length*100)+"%";}document.querySelector("[data-nav=previous]").addEventListener("click",()=>show(index-1));document.querySelector("[data-nav=next]").addEventListener("click",()=>show(index+1));document.querySelectorAll("[data-tool]").forEach((button,i)=>button.addEventListener("click",()=>{if(i===0){const o=document.getElementById("taOverlay");o.classList.add("on");o.setAttribute("aria-hidden","false");}else if(i===1)document.body.classList.toggle("loop-on");else if(i===2)document.querySelector(".n6m-guide-btn")?.click();else if(i===3)document.body.classList.toggle("word-help");else if(i===4)document.body.classList.toggle("calm");else document.body.classList.toggle("teacher-freeze");}));document.querySelector("[data-close-overlay]").addEventListener("click",()=>{const o=document.getElementById("taOverlay");o.classList.remove("on");o.setAttribute("aria-hidden","true");});document.addEventListener("keydown",e=>{if(e.key==="ArrowRight")show(index+1);if(e.key==="ArrowLeft")show(index-1);});show(0);})();</script>'''
    return f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc.escape(title)} · BUILD {cfg["domain"]}</title>{styles}{guide}</head><body><!--n6-nav1:v1-->{nav_style}<a class="mbmhome" href="{cfg["home"]}" aria-label="Back to the Lessons catalogue">← Lessons</a><!--/n6-nav1--><a class="skip" href="#lessonDeck">Skip to lesson</a><main id="lessonDeck" class="deck">{''.join(slides)}</main><nav class="controls" aria-label="Lesson controls"><button type="button" data-nav="previous">◀ Previous</button>{controls}<button type="button" data-nav="next">Next ▶</button></nav><div class="prog" aria-hidden="true"><span></span></div><div id="taOverlay" class="overlay" aria-hidden="true"><div class="overlay-card"><h2>TA Brief</h2><p>Use the least prompt needed. Keep adult preparation and exact-word scribing separate from pupil authorship. Guidance is hidden from the learner surface by default.</p><button type="button" data-close-overlay>Close</button></div></div>{print_pack}{splash}<script id="lesson-config" type="application/json">{json.dumps(config,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')}</script>{script}</body></html>'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--destination", required=True)
    parser.add_argument("--replace-generated", action="store_true", help="replace only a prior W2 generated lesson at the same frozen destination")
    args = parser.parse_args()
    build = json.loads(BUILD_SET.read_text(encoding="utf-8"))["build"]
    item = next((row for row in build if row["destination"] == args.destination), None)
    if item is None:
        raise SystemExit("destination is not in the frozen W2 build set")
    if args.destination not in PROFILES:
        raise SystemExit("NO DECK YET: no reviewed lesson-specific profile")
    if item["family"] not in FAMILY:
        raise SystemExit("NO DECK YET: family template not proved")
    target = ROOT / args.destination
    if target.exists():
        prior = target.read_text(encoding="utf-8")
        if not args.replace_generated:
            raise SystemExit(f"occupied destination path: {args.destination}")
        if '<script id="lesson-config" type="application/json">' not in prior or '<main id="lessonDeck" class="deck">' not in prior:
            raise SystemExit(f"REFUSE REPLACE: destination is not a prior W2 generated lesson: {args.destination}")
    source = build_lesson(item, PROFILES[args.destination])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source, encoding="utf-8")
    print(json.dumps({"status":"BUILT","destination":args.destination,"bytes":target.stat().st_size,"sourceWords":words(source)},indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
