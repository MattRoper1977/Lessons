/* ============================================================================
   GROW ANIMATION FRAMEWORK · Phase 12 — PREMIUM POLISH (behaviour)
   ---------------------------------------------------------------------------
   Optional. Load AFTER grow-anim.js. If it is absent, nothing breaks — the
   engine checks for it before calling.

   Everything here is in service of attention, not decoration:
     · a particle field so a stage has air in it rather than sitting on a slab
     · parallax so depth reads as depth on a projector at the back of the room
     · a ripple on tap so a pupil at the board knows their touch registered
     · a motion-blur filter for the small number of things genuinely moving fast

   Declared on the stage, never hard-coded:
     <div class="g-stage g-lit g-depth" data-g-particles="dust:14"></div>
   ========================================================================== */
(function (global, doc) {
  'use strict';

  var GP = {};
  var reduced = false;
  try {
    reduced = global.matchMedia && global.matchMedia('(prefers-reduced-motion: reduce)').matches;
  } catch (e) {}

  function $(s, r) { return (r || doc).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || doc).querySelectorAll(s)); }

  /* Deterministic pseudo-random. Particle fields must look identical on every
     reload, or a teacher who re-runs a slide sees a different picture and
     wonders what they changed. */
  function rnd(seed) {
    var s = seed;
    return function () { s = (s * 1103515245 + 12345) & 0x7fffffff; return s / 0x7fffffff; };
  }

  /* ---------------------------------------------------------- particles */
  function particleField(stage) {
    var spec = stage.getAttribute('data-g-particles');
    if (!spec || reduced || $('.g-particles', stage)) return;
    var p = spec.split(':');
    var kind = (p[0] || 'dust').trim();
    var count = Math.min(40, parseInt(p[1], 10) || 12);
    var r = rnd(kind.length * 7717 + count * 131);

    var host = doc.createElement('div');
    host.className = 'g-particles g-p-' + kind;
    host.setAttribute('aria-hidden', 'true');
    var html = '', i, size, dur;
    for (i = 0; i < count; i++) {
      size = 3 + r() * 6;
      dur = 9 + r() * 12;
      html += '<i style="left:' + (r() * 100).toFixed(1) + '%;top:' + (60 + r() * 50).toFixed(1) + '%;' +
        'width:' + size.toFixed(1) + 'px;height:' + size.toFixed(1) + 'px;' +
        '--gx:' + (r() * 60 - 30).toFixed(0) + 'px;--gy:' + (-90 - r() * 120).toFixed(0) + 'px;' +
        'animation-duration:' + dur.toFixed(1) + 's;animation-delay:-' + (r() * dur).toFixed(1) + 's"></i>';
    }
    host.innerHTML = html;
    stage.insertBefore(host, stage.firstChild);
  }

  /* ----------------------------------------------------------- parallax
     Depth layers lag behind the pointer. Small numbers only — on a projector,
     anything more than a few pixels reads as the picture being broken. */
  function parallax(stage) {
    if (!stage.classList.contains('g-parallax') || reduced || stage._gPar) return;
    stage._gPar = true;
    var max = 9;
    function move(ev) {
      var r = stage.getBoundingClientRect();
      var cx = ev.clientX == null ? r.width / 2 : ev.clientX - r.left;
      var cy = ev.clientY == null ? r.height / 2 : ev.clientY - r.top;
      var dx = (cx / r.width - 0.5) * 2, dy = (cy / r.height - 0.5) * 2;
      $$('[data-depth]', stage).forEach(function (el) {
        var k = parseFloat(getComputedStyle(el).getPropertyValue('--g-par')) || 0.5;
        el.style.transform = 'translate(' + (-dx * max * k).toFixed(1) + 'px,' + (-dy * max * k).toFixed(1) + 'px)';
      });
    }
    stage.addEventListener('pointermove', move);
    stage.addEventListener('pointerleave', function () {
      $$('[data-depth]', stage).forEach(function (el) { el.style.transform = ''; });
    });
  }

  /* ------------------------------------------------------------- ripple */
  function ripple(ev) {
    if (reduced) return;
    var el = ev.currentTarget;
    var r = el.getBoundingClientRect();
    var d = Math.max(r.width, r.height) * 0.6;
    var s = doc.createElement('span');
    s.className = 'g-ripple';
    s.style.width = s.style.height = d + 'px';
    s.style.left = (ev.clientX - r.left - d / 2) + 'px';
    s.style.top = (ev.clientY - r.top - d / 2) + 'px';
    if (getComputedStyle(el).position === 'static') el.style.position = 'relative';
    el.appendChild(s);
    setTimeout(function () { s.remove(); }, 600);
  }

  function wireRipples(root) {
    $$('.g-bar button, .g-pc, .g-xray button, .g-vote .g-chip, .g-micro', root)
      .forEach(function (b) {
        if (b._gRip) return;
        b._gRip = true;
        b.style.overflow = 'hidden';
        b.addEventListener('pointerdown', ripple);
      });
  }

  /* --------------------------------------------------------- motion blur
     One SVG filter for the whole document, referenced by .g-blur-fast. */
  function ensureBlurFilter() {
    if ($('#g-mblur') || reduced) return;
    var svg = doc.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', '0'); svg.setAttribute('height', '0');
    svg.setAttribute('aria-hidden', 'true');
    svg.style.position = 'absolute';
    svg.innerHTML = '<filter id="g-mblur" x="-20%" y="-20%" width="140%" height="140%">' +
      '<feGaussianBlur stdDeviation="2.4 0" /></filter>';
    doc.body.appendChild(svg);
  }

  /* ------------------------------------------------------------- public */

  GP.decorate = function (stage) {
    if (!stage) return;
    particleField(stage);
    parallax(stage);
    wireRipples(stage);
  };

  GP.init = function (root) {
    root = root || doc;
    ensureBlurFilter();
    $$('.g-stage', root).forEach(GP.decorate);
    wireRipples(root);
  };

  global.GrowPolish = GP;

  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', function () { GP.init(); });
  else setTimeout(function () { GP.init(); }, 0);

})(typeof window !== 'undefined' ? window : this, document);
