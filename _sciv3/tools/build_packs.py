"""Phase A — repair the three lesson packs, deterministically.

Reads the pristine extracted zips, writes repaired copies to a staging tree.
Every edit asserts its anchor exists before touching anything: a silent no-op is
the failure mode that produced the defects this run is fixing.

    python3 _sciv3/tools/build_packs.py <inputs-root> <staging-root>
"""
import sys, os, re, json, shutil, hashlib

IN = sys.argv[1] if len(sys.argv) > 1 else None
OUT = sys.argv[2] if len(sys.argv) > 2 else None
# Cumulative repair stages, so Phase A lands as a bisectable sequence of commits.
ALL_STAGES = ['s1_mech', 's2_pack', 's3_food', 's4_closure', 's5_baseline', 's6_reading']
STAGES = set(sys.argv[3].split(',')) if len(sys.argv) > 3 else set(ALL_STAGES)
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
LOG = []


def note(kind, f, msg):
    LOG.append((kind, f, msg))


class NoAnchor(Exception):
    pass


def sub1(t, old, new, f, what, count=1):
    """Replace exactly `count` occurrences, or raise. Never silently no-op."""
    n = t.count(old)
    if n != count:
        raise NoAnchor(f"{f}: {what}: expected {count} occurrence(s) of {old[:90]!r}, found {n}")
    return t.replace(old, new)


def subre(t, pat, new, f, what, count=1, flags=0):
    hits = re.findall(pat, t, flags)
    if len(hits) != count:
        raise NoAnchor(f"{f}: {what}: expected {count} match(es) of {pat[:90]!r}, found {len(hits)}")
    return re.sub(pat, new, t, flags=flags)


# ============================================================ pack description

DIALECT = {
    'grow':   dict(pack='print-pack', page='print-page', route='print-route',
                   attr='data-print-tier', ds='printTier', line='print-line', box='print-box'),
    'build':  dict(pack='printpack', page='pp', route='proute',
                   attr='data-tier', ds='tier', line='pline', box='box'),
    'launch': dict(pack='printpack', page='pp', route='proute',
                   attr='data-tier', ds='tier', line='pline', box='box'),
}

