/* JOB 3 — constrain the pixel-diff story instead of narrating it.
 *
 * The claim was: slides that moved are the ones carrying a stage, and slides
 * that are pixel-identical to main are the ones carrying none. That is a
 * partition, so it can be tested rather than asserted.
 *
 *   node reports/convergence/pixelsets.mjs <beforeShotsDir> <afterShotsDir>
 *
 * Prints the two set comparisons and names every slide that belongs to neither
 * side of the partition, which is the interesting case.
 */
import { createRequire } from 'module';
const require_ = createRequire(import.meta.url);
const { chromium } = require_(process.env.PLAYWRIGHT_PATH || '/opt/node22/lib/node_modules/playwright');
import { readFileSync, readdirSync, writeFileSync, existsSync } from 'fs';
import { resolve } from 'path';

const [A, B] = [process.argv[2], process.argv[3]];
const ROOT = process.cwd();
const LESSONS = {
  SCI_B_W3_Backbones: 'Science_Teesside/Build/SCI_B_W3_Backbones.html',
  SCI_B_W4_Muscle_Pairs: 'Science_Teesside/Build/SCI_B_W4_Muscle_Pairs.html',
  SCI_B_W5_Right_Nutrition: 'Science_Teesside/Build/SCI_B_W5_Right_Nutrition.html',
  SCI_B_W6_Balanced_Plate: 'Science_Teesside/Build/SCI_B_W6_Balanced_Plate.html',
  SCI_B_W7_Where_Food_Comes_From: 'Science_Teesside/Build/SCI_B_W7_Where_Food_Comes_From.html'
};

const browser = await chromium.launch();
const page = await (await browser.newContext()).newPage();

/* which slides carry a stage — read from the lesson, not assumed */
const carries = {};
for (const [name, rel] of Object.entries(LESSONS)) {
  await page.goto('file://' + resolve(ROOT, rel), { waitUntil: 'load' });
  await page.waitForTimeout(700);
  /* Two predicates, because the first one turned out to be too narrow. A slide
     "carries a stage" if it has a .g-stage or a prediction panel. But the
     engine also builds the motion-key panel, the story strip, the We Do panel
     and the retrieval grid, and those move for the same reason a stage does.
     Both are recorded so the partition can be tested against each. */
  carries[name] = await page.evaluate(() =>
    [...document.querySelectorAll('.slide')].map(s => ({
      stage: !!s.querySelector('.g-stage, .ba-stage, .g-predict, .ba-predict'),
      engine: !!s.querySelector('.g-stage, .ba-stage, .g-predict, .ba-predict,' +
        '.g-key, .ba-key, .g-story, .g-wedo, .g-retrieve, .g-misc'),
      components: [...s.querySelectorAll('[class]')]
        .map(e => (e.getAttribute('class') || '').split(/\s+/))
        .flat().filter(c => /^(g|ba)-(stage|predict|key|story|wedo|retrieve|misc)$/.test(c))
        .filter((v, i, a) => a.indexOf(v) === i)
    })));
}

/* pixel difference per slide */
const rows = [];
for (const dir of Object.keys(LESSONS)) {
  if (!existsSync(`${A}/${dir}`)) continue;
  for (const f of readdirSync(`${A}/${dir}`).sort()) {
    const a = readFileSync(`${A}/${dir}/${f}`).toString('base64');
    const b = readFileSync(`${B}/${dir}/${f}`).toString('base64');
    const pct = await page.evaluate(async ([x, y]) => {
      const load = s => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.src = 'data:image/png;base64,' + s; });
      const [ia, ib] = await Promise.all([load(x), load(y)]);
      const c1 = new OffscreenCanvas(ia.width, ia.height), c2 = new OffscreenCanvas(ib.width, ib.height);
      c1.getContext('2d').drawImage(ia, 0, 0); c2.getContext('2d').drawImage(ib, 0, 0);
      const d1 = c1.getContext('2d').getImageData(0, 0, ia.width, ia.height).data;
      const d2 = c2.getContext('2d').getImageData(0, 0, ib.width, ib.height).data;
      let n = 0;
      for (let i = 0; i < d1.length; i += 4)
        if (Math.abs(d1[i] - d2[i]) + Math.abs(d1[i+1] - d2[i+1]) + Math.abs(d1[i+2] - d2[i+2]) > 24) n++;
      return +(100 * n / (d1.length / 4)).toFixed(3);
    }, [a, b]);
    const idx = parseInt(f.match(/(\d+)/)[1], 10) - 1;
    rows.push({ lesson: dir, slide: idx + 1, file: `${dir}/${f}`, pct,
      stage: carries[dir][idx].stage, engine: carries[dir][idx].engine,
      components: carries[dir][idx].components });
  }
}
await browser.close();

