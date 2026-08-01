/* ==========================================================================
   SHARED MEASUREMENT HELPERS — the safe path is the only path.

   INSTRUMENTS.md standing rule 13: an animated property read at the wrong
   moment is not a measurement. Two ways to get it wrong, both seen:

     · reading computed style synchronously after adding a class — the
       animation has not started, so you read the pre-animation value;
     · reading on a hidden slide — Chromium does not start animations inside
       a display:none subtree, so everything looks inert whether gated or not.

   A rule in a document is weaker than a helper that only does the right thing,
   so these exist and instruments use them rather than re-deriving the wait.
   ========================================================================== */
'use strict';

/* Longer than the longest fill-mode animation in the shared language
   (gMorphIn/gMorphOut at .85s). Raise this if a slower one is added. */
const HOLD_MS = 1100;

/* Show slide `i`, then wait past the animations before anything is read. */
async function onSlide(page, i, fn, arg) {
  await page.evaluate(j => window.showSlide && window.showSlide(j), i);
  await page.waitForTimeout(HOLD_MS);
  return fn ? page.evaluate(fn, arg) : undefined;
}

/* Add classes, then wait for the animation to reach its held keyframe.
   Returns computed values AFTER the wait — there is deliberately no variant
   that reads immediately. */
async function afterClasses(page, selector, classes, read) {
  await page.evaluate(({ s, c }) => {
    const el = document.querySelector(s);
    if (el) c.forEach(x => el.classList.add(x));
  }, { s: selector, c: classes });
  await page.waitForTimeout(HOLD_MS);
  return page.evaluate(read, selector);
}

/* The one definition of "a pupil can read this". */
const LEGIBLE_SRC = `(el) => {
  const cs = getComputedStyle(el);
  return cs.display !== 'none' && cs.visibility !== 'hidden' &&
         parseFloat(cs.opacity) > 0.05;
}`;

module.exports = { HOLD_MS, onSlide, afterClasses, LEGIBLE_SRC };
