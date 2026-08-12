#!/usr/bin/env python3
"""Stage B — put the slide announcer within reach of the decks that never had it.

The announcer lives in hud.js and was built so that no lesson file needed
editing to get it. 225 decks already load hud.js and were covered the moment it
merged. This adds the include, and ONLY the include, to the decks that do not.

The change per file is one line before </body>:

    <script defer src="/hud.js"></script>

That exact form is not a preference. 220 of the 225 already-covered decks use
it; the other 5 use a loader with a relative fallback, which exists to survive
file:// and is out of scope here — hud.js loading from the domain root and
404ing under file:// is an established property of this estate, not a defect to
fix in a pass about announcements.

  python3 tools/stage_b_announcer.py --list                 what is in scope
  python3 tools/stage_b_announcer.py --apply POPULATION     insert the include
  python3 tools/stage_b_announcer.py --prove [--base REF]   prove it inert
  python3 tools/stage_b_announcer.py --self-test            prove the proof works

--prove is the gate. It asserts, per file, that the ONLY difference from the
base ref is that one insertion — which is a stronger statement than checking
regions one at a time, because it leaves nothing unchecked. The named regions
(closure, witness, tiers, print blocks, Oak text) are then asserted explicitly
on top of it, because a proof nobody can read is not much of a proof.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAG = '<script defer src="/hud.js"></script>'

# REGISTER.md:1545 (R-SEMH02, ruled 2026-08-04): the 2025-26 freeze on these
# four trees. Path-scoped, not a subject heuristic.
FROZEN_LEGACY_SCIENCE = ("biology/", "chemistry/", "2 Physics 10/", "5 Intervention 10/")
# Excluded regardless of anything else.
HARD_EXCLUDE_DIRS = ("Games/", "LundyLoop/", "Baseline_Weeks/", ".git/",
                     # GROW_Estate_v3 and LAUNCH_Estate_v3 are governed by
                     # .github/workflows/glv3-verify.yml, whose broken-link gate
                     # resolves every "/"-absolute href against the REPO root.
                     # /hud.js lives in the site repo and is only root-absolute
                     # on the deployed domain, so the include reads as 78 broken
                     # links there and turned that gate red. Correct in
                     # production, unacceptable to the gate as written. Excluded
                     # until Matt rules; see _teachgreen/DECISIONS.md.
                     "GROW_Estate_v3/", "LAUNCH_Estate_v3/")

# The named byte-regions the close order requires held. Each is (label, regex).
# They are asserted per file, before and after, on top of the exact-diff proof.
REGIONS = [
    ("closure",  re.compile(r"What I said, and what it changed")),
    ("witness",  re.compile(r"witness", re.I)),
    ("tiers",    re.compile(r"(?:Supported|Standard|Stretch)")),
    ("print",    re.compile(r"@media\s+print")),
    ("oak",      re.compile(r"Oak National Academy|thenational\.academy", re.I)),
    ("loopmark", re.compile(r"ll-g:loop-mark")),
]


def sh(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True, text=True).stdout


def title_of(text: str) -> str:
    m = re.search(r"<title>(.*?)</title>", text, re.S)
    return m.group(1).strip() if m else ""


def is_deck(text: str) -> bool:
    """A deck has slides to move between, which means more than one of them.

    Matching the bare string ".slide" also matches a CSS rule, and matching a
    single class="slide" also matches a page with one such container. Both
    false-positives were real: build-anim/demo.html and grow-anim/demo.html are
    "Animation Framework" reference pages carrying exactly one class="slide"
    element and no deck at all. They took the include, and the runtime gate
    caught them — 0 announcements, and the announcer correctly declining to arm
    because hud.js itself requires slides.length > 1. The include was reverted
    and the scope rule corrected here, so no later run re-adds them."""
    return len(re.findall(r'class="[^"]*\bslide\b[^"]*"', text)) > 1


def in_scope() -> list[str]:
    """Every deck that does not already load hud.js, minus every exclusion.

    The star matters only in the <title>. In the body it is the Stretch tier
    marker and appears in 221 files; in the title it marks an assessed lesson
    and appears in exactly 2. Excluding on the body marker would have removed
    the plan's own first population.
    """
    out = []
    for dirpath, _dirs, files in os.walk(ROOT):
        rel_dir = os.path.relpath(dirpath, ROOT)
        if rel_dir == ".":
            rel_dir = ""
        if any((rel_dir + "/").startswith(d) for d in HARD_EXCLUDE_DIRS):
            continue
        if ".git" in dirpath:
            continue
        for f in files:
            if not f.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, f), ROOT)
            if any(rel.startswith(d) for d in HARD_EXCLUDE_DIRS + FROZEN_LEGACY_SCIENCE):
                continue
            try:
                text = Path(dirpath, f).read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if not is_deck(text) or "hud.js" in text:
                continue
            if "★" in title_of(text):        # assessed lesson
                continue
            out.append(rel)
    return sorted(out)


def population_of(rel: str) -> str:
    head = rel.split(os.sep)[0]
    if head == "Science_Teesside":
        return "Science_Teesside/v3_40min" if "v3_40min" in rel else "Science_Teesside/other"
    return head


def apply_to(rels: list[str]) -> tuple[int, list[str]]:
    done, skipped = 0, []
    for rel in rels:
        p = ROOT / rel
        text = p.read_text(encoding="utf-8")
        if "hud.js" in text:
            skipped.append(f"{rel}: already loads hud.js")
            continue
        if "</body>" not in text:
            skipped.append(f"{rel}: no </body> to anchor the include")
            continue
        # Five decks carry a second </body> inside a JavaScript string: the
        # print-window template they hand to document.write. Inserting at the
        # FIRST match would corrupt that template. The document's own closing
        # tag is the LAST one, and it is only provably the last if nothing but
        # </html> and whitespace follows it — which is asserted, not assumed.
        cut = text.rfind("</body>")
        tail = text[cut + len("</body>"):]
        if not re.fullmatch(r"\s*(?:</html>)?\s*", tail, re.I):
            skipped.append(f"{rel}: content after the last </body> ({tail[:40]!r}), anchor unsafe")
            continue
        p.write_text(text[:cut] + TAG + text[cut:], encoding="utf-8")
        done += 1
    return done, skipped


def prove(base: str, rels: list[str] | None = None) -> list[str]:
    """The gate. For each changed file the ONLY difference from base must be the
    single insertion, and every named region must survive it."""
    problems: list[str] = []
    changed = [x for x in sh(f"git diff --name-only {base} -- '*.html'").split("\n") if x]
    if rels is not None:
        changed = [c for c in changed if c in set(rels)]
    for rel in changed:
        before = sh(f"git show {base}:'{rel}'")
        after = (ROOT / rel).read_text(encoding="utf-8")
        if before == after:
            continue
        cut = before.rfind("</body>")
        expected = before[:cut] + TAG + before[cut:]
        if after != expected:
            problems.append(f"{rel}: differs from base by more than the single include")
            continue
        if after.count(TAG) != 1:
            problems.append(f"{rel}: the include appears {after.count(TAG)} times")
        for label, rx in REGIONS:
            b, a = rx.findall(before), rx.findall(after)
            if b != a:
                problems.append(f"{rel}: {label} region changed ({len(b)} -> {len(a)})")
    return problems, changed


def sentinels(base: str) -> list[str]:
    """A hold pass declares no movement, so both sets must be set-identical.
    Derivation copied from _lsg1/tools/lgates.py so the two cannot disagree."""
    problems = []
    for name, pat, exp in (("ll-g:loop-mark", "ll-g:loop-mark", 50),
                           ("written-closure", "What I said, and what it changed", 123)):
        b = set(x.split(":", 1)[1] for x in sh(
            f"git grep -l -F '{pat}' {base} -- '*.html'").strip().split("\n") if x)
        h = set(x.split(":", 1)[1] for x in sh(
            f"git grep -l -F '{pat}' HEAD -- '*.html'").strip().split("\n") if x)
        ok = (b == h and len(h) == exp)
        print(f"   {name:18} base={len(b):<4} HEAD={len(h):<4} expected={exp:<4} "
              f"set-identical={b == h}")
        if not ok:
            problems.append(f"sentinel {name}: base={len(b)} HEAD={len(h)} expected={exp}")
    return problems


def protected_untouched(base: str) -> list[str]:
    """Frozen, assessed, Games and legacy must show zero changed files."""
    problems = []
    changed = [x for x in sh(f"git diff --name-only {base}").split("\n") if x]
    for rel in changed:
        if any(rel.startswith(d) for d in FROZEN_LEGACY_SCIENCE):
            problems.append(f"FROZEN legacy science touched: {rel}")
        if rel.startswith("Games/") or rel.startswith("LundyLoop/") or rel.startswith("Baseline_Weeks/"):
            problems.append(f"hard-excluded tree touched: {rel}")
        if rel.endswith(".html"):
            try:
                if "★" in title_of((ROOT / rel).read_text(encoding="utf-8", errors="ignore")):
                    problems.append(f"assessed (title-star) file touched: {rel}")
            except OSError:
                pass
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--apply", metavar="POPULATION")
    ap.add_argument("--prove", action="store_true")
    ap.add_argument("--base", default="origin/main")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        # The proof must reject a file carrying anything beyond the include.
        # Prefer a file this pass already changed; fall back to one still in
        # scope. Either way the tree is restored before returning.
        changed = [x for x in sh(f"git diff --name-only {a.base} -- '*.html'").split("\n") if x]
        victim_rel = changed[0] if changed else (in_scope() or [None])[0]
        if not victim_rel:
            print("[FAIL] self-test: no file available to test against")
            return 1
        victim = ROOT / victim_rel
        original = victim.read_text(encoding="utf-8")
        c = original.rfind("</body>")
        victim.write_text(original[:c] + "<!--stage-b-self-test-->" + original[c:], encoding="utf-8")
        probs, _ = prove(a.base, [victim_rel])
        victim.write_text(original, encoding="utf-8")
        if not probs:
            print("[FAIL] self-test: the proof accepted a file carrying more than the include")
            return 1
        print(f"[PASS] self-test: the proof rejected an over-wide change — {probs[0]}")
        return 0

    scope = in_scope()
    if a.list:
        pops: dict[str, int] = {}
        for rel in scope:
            pops[population_of(rel)] = pops.get(population_of(rel), 0) + 1
        print(f"IN SCOPE: {len(scope)} decks without hud.js, exclusions applied\n")
        for p, c in sorted(pops.items(), key=lambda x: -x[1]):
            print(f"   {p:34} {c:>4}")
        return 0

    if a.apply:
        rels = [r for r in scope if population_of(r) == a.apply]
        if not rels:
            print(f"no files in population {a.apply!r}")
            return 1
        done, skipped = apply_to(rels)
        print(f"{a.apply}: include added to {done} file(s)")
        for s in skipped:
            print("   skipped:", s)
        return 0

    if a.prove:
        problems, changed = prove(a.base)
        print(f"EXACT-DIFF PROOF · {len(changed)} changed file(s) vs {a.base}")
        print("   every changed file must differ by exactly one inserted include\n")
        print("SENTINELS (hold pass — unchanged is the only green)")
        problems += sentinels(a.base)
        print()
        problems += protected_untouched(a.base)
        if problems:
            print(f"[FAIL] Stage B — {len(problems)} problem(s):")
            for p in problems[:25]:
                print("   -", p)
            return 1
        print(f"[PASS] Stage B: {len(changed)} file(s) differ from {a.base} by exactly the "
              f"include; closure/witness/tiers/print/Oak/loop-mark regions identical; "
              f"sentinels 50/123 set-identical; frozen, assessed, Games and legacy untouched")
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
