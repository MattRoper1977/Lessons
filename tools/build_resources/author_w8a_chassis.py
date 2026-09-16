#!/usr/bin/env python3
"""D-1 · re-dress the BUILD W8A Sugar Evidence lesson on the classroom chassis, from the committed bytes.

Bounded like tools/launch_resources/author_w4l1.py: the input is the source blob at BASE
(never the working copy), every edit anchors on an exact string that must occur exactly
once, and the whole file is regenerated on every run, so the tool is idempotent by
construction. Not one word of the lesson is composed here: every string the new chrome
shows is read out of the lesson's own slide 1 (title, objective, success criteria, the
review-meta line) or is the classroom shell's own furniture vocabulary.

What it does, in order (docs/orders/SERVED_DEFECTS_AMENDMENT_2026-09-16.md D-1, and the
twelve-agent design's area 5 port strategy — CHOOSE B, re-dress in place):
  chrome    the review shell's pale pill row goes: nav.review-top. Its four controls are
            rehoused, not invented, into the chassis's OWN toolbar — nav.classic-toolbar,
            whose CSS (fixed slot, 44px controls, phone breakpoint, print rule) is already
            in this file byte-for-byte and was dead while the review shell held the page.
            main#lessonDeck STAYS: it is a real landmark with an accessible name, the
            census classifies on #xpWrap + #lc-overlay before it ever looks at the deck
            tag, and the accepted browser harness selects through it. Body order, the
            classic shell's: a.edu-skip (kept), div.xp-wrap#xpWrap, div#auto-timer,
            nav.classic-toolbar, a lesson-specific <noscript>, main#lessonDeck,
            div.controls, div.progress-wrap#classic-progress[role=progressbar] (kept),
            div.progress-label, p#classic-status (kept), div#lc-overlay, div#mp-overlay,
            then the six <dialog>s and #print-area byte-for-byte unchanged.
  engine    kept. The lesson's own engine already carries the repaired chassis behaviour
            (heading focus on transition, inert + aria-hidden on the other stages, native
            dialogs with focus return). Two edits, both taking the REPAIRED exemplar
            SCI_G_W3_Friction.html as the source: (1) the keydown guard learns the two new
            overlays AND adopts the exemplar's heading exemption, so arrow navigation still
            works once showSlide has parked focus on a heading — the shipped guard bailed
            out on [tabindex] before reaching its own h1-h6 exemption, which killed the
            arrows after one press; the dialog/overlay clause is kept FIRST so it stays
            load-bearing rather than shadowed. (2) showSlide writes the #slide-N fragment
            only on a user-driven move, so the boot call no longer sets the sequential
            focus navigation starting point inside the deck and a.edu-skip is the first Tab
            stop, which is the only thing a skip link is for. An incoming #slide-N is still
            read and still honoured. (3) the stage timer learns the BUILD family's
            independent-stage rule: the donor returns before it reads a duration when the stage is
            the independent one (SCI_B_W3_Backbones.html line 496, keyed on its own literal title),
            and the design's area 0 names re-keying that test on data-type="independent" as one of
            the five wiring changes the shell needs. Sugar's engine keys only off data-timer, so the
            clause goes where the donor's is, in front of the duration read. The attribute itself is
            untouched: data-timer="10" stays on slide-8, the nine durations still sum to 40, and
            tools/science_teaching_packs/check_build_sugar_browser.cjs line 21 -- which reads
            dataset.timer, not the display -- is unaffected. No donor engine is imported.
  access    the four review-top controls move verbatim into nav.classic-toolbar and stay
            exactly four: the back link with its own relative href, Word help, Pause and
            Tools & print, each keeping its data-action so the engine's delegation is
            untouched. Nothing is stamped into the deck: a per-stage control row would put
            pupil-facing label text inside the deck root, which is what the reading-band
            instrument measures, and would resolve [data-action="tools"] to nine elements,
            which is what the accepted browser harness presses.
  xp        the meter is wired to the lesson's own checked interactions (Matt, 16 Sep):
            one point per sort card graded by [data-sort-check] (four [data-item] cards)
            and one for the evidence hinge ([data-check], graded by [data-check-choice]).
            gainXP fires on a correct grading, once per card and once per hinge, never
            twice. The total is measured here and again at run time; this tool refuses to
            build a meter that would read 0/0.
  complete  the completion overlay opens from the lesson's own exit reveal
            ([data-exit-reveal] reaching aria-expanded=true), with the dialog semantics,
            focus-in, Tab trap and focus return from author_w4l1.py's modal helpers;
            confetti is gated on prefers-reduced-motion; no audio is added.
  colour    nothing. html.pathway-build and its token block are already byte-identical to
            the BUILD donor; the build asserts they did not move and that no GROW value
            (#3F7D6E, #215E53, pathway-grow) entered the file.
  hud       <script defer src="/hud.js"></script> as the last body script -- the exact tag
            form carried by 72 lesson files in Science_Teesside, 16 of them in Build/. It is
            root-absolute on purpose: the dock is served at /hud.js on the Lessons origin and
            exists nowhere else, so opening any classroom lesson from file:// costs one
            console error, "file:///hud.js net::ERR_FILE_NOT_FOUND", and no page error.
            MEASURED, not assumed: the accepted donor SCI_B_W3_Backbones.html and
            SCI_B_W6_Balanced_Plate.html emit exactly that one error from file:// too, so this
            port is conformant with the live chassis rather than divergent from it. The estate
            has already ruled on it twice in committed code -- lesson_acceptance.py line 56
            loads each lesson in BOTH standalone (file://) and http modes and drops any console
            error whose text names hud.js, and this lesson's own accepted gate,
            check_build_sugar_browser.cjs, serves over http and counts pageerror only (89/89
            PASS on these bytes). Do NOT "fix" it into a protocol-guarded injector: see the
            assertion at the foot of build() for what that would silently break.

    python3 tools/build_resources/author_w8a_chassis.py [--root .] [--check]

--check re-derives the file from BASE and compares its SHA-256 with the file on disk.
"""
from pathlib import Path
import argparse, hashlib, html as htmlmod, re, subprocess, sys

BASE = '9f08cc72aadc12b2480ea8c1104e0118c7335ce087446308d39336c79379e96f'   # sha256 of the source bytes
BASE_BLOB = '1035792c9d9a95865d16b7e829d9704014a53e42'                        # the git blob carrying them
REL = 'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html'
esc = htmlmod.escape


def once(text, anchor, name):
    n = text.count(anchor)
    assert n == 1, '%s: anchor occurs %d times: %r' % (name, n, anchor[:80])


def replace_once(text, old, new, name):
    once(text, old, name)
    return text.replace(old, new)


