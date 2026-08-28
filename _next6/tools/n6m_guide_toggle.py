#!/usr/bin/env python3
"""ORDER N6-M §M3 — the guidance toggle, keyed to addressee.

MECHANISM (PH-3's, not PH-3's patcher — that one classifies all 192 files as
chassis doc under `.li-box`/`.task-box`/`.wit-panel`, which occur 0 times here):

    data-mbm-guide="staff|route|lundy"   on the element, hidden not removed
    hidden unless html.mbm-guide-on
    an "ⓘ Guidance" button, and the G key
    localStorage mbm_guide_v1, default hidden

THE HIDE-SET IS THE MAP'S, READ RATHER THAN PATTERN-MATCHED. Every family below
comes from _next6/GUIDE_TAG_MAP.md §5, where each was read in a browser to
confirm what the whole block says and who it is talking to. Ten are reachable by
a class that already exists; four need label- or position-keying because the
class is shared with pupil-facing content; one paragraph needed a marker.

WHAT IS DELIBERATELY NOT TAGGED, and why it matters more than what is:

  .model-step        144 instances, and they READ like staff step-by-step
                     instructions, so any "Step"/"How it works" rule catches
                     them. Measured, they are 49-58% of their slide's text.
                     Hiding them halves two slides in every deck.
  .box.objective     class-wide would delete the pupil's "Learning objective:"
                     from every deck. Only the three staff labels are tagged.
  .box.good          "Success criteria" is the pupil's. Only "Authorship check:"
                     and "Adult close" are tagged.
  .box.rehearsal     96 of 120 are pupil-protective. Only the one staff string is.
  the TA layer       1188 data-ta1/data-ta2 strings already reach no screen. A
                     toggle for them would be theatre.

PRINT IS UNTOUCHED BY CONSTRUCTION. Every rule is inside `@media screen`, so the
attribute is inert on paper and the printed page cannot change. That is asserted
with n6m_print_equal.py rather than argued.

Idempotent, and strip-reversible: the head block is comment-marked and every
attribute is removable, so stripping returns the file byte-identical.
"""
import os, re, sys, glob

OPEN, CLOSE = '<!--n6m-guide:v1-->', '<!--/n6m-guide-->'
ATTR = re.compile(r'\s+data-mbm-guide="(?:staff|route|lundy)"')

CSS = (
    '<style id="n6m-guide-css">@media screen{'
    '[data-mbm-guide]{display:none!important}'
    'html.mbm-guide-on [data-mbm-guide]{display:revert!important}'
    '.n6m-guide-btn{position:fixed;right:12px;bottom:12px;z-index:2147483000;'
    'font:600 .8rem/1.2 "Segoe UI",Arial,sans-serif;padding:7px 11px;'
    'border:2px solid currentColor;border-radius:8px;background:#fff;color:#1e3a8a;'
    'cursor:pointer}'
    '.n6m-guide-btn[aria-pressed="true"]{background:#1e3a8a;color:#fff}'
    '}@media print{.n6m-guide-btn{display:none!important}}</style>'
)

JS = (
    '<script id="n6m-guide-js">(function(){'
    'var K="mbm_guide_v1",R=document.documentElement;'
    'function get(){try{return localStorage.getItem(K)==="1"}catch(e){return false}}'
    'function set(v){try{localStorage.setItem(K,v?"1":"0")}catch(e){}}'
    'function apply(v){R.classList.toggle("mbm-guide-on",!!v);'
    'var b=document.querySelector(".n6m-guide-btn");'
    'if(b){b.setAttribute("aria-pressed",v?"true":"false");}}'
    'function toggle(){var v=!R.classList.contains("mbm-guide-on");set(v);apply(v);}'
    'function boot(){'
    'if(!document.querySelector("[data-mbm-guide]"))return;'
    'var b=document.createElement("button");b.type="button";'
    'b.className="n6m-guide-btn";b.setAttribute("aria-pressed","false");'
    'b.setAttribute("data-n6m-guide-control","1");'
    'b.title="Show or hide staff guidance (G)";b.textContent="\\u24D8 Guidance";'
    'b.addEventListener("click",toggle);document.body.appendChild(b);'
    'apply(get());'
    'document.addEventListener("keydown",function(e){'
    'if(e.key!=="g"&&e.key!=="G")return;'
    'if(e.metaKey||e.ctrlKey||e.altKey)return;'
    'var t=e.target,n=t&&t.tagName;'
    'if(n==="INPUT"||n==="TEXTAREA"||n==="SELECT"||(t&&t.isContentEditable))return;'
    'toggle();});}'
    'if(document.readyState==="loading")'
    'document.addEventListener("DOMContentLoaded",boot);else boot();'
    '})();</script>'
)

PAYLOAD = OPEN + CSS + JS + CLOSE

