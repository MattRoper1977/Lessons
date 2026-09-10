#!/usr/bin/env python3
"""tools/gc1/repair_weeks.py - GC1 P2: the four audited defects in the GROW
Computing unit, repaired in place.

THE FOUR

d1  THE PRINT ROUTE IS DEAD IN SIX OF EIGHT LESSONS. Every lesson ships print CSS
    that hides header, main and footer and shows `.print-record`. Weeks 1 and 2
    ship that container EMPTY and never fill it. Weeks 3 to 6 dropped the element
    entirely. So six lessons have printed a blank sheet of paper for as long as
    they have existed, and nothing errored, because a blank page is what the CSS
    asks for when the container is empty.

    Weeks 7 and 8 have the working form: a filler that writes the pupil's record
    into the container, wired to `beforeprint` and to a Print button. That is
    copied back -- adapted, not pasted, because weeks 1 and 2 name their lesson
    data `DATA` while weeks 3 to 8 name it `W`. A blind paste would have thrown on
    two of the six.

    The filler selects `.print-record`, never an id. Weeks 1-2 already have that
    container empty, weeks 7-8 already have it working, and only weeks 3-6 gain
    one. So no existing element is mutated and there is no id to hand back on
    strip -- an earlier draft added `id="printRecord"` to the weeks 1-2 container
    and its strip then removed that id from weeks 7-8 too, which ship it
    themselves. Selecting on the class the CSS already uses avoids the whole
    question.

    This repair is load-bearing beyond tidiness: P2P's paper route is delivered
    through this same container, so a teacher with no printer-side download can
    produce the week's paper route from the lesson page. A print route that
    prints nothing cannot carry a completion route.

d2  DUPLICATE id="centre" IN WEEKS 1 AND 2. Measured before repair: the two
    occurrences are the two arms of ONE ternary, so at most one is ever in the
    document and the rendered DOM has no collision. The defect is real but it is
    a SOURCE defect, not a runtime one -- worth saying plainly, because a report
    that called it a live duplicate would be overclaiming. It still goes: a single
    `$('#centre')` binding over two elements that are only accidentally exclusive
    is one template edit away from breaking, and a static id census flags it
    forever. The two arms get distinct ids and both are bound.

d3  THE HUBS DO NOT CROSS-LINK. Three Start_Here hubs, zero links between them,
    and the Weeks 1-2 and Weeks 3-6 hubs do not mention Weeks 7-8 at all -- so a
    teacher who opens the unit at Week 1 has no route to the second half of it.

d4  ESTATE FURNITURE. Measured across the eight lessons: no way home, no Made by
    Matt mark, no guidance toggle. Prev/next is already there (`#prev`/`#next` in
    every one of the eight), so it is counted, not added.

    The donors are the estate's own bytes, following _next6/tools/n7_chassis_furniture.py:
    the way-home anchor is the single form used on 50 carriers, and the Made by
    Matt splash is the 503-byte inline SVG used on 116, read from
    _next6/tools/nav1_splash.html rather than retyped.

WHY THE GUIDANCE TOGGLE IS THE ESTATE'S MECHANISM MINUS ONE LINE

The estate toggle (_next6/tools/n6m_guide_toggle.py) is: a `data-mbm-guide`
attribute, hidden unless `html.mbm-guide-on`, an "Guidance" button, the G key,
all inside `@media screen` so print cannot change -- and it persists the open
state in `localStorage` under `mbm_guide_v1`.

That last part cannot come here. G3 requires ZERO storage APIs across all eight
lessons, and the same conflict is already on the record: n7_chassis_furniture.py
held PH-3 back for exactly this reason, and every new deck declares
`storageKeys: []`. So the mechanism is reproduced faithfully and the persistence
is dropped. The toggle then defaults closed on every load, which satisfies R4's
"hidden by default" more strictly than a persisting one, not less -- a persisted
toggle can open a lesson with staff notes already on screen in front of a class.

WHAT IS DELIBERATELY NOT DONE HERE

The usage layer is not authored into these files. The publisher adds it: Site
domain-split/usage_discovery.py says education lesson HTML gets "one published
adapter, just like the existing lesson navigation". Writing one into source would
be a second, divergent copy of a thing the build owns. It is asserted at P6
against the served page instead.

Idempotent and strip-reversible: every addition is comment-marked, and --strip
returns the file byte-identical to intake.

USAGE
  python3 tools/gc1/repair_weeks.py --unit <dir> [--dry] [--strip] [--intake <dir>]
  python3 tools/gc1/repair_weeks.py --self-test
"""
import argparse
import glob
import os
import re
import sys

