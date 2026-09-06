/* Real generated award pages in Chromium; route data is test-only, never a booking.
 * Usage: node tools/artsaward/award_chassis_browser.cjs [repository root]
 * Optional: --root REPO --targets TARGETS.json --content-dir SPEC_DIRECTORY
 * Optional: --print-fit-report REPORT.json (A4 DOM estimate; not PDF pagination proof)
 * When this draft lives outside the repo, supply the repository root explicitly.
 */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require('playwright');
const options = {};
for (let index = 2; index < process.argv.length; index += 1) {
  const arg = process.argv[index];
  if (['--root', '--targets', '--content-dir', '--print-fit-report'].includes(arg)) {
    assert.ok(process.argv[index + 1], 'Missing value for ' + arg);
    options[arg.slice(2)] = process.argv[++index];
  } else {
    assert.ok(!arg.startsWith('--') && !options.root, 'Unexpected argument: ' + arg);
    options.root = arg;
  }
}
const root = path.resolve(options.root || path.join(__dirname, '../..'));
const awardDir = path.join(root, 'tools/artsaward');
const targetsPath = path.resolve(options.targets || path.join(awardDir, 'BRONZE_TARGETS.json'));
const contentDir = path.resolve(options['content-dir'] || path.join(awardDir, 'content'));
const targets = JSON.parse(fs.readFileSync(targetsPath, 'utf8')).batch;
const specs = new Map(targets.map(target => [target.spec,
  JSON.parse(fs.readFileSync(path.resolve(contentDir, target.spec), 'utf8'))]));
const routePaths = new Map(targets.map((target, index) => [target,
  path.isAbsolute(target.route) ? '/fixtures/deck-' + index + '.html' : '/' + target.route]));
function requiredSlots(target) {
  const keys = (target.artsAward && target.artsAward.slots) || target.slots || [];
  assert.ok(Array.isArray(keys) && keys.every(key => typeof key === 'string' && key.trim()),
    target.route + ': slot requirements must be an array of names.');
  return Array.from(new Set(keys));
}
const fixtureSlots = {schema:'arts-award-slots-v1', slots:Object.fromEntries(
  Array.from(new Set(targets.flatMap(requiredSlots)), key => [key, {entries:[]}]))};
const normalize = text => text.replace(/\s+/g, ' ').trim();
assert.ok(targets.length > 0, 'The gate needs at least one generated target.');
if (!options.targets) assert.equal(targets.length, 14, 'The default Bronze gate covers all fourteen targets.');

