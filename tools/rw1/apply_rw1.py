#!/usr/bin/env python3
"""RW1 / RW1-A: turn the supplied return-week pack bytes into the two served files.

The pack is the authority for teaching content; the LIVE file is the authority for
furniture, week labels and cross-links (RW1 §6.1). Every edit below therefore
either deletes pack-only scaffolding or copies a live string verbatim -- nothing
here is composed.

Idempotent: running it twice changes nothing the second time. --check reports what
would move without writing.
"""
import argparse, re, sys, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import marking_card
import furniture
import ta_prompts
import print_identity
import pathways

REPO = Path(__file__).resolve().parents[2]
BRANDLINE_CSS = '.brandline{font-weight:950;color:var(--growdark);letter-spacing:.08em;text-transform:uppercase}'


def report(name, before, after, expect=None):
    moved = before != after
    print('  [%s] %-46s %s' % ('ok' if moved or expect == 0 else '--', name,
                               'applied' if moved else 'already applied / nothing to do'))
    return after


def brandline(text, which, pw):
    """B2: the pupil-visible dated review-meta lines become ONE live-form
    brandline on the title slide. Live carries one identity brandline per FILE,
    not per slide (measured on BUILD: 1 of 2 .brandline elements, the other is
    'Staff route'), so the surplus are deleted rather than relabelled."""
    forms = [re.compile(f) for f in pathways.need(pw, 'review_meta')]
    pat = next((f for f in forms if f.search(text)), forms[0])
    n = len(pat.findall(text))
    if not n:
        return text, 0
    text = pat.sub(pathways.need(pw, 'brandline', which), text, count=1)
    text = pat.sub('', text)
    # the live rule needs the live variable; the pack defines neither
    if BRANDLINE_CSS not in text:
        text = text.replace('.review-meta{', BRANDLINE_CSS + '\n.review-meta{', 1)
    growdark = pathways.need(pw, 'growdark')
    if growdark not in text:
        before = text
        text = re.sub(r'(--bg:#fff)', growdark + ';' + r'\1', text, count=1)
        assert text != before, ('the --bg:#fff anchor was not found, so %s was '
                                'never injected -- re.sub returns its input '
                                'unchanged on no match' % growdark)
    return text, n


def strip_lundy(text):
    """D2 / F2. Seven are whole-rule deletions; one is a selector-list edit, where
    .lundy-grid rides in a group with three live selectors that must survive."""
    text = text.replace('.content-grid,.arrival-grid,.compare-grid-3,.lundy-grid',
                        '.content-grid,.arrival-grid,.compare-grid-3')
    text = re.sub(r'\.lundy-(?:grid|box)\b[^{}]*\{[^}]*\}', '', text)
    text = re.sub(r'\.tag-lundy\b[^{}]*\{[^}]*\}', '', text)
    text = re.sub(r',?\s*\.(?:lundy-grid|lundy-box|tag-lundy)\b(?=[,{ ])', '', text)
    return text


def strip_self_links(text):
    """E1. The anchor sits alone in an <li> inside the staff TA dialog; drop the
    whole item so no empty bullet is left. The nhs.uk citation beside it STAYS
    (RW1-A E2): measured staff-gated, href only, no resource load."""
    text = re.sub(r'<li><a href="https://madebymatt\.uk/[^"]*"[^>]*>[^<]*</a></li>', '', text)
    text = re.sub(r'<a href="https://madebymatt\.uk/[^"]*"[^>]*>[^<]*</a>', '', text)
    return text


def fix_caption(text, pw):
    """D1. Measured string literals, one per defect found in that pack -- never a
    general 'tidy the spacing' pass, which would edit teaching content."""
    for before, after in pw.get('literal_fixes') or []:
        text = text.replace(before, after)
    return text


def cross_links(text, which, pw):
    """D3, and a defect the order did not name: the pack's forward links are
    PACK-RELATIVE. Every lesson lands in the SAME served directory, so each link
    must become the target's live filename or it 404s.

    Two lessons make 'the other one' unambiguous. Three do not -- L1 links
    forward to L2 and L2 back to L1 and on to L3 -- so the mapping is BY TARGET,
    read from pack_links as {pack-relative href: lesson key}, and never inferred
    from which file is being processed.
    """
    keys = list(pathways.need(pw, 'lessons'))
    for href, (kind, target) in pathways.need(pw, 'pack_links'):
        if kind == 'literal':
            repl = target
        elif target is None:
            if len(keys) != 2:
                raise ValueError('%s has %d lessons, so ("lesson", None) is '
                                 'ambiguous; name the target' % (pw['name'], len(keys)))
            repl = Path(pathways.need(pw, 'live', keys[1 - keys.index(which)])).name
        else:
            repl = Path(pathways.need(pw, 'live', target)).name
        text = text.replace(href, repl)
    return text


DETAILS = re.compile(
    r'<details class="teacher-only"><summary>Lundy alongside learning[^<]*</summary>.*?</details>',
    re.S)


