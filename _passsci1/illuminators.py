# -*- coding: utf-8 -*-
"""
Animated SVG illuminators for the Science suite, authored to the per-lesson briefs.

HOUSE RULES (each load-bearing; MASTER PROMPT §3 / Block-2 §3.3):
  * Reuse the existing illuminator keyframe vocabulary ONLY:
      ilmPop ilmDraw ilmGlow ilmSpin ilmHand ilmRide ilmRise ilmRipple ilmSweep ilmFill
    -> authoring against these adds ZERO new keyframe families, so the reduced-motion
    census is unchanged. The donor RM rule already covers everything inside `.ilm`:
      .ilm *{animation:none!important;opacity:1!important;stroke-dashoffset:0!important;transform:none!important}
  * NEVER position with transform (RM sets transform:none). Position by coordinate.
    transform is used ONLY for the animation itself, whose resting state == the coords.
  * All label text horizontal. Icon + word + colour on every tag, never colour alone.
  * Unicode characters only inside the SVG -- no named HTML entities.
  * Pair every reveal with a visible completed end state (opacity 1, dashoffset 0).
  * Calm palette, no neon/strobe. Real-bench framing: the thing as it sits on the bench.

Each function returns dict(alt=..., cap=..., svg=...).
"""
import math

_INK = "#1f2937"
_MUTE = "#94a3b8"
_TRAY = "#e2e8f0"
BUILD = "#4E7A9B"     # BUILD steel-blue
GROW = "#3F7D6E"      # GROW teal-green
OCHRE = "#C9803B"     # secondary contrast
VIOLET = "#7A5C9E"
GREEN = "#5B9E5B"
GOLD = "#D8A63B"


# ---------------------------------------------------------------- shared helpers
def _svg(inner, vb="0 0 640 300"):
    return (f'<svg viewBox="{vb}" width="100%" role="img" '
            f'xmlns="http://www.w3.org/2000/svg" font-family="system-ui,sans-serif">{inner}</svg>')


def _hdr(cx, text, color=_INK, y=40, fs=14):
    return (f'<text x="{cx}" y="{y}" text-anchor="middle" font-size="{fs}" font-weight="800" '
            f'fill="{color}" font-family="system-ui,sans-serif">{text}</text>')


def _lbl(x, y, w, text, color, delay=1.0, h=24, fs=14):
    """Horizontal white pill label carrying an icon+word tag; revealed with ilmRise."""
    return (f'<g style="animation:ilmRise .5s ease-out both;animation-delay:{delay}s">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#ffffff" '
            f'stroke="{color}" stroke-width="1.8"/>'
            f'<text x="{x+11}" y="{y+h-7}" font-size="{fs}" font-weight="800" fill="{color}" '
            f'font-family="system-ui,sans-serif">{text}</text></g>')


def _tray(text="specimen tray · school lab bench"):
    return (f'<rect x="24" y="238" width="592" height="16" rx="5" fill="{_TRAY}" '
            f'stroke="{_MUTE}" stroke-width="1"/>'
            f'<text x="320" y="250" text-anchor="middle" font-size="10.5" fill="#64748b" '
            f'font-family="system-ui,sans-serif">{text}</text>')


def _divider(x=320):
    return f'<line x1="{x}" y1="30" x2="{x}" y2="230" stroke="{_MUTE}" stroke-width="1" stroke-dasharray="4 5"/>'


def _arrow(x0, y0, x1, y1, color, w=3, delay=0.4):
    """Straight arrow with a head, drawn in with ilmDraw (resting state = fully drawn)."""
    ang = math.atan2(y1 - y0, x1 - x0)
    hx, hy = x1 - 12 * math.cos(ang), y1 - 12 * math.sin(ang)
    lx, ly = hx - 7 * math.sin(ang), hy + 7 * math.cos(ang)
    rx, ry = hx + 7 * math.sin(ang), hy - 7 * math.cos(ang)
    return (f'<line x1="{x0:.0f}" y1="{y0:.0f}" x2="{x1:.0f}" y2="{y1:.0f}" stroke="{color}" '
            f'stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M {x1:.0f} {y1:.0f} L {lx:.0f} {ly:.0f} L {rx:.0f} {ry:.0f} Z" fill="{color}"/>')


# ================================================================ BUILD W3
def backbones():
    BB, HC = BUILD, OCHRE
    verts = "".join(
        f'<rect x="{74 + i*18}" y="142" width="13" height="18" rx="3" fill="{BB}" '
        f'stroke="{_INK}" stroke-width="1.2" style="animation:ilmPop .4s ease-out both;'
        f'animation-delay:{0.15 + i*0.09:.2f}s"/>' for i in range(10))
    ribs = "".join(
        f'<path d="M {80 + i*30} 150 q 12 26 2 46" fill="none" stroke="{_MUTE}" stroke-width="1.6"/>'
        f'<path d="M {80 + i*30} 150 q 12 -26 2 -46" fill="none" stroke="{_MUTE}" stroke-width="1.6"/>'
        for i in range(5))
    fish = (f'<path d="M 250 150 l 34 -20 l 0 40 z" fill="none" stroke="{_MUTE}" stroke-width="1.8"/>'
            f'<circle cx="64" cy="150" r="15" fill="none" stroke="{_MUTE}" stroke-width="1.8"/>')
    beetle = (
        f'<ellipse cx="470" cy="150" rx="52" ry="66" fill="{HC}" fill-opacity="0.30" stroke="{HC}" stroke-width="2.4"/>'
        f'<line x1="470" y1="92" x2="470" y2="212" stroke="{HC}" stroke-width="2.4"/>'
        f'<ellipse cx="470" cy="96" rx="26" ry="18" fill="{HC}" fill-opacity="0.30" stroke="{HC}" stroke-width="2.2"/>'
        f'<circle cx="470" cy="74" r="12" fill="none" stroke="{_INK}" stroke-width="1.8"/>'
        f'<path d="M 462 66 q -12 -12 -20 -8" fill="none" stroke="{_INK}" stroke-width="1.6"/>'
        f'<path d="M 478 66 q 12 -12 20 -8" fill="none" stroke="{_INK}" stroke-width="1.6"/>')
    legs = "".join(
        f'<path d="M 418 {120+i*34} q -20 4 -34 {6+i*4}" fill="none" stroke="{_INK}" stroke-width="1.8"/>'
        f'<path d="M 522 {120+i*34} q 20 4 34 {6+i*4}" fill="none" stroke="{_INK}" stroke-width="1.8"/>'
        for i in range(3))
    lens = (f'<circle cx="150" cy="150" r="40" fill="#ffffff" fill-opacity="0.10" stroke="{_INK}" '
            f'stroke-width="2.6" style="animation:ilmGlow 3.4s ease-in-out infinite"/>'
            f'<line x1="179" y1="179" x2="212" y2="212" stroke="{_INK}" stroke-width="5" stroke-linecap="round"/>')
    inner = (_hdr(150, "FISH — vertebrate") + _hdr(470, "BEETLE — invertebrate") + _divider()
             + _tray() + ribs + fish + verts + lens + beetle + legs
             + _lbl(70, 96, 150, "● BACKBONE", BB, 1.1)
             + _lbl(372, 150, 196, "■ HARD CASE OUTSIDE", HC, 1.3))
    return dict(
        alt=("Two specimens on a lab tray. Left: a fish skeleton with the line of backbone blocks "
             "picked out in blue under a hand lens, labelled circle and the word BACKBONE. Right: a "
             "beetle with its hard outer case in orange, labelled square and HARD CASE OUTSIDE."),
        cap=("On the bench: the fish keeps its shape with a line of small bones down the middle "
             "(● BACKBONE); the beetle keeps its shape with a hard case outside (■ HARD CASE OUTSIDE)."),
        svg=_svg(inner))


