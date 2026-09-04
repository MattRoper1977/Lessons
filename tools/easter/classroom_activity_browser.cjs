/* Actual page interactions, not a declaration counter.
 * node classroom_activity_browser.cjs --root REPO --targets TARGETS.json --report REPORT.json
 * TARGETS: {schema:"classroom-activity-browser-targets-v1",kind:"authored-decks"|"standalone-fixtures",
 * targets:[{file:"relative/deck.html",activityId:"unique-id",activitySchema:"relative/activity.json"|{...},stageIndex:4}]}
 * Authored and fixture results are deliberately labelled separately.
 */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require('playwright');
const args = {};
for (let i = 2; i < process.argv.length; i++) {
  const name = process.argv[i];
  assert.ok(['--root', '--targets', '--report', '--channel'].includes(name), 'Unknown argument ' + name);
  assert.ok(process.argv[i + 1], 'Missing value for ' + name);
  args[name.slice(2)] = process.argv[++i];
}
assert.ok(args.root && args.targets && args.report, '--root, --targets and --report are required.');
const root = path.resolve(args.root);
const manifestPath = path.resolve(args.targets);
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
assert.equal(manifest.schema, 'classroom-activity-browser-targets-v1');
assert.ok(['authored-decks', 'standalone-fixtures'].includes(manifest.kind));
assert.ok(Array.isArray(manifest.targets) && manifest.targets.length === 14, 'This gate must name all fourteen Bronze decks.');
const modes = new Set(['sort', 'match', 'choice', 'order']);
const origin = 'http://classroom-activity.test';
const readSchema = row => typeof row.activitySchema === 'string'
  ? JSON.parse(fs.readFileSync(path.resolve(root, row.activitySchema), 'utf8')) : row.activitySchema;
function expectedItems(schema) {
  const common = schema.categories || schema.options || schema.positions;
  return schema.items.map(item => {
    const options = item.options || common;
    assert.ok(Array.isArray(options) && options.length >= 2, 'Each item needs choices.');
    const normalized = options.map(option => ({id:String(option.id), label:option.label}));
    const answer = String(item.answer);
    assert.ok(normalized.some(option => option.id === answer), 'Model answer must be an option.');
    return {...item, answer, options:normalized};
  });
}
const targets = manifest.targets.map((row, i) => {
  assert.ok(typeof row.file === 'string' && typeof row.activityId === 'string', 'Each row needs file and activityId.');
  assert.match(row.activityId, /^[A-Za-z][A-Za-z0-9_-]*$/);
  assert.ok(Number.isInteger(row.stageIndex) && row.stageIndex >= 0 && row.stageIndex < 9);
  const file = path.resolve(root, row.file);
  const relative = path.relative(root, file);
  assert.ok(relative && !relative.startsWith('..') && !path.isAbsolute(relative), 'Target file must be inside --root.');
  const schema = readSchema(row);
  assert.ok(schema && modes.has(schema.mode) && schema.items.length, 'Invalid activity schema.');
  const items = expectedItems(schema);
  return {...row, schema, items, file, route:'/' + relative.split(path.sep).map(encodeURIComponent).join('/'), index:i};
});
assert.equal(new Set(targets.map(t => t.file)).size, 14, 'Fourteen different authored files are required.');
assert.equal(new Set(targets.map(t => t.schema.mode)).size, 4, 'All four activity modes must be exercised.');
const report = {schema:'classroom-activity-browser-report-v1', kind:manifest.kind,
  targets:targets.map(t => ({file:t.file, activityId:t.activityId, mode:t.schema.mode})),
  startedAt:new Date().toISOString(), cases:[], pageErrors:[], blockedExternalRequests:[],
  scope:'Chromium page interaction and print-media visibility. This does not prove PDF pagination, physical device behaviour, media playback or award completion.'};
