#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ORDER N6-Z · Z3 — apply PH-3's guidance toggle to the nine landed packs.

THE MECHANISM IS PH-3's, NOT A NEW ONE. data-mbm-guide="staff|route|lundy",
hidden unless html.mbm-guide-on, an "ⓘ Guidance" button, key G, localStorage
mbm_guide_v1, default hidden, hidden and not removed. The CSS/JS/BUTTON strings
below are PH-3's own, taken from _eca1/tools/guidepatch.js rather than retyped.

THE PATCHER IS NEW, BECAUSE PH-3's CANNOT SEE THESE FILES. It classifies by
.li-box/.task-box/.wit-panel, which occur 0 times across all 159 files.

THE HIDE-SET IS KEYED TO ADDRESSEE, not to string families. That is the whole
lesson of I5's first pass, which asked for a list of SoW-provenance phrases and
concluded eight of nine packs had nothing on screen. The question for every
candidate is "who is this sentence talking to?".

ONE ADDITION TO PH-3's CSS, AND IT IS LOAD-BEARING. A print exemption:

    @media print{html:not(.mbm-guide-on) [data-mbm-guide]{display:revert!important}}

The order predicts that "print CSS hides the slide container, so slide-side
tagging must never reach it", and says to assert that rather than reason about
it. Asserted, it is FALSE for two packs: GROW_ASDAN and LAUNCH_ASDAN both carry
an @media print rule that reveals `.slide` (LAUNCH_ASDAN's is N6-I's own N3
addendum, added so the deck would print at all). In those 48 decks a slide-side
tag WOULD reach the printed page, and with the toggle defaulting to hidden it
would delete staff content from paper that used to carry it. The exemption keeps
the toggle a screen affordance and leaves print byte-identical, which is what
the order's own gate requires. Without it that gate cannot pass.

