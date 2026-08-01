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

  /* ==================================================================
     FEATURE · Illuminator replay and caption timing
     ------------------------------------------------------------------
     The I Do diagram builds itself over a few seconds using per-element
     animation delays written into each lesson's SVG. We read the longest
     of those delays so the caption can wait for the build to finish, and
     we add a Replay control so a teacher can run the build again while
     talking over it.
     ================================================================== */
  function setupIlluminator(block) {
    if (block.dataset.atIlm) return;
    block.dataset.atIlm = '1';

    // Longest delay + its animation duration = when the build settles.
    var latest = 0;
    block.querySelectorAll('svg *').forEach(function (el) {
      var cs = getComputedStyle(el);
      if (cs.animationName === 'none') return;
      var delay = parseFloat(cs.animationDelay) || 0;
      var dur = parseFloat(cs.animationDuration) || 0;
      // Looping animations never "finish" — they must not hold the caption back.
      if (cs.animationIterationCount === 'infinite') dur = 0;
      if (delay + dur > latest) latest = delay + dur;
    });
    block.style.setProperty('--ilm-end', (latest || 2.4).toFixed(2) + 's');

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'ilm-replay';
    btn.innerHTML = '↻ Replay';
    btn.setAttribute('aria-label', 'Play the diagram again');
    btn.addEventListener('click', function () {
      replayIlluminator(block);
    });
    block.appendChild(btn);
  }

  /* Restart every animation inside the block by detaching and reattaching
     the SVG. Re-parenting is the one restart that works no matter which of
     the deck's animation classes an element is using. */
  function replayIlluminator(block) {
    var svg = block.querySelector('svg');
    if (!svg) return;
    var next = svg.nextSibling;
    var parent = svg.parentNode;
    parent.removeChild(svg);
    void parent.offsetWidth; // force reflow so the removal is observed
    parent.insertBefore(svg, next);

    var cap = block.querySelector('.ilm-cap');
    if (cap) {
      cap.style.animation = 'none';
      void cap.offsetWidth;
      cap.style.animation = '';
    }
  }

  AT.replayIlluminator = replayIlluminator;

  /* ==================================================================
     FEATURE · Keyboard and screen-reader access for the card activities
     ------------------------------------------------------------------
     The We Do activities are built from <div onclick>, which no keyboard
     or screen reader can reach. We promote them to real buttons in the
     accessibility tree and add Enter/Space, without touching the markup
     the lessons ship or the handlers they already bind.
     ================================================================== */
  function makeOperable(el, label) {
    if (el.dataset.atKeys) return;
    el.dataset.atKeys = '1';
    if (!el.getAttribute('role')) el.setAttribute('role', 'button');
    if (!el.hasAttribute('tabindex')) el.setAttribute('tabindex', '0');
    if (label && !el.getAttribute('aria-label')) el.setAttribute('aria-label', label);
    el.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter' && e.key !== ' ' && e.key !== 'Spacebar') return;
      e.preventDefault();
      el.click();
    });
  }

  function setupCardKeyboard(root) {
    (root || document).querySelectorAll('.pres-card').forEach(function (el) {
      makeOperable(el);
    });
    (root || document).querySelectorAll('.match-pill, .match-target').forEach(function (el) {
      makeOperable(el);
    });
  }

  /* Feedback lines are updated by script; announce them so a pupil using a
     screen reader hears the same confirmation the room sees. The progress
     label already names the slide, so making it a status region is all that
     is needed to announce that the deck has moved on. */
  function setupLiveRegions() {
    ['pres-msg', 'match-fb', 'pres-num', 'match-score'].forEach(function (id) {
      var el = document.getElementById(id);
      if (el && !el.getAttribute('aria-live')) el.setAttribute('aria-live', 'polite');
    });
    var label = document.getElementById('progressLabel');
    if (label && !label.getAttribute('aria-live')) {
      label.setAttribute('role', 'status');
      label.setAttribute('aria-live', 'polite');
    }
  }

  /* ==================================================================
     FEATURE · Give each differentiated task card its level's colour
     ------------------------------------------------------------------
     Arrival, Independent and Exit each offer the same work at three
     levels, and each level's heading is already coloured by the lesson.
     The cards were identical, so a pupil had to read all three to find
     theirs. We lift the colour the lesson chose off its own heading and
     run it down the card's leading edge — nothing hardcoded, no new
     colour, and the heading still names the level in words and an icon.
     ================================================================== */
  function accentLevelCards(root) {
    (root || document).querySelectorAll('.task-box').forEach(function (box) {
      if (box.classList.contains('at-levelled')) return;
      var heading = box.querySelector('h3[style*="color"]');
      var colour = heading && heading.style.color;
      if (!colour) return;
      box.style.setProperty('--tb-accent', colour);
      box.classList.add('at-levelled');
    });
  }

  /* ==================================================================
     FEATURE · Tie each revealed answer to the card it came from
     ------------------------------------------------------------------
     presTap() appends the answer to a shared list, so with several cards
     turned it stops being obvious which answer belongs to which card.
     We number the cards and stamp the matching number on each answer.
     Wrapping rather than replacing keeps the lesson's own scoring, sound
     and XP behaviour exactly as it was.
     ================================================================== */
  function setupPresNumbering() {
    var cards = document.querySelectorAll('.pres-card');
    if (!cards.length) return;
    var order = {};
    cards.forEach(function (card, i) {
      var id = card.getAttribute('data-id');
      if (id) order[id] = i + 1;
    });

    if (typeof window.presTap === 'function' && !window.presTap._atWrapped) {
      var originalTap = window.presTap;
      var wrappedTap = function (el) {
        var out = originalTap.apply(this, arguments);
        try {
          var caps = document.getElementById('pres-caps');
          var last = caps && caps.lastElementChild;
          if (last && !last.hasAttribute('data-at-n')) {
            last.setAttribute('data-at-n', order[el.getAttribute('data-id')] || '');
          }
        } catch (e) {}
        return out;
      };
      wrappedTap._atWrapped = true;
      window.presTap = wrappedTap;
    }
  }

  /* ==================================================================
     FEATURE · Balance the match grid to the number of targets
     ------------------------------------------------------------------
     Every deck declares grid-template-columns:repeat(3,1fr) inline on the
     target row, but decks carry four, five or six targets, so most left a
     ragged last row. We pick the column count from the actual number of
     targets. Done here rather than in CSS because the value has to beat an
     inline style and because :has() is not safe to rely on across the
     devices these decks are taught from.
     ================================================================== */
  var GRID_COLUMNS = { 4: 2, 5: 3, 6: 3 };

  function fitMatchGrid() {
    var targets = document.querySelectorAll('.match-target');
    if (!targets.length) return;
    var grid = targets[0].parentNode;
    // Only touch a row that really is the grid holding the targets.
    if (!grid || grid.querySelectorAll('.match-target').length !== targets.length) return;
    var cols = GRID_COLUMNS[targets.length] || 3;
    grid.style.setProperty('grid-template-columns', 'repeat(' + cols + ',1fr)', 'important');
  }

  /* ==================================================================
     FEATURE · Mark the step the teacher has just revealed
     ------------------------------------------------------------------
     The deck's v5RevealNext() uncovers one step at a time and updates a
     "Step 2 of 3" label. Every revealed step then looked the same, so
     from the back of the room nothing said which one was being talked
     about. We move an .at-step-current marker to the newest step and
     fill one pip per step in the control strip.

     Earlier steps keep their full contrast — a class refers back to them
     while the teacher is on the next one. The CSS does the rest; without
     this file the steps still reveal exactly as they did.
     ================================================================== */
  function markCurrentStep(group) {
    var steps = group.querySelectorAll('.v5-step');
    var current = null;
    steps.forEach(function (step) {
      step.classList.remove('at-step-current');
      if (step.classList.contains('revealed')) current = step;
    });
    if (current) current.classList.add('at-step-current');

    var pips = group.parentNode && group.parentNode.querySelector('.v5-step-pips');
    if (!pips) return;
    var shown = group.querySelectorAll('.v5-step.revealed').length;
    Array.prototype.forEach.call(pips.children, function (pip, i) {
      var on = i < shown;
      // The pip that has just filled gets a moment of scale, so the eye
      // is drawn to the progress rather than having to hunt for it.
      pip.classList.toggle('at-just-on', on && !pip.classList.contains('on'));
      pip.classList.toggle('on', on);
    });
    window.setTimeout(function () {
      Array.prototype.forEach.call(pips.children, function (pip) {
        pip.classList.remove('at-just-on');
      });
    }, 260);
  }

  function setupStepBuild() {
    document.querySelectorAll('.v5-steps').forEach(function (group) {
      var slide = group.closest ? group.closest('.slide') : null;
      var controls = slide && slide.querySelector('.v5-step-controls');
      var count = group.querySelectorAll('.v5-step').length;
      if (controls && count && !controls.querySelector('.v5-step-pips')) {
        var pips = document.createElement('span');
        pips.className = 'v5-step-pips';
        // The label beside these already reads "Step 2 of 3"; repeating it
        // to a screen reader as a row of dots would only be noise.
        pips.setAttribute('aria-hidden', 'true');
        for (var i = 0; i < count; i++) pips.appendChild(document.createElement('i'));
        controls.appendChild(pips);
      }
      // A deck that opens with steps already revealed still starts in sync.
      markCurrentStep(group);
    });

    // The label is rewritten as steps come out; announce it politely so a
    // pupil using a screen reader hears the same "Step 2 of 3" the room sees.
    document.querySelectorAll('.v5-step-label').forEach(function (label) {
      if (!label.getAttribute('aria-live')) {
        label.setAttribute('role', 'status');
        label.setAttribute('aria-live', 'polite');
      }
    });

    if (typeof window.v5RevealNext === 'function' && !window.v5RevealNext._atWrapped) {
      var original = window.v5RevealNext;
      var wrapped = function (btn) {
        var out = original.apply(this, arguments);
        try {
          var slide = btn && btn.closest && btn.closest('.slide');
          var group = slide && slide.querySelector('.v5-steps');
          if (group) markCurrentStep(group);
        } catch (e) {}
        return out;
      };
      wrapped._atWrapped = true;
      window.v5RevealNext = wrapped;
    }
  }

  /* ==================================================================
     Registration
     ================================================================== */
  AT.ready(function () {
    document.querySelectorAll('.ilm').forEach(setupIlluminator);
    setupCardKeyboard(document);
    setupLiveRegions();
    setupPresNumbering();
    fitMatchGrid();
    accentLevelCards(document);
    setupStepBuild();
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
