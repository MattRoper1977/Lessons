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


def substitute(path, rules, encoding="utf-8"):
    """rules: list of (old, new, expected_count). Raises on any mismatch."""
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
    return sum(n for _, _, n in applied)
