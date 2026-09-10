#!/usr/bin/env python3
"""tools/gc1/wire_served.py - GC1 P4: the served surfaces.

TWO THINGS EACH WEEK'S PAGE MUST OFFER

R3. THE SIBLING .sb3, BESIDE THE data: URI, NOT INSTEAD OF IT.

Every lesson already carries its Scratch projects as base64 `data:` URIs built at
runtime from FILES[]. That is the offline path and it is load-bearing: the pack
works from a USB stick with no network. But a managed school browser can refuse a
`data:` download outright, and when it does the pupil gets nothing and no error.

So each week also links the real file sitting next to it in Scratch_Projects/.
Both ship. Neither replaces the other, because they fail in different situations:
the sibling link needs the file to be served, the data: URI needs the browser to
allow data: downloads, and a classroom will meet both failures.

R4/P4. THE PAPER ROUTE HAS TO BE FINDABLE WITHOUT KNOWING IT EXISTS.

A cover teacher who has never seen this unit, told at 8:55 that a pupil has no
device today, must be able to find the paper route from the lesson page. Not from
a folder, not from a subject page, not from a sentence in a teacher guide. So it
is a link on the page, labelled in plain words, next to the Scratch downloads --
and the same content is printable from the page itself (see embed_paper_route.py),
so a blocked download still leaves a way through.

WHERE IT GOES, AND WHY THAT MATTERS

Outside `main#content`. These lessons re-render `#content` on every stage change
and every route change -- 24 times per visit -- so anything written inside it is
destroyed by the next click. The block is placed immediately before `<footer>`,
which persists.

Idempotent and strip-reversible.

USAGE
  python3 tools/gc1/wire_served.py --unit <dir> [--strip]
  python3 tools/gc1/wire_served.py --self-test
"""
import argparse
import glob
import json
import os
import re
import sys

OPEN, CLOSE = '<!--gc1-p4:v1-->', '<!--/gc1-p4-->'

CSS = ('<style id="gc1-offline-css">'
       '.gc1-offline{max-width:1160px;margin:0 auto;padding:18px 28px;'
       'border-top:1px solid var(--line,#c5d4c8)}'
       '.gc1-offline h2{font-size:20px;margin:0 0 6px}'
       '.gc1-offline p{font-size:17px;margin:4px 0 10px}'
       '.gc1-offline ul{list-style:none;margin:0;padding:0;display:flex;gap:10px;flex-wrap:wrap}'
       '.gc1-offline a{display:inline-block;min-height:44px;padding:9px 15px;border-radius:7px;'
       'border:1px solid var(--green,#19624a);color:var(--green,#19624a);text-decoration:none}'
       '.gc1-offline a:hover,.gc1-offline a:focus{background:var(--pale,#e7f0e7)}'
       '.gc1-paper-link{background:var(--green,#19624a);color:#fff!important}'
       '@media print{.gc1-offline{display:none!important}}'
       '@media(max-width:750px){.gc1-offline{padding:16px 18px}.gc1-offline ul{flex-direction:column}}'
       '</style>')


def files_in(src):
    """The .sb3 names this lesson carries, read from its own FILES[] payload."""
    m = re.search(r'FILES\s*=\s*(\[.*?\])\s*,\s*WALLS', src, re.S)
    if not m:
        m = re.search(r'FILES\s*=\s*(\[.*?\])\s*;', src, re.S)
    if not m:
        return []
    try:
        return [f['name'] for f in json.loads(m.group(1)) if str(f.get('name', '')).endswith('.sb3')]
    except Exception:
        return re.findall(r'"name":\s*"([^"]+\.sb3)"', m.group(1))


# G8 wants every file reachable; R4 wants teacher material hidden by default.
# Those are not in conflict. The staff links are IN the page and marked
# data-mbm-guide="staff", so the guidance toggle reveals them and the default DOM
# never shows them. An orphaned teacher answer sheet is worse than a hidden one:
# nobody can find it when they need it, and nothing tells them it exists.
def staff_block(week):
    w = '%02d' % week
    items = [
        ('Paper_Route/GROW_Week_%s_Paper_Route.docx' % w, 'Paper route (editable DOCX)'),
        ('Teacher_Only/GROW_Week_%s_Paper_Route_Answers.pdf' % w, 'Paper route answers (PDF)'),
        ('Teacher_Only/GROW_Week_%s_Paper_Route_Answers.docx' % w, 'Paper route answers (editable DOCX)'),
        ('Teacher_Only/GROW_Week_%s_Teacher_Guide.pdf' % w, 'Teacher guide (PDF)'),
        ('Teacher_Only/W%s_Teacher_Model.sb3' % w, 'Teacher model project (SB3)'),
        ('../Teacher_Only/GROW_Computing_Final_Evidence_Check.pdf', 'Final evidence check (PDF)'),
    ]
    lis = ''.join('<li><a href="%s" download>%s</a></li>' % (h, t) for h, t in items)
    return ('<section class="gc1-offline gc1-staff" data-mbm-guide="staff" '
            'aria-label="Adult guidance and teacher files">'
            '<h2>For adults</h2>'
            '<p>These are teacher files. They are hidden until the Guidance button is pressed.</p>'
            '<ul>' + lis + '</ul>'
            '<p>Record the route a pupil took in the teacher guide. Never on the AQA summary '
            'sheet, which is completed the same way whichever route the pupil took.</p>'
            '</section>')


