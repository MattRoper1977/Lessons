#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NAV-1 Stage A — the persistent `← Lessons` control.

One real anchor per lesson file, rendered OUTSIDE the slide container (fixed,
top-right — the §2.1 derivation: the chassis owns the bottom strip with its
fixed `.controls` bar, whose left group is `display:none` at phone widths, and
nothing is fixed at the top; the stage tag owns the slide's top-LEFT). Derived
relative path, asserted to resolve in the repo tree. RM STATIC — no animation,
no transition. Hidden under `@media print` in its own rule, independent of the
file's print dialect. Byte-region protections asserted BEFORE the write, per
file (closure, close block, witness, print pack, tiers, word bank, Oak count).

Suite indexes get the same link IN FLOW at the top of the page (they are
scrolling documents, not decks); governance banner and policy links untouched.
"""
import re, os, sys

REPO = "/home/user/Lessons"
CLOSE_BLOCK = r'<div class="close">.*?(?:<div class="pline"[^>]*></div>){2}</div>'

CSS = """
/* ===== NAV-1: way home — chrome only, teaching surfaces untouched ===== */
.mbmhome{position:fixed;top:6px;right:10px;z-index:2500;display:inline-flex;align-items:center;justify-content:center;gap:6px;min-height:44px;min-width:44px;padding:8px 14px;background:#161D3D;color:#FFF6E8;border-radius:999px;font-weight:800;font-size:.85rem;letter-spacing:.03em;text-decoration:none;box-shadow:0 2px 10px rgba(15,23,42,.3)}
.mbmhome:hover{background:#232C55}
.mbmhome:focus-visible{outline:3px solid #E08A2E;outline-offset:2px}
@media print{.mbmhome{display:none!important}}
"""

def anchor(rel):
    return ('<a class="mbmhome" href="%s" '
            'aria-label="Back to the Lessons catalogue">← Lessons</a>' % rel)


def rel_to_hub(path):
    depth = len(os.path.relpath(path, REPO).split(os.sep)) - 1
    rel = "../" * depth + "index.html"
    target = os.path.normpath(os.path.join(os.path.dirname(path), rel))
    assert os.path.isfile(target) and target == os.path.join(REPO, "index.html"), \
        "derived path does not resolve to the hub: " + rel
    return rel


def guards(s):
    return dict(
        closure=len(re.findall(r'What I said, and what it changed', s)),
        close=(re.search(CLOSE_BLOCK, s, re.S) or [None]) and
              (re.search(CLOSE_BLOCK, s, re.S).group(0) if re.search(CLOSE_BLOCK, s, re.S) else None),
        witness=(re.search(r'<div id="print-witness".*?(?=</div>\s*</div>\s*<script|$)', s, re.S).group(0)
                 if re.search(r'<div id="print-witness"', s) else None),
        printpack=(re.search(r'<div class="printpack">.*?(?=<script)', s, re.S).group(0)
                   if '<div class="printpack">' in s else None),
        tiers=tuple(len(re.findall(t, s)) for t in ("Supported", "Standard", "Stretch")),
        wordbank=len(re.findall(r'(?i)word[ -]?bank', s)),
        oak=len(re.findall(r'thenational\.academy', s)),
    )


def apply_lesson(path):
    s = open(path, encoding="utf-8").read()
    assert "mbmhome" not in s, "button already present: " + path
    g = guards(s)
    rel = rel_to_hub(path)
    i = s.find("<body>")
    assert i >= 0, "no <body> in " + path
    s = s[:i + len("<body>")] + "\n" + anchor(rel) + "\n" + s[i + len("<body>"):]
    s = s.replace("</style>", CSS + "</style>", 1)
    g2 = guards(s)
    assert g == g2, "protected byte-regions changed: " + path
    assert not re.search(r'matchMedia|localStorage|sessionStorage|fetch\(|<form|XMLHttpRequest',
                         anchor(rel) + CSS), "prohibited API in the insert"
    open(path, "w", encoding="utf-8").write(s)
    return rel


def apply_index(path):
    s = open(path, encoding="utf-8").read()
    assert "mbmhome" not in s, "link already present: " + path
    rel = rel_to_hub(path)
    css = CSS.replace("position:fixed;top:6px;right:10px;z-index:2500",
                      "position:static;margin:10px 0 0 10px")
    i = s.find("<body>")
    assert i >= 0, "no <body> in " + path
    s = s[:i + len("<body>")] + "\n" + anchor(rel) + "\n" + s[i + len("<body>"):]
    s = s.replace("</style>", css + "</style>", 1)
    open(path, "w", encoding="utf-8").write(s)
    return rel


if __name__ == "__main__":
    for p in sys.argv[1:]:
        full = p if os.path.isabs(p) else os.path.join(REPO, p)
        fn = apply_index if full.endswith("index.html") else apply_lesson
        print("mbmhome + %s -> %s" % (fn(full), os.path.relpath(full, REPO)))
