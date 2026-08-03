#!/usr/bin/env node
/** Real-browser regression assertion for the Art Teesside visual teaching layer. */
'use strict';

const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const REPO = path.resolve(__dirname, '..', '..');
const ART = path.join(REPO, 'Art_Teesside');
const VIEWPORTS = [
  { width: 1920, height: 1080 },
  { width: 1280, height: 720 },
  { width: 768, height: 1024 },
  { width: 390, height: 844 },
];
const LESSON_RE = /^(?:BUILD|GROW|LAUNCH)_ART_(?:A2_)?W\d+_.+\.html$/;

function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const value = path.join(dir, entry.name);
    return entry.isDirectory() ? walk(value) : [value];
  });
}

function rel(file) {
  return path.relative(REPO, file).split(path.sep).join('/');
}

function parseArgs(argv) {
  const out = {
    baseUrl: process.env.ART_BASE_URL || '',
    report: process.env.ART_BROWSER_REPORT || path.join(REPO, 'art-browser-report.json'),
    screenshotDir: process.env.ART_SCREENSHOT_DIR || path.join(REPO, 'art-browser-failures'),
    selfTest: argv.includes('--self-test'),
  };
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === '--base-url') out.baseUrl = argv[++i];
    if (argv[i] === '--report') out.report = argv[++i];
    if (argv[i] === '--screenshot-dir') out.screenshotDir = argv[++i];
  }
  return out;
}

function urlFor(file, baseUrl) {
  if (!baseUrl) return pathToFileURL(file).href;
  const url = new URL(rel(file).split('/').map(encodeURIComponent).join('/'), baseUrl.endsWith('/') ? baseUrl : `${baseUrl}/`);
  return url.href;
}

function recorder(page, baseOrigin) {
  const state = { pageErrors: [], consoleErrors: [], failedRequests: [], badResponses: [] };
  page.on('pageerror', (error) => state.pageErrors.push(String(error && error.message ? error.message : error)));
  page.on('console', (message) => {
    if (message.type() === 'error') state.consoleErrors.push(message.text());
  });
  page.on('requestfailed', (request) => {
    let sameOrigin = true;
    try { sameOrigin = !baseOrigin || new URL(request.url()).origin === baseOrigin; } catch (_) {}
    if (sameOrigin) state.failedRequests.push(`${request.url()} :: ${request.failure() ? request.failure().errorText : 'failed'}`);
  });
  page.on('response', (response) => {
    let sameOrigin = true;
    try { sameOrigin = !baseOrigin || new URL(response.url()).origin === baseOrigin; } catch (_) {}
    if (sameOrigin && response.status() >= 400) state.badResponses.push(`${response.status()} ${response.url()}`);
  });
  return state;
}

function check(condition, label, failures, detail = '') {
  if (!condition) failures.push(detail ? `${label}: ${detail}` : label);
}

async function slideState(page) {
  return page.evaluate(() => {
    const slides = [...document.querySelectorAll('.slide')];
    const visible = slides.map((slide, index) => ({
      index,
      visible: getComputedStyle(slide).display !== 'none',
      activeClass: slide.classList.contains('active'),
    }));
    const visibleSlides = visible.filter((entry) => entry.visible);
    return {
      total: slides.length,
      visibleCount: visibleSlides.length,
      activeClassCount: visible.filter((entry) => entry.activeClass).length,
      activeIndex: visibleSlides.length === 1 ? visibleSlides[0].index : -1,
    };
  });
}

async function moveToSlide(page, targetIndex) {
  const total = await page.locator('.slide').count();
  if (!Number.isInteger(targetIndex) || targetIndex < 0 || targetIndex >= total) {
    throw new Error(`invalid target slide ${targetIndex} for population ${total}`);
  }
  for (let guard = 0; guard <= total; guard += 1) {
    const state = await slideState(page);
    if (state.visibleCount !== 1 || state.activeClassCount !== 1) {
      throw new Error(`ambiguous active slide while moving: ${JSON.stringify(state)}`);
    }
    if (state.activeIndex === targetIndex) return state;
    const label = state.activeIndex < targetIndex ? 'Next' : 'Previous';
    await page.locator('.controls button').filter({ hasText: label }).first().click();
    await page.waitForTimeout(18);
  }
  throw new Error(`failed to reach slide ${targetIndex}`);
}

