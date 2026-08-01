/* ============================================================================
   GROW ANIMATION FRAMEWORK · compatibility layer for build-anim
   ---------------------------------------------------------------------------
   BUILD and GROW were two codebases doing the same job. This closes that: the
   GROW engine is now the only engine, and this file makes every piece of
   existing BUILD lesson markup run against it unchanged.

   Load it INSTEAD of build-anim/build-anim.js and build-anim/bio-svg.js:

     <script src="/grow-anim/grow-svg.js"></script>
     <script src="/grow-anim/grow-svg-bio-animals.js"></script>   <- the 13 animals
     <script src="/grow-anim/grow-anim.js"></script>
     <script src="/grow-anim/compat-build-anim.js"></script>      <- this file

   What it provides
     window.BuildAnim          the old API, delegating to GrowAnim
     window.BioSVG             the old API, delegating to GrowSVG
     .ba-stage / .ba-predict   translated to .g-stage / .g-predict on load
     data-ba-*                 translated to data-grow-*
     dim / undim               kept as aliases of GROW's fade / unfade

   Nothing in a BUILD lesson has to change. When every BUILD lesson has been
   re-injected against grow-anim, build-anim/build-anim.js, build-anim.css and
   bio-svg.js can be deleted and this file retired with them.

   Ported across from build-anim so the BUILD science lessons survive that
   deletion (each verified in a browser, see build-anim/README.md):
     pose                      the whole of Week 4 is one `pose bend`
     per-card predict scripts  "asset:Label:script", | separated
     BioSVG.helpers            the build-anim spellings, which differ from
                               GrowSVG's — shape(d, fillOpacity) not (d, sw)
     the pop wrapper           in grow-anim.js, so a child's own transform
                               attribute is not overridden by the animation

   The translation runs BEFORE GrowAnim's own initialiser gets to the DOM, so a
   converted stage is built exactly once, by the same code path as a native one.
   ========================================================================== */