# ================================================================ BUILD W4
def muscle_pairs():
    CON, REL = BUILD, _MUTE
    # Frame 1 — ARM BENDS (shoulder 70,80)
    bend = (
        f'<line x1="70" y1="80" x2="70" y2="176" stroke="{_INK}" stroke-width="7" stroke-linecap="round"/>'
        f'<line x1="70" y1="176" x2="146" y2="112" stroke="{_INK}" stroke-width="7" stroke-linecap="round"/>'
        f'<circle cx="70" cy="176" r="6" fill="#fff" stroke="{_INK}" stroke-width="2"/>'
        f'<circle cx="150" cy="110" r="8" fill="none" stroke="{_INK}" stroke-width="2"/>'
        f'<line x1="76" y1="100" x2="120" y2="132" stroke="{CON}" stroke-width="9" stroke-linecap="round"/>'  # biceps thick
        f'<line x1="60" y1="100" x2="118" y2="150" stroke="{REL}" stroke-width="3" stroke-linecap="round"/>')  # triceps thin
    # Frame 2 — ARM STRAIGHTENS (shoulder 410,80)
    straight = (
        f'<line x1="410" y1="80" x2="410" y2="176" stroke="{_INK}" stroke-width="7" stroke-linecap="round"/>'
        f'<line x1="410" y1="176" x2="486" y2="196" stroke="{_INK}" stroke-width="7" stroke-linecap="round"/>'
        f'<circle cx="410" cy="176" r="6" fill="#fff" stroke="{_INK}" stroke-width="2"/>'
        f'<circle cx="490" cy="198" r="8" fill="none" stroke="{_INK}" stroke-width="2"/>'
        f'<line x1="404" y1="100" x2="452" y2="170" stroke="{CON}" stroke-width="9" stroke-linecap="round"/>'  # triceps thick
        f'<line x1="416" y1="100" x2="470" y2="182" stroke="{REL}" stroke-width="3" stroke-linecap="round"/>')  # biceps thin
    inner = (_hdr(150, "ARM BENDS") + _hdr(470, "ARM STRAIGHTENS") + _divider()
             + _tray("model arm — cardboard, split pin & elastic bands")
             + bend + straight
             + _lbl(90, 96, 176, "▲ BICEPS · CONTRACTS", CON, 1.0)
             + _lbl(30, 158, 150, "▽ TRICEPS · RELAXES", _INK, 1.15, fs=12)
             + _lbl(392, 96, 190, "▲ TRICEPS · CONTRACTS", CON, 1.3)
             + _lbl(452, 178, 150, "▽ BICEPS · RELAXES", _INK, 1.45, fs=12))
    return dict(
        alt=("A cardboard model arm in two frames. Left, arm bent: the biceps band is thick and "
             "tagged triangle CONTRACTS, the triceps band thin and tagged RELAXES. Right, arm "
             "straight: the labels swap — triceps CONTRACTS, biceps RELAXES."),
        cap=("On the bench model: when the arm bends the biceps CONTRACTS (▲, thick) and the triceps "
             "RELAXES (▽, thin). Straighten it and the jobs swap. A muscle can only pull."),
        svg=_svg(inner))


# ================================================================ BUILD W5
def what_body_needs():
    cols = [(110, "⚡ ENERGY", OCHRE, ["bread", "rice", "pasta"]),
            (320, "▲ GROWTH & REPAIR", BUILD, ["eggs", "beans", "fish"]),
            (530, "⚙ KEEPS BODY WORKING", GREEN, ["fruit", "veg", "water"])]
    parts = []
    for i, (cx, head, col, foods) in enumerate(cols):
        parts.append(f'<rect x="{cx-92}" y="60" width="184" height="150" rx="12" fill="{col}" '
                     f'fill-opacity="0.10" stroke="{col}" stroke-width="2"/>')
        parts.append(_lbl(cx - 92, 66, 184, head, col, 0.6 + i * 0.2, fs=12.5))
        for j, food in enumerate(foods):
            parts.append(
                f'<g style="animation:ilmPop .4s ease-out both;animation-delay:{1.1 + i*0.2 + j*0.12:.2f}s">'
                f'<rect x="{cx-70}" y="{108+j*30}" width="140" height="24" rx="6" fill="#fff" '
                f'stroke="{_MUTE}" stroke-width="1.5"/>'
                f'<text x="{cx}" y="{125+j*30}" text-anchor="middle" font-size="13" fill="{_INK}" '
                f'font-family="system-ui,sans-serif">{food}</text></g>')
    inner = (_hdr(320, "What job does each food do?") + _tray("food picture cards on the table")
             + "".join(parts))
    return dict(
        alt=("Three job columns, each headed with an icon and word: lightning ENERGY, triangle "
             "GROWTH AND REPAIR, cog KEEPS THE BODY WORKING. Food cards sit under each column."),
        cap=("Three jobs food does, each headed by icon + word: ⚡ ENERGY, ▲ GROWTH & REPAIR, "
             "⚙ KEEPS THE BODY WORKING. Sort by the job, never by good or bad."),
        svg=_svg(inner))