async function hubState(page) {
  return page.evaluate(() => {
    const grid = document.querySelector('.grid');
    const cards = grid ? [...grid.querySelectorAll(':scope > a')] : [];
    const skip = document.querySelector('.art-skip-link');
    return {
      cards: cards.length,
      animated: cards.filter((card) => card.classList.contains('art-card-enter')).length,
      labelled: cards.filter((card) => !!card.getAttribute('aria-label')).length,
      gridId: grid ? grid.id : '',
      skipHref: skip ? skip.getAttribute('href') : '',
    };
  });
}

async function pageState(page) {
  return page.evaluate(() => {
    const controls = [...document.querySelectorAll('.controls button')].map((button) => {
      const box = button.getBoundingClientRect();
      const style = getComputedStyle(button);
      return {
        text: (button.textContent || '').replace(/\s+/g, ' ').trim(),
        visible: style.display !== 'none' && style.visibility !== 'hidden' && box.width > 0 && box.height > 0,
        left: box.left,
        right: box.right,
        top: box.top,
        bottom: box.bottom,
        width: box.width,
        height: box.height,
      };
    });
    const slides = [...document.querySelectorAll('.slide')];
    const active = slides.filter((slide) => getComputedStyle(slide).display !== 'none');
    const activeIndex = active.length === 1 ? slides.indexOf(active[0]) : -1;
    return {
      ready: document.documentElement.getAttribute('data-art-teach-boot'),
      kind: document.documentElement.getAttribute('data-art-page'),
      scrollWidth: document.documentElement.scrollWidth,
      innerWidth,
      slides: slides.length,
      active: active.length,
      activeClass: slides.filter((slide) => slide.classList.contains('active')).length,
      activeIndex,
      controls,
      visualCss: [...document.styleSheets].some((sheet) => (sheet.href || '').includes('art-teach.css')),
      visualJs: !!window.ArtTeach,
    };
  });
}

