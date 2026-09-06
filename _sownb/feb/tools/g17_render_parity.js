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
const CONFIG = path.join(ROOT, "_sownb/G17_GROW_SCIENCE_FEB.json");
const VIEWPORTS = [
  { name: "phone390", width: 390, height: 844 },
  { name: "tablet768", width: 768, height: 1024 },
  { name: "desktop1365", width: 1365, height: 900 },
];
const REFERENCES = {
  "GROW Science": "Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W13B_Rover_Rescue_Investigation_Do.html",
};

async function growScienceWordBands(browser) {
  const directory = path.join(ROOT, "Science_Teesside/Grow/W8-W13_2026-27");
  const files = fs.readdirSync(directory).filter(name => /^SCI_.*\.html$/.test(name)).sort();
  if (files.length < 2) throw new Error("MEASUREMENT INVALID: fewer than two GROW Science reference lessons");
  const samples = [];
  for (const name of files) {
    const relative = path.relative(ROOT, path.join(directory, name));
    const page = await browser.newPage({ viewport: { width: 390, height: 844 }, colorScheme: "light" });
    await page.goto(pathToFileURL(path.join(directory, name)).href, { waitUntil: "load", timeout: 30000 });
    await settle(page);
    const words = await page.evaluate(() => [...document.querySelectorAll("main.deck > section.slide")].map(source => {
      const node = source.cloneNode(true);
      node.querySelectorAll("script,style,noscript,template,svg,[data-mbm-guide],[data-audience='staff'],.hero-visual").forEach(item => item.remove());
      return ((node.textContent || "").normalize("NFKC").match(/[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*/g) || []).length;
    }));
    await page.close();
    if (words.length !== 9) throw new Error(`MEASUREMENT INVALID: ${relative} has ${words.length} slides`);
    samples.push({ path: relative, words });
  }
  return [...Array(9)].map((_, index) => {
    const sample = samples.map(row => row.words[index]).sort((a, b) => a - b);
    return { slide: index + 1, sample, low: Math.max(40, Math.floor(sample[0] * .70)), high: Math.ceil(sample[sample.length - 1] * 1.50) };
  });
}

function digest(file) { return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex"); }
function rootTokens(source) {
  const rows = [];
  for (const block of [...source.matchAll(/:root\s*\{([^}]*)\}/gs)].map(match => match[1])) {
    for (const match of block.matchAll(/(--[\w-]+)\s*:\s*([^;}]*)/g)) rows.push({ name: match[1], value: match[2].trim() });
  }
  return rows;
}
async function settle(page) { await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))); }

