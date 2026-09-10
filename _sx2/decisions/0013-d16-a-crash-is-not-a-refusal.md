## D16 — A crash is not a refusal

A refusal names the problem, leaves the file byte-unchanged, and lets the run
continue. A crash aborts wherever it reached and says nothing about the files
after it. The two must never be reported together, and a crashed run's partial
output is not a measurement.

`tools/relabel_public.py` assumed a manifest was a JSON object. Three Science
`v3_40min` manifests are a top-level array, so `m.get('lessons')` raised
`AttributeError` on the **47 files in those folders — every one of them served**.
It had done so since before #466; #466's 25 self-tests did not cover it, which is
a gap in that PR's testing rather than a regression it introduced.

The consequence is bigger than 47 files. While the tool crashes on a tree, no
census that runs it over that tree can be trusted: the run has an unknown tail.
Any "0 findings" from such a run is a statement about where the crash happened,
not about the estate.

Fixed in #473 by normalising the envelope, not by catching the exception:
`manifest_lessons()` reads the object form, the array form, and returns no
entries for anything else — which makes `lesson_ref` refuse, the same outcome as
no manifest at all. Handled rather than refused for the array because the
evidence said so: its entries carry the same `file`, `week` and `id` fields the
object form does.

**What the crash had been hiding, and what it had not.** The 47 carry **zero**
`data-mbm-cal` attributes and zero `mbm-cal-staff` twins — the relabeller's own
signature on every node it rewrites. It had therefore never written to any of
them: the crash is in `sequence()`, before any rewrite. A rendered census of all
47 as published found **0 placeholders on every route**. The crash prevented
processing; it did not damage what is served.
