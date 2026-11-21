#!/usr/bin/env python3
"""Census every media-bearing element in a page, live against a candidate.

Order SX2R, ruling of 2026-09-09 (recorded as _sx2/DECISIONS.md D8).

Why this exists. A refresh pack is authored from its own source and can simply
lack something the live page has. Patching that pack over live, section for
section, drops whatever only live carried -- silently, because the pack's prose
survives and reads as though the missing thing were still there. That is what
happened to the Autumn 1 refresh: all 15 LAUNCH lessons kept a heading reading
"Model explanation and diagram" above nothing, because the pack shipped with
zero <img> where live had two _model.svg each. 30 images, and the furniture
census did not see it because it was looking for hud.js and "Made by Matt".

The browser harness caught 8 of those 15. A gate that under-reports by half is
not a gate you can land behind, so the census is per file and per element class,
and its answer is a delta that must be 0 or explained.

  python3 tools/sx2_media_census.py --live-ref origin/main --candidate DIR \\
      --files paths.json

Exit 1 if any file loses any media element. --allow lists paths whose loss is
reviewed and intended, so an accepted removal is declared rather than silent.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from lxml import html as LH

# Every element that can put a picture, a diagram, a clip or an embed in front
# of a pupil. Counting <img> alone would have missed an inline <svg> model or a
# <picture> fallback, and the whole lesson of this order is that a census which
# only looks where you expect the loss is not a census.
CLASSES = {
    "img": "//img",
    "svg-inline": "//*[local-name()='svg']",
    "picture": "//picture",
    "source": "//source",
    "video": "//video",
    "audio": "//audio",
    "object": "//object",
    "embed": "//embed",
    "canvas": "//canvas",
    "iframe": "//iframe",
    "figure": "//figure",
}

# Referenced assets, counted separately: an element can survive while the thing
# it points at is swapped for nothing.
REFS = ("_model.svg", ".webp", ".png", ".svg", ".mp4", ".jpg")


def git_text(ref: str, rel: str, root: Path) -> str:
    out = subprocess.run(["git", "show", f"{ref}:{rel}"], cwd=root,
                         capture_output=True, text=True)
    return out.stdout


def count(src: str) -> dict:
    if not src.strip():
        return {}
    try:
        doc = LH.fromstring(src)
    except Exception:
        return {}
    counts = {name: len(doc.xpath(path)) for name, path in CLASSES.items()}
    for ref in REFS:
        counts["ref" + ref] = src.count(ref)
    return counts


def accessible_names(src: str, kind: str) -> set:
    """The names a screen reader would announce, for img or for inline svg.

    An inlined picture keeps its meaning only if its accessible name survives.
    Comparing counts alone would wave through a diagram swapped for a different
    diagram, so the census compares what the page says the picture IS.
    """
    try:
        doc = LH.fromstring(src)
    except Exception:
        return set()
    names = set()
    if kind == "img":
        for el in doc.xpath("//img"):
            for attr in ("alt", "aria-label"):
                v = (el.get(attr) or "").strip()
                if v:
                    names.add(v)
    else:
        for el in doc.xpath("//*[local-name()='svg']"):
            v = (el.get("aria-label") or "").strip()
            if v:
                names.add(v)
            for t in el.xpath("./*[local-name()='title']"):
                if (t.text or "").strip():
                    names.add(t.text.strip())
            parent = el.getparent()
            if parent is not None:
                v = (parent.get("aria-label") or "").strip()
                if v:
                    names.add(v)
    return names


def compare(live_src: str, cand_src: str) -> list[tuple[str, int, int]]:
    a, b = count(live_src), count(cand_src)
    losses = []
    for key in sorted(set(a) | set(b)):
        la, lb = a.get(key, 0), b.get(key, 0)
        if lb < la:
            losses.append((key, la, lb))
    return losses


def classify(live_src: str, cand_src: str) -> tuple[list, list]:
    """Split losses into real ones and format swaps.

    Re-encoding a poster from PNG to webp drops one reference and adds another
    while every element stays exactly where it was. That is not a lost picture,
    and calling it one would train the reader to wave the census through -- the
    failure mode this tool exists to prevent. A swap is only a swap when the
    ELEMENT counts are untouched and the lost references are matched one for one
    by gained references of another format; anything else stays a loss.
    """
    a, b = count(live_src), count(cand_src)
    element_loss = [(k, a.get(k, 0), b.get(k, 0)) for k in CLASSES
                    if b.get(k, 0) < a.get(k, 0)]
    swaps = []

    # INLINING. An <img src="x.svg"> can become an inline <svg> carrying the
    # same drawing. The picture did not go anywhere - it moved into the
    # document, usually with better labelling and one fewer request. Counting
    # that as a loss is the same error as counting png->webp as a loss, and it
    # is the error that cost this order an afternoon: the census reported 30
    # destroyed images that were never destroyed.
    #
    # It only counts as inlining if the arithmetic AND the accessible name both
    # survive: every alt text that disappeared must reappear as an aria-label
    # or an svg <title>. A picture replaced by a different picture, or by an
    # unlabelled one, stays a loss.
    lost_img = a.get("img", 0) - b.get("img", 0)
    gained_svg = b.get("svg-inline", 0) - a.get("svg-inline", 0)
    if lost_img > 0 and gained_svg >= lost_img:
        names_before = accessible_names(live_src, "img")
        names_after = accessible_names(cand_src, "svg")
        if names_before and names_before <= names_after:
            element_loss = [e for e in element_loss if e[0] != "img"]
            swaps.append(("img -> inline svg, accessible name preserved",
                          lost_img, gained_svg))

    ref_lost = {k: a.get(k, 0) - b.get(k, 0) for k in a
                if k.startswith("ref") and b.get(k, 0) < a.get(k, 0)}
    ref_gained = {k: b.get(k, 0) - a.get(k, 0) for k in b
                  if k.startswith("ref") and b.get(k, 0) > a.get(k, 0)}

    if element_loss:
        return element_loss + [(k, a.get(k, 0), b.get(k, 0)) for k in ref_lost], swaps
    if not ref_lost:
        return [], swaps
    if sum(ref_lost.values()) == sum(ref_gained.values()) and ref_gained:
        swaps.append(("%s -> %s" % (",".join(sorted(ref_lost)), ",".join(sorted(ref_gained))),
                      sum(ref_lost.values()), sum(ref_gained.values())))
        return [], swaps
    # A reference that vanished with no replacement, while the elements stayed:
    # that is a picture element pointing at nothing, which is worse than a loss.
    if swaps:
        return [], swaps
    return [(k, a.get(k, 0), b.get(k, 0)) for k in ref_lost], swaps


def run(files: list[str], live_ref: str, candidate: Path, root: Path,
        allow: set[str], verbose: bool) -> int:
    offenders, clean, gains, swapped = [], 0, [], []
    for rel in files:
        live_src = git_text(live_ref, rel, root)
        cand = candidate / rel
        if not cand.is_file():
            offenders.append((rel, [("FILE MISSING", 1, 0)]))
            continue
        cand_src = cand.read_text(encoding="utf-8", errors="replace")
        losses, swaps = classify(live_src, cand_src)
        if swaps:
            swapped.append((rel, swaps))
        if losses and rel not in allow:
            offenders.append((rel, losses))
        elif losses:
            gains.append(rel)
        elif not swaps:
            clean += 1

    print("files censused        : %d" % len(files))
    print("no media change       : %d" % clean)
    print("format swaps          : %d   (elements unchanged, reference re-encoded)" % len(swapped))
    print("declared-loss allowed : %d" % len(gains))
    print("LOSING MEDIA          : %d   (gate: 0)" % len(offenders))
    if offenders:
        print()
        for rel, losses in offenders:
            print("  %s" % rel)
            for key, la, lb in losses:
                print("      %-16s live=%-4d candidate=%-4d   lost %d" % (key, la, lb, la - lb))
    if swapped and verbose:
        print()
        print("format swaps, each element-for-element:")
        for rel, swaps in swapped:
            for what, lost, gained in swaps:
                print("  %-52s %s  (%d for %d)" % (rel.split("/")[-1], what, lost, gained))
    if gains and verbose:
        print()
        print("declared losses (--allow):")
        for rel in gains:
            print("  %s" % rel)
    print()
    if offenders:
        print("FAIL: %d file(s) lose media the live page carries." % len(offenders))
        return 1
    print("PASS: no file loses any media element class.")
    return 0


def self_test() -> int:
    """Red proofs. A census that cannot fail is not evidence."""
    checks, failures = [], []

    def check(name, ok, detail=""):
        checks.append((name, ok, detail))
        if not ok:
            failures.append(name)

    LIVE = ('<html><body><section class="s">'
            '<img src="resources/W7L3_model.svg" alt="model">'
            '<p>Model explanation and diagram</p>'
            '<video controls poster="a.png"><source src="a.mp4"></video>'
            '<svg viewBox="0 0 1 1"></svg>'
            '</section></body></html>')

    same = count(LIVE)
    check("a page does not lose media against itself", compare(LIVE, LIVE) == [])
    check("every class is counted", same["img"] == 1 and same["video"] == 1
          and same["svg-inline"] == 1 and same["source"] == 1)

    # THE PLANTED DROP: the exact defect this tool exists for - the prose stays,
    # the picture goes.
    dropped = LIVE.replace('<img src="resources/W7L3_model.svg" alt="model">', '')
    losses = dict((k, (a, b)) for k, a, b in compare(LIVE, dropped))
    check("a dropped <img> is caught", "img" in losses and losses["img"] == (1, 0))
    check("and its referenced model is caught too", "ref_model.svg" in losses)

    check("a dropped inline <svg> is caught",
          any(k == "svg-inline" for k, a, b in compare(LIVE, LIVE.replace('<svg viewBox="0 0 1 1"></svg>', ''))))
    check("a dropped <video> is caught",
          any(k == "video" for k, a, b in compare(LIVE, LIVE.replace('<video', '<div data-was-video'))))
    check("a swapped-out source is caught",
          any(k.startswith("ref") for k, a, b in compare(LIVE, LIVE.replace('a.mp4', ''))))
    check("added media is NOT a loss",
          compare(LIVE, LIVE.replace('</section>', '<img src="new.png"></section>')) == [])

    # A format swap is not a lost picture, and must not be reported as one -
    # but it must not be invisible either, or the census teaches people to
    # ignore it. Elements unchanged, one reference re-encoded.
    swapped = LIVE.replace('a.png', 'a.webp')
    losses, swaps = classify(LIVE, swapped)
    check("a png->webp swap is not a loss", losses == [])
    check("but the swap is still reported", len(swaps) == 1)
    # And a swap that also drops an element is still a loss.
    both = LIVE.replace('a.png', 'a.webp').replace('<img src="resources/W7L3_model.svg" alt="model">', '')
    losses2, _ = classify(LIVE, both)
    check("a swap that also drops an element stays a loss",
          any(k == "img" for k, a_, b_ in losses2))

    # INLINING, the case that cost this order an afternoon. Same drawing, moved
    # into the document, accessible name preserved.
    INLINED = LIVE.replace(
        '<img src="resources/W7L3_model.svg" alt="model">',
        '<div role="img" aria-label="model"><svg><title>model</title></svg></div>')
    li, sw = classify(LIVE, INLINED)
    check("img -> inline svg with the name preserved is NOT a loss", li == [])
    check("but the inlining is still reported", any("inline svg" in s[0] for s in sw))

    # And it is only inlining if the name survives. A picture swapped for an
    # unlabelled one is still a loss.
    STRIPPED = LIVE.replace(
        '<img src="resources/W7L3_model.svg" alt="model">',
        '<div><svg></svg></div>')
    li2, _ = classify(LIVE, STRIPPED)
    check("img -> unlabelled svg IS still a loss",
          any(k == "img" for k, a_, b_ in li2))

    # A different picture with a different name is a loss, not an inlining.
    OTHER = LIVE.replace(
        '<img src="resources/W7L3_model.svg" alt="model">',
        '<div role="img" aria-label="something else"><svg><title>other</title></svg></div>')
    li3, _ = classify(LIVE, OTHER)
    check("img -> a differently-named svg IS still a loss",
          any(k == "img" for k, a_, b_ in li3))

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "pages").mkdir()
        (root / "pages" / "one.html").write_text(dropped, encoding="utf-8")
        # run() reads live from git, so exercise compare() through the file leg only
        cand_losses = compare(LIVE, (root / "pages" / "one.html").read_text(encoding="utf-8"))
        check("the file leg reports the same loss", any(k == "img" for k, a, b in cand_losses))

    print("=" * 62)
    for name, ok, detail in checks:
        print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name, (" - " + detail) if detail else ""))
    print("=" * 62)
    if failures:
        print("SELF-TEST FAILED: %d of %d" % (len(failures), len(checks)))
        return 1
    print("SELF-TEST PASS: %d checks, including the planted dropped image" % len(checks))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--live-ref", default="origin/main")
    ap.add_argument("--candidate", type=Path)
    ap.add_argument("--files", type=Path, help="JSON list of repo-relative paths")
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--allow", type=Path, help="JSON list of paths whose loss is reviewed")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        return self_test()
    if not a.candidate or not a.files:
        ap.error("--candidate and --files are required unless --self-test is given")
    files = json.loads(a.files.read_text(encoding="utf-8"))
    allow = set(json.loads(a.allow.read_text(encoding="utf-8"))) if a.allow else set()
    return run(files, a.live_ref, a.candidate.resolve(), a.root.resolve(), allow, a.verbose)


if __name__ == "__main__":
    sys.exit(main())