async function screenSurface(browser, file, viewport, defect) {
  const page = await browser.newPage({ viewport: { width: viewport.width, height: viewport.height }, colorScheme: "light" });
  await page.goto(pathToFileURL(file).href, { waitUntil: "load", timeout: 30000 });
  await page.emulateMedia({ media: "screen", colorScheme: "light" });
  if (defect) await page.addStyleTag({ content: ".controls button:first-of-type,.controls a:first-of-type{display:none!important}" });
  await settle(page);
  const count = await page.locator("main.deck > section.slide").count();
  const slides = [];
  for (let index = 0; index < count; index += 1) {
    const row = await page.evaluate(index => {
      const all = [...document.querySelectorAll("main.deck > section.slide")];
      all.forEach((slide, i) => {
        const on = i === index;
        slide.hidden = !on;
        slide.classList.toggle("active", on);
        slide.classList.toggle("on", on);
        slide.setAttribute("aria-hidden", String(!on));
      });
      const active = all[index];
      const visible = node => {
        const style = getComputedStyle(node), rect = node.getBoundingClientRect();
        return style.display !== "none" && style.visibility !== "hidden" && rect.width > 0 && rect.height > 0;
      };
      const controls = [...document.querySelectorAll(".controls button,.controls a")].filter(visible);
      const clone = active.cloneNode(true);
      clone.querySelectorAll("script,style,noscript,template,svg,[data-mbm-guide],[data-audience='staff'],.hero-visual").forEach(node => node.remove());
      const words = (clone.textContent || "").normalize("NFKC").match(/[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*/g) || [];
      const dimensions = controls.map(node => {
        const rect = node.getBoundingClientRect(); return Math.min(rect.width, rect.height);
      });
      return {
        slide: index + 1,
        pupilWords: words.length,
        controlCount: controls.length,
        minControl: dimensions.length ? Math.min(...dimensions) : null,
        overflowPx: Math.max(0, document.documentElement.scrollWidth - innerWidth, document.body.scrollWidth - innerWidth),
      };
    }, index);
    slides.push(row);
  }
  await page.close();
  return { viewport, slideCount: count, slides };
}

async function printSurface(browser, file) {
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, colorScheme: "light" });
  await page.goto(pathToFileURL(file).href, { waitUntil: "load", timeout: 30000 });
  await page.emulateMedia({ media: "print", colorScheme: "light" });
  await page.addStyleTag({ content: "@media print{html,body{color-scheme:light!important}}" });
  await settle(page);
  const result = await page.evaluate(() => {
    const visible = node => {
      const s = getComputedStyle(node), r = node.getBoundingClientRect();
      return s.display !== "none" && s.visibility !== "hidden" && r.width > 0 && r.height > 0;
    };
    const pages = [...document.querySelectorAll(".print-pack .print-page")].filter(visible);
    return {
      innerWidth, innerHeight,
      printPageElements: pages.length,
      printPackVisible: [...document.querySelectorAll(".print-pack")].some(visible),
      horizontalOverflowPx: Math.max(0, document.documentElement.scrollWidth - innerWidth, document.body.scrollWidth - innerWidth),
      confirmation: (document.body.innerText || "").includes("I confirm this is my own work."),
    };
  });
  await page.close();
  return result;
}

async function measureFile(browser, relative, defect = false) {
  const file = path.resolve(ROOT, relative); const source = fs.readFileSync(file, "utf8");
  const viewports = [];
  for (const viewport of VIEWPORTS) viewports.push(await screenSurface(browser, file, viewport, defect));
  return { path: relative, sha256: digest(file), cssTokens: rootTokens(source), viewports, print: await printSurface(browser, file) };
}

function evaluate(config, candidate) {
  const rows = [];
  const currentReferenceHash = digest(path.resolve(ROOT, config.reference));
  rows.push({ metric: "family reference binding", reference: config.referenceSha256, candidate: currentReferenceHash,
    status: currentReferenceHash === config.referenceSha256 ? "PASS" : "RED" });
  for (const surface of candidate.viewports) {
    const ref = config.render.viewports.find(row => row.viewport.name === surface.viewport.name);
    rows.push({ metric: `${surface.viewport.name} slide count`, reference: ref.slideCount, candidate: surface.slideCount,
      status: surface.slideCount === ref.slideCount && surface.slideCount === 9 ? "PASS" : "RED" });
    for (const slide of surface.slides) {
      const expected = ref.slides[slide.slide - 1];
      rows.push({ metric: `${surface.viewport.name} slide ${slide.slide} control count`, reference: expected.controlCount,
        candidate: slide.controlCount, status: slide.controlCount === expected.controlCount ? "PASS" : "RED" });
      rows.push({ metric: `${surface.viewport.name} slide ${slide.slide} overflow`, reference: 0,
        candidate: slide.overflowPx, status: slide.overflowPx === 0 ? "PASS" : "RED" });
    }
  }
  const first = candidate.viewports[0].slides;
  for (const slide of first) {
    const band = config.wordBands[slide.slide - 1];
    rows.push({ metric: `slide ${slide.slide} pupil words`, reference: band.sample, band: [band.low, band.high],
      candidate: slide.pupilWords, status: slide.pupilWords >= band.low && slide.pupilWords <= band.high ? "PASS" : "RED" });
  }
  const candidateNames = new Set(candidate.cssTokens.map(row => row.name));
  const missing = config.tokenNames.filter(name => !candidateNames.has(name));
  rows.push({ metric: "family token carriers", reference: config.tokenNames, candidate: [...candidateNames].sort(), missing,
    status: missing.length ? "RED" : "PASS" });
  const expectedPrint = config.render.print.printPageElements + ((candidate.print.confirmation && !config.render.print.confirmation) ? 1 : 0);
  rows.push({ metric: "A4 print-page element count", reference: config.render.print.printPageElements,
    candidate: candidate.print.printPageElements, expected: expectedPrint,
    status: candidate.print.printPageElements === expectedPrint ? "PASS" : "RED" });
  rows.push({ metric: "A4 print pack installed", reference: true, candidate: candidate.print.printPackVisible,
    status: candidate.print.printPackVisible ? "PASS" : "RED" });
  return { rows, rowsMet: rows.filter(row => row.status === "PASS").length,
    rowsRed: rows.filter(row => row.status === "RED").length,
    status: rows.every(row => row.status === "PASS") ? "PASS" : "RED" };
}

