#!/usr/bin/env python3
# l2k_build.py — pass PEQ-L2K: builds the seven Kitchen Programme surfaces in
# GROW_ASDAN/PEQ_L2_Kitchen/ from the proven ledger (l2k_plan.py output) and the
# committed AC facts. Deterministic: same inputs -> same bytes (idempotence gate).
#
#   python3 _passpq/tools/l2k_build.py            # build all pages
#   L2K_PLANT_GAP=1 python3 ... l2k_build.py      # control: drops one AC from the
#                                                 # matrix -> the build itself goes RED
#
# The coverage invariant lives HERE: every AC of all 18 units must land on a week
# with a named artefact, or the build raises and writes nothing.

import json, os, re, sys, html

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "GROW_ASDAN", "PEQ_L2_Kitchen")
LED = json.load(open(os.path.join(ROOT, "_passpq", "inputs", "peq_l2k_year_ledger.json")))
AC = json.load(open(os.path.join(ROOT, "_passpq", "inputs", "peq_l2k_ac_facts.json")))

SKILLS = ["Com", "DecMk", "LSk", "TmWk", "Th", "Wellb"]
LANES = ["E3", "L1", "L2"]
LANE_NAME = {"E3": "Entry 3", "L1": "Level 1", "L2": "Level 2"}
LANE_HEX = {"E3": "#4C9A6F", "L1": "#4A6FA5", "L2": "#96603C"}
SKILL_NAME = {"Com": "Communication", "DecMk": "Decision making", "LSk": "Learning",
              "TmWk": "Team working", "Th": "Thinking / Critical thinking", "Wellb": "Wellbeing in learning"}

# the Progress mark + the byte-identical staff facts panel, lifted from the live page
_grow = open(os.path.join(ROOT, "GROW_ASDAN", "Scheme_and_Resources.html"), encoding="utf-8").read()
def _slice(s, start, endtag):
    i = s.find(start); assert i >= 0, start
    j = s.find(endtag, i); assert j >= 0
    return s[i:j + len(endtag)]
MARK_SVG = _slice(_grow, '<svg width="56"', "</svg>")
def _panel(s):
    i = s.find('<div class="note" id="peq-facts-panel">'); assert i >= 0
    import re
    depth = 0
    for m in re.finditer(r'<div\b|</div>', s[i:]):
        depth += 1 if m.group(0).startswith("<div") else -1
        if depth == 0:
            return s[i:i + m.end()]
    raise AssertionError("panel close not found")
FACTS_PANEL = _panel(_grow)

def esc(x): return html.escape(str(x), quote=False)

BASE_CSS = """
body{font-family:'Segoe UI',system-ui,sans-serif;background:#faf7f0;color:#1f2937;margin:0;padding:24px}
.wrap{max-width:980px;margin:0 auto} h1{text-align:center;color:#4C9A6F;margin:6px 0 2px}
.sub{text-align:center;color:#64748b;font-weight:700} h2{margin-top:26px} h3{margin-top:20px}
table{width:100%;border-collapse:collapse;font-size:.9rem} th,td{border:1px solid #e2e8f0;padding:6px 8px;text-align:left;vertical-align:top}
th{background:#f1f5f9} .bank{background:#fef9ec;border-left:5px solid #D3A03C;padding:8px 12px;border-radius:8px;font-size:.92rem}
.note{background:#eef4f0;border-radius:10px;padding:12px 16px;margin-top:20px;font-size:.92rem}
ul{margin:6px 0 0 18px}
.lane-E3{border-left:6px solid #4C9A6F} .lane-L1{border-left:6px solid #4A6FA5} .lane-L2{border-left:6px solid #96603C}
.milestone{background:#eef4f0;font-weight:700}
.safebox{background:#fdf2f2;border:2px solid #b91c1c;border-left:8px solid #b91c1c;border-radius:8px;padding:10px 14px;margin:14px 0;font-size:.92rem}
.sheet{page-break-after:always;border:1px solid #cbd5e1;border-radius:10px;padding:14px 18px;margin:18px 0;background:#fff}
.sigrow td{height:44px} .num{text-align:right;font-variant-numeric:tabular-nums}
@media print{body{background:#fff;padding:0}.no-print{display:none!important}.sheet{border:none;border-radius:0;margin:0;padding:0 0 18px}}
"""

def page(title, h1, sub, body, extra_css=""):
    return ("<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\">"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
            f"<title>{esc(title)}</title><style>{BASE_CSS}{extra_css}</style>"
            "<link rel=\"stylesheet\" href=\"../visual-upgrade.css\">\n</head><body><div class=\"wrap\">"
            f"<div style=\"text-align:center;margin:14px 0\">{MARK_SVG}</div>\n"
            f"<h1>{h1}</h1><p class=\"sub\">{sub}</p>\n{body}\n"
            "<p style=\"text-align:center;margin:26px 0\" class=\"no-print\"><a href=\"../GROW_ASDAN_Hub.html\">&larr; Back to the GROW ASDAN hub</a> · <a href=\"Scheme_of_Work.html\">Kitchen Programme year map</a></p>"
            "</div><script src=\"../visual-upgrade.js\" defer></script></body></html>")

def mins(m):
    return f"{m//60}:{m%60:02d}" if m else ""

# ---------------------------------------------------------------- week focus --
FOCUS = {
 1:"Kitchen induction · bench safety · knife basics — the team forms, ground rules drafted",
 2:"Team plan decided together (SMART team goals, roles, ground rules) · first cook: knife-skills plates · wellbeing knowledge layer opens",
 3:"Cook cycle: fruit platters (knife ladder) · wellbeing knowledge: the four domains (L1/L2) / factors (E3)",
 4:"Cook cycle: sandwiches for service · team roles and responsibilities live",
 5:"Cook cycle: hot drinks + a timed round · features of effective teamwork observed and logged",
 6:"Menu &amp; budget project opens — decision-making factors and tools taught · cook: simple salads",
 7:"Decision tools listed (E3) / compared (L1·L2) · cook: eggs three ways",
 8:"Decision situations: short-, medium- and long-term (L1·L2) · cook: pasta base",
 9:"Decision plans open (review point named on the plan) · the cook cycle now banks the DecMk 10-hour window · budget bands set",
 10:"Menu costing against the budget bands · cook: sauce + pasta service",
 11:"Decision tools in live use on the menu choices · cook: bake batch 1",
 12:"Menu decision made and costed · cook: menu rehearsal",
 13:"Team evaluation at the exact minima · cook: service run 1",
 14:"Decision evaluation at the exact minima · Christmas service · AWARD milestone, all lanes",
 15:"Technique ladder opens — learning plans written (review point named) · knife &rarr; heat skills",
 16:"Ladder: heat control (pan skills)",
 17:"Ladder: multi-component timing (Communication preparation co-delivered — spec pp25/54)",
 18:"Ladder review point · mid-block skill check (Communication preparation co-delivered)",
 19:"Ladder: timed plate-up · the learning 10-hour window closes",
 20:"Learning evaluation at the exact minima · ladder badge round",
 21:"Communication plans open — E3/L1 one plan · L2 TWO plans over two DIFFERENT ways",
 22:"Plans finished: purpose, audience, content, resources, audience questions · rehearsal",
 23:"Live demonstrations round 1 (presentation route) · discussion tables run",
 24:"Live demonstrations round 2 · text route: recipe/menu guides drafted",
 25:"Activities complete — text pieces finished, evidence gathered against the activity minima",
 26:"Communication evaluation · EXTENDED AWARD milestone, all lanes",
 27:"Investigation opens — a food claim chosen · thinking plans (review point named) · wellbeing plans open",
 28:"Sources gathered — credibility, accuracy and bias assessed (L2) · blind taste test designed",
 29:"Primary evidence: the blind taste test runs in the kitchen",
 30:"Investigation review point · secondary sources logged",
 31:"Findings drafted · cook: the recipe behind the claim",
 32:"Findings communicated · the thinking 10-hour window closes",
 33:"Thinking / Critical-thinking evaluations at the exact minima · summer menu planning",
 34:"Evaluations continue (lane-timed) · cook: showcase preparation",
 35:"Wellbeing plan closing weeks · showcase cook 1",
 36:"Wellbeing evaluations begin (L2 first) · portfolio assembly opens",
 37:"Wellbeing evaluations (E3 · L1) · IQA sample drawn",
 38:"Portfolio sign-off · EQA-window preparation · summer service · CERTIFICATE milestone",
}

BLOCK_OF = {}
for (b, a, z) in LED["blocks"]:
    for w in range(a, z + 1): BLOCK_OF[w] = b
DECK_OF = {d["week"]: f'{d["suite"]} PEQ {d["deck"]}' for d in LED["decks"]}

