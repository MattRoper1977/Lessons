
/* Science Visual Learning Layer v1.0
   Add-only, dependency-free, no network requests, no persistent pupil data. */
(function (global) {
  'use strict';

  var document = global.document;
  if (!document || global.ScienceVisualLearning) return;

  var PAYLOADS = global.ScienceVisualPayloads || {};
  var reducedMotion = !!(global.matchMedia && global.matchMedia('(prefers-reduced-motion: reduce)').matches);

  function el(tag, attrs) {
    var node = document.createElement(tag);
    var children = Array.prototype.slice.call(arguments, 2);
    attrs = attrs || {};
    Object.keys(attrs).forEach(function (key) {
      var value = attrs[key];
      if (value === null || value === undefined || value === false) return;
      if (key === 'class') node.className = value;
      else if (key === 'text') node.textContent = value;
      else if (key === 'html') node.innerHTML = value;
      else if (key === 'dataset') Object.keys(value).forEach(function (d) { node.dataset[d] = value[d]; });
      else if (key === 'style' && typeof value === 'object') Object.keys(value).forEach(function (prop) { if (prop.indexOf('--') === 0) node.style.setProperty(prop, String(value[prop])); else node.style[prop] = value[prop]; });
      else if (key.slice(0, 2) === 'on' && typeof value === 'function') node.addEventListener(key.slice(2), value);
      else if (key in node && key !== 'list') {
        try { node[key] = value; } catch (err) { node.setAttribute(key, String(value)); }
      } else node.setAttribute(key, String(value));
    });
    children.flat(Infinity).forEach(function (child) {
      if (child === null || child === undefined || child === false) return;
      node.appendChild(typeof child === 'string' || typeof child === 'number' ? document.createTextNode(String(child)) : child);
    });
    return node;
  }

  function svgMarkup(markup, label) {
    var wrap = el('div', { class: 'svl-svg-wrap', html: markup });
    var svg = wrap.querySelector('svg');
    if (svg) {
      svg.setAttribute('role', 'img');
      svg.setAttribute('aria-label', label || 'Interactive science diagram');
      svg.setAttribute('focusable', 'false');
    }
    return wrap.firstElementChild;
  }

  function normaliseSlug(value) {
    return String(value || '').replace(/\.html?$/i, '').replace(/[^A-Za-z0-9_\-]/g, '');
  }

  function currentSlug() {
    var explicit = document.documentElement.getAttribute('data-svl-lesson') || document.body && document.body.getAttribute('data-svl-lesson');
    if (explicit) return normaliseSlug(explicit);
    var bits = String(global.location && global.location.pathname || '').split('/').filter(Boolean);
    return normaliseSlug(bits[bits.length - 1] || '');
  }

  function findTarget(payload) {
    if (payload.targetSelector) {
      try {
        var selected = document.querySelector(payload.targetSelector);
        if (selected) return selected;
      } catch (err) { /* invalid selector never stops the lesson */ }
    }
    var title = payload.targetTitle || 'We Do 1';
    var exact = document.querySelector('.slide[data-title="' + cssEscape(title) + '"]');
    if (exact) return exact;
    var slides = Array.prototype.slice.call(document.querySelectorAll('.slide[data-title]'));
    var near = slides.find(function (slide) { return String(slide.getAttribute('data-title')).toLowerCase().indexOf('we do') !== -1; });
    return near || document.querySelector('.slide.active') || document.body;
  }

  function cssEscape(value) {
    if (global.CSS && global.CSS.escape) return global.CSS.escape(value);
    return String(value).replace(/["\\]/g, '\\$&');
  }

  function shuffle(items, seedText) {
    var list = items.slice();
    var seed = 0;
    String(seedText || 'science').split('').forEach(function (c) { seed = (seed * 31 + c.charCodeAt(0)) >>> 0; });
    function random() {
      seed = (1664525 * seed + 1013904223) >>> 0;
      return seed / 4294967296;
    }
    for (var i = list.length - 1; i > 0; i -= 1) {
      var j = Math.floor(random() * (i + 1));
      var temp = list[i]; list[i] = list[j]; list[j] = temp;
    }
    if (list.every(function (item, index) { return item.id === items[index].id; }) && list.length > 1) list.push(list.shift());
    return list;
  }

  function announce(ctx, message, tone) {
    ctx.live.textContent = message;
    ctx.live.dataset.tone = tone || '';
  }

  function predictionGate(ctx) {
    var options = ctx.activity.predictionOptions || [];
    if (!options.length) return null;
    var gate = el('div', { class: 'svl-gate' },
      el('h4', { text: ctx.pathway === 'BUILD' ? 'Say it before the model moves' : 'Commit a prediction before running the model' }),
      el('div', { class: 'svl-predict-options', role: 'group', 'aria-label': 'Prediction choices' })
    );
    var group = gate.querySelector('.svl-predict-options');
    options.forEach(function (option) {
      var button = el('button', {
        type: 'button', class: 'svl-predict-option', text: option, 'aria-pressed': 'false',
        onclick: function () {
          ctx.prediction = option;
          Array.prototype.forEach.call(group.querySelectorAll('button'), function (b) { b.setAttribute('aria-pressed', String(b === button)); });
          announce(ctx, 'Prediction committed: ' + option + '. Now run or reveal the model.', 'notice');
        }
      });
      group.appendChild(button);
    });
    ctx.predictionGroup = group;
    return gate;
  }

  function evidenceGate(ctx) {
    var prompt = ctx.activity.evidencePrompt;
    if (!prompt || ctx.pathway !== 'LAUNCH') return null;
    var gate = el('div', { class: 'svl-gate' },
      el('h4', { text: 'Evidence before explanation' }),
      el('label', { class: 'svl-label', for: ctx.slug + '-evidence', text: prompt }),
      el('textarea', {
        id: ctx.slug + '-evidence', class: 'svl-evidence-input', disabled: true,
        placeholder: 'Complete the activity first. Then record the evidence or pattern you noticed.',
        'aria-describedby': ctx.slug + '-evidence-help'
      }),
      el('p', { id: ctx.slug + '-evidence-help', class: 'svl-small', text: 'This note stays in this page only. Nothing is saved or sent.' })
    );
    ctx.evidenceInput = gate.querySelector('textarea');
    ctx.evidenceInput.addEventListener('input', function () { refreshExplanation(ctx); });
    return gate;
  }

  function refreshExplanation(ctx) {
    if (!ctx.completed) return;
    var evidenceReady = !ctx.evidenceInput || ctx.evidenceInput.value.trim().length >= 8;
    if (ctx.pathway === 'LAUNCH' && !evidenceReady) {
      ctx.explanation.hidden = true;
      announce(ctx, 'Activity complete. Record a specific observation, value or pattern to unlock the explanation.', 'notice');
      return;
    }
    ctx.explanation.hidden = false;
    if (!ctx.explanation.dataset.opened) {
      ctx.explanation.dataset.opened = '1';
      ctx.explanation.dataset.sciOpenedBy = ctx.pathway === 'LAUNCH' ? 'completed activity and recorded evidence' : 'completed teaching interaction';
      ctx.explanation.classList.add('svl-reveal');
      announce(ctx, 'Explanation unlocked. Read it against the evidence you produced.', 'good');
    }
  }

  function complete(ctx, message) {
    ctx.completed = true;
    if (ctx.evidenceInput) {
      ctx.evidenceInput.disabled = false;
      ctx.evidenceInput.placeholder = 'Record the evidence or pattern you noticed.';
    }
    announce(ctx, message || 'Activity complete.', 'good');
    refreshExplanation(ctx);
  }

  function canRun(ctx) {
    if (ctx.pathway === 'BUILD') return true;
    if (!(ctx.activity.predictionOptions || []).length) return true;
    if (ctx.prediction) return true;
    announce(ctx, 'Commit a prediction first. The prediction is not scored; it gives the class something to test.', 'notice');
    return false;
  }

  function clearPrediction(ctx) {
    ctx.prediction = '';
    if (ctx.predictionGroup) Array.prototype.forEach.call(ctx.predictionGroup.querySelectorAll('button'), function (b) { b.setAttribute('aria-pressed', 'false'); });
  }

  function explanationNode(ctx) {
    var node = el('div', { class: 'svl-explanation', hidden: true, text: ctx.activity.completion || 'Use the evidence to explain the pattern.' });
    ctx.explanation = node;
    return node;
  }

  function renderSort(ctx, host) {
    var activity = ctx.activity;
    var selected = null;
    var placed = {};
    var items = shuffle(activity.items || [], ctx.slug + '-sort');
    var layout = el('div', { class: 'svl-sort-layout' });
    var bank = el('div', { class: 'svl-bank' },
      el('h4', { class: 'svl-bank-title', text: 'Cards · click a card, then a destination; dragging is optional' }),
      el('div', { class: 'svl-card-list', role: 'list', 'aria-label': 'Cards to place' })
    );
    var bankList = bank.querySelector('.svl-card-list');
    var zones = el('div', { class: 'svl-zones' },
      el('h4', { class: 'svl-bank-title', text: 'Destinations' }),
      el('div', { class: 'svl-zone-grid' })
    );
    var zoneGrid = zones.querySelector('.svl-zone-grid');
    var cardById = {};

    function selectCard(id, button) {
      if (placed[id]) {
        var item = activity.items.find(function (x) { return x.id === id; });
        if (item) announce(ctx, item.reason || item.label, 'good');
        return;
      }
      selected = id;
      Object.keys(cardById).forEach(function (key) { cardById[key].setAttribute('aria-pressed', String(key === id)); });
      announce(ctx, 'Selected ' + button.dataset.label + '. Now choose a destination.', 'notice');
    }

    function place(id, categoryId) {
      var item = activity.items.find(function (x) { return x.id === id; });
      var zone = zoneGrid.querySelector('[data-category="' + cssEscape(categoryId) + '"]');
      if (!item || !zone || placed[id]) return;
      var card = cardById[id];
      if (item.answer !== categoryId) {
        card.classList.remove('is-wrong'); void card.offsetWidth; card.classList.add('is-wrong');
        announce(ctx, ctx.pathway === 'BUILD' ? 'Not there yet. Use the visible deciding feature, not size or appearance.' : 'That placement does not fit all the evidence. Recheck the defining feature.', 'bad');
        return;
      }
      card.classList.remove('is-wrong');
      card.classList.add('is-correct');
      card.setAttribute('aria-pressed', 'false');
      zone.querySelector('.svl-card-list').appendChild(card);
      placed[id] = categoryId;
      selected = null;
      announce(ctx, item.label + ': correct. ' + (item.reason || ''), 'good');
      if (Object.keys(placed).length === activity.items.length) complete(ctx, 'All cards are placed using the scientific rule.');
    }

    items.forEach(function (item) {
      var button = el('button', {
        type: 'button', class: 'svl-card', draggable: true, role: 'listitem', 'aria-pressed': 'false',
        dataset: { id: item.id, label: item.label },
        onclick: function () { selectCard(item.id, button); }
      },
      el('span', { class: 'svl-card-icon', 'aria-hidden': 'true', text: item.icon || '•' }),
      el('span', { text: item.label })
      );
      button.addEventListener('dragstart', function (event) {
        selected = item.id;
        event.dataTransfer.effectAllowed = 'move';
        event.dataTransfer.setData('text/plain', item.id);
      });
      cardById[item.id] = button;
      bankList.appendChild(button);
    });

    (activity.categories || []).forEach(function (category) {
      var zone = el('section', { class: 'svl-zone', dataset: { category: category.id } },
        el('button', {
          type: 'button', class: 'svl-zone-head svl-ghost',
          'aria-label': 'Place selected card in ' + category.label,
          onclick: function () {
            if (!selected) { announce(ctx, 'Select a card first, then choose this destination.', 'notice'); return; }
            place(selected, category.id);
          }
        }, el('span', { class: 'svl-zone-icon', 'aria-hidden': 'true', text: category.icon || '•' }), el('span', { text: category.label })),
        el('div', { class: 'svl-card-list', role: 'list', 'aria-label': category.label + ' cards' })
      );
      zone.addEventListener('dragover', function (event) { event.preventDefault(); zone.classList.add('is-target'); });
      zone.addEventListener('dragleave', function () { zone.classList.remove('is-target'); });
      zone.addEventListener('drop', function (event) {
        event.preventDefault(); zone.classList.remove('is-target');
        place(event.dataTransfer.getData('text/plain') || selected, category.id);
      });
      zoneGrid.appendChild(zone);
    });

    layout.append(bank, zones);
    host.appendChild(layout);
  }

  function renderSequence(ctx, host) {
    var activity = ctx.activity;
    var original = activity.items || [];
    var order = shuffle(original, ctx.slug + '-sequence');
    var list = el('ol', { class: 'svl-sequence', 'aria-label': 'Sequence to arrange' });
    var draggedId = '';

    function redraw() {
      list.replaceChildren();
      order.forEach(function (item, index) {
        var row = el('li', { class: 'svl-sequence-item', draggable: true, dataset: { id: item.id } },
          el('span', { class: 'svl-sequence-text', text: item.label }),
          el('span', { class: 'svl-sequence-controls' },
            el('button', {
              type: 'button', class: 'svl-small-btn svl-ghost', 'aria-label': 'Move ' + item.label + ' up', text: '↑', disabled: index === 0,
              onclick: function () { if (index > 0) { var x = order[index - 1]; order[index - 1] = order[index]; order[index] = x; redraw(); } }
            }),
            el('button', {
              type: 'button', class: 'svl-small-btn svl-ghost', 'aria-label': 'Move ' + item.label + ' down', text: '↓', disabled: index === order.length - 1,
              onclick: function () { if (index < order.length - 1) { var x = order[index + 1]; order[index + 1] = order[index]; order[index] = x; redraw(); } }
            })
          )
        );
        row.addEventListener('dragstart', function (event) { draggedId = item.id; event.dataTransfer.setData('text/plain', item.id); });
        row.addEventListener('dragover', function (event) { event.preventDefault(); });
        row.addEventListener('drop', function (event) {
          event.preventDefault();
          var id = event.dataTransfer.getData('text/plain') || draggedId;
          var from = order.findIndex(function (x) { return x.id === id; });
          var to = order.findIndex(function (x) { return x.id === item.id; });
          if (from >= 0 && to >= 0 && from !== to) { var moving = order.splice(from, 1)[0]; order.splice(to, 0, moving); redraw(); }
        });
        list.appendChild(row);
      });
    }

    var check = el('button', {
      type: 'button', text: 'Check sequence',
      onclick: function () {
        var correct = order.every(function (item, index) { return item.id === original[index].id; });
        Array.prototype.forEach.call(list.children, function (row, index) { row.classList.toggle('is-correct', row.dataset.id === original[index].id); });
        if (correct) {
          complete(ctx, 'The sequence is correct. Explain why one step must come before the next.');
          check.disabled = true;
        } else {
          var count = order.filter(function (item, index) { return item.id === original[index].id; }).length;
          announce(ctx, count + ' of ' + order.length + ' positions are correct. Use the scientific reason for each step, not just memory.', 'notice');
        }
      }
    });
    redraw();
    host.append(list, el('div', { class: 'svl-arrow-rail', 'aria-hidden': 'true', text: '↓  ↓  ↓' }), el('div', { class: 'svl-actions' }, check));
  }

  function renderEvidence(ctx, host) {
    var activity = ctx.activity;
    var selected = {};
    var grid = el('div', { class: 'svl-evidence-grid', role: 'group', 'aria-label': 'Evidence statements' });
    var buttons = {};
    shuffle(activity.statements || [], ctx.slug + '-evidence').forEach(function (statement) {
      var button = el('button', {
        type: 'button', class: 'svl-evidence-card', text: statement.label, 'aria-pressed': 'false',
        onclick: function () {
          selected[statement.id] = !selected[statement.id];
          button.setAttribute('aria-pressed', String(!!selected[statement.id]));
          button.classList.remove('is-correct', 'is-wrong');
        }
      });
      buttons[statement.id] = button;
      grid.appendChild(button);
    });
    var reasons = el('ul', { class: 'svl-reason-list', hidden: true });
    var check = el('button', {
      type: 'button', text: 'Check selected evidence',
      onclick: function () {
        var statements = activity.statements || [];
        var allCorrect = statements.every(function (s) { return !!selected[s.id] === !!s.correct; });
        statements.forEach(function (s) {
          var button = buttons[s.id];
          button.classList.remove('is-correct', 'is-wrong');
          if (selected[s.id]) button.classList.add(s.correct ? 'is-correct' : 'is-wrong');
        });
        if (!allCorrect) {
          announce(ctx, 'Some selected lines do not answer the question, or a mark-bearing line is still missing. Test each line for relevance and causality.', 'bad');
          return;
        }
        reasons.replaceChildren();
        statements.filter(function (s) { return s.correct; }).forEach(function (s) { reasons.appendChild(el('li', { text: s.label + ' — ' + s.reason })); });
        reasons.hidden = false;
        check.disabled = true;
        complete(ctx, 'You selected the complete evidence set and rejected the distractors.');
      }
    });
    host.append(grid, el('div', { class: 'svl-actions', style: { marginTop: '10px' } }, check), reasons);
  }

  function renderCalculation(ctx, host) {
    var activity = ctx.activity;
    var formula = el('div', { class: 'svl-formula', text: 'magnification = image size ÷ actual size · units must match' });
    var conversion = el('input', { type: 'number', inputMode: 'decimal', placeholder: 'e.g. 30000', 'aria-label': 'Image size converted to micrometres' });
    var answer = el('input', { type: 'number', inputMode: 'decimal', placeholder: 'magnification', 'aria-label': 'Calculated magnification' });
    var grid = el('div', { class: 'svl-calc-grid' },
      el('div', { class: 'svl-calc-step' }, el('span', { class: 'svl-label', text: '1 · Convert ' + activity.imageSize + ' ' + activity.imageUnit + ' to ' + activity.actualUnit }), conversion),
      el('div', { class: 'svl-calc-step' }, el('span', { class: 'svl-label', text: '2 · Divide converted image size by ' + activity.actualSize + ' ' + activity.actualUnit }), el('div', { class: 'svl-small', text: 'Show the substitution before using a calculator.' })),
      el('div', { class: 'svl-calc-step' }, el('span', { class: 'svl-label', text: '3 · Magnification' }), answer)
    );
    var check = el('button', {
      type: 'button', text: 'Check working',
      onclick: function () {
        var expectedConversion = activity.imageUnit === 'mm' && activity.actualUnit === 'µm' ? activity.imageSize * 1000 : activity.imageSize;
        var conversionOK = Math.abs(Number(conversion.value) - expectedConversion) < 0.0001;
        var answerOK = Math.abs(Number(answer.value) - Number(activity.answer)) < 0.0001;
        if (conversionOK && answerOK) {
          conversion.setAttribute('aria-invalid', 'false'); answer.setAttribute('aria-invalid', 'false');
          check.disabled = true;
          complete(ctx, 'Correct conversion and magnification. The working is visible and units match.');
        } else {
          conversion.setAttribute('aria-invalid', String(!conversionOK)); answer.setAttribute('aria-invalid', String(!answerOK));
          announce(ctx, !conversionOK ? 'Fix the unit conversion first: 1 mm = 1000 µm.' : 'The conversion is correct. Recheck the division.', 'bad');
        }
      }
    });
    host.append(formula, grid, el('div', { class: 'svl-actions', style: { marginTop: '10px' } }, check));
  }

  function sceneAlveolus() {
    return '<svg viewBox="0 0 640 360" xmlns="http://www.w3.org/2000/svg">' +
      '<title>Bare model of an alveolus and surrounding capillary</title><desc>A cluster of air sacs with a thin wall, air pathway and capillary network. Numbered hotspots identify adaptations after the pupil selects them.</desc>' +
      '<rect width="640" height="360" fill="#f8fafc"/>' +
      '<path d="M83 63 C146 52 173 86 181 126 C225 78 288 89 304 137 C343 102 408 119 414 169 C459 145 520 177 506 231 C488 294 404 305 357 276 C326 326 246 327 213 281 C168 318 97 292 91 239 C46 215 37 147 83 120Z" fill="#fff7ed" stroke="#334155" stroke-width="5"/>' +
      '<path d="M95 113 C125 130 147 145 173 164" fill="none" stroke="#4d82a0" stroke-width="24" stroke-linecap="round"/><path d="M95 113 C125 130 147 145 173 164" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round"/>' +
      '<path d="M84 251 C144 311 224 318 287 291 C348 265 407 305 472 273 C522 249 547 205 520 161" fill="none" stroke="#9c2f45" stroke-width="25" stroke-linecap="round"/>' +
      '<path d="M84 251 C144 311 224 318 287 291 C348 265 407 305 472 273 C522 249 547 205 520 161" fill="none" stroke="#f9a8b6" stroke-width="12" stroke-linecap="round"/>' +
      '<g fill="#b42318"><circle cx="137" cy="282" r="9"/><circle cx="219" cy="298" r="9"/><circle cx="319" cy="286" r="9"/><circle cx="415" cy="288" r="9"/><circle cx="500" cy="238" r="9"/></g>' +
      '<g fill="#4d82a0" stroke="#1e3a8a" stroke-width="2"><circle cx="158" cy="167" r="5"/><circle cx="177" cy="174" r="5"/><circle cx="194" cy="181" r="5"/></g>' +
      '<g fill="#9c2f45" stroke="#7f1d1d" stroke-width="2"><circle cx="221" cy="207" r="5"/><circle cx="244" cy="219" r="5"/><circle cx="268" cy="229" r="5"/></g>' +
      '<path d="M188 184 C207 198 221 207 242 216" stroke="#4d82a0" stroke-width="4"/><path d="M274 230 C249 213 232 204 211 194" stroke="#9c2f45" stroke-width="4"/>' +
      '<text x="22" y="28" font-family="Segoe UI,Arial" font-size="16" fill="#334155" font-weight="700">MODEL · labels withheld until observed</text>' +
      '</svg>';
  }

  function sceneRootGut() {
    return '<svg viewBox="0 0 720 380" xmlns="http://www.w3.org/2000/svg">' +
      '<title>Comparison model of a root hair cell and an intestinal villus</title><desc>Two exchange surfaces drawn at matched scale with hidden numbered hotspots for surface area, thin barriers, mitochondria and blood supply.</desc>' +
      '<rect width="720" height="380" fill="#f8fafc"/><line x1="360" y1="36" x2="360" y2="350" stroke="#94a3b8" stroke-width="3" stroke-dasharray="8 8"/>' +
      '<text x="120" y="32" font-family="Segoe UI,Arial" font-size="18" font-weight="800" fill="#334155">ROOT HAIR CELL</text><text x="505" y="32" font-family="Segoe UI,Arial" font-size="18" font-weight="800" fill="#334155">VILLUS</text>' +
      '<path d="M88 130 Q145 74 232 111 Q287 135 286 205 Q285 277 206 292 Q140 302 99 259 Q59 215 88 130Z" fill="#e7f5e9" stroke="#3f7d6e" stroke-width="5"/>' +
      '<path d="M93 184 C51 179 28 186 17 205 C45 211 66 215 98 211" fill="#e7f5e9" stroke="#3f7d6e" stroke-width="5"/>' +
      '<ellipse cx="182" cy="199" rx="55" ry="72" fill="#dbeafe" stroke="#4d82a0" stroke-width="3"/><circle cx="237" cy="180" r="18" fill="#d8a63b" stroke="#7c5a10" stroke-width="3"/>' +
      '<g fill="#c9803b" stroke="#7c3f13" stroke-width="2"><ellipse cx="125" cy="153" rx="11" ry="6"/><ellipse cx="138" cy="239" rx="11" ry="6"/><ellipse cx="244" cy="234" rx="11" ry="6"/></g>' +
      '<path d="M438 301 C428 218 436 105 513 73 C593 102 605 221 589 301Z" fill="#fff1f2" stroke="#9c2f45" stroke-width="5"/>' +
      '<path d="M487 286 C470 232 474 150 513 106 C557 148 557 235 536 286" fill="none" stroke="#b42318" stroke-width="16" stroke-linecap="round"/>' +
      '<path d="M472 120 Q513 87 554 120" fill="none" stroke="#9c2f45" stroke-width="5"/>' +
      '<g stroke="#9c2f45" stroke-width="3"><path d="M460 112 l-18 -15"/><path d="M473 100 l-10 -22"/><path d="M489 91 l-4 -23"/><path d="M535 91 l4 -23"/><path d="M552 101 l12 -22"/><path d="M566 114 l18 -15"/></g>' +
      '<text x="26" y="352" font-family="Segoe UI,Arial" font-size="14" fill="#475569">MODEL · shared geometry makes comparison visible</text>' +
      '</svg>';
  }

  function renderHotspot(ctx, host) {
    var activity = ctx.activity;
    var markup = activity.scene === 'rootgut' ? sceneRootGut() : sceneAlveolus();
    var stage = el('div', { class: 'svl-hotspot-stage' });
    stage.appendChild(svgMarkup(markup, activity.scene === 'rootgut' ? 'Root hair cell and intestinal villus comparison model' : 'Alveolus and capillary model'));
    var list = el('div', { class: 'svl-hotspot-list' });
    var opened = {};
    (activity.hotspots || []).forEach(function (spot, index) {
      var note = el('div', { class: 'svl-hotspot-note', hidden: true }, el('strong', { text: (index + 1) + ' · ' + spot.label }), el('div', { text: spot.note }));
      var button = el('button', {
        type: 'button', class: 'svl-hotspot', text: String(index + 1),
        style: { '--x': spot.x, '--y': spot.y }, 'aria-label': 'Open hotspot ' + (index + 1) + ': ' + spot.label,
        onclick: function () {
          opened[spot.id] = true; button.classList.add('is-open'); note.hidden = false;
          announce(ctx, spot.label + ': ' + spot.note, 'good');
          if (Object.keys(opened).length === activity.hotspots.length) complete(ctx, 'Every visual feature has been observed. Now state how one feature changes diffusion or absorption.');
        }
      });
      stage.appendChild(button); list.appendChild(note);
    });
    host.appendChild(el('div', { class: 'svl-hotspot-wrap' }, stage, list));
  }

  function controlSelect(label, options, value) {
    var select = el('select', { 'aria-label': label });
    options.forEach(function (option) {
      var val = typeof option === 'string' ? option : option.value;
      var text = typeof option === 'string' ? option : option.label;
      select.appendChild(el('option', { value: val, text: text, selected: val === value }));
    });
    return el('div', { class: 'svl-control' }, el('label', { class: 'svl-label', text: label }), select);
  }

  function armSVG() {
    return '<svg viewBox="0 0 620 310" xmlns="http://www.w3.org/2000/svg">' +
      '<title>Cardboard arm model with antagonistic muscle pair</title><desc>An upper arm and forearm hinged at the elbow. Biceps and triceps bands change length when the arm bends and straightens.</desc>' +
      '<rect width="620" height="310" fill="#f8fafc"/><circle cx="120" cy="150" r="38" fill="#e2e8f0" stroke="#334155" stroke-width="5"/>' +
      '<path d="M150 150 L315 170" stroke="#cbd5e1" stroke-width="34" stroke-linecap="round"/><circle cx="315" cy="170" r="17" fill="#fff" stroke="#334155" stroke-width="5"/>' +
      '<g class="svl-forearm" style="transform-origin:315px 170px;transition:transform .75s cubic-bezier(.4,0,.2,1)"><path d="M325 170 L515 170" stroke="#cbd5e1" stroke-width="30" stroke-linecap="round"/><circle cx="535" cy="170" r="28" fill="#e2e8f0" stroke="#334155" stroke-width="5"/></g>' +
      '<path class="svl-biceps" d="M165 124 Q235 76 302 142" fill="none" stroke="#9c2f45" stroke-width="20" stroke-linecap="round" style="transition:d .7s ease,stroke-width .7s ease"/>' +
      '<path class="svl-triceps" d="M165 178 Q235 224 304 194" fill="none" stroke="#4d82a0" stroke-width="13" stroke-linecap="round" style="transition:d .7s ease,stroke-width .7s ease"/>' +
      '<text x="185" y="58" font-family="Segoe UI,Arial" font-size="17" font-weight="800" fill="#7f1d1d">BICEPS BAND</text><text x="185" y="262" font-family="Segoe UI,Arial" font-size="17" font-weight="800" fill="#1e3a8a">TRICEPS BAND</text>' +
      '<text x="22" y="292" font-family="Segoe UI,Arial" font-size="14" fill="#475569">MODEL, not a pupil body · muscle bands can pull, never push</text></svg>';
  }

  function renderMuscles(ctx, host) {
    var stage = el('div', { class: 'svl-stage' }); stage.appendChild(svgMarkup(armSVG(), 'Cardboard arm model showing biceps and triceps bands'));
    var status = el('div', { class: 'svl-readout' },
      el('div', {}, el('span', { class: 'svl-small', text: 'Biceps' }), el('strong', { class: 'biceps-state', text: 'waiting' })),
      el('div', {}, el('span', { class: 'svl-small', text: 'Triceps' }), el('strong', { class: 'triceps-state', text: 'waiting' }))
    );
    var visited = {};
    function move(state) {
      if (!canRun(ctx)) return;
      var svg = stage.querySelector('svg');
      var forearm = svg.querySelector('.svl-forearm');
      var biceps = svg.querySelector('.svl-biceps');
      var triceps = svg.querySelector('.svl-triceps');
      if (state === 'bend') {
        forearm.style.transform = 'rotate(-64deg)';
        biceps.setAttribute('d', 'M165 124 Q232 101 302 142'); biceps.setAttribute('stroke-width', '25');
        triceps.setAttribute('d', 'M165 178 Q233 235 304 194'); triceps.setAttribute('stroke-width', '11');
        status.querySelector('.biceps-state').textContent = 'CONTRACTS · pulls';
        status.querySelector('.triceps-state').textContent = 'RELAXES';
        announce(ctx, (ctx.prediction === 'Biceps pulls' || !ctx.prediction ? 'The prediction fits. ' : 'Revise the prediction. ') + 'The biceps shortens and pulls; the triceps relaxes.', ctx.prediction === 'Triceps pulls' ? 'notice' : 'good');
      } else {
        forearm.style.transform = 'rotate(0deg)';
        biceps.setAttribute('d', 'M165 124 Q235 76 302 142'); biceps.setAttribute('stroke-width', '13');
        triceps.setAttribute('d', 'M165 178 Q235 207 304 194'); triceps.setAttribute('stroke-width', '23');
        status.querySelector('.biceps-state').textContent = 'RELAXES';
        status.querySelector('.triceps-state').textContent = 'CONTRACTS · pulls';
        announce(ctx, (ctx.prediction === 'Triceps pulls' || !ctx.prediction ? 'The prediction fits. ' : 'Revise the prediction. ') + 'The triceps shortens and pulls; the biceps relaxes.', ctx.prediction === 'Biceps pulls' ? 'notice' : 'good');
      }
      visited[state] = true;
      if (Object.keys(visited).length === 2) complete(ctx, 'Both states are visible: the pair swaps jobs and neither muscle pushes.');
    }
    var controls = el('div', { class: 'svl-controls' },
      el('div', { class: 'svl-control' }, el('span', { class: 'svl-label', text: 'Choose the movement' }),
        el('div', { class: 'svl-actions' },
          el('button', { type: 'button', text: 'Bend arm', onclick: function () { move('bend'); } }),
          el('button', { type: 'button', class: 'svl-ghost', text: 'Straighten arm', onclick: function () { move('straight'); } })
        )), status
    );
    host.appendChild(el('div', { class: 'svl-model-grid' }, stage, controls));
  }

  function frictionSVG(surface) {
    var texture = surface === 'Carpet' ? '<path d="M85 235 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17 l8 -17 l8 17" fill="none" stroke="#475569" stroke-width="4"/>' :
      surface === 'Wood' ? '<path d="M75 235 C145 218 195 249 267 230 S390 242 535 227" fill="none" stroke="#8b5e34" stroke-width="6"/><path d="M75 246 C145 229 195 260 267 241 S390 253 535 238" fill="none" stroke="#c9803b" stroke-width="3"/>' :
      '<line x1="70" y1="235" x2="548" y2="235" stroke="#64748b" stroke-width="5"/>';
    return '<svg viewBox="0 0 620 310" xmlns="http://www.w3.org/2000/svg"><title>Comparative friction ramp model</title><desc>The same block leaves the same ramp and travels across a selected surface. A magnified strip shows the surface texture.</desc>' +
      '<rect width="620" height="310" fill="#f8fafc"/><path d="M65 68 L235 215 L65 215Z" fill="#dbeafe" stroke="#334155" stroke-width="5"/>' +
      '<line x1="70" y1="235" x2="555" y2="235" stroke="#334155" stroke-width="7"/>' + texture +
      '<g class="svl-block" style="transform-origin:center"><rect x="174" y="178" width="58" height="42" rx="6" fill="#d8a63b" stroke="#334155" stroke-width="4"/><text x="203" y="204" text-anchor="middle" font-family="Segoe UI,Arial" font-weight="800" font-size="14">same block</text></g>' +
      '<text x="72" y="276" font-family="Segoe UI,Arial" font-size="17" font-weight="800" fill="#334155">Surface: ' + surface + '</text><text x="365" y="286" font-family="Segoe UI,Arial" font-size="13" fill="#475569">relative comparison · not measured data</text></svg>';
  }

  function renderFriction(ctx, host) {
    var surfaces = { 'Smooth card': { distance: 82, travel: 320 }, 'Wood': { distance: 58, travel: 225 }, 'Carpet': { distance: 32, travel: 118 } };
    var surfaceControl = controlSelect('Surface under the block', Object.keys(surfaces), 'Smooth card');
    var select = surfaceControl.querySelector('select');
    var stage = el('div', { class: 'svl-stage' });
    var records = {};
    var tbody = el('tbody');
    var table = el('table', { class: 'svl-data-table' }, el('thead', {}, el('tr', {}, el('th', { text: 'Surface' }), el('th', { text: 'Relative travel' }), el('th', { text: 'Observation' }))), tbody);
    function draw() { stage.replaceChildren(svgMarkup(frictionSVG(select.value), 'Friction model using ' + select.value)); }
    select.addEventListener('change', function () { draw(); announce(ctx, 'Surface changed. The block and ramp remain the same.', 'notice'); });
    draw();
    var run = el('button', {
      type: 'button', text: 'Run one finite trial',
      onclick: function () {
        if (!canRun(ctx)) return;
        var name = select.value; var data = surfaces[name];
        draw();
        var block = stage.querySelector('.svl-block');
        block.style.setProperty('--svl-travel', data.travel + 'px');
        block.style.setProperty('--svl-duration', name === 'Carpet' ? '.75s' : name === 'Wood' ? '1s' : '1.25s');
        if (!ctx.isStatic()) block.classList.add('is-running'); else block.style.transform = 'translateX(' + data.travel + 'px)';
        run.disabled = true;
        global.setTimeout(function () {
          records[name] = data.distance;
          tbody.replaceChildren();
          Object.keys(records).forEach(function (key) {
            tbody.appendChild(el('tr', {}, el('td', { text: key }), el('td', { text: records[key] + ' relative units' }), el('td', { text: key === 'Carpet' ? 'stopped soonest' : key === 'Smooth card' ? 'travelled furthest' : 'between the two' })));
          });
          announce(ctx, name + ' recorded: ' + data.distance + ' relative travel units. Freeze the frame and compare it with another surface.', 'good');
          run.disabled = false;
          if (Object.keys(records).length === 3) { var supported = ctx.prediction === 'Carpet'; complete(ctx, (supported ? 'Prediction supported. ' : 'Prediction revised: carpet stopped the block soonest. ') + 'All three surfaces were compared with the block and ramp controlled.'); }
        }, ctx.isStatic() ? 20 : 1320);
      }
    });
    var controls = el('div', { class: 'svl-controls' }, surfaceControl, run, table, el('p', { class: 'svl-caveat', text: 'Teaching model only: the relative values illustrate a pattern. Use practical measurements as evidence about real materials.' }));
    host.appendChild(el('div', { class: 'svl-model-grid' }, stage, controls));
  }

  function mechanismSVG(kind, active) {
    var content = '';
    if (kind === 'Lever') {
      content = '<polygon points="110,224 510,160 520,185 120,249" fill="#dbeafe" stroke="#334155" stroke-width="5"/><polygon points="305,246 345,246 325,194" fill="#d8a63b" stroke="#334155" stroke-width="4"/><rect x="430" y="118" width="74" height="55" rx="6" fill="#c9803b" stroke="#334155" stroke-width="4"/><path d="M150 132 V205" stroke="#3f7d6e" stroke-width="8"/><path d="M138 187 l12 18 l12 -18" fill="#3f7d6e"/><text x="83" y="112" font-family="Segoe UI,Arial" font-size="17" font-weight="800">INPUT moves further</text><text x="410" y="92" font-family="Segoe UI,Arial" font-size="17" font-weight="800">LOAD lifts</text>';
    } else if (kind === 'Pulley') {
      content = '<circle cx="315" cy="108" r="52" fill="#e2e8f0" stroke="#334155" stroke-width="6"/><circle cx="315" cy="108" r="11" fill="#334155"/><path d="M263 108 V260 M367 108 V220" stroke="#3f7d6e" stroke-width="8"/><rect x="228" y="254" width="70" height="42" fill="#c9803b" stroke="#334155" stroke-width="4"/><path d="M367 220 v60" stroke="#3f7d6e" stroke-width="8"/><path d="M355 262 l12 18 l12 -18" fill="#3f7d6e"/><text x="385" y="250" font-family="Segoe UI,Arial" font-size="17" font-weight="800">pull down</text><text x="165" y="320" font-family="Segoe UI,Arial" font-size="17" font-weight="800">direction changes; useful arrangement can reduce force</text>';
    } else {
      content = '<circle cx="242" cy="180" r="82" fill="#dbeafe" stroke="#334155" stroke-width="8"/><circle cx="407" cy="180" r="45" fill="#fef3c7" stroke="#334155" stroke-width="8"/><circle cx="242" cy="180" r="14" fill="#334155"/><circle cx="407" cy="180" r="12" fill="#334155"/><path d="M242 70 v35 M242 255 v35 M132 180 h35 M317 180 h35 M164 102 l25 25 M295 233 l25 25 M164 258 l25 -25 M295 127 l25 -25" stroke="#334155" stroke-width="10"/><path d="M407 119 v20 M407 221 v20 M346 180 h20 M448 180 h20" stroke="#334155" stroke-width="9"/><path d="M225 78 C180 95 151 126 143 166" fill="none" stroke="#3f7d6e" stroke-width="7"/><path d="M143 145 l0 22 l21 -8" fill="#3f7d6e"/><text x="66" y="52" font-family="Segoe UI,Arial" font-size="17" font-weight="800">large gear: slower turn</text><text x="372" y="96" font-family="Segoe UI,Arial" font-size="17" font-weight="800">small gear: faster turn</text>';
    }
    return '<svg viewBox="0 0 620 350" xmlns="http://www.w3.org/2000/svg"><title>' + kind + ' trade-off model</title><desc>A simplified mechanism diagram showing input, output and the associated force, distance, direction or speed trade-off.</desc><rect width="620" height="350" fill="#f8fafc"/>' + content + '<text x="20" y="333" font-family="Segoe UI,Arial" font-size="13" fill="#475569">' + (active ? 'model run complete · compare input with output' : 'predict the trade-off before revealing') + '</text></svg>';
  }

  function renderMechanisms(ctx, host) {
    var kinds = ['Lever', 'Pulley', 'Gears'];
    var current = 'Lever'; var explored = {};
    var stage = el('div', { class: 'svl-stage' });
    var status = el('div', { class: 'svl-live', text: 'Choose a mechanism, commit a trade-off prediction, then run it.' });
    function draw(active) { stage.replaceChildren(svgMarkup(mechanismSVG(current, active), current + ' mechanism model')); }
    draw(false);
    var tabs = el('div', { class: 'svl-actions' });
    kinds.forEach(function (kind) {
      tabs.appendChild(el('button', { type: 'button', class: kind === current ? '' : 'svl-ghost', text: kind, onclick: function (event) {
        current = kind; Array.prototype.forEach.call(tabs.children, function (b) { b.classList.add('svl-ghost'); }); event.currentTarget.classList.remove('svl-ghost'); draw(false); clearPrediction(ctx);
        announce(ctx, kind + ' selected. Predict the input-output trade-off.', 'notice');
      } }));
    });
    var run = el('button', { type: 'button', text: 'Reveal the trade-off', onclick: function () {
      if (!canRun(ctx)) return;
      draw(true); explored[current] = true;
      var expected = current === 'Lever' ? 'Less input force, more input distance' : current === 'Pulley' ? 'Direction changes; ideal force stays similar' : 'Faster output, less turning force';
      var correct = ctx.prediction === expected;
      var detail = current === 'Lever' ? 'A longer effort movement can lift the load with less input force.' : current === 'Pulley' ? 'This fixed-pulley model changes the direction of the force; an ideal single fixed pulley does not reduce its size.' : 'A large driving gear turns the smaller output gear faster, with less turning force at the output.';
      status.textContent = (correct ? 'Prediction supported. ' : 'Revise the prediction. ') + detail;
      announce(ctx, status.textContent, correct ? 'good' : 'notice');
      if (Object.keys(explored).length === 3) complete(ctx, 'Lever, pulley and gear models have all been inspected for their input-output trade-offs.');
    } });
    var controls = el('div', { class: 'svl-controls' }, el('div', { class: 'svl-control' }, el('span', { class: 'svl-label', text: 'Mechanism' }), tabs), run, status, el('p', { class: 'svl-caveat', text: 'Idealised diagrams omit friction and deformation. They show the direction of a trade-off, not free energy.' }));
    host.appendChild(el('div', { class: 'svl-model-grid' }, stage, controls));
  }

  var moonPositions = [
    { code: 'A', phase: 'New', x: 180, y: 175, disc: '<circle cx="510" cy="182" r="66" fill="#111827"/>' },
    { code: 'B', phase: 'First quarter', x: 320, y: 50, disc: '<circle cx="510" cy="182" r="66" fill="#111827"/><path d="M510 116 A66 66 0 0 1 510 248Z" fill="#f8fafc"/>' },
    { code: 'C', phase: 'Full', x: 460, y: 175, disc: '<circle cx="510" cy="182" r="66" fill="#f8fafc" stroke="#334155" stroke-width="3"/>' },
    { code: 'D', phase: 'Last quarter', x: 320, y: 300, disc: '<circle cx="510" cy="182" r="66" fill="#111827"/><path d="M510 116 A66 66 0 0 0 510 248Z" fill="#f8fafc"/>' }
  ];

  function moonSVG(position, revealed) {
    return '<svg viewBox="0 0 620 350" xmlns="http://www.w3.org/2000/svg"><title>Moon phase orbit model</title><desc>The Sun is fixed at the left, Earth is central, and the Moon is shown at one of four orbital positions. A separate Earth-view disc is revealed after prediction.</desc>' +
      '<rect width="620" height="350" fill="#0f172a"/><circle cx="46" cy="175" r="38" fill="#facc15" stroke="#fff7c2" stroke-width="7"/><text x="20" y="236" fill="#fff" font-family="Segoe UI,Arial" font-size="15" font-weight="800">SUN</text>' +
      '<ellipse cx="320" cy="175" rx="145" ry="125" fill="none" stroke="#64748b" stroke-width="2" stroke-dasharray="8 8"/><circle cx="320" cy="175" r="44" fill="#4d82a0" stroke="#dbeafe" stroke-width="4"/><text x="298" y="180" fill="#fff" font-family="Segoe UI,Arial" font-size="14" font-weight="800">EARTH</text>' +
      '<g><circle cx="' + position.x + '" cy="' + position.y + '" r="25" fill="#64748b" stroke="#fff" stroke-width="3"/><path d="M' + position.x + ' ' + (position.y - 25) + ' A25 25 0 0 0 ' + position.x + ' ' + (position.y + 25) + ' L' + position.x + ' ' + (position.y - 25) + 'Z" fill="#f8fafc" opacity=".86"/></g>' +
      '<line x1="86" y1="88" x2="170" y2="88" stroke="#facc15" stroke-width="5"/><line x1="86" y1="175" x2="170" y2="175" stroke="#facc15" stroke-width="5"/><line x1="86" y1="262" x2="170" y2="262" stroke="#facc15" stroke-width="5"/>' +
      '<rect x="430" y="84" width="160" height="196" rx="18" fill="#fff" opacity=".12" stroke="#fff" stroke-width="3"/><text x="455" y="110" fill="#fff" font-family="Segoe UI,Arial" font-size="15" font-weight="800">VIEW FROM EARTH</text>' +
      (revealed ? position.disc + '<text x="510" y="270" text-anchor="middle" fill="#fff" font-family="Segoe UI,Arial" font-size="18" font-weight="900">' + position.phase + '</text>' : '<text x="510" y="188" text-anchor="middle" fill="#cbd5e1" font-family="Segoe UI,Arial" font-size="18" font-weight="800">PREDICT FIRST</text>') + '</svg>';
  }

  function renderMoon(ctx, host) {
    var current = moonPositions[0]; var explored = {};
    var stage = el('div', { class: 'svl-stage' });
    var selectControl = controlSelect('Orbital position', moonPositions.map(function (p) { return { value: p.code, label: 'Position ' + p.code }; }), 'A');
    var select = selectControl.querySelector('select');
    function draw(revealed) { stage.replaceChildren(svgMarkup(moonSVG(current, revealed), 'Moon at orbital position ' + current.code + (revealed ? ', phase ' + current.phase : ', phase withheld'))); }
    select.addEventListener('change', function () { current = moonPositions.find(function (p) { return p.code === select.value; }); clearPrediction(ctx); draw(false); announce(ctx, 'Position ' + current.code + ' selected. Use the Sun-Earth-Moon geometry to predict the Earth-view phase.', 'notice'); });
    draw(false);
    var reveal = el('button', { type: 'button', text: 'Reveal Earth view', onclick: function () {
      if (!canRun(ctx)) return;
      draw(true); explored[current.code] = true;
      var correct = ctx.prediction === current.phase;
      announce(ctx, (correct ? 'Prediction supported. ' : 'Prediction revised. ') + 'Position ' + current.code + ' gives ' + current.phase + '.', correct ? 'good' : 'notice');
      clearPrediction(ctx);
      if (Object.keys(explored).length === 4) complete(ctx, 'All four positions have been connected to the view from Earth.');
    } });
    host.appendChild(el('div', { class: 'svl-model-grid' }, stage, el('div', { class: 'svl-controls' }, selectControl, reveal, el('p', { class: 'svl-caveat', text: 'The orbit and sizes are not to scale. The illuminated half always faces the Sun; phases are viewing geometry, not Earth\'s shadow.' }))));
  }

  function particlePositions(count, side) {
    var points = [];
    for (var i = 0; i < count; i += 1) {
      var col = i % 6, row = Math.floor(i / 6);
      points.push({ x: (side === 'left' ? 45 : 345) + col * 38 + (row % 2) * 8, y: 62 + row * 48 });
    }
    return points;
  }

  function diffusionSVG(left, right, label) {
    var circles = particlePositions(left, 'left').map(function (p, i) { return '<g class="svl-particle"><circle cx="' + p.x + '" cy="' + p.y + '" r="10" fill="#4d82a0" stroke="#1e3a8a" stroke-width="2"/><text x="' + p.x + '" y="' + (p.y + 4) + '" text-anchor="middle" font-size="8" fill="#fff">P</text></g>'; }).join('') +
      particlePositions(right, 'right').map(function (p) { return '<g class="svl-particle"><circle cx="' + p.x + '" cy="' + p.y + '" r="10" fill="#4d82a0" stroke="#1e3a8a" stroke-width="2"/><text x="' + p.x + '" y="' + (p.y + 4) + '" text-anchor="middle" font-size="8" fill="#fff">P</text></g>'; }).join('');
    return '<svg viewBox="0 0 620 330" xmlns="http://www.w3.org/2000/svg"><title>Two-compartment diffusion particle model</title><desc>Identical particles move randomly on both sides of a boundary. Counts show the net change from the more concentrated side to the less concentrated side.</desc><rect width="620" height="330" fill="#f8fafc"/><rect x="22" y="35" width="276" height="248" rx="12" fill="#eff6ff" stroke="#334155" stroke-width="4"/><rect x="322" y="35" width="276" height="248" rx="12" fill="#eff6ff" stroke="#334155" stroke-width="4"/><line x1="310" y1="35" x2="310" y2="283" stroke="#64748b" stroke-width="5" stroke-dasharray="10 7"/>' + circles + '<text x="160" y="312" text-anchor="middle" font-family="Segoe UI,Arial" font-size="17" font-weight="900">LEFT: ' + left + '</text><text x="460" y="312" text-anchor="middle" font-family="Segoe UI,Arial" font-size="17" font-weight="900">RIGHT: ' + right + '</text><text x="310" y="24" text-anchor="middle" font-family="Segoe UI,Arial" font-size="14" font-weight="800" fill="#475569">' + label + '</text></svg>';
  }

  function renderDiffusion(ctx, host) {
    var gradient = controlSelect('Starting concentration difference', [{ value: 'small', label: 'Small · 16 left / 12 right' }, { value: 'medium', label: 'Medium · 20 left / 8 right' }, { value: 'large', label: 'Large · 24 left / 4 right' }], 'medium');
    var temperature = controlSelect('Temperature in the model', [{ value: '1', label: 'Cool' }, { value: '2', label: 'Warm' }, { value: '3', label: 'Hot' }], '2');
    var gSelect = gradient.querySelector('select'), tSelect = temperature.querySelector('select');
    var starts = { small: [16, 12], medium: [20, 8], large: [24, 4] };
    var stage = el('div', { class: 'svl-stage' }); var trials = []; var tbody = el('tbody');
    var table = el('table', { class: 'svl-data-table' }, el('thead', {}, el('tr', {}, el('th', { text: 'Gradient' }), el('th', { text: 'Temp' }), el('th', { text: 'Before L:R' }), el('th', { text: 'After L:R' }), el('th', { text: 'Net →' }))), tbody);
    function draw(left, right, label) { stage.replaceChildren(svgMarkup(diffusionSVG(left, right, label), 'Diffusion model with ' + left + ' particles left and ' + right + ' right')); }
    function resetView() { var start = starts[gSelect.value]; draw(start[0], start[1], 'before run · particles also move right to left'); }
    gSelect.addEventListener('change', resetView); tSelect.addEventListener('change', resetView); resetView();
    var run = el('button', { type: 'button', text: 'Run and freeze', onclick: function () {
      if (!canRun(ctx)) return;
      var start = starts[gSelect.value].slice();
      var difference = start[0] - start[1];
      var moved = Math.max(1, Math.min(Math.floor(difference / 2), Math.ceil((Number(tSelect.value) + ({ small: 1, medium: 2, large: 3 }[gSelect.value])) / 2)));
      draw(start[0], start[1], 'running · random movement occurs both ways');
      run.disabled = true;
      global.setTimeout(function () {
        var after = [start[0] - moved, start[1] + moved];
        draw(after[0], after[1], 'frozen evidence · net left to right = ' + moved);
        trials.push({ g: gSelect.options[gSelect.selectedIndex].text.split(' ·')[0], t: tSelect.options[tSelect.selectedIndex].text, before: start.join(':'), after: after.join(':'), net: moved });
        tbody.replaceChildren();
        trials.slice(-4).forEach(function (r) { tbody.appendChild(el('tr', {}, el('td', { text: r.g }), el('td', { text: r.t }), el('td', { text: r.before }), el('td', { text: r.after }), el('td', { text: String(r.net) }))); });
        var correct = ctx.prediction === 'Net left to right';
        announce(ctx, (correct ? 'Prediction supported. ' : 'Prediction revised. ') + 'Both directions occur, but the count change shows net movement from high to low concentration.', correct ? 'good' : 'notice');
        run.disabled = false;
        if (trials.length >= 2) complete(ctx, 'Two finite trials are recorded. Compare the gradients or temperatures before writing the pattern.');
      }, ctx.isStatic() ? 20 : Math.max(500, 1200 - Number(tSelect.value) * 180));
    } });
    var controls = el('div', { class: 'svl-controls' }, gradient, temperature, run, table, el('p', { class: 'svl-caveat', text: 'Illustrative particle counts, not laboratory measurements. The model shows direction and comparative rate only.' }));
    host.appendChild(el('div', { class: 'svl-model-grid' }, stage, controls));
  }

  function osmosisSVG(outside, radius, direction) {
    var outsideSolute = outside === 'dilute' ? 4 : outside === 'same' ? 9 : 16;
    var waterOutside = outside === 'dilute' ? 18 : outside === 'same' ? 13 : 7;
    var waterDots = '';
    for (var i = 0; i < waterOutside; i += 1) {
      var x = 35 + (i % 6) * 43, y = 55 + Math.floor(i / 6) * 55;
      waterDots += '<circle cx="' + x + '" cy="' + y + '" r="8" fill="#dbeafe" stroke="#1e3a8a" stroke-width="2"/><text x="' + x + '" y="' + (y + 3) + '" font-size="7" text-anchor="middle">W</text>';
    }
    var solutes = '';
    for (var j = 0; j < outsideSolute; j += 1) {
      var sx = 48 + (j % 5) * 49, sy = 82 + Math.floor(j / 5) * 55;
      solutes += '<rect x="' + (sx - 7) + '" y="' + (sy - 7) + '" width="14" height="14" rx="2" fill="#fef3c7" stroke="#7c5a10" stroke-width="2"/><text x="' + sx + '" y="' + (sy + 3) + '" font-size="7" text-anchor="middle">S</text>';
    }
    var arrow = direction === 'in' ? '<path d="M270 178 H375" stroke="#4d82a0" stroke-width="9"/><path d="M357 163 l20 15 l-20 15" fill="#4d82a0"/>' : direction === 'out' ? '<path d="M375 178 H270" stroke="#4d82a0" stroke-width="9"/><path d="M288 163 l-20 15 l20 15" fill="#4d82a0"/>' : '<path d="M280 165 H365 M365 191 H280" stroke="#4d82a0" stroke-width="6"/>';
    return '<svg viewBox="0 0 650 350" xmlns="http://www.w3.org/2000/svg"><title>Osmosis particle model</title><desc>Water particles and larger solute particles are shown outside a cell. A partially permeable membrane allows water movement, changing the model cell size.</desc><rect width="650" height="350" fill="#f8fafc"/><rect x="20" y="35" width="285" height="270" rx="14" fill="#eff6ff" stroke="#334155" stroke-width="4"/>' + waterDots + solutes + '<circle cx="495" cy="175" r="' + radius + '" fill="#ecfdf3" stroke="#3f7d6e" stroke-width="7" stroke-dasharray="8 5"/><g fill="#dbeafe" stroke="#1e3a8a" stroke-width="2"><circle cx="470" cy="145" r="8"/><circle cx="510" cy="140" r="8"/><circle cx="535" cy="180" r="8"/><circle cx="485" cy="205" r="8"/><circle cx="455" cy="185" r="8"/></g><g fill="#fef3c7" stroke="#7c5a10" stroke-width="2"><rect x="491" y="166" width="15" height="15"/><rect x="514" y="202" width="15" height="15"/></g>' + arrow + '<text x="162" y="330" text-anchor="middle" font-family="Segoe UI,Arial" font-weight="900">OUTSIDE: ' + outside + '</text><text x="495" y="330" text-anchor="middle" font-family="Segoe UI,Arial" font-weight="900">CELL MODEL</text><text x="20" y="20" font-family="Segoe UI,Arial" font-size="13" fill="#475569">W = water · S = solute · symbols and labels prevent colour-only meaning</text></svg>';
  }

  function renderOsmosis(ctx, host) {
    var solution = controlSelect('Outside solution', [{ value: 'dilute', label: 'Dilute outside solution' }, { value: 'same', label: 'Same concentration as cell' }, { value: 'concentrated', label: 'Concentrated outside solution' }], 'dilute');
    var select = solution.querySelector('select'); var stage = el('div', { class: 'svl-stage' }); var explored = {};
    function draw(radius, direction) { stage.replaceChildren(svgMarkup(osmosisSVG(select.value, radius, direction), 'Osmosis model with ' + select.value + ' outside solution')); }
    select.addEventListener('change', function () { clearPrediction(ctx); draw(78, 'none'); announce(ctx, 'Outside concentration changed. Predict net water movement before running.', 'notice'); });
    draw(78, 'none');
    var run = el('button', { type: 'button', text: 'Run and freeze', onclick: function () {
      if (!canRun(ctx)) return;
      var map = { dilute: { radius: 92, direction: 'in', answer: 'Water moves into the cell' }, same: { radius: 78, direction: 'none', answer: 'No net water movement' }, concentrated: { radius: 66, direction: 'out', answer: 'Water moves out of the cell' } };
      var result = map[select.value]; draw(result.radius, result.direction); explored[select.value] = true;
      var correct = ctx.prediction === result.answer;
      announce(ctx, (correct ? 'Prediction supported. ' : 'Prediction revised. ') + result.answer + ' because water moves from higher to lower water concentration through the membrane.', correct ? 'good' : 'notice');
      clearPrediction(ctx);
      if (Object.keys(explored).length === 3) complete(ctx, 'Dilute, equal and concentrated surroundings have all been tested against the same cell model.');
    } });
    host.appendChild(el('div', { class: 'svl-model-grid' }, stage, el('div', { class: 'svl-controls' }, solution, run, el('p', { class: 'svl-caveat', text: 'The changing circle is a conceptual cell model. Animal and plant cells respond differently because plant cells also have a cell wall.' }))));
  }

  function renderModel(ctx, host) {
    var name = ctx.activity.model;
    if (name === 'muscles') return renderMuscles(ctx, host);
    if (name === 'friction') return renderFriction(ctx, host);
    if (name === 'mechanisms') return renderMechanisms(ctx, host);
    if (name === 'moon') return renderMoon(ctx, host);
    if (name === 'diffusion') return renderDiffusion(ctx, host);
    if (name === 'osmosis') return renderOsmosis(ctx, host);
    host.appendChild(el('p', { class: 'svl-live', text: 'Model not available: ' + name }));
  }

  function renderActivity(ctx, host) {
    switch (ctx.activity.type) {
      case 'sort': return renderSort(ctx, host);
      case 'sequence': return renderSequence(ctx, host);
      case 'evidence': return renderEvidence(ctx, host);
      case 'calculation': return renderCalculation(ctx, host);
      case 'hotspot': return renderHotspot(ctx, host);
      case 'model': return renderModel(ctx, host);
      default: host.appendChild(el('p', { class: 'svl-live', text: 'Unknown activity type: ' + ctx.activity.type }));
    }
  }

  function copyText(text) {
    if (global.navigator && global.navigator.clipboard && global.isSecureContext) return global.navigator.clipboard.writeText(text);
    return new Promise(function (resolve, reject) {
      var area = el('textarea', { value: text, style: { position: 'fixed', left: '-9999px', top: '0' } });
      document.body.appendChild(area); area.select();
      try { document.execCommand('copy'); area.remove(); resolve(); } catch (err) { area.remove(); reject(err); }
    });
  }

  function buildPanel(slug, payload) {
    var panel = el('section', { class: 'svl-panel', dataset: { lesson: slug, pathway: payload.pathway }, 'aria-label': payload.title });
    var head = el('header', { class: 'svl-head' },
      el('h3', { class: 'svl-title', text: payload.title }),
      el('span', { class: 'svl-chip', text: payload.pathway + ' visual lab' }),
      el('p', { class: 'svl-purpose', text: payload.purpose })
    );
    var body = el('div', { class: 'svl-body' });
    var live = el('div', { class: 'svl-live', role: 'status', 'aria-live': 'polite', text: 'Ready. Use the prompt, make a decision and then manipulate the model or information.' });
    var ctx = {
      slug: slug, payload: payload, pathway: payload.pathway, activity: payload.activity || {}, panel: panel, body: body, live: live,
      prediction: '', predictionGroup: null, evidenceInput: null, explanation: null, completed: false,
      isStatic: function () { return reducedMotion || panel.classList.contains('svl-static'); }
    };
    body.appendChild(el('p', { class: 'svl-prompt' }, el('strong', { text: 'Together: ' }), document.createTextNode(ctx.activity.prompt || 'Use the visual evidence to solve the task.')));
    var prediction = predictionGate(ctx); if (prediction) body.appendChild(prediction);
    var activityHost = el('div', { class: 'svl-activity' }); body.appendChild(activityHost);
    renderActivity(ctx, activityHost);
    var evidence = evidenceGate(ctx); if (evidence) body.appendChild(evidence);
    body.appendChild(explanationNode(ctx));
    var independent = el('details', { class: 'svl-independent', style: { marginTop: '10px' } },
      el('summary', { text: 'Independent transfer task' }), el('p', { class: 'svl-small', text: payload.independent || 'Use the completed visual to produce an independent explanation.' })
    );
    body.appendChild(independent);
    body.appendChild(live);

    var staticButton = el('button', { type: 'button', class: 'svl-ghost', 'aria-pressed': 'false', text: 'Static diagrams: off', onclick: function () {
      var on = !panel.classList.contains('svl-static'); panel.classList.toggle('svl-static', on);
      staticButton.setAttribute('aria-pressed', String(on)); staticButton.textContent = 'Static diagrams: ' + (on ? 'on' : 'off');
      announce(ctx, on ? 'Static diagram mode is on. All essential information remains available.' : 'Finite motion is available again.', 'notice');
    } });
    var resetButton = el('button', { type: 'button', class: 'svl-neutral', text: 'Reset lab', onclick: function () {
      var fresh = buildPanel(slug, payload); panel.replaceWith(fresh); fresh.scrollIntoView({ block: 'nearest' });
    } });
    var copyButton = el('button', { type: 'button', class: 'svl-ghost', text: 'Copy evidence note', onclick: function () {
      var note = ctx.evidenceInput && ctx.evidenceInput.value.trim();
      var text = payload.title + '\n' + (note || 'No evidence note recorded yet.') + '\nIndependent transfer: ' + (payload.independent || '');
      copyText(text).then(function () { announce(ctx, 'Evidence note copied.', 'good'); }).catch(function () { announce(ctx, 'Copy was blocked by this browser. Select the note manually.', 'bad'); });
    } });
    body.appendChild(el('div', { class: 'svl-toolbar' }, el('div', { class: 'svl-actions' }, resetButton, staticButton), copyButton));
    panel.append(head, body);
    return panel;
  }

  function mountBySlug(slug, target) {
    slug = normaliseSlug(slug);
    var payload = PAYLOADS[slug];
    if (!payload || !target) return null;
    if (target.querySelector && target.querySelector('.svl-panel[data-lesson="' + cssEscape(slug) + '"]')) return target.querySelector('.svl-panel[data-lesson="' + cssEscape(slug) + '"]');
    var panel = buildPanel(slug, payload);
    target.appendChild(panel);
    return panel;
  }

  function mountAll() {
    var slug = currentSlug();
    if (!slug || !PAYLOADS[slug]) return [];
    var target = findTarget(PAYLOADS[slug]);
    var panel = mountBySlug(slug, target);
    return panel ? [panel] : [];
  }

  global.ScienceVisualLearning = {
    version: '1.0.0',
    mountAll: mountAll,
    mountBySlug: mountBySlug,
    payloads: PAYLOADS
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mountAll, { once: true });
  else mountAll();
})(typeof window !== 'undefined' ? window : this);

