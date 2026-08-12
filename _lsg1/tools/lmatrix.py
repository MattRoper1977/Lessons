#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LSG-1 A7 — LAUNCH Practicals & Equipment Matrix, both brandings.

Source: the v3+ review pack's LAUNCH_SCIENCE_V3PLUS_EQUIPMENT_MATRIX.md.

CREDIT WHERE IT IS DUE, because the previous sibling earned the opposite: this
matrix is per-lesson in every column - no degenerate boilerplate anywhere - and
every lab it names DOES exist. The GROW pack had three identical columns and ten
labs that were not installed; the LAUNCH one has neither fault. Verified, not
assumed: all 15 named labs were found in the live files.

ONE correction made: the pack's Digital-alternative column names each LESSON's
mission title ("Made by Matt · Membrane Reasoning Lab"). That is true but
imprecise for a staff artefact - a teacher covering a missing practical needs to
know WHICH interactive route inside the lesson substitutes for it. Every entry
below names the specific route verified present in the live file.
"""
import os

OUT = "/home/user/Lessons/Science_Teesside/Launch/v3_40min"

ROWS = [
 dict(k="W3L1", inv="Prepared-Slide Microscope Investigation",
  eq="Light microscope; prepared slide; lens tissue; observation sheet; pencil.",
  rc="Microscope, slides and lens tissue holder reusable. Lens tissue and any replaced slide are consumable.",
  prep="Adult sets the microscope on a firm bench, away from the edge, and starts it on the LOWEST power. Check no slide is cracked before it is issued.",
  st="4 min",
  saf="Keep the microscope back from the bench edge. Hold slides by their sides. <b>A cracked slide is never issued or used.</b> Adults handle any replacement.",
  dig="In-lesson <b>Scientific reasoning model</b> — reveal-step buttons that walk the low-power-first routine and separate magnification from resolution.",
  fb="The pupil directs the observation: says what to look for, what power to use and what has been seen, while an adult operates the microscope. The observation and its explanation stay the pupil's."),
 dict(k="W3L2", inv="Printed Micrograph Scale Investigation",
  eq="Printed cell images; rulers; calculators; unit conversion card; pencil.",
  rc="Rulers, calculators and laminated cards reusable. Unlaminated micrographs consumable.",
  prep="Adult issues one image at a time and displays the conversion 1 mm = 1000 µm before any calculation starts.",
  st="3 min",
  saf="Ordinary rulers and calculators only. Keep the working area clear so images are not torn or lost.",
  dig="In-lesson <b>Local calculation lab</b> — enter image and real size, get magnification, with the unit-matching rule stated on screen.",
  fb="The pupil chooses which measurement to take and states the calculation; an adult measures and writes to dictation. The decision about which quantity to divide is the assessed part."),
 dict(k="W3L3", inv="Magnification Question Circuit",
  eq="Question cards; rulers; calculators; conversion card; paper.",
  rc="Cards, rulers and calculators reusable. Printed question sheets consumable.",
  prep="Adult sets out three question stations and keeps model answers hidden until a pupil has made a full attempt.",
  st="4 min",
  saf="Keep the room calm. <b>No public scores, no leaderboards and no speed pressure</b> — this is a reasoning circuit, not a race.",
  dig="In-lesson <b>Local calculation lab</b> — one problem at a time, with the method line shown so the working stays visible.",
  fb="The pupil dictates the method step by step and an adult scribes it. Producing a checkable method is the assessment, not the handwriting."),
 dict(k="W4L1", inv="Food-Colour Diffusion Observation",
  eq="Clear cups; cool and warm water; food colour; timer; white card backing.",
  rc="Cups, timer and card reusable. Water and food colour consumable.",
  prep="<b>An adult sets up the matched cups and pours all water.</b> Use warm water, never hot. Fill both cups to the same level so the only deliberate difference is temperature.",
  st="5 min",
  saf="<b>The adult handles all warm water.</b> Nothing in the lab is drunk or tasted. Wipe spills immediately — a wet floor is the real hazard here.",
  dig="In-lesson <b>Scientific reasoning model</b> — reveal-step buttons for random motion, net movement and the factors that change the rate.",
  fb="The pupil calls the start, watches and describes what spreads and how fast, while an adult handles every cup. Describing the net movement is the assessed skill."),
 dict(k="W4L2", inv="Alveolus Adaptation Model",
  eq="Large and small bubble-wrap sheets or paper models; thin card; arrow cards; feature cards.",
  rc="Model kit reusable. Paper or film consumable if remade.",
  prep="Adult lays out clean model parts. <b>No breath, blood or body samples are collected or used at any point.</b>",
  st="4 min",
  saf="<b>Models only.</b> Do not collect breath, saliva, blood or any body sample. Pupils with latex or material sensitivities use the card model.",
  dig="In-lesson <b>Scientific reasoning model</b> — reveal-step buttons linking surface area, thinness and the gradient to the rate.",
  fb="The pupil directs which feature to add to the model and explains what it does to the rate; an adult assembles it. The explanation is the assessment."),
 dict(k="W4L3", inv="Explanation Construction Circuit",
  eq="Sentence-frame cards; example answers; annotated diagrams; paper.",
  rc="Cards and diagrams reusable if laminated. Printed frames consumable.",
  prep="Adult prepares one incomplete explanation for pupils to finish, and keeps the full version hidden until an attempt exists.",
  st="3 min",
  saf="Desk-based lesson with no equipment hazard. Keep the task unranked and give thinking time before any verbal prompt.",
  dig="In-lesson <b>Command-word decoder</b> — separates what the question asks you to DO from the Biology, one command word at a time.",
  fb="The pupil says the explanation aloud in order and an adult scribes the exact words. Linking cause to effect is the assessed skill, not writing it down."),
 dict(k="W5L1", inv="Membrane Demonstration",
  eq="Visking tubing or a modelled membrane; two solutions; beaker; stand; timer.",
  rc="Stand, beaker and timer reusable. Tubing and solutions consumable.",
  prep="<b>Adult prepares and fills the tubing</b> and ties both ends. Pupils observe and predict; they do not fill or cut anything.",
  st="5 min",
  saf="<b>Adult-performed demonstration.</b> Nothing is tasted. Wash hands afterwards. Follow the local risk assessment for the solutions in use.",
  dig="In-lesson <b>Scientific reasoning model</b> — reveal-step buttons for the partially permeable membrane and the direction of water movement.",
  fb="The pupil predicts the direction of water movement and explains it from the model; the demonstration is adult-run for everyone anyway, so no pupil is treated differently."),
 dict(k="W5L2", inv="Potato Osmosis Core Practical",
  eq="Adult-prepared matched potato cylinders; pre-soaked samples; labelled solutions; balance; forceps; paper towel; eye protection as the local risk assessment requires.",
  rc="Balances, forceps and vessels reusable. Potato samples and prepared solutions consumable.",
  prep="<b>All cutting and boring is adult-performed before the lesson.</b> Use pre-soaked matched samples so a mass change is measurable within the lesson. Label every solution. Follow the local risk assessment.",
  st="6 min",
  saf="<b>Cork borers and scalpels are adult-only tools and are not on the pupil bench.</b> Nothing is eaten or tasted. Clean spills at once and wash hands at the end. Eye protection per local policy.",
  dig="In-lesson <b>Percentage-change lab</b> (enter two masses, get the change) plus the <b>Osmosis prediction lab</b> — button-only, three solutions held side by side. <i>The prediction lab is a specimen awaiting sign-off.</i>",
  fb="The pupil chooses the solutions to compare, predicts each direction and calculates from the class dataset while an adult handles all samples and the balance. The prediction, the calculation and the evaluation are the assessment."),
 dict(k="W5L3", inv="Graph and Method Review",
  eq="Prepared data; graph paper; ruler; calculator; method review cards.",
  rc="Rulers, calculators and cards reusable. Printed graph and data sheets consumable.",
  prep="Adult gives the same dataset to everyone, and marks the axes and units before any plotting begins.",
  st="3 min",
  saf="Desk-based. Rulers and calculators used normally. Keep the task calm and unranked — this lesson judges a method, not a person.",
  dig="In-lesson <b>Osmosis data studio</b> — plot the series, read the trend and locate the zero-change crossing.",
  fb="The pupil states each plotted point and where the line crosses zero while an adult draws. Reading the pattern and evaluating the method is the assessed part."),
 dict(k="W6L1", inv="Against-the-Gradient Demonstration",
  eq="Gradient model cards; counters or beads; two labelled zones; energy tokens.",
  rc="All reusable. Printed zone cards consumable if unlaminated.",
  prep="Adult lays out the two zones and the counters. Keep the energy tokens visibly separate so the cost of the movement stays obvious.",
  st="3 min",
  saf="Desk-based with no hazard. <b>Small counters and beads are a choking risk</b> — check suitability for the group and supervise throughout.",
  dig="In-lesson <b>Scientific reasoning model</b> — reveal-step buttons for movement against the gradient and the respiration that pays for it.",
  fb="The pupil directs which counter moves where and states what the movement costs; an adult moves the pieces. Naming the energy source is the assessment."),
 dict(k="W6L2", inv="Root Hair and Gut Evidence Review",
  eq="Root hair and villus diagrams; uptake data cards; oxygen-effect dataset; highlighters.",
  rc="Diagrams and data cards reusable if laminated. Highlighted copies consumable.",
  prep="Adult prepares the oxygen-effect dataset in advance so pupils meet the evidence, not the experiment. <b>No plant or animal tissue is dissected.</b>",
  st="3 min",
  saf="Desk-based, evidence only. No dissection, no live material, no body samples.",
  dig="In-lesson <b>Scientific reasoning model</b> — reveal-step buttons linking cell shape, surface area and respiration to the uptake evidence.",
  fb="The pupil says which data support active transport and why; an adult highlights to dictation. Interpreting the evidence is the assessed skill."),
 dict(k="W6L3", inv="Transport Decision Circuit",
  eq="Scenario cards; three process labels; comparison grid; paper.",
  rc="Cards, labels and grid reusable. Printed grids consumable.",
  prep="Adult shuffles the scenario cards so the order is not predictable, and keeps the answer key hidden until a full attempt exists.",
  st="3 min",
  saf="Desk-based with no equipment hazard. Keep decisions private — no public sorting into right and wrong.",
  dig="In-lesson <b>Scientific reasoning model</b> — reveal-step buttons for the two questions that separate the three processes.",
  fb="The pupil classifies each scenario aloud with a reason and an adult places the card. The reason, not the placement, is the assessment."),
 dict(k="W7L1", inv="Topic 1 Knowledge Mapping",
  eq="Concept cards; large paper; link arrows; pens.",
  rc="Concept cards and arrows reusable. Large paper consumable.",
  prep="Adult lays out the concept cards face up. Do not pre-draw any links — the links are the lesson.",
  st="3 min",
  saf="Desk-based with no hazard. Keep the map private to the group; no public comparison of maps.",
  dig="In-lesson <b>Topic 1 retrieval map</b> — build the connections by button, one link at a time.",
  fb="The pupil names each link and why it holds while an adult draws it. Naming the connection is the assessment, not drawing the arrow."),
 dict(k="W7L2", inv="Command-Word Decoding Circuit",
  eq="Command-word cards; question cards; answer-shape frames; paper.",
  rc="Cards and frames reusable if laminated. Printed frames consumable.",
  prep="Adult pairs each command word with a question on the same Biology, so the only thing changing is the instruction.",
  st="3 min",
  saf="Desk-based with no hazard. No timed conditions and no public marking — this lesson decodes questions, it does not test them.",
  dig="In-lesson <b>Command-word decoder</b> — choose a command word and see what the answer has to do differently.",
  fb="The pupil says what the command word demands and an adult scribes the shaped answer. Decoding the demand is the assessed skill."),
 dict(k="W7L3", inv="Independent Question Practice and Improvement",
  eq="Question set; answer paper; improvement frame; pen.",
  rc="Question sets reusable if laminated. Answer paper consumable.",
  prep="Adult prepares the question set and one improvement frame per pupil. Keep any worked response hidden until an attempt exists.",
  st="3 min",
  saf="Desk-based. <b>Not run under exam conditions:</b> no timing pressure, no silence rule and no public results. Pupils may pause at any point.",
  dig="In-lesson <b>Scientific reasoning model</b> — reveal-step buttons for building an answer and then improving one.",
  fb="The pupil dictates the answer and then dictates the improvement, with an adult scribing both. Naming what the improvement changes is the assessment."),
]

CSS = """
body{font-family:'Segoe UI',Tahoma,Arial,sans-serif;margin:0;background:#f7f6fb;color:#1f2937}
main{max-width:1240px;margin:auto;padding:24px}
header{background:#2b2140;color:#fff;border-radius:20px;padding:22px}
h1{font-size:clamp(1.7rem,4vw,2.6rem);margin:.2rem 0}
.call{background:#f2eefa;border-left:7px solid #7A5C9E;padding:12px 14px;border-radius:12px;margin:14px 0}
.warn{background:#fff2e7;border-left:7px solid #b55f25;padding:12px 14px;border-radius:12px;margin:14px 0}
table{border-collapse:collapse;width:100%;background:#fff;box-shadow:0 10px 30px rgba(0,0,0,.08);font-size:.92rem}
th,td{padding:9px;border-bottom:1px solid #e2e8f0;text-align:left;vertical-align:top}
th{background:#f2eefa;position:sticky;top:0}
td b.ln{color:#2b2140}
footer{margin:18px 0 6px;font-size:.85rem;color:#64748b}
@media(max-width:900px){table,thead,tbody,tr,th,td{display:block}thead{display:none}td{border-bottom:0}td:before{content:attr(data-l);display:block;font-weight:900;color:#4b3b6b;font-size:.78rem;text-transform:uppercase}tr{border-bottom:8px solid #eeeaf5;padding:6px 0}}
@media print{header,.call,.warn{break-inside:avoid}table{font-size:8.5pt}@page{size:A4 landscape;margin:9mm}}
"""

COLS = [("Lesson", "k"), ("Investigation", "inv"), ("Equipment (per group)", "eq"),
        ("Reusable / consumable", "rc"), ("Preparation (adult)", "prep"),
        ("Setup", "st"), ("Safety", "saf"), ("Digital alternative", "dig"),
        ("No-equipment fallback", "fb")]


def build(progress):
    brand = '<meta name="x-brand" content="progress-schools">' if progress else ""
    comment = ("<!-- Progress Schools staff variant · " if progress
               else "<!-- Made by Matt · ")
    comment += ("LAUNCH GCSE Biology v3 40-minute route — practicals & equipment matrix. "
                "Staff-facing artefact. Derived from the v3+ review-pack equipment matrix, "
                "which unlike the GROW one carried NO degenerate columns and NO phantom "
                "labs — all 15 named labs verified present in the live files. One "
                "correction: its Digital-alternative column named each lesson's mission "
                "title; every entry here names the specific interactive route verified "
                "installed in that lesson. -->")
    head = ('<header><div>PROGRESS SCHOOLS · TEES VALLEY</div>'
            '<div style="font-size:.8rem;opacity:.85">LAUNCH GCSE Biology · 2026–27 Aut 1</div>'
            if progress else
            '<header><div>Made by Matt · for Progress Schools · LAUNCH GCSE Biology · 2026–27 Aut 1</div>')
    foot = ('Progress Schools · Tees Valley · staff use · LAUNCH GCSE Biology 40-minute '
            'route (Aut 1 W3–W7). Source: v3+ equipment matrix (received 2026-08-12), '
            'digital column re-derived per lesson against the live route. '
            '<span style="opacity:.75">by madebymatt.uk</span>'
            if progress else
            'Made by Matt · prepared for Progress Schools staff use · LAUNCH GCSE Biology '
            '40-minute route (Aut 1 W3–W7). Source: v3+ equipment matrix (received '
            '2026-08-12), digital column re-derived per lesson against the live route.')
    rows = ""
    for r in ROWS:
        cells = "".join('<td data-l="%s">%s</td>'
                        % (lbl, ('<b class="ln">%s</b>' % r[k]) if k == "k" else r[k])
                        for lbl, k in COLS)
        rows += "<tr>%s</tr>" % cells
    return (
      '<!doctype html><html lang="en-GB"><head><meta charset="utf-8">'
      '<meta name="viewport" content="width=device-width,initial-scale=1">'
      '<title>LAUNCH GCSE Biology W3–W7 · Practicals &amp; Equipment Matrix</title>'
      + brand + '<style>' + CSS + '</style></head><body>\n' + comment + '\n<main>\n' + head +
      '<h1>Practicals &amp; Equipment Matrix · W3–W7</h1>'
      '<p>One page per half-term: what each investigation needs, how it is made safe, and '
      'the two routes that keep every pupil in the practical — a digital alternative and a '
      'no-equipment fallback. A pupil who cannot handle materials still <b>directs</b> the '
      'investigation, and directing it is the assessed skill.</p></header>\n'
      '<div class="warn"><b>Safety authority.</b> No CLEAPSS approval is claimed for any '
      'activity on this page. Each activity requires a <b>local, proportionate risk '
      'assessment</b> before use, and local COSHH and risk-assessment decisions determine '
      'the actual controls — a headteacher signature alone is not sufficient. '
      '<b>Cork borers, scalpels and any other cutting or boring tool are adult-performed '
      'where the setting\'s risk assessment says so, and are not placed on the pupil '
      'bench.</b> Solutions are adult-prepared and labelled. Nothing in any of these '
      'lessons is eaten, tasted or drunk, and no breath, blood or other body sample is '
      'collected at any point.</div>\n'
      '<div class="call"><b>Two routes, not one.</b> Every lesson carries a digital '
      'alternative and a no-equipment fallback. Neither is a reduced version: the Biology '
      'goal is identical and only the response route changes. The digital column names '
      '<b>only routes verified present in the live lesson files</b>, and says where one is '
      'still awaiting sign-off rather than advertising it as available.</div>\n'
      '<div class="call"><b>This is Topic 1 teaching, not exam administration.</b> No mark '
      'schemes, mark allocations or grade boundaries appear anywhere in this suite or on '
      'this page. W7L3 is independent practice with feedback — it is explicitly <b>not</b> '
      'run under exam conditions.</div>\n'
      '<table><thead><tr>' + "".join("<th>%s</th>" % c[0] for c in COLS) +
      '</tr></thead><tbody>' + rows + '</tbody></table>\n'
      '<footer>' + foot + '</footer>\n</main></body></html>\n')


for progress in (False, True):
    name = ("LAUNCH_SCIENCE_PRACTICALS_MATRIX_PROGRESS_SCHOOLS.html" if progress
            else "LAUNCH_SCIENCE_PRACTICALS_MATRIX.html")
    p = os.path.join(OUT, name)
    open(p, "w", encoding="utf-8").write(build(progress))
    print("wrote %-60s %6d bytes" % (name, os.path.getsize(p)))
