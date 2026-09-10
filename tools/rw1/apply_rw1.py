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

REPO = Path(__file__).resolve().parents[2]
LIVE = {
    'A': 'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html',
    'B': 'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8B_Autumn_Science_Checkpoint_Do.html',
}
# Copied out of the live counterpart, not composed (RW1-A B2).
BRANDLINE = {
    'A': '<p class="brandline">BUILD &middot; Science &middot; Week 8A &middot; Explore</p>',
    'B': '<p class="brandline">BUILD &middot; Science &middot; Week 8B &middot; Do</p>',
}
BRANDLINE_CSS = '.brandline{font-weight:950;color:var(--growdark);letter-spacing:.08em;text-transform:uppercase}'
GROWDARK = '--growdark:#355E7B'
PACK_META = re.compile(r'<p class="review-meta">BUILD &middot; SCIENCE &middot; Week 8 &middot; w/c 19 October 2026</p>')
PACK_META_PLAIN = re.compile(r'<p class="review-meta">BUILD · SCIENCE · Week 8 · w/c 19 October 2026</p>')


def report(name, before, after, expect=None):
    moved = before != after
    print('  [%s] %-46s %s' % ('ok' if moved or expect == 0 else '--', name,
                               'applied' if moved else 'already applied / nothing to do'))
    return after


def brandline(text, which):
    """B2: the nine pupil-visible dated review-meta lines become ONE live-form
    brandline on the title slide. Live carries one identity brandline per FILE,
    not per slide (measured: 1 of 2 .brandline elements, the other is 'Staff
    route'), so the surplus eight are deleted rather than relabelled."""
    pat = PACK_META if PACK_META.search(text) else PACK_META_PLAIN
    n = len(pat.findall(text))
    if not n:
        return text, 0
    text = pat.sub(BRANDLINE[which], text, count=1)
    text = pat.sub('', text)
    # the live rule needs the live variable; the pack defines neither
    if BRANDLINE_CSS not in text:
        text = text.replace('.review-meta{', BRANDLINE_CSS + '\n.review-meta{', 1)
    if GROWDARK not in text:
        text = re.sub(r'(--bg:#fff)', GROWDARK + ';' + r'\1', text, count=1)
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


def fix_caption(text):
    """D1. One string literal in a ternary; the proof is the rendered caption."""
    return text.replace('E gives3+3+3+3=12 g sugar per 100 g.',
                        'E gives 3+3+3+3 = 12 g sugar per 100 g.')


def cross_links(text, which):
    """D3, and a defect the order did not name: the pack's forward link is
    PACK-RELATIVE (../Lesson_B_Body_Checkpoint/...). Both files land in the same
    served directory, so it must become the live sibling filename or it 404s."""
    sib = {'A': Path(LIVE['B']).name, 'B': Path(LIVE['A']).name}[which]
    text = text.replace('../Lesson_B_Body_Checkpoint/BUILD_W8B_Interactive.html', sib)
    text = text.replace('../Lesson_A_Sugar_Evidence/BUILD_W8A_Interactive.html', sib)
    return text


DETAILS = re.compile(
    r'<details class="teacher-only"><summary>Lundy alongside learning[^<]*</summary>.*?</details>',
    re.S)


def assessment_layer(text, which):
    """§4.2 removes the Lundy desk card; §4.3 puts the marking card in its place --
    in the SAME position, so no staff guidance is deleted without a replacement.
    §4.5 adds the print route beside the organiser's, on the existing mechanism."""
    if 'id="marking-card"' not in text:
        text = DETAILS.sub(lambda _: marking_card.card(which), text, count=1)
    if 'id="print-marking"' not in text:
        # last print section closes just before #print-area's own close
        i = text.rfind('</section></div>')
        if i < 0:
            i = text.rfind('</section>')
        text = text[:i + len('</section>')] + marking_card.print_section(which) + text[i + len('</section>'):]
    if '.mk-card{' not in text:
        text = text.replace('.review-meta{', marking_card.CSS + '\n.review-meta{', 1)
    return text


def run(which, src, check=False):
    text = original = Path(src).read_text(encoding='utf-8')
    print('%s  %s' % (which, src))
    t, n = brandline(text, which)
    text = report('B2 dated review-meta -> live brandline (%d found)' % n, text, t)
    text = report('D1 caption spacing', text, fix_caption(text))
    text = report('D2 lundy selectors', text, strip_lundy(text))
    text = report('E1 madebymatt.uk self-link', text, strip_self_links(text))
    text = report('D3 cross-link rewired to the served sibling', text, cross_links(text, which))
    text = report('4.2/4.3/4.5 Lundy desk card -> marking card + print route', text,
                  assessment_layer(text, which))
    carried, missing = furniture.carry(text, which)
    if missing:
        print('  [FAIL] furniture parts not found in live: ' + ', '.join(missing))
    text = report('D4/D6 estate furniture carried from live', text, carried)
    out = REPO / LIVE[which]
    if not check:
        out.write_text(text, encoding='utf-8')
    print('  bytes %d -> %d   target %s' % (len(original.encode()), len(text.encode()), LIVE[which]))
    return text


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--pack', required=True)
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    p = Path(a.pack)
    run('A', p / 'Lesson_A_Sugar_Evidence/BUILD_W8A_Interactive.html', a.check)
    run('B', p / 'Lesson_B_Body_Checkpoint/BUILD_W8B_Interactive.html', a.check)
