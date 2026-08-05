#!/usr/bin/env python3
"""Validator for the estate-review execution run (2026-08-05).

Two design rules, both written against defects found in the review this run
was asked to act on:

1.  Every count is proved by ENUMERATION, and markup patterns are counted only
    after <script>/<style>/<!-- --> bodies are blanked.  A census that did not
    do this returned 379 files / 6,438 hits for raw '<' -- all of it correct
    `i<n` loop code -- and invented an estate-wide crisis.

2.  Every check must be able to FAIL.  `--self-test` mutates a scratch copy of
    the estate to break each check in turn and asserts the check goes red.  A
    harness that cannot fail proves nothing.  (The fix pack's own
    validate_applied.py asserted both `'id="title"' not in grid` AND
    `count('class="panel-title"') == 3` -- mutually unsatisfiable while its own
    patch left a fourth id="title" in place.)

Usage:
    validate_estate_exec.py --repo /path/to/lessons
    validate_estate_exec.py --repo /path/to/lessons --self-test
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASE = "4aced082cc8f51868a99a8c6ab9d8147e380f6ec"

SCRIPT_RE = re.compile(r"<script\b[^>]*>.*?</script\s*>", re.S | re.I)
STYLE_RE = re.compile(r"<style\b[^>]*>.*?</style\s*>", re.S | re.I)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
ID_RE = re.compile(r"""\bid\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.I)
TAGSTART = re.compile(r"<[/!?a-zA-Z]")

WAVE = "2 Physics 10/Waves/L4a_Wave_Anatomy.html"
GRID = "Games/Grid_Chase.html"
DIGEST = "biology/Digestion_and_Absorption (1).html"
SURREAL = "6 Art/Surrealism_Eye_Study_v5.html"
HUMW2 = "Build/Slideshows/BUILD_HUM_W2_History_Detectives.html"
J2_CATALOGUED = [
    "2 Physics 10/L1_Circuits_Symbols_Series_Parallel-1.html",
    "2 Physics 10/L4_Wave_Properties_Definitions-1.html",
    "2 Physics 10/L5_Wave_Speed_Equation-1.html",
    "2 Physics 10/L6_Waves_Context_Reflection_Refraction-1.html",
]
J2_UNCATALOGUED = "2 Physics 10/L2_Voltage_Current_Resistance-1.html"
J5_FILES = [
    "Assembly/Behaviour Focus/resilience_poster.html",
    "Assembly/British Value/rule_of_law_poster.html",
    "Assembly/KCSIE/emergency_kcsie_poster (1).html",
    "Build/Resources/BUILD_Print_Kit.html",
    "Tutor_Time/Evidence_Tracker_Paper.html",
    "Tutor_Time/Lesson_Plans.html",
]
ASSESSED_PAIR = {
    "Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html": "a5545585ca28bbba01b55476abb73a9b0819bcc7",
    "Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html": "eb14d6104b94503d0e7ec0a99565ef116a333a57",
}
LOOP_MARK = b"ll-g:loop-mark v1"
WRITTEN_LINE = b"What I said, and what it changed"


def blank(m):
    return re.sub(r"[^\n]", " ", m.group(0))


def read(repo, rel):
    with open(os.path.join(repo, rel), encoding="utf-8", errors="surrogateescape") as fh:
        return fh.read()


def markup_only(text):
    return COMMENT_RE.sub(blank, STYLE_RE.sub(blank, SCRIPT_RE.sub(blank, text)))


def tracked_html(repo):
    out = subprocess.run(["git", "ls-files", "-z", "*.html"], capture_output=True, cwd=repo)
    return [f for f in out.stdout.decode("utf-8", "surrogateescape").split("\0") if f]


def div_delta(text):
    mk = markup_only(text)
    return len(re.findall(r"<div\b", mk)) - len(re.findall(r"</div\s*>", mk))


def after_html(text):
    i = text.lower().rfind("</html>")
    return "" if i == -1 else text[i + len("</html>"):].strip()


# ---------------------------------------------------------------- checks
# Each check returns (ok: bool, detail: str).  Named so a failure reads plainly.

def c_wave_balanced(repo):
    d = div_delta(read(repo, WAVE))
    return d == 0, f"L4a_Wave_Anatomy <div> delta={d} (want 0)"


def c_surreal_balanced(repo):
    d = div_delta(read(repo, SURREAL))
    return d == 0, f"Surrealism_Eye_Study_v5 <div> delta={d} (want 0)"


