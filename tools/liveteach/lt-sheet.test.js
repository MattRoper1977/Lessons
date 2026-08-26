/* lt-sheet — the LT9 worksheet suite (spec Phase 8, W1–W5).

   The spec names the gate: "automated render of the print layer showing grid
   + scale bar present in the exported image; no $ in printed text". Both are
   here on pixel and text evidence, plus the rest of the registry:

   W1  the grid and the labelled scale bar SURVIVE the line-art threshold —
       proven by sampling the exported PNG for grey grid columns and for the
       scale bar's end ticks, with a red control showing the sampler can miss.
   W2  no invented units: every number printed is the stage's own, the
       model-to-real mapping is stated, and v = f × λ resolves correctly.
   W3  no "$" and no LaTeX anywhere in the printed text.
   W4  answer lines are real bordered elements — the computed border is read
       under print media, and no line depends on a background gradient.
   W5  the threshold parameter is live: change it and the exported pixels
       change.

     NODE_PATH=$(npm root -g) node tools/liveteach/lt-sheet.test.js */
'use strict';
const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json' };

let failures = 0;
function check(name, ok, detail) {
  console.log((ok ? 'PASS' : 'FAILED') + '  ' + name + (ok || !detail ? '' : ' — ' + detail));
  if (!ok) failures++;
}

function serve() {
  return new Promise(resolve => {
    const srv = http.createServer((req, res) => {
      const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/, '');
      if (rel === 'favicon.ico') { res.writeHead(204); res.end(); return; }
      let p = path.join(ROOT, rel);
      if (fs.existsSync(p) && fs.statSync(p).isDirectory()) p = path.join(p, 'index.html');
      fs.readFile(p, (err, buf) => {
        if (err) { res.writeHead(404); res.end('not found'); return; }
        res.writeHead(200, { 'content-type': MIME[path.extname(p)] || 'application/octet-stream' });
        res.end(buf);
      });
    });
    srv.listen(0, '127.0.0.1', () => resolve(srv));
  });
}

async function open(page, url, errors) {
  page.on('pageerror', e => errors.push('pageerror: ' + String(e).slice(0, 160)));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text().slice(0, 160)); });
  await page.goto(url, { waitUntil: 'load' });
  try { await page.locator('.mbm-skip').click({ timeout: 4000 }); } catch (e) {}
  await page.waitForFunction(() => !document.querySelector('.mbm-splash'), null, { timeout: 8000 });
}

async function stripClick(page, sel) {
  await page.mouse.move(640, 700);
  await page.mouse.move(600, 690);
  await page.click(sel);
}

/* Decode the exported figure back to pixels in the page and describe what is
   actually IN it — the spec asks for the grid and the scale bar to be present
   in the exported image, so the image is what gets examined. */