OPEN, CLOSE = '<!--gc1-p2:v1-->', '<!--/gc1-p2-->'
HERE = os.path.dirname(os.path.abspath(__file__))
SPLASH_DONOR = os.path.join(HERE, '..', '..', '_next6', 'tools', 'nav1_splash.html')

WAYHOME = ('<a class="mbmhome" href="%sindex.html" '
           'aria-label="Back to the Lessons catalogue">← Lessons</a>')

FURNITURE_CSS = (
    '<style id="gc1-furniture-css">'
    '@media print{.mbmhome,.n6-splash,.n6m-guide-btn{display:none!important}}'
    '.mbmhome{display:inline-block;margin:6px 0 0 8px;font:600 .85rem/1.4 "Segoe UI",Arial,sans-serif;'
    'color:#1e3a8a;text-decoration:none}.mbmhome:hover,.mbmhome:focus{text-decoration:underline}'
    '@media screen{[data-mbm-guide]{display:none!important}'
    'html.mbm-guide-on [data-mbm-guide]{display:revert!important}'
    '.n6m-guide-btn{position:fixed;right:12px;bottom:12px;z-index:2147483000;'
    'font:600 .8rem/1.2 "Segoe UI",Arial,sans-serif;padding:7px 11px;'
    'border:2px solid currentColor;border-radius:8px;background:#fff;color:#1e3a8a;cursor:pointer}'
    '.n6m-guide-btn[aria-pressed="true"]{background:#1e3a8a;color:#fff}}'
    '</style>'
)

# The estate mechanism with the persistence removed. No localStorage, no
# sessionStorage, no indexedDB: the button flips a class on <html> and nothing is
# written anywhere, so the lesson opens closed every time.
GUIDE_JS = (
    '<script id="gc1-guide-js">(function(){'
    'var R=document.documentElement,b=document.createElement("button");'
    'b.className="n6m-guide-btn";b.type="button";b.textContent="ⓘ Guidance";'
    'b.setAttribute("aria-pressed","false");'
    'b.setAttribute("aria-label","Show or hide adult guidance");'
    'function set(on){R.classList.toggle("mbm-guide-on",on);'
    'b.setAttribute("aria-pressed",on?"true":"false")}'
    'b.addEventListener("click",function(){set(!R.classList.contains("mbm-guide-on"))});'
    'document.addEventListener("keydown",function(e){'
    'if((e.key==="g"||e.key==="G")&&!/^(INPUT|TEXTAREA|SELECT)$/.test((e.target.tagName||""))){'
    'set(!R.classList.contains("mbm-guide-on"))}});'
    'document.body.appendChild(b);set(false)})();</script>'
)

PRINT_JS = (
    '<script id="gc1-print-js">(function(){'
    'var D=%(data)s;'
    'function fill(){var el=document.querySelector(".print-record");if(!el)return;'
    'var r=(state&&state.responses)||{};'
    'var head="<h1>GROW Computing Week "+WEEK+": "+esc(D.title)+"</h1>"'
    '+"<p><b>"+esc(D.goal)+"</b></p>"'
    '+"<p>Name: ______________________  Date: ____________  Route: "'
    '+esc(r.route||"Main task")+"</p>";'
    'var body=Object.keys(r).filter(function(k){return k!=="route"})'
    '.map(function(k){return "<p><b>"+esc(k)+"</b><br>"+esc(r[k])+"</p>"}).join("");'
    'var tail="<p>Saved Scratch project: "+esc(D.save)'
    '+" __________  Adult response: ______________________</p>";'
    'el.innerHTML=head+body+tail}'
    'window.gc1FillPrint=fill;'
    'addEventListener("beforeprint",fill);'
    'var pb=document.getElementById("printBtn");'
    'if(pb)pb.addEventListener("click",function(){fill();window.print()});'
    '})();</script>'
)

