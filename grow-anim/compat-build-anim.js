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

  global.BioSVG = global.BioSVG || {
    render:  function (name) { return GS.render(name); },
    script:  function (name, which) { return GS.script(name, which); },
    asset:   function (name) { return GS.asset(name); },
    title:   function (name) { return GS.title(name); },
    kind:    function (name) { var a = GS.asset(name); return a && a.kind; },
    list:    function () { return GS.list('animals'); },
    register: function (assets) { GS.register(assets); return Object.keys(assets); },
    helpers: GS,
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