def unit_of(lane, sk): return LED["units"][lane][sk]

# ------------------------------------------------------------------ A1: SoW --
def build_sow():
    S = []
    S.append("""<div class="note"><b>The design in one paragraph.</b> The Kitchen Programme is a full 38-week year in which one mixed class cooks, plans, decides, investigates and evaluates its way through the ASDAN Personal Effectiveness Qualifications at three levels at once — the cohort at <b>Entry 3</b>, a small group at <b>Level 1</b>, and a directed few at <b>Level 2</b>. The kitchen is the shared vehicle (spec &sect;9 p16 explicitly permits mixed-level groups with differentiated demand): an E3 pupil, an L1 pupil and an L2 pupil cook in the same session and bank TmWkSkE3, TmWkSk1 and TmWkSk2 respectively — one level per skill per qualification (barred combinations, &sect;6.5), carried by the witness sheet's Level tick and the per-level minima on the evidence sheets. Every surface says <b>working towards</b>: registration and unit/level attribution are centre-coordinator decisions, and nothing on these pages promises a certificate. Food content is cooking skill, budget, teamwork and enjoyment — no diet, calorie, weight or body framing anywhere in this programme.</div>""")

    # the honest GLH statement + method
    S.append(f"""<h2>The hours, stated honestly</h2>
<p class="bank"><b>The live 12-week deck suite is the knowledge-and-assessment spine, not the hours.</b> Measured, it contributes <b>8.0 GLH</b>: {esc(LED["deck_method"])} Against that: ComSkE3 alone is <b>30 GLH</b>, and the smallest qualification (the E3 Award) is <b>40 GLH</b>. The guided hours therefore come from the planned year — the kitchen practicals, the challenge blocks, supervised tutor-time application — because GLH counts <em>any</em> taught or supervised time toward the unit, including assessment by the centre assessor (spec &sect;9 p16, &sect;5.1 p9).</p>
<p><b>Weekly PEQ hours are an owner input — still, and now labelled as one.</b> This map is worked at <b>3.5 supervised hours per week</b> (one classroom session + one kitchen practical), i.e. 3.5 &times; 38 = <b>133 physical GLH</b> per lane. A pass was run to replace that input with a rate <em>measured</em> from the school's own timetable, and it <b>stopped rather than guess</b>. What it established: the estate's period unit is <b>40 minutes</b> (fifteen agreeing statements across all three lanes) and BUILD runs <b>six discrete weekly slots at one period each</b> beside its PEQ row — which bounds BUILD's PEQ time at <b>0.67 to 4.67 hours a week</b> but does not fix a single figure. What it could not establish: how many of those six slots may bank an hour to PEQ <em>as well as</em> to their own ASDAN short course (that needs the member-gated PEQ delivery guide, or the coordinator); GROW's ASDAN row, which is empty in all eight built weeks; LAUNCH's weekly planners, which disagree with one another; and spring and summer term dates, which are nowhere in the estate. Full record: <code>_passpq/DERIVATION_YEAR1.md</code>.</p>
<div class="safebox"><b>Read this before setting the timetable.</b> 3.5 hours a week is <b>5.25 forty-minute periods</b> — the one rate in the table below that is <em>not</em> a whole number of the school's actual periods, and the exact point at which the Entry&nbsp;3 and Level&nbsp;1 Certificates flip from out-of-reach to reachable. At <b>five</b> whole periods (3.33 h/wk) the honest answer for those two lanes is the <b>Extended Award</b>, not the Certificate. At <b>six</b> (4.0 h/wk) all three Certificates are reachable with slack and the co-delivery claim can be dropped entirely. <b>The timetabling decision is therefore five periods or six, and it decides the qualification.</b></div>
<p>The E3 Certificate (134 qual-GLH; 140 unit-GLH) needs &asymp;3.5 supervised hours per week for the whole year with zero slack: at that rate the six-unit ledger only closes because <b>7 hours are co-delivered</b> (one supervised session banked to two units, declared week by week below). That is grounded in the spec's own model — Communication evidence is <em>expected</em> to be generated through a challenge that leads to another unit (pp25/54), ASDAN's worked assessment plan co-assesses two units in the same weekly activity, and ASDAN's own E3 Certificate GLH (134) already sits below the six-unit sum (140), netting the overlap out. <b>At six periods a week that claim is unnecessary and should be withdrawn</b> — the honest number, not the convenient one.</p>""")

    # sensitivity table
    rows = []
    for cell in LED["sensitivity"]:
        for i, lane in enumerate(LANES):
            quals = cell["lanes"][lane]
            cells = "".join(
                f"<td>{'&#9745; yes' if q['ok'] else '&#9746; no — short ' + ('%g' % q['short_h']) + ' h'}</td>"
                for q in quals)
            slot_txt = ("%g" % cell["slots"]) + (" &times; 40 min" if cell["whole_periods"]
                        else " &times; 40 min <b>(not a whole period)</b>")
            mark = " class=\"milestone\"" if cell.get("owner_input") else ""
            first = (f"<td rowspan=\"3\"{mark}><b>{'%g' % cell['hpw']} h/wk</b><br>"
                     f"<span style=\"font-size:.82rem;color:#475569\">{slot_txt}</span>"
                     + ("<br><b style=\"font-size:.82rem\">&#9432; the declared owner input</b>" if cell.get("owner_input") else "")
                     + f"</td><td rowspan=\"3\" class=\"num\"{mark}>{'%g' % cell['year_glh']}</td>"
                     if i == 0 else "")
            rows.append(f"<tr class=\"lane-{lane}\">{first}<td><b>{LANE_NAME[lane]}</b></td>{cells}</tr>")
    S.append(f"""<h3>Sensitivity: what each weekly commitment can honestly deliver (38 weeks)</h3>
<p style="font-size:.9rem">Re-based on the <b>measured 40-minute period</b> rather than round numbers: every row but one is a whole count of the school's real timetabled periods, across the band the timetable evidence actually supports (1&ndash;7 periods). The shaded row is the plan's declared owner input.</p>
<table><tr><th>Supervised h/wk</th><th>Year GLH</th><th>Lane</th><th>Award</th><th>Extended Award</th><th>Certificate</th></tr>
{''.join(rows)}</table>
<p style="font-size:.88rem">&#8220;Short&#8221; = the gap between the lane's unit-GLH requirement and the year's physical hours plus that lane's declared co-delivery (E3 7 h &middot; L1 2 h &middot; L2 0 h). <b>No row is marked live.</b> The weekly rate is an owner input, not a derived figure &mdash; see <code>_passpq/DERIVATION_YEAR1.md</code> for what the timetable evidence does and does not fix. The ledger below is worked at the shaded row.</p>""")

    # staged milestones
    mrows = []
    for lane in LANES:
        for m in LED["lanes"][lane]["milestones"]:
            mrows.append(f"<tr class=\"lane-{lane}\"><td><b>{LANE_NAME[lane]}</b></td><td>{esc(m['qual'])}</td>"
                         f"<td class=\"num\">{m['credits']}</td><td class=\"num\">{m['unit_credits']}</td>"
                         f"<td class=\"num\">{m['qual_glh']}</td><td class=\"num\">{m['unit_glh']}</td><td><b>W{m['week']}</b></td></tr>")
    S.append(f"""<h2>Staged certification — milestones, not promises</h2>
<p>Each stage is <em>proven in the ledger</em>: the constituent units' GLH is fully banked by the milestone week, and the credits are stated against the rule of combination (min-at-level and max-3-adjacent hold in every row — each stage below is all-at-level). Every lane follows the same ladder: <b>Award by Christmas (W14) &rarr; Extended Award by Easter (W26) &rarr; Certificate by summer (W38)</b>, built from Decision&nbsp;making + Team&nbsp;working, then + Communication + Learning, then + Thinking/Critical&nbsp;thinking + Wellbeing.</p>
<table><tr><th>Lane</th><th>Qualification</th><th>Credits required</th><th>Credits banked</th><th>Qual GLH</th><th>Constituent unit GLH banked</th><th>By week</th></tr>
{''.join(mrows)}</table>
<p class="bank"><b>The L1 14-of-15 choice, named.</b> {esc(LED["l1_cert_choice"])}</p>
<p class="bank"><b>Thinking vs Critical thinking — the lane split.</b> The E3 and L1 lanes plan <b>ThSkE3 / ThSk1</b> (Thinking skills); only the L2 lane plans <b>CrThSk2</b> (Critical thinking skills) — the unit changes name, code and demand at Level 2 (spec pp11&ndash;13). The shared summer investigation runs at three demands: E3/L1 pupils work their Thinking plan; the L2 pupil assesses sources for credibility, accuracy and bias across &ge;2 sources, primary vs secondary (the blind taste test is the primary source).</p>""")

    # block spine
    S.append("""<h2>The six blocks — one spine, three demands</h2>
<table><tr><th>Block</th><th>Weeks</th><th>Delivers</th><th>Plan windows and review points</th></tr>
<tr><td><b>Aut1</b></td><td>W1&ndash;7</td><td>Kitchen induction · the team plan (&ge;3 SMART team goals decided <em>with</em> the team) · wellbeing knowledge layer · the live deck spine begins (LAUNCH W1&ndash;6 = Communication knowledge at every lane's demand)</td><td>Team plan opens W2 (review point W6); TmWk 10-hour window W2&rarr;W12</td></tr>
<tr><td><b>Aut2</b></td><td>W8&ndash;14</td><td>The menu &amp; budget project: decision situations (short/medium/long-term at L1·L2), tools compared (&ge;3 at L2), plans, cook cycles, both evaluations · GROW decks W2&ndash;6 · <b>Award milestone W14</b></td><td>Decision plan opens W9 (review point W11); window W9&rarr;W13; TmWk evaluation W13&ndash;14, DecMk evaluation W14</td></tr>
<tr><td><b>Spr1</b></td><td>W15&ndash;20</td><td>The technique ladder — a named kitchen skill improved over the block; learning plans, barriers, ways of improving compared (L1·L2)</td><td>Learning plan opens W15 (review point W18); window W15&rarr;W19; evaluation W20</td></tr>
<tr><td><b>Spr2</b></td><td>W21&ndash;26</td><td>Communication at full GLH: plans (E3/L1 one · <b>L2 two, over two different ways</b>), live demonstrations, discussion tables and written recipe/menu guides at the activity minima · <b>Extended Award milestone W26</b></td><td>No 10-hour window on Communication at any level — activity minima instead: E3 &ge;2&nbsp;min / &ge;5&nbsp;min / &ge;100 words · L1 &ge;3&nbsp;min / &ge;8&nbsp;min / &ge;250 words · L2 &ge;4&nbsp;min / &ge;10&nbsp;min / &ge;500 words · evaluation W26</td></tr>
<tr><td><b>Sum1</b></td><td>W27&ndash;32</td><td>The food-claim investigation (Thinking at E3/L1 · Critical thinking at L2: &ge;2 sources, credibility/accuracy/bias, primary = own blind taste test) · wellbeing plans open and run through the learning weeks</td><td>Thinking plan opens W27 (review point W30), window W27&rarr;W32 · Wellbeing plan opens W27 (review point W32), window W27&rarr;W36</td></tr>
<tr><td><b>Sum2</b></td><td>W33&ndash;38</td><td>Evaluations at the exact minima, portfolio assembly, IQA sample, EQA-window preparation, summer service · <b>Certificate milestone W38</b></td><td>Wellbeing evaluations W36&ndash;37; portfolio sign-off W38</td></tr></table>
<p style="font-size:.88rem">Every plan opens early enough that its 10-hour window closes with headroom before its evaluation week (the ledger below carries the minutes); every review point has a named week; every assessment criterion lands on a week in the <a href="Criteria_Coverage_Matrix.html">coverage matrix</a>.</p>""")

    # per-lane weekly ledgers
    S.append("""<h2>The GLH ledger — every week &times; lane, minutes per unit</h2>
<p>Times are <b>h:mm of supervised time</b> attributed per unit (spec &sect;9 p16). <b>Physical</b> is the timetabled 3:30. A <b>co-delivered</b> entry is the same physical session banked to a second unit, declared here and justified above; the unit columns include it, the physical column does not. <b>QA</b> is supervised portfolio/IQA/EQA time not attributed to a unit (L2 lane headroom).</p>""")
    for lane in LANES:
        L = LED["lanes"][lane]
        head = ("<tr><th>Wk</th><th>Blk</th><th>Live deck</th><th>Focus (shared vehicle)</th>"
                + "".join(f"<th>{unit_of(lane, sk)['code']}</th>" for sk in SKILLS)
                + "<th>QA</th><th>Co-delivered</th><th>Physical</th></tr>")
        body = []
        for i in range(LED["weeks"]):
            w = i + 1; r = L["rows"][i]; c = L["co"][i]
            cells = []
            for sk in SKILLS:
                v = r.get(sk, 0); cv = c.get(sk, 0)
                cells.append(f"<td class=\"num\">{mins(v + cv)}{'&#8853;' if cv else ''}</td>")
            co_txt = " · ".join(f"{mins(v)} {unit_of(lane, k)['code']}" for k, v in c.items())
            cls = " class=\"milestone\"" if w in (14, 26, 38) else ""
            body.append(f"<tr{cls}><td><b>W{w}</b></td><td>{BLOCK_OF[w]}</td><td>{esc(DECK_OF.get(w,''))}</td>"
                        f"<td>{FOCUS[w]}</td>{''.join(cells)}<td class=\"num\">{mins(r.get('QA',0))}</td>"
                        f"<td>{co_txt}</td><td class=\"num\">{mins(sum(r.values()))}</td></tr>")
        tot = ("<tr><th colspan=\"4\">Ledger total (h) — must equal each unit's GLH</th>"
               + "".join(f"<th class=\"num\">{L['totals_min'][sk]//60}</th>" for sk in SKILLS)
               + f"<th class=\"num\">{L['qa_min']//60}</th><th class=\"num\">{L['co_min']//60} h</th><th class=\"num\">133</th></tr>")
        spec = ("<tr><th colspan=\"4\">Unit GLH (spec pp11&ndash;13)</th>"
                + "".join(f"<th class=\"num\">{unit_of(lane, sk)['glh']}</th>" for sk in SKILLS)
                + "<th>&mdash;</th><th>&mdash;</th><th>&mdash;</th></tr>")
        S.append(f"<h3 style=\"color:{LANE_HEX[lane]}\">{LANE_NAME[lane]} lane"
                 f"{' — the cohort' if lane=='E3' else (' — the 2&ndash;4 working above' if lane=='L1' else ' — the directed few (LAUNCH L2 route)')}</h3>"
                 f"<table>{head}{''.join(body)}{tot}{spec}</table>")
        u_rows = "".join(
            f"<tr><td>{unit_of(lane, sk)['code']}</td><td>{SKILL_NAME[sk]}</td>"
            f"<td class=\"num\">{unit_of(lane, sk)['credits']}</td><td class=\"num\">{unit_of(lane, sk)['glh']}</td>"
            f"<td class=\"num\">{L['totals_min'][sk]/60:g}</td><td>W{L['complete_week'][sk]}</td></tr>" for sk in SKILLS)
        S.append(f"<table style=\"margin-top:8px\"><tr><th>Unit</th><th>Skill</th><th>Credits</th><th>GLH</th><th>Ledger (h)</th><th>Ledger complete</th></tr>{u_rows}</table>")

    S.append("""<h2>The resource set (print-first, this folder)</h2>
<ul><li><a href="Criteria_Coverage_Matrix.html">Criteria coverage matrix</a> — every AC of all 18 units &#8614; week + artefact (zero gaps, proven at build)</li>
<li><a href="Plan_Templates.html">Plan templates</a> — six skills &times; three levels, level-correct elements (E3 without review points; L1/L2 with)</li>
<li><a href="Evidence_Sheets.html">Portfolio evidence sheets</a> — per unit per level, assessor/learner/date + IQA sample box</li>
<li><a href="Assessor_Checklists.html">Assessor criteria checklists</a> — tick-per-AC with the lane's own minima printed</li>
<li><a href="Plan_Hours_Grid.html">Plan-hours tracking grid</a> — the five 10-hour windows, lane column</li>
<li><a href="Staff_Kitchen_Guide.html">Staff guide</a> — the Level-2 route on one page, progression ladder, budget bands, kit, safety, safeguarding</li></ul>""")
    S.append(f"""<div class="note"><b>Registration and claims stay centre-side.</b> Every pupil is <b>working towards</b> these units; the coordinator registers learners before any assessment (spec &sect;14 p20), decides unit and level attribution, and confirms names &asymp;4 weeks before the EQA sampling date. Data twin for this page (for the office): <code>_passpq/inputs/PEQ_L2K_YearPlan_2026-27.xlsx</code>, built from the same proven ledger.</div>
{FACTS_PANEL}""")
    return page("Made by Matt · GROW ASDAN · Kitchen Programme PEQ Year Map · 2026–27",
                "Kitchen Programme · PEQ Year Map &amp; Scheme of Work",
                "Full year 2026&ndash;27 · three level lanes (Entry 3 · Level 1 · Level 2) · one kitchen, one class",
                "\n".join(S))

