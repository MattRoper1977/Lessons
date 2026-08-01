#!/usr/bin/env python3
"""Inline the BUILD Animation Framework into single-file lesson HTML.

Classroom laptops open lessons straight from a file or a USB stick, so the
lessons have to stay self-contained.  This keeps that true without copy-paste
drift: the canonical library lives in build-anim/, and this script pushes it
into every lesson that carries the marker comments.

    python3 build-anim/inject.py Science_Teesside/Build/SCI_B_W3_Backbones.html
    python3 build-anim/inject.py Science_Teesside/Build/*.html
    python3 build-anim/inject.py --check Science_Teesside/Build/*.html

--check writes nothing and exits 1 if any lesson is out of date, so it can run
in a pre-commit hook or a build step.

A lesson that has no markers is reported and left completely untouched.
"""

import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# marker name -> source file
BLOCKS = [
    ("CSS", "build-anim.css"),
    ("BIO", "bio-svg.js"),
    ("JS",  "build-anim.js"),
]


def wrap(name, body):
    return "/* BUILD-ANIM:%s:BEGIN — generated from build-anim/, do not edit here */\n%s\n/* BUILD-ANIM:%s:END */" % (
        name, body.rstrip("\n"), name)


def splice(html, name, body):
    begin = "/* BUILD-ANIM:%s:BEGIN" % name
    end = "/* BUILD-ANIM:%s:END */" % name
    i = html.find(begin)
    if i < 0:
        return html, False
    j = html.find(end, i)
    if j < 0:
        raise SystemExit("unclosed %s marker" % name)
    return html[:i] + wrap(name, body) + html[j + len(end):], True


def process(path, check_only):
    with open(path, encoding="utf-8") as fh:
        original = fh.read()

    html, found_any = original, False
    for name, src in BLOCKS:
        with open(os.path.join(HERE, src), encoding="utf-8") as fh:
            body = fh.read()
        html, found = splice(html, name, body)
        found_any = found_any or found

    if not found_any:
        print("  skip   %s  (no BUILD-ANIM markers)" % path)
        return None

    if html == original:
        print("  ok     %s" % path)
        return True
    if check_only:
        print("  STALE  %s" % path)
        return False
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("  update %s" % path)
    return True


def main(argv):
    check_only = "--check" in argv
    targets = [a for a in argv if not a.startswith("--")]
    if not targets:
        raise SystemExit(__doc__)
    results = [process(p, check_only) for p in targets]
    if check_only and False in results:
        raise SystemExit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