PRINT_BTN = '<button id="printBtn">Print my record</button>'
RECORD_BTN_RE = re.compile(r'<button id="record"')


def depth_prefix(rel):
    """One ../ per directory level between the file and the repo root."""
    return '../' * rel.replace(os.sep, '/').count('/')


def data_object(src):
    """Weeks 1-2 call their lesson data DATA; weeks 3-8 call it W."""
    return 'DATA' if re.search(r'\bconst DATA\s*=', src) else 'W'


def strip(src):
    while OPEN in src:
        i = src.find(OPEN)
        j = src.index(CLOSE, i) + len(CLOSE)
        src = src[:i] + src[j:]
    # d2 is an in-place rename rather than an insertion, so it reverses by name.
    src = src.replace('id="centreBack"', 'id="centre"').replace('id="centreReset"', 'id="centre"')
    src = src.replace("($('#centreBack')||$('#centreReset'))", "$('#centre')")
    return src


def repair_lesson(src, rel):
    """Return (repaired source, list of repairs applied)."""
    did = []
    if OPEN in src:
        return src, ['already']

    # --- d2: two ternary arms sharing one id, given distinct ones ---
    if src.count('id="centre"') > 1:
        first = src.find('id="centre"')
        second = src.find('id="centre"', first + 1)
        src = src[:second] + 'id="centreReset"' + src[second + len('id="centre"'):]
        src = src[:first] + 'id="centreBack"' + src[first + len('id="centre"'):]
        src = src.replace("$('#centre')", "($('#centreBack')||$('#centreReset'))")
        did.append('d2')

    # --- d1: the container, the button, the filler ---
    # Weeks 1-2 already have this container (empty) and weeks 7-8 already have it
    # filled, so only weeks 3-6 gain one. It is comment-marked, because strip has
    # to remove outright an element those six never had -- and nothing else is
    # mutated, so a lesson that shipped its own id keeps it untouched. An earlier
    # draft added id="printRecord" to the existing div instead, and its strip could
    # not tell that id from the one weeks 7-8 ship, so it removed both.
    if 'class="print-record"' not in src:
        m = re.search(r'<footer\b', src)
        if not m:
            return src, ['no-footer']
        src = (src[:m.start()] + OPEN + '<div class="print-record"></div>'
               + CLOSE + src[m.start():])
        did.append('d1:container')

    if 'id="printBtn"' not in src:
        m = RECORD_BTN_RE.search(src)
        if m:
            src = src[:m.start()] + OPEN + PRINT_BTN + CLOSE + src[m.start():]
            did.append('d1:button')

    if 'gc1-print-js' not in src and 'function fillPrint' not in src:
        src = src.replace('</body>', OPEN + (PRINT_JS % {'data': data_object(src)}) + CLOSE + '</body>', 1)
        did.append('d1:filler')

    # --- d4: way home, Made by Matt, guidance toggle. prev/next is already there. ---
    splash = open(os.path.abspath(SPLASH_DONOR), encoding='utf-8').read().strip()
    m = re.search(r'<body\b[^>]*>', src)
    if not m:
        return src, did + ['no-body']
    head = OPEN + FURNITURE_CSS + WAYHOME % depth_prefix(rel) + CLOSE
    src = src[:m.end()] + head + src[m.end():]
    src = src.replace('</body>', OPEN + '<div class="n6-splash">' + splash + '</div>'
                      + GUIDE_JS + CLOSE + '</body>', 1)
    did.append('d4')
    return src, did


HUB_NAV_ID = 'gc1-hub-nav'