async function smoke(page, file, viewport, baseUrl, failures) {
  const origin = baseUrl ? new URL(baseUrl).origin : '';
  const events = recorder(page, origin);
  const response = await page.goto(urlFor(file, baseUrl), { waitUntil: 'load', timeout: 30000 });
  await page.waitForTimeout(180);
  const state = await pageState(page);
  check(response && response.status() === 200, 'HTTP status is 200', failures, response ? String(response.status()) : 'no response');
  check(state.ready === 'ready', 'shared layer reaches ready state', failures, String(state.ready));
  check(state.visualCss, 'shared stylesheet loaded', failures);
  check(state.scrollWidth <= state.innerWidth + 4, 'no horizontal page overflow', failures, `${state.scrollWidth}px > ${state.innerWidth}px`);

  const lesson = LESSON_RE.test(path.basename(file));
  if (!lesson) {
    check(state.kind === 'hub', 'hub classified correctly', failures, String(state.kind));
    const hub = await hubState(page);
    check(hub.cards > 0, 'hub exposes primary lesson/resource cards', failures);
    check(hub.animated === hub.cards, 'primary hub cards receive ordered visual entry', failures, `${hub.animated}/${hub.cards}`);
    check(hub.labelled === hub.cards, 'primary hub cards receive accessible names', failures, `${hub.labelled}/${hub.cards}`);
    check(hub.gridId && hub.skipHref === `#${hub.gridId}`, 'hub skip link targets the primary card grid', failures, JSON.stringify(hub));
  } else {
    check(state.kind === 'lesson', 'lesson classified correctly', failures, String(state.kind));
    check(state.visualJs, 'ArtTeach lifecycle loaded', failures);
    check(state.slides === 10, 'ten authored slides present', failures, String(state.slides));
    check(state.active === 1 && state.activeClass === 1 && state.activeIndex === 0, 'intended initial slide is uniquely active', failures, JSON.stringify(state));
    for (const control of state.controls) {
      check(control.visible, `control visible: ${control.text}`, failures);
      check(control.left >= -1 && control.right <= viewport.width + 1, `control horizontally reachable: ${control.text}`, failures, JSON.stringify(control));
      check(control.top >= -1 && control.bottom <= viewport.height + 1, `control vertically reachable: ${control.text}`, failures, JSON.stringify(control));
      check(control.height >= 40, `control touch height: ${control.text}`, failures, `${control.height}px`);
    }

    await page.evaluate(() => {
      window.__artSlideMutations = 0;
      const slides = document.querySelectorAll('.slide');
      window.__artSlideObserver = new MutationObserver((records) => {
        window.__artSlideMutations += records.filter((record) => record.attributeName === 'class').length;
      });
      slides.forEach((slide) => window.__artSlideObserver.observe(slide, { attributes: true, attributeFilter: ['class'] }));
    });
    const next = page.locator('.controls button').filter({ hasText: 'Next' }).first();
    const previous = page.locator('.controls button').filter({ hasText: 'Previous' }).first();
    await next.click();
    await page.waitForTimeout(70);
    let nav = { ...(await slideState(page)), mutations: await page.evaluate(() => window.__artSlideMutations) };
    check(nav.activeIndex === 1 && nav.visibleCount === 1 && nav.activeClassCount === 1, 'pointer Next navigation works', failures, JSON.stringify(nav));
    await previous.click();
    await page.keyboard.press('ArrowRight');
    await page.waitForTimeout(70);
    nav = { ...(await slideState(page)), mutations: await page.evaluate(() => window.__artSlideMutations) };
    check(nav.activeIndex === 1 && nav.visibleCount === 1 && nav.activeClassCount === 1, 'keyboard navigation works', failures, JSON.stringify(nav));
    check(nav.mutations < 30, 'slide lifecycle does not recurse', failures, `${nav.mutations} mutations`);
    const beforeIdle = nav.mutations;
    await page.waitForTimeout(220);
    const afterIdle = await page.evaluate(() => window.__artSlideMutations);
    check(afterIdle - beforeIdle <= 2, 'slide lifecycle settles when idle', failures, `${afterIdle - beforeIdle} idle mutations`);
  }

  const eventProblems = [...events.pageErrors, ...events.consoleErrors, ...events.failedRequests, ...events.badResponses];
  eventProblems.forEach((problem) => failures.push(`browser event: ${problem}`));
}