def c_surreal_modals_free(repo):
    """The modals must NOT be inside #print-area (which is display:none)."""
    mk = markup_only(read(repo, SURREAL))
    i = mk.find('<div id="print-area">')
    j = mk.find('<canvas id="confetti-canvas">')
    if i == -1 or j == -1:
        return False, "print-area or confetti-canvas not found"
    depth = div_delta(mk[i:j])
    return depth == 0, f"open <div> depth between #print-area and confetti canvas={depth} (want 0)"


def c_grid_ids(repo):
    t = read(repo, GRID)
    ids = t.count('id="title"')
    cls = t.count('class="panel-title"')
    css = ".panel-title{font-size:32px" in t
    ok = ids == 0 and cls == 4 and css
    return ok, f'id="title"={ids} (want 0), class="panel-title"={cls} (want 4), CSS rule={css}'


def c_grid_standards(repo):
    t = read(repo, GRID)
    amp = "900&display" in t
    aria = t.count("aria-label=")
    ok = (not amp) and aria == 3
    return ok, f"bare & in fonts href={amp} (want False), aria-label count={aria} (want 3)"


def c_digest_timer(repo):
    t = read(repo, DIGEST)
    dup = t.count('id="indep-timer-display"')
    shared = t.count('class="timer-display indep-timer-display"')
    gebi = t.count("getElementById('indep-timer-display')")
    helper = "function indepDisplays()" in t
    ok = dup == 0 and shared == 2 and gebi == 0 and helper
    return ok, f"dup id={dup} (want 0), shared class={shared} (want 2), getElementById={gebi} (want 0), helper={helper}"


def c_no_orphan_tail(repo):
    """Catalogued files carry nothing after </html>."""
    bad = [f for f in J2_CATALOGUED + [DIGEST] if after_html(read(repo, f))]
    return not bad, f"catalogued files with content after </html>={len(bad)} (want 0) {bad}"


def c_uncatalogued_untouched(repo):
    """L2_Voltage is NOT catalogued -- it is deliberately left alone."""
    keep = bool(after_html(read(repo, J2_UNCATALOGUED)))
    return keep, f"uncatalogued L2_Voltage still carries its tail={keep} (want True)"


def c_raw_lt(repo):
    hits = []
    for f in tracked_html(repo):
        mk = markup_only(read(repo, f))
        for m in re.finditer(r"<", mk):
            if not TAGSTART.match(mk, m.start()):
                hits.append(f)
                break
    return not hits, f"files with raw '<' in markup text={len(hits)} (want 0) {hits[:4]}"


def c_viewport(repo):
    miss = [f for f in J5_FILES
            if not re.search(r"<meta[^>]+name\s*=\s*['\"]viewport['\"]", markup_only(read(repo, f)), re.I)]
    return not miss, f"print/poster files missing viewport={len(miss)} (want 0) {miss}"


def c_no_js_read_dupes(repo):
    """No file may carry a duplicate id in real markup that JS reads by id."""
    bad = {}
    for f in tracked_html(repo):
        raw = read(repo, f)
        mk = markup_only(raw)
        ids = [(a or b) for a, b in ID_RE.findall(mk)]
        ids = [i for i in ids if i and "+" not in i and "${" not in i]
        dups = {i for i in set(ids) if ids.count(i) > 1}
        if not dups:
            continue
        js = "\n".join(m.group(0) for m in SCRIPT_RE.finditer(raw))
        for d in dups:
            if re.search(r"getElementById\s*\(\s*['\"]" + re.escape(d) + r"['\"]", js):
                bad.setdefault(f, []).append(d)
    return not bad, f"files with a JS-read duplicate id={len(bad)} (want 0) {bad}"


# ------- red lines (these must hold, and must be able to fail) -------

def c_poster_untouched(repo):
    jpg = os.path.exists(os.path.join(repo, "assets/video/poster-art.jpg"))
    svg = os.path.exists(os.path.join(repo, "assets/video/poster-art.svg"))
    ref = '/assets/video/poster-art.jpg' in read(repo, "index.html")
    ok = (not jpg) and (not svg) and ref
    return ok, f"R2: poster jpg present={jpg} (want False), placeholder svg={svg} (want False), index.html ref intact={ref} (want True)"


