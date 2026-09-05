/* Supplemental Humanities acceptance using the existing reviewed CI browser.
 * This module never starts a browser. The parent driver owns routing, logs and
 * exported-page review. Native Office/PDF downloads retain reviewed ZIP bytes.
 */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const digest = data => crypto.createHash('sha256').update(data).digest('hex');
const origin = 'http://science-original.test';
const base = 'Humanities_Teesside/David_Cover_Autumn1_W3-W7';
const printSentinel = 'HUMANITIES_TEACHER_KEY_MUST_NOT_PRINT';

async function run({browser, root, out, configure, measured, report}) {
  const raw = fs.readFileSync(path.join(root, 'tools/humanities_resources/CONTENT.json'));
  const content = JSON.parse(raw);
  const source = JSON.parse(fs.readFileSync(path.join(root, 'tools/humanities_resources/SOURCE_MANIFEST.json')));
  const downloads = JSON.parse(fs.readFileSync(path.join(root, 'tools/humanities_resources/DOWNLOAD_MANIFEST.json')));
  const result = {schema: 'humanities-cover-browser-v1', contentSha256: digest(raw), cases: [], routes: [], pdfs: [], images: [], scope: 'Actual desktop, touch, keyboard, no-script and print CSS checks. Pupil PDF exports still require visual page review. No new curriculum cells or external qualification result claimed.'};
  const check = async (name, fn) => {
    try { await measured('humanities-cover/' + name, fn); result.cases.push({name, passed: true}); }
    catch (error) { result.cases.push({name, passed: false, error: error.message}); throw error; }
  };
  const snapshot = async (page, name) => {
    const file = name + '.png';
    await page.screenshot({path: path.join(out, file), fullPage: true});
    result.images.push(file);
  };
  const current = page => page.locator('[data-stage]:visible').getAttribute('data-stage');
  const go = (page, index) => page.locator('#stage-select').selectOption(String(index));
  const clearLayout = async page => {
    const metrics = await page.evaluate(() => ({width: innerWidth, document: document.documentElement.scrollWidth}));
    assert.ok(metrics.document <= metrics.width + 2, 'The page must fit the viewport');
    for (const selector of ['.stage-nav [data-prev]', '.stage-nav select', '.stage-nav [data-next]']) {
      const node = page.locator(selector); await node.scrollIntoViewIfNeeded();
      const box = await node.boundingBox();
      assert.ok(box && box.width >= 43.5 && box.height >= 43.5 && box.x >= 0 && box.x + box.width <= metrics.width + 1, 'Stage control must remain a visible touch target');
      const uncovered = await node.evaluate(n => {
        const r = n.getBoundingClientRect();
        const hit = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2);
        return hit === n || n.contains(hit);
      });
      assert.equal(uncovered, true, 'Nothing may cover a stage control');
    }
  };
  const periodMinutes = async page => {
    const minutes = await page.locator('[data-stage]').evaluateAll(nodes => nodes.map(n => Number(n.dataset.minutes)));
    assert.deepEqual(minutes, source.timings);
    assert.equal(minutes.reduce((n, value) => n + value, 0), 40);
  };
  const printSafe = async page => {
    assert.equal(await page.locator('.teacher-guide').isVisible(), false);
    assert.equal(await page.locator('.answer:visible').count(), 0);
    assert.equal(await page.locator('.stage-nav').isVisible(), false);
    assert.equal(await page.locator('.site-header').isVisible(), false);
    assert.equal(await page.locator('[data-stage="2"]').isVisible(), false);
    assert.equal(await page.locator('[data-stage="4"]').isVisible(), false);
    assert.equal(await page.locator('[data-stage="5"]').isVisible(), true);
  };
  const rejects = async fn => { let fired = false; try { await fn(); } catch (_) { fired = true; } assert.ok(fired, 'The planted defect must be detected'); };
  try {
    await check('source-identity', async () => {
      assert.equal(content.length, 25); assert.equal(digest(raw), source.content_sha256);
      const memberManifest = fs.readFileSync(path.join(root, 'tools/humanities_resources/ORIGINAL_MEMBER_MANIFEST.json'));
      assert.equal(digest(memberManifest), source.native_member_manifest_sha256);
      assert.equal(JSON.parse(memberManifest).source_archive_sha256, source.native_pack_sha256);
      assert.equal(downloads.archives.length, 3);
      for (const archive of downloads.archives) {
        const data = fs.readFileSync(path.join(root, base, archive.filename));
        assert.equal(digest(data), archive.sha256); assert.ok(data.length < 10000000);
      }
    });
    for (const viewport of [{width: 1280, height: 800}, {width: 390, height: 844}]) {
      const touch = viewport.width < 600;
      for (const lesson of content) {
        const id = lesson.id + '-humanities-' + viewport.width;
        const context = await browser.newContext({viewport, hasTouch: touch, reducedMotion: 'reduce'});
        await configure(context); const page = await context.newPage(); page.setDefaultTimeout(10000);
        const before = {errors: report.errors.length, missing: report.missingLocal.length, external: report.external.length};
        const route = base + '/' + lesson.id + '.html';
        const url = origin + '/Lessons/' + route;
        try {
          await check(id + '/title-and-40-minute-sequence', async () => {
            await page.goto(url, {waitUntil: 'domcontentloaded'});
            assert.equal(await page.locator('h1').innerText(), lesson.title);
            assert.equal(await current(page), '0'); await periodMinutes(page);
            assert.equal(await page.locator('.stage-nav [data-prev]').isDisabled(), true);
            assert.equal(await page.locator('.week-nav a').count(), 5);
            assert.equal(await page.locator('.week-nav [aria-current="page"]').getAttribute('href'), lesson.id + '.html');
            assert.equal(await page.locator('.teacher-answers').getAttribute('open'), null);
            await clearLayout(page); await snapshot(page, id + '-opening');
          });
          await check(id + '/real-next-previous-and-pathway-navigation', async () => {
            for (let index = 1; index < 8; index++) {
              const next = page.locator('[data-next]');
              if (touch) await next.tap(); else await next.click();
              assert.equal(await current(page), String(index));
              assert.equal(await page.locator('[data-stage="' + index + '"] h2').evaluate(n => n === document.activeElement), true);
            }
            assert.equal(await page.locator('[data-next]').isDisabled(), true);
            await page.locator('[data-prev]').click(); assert.equal(await current(page), '6');
            await page.locator('[data-stage="6"] h2').press('ArrowLeft'); assert.equal(await current(page), '5');
            await clearLayout(page);
          });
          await check(id + '/pupil-response-and-deliberate-answer-reveal', async () => {
            await go(page, 3);
            const choice = page.locator('input[name="hinge"]').nth(1);
            await choice.check(); assert.equal(await choice.isChecked(), true);
            await go(page, 4);
            const answer = page.locator('#stage-5 details.answer');
            assert.equal(await answer.getAttribute('open'), null);
            if (touch) await answer.locator('summary').tap(); else await answer.locator('summary').press('Enter');
            assert.equal(await answer.locator('.answer-letter').innerText(), lesson.hinge.answer);
            assert.equal((await answer.locator('p').nth(1).innerText()).trim(), lesson.hinge.reason);
            await answer.locator('summary').click(); assert.equal(await answer.getAttribute('open'), null);
            await go(page, 5);
            const response = page.locator('#response-1'); await response.fill('My first explanation');
            await response.press('ArrowRight'); assert.equal(await current(page), '5', 'Arrow keys still edit a pupil response');
            await go(page, 6); await page.locator('#improvement').fill('One source detail improves my reason');
            await go(page, 5); assert.equal(await response.inputValue(), 'My first explanation');
            if (lesson.lane === 'LAUNCH') assert.equal(await page.locator('.re-source').isVisible(), true);
            await snapshot(page, id + '-pupil-task');
          });
          await check(id + '/week-links-and-native-downloads', async () => {
            const adjacent = content.find(c => c.lane === lesson.lane && c.subject === lesson.subject && c.week === (lesson.week === 7 ? 3 : lesson.week + 1));
            assert.ok(adjacent, 'The reviewed content defines the neighbouring week');
            const destination = adjacent.id + '.html';
            await page.locator('.week-nav a[href="' + destination + '"]').click();
            await page.waitForURL(origin + '/Lessons/' + base + '/' + destination);
            await page.goto(url, {waitUntil: 'domcontentloaded'});
            const links = await page.locator('.downloads a').evaluateAll(nodes => nodes.map(n => n.getAttribute('href')));
            assert.equal(links.length, 3);
            for (const link of links) assert.ok(fs.statSync(path.join(root, base, link)).size > 0, 'Native download exists');
            assert.ok(links.some(link => link.endsWith(lesson.id + '_Pupil_Sheets.pdf')));
            assert.ok(links.some(link => link.endsWith(lesson.id + '.pptx')));
            assert.equal(await page.getByRole('link', {name: 'Lesson hub', exact: true}).getAttribute('href'), '../../index.html?subject=Humanities%20%26%20RE');
          });
          if (!touch) await check(id + '/pupil-print-excludes-teacher-answers', async () => {
            await page.locator('details').evaluateAll(nodes => nodes.forEach(n => { n.open = true; }));
            await page.locator('.teacher-answers li').first().evaluate((n, marker) => { n.textContent += ' ' + marker; }, printSentinel);
            await page.emulateMedia({media: 'print'}); await printSafe(page);
            const file = lesson.id + '-humanities-pupil.pdf';
            await page.pdf({path: path.join(out, file), format: 'A4', printBackground: true});
            const entry = {file, lesson: route, level: 'humanities-pupil-task', requiredText: lesson.title, forbiddenText: printSentinel};
            result.pdfs.push(entry); report.pdfs.push(entry);
            await page.emulateMedia({media: 'screen'});
          });
          await check(id + '/no-runtime-or-unexpected-network-errors', async () => {
            assert.equal(report.errors.length, before.errors); assert.equal(report.missingLocal.length, before.missing); assert.equal(report.external.length, before.external);
          });
          result.routes.push({file: route, viewport: viewport.width, result: 'PASS'});
        } catch (error) { result.routes.push({file: route, viewport: viewport.width, result: 'FAIL', error: error.message}); await snapshot(page, id + '-failure').catch(() => {}); }
        finally { await context.close(); }
      }
    }
    for (const lesson of content.filter(c => c.week === 3)) {
      const context = await browser.newContext({viewport: {width: 390, height: 844}, javaScriptEnabled: false});
      await configure(context); const page = await context.newPage();
      try { await check(lesson.id + '/no-script-fallback', async () => {
        await page.goto(origin + '/Lessons/' + base + '/' + lesson.id + '.html');
        assert.equal(await page.locator('[data-stage]:visible').count(), 8);
        assert.equal(await page.locator('.stage-nav').isVisible(), false);
        await page.locator('#stage-5 details summary').click(); assert.equal(await page.locator('#stage-5 .answer-letter').isVisible(), true);
        assert.equal(await page.locator('.downloads a').count(), 3);
      }); } finally { await context.close(); }
    }
    for (const viewport of [{width: 1280, height: 800}, {width: 390, height: 844}]) {
      const context = await browser.newContext({viewport, hasTouch: viewport.width < 600});
      await configure(context); const page = await context.newPage();
      try { await check('cover-index/' + viewport.width + '/three-complete-pathway-packs', async () => {
        await page.goto(origin + '/Lessons/' + base + '/index.html');
        for (const archive of downloads.archives) {
          const link = page.getByRole('link', {name: 'Download ' + archive.pathway + ' pack', exact: true});
          assert.equal(await link.getAttribute('href'), archive.filename);
          assert.notEqual(await link.getAttribute('download'), null);
        }
        assert.equal(await page.locator('.downloads a[download]').count(), 3);
        assert.equal(await page.locator('.lesson-card').count(), 25);
        const size = await page.evaluate(() => ({viewport: innerWidth, scroll: document.documentElement.scrollWidth}));
        assert.ok(size.scroll <= size.viewport + 2);
        await snapshot(page, 'humanities-cover-index-' + viewport.width);
      }); } finally { await context.close(); }
    }
    const control = await browser.newContext(); await configure(control); const page = await control.newPage();
    try {
      await page.goto(origin + '/Lessons/' + base + '/' + content[0].id + '.html');
      await check('negative-control/wrong-period', async () => {
        await page.locator('[data-stage]').first().evaluate(n => { n.dataset.minutes = '41'; });
        await rejects(() => periodMinutes(page));
      });
      await page.emulateMedia({media: 'print'});
      await page.addStyleTag({content: '@media print{.teacher-guide{display:block!important}}'});
      await check('negative-control/printed-teacher-guide', () => rejects(() => printSafe(page)));
    } finally { await control.close(); }
    assert.ok(result.routes.length === 50 && result.routes.every(r => r.result === 'PASS'), 'All cover routes must pass on desktop and phone');
    assert.equal(result.pdfs.length, 25); result.result = 'PASS';
  } catch (error) { result.result = 'FAIL'; result.error = error.message; throw error; }
  finally {
    fs.writeFileSync(path.join(out, 'humanities-cover-browser.json'), JSON.stringify(result, null, 2) + '\n');
    console.log(JSON.stringify({scope: 'humanities-cover', result: result.result, cases: result.cases.length, passed: result.cases.filter(c => c.passed).length, routes: result.routes.length, pdfs: result.pdfs.length, failed: result.cases.filter(c => !c.passed)}));
  }
}
module.exports = {run};
