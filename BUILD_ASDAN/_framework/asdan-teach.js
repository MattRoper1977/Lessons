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
window.ASDANVisualPayloads = Object.assign(window.ASDANVisualPayloads || {}, {"CAREERS_W1_My_Strengths":{"path":"BUILD_ASDAN/Careers/CAREERS_W1_My_Strengths.html","pathway":"BUILD","subsection":"Careers","lessonTitle":"Week 1 · My Strengths","targetTitle":"We Do 1","title":"Strengths → actions → work evidence","purpose":"Make strengths concrete before pupils build a profile, reducing empty claims such as ‘I am good at teamwork’.","activity":{"type":"sort","prompt":"Place each example under the strength it actually proves. Say the observable action, not just the positive word.","categories":[{"id":"team","icon":"👥","label":"TEAMWORK"},{"id":"reliable","icon":"⏱","label":"RELIABILITY"},{"id":"solve","icon":"🧩","label":"PROBLEM SOLVING"}],"items":[{"id":"i1","icon":"👥","label":"I shared the materials and checked my partner understood.","answer":"team","reason":"The action supports another person and the shared task."},{"id":"i2","icon":"⏱","label":"I arrived with the right equipment before the start.","answer":"reliable","reason":"It shows preparation and keeping a commitment."},{"id":"i3","icon":"🧩","label":"When the first method failed, I tried a second safe method.","answer":"solve","reason":"It shows a problem, a change and a result."},{"id":"i4","icon":"👥","label":"I listened, then used one idea from someone else.","answer":"team","reason":"Listening affects the group decision."},{"id":"i5","icon":"⏱","label":"I completed the agreed step by the deadline.","answer":"reliable","reason":"The evidence is a kept time commitment."},{"id":"i6","icon":"🧩","label":"I broke a large task into three smaller steps.","answer":"solve","reason":"The strategy makes the task manageable."}],"completion":"A strength becomes useful for careers when it is attached to something a person actually did."},"independent":"Choose two strengths. For each, add one real example using: I did… / This shows… / It could help in…","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original three-lane strength evidence map with action cards moving from pupil experience to workplace use.","mediaKey":"careers","slug":"CAREERS_W1_My_Strengths","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"f1d0562fcce182b9f258fc0a83e70563777318aa0fd9983309ece6cb2bea3d42"},"BUILD_DT_W1_Workshop_Audit":{"path":"Build/Slideshows/BUILD_DT_W1_Workshop_Audit.html","pathway":"BUILD","subsection":"D&T Community Upcycling","lessonTitle":"Week 1 · The Workshop Audit","targetTitle":"We Do 1","title":"Workshop safety hotspot audit","purpose":"Turn safety from a poster into a visual scan-and-report routine while keeping teacher instruction and local controls load-bearing.","activity":{"type":"hotspot","scene":"workshop","prompt":"Open each workshop hotspot. Name the hazard or control, then point to the physical feature that made you notice it. The local risk assessment remains authoritative.","hotspots":[{"id":"h1","x":18,"y":24,"label":"CLEAR WALKWAY","note":"Offcuts and bags create trip hazards and block movement routes."},{"id":"h2","x":50,"y":18,"label":"CLAMPING ZONE","note":"Work must be secured using the demonstrated method before cutting or drilling."},{"id":"h3","x":82,"y":27,"label":"TOOL HOME","note":"Tools need a visible safe storage position so missing or damaged items are noticed."},{"id":"h4","x":23,"y":66,"label":"DUST CONTROL","note":"Extraction, suitable cleaning and local protective measures control wood dust; never improvise."},{"id":"h5","x":52,"y":72,"label":"PPE / ACCESS CHECK","note":"Required protection and reasonable adjustments are confirmed for the actual task."},{"id":"h6","x":82,"y":65,"label":"STOP / REPORT ROUTE","note":"A pupil stops and tells the responsible adult when a guard, tool, material or condition is wrong."}],"completion":"A workshop audit links a visible condition to a control and a named reporting route; spotting is not permission to fix unfamiliar equipment."},"independent":"Complete the real workshop audit with the teacher. Record one safe condition, one issue reported and the agreed action owner.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original classroom workshop plan with walkway, bench, tool storage, dust control and stop/report hotspots.","mediaKey":"workshop","slug":"BUILD_DT_W1_Workshop_Audit","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["SEE","CHOOSE","SAY","DO"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"321c063244ac710ded8b4d02a7e617cde31d211d288d6ad96e0e438713c321fa"}});
/* ============================================================================
 * BLOCKED — DO NOT MOUNT
 *
 * This engine is committed but loaded by nothing. No lesson in this repository
 * references it, and none may until the blockers in README.md are cleared.
 *
 * Named blocking items (see README.md for the derivations):
 *   1. The vendor's decisive gate -- full post-integration regression in a real,
 *      current checkout -- is UNRUN. Nothing pupil-facing merges until it is.
 *   2. CLEARED 5 Aug 2026 -- reduced motion is now read from matchMedia at load
 *      and watched with a change listener; .asvl-static follows the OS preference.
 *      Proven in both directions in a real browser; family classified as RM-3.
 *   3. The six D&T decks are on a different chassis and outside the BUILD
 *      compiler's scope. They do not mount by mounting this.
 *
 * Landed 5 Aug 2026, band A of the ASDAN Visual-Learning review.
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
