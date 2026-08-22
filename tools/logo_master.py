#!/usr/bin/env python3
"""Derive the optimised Progress Schools master from an attached lockup, and gate it.

    python3 tools/logo_master.py --logo PATH [--out FILE] [--plant-recolour]

REBRAND.md rule 1 wants ONE master, embedded base64 per page, no external asset.
PEQ-YEAR-3 §9.2 allows exactly one derivation - a resize-only optimised master,
target 10 KB - and requires a COLOUR-SHIFT GATE: a recolour must go red.

WHY THIS TOOL EXISTS AT ALL
---------------------------
The 2026-08-22 owner-supplied master is a 447x447 JPEG with an opaque white
background, where the canonical master is a 225x225 PNG. Two things in
build_staff_pack.load_logo() are written for the PNG and quietly fail on the JPEG:

  1. It trims and splits on EXACT white (255,255,255). JPEG ringing means the gap
     between the P mark and the wordmark is full of 254s and 253s, so the splitter
     found no blank run, returned split == full width, and every "P mark only"
     placement silently got the entire lockup instead.
  2. It palettises the noisy JPEG straight to 16 colours - the only palette that
     fit the 10 KB budget at full size - which moved mean per-channel colour by
     4.24 / 3.26 / 4.87. That is a real colour shift, on a brand mark.

Neither failed loudly. Both are the class of defect REBRAND.md's own note describes:
a placeholder ending up in a school because nothing went red.

WHAT IS AND IS NOT A PERMITTED DERIVATION
-----------------------------------------
Permitted: trim, resize (LANCZOS), and snapping the near-white FIELD to pure white.
The last is denoising a JPEG artefact, not a recolour, and it is asserted as such:
no pixel outside the white tolerance may move. Everything else - recolour, redraw,
crop into the mark, outline, re-letter - is forbidden by §9.2 and by REBRAND.md.

THE GATE IS ON THE INK, NOT THE MEAN
------------------------------------
A whole-image mean delta is dominated by the white field, which is ~35% of the
lockup: a mean of "about zero" survives a brand colour being moved a long way.
So the mean is reported, and the gate is on the two brand ink colours - navy and
magenta - which is what a recolour actually moves. --plant-recolour proves it.
"""
from __future__ import annotations

import argparse
import base64
import collections
import hashlib
import io
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

# The recorded masters. Both are named in REBRAND.md; the builder accepts either.
MASTERS = {
    "b112fd98e3368f73df4da5588a04238ee4a816b56007ba60e2e63d0286cbdb04":
        "225x225 PNG - canonical",
    "b4d75c74b428600715bdbc91f210984f9b4b9c35685d3a207372b41fa426cb92":
        "447x447 JPEG, 9,099 B - owner-supplied 2026-08-22, opaque white, no alpha",
}

# Measured from the owner-supplied master: the two brand inks. A derivation that
# moves either of these is a recolour, whatever its mean delta says.
BRAND_INK = [(41, 43, 91), (229, 3, 128)]     # navy, magenta
INK_TOLERANCE = 6.0                            # per-channel, generous for palettisation
WHITE_TOL = 8                                  # a channel this close to 255 is field, not ink
BUDGET = 10240


def trim(img, tol=12):
    """Ink bounding box, tolerant of JPEG ringing. Exact-255 matching does not work."""
    mask = ImageChops.invert(img.convert("L")).point(lambda v: 255 if v > tol else 0)
    box = mask.getbbox()
    assert box, "the supplied image is blank"
    return img.crop(box)


def snap_white(img):
    """Near-white field -> pure white. Asserts no ink pixel moves."""
    src = img.load()
    out = Image.new("RGB", img.size, (255, 255, 255))
    dst = out.load()
    moved = 0
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            p = src[x, y]
            if min(p) >= 255 - WHITE_TOL:
                if p != (255, 255, 255):
                    moved += 1
                dst[x, y] = (255, 255, 255)
            else:
                dst[x, y] = p
    return out, moved


def split_mark(lock):
    """Columns of the P mark alone, by the widest blank column run.

    Returns None when no run is found, so the caller STOPs rather than silently
    treating the whole lockup as the mark - which is what the PNG-era splitter did
    on the JPEG.
    """
    w, h = lock.size
    g = lock.convert("L")
    blank = [min(g.getpixel((x, y)) for y in range(h)) >= 255 - WHITE_TOL for x in range(w)]
    runs, run = [], None
    for x, v in enumerate(blank):
        if v:
            run = x if run is None else run
        elif run is not None:
            runs.append((run, x - run))
            run = None
    inner = [r for r in runs if r[0] > 0 and r[1] >= 6]
    if not inner:
        return None
    start, length = max(inner, key=lambda r: r[1])
    return start


