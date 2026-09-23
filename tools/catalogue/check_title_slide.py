#!/usr/bin/env python3
"""Red proof for the title-slide rule (RULING 2026-09-23 B.2).

    tools/catalogue/check_title_slide.py --self-test

Every control below is a RED PROOF: it plants the fault and demands the rule refuse it.
A control that can only ever pass is not a control.

The W8A proofs read the deck's REAL SERVED BYTES from the repo, not a fixture, so the
proof cannot drift away from what the hub actually lists.
"""
from __future__ import annotations
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from title_slide import title_slide_heading, first_document_h1

ROOT = Path(__file__).resolve().parents[2]
W8A = ROOT / 'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8A_Day_And_Night_Explore.html'

# The five W8 exemplars whose listed title read "Your task * 1 of 2" on main before this fix.
EXEMPLARS = [
    'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8A_Day_And_Night_Explore.html',
    'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8B_Day_And_Night_Do.html',
    'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L1_Enzyme_Action_Introduce.html',
    'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L2_Amylase_pH_Core_Practical_Explore.html',
    'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L3_Amylase_Rate_And_Topic_1_Do.html',
]

DECK = ('<!doctype html><html lang="en-GB"><head><title>Doc title</title></head><body>'
        '<section class="slide" id="slide-1" data-timer="0" data-title="Declared title">'
        '{opener}</section>'
        '<section class="slide" id="slide-2" data-timer="10"><h1>Your task &#183; 1 of 2</h1></section>'
        '<section class="slide" id="slide-9" data-timer="0"><h2>Next useful step</h2></section>'
        '</body></html>')

ok = True


def check(name: str, condition: bool) -> None:
    global ok
    ok = ok and bool(condition)
    print(f"  [{'ok' if condition else 'FAIL'}] {name}")


def self_test() -> int:
    print('title-slide rule, red proofs')

    # --- the defect itself, on the real deck the ruling names ---
    text = W8A.read_text(encoding='utf-8', errors='replace')
    check('(1) W8A: the OLD rule returns the task slide\'s heading, which is the defect',
          first_document_h1(text) == 'Your task · 1 of 2')
    check('(2) W8A: the NEW rule returns the title slide\'s own heading',
          title_slide_heading(text) == 'Day and Night: Sky Shift')
    check('(3) W8A: the two rules DISAGREE, so the proof is not vacuous',
          first_document_h1(text) != title_slide_heading(text))

    # --- the whole reported population, by measurement not assertion ---
    wrong = [p for p in EXEMPLARS
             if first_document_h1((ROOT / p).read_text(encoding='utf-8', errors='replace'))
             == 'Your task · 1 of 2']
    check(f'(4) all five W8 exemplars carried the defect under the old rule ({len(wrong)}/5)',
          len(wrong) == 5)
    fixed = [p for p in EXEMPLARS
             if title_slide_heading((ROOT / p).read_text(encoding='utf-8', errors='replace'))
             not in (None, '', 'Your task · 1 of 2')]
    check(f'(5) and none of the five does under the new rule ({len(fixed)}/5)', len(fixed) == 5)

    # --- the 77-title trap: keying on the NAME instead of POSITION 0 ---
    # A deck whose opener is TIMED has its only untimed slide at the exit, so deck_dom's
    # stage_name() calls the EXIT 'title'. Planted here so the trap cannot come back.
    sys.path.insert(0, str(ROOT / 'tools/hum'))
    import deck_dom as D
    timed_opener = DECK.format(opener='<h2>Real title</h2>').replace(
        '<section class="slide" id="slide-1" data-timer="0"', '<section class="slide" id="slide-1" data-timer="5"')
    named = [s for s in D.stages(D.parse(timed_opener)) if D.stage_name(s) == 'title']
    check('(6) the trap is real: on a timed opener, stage_name() calls a LATER slide "title"',
          bool(named) and named[0] is not D.stages(D.parse(timed_opener))[0])
    check('(7) the rule keys on position 0, so the trap does not reach the title',
          title_slide_heading(timed_opener) == 'Real title')

    # --- ordinary shape proofs ---
    check('(8) an <h1> title slide is read',
          title_slide_heading(DECK.format(opener='<h1>Heading one</h1>')) == 'Heading one')
    check('(9) an <h2> title slide is read -- level is not fixed',
          title_slide_heading(DECK.format(opener='<h2>Heading two</h2>')) == 'Heading two')
    check('(10) a title slide that renders NO heading falls back to its own data-title',
          title_slide_heading(DECK.format(opener='<p>no heading here</p>')) == 'Declared title')
    check('(11) a page with no slides returns None, so off-deck pages keep the old rule',
          title_slide_heading('<!doctype html><html><body><h1>Hub</h1></body></html>') is None)
    check('(12) the task slide\'s heading is never returned when the title slide has one',
          title_slide_heading(DECK.format(opener='<h2>Heading two</h2>')) != 'Your task · 1 of 2')

    # --- HUB1 R3: a stage label is not a title ---
    labelled = ('<!doctype html><html><head><title>Body Science Checkpoint \u00b7 BUILD \u00b7 October review</title></head><body>'
                '<section class="slide" id="slide-1" data-timer="0"><h2>Lesson overview</h2><h3>Learning objective</h3>'
                '<h3>Success looks like</h3></section><section class="slide" id="slide-2" data-timer="5"><h2>Your task</h2></section></body></html>')
    check('(13) R3 RED PROOF: a title slide that opens on the label "Lesson overview" is not listed as "Lesson overview"',
          title_slide_heading(labelled) != 'Lesson overview')
    check('(14) R3: with only labels on the title slide, the deck\'s own head <title> names it',
          title_slide_heading(labelled) == 'Body Science Checkpoint')
    check('(15) R3: a real heading after a label still wins over the head <title>',
          title_slide_heading(labelled.replace('<h3>Learning objective</h3>', '<h2>Real deck title</h2>', 1)) == 'Real deck title')
    w8b = ROOT / 'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8B_Autumn_Science_Checkpoint_Do.html'
    if w8b.is_file():
        check('(16) R3 on the real deck: SCI_B_W8B lists "Body Science Checkpoint"',
              title_slide_heading(w8b.read_text(encoding='utf-8', errors='replace')) == 'Body Science Checkpoint')

    print('self-test', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(self_test() if '--self-test' in sys.argv else
                     print('usage: check_title_slide.py --self-test') or 2)
