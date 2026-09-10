#!/usr/bin/env python3
"""One place for everything that differs between pathways.

WHY THIS EXISTS. The return-week build is the same job twice: pack bytes become
the served file, live furniture is carried forward. Only the strings differ.
Forking the toolchain for GROW would duplicate nine hundred lines and guarantee
that the next fix lands in one copy and not the other -- which is how the
"Yellow Box" reconstruction survived three passes.

WHAT MAY LIVE HERE. Values MEASURED from the pack and live files. Nothing in this
file is composed: every string is either lifted verbatim from a live file or
matched against pack bytes. A value that has not been measured yet is None, and
`need()` turns using it into a loud failure rather than a silent one -- GW1-B R1
applied to configuration, where an unset value is 'empty', not 'zero'.
"""


class Unmeasured(Exception):
    pass


def need(pw, key, which=None):
    """Fetch a pathway value, refusing to hand back a placeholder.

    An unmeasured parameter must stop the build at the point of use, naming
    itself. The alternative -- None flowing into a regex or a replace() -- is a
    silent no-op that reports 'already applied / nothing to do'.
    """
    v = pw.get(key)
    if which is not None and isinstance(v, dict):
        v = v.get(which)
    if v is None:
        raise Unmeasured(
            '%s: %s%s has not been measured yet. Measure it from the pack/live '
            'files and put it in pathways.py; do not guess it from the other '
            'pathway.' % (pw.get('name', '?'), key, '[%s]' % which if which else ''))
    return v


BUILD = {
    'name': 'BUILD',
    # Lesson keys, in teaching order. BUILD and GROW run two lessons in the
    # return week; LAUNCH runs three. Nothing downstream may assume two.
    'lessons': ('A', 'B'),
    'live': {
        'A': 'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html',
        'B': 'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8B_Autumn_Science_Checkpoint_Do.html',
    },
    'pack': {
        'A': 'Lesson_A_Sugar_Evidence/BUILD_W8A_Interactive.html',
        'B': 'Lesson_B_Body_Checkpoint/BUILD_W8B_Interactive.html',
    },
    # Copied out of the live counterpart, not composed (RW1-A B2).
    'brandline': {
        'A': '<p class="brandline">BUILD &middot; Science &middot; Week 8A &middot; Explore</p>',
        'B': '<p class="brandline">BUILD &middot; Science &middot; Week 8B &middot; Do</p>',
    },
    # Both forms exist in these files; the entity form is tried first.
    'review_meta': [
        r'<p class="review-meta">BUILD &middot; SCIENCE &middot; Week 8 &middot; w/c 19 October 2026</p>',
        r'<p class="review-meta">BUILD · SCIENCE · Week 8 · w/c 19 October 2026</p>',
    ],
    # Pack-relative links. Every lesson lands in the SAME served directory, so a
    # pack-relative href is wrong there. Each entry is (href, (kind, target)):
    #   ('lesson', KEY)  -> the live filename of that lesson
    #   ('lesson', None) -> whichever sibling is not the file being processed
    #   ('literal', S)   -> S verbatim
    #
    # ../START_HERE.html is the pupil-facing "Lessons" control in the toolbar. It
    # is in ALL THREE packs and it 404s on every served route: START_HERE.html
    # exists in each WEEK directory and not in the pathway directory above it, so
    # the '../' walks straight past it. Dropping the '../' is what live already
    # does -- live links to 'START_HERE.html' with no prefix.
    'pack_links': [
        ('../Lesson_B_Body_Checkpoint/BUILD_W8B_Interactive.html', ('lesson', 'B')),
        ('../Lesson_A_Sugar_Evidence/BUILD_W8A_Interactive.html', ('lesson', 'A')),
        ('../START_HERE.html', ('literal', 'START_HERE.html')),
    ],
    # pathway · subject · lesson title, for the print identity line (RW1-E W2).
    'identity': {'A': ('BUILD', 'Science', 'Sugar Evidence'),
                 'B': ('BUILD', 'Science', 'Body Science Checkpoint')},
    # A single content defect measured in the pack, not a class of them.
    'literal_fixes': [('E gives3+3+3+3=12 g sugar per 100 g.',
                       'E gives 3+3+3+3 = 12 g sugar per 100 g.')],
    'date_tokens': [r'\s*&middot;\s*19 October 2026', r'\s*·\s*19 October 2026'],
    'growdark': '--growdark:#355E7B',
    # The host the marking card REPLACES. BUILD's pack ships a "Lundy alongside
    # learning" desk card and the card takes its place, so no staff guidance is
    # deleted without a replacement. Where a pack already authors its own card
    # this is None and the whole step stands down -- see assessment_layer().
    'assessment_host': (r'<details class="teacher-only"><summary>Lundy alongside '
                        r'learning[^<]*</summary>.*?</details>'),
}

