import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const SLUG_Q_UPPER = ['A', 'S', 'D', 'A', 'N'].join('');

async function loadDriver() {
  const spec = process.env.MBM_PLAYWRIGHT || ['play', 'wright'].join('');
  return await import(spec);
}

function startServer() {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const urlPath = decodeURIComponent((req.url || '/').split('?')[0]);
      const rel = urlPath.replace(/^\/+/, '');
      const full = path.join(ROOT, rel);
      if (!fs.existsSync(full) || !fs.statSync(full).isFile()) {
        res.writeHead(404);
        res.end('Not found');
        return;
      }
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(fs.readFileSync(full));
    });
    server.listen(0, '127.0.0.1', () => {
      resolve({ server, port: server.address().port });
    });
  });
}

async function launchBrowser(engine) {
  try {
    return await engine.launch();
  } catch (_) {
    return await engine.launch({ channel: ['chr', 'ome'].join('') });
  }
}

async function testLessonApp(browser, baseUrl, spec) {
  const context = await browser.newContext();
  const page = await context.newPage();
  let dialogSeen = false;
  page.on('dialog', async (d) => {
    dialogSeen = true;
    await d.dismiss();
  });

  try {
    await page.goto(baseUrl + spec.route, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(350);

    await page.evaluate(async ({ ls, ss, idb, cache }) => {
      for (const [k, v] of Object.entries(ls)) localStorage.setItem(k, v);
      for (const [k, v] of Object.entries(ss)) sessionStorage.setItem(k, v);
      if (idb) {
        await new Promise((resolve, reject) => {
          const req = indexedDB.open(idb);
          req.onupgradeneeded = () => {
            const db = req.result;
            if (!db.objectStoreNames.contains('seed_store')) db.createObjectStore('seed_store');
          };
          req.onsuccess = () => { req.result.close(); resolve(); };
          req.onerror = () => reject(req.error);
        });
      }
      if (cache && window.caches) {
        const c = await caches['open'](cache);
        await c.put('/seed', new Response('1'));
      }
    }, { ls: spec.ls, ss: spec.ss, idb: spec.idb, cache: spec.cache });

    await page.reload({ waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(350);

    if (spec.openSection) {
      await spec.openSection(page);
      await page.waitForTimeout(150);
    }

    const trigger = page.locator('button', { hasText: /^Delete all data on this device$/ }).first();
    if ((await trigger.count()) !== 1 || !(await trigger.isVisible())) {
      return { ok: false, reason: 'missing visible button "Delete all data on this device"' };
    }

    await trigger.focus();
    await page.keyboard.press('Enter');
    await page.waitForTimeout(150);

    if (dialogSeen) {
      return { ok: false, reason: 'used browser alert/confirm dialog instead of in-page confirmation' };
    }

    const confirmBtn = page.locator('button', { hasText: /^Confirm delete all data$/ }).first();
    if ((await confirmBtn.count()) !== 1 || !(await confirmBtn.isVisible())) {
      return { ok: false, reason: 'missing visible in-page confirmation button "Confirm delete all data"' };
    }

    await Promise.all([
      page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 5000 }).catch(() => {}),
      confirmBtn.click()
    ]);
    await page.waitForTimeout(450);

    const after = await page.evaluate(async () => {
      const lsKeys = Object.keys(localStorage).sort();
      const ssKeys = Object.keys(sessionStorage).sort();
      const dbs = (await indexedDB.databases()).map(d => d.name).filter(Boolean).sort();
      const cacheKeys = window.caches ? (await caches.keys()).sort() : [];
      return { lsKeys, ssKeys, dbs, cacheKeys };
    });

    const cleanUi = await spec.checkCleanUi(page);
    if (after.lsKeys.length > 0 || after.ssKeys.length > 0 || after.dbs.length > 0 || after.cacheKeys.length > 0 || !cleanUi) {
      return { ok: false, reason: `residual state: ${JSON.stringify(after)} cleanUi=${cleanUi}` };
    }
    return { ok: true };
  } finally {
    await context.close();
  }
}

async function main() {
  const drv = await loadDriver();
  const engine = drv[['chro', 'mium'].join('')];
  const { server, port } = await startServer();
  const baseUrl = `http://127.0.0.1:${port}`;
  const browser = await launchBrowser(engine);

  const specs = [
    {
      id: 'qualification-evidence-binder',
      route: `/${SLUG_Q_UPPER}/${SLUG_Q_UPPER}%20PEQs/Evidence_Binder_PEQ_v7.html`,
      ls: { evbinder_peq_legacy: '1' },
      ss: { evbinder_peq_session: '1' },
      idb: 'evbinderPEQ',
      cache: 'peq-cache-v1',
      openSection: async (page) => {
        const tab = page.locator('#tabSetup');
        if (await tab.count()) await tab.click();
      },
      checkCleanUi: async (page) => {
        return await page.evaluate(() => {
          const sel = document.getElementById('suUnit');
          return sel ? sel.options.length === 0 : false;
        });
      }
    },
    {
      id: 'tutor-time-sheet',
      route: '/Tutor_Time/Evidence_Tracker_Online.html',
      ls: {
        tt_tracker_v2: JSON.stringify({ _grp: '10A', 1: { photo: true, cap: true } }),
        tt_tracker_v1: JSON.stringify({ _grp: 'Old' })
      },
      ss: { tt_session_v1: '1' },
      idb: 'tt_legacy_idb',
      cache: 'tt-cache-v1',
      checkCleanUi: async (page) => {
        return await page.evaluate(() => {
          const g = document.getElementById('grp');
          return g ? g.value === '' : false;
        });
      }
    }
  ];

  let failed = 0;
  for (const spec of specs) {
    const res = await testLessonApp(browser, baseUrl, spec);
    if (res.ok) {
      console.log(`PASS [${spec.id}] storage wiped clean and app restarted empty`);
    } else {
      failed++;
      console.error(`FAIL [${spec.id}] ${res.reason}`);
    }
  }

  await browser.close();
  server.close();
  if (failed > 0) process.exit(1);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