async function deepLesson(page, file, baseUrl, failures) {
  const origin = baseUrl ? new URL(baseUrl).origin : '';
  const events = recorder(page, origin);
  await page.goto(urlFor(file, baseUrl), { waitUntil: 'load', timeout: 30000 });
  await page.waitForTimeout(160);

  const total = await page.locator('.slide').count();
  for (let index = 1; index < total; index += 1) {
    await page.locator('.controls button').filter({ hasText: 'Next' }).first().click();
    await page.waitForTimeout(18);
  }
  const atEnd = {
    ...(await slideState(page)),
    progress: await page.evaluate(() => document.getElementById('progressBar') ? document.getElementById('progressBar').style.width : ''),
  };
  check(atEnd.activeIndex === total - 1 && atEnd.visibleCount === 1 && atEnd.activeClassCount === 1, 'full forward navigation reaches last slide', failures, JSON.stringify(atEnd));
  check(atEnd.progress === '100%', 'authored progress reaches 100%', failures, atEnd.progress);
  for (let index = total - 1; index > 0; index -= 1) {
    await page.locator('.controls button').filter({ hasText: 'Previous' }).first().click();
    await page.waitForTimeout(12);
  }
  const backAtStart = await slideState(page);
  check(backAtStart.activeIndex === 0 && backAtStart.visibleCount === 1 && backAtStart.activeClassCount === 1, 'full backward navigation returns to first slide', failures, JSON.stringify(backAtStart));

  const presentationIndex = await page.evaluate(() => [...document.querySelectorAll('.slide')].findIndex((slide) => slide.querySelector('.pres-card')));
  check(presentationIndex >= 0, 'presentation-card activity exists', failures);
  if (presentationIndex >= 0) {
    await moveToSlide(page, presentationIndex);
    await page.evaluate(() => window.presReset());
    await page.waitForTimeout(80);
    const pick = page.locator('.slide.active .at-random-pick');
    check((await pick.count()) === 1, 'teacher random card picker exists once', failures, String(await pick.count()));
    if (await pick.count()) {
      await pick.click();
      const picked = await page.evaluate(() => ({ picked: document.querySelectorAll('.slide.active .pres-card.at-picked').length, done: document.querySelectorAll('.slide.active .pres-card.done').length }));
      check(picked.picked === 1 && picked.done === 0, 'random picker focuses without revealing', failures, JSON.stringify(picked));
    }
    const firstCard = page.locator('.slide.active .pres-card').first();
    await firstCard.focus();
    await page.keyboard.press('Enter');
    await page.waitForTimeout(60);
    const presentation = await page.evaluate(() => ({
      done: document.querySelectorAll('.slide.active .pres-card.done').length,
      now: document.querySelector('.slide.active .at-activity-bar[data-at-activity="presentation"] .at-activity-track')?.getAttribute('aria-valuenow'),
      pressed: document.querySelector('.slide.active .pres-card')?.getAttribute('aria-pressed'),
    }));
    check(presentation.done === 1 && presentation.now === '1' && presentation.pressed === 'true', 'presentation activity follows authored state', failures, JSON.stringify(presentation));
    await page.evaluate(() => window.presReset());
  }

  const matchingIndex = await page.evaluate(() => [...document.querySelectorAll('.slide')].findIndex((slide) => slide.querySelector('.match-pill') && slide.querySelector('.match-target')));
  check(matchingIndex >= 0, 'matching activity exists', failures);
  if (matchingIndex >= 0) {
    await moveToSlide(page, matchingIndex);
    await page.evaluate(() => window.resetMatch());
    await page.waitForTimeout(60);
    const match = await page.evaluate(() => {
      const slide = document.querySelector('.slide.active');
      const pill = slide.querySelector('.match-pill');
      const raw = pill.getAttribute('onclick') || '';
      const id = (raw.match(/selectKW\s*\(\s*this\s*,\s*['"]([^'"]+)['"]/i) || [])[1];
      window.selectKW(pill, id);
      const target = [...slide.querySelectorAll('.match-target')].find((item) => item.getAttribute('data-correct') === id);
      window.pickTarget(target);
      return { id, hasTarget: !!target };
    });
    check(match.id && match.hasTarget, 'matching control finds authored pair', failures, JSON.stringify(match));
    await page.waitForTimeout(80);
    let matching = await page.evaluate(() => ({
      correct: document.querySelectorAll('.slide.active .match-target.correct').length,
      now: document.querySelector('.slide.active .at-activity-bar[data-at-activity="matching"] .at-activity-track')?.getAttribute('aria-valuenow'),
      chips: document.querySelectorAll('.slide.active .at-pair-chip').length,
      hidden: document.querySelector('.slide.active .at-pair-trail')?.hidden,
    }));
    check(matching.correct === 1 && matching.now === '1' && matching.chips === 1 && matching.hidden === false, 'correct pair updates progress and trail', failures, JSON.stringify(matching));
    await page.evaluate(() => window.revealMatch());
    await page.waitForTimeout(70);
    matching = await page.evaluate(() => ({
      correct: document.querySelectorAll('.slide.active .match-target.correct').length,
      total: document.querySelectorAll('.slide.active .match-target').length,
      chips: document.querySelectorAll('.slide.active .at-pair-chip').length,
    }));
    check(matching.correct === matching.total && matching.chips === matching.total, 'reveal keeps completed connections synchronised', failures, JSON.stringify(matching));
    await page.evaluate(() => window.resetMatch());
    await page.waitForTimeout(70);
    matching = await page.evaluate(() => ({
      correct: document.querySelectorAll('.slide.active .match-target.correct').length,
      now: document.querySelector('.slide.active .at-activity-bar[data-at-activity="matching"] .at-activity-track')?.getAttribute('aria-valuenow'),
      chips: document.querySelectorAll('.slide.active .at-pair-chip').length,
    }));
    check(matching.correct === 0 && matching.now === '0' && matching.chips === 0, 'matching reset clears shared state', failures, JSON.stringify(matching));
  }

  const stepIndex = await page.evaluate(() => [...document.querySelectorAll('.slide')].findIndex((slide) => slide.querySelector('.v5-step-controls button')));
  if (stepIndex >= 0) {
    await moveToSlide(page, stepIndex);
    await page.locator('.slide.active .v5-step-controls button').click();
    const step = await page.evaluate(() => ({
      revealed: document.querySelectorAll('.slide.active .v5-step.revealed').length,
      current: document.querySelectorAll('.slide.active .v5-step.at-step-current').length,
      pips: document.querySelectorAll('.slide.active .v5-step-pips i.on').length,
    }));
    check(step.revealed >= 1 && step.current === 1 && step.pips === step.revealed, 'step reveal marker and pips track authored sequence', failures, JSON.stringify(step));
  }

  const illuminatorIndex = await page.evaluate(() => [...document.querySelectorAll('.slide')].findIndex((slide) => slide.querySelector('.ilm')));
  if (illuminatorIndex >= 0) {
    await moveToSlide(page, illuminatorIndex);
    await page.waitForTimeout(80);
    const replay = page.locator('.slide.active .ilm-replay');
    check((await replay.count()) === 1, 'diagram replay control exists exactly once', failures, String(await replay.count()));
    if (await replay.count()) {
      await replay.click();
      check(await page.locator('.slide.active .ilm.at-ilm-replaying').count() === 1, 'diagram replay restarts from controlled state', failures);
    }
    await page.locator('.controls button').filter({ hasText: 'Next' }).first().click();
    const paused = await page.evaluate(() => {
      const ilm = document.querySelector('.slide:not(.active) .ilm');
      if (!ilm) return true;
      const animated = [...ilm.querySelectorAll('*')].find((el) => getComputedStyle(el).animationName !== 'none');
      return !animated || getComputedStyle(animated).animationPlayState === 'paused';
    });
    check(paused, 'inactive-slide motion is paused', failures);
  }

  const timer = await page.evaluate(async () => {
    if (typeof window.startTimer !== 'function') return null;
    const initial = document.getElementById('timerDisplay')?.textContent || '';
    window.startTimer();
    await new Promise((resolve) => setTimeout(resolve, 1100));
    const display = document.getElementById('timerDisplay')?.textContent || '';
    window.pauseTimer();
    window.resetTimer();
    const reset = document.getElementById('timerDisplay')?.textContent || '';
    return { initial, display, reset };
  });
  if (timer) check(
    /^\d\d:\d\d$/.test(timer.initial)
      && /^\d\d:\d\d$/.test(timer.display)
      && timer.display !== timer.initial
      && timer.reset === timer.initial,
    'authored timer runs and resets',
    failures,
    JSON.stringify(timer),
  );

  const modals = await page.evaluate(() => {
    localStorage.setItem('mbm_cc_v1', JSON.stringify([{ n: 'Regression Learner', g: '2' }]));
    window.showTABrief();
    const ta = document.getElementById('ta-modal')?.classList.contains('visible') === true;
    document.getElementById('ta-modal')?.classList.remove('visible');
    window.showColdCall();
    const cold = document.getElementById('cc-modal')?.classList.contains('visible') === true;
    const name = document.getElementById('cc-name')?.textContent || '';
    document.getElementById('cc-modal')?.classList.remove('visible');
    localStorage.removeItem('mbm_cc_v1');
    return { ta, cold, name };
  });
  check(modals.ta && modals.cold && modals.name === 'Regression Learner', 'TA brief and seeded random cold-call controls open', failures, JSON.stringify(modals));

  const printState = await page.evaluate(() => {
    const generated = [...document.querySelectorAll('.at-activity-bar,.at-pair-trail,.ilm-replay')];
    return { generated: generated.length };
  });
  await page.emulateMedia({ media: 'print' });
  const printHidden = await page.evaluate(() => [...document.querySelectorAll('.at-activity-bar,.at-pair-trail,.ilm-replay')].every((el) => getComputedStyle(el).display === 'none'));
  check(printState.generated > 0 && printHidden, 'print mode suppresses generated interaction chrome', failures, JSON.stringify(printState));
  await page.emulateMedia({ media: 'screen' });

  const eventProblems = [...events.pageErrors, ...events.consoleErrors, ...events.failedRequests, ...events.badResponses];
  eventProblems.forEach((problem) => failures.push(`browser event: ${problem}`));
}

async function reducedMotionCheck(browser, file, baseUrl, failures) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, reducedMotion: 'reduce' });
  const origin = baseUrl ? new URL(baseUrl).origin : '';
  const events = recorder(page, origin);
  await page.goto(urlFor(file, baseUrl), { waitUntil: 'load', timeout: 30000 });
  await page.waitForTimeout(120);
  const illuminatorIndex = await page.evaluate(() => [...document.querySelectorAll('.slide')].findIndex((slide) => slide.querySelector('.ilm')));
  if (illuminatorIndex >= 0) await moveToSlide(page, illuminatorIndex);
  const result = await page.evaluate(() => {
    const active = document.querySelector('.slide.active');
    const visibleText = active && active.getBoundingClientRect().height > 0 && getComputedStyle(active).visibility !== 'hidden';
    const sweep = active?.querySelector('.at-ilm-sweep');
    const animations = active ? [...active.querySelectorAll('*')].filter((el) => getComputedStyle(el).animationName !== 'none') : [];
    return {
      visibleText: !!visibleText,
      sweepHidden: !sweep || getComputedStyle(sweep).display === 'none' || getComputedStyle(sweep).animationName === 'none',
      moving: animations.filter((el) => getComputedStyle(el).animationPlayState === 'running' && parseFloat(getComputedStyle(el).animationDuration) > 0).length,
    };
  });
  check(result.visibleText && result.sweepHidden && result.moving === 0, 'reduced-motion keeps content visible and suppresses non-essential motion', failures, JSON.stringify(result));
  [...events.pageErrors, ...events.consoleErrors, ...events.failedRequests, ...events.badResponses].forEach((problem) => failures.push(`reduced-motion browser event: ${problem}`));
  await page.close();
}