(async () => {
  const command = process.argv[2];
  const browser = await chromium.launch({ executablePath: browserPath, headless: true,
    args: ["--no-sandbox", "--disable-dev-shm-usage"] });
  try {
    if (command === "derive") {
      const output = path.resolve(ROOT, process.argv[3]); const families = {};
      for (const [family, relative] of Object.entries(REFERENCES)) {
        const render = await measureFile(browser, relative);
        families[family] = { reference: relative, referenceSha256: render.sha256, render,
          tokenNames: [...new Set(render.cssTokens.map(row => row.name))].sort(),
          wordBands: await growScienceWordBands(browser) };
        process.stdout.write(`DERIVED ${family}\n`);
      }
      fs.mkdirSync(path.dirname(output), { recursive: true });
      fs.writeFileSync(output, JSON.stringify({ schema: "feb-g17-grow-science-v1", chromiumVersion: await browser.version(), families }, null, 2) + "\n");
    } else if (command === "measure") {
      const family = process.argv[3], relative = process.argv[4], output = path.resolve(ROOT, process.argv[5]);
      if (family !== "GROW Science") throw new Error("MEASUREMENT INVALID: g17 is GROW-Science-only; use render-installation for other families");
      const config = JSON.parse(fs.readFileSync(CONFIG, "utf8")).families[family];
      const greenMeasured = await measureFile(browser, relative, false);
      const redMeasured = await measureFile(browser, relative, true);
      const green = evaluate(config, greenMeasured), red = evaluate(config, redMeasured);
      const report = { gate: "g17-grow-science-render-parity", route: "parameterised", family, candidate: relative,
        reference: config.reference, greenMeasurement: green,
        redControl: { mutation: "hide first control-bar item on this family's own candidate", measurement: red,
          fired: red.status === "RED" && red.rowsRed > green.rowsRed },
        status: green.status === "PASS" && red.status === "RED" && red.rowsRed > green.rowsRed ? "PASS" : "RED" };
      fs.mkdirSync(path.dirname(output), { recursive: true }); fs.writeFileSync(output, JSON.stringify(report, null, 2) + "\n");
      console.log(JSON.stringify({ gate: report.gate, family, status: report.status, rowsMet: green.rowsMet,
        rowsRed: green.rowsRed, redControlFired: report.redControl.fired }, null, 2));
      if (report.status !== "PASS") process.exitCode = 1;
    } else throw new Error("usage: g17_family_parity.js derive RAW.json | measure FAMILY CANDIDATE OUTPUT");
  } finally { await browser.close(); }
})().catch(error => { console.error(error.stack || String(error)); process.exitCode = 1; });