Idempotent, markered, strip-reversible.
"""
import glob
import json
import os
import re
import sys

OPEN = '<!--n6z-guide:v1-->'
CLOSE = '<!--/n6z-guide-->'

# --- PH-3's own runtime, verbatim from _eca1/tools/guidepatch.js -------------
STYLE = ('<style id="mbm-guide-css">html:not(.mbm-guide-on) [data-mbm-guide]'
         '{display:none!important}'
         '.mbm-guide-btn[aria-pressed="true"]{box-shadow:inset 0 0 0 2px currentColor}'
         '@media print{html:not(.mbm-guide-on) [data-mbm-guide]{display:revert!important}}'
         '</style>')
BUTTON = ('<button class="mbm-guide-btn" type="button" aria-pressed="false" '
          'onclick="mbmGuideToggle()">ⓘ Guidance</button>')
SCRIPT = """<script id="mbm-guide-js">
(function(){
  var KEY='mbm_guide_v1';
  function stored(){try{return localStorage.getItem(KEY)==='1'}catch(e){return false}}
  function store(on){try{localStorage.setItem(KEY,on?'1':'0')}catch(e){}}
  function apply(on){
    document.documentElement.classList.toggle('mbm-guide-on',on);
    var b=document.querySelector('.mbm-guide-btn');
    if(b){b.setAttribute('aria-pressed',on?'true':'false');b.textContent=on?'ⓘ Guidance ✓':'ⓘ Guidance';}
    var live=document.getElementById('vu-live-region');
    if(live)live.textContent=on?'Guidance shown':'Guidance hidden';
  }
  window.mbmGuideToggle=function(){var on=!document.documentElement.classList.contains('mbm-guide-on');store(on);apply(on);};
  document.addEventListener('keydown',function(e){
    if(e.key!=='g'&&e.key!=='G')return;
    var t=e.target;
    if(t&&(t.tagName==='INPUT'||t.tagName==='TEXTAREA'||t.isContentEditable))return;
    if(document.querySelector('dialog[open],.overlay.visible,.overlay.open,.v4-modal-overlay.visible,.mbm-modal.open'))return;
    window.mbmGuideToggle();
  });
  apply(stored());
})();
</script>"""

# --- THE ADDRESSEE PREDICATE ------------------------------------------------
# The question for every candidate element is "who is this sentence talking to?".
# Measured per INSTANCE, never per class: five of the classes the tag map called
# clean are mixed at instance level, and tagging them class-wide would have
# hidden pupil content.
#
#   .guard          44 staff / 30 not — one of the not-staff is a Lundy INFLUENCE
#                   zone box, which this order says stays visible
#   .evidence-note  18 / 18 — the other half is the offline notice "This file
#                   stores, uploads and scores nothing", which is not guidance
#   .screen         30 / 30 — likewise "Screen-only: The page stores and uploads
#                   nothing"
#   .small          the nine that first read as non-staff are "Secondary estate
#                   continuity metadata: Weeks 9-14", which IS staff; the probe
#                   lacked the phrase, not the file
#   .lnote          reads as mixed to a narrow probe and is NOT: every instance is
#                   a delivery note to the adult ("Teacher models disciplinary
#                   craft; staff watch access and pupil ownership")
STAFF_ADDRESSEE = re.compile(
    r'\b(Staff|Adult|Teacher|TA)\b|\b(staff|adult|teacher)\b|Named-adult|'
    r'assessor|moderat|scrib|co-regulate|least[- ]prompt|Do not reveal|'
    r'before delivery|before giving this page|pre-stage|report-back|'
    r'qualification boundary|Teaching / qualification|Evidence boundary|'
    r'Authorship check|Potential evidence only|not qualification evidence|'
    r'Registration, selected unit|continuity metadata|Sequence outcome:|'
    r'Exact SOW outcome|Estate sequence|Weekly - (Autumn|Spring|Summer)|'
    r'Learner owns|Learners can question|Pupil authors|Pupil question or inference|'
    r'Retrieve without forced disclosure|Predictable phases|Quiet response time|'
    r'A second model shows|The interactive makes|The interface helps thinking|'
    r'One Lundy loop only|One response genuinely received')

# Not guidance, whoever it addresses: the offline/technical notices. Hiding these
# would remove a safeguarding-adjacent statement behind a toggle that is off by
# default, which is the opposite of what the toggle is for.
NOT_GUIDANCE = re.compile(
    r'^(This file stores|Screen-only:|This page stores|The page stores)')

# The pupil-facing Lundy zone strip stays visible, per the order. Exactly one
# candidate was found sitting in one: a GROW_ASDAN `.guard` whose text begins
# "INFLUENCE · Use the learner's comparison to select the Autumn 2 Week 2
# examples…" — staff-worded, but inside a box a pupil is reading, so punching it
# out would leave a hole in the middle of the zone strip.
#
# A first attempt excluded anything within 2500 characters of a `.lundy` open
# tag. That blocked 100% of candidates in three packs, because these decks carry
# `.lundy` containers throughout — a window is not a containment test. Matching
# the zone label at the START of the element's own text is precise and is what
# the observed case actually looks like.
LUNDY_ZONE_HEAD = re.compile(r'^(SPACE|VOICE|AUDIENCE|INFLUENCE)\b', re.I)


# --- THE HIDE-SET, per pack, keyed to addressee -----------------------------
# Each entry: (css-ish selector kind, value, role, why-it-is-staff-addressed)
# 'class'      every element carrying the class
# 'class+label' elements of the class whose leading <strong>/<b> label is in the list
# 'class+text' elements of the class whose text starts with one of these
# 'lastchip'   the final .chip inside .chips
# 'p-strong'   an unclassed <p> whose leading <strong> matches
HIDE = {
    'BUILD_ASDAN/Autumn2_W1-W6_2026-27': [
        ('lastchip', None, 'route', 'the internal estate-sequence number; the three chips before it are the lane, unit and week a pupil reads'),
        ('class+addr', 'small', 'route', 'the SoW workbook cell reference — "Source: \'BUILD Weekly - Autumn\'!B181"'),
        ('class+addr', 'lesson-link', 'route', 'estate sequence plus SoW cell, on the index card'),
        ('p-strong', ['Exact SOW outcome:'], 'route', 'the SoW cell text, unclassed, inside .hero'),
        ('class+label', ('objective', ['SPACE routine', 'Model aloud:', 'Connect:']), 'staff',
         'room set-up, what to model aloud, what to connect — the fourth .box.objective is the pupil’s Learning objective:'),
        ('class+label', ('good', ['Adult close', 'Authorship check:']), 'staff',
         'a script for the adult’s closing turn, and a staff moderation rule'),
        ('class+text', ('rehearsal', ['Do not reveal the pupil']), 'staff',
         'an instruction to whoever is driving the model; the other 96 .box.rehearsal are pupil-protective'),
    ],
    'GROW_ASDAN/Autumn2_W1-W6_2026-27': [
        ('class+addr', 'choose', 'staff', '"Staff: select one route before giving this page to the learner."'),
        ('class+addr', 'staff', 'staff', '"Staff pre-stage before the 16-minute transfer…"'),
        ('class+addr', 'guard', 'staff', 'teaching / qualification boundary, addressed to the adult'),
        ('class+addr', 'evidence-note', 'staff', 'what does and does not count as evidence — an assessor note'),
        ('class+addr', 'boundary', 'staff', 'evidence boundary, addressed to the adult'),
    ],
    'LAUNCH_ASDAN/W7-W12_2026-27': [
        ('class+addr', 'screen', 'staff', '"Authorship check: Staff may model the process and preserve access…"'),
    ],
    'Science_Teesside/Build/W8-W13_2026-27':  [('class+addr', 'sowline', 'route', 'the SoW sequence outcome line')],
    'Science_Teesside/Grow/W8-W13_2026-27':   [('class+addr', 'sowline', 'route', 'the SoW sequence outcome line')],
    'Science_Teesside/Launch/W8-W13_2026-27': [('class+addr', 'sowline', 'route', 'the SoW sequence outcome line')],
    'Humanities_Teesside/BUILD_W9-W14_2026-27': [
        ('class+addr', 'reportback', 'staff', '"Decision maker: Class teacher — replace with the adult’s name before delivery."'),
        ('class+addr', 'lnote', 'staff', 'a design note about the Lundy loop, addressed to staff — NOT the pupil-facing .lundy zone strip, which stays'),
    ],
    'Humanities_Teesside/GROW_W9-W14_2026-27': [
        ('class+addr', 'lnote', 'staff', 'staff design note; the .lundy zone strip stays visible'),
    ],
    'Humanities_Teesside/LAUNCH_W9-W14_2026-27': [
        ('class+addr', 'lnote', 'staff', 'staff design note; the .lundy zone strip stays visible'),
        ('class+addr', 'mobile-teacher-tools', 'staff', '"Teacher tools"'),
    ],
}

TAG = re.compile(r'<(?P<tag>[a-z]+)(?P<attrs>[^>]*)>', re.I)


def _has_class(attrs, cls):
    m = re.search(r'class="([^"]*)"', attrs)
    return bool(m) and cls in m.group(1).split()


def _leading_label(html_after):
    m = re.match(r'\s*<(?:strong|b)>(.*?)</(?:strong|b)>', html_after, re.S)
    return re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else None


def _add_attr(open_tag, role):
    if 'data-mbm-guide' in open_tag:
        return open_tag, False
    return re.sub(r'^(<[a-z]+)', r'\1 data-mbm-guide="%s"' % role, open_tag, count=1, flags=re.I), True


def patch_text(s, rules):
    """Return (new_html, per-rule counts). Only opening tags are rewritten."""
    counts = {}
    for kind, val, role, _why in rules:
        n = 0
        if kind == 'class':
            out, i = [], 0
            for m in TAG.finditer(s):
                if not _has_class(m.group('attrs'), val):
                    continue
                new, done = _add_attr(m.group(0), role)
                if done:
                    out.append((m.start(), m.end(), new)); n += 1
            for a, b, new in reversed(out):
                s = s[:a] + new + s[b:]
        elif kind == 'class+label':
            cls, labels = val
            out = []
            for m in TAG.finditer(s):
                if not _has_class(m.group('attrs'), cls):
                    continue
                lab = _leading_label(s[m.end():m.end() + 260])
                if lab is None or not any(lab.startswith(x.rstrip(':')) for x in labels):
                    continue
                new, done = _add_attr(m.group(0), role)
                if done:
                    out.append((m.start(), m.end(), new)); n += 1
            for a, b, new in reversed(out):
                s = s[:a] + new + s[b:]
        elif kind == 'class+addr':
            # Per-instance addressee test, plus the two exclusions above.
            out = []
            for m in TAG.finditer(s):
                if not _has_class(m.group('attrs'), val):
                    continue
                body = re.sub(r'<[^>]+>', ' ', s[m.end():m.end() + 700])
                body = re.sub(r'\s+', ' ', body).strip()
                if NOT_GUIDANCE.match(body):
                    continue
                if not STAFF_ADDRESSEE.search(body):
                    continue
                if LUNDY_ZONE_HEAD.match(body):
                    continue
                new, done = _add_attr(m.group(0), role)
                if done:
                    out.append((m.start(), m.end(), new)); n += 1
            for a, b, new in reversed(out):
                s = s[:a] + new + s[b:]
        elif kind == 'class+text':
            cls, starts = val
            out = []
            for m in TAG.finditer(s):
                if not _has_class(m.group('attrs'), cls):
                    continue
                body = re.sub(r'<[^>]+>', '', s[m.end():m.end() + 300]).strip()
                if not any(body.startswith(x) for x in starts):
                    continue
                new, done = _add_attr(m.group(0), role)
                if done:
                    out.append((m.start(), m.end(), new)); n += 1
            for a, b, new in reversed(out):
                s = s[:a] + new + s[b:]
        elif kind == 'lastchip':
            out = []
            for cm in re.finditer(r'<div[^>]*class="[^"]*\bchips\b[^"]*"[^>]*>', s):
                end = s.find('</div>', cm.end())
                # the chips row is flat: take the last <span class="chip"> before it
                chips = list(re.finditer(r'<span[^>]*class="[^"]*\bchip\b[^"]*"[^>]*>', s[cm.end():end + 6]))
                if not chips:
                    continue
                last = chips[-1]
                a = cm.end() + last.start(); b = cm.end() + last.end()
                new, done = _add_attr(s[a:b], role)
                if done:
                    out.append((a, b, new)); n += 1
            for a, b, new in reversed(out):
                s = s[:a] + new + s[b:]
        elif kind == 'p-strong':
            out = []
            for m in re.finditer(r'<p>(?=\s*<strong>)', s):
                lab = _leading_label(s[m.end():m.end() + 200])
                if lab is None or not any(lab.startswith(x.rstrip(':')) for x in val):
                    continue
                new, done = _add_attr('<p>', role)
                if done:
                    out.append((m.start(), m.end(), new)); n += 1
            for a, b, new in reversed(out):
                s = s[:a] + new + s[b:]
        counts[str((kind, val if not isinstance(val, tuple) else val[0], role))] = n
    return s, counts


def controls_anchor(s):
    """Where the ⓘ Guidance button goes: inside the deck's own control bar."""
    for rx in (r'<div[^>]*class="[^"]*\bcontrols\b[^"]*"[^>]*>',
               r'<nav[^>]*class="[^"]*\bcontrols\b[^"]*"[^>]*>',
               r'<div[^>]*class="[^"]*\btoolbar\b[^"]*"[^>]*>',
               r'<footer[^>]*>'):
        m = re.search(rx, s)
        if m:
            return m.end()
    return None


