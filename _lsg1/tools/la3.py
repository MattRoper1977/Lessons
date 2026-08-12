#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LSG-1 A3 — sentence-level prose graft on the LIVE LAUNCH lessons.

A3 is DELIBERATELY SMALL on LAUNCH, and that is the finding, not a shortfall:

  * The heaviest pupil-facing sentence in the suite - "If local policy uses R, it
    follows genuine Audience only; this page never adds it automatically."
    (16 words, FK 12.0, on 15/15) - sits INSIDE the protected close block. It is
    RED to alter. Named, not touched.
  * Most of the remaining heavy sentences are Stretch-tier questions whose
    difficulty comes from protected GCSE vocabulary that must survive verbatim.
    Those were simplified at source in lcontent.py by fronting the proposition
    and then asking for the explanation - same demand, shorter carriers.
  * The pack is a poor quarry here: its Independent prose is differently scoped
    rather than simpler for the same content, and it carries GROW friction
    content on every LAUNCH exit frame.

What is left is the small set below: live-origin sentences that say the same
thing in two short carriers instead of one long one.
"""
import re, glob, os

LIVE = "/home/user/Lessons/Science_Teesside/Launch/v3_40min"

EDITS = [
 ("LIVE", "A compare answer describes diffusion perfectly but never mentions active transport.",
          "A compare answer describes diffusion perfectly. It never mentions active transport."),
 ("LIVE", "Explain why increasing magnification does not always reveal more detail.",
          "Increasing magnification does not always reveal more detail. Explain why."),
]


def main():
    tally = {}
    for p in sorted(glob.glob(os.path.join(LIVE, "SCI_L_W*L*.html"))):
        s = open(p, encoding="utf-8").read()
        o = s
        for kind, a, b in EDITS:
            if a in s:
                tally[kind] = tally.get(kind, 0) + s.count(a)
                s = s.replace(a, b)
        if s != o:
            open(p, "w", encoding="utf-8").write(s)
            print("edited  %s" % os.path.basename(p))
    print("replacements by kind:", tally or "none")


if __name__ == "__main__":
    main()
