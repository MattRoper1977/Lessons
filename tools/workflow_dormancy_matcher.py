#!/usr/bin/env python3
"""THE PATH-FILTER DORMANCY MATCHER — report only.

The watch reports that a workflow did not run and then refuses to judge it.
That refusal is honest: without matching each workflow's `paths:` against the
commit's changed files there is no way to separate a workflow that was
CORRECTLY DORMANT from one that SHOULD HAVE RUN AND DID NOT. The second is a
workflow that has silently stopped running, and nothing in the estate can
currently see it. This closes that, and nothing else.

Five verdicts, each with a predicate:

  SHOULD HAVE RUN + did       filters match this diff, and a run exists
  SHOULD HAVE RUN / DID NOT   filters match this diff, and no run exists  <-- THE FINDING
  CORRECTLY DORMANT           a filter excluded it: paths, paths-ignore, or branches
  NOT APPLICABLE              no pull_request trigger at all, provable from `on:`
  UNDETERMINED                workflow_run chains, unknown activity types, malformed YAML

UNDETERMINED is meant to get SMALLER, never to disappear. A matcher that
returns zero UNDETERMINED on a repo containing `workflow_run` chains is
overclaiming, not succeeding.

REPORT ONLY (R0.25). This is not wired into the watch's verdict and writes
nothing to the ledger. The watch's false positive came from a gate that could
go red before it had ever been shown able to go green. So this tool runs its
seven controls on EVERY invocation, prints how many fired in each direction,
and refuses to report at all unless every one of them fires BOTH ways.

  python3 tools/workflow_dormancy_matcher.py --self-test
  python3 tools/workflow_dormancy_matcher.py --workflows DIR --changed FILE \
          --base-ref main [--ran FILE] [--json]
"""
import argparse
import glob
import json
import os
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover - environment dependent
    sys.stderr.write(
        "[INCONCLUSIVE] PyYAML is not installed.\n"
        "A workflow trigger block is YAML, and hand-parsing YAML is exactly how a\n"
        "tool of this kind starts lying confidently. Exiting 2 rather than guessing.\n"
        "  python3 -m pip install pyyaml\n"
    )
    sys.exit(2)

HERE = os.path.dirname(os.path.abspath(__file__))
SOAK_FILE = os.path.join(HERE, "dormancy_matcher_soak.json")
FIXTURE = os.path.join(HERE, "fixtures", "pr124")

PR_EVENTS = ("pull_request", "pull_request_target")
DEFAULT_PR_TYPES = {"opened", "synchronize", "reopened"}

V_RAN = "SHOULD HAVE RUN"
V_DIDNT = "SHOULD HAVE RUN / DID NOT"
V_DORMANT = "CORRECTLY DORMANT"
V_NA = "NOT APPLICABLE"
V_UNDET = "UNDETERMINED"


# ---------------------------------------------------------------- glob semantics

def glob_to_regex(pat):
    """GitHub filter-pattern glob.

    `*` matches any run of characters but does NOT cross `/`.
    `**` does cross `/`.
    Getting this backwards makes every deep file look like a match, which turns
    the whole report into false reds. Control (c) pins the boundary.
    """
    out = ["^"]
    i = 0
    while i < len(pat):
        c = pat[i]
        if c == "*":
            if pat[i + 1:i + 2] == "*":
                out.append(".*")
                i += 2
            else:
                out.append("[^/]*")
                i += 1
        elif c == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(c))
            i += 1
    out.append("$")
    return re.compile("".join(out))


_RX = {}


def _rx(pat):
    if pat not in _RX:
        _RX[pat] = glob_to_regex(pat)
    return _RX[pat]


def included(patterns, path):
    """LAST MATCH WINS. `!` negates.

    Returns True (included), False (excluded by a negation), or None (no
    pattern in the list matched this path at all). The three are distinct and
    collapsing them loses the paths-ignore case.
    """
    verdict = None
    for pat in patterns:
        neg = isinstance(pat, str) and pat.startswith("!")
        body = pat[1:] if neg else pat
        if _rx(str(body)).match(path):
            verdict = not neg
    return verdict


def paths_match(patterns, changed):
    """A `paths:` filter fires when ANY changed file ends up included."""
    return any(included(patterns, f) is True for f in changed)


def paths_ignore_allows(patterns, changed):
    """A `paths-ignore:` filter fires when ANY changed file is NOT ignored."""
    return any(included(patterns, f) is not True for f in changed)


