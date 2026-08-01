/* ==========================================================================
   LAUNCH Scientific Observation Layer — engine
   --------------------------------------------------------------------------
   PHILOSOPHY (the reason every awkward-looking guard below exists)

     BUILD   animation REPLACES text        — the pupil reads less
     GROW    animation EXPLAINS a process   — the pupil follows a mechanism
     LAUNCH  animation SUPPORTS REASONING   — the pupil does the science

   So in LAUNCH nothing in this file may reveal a scientific label, pattern or
   explanation on load, on hover, or on a timer alone. Every reveal is gated on
   an act the pupil performed: a noticing placed, a prediction committed, a
   variable changed, a difference found. `_gate()` is the one function that
   opens things, and it takes the reason as an argument so that the gate is
   never opened by accident.

   The layer is injected into a lesson as ONE script plus ONE payload. It reads
   `window.SCI_LESSON` and places its components into the existing slides. It
   never rewrites slide markup it did not create, and it never touches the
   print pack (REGISTER R-E05).
   ========================================================================== */
(function (window, document) {
  'use strict';

  if (window.SCI && window.SCI.__v) { return; }           /* idempotent */

  var SCI = { __v: 1, comps: {}, scenes: {}, sims: {} };
  window.SCI = SCI;

  /* ---------------------------------------------------------------- utils */

  var REDUCED = false;
  try {
    REDUCED = window.matchMedia && window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  } catch (e) { REDUCED = false; }

  function el(tag, attrs, kids) {
    var n = document.createElement(tag), k;
    if (attrs) for (k in attrs) {
      if (!Object.prototype.hasOwnProperty.call(attrs, k)) continue;
      if (k === 'html') n.innerHTML = attrs[k];
      else if (k === 'text') n.textContent = attrs[k];
      else if (k === 'cls') n.className = attrs[k];
      else if (attrs[k] !== null && attrs[k] !== undefined) n.setAttribute(k, attrs[k]);
    }
    if (kids) kids.forEach(function (c) { if (c) n.appendChild(c); });
    return n;
  }
  function q(root, sel) { return root.querySelector(sel); }
  function qa(root, sel) { return Array.prototype.slice.call(root.querySelectorAll(sel)); }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  /* Borrow the host deck's feedback, but never depend on it. These lessons
     already define playDing/gainXP; a lesson that does not must still work. */
  function ding() { try { if (window.playDing) window.playDing(); } catch (e) {} }
  function buzz() { try { if (window.playBuzz) window.playBuzz(); } catch (e) {} }

  /* The deck's XP bar has a fixed total, registered before this layer mounts,
     and `gainXP()` fires level-up + confetti the moment the count reaches it.
     So the layer MUST declare how many awards it can make and then stay inside
     that figure — otherwise a pupil dragging a slider sets off the
     end-of-lesson celebration during the first I Do. Every award goes through
     `xp()`, which spends from a pool `declareXP()` filled and `registerXP()`
     was told about. Do not call window.gainXP directly from a component. */
  var XP_POOL = 0;
  function declareXP(n) {
    n = Math.max(0, Math.round(n || 0));
    if (!n) return;
    XP_POOL += n;
    try { if (window.registerXP) window.registerXP(n); } catch (e) {}
  }
  function xp() {
    if (XP_POOL <= 0) return;
    XP_POOL--;
    try { if (window.gainXP) window.gainXP(); } catch (e) {}
  }

  /* How many awards a component can possibly make. Deliberately an upper bound:
     under-declaring makes a component go quiet halfway through; over-declaring
     only means the bar fills a little more slowly than the lesson does. */
  function xpCost(c) {
    switch (c.type) {
      case 'observe':  return (c.noticeTarget || 3) + 1 + (c.hotspots || []).length;
      case 'discover': return (c.steps || []).length * 2 + 1;
      case 'zoom':     return Math.max(0, (c.levels || []).length - 1) * 2;
      case 'method':   return (c.steps || []).length * 2;
      case 'chain':    return (c.stages || []).length;
      case 'graph':    return (c.points || []).length + (c.predictBefore ? 1 : 0);
      case 'compare':  return (c.differences || []).length;
      case 'model':    return 4 + (c.tradeOff ? 1 : 0);   /* capped: sliders are unbounded */
      case 'pause':    return 1;
      default:         return 1;
    }
  }

  /* A label is positioned as a percentage of the figure, then centred on that
     point — so a long label near an edge hangs outside the stage and gets
     clipped by `overflow:hidden`. Nudge it back inside once it is on screen.
     Called after the reveal transition starts, so it measures a laid-out box. */
  function keepInside(stage, node) {
    try {
      var s = stage.getBoundingClientRect(), n = node.getBoundingClientRect();
      if (!s.width || !n.width) return;
      var over = 0;
      if (n.left < s.left + 4) over = (s.left + 4) - n.left;
      else if (n.right > s.right - 4) over = (s.right - 4) - n.right;
      if (over) node.style.marginLeft = over.toFixed(1) + 'px';
    } catch (e) {}
  }

  /* The single opening function. `why` is required and is recorded on the
     element, so that a reveal can always be traced to the act that earned it. */
  function _gate(node, why) {
    if (!node || !why) return false;
    node.setAttribute('data-sci-opened-by', why);
    node.removeAttribute('data-locked');
    return true;
  }

  /* -------------------------------------------------- the twelve LAUNCH verbs */

  var VERBS = {
    zoom:      ['🔍', 'Zoom'],
    spotlight: ['🎯', 'Spotlight'],
    annotate:  ['✏️', 'Annotate'],
    measure:   ['📏', 'Measure'],
    compare:   ['⚖️', 'Compare'],
    graph:     ['📊', 'Graph'],
    simulate:  ['🧪', 'Simulate'],
    classify:  ['🧩', 'Classify'],
    transform: ['🔄', 'Transform'],
    predict:   ['📝', 'Predict'],
    test:      ['✅', 'Test'],
    explain:   ['💡', 'Explain'],
    observe:   ['👁', 'Observe']
  };

  function verbBar(list) {
    var wrap = el('div', { cls: 'sci-verbs', role: 'list',
      'aria-label': 'Scientific tools used here' });
    (list || []).forEach(function (v) {
      var def = VERBS[v]; if (!def) return;
      wrap.appendChild(el('span', {
        cls: 'sci-verb', role: 'listitem', 'data-verb': v,
        html: '<span class="sci-verb-ico" aria-hidden="true">' + def[0] + '</span>' + esc(def[1])
      }));
    });
    return wrap;
  }
  function verbActive(host, v, on) {
    var n = q(host, '.sci-verb[data-verb="' + v + '"]');
    if (n) n.setAttribute('data-active', on ? '1' : '0');
  }

  /* ------------------------------------------------- the investigation spine */
  /* PHASE 11 — every LAUNCH component says where it sits in the enquiry:
     question → evidence → pattern → explanation → application → evaluation.  */

  var SPINE = ['Question', 'Evidence', 'Pattern', 'Explanation', 'Application', 'Evaluation'];

  function spineBar(at) {
    var wrap = el('div', { cls: 'sci-spine', 'aria-label': 'Where this sits in the investigation' });
    SPINE.forEach(function (s, i) {
      wrap.appendChild(el('span', { text: s, 'data-at': (s.toLowerCase() === String(at).toLowerCase()) ? '1' : '0' }));
      if (i < SPINE.length - 1) wrap.appendChild(el('i', { text: '›', 'aria-hidden': 'true' }));
    });
    return wrap;
  }

  /* --------------------------------------------------------- shell builder */

  function shell(cfg) {
    var host = el('section', {
      cls: 'sci', 'data-sci': cfg.type,
      'aria-label': (cfg.title || 'Scientific investigation') + ' — interactive'
    });
    if (cfg.spine) host.appendChild(spineBar(cfg.spine));
    if (cfg.verbs) host.appendChild(verbBar(cfg.verbs));
    var head = el('div', { cls: 'sci-head' });
    if (cfg.title) head.appendChild(el('h3', { cls: 'sci-title', text: cfg.title }));
    if (cfg.sub) head.appendChild(el('span', { cls: 'sci-sub', text: cfg.sub }));
    if (cfg.title || cfg.sub) host.appendChild(head);
    if (cfg.ask) host.appendChild(el('p', { cls: 'sci-ask', text: cfg.ask }));
    return host;
  }

  /* ======================================================================== *
   * PHASE 5 · THINKING PAUSE
   * ------------------------------------------------------------------------
   * The animation stops. A question is asked. Nothing continues until a
   * prediction is committed. A prediction is deliberately NOT marked right or
   * wrong at the moment it is made — being wrong here is how the evidence
   * afterwards does its work. Marking it would turn the pause into a quiz.
   * ======================================================================== */

  function pauseBlock(spec, onCommit) {
    var box = el('div', { cls: 'sci-pause', role: 'group', 'aria-label': 'Thinking pause' });
    box.appendChild(el('span', { cls: 'sci-pause-tag', text: '⏸ THINKING PAUSE' }));
    box.appendChild(el('p', { cls: 'sci-pause-q', text: spec.ask }));
    var opts = el('div', { cls: 'sci-opts' });
    var committed = false;
    (spec.options || []).forEach(function (o, i) {
      var b = el('button', { cls: 'sci-opt', type: 'button', text: o });
      b.addEventListener('click', function () {
        if (committed) return;
        committed = true;
        b.setAttribute('data-picked', '1');
        qa(opts, '.sci-opt').forEach(function (x) { x.disabled = (x !== b); });
        ding(); xp();
        var after = el('p', { cls: 'sci-pause-after',
          html: '<strong>Your prediction is recorded.</strong> ' + esc(spec.after || 'Now watch — and be ready to say whether the evidence agrees with you.') });
        box.appendChild(after);
        box.appendChild(el('p', { cls: 'sci-pause-note',
          text: 'A prediction that turns out wrong is still good science — it is the thing the evidence has to explain.' }));
        _gate(box, 'prediction committed: ' + o);
        if (onCommit) onCommit(i, o);
      });
      opts.appendChild(b);
    });
    box.appendChild(opts);
    return box;
  }

  SCI.comps.pause = function (cfg) {
    var host = shell({ type: 'pause', title: cfg.title, sub: cfg.sub, ask: cfg.teacherAsk,
      verbs: cfg.verbs || ['predict', 'explain'], spine: cfg.spine || 'Question' });
    host.appendChild(pauseBlock(cfg, function () { verbActive(host, 'predict', 1); }));
    if (cfg.reveal) {
      var rv = el('div', { cls: 'sci-link', 'data-open': '0' });
      rv.appendChild(el('div', { cls: 'sci-link-head',
        html: '<span class="sci-n">💡</span> What actually happens' }));
      rv.appendChild(el('div', { cls: 'sci-link-body', text: cfg.reveal }));
      var btn = el('button', { cls: 'sci-btn', type: 'button', text: '✅ Reveal the evidence', disabled: 'disabled' });
      btn.addEventListener('click', function () {
        rv.setAttribute('data-open', '1'); rv.setAttribute('data-done', '1');
        btn.disabled = true; verbActive(host, 'explain', 1); ding();
      });
      host.appendChild(rv);
      host.appendChild(el('div', { cls: 'sci-btns' }, [btn]));
      host.addEventListener('click', function () {
        if (q(host, '.sci-opt[data-picked="1"]')) btn.disabled = false;
      });
    }
    return host;
  };

  /* ======================================================================== *
   * PHASE 1 · SCIENTIFIC OBSERVATION ENGINE
   * ------------------------------------------------------------------------
   * Image → "What do you notice?" → the pupil marks what they saw → ONLY THEN
   * zoom → spotlight → label. The countdown is a floor, not a ceiling: it
   * stops a class racing to the labels; it never reveals them on its own.
   * ======================================================================== */

  SCI.comps.observe = function (cfg) {
    var host = shell({ type: 'observe', title: cfg.title, sub: cfg.sub,
      ask: cfg.teacherAsk || 'What do you notice? Not what it is called — what you can actually see.',
      verbs: cfg.verbs || ['observe', 'zoom', 'spotlight', 'annotate'],
      spine: cfg.spine || 'Evidence' });

    var need = cfg.noticeTarget || 3;
    var hold = (cfg.holdSeconds == null ? 20 : cfg.holdSeconds);
    var found = 0, elapsed = 0, revealing = false, revealed = 0;

    /* the observation bar: a tally of the pupil's own noticings + a floor timer */
    var bar = el('div', { cls: 'sci-obsbar' });
    bar.appendChild(el('b', { text: '👁 OBSERVE FIRST' }));
    var tally = el('span', { cls: 'sci-count', 'aria-live': 'polite',
      text: '0 / ' + need + ' noticed' });
    bar.appendChild(tally);
    var ring = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    ring.setAttribute('class', 'sci-ring'); ring.setAttribute('viewBox', '0 0 32 32');
    ring.setAttribute('aria-hidden', 'true');
    ring.innerHTML = '<circle class="sci-ring-bg" cx="16" cy="16" r="13"></circle>' +
                     '<circle class="sci-ring-fg" cx="16" cy="16" r="13" stroke-dasharray="81.7" stroke-dashoffset="81.7"></circle>';
    bar.appendChild(ring);
    bar.appendChild(el('span', { cls: 'sci-hint', style: 'color:#cbd5e1',
      text: cfg.hint || 'Tap the picture wherever you notice something.' }));
    host.appendChild(bar);

    /* the figure — carrying no labels at all until they are earned */
    var stage = el('div', { cls: 'sci-stage sci-clickable', role: 'img',
      'aria-label': cfg.alt || 'Scientific image to observe. Labels appear only after you have recorded what you notice.' });
    stage.innerHTML = sceneOf(cfg.scene, bare(cfg.sceneOpts));
    var spot = el('div', { cls: 'sci-spot', 'data-on': '0' });
    stage.appendChild(spot);
    host.appendChild(stage);

    var hotspots = cfg.hotspots || [];
    var labelNodes = hotspots.map(function (h) {
      var n = el('div', { cls: 'sci-label g-in', 'data-shown': '0', text: h.label });
      n.style.left = h.x + '%'; n.style.top = h.y + '%';
      n.style.transform = 'translate(-50%,-140%)';
      stage.appendChild(n);
      return n;
    });

    var noteWrap = el('p', { cls: 'sci-hint', 'aria-live': 'polite',
      text: 'Nothing is named yet. That is deliberate — name what you can see in your own words first.' });
    host.appendChild(noteWrap);

    var goBtn = el('button', { cls: 'sci-btn', type: 'button',
      text: '🔍 I have looked — zoom in', disabled: 'disabled' });
    var nextBtn = el('button', { cls: 'sci-btn sci-ghost', type: 'button',
      text: '🎯 Spotlight the next part', disabled: 'disabled' });
    var resetBtn = el('button', { cls: 'sci-btn sci-ghost', type: 'button', text: '↺ Clear my marks' });
    host.appendChild(el('div', { cls: 'sci-btns' }, [goBtn, nextBtn, resetBtn]));

    function refresh() {
      tally.textContent = found + ' / ' + need + ' noticed';
      var ok = (found >= need) && (elapsed >= hold);
      goBtn.disabled = !ok || revealing;
      if (!ok && !revealing) {
        goBtn.textContent = found < need
          ? '🔍 Mark ' + (need - found) + ' more thing' + ((need - found) === 1 ? '' : 's')
          : '🔍 Keep looking — ' + Math.ceil(hold - elapsed) + 's';
      } else if (!revealing) {
        goBtn.textContent = '🔍 I have looked — zoom in';
      }
    }

    stage.addEventListener('click', function (ev) {
      if (revealing) return;
      var r = stage.getBoundingClientRect();
      var x = ((ev.clientX - r.left) / r.width) * 100;
      var y = ((ev.clientY - r.top) / r.height) * 100;
      found++;
      var m = el('div', { cls: 'sci-notice', text: String(found) });
      m.style.left = x + '%'; m.style.top = y + '%';
      stage.appendChild(m);
      ding(); verbActive(host, 'observe', 1);
      refresh();
    });

    var tick = setInterval(function () {
      elapsed++;
      var fg = q(ring, '.sci-ring-fg');
      if (fg) fg.setAttribute('stroke-dashoffset', String(81.7 * (1 - clamp(elapsed / hold, 0, 1))));
      refresh();
      if (elapsed >= hold + 600) clearInterval(tick);
    }, 1000);

    /* PHASE 12 — the spotlight travels; it does not cut. Movement is what tells
       the class the parts belong to one specimen rather than to a list. */
    function spotlightTo(h, then) {
      spot.setAttribute('data-on', '1');
      spot.style.background =
        'radial-gradient(circle at ' + h.x + '% ' + h.y + '%,rgba(15,23,42,0) 0,' +
        'rgba(15,23,42,0) ' + (h.r || 52) + 'px,rgba(15,23,42,.58) ' + ((h.r || 52) + 68) + 'px)';
      setTimeout(then, REDUCED ? 10 : 620);
    }

    goBtn.addEventListener('click', function () {
      if (goBtn.disabled) return;
      revealing = true;
      _gate(host, 'observed ' + found + ' features over ' + elapsed + 's');
      verbActive(host, 'zoom', 1);
      noteWrap.textContent = 'Now you have looked — one part at a time. Say what it might do BEFORE the name appears.';
      stage.classList.remove('sci-clickable');
      goBtn.disabled = true; goBtn.textContent = '✓ Observation recorded';
      nextBtn.disabled = false;
      xp();
    });

    nextBtn.addEventListener('click', function () {
      if (revealed >= hotspots.length) return;
      var h = hotspots[revealed];
      nextBtn.disabled = true;
      verbActive(host, 'spotlight', 1);
      /* A spotlight that lands off-screen teaches nothing — bring the figure
         into view before lighting up part of it. */
      try { stage.scrollIntoView({ block: 'nearest', behavior: REDUCED ? 'auto' : 'smooth' }); } catch (e) {}
      spotlightTo(h, function () {
        labelNodes[revealed].setAttribute('data-shown', '1');
        keepInside(stage, labelNodes[revealed]);
        verbActive(host, 'annotate', 1);
        if (h.note) noteWrap.textContent = h.note;
        ding(); xp();
        revealed++;
        if (revealed >= hotspots.length) {
          nextBtn.textContent = '✓ All parts named';
          spot.setAttribute('data-on', '0');
          noteWrap.textContent = cfg.closing ||
            'Compare the names with the marks you made. Which of your noticings turned out to matter?';
        } else {
          nextBtn.disabled = false;
        }
      });
    });

    resetBtn.addEventListener('click', function () {
      qa(stage, '.sci-notice').forEach(function (n) { n.remove(); });
      found = 0; refresh();
    });

    refresh();
    return host;
  };

  /* ======================================================================== *
   * PHASE 2 · PROGRESSIVE SCIENTIFIC DISCOVERY
   * ------------------------------------------------------------------------
   * The diagram is assembled part by part, and each part is preceded by a
   * question about what is still missing. The pupil builds the model; they do
   * not receive it finished.
   * ======================================================================== */

  SCI.comps.discover = function (cfg) {
    var host = shell({ type: 'discover', title: cfg.title, sub: cfg.sub, ask: cfg.teacherAsk,
      verbs: cfg.verbs || ['observe', 'predict', 'annotate'], spine: cfg.spine || 'Evidence' });

    var stage = el('div', { cls: 'sci-stage', role: 'img',
      'aria-label': cfg.alt || 'A diagram built one part at a time.' });
    stage.innerHTML = sceneOf(cfg.scene, bare(cfg.sceneOpts));
    host.appendChild(stage);

    /* hide every part that the pupil has not yet asked for */
    var steps = cfg.steps || [];
    steps.forEach(function (s) {
      (s.parts || []).forEach(function (id) {
        var g = q(stage, '#' + id);
        if (g) { g.setAttribute('class', ((g.getAttribute('class') || '') + ' sci-part').trim()); g.setAttribute('data-built', '0'); }
      });
    });

    var strip = el('div', { cls: 'sci-steps' });
    steps.forEach(function (s, i) {
      strip.appendChild(el('span', { cls: 'sci-step', text: (i + 1) + '. ' + s.name, 'data-done': '0', 'data-now': i === 0 ? '1' : '0' }));
    });
    host.appendChild(strip);

    var askBox = el('div');
    host.appendChild(askBox);

    var labels = el('div');
    host.appendChild(labels);

    var i = 0;
    var btn = el('button', { cls: 'sci-btn', type: 'button', text: '▶ ' + (steps[0] ? steps[0].name : 'Begin') });
    var lblBtn = el('button', { cls: 'sci-btn sci-ghost', type: 'button', text: '✏️ Now add the labels', disabled: 'disabled' });
    host.appendChild(el('div', { cls: 'sci-btns' }, [btn, lblBtn,
      el('span', { cls: 'sci-hint', text: 'Labels come last — after the whole thing is built.' })]));

    function build(step) {
      (step.parts || []).forEach(function (id) {
        var g = q(stage, '#' + id);
        if (g) { g.setAttribute('data-built', '1'); g.classList.add('g-draw-pop'); }
      });
      ding(); xp();
    }

    btn.addEventListener('click', function () {
      var step = steps[i]; if (!step) return;
      btn.disabled = true;
      askBox.innerHTML = '';
      if (step.ask) {
        /* PHASE 5 woven in — a question before every reveal, not after it */
        askBox.appendChild(pauseBlock(
          { ask: step.ask, options: step.options || ['I have an idea', 'Not sure yet'],
            after: step.after || 'Watch what gets added.' },
          function () { proceed(step); }));
      } else { proceed(step); }
    });

    function proceed(step) {
      build(step);
      qa(strip, '.sci-step').forEach(function (n, k) {
        n.setAttribute('data-done', k <= i ? '1' : '0');
        n.setAttribute('data-now', k === i + 1 ? '1' : '0');
      });
      i++;
      if (i < steps.length) {
        btn.disabled = false; btn.textContent = '▶ ' + steps[i].name;
      } else {
        btn.textContent = '✓ Model complete'; lblBtn.disabled = false;
        _gate(host, 'model assembled in ' + steps.length + ' steps');
      }
    }

    lblBtn.addEventListener('click', function () {
      (cfg.labels || []).forEach(function (L, k) {
        var n = el('div', { cls: 'sci-label g-in', text: L.label, 'data-shown': '0' });
        n.style.left = L.x + '%'; n.style.top = L.y + '%';
        n.style.transform = 'translate(-50%,-140%)';
        stage.appendChild(n);
        setTimeout(function () { n.setAttribute('data-shown', '1'); keepInside(stage, n); }, REDUCED ? 0 : k * 260);
      });
      lblBtn.disabled = true; lblBtn.textContent = '✓ Labelled';
      ding(); xp();
    });

    return host;
  };

  /* ======================================================================== *
   * PHASE 3 · ZOOM FRAMEWORK  — the signature LAUNCH interaction
   * ------------------------------------------------------------------------
   * Leaf → cells → chloroplast → membrane → molecules, as ONE continuous
   * movement. Changing slides teaches "next topic". Zooming teaches scale.
   * The scale readout and the field-of-view rule move with it, so the pupil
   * can see the price of magnification while it is being paid.
   * ======================================================================== */

  SCI.comps.zoom = function (cfg) {
    var host = shell({ type: 'zoom', title: cfg.title, sub: cfg.sub,
      ask: cfg.teacherAsk || 'We are not changing picture — we are going further in. What is getting smaller?',
      verbs: cfg.verbs || ['zoom', 'measure', 'observe'], spine: cfg.spine || 'Evidence' });

    var levels = cfg.levels || [];
    var Z = cfg.factor || 7;                                   /* scale per level */
    var stage = el('div', { cls: 'sci-zoomstage', role: 'img',
      'aria-label': cfg.alt || 'One continuous zoom from ' + (levels[0] || {}).name + ' to ' + (levels[levels.length - 1] || {}).name });
    stage.style.aspectRatio = '16 / 9';
    host.appendChild(stage);

    var layers = levels.map(function (L, i) {
      var d = el('div', { cls: 'sci-layer' });
      d.innerHTML = sceneOf(L.scene, L.sceneOpts);
      d.style.zIndex = String(10 + i);
      stage.appendChild(d);
      return d;
    });

    /* Two readouts, each with a data-role so they are addressable: what you are
       looking AT, and how big the field of view now is. Both must move together
       — that pairing is what makes the cost of magnification visible. */
    var scaleRow = el('div', { cls: 'sci-scalebar' });
    var scaleName = el('span', { cls: 'sci-scalabel', 'data-role': 'level-name', text: (levels[0] || {}).name || '' });
    var rule = el('span', { cls: 'sci-rule', style: 'width:120px' });
    var scaleTxt = el('span', { cls: 'sci-scalabel', 'data-role': 'level-scale', text: (levels[0] || {}).scale || '' });
    scaleRow.appendChild(el('span', { text: '🔍 Now looking at' }));
    scaleRow.appendChild(scaleName);
    scaleRow.appendChild(el('span', { text: '· how much you can see' }));
    scaleRow.appendChild(rule);
    scaleRow.appendChild(el('span', { text: '· roughly' }));
    scaleRow.appendChild(scaleTxt);
    host.appendChild(scaleRow);

    var slider = el('input', { cls: 'sci-slider', type: 'range', min: '0',
      max: String(Math.max(0, levels.length - 1) * 100), value: '0', step: '1',
      'aria-label': 'Zoom depth' });
    host.appendChild(slider);

    var msg = el('p', { cls: 'sci-hint', 'aria-live': 'polite',
      text: 'Drag, or press ▶. Stop whenever you can name what you are looking at.' });
    host.appendChild(msg);

    var playBtn = el('button', { cls: 'sci-btn', type: 'button', text: '▶ Zoom in one level' });
    var outBtn = el('button', { cls: 'sci-btn sci-ghost', type: 'button', text: '◀ Back out' });
    var pauseHost = el('div');
    host.appendChild(el('div', { cls: 'sci-btns' }, [playBtn, outBtn]));
    host.appendChild(pauseHost);

    var t = 0, animating = false;

    function render() {
      layers.forEach(function (d, i) {
        var dd = t - i;
        var s = Math.pow(Z, dd);
        var o = clamp(1.25 - Math.abs(dd) * 1.15, 0, 1);
        if (Math.abs(dd) > 1.35) { d.style.display = 'none'; return; }
        d.style.display = 'flex';
        d.style.opacity = String(o);
        d.style.transform = 'scale(' + s.toFixed(4) + ')';
      });
      var k = clamp(Math.round(t), 0, levels.length - 1);
      var L = levels[k] || {};
      scaleName.textContent = L.name || '';
      scaleTxt.textContent = L.scale || '';
      /* the rule shrinks as magnification climbs — the trade-off, made visible */
      rule.style.width = Math.max(8, 130 / Math.pow(1.9, t)).toFixed(1) + 'px';
    }

    function glide(to, done) {
      to = clamp(to, 0, levels.length - 1);
      if (REDUCED) { t = to; render(); if (done) done(); return; }
      animating = true;
      var from = t, t0 = null, dur = 900;
      function step(ts) {
        if (t0 === null) t0 = ts;
        var p = clamp((ts - t0) / dur, 0, 1);
        var e = p < .5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;   /* easeInOutQuad */
        t = from + (to - from) * e;
        slider.value = String(Math.round(t * 100));
        render();
        if (p < 1) requestAnimationFrame(step);
        else { animating = false; if (done) done(); }
      }
      requestAnimationFrame(step);
    }

    function askAt(k) {
      /* PHASE 5 — the zoom stops at each level and asks before going deeper */
      var L = levels[k];
      pauseHost.innerHTML = '';
      if (!L || !L.ask) return;
      pauseHost.appendChild(pauseBlock(
        { ask: L.ask, options: L.options || ['Smaller structures', 'The same thing again', 'Something new'],
          after: L.after || 'Go one level deeper and check.' },
        function () { playBtn.disabled = false; }));
      playBtn.disabled = true;
    }

    playBtn.addEventListener('click', function () {
      if (animating) return;
      var to = Math.min(levels.length - 1, Math.round(t) + 1);
      if (to === Math.round(t)) { msg.textContent = 'That is as far in as this journey goes.'; return; }
      verbActive(host, 'zoom', 1); verbActive(host, 'measure', 1);
      glide(to, function () {
        ding(); xp();
        var L = levels[to] || {};
        msg.textContent = L.note || ('Now at: ' + (L.name || ''));
        if (to === levels.length - 1) {
          playBtn.textContent = '✓ Deepest level';
          playBtn.disabled = true;
          _gate(host, 'zoomed through ' + levels.length + ' scale levels');
        } else { askAt(to); }
      });
    });

    outBtn.addEventListener('click', function () {
      if (animating) return;
      glide(Math.max(0, Math.round(t) - 1), function () {
        playBtn.disabled = false; playBtn.textContent = '▶ Zoom in one level';
        msg.textContent = 'Backed out. The specimen has not changed — only how much of it you can see.';
      });
    });

    slider.addEventListener('input', function () {
      if (animating) return;
      t = clamp(parseFloat(slider.value) / 100, 0, levels.length - 1);
      render();
    });

    render();
    return host;
  };

  /* ======================================================================== *
   * PHASE 4 · SCIENTIFIC INVESTIGATION ANIMATION
   * ------------------------------------------------------------------------
   * The practical is animated rather than described. The pupil watches the
   * method happen — including the bit that goes wrong (the blur before the
   * sharpen), because the recovery is the skill.
   * ======================================================================== */

  SCI.comps.method = function (cfg) {
    var host = shell({ type: 'method', title: cfg.title, sub: cfg.sub,
      ask: cfg.teacherAsk || 'Watch the order. Which step could you not swap with the one before it?',
      verbs: cfg.verbs || ['simulate', 'observe', 'predict'], spine: cfg.spine || 'Evidence' });

    var grid = el('div', { cls: 'sci-method' });
    var stage = el('div', { cls: 'sci-stage', role: 'img',
      'aria-label': cfg.alt || 'An animated laboratory method.' });
    stage.innerHTML = sceneOf(cfg.scene, cfg.sceneOpts);
    grid.appendChild(stage);

    /* everything the method will reveal starts hidden */
    function hideParts() {
      (cfg.steps || []).forEach(function (st) {
        (st.parts || []).forEach(function (id) {
          var g = q(stage, '#' + id);
          if (g) { g.setAttribute('class', ((g.getAttribute('class') || '') + ' sci-part').trim()); g.setAttribute('data-built', '0'); }
        });
      });
    }
    hideParts();

    var list = el('ol', { cls: 'sci-methodlist' });
    (cfg.steps || []).forEach(function (s, i) {
      list.appendChild(el('li', { text: (i + 1) + '. ' + s.label, 'data-state': i === 0 ? 'now' : 'wait' }));
    });
    grid.appendChild(list);
    host.appendChild(grid);

    var pauseHost = el('div'); host.appendChild(pauseHost);
    var note = el('p', { cls: 'sci-hint', 'aria-live': 'polite', text: cfg.opening || 'Press play and watch — do not write yet.' });
    host.appendChild(note);

    var i = 0;
    var btn = el('button', { cls: 'sci-btn', type: 'button', text: '▶ Next step' });
    var again = el('button', { cls: 'sci-btn sci-ghost', type: 'button', text: '↺ Watch again' });
    host.appendChild(el('div', { cls: 'sci-btns' }, [btn, again]));

    function apply(step) {
      /* A step reveals named parts of the scene — the same contract `discover`
         uses. `state` is also written to the root svg for any scene that wants
         to restyle wholesale, but parts are what make the method visible. */
      (step.parts || []).forEach(function (id) {
        var g = q(stage, '#' + id);
        if (g) { g.setAttribute('data-built', '1'); g.classList.add('g-draw-pop'); }
      });
      stage.firstElementChild && stage.firstElementChild.setAttribute('data-state', step.state || '');
      if (step.blur != null) {
        var f = q(stage, '.sci-optics-blur');
        if (f) f.style.filter = step.blur ? ('blur(' + step.blur + 'px)') : 'none';
      }
      note.textContent = step.note || '';
      ding();
    }

    /* Paint AFTER the index has advanced. Painting with the pre-increment index
       leaves the step just performed showing as "now" and the final step never
       reaching "done" — the list then lags the animation by one the whole way. */
    function paint() {
      qa(list, 'li').forEach(function (n, k) {
        n.setAttribute('data-state', k < i ? 'done' : k === i ? 'now' : 'wait');
      });
    }

    btn.addEventListener('click', function () {
      var step = (cfg.steps || [])[i]; if (!step) return;
      btn.disabled = true; pauseHost.innerHTML = '';
      function go() {
        apply(step); xp();
        i++;
        paint();
        if (i >= (cfg.steps || []).length) {
          btn.textContent = '✓ Method complete';
          _gate(host, 'watched the full method');
          note.textContent = cfg.closing || 'Now write the method in your own words — in the order you just saw.';
        } else { btn.disabled = false; btn.textContent = '▶ ' + (cfg.steps[i].label || 'Next step'); }
      }
      if (step.ask) {
        pauseHost.appendChild(pauseBlock({ ask: step.ask, options: step.options || ['Yes', 'No', 'Not sure'],
          after: step.after || 'Watch and check.' }, go));
      } else { go(); }
    });

    again.addEventListener('click', function () {
      i = 0; pauseHost.innerHTML = '';
      stage.innerHTML = sceneOf(cfg.scene, cfg.sceneOpts);
      hideParts();
      paint();
      btn.disabled = false; btn.textContent = '▶ Next step';
      note.textContent = cfg.opening || 'Press play and watch — do not write yet.';
    });

    return host;
  };

  /* ======================================================================== *
   * PHASE 6 · EVIDENCE BEFORE EXPLANATION
   * ------------------------------------------------------------------------
   * Observe → Evidence → Pattern → Conclusion → Explanation, each locked
   * behind the one before it. The explanation is physically unreachable until
   * the pattern has been stated. That ordering is the whole point.
   * ======================================================================== */

  SCI.comps.chain = function (cfg) {
    var host = shell({ type: 'chain', title: cfg.title, sub: cfg.sub,
      ask: cfg.teacherAsk || 'We are not allowed the explanation yet. What does the evidence actually show?',
      verbs: cfg.verbs || ['observe', 'compare', 'explain'], spine: cfg.spine || 'Pattern' });

    var wrap = el('div', { cls: 'sci-chain' });
    var stages = cfg.stages || [];
    var nodes = stages.map(function (s, i) {
      var n = el('div', { cls: 'sci-link', 'data-open': i === 0 ? '1' : '0' });
      n.appendChild(el('div', { cls: 'sci-link-head',
        html: '<span class="sci-n">' + (i + 1) + '</span>' + esc(s.title) }));
      var body = el('div', { cls: 'sci-link-body' });
      body.innerHTML = '<p>' + esc(s.body) + '</p>';
      if (s.prompt) body.appendChild(el('p', { cls: 'sci-hint', text: s.prompt }));
      n.appendChild(body);
      if (i > 0) n.appendChild(el('p', { cls: 'sci-link-lock', text: '🔒 Locked until step ' + i + ' is done.' }));
      wrap.appendChild(n);
      return n;
    });
    host.appendChild(wrap);

    var i = 0;
    var btn = el('button', { cls: 'sci-btn', type: 'button',
      text: '✅ ' + (stages[0] ? (stages[0].action || 'We have done this — unlock the next step') : 'Next') });
    host.appendChild(el('div', { cls: 'sci-btns' }, [btn,
      el('span', { cls: 'sci-hint', text: 'The explanation is the last thing you are allowed, not the first.' })]));

    btn.addEventListener('click', function () {
      nodes[i].setAttribute('data-done', '1');
      var lock = q(nodes[i], '.sci-link-lock'); if (lock) lock.remove();
      i++;
      if (i < nodes.length) {
        nodes[i].setAttribute('data-open', '1');
        var l2 = q(nodes[i], '.sci-link-lock'); if (l2) l2.remove();
        _gate(nodes[i], 'previous stage completed');
        btn.textContent = '✅ ' + (stages[i].action || 'We have done this — unlock the next step');
        nodes[i].scrollIntoView({ block: 'nearest', behavior: REDUCED ? 'auto' : 'smooth' });
        ding(); xp();
      } else {
        btn.disabled = true; btn.textContent = '✓ Full chain built';
        _gate(host, 'evidence chain completed in order');
      }
    });

    return host;
  };

  /* ======================================================================== *
   * PHASE 7 · DATA VISUALISATION
   * ------------------------------------------------------------------------
   * Bars grow, the table fills a row at a time, the axis rescales when the
   * data demands it. Pupils are asked to read the trend BEFORE the last point
   * is plotted, so the graph is a prediction instrument, not a picture.
   * ======================================================================== */

  function plotSVG(cfg, upTo) {
    var W = 460, H = 250, P = { l: 52, r: 14, t: 16, b: 42 };
    var pts = (cfg.points || []).slice(0, upTo);
    var all = cfg.points || [];
    var xs = all.map(function (p) { return p.x; });
    var ysAll = all.map(function (p) { return p.y; });
    /* the axis only knows about the data plotted so far — it rescales live */
    var yMaxNow = Math.max.apply(null, pts.length ? pts.map(function (p) { return p.y; }) : [1]);
    var yMin = cfg.yMin != null ? cfg.yMin : Math.min(0, Math.min.apply(null, ysAll.concat([0])));
    var yMax = cfg.fixedAxis ? Math.max.apply(null, ysAll) : Math.max(yMaxNow, yMin + 1);
    yMax = yMax + (yMax - yMin) * 0.12;
    var xMin = Math.min.apply(null, xs), xMax = Math.max.apply(null, xs);
    if (xMax === xMin) xMax = xMin + 1;
    function X(v) { return P.l + (v - xMin) / (xMax - xMin) * (W - P.l - P.r); }
    function Y(v) { return H - P.b - (v - yMin) / (yMax - yMin) * (H - P.t - P.b); }

    var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" width="100%" role="img" aria-label="' +
      esc(cfg.alt || cfg.title || 'Graph of results') + '" xmlns="http://www.w3.org/2000/svg">';
    for (var g = 0; g <= 4; g++) {
      var yv = yMin + (yMax - yMin) * g / 4;
      s += '<line class="sci-gridline" x1="' + P.l + '" y1="' + Y(yv).toFixed(1) + '" x2="' + (W - P.r) + '" y2="' + Y(yv).toFixed(1) + '"/>';
      s += '<text x="' + (P.l - 6) + '" y="' + (Y(yv) + 4).toFixed(1) + '" text-anchor="end">' + (Math.round(yv * 10) / 10) + '</text>';
    }
    s += '<line class="sci-axis" x1="' + P.l + '" y1="' + P.t + '" x2="' + P.l + '" y2="' + (H - P.b) + '"/>';
    s += '<line class="sci-axis" x1="' + P.l + '" y1="' + (H - P.b) + '" x2="' + (W - P.r) + '" y2="' + (H - P.b) + '"/>';
    s += '<text x="' + (P.l + (W - P.l - P.r) / 2) + '" y="' + (H - 8) + '" text-anchor="middle" font-weight="700">' + esc(cfg.xLabel || '') + '</text>';
    s += '<text transform="translate(13,' + (P.t + (H - P.t - P.b) / 2) + ') rotate(-90)" text-anchor="middle" font-weight="700">' + esc(cfg.yLabel || '') + '</text>';

    if (cfg.plot === 'bar') {
      var bw = (W - P.l - P.r) / Math.max(1, all.length) * 0.62;
      all.forEach(function (p, i) {
        var cx = P.l + (W - P.l - P.r) * (i + 0.5) / all.length;
        var shown = i < upTo;
        var y = shown ? Y(p.y) : Y(yMin), h = shown ? (Y(yMin) - Y(p.y)) : 0;
        s += '<rect class="sci-bar" x="' + (cx - bw / 2).toFixed(1) + '" y="' + y.toFixed(1) +
             '" width="' + bw.toFixed(1) + '" height="' + Math.max(0, h).toFixed(1) +
             '" rx="3" fill="' + (p.colour || '#7A5C9E') + '" opacity="' + (shown ? 1 : 0) + '"/>';
        s += '<text x="' + cx.toFixed(1) + '" y="' + (H - P.b + 15) + '" text-anchor="middle">' + esc(p.label != null ? p.label : p.x) + '</text>';
      });
    } else {
      var d = pts.map(function (p, i) { return (i ? 'L' : 'M') + X(p.x).toFixed(1) + ' ' + Y(p.y).toFixed(1); }).join(' ');
      if (d) s += '<path class="sci-trace" d="' + d + '"/>';
      pts.forEach(function (p) {
        s += '<circle cx="' + X(p.x).toFixed(1) + '" cy="' + Y(p.y).toFixed(1) + '" r="4.5" fill="#7A5C9E" stroke="#fff" stroke-width="1.6"/>';
      });
      all.forEach(function (p, i) {
        if (i % Math.ceil(all.length / 6) === 0 || i === all.length - 1) {
          s += '<text x="' + X(p.x).toFixed(1) + '" y="' + (H - P.b + 15) + '" text-anchor="middle">' + esc(p.label != null ? p.label : p.x) + '</text>';
        }
      });
      if (cfg.zeroLine) s += '<line class="sci-gridline" stroke="#dc2626" stroke-dasharray="4 3" x1="' + P.l + '" y1="' + Y(0).toFixed(1) + '" x2="' + (W - P.r) + '" y2="' + Y(0).toFixed(1) + '"/>';
    }
    return s + '</svg>';
  }

  SCI.comps.graph = function (cfg) {
    var host = shell({ type: 'graph', title: cfg.title, sub: cfg.sub,
      ask: cfg.teacherAsk || 'Before the last point goes on — where is it going to land, and why?',
      verbs: cfg.verbs || ['graph', 'measure', 'predict'], spine: cfg.spine || 'Pattern' });

    var plot = el('div', { cls: 'sci-plot' });
    host.appendChild(plot);

    var tbl = el('table', { cls: 'sci-table' });
    var head = el('tr');
    head.appendChild(el('th', { text: cfg.xLabel || 'x' }));
    head.appendChild(el('th', { text: cfg.yLabel || 'y' }));
    tbl.appendChild(head);
    host.appendChild(tbl);

    var pauseHost = el('div'); host.appendChild(pauseHost);
    var note = el('p', { cls: 'sci-hint', 'aria-live': 'polite', text: cfg.opening || 'No data yet. Add one result at a time.' });
    host.appendChild(note);

    var n = 0;
    var pts = cfg.points || [];
    var addBtn = el('button', { cls: 'sci-btn', type: 'button', text: '📊 Plot the next result' });
    var allBtn = el('button', { cls: 'sci-btn sci-ghost', type: 'button', text: '⏭ Plot the rest' });
    host.appendChild(el('div', { cls: 'sci-btns' }, [addBtn, allBtn]));
    if (cfg.caveat) host.appendChild(el('p', { cls: 'sci-caveat', text: cfg.caveat }));

    function draw() { plot.innerHTML = plotSVG(cfg, n); }

    function addRow(p) {
      var tr = el('tr', { cls: 'sci-row-new' });
      tr.appendChild(el('td', { text: String(p.label != null ? p.label : p.x) }));
      tr.appendChild(el('td', { text: String(p.y) }));
      tbl.appendChild(tr);
    }

    function step() {
      if (n >= pts.length) return false;
      var p = pts[n];
      n++;
      draw(); addRow(p); ding(); xp();
      note.textContent = p.note || (n + ' of ' + pts.length + ' results plotted.');
      verbActive(host, 'graph', 1);
      /* PHASE 5 — the pause lands before the final point, where prediction is
         a real risk rather than a formality */
      if (cfg.predictBefore && n === pts.length - 1) {
        addBtn.disabled = true;
        pauseHost.innerHTML = '';
        pauseHost.appendChild(pauseBlock({ ask: cfg.predictBefore.ask,
          options: cfg.predictBefore.options || ['Higher', 'About the same', 'Lower'],
          after: 'Plot it and see.' }, function () { addBtn.disabled = false; }));
      }
      if (n >= pts.length) {
        addBtn.disabled = true; addBtn.textContent = '✓ All results plotted';
        allBtn.disabled = true;
        note.textContent = cfg.closing || 'Describe the pattern in one sentence — using numbers from the table.';
        _gate(host, 'all ' + pts.length + ' results plotted');
      }
      return true;
    }

    addBtn.addEventListener('click', function () { if (!addBtn.disabled) step(); });
    /* "plot the rest" stops dead at the prediction pause rather than skating
       past it — the pause is the point of the component, not an obstacle. */
    allBtn.addEventListener('click', function () {
      var guard = 0;
      while (n < pts.length && !addBtn.disabled && guard++ < 200) { step(); }
    });

    draw();
    return host;
  };

  /* ======================================================================== *
   * PHASE 8/9 · INTERACTIVE SCIENTIFIC MODELS + REASONING ANIMATIONS
   * ------------------------------------------------------------------------
   * The pupil moves a variable; the model answers honestly, including when the
   * answer is "worse". A simulator that only ever improves teaches nothing —
   * the trade-off IS the science.
   * ======================================================================== */

  SCI.comps.model = function (cfg) {
    var sim = SCI.sims[cfg.sim];
    var host = shell({ type: 'model', title: cfg.title, sub: cfg.sub,
      ask: cfg.teacherAsk, verbs: cfg.verbs || ['simulate', 'measure', 'observe', 'explain'],
      spine: cfg.spine || 'Explanation' });
    if (!sim) {
      host.appendChild(el('p', { cls: 'sci-caveat', text: 'Model "' + cfg.sim + '" is not available in this deck.' }));
      return host;
    }

    var stage = el('div', { cls: 'sci-stage', role: 'img',
      'aria-label': cfg.alt || (cfg.title + ' — interactive model') });
    host.appendChild(stage);

    var readout = el('div', { cls: 'sci-readout', 'aria-live': 'polite' });
    host.appendChild(readout);

    var controls = el('div', { cls: 'sci-controls' });
    host.appendChild(controls);

    var note = el('p', { cls: 'sci-hint', 'aria-live': 'polite', text: cfg.opening || '' });
    host.appendChild(note);

    var state = {};
    (sim.params || []).forEach(function (p) { state[p.key] = (cfg.start && cfg.start[p.key] != null) ? cfg.start[p.key] : p.value; });

    function update(changedKey) {
      var out = sim.render(state, cfg);
      stage.innerHTML = out.svg;
      readout.innerHTML = (out.readout || []).map(function (r) {
        return '<span>' + esc(r[0]) + ' <b>' + esc(r[1]) + '</b></span>';
      }).join('');
      if (changedKey && out.note) note.textContent = out.note;
      verbActive(host, 'simulate', 1);
    }

    (sim.params || []).forEach(function (p) {
      var box = el('div', { cls: 'sci-ctl' });
      if (p.type === 'choice') {
        box.appendChild(el('label', { text: p.label }));
        var row = el('div', { cls: 'sci-turret' });
        p.options.forEach(function (o) {
          var b = el('button', { type: 'button', text: o.label, 'aria-pressed': String(state[p.key] === o.value) });
          var paidChoice = false;
          b.addEventListener('click', function () {
            state[p.key] = o.value;
            qa(row, 'button').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
            ding(); if (!paidChoice) { paidChoice = true; xp(); } update(p.key);
          });
          row.appendChild(b);
        });
        box.appendChild(row);
      } else {
        var lab = el('label', { html: esc(p.label) + '<span class="sci-val" id="v-' + p.key + '"></span>' });
        box.appendChild(lab);
        var inp = el('input', { type: 'range', min: String(p.min), max: String(p.max),
          step: String(p.step || 1), value: String(state[p.key]), 'aria-label': p.label });
        inp.addEventListener('input', function () {
          state[p.key] = parseFloat(inp.value);
          var v = q(box, '.sci-val'); if (v) v.textContent = (p.fmt ? p.fmt(state[p.key]) : state[p.key]);
          update(p.key);
        });
        /* one award per control, not one per drag — see declareXP() */
        var paid = false;
        inp.addEventListener('change', function () { ding(); if (!paid) { paid = true; xp(); } });
        box.appendChild(inp);
        setTimeout(function () {
          var v = q(box, '.sci-val'); if (v) v.textContent = (p.fmt ? p.fmt(state[p.key]) : state[p.key]);
        }, 0);
      }
      controls.appendChild(box);
    });

    /* PHASE 9 — the trade-off is asked about, never stated first */
    if (cfg.tradeOff) {
      host.appendChild(pauseBlock({ ask: cfg.tradeOff.ask,
        options: cfg.tradeOff.options, after: cfg.tradeOff.after ||
          'Now go back to the model and change only that one thing. Watch what you lose.' },
        function () { _gate(host, 'trade-off predicted'); }));
    }
    if (cfg.caveat) host.appendChild(el('p', { cls: 'sci-caveat', text: cfg.caveat }));

    update(null);
    return host;
  };

  /* ======================================================================== *
   * PHASE 10 · COMPARATIVE INVESTIGATION
   * ------------------------------------------------------------------------
   * Two panels, driven by ONE control, so a difference cannot be an artefact
   * of the pupil looking at them at different moments. Differences are found
   * by the class and ticked off; the explanation box opens only when they are
   * all found.
   * ======================================================================== */

  SCI.comps.compare = function (cfg) {
    var host = shell({ type: 'compare', title: cfg.title, sub: cfg.sub,
      ask: cfg.teacherAsk || 'Same specimen, one thing changed. Find every difference before anyone explains one.',
      verbs: cfg.verbs || ['compare', 'observe', 'explain'], spine: cfg.spine || 'Pattern' });

    var grid = el('div', { cls: 'sci-compare' });
    var panels = (cfg.panels || []).map(function (p) {
      var d = el('div', { cls: 'sci-panel' });
      d.appendChild(el('span', { cls: 'sci-panel-label', text: p.label }));
      var inner = el('div', { cls: 'sci-stage', role: 'img', 'aria-label': p.alt || p.label });
      inner.innerHTML = sceneOf(p.scene, p.sceneOpts);
      d.appendChild(inner);
      grid.appendChild(d);
      return inner;
    });
    host.appendChild(grid);

    /* One control, both panels — synchronised by construction rather than by
       the pupil trying to move two sliders together. A difference they see is
       then a difference in the science, not in when they looked. */
    if (cfg.sync) {
      var syncBox = el('div', { cls: 'sci-ctl' });
      var unit = cfg.sync.unit || '';
      syncBox.appendChild(el('label', { html: esc(cfg.sync.label) + '<span class="sci-val"></span>' }));
      var inp = el('input', { type: 'range', min: String(cfg.sync.min), max: String(cfg.sync.max),
        step: String(cfg.sync.step || 1), value: String(cfg.sync.value), 'aria-label': cfg.sync.label });
      function syncTo(v) {
        var lab = q(syncBox, '.sci-val'); if (lab) lab.textContent = v + unit;
        (cfg.panels || []).forEach(function (p, i) {
          var o = {}; for (var k in (p.sceneOpts || {})) o[k] = p.sceneOpts[k];
          o[cfg.sync.key] = v * (p.syncScale == null ? 1 : p.syncScale);
          panels[i].innerHTML = sceneOf(p.scene, o);
        });
      }
      inp.addEventListener('input', function () { syncTo(parseFloat(inp.value)); });
      syncBox.appendChild(inp);
      host.appendChild(syncBox);
      syncTo(parseFloat(cfg.sync.value));
    }

    var diffs = el('div', { cls: 'sci-diffs' });
    var target = (cfg.differences || []).length, got = 0;
    var explain = el('div', { cls: 'sci-link', 'data-open': '0' });
    explain.appendChild(el('div', { cls: 'sci-link-head', html: '<span class="sci-n">💡</span>Now explain it' }));
    var eb = el('div', { cls: 'sci-link-body' });
    eb.innerHTML = '<p>' + esc(cfg.explanation || '') + '</p>';
    explain.appendChild(eb);
    explain.appendChild(el('p', { cls: 'sci-link-lock', text: '🔒 Locked until every difference has been found.' }));

    (cfg.differences || []).forEach(function (d) {
      var b = el('button', { cls: 'sci-diff', type: 'button', text: d.spot, 'data-found': '0' });
      b.addEventListener('click', function () {
        if (b.getAttribute('data-found') === '1') return;
        b.setAttribute('data-found', '1');
        b.classList.add('g-bounce');              /* GROW verb: correct */
        b.textContent = '✓ ' + d.spot;
        if (d.note) b.title = d.note;
        got++; ding(); xp(); verbActive(host, 'compare', 1);
        counter.textContent = got + ' / ' + target + ' differences found';
        if (got >= target) {
          explain.setAttribute('data-open', '1');
          var l = q(explain, '.sci-link-lock'); if (l) l.remove();
          _gate(explain, 'all differences found by the class');
          verbActive(host, 'explain', 1);
        }
      });
      diffs.appendChild(b);
    });
    var counter = el('p', { cls: 'sci-hint', 'aria-live': 'polite', text: '0 / ' + target + ' differences found' });
    host.appendChild(el('p', { cls: 'sci-hint', text: cfg.prompt || 'Tap each difference as the class agrees it is real.' }));
    host.appendChild(diffs);
    host.appendChild(counter);
    host.appendChild(explain);
    if (cfg.caveat) host.appendChild(el('p', { cls: 'sci-caveat', text: cfg.caveat }));
    return host;
  };

  /* ======================================================================== *
   * SCENES — the drawn science. Every scene is a pure function of its options
   * so that a comparison panel and a simulator can share one drawing.
   * ======================================================================== */

  /* `observe` and `discover` withhold names until the pupil has earned them. A
     scene that draws its own captions hands those names straight back — the
     diffusion box literally captioned "more particles here", which is one of
     the things the pupil is asked to notice. So the two withholding components
     force `bare` rather than trusting each payload to remember, and every
     scene that draws text must honour it. check.js asserts that they do. */
  function bare(opts) {
    var o = {}; for (var k in (opts || {})) o[k] = opts[k];
    o.bare = true; return o;
  }

  function sceneOf(name, opts) {
    var fn = SCI.scenes[name];
    if (!fn) return '<svg viewBox="0 0 400 240" width="100%" role="img" aria-label="Diagram unavailable"><rect width="400" height="240" fill="#f1f5f9"/><text x="200" y="124" text-anchor="middle" font-family="system-ui" font-size="13" fill="#64748b">Scene "' + esc(name) + '" not in this deck</text></svg>';
    return fn(opts || {});
  }

  var SVGOPEN = '<svg viewBox="0 0 400 260" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,Segoe UI,sans-serif">';

  /* Every gradient, filter and clipPath id MUST be unique across the document.
     A deck holds several copies of the same scene — two comparison panels plus
     a simulator — and a duplicated id makes `url(#…)` resolve to the FIRST
     match in the document. When that first match sits on a `display:none`
     slide, Chromium silently drops the reference: the field-of-view clip stops
     clipping and cells spill outside the eyepiece circle. This counter is the
     fix; do not hard-code scene ids back in. */
  var UID = 0;
  function uid(p) { UID++; return p + UID; }

  /* --- shared optical furniture (PHASE 12) -------------------------------- */
  function defsOptics(id) {
    return '<defs>' +
      '<radialGradient id="' + id + '-beam" cx="50%" cy="50%" r="50%">' +
        '<stop offset="0%" stop-color="#fff8dc" stop-opacity=".95"/>' +
        '<stop offset="70%" stop-color="#fde68a" stop-opacity=".35"/>' +
        '<stop offset="100%" stop-color="#fde68a" stop-opacity="0"/></radialGradient>' +
      '<radialGradient id="' + id + '-glint" cx="32%" cy="26%" r="55%">' +
        '<stop offset="0%" stop-color="#ffffff" stop-opacity=".65"/>' +
        '<stop offset="60%" stop-color="#ffffff" stop-opacity="0"/></radialGradient>' +
      '<radialGradient id="' + id + '-vig" cx="50%" cy="50%" r="52%">' +
        '<stop offset="72%" stop-color="#000" stop-opacity="0"/>' +
        '<stop offset="100%" stop-color="#000" stop-opacity=".38"/></radialGradient>' +
      '</defs>';
  }

  /* --- plant cell --------------------------------------------------------- */
  SCI.scenes.plantCell = function (o) {
    var n = o.chloroplasts == null ? 9 : o.chloroplasts;
    var s = SVGOPEN + '<rect width="400" height="260" fill="#f0fdf4"/>';
    s += '<g id="pc-wall"><rect x="30" y="26" width="340" height="208" rx="10" fill="#dcfce7" stroke="#15803d" stroke-width="7"/></g>';
    s += '<g id="pc-membrane"><rect x="41" y="37" width="318" height="186" rx="7" fill="none" stroke="#166534" stroke-width="2.5" stroke-dasharray="7 4"/></g>';
    s += '<g id="pc-cytoplasm"><rect x="46" y="42" width="308" height="176" rx="6" fill="#bbf7d0" opacity=".55"/></g>';
    s += '<g id="pc-vacuole"><ellipse cx="200" cy="130" rx="112" ry="62" fill="#a7f3d0" stroke="#0d9488" stroke-width="2.5" opacity=".85"/></g>';
    s += '<g id="pc-nucleus"><circle cx="98" cy="86" r="27" fill="#c084fc" stroke="#7e22ce" stroke-width="3"/><circle cx="98" cy="86" r="10" fill="#7e22ce" opacity=".55"/></g>';
    s += '<g id="pc-chloro">';
    for (var i = 0; i < n; i++) {
      var a = (i / n) * Math.PI * 2, cx = 200 + Math.cos(a) * 132, cy = 130 + Math.sin(a) * 78;
      s += '<ellipse class="g-flow-jiggle" style="animation-delay:' + (i * .5).toFixed(1) + 's" cx="' + cx.toFixed(0) + '" cy="' + cy.toFixed(0) + '" rx="15" ry="9" transform="rotate(' + (i * 37) + ' ' + cx.toFixed(0) + ' ' + cy.toFixed(0) + ')" fill="#22c55e" stroke="#15803d" stroke-width="2"/>';
    }
    s += '</g>';
    return s + '</svg>';
  };

  /* --- animal cell -------------------------------------------------------- */
  SCI.scenes.animalCell = function (o) {
    var s = SVGOPEN + '<rect width="400" height="260" fill="#fdf2f8"/>';
    s += '<g id="ac-membrane"><ellipse cx="200" cy="130" rx="160" ry="102" fill="#fce7f3" stroke="#be185d" stroke-width="4"/></g>';
    s += '<g id="ac-cytoplasm"><ellipse cx="200" cy="130" rx="152" ry="94" fill="#fbcfe8" opacity=".5"/></g>';
    s += '<g id="ac-nucleus"><circle cx="200" cy="126" r="38" fill="#c084fc" stroke="#7e22ce" stroke-width="3.5"/><circle cx="200" cy="126" r="13" fill="#7e22ce" opacity=".5"/></g>';
    s += '<g id="ac-mito">';
    [[104, 88], [292, 96], [120, 178], [286, 176], [200, 208]].forEach(function (p, i) {
      s += '<g class="g-flow-jiggle" style="animation-delay:' + (i * .7) + 's" transform="translate(' + p[0] + ',' + p[1] + ') rotate(' + (i * 41 - 20) + ')">' +
        '<ellipse rx="21" ry="11" fill="#fb923c" stroke="#c2410c" stroke-width="2"/>' +
        '<path d="M -14 0 q 5 -7 10 0 q 5 7 10 0" fill="none" stroke="#c2410c" stroke-width="1.8"/></g>';
    });
    s += '</g>';
    return s + '</svg>';
  };

  /* --- the microscope itself, in named parts for staged assembly ---------- */
  SCI.scenes.microscope = function (o) {
    /* Part ids (ms-base, ms-light, …) stay STABLE — the discover payload names
       them. Only the gradient ids are uniquified, because those are what
       url(#…) resolves across the whole document. */
    var OPT = uid('msopt');
    var s = SVGOPEN + '<rect width="400" height="260" fill="#f8fafc"/>' + defsOptics(OPT);
    s += '<g id="ms-base"><rect x="96" y="214" width="180" height="18" rx="6" fill="#e2e8f0" stroke="#475569" stroke-width="2.5"/>' +
         '<path d="M 150 214 Q 118 150 158 112" fill="none" stroke="#334155" stroke-width="9" stroke-linecap="round"/></g>';
    s += '<g id="ms-light"><circle cx="126" cy="150" r="12" fill="#fde68a" stroke="#a16207" stroke-width="2.5"/>' +
         '<circle class="sci-beam" data-on="1" cx="126" cy="150" r="26" fill="url(#' + OPT + '-beam)"/></g>';
    s += '<g id="ms-stage"><rect x="112" y="160" width="108" height="11" rx="3" fill="#fff" stroke="#334155" stroke-width="2.5"/>' +
         '<rect x="142" y="153" width="44" height="8" rx="1.5" fill="#bae6fd" stroke="#0369a1" stroke-width="1.8"/></g>';
    s += '<g id="ms-focus"><circle cx="118" cy="188" r="13" fill="#fff" stroke="#334155" stroke-width="2.5"/>' +
         '<circle cx="118" cy="188" r="5" fill="#94a3b8"/>' +
         '<circle cx="140" cy="190" r="8" fill="#fff" stroke="#64748b" stroke-width="2"/></g>';
    s += '<g id="ms-objectives"><rect x="136" y="108" width="66" height="15" rx="7" fill="#fff" stroke="#334155" stroke-width="2.5"/>' +
         '<rect x="142" y="123" width="11" height="22" rx="2" fill="#ede9fe" stroke="#7A5C9E" stroke-width="2"/>' +
         '<rect x="158" y="123" width="11" height="28" rx="2" fill="#ede9fe" stroke="#7A5C9E" stroke-width="2"/>' +
         '<rect x="174" y="123" width="11" height="34" rx="2" fill="#ede9fe" stroke="#7A5C9E" stroke-width="2"/></g>';
    s += '<g id="ms-eyepiece"><rect x="152" y="52" width="26" height="46" rx="5" fill="#fff" stroke="#334155" stroke-width="2.5"/>' +
         '<ellipse cx="165" cy="52" rx="16" ry="6.5" fill="#7A5C9E" fill-opacity=".45" stroke="#7A5C9E" stroke-width="2.5"/></g>';
    /* the live field of view, drawn beside the instrument */
    s += '<g id="ms-field"><circle cx="308" cy="130" r="66" fill="#0b1220" stroke="#334155" stroke-width="3"/>' +
         '<circle cx="308" cy="130" r="62" fill="url(#' + OPT + '-beam)" opacity=".5"/>' +
         '<circle cx="308" cy="130" r="66" fill="url(#' + OPT + '-glint)" opacity=".8"/>' +
         '<text class="sci-neutral" x="308" y="212" text-anchor="middle" font-size="11" font-weight="700" fill="#475569">what you see</text></g>';
    return s + '</svg>';
  };

  /* --- the view down the eyepiece: shared by simulator and comparison -----
     `detail` is what makes the resolution lesson honest. A light microscope and
     an electron microscope at the SAME magnification must not render the same
     picture with a caption claiming one is sharper — the pupil is being asked
     to observe a difference, so the difference has to be there to observe.
     detail:'electron' resolves structures inside the cell that detail:'light'
     genuinely cannot, and a light view always carries a little softness. */
  SCI.scenes.field = function (o) {
    var mag = o.mag || 40;                        /* total magnification */
    var focus = o.focus == null ? 0 : o.focus;    /* -10..10, 0 is best focus */
    var bright = o.bright == null ? 60 : o.bright;
    var detail = o.detail || 'light';
    var R = 118, cx = 200, cy = 128;
    var floor = detail === 'electron' ? 0 : 0.9;  /* light optics are never perfect */
    var blur = Math.min(9, Math.abs(focus) * .9 + floor);
    /* Cell size tracks magnification exactly, so the field of view genuinely
       empties as the pupil magnifies. The trade-off is real, not a caption. */
    var cell = 13 * (mag / 40);
    var CLIP = uid('clip'), OPT = uid('opt');
    var s = '<svg viewBox="0 0 400 260" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,sans-serif">' + defsOptics(OPT);
    s += '<rect width="400" height="260" fill="#0b1220"/>';
    s += '<clipPath id="' + CLIP + '"><circle cx="' + cx + '" cy="' + cy + '" r="' + R + '"/></clipPath>';
    s += '<circle cx="' + cx + '" cy="' + cy + '" r="' + R + '" fill="#f7f3e8" opacity="' + (0.18 + bright / 140).toFixed(2) + '"/>';
    s += '<g clip-path="url(#' + CLIP + ')" class="sci-optics-blur" style="filter:blur(' + blur.toFixed(1) + 'px)">';
    /* capped so a very low magnification cannot emit thousands of nodes */
    var cols = clamp(Math.round(240 / cell), 1, 34), rows = clamp(Math.round(240 / cell), 1, 34);
    for (var r = 0; r < rows; r++) for (var c = 0; c < cols; c++) {
      var x = cx - 120 + c * cell + (r % 2 ? cell / 2 : 0), y = cy - 120 + r * cell;
      var dx = x - cx, dy = y - cy;
      if (dx * dx + dy * dy > (R + cell) * (R + cell)) continue;
      var w = cell * .92, sw = Math.max(.6, cell * .06);
      s += '<rect x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="' + w.toFixed(1) +
           '" height="' + w.toFixed(1) + '" rx="' + (cell * .22).toFixed(1) +
           '" fill="#d9f0d9" stroke="#2f6b3a" stroke-width="' + sw.toFixed(2) + '"/>';
      if (cell > 11) {
        s += '<circle cx="' + (x + cell * .46).toFixed(1) + '" cy="' + (y + cell * .46).toFixed(1) +
             '" r="' + (cell * .16).toFixed(1) + '" fill="#7e22ce" opacity=".75"/>';
      }
      /* Only an electron view resolves what is inside — this is the whole
         difference the comparison component asks pupils to find. */
      if (detail === 'electron' && cell > 20) {
        s += '<circle cx="' + (x + cell * .46).toFixed(1) + '" cy="' + (y + cell * .46).toFixed(1) +
             '" r="' + (cell * .06).toFixed(1) + '" fill="#3b0764"/>';
        for (var k = 0; k < 4; k++) {
          var gx = x + cell * (0.14 + (k % 2) * 0.62), gy = y + cell * (0.14 + Math.floor(k / 2) * 0.62);
          s += '<ellipse cx="' + gx.toFixed(1) + '" cy="' + gy.toFixed(1) + '" rx="' + (cell * .1).toFixed(1) +
               '" ry="' + (cell * .06).toFixed(1) + '" fill="#22c55e" stroke="#14532d" stroke-width="' + (sw * .7).toFixed(2) + '"/>';
          for (var m = 0; m < 3; m++) {
            s += '<line x1="' + (gx - cell * .07).toFixed(1) + '" y1="' + (gy - cell * .03 + m * cell * .03).toFixed(1) +
                 '" x2="' + (gx + cell * .07).toFixed(1) + '" y2="' + (gy - cell * .03 + m * cell * .03).toFixed(1) +
                 '" stroke="#14532d" stroke-width="' + (sw * .45).toFixed(2) + '"/>';
          }
        }
        s += '<rect x="' + (x + sw * 1.6).toFixed(1) + '" y="' + (y + sw * 1.6).toFixed(1) + '" width="' + (w - sw * 3.2).toFixed(1) +
             '" height="' + (w - sw * 3.2).toFixed(1) + '" rx="' + (cell * .18).toFixed(1) +
             '" fill="none" stroke="#166534" stroke-width="' + (sw * .55).toFixed(2) + '" stroke-dasharray="' + (cell * .1).toFixed(1) + ' ' + (cell * .06).toFixed(1) + '"/>';
      }
    }
    s += '</g>';
    s += '<circle cx="' + cx + '" cy="' + cy + '" r="' + R + '" fill="url(#' + OPT + '-vig)"/>';
    s += '<circle cx="' + cx + '" cy="' + cy + '" r="' + R + '" fill="url(#' + OPT + '-glint)" opacity=".55"/>';
    s += '<circle cx="' + cx + '" cy="' + cy + '" r="' + R + '" fill="none" stroke="#1e293b" stroke-width="6"/>';
    /* PHASE 7 — the scale bar rescales with magnification, on the image */
    var barPx = 70, micronsPerPx = 400 / mag / 2.2;
    var microns = Math.round(barPx * micronsPerPx);
    s += '<g><rect x="' + (cx - barPx / 2) + '" y="' + (cy + R - 26) + '" width="' + barPx + '" height="5" rx="2" fill="#fff" stroke="#0f172a"/>' +
         '<text x="' + cx + '" y="' + (cy + R - 9) + '" text-anchor="middle" font-size="12" font-weight="800" fill="#fff">' + microns + ' µm</text></g>';
    return s + '</svg>';
  };

  /* --- zoom journey scenes ------------------------------------------------ */
  SCI.scenes.leaf = function (o) {
    o = o || {};
    var s = SVGOPEN + '<rect width="400" height="260" fill="#e0f2fe"/>';
    s += '<path d="M 200 30 C 300 60 340 150 200 232 C 60 150 100 60 200 30 Z" fill="#4ade80" stroke="#15803d" stroke-width="4"/>';
    s += '<path d="M 200 34 L 200 228" stroke="#15803d" stroke-width="5"/>';
    for (var i = 1; i <= 6; i++) {
      var y = 50 + i * 26;
      s += '<path d="M 200 ' + y + ' Q ' + (200 - 46) + ' ' + (y - 8) + ' ' + (200 - 74) + ' ' + (y + 16) + '" fill="none" stroke="#15803d" stroke-width="2.4"/>';
      s += '<path d="M 200 ' + y + ' Q ' + (200 + 46) + ' ' + (y - 8) + ' ' + (200 + 74) + ' ' + (y + 16) + '" fill="none" stroke="#15803d" stroke-width="2.4"/>';
    }
    s += '<rect x="176" y="112" width="48" height="36" fill="none" stroke="#0284c7" stroke-width="2.5" stroke-dasharray="5 3"/>';
    return s + '</svg>';
  };
  SCI.scenes.leafCells = function (o) {
    o = o || {};
    var s = SVGOPEN + '<rect width="400" height="260" fill="#dcfce7"/>';
    for (var r = 0; r < 5; r++) for (var c = 0; c < 7; c++) {
      var x = 14 + c * 55 + (r % 2 ? 12 : 0), y = 16 + r * 48;
      s += '<rect x="' + x + '" y="' + y + '" width="48" height="42" rx="8" fill="#bbf7d0" stroke="#15803d" stroke-width="2.6"/>';
      for (var k = 0; k < 4; k++) {
        s += '<ellipse cx="' + (x + 10 + (k % 2) * 24) + '" cy="' + (y + 12 + Math.floor(k / 2) * 20) + '" rx="6.5" ry="4" fill="#22c55e" stroke="#166534" stroke-width="1.4"/>';
      }
    }
    s += '<rect x="168" y="106" width="56" height="46" fill="none" stroke="#0284c7" stroke-width="2.5" stroke-dasharray="5 3"/>';
    return s + '</svg>';
  };
  SCI.scenes.chloroplast = function (o) {
    o = o || {};
    var s = SVGOPEN + '<rect width="400" height="260" fill="#14532d"/>';
    s += '<ellipse cx="200" cy="130" rx="168" ry="98" fill="#16a34a" stroke="#052e16" stroke-width="6"/>';
    for (var i = 0; i < 6; i++) {
      var x = 70 + i * 52;
      s += '<g transform="translate(' + x + ',130)">';
      for (var j = 0; j < 6; j++) s += '<ellipse cy="' + (-32 + j * 13) + '" rx="20" ry="5" fill="#166534" stroke="#052e16" stroke-width="1.6"/>';
      s += '</g>';
    }
    s += '<rect x="172" y="108" width="54" height="44" fill="none" stroke="#bae6fd" stroke-width="2.5" stroke-dasharray="5 3"/>';
    return s + '</svg>';
  };
  SCI.scenes.membrane = function (o) {
    var s = SVGOPEN + '<rect width="400" height="260" fill="#eff6ff"/>';
    /* phospholipid bilayer */
    for (var i = 0; i < 22; i++) {
      var x = 8 + i * 18;
      s += '<g><circle cx="' + x + '" cy="96" r="8" fill="#fbbf24" stroke="#b45309" stroke-width="1.8"/>' +
           '<path d="M ' + (x - 3) + ' 104 l 0 26 M ' + (x + 3) + ' 104 l 0 26" stroke="#b45309" stroke-width="2.4"/></g>';
      s += '<g><circle cx="' + x + '" cy="164" r="8" fill="#fbbf24" stroke="#b45309" stroke-width="1.8"/>' +
           '<path d="M ' + (x - 3) + ' 156 l 0 -26 M ' + (x + 3) + ' 156 l 0 -26" stroke="#b45309" stroke-width="2.4"/></g>';
    }
    s += '<ellipse cx="140" cy="130" rx="26" ry="40" fill="#60a5fa" stroke="#1d4ed8" stroke-width="2.5" opacity=".9"/>';
    s += '<ellipse cx="268" cy="130" rx="22" ry="40" fill="#a78bfa" stroke="#6d28d9" stroke-width="2.5" opacity=".9"/>';
    s += '<rect x="176" y="110" width="50" height="42" fill="none" stroke="#0284c7" stroke-width="2.5" stroke-dasharray="5 3"/>';
    return s + '</svg>';
  };
  SCI.scenes.molecules = function (o) {
    o = o || {};
    var s = SVGOPEN + '<rect width="400" height="260" fill="#f8fafc"/>';
    var pts = [[90, 80], [160, 60], [230, 92], [300, 70], [120, 160], [200, 140], [280, 172], [340, 132], [60, 128], [170, 210], [250, 214]];
    pts.forEach(function (p, i) {
      s += '<g class="g-flow-jiggle" style="animation-delay:' + (i * .35).toFixed(2) + 's">' +
        '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="13" fill="#38bdf8" stroke="#0369a1" stroke-width="2"/>' +
        '<circle cx="' + (p[0] - 13) + '" cy="' + (p[1] + 9) + '" r="7" fill="#e2e8f0" stroke="#64748b" stroke-width="1.6"/>' +
        '<circle cx="' + (p[0] + 13) + '" cy="' + (p[1] + 9) + '" r="7" fill="#e2e8f0" stroke="#64748b" stroke-width="1.6"/></g>';
    });
    if (!o.bare) s += '<text x="200" y="244" text-anchor="middle" font-size="12" font-weight="700" fill="#475569">water molecules, moving all the time</text>';
    return s + '</svg>';
  };

  /* --- alveolus / gas exchange ------------------------------------------- */
  SCI.scenes.alveolus = function (o) {
    var g = o.gradient == null ? 1 : o.gradient;
    var s = SVGOPEN + '<rect width="400" height="260" fill="#fef2f2"/>';
    /* Grouped under ids so `discover` can assemble the exchange surface one
       adaptation at a time. Ids are part of the payload contract — renaming
       one silently empties a build step, so change both together. */
    s += '<g id="alv-sac"><circle cx="140" cy="128" r="86" fill="#fee2e2" stroke="#b91c1c" stroke-width="4"/>' +
         (o.bare ? '' : '<text x="140" y="40" text-anchor="middle" font-size="12" font-weight="800" fill="#7f1d1d">air sac</text>') + '</g>';
    s += '<g id="alv-blood"><rect x="222" y="46" width="60" height="166" rx="26" fill="#fecaca" stroke="#b91c1c" stroke-width="4"/>' +
         (o.bare ? '' : '<text x="252" y="34" text-anchor="middle" font-size="12" font-weight="800" fill="#7f1d1d">blood</text>') + '</g>';
    s += '<g id="alv-wall"><rect x="204" y="52" width="16" height="154" rx="6" fill="#fca5a5" stroke="#b91c1c" stroke-width="2"/></g>';
    s += '<g id="alv-cross">';
    var n = Math.round(4 + g * 8);
    for (var i = 0; i < n; i++) {
      var y = 60 + (i * 143 / Math.max(1, n - 1));
      s += '<circle class="g-flow-jiggle" style="animation-delay:' + (i * .3).toFixed(2) + 's" cx="' + (160 + (i % 3) * 14) + '" cy="' + y.toFixed(0) + '" r="7" fill="#38bdf8" stroke="#0369a1" stroke-width="1.8"/>';
    }
    s += '<path d="M 186 128 l 30 0 m -9 -7 l 9 7 l -9 7" stroke="#0369a1" stroke-width="3.5" fill="none" stroke-linecap="round"/>';
    s += '</g>';
    return s + '</svg>';
  };

  /* --- root hair cell ----------------------------------------------------- */
  SCI.scenes.rootHair = function (o) {
    var s = SVGOPEN + '<rect width="400" height="260" fill="#fefce8"/>';
    s += '<rect x="34" y="88" width="200" height="86" rx="10" fill="#dcfce7" stroke="#15803d" stroke-width="4"/>';
    s += '<path d="M 234 118 q 70 -18 130 -46 q -54 44 -130 60 q 74 12 128 44 q -66 -22 -128 -32 z" fill="#dcfce7" stroke="#15803d" stroke-width="3.5"/>';
    s += '<circle cx="88" cy="130" r="20" fill="#c084fc" stroke="#7e22ce" stroke-width="3"/>';
    for (var i = 0; i < 8; i++) {
      s += '<circle class="g-flow-jiggle" style="animation-delay:' + (i * .4).toFixed(2) + 's" cx="' + (250 + (i % 4) * 30) + '" cy="' + (100 + Math.floor(i / 4) * 56) + '" r="6.5" fill="#38bdf8" stroke="#0369a1" stroke-width="1.6"/>';
    }
    if (!o.bare) s += '<text x="200" y="238" text-anchor="middle" font-size="12" font-weight="700" fill="#475569">a root hair cell — one cell, stretched</text>';
    return s + '</svg>';
  };

  /* --- diffusion box ------------------------------------------------------ */
  SCI.scenes.diffusionBox = function (o) {
    var spread = o.spread == null ? 0 : clamp(o.spread, 0, 1);   /* 0 = separated, 1 = even */
    var temp = o.temp == null ? 1 : o.temp;
    var s = SVGOPEN + '<rect width="400" height="260" fill="#f8fafc"/>';
    s += '<rect x="20" y="26" width="360" height="208" rx="10" fill="#fff" stroke="#334155" stroke-width="3.5"/>';
    s += '<line x1="200" y1="26" x2="200" y2="234" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="6 5"/>';
    var N = 34;
    for (var i = 0; i < N; i++) {
      /* deterministic pseudo-random so the picture is stable between renders */
      var a = Math.sin(i * 12.9898) * 43758.5453; a = a - Math.floor(a);
      var b = Math.sin(i * 78.233) * 43758.5453; b = b - Math.floor(b);
      var startX = 40 + a * 140;
      var evenX = 32 + a * 336;
      var x = startX + (evenX - startX) * spread;
      var y = 40 + b * 180;
      /* --g-heat is the GROW motion language's own temperature knob: hotter
         means a faster, wider jiggle. Driving it from the temperature slider
         means the shared vocabulary reacts to the pupil's variable. */
      s += '<circle class="g-flow-jiggle" style="--g-heat:' + temp.toFixed(2) + ';animation-delay:' + (i * .17).toFixed(2) + 's" cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="7" fill="#f472b6" stroke="#9d174d" stroke-width="1.7" opacity=".92"/>';
    }
    if (!o.bare) {
      s += '<text x="110" y="250" text-anchor="middle" font-size="11" font-weight="700" fill="#475569">more particles here</text>';
      s += '<text x="300" y="250" text-anchor="middle" font-size="11" font-weight="700" fill="#475569">fewer particles here</text>';
    }
    return s + '</svg>';
  };

  /* --- osmosis: potato chip in solution ----------------------------------- */
  SCI.scenes.osmosisChip = function (o) {
    var conc = o.conc == null ? 0 : o.conc;      /* solution concentration, mol/dm3 */
    var inside = o.inside == null ? 0.3 : o.inside;
    var d = (inside - conc);                     /* + = water moves in */
    var len = clamp(1 + d * 0.55, 0.72, 1.3);
    var s = SVGOPEN + '<rect width="400" height="260" fill="#eff6ff"/>';
    s += '<path d="M 60 60 L 60 220 Q 60 236 78 236 L 322 236 Q 340 236 340 220 L 340 60" fill="#dbeafe" stroke="#1d4ed8" stroke-width="4"/>';
    var w = 150 * len, h = 46;
    s += '<rect x="' + (200 - w / 2).toFixed(1) + '" y="' + (150 - h / 2) + '" width="' + w.toFixed(1) + '" height="' + h + '" rx="8" fill="#fef9c3" stroke="#a16207" stroke-width="3.5" style="transition:all .7s ease"/>';
    s += '<text x="200" y="' + (150 + 5) + '" text-anchor="middle" font-size="12" font-weight="800" fill="#78350f">potato</text>';
    var arrows = Math.abs(d) > .04 ? 5 : 0;
    for (var i = 0; i < arrows; i++) {
      var y = 104 + i * 22, dir = d > 0 ? 1 : -1;
      var x0 = d > 0 ? 92 + i * 4 : 200 - w / 2 - 6;
      var x1 = d > 0 ? 200 - w / 2 - 6 : 92 + i * 4;
      s += '<path class="g-flow-jiggle" style="animation-delay:' + (i * .3) + 's" d="M ' + x0 + ' ' + y + ' L ' + x1 + ' ' + y + '" stroke="#0369a1" stroke-width="2.6" marker-end="" stroke-linecap="round"/>';
      s += '<circle cx="' + ((x0 + x1) / 2).toFixed(0) + '" cy="' + y + '" r="5" fill="#38bdf8" stroke="#0369a1" stroke-width="1.5"/>';
    }
    s += '<text x="200" y="' + 250 + '" text-anchor="middle" font-size="11" font-weight="700" fill="#1e3a8a">' +
      (Math.abs(d) < .04 ? 'no net movement of water' : (d > 0 ? 'net water movement INTO the potato' : 'net water movement OUT of the potato')) + '</text>';
    return s + '</svg>';
  };

  /* --- active transport: against the gradient ----------------------------- */
  SCI.scenes.activeTransport = function (o) {
    var energy = o.energy == null ? 100 : o.energy;   /* % respiration */
    var s = SVGOPEN + '<rect width="400" height="260" fill="#f5f3ff"/>';
    s += '<rect x="0" y="0" width="400" height="104" fill="#e0f2fe"/>' + (o.bare ? '' : '<text x="20" y="24" font-size="12" font-weight="800" fill="#075985">OUTSIDE — few particles</text>');
    s += '<rect x="0" y="156" width="400" height="104" fill="#ede9fe"/>' + (o.bare ? '' : '<text x="20" y="250" font-size="12" font-weight="800" fill="#4c1d95">INSIDE — already lots of particles</text>');
    for (var i = 0; i < 22; i++) {
      var x = 8 + i * 18;
      s += '<circle cx="' + x + '" cy="118" r="7.5" fill="#fbbf24" stroke="#b45309" stroke-width="1.7"/>';
      s += '<circle cx="' + x + '" cy="146" r="7.5" fill="#fbbf24" stroke="#b45309" stroke-width="1.7"/>';
      s += '<path d="M ' + x + ' 125 l 0 14" stroke="#b45309" stroke-width="2.2"/>';
    }
    s += '<rect x="168" y="102" width="64" height="60" rx="12" fill="#a78bfa" stroke="#5b21b6" stroke-width="3"/>';
    if (!o.bare) s += '<text x="200" y="136" text-anchor="middle" font-size="11" font-weight="900" fill="#fff">carrier</text>';
    var n = Math.round(energy / 20);
    for (var j = 0; j < 5; j++) {
      var on = j < n;
      s += '<circle cx="' + (150 + j * 25) + '" cy="' + (on ? 78 : 40) + '" r="8" fill="' + (on ? '#38bdf8' : '#cbd5e1') + '" stroke="' + (on ? '#0369a1' : '#94a3b8') + '" stroke-width="1.8" style="transition:all .6s"/>';
    }
    s += '<g opacity="' + (energy > 0 ? 1 : .25) + '"><path d="M 200 96 L 200 60 m -8 10 l 8 -10 l 8 10" fill="none" stroke="#dc2626" stroke-width="3.4" stroke-linecap="round"/>' +
         (o.bare ? '' : '<text x="252" y="70" font-size="11" font-weight="800" fill="#b91c1c">uphill — needs energy</text>') + '</g>';
    if (!o.bare) s += '<text x="200" y="196" text-anchor="middle" font-size="12" font-weight="800" fill="#4c1d95">energy from respiration: ' + Math.round(energy) + '%</text>';
    return s + '</svg>';
  };

  /* --- the osmosis core practical, in method order ------------------------
     Separate from slidePrep because these are two different practicals, and a
     method animation that shows the wrong apparatus teaches the wrong method. */
  SCI.scenes.osmosisPractical = function (o) {
    var s = SVGOPEN + '<rect width="400" height="260" fill="#f8fafc"/>';
    s += '<g id="op-chips"><rect x="18" y="30" width="86" height="52" rx="6" fill="#fef9c3" stroke="#a16207" stroke-width="3"/>';
    for (var i = 0; i < 3; i++) {
      s += '<rect x="26" y="' + (38 + i * 15) + '" width="70" height="9" rx="3" fill="#fde68a" stroke="#a16207" stroke-width="1.6"/>';
    }
    s += '<text x="61" y="96" text-anchor="middle" font-size="10" font-weight="800" fill="#78350f">equal chips</text></g>';
    s += '<g id="op-balance"><rect x="130" y="56" width="86" height="26" rx="5" fill="#e2e8f0" stroke="#334155" stroke-width="2.5"/>' +
         '<rect x="146" y="42" width="54" height="14" rx="3" fill="#fff" stroke="#334155" stroke-width="2"/>' +
         '<text x="173" y="74" text-anchor="middle" font-size="11" font-weight="900" fill="#0f172a">2.41 g</text>' +
         '<text x="173" y="96" text-anchor="middle" font-size="10" font-weight="800" fill="#334155">blot, then weigh</text></g>';
    s += '<g id="op-tubes">';
    var concs = ['0.0', '0.2', '0.4', '0.6', '0.8', '1.0'];
    for (var t = 0; t < 6; t++) {
      var x = 22 + t * 62;
      s += '<rect x="' + x + '" y="130" width="40" height="76" rx="8" fill="#dbeafe" stroke="#1d4ed8" stroke-width="2.5"/>';
      s += '<rect x="' + (x + 4) + '" y="' + (146 + t * 2) + '" width="32" height="' + (56 - t * 2) + '" rx="5" fill="#bfdbfe" opacity="' + (0.35 + t * 0.11).toFixed(2) + '"/>';
      s += '<rect x="' + (x + 8) + '" y="164" width="24" height="9" rx="3" fill="#fef9c3" stroke="#a16207" stroke-width="1.6"/>';
      s += '<text x="' + (x + 20) + '" y="222" text-anchor="middle" font-size="10" font-weight="800" fill="#1e3a8a">' + concs[t] + '</text>';
    }
    s += '<text x="200" y="240" text-anchor="middle" font-size="10" font-weight="800" fill="#1e3a8a">sugar concentration (mol/dm³) — everything else kept the same</text></g>';
    s += '<g id="op-reweigh"><rect x="248" y="30" width="130" height="70" rx="8" fill="#fff" stroke="#334155" stroke-width="2.5"/>' +
         '<text x="313" y="54" text-anchor="middle" font-size="11" font-weight="900" fill="#0f172a">blot the same way</text>' +
         '<text x="313" y="72" text-anchor="middle" font-size="11" font-weight="900" fill="#0f172a">reweigh: 2.64 g</text>' +
         '<text x="313" y="90" text-anchor="middle" font-size="10" font-weight="700" fill="#475569">start 2.41 g</text></g>';
    s += '<g id="op-calc"><rect x="112" y="102" width="180" height="24" rx="6" fill="#dcfce7" stroke="#15803d" stroke-width="2.5"/>' +
         '<text x="202" y="119" text-anchor="middle" font-size="11" font-weight="900" fill="#14532d">(0.23 ÷ 2.41) × 100 = +9.5%</text></g>';
    return s + '</svg>';
  };

  /* --- slide preparation, for the animated method ------------------------- */
  SCI.scenes.slidePrep = function (o) {
    var OPT = uid('spopt');
    var s = SVGOPEN + '<rect width="400" height="260" fill="#f8fafc"/>' + defsOptics(OPT);
    s += '<rect x="70" y="150" width="260" height="16" rx="3" fill="#e0f2fe" stroke="#0369a1" stroke-width="2.5"/>';
    s += '<text x="200" y="188" text-anchor="middle" font-size="11" font-weight="700" fill="#475569">glass slide</text>';
    s += '<g id="sp-specimen" class="sci-part" data-built="0"><ellipse cx="200" cy="150" rx="34" ry="8" fill="#bbf7d0" stroke="#15803d" stroke-width="2"/></g>';
    s += '<g id="sp-stain" class="sci-part" data-built="0"><circle cx="200" cy="128" r="9" fill="#60a5fa" stroke="#1d4ed8" stroke-width="2"/>' +
         '<path d="M 200 138 l 0 8" stroke="#1d4ed8" stroke-width="2.4"/></g>';
    s += '<g id="sp-coverslip" class="sci-part" data-built="0"><rect x="146" y="120" width="108" height="6" rx="2" fill="#dbeafe" stroke="#0369a1" stroke-width="2" transform="rotate(-16 200 123)"/></g>';
    s += '<g id="sp-eye" class="sci-part" data-built="0"><circle cx="200" cy="62" r="40" fill="#0b1220" stroke="#334155" stroke-width="3"/>' +
         '<g class="sci-optics-blur"><circle cx="188" cy="54" r="9" fill="#d9f0d9" stroke="#2f6b3a" stroke-width="1.6"/>' +
         '<circle cx="210" cy="66" r="9" fill="#d9f0d9" stroke="#2f6b3a" stroke-width="1.6"/>' +
         '<circle cx="196" cy="76" r="9" fill="#d9f0d9" stroke="#2f6b3a" stroke-width="1.6"/></g>' +
         '<circle cx="200" cy="62" r="40" fill="url(#' + OPT + '-glint)" opacity=".5"/></g>';
    return s + '</svg>';
  };

  /* ======================================================================== *
   * SIMULATORS
   * ======================================================================== */

  /* --- the microscope simulator: PHASES 8, 9 and 12 in one component ------ */
  SCI.sims.microscope = {
    params: [
      { key: 'obj', type: 'choice', label: 'Objective lens (turret)', value: 4,
        options: [{ label: '×4', value: 4 }, { label: '×10', value: 10 }, { label: '×40', value: 40 }] },
      { key: 'focus', type: 'range', label: 'Fine focus wheel', value: 6, min: -10, max: 10, step: 1,
        fmt: function (v) { return v === 0 ? 'sharp' : (Math.abs(v) > 5 ? 'well out' : 'nearly'); } },
      { key: 'bright', type: 'range', label: 'Lamp brightness', value: 60, min: 5, max: 100, step: 5,
        fmt: function (v) { return v + '%'; } }
    ],
    render: function (st) {
      var eye = 10, total = eye * st.obj;
      var fovMm = (4.5 / (total / 40));
      var note = '';
      if (Math.abs(st.focus) <= 1) note = 'Sharp. That is resolution — detail you can actually separate.';
      else if (Math.abs(st.focus) > 6) note = 'Bigger, but you cannot tell two things apart. Magnification without resolution is just a bigger blur.';
      else note = 'Nearly. Keep turning the fine focus, slowly.';
      if (st.bright < 20) note = 'Too dark to judge focus at all. Light first, then focus.';
      if (st.bright > 90 && st.obj === 4) note = 'Glare at low power washes out the edges. More light is not always better.';
      return {
        svg: SCI.scenes.field({ mag: total, focus: st.focus, bright: st.bright }),
        readout: [
          ['Eyepiece', '×' + eye],
          ['Objective', '×' + st.obj],
          ['Total magnification', '×' + total],
          ['Field of view', fovMm.toFixed(2) + ' mm'],
          ['Image', Math.abs(st.focus) <= 1 ? 'sharp' : 'blurred']
        ],
        note: note
      };
    }
  };

  /* --- magnification arithmetic, made physical --------------------------- */
  SCI.sims.magnification = {
    params: [
      { key: 'obj', type: 'choice', label: 'Objective lens', value: 10,
        options: [{ label: '×4', value: 4 }, { label: '×10', value: 10 }, { label: '×40', value: 40 }] },
      { key: 'real', type: 'range', label: 'Real size of the cell (µm)', value: 50, min: 10, max: 200, step: 5,
        fmt: function (v) { return v + ' µm'; } }
    ],
    render: function (st) {
      var total = 10 * st.obj;
      var imageUm = st.real * total;
      return {
        svg: SCI.scenes.field({ mag: total, focus: 0, bright: 65 }),
        readout: [
          ['Total magnification', '×' + total],
          ['Real size', st.real + ' µm'],
          ['Image size', (imageUm / 1000).toFixed(2) + ' mm'],
          ['magnification =', 'image ÷ real']
        ],
        note: 'Image ' + (imageUm / 1000).toFixed(2) + ' mm ÷ real ' + (st.real / 1000).toFixed(3) +
              ' mm = ×' + total + '. The same three numbers, rearranged, answer every version of this question.'
      };
    }
  };

  SCI.sims.diffusion = {
    params: [
      { key: 'spread', type: 'range', label: 'Time', value: 0, min: 0, max: 100, step: 1,
        fmt: function (v) { return v === 0 ? 'start' : v + ' s'; } },
      { key: 'temp', type: 'range', label: 'Temperature', value: 1, min: 0.4, max: 2, step: 0.1,
        fmt: function (v) { return v < .8 ? 'cold' : v > 1.4 ? 'warm' : 'room'; } }
    ],
    render: function (st) {
      var sp = clamp(st.spread / 100, 0, 1);
      var evenness = Math.round(sp * 100);
      return {
        svg: SCI.scenes.diffusionBox({ spread: sp, temp: st.temp }),
        readout: [
          ['Difference across the box', (100 - evenness) + '%'],
          ['Net movement', evenness >= 97 ? 'none — but particles still move' : 'left → right'],
          ['Particle speed', st.temp < .8 ? 'slow' : st.temp > 1.4 ? 'fast' : 'normal']
        ],
        note: evenness >= 97
          ? 'Evenly spread — and the particles have NOT stopped. Equal numbers cross each way, so there is no NET movement. That distinction is worth a mark.'
          : 'Particles move in every direction. More of them start on the left, so more happen to cross to the right. That is all diffusion is.'
      };
    }
  };

  SCI.sims.osmosis = {
    params: [
      { key: 'conc', type: 'range', label: 'Sugar concentration outside (mol/dm³)', value: 0, min: 0, max: 1, step: 0.05,
        fmt: function (v) { return v.toFixed(2); } }
    ],
    render: function (st, cfg) {
      var inside = (cfg && cfg.inside) || 0.3;
      var d = inside - st.conc;
      var pct = (d * 22).toFixed(1);
      return {
        svg: SCI.scenes.osmosisChip({ conc: st.conc, inside: inside }),
        readout: [
          ['Outside', st.conc.toFixed(2) + ' mol/dm³'],
          ['Inside the cell', inside.toFixed(2) + ' mol/dm³'],
          ['Predicted change in mass', (d > 0 ? '+' : '') + pct + '%'],
          ['Water moves', Math.abs(d) < .03 ? 'no net movement' : (d > 0 ? 'into the potato' : 'out of the potato')]
        ],
        note: Math.abs(d) < .03
          ? 'The two concentrations match, so there is no NET movement. Where the line crosses zero is the concentration inside the cells — that is the whole point of the graph.'
          : (d > 0
            ? 'More water outside than in, so water moves in and the chip gains mass.'
            : 'More water inside than out, so water leaves and the chip loses mass.')
      };
    }
  };

  SCI.sims.activeTransport = {
    params: [
      { key: 'energy', type: 'range', label: 'Energy available from respiration', value: 100, min: 0, max: 100, step: 10,
        fmt: function (v) { return v + '%'; } }
    ],
    render: function (st) {
      return {
        svg: SCI.scenes.activeTransport({ energy: st.energy }),
        readout: [
          ['Energy from respiration', st.energy + '%'],
          ['Movement against the gradient', st.energy > 0 ? 'happening' : 'stopped'],
          ['Diffusion', 'unaffected — needs no energy']
        ],
        note: st.energy === 0
          ? 'Take the energy away and active transport stops — but diffusion carries on. That single difference is the test question.'
          : 'Particles are being moved from where there are FEWER to where there are MORE. Nothing does that for free.'
      };
    }
  };

  SCI.sims.surfaceArea = {
    params: [
      { key: 'size', type: 'range', label: 'Size of the block (cm)', value: 1, min: 1, max: 5, step: 1,
        fmt: function (v) { return v + ' cm'; } }
    ],
    render: function (st) {
      var a = 6 * st.size * st.size, v = st.size * st.size * st.size, r = a / v;
      var s = SVGOPEN + '<rect width="400" height="260" fill="#f8fafc"/>';
      var px = 26 * st.size;
      s += '<g transform="translate(' + (150 - px / 2) + ',' + (150 - px / 2) + ')">' +
        '<rect width="' + px + '" height="' + px + '" fill="#fca5a5" stroke="#b91c1c" stroke-width="3" style="transition:all .5s"/>' +
        '<path d="M 0 0 l 22 -20 l ' + px + ' 0 l -22 20 z" fill="#fecaca" stroke="#b91c1c" stroke-width="3"/>' +
        '<path d="M ' + px + ' 0 l 22 -20 l 0 ' + px + ' l -22 20 z" fill="#f87171" stroke="#b91c1c" stroke-width="3"/></g>';
      s += '<text x="300" y="110" text-anchor="middle" font-size="15" font-weight="900" fill="#0f172a">SA : V</text>';
      s += '<text x="300" y="142" text-anchor="middle" font-size="26" font-weight="900" fill="#b91c1c">' + r.toFixed(2) + '</text>';
      s += '<text x="300" y="168" text-anchor="middle" font-size="12" fill="#475569">' + a + ' cm² ÷ ' + v + ' cm³</text>';
      s += '</svg>';
      return {
        svg: s,
        readout: [['Surface area', a + ' cm²'], ['Volume', v + ' cm³'], ['SA : V ratio', r.toFixed(2)]],
        note: st.size === 1
          ? 'Small object, big ratio — diffusion alone can supply the whole thing.'
          : 'As it gets bigger the ratio falls. The inside is further from the surface, so diffusion alone can no longer keep up. That is why big organisms need exchange surfaces.'
      };
    }
  };

  /* ======================================================================== *
   * MOUNTING — place components into the deck's existing slides
   * ------------------------------------------------------------------------
   * The engine never rewrites slide markup it did not create. It finds a slide
   * by its data-title, finds an anchor inside it, and inserts. If either is
   * missing the component is skipped and reported — a silently absent
   * component is worse than a visibly missing one.
   * ======================================================================== */

  function slideByTitle(t) {
    var all = qa(document, '.slide');
    for (var i = 0; i < all.length; i++) {
      if ((all[i].getAttribute('data-title') || '').toLowerCase() === String(t).toLowerCase()) return all[i];
    }
    return null;
  }

  SCI.mount = function (payload) {
    payload = payload || window.SCI_LESSON;
    if (!payload || !payload.components) return { placed: 0, skipped: [] };
    var placed = 0, skipped = [];

    payload.components.forEach(function (c, idx) {
      var slide = slideByTitle(c.slide);
      if (!slide) { skipped.push(c.slide + ' (slide not found)'); return; }
      if (q(slide, '.sci[data-sci-key="' + (c.key || ('c' + idx)) + '"]')) return;   /* idempotent */
      var build = SCI.comps[c.type];
      if (!build) { skipped.push(c.type + ' (no such component)'); return; }
      var node;
      /* declare the XP budget BEFORE building, so a component that awards on
         construction cannot spend from an empty pool */
      declareXP(xpCost(c));
      try { node = build(c); }
      catch (e) { skipped.push(c.type + ' (' + e.message + ')'); return; }
      node.setAttribute('data-sci-key', c.key || ('c' + idx));

      /* `anchor`, NOT `after` — `after` is already the pause component's
         follow-up sentence, and feeding a sentence to querySelector throws.
         The try/catch means a future bad selector costs one component's
         position, not the whole layer. */
      var anchor = null;
      if (c.anchor) {
        try { anchor = q(slide, c.anchor); }
        catch (e) { skipped.push((c.key || c.type) + ' (bad anchor selector "' + c.anchor + '")'); }
      }
      if (anchor && anchor.parentNode) anchor.parentNode.insertBefore(node, anchor.nextSibling);
      else slide.appendChild(node);
      placed++;
    });

    if (skipped.length && window.console) {
      console.warn('[SCI] components skipped:', skipped);
    }
    SCI.report = { placed: placed, skipped: skipped, total: payload.components.length };
    return SCI.report;
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { SCI.mount(); });
  } else { SCI.mount(); }

})(window, document);
