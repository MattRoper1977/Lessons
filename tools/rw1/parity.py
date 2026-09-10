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
 ('[data-ta1]',             r'data-ta1=',                   '//*[@data-ta1]',                   None),
 ('[data-prompt]',          r'data-prompt=',                '//*[@data-prompt]',                None),
 ('[data-mbm-guide=staff]', r'data-mbm-guide="staff"',      "//*[@data-mbm-guide='staff']",     None),
 ('.teacher-only',          r'class="[^"]*teacher-only',    cls('*','teacher-only'),            None),
 ('button.n6m-guide-btn',   r'n6m-guide-btn',               cls('button','n6m-guide-btn'),      None),
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


def counts(text):
    doc = doc_of(text)
    out = []
    for label, sub, css, note in ROWS:
        s = len(re.findall(sub, text))
        if label == 'script holding the key':
            d, s = script_with_key(doc), len(re.findall(r'mbm_guide_v1', text))
        elif css is None:
            d = None
        else:
            d = len(doc.xpath(css))
        out.append((label, s, d, note))
    return out, doc


def live_text(k):
    return subprocess.check_output(['git', 'show', 'origin/main:' + LIVE[k]], cwd=str(REPO)).decode('utf-8')


def main():
    moved = []
    for k in 'AB':
        now = (REPO / LIVE[k]).read_text(encoding='utf-8')
        lc, ldoc = counts(live_text(k))
        nc, ndoc = counts(now)
        print('=== %s  ·  substring vs DOM, live vs now ===' % k)
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
        # H5
        ids = ndoc.xpath('//*[@id]')
        vals = [e.get('id') for e in ids]
        deck = ndoc.xpath(cls('main', 'slide-container'))
        print('   H5: duplicate ids %d · main.slide-container resolves %d · #lessonDeck is that element %s'
              % (len(vals) - len(set(vals)), len(deck),
                 bool(deck) and deck[0].get('id') == 'lessonDeck'))
        print()
    print('ROWS WHERE A CARRIED MARKER IS ABSENT:', moved or 'none')
    return 1 if moved else 0


if __name__ == '__main__':
    sys.exit(main())
