/* ============================================================================
   BUILD Animation Framework — engine
   ---------------------------------------------------------------------------
   Teacher-controlled, step-by-step scientific animation for BUILD lessons.

   THE IDEA
     A slide holds a "stage". A stage holds a layered SVG and a SCRIPT. The
     teacher presses ▶ Next; one step of the script fires; the teacher narrates
     the line the framework prints for them. Pupils cannot read ahead, because
     there is nothing to read yet.

   MARKUP
     <div class="ba-stage" data-ba-asset="fish" data-ba-script="@teach"></div>

     data-ba-asset   name from the BioSVG library (fish, crab, human, …)
     data-ba-script  either an inline script, or @teach / @reveal to use the
                     script that ships with the asset
     data-ba-title   optional caption shown above the picture
     data-ba-nobar   present = no control bar (driven by code instead)

     Anything on the same slide carrying data-ba-step="3" appears at step 3.
     Use it for the short label / definition that CONFIRMS what was just shown.

   SCRIPT FORMAT — one step per line
     verb targets + verb targets :: what the teacher says
     e.g.  glow spine + hi spine :: Not the ribs. The line down the middle.

   VERBS
     show hide draw pop glow unglow hi unhi dim only undim pulse unpulse
     spot unspot zoom unzoom trace bounce shake label unlabel tick cross
     think unthink note wait

   PUBLIC HELPERS (the named ones asked for, plus the general engine)
     drawSkeleton(stage)    highlightBone(stage, part)  traceBackbone(stage)
     revealLabels(stage)    pulseCorrect(el)            zoomFeature(stage,part)
     fadeOthers(stage,keep) BuildAnim.next/reset/all/load/advanceActive
   ========================================================================== */