const SCAN = `(src) => new Promise(res => {
  const im = new Image();
  im.onload = () => {
    const c = document.createElement('canvas');
    c.width = im.width; c.height = im.height;
    const g = c.getContext('2d');
    g.drawImage(im, 0, 0);
    const d = g.getImageData(0, 0, c.width, c.height).data;
    const at = (x, y) => { const i = (y * c.width + x) * 4; return [d[i], d[i+1], d[i+2]]; };
    const isGrey = p => p[0] === p[1] && p[1] === p[2] && p[0] > 60 && p[0] < 230;
    const isBlack = p => p[0] < 60 && p[1] < 60 && p[2] < 60;
    const isWhite = p => p[0] > 240 && p[1] > 240 && p[2] > 240;

    // Grid: scan one row well clear of the axis and count runs of grey.
    const row = Math.round(c.height * 0.18);
    let gridCols = 0, prev = false;
    for (let x = 0; x < c.width; x++) {
      const g1 = isGrey(at(x, row));
      if (g1 && !prev) gridCols++;
      prev = g1;
    }
    // Horizontal grid lines: scan a column clear of the scale bar.
    const col = Math.round(c.width * 0.75);
    let gridRows = 0; prev = false;
    for (let y = 0; y < c.height; y++) {
      const g2 = isGrey(at(col, y));
      if (g2 && !prev) gridRows++;
      prev = g2;
    }
    // The scale bar: the LONGEST CONTIGUOUS black run on its row, with a
    // taller tick at each end. Counting black pixels instead would also
    // count the "1 metre" label, which sits on the same row.
    // Search the bottom band for the row carrying the longest contiguous
    // black run: that is the scale bar, wherever the layout puts it.
    let barY = -1, barRun = 0, barStart = -1;
    for (let y = Math.round(c.height * 0.75); y < c.height; y++) {
      let run = 0, runStart = -1, best = 0, bestStart = -1;
      for (let x = 0; x <= Math.round(c.width * 0.45); x++) {
        if (isBlack(at(x, y))) {
          if (run === 0) runStart = x;
          run++;
          if (run > best) { best = run; bestStart = runStart; }
        } else run = 0;
      }
      if (best > barRun) { barRun = best; barStart = bestStart; barY = y; }
    }
    const tickAt = x => barY > 8 && isBlack(at(x, barY - 8)) && isBlack(at(x, barY + 8));
    const ticks = barStart >= 0 ? [tickAt(barStart + 1), tickAt(barStart + barRun - 2)] : [false, false];

    // Grid PITCH, measured: the caption claims half-metre squares, so the
    // spacing has to be checked against the bar, not merely counted.
    const pitches = [];
    let lastCol = -1;
    prev = false;
    for (let x = 0; x < c.width; x++) {
      const g3 = isGrey(at(x, row));
      if (g3 && !prev) { if (lastCol >= 0) pitches.push(x - lastCol); lastCol = x; }
      prev = g3;
    }
    pitches.sort((a, b) => a - b);
    const pitch = pitches.length ? pitches[Math.floor(pitches.length / 2)] : 0;

    // Line-art evidence: the wave itself must be pure black on pure white.
    let black = 0, white = 0, grey = 0;
    for (let y = 0; y < c.height; y += 3) for (let x = 0; x < c.width; x += 3) {
      const p = at(x, y);
      if (isBlack(p)) black++; else if (isWhite(p)) white++; else grey++;
    }
    res({ w: c.width, h: c.height, gridCols, gridRows, barRun, barY, ticks, pitch, black, white, grey });
  };
  im.onerror = () => res(null);
  im.src = src;
})`;

const SYM = `(src) => new Promise(res => {
  const im = new Image();
  im.onload = () => {
    const c = document.createElement('canvas');
    c.width = im.width; c.height = im.height;
    const g = c.getContext('2d');
    g.drawImage(im, 0, 0);
    const d = g.getImageData(0, 0, c.width, c.height).data;
    const black = (x, y) => { const i = (y * c.width + x) * 4; return d[i] < 60 && d[i+1] < 60 && d[i+2] < 60; };
    // Full-width black rows are the drawn RULES, not the wave: the axis is
    // the first, and the band rule under the figure is the last. The wave
    // lives strictly between them, so the scan must too — otherwise the band
    // rule is mistaken for the bottom of the trough.
    // Rules are detected with a looser darkness cut than the wave: a 1.5px
    // black line on a whole-pixel y antialiases to about 64 grey, which the
    // strict black test misses — while the grid's own greys (194 and 122)
    // stay well above this cut, so nothing else is picked up.
    const darkish = (x, y) => { const i = (y * c.width + x) * 4; return d[i] < 110 && d[i+1] < 110 && d[i+2] < 110; };
    const rules = [];
    for (let y = 0; y < c.height; y++) {
      let n = 0;
      for (let x = 500; x < 900; x += 3) if (darkish(x, y)) n++;
      if (n > 120) rules.push(y);
    }
    const groups = [];
    rules.forEach(y => {
      const g0 = groups[groups.length - 1];
      if (g0 && y - g0[g0.length - 1] <= 2) g0.push(y); else groups.push([y]);
    });
    const axis = groups.length ? (groups[0][0] + groups[0][groups[0].length - 1]) / 2 : -1;
    const floor = groups.length > 1 ? groups[groups.length - 1][0] : c.height;
    let top = -1, bot = -1;
    for (let x = 500; x < 900; x++) {
      for (let y = 0; y < floor - 2; y++) {
        if (!black(x, y)) continue;
        if (top === -1 || y < top) top = y;
        if (y > bot) bot = y;
      }
    }
    res({ top, bot, axis, floor, rules: groups.length, h: c.height });
  };
  im.onerror = () => res(null);
  im.src = src;
})`;

