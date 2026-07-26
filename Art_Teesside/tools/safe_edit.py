"""
Substitution harness. Rule: A SUBSTITUTION MATCHING ZERO OCCURRENCES IS AN ERROR,
NOT A NO-OP.

75612fd was a "fix" that targeted a string not present in the file, changed
nothing, reported nothing, and was pushed on top of a still-broken guard. Same
family as the nbsp near-miss, where a dry run said 4 of 4 and the apply said 21 of
28: an edit that silently matches less than it claims.

Every substitution declares its expected count and is verified after writing.
"""
import re


TEXT_RUN = re.compile(r">([^<>]*)<")


def substitute(path, rules, encoding="utf-8", forbid=None):
    """rules: list of (old, new, expected_count). Raises on any mismatch.

    forbid: optional regex. After writing, every markup text run containing a
    replacement is checked against it. This is the HALF-MATCH guard -- see the
    handover. A substitution can match the right number of times and still be
    semantically incomplete, leaving an orphaned fragment of the surrounding
    unit. Zero-match raises; count-match does not; only the neighbourhood does.
    """
    s = open(path, encoding=encoding).read()
    applied = []
    for old, new, expected in rules:
        n = s.count(old)
        if n == 0:
            raise ValueError(f"{path}: substitution matched ZERO occurrences: {old!r}")
        if n != expected:
            raise ValueError(f"{path}: {old!r} matched {n}, expected {expected}")
        s = s.replace(old, new)
        applied.append((old, new, n))
    open(path, "w", encoding=encoding).write(s)

    # read back from disk, per standing rule 6 -- counts are not verification
    back = open(path, encoding=encoding).read()
    for old, new, n in applied:
        if back.count(new) < n:
            raise ValueError(f"{path}: read-back found {back.count(new)} of {n} for {new!r}")
        if old in back and old not in new:
            raise ValueError(f"{path}: read-back still finds the old string {old!r}")

    if forbid is not None:
        pat = re.compile(forbid, re.I)
        for _, new, _ in applied:
            for run in TEXT_RUN.findall(back):
                if new in run:
                    m = pat.search(run)
                    if m:
                        raise ValueError(
                            f"{path}: HALF-MATCH -- replacement {new!r} left {m.group(0)!r} "
                            f"orphaned in its own text run: {run.strip()!r}")
    return sum(n for _, _, n in applied)
