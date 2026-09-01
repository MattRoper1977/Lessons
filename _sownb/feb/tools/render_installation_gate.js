#!/usr/bin/env node
"use strict";

const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const { pathToFileURL } = require("node:url");
const modules = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
const browserPath = process.env.FEB_CHROMIUM_PATH || process.env.RSH_CHROMIUM_PATH;
if (!modules) throw new Error("CODEX_PRIMARY_RUNTIME_NODE_MODULES is absent");
if (!browserPath || !fs.existsSync(browserPath)) throw new Error("FEB_CHROMIUM_PATH/RSH_CHROMIUM_PATH is not the proved Chromium binary");
const { chromium } = require(path.join(modules, "playwright"));
const ROOT = path.resolve(__dirname, "../../..");
const VIEWS = [{ name: "phone", width: 390, height: 844 }, { name: "tablet", width: 768, height: 1024 }, { name: "desktop", width: 1365, height: 900 }];

function sha(file) { return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex"); }
async function settle(page) { await page.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))); }
async function prepareInteriorState(page) {
  const previous = page.locator(".controls button,.controls a").filter({ hasText: /Previous/i }).first();
  const next = page.locator(".controls button,.controls a").filter({ hasText: /Next/i }).first();
  if (await previous.count() && await next.count() && await previous.isDisabled() && await next.isEnabled()) {
    const point = await next.evaluate(node => {
      const rect = node.getBoundingClientRect(), x = rect.left + rect.width / 2, y = rect.top + rect.height / 2;
      const hit = document.elementFromPoint(x, y);
      return hit === node || node.contains(hit) ? { x, y } : null;
    });
    if (point) {
      await page.mouse.click(point.x, point.y);
    } else {
      // A reference may itself have pointer occlusion. Trusted keyboard input still
      // reaches an interior slide so the installation measurement can report it.
      await next.focus();
      await page.keyboard.press("Enter");
    }
    await settle(page);
  }
}
async function boot(page, file, view, blocker = false) {
  await page.setViewportSize({ width: view.width, height: view.height });
  const target = pathToFileURL(file).href;
  try {
    await page.goto(target, { waitUntil: "load", timeout: 30000 });
  } catch (error) {
    if (!String(error).includes("interrupted by another navigation")) throw error;
    await page.waitForTimeout(100);
    await page.goto(target, { waitUntil: "load", timeout: 30000 });
  }
  await page.emulateMedia({ media: "screen", colorScheme: "light" }); await settle(page);
  await prepareInteriorState(page);
  return page.evaluate(blocker => {
    document.querySelectorAll("[data-rsh3-control]").forEach(n => n.removeAttribute("data-rsh3-control"));
    const visible = n => { const s = getComputedStyle(n), r = n.getBoundingClientRect(); return s.display !== "none" && s.visibility !== "hidden" && r.width > 0 && r.height > 0; };
    const controls = [...document.querySelectorAll(".controls button,.controls a,.n6m-guide-btn")].filter(visible);
    controls.forEach((node, index) => node.dataset.rsh3Control = `control-${index + 1}`);
    if (blocker && controls[0]) {
      const r = controls[0].getBoundingClientRect(), b = document.createElement("div");
      b.id = "rsh3-blocker"; Object.assign(b.style, { position: "fixed", left: `${r.left}px`, top: `${r.top}px`, width: `${r.width}px`, height: `${r.height}px`, zIndex: "2147483647", pointerEvents: "auto", background: "rgba(0,0,0,.01)" });
      document.body.appendChild(b);
    }
    return controls.map((node, index) => ({ key: `control-${index + 1}`, label: (node.textContent || node.getAttribute("aria-label") || "").replace(/\s+/g, " ").trim(), tag: node.tagName.toLowerCase(), href: node.getAttribute("href"), disabled: !!node.disabled }));
  }, blocker);
}
async function reach(page, key) {
  return page.evaluate(async key => {
    const node = document.querySelector(`[data-rsh3-control="${key}"]`); if (!node) return { painted: false, samples: [], completeColumns: [], practicalPointerReach: false };
    node.scrollIntoView({ block: "nearest", inline: "center" });
    await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    const rect = node.getBoundingClientRect(), style = getComputedStyle(node);
    const painted = style.display !== "none" && style.visibility !== "hidden" && +style.opacity > 0 && rect.width > 0 && rect.height > 0;
    const samples = [];
    for (let column = 0; column < 5; column++) for (let row = 0; row < 3; row++) {
      const x = rect.left + rect.width * (.1 + column * .2), y = rect.top + rect.height * (.2 + row * .3);
      const hit = document.elementFromPoint(x, y), hitsTarget = !!hit && (hit === node || node.contains(hit));
      samples.push({ column, row, x: +x.toFixed(3), y: +y.toFixed(3), inViewport: x >= 0 && y >= 0 && x < innerWidth && y < innerHeight,
        hitTag: hit?.tagName?.toLowerCase() || null, hitId: hit?.id || null, hitsTarget });
    }
    const completeColumns = [...Array(5).keys()].filter(column => samples.filter(s => s.column === column).every(s => s.inViewport && s.hitsTarget));
    return { rect: { x: +rect.x.toFixed(3), y: +rect.y.toFixed(3), width: +rect.width.toFixed(3), height: +rect.height.toFixed(3) },
      computed: { display: style.display, visibility: style.visibility, opacity: +style.opacity, pointerEvents: style.pointerEvents }, painted, samples,
      grid: "5x3", completeColumns, practicalPointerReach: painted && completeColumns.length > 0 };
  }, key);
}
async function focusCycle(page, keys) {
  await page.evaluate(() => {
    const visible = n => { const s = getComputedStyle(n), r = n.getBoundingClientRect(); return s.display !== "none" && s.visibility !== "hidden" && r.width > 0 && r.height > 0; };
    const nodes = [...document.querySelectorAll('a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])')]
      .filter(visible);
    nodes.forEach((node, index) => node.dataset.rsh3Focus = `focus-${index + 1}`);
    document.body.tabIndex = -1; document.body.focus();
  });
  const seen = [];
  let first = null;
  for (let i = 0; i < 100; i++) {
    await page.keyboard.press("Tab");
    const observation = await page.evaluate(index => {
      const active = document.activeElement;
      if (active && !active.dataset.rsh3Focus) active.dataset.rsh3Focus = `observed-${index + 1}`;
      return { focusKey: active?.dataset?.rsh3Focus || null, gateKey: active?.dataset?.rsh3Control || null };
    }, i);
    if (first && observation.focusKey === first) break;
    if (!first) first = observation.focusKey;
    seen.push(observation);
  }
  const counts = Object.fromEntries(keys.map(key => [key, seen.filter(item => item.gateKey === key).length]));
  return { expectedFocusableCount: seen.length, observations: seen, counts, completedOneCycle: !!first && seen.length < 100 };
}
async function trustedActivation(page, key, pointerPoint = null) {
  await page.evaluate(key => {
    window.__rsh3Events = [];
    document.addEventListener("click", event => { const target = event.target.closest?.("[data-rsh3-control]"); if (target) window.__rsh3Events.push({ key: target.dataset.rsh3Control, isTrusted: event.isTrusted }); }, true);
    document.addEventListener("click", event => { const a = event.target.closest?.("a[data-rsh3-control]"); if (a) event.preventDefault(); }, true);
  }, key);
  try {
    if (pointerPoint) await page.mouse.click(pointerPoint.x, pointerPoint.y);
    else { await page.locator(`[data-rsh3-control="${key}"]`).focus(); await page.keyboard.press("Enter"); }
    await settle(page);
    return await page.evaluate(key => ({ events: window.__rsh3Events || [], trusted: (window.__rsh3Events || []).some(e => e.key === key && e.isTrusted), navigated: false }), key);
  } catch (error) {
    return { events: [], trusted: false, navigated: true, error: String(error) };
  }
}
function localNavigationSafe(row) { return !row.href || !/^(?:https?:)?\/\//i.test(row.href); }

async function runCandidate(browser, file, blockFirst = false) {
  const viewports = [];
  for (const view of VIEWS) {
    const page = await browser.newPage({ viewport: { width: view.width, height: view.height }, colorScheme: "light" });
    const controls = await boot(page, file, view, blockFirst);
    const keys = controls.map(r => r.key), cycle = await focusCycle(page, keys), rows = [];
    for (const control of controls) {
      await boot(page, file, view, blockFirst);
      const pointerReach = await reach(page, control.key);
      const sample = pointerReach.samples.find(s => pointerReach.completeColumns.includes(s.column) && s.row === 1);
      const pointer = sample ? await trustedActivation(page, control.key, { x: sample.x, y: sample.y }) : { events: [], trusted: false };
      await boot(page, file, view, blockFirst);
      const keyboard = await trustedActivation(page, control.key, null);
      const exactFocus = cycle.counts[control.key] === 1;
      const safe = localNavigationSafe(control);
      const passed = !control.disabled && pointerReach.practicalPointerReach && pointer.trusted && exactFocus && keyboard.trusted && safe;
      rows.push({ ...control, pointer: { reach: pointerReach, trustedEvent: pointer.trusted }, keyboard: { exactFocus, cycleHits: cycle.counts[control.key], trustedEvent: keyboard.trusted }, navigationSafe: safe, status: passed ? "PASS" : "RED" });
    }
    viewports.push({ viewport: view, focusCycle: cycle, rows }); await page.close();
  }
  const rows = viewports.flatMap(v => v.rows);
  return { viewports, rowsMet: rows.filter(r => r.status === "PASS").length, rowsRed: rows.filter(r => r.status === "RED").length,
    status: rows.every(r => r.status === "PASS") && rows.length > 0 ? "PASS" : "RED" };
}

(async () => {
  const relative = process.argv[2], output = process.argv[3]; if (!relative || !output) throw new Error("usage: render_installation_gate.js FILE OUTPUT");
  const file = path.resolve(ROOT, relative), browser = await chromium.launch({ executablePath: browserPath, headless: true, args: ["--no-sandbox", "--disable-dev-shm-usage"] });
  try {
    const candidate = await runCandidate(browser, file, false), red = await runCandidate(browser, file, true);
    const report = { gate: "render-installation", candidate: relative, candidateSha256: sha(file), chromiumVersion: await browser.version(),
      rule: "each control paints, has one complete 3-point interior column in a 5x3 grid, receives a trusted pointer click, appears exactly once in the Tab cycle, and receives a trusted keyboard click",
      measurement: candidate, redControl: { mutation: "opaque hit-test blocker over the first control", measurement: red,
        fired: red.status === "RED" && red.rowsRed > candidate.rowsRed },
      status: candidate.status === "PASS" && red.status === "RED" && red.rowsRed > candidate.rowsRed ? "PASS" : "RED" };
    const out = path.resolve(ROOT, output); fs.mkdirSync(path.dirname(out), { recursive: true }); fs.writeFileSync(out, JSON.stringify(report, null, 2) + "\n");
    console.log(JSON.stringify({ gate: report.gate, status: report.status, rowsMet: candidate.rowsMet, rowsRed: candidate.rowsRed, redControlFired: report.redControl.fired }, null, 2));
    if (report.status !== "PASS") process.exitCode = 1;
  } finally { await browser.close(); }
})().catch(error => { console.error(error.stack || String(error)); process.exitCode = 1; });