def strip(s):
    i = s.find(OPEN)
    if i >= 0:
        j = s.index(CLOSE, i) + len(CLOSE)
        s = s[:i] + s[j:]
    s = re.sub(r'\s*data-mbm-guide="(?:staff|route|lundy)"', '', s)
    s = s.replace(BUTTON, '')
    return s


# Assessor-side and front-door surfaces are never touched. The same exclusion the
# N2 port used, plus the Science practicals matrix and the teacher planning SoW.
NEVER = re.compile(
    r'^(index\.html|START_HERE.*|STAFF_GUIDE\.html|STAFF_ONLY_.*|TEACHER_.*|'
    r'SCHEME_OF_WORK\.html|SOURCE_PROVENANCE_REGISTER\.html|SOURCE_REGISTER\.html|'
    r'LOCAL_SOURCE_CARDS_.*|PRACTICALS_MATRIX\.html|PRINTABLE_RESOURCES\.html|'
    r'.*_TEACHER_PLANNING_SOW\.html|.*_EVIDENCE_WINDOW\.html|'
    r'.*_SAME_DAY_EVIDENCE\.html|.*_PORTFOLIO_STUDIO\.html|.*_Hub\.html|'
    r'Resources_and_Tools\.html|VISUAL_UPGRADE_GUIDE\.html|QA_REPORT\.html|README.*)$', re.I)


