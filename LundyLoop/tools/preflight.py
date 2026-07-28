#!/usr/bin/env python3
"""
preflight.py  —  LundyLoop shared instrument preflight  [LL-INST-11]

WHY THIS EXISTS (Pass X, from Pass U's finding)
  `ko_staleness.py` returned "0 candidates, all clean" on a shallow (`--depth 1`)
  clone: with one commit per file, every KO block and body appear to have last
  moved together, so nothing is a candidate. The same tool on the same tree after
  `git fetch --unshallow` returned 114. It did NOT fail loud — it handed back the
  reassuring number. In this estate a FALSE ZERO from an under-specified check is
  the most expensive defect class: it CLOSES a question that was never examined.

  `sitemap_audit.py` already has the correct shape — when it cannot reach its
  subject it prints "NOT a pass. Nothing below was checked." and exits non-zero.
  This module is that shape, extracted so every instrument can declare the thing
  it depends on and fail loud when it is absent, instead of each tool re-inventing
  the check (or forgetting it).

THE RULE IT ENFORCES
  An instrument depends on things OUTSIDE the file it reads — full git history, a
  reachable host, a corpus of the expected size. When one is absent it must FAIL
  LOUD, never return a plausible number. And every result it prints must carry the
  assumptions it rests on, so "0 candidates" can never again be read without
  "(full clone, N-file corpus, network not required)" beside it.

  These helpers print to STDERR and exit non-zero on failure — a guard's whole job
  is to stop the run, not to be caught and swallowed.

STATUS: current
"""
import subprocess
import sys

# Distinct from sitemap_audit's exit(2): a preflight failure is "the environment is
# not what this instrument requires", not "the subject could not be measured".
PREFLIGHT_EXIT = 3


def _git(repo, *args):
    """Run git in `repo`; return (returncode, stdout.strip()). Never raises."""
    p = subprocess.run(["git", "-C", str(repo), *args],
                       capture_output=True, text=True, errors="replace")
    return p.returncode, p.stdout.strip()


def _fail(msg):
    print(f"FAIL — {msg}", file=sys.stderr)
    print("This is NOT a pass. Nothing below was checked.", file=sys.stderr)
    sys.exit(PREFLIGHT_EXIT)


def require_full_clone(repo):
    """Exit non-zero unless `repo` has full history.

    A shallow clone truncates per-file history to the clone's single commit, which
    silently breaks any tool that compares a file across commits (`git log -- f`,
    `git show <old>:f`, blame, commit dates). `git rev-parse --is-shallow-repository`
    prints 'true'/'false' (git >= 2.15); an unexpected value is treated as unsafe.
    """
    rc, out = _git(repo, "rev-parse", "--is-shallow-repository")
    if rc != 0:
        _fail(f"not a git working tree, or git unavailable, at {repo}. "
              "This instrument needs full git history.")
    if out == "true":
        _fail("shallow clone: per-file history is truncated to one commit, so "
              "cross-commit comparisons are meaningless and a history-based count "
              "would report a false zero. Run `git fetch --unshallow` first.")
    if out != "false":
        _fail(f"could not determine clone depth (rev-parse returned {out!r}); "
              "refusing to run a history-based check on an unverifiable clone.")
    return True


def require_network(host, timeout=10):
    """Exit non-zero unless `host` is reachable over TCP:443.

    Behind the container proxy a blocked host returns a 403 that is the PROXY, not
    the site; a tool that reads that as 'dead' produces a false positive, and one
    that skips it and still prints a total produces a false zero. Fail loud instead.
    """
    import socket
    try:
        socket.create_connection((host, 443), timeout=timeout).close()
    except Exception as e:                                        # noqa: BLE001
        _fail(f"host {host!r} is not reachable ({type(e).__name__}). A network "
              "check cannot pass without its subject.")
    return True


def require_corpus(expected_min, actual, label="corpus"):
    """Exit non-zero if the measured corpus is smaller than expected.

    A scope that is not the one you meant is not evidence of coverage. If a glob or
    directory scope silently returns fewer files than the estate is known to hold,
    a clean result is clean for the wrong reason.
    """
    if actual < expected_min:
        _fail(f"{label} has {actual} items, fewer than the expected minimum "
              f"{expected_min}. The scope is wrong; a result over it is not coverage.")
    return True


def declare_assumptions(items):
    """Print the assumptions a result rests on, so the number is never read alone.

    `items` is a list of short strings, e.g.
        ['full clone', '161-file KO corpus', 'network not required'].
    """
    print("assumptions: " + " · ".join(items))


if __name__ == "__main__":
    # Self-test / demonstration: run against this repo.
    import pathlib
    here = pathlib.Path(__file__).resolve().parents[2]
    require_full_clone(here)
    declare_assumptions(["full clone", "self-test"])
    print("preflight: OK")