def assessment_layer(text, which, pw):
    """§4.2 removes the Lundy desk card; §4.3 puts the marking card in its place --
    in the SAME position, so no staff guidance is deleted without a replacement.
    §4.5 adds the print route beside the organiser's, on the existing mechanism."""
    if 'id="marking-card"' not in text:
        text = DETAILS.sub(lambda _: marking_card.card(which, pw), text, count=1)
    if 'id="print-marking"' not in text:
        # last print section closes just before #print-area's own close
        i = text.rfind('</section></div>')
        if i < 0:
            i = text.rfind('</section>')
        text = (text[:i + len('</section>')] + marking_card.print_section(which, pw)
                + text[i + len('</section>'):])
    if '.mk-card{' not in text:
        text = text.replace('.review-meta{', marking_card.CSS + '\n.review-meta{', 1)
    return text



# LW1 §A2 · the knowledge organiser's own dated header, which every earlier check
# walked straight past.
#
# HOW IT HID. The organiser header is rendered TWICE: once as <text> inside the
# SVG (both the on-screen #ko-screen-group and the printed #ko-print-group) and
# once as the <p> transcript behind "Read organiser text". print_identity only
# ever looked for <p class="science-meta">, so the SVG was invisible to it. And
# the string is spaced "Week 8  |  19 October 2026" with DOUBLE spaces around the
# pipes, so a grep for the single-spaced form returned zero -- which is what my
# own B3 check ran and reported clean.
#
# The organiser is a PUPIL sheet (#print-organiser carries data-print-route="all"),
# so under RW1-E §W2 it may carry no week token and no date.
#
# NOTHING REPLACES THEM. The header is three lines and the first two already read
# "BUILD SCIENCE  |  KNOWLEDGE ORGANISER" and then the sheet title -- which IS the
# pathway / subject / lesson-title identity, with the sheet type standing in for
# the route. Substituting the title into the third line produced "Sugar evidence
# Sugar Evidence  |  Made by Matt", a near-duplicate differing only in case. So
# the week and the date are deleted and "Made by Matt" stays where it was: the
# smallest pupil-visible delta that satisfies W2, per RW1-A B6.
#
# The transcript is rewritten in the SAME pass and by the same rule. Changing the
# SVG alone would leave the screen-reader text disagreeing with the picture, which
# is a worse accessibility outcome than the date.
ORGANISER_HEAD = re.compile(
    r'Week\s*\d{1,2}\s*\|\s*'
    r'\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September'
    r'|October|November|December)\s+\d{4}\s*\|\s*')


def organiser_identity(text, which, pw):
    """Delete the week token and the date from the organiser header, on every
    surface that renders it -- the SVG and its transcript alike."""
    pathways.need(pw, 'identity', which)      # refuse to run on an unmeasured pathway
    return ORGANISER_HEAD.sub('', text)


def run(which, src, pw, check=False):
    text = original = Path(src).read_text(encoding='utf-8')
    print('%s  %s  [%s]' % (which, src, pw['name']))
    t, n = brandline(text, which, pw)
    text = report('B2 dated review-meta -> live brandline (%d found)' % n, text, t)
    text = report('D1 measured literal fixes (%d)' % len(pw.get('literal_fixes') or []),
                  text, fix_caption(text, pw))
    text = report('D2 lundy selectors', text, strip_lundy(text))
    text = report('E1 madebymatt.uk self-link', text, strip_self_links(text))
    text = report('D3 cross-link rewired to the served sibling', text,
                  cross_links(text, which, pw))
    text = report('4.2/4.3/4.5 Lundy desk card -> marking card + print route', text,
                  assessment_layer(text, which, pw))
    prompted, npr = ta_prompts.apply(text, which, pw)
    text = report('I1 nine stage-specific TA prompts (%d hosts)' % npr, text, prompted)
    before_org = text
    text = organiser_identity(text, which, pw)
    text = report('A2 organiser header: week token and date deleted, SVG + transcript (%d)'
                  % len(ORGANISER_HEAD.findall(before_org)), before_org, text)
    ident, nadd, nclean, nnorm, pstats = print_identity.apply(text, which, pw)
    text = report('W print identity (%d of %d pupil sections: +%d added, %d dates '
                  'removed, %d normalised, %d already correct; %d staff skipped, '
                  '%d sections examined)'
                  % (nadd + nclean + nnorm + pstats['already_correct'],
                     pstats['pupil_sections'], nadd, nclean, nnorm,
                     pstats['already_correct'], pstats['staff_skipped'],
                     pstats['sections_examined']), text, ident)
    carried, missing = furniture.carry(text, which, pw)
    if missing:
        print('  [FAIL] furniture parts not found in live: ' + ', '.join(missing))
    text = report('D4/D6 estate furniture carried from live', text, carried)
    target = pathways.need(pw, 'live', which)
    out = REPO / target
    if not check:
        out.write_text(text, encoding='utf-8')
    print('  bytes %d -> %d   target %s' % (len(original.encode()), len(text.encode()), target))
    return text


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--pack', required=True)
    ap.add_argument('--pathway', default='BUILD', choices=sorted(pathways.ALL))
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    pw = pathways.ALL[a.pathway]
    p = Path(a.pack)
    for which in pathways.need(pw, 'lessons'):
        run(which, p / pathways.need(pw, 'pack', which), pw, a.check)