# ================================================================ BUILD W6
def balanced_plate():
    cx, cy, r = 180, 150, 96
    segs = [("Fruit & veg", 0.39, "BIGGEST", GREEN, "●"),
            ("Starchy foods", 0.37, "BIG", OCHRE, "■"),
            ("Protein", 0.12, "MEDIUM", BUILD, "▲"),
            ("Dairy", 0.08, "SMALL", VIOLET, "◆"),
            ("Oils & spreads", 0.04, "SMALL", GOLD, "○")]
    wedges, icons = [], []
    a = -math.pi / 2
    for name, frac, size, col, ic in segs:
        a1 = a + frac * 2 * math.pi
        x0, y0 = cx + r * math.cos(a), cy + r * math.sin(a)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        large = 1 if (a1 - a) > math.pi else 0
        wedges.append(f'<path d="M {cx} {cy} L {x0:.1f} {y0:.1f} A {r} {r} 0 {large} 1 {x1:.1f} {y1:.1f} Z" '
                      f'fill="{col}" fill-opacity="0.30" stroke="{col}" stroke-width="1.8"/>')
        am = (a + a1) / 2
        icons.append(f'<text x="{cx + 0.6*r*math.cos(am):.0f}" y="{cy + 0.6*r*math.sin(am)+5:.0f}" '
                     f'text-anchor="middle" font-size="15" font-weight="800" fill="{col}">{ic}</text>')
        a = a1
    plate = (f'<circle cx="{cx}" cy="{cy}" r="{r+6}" fill="none" stroke="{_INK}" stroke-width="2.5"/>'
             + "".join(wedges) + "".join(icons))
    # keyed legend on the right, horizontal, icon+word+size
    legend = "".join(
        _lbl(320, 60 + i * 34, 300, f'{ic} {name} — {size} SECTION', col, 0.8 + i * 0.12, h=26, fs=12.5)
        for i, (name, frac, size, col, ic) in enumerate(segs))
    inner = (_hdr(180, "The balanced plate") + _tray("the Eatwell plate on the bench")
             + plate + legend)
    return dict(
        alt=("An Eatwell-style plate split into five wedges, each with an icon and a size word: "
             "fruit and veg is the biggest section, then starchy foods, protein, dairy, and oils "
             "the smallest. A keyed list on the right repeats each label in words."),
        cap=("The plate read by icon + word + size, not colour alone: ● fruit & veg is BIGGEST, "
             "○ oils & spreads the SMALLEST. Balance is some from each, not equal slices."),
        svg=_svg(inner))


# ================================================================ BUILD W7
def food_chain():
    nodes = [("grass", 90, "■ PRODUCER · MAKES ITS OWN", GREEN),
             ("rabbit", 320, "● CONSUMER · MUST EAT", BUILD),
             ("fox", 550, "● CONSUMER · MUST EAT", BUILD)]
    parts = []
    for i, (name, cx, tag, col) in enumerate(nodes):
        parts.append(
            f'<g style="animation:ilmPop .45s ease-out both;animation-delay:{0.4+i*0.3:.2f}s">'
            f'<circle cx="{cx}" cy="140" r="40" fill="{col}" fill-opacity="0.16" stroke="{col}" stroke-width="2.4"/>'
            f'<text x="{cx}" y="146" text-anchor="middle" font-size="15" font-weight="800" fill="{_INK}">{name}</text></g>')
        parts.append(_lbl(cx - 92, 190, 184, tag, col, 1.2 + i * 0.2, fs=11))
    arrows = ""
    for (x0, x1) in [(140, 275), (370, 505)]:
        arrows += _arrow(x0, 140, x1, 140, _INK, 3)
        mid = (x0 + x1) / 2
        arrows += (f'<text x="{mid:.0f}" y="128" text-anchor="middle" font-size="11" font-weight="800" '
                   f'fill="{_INK}">IS EATEN BY</text>')
    inner = (_hdr(320, "Read the arrow: IS EATEN BY") + _tray("food-chain cards on the wall")
             + arrows + "".join(parts))
    return dict(
        alt=("A horizontal food chain: grass, arrow, rabbit, arrow, fox. Each arrow carries the "
             "words IS EATEN BY. Grass is tagged square PRODUCER MAKES ITS OWN; rabbit and fox are "
             "tagged circle CONSUMER MUST EAT."),
        cap=("The arrow means IS EATEN BY, and the chain starts with a plant: ■ PRODUCER (grass) "
             "→ ● CONSUMER (rabbit) → ● CONSUMER (fox). Icon + word on every tag."),
        svg=_svg(inner))


# ================================================================ GROW W3
def friction():
    parts = []
    # Frame 1 rough (ramp left), short travel; Frame 2 smooth (ramp right), long travel
    for i, (x, head, hatch, dist, col) in enumerate(
            [(60, "■ ROUGH SURFACE · MORE FRICTION", True, 40, GROW),
             (360, "▭ SMOOTH SURFACE · LESS FRICTION", False, 150, OCHRE)]):
        parts.append(f'<line x1="{x}" y1="90" x2="{x+150}" y2="180" stroke="{_INK}" stroke-width="4"/>')
        parts.append(f'<line x1="{x}" y1="180" x2="{x+230}" y2="180" stroke="{_INK}" stroke-width="4"/>')
        if hatch:
            parts.append("".join(f'<line x1="{x+18+j*20}" y1="180" x2="{x+12+j*20}" y2="188" '
                                 f'stroke="{_MUTE}" stroke-width="1.6"/>' for j in range(10)))
        # block on the ramp
        parts.append(f'<rect x="{x+70}" y="118" width="26" height="20" rx="3" fill="{col}" '
                     f'fill-opacity="0.4" stroke="{col}" stroke-width="2" '
                     f'style="animation:ilmPop .4s ease-out both;animation-delay:{0.6+i*0.3}s"/>')
        # travel arrow along the flat
        parts.append(_arrow(x + 150, 172, x + 150 + dist, 172, col, 4, 0.8))
        parts.append(_lbl(x - 6, 200, 250, head, col, 1.1 + i * 0.2, fs=11))
    # friction arrow opposing motion (on the first ramp block)
    parts.append(_arrow(150, 130, 118, 130, "#b91c1c", 3))
    parts.append(f'<text x="90" y="120" font-size="10.5" font-weight="800" fill="#b91c1c">FRICTION ACTS THIS WAY</text>')
    inner = (_hdr(320, "Same block, one thing changed: the surface")
             + _tray("ramp, block & metre rule on the bench") + "".join(parts))
    return dict(
        alt=("Two ramps. Left, a rough hatched surface tagged square MORE FRICTION with a short "
             "travel arrow and a friction arrow pointing back against the motion. Right, a smooth "
             "surface tagged MORE FRICTION-less with a long travel arrow."),
        cap=("Change one thing — the surface. ■ ROUGH gives MORE FRICTION and a short run; ▭ SMOOTH "
             "gives less and a long run. Friction always acts against the motion."),
        svg=_svg(inner))


