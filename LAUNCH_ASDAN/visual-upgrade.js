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
/* ASDAN-VISUAL-LEARNING:JS:BEGIN v1 */
window.ASDANVisualPayloads = Object.assign(window.ASDANVisualPayloads || {}, {"CAREERS_W1_Know_Myself_for_Work":{"path":"LAUNCH_ASDAN/Careers/CAREERS_W1_Know_Myself_for_Work.html","pathway":"LAUNCH","subsection":"Careers","lessonTitle":"Week 1 · Know Myself for Work","targetTitle":"We Do 1","title":"Work-profile evidence dashboard","purpose":"Develop a profile pupils can actually use to compare opportunities independently.","activity":{"type":"hotspot","scene":"careers","prompt":"Predict which part of a work profile will most change the next-step decision. Open each evidence lens and identify what makes it usable.","hotspots":[{"id":"h1","x":18,"y":24,"label":"STRENGTH + EXAMPLE","note":"A work-related strength is tied to a real action, context and result."},{"id":"h2","x":50,"y":18,"label":"INTEREST + ACTIVITY","note":"An interest specifies what the pupil likes doing, not only a sector label."},{"id":"h3","x":82,"y":27,"label":"WORKING CONDITIONS","note":"Pace, environment, support, group size and task structure affect fit."},{"id":"h4","x":23,"y":66,"label":"VALUES","note":"Priorities such as helping, making, security or creativity are evidenced through choices."},{"id":"h5","x":52,"y":72,"label":"ACCESS / SUPPORT","note":"Reasonable adjustment and support needs are recorded as access, never as a deficit ranking."},{"id":"h6","x":82,"y":65,"label":"NEXT TEST","note":"A visit, conversation, task or current-source search can test the profile."}],"completion":"A work profile becomes a decision tool when it connects authentic evidence, preferred conditions, access and a testable next step.","predictionOptions":["Strength evidence will change the decision most","Working conditions will change it most","A next test will change it most"]},"independent":"Create the work profile with two evidenced strengths, two specific interests, preferred conditions, access/support and one next test.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original work-profile dashboard with six equal evidence lenses and no ranking dial.","mediaKey":"careers","slug":"CAREERS_W1_Know_Myself_for_Work","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"4fbcdb07ce229111bd48412419b0a0453f3aec8865d3a21852f97a31bbab0d6c"},"CAREERS_W2_The_World_of_Work_and_Its_Sectors":{"path":"LAUNCH_ASDAN/Careers/CAREERS_W2_The_World_of_Work_and_Its_Sectors.html","pathway":"LAUNCH","subsection":"Careers","lessonTitle":"Week 2 · The World of Work & Its Sectors","targetTitle":"We Do 1","title":"Sector–occupation connection map","purpose":"Avoid static job lists by showing cross-sector roles and transferable skills.","activity":{"type":"sort","prompt":"Predict which job will cross the most sector boundaries. Sort each task into its main sector, then discuss why real organisations use connected roles.","categories":[{"id":"health","icon":"🩺","label":"HEALTH & CARE"},{"id":"construct","icon":"🏗","label":"CONSTRUCTION & ENGINEERING"},{"id":"digital","icon":"💻","label":"DIGITAL & CREATIVE"},{"id":"hospital","icon":"🍽","label":"HOSPITALITY & RETAIL"},{"id":"public","icon":"🏛","label":"PUBLIC / COMMUNITY SERVICES"}],"items":[{"id":"i1","icon":"🩺","label":"Support a person’s daily care plan in an authorised role.","answer":"health","reason":"The task centres on health and care."},{"id":"i2","icon":"🏗","label":"Install and maintain equipment safely.","answer":"construct","reason":"The work uses engineering or trade processes."},{"id":"i3","icon":"💻","label":"Create and test accessible digital content.","answer":"digital","reason":"The task combines digital production and user needs."},{"id":"i4","icon":"🍽","label":"Prepare, present or sell food and customer services safely.","answer":"hospital","reason":"The task belongs mainly to hospitality or retail."},{"id":"i5","icon":"🏛","label":"Coordinate a community service or public facility.","answer":"public","reason":"The task serves a public or community function."},{"id":"i6","icon":"💻","label":"Design promotional material for a construction company.","answer":"digital","reason":"The employer’s sector and the worker’s occupational function can differ."},{"id":"i7","icon":"🩺","label":"Maintain digital appointment systems in a health setting.","answer":"digital","reason":"The occupational role is digital within a health organisation."},{"id":"i8","icon":"🏗","label":"Manage energy or infrastructure projects in Tees Valley.","answer":"construct","reason":"The work connects engineering, planning and local development."}],"completion":"Sectors describe broad areas of economic activity, while occupations and functions can move across them; pupils need both views.","predictionOptions":["Digital roles will cross most sectors","Customer-service roles will cross most sectors","Technical roles will cross most sectors"]},"independent":"Choose one local sector and map four different functions inside it. Add one occupation that could work across several sectors.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original sector metro map with cross-cutting digital, customer and technical lines.","mediaKey":"careers","slug":"CAREERS_W2_The_World_of_Work_and_Its_Sectors","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"bed337241de6b595f176b5eebeac49d94d1fff9e639d98db2e7a024713c77ca7"},"CAREERS_W3_Labour-Market_Information_and_Pathways":{"path":"LAUNCH_ASDAN/Careers/CAREERS_W3_Labour-Market_Information_and_Pathways.html","pathway":"LAUNCH","subsection":"Careers","lessonTitle":"Week 3 · Labour-Market Information & Pathways","targetTitle":"We Do 1","title":"LMI source-quality audit","purpose":"Build independent source-checking and reduce reliance on remembered or generic career claims.","activity":{"type":"evidence","prompt":"Predict which source feature is most likely to invalidate an LMI claim. Select the complete checks for current careers information.","statements":[{"id":"e1","label":"The source is identifiable and appropriate, such as an official careers, government or local labour-market service.","correct":true,"reason":"Authority and purpose can be evaluated."},{"id":"e2","label":"The publication or update date is visible.","correct":true,"reason":"Vacancies, routes, pay and demand can change."},{"id":"e3","label":"The geographic area matches the question.","correct":true,"reason":"National and local opportunities may differ."},{"id":"e4","label":"One social-media post is treated as proof of the whole sector.","correct":false,"reason":"It is not sufficient or representative evidence."},{"id":"e5","label":"Entry routes and requirements are checked on the current provider or official service.","correct":true,"reason":"Route information is live and specific."},{"id":"e6","label":"A salary figure is copied without range, date, location or conditions.","correct":false,"reason":"The number lacks usable context."},{"id":"e7","label":"At least two relevant sources are compared where a decision matters.","correct":true,"reason":"Comparison can expose differences or outdated claims."},{"id":"e8","label":"The screen fills an unknown pathway with a plausible answer.","correct":false,"reason":"Unknown remains not yet checked."}],"completion":"Useful LMI is current, attributable, geographically relevant and connected to a live route; it is evidence for enquiry, not a promise of a job.","predictionOptions":["Date will invalidate most claims","Location will invalidate most claims","Source authority will invalidate most claims"]},"independent":"Use two current official sources to compare one pathway. Record source, date checked, area, route, requirement and one uncertainty.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original LMI verification desk with source badge, date clock, map, route and uncertainty field.","mediaKey":"careers","slug":"CAREERS_W3_Labour-Market_Information_and_Pathways","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"d92513c7e8910e84e303d11d4d64c1f068c37cbd45d2fe23c36adc8e518d93a9"},"CAREERS_W4_Meeting_an_Employer":{"path":"LAUNCH_ASDAN/Careers/CAREERS_W4_Meeting_an_Employer.html","pathway":"LAUNCH","subsection":"Careers","lessonTitle":"Week 4 · Meeting an Employer","targetTitle":"We Do 1","title":"Employer encounter journey","purpose":"Give pupils a portable routine for employer visits, talks or interviews and make the next-step transfer explicit.","activity":{"type":"sequence","prompt":"Predict which part of the employer encounter will create the best evidence. Put the preparation-to-review route in order.","steps":[{"id":"s1","label":"Research the employer, role and purpose using current approved information.","reason":"Questions become relevant rather than generic."},{"id":"s2","label":"Prepare two evidence-led questions and one accessible participation route.","reason":"The learner can enter the conversation successfully."},{"id":"s3","label":"Confirm time, location, conduct, consent and responsible-adult arrangements.","reason":"The encounter is authorised and predictable."},{"id":"s4","label":"Listen, clarify and record key points using the agreed method.","reason":"The learner collects usable information."},{"id":"s5","label":"Ask a follow-up question that connects the answer to the learner’s profile.","reason":"The meeting informs a decision."},{"id":"s6","label":"Thank the employer and close through the agreed route.","reason":"Professional communication includes closure."},{"id":"s7","label":"Review what was learned, what changed and the next careers action.","reason":"The encounter becomes learning rather than attendance."}],"completion":"An employer encounter is prepared, purposeful, authorised and reviewed; attendance alone is not evidence of career learning.","predictionOptions":["Research will create the best evidence","The follow-up question will create the best evidence","The review will create the best evidence"]},"independent":"Use the approved encounter sheet. Record two answers, one connection to your profile and one current next action.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original employer-meeting pathway with research, question, encounter, review and action frames.","mediaKey":"careers","slug":"CAREERS_W4_Meeting_an_Employer","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"e75cd906d7fb76e2fa0f95cf3f20d926d9e91f40dd9682685ab16ed5f15ebdf0"},"CAREERS_W5_Matching_My_Profile_to_Opportunities":{"path":"LAUNCH_ASDAN/Careers/CAREERS_W5_Matching_My_Profile_to_Opportunities.html","pathway":"LAUNCH","subsection":"Careers","lessonTitle":"Week 5 · Matching My Profile to Opportunities","targetTitle":"We Do 1","title":"Profile–opportunity fit comparator","purpose":"Teach pupils to hold fit and uncertainty together and generate their own next enquiry.","activity":{"type":"model","prompt":"Choose profile evidence, opportunity facts and an access/next-test response. Run two comparisons changing one factor.","controls":[{"id":"c1","label":"Profile evidence","default":"broad","options":[{"value":"broad","label":"Generic interests and strengths","quality":0,"feedback":"The match can be made to almost anything."},{"value":"specific","label":"Evidenced skills, interests and conditions","quality":2,"feedback":"The comparison has meaningful criteria."}]},{"id":"c2","label":"Opportunity facts","default":"old","options":[{"value":"old","label":"Undated summary or hearsay","quality":0,"feedback":"The route may be inaccurate."},{"value":"current","label":"Current official description, tasks and requirements","quality":2,"feedback":"The opportunity side is traceable."}]},{"id":"c3","label":"Gap response","default":"ignore","options":[{"value":"ignore","label":"Ignore differences","quality":0,"feedback":"Fit is overstated."},{"value":"test","label":"Name a gap, access question or experience to test","quality":2,"feedback":"The comparison leads to enquiry."}]}],"outcomes":[{"min":0,"max":2,"label":"superficial match","message":"The conclusion is too broad or outdated."},{"min":3,"max":4,"label":"possible match with an open gap","message":"One side of the comparison needs stronger evidence."},{"min":5,"max":6,"label":"reasoned opportunity comparison","message":"Profile, current facts and next test connect."}],"completion":"A careers match is a reasoned comparison with open questions—not a prediction that a pupil will get or enjoy a job.","predictionOptions":["The profile evidence will be the weak side","The opportunity information will be the weak side","The gap response will change the conclusion"],"requiredRuns":2},"independent":"Compare two live opportunities using the matrix. Record evidence for fit, one gap, one access question and one next test.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original two-column opportunity comparator with fit links, open gaps and enquiry arrows.","mediaKey":"careers","slug":"CAREERS_W5_Matching_My_Profile_to_Opportunities","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"b184bef4e7b685112d41e889bd25b7926f34649191cdb480103d0dccff65d39e"},"CAREERS_W6_Setting_SMART_Careers_Targets":{"path":"LAUNCH_ASDAN/Careers/CAREERS_W6_Setting_SMART_Careers_Targets.html","pathway":"LAUNCH","subsection":"Careers","lessonTitle":"Week 6 · Setting SMART Careers Targets","targetTitle":"We Do 1","title":"SMART careers target builder","purpose":"End the sequence with an achievable enquiry or preparation action pupils can carry forward independently.","activity":{"type":"model","prompt":"Build a target from a current next step, an observable action and a review point. Run two trials changing one condition.","controls":[{"id":"c1","label":"Action","default":"vague","options":[{"value":"vague","label":"Explore careers more","quality":0,"feedback":"The first action is not visible."},{"value":"specific","label":"Compare two current apprenticeships and record requirements","quality":2,"feedback":"The task can begin and finish."}]},{"id":"c2","label":"Control","default":"dependent","options":[{"value":"dependent","label":"Depends entirely on an employer offering a place","quality":0,"feedback":"The pupil does not control the outcome."},{"value":"owned","label":"Uses an action the pupil can complete","quality":2,"feedback":"Responsibility is appropriately located."}]},{"id":"c3","label":"Review","default":"none","options":[{"value":"none","label":"No date or evidence check","quality":0,"feedback":"Progress cannot be reviewed."},{"value":"dated","label":"Named evidence and review date","quality":2,"feedback":"The target has a feedback loop."}]}],"outcomes":[{"min":0,"max":2,"label":"aspiration without a route","message":"The pupil cannot yet begin or review it."},{"min":3,"max":4,"label":"target needs one boundary","message":"One feature remains outside control or unmeasured."},{"min":5,"max":6,"label":"actionable careers target","message":"Owned action, evidence and review point align."}],"completion":"A careers target focuses on an action the pupil can control, using current information and a dated review—not on guaranteeing an external outcome.","predictionOptions":["Specific wording will matter most","Control over the action will matter most","The review point will matter most"],"requiredRuns":2},"independent":"Write one target with action, reason, first step, evidence, support/access and review date. Check it against a current route.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original target route with owned-action lane, external-outcome boundary and review checkpoint.","mediaKey":"careers","slug":"CAREERS_W6_Setting_SMART_Careers_Targets","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"01c0c5cdeaf4380578e7c34315da575d896be17971ebad996beafaa5500adf14"},"COMM_W1_Identify_a_Community_Need":{"path":"LAUNCH_ASDAN/Community_Enterprise/COMM_W1_Identify_a_Community_Need.html","pathway":"LAUNCH","subsection":"Community & Enterprise","lessonTitle":"Week 1 · Identify a Community Need","targetTitle":"We Do 1","title":"Community-need investigation map","purpose":"Raise the quality of enquiry before pupils commit to a social-action or enterprise response.","activity":{"type":"hotspot","scene":"community","prompt":"Predict which evidence source will most change the initial need statement. Open every hotspot and test whether the group has observation, voice and context.","hotspots":[{"id":"h1","x":18,"y":24,"label":"PEOPLE / USERS","note":"Define who is affected without collecting unnecessary personal information."},{"id":"h2","x":50,"y":18,"label":"PLACE / SERVICE","note":"Bound the location, service or situation being considered."},{"id":"h3","x":82,"y":27,"label":"CURRENT EXPERIENCE","note":"Describe what happens now using observable, attributable evidence."},{"id":"h4","x":23,"y":66,"label":"AUTHORISED VOICE","note":"Use real consultation through approved routes; never invent a quote or audience."},{"id":"h5","x":52,"y":72,"label":"CONSEQUENCE","note":"State a proportionate practical effect rather than a dramatic assumption."},{"id":"h6","x":82,"y":65,"label":"EXISTING ASSETS","note":"Map what already works so the project builds on rather than duplicates it."}],"completion":"A community need is a bounded, evidence-supported gap for real people in a real context; it is not a slogan or a solution written as a problem.","predictionOptions":["Direct observation will change the statement most","Authorised voice will change it most","Existing assets will change it most"]},"independent":"Write the need statement using: people / place / current evidence / consequence / what already exists / question still open.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original community-system map with users, place, experience, voice, consequence and existing-assets lenses.","mediaKey":"community","slug":"COMM_W1_Identify_a_Community_Need","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"60763f79119cd629f86f63e8c2d4eb22fef93fef15929eb36014a4de65ac486c"},"COMM_W2_Plan_a_Social-Action_or_Enterprise_Project":{"path":"LAUNCH_ASDAN/Community_Enterprise/COMM_W2_Plan_a_Social-Action_or_Enterprise_Project.html","pathway":"LAUNCH","subsection":"Community & Enterprise","lessonTitle":"Week 2 · Plan a Social-Action or Enterprise Project","targetTitle":"We Do 1","title":"Need–response–benefit project canvas","purpose":"Make causal reasoning and feasibility visible before pupils invest in branding or activity details.","activity":{"type":"model","prompt":"Choose the project response, resource route and intended benefit. Run two comparisons changing one factor.","controls":[{"id":"c1","label":"Response fit","default":"activity","options":[{"value":"activity","label":"An enjoyable activity unrelated to the need","quality":0,"feedback":"The project may be engaging but not responsive."},{"value":"fit","label":"A product, service or action linked directly to evidence","quality":2,"feedback":"The response has a causal link."}]},{"id":"c2","label":"Resources / feasibility","default":"assume","options":[{"value":"assume","label":"Time, money, permission and people assumed","quality":0,"feedback":"The plan may not be deliverable."},{"value":"checked","label":"Key resources, constraints and approvals identified","quality":2,"feedback":"The group can test feasibility."}]},{"id":"c3","label":"Benefit / measure","default":"broad","options":[{"value":"broad","label":"Improve the whole community","quality":0,"feedback":"The claim cannot be evidenced by the project."},{"value":"bounded","label":"Specific intended benefit and proportionate check","quality":2,"feedback":"The group can review what happened."}]}],"outcomes":[{"min":0,"max":2,"label":"activity without a project case","message":"Need, feasibility or benefit is disconnected."},{"min":3,"max":4,"label":"promising project concept","message":"One dependency needs development."},{"min":5,"max":6,"label":"workable project hypothesis","message":"Response, resources and bounded benefit align."}],"completion":"A project plan is a testable hypothesis: because this need exists, this feasible response may create this bounded benefit.","predictionOptions":["Response fit will matter most","Feasibility will matter most","The benefit measure will matter most"],"requiredRuns":2},"independent":"Complete the project canvas and state one assumption that must be checked before delivery.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original project hypothesis bridge from need evidence through response/resources to bounded benefit.","mediaKey":"community","slug":"COMM_W2_Plan_a_Social-Action_or_Enterprise_Project","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"c03d85fd97ab2812ae7bccee1fc75c39f0ac9b3d10157215e4052554a34ebacb"},"COMM_W3_Agree_Roles_Aims_and_Timeline":{"path":"LAUNCH_ASDAN/Community_Enterprise/COMM_W3_Agree_Roles_Aims_and_Timeline.html","pathway":"LAUNCH","subsection":"Community & Enterprise","lessonTitle":"Week 3 · Agree Roles, Aims & Timeline","targetTitle":"We Do 1","title":"Project timeline and handover network","purpose":"Give pupils enough project visibility to locate and own their next step without constant adult direction.","activity":{"type":"sequence","prompt":"Predict which dependency is most likely to create delay. Put the planning route in order and mark critical handovers.","steps":[{"id":"s1","label":"Confirm the agreed need, project aim and finished outcome.","reason":"The team shares the same destination."},{"id":"s2","label":"Break the outcome into milestones and observable tasks.","reason":"Progress can be seen and scheduled."},{"id":"s3","label":"Identify resources, approvals and partner inputs for each milestone.","reason":"External dependencies are visible."},{"id":"s4","label":"Assign roles through strengths, access and fair participation.","reason":"Ownership is purposeful rather than status-based."},{"id":"s5","label":"Add deadlines, handovers and review points.","reason":"The timeline shows when work changes hands."},{"id":"s6","label":"Run an absence, delay and missing-resource scenario.","reason":"The plan has a recovery route."},{"id":"s7","label":"Confirm the immediate next action and communication owner.","reason":"The plan becomes action."}],"completion":"A timeline is a dependency map with roles, handovers and recovery—not a decorative row of dates.","predictionOptions":["Partner input will cause most delay","Resource availability will cause most delay","Role handover will cause most delay"]},"independent":"Complete the live project board with milestones, owners, dependencies, review points and one recovery plan.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original critical-path timeline with role lanes, dependency diamonds and recovery branch.","mediaKey":"community","slug":"COMM_W3_Agree_Roles_Aims_and_Timeline","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"3805cfb4a21aa1afcc0f771e8848ddd1d680280797433d75d17c3383f9440015"},"COMM_W4_Partner_with_a_Local_Group_or_Charity":{"path":"LAUNCH_ASDAN/Community_Enterprise/COMM_W4_Partner_with_a_Local_Group_or_Charity.html","pathway":"LAUNCH","subsection":"Community & Enterprise","lessonTitle":"Week 4 · Partner with a Local Group or Charity","targetTitle":"We Do 1","title":"Partnership authenticity audit","purpose":"Build professional partnership reasoning while enforcing contact and data boundaries.","activity":{"type":"evidence","prompt":"Predict which partnership check will most change the project. Select the complete set for an authentic, authorised partnership.","statements":[{"id":"e1","label":"The organisation and contact route are verified through an official or centre-approved source.","correct":true,"reason":"The group knows who it is approaching."},{"id":"e2","label":"The project team identifies a specific reason the partnership could be useful to both sides.","correct":true,"reason":"Contact has purpose and reciprocity."},{"id":"e3","label":"Pupils message personal accounts directly because it is quicker.","correct":false,"reason":"External contact follows the authorised adult route."},{"id":"e4","label":"The partner’s real priorities, capacity and boundaries are heard and recorded accurately.","correct":true,"reason":"Partnership changes the plan rather than rubber-stamping it."},{"id":"e5","label":"The team promises outcomes before the partner has agreed.","correct":false,"reason":"Commitments cannot be invented."},{"id":"e6","label":"Consent, safeguarding, data, travel and recording requirements are checked.","correct":true,"reason":"Participation remains within centre processes."},{"id":"e7","label":"A real response is stored or referenced through the authorised evidence route.","correct":true,"reason":"The partnership is authentic and traceable."},{"id":"e8","label":"No reply is replaced with a fictional acceptance so planning can continue.","correct":false,"reason":"No response remains no response."}],"completion":"A partnership is verified, purposeful, reciprocal, authorised and capable of changing the plan; contact alone is not partnership evidence.","predictionOptions":["Verification will change the plan most","The partner’s capacity will change it most","Safeguarding/data requirements will change it most"]},"independent":"Prepare the partner brief and approved contact. Record actual priorities, boundaries, decisions and next action exactly when received.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original partnership bridge with verification, shared value, adult contact gate, partner voice and plan-change arrow.","mediaKey":"community","slug":"COMM_W4_Partner_with_a_Local_Group_or_Charity","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"f6b563d22cc3b20ce95396e25e7b6310eb261f535c4dc3088f52ee048b6af0b6"},"COMM_W5_Begin_Delivering_the_Project":{"path":"LAUNCH_ASDAN/Community_Enterprise/COMM_W5_Begin_Delivering_the_Project.html","pathway":"LAUNCH","subsection":"Community & Enterprise","lessonTitle":"Week 5 · Begin Delivering the Project","targetTitle":"We Do 1","title":"Live project delivery simulator","purpose":"Let pupils rehearse operational decisions and recovery before working with real participants or partners.","activity":{"type":"model","prompt":"Choose instruction, role coordination and monitoring. Run two delivery rehearsals changing one factor.","controls":[{"id":"c1","label":"Start / instruction","default":"unclear","options":[{"value":"unclear","label":"Begin when ready","quality":0,"feedback":"Participants and team members lack a shared first action."},{"value":"clear","label":"Brief model, visible first action and check for understanding","quality":2,"feedback":"Delivery has an accessible entry."}]},{"id":"c2","label":"Roles / handover","default":"blur","options":[{"value":"blur","label":"Roles change without communication","quality":0,"feedback":"Work may be duplicated, missed or unsafe."},{"value":"live","label":"Named roles, handover language and support route","quality":2,"feedback":"The team can coordinate."}]},{"id":"c3","label":"Monitor / adapt","default":"finish","options":[{"value":"finish","label":"Continue the plan regardless","quality":0,"feedback":"Evidence cannot influence delivery."},{"value":"check","label":"Use participant, quality and risk checks to adapt one thing","quality":2,"feedback":"Delivery becomes responsive."}]}],"outcomes":[{"min":0,"max":2,"label":"delivery likely to drift","message":"The team cannot start, coordinate or adapt reliably."},{"min":3,"max":4,"label":"delivery works only in ideal conditions","message":"One live-control feature is missing."},{"min":5,"max":6,"label":"responsive delivery rehearsal","message":"Start, roles and monitoring align; real delivery remains authorised."}],"completion":"Project delivery is a monitored system: clear entry, role handovers and evidence-led adaptation keep the plan connected to participants and purpose.","predictionOptions":["The start instruction will be the weak link","Role handover will be the weak link","Monitoring and adaptation will be the weak link"],"requiredRuns":2},"independent":"Deliver through the authorised plan. Record one monitoring point, one authentic change, support used and the immediate result.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original live-delivery control room with participant entry, role lanes, monitor gauge and adaptation loop.","mediaKey":"community","slug":"COMM_W5_Begin_Delivering_the_Project","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"75953dca121ecb17b2ad137d6db72d839ab9f174464d94c2072927f415e0cb32"},"COMM_W6_Promote_Our_Project":{"path":"LAUNCH_ASDAN/Community_Enterprise/COMM_W6_Promote_Our_Project.html","pathway":"LAUNCH","subsection":"Community & Enterprise","lessonTitle":"Week 6 · Promote Our Project","targetTitle":"We Do 1","title":"Promotion truth-and-access audit","purpose":"Move promotion from visual decoration to audience-centred, evidence-led communication.","activity":{"type":"evidence","prompt":"Predict which communication check will most affect trust. Select everything a safe, truthful promotion needs.","statements":[{"id":"e1","label":"A clear purpose and intended audience.","correct":true,"reason":"The format and message can be judged against a real need."},{"id":"e2","label":"Accurate project facts and a proportionate claim about current progress.","correct":true,"reason":"Promotion does not outrun evidence."},{"id":"e3","label":"Names, faces or stories of participants used without filed permission.","correct":false,"reason":"Consent and data boundaries apply."},{"id":"e4","label":"An accessible route such as readable layout, captions or an equivalent format.","correct":true,"reason":"Audience access is planned."},{"id":"e5","label":"A specific call to action that the audience can actually complete.","correct":true,"reason":"The message leads to a defined next step."},{"id":"e6","label":"An invented impact statistic to make the project sound important.","correct":false,"reason":"Only real, contextualised evidence can support impact."},{"id":"e7","label":"Partner name or logo used only with the agreed permission and wording.","correct":true,"reason":"Representation is authorised."},{"id":"e8","label":"A publication and responsible-adult check through the centre’s route.","correct":true,"reason":"Pupil drafting does not itself authorise release."}],"completion":"Trustworthy promotion is accurate, accessible, consented and proportionate, with a real call to action and authorised publication route.","predictionOptions":["Claim accuracy will matter most","Consent will matter most","Accessibility will matter most"]},"independent":"Create the promotional draft using authorised assets. Annotate claim evidence, consent/permission, access features, call to action and publication owner.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original campaign message checker with fact, consent, access, action and publication gates.","mediaKey":"community","slug":"COMM_W6_Promote_Our_Project","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"71d4b1f9d168ce8d22d4ba960b1949eb6b0c0b7e03957e89190bc3c52df7785e"},"LI_W1_Self-Care_Routines_and_Organisation":{"path":"LAUNCH_ASDAN/Living_Independently/LI_W1_Self-Care_Routines_and_Organisation.html","pathway":"LAUNCH","subsection":"Living Independently","lessonTitle":"Week 1 · Self-Care Routines & Organisation","targetTitle":"We Do 1","title":"Self-care routine architecture","purpose":"Support routine independence through task-specific scaffolding while preserving dignity and privacy.","activity":{"type":"sequence","prompt":"Predict which routine point is most likely to need a prompt. Order the planning-and-review cycle without requiring pupils to disclose private health information.","steps":[{"id":"s1","label":"Choose one ordinary, appropriate routine and define the finished state.","reason":"The task is bounded and privacy-safe."},{"id":"s2","label":"Identify time, place, items and any authorised support or reminder.","reason":"The environment is prepared."},{"id":"s3","label":"Use a visible first-step cue.","reason":"The pupil can begin without holding the whole routine in memory."},{"id":"s4","label":"Follow the routine and pause at any agreed safety or adult-check point.","reason":"Independence does not remove necessary checks."},{"id":"s5","label":"Use the short completion checklist.","reason":"The pupil verifies the result."},{"id":"s6","label":"Reset items and prepare for the next occurrence.","reason":"Organisation supports repetition."},{"id":"s7","label":"Review one cue to keep, change or reduce.","reason":"The routine develops over time."}],"completion":"An independent routine has a visible endpoint, prepared environment, first-step cue, appropriate check and review; private personal details are not classroom evidence.","predictionOptions":["Starting will need the prompt","Remembering the middle will need it","Closing and resetting will need it"]},"independent":"Complete the approved routine-planning sheet using a non-sensitive or fictional example where appropriate. Record only the task, support and review—not medical or personal circumstances.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original routine pathway with preparation, cue, action, check, reset and review stations.","mediaKey":"living","slug":"LI_W1_Self-Care_Routines_and_Organisation","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"5892429900c267cd8ee825001bd190ebfa26722e97bbad39b5e936faf4a83d6f"},"LI_W2_Home_Safety_and_Hazard_Awareness":{"path":"LAUNCH_ASDAN/Living_Independently/LI_W2_Home_Safety_and_Hazard_Awareness.html","pathway":"LAUNCH","subsection":"Living Independently","lessonTitle":"Week 2 · Home Safety & Hazard Awareness","targetTitle":"We Do 1","title":"Home hazard scan and stop route","purpose":"Turn safety into a repeatable scan-and-report process rather than a fear-based list.","activity":{"type":"hotspot","scene":"home","prompt":"Predict which hazard will be easiest to miss. Open every hotspot, identify the hazard-control link and name when to stop and seek responsible-adult help.","hotspots":[{"id":"h1","x":18,"y":24,"label":"TRIP / EXIT ROUTE","note":"Keep routes and exits clear; do not move heavy or unfamiliar items without the right support."},{"id":"h2","x":50,"y":18,"label":"ELECTRICAL","note":"Damaged plugs, overloaded sockets or wet electrical areas are reported and not handled."},{"id":"h3","x":82,"y":27,"label":"HEAT / FIRE","note":"Cooking, heaters, candles and alarms follow household and emergency procedures."},{"id":"h4","x":23,"y":66,"label":"CHEMICALS","note":"Cleaning products remain labelled, stored and used according to instructions; never mix products."},{"id":"h5","x":52,"y":72,"label":"WATER / SLIP","note":"Leaks and wet floors are controlled and reported before someone is harmed."},{"id":"h6","x":82,"y":65,"label":"SECURITY / STRANGER","note":"Doors, keys, callers and online contact follow agreed safety routines."}],"completion":"Hazard awareness means notice, avoid exposure, use a known control where trained, and report/escalate; the screen is not a home risk assessment.","predictionOptions":["The electrical hazard will be easiest to miss","The chemical hazard will be easiest to miss","The blocked route will be easiest to miss"]},"independent":"Complete the teacher-supplied fictional home audit. For each scenario record hazard / immediate safe action / who to contact.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original room plan with six numbered hazards, control shields and stop/report route.","mediaKey":"living","slug":"LI_W2_Home_Safety_and_Hazard_Awareness","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"786bf58810d028950eb6cf81466e7f658f9ea23e915f0b0b99b67d2aff5510a0"},"LI_W3_Laundry_and_Household_Maintenance":{"path":"LAUNCH_ASDAN/Living_Independently/LI_W3_Laundry_and_Household_Maintenance.html","pathway":"LAUNCH","subsection":"Living Independently","lessonTitle":"Week 3 · Laundry & Household Maintenance","targetTitle":"We Do 1","title":"Laundry label-to-storage sequence","purpose":"Build a visual procedure pupils can transfer to a real appliance only after local demonstration.","activity":{"type":"sequence","prompt":"Predict where a laundry routine is most likely to fail. Order the visual routine and identify which labels or appliance instructions must be checked locally.","steps":[{"id":"s1","label":"Check the item label and the appliance or household instruction.","reason":"Material and equipment rules are verified first."},{"id":"s2","label":"Sort by the taught criteria, such as colour, fabric and care requirement.","reason":"The load is made compatible."},{"id":"s3","label":"Check pockets, damage and load suitability.","reason":"Problems are found before the cycle."},{"id":"s4","label":"Measure the approved product using the label and local method.","reason":"More product is not automatically better."},{"id":"s5","label":"Select the authorised programme and start safely.","reason":"The pupil follows the actual appliance guidance."},{"id":"s6","label":"Dry and store items using the care instructions.","reason":"The routine continues after washing."},{"id":"s7","label":"Clean the area, report issues and review the routine.","reason":"Maintenance and fault reporting complete the task."}],"completion":"Laundry independence comes from reading labels, sorting, measuring, following the actual appliance instruction and closing the routine safely.","predictionOptions":["Sorting will be the weak point","Measuring/product choice will be the weak point","Drying and storage will be the weak point"]},"independent":"Use the supplied mock care labels and appliance guide to complete the rehearsal. Perform any real task only under the setting’s agreed supervision.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original laundry cycle with care label, sorting baskets, measure, programme, drying and storage.","mediaKey":"living","slug":"LI_W3_Laundry_and_Household_Maintenance","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"2fd7bb20d42536b5f14b852a3719c4917d0a7307c598fe1f77128949cda360d3"},"LI_W4_Keeping_a_Clean_Safe_Living_Space":{"path":"LAUNCH_ASDAN/Living_Independently/LI_W4_Keeping_a_Clean_Safe_Living_Space.html","pathway":"LAUNCH","subsection":"Living Independently","lessonTitle":"Week 4 · Keeping a Clean, Safe Living Space","targetTitle":"We Do 1","title":"Clean-zone control model","purpose":"Prevent overload and unsafe improvisation by externalising the task boundary and end state.","activity":{"type":"model","prompt":"Choose the task boundary, product match and close-down route. Run two trials changing one factor.","controls":[{"id":"c1","label":"Task boundary","default":"whole","options":[{"value":"whole","label":"Clean the whole home now","quality":0,"feedback":"The task is too broad to start or check."},{"value":"zone","label":"One named surface or zone","quality":2,"feedback":"The task has a visible endpoint."}]},{"id":"c2","label":"Product / method","default":"guess","options":[{"value":"guess","label":"Use any product or mix products","quality":0,"feedback":"This can be unsafe and ineffective."},{"value":"label","label":"Use the authorised product and label/local method","quality":2,"feedback":"The method is matched and controlled."}]},{"id":"c3","label":"Close-down","default":"leave","options":[{"value":"leave","label":"Leave products and waste out","quality":0,"feedback":"The space remains unsafe."},{"value":"close","label":"Store, dispose, ventilate and report as instructed","quality":2,"feedback":"The task ends safely."}]}],"outcomes":[{"min":0,"max":2,"label":"unsafe or unfinishable plan","message":"The task is too broad or the method is not controlled."},{"min":3,"max":4,"label":"partly workable routine","message":"One safety or completion feature is missing."},{"min":5,"max":6,"label":"bounded safe routine","message":"Zone, matched method and close-down align."}],"completion":"A cleaning routine is independent when the zone is bounded, the product and method are authorised, and storage/disposal complete the task.","predictionOptions":["The task boundary will matter most","Product choice will matter most","Close-down will matter most"],"requiredRuns":2},"independent":"Complete one approved practical zone using the physical checklist. Record the finished check and any issue reported, not personal household details.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original clean-zone plan with boundary frame, product-label match and close-down cabinet.","mediaKey":"living","slug":"LI_W4_Keeping_a_Clean_Safe_Living_Space","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"675639a5939553512803401c9cfe403934018c9563bfdd03c97c3228e4b6d48f"},"LI_W5_Personal_Admin_and_Responsibilities":{"path":"LAUNCH_ASDAN/Living_Independently/LI_W5_Personal_Admin_and_Responsibilities.html","pathway":"LAUNCH","subsection":"Living Independently","lessonTitle":"Week 5 · Personal Admin & Responsibilities","targetTitle":"We Do 1","title":"Private-document firewall","purpose":"Build functional admin literacy while enforcing the ASDAN data boundary.","activity":{"type":"evidence","prompt":"Predict which document clue will matter most in a fictional admin task. Select the safe, accurate actions and reject use of real personal documents as classroom evidence.","statements":[{"id":"e1","label":"Use teacher-produced exemplar letters, bills, forms or appointment cards.","correct":true,"reason":"The learning can be authentic without exposing personal data."},{"id":"e2","label":"Photograph a real bank statement or identity document for the portfolio.","correct":false,"reason":"Real financial, identity, medical or tenancy documents must not enter the evidence workflow."},{"id":"e3","label":"Identify sender, purpose, date, action and deadline on the exemplar.","correct":true,"reason":"These features support an admin decision."},{"id":"e4","label":"Use an authorised adult or service route when the document needs action.","correct":true,"reason":"Some responsibilities require support or formal contact."},{"id":"e5","label":"Guess what an unfamiliar official message means.","correct":false,"reason":"The pupil should pause and seek the appropriate help."},{"id":"e6","label":"Record a fictional completion check on the supplied task sheet.","correct":true,"reason":"The skill can be evidenced without copying private content."},{"id":"e7","label":"Share login details so an adult can complete the task quickly.","correct":false,"reason":"Security information is not shared."},{"id":"e8","label":"Store or dispose of sensitive documents using the agreed local process.","correct":true,"reason":"Personal admin includes data handling and security."}],"completion":"Personal-admin skills are taught with produced exemplars, clear action routes and secure handling; real sensitive documents are never photographed or uploaded as evidence.","predictionOptions":["The deadline will matter most","The action required will matter most","The authorised help route will matter most"]},"independent":"Complete the fictional admin scenario: identify / prioritise / choose action / use help route / record completion. Do not bring or upload real documents.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original mock-letter desk with sender, date, action, deadline, security and help-route lenses.","mediaKey":"living","slug":"LI_W5_Personal_Admin_and_Responsibilities","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"5478cd4b662d3425cb2c92bf8958e67f2186043a5776c235d080c052293e8b17"},"LI_W6_Plan_and_Shop_for_a_Balanced_Meal":{"path":"LAUNCH_ASDAN/Living_Independently/LI_W6_Plan_and_Shop_for_a_Balanced_Meal.html","pathway":"LAUNCH","subsection":"Living Independently","lessonTitle":"Week 6 · Plan & Shop for a Balanced Meal","targetTitle":"We Do 1","title":"Meal-to-basket planning model","purpose":"Integrate food, money and organisational skills into a single real-world planning sequence.","activity":{"type":"model","prompt":"Choose meal balance, fictional budget fit and shopping evidence. Run two comparisons changing one factor.","controls":[{"id":"c1","label":"Meal pattern","default":"narrow","options":[{"value":"narrow","label":"One main food group","quality":0,"feedback":"The plan lacks variety."},{"value":"balanced","label":"Several relevant Eatwell groups","quality":2,"feedback":"The plan has a broader balanced pattern."}]},{"id":"c2","label":"Budget / quantity","default":"ignore","options":[{"value":"ignore","label":"Ignore pack size and total","quality":0,"feedback":"The shop may exceed the fictional limit or waste food."},{"value":"check","label":"Compare total, quantity and planned use","quality":2,"feedback":"The plan considers cost and waste."}]},{"id":"c3","label":"Safe shop-to-home route","default":"missing","options":[{"value":"missing","label":"No label, storage or transport check","quality":0,"feedback":"Safety and suitability can fail after purchase."},{"value":"planned","label":"Check label/allergy task, chilled route and storage","quality":2,"feedback":"The plan continues safely into use."}]}],"outcomes":[{"min":0,"max":2,"label":"meal idea only","message":"The plan does not yet work as an independent shop."},{"min":3,"max":4,"label":"partly workable shop","message":"One balance, cost or safety link remains."},{"min":5,"max":6,"label":"workable fictional shopping plan","message":"Meal, quantity, budget and safe route align."}],"completion":"Independent meal shopping links a balanced plan, list, quantity, fictional budget and safe transport/storage route.","predictionOptions":["Meal balance will be the weak link","Budget and pack size will be the weak link","Storage/transport will be the weak link"],"requiredRuns":2},"independent":"Complete the fictional meal and shopping plan. Show list, quantities, prices, total, alternatives and safe storage route.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original meal-to-shop map with plate, list, shelf comparison, budget and fridge route.","mediaKey":"living","slug":"LI_W6_Plan_and_Shop_for_a_Balanced_Meal","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"db1ae669ef93cc2a00639ec491b13f2a3e662ce92fce40c3ef3abd90dee7ed0c"},"PEQ_W1_Intro_and_Choosing_My_Level":{"path":"LAUNCH_ASDAN/PEQ/PEQ_W1_Intro_and_Choosing_My_Level.html","pathway":"LAUNCH","subsection":"PEQ","lessonTitle":"Week 1 · Introduction & Choosing My Level","targetTitle":"We Do 1","title":"Starting-point evidence · no self-grading","purpose":"Protect the integrity of level choice while helping pupils understand what evidence makes the conversation fair and transparent.","activity":{"type":"evidence","prompt":"Predict which evidence will be most useful in a starting-point conversation. Select information that supports an honest centre decision; reject self-grading and guessed levels.","statements":[{"id":"e1","label":"A recent authentic task showing how independently the learner planned and completed it.","correct":true,"reason":"It provides observable starting-point evidence."},{"id":"e2","label":"The level the learner would most like printed on a certificate.","correct":false,"reason":"Preference does not determine assessment level."},{"id":"e3","label":"A comparable communication or teamwork task with the support used recorded honestly.","correct":true,"reason":"The action and access route can be discussed."},{"id":"e4","label":"A score created by this rehearsal activity.","correct":false,"reason":"The visual tool does not assess or select a qualification level."},{"id":"e5","label":"The current PEQ specification and centre assessment process.","correct":true,"reason":"Official criteria and authorised professional judgement govern the decision."},{"id":"e6","label":"A guessed criterion code because it looks plausible.","correct":false,"reason":"Unknown mappings remain not yet mapped."},{"id":"e7","label":"The learner’s goals and suitable challenge, considered alongside evidence.","correct":true,"reason":"The route should be meaningful as well as valid."},{"id":"e8","label":"A single good day treated as proof of all future performance.","correct":false,"reason":"A broader evidence picture is needed."}],"completion":"Choosing a working level is an authorised centre decision informed by current specification, authentic evidence, honest support records and suitable challenge; this screen never assigns it.","predictionOptions":["A recent task will matter most","Support and independence information will matter most","The current specification will matter most"]},"independent":"Prepare for the real level discussion by locating two recent tasks, the support used and one goal. The tutor or assessor follows the centre’s authorised process.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original evidence table with authentic task, support record, goal and official-criteria gate; no rank ladder.","mediaKey":"peq","slug":"PEQ_W1_Intro_and_Choosing_My_Level","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"5c2c9110f009657ff5f0a55fafe457e0a68f8de24e24a05034ac873defd1b20c"},"PEQ_W2_What_Makes_Communication_Effective":{"path":"LAUNCH_ASDAN/PEQ/PEQ_W2_What_Makes_Communication_Effective.html","pathway":"LAUNCH","subsection":"PEQ","lessonTitle":"Week 2 · What Makes Communication Effective","targetTitle":"We Do 1","title":"Communication-effect evidence filter","purpose":"Make communication effectiveness observable so pupils can plan and self-check rather than wait for general adult feedback.","activity":{"type":"evidence","prompt":"Predict which feature most changes whether a message works. Select every feature that can be evidenced in a real communication task.","statements":[{"id":"e1","label":"The purpose and intended audience are clear.","correct":true,"reason":"The choices can be judged against who needs the message and why."},{"id":"e2","label":"The message uses a format the sender personally prefers.","correct":false,"reason":"Sender preference alone does not establish audience access."},{"id":"e3","label":"Key information is ordered and easy to locate.","correct":true,"reason":"Structure affects understanding."},{"id":"e4","label":"The sender checks understanding or obtains an authentic response.","correct":true,"reason":"Communication includes reception, not only delivery."},{"id":"e5","label":"Lots of technical vocabulary is used.","correct":false,"reason":"Complexity is not automatically effective."},{"id":"e6","label":"Language, pace, visuals or format are adapted for the audience.","correct":true,"reason":"The message responds to access and context."},{"id":"e7","label":"The message is long enough to look impressive.","correct":false,"reason":"Length is not evidence of effectiveness."},{"id":"e8","label":"The sender can explain one choice and its effect.","correct":true,"reason":"Reasoned decisions support review."}],"completion":"Effective communication connects purpose, audience, accessible choices, organised content and evidence of reception.","predictionOptions":["Audience adaptation will matter most","Message structure will matter most","Checking reception will matter most"]},"independent":"Analyse one real or supplied communication: purpose / audience / three choices / reception evidence / one improvement.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original communication path from purpose through audience and design choices to reception check.","mediaKey":"peq","slug":"PEQ_W2_What_Makes_Communication_Effective","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"a705342d2c9bb59ff74f5161b49f4d44a948ee47c1fb2dee090f41c1ddeee318"},"PEQ_W3_Active_Listening_and_Giving_Feedback":{"path":"LAUNCH_ASDAN/PEQ/PEQ_W3_Active_Listening_and_Giving_Feedback.html","pathway":"LAUNCH","subsection":"PEQ","lessonTitle":"Week 3 · Active Listening & Giving Feedback","targetTitle":"We Do 1","title":"Listening evidence observatory","purpose":"Replace vague ‘good listening’ expectations with inclusive, observable functions.","activity":{"type":"hotspot","scene":"communication","prompt":"Predict which listening behaviour will be hardest to evidence. Open every hotspot and identify what an observer could actually notice.","hotspots":[{"id":"h1","x":18,"y":24,"label":"ATTEND","note":"Body position, agreed eye-contact alternative or other access behaviour shows attention without enforcing one presentation style."},{"id":"h2","x":50,"y":18,"label":"RETAIN","note":"The listener can accurately restate the key point."},{"id":"h3","x":82,"y":27,"label":"CLARIFY","note":"A question checks meaning rather than changing the topic."},{"id":"h4","x":23,"y":66,"label":"RESPOND","note":"The response addresses what was said."},{"id":"h5","x":52,"y":72,"label":"FEEDBACK","note":"Specific observation is linked to effect and a manageable next step."},{"id":"h6","x":82,"y":65,"label":"USE","note":"The listener changes a decision or action when the feedback is valid."}],"completion":"Active listening is evidenced when information is received, checked, responded to and used; visible behaviour must allow for individual access needs.","predictionOptions":["Restating will be hardest to evidence","Clarifying will be hardest to evidence","Using feedback will be hardest to evidence"]},"independent":"Complete a paired communication task. Use the observation sheet to record one listen/clarify/respond/use sequence and one specific feedback point.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original listening loop with inclusive attention routes, memory, clarification, response and action.","mediaKey":"peq","slug":"PEQ_W3_Active_Listening_and_Giving_Feedback","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"0941e94e4f732f516896b4f1fea1a9663ab0047d9ba90048aa3db259c065bf79"},"PEQ_W4_Plan_a_Communication_Activity":{"path":"LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html","pathway":"LAUNCH","subsection":"PEQ","lessonTitle":"Week 4 · Plan a Communication Activity","targetTitle":"We Do 1","title":"Communication activity dependency plan","purpose":"Support independent project planning while keeping consent, risk and delivery authority explicit.","activity":{"type":"sequence","prompt":"Predict where the activity plan will need the most revision. Put the planning sequence in dependency order.","steps":[{"id":"s1","label":"Define the communication purpose and intended participant outcome.","reason":"The activity has a reason beyond completing a worksheet."},{"id":"s2","label":"Identify participants, access needs and authorised context.","reason":"Design starts with the real people and setting."},{"id":"s3","label":"Choose a format and content route that match purpose and access.","reason":"Medium follows function."},{"id":"s4","label":"Plan instructions, roles, timing, resources and alternatives.","reason":"Participants can begin and continue."},{"id":"s5","label":"Define how understanding, participation and feedback will be observed.","reason":"Evidence is planned before delivery."},{"id":"s6","label":"Complete risk, consent, permission and responsible-adult checks.","reason":"External or recorded activity remains authorised."},{"id":"s7","label":"Rehearse, find one failure point and revise the plan.","reason":"The activity is tested before participants carry the risk."}],"completion":"A communication activity is ready when purpose, participants, access, delivery, evidence and authorisation are linked and rehearsed.","predictionOptions":["Access will drive the biggest revision","Instructions will drive the biggest revision","Evidence planning will drive the biggest revision"]},"independent":"Complete the authorised activity plan and rehearsal log. Record one test failure, the revision and who approves delivery.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original communication-activity canvas with participant route, format, access, evidence and approval locks.","mediaKey":"peq","slug":"PEQ_W4_Plan_a_Communication_Activity","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"27ce791ab11382919dfe6bfa709fe46a56bf85b556834badbd3c6cb90ec1a52d"},"PEQ_W5_Deliver_the_Activity_and_Gather_Evidence":{"path":"LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html","pathway":"LAUNCH","subsection":"PEQ","lessonTitle":"Week 5 · Deliver the Activity & Gather Evidence","targetTitle":"We Do 1","title":"Delivery rehearsal laboratory","purpose":"Allow pupils to rehearse adaptations and evidence decisions without generating a false performance record.","activity":{"type":"model","prompt":"Choose instruction clarity, access route and evidence method. Run two simulated trials, changing one factor, before the real authorised delivery.","controls":[{"id":"c1","label":"Instruction","default":"dense","options":[{"value":"dense","label":"One long spoken explanation","quality":0,"feedback":"Participants may not locate the first action."},{"value":"chunked","label":"Short modelled steps with a visible first action","quality":2,"feedback":"The route is easier to enter."}]},{"id":"c2","label":"Participation","default":"single","options":[{"value":"single","label":"One compulsory response route","quality":0,"feedback":"Access barriers may prevent participation."},{"value":"choice","label":"Equivalent speaking, doing, pointing or supported routes","quality":2,"feedback":"Participants can show the same learning accessibly."}]},{"id":"c3","label":"Evidence","default":"final","options":[{"value":"final","label":"Only a final photograph","quality":0,"feedback":"Process, communication and participant response are missing."},{"value":"planned","label":"Authorised plan, observation/witness and learner review","quality":2,"feedback":"Evidence is linked to the activity and privacy boundary."}]}],"outcomes":[{"min":0,"max":2,"label":"delivery fragile","message":"Participants or evidence can fail at several points."},{"min":3,"max":4,"label":"conditional delivery","message":"One dependency remains weak."},{"min":5,"max":6,"label":"stronger rehearsal plan","message":"Instruction, access and evidence route align; real delivery still needs authorisation."}],"completion":"Successful delivery gives participants a clear entry route, equivalent access choices and an authorised evidence plan; simulation is not evidence of delivery.","predictionOptions":["Instructions will be the main barrier","Participation route will be the main barrier","Evidence collection will be the main barrier"],"requiredRuns":2},"independent":"Deliver only through the approved plan. Afterwards locate authentic evidence and record support, changes and participant response without identifying audience members.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original participant-flow simulation with instruction, access-choice and evidence lanes.","mediaKey":"peq","slug":"PEQ_W5_Deliver_the_Activity_and_Gather_Evidence","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"7f5a5de8fd2522799eb43927622b8894319deecc314fd76607ecb3b43d25064b"},"PEQ_W6_Review_Progress_and_Sign_Off_the_Unit":{"path":"LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html","pathway":"LAUNCH","subsection":"PEQ","lessonTitle":"Week 6 · Review Progress & Sign Off the Unit","targetTitle":"We Do 1","title":"Portfolio review · evidence states stay outside","purpose":"Teach transparent portfolio curation while drawing a bright line around assessment authority.","activity":{"type":"evidence","prompt":"Predict which portfolio gap will be hardest to resolve. Select what belongs in an honest review pack; reject anything that pretends the screen or pupil can sign off achievement.","statements":[{"id":"e1","label":"A criterion or unit mapping taken from the current authorised specification.","correct":true,"reason":"The code is verified rather than guessed."},{"id":"e2","label":"Authentic products, observations, witness or review evidence linked to the task.","correct":true,"reason":"The evidence comes from real activity."},{"id":"e3","label":"A note of the support and reasonable adjustments used.","correct":true,"reason":"Authorship and access are recorded honestly."},{"id":"e4","label":"A certificate generated because every screen card was selected.","correct":false,"reason":"This tool has no certification or assessment authority."},{"id":"e5","label":"A learner review identifying evidence, learning and a next step.","correct":true,"reason":"The learner contributes meaning without being asked to self-certify."},{"id":"e6","label":"An invented witness statement to fill a missing box.","correct":false,"reason":"Missing evidence remains missing."},{"id":"e7","label":"Assessor or centre actions recorded through the authorised workflow.","correct":true,"reason":"Review and sign-off are professional processes outside the rehearsal."},{"id":"e8","label":"A guessed ‘achieved’ label because the work looks good.","correct":false,"reason":"Evidence states cannot be inferred by this tool."}],"completion":"The learner can review and locate evidence; only authorised centre and awarding-body processes determine assessment, quality assurance and certification.","predictionOptions":["Criterion mapping will be the hardest gap","Authentic evidence location will be hardest","Support/authorship records will be hardest"]},"independent":"Complete the learner review and evidence locator. Any gap is recorded for authorised review or one authentic addition; do not invent or self-sign evidence.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original portfolio map with evidence, mapping, support and learner-review lanes ending at an assessor gate.","mediaKey":"peq","slug":"PEQ_W6_Review_Progress_and_Sign_Off_the_Unit","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"8c383321f4cabf26312ecde577d34496f56b6df7f50ece334268d606e9376af5"},"VOC_W1_Introduction_to_Vocational_Skills_and_Workplaces":{"path":"LAUNCH_ASDAN/Vocational/VOC_W1_Introduction_to_Vocational_Skills_and_Workplaces.html","pathway":"LAUNCH","subsection":"Vocational","lessonTitle":"Week 1 · Vocational Skills & Workplaces","targetTitle":"We Do 1","title":"Transferable vocational skills map","purpose":"Build a cross-workplace skill language before pupils encounter specific tasks.","activity":{"type":"sort","prompt":"Predict which skill will transfer across the most workplaces. Sort each action by its main vocational function, then identify cross-over.","categories":[{"id":"safe","icon":"🛡","label":"SAFE WORKING"},{"id":"quality","icon":"✅","label":"QUALITY"},{"id":"team","icon":"👥","label":"TEAMWORK"},{"id":"routine","icon":"📋","label":"ROUTINE & RELIABILITY"},{"id":"service","icon":"💬","label":"SERVICE / COMMUNICATION"}],"items":[{"id":"i1","icon":"🛡","label":"Stop and report when equipment or conditions differ from the instruction.","answer":"safe","reason":"The action prevents exposure to an unknown risk."},{"id":"i2","icon":"✅","label":"Compare the finished item with the specification.","answer":"quality","reason":"The result is checked against a standard."},{"id":"i3","icon":"👥","label":"Complete a role and make the handover clear.","answer":"team","reason":"The action supports coordinated work."},{"id":"i4","icon":"📋","label":"Arrive prepared and follow the agreed sequence.","answer":"routine","reason":"The behaviour is repeatable and time-linked."},{"id":"i5","icon":"💬","label":"Clarify what the customer, colleague or participant needs.","answer":"service","reason":"Communication serves a work purpose."},{"id":"i6","icon":"✅","label":"Record a defect instead of hiding it.","answer":"quality","reason":"Accurate fault reporting protects later work."},{"id":"i7","icon":"🛡","label":"Use the taught control and required protective equipment.","answer":"safe","reason":"Controls are used as instructed."},{"id":"i8","icon":"👥","label":"Ask for support early without handing over the whole task.","answer":"team","reason":"The person remains responsible while using appropriate help."}],"completion":"Vocational competence combines safe action, quality, routine, communication and teamwork; most real tasks use several at once.","predictionOptions":["Safe working will transfer most","Routine and reliability will transfer most","Communication will transfer most"]},"independent":"Choose one workplace task. Map the five functions and add one observable action for each that applies.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original five-spoke workplace skills wheel with cross-over arrows.","mediaKey":"vocational","slug":"VOC_W1_Introduction_to_Vocational_Skills_and_Workplaces","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"f73ad4ac42a2c31ed4011fccb65c50c118b08d4f44053d7002f453643ccd5192"},"VOC_W2_Health_Safety_and_Hygiene_at_Work":{"path":"LAUNCH_ASDAN/Vocational/VOC_W2_Health_Safety_and_Hygiene_at_Work.html","pathway":"LAUNCH","subsection":"Vocational","lessonTitle":"Week 2 · Health, Safety & Hygiene at Work","targetTitle":"We Do 1","title":"Workplace control hotspot audit","purpose":"Make the hierarchy and ownership of workplace controls visible while avoiding generic ‘be careful’ messages.","activity":{"type":"hotspot","scene":"workplace","prompt":"Predict which control will be easiest to overlook. Open every workplace hotspot and distinguish hazard, control, responsibility and stop route.","hotspots":[{"id":"h1","x":18,"y":24,"label":"WORK AREA","note":"Routes, surfaces and storage are maintained so ordinary movement remains safe."},{"id":"h2","x":50,"y":18,"label":"EQUIPMENT","note":"Guards, condition, authorisation and training are checked before use."},{"id":"h3","x":82,"y":27,"label":"SUBSTANCES / DUST","note":"Labels, extraction, ventilation and local COSHH controls govern exposure."},{"id":"h4","x":23,"y":66,"label":"HYGIENE","note":"Hand, food, surface or personal-hygiene routines match the workplace task."},{"id":"h5","x":52,"y":72,"label":"PPE / RPE","note":"Protective equipment is task-specific, correctly fitted and additional to source control."},{"id":"h6","x":82,"y":65,"label":"REPORT / EMERGENCY","note":"Faults, near misses and changing conditions follow the named workplace route."}],"completion":"Workplace safety is a system of source control, training, equipment, hygiene, supervision and reporting; a pupil must not infer permission from this model.","predictionOptions":["Equipment condition will be overlooked","Substance/dust control will be overlooked","The report route will be overlooked"]},"independent":"Complete the local workplace induction task with the responsible adult. Record the taught controls, stop triggers and reporting route exactly.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original workplace panorama with work area, equipment, substance, hygiene, PPE and reporting hotspots.","mediaKey":"vocational","slug":"VOC_W2_Health_Safety_and_Hygiene_at_Work","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"33fd308dcf6977044716dce151734cfe37176eb4fd0ad52a5020ce3b9483f654"},"VOC_W3_Following_Instructions_and_Routines":{"path":"LAUNCH_ASDAN/Vocational/VOC_W3_Following_Instructions_and_Routines.html","pathway":"LAUNCH","subsection":"Vocational","lessonTitle":"Week 3 · Following Instructions & Routines","targetTitle":"We Do 1","title":"Instruction-to-action loop","purpose":"Teach a self-checking routine that reduces passive waiting and unsafe guessing.","activity":{"type":"sequence","prompt":"Predict where misunderstanding is most likely. Put the instruction cycle in order and identify where clarification belongs.","steps":[{"id":"s1","label":"Receive the instruction in the agreed accessible format.","reason":"The task information must reach the worker."},{"id":"s2","label":"Restate the outcome, first step and important control.","reason":"Understanding is checked before action."},{"id":"s3","label":"Prepare tools, materials and workspace in the stated order.","reason":"The environment supports the routine."},{"id":"s4","label":"Complete one chunk and compare it with the instruction.","reason":"A checkpoint catches drift early."},{"id":"s5","label":"Pause and clarify when wording, condition or result differs.","reason":"Asking early is part of reliable work."},{"id":"s6","label":"Complete the final check and handover.","reason":"The task ends against a defined standard."},{"id":"s7","label":"Review one prompt that could be reduced or retained next time.","reason":"Routine develops independence."}],"completion":"Following instructions is active: receive, restate, prepare, act, check, clarify and hand over.","predictionOptions":["Receiving the instruction will be the weak point","Checking after a chunk will be the weak point","Clarification will be the weak point"]},"independent":"Use the real task instruction. Mark the first action, checkpoint, stop/clarify cue, final standard and handover.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original instruction strip with chunk cards, checkpoint, clarification branch and final standard.","mediaKey":"vocational","slug":"VOC_W3_Following_Instructions_and_Routines","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"2a373fe279aaf6788713cada255358a883f3af7ebedf047aeb259835ac428b1a"},"VOC_W4_Teamwork_in_a_Vocational_Setting":{"path":"LAUNCH_ASDAN/Vocational/VOC_W4_Teamwork_in_a_Vocational_Setting.html","pathway":"LAUNCH","subsection":"Vocational","lessonTitle":"Week 4 · Teamwork in a Vocational Setting","targetTitle":"We Do 1","title":"Team shift simulator","purpose":"Make workplace coordination visible and allow pupils to rehearse disruption before the real task.","activity":{"type":"model","prompt":"Choose role clarity, handover quality and response to change. Run two simulated shifts changing one factor.","controls":[{"id":"c1","label":"Roles","default":"blur","options":[{"value":"blur","label":"Everyone does whatever is nearest","quality":0,"feedback":"Important work may be duplicated or missed."},{"value":"clear","label":"Named roles with shared aim","quality":2,"feedback":"Ownership and contribution are visible."}]},{"id":"c2","label":"Handover","default":"silent","options":[{"value":"silent","label":"Leave work without status","quality":0,"feedback":"The next person cannot continue safely or accurately."},{"value":"specific","label":"Item, state, issue and next action stated","quality":2,"feedback":"Work can transfer."}]},{"id":"c3","label":"Change","default":"hide","options":[{"value":"hide","label":"Keep disruption quiet","quality":0,"feedback":"The team loses time and risk increases."},{"value":"signal","label":"Report early, agree adaptation and update roles","quality":2,"feedback":"The team can recover."}]}],"outcomes":[{"min":0,"max":2,"label":"fragile team process","message":"Ownership and continuity are unclear."},{"min":3,"max":4,"label":"team works until conditions change","message":"One coordination control is missing."},{"min":5,"max":6,"label":"coordinated vocational team","message":"Roles, handover and recovery align."}],"completion":"Vocational teamwork protects continuity: clear ownership, explicit handover and early communication when conditions change.","predictionOptions":["Role clarity will matter most","Handover will matter most","Response to change will matter most"],"requiredRuns":2},"independent":"Complete the team task. Record your role, contribution, handover, one change and how the team responded.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original shift board with role lanes, handover card and disruption/replan signal.","mediaKey":"vocational","slug":"VOC_W4_Teamwork_in_a_Vocational_Setting","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"299ce3559940764acdb71de37aee6b460d151019cd0a5c540d9780853758a00b"},"VOC_W5_Tools_Equipment_and_Safe_Use":{"path":"LAUNCH_ASDAN/Vocational/VOC_W5_Tools_Equipment_and_Safe_Use.html","pathway":"LAUNCH","subsection":"Vocational","lessonTitle":"Week 5 · Tools, Equipment & Safe Use","targetTitle":"We Do 1","title":"Tool-use authorisation evidence audit","purpose":"Support safety reasoning while maintaining a non-negotiable boundary between digital rehearsal and physical authorisation.","activity":{"type":"evidence","prompt":"Predict which safe-use check is most likely to stop a task. Select the complete evidence set for choosing and using a tool under local authorisation.","statements":[{"id":"e1","label":"The tool is the specified type and size for the material and operation.","correct":true,"reason":"Selection is task-specific."},{"id":"e2","label":"The pupil has watched a video online, so local training is unnecessary.","correct":false,"reason":"External media cannot authorise equipment use."},{"id":"e3","label":"Condition, guard, cable, battery or other relevant features are checked as taught.","correct":true,"reason":"A visible pre-use inspection is completed."},{"id":"e4","label":"The work is secured and the area prepared using the local method.","correct":true,"reason":"The work condition supports safe use."},{"id":"e5","label":"Required supervision, competence check and PPE/RPE are confirmed.","correct":true,"reason":"Use remains within the workplace system."},{"id":"e6","label":"The pupil continues when the tool behaves differently because the task is nearly finished.","correct":false,"reason":"Unexpected condition triggers stop and report."},{"id":"e7","label":"The tool is made safe, returned and any fault reported after use.","correct":true,"reason":"Close-down is part of competent use."},{"id":"e8","label":"A high score in this rehearsal unlocks the real tool.","correct":false,"reason":"The component never grants permission or competence."}],"completion":"Safe tool use depends on correct selection, condition, setup, training, supervision, controls and stop/report behaviour; only the local responsible adult authorises use.","predictionOptions":["Tool selection will stop most tasks","Condition/setup will stop most tasks","Training/supervision will stop most tasks"]},"independent":"Complete the local tool checklist with the responsible adult. Record the authorised tool, task, controls and stop trigger—never a self-issued competence claim.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original tool station with selection, condition, setup, supervision, stop and return checkpoints.","mediaKey":"vocational","slug":"VOC_W5_Tools_Equipment_and_Safe_Use","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"58914e361c8c886173312c87b068fa6796404b0474b0dcb083ab0356a466f0e9"},"VOC_W6_Complete_a_Supported_Vocational_Task":{"path":"LAUNCH_ASDAN/Vocational/VOC_W6_Complete_a_Supported_Vocational_Task.html","pathway":"LAUNCH","subsection":"Vocational","lessonTitle":"Week 6 · Complete a Supported Vocational Task","targetTitle":"We Do 1","title":"Supported-task authenticity model","purpose":"Help pupils use support deliberately and explain their own contribution without being pushed toward false independence.","activity":{"type":"model","prompt":"Choose task clarity, support use and final checking. Run two rehearsals changing one factor before the real supported task.","controls":[{"id":"c1","label":"Task endpoint","default":"unclear","options":[{"value":"unclear","label":"Do some work until told to stop","quality":0,"feedback":"The pupil cannot judge completion."},{"value":"standard","label":"Named product, quantity or service standard","quality":2,"feedback":"The endpoint is visible."}]},{"id":"c2","label":"Support","default":"takeover","options":[{"value":"takeover","label":"Adult completes difficult parts","quality":0,"feedback":"Authorship and learning become unclear."},{"value":"planned","label":"Specific model, prompt or check with pupil action retained","quality":2,"feedback":"Support gives access while preserving ownership."}]},{"id":"c3","label":"Final check","default":"praise","options":[{"value":"praise","label":"Looks good","quality":0,"feedback":"The judgement is not tied to a standard."},{"value":"criteria","label":"Compare quality, safety and handover with the instruction","quality":2,"feedback":"The result is checked systematically."}]}],"outcomes":[{"min":0,"max":2,"label":"task cannot evidence pupil performance clearly","message":"Endpoint, ownership or check is weak."},{"min":3,"max":4,"label":"supported task needs one clarification","message":"One part of action or review remains ambiguous."},{"min":5,"max":6,"label":"clear supported-task plan","message":"Endpoint, honest support and criteria align."}],"completion":"A supported vocational task can still show authentic pupil performance when the endpoint, pupil action, support and final check are recorded honestly.","predictionOptions":["The endpoint will be the weak link","Support ownership will be the weak link","The final check will be the weak link"],"requiredRuns":2},"independent":"Complete the real authorised task. Record: instruction / my actions / support used / result / check / next skill.","independenceSteps":["Use the frozen visual to decide your first step.","Complete the real lesson task without copying the screen.","Check your work against the visible success conditions.","Ask for one specific prompt only if the check shows a gap."],"imageBrief":"Original vocational task bench with endpoint card, pupil-action lane, support bridge and quality gate.","mediaKey":"vocational","slug":"VOC_W6_Complete_a_Supported_Vocational_Task","version":"2026.08.05","rehearsalOnly":true,"panelNotice":"Rehearsal only. Nothing is saved, uploaded, graded, certified or added to a portfolio. Evidence comes from the real task and the lesson’s authorised process.","pathwayCycle":["INVESTIGATE","LOCATE EVIDENCE","REASON","ACT"],"helpLadder":["Look again at the frozen example or process.","Use one visible cue or sentence stem.","Ask for one specific prompt.","Use the teacher, assessor or responsible-adult route where safety, permission or evidence status is involved."],"successChecks":["The real task is completed, not only the screen rehearsal.","The choice, process or explanation is supported by visible evidence.","Any help, access route or adult decision is recorded honestly through the lesson’s authorised process."],"locator":{"evidenceForms":[{"id":"real","label":"Real task, product or action exists"},{"id":"observe","label":"Authentic observation, calculation or decision exists"},{"id":"witness","label":"Authentic feedback or witness evidence exists"},{"id":"none","label":"Evidence is not yet available"}],"locations":[{"id":"sheet","label":"Lesson sheet or physical work"},{"id":"record","label":"Authorised photo or record"},{"id":"witness","label":"Witness or feedback record"},{"id":"unlocated","label":"Not yet located"}],"routes":[{"id":"review","label":"Teacher or assessor review"},{"id":"safety","label":"Responsible-adult safety or permission check"},{"id":"addition","label":"Complete one authentic addition"},{"id":"access","label":"Use the approved access or reasonable-adjustment route"}]},"payloadSha256":"e3f1773427f9345959596ff92c5cd721484b51285fd8f359e4410b40b43bdc2e"}});
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