NAMES = {
 'grow': {
  'SCI_G_W3A_Friction_Explore_OUTSTANDING_V3_TEST.html': 'SCI_G_W3A_Friction_Explore.html',
  'SCI_G_W3B_Friction_Do_OUTSTANDING_V3_TEST.html': 'SCI_G_W3B_Friction_Do.html',
  'SCI_G_W4A_Mechanisms_Explore_OUTSTANDING_V3_TEST.html': 'SCI_G_W4A_Mechanisms_Explore.html',
  'SCI_G_W4B_Mechanisms_Do_OUTSTANDING_V3_TEST.html': 'SCI_G_W4B_Mechanisms_Do.html',
  'SCI_G_W5A_Fair_Test_Explore_OUTSTANDING_V3_TEST.html': 'SCI_G_W5A_Fair_Test_Explore.html',
  'SCI_G_W5B_Fair_Test_Do_OUTSTANDING_V3_TEST.html': 'SCI_G_W5B_Fair_Test_Do.html',
  'SCI_G_W6A_Earth_And_Planets_Explore_OUTSTANDING_V3_TEST.html': 'SCI_G_W6A_Earth_And_Planets_Explore.html',
  'SCI_G_W6B_Earth_And_Planets_Do_OUTSTANDING_V3_TEST.html': 'SCI_G_W6B_Earth_And_Planets_Do.html',
  'SCI_G_W7A_The_Moon_Explore_OUTSTANDING_V3_TEST.html': 'SCI_G_W7A_The_Moon_Explore.html',
  'SCI_G_W7B_The_Moon_Do_OUTSTANDING_V3_TEST.html': 'SCI_G_W7B_The_Moon_Do.html',
  'START_HERE_GROW_SCIENCE_OUTSTANDING_V3.html': 'index.html',
 },
 'build': {
  'SCI_B_W3A_Backbones_and_No_Backbones_OUTSTANDING_V3_TEST.html': 'SCI_B_W3A_Backbones_Explore.html',
  'SCI_B_W3B_Backbone_Detectives_OUTSTANDING_V3_TEST.html': 'SCI_B_W3B_Backbone_Detectives_Do.html',
  'SCI_B_W4A_Muscles_Work_in_Pairs_OUTSTANDING_V3_TEST.html': 'SCI_B_W4A_Muscles_Explore.html',
  'SCI_B_W4B_Build_a_Working_Muscle_Model_OUTSTANDING_V3_TEST.html': 'SCI_B_W4B_Muscle_Model_Do.html',
  'SCI_B_W5A_What_a_Body_Needs_OUTSTANDING_V3_TEST.html': 'SCI_B_W5A_Body_Needs_Explore.html',
  'SCI_B_W5B_Nutrition_Mission_OUTSTANDING_V3_TEST.html': 'SCI_B_W5B_Nutrition_Mission_Do.html',
  'SCI_B_W6A_Building_a_Balanced_Plate_OUTSTANDING_V3_TEST.html': 'SCI_B_W6A_Balanced_Plate_Explore.html',
  'SCI_B_W6B_Balanced_Plate_Design_Challenge_OUTSTANDING_V3_TEST.html': 'SCI_B_W6B_Balanced_Plate_Do.html',
  'SCI_B_W7A_Animals_Cannot_Make_Their_Own_Food_OUTSTANDING_V3_TEST.html': 'SCI_B_W7A_Food_Sources_Explore.html',
  'SCI_B_W7B_Build_a_Food_Source_Chain_OUTSTANDING_V3_TEST.html': 'SCI_B_W7B_Food_Chain_Do.html',
  'START_HERE_BUILD_SCIENCE_OUTSTANDING_V3.html': 'index.html',
 },
 'launch': {
  'SCI_L_W3L1_Microscopy_Magnification_Resolution_INTRODUCE_OUTSTANDING_V3_TEST.html': 'SCI_L_W3L1_Microscopy_Introduce.html',
  'SCI_L_W3L2_Calculating_Magnification_EXPLORE_OUTSTANDING_V3_TEST.html': 'SCI_L_W3L2_Calculating_Magnification_Explore.html',
  'SCI_L_W3L3_Magnification_Exam_Measurement_Lab_DO_OUTSTANDING_V3_TEST.html': 'SCI_L_W3L3_Magnification_Lab_Do.html',
  'SCI_L_W4L1_Diffusion_Net_Movement_Down_a_Gradient_INTRODUCE_OUTSTANDING_V3_TEST.html': 'SCI_L_W4L1_Diffusion_Introduce.html',
  'SCI_L_W4L2_Diffusion_in_the_Lungs_EXPLORE_OUTSTANDING_V3_TEST.html': 'SCI_L_W4L2_Diffusion_Lungs_Explore.html',
  'SCI_L_W4L3_Diffusion_Explanation_Exam_Lab_DO_OUTSTANDING_V3_TEST.html': 'SCI_L_W4L3_Diffusion_Explanation_Do.html',
  'SCI_L_W5L1_Osmosis_Water_Across_a_Membrane_INTRODUCE_OUTSTANDING_V3_TEST.html': 'SCI_L_W5L1_Osmosis_Introduce.html',
  'SCI_L_W5L2_Osmosis_Core_Practical_EXPLORE_OUTSTANDING_V3_TEST.html': 'SCI_L_W5L2_Osmosis_Core_Practical_Explore.html',
  'SCI_L_W5L3_Analyse_Evaluate_Osmosis_Data_DO_OUTSTANDING_V3_TEST.html': 'SCI_L_W5L3_Osmosis_Data_Do.html',
  'SCI_L_W6L1_Active_Transport_INTRODUCE_OUTSTANDING_V3_TEST.html': 'SCI_L_W6L1_Active_Transport_Introduce.html',
  'SCI_L_W6L2_Active_Transport_in_Root_Hairs_Gut_EXPLORE_OUTSTANDING_V3_TEST.html': 'SCI_L_W6L2_Root_Hairs_And_Gut_Explore.html',
  'SCI_L_W6L3_Compare_Diffusion_Osmosis_Active_Transport_DO_OUTSTANDING_V3_TEST.html': 'SCI_L_W6L3_Compare_Transport_Do.html',
  'SCI_L_W7L1_Topic_1_Knowledge_Round_Up_INTRODUCE_OUTSTANDING_V3_TEST.html': 'SCI_L_W7L1_Topic_1_Round_Up_Introduce.html',
  'SCI_L_W7L2_GCSE_Command_Words_Across_Topic_1_EXPLORE_OUTSTANDING_V3_TEST.html': 'SCI_L_W7L2_Command_Words_Explore.html',
  'SCI_L_W7L3_Topic_1_Independent_Exam_Practice_DO_OUTSTANDING_V3_TEST.html': 'SCI_L_W7L3_Exam_Practice_Do.html',
  'START_HERE_LAUNCH_SCIENCE_OUTSTANDING_V3.html': 'index.html',
 },
}

