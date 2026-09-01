#!/usr/bin/env node
"use strict";

const fs = require("node:fs");
const crypto = require("node:crypto");
const path = require("node:path");
const { pathToFileURL } = require("node:url");

const runtimeModules = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
const browserBinary = process.env.RSH_CHROMIUM_PATH;
if (!runtimeModules) throw new Error("CODEX_PRIMARY_RUNTIME_NODE_MODULES is absent");
if (!browserBinary || !fs.existsSync(browserBinary)) throw new Error("RSH_CHROMIUM_PATH must name the proved Chromium 149 binary");
const { chromium } = require(path.join(runtimeModules, "playwright"));

const repo = path.resolve(__dirname, "../../..");
const mode = process.argv[2] || "references";
const candidatePath = process.argv[3] || null;
const outRoot = path.join(repo, "_sownb/rsh/output", mode);

const references = [
  ["grow-asdan", "GROW ASDAN", "GROW_ASDAN/Autumn2_W1-W6_2026-27/PEQ_A2_W6_My_Future_Profile_Now_Next_Maybe_GROW_v3_40min.html"],
  ["grow-science", "GROW Science", "Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W13B_Rover_Rescue_Investigation_Do.html"],
  ["launch-asdan", "LAUNCH ASDAN", "LAUNCH_ASDAN/W7-W12_2026-27/lessons/PEQ/PEQ_W12_Review_My_Teamwork_Progress_Evidence_Next_Action_LAUNCH.html"],
  ["launch-science", "LAUNCH Science", "Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W13L3_Inheritance_Probability_Do.html"],
];
const targets = mode === "references"
  ? references
  : [[mode, "GROW Science candidate", candidatePath]];
const viewports = [
  { name: "phone", width: 390, height: 844 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "desktop", width: 1365, height: 768 },
];

function sourceTokens(text) {
  const rows = [];
  const rootBlocks = [...text.matchAll(/:root\s*\{([^}]*)\}/g)].map(match => match[1]);
  for (const block of rootBlocks) {
    for (const match of block.matchAll(/(--[\w-]+)\s*:\s*([^;}]*)/g)) {
      rows.push({ name: match[1], value: match[2].trim() });
    }
  }
  return rows;
}

async function activate(page, index, bottom) {
  return page.evaluate(({ index, bottom }) => {
    const slides = [...document.querySelectorAll("main.deck > section.slide")];
    slides.forEach((slide, i) => {
      const on = i === index;
      slide.classList.toggle("active", on);
      slide.classList.toggle("on", on);
      slide.hidden = !on;
      slide.setAttribute("aria-hidden", String(!on));
    });
    const active = slides[index];
    document.documentElement.style.scrollBehavior = "auto";
    document.documentElement.scrollTop = 0;
    document.body.scrollTop = 0;
    window.scrollTo(0, 0);
    active.scrollTop = 0;
    if (bottom) {
      active.scrollTop = Math.max(0, active.scrollHeight - active.clientHeight);
      window.scrollTo(0, Math.max(0, Math.max(document.body.scrollHeight, document.documentElement.scrollHeight) - innerHeight));
    }
    return {
      activeScrollTop: active.scrollTop,
      windowScrollY: window.scrollY,
      activeScrollHeight: active.scrollHeight,
      activeClientHeight: active.clientHeight,
    };
  }, { index, bottom });
}

