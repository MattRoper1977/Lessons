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

import importlib.util

VERSION = "g25-v4.0.0-shell-aware-with-integrated-controls"
ROOT = Path(__file__).resolve().parents[3]

# A2R 3.2. Stage discovery was `main.deck > section.slide`, the n6 shell alone,
# so every classic-shell deck reported weDoStages=0 and RED'd with "deck has no
# we-do stage to corroborate the declaration" -- a gate failing for want of an
# instrument, not for want of variety. BUILD_HUM_W16 did exactly that on main
# after #271. Stage discovery now comes from lesson_stages, which reads both
# shells and excludes the print pack, the staff drawer and hidden content.
_ls = importlib.util.spec_from_file_location(
    "lesson_stages", ROOT / "_sownb/vb/tools/lesson_stages.py")
stages_mod = importlib.util.module_from_spec(_ls); _ls.loader.exec_module(stages_mod)

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

def stage_text(node, screen=None) -> str:
    """Pupil text of one stage. Delegates to lesson_stages so that the staff
    drawer, hidden content and the print pack are excluded the same way here as
    in g18, g23 and g24 -- one answer to "what did the pupil read", not four."""
    if screen is not None:
        return stages_mod.stage_text(node, screen)
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
    tree = lh.fromstring(Path(path).read_text(encoding="utf-8"))
    screen = stages_mod.ScreenView(tree)
    found = stages_mod.stages(tree, screen)
    out = []
    for i, s in enumerate(found, 1):
        title = (s.get("data-title") or "")
        if not re.match(r"\s*we\s*do", title, re.I): continue
        txt = stage_text(s, screen)
        hits = classify(txt)
        out.append({"stage": i, "title": title, "minutes": s.get("data-min"),
                    "types": hits or ["UNCLASSIFIED"],
                    "opening": txt[:110]})
    try:
        rel = str(Path(path).relative_to(ROOT))
    except ValueError:
        rel = str(path)
    return {"file": rel, "toolVersion": VERSION,
            "shell": stages_mod.shell_of(tree),
            "deckStages": len(found),
            "weDoStages": len(out), "stages": out,
            "typesUsed": sorted({t for o in out for t in o["types"]})}

CONTRACT = ROOT / "_sownb/STYLE_CONTRACT.json"

def taxonomy() -> tuple[list, bool]:
    rows = {r["id"]: r for r in json.loads(CONTRACT.read_text())["rows"]}
    row = rows.get("wedo.taxonomy")
    if row is None:
        return [], False
    return list(row["value"]), row.get("scope") == "new"


# The PATTERNS vocabulary above was DISCOVERED from the estate in run 6 and is
# not the same vocabulary as the contract's six accepted types. Until run 7 the
# gate compared the declaration only against the six, so it could not fail on
# content: a deck declaring "commit-and-reveal" over a sorting activity was
# green. This map is the join between the two vocabularies, written once and
# explicitly. A discovery label with no contract equivalent maps to nothing and
# simply does not corroborate.
DISCOVERY_TO_CONTRACT = {
    "sort-or-match":       "sort-or-match",
    "predict-then-check":  "predict-then-check",
    "label-the-diagram":   "label-or-annotate",
    "rank-or-order":       "sequence-or-rank",
    "spot-the-error":      "spot-the-error",
    "show-me":             "commit-and-reveal",
    "quick-quiz":          "commit-and-reveal",
    "worked-example-gaps": None,
    "paired-talk":         None,
    "decision-lab":        None,
}


def corroborated(m: dict) -> list:
    """The contract types the deck's own we-do text actually evidences."""
    out = []
    for label in m.get("typesUsed", []):
        mapped = DISCOVERY_TO_CONTRACT.get(label)
        if mapped and mapped not in out:
            out.append(mapped)
    return sorted(out)


