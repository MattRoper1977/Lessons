/* Prove every illuminator label is readable AT REST.
 *
 *   node _framework/label_rest_check.js <strand>/[A-Z]*.html
 *
 * A label whose legibility depends on an animation completing is a gate
 * released by something that never happens. It is the same defect as a reveal
 * that never fires, wearing different clothes, and it hides most easily on the
 * decks whose diagrams animate continuously — there is no "after the build"
 * for a loop, so a label caught inside one is invisible on a schedule.
 *
 * Two conditions, per the house standard:
 *
 *   AT REST      effective opacity >= 1 and non-zero size, sampled right across
 *                a full animation cycle rather than at two convenient instants.
 *                Sampling at 0.3s and 3.0s passes a label that is invisible at
 *                1.7s, which is exactly the case this exists to catch.
 *
 *   REDUCED      under prefers-reduced-motion the scene must be complete and
 *   MOTION       labelled and static: animation resolved, opacity 1, and any
 *                dash offset at 0 so a drawn line is drawn.
 *
 * Effective opacity is the product down the ancestor chain — a text at
 * opacity 1 inside a group fading to 0 is invisible, and reading the element
 * alone says it is fine.
 *
 * Exits non-zero if any label fails, so it can gate.
 */
const { chromium } = require('playwright');
const path = require('path');

const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const CYCLE_MS = 6000; // longest loop in the suite is 5.5s (ilmRide)
const STEP_MS = 150;
/* "At rest" means after the slide has arrived, not from the instant it is
   asked for. The deck fades each slide's children in on entry, so sampling
   from t=0 catches every label of every deck at opacity 0 — a one-off arrival
   transient, not a label whose legibility depends on a loop. Settle past it
   first, and past the longest finite illuminator build (measured 4.4s), so
   what is sampled is genuinely the resting state. */
const SETTLE_MS = 5000;