(function (global, doc) {
  'use strict';

  var VB_W = 400, VB_H = 300;
  var BA = {};

  function $(sel, root) { return (root || doc).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || doc).querySelectorAll(sel)); }
  function ding() { try { if (typeof global.playDing === 'function') global.playDing(); } catch (e) {} }
  function buzz() { try { if (typeof global.playBuzz === 'function') global.playBuzz(); } catch (e) {} }

  /* ====================================================== script parsing */

  function parseScript(src) {
    if (!src) return [];
    return src.split('\n').map(function (l) { return l.trim(); })
      .filter(function (l) { return l && l.charAt(0) !== '#'; })
      .map(function (line) {
        var i = line.indexOf('::');
        var head = i < 0 ? line : line.slice(0, i);
        var say = i < 0 ? '' : line.slice(i + 2).trim();
        var acts = head.split('+').map(function (s) { return s.trim(); })
          .filter(Boolean).map(function (a) {
            var m = a.match(/^([a-zA-Z-]+)\s*([\s\S]*)$/);
            if (!m) return null;
            var verb = m[1].toLowerCase(), rest = (m[2] || '').trim(), text = null;
            var q = rest.match(/"([^"]*)"\s*$/);
            if (q) { text = q[1]; rest = rest.slice(0, q.index).trim(); }
            return {
              verb: verb, text: text,
              targets: rest ? rest.split(',').map(function (s) { return s.trim(); }).filter(Boolean) : []
            };
          }).filter(Boolean);
        return { acts: acts, say: say };
      });
  }

  /* which parts does the script switch ON at some point?  Those start hidden. */
  function hiddenParts(steps) {
    var set = {};
    steps.forEach(function (st) {
      st.acts.forEach(function (a) {
        if (a.verb === 'show' || a.verb === 'draw' || a.verb === 'pop') {
          a.targets.forEach(function (t) { set[t.split('#')[0]] = true; });
        }
      });
    });
    return set;
  }

  /* ============================================================= geometry */

  function svgMetrics(stage) {
    var svg = $('.ba-svg', stage), canvas = $('.ba-canvas', stage);
    if (!svg || !canvas) return null;
    var r = svg.getBoundingClientRect(), cr = canvas.getBoundingClientRect();
    if (!r.width || !r.height) return null;
    var k = Math.min(r.width / VB_W, r.height / VB_H);
    return {
      svg: svg, k: k,
      ox: (r.left - cr.left) + (r.width - VB_W * k) / 2,
      oy: (r.top - cr.top) + (r.height - VB_H * k) / 2
    };
  }

  function partBox(stage, name) {
    var els = $$('[data-part="' + name + '"]', stage);
    if (!els.length) return null;
    var box = null;
    els.forEach(function (el) {
      var b; try { b = el.getBBox(); } catch (e) { return; }
      if (!b || (!b.width && !b.height)) return;
      if (!box) box = { x: b.x, y: b.y, w: b.width, h: b.height };
      else {
        var x2 = Math.max(box.x + box.w, b.x + b.width), y2 = Math.max(box.y + box.h, b.y + b.height);
        box.x = Math.min(box.x, b.x); box.y = Math.min(box.y, b.y);
        box.w = x2 - box.x; box.h = y2 - box.y;
      }
    });
    return box;
  }

  /* ============================================================ the verbs */

  /* Targets are part names.  In a comparison rail, "body#2" means "the body
     of the SECOND animal along" — everything else addresses every animal. */
  function parts(stage, names) {
    if (!names || !names.length || names[0] === '*') return $$('[data-part]', stage);
    var out = [];
    names.forEach(function (nm) {
      var h = nm.indexOf('#'), sel;
      if (h > 0) sel = '.ba-cell:nth-of-type(' + parseInt(nm.slice(h + 1), 10) + ') [data-part="' + nm.slice(0, h) + '"]';
      else sel = '[data-part="' + nm + '"]';
      $$(sel, stage).forEach(function (e) { out.push(e); });
    });
    return out;
  }

  function restart(el, cls) {
    el.classList.remove(cls);
    el.getBoundingClientRect();       /* force reflow so the animation replays */
    el.classList.add(cls);
  }

  /* `pop` animates a transform, which would otherwise override the transform
     ATTRIBUTE a child uses to position itself — a rotated vertebra would snap
     upright, a placed icon would jump to the origin. So each direct child gets
     a wrapper the first time it is popped: the wrapper carries the animation,
     the child keeps its own placement. Done once, then cached. */
  var SVGNS = 'http://www.w3.org/2000/svg';
  function popTargets(e) {
    if (e._baPopKids) return e._baPopKids;
    var out = [];
    Array.prototype.slice.call(e.children).forEach(function (k) {
      if (k.tagName === 'text') { out.push(k); return; }
      var w = doc.createElementNS(SVGNS, 'g');
      w.setAttribute('class', 'ba-popwrap');
      e.insertBefore(w, k);
      w.appendChild(k);
      out.push(w);
    });
    e._baPopKids = out;
    return out;
  }

  function overlay(stage, cls, html) {
    var canvas = $('.ba-canvas', stage);
    var el = doc.createElement('div');
    el.className = cls;
    el.innerHTML = html || '';
    canvas.appendChild(el);
    return el;
  }

  var VERBS = {
    show: function (stage, a) {
      parts(stage, a.targets).forEach(function (e) { e.classList.remove('ba-hidden'); restart(e, 'ba-fadein'); });
    },
    hide: function (stage, a) {
      parts(stage, a.targets).forEach(function (e) { e.classList.add('ba-hidden'); });
    },
    draw: function (stage, a) {
      parts(stage, a.targets).forEach(function (e) {
        e.classList.remove('ba-hidden');
        e.classList.add('ba-drew');
        $$('path,line,polyline,rect,circle,ellipse', e).forEach(function (s) { restart(s, 'draw-svg'); });
      });
    },
    pop: function (stage, a) {
      parts(stage, a.targets).forEach(function (e) {
        e.classList.remove('ba-hidden');
        popTargets(e).forEach(function (k, i) {
          k.style.animationDelay = (i * 0.085) + 's';
          restart(k, 'ba-pop');
        });
      });
      ding();
    },
    glow:   function (s, a) { parts(s, a.targets).forEach(function (e) { e.classList.add('glow-path'); }); },
    unglow: function (s, a) { parts(s, a.targets).forEach(function (e) { e.classList.remove('glow-path'); }); },
    hi:     function (s, a) { parts(s, a.targets).forEach(function (e) { e.classList.add('highlight-region'); }); ding(); },
    unhi:   function (s, a) { parts(s, a.targets).forEach(function (e) { e.classList.remove('highlight-region'); }); },
    dim:    function (s, a) { parts(s, a.targets).forEach(function (e) { e.classList.add('fade-rest'); }); },
    undim:  function (s) { $$('.fade-rest', s).forEach(function (e) { e.classList.remove('fade-rest'); }); },
    only: function (stage, a) {
      $$('[data-part]', stage).forEach(function (e) {
        var keep = a.targets.indexOf(e.getAttribute('data-part')) >= 0;
        e.classList.toggle('fade-rest', !keep);
      });
    },
    pulse:   function (s, a) { parts(s, a.targets).forEach(function (e) { e.classList.add('pulse-answer'); }); },
    unpulse: function (s, a) { parts(s, a.targets).forEach(function (e) { e.classList.remove('pulse-answer'); }); },
    trace: function (s, a) {
      parts(s, a.targets).forEach(function (e) { $$('path,line,polyline', e).forEach(function (p) { p.classList.add('trace-line'); }); });
    },
    bounce: function (s, a) {
      parts(s, a.targets).forEach(function (e) { restart(e, 'ba-bounce'); setTimeout(function () { e.classList.remove('ba-bounce'); }, 700); });
    },
    shake: function (s, a) {
      parts(s, a.targets).forEach(function (e) { restart(e, 'ba-shake'); setTimeout(function () { e.classList.remove('ba-shake'); }, 500); });
      buzz();
    },
    spot: function (stage, a) {
      VERBS.unspot(stage);
      var m = svgMetrics(stage), b = partBox(stage, a.targets[0]);
      if (!m || !b) return;
      var d = Math.max(b.w, b.h) * m.k * 1.35 + 26;
      var el = overlay(stage, 'focus-circle ba-fx', '');
      el.style.width = el.style.height = d + 'px';
      el.style.left = (m.ox + (b.x + b.w / 2) * m.k - d / 2) + 'px';
      el.style.top = (m.oy + (b.y + b.h / 2) * m.k - d / 2) + 'px';
    },
    unspot: function (stage) { $$('.focus-circle', stage).forEach(function (e) { e.remove(); }); },
    zoom: function (stage, a) {
      var z = $('.ba-zoom', stage), b = partBox(stage, a.targets[0]);
      if (!z || !b) return;
      var k = Math.min(3, Math.max(1.15, Math.min(VB_W / Math.max(b.w, 40), VB_H / Math.max(b.h, 30)) * 0.62));
      z.style.transform = 'translate(' + (VB_W / 2 - k * (b.x + b.w / 2)) + 'px,' +
        (VB_H / 2 - k * (b.y + b.h / 2)) + 'px) scale(' + k + ')';
    },
    unzoom: function (stage) { var z = $('.ba-zoom', stage); if (z) z.style.transform = ''; },
    label: function (stage, a) {
      a.targets.forEach(function (t) {
        $$('[data-label="' + t + '"]', stage).forEach(function (e) {
          if (a.text) { var tx = $('text', e); if (tx) tx.textContent = a.text; }
          restart(e, 'reveal-label');
        });
      });
      ding();
    },
    unlabel: function (stage, a) {
      parts_labels(stage, a.targets).forEach(function (e) { e.classList.remove('reveal-label'); });
    },
    tick:  function (stage) { verdict(stage, 'ba-tick', '✓'); ding(); },
    cross: function (stage) { verdict(stage, 'ba-cross', '✖'); buzz(); },
    think: function (stage) {
      VERBS.unthink(stage);
      stage.classList.add('ba-thinking');
      overlay(stage, 'think-delay', '<b></b><b></b><b></b>');
    },
    unthink: function (stage) {
      stage.classList.remove('ba-thinking');
      $$('.think-delay', stage).forEach(function (e) { e.remove(); });
    },
    note: function (stage, a) {
      var host = $('.ba-notes', stage); if (!host) return;
      var el = doc.createElement('div');
      el.className = 'ba-note';
      el.textContent = a.text || a.targets.join(' ');
      host.appendChild(el);
    },
    /* POSE — a whole composite change of state (a muscle pair swapping jobs,
       a lever moving). The asset ships CSS keyed on [data-pose="name"]. */
    pose: function (stage, a) { stage.setAttribute('data-pose', a.targets[0] || a.text || ''); },
    unpose: function (stage) { stage.removeAttribute('data-pose'); },
    wait: function () { /* a beat with narration only — nothing moves */ }
  };

  function parts_labels(stage, names) {
    var out = [];
    (names && names.length ? names : ['*']).forEach(function (nm) {
      $$(nm === '*' ? '[data-label]' : '[data-label="' + nm + '"]', stage).forEach(function (e) { out.push(e); });
    });
    return out;
  }

  function verdict(stage, cls, glyph) {
    $$('.ba-verdict', stage).forEach(function (e) { e.remove(); });
    overlay(stage, 'ba-verdict ' + cls, glyph);
  }

  /* ============================================================== stages */

  function scriptFor(stage) {
    var src = stage.getAttribute('data-ba-script') || '';
    var asset = stage.getAttribute('data-ba-asset');
    if (src.charAt(0) === '@' && asset && global.BioSVG) {
      src = global.BioSVG.script(asset, src.slice(1));
    }
    return src;
  }

  /* a comparison rail: several animals side by side, addressable as part#1.. */
  function railHTML(spec) {
    var sep = spec.indexOf('|') >= 0 ? '|' : ',';
    return '<div class="ba-rail">' + spec.split(sep).map(function (s) {
      var p = s.split(':'), a = p[0].trim(), nm = (p[1] || '').trim() || (global.BioSVG ? global.BioSVG.title(a) : a);
      return '<div class="ba-cell">' + (global.BioSVG ? global.BioSVG.render(a) : '') + '<span>' + nm + '</span></div>';
    }).join('') + '</div>';
  }

  function build(stage) {
    if (stage._ba) return stage._ba;
    var asset = stage.getAttribute('data-ba-asset');
    var rail = stage.getAttribute('data-ba-rail');
    var title = stage.getAttribute('data-ba-title');

    stage.innerHTML =
      (stage.getAttribute('data-ba-nobar') === null ? barHTML() : '') +
      (title ? '<p class="ba-note" style="margin-top:0">' + title + '</p>' : '') +
      '<div class="ba-canvas">' +
        (rail ? railHTML(rail) : (asset && global.BioSVG ? global.BioSVG.render(asset) : '')) +
      '</div><div class="ba-notes"></div>';

    var st = stage._ba = { steps: [], i: 0 };
    wireBar(stage);
    loadScript(stage, scriptFor(stage));
    return st;
  }

  function barHTML() {
    return '<div class="ba-bar">' +
      '<button type="button" class="ba-next">▶ Next</button>' +
      '<span class="ba-dots"></span>' +
      '<span class="ba-say" aria-live="polite"></span>' +
      '<button type="button" class="ba-mini ba-all">⏭ Show all</button>' +
      '<button type="button" class="ba-mini ba-reset">↺ Replay</button>' +
      '</div>';
  }

  function wireBar(stage) {
    var b = $('.ba-bar', stage); if (!b) return;
    $('.ba-next', b).addEventListener('click', function () { next(stage); });
    $('.ba-all', b).addEventListener('click', function () { all(stage); });
    $('.ba-reset', b).addEventListener('click', function () { reset(stage); });
  }

  function loadScript(stage, src) {
    var st = stage._ba || (stage._ba = { steps: [], i: 0 });
    st.steps = parseScript(src);
    st.hidden = hiddenParts(st.steps);
    reset(stage);
  }

  /* Elements elsewhere on the slide that follow this stage's step count.
     Tie them to one particular stage with data-ba-for="<stage id>" when a
     slide carries more than one stage. */
  function followers(stage) {
    var slide = (stage.closest && stage.closest('.slide')) || doc;
    var id = stage.id;
    if (id && $('[data-ba-step][data-ba-for="' + id + '"]', slide)) {
      return $$('[data-ba-step][data-ba-for="' + id + '"]', slide);
    }
    return $$('[data-ba-step]:not([data-ba-for])', slide);
  }

  function reset(stage) {
    var st = stage._ba; if (!st) return;
    st.i = 0;
    $$('[data-part]', stage).forEach(function (e) {
      e.classList.remove('glow-path', 'highlight-region', 'fade-rest', 'pulse-answer', 'ba-drew', 'ba-bounce', 'ba-shake', 'ba-fadein');
      e.classList.toggle('ba-hidden', !!st.hidden[e.getAttribute('data-part')]);
      $$('*', e).forEach(function (k) { k.classList.remove('ba-pop', 'draw-svg', 'trace-line'); k.style.animationDelay = ''; });
    });
    $$('[data-label]', stage).forEach(function (e) { e.classList.remove('reveal-label'); });
    $$('.focus-circle,.ba-verdict,.think-delay', stage).forEach(function (e) { e.remove(); });
    stage.classList.remove('ba-thinking');
    stage.removeAttribute('data-pose');
    VERBS.unzoom(stage);
    var notes = $('.ba-notes', stage); if (notes) notes.innerHTML = '';
    var say = $('.ba-say', stage); if (say) { say.textContent = ''; say.classList.remove('ba-said'); }
    followers(stage).forEach(function (e) { e.classList.remove('ba-shown'); });
    /* data-ba-static: annotation that is always on — a permanently labelled
       diagram rather than a sequence. Re-applied after every reset. */
    var stat = stage.getAttribute('data-ba-static');
    if (stat) {
      parseScript(stat).forEach(function (st) {
        st.acts.forEach(function (a) { if (VERBS[a.verb]) VERBS[a.verb](stage, a); });
      });
    }
    paint(stage);
  }

  function step(stage, n) {
    var st = stage._ba; if (!st || n >= st.steps.length) return false;
    var s = st.steps[n];
    s.acts.forEach(function (a) { if (VERBS[a.verb]) VERBS[a.verb](stage, a); });
    followers(stage).forEach(function (e) {
      if (parseInt(e.getAttribute('data-ba-step'), 10) === n + 1) restart(e, 'ba-shown');
    });
    var say = $('.ba-say', stage);
    if (say) { say.textContent = s.say || ''; restart(say, 'ba-said'); }
    return true;
  }

  function next(stage) {
    var st = stage._ba; if (!st) return false;
    if (st.i >= st.steps.length) return false;
    /* The class has had its say — clear the waiting state however we got here
       (stage button, slide Next, or the arrow keys). */
    if (st.i === 0) VERBS.unthink(stage);
    step(stage, st.i);
    st.i++;
    paint(stage);
    if (st.i >= st.steps.length && typeof stage._baDone === 'function') stage._baDone(stage);
    return true;
  }

  function all(stage) {
    var st = stage._ba; if (!st) return;
    VERBS.unthink(stage);
    while (st.i < st.steps.length) { step(stage, st.i); st.i++; }
    paint(stage);
    if (typeof stage._baDone === 'function') stage._baDone(stage);
  }

  function paint(stage) {
    var st = stage._ba, bar = $('.ba-bar', stage); if (!st || !bar) return;
    var dots = $('.ba-dots', bar);
    if (dots) {
      if (dots.children.length !== st.steps.length) {
        dots.innerHTML = st.steps.map(function () { return '<i></i>'; }).join('');
      }
      $$('i', dots).forEach(function (d, i) { d.classList.toggle('on', i < st.i); });
    }
    var nb = $('.ba-next', bar);
    if (nb) {
      var done = st.i >= st.steps.length;
      nb.disabled = done;
      nb.textContent = done ? '✓ All shown' : (st.i === 0 ? '▶ Start' : '▶ Next (' + (st.i + 1) + '/' + st.steps.length + ')');
    }
  }

  /* swap a stage onto a different animal / script at runtime */
  function load(stage, assetName, which) {
    build(stage);
    var canvas = $('.ba-canvas', stage);
    canvas.innerHTML = global.BioSVG ? global.BioSVG.render(assetName) : '';
    $$('.focus-circle,.ba-verdict,.think-delay', stage).forEach(function (e) { e.remove(); });
    stage.setAttribute('data-ba-asset', assetName);
    loadScript(stage, global.BioSVG ? global.BioSVG.script(assetName, which || 'reveal') : '');
  }

  /* ============================================ "is this a vertebrate?" panel */

  /* data-ba-cards / data-ba-animals: "asset:Label" per card, separated by | (or
     by , when no label contains one). A third field names which of the asset's
     scripts to run, so one asset can answer several different questions. */
  function buildPredict(host) {
    var raw = host.getAttribute('data-ba-cards') || host.getAttribute('data-ba-animals') || '';
    var spec = raw.split(raw.indexOf('|') >= 0 ? '|' : ',')
      .map(function (s) { return s.trim(); }).filter(Boolean)
      .map(function (s) {
        var p = s.split(':');
        return {
          asset: p[0].trim(),
          name: (p[1] || '').trim() || p[0].trim(),
          script: (p[2] || '').trim() || 'reveal'
        };
      });

    var voteA = host.getAttribute('data-ba-vote-a') || '● Backbone (vertebrate)';
    var voteB = host.getAttribute('data-ba-vote-b') || '■ No backbone (invertebrate)';

    host.innerHTML =
      '<div class="ba-predict-cards">' + spec.map(function (s, i) {
        return '<button type="button" class="ba-pc" data-i="' + i + '">' + s.name + '</button>';
      }).join('') + '</div>' +
      '<div class="ba-vote"><span class="ba-chip">' + voteA + '</span>' +
      '<span class="ba-chip ba-chip-b">' + voteB + '</span>' +
      '<span class="ba-tally">Checked <strong class="ba-count">0</strong>/' + spec.length + '</span></div>' +
      '<div class="ba-stage ba-plain" data-ba-frame="wide"></div>';

    var stage = $('.ba-stage', host);
    build(stage);
    var count = 0, seen = {};

    stage._baDone = function () {
      var i = host._baCur;
      if (i == null || seen[i]) return;
      seen[i] = true; count++;
      $('.ba-count', host).textContent = count;
      try { if (typeof global.gainXP === 'function') global.gainXP(); } catch (e) {}
      var card = $('.ba-pc[data-i="' + i + '"]', host);
      if (card) card.classList.add('ba-done');
    };

    $$('.ba-pc', host).forEach(function (card) {
      card.addEventListener('click', function () {
        var i = +card.getAttribute('data-i');
        host._baCur = i;
        $$('.ba-pc', host).forEach(function (c) { c.classList.remove('ba-current'); });
        card.classList.add('ba-current');
        load(stage, spec[i].asset, spec[i].script);
        VERBS.think(stage, {});
        var say = $('.ba-say', stage);
        if (say) { say.textContent = spec[i].name + ' — vertebrate or invertebrate? Everybody decide. Then I press Next.'; restart(say, 'ba-said'); }
      });
    });

    host._baStage = stage;
    return stage;
  }

  /* ================================================== navigation plumbing */

  function activeRoot() { return $('.slide.active') || doc.body; }

  function advanceActive() {
    var root = activeRoot();
    var stages = $$('.ba-stage', root).filter(function (s) {
      return s._ba && s._ba.steps.length && s._ba.i < s._ba.steps.length;
    });
    if (!stages.length) return false;
    return next(stages[0]);
  }

  function hookNav() {
    if (typeof global.nextSlide !== 'function' || global.nextSlide._baWrapped) return;
    var orig = global.nextSlide;
    var wrapped = function () { if (advanceActive()) return; orig.apply(this, arguments); };
    wrapped._baWrapped = true;
    global.nextSlide = wrapped;

    if (typeof global.showSlide === 'function' && !global.showSlide._baWrapped) {
      var os = global.showSlide;
      var ws = function (i) {
        os.apply(this, arguments);
        setTimeout(function () { $$('.ba-stage', activeRoot()).forEach(reset); }, 20);
      };
      ws._baWrapped = true;
      global.showSlide = ws;
    }
  }

  /* ============================================================ named API */

  function stageOf(x) {
    if (!x) return $('.ba-stage');
    if (typeof x === 'string') return $(x);
    return x.classList && x.classList.contains('ba-stage') ? x : (x.closest ? x.closest('.ba-stage') : x);
  }

  function drawSkeleton(x)          { var s = stageOf(x); VERBS.draw(s, { targets: ['skull', 'ribs', 'pelvis', 'limbs'] }); VERBS.pop(s, { targets: ['spine'] }); }
  function highlightBone(x, part)   { var s = stageOf(x); VERBS.glow(s, { targets: [part || 'spine'] }); VERBS.hi(s, { targets: [part || 'spine'] }); }
  function traceBackbone(x)         { VERBS.trace(stageOf(x), { targets: ['spine'] }); }
  function revealLabels(x)          { parts_labels(stageOf(x), ['*']).forEach(function (e) { restart(e, 'reveal-label'); }); }
  function pulseCorrect(el)         { if (el) { restart(el, 'ba-bounce'); ding(); setTimeout(function () { el.classList.remove('ba-bounce'); }, 700); } }
  function shakeWrong(el)           { if (el) { restart(el, 'ba-shake'); buzz(); setTimeout(function () { el.classList.remove('ba-shake'); }, 500); } }
  function zoomFeature(x, part)     { VERBS.zoom(stageOf(x), { targets: [part || 'spine'] }); }
  function fadeOthers(x, keep)      { VERBS.only(stageOf(x), { targets: [].concat(keep || 'spine') }); }

  /* ================================================================ init */

  function init(root) {
    $$('.ba-predict[data-ba-animals],.ba-predict[data-ba-cards]', root || doc).forEach(function (h) { if (!h._baBuilt) { h._baBuilt = true; buildPredict(h); } });
    $$('.ba-stage', root || doc).forEach(function (s) { if (!s._ba) build(s); });
    hookNav();
  }

  BA.init = init;
  BA.build = build;
  BA.load = load;
  BA.next = function (x) { return next(stageOf(x)); };
  BA.reset = function (x) { return reset(stageOf(x)); };
  BA.all = function (x) { return all(stageOf(x)); };
  BA.run = function (x, verb, targets, text) { var s = stageOf(x); if (VERBS[verb]) VERBS[verb](s, { targets: [].concat(targets || []), text: text || null }); };
  BA.advanceActive = advanceActive;
  BA.hookNav = hookNav;
  BA.parse = parseScript;
  BA.verbs = VERBS;

  global.BuildAnim = BA;
  global.drawSkeleton = drawSkeleton;
  global.highlightBone = highlightBone;
  global.traceBackbone = traceBackbone;
  global.revealLabels = revealLabels;
  global.pulseCorrect = pulseCorrect;
  global.shakeWrong = shakeWrong;
  global.zoomFeature = zoomFeature;
  global.fadeOthers = fadeOthers;

  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', function () { init(); });
  else setTimeout(function () { init(); }, 0);

})(typeof window !== 'undefined' ? window : this, document);
