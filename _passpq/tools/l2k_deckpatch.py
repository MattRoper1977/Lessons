#!/usr/bin/env python3
# l2k_deckpatch.py — pass PEQ-L2K Deliverable B: the Level 2 route inside the six
# live LAUNCH PEQ decks (LAUNCH_ASDAN/PEQ/PEQ_W*.html — LAUNCH ONLY; GROW stays E3/L1).
#
#   python3 _passpq/tools/l2k_deckpatch.py patch     # apply (idempotent: re-run = no-op)
#   python3 _passpq/tools/l2k_deckpatch.py strip     # exact inverse (reversibility gate)
#   python3 _passpq/tools/l2k_deckpatch.py verify    # count panels/markers per deck
#
# What patch does, per deck — the ruled, named exception to PEQ-E3's L2 removal
# (owner ruling 2026-08-21, scoped to the LAUNCH suite only):
#  1. one Level-2 route panel on the Independent Work slide, data-mbm-guide="1"
#     (hidden by default, revealed by the existing (i) Guidance toggle, persistence
#     key mbm_guide_v1) + data-speak-text; content = the L2 verb form of the task
#     + its ComSk2 minima from SPEC_FACTS_L2;
#  2. a print mirror (#print-l2route) that prints ONLY while the route toggle is on,
#     so the three standard print packs stay text-identical bar the ruled strings;
#  3. the ruled banking strings:  "PEQ Entry 3 (Level 1 stretch)" ->
#     "PEQ Entry 3 (Level 1 · Level 2 routes)"  and  "(ComSkE3 · ComSk1 (stretch)"
#     -> "(ComSkE3 · ComSk1 · ComSk2 routes"  (+ the W1 "begins" variants);
#  4. the witness sheet Level tick gains Level 2, and the tick guidance sentence
#     is extended (the one non-additive word: "never both" -> "never more than one",
#     recorded in DECISIONS_L2K — three levels made the two-level wording false).
# Existing tier content untouched. Engine/rules untouched. All edits string-anchored.

import os, re, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DIR = os.path.join(ROOT, "LAUNCH_ASDAN", "PEQ")
DECKS = ["PEQ_W1_Intro_and_Choosing_My_Level.html", "PEQ_W2_What_Makes_Communication_Effective.html",
         "PEQ_W3_Active_Listening_and_Giving_Feedback.html", "PEQ_W4_Plan_a_Communication_Activity.html",
         "PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html", "PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html"]

# --- ruled banking-string replacements (anchored, exact) ---------------------
BANKING = [
 ("PEQ Entry 3 (Level 1 stretch)", "PEQ Entry 3 (Level 1 · Level 2 routes)"),
 ("(ComSkE3 · ComSk1 (stretch)", "(ComSkE3 · ComSk1 · ComSk2 routes"),
 ("ComSkE3 · ComSk1 (stretch), begins", "ComSkE3 · ComSk1 · ComSk2 routes, begins"),
 ("(Communication, ComSk1, begins)", "(Communication, ComSk1 · ComSk2 routes, begins)"),
]

# --- witness sheet: the tick gains Level 2 -----------------------------------
WITNESS = [
 ("&#9744;&nbsp;<strong>Entry 3</strong> &nbsp;&nbsp;&nbsp; &#9744;&nbsp;<strong>Level 1</strong><br>",
  "&#9744;&nbsp;<strong>Entry 3</strong> &nbsp;&nbsp;&nbsp; &#9744;&nbsp;<strong>Level 1</strong> &nbsp;&nbsp;&nbsp; &#9744;&nbsp;<strong>Level 2</strong><br>"),
 ("Entry 3 <em>or</em> Level 1, never both (barred combinations, spec v1.2 &#167;6.5). Supported and Standard evidence Entry 3; Stretch evidences Level 1.",
  "Entry 3, Level 1 <em>or</em> Level 2, never more than one (barred combinations, spec v1.2 &#167;6.5). Supported and Standard evidence Entry 3; Stretch evidences Level 1; the staff-directed Level 2 route evidences Level 2."),
]

# --- printPack hook: the mirror prints only while the route toggle is on -----
PP_ANCHOR = "const ws=document.getElementById('print-worksheet-'+level);if(ws)ws.classList.add('visible');"
PP_HOOK = "const l2=document.getElementById('print-l2route');if(l2&&document.documentElement.classList.contains('mbm-guide-on'))l2.classList.add('visible');"

