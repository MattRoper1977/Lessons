(() => {
  'use strict';

  const root = document.documentElement;
  if (root.dataset.visualUpgrade === 'ready' || root.dataset.visualUpgrade === 'loading') return;
  root.dataset.visualUpgrade = 'loading';

  const reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const motionTimers = new WeakMap();
  let liveRegion;
  let announceTimer;

  const nativeInteractive = (element) =>
    /^(A|BUTTON|INPUT|SELECT|TEXTAREA|SUMMARY)$/.test(element.tagName);

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

  function syncInteractiveState(element) {
    if (!(element instanceof Element)) return;

    if (element.matches('.match-pill, .pres-card, .hint-btn, .wagoll-trigger, .v5-step-controls button')) {
      const pressed = element.classList.contains('selected') ||
        element.classList.contains('done') ||
        element.classList.contains('active') ||
        element.getAttribute('aria-expanded') === 'true';
      element.setAttribute('aria-pressed', String(pressed));
    }

    if (element.matches('.answer')) {
      const visible = getComputedStyle(element).display !== 'none';
      element.setAttribute('aria-hidden', String(!visible));
    }

    if (element.matches('.hint-box, .wagoll-panel, .v5-step')) {
      const visible = element.classList.contains('show') ||
        element.classList.contains('visible') ||
        element.classList.contains('revealed');
      element.setAttribute('aria-hidden', String(!visible));
    }

    if (element.matches('.match-target.correct')) element.dataset.vuState = 'correct';
    else if (element.matches('.match-target.wrong')) element.dataset.vuState = 'incorrect';
    else if (element.matches('.match-target')) delete element.dataset.vuState;
  }

  function enhanceInteractive(scope = document) {
    const selector = [
      'button',
      'a[href]',
      '.match-pill',
      '.match-target',
      '.pres-card',
      '.hl-sentence',
      '.fact-dot',
      '[onclick]'
    ].join(',');

    scope.querySelectorAll(selector).forEach((element) => {
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
    }, 6500));
  }

  function syncSlides({ announceCurrent = false } = {}) {
    const slides = Array.from(document.querySelectorAll('.slide'));
    slides.forEach((slide, index) => {
      const active = slide.classList.contains('active');
      slide.setAttribute('aria-hidden', String(!active));
      slide.dataset.vuIndex = String(index + 1);
      prepareReveal(slide);
      if (active) {
        slide.classList.remove('vu-ready');
        requestAnimationFrame(() => slide.classList.add('vu-ready'));
        settleMotion(slide);
        if (announceCurrent) {
          const title = slide.getAttribute('data-title') || slide.querySelector('h1,h2')?.textContent?.trim() || `Slide ${index + 1}`;
          announce(`${title}. Slide ${index + 1} of ${slides.length}.`);
        }
      }
    });

    const progress = document.getElementById('progressLabel');
    if (progress) {
      progress.setAttribute('role', 'status');
      progress.setAttribute('aria-live', 'polite');
    }
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
      let slidesChanged = false;
      for (const mutation of mutations) {
        if (mutation.type === 'attributes') {
          const element = mutation.target;
          syncInteractiveState(element);
          if (element.classList?.contains('slide')) slidesChanged = true;
        }
        mutation.addedNodes.forEach((node) => {
          if (!(node instanceof Element)) return;
          enhanceInteractive(node);
          syncInteractiveState(node);
        });
      }
      if (slidesChanged) syncSlides({ announceCurrent: true });
    });

    observer.observe(document.body, {
      subtree: true,
      childList: true,
      attributes: true,
      attributeFilter: ['class', 'aria-expanded', 'hidden']
    });
  }

  function init() {
    if (!document.body || root.dataset.visualUpgrade === 'ready') return;
    createLiveRegion();
    enhanceInteractive();
    syncSlides();
    installObservers();
    document.addEventListener('click', (event) => {
      window.setTimeout(() => {
        enhanceInteractive();
        document.querySelectorAll('.answer, .hint-box, .wagoll-panel, .v5-step, .match-target').forEach(syncInteractiveState);
        describeInteraction(event.target);
      }, 0);
    }, true);
    root.dataset.visualUpgrade = 'ready';
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