# ------------------------------------------------------- A2: coverage matrix --
# phase -> weeks per skill (shared vehicle; lane-specific evaluation from the ledger)
KNOW_WEEKS = {"Com": "W2&ndash;3 (LAUNCH decks) · W21&ndash;22 at-level recap",
              "DecMk": "W6&ndash;8", "LSk": "W7&ndash;10 (GROW decks) · W15&ndash;16 at level",
              "TmWk": "W1&ndash;2 · W9 (GROW deck)", "Th": "W11 (GROW deck) · W27&ndash;28", "Wellb": "W2&ndash;3 · W27&ndash;28"}
PLAN_WEEKS = {"Com": "W4 (deck first pass) · W21&ndash;22", "DecMk": "W9", "LSk": "W15", "TmWk": "W2", "Th": "W27", "Wellb": "W27"}
USE_WEEKS = {"Com": "W5 (deck first pass) · W23&ndash;25", "DecMk": "W9&ndash;13", "LSk": "W15&ndash;19", "TmWk": "W2&ndash;12", "Th": "W27&ndash;32", "Wellb": "W28&ndash;36"}
ARTEFACT = {
 "Com": {"know": "LAUNCH W2/W3 worksheets + witness sheet; at-level recap sheet",
         "plan": "Communication plan template (lane copy; L2 = two plans, two different ways)",
         "use": "Delivered activity + witness sheet (timed/word-counted vs the lane's activity minima)",
         "eval": "Communication evaluation sheet at the lane's exact minima"},
 "DecMk": {"know": "Tools comparison sheet (menu &amp; budget project file)",
           "plan": "Decision plan template (lane copy)",
           "use": "Cook-cycle log + plan-hours grid (&ge;10 h window W9&rarr;W13)",
           "eval": "Decision evaluation sheet at the lane's exact minima"},
 "LSk": {"know": "GROW W1/W2/W4 worksheets + witness sheet; ways-of-learning comparison",
         "plan": "Learning plan template — the technique ladder (lane copy)",
         "use": "Technique-ladder log + plan-hours grid (&ge;10 h window W15&rarr;W19)",
         "eval": "Learning evaluation sheet at the lane's exact minima"},
 "TmWk": {"know": "Teamwork features log (induction) + GROW W3 worksheet",
          "plan": "Team plan template — decided with the team (lane copy)",
          "use": "Practical service log + plan-hours grid (&ge;10 h window W2&rarr;W12)",
          "eval": "Team evaluation sheet at the lane's exact minima"},
 "Th": {"know": "GROW W5 worksheet; investigation briefing notes",
        "plan": "Thinking / Critical-thinking plan template (lane copy; topic = a food claim)",
        "use": "Investigation file: sources log, blind-taste-test record, findings + plan-hours grid (W27&rarr;W32)",
        "eval": "Thinking evaluation sheet at the lane's exact minima"},
 "Wellb": {"know": "Wellbeing knowledge sheets (domains at L1/L2; factors, people, services)",
           "plan": "Wellbeing plan template (lane copy)",
           "use": "Plan-in-use log across the learning weeks + plan-hours grid (W28&rarr;W36)",
           "eval": "Wellbeing evaluation sheet at the lane's exact minima"},
}
UNIT_BY = {("E3", "Com"): "ComSkE3", ("E3", "DecMk"): "DecMkSkE3", ("E3", "LSk"): "LSkE3",
           ("E3", "TmWk"): "TmWkSkE3", ("E3", "Th"): "ThSkE3", ("E3", "Wellb"): "WellbLeE3",
           ("L1", "Com"): "ComSk1", ("L1", "DecMk"): "DecMkSk1", ("L1", "LSk"): "LSk1",
           ("L1", "TmWk"): "TmWkSk1", ("L1", "Th"): "ThSk1", ("L1", "Wellb"): "WellbLe1",
           ("L2", "Com"): "ComSk2", ("L2", "DecMk"): "DecMkSk2", ("L2", "LSk"): "LSk2",
           ("L2", "TmWk"): "TmWkSk2", ("L2", "Th"): "CrThSk2", ("L2", "Wellb"): "WellbLe2"}

