#!/usr/bin/env python3
"""AAE-R1B §R2 -- classify every venue mention EXAMPLE or ASSERTED, then convert.

THE RULING, AND WHY THE DEFAULT IS TO KEEP
-------------------------------------------
R2: classify every line EXAMPLE (an organisation named as teaching content or
"e.g." -- keep) or ASSERTED (the pupil's visit, attendance or booking -- convert
to a slot read). And explicitly: do not strip a venue named as an example. A
Teesside Art deck may name Teesside's gallery.

That matters because the obvious automation -- delete every venue name -- would
have removed ten pieces of real teaching to fix one graphic. A gallery named in
a knowledge organiser, offered as an answer to "name one Teesside arts
organisation", or drawn on a sorting card IS the lesson. What is not allowed is
a deck telling a pupil they are going somewhere that is not booked.

THE DISCRIMINATOR
-----------------
ASSERTED when the mention sits in second-person attendance language -- your
visit, when we go, on the trip, bring your ticket -- or on a ticket, pass or
itinerary graphic, which depicts an attendance whatever the words around it say.
EVERYTHING ELSE IS AN EXAMPLE, including a definition, a recall answer, a
sorting card, a key fact and an "or own answer" prompt. The default keeps.

The window is 200 characters either side of the mention, not the whole line:
these decks put a whole slide on one line, so a whole-line read would classify a
knowledge organiser by something three slides away.

Every mention is printed with its classification and the reason, because a
selector that narrows a set must say what it dropped and why.

    python3 tools/artsaward/venue_classify.py            # classify and print
    python3 tools/artsaward/venue_classify.py --apply    # make the conversions
    python3 tools/artsaward/venue_classify.py --self-test
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

VERSION = "venue-classify-v1.0.0"
ROOT = Path(__file__).resolve().parents[2]
SLOTS_PATH = ROOT / "tools/artsaward/SLOTS.json"

ASSERTED_NEAR = re.compile(
    r"\b(your visit|when we visit|when you visit|when we go|on the trip|"
    r"during the trip|book(?:ing)? (?:your |the )?tickets?|buy (?:a |your )?tickets?|"
    r"bring your ticket|we will be going|you will be going)\b", re.I)
TICKET_GRAPHIC = re.compile(r"\bADMIT ONE\b", re.I)
EXAMPLE_NEAR = re.compile(
    r"\b(e\.g\.|for example|such as|or own answer|or any|name one|name a|"
    r"which cards|key facts?|definition)\b", re.I)


def digest(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def venues() -> list[str]:
    doc = json.loads(SLOTS_PATH.read_text(encoding="utf-8"))
    return [c["name"] for c in (doc.get("candidates") or [])]


def strip_tags(s: str) -> str:
    return " ".join(re.sub(r"<[^>]+>", " ", s).split())


def classify(line: str, start: int, end: int) -> tuple[str, str]:
    window = line[max(0, start - 200):min(len(line), end + 200)]
    plain = strip_tags(window)
    if TICKET_GRAPHIC.search(plain):
        return "ASSERTED", ("the venue is lettered on a ticket graphic, which depicts "
                            "an attendance whatever the words around it say")
    m = ASSERTED_NEAR.search(plain)
    if m:
        return "ASSERTED", f"second-person attendance language nearby: {m.group(0)!r}"
    m = EXAMPLE_NEAR.search(plain)
    if m:
        return "EXAMPLE", f"offered as teaching content or an option: {m.group(0)!r}"
    return "EXAMPLE", ("named as content with no attendance language around it; the "
                       "default is to keep, because a Teesside Art deck may name "
                       "Teesside's gallery")


def scan(files: list[Path] | None = None) -> dict:
    names = venues()
    pat = re.compile("|".join(rf"\b{re.escape(n)}\b" for n in names))
    if files is None:
        files = [p for p in ROOT.rglob("*.html")
                 if "node_modules" not in str(p) and pat.search(
                     p.read_text(encoding="utf-8", errors="replace"))]
    rows = []
    for p in sorted(files):
        raw = p.read_text(encoding="utf-8", errors="replace")
        for i, line in enumerate(raw.splitlines(), 1):
            for m in pat.finditer(line):
                verdict, why = classify(line, m.start(), m.end())
                a = max(0, m.start() - 110)
                b = min(len(line), m.end() + 110)
                try:
                    rel = str(p.resolve().relative_to(ROOT))
                except ValueError:
                    rel = str(p)
                rows.append({"file": rel, "line": i, "venue": m.group(0),
                             "verdict": verdict, "why": why,
                             "context": strip_tags(line[a:b])})
    return {"tool": VERSION, "slotsSha256": digest(SLOTS_PATH),
            "venues": names, "mentions": len(rows),
            "asserted": sum(1 for r in rows if r["verdict"] == "ASSERTED"),
            "example": sum(1 for r in rows if r["verdict"] == "EXAMPLE"),
            "rows": rows}


# The conversions this scan calls for, written out as pairs so they are
# reviewable and so --apply cannot do anything the classification did not name.
CONVERSIONS = [
    {"file": "Art_Teesside/Grow/GROW_ART_W4_Arts_Event_Attend_Capture_and_Review.html",
     "from": ">MIMA · GALLERY · SHOW<",
     "to": ">GALLERY · SHOW<",
     "why": ("the venue is lettered on a ticket graphic in a deck about attending an "
             "arts event, which tells a pupil they are going to a named place that is "
             "not booked. The drawing stays; the venue comes from EVENT_SLOT.")},
]


def apply_conversions() -> list[dict]:
    done = []
    for c in CONVERSIONS:
        p = ROOT / c["file"]
        raw = p.read_text(encoding="utf-8")
        if c["from"] not in raw:
            done.append({**c, "status": "ALREADY CONVERTED"
                         if c["to"] in raw else "NOT FOUND"})
            continue
        p.write_text(raw.replace(c["from"], c["to"]), encoding="utf-8")
        done.append({**c, "status": "CONVERTED", "sha256": digest(p)})
    return done


def controls() -> list[dict]:
    out = []

    def rec(cid, claim, expect, actual):
        out.append({"id": cid, "claim": claim, "expected": expect, "actual": actual,
                    "verdict": "PASS" if expect == actual else "RED"})

    def verdict_of(html: str) -> str:
        i = html.index("MIMA")
        return classify(html, i, i + 4)[0]

    rec("a-venue-on-a-ticket-graphic-is-asserted",
        "a ticket depicts an attendance whatever the words around it say",
        "ASSERTED",
        verdict_of('<text>ADMIT ONE</text><text>MIMA · GALLERY · SHOW</text>'))
    rec("a-venue-offered-as-an-answer-is-an-example",
        "a gallery named as a recall answer is the lesson, not a claim",
        "EXAMPLE",
        verdict_of('<p>Name one Teesside arts organisation.</p>'
                   '<p>MIMA (or any local gallery).</p>'))
    rec("second-person-attendance-language-is-asserted",
        "'when we visit' asserts an attendance",
        "ASSERTED", verdict_of('<p>When we visit MIMA you will look at three works.</p>'))
    rec("a-bare-fact-defaults-to-example",
        "the default keeps; a Teesside Art deck may name Teesside's gallery",
        "EXAMPLE", verdict_of('<li>MIMA sits in the middle of Middlesbrough.</li>'))
    rec("every-conversion-names-a-real-string-in-a-real-file",
        "a conversion pair that no longer matches is reported, never applied blind",
        [], [c["file"] for c in CONVERSIONS
             if not (ROOT / c["file"]).is_file()
             or (c["from"] not in (ROOT / c["file"]).read_text(encoding="utf-8")
                 and c["to"] not in (ROOT / c["file"]).read_text(encoding="utf-8"))])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--output")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--list-controls", action="store_true")
    a = ap.parse_args()

    if a.list_controls:
        for c in controls():
            print(c["id"])
        return 0
    if a.self_test:
        cs = controls()
        for c in cs:
            print(f"{c['verdict']:4s} {c['id']}: {c['claim']}")
            if c["verdict"] == "RED":
                print(f"       expected {c['expected']!r} got {c['actual']!r}")
        red = [c for c in cs if c["verdict"] == "RED"]
        print(f"{len(cs) - len(red)}/{len(cs)} controls PASS")
        return 1 if red else 0

    doc = scan()
    print(f"{VERSION}: {doc['mentions']} venue mention(s) — "
          f"{doc['asserted']} ASSERTED, {doc['example']} EXAMPLE")
    last = None
    for i, r in enumerate(doc["rows"], 1):
        if r["file"] != last:
            print(f"\n  {r['file']}")
            last = r["file"]
        print(f"    [{i:>2}] line {r['line']:>4}  {r['verdict']:8s} {r['venue']}")
        print(f"         why: {r['why']}")
        print(f"         …{r['context'][:150]}…")
    if a.apply:
        print("\n--- conversions ---")
        doc["conversions"] = apply_conversions()
        for c in doc["conversions"]:
            print(f"  {c['status']:18s} {c['file']}")
            print(f"    {c['from']!r} -> {c['to']!r}")
            print(f"    {c['why']}")
    if a.output:
        Path(a.output).parent.mkdir(parents=True, exist_ok=True)
        Path(a.output).write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
        print(f"\nwrote {a.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