(async () => {
  const browser = await chromium.launch({headless:true, channel:process.env.CI ? 'chrome' : undefined});
  const errors = [];
  const printMeasurements = [];
  try {
    const page = await browser.newPage({viewport:{width:1280, height:800}});
    page.on('pageerror', error => errors.push(error.message));
    await page.addInitScript(() => {
      window.__printCalls = 0;
      window.print = () => { window.__printCalls += 1; };
    });
    const pages = new Map(targets.map(target => [routePaths.get(target),
      fs.readFileSync(path.resolve(root, target.route), 'utf8')]));
    await page.route('http://award.test/**', route => {
      const pathname = new URL(route.request().url()).pathname;
      if (pathname.endsWith('/SLOTS.json')) {
        return route.fulfill({contentType:'application/json', body:JSON.stringify(fixtureSlots)});
      }
      if (pages.has(pathname)) return route.fulfill({contentType:'text/html; charset=utf-8', body:pages.get(pathname)});
      return route.fulfill({status:404, contentType:'text/plain', body:'No test fixture for this path.'});
    });

    async function go(target) {
      await page.emulateMedia({media:'screen'});
      await page.goto('http://award.test' + routePaths.get(target));
      await page.locator('main.deck > .slide.active').waitFor();
      assert.equal(await page.locator('main.deck > .slide').count(), 9, target.route);
      assert.equal(await page.locator('main.deck > .slide.active').count(), 1, target.route);
    }

    async function assertStage(index) {
      const state = await page.evaluate(() => {
        const slides = Array.from(document.querySelectorAll('main.deck > .slide'));
        const progress = document.querySelector('.prog');
        return {index:slides.findIndex(slide => slide.classList.contains('active')),
          visible:slides.filter(slide => getComputedStyle(slide).display !== 'none').length,
          max:progress.getAttribute('aria-valuemax'), now:progress.getAttribute('aria-valuenow'),
          width:parseFloat(progress.querySelector('span').style.width)};
      });
      assert.equal(state.index, index, 'Navigation must show the intended stage.');
      assert.equal(state.visible, 1, 'Only the selected stage is on the learner surface.');
      assert.equal(state.max, '9');
      assert.equal(state.now, String(index + 1));
      assert.ok(Math.abs(state.width - (index + 1) / 9 * 100) < 0.01, 'Progress width follows the stage.');
    }

    const first = targets[0];
    await go(first);
    await assertStage(0);
    await page.locator('[data-nav="next"]').click();
    await assertStage(1);
    await page.locator('[data-nav="previous"]').click();
    await assertStage(0);
    await page.keyboard.press('ArrowLeft');
    await assertStage(8);
    await page.keyboard.press('ArrowRight');
    await assertStage(0);
    for (let index = 1; index < 9; index += 1) {
      await page.keyboard.press('ArrowRight');
      await assertStage(index);
    }
    await page.keyboard.press('ArrowRight');
    await assertStage(0);
    // The legacy duplicate navigation buttons are optional, but must work if retained.
    if (await page.locator('[data-tool="5"]').count()) {
      await page.locator('[data-tool="5"]').click();
      await assertStage(8);
      await page.locator('[data-nav="next"]').click();
    }
    if (await page.locator('[data-tool="6"]').count()) {
      await page.locator('[data-tool="6"]').click();
      await assertStage(1);
      await page.locator('[data-nav="previous"]').click();
    }
    await assertStage(0);
    assert.equal(await page.locator('.n6m-guide-btn').count(), 0, 'The legacy all-guidance control must be absent.');
    assert.equal(await page.locator('#taOverlay').isVisible(), false, 'Teacher tools start closed.');
    assert.equal(await page.locator('#taOverlay').getAttribute('aria-hidden'), 'true');
    assert.equal(await page.locator('[data-tool="1"]').getAttribute('aria-expanded'), 'false');
    assert.equal(await page.locator('main.deck [data-mbm-guide]:visible').count(), 0);

    await page.locator('[data-tool="2"]').click();
    assert.equal(await page.evaluate(() => window.__printCalls), 1, 'Evidence & print invokes printing once.');
    assert.equal(await page.locator('body').evaluate(node => node.classList.contains('loop-on')), false);
    for (const [tool, className] of [['3', 'calm'], ['4', 'teacher-freeze']]) {
      const button = page.locator('[data-tool="' + tool + '"]');
      assert.equal(await button.getAttribute('aria-pressed'), 'false');
      await button.click();
      assert.equal(await button.getAttribute('aria-pressed'), 'true');
      assert.equal(await page.locator('body').evaluate((node, key) => node.classList.contains(key), className), true);
      await button.click();
      assert.equal(await button.getAttribute('aria-pressed'), 'false');
      assert.equal(await page.locator('body').evaluate((node, key) => node.classList.contains(key), className), false);
      await assertStage(0);
    }

    // A native editable control must keep arrow keys, rather than changing a slide.
    await page.evaluate(() => {
      const input = document.createElement('textarea');
      input.id = 'keyboard-test-input'; input.value = 'abc';
      document.querySelector('main.deck > .slide.active').appendChild(input);
      input.focus(); input.setSelectionRange(0, 0);
    });
    await page.keyboard.press('ArrowRight');
    await assertStage(0);
    assert.equal(await page.locator('#keyboard-test-input').evaluate(node => node.selectionStart), 1);
    await page.locator('#keyboard-test-input').evaluate(node => node.remove());

    async function checkTeacherOpen(stageIndex) {
      const teacher = page.locator('[data-tool="1"]');
      await teacher.click();
      const dialog = page.getByRole('dialog', {name:'Teacher tools'});
      await dialog.waitFor();
      assert.equal(await teacher.getAttribute('aria-expanded'), 'true');
      assert.equal(await dialog.getAttribute('aria-modal'), 'true');
      assert.equal(await page.locator('#taOverlay').getAttribute('aria-hidden'), 'false');
      const expectedNotes = await page.locator('main.deck > .slide').evaluateAll((slides, index) => {
        const stage = slides[index];
        const sources = index ? [stage, slides[0]] : [stage];
        return [stage.dataset.title, stage.dataset.ta1, stage.dataset.ta2,
          ...sources.flatMap(source => Array.from(source.querySelectorAll('[data-mbm-guide]'))
            .filter(node => node.id !== 'award-slot-panel' && !node.closest('#award-slot-panel'))
            .map(node => node.textContent))].filter(Boolean);
      }, stageIndex);
      const actual = normalize(await page.locator('#award-teacher-notes').innerText());
      expectedNotes.forEach(text => assert.ok(actual.includes(normalize(text)), 'Teacher note missing: ' + text));
      assert.equal(await dialog.evaluate(node => node.contains(document.activeElement)), true);
      // Focus last then Tab, and first then Shift+Tab: neither may leave the dialog.
      const focusSelector = 'a[href], button, input, select, textarea, [tabindex]';
      await dialog.evaluate((node, selector) => {
        const list = Array.from(node.querySelectorAll(selector))
          .filter(item => !item.disabled && item.tabIndex >= 0 && item.getClientRects().length);
        list[list.length - 1].focus();
      }, focusSelector);
      await page.keyboard.press('Tab');
      assert.equal(await dialog.evaluate((node, selector) => {
        const list = Array.from(node.querySelectorAll(selector))
          .filter(item => !item.disabled && item.tabIndex >= 0 && item.getClientRects().length);
        return document.activeElement === list[0];
      }, focusSelector), true, 'Tab wraps to the first dialog control.');
      await page.keyboard.press('Shift+Tab');
      assert.equal(await dialog.evaluate((node, selector) => {
        const list = Array.from(node.querySelectorAll(selector))
          .filter(item => !item.disabled && item.tabIndex >= 0 && item.getClientRects().length);
        return document.activeElement === list[list.length - 1];
      }, focusSelector), true, 'Shift+Tab wraps to the last dialog control.');
      await page.keyboard.press('ArrowRight');
      await assertStage(stageIndex);
    }

    async function assertTeacherClosed() {
      assert.equal(await page.locator('#taOverlay').isVisible(), false);
      assert.equal(await page.locator('#taOverlay').getAttribute('aria-hidden'), 'true');
      assert.equal(await page.locator('[data-tool="1"]').getAttribute('aria-expanded'), 'false');
      assert.equal(await page.locator('[data-tool="1"]').evaluate(node => node === document.activeElement), true);
      assert.equal(await page.locator('main.deck [data-mbm-guide]:visible').count(), 0);
    }

    await page.locator('[data-nav="next"]').click();
    await checkTeacherOpen(1);
    await page.keyboard.press('Escape');
    await assertTeacherClosed();
    await page.locator('[data-nav="next"]').click();
    await checkTeacherOpen(2);
    await page.locator('[data-close-overlay]').click();
    await assertTeacherClosed();

    // Prefer a deck with several requirements, so confirmation must satisfy all of them.
    const slotTarget = targets.reduce((best, target) => requiredSlots(target).length
      > (best ? requiredSlots(best).length : 0) ? target : best, null);
    assert.ok(slotTarget, 'A generated deck with declared slots is required for the live reader integration.');
    const slotKeys = requiredSlots(slotTarget);
    const chosenKey = slotKeys[0];
    await go(slotTarget);
    const slotInput = page.locator('#award-slot-panel input[type="file"]');
    await slotInput.waitFor({state:'attached'});
    const originalInput = await slotInput.elementHandle();
    assert.equal(await slotInput.isVisible(), false, 'Slot details are staff-only.');
    await checkTeacherOpen(0);
    assert.equal(await originalInput.evaluate(node => node === document.querySelector('#award-slot-panel input')), true);
    assert.equal(await slotInput.isVisible(), true, 'Teacher tools expose the actual slot reader.');
    assert.equal(await page.locator('#taOverlay #award-slot-panel').count(), 1);
    const localSlots = structuredClone(fixtureSlots);
    slotKeys.forEach(key => localSlots.slots[key].entries.push({
      name:key === chosenKey ? '<b>Local test session</b>' : 'Local test ' + key,
      route:'R3', status:'CONFIRMED'}));
    async function assertLocalSlotRows() {
      assert.equal(await page.locator('#award-slot-panel li').count(), slotKeys.length);
      for (const key of slotKeys) {
        await page.getByText(key + ': ' + localSlots.slots[key].entries[0].name + ' · R3', {exact:true}).waitFor();
      }
    }
    await slotInput.setInputFiles({name:'SLOTS.json', mimeType:'application/json',
      buffer:Buffer.from(JSON.stringify(localSlots))});
    await page.getByRole('status').filter({hasText:'A confirmed route'}).waitFor();
    await assertLocalSlotRows();
    assert.equal(await page.locator('#award-slot-panel li b').count(), 0, 'File data stays literal text.');
    await slotInput.focus();
    await page.keyboard.press('ArrowRight');
    await assertStage(0);
    await page.keyboard.press('Escape');
    await assertTeacherClosed();
    await checkTeacherOpen(0);
    assert.equal(await originalInput.evaluate(node => node === document.querySelector('#award-slot-panel input')), true,
      'The same input node survives the second opening.');
    await assertLocalSlotRows();
    assert.equal(await slotInput.evaluate(node => node.files[0].name), 'SLOTS.json');
    localSlots.slots[chosenKey].entries[0].name = 'Second local test session';
    await slotInput.setInputFiles({name:'SLOTS-updated.json', mimeType:'application/json',
      buffer:Buffer.from(JSON.stringify(localSlots))});
    await page.getByRole('status').filter({hasText:'A confirmed route'}).waitFor();
    await assertLocalSlotRows();
    await page.locator('[data-close-overlay]').click();
    await assertTeacherClosed();
    await originalInput.dispose();

    for (const target of targets) {
      await go(target);
      const spec = specs.get(target.spec);
      assert.equal(spec.print.figures.length, 2, target.spec + ': expected two source figures.');
      const print = page.locator('.print-pack');
      assert.equal(await print.count(), 1, target.route);
      assert.equal(await print.isVisible(), false, 'The print pack stays off the screen.');
      const result = await print.evaluate((pack, source) => {
        const normalize = text => text.replace(/\s+/g, ' ').trim();
        function canonical(node) {
          if (node.nodeType === Node.TEXT_NODE) return normalize(node.textContent) || null;
          if (node.nodeType !== Node.ELEMENT_NODE) return null;
          return [node.namespaceURI, node.localName,
            Array.from(node.attributes, attr => [attr.name, attr.value]).sort((a, b) => a[0].localeCompare(b[0])),
            Array.from(node.childNodes, canonical).filter(value => value !== null)];
        }
        const parser = new DOMParser();
        const expected = source.figures.map(svg => canonical(parser.parseFromString(svg, 'text/html').querySelector('svg')));
        const actual = Array.from(pack.querySelectorAll('svg')).filter(svg => !svg.closest('[data-activity-print]')).map(canonical);
        const activityExpected = source.activities.filter(row => row.diagram).map(row => {
          const svg = parser.parseFromString(row.diagram.svg, 'text/html').querySelector('svg');
          const ids = new Map(Array.from(svg.querySelectorAll('[id]'), node => [node.id, row.id + '-print-' + node.id]));
          if (svg.id) ids.set(svg.id, row.id + '-print-' + svg.id);
          for (const node of [svg, ...svg.querySelectorAll('*')]) {
            for (const attr of Array.from(node.attributes)) {
              if (attr.name === 'id') node.setAttribute('id', ids.get(attr.value));
              else if (['aria-labelledby', 'aria-describedby'].includes(attr.name)) node.setAttribute(attr.name, attr.value.split(/\s+/).map(id => ids.get(id)).join(' '));
              else if (attr.value.startsWith('url(#')) node.setAttribute(attr.name, 'url(#' + ids.get(attr.value.slice(5, -1)) + ')');
            }
          }
          svg.setAttribute('role', 'img');
          if (!svg.hasAttribute('aria-labelledby')) svg.setAttribute('aria-label', row.diagram.alt);
          return canonical(svg);
        });
        const activityActual = Array.from(pack.querySelectorAll('[data-activity-print] svg'), canonical);
        const pages = Array.from(pack.querySelectorAll('.print-page'));
        return {actual, expected, activityActual, activityExpected,
          pageHeadings:pages.map(page => Array.from(page.querySelectorAll('h1,h2'), node => normalize(node.textContent))),
          headings:Array.from(pack.querySelectorAll('h1,h2,h3'), node => normalize(node.textContent)),
          headers:Array.from(pack.querySelectorAll('th'), node => normalize(node.textContent)),
          text:normalize(pack.textContent)};
      }, {...spec.print, activities:spec.stages.flatMap((stage, si) => stage.blocks.flatMap((block, bi) => block.kind === 'activity'
        ? [{id:spec.id + '-stage' + si + '-' + (bi + 1), diagram:block.data.diagram}] : []))});
      assert.deepEqual(result.actual, result.expected, target.route + ': printed figures must match the two source figures.');
      assert.deepEqual(result.activityActual, result.activityExpected, target.route + ': printed activity diagrams must match their authored sources.');
      assert.ok(result.pageHeadings.length > 0, target.route + ': print pages exist.');
      assert.ok(result.pageHeadings.every(headings => headings.length && headings.every(Boolean)), target.route + ': nonblank page headings.');
      assert.ok(result.headings.every(Boolean), target.route + ': no empty print heading.');
      assert.ok(result.headers.length >= 3 && result.headers.every(Boolean), target.route + ': named table headers.');
      for (const text of [...(spec.print.sections || []), spec.print.intro, ...spec.print.focusRows,
        ...spec.print.tiers, ...spec.print.checks]) {
        assert.ok(result.text.includes(normalize(text)), target.route + ': missing print source text: ' + text);
      }
      await page.emulateMedia({media:'print'});
      assert.equal(await print.isVisible(), true, target.route + ': pack appears for printing.');
      assert.equal(await page.locator('main.deck').isVisible(), false, target.route + ': slides stay outside the print pack.');
      assert.equal(await page.locator('.controls').isVisible(), false, target.route + ': toolbar is not printed.');
      assert.equal(await page.locator('#taOverlay').isVisible(), false, target.route + ': teacher dialog is not printed.');
      if (options['print-fit-report']) {
        const pages = await print.evaluate(pack => {
          const previousWidth = pack.style.width;
          // A4 minus the donor's 10 mm margins. Print media alone retains viewport width.
          pack.style.width = '190mm';
          try {
            const mmPerPixel = 25.4 / 96;
            const round = value => Math.round(value * 10) / 10;
            return Array.from(pack.querySelectorAll('.print-page'), (sheet, index) => {
              const box = sheet.getBoundingClientRect();
              const style = getComputedStyle(sheet);
              const borders = parseFloat(style.borderTopWidth) + parseFloat(style.borderBottomWidth);
              const height = Math.max(box.height, sheet.scrollHeight + borders) * mmPerPixel;
              const horizontalOverflow = Math.max(0, sheet.scrollWidth - sheet.clientWidth) * mmPerPixel;
              return {page:index + 1, heightMm:round(height),
                excessHeightMm:round(Math.max(0, height - 277)),
                horizontalOverflowMm:round(horizontalOverflow),
                withinMeasuredBox:height <= 277.5 && horizontalOverflow <= 0.5};
            });
          } finally {
            pack.style.width = previousWidth;
          }
        });
        printMeasurements.push({route:target.route, pages});
      }
    }
    assert.deepEqual(errors, [], 'No page runtime errors.');
    if (options['print-fit-report']) {
      fs.writeFileSync(path.resolve(options['print-fit-report']), JSON.stringify({
        method:'Print-media DOM layout at 190 mm width; compared with the 277 mm A4 content height after 10 mm margins.',
        limitation:'Informational estimate only. This does not test PDF pagination, browser print headers, printer scaling or physical output.',
        decks:printMeasurements}, null, 2) + '\n');
      console.log('INFO: wrote A4 DOM fit estimates for ' + printMeasurements.length + ' decks.');
    }
    console.log('PASS: award toolbar, 9-stage navigation/progress, modal keyboard/focus, live slot input across two cycles, print invocation and ' + targets.length + ' source-matched print packs in Chromium.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
