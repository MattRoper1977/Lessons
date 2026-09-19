#!/usr/bin/env python3
"""Re-derive the Science shelf cards' TITLE TEXT from the shelf JSON.

    sync_shelf_card_titles.py --check | --write | --self-test [--root .]

Science_Teesside/index.html is a derived file: tools/catalogue/build_science_shelf.py
writes it from assets/catalogue/science-shelf.json. That builder cannot currently run
-- it asserts on tools/catalogue/SCIENCE_WEEK_BINDINGS.json, of which 77 of 129 entries
are stale -- so the composite has been frozen while the shelf JSON moved underneath it.
A deck's title is mirrored in five places and only the deck is the source; the composite
is mirror three, and it had no control at all. This supplies the control.

SCOPE, deliberately narrow. This tool re-derives the text inside each existing card's
<h4><a> and nothing else. It does not read, write or validate a week binding. It does
not add a card, remove a card, reorder cards, or touch any attribute, href, week label,
style line or download link. Where the real builder cannot be run, this keeps the one
mirror that is visible to a teacher honest; it is not a substitute for the builder.

The rule is a pure function of (composite text, shelf rows) so the self-test can plant
cases against the same code the tree is judged by -- the same shape as
domain-split/check_education_separation.py's registry_partition().

Two refusals, both red-proved by --self-test:
  * a card whose title disagrees with its shelf row          -> FAIL
  * a card whose data-lesson-path has no shelf row           -> FAIL, and it will not
    invent a title for it
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMPOSITE = 'Science_Teesside/index.html'
SHELF = 'assets/catalogue/science-shelf.json'

# build_science_shelf.py drops the duration suffix before it writes the card.
DURATION = re.compile(r'\s*[·—]\s*40 minutes\s*$')
# One card: its path attribute, then the first <h4><a ...>TITLE</a></h4> after it.
CARD = re.compile(
    r'(?P<head>data-lesson-path="(?P<path>[^"]*)"'  # the card's identity
    r'.*?'                                          # attributes and kind line, untouched
    r'<h4><a href="[^"]*">)'                        # the title link's opening tag
    r'(?P<title>[^<]*)'                             # the title text -- the ONLY rewrite
    r'(?P<tail></a></h4>)',
    re.S)


def expected_title(row: dict) -> str:
    """The exact bytes build_science_shelf.py would place in the card."""
    return html.escape(DURATION.sub('', row['title']))


def card_title_errors(text: str, rows: list[dict]):
    """Pure rule, so the self-test can plant cards and rows against it.

    Returns (errors, replacements, cards_seen). A replacement is
    (path, current_title, derived_title) for a card that disagrees with its row."""
    by_path = {r['path']: r for r in rows}
    errors: list[str] = []
    replacements: list[tuple[str, str, str]] = []
    seen: list[str] = []
    for m in CARD.finditer(text):
        path = html.unescape(m.group('path'))
        seen.append(path)
        row = by_path.get(path)
        if row is None:
            errors.append('Card has no shelf row, refusing to invent a title: ' + path)
            continue
        want, have = expected_title(row), m.group('title')
        if want != have:
            replacements.append((path, have, want))
    missing = [p for p in by_path if p not in seen]
    for path in sorted(missing):
        errors.append('Shelf row has no card; only build_science_shelf.py can add one: ' + path)
    return errors, replacements, seen


def apply(text: str, rows: list[dict]) -> str:
    """Rewrite only the title text of cards that disagree with their row."""
    by_path = {r['path']: r for r in rows}

    def swap(m: re.Match) -> str:
        row = by_path.get(html.unescape(m.group('path')))
        if row is None:
            return m.group(0)
        return m.group('head') + expected_title(row) + m.group('tail')

    return CARD.sub(swap, text)


def run(root: Path, write: bool) -> int:
    composite, shelf = root / COMPOSITE, root / SHELF
    rows = json.loads(shelf.read_text())['lessons']
    text = composite.read_text()
    errors, replacements, seen = card_title_errors(text, rows)
    print(f'SEARCH SCOPE: {composite} ({len(text)} bytes, {len(seen)} cards) '
          f'against {shelf} ({len(rows)} lesson rows)')
    for e in errors:
        print('  [FAIL] ' + e)
    for path, have, want in replacements:
        print(f'  [{"SYNC" if write else "STALE"}] {path}\n      card : {have}\n      shelf: {want}')
    if errors:
        print(f'[FAIL] {len(errors)} card/row mismatch(es); nothing written')
        return 1
    if write:
        if replacements:
            out = apply(text, rows)
            after_errors, after_replacements, _ = card_title_errors(out, rows)
            assert not after_errors and not after_replacements, 'rewrite did not settle'
            assert len(out.splitlines()) == len(text.splitlines()), 'line count changed'
            composite.write_text(out)
        print(f'[DONE] {len(replacements)} card title(s) re-derived from the shelf')
        return 0
    if replacements:
        print(f'[FAIL] {len(replacements)} card title(s) do not match the shelf; '
              'run tools/catalogue/sync_shelf_card_titles.py --write')
        return 1
    print(f'[PASS] all {len(seen)} card titles equal their shelf row')
    return 0


def self_test() -> int:
    """Red proofs. A control that cannot fail is not a control."""
    def card(path: str, title: str) -> str:
        return (f'<article class="card t-BUILD" data-lesson-path="{html.escape(path)}" '
                f'data-term="Aut1"><p class="kind">BUILD · Science</p>'
                f'<h4><a href="x.html">{title}</a></h4><p class="science-week">W1</p></article>')

    rows = [{'path': 'A.html', 'title': 'Alpha · 40 minutes'},
            {'path': 'B.html', 'title': 'Beta & Gamma'}]
    ok = 0

    def check(name: str, condition: bool) -> None:
        nonlocal ok
        print(f'  [{"ok" if condition else "FAIL"}] {name}')
        ok += 0 if condition else 1

    clean = card('A.html', 'Alpha') + card('B.html', 'Beta &amp; Gamma')
    e, r, seen = card_title_errors(clean, rows)
    check('a matching tree reports no error and no replacement', not e and not r and len(seen) == 2)

    stale = card('A.html', 'Alpha') + card('B.html', 'Beta and Gamma')
    e, r, _ = card_title_errors(stale, rows)
    check('(i) one planted stale title is caught', not e and [x[0] for x in r] == ['B.html'])
    check('(i) --write settles it, and settles idempotently',
          not any(card_title_errors(apply(stale, rows), rows)[:2]))

    orphan = clean + card('GHOST.html', 'Invented')
    e, r, _ = card_title_errors(orphan, rows)
    check('(ii) a card with no shelf row FAILS', len(e) == 1 and 'refusing to invent' in e[0])
    check('(ii) and its title is left exactly as found',
          '<h4><a href="x.html">Invented</a></h4>' in apply(orphan, rows))

    e, _, _ = card_title_errors(clean, rows + [{'path': 'C.html', 'title': 'Gamma'}])
    check('a shelf row with no card FAILS', len(e) == 1 and 'has no card' in e[0])

    check('the duration suffix is dropped exactly as the builder drops it',
          expected_title({'title': 'Alpha · 40 minutes'}) == 'Alpha'
          and expected_title({'title': 'Alpha — 40 minutes'}) == 'Alpha'
          and expected_title({'title': 'Alpha 40 minutes of work'}) == 'Alpha 40 minutes of work')
    check('a title is escaped, so markup in a shelf row cannot reach the page',
          expected_title({'title': '<b>x</b>'}) == '&lt;b&gt;x&lt;/b&gt;')
    check('nothing outside the title text is rewritten',
          apply(stale, rows).replace('Beta &amp; Gamma', 'Beta and Gamma') == stale)
    check('the closing </a></h4> survives a rewrite',
          apply(stale, rows).count('</a></h4>') == stale.count('</a></h4>') == 2)

    print('self-test ' + ('PASS' if not ok else f'FAIL ({ok})'))
    return 1 if ok else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=ROOT)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--self-test', action='store_true')
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    return run(args.root, write=args.write)


if __name__ == '__main__':
    sys.exit(main())
