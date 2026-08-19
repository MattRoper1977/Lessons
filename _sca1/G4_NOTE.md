# G4 instrument — how "PROTECTED, never edited" is actually tested

These lesson files are single enormous lines. Three instrument designs were tried; the
first two were rejected because they cannot distinguish a protected-string edit from an
unrelated prose edit somewhere else on the same line.

1. **Whole-line hash** — REJECTED. Every protected string on a file shares one line hash, so
   any edit anywhere in the file fails G4. Produced 5 false positives on the first BUILD
   commit (W7A's arrival edit "changed" the witness statement and three answer keys).
2. **Context hash, +/-140 chars** — REJECTED. Narrower, but still fires on adjacent prose.
   Produced 1 false positive: the BUILD W4B Oak URL, because the elastic->string safety fix
   lands 100-odd characters after the URL. The URL itself was verified byte-identical.
3. **Exact protected-string multiset + tight +/-25 context** — ADOPTED. Per file, per family,
   the sorted list of matched protected strings must be byte-identical to BASE_SHA, and each
   string's immediate delimiters unchanged. This is what §5 actually protects: the string is
   not edited, not deleted, not duplicated. Unrelated prose 100 chars away is not a violation.

Verified independently for the one case that motivated the change:
`git show BASE:...SCI_B_W4B... | grep -o 'https://www.thenational.academy[^"<> ]*'`
is byte-identical to the same grep on the working tree.