# --- panel content per deck (ComSk2 facts: SPEC_FACTS_L2.md, spec pp52-54) ---
PANEL_STYLE = ("margin-top:14px;border:2px solid var(--lo-border);border-left:8px solid var(--lo-border);"
               "border-radius:12px;background:var(--lo-bg);padding:14px 16px")
PANELS = {
 "PEQ_W1": ("Level 2 route. For pupils directed here by staff. At Level 2 the six skills carry Level 2 units, and Thinking becomes Critical thinking, CrThSk2. Your task at Level 2: complete the six-skill self-assessment, then EVALUATE your starting points: describe your strongest evidence for each skill and assess which two skills need most development, giving reasons.",
  "<strong>Your task at Level 2:</strong> complete the six-skill self-assessment, then <strong>evaluate</strong> your starting points &#8212; <em>describe</em> your strongest evidence for each skill and <em>assess</em> which two skills need most development, giving reasons. At Level 2 the units are ComSk2 &#183; DecMkSk2 &#183; LSk2 &#183; TmWkSk2 &#183; <strong>CrThSk2 (Thinking becomes Critical thinking)</strong> &#183; WellbLe2. Verbs move from State/List to <strong>Describe &#183; Explain &#183; Compare &#183; Assess &#183; Evaluate</strong>."),
 "PEQ_W2": ("Level 2 route. Your task at Level 2, unit ComSk2: describe at least four ways people communicate, at least three types and at least three purposes of communication; describe at least four components of effective communication; and explain at least four difficulties and the impact of poor communication.",
  "<strong>Your task at Level 2 (ComSk2 2.1.1&#8211;2.1.3):</strong> <em>describe</em> what communication means &#8212; at least <strong>4 ways</strong> people communicate, <strong>3 types</strong> and <strong>3 purposes</strong>; <em>describe</em> at least <strong>4 components</strong> of effective communication; <em>explain</em> at least <strong>4 difficulties</strong> and the potential impact of poor communication."),
 "PEQ_W3": ("Level 2 route. Your task at Level 2, unit ComSk2: describe active listening and its components, explain why it matters, define feedback, explain why feedback is important, and describe ways feedback can be demonstrated with examples across different ways, types and purposes of communication.",
  "<strong>Your task at Level 2 (ComSk2 2.2.1&#8211;2.3.3):</strong> <em>describe</em> active listening and its components and <em>explain</em> its importance; <em>define</em> feedback, <em>explain</em> why it matters, and <em>describe</em> ways feedback can be demonstrated &#8212; with examples across different ways, types and purposes of communication."),
 "PEQ_W4": ("Level 2 route. Your task at Level 2, unit ComSk2: create TWO plans covering two DIFFERENT ways of communicating. Each plan needs purpose, audience, type with reason for choice, content outline, resources, and at least four audience questions in total, two per activity. There is no review point on the communication plan.",
  "<strong>Your task at Level 2 (ComSk2 2.4.1):</strong> <em>create</em> <strong>TWO plans covering two DIFFERENT ways of communicating</strong> (one can be a presentation or a group discussion). Each plan: purpose &#183; audience &#183; type with reason for choice &#183; content outline &#183; resources &#183; potential audience questions and responses &#8212; <strong>at least 4 questions in total, 2 per activity</strong>."),
 "PEQ_W5": ("Level 2 route. Your task at Level 2, unit ComSk2: use BOTH plans. Minimum sizes at Level 2: a presentation of at least four minutes, a discussion of at least ten minutes, or a written text of at least five hundred words. A group must have at least three members.",
  "<strong>Your task at Level 2 (ComSk2 2.5.1):</strong> <em>use BOTH plans</em>. Level 2 activity minima: presentation <strong>&#8805;4 min</strong> &#183; discussion <strong>&#8805;10 min</strong> &#183; text <strong>&#8805;500 words</strong>. A group must have &#8805;3 members. Evidence both activities &#8212; witness sheet ticks <strong>Level 2</strong>."),
 "PEQ_W6": ("Level 2 route. Your task at Level 2, unit ComSk2: evaluate your progress. Include at least three positive outcomes, your use of active listening, how difficulties were managed, how you used peer feedback, at least two areas of further development, and future situations for your communication skills.",
  "<strong>Your task at Level 2 (ComSk2 2.6.1):</strong> <em>evaluate</em> personal progress &#8212; at least <strong>3 positive outcomes</strong> &#183; use of active listening &#183; how difficulties were managed &#183; use of <strong>peer feedback</strong> to inform future development &#183; at least <strong>2 areas of further development</strong> &#183; future situations."),
}
LEAD = ("<p style=\"margin:0 0 6px;font-weight:900;font-size:.85rem;letter-spacing:.5px;text-transform:uppercase;color:var(--aspire-text)\">"
        "Level 2 route &#8212; for pupils directed here by staff</p>")