def judge(m: dict, types: list) -> dict:
    """Two things, not one. (1) The declared type must be one of the six --
    undeclared fails, because a rotation rule cannot be checked against a deck
    that does not say which type it used. (2) The declaration must be
    corroborated by the we-do text itself: at least one stage must read as the
    declared type. Without (2) the gate is a rubber stamp on a JSON string."""
    declared = m.get("declaredType")
    fails = []
    if not declared:
        fails.append("wedo.taxonomy: deck declares no we-do type")
    elif declared not in types:
        fails.append(f"wedo.taxonomy: '{declared}' is not one of {types}")
    else:
        evidence = corroborated(m)
        if not m.get("weDoStages"):
            fails.append("wedo.taxonomy: deck has no we-do stage to corroborate the declaration")
        elif declared not in evidence:
            fails.append(
                f"wedo.taxonomy: declared '{declared}' but the we-do text evidences "
                f"{evidence or ['nothing classifiable']} (discovery labels {m.get('typesUsed')})"
            )
    return {"fails": fails, "verdict": "PASS" if not fails else "RED",
            "corroborated": corroborated(m)}


def declared_type(path: Path) -> str | None:
    src = path.read_text(encoding="utf-8")
    m = re.search(r'"weDoType"\s*:\s*"([^"]+)"', src)
    return m.group(1) if m else None


# --------------------------------------------------------------------------
# Controls (A2R 3.2). The rotation rule the contract states is
# `wedo.rotation`: no two consecutive lessons in a family share a we-do type,
# and any six consecutive show >= 4 types. It is a rule about a SEQUENCE, so
# its controls are sequences: three of a kind must fire, a rotation must not.
# --------------------------------------------------------------------------

def rotation_verdict(sequence: list) -> dict:
    """The contract's wedo.rotation row, applied to a family's ordered types."""
    rows = {r["id"]: r for r in json.loads(CONTRACT.read_text())["rows"]}
    row = rows.get("wedo.rotation")
    if row is None:
        return {"verdict": "NO ROW", "fails": ["wedo.rotation is not in the contract"]}
    no_consecutive = row["value"]["noConsecutiveSameType"]
    min_distinct = row["value"]["minDistinctTypesPerSixLessons"]
    fails = []
    if no_consecutive:
        for a, b in zip(sequence, sequence[1:]):
            if a == b:
                fails.append(f"wedo.rotation: two consecutive lessons both use '{a}'")
                break
    for start in range(0, max(1, len(sequence) - 5)):
        window = sequence[start:start + 6]
        if len(window) == 6 and len(set(window)) < min_distinct:
            fails.append(f"wedo.rotation: lessons {start+1}-{start+6} show "
                         f"{len(set(window))} types, fewer than {min_distinct}")
            break
    return {"verdict": "PASS" if not fails else "RED", "fails": fails}


_WEDO_SHELL = """<!doctype html><html><head><style>
.slide{display:none}.slide.active{display:flex}#print-area{display:none}
@media print{#print-area{display:block!important}}
</style></head><body>
<main id="lessonDeck" class="deck"><div class="slide-container">
  <div class="slide active" data-title="I Do"><p>Watch me do it.</p></div>
  <div class="slide" data-title="We Do 1"><p>__T1__</p></div>
  <div class="slide" data-title="We Do 2"><p>__T2__</p></div>
</div></main>
<div id="print-area"><div class="print-section"><p>__T1__</p></div></div>
<script>var meta = {"weDoType": "__D__"};</script>
</body></html>"""

_TEXT = {
    "sort-or-match":     "Sort the cards into two groups and match each pair.",
    "sequence-or-rank":  "Rank the cards and put them in order along the timeline.",
    "commit-and-reveal": "Show me on your whiteboard, everyone commits, then hold up your answer.",
    "predict-then-check": "Predict what will happen, then check it.",
    "label-or-annotate": "Label the diagram and annotate what you see.",
    "spot-the-error":    "Spot the mistake and correct the sentence.",
}


def _measure_html(source: str) -> dict:
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as fh:
        fh.write(source)
        name = fh.name
    try:
        m = measure(Path(name))
        m["declaredType"] = declared_type(Path(name))
        return m
    finally:
        Path(name).unlink(missing_ok=True)


def _deck(declared, t1, t2):
    return (_WEDO_SHELL.replace("__T1__", _TEXT[t1]).replace("__T2__", _TEXT[t2])
            .replace("__D__", declared))