(function (global, doc) {
  'use strict';

  if (!global.GrowAnim || !global.GrowSVG) { return; }
  var GA = global.GrowAnim, GS = global.GrowSVG;

  function $$(sel, root) { return Array.prototype.slice.call((root || doc).querySelectorAll(sel)); }

  /* ------------------------------------------------------- verb aliases
     BUILD called the "this matters less right now" motion `dim`. GROW calls it
     `fade`. Same motion, same meaning — so the old word keeps working rather
     than silently doing nothing in a lesson nobody has re-read. */
  if (GA.verbs && !GA.verbs.dim) {
    GA.verbs.dim = GA.verbs.fade;
    GA.verbs.undim = GA.verbs.unfade;
  }

  /* --------------------------------------------------- markup translation */

  var ATTRS = [
    ['data-ba-asset',   'data-grow-asset'],
    ['data-ba-script',  'data-grow-script'],
    ['data-ba-rail',    'data-grow-rail'],
    ['data-ba-static',  'data-grow-static'],
    ['data-ba-title',   'data-grow-title'],
    ['data-ba-nobar',   'data-grow-nobar'],
    ['data-ba-frame',   'data-grow-frame'],
    ['data-ba-step',    'data-grow-step'],
    ['data-ba-for',     'data-grow-for'],
    ['data-ba-animals', 'data-grow-items'],
    ['data-ba-cards',   'data-grow-items'],
    ['data-ba-pose',    'data-grow-pose'],
    ['data-ba-vote-a',  'data-grow-vote-a'],
    ['data-ba-vote-b',  'data-grow-vote-b']
  ];

  var CLASSES = [
    ['ba-stage',   'g-stage'],
    ['ba-predict', 'g-predict'],
    ['ba-plain',   'g-plain'],
    ['ba-key',     'g-key']
  ];

  function translate(el) {
    ATTRS.forEach(function (pair) {
      if (!el.hasAttribute(pair[0])) return;
      if (!el.hasAttribute(pair[1])) el.setAttribute(pair[1], el.getAttribute(pair[0]));
    });
    CLASSES.forEach(function (pair) {
      if (el.classList.contains(pair[0])) el.classList.add(pair[1]);
    });
  }

  function convert(root) {
    var sel = CLASSES.map(function (p) { return '.' + p[0]; })
      .concat(ATTRS.map(function (p) { return '[' + p[0] + ']'; })).join(',');
    $$(sel, root || doc).forEach(translate);
  }

  /* ------------------------------------------------------------ old APIs */

  /* ------------------------------------------------- the BUILD helper kit
     GrowSVG exports its own builder kit, but under different names and with
     different argument meanings — GrowSVG's shape(d, strokeWidth) against
     build-anim's shape(d, fillOpacity), for one. The BUILD subject libraries
     (body-svg, food-svg, chain-svg) are written against the build-anim
     spellings, so those are provided here verbatim rather than aliased to
     something that would render subtly wrong. */
  var BONE = '#4E7A9B', SHELL = '#C9803B', SOFT = '#94a3b8', INK = '#1f2937';
  function bn(v) { return (Math.round(v * 10) / 10).toString(); }
  var HELPERS = {
    BONE: BONE, SHELL: SHELL, SOFT: SOFT, INK: INK,
    n: bn,
    g: function (part, colour, inner) {
      return '<g data-part="' + part + '" style="color:' + colour + '">' + inner + '</g>';
    },
    shape: function (d, opacity) {
      return '<path d="' + d + '" fill="currentColor" fill-opacity="' +
        (opacity == null ? 0.28 : opacity) + '" stroke="currentColor" stroke-width="2.6"' +
        ' stroke-linejoin="round" pathLength="1"/>';
    },
    stroke: function (d, w) {
      return '<path d="' + d + '" fill="none" stroke="currentColor" stroke-width="' + (w || 3) +
        '" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/>';
    },
    label: function (key, x, y, text, colour, ax, ay) {
      var w = Math.max(96, text.length * 10.6 + 26), leader = '';
      if (ax != null) {
        var lx = (ax < x) ? x : x + w;
        leader = '<path d="M ' + bn(ax) + ' ' + bn(ay) + ' L ' + bn(lx) + ' ' + bn(y + 15) +
          '" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="5 5"/>' +
          '<circle cx="' + bn(ax) + '" cy="' + bn(ay) + '" r="4.5" fill="currentColor"/>';
      }
      return '<g class="ba-label" data-label="' + key + '" style="color:' + colour + '">' + leader +
        '<rect x="' + bn(x) + '" y="' + bn(y) + '" width="' + bn(w) + '" height="30" rx="9" fill="#ffffff"' +
        ' stroke="currentColor" stroke-width="2.4"/>' +
        '<text x="' + bn(x + w / 2) + '" y="' + bn(y + 20.5) + '" text-anchor="middle" font-size="15.5"' +
        ' font-weight="800" fill="currentColor" font-family="system-ui,sans-serif">' + text + '</text></g>';
    }
  };

  global.BioSVG = global.BioSVG || {
    render:  function (name) { return GS.render(name); },
    script:  function (name, which) { return GS.script(name, which); },
    asset:   function (name) { return GS.asset(name); },
    title:   function (name) { return GS.title(name); },
    kind:    function (name) { var a = GS.asset(name); return a && a.kind; },
    list:    function () { return GS.list('animals'); },
    register: function (assets) { GS.register(assets); return Object.keys(assets); },
    helpers: HELPERS,
    vertebrates:   function () { return GS.list('vertebrates'); },
    invertebrates: function () { return GS.list('invertebrates'); }
  };

  global.BuildAnim = global.BuildAnim || {
    init: function (root) { convert(root); return GA.init(root); },
    build: GA.build,
    load: GA.load,
    next: GA.next,
    reset: GA.reset,
    all: GA.all,
    run: GA.run,
    advanceActive: GA.advanceActive,
    hookNav: GA.hookNav,
    parse: GA.parse,
    verbs: GA.verbs
  };

  /* The named helpers BUILD lessons call inline. GROW exports the same
     behaviours under clearer names; these keep the old spellings alive. */
  var ALIAS = {
    drawSkeleton: function (x) { GA.run(x, 'draw', ['skull', 'ribs', 'pelvis', 'limbs']); GA.run(x, 'pop', ['spine']); },
    highlightBone: function (x, part) { global.highlightPart(x, part || 'spine'); },
    traceBackbone: function (x) { global.tracePathway(x, 'spine'); }
  };
  Object.keys(ALIAS).forEach(function (k) { if (!global[k]) global[k] = ALIAS[k]; });
  /* revealLabels, pulseCorrect, shakeWrong, zoomFeature and fadeOthers are
     already exported by grow-anim.js under exactly these names. */

  /* ---------------------------------------------------------------- init
     Convert first, then let GROW's initialiser find the results. It is safe to
     call init twice: every builder in the engine guards on its own flag. */
  function boot() { convert(doc); GA.init(doc); }
  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', boot);
  else boot();

  global.BuildAnimCompat = { convert: convert, translate: translate };

})(typeof window !== 'undefined' ? window : this, document);
