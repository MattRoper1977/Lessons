#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path.cwd()
SUITE = ROOT / "BUILD_ASDAN"
FRAMEWORK = SUITE / "_framework"
JS_PATH = FRAMEWORK / "asdan-teach.js"
CSS_PATH = FRAMEWORK / "asdan-teach.css"
README_PATH = FRAMEWORK / "README.md"

JS_MARKER = "FEATURE · Live We Do orchestration and purposeful motion lifecycle"
CSS_MARKER = "14 · WE DO ORCHESTRATION AND PURPOSEFUL MOTION"
README_MARKER = "## August 2026 classroom orchestration upgrade"

JS_FEATURE = r'''
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
'''

CSS_FEATURE = r'''
/* ==========================================================================
   14 · WE DO ORCHESTRATION AND PURPOSEFUL MOTION
   ---------------------------------------------------------------------------
   The lesson's own activity state drives everything here. The framework adds
   no answers and changes no score: it makes progress, the next discussion
   choice and completed matches readable from the back of the room.

   Motion is similarly purposeful. Hidden slides are paused, an illuminator
   replays when its teaching slide opens, one sweep places attention on the
   diagram, and decorative glow/ripple loops settle only after a mixed build.
   Loop-only concept diagrams keep moving because the cycle is the concept.
   ========================================================================== */

/* Nothing hidden should consume attention or processor time. When the slide
   becomes active its authored animation resumes; illuminators are restarted by
   the interaction layer so their explanatory sequence always begins at step 1. */
.slide:not(.active),.slide:not(.active) *{animation-play-state:paused!important}

.at-sr-only{
  position:absolute!important;width:1px!important;height:1px!important;
  padding:0!important;margin:-1px!important;overflow:hidden!important;
  clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important;
}

.at-activity-bar{
  display:grid;grid-template-columns:auto minmax(120px,1fr) auto auto;
  align-items:center;gap:10px;
  margin:10px 0 12px;padding:9px 10px;
  background:linear-gradient(90deg,var(--wedo-bg),#fff 72%);
  border:1px solid #e2e8f0;border-left:6px solid var(--wedo-border);
  border-radius:12px;box-shadow:0 5px 14px rgba(15,23,42,.07);
}
.at-activity-label{
  color:var(--text,#1f2937);font-size:.75rem;font-weight:900;
  letter-spacing:.08em;text-transform:uppercase;white-space:nowrap;
}
.at-activity-track{
  position:relative;display:block;height:12px;min-width:100px;
  overflow:hidden;border:1px solid #cbd5e1;border-radius:999px;
  background:rgba(255,255,255,.88);
}
.at-activity-fill{
  display:block;width:0;height:100%;border-radius:inherit;
  background:var(--wedo-border);
  transition:width var(--at-base) var(--at-ease),background var(--at-fast) var(--at-ease);
}
.at-activity-count{
  min-width:52px;text-align:center;color:var(--text,#1f2937);
  font-size:.84rem;font-weight:900;font-variant-numeric:tabular-nums;
}
.at-activity-actions{display:flex;align-items:center;justify-content:flex-end}
.at-random-pick{
  min-height:38px;padding:7px 13px;
  background:#fff;color:var(--text,#1f2937);
  border:2px solid var(--wedo-border);border-radius:999px;
  font-size:.8rem;font-weight:900;letter-spacing:.02em;
  box-shadow:0 3px 8px rgba(15,23,42,.09);
}
.at-random-pick:hover,.at-random-pick:focus-visible{
  background:var(--wedo-bg);color:var(--text,#1f2937);transform:translateY(-1px);
  outline:3px solid var(--wedo-border);outline-offset:2px;
}
.at-random-pick:disabled{opacity:.45;cursor:default;transform:none;box-shadow:none}
.at-activity-bar.at-complete{border-left-color:var(--success)}
.at-activity-bar.at-complete .at-activity-fill{background:var(--success)}
@keyframes atActivityComplete{
  0%{transform:scale(1)}45%{transform:scale(1.018)}100%{transform:scale(1)}
}
.at-activity-bar.at-just-complete{animation:atActivityComplete .5s var(--at-pop)}

/* A number makes the teacher's random choice and the revealed-answer number
   refer to the same object. The question mark remains as a separate cue that
   the card is still face down. */
.pres-card[data-at-card]::before{
  content:attr(data-at-card);width:26px;height:26px;
  background:#fff;color:var(--text,#1f2937);border:2px solid var(--wedo-border);
}
.pres-card:not(.done)[data-at-card]::after{
  content:'?';position:absolute;right:10px;top:8px;
  width:19px;height:19px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  background:var(--wedo-bg);color:var(--text,#1f2937);
  border:1px solid var(--wedo-border);font-size:.72rem;font-weight:900;
}
.pres-card.done[data-at-card]::before{
  content:'✓';background:var(--success);color:#fff;border-color:var(--success);
}
.pres-card.at-picked:not(.done){
  border-style:solid;border-color:var(--wedo-border);
  transform:translateY(-4px) scale(1.025);
  box-shadow:0 0 0 5px var(--wedo-bg),0 12px 26px rgba(15,23,42,.16);
}
.pres-card.at-picked:not(.done)::after{content:'→'}

/* When a word card is held, the other word cards quieten. Targets remain fully
   legible because the pupil still needs to compare every possible partner. */
#wedo2.at-match-holding #kw-pills .match-pill:not(.selected):not(.placed){
  opacity:.52;filter:saturate(.55);transform:scale(.97);
}
#kw-pills .match-pill{
  transition:opacity var(--at-fast) var(--at-ease),filter var(--at-fast) var(--at-ease),
             transform var(--at-fast) var(--at-ease),box-shadow var(--at-fast) var(--at-ease);
}

.at-pair-trail{
  margin:12px 0 4px;padding:10px 12px;
  border:1px solid #e2e8f0;border-left:6px solid var(--wedo-border);
  border-radius:12px;background:#fff;
}
.at-pair-trail[hidden]{display:none!important}
.at-pair-label{
  display:block;margin-bottom:7px;color:var(--text,#1f2937);
  font-size:.73rem;font-weight:900;letter-spacing:.08em;text-transform:uppercase;
}
.at-pair-list{display:grid;gap:7px}
@keyframes atPairIn{
  from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:translateY(0)}
}
.at-pair-chip{
  display:grid;grid-template-columns:26px minmax(90px,.8fr) 24px minmax(160px,1.3fr);
  align-items:center;gap:8px;
  min-height:42px;padding:7px 10px;
  border:1px solid #cbd5e1;border-left:4px solid var(--success);
  border-radius:10px;background:linear-gradient(90deg,var(--wedo-bg),#fff 48%);
  color:var(--text,#1f2937);font-size:.88rem;line-height:1.3;
  animation:atPairIn var(--at-fast) var(--at-ease) backwards;
}
.at-pair-number{
  width:23px;height:23px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  background:#fff;color:var(--text,#1f2937);border:2px solid var(--wedo-border);
  font-size:.72rem;font-weight:900;font-variant-numeric:tabular-nums;
}
.at-pair-key{font-weight:900}
.at-pair-arrow{text-align:center;color:var(--text,#1f2937);font-size:1rem;font-weight:900}
.at-pair-target{font-weight:650}

/* One replay sweep directs the eye without becoming permanent decoration. */
.ilm-replay{z-index:4}
.ilm.at-ilm-replaying{
  box-shadow:0 0 0 3px var(--ido-bg),0 10px 26px rgba(15,23,42,.10);
  border-radius:12px;
}
.at-ilm-sweep{
  position:absolute;z-index:3;left:0;top:0;bottom:0;width:34%;
  pointer-events:none;opacity:0;transform:translateX(-125%);
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.72),transparent);
}
@keyframes atIlmSpotlight{
  0%{opacity:0;transform:translateX(-125%)}
  18%{opacity:.68}
  100%{opacity:0;transform:translateX(390%)}
}
.ilm.at-ilm-replaying .at-ilm-sweep{
  animation:atIlmSpotlight 1.2s var(--at-ease) both;
}
/* In a mixed staged build, glow and ripple are emphasis, not the idea itself.
   They settle after the explanatory window. Loop-only concept diagrams are not
   marked by the JS and therefore remain continuous. */
.ilm.at-ilm-settled .at-settle-glow{animation:none!important;opacity:1!important}
.ilm.at-ilm-settled .at-settle-rip{animation:none!important;opacity:0!important}

@media (max-width:760px){
  .at-activity-bar{grid-template-columns:auto 1fr auto;gap:7px}
  .at-activity-actions{grid-column:1/-1;justify-content:flex-start}
  .at-random-pick{min-height:34px;padding:5px 11px}
  .at-pair-chip{grid-template-columns:24px minmax(70px,.75fr) 18px minmax(110px,1.25fr);font-size:.8rem}
}
@media (max-width:480px){
  .at-activity-bar{grid-template-columns:1fr auto}
  .at-activity-label{grid-column:1/-1}
  .at-activity-track{min-width:0}
  .at-pair-chip{grid-template-columns:23px 1fr;gap:5px 8px}
  .at-pair-arrow{display:none}
  .at-pair-target{grid-column:2}
}
@media print{
  .at-activity-bar,.at-pair-trail,.at-ilm-sweep{display:none!important}
  .pres-card.at-picked{transform:none!important;box-shadow:none!important}
}
@media (prefers-reduced-motion:reduce){
  .at-activity-fill,.at-activity-bar.at-just-complete,.at-pair-chip,
  .pres-card.at-picked,.ilm.at-ilm-replaying .at-ilm-sweep{
    animation:none!important;transition:none!important;transform:none!important;
  }
  .at-ilm-sweep{display:none!important}
  .ilm.at-ilm-replaying{box-shadow:none!important}
}

'''