# new-lesson key -> live lesson supplying the witness wording (A2 / D4a)
LIVE_FOR = {
 'grow': {k: v for k, v in [
   ('W3A', 'Grow/SCI_G_W3_Friction.html'), ('W3B', 'Grow/SCI_G_W3_Friction.html'),
   ('W4A', 'Grow/SCI_G_W4_Mechanisms.html'), ('W4B', 'Grow/SCI_G_W4_Mechanisms.html'),
   ('W5A', 'Grow/SCI_G_W5_Fair_Test.html'), ('W5B', 'Grow/SCI_G_W5_Fair_Test.html'),
   ('W6A', 'Grow/SCI_G_W6_Earth_And_Planets.html'), ('W6B', 'Grow/SCI_G_W6_Earth_And_Planets.html'),
   ('W7A', 'Grow/SCI_G_W7_The_Moon.html'), ('W7B', 'Grow/SCI_G_W7_The_Moon.html')]},
 'build': {k: v for k, v in [
   ('W3A', 'Build/SCI_B_W3_Backbones.html'), ('W3B', 'Build/SCI_B_W3_Backbones.html'),
   ('W4A', 'Build/SCI_B_W4_Muscle_Pairs.html'), ('W4B', 'Build/SCI_B_W4_Muscle_Pairs.html'),
   ('W5A', 'Build/SCI_B_W5_Right_Nutrition.html'), ('W5B', 'Build/SCI_B_W5_Right_Nutrition.html'),
   ('W6A', 'Build/SCI_B_W6_Balanced_Plate.html'), ('W6B', 'Build/SCI_B_W6_Balanced_Plate.html'),
   ('W7A', 'Build/SCI_B_W7_Where_Food_Comes_From.html'),
   ('W7B', 'Build/SCI_B_W7_Where_Food_Comes_From.html')]},
 'launch': {k: 'Launch/' + v for k, v in [
   ('W3L1', 'SCI_L_W3_L1_Microscopy.html'), ('W3L2', 'SCI_L_W3_L2_Magnification.html'),
   ('W3L3', 'SCI_L_W3_L3_ExamSkills.html'), ('W4L1', 'SCI_L_W4_L1_Diffusion.html'),
   ('W4L2', 'SCI_L_W4_L2_GasExchange.html'), ('W4L3', 'SCI_L_W4_L3_ExamSkills.html'),
   ('W5L1', 'SCI_L_W5_L1_Osmosis.html'), ('W5L2', 'SCI_L_W5_L2_OsmosisCP.html'),
   ('W5L3', 'SCI_L_W5_L3_Evaluate.html'), ('W6L1', 'SCI_L_W6_L1_ActiveTransport.html'),
   ('W6L2', 'SCI_L_W6_L2_RootAndGut.html'), ('W6L3', 'SCI_L_W6_L3_Compare.html'),
   ('W7L1', 'SCI_L_W7_L1_RoundUp.html'), ('W7L2', 'SCI_L_W7_L2_CommandWords.html'),
   ('W7L3', 'SCI_L_W7_L3_ExamPractice.html')]},
}

ROUTE_WORD = {'A': 'Explore', 'B': 'Do'}
LAUNCH_STAGE = {'L1': 'Introduce', 'L2': 'Explore', 'L3': 'Do'}


def lesson_key(pack, src):
    m = re.search(r'SCI_[GBL]_(W\d(?:[AB]|L\d))_', src)
    return m.group(1) if m else None


# ============================================================ A7 / A9 text

A7_LINE = ("<b>Not here last lesson?</b> Everything you need is in the box above — "
           "read it, then answer.")
A7_LINE_W3 = ("<b>New to this class, or not sure?</b> Everything you need is in the box above — "
              "read it, then answer.")
A9_RETRIEVAL = ("<b>Weeks 1 and 2 were baseline.</b> There is no previous lesson to recall — "
                "this is where the teaching starts. Begin from what you already know.")
A9_LABEL = "🚪 Arrival · what you already know"

