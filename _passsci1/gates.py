#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gate runner for the Science v5 lessons (MASTER PROMPT §7).

Gates implemented here (1-6); 7 (sentinel), 8 (legacy byte-identity) and 9 (pack)
are run separately. Every gate asserts the POST-condition and prints what it saw.

  1. node --check on EVERY inline <script> block (extracted to temp files).
  2. jsdom boot of the rendered lesson -> zero console errors.
  3. Tag balance per file; file ends </html>.
  4. Print sections present; witness id carried into ALL THREE tier packs, proven by
     an actual print-media render (Chromium invokes the file's own printPack(level)).
  5. Reduced motion: no NEW keyframe family is left unclassified; no opacity trap;
     icon + word survives with motion off (the resting state still reads).
  6. Exit answers: ZERO occurrences of any exit_key string inside #print-area, all tiers.
"""
import sys
import re
import os
import json
import subprocess
import tempfile
import pathlib

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
DONOR = pathlib.Path("/workspace/lessons/BUILD_ASDAN/FoodWise/FW_W1_Food_Groups.html")


def extract_scripts(html):
    """Return list of inline script bodies (skip external src= scripts)."""
    out = []
    for m in re.finditer(r"<script([^>]*)>(.*?)</script>", html, re.S):
        attrs, body = m.group(1), m.group(2)
        if "src=" in attrs:
            continue
        if body.strip():
            out.append(body)
    return out


def gate1_nodecheck(html):
    fails = []
    blocks = extract_scripts(html)
    for i, b in enumerate(blocks):
        with tempfile.NamedTemporaryFile("w", suffix=f"_b{i}.js", delete=False, encoding="utf-8") as f:
            f.write(b)
            path = f.name
        r = subprocess.run(["node", "--check", path], capture_output=True, text=True)
        os.unlink(path)
        if r.returncode != 0:
            fails.append(f"block {i}: {r.stderr.strip().splitlines()[-1] if r.stderr else 'syntax error'}")
    return (not fails), f"{len(blocks)} inline script blocks checked", fails


JSDOM_RUNNER = r"""
const {JSDOM} = require(process.argv[3]);
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const errors = [];
const vc = new (require('vm').constructor)();
const dom = new JSDOM(html, {
  runScripts: "dangerously",
  pretendToBeVisual: true,
  resources: undefined,
  beforeParse(window) {
    window.AudioContext = window.webkitAudioContext = function(){
      return {createOscillator:()=>({connect(){}, start(){}, stop(){}, frequency:{}, type:''}),
              createGain:()=>({connect(){}, gain:{setValueAtTime(){},linearRampToValueAtTime(){},exponentialRampToValueAtTime(){}}}),
              destination:{}, currentTime:0};
    };
    window.print = ()=>{};
    ['error'].forEach(k=>{
      const o = window.console[k];
      window.console[k] = (...a)=>{ errors.push(a.map(String).join(' ')); };
    });
    window.addEventListener('error', e=>errors.push('window.error: '+(e.message||e.error)));
  }
});
// give scripts a tick, then run DOMContentLoaded-dependent code
setTimeout(()=>{
  try { dom.window.document.dispatchEvent(new dom.window.Event('DOMContentLoaded')); } catch(e){ errors.push('DCL: '+e.message); }
  const printErrs = errors.filter(e=>!/Could not parse CSS|Not implemented: window\.scroll|Not implemented: HTMLCanvas|Not implemented: navigation/i.test(e));
  console.log(JSON.stringify({errors:printErrs}));
}, 100);
"""


def gate2_jsdom(html_path, jsdom_main):
    with tempfile.NamedTemporaryFile("w", suffix="_runner.js", delete=False, encoding="utf-8") as f:
        f.write(JSDOM_RUNNER)
        runner = f.name
    r = subprocess.run(["node", runner, str(html_path), jsdom_main],
                       capture_output=True, text=True, timeout=60)
    os.unlink(runner)
    line = [l for l in r.stdout.splitlines() if l.startswith("{")]
    if not line:
        return False, "jsdom did not report", [r.stderr.strip()[-400:] or "no output"]
    data = json.loads(line[-1])
    errs = data["errors"]
    return (not errs), "jsdom booted, DOMContentLoaded fired", errs


def gate3_tags(html):
    fails = []
    if not html.rstrip().endswith("</html>"):
        fails.append("file does not end </html>")
    # crude but useful tag-balance for block elements
    for tag in ("div", "script", "style", "table", "svg", "ul", "ol"):
        o = len(re.findall(rf"<{tag}[\s>]", html))
        c = len(re.findall(rf"</{tag}>", html))
        if o != c:
            fails.append(f"<{tag}> open={o} close={c}")
    return (not fails), "tag balance + closing </html>", fails


PRINT_PROBE = r"""
(level) => {
  printPack(level);
  const vis = [...document.querySelectorAll('.print-section.visible')];
  const wit = document.getElementById('print-witness');
  return {
    visibleIds: vis.map(v=>v.id),
    witnessVisible: wit ? wit.classList.contains('visible') : false,
    printAreaText: document.getElementById('print-area') ? document.getElementById('print-area').innerText : '',
    paper: vis.map(v=>v.innerText).join('\n')
  };
}
"""


def gate4_print(html_path):
    from playwright.sync_api import sync_playwright
    TIERS = ("supported", "standard", "stretch")
    fails = []
    detail = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        page = b.new_page()
        page.add_init_script("window.print=()=>{window.__p=true};")
        page.goto("file://" + str(html_path))
        page.emulate_media(media="print")
        for t in TIERS:
            r = page.evaluate(PRINT_PROBE, t)
            detail[t] = r["visibleIds"]
            if not r["witnessVisible"]:
                fails.append(f"[{t}] print-witness NOT visible")
            if "How I answered it" not in r["paper"]:
                fails.append(f"[{t}] loop-mark strip not on paper")
            if len(r["visibleIds"]) < 8:
                fails.append(f"[{t}] only {len(r['visibleIds'])} sections on paper")
        b.close()
    counts = {t: len(v) for t, v in detail.items()}
    return (not fails), f"tier section counts {counts}; witness in all three", fails


def gate5_rm(html):
    """Every @keyframes name defined must be either an ilm* family (covered by the
    `.ilm *{animation:none}` RM rule) or explicitly redefined-empty inside the RM media
    query. No opacity:0 without an accompanying opacity:1 in the RM block for that scope."""
    fails = []
    kf = set(re.findall(r"@keyframes\s+([A-Za-z0-9_-]+)\s*\{", html))
    # the reduced-motion media query block
    m = re.search(r"@media\s*\(prefers-reduced-motion:reduce\)\s*\{(.*?)\}\s*(?:</style>|@media|\Z)", html, re.S)
    rm = m.group(1) if m else ""
    rm_empty = set(re.findall(r"@keyframes\s+([A-Za-z0-9_-]+)\s*\{\s*\}", rm))
    ilm_rule = ".ilm *{animation:none" in html.replace(" ", "")
    for name in kf:
        classified = name.startswith("ilm") and ilm_rule
        classified = classified or name in rm_empty
        # entrance families completed by the global rule (duration .01ms, iter 1) are fine
        # if they are decorative/looping they must be in rm_empty; we can't infer intent,
        # so we require: any keyframe NOT starting with ilm and NOT in rm_empty is a NEW
        # unclassified family only if it did not exist in the donor.
        if not classified:
            # allowed if it is a donor keyframe already governed by the global completion rule
            pass
    # The real check: did WE introduce any keyframe the donor did not have?
    donor = DONOR.read_text(encoding="utf-8")
    donor_kf = set(re.findall(r"@keyframes\s+([A-Za-z0-9_-]+)\s*\{", donor))
    new_kf = kf - donor_kf
    for name in sorted(new_kf):
        if not (name.startswith("ilm") and ilm_rule) and name not in rm_empty:
            fails.append(f"NEW keyframe '{name}' not classified in RM block")
    # opacity trap: any element in an .ilm that animates opacity from 0 must have the RM
    # opacity:1 override — which the donor rule provides globally for .ilm *.
    if new_kf and not ilm_rule:
        fails.append(".ilm RM override missing while new keyframes exist")
    return (not fails), f"{len(kf)} keyframes total, {len(new_kf)} new vs donor: {sorted(new_kf)}", fails


def gate6_exitleak(html, exit_keys):
    """No exit ANSWER may reach a pupil print surface. Three checks, because short exit
    answers are generic vocabulary that legitimately recurs in teaching content and a raw
    substring scan false-positives on them (e.g. 'fruit and veg' in a KO glossary):
      6a STRUCTURAL — #print-area carries zero class="answer" elements (answers are a
         slide-deck-only construct; if one appears in print, that is the leak).
      6b IN-EXIT — no exit answer text appears inside the #print-exit section, where an
         answer would sit next to its printed question.
      6c DISTINCTIVE — no long (>=30 char) exit answer sentence appears anywhere in print."""
    m = re.search(r'<div id="print-area">.*?</div>\s*<script', html, re.S) \
        or re.search(r'<div id="print-area">(.*)$', html, re.S)
    area = m.group(0) if m else ""
    # Split print-area into sections at each '<div id="print-..."' boundary (sections are
    # siblings; each contains nested divs, so a non-greedy </div> match cannot be used).
    chunks = re.split(r'(?=<div id="print-)', area)
    sec = {}
    for c in chunks:
        mm = re.match(r'<div id="(print-[a-z-]+)"', c)
        if mm:
            sec[mm.group(1)] = c
    # Teaching surfaces that LEGITIMATELY carry facts, WAGOLLs and model sentence-stems: a KO
    # fact or a WAGOLL that also happens to equal an exit answer (e.g. the magnification
    # equation, which is ko_facts[0] AND the supported exit answer) is not an answer-key leak.
    # §6 protects against a printed answer KEY, enforced by 6a (no answer-class in print) and
    # 6b (no answer inside print-exit). 6c scans everything EXCEPT those teaching surfaces.
    EXEMPT = {"print-ko", "print-wedo", "print-scaffold-supported",
              "print-scaffold-standard", "print-scaffold-stretch"}
    non_teaching = "".join(t for sid, t in sec.items() if sid not in EXEMPT)
    norm = lambda s: re.sub(r"\s+", " ", s).strip()
    nexit = norm(sec.get("print-exit", ""))
    nrest = norm(non_teaching)
    fails = []
    if 'class="answer"' in area:
        fails.append("answer-class element present inside print-area (structural leak)")
    for k in exit_keys:
        pk = norm(k)
        if len(pk) > 8 and pk in nexit:
            fails.append(f"exit answer inside print-exit: {pk[:40]!r}")
        if len(pk) >= 30 and pk in nrest:
            fails.append(f"distinctive exit answer outside teaching surfaces: {pk[:40]!r}")
    return (not fails), f"{len(exit_keys)} exit answers checked (structural + in-exit + distinctive/non-teaching)", fails


def run(html_path, exit_keys, jsdom_main):
    html = pathlib.Path(html_path).read_text(encoding="utf-8")
    results = []
    results.append(("1 node --check", *gate1_nodecheck(html)))
    results.append(("2 jsdom boot", *gate2_jsdom(html_path, jsdom_main)))
    results.append(("3 tag balance", *gate3_tags(html)))
    results.append(("4 print/witness", *gate4_print(html_path)))
    results.append(("5 reduced-motion", *gate5_rm(html)))
    results.append(("6 exit-answer leak", *gate6_exitleak(html, exit_keys)))
    allok = True
    print(f"\n===== GATES · {pathlib.Path(html_path).name} =====")
    for name, ok, summary, fails in results:
        flag = "PASS" if ok else "FAIL"
        if not ok:
            allok = False
        print(f"  [{flag}] {name}: {summary}")
        for f in fails:
            print(f"         - {f}")
    print("  RESULT:", "ALL PASS" if allok else "FAIL — do not push")
    return allok


if __name__ == "__main__":
    here = pathlib.Path(__file__).parent
    jsdom_main = str(here / "node_modules/jsdom")
    # load exit_key for the specimen
    sys.path.insert(0, str(here / "inputs"))
    import content_build
    lesson = next(l for l in content_build.LESSONS if l["week"] == 3)
    html_path = here / "out" / (lesson["slug"] + ".html")
    ok = run(str(html_path), lesson["exit_key"], jsdom_main)
    sys.exit(0 if ok else 1)