def branch_allows(cfg, ref):
    """Branch filters gate a workflow just as hard as path filters do.

    A workflow whose paths match but whose `branches:` exclude the ref is
    CORRECTLY DORMANT, not a finding. Omitting this is the likeliest way to
    ship a tool that produces false reds. Control (e) pins it.
    """
    if "branches" in cfg and cfg["branches"] is not None:
        return included(cfg["branches"], ref) is True
    if "branches-ignore" in cfg and cfg["branches-ignore"] is not None:
        return included(cfg["branches-ignore"], ref) is not True
    return True


# ---------------------------------------------------------------- the `on:` trap

def trigger_block(doc):
    """YAML 1.1 parses the bare key `on` as the BOOLEAN True.

    `doc.get("on")` therefore returns None for every workflow in this estate,
    which a naive matcher reads as "no paths filter -> matches everything ->
    should have run" and reports as a wall of false reds. Both spellings are
    accepted here. This is not hypothetical; it is what the first draft did.
    """
    if isinstance(doc, dict):
        if True in doc:
            return doc[True]
        return doc.get("on")
    return None


def events(doc):
    on = trigger_block(doc)
    if on is None:
        return {}
    if isinstance(on, str):
        return {on: {}}
    if isinstance(on, list):
        return {e: {} for e in on}
    if isinstance(on, dict):
        return {k: (v if isinstance(v, dict) else {}) for k, v in on.items()}
    return {}


# ---------------------------------------------------------------- classification

def classify(name, doc, changed, base_ref, ran):
    """Return (verdict, predicate). `ran` is a set of workflow filenames that
    actually ran, or None when that evidence was not supplied."""
    if not isinstance(doc, dict) or not doc:
        return (V_UNDET, "workflow YAML did not parse into a mapping")

    ev = events(doc)
    pr = None
    for e in PR_EVENTS:
        if e in ev:
            pr = ev[e]
            break

    if pr is None:
        if "workflow_run" in ev:
            return (V_UNDET,
                    "workflow_run chain — depends on an upstream run; not guessed")
        trig = ", ".join(sorted(str(k) for k in ev)) or "no triggers at all"
        return (V_NA, "no pull_request trigger — %s" % trig)

    types = pr.get("types")
    if types is not None and not (set(types) & DEFAULT_PR_TYPES):
        return (V_UNDET,
                "pull_request types: %s — the PR activity type is not known here" % (types,))

    if not branch_allows(pr, base_ref):
        b = pr.get("branches", pr.get("branches-ignore"))
        return (V_DORMANT, "branches: %s excludes base ref %r" % (b, base_ref))

    has_p = pr.get("paths") is not None
    has_pi = pr.get("paths-ignore") is not None
    if has_p and has_pi:
        return (V_UNDET,
                "paths: and paths-ignore: are mutually exclusive within one event "
                "filter — this workflow is malformed and its behaviour is not derived")

    if has_p:
        if not paths_match(pr["paths"], changed):
            return (V_DORMANT,
                    "paths: (%d entries) matches nothing in this diff" % len(pr["paths"]))
        matched = next(f for f in changed if included(pr["paths"], f) is True)
    elif has_pi:
        if not paths_ignore_allows(pr["paths-ignore"], changed):
            return (V_DORMANT,
                    "paths-ignore: (%d entries) covers every changed file"
                    % len(pr["paths-ignore"]))
        matched = next(f for f in changed if included(pr["paths-ignore"], f) is not True)
    else:
        matched = "(no paths filter — matches everything)"

    if ran is None:
        return (V_UNDET,
                "filters match (%s) but the set of runs was not supplied" % matched)
    if name in ran:
        return (V_RAN, "and did — matched %s" % matched)
    return (V_DIDNT, "filters match (%s) and no run exists" % matched)


def assess(workflows, changed, base_ref, ran):
    rows = []
    for name, doc in workflows:
        verdict, why = classify(name, doc, changed, base_ref, ran)
        rows.append({"workflow": name, "verdict": verdict, "why": why})
    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    return {
        "rows": sorted(rows, key=lambda r: r["workflow"]),
        "counts": counts,
        "findings": [r for r in rows if r["verdict"] == V_DIDNT],
        # An empty workflow set is an absence, not a result (R0.28). Reporting
        # "0 findings" over nothing reads exactly like a clean estate.
        "inconclusive": len(workflows) == 0,
    }


# ---------------------------------------------------------------- the controls

def _wf(text):
    return yaml.safe_load(text)