# GROW is measured by the GW1-B survey. Every None below is a value that must be
# read off the GROW pack or the GROW live file before the build can run; need()
# refuses to proceed without it.
GROW = {
    'name': 'GROW',
    'lessons': ('A', 'B'),
    'live': {
        'A': 'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8A_Day_And_Night_Explore.html',
        'B': 'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8B_Day_And_Night_Do.html',
    },
    'pack': {
        'A': 'Lesson_A_Sky_Shift/SCI_G_W8A_Day_And_Night_Explore.html',
        'B': 'Lesson_B_Control_Room/SCI_G_W8B_Day_And_Night_Do.html',
    },
    # Measured by the GW1-B survey and spot-checked independently. GROW uses the
    # LITERAL separator U+00B7 exclusively: '&middot;' appears 0 times in either
    # pack file and 0 times in either live file. Composing with the entity form
    # would emit bytes that exist nowhere in the GROW estate -- and BUILD's
    # entity-first pattern matches 0 of 9 here, which report() prints as
    # "already applied / nothing to do". A silent no-op that reads as success.
    'brandline': {
        'A': '<p class="brandline">GROW \u00b7 Science \u00b7 Week 8A \u00b7 Explore</p>',
        'B': '<p class="brandline">GROW \u00b7 Science \u00b7 Week 8B \u00b7 Do</p>',
    },
    'review_meta': [
        r'<p class="review-meta">GROW \u00b7 SCIENCE \u00b7 Week 8 \u00b7 w/c 19 October 2026</p>',
    ],
    'pack_links': [
        ('../Lesson_B_Control_Room/SCI_G_W8B_Day_And_Night_Do.html', ('lesson', 'B')),
        ('../Lesson_A_Sky_Shift/SCI_G_W8A_Day_And_Night_Explore.html', ('lesson', 'A')),
        ('../START_HERE.html', ('literal', 'START_HERE.html')),
    ],
    # Titles corroborated three ways: the pack <title>, the pack's own
    # science-meta bodies, and the live <title>.
    'identity': {'A': ('GROW', 'Science', 'Day and Night: Sky Shift'),
                 'B': ('GROW', 'Science', 'Day and Night: 24-Hour Control Room')},
    'literal_fixes': [],
    # BUILD's patterns anchor the date to a preceding separator. GROW writes
    # "\u00b7 w/c 19 October 2026", so the 'w/c ' sits between them and BUILD's
    # form matches 0 of 6. Match the date itself.
    'date_tokens': [r'\s*\u00b7\s*w/c\s+19\s+October\s+2026', r'\s*\u00b7\s*19\s+October\s+2026'],
    # GROW live defines its own brand colour. BUILD's #355E7B is a different hue.
    'growdark': '--growdark:#215E53',
    # None, and measured: the GROW pack carries 0 "Lundy alongside learning" desk
    # cards and already ships id="print-marking" of its own. Running BUILD's
    # replacement here would substitute against 0 hosts and then inject the card
    # CSS anyway -- dead rules for an element that never gets created.
    'assessment_host': None,
}

# LAUNCH is three lessons, not two (LW1 §0.2), and its filenames are preserved
# exactly -- no renames. Live directory and every string are measured, not
# assumed; the None slots are what the LW1 survey must fill.
LAUNCH = {
    'name': 'LAUNCH',
    'lessons': ('L1', 'L2', 'L3'),
    # Derived from the estate, not assumed (LW1 §0.2): all three routes exist on
    # origin/main under Science_Teesside/Launch/W8-W13_2026-27/, so all three are
    # REPLACEs and none takes the admission path. Filenames preserved exactly.
    'live': {
        'L1': 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L1_Enzyme_Action_Introduce.html',
        'L2': 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L2_Amylase_pH_Core_Practical_Explore.html',
        'L3': 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L3_Amylase_Rate_And_Topic_1_Do.html',
    },
    'pack': {
        'L1': 'Lesson_1_Enzyme_Action/SCI_L_W8L1_Enzyme_Action_Introduce.html',
        'L2': 'Lesson_2_Amylase_pH/SCI_L_W8L2_Amylase_pH_Core_Practical_Explore.html',
        'L3': 'Lesson_3_Rates_And_Reasoning/SCI_L_W8L3_Amylase_Rate_And_Topic_1_Do.html',
    },
    'brandline': None,
    'review_meta': None,
    'pack_links': None,
    'identity': None,
    'literal_fixes': [],
    'date_tokens': None,
    # Measured: all three LAUNCH pack files already ship id="print-marking" and
    # carry 0 Lundy desk cards, same as GROW.
    'assessment_host': None,
}

ALL = {'BUILD': BUILD, 'GROW': GROW, 'LAUNCH': LAUNCH}
