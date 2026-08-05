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
    startIlluminatorSpotlight(block);
    scheduleIlluminatorSettle(block);
  }

  AT.replayIlluminator = replayIlluminator;

  /* ==================================================================
     FEATURE · Draw-on against the path's own length
     ------------------------------------------------------------------
     Each deck's .ilm .draw rule sets stroke-dasharray:260 and animates
     the offset from 260 to 0. Measured, the paths using it run 20 to 119
     units long — every one shorter than the dash, so none of them ever
     drew: a short path slides inside its first dash, a longer one stays
     invisible for half the animation then appears from the wrong end.

     We measure each path and hand its real length to the CSS. Geometry
     only, so this works while the slide is still hidden.
     ================================================================== */
  function fixDrawLengths(block) {
    block.querySelectorAll('.draw').forEach(function (el) {
      if (el.classList.contains('at-drawn')) return;
      if (typeof el.getTotalLength !== 'function') return;
      var len;
      try {
        len = el.getTotalLength();
      } catch (e) {
        return;
      }
      if (!len || !isFinite(len)) return;
      el.style.setProperty('--at-len', len.toFixed(1));
      el.classList.add('at-drawn');
    });
  }

  /* ==================================================================
     FEATURE · A label waits for the thing it labels
     ------------------------------------------------------------------
     94 of the 225 <text> elements in the suite's illuminators carry no
     animation of their own, so they painted at t=0 — "¼ CARBS" sitting
     on empty white for two seconds until its wedge arrived.

     Each such label is paired with the animated shape it sits inside
     (the smallest one, which is the most specific) or, failing that, the
     nearest, and held until that shape has settled. Every delay is read
     off the deck's own SVG, so nothing is written down per lesson.

     Geometry has to be measured while the slide is visible — a hidden
     slide measures as zero — and with the build frozen for one frame, or
     a shape part way through a scale-from-zero measures as a point.
     ================================================================== */
  var LABEL_DELAY_CAP = 6; // seconds — a class should never wait longer

  function isAnimated(el, root) {
    while (el && el !== root) {
      if (getComputedStyle(el).animationName !== 'none') return true;
      el = el.parentNode;
    }
    return false;
  }

  function stageIlluminatorLabels(block) {
    if (block.dataset.atLabels) return;
    var svg = block.querySelector('svg');
    if (!svg) return;
    // A hidden slide has no geometry to measure; wait until it is shown.
    if (!svg.getBoundingClientRect().width) return;
    block.dataset.atLabels = '1';

    // Shapes that finish. A looping animation never settles, so a label
    // must not be held behind one.
    var shapes = [];
    svg.querySelectorAll('*').forEach(function (el) {
      var cs = getComputedStyle(el);
      if (cs.animationName === 'none' || cs.animationIterationCount === 'infinite') return;
      shapes.push({
        el: el,
        settle: (parseFloat(cs.animationDelay) || 0) + (parseFloat(cs.animationDuration) || 0),
      });
    });
    if (!shapes.length) return;

    var labels = [];
    svg.querySelectorAll('text').forEach(function (t) {
      if (!isAnimated(t, svg)) labels.push(t);
    });
    if (!labels.length) return;

    // Freeze, measure everything in one pass, unfreeze. Synchronous, so the
    // browser paints once — the build restarts from the top and is not seen
    // to stutter.
    block.classList.add('at-ilm-measuring');
    void block.offsetWidth;
    var shapeBoxes = shapes.map(function (s) {
      return s.el.getBoundingClientRect();
    });
    var labelBoxes = labels.map(function (l) {
      return l.getBoundingClientRect();
    });
    block.classList.remove('at-ilm-measuring');
    void block.offsetWidth;

    var latest = 0;
    labels.forEach(function (label, i) {
      var lb = labelBoxes[i];
      if (!lb.width && !lb.height) return;
      var cx = lb.left + lb.width / 2;
      var cy = lb.top + lb.height / 2;
      var best = null;

      shapes.forEach(function (shape, j) {
        var b = shapeBoxes[j];
        if (!b.width && !b.height) return;
        var inside = cx >= b.left && cx <= b.right && cy >= b.top && cy <= b.bottom;
        var dx = Math.max(b.left - cx, 0, cx - b.right);
        var dy = Math.max(b.top - cy, 0, cy - b.bottom);
        var cand = {
          inside: inside,
          area: b.width * b.height,
          dist: Math.sqrt(dx * dx + dy * dy),
          settle: shape.settle,
        };
        if (!best) {
          best = cand;
        } else if (cand.inside !== best.inside) {
          if (cand.inside) best = cand;
        } else if (cand.inside ? cand.area < best.area : cand.dist < best.dist) {
          best = cand;
        }
      });

      if (!best || best.settle <= 0) return;
      var delay = Math.min(best.settle, LABEL_DELAY_CAP);
      label.style.setProperty('--at-lab-delay', delay.toFixed(2) + 's');
      label.classList.add('at-ilm-label');
      if (delay > latest) latest = delay;
    });

    // The caption names what to notice, so it still comes after everything
    // it could be naming — including a label that now arrives late.
    if (latest) {
      var end = parseFloat(block.style.getPropertyValue('--ilm-end')) || 0;
      if (latest + 0.25 > end) {
        block.style.setProperty('--ilm-end', (latest + 0.25).toFixed(2) + 's');
      }
    }
  }

  AT.stageIlluminatorLabels = stageIlluminatorLabels;

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
    if (current) {
      current.classList.add('at-step-current');
      // Measured on a 1440x900 screen: once all three steps are out, every one
      // of the 31 I Do slides is 256-345px taller than the space it has, so the
      // step the teacher has just revealed lands below the fold and the class
      // never sees it. Bring it into view — 'nearest' so a step already on
      // screen does not move, and the diagram above stays where it is.
      if (typeof current.scrollIntoView === 'function') {
        try {
          current.scrollIntoView({
            block: 'nearest',
            behavior: reduceMotion.matches ? 'auto' : 'smooth',
          });
        } catch (e) {
          current.scrollIntoView(false);
        }
      }
    }

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
     FEATURE · Live We Do orchestration and purposeful motion lifecycle
     ------------------------------------------------------------------
     The authored activities remain authoritative. This layer only makes
     their real state easier to teach from: a large class-progress rail,
     a teacher-controlled random choice that never reveals an answer, and
     a completed-connection trail that repeats the lesson's exact wording.

     The motion lifecycle keeps authored SVG builds purposeful: animations
     wait while their slide is off screen, replay when the I Do slide opens,
     receive one short spotlight, and then settle only decorative glow/ripple
     loops in mixed build diagrams. The four loop-only concept diagrams are
     deliberately left continuous.
     ================================================================== */
  var atActivityFrame = 0;
  var atMotionTimers = new WeakMap();

  function atCleanText(el) {
    return ((el && el.textContent) || '').replace(/\s+/g, ' ').trim();
  }

  function atAnnounce(text) {
    var live = document.getElementById('at-activity-live');
    if (!live) {
      live = document.createElement('div');
      live.id = 'at-activity-live';
      live.className = 'at-sr-only';
      live.setAttribute('role', 'status');
      live.setAttribute('aria-live', 'polite');
      live.setAttribute('aria-atomic', 'true');
      document.body.appendChild(live);
    }
    live.textContent = '';
    window.setTimeout(function () {
      live.textContent = text;
    }, 20);
  }

  function atEnsureActivityBar(slide, kind, total) {
    if (!slide) return null;
    var bar = slide.querySelector('.at-activity-bar[data-at-activity="' + kind + '"]');
    if (bar) {
      var currentTrack = bar.querySelector('.at-activity-track');
      if (currentTrack) currentTrack.setAttribute('aria-valuemax', String(total));
      return bar;
    }

    bar = document.createElement('div');
    bar.className = 'at-activity-bar';
    bar.setAttribute('data-at-activity', kind);

    var label = document.createElement('span');
    label.className = 'at-activity-label';
    label.textContent = 'Class progress';

    var track = document.createElement('span');
    track.className = 'at-activity-track';
    track.setAttribute('role', 'progressbar');
    track.setAttribute('aria-label', kind === 'presentation' ? 'Prediction-card progress' : 'Matching progress');
    track.setAttribute('aria-valuemin', '0');
    track.setAttribute('aria-valuemax', String(total));
    track.setAttribute('aria-valuenow', '0');

    var fill = document.createElement('span');
    fill.className = 'at-activity-fill';
    track.appendChild(fill);

    var count = document.createElement('span');
    count.className = 'at-activity-count';
    count.setAttribute('aria-live', 'polite');
    count.textContent = '0 / ' + total;

    var actions = document.createElement('span');
    actions.className = 'at-activity-actions';

    if (kind === 'presentation') {
      var pick = document.createElement('button');
      pick.type = 'button';
      pick.className = 'at-random-pick';
      pick.textContent = 'Pick a card';
      pick.setAttribute('aria-label', 'Choose an unrevealed card without revealing it');
      pick.setAttribute('aria-controls', 'pres-pills');
      pick.addEventListener('click', function () {
        atPickPresentationCard(slide);
      });
      actions.appendChild(pick);
    }

    bar.appendChild(label);
    bar.appendChild(track);
    bar.appendChild(count);
    bar.appendChild(actions);

    var anchor = slide.querySelector('.li-box');
    if (anchor && anchor.parentNode) {
      anchor.parentNode.insertBefore(bar, anchor.nextSibling);
    } else {
      slide.insertBefore(bar, slide.firstChild);
    }
    return bar;
  }

  function atSetActivityProgress(bar, done, total) {
    if (!bar) return;
    var safeTotal = Math.max(total, 1);
    var track = bar.querySelector('.at-activity-track');
    var fill = bar.querySelector('.at-activity-fill');
    var count = bar.querySelector('.at-activity-count');
    var previous = parseInt(bar.getAttribute('data-at-done') || '0', 10);
    var complete = total > 0 && done >= total;

    if (track) {
      track.setAttribute('aria-valuemax', String(total));
      track.setAttribute('aria-valuenow', String(done));
      track.setAttribute('aria-valuetext', done + ' of ' + total + ' completed');
    }
    if (fill) fill.style.width = Math.round((done / safeTotal) * 100) + '%';
    if (count) count.textContent = done + ' / ' + total;

    bar.classList.toggle('at-complete', complete);
    if (complete && previous !== done) {
      bar.classList.remove('at-just-complete');
      void bar.offsetWidth;
      bar.classList.add('at-just-complete');
      window.setTimeout(function () {
        bar.classList.remove('at-just-complete');
      }, 520);
    }
    bar.setAttribute('data-at-done', String(done));
  }

  function atPickPresentationCard(slide) {
    var cards = Array.prototype.slice.call(slide.querySelectorAll('.pres-card'));
    var unrevealed = cards.filter(function (card) {
      return !card.classList.contains('done');
    });
    if (!unrevealed.length) return;

    var last = slide.getAttribute('data-at-last-pick');
    var pool = unrevealed.filter(function (card) {
      return card.getAttribute('data-at-card') !== last;
    });
    if (!pool.length) pool = unrevealed;

    cards.forEach(function (card) {
      card.classList.remove('at-picked');
    });
    var choice = pool[Math.floor(Math.random() * pool.length)];
    choice.classList.add('at-picked');
    slide.setAttribute('data-at-last-pick', choice.getAttribute('data-at-card') || '');
    try {
      choice.focus({ preventScroll: true });
    } catch (e) {
      choice.focus();
    }
    if (typeof choice.scrollIntoView === 'function') {
      try {
        choice.scrollIntoView({ block: 'nearest', behavior: reduceMotion.matches ? 'auto' : 'smooth' });
      } catch (e) {}
    }
    atAnnounce('Card ' + (choice.getAttribute('data-at-card') || '') + ' selected.');
    atQueueActivityRefresh();
  }

  function atRefreshPresentationActivity() {
    var cards = Array.prototype.slice.call(document.querySelectorAll('.pres-card'));
    if (!cards.length) return;
    var slide = cards[0].closest ? cards[0].closest('.slide') : null;
    if (!slide) return;

    cards.forEach(function (card, i) {
      card.setAttribute('data-at-card', String(i + 1));
      card.setAttribute('aria-pressed', card.classList.contains('done') ? 'true' : 'false');
      if (card.classList.contains('done')) card.classList.remove('at-picked');
    });

    var done = cards.filter(function (card) {
      return card.classList.contains('done');
    }).length;
    var bar = atEnsureActivityBar(slide, 'presentation', cards.length);
    atSetActivityProgress(bar, done, cards.length);

    var pick = bar && bar.querySelector('.at-random-pick');
    if (pick) {
      pick.disabled = done >= cards.length;
      pick.setAttribute('aria-disabled', pick.disabled ? 'true' : 'false');
    }
  }

  function atMatchId(pill) {
    var raw = (pill && pill.getAttribute('onclick')) || '';
    var match = raw.match(/selectKW\s*\(\s*this\s*,\s*['"]([^'"]+)['"]/i);
    return match ? match[1] : '';
  }

  function atEnsurePairTrail(slide, grid) {
    var trail = slide.querySelector('.at-pair-trail');
    if (trail) return trail;

    trail = document.createElement('div');
    trail.className = 'at-pair-trail';
    trail.hidden = true;
    trail.setAttribute('aria-live', 'polite');
    trail.setAttribute('aria-atomic', 'false');

    var label = document.createElement('span');
    label.className = 'at-pair-label';
    label.textContent = 'Completed connections';

    var list = document.createElement('div');
    list.className = 'at-pair-list';

    trail.appendChild(label);
    trail.appendChild(list);
    if (grid && grid.parentNode) {
      grid.parentNode.insertBefore(trail, grid.nextSibling);
    } else {
      slide.appendChild(trail);
    }
    return trail;
  }

  function atRenderPairTrail(slide, pills, targets) {
    var byId = {};
    pills.forEach(function (pill) {
      var id = atMatchId(pill);
      if (id) byId[id] = pill;
    });

    var pairs = [];
    targets.forEach(function (target) {
      if (!target.classList.contains('correct')) return;
      var id = target.getAttribute('data-correct') || '';
      if (id && byId[id]) pairs.push({ id: id, pill: byId[id], target: target });
    });

    var grid = targets[0] && targets[0].parentNode;
    var trail = atEnsurePairTrail(slide, grid);
    var signature = pairs.map(function (pair) { return pair.id; }).join('|');
    trail.hidden = pairs.length === 0;
    if (trail.getAttribute('data-at-signature') === signature) return;
    trail.setAttribute('data-at-signature', signature);

    var list = trail.querySelector('.at-pair-list');
    list.textContent = '';
    pairs.forEach(function (pair, i) {
      var chip = document.createElement('div');
      chip.className = 'at-pair-chip';
      chip.setAttribute('data-at-pair', pair.id);

      var number = document.createElement('span');
      number.className = 'at-pair-number';
      number.setAttribute('aria-hidden', 'true');
      number.textContent = String(i + 1);

      var key = document.createElement('span');
      key.className = 'at-pair-key';
      key.textContent = atCleanText(pair.pill);

      var arrow = document.createElement('span');
      arrow.className = 'at-pair-arrow';
      arrow.setAttribute('aria-hidden', 'true');
      arrow.textContent = '→';

      var value = document.createElement('span');
      value.className = 'at-pair-target';
      value.textContent = atCleanText(pair.target);

      chip.appendChild(number);
      chip.appendChild(key);
      chip.appendChild(arrow);
      chip.appendChild(value);
      list.appendChild(chip);
    });
  }

  function atRefreshMatchingActivity() {
    var targets = Array.prototype.slice.call(document.querySelectorAll('.match-target'));
    var pills = Array.prototype.slice.call(document.querySelectorAll('#kw-pills .match-pill'));
    if (!targets.length || !pills.length) return;
    var slide = targets[0].closest ? targets[0].closest('.slide') : null;
    if (!slide) return;

    var done = targets.filter(function (target) {
      return target.classList.contains('correct');
    }).length;
    var selected = slide.querySelector('.match-pill.selected');
    slide.classList.toggle('at-match-holding', !!selected);

    pills.forEach(function (pill) {
      pill.setAttribute('aria-pressed', pill.classList.contains('selected') ? 'true' : 'false');
      pill.setAttribute('aria-disabled', pill.classList.contains('placed') ? 'true' : 'false');
    });
    targets.forEach(function (target) {
      target.setAttribute('aria-pressed', target.classList.contains('correct') ? 'true' : 'false');
      target.setAttribute('aria-disabled', target.classList.contains('correct') ? 'true' : 'false');
    });

    var bar = atEnsureActivityBar(slide, 'matching', targets.length);
    atSetActivityProgress(bar, done, targets.length);
    atRenderPairTrail(slide, pills, targets);
  }

  function atQueueActivityRefresh() {
    if (atActivityFrame) return;
    atActivityFrame = window.requestAnimationFrame(function () {
      atActivityFrame = 0;
      atRefreshPresentationActivity();
      atRefreshMatchingActivity();
    });
  }

  function setupWeDoEnhancements() {
    atRefreshPresentationActivity();
    atRefreshMatchingActivity();

    var slides = [];
    document.querySelectorAll('.pres-card, .match-target').forEach(function (el) {
      var slide = el.closest ? el.closest('.slide') : null;
      if (slide && slides.indexOf(slide) === -1) slides.push(slide);
    });

    slides.forEach(function (slide) {
      var observer = new MutationObserver(function () {
        atQueueActivityRefresh();
      });
      observer.observe(slide, {
        subtree: true,
        attributes: true,
        attributeOldValue: true,
        attributeFilter: ['class'],
      });
    });

    AT.onSlideChange(function (slide) {
      if (slide && slide.querySelector('.pres-card, .match-target')) atQueueActivityRefresh();
    });
    document.documentElement.setAttribute('data-at-build-upgrade', 'ready');
  }

  function atEnsureMotionSweep(block) {
    var sweep = block.querySelector('.at-ilm-sweep');
    if (sweep) return sweep;
    sweep = document.createElement('span');
    sweep.className = 'at-ilm-sweep';
    sweep.setAttribute('aria-hidden', 'true');
    var replay = block.querySelector('.ilm-replay');
    if (replay) block.insertBefore(sweep, replay);
    else block.appendChild(sweep);
    return sweep;
  }


  /* Keep words readable when a diagram uses a pulsing glow on a group that
     contains both a shape and its text label. The pulse moves to the visual
     branches only; the exact authored label remains inside the finite build. */
  function atProtectLoopLabels(block) {
    if (!block || block.getAttribute('data-at-loop-labels') === 'ready') return;
    block.setAttribute('data-at-loop-labels', 'ready');

    block.querySelectorAll('.glow').forEach(function (loop) {
      var labels = loop.querySelectorAll ? loop.querySelectorAll('text') : [];
      if (!labels.length) return;

      var delay = getComputedStyle(loop).animationDelay || '';
      loop.classList.remove('glow');

      Array.prototype.forEach.call(loop.children || [], function (child) {
        var tag = (child.tagName || '').toLowerCase();
        if (tag === 'text' || (child.querySelector && child.querySelector('text'))) return;
        child.classList.add('glow', 'at-label-safe-glow');
        if (delay && delay !== '0s') child.style.animationDelay = delay;
      });
    });
  }

  function atClassifyIlluminatorMotion(block) {
    if (block.getAttribute('data-at-motion-ready')) return;
    block.setAttribute('data-at-motion-ready', '1');
    var hasFinite = false;
    var loops = [];

    block.querySelectorAll('svg *').forEach(function (el) {
      var cs = getComputedStyle(el);
      if (cs.animationName === 'none') return;
      if (cs.animationIterationCount === 'infinite') loops.push(el);
      else hasFinite = true;
    });

    var count = 0;
    if (hasFinite) {
      loops.forEach(function (el) {
        if (el.classList.contains('glow')) {
          el.classList.add('at-settle-glow');
          count++;
        } else if (el.classList.contains('rip')) {
          el.classList.add('at-settle-rip');
          count++;
        }
      });
    }
    block.setAttribute('data-at-settle-count', String(count));
  }

  function startIlluminatorSpotlight(block) {
    if (!block || reduceMotion.matches) return;
    atEnsureMotionSweep(block);
    block.classList.remove('at-ilm-replaying');
    void block.offsetWidth;
    block.classList.add('at-ilm-replaying');

    var state = atMotionTimers.get(block) || {};
    if (state.spotlight) window.clearTimeout(state.spotlight);
    state.spotlight = window.setTimeout(function () {
      block.classList.remove('at-ilm-replaying');
    }, 1350);
    atMotionTimers.set(block, state);
  }

  function scheduleIlluminatorSettle(block) {
    if (!block) return;
    atClassifyIlluminatorMotion(block);
    block.classList.remove('at-ilm-settled');

    var state = atMotionTimers.get(block) || {};
    if (state.settle) window.clearTimeout(state.settle);
    var count = parseInt(block.getAttribute('data-at-settle-count') || '0', 10);
    if (!count || reduceMotion.matches) {
      atMotionTimers.set(block, state);
      return;
    }

    var end = parseFloat(block.style.getPropertyValue('--ilm-end')) || 2.4;
    var delay = Math.min(8000, Math.max(2800, (end + 1.35) * 1000));
    state.settle = window.setTimeout(function () {
      if (block.isConnected) block.classList.add('at-ilm-settled');
    }, delay);
    atMotionTimers.set(block, state);
  }

  function setupMotionLifecycle() {
    document.querySelectorAll('.ilm').forEach(function (block) {
      atEnsureMotionSweep(block);
      atProtectLoopLabels(block);
      atClassifyIlluminatorMotion(block);
    });

    AT.onSlideChange(function (slide) {
      document.querySelectorAll('.ilm.at-ilm-replaying').forEach(function (block) {
        if (!slide || !slide.contains(block)) block.classList.remove('at-ilm-replaying');
      });
      if (!slide) return;
      slide.querySelectorAll('.ilm').forEach(function (block) {
        window.requestAnimationFrame(function () {
          var active = document.querySelector('.slide.active');
          if (active && active.contains(block)) replayIlluminator(block);
        });
      });
    });
  }

  /* ==================================================================
     Registration
     ================================================================== */
  AT.ready(function () {
    document.querySelectorAll('.ilm').forEach(function (block) {
      setupIlluminator(block);
      fixDrawLengths(block);
    });
    // Label timing needs the slide on screen to measure, so it is staged the
    // first time the I Do slide is reached rather than at boot.
    AT.onSlideChange(function (slide) {
      if (!slide) return;
      slide.querySelectorAll('.ilm').forEach(stageIlluminatorLabels);
    });
    setupCardKeyboard(document);
    setupLiveRegions();
    setupPresNumbering();
    fitMatchGrid();
    accentLevelCards(document);
    setupStepBuild();
    setupWeDoEnhancements();
    setupMotionLifecycle();
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
/* ASDAN-VISUAL-LEARNING:JS:BEGIN v1 */
window.ASDANVisualPayloads = Object.assign(window.ASDANVisualPayloads || {}, {"CAREERS_W1_My_Strengths":{"path":"BUILD_ASDAN/Careers/CAREERS_W1_My_Strengths.html","pathway":"BUILD","subsection":"Careers","lessonTitle":"Week 1 · My Strengths","targetTitle":"We Do 1","title":"Strengths → actions → work evidence","purpose":"Make strengths concrete before pupils build a profile, reducing empty claims such as ‘I am good at teamwork’.","activity":{"type":"sort","prompt":"Place each example under the strength it actually proves. Say the observable action, not just the positive word.","categories":[{"id":"team","icon":"👥","label":"TEAMWORK"},{"id":"reliable","icon":"⏱","label":"RELIABILITY"},{"id":"solve","icon":"🧩","label":"PROBLEM SOLVING"}],"items":[{"id":"i1","icon":"👥","label":"I shared the materials and checked my partner understood.","answer":"team","reason":"The action supports another person and the shared task."},{"id":"i2","icon":"⏱","label":"I arrived with the right equipment before the start.","answer":"reliable","reason":"It shows preparation and keeping a commitment."},{"id":"i3","icon":"🧩","label":"When the first method failed, I tried a second safe method.","answer":"solve","reason":"It shows a problem, a change and a result."},{"id":"i4","icon":"👥","label":"I listened, then used one idea from someone else.","answer":"team","reason":"Listening affects the group decision."},{"id":"i5","icon":"⏱","label":"I completed the agreed step by the deadline.","answer":"reliable","reason":"The evidence is a kept time commitment."},{"id":"i6","icon":"🧩","label":"I broke a large task into three smaller steps.","answer":"solve","reason":"The strategy makes the task manageable."}],"completion":"A strength becomes useful for careers when it is attached to something a person actually did."},"independent":"Choose two strengths. For each, add one real example using: I did… / This shows… / It could help in…","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original three-lane strength evidence map with action cards moving from pupil experience to workplace use.","mediaKey":"careers","slug":"CAREERS_W1_My_Strengths","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"f1d0562fcce182b9f258fc0a83e70563777318aa0fd9983309ece6cb2bea3d42"},"CAREERS_W2_Jobs_in_My_Community":{"path":"BUILD_ASDAN/Careers/CAREERS_W2_Jobs_in_My_Community.html","pathway":"BUILD","subsection":"Careers","lessonTitle":"Week 2 · Jobs in My Community","targetTitle":"We Do 1","title":"Community job-system map","purpose":"Show jobs as visible services and task systems rather than a list of unfamiliar titles.","activity":{"type":"hotspot","scene":"community","prompt":"Open each place on the community map. Identify the job, who benefits and one visible task that the worker completes.","hotspots":[{"id":"h1","x":18,"y":24,"label":"HEALTH CENTRE · care roles","note":"A receptionist organises contact and a healthcare worker supports patients; the place needs more than one job."},{"id":"h2","x":50,"y":18,"label":"SUPERMARKET · retail roles","note":"Stock, customer service, deliveries and safety are different tasks inside one workplace."},{"id":"h3","x":82,"y":27,"label":"COLLEGE · education roles","note":"Tutors, support staff, administrators and site staff all contribute to learning."},{"id":"h4","x":23,"y":66,"label":"CONSTRUCTION SITE · trades","note":"A site combines skilled trades, planning, safety and teamwork."},{"id":"h5","x":52,"y":72,"label":"PARK · environment roles","note":"Grounds and community roles maintain spaces that local people use."},{"id":"h6","x":82,"y":65,"label":"CAFÉ · hospitality roles","note":"Food preparation, serving, hygiene and payment tasks work together."}],"completion":"A workplace is a system of connected roles, not a single job title."},"independent":"Pick one local workplace. Draw a role web with at least three jobs, one task for each and who receives the service.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original local community map with six accessible workplace hotspots and linked worker-task-audience callouts.","mediaKey":"careers","slug":"CAREERS_W2_Jobs_in_My_Community","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"91e671f49a2719655a82586c31bb1adc11d3c8de6cf74c2d9fe3db177a440898"},"CAREERS_W3_Skills_Employers_Want":{"path":"BUILD_ASDAN/Careers/CAREERS_W3_Skills_Employers_Want.html","pathway":"BUILD","subsection":"Careers","lessonTitle":"Week 3 · Skills Employers Want","targetTitle":"We Do 1","title":"Evidence or empty claim?","purpose":"Teach pupils to distinguish evidence from labels so later profiles and applications are more independent and credible.","activity":{"type":"evidence","prompt":"Select every statement that would count as usable evidence of an employability skill. Reject statements that are only labels or praise.","statements":[{"id":"e1","label":"I followed the four-step instruction and checked step 3 before finishing.","correct":true,"reason":"It names an action and a checking behaviour."},{"id":"e2","label":"I am amazing at everything.","correct":false,"reason":"It is a broad claim with no observable evidence."},{"id":"e3","label":"I told the team early that the material was missing and suggested an alternative.","correct":true,"reason":"It evidences communication and problem solving."},{"id":"e4","label":"The teacher said I was good.","correct":false,"reason":"It does not say what the pupil did."},{"id":"e5","label":"I completed my role, then helped another person without taking over.","correct":true,"reason":"It shows responsibility and teamwork."},{"id":"e6","label":"I never make mistakes.","correct":false,"reason":"It is implausible and gives no evidence of learning."},{"id":"e7","label":"I used feedback to change the second version.","correct":true,"reason":"It shows response to feedback and improvement."},{"id":"e8","label":"I like jobs.","correct":false,"reason":"It is an interest statement, not skill evidence."}],"completion":"Employability evidence is specific, observable and connected to a task or result."},"independent":"Write one claim about a skill. Underline the action, circle the result and add the context where it happened.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original evidence-filter conveyor with action, context and result lenses rejecting unsupported claims.","mediaKey":"careers","slug":"CAREERS_W3_Skills_Employers_Want","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"4d98ebbbdb753e69cf0016e45d890e31fe2d119a3af884b42a8948f858315f82"},"CAREERS_W4_Routines_and_Reliability":{"path":"BUILD_ASDAN/Careers/CAREERS_W4_Routines_and_Reliability.html","pathway":"BUILD","subsection":"Careers","lessonTitle":"Week 4 · Routines & Reliability","targetTitle":"We Do 1","title":"Build a reliable arrival routine","purpose":"Make routine planning visible and causal, supporting pupils who struggle to hold a multi-step plan in working memory.","activity":{"type":"sequence","prompt":"Put the routine in an order that makes arriving ready more likely. Explain which step protects against a problem.","steps":[{"id":"s1","label":"Check tomorrow’s time, place and required equipment.","reason":"The plan begins while there is still time to solve a problem."},{"id":"s2","label":"Prepare clothes, equipment and travel information.","reason":"Preparation removes avoidable decisions in the morning."},{"id":"s3","label":"Set an alarm and a back-up prompt.","reason":"A second cue protects against one missed signal."},{"id":"s4","label":"Leave with enough travel margin.","reason":"A margin allows for ordinary delays."},{"id":"s5","label":"Arrive, check in and begin the agreed first task.","reason":"Reliability includes starting correctly, not only reaching the building."},{"id":"s6","label":"Review what worked and change one weak step.","reason":"The routine improves through evidence rather than blame."}],"completion":"Reliable behaviour is a repeatable system with prompts, preparation, margins and review."},"independent":"Create your own five-step readiness strip for one real lesson, appointment or work-related visit. Add one back-up step.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original timeline from evening preparation to arrival, with delay shields and a review loop.","mediaKey":"careers","slug":"CAREERS_W4_Routines_and_Reliability","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"8581026623d293f6c5db73bc223ee2392793bec9080f3f87f68ca15d27229958"},"CAREERS_W5_Applying_Myself":{"path":"BUILD_ASDAN/Careers/CAREERS_W5_Applying_Myself.html","pathway":"BUILD","subsection":"Careers","lessonTitle":"Week 5 · Applying Myself","targetTitle":"We Do 1","title":"Application profile strength check","purpose":"Externalise the hidden decisions behind a short profile so pupils can plan before writing independently.","activity":{"type":"model","prompt":"Choose one option in each control, predict the strength of the profile, then run the check. The screen tests structure; pupils still write their own words.","controls":[{"id":"c1","label":"Opening","default":"vague","options":[{"value":"vague","label":"I am a nice person","quality":0,"feedback":"Friendly but too vague for an application."},{"value":"specific","label":"I am reliable in practical team tasks","quality":2,"feedback":"Names a relevant strength and context."},{"value":"copied","label":"I am a dynamic self-starter","quality":0,"feedback":"Generic language may not sound authentic."}]},{"id":"c2","label":"Evidence","default":"none","options":[{"value":"none","label":"No example","quality":0,"feedback":"A claim without evidence is weak."},{"value":"action","label":"One action only","quality":1,"feedback":"Better, but a result would strengthen it."},{"value":"action_result","label":"Action + result","quality":2,"feedback":"Shows what happened and why it matters."}]},{"id":"c3","label":"Fit","default":"any","options":[{"value":"any","label":"Could be for any role","quality":0,"feedback":"The reader cannot see the connection."},{"value":"named","label":"Links to one task in the opportunity","quality":2,"feedback":"Shows that the application was adapted."},{"value":"wish","label":"Says only that I want it","quality":1,"feedback":"Motivation helps but does not prove fit."}]}],"outcomes":[{"min":0,"max":2,"label":"too vague","message":"The reader cannot yet see a trustworthy match."},{"min":3,"max":4,"label":"partly evidenced","message":"One useful element is present; strengthen the missing link."},{"min":5,"max":6,"label":"clear and evidenced","message":"Strength, example and opportunity fit connect."}],"completion":"A useful profile links a truthful strength to a specific example and a real opportunity task.","predictionOptions":["The profile will be too vague","The profile will be partly convincing","The profile will show a clear fit"],"requiredRuns":1},"independent":"Write a four-sentence profile: strength / evidence / opportunity link / next step. Use your own words and a real example.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original three-link application profile bridge: strength, evidence and opportunity fit.","mediaKey":"careers","slug":"CAREERS_W5_Applying_Myself","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"b396b29ca5ed0de10c8837c8dfe399a65e5d16b0a00b60937a269e7a8e4f50f3"},"CAREERS_W7_After_Year_11":{"path":"BUILD_ASDAN/Careers/CAREERS_W7_After_Year_11.html","pathway":"BUILD","subsection":"Careers","lessonTitle":"Week 6 · What Happens After Year 11","targetTitle":"We Do 1","title":"Compare post-16 routes safely","purpose":"Give pupils a stable comparison framework while keeping live entry requirements and vacancies for current-source checking.","activity":{"type":"sort","prompt":"Sort each feature under the route it describes. Then identify one question a pupil would need to ask before choosing.","categories":[{"id":"college","icon":"🏫","label":"COLLEGE COURSE"},{"id":"apprentice","icon":"🛠","label":"APPRENTICESHIP"},{"id":"training","icon":"🧭","label":"TRAINING / SUPPORTED ROUTE"},{"id":"sixth","icon":"📚","label":"SIXTH FORM"}],"items":[{"id":"i1","icon":"🏫","label":"Mostly classroom or practical course learning at a college.","answer":"college","reason":"The route is organised around a chosen course."},{"id":"i2","icon":"🛠","label":"Paid employment combined with off-the-job training.","answer":"apprentice","reason":"Work and training are both required."},{"id":"i3","icon":"🧭","label":"A programme may build employability, independence or sector skills with added support.","answer":"training","reason":"The route can prepare a learner for later work or study."},{"id":"i4","icon":"📚","label":"A school or college route usually centred on Level 3 study.","answer":"sixth","reason":"It commonly continues academic or applied study."},{"id":"i5","icon":"🛠","label":"Vacancies are applied for and an employer selects the apprentice.","answer":"apprentice","reason":"It is not automatic enrolment on a course."},{"id":"i6","icon":"🏫","label":"Entry requirements, course level and travel must be checked.","answer":"college","reason":"A course name alone is not enough."},{"id":"i7","icon":"🧭","label":"The exact provider, progression route and support offer must be verified.","answer":"training","reason":"Training routes vary and need current checking."},{"id":"i8","icon":"📚","label":"Subject combination and assessment style affect suitability.","answer":"sixth","reason":"The learner needs to compare how the programme works."}],"completion":"Post-16 routes are compared through current facts, fit, access and progression—not by ranking one route as best for everyone."},"independent":"Choose two routes. Complete a comparison box for: what I do / how I learn / what I must check / my next enquiry.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original four-route station map with equal-sized paths and a live-information checkpoint.","mediaKey":"careers","slug":"CAREERS_W7_After_Year_11","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"4805179c2f869b4fd2641d7040039faa87368fdd0b0a1e7e9fbc23f905005144"},"CAREERS_W6_My_Career_Profile":{"path":"BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html","pathway":"BUILD","subsection":"Careers","lessonTitle":"Week 7 · My Career Profile","targetTitle":"We Do 1","title":"Career-profile decision panel","purpose":"Turn the final profile into a decision tool, not a decorative poster or collection of unsupported adjectives.","activity":{"type":"model","prompt":"Build a career-profile panel from truthful information. Predict whether another person could use it to suggest a next step.","controls":[{"id":"c1","label":"Strength evidence","default":"label","options":[{"value":"label","label":"Strength word only","quality":0,"feedback":"The reader cannot verify the claim."},{"value":"example","label":"Strength + real example","quality":2,"feedback":"The example makes the claim usable."}]},{"id":"c2","label":"Interest detail","default":"broad","options":[{"value":"broad","label":"I like practical things","quality":1,"feedback":"A starting point, but still broad."},{"value":"specific","label":"I enjoy measuring, assembling and improving objects","quality":2,"feedback":"Specific activities help match opportunities."}]},{"id":"c3","label":"Next step","default":"none","options":[{"value":"none","label":"No next step","quality":0,"feedback":"The profile cannot guide action."},{"value":"enquiry","label":"One named enquiry or experience","quality":2,"feedback":"The profile leads to an achievable action."}]}],"outcomes":[{"min":0,"max":2,"label":"profile needs evidence","message":"It describes the pupil but cannot yet guide a decision."},{"min":3,"max":4,"label":"profile is usable","message":"Another person can begin to discuss suitable directions."},{"min":5,"max":6,"label":"profile leads to action","message":"Evidence, interests and a next enquiry connect."}],"completion":"A career profile is useful when it is authentic, evidenced and ends with a manageable next action.","predictionOptions":["It will only describe me","It will help someone suggest a route","It will lead to a clear next enquiry"],"requiredRuns":1},"independent":"Create the final profile using two evidenced strengths, two specific interests, one preferred working condition and one next enquiry.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original profile dashboard with evidence tags, interest controls, working-condition symbols and an action arrow.","mediaKey":"careers","slug":"CAREERS_W6_My_Career_Profile","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"ae0ae247e50af89f16b5e4db383048d18dc0d8a8a37d6ab03bbcad2ccc6d9f88"},"LI_W1_Where_Money_Comes_From":{"path":"BUILD_ASDAN/Living_Independently/LI_W1_Where_Money_Comes_From.html","pathway":"BUILD","subsection":"Living Independently","lessonTitle":"Week 1 · Where Money Comes From","targetTitle":"We Do 1","title":"Money-flow sorting board","purpose":"Make the direction of money visible without asking pupils to disclose personal finances.","activity":{"type":"sort","prompt":"Sort each example into money coming in, money going out or money moved aside. Explain what visible clue made the decision.","categories":[{"id":"in","icon":"➕","label":"MONEY IN"},{"id":"out","icon":"➖","label":"MONEY OUT"},{"id":"save","icon":"🏦","label":"SET ASIDE"}],"items":[{"id":"i1","icon":"➕","label":"Wages paid for work completed.","answer":"in","reason":"The amount enters the budget as income."},{"id":"i2","icon":"➕","label":"A regular benefit payment shown on a mock statement.","answer":"in","reason":"It is money received; use produced examples, never real documents."},{"id":"i3","icon":"➖","label":"Bus fare for a planned journey.","answer":"out","reason":"It is a cost paid from available money."},{"id":"i4","icon":"➖","label":"Phone credit purchased this week.","answer":"out","reason":"The payment reduces the amount left."},{"id":"i5","icon":"🏦","label":"£5 moved into a savings pot for an agreed goal.","answer":"save","reason":"It remains the pupil’s money but is reserved."},{"id":"i6","icon":"➖","label":"An unexpected replacement charger.","answer":"out","reason":"It is an unplanned cost that still leaves the budget."},{"id":"i7","icon":"🏦","label":"Money kept for next month’s travel.","answer":"save","reason":"The purpose is future essential spending."},{"id":"i8","icon":"➕","label":"Money received for a completed one-off job.","answer":"in","reason":"The payment adds to available income."}],"completion":"A budget begins by distinguishing income, spending and money deliberately reserved for later."},"independent":"Use the supplied fictional scenario. Mark every amount IN, OUT or SET ASIDE and calculate the amount left.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original three-channel money-flow board using arrows, mock amounts and privacy-safe example cards.","mediaKey":"money","slug":"LI_W1_Where_Money_Comes_From","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"4256b2aea6195ab55c1bef2c1bc1657724cc3a8639610db761037d5d54448955"},"LI_W2_Notes_and_Coins":{"path":"BUILD_ASDAN/Living_Independently/LI_W2_Notes_and_Coins.html","pathway":"BUILD","subsection":"Living Independently","lessonTitle":"Week 2 · Notes & Coins","targetTitle":"We Do 1","title":"Make the amount · more than one route","purpose":"Develop flexible amount recognition and a visible checking routine rather than speed-based recall.","activity":{"type":"sort","prompt":"Build each target amount by matching the set of notes and coins. More than one correct combination may exist; explain how you checked.","categories":[{"id":"a","icon":"£","label":"£1.50"},{"id":"b","icon":"£","label":"£2.35"},{"id":"c","icon":"£","label":"£5.00"}],"items":[{"id":"i1","icon":"🪙","label":"£1 + 50p","answer":"a","reason":"100p + 50p = 150p."},{"id":"i2","icon":"🪙","label":"£1 + £1 + 20p + 10p + 5p","answer":"b","reason":"200p + 35p = 235p."},{"id":"i3","icon":"💷","label":"One £5 note","answer":"c","reason":"The note already equals the target."},{"id":"i4","icon":"🪙","label":"50p + 50p + 20p + 20p + 10p","answer":"a","reason":"The coins total 150p."},{"id":"i5","icon":"🪙","label":"£2 + 20p + 10p + 5p","answer":"b","reason":"The pounds and pence total £2.35."},{"id":"i6","icon":"🪙","label":"£2 + £2 + £1","answer":"c","reason":"The three coins total £5."},{"id":"i7","icon":"🪙","label":"£1 + 20p + 20p + 10p","answer":"a","reason":"The total is £1.50."},{"id":"i8","icon":"🪙","label":"£1 + £1 + 50p","answer":"b","reason":"This totals £2.50, so it does not match £2.35."}],"completion":"Money combinations are checked by converting to a common unit or adding pounds and pence systematically."},"independent":"Choose two prices from the fictional shop. Show two different ways to make each amount and check both totals.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original accessible UK money-combination board using clear symbols and printed values rather than photorealistic currency.","mediaKey":"money","slug":"LI_W2_Notes_and_Coins","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"a66e33996499393f153ec86f8d5d90bc5b59cd61ccd19aa7d7b6949a90673c31"},"LI_W3_Needs_vs_Wants":{"path":"BUILD_ASDAN/Living_Independently/LI_W3_Needs_vs_Wants.html","pathway":"BUILD","subsection":"Living Independently","lessonTitle":"Week 3 · Needs vs Wants","targetTitle":"We Do 1","title":"Needs, wants and the reason between them","purpose":"Prevent simplistic sorting by making justification and context visible.","activity":{"type":"evidence","prompt":"Select the statements that use context to justify a need or a want. Reject statements that treat the label as fixed for every person.","statements":[{"id":"e1","label":"The bus fare is a need in this scenario because it is the only safe route to the appointment.","correct":true,"reason":"The decision is linked to a specific situation and purpose."},{"id":"e2","label":"A phone is always a want for everybody.","correct":false,"reason":"Access, safety and work contexts can change the judgement."},{"id":"e3","label":"Food for planned meals is an essential budget category.","correct":true,"reason":"The statement identifies a necessary function."},{"id":"e4","label":"Anything enjoyable is automatically a want.","correct":false,"reason":"Enjoyment does not decide whether something is essential."},{"id":"e5","label":"Replacing a broken coat can be a need when no safe alternative is available.","correct":true,"reason":"The context explains why the purchase is necessary."},{"id":"e6","label":"A branded version may be a want even when the basic item is needed.","correct":true,"reason":"It separates the function from an optional feature."},{"id":"e7","label":"If my friend has it, I need it.","correct":false,"reason":"Peer ownership is not evidence of necessity."},{"id":"e8","label":"The same item can move between need and want depending on the person and situation.","correct":true,"reason":"The category depends on function and context."}],"completion":"Needs and wants are reasoned judgements about function, alternatives and context—not permanent labels attached to objects."},"independent":"Use the fictional weekly budget. Choose one essential, one optional item and one item that depends on context. Write the reason for each.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original balance scale with function, alternative and consequence evidence weights.","mediaKey":"money","slug":"LI_W3_Needs_vs_Wants","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"50abd0b7644421b93485255688493f7bcc2dcaa4f55f93a6ae115f0f76d81527"},"LI_W4_Everyday_Prices":{"path":"BUILD_ASDAN/Living_Independently/LI_W4_Everyday_Prices.html","pathway":"BUILD","subsection":"Living Independently","lessonTitle":"Week 4 · Everyday Prices","targetTitle":"We Do 1","title":"Price, quantity and hidden-cost comparator","purpose":"Teach a repeatable compare routine while using fictional prices that can be replaced locally.","activity":{"type":"model","prompt":"Estimate first, then compare two fictional offers. Change one feature at a time and freeze the result.","controls":[{"id":"c1","label":"Item price","default":"low","options":[{"value":"low","label":"£1.80","quality":2,"feedback":"Lower ticket price."},{"value":"high","label":"£2.40","quality":1,"feedback":"Higher ticket price."}]},{"id":"c2","label":"Quantity","default":"small","options":[{"value":"small","label":"500 g","quality":1,"feedback":"Smaller quantity."},{"value":"large","label":"1 kg","quality":2,"feedback":"Larger quantity."}]},{"id":"c3","label":"Travel cost","default":"none","options":[{"value":"none","label":"No extra travel","quality":2,"feedback":"No additional journey cost."},{"value":"bus","label":"£2 return travel","quality":0,"feedback":"The journey changes the total cost."}]}],"outcomes":[{"min":0,"max":2,"label":"poor overall value","message":"The visible price misses quantity or another cost."},{"min":3,"max":4,"label":"needs comparison","message":"Some features help, but calculate the full cost."},{"min":5,"max":6,"label":"stronger value in this scenario","message":"Price, amount and access cost align."}],"completion":"The cheapest label is not always the lowest real cost; quantity and access can change the comparison.","predictionOptions":["The first offer will cost less overall","The second offer will cost less overall","The label price will not be enough to decide"],"requiredRuns":1},"independent":"Compare two supplied fictional products. Record estimate, exact total or unit comparison, and one reason for the final choice.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original shop-shelf comparator with ticket price, pack size and travel-cost layers.","mediaKey":"money","slug":"LI_W4_Everyday_Prices","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"34d40fffc8975d3377155ebb9ffb3cb093ca669a45f50940c5664bc505ad0029"},"LI_W5_A_Simple_Budget":{"path":"BUILD_ASDAN/Living_Independently/LI_W5_A_Simple_Budget.html","pathway":"BUILD","subsection":"Living Independently","lessonTitle":"Week 5 · A Simple Budget","targetTitle":"We Do 1","title":"Budget balance simulator","purpose":"Externalise the budget calculation and decision sequence so pupils can reproduce it on paper.","activity":{"type":"model","prompt":"Choose a fictional income, essential costs and one optional choice. Predict the balance, then run the budget.","controls":[{"id":"c1","label":"Income","default":"low","options":[{"value":"low","label":"£25 available","quality":1,"feedback":"A smaller amount requires tighter choices."},{"value":"mid","label":"£35 available","quality":2,"feedback":"More room remains after essentials."}]},{"id":"c2","label":"Essential total","default":"planned","options":[{"value":"planned","label":"£20 essentials","quality":2,"feedback":"The essential costs fit the available amount."},{"value":"high","label":"£30 essentials","quality":0,"feedback":"Essentials use most or all of the budget."}]},{"id":"c3","label":"Optional choice","default":"buy","options":[{"value":"wait","label":"Delay the optional item","quality":2,"feedback":"Protects the remaining balance."},{"value":"buy","label":"Spend £8 now","quality":0,"feedback":"May create a shortfall depending on income."}]}],"outcomes":[{"min":0,"max":2,"label":"budget shortfall risk","message":"Spending is likely to exceed or remove the safety margin."},{"min":3,"max":4,"label":"budget just balances","message":"The plan may work but has little room for change."},{"min":5,"max":6,"label":"budget has a margin","message":"Essentials are covered and money remains or is reserved."}],"completion":"A simple budget shows income, essentials, choices and what remains; delaying a choice is a valid decision.","predictionOptions":["The plan will leave money","The plan will use everything","The plan will go short"],"requiredRuns":1},"independent":"Complete the fictional budget table independently. Add one change that would repair a shortfall or protect a margin.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original balance dashboard with income tank, essential pipes, optional valve and remaining-money gauge.","mediaKey":"money","slug":"LI_W5_A_Simple_Budget","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"a8fd8f0a289c878dd2e38bd42893b5a4136333147231cfc76bbea1cc6a52dd69"},"LI_W6_Shopping_and_Change":{"path":"BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html","pathway":"BUILD","subsection":"Living Independently","lessonTitle":"Week 6 · Shopping & Change","targetTitle":"We Do 1","title":"Shop, pay, check","purpose":"Create a visible self-check routine pupils can use in a practical role-play without relying on adult prompting.","activity":{"type":"sequence","prompt":"Put the shopping-and-change check in a safe, efficient order. Explain why checking happens before leaving.","steps":[{"id":"s1","label":"Read the fictional list and set the spending limit.","reason":"The task and limit guide every later choice."},{"id":"s2","label":"Select the items and compare the displayed prices.","reason":"The basket is built from visible information."},{"id":"s3","label":"Estimate the basket total before paying.","reason":"An estimate gives an error check."},{"id":"s4","label":"Calculate or confirm the exact total.","reason":"The exact value decides the payment."},{"id":"s5","label":"Choose a suitable payment amount.","reason":"The payment must cover the total without guessing."},{"id":"s6","label":"Check receipt, items and change before leaving.","reason":"Errors are easier to resolve at the point of sale."},{"id":"s7","label":"Record the result on the lesson sheet.","reason":"The real task evidence is the completed calculation and check."}],"completion":"Independent shopping uses a planned limit, an estimate, an exact check and a final receipt/change check."},"independent":"Complete the role-play shop using the fictional price cards. Show estimate, exact total, payment and change.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original checkout sequence with list, basket, estimate, payment and receipt checkpoints.","mediaKey":"money","slug":"LI_W6_Shopping_and_Change","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"71a0cfcf840d8d627e94c1c9ab948f01c29fe7d22a43fd3fff1596d342651a14"},"FW_W1_Food_Groups":{"path":"BUILD_ASDAN/FoodWise/FW_W1_Food_Groups.html","pathway":"BUILD","subsection":"FoodWise","lessonTitle":"Week 1 · Food Groups","targetTitle":"We Do 1","title":"Build the food-group map","purpose":"Use a calm, neutral visual model that avoids weight-loss language and starts with recognisable foods.","activity":{"type":"sort","prompt":"Place each neutral food example in the Eatwell Guide group it mainly belongs to. Use the food itself, not packaging colour or whether you like it.","categories":[{"id":"fruitveg","icon":"🥕","label":"FRUIT & VEGETABLES"},{"id":"starch","icon":"🍞","label":"STARCHY CARBOHYDRATES"},{"id":"protein","icon":"🫘","label":"BEANS, PULSES, FISH, EGGS, MEAT & OTHER PROTEINS"},{"id":"dairy","icon":"🥛","label":"DAIRY & ALTERNATIVES"},{"id":"oils","icon":"🫒","label":"OILS & SPREADS"}],"items":[{"id":"i1","icon":"🥕","label":"Carrots","answer":"fruitveg","reason":"A vegetable example."},{"id":"i2","icon":"🍎","label":"Apple","answer":"fruitveg","reason":"A fruit example."},{"id":"i3","icon":"🍞","label":"Wholemeal bread","answer":"starch","reason":"Bread is a starchy carbohydrate."},{"id":"i4","icon":"🥔","label":"Potatoes","answer":"starch","reason":"Potatoes belong in the starchy group."},{"id":"i5","icon":"🫘","label":"Beans","answer":"protein","reason":"Beans and pulses are protein foods."},{"id":"i6","icon":"🥚","label":"Eggs","answer":"protein","reason":"Eggs belong in the protein group."},{"id":"i7","icon":"🥛","label":"Plain yoghurt","answer":"dairy","reason":"Yoghurt is a dairy food."},{"id":"i8","icon":"🫒","label":"Vegetable oil","answer":"oils","reason":"Oil belongs in the small oils and spreads group."}],"completion":"The groups describe the main food type; the Eatwell Guide also shows that the groups are not intended in equal proportions."},"independent":"Use the official class food cards to build one day of examples. Label each group and add one food not shown on the screen.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original five-zone plate map with food icons, labels and textures so meaning is not colour-only.","mediaKey":"food","slug":"FW_W1_Food_Groups","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"fa1847ccb043a928c7a9183c27d26412b1c83364d61b876e6179f16b926c2326"},"FW_W2_A_Balanced_Plate":{"path":"BUILD_ASDAN/FoodWise/FW_W2_A_Balanced_Plate.html","pathway":"BUILD","subsection":"FoodWise","lessonTitle":"Week 2 · A Balanced Plate","targetTitle":"We Do 1","title":"Balanced-meal plate builder","purpose":"Make meal composition visible while avoiding moral labels such as good/bad food.","activity":{"type":"model","prompt":"Change one meal component at a time. Predict whether the fictional meal becomes more balanced, then freeze the plate.","controls":[{"id":"c1","label":"Fruit/vegetable presence","default":"none","options":[{"value":"none","label":"No fruit or vegetables","quality":0,"feedback":"A major food group is absent."},{"value":"some","label":"One fruit or vegetable component","quality":2,"feedback":"Adds variety and the group is represented."}]},{"id":"c2","label":"Starchy base","default":"none","options":[{"value":"none","label":"No starchy carbohydrate","quality":0,"feedback":"The meal lacks a starchy base."},{"value":"whole","label":"Wholegrain or potato base","quality":2,"feedback":"Provides a suitable starchy component."}]},{"id":"c3","label":"Protein source","default":"none","options":[{"value":"none","label":"No protein source","quality":0,"feedback":"The meal lacks a protein component."},{"value":"source","label":"Beans, egg, fish, meat or alternative","quality":2,"feedback":"Adds a protein source."}]}],"outcomes":[{"min":0,"max":2,"label":"several groups missing","message":"Use the guide to identify the first missing group."},{"min":3,"max":4,"label":"partly balanced","message":"The meal has useful parts but one major group is still missing."},{"min":5,"max":6,"label":"more balanced meal","message":"The main components are represented; portions and individual needs still matter."}],"completion":"A balanced pattern is built across meals and days; this model checks food-group variety, not calories or a pupil’s body.","predictionOptions":["The meal will still miss major groups","The meal will be partly balanced","The meal will show the main groups"],"requiredRuns":1},"independent":"Plan a fictional meal using the class ingredient list. Annotate the group represented by each component.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original adjustable plate with labelled sections and a visible ‘not every meal must look identical’ note.","mediaKey":"food","slug":"FW_W2_A_Balanced_Plate","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"9d9b0ecd45212a1ecf7426c62c06ee963561a0b6a5383a34b00a39de8ebed8b7"},"FW_W3_Reading_Labels":{"path":"BUILD_ASDAN/FoodWise/FW_W3_Reading_Labels.html","pathway":"BUILD","subsection":"FoodWise","lessonTitle":"Week 3 · Reading Labels","targetTitle":"We Do 1","title":"Label evidence scanner","purpose":"Teach pupils to manipulate the evidence on a food label rather than merely recognise traffic-light colours.","activity":{"type":"evidence","prompt":"Select every label feature that helps compare two similar products fairly. Reject clues that can mislead.","statements":[{"id":"e1","label":"Compare the same nutrient on the same basis, such as per 100 g.","correct":true,"reason":"A common basis makes the numbers comparable."},{"id":"e2","label":"Choose the package with the healthiest-looking picture.","correct":false,"reason":"Marketing imagery is not nutrition evidence."},{"id":"e3","label":"Check the portion size used for the front-of-pack figures.","correct":true,"reason":"Different portions can change the displayed numbers."},{"id":"e4","label":"Use red, amber and green together with the printed nutrient names and values.","correct":true,"reason":"Colour is a cue, not the only information."},{"id":"e5","label":"Assume green packaging means a healthier product.","correct":false,"reason":"Package colour is not the traffic-light label."},{"id":"e6","label":"Compare salt, sugars, saturates and fat where relevant to the task.","correct":true,"reason":"These are named front-of-pack nutrients."},{"id":"e7","label":"Pick the product with the lowest single number without reading its unit.","correct":false,"reason":"The number may refer to a different nutrient or basis."},{"id":"e8","label":"Check allergens and ingredients separately when the task requires them.","correct":true,"reason":"Nutrition and allergy information have different purposes."}],"completion":"Reliable label reading compares like with like and uses words, values, units and portion information—not colour alone."},"independent":"Use two teacher-supplied mock labels. Circle the common comparison basis and record two evidence-led differences.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original paired mock food labels with magnifying lenses for basis, portion, nutrients and allergen information.","mediaKey":"food","slug":"FW_W3_Reading_Labels","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"85c9cdfa32109772c0a738e9baa29a35d535891b5255baf54d8a239c91ec4f9f"},"FW_W4_Kitchen_Hygiene_and_Safety":{"path":"BUILD_ASDAN/FoodWise/FW_W4_Kitchen_Hygiene_and_Safety.html","pathway":"BUILD","subsection":"FoodWise","lessonTitle":"Week 4 · Kitchen Hygiene & Safety","targetTitle":"We Do 1","title":"Kitchen safety chain · the 4Cs in action","purpose":"Convert several safety rules into one repeatable workflow that pupils can follow more independently.","activity":{"type":"sequence","prompt":"Order the safe preparation routine. Link each step to cleaning, cooking, chilling or avoiding cross-contamination.","steps":[{"id":"s1","label":"Check the local recipe, allergies and equipment before starting.","reason":"The task must be suitable before food is handled."},{"id":"s2","label":"Wash hands and prepare a clean work area.","reason":"Cleaning happens before contact with food."},{"id":"s3","label":"Separate raw and ready-to-eat foods, boards and utensils.","reason":"Separation controls cross-contamination."},{"id":"s4","label":"Prepare food using the taught safe tool routine.","reason":"The local demonstration governs tool use."},{"id":"s5","label":"Cook or assemble exactly as the recipe and teacher instruction require.","reason":"Time, temperature and method are followed rather than guessed."},{"id":"s6","label":"Keep chilled ingredients chilled and return them promptly.","reason":"Temperature control continues during preparation."},{"id":"s7","label":"Clean, store and dispose of items using the agreed routine.","reason":"The task ends with a safe workspace, not at the first taste."}],"completion":"Safe food preparation is a chain: check, clean, separate, follow the taught method, control temperature and close down."},"independent":"Use the physical bench card during the practical. Tick each stage only when it is actually complete; do not photograph personal allergy information.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original kitchen workflow with four labelled safety shields and a start-to-close-down route.","mediaKey":"food","slug":"FW_W4_Kitchen_Hygiene_and_Safety","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"75efeab482c2317e095dd26d0e38839e5a278f555e7c19ea0f7391feb1f64dfc"},"FW_W5_Prepare_a_Healthy_Snack":{"path":"BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html","pathway":"BUILD","subsection":"FoodWise","lessonTitle":"Week 5 · Prepare a Healthy Snack","targetTitle":"We Do 1","title":"Visual recipe rehearsal","purpose":"Reduce memory load before the practical and make adult-check points explicit rather than hidden.","activity":{"type":"sequence","prompt":"Build the preparation sequence for the supplied snack. Explain which steps need an adult check in your room.","steps":[{"id":"s1","label":"Read the visual recipe and identify the finished product.","reason":"Knowing the endpoint makes later checks meaningful."},{"id":"s2","label":"Check ingredients, allergies, equipment and the local permission route.","reason":"The recipe is adapted or stopped before preparation if needed."},{"id":"s3","label":"Wash hands and prepare the workspace.","reason":"The practical starts with hygiene."},{"id":"s4","label":"Collect and measure only the required ingredients.","reason":"This reduces clutter and waste."},{"id":"s5","label":"Follow the demonstrated preparation steps in order.","reason":"The screen rehearses; the teacher’s live method is authoritative."},{"id":"s6","label":"Present and check the snack against the brief.","reason":"The result is compared with the intended product."},{"id":"s7","label":"Clean down and record authorised evidence of the task.","reason":"Evidence follows the centre’s process and never includes sensitive personal information."}],"completion":"Independent practical work is safe when pupils can see the endpoint, follow a finite sequence and recognise where an adult check remains essential."},"independent":"Complete the real snack task using the printed visual recipe. Use the self-check: safe / in order / balanced / cleaned down.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original seven-frame visual recipe strip using generic ingredients and explicit adult-check symbols.","mediaKey":"food","slug":"FW_W5_Prepare_a_Healthy_Snack","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"b5eb7314a43c34b68838ea117874fbfc5492d766882994f1ca3375d3c0e5fb51"},"FW_W6_Plan_a_Healthy_Meal":{"path":"BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html","pathway":"BUILD","subsection":"FoodWise","lessonTitle":"Week 6 · Plan a Healthy Meal","targetTitle":"We Do 1","title":"Meal-plan dependency check","purpose":"Bring nutrition and independent-living decisions together in one visible planning system.","activity":{"type":"model","prompt":"Choose a meal purpose, food-group coverage and practical constraint. Predict whether the plan is usable, then run the check.","controls":[{"id":"c1","label":"Meal purpose","default":"unclear","options":[{"value":"unclear","label":"No named user or occasion","quality":0,"feedback":"The plan has no clear context."},{"value":"named","label":"Named fictional user and occasion","quality":2,"feedback":"The context guides choices."}]},{"id":"c2","label":"Food-group coverage","default":"narrow","options":[{"value":"narrow","label":"One main food group","quality":0,"feedback":"The plan lacks variety."},{"value":"varied","label":"Several relevant groups","quality":2,"feedback":"The plan shows a balanced pattern."}]},{"id":"c3","label":"Practical fit","default":"unreal","options":[{"value":"unreal","label":"Ignores time, equipment or budget","quality":0,"feedback":"The plan may not be deliverable."},{"value":"fit","label":"Fits the supplied time, equipment and fictional budget","quality":2,"feedback":"The plan can be acted on."}]}],"outcomes":[{"min":0,"max":2,"label":"idea only","message":"The meal cannot yet be followed or justified."},{"min":3,"max":4,"label":"partly workable plan","message":"One link between purpose, balance and practical fit is weak."},{"min":5,"max":6,"label":"workable meal plan","message":"Purpose, food-group variety and practical constraints connect."}],"completion":"A useful meal plan is balanced for its context and possible with the time, equipment, ingredients and fictional budget available.","predictionOptions":["The plan will be an idea only","The plan will be partly workable","The plan will be ready to use"],"requiredRuns":1},"independent":"Complete the meal-plan sheet with ingredients, food groups, steps, equipment, fictional cost and one adaptation.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original meal-planning canvas linking user, plate, equipment clock and budget card.","mediaKey":"food","slug":"FW_W6_Plan_a_Healthy_Meal","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"a09c68a2ba0cec5413e1df4274cc4781ba4351530f20d09d1e6248975f653471"},"COMM_W1_Choose_Our_Asset":{"path":"BUILD_ASDAN/Community_Project/COMM_W1_Choose_Our_Asset.html","pathway":"BUILD","subsection":"Community Project","lessonTitle":"Week 1 · Choose Our Asset","targetTitle":"We Do 1","title":"Community asset decision map","purpose":"Place the user and site before the object, preventing a making project from becoming detached from community benefit.","activity":{"type":"hotspot","scene":"community","prompt":"Open every part of the community-use scene. For each option, name who would use it, what it must do and one question still needing a real answer.","hotspots":[{"id":"h1","x":18,"y":24,"label":"PLANTER · users and maintenance","note":"A planter needs a location, a person who will maintain it and an accessible height."},{"id":"h2","x":50,"y":18,"label":"WILDLIFE BOX · species and site","note":"The intended wildlife, mounting position and safe maintenance must be checked."},{"id":"h3","x":82,"y":27,"label":"SEATING / REST POINT · access","note":"A rest asset needs suitable dimensions, route access and permission."},{"id":"h4","x":23,"y":66,"label":"SIGN / INFORMATION · audience","note":"The message, reading level, weather resistance and site approval matter."},{"id":"h5","x":52,"y":72,"label":"STORAGE / TOOL ASSET · security","note":"The user, contents, safe access and secure location must be known."},{"id":"h6","x":82,"y":65,"label":"DISPLAY FEATURE · purpose","note":"A display needs a real audience and a plan for what happens after installation."}],"completion":"A community asset is chosen through user, purpose, site, permission and maintenance—not just which object looks most exciting."},"independent":"Choose one asset option from the class shortlist. Complete: user / need / site / question / who must confirm it.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original community-space map with six possible assets and linked user, access, permission and upkeep hotspots.","mediaKey":"community","slug":"COMM_W1_Choose_Our_Asset","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"1caaa36dbe1d10a28a9522bc4079cfcaaa9cf663d31c8b8257283fd3076f3ff6"},"COMM_W2_The_Site's_Need":{"path":"BUILD_ASDAN/Community_Project/COMM_W2_The_Site's_Need.html","pathway":"BUILD","subsection":"Community Project","lessonTitle":"Week 2 · The Site’s Need","targetTitle":"We Do 1","title":"Need evidence or assumption?","purpose":"Teach pupils to test whether information genuinely supports the project instead of collecting decorative evidence.","activity":{"type":"evidence","prompt":"Select the evidence that could justify a site need. Reject assumptions, invented feedback and details that do not answer the need.","statements":[{"id":"e1","label":"A dated site observation shows there is no sheltered place for the intended activity.","correct":true,"reason":"It is direct, relevant evidence."},{"id":"e2","label":"We think people will probably love it.","correct":false,"reason":"This is an assumption, not evidence."},{"id":"e3","label":"The named partner confirms the route must remain clear for wheelchair access.","correct":true,"reason":"It is relevant partner information and a design constraint."},{"id":"e4","label":"A pupil says the colour is cool.","correct":false,"reason":"Preference alone does not establish a community need."},{"id":"e5","label":"A counted observation shows the existing storage is full during the agreed period.","correct":true,"reason":"The count directly relates to capacity."},{"id":"e6","label":"A made-up quote from a visitor supports our idea.","correct":false,"reason":"Invented audiences or responses cannot be evidence."},{"id":"e7","label":"A photograph of the empty area is useful only when its date, viewpoint and purpose are explained.","correct":true,"reason":"Context makes the image interpretable."},{"id":"e8","label":"The design is easy for us to make.","correct":false,"reason":"Build convenience does not prove site need."}],"completion":"Site-need evidence is authentic, relevant and traceable to observation, consultation or an authorised source."},"independent":"Use the supplied site information. Write one need claim and attach two real evidence sources plus one remaining question.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original evidence funnel from site, partner and user observations into a clearly bounded need statement.","mediaKey":"community","slug":"COMM_W2_The_Site's_Need","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"01a3562ef6b8a3cc36fe5dd664ffe0b996a5a45152636621d30ad9f4b5761d69"},"COMM_W3_Our_Team_Roles":{"path":"BUILD_ASDAN/Community_Project/COMM_W3_Our_Team_Roles.html","pathway":"BUILD","subsection":"Community Project","lessonTitle":"Week 3 · Our Team Roles","targetTitle":"We Do 1","title":"Role ownership and handover board","purpose":"Reduce confusion and dependence by making role boundaries, communication points and handovers visible.","activity":{"type":"sort","prompt":"Match each responsibility to the role that owns it. Then identify where two roles must communicate rather than duplicate one another.","categories":[{"id":"maker","icon":"🛠","label":"MAKER / BUILD"},{"id":"document","icon":"📷","label":"DOCUMENTARIAN"},{"id":"liaison","icon":"💬","label":"PARTNER LIAISON"},{"id":"check","icon":"✅","label":"QUALITY & SAFETY CHECK"}],"items":[{"id":"i1","icon":"🛠","label":"Complete the agreed practical step using the taught method.","answer":"maker","reason":"The role owns the making action."},{"id":"i2","icon":"📷","label":"Capture authorised evidence of the work, not faces or personal information.","answer":"document","reason":"The role documents the task within the centre’s rules."},{"id":"i3","icon":"💬","label":"Prepare and send the agreed update through the authorised adult route.","answer":"liaison","reason":"The role communicates with the real partner."},{"id":"i4","icon":"✅","label":"Compare the result with the blueprint and safety checklist.","answer":"check","reason":"The role tests quality and safety."},{"id":"i5","icon":"🛠","label":"Report a material problem before changing the design.","answer":"maker","reason":"The maker identifies the practical issue but does not silently redesign."},{"id":"i6","icon":"✅","label":"Record the exact check that did not pass.","answer":"check","reason":"The checker makes the gap visible."},{"id":"i7","icon":"💬","label":"Confirm what information the partner actually needs next.","answer":"liaison","reason":"The communication has a real purpose."},{"id":"i8","icon":"📷","label":"Label what the image shows and when it was made.","answer":"document","reason":"Context turns an image into usable authorised evidence."}],"completion":"Clear roles separate ownership while keeping handovers visible; teamwork is not everyone doing everything."},"independent":"Complete your role card: my action / what I need / who I hand to / how I know it is complete.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original four-role project board with handover arrows and non-overlapping responsibility zones.","mediaKey":"community","slug":"COMM_W3_Our_Team_Roles","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"09dabe874de6dfbbfa832a91a24a549eb308807e8ceecb679b7e9e58b5556753"},"COMM_W4_Partner_Update":{"path":"BUILD_ASDAN/Community_Project/COMM_W4_Partner_Update.html","pathway":"BUILD","subsection":"Community Project","lessonTitle":"Week 4 · Partner Update","targetTitle":"We Do 1","title":"Partner update message pathway","purpose":"Make external communication a visible workflow and protect pupils from treating screen rehearsal as permission to contact externally.","activity":{"type":"sequence","prompt":"Order the update so a real partner can understand the project and respond. Identify where the authorised adult route is used.","steps":[{"id":"s1","label":"Confirm the purpose of the update and the approved recipient.","reason":"The message starts with a real need and correct route."},{"id":"s2","label":"State what has been completed using specific evidence.","reason":"The partner can see progress without exaggerated claims."},{"id":"s3","label":"Explain one decision or change and why it happened.","reason":"The update shows responsive project work."},{"id":"s4","label":"Name one question or decision needed from the partner.","reason":"The partner knows what response would move the project forward."},{"id":"s5","label":"Check privacy, accuracy, tone and attachments with the authorised adult.","reason":"External communication is reviewed before sending."},{"id":"s6","label":"Send through the centre’s approved route.","reason":"Pupils rehearse communication; the authorised process governs release."},{"id":"s7","label":"Record the response accurately when it arrives.","reason":"A real response is not invented or paraphrased into a stronger claim."}],"completion":"A useful partner update is accurate, purposeful, checked and routed through the centre’s authorised process."},"independent":"Draft the update on the lesson template. Highlight progress, decision, question and adult-check point in different patterns.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original message pathway from project evidence through adult check to partner response, with privacy shields.","mediaKey":"community","slug":"COMM_W4_Partner_Update","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"034f3dccbb175ae717758a0dfb5729606033dc8e76d7041b13653fdfd384e2e7"},"COMM_W5_Plan_the_Handover":{"path":"BUILD_ASDAN/Community_Project/COMM_W5_Plan_the_Handover.html","pathway":"BUILD","subsection":"Community Project","lessonTitle":"Week 5 · Plan the Handover","targetTitle":"We Do 1","title":"Handover dependency canvas","purpose":"Show hidden dependencies so pupils can independently check the plan before the real event.","activity":{"type":"model","prompt":"Build a handover plan. Predict whether the recipient could receive, use and maintain the asset, then run the dependency check.","controls":[{"id":"c1","label":"Recipient readiness","default":"unknown","options":[{"value":"unknown","label":"Recipient/time not confirmed","quality":0,"feedback":"The handover may have no real receiver."},{"value":"confirmed","label":"Recipient and time confirmed","quality":2,"feedback":"A real person and occasion exist."}]},{"id":"c2","label":"Access and installation","default":"missing","options":[{"value":"missing","label":"Access or installation unresolved","quality":0,"feedback":"The asset may not reach or fit the site."},{"value":"checked","label":"Route, location and installation checked","quality":2,"feedback":"The physical handover is feasible."}]},{"id":"c3","label":"Aftercare","default":"none","options":[{"value":"none","label":"No maintenance or report-back owner","quality":0,"feedback":"Benefit may stop after delivery."},{"value":"owner","label":"Named maintenance and report-back owner","quality":2,"feedback":"Responsibility continues after handover."}]}],"outcomes":[{"min":0,"max":2,"label":"ceremony without a handover","message":"The project may be presented but not successfully transferred."},{"min":3,"max":4,"label":"handover partly ready","message":"One practical or aftercare dependency remains."},{"min":5,"max":6,"label":"handover ready for confirmation","message":"Recipient, access and aftercare connect; local approval still governs delivery."}],"completion":"A handover transfers an asset, information and future responsibility to a real recipient; it is more than taking a photograph.","predictionOptions":["The handover will fail at the site","The handover will be partly ready","The recipient will be able to receive and use it"],"requiredRuns":1},"independent":"Complete the handover plan: recipient / item / route / installation / explanation / maintenance / report-back.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original handover canvas linking asset, recipient, route, installation and maintenance owner.","mediaKey":"community","slug":"COMM_W5_Plan_the_Handover","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"d7daa64838233f31f515b2035d482f9ae098d177b86979ec3ca0e07f895a4fce"},"COMM_W6_The_Handover_and_Its_Benefit":{"path":"BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html","pathway":"BUILD","subsection":"Community Project","lessonTitle":"Week 6 · The Handover & Its Benefit","targetTitle":"We Do 1","title":"Benefit claim evidence audit","purpose":"Separate completion, receipt and longer-term impact so pupils learn honest evaluation rather than inflated claims.","activity":{"type":"evidence","prompt":"Select the evidence that could support a careful claim about community benefit. Reject celebration images or invented impact.","statements":[{"id":"e1","label":"The recipient confirms the asset was received and describes its intended use.","correct":true,"reason":"This is a real receipt and purpose statement, not proof of long-term impact."},{"id":"e2","label":"A group photograph proves the project improved the whole community.","correct":false,"reason":"A photograph of people at an event cannot prove broad impact."},{"id":"e3","label":"A before-and-after site check shows the agreed asset is installed in the approved place.","correct":true,"reason":"It evidences delivery against the plan."},{"id":"e4","label":"We know everyone is happier now.","correct":false,"reason":"The claim is unmeasured and over-broad."},{"id":"e5","label":"A later report-back records one observed use or one maintenance issue.","correct":true,"reason":"A dated follow-up can support a limited claim."},{"id":"e6","label":"The project was brilliant because we worked hard.","correct":false,"reason":"Effort matters but does not establish recipient benefit."},{"id":"e7","label":"The partner identifies one specific useful feature and one next action.","correct":true,"reason":"The response is specific and can guide improvement."},{"id":"e8","label":"No response was received, so we wrote what they probably thought.","correct":false,"reason":"An absent response must remain absent."}],"completion":"Benefit claims stay proportionate to authentic evidence: delivery can be proven immediately; wider or lasting impact needs later report-back."},"independent":"Complete the impact record using only evidence that exists. Use ‘not yet known’ for any effect that needs later checking.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original three-stage evidence timeline: delivered, received, later use/report-back, with claim-size limits.","mediaKey":"community","slug":"COMM_W6_The_Handover_and_Its_Benefit","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"8a0931192d4812aaddeb0faef16482319985e87729ee1737c73f00e36b02b07b"},"DUKE_W1_Choose_My_Challenges":{"path":"BUILD_ASDAN/Duke_and_Enterprise/DUKE_W1_Choose_My_Challenges.html","pathway":"BUILD","subsection":"Duke & Enterprise","lessonTitle":"Week 1 · Choose My Challenges","targetTitle":"We Do 1","title":"Choose a challenge that can succeed","purpose":"Prevent challenge choice from becoming a popularity vote and give pupils a visible way to judge fit.","activity":{"type":"model","prompt":"Choose the size, support and proof route for a personal challenge. Predict whether it is achievable and still meaningful.","controls":[{"id":"c1","label":"Challenge size","default":"tiny","options":[{"value":"tiny","label":"Already easy and completed often","quality":0,"feedback":"It may not create meaningful learning."},{"value":"fit","label":"New but possible within the time","quality":2,"feedback":"It offers stretch with a realistic route."},{"value":"huge","label":"Depends on many unconfirmed events","quality":0,"feedback":"It may be too large for the module."}]},{"id":"c2","label":"Support plan","default":"none","options":[{"value":"none","label":"No support identified","quality":0,"feedback":"A predictable barrier has no route."},{"value":"specific","label":"One named prompt, model or adult check","quality":2,"feedback":"Support is clear and can fade where appropriate."}]},{"id":"c3","label":"Evidence route","default":"vague","options":[{"value":"vague","label":"I will remember it","quality":0,"feedback":"The achievement may not be verifiable."},{"value":"real","label":"Product/action + short reflection or witness route","quality":2,"feedback":"The task and learning can be evidenced honestly."}]}],"outcomes":[{"min":0,"max":2,"label":"challenge needs redesign","message":"It is too easy, too large or impossible to evidence."},{"min":3,"max":4,"label":"challenge nearly usable","message":"One condition needs tightening."},{"min":5,"max":6,"label":"well-sized challenge","message":"Stretch, support and proof route align."}],"completion":"A useful personal challenge is genuinely new, achievable in context and linked to authentic evidence.","predictionOptions":["The challenge will be too easy","The challenge will be too large","The challenge will be a productive stretch"],"requiredRuns":1},"independent":"Complete your challenge card: what / why new / first step / support / evidence / check date.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original challenge-scope mountain with easy floor, productive route and over-large summit.","mediaKey":"challenge","slug":"DUKE_W1_Choose_My_Challenges","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"9b1f034f6c545f3dc7958113af812fe44f235a450f2738720cb5ce9f59857b77"},"DUKE_W2_A_Kindness_Challenge":{"path":"BUILD_ASDAN/Duke_and_Enterprise/DUKE_W2_A_Kindness_Challenge.html","pathway":"BUILD","subsection":"Duke & Enterprise","lessonTitle":"Week 2 · A Kindness Challenge","targetTitle":"We Do 1","title":"Kindness action · intention to impact","purpose":"Move beyond slogans by showing the decisions that make an action safe and genuinely useful.","activity":{"type":"hotspot","scene":"community","prompt":"Open each part of the kindness-action map. Decide whether the action is respectful, wanted, specific and possible to confirm.","hotspots":[{"id":"h1","x":18,"y":24,"label":"ASK, DO NOT ASSUME","note":"A kind action begins by checking what would actually help."},{"id":"h2","x":50,"y":18,"label":"KEEP DIGNITY","note":"The action should not display, embarrass or identify another person."},{"id":"h3","x":82,"y":27,"label":"MAKE IT SPECIFIC","note":"‘Help more’ becomes an observable action such as preparing or explaining one item."},{"id":"h4","x":23,"y":66,"label":"USE THE APPROVED ROUTE","note":"Contact, gifts, photographs and public messages follow centre rules."},{"id":"h5","x":52,"y":72,"label":"NOTICE THE RESPONSE","note":"The recipient’s real response may show usefulness or a need to change."},{"id":"h6","x":82,"y":65,"label":"REFLECT WITHOUT CLAIMING CREDIT","note":"The reflection focuses on action, effect and learning rather than presenting another person as evidence."}],"completion":"Kindness is relational: the intended recipient, consent, dignity and actual usefulness matter as much as intention."},"independent":"Plan one approved kindness action. Include recipient need, consent/check, action, boundary and how you will know it was useful.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original kindness pathway with consent gate, dignity shield, action and response loop.","mediaKey":"challenge","slug":"DUKE_W2_A_Kindness_Challenge","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"dc8cee10ccee45b688cbe30fd6475a7a5cab2741b839db31f00b2c02635cb5ea"},"DUKE_W3_An_Eco_Challenge":{"path":"BUILD_ASDAN/Duke_and_Enterprise/DUKE_W3_An_Eco_Challenge.html","pathway":"BUILD","subsection":"Duke & Enterprise","lessonTitle":"Week 3 · An Eco Challenge","targetTitle":"We Do 1","title":"Eco action · evidence not slogan","purpose":"Teach pupils to connect action to a proportionate measure and to treat a mixed result as information, not failure.","activity":{"type":"evidence","prompt":"Select the statements that could show a small environmental action happened and made a measurable difference. Reject vague or exaggerated claims.","statements":[{"id":"e1","label":"The class weighed one bag of avoidable paper waste before and after the change.","correct":true,"reason":"The same measure allows comparison."},{"id":"e2","label":"We saved the planet today.","correct":false,"reason":"The claim is far larger than the evidence."},{"id":"e3","label":"A dated tally shows reusable bottles increased during the agreed week.","correct":true,"reason":"A bounded count can show local change."},{"id":"e4","label":"The poster looked green, so it must have worked.","correct":false,"reason":"Appearance is not impact evidence."},{"id":"e5","label":"The action had a named place, duration and person responsible.","correct":true,"reason":"Scope and ownership make the action testable."},{"id":"e6","label":"Everyone promised they will always recycle.","correct":false,"reason":"A promise is not completed action or measured outcome."},{"id":"e7","label":"The result was mixed, so the group recorded what did not change.","correct":true,"reason":"Honest non-change is useful evidence."},{"id":"e8","label":"The class copied a national statistic but did not connect it to the local action.","correct":false,"reason":"Context information does not prove local impact."}],"completion":"Eco evidence uses the same bounded measure before and after and keeps the claim local to what was actually observed."},"independent":"Complete the eco challenge using the agreed local measure. Record before, action, after and one next adjustment.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original local eco-impact meter with before/action/after frames and a claim-size boundary.","mediaKey":"challenge","slug":"DUKE_W3_An_Eco_Challenge","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"f4848c4012c239895946b7c8902ce03091a91277d9742d1d4c3dc96dbba46024"},"DUKE_W4_An_Independence_Challenge":{"path":"BUILD_ASDAN/Duke_and_Enterprise/DUKE_W4_An_Independence_Challenge.html","pathway":"BUILD","subsection":"Duke & Enterprise","lessonTitle":"Week 4 · An Independence Challenge","targetTitle":"We Do 1","title":"From model to independent action","purpose":"Make gradual release and prompt-fading visible to pupils without turning support into shame.","activity":{"type":"sequence","prompt":"Order the challenge so support helps the pupil start but does not take over the task.","steps":[{"id":"s1","label":"Choose one real task and define what finished looks like.","reason":"A visible endpoint reduces uncertainty."},{"id":"s2","label":"Watch or read the short model and name the first step.","reason":"The pupil rehearses the route before acting."},{"id":"s3","label":"Set out the required items in the order they will be used.","reason":"The environment becomes part of the scaffold."},{"id":"s4","label":"Complete the task using the least prompt needed.","reason":"Responsibility stays with the pupil."},{"id":"s5","label":"Pause at the agreed safety or quality checkpoint.","reason":"Some checks appropriately remain with an adult."},{"id":"s6","label":"Use the finished checklist before asking for help.","reason":"Self-check comes before general rescue."},{"id":"s7","label":"Reflect on which support can be reduced next time.","reason":"The challenge builds future independence, not permanent dependence."}],"completion":"Independence means owning the action and check; it does not mean removing necessary safety, access or reasonable adjustment."},"independent":"Complete the chosen real task. Record: what I did alone / prompt used / adult check / what I can try with less help next time.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original scaffold bridge moving from model to self-check while a safety rail remains.","mediaKey":"challenge","slug":"DUKE_W4_An_Independence_Challenge","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"f63b3209b7af5423469a0eb99573c49e9eeda4fd84aba28810d89ac141cd309b"},"DUKE_W5_Our_Social_Enterprise":{"path":"BUILD_ASDAN/Duke_and_Enterprise/DUKE_W5_Our_Social_Enterprise.html","pathway":"BUILD","subsection":"Duke & Enterprise","lessonTitle":"Week 5 · Our Social Enterprise","targetTitle":"We Do 1","title":"Need → offer → money → benefit","purpose":"Create a shared decision canvas that keeps social benefit and basic enterprise thinking together.","activity":{"type":"model","prompt":"Build a small enterprise idea that helps a real audience and can operate safely. Predict whether it is only a product idea or a usable plan.","controls":[{"id":"c1","label":"Need","default":"assumed","options":[{"value":"assumed","label":"We assume people want it","quality":0,"feedback":"No authentic need has been established."},{"value":"checked","label":"A bounded need is supported by real consultation or observation","quality":2,"feedback":"The idea starts from evidence."}]},{"id":"c2","label":"Offer","default":"unclear","options":[{"value":"unclear","label":"A general nice idea","quality":0,"feedback":"The action or product is not defined."},{"value":"specific","label":"A specific product or service","quality":2,"feedback":"The group can plan materials, roles and message."}]},{"id":"c3","label":"Money and benefit","default":"missing","options":[{"value":"missing","label":"No cost, price or benefit route","quality":0,"feedback":"The enterprise cannot judge viability or social purpose."},{"value":"visible","label":"Simple fictional cost/price plus named benefit","quality":2,"feedback":"The financial and social sides are explicit."}]}],"outcomes":[{"min":0,"max":2,"label":"idea only","message":"The group cannot yet explain who it helps or how it works."},{"min":3,"max":4,"label":"promising concept","message":"One connection between need, offer and resources is missing."},{"min":5,"max":6,"label":"small workable enterprise plan","message":"Need, offer, basic money and social benefit align."}],"completion":"A social enterprise connects a checked need, a defined offer, workable resources and a clear community benefit.","predictionOptions":["It will be only a product idea","It will have some workable parts","It will be a small usable plan"],"requiredRuns":1},"independent":"Complete the one-page enterprise canvas: user need / offer / resources / fictional cost / price or exchange / benefit / next test.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original social-enterprise loop linking user need, offer, simple money and community benefit.","mediaKey":"enterprise","slug":"DUKE_W5_Our_Social_Enterprise","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"e0a4db0901c321966e46d111e6c5817396be4d58b24b21b2fef7a93e43b5dc6d"},"DUKE_W6_Pitch_and_Reflect":{"path":"BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html","pathway":"BUILD","subsection":"Duke & Enterprise","lessonTitle":"Week 6 · Pitch & Reflect","targetTitle":"We Do 1","title":"Pitch evidence selector","purpose":"Help pupils plan a concise pitch and self-check content before focusing on performance.","activity":{"type":"evidence","prompt":"Select everything a short, truthful pitch needs. Reject exaggeration, invented results and presentation features that replace substance.","statements":[{"id":"e1","label":"A clear sentence naming the need and intended user.","correct":true,"reason":"The audience understands the problem."},{"id":"e2","label":"A demonstration or visual of the proposed offer.","correct":true,"reason":"The idea becomes concrete."},{"id":"e3","label":"A claim that everybody will buy it.","correct":false,"reason":"The claim is untested and exaggerated."},{"id":"e4","label":"A simple explanation of cost, price or required resources.","correct":true,"reason":"The practical basis is visible."},{"id":"e5","label":"A specific social benefit stated at the right scale.","correct":true,"reason":"The purpose is clear without overclaiming."},{"id":"e6","label":"An invented quote from a customer.","correct":false,"reason":"Only real consultation or feedback can be used."},{"id":"e7","label":"One question the team still needs to test.","correct":true,"reason":"Uncertainty is honest and guides the next step."},{"id":"e8","label":"Lots of animation and sound but no explanation of the idea.","correct":false,"reason":"Presentation effects cannot replace evidence."}],"completion":"A strong pitch makes the need, offer, practical route, benefit and remaining question easy to follow."},"independent":"Deliver the real pitch using the lesson structure. Afterwards record one feedback point, one decision and one next action in your own words.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original five-panel pitch storyboard ending in authentic feedback and one next action.","mediaKey":"enterprise","slug":"DUKE_W6_Pitch_and_Reflect","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"fc9ad1fd09e52b36fb51e01f2c2f955d4c765d9b50b51782af80cbf06a834e99"},"BUILD_DT_W1_Workshop_Audit":{"path":"Build/Slideshows/BUILD_DT_W1_Workshop_Audit.html","pathway":"BUILD","subsection":"D&T Community Upcycling","lessonTitle":"Week 1 · The Workshop Audit","targetTitle":"We Do 1","title":"Workshop safety hotspot audit","purpose":"Turn safety from a poster into a visual scan-and-report routine while keeping teacher instruction and local controls load-bearing.","activity":{"type":"hotspot","scene":"workshop","prompt":"Open each workshop hotspot. Name the hazard or control, then point to the physical feature that made you notice it. The local risk assessment remains authoritative.","hotspots":[{"id":"h1","x":18,"y":24,"label":"CLEAR WALKWAY","note":"Offcuts and bags create trip hazards and block movement routes."},{"id":"h2","x":50,"y":18,"label":"CLAMPING ZONE","note":"Work must be secured using the demonstrated method before cutting or drilling."},{"id":"h3","x":82,"y":27,"label":"TOOL HOME","note":"Tools need a visible safe storage position so missing or damaged items are noticed."},{"id":"h4","x":23,"y":66,"label":"DUST CONTROL","note":"Extraction, suitable cleaning and local protective measures control wood dust; never improvise."},{"id":"h5","x":52,"y":72,"label":"PPE / ACCESS CHECK","note":"Required protection and reasonable adjustments are confirmed for the actual task."},{"id":"h6","x":82,"y":65,"label":"STOP / REPORT ROUTE","note":"A pupil stops and tells the responsible adult when a guard, tool, material or condition is wrong."}],"completion":"A workshop audit links a visible condition to a control and a named reporting route; spotting is not permission to fix unfamiliar equipment."},"independent":"Complete the real workshop audit with the teacher. Record one safe condition, one issue reported and the agreed action owner.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original classroom workshop plan with walkway, bench, tool storage, dust control and stop/report hotspots.","mediaKey":"workshop","slug":"BUILD_DT_W1_Workshop_Audit","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"321c063244ac710ded8b4d02a7e617cde31d211d288d6ad96e0e438713c321fa"},"BUILD_DT_W2_Blueprint":{"path":"Build/Slideshows/BUILD_DT_W2_Blueprint.html","pathway":"BUILD","subsection":"D&T Community Upcycling","lessonTitle":"Week 2 · The Blueprint","targetTitle":"We Do 1","title":"Blueprint-to-material accuracy model","purpose":"Visualise the hidden geometry and checking routine before pupils handle reclaimed material.","activity":{"type":"model","prompt":"Choose a measuring reference, marking method and check. Predict whether the cut line will match the blueprint, then run the accuracy check.","controls":[{"id":"c1","label":"Reference edge","default":"rough","options":[{"value":"rough","label":"Measure from an unchecked rough edge","quality":0,"feedback":"The starting point may not be straight or stable."},{"value":"datum","label":"Use the agreed straight datum edge","quality":2,"feedback":"Every measurement begins from the same reference."}]},{"id":"c2","label":"Marking","default":"dot","options":[{"value":"dot","label":"Single approximate dot","quality":0,"feedback":"The cutting line is unclear."},{"value":"square","label":"Measured marks joined with the demonstrated square","quality":2,"feedback":"The line is visible and square to the datum."}]},{"id":"c3","label":"Check","default":"none","options":[{"value":"none","label":"Cut immediately","quality":0,"feedback":"An error becomes material waste."},{"value":"second","label":"Second measurement and teacher/tool-unlock check","quality":2,"feedback":"The dimension and method are confirmed before action."}]}],"outcomes":[{"min":0,"max":2,"label":"high error risk","message":"The line does not yet have a trustworthy reference or check."},{"min":3,"max":4,"label":"partly controlled","message":"One accuracy control is missing."},{"min":5,"max":6,"label":"ready for local tool check","message":"Datum, marking and recheck align; the teacher still authorises tool use."}],"completion":"Accurate marking uses one stable reference, a clear line and a check before material is cut.","predictionOptions":["The marked part will be unreliable","The line will be partly controlled","The line will be ready for the teacher’s tool check"],"requiredRuns":1},"independent":"Mark the supplied practice piece from the blueprint. Label datum, measurement, line and second check before asking for tool authorisation.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original datum-and-square blueprint model with dimension arrows, error ghost and second-check overlay.","mediaKey":"workshop","slug":"BUILD_DT_W2_Blueprint","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"8310e5e414eadb8936b5c94b69c0eeba5735402f7dbdb266c8a32b3691e1d937"},"BUILD_DT_W3_Core_Cut":{"path":"Build/Slideshows/BUILD_DT_W3_Core_Cut.html","pathway":"BUILD","subsection":"D&T Community Upcycling","lessonTitle":"Week 3 · The Core Cut","targetTitle":"We Do 1","title":"Core-cut safety sequence","purpose":"Reduce dependence on repeated verbal reminders while making the non-negotiable stop route unmistakable.","activity":{"type":"sequence","prompt":"Order the teacher-approved hand-tool routine. Identify every point where the pupil must stop rather than continue through a problem.","steps":[{"id":"s1","label":"Read the cut plan and inspect the material for the agreed safe condition.","reason":"Reclaimed material can contain defects or contamination that require adult judgement."},{"id":"s2","label":"Set the work in the demonstrated orientation and clamping position.","reason":"The material must be stable before force is applied."},{"id":"s3","label":"Ask for the local tool-unlock or competence check.","reason":"Screen rehearsal never authorises use."},{"id":"s4","label":"Start the cut using the modelled body, hand and tool position.","reason":"The teacher’s live demonstration governs the technique."},{"id":"s5","label":"Maintain the marked route without forcing the tool.","reason":"A change in resistance, movement or condition triggers a stop."},{"id":"s6","label":"Stop, make the tool safe and report any slip, damage or unexpected feature.","reason":"Continuing through a fault increases risk and waste."},{"id":"s7","label":"Check the cut against the blueprint before the next operation.","reason":"The completed part becomes evidence for the following decision."}],"completion":"Safe cutting is a stop-capable sequence: inspect, secure, authorise, use the taught method, stop on change and check the result."},"independent":"Complete the supervised cut using the physical bench card. Record the check result and any authorised adaptation, not a claim of independent competence.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original clamped-work sequence with tool-unlock gate, cut path, stop signal and blueprint check.","mediaKey":"workshop","slug":"BUILD_DT_W3_Core_Cut","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"fc25a063ff8b1065d7646ed9e811c6772bb2c18fd3c0f9bc4da6c6ef573d36b6"},"BUILD_DT_W4_Assembly":{"path":"Build/Slideshows/BUILD_DT_W4_Assembly.html","pathway":"BUILD","subsection":"D&T Community Upcycling","lessonTitle":"Week 4 · The Assembly","targetTitle":"We Do 1","title":"Assembly joint control model","purpose":"Make three interacting quality decisions visible before pupils perform a supervised assembly.","activity":{"type":"model","prompt":"Choose joint alignment, pilot preparation and screw finish. Predict whether the assembly will be strong, square and safe to handle.","controls":[{"id":"c1","label":"Alignment","default":"free","options":[{"value":"free","label":"Parts held by eye only","quality":0,"feedback":"The joint may move or finish out of square."},{"value":"jig","label":"Clamped or supported to the demonstrated square reference","quality":2,"feedback":"Position is controlled during assembly."}]},{"id":"c2","label":"Pilot preparation","default":"none","options":[{"value":"none","label":"No pilot where the plan requires one","quality":0,"feedback":"The timber may split or the fixing may wander."},{"value":"pilot","label":"Pilot prepared to the teacher-approved method","quality":2,"feedback":"The fixing route is controlled."}]},{"id":"c3","label":"Finish","default":"proud","options":[{"value":"proud","label":"Fixing left proud","quality":0,"feedback":"It may catch and the joint may not seat correctly."},{"value":"flush","label":"Correctly seated or countersunk to the plan","quality":2,"feedback":"The surface and joint meet the quality check."}]}],"outcomes":[{"min":0,"max":2,"label":"weak or unsafe assembly risk","message":"Several controls are absent."},{"min":3,"max":4,"label":"assembly needs one correction","message":"One joint condition remains unreliable."},{"min":5,"max":6,"label":"ready for physical quality check","message":"Alignment, preparation and finish connect; the real joint still needs inspection."}],"completion":"A reliable assembly controls position before fixing, follows the specified pilot method and finishes the fixing safely.","predictionOptions":["The joint will be weak or out of square","The joint will need one correction","The joint will be ready for quality checking"],"requiredRuns":1},"independent":"Assemble the practice joint using the teacher-approved method. Check square, stability and fixing finish against the physical sample.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original exploded joint diagram with clamp, pilot path, fixing and square/flush checks.","mediaKey":"workshop","slug":"BUILD_DT_W4_Assembly","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"74ec9a4dc17490b6797de91bfbad5cc9edb06f206d1e93469717ae81ef3087ad"},"BUILD_DT_W5_Finish":{"path":"Build/Slideshows/BUILD_DT_W5_Finish.html","pathway":"BUILD","subsection":"D&T Community Upcycling","lessonTitle":"Week 5 · The Finish","targetTitle":"We Do 1","title":"Finish and quality evidence audit","purpose":"Teach pupils to use evidence-led quality checks instead of stopping when the object looks complete.","activity":{"type":"evidence","prompt":"Select the checks that could justify saying the asset is ready for the next stage. Reject appearance-only or unsafe shortcuts.","statements":[{"id":"e1","label":"Edges and surfaces are checked by sight and the agreed safe touch method.","correct":true,"reason":"The check targets splinters, sharpness and surface condition."},{"id":"e2","label":"The colour looks professional from across the room.","correct":false,"reason":"Appearance alone does not establish safety or specification."},{"id":"e3","label":"The finish used matches the local product instruction, risk assessment and intended environment.","correct":true,"reason":"Suitability is confirmed rather than guessed."},{"id":"e4","label":"Dust was brushed into the air so the bench looked clear.","correct":false,"reason":"Dry sweeping or dispersing dust can increase exposure; follow local controls."},{"id":"e5","label":"Dimensions and stability are rechecked after finishing.","correct":true,"reason":"The product still needs to meet the blueprint."},{"id":"e6","label":"More coating is always better.","correct":false,"reason":"Application follows the specified product and method."},{"id":"e7","label":"A named defect is recorded with an action owner before handover.","correct":true,"reason":"The issue remains visible and controlled."},{"id":"e8","label":"A photograph proves the surface is smooth and safe.","correct":false,"reason":"A photograph may support documentation but cannot replace physical inspection."}],"completion":"Quality control combines physical inspection, specification, safe process and an explicit defect route; appearance is only one part."},"independent":"Complete the physical QC sheet with the responsible adult: surface / dimensions / stability / finish / defect action.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original quality-control light table with surface, dimension, stability, specification and defect lenses.","mediaKey":"workshop","slug":"BUILD_DT_W5_Finish","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"5a8132d8f1e7535c67cee97b0d562ea4f813e3d49a323aeb0bac7372043f76df"},"BUILD_DT_W6_Handover":{"path":"Build/Slideshows/BUILD_DT_W6_Handover.html","pathway":"BUILD","subsection":"D&T Community Upcycling","lessonTitle":"Week 6 · The Handover","targetTitle":"We Do 1","title":"Evaluate, approve, transfer, report back","purpose":"Show how practical quality evidence, portfolio evidence and community transfer connect without collapsing into one celebration moment.","activity":{"type":"sequence","prompt":"Order the final evaluation and handover route. Explain which statements can be made now and which need later report-back.","steps":[{"id":"s1","label":"Compare the finished asset with the approved blueprint and site need.","reason":"Evaluation begins with the agreed criteria."},{"id":"s2","label":"Record any variance, repair or limitation honestly.","reason":"A difference is not hidden by presentation."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult approval."},{"id":"s4","label":"Prepare concise use, installation or maintenance information.","reason":"The recipient needs more than the object."},{"id":"s5","label":"Transfer the asset through the approved partner and site process.","reason":"The real handover follows local permissions."},{"id":"s6","label":"Record authentic receipt and immediate feedback only.","reason":"Do not invent use or impact that has not happened."},{"id":"s7","label":"Schedule or identify the later report-back owner.","reason":"Longer-term benefit requires later evidence."}],"completion":"A complete handover links specification, approval, recipient information, authentic receipt and a later report-back route."},"independent":"Complete the authorised portfolio and handover records. Mark any future impact as ‘not yet known’ until a real report-back exists.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original asset journey from blueprint through QC and approval to recipient and later report-back.","mediaKey":"workshop","slug":"BUILD_DT_W6_Handover","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"2e78cae9b3c2400096d0be90d156fcea5ccc42f6308724293cd307631e4d5a17"}});
/* ============================================================================
 * STATUS: mounted across all 85 taught ASDAN decks. The BLOCKED banner that
 * headed this file has been REMOVED, not softened -- it had become untrue.
 * All four original blocking items are closed; the only parked item is
 * docs/MEDIA_REGISTER.md, a candidate register that gates nothing (0 external
 * URLs in the payloads, so no mounted surface depends on it).
 *
 * Accessibility: eyebrow, sequence badges and buttons render on a SOLID chip
 * (--asvl-accent-chip, the pathway hue at a 74% mix toward black). The pair is
 * known rather than inherited, because the header tint moves per deck.
 * ========================================================================== */

/* ASDAN Visual Learning — progressive enhancement, rehearsal only. */
(() => {
  'use strict';

  const API_NAME = 'ASDANVisualLearning';
  if (window[API_NAME]?.version) return;

  const qs = (selector, root = document) => root.querySelector(selector);
  const qsa = (selector, root = document) => Array.from(root.querySelectorAll(selector));
  const el = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined && text !== null) node.textContent = String(text);
    return node;
  };
  const button = (label, className = 'asvl-button') => {
    const node = el('button', className, label);
    node.type = 'button';
    return node;
  };
  const setText = (node, text) => { if (node) node.textContent = String(text ?? ''); };

  /* Reduced motion, watched rather than sampled once.
     The blanket CSS rule already suppressed animation when the OS asked for it,
     but nothing in JS read the preference, so .asvl-static -- and the button that
     reports it -- stayed false while motion was actually off. Pattern taken from
     art-visual-learning.js, which fixed the same defect in the same shape. */
  const motionQuery = typeof window.matchMedia === 'function'
    ? window.matchMedia('(prefers-reduced-motion: reduce)')
    : null;
  const prefersReducedMotion = () => !!(motionQuery && motionQuery.matches);
  const motionSubscribers = new Set();
  if (motionQuery) {
    const onMotionChange = () => { motionSubscribers.forEach(fn => { try { fn(); } catch (e) {} }); };
    if (motionQuery.addEventListener) motionQuery.addEventListener('change', onMotionChange);
    else if (motionQuery.addListener) motionQuery.addListener(onMotionChange);
  }
  const slugFromLocation = () => {
    const declared = document.documentElement.dataset.asdanLesson || document.body?.dataset.asdanLesson;
    if (declared) return declared;
    const path = decodeURIComponent(location.pathname || '');
    const name = path.split('/').pop() || '';
    return name.replace(/\.html?$/i, '');
  };
  const seededShuffle = (values, seedText) => {
    const out = values.slice();
    let seed = 2166136261;
    for (const char of String(seedText)) {
      seed ^= char.charCodeAt(0);
      seed = Math.imul(seed, 16777619) >>> 0;
    }
    const next = () => {
      seed += 0x6D2B79F5;
      let t = seed;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
    for (let i = out.length - 1; i > 0; i -= 1) {
      const j = Math.floor(next() * (i + 1));
      [out[i], out[j]] = [out[j], out[i]];
    }
    if (out.length > 2 && out.every((item, index) => item === values[index])) {
      [out[0], out[1]] = [out[1], out[0]];
    }
    return out;
  };
  const announce = (panel, message) => {
    const live = qs('.asvl-live', panel);
    if (!live) return;
    live.textContent = '';
    window.setTimeout(() => { live.textContent = String(message); }, 20);
  };
  const safeFocus = node => { try { node?.focus({ preventScroll: false }); } catch (_) { node?.focus?.(); } };

  const pathwayCopy = {
    BUILD: {
      eyebrow: 'BUILD · SEE → CHOOSE → SAY → DO',
      predictionTitle: 'Look first',
      completionLead: 'You have rehearsed the decision.',
      colourLabel: 'BUILD visual rehearsal'
    },
    GROW: {
      eyebrow: 'GROW · PREDICT → TEST → COMPARE → JUSTIFY',
      predictionTitle: 'Commit a prediction',
      completionLead: 'You have compared evidence rather than guessed.',
      colourLabel: 'GROW visual investigation'
    },
    LAUNCH: {
      eyebrow: 'LAUNCH · INVESTIGATE → LOCATE EVIDENCE → REASON → ACT',
      predictionTitle: 'Commit a prediction',
      completionLead: 'The investigation is complete; now locate authentic evidence.',
      colourLabel: 'LAUNCH evidence-led investigation'
    }
  };

  function createState(payload) {
    const activity = payload.activity;
    const state = {
      prediction: null,
      completed: false,
      explanationOpen: false,
      transferOpen: false,
      staticMode: false,
      selectedItem: null,
      placed: new Map(),
      selectedEvidence: new Set(),
      openedHotspots: new Set(),
      sequence: activity.type === 'sequence'
        ? seededShuffle(activity.steps.map(step => step.id), payload.slug)
        : [],
      runs: [],
      locator: { evidenceForm: null, location: null, route: null },
      feedback: '',
      feedbackKind: 'neutral'
    };
    return state;
  }

  function targetForPayload(payload) {
    const exact = qsa('.slide').find(slide => (slide.getAttribute('data-title') || '').trim() === payload.targetTitle);
    if (exact) return exact;
    const wedo = qs('.slide[data-type="wedo"]') || qsa('.slide').find(slide => /we do/i.test(slide.getAttribute('data-title') || ''));
    return wedo || qs('.slide.active') || qs('main') || document.body;
  }

  function createPanel(payload) {
    const panel = el('section', `asvl-panel asvl-${payload.pathway.toLowerCase()}`);
    panel.dataset.asdanVisualLearning = payload.slug;
    panel.dataset.pathway = payload.pathway;
    panel.setAttribute('aria-label', `${payload.title}. ${pathwayCopy[payload.pathway].colourLabel}`);
    panel.tabIndex = -1;

    const header = el('header', 'asvl-header');
    const headText = el('div', 'asvl-header-text');
    headText.append(
      el('p', 'asvl-eyebrow', pathwayCopy[payload.pathway].eyebrow),
      el('h3', 'asvl-title', payload.title),
      el('p', 'asvl-purpose', payload.purpose)
    );
    const tools = el('div', 'asvl-tools');
    const staticBtn = button('▣ Static diagrams', 'asvl-button asvl-button-secondary asvl-static-toggle');
    staticBtn.setAttribute('aria-pressed', 'false');
    const resetBtn = button('↺ Reset rehearsal', 'asvl-button asvl-button-secondary asvl-reset');
    tools.append(staticBtn, resetBtn);
    header.append(headText, tools);

    const notice = el('p', 'asvl-notice', payload.panelNotice);
    const cycle = el('ol', 'asvl-cycle');
    payload.pathwayCycle.forEach((label, index) => {
      const item = el('li', index === 0 ? 'is-current' : '', label);
      item.dataset.stage = String(index);
      cycle.append(item);
    });

    const prediction = el('section', 'asvl-prediction');
    const activity = el('section', 'asvl-activity');
    const locator = el('section', 'asvl-locator');
    const explanation = el('section', 'asvl-explanation');
    const transfer = el('section', 'asvl-transfer');
    const route = el('aside', 'asvl-route');
    route.append(
      el('h4', '', 'Teacher, assessor and access route'),
      el('p', '', 'Use the lesson’s existing teacher, TA, assessor, responsible-adult, safety and reasonable-adjustment routes. This rehearsal cannot approve a risk, permission, criterion, level, evidence state or qualification outcome.')
    );
    const live = el('div', 'asvl-live');
    live.setAttribute('aria-live', 'polite');
    live.setAttribute('aria-atomic', 'true');

    panel.append(header, notice, cycle, prediction, activity, locator, explanation, transfer, route, live);
    return panel;
  }

  function setCycle(panel, stage) {
    qsa('.asvl-cycle li', panel).forEach((item, index) => {
      item.classList.toggle('is-current', index === stage);
      item.classList.toggle('is-complete', index < stage);
      if (index === stage) item.setAttribute('aria-current', 'step');
      else item.removeAttribute('aria-current');
    });
  }

  function setFeedback(panel, message, kind = 'neutral') {
    const box = qs('.asvl-feedback', panel);
    if (!box) return;
    box.className = `asvl-feedback is-${kind}`;
    setText(box, message);
    box.hidden = !message;
    if (message) announce(panel, message);
  }

  function renderPrediction(panel, payload, state) {
    const wrap = qs('.asvl-prediction', panel);
    wrap.replaceChildren();
    const options = payload.activity.predictionOptions || [];
    if (payload.pathway === 'BUILD' || !options.length) {
      wrap.hidden = true;
      return;
    }
    wrap.hidden = false;
    const heading = el('h4', '', pathwayCopy[payload.pathway].predictionTitle);
    const prompt = el('p', 'asvl-small', 'Choose the result or factor you expect before manipulating the information. You may revise your thinking after the evidence freezes.');
    const group = el('div', 'asvl-choice-row');
    group.setAttribute('role', 'group');
    group.setAttribute('aria-label', 'Prediction choices');
    options.forEach((option, index) => {
      const choice = button(option, 'asvl-choice');
      choice.dataset.prediction = String(index);
      choice.setAttribute('aria-pressed', state.prediction === index ? 'true' : 'false');
      choice.addEventListener('click', () => {
        state.prediction = index;
        qsa('.asvl-choice', group).forEach((node, nodeIndex) => {
          node.setAttribute('aria-pressed', nodeIndex === index ? 'true' : 'false');
        });
        panel.classList.add('has-prediction');
        setCycle(panel, 1);
        setActivityLocked(panel, false);
        announce(panel, `Prediction recorded: ${option}. The activity is now available.`);
        const firstControl = qs('.asvl-activity button:not([disabled]), .asvl-activity select:not([disabled])', panel);
        safeFocus(firstControl);
      });
      group.append(choice);
    });
    wrap.append(heading, prompt, group);
  }

  function setActivityLocked(panel, locked) {
    const activity = qs('.asvl-activity', panel);
    activity.classList.toggle('is-locked', locked);
    qsa('button, select', activity).forEach(control => {
      if (control.dataset.keepEnabled === 'true') return;
      control.disabled = locked;
    });
    const lock = qs('.asvl-activity-lock', activity);
    if (lock) lock.hidden = !locked;
  }

  function commonActivityShell(panel, payload, state) {
    const wrap = qs('.asvl-activity', panel);
    wrap.replaceChildren();
    const heading = el('h4', '', 'Manipulate the information');
    const prompt = el('p', 'asvl-prompt', payload.activity.prompt);
    const lock = el('p', 'asvl-activity-lock', 'Choose a prediction first. This prevents hindsight from replacing thinking.');
    const canvas = el('div', 'asvl-canvas');
    const feedback = el('div', 'asvl-feedback');
    feedback.hidden = true;
    feedback.setAttribute('role', 'status');
    wrap.append(heading, prompt, lock, canvas, feedback);
    const locked = payload.pathway !== 'BUILD' && state.prediction === null;
    setActivityLocked(panel, locked);
    return canvas;
  }

  function completeActivity(panel, payload, state) {
    if (state.completed) return;
    state.completed = true;
    panel.classList.add('is-activity-complete');
    setCycle(panel, payload.pathway === 'LAUNCH' ? 1 : 2);
    qsa('.asvl-activity button, .asvl-activity select', panel).forEach(control => {
      if (!control.classList.contains('asvl-reset')) control.disabled = true;
    });
    setFeedback(panel, `${pathwayCopy[payload.pathway].completionLead} ${payload.activity.completion}`, 'success');
    renderLocator(panel, payload, state);
    renderExplanation(panel, payload, state);
  }

  function renderSort(panel, payload, state) {
    const canvas = commonActivityShell(panel, payload, state);
    const activity = payload.activity;
    const layout = el('div', 'asvl-sort-layout');
    const bank = el('div', 'asvl-bank');
    bank.append(el('h5', '', 'Choose one card'));
    const items = el('div', 'asvl-item-grid');
    const targets = el('div', 'asvl-target-grid');

    const chooseItem = itemId => {
      if (state.placed.has(itemId)) return;
      state.selectedItem = itemId;
      qsa('.asvl-sort-item', panel).forEach(node => {
        const selected = node.dataset.itemId === itemId;
        node.classList.toggle('is-selected', selected);
        node.setAttribute('aria-pressed', selected ? 'true' : 'false');
      });
      const item = activity.items.find(entry => entry.id === itemId);
      setFeedback(panel, `Selected: ${item.label}. Now choose a destination.`, 'neutral');
    };

    activity.items.forEach(item => {
      const card = button(`${item.icon || '◆'} ${item.label}`, 'asvl-sort-item');
      card.dataset.itemId = item.id;
      card.setAttribute('aria-pressed', 'false');
      card.draggable = true;
      card.addEventListener('click', () => chooseItem(item.id));
      card.addEventListener('dragstart', event => {
        event.dataTransfer?.setData('text/plain', item.id);
        chooseItem(item.id);
      });
      if (state.placed.has(item.id)) card.hidden = true;
      items.append(card);
    });

    activity.categories.forEach(category => {
      const target = el('div', 'asvl-sort-target');
      target.dataset.categoryId = category.id;
      const targetButton = button(`${category.icon || '◇'} ${category.label}`, 'asvl-target-button');
      targetButton.addEventListener('click', () => place(state.selectedItem, category.id));
      const placed = el('div', 'asvl-placed-list');
      placed.setAttribute('aria-label', `Cards placed under ${category.label}`);
      for (const [itemId, categoryId] of state.placed.entries()) {
        if (categoryId !== category.id) continue;
        const item = activity.items.find(entry => entry.id === itemId);
        placed.append(el('div', 'asvl-placed-card', `✓ ${item.label}`));
      }
      target.addEventListener('dragover', event => event.preventDefault());
      target.addEventListener('drop', event => {
        event.preventDefault();
        const itemId = event.dataTransfer?.getData('text/plain') || state.selectedItem;
        place(itemId, category.id);
      });
      target.append(targetButton, placed);
      targets.append(target);
    });

    function place(itemId, categoryId) {
      if (!itemId) {
        setFeedback(panel, 'Choose a card before choosing a destination.', 'prompt');
        return;
      }
      const item = activity.items.find(entry => entry.id === itemId);
      if (!item || state.placed.has(itemId)) return;
      if (item.answer !== categoryId) {
        setFeedback(panel, `Not there yet. ${item.reason}`, 'retry');
        return;
      }
      state.placed.set(itemId, categoryId);
      state.selectedItem = null;
      setFeedback(panel, `Placed correctly. ${item.reason}`, 'success');
      renderSort(panel, payload, state);
      if (state.placed.size === activity.items.length) completeActivity(panel, payload, state);
      else {
        setCycle(panel, 1);
        const next = qs('.asvl-sort-item:not([hidden])', panel);
        safeFocus(next);
      }
    }

    bank.append(items);
    layout.append(bank, targets);
    canvas.append(layout);
  }

  function renderSequence(panel, payload, state) {
    const canvas = commonActivityShell(panel, payload, state);
    const activity = payload.activity;
    const list = el('ol', 'asvl-sequence-list');
    state.sequence.forEach((stepId, index) => {
      const step = activity.steps.find(entry => entry.id === stepId);
      const row = el('li', 'asvl-sequence-row');
      const number = el('span', 'asvl-sequence-number', String(index + 1));
      const text = el('span', 'asvl-sequence-text', step.label);
      const controls = el('span', 'asvl-sequence-controls');
      const up = button('↑ Move up', 'asvl-mini-button');
      const down = button('↓ Move down', 'asvl-mini-button');
      up.setAttribute('aria-label', `Move ${step.label} up`);
      down.setAttribute('aria-label', `Move ${step.label} down`);
      up.disabled = index === 0 || (payload.pathway !== 'BUILD' && state.prediction === null);
      down.disabled = index === state.sequence.length - 1 || (payload.pathway !== 'BUILD' && state.prediction === null);
      up.addEventListener('click', () => {
        [state.sequence[index - 1], state.sequence[index]] = [state.sequence[index], state.sequence[index - 1]];
        renderSequence(panel, payload, state);
        safeFocus(qsa('.asvl-sequence-row', panel)[index - 1]?.querySelector('button'));
      });
      down.addEventListener('click', () => {
        [state.sequence[index + 1], state.sequence[index]] = [state.sequence[index], state.sequence[index + 1]];
        renderSequence(panel, payload, state);
        safeFocus(qsa('.asvl-sequence-row', panel)[index + 1]?.querySelector('button'));
      });
      controls.append(up, down);
      row.append(number, text, controls);
      list.append(row);
    });
    const check = button('Check the sequence', 'asvl-button asvl-check');
    check.addEventListener('click', () => {
      const expected = activity.steps.map(step => step.id);
      const correct = state.sequence.every((id, index) => id === expected[index]);
      if (correct) {
        qsa('.asvl-sequence-row', panel).forEach(row => row.classList.add('is-correct'));
        completeActivity(panel, payload, state);
      } else {
        const firstWrong = state.sequence.findIndex((id, index) => id !== expected[index]);
        const expectedStep = activity.steps[firstWrong];
        setFeedback(panel, `Recheck position ${firstWrong + 1}. Ask what must already be true before “${expectedStep.label}”.`, 'retry');
      }
    });
    canvas.append(list, check);
  }

  function renderEvidence(panel, payload, state) {
    const canvas = commonActivityShell(panel, payload, state);
    const activity = payload.activity;
    const grid = el('div', 'asvl-evidence-grid');
    activity.statements.forEach(statement => {
      const card = button(statement.label, 'asvl-evidence-card');
      card.dataset.statementId = statement.id;
      const selected = state.selectedEvidence.has(statement.id);
      card.setAttribute('aria-pressed', selected ? 'true' : 'false');
      card.classList.toggle('is-selected', selected);
      card.addEventListener('click', () => {
        if (state.selectedEvidence.has(statement.id)) state.selectedEvidence.delete(statement.id);
        else state.selectedEvidence.add(statement.id);
        renderEvidence(panel, payload, state);
        setFeedback(panel, `${state.selectedEvidence.size} item${state.selectedEvidence.size === 1 ? '' : 's'} selected. Check when the set is complete.`, 'neutral');
      });
      grid.append(card);
    });
    const check = button('Check the evidence set', 'asvl-button asvl-check');
    check.addEventListener('click', () => {
      const correctIds = new Set(activity.statements.filter(item => item.correct).map(item => item.id));
      const exact = correctIds.size === state.selectedEvidence.size &&
        Array.from(correctIds).every(id => state.selectedEvidence.has(id));
      qsa('.asvl-evidence-card', panel).forEach(card => {
        const statement = activity.statements.find(item => item.id === card.dataset.statementId);
        const selected = state.selectedEvidence.has(statement.id);
        card.classList.toggle('is-correct-choice', selected && statement.correct);
        card.classList.toggle('is-wrong-choice', selected && !statement.correct);
        card.classList.toggle('is-missed-choice', !selected && statement.correct);
      });
      if (exact) {
        completeActivity(panel, payload, state);
      } else {
        const selectedWrong = activity.statements.find(item => state.selectedEvidence.has(item.id) && !item.correct);
        const missed = activity.statements.find(item => !state.selectedEvidence.has(item.id) && item.correct);
        const focus = selectedWrong || missed;
        setFeedback(panel, focus ? focus.reason : 'Recheck the complete set.', 'retry');
      }
    });
    canvas.append(grid, check);
  }

  function sceneSvg(scene, label) {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 100 70');
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', `${label}. Simplified original teaching model.`);
    svg.classList.add('asvl-hotspot-svg');
    const ns = 'http://www.w3.org/2000/svg';
    const rect = (x, y, w, h, cls) => {
      const node = document.createElementNS(ns, 'rect');
      node.setAttribute('x', x); node.setAttribute('y', y); node.setAttribute('width', w); node.setAttribute('height', h);
      node.setAttribute('rx', '3'); node.setAttribute('class', cls);
      return node;
    };
    const path = document.createElementNS(ns, 'path');
    path.setAttribute('d', scene === 'room'
      ? 'M8 58 H92 M12 58 V18 H88 V58 M35 18 V58 M64 18 V58'
      : scene === 'workplace'
        ? 'M6 58 H94 M12 58 V26 L28 14 L44 26 V58 M55 58 V20 H86 V58'
        : 'M5 60 C24 44 34 62 50 49 C64 38 76 46 95 28');
    path.setAttribute('class', 'asvl-scene-line');
    svg.append(path);
    svg.append(rect(10, 10, 22, 14, 'asvl-scene-shape'));
    svg.append(rect(39, 23, 22, 14, 'asvl-scene-shape'));
    svg.append(rect(68, 10, 22, 14, 'asvl-scene-shape'));
    svg.append(rect(17, 45, 22, 14, 'asvl-scene-shape'));
    svg.append(rect(62, 43, 22, 14, 'asvl-scene-shape'));
    return svg;
  }

  function renderHotspot(panel, payload, state) {
    const canvas = commonActivityShell(panel, payload, state);
    const activity = payload.activity;
    const scene = el('div', 'asvl-hotspot-scene');
    scene.append(sceneSvg(activity.scene || 'map', payload.title));
    activity.hotspots.forEach((spot, index) => {
      const spotButton = button(String(index + 1), 'asvl-hotspot-button');
      spotButton.style.left = `${spot.x}%`;
      spotButton.style.top = `${spot.y}%`;
      spotButton.setAttribute('aria-label', `Open hotspot ${index + 1}: ${spot.label}`);
      const opened = state.openedHotspots.has(spot.id);
      spotButton.classList.toggle('is-open', opened);
      spotButton.setAttribute('aria-pressed', opened ? 'true' : 'false');
      spotButton.addEventListener('click', () => {
        state.openedHotspots.add(spot.id);
        renderHotspot(panel, payload, state);
        setFeedback(panel, `${spot.label}. ${spot.note}`, 'success');
        if (state.openedHotspots.size === activity.hotspots.length) completeActivity(panel, payload, state);
      });
      scene.append(spotButton);
    });
    const notes = el('div', 'asvl-hotspot-notes');
    activity.hotspots.forEach((spot, index) => {
      if (!state.openedHotspots.has(spot.id)) return;
      const note = el('article', 'asvl-hotspot-note');
      note.append(el('strong', '', `${index + 1}. ${spot.label}`), el('p', '', spot.note));
      notes.append(note);
    });
    canvas.append(scene, notes);
  }

  function findOutcome(activity, score) {
    return activity.outcomes.find(outcome => score >= outcome.min && score <= outcome.max)
      || activity.outcomes[activity.outcomes.length - 1];
  }

  function renderModel(panel, payload, state) {
    const canvas = commonActivityShell(panel, payload, state);
    const activity = payload.activity;
    const form = el('div', 'asvl-model');
    const controlsWrap = el('div', 'asvl-model-controls');
    activity.controls.forEach(control => {
      const label = el('label', 'asvl-model-control');
      label.append(el('span', '', control.label));
      const select = el('select', '');
      select.dataset.controlId = control.id;
      control.options.forEach(option => {
        const optionNode = el('option', '', option.label);
        optionNode.value = option.value;
        select.append(optionNode);
      });
      const last = state.runs[state.runs.length - 1];
      select.value = last?.values?.[control.id] ?? control.default ?? control.options[0].value;
      label.append(select);
      controlsWrap.append(label);
    });

    const run = button(state.runs.length ? 'Run one controlled change' : 'Run and freeze the result', 'asvl-button asvl-run');
    run.addEventListener('click', () => {
      const values = {};
      let score = 0;
      const feedback = [];
      activity.controls.forEach(control => {
        const value = qs(`select[data-control-id="${CSS.escape(control.id)}"]`, panel)?.value;
        values[control.id] = value;
        const option = control.options.find(item => item.value === value) || control.options[0];
        score += Number(option.quality || 0);
        feedback.push(`${control.label}: ${option.feedback}`);
      });
      if (state.runs.length && activity.requiredRuns > 1) {
        const previous = state.runs[state.runs.length - 1].values;
        const changed = Object.keys(values).filter(key => values[key] !== previous[key]);
        if (changed.length !== 1) {
          setFeedback(panel, `Change exactly one variable between frozen runs. You changed ${changed.length}.`, 'retry');
          return;
        }
      }
      const outcome = findOutcome(activity, score);
      state.runs.push({ values, score, outcome, feedback });
      setCycle(panel, 2);
      setFeedback(panel, `Frozen result ${state.runs.length}: ${outcome.label}. ${outcome.message}`, 'success');
      renderModel(panel, payload, state);
      if (state.runs.length >= activity.requiredRuns) completeActivity(panel, payload, state);
    });

    const history = el('div', 'asvl-run-history');
    state.runs.forEach((record, index) => {
      const card = el('article', 'asvl-run-card');
      card.append(
        el('h5', '', `Frozen run ${index + 1} · ${record.outcome.label}`),
        el('p', '', record.outcome.message)
      );
      const list = el('ul', '');
      record.feedback.forEach(line => list.append(el('li', '', line)));
      card.append(list);
      history.append(card);
    });

    const runRule = el('p', 'asvl-small', activity.requiredRuns > 1
      ? `Complete ${activity.requiredRuns} frozen runs. After the first, change exactly one variable so the comparison is fair.`
      : 'Complete one frozen run, then transfer the structure to the real task.');
    form.append(runRule, controlsWrap, run, history);
    canvas.append(form);
  }

  function renderActivity(panel, payload, state) {
    const renderers = {
      sort: renderSort,
      sequence: renderSequence,
      evidence: renderEvidence,
      hotspot: renderHotspot,
      model: renderModel
    };
    const renderer = renderers[payload.activity.type];
    if (!renderer) {
      const canvas = commonActivityShell(panel, payload, state);
      canvas.append(el('p', 'asvl-error', `Unsupported activity type: ${payload.activity.type}`));
      return;
    }
    renderer(panel, payload, state);
  }

  function locatorComplete(state) {
    return Boolean(state.locator.evidenceForm && state.locator.location && state.locator.route);
  }

  function renderLocator(panel, payload, state) {
    const wrap = qs('.asvl-locator', panel);
    wrap.replaceChildren();
    if (payload.pathway !== 'LAUNCH') {
      wrap.hidden = true;
      return;
    }
    wrap.hidden = false;
    wrap.classList.toggle('is-locked', !state.completed);
    wrap.append(
      el('h4', '', 'Structured evidence locator · not an evidence judgement'),
      el('p', 'asvl-small', 'After the real task, select where authentic evidence could be found and the authorised next route. Do not upload anything here. “Not yet” is an honest option.')
    );
    const groups = [
      ['evidenceForm', 'What exists?', payload.locator.evidenceForms],
      ['location', 'Where is it?', payload.locator.locations],
      ['route', 'What is the next authorised route?', payload.locator.routes]
    ];
    groups.forEach(([key, legendText, options]) => {
      const fieldset = el('fieldset', 'asvl-locator-group');
      const legend = el('legend', '', legendText);
      fieldset.append(legend);
      options.forEach(option => {
        const label = el('label', 'asvl-radio-card');
        const input = el('input', '');
        input.type = 'radio';
        input.name = `${payload.slug}-${key}`;
        input.value = option.id;
        input.checked = state.locator[key] === option.id;
        input.disabled = !state.completed;
        input.addEventListener('change', () => {
          state.locator[key] = option.id;
          renderLocator(panel, payload, state);
          renderExplanation(panel, payload, state);
          if (locatorComplete(state)) {
            announce(panel, 'The structured evidence locator is complete. The explanation is now available.');
            safeFocus(qs('.asvl-open-explanation:not([disabled])', panel));
          }
        });
        label.append(input, el('span', '', option.label));
        fieldset.append(label);
      });
      wrap.append(fieldset);
    });
    const caution = el('p', 'asvl-caution', 'This locator records no evidence state. It cannot mark work achieved, verified, moderated, certified or returned. Those are authorised human and awarding-body processes.');
    wrap.append(caution);
  }

  function canOpenExplanation(payload, state) {
    return state.completed && (payload.pathway !== 'LAUNCH' || locatorComplete(state));
  }

  function renderExplanation(panel, payload, state) {
    const wrap = qs('.asvl-explanation', panel);
    wrap.replaceChildren();
    const allowed = canOpenExplanation(payload, state);
    const heading = el('h4', '', payload.pathway === 'LAUNCH' ? 'Reason from the evidence' : 'Name the learning');
    const status = el('p', 'asvl-small', allowed
      ? 'The rehearsal conditions are complete. Open the explanation, then transfer it to the real task.'
      : payload.pathway === 'LAUNCH'
        ? 'Complete the investigation and all three structured locator choices. Activity completion alone does not unlock the explanation.'
        : 'Complete the manipulation before opening the explanation.');
    const open = button(state.explanationOpen ? '✓ Explanation opened' : 'Open explanation', 'asvl-button asvl-open-explanation');
    open.disabled = !allowed || state.explanationOpen;
    open.addEventListener('click', () => {
      state.explanationOpen = true;
      const openedBy = payload.pathway === 'LAUNCH'
        ? 'completed activity and selected structured evidence-locator route'
        : 'completed classroom rehearsal';
      panel.dataset.asdanOpenedBy = openedBy;
      setCycle(panel, 2);
      renderExplanation(panel, payload, state);
      announce(panel, payload.activity.completion);
      safeFocus(qs('.asvl-explanation-body', panel));
    });
    wrap.append(heading, status, open);
    if (state.explanationOpen) {
      const body = el('div', 'asvl-explanation-body');
      body.tabIndex = -1;
      body.append(
        el('p', 'asvl-completion', payload.activity.completion),
        el('p', 'asvl-prediction-review', state.prediction !== null && payload.activity.predictionOptions
          ? `Your prediction was: ${payload.activity.predictionOptions[state.prediction]}. Compare it with the frozen evidence; changing your mind is evidence of thinking, not failure.`
          : 'Point to the part of the frozen visual that supports the explanation.')
      );
      const transferBtn = button('Begin the independent task', 'asvl-button asvl-transfer-button');
      transferBtn.addEventListener('click', () => {
        state.transferOpen = true;
        setCycle(panel, 3);
        renderTransfer(panel, payload, state);
        panel.classList.add('is-transfer-mode');
        safeFocus(qs('.asvl-transfer', panel));
      });
      body.append(transferBtn);
      wrap.append(body);
    }
  }

  function renderTransfer(panel, payload, state) {
    const wrap = qs('.asvl-transfer', panel);
    wrap.replaceChildren();
    wrap.hidden = !state.transferOpen;
    if (!state.transferOpen) return;
    wrap.tabIndex = -1;
    wrap.append(
      el('p', 'asvl-eyebrow', 'INDEPENDENT HANDOVER'),
      el('h4', '', 'Use the rehearsal, then close the distance yourself'),
      el('p', 'asvl-independent-task', payload.independent)
    );
    const steps = el('ol', 'asvl-independence-steps');
    payload.independenceSteps.forEach(step => steps.append(el('li', '', step)));
    const checks = el('div', 'asvl-success-checks');
    checks.append(el('h5', '', 'Stop-and-check conditions'));
    const checkList = el('ul', '');
    payload.successChecks.forEach(check => checkList.append(el('li', '', check)));
    checks.append(checkList);
    const help = el('details', 'asvl-help-ladder');
    const summary = el('summary', '', 'Help ladder · use the least help that works');
    const helpList = el('ol', '');
    payload.helpLadder.forEach(step => helpList.append(el('li', '', step)));
    help.append(summary, helpList);
    const back = button('Return to the frozen rehearsal', 'asvl-button asvl-button-secondary');
    back.addEventListener('click', () => {
      state.transferOpen = false;
      panel.classList.remove('is-transfer-mode');
      setCycle(panel, 2);
      renderTransfer(panel, payload, state);
      safeFocus(qs('.asvl-transfer-button', panel));
    });
    wrap.append(steps, checks, help, back);
  }

  function resetPanel(panel, payload, stateRef) {
    const replacement = createState(payload);
    Object.keys(stateRef).forEach(key => delete stateRef[key]);
    Object.assign(stateRef, replacement);
    panel.classList.remove('has-prediction', 'is-activity-complete', 'is-transfer-mode', 'asvl-static');
    /* Reset clears the user's override, never the machine's preference. */
    panel.classList.toggle('asvl-static', prefersReducedMotion());
    delete panel.dataset.asdanOpenedBy;
    setCycle(panel, 0);
    renderPrediction(panel, payload, stateRef);
    renderActivity(panel, payload, stateRef);
    renderLocator(panel, payload, stateRef);
    renderExplanation(panel, payload, stateRef);
    renderTransfer(panel, payload, stateRef);
    announce(panel, 'Rehearsal reset. No data was stored.');
  }

  function mountPayload(payload, target) {
    if (!payload || !payload.slug) throw new Error('A valid ASDAN visual-learning payload is required.');
    const host = target || targetForPayload(payload);
    if (!host) throw new Error(`No mount target found for ${payload.slug}.`);
    const previous = qs(`[data-asdan-visual-learning="${CSS.escape(payload.slug)}"]`, host);
    if (previous) return previous;

    const panel = createPanel(payload);
    const state = createState(payload);
    host.append(panel);
    if (!host.classList.contains('slide')) panel.classList.add('asvl-standalone');

    const staticBtn = qs('.asvl-static-toggle', panel);
    /* Effective state is the user's choice OR the OS preference. The OS is a floor,
       not a default: if the machine asks for reduced motion, the button cannot turn
       movement back on, because the CSS rule would suppress it anyway and the
       control would then be lying about what the pupil sees. */
    const staticIsOn = () => state.staticMode || prefersReducedMotion();
    const paintStatic = () => {
      const on = staticIsOn();
      panel.classList.toggle('asvl-static', on);
      staticBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
      staticBtn.textContent = on ? '✓ Static diagrams' : '▣ Static diagrams';
      staticBtn.disabled = prefersReducedMotion();
    };
    paintStatic();
    motionSubscribers.add(paintStatic);
    staticBtn.addEventListener('click', () => {
      if (prefersReducedMotion()) return;
      state.staticMode = !state.staticMode;
      paintStatic();
      announce(panel, state.staticMode ? 'Static diagrams enabled.' : 'Finite teaching movement enabled.');
    });
    qs('.asvl-reset', panel).addEventListener('click', () => resetPanel(panel, payload, state));

    renderPrediction(panel, payload, state);
    renderActivity(panel, payload, state);
    renderLocator(panel, payload, state);
    renderExplanation(panel, payload, state);
    renderTransfer(panel, payload, state);
    setCycle(panel, 0);

    panel.__asdanVisualState = state;
    panel.__asdanVisualPayload = payload;
    panel.dataset.asdanVisualReady = 'true';
    return panel;
  }

  function autoMount() {
    const registry = window.ASDANVisualPayloads || {};
    const slug = slugFromLocation();
    const payload = registry[slug];
    if (!payload) return null;
    return mountPayload(payload, targetForPayload(payload));
  }

  const api = {
    version: '1.0.0',
    mountPayload,
    autoMount,
    slugFromLocation,
    targetForPayload,
    getState(panel) { return panel?.__asdanVisualState || null; }
  };
  window[API_NAME] = api;

  const start = () => {
    try { autoMount(); }
    catch (error) {
      console.error('ASDAN Visual Learning did not mount:', error);
      document.documentElement.dataset.asdanVisualError = 'true';
    }
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
  else start();
})();
/* ASDAN-VISUAL-LEARNING:JS:END v1 */
