(() => {
  'use strict';

  const root = document.documentElement;
  if (root.dataset.growUpgrade === 'ready' || root.dataset.growUpgrade === 'loading') return;
  root.dataset.growUpgrade = 'loading';

  const reducedMotion = Boolean(window.matchMedia?.('(prefers-reduced-motion: reduce)').matches);
  const motionTimers = new WeakMap();
  const revealTimers = new WeakMap();
  const activityQueue = new Set();
  let activityFrame = 0;
  let activeSlide = null;
  let slideSyncQueued = false;
  let liveRegion = null;
  let announceTimer = 0;

  const interactiveSelector = [
    'button',
    'a[href]',
    '.pres-card',
    '.match-pill',
    '.match-target',
    '.hl-sentence',
    '.fact-dot',
    '[onclick]:not(.slide):not(.midpoint-overlay):not(.v4-modal-overlay):not(.lesson-complete-overlay)'
  ].join(',');

  const nativeInteractive = element => /^(A|BUTTON|INPUT|SELECT|TEXTAREA|SUMMARY)$/.test(element.tagName);

  function elementsWithin(scope, selector) {
    const elements = [];
    if (scope instanceof Element && scope.matches(selector)) elements.push(scope);
    if (scope?.querySelectorAll) elements.push(...scope.querySelectorAll(selector));
    return elements;
  }

  function announce(message) {
    if (!message || !liveRegion) return;
    window.clearTimeout(announceTimer);
    liveRegion.textContent = '';
    announceTimer = window.setTimeout(() => {
      liveRegion.textContent = message;
    }, 30);
  }

  function createLiveRegion() {
    liveRegion = document.getElementById('grow-live-region');
    if (liveRegion) return;
    liveRegion = document.createElement('div');
    liveRegion.id = 'grow-live-region';
    liveRegion.className = 'grow-live-region';
    liveRegion.setAttribute('role', 'status');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    document.body.appendChild(liveRegion);
  }

  function makeKeyboardOperable(element) {
    if (!element || element.dataset.growKeyboard === 'true' || nativeInteractive(element)) return;
    element.dataset.growKeyboard = 'true';
    if (!element.hasAttribute('role')) element.setAttribute('role', 'button');
    if (!element.hasAttribute('tabindex')) element.setAttribute('tabindex', '0');
    element.addEventListener('keydown', event => {
      if (event.key !== 'Enter' && event.key !== ' ') return;
      event.preventDefault();
      element.click();
    });
  }

  function isDisplayed(element) {
    return Boolean(element && !element.hidden && getComputedStyle(element).display !== 'none');
  }

  function syncInteractiveState(element) {
    if (!(element instanceof Element)) return;

    if (element.matches('.pres-card')) {
      element.setAttribute('aria-pressed', String(element.classList.contains('done')));
    }

    if (element.matches('.match-pill')) {
      element.setAttribute('aria-pressed', String(element.classList.contains('selected')));
    }

    if (element.matches('.match-target')) {
      if (element.classList.contains('correct')) {
        element.dataset.growState = 'correct';
        element.setAttribute('aria-invalid', 'false');
      } else if (element.classList.contains('wrong')) {
        element.dataset.growState = 'incorrect';
        element.setAttribute('aria-invalid', 'true');
      } else {
        delete element.dataset.growState;
        element.removeAttribute('aria-invalid');
      }
    }

    if (element.matches('.answer')) {
      element.setAttribute('aria-hidden', String(!isDisplayed(element)));
    }

    if (element.matches('.hint-box, .wagoll-panel, .v5-step')) {
      const visible = element.classList.contains('show') || element.classList.contains('visible') || element.classList.contains('revealed');
      element.setAttribute('aria-hidden', String(!visible));
    }

    if (element.matches('.hint-btn')) {
      element.setAttribute('aria-expanded', String(Boolean(element.nextElementSibling?.classList.contains('show'))));
    }

    if (element.matches('.wagoll-trigger')) {
      const panel = document.getElementById('wagoll-panel') || element.nextElementSibling;
      element.setAttribute('aria-expanded', String(Boolean(panel?.classList.contains('visible'))));
    }

    if (element.matches('.fact-dot')) {
      if (element.classList.contains('active')) element.setAttribute('aria-current', 'step');
      else element.removeAttribute('aria-current');
    }
  }

  function enhanceInteractive(scope = document) {
    elementsWithin(scope, interactiveSelector).forEach(element => {
      makeKeyboardOperable(element);
      if (!element.getAttribute('aria-label') && element.getAttribute('title') && !element.textContent.trim()) {
        element.setAttribute('aria-label', element.getAttribute('title'));
      }
      syncInteractiveState(element);
    });
  }

  function isWeDoSlide(slide) {
    const label = `${slide.getAttribute('data-title') || ''} ${slide.querySelector('.slide-tag')?.textContent || ''}`;
    return slide.getAttribute('data-type') === 'wedo' || /\bwe do\b/i.test(label);
  }

  function createActivityBar(slide, total, mode) {
    const bar = document.createElement('div');
    bar.className = 'grow-activity-bar';
    bar.dataset.growMode = mode;

    const rail = document.createElement('div');
    rail.className = 'grow-activity-rail';
    rail.setAttribute('role', 'progressbar');
    rail.setAttribute('aria-label', 'Class activity progress');
    rail.setAttribute('aria-valuemin', '0');
    rail.setAttribute('aria-valuemax', String(total));
    rail.setAttribute('aria-valuenow', '0');
    rail.innerHTML = '<span class="grow-activity-fill" aria-hidden="true"></span>';

    const count = document.createElement('span');
    count.className = 'grow-activity-count';
    count.setAttribute('aria-hidden', 'true');
    count.textContent = `0/${total}`;

    bar.append(rail, count);
    const tag = slide.querySelector('.slide-tag');
    if (tag) tag.insertAdjacentElement('afterend', bar);
    else slide.prepend(bar);
    return bar;
  }

  function setActivityProgress(slide, completed, total, shouldAnnounce = false) {
    const bar = slide.querySelector('.grow-activity-bar');
    const rail = bar?.querySelector('.grow-activity-rail');
    const count = bar?.querySelector('.grow-activity-count');
    if (!bar || !rail || !count) return;

    const percentage = total ? Math.round((completed / total) * 100) : 0;
    rail.style.setProperty('--grow-progress', `${percentage}%`);
    rail.setAttribute('aria-valuemax', String(total));
    rail.setAttribute('aria-valuenow', String(completed));
    count.textContent = `${completed}/${total}`;

    const complete = total > 0 && completed === total;
    slide.classList.toggle('grow-activity-complete', complete);
    if (shouldAnnounce) announce(complete ? 'Class activity complete.' : `${completed} of ${total} activity points complete.`);
  }

  function spotlightCard(card) {
    const slide = card.closest('.slide');
    slide?.querySelectorAll('.pres-card.grow-picked').forEach(element => element.classList.remove('grow-picked'));
    card.classList.add('grow-picked');
    card.focus({ preventScroll: true });
    card.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth', block: 'center' });
    announce('Discussion card selected. Talk first, then reveal.');
  }

  function sequenceMode(slide) {
    const text = (slide.innerText || '').toLowerCase();
    return text.includes('put it in order') || text.includes('belong in an order');
  }

  function enhancePresentationActivity(slide, cards) {
    slide.dataset.growActivity = 'presentation';
    const bar = createActivityBar(slide, cards.length, 'presentation');

    const picker = document.createElement('button');
    picker.type = 'button';
    picker.className = 'grow-random-pick';
    picker.textContent = '🎲';
    picker.setAttribute('aria-label', 'Choose an unrevealed discussion card');
    picker.addEventListener('click', () => {
      const available = cards.filter(card => !card.classList.contains('done'));
      const pool = available.length ? available : cards;
      const card = pool[Math.floor(Math.random() * pool.length)];
      if (card) spotlightCard(card);
    });
    bar.appendChild(picker);

    const trail = document.createElement('div');
    trail.className = 'grow-discussion-trail';
    trail.setAttribute('aria-label', 'Discussion points');
    cards.forEach((card, index) => {
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.className = 'grow-discussion-dot';
      dot.textContent = String(index + 1);
      dot.setAttribute('aria-label', `Focus discussion point ${index + 1}`);
      dot.addEventListener('click', () => spotlightCard(card));
      trail.appendChild(dot);

      makeKeyboardOperable(card);
      card.addEventListener('click', () => {
        window.setTimeout(() => {
          card.classList.remove('grow-picked');
          if (sequenceMode(slide) && card.classList.contains('done') && !card.dataset.growOrder) {
            const assigned = cards.map(item => Number(item.dataset.growOrder || 0));
            card.dataset.growOrder = String(Math.max(0, ...assigned) + 1);
          }
          scheduleActivityUpdate(slide, true);
        }, 0);
      });
    });

    bar.insertAdjacentElement('afterend', trail);
    updatePresentationActivity(slide);
  }

  function updatePresentationActivity(slide, shouldAnnounce = false) {
    const cards = [...slide.querySelectorAll('.pres-card')];
    const dots = [...slide.querySelectorAll('.grow-discussion-dot')];
    cards.forEach((card, index) => {
      const done = card.classList.contains('done');
      card.setAttribute('aria-pressed', String(done));
      dots[index]?.classList.toggle('done', done);
      if (!done) delete card.dataset.growOrder;
    });
    const completed = cards.filter(card => card.classList.contains('done')).length;
    setActivityProgress(slide, completed, cards.length, shouldAnnounce);
  }

  function pairIdForPill(pill) {
    const inline = pill.getAttribute('onclick') || '';
    return inline.match(/selectKW\(this\s*,\s*['"]([^'"]+)['"]\)/)?.[1] || pill.dataset.id || pill.dataset.match || null;
  }

  function matchingPillForTarget(slide, target) {
    const id = target.getAttribute('data-correct');
    if (!id) return null;
    return [...slide.querySelectorAll('.match-pill')].find(pill => pairIdForPill(pill) === id) || null;
  }

  function createPairChip(slide, target, index) {
    const pill = matchingPillForTarget(slide, target);
    const chip = document.createElement('div');
    chip.className = 'grow-pair-chip';
    chip.dataset.growTarget = String(index);
    chip.setAttribute('role', 'listitem');

    const source = document.createElement('span');
    source.className = 'grow-pair-source';
    source.textContent = pill?.textContent.trim() || String(index + 1);

    const arrow = document.createElement('span');
    arrow.className = 'grow-pair-arrow';
    arrow.setAttribute('aria-hidden', 'true');
    arrow.textContent = '→';

    const destination = document.createElement('span');
    destination.className = 'grow-pair-destination';
    destination.textContent = target.textContent.trim();

    chip.append(source, arrow, destination);
    return chip;
  }

  function enhanceMatchingActivity(slide, pills, targets) {
    slide.dataset.growActivity = 'matching';
    createActivityBar(slide, targets.length, 'matching');

    const trail = document.createElement('div');
    trail.className = 'grow-pair-trail';
    trail.setAttribute('role', 'list');
    trail.setAttribute('aria-label', 'Completed connections');
    const anchor = slide.querySelector('.scaffold-box') || slide.querySelector('.wagoll-trigger') || targets.at(-1);
    if (anchor) anchor.insertAdjacentElement('beforebegin', trail);
    else slide.appendChild(trail);

    pills.forEach(pill => makeKeyboardOperable(pill));
    targets.forEach(target => makeKeyboardOperable(target));
    updateMatchingActivity(slide);
  }

  function updateMatchingActivity(slide, shouldAnnounce = false) {
    const pills = [...slide.querySelectorAll('.match-pill')];
    const targets = [...slide.querySelectorAll('.match-target')];
    const trail = slide.querySelector('.grow-pair-trail');
    if (!trail) return;

    pills.forEach(pill => pill.setAttribute('aria-pressed', String(pill.classList.contains('selected'))));
    const hasSelection = pills.some(pill => pill.classList.contains('selected'));
    slide.classList.toggle('grow-has-selection', hasSelection);

    targets.forEach((target, index) => {
      syncInteractiveState(target);
      const existing = trail.querySelector(`[data-grow-target="${index}"]`);
      if (target.classList.contains('correct')) {
        if (!existing) trail.appendChild(createPairChip(slide, target, index));
      } else if (existing) {
        existing.remove();
      }
    });

    const completed = targets.filter(target => target.classList.contains('correct')).length;
    setActivityProgress(slide, completed, targets.length, shouldAnnounce);
  }

  function enhanceWeDoSlide(slide) {
    if (!isWeDoSlide(slide) || slide.dataset.growWeDo === 'true') return;
    slide.dataset.growWeDo = 'true';

    const cards = [...slide.querySelectorAll('.pres-card')];
    const pills = [...slide.querySelectorAll('.match-pill')];
    const targets = [...slide.querySelectorAll('.match-target')];

    if (cards.length) enhancePresentationActivity(slide, cards);
    else if (pills.length && targets.length) enhanceMatchingActivity(slide, pills, targets);
  }

  function scheduleActivityUpdate(slide, shouldAnnounce = false) {
    if (!slide?.dataset.growActivity) return;
    if (shouldAnnounce) slide.dataset.growAnnounce = 'true';
    activityQueue.add(slide);
    if (activityFrame) return;
    activityFrame = window.requestAnimationFrame(() => {
      activityFrame = 0;
      activityQueue.forEach(item => {
        const announceUpdate = item.dataset.growAnnounce === 'true';
        delete item.dataset.growAnnounce;
        if (item.dataset.growActivity === 'presentation') updatePresentationActivity(item, announceUpdate);
        else if (item.dataset.growActivity === 'matching') updateMatchingActivity(item, announceUpdate);
      });
      activityQueue.clear();
    });
  }

  function replayDiagram(diagram) {
    if (!diagram || reducedMotion) return;
    diagram.classList.remove('grow-diagram-replaying');
    void diagram.offsetWidth;
    diagram.classList.add('grow-diagram-replaying');
    diagram.querySelectorAll('.pop, .draw, .rise, .fill, .glow, .spin, .hand, .ride, .rip, .sweep').forEach(element => {
      element.getAnimations().forEach(animation => {
        try {
          animation.cancel();
          animation.play();
        } catch (_) {
          // Authored CSS remains authoritative if the browser cannot restart an animation.
        }
      });
    });
    window.setTimeout(() => diagram.classList.remove('grow-diagram-replaying'), 1250);
  }

  function enhanceDiagram(diagram) {
    if (diagram.dataset.growDiagram === 'true') return;
    diagram.dataset.growDiagram = 'true';
    diagram.setAttribute('role', 'button');
    diagram.setAttribute('tabindex', '0');
    const caption = diagram.querySelector('.ilm-cap')?.textContent?.trim();
    diagram.setAttribute('aria-label', caption ? `Replay diagram: ${caption}` : 'Replay diagram animation');

    const icon = document.createElement('span');
    icon.className = 'grow-diagram-replay-icon';
    icon.setAttribute('aria-hidden', 'true');
    icon.textContent = '↻';

    const sweep = document.createElement('span');
    sweep.className = 'grow-diagram-sweep';
    sweep.setAttribute('aria-hidden', 'true');
    diagram.append(icon, sweep);

    diagram.addEventListener('click', event => {
      if (event.target.closest('button, a, input, select, textarea')) return;
      replayDiagram(diagram);
      announce('Diagram animation replayed.');
    });
    diagram.addEventListener('keydown', event => {
      if (event.key !== 'Enter' && event.key !== ' ') return;
      event.preventDefault();
      replayDiagram(diagram);
      announce('Diagram animation replayed.');
    });
  }

  function enhanceDiagrams(scope = document) {
    elementsWithin(scope, '.ilm').forEach(enhanceDiagram);
  }

  function prepareReveal(slide) {
    const selector = [
      '.slide-tag', 'h1', 'h2', '.li-box', '.ido-box', '.task-box', '.wedo-capture',
      '.scaffold-box', '.aspire-box', '.sc-box', '.ilm', '.content-grid > *',
      '.arrival-grid > *', '.compare-grid-3 > *', '.lundy-grid > *'
    ].join(',');
    let order = 0;
    slide.querySelectorAll(selector).forEach(element => {
      if (element.closest('.slide') !== slide || element.classList.contains('grow-reveal')) return;
      element.classList.add('grow-reveal');
      element.style.setProperty('--grow-order', String(Math.min(order++, 8)));
    });
  }

  function settleMotion(slide) {
    const previous = motionTimers.get(slide);
    if (previous) window.clearTimeout(previous);
    slide.classList.remove('grow-motion-settled');
    if (reducedMotion) {
      slide.classList.add('grow-motion-settled');
      return;
    }
    motionTimers.set(slide, window.setTimeout(() => slide.classList.add('grow-motion-settled'), 6200));
  }

  function activateSlide(slide, slides, announceCurrent) {
    if (!slide || activeSlide === slide) return;

    if (activeSlide) {
      window.clearTimeout(revealTimers.get(activeSlide));
      window.clearTimeout(motionTimers.get(activeSlide));
      activeSlide.classList.remove('grow-entering', 'grow-ready');
    }

    activeSlide = slide;
    slide.classList.remove('grow-ready', 'grow-motion-settled');
    slide.classList.add('grow-entering');

    window.requestAnimationFrame(() => {
      window.requestAnimationFrame(() => {
        if (activeSlide !== slide) return;
        slide.classList.add('grow-ready');
        slide.querySelectorAll('.ilm').forEach(replayDiagram);
      });
    });

    revealTimers.set(slide, window.setTimeout(() => slide.classList.remove('grow-entering'), reducedMotion ? 0 : 1250));
    settleMotion(slide);

    if (announceCurrent) {
      const index = slides.indexOf(slide);
      const title = slide.getAttribute('data-title') || slide.querySelector('h1,h2')?.textContent?.trim() || `Slide ${index + 1}`;
      announce(`${title}. Slide ${index + 1} of ${slides.length}.`);
    }
  }

  function syncSlides({ announceCurrent = false } = {}) {
    const slides = [...document.querySelectorAll('.slide')];
    let current = null;

    slides.forEach(slide => {
      const active = slide.classList.contains('active');
      if (active && !current) current = slide;
      const hidden = String(!active);
      if (slide.getAttribute('aria-hidden') !== hidden) slide.setAttribute('aria-hidden', hidden);
      prepareReveal(slide);
      enhanceWeDoSlide(slide);
    });

    enhanceDiagrams();
    activateSlide(current, slides, announceCurrent);

    const progress = document.getElementById('progressLabel');
    if (progress) {
      progress.setAttribute('role', 'status');
      progress.setAttribute('aria-live', 'polite');
    }
  }

  function queueSlideSync() {
    if (slideSyncQueued) return;
    slideSyncQueued = true;
    window.requestAnimationFrame(() => {
      slideSyncQueued = false;
      syncSlides({ announceCurrent: true });
    });
  }

  function installObservers() {
    const observer = new MutationObserver(mutations => {
      let activeChanged = false;

      mutations.forEach(mutation => {
        if (mutation.type === 'attributes') {
          const element = mutation.target;
          syncInteractiveState(element);

          if (element.classList?.contains('slide') && mutation.attributeName === 'class') {
            const previous = new Set((mutation.oldValue || '').split(/\s+/).filter(Boolean));
            const wasActive = previous.has('active');
            const isActive = element.classList.contains('active');
            if (wasActive !== isActive) activeChanged = true;
          }

          const activitySlide = element.closest?.('.slide[data-grow-activity]');
          if (activitySlide) scheduleActivityUpdate(activitySlide);
        }

        mutation.addedNodes.forEach(node => {
          if (!(node instanceof Element)) return;
          enhanceInteractive(node);
          enhanceDiagrams(node);
          elementsWithin(node, '.slide').forEach(enhanceWeDoSlide);
        });
      });

      if (activeChanged) queueSlideSync();
    });

    observer.observe(document.body, {
      subtree: true,
      childList: true,
      attributes: true,
      attributeOldValue: true,
      attributeFilter: ['class', 'hidden']
    });
  }

  function describeInteraction(target) {
    if (!(target instanceof Element)) return;
    const activity = target.closest('.slide[data-grow-activity]');
    if (activity) scheduleActivityUpdate(activity, true);

    const matchTarget = target.closest('.match-target');
    if (matchTarget?.classList.contains('correct')) announce('Correct connection confirmed.');
    else if (matchTarget?.classList.contains('wrong')) announce('That connection is not correct yet. Try again.');
    else if (target.closest('.v5-step-controls')) announce('Next teaching step revealed.');
    else if (target.closest('.hint-btn')) {
      const box = target.closest('.hint-btn')?.nextElementSibling;
      announce(box?.classList.contains('show') ? 'Hint shown.' : 'Hint hidden.');
    } else if (target.closest('.wagoll-trigger')) announce('Model example shown.');
  }

  function init() {
    if (!document.body || root.dataset.growUpgrade === 'ready') return;
    createLiveRegion();
    enhanceInteractive();
    enhanceDiagrams();
    root.dataset.growUpgrade = 'ready';
    syncSlides();
    installObservers();

    document.addEventListener('click', event => {
      window.setTimeout(() => {
        enhanceInteractive();
        document.querySelectorAll('.answer, .hint-box, .wagoll-panel, .v5-step, .match-target, .match-pill, .pres-card, .fact-dot').forEach(syncInteractiveState);
        describeInteraction(event.target);
      }, 0);
    }, true);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
/* ASDAN-VISUAL-LEARNING:JS:BEGIN v1 */
window.ASDANVisualPayloads = Object.assign(window.ASDANVisualPayloads || {}, {"PEQ_W1_Knowing_Myself":{"path":"GROW_ASDAN/PEQ/PEQ_W1_Knowing_Myself.html","pathway":"GROW","subsection":"PEQ","lessonTitle":"Week 1 · Knowing Myself","targetTitle":"We Do 1","title":"Self-knowledge evidence map","purpose":"Move the lesson from adjective collection to testable self-knowledge that can guide independent decisions.","activity":{"type":"hotspot","scene":"profile","prompt":"Commit a prediction about which evidence type will be easiest to use. Open every part of the self-knowledge map and compare the strength of the evidence.","hotspots":[{"id":"h1","x":18,"y":24,"label":"STRENGTH","note":"Name the action that supports the strength, not only the label."},{"id":"h2","x":50,"y":18,"label":"INTEREST","note":"Specify the activity or topic and what keeps attention."},{"id":"h3","x":82,"y":27,"label":"VALUE","note":"Show the choice or behaviour that reveals what matters."},{"id":"h4","x":23,"y":66,"label":"WORKING CONDITION","note":"Notice when focus is stronger: pace, space, group size or task type."},{"id":"h5","x":52,"y":72,"label":"STARTING POINT","note":"Record what can already be done and what is still developing."},{"id":"h6","x":82,"y":65,"label":"NEXT TEST","note":"Choose a small real task that can test the self-view."}],"completion":"Self-awareness grows when a pupil compares a self-description with actions, conditions and a new test.","predictionOptions":["A strength example will be easiest","A working-condition example will be easiest","The next test will reveal something unexpected"]},"independent":"Complete your profile using one strength, interest, value and working condition. Add the evidence and one next test for each.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original six-lens self-knowledge map with evidence tags and a next-test arrow.","mediaKey":"peq","slug":"PEQ_W1_Knowing_Myself","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["PREDICT","TEST","COMPARE","JUSTIFY"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"6219dd18bed377655f598c063152f6c6030332bfea996873619b50f65e9e612d"}});
/* ============================================================================
 * BLOCKED — DO NOT MOUNT
 *
 * This engine is committed but loaded by nothing. No lesson in this repository
 * references it, and none may until the blockers in README.md are cleared.
 *
 * Named blocking items (see README.md for the derivations):
 *   1. The vendor's decisive gate -- full post-integration regression in a real,
 *      current checkout -- is UNRUN. Nothing pupil-facing merges until it is.
 *   2. CLEARED 5 Aug 2026 -- reduced motion is now read from matchMedia at load
 *      and watched with a change listener; .asvl-static follows the OS preference.
 *      Proven in both directions in a real browser; family classified as RM-3.
 *   3. The six D&T decks are on a different chassis and outside the BUILD
 *      compiler's scope. They do not mount by mounting this.
 *
 * Landed 5 Aug 2026, band A of the ASDAN Visual-Learning review.
 * ========================================================================== */

/* ASDAN Visual Learning — progressive enhancement, rehearsal only. */
(() => {
  'use strict';

  const API_NAME = 'ASDANVisualLearning';
  if (window[API_NAME]?.version) return;

  const qs = (selector, root = document) => root.querySelector(selector);
  const qsa = (selector, root = document) => Array.from(root.querySelectorAll(selector));
  const el = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined && text !== null) node.textContent = String(text);
    return node;
  };
  const button = (label, className = 'asvl-button') => {
    const node = el('button', className, label);
    node.type = 'button';
    return node;
  };
  const setText = (node, text) => { if (node) node.textContent = String(text ?? ''); };

  /* Reduced motion, watched rather than sampled once.
     The blanket CSS rule already suppressed animation when the OS asked for it,
     but nothing in JS read the preference, so .asvl-static -- and the button that
     reports it -- stayed false while motion was actually off. Pattern taken from
     art-visual-learning.js, which fixed the same defect in the same shape. */
  const motionQuery = typeof window.matchMedia === 'function'
    ? window.matchMedia('(prefers-reduced-motion: reduce)')
    : null;
  const prefersReducedMotion = () => !!(motionQuery && motionQuery.matches);
  const motionSubscribers = new Set();
  if (motionQuery) {
    const onMotionChange = () => { motionSubscribers.forEach(fn => { try { fn(); } catch (e) {} }); };
    if (motionQuery.addEventListener) motionQuery.addEventListener('change', onMotionChange);
    else if (motionQuery.addListener) motionQuery.addListener(onMotionChange);
  }
  const slugFromLocation = () => {
    const declared = document.documentElement.dataset.asdanLesson || document.body?.dataset.asdanLesson;
    if (declared) return declared;
    const path = decodeURIComponent(location.pathname || '');
    const name = path.split('/').pop() || '';
    return name.replace(/\.html?$/i, '');
  };
  const seededShuffle = (values, seedText) => {
    const out = values.slice();
    let seed = 2166136261;
    for (const char of String(seedText)) {
      seed ^= char.charCodeAt(0);
      seed = Math.imul(seed, 16777619) >>> 0;
    }
    const next = () => {
      seed += 0x6D2B79F5;
      let t = seed;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
    for (let i = out.length - 1; i > 0; i -= 1) {
      const j = Math.floor(next() * (i + 1));
      [out[i], out[j]] = [out[j], out[i]];
    }
    if (out.length > 2 && out.every((item, index) => item === values[index])) {
      [out[0], out[1]] = [out[1], out[0]];
    }
    return out;
  };
  const announce = (panel, message) => {
    const live = qs('.asvl-live', panel);
    if (!live) return;
    live.textContent = '';
    window.setTimeout(() => { live.textContent = String(message); }, 20);
  };
  const safeFocus = node => { try { node?.focus({ preventScroll: false }); } catch (_) { node?.focus?.(); } };

  const pathwayCopy = {
    BUILD: {
      eyebrow: 'BUILD · SEE → CHOOSE → SAY → DO',
      predictionTitle: 'Look first',
      completionLead: 'You have rehearsed the decision.',
      colourLabel: 'BUILD visual rehearsal'
    },
    GROW: {
      eyebrow: 'GROW · PREDICT → TEST → COMPARE → JUSTIFY',
      predictionTitle: 'Commit a prediction',
      completionLead: 'You have compared evidence rather than guessed.',
      colourLabel: 'GROW visual investigation'
    },
    LAUNCH: {
      eyebrow: 'LAUNCH · INVESTIGATE → LOCATE EVIDENCE → REASON → ACT',
      predictionTitle: 'Commit a prediction',
      completionLead: 'The investigation is complete; now locate authentic evidence.',
      colourLabel: 'LAUNCH evidence-led investigation'
    }
  };

  function createState(payload) {
    const activity = payload.activity;
    const state = {
      prediction: null,
      completed: false,
      explanationOpen: false,
      transferOpen: false,
      staticMode: false,
      selectedItem: null,
      placed: new Map(),
      selectedEvidence: new Set(),
      openedHotspots: new Set(),
      sequence: activity.type === 'sequence'
        ? seededShuffle(activity.steps.map(step => step.id), payload.slug)
        : [],
      runs: [],
      locator: { evidenceForm: null, location: null, route: null },
      feedback: '',
      feedbackKind: 'neutral'
    };
    return state;
  }

  function targetForPayload(payload) {
    const exact = qsa('.slide').find(slide => (slide.getAttribute('data-title') || '').trim() === payload.targetTitle);
    if (exact) return exact;
    const wedo = qs('.slide[data-type="wedo"]') || qsa('.slide').find(slide => /we do/i.test(slide.getAttribute('data-title') || ''));
    return wedo || qs('.slide.active') || qs('main') || document.body;
  }

  function createPanel(payload) {
    const panel = el('section', `asvl-panel asvl-${payload.pathway.toLowerCase()}`);
    panel.dataset.asdanVisualLearning = payload.slug;
    panel.dataset.pathway = payload.pathway;
    panel.setAttribute('aria-label', `${payload.title}. ${pathwayCopy[payload.pathway].colourLabel}`);
    panel.tabIndex = -1;

    const header = el('header', 'asvl-header');
    const headText = el('div', 'asvl-header-text');
    headText.append(
      el('p', 'asvl-eyebrow', pathwayCopy[payload.pathway].eyebrow),
      el('h3', 'asvl-title', payload.title),
      el('p', 'asvl-purpose', payload.purpose)
    );
    const tools = el('div', 'asvl-tools');
    const staticBtn = button('▣ Static diagrams', 'asvl-button asvl-button-secondary asvl-static-toggle');
    staticBtn.setAttribute('aria-pressed', 'false');
    const resetBtn = button('↺ Reset rehearsal', 'asvl-button asvl-button-secondary asvl-reset');
    tools.append(staticBtn, resetBtn);
    header.append(headText, tools);

    const notice = el('p', 'asvl-notice', payload.panelNotice);
    const cycle = el('ol', 'asvl-cycle');
    payload.pathwayCycle.forEach((label, index) => {
      const item = el('li', index === 0 ? 'is-current' : '', label);
      item.dataset.stage = String(index);
      cycle.append(item);
    });

    const prediction = el('section', 'asvl-prediction');
    const activity = el('section', 'asvl-activity');
    const locator = el('section', 'asvl-locator');
    const explanation = el('section', 'asvl-explanation');
    const transfer = el('section', 'asvl-transfer');
    const route = el('aside', 'asvl-route');
    route.append(
      el('h4', '', 'Teacher, assessor and access route'),
      el('p', '', 'Use the lesson’s existing teacher, TA, assessor, responsible-adult, safety and reasonable-adjustment routes. This rehearsal cannot approve a risk, permission, criterion, level, evidence state or qualification outcome.')
    );
    const live = el('div', 'asvl-live');
    live.setAttribute('aria-live', 'polite');
    live.setAttribute('aria-atomic', 'true');

    panel.append(header, notice, cycle, prediction, activity, locator, explanation, transfer, route, live);
    return panel;
  }

  function setCycle(panel, stage) {
    qsa('.asvl-cycle li', panel).forEach((item, index) => {
      item.classList.toggle('is-current', index === stage);
      item.classList.toggle('is-complete', index < stage);
      if (index === stage) item.setAttribute('aria-current', 'step');
      else item.removeAttribute('aria-current');
    });
  }

  function setFeedback(panel, message, kind = 'neutral') {
    const box = qs('.asvl-feedback', panel);
    if (!box) return;
    box.className = `asvl-feedback is-${kind}`;
    setText(box, message);
    box.hidden = !message;
    if (message) announce(panel, message);
  }

  function renderPrediction(panel, payload, state) {
    const wrap = qs('.asvl-prediction', panel);
    wrap.replaceChildren();
    const options = payload.activity.predictionOptions || [];
    if (payload.pathway === 'BUILD' || !options.length) {
      wrap.hidden = true;
      return;
    }
    wrap.hidden = false;
    const heading = el('h4', '', pathwayCopy[payload.pathway].predictionTitle);
    const prompt = el('p', 'asvl-small', 'Choose the result or factor you expect before manipulating the information. You may revise your thinking after the evidence freezes.');
    const group = el('div', 'asvl-choice-row');
    group.setAttribute('role', 'group');
    group.setAttribute('aria-label', 'Prediction choices');
    options.forEach((option, index) => {
      const choice = button(option, 'asvl-choice');
      choice.dataset.prediction = String(index);
      choice.setAttribute('aria-pressed', state.prediction === index ? 'true' : 'false');
      choice.addEventListener('click', () => {
        state.prediction = index;
        qsa('.asvl-choice', group).forEach((node, nodeIndex) => {
          node.setAttribute('aria-pressed', nodeIndex === index ? 'true' : 'false');
        });
        panel.classList.add('has-prediction');
        setCycle(panel, 1);
        setActivityLocked(panel, false);
        announce(panel, `Prediction recorded: ${option}. The activity is now available.`);
        const firstControl = qs('.asvl-activity button:not([disabled]), .asvl-activity select:not([disabled])', panel);
        safeFocus(firstControl);
      });
      group.append(choice);
    });
    wrap.append(heading, prompt, group);
  }

  function setActivityLocked(panel, locked) {
    const activity = qs('.asvl-activity', panel);
    activity.classList.toggle('is-locked', locked);
    qsa('button, select', activity).forEach(control => {
      if (control.dataset.keepEnabled === 'true') return;
      control.disabled = locked;
    });
    const lock = qs('.asvl-activity-lock', activity);
    if (lock) lock.hidden = !locked;
  }

  function commonActivityShell(panel, payload, state) {
    const wrap = qs('.asvl-activity', panel);
    wrap.replaceChildren();
    const heading = el('h4', '', 'Manipulate the information');
    const prompt = el('p', 'asvl-prompt', payload.activity.prompt);
    const lock = el('p', 'asvl-activity-lock', 'Choose a prediction first. This prevents hindsight from replacing thinking.');
    const canvas = el('div', 'asvl-canvas');
    const feedback = el('div', 'asvl-feedback');
    feedback.hidden = true;
    feedback.setAttribute('role', 'status');
    wrap.append(heading, prompt, lock, canvas, feedback);
    const locked = payload.pathway !== 'BUILD' && state.prediction === null;
    setActivityLocked(panel, locked);
    return canvas;
  }

  function completeActivity(panel, payload, state) {
    if (state.completed) return;
    state.completed = true;
    panel.classList.add('is-activity-complete');
    setCycle(panel, payload.pathway === 'LAUNCH' ? 1 : 2);
    qsa('.asvl-activity button, .asvl-activity select', panel).forEach(control => {
      if (!control.classList.contains('asvl-reset')) control.disabled = true;
    });
    setFeedback(panel, `${pathwayCopy[payload.pathway].completionLead} ${payload.activity.completion}`, 'success');
    renderLocator(panel, payload, state);
    renderExplanation(panel, payload, state);
  }

  function renderSort(panel, payload, state) {
    const canvas = commonActivityShell(panel, payload, state);
    const activity = payload.activity;
    const layout = el('div', 'asvl-sort-layout');
    const bank = el('div', 'asvl-bank');
    bank.append(el('h5', '', 'Choose one card'));
    const items = el('div', 'asvl-item-grid');
    const targets = el('div', 'asvl-target-grid');

    const chooseItem = itemId => {
      if (state.placed.has(itemId)) return;
      state.selectedItem = itemId;
      qsa('.asvl-sort-item', panel).forEach(node => {
        const selected = node.dataset.itemId === itemId;
        node.classList.toggle('is-selected', selected);
        node.setAttribute('aria-pressed', selected ? 'true' : 'false');
      });
      const item = activity.items.find(entry => entry.id === itemId);
      setFeedback(panel, `Selected: ${item.label}. Now choose a destination.`, 'neutral');
    };

    activity.items.forEach(item => {
      const card = button(`${item.icon || '◆'} ${item.label}`, 'asvl-sort-item');
      card.dataset.itemId = item.id;
      card.setAttribute('aria-pressed', 'false');
      card.draggable = true;
      card.addEventListener('click', () => chooseItem(item.id));
      card.addEventListener('dragstart', event => {
        event.dataTransfer?.setData('text/plain', item.id);
        chooseItem(item.id);
      });
      if (state.placed.has(item.id)) card.hidden = true;
      items.append(card);
    });

    activity.categories.forEach(category => {
      const target = el('div', 'asvl-sort-target');
      target.dataset.categoryId = category.id;
      const targetButton = button(`${category.icon || '◇'} ${category.label}`, 'asvl-target-button');
      targetButton.addEventListener('click', () => place(state.selectedItem, category.id));
      const placed = el('div', 'asvl-placed-list');
      placed.setAttribute('aria-label', `Cards placed under ${category.label}`);
      for (const [itemId, categoryId] of state.placed.entries()) {
        if (categoryId !== category.id) continue;
        const item = activity.items.find(entry => entry.id === itemId);
        placed.append(el('div', 'asvl-placed-card', `✓ ${item.label}`));
      }
      target.addEventListener('dragover', event => event.preventDefault());
      target.addEventListener('drop', event => {
        event.preventDefault();
        const itemId = event.dataTransfer?.getData('text/plain') || state.selectedItem;
        place(itemId, category.id);
      });
      target.append(targetButton, placed);
      targets.append(target);
    });

    function place(itemId, categoryId) {
      if (!itemId) {
        setFeedback(panel, 'Choose a card before choosing a destination.', 'prompt');
        return;
      }
      const item = activity.items.find(entry => entry.id === itemId);
      if (!item || state.placed.has(itemId)) return;
      if (item.answer !== categoryId) {
        setFeedback(panel, `Not there yet. ${item.reason}`, 'retry');
        return;
      }
      state.placed.set(itemId, categoryId);
      state.selectedItem = null;
      setFeedback(panel, `Placed correctly. ${item.reason}`, 'success');
      renderSort(panel, payload, state);
      if (state.placed.size === activity.items.length) completeActivity(panel, payload, state);
      else {
        setCycle(panel, 1);
        const next = qs('.asvl-sort-item:not([hidden])', panel);
        safeFocus(next);
      }
    }

    bank.append(items);
    layout.append(bank, targets);
    canvas.append(layout);
  }

  function renderSequence(panel, payload, state) {
    const canvas = commonActivityShell(panel, payload, state);
    const activity = payload.activity;
    const list = el('ol', 'asvl-sequence-list');
    state.sequence.forEach((stepId, index) => {
      const step = activity.steps.find(entry => entry.id === stepId);
      const row = el('li', 'asvl-sequence-row');
      const number = el('span', 'asvl-sequence-number', String(index + 1));
      const text = el('span', 'asvl-sequence-text', step.label);
      const controls = el('span', 'asvl-sequence-controls');
      const up = button('↑ Move up', 'asvl-mini-button');
      const down = button('↓ Move down', 'asvl-mini-button');
      up.setAttribute('aria-label', `Move ${step.label} up`);
      down.setAttribute('aria-label', `Move ${step.label} down`);
      up.disabled = index === 0 || (payload.pathway !== 'BUILD' && state.prediction === null);
      down.disabled = index === state.sequence.length - 1 || (payload.pathway !== 'BUILD' && state.prediction === null);
      up.addEventListener('click', () => {
        [state.sequence[index - 1], state.sequence[index]] = [state.sequence[index], state.sequence[index - 1]];
        renderSequence(panel, payload, state);
        safeFocus(qsa('.asvl-sequence-row', panel)[index - 1]?.querySelector('button'));
      });
      down.addEventListener('click', () => {
        [state.sequence[index + 1], state.sequence[index]] = [state.sequence[index], state.sequence[index + 1]];
        renderSequence(panel, payload, state);
        safeFocus(qsa('.asvl-sequence-row', panel)[index + 1]?.querySelector('button'));
      });
      controls.append(up, down);
      row.append(number, text, controls);
      list.append(row);
    });
    const check = button('Check the sequence', 'asvl-button asvl-check');
    check.addEventListener('click', () => {
      const expected = activity.steps.map(step => step.id);
      const correct = state.sequence.every((id, index) => id === expected[index]);
      if (correct) {
        qsa('.asvl-sequence-row', panel).forEach(row => row.classList.add('is-correct'));
        completeActivity(panel, payload, state);
      } else {
        const firstWrong = state.sequence.findIndex((id, index) => id !== expected[index]);
        const expectedStep = activity.steps[firstWrong];
        setFeedback(panel, `Recheck position ${firstWrong + 1}. Ask what must already be true before “${expectedStep.label}”.`, 'retry');
      }
    });
    canvas.append(list, check);
  }

  function renderEvidence(panel, payload, state) {
    const canvas = commonActivityShell(panel, payload, state);
    const activity = payload.activity;
    const grid = el('div', 'asvl-evidence-grid');
    activity.statements.forEach(statement => {
      const card = button(statement.label, 'asvl-evidence-card');
      card.dataset.statementId = statement.id;
      const selected = state.selectedEvidence.has(statement.id);
      card.setAttribute('aria-pressed', selected ? 'true' : 'false');
      card.classList.toggle('is-selected', selected);
      card.addEventListener('click', () => {
        if (state.selectedEvidence.has(statement.id)) state.selectedEvidence.delete(statement.id);
        else state.selectedEvidence.add(statement.id);
        renderEvidence(panel, payload, state);
        setFeedback(panel, `${state.selectedEvidence.size} item${state.selectedEvidence.size === 1 ? '' : 's'} selected. Check when the set is complete.`, 'neutral');
      });
      grid.append(card);
    });
    const check = button('Check the evidence set', 'asvl-button asvl-check');
    check.addEventListener('click', () => {
      const correctIds = new Set(activity.statements.filter(item => item.correct).map(item => item.id));
      const exact = correctIds.size === state.selectedEvidence.size &&
        Array.from(correctIds).every(id => state.selectedEvidence.has(id));
      qsa('.asvl-evidence-card', panel).forEach(card => {
        const statement = activity.statements.find(item => item.id === card.dataset.statementId);
        const selected = state.selectedEvidence.has(statement.id);
        card.classList.toggle('is-correct-choice', selected && statement.correct);
        card.classList.toggle('is-wrong-choice', selected && !statement.correct);
        card.classList.toggle('is-missed-choice', !selected && statement.correct);
      });
      if (exact) {
        completeActivity(panel, payload, state);
      } else {
        const selectedWrong = activity.statements.find(item => state.selectedEvidence.has(item.id) && !item.correct);
        const missed = activity.statements.find(item => !state.selectedEvidence.has(item.id) && item.correct);
        const focus = selectedWrong || missed;
        setFeedback(panel, focus ? focus.reason : 'Recheck the complete set.', 'retry');
      }
    });
    canvas.append(grid, check);
  }

  function sceneSvg(scene, label) {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 100 70');
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', `${label}. Simplified original teaching model.`);
    svg.classList.add('asvl-hotspot-svg');
    const ns = 'http://www.w3.org/2000/svg';
    const rect = (x, y, w, h, cls) => {
      const node = document.createElementNS(ns, 'rect');
      node.setAttribute('x', x); node.setAttribute('y', y); node.setAttribute('width', w); node.setAttribute('height', h);
      node.setAttribute('rx', '3'); node.setAttribute('class', cls);
      return node;
    };
    const path = document.createElementNS(ns, 'path');
    path.setAttribute('d', scene === 'room'
      ? 'M8 58 H92 M12 58 V18 H88 V58 M35 18 V58 M64 18 V58'
      : scene === 'workplace'
        ? 'M6 58 H94 M12 58 V26 L28 14 L44 26 V58 M55 58 V20 H86 V58'
        : 'M5 60 C24 44 34 62 50 49 C64 38 76 46 95 28');
    path.setAttribute('class', 'asvl-scene-line');
    svg.append(path);
    svg.append(rect(10, 10, 22, 14, 'asvl-scene-shape'));
    svg.append(rect(39, 23, 22, 14, 'asvl-scene-shape'));
    svg.append(rect(68, 10, 22, 14, 'asvl-scene-shape'));
    svg.append(rect(17, 45, 22, 14, 'asvl-scene-shape'));
    svg.append(rect(62, 43, 22, 14, 'asvl-scene-shape'));
    return svg;
  }

  function renderHotspot(panel, payload, state) {
    const canvas = commonActivityShell(panel, payload, state);
    const activity = payload.activity;
    const scene = el('div', 'asvl-hotspot-scene');
    scene.append(sceneSvg(activity.scene || 'map', payload.title));
    activity.hotspots.forEach((spot, index) => {
      const spotButton = button(String(index + 1), 'asvl-hotspot-button');
      spotButton.style.left = `${spot.x}%`;
      spotButton.style.top = `${spot.y}%`;
      spotButton.setAttribute('aria-label', `Open hotspot ${index + 1}: ${spot.label}`);
      const opened = state.openedHotspots.has(spot.id);
      spotButton.classList.toggle('is-open', opened);
      spotButton.setAttribute('aria-pressed', opened ? 'true' : 'false');
      spotButton.addEventListener('click', () => {
        state.openedHotspots.add(spot.id);
        renderHotspot(panel, payload, state);
        setFeedback(panel, `${spot.label}. ${spot.note}`, 'success');
        if (state.openedHotspots.size === activity.hotspots.length) completeActivity(panel, payload, state);
      });
      scene.append(spotButton);
    });
    const notes = el('div', 'asvl-hotspot-notes');
    activity.hotspots.forEach((spot, index) => {
      if (!state.openedHotspots.has(spot.id)) return;
      const note = el('article', 'asvl-hotspot-note');
      note.append(el('strong', '', `${index + 1}. ${spot.label}`), el('p', '', spot.note));
      notes.append(note);
    });
    canvas.append(scene, notes);
  }

  function findOutcome(activity, score) {
    return activity.outcomes.find(outcome => score >= outcome.min && score <= outcome.max)
      || activity.outcomes[activity.outcomes.length - 1];
  }

  function renderModel(panel, payload, state) {
    const canvas = commonActivityShell(panel, payload, state);
    const activity = payload.activity;
    const form = el('div', 'asvl-model');
    const controlsWrap = el('div', 'asvl-model-controls');
    activity.controls.forEach(control => {
      const label = el('label', 'asvl-model-control');
      label.append(el('span', '', control.label));
      const select = el('select', '');
      select.dataset.controlId = control.id;
      control.options.forEach(option => {
        const optionNode = el('option', '', option.label);
        optionNode.value = option.value;
        select.append(optionNode);
      });
      const last = state.runs[state.runs.length - 1];
      select.value = last?.values?.[control.id] ?? control.default ?? control.options[0].value;
      label.append(select);
      controlsWrap.append(label);
    });

    const run = button(state.runs.length ? 'Run one controlled change' : 'Run and freeze the result', 'asvl-button asvl-run');
    run.addEventListener('click', () => {
      const values = {};
      let score = 0;
      const feedback = [];
      activity.controls.forEach(control => {
        const value = qs(`select[data-control-id="${CSS.escape(control.id)}"]`, panel)?.value;
        values[control.id] = value;
        const option = control.options.find(item => item.value === value) || control.options[0];
        score += Number(option.quality || 0);
        feedback.push(`${control.label}: ${option.feedback}`);
      });
      if (state.runs.length && activity.requiredRuns > 1) {
        const previous = state.runs[state.runs.length - 1].values;
        const changed = Object.keys(values).filter(key => values[key] !== previous[key]);
        if (changed.length !== 1) {
          setFeedback(panel, `Change exactly one variable between frozen runs. You changed ${changed.length}.`, 'retry');
          return;
        }
      }
      const outcome = findOutcome(activity, score);
      state.runs.push({ values, score, outcome, feedback });
      setCycle(panel, 2);
      setFeedback(panel, `Frozen result ${state.runs.length}: ${outcome.label}. ${outcome.message}`, 'success');
      renderModel(panel, payload, state);
      if (state.runs.length >= activity.requiredRuns) completeActivity(panel, payload, state);
    });

    const history = el('div', 'asvl-run-history');
    state.runs.forEach((record, index) => {
      const card = el('article', 'asvl-run-card');
      card.append(
        el('h5', '', `Frozen run ${index + 1} · ${record.outcome.label}`),
        el('p', '', record.outcome.message)
      );
      const list = el('ul', '');
      record.feedback.forEach(line => list.append(el('li', '', line)));
      card.append(list);
      history.append(card);
    });

    const runRule = el('p', 'asvl-small', activity.requiredRuns > 1
      ? `Complete ${activity.requiredRuns} frozen runs. After the first, change exactly one variable so the comparison is fair.`
      : 'Complete one frozen run, then transfer the structure to the real task.');
    form.append(runRule, controlsWrap, run, history);
    canvas.append(form);
  }

  function renderActivity(panel, payload, state) {
    const renderers = {
      sort: renderSort,
      sequence: renderSequence,
      evidence: renderEvidence,
      hotspot: renderHotspot,
      model: renderModel
    };
    const renderer = renderers[payload.activity.type];
    if (!renderer) {
      const canvas = commonActivityShell(panel, payload, state);
      canvas.append(el('p', 'asvl-error', `Unsupported activity type: ${payload.activity.type}`));
      return;
    }
    renderer(panel, payload, state);
  }

  function locatorComplete(state) {
    return Boolean(state.locator.evidenceForm && state.locator.location && state.locator.route);
  }

  function renderLocator(panel, payload, state) {
    const wrap = qs('.asvl-locator', panel);
    wrap.replaceChildren();
    if (payload.pathway !== 'LAUNCH') {
      wrap.hidden = true;
      return;
    }
    wrap.hidden = false;
    wrap.classList.toggle('is-locked', !state.completed);
    wrap.append(
      el('h4', '', 'Structured evidence locator · not an evidence judgement'),
      el('p', 'asvl-small', 'After the real task, select where authentic evidence could be found and the authorised next route. Do not upload anything here. “Not yet” is an honest option.')
    );
    const groups = [
      ['evidenceForm', 'What exists?', payload.locator.evidenceForms],
      ['location', 'Where is it?', payload.locator.locations],
      ['route', 'What is the next authorised route?', payload.locator.routes]
    ];
    groups.forEach(([key, legendText, options]) => {
      const fieldset = el('fieldset', 'asvl-locator-group');
      const legend = el('legend', '', legendText);
      fieldset.append(legend);
      options.forEach(option => {
        const label = el('label', 'asvl-radio-card');
        const input = el('input', '');
        input.type = 'radio';
        input.name = `${payload.slug}-${key}`;
        input.value = option.id;
        input.checked = state.locator[key] === option.id;
        input.disabled = !state.completed;
        input.addEventListener('change', () => {
          state.locator[key] = option.id;
          renderLocator(panel, payload, state);
          renderExplanation(panel, payload, state);
          if (locatorComplete(state)) {
            announce(panel, 'The structured evidence locator is complete. The explanation is now available.');
            safeFocus(qs('.asvl-open-explanation:not([disabled])', panel));
          }
        });
        label.append(input, el('span', '', option.label));
        fieldset.append(label);
      });
      wrap.append(fieldset);
    });
    const caution = el('p', 'asvl-caution', 'This locator records no evidence state. It cannot mark work achieved, verified, moderated, certified or returned. Those are authorised human and awarding-body processes.');
    wrap.append(caution);
  }

  function canOpenExplanation(payload, state) {
    return state.completed && (payload.pathway !== 'LAUNCH' || locatorComplete(state));
  }

  function renderExplanation(panel, payload, state) {
    const wrap = qs('.asvl-explanation', panel);
    wrap.replaceChildren();
    const allowed = canOpenExplanation(payload, state);
    const heading = el('h4', '', payload.pathway === 'LAUNCH' ? 'Reason from the evidence' : 'Name the learning');
    const status = el('p', 'asvl-small', allowed
      ? 'The rehearsal conditions are complete. Open the explanation, then transfer it to the real task.'
      : payload.pathway === 'LAUNCH'
        ? 'Complete the investigation and all three structured locator choices. Activity completion alone does not unlock the explanation.'
        : 'Complete the manipulation before opening the explanation.');
    const open = button(state.explanationOpen ? '✓ Explanation opened' : 'Open explanation', 'asvl-button asvl-open-explanation');
    open.disabled = !allowed || state.explanationOpen;
    open.addEventListener('click', () => {
      state.explanationOpen = true;
      const openedBy = payload.pathway === 'LAUNCH'
        ? 'completed activity and selected structured evidence-locator route'
        : 'completed classroom rehearsal';
      panel.dataset.asdanOpenedBy = openedBy;
      setCycle(panel, 2);
      renderExplanation(panel, payload, state);
      announce(panel, payload.activity.completion);
      safeFocus(qs('.asvl-explanation-body', panel));
    });
    wrap.append(heading, status, open);
    if (state.explanationOpen) {
      const body = el('div', 'asvl-explanation-body');
      body.tabIndex = -1;
      body.append(
        el('p', 'asvl-completion', payload.activity.completion),
        el('p', 'asvl-prediction-review', state.prediction !== null && payload.activity.predictionOptions
          ? `Your prediction was: ${payload.activity.predictionOptions[state.prediction]}. Compare it with the frozen evidence; changing your mind is evidence of thinking, not failure.`
          : 'Point to the part of the frozen visual that supports the explanation.')
      );
      const transferBtn = button('Begin the independent task', 'asvl-button asvl-transfer-button');
      transferBtn.addEventListener('click', () => {
        state.transferOpen = true;
        setCycle(panel, 3);
        renderTransfer(panel, payload, state);
        panel.classList.add('is-transfer-mode');
        safeFocus(qs('.asvl-transfer', panel));
      });
      body.append(transferBtn);
      wrap.append(body);
    }
  }

  function renderTransfer(panel, payload, state) {
    const wrap = qs('.asvl-transfer', panel);
    wrap.replaceChildren();
    wrap.hidden = !state.transferOpen;
    if (!state.transferOpen) return;
    wrap.tabIndex = -1;
    wrap.append(
      el('p', 'asvl-eyebrow', 'INDEPENDENT HANDOVER'),
      el('h4', '', 'Use the rehearsal, then close the distance yourself'),
      el('p', 'asvl-independent-task', payload.independent)
    );
    const steps = el('ol', 'asvl-independence-steps');
    payload.independenceSteps.forEach(step => steps.append(el('li', '', step)));
    const checks = el('div', 'asvl-success-checks');
    checks.append(el('h5', '', 'Stop-and-check conditions'));
    const checkList = el('ul', '');
    payload.successChecks.forEach(check => checkList.append(el('li', '', check)));
    checks.append(checkList);
    const help = el('details', 'asvl-help-ladder');
    const summary = el('summary', '', 'Help ladder · use the least help that works');
    const helpList = el('ol', '');
    payload.helpLadder.forEach(step => helpList.append(el('li', '', step)));
    help.append(summary, helpList);
    const back = button('Return to the frozen rehearsal', 'asvl-button asvl-button-secondary');
    back.addEventListener('click', () => {
      state.transferOpen = false;
      panel.classList.remove('is-transfer-mode');
      setCycle(panel, 2);
      renderTransfer(panel, payload, state);
      safeFocus(qs('.asvl-transfer-button', panel));
    });
    wrap.append(steps, checks, help, back);
  }

  function resetPanel(panel, payload, stateRef) {
    const replacement = createState(payload);
    Object.keys(stateRef).forEach(key => delete stateRef[key]);
    Object.assign(stateRef, replacement);
    panel.classList.remove('has-prediction', 'is-activity-complete', 'is-transfer-mode', 'asvl-static');
    /* Reset clears the user's override, never the machine's preference. */
    panel.classList.toggle('asvl-static', prefersReducedMotion());
    delete panel.dataset.asdanOpenedBy;
    setCycle(panel, 0);
    renderPrediction(panel, payload, stateRef);
    renderActivity(panel, payload, stateRef);
    renderLocator(panel, payload, stateRef);
    renderExplanation(panel, payload, stateRef);
    renderTransfer(panel, payload, stateRef);
    announce(panel, 'Rehearsal reset. No data was stored.');
  }

  function mountPayload(payload, target) {
    if (!payload || !payload.slug) throw new Error('A valid ASDAN visual-learning payload is required.');
    const host = target || targetForPayload(payload);
    if (!host) throw new Error(`No mount target found for ${payload.slug}.`);
    const previous = qs(`[data-asdan-visual-learning="${CSS.escape(payload.slug)}"]`, host);
    if (previous) return previous;

    const panel = createPanel(payload);
    const state = createState(payload);
    host.append(panel);
    if (!host.classList.contains('slide')) panel.classList.add('asvl-standalone');

    const staticBtn = qs('.asvl-static-toggle', panel);
    /* Effective state is the user's choice OR the OS preference. The OS is a floor,
       not a default: if the machine asks for reduced motion, the button cannot turn
       movement back on, because the CSS rule would suppress it anyway and the
       control would then be lying about what the pupil sees. */
    const staticIsOn = () => state.staticMode || prefersReducedMotion();
    const paintStatic = () => {
      const on = staticIsOn();
      panel.classList.toggle('asvl-static', on);
      staticBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
      staticBtn.textContent = on ? '✓ Static diagrams' : '▣ Static diagrams';
      staticBtn.disabled = prefersReducedMotion();
    };
    paintStatic();
    motionSubscribers.add(paintStatic);
    staticBtn.addEventListener('click', () => {
      if (prefersReducedMotion()) return;
      state.staticMode = !state.staticMode;
      paintStatic();
      announce(panel, state.staticMode ? 'Static diagrams enabled.' : 'Finite teaching movement enabled.');
    });
    qs('.asvl-reset', panel).addEventListener('click', () => resetPanel(panel, payload, state));

    renderPrediction(panel, payload, state);
    renderActivity(panel, payload, state);
    renderLocator(panel, payload, state);
    renderExplanation(panel, payload, state);
    renderTransfer(panel, payload, state);
    setCycle(panel, 0);

    panel.__asdanVisualState = state;
    panel.__asdanVisualPayload = payload;
    panel.dataset.asdanVisualReady = 'true';
    return panel;
  }

  function autoMount() {
    const registry = window.ASDANVisualPayloads || {};
    const slug = slugFromLocation();
    const payload = registry[slug];
    if (!payload) return null;
    return mountPayload(payload, targetForPayload(payload));
  }

  const api = {
    version: '1.0.0',
    mountPayload,
    autoMount,
    slugFromLocation,
    targetForPayload,
    getState(panel) { return panel?.__asdanVisualState || null; }
  };
  window[API_NAME] = api;

  const start = () => {
    try { autoMount(); }
    catch (error) {
      console.error('ASDAN Visual Learning did not mount:', error);
      document.documentElement.dataset.asdanVisualError = 'true';
    }
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
  else start();
})();
/* ASDAN-VISUAL-LEARNING:JS:END v1 */
