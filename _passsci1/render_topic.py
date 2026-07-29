#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render every lesson in a content module, then gate each. Usage: render_topic.py <module>."""
import sys
import pathlib
import importlib

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "inputs"))
import render_v5
import illuminators
import gates

J = str((HERE / "node_modules/jsdom").resolve())
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)


def run(modname):
    importlib.reload(illuminators)
    importlib.reload(render_v5)
    mod = importlib.import_module(modname)
    slugs = []
    for L in mod.LESSONS:
        html = render_v5.render_lesson(mod, L, illuminators.ILLUMINATORS)
        (OUT / (L["slug"] + ".html")).write_text(html, encoding="utf-8")
        slugs.append(L["slug"])
        print(f"  rendered {L['slug']} ({len(html)}b)")
    allok = True
    for L in mod.LESSONS:
        p = str((OUT / (L["slug"] + ".html")).resolve())
        ok = gates.run(p, L["exit_key"], J)
        allok = allok and ok
    print(f"\n{modname}: {'ALL GREEN' if allok else 'FAIL'}  ({len(slugs)} lessons: {', '.join(slugs)})")
    return allok


if __name__ == "__main__":
    ok = run(sys.argv[1])
    sys.exit(0 if ok else 1)