# --------------------------------------------------------------- the hide-set
# (pack-path fragment, kind, matcher). Matchers add the attribute to ONE opening
# tag each and are anchored on markup verified in GUIDE_TAG_MAP.md §5.
PLAIN = [
    ('GROW_ASDAN/Autumn2_W1-W6_2026-27', 'staff', ['choose', 'staff', 'guard',
                                                   'evidence-note', 'boundary']),
    ('LAUNCH_ASDAN/W7-W12_2026-27', 'staff', ['screen']),
    ('Humanities_Teesside/BUILD_W9-W14_2026-27', 'staff', ['reportback']),
    ('Humanities_Teesside/', 'lundy', ['lnote']),
    ('Science_Teesside/', 'route', ['sowline']),
    ('BUILD_ASDAN/Autumn2_W1-W6_2026-27', 'route', ['lesson-link']),
]

# BUILD_ASDAN label-keyed families: (kind, container-class, leading <strong> labels)
LABELLED = [
    ('staff', 'box objective', ['SPACE routine', 'Model aloud:', 'Connect:']),
    ('staff', 'box good', ['Authorship check:', 'Adult close']),
]
REHEARSAL_STAFF = "Do not reveal the pupil"


def class_token(c):
    """Match a class ATTRIBUTE whose token list contains exactly `c`.

    `\bstaff\b` is not good enough: a hyphen is a word boundary, so it also
    matches `staff-card`, `staff-note` and anything else sharing the stem. That
    over-match is the precise failure the map warns about — a rule that reaches
    past the family it was read for and hides content nobody checked.
    """
    return (r'<[a-z][a-z0-9]*\b[^>]*\bclass="(?:[^"]*\s)?%s(?:\s[^"]*)?"[^>]*>'
            % re.escape(c))


def tag_open(s, pattern, kind, limit=None):
    """Insert the attribute into the opening tag matched by `pattern` group 0."""
    n = 0
    out, pos = [], 0
    for m in re.finditer(pattern, s):
        if limit is not None and n >= limit:
            break
        tag = m.group(0)
        if 'data-mbm-guide' in tag:
            continue
        end = tag.index('>')
        out.append(s[pos:m.start()])
        out.append(tag[:end] + ' data-mbm-guide="%s"' % kind + tag[end:])
        pos = m.start() + len(tag)
        n += 1
    out.append(s[pos:])
    return ''.join(out), n


def patch(path, dry=False):
    s0 = open(path, encoding='utf-8').read()
    if OPEN in s0:
        return 'already', 0
    s = s0
    total = 0
    rel = path.replace(os.sep, '/')

    for frag, kind, classes in PLAIN:
        if frag not in rel:
            continue
        for c in classes:
            s, n = tag_open(s, class_token(c), kind)
            total += n

    if 'BUILD_ASDAN/Autumn2_W1-W6_2026-27' in rel:
        # the Source line — `.small` is the SoW citation in these decks
        s, n = tag_open(s, r'<p class="small"><strong>Source:</strong>', 'route')
        total += n
        # the Estate sequence chip: the last of four, matched on its own text
        s, n = tag_open(s, r'<span class="chip">Estate sequence\b[^<]*</span>', 'route')
        total += n
        # the authored marker: an unclassed <p> holding the SoW outcome
        s, n = tag_open(s, r'<p><strong>Exact SOW outcome:</strong>', 'route')
        total += n
        for kind, cls, labels in LABELLED:
            for lab in labels:
                s, n = tag_open(
                    s, r'<div class="%s"><strong>%s' % (re.escape(cls), re.escape(lab)),
                    kind)
                total += n
        # .box.rehearsal — only the one staff string of the 120
        s, n = tag_open(
            s, r'<div class="box rehearsal">(?=(?:(?!</div>).)*?%s)' % re.escape(REHEARSAL_STAFF),
            'staff')
        total += n

    if total == 0:
        return 'nothing-to-tag', 0
    if '</head>' not in s:
        return 'no-head', 0
    s = s.replace('</head>', PAYLOAD + '</head>', 1)
    if not dry:
        open(path, 'w', encoding='utf-8').write(s)
    return 'tagged', total


def strip(s):
    i = s.find(OPEN)
    if i >= 0:
        j = s.index(CLOSE, i) + len(CLOSE)
        s = s[:i] + s[j:]
    return ATTR.sub('', s)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    roots = args or ['.']
    do_strip, dry = '--strip' in sys.argv, '--dry' in sys.argv
    tally, marks = {}, 0
    for r in roots:
        for p in sorted(glob.glob(os.path.join(r, '**', '*.html'), recursive=True)):
            if do_strip:
                s = open(p, encoding='utf-8').read()
                o = strip(s)
                k = 'stripped' if o != s else 'clean'
                if o != s and not dry:
                    open(p, 'w', encoding='utf-8').write(o)
            else:
                k, n = patch(p, dry)
                marks += n
            tally[k] = tally.get(k, 0) + 1
    print('%s  %s%s' % (','.join(os.path.basename(r.rstrip('/')) for r in roots),
                        tally, '' if do_strip else '  · %d elements tagged' % marks))