def build_matrix():
    plant = os.environ.get("L2K_PLANT_GAP") == "1"
    S = ["""<div class="note"><b>The contract of this page.</b> Every assessment criterion of all eighteen units (six skills &times; three levels) maps to the week(s) that evidence it and the named artefact that holds the evidence. <b>A gap is a red gate</b>: the page builder refuses to emit this file if any criterion is unmapped. Criteria wording is condensed (facts with citations, spec v1.2 &sect;17); the authoritative wording is the spec and the member-gated unit assessment booklets.</div>"""]
    total = 0
    for lane in LANES:
        S.append(f"<h2 style=\"color:{LANE_HEX[lane]}\">{LANE_NAME[lane]} lane</h2>")
        for sk in SKILLS:
            code = UNIT_BY[(lane, sk)]
            u = AC[code]
            eval_wk = LED["lanes"][lane]["complete_week"][sk]
            rows = []
            acs = u["acs"][:-1] if (plant and lane == "L2" and sk == "Th") else u["acs"]
            for ac in acs:
                if ac["code"] == u.get("plan_ac"):
                    wk, art = PLAN_WEEKS[sk], ARTEFACT[sk]["plan"]
                elif ac["code"] == u.get("use_ac"):
                    wk, art = USE_WEEKS[sk], ARTEFACT[sk]["use"]
                elif ac["code"] == u.get("eval_ac"):
                    wk, art = f"W{eval_wk}", ARTEFACT[sk]["eval"]
                else:
                    wk, art = KNOW_WEEKS[sk], ARTEFACT[sk]["know"]
                assert wk and art, f"GAP: {code} {ac['code']}"
                total += 1
                sub = ("<br><span style=\"font-size:.82rem;color:#475569\">" + " · ".join(esc(x) for x in ac.get("sub", [])) + "</span>") if ac.get("sub") else ""
                mn = f"<br><b style=\"font-size:.82rem\">min: {esc(ac['min'])}</b>" if ac.get("min") else ""
                rows.append(f"<tr><td><b>{ac['code']}</b></td><td>{esc(ac['label'])}{sub}{mn}</td><td>{wk}</td><td>{art}</td></tr>")
            if plant and lane == "L2" and sk == "Th":
                raise SystemExit(f"RED GATE (planted control): {code} has unmapped criteria — matrix refused")
            notes = ("<p style=\"font-size:.85rem\">" + " · ".join(esc(n) for n in u.get("notes", [])) + "</p>") if u.get("notes") else ""
            S.append(f"<h3>{code} — {esc(u['title'])} ({u['credits']} cr / {u['glh']} GLH, spec pp{u['pages']})</h3>"
                     f"<table><tr><th>AC</th><th>Demand (condensed) + minima</th><th>Week(s)</th><th>Artefact</th></tr>{''.join(rows)}</table>{notes}")
    S.append(f"<div class=\"note\"><b>Coverage proven at build time:</b> {total} criteria mapped, 0 gaps. "
             "Rebuild check: <code>python3 _passpq/tools/l2k_build.py</code>; planted-gap control: "
             "<code>L2K_PLANT_GAP=1</code> makes the same build refuse (red).</div>")
    assert total == sum(len(AC[UNIT_BY[(l, s)]]["acs"]) for l in LANES for s in SKILLS), "matrix count drift"
    return page("Made by Matt · GROW ASDAN · Kitchen Programme PEQ Criteria Coverage Matrix",
                "Kitchen Programme · Criteria Coverage Matrix",
                "Every assessment criterion &#8614; week(s) + artefact · Entry 3 · Level 1 · Level 2",
                "\n".join(S))

# ------------------------------------------------- A3: plan templates ---------
def sig_block(iqa=False):
    iqarow = ("<tr><td colspan=\"2\" style=\"height:52px\"><b>IQA sample box</b> (where sampled — spec &sect;10/&sect;11): IQA name · signature · date · sampling decision</td></tr>" if iqa else "")
    return ("<table class=\"sigrow\" style=\"margin-top:10px\"><tr><td style=\"width:50%\">Learner name + signature · date</td>"
            "<td>Assessor name + signature · date</td></tr>" + iqarow + "</table>")

