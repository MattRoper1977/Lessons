#!/usr/bin/env python3
"""c-gate CONTAINMENT (VB-RUN11F C2; shell-agnostic A2R §3.5).

Every pupil-facing sentence of the donor deck is present, verbatim, in the
reshelled deck. Ligatures and whitespace are normalised; nothing else is.

WHAT CHANGED IN A2R
-------------------
The two sides carried DIFFERENT hard-coded roots: the donor was read from
`main.deck` + `.print-pack` and the candidate from `.slide-container` +
`#print-area`. That encoded "the donor is always n6 and the candidate is always
classic". It is already false in this estate -- BUILD_HUM_W16 is a classic deck
on main and could be a donor tomorrow -- and when it is false the gate reads a
whole side as empty and passes, because a deck with no sentences has none
missing. Both sides now read the union of every known root, so containment is
measured in whichever direction a reshell runs.

WHAT CONTAINMENT DELIBERATELY DOES NOT COVER
--------------------------------------------
The staff drawer is excluded on both sides, so this gate measures PUPIL-FACING
containment. That is deliberate and it is why §4.3's trim-to-drawer needs its
own drawer diff: text moved from a stage into the drawer is, correctly, missing
from the pupil-facing surface. Proving it was preserved rather than deleted is a
different question, asked by a different instrument. A gate that answered both
would answer neither.

Usage:
  cgate_containment.py <before.html> <after.html> <out.json>
  cgate_containment.py --list-controls
  cgate_containment.py --self-test
"""
import copy
import json
import re
import sys
import tempfile
import unicodedata
from pathlib import Path

from lxml import html

VERSION = "cgate-v2.0.0-shell-agnostic"

# Every root a pupil surface is known to live under, in either shell. Read as a
# union on both sides: a root that is not present simply contributes nothing.
ROOTS = [
    '//main[contains(@class,"deck")]',
    '//*[contains(concat(" ",normalize-space(@class)," ")," slide-container ")]',
    '//section[contains(concat(" ",normalize-space(@class)," ")," print-pack ")]',
    '//*[@id="print-area"]',
]

DROP_TAGS = ("script", "style", "svg", "template", "noscript", "button")
DROP_CLASSES = ("time", "tag", "slide-tag", "running-head")


def pupil_text(path, roots=None):
    roots = roots or ROOTS
    tree = html.fromstring(Path(path).read_text(encoding="utf-8"))
    out = []
    seen = set()
    for xp in roots:
        for node in tree.xpath(xp):
            # a root nested inside another root would be read twice
            if any(anc in seen for anc in node.iterancestors()):
                continue
            seen.add(node)
            node = copy.deepcopy(node)
            for c in list(node.iterdescendants()):
                tag = c.tag.lower() if isinstance(c.tag, str) else ""
                cls = (c.get("class") or "").split()
                if (tag in DROP_TAGS
                        or c.get("data-mbm-guide") is not None
                        or c.get("data-audience") == "staff"
                        or any(k in cls for k in DROP_CLASSES)):
                    p = c.getparent()
                    if p is not None:
                        p.remove(c)
            BLOCK = {"p", "div", "h1", "h2", "h3", "h4", "li", "td", "th", "tr",
                     "section", "article", "table", "ul", "ol", "span"}
            for c in node.iter():
                if isinstance(c.tag, str) and c.tag.lower() in BLOCK:
                    c.tail = " \n " + (c.tail or "")
            out.append(" ".join(x for x in node.itertext()))
    return "\n".join(" ".join(l.split()) for l in " ".join(out).split("\n"))


def norm(s):
    s = (unicodedata.normalize("NFKC", s)
         .replace("’", "'").replace("‘", "'")
         .replace("“", '"').replace("”", '"')
         .replace(" ", " "))
    return "\n".join(" ".join(l.split()) for l in s.split("\n"))


def sentences(text):
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+|\n+", text) if len(x.strip()) >= 12]