# ================================================================ GROW W4
def mechanisms():
    parts = []
    for i, (x, pivx, head) in enumerate(
            [(40, 150, "EFFORT: HARDER · HAND MOVES LESS"),
             (360, 470, "EFFORT: EASIER · HAND MOVES FURTHER")]):
        bx0, bx1 = x + 10, x + 240
        parts.append(f'<line x1="{bx0}" y1="150" x2="{bx1}" y2="150" stroke="{_INK}" stroke-width="6" stroke-linecap="round"/>')
        # pivot triangle
        parts.append(f'<path d="M {pivx-12} 172 L {pivx+12} 172 L {pivx} 150 Z" fill="{GROW}" stroke="{_INK}" stroke-width="1.5"/>')
        parts.append(_lbl(pivx - 34, 176, 68, "▲ PIVOT", GROW, 0.7 + i * 0.2, h=20, fs=11))
        # load on the near end (left)
        parts.append(f'<rect x="{bx0-4}" y="120" width="26" height="26" rx="3" fill="{OCHRE}" fill-opacity="0.4" stroke="{OCHRE}" stroke-width="2"/>')
        # effort distance arrow on the far end (right) — longer in frame 2
        d = 22 if i == 0 else 44
        parts.append(_arrow(bx1, 150 - 22, bx1, 150 - 22 - d, GROW, 3, 0.9))
        parts.append(_lbl(x - 4, 196, 262, head, _INK, 1.2 + i * 0.2, fs=10.5))
    inner = (_hdr(320, "Move the pivot: gain force, pay in distance")
             + _tray("metre rule, pencil pivot & 100 g masses") + "".join(parts))
    return dict(
        alt=("Two levers, each a bar on a triangular pivot tagged triangle PIVOT with a load at the "
             "left end. Left: pivot central, tagged EFFORT HARDER, short effort arrow. Right: pivot "
             "near the load, tagged EFFORT EASIER, a longer effort arrow."),
        cap=("Slide the ▲ PIVOT toward the load and the lift gets EASIER — but the hand travels "
             "FURTHER. A mechanism trades distance for force; it never gives force for free."),
        svg=_svg(inner))


# ================================================================ GROW W5
def fair_test():
    boxes = [("◆ I CHANGE (one only)", "the surface", GROW, 40),
             ("■ I KEEP THE SAME", "ramp · trolley · push", OCHRE, 235),
             ("▶ I MEASURE (with units)", "distance in cm", BUILD, 430)]
    parts = []
    for i, (head, body, col, x) in enumerate(boxes):
        parts.append(f'<rect x="{x}" y="60" width="170" height="96" rx="12" fill="{col}" '
                     f'fill-opacity="0.10" stroke="{col}" stroke-width="2" '
                     f'style="animation:ilmPop .4s ease-out both;animation-delay:{0.5+i*0.25}s"/>')
        parts.append(_lbl(x + 4, 66, 162, head, col, 0.8 + i * 0.2, fs=11))
        parts.append(f'<text x="{x+85}" y="128" text-anchor="middle" font-size="12.5" fill="{_INK}">{body}</text>')
    # results table with three repeat columns + mean
    tx, ty = 60, 176
    heads = ["surface", "try 1", "try 2", "try 3", "mean"]
    cols = len(heads)
    cw = 104
    tbl = [f'<rect x="{tx}" y="{ty}" width="{cw*cols}" height="46" fill="#fff" stroke="{_INK}" stroke-width="1.5"/>']
    for c in range(1, cols):
        tbl.append(f'<line x1="{tx+c*cw}" y1="{ty}" x2="{tx+c*cw}" y2="{ty+46}" stroke="{_MUTE}" stroke-width="1"/>')
    tbl.append(f'<line x1="{tx}" y1="{ty+23}" x2="{tx+cw*cols}" y2="{ty+23}" stroke="{_MUTE}" stroke-width="1"/>')
    for c, h in enumerate(heads):
        tbl.append(f'<text x="{tx+c*cw+cw/2:.0f}" y="{ty+15}" text-anchor="middle" font-size="11" '
                   f'font-weight="800" fill="{_INK}">{h}</text>')
    inner = (_hdr(320, "Change one thing · keep the rest the same")
             + _tray("trolley, ramp & metre rule on the bench")
             + "".join(parts) + "".join(tbl))
    return dict(
        alt=("A three-box planning frame: diamond I CHANGE one thing (the surface), square I KEEP "
             "THE SAME (ramp, trolley, push), triangle-play I MEASURE distance in centimetres. Below, "
             "a results table with three repeat columns and a mean column."),
        cap=("Plan a fair test: ◆ I CHANGE one thing, ■ I KEEP THE SAME the rest, ▶ I MEASURE with "
             "units — then three repeats and a mean. Icon + word on every box."),
        svg=_svg(inner))


