#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Block-2 batch driver: render 10 lessons (9 Block-2 + the held specimen), run the full
gate set per file, plus the batch-level gates (§6 gates 9-13):
  - cardinality (n in, n out, named)
  - specimen reproduced byte-for-byte vs baseline (or diff explained)
  - LL-INST-09 loop-mark gate, all tiers
  - sentinel derivation (deferred to placement step, run separately)
  - legacy byte-identity (run separately against git)
"""
import sys
import subprocess
import hashlib
import pathlib

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "inputs"))
import gates  # noqa: E402
import content_build  # noqa: E402
import content_grow  # noqa: E402

JSDOM = str(HERE / "node_modules/jsdom")
OUT = HERE / "out"

EXPECT = {  # slug -> exit_key, per pathway
    "content_build": {l["slug"]: l["exit_key"] for l in content_build.LESSONS},
    "content_grow": {l["slug"]: l["exit_key"] for l in content_grow.LESSONS},
}
ALL = {**EXPECT["content_build"], **EXPECT["content_grow"]}


def main():
    # cardinality: exactly these 10 files must exist
    produced = sorted(p.name for p in OUT.glob("*.html"))
    expected = sorted(s + ".html" for s in ALL)
    print(f"CARDINALITY: expected {len(expected)}, produced {len(produced)}")
    missing = set(expected) - set(produced)
    extra = set(produced) - set(expected)
    if missing:
        print("  MISSING:", sorted(missing))
    if extra:
        print("  UNEXPECTED:", sorted(extra))
    card_ok = not missing and not extra

    # per-file gates 1-6
    allok = card_ok
    for slug, keys in ALL.items():
        path = OUT / (slug + ".html")
        ok = gates.run(str(path), keys, JSDOM)
        allok = allok and ok

    # LL-INST-09 (estate loop-mark gate), all files
    print("\n===== LL-INST-09 loop-mark gate (estate instrument) =====")
    r = subprocess.run(
        ["python3", "/workspace/lessons/LundyLoop/tools/loop_mark_print_gate.py"]
        + [str(OUT / (s + ".html")) for s in ALL],
        capture_output=True, text=True, env={"PLAYWRIGHT_BROWSERS_PATH": "/opt/pw-browsers",
                                             "PATH": "/usr/bin:/bin:/usr/local/bin"})
    tail = r.stdout.strip().splitlines()[-1] if r.stdout else r.stderr[-200:]
    print(" ", tail)
    ll_ok = "PASS" in (r.stdout or "")
    allok = allok and ll_ok

    # gate 11: specimen reproduced byte-for-byte
    base = (HERE / "specimen_baseline.sha")
    spec = OUT / "SCI_B_W3_Backbones.html"
    if base.exists():
        want = base.read_text().split()[0]
        got = hashlib.sha256(spec.read_bytes()).hexdigest()
        same = want == got
        print(f"\nGATE 11 specimen reproduction: baseline={want[:12]} now={got[:12]} "
              f"{'IDENTICAL' if same else 'DIFFERS — explain the diff'}")
        allok = allok and same
    else:
        print("\nGATE 11: no baseline recorded")

    print("\n==================== BATCH RESULT:",
          "ALL GREEN" if allok else "FAIL — do not push", "====================")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
