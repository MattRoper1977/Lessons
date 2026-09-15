#!/usr/bin/env python3
"""RW1-B §H · furniture parity re-derived by DOM QUERY, not substring count.

WHY. The splash guard tested for the string "n6-splash" and was already true,
because the carried nav CSS contains ".n6-splash". The guard reported success
and the element was never inserted. A substring count cannot tell an ELEMENT
from a CSS rule, a JS reference or a comment that happens to spell its name.

So every row below is counted twice -- once by substring, once by parsing the
document and asking it -- and printed side by side. A row where the two disagree
is a finding with a named cause, not a rounding error.

Markers that are genuinely NOT DOM elements (a CSS block, a storage key inside a
script) are declared as such and given the nearest real DOM question instead;
they are not silently counted as if they were tags.
"""
import re, subprocess, sys
from pathlib import Path
import lxml.html

REPO = Path(__file__).resolve().parents[2]
LIVE = {
    'A': 'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html',
    'B': 'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8B_Autumn_Science_Checkpoint_Do.html',
}

def cls(tag, name):
    """Class matching by TOKEN, not by substring: contains(@class,'skip') also
    matches class="skipped". This instrument exists because substring matching
    lied once already."""
    return "//%s[contains(concat(' ', normalize-space(@class), ' '), ' %s ')]" % (tag, name)


# XPath, not CSS: cssselect is not installed here and this instrument is committed,
# so it must not depend on a package CI may lack.
# (label, substring pattern, xpath or None, note when it is not an element)
ROWS = [
 ('a.mbmhome',              r'class="mbmhome"',            cls('a','mbmhome'),                 None),
 ('div.n6-splash',          r'<div class="n6-splash"',      cls('div','n6-splash'),             None),
 ('[rel=prev]',             r'rel="prev"',                  "//*[@rel='prev']",                 None),
 ('[rel=next]',             r'rel="next"',                  "//*[@rel='next']",                 None),
 ('a.next-link',            r'class="next-link"',           cls('a','next-link'),               None),
 ('a.skip',                 r'class="skip"',                cls('a','skip'),                    None),
 ('#lessonDeck',            r'id="lessonDeck"',             "//*[@id='lessonDeck']",            None),
 ('[data-lesson-id]',       r'data-lesson-id',              '//*[@data-lesson-id]',             None),
 ('[data-pathway]',         r'data-pathway',                '//*[@data-pathway]',               None),
 # DECLARED EQUIVALENCE, and the pairing matters.
 #
 # Live's 9 data-ta1 are TA BRIEFS ("Read setup, safety and sensory notes before
 # pupils enter"), read by a script that says dataset.ta1. The pack replaces the
 # whole chassis: its script reads dataset.teacher and dataset.prompt, and its
 # markup supplies 9 data-teacher briefs (the same ROLE as live's data-ta1) plus
 # 9 data-prompt cold-call questions (a role live had no attribute for).
 #
 # So the equivalence is data-ta1 -> data-teacher BY ROLE, and data-prompt is an
 # addition. I first declared it as data-ta1 -> data-prompt, which pairs a TA
 # brief with a pupil question -- right about nothing being dropped, wrong about
 # what replaced what.
 #
 # And the reason nothing is orphaned is the READER, not the count: live's script
 # references dataset.ta1 once, the built file references it zero times, so there
 # is no code left looking for the attribute that went away. Both halves are
 # checked below -- an attribute arriving is not enough if the old reader
 # survives, and a reader disappearing is not enough if nothing replaced it.
 ('[data-ta1]',             r'data-ta1=',                   '//*[@data-ta1]',                   None),
 ('[data-teacher]',         r'data-teacher=',               '//*[@data-teacher]',               None),
 ('[data-prompt]',          r'data-prompt=',                '//*[@data-prompt]',                None),
 ('[data-mbm-guide=staff]', r'data-mbm-guide="staff"',      "//*[@data-mbm-guide='staff']",     None),
 ('.teacher-only',          r'class="[^"]*teacher-only',    cls('*','teacher-only'),            None),
 # NOT an element in the static document. All six substring hits are a CSS rule,
 # a docked-variant rule, a print rule, and two lines of script -- the button is
 # built at runtime by document.createElement. A static parse returns 0 forever,
 # so asking the parse for a tag was asking the wrong question; the real static
 # question is whether a script still constructs it. render_check.cjs answers the
 # rendered question and finds it present, visible, labelled "(i) Guidance".
 ('button.n6m-guide-btn',   r'n6m-guide-btn',               None,
    'SCRIPT-CREATED: never in the static DOM. DOM question is the row below; '
    'the rendered proof is render_check.cjs'),
 ('script building the btn', r'zzz-never-matches-zzz',       None,
    'counted by parsing <script> text for the className assignment'),
 ('style#n6m-guide-css',    r'n6m-guide-css',               "//style[@id='n6m-guide-css']",     None),
 ('script[usage-client]',   r'usage-client\.js',            '//script[contains(@src,"usage-client.js")]', None),
 ('script[lesson-nav]',     r'lesson-navigation\.js',       '//script[contains(@src,"lesson-navigation.js")]', None),
 ('link[rel=canonical]',    r'rel="canonical"',             "//link[@rel='canonical']",         None),
 ('n6m-guide (name)',       r'n6m-guide',                   None,
    'a NAME, not an element: CSS rules, a comment marker and JS all spell it'),
 ('mbm_guide_v1 (key)',     r'mbm_guide_v1',                None,
    'a localStorage KEY inside a script; DOM question is the script below'),
 ('script holding the key', r'zzz-never-matches-zzz',       None,
    'counted by parsing <script> text, see script_with_key()'),
]


