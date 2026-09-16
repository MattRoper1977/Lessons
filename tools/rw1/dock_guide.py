#!/usr/bin/env python3
"""CX2 §8.3 · dock the staff-guidance button in the six return-week lessons.

    python3 tools/rw1/dock_guide.py [--check] [--self-test]

Every Science lesson carries the same N6M guidance shell (<!--n6m-guide:v1-->; the
block is byte-identical between the return-week builds and the lessons on main). Its
boot() creates the "Guidance" button and docks it into `.controls .left` when that host
exists — `if(host) b.classList.add("n6m-guide-docked")`, and the shell's own CSS then
makes it `position:static` inside the bar. Without a host it falls back to
document.body as a fixed button at the bottom-right corner.

The return-week chassis has a `.controls` bar (Previous · TA Brief · Question · Next) with
no `.left` group, so the button floats — and, measured in Chromium at 1280 and 390, it
sits exactly over Next: `document.elementFromPoint` at Next's centre returns the guide
button. That is the defect the offline-pack check names ("Guidance must not obstruct
Next") and the reason it reported these lessons red. This inserts `<div class="left">`
as the first child of the bar so the shell docks the button where the estate's canon
puts it. No script changes, no new control, no text moves.
"""
from pathlib import Path
import argparse, re, sys

ROOT = Path(__file__).resolve().parents[2]
LESSONS = (
    'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8B_Autumn_Science_Checkpoint_Do.html',
    'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8A_Day_And_Night_Explore.html',
    'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8B_Day_And_Night_Do.html',
    'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L1_Enzyme_Action_Introduce.html',
    'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L2_Amylase_pH_Core_Practical_Explore.html',
    'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L3_Amylase_Rate_And_Topic_1_Do.html',
)
BAR = re.compile(r'<div class="controls">(?!\s*<div class="left">)')
HOST = '<div class="controls"><div class="left"></div>'


def apply(text):
    assert text.count('<div class="controls">') == 1, 'expected exactly one controls bar'
    assert 'n6m-guide:v1' in text, 'the N6M guidance shell must be present'
    out, n = BAR.subn(HOST, text, count=1)
    return out, n == 1


def self_test():
    page = '<html><body><!--n6m-guide:v1--><div class="controls"><button id="next-slide">Next</button></div></body></html>'
    out, changed = apply(page)
    assert changed and '<div class="controls"><div class="left"></div><button id="next-slide">' in out, 'host inserted first'
    again, changed2 = apply(out); assert not changed2 and again == out, 'idempotent'
    try:
        apply('<html><body><div class="controls"></div></body></html>'); raise AssertionError('must refuse a page without the shell')
    except AssertionError as e:
        assert 'shell' in str(e)
    print('self-test PASS: 3 controls (insert-first, idempotent, refuse-without-shell)')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true'); ap.add_argument('--self-test', action='store_true'); a = ap.parse_args()
    if a.self_test:
        self_test(); raise SystemExit(0)
    changed = []
    for rel in LESSONS:
        p = ROOT / rel; before = p.read_text(encoding='utf-8'); out, did = apply(before)
        print(f"  {rel.split('/')[-1][:46]:<46} {'host inserted' if did else 'already docked'}")
        if did:
            changed.append(rel)
            if not a.check: p.write_text(out, encoding='utf-8')
    print(f"{len(changed)} file(s) {'would change' if a.check else 'changed'}")
    raise SystemExit(1 if (a.check and changed) else 0)
