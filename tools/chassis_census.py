#!/usr/bin/env python3
"""D-1 — which shell is each taught lesson mounted on, measured by DOM query.

    chassis_census.py --write | --check | --self-test [--root .]

THREE shells are in service across the Science estate and they are not interchangeable.
Counting them is the point: an impression that "most lessons look right" is not a number.

  classroom  the shell the accepted lessons use, and the one Matt asked for: an XP meter,
             the auto timer, the slide container, the controls, the progress bar and the
             lesson-complete overlay. Identified by BOTH #xpWrap and #lc-overlay.
  classic    the toolbar shell: a home control, the auto timer, div.classic-toolbar, the
             deck as <main class="slide-container">, .classic-progress and p.classic-status.
             Identified by div.classic-toolbar, or by .classic-progress with p.classic-status.
  review     the review deck: a home control, a skip link, the deck as <main id="lessonDeck">,
             nav controls and a word-help control. Identified by main#lessonDeck or
             nav.review-top. This is the shell Matt reported the Sugar lesson on.
  v3-deck    the earlier forty-minute deck under Build/v3_40min and its siblings: a home
             control, <main class="deck"> with no id, a TA overlay and a loop overlay, a
             media aside and a print pack. Identified by #taOverlay or #loopOverlay or
             .printpack.

Classification is a DOM query, never a substring search: the n6-splash guard lesson in
CLAUDE.md is that a substring match on generated markup proves nothing about the rendered
page. Every marker below is an element identity or an attribute, resolved by lxml.

Two separate verdicts, because they answer different questions and fail for different reasons:

  --check  is the record fresh? Fails when data/chassis-census.json differs from the working
           tree. Safe to run in CI from the moment the record is committed.
  --gate   are the DECLARED lessons on the classroom shell? The declared set is the accepted
           EDU-Q1 identities and nothing else: this gate is not a sweep of the estate and it
           rules on no lesson Matt has not ruled on. It is red until D-1 lands, so it is
           wired into CI by the pull request that fixes the lesson, not by this one.

Every lesson is reported in the record either way, so the size of the remainder is a measured
number rather than an impression.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from lxml import html

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / 'data/chassis-census.json'

DECLARED = {
    'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html': 'BUILD',
    'Science_Teesside/Grow/SCI_G_W3_Friction.html': 'GROW',
    'Science_Teesside/Launch/SCI_L_W4_L1_Diffusion.html': 'LAUNCH',
}


def classify(raw: bytes):
    doc = html.fromstring(raw)
    marks = {
        'xpWrap': len(doc.xpath('//*[@id="xpWrap"]')),
        'lessonCompleteOverlay': len(doc.xpath('//*[@id="lc-overlay"]')),
        'autoTimer': len(doc.xpath('//*[@id="auto-timer"]')),
        'slideContainer': len(doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," slide-container ")]')),
        'reviewTopNav': len(doc.xpath('//nav[contains(concat(" ",normalize-space(@class)," ")," review-top ")]')),
        'lessonDeckMain': len(doc.xpath('//main[@id="lessonDeck"]')),
        'classicProgress': len(doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," classic-progress ")]')),
        'classicToolbar': len(doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," classic-toolbar ")]')),
        'classicStatus': len(doc.xpath('//p[contains(concat(" ",normalize-space(@class)," ")," classic-status ")]')),
        'wordHelp': len(doc.xpath('//*[@id="wordHelp"]')),
        'homeControl': len(doc.xpath('//a[contains(concat(" ",normalize-space(@class)," ")," mbmhome ")]')),
        'taOverlay': len(doc.xpath('//*[@id="taOverlay"]')),
        'loopOverlay': len(doc.xpath('//*[@id="loopOverlay"]')),
        'printPack': len(doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," printpack ")]')),
    }
    if marks['xpWrap'] and marks['lessonCompleteOverlay']:
        return 'classroom', marks
    if marks['classicToolbar'] or (marks['classicProgress'] and marks['classicStatus']):
        return 'classic', marks
    if marks['lessonDeckMain'] or marks['reviewTopNav']:
        return 'review', marks
    if marks['taOverlay'] or marks['loopOverlay'] or marks['printPack']:
        return 'v3-deck', marks
    return 'other', marks


def census(root: Path) -> dict:
    rows = {}
    for path in sorted((root / 'Science_Teesside').rglob('SCI_*.html')):
        rel = path.relative_to(root).as_posix()
        shell, marks = classify(path.read_bytes())
        rows[rel] = {'shell': shell, 'markers': marks,
                     'pathway': 'BUILD' if '/Build/' in rel else 'GROW' if '/Grow/' in rel else 'LAUNCH' if '/Launch/' in rel else 'OTHER',
                     'declared': rel in DECLARED}
    counts = {}
    by_pathway = {}
    for r in rows.values():
        counts[r['shell']] = counts.get(r['shell'], 0) + 1
        by_pathway.setdefault(r['pathway'], {}).setdefault(r['shell'], 0)
        by_pathway[r['pathway']][r['shell']] += 1
    return {'schema': 1,
            'basis': 'Shell identified by DOM query on the committed bytes, never by substring. '
                     'Declared lessons are the accepted EDU-Q1 identities and must be on the classroom shell.',
            'counts': counts, 'byPathway': by_pathway, 'lessons': rows}


def declared_errors(data: dict):
    out = []
    for rel, pathway in sorted(DECLARED.items()):
        row = data['lessons'].get(rel)
        if row is None:
            out.append('declared lesson missing from the checkout: ' + rel)
        elif row['shell'] != 'classroom':
            out.append('declared ' + pathway + ' lesson is on the ' + row['shell'] + ' shell, not the classroom shell: ' + rel)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', type=Path, default=ROOT)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true', help='record freshness only')
    ap.add_argument('--gate', action='store_true', help='declared lessons must be on the classroom shell')
    ap.add_argument('--self-test', action='store_true')
    a = ap.parse_args()

    if a.self_test:
        classroom = b'<html><body><div id="xpWrap"></div><div id="lc-overlay"></div><div class="slide-container"></div></body></html>'
        review = b'<html><body><nav class="review-top"></nav><main id="lessonDeck"></main></body></html>'
        v3 = b'<html><body><a class="mbmhome"></a><main class="deck"></main><div class="overlay" id="taOverlay"></div><div class="printpack"></div></body></html>'
        classic = b'<html><body><div class="classic-toolbar"></div><main class="slide-container"></main><div class="progress-wrap classic-progress"></div><p class="classic-status"></p></body></html>'
        checks = [
            ('a classroom shell is recognised', classify(classroom)[0] == 'classroom'),
            ('a review shell is recognised', classify(review)[0] == 'review'),
            ('a classic shell is recognised', classify(classic)[0] == 'classic'),
            ('a v3 deck is recognised', classify(v3)[0] == 'v3-deck'),
            ('CONTROL: the four shells are told apart, not merged',
             len({classify(classroom)[0], classify(review)[0], classify(classic)[0], classify(v3)[0]}) == 4),
            ('CONTROL: removing the XP meter stops it counting as classroom',
             classify(classroom.replace(b'<div id="xpWrap"></div>', b''))[0] != 'classroom'),
            ('CONTROL: removing the completion overlay stops it counting as classroom',
             classify(classroom.replace(b'<div id="lc-overlay"></div>', b''))[0] != 'classroom'),
            ('CONTROL: a review shell given both markers flips to classroom',
             classify(review.replace(b'<main id="lessonDeck"></main>',
                                   b'<div id="xpWrap"></div><div id="lc-overlay"></div>'))[0] == 'classroom'),
            ('CONTROL: the declared gate fires when a declared lesson is on the review shell',
             bool(declared_errors({'lessons': {rel: {'shell': 'review'} for rel in DECLARED}}))),
            ('CONTROL: the declared gate is silent when every declared lesson is classroom',
             not declared_errors({'lessons': {rel: {'shell': 'classroom'} for rel in DECLARED}})),
        ]
        for name, ok in checks:
            print(('GREEN ' if ok else 'RED   ') + name)
        return 0 if all(ok for _, ok in checks) else 1

    data = census(a.root)
    if a.write:
        RECORD.parent.mkdir(parents=True, exist_ok=True)
        RECORD.write_text(json.dumps(data, indent=2) + '\n')
        print('[DONE] wrote data/chassis-census.json: ' + ', '.join(str(v) + ' ' + k for k, v in sorted(data['counts'].items())))

    stale = False
    if a.check:
        if not RECORD.is_file():
            print('[FAIL] data/chassis-census.json is missing — run --write')
            return 1
        committed = json.loads(RECORD.read_text())
        if committed.get('lessons') != data['lessons']:
            drift = [k for k in sorted(set(committed.get('lessons', {})) | set(data['lessons']))
                     if committed.get('lessons', {}).get(k) != data['lessons'].get(k)]
            print('[FAIL] data/chassis-census.json differs from the working tree — run --write. Rows: ' + ', '.join(drift[:5]))
            stale = True
        else:
            print('[PASS] data/chassis-census.json equals its derivation: ' + str(len(data['lessons'])) + ' lessons')

    problems = declared_errors(data)
    for p in problems:
        print('RED  ' + p)
    print(str(len(DECLARED) - len(problems)) + '/' + str(len(DECLARED)) + ' declared lessons on the classroom shell; '
          + ', '.join(str(v) + ' ' + k for k, v in sorted(data['counts'].items())))
    if stale:
        return 1
    return 1 if (a.gate and problems) else 0


if __name__ == '__main__':
    raise SystemExit(main())
