#!/usr/bin/env python3
"""Every bare module specifier resolves to a file in this repository.

WHY THIS EXISTS
Trekkers_Trail_Runner (2).html shipped an exit control that never worked. The
source contained the line that sets its href, and the rendered href was still
'#' - on load and after Start, with NO PAGE ERRORS. The cause was one level up
from anything a reader would look at: the whole game is a single
<script type="module">, and its importmap resolved `three` to
https://cdn.jsdelivr.net/npm/three@0.160.0/. A module whose imports cannot be
fetched never executes AT ALL, so init() never ran, so the setup function that
sets the href never ran.

The signature is what makes it dangerous: a blank or half-built page, and a
clean console. A failed module import surfaces as a network error, not an
uncaught exception, so nothing in the page says the game did not start. Two
other games in this estate were carried as broken for two passes on a related
misreading.

WHAT IT CHECKS
Two things, because they fail identically and silently:
  1. No importmap target and no <script type="module" src=...> is off-origin.
     An offline estate that fetches its engine from a CDN is not offline, and on
     a school network that blocks the CDN the game simply does not start.
  2. Every bare specifier a module imports resolves, THROUGH the importmap, to a
     file that exists. A vendored path with a typo fails exactly like a blocked
     CDN: silently, with a clean console.

Checking (2) matters as much as (1). Vendoring a dependency and mistyping the
path swaps a network failure for a filesystem one and looks identical.

Exits: 0 clean · 1 findings · 3 INCONCLUSIVE (nothing to judge)
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKIP_DIRS = {".git", "node_modules", "vendor", ".github"}

IMPORTMAP = re.compile(r'<script[^>]*type=["\']importmap["\'][^>]*>(.*?)</script>', re.S | re.I)
MODULE_SRC = re.compile(r'<script[^>]*type=["\']module["\'][^>]*\bsrc\s*=\s*["\']([^"\']+)', re.I)
# A bare specifier is one that is neither relative nor absolute: `three`, not
# './x.js' and not '/x.js'. Those are the ones an importmap has to resolve.
BARE_IMPORT = re.compile(r'^\s*import\s+[^;]*?\bfrom\s+["\'](?!\.|/)([^"\']+)["\']', re.M)
OFF_ORIGIN = re.compile(r'^(?:https?:)?//', re.I)


def html_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.lower().endswith((".html", ".htm")):
                yield os.path.join(dirpath, name)


def main():
    findings = []
    checked = specifiers = 0

    for path in sorted(html_files()):
        rel = os.path.relpath(path, ROOT)
        try:
            src = open(path, encoding="utf-8", errors="replace").read()
        except OSError as exc:
            findings.append(f"{rel}: unreadable ({exc})")
            continue

        for url in MODULE_SRC.findall(src):
            if OFF_ORIGIN.match(url):
                findings.append(f"{rel}: <script type=module> loads {url} off-origin — "
                                f"if it cannot be fetched the module never executes and nothing errors")

        match = IMPORTMAP.search(src)
        if not match:
            continue
        checked += 1
        try:
            imports = json.loads(match.group(1)).get("imports", {})
        except json.JSONDecodeError as exc:
            findings.append(f"{rel}: the importmap is not valid JSON ({exc}) — "
                            f"the browser ignores it entirely and every bare specifier fails")
            continue

        for spec, target in imports.items():
            if OFF_ORIGIN.match(target):
                findings.append(f"{rel}: importmap resolves '{spec}' to {target} off-origin — "
                                f"a blocked CDN stops the whole module executing, silently")

        base = os.path.dirname(path)
        for spec in sorted(set(BARE_IMPORT.findall(src))):
            specifiers += 1
            target = imports.get(spec)
            if target is None:
                for prefix, value in imports.items():
                    if prefix.endswith("/") and spec.startswith(prefix):
                        target = value + spec[len(prefix):]
                        break
            if target is None:
                findings.append(f"{rel}: imports '{spec}', which the importmap does not resolve")
                continue
            if OFF_ORIGIN.match(target):
                continue                                  # already reported above
            resolved = os.path.normpath(os.path.join(base, target))
            if not os.path.exists(resolved):
                findings.append(f"{rel}: '{spec}' resolves to {os.path.relpath(resolved, ROOT)}, "
                                f"which does not exist — the module will not execute and nothing will say so")

    if checked == 0:
        print("INCONCLUSIVE: no file in this repository carries an importmap, so this gate "
              "judged nothing. That is not a pass.", file=sys.stderr)
        raise SystemExit(3)

    print(f"{checked} file(s) with an importmap · {specifiers} bare specifier(s) resolved")
    if findings:
        print(f"\n{len(findings)} finding(s):", file=sys.stderr)
        for f in findings:
            print(f"  · {f}", file=sys.stderr)
        raise SystemExit(1)
    print("every module specifier resolves to a file in this repository; nothing is fetched off-origin")


if __name__ == "__main__":
    main()
