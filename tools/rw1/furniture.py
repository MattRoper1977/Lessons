#!/usr/bin/env python3
"""RW1 D5/D6 as corrected by RW1-A §D: carry the estate furniture from the LIVE
file, verbatim, never authored.

STRUCK from the original D6 by measurement (RW1-A D1/D2), and deliberately NOT
carried here:
  usage.css, usage-client.js, lesson-navigation.js -- the PUBLISHER injects these.
    Proved on a real build of this very route: source 0, built 1 for each. Writing
    them into source would duplicate the injection, and build_education's
    with_lesson_navigation raises ValueError on a duplicate adapter.
  rel="canonical" -- absent from source AND built. Nothing to carry.

Everything below is lifted out of the live file at origin/main by marker, so a
change to the estate's furniture reaches these two lessons the next time this
runs rather than being frozen as a copy.
"""
import re, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pathways


def live_text(which, pw):
    return subprocess.check_output(
        ['git', 'show', 'origin/main:' + pathways.need(pw, 'live', which)],
        cwd=str(Path(__file__).resolve().parents[2])
    ).decode('utf-8')


def _span(s, open_pat, close_lit):
    i = s.find(open_pat)
    if i < 0:
        return None
    j = s.find(close_lit, i)
    return s[i:j + len(close_lit)] if j >= 0 else None


def parts(which, pw):
    s = live_text(which, pw)
    body = re.search(r'<body([^>]*)>', s)
    # Balanced walk, not "the first </div> after </svg>". That shortcut closed the
    # INNER div and left <div class="n6-splash"> open, so every element after it --
    # including the prev/next row -- became a child of the splash, which the print
    # CSS hides. The browser auto-closed the tag, so it still RENDERED; only a
    # balance check finds it.
    splash = None
    k = s.find('<div class="n6-splash"')
    if k >= 0:
        depth, i = 0, k
        while i < len(s):
            if s.startswith('<div', i):
                depth += 1; i += 4
            elif s.startswith('</div>', i):
                depth -= 1; i += 6
                if depth == 0:
                    splash = s[k:i]; break
            else:
                i += 1
    skip = re.search(r'<a class="skip"[^>]*>[^<]*</a>', s)
    # The CSS for the carried furniture lives in the LIVE FILE'S OWN <style>, not
    # in the 411-byte nav block, and the packs have none of it. Carrying the
    # markup without these rules ships a permanently visible "Skip to lesson"
    # link on every pupil route -- .skip is position:fixed;left:-9999px until
    # :focus -- and an unstyled prev/next row.
    #
    # render_check.cjs passed it: the link existed and moved focus, which is what
    # it asks. Neither question is "is it off screen until focused". Evidence,
    # not proxy -- the rendered position is now asserted, see the same file.
    # SINGLE selectors only, and never a grouped one. The first version allowed
    # a comma-separated group and included .mbmhome, so it lifted
    #   @media print{.mbmhome,.n6-splash{display:none!important}}
    # out of its @media wrapper and pasted the inner rule into the top-level
    # sheet -- which hid the splash on screen, on all seven files. The render
    # check caught it (splash visible false) within a minute of the previous fix.
    # A rule inside @media cannot be carried by copying its body; carry only what
    # is safe to carry, and .mbmhome is already handled by the nav block anyway.
    CSS_WANTED = ('.skip', '.skip:focus', '.links', '.next-link',
                  '.next-link:hover', '.next-link:focus')
    css = ''
    for sel in CSS_WANTED:
        m = re.search(r'(?<![-\w.])' + re.escape(sel) + r'\s*\{[^}]*\}', s)
        if m:
            css += m.group(0)
    deck = re.search(r'<main id="lessonDeck"([^>]*)>', s)
    links = _span(s, '<div class="links">', '</div>')
    return dict(
        body_attrs=(body.group(1).strip() if body else ''),
        nav=_span(s, '<!--n6-nav1', '<!--/n6-nav1-->'),
        guide=_span(s, '<!--n6m-guide', '<!--/n6m-guide-->'),
        splash=splash,
        skip=(skip.group(0) if skip else None),
        deck_attrs=(deck.group(1).strip() if deck else ''),
        links=links,
        css=css,
    )


def carry(text, which, pw):
    p = parts(which, pw)
    missing = [k for k, v in p.items() if not v]
    # <body> data attributes: the guide, nav and pathway layers read them
    if p['body_attrs'] and 'data-lesson-id' not in text:
        text = re.sub(r'<body([^>]*)>', lambda m: '<body ' + p['body_attrs'] + '>', text, count=1)
    # head: the guide toggle, which is where the mbm_guide_v1 localStorage lives.
    # RULE B is amended by RW1-A D5 -- this storage is furniture and MUST be here.
    if p['guide'] and 'n6m-guide' not in text:
        text = text.replace('</head>', p['guide'] + '</head>', 1)
    # first thing in the body, exactly as live has it
    if p['nav'] and 'n6-nav1' not in text:
        add = p['nav'] + (p['skip'] or '')
        text = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + add, text, count=1)
    # The carried skip link points at #lessonDeck. The pack's deck is
    # <main class="slide-container"> with no id, so carrying the skip link alone
    # would have shipped a dangling anchor -- an accessibility regression
    # introduced BY the furniture carry. Give the deck the live deck's identity;
    # that also restores the second data-lesson-id the parity table flagged.
    if p['deck_attrs'] and 'id="lessonDeck"' not in text:
        text = re.sub(r'<main class="slide-container"([^>]*)>',
                      lambda m: '<main id="lessonDeck" class="slide-container deck" '
                                + p['deck_attrs'].replace('class="deck"', '').strip()
                                + m.group(1) + '>', text, count=1)
    # near the end of the body, as live has it
    # NOT 'n6-splash': the carried nav CSS mentions .n6-splash, so that guard was
    # already true and the splash div was silently never inserted.
    if p['splash'] and '<div class="n6-splash"' not in text:
        text = text.replace('</body>', p['splash'] + '</body>', 1)
    # the prev/next row. On W8B this row IS RW1 D3's reciprocal link, supplied by
    # the estate's own mechanism rather than by an invented anchor.
    if p['links'] and 'next-link' not in text:
        text = text.replace('</body>', p['links'] + '</body>', 1)
    # ...and the rules that make all of it behave. Last, so the guard sees the
    # markup that is actually present.
    if p['css'] and '.skip{' not in text:
        text = text.replace('</style>', p['css'] + '</style>', 1)
    return text, missing
