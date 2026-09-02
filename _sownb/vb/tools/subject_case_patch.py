#!/usr/bin/env python3
"""R2.3 — mid-sentence Title-Case subject terms to house case (ORDER VB-RUN14).

"A capitalisation defect wearing a name-detection costume: 'Natural Selection'
mid-sentence looks like a person because it is Title-Cased mid-sentence. Fix at
source, not in the detector."

WHAT IT TOUCHES. Text nodes only, in pupil-facing body content, where a
register term appears Title-Cased and is NOT at the start of a sentence.

WHAT IT NEVER TOUCHES, and how each is guaranteed:
  sentence starts      the character run before the match must not end in
                       . ! ? or be the start of the text node
  headings             h1-h6, title, th, figcaption, and any element with a
                       class containing "tag" or "label", are skipped whole
  NAMED-AFTER rows     not in the house-case map at all
  code and paths       script, style, code, pre, kbd, samp, and any attribute
                       value; only text nodes are read
  staff guidance       [data-mbm-guide], [data-audience=staff],
                       [data-addressee=staff] subtrees are skipped whole
  the print pack       included: it is pupil-facing

The register is _sownb/SUBJECT_TERMS.md; the house-case map is read from the
"->" lines in it, so the file is the single source. Output is a byte diff of the
deck, and the containment rule (every changed line must match the term pattern)
is checked by containment_check() and reported alongside.

Usage: subject_case_patch.py <deck> [<deck> ...] [--dry-run] [--json <out>]
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

from lxml import html as lh

ROOT = Path(__file__).resolve().parents[3]
REGISTER = ROOT / "_sownb/SUBJECT_TERMS.md"
SKIP_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "title", "th", "figcaption", "script", "style", "code", "pre", "kbd", "samp", "svg"}
SKIP_ATTR = ("data-mbm-guide", "data-audience", "data-addressee")


def house_case_map() -> dict[str, str]:
    out = {}
    for line in REGISTER.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s+(.+?)\s+->\s+(.+?)\s*$", line)
        if m:
            out[m.group(1).strip()] = m.group(2).strip()
    return out


def skip(el) -> bool:
    if el.tag in SKIP_TAGS:
        return True
    cls = (el.get("class") or "").lower()
    if "tag" in cls.split() or "label" in cls or "slide-tag" in cls:
        return True
    return any(el.get(a) is not None and (a == "data-mbm-guide" or el.get(a) == "staff") for a in SKIP_ATTR)


def patch_text(text: str, mapping: dict[str, str]) -> tuple[str, int]:
    n = 0
    for tc, hc in mapping.items():
        pat = re.compile(r"(?<!^)(?<![.!?]\s)(?<![.!?]\s\s)\b" + re.escape(tc) + r"\b")
        def rep(m):
            nonlocal n
            before = text[: m.start()]
            after = text[m.end():]
            if not before.strip() or re.search(r"[.!?][\"')\]]?\s*$", before):
                return m.group(0)
            # A Title-Case run is a title, not a sentence: "Solar System Presentation"
            # in a next-lesson link keeps its case, as does anything after a
            # breadcrumb dot ("Next · W10B · Solar System ...").
            if re.match(r"\s+[A-Z][a-z]", after) or re.search(r"[·|>]\s*$", before):
                return m.group(0)
            n += 1
            return hc
        text = pat.sub(rep, text)
    return text, n


def patch_deck(path: Path, mapping: dict[str, str]) -> tuple[str, int]:
    """One pass over the raw bytes: text runs between tags are patched, tags are
    never touched, and skipped subtrees are tracked with a tag stack. A single
    mechanism produces both the count and the output, so the two can never
    disagree -- the first version walked the DOM to count and spliced the source
    to write, and reported four occurrences with zero changed lines."""
    src = path.read_text(encoding="utf-8")
    pieces = re.split(r"(<[^>]+>)", src)
    stack: list[bool] = []
    in_skip = 0
    changed = 0
    VOID = {"br", "hr", "img", "input", "meta", "link", "source", "wbr", "col", "area", "base", "embed", "param", "track"}
    in_body = False
    for i, piece in enumerate(pieces):
        if piece.startswith("<"):
            m = re.match(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)", piece)
            if not m:
                continue
            closing, tag = m.group(1), m.group(2).lower()
            if tag == "body" and not closing:
                in_body = True
            if closing:
                if stack:
                    in_skip -= stack.pop()
                continue
            if tag in VOID or piece.endswith("/>"):
                continue
            is_skip = (tag in SKIP_TAGS
                       or bool(re.search(r'class="[^"]*\b(slide-tag|tag|label)\b', piece))
                       or "data-mbm-guide" in piece
                       or bool(re.search(r'data-(audience|addressee)="staff"', piece)))
            stack.append(is_skip)
            in_skip += is_skip
        elif in_body and in_skip == 0 and piece.strip():
            new, n = patch_text(piece, mapping)
            if n:
                pieces[i] = new
                changed += n
    return "".join(pieces), changed


def containment_check(before: str, after: str, mapping: dict[str, str]) -> dict:
    diff = list(difflib.unified_diff(before.splitlines(), after.splitlines(), lineterm="", n=0))
    changed = [l for l in diff if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]
    terms = [re.escape(t) for t in mapping] + [re.escape(v) for v in mapping.values()]
    pat = re.compile("|".join(terms)) if terms else re.compile(r"$^")
    stray = [l[:120] for l in changed if not pat.search(l)]
    return {"changedLines": len(changed), "strayLines": stray, "contained": not stray}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("decks", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--json")
    args = ap.parse_args()
    mapping = house_case_map()
    report = {"file": "_sownb/SUBJECT_TERMS.md", "subject": "R2.3 subject-term case patch, mid-sentence only", "houseCaseMap": mapping, "decks": []}
    ok = True
    for d in args.decks:
        p = ROOT / d if not Path(d).is_absolute() else Path(d)
        before = p.read_text(encoding="utf-8")
        after, n = patch_deck(p, mapping)
        cont = containment_check(before, after, mapping)
        row = {"deck": d, "occurrencesPatched": n, "bytesBefore": len(before.encode()), "bytesAfter": len(after.encode()), **cont}
        if not cont["contained"]:
            ok = False; row["status"] = "STOP — a changed line does not match the term pattern"
        else:
            row["status"] = "PASS"
            if n and not args.dry_run:
                p.write_text(after, encoding="utf-8")
        report["decks"].append(row)
        print(f"  {row['status'][:4]:4s} patched={n:3d} changedLines={cont['changedLines']:3d} stray={len(cont['strayLines'])}  {d[-60:]}")
    report["status"] = "PASS" if ok else "STOP"
    if args.json:
        out = ROOT / args.json if not Path(args.json).is_absolute() else Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