def doc_of(text):
    return lxml.html.document_fromstring(text)


def script_with_key(doc, key='mbm_guide_v1'):
    return sum(1 for s in doc.xpath('//script') if key in (s.text or ''))


def script_builds_button(doc):
    """The static DOM question for a script-created element: does a script still
    assign the class that makes it?"""
    return sum(1 for s in doc.xpath('//script')
               if 'n6m-guide-btn' in (s.text or '') and 'createElement' in (s.text or ''))


# A carried marker may legitimately go to zero if a DECLARED equivalent picks up
# the same population. (gone, arrived, what it means)
EQUIVALENCE = [('[data-ta1]', '[data-teacher]',
                'TA briefs: live names them data-ta1 and reads them as '
                'dataset.ta1; the pack names them data-teacher and reads them as '
                'dataset.teacher. Same role, replaced together with their reader.',
                'dataset.ta1')]


def denominators(doc):
    """GW1-B R1. Every row below is a count; these are what those counts are
    drawn from. A denominator of zero means the parse saw nothing and every
    zero above it is vacuous, not clean."""
    ids = [e.get('id') for e in doc.xpath('//*[@id]')]
    return {'elements': len(doc.xpath('//*')),
            'elements_with_class': len(doc.xpath('//*[@class]')),
            'ids': len(ids), 'unique_ids': len(set(ids)),
            'scripts': len(doc.xpath('//script')),
            'markers_examined': len(ROWS)}


def counts(text):
    doc = doc_of(text)
    out = []
    for label, sub, css, note in ROWS:
        s = len(re.findall(sub, text))
        if label == 'script holding the key':
            d, s = script_with_key(doc), len(re.findall(r'mbm_guide_v1', text))
        elif label == 'script building the btn':
            d, s = script_builds_button(doc), len(re.findall(r'n6m-guide-btn', text))
        elif css is None:
            d = None
        else:
            d = len(doc.xpath(css))
        out.append((label, s, d, note))
    return out, doc


def live_text(k):
    return subprocess.check_output(['git', 'show', 'origin/main:' + LIVE[k]], cwd=str(REPO)).decode('utf-8')


