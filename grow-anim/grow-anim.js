/* ============================================================================
   GROW ANIMATION FRAMEWORK · engine
   ---------------------------------------------------------------------------
   Phases 3–11 of the framework live here. The motion vocabulary itself lives in
   grow-motion.css; this file only ever SEQUENCES it.

   THE TEACHING MODEL
     A slide holds a STAGE. A stage holds a layered SVG and a SCRIPT. The
     teacher presses ▶ Next; one step fires; the teacher narrates the line the
     framework prints for them. Pupils cannot read ahead because nothing has
     been written yet — the words arrive only after the picture has made the
     point.

   THE FIVE BEATS (Phase 3)
     observe -> notice -> think -> explain -> label
     Every step may declare its beat. The bar shows it, so the teacher always
     knows whether they are showing, questioning, explaining or confirming.

   MARKUP
     <div class="g-stage" data-grow-asset="circuit" data-grow-script="@teach"></div>

     data-grow-asset    name from any registered GrowSVG library
     data-grow-script   an inline script, or @teach / @reveal / @process / @story
     data-grow-rail     "human:Human, fish:Fish"  — comparison rail
     data-grow-dual     "ball|forces"             — real world | model (Phase 8)
     data-grow-static   steps applied on every reset (a permanently labelled
                        diagram rather than a sequence)
     data-grow-title    caption above the picture
     data-grow-nobar    present = no control bar (driven by code instead)
     data-grow-overlays "force,friction,energy"   — invisible-science switches
     data-grow-frame    mini | wide | tall

     Anything on the slide carrying data-grow-step="3" appears at step 3. Use it
     for the definition that CONFIRMS what the animation has already shown.

   SCRIPT FORMAT — one step per line, one press of ▶ Next per step
     [beat] verb targets + verb targets :: what the teacher says
     e.g.  notice: glow lamp + flow current :: The lamp only lights when the
                                               loop is complete.

   VERBS
     THE TEN         draw pop glow pulse fade morph flow shake bounce trace zoom
     SUPPORTING      show hide unglow hi unhi unfade only unpulse untrace unzoom
                     spot unspot label unlabel tick cross think unthink note wait
     TEACHING        pause overlay unoverlay heat beat

   PUBLIC API
     GrowAnim.init/next/reset/all/load/run/advanceActive
     plus the named helpers at the foot of the file.
   ========================================================================== */