let browser;
let activeCase = '';
async function measured(name, run) {
  activeCase = name;
  try { await run(); report.cases.push({name, passed:true}); }
  catch (error) { report.cases.push({name, passed:false, error:error.message}); throw error; }
}
function activity(page, target) { return page.locator('[data-mbm-activity="' + target.activityId + '"]'); }
function rowControl(host, index) { return host.locator('[data-activity-row]').nth(index); }
async function stage(page) {
  return page.locator('main.deck > .slide').evaluateAll(slides => slides.findIndex(s => s.classList.contains('active')));
}
async function activate(page, target, touch) {
  await page.emulateMedia({media:'screen'});
  await page.goto(origin + target.route, {waitUntil:'domcontentloaded'});
  await page.locator('main.deck > .slide.active').waitFor();
  assert.equal(await page.locator('main.deck > .slide').count(), 9);
  for (let i = 0; i < 10 && await stage(page) !== target.stageIndex; i++) {
    const next = page.locator('[data-nav="next"]:visible').first();
    touch ? await next.tap() : await next.click();
  }
  assert.equal(await stage(page), target.stageIndex, 'The actual activity stage is reached by deck navigation.');
  const host = activity(page, target);
  await host.waitFor({state:'visible'});
  assert.equal(await host.getAttribute('data-activity-ready'), 'true', 'Activity runtime mounted without error.');
  assert.equal(await host.getAttribute('data-mode'), target.schema.mode);
  assert.equal(await host.locator('[data-activity-row]').count(), target.items.length);
  assert.equal(await host.locator('.mbm-act-status').getAttribute('aria-live'), 'polite');
  return host;
}
async function action(host, name, touch) {
  const button = host.locator('[data-activity-action="' + name + '"]');
  if (touch) await button.tap(); else await button.click();
}
async function setChoice(page, host, target, index, value, touch) {
  const row = rowControl(host, index);
  const item = target.items[index];
  const optionIndex = item.options.findIndex(option => option.id === value);
  assert.ok(optionIndex >= 0);
  if (target.schema.mode === 'choice') {
    const radios = row.locator('input[type="radio"]');
    if (touch) {
      // Touch the full native label, not a synthetic checked-property write.
      await row.locator('label.mbm-act-choice').nth(optionIndex).tap();
    } else {
      await radios.first().focus();
      await page.keyboard.press('Space');
      for (let i = 0; i < optionIndex; i++) await page.keyboard.press('ArrowRight');
    }
    assert.equal(await radios.nth(optionIndex).isChecked(), true, 'Native radio selection took effect.');
  } else {
    const select = row.locator('select');
    if (touch) {
      // Chromium owns the popup. Tap the real select, then use Playwright's
      // native select API for its option; this is not a physical OS-picker test.
      await select.tap();
      await page.keyboard.press('Escape');
      await select.selectOption(value);
    } else {
      await select.focus();
      await page.keyboard.press('Home');
      for (let i = 0; i <= optionIndex; i++) await page.keyboard.press('ArrowDown');
    }
    assert.equal(await select.inputValue(), value, 'Native select choice took effect.');
  }
  assert.equal(await stage(page), target.stageIndex, 'Form arrow keys must not move the deck stage.');
}
async function allCorrect(page, host, target, touch) {
  for (let i = 0; i < target.items.length; i++) await setChoice(page, host, target, i, target.items[i].answer, touch);
  await action(host, 'check', touch);
  assert.equal(await host.locator('[data-check="match"]').count(), target.items.length);
  assert.match(await host.locator('.mbm-act-status').innerText(), /choices match the model/i);
}
async function layout(page, host) {
  const sizes = await page.evaluate(() => ({width:innerWidth, scroll:document.documentElement.scrollWidth}));
  assert.ok(sizes.scroll <= sizes.width + 2, 'The page must not overflow horizontally at the tested viewport.');
  const geometry = await host.locator('select, .mbm-act-choice, .mbm-act-actions button').evaluateAll(nodes => nodes.map(node => {
    const r = node.getBoundingClientRect();
    return {left:r.left, right:r.right, height:r.height, width:innerWidth};
  }));
  assert.ok(geometry.length > 0);
  geometry.forEach(r => {
    assert.ok(r.height >= 43.5, 'Activity touch target needs at least 44 CSS pixels.');
    assert.ok(r.left >= -1 && r.right <= r.width + 1, 'Activity control must fit the viewport horizontally.');
  });
}
async function teacherAndPrint(page, host, target, touch) {
  assert.equal(await page.locator('main.deck .mbm-activity-staff:visible').count(), 0);
  const button = page.locator('[data-tool="1"]:visible').first();
  touch ? await button.tap() : await button.click();
  const notes = page.locator('#award-teacher-notes');
  await notes.waitFor({state:'visible'});
  const key = notes.locator('.mbm-activity-staff').filter({hasText:target.schema.heading});
  assert.equal(await key.count(), 1, 'Current activity has exactly one visible teacher key.');
  assert.equal(await key.isVisible(), true);
  const keyText = await key.innerText();
  target.items.forEach(item => assert.ok(keyText.includes(item.feedback), 'Teacher tools must include each actual model reason.'));
  // Print while the teacher key and pupil explanation have both been opened.
  // The screen state must never leak either onto the default pupil print.
  await page.emulateMedia({media:'print'});
  const printed = page.locator('[data-activity-print="' + target.activityId + '-print"]');
  assert.equal(await printed.isVisible(), true, 'The actual pupil print task survives the chassis print CSS.');
  assert.equal(await host.isVisible(), false, 'Interactive screen task is hidden in print.');
  assert.equal(await page.locator('.mbm-activity-staff:visible').count(), 0, 'Teacher keys remain hidden when printing from an open Teacher tools dialog.');
  const printQuestions = await printed.locator('.mbm-print-task').allTextContents();
  assert.deepEqual(printQuestions, target.items.map(item => item.label));
  assert.deepEqual(await printed.locator('.mbm-print-options').allTextContents(), target.items.map(item => item.options.map(o => o.label).join(' · ')));
  assert.equal(await printed.locator('input, select, [data-mbm-guide], .mbm-act-explanations').count(), 0);
  const printText = await printed.innerText();
  target.items.forEach(item => assert.ok(!printText.includes(item.feedback), 'Pupil print must not carry the model reason.'));
  await page.emulateMedia({media:'screen'});
  await page.keyboard.press('Escape');
  assert.equal(await page.locator('#taOverlay').isVisible(), false);
  assert.equal(await button.evaluate(node => node === document.activeElement), true, 'Teacher tools restores focus to its opener.');
  assert.equal(await stage(page), target.stageIndex);
}
async function exercise(page, target, touch, prefix) {
  const beforeErrors = report.pageErrors.length;
  let host;
  await measured(prefix + '/load-and-activate', async () => { host = await activate(page, target, touch); });
  await measured(prefix + '/blank-check', async () => {
    await action(host, 'check', touch);
    assert.equal(await host.locator('[data-check="missing"]').count(), target.items.length);
    assert.match(await host.locator('.mbm-act-status').innerText(), /still blank/i);
  });
  await measured(prefix + '/native-correct-choices', async () => { await allCorrect(page, host, target, touch); });
  await measured(prefix + '/wrong-choice-needs-review', async () => {
    const item = target.items[0];
    await setChoice(page, host, target, 0, item.options.find(o => o.id !== item.answer).id, touch);
    await action(host, 'check', touch);
    assert.equal(await rowControl(host, 0).getAttribute('data-check'), 'review');
    assert.match(await host.locator('.mbm-act-status').innerText(), /differ from the model/i);
  });
  if (target.schema.mode === 'order') await measured(prefix + '/duplicate-order-position', async () => {
    const same = target.items[0].options[0].id;
    await setChoice(page, host, target, 0, same, touch);
    await setChoice(page, host, target, 1, same, touch);
    await action(host, 'check', touch);
    for (let i = 0; i < 2; i++) assert.match(await rowControl(host, i).locator('.mbm-act-row-feedback').innerText(), /used more than once/);
  });
  await measured(prefix + '/retry-clears-values-feedback-and-focus', async () => {
    await action(host, 'retry', touch);
    assert.equal(await host.locator('input[type="radio"]:checked').count(), 0);
    assert.ok((await host.locator('select').evaluateAll(nodes => nodes.map(n => n.value))).every(v => v === ''));
    assert.equal(await host.locator('[data-check]').count(), 0);
    assert.ok((await host.locator('.mbm-act-row-feedback').allTextContents()).every(t => t === ''));
    assert.equal(await host.locator('.mbm-act-explanations').isVisible(), false);
    assert.equal(await host.locator('[data-activity-action="explain"]').getAttribute('aria-expanded'), 'false');
    assert.equal(await host.locator('select, input[type="radio"]').first().evaluate(node => node === document.activeElement), true);
    assert.match(await host.locator('.mbm-act-status').innerText(), /Choices cleared/);
  });
  await measured(prefix + '/show-hide-and-restore-explanations', async () => {
    const button = host.locator('[data-activity-action="explain"]');
    await action(host, 'explain', touch);
    assert.equal(await button.getAttribute('aria-expanded'), 'true');
    assert.equal(await host.locator('.mbm-act-explanations').isVisible(), true);
    const model = await host.locator('.mbm-act-explanations').innerText();
    target.items.forEach(item => assert.ok(model.includes(item.feedback)));
    await action(host, 'explain', touch);
    assert.equal(await button.getAttribute('aria-expanded'), 'false');
    assert.equal(await host.locator('.mbm-act-explanations').isVisible(), false);
    await action(host, 'explain', touch);
  });
  await measured(prefix + '/teacher-key-and-pupil-print', async () => { await teacherAndPrint(page, host, target, touch); });
  await measured(prefix + '/tab-can-leave-activity', async () => {
    const first = host.locator('select, input[type="radio"]').first();
    await first.focus();
    let left = false;
    for (let i = 0; i < target.items.length + 8; i++) {
      await page.keyboard.press('Tab');
      if (!await host.evaluate(node => node.contains(document.activeElement))) { left = true; break; }
    }
    assert.equal(left, true, 'The activity must not trap the Tab sequence.');
    assert.equal(await stage(page), target.stageIndex);
  });
  if (target.coexistingActivity) await measured(prefix + '/coexisting-activity-state-isolation', async () => {
    const otherSchema = readSchema(target.coexistingActivity);
    const otherTarget = {...target, activityId:target.coexistingActivity.activityId, schema:otherSchema, items:expectedItems(otherSchema)};
    const other = activity(page, otherTarget);
    assert.equal(await other.isVisible(), true);
    assert.equal(await other.getAttribute('data-activity-ready'), 'true');
    const snapshot = async () => host.evaluate(node => ({
      values:Array.from(node.querySelectorAll('input,select'), n => ({value:n.value, checked:n.checked || false})),
      status:node.querySelector('.mbm-act-status').textContent,
      explanationsHidden:node.querySelector('.mbm-act-explanations').hidden
    }));
    const before = await snapshot();
    await allCorrect(page, other, otherTarget, touch);
    assert.deepEqual(await snapshot(), before, 'Checking a second activity must not change the first.');
    await action(other, 'retry', touch);
    assert.deepEqual(await snapshot(), before, 'Retry in a second activity must not clear the first.');
  });
  await measured(prefix + '/ids-and-accessible-targets', async () => {
    const result = await page.evaluate(() => {
      const ids = Array.from(document.querySelectorAll('[id]'), n => n.id);
      const ownedIds = Array.from(document.querySelectorAll('[data-mbm-activity] [id], [data-activity-print] [id]'), n => n.id);
      const missing = [];
      document.querySelectorAll('[data-mbm-activity] [aria-labelledby], [data-mbm-activity] [aria-describedby], [data-mbm-activity] [aria-controls]').forEach(node => {
        ['aria-labelledby', 'aria-describedby', 'aria-controls'].forEach(a => (node.getAttribute(a) || '').split(/\s+/).filter(Boolean).forEach(id => { if (!document.getElementById(id)) missing.push(id); }));
      });
      return {duplicateIds:ownedIds.filter(id => ids.filter(value => value === id).length > 1), missing};
    });
    assert.deepEqual(result, {duplicateIds:[], missing:[]});
  });
  if (touch) await measured(prefix + '/touch-size-and-horizontal-fit', async () => { await layout(page, host); });
  await measured(prefix + '/no-page-errors', async () => { assert.equal(report.pageErrors.length, beforeErrors); });
}
async function configure(context) {
  await context.route('**/*', async route => {
    const url = new URL(route.request().url());
    if (url.origin !== origin) {
      report.blockedExternalRequests.push({url:url.href, case:activeCase});
      return route.abort('blockedbyclient');
    }
    let file;
    try { file = path.resolve(root, '.' + decodeURIComponent(url.pathname)); }
    catch (_) { return route.fulfill({status:400, body:'Invalid local path'}); }
    if (!file.startsWith(root + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) return route.fulfill({status:404, body:'No local fixture at this path'});
    const ext = path.extname(file).toLowerCase();
    const types = {'.html':'text/html; charset=utf-8','.js':'application/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml','.jpg':'image/jpeg','.png':'image/png'};
    return route.fulfill({contentType:types[ext] || 'application/octet-stream', body:fs.readFileSync(file)});
  });
  context.on('page', page => page.on('pageerror', error => report.pageErrors.push({case:activeCase, message:error.message})));
}
(async () => {
  try {
    browser = await chromium.launch({headless:true, channel:args.channel || (process.env.CI ? 'chrome' : undefined)});
    const desktop = await browser.newContext({viewport:{width:1280,height:900}});
    await configure(desktop);
    const page = await desktop.newPage();
    for (const target of targets) await exercise(page, target, false, 'desktop/' + path.basename(target.file));
    await desktop.close();
    const representatives = [...modes].map(mode => targets.find(t => t.schema.mode === mode));
    for (const viewport of [{width:390,height:844}, {width:840,height:1180}]) {
      const context = await browser.newContext({viewport, hasTouch:true, isMobile:true});
      await configure(context);
      const touchPage = await context.newPage();
      for (const target of representatives) await exercise(touchPage, target, true, 'touch-' + viewport.width + '/' + target.schema.mode);
      await context.close();
    }
    await measured('all-contexts/no-unclaimed-page-errors', async () => { assert.equal(report.pageErrors.length, 0); });
    report.result = 'PASS';
  } catch (error) {
    report.result = 'FAIL'; report.error = error.stack;
    process.exitCode = 1;
  } finally {
    if (browser) await browser.close();
    report.finishedAt = new Date().toISOString();
    report.measuredCases = report.cases.length;
    report.passedCases = report.cases.filter(c => c.passed).length;
    fs.mkdirSync(path.dirname(path.resolve(args.report)), {recursive:true});
    fs.writeFileSync(args.report, JSON.stringify(report, null, 2) + '\n');
    console.log(JSON.stringify({result:report.result, kind:manifest.kind, measuredCases:report.measuredCases, passedCases:report.passedCases, pageErrors:report.pageErrors.length, report:path.resolve(args.report)}));
    if (report.error) console.error(report.error);
  }
})();
