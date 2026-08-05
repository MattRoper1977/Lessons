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
window.ASDANVisualPayloads = Object.assign(window.ASDANVisualPayloads || {}, {"ENT_W1_Helps_And_Earns":{"path":"GROW_ASDAN/Enterprise/ENT_W1_Helps_And_Earns.html","pathway":"GROW","subsection":"Enterprise","lessonTitle":"Week 1 · Helps and Earns","targetTitle":"We Do 1","title":"Enterprise value-flow sorter","purpose":"Prevent ‘helps and earns’ from becoming a vague slogan by separating linked but distinct functions.","activity":{"type":"sort","prompt":"Predict which example will be hardest to classify. Sort each statement by whether it describes customer value, income, cost or social benefit.","categories":[{"id":"value","icon":"🎯","label":"VALUE TO USER"},{"id":"income","icon":"➕","label":"MONEY IN"},{"id":"cost","icon":"➖","label":"COST / RESOURCE"},{"id":"benefit","icon":"🌱","label":"SOCIAL BENEFIT"}],"items":[{"id":"i1","icon":"🎯","label":"The product saves the user time when completing a routine.","answer":"value","reason":"It explains why the user might choose it."},{"id":"i2","icon":"➕","label":"£3 is received for one fictional sale.","answer":"income","reason":"Money enters the enterprise."},{"id":"i3","icon":"➖","label":"Materials cost £1.20 per item.","answer":"cost","reason":"The resource has a financial cost."},{"id":"i4","icon":"🌱","label":"Surplus supports a named local activity.","answer":"benefit","reason":"The enterprise has a bounded social purpose."},{"id":"i5","icon":"🎯","label":"The service offers a clearer accessible instruction route.","answer":"value","reason":"The user receives a practical benefit."},{"id":"i6","icon":"➖","label":"Venue or travel is required for delivery.","answer":"cost","reason":"Resources include more than materials."},{"id":"i7","icon":"➕","label":"A grant or agreed contribution funds the activity.","answer":"income","reason":"It is a possible source of funds, subject to the real scheme."},{"id":"i8","icon":"🌱","label":"Participants gain a specific opportunity agreed with them.","answer":"benefit","reason":"The intended social change is named and user-centred."}],"completion":"Enterprise decisions keep four different questions visible: what the user gains, what comes in, what it costs and what social benefit is intended.","predictionOptions":["Value and social benefit will overlap most","Income and social benefit will overlap most","Cost and value will overlap most"]},"independent":"Analyse one supplied enterprise example using the four headings, then add one missing question.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original four-channel enterprise flow from user value and resources to income and social benefit.","mediaKey":"enterprise","slug":"ENT_W1_Helps_And_Earns","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["PREDICT","TEST","COMPARE","JUSTIFY"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"fbf97f0ce3834e13c1680050ef3bad4b364c18f7d110d416e9e5540e60f26d4f"},"ENT_W2_Spot_The_Gap":{"path":"GROW_ASDAN/Enterprise/ENT_W2_Spot_The_Gap.html","pathway":"GROW","subsection":"Enterprise","lessonTitle":"Week 2 · Spot the Gap","targetTitle":"We Do 1","title":"Opportunity hotspot scan","purpose":"Develop observation and user-empathy before idea generation.","activity":{"type":"hotspot","scene":"enterprise","prompt":"Predict which observation will reveal the strongest enterprise opportunity. Open each hotspot and separate inconvenience, genuine need and possible solution.","hotspots":[{"id":"h1","x":18,"y":24,"label":"WAITING","note":"Count or observe where time is lost and for whom."},{"id":"h2","x":50,"y":18,"label":"WASTE","note":"Identify a repeated unused resource and why it is unused."},{"id":"h3","x":82,"y":27,"label":"ACCESS","note":"Notice where instructions, routes or products exclude a user."},{"id":"h4","x":23,"y":66,"label":"REPEAT REQUEST","note":"A repeated request may reveal demand, but it still needs checking."},{"id":"h5","x":52,"y":72,"label":"WORKAROUND","note":"What people already do can show both need and a competing solution."},{"id":"h6","x":82,"y":65,"label":"CONSTRAINT","note":"Rules, cost, capacity and safety may make an attractive gap unsuitable."}],"completion":"An opportunity is a checked user problem with enough value and workable scope—not simply something that annoys the team.","predictionOptions":["A repeated request will reveal most","A visible workaround will reveal most","An access barrier will reveal most"]},"independent":"Complete a gap card: user / current problem / evidence / existing workaround / constraint / question to test.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original service journey with waiting, waste, access, request, workaround and constraint hotspots.","mediaKey":"enterprise","slug":"ENT_W2_Spot_The_Gap","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["PREDICT","TEST","COMPARE","JUSTIFY"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"e6c2db3b9ce9cd60c78a5b645a2d345ff2283b9a762265c8b1d40dd7b6a80225"},"ENT_W3_Our_Idea_Our_Users":{"path":"GROW_ASDAN/Enterprise/ENT_W3_Our_Idea_Our_Users.html","pathway":"GROW","subsection":"Enterprise","lessonTitle":"Week 3 · Our Idea, Our Users","targetTitle":"We Do 1","title":"User–need–feature fit model","purpose":"Make user-centred design visible and require a causal link between consultation and product decision.","activity":{"type":"model","prompt":"Choose a user definition, need evidence and feature response. Run two trials changing one factor to test fit.","controls":[{"id":"c1","label":"User","default":"everyone","options":[{"value":"everyone","label":"Everyone","quality":0,"feedback":"The team cannot design or consult meaningfully."},{"value":"specific","label":"A specific fictional or agreed user group","quality":2,"feedback":"Needs and access can be checked."}]},{"id":"c2","label":"Need evidence","default":"guess","options":[{"value":"guess","label":"Team preference","quality":0,"feedback":"It does not establish user demand."},{"value":"evidence","label":"Authorised observation, consultation or existing information","quality":2,"feedback":"The need has a traceable basis."}]},{"id":"c3","label":"Feature response","default":"random","options":[{"value":"random","label":"Favourite feature","quality":0,"feedback":"The feature is not connected to need."},{"value":"matched","label":"Feature explicitly responds to the evidence","quality":2,"feedback":"The offer has a reason."}]}],"outcomes":[{"min":0,"max":2,"label":"idea-led, not user-led","message":"The group is designing for itself."},{"min":3,"max":4,"label":"partial user fit","message":"One link is still assumed."},{"min":5,"max":6,"label":"testable user–idea fit","message":"User, evidence and feature connect."}],"completion":"A useful enterprise idea can show exactly which user evidence led to which feature.","predictionOptions":["The favourite idea will remain strongest","Narrowing the user will change the design","Evidence will change the chosen feature"],"requiredRuns":2},"independent":"Complete the fit statement: For [user], who needs [evidence], our offer provides [feature], which helps by [benefit].","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original three-link user-fit canvas with evidence arrow into a product feature.","mediaKey":"enterprise","slug":"ENT_W3_Our_Idea_Our_Users","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["PREDICT","TEST","COMPARE","JUSTIFY"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"0fc254346b6d289fd7e78808b73b6b073fa9425c3467e17e4e541c4572b7224c"},"ENT_W4_Money_In_Money_Out":{"path":"GROW_ASDAN/Enterprise/ENT_W4_Money_In_Money_Out.html","pathway":"GROW","subsection":"Enterprise","lessonTitle":"Week 4 · Money In, Money Out","targetTitle":"We Do 1","title":"Money-in / money-out sandbox","purpose":"Allow pupils to manipulate the variables behind break-even and compare one change at a time.","activity":{"type":"model","prompt":"Choose fictional sales volume, unit price and unit cost. Predict the result, run a baseline, then change one variable.","controls":[{"id":"c1","label":"Sales volume","default":"low","options":[{"value":"low","label":"Sell 5","quality":1,"feedback":"A smaller number of sales limits income."},{"value":"high","label":"Sell 10","quality":2,"feedback":"More sales increase income if demand exists."}]},{"id":"c2","label":"Unit price","default":"p2","options":[{"value":"p2","label":"£2 each","quality":1,"feedback":"Lower income per unit."},{"value":"p3","label":"£3 each","quality":2,"feedback":"Higher income per unit, but user value still matters."}]},{"id":"c3","label":"Unit cost","default":"c2","options":[{"value":"c2","label":"£2 cost each","quality":0,"feedback":"Little or no margin remains at low price."},{"value":"c1","label":"£1 cost each","quality":2,"feedback":"More margin remains, if the estimate is accurate."}]}],"outcomes":[{"min":0,"max":2,"label":"loss or no useful margin","message":"Costs consume the expected income."},{"min":3,"max":4,"label":"small margin","message":"The plan may work but assumptions need testing."},{"min":5,"max":6,"label":"stronger fictional margin","message":"Income exceeds estimated costs; real demand and full costs still need checking."}],"completion":"Income, cost and surplus are calculated from transparent assumptions; the model is fictional rehearsal, not financial advice or a real account.","predictionOptions":["The baseline will lose money","Changing volume will matter most","Changing unit cost will matter most"],"requiredRuns":2},"independent":"Complete the supplied fictional calculation independently. Show sales income, total cost, difference and one assumption to test.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original enterprise balance sheet with unit blocks, income stream and cost drain.","mediaKey":"enterprise","slug":"ENT_W4_Money_In_Money_Out","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["PREDICT","TEST","COMPARE","JUSTIFY"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"048a6e162a39f6b5a8f25e3978da6d7dcf6b2ca3ee1b0c8482581f905e5f3d80"},"ENT_W5_Brand_And_Pitch":{"path":"GROW_ASDAN/Enterprise/ENT_W5_Brand_And_Pitch.html","pathway":"GROW","subsection":"Enterprise","lessonTitle":"Week 5 · Brand & Pitch","targetTitle":"We Do 1","title":"Pitch-content evidence filter","purpose":"Keep pupils from spending all planning time on logos and effects while core enterprise reasoning remains weak.","activity":{"type":"evidence","prompt":"Predict which pitch element will most affect audience understanding. Select a complete brand-and-pitch evidence set.","statements":[{"id":"e1","label":"A name or visual identity that is readable and appropriate for the user.","correct":true,"reason":"Branding helps recognition when it remains accessible."},{"id":"e2","label":"A clear statement of the user need and offer.","correct":true,"reason":"The audience understands the purpose."},{"id":"e3","label":"A slogan that makes a guarantee the team cannot evidence.","correct":false,"reason":"Brand language must remain truthful."},{"id":"e4","label":"One demonstration, mock-up or process visual.","correct":true,"reason":"The offer becomes concrete."},{"id":"e5","label":"A simple cost/price/resource explanation.","correct":true,"reason":"The practical route is visible."},{"id":"e6","label":"Animations, music and effects with no content plan.","correct":false,"reason":"Effects cannot replace message structure."},{"id":"e7","label":"A direct next step for the audience, such as feedback on one feature.","correct":true,"reason":"The pitch has a purposeful response route."},{"id":"e8","label":"An invented customer testimonial.","correct":false,"reason":"Only authentic feedback can be used."}],"completion":"A brand helps people recognise an offer; a pitch explains need, value, practical route and next action with truthful evidence.","predictionOptions":["The visual identity will matter most","The need-and-offer sentence will matter most","The demonstration will matter most"]},"independent":"Build the pitch storyboard: hook / need / offer / demonstration / simple money / benefit / ask.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original pitch storyboard with brand mark held as one panel among six evidence panels.","mediaKey":"enterprise","slug":"ENT_W5_Brand_And_Pitch","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["PREDICT","TEST","COMPARE","JUSTIFY"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"e089be0ed3c21e82915506a751f3289a6ca4b3d6032e4edf51b142350afd4cc2"},"ENT_W6_Pitch_Day":{"path":"GROW_ASDAN/Enterprise/ENT_W6_Pitch_Day.html","pathway":"GROW","subsection":"Enterprise","lessonTitle":"Week 6 · Pitch Day","targetTitle":"We Do 1","title":"Feedback → decision → next move","purpose":"Help pupils receive feedback as evidence and independently convert it into a bounded decision.","activity":{"type":"evidence","prompt":"Predict which feedback type will be most useful. Select feedback that the team can act on and reject praise or criticism with no evidence.","statements":[{"id":"e1","label":"I understood the user, but the price basis was unclear.","correct":true,"reason":"It identifies a specific communication gap."},{"id":"e2","label":"It was good.","correct":false,"reason":"It gives no evidence or next decision."},{"id":"e3","label":"The demonstration showed the feature, but I still need to know how the user requested it.","correct":true,"reason":"It links a strength and an evidence gap."},{"id":"e4","label":"I do not like the colour.","correct":false,"reason":"Preference may matter only when linked to the intended user or accessibility."},{"id":"e5","label":"The first sentence was too long; the need became clear after the example.","correct":true,"reason":"The team can revise sequence and wording."},{"id":"e6","label":"Your group is the best.","correct":false,"reason":"Ranking does not improve the enterprise."},{"id":"e7","label":"I would test whether the intended user can complete the next step without help.","correct":true,"reason":"It proposes a relevant user test."},{"id":"e8","label":"You should change everything.","correct":false,"reason":"It is too broad to act on."}],"completion":"Useful pitch feedback is specific, relevant to the intended user or decision, and small enough to turn into one next action.","predictionOptions":["Message feedback will be most useful","User-fit feedback will be most useful","Practical-money feedback will be most useful"]},"independent":"After the real pitch, choose one authentic feedback point. Record keep / change / test and the reason in your own words.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original feedback triage board moving a comment through relevance and specificity gates into one action.","mediaKey":"enterprise","slug":"ENT_W6_Pitch_Day","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["PREDICT","TEST","COMPARE","JUSTIFY"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"54aa22ba99455af3c61134c5e1368c020b23e1a5efe355c860442a0022553e1f"},"GCOMM_W1_Our_Patch_Our_Say":{"path":"GROW_ASDAN/Community_Project/GCOMM_W1_Our_Patch_Our_Say.html","pathway":"GROW","subsection":"Community Project","lessonTitle":"Week 1 · Our Patch, Our Say","targetTitle":"We Do 1","title":"Community observation lenses","purpose":"Strengthen enquiry and protect against assumptions before the group chooses a project.","activity":{"type":"hotspot","scene":"community","prompt":"Predict which evidence source will reveal the most useful need. Open each community-observation hotspot and separate observation from interpretation.","hotspots":[{"id":"h1","x":18,"y":24,"label":"ROUTE","note":"Record who uses the route, when and what barrier is visible without identifying individuals."},{"id":"h2","x":50,"y":18,"label":"SPACE","note":"Notice access, condition, use and what is absent at a specific time."},{"id":"h3","x":82,"y":27,"label":"SERVICE","note":"Map what the service provides and what users currently have to do."},{"id":"h4","x":23,"y":66,"label":"VOICE","note":"Use authorised consultation questions; exact words are stronger than an adult summary."},{"id":"h5","x":52,"y":72,"label":"ASSET","note":"Check current condition, ownership and maintenance before proposing replacement."},{"id":"h6","x":82,"y":65,"label":"GAP","note":"Describe the difference between what happens now and the bounded improvement sought."}],"completion":"A community need begins as a bounded, evidence-supported gap; pupil voice contributes but is not invented or over-generalised.","predictionOptions":["Direct observation will reveal most","Authorised consultation will reveal most","Existing service information will reveal most"]},"independent":"Complete the observation sheet for one agreed place or service. Separate: what I saw / what I think / what must be checked.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original local patch map with route, space, service, voice, asset and gap lenses.","mediaKey":"community","slug":"GCOMM_W1_Our_Patch_Our_Say","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["PREDICT","TEST","COMPARE","JUSTIFY"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"7dfa0d2a5b09f512d25488631510d6e882204984b7712714ae650cfb51bc89fd"},"GCOMM_W2_Choose_The_Need":{"path":"GROW_ASDAN/Community_Project/GCOMM_W2_Choose_The_Need.html","pathway":"GROW","subsection":"Community Project","lessonTitle":"Week 2 · Choose the Need","targetTitle":"We Do 1","title":"Need decision matrix","purpose":"Make a group decision process visible and repeatable, allowing pupils to justify rather than defend preferences.","activity":{"type":"model","prompt":"Compare a need through evidence strength, achievable scope and community benefit. Run two trials changing one factor.","controls":[{"id":"c1","label":"Evidence","default":"weak","options":[{"value":"weak","label":"Preference or assumption only","quality":0,"feedback":"The need is not established."},{"value":"strong","label":"Observation plus authorised voice or partner information","quality":2,"feedback":"The need has more than one relevant source."}]},{"id":"c2","label":"Scope","default":"wide","options":[{"value":"wide","label":"Fix a whole community issue","quality":0,"feedback":"The group cannot control the outcome."},{"value":"bounded","label":"One place, group, product or action within the unit","quality":2,"feedback":"The project can be planned and reviewed."}]},{"id":"c3","label":"Benefit","default":"unclear","options":[{"value":"unclear","label":"No named beneficiary or useful change","quality":0,"feedback":"The project may become activity for its own sake."},{"value":"specific","label":"Named beneficiary and intended practical benefit","quality":2,"feedback":"The purpose can guide decisions."}]}],"outcomes":[{"min":0,"max":2,"label":"poor project candidate","message":"The group cannot yet justify or control it."},{"min":3,"max":4,"label":"candidate needs refinement","message":"One decision criterion remains weak."},{"min":5,"max":6,"label":"stronger project need","message":"Evidence, scope and benefit align."}],"completion":"A project need is chosen by evidence, controllable scope and intended benefit—not by the loudest preference.","predictionOptions":["The popular idea will remain strongest","Narrowing the scope will change the choice","Better evidence will change the choice"],"requiredRuns":2},"independent":"Score the shortlisted needs using the class matrix. Record the chosen need, one rejected option and the evidence-led reason.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original weighted decision matrix with evidence, scope and benefit gauges.","mediaKey":"community","slug":"GCOMM_W2_Choose_The_Need","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["PREDICT","TEST","COMPARE","JUSTIFY"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"dcbb12dcfb84f7f0b7972606b08d0050b11311da02495505dd0f2c5d037d2f64"},"GCOMM_W3_Roles_Steps_Resources":{"path":"GROW_ASDAN/Community_Project/GCOMM_W3_Roles_Steps_Resources.html","pathway":"GROW","subsection":"Community Project","lessonTitle":"Week 3 · Roles, Steps, Resources","targetTitle":"We Do 1","title":"Project dependency sequence","purpose":"Externalise project planning so pupils can independently locate the next step and recover from disruption.","activity":{"type":"sequence","prompt":"Predict where the project plan is most likely to break. Put the plan-building sequence in order and mark dependencies.","steps":[{"id":"s1","label":"Restate the bounded need and finished project outcome.","reason":"The team plans the same project."},{"id":"s2","label":"Break the outcome into observable steps.","reason":"Work becomes assignable and checkable."},{"id":"s3","label":"Identify resources, permissions and information for each step.","reason":"Hidden dependencies become visible."},{"id":"s4","label":"Assign one owner and one handover point to each step.","reason":"Responsibility is clear without isolating the owner."},{"id":"s5","label":"Place steps in time and mark what must happen first.","reason":"The schedule reflects dependencies."},{"id":"s6","label":"Run a missing-resource and absence test.","reason":"The team plans a recovery route."},{"id":"s7","label":"Confirm the first action and the next review point.","reason":"The plan leads into action."}],"completion":"A project plan links outcome, steps, resources, owners, dependencies and review; a list of jobs is not enough.","predictionOptions":["The plan will break at resources","The plan will break at role handover","The plan will break at timing"]},"independent":"Complete the team plan. Use arrows to show dependencies and name the first review point.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original project network with role cards, resources and dependency arrows.","mediaKey":"community","slug":"GCOMM_W3_Roles_Steps_Resources","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["PREDICT","TEST","COMPARE","JUSTIFY"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"b393a073578427bc5dc46eeaaa82b3167b86330af4830cb820e83479e6eae777"},"GCOMM_W4_First_Contact":{"path":"GROW_ASDAN/Community_Project/GCOMM_W4_First_Contact.html","pathway":"GROW","subsection":"Community Project","lessonTitle":"Week 4 · First Contact","targetTitle":"We Do 1","title":"First-contact evidence checklist","purpose":"Build independent drafting skill while keeping external contact behind centre approval.","activity":{"type":"evidence","prompt":"Predict which part of a first-contact draft is most likely to be missing. Select the complete set for an authorised, purposeful message.","statements":[{"id":"e1","label":"Who the group is and the approved setting contact route.","correct":true,"reason":"The recipient can identify the legitimate context."},{"id":"e2","label":"A concise, evidence-based statement of the need.","correct":true,"reason":"The message has a grounded purpose."},{"id":"e3","label":"Every detail about individual pupils and their circumstances.","correct":false,"reason":"Personal information is not needed for the enquiry."},{"id":"e4","label":"A specific request, question or proposed next step.","correct":true,"reason":"The partner knows how to respond."},{"id":"e5","label":"A realistic timeframe and named adult contact.","correct":true,"reason":"The contact route is workable and safeguarded."},{"id":"e6","label":"A promise that the project will definitely solve the issue.","correct":false,"reason":"Outcome cannot be guaranteed before consultation and delivery."},{"id":"e7","label":"A check for accuracy, privacy, tone and permission before sending.","correct":true,"reason":"The authorised adult process is explicit."},{"id":"e8","label":"A made-up partner response to finish the worksheet.","correct":false,"reason":"Absent evidence remains absent."}],"completion":"First contact is brief, relevant, privacy-safe, realistic and routed through an authorised adult.","predictionOptions":["The request will be missing","The privacy check will be missing","The next-step detail will be missing"]},"independent":"Draft the real message on the approved template. Annotate purpose, evidence, request, adult route and privacy check.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original message anatomy diagram with sender, need, request, adult gate and partner response.","mediaKey":"community","slug":"GCOMM_W4_First_Contact","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["PREDICT","TEST","COMPARE","JUSTIFY"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"a1f75e523fc99736d1cd6460d724339fdba0855940ba855f429e4ee67eb66ec0"},"GCOMM_W5_Risk_And_Ready":{"path":"GROW_ASDAN/Community_Project/GCOMM_W5_Risk_And_Ready.html","pathway":"GROW","subsection":"Community Project","lessonTitle":"Week 5 · Risk & Ready","targetTitle":"We Do 1","title":"Risk-control chain","purpose":"Teach pupils to participate meaningfully in risk planning without implying they authorise activity.","activity":{"type":"model","prompt":"Choose a hazard description, control and ownership route. Run two trials changing one factor and compare readiness.","controls":[{"id":"c1","label":"Hazard","default":"vague","options":[{"value":"vague","label":"Something could go wrong","quality":0,"feedback":"The team cannot choose a proportionate control."},{"value":"specific","label":"Named source, person affected and possible harm","quality":2,"feedback":"The risk is understandable."}]},{"id":"c2","label":"Control","default":"generic","options":[{"value":"generic","label":"Be careful","quality":0,"feedback":"The instruction does not change the condition."},{"value":"matched","label":"Remove, reduce or manage the specific hazard","quality":2,"feedback":"The control targets the risk."}]},{"id":"c3","label":"Owner / stop route","default":"none","options":[{"value":"none","label":"No owner or stop decision","quality":0,"feedback":"The plan may continue when conditions change."},{"value":"named","label":"Named responsible adult/role and stop-review trigger","quality":2,"feedback":"Action and escalation are clear."}]}],"outcomes":[{"min":0,"max":2,"label":"not ready","message":"The risk statement cannot guide safe action."},{"min":3,"max":4,"label":"conditional readiness","message":"One part of the control chain is incomplete."},{"min":5,"max":6,"label":"ready for responsible-adult review","message":"Hazard, matched control and ownership align."}],"completion":"Risk planning is specific and actionable; the model never replaces the setting’s formal assessment or responsible-adult decision.","predictionOptions":["The first plan will only say ‘be careful’","One change will make it conditional","The final plan will be ready for adult review"],"requiredRuns":2},"independent":"Complete the pupil planning section, then take it through the named adult review. Record the authorised controls exactly.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original bow-tie risk diagram with hazard, controls, action owner and stop trigger.","mediaKey":"community","slug":"GCOMM_W5_Risk_And_Ready","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["PREDICT","TEST","COMPARE","JUSTIFY"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"eb53ef121773373f1867be60d7b9735d995e5404ef7532a10ae871851ac48498"},"GCOMM_W6_Green_Light":{"path":"GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html","pathway":"GROW","subsection":"Community Project","lessonTitle":"Week 6 · Green Light","targetTitle":"We Do 1","title":"Project readiness gate","purpose":"Give pupils a transparent readiness test and permission to stop at ‘not yet confirmed’.","activity":{"type":"evidence","prompt":"Predict which dependency is most likely to prevent the green light. Select every item that must be genuinely confirmed before delivery begins.","statements":[{"id":"e1","label":"The bounded need and intended outcome are agreed.","correct":true,"reason":"The team knows what it is delivering."},{"id":"e2","label":"Roles, steps, resources and time are workable.","correct":true,"reason":"The action plan can operate."},{"id":"e3","label":"The group has designed a logo.","correct":false,"reason":"Branding does not establish project readiness."},{"id":"e4","label":"Required permission, partner, access and responsible-adult checks are confirmed.","correct":true,"reason":"External dependencies are real, not assumed."},{"id":"e5","label":"Risks and matched controls are recorded through the setting’s process.","correct":true,"reason":"Safety is authorised outside the rehearsal tool."},{"id":"e6","label":"The pupils feel excited.","correct":false,"reason":"Motivation helps but is not a readiness gate."},{"id":"e7","label":"The evidence and report-back route is planned without sensitive data.","correct":true,"reason":"The team knows how authentic learning and delivery will be documented."},{"id":"e8","label":"Any unresolved item is visible as NOT YET CONFIRMED.","correct":true,"reason":"Unknowns are not converted into fictional approvals."}],"completion":"A genuine green light means the need, plan, resources, permissions, controls and evidence route are confirmed; enthusiasm cannot replace a dependency.","predictionOptions":["Permission will be the main blocker","Resources will be the main blocker","The evidence/report-back route will be the main blocker"]},"independent":"Complete the green-light sheet with the responsible adult. Any missing item remains open with an owner and next check date.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original project traffic gate using words, symbols and dependency locks rather than colour alone.","mediaKey":"community","slug":"GCOMM_W6_Green_Light","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["PREDICT","TEST","COMPARE","JUSTIFY"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"6be4034ffec735093514168243a92a994096ebe3aa590b02db230a11e2682c9d"},"PEQ_W1_Knowing_Myself":{"path":"GROW_ASDAN/PEQ/PEQ_W1_Knowing_Myself.html","pathway":"GROW","subsection":"PEQ","lessonTitle":"Week 1 · Knowing Myself","targetTitle":"We Do 1","title":"Self-knowledge evidence map","purpose":"Move the lesson from adjective collection to testable self-knowledge that can guide independent decisions.","activity":{"type":"hotspot","scene":"profile","prompt":"Commit a prediction about which evidence type will be easiest to use. Open every part of the self-knowledge map and compare the strength of the evidence.","hotspots":[{"id":"h1","x":18,"y":24,"label":"STRENGTH","note":"Name the action that supports the strength, not only the label."},{"id":"h2","x":50,"y":18,"label":"INTEREST","note":"Specify the activity or topic and what keeps attention."},{"id":"h3","x":82,"y":27,"label":"VALUE","note":"Show the choice or behaviour that reveals what matters."},{"id":"h4","x":23,"y":66,"label":"WORKING CONDITION","note":"Notice when focus is stronger: pace, space, group size or task type."},{"id":"h5","x":52,"y":72,"label":"STARTING POINT","note":"Record what can already be done and what is still developing."},{"id":"h6","x":82,"y":65,"label":"NEXT TEST","note":"Choose a small real task that can test the self-view."}],"completion":"Self-awareness grows when a pupil compares a self-description with actions, conditions and a new test.","predictionOptions":["A strength example will be easiest","A working-condition example will be easiest","The next test will reveal something unexpected"]},"independent":"Complete your profile using one strength, interest, value and working condition. Add the evidence and one next test for each.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original six-lens self-knowledge map with evidence tags and a next-test arrow.","mediaKey":"peq","slug":"PEQ_W1_Knowing_Myself","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["PREDICT","TEST","COMPARE","JUSTIFY"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"6219dd18bed377655f598c063152f6c6030332bfea996873619b50f65e9e612d"},"PEQ_W2_Goals_That_Work":{"path":"GROW_ASDAN/PEQ/PEQ_W2_Goals_That_Work.html","pathway":"GROW","subsection":"PEQ","lessonTitle":"Week 2 · Goals That Work","targetTitle":"We Do 1","title":"Goal quality test bench","purpose":"Let pupils see the effect of changing specificity, route or evidence one at a time.","activity":{"type":"model","prompt":"Choose one version of each goal feature, predict whether the goal will guide action, then run two trials changing one feature only.","controls":[{"id":"c1","label":"Outcome","default":"vague","options":[{"value":"vague","label":"Get better at communication","quality":0,"feedback":"The desired change is not observable."},{"value":"specific","label":"Give a two-minute update using three planned points","quality":2,"feedback":"The action and product are visible."}]},{"id":"c2","label":"Route","default":"none","options":[{"value":"none","label":"No first step","quality":0,"feedback":"The pupil cannot begin independently."},{"value":"steps","label":"Three short steps in order","quality":2,"feedback":"The route reduces uncertainty."}]},{"id":"c3","label":"Check","default":"feeling","options":[{"value":"feeling","label":"I will know because it feels good","quality":0,"feedback":"The check is not clear enough."},{"value":"evidence","label":"Named product, observation or feedback check","quality":2,"feedback":"Progress can be reviewed."}]}],"outcomes":[{"min":0,"max":2,"label":"wish rather than goal","message":"It does not yet tell the pupil what to do or check."},{"min":3,"max":4,"label":"goal partly usable","message":"One feature still leaves the route unclear."},{"min":5,"max":6,"label":"actionable goal","message":"Outcome, route and check align."}],"completion":"A goal supports independence when it makes the next action and the evidence of progress visible.","predictionOptions":["The first version will remain a wish","One change will make it partly usable","Two linked changes will make it actionable"],"requiredRuns":2},"independent":"Write one goal, three steps and one check. Cover the model and use your own checklist to decide whether another pupil could start it.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original goal telescope with observable outcome, stepping stones and check flag.","mediaKey":"peq","slug":"PEQ_W2_Goals_That_Work","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["PREDICT","TEST","COMPARE","JUSTIFY"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"5dc7eb1a2d941f114f9830a472eeb5ee8be9817b3a975ec566dc9b5d69b896b5"},"PEQ_W3_Working_With_Others":{"path":"GROW_ASDAN/PEQ/PEQ_W3_Working_With_Others.html","pathway":"GROW","subsection":"PEQ","lessonTitle":"Week 3 · Working With Others","targetTitle":"We Do 1","title":"Teamwork behaviour functions","purpose":"Make hidden team processes observable so pupils can choose a strategy independently during later group work.","activity":{"type":"sort","prompt":"Predict which behaviour will be hardest to classify. Sort the actions by the teamwork function they serve, then justify one borderline case.","categories":[{"id":"join","icon":"🤝","label":"CONTRIBUTE"},{"id":"listen","icon":"👂","label":"LISTEN & USE"},{"id":"coordinate","icon":"🧭","label":"COORDINATE"},{"id":"repair","icon":"🔧","label":"REPAIR A PROBLEM"}],"items":[{"id":"i1","icon":"🤝","label":"Complete the agreed part and share it at the handover point.","answer":"join","reason":"The person contributes a defined product."},{"id":"i2","icon":"👂","label":"Restate another person’s idea before responding.","answer":"listen","reason":"It proves the idea was processed."},{"id":"i3","icon":"🧭","label":"Check who owns each step and when it is due.","answer":"coordinate","reason":"It aligns roles and time."},{"id":"i4","icon":"🔧","label":"Name the disagreement and return to the shared aim.","answer":"repair","reason":"It addresses a barrier without attacking a person."},{"id":"i5","icon":"👂","label":"Change the plan after a valid access point is raised.","answer":"listen","reason":"Listening affects action."},{"id":"i6","icon":"🤝","label":"Offer help without taking over the other person’s role.","answer":"join","reason":"Support keeps ownership with the role holder."},{"id":"i7","icon":"🧭","label":"Signal early that a resource or deadline has changed.","answer":"coordinate","reason":"The team can adapt before failure."},{"id":"i8","icon":"🔧","label":"Ask for a pause and use the agreed restart routine.","answer":"repair","reason":"A regulated reset protects the task and relationships."}],"completion":"Effective teamwork includes contribution, listening that changes action, coordination and repair—not simply being in a group.","predictionOptions":["Listening and contributing will overlap most","Coordinating and repairing will overlap most","Every card will have one obvious home"]},"independent":"Choose one teamwork function to practise. Record the cue you will notice, the action you will take and the evidence after the task.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original teamwork control room with four functions and handover signals.","mediaKey":"peq","slug":"PEQ_W3_Working_With_Others","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["PREDICT","TEST","COMPARE","JUSTIFY"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"24f07627b076bfece828f13ffa36f4bac00209a2438f4ce368789b3740d09257"},"PEQ_W4_Managing_Myself":{"path":"GROW_ASDAN/PEQ/PEQ_W4_Managing_Myself.html","pathway":"GROW","subsection":"PEQ","lessonTitle":"Week 4 · Managing Myself","targetTitle":"We Do 1","title":"Manage the task, not just the clock","purpose":"Give pupils a reusable visual routine and a dignified recovery path.","activity":{"type":"sequence","prompt":"Predict which point in the routine is most likely to fail. Put the management loop in order and identify a recovery route.","steps":[{"id":"s1","label":"Define the task endpoint and the available time.","reason":"A visible finish and boundary guide planning."},{"id":"s2","label":"Choose the first small action and prepare required items.","reason":"Starting friction is reduced."},{"id":"s3","label":"Set one prompt or checkpoint, not a wall of reminders.","reason":"A cue supports action without taking over."},{"id":"s4","label":"Work until the checkpoint, then compare with the plan.","reason":"The pupil gets evidence before changing course."},{"id":"s5","label":"Use the agreed recovery action if attention, emotion or conditions change.","reason":"A planned reset is safer than waiting for crisis."},{"id":"s6","label":"Finish, store evidence and close the workspace.","reason":"Completion includes organisation."},{"id":"s7","label":"Reflect on one support to keep and one to reduce next time.","reason":"The routine develops independence."}],"completion":"Self-management is a plan-monitor-recover-review loop; needing a planned support does not mean the task was not independent.","predictionOptions":["Starting will be the weak point","Monitoring will be the weak point","Recovery after disruption will be the weak point"]},"independent":"Run the routine on one real lesson task. Record the planned prompt, checkpoint, recovery action and one change for next time.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original self-management loop with start, focus, check, recovery and reflection stations.","mediaKey":"peq","slug":"PEQ_W4_Managing_Myself","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["PREDICT","TEST","COMPARE","JUSTIFY"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"f6589114d2978693fd77f191ddc1a128a3d406f9db4541f6e6494874f2dad1a8"},"PEQ_W5_Solving_Problems":{"path":"GROW_ASDAN/PEQ/PEQ_W5_Solving_Problems.html","pathway":"GROW","subsection":"PEQ","lessonTitle":"Week 5 · Solving Problems","targetTitle":"We Do 1","title":"Problem → options → test","purpose":"Help pupils transfer a stable problem-solving method to practical and social tasks.","activity":{"type":"model","prompt":"Choose how the problem is defined, how options are generated and how the result is checked. Run two trials changing one choice.","controls":[{"id":"c1","label":"Define","default":"blur","options":[{"value":"blur","label":"Everything has gone wrong","quality":0,"feedback":"The problem is too broad to act on."},{"value":"specific","label":"One observable gap between current and needed state","quality":2,"feedback":"The team can target a solution."}]},{"id":"c2","label":"Options","default":"first","options":[{"value":"first","label":"Use the first idea immediately","quality":0,"feedback":"Alternatives and consequences are not considered."},{"value":"compare","label":"Generate and compare at least two safe options","quality":2,"feedback":"The decision has a basis."}]},{"id":"c3","label":"Check","default":"hope","options":[{"value":"hope","label":"Hope it worked","quality":0,"feedback":"There is no feedback loop."},{"value":"measure","label":"Use a named check and decide keep/change/stop","quality":2,"feedback":"The result informs the next action."}]}],"outcomes":[{"min":0,"max":2,"label":"panic response","message":"The pupil has action without a clear problem or check."},{"min":3,"max":4,"label":"partial problem-solving method","message":"One stage still relies on guessing."},{"min":5,"max":6,"label":"testable solution cycle","message":"Problem, options and check connect."}],"completion":"A problem-solving method makes the problem small enough to act on, compares safe options and tests the result.","predictionOptions":["The first trial will stay stuck","Changing one feature will improve the method","The final trial will create a testable cycle"],"requiredRuns":2},"independent":"Use the method on one supplied scenario. Record problem, two options, chosen action, check and next decision.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original problem-solving laboratory with magnifier, option branches and test loop.","mediaKey":"peq","slug":"PEQ_W5_Solving_Problems","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["PREDICT","TEST","COMPARE","JUSTIFY"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"9be8204195999ed6d31b67a65990c46626c669bc213c20bd91be60f9ff070f86"},"PEQ_W6_Present_My_Progress":{"path":"GROW_ASDAN/PEQ/PEQ_W6_Present_My_Progress.html","pathway":"GROW","subsection":"PEQ","lessonTitle":"Week 6 · Present My Progress","targetTitle":"We Do 1","title":"Progress evidence curator","purpose":"Teach pupils to curate and explain progress rather than depend on an adult to assemble a celebration narrative.","activity":{"type":"evidence","prompt":"Predict which evidence type will make the progress claim strongest. Select a complete, honest presentation evidence set.","statements":[{"id":"e1","label":"A dated starting-point example and a later example from a similar task.","correct":true,"reason":"Comparable before-and-after evidence supports change."},{"id":"e2","label":"A list of everything completed this term.","correct":false,"reason":"Volume alone does not explain progress."},{"id":"e3","label":"One specific skill claim linked to an observable action.","correct":true,"reason":"The claim has a defined focus."},{"id":"e4","label":"A reflection explaining what changed, what helped and what remains difficult.","correct":true,"reason":"It interprets the evidence without pretending perfection."},{"id":"e5","label":"Only the best-looking final product.","correct":false,"reason":"The starting point and process are missing."},{"id":"e6","label":"One authentic feedback point and the decision made because of it.","correct":true,"reason":"Feedback is connected to action."},{"id":"e7","label":"A claim that no support was used even when support was present.","correct":false,"reason":"Authorship and support must be recorded honestly."},{"id":"e8","label":"One next goal based on the remaining gap.","correct":true,"reason":"The presentation leads to further action."}],"completion":"Progress is shown by comparable evidence, an honest account of support and change, and a next goal—not by a perfect final product.","predictionOptions":["Before-and-after work will matter most","Feedback and response will matter most","Reflection will matter most"]},"independent":"Build a three-minute progress presentation: starting point / change evidence / strategy or support / next goal.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original progress gallery with baseline, changed version, feedback arrow and next-goal door.","mediaKey":"peq","slug":"PEQ_W6_Present_My_Progress","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["PREDICT","TEST","COMPARE","JUSTIFY"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"payloadSha256":"3ac64257565050db7af2bbf97e717b3fc6f01774694b41bbdf97086801c3b1f3"}});
/* ============================================================================
 * BLOCKED — DO NOT MOUNT (band C outstanding)
 *
 * Band B is mounted: four decks load this engine, one per pathway plus one D&T.
 * No other deck may be mounted outside a gated band-C batch. This banner comes
 * off entirely when band C completes.
 *
 *   1. CLEARED -- the vendor's decisive post-integration regression has now been
 *      RUN in a real browser and is green for band B. Re-run it per batch.
 *   2. CLEARED at cc4f6fa -- reduced motion is read from matchMedia at load and
 *      watched with a change listener; .asvl-static follows the OS preference.
 *   3. RESOLVED -- the D&T decks are off the BUILD compiler but their chassis
 *      does carry the staff answers organ; they mount per-file.
 *   4. PARKED, gating nothing -- docs/MEDIA_REGISTER.md is a candidate register;
 *      lesson-payloads.json has 0 external URLs, so no mounted surface needs it.
 *
 * Accessibility ruling 5 Aug 2026: --asvl-accent-text / --asvl-muted-text darken
 * inherited colours for TEXT only, hue angle preserved. The estate palette and
 * every non-text use of --asvl-accent are untouched.
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
