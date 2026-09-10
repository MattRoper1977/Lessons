## D33 — a text-mode read is not a byte measurement

Byte equality is asserted from **binary reads or `os.path.getsize` plus a content
hash**, never from a text-mode read, which normalises line endings and produces a
plausible near-miss.

Re-asserted for W03–W06, zip against loose, md5 on binary reads: **`6973fbee1ffc`,
`ba23e3f395f6`, `c27cadaccf0a`, `14c1411c2a29` — equal, all four.** The earlier
"byte-identical" was right by luck, not by instrument: the text-mode read showed
26,427 against a real 26,429, and a two-byte gap is exactly the size of a mistake
that looks like rounding.