def build_templates():
    S = ["""<div class="note no-print"><b>How to use.</b> One template per skill per level lane. Print the lane's copy — the required elements differ by level and are printed on the sheet: <b>Entry 3 plans carry NO review point</b>; Level 1 and Level 2 plans carry one (spec &sect;17 — verified per unit). Communication is the exception twice over: no 10-hour window at any level (activity minima instead), and at <b>Level 2 a pupil needs TWO plans over two DIFFERENT ways of communicating</b> — print the L2 communication sheet twice. Plans that carry a 10-hour window log their hours on the <a href="Plan_Hours_Grid.html">plan-hours grid</a>.</div>"""]
    for lane in LANES:
        S.append(f"<h2 style=\"color:{LANE_HEX[lane]}\">{LANE_NAME[lane]} plan templates</h2>")
        for sk in SKILLS:
            code = UNIT_BY[(lane, sk)]
            u = AC[code]
            pac = next(a for a in u["acs"] if a["code"] == u["plan_ac"])
            elems = "".join(f"<tr><td style=\"width:34%\"><b>{esc(e)}</b></td><td style=\"height:52px\"></td></tr>" for e in pac.get("sub", []))
            mn = f"<p class=\"bank\"><b>Minima on this plan:</b> {esc(pac['min'])}</p>" if pac.get("min") else ""
            if u["ten_hour"]:
                use_line = "<p><b>Use of the plan:</b> a minimum of <b>10 hours</b> — tracked on the plan-hours grid (lane column ticked)."
            else:
                use_line = f"<p><b>Use of the plan:</b> no 10-hour window on Communication — activity minima instead: <b>{esc(LED['com_activity'][lane])}</b>.</p>"
            rp = ("" if u["review_point_in_plan"] else
                  ("<p style=\"font-size:.85rem\"><b>No review point on this plan</b> — Entry 3 plans do not carry one (spec &sect;17)."
                   if lane == "E3" else "<p style=\"font-size:.85rem\"><b>No review point on the Communication plan</b> at any level (spec &sect;17).</p>"))
            two = ("<p class=\"bank\"><b>Level 2 Communication needs TWO of these sheets</b>, covering two DIFFERENT ways of communicating (2.4.1).</p>"
                   if (lane == "L2" and sk == "Com") else "")
            S.append(f"""<div class="sheet lane-{lane}"><h3>{esc(SKILL_NAME[sk])} plan — {code} ({LANE_NAME[lane]}) · working towards</h3>
<p style="font-size:.88rem">Plan criterion <b>{pac['code']}</b>: {esc(pac['label'])}. Unit: {u['credits']} cr / {u['glh']} GLH.</p>
{two}<table>{elems}</table>{mn}{use_line}{rp}
<p style="font-size:.88rem"><b>Named weeks (year map):</b> plan opens W{LED['plan_windows'].get(sk, {}).get('open', '21')} · review point W{LED['plan_windows'].get(sk, {}).get('review', '&mdash;') if u['review_point_in_plan'] else '&mdash; (none at this level)'} · window/activities close before the evaluation week.</p>
{sig_block()}</div>""")
    return page("Made by Matt · GROW ASDAN · Kitchen Programme PEQ Plan Templates",
                "Kitchen Programme · Plan Templates",
                "Print-first · level-correct required elements · Entry 3 · Level 1 · Level 2",
                "\n".join(S))

# ------------------------------------------------- A3: evidence sheets --------
def build_evidence():
    S = ["""<div class="note no-print"><b>What this is.</b> One portfolio evidence sheet per unit per level: the cover record the spec requires — explicit evidence per criterion, signed and dated by assessor and learner, IQA box where sampled (spec &sect;10 p17). The witness Level tick carries the barred-combination rule: <b>each pupil banks each skill at ONE level only</b> (&sect;6.5).</div>"""]
    for lane in LANES:
        S.append(f"<h2 style=\"color:{LANE_HEX[lane]}\">{LANE_NAME[lane]} evidence sheets</h2>")
        for sk in SKILLS:
            code = UNIT_BY[(lane, sk)]
            u = AC[code]
            rows = "".join(
                f"<tr><td>&#9744;</td><td><b>{a['code']}</b></td><td>{esc(a['label'])}"
                + (f"<br><b style=\"font-size:.82rem\">min: {esc(a['min'])}</b>" if a.get("min") else "")
                + "</td><td style=\"width:26%\"></td></tr>" for a in u["acs"])
            ticks = " &nbsp; ".join(f"&#9744;&nbsp;<b>{LANE_NAME[x]}</b>" for x in LANES)
            S.append(f"""<div class="sheet lane-{lane}"><h3>{code} — {esc(u['title'])} ({LANE_NAME[lane]}) · {u['credits']} cr / {u['glh']} GLH · working towards</h3>
<table><tr><th></th><th>AC</th><th>Criterion (condensed) + minimum</th><th>Evidence ref (portfolio)</th></tr>{rows}</table>
<p style="margin:10px 0 4px"><b>Level this evidence banks at — tick ONE:</b> &nbsp; {ticks}<br>
<span style="font-size:.8rem">A learner's evidence for a skill banks at ONE level only (barred combinations, spec v1.2 &sect;6.5). The level tick is the assessor's decision on the day, confirmed by the coordinator at claim time.</span></p>
{sig_block(iqa=True)}</div>""")
    return page("Made by Matt · GROW ASDAN · Kitchen Programme PEQ Evidence Sheets",
                "Kitchen Programme · Portfolio Evidence Sheets",
                "Per unit · per level · assessor + learner + date · IQA sample box (spec &sect;10)",
                "\n".join(S))

# ------------------------------------------------- A3: assessor checklists ----
def build_checklists():
    S = ["""<div class="note no-print"><b>What this is.</b> The assessor's tick-per-criterion working checklist, with every printed minimum at the lane's own level — an Entry 3 surface carries Entry 3 minima only, a Level 1 surface Level 1 minima only, a Level 2 surface Level 2 minima only (the cross-level gate reds otherwise). 'Plural' = at least 2 · 'Range' = at least 3 unless a criterion states otherwise (every unit's requirements page).</div>"""]
    for lane in LANES:
        S.append(f"<h2 style=\"color:{LANE_HEX[lane]}\">{LANE_NAME[lane]} assessor checklists</h2>")
        for sk in SKILLS:
            code = UNIT_BY[(lane, sk)]
            u = AC[code]
            rows = "".join(
                f"<tr><td><b>{a['code']}</b></td><td>{esc(a['label'])}"
                + (("<br><span style=\"font-size:.82rem;color:#475569\">" + " · ".join(esc(x) for x in a["sub"]) + "</span>") if a.get("sub") else "")
                + "</td><td>" + (f"<b>{esc(a['min'])}</b>" if a.get("min") else "&mdash;")
                + "</td><td style=\"width:8%\">&#9744;</td><td style=\"width:14%\"></td></tr>" for a in u["acs"])
            notes = ("<p style=\"font-size:.85rem\">" + " · ".join(esc(n) for n in u.get("notes", [])) + "</p>") if u.get("notes") else ""
            S.append(f"""<div class="sheet lane-{lane}"><h3>Assessor checklist — {code} ({LANE_NAME[lane]})</h3>
<table><tr><th>AC</th><th>Criterion (condensed)</th><th>Minimum</th><th>Met</th><th>Date / initials</th></tr>{rows}</table>{notes}</div>""")
    return page("Made by Matt · GROW ASDAN · Kitchen Programme PEQ Assessor Checklists",
                "Kitchen Programme · Assessor Criteria Checklists",
                "Tick-per-criterion · minima printed at the lane's own level",
                "\n".join(S))

# ------------------------------------------------- A3: plan-hours grid --------
def build_grid():
    S = ["""<div class="note no-print"><b>What this is.</b> The tracking grid for the five 10-hour plan-use windows (Decision making · Learning · Team working · Thinking/Critical thinking · Wellbeing — Communication has no window at any level; its activity minima are recorded on the witness sheet instead). One row per supervised session. <b>The lane column is part of the record</b>: a session can serve all three lanes at once; each pupil's grid still shows their own lane. Windows overlap (PEQ002 model) — one cook cycle can log against two open windows where both plans are genuinely in use, matching the declared co-delivery in the year map.</div>"""]
    wins = "".join(
        f"<tr><td><b>{SKILL_NAME[sk]}</b></td><td>W{v['open']}</td><td>W{v['review']}</td><td>W{v['close']}</td><td class=\"num\">600 min</td></tr>"
        for sk, v in LED["plan_windows"].items())
    S.append(f"<h2>The five windows (year-map weeks)</h2><table><tr><th>Skill</th><th>Plan opens</th><th>Review point (L1·L2 plans)</th><th>Window closes</th><th>Target</th></tr>{wins}</table>")
    rows = "".join("<tr><td style=\"height:34px\"></td><td></td><td></td><td>&#9744; E3 &nbsp;&#9744; L1 &nbsp;&#9744; L2</td><td></td><td></td><td></td></tr>" for _ in range(18))
    S.append(f"""<h2>Session log (print one per pupil per window)</h2>
<div class="sheet"><p><b>Pupil (working towards):</b> ______________________ &nbsp; <b>Unit:</b> ______________ &nbsp; <b>Plan opened (date):</b> __________</p>
<table><tr><th>Date</th><th>Week</th><th>Session / activity</th><th>Lane</th><th>Minutes</th><th>Running total</th><th>Staff initials</th></tr>{rows}</table>
<p style="font-size:.88rem"><b>Window closed at &ge;600 minutes:</b> date __________ · assessor initials ______ · carried to the unit's evidence sheet.</p></div>""")
    return page("Made by Matt · GROW ASDAN · Kitchen Programme PEQ Plan-Hours Grid",
                "Kitchen Programme · Plan-Hours Tracking Grid",
                "The 10-hour windows · lane column · one row per supervised session",
                "\n".join(S))

