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

VERSION = "g25-v2.0.0-binding-on-scope-new"
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

CONTRACT = ROOT / "_sownb/STYLE_CONTRACT.json"

def taxonomy() -> tuple[list, bool]:
    rows = {r["id"]: r for r in json.loads(CONTRACT.read_text())["rows"]}
    row = rows.get("wedo.taxonomy")
    if row is None:
        return [], False
    return list(row["value"]), row.get("scope") == "new"


def judge(m: dict, types: list) -> dict:
    """The declared type must be one of the six. Undeclared is a fail under the
    binding scope: a rotation rule cannot be checked against a deck that does
    not say which type it used."""
    declared = m.get("declaredType")
    fails = []
    if not declared:
        fails.append("wedo.taxonomy: deck declares no we-do type")
    elif declared not in types:
        fails.append(f"wedo.taxonomy: '{declared}' is not one of {types}")
    return {"fails": fails, "verdict": "PASS" if not fails else "RED"}


def declared_type(path: Path) -> str | None:
    src = path.read_text(encoding="utf-8")
    m = re.search(r'"weDoType"\s*:\s*"([^"]+)"', src)
    return m.group(1) if m else None


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    scope = "new" if "--scope=new" in sys.argv else "live"
    types, scoped_new = taxonomy()
    binding = scope == "new" and scoped_new
    out, red = [], 0
    sha = __import__("hashlib").sha256(CONTRACT.read_bytes()).hexdigest()
    for a in args:
        m = measure(ROOT / a)
        m["declaredType"] = declared_type(ROOT / a)
        j = judge(m, types)
        m.update({"scope": scope, "binding": binding, "contractSha256": sha, **j})
        if binding and j["verdict"] == "RED":
            red += 1
        out.append(m)
        print(f"{Path(a).name[:46]:46s} weDoStages={m['weDoStages']} declared={m['declaredType']} "
              f"observed={m['typesUsed']} {j['verdict']:4s} "
              f"{'BINDING' if binding else 'report-only'} contract {sha[:8]} [{VERSION}]")
        for f in j["fails"]:
            print(f"    {f}")
    Path("/tmp/g25_last.json").write_text(json.dumps(out, indent=1))
    sys.exit(1 if red else 0)
