#!/usr/bin/env python3
"""g26 — pupil-text reading level within the pathway band. Order VB run 8 §3.1(d).

Measures Flesch-Kincaid on PUPIL-ADDRESSEE text only. The addressee key is the
estate's own: data-mbm-guide (and data-audience="staff") mark adult-facing text.
Run 6's I5 addressee map is not in this repository, so the selector is derived
from the tree rather than pinned to a name that does not exist here.

Whole-deck FK is printed beside pupil FK on every row, because the difference
between them is itself the finding when a deck mixes addressees.
"""
from __future__ import annotations
import copy, json, re, sys, hashlib
from pathlib import Path
import lxml.html as LH

VERSION = "g26-v1.0.0-pathway-reading-band"
ROOT = Path(__file__).resolve().parents[3]
CONTRACT = ROOT / "_sownb/STYLE_CONTRACT.json"
VOWELS = "aeiouy"


def syllables(w: str) -> int:
    w = w.lower().strip("'")
    if not w:
        return 1
    n, prev = 0, False
    for ch in w:
        v = ch in VOWELS
        if v and not prev:
            n += 1
        prev = v
    if w.endswith("e") and n > 1:
        n -= 1
    return max(1, n)


def fk(text: str):
    words = re.findall(r"[A-Za-z']+", text)
    sents = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    if not words or not sents:
        return None, 0, 0
    syl = sum(syllables(w) for w in words)
    return 0.39 * len(words) / len(sents) + 11.8 * syl / len(words) - 15.59, len(words), len(sents)


def measure(path: Path) -> dict:
    tree = LH.fromstring(path.read_text(encoding="utf-8"))
    main = tree.xpath('//main[@id="lessonDeck"]') or tree.xpath(
        '//main[contains(concat(" ",normalize-space(@class)," ")," deck ")]')
    if not main:
        return {"file": str(path), "error": "no deck"}
    def strip(node, staff_too):
        n = copy.deepcopy(node)
        sel = './/script|.//style|.//svg'
        if staff_too:
            sel += '|.//*[@data-mbm-guide]|.//*[@data-audience="staff"]'
        for bad in n.xpath(sel):
            bad.getparent().remove(bad)
        return " ".join(n.text_content().split())
    whole, pupil = strip(main[0], False), strip(main[0], True)
    fw, ww, sw = fk(whole)
    fu, wu, su = fk(pupil)
    return {"file": str(path.relative_to(ROOT)), "toolVersion": VERSION,
            "wholeDeckFK": None if fw is None else round(fw, 2), "wholeWords": ww,
            "pupilFK": None if fu is None else round(fu, 2), "pupilWords": wu, "pupilSentences": su}


def bands():
    rows = {r["id"]: r for r in json.loads(CONTRACT.read_text())["rows"]}
    row = rows.get("reading.pathway.band")
    if row is None:
        return None, False
    return row["value"]["bands"], row.get("scope") == "new"


def pathway_of(rel: str) -> str | None:
    u = rel.upper()
    for p in ("BUILD", "GROW", "LAUNCH"):
        if f"/{p}_" in u or f"/{p}/" in u or u.startswith(p + "_"):
            return p
    return None


def judge(m: dict, bnds: dict, pathway: str) -> dict:
    fails = []
    if pathway is None or pathway not in bnds:
        return {"fails": ["g26: pathway not derivable from the path"], "verdict": "NOT-APPLICABLE"}
    lo, hi = bnds[pathway]
    v = m.get("pupilFK")
    if v is None:
        fails.append("g26: no pupil-addressee text to measure")
    elif not (lo <= v <= hi):
        fails.append(f"g26: pupil FK {v} outside the {pathway} band {lo}-{hi}")
    return {"fails": fails, "verdict": "PASS" if not fails else "RED"}


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    scope = "new" if "--scope=new" in sys.argv else "live"
    bnds, scoped_new = bands()
    binding = scope == "new" and scoped_new
    sha = hashlib.sha256(CONTRACT.read_bytes()).hexdigest()
    red = 0
    out = []
    for a in args:
        p = Path(a) if Path(a).is_absolute() else ROOT / a
        m = measure(p)
        pw = pathway_of(str(p.relative_to(ROOT)) if str(p).startswith(str(ROOT)) else a)
        j = judge(m, bnds or {}, pw)
        m.update({"pathway": pw, "scope": scope, "binding": binding, "contractSha256": sha, **j})
        if binding and j["verdict"] == "RED":
            red += 1
        out.append(m)
        band = f"{bnds[pw][0]}-{bnds[pw][1]}" if bnds and pw in bnds else "n/a"
        print(f"{p.name[:46]:46s} pathway={pw or '?':6s} whole={m.get('wholeDeckFK')} "
              f"pupil={m.get('pupilFK')} band={band} {j['verdict']:4s} "
              f"{'BINDING' if binding else 'report-only'} contract {sha[:8]} [{VERSION}]")
        for f in j["fails"]:
            print(f"    {f}")
    Path("/tmp/g26_last.json").write_text(json.dumps(out, indent=1))
    sys.exit(1 if red else 0)
