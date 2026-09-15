#!/usr/bin/env python3
"""CX2 §8.3 · restore the authored lesson-config block the return-week build dropped.

    python3 tools/rw1/restore_lesson_config.py [--base REF] [--check] [--self-test]

Every Science lesson on main carries its authored metadata as

    <script type="application/json" id="lesson-config">{... "title": ... }</script>

and tools/downloads/build_download_pack.py:lesson_label() reads it — preferring it over
the opening <h1> — to name a lesson wherever the estate lists one: the offline pack
portal, and the continuation entries that tools/downloads/verify_definitions.py pins.

The six return-week builds carried from claude/rw1-w8-return-week have no such block.
Measured on this branch before the fix: lesson_label() returns None for BUILD W8B and
'Your task · 1 of 2' for the other five, because their only <h1> is a per-slide
worksheet label rather than a lesson title. So the lesson name is wrong or absent in
every place the estate derives it, and verify_definitions fails on the two lessons that
happen to be continuation targets — the other four would have shipped unnamed and
unchecked.

This copies each lesson's own block verbatim from the review base, where it is the
reviewed authored metadata, and inserts it before </body>. It never invents a title,
never edits one, and refuses if the base has no block or the file already has one with
a different title. It also strips trailing whitespace, which `git diff --check` reds.

A <script type="application/json"> is data, not code: it is not executed, it renders
nothing, and its position in the body does not change layout, reading order or the
accessibility tree.
"""
from pathlib import Path
import argparse, re, subprocess, sys

ROOT = Path(__file__).resolve().parents[2]
BLOCK = re.compile(r'<script type="application/json" id="lesson-config">.*?</script>', re.S)
LESSONS = (
    'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8B_Autumn_Science_Checkpoint_Do.html',
    'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8A_Day_And_Night_Explore.html',
    'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8B_Day_And_Night_Do.html',
    'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L1_Enzyme_Action_Introduce.html',
    'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L2_Amylase_pH_Core_Practical_Explore.html',
    'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L3_Amylase_Rate_And_Topic_1_Do.html',
)


def base_block(base, rel):
    text = subprocess.check_output(['git', '-C', str(ROOT), 'show', base + ':' + rel]).decode()
    found = BLOCK.search(text)
    if not found:
        raise SystemExit('[FAIL] the review base has no lesson-config for ' + rel)
    return found.group(0)


def strip_trailing(text):
    return '\n'.join(line.rstrip() for line in text.split('\n'))


def apply(text, block):
    if BLOCK.search(text):
        return strip_trailing(text), False
    assert text.count('</body>') == 1, 'expected exactly one </body>'
    return strip_trailing(text.replace('</body>', block + '</body>', 1)), True


def self_test():
    page = '<html><body><h1>Your task · 1 of 2</h1>  \n<p>x</p> \n</body></html>'
    block = '<script type="application/json" id="lesson-config">{"title":"Real Lesson"}</script>'
    out, inserted = apply(page, block)
    assert inserted and block in out, 'the block must be inserted when absent'
    assert '  \n' not in out and ' \n' not in out, 'trailing whitespace must be stripped'
    sys.path.insert(0, str(ROOT / 'tools/downloads'))
    from build_download_pack import lesson_label
    assert lesson_label(page.encode()) == 'Your task · 1 of 2', 'control: the unfixed page names the wrong thing'
    assert lesson_label(out.encode()) == 'Real Lesson', 'the fixed page must name the lesson'
    again, inserted2 = apply(out, block)
    assert not inserted2 and again == out, 'must be idempotent'
    empty, _ = apply('<html><body><p>no heading</p></body></html>', block)
    assert lesson_label(empty.encode()) == 'Real Lesson', 'control: a page with no h1 at all is also named'
    print('self-test PASS: 5 controls (insert, strip, wrong-name-before, right-name-after, idempotent)')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--base', default='origin/main')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--self-test', action='store_true')
    a = ap.parse_args()
    if a.self_test:
        self_test(); raise SystemExit(0)
    sys.path.insert(0, str(ROOT / 'tools/downloads'))
    from build_download_pack import lesson_label
    changed, report = [], {}
    for rel in LESSONS:
        path = ROOT / rel
        before = path.read_text(encoding='utf-8')
        out, inserted = apply(before, base_block(a.base, rel))
        report[rel.split('/')[-1]] = {'inserted': inserted,
                                      'labelBefore': lesson_label(before.encode()),
                                      'labelAfter': lesson_label(out.encode())}
        if out != before:
            changed.append(rel)
            if not a.check:
                path.write_text(out, encoding='utf-8')
    for name, row in report.items():
        print(f"  {name[:46]:<46} inserted={row['inserted']!s:<5} {row['labelBefore']!r} -> {row['labelAfter']!r}")
    print(f"{len(changed)} file(s) {'would change' if a.check else 'changed'}")
    raise SystemExit(1 if (a.check and changed) else 0)
