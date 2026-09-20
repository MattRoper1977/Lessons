#!/usr/bin/env python3
"""ORDER HUM-T landing — admit one batch of transplanted decks.

The standalone/offline fence admits a changed deck only when the deck is named in
REVIEWED_PATHS, exactly, in `tools/catalogue/pin_catalogue_contract.py`. A deck
cannot become permitted because it shares a directory with a permitted one — that
is the point of the fence, and this tool does not weaken it: it appends the exact
paths of the batch being landed, with the batch named beside them, and nothing else.

After this, run the pin writer and `tools/pin1/derive_triggers.py --write`, which
materialises the matching trigger path; PIN1 asserts the two sets are equal in both
directions, so an admission without a trigger (or the reverse) is red.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

MARK = '# ORDER HUM-T landing — transplanted decks, admitted per batch'


def admit(root: Path, paths, batch: str):
    f = root / 'tools/catalogue/pin_catalogue_contract.py'
    src = f.read_text()
    already = set(re.findall(r"'([^']+\.html)'", src)) | set(re.findall(r'"([^"]+\.html)"', src))
    new = [p for p in paths if p not in already]
    if not new:
        return 0
    block = ('\n%s\n# %s\nREVIEWED_PATHS += (\n' % (MARK, batch)
             + ''.join("    '%s',\n" % p for p in sorted(new)) + ')\n')
    anchor = '\n# Owner-reviewed additive Science download transaction'
    i = src.index(anchor)
    f.write_text(src[:i] + block + src[i:])
    return len(new)


if __name__ == '__main__':
    root = Path(sys.argv[1]); batch = sys.argv[2]
    paths = [l.strip() for l in sys.stdin if l.strip()]
    n = admit(root, paths, batch)
    print('admitted %d deck(s) for batch %s' % (n, batch))