def repair_hub(src, this_file, hubs):
    """d3: every hub reaches every other hub, and names the whole unit."""
    if HUB_NAV_ID in src:
        return src, 'already'
    links = ''.join(
        '<li><a href="%s">%s</a></li>' % (f, label)
        for f, label in hubs if f != this_file)
    nav = (OPEN + '<nav id="' + HUB_NAV_ID + '" aria-label="The rest of this unit">'
           '<h2>The rest of this unit</h2>'
           '<p>GROW Computing runs for eight weeks. Every week is on one of these three pages.</p>'
           '<ul>' + links + '</ul></nav>' + CLOSE)
    if '</main>' in src:
        return src.replace('</main>', nav + '</main>', 1), 'patched'
    if '</body>' in src:
        return src.replace('</body>', nav + '</body>', 1), 'patched'
    # The Weeks 1-2 hub is a minimal document with no <body> and no <main> -- it
    # ends at </html>. Refusing it would leave a third of the unit unreachable
    # from the page a teacher opens first.
    if '</html>' in src:
        return src.replace('</html>', nav + '</html>', 1), 'patched'
    return src, 'no-anchor'


HUBS = [
    ('Start_Here_Weeks_01_02.html', 'Weeks 1 and 2 · Get a result, Control a character'),
    ('Start_Here_Weeks_03_06.html', 'Weeks 3 to 6 · Build the world, controls, rules, finish'),
    ('Start_Here_Weeks_07_08.html', 'Weeks 7 and 8 · Add one challenge, Test and improve'),
]


def run(unit, destprefix, dry=False, do_strip=False, intake=None):
    tally = {}
    for path in sorted(glob.glob(os.path.join(unit, 'Week_*', '*Interactive.html'))):
        rel = os.path.join(destprefix, os.path.relpath(path, unit))
        src = open(path, encoding='utf-8').read()
        if do_strip:
            out, key = strip(src), 'stripped'
            if intake:
                orig = open(os.path.join(intake, os.path.relpath(path, unit)), encoding='utf-8').read()
                key = 'strip==intake' if out == orig else 'STRIP MISMATCH'
        else:
            out, did = repair_lesson(src, rel)
            key = ','.join(did) or 'none'
        if not dry and not (do_strip and intake):
            open(path, 'w', encoding='utf-8').write(out)
        tally[key] = tally.get(key, 0) + 1

    for name, _ in HUBS:
        path = os.path.join(unit, name)
        if not os.path.exists(path):
            tally['hub-missing'] = tally.get('hub-missing', 0) + 1
            continue
        src = open(path, encoding='utf-8').read()
        if do_strip:
            out, key = strip(src), 'hub:stripped'
        else:
            out, key = repair_hub(src, name, HUBS)
            key = 'hub:' + key
        if not dry:
            open(path, 'w', encoding='utf-8').write(out)
        tally[key] = tally.get(key, 0) + 1
    return tally