CONTROL_IDS = [
    "classic-shell-we-do-stages-are-found",
    "print-pack-copy-is-not-a-second-we-do-stage",
    "declared-type-uncorroborated-reds",
    "declared-type-corroborated-passes",
    "undeclared-type-reds",
    "same-type-three-times-fires",
    "rotated-types-pass",
    "six-lessons-under-four-types-fires",
]


def controls() -> list[dict]:
    out = []

    def rec(cid, description, expected, observed):
        out.append({"id": cid, "description": description, "expected": expected,
                    "observed": observed, "fired": expected == observed})

    types, _ = taxonomy()

    m = _measure_html(_deck("sort-or-match", "sort-or-match", "sequence-or-rank"))
    rec("classic-shell-we-do-stages-are-found",
        "a classic-shell deck's two We Do stages are found (they used to read as zero)",
        2, m["weDoStages"])

    rec("print-pack-copy-is-not-a-second-we-do-stage",
        "the print pack re-prints We Do 1 and must not add a third stage",
        2, m["weDoStages"])

    rec("declared-type-corroborated-passes",
        "a deck whose We Do text evidences its declared type passes",
        "PASS", judge(m, types)["verdict"])

    bad = _measure_html(_deck("spot-the-error", "sort-or-match", "sequence-or-rank"))
    rec("declared-type-uncorroborated-reds",
        "a deck declaring spot-the-error over sorting and ranking text reds",
        "RED", judge(bad, types)["verdict"])

    none = _measure_html(_deck("sort-or-match", "sort-or-match", "sequence-or-rank")
                         .replace('var meta = {"weDoType": "sort-or-match"};', "var meta = {};"))
    rec("undeclared-type-reds",
        "a deck declaring no we-do type reds",
        "RED", judge(none, types)["verdict"])

    rec("same-type-three-times-fires",
        "three consecutive lessons of one type breaks wedo.rotation",
        "RED", rotation_verdict(["sort-or-match"] * 3)["verdict"])

    rotated = ["sort-or-match", "sequence-or-rank", "commit-and-reveal",
               "predict-then-check", "label-or-annotate", "spot-the-error"]
    rec("rotated-types-pass",
        "six lessons rotating six distinct types passes wedo.rotation",
        "PASS", rotation_verdict(rotated)["verdict"])

    thin = ["sort-or-match", "sequence-or-rank", "sort-or-match",
            "sequence-or-rank", "sort-or-match", "sequence-or-rank"]
    rec("six-lessons-under-four-types-fires",
        "six lessons alternating only two types breaks the >=4-in-6 limb",
        "RED", rotation_verdict(thin)["verdict"])

    return out


def self_test() -> dict:
    results = controls()
    ids = [r["id"] for r in results]
    missing = [c for c in CONTROL_IDS if c not in ids]
    extra = [c for c in ids if c not in CONTROL_IDS]
    return {"tool": "g25_wedo_variety", "toolVersion": VERSION,
            "file": "_sownb/vb/tools/g25_wedo_variety.py",
            "controlsDeclared": len(CONTROL_IDS), "controlsRun": len(results),
            "controlsFired": sum(1 for r in results if r["fired"]),
            "missingControls": missing, "undeclaredControls": extra,
            "allListedControlsFired": not missing and not extra and all(r["fired"] for r in results),
            "controls": results}


if __name__ == "__main__":
    if "--list-controls" in sys.argv:
        for c in CONTROL_IDS:
            print(c)
        raise SystemExit(0)
    if "--self-test" in sys.argv:
        report = self_test()
        print(f"g25 self-test  [{VERSION}]")
        for r in report["controls"]:
            print(f"  {'ok  ' if r['fired'] else 'FAIL'} {r['id']:46s} "
                  f"expected={r['expected']} observed={r['observed']}")
        print(f"{report['controlsFired']}/{report['controlsRun']} controls fired")
        print("PASS" if report["allListedControlsFired"] else "MEASUREMENT INVALID")
        raise SystemExit(0 if report["allListedControlsFired"] else 1)

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
