#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GSG-1 A7 — GROW Practicals & Equipment Matrix, both brandings.

Source: the v3+ review pack's GROW_SCIENCE_V3PLUS_EQUIPMENT_MATRIX.md,
CORRECTED against the live lessons. The source matrix carries the same class of
defect BSG-1 found in the BUILD one, and worse: THREE of its nine columns are
identical boilerplate in all ten rows —

  Preparation            "Prepare labelled stations/marks and offer ready-cut
                          or ready-made access where stated."   x10
  Reusable / consumable  "Mostly reusable. Paper tables/cards and worn surfaces
                          are replaceable consumables."         x10
  Setup time             "About 2-6 minutes"                    x10

— and its Digital alternative column names ten "Made by Matt" labs that are NOT
installed in the live suite. Every one of those four columns is re-derived here
per lesson against the live files. Nothing that does not exist is advertised.
"""
import os, html

OUT = "/home/user/Lessons/Science_Teesside/Grow/v3_40min"

ROWS = [
 dict(k="W3A", inv="Grip and Slide Investigation",
  eq="Trainer sole or rubber offcut; smooth plastic; fabric; rough card; small light block; shallow tray.",
  rc="Soles, plastic, block and tray reusable. Rough card and fabric abrade with use — consumable, expect to replace termly.",
  prep="Adult cuts and labels the four surface pieces before the lesson and tapes them into the tray. Pupils never cut card.",
  st="4 min",
  saf="Light block only, worked inside the tray. Keep the floor clear. Do not use sandpaper — its cut edge abrades skin.",
  dig="In-lesson <b>Surface explorer</b> (three buttons: smooth / medium / rough). Button-only, no handling, no drag.",
  fb="The pupil directs: names the two surfaces to compare, states the prediction, and an adult performs the slide on the pupil’s instruction. The prediction and the explanation stay the pupil’s."),
 dict(k="W3B", inv="Fixed-Ramp Surface Test",
  eq="Small block or trolley; low ramp fixed at one height; three surfaces; tape measure; tray; results table.",
  rc="Ramp, block, tape measure and tray reusable. Surfaces and printed results tables consumable.",
  prep="Adult fixes the ramp at ONE height and marks the release point — the fixed height is the controlled variable and must not be adjustable mid-lesson. Pre-print the three-column results table.",
  st="5 min",
  saf="Low ramp inside a tray. One release at a time. Hands clear of the run-off. Light loads only.",
  dig="In-lesson <b>results tool</b>: enter three distances, the bar chart redraws. Typed entry, keyboard-operable.",
  fb="The pupil calls each release, reads the measurement with an adult’s finger held on the tape, and decides which surface needs a repeat."),
 dict(k="W4A", inv="Mechanism Station Hunt",
  eq="Ruler and pivot block; simple pulley or pulley image; gear pair or bicycle-gear image; bottle opener; scissors (adult-held only).",
  rc="All items reusable. Printed station cards consumable.",
  prep="Adult sets out four labelled stations and keeps every sharp tool. No station requires a pupil to cut, pierce or force anything.",
  st="6 min (four stations)",
  saf="Stable pivots and light loads. <b>Adult controls all sharp tools.</b> Name the pinch and trap points aloud before starting: gear teeth mesh, pulley rope entry, and the hinge of the bottle opener. Fingers stay clear of all three.",
  dig="In-lesson <b>lever model</b> (pivot slider, arrow-key operable, with a written result line). It covers the lever station only — pulleys and gears have no installed digital route in this lesson.",
  fb="The pupil directs the hunt: chooses which station to visit, points to where the force goes in and where it comes out, and an adult operates the mechanism exactly as instructed."),
 dict(k="W4B", inv="Lever Pivot Investigation",
  eq="Ruler or wooden strip; stable pivot block; light load; tape measure; optional spring balance; tray.",
  rc="All items reusable. Recording sheets consumable.",
  prep="Adult marks three pivot positions on the ruler in advance and checks the pivot block cannot roll. Agree the effort scale before the lesson if a spring balance is not available.",
  st="4 min",
  saf="Stable pivot, light load, worked over a tray or low table. Keep fingers clear of the pivot and of the falling load — <b>both are trap points</b>. An adult positions the load for any pupil who cannot judge the drop.",
  dig="In-lesson <b>lever model</b>: pivot slider with a written explanation of the effort/distance trade. Native slider, arrow-key operable.",
  fb="The pupil chooses each pivot position and predicts the effect; an adult moves the pivot and reads the result back. The pupil states the conclusion."),
 dict(k="W5A", inv="Fair-Test Planning Lab (planning only — no equipment handled)",
  eq="CHANGE / MEASURE / KEEP-SAME cards; unit cards; a ramp and block for demonstration only; planning frame.",
  rc="Cards and ramp reusable. Planning frames consumable.",
  prep="Adult prepares one deliberately faulty method for the pupils to repair, and checks the card set is complete. Equipment is demonstrated, not issued.",
  st="3 min",
  saf="Planning lesson: pupils handle no equipment. The demonstration uses a low ramp, a light object and a clear run-off area. <b>An adult checks every plan before any equipment is used in W5B.</b>",
  dig="In-lesson <b>method repair tool</b>: three checkboxes and a written verdict on whether the method can answer its question.",
  fb="The pupil makes every variable decision aloud and an adult places the cards as directed. No handling is required at any point in this lesson."),
 dict(k="W5B", inv="Repeat Evidence Investigation",
  eq="Trolley or block; ramp fixed at the W5A-agreed height; three surfaces; tape measure; repeat table; calculator optional.",
  rc="Ramp, trolley, tape measure reusable. Surfaces and repeat tables consumable.",
  prep="Adult sets the ramp to the height the class agreed in W5A and pre-prints the nine-cell repeat table. Check the calculator if means are to be worked digitally.",
  st="5 min",
  saf="Low ramp, light block, clear run-off tray. One person releases at a time. Agree who releases and who measures before starting.",
  dig="In-lesson <b>data tool</b>: nine readings in, three means and a bar chart out, with a written prompt to inspect the individual repeats before trusting the summary.",
  fb="The pupil decides the number of repeats, says which reading looks wrong and why, and directs an adult through the measuring. The judgement is the assessed part, not the handling."),
 dict(k="W6A", inv="Planet Order and Orbit Model",
  eq="Sun card; eight planet cards; orbit arrows; floor or desk space; optional short string circles.",
  rc="All cards reusable if laminated. Unlaminated cards consumable.",
  prep="Adult clears a floor area or desk run and lays the Sun card. Keep string pre-cut, short and flat — it is a trip hazard at length.",
  st="5 min",
  saf="Floor markers in a clear area only. No running. String stays flat and short. Use the desk version where floor work is not safe.",
  dig="In-lesson <b>Mission Control</b>: order the eight planets by button, with a reset, and a written prompt at each step. No floor movement needed.",
  fb="The pupil names the next planet and an adult places the card. Ordering the Solar System aloud is the whole task — placement is not."),
 dict(k="W6B", inv="Orbit Model Build and Review",
  eq="Sun and planet cards or balls; labels; arrows; large paper; tape; optional short string.",
  rc="Balls, tape dispenser and arrows reusable. Paper, labels and string consumable.",
  prep="Adult pre-cuts every card, label and string length. Nothing in this build requires a pupil to cut or pierce. Decide in advance whether the model will be honest about size or about distance — it cannot be both.",
  st="6 min",
  saf="Blunt, pre-cut materials only. Keep floor models clear of walkways. String stays short and flat.",
  dig="In-lesson <b>orbit model</b>: four orbital positions by button, each with a written gravity/motion prompt.",
  fb="The pupil directs an adult to place each piece exactly where the pupil chooses, then states what the model gets right and what it deliberately gets wrong. Directing the build is the assessed skill."),
 dict(k="W7A", inv="Torch-and-Moon Investigation",
  eq="Lamp or torch; foam ball; Earth/observer marker; phase cards; a dimmable area, or the bright-room diagram alternative.",
  rc="Lamp, ball and markers reusable. Phase cards consumable if unlaminated.",
  prep="Adult positions the lamp at pupil head height pointing away from faces, and tests the dimming level in advance. If the room cannot be dimmed safely, print the bright-room diagram instead — it is a full alternative, not a lesser one.",
  st="5 min",
  saf="<b>Never shine a torch towards anyone’s eyes.</b> Keep the room light enough to move safely. Use the bright-room diagram where dimming would distress a pupil or make movement unsafe.",
  dig="In-lesson <b>phase model</b>: four positions by button, each stating that the effect is viewing geometry and not Earth’s shadow.",
  fb="The pupil directs the lamp and ball positions and names what an observer on Earth would see. An adult holds the equipment throughout."),
 dict(k="W7B", inv="Eight-Step Lunar Studio",
  eq="Lamp or torch; foam ball; Earth marker; eight phase cards or a ready-made phase wheel.",
  rc="Lamp, ball, marker and wheel reusable. Phase cards consumable.",
  prep="Adult uses a ready-made or pre-punched phase wheel. <b>No pupil uses a split pin or punches a hole.</b> Test the lamp position before the lesson.",
  st="5 min",
  saf="Do not point light at faces. Pre-punched or ready-made wheels only. Keep the movement area clear before anyone stands up.",
  dig="In-lesson <b>phase model</b> used as the eight-step route: buttons are the complete task, with the phase-versus-eclipse distinction stated in text.",
  fb="The pupil calls each of the eight positions in order and an adult moves the ball. Producing the phases on command is the assessment, whoever holds the equipment."),
]

CSS = """
body{font-family:'Segoe UI',Tahoma,Arial,sans-serif;margin:0;background:#f4f9f7;color:#1f2937}
main{max-width:1240px;margin:auto;padding:24px}
header{background:#10233f;color:#fff;border-radius:20px;padding:22px}
h1{font-size:clamp(1.7rem,4vw,2.6rem);margin:.2rem 0}
.call{background:#eaf6f1;border-left:7px solid #3F7D6E;padding:12px 14px;border-radius:12px;margin:14px 0}
.warn{background:#fff2e7;border-left:7px solid #b55f25;padding:12px 14px;border-radius:12px;margin:14px 0}
table{border-collapse:collapse;width:100%;background:#fff;box-shadow:0 10px 30px rgba(0,0,0,.08);font-size:.92rem}
th,td{padding:9px;border-bottom:1px solid #e2e8f0;text-align:left;vertical-align:top}
th{background:#eaf6f1;position:sticky;top:0}
td b.ln{color:#10233f}
footer{margin:18px 0 6px;font-size:.85rem;color:#64748b}
@media(max-width:900px){table,thead,tbody,tr,th,td{display:block}thead{display:none}td{border-bottom:0}td:before{content:attr(data-l);display:block;font-weight:900;color:#215e53;font-size:.78rem;text-transform:uppercase}tr{border-bottom:8px solid #eef4f1;padding:6px 0}}
@media print{header,.call,.warn{break-inside:avoid}table{font-size:8.5pt}@page{size:A4 landscape;margin:9mm}}
"""

COLS = [("Lesson", "k"), ("Investigation", "inv"), ("Equipment (per group)", "eq"),
        ("Reusable / consumable", "rc"), ("Preparation (adult)", "prep"),
        ("Setup", "st"), ("Safety", "saf"), ("Digital alternative", "dig"),
        ("No-equipment fallback", "fb")]


def build(progress):
    brand_meta = ('<meta name="x-brand" content="progress-schools">' if progress else "")
    comment = ("<!-- Progress Schools staff variant · GROW Science v3 40-minute route — "
               if progress else
               "<!-- Made by Matt · GROW Science v3 40-minute route — ")
    comment += ("practicals & equipment matrix. Staff-facing artefact. Derived from the v3+ "
                "review-pack equipment matrix and corrected against the live lessons at "
                "dcc23dc: the source matrix's Preparation, Reusable/consumable and Setup-time "
                "columns were identical boilerplate in all ten rows, and its Digital "
                "alternative column named ten labs that are not installed. All four columns "
                "re-derived per lesson. -->")
    head = ('<header><div>PROGRESS SCHOOLS · TEES VALLEY</div>'
            '<div style="font-size:.8rem;opacity:.85">GROW Science · 2026–27 Aut 1</div>'
            if progress else
            '<header><div>Made by Matt · for Progress Schools · GROW Science · 2026–27 Aut 1</div>')
    foot = ('Progress Schools · Tees Valley · staff use · GROW Science 40-minute route '
            '(Aut 1 W3–W7). Source: v3+ equipment matrix (received 2026-08-12), corrected '
            'per lesson against the live route. <span style="opacity:.75">by madebymatt.uk</span>'
            if progress else
            'Made by Matt · prepared for Progress Schools staff use · GROW Science '
            '40-minute route (Aut 1 W3–W7). Source: v3+ equipment matrix (received '
            '2026-08-12), corrected per lesson against the live route.')

    rows = ""
    for r in ROWS:
        cells = ""
        for label, key in COLS:
            v = r[key]
            if key == "k":
                v = '<b class="ln">%s</b>' % v
            cells += '<td data-l="%s">%s</td>' % (label, v)
        rows += "<tr>%s</tr>" % cells

    return (
      '<!doctype html><html lang="en-GB"><head><meta charset="utf-8">'
      '<meta name="viewport" content="width=device-width,initial-scale=1">'
      '<title>GROW Science W3–W7 · Practicals &amp; Equipment Matrix</title>'
      + brand_meta + '<style>' + CSS + '</style></head><body>\n' + comment + '\n<main>\n'
      + head +
      '<h1>Practicals &amp; Equipment Matrix · W3–W7</h1>'
      '<p>One page per half-term: what each investigation needs, how it is made safe, and '
      'the two routes that keep every pupil in the practical — a digital alternative and a '
      'no-equipment fallback. A pupil who cannot handle materials still <b>directs</b> the '
      'investigation, and directing it is the assessed skill.</p></header>\n'
      '<div class="warn"><b>Safety authority.</b> No CLEAPSS approval is claimed for any '
      'activity on this page. Each activity requires a <b>local, proportionate risk '
      'assessment</b> before use; local COSHH and risk-assessment decisions determine the '
      'actual controls, and a headteacher signature alone is not sufficient. '
      '<b>An adult does all cutting, piercing and pin-fitting</b> — pupils never cut card, '
      'punch holes or fit split pins. Where a mechanism has pinch or trap points (W4A gear '
      'teeth and pulley rope entry, W4B pivot and falling load) name them aloud before the '
      'practical begins.</div>\n'
      '<div class="call"><b>Two routes, not one.</b> Every lesson carries a digital '
      'alternative and a no-equipment fallback. Neither is a reduced version of the lesson: '
      'the Science goal is identical and only the response route changes. The digital column '
      'names <b>only routes that are installed in the live lesson files</b> — where a route '
      'does not exist, this page says so rather than advertising one.</div>\n'
      '<table><thead><tr>' +
      "".join("<th>%s</th>" % c[0] for c in COLS) +
      '</tr></thead><tbody>' + rows + '</tbody></table>\n'
      '<footer>' + foot + '</footer>\n</main></body></html>\n')


for progress in (False, True):
    name = ("GROW_SCIENCE_PRACTICALS_MATRIX_PROGRESS_SCHOOLS.html" if progress
            else "GROW_SCIENCE_PRACTICALS_MATRIX.html")
    p = os.path.join(OUT, name)
    open(p, "w", encoding="utf-8").write(build(progress))
    print("wrote %-58s %6d bytes" % (name, os.path.getsize(p)))