(async () => {
  const files = process.argv.slice(2).filter((a) => !a.startsWith('--'));
  if (!files.length) {
    console.error('usage: label_rest_check.js <files...>');
    process.exit(2);
  }

  const browser = await chromium.launch({ executablePath: CHROME });
  let failed = 0;

  for (const file of files) {
    const name = path.basename(file);

    /* ---- AT REST, motion on, sampled across a whole cycle ---- */
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto('file://' + path.resolve(file));
    await page.waitForTimeout(200);
    const onSlide = await page.evaluate(() => {
      const i = [...document.querySelectorAll('.slide')].findIndex((s) => s.querySelector('.ilm'));
      if (i < 0) return false;
      currentSlide = i;
      showSlide(i);
      return true;
    });
    if (!onSlide) {
      console.log(`SKIP  ${name}  (no illuminator)`);
      await page.close();
      continue;
    }

    const samples = await page.evaluate(
      async ({ cycle, step, settle }) => {
        await new Promise((r) => setTimeout(r, settle));
        const svg = document.querySelector('.slide.active .ilm svg');
        /* A glyph riding inside a travelling token is not a label. COMM_W4's
           diagram is described by its own aria-label as "a message flies from
           the team to the partner and a reply returns" — the tick is the reply
           in flight, and fading as it lands is the animation, not a legibility
           failure. The meaning is carried by the static labels around it.
           Exemptions are reported, never silently skipped: a gate that goes
           red for something nobody will ever fix trains people to ignore it. */
        const carried = (el) => {
          for (let cur = el; cur && cur !== svg; cur = cur.parentNode) {
            if (cur.nodeType !== 1) break;
            if (cur.classList && cur.classList.contains('ride')) return true;
          }
          return false;
        };
        const labels = [...svg.querySelectorAll('text')];
        const state = labels.map((t) => ({
          text: (t.textContent || '').trim().slice(0, 22),
          exempt: carried(t) ? 'token in transit' : null,
          minOpacity: 1,
          minW: Infinity,
          minH: Infinity,
          atWorst: 0,
        }));
        const effective = (el) => {
          let o = 1;
          for (let cur = el; cur && cur !== document; cur = cur.parentNode) {
            if (cur.nodeType !== 1) break;
            o *= parseFloat(getComputedStyle(cur).opacity);
          }
          return o;
        };
        for (let t = 0; t <= cycle; t += step) {
          labels.forEach((el, k) => {
            const o = effective(el);
            const r = el.getBoundingClientRect();
            if (o < state[k].minOpacity) {
              state[k].minOpacity = o;
              state[k].atWorst = t;
            }
            state[k].minW = Math.min(state[k].minW, r.width);
            state[k].minH = Math.min(state[k].minH, r.height);
          });
          await new Promise((r) => setTimeout(r, step));
        }
        return state;
      },
      { cycle: CYCLE_MS, step: STEP_MS, settle: SETTLE_MS }
    );
    await page.close();

    /* ---- REDUCED MOTION: the scene must be complete and static ---- */
    const rmPage = await browser.newPage({
      viewport: { width: 1440, height: 900 },
      reducedMotion: 'reduce',
    });
    await rmPage.goto('file://' + path.resolve(file));
    await rmPage.waitForTimeout(200);
    await rmPage.evaluate(() => {
      const i = [...document.querySelectorAll('.slide')].findIndex((s) => s.querySelector('.ilm'));
      currentSlide = i;
      showSlide(i);
    });
    await rmPage.waitForTimeout(SETTLE_MS);
    const rm = await rmPage.evaluate(() => {
      const svg = document.querySelector('.slide.active .ilm svg');
      const effective = (el) => {
        let o = 1;
        for (let cur = el; cur && cur.nodeType === 1; cur = cur.parentNode) {
          o *= parseFloat(getComputedStyle(cur).opacity);
        }
        return o;
      };
      return {
        labels: [...svg.querySelectorAll('text')].map((t) => ({
          text: (t.textContent || '').trim().slice(0, 22),
          opacity: +effective(t).toFixed(3),
          w: Math.round(t.getBoundingClientRect().width),
          h: Math.round(t.getBoundingClientRect().height),
        })),
        // A drawn line under reduced motion must be drawn, not held at its
        // start offset.
        strokes: [...svg.querySelectorAll('*')]
          .filter((e) => getComputedStyle(e).strokeDasharray !== 'none')
          .map((e) => ({
            dash: getComputedStyle(e).strokeDasharray,
            offset: getComputedStyle(e).strokeDashoffset,
          })),
        stillAnimating: [...svg.querySelectorAll('*')].filter(
          (e) => e.getAnimations && e.getAnimations().length
        ).length,
      };
    });
    await rmPage.close();

    const exempt = samples.filter((s) => s.exempt);
    const restBad = samples.filter(
      (s) => !s.exempt && (s.minOpacity < 1 || s.minW <= 0 || s.minH <= 0)
    );
    // Under reduced motion nothing is in transit, so every glyph — tokens
    // included — must be present in the static scene. No exemption here.
    const rmBad = rm.labels.filter((l) => l.opacity < 1 || !l.w || !l.h);
    const strokeBad = rm.strokes.filter((s) => parseFloat(s.offset) !== 0);
    const ok = !restBad.length && !rmBad.length && !strokeBad.length;
    if (!ok) failed++;

    console.log(
      `${ok ? 'PASS' : 'FAIL'}  ${name.padEnd(42)} ${samples.length} labels · ` +
        `at rest min opacity ${Math.min(...samples.filter((s) => !s.exempt).map((s) => s.minOpacity), 1).toFixed(2)} · ` +
        `reduced-motion min ${Math.min(...rm.labels.map((l) => l.opacity)).toFixed(2)} · ` +
        `dashed strokes ${rm.strokes.length} all at offset 0: ${!strokeBad.length}`
    );
    exempt.forEach((s) =>
      console.log(
        `        · exempt "${s.text}" — ${s.exempt}; drops to ${s.minOpacity.toFixed(2)} at ` +
          `${s.atWorst}ms by design, meaning carried by the static labels`
      )
    );
    restBad.forEach((s) =>
      console.log(
        `        ✗ at rest "${s.text}" drops to opacity ${s.minOpacity.toFixed(2)} at ${s.atWorst}ms`
      )
    );
    rmBad.forEach((l) =>
      console.log(`        ✗ reduced motion "${l.text}" opacity ${l.opacity} size ${l.w}x${l.h}`)
    );
    strokeBad.forEach((s) => console.log(`        ✗ reduced motion stroke left at offset ${s.offset}`));
  }

  await browser.close();
  process.exit(failed ? 1 : 0);
})();
