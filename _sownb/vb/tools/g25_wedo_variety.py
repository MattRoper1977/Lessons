#!/usr/bin/env python3
"""g25 — "we do" activity variety. REPORT ONLY. Order VB run 6 §4.2.

Finds the guided-practice stages by their declared title ("We Do ...") rather
than by position, because families differ in how many they run. Extracts the
instruction text and classifies the activity by the verb-and-pattern it
actually uses. The type list is DISCOVERED from the estate, not imposed: an
unmatched stage is reported as UNCLASSIFIED with its opening words, so the
taxonomy grows from what is really there.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from lxml import html as lh

VERSION = "g25-v1.0.0-wedo-variety-report-only"
ROOT = Path(__file__).resolve().parents[3]

# Discovered patterns, each (type, regex over the stage's pupil text).
PATTERNS = [
    ("sort-or-match",        r"\bsort\b|\bmatch\b|\bgroup (them|these|into)\b|\bcategoris|\bodd one out\b"),
    ("predict-then-check",   r"\bpredict\b|\bwhat will happen\b|\bthen check\b|\bbefore you (look|test)\b"),
    ("label-the-diagram",    r"\blabel\b|\bannotate\b|\bmark on\b|\badd (the )?labels\b"),
    ("rank-or-order",        r"\brank\b|\border\b|\bsequence\b|\bput .{0,20}in order\b|\btimeline\b"),
    ("worked-example-gaps",  r"\bfill (in )?the gap|\bcomplete the (example|sentence|frame)\b|\bmissing (word|step)\b"),
    ("paired-talk",          r"\btalk (to|with) (a )?partner\b|\bpair\b|\bdiscuss with\b|\bturn to your\b"),
    ("show-me",             r"\bshow me\b|\bwhiteboard\b|\bhold up\b|\bthumbs\b|\beveryone commits\b|\bvote\b"),
    ("quick-quiz",           r"\bquiz\b|\btrue or false\b|\bmultiple choice\b|\bA, B or C\b"),
    ("spot-the-error",       r"\bspot the (error|mistake)\b|\bwhat.{0,12}wrong\b|\bcorrect the\b"),
    ("decision-lab",         r"\bdecision lab\b|\bdecide\b|\bchoose .{0,20}(route|option)\b|\bjustify your choice\b"),
]

def stage_text(node) -> str:
    n = node.__copy__()
    for bad in n.xpath('.//*[@data-audience="staff"]|.//*[@data-mbm-guide]|.//script|.//style'):
        p = bad.getparent()
        if p is not None: p.remove(bad)
    return " ".join(n.text_content().split())

def classify(text: str):
    low = text.lower()
    hits = [t for t, pat in PATTERNS if re.search(pat, low)]
    return hits

def measure(path: Path) -> dict:
    tree = lh.fromstring(path.read_text(encoding="utf-8"))
    stages = tree.xpath('//main[contains(concat(" ",normalize-space(@class)," ")," deck ")]'
                        '/section[contains(concat(" ",normalize-space(@class)," ")," slide ")]')
    out = []
    for i, s in enumerate(stages, 1):
        title = (s.get("data-title") or "")
        if not re.match(r"\s*we\s*do", title, re.I): continue
        txt = stage_text(s)
        hits = classify(txt)
        out.append({"stage": i, "title": title, "minutes": s.get("data-min"),
                    "types": hits or ["UNCLASSIFIED"],
                    "opening": txt[:110]})
    return {"file": str(path.relative_to(ROOT)), "toolVersion": VERSION,
            "weDoStages": len(out), "stages": out,
            "typesUsed": sorted({t for o in out for t in o["types"]})}

if __name__ == "__main__":
    print(json.dumps([measure(ROOT / a) for a in sys.argv[1:]], indent=1))
