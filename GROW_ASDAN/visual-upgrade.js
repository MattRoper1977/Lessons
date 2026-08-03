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
