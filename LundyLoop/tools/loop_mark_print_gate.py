#!/usr/bin/env python3
"""
LL-INST-09 — per-tier print gate.

Asserts that a named element actually reaches paper in each of the three tier
packs. It does NOT read the printPack array and infer. It loads the file in
Chromium, emulates print media, invokes the file's own printPack(level), and
reads back what carried .visible and what appears in the printed text.

A static read of printPack's array is a vocabulary test wearing a presence
test's clothes (LL-INST-05). This instrument tests for the thing.

Known limit, quote it with the result: this proves an element is in the print
box and in the printed text. It does not prove legibility, pagination, or the
behaviour of a specific physical printer. Greyscale and glyph-loss are asserted
separately, in-page, not here.

Usage:
    python3 loop_mark_print_gate.py <absolute-path-to-html> [more paths...]
Exit 0 if every tier passes every assertion for every file, 1 otherwise.
"""
import sys
from playwright.sync_api import sync_playwright

TIERS = ("supported", "standard", "stretch")
LABELS = ["pointed", "said it", "showed", "picture", "tried again", "filmed"]
OWN = "Ring this yourself"
PHOTO = "work, not faces, unless consent is filed"
NULL = "Nothing yet is a real answer"
RBOX = "adult initials that they received it"

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

JS_PROBE = """
(level) => {
  printPack(level);
  const strip = document.querySelector('.lm-strip');
  if (!strip) return {found:false};
  const r = strip.getBoundingClientRect();
  const cs = getComputedStyle(strip);
  const vis = [...document.querySelectorAll('.print-section.visible')];
  const sec = strip.closest('.print-section');
  const clone = strip.cloneNode(true);
  clone.querySelectorAll('.lm-g').forEach(g => g.textContent = '');
  return {
    found: true,
    h: r.height,
    display: cs.display,
    visibility: cs.visibility,
    sectionId: sec ? sec.id : null,
    sectionVisible: sec ? sec.classList.contains('visible') : false,
    visibleIds: vis.map(v => v.id),
    paper: vis.map(v => v.innerText).join('\\n'),
    noglyph: clone.innerText
  };
}
"""


def probe(page, path):
    page.add_init_script("window.print = () => { window.__printCalled = true; };")
    page.goto("file://" + path)
    page.emulate_media(media="print")
    return {t: page.evaluate(JS_PROBE, t) for t in TIERS}


def assertions(r):
    a = [
        ("strip element renders (h>0)", r["h"] > 0, f'h={r["h"]:.0f}px'),
        ("display not none", r["display"] != "none", r["display"]),
        ("visibility visible", r["visibility"] == "visible", r["visibility"]),
        ("enclosing section is print-feedback", r["sectionId"] == "print-feedback",
         str(r["sectionId"])),
        ("that section carries .visible", r["sectionVisible"], ""),
        ("strip text on paper", "How I answered it" in r["paper"], ""),
    ]
    a += [(f"label {lb!r} on paper", lb in r["paper"], "") for lb in LABELS]
    a += [
        ("ownership sentence on paper", OWN in r["paper"], ""),
        ("photo rule on paper", PHOTO in r["paper"], ""),
        ("truthful null on paper", NULL in r["paper"], ""),
        ("R box on paper", RBOX in r["paper"], ""),
        ("all labels survive glyph loss",
         all(lb in r["noglyph"] for lb in LABELS), ""),
    ]
    return a


def main(paths):
    allpass = True
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        for path in paths:
            page = b.new_page()
            res = probe(page, path)
            page.close()
            print(f"\n=== PER-TIER PRINT GATE · {path.split('/')[-1]} ===")
            for t in TIERS:
                r = res[t]
                if not r.get("found"):
                    print(f"  [{t}] STRIP ELEMENT NOT FOUND")
                    allpass = False
                    continue
                checks = assertions(r)
                n = sum(1 for _, ok, _ in checks if ok)
                print(f"  [{t}]  {n}/{len(checks)}   sections on paper: "
                      f"{len(r['visibleIds'])}")
                for name, ok, d in checks:
                    if not ok:
                        allpass = False
                        print(f"        FAIL {name} {d}")
                if n == len(checks):
                    print("        all assertions passed")
        b.close()
    print("\nPER-TIER GATE:",
          "PASS" if allpass else "FAIL — STOP, do not deploy")
    return 0 if allpass else 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: loop_mark_print_gate.py <abs-path.html> [...]")
    sys.exit(main(sys.argv[1:]))
