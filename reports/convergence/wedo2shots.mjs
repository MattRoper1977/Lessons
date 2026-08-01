/* The new arrangement, rendered at the viewport it was built for, plus the
   nominal one it also fixes. Before/after pairs for Matt. */
import { createRequire } from 'module';
const require_ = createRequire(import.meta.url);
const { chromium } = require_(process.env.PLAYWRIGHT_PATH || '/opt/node22/lib/node_modules/playwright');
import { mkdirSync } from 'fs';
import { resolve } from 'path';
const LABEL = process.argv[2] || 'after';
const OUT = 'reports/convergence/_wedo2';
mkdirSync(resolve(process.cwd(), OUT), { recursive: true });
const b = await chromium.launch();
for (const [w, h] of [[1280, 720], [1024, 768], [819, 614]]) {
  for (const d of ['SCI_B_W6_Balanced_Plate', 'SCI_B_W7_Where_Food_Comes_From']) {
    const ctx = await b.newContext({ viewport: { width: w, height: h } });
    const p = await ctx.newPage();
    await p.goto('file://' + resolve(process.cwd(), `Science_Teesside/Build/${d}.html`), { waitUntil: 'load' });
    await p.waitForTimeout(800);
    const o = await p.evaluate(() => {
      const st = document.getElementById('wedo2-rule'), sl = st.closest('.slide');
      document.querySelectorAll('.slide').forEach(s => s.classList.remove('active'));
      sl.classList.add('active');
      try { window.GrowAnim.all(st); } catch (e) {}
      return sl.scrollHeight - sl.clientHeight;
    });
    await p.waitForTimeout(500);
    const f = `${OUT}/${d.replace('SCI_B_', '')}--${w}x${h}--${LABEL}.png`;
    await p.screenshot({ path: resolve(process.cwd(), f) });
    console.log(`${d.replace('SCI_B_', '').padEnd(24)} ${w}x${h}  overflow ${String(o).padStart(4)}px  -> ${f}`);
    await ctx.close();
  }
}
await b.close();