async function selfTest(browser) {
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  const events = recorder(page, '');
  await page.setContent('<!doctype html><meta charset="utf-8"><script>console.error("deliberate control")<\/script><div id="wide" style="width:5000px">control</div>');
  await page.waitForTimeout(20);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 4);
  const browserSignals = overflow && events.consoleErrors.some((entry) => entry.includes('deliberate control'));
  console.log(`CONTROL browser console + overflow: ${browserSignals ? 'DETECTED' : 'MISSED'}`);

  await page.setContent(`<!doctype html><meta charset="utf-8">
    <style>.slide{display:none}.slide.active{display:block}</style>
    <section class="slide active">one</section><section class="slide">two</section>
    <div class="controls"><button onclick="nextSlide()">Next</button><button onclick="prevSlide()">Previous</button></div>
    <script>let currentSlide=0;const slides=document.querySelectorAll('.slide');function showSlide(i){slides.forEach((s,j)=>s.classList.toggle('active',j===i))}function nextSlide(){if(currentSlide<slides.length-1){currentSlide++;showSlide(currentSlide)}}function prevSlide(){if(currentSlide>0){currentSlide--;showSlide(currentSlide)}}<\/script>`);
  await page.locator('.controls button').filter({ hasText: 'Next' }).click();
  const lexical = await slideState(page);
  const lexicalDetected = lexical.activeIndex === 1 && lexical.visibleCount === 1 && lexical.activeClassCount === 1
    && await page.evaluate(() => typeof window.currentSlide === 'undefined');
  console.log(`CONTROL lexical slide state via rendered DOM: ${lexicalDetected ? 'DETECTED' : 'MISSED'}`);

  await page.setContent(`<!doctype html><meta charset="utf-8">
    <a class="art-skip-link" href="#primary">Skip</a>
    <div class="grid" id="primary"><a class="art-card-enter" aria-label="One"></a><a class="art-card-enter" aria-label="Two"></a></div>
    <div class="grid"><a></a><a></a><a></a></div>`);
  const hub = await hubState(page);
  const hubScoped = hub.cards === 2 && hub.animated === 2 && hub.labelled === 2 && hub.skipHref === '#primary';
  console.log(`CONTROL scoped primary hub-card census: ${hubScoped ? 'DETECTED' : 'MISSED'}`);
  await page.close();
  return browserSignals && lexicalDetected && hubScoped;
}

