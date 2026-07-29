#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Placement (§5): copy rendered science lessons into a NEW folder (never inside the frozen
science folders) following the Art_Teesside / Humanities_Teesside convention, and register
them in resources.json so the Lessons hub returns them.

  Folder convention (mirrors Art_Teesside/Build|Grow|Launch): Science_Teesside/<Tier>/
  Subject:  "Science · Teesside"  (one subject; tier is derived from the path by the hub)
  desc:     the lesson's own authored Learning Objective (nothing invented)
  year:     2026-27 (active collection)

Idempotent: strips any prior sci-tees-* entries before re-adding.
Safe I/O (§7): read fully -> build -> assert -> write.
"""
import json
import pathlib
import shutil
import sys

REPO = pathlib.Path("/workspace/lessons")
OUT = REPO / "_passsci1/out"
RES = REPO / "resources.json"
ADDED = "2026-07-29"
SUBJECT = "Science · Teesside"
FAMILY = "Science Teesside"
TIER_DIR = {"content_build": "Build", "content_grow": "Grow", "content_launch": "Launch"}
TIER_ID = {"content_build": "b", "content_grow": "g", "content_launch": "l"}

sys.path.insert(0, str(REPO / "_passsci1/inputs"))


def entries_for(modname):
    mod = __import__(modname)
    tdir = TIER_DIR[modname]
    tid = TIER_ID[modname]
    out = []
    for L in mod.LESSONS:
        slug = L["slug"]
        rel = f"Science_Teesside/{tdir}/{slug}.html"
        kw = [mod.PATHWAY.lower(), "science", f"week {L['week']}"] + [t for t, _ in L["ko_vocab"][:4]]
        out.append({
            "subject": SUBJECT,
            "title": f'{mod.PATHWAY} · {L["title"]}',
            "file": rel,
            "id": f"sci-tees-{tid}-w{L['week']}",
            "type": "lesson",
            "family": FAMILY,
            "keywords": [k.lower() for k in kw],
            "desc": L["lo"],                       # authored LO, nothing invented
            "added": ADDED,
            "new": True,
            "year": "2026-27",
        })
    return out


def main(modnames):
    # 1 · copy files into the new folder
    copied = []
    for modname in modnames:
        tdir = TIER_DIR[modname]
        (REPO / "Science_Teesside" / tdir).mkdir(parents=True, exist_ok=True)
        mod = __import__(modname)
        for L in mod.LESSONS:
            src = OUT / (L["slug"] + ".html")
            assert src.exists(), f"rendered file missing: {src}"
            dst = REPO / "Science_Teesside" / tdir / (L["slug"] + ".html")
            shutil.copy2(src, dst)
            # post-condition: byte-identical copy that ends </html>
            assert dst.read_bytes() == src.read_bytes(), f"copy mismatch {dst}"
            assert dst.read_text(encoding="utf-8").rstrip().endswith("</html>"), f"{dst} !</html>"
            copied.append(str(dst.relative_to(REPO)))

    # 2 · register in resources.json (read fully -> transform -> assert -> write)
    raw = RES.read_text(encoding="utf-8")
    data = json.loads(raw)
    assert isinstance(data, list), "resources.json is not a list"
    n0 = len(data)
    data = [e for e in data if not str(e.get("id", "")).startswith("sci-tees-")]  # idempotent
    new_entries = []
    for modname in modnames:
        new_entries += entries_for(modname)
    data += new_entries
    # asserts BEFORE writing
    files_on_disk = {e["file"] for e in new_entries}
    for f in files_on_disk:
        assert (REPO / f).exists(), f"resources entry points at missing file: {f}"
    ids = [e["id"] for e in data if str(e.get("id", "")).startswith("sci-tees-")]
    assert len(ids) == len(set(ids)), "duplicate sci-tees ids"
    out = json.dumps(data, ensure_ascii=False, indent=1) + "\n"
    assert json.loads(out) == data, "round-trip mismatch"
    RES.write_text(out, encoding="utf-8")

    print(f"placed {len(copied)} files; resources.json {n0} -> {len(data)} entries "
          f"(+{len(new_entries)} sci-tees)")
    for e in new_entries:
        print(f"  {e['id']:16} {e['file']}")


if __name__ == "__main__":
    mods = sys.argv[1:] or ["content_build", "content_grow"]
    main(mods)