def run(root, rules, dry=False, revert=False):
    files = [f for f in sorted(glob.glob(os.path.join(root, '**', '*.html'), recursive=True))
             if not NEVER.match(os.path.basename(f))]
    tally = {'files': 0, 'tagged': 0, 'perRule': {}, 'noAnchor': [], 'skipped': 0}
    for f in files:
        s0 = open(f, encoding='utf-8').read()
        if revert:
            s = strip(s0)
            if s != s0 and not dry:
                open(f, 'w', encoding='utf-8').write(s)
            tally['files'] += 1 if s != s0 else 0
            continue
        if OPEN in s0:
            tally['skipped'] += 1
            continue
        s, counts = patch_text(s0, rules)
        total = sum(counts.values())
        for k, v in counts.items():
            tally['perRule'][k] = tally['perRule'].get(k, 0) + v
        if total == 0:
            continue
        anchor = controls_anchor(s)
        if anchor is None:
            tally['noAnchor'].append(os.path.basename(f))
            btn = ''
        else:
            btn = BUTTON
            s = s[:anchor] + btn + s[anchor:]
        if '</head>' not in s:
            tally['noAnchor'].append(os.path.basename(f) + ' (no head)')
            continue
        s = s.replace('</head>', OPEN + STYLE + '</head>', 1)
        s = s.replace('</body>', SCRIPT + CLOSE + '</body>', 1)
        if not dry:
            open(f, 'w', encoding='utf-8').write(s)
        tally['files'] += 1
        tally['tagged'] += total
    return tally


if __name__ == '__main__':
    dry = '--dry' in sys.argv
    revert = '--strip' in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    grand = 0
    for root, rules in HIDE.items():
        if only and not any(o in root for o in only):
            continue
        t = run(root, rules, dry, revert)
        grand += t['tagged']
        print('%-46s files=%-3d tagged=%-4d skipped=%-3d %s'
              % (root.split('/')[-2] + '/' + root.split('/')[-1], t['files'], t['tagged'],
                 t['skipped'], ('NO ANCHOR: ' + ', '.join(t['noAnchor'])) if t['noAnchor'] else ''))
        for k, v in sorted(t['perRule'].items()):
            if v:
                print('      %-70s %d' % (k[:70], v))
    print('TOTAL tagged: %d' % grand)