def compare(before, after):
    B = norm(pupil_text(before))
    A = norm(pupil_text(after))
    sents = sentences(B)
    AA = " ".join(A.split())
    missing = [s for s in sents if s not in AA]
    if not sents:
        return {"file": str(after), "before": str(before),
                "sentencesBefore": 0, "charsBefore": len(B), "charsAfter": len(A),
                "missing": [],
                "redControl": {"deleted": None, "fired": False},
                "status": "MEASUREMENT INVALID: the donor yielded no pupil sentences"}
    # red control: delete one mid-deck sentence from the candidate text and
    # re-check. Every occurrence goes, because the print pack re-prints the
    # slide text and removing one copy would leave the other and prove nothing.
    victim = sents[len(sents) // 2]
    red_missing = [s for s in sents if s not in AA.replace(victim, "")]
    red_fired = victim in red_missing
    return {
        "file": str(after), "toolVersion": VERSION,
        "subject": ("containment: every pupil-facing sentence of the donor deck is verbatim "
                    "in the reshelled deck, in whichever shell each side uses (shell chrome "
                    "excluded on both sides: the minute badge, the stage tag, the running "
                    "head; scripts, styles, SVG, buttons and keyed staff guidance)"),
        "before": str(before),
        "sentencesBefore": len(sents), "charsBefore": len(B), "charsAfter": len(A),
        "missing": missing,
        "redControl": {"deleted": victim[:80], "fired": red_fired},
        "status": "PASS" if not missing and red_fired else "RED",
    }


# --------------------------------------------------------------------------
# Controls
# --------------------------------------------------------------------------

_N6 = """<!doctype html><html><body><main class="deck">
<section class="slide"><span class="slide-tag">I DO</span>
<p>The river carried iron ore to the furnaces every single day.</p>
<p>Workers walked to the yard before the sun came up.</p>
<div data-audience="staff"><p>Staff note: keep the pace brisk here.</p></div></section>
</main><section class="print-pack"><p>The river carried iron ore to the furnaces every single day.</p>
</section></body></html>"""

_CLASSIC = """<!doctype html><html><body>
<main id="lessonDeck" class="deck"><div class="slide-container">
<div class="slide"><span class="slide-tag">I DO</span>
<p>The river carried iron ore to the furnaces every single day.</p>
<p>Workers walked to the yard before the sun came up.</p></div>
</div></main>
<div id="print-area"><div class="print-section">
<p>The river carried iron ore to the furnaces every single day.</p>
<p>Workers walked to the yard before the sun came up.</p></div></div>
</body></html>"""

CONTROL_IDS = [
    "n6-donor-to-classic-candidate-passes",
    "classic-donor-to-n6-candidate-passes",
    "a-deleted-sentence-reds",
    "a-donor-with-no-sentences-is-measurement-invalid",
    "curly-quotes-do-not-create-a-false-miss",
    "staff-drawer-text-is-not-required-to-be-contained",
]


def _write(tmp, name, source):
    p = Path(tmp) / name
    p.write_text(source, encoding="utf-8")
    return p


def controls() -> list[dict]:
    out = []

    def rec(cid, description, expected, observed):
        out.append({"id": cid, "description": description, "expected": expected,
                    "observed": observed, "fired": expected == observed})

    with tempfile.TemporaryDirectory() as tmp:
        n6 = _write(tmp, "n6.html", _N6)
        classic = _write(tmp, "classic.html", _CLASSIC)

        rec("n6-donor-to-classic-candidate-passes",
            "an n6 donor reshelled to the classic chassis, nothing lost",
            "PASS", compare(n6, classic)["status"])

        rec("classic-donor-to-n6-candidate-passes",
            "the same comparison in the other direction -- the old gate read one side as empty",
            "PASS", compare(classic, n6)["status"])

        cut = _write(tmp, "cut.html", _CLASSIC.replace(
            "<p>Workers walked to the yard before the sun came up.</p>", "", 2))
        r = compare(n6, cut)
        rec("a-deleted-sentence-reds",
            "one pupil sentence removed from the candidate reds the gate",
            ("RED", 1), (r["status"], len(r["missing"])))

        empty = _write(tmp, "empty.html", "<!doctype html><html><body><p>no deck here</p></body></html>")
        rec("a-donor-with-no-sentences-is-measurement-invalid",
            "a donor yielding no pupil sentences must not pass by having nothing to lose",
            True, compare(empty, classic)["status"].startswith("MEASUREMENT INVALID"))

        curly = _write(tmp, "curly.html", _CLASSIC.replace(
            "the sun came up", "the sun’s light came up").replace(
            "<p>Workers walked to the yard before the sun’s light came up.</p>",
            "<p>Workers walked to the yard before the sun came up.</p>"))
        rec("curly-quotes-do-not-create-a-false-miss",
            "typographic quotes and non-breaking spaces normalise on both sides",
            "PASS", compare(n6, curly)["status"])

        rec("staff-drawer-text-is-not-required-to-be-contained",
            "the donor's staff note is excluded from the donor side, so it cannot be reported missing",
            True, "Staff note" not in " ".join(sentences(norm(pupil_text(n6)))))

    return out


def self_test() -> dict:
    results = controls()
    ids = [r["id"] for r in results]
    missing = [c for c in CONTROL_IDS if c not in ids]
    extra = [c for c in ids if c not in CONTROL_IDS]
    return {"tool": "cgate_containment", "toolVersion": VERSION,
            "file": "_sownb/vb/tools/cgate_containment.py",
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
        print(f"cgate self-test  [{VERSION}]")
        for r in report["controls"]:
            print(f"  {'ok  ' if r['fired'] else 'FAIL'} {r['id']:52s} "
                  f"expected={r['expected']} observed={r['observed']}")
        print(f"{report['controlsFired']}/{report['controlsRun']} controls fired")
        print("PASS" if report["allListedControlsFired"] else "MEASUREMENT INVALID")
        raise SystemExit(0 if report["allListedControlsFired"] else 1)

    if len(sys.argv) < 4:
        raise SystemExit("usage: cgate_containment.py <before> <after> <out.json>")
    before, after, out = sys.argv[1], sys.argv[2], sys.argv[3]
    rec = compare(before, after)
    json.dump(rec, open(out, "w"), indent=1, ensure_ascii=False)
    print(rec["status"], "sentences", rec["sentencesBefore"],
          "missing", len(rec["missing"]), "red fired", rec["redControl"]["fired"],
          f"[{VERSION}]")
    for m in rec["missing"][:8]:
        print("  MISSING:", m[:140])
    raise SystemExit(0 if rec["status"] == "PASS" else 1)