# ================================================================ GROW W6
def earth_and_planets():
    names = [("Mercury", "●", GROW), ("Venus", "●", GROW), ("Earth", "●", GROW), ("Mars", "●", GROW),
             ("Jupiter", "○", OCHRE), ("Saturn", "○", OCHRE), ("Uranus", "○", OCHRE), ("Neptune", "○", OCHRE)]
    sun = (f'<circle cx="40" cy="150" r="30" fill="{GOLD}" fill-opacity="0.5" stroke="{GOLD}" stroke-width="2.5"/>'
           f'<text x="40" y="196" text-anchor="middle" font-size="10.5" font-weight="800" fill="{_INK}">Sun</text>')
    planets = []
    for i, (name, ic, col) in enumerate(names):
        x = 100 + i * 62
        rr = 8 if i < 4 else 15
        planets.append(
            f'<g style="animation:ilmPop .4s ease-out both;animation-delay:{0.5+i*0.12:.2f}s">'
            f'<circle cx="{x}" cy="150" r="{rr}" fill="{col}" fill-opacity="0.35" stroke="{col}" stroke-width="2"/>'
            f'<text x="{x}" y="{150-rr-6}" text-anchor="middle" font-size="9.5" fill="{_INK}">{name}</text>'
            f'<text x="{x}" y="{150+rr+13}" text-anchor="middle" font-size="11" font-weight="800" fill="{col}">{ic}</text></g>')
    # orbit inset: gravity inward + motion sideways
    inset = (f'<circle cx="500" cy="235" r="4" fill="{GOLD}"/>'
             f'<circle cx="560" cy="235" r="6" fill="{GROW}" fill-opacity="0.4" stroke="{GROW}" stroke-width="1.5"/>'
             + _arrow(560, 229, 560, 210, BUILD, 2.4)
             + _arrow(554, 235, 512, 235, "#b91c1c", 2.4))
    inner = (_hdr(320, "Order from the Sun · rocky then giant", y=26)
             + _hdr(320, "● rocky (inner)   ○ gas / ice giant (outer)", _MUTE, y=286, fs=11)
             + sun + "".join(planets)
             + f'<text x="500" y="205" font-size="9.5" font-weight="800" fill="{BUILD}">MOTION SIDEWAYS</text>'
             + f'<text x="470" y="252" font-size="9.5" font-weight="800" fill="#b91c1c">GRAVITY PULLS IN</text>'
             + inset)
    return dict(
        alt=("The Sun at the left with the eight planets in order. The four inner planets are small "
             "and tagged with a filled circle ROCKY; the four outer planets are larger and tagged "
             "with an open circle GAS or ICE GIANT. An inset shows one orbit with a red arrow for "
             "gravity pulling inward and a blue arrow for motion going sideways."),
        cap=("Order from the Sun, read by icon + word: ● rocky inner planets, ○ gas and ice giants "
             "outer. The inset shows why they orbit — gravity pulls in, motion goes sideways."),
        svg=_svg(inner))


# ================================================================ GROW W7
def the_moon():
    cx, cy, R = 200, 146, 84
    earth = (f'<circle cx="{cx}" cy="{cy}" r="20" fill="{BUILD}" fill-opacity="0.4" stroke="{BUILD}" stroke-width="2"/>'
             f'<text x="{cx}" y="{cy+36}" text-anchor="middle" font-size="10" font-weight="800" fill="{_INK}">Earth</text>')
    # sunlight arrows from the left (one side always lit)
    sun = "".join(_arrow(20, 86 + k * 40, 55, 86 + k * 40, GOLD, 2.4) for k in range(4))
    moons = []
    # Sunlight comes from the LEFT, so the Moon's left half is always lit. The phase Earth
    # SEES depends on where the Moon sits: between Earth and Sun (left, k=6) = NEW; opposite
    # the Sun (right, k=2) = FULL; top/bottom (k=0,4) = HALF. Getting this right is the lesson.
    labels = ["HALF", "", "FULL", "", "HALF", "", "NEW", ""]
    for k in range(8):
        a = -math.pi / 2 + k * (math.pi / 4)
        mx, my = cx + R * math.cos(a), cy + R * math.sin(a)
        # half always lit: left half filled (facing the Sun), right half dark
        moons.append(
            f'<g style="animation:ilmPop .35s ease-out both;animation-delay:{0.4+k*0.1:.2f}s">'
            f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="11" fill="#1f2937" stroke="{_INK}" stroke-width="1.2"/>'
            f'<path d="M {mx:.0f} {my-11:.0f} A 11 11 0 0 0 {mx:.0f} {my+11:.0f} Z" fill="{GOLD}"/></g>')
        if labels[k]:
            moons.append(f'<text x="{mx:.0f}" y="{my-16:.0f}" text-anchor="middle" font-size="10" '
                         f'font-weight="800" fill="{_INK}">{labels[k]}</text>')
    note = _lbl(360, 120, 250, "HALF IS ALWAYS LIT", GROW, 1.2, fs=12)
    note2 = _lbl(360, 150, 250, "OUR ANGLE CHANGES", OCHRE, 1.35, fs=12)
    inner = (_hdr(200, "Why the Moon looks different", y=26)
             + _tray("torch (Sun), ball (Moon), your head (Earth)")
             + f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{_MUTE}" stroke-width="1" stroke-dasharray="4 5"/>'
             + sun + earth + "".join(moons) + note + note2
             + f'<text x="40" y="80" font-size="9.5" font-weight="800" fill="{GOLD}">SUNLIGHT</text>')
    return dict(
        alt=("The Earth at the centre of a dashed orbit with eight Moon positions around it. Sunlight "
             "arrows come from the left, so each Moon has its left half lit and right half dark. The "
             "phases we see are labelled NEW, HALF and FULL. A note reads HALF IS ALWAYS LIT, OUR "
             "ANGLE CHANGES."),
        cap=("Torch-and-ball model: sunlight lights one half of the Moon always; as it orbits, our "
             "angle changes, so we see NEW, HALF, FULL. The phases are not the Earth's shadow."),
        svg=_svg(inner))