README_FEATURE = r'''

---

## August 2026 classroom orchestration upgrade

This pass deepens the existing presentation-only framework without changing any
lesson wording, question, answer, outcome, assessment evidence or sequence.

**We Do 1 — prediction cards**

- A large class-progress rail mirrors the real `.done` state.
- Every card carries the same visible number as the answer it produces.
- **Pick a card** chooses an unrevealed card for talk-before-tap without opening
  it, changing the score or bypassing the authored `presTap()` behaviour.
- The picked state is visible, keyboard-focused and announced accessibly.

**We Do 2 — matching**

- A second progress rail mirrors the real `.correct` target state.
- Holding a word card quietens the unused word cards while leaving every target
  fully readable for comparison.
- Each completed pair is copied into a connection trail using only the exact
  existing word-card and target wording. Reset and Reveal remain the authored
  controls and the trail follows them automatically.

**Purposeful CSS and SVG motion**

- Animations on inactive slides are paused.
- An illuminator restarts whenever its I Do slide becomes active, as well as from
  the existing Replay control.
- One short light sweep places the eye on the diagram; it does not loop.
- In diagrams that combine a staged build with decorative glow or ripple, those
  decorative loops settle after the teaching window. The four loop-only concept
  diagrams remain continuous because their cycle carries the meaning.
- Reduced-motion and print modes remove the new motion and presentation chrome.

The content-integrity gate still strips the generated framework blocks and
compares all 31 decks to the recorded baseline byte for byte.
'''


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one signature, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    js = JS_PATH.read_text(encoding="utf-8")
    css = CSS_PATH.read_text(encoding="utf-8")
    readme = README_PATH.read_text(encoding="utf-8")

    if JS_MARKER in js or CSS_MARKER in css or README_MARKER in readme:
        raise SystemExit("Upgrade markers already present; refusing a duplicate application")

    replay_old = """    if (cap) {\n      cap.style.animation = 'none';\n      void cap.offsetWidth;\n      cap.style.animation = '';\n    }\n  }\n\n  AT.replayIlluminator = replayIlluminator;\n"""
    replay_new = """    if (cap) {\n      cap.style.animation = 'none';\n      void cap.offsetWidth;\n      cap.style.animation = '';\n    }\n    startIlluminatorSpotlight(block);\n    scheduleIlluminatorSettle(block);\n  }\n\n  AT.replayIlluminator = replayIlluminator;\n"""
    js = replace_once(js, replay_old, replay_new, "illuminator replay hook")

    registration_marker = """  /* ==================================================================\n     Registration\n     ================================================================== */\n"""
    js = replace_once(js, registration_marker, JS_FEATURE + "\n" + registration_marker, "JS registration marker")
    js = replace_once(
        js,
        """    setupStepBuild();\n  });\n""",
        """    setupStepBuild();\n    setupWeDoEnhancements();\n    setupMotionLifecycle();\n  });\n""",
        "JS boot registration",
    )

    reduced_marker = """/* ==========================================================================\n   14 · REDUCED MOTION\n"""
    css = replace_once(
        css,
        reduced_marker,
        CSS_FEATURE + "/* ==========================================================================\n   15 · REDUCED MOTION\n",
        "CSS reduced-motion marker",
    )

    readme = readme.rstrip() + README_FEATURE.rstrip() + "\n"

    JS_PATH.write_text(js, encoding="utf-8")
    CSS_PATH.write_text(css, encoding="utf-8")
    README_PATH.write_text(readme, encoding="utf-8")
    print("Patched asdan-teach.js, asdan-teach.css and framework README")


if __name__ == "__main__":
    main()