async function metrics(page, index) {
  return page.evaluate(index => {
    const slides = [...document.querySelectorAll("main.deck > section.slide")];
    const active = slides[index];
    const visible = node => {
      const style = getComputedStyle(node), rect = node.getBoundingClientRect();
      return style.display !== "none" && style.visibility !== "hidden" && rect.width > 0 && rect.height > 0;
    };
    const controls = [...document.querySelectorAll("button,a,[role=button]")].filter(visible);
    const controlBar = [...document.querySelectorAll(".controls button,.controls a")].filter(visible);
    const text = (active?.innerText || "").replace(/\s+/g, " ").trim();
    const words = text.match(/[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*/g) || [];
    const overflowNodes = [...document.querySelectorAll("body *")].filter(visible).filter(node => {
      const rect = node.getBoundingClientRect();
      return node.scrollWidth > node.clientWidth + 1 || rect.right > innerWidth + 1 || rect.left < -1;
    }).slice(0, 25).map(node => ({
      tag: node.tagName.toLowerCase(), id: node.id,
      className: String(node.className || "").slice(0, 120),
      scrollWidth: node.scrollWidth, clientWidth: node.clientWidth,
      left: +node.getBoundingClientRect().left.toFixed(2),
      right: +node.getBoundingClientRect().right.toFixed(2),
    }));
    const dimensions = controls.map(node => {
      const rect = node.getBoundingClientRect();
      return {
        text: (node.textContent || node.getAttribute("aria-label") || "").replace(/\s+/g, " ").trim(),
        width: +rect.width.toFixed(2), height: +rect.height.toFixed(2),
        minDimension: +Math.min(rect.width, rect.height).toFixed(2),
      };
    });
    const guideNodes = [...document.querySelectorAll("[data-mbm-guide]")];
    const guideShown = guideNodes.filter(visible);
    return {
      index,
      title: active?.dataset.title || active?.querySelector("h1,h2")?.textContent?.trim() || "",
      text,
      wordCount: words.length,
      slideCount: slides.length,
      bodyScrollWidth: document.body.scrollWidth,
      documentScrollWidth: document.documentElement.scrollWidth,
      horizontalOverflowPx: Math.max(0, document.body.scrollWidth - innerWidth, document.documentElement.scrollWidth - innerWidth),
      overflowNodes,
      visibleControlCount: controls.length,
      controlBarButtonCount: controlBar.length,
      controlBarStrings: controlBar.map(node => (node.textContent || node.getAttribute("aria-label") || "").replace(/\s+/g, " ").trim()),
      minVisibleControl: dimensions.length ? dimensions.reduce((a, b) => a.minDimension <= b.minDimension ? a : b) : null,
      guideNodeCount: guideNodes.length,
      guideVisibleByDefault: guideShown.length,
      structuralCounts: {
        lundy: active?.querySelectorAll(".lundy").length || 0,
        ladder: active?.querySelectorAll(".ladder").length || 0,
        routes: active?.querySelectorAll(".routes").length || 0,
        routeSMH: active?.querySelectorAll(".route.s,.route.m,.route.h").length || 0,
        staffCard: active?.querySelectorAll(".staff-card,.ta-card").length || 0,
        drawer: document.querySelectorAll(".drawer,.media").length,
        chips: active?.querySelectorAll(".chips").length || 0,
        heroVisual: active?.querySelectorAll(".hero-visual").length || 0,
        evidenceGate: active?.querySelectorAll(".evidence-gate,.evgate").length || 0,
      },
    };
  }, index);
}

(async () => {
  fs.mkdirSync(outRoot, { recursive: true });
  const browser = await chromium.launch({
    executablePath: path.resolve(browserBinary),
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
  });
  const report = { chromiumVersion: await browser.version(), mode, targets: [] };
  try {
    for (const [slug, family, relative] of targets) {
      if (!relative) throw new Error(`missing path for ${slug}`);
      const html = path.resolve(repo, relative);
      const source = fs.readFileSync(html, "utf8");
      const dir = path.join(outRoot, slug);
      fs.mkdirSync(dir, { recursive: true });
      const row = {
        slug, family, path: path.relative(repo, html),
        sha256: crypto.createHash("sha256").update(fs.readFileSync(html)).digest("hex"),
        cssTokens: sourceTokens(source),
        errors: [], viewports: [], print: null,
      };
      for (const viewport of viewports) {
        const page = await browser.newPage({ viewport: { width: viewport.width, height: viewport.height }, deviceScaleFactor: 1 });
        page.on("console", message => { if (message.type() === "error") row.errors.push(`${viewport.name} console: ${message.text()}`); });
        page.on("pageerror", error => row.errors.push(`${viewport.name} page: ${String(error)}`));
        await page.goto(pathToFileURL(html).href, { waitUntil: "load", timeout: 30000 });
        const count = await page.locator("main.deck > section.slide").count();
        const rendered = { viewport, slides: [] };
        for (let index = 0; index < count; index += 1) {
          const topScroll = await activate(page, index, false);
          const topMetrics = await metrics(page, index);
          const top = path.join(dir, `${viewport.name}-slide-${String(index + 1).padStart(2, "0")}-top.png`);
          await page.screenshot({ path: top, fullPage: false, animations: "disabled" });
          const bottomScroll = await activate(page, index, true);
          const bottomMetrics = await metrics(page, index);
          const bottom = path.join(dir, `${viewport.name}-slide-${String(index + 1).padStart(2, "0")}-bottom.png`);
          await page.screenshot({ path: bottom, fullPage: false, animations: "disabled" });
          rendered.slides.push({
            index, top: path.relative(repo, top), bottom: path.relative(repo, bottom),
            topScroll, bottomScroll, topMetrics, bottomMetrics,
          });
        }
        row.viewports.push(rendered);
        await page.close();
      }
      const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 1 });
      page.on("console", message => { if (message.type() === "error") row.errors.push(`print console: ${message.text()}`); });
      page.on("pageerror", error => row.errors.push(`print page: ${String(error)}`));
      await page.goto(pathToFileURL(html).href, { waitUntil: "load", timeout: 30000 });
      await page.emulateMedia({ media: "print", colorScheme: "light" });
      await page.addStyleTag({ content: "@media print{html,body{color-scheme:light!important;background:#fff!important;color:#111!important}}" });
      const pdf = path.join(dir, `${slug}-a4.pdf`);
      await page.pdf({
        path: pdf, format: "A4", printBackground: true, preferCSSPageSize: false,
        margin: { top: "0mm", right: "0mm", bottom: "0mm", left: "0mm" },
      });
      row.print = { pdf: path.relative(repo, pdf), bytes: fs.statSync(pdf).size };
      await page.close();
      report.targets.push(row);
      process.stdout.write(`RENDERED ${family} ${row.sha256}\n`);
    }
  } finally {
    await browser.close();
  }
  const out = path.join(outRoot, "render_metrics.json");
  fs.writeFileSync(out, JSON.stringify(report, null, 2) + "\n");
  process.stdout.write(`${out}\n`);
})().catch(error => {
  console.error(error.stack || String(error));
  process.exitCode = 1;
});
