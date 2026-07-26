#!/usr/bin/env python3
"""
AT-INST-01 - Art Teesside estate assertions.

Runs the house assertion set across every tracked HTML file under Art_Teesside/
and reports counts. Read Art_Teesside/tools/INSTRUMENTS_ART.md before quoting a
number from this.

WHAT THIS STRUCTURALLY CANNOT DETECT
  * Paraphrase. Every assertion is literal string matching. A lesson that teaches
    a press without writing "press" is invisible. Counts are floors, not totals.
  * Intent. A banned string inside a sentence refusing it looks identical to one
    asserting it. That is why every surviving instance is declared below by exact
    string and reason, rather than inferred, and why anything not matching a
    declared residual is reported for a human to read.
  * Itself. EXPECTED encodes what the estate should look like. A pass that
    changes the estate and edits EXPECTED in the same commit makes this file
    agree with itself and prove nothing. The commit message must say what moved.

CALIBRATION - four false-positive families were found and removed before this
instrument was trusted. Recorded so they are not reintroduced:
  * "Distinction" matched "the method-vs-biography distinction". A grade word
    that is also an ordinary noun. Removed.
  * "Greater depth" matched "4. Greater depth (Think)", a question-difficulty
    label in every arrival grid. Not a grade band. Removed.
  * "pupil name" matched 73 times, every one inside a sentence forbidding pupil
    names ("carries no pupil names - codes only") or the verb ("Every pupil
    names their own PROTECT"). Replaced with a search for actual name-collection
    FIELDS, of which the estate has none.
  * "working at" matched ordinary prose. Removed.
Scope note: this globs *.html only. The staff-side .md files in Art_Teesside/
quote banned strings when describing them and must never be swept.
"""
import re, sys, glob, os, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERBOSE = "--verbose" in sys.argv

# (assertion, exact string, why it survives) - the declared residuals register.
RESIDUALS = [
    ("A2_no_aos", "Never map a sheet to AO1&ndash;AO4 and never use GCSE grade bands", "refusal, 3 SoWs"),
    ("A2_no_aos", "Never map an art sheet to AO1&ndash;AO4, and never label a tier", "refusal, House Standard"),
    ("A2_no_aos", "No GCSE assessment objectives, and no GCSE grade bands", "refusal, House Standard"),
    ("A2_no_aos", "No GCSE assessment objectives anywhere.", "refusal, 3 SoWs"),
    ("A3_no_grade_bands", "Never map a sheet to AO1&ndash;AO4 and never use GCSE grade bands", "refusal, 3 SoWs"),
    ("A3_no_grade_bands", "never label a tier &ldquo;Grades 4&ndash;5&rdquo;", "refusal, House Standard"),
    ("A3_no_grade_bands", "No GCSE assessment objectives, and no GCSE grade bands", "refusal, House Standard"),
    ("A3_no_grade_bands", "No GCSE assessment objectives anywhere.", "refusal, 3 SoWs"),
    ("A4_no_hours_gate", "No hours threshold, ever.", "refusal"),
    ("A4_no_hours_gate", "There is no minimum-hours gate", "refusal"),
    ("A4_no_hours_gate", "there is no minimum-hours gate", "refusal, lowercase variant"),
    ("A4_no_hours_gate", "And never add an hours threshold.", "refusal"),
    ("A4_no_hours_gate", "There is no hours threshold to clear", "refusal"),
    ("A4_no_hours_gate", "guided-learning figures are guidance only", "refusal, continuation clause"),
    ("A4_no_hours_gate", "Guided-learning figures are guidance only", "refusal, sentence-initial variant"),
    ("A4_no_hours_gate", "Bronze guidance is 40 GLH + 20 ILH", "staff-side SoW planning note, immediately "
                                                              "followed by its own refusal to gate on it; "
                                                              "never pupil-facing"),
    ("A8_closed_kit", "there is no press, no rollers and no printing inks in the room", "refusal, Autumn2 SoW"),
    ("A8_closed_kit", "No press, no rollers, no inks", "refusal, START_HERE"),
]