(function (global, doc) {
  'use strict';

  var VB_W = 400, VB_H = 300;
  var GA = {};
  var BEATS = ['observe', 'notice', 'think', 'explain', 'label', 'apply'];

  function $(sel, root) { return (root || doc).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || doc).querySelectorAll(sel)); }
  function ding() { try { if (typeof global.playDing === 'function') global.playDing(); } catch (e) {} }
  function buzz() { try { if (typeof global.playBuzz === 'function') global.playBuzz(); } catch (e) {} }
  function lib() { return global.GrowSVG; }

  /* ======================================================== script parsing */

  function parseScript(src) {
    if (!src) return [];
    return src.split('\n').map(function (l) { return l.trim(); })
      .filter(function (l) { return l && l.charAt(0) !== '#'; })
      .map(function (line) {
        /* optional leading beat:  "notice: glow spine :: …" */
        var beat = null;
        var bm = line.match(/^([a-z]+)\s*:(?!:)\s*/i);
        if (bm && BEATS.indexOf(bm[1].toLowerCase()) >= 0) {
          beat = bm[1].toLowerCase();
          line = line.slice(bm[0].length);
        }
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
        return { acts: acts, say: say, beat: beat };
      });
  }

  /* Parts a script switches ON at some point start hidden — so there is
     genuinely nothing on screen for a pupil to read ahead into. */
  function hiddenParts(steps) {
    var set = {};
    steps.forEach(function (st) {
      st.acts.forEach(function (a) {
        if (a.verb === 'show' || a.verb === 'draw' || a.verb === 'pop') {
          a.targets.forEach(function (t) { set[t.split('#')[0]] = true; });
        }
        if (a.verb === 'morph') {
          a.targets.forEach(function (t) {
            var to = t.split('>')[1];
            if (to) set[to.trim().split('#')[0]] = true;
          });
        }
      });
    });
    return set;
  }

  /* =============================================================== geometry */

  function svgMetrics(stage) {
    var svg = $('.g-svg', stage), canvas = $('.g-canvas', stage);
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
    var els = parts(stage, [name]);
    if (!els.length) return null;
    var box = null;
    els.forEach(function (el) {
      var b; try { b = el.getBBox(); } catch (e) { return; }
      if (!b || (!b.width && !b.height)) return;
      if (!box) { box = { x: b.x, y: b.y, w: b.width, h: b.height }; return; }
      var x2 = Math.max(box.x + box.w, b.x + b.width), y2 = Math.max(box.y + box.h, b.y + b.height);
      box.x = Math.min(box.x, b.x); box.y = Math.min(box.y, b.y);
      box.w = x2 - box.x; box.h = y2 - box.y;
    });
    return box;
  }

  /* ================================================================= verbs */

  /* Targets are part names. In a rail or a dual stage, "body#2" means "the
     body of the SECOND panel"; everything else addresses every panel. */
  function parts(stage, names) {
    if (!names || !names.length || names[0] === '*') return $$('[data-part]', stage);
    var out = [];
    names.forEach(function (nm) {
      nm = nm.split('>')[0].trim();
      var h = nm.indexOf('#'), sel;
      if (h > 0) {
        sel = '.g-cell:nth-of-type(' + parseInt(nm.slice(h + 1), 10) + ') [data-part="' + nm.slice(0, h) + '"],' +
              '.g-dual > figure:nth-of-type(' + parseInt(nm.slice(h + 1), 10) + ') [data-part="' + nm.slice(0, h) + '"]';
      } else {
        sel = '[data-part="' + nm + '"]';
      }
      $$(sel, stage).forEach(function (e) { if (out.indexOf(e) < 0) out.push(e); });
    });
    return out;
  }

  function restart(el, cls) {
    el.classList.remove(cls);
    el.getBoundingClientRect();          /* force reflow so the animation replays */
    el.classList.add(cls);
  }

  function overlayEl(stage, cls, html) {
    var canvas = $('.g-canvas', stage) || stage;
    var el = doc.createElement('div');
    el.className = cls;
    el.innerHTML = html || '';
    canvas.appendChild(el);
    return el;
  }

  function show(stage, a) {
    parts(stage, a.targets).forEach(function (e) {
      e.classList.remove('g-hidden');
      restart(e, 'g-in');
    });
  }

  var VERBS = {

    /* ---------------------------------------------------- the ten motions */

    /* DRAW — a structure is forming */
    draw: function (stage, a) {
      parts(stage, a.targets).forEach(function (e) {
        e.classList.remove('g-hidden');
        $$('path,line,polyline,polygon,rect,circle,ellipse', e).forEach(function (s) { restart(s, 'g-draw'); });
      });
    },
    /* POP — the same message, but countable: parts arriving one at a time */
    pop: function (stage, a) {
      parts(stage, a.targets).forEach(function (e) {
        e.classList.remove('g-hidden');
        $$('*', e).filter(function (k) { return k.tagName !== 'text' && k.tagName !== 'tspan'; })
          .forEach(function (k, i) {
            k.style.animationDelay = (i * 0.085) + 's';
            restart(k, 'g-draw-pop');
          });
      });
      ding();
    },

    /* GLOW — this is the important feature */
    glow:   function (s, a) { parts(s, a.targets).forEach(function (e) { e.classList.add('g-glow'); }); },
    unglow: function (s, a) { parts(s, a.targets).forEach(function (e) { e.classList.remove('g-glow'); }); },
    hi:     function (s, a) { parts(s, a.targets).forEach(function (e) { e.classList.add('g-hi'); }); ding(); },
    unhi:   function (s, a) { parts(s, a.targets).forEach(function (e) { e.classList.remove('g-hi'); }); },

    /* PULSE — pay attention, look here now */
    pulse:   function (s, a) { parts(s, a.targets).forEach(function (e) { e.classList.add('g-pulse'); }); },
    unpulse: function (s, a) { parts(s, a.targets).forEach(function (e) { e.classList.remove('g-pulse'); }); },

    /* FADE — this matters less right now */
    fade:   function (s, a) { parts(s, a.targets).forEach(function (e) { e.classList.add('g-fade'); }); },
    unfade: function (s) { $$('.g-fade', s).forEach(function (e) { e.classList.remove('g-fade'); }); },
    only: function (stage, a) {
      $$('[data-part]', stage).forEach(function (e) {
        e.classList.toggle('g-fade', a.targets.indexOf(e.getAttribute('data-part')) < 0);
      });
    },

    /* MORPH — something is CHANGING.  "morph ice>water" */
    morph: function (stage, a) {
      a.targets.forEach(function (t) {
        var pair = t.split('>');
        var from = pair[0].trim(), to = (pair[1] || '').trim();
        parts(stage, [from]).forEach(function (e) {
          e.classList.remove('g-morph-in');
          restart(e, 'g-morph-out');
          setTimeout(function () { e.classList.add('g-hidden'); }, 850);
        });
        if (!to) return;
        parts(stage, [to]).forEach(function (e) {
          e.classList.remove('g-hidden', 'g-morph-out');
          restart(e, 'g-morph-in');
        });
      });
      ding();
    },

    /* FLOW — something is MOVING.  Along a named path if the layer declares
       one (data-flow-along="#loop"), otherwise a steady drift.            */
    flow: function (stage, a) {
      parts(stage, a.targets).forEach(function (e) {
        e.classList.remove('g-hidden');
        /* going round something — a planet, a moon, a loop of current */
        var orbit = e.getAttribute('data-flow-orbit');
        if (orbit) {
          var o = orbit.split(/[\s,]+/);
          e.style.transformOrigin = o[0] + 'px ' + o[1] + 'px';
          if (o[2]) e.style.setProperty('--g-orbit', o[2] + 's');
          e.classList.add('g-flow-orbit');
          return;
        }
        var along = e.getAttribute('data-flow-along');
        var d = along ? (($(along, stage) || {}).getAttribute ? $(along, stage).getAttribute('d') : null) : null;
        var movers = $$('[data-flow-item]', e);
        if (!movers.length) movers = [e];
        movers.forEach(function (m, i) {
          if (d) {
            m.style.offsetPath = 'path("' + d + '")';
            m.style.webkitOffsetPath = 'path("' + d + '")';
            m.style.animationDelay = (i * (2.4 / movers.length)) + 's';
            m.classList.add('g-flow');
          } else {
            m.style.animationDelay = (i * 0.22) + 's';
            m.classList.add('g-flow-drift');
          }
        });
      });
    },
    unflow: function (s, a) {
      parts(s, a.targets).forEach(function (e) {
        [e].concat($$('[data-flow-item]', e)).forEach(function (m) {
          m.classList.remove('g-flow', 'g-flow-drift', 'g-flow-orbit');
          m.style.animationDelay = '';
        });
      });
    },
    /* particles jiggling on the spot — the model of temperature */
    jiggle: function (stage, a) {
      parts(stage, a.targets).forEach(function (e) {
        e.classList.remove('g-hidden');
        var items = $$('circle,rect,ellipse,path', e);
        (items.length ? items : [e]).forEach(function (m, i) {
          m.style.animationDelay = ((i % 7) * 0.06) + 's';
          m.classList.add('g-flow-jiggle');
        });
      });
    },
    /* heat 0..3 — how hard the particles jiggle. The one dial that makes
       "hotter means faster" visible rather than asserted. */
    heat: function (stage, a) {
      /* "heat solid 2.6" — the value is the last bare number, whether it was
         written after the part name or as a quoted argument. */
      var names = [], v = NaN;
      a.targets.forEach(function (t) {
        t.split(/\s+/).forEach(function (tok) {
          if (!tok) return;
          if (/^[0-9]*\.?[0-9]+$/.test(tok)) v = parseFloat(tok);
          else names.push(tok);
        });
      });
      if (a.text != null && /^[0-9]*\.?[0-9]+$/.test(String(a.text).trim())) v = parseFloat(a.text);
      if (isNaN(v)) v = 1;
      parts(stage, names.length ? names : ['*']).forEach(function (e) {
        [e].concat($$('*', e)).forEach(function (m) {
          if (m.style) m.style.setProperty('--g-heat', String(Math.max(0.15, v)));
        });
      });
    },

    /* SHAKE — that idea is incorrect.  Nothing else in GROW may shake. */
    shake: function (s, a) {
      parts(s, a.targets).forEach(function (e) {
        restart(e, 'g-shake');
        setTimeout(function () { e.classList.remove('g-shake'); }, 520);
      });
      buzz();
    },
    /* BOUNCE — that answer is correct. */
    bounce: function (s, a) {
      parts(s, a.targets).forEach(function (e) {
        restart(e, 'g-bounce');
        setTimeout(function () { e.classList.remove('g-bounce'); }, 700);
      });
      ding();
    },

    /* TRACE — follow this pathway */
    trace: function (s, a) {
      parts(s, a.targets).forEach(function (e) {
        var lines = $$('path,line,polyline', e);
        (lines.length ? lines : [e]).forEach(function (p) { p.classList.add('g-trace'); });
      });
    },
    untrace: function (s, a) {
      parts(s, a.targets).forEach(function (e) {
        [e].concat($$('path,line,polyline', e)).forEach(function (p) { p.classList.remove('g-trace'); });
      });
    },

    /* ZOOM — look closer.  The camera moves, not the specimen. */
    zoom: function (stage, a) {
      var b = partBox(stage, a.targets[0]);
      if (!b) return;
      var k = Math.min(3, Math.max(1.15, Math.min(VB_W / Math.max(b.w, 40), VB_H / Math.max(b.h, 30)) * 0.62));
      $$('.g-zoom-layer', stage).forEach(function (z) {
        z.style.transform = 'translate(' + (VB_W / 2 - k * (b.x + b.w / 2)) + 'px,' +
          (VB_H / 2 - k * (b.y + b.h / 2)) + 'px) scale(' + k + ')';
      });
    },
    unzoom: function (stage) { $$('.g-zoom-layer', stage).forEach(function (z) { z.style.transform = ''; }); },

    /* ------------------------------------------------ supporting marks */

    show: show,
    hide: function (stage, a) { parts(stage, a.targets).forEach(function (e) { e.classList.add('g-hidden'); }); },

    spot: function (stage, a) {
      VERBS.unspot(stage);
      var m = svgMetrics(stage), b = partBox(stage, a.targets[0]);
      if (!m || !b) return;
      var d = Math.max(b.w, b.h) * m.k * 1.35 + 26;
      var el = overlayEl(stage, 'g-spot');
      el.style.width = el.style.height = d + 'px';
      el.style.left = (m.ox + (b.x + b.w / 2) * m.k - d / 2) + 'px';
      el.style.top  = (m.oy + (b.y + b.h / 2) * m.k - d / 2) + 'px';
    },
    unspot: function (stage) { $$('.g-spot', stage).forEach(function (e) { e.remove(); }); },

    /* the words arrive only after the picture has made the point */
    label: function (stage, a) {
      a.targets.forEach(function (t) {
        $$('[data-label="' + t + '"]', stage).forEach(function (e) {
          if (a.text) { var tx = $('text', e); if (tx) tx.textContent = a.text; }
          restart(e, 'g-labelled');
        });
      });
      ding();
    },
    unlabel: function (stage, a) {
      labels(stage, a.targets).forEach(function (e) { e.classList.remove('g-labelled'); });
    },

    tick:  function (stage) { verdict(stage, 'g-tick', '✓'); ding(); },
    cross: function (stage) { verdict(stage, 'g-cross', '✖'); buzz(); },

    think: function (stage) {
      VERBS.unthink(stage);
      stage.classList.add('g-thinking');
      overlayEl(stage, 'g-think', '<b></b><b></b><b></b>');
    },
    unthink: function (stage) {
      stage.classList.remove('g-thinking');
      $$('.g-think', stage).forEach(function (e) { e.remove(); });
    },

    note: function (stage, a) {
      var host = $('.g-notes', stage); if (!host) return;
      var el = doc.createElement('div');
      el.className = 'g-note';
      el.textContent = a.text || a.targets.join(' ');
      host.appendChild(el);
    },

    /* ------------------------------------------- Phase 6 · invisible science */
    overlay: function (stage, a) {
      a.targets.forEach(function (t) { setOverlay(stage, t, true); });
    },
    unoverlay: function (stage, a) {
      if (!a.targets.length) { $$('[data-overlay]', stage).forEach(function (e) { e.classList.remove('on'); }); syncXray(stage); return; }
      a.targets.forEach(function (t) { setOverlay(stage, t, false); });
    },

    /* ------------------------------------------------ Phase 7 · prediction */
    /* pause "What happens next?"  — the animation stops dead and asks.       */
    pause: function (stage, a) {
      var st = stage._g; if (!st) return;
      st.paused = true;
      var q = a.text || a.targets.join(' ') || 'What happens next?';
      var el = overlayEl(stage, 'g-pause',
        '<span class="g-pause-tag">PREDICT</span><h4></h4>' +
        '<button type="button">Everyone decided — reveal ▶</button>');
      $('h4', el).textContent = q;
      $('button', el).addEventListener('click', function () {
        el.remove();
        st.paused = false;
        paint(stage);
        next(stage);
      });
      paint(stage);
    },

    beat: function () { /* declared as a prefix; nothing to do at run time */ },
    wait: function () { /* a beat with narration only — nothing moves */ }
  };

  function labels(stage, names) {
    var out = [];
    (names && names.length ? names : ['*']).forEach(function (nm) {
      $$(nm === '*' ? '[data-label]' : '[data-label="' + nm + '"]', stage).forEach(function (e) { out.push(e); });
    });
    return out;
  }

  function verdict(stage, cls, glyph) {
    $$('.g-verdict', stage).forEach(function (e) { e.remove(); });
    overlayEl(stage, 'g-verdict ' + cls, glyph);
  }

  /* ==================================== Phase 6 · invisible-science overlays */

  function setOverlay(stage, name, on) {
    $$('[data-overlay="' + name + '"]', stage).forEach(function (e) { e.classList.toggle('on', !!on); });
    syncXray(stage);
  }

  function syncXray(stage) {
    $$('.g-xray button', stage).forEach(function (b) {
      var name = b.getAttribute('data-layer');
      var any = $$('[data-overlay="' + name + '"]', stage).some(function (e) { return e.classList.contains('on'); });
      b.classList.toggle('on', any);
      b.setAttribute('aria-pressed', any ? 'true' : 'false');
    });
  }

  /* The switch strip. Labels are deliberately plain English — "Forces",
     "Energy" — because the point is that these things were always there. */
  var XRAY_NAMES = {
    force: 'Forces', friction: 'Friction', gravity: 'Gravity', reaction: 'Reaction',
    energy: 'Energy', heat: 'Heat', particle: 'Particles', field: 'Field',
    current: 'Current', pressure: 'Pressure', light: 'Light rays', air: 'Air resistance'
  };

  function xrayHTML(list) {
    return '<div class="g-xray"><span class="g-xray-label">See the invisible</span>' +
      list.map(function (n) {
        return '<button type="button" data-layer="' + n + '" aria-pressed="false">' +
          (XRAY_NAMES[n] || n.charAt(0).toUpperCase() + n.slice(1)) + '</button>';
      }).join('') + '</div>';
  }

  function wireXray(stage) {
    $$('.g-xray button', stage).forEach(function (b) {
      b.addEventListener('click', function () {
        var name = b.getAttribute('data-layer');
        setOverlay(stage, name, !b.classList.contains('on'));
      });
    });
  }

  /* ================================================================ stages */

  function scriptFor(stage) {
    var src = stage.getAttribute('data-grow-script') || '';
    var asset = stage.getAttribute('data-grow-asset') ||
      (stage.getAttribute('data-grow-dual') || '').split('|')[0];
    if (src.charAt(0) === '@' && asset && lib()) {
      src = lib().script(asset.trim(), src.slice(1));
    }
    return src;
  }

  function render(name) { return lib() ? lib().render(name) : ''; }
  function titleOf(name) { return lib() ? lib().title(name) : name; }

  /* a comparison rail: several specimens side by side, addressable as part#1.. */
  function railHTML(spec) {
    var sep = spec.indexOf('|') >= 0 ? '|' : ',';
    return '<div class="g-rail">' + spec.split(sep).map(function (s) {
      var p = s.split(':'), a = p[0].trim(), nm = (p[1] || '').trim() || titleOf(a);
      return '<div class="g-cell">' + render(a) + '<span>' + nm + '</span></div>';
    }).join('') + '</div>';
  }

  /* Phase 8 · dual representation — real world | scientific model, one script */
  function dualHTML(spec) {
    var p = spec.split('|').map(function (s) { return s.trim(); });
    var caps = ['REAL WORLD', 'SCIENTIFIC MODEL'];
    return '<div class="g-dual">' + p.map(function (s, i) {
      var q = s.split(':'), a = q[0].trim(), cap = (q[1] || '').trim() || caps[i] || 'MODEL';
      return '<figure><figcaption>' + cap + '</figcaption>' + render(a) + '</figure>';
    }).join('') + '</div>';
  }

  function barHTML() {
    return '<div class="g-bar">' +
      '<button type="button" class="g-next">▶ Start</button>' +
      '<span class="g-beat" data-beat="observe">observe</span>' +
      '<span class="g-dots"></span>' +
      '<span class="g-say" aria-live="polite"></span>' +
      '<button type="button" class="g-mini g-all">⏭ Show all</button>' +
      '<button type="button" class="g-mini g-reset">↺ Replay</button>' +
      '</div>';
  }

  function build(stage) {
    if (stage._g) return stage._g;
    var asset = stage.getAttribute('data-grow-asset');
    var rail  = stage.getAttribute('data-grow-rail');
    var dual  = stage.getAttribute('data-grow-dual');
    var title = stage.getAttribute('data-grow-title');
    var overs = (stage.getAttribute('data-grow-overlays') || '').split(',')
      .map(function (s) { return s.trim(); }).filter(Boolean);

    stage.innerHTML =
      (stage.getAttribute('data-grow-nobar') === null ? barHTML() : '') +
      (overs.length ? xrayHTML(overs) : '') +
      (title ? '<p class="g-note" style="margin-top:0">' + title + '</p>' : '') +
      '<div class="g-canvas">' +
        (dual ? dualHTML(dual) : rail ? railHTML(rail) : asset ? render(asset) : '') +
      '</div><div class="g-notes"></div>';

    var st = stage._g = { steps: [], i: 0, paused: false };
    wireBar(stage);
    wireXray(stage);
    if (global.GrowPolish) global.GrowPolish.decorate(stage);
    loadScript(stage, scriptFor(stage));
    return st;
  }

  function wireBar(stage) {
    var b = $('.g-bar', stage); if (!b) return;
    $('.g-next',  b).addEventListener('click', function () { next(stage); });
    $('.g-all',   b).addEventListener('click', function () { all(stage); });
    $('.g-reset', b).addEventListener('click', function () { reset(stage); });
  }

  function loadScript(stage, src) {
    var st = stage._g || (stage._g = { steps: [], i: 0, paused: false });
    st.steps = parseScript(src);
    st.hidden = hiddenParts(st.steps);
    reset(stage);
  }

  /* Text elsewhere on the slide that follows this stage's step count. Tie it
     to one stage with data-grow-for="<stage id>" when a slide has several. */
  function followers(stage) {
    var slide = (stage.closest && (stage.closest('.slide') || stage.closest('section'))) || doc;
    var id = stage.id;
    if (id && $('[data-grow-step][data-grow-for="' + id + '"]', slide)) {
      return $$('[data-grow-step][data-grow-for="' + id + '"]', slide);
    }
    return $$('[data-grow-step]:not([data-grow-for])', slide);
  }

  function reset(stage) {
    var st = stage._g; if (!st) return;
    st.i = 0; st.paused = false;
    $$('[data-part]', stage).forEach(function (e) {
      e.classList.remove('g-glow', 'g-hi', 'g-fade', 'g-pulse', 'g-bounce', 'g-shake',
        'g-in', 'g-trace', 'g-flow', 'g-flow-drift', 'g-flow-orbit', 'g-flow-jiggle', 'g-morph-in', 'g-morph-out');
      e.classList.toggle('g-hidden', !!st.hidden[e.getAttribute('data-part')]);
      e.style.animationDelay = '';
      $$('*', e).forEach(function (k) {
        k.classList.remove('g-draw-pop', 'g-draw', 'g-trace', 'g-flow', 'g-flow-drift', 'g-flow-orbit', 'g-flow-jiggle');
        if (k.style) { k.style.animationDelay = ''; k.style.offsetPath = ''; k.style.removeProperty('--g-heat'); }
      });
    });
    $$('[data-label]', stage).forEach(function (e) { e.classList.remove('g-labelled'); });
    $$('[data-overlay]', stage).forEach(function (e) { e.classList.remove('on'); });
    $$('.g-spot,.g-verdict,.g-think,.g-pause', stage).forEach(function (e) { e.remove(); });
    stage.classList.remove('g-thinking');
    VERBS.unzoom(stage);
    syncXray(stage);
    var notes = $('.g-notes', stage); if (notes) notes.innerHTML = '';
    var say = $('.g-say', stage); if (say) { say.textContent = ''; say.classList.remove('g-said'); }
    followers(stage).forEach(function (e) { e.classList.remove('g-shown'); });

    /* data-grow-static: a permanently annotated diagram rather than a
       sequence. Re-applied after every reset. */
    var stat = stage.getAttribute('data-grow-static');
    if (stat) {
      parseScript(stat).forEach(function (s) {
        s.acts.forEach(function (a) { if (VERBS[a.verb]) VERBS[a.verb](stage, a); });
      });
    }
    paint(stage);
  }

  function step(stage, n) {
    var st = stage._g; if (!st || n >= st.steps.length) return false;
    var s = st.steps[n];
    s.acts.forEach(function (a) { if (VERBS[a.verb]) VERBS[a.verb](stage, a); });
    followers(stage).forEach(function (e) {
      if (parseInt(e.getAttribute('data-grow-step'), 10) === n + 1) restart(e, 'g-shown');
    });
    var say = $('.g-say', stage);
    if (say) { say.textContent = s.say || ''; restart(say, 'g-said'); }
    var badge = $('.g-beat', stage);
    if (badge && s.beat) { badge.textContent = s.beat; badge.setAttribute('data-beat', s.beat); }
    return true;
  }

  function next(stage) {
    var st = stage._g; if (!st) return false;
    if (st.paused) return true;                       /* a prediction is on screen */
    if (st.i >= st.steps.length) return false;
    step(stage, st.i);
    st.i++;
    paint(stage);
    if (st.i >= st.steps.length && typeof stage._gDone === 'function') stage._gDone(stage);
    return true;
  }

  function all(stage) {
    var st = stage._g; if (!st) return;
    st.paused = false;
    $$('.g-pause', stage).forEach(function (e) { e.remove(); });
    while (st.i < st.steps.length) {
      var s = st.steps[st.i];
      s.acts.forEach(function (a) { if (a.verb !== 'pause' && a.verb !== 'think' && VERBS[a.verb]) VERBS[a.verb](stage, a); });
      followers(stage).forEach(function (e) {
        if (parseInt(e.getAttribute('data-grow-step'), 10) === st.i + 1) e.classList.add('g-shown');
      });
      st.i++;
    }
    st.paused = false;
    paint(stage);
    if (typeof stage._gDone === 'function') stage._gDone(stage);
  }

  function paint(stage) {
    var st = stage._g, bar = $('.g-bar', stage); if (!st || !bar) return;
    var dots = $('.g-dots', bar);
    if (dots) {
      if (dots.children.length !== st.steps.length) {
        dots.innerHTML = st.steps.map(function (s) {
          return '<i class="' + (s.beat ? 'g-beat-' + s.beat : '') + '"></i>';
        }).join('');
      }
      $$('i', dots).forEach(function (d, i) { d.classList.toggle('on', i < st.i); });
    }
    var nb = $('.g-next', bar);
    if (nb) {
      var done = st.i >= st.steps.length;
      nb.disabled = done || st.paused;
      nb.textContent = done ? '✓ All shown'
        : st.paused ? '⏸ Take the predictions'
        : st.i === 0 ? '▶ Start' : '▶ Next (' + (st.i + 1) + '/' + st.steps.length + ')';
      nb.classList.toggle('g-next-ready', !done && !st.paused);
    }
  }

  /* swap a stage onto a different asset / script at run time */
  function load(stage, assetName, which) {
    build(stage);
    var canvas = $('.g-canvas', stage);
    canvas.innerHTML = render(assetName);
    $$('.g-spot,.g-verdict,.g-think,.g-pause', stage).forEach(function (e) { e.remove(); });
    stage.setAttribute('data-grow-asset', assetName);
    if (global.GrowPolish) global.GrowPolish.decorate(stage);
    loadScript(stage, lib() ? lib().script(assetName, which || 'reveal') : '');
  }

  /* ======================================== Phase 4 · the We-Do framework
     Question -> Prediction -> Discussion -> Animation -> Explanation -> Check.
     Each move unlocks the next, so nothing can be skim-read ahead of the class.
       <div class="g-wedo" data-grow-asset="circuit"
            data-grow-q="Will the lamp light?"
            data-grow-options="Yes|No|Only if the switch is closed"
            data-grow-discuss="Talk to your partner. Give a reason, not a guess."
            data-grow-explain="A lamp lights only when the circuit is a complete loop."
            data-grow-check="Draw one circuit that works and one that cannot."></div>
   ========================================================================= */

  var WEDO_MOVES = ['Question', 'Predict', 'Discuss', 'Watch', 'Explain', 'Check'];

  function buildWedo(host) {
    var q       = host.getAttribute('data-grow-q') || 'What do you think will happen?';
    var opts    = (host.getAttribute('data-grow-options') || 'Yes|No').split('|').map(function (s) { return s.trim(); }).filter(Boolean);
    var discuss = host.getAttribute('data-grow-discuss') || 'Turn and talk. You must give a REASON, not just an answer.';
    var explain = host.getAttribute('data-grow-explain') || '';
    var check   = host.getAttribute('data-grow-check') || '';
    var asset   = host.getAttribute('data-grow-asset') || '';
    var script  = host.getAttribute('data-grow-script') || '@teach';
    var overs   = host.getAttribute('data-grow-overlays') || '';

    host.innerHTML =
      '<div class="g-wedo-track">' + WEDO_MOVES.map(function (m, i) {
        return '<span' + (i === 0 ? ' class="on"' : '') + '>' + m + '</span>';
      }).join('') + '</div>' +
      '<p class="g-wedo-q">' + q + '</p>' +
      '<div class="g-wedo-panel on" data-move="1">' +
        '<div class="g-vote">' + opts.map(function (o, i) {
          return '<button type="button" class="g-chip' + (i === 1 ? ' g-chip-b' : i === 2 ? ' g-chip-c' : '') +
            '" data-i="' + i + '">' + o + '<span class="g-n">0</span></button>';
        }).join('') + '</div>' +
        '<p class="g-wedo-prompt">Hands up for one. <strong>Everyone commits</strong> — a wrong prediction is worth as much as a right one.</p>' +
        '<button type="button" class="g-mini g-wedo-go">Predictions in →</button>' +
      '</div>' +
      '<div class="g-wedo-panel" data-move="2">' +
        '<p class="g-wedo-prompt">🗣️ ' + discuss + '</p>' +
        '<button type="button" class="g-mini g-wedo-go">Ready to watch →</button>' +
      '</div>' +
      '<div class="g-wedo-panel" data-move="3">' +
        '<div class="g-stage g-plain" data-grow-frame="wide"' +
          (asset ? ' data-grow-asset="' + asset + '"' : '') +
          (overs ? ' data-grow-overlays="' + overs + '"' : '') +
          ' data-grow-script="' + script.replace(/"/g, '&quot;') + '"></div>' +
      '</div>' +
      '<div class="g-wedo-panel" data-move="4">' +
        (explain ? '<p class="g-wedo-prompt">' + explain + '</p>' : '') +
        '<button type="button" class="g-mini g-wedo-go">On to the check →</button>' +
      '</div>' +
      (check ? '<div class="g-wedo-panel" data-move="5"><p class="g-wedo-prompt">✍️ ' + check + '</p></div>' : '');

    var stage = $('.g-stage', host);
    if (stage) build(stage);

    /* the vote counter — a show of hands, tallied on the board */
    $$('.g-chip', host).forEach(function (c) {
      c.addEventListener('click', function () {
        var n = $('.g-n', c);
        n.textContent = String((parseInt(n.textContent, 10) || 0) + 1);
      });
    });

    /* move 0 = question+predict; the track lights as the class moves on */
    var move = 0;
    var panels = $$('.g-wedo-panel', host);
    var pips = $$('.g-wedo-track span', host);

    function goto(m) {
      move = m;
      panels.forEach(function (p) { p.classList.toggle('on', +p.getAttribute('data-move') === m + 1); });
      pips.forEach(function (p, i) {
        p.classList.toggle('on', i === m + 1 || (m === 0 && i <= 1));
        p.classList.toggle('done', i < m + 1);
      });
      if (m === 2 && stage) { reset(stage); }
    }

    $$('.g-wedo-go', host).forEach(function (b) {
      b.addEventListener('click', function () { goto(Math.min(move + 1, panels.length - 1)); });
    });

    /* when the animation finishes, the explanation unlocks itself */
    if (stage) stage._gDone = function () { if (move === 2) goto(3); };

    host._gWedo = { goto: goto, stage: stage };
    return host._gWedo;
  }

  /* ================================= Phases 4 & 7 · standalone prediction panel
       <div class="g-predict" data-grow-items="crab:Crab, bird:Robin"
            data-grow-vote-a="● Yes" data-grow-vote-b="■ No"></div>          */

  function buildPredict(host) {
    var spec = (host.getAttribute('data-grow-items') || host.getAttribute('data-grow-animals') || '')
      .split(',').map(function (s) { return s.trim(); }).filter(Boolean)
      .map(function (s) { var p = s.split(':'); return { asset: p[0].trim(), name: (p[1] || '').trim() || titleOf(p[0].trim()) }; });

    var voteA = host.getAttribute('data-grow-vote-a') || '● Yes';
    var voteB = host.getAttribute('data-grow-vote-b') || '■ No';

    host.innerHTML =
      '<div class="g-predict-cards">' + spec.map(function (s, i) {
        return '<button type="button" class="g-pc" data-i="' + i + '">' + s.name + '</button>';
      }).join('') + '</div>' +
      '<div class="g-vote"><span class="g-chip">' + voteA + '</span>' +
      '<span class="g-chip g-chip-b">' + voteB + '</span>' +
      '<span class="g-tally">Checked <strong class="g-count">0</strong>/' + spec.length + '</span></div>' +
      '<div class="g-stage g-plain" data-grow-frame="wide"></div>';

    var stage = $('.g-stage', host);
    build(stage);
    var count = 0, seen = {};

    stage._gDone = function () {
      var i = host._gCur;
      if (i == null || seen[i]) return;
      seen[i] = true; count++;
      $('.g-count', host).textContent = count;
      var card = $('.g-pc[data-i="' + i + '"]', host);
      if (card) card.classList.add('g-done');
    };

    $$('.g-pc', host).forEach(function (card) {
      card.addEventListener('click', function () {
        var i = +card.getAttribute('data-i');
        host._gCur = i;
        $$('.g-pc', host).forEach(function (c) { c.classList.remove('g-current'); });
        card.classList.add('g-current');
        load(stage, spec[i].asset, 'reveal');
        VERBS.think(stage, {});
        var say = $('.g-say', stage);
        if (say) { say.textContent = spec[i].name + ' — everybody decide. Then I press Next.'; restart(say, 'g-said'); }
      });
    });

    var nb = $('.g-next', stage);
    if (nb) nb.addEventListener('click', function () { VERBS.unthink(stage); }, true);

    host._gStage = stage;
    return stage;
  }

  /* ================================================ Phase 9 · retrieval
       <div class="g-retrieve" data-grow-asset="foodchain"
            data-grow-script="@retrieve"
            data-grow-stop="2"
            data-grow-cue="Say the next organism in the chain."></div>

     The picture starts to build, stops at the declared step and waits for the
     class to say what comes next. Recall, out loud, before the reveal.      */

  function buildRetrieve(host) {
    var stop = parseInt(host.getAttribute('data-grow-stop') || '2', 10);
    var cue  = host.getAttribute('data-grow-cue') || 'What comes next? Say it before I click.';
    var asset = host.getAttribute('data-grow-asset') || '';
    var script = host.getAttribute('data-grow-script') || '@retrieve';

    host.innerHTML =
      '<div class="g-retrieve-score">🎯 Recalled <span class="g-n">0</span>' +
      '<span style="font-weight:600;opacity:.8">— say it out loud before every reveal</span></div>' +
      '<div class="g-stage g-plain" data-grow-frame="wide"' +
        (asset ? ' data-grow-asset="' + asset + '"' : '') +
        ' data-grow-script="' + script.replace(/"/g, '&quot;') + '"></div>';

    var stage = $('.g-stage', host);
    build(stage);

    /* after the declared step, every further press asks first and shows second */
    var armed = false, scored = 0;
    var nb = $('.g-next', stage);
    if (!nb) return stage;

    nb.addEventListener('click', function (ev) {
      var st = stage._g;
      if (!st || st.paused) return;
      if (st.i >= stop && st.i < st.steps.length && !armed) {
        ev.stopImmediatePropagation();
        ev.preventDefault();
        armed = true;
        VERBS.pause(stage, { text: cue, targets: [] });
        var el = $('.g-pause', stage);
        if (el) {
          $('button', el).addEventListener('click', function () {
            armed = false;
            scored++;
            $('.g-n', host).textContent = String(scored);
          });
        }
      }
    }, true);

    host._gStage = stage;
    return stage;
  }

  /* ============================================ Phase 10 · misconception engine
       <div class="g-misc" data-grow-asset="wallpush"
            data-grow-claim="Pushing a wall — there are no forces, nothing moves."
            data-grow-wrong="@wrong" data-grow-right="@right"></div>

     The wrong idea is animated FIRST, honestly and without sneering, because a
     pupil who has never seen their own idea taken seriously does not give it
     up. Then the same scene is corrected in front of them.                  */

  function buildMisc(host) {
    var claim = host.getAttribute('data-grow-claim') || 'What most people think…';
    var asset = host.getAttribute('data-grow-asset') || '';
    var wrong = host.getAttribute('data-grow-wrong') || '@wrong';
    var right = host.getAttribute('data-grow-right') || '@right';

    host.innerHTML =
      '<p class="g-misc-claim">' + claim + '</p>' +
      '<div class="g-stage g-plain" data-grow-frame="wide"' +
        (asset ? ' data-grow-asset="' + asset + '"' : '') +
        ' data-grow-script="' + wrong.replace(/"/g, '&quot;') + '"></div>' +
      '<button type="button" class="g-mini g-misc-fix" style="margin-top:6px">🔎 Now look again — what is REALLY happening</button>';

    var stage = $('.g-stage', host);
    build(stage);

    $('.g-misc-fix', host).addEventListener('click', function () {
      host.classList.add('g-corrected');
      var c = $('.g-misc-claim', host);
      if (c && c.innerHTML.indexOf('<s>') < 0) c.innerHTML = '<s>' + c.innerHTML + '</s>';
      this.remove();
      loadScript(stage, right.charAt(0) === '@' && asset && lib() ? lib().script(asset, right.slice(1)) : right);
      next(stage);
    });

    host._gStage = stage;
    return stage;
  }

  /* ============================================ Phase 11 · the story spine
       <div class="g-story" data-grow-story="Why do we slip on ice?|Test three
            surfaces|Rough grips, smooth slides|Friction between surfaces|
            Choosing the right sole"></div>

     Sits at the top of the lesson and lights up as the lesson moves, so pupils
     always know which part of the story they are in.                        */

  var STORY_BEATS = ['Question', 'Investigation', 'Discovery', 'Explanation', 'Application'];

  function buildStory(host) {
    var parts_ = (host.getAttribute('data-grow-story') || '').split('|').map(function (s) { return s.trim(); });
    host.innerHTML = STORY_BEATS.map(function (b, i) {
      return '<div class="g-story-beat" data-i="' + i + '"><b>' + b + '</b><span>' + (parts_[i] || '') + '</span></div>';
    }).join('');
    host.setStoryBeat = function (n) {
      $$('.g-story-beat', host).forEach(function (e, i) {
        e.classList.toggle('on', i === n);
        e.classList.toggle('done', i < n);
      });
    };
    var start = parseInt(host.getAttribute('data-grow-at') || '0', 10);
    host.setStoryBeat(start);
    return host;
  }

  /* Slides may declare which beat of the story they belong to with
     data-grow-beat="2"; the spine follows the deck automatically. */
  function syncStory(root) {
    var slide = $('.slide.active') || root;
    if (!slide || !slide.getAttribute) return;
    var b = slide.getAttribute('data-grow-beat');
    if (b == null) return;
    $$('.g-story').forEach(function (s) { if (s.setStoryBeat) s.setStoryBeat(parseInt(b, 10)); });
  }

  /* ============================================================ motion key */

  var KEY = [
    ['✏️', 'Draw',   'Structure forming'],
    ['✨', 'Glow',   'Important feature'],
    ['💓', 'Pulse',  'Pay attention'],
    ['🌫️', 'Fade',   'Less important'],
    ['🔄', 'Morph',  'Change'],
    ['➡️', 'Flow',   'Movement'],
    ['↔️', 'Shake',  'Incorrect idea'],
    ['⬆️', 'Bounce', 'Correct answer'],
    ['〰️', 'Trace',  'Follow a pathway'],
    ['🔍', 'Zoom',   'Look closer']
  ];

  function buildKey(host) {
    host.innerHTML = KEY.map(function (k) {
      return '<div><b>' + k[0] + '</b>' + k[1] + '<i>' + k[2] + '</i></div>';
    }).join('');
  }

  /* ==================================================== navigation plumbing */

  function activeRoot() { return $('.slide.active') || doc.body; }

  /* One press of the deck's own Next key first advances any unfinished stage
     on the slide. The teacher never has to think about which Next they mean.

     At a prediction pause the deck's Next becomes the reveal — press once to
     stop and ask, press again to show the answer. It must never simply do
     nothing: a teacher whose Next button has apparently died in front of a
     class will not use the feature twice. */
  function advanceActive() {
    var root = activeRoot();
    var stages = $$('.g-stage', root).filter(function (s) {
      return s._g && s._g.steps.length && (s._g.paused || s._g.i < s._g.steps.length) &&
             s.offsetParent !== null;
    });
    if (!stages.length) return false;
    if (stages[0]._g.paused) {
      var reveal = $('.g-pause button', stages[0]);
      if (reveal) { reveal.click(); return true; }
      stages[0]._g.paused = false;             /* pause with no overlay left — unstick */
    }
    return next(stages[0]);
  }

  function hookNav() {
    if (typeof global.nextSlide === 'function' && !global.nextSlide._gWrapped) {
      var orig = global.nextSlide;
      var wrapped = function () { if (advanceActive()) return; orig.apply(this, arguments); };
      wrapped._gWrapped = true;
      global.nextSlide = wrapped;
    }
    if (typeof global.showSlide === 'function' && !global.showSlide._gWrapped) {
      var os = global.showSlide;
      var ws = function () {
        os.apply(this, arguments);
        setTimeout(function () {
          $$('.g-stage', activeRoot()).forEach(function (s) { if (s._g) reset(s); });
          syncStory(activeRoot());
        }, 20);
      };
      ws._gWrapped = true;
      global.showSlide = ws;
    }
  }

  /* ============================================================= named API */

  function stageOf(x) {
    if (!x) return $('.g-stage');
    if (typeof x === 'string') return $(x);
    return x.classList && x.classList.contains('g-stage') ? x : (x.closest ? x.closest('.g-stage') : x);
  }
  function run(x, verb, targets, text) {
    var s = stageOf(x);
    if (s && VERBS[verb]) VERBS[verb](s, { targets: [].concat(targets || []), text: text || null });
  }

  function drawStructure(x, p)  { run(x, 'draw', p || '*'); }
  function highlightPart(x, p)  { run(x, 'glow', p); run(x, 'hi', p); }
  function tracePathway(x, p)   { run(x, 'trace', p); }
  function revealLabels(x)      { labels(stageOf(x), ['*']).forEach(function (e) { restart(e, 'g-labelled'); }); }
  function pulseCorrect(el)     { if (el) { restart(el, 'g-bounce'); ding(); setTimeout(function () { el.classList.remove('g-bounce'); }, 700); } }
  function shakeWrong(el)       { if (el) { restart(el, 'g-shake'); buzz(); setTimeout(function () { el.classList.remove('g-shake'); }, 520); } }
  function zoomFeature(x, p)    { run(x, 'zoom', p); }
  function fadeOthers(x, keep)  { run(x, 'only', [].concat(keep || [])); }
  function showInvisible(x, l)  { run(x, 'overlay', [].concat(l || [])); }
  function morphInto(x, a, b)   { run(x, 'morph', [a + '>' + b]); }
  function setHeat(x, p, v)     { run(x, 'heat', [].concat(p || '*'), String(v)); }

  /* ================================================================== init */

  function init(root) {
    root = root || doc;
    $$('.g-story[data-grow-story]', root).forEach(function (h) { if (!h._gBuilt) { h._gBuilt = true; buildStory(h); } });
    $$('.g-key', root).forEach(function (h) { if (!h._gBuilt) { h._gBuilt = true; buildKey(h); } });
    $$('.g-wedo', root).forEach(function (h) { if (!h._gBuilt) { h._gBuilt = true; buildWedo(h); } });
    $$('.g-retrieve', root).forEach(function (h) { if (!h._gBuilt) { h._gBuilt = true; buildRetrieve(h); } });
    $$('.g-misc', root).forEach(function (h) { if (!h._gBuilt) { h._gBuilt = true; buildMisc(h); } });
    $$('.g-predict', root).forEach(function (h) { if (!h._gBuilt) { h._gBuilt = true; buildPredict(h); } });
    $$('.g-stage', root).forEach(function (s) { if (!s._g) build(s); });
    hookNav();
    syncStory(root);
  }

  GA.init = init;
  GA.build = build;
  GA.load = load;
  GA.next = function (x) { return next(stageOf(x)); };
  GA.reset = function (x) { return reset(stageOf(x)); };
  GA.all = function (x) { return all(stageOf(x)); };
  GA.run = run;
  GA.script = function (x, src) { loadScript(stageOf(x), src); };
  GA.advanceActive = advanceActive;
  GA.hookNav = hookNav;
  GA.parse = parseScript;
  GA.verbs = VERBS;
  GA.beats = BEATS;
  GA.key = KEY;

  global.GrowAnim = GA;
  global.drawStructure = drawStructure;
  global.highlightPart = highlightPart;
  global.tracePathway = tracePathway;
  global.revealLabels = revealLabels;
  global.pulseCorrect = pulseCorrect;
  global.shakeWrong = shakeWrong;
  global.zoomFeature = zoomFeature;
  global.fadeOthers = fadeOthers;
  global.showInvisible = showInvisible;
  global.morphInto = morphInto;
  global.setHeat = setHeat;

  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', function () { init(); });
  else setTimeout(function () { init(); }, 0);

})(typeof window !== 'undefined' ? window : this, document);