def run_controls():
    """Seven controls. Every one must fire in BOTH directions, every run."""
    reds = greens = 0
    failures = []

    def check(label, got, want, direction):
        nonlocal reds, greens
        if direction == "red":
            reds += 1
        else:
            greens += 1
        if got != want:
            failures.append("%s [%s]: expected %r, got %r" % (label, direction, want, got))

    def v(name, doc, changed, base, ran):
        return classify(name, doc, changed, base, ran)[0]

    # (a) a workflow whose filter matches a changed file and did not run
    a = _wf("on:\n  pull_request:\n    paths: ['tools/**']\n")
    check("(a) matching filter, no run", v("a.yml", a, ["tools/x.mjs"], "main", set()),
          V_DIDNT, "red")
    check("(a) matching filter, run exists", v("a.yml", a, ["tools/x.mjs"], "main", {"a.yml"}),
          V_RAN, "green")

    # (b) a correctly dormant workflow is green and is NOT a finding
    b = _wf("on:\n  pull_request:\n    paths: ['Games/**']\n")
    check("(b) unrelated diff is dormant", v("b.yml", b, ["tools/x.mjs"], "main", set()),
          V_DORMANT, "green")
    check("(b) same workflow, related diff", v("b.yml", b, ["Games/g.html"], "main", set()),
          V_DIDNT, "red")

    # (c) the `*` vs `**` boundary, proved on a file one directory deeper
    star = _wf("on:\n  pull_request:\n    paths: ['Games/*.html']\n")
    dstar = _wf("on:\n  pull_request:\n    paths: ['Games/**']\n")
    deep = ["Games/sub/deep.html"]
    check("(c) '*' does not cross '/'", v("c.yml", star, deep, "main", set()),
          V_DORMANT, "green")
    check("(c) '**' does cross '/'", v("c.yml", dstar, deep, "main", set()),
          V_DIDNT, "red")

    # (d) negation ordering — last match wins
    late = _wf("on:\n  pull_request:\n    paths: ['Games/**', '!Games/skip.html']\n")
    early = _wf("on:\n  pull_request:\n    paths: ['!Games/skip.html', 'Games/**']\n")
    skip = ["Games/skip.html"]
    check("(d) negation last -> excluded", v("d.yml", late, skip, "main", set()),
          V_DORMANT, "green")
    check("(d) negation first -> re-included", v("d.yml", early, skip, "main", set()),
          V_DIDNT, "red")

    # (e) paths match but the branch filter excludes the ref
    e = _wf("on:\n  pull_request:\n    paths: ['tools/**']\n    branches: ['release/*']\n")
    check("(e) branch filter excludes base", v("e.yml", e, ["tools/x.mjs"], "main", set()),
          V_DORMANT, "green")
    check("(e) same workflow on a permitted base",
          v("e.yml", e, ["tools/x.mjs"], "release/1", set()), V_DIDNT, "red")

    # (f) an empty workflow set is INCONCLUSIVE, never "0 findings"
    check("(f) empty set is inconclusive",
          assess([], ["tools/x.mjs"], "main", set())["inconclusive"], True, "green")
    check("(f) non-empty set is not inconclusive",
          assess([("z.yml", _wf("on:\n  pull_request:\n"))], ["tools/x.mjs"], "main",
                 set())["inconclusive"], False, "red")

    # (g) THE TRUE NEGATIVE: the real workflow set at PR #124's head commit must
    #     reproduce that PR's hand-verified trigger table exactly, with zero
    #     findings — and the same set, with the one run that did happen removed,
    #     must produce exactly one finding naming it.
    if not os.path.isdir(FIXTURE):
        failures.append("(g) fixture missing at %s" % FIXTURE)
        reds += 1
        greens += 1
    else:
        wfs = load_dir(os.path.join(FIXTURE, "workflows"))
        changed = read_lines(os.path.join(FIXTURE, "changed_files.txt"))
        ran = set(read_lines(os.path.join(FIXTURE, "ran.txt")))
        expected = json.load(open(os.path.join(FIXTURE, "expected.json")))
        got = assess(wfs, changed, expected["base_ref"], ran)
        table = {r["workflow"]: r["verdict"] for r in got["rows"]}
        check("(g) #124 table reproduced", table, expected["table"], "green")
        check("(g) #124 findings", len(got["findings"]), 0, "green")
        # both directions: pretend the one workflow that ran did not
        mutated = assess(wfs, changed, expected["base_ref"], set())
        names = sorted(r["workflow"] for r in mutated["findings"])
        check("(g) mutated #124 names the silent workflow", names,
              sorted(expected["ran"]), "red")

    return {"reds": reds, "greens": greens, "failures": failures}


