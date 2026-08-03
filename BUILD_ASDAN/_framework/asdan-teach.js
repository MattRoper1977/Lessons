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
