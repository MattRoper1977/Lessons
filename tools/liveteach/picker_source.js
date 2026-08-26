/* Live-Teach cold-call picker engine — the rules only, no DOM, no storage.
   ONE SOURCE, MANY COPIES: stamped into the views by stamp_picker.mjs (the
   pinned-region pattern) and require()d by tools/liveteach/picker_gate.mjs,
   so the 10,000-draw simulation exercises the exact bytes that ship.

   THE ROSTER NEVER LEAVES MEMORY (order LT-GO D2). Nothing in this file
   touches localStorage, the bus, the URL or the console; names live in a
   plain array for the length of one lesson and die with the tab. The view
   code renders them with textContent only.

   P2 — THE NO-IMMEDIATE-REPEAT GUARANTEE, AND WHY IT IS ABSOLUTE.
   The reviewed fragment gave every pupil a minimum weight, so the pupil who
   had just answered could come straight back up — about a 1% chance per
   draw. In a mainstream room that reads as keeping people on their toes. In
   an SEMH alternative provision it does not: being asked twice in a row
   reads as being singled out, and the escalation that follows costs the rest
   of the lesson. So the guard here is structural rather than statistical.
   Weight is "draws since you were last called", which is exactly 0 for the
   pupil who just answered — they cannot be drawn at all on the next draw,
   not merely rarely. One draw later their weight is 1 and they are back in
   the pool, and it keeps climbing while they are not called, so the same
   counter that guarantees the gap also does the decay-recovery that keeps
   the room balanced. There is no floor to tune and no dice roll to lose. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.LTPick = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var MAX_NAMES = 40;      // a class, not a database
  var MAX_LEN = 32;        // one name, not a paragraph
  var HISTORY_CAP = 60;

  /* Roster text → names. Splits on newlines OR commas so a paste from a
     register works either way; trims, drops blanks, de-duplicates
     case-insensitively (two "Sam"s would be indistinguishable on screen,
     which is its own safeguarding problem — the view tells the teacher to
     add an initial). */
  function parseRoster(text) {
    var seen = Object.create(null);
    var out = [];
    String(text == null ? '' : text).split(/[\n,]/).forEach(function (raw) {
      var n = String(raw).replace(/\s+/g, ' ').trim().slice(0, MAX_LEN);
      if (!n) return;
      var key = n.toLowerCase();
      if (seen[key]) return;
      seen[key] = 1;
      if (out.length < MAX_NAMES) out.push(n);
    });
    return out;
  }

  /* since: draws since this pupil was last called. Everyone starts equal, so
     the first draw is uniform over the room. */
  function create(names) {
    var list = Array.isArray(names) ? names : parseRoster(names);
    return {
      names: list.slice(),
      present: list.map(function () { return true; }),
      since: list.map(function () { return 1; }),
      justPassed: -1,     // excluded for exactly one draw (see pass())
      last: -1,
      lastPriorSince: 0,
      history: []         // {name, passed} — MEMORY ONLY, never broadcast (P5)
    };
  }

  function setPresent(st, i, on) {
    if (i < 0 || i >= st.names.length) return;
    st.present[i] = !!on;
    /* An absent pupil holding the cooldown slot would keep punishing the
       room after they have gone; releasing it costs nothing. */
    if (!st.present[i] && st.last === i) st.last = -1;
  }

  function weights(st) {
    return st.names.map(function (_, i) {
      if (!st.present[i]) return 0;        // P4: absent pupils are not in the draw
      if (i === st.justPassed) return 0;   // a pass does not put you straight back up
      return st.since[i];                  // P2: exactly 0 for the pupil just called
    });
  }

  /* P3/P4 support: the numbers the view renders. Absent pupils are reported
     with p = 0 so the view can show them greyed and stated as absent rather
     than silently dropping them (a pupil who cannot see themselves listed
     assumes they were forgotten). */
  function probabilities(st) {
    var w = weights(st);
    var total = w.reduce(function (a, b) { return a + b; }, 0);
    var fallback = total <= 0;
    return st.names.map(function (name, i) {
      var eligible = st.present[i] && (!fallback ? w[i] > 0 : true);
      var p;
      if (!st.present[i]) p = 0;
      else if (fallback) p = 1 / Math.max(1, st.present.filter(Boolean).length);
      else p = w[i] / total;
      return {
        name: name,
        present: !!st.present[i],
        cooldown: st.present[i] && w[i] === 0,
        eligible: eligible,
        p: p
      };
    });
  }

  /* rng is injectable so the harness can drive a deterministic sequence;
     the views pass nothing and get Math.random. */
  function pick(st, rng) {
    var r = typeof rng === 'function' ? rng : Math.random;
    var w = weights(st);
    var total = w.reduce(function (a, b) { return a + b; }, 0);
    var fellBack = false;
    if (total <= 0) {
      /* Everyone present is on cooldown — one pupil present, or two with the
         other just called. The guarantee cannot hold with nobody left to
         call, so it degrades openly: the view says the room is too small for
         the no-repeat guard rather than pretending it applied. */
      var present = [];
      for (var j = 0; j < st.names.length; j++) if (st.present[j]) present.push(j);
      if (!present.length) return null;
      fellBack = true;
      w = st.names.map(function (_, i) { return st.present[i] ? 1 : 0; });
      total = present.length;
    }
    var t = r() * total, idx = -1;
    for (var i = 0; i < w.length; i++) {
      t -= w[i];
      if (t < 0) { idx = i; break; }
    }
    if (idx === -1) for (var k = w.length - 1; k >= 0; k--) { if (w[k] > 0) { idx = k; break; } }
    if (idx === -1) return null;

    for (var m = 0; m < st.since.length; m++) if (st.present[m]) st.since[m]++;
    st.lastPriorSince = st.since[idx];
    st.since[idx] = 0;
    st.last = idx;
    st.justPassed = -1;
    st.history.unshift({ name: st.names[idx], passed: false });
    if (st.history.length > HISTORY_CAP) st.history.pop();
    return { index: idx, name: st.names[idx], fellBack: fellBack };
  }

  /* M — pass / bounce. The question moves on, but passing is a scaffold, not
     an exit: the pupil's place in the queue is handed back (their since is
     restored to what it was before they were drawn) so they come round again
     soon, while a one-draw exclusion stops the bounce landing straight back
     on them. Their turn is recorded as a pass, so the history shows who was
     asked and who answered. */
  function pass(st, rng) {
    if (st.last < 0) return null;
    var passer = st.last;
    st.since[passer] = st.lastPriorSince;
    if (st.history.length && !st.history[0].passed) st.history[0].passed = true;
    st.justPassed = passer;
    var out = pick(st, rng);
    st.justPassed = -1;
    return out;
  }

  function clear(st) {
    st.names.length = 0;
    st.present.length = 0;
    st.since.length = 0;
    st.history.length = 0;
    st.last = -1;
    st.justPassed = -1;
  }

  return {
    parseRoster: parseRoster,
    create: create,
    setPresent: setPresent,
    probabilities: probabilities,
    pick: pick,
    pass: pass,
    clear: clear,
    MAX_NAMES: MAX_NAMES,
    MAX_LEN: MAX_LEN
  };
});
