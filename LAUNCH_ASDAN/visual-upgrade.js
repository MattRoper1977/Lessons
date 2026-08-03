(() => {
  'use strict';

  const root = document.documentElement;
  if (root.dataset.visualUpgrade === 'ready' || root.dataset.visualUpgrade === 'loading') return;
  root.dataset.visualUpgrade = 'loading';

  const reducedMotion = Boolean(window.matchMedia?.('(prefers-reduced-motion: reduce)').matches);
  const motionTimers = new WeakMap();
  const revealTimers = new WeakMap();
  let liveRegion;
  let announceTimer;
  let activeSlide = null;
  let slideSyncQueued = false;

  const nativeInteractive = (element) =>
    /^(A|BUTTON|INPUT|SELECT|TEXTAREA|SUMMARY)$/.test(element.tagName);

  const interactiveSelector = [
    'button',
    'a[href]',
    '.match-pill',
    '.match-target',
    '.pres-card',
    '.hl-sentence',
    '.fact-dot',
    '.vu-checkpoint',
    '[onclick]:not(.slide):not(.midpoint-overlay):not(.v4-modal-overlay):not(.lesson-complete-overlay)'
  ].join(',');

  function announce(message) {
    if (!message || !liveRegion) return;
    window.clearTimeout(announceTimer);
    liveRegion.textContent = '';
    announceTimer = window.setTimeout(() => {
      liveRegion.textContent = message;
    }, 30);
  }

  function createLiveRegion() {
    liveRegion = document.getElementById('vu-live-region');
    if (liveRegion) return;
    liveRegion = document.createElement('div');
    liveRegion.id = 'vu-live-region';
    liveRegion.className = 'vu-live-region';
    liveRegion.setAttribute('role', 'status');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    document.body.appendChild(liveRegion);
  }

  function elementsWithin(scope, selector) {
    const elements = [];
    if (scope instanceof Element && scope.matches(selector)) elements.push(scope);
    if (scope?.querySelectorAll) elements.push(...scope.querySelectorAll(selector));
    return elements;
  }

  function makeKeyboardOperable(element) {
    if (!element || element.dataset.vuKeyboard === 'true' || nativeInteractive(element)) return;
    element.dataset.vuKeyboard = 'true';
    if (!element.hasAttribute('role')) element.setAttribute('role', 'button');
    if (!element.hasAttribute('tabindex')) element.setAttribute('tabindex', '0');
    element.addEventListener('keydown', (event) => {
      if (event.key !== 'Enter' && event.key !== ' ') return;
      event.preventDefault();
      element.click();
    });
  }

  function isDisplayed(element) {
    return Boolean(element && getComputedStyle(element).display !== 'none' && !element.hidden);
  }

  function syncInteractiveState(element) {
    if (!(element instanceof Element)) return;

    if (element.matches('.match-pill, .pres-card, .hl-sentence, .vu-checkpoint')) {
      const pressed = element.classList.contains('selected') ||
        element.classList.contains('done') ||
        element.classList.contains('highlighted') ||
        element.dataset.vuComplete === 'true';
      element.setAttribute('aria-pressed', String(pressed));
    }

    if (element.matches('.hint-btn')) {
      element.setAttribute('aria-expanded', String(Boolean(element.nextElementSibling?.classList.contains('show'))));
    }

    if (element.matches('.wagoll-trigger')) {
      const panel = document.getElementById('wagoll-panel') || element.nextElementSibling;
      element.setAttribute('aria-expanded', String(Boolean(panel?.classList.contains('visible'))));
    }

    if (element.matches('.answer')) {
      element.setAttribute('aria-hidden', String(!isDisplayed(element)));
    }

    if (element.matches('.hint-box, .wagoll-panel, .v5-step')) {
      const visible = element.classList.contains('show') ||
        element.classList.contains('visible') ||
        element.classList.contains('revealed');
      element.setAttribute('aria-hidden', String(!visible));
    }

    if (element.matches('.match-target')) {
      if (element.classList.contains('correct')) {
        element.dataset.vuState = 'correct';
        element.setAttribute('aria-invalid', 'false');
      } else if (element.classList.contains('wrong')) {
        element.dataset.vuState = 'incorrect';
        element.setAttribute('aria-invalid', 'true');
      } else {
        delete element.dataset.vuState;
        element.removeAttribute('aria-invalid');
      }
    }

    if (element.matches('.fact-dot')) {
      if (element.classList.contains('active')) element.setAttribute('aria-current', 'step');
      else element.removeAttribute('aria-current');
    }
  }

  function enhanceInteractive(scope = document) {
    elementsWithin(scope, interactiveSelector).forEach((element) => {
      makeKeyboardOperable(element);
      if (!element.getAttribute('aria-label') && element.getAttribute('title') && !element.textContent.trim()) {
        element.setAttribute('aria-label', element.getAttribute('title'));
      }
      syncInteractiveState(element);
    });
  }

  function prepareReveal(slide) {
    const selectors = [
      '.slide-tag',
      'h1',
      'h2',
      '.li-box',
      '.ido-box',
      '.task-box',
      '.wedo-capture',
      '.scaffold-box',
      '.aspire-box',
      '.sc-box',
      '.ilm',
      '.content-grid > *',
      '.arrival-grid > *',
      '.compare-grid-3 > *',
      '.lundy-grid > *'
    ].join(',');

    let order = 0;
    slide.querySelectorAll(selectors).forEach((element) => {
      if (element.closest('.slide') !== slide || element.classList.contains('vu-reveal')) return;
      element.classList.add('vu-reveal');
      element.style.setProperty('--vu-order', String(Math.min(order++, 8)));
    });
  }

  function restartPurposefulMotion(slide) {
    if (reducedMotion || !slide) return;
    window.requestAnimationFrame(() => {
      slide.querySelectorAll('.ilm .pop, .ilm .draw, .ilm .rise, .ilm .fill, .ilm .glow, .ilm .spin, .ilm .hand, .ilm .ride, .ilm .rip, .ilm .sweep').forEach((element) => {
        element.getAnimations().forEach((animation) => {
          try {
            animation.cancel();
            animation.play();
          } catch (_) {
            // CSS animation control is progressive enhancement; leave the original animation intact.
          }
        });
      });
    });
  }

  function settleMotion(slide) {
    const previous = motionTimers.get(slide);
    if (previous) window.clearTimeout(previous);
    slide.classList.remove('vu-motion-settled');
    if (reducedMotion) {
      slide.classList.add('vu-motion-settled');
      return;
    }
    motionTimers.set(slide, window.setTimeout(() => {
      slide.classList.add('vu-motion-settled');
    }, 6200));
  }

  function slideTitle(slide, index) {
    return slide.getAttribute('data-title') || slide.querySelector('h1,h2')?.textContent?.trim() || `Slide ${index + 1}`;
  }

  function activateSlide(slide, slides, announceCurrent) {
    if (!slide || activeSlide === slide) return;

    if (activeSlide) {
      window.clearTimeout(revealTimers.get(activeSlide));
      window.clearTimeout(motionTimers.get(activeSlide));
      activeSlide.classList.remove('vu-entering', 'vu-ready');
    }

    activeSlide = slide;
    slide.classList.remove('vu-ready', 'vu-motion-settled');
    slide.classList.add('vu-entering');

    window.requestAnimationFrame(() => {
      window.requestAnimationFrame(() => {
        if (activeSlide !== slide) return;
        slide.classList.add('vu-ready');
        restartPurposefulMotion(slide);
      });
    });

    revealTimers.set(slide, window.setTimeout(() => {
      slide.classList.remove('vu-entering');
    }, reducedMotion ? 0 : 1250));

    settleMotion(slide);

    if (announceCurrent) {
      const index = slides.indexOf(slide);
      announce(`${slideTitle(slide, index)}. Slide ${index + 1} of ${slides.length}.`);
    }
  }

  function isWeDoSlide(slide) {
    const label = `${slide.getAttribute('data-title') || ''} ${slide.querySelector('.slide-tag')?.textContent || ''}`;
    return slide.getAttribute('data-type') === 'wedo' || /\bwe do\b/i.test(label);
  }

  function findProgressGroup(slide) {
    const groups = [
      { selector: '.match-target', done: (element) => element.classList.contains('correct') },
      { selector: '.pres-card', done: (element) => element.classList.contains('done') },
      { selector: '.hl-sentence', done: (element) => element.classList.contains('highlighted') },
      { selector: '.v5-step', done: (element) => element.classList.contains('revealed') }
    ];
    for (const group of groups) {
      const elements = Array.from(slide.querySelectorAll(group.selector));
      if (elements.length >= 2) return { ...group, elements };
    }
    return null;
  }

  function checkpointCandidates(slide) {
    const selectors = [
      '.wedo-capture > .task-box',
      '.wedo-capture > .ido-box',
      '.wedo-capture > .compare-card',
      '.wedo-capture > .react-q',
      '.content-grid > .task-box',
      '.compare-grid-3 > .compare-card',
      '.react-panel > .react-q',
      '.wedo-capture > li',
      '.wedo-capture ul > li',
      '.wedo-capture ol > li'
    ].join(',');

    return Array.from(slide.querySelectorAll(selectors)).filter((element, index, all) => {
      if (element.closest('.slide') !== slide || all.indexOf(element) !== index) return false;
      if (element.matches(interactiveSelector) || element.querySelector(interactiveSelector)) return false;
      return isDisplayed(element);
    }).slice(0, 8);
  }

  function createWeDoMeter(slide, source, total) {
    const meter = document.createElement('div');
    meter.className = 'vu-we-do-meter';
    meter.dataset.vuSource = source;
    meter.setAttribute('role', 'progressbar');
    meter.setAttribute('aria-label', 'Class activity progress');
    meter.setAttribute('aria-valuemin', '0');
    meter.setAttribute('aria-valuemax', String(total));
    meter.setAttribute('aria-valuenow', '0');
    meter.innerHTML = '<span class="vu-we-do-meter__fill" aria-hidden="true"></span>';
    const anchor = slide.querySelector('.slide-tag');
    if (anchor) anchor.insertAdjacentElement('afterend', meter);
    else slide.prepend(meter);
    return meter;
  }

  function refreshWeDoState(slide, shouldAnnounce = false) {
    if (!slide?.dataset.vuWeDo) return;
    const meter = slide.querySelector('.vu-we-do-meter');
    if (!meter) return;

    let elements = [];
    let completed = 0;
    const source = meter.dataset.vuSource;

    if (source === 'checkpoints') {
      elements = Array.from(slide.querySelectorAll('.vu-checkpoint'));
      completed = elements.filter((element) => element.dataset.vuComplete === 'true').length;
    } else {
      elements = Array.from(slide.querySelectorAll(source));
      if (source === '.match-target') completed = elements.filter((element) => element.classList.contains('correct')).length;
      else if (source === '.pres-card') completed = elements.filter((element) => element.classList.contains('done')).length;
      else if (source === '.hl-sentence') completed = elements.filter((element) => element.classList.contains('highlighted')).length;
      else if (source === '.v5-step') completed = elements.filter((element) => element.classList.contains('revealed')).length;
    }

    const total = elements.length;
    const percentage = total ? Math.round((completed / total) * 100) : 0;
    meter.style.setProperty('--vu-progress', `${percentage}%`);
    meter.setAttribute('aria-valuemax', String(total));
    meter.setAttribute('aria-valuenow', String(completed));

    const complete = total > 0 && completed === total;
    if (slide.classList.contains('vu-activity-complete') !== complete) {
      slide.classList.toggle('vu-activity-complete', complete);
    }

    if (shouldAnnounce) {
      announce(complete ? 'Class activity complete.' : `${completed} of ${total} activity points complete.`);
    }
  }

  function enhanceWeDoSlide(slide) {
    if (!isWeDoSlide(slide) || slide.dataset.vuWeDo === 'true') return;
    slide.dataset.vuWeDo = 'true';

    const progressGroup = findProgressGroup(slide);
    if (progressGroup) {
      createWeDoMeter(slide, progressGroup.selector, progressGroup.elements.length);
      progressGroup.elements.forEach((element) => syncInteractiveState(element));
      refreshWeDoState(slide);
      return;
    }

    const candidates = checkpointCandidates(slide);
    if (candidates.length < 2) return;

    candidates.forEach((element, index) => {
      element.classList.add('vu-checkpoint');
      element.dataset.vuCheckpoint = String(index + 1);
      element.dataset.vuComplete = 'false';
      element.setAttribute('aria-pressed', 'false');
      makeKeyboardOperable(element);
      element.addEventListener('click', (event) => {
        if (event.target.closest('button, a, input, select, textarea')) return;
        const next = element.dataset.vuComplete !== 'true';
        element.dataset.vuComplete = String(next);
        element.setAttribute('aria-pressed', String(next));
        refreshWeDoState(slide, true);
      });
    });

    createWeDoMeter(slide, 'checkpoints', candidates.length);
    refreshWeDoState(slide);
  }

  function syncSlides({ announceCurrent = false } = {}) {
    const slides = Array.from(document.querySelectorAll('.slide'));
    let current = null;

    slides.forEach((slide) => {
      const active = slide.classList.contains('active');
      if (active && !current) current = slide;
      const hidden = String(!active);
      if (slide.getAttribute('aria-hidden') !== hidden) slide.setAttribute('aria-hidden', hidden);
      prepareReveal(slide);
      enhanceWeDoSlide(slide);
    });

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

  function describeInteraction(target) {
    if (!(target instanceof Element)) return;
    const matchTarget = target.closest('.match-target');
    if (matchTarget?.classList.contains('correct')) announce('Correct selection confirmed.');
    else if (matchTarget?.classList.contains('wrong')) announce('That selection is not correct yet. Try again.');
    else if (target.closest('.v5-step-controls')) announce('Next teaching step revealed.');
    else if (target.closest('.hint-btn')) {
      const box = target.closest('.hint-btn')?.nextElementSibling;
      announce(box?.classList.contains('show') ? 'Hint shown.' : 'Hint hidden.');
    } else if (target.closest('.wagoll-trigger')) announce('Model example shown.');
  }

  function installObservers() {
    const observer = new MutationObserver((mutations) => {
      let activeChanged = false;
      const affectedWeDoSlides = new Set();

      for (const mutation of mutations) {
        if (mutation.type === 'attributes') {
          const element = mutation.target;
          syncInteractiveState(element);

          if (element.classList?.contains('slide') && mutation.attributeName === 'class') {
            const previousClasses = new Set((mutation.oldValue || '').split(/\s+/).filter(Boolean));
            const wasActive = previousClasses.has('active');
            const isActive = element.classList.contains('active');
            if (wasActive !== isActive) activeChanged = true;
          }

          const weDoSlide = element.closest?.('.slide[data-vu-we-do="true"]');
          if (weDoSlide) affectedWeDoSlides.add(weDoSlide);
        }

        mutation.addedNodes.forEach((node) => {
          if (!(node instanceof Element)) return;
          enhanceInteractive(node);
          syncInteractiveState(node);
          elementsWithin(node, '.slide').forEach(enhanceWeDoSlide);
        });
      }

      affectedWeDoSlides.forEach((slide) => refreshWeDoState(slide));
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

  function init() {
    if (!document.body || root.dataset.visualUpgrade === 'ready') return;
    createLiveRegion();
    enhanceInteractive();
    root.dataset.visualUpgrade = 'ready';
    syncSlides();
    installObservers();

    document.addEventListener('click', (event) => {
      window.setTimeout(() => {
        enhanceInteractive();
        document.querySelectorAll('.answer, .hint-box, .wagoll-panel, .v5-step, .match-target, .match-pill, .pres-card, .hl-sentence, .fact-dot').forEach(syncInteractiveState);
        const weDoSlide = event.target.closest?.('.slide[data-vu-we-do="true"]');
        if (weDoSlide) refreshWeDoState(weDoSlide);
        describeInteraction(event.target);
      }, 0);
    }, true);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
