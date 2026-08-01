/* Functional smoke test for a BUILD_ASDAN lesson deck.
   Exercises the interactions teachers rely on and reports anything broken. */
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const files = process.argv.slice(2);
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  });
  let failures = 0;

  for (const file of files) {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    const errs = [];
    page.on('pageerror', (e) => errs.push('JS ERROR: ' + e.message));
    page.on('console', (m) => {
      const t = m.text();
      if (m.type() === 'error' && !t.includes('hud.js') && !t.includes('ERR_FILE_NOT_FOUND'))
        errs.push('CONSOLE: ' + t);
    });

    await page.goto('file://' + path.resolve(file));
    await page.waitForTimeout(400);
    const checks = [];
    const ok = (name, val) => checks.push([name, !!val]);

    // --- navigation through every slide, forwards then back
    const total = await page.evaluate(() => document.querySelectorAll('.slide').length);
    // The documented invocation is `*/[A-Z]*.html`, which also matches each
    // strand's START_HERE page. Those are not decks and have no deck script,
    // so every assertion below would throw rather than fail. Skip them.
    if (!total) {
      console.log(`SKIP  ${path.basename(file)}  (not a lesson deck)`);
      await page.close();
      continue;
    }
    ok('10 slides', total === 10);
    for (let i = 1; i < total; i++) await page.evaluate(() => nextSlide());
    ok('advances to last slide', (await page.evaluate(() => currentSlide)) === total - 1);
    ok(
      'progress bar tracks',
      (await page.evaluate(() => document.getElementById('progressBar').style.width)) === '100%'
    );
    for (let i = 0; i < total; i++) await page.evaluate(() => prevSlide());
    ok('returns to first slide', (await page.evaluate(() => currentSlide)) === 0);

    // --- keyboard navigation
    await page.keyboard.press('ArrowRight');
    ok('ArrowRight advances', (await page.evaluate(() => currentSlide)) === 1);
    await page.keyboard.press('ArrowLeft');
    ok('ArrowLeft goes back', (await page.evaluate(() => currentSlide)) === 0);

    // --- differentiation level toggles
    await page.evaluate(() => switchLevel('arrival', 'stretch'));
    ok(
      'level toggle switches',
      (await page.evaluate(
        () => document.getElementById('arrival-stretch').style.display === 'grid'
      ))
    );

    // --- We Do 1: tap-to-reveal cards
    const presBefore = await page.evaluate(
      () => document.querySelectorAll('.pres-card').length
    );
    await page.evaluate(() => {
      const c = document.querySelector('.pres-card');
      if (c) presTap(c);
    });
    ok('pres card reveals a caption', (await page.evaluate(
      () => document.querySelectorAll('#pres-caps .pres-cap').length
    )) === 1);
    await page.evaluate(() => presReset());
    ok('pres reset clears', (await page.evaluate(
      () => document.getElementById('pres-num').textContent
    )) === '0');
    ok('pres cards present', presBefore > 0);

    // --- We Do 2: match game scoring, wrong answer, reveal, reset
    await page.evaluate(() => {
      const pill = document.querySelector('#kw-pills .match-pill');
      selectKW(pill, pill.getAttribute('onclick').match(/'(m\d)'/)[1]);
      const right = [...document.querySelectorAll('#wedo2 .match-target')].find(
        (t) => t.getAttribute('data-correct') === selectedKWId
      );
      pickTarget(right);
    });
    ok('match scores a correct pair', (await page.evaluate(
      () => document.getElementById('match-score').textContent
    )) === '1');
    await page.evaluate(() => revealMatch());
    ok('reveal marks all correct', (await page.evaluate(
      () =>
        document.querySelectorAll('#wedo2 .match-target.correct').length ===
        document.querySelectorAll('#wedo2 .match-target').length
    )));
    await page.evaluate(() => resetMatch());
    ok('match reset clears', (await page.evaluate(
      () => document.querySelectorAll('#wedo2 .match-target.correct').length
    )) === 0);

    // --- I Do step reveal
    await page.evaluate(() => {
      const s = [...document.querySelectorAll('.slide')].find((x) =>
        x.querySelector('.v5-step-controls')
      );
      s.querySelector('.v5-step-controls button').click();
    });
    ok('I Do step reveals', (await page.evaluate(
      () => document.querySelectorAll('.v5-step.revealed').length
    )) >= 1);

    // --- the step build: marker tracks the newest step, pips track the count
    const build = await page.evaluate(() => {
      const slide = [...document.querySelectorAll('.slide')].find((x) =>
        x.querySelector('.v5-step-controls')
      );
      const group = slide.querySelector('.v5-steps');
      const btn = slide.querySelector('.v5-step-controls button');
      const pips = slide.querySelector('.v5-step-pips');
      const steps = [...group.querySelectorAll('.v5-step')];
      // The check above already revealed one, so the walk starts from there.
      const from = group.querySelectorAll('.v5-step.revealed').length;
      const seen = [];
      while (group.querySelector('.v5-step:not(.revealed)')) {
        btn.click();
        const cur = group.querySelector('.v5-step.at-step-current');
        seen.push({
          at: cur ? steps.indexOf(cur) : -1,
          lit: pips ? [...pips.children].filter((p) => p.classList.contains('on')).length : -1,
        });
      }
      return { seen, from, pips: pips ? pips.children.length : 0, steps: steps.length };
    });
    ok('one pip per step', build.pips === build.steps);
    ok(
      'current-step marker follows the reveal',
      build.seen.length > 0 &&
        build.seen.every((s, i) => s.at === build.from + i && s.lit === build.from + i + 1)
    );

    // --- the illuminator: every draw path measured, labels held for their shape
    const ilm = await page.evaluate(() => {
      const i = [...document.querySelectorAll('.slide')].findIndex((s) => s.querySelector('.ilm'));
      if (i < 0) return null;
      currentSlide = i;
      showSlide(i);
      const svg = document.querySelector('.slide.active .ilm svg');
      const draws = [...svg.querySelectorAll('.draw')];
      return {
        draws: draws.length,
        measured: draws.filter(
          (e) => e.classList.contains('at-drawn') && parseFloat(e.style.getPropertyValue('--at-len')) > 0
        ).length,
        // A label held past the build must still end up visible.
        stranded: [...svg.querySelectorAll('text.at-ilm-label')].filter(
          (t) => !parseFloat(t.style.getPropertyValue('--at-lab-delay'))
        ).length,
      };
    });
    ok('draw paths measured to their own length', !ilm || ilm.measured === ilm.draws);
    ok('no label held with no delay to wait for', !ilm || ilm.stranded === 0);

    // --- independent work timer
    await page.evaluate(() => { startTimer(); });
    await page.waitForTimeout(1200);
    const running = await page.evaluate(() => timerRunning);
    await page.evaluate(() => { pauseTimer(); resetTimer(); });
    ok('independent timer runs', running === true);
    ok('timer resets', (await page.evaluate(
      () => document.getElementById('timerDisplay').textContent
    )).match(/^\d\d:\d\d$/) !== null);

    // --- auto timer (per-slide, data-timer)
    ok('auto timer shows a value', (await page.evaluate(
      () => document.getElementById('auto-timer-display').textContent
    )).match(/^\d\d:\d\d$/) !== null);

    // --- teacher modals
    await page.evaluate(() => showTABrief());
    ok('TA brief opens', await page.evaluate(
      () => document.getElementById('ta-modal').classList.contains('visible')
    ));
    await page.keyboard.press('Escape');
    ok('Escape closes modal', !(await page.evaluate(
      () => document.getElementById('ta-modal').classList.contains('visible')
    )));

    // --- WAGOLL typer
    await page.evaluate(() => skipWagoll());
    ok('WAGOLL renders full text', (await page.evaluate(
      () => (document.getElementById('wagoll-text') || {}).textContent || ''
    )).length > 40);

    // --- print pack wiring (no window.print, just the class plumbing)
    await page.evaluate(() => {
      document.body.classList.remove('print-supported', 'print-standard', 'print-stretch');
      document.querySelectorAll('.print-section').forEach((e) => e.classList.remove('visible'));
      ['ko', 'intro', 'arrival', 'starter', 'wedo', 'exit', 'witness', 'feedback'].forEach((id) => {
        const el = document.getElementById('print-' + id);
        if (el) el.classList.add('visible');
      });
    });
    ok('print sections resolve', (await page.evaluate(
      () => document.querySelectorAll('.print-section.visible').length
    )) >= 8);

    // --- the framework itself
    ok('framework loaded', await page.evaluate(() => !!window.ASDANTeach));

    const bad = checks.filter(([, v]) => !v);
    const status = bad.length === 0 && errs.length === 0 ? 'PASS' : 'FAIL';
    if (status === 'FAIL') failures++;
    console.log(`${status}  ${path.basename(file)}  (${checks.length} checks)`);
    bad.forEach(([n]) => console.log(`         ✗ ${n}`));
    errs.forEach((e) => console.log(`         ✗ ${e}`));
    await page.close();
  }

  await browser.close();
  process.exit(failures ? 1 : 0);
})();
