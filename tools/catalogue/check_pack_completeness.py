#!/usr/bin/env python3
"""Pack completeness (rulings tq-1, tq-2 standing rule, tq add.1 Q1-Q4).

For every landed companion pack (a resources.json row of kind "pack" whose
companionOf page is in the tree):
  * the Pack row's files[] equal the pack's members;
  * where the pack sits beside its page (the Week 8 layout), the page's links to
    pack files equal the same members; older pages, whose pack lives in its own
    folder, are reported "hub-only" and pass (the hub pack page reaches them);
  * a 12-member pack carries the labels of record on its files.

Members. Beside the page: the page basename + "_" + one of the 12 member names of
record; any other file with that prefix is reported as "outside the pack" (the
older Teacher_Notes.pdf beside two pages stays linked and outside, tq add.1 Q4).
Own folder: every pdf/docx/pptx in the folder that shares the row's common
file-name stem (several lessons may share one Teaching_Packs folder).

    python3 tools/catalogue/check_pack_completeness.py            # check this tree
    python3 tools/catalogue/check_pack_completeness.py --self-test
"""
import argparse, copy, json, os, posixpath, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXTS = ("pdf", "docx", "pptx")
LINK = re.compile(r'href="([^"#?]+\.(?:pdf|docx|pptx))"')
# The 12-member pack: member name of record -> label of record (tq add.1 Q3).
LABELS = {
    "Slides.pptx": "Slides",
    "Editable_Pack.docx": "Editable pack",
    "Teacher_and_Cover_Plan.docx": "Teacher and cover plan (editable)",
    "Teacher_and_Cover_Plan.pdf": "Teacher and cover plan (print)",
    "TA_Brief.pdf": "TA brief",
    "Staff_Answers.pdf": "Staff answers",
    "Knowledge_Organiser.pdf": "Knowledge organiser",
    "Pupil_Resources.pdf": "Pupil resources",
    "Word_Page.pdf": "Word page",
    "Tier_Pack_Supported.pdf": "Tier pack – Supported",
    "Tier_Pack_Standard.pdf": "Tier pack – Standard",
    "Tier_Pack_Stretch.pdf": "Tier pack – Stretch",
}


def common_stem(names):
    s = os.path.commonprefix(sorted(names))
    return s


def members(row, page, files):
    pd = posixpath.dirname(page)
    dirs = {posixpath.dirname(f.get("path", "")) for f in row.get("files", [])}
    if dirs == {pd}:  # beside the page
        base = posixpath.basename(page)[:-5] + "_"
        named = [p for p in files if posixpath.dirname(p) == pd and posixpath.basename(p).startswith(base)
                 and p.rsplit(".", 1)[-1] in EXTS]
        inside = sorted(p for p in named if posixpath.basename(p)[len(base):] in LABELS)
        outside = sorted(set(named) - set(inside))
        return "beside", inside, outside
    stem = common_stem([posixpath.basename(f.get("path", "")) for f in row.get("files", [])])
    inside = sorted(p for p in files if posixpath.dirname(p) in dirs and posixpath.basename(p).startswith(stem)
                    and p.rsplit(".", 1)[-1] in EXTS)
    return "folder", inside, []


def page_links(page, html):
    d = posixpath.dirname(page)
    return {posixpath.normpath(posixpath.join(d, h)) for h in LINK.findall(html) if "://" not in h and not h.startswith("/")}


def evaluate(rows, files, read):
    errs, notes, counts = [], [], {"beside": 0, "hub-only": 0}
    for r in rows:
        if r.get("kind") != "pack" or r.get("companionOf") not in files:
            continue
        page = r["companionOf"]; name = posixpath.basename(page)
        layout, want, outside = members(r, page, files)
        row = sorted(f.get("path") for f in r.get("files", []))
        if row != want:
            errs.append(f"{name}: Pack row lists {len(row)} of {len(want)} members"
                        f" (missing {len(set(want) - set(row))}, not members {len(set(row) - set(want))})")
        if layout == "beside":
            counts["beside"] += 1
            linked = sorted(page_links(page, read(page)) & (set(want) | set(outside)))
            got = sorted(set(linked) & set(want))
            if got != want:
                errs.append(f"{name}: page links {len(got)} of {len(want)} members")
            if len(want) == len(LABELS):
                base = name[:-5] + "_"
                bad = [f for f in r.get("files", []) if f.get("label") != LABELS.get(posixpath.basename(f.get("path", ""))[len(base):])]
                if bad:
                    errs.append(f"{name}: {len(bad)} of {len(want)} files lack their label of record")
            for o in outside:
                notes.append(f"{name}: {posixpath.basename(o)} sits beside the page, outside the pack")
        else:
            counts["hub-only"] += 1
    return errs, notes, counts


def tree_inputs(root):
    rows = json.loads((root / "resources.json").read_text(encoding="utf-8"))
    files = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and ".git" not in p.parts}
    return rows, files, lambda page: (root / page).read_text(encoding="utf-8", errors="replace")


def self_test():
    page = "S/W/X_P1.html"
    m = [f"S/W/X_P1_{n}" for n in LABELS]
    files = set(m) | {page, "S/W/X_P2_Slides.pptx", "S/W/X_P1_Teacher_Notes.pdf",
                      "S/T/W4L1_A.pdf", "S/T/W4L1_B.pptx", "S/T/W4L2_A.pdf", "S/p.html"}
    good = [{"kind": "pack", "companionOf": page,
             "files": [{"path": p, "label": LABELS[p.split("X_P1_")[1]]} for p in m]},
            {"kind": "pack", "companionOf": "S/p.html", "files": [{"path": "S/T/W4L1_A.pdf"}, {"path": "S/T/W4L1_B.pptx"}]}]
    html = "".join(f'<a href="{posixpath.basename(p)}">x</a>' for p in m) + '<a href="X_P1_Teacher_Notes.pdf">t</a>'
    read = lambda p: html if p == page else ""
    e, n, c = evaluate(good, files, read)
    assert e == [] and c == {"beside": 1, "hub-only": 1} and len(n) == 1, (e, n, c)
    plants = []
    a = copy.deepcopy(good); a[0]["files"].pop(); plants.append(("row lists fewer members", a, files, read))
    b = copy.deepcopy(good); b[0]["files"].append({"path": "S/W/X_P2_Slides.pptx"}); plants.append(("row lists another page's file", b, files, read))
    plants.append(("page links fewer members", good, files, lambda p: html.split("</a>", 1)[1] if p == page else ""))
    plants.append(("a folder member on disk the row does not list", good, files | {"S/T/W4L1_C.pdf"}, read))
    d = copy.deepcopy(good); d[0]["files"][3]["label"] = "Teacher guide"; plants.append(("a wrong label", d, files, read))
    g = copy.deepcopy(good); del g[0]["files"][5]["label"]; plants.append(("a missing label", g, files, read))
    for name, rows, fs, rd in plants:
        if not evaluate(rows, fs, rd)[0]:
            print(f"[SELF-TEST FAIL] not caught: {name}"); return 1
    print(f"[SELF-TEST PASS] green control (1 beside, 1 hub-only, 1 outside noted) + {len(plants)} planted defects caught")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    errs, notes, c = evaluate(*tree_inputs(a.root))
    for e in errs: print("[RED]", e)
    for n in notes: print("[NOTE]", n)
    print(f"{'[PASS]' if not errs else '[FAIL]'} pack completeness: {c['beside']} beside the page, "
          f"{c['hub-only']} hub-only; {len(errs)} error(s), {len(notes)} outside the pack")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