ASSERTIONS = {
    "A2_no_aos":         r"AO[1-4]\b|Assessment Objective",
    "A3_no_grade_bands": r"grade band|\bGCSE\b|Grades \d",
    "A4_no_hours_gate":  r"minimum[- ]hours|hours (?:gate|threshold)|at least \d+ hours|\bGLH\b|\bILH\b|guided[- ]learning",
    "A5_tier_vocab":     r"\b(?:foundation|middle|higher)[- ]tier\b|tier\s*[1-3]\b",
    "A6_no_pupil_names": r"Full name|First name|Surname|Name of (?:pupil|student)|Name:\s*_"
                         r"|Pupil name:|Student name:|Pupil name<|Name of learner",
    "A8_closed_kit":     r"press corner|inking bench|inking queue|inking slab|printing ink|ink load|relief print"
                         r"|\brollers?\b|\bbrayer\b|\blino\b|pre-cut plate|plate wear|re-inked|pull an edition",
}

# Non-residual hits expected. Anything but zero is an OPEN FINDING, named here.
EXPECTED = {
    "A2_no_aos": 0, "A3_no_grade_bands": 0, "A4_no_hours_gate": 0,
    "A5_tier_vocab": 0,
    # D-NAMES-01, open. 24 feedback sheets print "Pupil name:" as a field while
    # the estate states in four other files that no pupil names are stored and
    # codes work everywhere. Awaiting a ruling; not silently fixed.
    "A6_no_pupil_names": 24,
    # D-PRESS-01 (31, in GROW W2/W3/W6 + LAUNCH W6) and D-PRESS-02 (9, in BUILD
    # A2_W6 + Autumn2 SoW + Autumn2 pack). Open until A2a. A floor, not a total.
    # A few Autumn2 SoW hits name the press in order to refuse it and could be
    # declared residuals; they are deliberately counted live instead, because
    # under-counting a banned string is the failure that matters here.
    "A8_closed_kit": 40,
}
COUNTED = {"tier_supported": r"\bSupported\b", "tier_standard": r"\bStandard\b", "tier_stretch": r"\bStretch\b",
           "attrib_made_by_matt": r"Made by Matt", "attrib_progress_schools": r"Progress Schools"}


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True))
    print(f"Art Teesside estate assertions - {len(files)} HTML files\n")
    totals, res_totals, detail = collections.Counter(), collections.Counter(), collections.defaultdict(list)

    for path in files:
        raw = open(path, encoding="utf-8", errors="replace").read()
        rel = os.path.relpath(path, ROOT)
        for key, pat in ASSERTIONS.items():
            s = raw
            for k, string, _ in RESIDUALS:
                if k == key:
                    res_totals[key] += s.count(string)
                    s = s.replace(string, " ")
            hits = re.findall(pat, s, re.I)
            if hits:
                totals[key] += len(hits)
                detail[key].append((rel, len(hits), dict(collections.Counter(h.lower() for h in hits))))

    print(f"{'assertion':<20}{'live':>6}{'exp':>6}{'residual':>10}   verdict")
    print("-" * 56)
    ok = True
    for key in ASSERTIONS:
        good = totals[key] == EXPECTED[key]
        ok &= good
        print(f"{key:<20}{totals[key]:>6}{EXPECTED[key]:>6}{res_totals[key]:>10}   {'PASS' if good else 'MOVED'}")

    print("\ncounted (not asserted):")
    for key, pat in COUNTED.items():
        n = sum(len(re.findall(pat, open(p, encoding='utf-8', errors='replace').read())) for p in files)
        print(f"  {key:<26}{n:>6}")
    print(f"\ndeclared residuals: {len(RESIDUALS)} strings, {sum(res_totals.values())} instances")

    if VERBOSE or not ok:
        for key, rows in detail.items():
            if not rows:
                continue
            print(f"\n[{key}] live hits by file:")
            for rel, n, c in sorted(rows, key=lambda r: -r[1]):
                print(f"  {n:>3}  {rel}  {c}")

    print("\n" + ("ALL ASSERTIONS AT EXPECTED COUNTS" if ok else "AT LEAST ONE ASSERTION MOVED - read above"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
