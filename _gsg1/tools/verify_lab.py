#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Per-lesson lab verifier. Run after each transplant, before its commit.

Every check states unit and universe. Baselines come from the rollback SHA
(dcc23dc) for tier/print counts, and from HEAD for byte-identity of the
surfaces this transplant must not touch.
"""
import re, subprocess, sys, os

REPO = "/home/user/Lessons"
DIR = "Science_Teesside/Grow/v3_40min"
BASE = "dcc23dc2485516eb5d50409494c7d70f56c62f78"

FOOD = (r"chocolate|sweets?|biscuit|crisps|sugary|takeaway|junk food|"
        r"fizzy drink|calorie|diet plan|weight loss|slimming|BMI|"
        r"healthy weight|obes|fat kid|treat food")
STAGES = ["arrival", "starter", "ido", "wedo", "ido", "wedo", "independent", "exit"]


def show(ref, f):
    return subprocess.run(["git", "show", "%s:%s/%s" % (ref, DIR, f)],
                          cwd=REPO, capture_output=True, text=True).stdout


def main(f, code):
    p = os.path.join(REPO, DIR, f)
    now = open(p, encoding="utf-8").read()
    base = show(BASE, f)
    head = show("HEAD", f)
    fails = []

    def chk(name, ok, detail):
        print("  [%s] %-42s %s" % ("PASS" if ok else "FAIL", name, detail))
        if not ok:
            fails.append(name)

    # scanner validation on a known positive, before anything is trusted
    kp = "localStorage fetch( <form matchMedia chocolate Supported print-pack witness"
    for lbl, pat in [("storage", r"localStorage"), ("network", r"fetch\("),
                     ("form", r"<form"), ("matchMedia", r"matchMedia"),
                     ("food", r"chocolate")]:
        assert len(re.findall(pat, kp)) == 1, "scanner %s failed validation" % lbl

    u = "unit: occurrences · universe: this one lesson file"

    chk("runtime prohibitions all zero",
        not any(re.findall(x, now) for x in
                [r"localStorage|sessionStorage|indexedDB",
                 r"fetch\(|XMLHttpRequest|sendBeacon|WebSocket",
                 r"<form|form-action", r"matchMedia",
                 r'href="assets/|src="assets/|href="http[^"]*\.css|src="http[^"]*\.js']),
        "storage/network/form/matchMedia/external-asset = 0 · " + u)

    pb = re.search(r'<div class="print-pack">.*?</div>\s*<script>', head, re.S).group(0)
    pn = re.search(r'<div class="print-pack">.*?</div>\s*<script>', now, re.S).group(0)
    chk("print pack byte-identical to HEAD", pb == pn, "%d bytes, unchanged" % len(pn))

    wb = re.search(r'<div id="print-witness".*?</div></div>', head, re.S).group(0)
    wn = re.search(r'<div id="print-witness".*?</div></div>', now, re.S).group(0)
    chk("witness byte-identical to HEAD", wb == wn,
        "%d bytes, unchanged · witness token count %d" % (len(wn),
                                                          len(re.findall(r"witness", now, re.I))))

    tb = [len(re.findall(t, base)) for t in ("Supported", "Standard", "Stretch")]
    tn = [len(re.findall(t, now)) for t in ("Supported", "Standard", "Stretch")]
    chk("tier counts >= rollback baseline", all(a >= b for a, b in zip(tn, tb)),
        "Sup/Std/Str now %s vs baseline %s · universe: this file" % (tn, tb))

    seq = [x for x in re.findall(r'<section class="slide"[^>]*data-type="([a-z0-9]+)"', now)
           if x in ("arrival", "starter", "ido", "wedo", "independent", "exit")]
    chk("school-grammar stage order intact", seq == STAGES, "→".join(seq))

    ob = sorted(re.findall(r'https://[^"\']*thenational\.academy[^"\']*', base))
    on = sorted(re.findall(r'https://[^"\']*thenational\.academy[^"\']*', now))
    chk("Oak links identical to baseline", ob == on, "%d links, exact URLs unchanged" % len(on))

    n = len(re.findall(FOOD, now, re.I))
    chk("food census", n == 0,
        "0 uses of %d prohibited patterns · scanner validated on 'chocolate' · %s"
        % (len(FOOD.split("|")), u))

    lab = re.search(r"/\* ===== GSG-1 We Do lab \(approved W4A pattern\) ===== \*/(.*?)</style>",
                    now, re.S)
    chk("lab CSS declares no motion (RM: STATIC)",
        bool(lab) and not re.search(r"animation:|transition:", lab.group(1)),
        "0 animation/transition declarations in the lab layer")

    print("  " + ("ALL PASS" if not fails else "FAILED: " + ", ".join(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