def encode(img):
    """Smallest palette that fits the budget with the least colour movement."""
    best = None
    for colors in (256, 128, 64, 32, 16):
        q = img.convert("P", palette=Image.ADAPTIVE, colors=colors)
        buf = io.BytesIO()
        q.save(buf, format="PNG", optimize=True)
        d = buf.getvalue()
        if len(d) <= BUDGET:
            return d, colors
        best = (d, colors)
    return best


def nearest(colours, target):
    return min(colours, key=lambda c: sum((a - b) ** 2 for a, b in zip(c, target)))


def ink_colours(img):
    data = list(img.convert("RGB").getdata())
    return collections.Counter(p for p in data if min(p) < 200)


def derive(path, plant_recolour=False):
    raw = Path(path).read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    if got not in MASTERS:
        sys.exit(f"HARD STOP: unrecognised logo binary.\n  sha256 {got}\n"
                 "  Not one of the masters recorded in REBRAND.md. Refusing to proceed.")
    src = Image.open(io.BytesIO(raw))
    print(f"source        {src.size[0]}x{src.size[1]} {src.format} {len(raw)} B")
    print(f"              sha256 {got}")
    print(f"              matches recorded master: {MASTERS[got]}")

    rgb = src.convert("RGB")
    if plant_recolour:
        # CONTROL: rotate the brand hues. Nothing else changes. The gate must fire.
        px = rgb.load()
        for y in range(rgb.size[1]):
            for x in range(rgb.size[0]):
                r, g, b = px[x, y]
                if min(r, g, b) < 200:
                    px[x, y] = (b, r, g)
        print("              *** PLANTED RECOLOUR (channel rotation on ink) ***")

    lock = trim(rgb)
    print(f"trimmed       {lock.size[0]}x{lock.size[1]}")

    split = split_mark(lock)
    if split is None:
        sys.exit("HARD STOP: no blank column run between the P mark and the wordmark.\n"
                 "  The mark cannot be separated, and shipping the whole lockup where a\n"
                 "  mark-only footprint is expected is the defect this stop exists for.")
    print(f"P-mark split  x={split}  (mark 0..{split}, wordmark {split}..{lock.size[0]})")

    out = {}
    for name, img in (("lockup", lock), ("mark", trim(lock.crop((0, 0, split, lock.size[1]))))):
        # resize-only: 2x a ~200px display width for the lockup, ~64px for the mark
        target_w = 400 if name == "lockup" else 128
        scale = min(1.0, target_w / img.size[0])
        resized = img.resize((max(1, round(img.size[0] * scale)),
                              max(1, round(img.size[1] * scale))), Image.LANCZOS)
        snapped, moved = snap_white(resized)

        # the snap must not have touched ink
        diff = ImageChops.difference(resized, snapped)
        worst = max(max(band.getextrema()) for band in diff.split())
        assert worst <= WHITE_TOL, f"{name}: snap_white moved a pixel by {worst} (> {WHITE_TOL})"

        data, colors = encode(snapped)
        back = Image.open(io.BytesIO(data)).convert("RGB")
        mean = ImageStat.Stat(ImageChops.difference(snapped, back)).mean
        sha = hashlib.sha256(data).hexdigest()

        print(f"\n{name}")
        print(f"  derived     {resized.size[0]}x{resized.size[1]}  palette {colors}  {len(data)} B"
              f"  {'OK' if len(data) <= BUDGET else 'OVER BUDGET'}")
        print(f"  sha256      {sha}")
        print(f"  white snap  {moved} field pixel(s) to pure white, max ink movement {worst}")
        print(f"  mean delta  {[round(x, 3) for x in mean]}  (reported, not the gate)")

        derived_inks = ink_colours(back)
        ok = True
        for want in BRAND_INK:
            if not derived_inks:
                print(f"  INK GATE    RED - the derived master has no ink at all")
                ok = False
                break
            near = nearest(list(derived_inks), want)
            d = [abs(a - b) for a, b in zip(near, want)]
            verdict = "ok " if max(d) <= INK_TOLERANCE else "RED"
            if max(d) > INK_TOLERANCE:
                ok = False
            print(f"  ink gate    {verdict} brand {want} -> nearest derived {near}"
                  f"  delta {d}  (tolerance {INK_TOLERANCE})")
        out[name] = (data, sha, resized.size, len(data), colors, ok)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--logo", required=True)
    ap.add_argument("--out")
    ap.add_argument("--plant-recolour", action="store_true",
                    help="control: rotate the brand hues; the ink gate must go red")
    a = ap.parse_args()
    res = derive(a.logo, a.plant_recolour)
    bad = [n for n, v in res.items() if not v[-1] or v[3] > BUDGET]
    print()
    if bad:
        print(f"[FAIL] colour-shift / budget gate: {', '.join(bad)}")
        return 1
    print("[PASS] colour-shift gate: both brand inks preserved, both assets within budget")
    if a.out:
        Path(a.out).write_bytes(res["lockup"][0])
        print(f"       lockup written to {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
