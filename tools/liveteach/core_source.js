/* Live-Teach core — bus contract, keyboard registry, motion + theme state.
   ONE SOURCE, MANY COPIES: this file is stamped byte-identically into every
   liveteach view by tools/liveteach/stamp_core.mjs (between the
   MBM-LIVETEACH-CORE markers). Edit HERE, run the stamper, never edit a
   stamped copy — tools/liveteach/static_gates.mjs reds on drift. The views
   stay single self-contained files (the estate's offline-first promise); the
   pinned-region pattern is the same one the inline exit region uses. */
(function () {
  'use strict';
  var LT = window.LT = window.LT || {};
  LT.CHANNEL = 'mbm_liveteach_v1';
  LT.VERSION = 1;

  /* --- message bus -------------------------------------------------------
     Contract (order LT-GO / governing spec): every message is
     { v: 1, type, payload }. Unknown type or missing v is ignored silently.
     Listeners use addEventListener ONLY — assigning bus.onmessage anywhere in
     liveteach is a static-gate failure: two of the reviewed fragments each
     overwrote onmessage and silently killed the other's handlers. */
  var bus = null;
  LT.bus = function () {
    if (!bus) bus = new BroadcastChannel(LT.CHANNEL);
    return bus;
  };
  LT.send = function (type, payload) {
    try { LT.bus().postMessage({ v: 1, type: type, payload: payload || {} }); } catch (e) {}
  };
  LT.on = function (handler) {
    LT.bus().addEventListener('message', function (ev) {
      var m = ev.data;
      if (!m || m.v !== 1 || typeof m.type !== 'string') return;
      handler(m.type, m.payload || {});
    });
  };

  /* --- keyboard registry -------------------------------------------------
     One keydown listener per view, total. Registering a code twice throws at
     boot — the guard against the KeyB-class double-fire collision. Hotkeys
     are skipped while focus is in INPUT / TEXTAREA / SELECT / contenteditable
     (the fragments missed the last two). */
  var keys = new Map();
  LT.registerKey = function (code, handler, description) {
    if (keys.has(code)) throw new Error('Live-Teach key registered twice: ' + code);
    keys.set(code, { handler: handler, description: description || '' });
  };
  LT.keymap = function () {
    var out = [];
    keys.forEach(function (v, k) { out.push([k, v.description]); });
    return out;
  };
  document.addEventListener('keydown', function (e) {
    var t = e.target;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.tagName === 'SELECT' || t.isContentEditable)) return;
    var entry = keys.get(e.code);
    if (entry) entry.handler(e);
  });

  /* --- reduced motion ----------------------------------------------------
     Both halves of the house rule: each view carries a CSS
     @media (prefers-reduced-motion: reduce) blanket, and this JS half mirrors
     the query onto body.reduce with a LIVE change subscription (a boot-only
     read was a recorded estate defect). Calm is the pupil-facing stillness
     choice, independent of the OS setting; either source reduces. */
  var mq = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
  var calmChoice = false;
  LT.onMotion = [];
  function applyMotion() {
    var reduce = calmChoice || !!(mq && mq.matches);
    document.body.classList.toggle('reduce', reduce);
    for (var i = 0; i < LT.onMotion.length; i++) {
      try { LT.onMotion[i](reduce); } catch (e) {}
    }
  }
  LT.reduced = function () { return document.body.classList.contains('reduce'); };
  LT.calm = function () { return calmChoice; };
  LT.setCalm = function (on) { calmChoice = !!on; applyMotion(); saveSettings(); };
  if (mq) {
    if (mq.addEventListener) mq.addEventListener('change', applyMotion);
    else if (mq.addListener) mq.addListener(applyMotion);
  }

  /* --- settings ----------------------------------------------------------
     One key, JSON, display preferences only. Pupil data NEVER enters storage
     from liveteach (order LT-GO D2: rosters live in memory for the lesson and
     die with the tab). Registered in REGISTER.md §B via R-LT2xx. */
  var SKEY = 'mbm_liveteach_v1_settings';
  function loadSettings() {
    try { return JSON.parse(localStorage.getItem(SKEY)) || {}; } catch (e) { return {}; }
  }
  function saveSettings() {
    try { localStorage.setItem(SKEY, JSON.stringify({ highlumen: LT.highlumen(), calm: calmChoice })); } catch (e) {}
  }
  LT.saveSettings = saveSettings;

  /* --- high-lumen (correction S5) ---------------------------------------
     A washed-out classroom projector loses dark themes; highlumen swaps to a
     light palette. Flags BOTH html and body — the page fill lives on <html>
     (the estate's recorded CSS gotcha). Vocabulary follows the hub's
     "High lumen — projector / IWB" mode. */
  LT.highlumen = function () { return document.body.classList.contains('highlumen'); };
  LT.setHighlumen = function (on) {
    document.body.classList.toggle('highlumen', !!on);
    document.documentElement.classList.toggle('highlumen', !!on);
    saveSettings();
  };

  LT.boot = function () {
    var s = loadSettings();
    if (s.highlumen) {
      document.body.classList.add('highlumen');
      document.documentElement.classList.add('highlumen');
    }
    if (s.calm) calmChoice = true;
    applyMotion();
  };
})();