# ================================================================ LAUNCH W3 · L1
def launch_microscope():
    V = VIOLET
    # light microscope, schematic, on the bench
    body = (
        f'<rect x="70" y="228" width="150" height="14" rx="4" fill="{_TRAY}" stroke="{_MUTE}"/>'  # base
        f'<path d="M 120 228 Q 96 150 130 120" fill="none" stroke="{_INK}" stroke-width="6"/>'      # arm
        # eyepiece tube + lens (top)
        f'<rect x="118" y="60" width="26" height="40" rx="4" fill="#fff" stroke="{_INK}" stroke-width="2"/>'
        f'<ellipse cx="131" cy="60" rx="15" ry="6" fill="{V}" fill-opacity="0.4" stroke="{V}" stroke-width="2"/>'
        # nosepiece + objectives
        f'<rect x="112" y="118" width="60" height="14" rx="6" fill="#fff" stroke="{_INK}" stroke-width="2"/>'
        f'<rect x="118" y="132" width="10" height="22" rx="2" fill="{V}" fill-opacity="0.3" stroke="{V}" stroke-width="1.6"/>'
        f'<rect x="132" y="132" width="10" height="28" rx="2" fill="{V}" fill-opacity="0.3" stroke="{V}" stroke-width="1.6"/>'
        f'<rect x="146" y="132" width="10" height="34" rx="2" fill="{V}" fill-opacity="0.3" stroke="{V}" stroke-width="1.6"/>'
        # stage + slide
        f'<rect x="96" y="176" width="90" height="10" rx="2" fill="#fff" stroke="{_INK}" stroke-width="2"/>'
        f'<rect x="122" y="170" width="34" height="6" rx="1" fill="{V}" fill-opacity="0.5" stroke="{V}" stroke-width="1.4"/>'
        # focus wheel
        f'<circle cx="96" cy="150" r="10" fill="#fff" stroke="{_INK}" stroke-width="2" '
        f'style="animation:ilmGlow 3.6s ease-in-out infinite"/>'
        # light
        f'<circle cx="141" cy="205" r="9" fill="{GOLD}" fill-opacity="0.6" stroke="{GOLD}" stroke-width="1.6"/>')
    # two comparison image circles (magnify vs resolve)
    sharp = "".join(f'<circle cx="{430+ (i%3)*16}" cy="{110+(i//3)*16}" r="3.5" fill="{V}"/>' for i in range(6))
    blur = "".join(f'<circle cx="{430+(i%3)*16}" cy="{190+(i//3)*16}" r="6" fill="{_MUTE}" fill-opacity="0.5"/>' for i in range(6))
    circles = (
        f'<circle cx="446" cy="118" r="42" fill="none" stroke="{_INK}" stroke-width="2"/>{sharp}'
        f'<circle cx="446" cy="198" r="42" fill="none" stroke="{_INK}" stroke-width="2"/>{blur}')
    inner = (_hdr(140, "A light microscope on the bench", y=32)
             + body + circles
             + _lbl(150, 46, 150, "● EYEPIECE ×10", V, 0.9, fs=12)
             + _lbl(180, 128, 160, "■ OBJECTIVE ×4/×10/×40", V, 1.1, fs=11)
             + _lbl(40, 190, 130, "◆ STAGE + SLIDE", _INK, 1.25, fs=11)
             + _lbl(70, 268, 210, "specimen slide · school lab microscope", _MUTE, 1.4, h=20, fs=10)
             + _lbl(500, 100, 120, "BIGGER · CLEARER", V, 1.4, h=22, fs=11)
             + _lbl(500, 190, 120, "BIGGER · BLURRY", _MUTE, 1.5, h=22, fs=11))
    return dict(
        alt=("A light microscope on the lab bench with the eyepiece lens (×10), the revolving "
             "objective lenses (×4, ×10, ×40), the stage with a slide, the focus wheel and the "
             "light all labelled. Two image circles compare a sharp 'bigger and clearer' view with "
             "a fuzzy 'bigger but blurry' one."),
        cap=("On the bench: light enters through the slide, the objective and eyepiece lenses "
             "multiply to magnify. More magnification only helps if the image stays clear — "
             "resolution, not just size."),
        svg=_svg(inner))


# ================================================================ LAUNCH W3 · L2
def launch_formula_triangle():
    V = VIOLET
    # triangle: IMAGE SIZE on top row, MAGNIFICATION x ACTUAL SIZE on bottom row
    tri = (
        f'<path d="M 150 70 L 60 210 L 240 210 Z" fill="{V}" fill-opacity="0.10" stroke="{V}" stroke-width="2.5"/>'
        f'<line x1="60" y1="150" x2="240" y2="150" stroke="{V}" stroke-width="2"/>'      # horizontal divider
        f'<line x1="150" y1="150" x2="150" y2="210" stroke="{V}" stroke-width="2"/>'     # vertical divider
        f'<text x="150" y="122" text-anchor="middle" font-size="14" font-weight="800" fill="{_INK}">IMAGE SIZE</text>'
        f'<text x="105" y="188" text-anchor="middle" font-size="12.5" font-weight="800" fill="{_INK}">MAGNIF.</text>'
        f'<text x="150" y="140" text-anchor="middle" font-size="16" fill="{V}">×</text>'
        f'<text x="196" y="188" text-anchor="middle" font-size="12.5" font-weight="800" fill="{_INK}">ACTUAL</text>')
    # conversion ladder (right)
    ladder = (
        f'<rect x="360" y="90" width="70" height="30" rx="6" fill="#fff" stroke="{_INK}" stroke-width="1.8"/>'
        f'<text x="395" y="110" text-anchor="middle" font-size="15" font-weight="800" fill="{_INK}">mm</text>'
        f'<rect x="510" y="90" width="70" height="30" rx="6" fill="#fff" stroke="{_INK}" stroke-width="1.8"/>'
        f'<text x="545" y="110" text-anchor="middle" font-size="15" font-weight="800" fill="{_INK}">µm</text>'
        + _arrow(432, 100, 508, 100, V, 2.4)
        + f'<text x="470" y="88" text-anchor="middle" font-size="12" font-weight="800" fill="{V}">×1000</text>'
        + _arrow(508, 132, 432, 132, OCHRE, 2.4)
        + f'<rect x="510" y="122" width="70" height="0" />'
        + f'<text x="470" y="150" text-anchor="middle" font-size="12" font-weight="800" fill="{OCHRE}">÷1000</text>')
    inner = (_hdr(150, "The magnification triangle", y=40)
             + _hdr(470, "mm ↔ µm conversion", y=40)
             + tri + ladder
             + _lbl(60, 226, 210, "cover the one you want, read the rest", _MUTE, 1.0, h=20, fs=10.5)
             + _lbl(360, 168, 220, "match the units BEFORE you divide", V, 1.15, h=22, fs=11))
    return dict(
        alt=("A formula triangle with IMAGE SIZE across the top and MAGNIFICATION times ACTUAL SIZE "
             "along the bottom — cover the quantity you want and read off the calculation. Beside it "
             "a conversion ladder: millimetres to micrometres is times 1000, back is divide by 1000."),
        cap=("Cover what you want in the triangle: image size on top, magnification × actual size "
             "below. And match the units first — mm to µm is ×1000, back is ÷1000."),
        svg=_svg(inner))