def c_gmblur_intact(repo):
    files = [f for f in tracked_html(repo) if b"g-mblur" in open(os.path.join(repo, f), "rb").read()]
    defs = [f for f in files if "ensureBlurFilter" in read(repo, f)]
    ok = len(files) == 10 and len(defs) == 10
    return ok, f"R3: g-mblur files={len(files)} (want 10), of which define ensureBlurFilter={len(defs)} (want 10)"


def c_assessed_pair(repo):
    bad = []
    for rel, want in ASSESSED_PAIR.items():
        got = subprocess.run(["git", "hash-object", rel], capture_output=True, cwd=repo).stdout.decode().strip()
        if got != want:
            bad.append(f"{rel}: {got} != {want}")
    return not bad, f"R6: assessed pair byte-locked, mismatches={len(bad)} {bad}"


def c_sentinels(repo):
    files = tracked_html(repo)
    loop = writ = 0
    for f in files:
        b = open(os.path.join(repo, f), "rb").read()
        loop += LOOP_MARK in b
        writ += WRITTEN_LINE in b
    ok = (loop, writ, len(files)) == (50, 98, 548)
    return ok, f"sentinels loop/written/universe = {loop}/{writ}/{len(files)} (want 50/98/548)"


CHECKS = [
    ("wave_div_balanced", c_wave_balanced),
    ("surreal_div_balanced", c_surreal_balanced),
    ("surreal_modals_outside_print_area", c_surreal_modals_free),
    ("grid_chase_ids", c_grid_ids),
    ("grid_chase_standards", c_grid_standards),
    ("digestion_timer_shared", c_digest_timer),
    ("no_orphan_tail_in_catalogued", c_no_orphan_tail),
    ("uncatalogued_left_alone", c_uncatalogued_untouched),
    ("no_raw_lt_in_markup", c_raw_lt),
    ("viewport_on_print_pages", c_viewport),
    ("no_js_read_duplicate_ids", c_no_js_read_dupes),
    ("R2_poster_untouched", c_poster_untouched),
    ("R3_gmblur_intact", c_gmblur_intact),
    ("R6_assessed_pair_bytelocked", c_assessed_pair),
    ("sentinels_unmoved", c_sentinels),
]


def run(repo, quiet=False):
    failed = []
    for name, fn in CHECKS:
        try:
            ok, detail = fn(repo)
        except Exception as exc:  # a check that explodes is a check that failed
            ok, detail = False, f"raised {type(exc).__name__}: {exc}"
        if not quiet:
            print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
        if not ok:
            failed.append(name)
    return failed


# ---------------------------------------------------------------- self-test
# Each entry breaks exactly one check.  If the mutation does not turn that
# check red, the check is vacuous and the self-test fails.

def _sub(path, old, new):
    def go(repo):
        p = os.path.join(repo, path)
        t = open(p, encoding="utf-8", errors="surrogateescape").read()
        assert old in t, f"tamper anchor missing in {path}"
        open(p, "w", encoding="utf-8", errors="surrogateescape").write(t.replace(old, new, 1))
    return go


def _sub_all(path, old, new):
    """Replace EVERY occurrence.  Replacing only the first left the file still
    matching the pattern under test, which read as a vacuous check when in fact
    the tamper was too weak."""
    def go(repo):
        p = os.path.join(repo, path)
        t = open(p, encoding="utf-8", errors="surrogateescape").read()
        assert old in t, f"tamper anchor missing in {path}"
        open(p, "w", encoding="utf-8", errors="surrogateescape").write(t.replace(old, new))
    return go


def _seq(*fns):
    def go(repo):
        for f in fns:
            f(repo)
    return go


def _append(path, text):
    def go(repo):
        with open(os.path.join(repo, path), "a", encoding="utf-8") as fh:
            fh.write(text)
    return go


def _touch(path, text=""):
    def go(repo):
        p = os.path.join(repo, path)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write(text)
    return go


