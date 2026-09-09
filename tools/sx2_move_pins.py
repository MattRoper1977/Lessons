#!/usr/bin/env python3
"""Move the reviewed content pins in a browser-harness targets file.

Order SX2R R2 (SX3 amendment A1, recorded as _sx2/DECISIONS.md D4).

A targets file pins the exact bytes of each page a browser harness drives:

    {"targets": [{"path": "...", "expectedPatchedSha256": "<64 hex>", ...}, ...]}

tools/easter/science_original_browser.cjs asserts each one as
"Source identity: <file>". So any PR that patches a pinned page must move its
pin in the SAME commit, or that job goes red on content the reviewer meant to
change. Nothing rewrote these before this tool; the file was maintained by hand,
which is why the 25 Autumn 1 pages the refresh touches were a landmine.

Deliberately narrow:

  * default is CHECK. It never writes unless asked.
  * --write refuses to write anything at all if a target path is missing, so a
    partially-correct pin file cannot be produced by a typo in a path.
  * it rewrites the hash values IN PLACE as text rather than re-serialising the
    JSON. Round-tripping through json.dump would reformat the whole file and
    bury 25 real changes in a few thousand cosmetic ones. The diff this
    produces is exactly one line per moved pin.
  * it re-reads and re-parses what it wrote and re-checks every pin before
    reporting success, so a bad substitution cannot pass silently.
  * it is path-agnostic. The targets file is an argument, so SX3 and Part A
    reuse it as-is.

Only targets[].expectedPatchedSha256 moves. reviewedHud.sha256 pins hud.js in
the site repository and is not this repository's to move.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

PIN_KEY = "expectedPatchedSha256"
PIN_RE = re.compile(r'("' + PIN_KEY + r'"\s*:\s*")([0-9a-f]{64})(")')
DEFAULT_ROOT = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(targets_path: Path) -> tuple[dict, str]:
    text = targets_path.read_text(encoding="utf-8")
    return json.loads(text), text


def survey(doc: dict, root: Path) -> tuple[list[dict], list[str]]:
    """Per-target actual/pinned state, plus the paths that are not there."""
    rows, missing = [], []
    for entry in doc["targets"]:
        rel = entry["path"]
        path = root / rel
        if not path.is_file():
            missing.append(rel)
            rows.append({"path": rel, "pinned": entry.get(PIN_KEY), "actual": None})
            continue
        rows.append({"path": rel, "pinned": entry.get(PIN_KEY), "actual": sha256_file(path)})
    return rows, missing


def report(rows: list[dict], missing: list[str]) -> list[str]:
    problems = []
    for rel in missing:
        problems.append("MISSING   " + rel)
    for row in rows:
        if row["actual"] is None:
            continue
        if row["pinned"] != row["actual"]:
            problems.append(
                "STALE PIN " + row["path"]
                + "\n            pinned " + str(row["pinned"])
                + "\n            actual " + row["actual"]
            )
    return problems


def rewrite(targets_path: Path, text: str, doc: dict, rows: list[dict]) -> int:
    """Substitute the i-th pin literal with the i-th computed hash."""
    found = PIN_RE.findall(text)
    if len(found) != len(doc["targets"]):
        raise SystemExit(
            "REFUSING TO WRITE: the file has %d %s literals but %d targets. "
            "The structure is not what this tool understands."
            % (len(found), PIN_KEY, len(doc["targets"]))
        )
    order = iter(rows)

    def swap(match: re.Match) -> str:
        row = next(order)
        return match.group(1) + row["actual"] + match.group(3)

    new_text = PIN_RE.sub(swap, text)
    targets_path.write_text(new_text, encoding="utf-8")
    return sum(1 for r in rows if r["pinned"] != r["actual"])


def run(targets_path: Path, root: Path, write: bool) -> int:
    doc, text = load(targets_path)
    rows, missing = survey(doc, root)
    problems = report(rows, missing)
    moved = sum(1 for r in rows if r["actual"] is not None and r["pinned"] != r["actual"])

    print("targets file : %s" % targets_path)
    print("root         : %s" % root)
    print("targets      : %d" % len(rows))
    print("missing      : %d" % len(missing))
    print("pins to move : %d" % moved)

    if missing:
        # A missing path means the reviewer's intent cannot be established for
        # that row, so nothing is written even if every other row is fine.
        print()
        for line in problems:
            print("  " + line)
        print()
        print("FAIL: %d target path(s) missing. Nothing written." % len(missing))
        return 1

    if not write:
        if problems:
            print()
            for line in problems:
                print("  " + line)
            print()
            print("FAIL: %d pin(s) do not match the bytes on disk." % len(problems))
            return 1
        print()
        print("PASS: every pin equals the bytes on disk.")
        return 0

    if moved == 0:
        print()
        print("PASS: nothing to move; every pin already equals the bytes on disk.")
        return 0

    changed = rewrite(targets_path, text, doc, rows)

    # Read back what was written and re-check from scratch. A substitution that
    # landed on the wrong row would still produce 64 valid hex characters.
    doc2, _ = load(targets_path)
    rows2, missing2 = survey(doc2, root)
    residue = report(rows2, missing2)
    if residue:
        print()
        for line in residue:
            print("  " + line)
        print()
        print("FAIL: the file was rewritten but does not verify. Revert it.")
        return 1

    print()
    for row in rows:
        if row["pinned"] != row["actual"]:
            print("  moved %s" % row["path"])
            print("        %s -> %s" % (row["pinned"], row["actual"]))
    print()
    print("WROTE: %d pin(s) moved, re-read and re-verified." % changed)
    return 0


def self_test() -> int:
    """The red proofs, so the tool is never trusted on its own say-so."""
    checks, failures = [], []

    def check(name: str, ok: bool, detail: str = "") -> None:
        checks.append((name, ok, detail))
        if not ok:
            failures.append(name)

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "pages").mkdir()
        one = root / "pages" / "one.html"
        two = root / "pages" / "two.html"
        one.write_text("<p>one</p>", encoding="utf-8")
        two.write_text("<p>two</p>", encoding="utf-8")
        targets = root / "TARGETS.json"

        def fixture(pin_one: str, pin_two: str, extra_path: str | None = None) -> None:
            entries = [
                {"path": "pages/one.html", PIN_KEY: pin_one, "note": "keep me"},
                {"path": "pages/two.html", PIN_KEY: pin_two},
            ]
            if extra_path:
                entries.append({"path": extra_path, PIN_KEY: "f" * 64})
            targets.write_text(
                json.dumps({"schema": "t-v1", "targets": entries}, indent=1) + "\n",
                encoding="utf-8",
            )

        h1, h2 = sha256_file(one), sha256_file(two)

        fixture(h1, h2)
        check("correct pins check green", run(targets, root, write=False) == 0)

        # THE PLANTED STALE HASH the order names.
        fixture("0" * 64, h2)
        check("a planted stale pin goes red", run(targets, root, write=False) == 1)

        fixture("0" * 64, h2)
        check("--write moves it", run(targets, root, write=True) == 0)
        after = json.loads(targets.read_text(encoding="utf-8"))
        check("the planted row now holds the real hash",
              after["targets"][0][PIN_KEY] == h1)
        check("the untouched row is untouched", after["targets"][1][PIN_KEY] == h2)
        check("sibling keys survive the rewrite",
              after["targets"][0].get("note") == "keep me")
        check("the rewritten file re-checks green", run(targets, root, write=False) == 0)

        # A missing path must refuse the whole write, not skip the row.
        fixture("0" * 64, h2, extra_path="pages/absent.html")
        check("a missing target path fails the check", run(targets, root, write=False) == 1)
        before = targets.read_text(encoding="utf-8")
        check("a missing target path refuses --write", run(targets, root, write=True) == 1)
        check("and writes nothing at all", targets.read_text(encoding="utf-8") == before)

        # Content moving under a correct pin is the real-world case.
        fixture(h1, h2)
        one.write_text("<p>one, edited</p>", encoding="utf-8")
        check("edited content makes its pin stale", run(targets, root, write=False) == 1)
        check("--write catches up", run(targets, root, write=True) == 0)
        check("and it verifies afterwards", run(targets, root, write=False) == 0)

        # The formatting guarantee: only pin lines move.
        fixture(h1, sha256_file(two))
        one.write_text("<p>one, edited again</p>", encoding="utf-8")
        text_before = targets.read_text(encoding="utf-8").splitlines()
        run(targets, root, write=True)
        text_after = targets.read_text(encoding="utf-8").splitlines()
        differing = [i for i, (a, b) in enumerate(zip(text_before, text_after)) if a != b]
        check("exactly one line changes for one moved pin",
              len(text_before) == len(text_after) and len(differing) == 1,
              "lines differing: %d" % len(differing))

    print()
    print("=" * 62)
    for name, ok, detail in checks:
        print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name,
                               (" - " + detail) if detail else ""))
    print("=" * 62)
    if failures:
        print("SELF-TEST FAILED: %d of %d" % (len(failures), len(checks)))
        return 1
    print("SELF-TEST PASS: %d checks, including the planted stale pin" % len(checks))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("targets", nargs="?", type=Path,
                        help="the targets JSON to check or move")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT,
                        help="repository root the target paths are relative to")
    parser.add_argument("--write", action="store_true",
                        help="recompute and rewrite the pins (default is check only)")
    parser.add_argument("--self-test", action="store_true",
                        help="run the built-in red proofs and exit")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if args.targets is None:
        parser.error("a targets file is required unless --self-test is given")
    if not args.targets.is_file():
        print("FAIL: no targets file at %s" % args.targets)
        return 1
    return run(args.targets.resolve(), args.root.resolve(), args.write)


if __name__ == "__main__":
    sys.exit(main())