TAIL = ("<p style=\"margin:8px 0 0;font-size:.85rem\">Working towards &#8212; registration and level are coordinator decisions; "
        "evidence banks at ONE level per skill (spec &#167;6.5). Full Level 2 facts: SPEC_FACTS_L2.</p>")

def panel_html(key):
    speak, body = PANELS[key]
    return (f'<div class="wit-panel" data-mbm-guide="1" data-l2route="1" data-speak-text="{speak}" '
            f'style="{PANEL_STYLE}">{LEAD}<p style="margin:0 0 8px">{body}</p>{TAIL}</div>')

def mirror_html(key):
    speak, body = PANELS[key]
    return (f'<div class="print-section" id="print-l2route"><h2>Level 2 route &#8212; staff-directed (ComSk2)</h2>'
            f'<p>{body}</p><p style="font-size:.9rem">Working towards &#8212; registration and level are coordinator '
            f'decisions; evidence banks at ONE level per skill (spec &#167;6.5).</p></div>')

INSTR_ANCHOR = '<div class="li-box" data-mbm-guide="1"><strong>Instructions:</strong>'
PRINT_WITNESS = '<div id="print-witness" class="print-section"'

def div_end(s, i):
    depth = 0
    for m in re.finditer(r'<div\b|</div>', s[i:]):
        depth += 1 if m.group(0).startswith("<div") else -1
        if depth == 0:
            return i + m.end()
    raise AssertionError("unbalanced divs")

def patch_one(path):
    key = os.path.basename(path)[:6].rstrip("_")
    s0 = open(path, encoding="utf-8").read()
    s = s0
    if 'data-l2route="1"' not in s:
        i = s.find(INSTR_ANCHOR)
        assert i >= 0, f"{path}: instructions anchor missing"
        j = div_end(s, i)
        s = s[:j] + panel_html(key) + s[j:]
    if 'id="print-l2route"' not in s:
        k = s.find(PRINT_WITNESS)
        assert k >= 0, f"{path}: print-witness anchor missing"
        s = s[:k] + mirror_html(key) + s[k:]
    if PP_HOOK not in s:
        assert PP_ANCHOR in s, f"{path}: printPack anchor missing"
        s = s.replace(PP_ANCHOR, PP_ANCHOR + PP_HOOK, 1)
    for old, new in BANKING:
        s = s.replace(old, new)
    for old, new in WITNESS:
        s = s.replace(old, new)
    if s != s0:
        open(path, "w", encoding="utf-8").write(s)
        return 1
    return 0

def strip_one(path):
    s0 = open(path, encoding="utf-8").read()
    s = s0
    i = s.find('<div class="wit-panel" data-mbm-guide="1" data-l2route="1"')
    if i >= 0: s = s[:i] + s[div_end(s, i):]
    k = s.find('<div class="print-section" id="print-l2route">')
    if k >= 0: s = s[:k] + s[div_end(s, k):]
    s = s.replace(PP_HOOK, "")
    for old, new in BANKING + WITNESS:
        s = s.replace(new, old)
    if s != s0:
        open(path, "w", encoding="utf-8").write(s)
        return 1
    return 0

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "verify"
    changed = 0
    for d in DECKS:
        p = os.path.join(DIR, d)
        if mode == "patch": changed += patch_one(p)
        elif mode == "strip": changed += strip_one(p)
        else:
            s = open(p, encoding="utf-8").read()
            print(f"{d}: panels={s.count('data-l2route=')} mirrors={s.count('id=' + chr(34) + 'print-l2route')} "
                  f"ruled-strings={sum(s.count(new) for _, new in BANKING)} "
                  f"L2-tick={'yes' if WITNESS[0][1] in s else 'no'} hook={'yes' if PP_HOOK in s else 'no'}")
    if mode in ("patch", "strip"):
        print(f"{mode}: {changed} file(s) changed")

if __name__ == "__main__":
    main()
