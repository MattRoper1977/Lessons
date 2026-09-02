#!/usr/bin/env python3
"""g26 — pupil-text reading level within the pathway band. Order VB run 8 §3.1(d).

Measures Flesch-Kincaid on PUPIL-ADDRESSEE text only. The addressee key is the
estate's own: data-mbm-guide (and data-audience="staff") mark adult-facing text.
Run 6's I5 addressee map is not in this repository, so the selector is derived
from the tree rather than pinned to a name that does not exist here.

Whole-deck FK is printed beside pupil FK on every row, because the difference
between them is itself the finding when a deck mixes addressees.

Matt's ruling of 2026-09-02 (VB-RUN10 D-J) made LAUNCH CEILING-ONLY: a LAUNCH
lesson that reads more simply than the live pack is not a defect, so only the
upper bound binds there. The floor is still measured and still printed - it is
withdrawn as a failure condition, not as a number. Which bound binds is read
from the contract row's bindingMode, so changing the ruling is a contract edit,
not a code edit.
"""
from __future__ import annotations
import copy, json, re, sys, hashlib
from pathlib import Path
import lxml.html as LH

VERSION = "g26-v1.1.0-pathway-reading-band-launch-ceiling-only"
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
    return row["value"]["bands"], row.get("scope") == "new", row["value"].get("bindingMode", {})


def pathway_of(rel: str) -> str | None:
    u = rel.upper()
    for p in ("BUILD", "GROW", "LAUNCH"):
        if f"/{p}_" in u or f"/{p}/" in u or u.startswith(p + "_"):
            return p
    return None


def judge(m: dict, bnds: dict, pathway: str, modes: dict | None = None) -> dict:
    fails = []
    if pathway is None or pathway not in bnds:
        return {"fails": ["g26: pathway not derivable from the path"], "verdict": "NOT-APPLICABLE"}
    lo, hi = bnds[pathway]
    mode = (modes or {}).get(pathway, "band")
    v = m.get("pupilFK")
    if v is None:
        fails.append("g26: no pupil-addressee text to measure")
    elif mode == "ceiling":
        # D-J: the floor is measured and printed, never failed.
        if v > hi:
            fails.append(f"g26: pupil FK {v} above the {pathway} ceiling {hi}")
    elif not (lo <= v <= hi):
        fails.append(f"g26: pupil FK {v} outside the {pathway} band {lo}-{hi}")
    return {"fails": fails, "verdict": "PASS" if not fails else "RED",
            "bindingMode": mode,
            "belowWithdrawnFloor": bool(v is not None and mode == "ceiling" and v < lo)}


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    scope = "new" if "--scope=new" in sys.argv else "live"
    bnds, scoped_new, modes = bands()
    binding = scope == "new" and scoped_new
    sha = hashlib.sha256(CONTRACT.read_bytes()).hexdigest()
    red = 0
    out = []
    for a in args:
        p = Path(a) if Path(a).is_absolute() else ROOT / a
        m = measure(p)
        pw = pathway_of(str(p.relative_to(ROOT)) if str(p).startswith(str(ROOT)) else a)
        j = judge(m, bnds or {}, pw, modes)
        m.update({"pathway": pw, "scope": scope, "binding": binding, "contractSha256": sha, **j})
        if binding and j["verdict"] == "RED":
            red += 1
        out.append(m)
        if bnds and pw in bnds:
            band = (f"<={bnds[pw][1]}" if modes.get(pw) == "ceiling"
                    else f"{bnds[pw][0]}-{bnds[pw][1]}")
        else:
            band = "n/a"
        print(f"{p.name[:46]:46s} pathway={pw or '?':6s} whole={m.get('wholeDeckFK')} "
              f"pupil={m.get('pupilFK')} band={band} {j['verdict']:4s} "
              f"{'BINDING' if binding else 'report-only'} contract {sha[:8]} [{VERSION}]")
        for f in j["fails"]:
            print(f"    {f}")
    Path("/tmp/g26_last.json").write_text(json.dumps(out, indent=1))
    sys.exit(1 if red else 0)