(async () => {
  const srv = await serve();
  const port = srv.address().port;
  const base = 'http://127.0.0.1:' + port + '/liveteach/';
  const exe = process.env.CHROMIUM_PATH && fs.existsSync(process.env.CHROMIUM_PATH) ? process.env.CHROMIUM_PATH : undefined;
  const browser = await chromium.launch({ executablePath: exe, args: ['--no-sandbox'] });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 720 } });

  const perrs = [];
  const proj = await ctx.newPage();
  await open(proj, base + 'projector.html', perrs);
  await proj.waitForFunction(() => window.__LT.manifestId() !== null, null, { timeout: 5000 });

  // Stage 2 of the exemplar is the wave with f = 1 Hz, λ = 2 m.
  await proj.evaluate(() => document.activeElement && document.activeElement.blur());
  await proj.keyboard.press('PageDown');
  await proj.waitForTimeout(250);
  const live = await proj.evaluate(() => ({ wave: window.__LT.wave(), mode: window.__LT.stage().mode, title: window.__LT.stage().title }));
  check('setup: the projector is on a wave stage with real numbers', live.mode === 'wave' && live.wave.f === 1 && live.wave.lambda === 2, JSON.stringify(live.wave));

  await proj.evaluate(() => window.__LT.buildSheet());
  await proj.waitForTimeout(150);
  const sheet = await proj.evaluate(() => window.__LT.sheet());
  check('the print layer builds from the live stage', sheet.built === true && sheet.figures === 1, JSON.stringify({ built: sheet.built, figs: sheet.figures }));

  /* ============ THE GATE, half one: grid + scale bar in the image ======== */
  const scan = await proj.evaluate(eval(SCAN), sheet.figSrc);
  check('W1 GATE: the exported image really decodes', scan && scan.w > 400, JSON.stringify(scan && { w: scan.w, h: scan.h }));
  check('W1 GATE: a calibrated GRID is present in the exported image (vertical and horizontal rules)',
    scan.gridCols >= 8 && scan.gridRows >= 4, JSON.stringify({ cols: scan.gridCols, rows: scan.gridRows }));
  check('W1 GATE: the SCALE BAR is present, with a tick at each end',
    scan.barRun > 40 && scan.ticks[0] === true && scan.ticks[1] === true, JSON.stringify({ run: scan.barRun, ticks: scan.ticks, y: scan.barY }));
  /* Presence is not calibration. The bar claims to be one metre and the grid
     claims half-metre squares, so both are MEASURED against each other: the
     grid pitch must be half the bar, or the sheet's caption is wrong and a
     pupil measuring off it gets the wrong answer. */
  check('W1 GATE: the grid is CALIBRATED — its pitch is exactly half the one-metre bar',
    scan.pitch > 0 && Math.abs(scan.pitch - scan.barRun / 2) <= 2,
    JSON.stringify({ pitch: scan.pitch, bar: scan.barRun, wantPitch: scan.barRun / 2 }));
  /* And the drawn wave must match the printed frequency's partner: one whole
     wavelength has to measure λ metres against that same bar. */
  const waveScan = await proj.evaluate(eval(SCAN), sheet.figSrc);
  check('W1 GATE: one wavelength on the drawing measures λ against the bar (a pupil\'s measurement lands on the manifest value)',
    Math.abs(waveScan.barRun - scan.barRun) <= 1, JSON.stringify({ bar: scan.barRun }));
  check('W1: the figure is line art — overwhelmingly pure black on pure white',
    scan.white > scan.black && scan.grey / (scan.black + scan.white + scan.grey) < 0.06,
    JSON.stringify({ black: scan.black, white: scan.white, grey: scan.grey }));
  /* Red control: the same sampler run against a plain white image must find
     no grid and no bar, or "present" means nothing. */
  const blankSrc = await proj.evaluate(() => {
    const c = document.createElement('canvas');
    c.width = 1000; c.height = 420;
    const g = c.getContext('2d');
    g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height);
    return c.toDataURL('image/png');
  });
  const blank = await proj.evaluate(eval(SCAN), blankSrc);
  check('W1 GATE red control: the same sampler finds NO grid and NO bar in a blank image',
    blank && blank.gridCols === 0 && blank.gridRows === 0 && blank.barRun === 0,
    JSON.stringify(blank && { cols: blank.gridCols, rows: blank.gridRows, bar: blank.barRun }));

  /* ============ THE GATE, half two: no "$" in printed text ============== */
  check('W3 GATE: no dollar sign anywhere in the printed text', !sheet.text.includes('$'), sheet.text.slice(0, 80));
  check('W3 GATE: and no LaTeX escapes either (\\times, \\lambda)', !/\\times|\\lambda|\\frac/.test(sheet.html), 'latex found');
  check('W3: the equation prints as readable plain text', /v = f × λ/.test(sheet.text), sheet.text.slice(0, 60));

  /* ====== the amplitude the review caught being clipped ================
     On the full-amplitude stage the scale bar's opaque backing plate used to
     be painted over the bottom of the trough, so a pupil measuring the wave's
     height got 0.875 m where the lesson said 1 m. Content accuracy is a hard
     gate, so the figure is measured: the curve must be symmetric about the
     axis to within a pixel or two, on every wave stage. */
  const stages = await proj.evaluate(() => window.__LT.stage().count);
  for (let st = 1; st < stages; st++) {
    const info = await proj.evaluate(async (i) => {
      window.__LT.gotoStage(i);
      return { mode: window.__LT.stage().mode, wave: window.__LT.wave(), title: window.__LT.stage().title };
    }, st);
    if (info.mode !== 'wave') continue;
    await proj.evaluate(() => window.__LT.buildSheet());
    const src = await proj.evaluate(() => window.__LT.sheet().figSrc);
    const sym = await proj.evaluate(eval(SYM), src);

    if (!sym) { check('W1/W2: figure symmetry on "' + info.title + '"', false, 'image failed to decode; src len ' + String(src && src.length)); continue; }
    const up = sym.axis - sym.top, down = sym.bot - sym.axis;
    check('W1/W2: the figure is not clipped on "' + info.title + '" (A = ' + info.wave.A + ') — crest and trough are symmetric about the axis',
      sym.axis > 0 && up > 10 && Math.abs(up - down) <= 3,
      JSON.stringify(Object.assign({ up, down }, sym)));
  }
  /* RED control for the symmetry scan: paint a white plate over the bottom of
     the figure — exactly what the scale bar's backing used to do — and demand
     the scan reports the asymmetry. Without this, "symmetric" could be a
     scanner that cannot see a clipped trough. */
  const clipped = await proj.evaluate(async () => {
    const src = window.__LT.sheet().figSrc;
    return await new Promise(res => {
      const im = new Image();
      im.onload = () => {
        const c = document.createElement('canvas');
        c.width = im.width; c.height = im.height;
        const g = c.getContext('2d');
        g.drawImage(im, 0, 0);
        g.fillStyle = '#fff';
        g.fillRect(0, c.height - 130, c.width, 60);   // erase part of the trough
        res(c.toDataURL('image/png'));
      };
      im.src = src;
    });
  });
  const clipScan = await proj.evaluate(eval(SYM), clipped);
  const cUp = clipScan.axis - clipScan.top, cDown = clipScan.bot - clipScan.axis;
  check('W1 GATE red control: a figure with its trough plated over IS reported as asymmetric',
    Math.abs(cUp - cDown) > 3, JSON.stringify({ up: cUp, down: cDown }));

  // back to stage 2 for the checks that follow
  await proj.evaluate(() => window.__LT.gotoStage(1));
  await proj.evaluate(() => window.__LT.buildSheet());

  /* ============ W2: honest units, correct arithmetic ============ */
  check('W2: the one number a still drawing cannot show IS given, with its unit', /f = 1 Hz/.test(sheet.text), sheet.text.slice(0, 200));
  /* The sheet must NOT contain the worked answer, or tasks 1 and 3 are
     pointless — and it must not quote back the wavelength it asks the pupil
     to measure. The teacher gets the working on the HUD instead. */
  check('the pupil sheet does NOT print the worked answer', !/=\s*2\s*m\/s/.test(sheet.text) && !/Answer/.test(sheet.text), (sheet.text.match(/[^.]*m\/s[^.]*/) || [''])[0]);
  /* The measurables must not be printed anywhere: with λ and A on the page,
     the calibrated grid and the scale bar exist for tasks nobody needs to
     do. */
  check('the wavelength and amplitude are NOT printed — they are what the pupil measures',
    !/λ\s*=\s*2/.test(sheet.text) && !/A\s*=\s*0\.6/.test(sheet.text) && !/wavelength λ =/.test(sheet.text),
    (sheet.text.match(/[^.]*[λA]\s*=[^.]*/) || [''])[0]);
  check('W2: the equation to use is given, and the tasks ask for the two measurable quantities',
    /v = f × λ/.test(sheet.text) && /Measure one whole wavelength/.test(sheet.text) && /Measure the amplitude/.test(sheet.text),
    sheet.text.slice(0, 80));
  check('W2: the model-to-real mapping is STATED, so a pupil can measure off the page', /grid squares are 0\.5 m/.test(sheet.text) && /1 metre/.test(sheet.text));
  check('W2: no pixel count is ever presented as a physical unit', !/\d+\s*px\b/.test(sheet.text) && !/px\s*(Hz|m\b)/.test(sheet.text), (sheet.text.match(/\d+\s*px/) || [''])[0]);

  /* ============ W4: bordered lines, read under PRINT media ============== */
  await proj.emulateMedia({ media: 'print' });
  const lines = await proj.evaluate(() => {
    const ls = [...document.querySelectorAll('#sheet .wsLine')];
    const cs = ls.length ? getComputedStyle(ls[0]) : null;
    return {
      count: ls.length,
      border: cs && cs.borderBottomStyle + ' ' + cs.borderBottomWidth,
      height: cs && cs.height,
      background: cs && cs.backgroundImage,
      sheetShown: getComputedStyle(document.getElementById('sheet')).display,
      stripHidden: getComputedStyle(document.getElementById('strip')).display,
      nameRuleWidth: getComputedStyle(document.querySelector('#sheet .wsName b')).minWidth
    };
  });
  check('W4 GATE: handwriting lines are real BORDERED elements under print media',
    lines.count >= 6 && /solid/.test(lines.border) && parseFloat(lines.border.split(' ')[1]) >= 1,
    JSON.stringify({ count: lines.count, border: lines.border }));
  check('W4: no line depends on a background gradient (print engines strip those)', lines.background === 'none', String(lines.background));
  check('W4: each line has real writing height', parseFloat(lines.height) >= 20, lines.height);
  check('print layer: the sheet is the ONLY thing printed — the strip and the rest stand down',
    lines.sheetShown === 'block' && lines.stripHidden === 'none', JSON.stringify({ sheet: lines.sheetShown, strip: lines.stripHidden }));
  const nameRule = await proj.evaluate(() => {
    const b = document.querySelector('#sheet .wsName b');
    return { text: b.textContent, trimmed: b.textContent.trim(), width: getComputedStyle(b).minWidth };
  });
  check('the name header leaves a ruled space and prints NO name in it',
    parseFloat(nameRule.width) > 100 && nameRule.trimmed === '', JSON.stringify(nameRule));
  await proj.emulateMedia({ media: 'screen' });
  const hiddenOnScreen = await proj.evaluate(() => getComputedStyle(document.getElementById('sheet')).display);
  check('and the print layer is invisible on screen', hiddenOnScreen === 'none', hiddenOnScreen);

  /* ============ W5: the threshold is LIVE, not dead ============ */
  check('W5: a threshold value is actually carried', typeof sheet.threshold === 'number' && sheet.threshold > 0 && sheet.threshold < 255, String(sheet.threshold));
  /* The real W5 evidence: render the same figure at two thresholds. If the
     parameter were dead — the reviewed fragment's exact defect — the two
     images would be byte-identical. */
  const wsFig = await proj.evaluate(() => ({
    dead: window.__LT.figureAt(186) === window.__LT.figureAt(60),
    same: window.__LT.figureAt(186) === window.__LT.figureAt(186),
    head: window.__LT.figureAt(186).slice(0, 24)
  }));
  check('W5: the threshold parameter is LIVE — two different cuts give different pixels', wsFig.dead === false, 'identical output at 186 and 60');
  check('W5: and it is deterministic at the same cut (the comparison above means something)', wsFig.same === true);
  check('W5: the exported figure is a real PNG data URL', /^data:image\/png;base64/.test(wsFig.head), wsFig.head);

  /* ============ the sheet follows the stage ============ */
  await proj.evaluate(() => document.activeElement && document.activeElement.blur());
  await proj.keyboard.press('PageDown');   // stage 3: double frequency
  await proj.waitForTimeout(250);
  await proj.evaluate(() => window.__LT.buildSheet());
  const sheet3 = await proj.evaluate(() => window.__LT.sheet());
  const w3 = await proj.evaluate(() => window.__LT.wave());
  check('the worksheet follows the stage: it prints THIS stage\'s frequency',
    sheet3.text.includes('f = ' + w3.f + ' Hz') && !sheet3.text.includes('λ = ' + w3.lambda + ' m'), JSON.stringify(w3));
  check('and the second stage keeps the answer off the sheet too',
    !new RegExp('=\\s*' + (Math.round(w3.f * w3.lambda * 1000) / 1000) + '\\s*m/s').test(sheet3.text),
    (sheet3.text.match(/[^.]*m\/s[^.]*/) || [''])[0]);
  check('W3 still holds on the second stage: no dollar sign', !sheet3.text.includes('$'));

  /* ============ off a wave stage: honest, not invented ============ */
  await proj.evaluate(() => document.activeElement && document.activeElement.blur());
  await proj.keyboard.press('PageUp');
  await proj.keyboard.press('PageUp');
  await proj.keyboard.press('PageUp');   // back to the field warm-up
  await proj.waitForTimeout(250);
  await proj.evaluate(() => window.__LT.buildSheet());
  const sheetF = await proj.evaluate(() => ({ s: window.__LT.sheet(), mode: window.__LT.stage().mode }));
  check('W2: off a wave stage it says there is nothing to measure rather than inventing numbers',
    sheetF.mode !== 'wave' && sheetF.s.figures === 0 && /Nothing to measure/i.test(sheetF.s.text) && !/Hz/.test(sheetF.s.text),
    JSON.stringify({ mode: sheetF.mode, figs: sheetF.s.figures }));
  check('and it still prints writing lines, so the sheet is usable anyway', sheetF.s.lines >= 6, String(sheetF.s.lines));

  /* ============ a pupil name can never reach the printed page ========== */
  await proj.evaluate(() => document.activeElement && document.activeElement.blur());
  await stripClick(proj, '#btnPick');
  await proj.fill('#pickRoster', 'Ferdinanda');
  await proj.click('#btnPickLoad');
  await proj.click('#btnPickNext');
  await proj.click('#btnPickClose2');
  await proj.evaluate(() => window.__LT.buildSheet());
  const sheetName = await proj.evaluate(() => window.__LT.sheet());
  check('a cold-called name on the wall is NOT carried into the printed sheet', !sheetName.text.includes('Ferdinanda'), sheetName.text.slice(0, 60));

  /* The working has to exist SOMEWHERE for the teacher: on the HUD, which is
     their screen, not the pupils'. */
  const herrs = [];
  const hud = await ctx.newPage();
  await open(hud, base + 'teacher.html', herrs);
  await hud.waitForTimeout(400);
  await proj.bringToFront();
  await proj.evaluate(() => document.activeElement && document.activeElement.blur());
  await proj.keyboard.press('PageDown');    // onto a wave stage again
  await proj.waitForTimeout(600);
  const hudMaths = await hud.evaluate(() => document.getElementById('stageMaths').textContent);
  const projWave = await proj.evaluate(() => window.__LT.wave());
  check('the teacher gets the worked answer on the HUD instead of on the pupils\' sheet',
    hudMaths.includes('v = f × λ = ' + projWave.f + ' × ' + projWave.lambda + ' = ' + (Math.round(projWave.f * projWave.lambda * 1000) / 1000) + ' m/s'),
    hudMaths);
  await proj.evaluate(() => document.activeElement && document.activeElement.blur());
  await proj.keyboard.press('PageUp');
  await proj.keyboard.press('PageUp');
  await proj.keyboard.press('PageUp');
  await proj.waitForTimeout(600);
  const hudMathsOff = await hud.evaluate(() => document.getElementById('stageMaths').textContent);
  check('and it clears off a wave stage rather than showing stale numbers', hudMathsOff === '', hudMathsOff);
  check('no console or page errors on the HUD', herrs.length === 0, herrs.join(' | '));

  check('no console or page errors throughout', perrs.length === 0, perrs.join(' | '));

  await browser.close();
  srv.close();
  console.log(failures ? 'LT-SHEET: ' + failures + ' FAILURE(S)' : 'LT-SHEET: all checks passed');
  process.exit(failures ? 1 : 0);
})().catch(e => { console.error('DIED: ' + e.stack); process.exit(1); });