# ================================================================ LAUNCH W3 · L3
def launch_exam_method():
    V = VIOLET
    lines = [("1", "EQUATION", "mag = image ÷ actual"),
             ("2", "UNITS CHECK", "both in mm?"),
             ("3", "SUBSTITUTE", "60 ÷ 0.15"),
             ("4", "ANSWER", "×400  (no unit)")]
    rows = "".join(
        f'<g style="animation:ilmRise .45s ease-out both;animation-delay:{0.5+i*0.25:.2f}s">'
        f'<circle cx="60" cy="{78+i*40}" r="13" fill="{V}" fill-opacity="0.4" stroke="{V}" stroke-width="1.8"/>'
        f'<text x="60" y="{83+i*40}" text-anchor="middle" font-size="13" font-weight="800" fill="{_INK}">{n}</text>'
        f'<text x="84" y="{76+i*40}" font-size="12.5" font-weight="800" fill="{_INK}">{lab}</text>'
        f'<text x="84" y="{92+i*40}" font-size="12" fill="#475569">{val}</text></g>'
        for i, (n, lab, val) in enumerate(lines))
    cmds = [("CALCULATE", "number + working", V),
            ("DESCRIBE", "what you see", OCHRE),
            ("ESTIMATE", "use the scale bar", GROW)]
    card = "".join(
        f'<g style="animation:ilmPop .4s ease-out both;animation-delay:{1.4+i*0.15:.2f}s">'
        f'<rect x="360" y="{70+i*46}" width="230" height="38" rx="8" fill="{col}" fill-opacity="0.10" stroke="{col}" stroke-width="1.8"/>'
        f'<text x="374" y="{88+i*46}" font-size="13" font-weight="800" fill="{col}">▸ {cw}</text>'
        f'<text x="374" y="{102+i*46}" font-size="11.5" fill="#475569">{ask}</text></g>'
        for i, (cw, ask, col) in enumerate(cmds))
    inner = (_hdr(150, "Four lines, every calculation", y=36)
             + _hdr(475, "Read the command word", y=36)
             + rows + card)
    return dict(
        alt=("A worked exam answer laid out as four numbered lines: equation, units check, "
             "substitute, answer with no unit. Beside it a command-word card: CALCULATE means "
             "number plus working, DESCRIBE means what you see, ESTIMATE means use the scale bar."),
        cap=("Every calculation, four lines: equation, units check, substitute, answer. And the "
             "command word decides the shape — ▸ CALCULATE, ▸ DESCRIBE, ▸ ESTIMATE ask for "
             "different things."),
        svg=_svg(inner))


# ================================================================ LAUNCH W4 · L1
def launch_diffusion():
    V = VIOLET
    import random as _r  # not used; keep deterministic below
    # two chambers separated by a dashed membrane
    left = "".join(f'<circle cx="{60 + (i % 6) * 18}" cy="{80 + (i // 6) * 18}" r="4" fill="{V}"/>'
                   for i in range(24))
    right = "".join(f'<circle cx="{360 + (i % 3) * 30}" cy="{86 + (i // 3) * 30}" r="4" fill="{_MUTE}"/>'
                    for i in range(6))
    chambers = (
        f'<rect x="44" y="64" width="200" height="120" rx="8" fill="{V}" fill-opacity="0.06" stroke="{_INK}" stroke-width="2"/>'
        f'<rect x="352" y="64" width="200" height="120" rx="8" fill="{_MUTE}" fill-opacity="0.06" stroke="{_INK}" stroke-width="2"/>'
        f'<line x1="298" y1="60" x2="298" y2="188" stroke="{_INK}" stroke-width="2.5" stroke-dasharray="5 5"/>'
        + left + right)
    net = (_arrow(250, 110, 346, 110, V, 6)
           + f'<text x="298" y="100" text-anchor="middle" font-size="12" font-weight="800" fill="{V}">NET MOVEMENT</text>'
           + _arrow(346, 150, 250, 150, _MUTE, 2))
    factors = "".join(
        _lbl(40 + i * 200, 210, 180, tag, col, 0.9 + i * 0.15, h=22, fs=11)
        for i, (tag, col) in enumerate([("↑ STEEPER GRADIENT", V), ("↑ HIGHER TEMPERATURE", OCHRE),
                                        ("↑ MORE SURFACE AREA", GROW)]))
    inner = (_lbl(70, 40, 150, "● HIGH CONCENTRATION", V, 0.6, h=22, fs=11)
             + _lbl(372, 40, 150, "○ LOW CONCENTRATION", _INK, 0.75, h=22, fs=11)
             + chambers + net + factors)
    return dict(
        alt=("Two chambers either side of a dashed membrane. The left is densely dotted, tagged "
             "circle HIGH CONCENTRATION; the right is sparsely dotted, tagged open-circle LOW "
             "CONCENTRATION. A thick arrow labelled NET MOVEMENT points from high to low. Three "
             "tags below name what speeds diffusion up: steeper gradient, higher temperature, "
             "more surface area."),
        cap=("Diffusion is the NET movement from ● high to ○ low concentration, down the gradient. "
             "It goes faster with a steeper gradient, higher temperature or more surface area."),
        svg=_svg(inner))


