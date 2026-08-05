# Lessons estate — proposed fixes for Matt and Claude review

**Base:** `MattRoper1977/Lessons@4aced082cc8f51868a99a8c6ab9d8147e380f6ec`

This directory contains proposed changes only. Nothing here has been applied to
lesson files or merged to `main`.

## Patch order

1. `0001` removes the confirmed extra closing `div` in Wave Anatomy.
2. `0002` replaces Grid Chase’s three duplicate `title` IDs with a class, encodes
   the Google Fonts query ampersand, and explicitly names its three form fields.
3. `0003` gives both independent-work timers a shared class, updates both displays,
   and moves the orphaned memory-trick box back inside the Enzymes & Bile slide.
4. `0004` changes the Lesson Hub to a repository-local poster and adds the proposed
   SVG under `assets/video/`.
5. `0005` removes ten references to an SVG filter ID that is never defined; the
   existing CSS `blur(.8px)` fallback remains active.

`MANUAL_REVIEW.md` lists structural findings where the correct pedagogical
placement cannot be inferred safely.

## Validation

The companion workflow applies all five patches to a disposable worktree created
from the exact base commit, verifies the changed-path allowlist, parses the edited
HTML/CSS/SVG, checks the defect-specific invariants, and opens every affected page
in Chrome in desktop and mobile/touch modes. It uploads a 90-day validation bundle
before enforcing the result.

## Apply in a disposable branch

```bash
git checkout -b review/lessons-estate-fixes 4aced082cc8f51868a99a8c6ab9d8147e380f6ec
for patch in review/estate-fixes/000*.patch; do
  git apply --check "$patch" && git apply "$patch"
done
```

After applying, run the whole-estate audit and visually inspect every changed page.
Keep each numbered patch as a separate commit so Matt or Claude can accept or reject
it independently.
