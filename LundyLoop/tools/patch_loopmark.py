#!/usr/bin/env python3
"""patch_loopmark.py — port the BUILD loop-mark block from a donor file into named targets.

WHAT IT KEYS ON (the tell): the literal marker string "ll-g:loop-mark v1" inside the
donor, and the donor block's own structural anchor (the id of the element immediately
preceding it). Position decides the insertion point in each target; the marker text
only confirms. If the anchor cannot be found identically in a target, that target
FAILS CLOSED and is skipped with a reason — the file is never modified on a guess.

WHAT IT CANNOT SEE (the unseen sibling): a closure block already present in a target
under DIFFERENT wording or a different marker version — this script would insert a
second block beside it. The idempotence check catches only the exact v1 marker; a
same-purpose block with other words is invisible to it (the LL-E lesson). A human
reads the report before anything ships.

DISCIPLINE:
  * DRY-RUN BY DEFAULT. Nothing is written without --write.
  * Explicit target files only — no globs, no directories, no discovery.
  * Refuses targets outside Build/ ; refuses assessed files, LundyLoop/, tools/.
  * Idempotent: a target already carrying the marker is skipped and reported.
  * Emits a manifest (would-patch / patched / skipped-reason) and asserts
    would+skipped == targets given. Emit, don't transcribe.
  * The marker string here is inert to the estate's sentinel derivations, which
    carry the pathspec -- '*.html' (R-E10): a .py file is never counted.

Usage:
  python3 patch_loopmark.py --donor <build_lesson.html> <target.html> [<target.html> ...]
  python3 patch_loopmark.py --write --donor <donor> <targets...>
Exit: 0 clean · 1 nothing actionable · 2 misuse or environment refusal.
"""
import sys, re
from pathlib import Path

MARKER = "ll-g:loop-mark v1"
ROOT = Path(__file__).resolve().parents[2]   # LundyLoop/tools/ -> repo root

def die(msg, code=2):
    print(f"REFUSED: {msg}", file=sys.stderr); sys.exit(code)

def extract_block(html: str):
    """Return (block_text, anchor_id) for the smallest balanced element containing MARKER,
    plus the id of the nearest preceding element carrying an id. Fails closed on any doubt."""
    i = html.find(MARKER)
    if i < 0:
        return None, None, "donor does not contain the marker"
    # walk back to the opening '<' of the ELEMENT containing the marker,
    # skipping non-element openers (comments <!--, doctype <!, closers </)
    start = html.rfind("<", 0, i)
    m = None
    while start >= 0:
        m = re.match(r"<([a-zA-Z][a-zA-Z0-9-]*)", html[start:])
        if m:
            break
        start = html.rfind("<", 0, start)
    if not m:
        return None, None, "could not identify the marker's containing element"
    tag = m.group(1).lower()
    # balance forward over same-name tags
    depth, j = 0, start
    opener = re.compile(rf"<{tag}\b(?![^>]*/>)", re.I)
    closer = re.compile(rf"</{tag}\s*>", re.I)
    pos = start
    while True:
        o = opener.search(html, pos); c = closer.search(html, pos)
        if c is None:
            return None, None, f"unbalanced <{tag}> while extracting the block"
        if o is not None and o.start() < c.start():
            depth += 1; pos = o.end()
        else:
            depth -= 1; pos = c.end()
            if depth == 0:
                block = html[start:pos]; break
    # structural anchor: nearest preceding id=""
    pre = html[:start]
    ids = re.findall(r'id\s*=\s*"([^"]+)"', pre)
    if not ids:
        return None, None, "no preceding id found to anchor on"
    return block, ids[-1], None

def main(argv):
    write = "--write" in argv
    argv = [a for a in argv if a != "--write"]
    if "--donor" not in argv:
        die("usage: patch_loopmark.py [--write] --donor <file> <targets...>")
    d = argv.index("--donor")
    try:
        donor = Path(argv[d+1])
    except IndexError:
        die("--donor requires a file")
    targets = [Path(t) for t in argv[d+2:]]
    if not targets:
        die("no target files given — explicit files only, no discovery")
    for t in targets:
        if t.is_dir(): die(f"{t} is a directory — explicit files only")
        if t.suffix.lower() != ".html": die(f"{t} is not an .html file")
        rel = t.resolve()
        try:
            relstr = str(rel.relative_to(ROOT))
        except ValueError:
            relstr = str(rel)
        low = relstr.lower().replace("\\", "/")
        if "/build/" not in ("/" + low) and not low.startswith("build/"):
            die(f"{t}: outside Build/ — scope guard")
        for banned in ("lundyloop/", "tools/", "_w7", "hum_w7"):
            if banned in low:
                die(f"{t}: matches no-go scope '{banned}'")
    if not donor.is_file(): die(f"donor {donor} not found")
    block, anchor, err = extract_block(donor.read_text(encoding="utf-8", errors="strict"))
    if err: die(f"donor: {err}")
    print(f"donor block: {len(block)} bytes · anchored after id=\"{anchor}\"")
    would, skipped = [], []
    for t in targets:
        html = t.read_text(encoding="utf-8", errors="strict")
        if MARKER in html:
            skipped.append((t, "already carries the marker (idempotence)")); continue
        am = re.search(rf'id\s*=\s*"{re.escape(anchor)}"', html)
        if not am:
            skipped.append((t, f'anchor id="{anchor}" not found — FAIL CLOSED')); continue
        # insertion point: after the CLOSE of the anchor element — balance it directly
        astart = html.rfind("<", 0, am.start())
        tm = re.match(r"<([a-zA-Z][a-zA-Z0-9-]*)", html[astart:])
        if not tm:
            skipped.append((t, "could not read the anchor's tag — FAIL CLOSED")); continue
        atag = tm.group(1).lower()
        depth, pos = 0, astart
        op = re.compile(rf"<{atag}\b(?![^>]*/>)", re.I); cl = re.compile(rf"</{atag}\s*>", re.I)
        end = None
        while True:
            o = op.search(html, pos); c = cl.search(html, pos)
            if c is None: break
            if o is not None and o.start() < c.start(): depth += 1; pos = o.end()
            else:
                depth -= 1; pos = c.end()
                if depth == 0: end = pos; break
        if end is None:
            skipped.append((t, "anchor element unbalanced — FAIL CLOSED")); continue
        would.append((t, html[:end] + "\n" + block + html[end:]))
    print("\nMANIFEST")
    for t, _ in would: print(f"  WOULD-PATCH {t}")
    for t, why in skipped: print(f"  SKIP        {t} — {why}")
    assert len(would) + len(skipped) == len(targets), "manifest does not sum to targets"
    print(f"  asserted: {len(would)} would-patch + {len(skipped)} skipped = {len(targets)} targets")
    if not write:
        print("\nDRY RUN — nothing written. Re-run with --write to apply."); return 0 if would else 1
    for t, new in would:
        t.write_text(new, encoding="utf-8"); print(f"  PATCHED {t}")
    print(f"\nWROTE {len(would)} file(s). Verify with git diff before any commit.")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
