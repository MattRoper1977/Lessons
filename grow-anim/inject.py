#!/usr/bin/env python3
"""Inline the GROW Animation Framework into single-file lesson HTML.

Classroom laptops open lessons straight from a file or a USB stick, and the
Teesside rooms cannot be relied on for network, so every lesson has to stay a
single self-contained file. This keeps that true without copy-paste drift: the
canonical library lives in grow-anim/, and this script pushes it into every
lesson.

    python3 grow-anim/inject.py Science_Teesside/Grow/*.html
    python3 grow-anim/inject.py --check Science_Teesside/Grow/*.html
    python3 grow-anim/inject.py --no-polish Science_Teesside/Grow/*.html

The first run on a lesson INSTALLS the marker blocks (CSS before </head>, JS
before </body>). Every run after that just refreshes what is between the
markers, so a fix made once in grow-anim/ reaches every lesson.

--check writes nothing and exits 1 if any lesson is out of date, so it can run
in a pre-commit hook or a build step.
"""

import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))

CSS_BLOCKS = [
    ("MOTION", "grow-motion.css"),   # Phase 1 — the motion language
    ("COMP",   "grow-anim.css"),     # Phases 3-11 — component furniture
    ("POLISH", "grow-polish.css"),   # Phase 12 — optional
]
JS_BLOCKS = [
    ("SVG",    "grow-svg.js"),       # Phase 2 — registry + drawing kit
    ("BIO",    "grow-svg-bio.js"),
    ("ANIM",   "grow-svg-bio-animals.js"),
    ("PHY",    "grow-svg-phy.js"),
    ("CHEM",   "grow-svg-chem.js"),
    ("ENGINE", "grow-anim.js"),      # Phases 3-11 — the engine
    ("SHINE",  "grow-polish.js"),    # Phase 12 — optional
]
OPTIONAL = {"POLISH", "SHINE"}

BEGIN = "/* GROW-ANIM:%s:BEGIN"
END = "/* GROW-ANIM:%s:END */"


# Inlining puts a source inside a <script> or <style> element, and the HTML
# parser does not care that a token sits inside a JS comment or a string: the
# first literal "</script" it meets ends the block, and everything after it is
# parsed as markup. compat-build-anim.js documents its own usage with four
# <script src=...></script> lines; inlined raw, three of them became real script
# elements requesting files that were not there, the engine never loaded, and
# twelve slides of a lesson sat still with no error and exit 0.
#
# The escape is the standard one: a backslash before the slash. "<\/script>" is
# the same string to a JavaScript parser and is not a close tag to an HTML one.
# In CSS a "\/" is likewise inert inside a comment or a string.
ESCAPES = [("</script", "<\\/script"), ("</style", "<\\/style")]


def escape_for_inline(text):
    for token, safe in ESCAPES:
        text = text.replace(token, safe)
    return text


def read(src):
    with open(os.path.join(HERE, src), encoding="utf-8") as fh:
        return escape_for_inline(fh.read().rstrip("\n"))


def wrap(name, body):
    return "%s — generated from grow-anim/%s, do not edit here */\n%s\n%s" % (
        BEGIN % name, SOURCE_OF[name], body, END % name)


SOURCE_OF = dict(CSS_BLOCKS + JS_BLOCKS)


def splice(html, name, body):
    """Replace an existing marked block. Returns (html, found)."""
    i = html.find(BEGIN % name)
    if i < 0:
        return html, False
    j = html.find(END % name, i)
    if j < 0:
        raise SystemExit("unclosed %s marker" % name)
    return html[:i] + wrap(name, body) + html[j + len(END % name):], True


def install(html, blocks, tag, closing):
    """First-time install: build one <style>/<script> element before `closing`."""
    inner = "\n".join(wrap(name, read(src)) for name, src in blocks)
    el = '<%s id="grow-anim-%s">\n%s\n</%s>' % (tag, tag, inner, tag)
    i = html.rfind(closing)
    if i < 0:
        raise SystemExit("no %s found — cannot install" % closing)
    return html[:i] + el + html[i:]


def process(path, check_only, polish):
    with open(path, encoding="utf-8") as fh:
        original = fh.read()
    html = original

    css = [b for b in CSS_BLOCKS if polish or b[0] not in OPTIONAL]
    js = [b for b in JS_BLOCKS if polish or b[0] not in OPTIONAL]

    if BEGIN % "ENGINE" not in html:
        if check_only:
            print("  MISSING %s  (framework not installed)" % path)
            return False
        html = install(html, css, "style", "</head>")
        html = install(html, js, "script", "</body>")
    else:
        for name, src in css + js:
            html, _ = splice(html, name, read(src))

    if html == original:
        print("  ok      %s" % path)
        return True
    if check_only:
        print("  STALE   %s" % path)
        return False
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("  update  %s  (%+d bytes)" % (path, len(html) - len(original)))
    return True


def main(argv):
    check_only = "--check" in argv
    polish = "--no-polish" not in argv
    targets = [a for a in argv if not a.startswith("--")]
    if not targets:
        raise SystemExit(__doc__)
    results = [process(p, check_only, polish) for p in targets]
    if False in results:
        raise SystemExit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
