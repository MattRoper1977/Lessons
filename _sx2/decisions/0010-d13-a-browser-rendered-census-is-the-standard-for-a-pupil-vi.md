## D13 — A browser-rendered census is the standard for a pupil-visible claim

Two false findings in one day, from opposite directions, both from not rendering:

- **Mine.** `git grep -c` counts matching *lines*, not occurrences, and the search
  set omitted `the next unit` in the Science Build tree. Reported 31 across 19
  files. The real figure was **121 across 22** — and the two worst pages in the
  estate, `SCI_B_W13A` (18) and `SCI_B_W13B` (33), were not in the list at all.
- **Matt's.** A direct fetch of `SCI_B_W13A` appeared to show the placeholder and
  the correct copy in one node. It is the `span.mbm-cal-staff` twin, inline
  `display:none`; a browser renders one copy, but any tag strip that ignores CSS
  concatenates both.

Neither a source grep nor a tag-stripped fetch is a render. `tools/lf1/render_census.cjs`
walks the DOM the browser builds. A source scan is still sound for *enumerating
candidates* — nothing can render that is not in the bytes — but it never
adjudicates what a pupil reads.