def block(week, names):
    links = ''.join(
        '<li><a href="Scratch_Projects/%s" download>%s</a></li>' % (n, n) for n in names)
    paper = ('<li><a class="gc1-paper-link" '
             'href="Paper_Route/GROW_Week_%02d_Paper_Route.pdf">'
             'Paper route for this week (PDF)</a></li>' % week)
    return (OPEN + CSS +
            '<section class="gc1-offline" aria-label="Files and the paper route">'
            '<h2>If the screen route is not available today</h2>'
            '<p>Every part of this week can be done on paper, with no device. '
            'Open the paper route below, or press <b>Print my record</b> at the top of the page '
            'and it prints the same thing.</p>'
            '<ul>' + paper + links + '</ul>'
            '<p class="gc1-note">The Scratch files above are also built into this page, so the '
            'download buttons in the lesson still work with no network. If your browser blocks a '
            'download, use the links above instead.</p>'
            '</section>' + staff_block(week) + CLOSE)


def wire(src, week):
    if OPEN in src:
        return src, 'already'
    if '<footer' not in src:
        return src, 'no-footer'
    names = files_in(src)
    if not names:
        return src, 'no-files'
    i = src.index('<footer')
    return src[:i] + block(week, names) + src[i:], 'wired:%d' % len(names)


def strip(src):
    while OPEN in src:
        i = src.find(OPEN)
        j = src.index(CLOSE, i) + len(CLOSE)
        src = src[:i] + src[j:]
    return src


def self_test():
    n, bad = [0], []
    def want(name, cond):
        n[0] += 1
        print(('  PASS  ' if cond else '  FAIL  ') + name)
        if not cond: bad.append(name)

    page = ('<html><body><main id="content">stage</main>'
            '<script>const WEEK=5,W={},FILES=[{"name":"W05_Bug_Hunt.sb3","data":"AAA"},'
            '{"name":"W05_Recovery_Controls.sb3","data":"BBB"}],WALLS=[];</script>'
            '<footer>f</footer></body></html>')
    out, key = wire(page, 5)
    want('a lesson is wired', key == 'wired:2')
    want('both sibling .sb3 links are added',
         'Scratch_Projects/W05_Bug_Hunt.sb3' in out and 'Scratch_Projects/W05_Recovery_Controls.sb3' in out)
    want('the paper route is linked by name', 'GROW_Week_05_Paper_Route.pdf' in out)
    want('  ... and labelled so a cover teacher finds it', 'Paper route for this week' in out)
    want('  ... and it says the week can be done with no device', 'no device' in out)
    want('the data: URIs are NOT removed (R3: both ship)', '"data":"AAA"' in out.replace(' ', ''))

    # The placement is the part that would fail silently: #content is re-rendered
    # 24 times a visit, so anything inside it is gone after one click.
    want('it lands OUTSIDE main#content', out.index('gc1-offline') > out.index('</main>'))
    want('  ... and before the footer', out.index('gc1-offline') < out.index('<footer'))
    want('it is hidden on paper, because the printed sheet carries the route itself',
         '@media print{.gc1-offline{display:none!important}' in out)

    want('the staff block is added', 'gc1-staff' in out)
    want('  ... marked for the guidance toggle, so it is hidden by default (R4/G10)',
         'data-mbm-guide="staff"' in out)
    want('  ... and it reaches the answers, the model and the evidence check',
         'Paper_Route_Answers.pdf' in out and 'W05_Teacher_Model.sb3' in out
         and 'Final_Evidence_Check.pdf' in out)
    want('  ... and the editable paper-route docx, so it is not an orphan (G8)',
         'GROW_Week_05_Paper_Route.docx' in out)
    want('  ... and it says the route goes in the teacher guide, not on the AQA form (R9)',
         'Never on the AQA summary' in out)
    want('re-running changes nothing', wire(out, 5)[1] == 'already')
    want('strip returns the page byte-identical', strip(out) == page)

    want('a lesson with no FILES is refused, not silently skipped',
         wire('<html><body><main id="content"></main><footer></footer></body></html>', 5)[1] == 'no-files')
    want('a lesson with no footer is refused',
         wire('<html><body><script>FILES=[{"name":"a.sb3"}];</script></body></html>', 5)[1] == 'no-footer')

    want('files_in reads the lesson’s own payload', files_in(page) ==
         ['W05_Bug_Hunt.sb3', 'W05_Recovery_Controls.sb3'])
    want('  ... and ignores non-sb3 entries',
         files_in('<script>FILES=[{"name":"a.sb3"},{"name":"b.png"}];</script>') == ['a.sb3'])

    print('\n%d checks, %d failed' % (n[0], len(bad)))
    for b in bad: print('  FAILED:', b)
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit')
    ap.add_argument('--strip', action='store_true', dest='do_strip')
    ap.add_argument('--self-test', action='store_true', dest='self_test')
    a = ap.parse_args()
    if a.self_test:
        sys.exit(self_test())
    if not a.unit:
        print('--unit is required', file=sys.stderr)
        sys.exit(2)
    tally = {}
    for path in sorted(glob.glob(os.path.join(a.unit, 'Week_*', '*Interactive.html'))):
        wk = int(re.search(r'Week_(\d+)', path).group(1))
        src = open(path, encoding='utf-8').read()
        out, key = (strip(src), 'stripped') if a.do_strip else wire(src, wk)
        open(path, 'w', encoding='utf-8').write(out)
        tally[key] = tally.get(key, 0) + 1
    for k in sorted(tally):
        print('  %-12s %d' % (k, tally[k]))
    sys.exit(1 if any(k.startswith('no-') for k in tally) else 0)


if __name__ == '__main__':
    main()
