#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LSG-1 A4 — restore the Matt-verified Oak osmosis clip into live W5L2.

The URL is READ FROM the v5 original at run time and asserted byte-equal. It is
never retyped in this file and never re-searched: the v5 original is the only
authority, and verification authority is not delegated.
"""
import re, os

REPO = "/home/user/Lessons"
V5 = os.path.join(REPO, "Science_Teesside/Launch/SCI_L_W5_L2_OsmosisCP.html")
V3 = os.path.join(REPO, "Science_Teesside/Launch/v3_40min/"
                        "SCI_L_W5L2_Osmosis_Core_Practical_Explore.html")

CSS = """
/* ===== LSG-1 A4: restored Oak clip (screen only, never printed) ===== */
.lclip{border:2px solid #7A5C9E;border-left:8px solid #7A5C9E;border-radius:12px;padding:10px 14px;margin:10px 0;background:#7A5C9E12}
.lclip a{color:#4b3b6b;font-weight:800}
.lclip .lclip-note{display:block;font-size:.85rem;color:#555;margin-top:3px}
@media print{.lclip{display:none!important}}
"""


def main():
    v5 = open(V5, encoding="utf-8").read()
    urls = re.findall(r'https://www\.thenational\.academy[^"]*', v5)
    assert len(urls) == 1, "expected exactly one clip URL in the v5 original, got %d" % len(urls)
    url = urls[0]

    s = open(V3, encoding="utf-8").read()
    if url in s:
        print("A4 already installed"); return
    block = ('<div class="lclip"><strong>📺 Optional clip — Oak National Academy · ad-free · '
             'Foundation Edexcel:</strong> <a href="' + url + '" target="_blank" '
             'rel="noopener noreferrer">Osmosis &amp; sugar concentration on plant tissue — '
             'required practical</a><span class="lclip-note">Watch the practical set-up '
             'before you run it · needs internet · captions on · <b>this lesson teaches '
             'fully without it</b>. Not part of the printed pack.</span></div>')
    m = re.search(r'(<section class="slide"[^>]*data-type="ido".*?</section>)', s, re.S)
    blk = m.group(1)
    anchor = '<div class="lmodel">'
    assert anchor in blk, "model-limit anchor missing — run lgraft.py first"
    s = s.replace(blk, blk.replace(anchor, block + anchor, 1), 1)
    s = s.replace("</style>", CSS + "</style>", 1)

    assert s.count(url) == 1
    pp = re.search(r'<div class="printpack">.*?(?=<script)', s, re.S).group(0)
    assert "thenational.academy" not in pp, "clip leaked into the print pack"
    open(V3, "w", encoding="utf-8").write(s)
    print("A4 installed · URL byte-equal to the v5 original · 1 occurrence · absent from print")


if __name__ == "__main__":
    main()