# ------------------------------------------------- A3: staff kitchen guide ----
def build_staff():
    S = []
    S.append("""<h2>The Level-2 route, on one page</h2>
<p class="bank"><b>Who it is for.</b> A small number of pupils, directed by staff after initial assessment, working at the Level 2 evidence standard — <b>Describe / Explain / Compare / Assess / Evaluate</b>, not the Entry 3 <em>State / List / Identify</em>. Everyone else's view is unchanged: the E3 cohort and the L1 group keep their lanes. In the live LAUNCH PEQ decks the Level 2 route appears as hidden panels revealed by the <b>&#9432; Guidance</b> toggle for the pupils staff direct there; in this kitchen year it is the L2 lane of the <a href="Scheme_of_Work.html">year map</a>.</p>
<ul>
<li><b>Barred combinations (spec &sect;6.5):</b> each pupil banks each of the six skills at ONE level only — the credit from the highest-level unit counts. The witness sheet's Level tick (E3 · L1 · L2) is the record.</li>
<li><b>Sizes (spec p4/p10):</b> L2 Award 4 cr all-at-level (32 GLH) · L2 Extended Award 9 cr, min 6 at L2 (68 GLH) · L2 Certificate 15 cr, min 12 at L2, max 3 below (106 GLH). At L2 the thinking unit is <b>Critical thinking (CrThSk2)</b>, not ThSk.</li>
<li><b>Key L2 demands:</b> Communication = TWO plans over two DIFFERENT ways (presentation &ge;4 min · discussion &ge;10 min · text &ge;500 words) · Decision making = short/medium/long-term situations, &ge;3 tools COMPARED · plans at L1/L2 carry review points (never at E3) · five of six units carry the 10-hour plan-use window (never Communication) · Critical thinking = credibility/accuracy/bias across &ge;2 sources, primary vs secondary.</li>
<li><b>Wording:</b> every surface says <b>working towards</b>. No deck or sheet claims a pupil is registered or will certificate — registration, unit and level attribution are the coordinator's decisions (spec &sect;14 p20).</li>
</ul>""")
    S.append("""<h2>Kitchen progression ladder</h2>
<table><tr><th>Rung</th><th>Skills</th><th>Typical dishes</th><th>Year-map weeks</th></tr>
<tr><td><b>1 · Knife</b></td><td>Grip, bridge and claw cuts, board hygiene</td><td>Fruit platters, salads, sandwiches</td><td>W1&ndash;6</td></tr>
<tr><td><b>2 · Heat</b></td><td>Pan control, boiling, toasting, oven safety</td><td>Eggs three ways, pasta base, bakes</td><td>W7&ndash;16</td></tr>
<tr><td><b>3 · Multi-component</b></td><td>Timing two elements to land together</td><td>Sauce + pasta, plated mains</td><td>W17&ndash;25</td></tr>
<tr><td><b>4 · Timed service</b></td><td>Service under the clock, plating, front-of-house</td><td>Christmas service, showcase, summer service</td><td>W13&ndash;14 · W26&ndash;38</td></tr></table>
<h2>Budget framework bands</h2>
<table><tr><th>Band</th><th>Per head</th><th>Used for</th></tr>
<tr><td>A — practice</td><td>low</td><td>Weekly cook cycles, single-component dishes</td></tr>
<tr><td>B — project</td><td>medium</td><td>The menu &amp; budget project (Aut2): costing against a set band is the decision-making evidence</td></tr>
<tr><td>C — service</td><td>agreed per event</td><td>Christmas service · showcase · summer service</td></tr></table>
<p style="font-size:.88rem">Bands are set by the school office each term; the pupils' work is choosing, costing and justifying within the band — the numbers themselves are a school decision, not part of this page.</p>
<h2>Kit list</h2>
<ul><li>Colour-coded boards + bench mats · knife set (school-held, signed in/out) · peelers, graters, measuring sets</li>
<li>Pans, baking trays, mixing bowls · oven gloves, aprons, blue plasters, first-aid point</li>
<li>Timers (one per team) · plate stock for service · cleaning caddies per bench</li>
<li>Print stock: plan templates, evidence sheets, plan-hours grids, witness sheets (this folder)</li></ul>""")
    S.append("""<h2>Staff safety page</h2>
<div class="note"><b>Supervised bench, always.</b> Every practical runs as a <b>supervised bench</b>: a trained member of staff at the bench for any knife or heat work, ratios per the school's own policy. The kitchen <b>risk assessment is named school-side</b> — it is the school's document, owned and reviewed by the school, and this programme runs inside it; nothing on these pages replaces it. Allergen and dietary-requirement checks are the school's standing process and happen before any menu is cooked. Food content across the programme is <b>cooking skill, budget, teamwork and enjoyment</b> — no diet, calorie, weight or body framing on any pupil surface.</div>
<div class="safebox"><b>Safeguarding — Decision making (spec p57, and pp27/41 at E3/L1).</b> When pupils identify decision-making situations, steer them to situations that do not negatively impact their wellbeing. If a pupil identifies a situation raising a potential safeguarding concern, it is managed through the school's safeguarding processes — <b>and this is communicated to the pupils as part of the session</b>, before the activity runs. This box is read aloud, in pupil-appropriate words, when the decision plans open (year-map W9).</div>
<div class="safebox"><b>Safeguarding — Wellbeing in learning (spec p66, and pp35/50 at E3/L1).</b> When pupils plan ways to improve their own wellbeing while learning, they may disclose issues that negatively impact their wellbeing. Any disclosure raising a potential safeguarding concern is managed through the school's safeguarding processes — <b>and this is communicated to the pupils as part of the session</b>, before the discussion opens. This box is read aloud, in pupil-appropriate words, when the wellbeing plans open (year-map W27).</div>""")
    S.append(FACTS_PANEL)
    return page("Made by Matt · GROW ASDAN · Kitchen Programme Staff Guide",
                "Kitchen Programme · Staff Guide",
                "The Level-2 route · progression ladder · budget bands · kit · safety · safeguarding",
                "\n".join(S))


# ============================================================ PEQ-YEAR-1 §4 ====
# The colleague's cooking frame. FRAME ONLY: these four pages carry no dish, no
# recipe, no menu and no ingredient. The "what we're cooking" box is left empty
# on purpose - it is hers to fill. Enforced by _passpq/tools/food_gate.py, which
# goes red if a dish name appears on any of them.

WEEK_RE = re.compile(r'W(\d+)(?:\s*(?:&ndash;|&#8211;|-|–)\s*(\d+))?')

def weeks_of(expr):
    """Turn a matrix week-expression ('W9&ndash;13', 'W4 (deck first pass) · W21&ndash;22')
    into the set of week numbers it covers. Used to invert the matrix by week."""
    out = set()
    for m in WEEK_RE.finditer(expr or ""):
        a = int(m.group(1)); b = int(m.group(2)) if m.group(2) else a
        if b < a: a, b = b, a
        out |= set(range(a, min(b, LED["weeks"]) + 1))
    return out

def criteria_by_week():
    """week -> lane -> [(unit code, AC code, demand, artefact, stage)] — inverted
    from exactly the same mapping the coverage matrix is built from, so the two
    pages can never drift."""
    idx = {w: {l: [] for l in LANES} for w in range(1, LED["weeks"] + 1)}
    for lane in LANES:
        for sk in SKILLS:
            code = UNIT_BY[(lane, sk)]
            u = AC[code]
            eval_wk = LED["lanes"][lane]["complete_week"][sk]
            for ac in u["acs"]:
                if ac["code"] == u.get("plan_ac"):
                    expr, art, stage = PLAN_WEEKS[sk], ARTEFACT[sk]["plan"], "plan"
                elif ac["code"] == u.get("use_ac"):
                    expr, art, stage = USE_WEEKS[sk], ARTEFACT[sk]["use"], "use"
                elif ac["code"] == u.get("eval_ac"):
                    expr, art, stage = f"W{eval_wk}", ARTEFACT[sk]["eval"], "evaluate"
                else:
                    expr, art, stage = KNOW_WEEKS[sk], ARTEFACT[sk]["know"], "know"
                for w in weeks_of(expr):
                    idx[w][lane].append((code, ac["code"], ac["label"], art, stage,
                                         ac.get("min")))
    return idx