def main():
    moved, satisfied = [], set()
    for k in 'AB':
        now = (REPO / LIVE[k]).read_text(encoding='utf-8')
        lc, ldoc = counts(live_text(k))
        nc, ndoc = counts(now)
        ld_, nd_ = denominators(ldoc), denominators(ndoc)
        print('=== %s  ·  substring vs DOM, live vs now ===' % k)
        print('   examined %d markers against %d elements (%d with a class), %d ids '
              '(%d unique), %d scripts   [live: %d elements, %d ids]'
              % (nd_['markers_examined'], nd_['elements'], nd_['elements_with_class'],
                 nd_['ids'], nd_['unique_ids'], nd_['scripts'],
                 ld_['elements'], ld_['ids']))
        if not nd_['elements'] or not nd_['ids']:
            print('   [DENOMINATOR ZERO] the parse saw nothing -- every count below is vacuous')
            moved.append('%s DENOMINATOR ZERO' % k)
        print('   %-26s %-13s %-13s' % ('marker', 'LIVE sub/dom', 'NOW sub/dom'))
        for (lab, ls, ld, note), (_, ns, nd, _n) in zip(lc, nc):
            disagree = (ld is not None and ls != ld) or (nd is not None and ns != nd)
            drop = (ld not in (None, 0) and nd == 0)
            if drop:
                moved.append('%s %s' % (k, lab))
            print('   %-26s %-13s %-13s%s%s'
                  % (lab, '%s / %s' % (ls, '-' if ld is None else ld),
                     '%s / %s' % (ns, '-' if nd is None else nd),
                     '   <-- SUB≠DOM' if disagree else '',
                     '   <-- DROPPED' if drop else ''))
            if note and (lab.endswith('(name)') or lab.endswith('(key)')):
                print('   %-26s   %s' % ('', note))
        # Declared equivalences, checked rather than trusted.
        by_label_live = {r[0]: r[2] for r in lc}
        by_label_now = {r[0]: r[2] for r in nc}
        for gone, arrived, why, reader in EQUIVALENCE:
            lg, ng = by_label_live.get(gone), by_label_now.get(gone)
            na = by_label_now.get(arrived)
            if lg and not ng:
                same_count = na == lg
                # the second half: is the code that read the old attribute gone?
                reader_live = len(re.findall(re.escape(reader), live_text(k)))
                reader_now = len(re.findall(re.escape(reader), now))
                orphaned = reader_now > 0
                ok = same_count and not orphaned
                print('   EQUIVALENCE %s -> %s : live %s hosts, now %s   reader %r '
                      'live %d / now %d   %s'
                      % (gone, arrived, lg, na, reader, reader_live, reader_now,
                         'HOLDS' if ok else 'DOES NOT HOLD'))
                print('   %-26s   %s' % ('', why))
                if orphaned:
                    print('   %-26s   ORPHANED READER: code still asks for the '
                          'attribute that went away' % '')
                satisfied.add('%s %s' % (k, gone))
                if not ok:
                    moved.append('%s %s (equivalence failed)' % (k, arrived))
        # H5
        ids = ndoc.xpath('//*[@id]')
        vals = [e.get('id') for e in ids]
        deck = ndoc.xpath(cls('main', 'slide-container'))
        print('   H5: duplicate ids %d of %d ids examined · main.slide-container '
              'resolves %d · #lessonDeck is that element %s'
              % (len(vals) - len(set(vals)), len(vals), len(deck),
                 bool(deck) and deck[0].get('id') == 'lessonDeck'))
        print()
    unexplained = [m for m in moved if m not in satisfied]
    explained = [m for m in moved if m in satisfied]
    if explained:
        print('CARRIED MARKERS ABSENT BUT EXPLAINED BY A CHECKED EQUIVALENCE:', explained)
    print('ROWS WHERE A CARRIED MARKER IS ABSENT AND UNEXPLAINED:', unexplained or 'none')
    return 1 if unexplained else 0


if __name__ == '__main__':
    sys.exit(main())
