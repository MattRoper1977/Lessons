/* ==========================================================================
   ASDAN TEACH — shared interaction layer for the BUILD_ASDAN suite
   --------------------------------------------------------------------------
   Source of truth. Injected into every lesson deck by _framework/apply_framework.py
   between the ASDAN-TEACH:JS markers. Edit here, never in a lesson file.

   RULES OBSERVED BY THIS LAYER
   - Progressive enhancement only. Every lesson must still teach correctly with
     this file removed; nothing here is load-bearing for content or navigation.
   - It wraps existing lesson functions rather than replacing them, so timers,
     print packs, cold call, the match game and the slide deck keep working.
   - No text is written into the page that carries teaching meaning. Labels
     added here are navigational chrome only ("Replay", "Step 2 of 3").
   - Everything is namespaced under window.ASDANTeach.
   ========================================================================== */
(function () {
  'use strict';

  var AT = (window.ASDANTeach = window.ASDANTeach || {});
  var reduceMotion = window.matchMedia
    ? window.matchMedia('(prefers-reduced-motion: reduce)')
    : { matches: false };

  /* ------------------------------------------------------------------
     Slide-change hook
     The decks call showSlide() from next/prev/keyboard. We wrap it once and
     fan out to registered listeners, so later features never have to wrap it
     again and we never double-fire.
     ------------------------------------------------------------------ */
  var slideListeners = [];

  AT.onSlideChange = function (fn) {
    if (typeof fn === 'function') slideListeners.push(fn);
  };

  function fireSlideChange() {
    var slides = document.querySelectorAll('.slide');
    var active = document.querySelector('.slide.active');
    var index = Array.prototype.indexOf.call(slides, active);
    slideListeners.forEach(function (fn) {
      try {
        fn(active, index);
      } catch (e) {
        /* one broken listener must never stop the lesson advancing */
      }
    });
  }

  function installSlideHook() {
    if (typeof window.showSlide !== 'function') return false;
    var original = window.showSlide;
    window.showSlide = function (i) {
      var out = original.apply(this, arguments);
      try {
        fireSlideChange();
      } catch (e) {}
      return out;
    };
    return true;
  }

  /* ------------------------------------------------------------------
     Stagger indexing
     .at-stagger children read their position from --at-i so the CSS can
     space their arrival without a per-item rule.
     ------------------------------------------------------------------ */
  AT.indexStagger = function (root) {
    (root || document).querySelectorAll('.at-stagger').forEach(function (group) {
      Array.prototype.forEach.call(group.children, function (child, i) {
        child.style.setProperty('--at-i', Math.min(i, 12));
      });
    });
  };

  /* ------------------------------------------------------------------
     Zone colour
     Returns the palette token for the slide's teaching zone, so highlights
     always match the subject's approved colours instead of inventing one.
     ------------------------------------------------------------------ */
  AT.zoneVar = function (slide) {
    var type = slide && slide.getAttribute('data-type');
    var title = (slide && slide.getAttribute('data-title')) || '';
    if (type === 'ido' || /I Do/i.test(title)) return '--ido-border';
    if (type === 'wedo' || /We Do/i.test(title)) return '--wedo-border';
    if (type === 'independent' || /Independent/i.test(title)) return '--task-border';
    return '--lo-border';
  };

  AT.reduceMotion = function () {
    return !!reduceMotion.matches;
  };

  /* ------------------------------------------------------------------
     Boot
     ------------------------------------------------------------------ */
  var booted = false;

  function boot() {
    if (booted) return;
    booted = true;
    AT.indexStagger(document);
    installSlideHook();
    (AT._boot || []).forEach(function (fn) {
      try {
        fn();
      } catch (e) {}
    });
    // Announce the slide the deck opened on, so listeners start in sync.
    fireSlideChange();
  }

  /* Features registered before boot run once the DOM and the deck's own
     scripts are in place; anything registered later runs immediately. */
  AT.ready = function (fn) {
    if (booted) {
      try {
        fn();
      } catch (e) {}
      return;
    }
    (AT._boot = AT._boot || []).push(fn);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