def _events_due(w):
    """Plan opens, review points and evaluation weeks falling in week w."""
    ev = []
    for sk, win in LED["plan_windows"].items():
        if win["open"] == w:   ev.append(f"<b>{SKILL_NAME[sk]}</b> plan opens (10-hour window to W{win['close']})")
        if win["review"] == w: ev.append(f"<b>{SKILL_NAME[sk]}</b> plan <b>review point</b> (Level 1 &amp; Level 2 only &mdash; Entry 3 plans carry none)")
        if win["close"] == w:  ev.append(f"<b>{SKILL_NAME[sk]}</b> 10-hour window closes &mdash; hours must be logged")
    ca = LED["com_activity"]
    if w in ca["plan_weeks"]:     ev.append("<b>Communication</b> plan written (L2: <b>two</b> plans, two different ways)")
    if w in range(ca["activity_weeks"][0], ca["activity_weeks"][1] + 1):
        ev.append("<b>Communication</b> activity delivered &mdash; time it / count the words against the lane minima")
    if w == ca["eval_week"]:      ev.append("<b>Communication</b> evaluation")
    for lane in LANES:
        for sk in SKILLS:
            if LED["lanes"][lane]["complete_week"][sk] == w:
                ev.append(f"{LANE_NAME[lane]}: <b>{UNIT_BY[(lane, sk)]}</b> evaluation &amp; unit sign-off")
    for lane in LANES:
        for m in LED["lanes"][lane]["milestones"]:
            if m["week"] == w:
                ev.append(f"<b>MILESTONE</b> &mdash; {LANE_NAME[lane]}: {m['qual']} ({m['credits']} cr)")
    return ev

HARD_RULES_HTML = """<div class="safebox"><b>The five rules that do not bend.</b>
<ol style="margin:6px 0 0 18px">
<li><b>Supervised bench, always.</b> A trained adult at the bench for any knife or heat work,
ratios per the school's own policy. The kitchen <b>risk assessment is the school's document</b>
&mdash; this programme runs inside it and nothing here replaces it. Allergen and
dietary-requirement checks are the school's standing process and happen <b>before</b> any
cooking is planned.</li>
<li><b>No diet, calorie, weight or body framing.</b> Anywhere, on any surface a pupil sees.
The food content of this programme is <b>cooking skill, budget, teamwork and enjoyment</b>.
This is not a style preference; it is a safeguarding rule for this cohort.</li>
<li><b>Pupil names never enter the repository.</b> Named registers, photos with faces, and
anything identifying stay on the school network. Repository copies use Pupil&nbsp;A&ndash;D.</li>
<li><b>Evidence is signed and dated</b> by <b>both</b> assessor and learner (spec &sect;10 p17),
with the IQA box completed where the piece is sampled. An unsigned sheet is not evidence.</li>
<li><b>Every surface says &ldquo;working towards&rdquo;.</b> A pupil has not achieved a unit
until it is assessed, internally quality-assured and EQA-sampled. Nothing you write may promise
a certificate.</li>
</ol></div>"""

def build_cooking_handover():
    S = [f"""<div class="note"><b>Who this is for.</b> This is the teacher frame for the kitchen
year &mdash; what it is for, which units each block evidences, what paperwork exists, and what is
yours to build. It deliberately contains <b>no recipes, no menus, no dishes and no ingredient
lists</b>. Those are yours: you know the kitchen, the budget and the pupils. What is provided is
everything that has to line up with the qualification, so that whatever you cook lands on a
criterion.</div>

<h2>The kitchen year in one page</h2>
<p>One mixed class, one kitchen, a full {LED["weeks"]}-week year, running the ASDAN Personal
Effectiveness Qualifications at <b>three levels at once</b> &mdash; the cohort at Entry&nbsp;3, a
small group at Level&nbsp;1, a directed few at Level&nbsp;2. Everyone cooks in the same session;
what differs is the <b>demand</b> placed on each pupil and the <b>level</b> their evidence banks
at. An Entry&nbsp;3 pupil states and lists; a Level&nbsp;1 pupil describes and explains; a
Level&nbsp;2 pupil compares, assesses and evaluates. Same bench, same task, three standards.</p>
<p>The qualification is <b>not about food</b>. It is about six personal skills &mdash;
communication, decision making, learning, team working, thinking, and wellbeing in learning
&mdash; and the kitchen is simply the vehicle that generates honest evidence of them. That is
why this pack can hand you the criteria without handing you a menu: <b>what</b> you cook is
yours; <b>what it has to prove</b> is fixed.</p>
{HARD_RULES_HTML}

<h2>Which block evidences what</h2>
<table><tr><th>Block</th><th>Weeks</th><th>Skill in focus</th><th>Unit banked, per lane</th></tr>"""]
    order = [("TmWk", "Team working"), ("DecMk", "Decision making"), ("LSk", "Learning"),
             ("Com", "Communication"), ("Th", "Thinking / Critical thinking"),
             ("Wellb", "Wellbeing in learning")]
    for (b, a, z) in LED["blocks"]:
        focus = []
        for sk, name in order:
            mins_in = sum(sum(v for k, v in LED["lanes"]["E3"]["rows"][w - 1].items() if k == sk)
                          for w in range(a, z + 1))
            if mins_in: focus.append((mins_in, sk, name))
        focus.sort(reverse=True)
        if not focus: continue
        _, sk, name = focus[0]
        units = " &middot; ".join(f"{LANE_NAME[l]} <b>{UNIT_BY[(l, sk)]}</b>" for l in LANES)
        S.append(f"<tr><td><b>{b}</b></td><td>W{a}&ndash;{z}</td><td>{name}</td><td>{units}</td></tr>")
    S.append("</table>")
    S.append(f"""<p style="font-size:.88rem">The full week-by-week ledger is on the
<a href="Scheme_of_Work.html">year map</a>; every individual criterion is on the
<a href="Criteria_Coverage_Matrix.html">coverage matrix</a>, and the same mapping inverted
week-by-week is on <a href="Criteria_By_Week.html">what each week must produce</a>.</p>

<h2>What is already provided &mdash; you should not rebuild any of this</h2>
<table><tr><th>Sheet</th><th>What it does</th></tr>
<tr><td><a href="Kitchen_Week_Shell.html">Week shells</a></td><td>One printable page per week, pre-filled with the block, the units and the exact criteria due that week, the plan and review-point events, and the artefacts to collect &mdash; with a <b>blank box for what you are cooking</b>.</td></tr>
<tr><td><a href="Criteria_By_Week.html">Criteria by week</a></td><td>The coverage matrix inverted: for any week, what each lane must produce.</td></tr>
<tr><td><a href="Kitchen_Completion_Checklist.html">Completion checklist</a></td><td>A weekly tick sheet &mdash; evidence collected, sheets signed, plan hours logged.</td></tr>
<tr><td><a href="Plan_Templates.html">Plan templates</a></td><td>Six skills &times; three levels, level-correct (Entry&nbsp;3 plans carry <b>no</b> review point; L1 and L2 do).</td></tr>
<tr><td><a href="Evidence_Sheets.html">Evidence sheets</a></td><td>Per unit per level, with assessor / learner / date and the IQA sample box.</td></tr>
<tr><td><a href="Assessor_Checklists.html">Assessor checklists</a></td><td>Tick-per-criterion, with the lane's own minima printed on the sheet.</td></tr>
<tr><td><a href="Plan_Hours_Grid.html">Plan-hours grid</a></td><td>The five 10-hour windows, per lane.</td></tr>
<tr><td><a href="Staff_Kitchen_Guide.html">Staff guide</a></td><td>Progression ladder, budget bands, kit list, safety and safeguarding.</td></tr></table>

<h2>What is yours to produce</h2>
<p>Everything about the food, and nothing about the qualification:</p>
<ul>
<li><b>What is cooked each week</b> &mdash; dishes, recipes, menus, ingredient and shopping
lists, quantities, substitutions.</li>
<li><b>The practical demonstrations</b> and how techniques are modelled and sequenced.</li>
<li><b>Ordering and the budget within the band</b> the office sets each term.</li>
<li><b>Which pupils work at which bench</b>, and the pairings that work in your room.</li>
</ul>
<p class="bank"><b>The one thing to hold on to when you plan a week:</b> pick the food first if
that is how you think &mdash; then open that week's shell and check the criteria it has to
carry. If a criterion has no natural home in what you have chosen, change the task slightly
rather than the criterion. The criteria are fixed by the awarding body; the food is not.</p>

<h2>Where to ask</h2>
<p>Anything about <b>criteria wording, levels, minima, plans or evidence</b> &mdash; the
<a href="Criteria_Coverage_Matrix.html">coverage matrix</a> first, then the course coordinator.
Anything about <b>registration, unit entry or claims</b> &mdash; the coordinator; those are
settled centre-side and are not decisions you need to make. Anything about <b>kitchen safety,
allergens or the risk assessment</b> &mdash; the school's own policy and the Head of School.</p>""")
    S.append(FACTS_PANEL)
    return page("Made by Matt · GROW ASDAN · Kitchen Programme · Cooking Handover",
                "Kitchen Programme &middot; Cooking Handover",
                "The teacher frame &mdash; what is provided, what is yours, and the rules that do not bend",
                "\n".join(S))

