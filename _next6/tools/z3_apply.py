#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ORDER N6-Z · Z3 — apply PH-3's guidance toggle from the browser-made selection.

Selection is z3_select.mjs's job (a real DOM: visibility, ancestry, addressee).
This applies it: one `data-mbm-guide` attribute per selected element, plus PH-3's
own CSS, button and script.

Matching back to source: each selection carries `tag|classAttr` and the element's
index among all elements sharing that signature. Opening tags appear in source in
DOM order, so the nth matching open tag in the file is the nth element. Asserted
per file — if the counts disagree the file is skipped and reported, never
patched on a guess.

THE PRINT EXEMPTION IS LOAD-BEARING. The order predicts "print CSS hides the
slide container, so slide-side tagging must never reach it" and says to assert
that. Asserted: FALSE for GROW_ASDAN and LAUNCH_ASDAN, both of which carry an
@media print rule that reveals `.slide` (LAUNCH_ASDAN's is N6-I's own N3
addendum, added so the deck would print at all). In those 48 decks a slide-side
tag would reach paper, and with the toggle defaulting to hidden it would delete
staff content from a printed artefact that used to carry it. Hence:

    @media print{html:not(.mbm-guide-on) [data-mbm-guide]{display:revert!important}}

which keeps the toggle a screen affordance and leaves print byte-identical —
which is the order's own gate. Without it that gate cannot pass.
"""
import json
import os
import re
import sys

# TWO SELF-CONTAINED MARKED BLOCKS, not one pair bracketing the document.
# A first version opened before </head> and closed before </body>, so strip()
# removed everything between them — the entire body. The reversibility gate
# caught it on the first run: 0 of 126 files stripped back to their pre-patch
# bytes, every one 40KB short. Markers must wrap what they own and nothing else.
HEAD_OPEN, HEAD_CLOSE = '<!--n6z-guide-css:v1-->', '<!--/n6z-guide-css-->'
BODY_OPEN, BODY_CLOSE = '<!--n6z-guide-js:v1-->', '<!--/n6z-guide-js-->'

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


def open_tags(s, tag, cls):
    """Every opening `<tag ...>` whose class attribute is exactly `cls`.

    `cls` of '' means the element carries NO class attribute — the signature the
    browser produces for an unclassed node. Requiring a class="" match there
    found zero candidates and the applier correctly refused to patch rather than
    guessing at the nearest <p>; the "Exact SOW outcome" paragraph is unclassed,
    so this is the common case, not an edge one.
    """
    rx = re.compile(r'<%s(\s[^>]*)?>' % re.escape(tag), re.I)
    out = []
    for m in rx.finditer(s):
        a = m.group(1) or ''
        cm = re.search(r'class="([^"]*)"', a)
        if cls == '':
            if cm is None:
                out.append(m)
        elif cm and cm.group(1) == cls:
            out.append(m)
    return out


def controls_anchor(s):
    for rx in (r'<div[^>]*class="[^"]*\bcontrols\b[^"]*"[^>]*>',
               r'<nav[^>]*class="[^"]*\bcontrols\b[^"]*"[^>]*>',
               r'<div[^>]*class="[^"]*\btoolbar\b[^"]*"[^>]*>',
               r'<div[^>]*class="[^"]*\bdeck-controls\b[^"]*"[^>]*>'):
        m = re.search(rx, s)
        if m:
            return m.end()
    return None


def strip(s):
    for a, b in ((HEAD_OPEN, HEAD_CLOSE), (BODY_OPEN, BODY_CLOSE)):
        i = s.find(a)
        if i >= 0:
            j = s.index(b, i) + len(b)
            s = s[:i] + s[j:]
    s = re.sub(r' data-mbm-guide="(?:staff|route|lundy)"', '', s)
    s = s.replace(BUTTON, '')
    return s


def main():
    selpath = sys.argv[1]
    dry = '--dry' in sys.argv
    revert = '--strip' in sys.argv
    sel = json.load(open(selpath))
    stats = {'files': 0, 'tagged': 0, 'skipped': 0, 'mismatch': [], 'noAnchor': []}

    targets = sel.keys() if not revert else None
    if revert:
        import glob
        targets = [f for f in glob.glob('**/*.html', recursive=True)
                   if HEAD_OPEN in open(f, encoding='utf-8', errors='ignore').read()]
    for f in sorted(targets):
        s0 = open(f, encoding='utf-8').read()
        if revert:
            s = strip(s0)
            if s != s0 and not dry:
                open(f, 'w', encoding='utf-8').write(s)
            stats['files'] += 1
            continue
        items = sel[f]
        if not isinstance(items, list):
            stats['mismatch'].append((f, 'selector error')); continue
        if HEAD_OPEN in s0:
            stats['skipped'] += 1; continue

        # group by signature so indices are applied against the right list
        bysig = {}
        for it in items:
            bysig.setdefault(it['sig'], []).append(it)
        edits = []
        bad = False
        for sig, group in bysig.items():
            tag, cls = sig.split('|', 1)
            found = open_tags(s0, tag, cls)
            for it in group:
                if it['idx'] >= len(found):
                    stats['mismatch'].append((f, '%s idx %d of %d' % (sig, it['idx'], len(found))))
                    bad = True; break
                m = found[it['idx']]
                if 'data-mbm-guide' in m.group(0):
                    continue
                new = re.sub(r'^(<[a-zA-Z]+)', r'\1 data-mbm-guide="%s"' % it['role'],
                             m.group(0), count=1)
                edits.append((m.start(), m.end(), new))
            if bad:
                break
        if bad:
            continue
        # DEDUPE BY SPAN. Two rules can legitimately select the same element —
        # BUILD_ASDAN's `p.small` and `.hero p` (label "Source:") both reach the
        # SoW cell-reference paragraph. Applying both edits to one span produced
        # `<p class="small">="route" class="small">`, a corrupted tag that the
        # reversibility gate caught as 24 files failing to strip back. One edit
        # per element, first rule wins.
        seen_spans = set()
        deduped = []
        for a, b, new in edits:
            if a in seen_spans:
                continue
            seen_spans.add(a)
            deduped.append((a, b, new))
        edits = deduped
        edits.sort(key=lambda e: -e[0])
        s = s0
        for a, b, new in edits:
            s = s[:a] + new + s[b:]

        anchor = controls_anchor(s)
        if anchor is None:
            stats['noAnchor'].append(os.path.basename(f))
        else:
            s = s[:anchor] + BUTTON + s[anchor:]
        if '</head>' not in s or '</body>' not in s:
            stats['mismatch'].append((f, 'no head/body')); continue
        s = s.replace('</head>', HEAD_OPEN + STYLE + HEAD_CLOSE + '</head>', 1)
        s = s.replace('</body>', BODY_OPEN + SCRIPT + BODY_CLOSE + '</body>', 1)
        if not dry:
            open(f, 'w', encoding='utf-8').write(s)
        stats['files'] += 1
        stats['tagged'] += len(edits)

    print('files=%d tagged=%d skipped=%d mismatch=%d noAnchor=%d'
          % (stats['files'], stats['tagged'], stats['skipped'],
             len(stats['mismatch']), len(stats['noAnchor'])))
    for f, why in stats['mismatch'][:10]:
        print('   MISMATCH %s : %s' % (os.path.basename(f), why))
    if stats['noAnchor']:
        print('   no controls anchor (button not placed): %d files, e.g. %s'
              % (len(stats['noAnchor']), ', '.join(stats['noAnchor'][:4])))
    return 1 if stats['mismatch'] else 0


if __name__ == '__main__':
    sys.exit(main())