A9_PROMPTS = {
 'grow': {
   'Supported': ("Point or say: which force from last lesson can slow something moving through air or water?",
                 "Point or say: what force do you already know that can slow a moving object down?"),
   'Standard': ("Name one resistance force from last lesson and say what it does to motion.",
                "Name one resistance force you already know, and say what it does to motion."),
   'Stretch': ("Explain how changing shape can change air or water resistance.",
               "What do you already know about how an object\u2019s shape changes air or water resistance?"),
 },
 'build': {
   'Supported': ("Point to the spine/backbone on the skeleton diagram from last lesson.",
                 "Point to the spine/backbone on the skeleton diagram."),
   'Standard': ("Name two major bones from last lesson and point to the backbone.",
                "Name any two major bones you already know, then point to the backbone."),
   'Stretch': ("Explain one job of the skeleton and locate the backbone on the model.",
               "What do you already know about what a skeleton does? Then locate the backbone on the model."),
 },
 'launch': {
   'Supported': ("Label eyepiece and objective lens.",
                 "Point to the eyepiece and the objective lens on the microscope \u2014 have a go, even if you are not sure."),
   'Standard': ("Name the two lenses and which one you look through.",
                "Have you used a microscope before? Point to the two lenses and name any parts you already know."),
   'Stretch': ("Calculate \u00d710 eyepiece \u00d7 \u00d740 objective.",
               "One lens \u2014 the eyepiece \u2014 makes an image 10 times bigger. A second \u2014 the objective \u2014 makes it 40 times bigger. What do you think the total magnification would be?"),
 },
}

# A6 — GROW Supported route only. Fragment -> replacement. Applied wherever the
# fragment appears (print route AND the Independent slide carry the same string).
A6_EDITS = {
 'W4B': [("Photo/diagram sequence + two labelled pivot positions + choice vocabulary: easier / harder / further / less far.",
          "Photo or diagram sequence. Two labelled pivot positions. Choice words: easier · harder · further · less far.")],
 'W6A': [("◆ Use labelled cards + mnemonic strip + pre-drawn gravity arrow to complete.",
          "◆ Use the labelled cards and the mnemonic strip. The gravity arrow is already drawn.")],
 'W6B': [("◆ Numbered planet cards + completed type key + teacher-supplied orbit arrows.",
          "◆ Use the numbered planet cards. The type key and the orbit arrows are given.")],
 'W7B': [("◆ Four-position wheel with sunlight arrow already printed; pupil matches observer views.",
          "◆ Use the four-position wheel. The sunlight arrow is already printed. Match what the observer sees.")],
}

# §0.7 — the six healthy-eating links to remove
FOOD_UNIT = '/units/healthy-eating/'
FOOD_CARD_TEXT = ("No external food media in this lesson — see the BUILD protection rule.")

UNVERIFIED = ['/lessons/how-gears-can-help-us',
              '/lessons/the-planets-in-our-solar-system-non-statutory']


# ============================================================ witness statement

_live_cache = {}


def live_text(rel):
    if rel not in _live_cache:
        _live_cache[rel] = open(os.path.join(REPO, 'Science_Teesside', rel), encoding='utf-8').read()
    return _live_cache[rel]


def witness_html(pack, key, live_rel, route_label):
    """Copy the live Assessor Witness Statement chassis byte-for-byte; substitute
    only the Lesson row's route suffix. Wording is never invented (A2 / D4a)."""
    t = live_text(live_rel)
    i = t.find('<div id="print-witness"')
    j = t.find('<div id="print-lundy"', i)
    if i < 0 or j < 0:
        raise NoAnchor(f'{live_rel}: no witness block')
    blk = t[i:j]
    m = re.search(r'(<strong>Lesson</strong></td><td style="[^"]*">)([^<]*)(</td>)', blk)
    if not m:
        raise NoAnchor(f'{live_rel}: no Lesson row')
    blk = blk[:m.start(2)] + m.group(2) + f' ({route_label})' + blk[m.end(2):]
    return blk


def closure_html(live_rel):
    """A8.1 — the ratified LAUNCH written closure, copied verbatim from the
    matching live lesson (preamble sentence and the line itself)."""
    t = live_text(live_rel)
    i = t.find('<p style="font-size:.95rem;margin:.5rem 0 0"><strong>Closing the loop:</strong>')
    if i < 0:
        raise NoAnchor(f'{live_rel}: no closing-the-loop paragraph')
    j = t.find('What I said, and what it changed:', i)
    k = t.find('</p>', j)
    return t[i:k + 4]


# ============================================================ per-file transform