const moved = rows.filter(r => r.pct > 0);
const identical = rows.filter(r => r.pct === 0);
const withStage = rows.filter(r => r.stage);
const without = rows.filter(r => !r.stage);
const withEngine = rows.filter(r => r.engine);
const withoutEngine = rows.filter(r => !r.engine);

const movedNoStage = moved.filter(r => !r.stage);
const stageNotMoved = withStage.filter(r => r.pct === 0);
const identicalWithStage = identical.filter(r => r.stage);
const withoutNotIdentical = without.filter(r => r.pct > 0);

const out = {
  slides: rows.length,
  moved: moved.length, identical: identical.length,
  withStage: withStage.length, withoutStage: without.length,
  movedEqualsStages: movedNoStage.length === 0 && stageNotMoved.length === 0,
  identicalEqualsStageless: identicalWithStage.length === 0 && withoutNotIdentical.length === 0,
  exceptions: {
    movedButNoStage: movedNoStage.map(r => `${r.file} (${r.pct}%)`),
    hasStageButIdentical: stageNotMoved.map(r => r.file),
    noStageButMoved: withoutNotIdentical.map(r => `${r.file} (${r.pct}%)`)
  },
  movedEqualsEngineBuilt: moved.filter(r => !r.engine).length === 0 &&
                          withEngine.filter(r => r.pct === 0).length === 0,
  identicalEqualsNotEngineBuilt: identical.filter(r => r.engine).length === 0 &&
                                 withoutEngine.filter(r => r.pct > 0).length === 0,
  engineExceptions: {
    movedButNoEngineComponent: moved.filter(r => !r.engine).map(r => `${r.file} (${r.pct}%)`),
    engineComponentButIdentical: withEngine.filter(r => r.pct === 0).map(r => r.file)
  },
  withEngine: withEngine.length, withoutEngine: withoutEngine.length,
  rows
};
writeFileSync(resolve(ROOT, 'reports/convergence/_data/pixel-sets.json'), JSON.stringify(out, null, 1));

console.log(`slides ${out.slides}  moved ${out.moved}  identical ${out.identical}` +
  `  withStage ${out.withStage}  stageless ${out.withoutStage}`);
console.log(`moved == set-with-stages?        ${out.movedEqualsStages}`);
console.log(`identical == set-without-stages? ${out.identicalEqualsStageless}`);
for (const [k, v] of Object.entries(out.exceptions)) {
  console.log(`  ${k}: ${v.length ? v.join(', ') : 'none'}`);
}
console.log(`\nwider predicate — any engine-built component (stage, predict, key, story, wedo, retrieve):`);
console.log(`  withEngineComponent ${out.withEngine}  without ${out.withoutEngine}`);
console.log(`  moved == engine-built?      ${out.movedEqualsEngineBuilt}`);
console.log(`  identical == not-built?     ${out.identicalEqualsNotEngineBuilt}`);
for (const [k, v] of Object.entries(out.engineExceptions)) {
  console.log(`  ${k}: ${v.length ? v.join(', ') : 'none'}`);
}
const odd = rows.filter(r => !r.engine && r.pct > 0);
if (odd.length) {
  console.log('\nslides in neither set, with what they do carry:');
  odd.forEach(r => console.log(`  ${r.file}  ${r.pct}%  components=[${r.components.join(',')}]`));
}