# ---------------------------------------------------------------- io

def read_lines(path):
    with open(path) as fh:
        return [l.strip() for l in fh if l.strip() and not l.startswith("#")]


def load_dir(d):
    out = []
    for p in sorted(glob.glob(os.path.join(d, "*.yml")) + glob.glob(os.path.join(d, "*.yaml"))):
        try:
            doc = yaml.safe_load(open(p))
        except yaml.YAMLError:
            doc = None
        out.append((os.path.basename(p), doc))
    return out


def soak_read():
    try:
        return json.load(open(SOAK_FILE))
    except Exception:
        return {"runs": 0, "declared_soak": 10, "wired": False}


def soak_bump():
    s = soak_read()
    s["runs"] = s.get("runs", 0) + 1
    with open(SOAK_FILE, "w") as fh:
        json.dump(s, fh, indent=2)
        fh.write("\n")
    return s


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workflows", help="directory of workflow YAML, read AT THE COMMIT")
    ap.add_argument("--changed", help="file listing the commit's changed paths, one per line")
    ap.add_argument("--base-ref", default="main", help="the PR's base branch (default: main)")
    ap.add_argument("--ran", help="file listing workflow filenames that actually ran")
    ap.add_argument("--self-test", action="store_true", help="run the controls and stop")
    ap.add_argument("--record-soak", action="store_true", help="increment the soak counter")
    ap.add_argument("--json", action="store_true", help="emit the assessment as JSON")
    args = ap.parse_args()

    controls = run_controls()
    line = ("controls: %d red fired, %d green returned"
            % (controls["reds"], controls["greens"]))

    if controls["failures"]:
        print("[CONTROLS FAILED] " + line)
        for f in controls["failures"]:
            print("   " + f)
        print("A control that fires in only one direction is not a control.")
        print("Refusing to report.")
        return 1

    if args.self_test:
        print("[CONTROLS PASS] " + line)
        print("Seven controls, each fired in both directions.")
        return 0

    if not args.workflows or not args.changed:
        print("[INCONCLUSIVE] --workflows and --changed are both required.")
        print(line)
        return 2

    workflows = load_dir(args.workflows)
    changed = read_lines(args.changed)
    ran = set(read_lines(args.ran)) if args.ran else None

    result = assess(workflows, changed, args.base_ref, ran)

    if result["inconclusive"]:
        print("[INCONCLUSIVE] no workflows found in %s" % args.workflows)
        print("An absence is not a result: reporting 0 findings over 0 workflows")
        print("would read exactly like a clean estate.")
        print(line)
        return 2

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("SCOPE: %d workflow(s) in %s" % (len(workflows), args.workflows))
        print("       %d changed file(s), base ref %r" % (len(changed), args.base_ref))
        if ran is None:
            print("       run evidence NOT supplied — the did/did-not leg is UNDETERMINED")
        print("")
        w = max(len(r["workflow"]) for r in result["rows"])
        for r in result["rows"]:
            print("  %-*s  %-25s  %s" % (w, r["workflow"], r["verdict"], r["why"]))
        print("")
        print("VERDICT COUNTS, each with its predicate:")
        for verdict in (V_RAN, V_DIDNT, V_DORMANT, V_NA, V_UNDET):
            print("  %-25s %d" % (verdict, result["counts"].get(verdict, 0)))
        print("")
        if result["findings"]:
            print("FINDINGS — workflows that should have run and did not:")
            for f in result["findings"]:
                print("  * %s — %s" % (f["workflow"], f["why"]))
        else:
            print("FINDINGS: none. Every workflow that could have run, ran.")

    soak = soak_bump() if args.record_soak else soak_read()
    # Under --json, stdout must be exactly the JSON document and nothing else,
    # or every caller has to strip a trailer before it can parse. The control
    # tally and the soak count are still emitted on EVERY run — on stderr, so a
    # machine reading stdout cannot lose them silently.
    trailer = sys.stderr if args.json else sys.stdout
    print("", file=trailer)
    print(line, file=trailer)
    print("soak: %d recorded run(s); declared soak before any wiring is %d."
          % (soak.get("runs", 0), soak.get("declared_soak", 10)), file=trailer)
    print("REPORT ONLY — not wired into the watch's verdict, writes nothing to the ledger.",
          file=trailer)
    # Report-only: findings do NOT set a non-zero exit. Wiring this into a gate
    # is a later decision and needs its own true-negative there (R0.24).
    return 0


if __name__ == "__main__":
    sys.exit(main())