def transform_lesson(pack, src_name, t):
    d = DIALECT[pack]
    key = lesson_key(pack, src_name)
    is_w3_first = key in ('W3A', 'W3L1')
    f = src_name

    # ---------------- A1 · print default + afterprint
    t = sub1(t, '.%s{display:none}body[%s=' % (d['route'], d['attr']),
             '.%s{display:block}body[%s] .%s{display:none}body[%s=' % (
                 d['route'], d['attr'], d['route'], d['attr']),
             f, 'A1 css') if pack != 'grow' else t
    if pack == 'grow':
        t = sub1(t, '.print-route{display:none}\n body[data-print-tier=',
                 '.print-route{display:block}body[data-print-tier] .print-route{display:none}\n'
                 ' body[data-print-tier=', f, 'A1 css')
        t = sub1(t,
                 'function printTier(tier){document.body.dataset.printTier=tier;window.print();'
                 'setTimeout(()=>{delete document.body.dataset.printTier},500)}',
                 'function printTier(tier){document.body.dataset.printTier=tier;window.print()}\n'
                 "window.addEventListener('afterprint',()=>{delete document.body.dataset.printTier});",
                 f, 'A1 js')
    else:
        t = sub1(t,
                 'function printTier(t){document.body.dataset.tier=t;window.print();'
                 'setTimeout(()=>delete document.body.dataset.tier,500)}',
                 'function printTier(t){document.body.dataset.tier=t;window.print()}\n'
                 "window.addEventListener('afterprint',()=>{delete document.body.dataset.tier});",
                 f, 'A1 js')

    # ---------------- A4 · aria-live on every feedback region
    n_live = 0
    for old, new in [('<div class="feedback">', '<div class="feedback" aria-live="polite">'),
                     ('<div class="wf"', '<div class="wf" aria-live="polite"'),
                     ('<div class="widget-feedback"', '<div class="widget-feedback" aria-live="polite"')]:
        if old in t:
            n_live += t.count(old)
            t = t.replace(old, new)
    if n_live == 0:
        raise NoAnchor(f'{f}: A4 found no feedback region')
    note('A4', f, f'aria-live added to {n_live} feedback region(s)')

    # ---------------- A4 · aria-label on unlabelled inputs (GROW)
    if pack == 'grow':
        rows = {'r': 'Rough', 'm': 'Medium', 's': 'Smooth'}
        for rk, rname in rows.items():
            for run in '123':
                old = f'<input id="W5B-{rk}{run}" min="0" step="0.1" type="number"/>'
                if old in t:
                    t = sub1(t, old, old[:-2] +
                             f' aria-label="{rname} surface, run {run}, distance in cm"/>',
                             f, f'A4 label W5B-{rk}{run}')
                    note('A4', f, f'aria-label W5B-{rk}{run}')
        m = re.search(r'<input id="lev-(W\d[AB])" max="70" min="25" oninput="leverDemo\(\'\1\'\)" '
                      r'style="width:100%" type="range" value="48"/>', t)
        if m:
            t = t.replace(m.group(0), m.group(0)[:-2] +
                          ' aria-label="Lever pivot position slider, 25 to 70"/>')
            note('A4', f, 'aria-label lever slider')

    # ---------------- A9 · the W3 baseline correction (three files only)
    if is_w3_first and 's5_baseline' in STAGES:
        label_old = {'grow': '🚪 Arrival · prior lesson retrieval',
                     'build': '🚪 Arrival · retrieve last lesson',
                     'launch': '🚪 Arrival · previous learning'}[pack]
        t = t.replace(label_old, A9_LABEL)
        note('A9', f, f'arrival label {label_old!r} -> {A9_LABEL!r}')

        # screen retrieval box
        if pack == 'grow':
            t = subre(t, r'<div class="li-box"><b>Retrieve the previous lesson:</b>[^<]*</div>',
                      '<div class="li-box">' + A9_RETRIEVAL + '</div>', f, 'A9 screen box')
            t = sub1(t, '“Last lesson your evidence showed ___. Today we are starting by remembering ___.”',
                     '“Today we are starting from what you already know about ___.”',
                     f, 'A9 staff opener')
            t = sub1(t, 'Influence is made visible here: retrieve what the previous lesson actually '
                        'showed before adding new Science.',
                     'Influence is made visible here: start from what pupils already know before '
                     'adding new Science.', f, 'A9 lundy thread')
            t = subre(t, r'<p><b>Arrival retrieval:</b>[^<]*</p>',
                      '<p><b>Arrival — what you already know:</b> Weeks 1 and 2 were baseline. '
                      'There is no previous lesson to recall — this is where the teaching starts.</p>',
                      f, 'A9 print line')
        else:
            lead = {'build': 'Retrieve the actual previous lesson:',
                    'launch': 'Retrieve the previous learning:'}[pack]
            t = subre(t, r'<div class="box scaf"><b>%s</b>[^<]*</div>' % re.escape(lead),
                      '<div class="box scaf">' + A9_RETRIEVAL + '</div>', f, 'A9 screen box')
            plead = {'build': 'Previous lesson retrieval:', 'launch': 'Retrieval:'}[pack]
            t = subre(t, r'<p><b>%s</b>[^<]*</p>' % re.escape(plead),
                      '<p><b>Arrival — what you already know:</b> Weeks 1 and 2 were baseline. '
                      'There is no previous lesson to recall — this is where the teaching starts.</p>',
                      f, 'A9 print line')

        for tier, (old, new) in A9_PROMPTS[pack].items():
            t = sub1(t, '<p>' + old + '</p>', '<p>' + new + '</p>', f, f'A9 prompt {tier}')
            note('A9', f, f'{tier} prompt rewritten as elicitation')

    # ---------------- A7 · the arrival entry route
    # The W3 variant belongs with A9: until the baseline correction lands, those three
    # lessons genuinely did describe a previous lesson, so the standard line is the true one.
    line = A7_LINE_W3 if (is_w3_first and 's5_baseline' in STAGES) else A7_LINE
    if 's2_pack' in STAGES:
        cls = 'li-box' if pack == 'grow' else 'box scaf'
        m = re.search(r'<div class="%s">(?:(?!</div>).)*</div>' % re.escape(cls), t, re.S)
        if not m:
            raise NoAnchor(f'{f}: A7 could not find the arrival retrieval box')
        entry = ('<div class="entry-route" style="background:#fff7ed;border-left:5px solid '
                 '#f97316;padding:9px 12px;border-radius:10px;margin:6px 0">' + line + '</div>')
        t = t[:m.end()] + entry + t[m.end():]
        note('A7', f, 'entry line on arrival slide')

    # ---------------- A2 · date + name line and A7 line at the head of print page 1
    if 's2_pack' in STAGES:
        idline = ('<p class="pidline" style="margin:2px 0 8px;font-size:.92rem">'
                  '<b>Name:</b> _______________________________ &nbsp; '
                  '<b>Date:</b> ______________________</p>')
        entry_print = ('<p class="pentry" style="margin:0 0 8px;font-size:.92rem">'
                       + line + '</p>')
        if pack == 'grow':
            m = re.search(r'(<div class="print-page"><h1>.*?</h1><h2>.*?</h2>)', t, re.S)
        else:
            m = re.search(r'(<div class="pp"><h1>.*?</h1>)', t, re.S)
        if not m:
            raise NoAnchor(f'{f}: A2 could not find print page 1 heading')
        t = t[:m.end()] + idline + entry_print + t[m.end():]
        note('A2', f, 'date+name line and entry line on print page 1')

    # ---------------- A2 · Assessor Witness Statement on print page 2
    key = lesson_key(pack, src_name)
    if pack == 'launch':
        route_label = '40-min route · ' + LAUNCH_STAGE[key[2:]]
    else:
        route_label = '40-min route · ' + ROUTE_WORD[key[-1]]
    wit = witness_html(pack, key, LIVE_FOR[pack][key], route_label)

    tail = '</div></div>'
    pk = t.find('<div class="%s">' % d['pack'])
    end = t.find('<script', pk)
    seg = t[pk:end]
    if not seg.rstrip().endswith(tail):
        raise NoAnchor(f'{f}: A2 print pack does not end with {tail!r}')
    cut = pk + seg.rstrip().rfind(tail)
    add = ''
    if pack == 'launch' and 's4_closure' in STAGES:
        add += closure_html(LIVE_FOR[pack][key])
        note('A8.1', f, 'written closure line added to print page 2')
    if 's2_pack' in STAGES:
        add += wit
        note('A2', f, 'witness statement on print page 2')
    t = t[:cut] + add + t[cut:]

    # ---------------- A8.1 · the same closure line on the exit slide (screen)
    if pack == 'launch' and 's4_closure' in STAGES:
        anchor = ('<p class="note">No adult signature/countersignature. If local policy uses R, '
                  'it follows genuine Audience only; this page never adds it automatically.</p>')
        screen = ('<p style="font-size:.95rem;margin:.5rem 0 0"><strong>Closing the loop:</strong> '
                  'this one ends on paper &mdash; your own hand, or your words scribed by an adult. '
                  'Saying it aloud starts the loop; writing it is what closes it. Pass is always '
                  'allowed.</p><p style="font-size:.9rem;color:#444;margin:.4rem 0 .2rem">'
                  'What I said, and what it changed:</p>'
                  '<div class="pline" style="height:11mm;border-bottom:1px solid #999"></div>'
                  '<div class="pline" style="height:11mm;border-bottom:1px solid #999"></div>')
        t = sub1(t, anchor, anchor + screen, f, 'A8.1 exit slide')
        note('A8.1', f, 'written closure line on the exit slide')

    # ---------------- §0.7 · BUILD food links
    if pack == 'build' and 's3_food' in STAGES and FOOD_UNIT in t:
        m = re.search(r'<div class="media-card"><b>Optional current Oak resource</b>.*?</a></div>',
                      t, re.S)
        if not m or FOOD_UNIT not in m.group(0):
            raise NoAnchor(f'{f}: 0.7 could not find the food media card')
        url = re.search(r'href="([^"]*)"', m.group(0)).group(1)
        t = (t[:m.start()]
             + '<div class="media-card"><b>Optional current Oak resource</b>'
               '<p class="note">' + FOOD_CARD_TEXT + '</p></div>'
             + t[m.end():])
        if url in t:
            raise NoAnchor(f'{f}: 0.7 removed the card but {url} still appears')
        note('0.7', f, f'removed {url}')

    # ---------------- A3 · flag the two unverified GROW slugs
    if pack == 'grow':
        for slug in UNVERIFIED:
            if slug in t:
                t = re.sub(r'(<a\b(?![^>]*data-link-unverified)[^>]*href="[^"]*'
                           + re.escape(slug) + r'"[^>]*)>',
                           r'\1 data-link-unverified="true">', t)
                note('A3', f, f'flagged unverified slug {slug}')

    # ---------------- A6 · GROW Supported reading load
    if pack == 'grow' and 's6_reading' in STAGES and key in A6_EDITS:
        for old, new in A6_EDITS[key]:
            n = t.count(old)
            if n == 0:
                raise NoAnchor(f'{f}: A6 fragment not found: {old[:60]!r}')
            t = t.replace(old, new)
            note('A6', f, f'rewrote Supported fragment (x{n})')

    # ---------------- A5 · the provenance comment must stop saying TEST / no repo write
    t = re.sub(r'<!--\s*TEST BUILD\.', '<!-- Made by Matt · Science v3 40-minute route.', t)
    t = t.replace('No repo write.', 'Installed as a parallel route; the live lesson is unchanged.')
    t = t.replace('Repository unchanged.',
                  'Installed as a parallel route; the live lesson is unchanged.')
    return t