def build_week_shell():
    idx = criteria_by_week()
    S = ["""<div class="note no-print"><b>How to use.</b> One page per week. The left column is
fixed by the qualification &mdash; block, units, criteria, events, artefacts. The
<b>&ldquo;What we are cooking&rdquo;</b> box is deliberately empty: it is yours. Print the weeks
you need; the pages break one per sheet.</div>"""]
    for w in range(1, LED["weeks"] + 1):
        ev = _events_due(w)
        deck = DECK_OF.get(w)
        rows = []
        for lane in LANES:
            items = idx[w][lane]
            if not items: continue
            seen, bits = set(), []
            for code, ac, label, art, stage, mn in items:
                key = (code, ac)
                if key in seen: continue
                seen.add(key)
                mtxt = f' <b style="font-size:.8rem">min: {esc(mn)}</b>' if mn else ""
                bits.append(f"<b>{code}</b> {ac} <span style=\"font-size:.85rem\">({stage})</span> "
                            f"&mdash; {esc(label)}{mtxt}")
            arts = sorted({a for _, _, _, a, _, _ in items})
            rows.append(f"<tr class=\"lane-{lane}\"><td style=\"width:14%\"><b>{LANE_NAME[lane]}</b></td>"
                        f"<td>{'<br>'.join(bits)}</td>"
                        f"<td style=\"width:26%\">{'<br>'.join(arts)}</td></tr>")
        body = ("".join(rows) or
                "<tr><td colspan=\"3\"><i>No new criteria fall in this week &mdash; consolidation, "
                "gap-fill and plan hours.</i></td></tr>")
        S.append(f"""<div class="sheet">
<h2 style="margin-top:0">Week {w} &middot; {BLOCK_OF[w]}</h2>
<p class="sub" style="text-align:left;font-weight:400">
{('Live PEQ deck this week: <b>' + esc(deck) + '</b>') if deck else 'No PEQ deck this week &mdash; kitchen session and plan hours.'}</p>
<table><tr><th>Lane</th><th>Units &amp; the exact criteria due this week</th><th>Evidence to collect</th></tr>
{body}</table>
<h3>Plan &amp; review-point events due</h3>
{('<ul>' + ''.join('<li>' + e + '</li>' for e in ev) + '</ul>') if ev else '<p><i>None due this week.</i></p>'}
<h3>What we are cooking this week</h3>
<div style="border:1px dashed #94a3b8;border-radius:8px;min-height:150px;padding:10px">
<span class="no-print" style="color:#94a3b8;font-size:.85rem">&mdash; for the class teacher to complete &mdash;</span></div>
<table class="sigrow" style="margin-top:10px"><tr>
<td style="width:50%">Session led by &middot; date</td><td>Evidence collected &amp; filed &middot; initials</td></tr></table>
</div>""")
    return page("Made by Matt · GROW ASDAN · Kitchen Programme · Weekly Shells",
                "Kitchen Programme &middot; Weekly Shells",
                f"One page per week &middot; all {LED['weeks']} weeks &middot; the cooking box is yours to fill",
                "\n".join(S))

def build_criteria_by_week():
    idx = criteria_by_week()
    S = ["""<div class="note"><b>The coverage matrix, inverted.</b> The
<a href="Criteria_Coverage_Matrix.html">matrix</a> reads unit&nbsp;&#8614;&nbsp;week. This page
reads <b>week&nbsp;&#8614;&nbsp;unit</b>, per lane, so a week can be planned at a glance. Both
are generated from the same mapping in the same build, so they cannot drift apart.</div>"""]
    for lane in LANES:
        S.append(f"<h2 style=\"color:{LANE_HEX[lane]}\">{LANE_NAME[lane]} lane</h2>")
        rows = []
        for w in range(1, LED["weeks"] + 1):
            items = idx[w][lane]
            if not items:
                rows.append(f"<tr><td><b>W{w}</b></td><td>{BLOCK_OF[w]}</td>"
                            f"<td colspan=\"2\"><i>consolidation / plan hours &mdash; no new criteria</i></td></tr>")
                continue
            seen, bits = set(), []
            for code, ac, label, art, stage, mn in items:
                if (code, ac) in seen: continue
                seen.add((code, ac))
                bits.append(f"<b>{code}</b>&nbsp;{ac} <span style=\"font-size:.85rem\">({stage})</span>")
            arts = sorted({a for _, _, _, a, _, _ in items})
            cls = " class=\"milestone\"" if any(m["week"] == w for m in LED["lanes"][lane]["milestones"]) else ""
            rows.append(f"<tr{cls}><td><b>W{w}</b></td><td>{BLOCK_OF[w]}</td>"
                        f"<td>{' &middot; '.join(bits)}</td><td style=\"width:32%\">{'<br>'.join(arts)}</td></tr>")
        S.append("<table><tr><th style=\"width:7%\">Week</th><th style=\"width:9%\">Block</th>"
                 "<th>Criteria due</th><th>Evidence artefact</th></tr>" + "".join(rows) + "</table>")
    return page("Made by Matt · GROW ASDAN · Kitchen Programme · Criteria by Week",
                "Kitchen Programme &middot; Criteria by Week",
                "The coverage matrix inverted &mdash; what each week must produce, per lane",
                "\n".join(S))

def build_completion_checklist():
    S = ["""<div class="note no-print"><b>How to use.</b> One row per week. Tick as the week
closes; anything untickable is a gap to fix while the kit is still out and the pupils still
remember the session. A gap found at the audit week is a gap found too late.</div>
<table><tr><th style="width:6%">Week</th><th style="width:8%">Block</th>
<th style="width:22%">Evidence collected</th><th style="width:22%">Sheets signed (assessor + learner)</th>
<th style="width:22%">Plan hours logged</th><th>Gap / action</th></tr>"""]
    for w in range(1, LED["weeks"] + 1):
        due = [sk for sk, win in LED["plan_windows"].items() if win["open"] <= w <= win["close"]]
        hrs = (" &middot; ".join(SKILL_NAME[sk] for sk in due)) if due else "&mdash;"
        mile = any(m["week"] == w for lane in LANES for m in LED["lanes"][lane]["milestones"])
        cls = " class=\"milestone\"" if mile else ""
        S.append(f"<tr{cls}><td><b>W{w}</b></td><td>{BLOCK_OF[w]}</td>"
                 f"<td>&#9744;</td><td>&#9744;</td><td>&#9744; <span style=\"font-size:.8rem\">{hrs}</span></td><td></td></tr>")
    S.append("""</table>
<p style="font-size:.88rem">&ldquo;Plan hours logged&rdquo; names the 10-hour windows open that
week &mdash; the hours go on the <a href="Plan_Hours_Grid.html">plan-hours grid</a>, not here;
this column only records that it was done. Shaded rows are qualification milestones.
Communication carries <b>no</b> 10-hour window at any level &mdash; it has activity minima
instead, printed on the <a href="Assessor_Checklists.html">assessor checklists</a>.</p>""")
    S.append(FACTS_PANEL)
    return page("Made by Matt · GROW ASDAN · Kitchen Programme · Weekly Completion Checklist",
                "Kitchen Programme &middot; Weekly Completion Checklist",
                "Evidence collected &middot; sheets signed &middot; plan hours logged",
                "\n".join(S))


def main():
    os.makedirs(OUT, exist_ok=True)
    pages = {
        "Scheme_of_Work.html": build_sow(),
        "Criteria_Coverage_Matrix.html": build_matrix(),
        "Plan_Templates.html": build_templates(),
        "Evidence_Sheets.html": build_evidence(),
        "Assessor_Checklists.html": build_checklists(),
        "Plan_Hours_Grid.html": build_grid(),
        "Staff_Kitchen_Guide.html": build_staff(),
        # PEQ-YEAR-1 §4 — the colleague's cooking frame (frame only, zero cooking content)
        "Cooking_Handover.html": build_cooking_handover(),
        "Kitchen_Week_Shell.html": build_week_shell(),
        "Criteria_By_Week.html": build_criteria_by_week(),
        "Kitchen_Completion_Checklist.html": build_completion_checklist(),
    }
    for name, content in pages.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"wrote {name} ({len(content)} bytes)")

if __name__ == "__main__":
    main()
