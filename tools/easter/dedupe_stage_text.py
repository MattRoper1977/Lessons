#!/usr/bin/env python3
"""Remove verbatim sentence repeats from WITHIN a single pupil paragraph.

WHY THIS IS NOT A TRIM
----------------------
ORDER VB-EASTER-A3 §0c asks for a TRIM-TO-DRAWER on decks over the 1.25 ratio.
Before trimming anything it is worth knowing what the words ARE. In three of the
six over-ratio decks the excess is not authored teaching, it is the same
instruction block printed several times inside one paragraph:

    BUILD_HUM_W15  stage 6  one <p> of 517 words = one block printed 4x
    GROW_HUM_W15   stage 6  798 duplicated words in one <p>
    LAUNCH_HUM_W15 stage 6  810 duplicated words in one <p>

Moving a duplicate copy of a sentence into the staff drawer would be absurd: the
drawer would hold a second copy of a sentence the pupil still reads once. So the
duplicate is deleted, and nothing is lost, because the sentence remains in the
lesson exactly where it was the first time. That is why this tool exists as a
step BEFORE the trim, not as part of it.

WHAT IT WILL NOT TOUCH, AND WHY
-------------------------------
  ACROSS-PARAGRAPH REPEATS. A sentence repeated in two different paragraphs, or
  on two different stages, is left alone. Some of those are deliberate and
  load-bearing: GROW_HUM_W15 repeats "No learner has to disclose a personal
  belief, protest experience, family history, identity, hardship..." on six
  consecutive stages, and a safeguarding line SHOULD appear wherever the pupil
  is working. This tool cannot tell a deliberate refrain from a bug, so it does
  not try; it only removes repeats inside one paragraph, where no pedagogy puts
  them.

  ELEMENTS CARRYING INLINE MARKUP. If the paragraph has child elements, editing
  its text by string surgery would destroy the markup. Those are REFUSED and
  reported, never silently edited. In practice this spares the "Truth boundary"
  block, whose repeats are safeguarding statements.

  THE STAFF DRAWER AND THE PRINT PACK. Stage discovery comes from lesson_stages,
  which excludes both.

HOW THE EDIT IS MADE SAFE
-------------------------
Every target element is pure text with no children, so the edit is an exact
replacement of that element's text in the raw file, asserted to match exactly
once. Everything else in the file is byte-identical afterwards. The tool then
re-parses and requires that the set of distinct pupil sentences is unchanged --
a deletion that loses a sentence is a failure, not a trim.

Usage:
  dedupe_stage_text.py <deck.html> [...] [--apply] [--output report.json]
  dedupe_stage_text.py --list-controls
  dedupe_stage_text.py --self-test
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERSION = "dedupe-stage-text-v1.0.0"

_ls = importlib.util.spec_from_file_location(
    "lesson_stages", ROOT / "_sownb/vb/tools/lesson_stages.py")
ls = importlib.util.module_from_spec(_ls)
_ls.loader.exec_module(ls)

BLOCK = ("p", "li", "td")
MIN_SENTENCE_WORDS = 4


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text)
            if len(s.strip().split()) >= MIN_SENTENCE_WORDS]


def dedupe_text(text: str) -> tuple[str, int]:
    """Keep the first occurrence of each sentence, drop later verbatim repeats."""
    parts = re.split(r"(?<=[.!?])(\s+)", text)
    out, seen, removed = [], set(), 0
    i = 0
    while i < len(parts):
        chunk = parts[i]
        sep = parts[i + 1] if i + 1 < len(parts) else ""
        key = chunk.strip()
        if len(key.split()) >= MIN_SENTENCE_WORDS:
            if key in seen:
                removed += len(key.split())
                i += 2
                continue
            seen.add(key)
        out.append(chunk)
        if sep:
            out.append(sep)
        i += 2
    return "".join(out).strip(), removed


def analyse(path: Path) -> dict:
    raw = Path(path).read_text(encoding="utf-8")
    tree = ls.parse(Path(path))
    screen = ls.ScreenView(tree)
    targets, refused = [], []
    for index, stage in enumerate(ls.stages(tree, screen), 1):
        node = ls.stage_pupil_node(stage, screen)
        for el in node.iter():
            if not isinstance(el.tag, str) or el.tag.lower() not in BLOCK:
                continue
            text = " ".join(el.text_content().split())
            counts = Counter(sentences(text))
            repeated = sum((n - 1) * len(s.split()) for s, n in counts.items() if n > 1)
            if not repeated:
                continue
            children = [k.tag for k in el if isinstance(k.tag, str)]
            row = {"stage": index, "stageTitle": stage.get("data-title") or "",
                   "tag": el.tag, "class": el.get("class"),
                   "duplicatedWords": repeated,
                   "repeatedSentences": {s: n for s, n in counts.items() if n > 1}}
            if children:
                row["refused"] = ("carries inline markup " + str(children) +
                                  "; string surgery would destroy it")
                refused.append(row)
                continue
            new, removed = dedupe_text(el.text or text)
            if raw.count(el.text or "") != 1:
                row["refused"] = ("its text does not appear exactly once in the file, "
                                  f"so the edit could not be anchored ({raw.count(el.text or '')} matches)")
                refused.append(row)
                continue
            row["removedWords"] = removed
            row["oldText"] = el.text
            row["newText"] = new
            targets.append(row)
    return {"file": str(Path(path)), "toolVersion": VERSION,
            "targets": targets, "refused": refused,
            "duplicatedWordsRemovable": sum(t["removedWords"] for t in targets),
            "duplicatedWordsRefused": sum(r["duplicatedWords"] for r in refused)}


def apply(path: Path) -> dict:
    path = Path(path)
    before = ls.measure(path)
    plan = analyse(path)
    if not plan["targets"]:
        plan.update({"applied": False, "wordsBefore": before["totalWords"],
                     "wordsAfter": before["totalWords"]})
        return plan

    tree = ls.parse(path)
    screen = ls.ScreenView(tree)
    sent_before = set()
    for stage in ls.stages(tree, screen):
        sent_before |= set(sentences(ls.stage_text(stage, screen)))

    raw = path.read_text(encoding="utf-8")
    for t in plan["targets"]:
        assert raw.count(t["oldText"]) == 1, "anchor lost between analyse and apply"
        raw = raw.replace(t["oldText"], t["newText"], 1)
    path.write_text(raw, encoding="utf-8")

    after = ls.measure(path)
    tree2 = ls.parse(path)
    screen2 = ls.ScreenView(tree2)
    sent_after = set()
    for stage in ls.stages(tree2, screen2):
        sent_after |= set(sentences(ls.stage_text(stage, screen2)))
    lost = sorted(sent_before - sent_after)

    plan.update({
        "applied": True,
        "wordsBefore": before["totalWords"], "wordsAfter": after["totalWords"],
        "wordsRemoved": before["totalWords"] - after["totalWords"],
        "distinctSentencesBefore": len(sent_before),
        "distinctSentencesAfter": len(sent_after),
        "sentencesLost": lost,
        "status": "PASS" if not lost else "RED: a distinct pupil sentence was lost",
    })
    return plan


# --------------------------------------------------------------------------
# Controls
# --------------------------------------------------------------------------

_BLOCK = ("Order three fictional school-week cards and narrate them. "
          "Then read the approved extract and identify the action taken. "
          "No learner is asked to reveal home routines.")

_SHELL = """<!doctype html><html><head><style>
.slide{display:none}.slide.active{display:flex}#print-area{display:none}
@media print{#print-area{display:block!important}}
</style></head><body>
<main id="lessonDeck" class="deck"><div class="slide-container">
  <div class="slide active" data-title="I Do"><p>__A__</p>__EXTRA__</div>
  <div class="slide" data-title="We Do"><p>__B__</p></div>
</div></main>
<div id="print-area"><div class="print-section"><p>__P__</p></div></div>
</body></html>"""


def _mk(a="", b="", p="", extra=""):
    return (_SHELL.replace("__A__", a).replace("__B__", b)
            .replace("__P__", p).replace("__EXTRA__", extra))


def _words(source: str) -> int:
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as fh:
        fh.write(source); name = fh.name
    try:
        return ls.measure(Path(name))["totalWords"]
    finally:
        Path(name).unlink(missing_ok=True)


def _run(source: str):
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as fh:
        fh.write(source); name = fh.name
    try:
        before = Path(name).read_text(encoding="utf-8")
        rep = apply(Path(name))
        after = Path(name).read_text(encoding="utf-8")
        return rep, before, after
    finally:
        Path(name).unlink(missing_ok=True)


CONTROL_IDS = [
    "four-fold-repeat-in-one-paragraph-reduces-to-one",
    "no-distinct-sentence-is-lost",
    "a-paragraph-without-repeats-is-byte-identical",
    "a-repeat-across-two-paragraphs-is-left-alone",
    "an-element-with-inline-markup-is-refused-not-edited",
    "staff-drawer-text-is-untouched",
    "print-pack-text-is-untouched",
]


def controls() -> list[dict]:
    out = []

    def rec(cid, description, expected, observed):
        out.append({"id": cid, "description": description, "expected": expected,
                    "observed": observed, "fired": expected == observed})

    quad = _mk(a=(_BLOCK + " ") * 4, b="A single unrepeated pupil sentence here.")
    rep, before, after = _run(quad)
    one = _mk(a=_BLOCK, b="A single unrepeated pupil sentence here.")
    rec("four-fold-repeat-in-one-paragraph-reduces-to-one",
        "a block printed four times in one paragraph collapses to one copy",
        _words(one), rep["wordsAfter"])
    rec("no-distinct-sentence-is-lost",
        "every distinct pupil sentence present before is present after",
        [], rep["sentencesLost"])

    clean = _mk(a="One clean pupil sentence here. And a second clean sentence here.",
                b="A third clean sentence here.")
    rep2, before2, after2 = _run(clean)
    rec("a-paragraph-without-repeats-is-byte-identical",
        "a paragraph with no repeats is not rewritten at all",
        True, before2 == after2)

    split = _mk(a=_BLOCK, b=_BLOCK)
    rep3, before3, after3 = _run(split)
    rec("a-repeat-across-two-paragraphs-is-left-alone",
        "the same block in two different paragraphs is a possible refrain, not a bug",
        True, before3 == after3)

    marked = _mk(a="", extra=f'<p><b>Truth boundary:</b> {(_BLOCK + " ") * 2}</p>',
                 b="A single unrepeated pupil sentence here.")
    rep4, before4, after4 = _run(marked)
    rec("an-element-with-inline-markup-is-refused-not-edited",
        "an element with children is refused and reported, never edited",
        (True, 1), (before4 == after4, len(rep4["refused"])))

    drawer = _mk(a=(_BLOCK + " ") * 2,
                 extra=f'<div data-audience="staff"><p>{(_BLOCK + " ") * 3}</p></div>',
                 b="A single unrepeated pupil sentence here.")
    rep5, before5, after5 = _run(drawer)
    rec("staff-drawer-text-is-untouched",
        "repeats inside the staff drawer are not this tool's business",
        True, (_BLOCK + " ") * 3 in after5.replace("\n", " ") or
              after5.count("Order three fictional school-week cards") >= 4)

    pp = _mk(a="A single unrepeated pupil sentence here.", p=(_BLOCK + " ") * 3,
             b="Another single unrepeated sentence here.")
    rep6, before6, after6 = _run(pp)
    rec("print-pack-text-is-untouched",
        "repeats inside the print pack are not this tool's business",
        True, before6 == after6)

    return out


def self_test() -> dict:
    results = controls()
    ids = [r["id"] for r in results]
    missing = [c for c in CONTROL_IDS if c not in ids]
    extra = [c for c in ids if c not in CONTROL_IDS]
    return {"tool": "dedupe_stage_text", "toolVersion": VERSION,
            "file": "tools/easter/dedupe_stage_text.py",
            "controlsDeclared": len(CONTROL_IDS), "controlsRun": len(results),
            "controlsFired": sum(1 for r in results if r["fired"]),
            "missingControls": missing, "undeclaredControls": extra,
            "allListedControlsFired": not missing and not extra and all(r["fired"] for r in results),
            "controls": results}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--output")
    ap.add_argument("--list-controls", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.list_controls:
        for c in CONTROL_IDS:
            print(c)
        return 0
    if a.self_test:
        r = self_test()
        print(f"dedupe_stage_text self-test  [{VERSION}]")
        for row in r["controls"]:
            print(f"  {'ok  ' if row['fired'] else 'FAIL'} {row['id']:52s} "
                  f"expected={row['expected']} observed={row['observed']}")
        print(f"{r['controlsFired']}/{r['controlsRun']} controls fired")
        if a.output:
            out = ROOT / a.output if not Path(a.output).is_absolute() else Path(a.output)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(r, indent=1) + "\n", encoding="utf-8")
        print("PASS" if r["allListedControlsFired"] else "MEASUREMENT INVALID")
        return 0 if r["allListedControlsFired"] else 1

    rows = []
    for f in a.files:
        p = ROOT / f if not Path(f).is_absolute() else Path(f)
        r = apply(p) if a.apply else analyse(p)
        rows.append(r)
        name = Path(f).name[:46]
        if a.apply:
            print(f"{name:46s} {r['wordsBefore']:5d} -> {r['wordsAfter']:5d} words "
                  f"(-{r.get('wordsRemoved', 0)})  sentences "
                  f"{r.get('distinctSentencesBefore','-')} -> {r.get('distinctSentencesAfter','-')}  "
                  f"{r.get('status','no change')}")
        else:
            print(f"{name:46s} removable={r['duplicatedWordsRemovable']:4d}  "
                  f"refused={r['duplicatedWordsRefused']:4d}  targets={len(r['targets'])}")
        for ref in r["refused"]:
            print(f"    REFUSED stage {ref['stage']} <{ref['tag']} class={ref['class']!r}> "
                  f"{ref['duplicatedWords']}w — {ref['refused']}")
    if a.output:
        out = ROOT / a.output if not Path(a.output).is_absolute() else Path(a.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(rows, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