# ============================================================ hubs / guides / manifests

def transform_hub(pack, t):
    f = f'{pack}/index.html'
    for old, new in NAMES[pack].items():
        t = t.replace('href="%s"' % old, 'href="%s"' % new)
    t = t.replace('href="POLICY_ALIGNMENT.md"', 'href="../../../_sciv3/%s/POLICY_ALIGNMENT.md"' % pack)
    t = t.replace('href="SOW_AND_POLICY_ALIGNMENT.md"',
                  'href="../../../_sciv3/%s/SOW_AND_POLICY_ALIGNMENT.md"' % pack)
    lab = pack.upper()
    banner = ('<div class="v3banner" style="background:#0f2942;color:#fff;border-radius:12px;'
              'padding:11px 14px;margin:10px 0;font-weight:700">Alternative 40-minute route for '
              f'{lab} Science Aut 1 W3–W7. The existing route remains available in the Lessons '
              'catalogue.</div>')
    m = re.search(r'<body[^>]*>', t)
    t = t[:m.end()] + banner + t[m.end():]
    if pack in ('build', 'launch') and 's5_baseline' in STAGES:
        t = subre(t, r'<td>Aut1·W2[^<]*</td>',
                  '<td>Weeks 1 and 2 were baseline — no previous lesson to recall.</td>',
                  f, 'A9 hub row')
    base = ('<p style="margin:10px 0 0"><a href="../../../Baseline_Weeks/index.html">'
            'Baseline Weeks (public HTML baseline pack)</a> — a separate instrument, not this '
            'route’s prior learning.</p>')
    t = t.replace('</body>', base + '</body>')
    return t


