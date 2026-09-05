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

VERSION = "g26-v1.2.0-block-boundary-aware-extraction"
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


# A browser puts a box boundary between two block-level elements, and every
# screen reader reads them as separate runs. lxml's text_content() does not: it
# concatenates, so `<h3>0 min</h3><span>GROW Art</span>` becomes "0 minGROW Art"
# and Flesch-Kincaid then scores "minGROW" as one long word. On a minified deck
# that inflates syllables-per-word enough to move the verdict - it is what put
# Silver W7 at 7.01 against a ceiling of 7.0, where the same deck pretty-printed
# measures 6.19. Joining at the boundary is not a relaxation; it is measuring the
# text the reader actually meets.
BLOCKISH = {"p", "div", "section", "article", "h1", "h2", "h3", "h4", "h5", "h6",
            "li", "ul", "ol", "td", "th", "tr", "table", "main", "header", "footer",
            "span", "figcaption", "figure", "button", "summary", "details", "br", "label"}


def visible_text(node) -> str:
    """text_content(), but with a space wherever the rendered box would break."""
    parts = []

    def walk(n):
        if not isinstance(n.tag, str) or n.tag.lower() in ("script", "style", "svg"):
            if n.tail:
                parts.append(n.tail)
            return
        if n.text:
            parts.append(n.text)
        for child in n:
            walk(child)
            if child.tail:
                parts.append(child.tail)
        if n.tag.lower() in BLOCKISH:
            parts.append(" ")

    walk(node)
    return " ".join("".join(parts).split())


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
        return visible_text(n)
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


def controls() -> list[dict]:
    """g26's own controls. Each states what it expects and what it observed, so a
    control that stops discriminating is visible rather than quietly green."""
    rows = []

    def row(cid, expected, actual):
        rows.append({"id": cid, "expected": expected, "actual": actual,
                     "fired": expected == actual})

    frag = LH.fromstring('<main class="deck"><h3>0 min</h3><span>GROW Art</span></main>')
    row("blockBoundaryIsAWordBoundary", "0 min GROW Art", visible_text(frag))

    # The bug this gate shipped with, pinned so it cannot come back.
    row("concatenatedPseudoWordIsNotProduced", False, "minGROW" in visible_text(frag))

    # Inline tails must survive the boundary insertion - dropping them would
    # lower the word count and flatter every deck.
    tail = LH.fromstring('<main class="deck"><p>keep <b>this</b> tail</p></main>')
    row("inlineTailTextSurvives", "keep this tail", visible_text(tail))

    # A boundary must not be invented inside a run of plain prose.
    plain = LH.fromstring('<main class="deck"><p>one two three</p></main>')
    row("plainProseIsUnchanged", "one two three", visible_text(plain))

    # NEGATIVE control: the extraction must not silently swallow staff text -
    # excluding it is measure()'s job, not visible_text()'s, and conflating the
    # two would hide an addressee bug inside a whitespace fix.
    staff = LH.fromstring('<main class="deck"><p data-mbm-guide="1">adult</p></main>')
    row("visibleTextDoesNotItselfDropStaffText", "adult", visible_text(staff))

    # The arithmetic still discriminates: a harder sentence must score higher.
    easy = fk("The cat sat. The dog ran.")[0]
    hard = fk("Consequently, the extraordinary categorisation demonstrated "
              "considerable methodological inconsistency.")[0]
    row("harderProseScoresHigher", True, bool(hard is not None and easy is not None and hard > easy))

    return rows


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    scope = "new" if "--scope=new" in sys.argv else "live"
    if "--list-controls" in sys.argv:
        print("\n".join(c["id"] for c in controls()))
        sys.exit(0)
    if "--self-test" in sys.argv:
        rows = controls()
        for c in rows:
            print(f"  {'ok  ' if c['fired'] else 'FAIL'} {c['id']:44s} "
                  f"expected={c['expected']!r} observed={c['actual']!r}")
        fired = sum(1 for c in rows if c["fired"])
        print(f"{fired}/{len(rows)} controls fired")
        print("PASS" if fired == len(rows) else "MEASUREMENT INVALID")
        sys.exit(0 if fired == len(rows) else 1)
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
