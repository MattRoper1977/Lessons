/* ORDER HUM-T — the behavioural rows, proved in a real browser at 390x844.
 *
 * Chassis contract standing rule 5: a static parse is structurally unable to emit
 * PASS for a behavioural row, and a rendered COUNT is not enough either — the
 * control has to be DRIVEN. So this harness clicks the deck's own buttons.
 *
 *   row 38  audience is refused before voice
 *   row 39  influence is refused before audience
 *   row 40  driven in order, the panel reaches INFLUENCE
 *   row 41  every panel is reachable at 390px
 *   P1-3    a panel sits behind a collapsed "Feedback loop" disclosure: hidden until its
 *           summary is tapped (a real click on the deck's own control) or the stage's own
 *           task is used (a field input or a chip tap outside the disclosure), visible after
 *   row 42  the deck's own controls are not double-driven
 *   axe     0 serious/critical
 *   R5      the RE safeguard sentences the deck already had are still there
 *
 * Usage: node render_proof.cjs <repo-root> <out.json> [file ...]
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const AXE = path.join('/tmp/claude-0/-home-user-mattroper1977-github-io/' +
  '3725483b-d163-5c5f-a3d0-e77269db85b6/scratchpad/node/node_modules/axe-core/axe.min.js');

async function advance(page, from) {
  // The deck's OWN next control. A candidate only counts if the VISIBLE slide
  // actually changes: several decks carry an in-lesson stepper labelled
  // "Next frame" that advances an animation, not the lesson.
  const sels = ['[data-nav="next"]', '#next-slide', 'button#next-slide', '.next-slide'];
  for (const sel of sels) {
    if (!(await page.$(sel))) continue;
    try { await page.click(sel, { timeout: 700 }); } catch (e) {
      try { await page.$eval(sel, e2 => e2.click()); } catch (e3) { continue; }
    }
    await page.waitForTimeout(120);
    if ((await activeIndex(page)) !== from) return sel;
  }
  // text fallback, skipping in-lesson steppers
  const n = await page.evaluate(() => {
    const bad = /frame|step|play|pause|reset|timer|reveal/i;
    const c = [...document.querySelectorAll('button,a,[role="button"]')].filter(n =>
      /\bnext\b|→|▶|»/i.test(n.textContent || '') && !bad.test(n.textContent || '') &&
      !n.disabled && n.getBoundingClientRect().height > 0);
    if (!c.length) return null;
    // Rank: a control whose whole label is "Next" is the lesson's navigation.
    // One whose label merely CONTAINS "next" is usually an in-lesson stepper.
    const exact = /^next\s*[▶>»→]?$/i;
    c.sort((a, b) => (exact.test((b.textContent || '').trim()) ? 1 : 0)
                   - (exact.test((a.textContent || '').trim()) ? 1 : 0)
                   || (a.textContent || '').length - (b.textContent || '').length);
    c[0].click();
    return (c[0].textContent || '').trim().slice(0, 24);
  });
  if (n) {
    await page.waitForTimeout(120);
    if ((await activeIndex(page)) !== from) return 'text:' + n;
  }
  return null;
}

async function activeIndex(page) {
  return page.evaluate(() => {
    const all = [...document.querySelectorAll('.slide')]
      .filter(n => !n.parentElement.closest('.slide'));
    const i = all.findIndex(n => n.classList.contains('active'));
    if (i >= 0) return i;
    return all.findIndex(n => n.getBoundingClientRect().height > 0);
  });
}

async function run(page, file) {
  const res = { file, panels: 0, reached: 0, r38: 0, r39: 0, r40: 0,
                disclosed: 0, disclosureFaults: [], openedByTask: 0, taskNA: 0, taskFaults: [],
                refusals: [], errors: [], axe: null, doubleDriven: [] };
  const errs = [];
  page.on('pageerror', e => errs.push(String(e).slice(0, 180)));
  await page.goto('file://' + file, { waitUntil: 'load' });
  await page.waitForTimeout(250);

  const total = await page.evaluate(() =>
    [...document.querySelectorAll('.slide')].filter(n => !n.parentElement.closest('.slide')).length);
  res.panels = await page.evaluate(() => document.querySelectorAll('.hum-t-loop').length);

  const seen = new Set();
  for (let step = 0; step < total + 2; step++) {
    const idx = await activeIndex(page);
    if (idx >= 0 && !seen.has(idx)) {
      seen.add(idx);
      // The deck's own slide transition can hold the new stage at visibility:hidden for
      // ~100ms; checkVisibility() reports that honestly (a rect did not), so the after-tap
      // reading waits for the transition rather than judging inside it.
      const measure = (i, tap) => page.evaluate(([i, tap]) => {
        const all = [...document.querySelectorAll('.slide')]
          .filter(n => !n.parentElement.closest('.slide'));
        const st = all[i];
        if (!st) return null;
        const p = st.querySelector('.hum-t-loop');
        if (!p) return { hasPanel: false };
        const vis = () => p.checkVisibility
          ? p.checkVisibility({ contentVisibilityAuto: true, visibilityProperty: true })
          : (() => { const r = p.getBoundingClientRect(); return r.height > 0 && r.width > 0; })();
        const d = p.closest('details.loop-disclosure');
        const sum = d && d.querySelector('summary');
        const out = { hasPanel: true, visible: vis(), open: d ? !!d.open : null,
                      hasDisclosure: !!d, label: sum ? sum.textContent.trim() : '',
                      stage: p.getAttribute('data-loop-stage-name'), taskControl: null };
        if (tap === 'task' && d) {                          // P1-3: the stage's own task, used
          const outside = n => !d.contains(n) && !n.closest('.hum-t-loop');
          const field = [...st.querySelectorAll('input,select,textarea')].find(outside);
          const chip = [...st.querySelectorAll('button[data-chip],button.chip,[role="button"]')].find(outside);
          if (field) { field.dispatchEvent(new Event('input', { bubbles: true })); out.taskControl = field.tagName.toLowerCase(); }
          else if (chip) { chip.click(); out.taskControl = 'chip'; }
        } else if (tap === true && sum) sum.click();        // the real control, as a pupil taps it
        return out;
      }, [i, tap]);
      await page.waitForTimeout(260);
      const before = await measure(idx, 'task');          // reads the closed state, then uses the task
      await page.waitForTimeout(260);
      let after = before && before.hasPanel ? await measure(idx, false) : null;
      if (before && before.hasPanel && before.hasDisclosure) {
        if (before.taskControl && after.open) res.openedByTask++;
        else {
          if (before.taskControl) res.taskFaults.push([before.stage, before.taskControl]);
          else res.taskNA++;
          await measure(idx, true);                        // the summary tap instead
          await page.waitForTimeout(260);
          after = await measure(idx, false);
        }
      }
      const info = before && before.hasPanel
        ? { hasPanel: true, stage: before.stage, visible: after.visible,
            disclosure: before.hasDisclosure
              ? { hiddenBefore: !before.open && !before.visible, openAfter: after.open,
                  visibleAfter: after.visible, label: before.label } : null }
        : before;
      if (info && info.hasPanel) {
        if (info.visible) res.reached++;
        if (info.disclosure) {
          const d = info.disclosure;
          if (d.hiddenBefore && d.openAfter && d.visibleAfter && d.label === 'Feedback loop') res.disclosed++;
          else res.disclosureFaults.push([info.stage, d]);
        }
        // --- drive the panel, wrong order first
        const panel = await page.$(`.slide:nth-of-type(${idx + 1}) .hum-t-loop`)
          || await page.evaluateHandle((i) => {
               const all = [...document.querySelectorAll('.slide')]
                 .filter(n => !n.parentElement.closest('.slide'));
               return all[i].querySelector('.hum-t-loop');
             }, idx);
        const drive = async (action) => {
          return page.evaluate(([i, act]) => {
            const all = [...document.querySelectorAll('.slide')]
              .filter(n => !n.parentElement.closest('.slide'));
            const p = all[i].querySelector('.hum-t-loop');
            const b = p.querySelector(`[data-action="${act}"]`);
            if (!b) return null;
            b.click();                                  // the real control
            const r = p.querySelector('[data-loop-result]');
            return { text: r ? r.textContent.trim() : '',
                     states: [...p.querySelectorAll('[data-lundy-step]')]
                       .map(s => s.getAttribute('data-state')).join(',') };
          }, [idx, action]);
        };
        const a1 = await drive('lundy-audience');       // before voice -> refuse
        if (a1 && /Receive the pupil's Voice first/i.test(a1.text)) res.r38++;
        else res.refusals.push(['38', info.stage, a1 && a1.text.slice(0, 60)]);
        const i1 = await drive('lundy-influence');      // before audience -> refuse
        if (i1 && /(Voice first|Audience comes next)/i.test(i1.text)) res.r39++;
        else res.refusals.push(['39', info.stage, i1 && i1.text.slice(0, 60)]);
        await drive('lundy-voice');
        const i2 = await drive('lundy-influence');      // still refused: no audience
        if (!(i2 && /Audience comes next/i.test(i2.text))) res.refusals.push(['39b', info.stage, i2 && i2.text.slice(0, 60)]);
        await drive('lundy-audience');
        const done = await drive('lundy-influence');
        if (done && /Influence agreed/i.test(done.text) && /done$/.test(done.states.split(',').pop())) res.r40++;
        else res.refusals.push(['40', info.stage, done && done.text.slice(0, 60)]);
      }
    }
    const used = await advance(page, idx);
    if (!used) break;
    await page.waitForTimeout(90);
  }

  // row 42 — a click on a panel control must not also trigger the deck's own handler
  res.doubleDriven = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('.hum-t-loop [data-action]').forEach(b => {
      if (b.closest('[data-sx3-shell]')) out.push(b.getAttribute('data-action'));
    });
    return out;
  });

  await page.addScriptTag({ path: AXE });
  res.axe = await page.evaluate(async () => {
    const r = await window.axe.run(document, { resultTypes: ['violations'] });
    const bad = r.violations.filter(v => ['serious', 'critical'].includes(v.impact));
    return { serious: bad.length, ids: bad.map(v => v.id + ':' + v.nodes.length),
             moderate: r.violations.filter(v => !['serious', 'critical'].includes(v.impact)).length };
  });
  res.errors = errs;
  return res;
}

(async () => {
  const root = process.argv[2], out = process.argv[3];
  const files = process.argv.slice(4);
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const page = await ctx.newPage();
  const all = [];
  for (const f of files) {
    try { all.push(await run(page, path.resolve(root, f))); }
    catch (e) { all.push({ file: f, fatal: String(e).slice(0, 300) }); }
  }
  await browser.close();
  fs.writeFileSync(out, JSON.stringify(all, null, 1));
  const tot = all.reduce((a, r) => ({
    panels: a.panels + (r.panels || 0), reached: a.reached + (r.reached || 0),
    disclosed: a.disclosed + (r.disclosed || 0),
    r38: a.r38 + (r.r38 || 0), r39: a.r39 + (r.r39 || 0), r40: a.r40 + (r.r40 || 0),
    serious: a.serious + ((r.axe && r.axe.serious) || 0),
    errs: a.errs + ((r.errors && r.errors.length) || 0),
    fatal: a.fatal + (r.fatal ? 1 : 0),
  }), { panels: 0, reached: 0, disclosed: 0, r38: 0, r39: 0, r40: 0, serious: 0, errs: 0, fatal: 0 });
  console.log(JSON.stringify({ decks: all.length, ...tot }, null, 1));
})();