TAMPERS = [
    ("wave_div_balanced", _append(WAVE, "\n<div>\n")),
    ("surreal_div_balanced", _sub(SURREAL, '<div id="print-evidence" class="print-section"></div>\n</div>',
                                  '<div id="print-evidence" class="print-section"></div>')),
    ("surreal_modals_outside_print_area", _sub(SURREAL, '<div id="print-evidence" class="print-section"></div>\n</div>',
                                               '<div id="print-evidence" class="print-section"></div>')),
    ("grid_chase_ids", _sub(GRID, '<div class="panel-title" style="font-size:22px">TOP RUNS</div>',
                            '<div id="title" style="font-size:22px">TOP RUNS</div>')),
    ("grid_chase_standards", _sub(GRID, "900&amp;display=swap", "900&display=swap")),
    ("digestion_timer_shared", _sub(DIGEST, '<div class="timer-display indep-timer-display">08:00</div>',
                                    '<div class="timer-display" id="indep-timer-display">08:00</div>')),
    ("no_orphan_tail_in_catalogued", _append(J2_CATALOGUED[0], "\n<div>stray</div>\n")),
    ("uncatalogued_left_alone", _sub(J2_UNCATALOGUED, "</html>", "</htmlX>")),
    ("no_raw_lt_in_markup", _sub(HUMW2, "Shows &lt; suggests", "Shows < suggests")),
    ("viewport_on_print_pages", _sub(J5_FILES[0], '<meta name="viewport" content="width=device-width, initial-scale=1.0">', "")),
    # must restore BOTH the duplicated id AND a by-id read: reverting the markup
    # alone leaves nothing reading it by id, so the check rightly stays green.
    ("no_js_read_duplicate_ids", _seq(
        _sub_all(DIGEST, '<div class="timer-display indep-timer-display">08:00</div>',
                 '<div class="timer-display" id="indep-timer-display">08:00</div>'),
        _sub(DIGEST, "function indepDisplays(){",
             "function indepDisplaysLegacy(){document.getElementById('indep-timer-display');}\n  function indepDisplays(){"))),
    ("R2_poster_untouched", _touch("assets/video/poster-art.svg", "<svg/>")),
    # every occurrence, and the replacement must NOT contain the needle:
    # "g-mblurX" still contains "g-mblur", so that tamper defeated itself.
    ("R3_gmblur_intact", _sub_all("Science_Teesside/Grow/SCI_G_W7_The_Moon.html", "g-mblur", "g-QQblur")),
    ("R6_assessed_pair_bytelocked", _append("Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html", "\n<!-- x -->\n")),
    # the sentinel universe is the tracked *.html count -- so add a tracked file.
    ("sentinels_unmoved", _touch("review/estate-exec/_tamper_probe.html", "<html><body>x</body></html>\n")),
]


def self_test(repo):
    print("\n--- SELF-TEST: prove every check can FAIL ---")
    print("    (each row tampers a scratch copy to break exactly one check)\n")
    results = []
    for target, tamper in TAMPERS:
        with tempfile.TemporaryDirectory() as td:
            work = os.path.join(td, "repo")
            shutil.copytree(repo, work, symlinks=True,
                            ignore=shutil.ignore_patterns(".git"))
            # a git dir is needed for ls-files/hash-object; make a throwaway one
            subprocess.run(["git", "init", "-q"], cwd=work, check=True)
            subprocess.run(["git", "add", "-A"], cwd=work, check=True,
                           capture_output=True)
            try:
                tamper(work)
            except AssertionError as exc:
                results.append((target, "ANCHOR-MISSING", str(exc)))
                continue
            subprocess.run(["git", "add", "-A"], cwd=work, capture_output=True)
            failed = run(work, quiet=True)
            caught = target in failed
            results.append((target, "CAUGHT" if caught else "VACUOUS", ",".join(failed) or "none"))

    width = max(len(r[0]) for r in results)
    vacuous = 0
    for name, verdict, detail in results:
        mark = "ok  " if verdict == "CAUGHT" else "BAD "
        if verdict != "CAUGHT":
            vacuous += 1
        print(f"  {mark}{name:<{width}}  tampered -> {verdict}")
    print(f"\n  checks proved able to fail: {len(results) - vacuous}/{len(results)}")
    return vacuous


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    print(f"=== estate-exec validation against {a.repo} ===\n")
    print("--- LIVE: the estate as it stands ---")
    failed = run(a.repo)
    print(f"\n  {len(CHECKS) - len(failed)}/{len(CHECKS)} checks pass")

    vacuous = 0
    if a.self_test:
        vacuous = self_test(a.repo)

    if failed:
        print(f"\nRED: {len(failed)} check(s) failed: {failed}")
    if vacuous:
        print(f"\nRED: {vacuous} check(s) could not be made to fail -- vacuous.")
    if failed or vacuous:
        return 1
    print("\nGREEN: every check passes, and every check was proved able to fail.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
