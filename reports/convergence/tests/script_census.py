#!/usr/bin/env python3
"""JOB 1(b) — census every source either injector can inline, for tokens that
would close the element they are inlined into.

A hit is not automatically a bug: it is a bug only if the source is inlined
without escaping. This reports the hit, which injector would carry it, and
whether that injector escapes.

    python3 reports/convergence/tests/script_census.py
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "grow-anim"))
import inject as grow_inject                                        # noqa: E402
sys.path.insert(0, os.path.join(ROOT, "reports", "convergence"))
import inject_convergence                                            # noqa: E402

# source -> list of (injector, element it is inlined INTO, escapes?)
SOURCES = {}


def note(src, injector, element, escapes):
    SOURCES.setdefault(src, []).append((injector, element, escapes))


for name, src in grow_inject.CSS_BLOCKS:
    note(os.path.join("grow-anim", src), "grow-anim/inject.py:" + name, "style", True)
for name, src in grow_inject.JS_BLOCKS:
    note(os.path.join("grow-anim", src), "grow-anim/inject.py:" + name, "script", True)
for name, srcs in inject_convergence.MAP:
    element = "style" if name == "CSS" else "script"
    for src in srcs:
        note(src, "inject_convergence.py:" + name, element, True)
# build-anim/inject.py must not be touched, so its table is transcribed rather
# than imported. CSS goes into a <style>, everything else into a <script>.
for src, element in [("build-anim.css", "style"), ("bio-svg.js", "script"),
                     ("body-svg.js", "script"), ("food-svg.js", "script"),
                     ("chain-svg.js", "script"), ("build-anim.js", "script")]:
    note(os.path.join("build-anim", src), "build-anim/inject.py", element, False)

TOKEN = {"script": "</script", "style": "</style"}
live, inert, clean = [], [], []

for src in sorted(SOURCES):
    path = os.path.join(ROOT, src)
    if not os.path.exists(path):
        continue
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    found = False
    for injector, element, escapes in SOURCES[src]:
        token = TOKEN[element]
        for i, line in enumerate(lines, 1):
            for m in re.finditer(re.escape(token), line):
                if line[m.start():m.start() + 2] == "<\\":
                    continue                      # already escaped, inert
                rec = (src, i, token, element, injector, escapes, line.strip()[:84])
                (live if not escapes else inert).append(rec)
                found = True
        # a token that cannot close this element is not a hazard at all
        other = TOKEN["style" if element == "script" else "script"]
        for i, line in enumerate(lines, 1):
            if other in line and line[line.index(other):line.index(other) + 2] != "<\\":
                inert.append((src, i, other, element, injector, escapes,
                              line.strip()[:84] + "   [cannot close a <%s>]" % element))
                found = True
    if not found:
        clean.append(src)

print("Sources an injector can inline: %d" % len(SOURCES))
print("Sources with no self-closing token at all: %d" % len(clean))
print()
print("LIVE HAZARDS (token can close its element AND the injector does not escape): %d"
      % len(live))
for src, i, token, element, injector, _e, text in live:
    print("  %s:%d  %r inside a <%s> written by %s" % (src, i, token, element, injector))
    print("      %s" % text)
if not live:
    print("  none")
print()
print("HANDLED OR INERT: %d" % len(inert))
for src, i, token, element, injector, escapes, text in inert:
    why = "escaped by " + injector if escapes else "inert"
    print("  %s:%d  %r  (<%s>)  -> %s" % (src, i, token, element, why))
    print("      %s" % text)
sys.exit(1 if live else 0)
