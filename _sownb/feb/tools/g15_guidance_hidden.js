#!/usr/bin/env node
"use strict";
const fs = require("node:fs"), path = require("node:path"), crypto = require("node:crypto");
const { pathToFileURL } = require("node:url");
const modules = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES, browserPath = process.env.FEB_CHROMIUM_PATH || process.env.RSH_CHROMIUM_PATH;
if (!modules || !browserPath || !fs.existsSync(browserPath)) throw new Error("proved runtime and FEB_CHROMIUM_PATH/RSH_CHROMIUM_PATH required");
const { chromium } = require(path.join(modules, "playwright"));
const ROOT = path.resolve(__dirname, "../../..");
const selector = '[data-mbm-guide],[data-addressee="staff"],[data-audience="staff"]';
const visibleRows = selector => [...document.querySelectorAll(selector)].map((node, index) => {
  const style = getComputedStyle(node), rect = node.getBoundingClientRect();
  return { number: index + 1, tag: node.tagName.toLowerCase(), key: node.getAttribute("data-mbm-guide") || node.getAttribute("data-addressee") || node.getAttribute("data-audience"), display: style.display, visibility: style.visibility, opacity: +style.opacity, rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height }, painted: style.display !== "none" && style.visibility !== "hidden" && +style.opacity > 0 && rect.width > 0 && rect.height > 0 };
});
(async () => {
  const rel = process.argv[2], outRel = process.argv[3]; if (!rel || !outRel) throw new Error("usage: g15_guidance_hidden.js FILE OUTPUT");
  const file = path.resolve(ROOT, rel), browser = await chromium.launch({ executablePath: browserPath, headless: true, args: ["--no-sandbox"] });
  try {
    const page = await browser.newPage({ viewport: { width: 390, height: 844 }, colorScheme: "light" });
    await page.goto(pathToFileURL(file).href, { waitUntil: "load" });
    const initial = await page.evaluate(visibleRows, selector);
    const mutation = await page.evaluate(selector => {
      const node = document.querySelector(selector); if (!node) return [];
      for (let item = node; item && item !== document.documentElement; item = item.parentElement) {
        item.style.setProperty("display", "block", "important"); item.hidden = false;
      }
      Object.assign(node.style, { position: "fixed", left: "5px", top: "5px", width: "300px", minHeight: "60px", zIndex: "2147483647", background: "white" });
      return [...document.querySelectorAll(selector)].map((candidate, index) => { const s = getComputedStyle(candidate), r = candidate.getBoundingClientRect(); return { number: index + 1, painted: s.display !== "none" && s.visibility !== "hidden" && +s.opacity > 0 && r.width > 0 && r.height > 0 }; });
    }, selector);
    const green = initial.length > 0 && initial.every(row => !row.painted), red = mutation.some(row => row.painted);
    const report = { gate: "g15-rendered-guidance-hidden", candidate: rel, candidateSha256: crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex"), chromiumVersion: await browser.version(), selector, measurement: { keyedCount: initial.length, rows: initial, nonVacuous: initial.length > 0 }, firingControl: { mutation: "unhide the first keyed guidance node and its hidden ancestors in memory", paintedRows: mutation.filter(row => row.painted), fired: red }, status: green && red ? "PASS" : "RED",
      // ATTRIBUTION (ORDER VB-RUN13 H12-4). The stale-evidence sweep keys a verdict
      // to its subject on these two fields. Without them a record states "PASS" with
      // nothing naming what passed, the sweep reports the row as unparseable rather
      // than guessing, and the job fails. That was hand-patched three runs running
      // -- run 11 on 45 records, run 12 on the R4 rollout, run 12 again on six more
      // -- so it is fixed here, at the source, and never in the sweep.
      file: rel,
      subject: `g15 rendered-guidance-hidden on ${rel}` };
    const out = path.resolve(ROOT, outRel); fs.mkdirSync(path.dirname(out), { recursive: true }); fs.writeFileSync(out, JSON.stringify(report, null, 2) + "\n");
    console.log(JSON.stringify({ status: report.status, keyed: initial.length, initiallyPainted: initial.filter(row => row.painted).length, redControlFired: red }, null, 2));
    if (report.status !== "PASS") process.exitCode = 1; await page.close();
  } finally { await browser.close(); }
})().catch(error => { console.error(error.stack || String(error)); process.exitCode = 1; });
