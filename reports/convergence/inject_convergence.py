#!/usr/bin/env python3
"""Re-inject the five Autumn 1 BUILD lessons against grow-anim/ instead of build-anim/.

This is README step 1 of the convergence plan, done for real. The README says
"inject.py's BLOCKS table is where that switch happens" — that is too glib, and
this script exists because of the two reasons why:

  1. The marker vocabularies are DISJOINT. BUILD lessons carry
     /* BUILD-ANIM:CSS|BIO|BODY|FOOD|CHAIN|JS */ markers; grow-anim/inject.py
     writes /* GROW-ANIM:MOTION|COMP|POLISH|SVG|BIO|ANIM|PHY|CHEM|ENGINE|SHINE */.
     Pointing either injector at the other suite's files finds no markers and
     does nothing. The switch has to be a re-MAPPING of BUILD's markers onto
     GROW's sources, which is what MAP below is.

  2. Load order is forced. compat-build-anim.js has to run after grow-anim.js
     (it reads global.GrowAnim) but before the BUILD subject libraries
     body/food/chain-svg.js (they call global.BioSVG.helpers at load time, and
     compat is what defines BioSVG). In a BUILD lesson the marker order is
     CSS -> BIO -> SUBJECT -> JS, so the whole GROW engine plus the compat shim
     must land in the BIO block, and the JS block becomes a stub.

Nothing in build-anim/ is modified. The subject libraries are still read from
build-anim/ — they register into the shared registry through the compat shim
and are engine-agnostic already.

    python3 reports/convergence/inject_convergence.py --check   Science_Teesside/Build/*.html
    python3 reports/convergence/inject_convergence.py           Science_Teesside/Build/*.html
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

STUB = ("/* The engine now loads in the BIO block above, together with the GROW\n"
        "   asset registry and the build-anim compatibility shim. Kept as an empty\n"
        "   marked block so the injector still has somewhere to write. */")

# BUILD marker name -> the grow-anim sources that now fill it, in load order.
# A source of None means "leave whatever build-anim source already filled it".
MAP = [
    ("CSS",   ["grow-anim/grow-motion.css",
               "grow-anim/grow-anim.css",
               "grow-anim/grow-polish.css"]),
    ("BIO",   ["grow-anim/grow-svg.js",
               "grow-anim/grow-svg-bio-animals.js",
               "grow-anim/grow-anim.js",
               "grow-anim/grow-polish.js",
               "grow-anim/compat-build-anim.js"]),
    ("BODY",  ["build-anim/body-svg.js"]),
    ("FOOD",  ["build-anim/food-svg.js"]),
    ("CHAIN", ["build-anim/chain-svg.js"]),
    ("JS",    []),
]


# The escaping that makes an inlined source survive the HTML parser lives in the
# shared injection path now, not here — see grow-anim/inject.py's
# escape_for_inline(). This module imports it rather than keeping a second copy,
# so a lesson injected by either route is protected the same way.
sys.path.insert(0, os.path.join(ROOT, "grow-anim"))
from inject import escape_for_inline  # noqa: E402


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return escape_for_inline(fh.read().rstrip("\n"))


def body_for(sources):
    if not sources:
        return STUB
    return "\n".join("/* --- %s --- */\n%s" % (s, read(s)) for s in sources)


def wrap(name, sources, body):
    origin = ", ".join(sources) if sources else "nothing — see below"
    return ("/* BUILD-ANIM:%s:BEGIN — generated from %s, do not edit here */\n"
            "%s\n/* BUILD-ANIM:%s:END */" % (name, origin, body, name))


def splice(html, name, sources):
    begin = "/* BUILD-ANIM:%s:BEGIN" % name
    end = "/* BUILD-ANIM:%s:END */" % name
    i = html.find(begin)
    if i < 0:
        return html, False
    j = html.find(end, i)
    if j < 0:
        raise SystemExit("unclosed %s marker" % name)
    return html[:i] + wrap(name, sources, body_for(sources)) + html[j + len(end):], True


def process(path, check_only):
    with open(path, encoding="utf-8") as fh:
        original = fh.read()
    html, hit = original, []
    for name, sources in MAP:
        html, found = splice(html, name, sources)
        if found:
            hit.append(name)
    if not hit:
        print("  skip    %s  (no BUILD-ANIM markers)" % path)
        return None
    if html == original:
        print("  ok      %-56s  markers: %s" % (path, "+".join(hit)))
        return True
    if check_only:
        print("  STALE   %-56s  markers: %s" % (path, "+".join(hit)))
        return False
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("  rewrite %-56s  markers: %s  (%+d bytes)"
          % (path, "+".join(hit), len(html) - len(original)))
    return True


def main(argv):
    check_only = "--check" in argv
    targets = [a for a in argv if not a.startswith("--")]
    if not targets:
        raise SystemExit(__doc__)
    results = [process(p, check_only) for p in targets]
    if False in results:
        raise SystemExit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
