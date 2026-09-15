/* CX2 §3.2 · demonstrate the four LAUNCH focus findings on Diffusion's OWN bytes.
 * Read-only probe: it reports where keyboard focus lands after (1) a slide
 * transition, (2) a reveal, (3) a control that disables itself, (4) opening and
 * closing a dialog. It asserts nothing; the report is the red-before evidence,
 * and the same probe run on the candidate is the green-after.
 *
 *   PLAYWRIGHT_MODULE=/opt/node22/lib/node_modules/playwright \
 *   node tools/launch_resources/focus_probe.cjs <lesson.html> [report.json]
 */
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

const file = process.argv[2];
const out = process.argv[3];
if (!file) { console.error('usage: focus_probe.cjs <lesson.html> [report.json]'); process.exit(2); }

const describe = () => {
  const a = document.activeElement;
  if (!a || a === document.body) return {tag: 'BODY', text: ''};
  return {tag: a.tagName, text: (a.textContent || '').trim().slice(0, 40), id: a.id || '', cls: (a.className || '').toString().slice(0, 40)};
};
const activeTitle = () => { const s = document.querySelector('.slide.active'); return s ? (s.dataset.title || s.id || '') : ''; };

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({viewport: {width: 1280, height: 800}});
  const errors = []; page.on('pageerror', e => errors.push(String(e).slice(0, 160)));
  await page.goto(pathToFileURL(path.resolve(file)).href, {waitUntil: 'load'});
  const report = {file, findings: [], errors};
  const record = async (name, extra) => report.findings.push({name, slide: await page.evaluate(activeTitle), focus: await page.evaluate(describe), ...(extra || {})});

  // 1. slide transition by keyboard on the deck's Next control
  const next = page.locator('button[onclick="nextSlide()"]').first();
  await next.focus(); await page.keyboard.press('Enter'); await page.waitForTimeout(400);
  await record('after Next (Enter): where is focus?', {expected: 'the new slide heading'});

  // 2. a reveal control on the current slide (hint / answers / reveal), if any
  const reveal = page.locator('.slide.active button[onclick*="toggleHint"], .slide.active button[onclick*="reveal"], .slide.active button[onclick*="Reveal"], .slide.active details summary').first();
  if (await reveal.count()) {
    await reveal.focus(); const before = await page.evaluate(describe);
    await page.keyboard.press('Enter'); await page.waitForTimeout(300);
    await record('after reveal (Enter): where is focus?', {before, expected: 'stays on the control or moves to the revealed content'});
  } else {
    report.findings.push({name: 'reveal control on the arrival slide', note: 'none present'});
  }

  // 3. a control that disables itself after use (model step / next-step buttons), searched across slides
  const disabling = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('.slide button').forEach(b => { const o = b.getAttribute('onclick') || ''; if (/disabled\s*=\s*true|\.disabled=true/.test(o) || /v5RevealNext|startWagoll|revealSort|revealMatch/.test(o)) out.push({slide: b.closest('.slide')?.dataset.title, onclick: o.slice(0, 60)}); });
    return out.slice(0, 6);
  });
  report.findings.push({name: 'self-disabling controls found (static scan)', controls: disabling});
  if (disabling.length) {
    const title = disabling[0].slide;
    await page.evaluate(t => { const slides = [...document.querySelectorAll('.slide')]; const i = slides.findIndex(s => s.dataset.title === t); if (i >= 0 && typeof showSlide === 'function') showSlide(i); }, title);
    await page.waitForTimeout(300);
    const btn = page.locator(`.slide.active button[onclick="${disabling[0].onclick.replace(/"/g, '\\"')}"]`).first();
    if (await btn.count()) {
      await btn.focus(); await page.keyboard.press('Enter'); await page.waitForTimeout(400);
      const disabledNow = await btn.evaluate(b => b.disabled || b.getAttribute('aria-disabled') === 'true');
      await record('after a self-disabling control (Enter): where is focus?', {control: disabling[0].onclick, disabledNow, expected: 'focus moved to the next enabled control before disabling'});
    }
  }

  // 4. dialog modality and return focus (TA Brief), from the deck controls
  const ta = page.locator('button[onclick*="showTABrief"]').first();
  if (await ta.count()) {
    await ta.focus(); await page.keyboard.press('Enter'); await page.waitForTimeout(300);
    const open = await page.evaluate(() => { const d = document.querySelector('dialog[open], .v4-modal-overlay.visible'); if (!d) return null; const box = d.querySelector('.v4-modal') || d; return {tag: d.tagName, id: d.id, isDialog: d.tagName === 'DIALOG', modal: d.tagName === 'DIALOG' ? d.matches(':modal') : box.getAttribute('aria-modal') === 'true', role: box.getAttribute('role'), focusInside: d.contains(document.activeElement)}; });
    await record('TA Brief opened: focus and modality', {open, expected: 'dialog semantics with focus inside it'});
    await page.keyboard.press('Escape'); await page.waitForTimeout(300);
    const stillOpen = await page.evaluate(() => !!document.querySelector('dialog[open], .v4-modal-overlay.visible'));
    await record('after Escape: focus returned?', {stillOpen, expected: 'closed, focus back on the TA Brief control'});
  }
  await browser.close();
  const text = JSON.stringify(report, null, 2);
  if (out) fs.writeFileSync(out, text);
  console.log(text);
})();