def balanced(text, anchor, tag='div'):
    i = text.index(anchor)
    # an anchor that IS the opening tag starts the span itself; an attribute anchor sits inside it
    start = i if text.startswith('<' + tag, i) else text.rfind('<' + tag, 0, i)
    depth = 0; j = start
    while j < len(text):
        if text.startswith('<' + tag, j) and text[j + 1 + len(tag)] in ' >':
            depth += 1; j += 1
        elif text.startswith('</' + tag + '>', j):
            depth -= 1; j += len(tag) + 3
            if depth == 0:
                return start, j
        else:
            j += 1
    raise AssertionError(anchor)


def source(root):
    """The committed bytes at BASE, never the working copy. Refuses anything else."""
    try:
        raw = subprocess.check_output(['git', '-C', str(root), 'cat-file', 'blob', BASE_BLOB], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raw = (root / REL).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == BASE, 'input bytes are not the pinned source: sha256 %s, expected %s' % (digest, BASE)
    return raw.decode('utf-8')


def dom(text):
    from lxml import html
    return html.fromstring(text)


def text_of(node):
    return re.sub(r'\s+', ' ', ''.join(node.itertext())).strip()


def build(root):
    src = source(root)
    t = src
    doc = dom(src)

    # ------------------------------------------------- what the new chrome may say: the lesson's own words
    title = text_of(doc.xpath('//section[@id="slide-1"]//h1')[0])
    meta = text_of(doc.xpath('//section[@id="slide-1"]//p[@class="review-meta"]')[0])
    objective = text_of(doc.xpath('//section[@id="slide-1"]//div[@class="li-box"]/p')[0])
    criteria = [text_of(li) for li in doc.xpath('//section[@id="slide-1"]//div[@class="sc-box"]//li')]
    assert len(criteria) == 3, 'success criteria: %d' % len(criteria)
    assert objective.startswith('I can '), objective
    nojs_words = text_of(doc.xpath('//noscript/p')[0])

    # ------------------------------------------------- the XP sources, measured on the source DOM
    items = doc.xpath('//*[@data-sort]//*[@data-item]')
    hinges = doc.xpath('//*[@data-check]')
    assert len(items) == 4 and all(i.get('data-correct') for i in items), 'sort cards: %d' % len(items)
    assert len(hinges) == 1, 'evidence hinges: %d' % len(hinges)
    choices = hinges[0].xpath('.//*[@data-check-choice]')
    graded = [c for c in choices if re.match(r'Yes\b', c.get('data-feedback', ''))]
    assert len(choices) == 2 and len(graded) == 1 and all(c.get('data-feedback', '').startswith('Revisit') for c in choices if c not in graded), \
        'the hinge must grade exactly one choice Yes and the other Revisit'
    xp_total = len(items) + len(hinges)
    assert xp_total > 0, 'the meter would read 0/0'
    assert len(doc.xpath('//*[@data-sort-check]')) == 1, 'one sort check control'

    # ------------------------------------------------- body chrome: review shell out, classroom shell in
    DECK = '<main class="slide-container" id="lessonDeck" aria-label="Sugar evidence lesson">'
    old_open = t[t.index('<body data-pathway="BUILD"'):t.index(DECK) + len(DECK)]
    once(t, old_open, 'body open block')
    assert '<nav class="review-top"' in old_open and '<noscript>' in old_open and 'id="auto-timer"' in old_open and 'class="edu-skip"' in old_open, 'review chrome shape'
    timer = old_open[old_open.index('<div id="auto-timer"'):old_open.index('</div>', old_open.index('<div id="auto-timer"')) + 6]
    # the review shell's pill row, read out of the source: four controls, none of them composed here
    nav = old_open[old_open.index('<nav class="review-top"'):old_open.index('</nav>') + 6]
    home = re.search(r'<a href="([^"]+)" aria-label="([^"]+)">([^<]+)</a>', nav)
    assert home and home.group(1).startswith('../') and '\u2190 Lessons' in home.group(3), 'review back link: %r' % nav[:200]
    labels = re.findall(r'<button type="button" data-action="(\w+)">([^<]+)</button>', nav)
    assert labels == [('words', 'Word help'), ('pause', 'Pause'), ('tools', 'Tools &amp; print')], labels
    toolbar = ('<nav class="classic-toolbar" aria-label="Lesson tools">'
               '<a href="%s" aria-label="%s">%s</a>' % (home.group(1), home.group(2), home.group(3))
               + ''.join('<button type="button" class="ghost" data-action="%s">%s</button>' % pair for pair in labels)
               + '</nav>')
    xp = ('<div class="xp-wrap" id="xpWrap" role="status" aria-label="XP earned"><span class="xp-label">⭐ XP <span id="xpCount">0</span>/<span id="xpTotal">0</span></span>'
          '<div class="xp-track" aria-hidden="true"><div class="xp-fill" id="xpFill"></div></div></div>')
    noscript = ('<noscript><style>body{height:auto!important;overflow:auto!important}'
                '.slide-container{height:auto!important;min-height:0!important;display:block!important;padding:12px!important}'
                '.slide{display:block!important;height:auto!important;max-height:none!important;overflow:visible!important;margin:0 0 16px!important;animation:none!important}'
                '.controls,.progress-wrap,.progress-label,.classic-dialog,.chassis-chrome,#auto-timer,.xp-wrap,.classic-toolbar,.lesson-complete-overlay,.midpoint-overlay,.v4-modal-overlay,.confetti,.js-only,.slide button{display:none!important}'
                '[hidden],[data-arrival-panel][hidden],[data-help-panel][hidden],[data-task-panel][hidden],[data-exit-panel][hidden],[data-arrival-answer][hidden],[data-exit-answer][hidden]{display:block!important}'
                '#print-area{display:block}.print-section[data-print-route=staff]{display:none!important}'
                '.nojs-note{width:92%;margin:12px auto;padding:12px 16px;background:var(--task-bg);border:2px solid var(--task-border);border-radius:12px;font-size:1rem;line-height:1.4}'
                '@media print{.slide-container{display:none!important}.print-section[data-print-route=all],.print-section[data-print-route=standard]{display:block!important}}</style>'
                '<p class="nojs-note" role="note">' + esc(nojs_words) + '</p></noscript>')
    # ONE fixed container for the three chrome pieces, not three independently-positioned fixed boxes.
    # MEASURED reason, not a preference: .xp-wrap, #auto-timer and .classic-toolbar were each position:fixed
    # at a hand-computed px offset (top:8/54/58) while their heights grow with the text size, so at 200% text
    # the timer painted over the XP meter at every width tested -- 249x2px at 1280 and 768, 82x44px at 390,
    # 87x44px at 320, with the meter's "0/5" clipped mid-glyph -- the toolbar painted over the meter at 768
    # (33x48px), and at 390 the toolbar's wrapped second row painted over the deck (370x42px) because
    # .slide-container's padding-top was the literal 112px. Stacking more offsets cannot fix that class of
    # defect. Flex items cannot overlap each other, and flex-wrap gives a piece its own row when the row runs
    # out, so one set of rules is correct at every text size. The deck's clearance follows from the same
    # place: --chrome-h, the wrapper's measured height (see the CSS block and the ResizeObserver below).
    chrome = '<div class="chassis-chrome" id="chassisChrome">' + xp + timer + toolbar + '</div>'
    new_open = ('<body data-pathway="BUILD" data-lesson-id="W8A" data-lesson-mode="Explore"><a class="edu-skip" href="#slide-1">Skip to lesson</a>'
                + chrome + '\n' + noscript + DECK)
    t = t.replace(old_open, new_open)
    t = replace_once(t, 'class="slide science-slide" id="slide-1"', 'class="slide science-slide active" id="slide-1"', 'slide 1 active')

    # ------------------------------------------------- completion and midpoint overlays, after the progress label and status line
    summary = ''.join('<span><strong>✓</strong> %s</span>' % esc(c) for c in criteria)
    lc = ('<div class="lesson-complete-overlay" id="lc-overlay"><div class="lesson-complete-modal"><div class="lc-stars" aria-hidden="true"><span>🏅</span><span>📸</span><span>✍️</span></div>'
          '<h2>%s — banked!</h2><p>%s ✅</p><div class="lc-summary">%s</div><button type="button" data-action="lc-close">Onwards! 🚀</button></div></div>' % (esc(title), esc(meta), summary))
    mp = ('<div class="midpoint-overlay" id="mp-overlay"><div class="midpoint-modal"><span class="mp-tag">OPTIONAL EVIDENCE CHECK</span><h2>Check one piece of evidence</h2>'
          '<div class="mp-prompt">Show an adult or chosen partner, or quietly check your own work against today’s success: <strong>%s</strong> and <strong>%s</strong> Keep or correct one thing using the evidence.</div>'
          '<p class="mp-sub">If this optional panel is opened, resume when ready and allow for the pause in the teaching plan.</p>'
          '<button type="button" data-action="mp-resume">▶ Resume the task</button></div></div>' % (esc(criteria[0]), esc(criteria[1])))
    t = replace_once(t, '<p class="classic-status" id="classic-status" role="status"></p>',
                     '<p class="classic-status" id="classic-status" role="status"></p>' + lc + mp, 'overlays placement')

    # ------------------------------------------------- the review shell's stylesheet rules go with it
    t = replace_once(t, '.review-top{position:fixed;top:10px;right:14px;display:flex;gap:7px;z-index:2400}\n'
                        '.review-top a,.review-top button{display:inline-flex;align-items:center;min-height:44px;border-radius:10px;padding:9px 13px;font-size:1rem;text-decoration:none;background:#e2e8f0;color:#172033;border:0;font-weight:700}\n'
                        '.review-top a{background:#161d3d;color:#fff}\n', '', 'review-top rules')
    t = replace_once(t, '@media(max-width:700px){.review-top{top:62px;left:10px;right:10px;gap:5px;justify-content:flex-end}.review-top a,.review-top button{padding:9px 10px;font-size:.9rem}.sort-zones',
                     '@media(max-width:700px){.sort-zones', 'review-top 700px rules')
    t = replace_once(t, '@media print{.review-top{display:none!important}.print-section{break-after:page}',
                     '@media print{.print-section{break-after:page}', 'review-top print rule')
    # the body grid pinned the review shell's four in-flow children to four rows; the classroom shell is a
    # full-viewport flex deck with fixed chrome, so only the content-side declarations stay
    t = replace_once(t, '@media screen{body{height:100dvh;display:grid;grid-template-rows:auto minmax(0,1fr) auto auto;overflow:hidden}.review-top{position:static;grid-row:1;justify-content:flex-end;flex-wrap:wrap;padding:8px;gap:6px;padding-left:180px;min-height:62px}.slide-container{grid-row:2;width:100%;height:100%;min-height:0;padding:0 12px 8px;display:block}.slide{width:100%;height:100%;margin:0;padding:22px;border-radius:14px}.controls{position:static;grid-row:3;justify-content:flex-end;flex-wrap:wrap;padding:5px 10px;gap:6px;background:var(--bg)}.progress-label{position:static;grid-row:4;border-radius:0;padding:4px 12px;margin:0;max-width:100%;box-shadow:none;font-size:.85rem}.progress-wrap{height:4px}.classic-status{position:absolute}#auto-timer{top:8px;left:8px;right:auto}.review-top button,.review-top a,.controls button{font-size:1rem;line-height:1.25;padding:8px 12px}.print-section{display:none}.v4-modal{max-height:82dvh;overflow:auto}.slide p,.slide li{overflow-wrap:anywhere}}',
                     '@media screen{.print-section{display:none}.v4-modal{max-height:82dvh;overflow:auto}.slide p,.slide li{overflow-wrap:anywhere}}', 'review body grid')
    t = replace_once(t, '@media screen and (max-width:600px){.review-top{padding-top:62px;padding-left:8px;justify-content:flex-start;min-height:0}.slide-container{padding:0 6px 6px}.slide{padding:14px 11px;border-top-width:6px}',
                     '@media screen and (max-width:600px){.slide{padding:14px 11px;border-top-width:6px}', 'review-top 600px rules')
    t = replace_once(t, '.edu-skip,.review-top,.controls,.progress-label,.progress-wrap,.classic-dialog,.slide-container,#auto-timer{display:none!important}',
                     '.edu-skip,.controls,.progress-label,.progress-wrap,.classic-dialog,.slide-container,.chassis-chrome,#auto-timer,.xp-wrap,.classic-toolbar,.lesson-complete-overlay,.midpoint-overlay,.confetti{display:none!important}', 'print hide list')

    # ------------------------------------------------- engine repairs, both taken from SCI_G_W3_Friction.html
    # (1) the keydown guard. The shipped second line bails on any [tabindex], and showSlide parks focus on the
    #     stage heading with tabindex="-1" -- so the arrows died after one press and the guard's own h1-h6
    #     exemption on the next line was unreachable. The exemplar's form exempts a heading that IS the target.
    #     The dialog/overlay clause stays FIRST: put it after, as the exemplar does, and a heading focused inside
    #     an open dialog would let the arrows through.
    t = replace_once(t,
        "    if(document.querySelector('.classic-dialog[open]')||event.altKey||event.ctrlKey||event.metaKey)return;\n"
        "    if(event.target.closest('button,input,textarea,select,a,summary,details,video,audio,[contenteditable=\"true\"],[role=\"button\"],[role=\"slider\"],[tabindex]'))return;\n"
        "    if(event.target!==document.body&&event.target.closest('.slide')&&event.target.matches(':focus')&&!event.target.matches('h1,h2,h3,h4,h5,h6'))return;\n",
        "    if(document.querySelector('.classic-dialog[open]')||document.querySelector('.lesson-complete-overlay.visible')||document.querySelector('.midpoint-overlay.visible')||event.altKey||event.ctrlKey||event.metaKey)return;\n"
        "    if(event.defaultPrevented||!(event.target instanceof Element))return;\n"
        "    const heading=event.target.matches('h1,h2,h3,h4,h5,h6');\n"
        "    const control=event.target.closest('button,input,textarea,select,a,summary,details,video,audio,[contenteditable=\"true\"],[role=\"button\"],[role=\"slider\"],[tabindex]');\n"
        "    if(control&&!(control===event.target&&heading))return;\n"
        "    if(event.target!==document.body&&event.target.closest('.slide')&&event.target.matches(':focus')&&!heading)return;\n", 'keydown guard')
    # (2) the boot call is showSlide(n,false); writing the fragment there set Chromium's sequential focus
    #     navigation starting point inside the deck, so Tab began after a.edu-skip and the skip link was
    #     reachable only by tabbing through the whole of stage 1. The exemplar writes no fragment at all; here
    #     the fragment is kept for user-driven moves (deep links and the incoming #slide-N still work) and
    #     dropped from the boot call only.
    t = replace_once(t, "if(location.hash!=='#slide-'+(index+1))history.replaceState(null,'','#slide-'+(index+1));",
                     "if(moveFocus&&location.hash!=='#slide-'+(index+1))history.replaceState(null,'','#slide-'+(index+1));", 'boot fragment')
    # (3) the independent stage. Every BUILD lesson already on this chassis suppresses the countdown on
    #     its independent stage -- the donor's _atOnSlideChange returns before it reads data-timer when the
    #     stage is that one -- and the design's area 0 lists re-keying that test on data-type="independent"
    #     (which slide-8 already carries) as one of the five wiring changes this port owes the shell. The
    #     clause goes in seconds(), the one place timerLeft(), updateTimerDisplay() and autoTimerReset()
    #     all read a duration through, so the display sits at 00:00 and startTimer() bails on its own
    #     timerLeft()<=0 guard: no new state and no second code path. The ATTRIBUTE is not touched --
    #     data-timer="10" stays on the section, the nine durations still sum to 40, and both are asserted.
    t = replace_once(t, "  function seconds(slide) { return Math.round(number(slide.dataset.timer) * 60); }\n",
                     "  function seconds(slide) { if (slide && slide.dataset.type === 'independent') return 0; return Math.round(number(slide.dataset.timer) * 60); }\n",
                     'independent stage timer')

    # ------------------------------------------------- chassis furniture CSS: tokens only, no new hex
    css = ('<style id="build-w8a-chassis-css">'
           '/* D-1: classroom chassis furniture for this lesson (tools/build_resources/author_w8a_chassis.py). Colour comes from the html.pathway-build tokens already in this file; no hex is written here. */'
           # THE CHROME IS ONE FLEX ROW. The three pieces stop being positioned and become flex items, so the
           # browser lays them out and they cannot overlap; when the row runs out of width a piece takes the
           # next row instead of being painted on top of its neighbour. Nothing here positions a piece by hand.
           '.chassis-chrome{position:fixed;top:0;left:0;right:0;z-index:6001;display:flex;flex-wrap:wrap;align-items:flex-start;gap:6px;padding:8px 14px;pointer-events:none}'
           # the strip spans the viewport, so only the pieces themselves may take a click; the rest passes through
           '.chassis-chrome>*{pointer-events:auto}'
           '.chassis-chrome .xp-wrap,.chassis-chrome #auto-timer,.chassis-chrome .classic-toolbar{position:static;top:auto;right:auto;bottom:auto;left:auto;margin:0;max-width:100%}'
           '.chassis-chrome .xp-wrap{min-height:40px}'
           '.chassis-chrome .classic-toolbar{margin-left:auto;flex-wrap:wrap;justify-content:flex-end}'
           # AND THE DECK'S CLEARANCE IS THE CHROME'S MEASURED HEIGHT, not a literal: --chrome-h is set from
           # the wrapper's own bounding box by the ResizeObserver in script#build-w8a-chassis, so it is right
           # at 100%, at 200% and at any size in between, including sizes nobody thought to test. The fallback
           # in each band is the TALLEST height that band measures at 100% text -- swept at 21 widths from
           # 280px to 1920px, because the toolbar's wrap count changes inside a band (default is 64px at
           # 900-1920 but 114px at 701-768; <=379 is 113px at 340-379 but 206px at 280-300). Taking the
           # tallest means the frames before the script runs, and the path where ResizeObserver does not
           # exist at all, can over-clear but can never put the deck under the chrome.
           '.slide-container{padding-top:calc(var(--chrome-h,114px) + 8px)}'
           '@media screen and (max-width:700px){.chassis-chrome{padding:8px 10px;gap:5px}.xp-wrap{font-size:.8rem;padding:5px 10px;gap:7px}.xp-track{width:56px}'
           '.slide-container{padding-top:calc(var(--chrome-h,113px) + 8px)}}'
           # narrow phones: the timer cannot shrink below its two 44px controls, so the meter drops its
           # decorative (aria-hidden) bar and keeps its text, and the toolbar takes two rows of its own
           '@media screen and (max-width:379px){.xp-track{display:none}.xp-wrap{gap:0;padding:5px 9px}'
           '.slide-container{padding-top:calc(var(--chrome-h,206px) + 8px)}}'
           # THE HUD OWNS THE BOTTOM STRIP, and this lesson's own bottom furniture has to sit above it.
           # <script defer src="/hud.js"> is part of this chassis (see the `hud` note at the top) and injects
           # #mbmhud-pill at position:fixed;bottom:10px with z-index 2147483000 -- a stacking level this lesson
           # cannot outrank and must not try to. MEASURED on the PACKAGED lesson at the offline gate's own phone
           # viewport, 390x844 reduced motion: the pill is (146,790) 98x44 and the TA Brief button (103,786)
           # 91x44, overlapping 48x40, and document.elementFromPoint at the button's centre returns the pill --
           # so the gate's real pointer click never reached the button and "Extracted lesson packs work offline"
           # went red at 11/12 with build-science-aut1-main failing on locator('button[data-action="ta"]').
           # The same collision is present at 768x800 (.controls x 311-750 against the pill at x 335-433); 1280
           # escapes it only because the two happen to be horizontally disjoint there, which is luck rather than
           # design, so the reservation is unconditional. Pre-port this lesson carried no HUD, so the pill did
           # not exist and the click landed: this is the port's to fix.
           # --hud-safe is the space the pill claims measured from the pill itself, published by the observer
           # below; 54px is that measurement at 320, 390, 768 and 1280 alike (bottom:10px + a 44px target) and
           # is the fallback for the frames before the pill arrives and for a browser without the observers.
           # The pill itself is not moved, resized or restyled -- it belongs to the HUD, and other lessons in
           # the estate depend on where it sits.
           '.controls{bottom:calc(18px + var(--hud-safe,54px))}'
           '@media (max-width:640px){.controls{bottom:calc(14px + var(--hud-safe,54px))}}'
           '.progress-label{bottom:calc(62px + var(--hud-safe,54px))}'
           '/* a skip link is a control: the authored padding left it 42px tall, two short of the target size the rest of this page meets */'
           '.edu-skip{display:inline-flex;align-items:center;min-height:44px;box-sizing:border-box}'
           # the label-detective tokens are pressable controls: "14" and "g" fell short of 44px on a phone.
           # min-width/min-height only, so the authored padding, borders and colours are untouched (the unit
           # token's border-radius:50% becomes a true circle rather than a narrow ellipse).
           '.detective-label button{min-width:44px;min-height:44px}'
           # the exit stage's next-lesson link is the last control of the lesson and was 17px tall. It is
           # the only link in its own <p>, so giving it the .edu-skip treatment changes no word, no colour
           # and no other line -- the alternative on offer was re-authoring accepted pupil text, which D-1
           # forbids. Width is unchanged (it was already 178px) and the box still shrinks to fit, so the
           # label wraps on a narrow phone rather than pushing the stage sideways.
           '.sugar-next a{display:inline-flex;align-items:center;min-height:44px;box-sizing:border-box}'
           '.lesson-complete-modal,.midpoint-modal{max-height:88vh;overflow:auto}'
           # CONTRAST, MEASURED WITH axe-core ON THE BUILT PAGE, NOT EYEBALLED. The base file has carried
           # .midpoint-modal / .lesson-complete-modal CSS since before this port, but the accepted bytes
           # held no #mp-overlay and no #lc-overlay, so those rules never painted -- measured: both element
           # queries return false on the BASE file and true here. THIS PORT is what puts them on a pupil
           # screen, and three of their pairs land below WCAG AA once they do:
           #   .mp-tag              #fff on var(--scaffold-border) #38bdf8  2.14:1   bold 12.5px
           #   .midpoint-modal button        same pair                      2.14:1   bold 16.8px
           #   .lesson-complete-modal button #fff on var(--ido-border) #c9803b 3.17:1 bold 16px
           # None of those is large text (AA large starts at 18.66px bold), so 4.5:1 applies to all three
           # and axe-core scores every one of them a SERIOUS violation -- the same impact class the estate's
           # acceptance instrument fails a stage on. It never saw them because nothing in a stage opens an
           # overlay. Tokens only, no new hex, and the ink the base rules set (#fff) is left alone:
           #   the chip keeps the scaffold blue and takes the page's own ink  #1f2937 on #38bdf8  6.85:1
           #   both buttons take the page's standard button background        #fff on #4e7a9b     4.58:1
           # The hover pair moves with them for the same reason: the base hover literal under .midpoint-modal
           # is #0284c7, which is 4.10:1 against the white the base rule sets, so repairing only the resting
           # state would have left the failure on :hover. var(--btn-hover) is 4.86:1. The lesson's global
           # button rule is already background:var(--btn-bg);color:#fff with :hover background:var(--btn-hover),
           # so this returns the two overlay calls-to-action to the pair every other button here uses rather
           # than inventing a colour for them. Specificity is matched, not raised; this block sits before
           # </head> and therefore after the base rules, so equal weight wins on order.
           '.midpoint-modal .mp-tag{color:var(--text)}'
           '.midpoint-modal button,.lesson-complete-modal button{background:var(--btn-bg)}'
           '.midpoint-modal button:hover,.lesson-complete-modal button:hover{background:var(--btn-hover)}'
           '</style>')
    t = replace_once(t, '</head>', css + '</head>', 'css placement')

    # ------------------------------------------------- the chrome's behaviour, after every lesson script, then the HUD
    script = r"""<script id="build-w8a-chassis">
/* D-1: the classroom chrome (XP meter, completion overlay, optional midpoint panel) wired to this lesson's own checked
   interactions. Runs after the engine and the interaction scripts; nothing here is wrapped in a bare catch. */
(function(){
 'use strict';
 const byId=id=>document.getElementById(id);
 const reduced=()=>Boolean(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches);
 /* THE DECK'S TOP CLEARANCE. --chrome-h is the chrome strip's own measured height, so the deck cannot sit
    under the chrome at any text size, and no offset in the stylesheet has to be kept in step with a font.
    Deliberately not wrapped in a catch: the element is asserted to exist at build time, and if this ever
    throws it must be a visible error rather than a deck that silently slides under the toolbar. Where
    ResizeObserver is absent the per-band CSS fallback stands, which is the reason that fallback exists. */
 const chromeBar=byId('chassisChrome');
 const sizeChrome=()=>document.documentElement.style.setProperty('--chrome-h',Math.ceil(chromeBar.getBoundingClientRect().height)+'px');
 sizeChrome();
 if(window.ResizeObserver)new ResizeObserver(sizeChrome).observe(chromeBar);
 window.addEventListener('resize',sizeChrome);
 /* this lesson embeds two font faces; a swap after the first measure changes the strip's height, and
    the observer is what catches a text-size change, so both re-measure rather than trusting one shot. */
 if(document.fonts&&document.fonts.ready)document.fonts.ready.then(sizeChrome);
 /* THE HUD'S BOTTOM STRIP, the same shape as --chrome-h at the top. hud.js is deferred, so #mbmhud-pill does
    not exist yet when this runs: its ARRIVAL is watched as well as its size. --hud-safe is the space the pill
    claims from the bottom of the viewport, taken from the pill's own box. While it cannot be measured the
    property is left unset so the measured CSS fallback governs -- reserve unless we know better, which is the
    fail-safe direction: a missing measurement over-reserves, it never lets the pill cover a control. The
    lower-half test keeps a HUD that ever docks elsewhere from being read as a bottom claim. Not wrapped in a
    catch, and it never writes to the pill. */
 const hudSafe=()=>{
  const pill=byId('mbmhud-pill');const box=pill&&pill.getBoundingClientRect();
  if(box&&box.height>0&&box.bottom>window.innerHeight/2)document.documentElement.style.setProperty('--hud-safe',Math.ceil(window.innerHeight-box.top)+'px');
  else document.documentElement.style.removeProperty('--hud-safe');
  return pill;};
 let hudSized=null;
 const watchHud=()=>{const pill=hudSafe();
  if(pill&&window.ResizeObserver&&!hudSized){hudSized=new ResizeObserver(hudSafe);hudSized.observe(pill);}
  return pill;};
 watchHud();
 window.addEventListener('resize',watchHud);
 if(!byId('mbmhud-pill')&&window.MutationObserver){
  const hudArrival=new MutationObserver(()=>{if(watchHud())hudArrival.disconnect();});
  hudArrival.observe(document.documentElement,{childList:true,subtree:true});}
 /* XP: one point per graded item. The label sort grades four cards ([data-item]) when [data-sort-check] is pressed;
    the evidence hinge ([data-check]) grades one choice ([data-check-choice]). Each is credited once. */
 let xpCount=0,xpTotal=0;const earned=new Set();
 function registerXP(n){xpTotal+=(n||1);byId('xpTotal').textContent=xpTotal;}
 function gainXP(){if(xpCount>=xpTotal&&xpTotal>0)return;xpCount++;byId('xpCount').textContent=xpCount;byId('xpFill').style.width=((xpCount/xpTotal)*100)+'%';if(xpCount===xpTotal)fireConfetti();}
 function fireConfetti(){if(reduced())return;const cols=['#9c27b0','#eab308','#22c55e','#38bdf8','#f97316','#dc2626','#7c3aed','#db2777'];for(let i=0;i<50;i++){const c=document.createElement('div');c.className='confetti';c.setAttribute('aria-hidden','true');c.style.left=Math.random()*100+'vw';c.style.background=cols[i%cols.length];c.style.borderRadius=Math.random()>.5?'50%':'0';c.style.animation='confettiFall '+(2+Math.random()*1.5)+'s linear '+(Math.random()*.3)+'s forwards';document.body.appendChild(c);setTimeout(()=>c.remove(),4000);}}
 registerXP(document.querySelectorAll('[data-sort] [data-item]').length);
 registerXP(document.querySelectorAll('[data-check]').length);
 document.addEventListener('rich-sort-check',()=>{document.querySelectorAll('[data-sort] [data-item][data-result="correct"]').forEach(item=>{const key='item:'+item.dataset.item;if(earned.has(key))return;earned.add(key);gainXP();});});
 document.addEventListener('click',event=>{
  const choice=event.target.closest('[data-check-choice]');
  if(!choice||!/^Yes\b/.test(choice.dataset.feedback||''))return;
  const root=choice.closest('[data-check]');const key='check:'+(root&&root.id||'hinge');
  if(earned.has(key))return;earned.add(key);gainXP();
 });
 /* overlay dialogs: semantics, focus in, Tab trap, focus back (tools/launch_resources/author_w4l1.py) */
 function _mbmModalOpened(m,opener){m._mbmOpener=opener;const box=m.querySelector('.v4-modal,.lesson-complete-modal,.midpoint-modal');if(!box)return;box.setAttribute('role','dialog');box.setAttribute('aria-modal','true');
  const h=box.querySelector('h2,h3');if(h&&!h.id){h.id=m.id+'-title';}if(h)box.setAttribute('aria-labelledby',h.id);
  const focusables=()=>[...box.querySelectorAll('button,[href],input,select,textarea,[tabindex]:not([tabindex="-1"])')].filter(el=>!el.disabled);
  const first=focusables()[0];if(first)first.focus({preventScroll:true});
  if(!m._mbmTrap){m._mbmTrap=true;m.addEventListener('keydown',ev=>{if(ev.key!=='Tab')return;const f=focusables();if(!f.length)return;const a=f[0],z=f[f.length-1];if(ev.shiftKey&&document.activeElement===a){ev.preventDefault();z.focus();}else if(!ev.shiftKey&&document.activeElement===z){ev.preventDefault();a.focus();}});}}
 function _mbmModalClose(id){const m=byId(id);if(!m)return;const was=m.classList.contains('visible');m.classList.remove('visible');const o=m._mbmOpener;if(was&&o&&o.isConnected)o.focus({preventScroll:true});}
 /* completion: the lesson's own exit reveal ([data-exit-reveal] reaching aria-expanded=true), once */
 let lcShown=false;
 function showLessonComplete(opener){if(lcShown)return;lcShown=true;const ov=byId('lc-overlay');setTimeout(()=>{fireConfetti();ov.classList.add('visible');_mbmModalOpened(ov,opener);},reduced()?0:400);}
 function hideLessonComplete(){_mbmModalClose('lc-overlay');}
 document.addEventListener('click',event=>{const reveal=event.target.closest('[data-exit-reveal]');if(reveal&&reveal.getAttribute('aria-expanded')==='true')showLessonComplete(reveal);});
 /* midpoint: an optional teacher panel, opened only by name (as on the donor); pauses the stage timer and resumes it if it was running */
 let mpWasRunning=false;
 function fireMidpoint(opener){const ov=byId('mp-overlay');const toggle=byId('auto-timer-toggle');mpWasRunning=Boolean(toggle&&toggle.getAttribute('aria-label')==='Pause stage timer');if(typeof window.pauseTimer==='function')window.pauseTimer();ov.classList.add('visible');_mbmModalOpened(ov,opener||document.activeElement);}
 function resumeFromMidpoint(){_mbmModalClose('mp-overlay');if(mpWasRunning&&typeof window.startTimer==='function')window.startTimer();mpWasRunning=false;}
 document.addEventListener('click',event=>{
  if(event.target.closest('[data-action="lc-close"]'))hideLessonComplete();
  if(event.target.closest('[data-action="mp-resume"]'))resumeFromMidpoint();
  if(event.target===byId('lc-overlay'))hideLessonComplete();
 });
 document.addEventListener('keydown',event=>{if(event.key==='Escape'){['lc-overlay','mp-overlay'].forEach(_mbmModalClose);}});
 Object.assign(window,{registerXP,gainXP,fireMidpoint,resumeFromMidpoint,hideLessonComplete,showLessonComplete,mbmXP:()=>({count:xpCount,total:xpTotal})});
}());
</script>
<script defer src="/hud.js"></script></body></html>"""
    t = replace_once(t, '</script></body></html>', '</script>\n' + script, 'chrome script placement')

    # ------------------------------------------------- what must hold on the way out
    out = dom(t)
    body_children = [c.tag + ('#' + c.get('id') if c.get('id') else '') for c in out.xpath('//body/*') if c.tag not in ('script', 'noscript')]
    expected = ['a', 'div#chassisChrome', 'main#lessonDeck', 'div', 'div#classic-progress', 'div#progressLabel', 'p#classic-status', 'div#lc-overlay', 'div#mp-overlay',
                'dialog#pause-dialog', 'dialog#cold-call-dialog', 'dialog#tools-dialog', 'dialog#organiser-dialog', 'dialog#word-dialog', 'dialog#ta-dialog', 'div#print-area']
    assert body_children == expected, body_children
    assert out.xpath('//body/noscript'), 'noscript present'
    # the review shell's pill row is gone; its four controls are in the chassis toolbar, once each
    assert 'review-top' not in t and not out.xpath('//*[contains(@class,"review-top")]'), 'review chrome remains'
    # THE CHROME STRIP: one wrapper, the three pieces inside it in order, laid out by flex, and a deck
    # clearance that is measured rather than typed. Pinned so a later round cannot quietly return to three
    # fixed boxes with px offsets -- the shape that put the timer over the XP meter at 200% text.
    strip = out.xpath('//div[@id="chassisChrome" and @class="chassis-chrome"]')
    assert len(strip) == 1 and [c.tag + ('#' + c.get('id') if c.get('id') else '') for c in strip[0]] == \
        ['div#xpWrap', 'div#auto-timer', 'nav'], 'the chrome strip holds the meter, the timer and the toolbar, in that order'
    assert t.count('.chassis-chrome{position:fixed;top:0;left:0;right:0;z-index:6001;display:flex;flex-wrap:wrap;') == 1, \
        'the strip is one fixed flex row that wraps'
    assert not re.search(r'\.(?:xp-wrap|classic-toolbar)\{[^}]*position:fixed', t.split('build-w8a-chassis-css')[1]), \
        'no chrome piece may be positioned by hand again'
    for fallback in (114, 113, 206):
        assert t.count('padding-top:calc(var(--chrome-h,%dpx) + 8px)' % fallback) == 1, \
            'each band needs its measured tallest-at-100%% fallback, missing %dpx' % fallback
    assert t.count("setProperty('--chrome-h',Math.ceil(chromeBar.getBoundingClientRect().height)+'px')") == 1 and \
        t.count('new ResizeObserver(sizeChrome).observe(chromeBar)') == 1 and t.count('sizeChrome();') == 1 and \
        t.count('document.fonts.ready.then(sizeChrome)') == 1, \
        'the deck clearance is measured, once, and re-measured on resize, on strip resize and after font swap'
    assert '.classic-dialog,.chassis-chrome,#auto-timer' in t and '.slide-container,.chassis-chrome,#auto-timer' in t, \
        'the no-JS and print paths hide the strip itself, not only its three children'
    # THE HUD STRIP AT THE BOTTOM. Pinned for the same reason as the top: the offline pack gate clicks
    # button[data-action="ta"] with a real pointer at 390x844, and without this reservation the pill covers it.
    for rule in ('.controls{bottom:calc(18px + var(--hud-safe,54px))}',
                 '@media (max-width:640px){.controls{bottom:calc(14px + var(--hud-safe,54px))}}',
                 '.progress-label{bottom:calc(62px + var(--hud-safe,54px))}'):
        assert t.count(rule) == 1, 'the bottom furniture must clear the HUD strip in every band: ' + rule
    assert t.count("setProperty('--hud-safe',Math.ceil(window.innerHeight-box.top)+'px')") == 1 and \
        t.count("removeProperty('--hud-safe')") == 1 and t.count('new ResizeObserver(hudSafe)') == 1 and \
        t.count('hudArrival.observe(document.documentElement') == 1 and t.count('watchHud();') == 1, \
        'the HUD strip is measured on arrival and on resize, and falls back when it cannot be measured'
    chassis_css = t[t.index('<style id="build-w8a-chassis-css">'):]
    chassis_css = chassis_css[:chassis_css.index('</style>')]
    assert 'mbmhud' not in chassis_css, 'this lesson must not restyle the HUD pill: it belongs to the HUD'
    bar = out.xpath('//nav[@class="classic-toolbar"]')
    assert len(bar) == 1 and bar[0].get('aria-label') == 'Lesson tools', 'one named toolbar'
    assert [(c.tag, c.get('data-action'), text_of(c)) for c in bar[0]] == \
        [('a', None, home.group(3)), ('button', 'words', 'Word help'), ('button', 'pause', 'Pause'), ('button', 'tools', 'Tools & print')], \
        [(c.tag, c.get('data-action'), text_of(c)) for c in bar[0]]
    assert bar[0][0].get('href') == htmlmod.unescape(home.group(1)) and not re.search(r'https?://', bar[0][0].get('href')), 'the back link keeps its own relative href'
    for action in ('words', 'pause', 'tools', 'organiser', 'ta', 'cold-call'):
        assert len(out.xpath('//*[@data-action="%s"]' % action)) == 1, 'data-action %s is not singular' % action
    assert not out.xpath('//*[contains(@class,"build-ko-access")]') and 'build-ko-access' not in t, 'no control text was stamped into the deck'
    stages = out.xpath('//main[@id="lessonDeck"]/section[contains(concat(" ",@class," ")," slide ")]')
    assert len(stages) == 9 and [s.get('id') for s in stages] == ['slide-%d' % i for i in range(1, 10)], 'nine stages'
    for attr in ('data-title', 'data-timer', 'data-type', 'data-teacher', 'data-prompt'):
        assert [s.get(attr) for s in stages] == [s.get(attr) for s in doc.xpath('//main//section')], attr + ' moved'
    assert sum(int(s.get('data-timer')) for s in stages) == 40
    # THE HUD TAG: the estate's standard form, exactly once, and last in the body. A root-absolute
    # src cannot resolve from file://, and that trade-off is recorded here rather than engineered
    # away, because the two committed instruments that judge this lesson already rule on it (see the
    # `hud` paragraph above) and because rewriting it into a protocol-guarded script injector would
    # break a third: tools/downloads/build_download_pack.py finds the HUD only through this static
    # tag or the reviewed id="grow-hud-loader" helper, so a new third shape would be invisible to it
    # and hud.js would drop out of the offline pack with no gate going red.
    assert t.count('<script defer src="/hud.js"></script>') == 1 and \
        t.rstrip('\n').endswith('<script defer src="/hud.js"></script></body></html>'), 'the standard HUD tag, once, last'
    # THREE PRE-EXISTING DEVIATIONS ARE CARRIED, NOT FIXED. The design's area 1 G is explicit --
    # "leave the nine identical data-prompt strings identical ... Record all four as Matt-list items;
    # fixing any of them inside a shell-change commit would make the port unprovable" -- and
    # LESSON_STANDARD_2026-27.md line 199 makes Sugar report-only: "measure, record, Matt list. No
    # re-open." Each is asserted as CARRIED so a later round cannot quietly author over it:
    #  (1) Part C line 350 wants nine distinct data-prompt values; the accepted lesson has nine
    #      copies of one string, in BASE and here alike -- a zero-delta inherited failure.
    #  (2) slide-6's data-teacher reads "gper 100 g", one missing space, authored.
    #  (3) g26_reading_band.py reads pupil FK 5.26 against the BUILD band 1.0-4.0. This tool cannot
    #      move it and must not: the deck is asserted byte-identical to BASE below, which is why the
    #      instrument's extracted pupil text, and therefore every FK figure, is identical by
    #      construction rather than by rounding.
    # What the standard DOES require per stage and this lesson does meet is nine distinct TA briefs.
    prompts = [s.get('data-prompt') for s in stages]
    assert len(prompts) == 9 and len(set(prompts)) == 1 and \
        prompts == [s.get('data-prompt') for s in doc.xpath('//main//section')], \
        'the nine authored data-prompt strings are carried unchanged, including their inherited sameness'
    assert len({s.get('data-teacher') for s in stages}) == 9, 'nine distinct per-stage TA briefs'
    assert t.count('gper 100 g') == src.count('gper 100 g') == 1, 'the authored slide-6 typo is carried unchanged'
    # no pupil word moved: apart from slide 1 gaining .active, the deck is byte-identical to the source
    src_deck = src[src.index('<section class="slide science-slide" id="slide-1"'):src.index('</main>')]
    out_deck = t[t.index('<section class="slide science-slide active" id="slide-1"'):t.index('</main><div class="controls">')]
    assert out_deck.replace('class="slide science-slide active" id="slide-1"', 'class="slide science-slide" id="slide-1"') == src_deck, 'stage content moved'
    for sel in ('//*[@id="xpWrap"]', '//*[@id="lc-overlay"]', '//*[@id="mp-overlay"]', '//*[@id="xpCount"]', '//*[@id="xpTotal"]', '//*[@id="xpFill"]',
                '//button[@data-action="ta"]', '//dialog[@id="ta-dialog"]//button[@data-action="close"]', '//button[@id="next-slide" and @data-action="next"]',
                '//button[@id="previous-slide" and @data-action="previous"]', '//nav[@class="classic-toolbar"]/button[@data-action="pause"]', '//a[@class="edu-skip"]',
                '//div[@id="classic-progress" and @role="progressbar"]', '//p[@id="classic-status" and @role="status"]',
                '//main[@id="lessonDeck" and contains(@class,"slide-container")]', '//main[@id="lessonDeck"]//*[@class="sugar-lundy" or @id="sugar-lundy"]'):
        assert len(out.xpath(sel)) == 1, sel
    # the two engine repairs, asserted on the built bytes rather than assumed from the patch
    assert "if(control&&!(control===event.target&&heading))return;" in t and "[tabindex]'))return;" not in t, 'keydown guard repair'
    assert t.count("if(moveFocus&&location.hash!==") == 1 and "if(location.hash!=='#slide-'" not in t, 'boot fragment repair'
    assert t.count("if (slide && slide.dataset.type === 'independent') return 0;") == 1 and \
        "function seconds(slide) { return Math.round" not in t, 'independent stage timer repair'
    indep = [s for s in stages if s.get('data-type') == 'independent']
    assert [s.get('id') for s in indep] == ['slide-8'] and indep[0].get('data-timer') == '10', \
        'the independent stage kept its id and its authored duration: %r' % [(s.get('id'), s.get('data-timer')) for s in indep]
    # the three overlay contrast repairs, pinned on the built bytes: the port paints these surfaces, so
    # a later round must not drop the rules that keep them at WCAG AA (see the note in the CSS block).
    for rule in ('.midpoint-modal .mp-tag{color:var(--text)}',
                 '.midpoint-modal button,.lesson-complete-modal button{background:var(--btn-bg)}',
                 '.midpoint-modal button:hover,.lesson-complete-modal button:hover{background:var(--btn-hover)}'):
        assert t.count(rule) == 1, 'overlay contrast rule missing or duplicated: ' + rule
    assert t.index('.midpoint-modal .mp-tag{color:var(--text)}') > t.index('.midpoint-modal .mp-tag{display:inline-block'), \
        'the contrast override must follow the base rule it overrides'
    nxt = out.xpath('//p[@class="sugar-next"]/a')
    assert len(nxt) == 1 and nxt[0].get('href') == 'SCI_B_W8B_Autumn_Science_Checkpoint_Do.html' and \
        t.count('.sugar-next a{display:inline-flex') == 1, 'one next-lesson link, given a target size'
    ids = out.xpath('//*[@id]/@id'); assert len(ids) == len(set(ids)), 'duplicate ids'
    # content that must not move: the print pack, the six dialogs, the organiser, the video, the pathway tokens
    for a, b in (('<dialog id="pause-dialog"', '<div id="print-area">'), ('<div id="print-area">', '</div><script>window.CLASSIC_LESSON')):
        assert src[src.index(a):src.index(b)] == t[t.index(a):t.index(b)], a + ' moved'
    token_block = src[src.index('html.pathway-build{'):src.index('}', src.index('html.pathway-build{')) + 1]
    assert t.count(token_block) == src.count(token_block) == 1 and '<html lang="en-GB" class="pathway-build">' in t, 'pathway tokens moved'
    assert not re.search(r'3F7D6E|215E53|pathway-grow|pathway-launch', t, re.I), 'GROW or LAUNCH colour entered the file'
    assert t.count('data:video/mp4;base64') == 1 and t.count('data:font/ttf;base64') == 2, 'media moved'
    words = text_of(out.xpath('//body')[0])
    assert words.index('I can ') == words.index(objective), 'the first "I can" sentence is no longer the objective'
    assert '40 minutes' in words or '40-minute' in words, 'duration text'
    assert 'Autumn 1 · Sugar evidence: compare label values on the same basis.' in t, 'catalogue proof quote'
    return t, xp_total


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', type=Path, default=Path('.'))
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    root = args.root.resolve(); out = root / REL
    text, xp_total = build(root)
    data = text.encode('utf-8')
    digest = hashlib.sha256(data).hexdigest()
    if args.check:
        current = hashlib.sha256(out.read_bytes()).hexdigest()
        print('candidate', digest, 'on disk', current, 'MATCH' if digest == current else 'DIFFERS')
        raise SystemExit(0 if digest == current else 1)
    out.write_bytes(data)
    print('written', REL, len(data), 'bytes', digest, 'xp total', xp_total)
