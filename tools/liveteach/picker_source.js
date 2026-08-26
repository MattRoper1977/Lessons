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
  function clampName(n) {
    /* slice() counts UTF-16 code units, so a cut can land between the halves
       of a surrogate pair and leave a lone high surrogate — which renders as
       the replacement diamond in a name on the class screen. Cut by
       CHARACTERS instead. */
    var chars = Array.from(n);
    return chars.length > MAX_LEN ? chars.slice(0, MAX_LEN).join('') : n;
  }
  function parseRoster(text) {
    var seen = Object.create(null);
    var out = [];
    var dropped = 0;
    String(text == null ? '' : text).split(/[\n,]/).forEach(function (raw) {
      var n = clampName(String(raw).replace(/\s+/g, ' ').trim());
      if (!n) return;
      /* Normalise before comparing: a register pasted from two sources can
         carry the same name in NFC and NFD, which are byte-different and
         pixel-identical — exactly the indistinguishable-duplicate the dedupe
         exists to prevent. */
      var key = (n.normalize ? n.normalize('NFC') : n).toLowerCase();
      if (seen[key]) return;
      seen[key] = 1;
      if (out.length < MAX_NAMES) out.push(n); else dropped++;
    });
    /* The caller is told what was lost, so a 45-name paste cannot be
       confirmed as "40 names loaded" with no mention of the five. */
    out.dropped = dropped;
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
    var was = st.present[i];
    st.present[i] = !!on;
    /* st.last is deliberately NOT cleared when that pupil is marked away. It
       records who answered most recently, which is the single fact P2 rests
       on; forgetting it meant a pupil could be called, marked away, marked
       back, and called again immediately — a repeat, by the shipped buttons.
       An away pupil is already excluded by `present`, so keeping `last`
       costs the room nothing and keeps the guarantee true across attendance
       changes. */
    /* Coming BACK is the subtle one. since only advances for pupils who are
       here, so a pupil marked away moments after being called keeps since=0
       — and a frozen zero never expires. Returning with that zero made them
       weightless, which in a small room emptied the pool into the uniform
       fallback and let the pupil who had just answered be drawn again: the
       exact repeat P2 exists to forbid. So a returning pupil re-enters at
       least at 1 — in the pool, ordinary priority. Not higher: someone who
       has just walked back in is the last person who should be cold-called
       on the spot. */
    if (st.present[i] && !was && st.since[i] < 1) st.since[i] = 1;
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
      /* Nobody has any weight left. Falling back to "everyone present,
         equally" is right — but it must NOT quietly re-admit the pupil who
         just answered: P2 is the phase's one absolute, so the fallback drops
         them too whenever anyone else is available, and only concedes when
         there is literally nobody else to ask. */
      var present = [];
      for (var j = 0; j < st.names.length; j++) if (st.present[j]) present.push(j);
      if (!present.length) return null;
      var eligible = present.filter(function (i) { return i !== st.last && i !== st.justPassed; });
      var pool = eligible.length ? eligible : present;
      /* fellBack means precisely "this draw could not honour the no-repeat
         guarantee" — not "the room is small". Both views word their notice
         from that, so the notice is true whichever way the room got here. */
      fellBack = !eligible.length;
      w = st.names.map(function (_, i) { return pool.indexOf(i) === -1 ? 0 : 1; });
      total = pool.length;
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
