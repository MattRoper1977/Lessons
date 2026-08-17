#!/usr/bin/env node
'use strict';
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { JSDOM, VirtualConsole, ResourceLoader } = require('jsdom');

function serialise(value) {
  if (value instanceof Error) return `${value.name}: ${value.message}`;
  if (typeof value === 'string') return value;
  try { return JSON.stringify(value); } catch (_) { return String(value); }
}

class LocalOnlyLoader extends ResourceLoader {
  constructor(errors) { super(); this.errors = errors; }
  fetch(url, options) {
    if (/^https?:\/\//i.test(url)) {
      this.errors.push(`NETWORK_DEPENDENCY: ${url}`);
      return null;
    }
    try {
      const result = super.fetch(url, options);
      if (result && typeof result.catch === 'function') {
        return result.catch(err => {
          this.errors.push(`RESOURCE_ERROR ${url}: ${serialise(err)}`);
          return null;
        });
      }
      return result;
    } catch (err) {
      this.errors.push(`RESOURCE_ERROR ${url}: ${serialise(err)}`);
      return null;
    }
  }
}

async function loadOne(file) {
  const absolute = path.resolve(file);
  const errors = [];
  const virtualConsole = new VirtualConsole();
  virtualConsole.on('jsdomError', err => errors.push(`JSDOM_ERROR: ${serialise(err)}`));
  virtualConsole.on('error', (...args) => errors.push(`CONSOLE_ERROR: ${args.map(serialise).join(' ')}`));
  const html = fs.readFileSync(absolute, 'utf8');
  let dom;
  try {
    dom = new JSDOM(html, {
      url: pathToFileURL(absolute).href,
      runScripts: 'dangerously',
      resources: new LocalOnlyLoader(errors),
      pretendToBeVisual: true,
      virtualConsole,
      beforeParse(window) {
        window.alert = () => {};
        window.confirm = () => true;
        window.prompt = () => null;
        window.print = () => {};
        window.scrollTo = () => {};
        window.matchMedia = window.matchMedia || (() => ({
          matches: false,
          media: '',
          onchange: null,
          addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {}, dispatchEvent() { return false; }
        }));
        window.requestAnimationFrame = window.requestAnimationFrame || (cb => setTimeout(() => cb(Date.now()), 16));
        window.cancelAnimationFrame = window.cancelAnimationFrame || (id => clearTimeout(id));
        if (window.HTMLCanvasElement) {
          window.HTMLCanvasElement.prototype.getContext = function() { return null; };
        }
      }
    });
  } catch (err) {
    errors.push(`HARNESS_CONSTRUCTION: ${serialise(err)}`);
    return { file, rendered: false, readyState: null, marker: null, errors };
  }

  const window = dom.window;
  await new Promise(resolve => {
    let settled = false;
    const finish = () => { if (!settled) { settled = true; resolve(); } };
    if (window.document.readyState === 'complete') setTimeout(finish, 50);
    else window.addEventListener('load', () => setTimeout(finish, 120), { once: true });
    setTimeout(() => {
      if (!settled) errors.push('HARNESS_TIMEOUT: load did not settle within 4000ms');
      finish();
    }, 4000);
  });
  await new Promise(resolve => setTimeout(resolve, 100));
  const document = window.document;
  const rendered = Boolean(document && document.body && document.body.childNodes.length > 0);
  const marker = document && document.documentElement ? document.documentElement.getAttribute('data-ph1-control') : null;
  const readyState = document ? document.readyState : null;
  try { window.close(); } catch (_) {}
  return { file, rendered, readyState, marker, errors };
}

(async () => {
  const files = process.argv.slice(2);
  if (!files.length) {
    console.error('usage: node G2_HARNESS.cjs <html> [...]');
    process.exit(64);
  }
  const results = [];
  for (const file of files) results.push(await loadOne(file));
  process.stdout.write(JSON.stringify(results, null, 2) + '\n');
  process.exit(results.some(result => !result.rendered || result.errors.length) ? 1 : 0);
})().catch(err => {
  console.error(err && err.stack ? err.stack : String(err));
  process.exit(70);
});