def self_test():
    n, bad = [0], []
    def want(name, cond):
        n[0] += 1
        print(('  PASS  ' if cond else '  FAIL  ') + name)
        if not cond: bad.append(name)

    # Weeks 3-6 shape: no container at all, data named W, one record button.
    w36 = ('<html><body><header><div class="toolbar"><button id="record">R</button></div></header>'
           '<script>const W={"title":"T","goal":"G","save":"S.sb3"};const WEEK=3;</script>'
           '<footer><button id="prev">p</button><button id="next">n</button></footer></body></html>')
    out, did = repair_lesson(w36, 'ICT/Teaching_Packs/GROW_Computing/Week_03/x.html')
    want('weeks 3-6 gain the print container', 'class="print-record"' in out)
    want('  ... and it lands before the footer', out.index('print-record') < out.index('<footer'))
    want('weeks 3-6 gain the print button', 'id="printBtn"' in out)
    want('weeks 3-6 gain the filler wired to beforeprint', 'beforeprint' in out and 'gc1-print-js' in out)
    want('the filler reads W for weeks 3-8', 'var D=W;' in out)
    want('the way home is the estate anchor', 'class="mbmhome"' in out and '← Lessons' in out)
    want('  ... at the right depth for Week_03', 'href="../../../../index.html"' in out)
    want('the Made by Matt splash is added', 'n6-splash' in out)
    want('the guidance toggle is added', 'n6m-guide-btn' in out)
    want('the toggle stores NOTHING (G3)',
         not re.search(r'localStorage|sessionStorage|indexedDB', out))
    want('the toggle starts closed (R4)', 'set(false)' in out)
    want('furniture is print-hidden', '.n6m-guide-btn{display:none!important}' in out.replace('.mbmhome,.n6-splash,', ''))

    # Weeks 1-2 shape: container present but empty, data named DATA.
    w12 = ('<html><body><header><div class="toolbar"><button id="record">R</button></div></header>'
           '<div class="print-record"></div>'
           '<script>const DATA={"title":"T","goal":"G","save":"S.sb3"};const WEEK=1;'
           'x=`<button id="centre">a</button>`;y=`<button id="centre">b</button>`;'
           "$('#centre').onclick=f;</script>"
           '<footer></footer></body></html>')
    out2, did2 = repair_lesson(w12, 'ICT/Teaching_Packs/GROW_Computing/Week_01/x.html')
    want('weeks 1-2 keep their one container, untouched', out2.count('class="print-record"') == 1
         and 'id="printRecord"' not in out2)
    want('the filler reads DATA for weeks 1-2', 'var D=DATA;' in out2)
    want('d2: the two arms get distinct ids', 'id="centreBack"' in out2 and 'id="centreReset"' in out2)
    want('d2: no id="centre" survives', 'id="centre"' not in out2)
    want('d2: the binding reaches whichever arm rendered',
         "($('#centreBack')||$('#centreReset'))" in out2)

    # Idempotence and reversibility are the two properties that let this be re-run.
    again, did3 = repair_lesson(out, 'ICT/Teaching_Packs/GROW_Computing/Week_03/x.html')
    want('re-running changes nothing', again == out and did3 == ['already'])
    want('strip returns weeks 3-6 byte-identical to intake', strip(out) == w36)
    want('strip returns weeks 1-2 byte-identical to intake', strip(out2) == w12)

    # The regression that cost a round-trip: weeks 7-8 already ship
    # <div class="print-record" id="printRecord">. Repair must not touch it and
    # strip must not take the id off a file it never patched.
    w78 = ('<html><body><header><div class="toolbar"><button id="printBtn">P</button>'
           '<button id="record">R</button></div></header>'
           '<div class="print-record" id="printRecord"></div>'
           '<script>const W={"title":"T","goal":"G","save":"S.sb3"};const WEEK=7;'
           'function fillPrint(){}</script><footer></footer></body></html>')
    out7, _ = repair_lesson(w78, 'a/b/c/d/x.html')
    want('a lesson that already prints keeps its own id', 'id="printRecord"' in out7)
    want('  ... and gains no second container', out7.count('class="print-record"') == 1)
    want('  ... and strip returns it byte-identical', strip(out7) == w78)

    # A lesson with no footer must be refused, not silently half-patched.
    out4, did4 = repair_lesson('<html><body><div class="toolbar"></div></body></html>', 'a/b.html')
    want('a lesson with no footer is refused, not half-patched', 'no-footer' in did4)

    # d3
    hub, key = repair_hub('<html><body><main>x</main></body></html>', HUBS[0][0], HUBS)
    want('a hub gains links to the other two', key == 'patched'
         and hub.count('<li><a href=') == 2)
    want('  ... and not to itself', HUBS[0][0] not in hub.split('<nav id="gc1-hub-nav"')[1])
    want('  ... and it names weeks 7 and 8', 'Weeks 7 and 8' in hub)
    want('re-running the hub changes nothing', repair_hub(hub, HUBS[0][0], HUBS)[1] == 'already')

    print('\n%d checks, %d failed' % (n[0], len(bad)))
    for b in bad: print('  FAILED:', b)
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit')
    ap.add_argument('--destprefix', default='ICT/Teaching_Packs/GROW_Computing')
    ap.add_argument('--intake')
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--strip', action='store_true', dest='do_strip')
    ap.add_argument('--self-test', action='store_true', dest='self_test')
    a = ap.parse_args()
    if a.self_test:
        sys.exit(self_test())
    if not a.unit:
        print('--unit is required', file=sys.stderr)
        sys.exit(2)
    tally = run(a.unit, a.destprefix, a.dry, a.do_strip, a.intake)
    for k in sorted(tally):
        print('  %-24s %d' % (k, tally[k]))
    sys.exit(1 if any(k.startswith(('no-', 'STRIP', 'hub-missing')) for k in tally) else 0)


if __name__ == '__main__':
    main()
