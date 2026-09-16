#!/usr/bin/env python3
"""CX2 §8.3 · keep the stage timer off the "← Lessons" home link in the six return-week lessons.

    python3 tools/rw1/clear_home_link.py [--check] [--self-test]

The return-week chassis places `#auto-timer` fixed at (14,10), 200×48, z-index 6000, and
the N6 nav shell places the home link `a.mbmhome` inline at (8,6), 73×19. Measured in
Chromium at 1280 and 390: `document.elementFromPoint` at the link's centre returns
`DIV#auto-timer`, so the link cannot be clicked — the defect the offline-pack check
names ("Reachable lesson home control") on every one of the six.

Sixty lessons on main carry both widgets and avoid this with the estate's `mbm-nav1`
variant (home link fixed top-right). That variant would collide with the return-week
`.review-top` nav, which is also top-right, so the fix here moves the timer instead:
`left:96px` sits it 15px right of the link. Measured after the change at both widths:
the link's centre resolves to the link, the timer's own toggle still resolves to itself,
and the timer does not overlap `.review-top` (x ≥ 833 at 1280; y ≥ 62 at 390).

One rule, inserted as its own <style> after the nav shell so its provenance is visible;
no script, no text, no other layout moves.
"""
from pathlib import Path
import argparse, sys

ROOT = Path(__file__).resolve().parents[2]
LESSONS = (
    'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8B_Autumn_Science_Checkpoint_Do.html',
    'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8A_Day_And_Night_Explore.html',
    'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8B_Day_And_Night_Do.html',
    'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L1_Enzyme_Action_Introduce.html',
    'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L2_Amylase_pH_Core_Practical_Explore.html',
    'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L3_Amylase_Rate_And_Topic_1_Do.html',
)
ANCHOR = '<!--/n6-nav1-->'
STYLE = '<style id="rw1-timer-clear">#auto-timer{left:96px!important}</style>'


def apply(text):
    if STYLE in text:
        return text, False
    assert text.count(ANCHOR) == 1, 'expected exactly one N6 nav shell'
    assert 'id="auto-timer"' in text, 'expected the stage timer'
    return text.replace(ANCHOR, ANCHOR + STYLE, 1), True


def self_test():
    page = '<body><!--n6-nav1:v1--><a class="mbmhome" href="x">← Lessons</a><!--/n6-nav1--><div id="auto-timer"></div></body>'
    out, did = apply(page); assert did and out.index(STYLE) > out.index(ANCHOR), 'style follows the shell'
    again, did2 = apply(out); assert not did2 and again == out, 'idempotent'
    try:
        apply('<body><!--/n6-nav1--><p>no timer</p></body>'); raise AssertionError('must refuse a page without the timer')
    except AssertionError as e:
        assert 'timer' in str(e)
    print('self-test PASS: 3 controls (placement, idempotent, refuse-without-timer)')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true'); ap.add_argument('--self-test', action='store_true'); a = ap.parse_args()
    if a.self_test:
        self_test(); raise SystemExit(0)
    changed = []
    for rel in LESSONS:
        p = ROOT / rel; out, did = apply(p.read_text(encoding='utf-8'))
        print(f"  {rel.split('/')[-1][:46]:<46} {'rule inserted' if did else 'already present'}")
        if did:
            changed.append(rel)
            if not a.check: p.write_text(out, encoding='utf-8')
    print(f"{len(changed)} file(s) {'would change' if a.check else 'changed'}")
    raise SystemExit(1 if (a.check and changed) else 0)