(async () => {
  const options = parseArgs(process.argv.slice(2));
  const executablePath = process.env.ART_CHROMIUM_EXECUTABLE || undefined;
  const browser = await chromium.launch(executablePath ? { executablePath } : {});
  if (options.selfTest) {
    const ok = await selfTest(browser);
    await browser.close();
    process.exit(ok ? 0 : 1);
  }

  const lessons = walk(ART).filter((file) => file.endsWith('.html') && LESSON_RE.test(path.basename(file))).sort();
  const hubs = [path.join(REPO, 'art_teesside.html'), ...['Build', 'Grow', 'Launch'].map((strand) => path.join(ART, strand, 'START_HERE.html'))].sort();
  if (lessons.length !== 31 || hubs.length !== 4) throw new Error(`population mismatch lessons=${lessons.length} hubs=${hubs.length}`);
  fs.mkdirSync(options.screenshotDir, { recursive: true });
  const results = [];

  for (const file of [...hubs, ...lessons]) {
    for (const viewport of VIEWPORTS) {
      const page = await browser.newPage({ viewport });
      const failures = [];
      try {
        await smoke(page, file, viewport, options.baseUrl, failures);
      } catch (error) {
        failures.push(`uncaught smoke exception: ${error && error.stack ? error.stack : error}`);
      }
      if (failures.length) {
        const shot = `${rel(file).replace(/[^a-z0-9]+/gi, '_')}-${viewport.width}x${viewport.height}.png`;
        try { await page.screenshot({ path: path.join(options.screenshotDir, shot), fullPage: true }); } catch (_) {}
      }
      const result = { file: rel(file), phase: 'viewport-smoke', viewport, failures };
      results.push(result);
      console.log(`${failures.length ? 'FAIL' : 'PASS'} ${result.file} ${viewport.width}x${viewport.height}${failures.length ? ` — ${failures.join(' | ')}` : ''}`);
      await page.close();
    }
  }

  for (const file of lessons) {
    const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
    const failures = [];
    try {
      await deepLesson(page, file, options.baseUrl, failures);
    } catch (error) {
      failures.push(`uncaught deep exception: ${error && error.stack ? error.stack : error}`);
    }
    if (failures.length) {
      const shot = `${rel(file).replace(/[^a-z0-9]+/gi, '_')}-deep.png`;
      try { await page.screenshot({ path: path.join(options.screenshotDir, shot), fullPage: true }); } catch (_) {}
    }
    const result = { file: rel(file), phase: 'deep-interaction', viewport: { width: 1280, height: 720 }, failures };
    results.push(result);
    console.log(`${failures.length ? 'FAIL' : 'PASS'} ${result.file} deep${failures.length ? ` — ${failures.join(' | ')}` : ''}`);
    await page.close();
  }

  for (const file of [lessons.find((file) => file.includes('/Build/BUILD_ART_W1_')), lessons.find((file) => file.includes('/Grow/GROW_ART_W1_')), lessons.find((file) => file.includes('/Launch/LAUNCH_ART_W1_'))].filter(Boolean)) {
    const failures = [];
    try { await reducedMotionCheck(browser, file, options.baseUrl, failures); }
    catch (error) { failures.push(`uncaught reduced-motion exception: ${error && error.stack ? error.stack : error}`); }
    const result = { file: rel(file), phase: 'reduced-motion', viewport: { width: 1280, height: 720 }, failures };
    results.push(result);
    console.log(`${failures.length ? 'FAIL' : 'PASS'} ${result.file} reduced-motion${failures.length ? ` — ${failures.join(' | ')}` : ''}`);
  }

  await browser.close();
  const failures = results.filter((result) => result.failures.length);
  fs.writeFileSync(options.report, `${JSON.stringify({ generatedAt: new Date().toISOString(), lessons: lessons.map(rel), hubs: hubs.map(rel), viewports: VIEWPORTS, results, failureCount: failures.length }, null, 2)}\n`);
  console.log(`\nART BROWSER ASSERTION ${failures.length ? 'FAILED' : 'PASS'} — ${results.length} checks, ${failures.length} failed`);
  process.exit(failures.length ? 1 : 0);
})().catch((error) => {
  console.error(error && error.stack ? error.stack : error);
  process.exit(1);
});