def transform_guide(pack, t):
    add = ('<p><b>Pupils joining mid-year:</b> every arrival slide carries a read-it-here route.</p>'
           '<p><b>Autumn 1 W1–W2 were baseline weeks.</b> No science was taught in them, so the W3 '
           'lesson opens from what pupils already know rather than from a previous lesson. The '
           'baseline itself is delivered separately and is not in this repository.</p>')
    lab = pack.upper()
    banner = ('<div style="background:#0f2942;color:#fff;border-radius:12px;padding:11px 14px;'
              f'margin:10px 0;font-weight:700">Alternative 40-minute route for {lab} Science '
              'Aut 1 W3–W7. The existing route remains available in the Lessons catalogue.</div>')
    m = re.search(r'<body[^>]*>', t)
    t = t[:m.end()] + banner + t[m.end():]
    return t.replace('</body>', add + '</body>')


def transform_manifest(pack, raw):
    j = json.loads(raw)
    txt = json.dumps(j)
    # A9 — the W3 prior-learning claim
    def fix(o):
        if 's5_baseline' not in STAGES:
            return
        if isinstance(o, dict):
            for k, v in list(o.items()):
                if isinstance(v, str) and 'Aut1·W2' in v:
                    o[k] = ('Weeks 1 and 2 were baseline — no previous lesson to recall. '
                            'Teaching starts at W3.')
                else:
                    fix(v)
        elif isinstance(o, list):
            for v in o:
                fix(v)
    fix(j)
    # filenames
    s = json.dumps(j, ensure_ascii=False, indent=2)
    for old, new in NAMES[pack].items():
        s = s.replace(old, new)
    j = json.loads(s)
    # §0.7 — the manifest must state the media that actually exists.
    # Measured, against the document: BUILD's manifest has NO `media` key at all,
    # rather than `media: []`. Same audit consequence, different cause; recorded.
    OAK = 'https://www.thenational.academy/teachers/programmes/science-primary-ks2/units/'
    if pack == 'build' and 's3_food' in STAGES:
        keep = {'W3A': 'animals-without-bones', 'W3B': 'animals-without-bones',
                'W4A': 'muscles-for-movement', 'W4B': 'muscles-for-movement'}
        removed = {'W5A': 'healthy-eating/lessons/types-of-food',
                   'W5B': 'healthy-eating/lessons/types-of-food',
                   'W6A': 'healthy-eating/lessons/nutrient-rich-meal-planning-non-statutory',
                   'W6B': 'healthy-eating/lessons/nutrient-rich-meal-planning-non-statutory',
                   'W7A': 'healthy-eating/lessons/making-or-finding-food',
                   'W7B': 'healthy-eating/lessons/making-or-finding-food'}
        for les in j:
            k = les.get('id')
            if k in keep:
                les['media'] = [OAK + 'introduction-to-the-human-skeleton-and-muscles/lessons/'
                                + keep[k]]
                les['media_note'] = ('Optional teacher-only link, confirmed at this exact URL. '
                                     'Skeleton/muscle unit, not food.')
            elif k in removed:
                les['media'] = []
                les['media_removed'] = [OAK + removed[k]]
                les['media_note'] = ('Healthy-eating link removed under the BUILD protection rule '
                                     '(sci-v3 install, §0.7). No external food media in this '
                                     'lesson. The card remains, stating that.')
    if pack == 'launch':
        # LAUNCH genuinely has zero external URLs; make the zero auditable rather
        # than merely absent, so a manifest audit and a page audit agree.
        for les in j:
            les['media'] = []
            les['media_note'] = 'No external media anywhere in the LAUNCH v3 pack.'
    if pack == 'grow':
        for les in j:
            unver = [u for u in les.get('media', [])
                     if any(s.lstrip('/') in u for s in UNVERIFIED)]
            if unver:
                les['media_unverified'] = unver
                les['media_note'] = ('Slug unproven — the Oak lesson appears in the unit listing '
                                     'but the exact URL could not be fetched. Flagged in-page as '
                                     'data-link-unverified.')
    return json.dumps(j, ensure_ascii=False, indent=2) + '\n'


# ============================================================ drive

def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    for pack in ('grow', 'build', 'launch'):
        dst = os.path.join(OUT, pack)
        os.makedirs(dst)
        for src in sorted(os.listdir(os.path.join(IN, pack))):
            p = os.path.join(IN, pack, src)
            raw = open(p, encoding='utf-8').read()
            if src.startswith('SCI_'):
                out = transform_lesson(pack, src, raw)
                name = NAMES[pack][src]
            elif src.startswith('START_HERE'):
                out = transform_hub(pack, raw)
                name = 'index.html'
            elif src == 'TEACHER_IMPLEMENTATION_GUIDE.html':
                out = transform_guide(pack, raw)
                name = src
            elif src == 'manifest-v3.json':
                out = transform_manifest(pack, raw)
                name = src
            else:
                out, name = raw, src
            open(os.path.join(dst, name), 'w', encoding='utf-8').write(out)
    json.dump({'names': NAMES, 'live_for': LIVE_FOR},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'namemap.json'),
                   'w'), indent=1)
    for kind, f, msg in LOG:
        print(f'{kind:5s} {f[:52]:52s} {msg}')
    print(f'\n{len(LOG)} edits logged')


if __name__ == '__main__':
    main()