# ================================================================ LAUNCH W4 · L2
def launch_gas_exchange():
    V = VIOLET
    # alveolus + capillary
    alv = (f'<circle cx="150" cy="140" r="60" fill="#fff" stroke="{_INK}" stroke-width="2.5"/>'
           f'<text x="150" y="145" text-anchor="middle" font-size="12" font-weight="800" fill="{_INK}">alveolus</text>'
           f'<path d="M 205 100 Q 250 140 205 180" fill="none" stroke="#b91c1c" stroke-width="10" stroke-opacity="0.35"/>'
           f'<text x="238" y="205" text-anchor="middle" font-size="10.5" fill="#7f1d1d">capillary</text>')
    o2 = _arrow(180, 120, 214, 128, V, 3) + f'<text x="196" y="112" font-size="11" font-weight="800" fill="{V}">● O2 IN</text>'
    co2 = _arrow(214, 172, 180, 164, _INK, 3) + f'<text x="150" y="200" font-size="11" font-weight="800" fill="{_INK}">○ CO2 OUT</text>'
    # two limewater tubes
    tubes = (
        f'<rect x="470" y="90" width="26" height="100" rx="10" fill="#e0f2fe" stroke="{_INK}" stroke-width="2"/>'
        f'<text x="483" y="210" text-anchor="middle" font-size="10" font-weight="800" fill="{_INK}">CLEAR</text>'
        f'<rect x="540" y="90" width="26" height="100" rx="10" fill="#d9cbe6" stroke="{_INK}" stroke-width="2"/>'
        f'<text x="553" y="210" text-anchor="middle" font-size="10" font-weight="800" fill="{_INK}">CLOUDY</text>')
    inner = (_hdr(150, "Gas exchange in one alveolus", y=32)
             + _hdr(518, "limewater test", y=32)
             + alv + o2 + co2 + tubes
             + _lbl(300, 60, 140, "■ LARGE SURFACE AREA", V, 0.9, h=20, fs=10)
             + _lbl(300, 86, 150, "■ WALL ONE CELL THICK", V, 1.05, h=20, fs=10)
             + _lbl(300, 112, 150, "■ GOOD BLOOD SUPPLY", V, 1.2, h=20, fs=10)
             + _lbl(452, 214, 130, "clear = no CO2", _MUTE, 1.3, h=18, fs=9.5)
             + _lbl(524, 214, 130, "cloudy = CO2 present", V, 1.35, h=18, fs=9.5))
    return dict(
        alt=("A single alveolus wrapped by a capillary. An arrow tagged O2 IN shows oxygen "
             "diffusing into the blood; an arrow tagged CO2 OUT shows carbon dioxide diffusing out. "
             "Three adaptation tags: large surface area, wall one cell thick, good blood supply. "
             "Beside it, a clear limewater tube (no CO2) and a cloudy one (CO2 present)."),
        cap=("At the alveolus, ● O2 diffuses in and ○ CO2 diffuses out — helped by a large surface "
             "area, a one-cell-thick wall and a good blood supply. Cloudy limewater is the evidence "
             "the body makes CO2."),
        svg=_svg(inner))


# ================================================================ LAUNCH W4 · L3
def launch_diffusion_exam():
    V = VIOLET
    cards = (
        f'<rect x="40" y="70" width="250" height="40" rx="8" fill="{V}" fill-opacity="0.10" stroke="{V}" stroke-width="1.8"/>'
        f'<text x="54" y="88" font-size="13" font-weight="800" fill="{V}">▸ DESCRIBE</text>'
        f'<text x="54" y="104" font-size="11.5" fill="#475569">what happens</text>'
        f'<rect x="40" y="120" width="250" height="40" rx="8" fill="{OCHRE}" fill-opacity="0.10" stroke="{OCHRE}" stroke-width="1.8"/>'
        f'<text x="54" y="138" font-size="13" font-weight="800" fill="{OCHRE}">▸ EXPLAIN</text>'
        f'<text x="54" y="154" font-size="11.5" fill="#475569">why … because</text>')
    pts = [("1", "higher O2 in the alveolus"),
           ("2", "so it diffuses down the gradient"),
           ("3", "wall one cell thick → short distance")]
    ans = "".join(
        f'<g style="animation:ilmRise .45s ease-out both;animation-delay:{0.6+i*0.25:.2f}s">'
        f'<circle cx="360" cy="{82+i*44}" r="13" fill="{V}" fill-opacity="0.4" stroke="{V}" stroke-width="1.8"/>'
        f'<text x="360" y="{87+i*44}" text-anchor="middle" font-size="13" font-weight="800" fill="{_INK}">{n}</text>'
        f'<text x="384" y="{87+i*44}" font-size="12" fill="{_INK}">{t}</text></g>'
        for i, (n, t) in enumerate(pts))
    inner = (_hdr(155, "Command word decides the shape", y=40)
             + _hdr(470, "3 marks → 3 points", y=40)
             + cards + ans)
    return dict(
        alt=("A command-word card: DESCRIBE means what happens, EXPLAIN means why, using because. "
             "Beside it a 3-mark explain answer broken into three numbered points: higher oxygen in "
             "the alveolus, so it diffuses down the gradient, and the wall is one cell thick giving "
             "a short distance."),
        cap=("▸ DESCRIBE asks what happens; ▸ EXPLAIN asks why. A 3-mark explain needs three "
             "points: direction, gradient, adaptation."),
        svg=_svg(inner))


ILLUMINATORS = {
    "SCI_B_W3_Backbones": backbones,
    "SCI_L_W3_L1_Microscopy": launch_microscope,
    "SCI_L_W4_L1_Diffusion": launch_diffusion,
    "SCI_L_W4_L2_GasExchange": launch_gas_exchange,
    "SCI_L_W4_L3_ExamSkills": launch_diffusion_exam,
    "SCI_L_W3_L2_Magnification": launch_formula_triangle,
    "SCI_L_W3_L3_ExamSkills": launch_exam_method,
    "SCI_B_W4_Muscle_Pairs": muscle_pairs,
    "SCI_B_W5_Right_Nutrition": what_body_needs,
    "SCI_B_W6_Balanced_Plate": balanced_plate,
    "SCI_B_W7_Where_Food_Comes_From": food_chain,
    "SCI_G_W3_Friction": friction,
    "SCI_G_W4_Mechanisms": mechanisms,
    "SCI_G_W5_Fair_Test": fair_test,
    "SCI_G_W6_Earth_And_Planets": earth_and_planets,
    "SCI_G_W7_The_Moon": the_moon,
}
