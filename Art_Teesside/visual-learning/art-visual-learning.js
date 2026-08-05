
/* Art Visual Learning Layer v1.0
   Add-only, dependency-free, no network requests, no persistent pupil data. Art process models preserve authored Arts Award evidence and studio constraints. */
(function (global) {
  'use strict';

  var document = global.document;
  if (!document || global.ArtVisualLearning) return;

  var PAYLOADS = global.ArtVisualPayloads || {};
  /* As recovered, reducedMotion was computed once at load with no change
     listener, so an OS preference changed mid-session was never honoured in
     JS. The blanket CSS rule still applied, so it degraded rather than failed.
     The query is now watched, and isStatic() reads the live value. */
  var motionQuery = global.matchMedia ? global.matchMedia('(prefers-reduced-motion: reduce)') : null;
  var reducedMotion = !!(motionQuery && motionQuery.matches);
  if (motionQuery) {
    var onMotionChange = function (event) { reducedMotion = !!event.matches; };
    if (motionQuery.addEventListener) motionQuery.addEventListener('change', onMotionChange);
    else if (motionQuery.addListener) motionQuery.addListener(onMotionChange);
  }

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
    var wrap = el('div', { class: 'avl-svg-wrap', html: markup });
    var svg = wrap.querySelector('svg');
    if (svg) {
      svg.setAttribute('role', 'img');
      svg.setAttribute('aria-label', label || 'Interactive art teaching diagram');
      svg.setAttribute('focusable', 'false');
    }
    return wrap.firstElementChild;
  }

  function normaliseSlug(value) {
    return String(value || '').replace(/\.html?$/i, '').replace(/[^A-Za-z0-9_\-]/g, '');
  }

  function currentSlug() {
    var explicit = document.documentElement.getAttribute('data-avl-lesson') || document.body && document.body.getAttribute('data-avl-lesson');
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
    String(seedText || 'art').split('').forEach(function (c) { seed = (seed * 31 + c.charCodeAt(0)) >>> 0; });
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
    var gate = el('div', { class: 'avl-gate' },
      el('h4', { text: ctx.pathway === 'BUILD' ? 'Say it before the model moves' : 'Commit a prediction before running the model' }),
      el('div', { class: 'avl-predict-options', role: 'group', 'aria-label': 'Prediction choices' })
    );
    var group = gate.querySelector('.avl-predict-options');
    options.forEach(function (option) {
      var button = el('button', {
        type: 'button', class: 'avl-predict-option', text: option, 'aria-pressed': 'false',
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
    var gate = el('div', { class: 'avl-gate' },
      el('h4', { text: 'Evidence before explanation' }),
      el('label', { class: 'avl-label', for: ctx.slug + '-evidence', text: prompt }),
      el('textarea', {
        id: ctx.slug + '-evidence', class: 'avl-evidence-input', disabled: true,
        placeholder: 'Complete the activity first. Then record the evidence or pattern you noticed.',
        'aria-describedby': ctx.slug + '-evidence-help'
      }),
      el('p', { id: ctx.slug + '-evidence-help', class: 'avl-small', text: 'This note stays in this page only. Nothing is saved or sent.' })
    );
    ctx.evidenceInput = gate.querySelector('textarea');
    ctx.evidenceInput.addEventListener('input', function () { refreshExplanation(ctx); });
    return gate;
  }

  /* The staff route to the explanation.

     The chassis exit slide already carries the adult answer organ: a button
     toggling .show-ans on #exit-slide. The explanation follows that same
     organ. No second toggle concept, and no new adult control invented.

     Without this, a LAUNCH pupil must complete the activity AND type eight
     characters before the teaching appears, with no adult override on screen.
     A pupil-facing gate must have no failing answer: a pupil with writing
     difficulty must not be the one person who cannot reach the teaching. */
  function staffAnswersShown() {
    var exit = document.getElementById('exit-slide');
    return !!(exit && exit.classList.contains('show-ans'));
  }

  function refreshExplanation(ctx) {
    var staff = staffAnswersShown();
    if (!ctx.completed && !staff) { ctx.explanation.hidden = true; return; }
    var evidenceReady = !ctx.evidenceInput || ctx.evidenceInput.value.trim().length >= 8;
    if (ctx.pathway === 'LAUNCH' && !evidenceReady && !staff) {
      ctx.explanation.hidden = true;
      announce(ctx, 'Activity complete. Record a specific observation, value or pattern to unlock the explanation.', 'notice');
      return;
    }
    ctx.explanation.hidden = false;
    if (!ctx.explanation.dataset.opened) {
      ctx.explanation.dataset.opened = '1';
      ctx.explanation.dataset.artOpenedBy = staff && !ctx.completed
        ? 'staff answer reveal'
        : (ctx.pathway === 'LAUNCH' ? 'completed activity and recorded evidence' : 'completed teaching interaction');
      ctx.explanation.classList.add('avl-reveal');
      announce(ctx, 'Explanation unlocked. Read it against the evidence you produced.', 'good');
    }
  }

  /* Panels re-check the staff organ whenever it is toggled, so the reveal is
     live rather than only correct at mount time. Contexts whose panel has been
     replaced (Reset lab) are pruned rather than left to accumulate. */
  var MOUNTED = [];
  var staffObserver = null;

  function watchStaffToggle() {
    if (staffObserver || !global.MutationObserver) return;
    var exit = document.getElementById('exit-slide');
    if (!exit) return;
    staffObserver = new global.MutationObserver(function () {
      MOUNTED = MOUNTED.filter(function (c) { return c.explanation && c.explanation.isConnected; });
      MOUNTED.forEach(function (c) { refreshExplanation(c); });
    });
    staffObserver.observe(exit, { attributes: true, attributeFilter: ['class'] });
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
    var node = el('div', { class: 'avl-explanation', hidden: true, text: ctx.activity.completion || 'Use the evidence to explain the pattern.' });
    ctx.explanation = node;
    return node;
  }

  function renderSort(ctx, host) {
    var activity = ctx.activity;
    var selected = null;
    var placed = {};
    var items = shuffle(activity.items || [], ctx.slug + '-sort');
    var layout = el('div', { class: 'avl-sort-layout' });
    var bank = el('div', { class: 'avl-bank' },
      el('h4', { class: 'avl-bank-title', text: 'Cards · click a card, then a destination; dragging is optional' }),
      el('div', { class: 'avl-card-list', role: 'list', 'aria-label': 'Cards to place' })
    );
    var bankList = bank.querySelector('.avl-card-list');
    var zones = el('div', { class: 'avl-zones' },
      el('h4', { class: 'avl-bank-title', text: 'Destinations' }),
      el('div', { class: 'avl-zone-grid' })
    );
    var zoneGrid = zones.querySelector('.avl-zone-grid');
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
      zone.querySelector('.avl-card-list').appendChild(card);
      placed[id] = categoryId;
      selected = null;
      announce(ctx, item.label + ': correct. ' + (item.reason || ''), 'good');
      if (Object.keys(placed).length === activity.items.length) complete(ctx, 'All cards are placed using the visual rule.');
    }

    items.forEach(function (item) {
      var button = el('button', {
        type: 'button', class: 'avl-card', draggable: true, role: 'listitem', 'aria-pressed': 'false',
        dataset: { id: item.id, label: item.label },
        onclick: function () { selectCard(item.id, button); }
      },
      el('span', { class: 'avl-card-icon', 'aria-hidden': 'true', text: item.icon || '•' }),
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
      var zone = el('section', { class: 'avl-zone', dataset: { category: category.id } },
        el('button', {
          type: 'button', class: 'avl-zone-head avl-ghost',
          'aria-label': 'Place selected card in ' + category.label,
          onclick: function () {
            if (!selected) { announce(ctx, 'Select a card first, then choose this destination.', 'notice'); return; }
            place(selected, category.id);
          }
        }, el('span', { class: 'avl-zone-icon', 'aria-hidden': 'true', text: category.icon || '•' }), el('span', { text: category.label })),
        el('div', { class: 'avl-card-list', role: 'list', 'aria-label': category.label + ' cards' })
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
    var list = el('ol', { class: 'avl-sequence', 'aria-label': 'Sequence to arrange' });
    var draggedId = '';

    function redraw() {
      list.replaceChildren();
      order.forEach(function (item, index) {
        var row = el('li', { class: 'avl-sequence-item', draggable: true, dataset: { id: item.id } },
          el('span', { class: 'avl-sequence-text', text: item.label }),
          el('span', { class: 'avl-sequence-controls' },
            el('button', {
              type: 'button', class: 'avl-small-btn avl-ghost', 'aria-label': 'Move ' + item.label + ' up', text: '↑', disabled: index === 0,
              onclick: function () { if (index > 0) { var x = order[index - 1]; order[index - 1] = order[index]; order[index] = x; redraw(); } }
            }),
            el('button', {
              type: 'button', class: 'avl-small-btn avl-ghost', 'aria-label': 'Move ' + item.label + ' down', text: '↓', disabled: index === order.length - 1,
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
          announce(ctx, count + ' of ' + order.length + ' positions are correct. Use the visual or process reason for each step, not just memory.', 'notice');
        }
      }
    });
    redraw();
    host.append(list, el('div', { class: 'avl-arrow-rail', 'aria-hidden': 'true', text: '↓  ↓  ↓' }), el('div', { class: 'avl-actions' }, check));
  }

  function renderEvidence(ctx, host) {
    var activity = ctx.activity;
    var selected = {};
    var grid = el('div', { class: 'avl-evidence-grid', role: 'group', 'aria-label': 'Evidence statements' });
    var buttons = {};
    shuffle(activity.statements || [], ctx.slug + '-evidence').forEach(function (statement) {
      var button = el('button', {
        type: 'button', class: 'avl-evidence-card', text: statement.label, 'aria-pressed': 'false',
        onclick: function () {
          selected[statement.id] = !selected[statement.id];
          button.setAttribute('aria-pressed', String(!!selected[statement.id]));
          button.classList.remove('is-correct', 'is-wrong');
        }
      });
      buttons[statement.id] = button;
      grid.appendChild(button);
    });
    var reasons = el('ul', { class: 'avl-reason-list', hidden: true });
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
    host.append(grid, el('div', { class: 'avl-actions', style: { marginTop: '10px' } }, check), reasons);
  }


  function controlSelect(label, options, value) {
    var select = el('select', { 'aria-label': label });
    options.forEach(function (option) {
      var val = typeof option === 'string' ? option : option.value;
      var text = typeof option === 'string' ? option : option.label;
      select.appendChild(el('option', { value: val, text: text, selected: val === value }));
    });
    return el('label', { class: 'avl-control' }, el('span', { class: 'avl-label', text: label }), select);
  }

  function drawStage(stage, markup, label) {
    stage.replaceChildren(svgMarkup(markup, label));
  }

  function trialTable(headers) {
    var table = el('table', { class: 'avl-data-table' });
    var head = el('thead');
    var row = el('tr');
    headers.forEach(function (h) { row.appendChild(el('th', { scope: 'col', text: h })); });
    head.appendChild(row);
    table.append(head, el('tbody'));
    return table;
  }

  function addTrial(table, cells) {
    var row = el('tr');
    cells.forEach(function (value) { row.appendChild(el('td', { text: value })); });
    table.querySelector('tbody').appendChild(row);
  }

  function artBase(title, desc, inner) {
    return '<svg viewBox="0 0 680 360" xmlns="http://www.w3.org/2000/svg"><title>' + title + '</title><desc>' + desc + '</desc><rect width="680" height="360" fill="#f8f5ee"/><text x="22" y="28" font-family="Segoe UI,Arial" font-size="14" font-weight="800" fill="#334155">MODEL · one decision at a time</text>' + inner + '</svg>';
  }

  function sceneFormal() {
    return '<svg viewBox="0 0 720 390" xmlns="http://www.w3.org/2000/svg"><title>Teesside formal elements observation scene</title><desc>A stylised industrial riverside with a steel bridge, crane, rust plate, rivets and reflections. Numbered hotspots are overlaid by the lesson component.</desc><defs><pattern id="avl-rust" width="30" height="30" patternUnits="userSpaceOnUse"><rect width="30" height="30" fill="#b75a35"/><circle cx="7" cy="8" r="3" fill="#6e3b2b"/><circle cx="23" cy="17" r="4" fill="#d79249"/><path d="M2 25 l10 -4" stroke="#70412f" stroke-width="3"/></pattern><linearGradient id="avl-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#dfeaf0"/><stop offset="1" stop-color="#f5d6b2"/></linearGradient></defs><rect width="720" height="390" fill="url(#avl-sky)"/><rect y="230" width="720" height="160" fill="#6d91a1"/><g opacity=".45" stroke="#eef6f8" stroke-width="8"><path d="M0 270 H180"/><path d="M250 300 H460"/><path d="M510 255 H720"/><path d="M60 345 H300"/></g><g fill="none" stroke="#263b46" stroke-width="9"><path d="M28 88 H430"/><path d="M55 88 L138 218 L225 88 L312 218 L397 88"/><path d="M28 88 L28 222 M430 88 L430 222"/></g><g fill="#d8a63b" stroke="#263b46" stroke-width="4"><circle cx="76" cy="94" r="8"/><circle cx="126" cy="94" r="8"/><circle cx="176" cy="94" r="8"/><circle cx="226" cy="94" r="8"/><circle cx="276" cy="94" r="8"/><circle cx="326" cy="94" r="8"/></g><g fill="none" stroke="#334155" stroke-width="7"><path d="M490 215 V70 H640"/><path d="M520 72 L635 135"/><path d="M560 72 L560 205"/><path d="M638 70 V222"/></g><rect x="210" y="205" width="150" height="84" rx="8" fill="url(#avl-rust)" stroke="#4b332a" stroke-width="5"/><g opacity=".75"><path d="M35 260 L185 312" stroke="#263b46" stroke-width="9"/><path d="M85 260 L222 330" stroke="#d8a63b" stroke-width="5"/><path d="M492 248 L630 325" stroke="#334155" stroke-width="8"/></g><text x="22" y="375" font-family="Segoe UI,Arial" font-size="14" fill="#334155">PHOTOGRAPHIC FEATURES SIMPLIFIED INTO AN ORIGINAL MODEL</text></svg>';
  }

  function sceneEvent(mode) {
    var advanced = mode === 'analysis';
    return '<svg viewBox="0 0 720 390" xmlns="http://www.w3.org/2000/svg"><title>' + (advanced ? 'Arts experience analysis scene' : 'Arts event observation scene') + '</title><desc>A fictional accessible gallery with abstract artworks, interpretation, audience route, seating and a caption screen.</desc><rect width="720" height="390" fill="#f7f3eb"/><path d="M35 55 H685 V340 H35Z" fill="#fff" stroke="#334155" stroke-width="5"/><path d="M35 290 H685" stroke="#c8b9a6" stroke-width="4"/><rect x="90" y="85" width="170" height="145" fill="#24465b" stroke="#172f3d" stroke-width="5"/><path d="M105 195 C145 115 205 210 245 105" fill="none" stroke="#d1673d" stroke-width="18"/><circle cx="175" cy="153" r="31" fill="#dfad3e"/><rect x="315" y="85" width="170" height="145" fill="#efe3d0" stroke="#334155" stroke-width="5"/><g fill="#2ba193"><path d="M340 205 L400 105 L460 205Z"/><circle cx="401" cy="160" r="22" fill="#7659a7"/></g><rect x="525" y="112" width="105" height="68" rx="5" fill="#edf2f4" stroke="#334155" stroke-width="3"/><g fill="#334155"><rect x="538" y="126" width="72" height="6"/><rect x="538" y="140" width="56" height="6"/><rect x="538" y="154" width="65" height="6"/></g><rect x="540" y="215" width="105" height="58" rx="6" fill="#14212b"/><text x="592" y="240" text-anchor="middle" fill="#fff" font-family="Segoe UI,Arial" font-size="13" font-weight="800">CAPTIONS</text><path d="M548 254 H635" stroke="#fff" stroke-width="4" stroke-dasharray="8 5"/><g fill="#64748b"><circle cx="286" cy="292" r="13"/><path d="M286 305 V340 M267 322 H305" stroke="#64748b" stroke-width="8"/><circle cx="410" cy="287" r="13"/><path d="M410 300 V340 M391 318 H429" stroke="#64748b" stroke-width="8"/></g><rect x="92" y="280" width="100" height="28" rx="8" fill="#dfe7e9" stroke="#334155" stroke-width="3"/><path d="M70 325 C155 350 250 345 350 320 C470 290 575 322 660 310" fill="none" stroke="#2ba193" stroke-width="7" stroke-dasharray="12 9"/><path d="M645 296 l18 14 l-19 13" fill="#2ba193"/><text x="53" y="80" font-family="Segoe UI,Arial" font-size="14" font-weight="800" fill="#334155">FICTIONAL EVENT SCENE · observe before judging</text></svg>';
  }

  function renderHotspot(ctx, host) {
    var activity = ctx.activity;
    var markup = activity.scene === 'formal' ? sceneFormal() : sceneEvent(activity.scene);
    var stage = el('div', { class: 'avl-hotspot-stage' });
    stage.appendChild(svgMarkup(markup, activity.scene === 'formal' ? 'Teesside formal elements observation model' : 'Accessible arts experience observation model'));
    var list = el('div', { class: 'avl-hotspot-list' });
    var opened = {};
    (activity.hotspots || []).forEach(function (spot, index) {
      var note = el('div', { class: 'avl-hotspot-note', hidden: true }, el('strong', { text: (index + 1) + ' · ' + spot.label }), el('div', { text: spot.note }));
      var button = el('button', {
        type: 'button', class: 'avl-hotspot', text: String(index + 1),
        style: { '--x': spot.x, '--y': spot.y }, 'aria-label': 'Open hotspot ' + (index + 1) + ': ' + spot.label,
        onclick: function () {
          opened[spot.id] = true; button.classList.add('is-open'); note.hidden = false;
          announce(ctx, spot.label + ': ' + spot.note, 'good');
          if (Object.keys(opened).length === activity.hotspots.length) complete(ctx, 'Every visual feature has been observed. Use one exact feature as evidence in the explanation.');
        }
      });
      stage.appendChild(button); list.appendChild(note);
    });
    host.appendChild(el('div', { class: 'avl-hotspot-wrap' }, stage, list));
  }

  function markPaths(tool, pressure, direction, running) {
    var width = pressure === 'light' ? 2 : pressure === 'medium' ? 5 : 9;
    var opacity = pressure === 'light' ? .55 : pressure === 'medium' ? .78 : .94;
    var count = tool === 'card' ? 6 : tool === 'charcoal' ? 13 : 9;
    var paths = '';
    for (var i = 0; i < count; i += 1) {
      var offset = i * (tool === 'card' ? 22 : 12);
      if (direction === 'vertical') paths += '<path class="avl-mark-stroke ' + (running ? 'is-running' : '') + '" d="M' + (245 + offset) + ' 102 C' + (238 + offset) + ' 155 ' + (252 + offset) + ' 218 ' + (245 + offset) + ' 270"/>';
      else if (direction === 'cross') paths += '<path class="avl-mark-stroke ' + (running ? 'is-running' : '') + '" d="M220 ' + (110 + offset * .75) + ' L515 ' + (80 + offset * .75) + ' M220 ' + (80 + offset * .75) + ' L515 ' + (125 + offset * .75) + '"/>';
      else paths += '<path class="avl-mark-stroke ' + (running ? 'is-running' : '') + '" d="M225 ' + (115 + offset) + ' C300 ' + (75 + offset) + ' 405 ' + (155 + offset) + ' 520 ' + (105 + offset) + '"/>';
    }
    var dash = tool === 'pencil' ? 'stroke-dasharray="0"' : tool === 'charcoal' ? 'stroke-dasharray="18 5"' : 'stroke-linecap="square"';
    return '<g fill="none" stroke="' + (tool === 'charcoal' ? '#31343a' : tool === 'card' ? '#9b5b3d' : '#465f70') + '" stroke-width="' + width + '" opacity="' + opacity + '" ' + dash + '>' + paths + '</g>';
  }

  function surfaceSVG(tool, pressure, direction, running) {
    var toolLabel = { pencil: 'GRAPHITE', charcoal: 'CHARCOAL', card: 'CARD EDGE' }[tool];
    return artBase('Surface mark laboratory', 'A tool, pressure and direction create a frozen mark sample.', '<rect x="185" y="68" width="390" height="238" rx="14" fill="#fff" stroke="#334155" stroke-width="4"/>' + markPaths(tool, pressure, direction, running) + '<g transform="translate(42 92)"><rect width="104" height="176" rx="14" fill="#e8dfd2" stroke="#334155" stroke-width="4"/><text x="52" y="44" text-anchor="middle" font-family="Segoe UI,Arial" font-weight="900" fill="#334155">' + toolLabel + '</text><path d="M25 91 H79" stroke="#334155" stroke-width="' + (pressure === 'light' ? 3 : pressure === 'medium' ? 7 : 12) + '"/><text x="52" y="126" text-anchor="middle" font-family="Segoe UI,Arial" font-size="13" fill="#334155">' + pressure.toUpperCase() + '</text><text x="52" y="148" text-anchor="middle" font-family="Segoe UI,Arial" font-size="12" fill="#334155">' + direction.toUpperCase() + '</text></g><text x="380" y="332" text-anchor="middle" font-family="Segoe UI,Arial" font-weight="800" fill="#334155">sample freezes so the class can point to evidence</text>');
  }

  function renderSurfaceMarks(ctx, host) {
    var tool = controlSelect('Tool', [{value:'pencil',label:'Graphite pencil'},{value:'charcoal',label:'Charcoal'},{value:'card',label:'Card edge'}], 'pencil');
    var pressure = controlSelect('Pressure', ['light','medium','firm'], 'light');
    var direction = controlSelect('Direction', [{value:'horizontal',label:'One direction'},{value:'cross',label:'Crossed marks'},{value:'vertical',label:'Vertical marks'}], 'horizontal');
    var selects=[tool,pressure,direction].map(function(c){return c.querySelector('select');});
    var stage=el('div',{class:'avl-stage'}); var tried={};
    function draw(run){drawStage(stage,surfaceSVG(selects[0].value,selects[1].value,selects[2].value,run),'Surface mark sample');}
    selects.forEach(function(s){s.addEventListener('change',function(){draw(false); announce(ctx,'Choice changed. Say what kind of surface the mark might suggest before making the sample.','notice');});});
    draw(false);
    var run=el('button',{type:'button',text:'Make one sample',onclick:function(){
      draw(!ctx.isStatic()); var key=selects.map(function(s){return s.value;}).join('|'); tried[key]=true;
      var surface=selects[0].value==='charcoal'&&selects[1].value==='firm'?'dense or soot-like':selects[2].value==='cross'?'woven, scratched or layered':'directional and controlled';
      announce(ctx,'Frozen sample: '+surface+'. Record tool, pressure and direction beside it.','good');
      if(Object.keys(tried).length>=3) complete(ctx,'Three different combinations have been compared and their causes remain visible.');
    }});
    host.appendChild(el('div',{class:'avl-model-grid'},stage,el('div',{class:'avl-controls'},tool,pressure,direction,run,el('p',{class:'avl-caveat',text:'The model predicts mark character. Physical samples remain the evidence for the pupil portfolio.'}))));
  }

  function resolveSVG(issue, action, after) {
    var base='<g><rect x="70" y="78" width="235" height="220" rx="8" fill="#e8dfd2" stroke="#334155" stroke-width="4"/><path d="M90 245 C140 130 190 270 285 110" fill="none" stroke="#356f83" stroke-width="22"/><circle cx="190" cy="178" r="52" fill="#d1673d" opacity=".82"/><g fill="#1c2b36"><rect x="105" y="105" width="42" height="42"/><rect x="240" y="222" width="32" height="32"/></g></g>';
    var afterGroup=base.replace(/x="70"/g,'x="375"').replace(/x="90"/g,'x="395"').replace(/x="190"/g,'x="495"').replace(/x="285"/g,'x="590"').replace(/x="105"/g,'x="410"').replace(/x="240"/g,'x="545"');
    if(after){
      if(action==='remove') afterGroup=afterGroup.replace('<circle cx="495" cy="178" r="52" fill="#d1673d" opacity=".82"/>','<circle cx="495" cy="178" r="28" fill="#d1673d" opacity=".72"/>');
      if(action==='strengthen') afterGroup=afterGroup.replace('stroke="#356f83" stroke-width="22"','stroke="#356f83" stroke-width="32"');
      if(action==='simplify') afterGroup=afterGroup.replace('<g fill="#1c2b36"><rect x="410" y="105" width="42" height="42"/><rect x="545" y="222" width="32" height="32"/></g>','<g fill="#1c2b36"><rect x="440" y="118" width="50" height="50"/></g>');
      if(action==='stop') afterGroup += '<path d="M392 282 H590" stroke="#238c80" stroke-width="7"/><text x="491" y="276" text-anchor="middle" font-family="Segoe UI,Arial" font-size="14" font-weight="900" fill="#238c80">DELIBERATE STOP</text>';
    }
    return artBase('Resolve artwork comparison','A protected before state sits beside a tested after state.','<text x="187" y="58" text-anchor="middle" font-family="Segoe UI,Arial" font-weight="900">BEFORE · protected</text><text x="493" y="58" text-anchor="middle" font-family="Segoe UI,Arial" font-weight="900">AFTER · '+(after?action.toUpperCase():'not tested')+'</text>'+base+afterGroup+'<text x="340" y="330" text-anchor="middle" font-family="Segoe UI,Arial" font-size="13" fill="#334155">ISSUE: '+issue.replace('_',' ').toUpperCase()+'</text>');
  }

  function renderResolve(ctx,host){
    var issue=controlSelect('Visible issue',[{value:'muddy',label:'Layers feel muddy'},{value:'weak_focal',label:'Focal point is weak'},{value:'crowded',label:'Composition feels crowded'},{value:'edge',label:'One edge feels unfinished'}],'muddy');
    var action=controlSelect('Test one response',[{value:'remove',label:'Remove or reduce'},{value:'strengthen',label:'Strengthen one feature'},{value:'simplify',label:'Simplify the composition'},{value:'stop',label:'Make a deliberate stop'}],'remove');
    var is=issue.querySelector('select'),as=action.querySelector('select'),stage=el('div',{class:'avl-stage'}),tried={};
    function draw(after){drawStage(stage,resolveSVG(is.value,as.value,after),'Before and after resolution test');}
    [is,as].forEach(function(s){s.addEventListener('change',function(){draw(false);});}); draw(false);
    var test=el('button',{type:'button',text:'Test and freeze',onclick:function(){draw(true);tried[is.value+'|'+as.value]=true;announce(ctx,'The before state is still visible. Decide KEEP, REVISE or REJECT from the comparison.','good');if(Object.keys(tried).length>=3)complete(ctx,'Three controlled resolution choices have been compared without erasing the original.');}});
    host.appendChild(el('div',{class:'avl-model-grid'},stage,el('div',{class:'avl-controls'},issue,action,test,el('p',{class:'avl-caveat',text:'The model rehearses decision-making. It does not tell the maker which artistic choice is correct.'}))));
  }

  function curationSVG(spacing,eye,route,running){
    var gap={tight:18,even:42,generous:74}[spacing],start=125-(gap-18),eyeY={low:225,eye:170,high:118}[eye];
    var xs=[start,start+150+gap,start+300+gap*2];
    var works=xs.map(function(x,i){return '<g><rect x="'+x+'" y="95" width="120" height="145" fill="'+['#356f83','#d1673d','#2ba193'][i]+'" stroke="#1c2b36" stroke-width="4"/><path d="M'+(x+15)+' '+(210-i*18)+' L'+(x+60)+' '+(112+i*20)+' L'+(x+105)+' '+(205-i*8)+'" fill="none" stroke="#f8f5ee" stroke-width="12"/><rect x="'+(x+18)+'" y="252" width="84" height="26" fill="#fff" stroke="#334155" stroke-width="2"/></g>';}).join('');
    var blocked=route==='blocked';
    return artBase('Curation wall and visitor route','Three works, eye line, labels and an access route change with the controls.','<rect x="40" y="60" width="600" height="245" fill="#fff" stroke="#334155" stroke-width="4"/>'+works+'<path d="M55 '+eyeY+' H625" stroke="#dfad3e" stroke-width="4" stroke-dasharray="12 8"/><text x="58" y="'+(eyeY-8)+'" font-family="Segoe UI,Arial" font-size="12" font-weight="900" fill="#7c5a10">EYE LINE</text>'+(blocked?'<rect x="320" y="282" width="110" height="42" rx="8" fill="#9b5b3d"/><text x="375" y="307" text-anchor="middle" fill="#fff" font-family="Segoe UI,Arial" font-size="12" font-weight="900">BLOCKED</text>':'<path class="avl-route '+(running?'is-running':'')+'" d="M62 320 C180 286 280 336 390 309 C490 286 560 320 625 300" fill="none" stroke="#238c80" stroke-width="8" stroke-dasharray="12 8"/><path d="M611 287 l18 12 l-17 15" fill="#238c80"/>')+'<text x="340" y="347" text-anchor="middle" font-family="Segoe UI,Arial" font-size="13" fill="#334155">'+spacing.toUpperCase()+' SPACING · '+eye.toUpperCase()+' SIGHTLINE · '+route.toUpperCase()+' ROUTE</text>');
  }

  function renderCuration(ctx,host){
    var spacing=controlSelect('Spacing',['tight','even','generous'],'tight'),eye=controlSelect('Eye line',[{value:'low',label:'Low'},{value:'eye',label:'Mixed eye line'},{value:'high',label:'High'}],'eye'),route=controlSelect('Visitor route',[{value:'blocked',label:'Blocked by furniture'},{value:'clear',label:'Clear alternative route'}],'blocked');
    var ss=spacing.querySelector('select'),es=eye.querySelector('select'),rs=route.querySelector('select'),stage=el('div',{class:'avl-stage'}),tested={};
    function draw(run){drawStage(stage,curationSVG(ss.value,es.value,rs.value,run),'Curation wall and visitor route');}
    [ss,es,rs].forEach(function(s){s.addEventListener('change',function(){draw(false);});});draw(false);
    var run=el('button',{type:'button',text:'Run visitor trace',onclick:function(){draw(!ctx.isStatic());tested[ss.value+'|'+es.value+'|'+rs.value]=true;announce(ctx,rs.value==='clear'?'The route reaches every work. Now judge spacing, label position and sequence.':'The route is interrupted. Change the layout rather than expecting the visitor to adapt.','notice');if(Object.keys(tested).length>=3&&rs.value==='clear')complete(ctx,'Several layouts have been compared and a clear route has been tested.');}});
    host.appendChild(el('div',{class:'avl-model-grid'},stage,el('div',{class:'avl-controls'},spacing,eye,route,run)));
  }

  function rubbingSVG(surface,pressure,direction,running){
    var detail={deep:8,fine:3,soft:5}[surface],p={light:2,medium:5,firm:9}[pressure],quality=(surface==='fine'&&pressure==='firm')?'muddy':(surface==='deep'&&pressure==='light')?'faint':(surface==='soft'&&pressure==='firm')?'flattened':'clear';
    var pattern='';for(var i=0;i<18;i++){var x=220+i*20; if(direction==='cross')pattern+='<path class="avl-rub '+(running?'is-running':'')+'" d="M'+x+' 110 l-40 170 M'+(x-35)+' 110 l75 170"/>';else pattern+='<path class="avl-rub '+(running?'is-running':'')+'" d="M'+x+' 105 L'+(x+(direction==='diagonal'?50:0))+' 282"/>';}
    return artBase('Frottage pressure and direction model','A textured surface sits under paper and a finite rubbing reveals its relief.','<g transform="translate(56 86)"><rect width="105" height="205" rx="12" fill="#d6cab8" stroke="#334155" stroke-width="4"/><g fill="#765f4b">'+Array.from({length:8},function(_,i){return '<rect x="'+(12+(i%2)*43)+'" y="'+(15+i*22)+'" width="34" height="'+detail+'" rx="3"/>';}).join('')+'</g><text x="52" y="190" text-anchor="middle" font-family="Segoe UI,Arial" font-size="12" font-weight="900">'+surface.toUpperCase()+'</text></g><rect x="190" y="75" width="420" height="230" rx="12" fill="#fff" fill-opacity=".88" stroke="#334155" stroke-width="4"/><g fill="none" stroke="#465f70" stroke-width="'+p+'" opacity="'+(quality==='muddy'?'.94':quality==='faint'?'.35':'.72')+'">'+pattern+'</g><text x="400" y="330" text-anchor="middle" font-family="Segoe UI,Arial" font-weight="900" fill="'+(quality==='clear'?'#238c80':'#9b5b3d')+'">RESULT: '+quality.toUpperCase()+'</text>');
  }

  function renderRubbing(ctx,host){
    var surface=controlSelect('Surface relief',[{value:'deep',label:'Deep relief'},{value:'fine',label:'Fine detail'},{value:'soft',label:'Soft grain'}],'deep'),pressure=controlSelect('Pressure',['light','medium','firm'],'light'),direction=controlSelect('Direction',[{value:'one',label:'One direction'},{value:'diagonal',label:'Diagonal'},{value:'cross',label:'Crossed'}],'one');
    var sels=[surface,pressure,direction].map(function(c){return c.querySelector('select');}),stage=el('div',{class:'avl-stage'}),trials={};
    function draw(run){drawStage(stage,rubbingSVG(sels[0].value,sels[1].value,sels[2].value,run),'Frottage control model');}sels.forEach(function(s){s.addEventListener('change',function(){draw(false);});});draw(false);
    var run=el('button',{type:'button',text:'Rub once and freeze',onclick:function(){draw(!ctx.isStatic());trials[sels.map(function(s){return s.value;}).join('|')]=true;announce(ctx,'Compare the revealed detail, not how hard the control was pushed.','good');if(Object.keys(trials).length>=3)complete(ctx,'Three surface-pressure-direction combinations have been compared.');}});
    host.appendChild(el('div',{class:'avl-model-grid'},stage,el('div',{class:'avl-controls'},surface,pressure,direction,run)));
  }

  function stencilSVG(bridge,tape,motion,running){
    var safe=bridge!=='none'&&tape==='yes'&&motion==='vertical';
    var island=bridge==='none'?'<circle cx="350" cy="170" r="42" fill="#f8f5ee" stroke="#334155" stroke-width="4" stroke-dasharray="8 6"/>':'<circle cx="350" cy="170" r="42" fill="#f8f5ee" stroke="#334155" stroke-width="4"/><rect x="345" y="102" width="10" height="30" fill="#f8f5ee" stroke="#334155" stroke-width="3"/>'+(bridge==='two'?'<rect x="345" y="208" width="10" height="30" fill="#f8f5ee" stroke="#334155" stroke-width="3"/>':'');
    var result=safe?'crisp':bridge==='none'?'island drops':motion==='sideways'?'dragged edge':'colour creeps';
    return artBase('Stencil bridge and edge model','A hand-cut stencil, island, bridges, tape and dab direction create a frozen result.','<rect x="170" y="62" width="360" height="225" rx="14" fill="#e5d5bd" stroke="#334155" stroke-width="5"/><path d="M250 245 L350 90 L450 245Z" fill="#d1673d" opacity=".88"/>'+island+(tape==='yes'?'<g fill="#dfad3e"><rect x="145" y="72" width="70" height="22" transform="rotate(-12 145 72)"/><rect x="475" y="72" width="70" height="22" transform="rotate(12 475 72)"/></g>':'')+'<g class="avl-dab '+(running?'is-running':'')+'"><circle cx="570" cy="130" r="32" fill="#2ba193" opacity=".85"/><path d="M570 165 V230" stroke="#2ba193" stroke-width="8"/>'+(motion==='vertical'?'<path d="M558 216 l12 17 l12 -17" fill="#2ba193"/>':'<path d="M548 213 H615" stroke="#2ba193" stroke-width="8"/><path d="M600 200 l18 13 l-18 13" fill="#2ba193"/>')+'</g><text x="350" y="326" text-anchor="middle" font-family="Segoe UI,Arial" font-weight="900" fill="'+(safe?'#238c80':'#9b5b3d')+'">'+result.toUpperCase()+'</text>');
  }

  function renderStencil(ctx,host){
    var bridge=controlSelect('Bridge',[{value:'none',label:'No bridge'},{value:'one',label:'One bridge'},{value:'two',label:'Two bridges'}],'none'),tape=controlSelect('Secure edges',[{value:'no',label:'Not secured'},{value:'yes',label:'Tape points used'}],'no'),motion=controlSelect('Application movement',[{value:'sideways',label:'Sideways wipe'},{value:'vertical',label:'Vertical dab and lift'}],'sideways');
    var bs=bridge.querySelector('select'),ts=tape.querySelector('select'),ms=motion.querySelector('select'),stage=el('div',{class:'avl-stage'}),tests={};function draw(run){drawStage(stage,stencilSVG(bs.value,ts.value,ms.value,run),'Stencil bridge and edge test');}[bs,ts,ms].forEach(function(s){s.addEventListener('change',function(){draw(false);});});draw(false);
    var run=el('button',{type:'button',text:'Dab, lift and freeze',onclick:function(){draw(!ctx.isStatic());tests[bs.value+'|'+ts.value+'|'+ms.value]=true;var ok=bs.value!=='none'&&ts.value==='yes'&&ms.value==='vertical';announce(ctx,ok?'The island stays attached and the edge remains controlled.':'The frozen result shows a cause to change. Alter one control and retest.',ok?'good':'notice');if(ok&&Object.keys(tests).length>=3)complete(ctx,'A stable bridge and controlled edge have been found after comparison.');}});
    host.appendChild(el('div',{class:'avl-model-grid'},stage,el('div',{class:'avl-controls'},bridge,tape,motion,run)));
  }

  function layersSVG(order,dry,alignment,running){
    var offsets=alignment==='aligned'?[0,0,0]:[0,18,-14], colours={rust:'#d1673d',steel:'#356f83',teal:'#2ba193'}, names=order.split('-');
    var shapes=names.map(function(n,i){var x=255+offsets[i],y=95+i*22,shape=n==='rust'?'<circle cx="'+(x+85)+'" cy="'+(y+70)+'" r="68"/>':n==='steel'?'<path d="M'+x+' '+(y+140)+' L'+(x+85)+' '+y+' L'+(x+170)+' '+(y+140)+'Z"/>':'<rect x="'+x+'" y="'+y+'" width="170" height="135" rx="20"/>';return '<g class="avl-layer '+(running?'is-running':'')+'" style="--avl-delay:'+(i*.18)+'s" fill="'+colours[n]+'" opacity=".67">'+shape+'</g>';}).join('');
    var result=dry==='yes'?(alignment==='aligned'?'registered layers':'intentional offset'):'muddy overlap';
    return artBase('Layer order and registration model','Three transparent layers assemble in order over registration marks.','<g stroke="#334155" stroke-width="3"><path d="M210 75 h24 M222 63 v24"/><path d="M470 285 h24 M482 273 v24"/></g>'+shapes+(dry==='no'?'<rect x="245" y="90" width="210" height="190" fill="#5c4a4a" opacity=".28"/>':'')+'<text x="340" y="327" text-anchor="middle" font-family="Segoe UI,Arial" font-weight="900" fill="'+(dry==='yes'?'#238c80':'#9b5b3d')+'">'+result.toUpperCase()+'</text>');
  }

  function renderLayers(ctx,host){
    var order=controlSelect('Layer order',[{value:'rust-steel-teal',label:'Rust → steel → teal'},{value:'steel-teal-rust',label:'Steel → teal → rust'},{value:'teal-rust-steel',label:'Teal → rust → steel'}],'rust-steel-teal'),dry=controlSelect('Between layers',[{value:'no',label:'Continue while wet'},{value:'yes',label:'Allow to dry'}],'no'),alignment=controlSelect('Registration',[{value:'aligned',label:'Registration marks aligned'},{value:'offset',label:'Deliberately offset'}],'aligned');
    var os=order.querySelector('select'),ds=dry.querySelector('select'),as=alignment.querySelector('select'),stage=el('div',{class:'avl-stage'}),tried={};function draw(run){drawStage(stage,layersSVG(os.value,ds.value,as.value,run),'Layer order and registration model');}[os,ds,as].forEach(function(s){s.addEventListener('change',function(){draw(false);});});draw(false);
    var run=el('button',{type:'button',text:'Build three layers',onclick:function(){draw(!ctx.isStatic());tried[os.value+'|'+ds.value+'|'+as.value]=true;announce(ctx,ds.value==='yes'?'The layer edges remain readable. Compare order and registration.':'Wet overlap has reduced edge clarity; alter one cause and retest.','notice');if(Object.keys(tried).length>=3&&ds.value==='yes')complete(ctx,'Several layer orders have been compared with drying and registration made visible.');}});
    host.appendChild(el('div',{class:'avl-model-grid'},stage,el('div',{class:'avl-controls'},order,dry,alignment,run)));
  }

  function editionSVG(load,align,dabs,running){
    var consistent=load==='same'&&align==='aligned'&&dabs==='one';var panels='';for(var i=0;i<5;i++){var variance=consistent?(i%2)*2:(load==='varied'?i*5:0)+(align==='shifted'?(i-2)*6:0)+(dabs==='two'?i*2:0);var opacity=load==='varied'?.55+i*.08:.82;panels+='<g class="avl-edition '+(running?'is-running':'')+'" style="--avl-delay:'+(i*.1)+'s"><rect x="'+(55+i*122)+'" y="100" width="102" height="150" rx="8" fill="#fff" stroke="#334155" stroke-width="3"/><path d="M'+(70+i*122+variance)+' 220 L'+(106+i*122+variance)+' 125 L'+(142+i*122+variance)+' 220Z" fill="#356f83" opacity="'+opacity+'"/><circle cx="'+(106+i*122+variance)+'" cy="177" r="20" fill="#d1673d" opacity="'+opacity+'"/><text x="'+(106+i*122)+'" y="275" text-anchor="middle" font-family="Segoe UI,Arial" font-size="13" font-weight="900">'+(i+1)+'</text></g>';}
    return artBase('Edition consistency model','Five handmade results show controlled process and honest variation.',panels+'<text x="340" y="322" text-anchor="middle" font-family="Segoe UI,Arial" font-weight="900" fill="'+(consistent?'#238c80':'#9b5b3d')+'">'+(consistent?'CONTROLLED PROCESS · SMALL HANDMADE VARIATION':'CAUSE OF VARIATION NEEDS IDENTIFYING')+'</text>');
  }

  function renderEdition(ctx,host){
    var load=controlSelect('Material loading',[{value:'varied',label:'Different each time'},{value:'same',label:'Same measured loading'}],'varied'),align=controlSelect('Placement',[{value:'shifted',label:'Unmarked placement'},{value:'aligned',label:'Registration marks'}],'shifted'),dabs=controlSelect('Passes',[{value:'two',label:'Two extra passes'},{value:'one',label:'One controlled pass'}],'two');
    var ls=load.querySelector('select'),as=align.querySelector('select'),ds=dabs.querySelector('select'),stage=el('div',{class:'avl-stage'}),tests={};function draw(run){drawStage(stage,editionSVG(ls.value,as.value,ds.value,run),'Five-result edition model');}[ls,as,ds].forEach(function(s){s.addEventListener('change',function(){draw(false);});});draw(false);
    var run=el('button',{type:'button',text:'Make five samples',onclick:function(){draw(!ctx.isStatic());tests[ls.value+'|'+as.value+'|'+ds.value]=true;var ok=ls.value==='same'&&as.value==='aligned'&&ds.value==='one';announce(ctx,ok?'The repeatable causes are controlled; small handmade differences remain honest.':'Name which process choice caused the largest variation, then alter only that cause.','notice');if(ok&&Object.keys(tests).length>=2)complete(ctx,'A controlled five-sample edition has been compared with an uncontrolled version.');}});
    host.appendChild(el('div',{class:'avl-model-grid'},stage,el('div',{class:'avl-controls'},load,align,dabs,run)));
  }

  function processControlSVG(wet,tape,dabs,result,running){
    var creep=result==='creep',soft=result==='soft';return artBase('Stencil process-control model','Moisture, securing and dab count create a frozen edge result.','<rect x="125" y="82" width="400" height="210" rx="14" fill="#efe3d0" stroke="#334155" stroke-width="4"/><path d="M230 245 L325 105 L420 245Z" fill="#d1673d" opacity="'+(creep?'.54':'.84')+'" '+(soft?'stroke="#f0a184" stroke-width="12" stroke-linejoin="round"':'')+'/>'+(creep?'<path d="M205 250 C250 270 390 270 445 245" fill="#d1673d" opacity=".45"/>':'')+(tape==='yes'?'<g fill="#dfad3e"><rect x="105" y="75" width="70" height="22" transform="rotate(-10 105 75)"/><rect x="480" y="75" width="70" height="22" transform="rotate(10 480 75)"/></g>':'')+'<g class="avl-dab '+(running?'is-running':'')+'" transform="translate(560 122)"><circle r="30" fill="#2ba193"/><text y="5" text-anchor="middle" font-family="Segoe UI,Arial" font-size="12" fill="#fff" font-weight="900">'+dabs+'×</text></g><g transform="translate(44 110)"><text font-family="Segoe UI,Arial" font-size="13" font-weight="900" fill="#334155">MOISTURE</text><text y="24" font-family="Segoe UI,Arial" font-size="20" font-weight="900" fill="#356f83">'+wet.toUpperCase()+'</text></g><text x="340" y="327" text-anchor="middle" font-family="Segoe UI,Arial" font-weight="900" fill="'+(result==='crisp'?'#238c80':'#9b5b3d')+'">'+result.toUpperCase()+' EDGE</text>');
  }

  function renderProcessControl(ctx,host){
    var wet=controlSelect('Sponge moisture',[{value:'dry',label:'Almost dry'},{value:'damp',label:'Damp'},{value:'wet',label:'Wet'}],'damp'),tape=controlSelect('Stencil securing',[{value:'yes',label:'Edges secured'},{value:'no',label:'Not secured'}],'yes'),dabs=controlSelect('Dab count',[{value:'1',label:'One pass'},{value:'3',label:'Three passes'},{value:'6',label:'Six passes'}],'1');
    var ws=wet.querySelector('select'),ts=tape.querySelector('select'),ds=dabs.querySelector('select'),stage=el('div',{class:'avl-stage'}),table=trialTable(['Changed variable','Fixed controls','Frozen edge']),trials={};
    function result(){if(ws.value==='wet'||ts.value==='no')return 'creep';if(ds.value==='6')return 'soft';return 'crisp';}
    function draw(run){drawStage(stage,processControlSVG(ws.value,ts.value,ds.value,result(),run),'Stencil process control model');}[ws,ts,ds].forEach(function(s){s.addEventListener('change',function(){clearPrediction(ctx);draw(false);announce(ctx,'Control changed. Commit a prediction before the next test.','notice');});});draw(false);
    var last={wet:ws.value,tape:ts.value,dabs:ds.value};
    var run=el('button',{type:'button',text:'Run one controlled trial',onclick:function(){if(!canRun(ctx))return;var current={wet:ws.value,tape:ts.value,dabs:ds.value},changed=Object.keys(current).filter(function(k){return current[k]!==last[k];});if(Object.keys(trials).length&&changed.length!==1){announce(ctx,'Change exactly one control between trials. Restore the other controls, then test again.','bad');return;}var r=result(),pred=ctx.prediction.toLowerCase().indexOf(r==='creep'?'creep':r)!==-1;draw(!ctx.isStatic());addTrial(table,[changed[0]||'baseline',(changed[0]!=='wet'?'moisture '+ws.value:'')+' '+(changed[0]!=='tape'?'securing '+ts.value:'')+' '+(changed[0]!=='dabs'?'dabs '+ds.value:''),r]);trials[JSON.stringify(current)]=true;last=current;announce(ctx,(pred?'Prediction supported. ':'Prediction revised. ')+r+' edge frozen and recorded.',pred?'good':'notice');clearPrediction(ctx);if(Object.keys(trials).length>=3)complete(ctx,'Three one-variable stencil trials have been recorded.');}});
    host.appendChild(el('div',{class:'avl-model-grid'},stage,el('div',{class:'avl-controls'},wet,tape,dabs,run,table)));
  }

  function challengeScopeSVG(spec,demand,sessions,history){
    var score={low:1,medium:2,high:3}[spec]+{low:1,medium:2,high:3}[demand]+{one:1,two:2,four:3}[sessions];var result=score<=4?'too small':score>=8?'too broad':'productive stretch';
    var historySvg=(history||[]).slice(-3).map(function(h,i){return '<g transform="translate('+(70+i*180)+' 275)"><rect width="155" height="38" rx="9" fill="'+(h.result==='productive stretch'?'#dff4ed':'#f8e7de')+'" stroke="#334155" stroke-width="2"/><text x="77" y="16" text-anchor="middle" font-family="Segoe UI,Arial" font-size="11" font-weight="900">'+h.result.toUpperCase()+'</text><text x="77" y="30" text-anchor="middle" font-family="Segoe UI,Arial" font-size="10">'+h.label+'</text></g>';}).join('');
    return artBase('Challenge scope tester','Specificity, personal demand and available sessions create a visible scope judgement.','<g transform="translate(70 75)"><text font-family="Segoe UI,Arial" font-size="14" font-weight="900">SPECIFICITY</text><rect y="22" width="150" height="24" rx="12" fill="#d8dee2"/><rect y="22" width="'+({low:50,medium:100,high:150}[spec])+'" height="24" rx="12" fill="#356f83"/></g><g transform="translate(265 75)"><text font-family="Segoe UI,Arial" font-size="14" font-weight="900">DEMAND</text><rect y="22" width="150" height="24" rx="12" fill="#d8dee2"/><rect y="22" width="'+({low:50,medium:100,high:150}[demand])+'" height="24" rx="12" fill="#d1673d"/></g><g transform="translate(460 75)"><text font-family="Segoe UI,Arial" font-size="14" font-weight="900">CONDITIONS</text><rect y="22" width="150" height="24" rx="12" fill="#d8dee2"/><rect y="22" width="'+({one:50,two:100,four:150}[sessions])+'" height="24" rx="12" fill="#2ba193"/></g><path d="M100 185 H580" stroke="#334155" stroke-width="6"/><circle cx="'+(100+(score-3)/6*480)+'" cy="185" r="22" fill="#dfad3e" stroke="#334155" stroke-width="4"/><g font-family="Segoe UI,Arial" font-size="12" font-weight="900"><text x="110" y="220">TOO SMALL</text><text x="305" y="220">PRODUCTIVE</text><text x="515" y="220">TOO BROAD</text></g><text x="340" y="255" text-anchor="middle" font-family="Segoe UI,Arial" font-size="19" font-weight="900" fill="'+(result==='productive stretch'?'#238c80':'#9b5b3d')+'">'+result.toUpperCase()+'</text>'+historySvg);}

  function renderChallengeScope(ctx,host){
    var spec=controlSelect('Specificity',[{value:'low',label:'Vague outcome'},{value:'medium',label:'Named outcome'},{value:'high',label:'Named outcome and checks'}],'low'),demand=controlSelect('Demand from baseline',[{value:'low',label:'Mostly familiar'},{value:'medium',label:'One genuine stretch'},{value:'high',label:'Several new demands'}],'medium'),sessions=controlSelect('Available conditions',[{value:'one',label:'One session'},{value:'two',label:'Two sessions'},{value:'four',label:'Four sessions'}],'two');
    var ss=spec.querySelector('select'),ds=demand.querySelector('select'),ts=sessions.querySelector('select'),stage=el('div',{class:'avl-stage'}),history=[];function getResult(){var score={low:1,medium:2,high:3}[ss.value]+{low:1,medium:2,high:3}[ds.value]+{one:1,two:2,four:3}[ts.value];return score<=4?'too small':score>=8?'too broad':'productive stretch';}function draw(){drawStage(stage,challengeScopeSVG(ss.value,ds.value,ts.value,history),'Challenge scope gauge');}[ss,ds,ts].forEach(function(s){s.addEventListener('change',function(){clearPrediction(ctx);draw();});});draw();
    var test=el('button',{type:'button',text:'Test this version',onclick:function(){if(!canRun(ctx))return;var r=getResult();history.push({result:r,label:ss.value+'/'+ds.value+'/'+ts.value});draw();var predicted=ctx.prediction.toLowerCase().indexOf(r==='productive stretch'?'productive':r.replace('too ',''))!==-1;announce(ctx,(predicted?'Prediction supported. ':'Prediction revised. ')+r+'. Keep this version visible and redraft one condition.',predicted?'good':'notice');clearPrediction(ctx);if(history.length>=3&&history.some(function(h){return h.result==='productive stretch';}))complete(ctx,'Failed and productive versions remain visible as a scope evidence trail.');}});
    host.appendChild(el('div',{class:'avl-model-grid'},stage,el('div',{class:'avl-controls'},spec,demand,sessions,test)));
  }

  function iterationSVG(evidence,change,version,running){
    var base='<rect x="65" y="95" width="150" height="170" rx="9" fill="#efe3d0" stroke="#334155" stroke-width="3"/><path d="M85 235 C120 105 170 245 198 115" fill="none" stroke="#356f83" stroke-width="16"/><circle cx="150" cy="180" r="35" fill="#d1673d" opacity=".8"/>';
    var v2=base.replace(/x="65"/g,'x="265"').replace(/x="85"/g,'x="285"').replace(/x="120"/g,'x="320"').replace(/x="170"/g,'x="370"').replace(/x="198"/g,'x="398"').replace(/cx="150"/g,'cx="350"');
    var v3=base.replace(/x="65"/g,'x="465"').replace(/x="85"/g,'x="485"').replace(/x="120"/g,'x="520"').replace(/x="170"/g,'x="570"').replace(/x="198"/g,'x="598"').replace(/cx="150"/g,'cx="550"');
    function apply(s,v){if(change==='contrast')return s.replace('fill="#d1673d" opacity=".8"','fill="#dfad3e" opacity="1"').replace('stroke-width="16"','stroke-width="24"');if(change==='space')return s.replace('r="35"','r="23"');if(change==='repeat')return s.replace('</g>','')+'<circle cx="'+(v===2?310:510)+'" cy="135" r="18" fill="#d1673d" opacity=".7"/>';return s;}
    if(version>=2)v2=apply(v2,2);if(version>=3)v3=apply(v3,3);
    return artBase('Iteration evidence trace','Three preserved versions connect evidence to one controlled change.','<g class="avl-version '+(running?'is-running':'')+'">'+base+'</g><g class="avl-version '+(running?'is-running':'')+'" style="--avl-delay:.16s">'+(version>=2?v2:'')+'</g><g class="avl-version '+(running?'is-running':'')+'" style="--avl-delay:.32s">'+(version>=3?v3:'')+'</g><g font-family="Segoe UI,Arial" font-size="13" font-weight="900"><text x="140" y="292">VERSION 1</text><text x="340" y="292">VERSION 2</text><text x="540" y="292">VERSION 3</text></g><path d="M220 180 H258 M420 180 H458" stroke="#238c80" stroke-width="7"/><path d="M245 168 l17 12 l-17 12 M445 168 l17 12 l-17 12" fill="#238c80"/><text x="340" y="326" text-anchor="middle" font-family="Segoe UI,Arial" font-size="13" fill="#334155">EVIDENCE: '+evidence.toUpperCase()+' · CONTROLLED CHANGE: '+change.toUpperCase()+'</text>');
  }

  function renderIteration(ctx,host){
    var evidence=controlSelect('Evidence driving change',[{value:'audience',label:'Audience missed the focal point'},{value:'test',label:'Material test lost edge clarity'},{value:'intent',label:'Version does not support the stated intention'}],'audience'),change=controlSelect('One controlled change',[{value:'contrast',label:'Increase contrast'},{value:'space',label:'Create more space'},{value:'repeat',label:'Repeat one motif'}],'contrast');
    var es=evidence.querySelector('select'),cs=change.querySelector('select'),stage=el('div',{class:'avl-stage'}),version=1,seen={};function draw(run){drawStage(stage,iterationSVG(es.value,cs.value,version,run),'Three-version iteration trace');}[es,cs].forEach(function(s){s.addEventListener('change',function(){version=1;draw(false);});});draw(false);
    var run=el('button',{type:'button',text:'Create next version',onclick:function(){version=Math.min(3,version+1);draw(!ctx.isStatic());seen[es.value+'|'+cs.value]=true;announce(ctx,'Version '+version+' keeps the previous state visible. Judge the change against the challenge evidence.','good');if(version===3&&Object.keys(seen).length>=1)complete(ctx,'Three versions now show evidence, decision and controlled change.');}});
    host.appendChild(el('div',{class:'avl-model-grid'},stage,el('div',{class:'avl-controls'},evidence,change,run)));
  }

  function projectCanvasSVG(aim,audience,consult,access,evidence,ok){
    var nodes=[['AIM',aim,95,90,'#356f83'],['PARTICIPANTS',audience,285,90,'#7659a7'],['CONSULT',consult,475,90,'#d1673d'],['ACCESS',access,170,225,'#238c80'],['EVIDENCE',evidence,400,225,'#dfad3e']];var svg=nodes.map(function(n){return '<g><rect x="'+n[2]+'" y="'+n[3]+'" width="150" height="72" rx="13" fill="'+n[4]+'" opacity=".9"/><text x="'+(n[2]+75)+'" y="'+(n[3]+23)+'" text-anchor="middle" font-family="Segoe UI,Arial" font-size="12" font-weight="900" fill="#fff">'+n[0]+'</text><text x="'+(n[2]+75)+'" y="'+(n[3]+48)+'" text-anchor="middle" font-family="Segoe UI,Arial" font-size="11" fill="#fff">'+n[1].toUpperCase()+'</text></g>';}).join('');
    return artBase('Leadership project dependency canvas','Aim, participants, consultation, access and evidence are joined by decision arrows.','<g stroke="#334155" stroke-width="5" fill="none"><path d="M245 126 H280"/><path d="M435 126 H470"/><path d="M540 165 C520 220 500 240 550 260"/><path d="M360 165 C330 205 300 225 320 260"/><path d="M320 260 H395"/></g>'+svg+'<text x="340" y="330" text-anchor="middle" font-family="Segoe UI,Arial" font-weight="900" fill="'+(ok?'#238c80':'#9b5b3d')+'">'+(ok?'CONSULTATION CHANGES THE PLAN':'DEPENDENCY GAP · REVISE ONE LINK')+'</text>');
  }

  function renderProjectCanvas(ctx,host){
    var aim=controlSelect('Aim',[{value:'share skill',label:'Share one accessible art skill'},{value:'make display',label:'Co-create a public display'}],'share skill'),aud=controlSelect('Participants',[{value:'small group',label:'Small invited group'},{value:'mixed needs',label:'Mixed-needs group'}],'small group'),consult=controlSelect('Consultation finding',[{value:'needs visual steps',label:'Needs visual step cards'},{value:'needs choice',label:'Needs two participation routes'},{value:'no consultation',label:'No participant evidence yet'}],'no consultation'),access=controlSelect('Plan response',[{value:'visual steps',label:'Visual steps and demonstration'},{value:'two routes',label:'Hands-on or observation route'},{value:'unchanged',label:'Plan unchanged'}],'unchanged'),evidence=controlSelect('Evidence route',[{value:'plan plus witness',label:'Plan + consented/witness evidence + reflection'},{value:'final photo only',label:'Final outcome photograph only'}],'final photo only');
    var sels=[aim,aud,consult,access,evidence].map(function(c){return c.querySelector('select');}),stage=el('div',{class:'avl-stage'});function ok(){return sels[2].value!=='no consultation'&&sels[3].value!=='unchanged'&&sels[4].value==='plan plus witness';}function draw(){drawStage(stage,projectCanvasSVG(sels[0].value,sels[1].value,sels[2].value,sels[3].value,sels[4].value,ok()),'Leadership project dependency canvas');}sels.forEach(function(s){s.addEventListener('change',draw);});draw();
    var check=el('button',{type:'button',text:'Run dependency check',onclick:function(){draw();if(ok()){complete(ctx,'The consultation evidence changes an access or delivery decision and the evidence route covers planning, action and reflection.');}else announce(ctx,'A project box is filled, but the links do not yet prove that participant evidence changed the plan.','bad');}});
    host.appendChild(el('div',{class:'avl-model-grid'},stage,el('div',{class:'avl-controls'},aim,aud,consult,access,evidence,check)));
  }

  function pilotSVG(adapt,runNo,result,running){
    var baseBars='<rect x="115" y="230" width="80" height="'+(runNo===1?70:result.participation)+'" fill="#356f83"/><rect x="255" y="230" width="80" height="'+(runNo===1?110:result.timing)+'" fill="#d1673d"/><rect x="395" y="230" width="80" height="'+(runNo===1?90:result.access)+'" fill="#2ba193"/>';
    return artBase('Pilot baseline and adaptation dashboard','A baseline and second run compare participation, timing and access after one adaptation.','<g class="avl-bars '+(running?'is-running':'')+'" transform="translate(0 -1)">'+baseBars+'</g><path d="M80 230 H520" stroke="#334155" stroke-width="4"/><g font-family="Segoe UI,Arial" font-size="12" font-weight="900"><text x="155" y="322">PARTICIPATION</text><text x="295" y="322">TIMING</text><text x="435" y="322">ACCESS</text></g><rect x="535" y="90" width="110" height="145" rx="12" fill="#fff" stroke="#334155" stroke-width="3"/><text x="590" y="118" text-anchor="middle" font-family="Segoe UI,Arial" font-size="12" font-weight="900">RUN '+runNo+'</text><text x="590" y="155" text-anchor="middle" font-family="Segoe UI,Arial" font-size="11">ADAPT</text><text x="590" y="179" text-anchor="middle" font-family="Segoe UI,Arial" font-size="11" font-weight="900">'+adapt.toUpperCase()+'</text><text x="590" y="212" text-anchor="middle" font-family="Segoe UI,Arial" font-size="10">other conditions fixed</text>');
  }

  function renderPilot(ctx,host){
    var adapt=controlSelect('One adaptation',[{value:'visual cue',label:'Add one visual cue'},{value:'shorter step',label:'Shorten one instruction'},{value:'choice route',label:'Add an alternative participation route'}],'visual cue'),as=adapt.querySelector('select'),stage=el('div',{class:'avl-stage'}),table=trialTable(['Run','Adaptation','Participation','Timing','Access']),runNo=0;
    function values(){if(as.value==='visual cue')return{participation:95,timing:88,access:82};if(as.value==='shorter step')return{participation:82,timing:65,access:78};return{participation:105,timing:96,access:55};}function draw(run){drawStage(stage,pilotSVG(as.value,Math.max(1,runNo),values(),run),'Pilot dashboard');}as.addEventListener('change',function(){clearPrediction(ctx);if(runNo>0)announce(ctx,'Adaptation changed. Keep the baseline fixed and commit a prediction before run 2.','notice');draw(false);});draw(false);
    var run=el('button',{type:'button',text:'Run baseline / second run',onclick:function(){if(!canRun(ctx))return;runNo+=1;if(runNo===1){draw(!ctx.isStatic());addTrial(table,['1','baseline','medium','slow','barrier noted']);announce(ctx,'Baseline frozen. Choose one adaptation, keep other conditions fixed and predict run 2.','notice');clearPrediction(ctx);return;}var v=values();draw(!ctx.isStatic());addTrial(table,['2',as.value,v.participation>90?'clearer':'mixed',v.timing<80?'improved':'similar',v.access<70?'barrier reduced':'barrier remains']);announce(ctx,'Second run frozen. Compare it with the baseline and record the single adaptation.','good');complete(ctx,'Baseline and adapted run are now linked by one documented change.');run.disabled=true;}});
    host.appendChild(el('div',{class:'avl-model-grid'},stage,el('div',{class:'avl-controls'},adapt,run,table)));
  }

  function deliverySVG(roles,access,disruption,running){
    var stations=[['WELCOME',70],['MAKE',190],['CHECK',310],['CURATE',430],['SHARE',550]],svg='';stations.forEach(function(s,i){svg+='<g><rect x="'+s[1]+'" y="130" width="88" height="70" rx="12" fill="'+['#356f83','#7659a7','#d1673d','#2ba193','#dfad3e'][i]+'"/><text x="'+(s[1]+44)+'" y="171" text-anchor="middle" font-family="Segoe UI,Arial" font-size="12" font-weight="900" fill="#fff">'+s[0]+'</text></g>';if(i<stations.length-1)svg+='<path d="M'+(s[1]+90)+' 165 H'+(stations[i+1][1]-4)+'" stroke="#334155" stroke-width="6"/><path d="M'+(stations[i+1][1]-16)+' 153 l17 12 l-17 12" fill="#334155"/>';});
    var breakX=disruption==='late'?150:disruption==='missing'?270:disruption==='noise'?390:510;
    return artBase('Live delivery participant flow','Welcome, making, check, curation and sharing stations show role, access and contingency decisions.','<g class="avl-flow '+(running?'is-running':'')+'">'+svg+'</g><path d="M80 255 H610" stroke="'+(access==='alternative'?'#238c80':'#9b5b3d')+'" stroke-width="8" stroke-dasharray="12 8"/><circle cx="'+breakX+'" cy="255" r="18" fill="#fff" stroke="#9b5b3d" stroke-width="6"/><text x="'+breakX+'" y="260" text-anchor="middle" font-family="Segoe UI,Arial" font-size="15" font-weight="900">!</text><g font-family="Segoe UI,Arial" font-size="12" font-weight="900"><text x="90" y="305">ROLES: '+roles.toUpperCase()+'</text><text x="300" y="305">ACCESS: '+access.toUpperCase()+'</text><text x="500" y="305">DISRUPTION: '+disruption.toUpperCase()+'</text></g>');
  }

  function renderDeliveryFlow(ctx,host){
    var roles=controlSelect('Role coverage',[{value:'one person',label:'One person holds every role'},{value:'assigned',label:'Welcome, materials, support and evidence assigned'}],'one person'),access=controlSelect('Participation route',[{value:'single',label:'Single compulsory route'},{value:'alternative',label:'Hands-on, observation or supported route'}],'single'),dis=controlSelect('Disruption',[{value:'late',label:'Participant arrives late'},{value:'missing',label:'A material is unavailable'},{value:'noise',label:'Sound level becomes a barrier'},{value:'timing',label:'One station overruns'}],'late');
    var rs=roles.querySelector('select'),as=access.querySelector('select'),ds=dis.querySelector('select'),stage=el('div',{class:'avl-stage'}),seen={};function draw(run){drawStage(stage,deliverySVG(rs.value,as.value,ds.value,run),'Live delivery participant flow');}[rs,as,ds].forEach(function(s){s.addEventListener('change',function(){draw(false);});});draw(false);
    var run=el('button',{type:'button',text:'Run and freeze disruption',onclick:function(){draw(!ctx.isStatic());seen[ds.value]=true;var ready=rs.value==='assigned'&&as.value==='alternative';announce(ctx,ready?'Roles and alternative routes allow the leader to respond without stopping the whole project.':'The disruption exposes a role or access gap. Change the plan and rerun.','notice');if(ready&&Object.keys(seen).length>=2)complete(ctx,'Two disruptions have been tested with roles, access and participant flow visible.');}});
    host.appendChild(el('div',{class:'avl-model-grid'},stage,el('div',{class:'avl-controls'},roles,access,dis,run)));
  }

  function renderModel(ctx, host) {
    var name = ctx.activity.model;
    if (name === 'surface_marks') return renderSurfaceMarks(ctx, host);
    if (name === 'resolve') return renderResolve(ctx, host);
    if (name === 'curation') return renderCuration(ctx, host);
    if (name === 'rubbing') return renderRubbing(ctx, host);
    if (name === 'stencil') return renderStencil(ctx, host);
    if (name === 'layers') return renderLayers(ctx, host);
    if (name === 'edition') return renderEdition(ctx, host);
    if (name === 'process_control') return renderProcessControl(ctx, host);
    if (name === 'challenge_scope') return renderChallengeScope(ctx, host);
    if (name === 'iteration') return renderIteration(ctx, host);
    if (name === 'project_canvas') return renderProjectCanvas(ctx, host);
    if (name === 'pilot') return renderPilot(ctx, host);
    if (name === 'delivery_flow') return renderDeliveryFlow(ctx, host);
    host.appendChild(el('p', { class: 'avl-live', text: 'Model not available: ' + name }));
  }

  function renderActivity(ctx, host) {
    switch (ctx.activity.type) {
      case 'sort': return renderSort(ctx, host);
      case 'sequence': return renderSequence(ctx, host);
      case 'evidence': return renderEvidence(ctx, host);
      case 'hotspot': return renderHotspot(ctx, host);
      case 'model': return renderModel(ctx, host);
      default: host.appendChild(el('p', { class: 'avl-live', text: 'Unknown activity type: ' + ctx.activity.type }));
    }
  }

  /* Clipboard capability: SHIPS DISABLED (ruled 2026-08-05).

     As recovered, this called navigator.clipboard.writeText, and fell back to
     document.execCommand('copy'). Both write to the pupil's clipboard — a
     device capability this estate has not previously taken, and one the
     science sibling did not have.

     Nothing here writes to any clipboard. The note is shown selected, and the
     pupil copies it themselves with their own keystroke if they want it. Do
     not reintroduce a programmatic clipboard write without a fresh ruling. */
  function showNoteForManualCopy(ctx, text) {
    var existing = ctx.panel.querySelector('.avl-copy-area');
    if (existing) existing.remove();
    var area = el('textarea', {
      class: 'avl-copy-area avl-evidence-input', value: text, readOnly: true, rows: 4,
      'aria-label': 'Evidence note, ready to select and copy'
    });
    ctx.panel.querySelector('.avl-toolbar').before(area);
    area.focus();
    area.setSelectionRange(0, text.length);
  }

  function buildPanel(slug, payload) {
    var panel = el('section', { class: 'avl-panel', dataset: { lesson: slug, pathway: payload.pathway }, 'aria-label': payload.title });
    var head = el('header', { class: 'avl-head' },
      el('h3', { class: 'avl-title', text: payload.title }),
      el('span', { class: 'avl-chip', text: payload.pathway + ' visual lab' }),
      el('p', { class: 'avl-purpose', text: payload.purpose })
    );
    var body = el('div', { class: 'avl-body' });
    var live = el('div', { class: 'avl-live', role: 'status', 'aria-live': 'polite', text: 'Ready. Use the prompt, make a decision and then manipulate the model or information.' });
    var ctx = {
      slug: slug, payload: payload, pathway: payload.pathway, activity: payload.activity || {}, panel: panel, body: body, live: live,
      prediction: '', predictionGroup: null, evidenceInput: null, explanation: null, completed: false,
      isStatic: function () { return reducedMotion || panel.classList.contains('avl-static'); }
    };
    body.appendChild(el('p', { class: 'avl-prompt' }, el('strong', { text: 'Together: ' }), document.createTextNode(ctx.activity.prompt || 'Use the visual evidence to solve the task.')));
    var prediction = predictionGate(ctx); if (prediction) body.appendChild(prediction);
    var activityHost = el('div', { class: 'avl-activity' }); body.appendChild(activityHost);
    renderActivity(ctx, activityHost);
    var evidence = evidenceGate(ctx); if (evidence) body.appendChild(evidence);
    body.appendChild(explanationNode(ctx));
    MOUNTED.push(ctx);
    watchStaffToggle();
    /* The transfer task is a teaching activity, not Arts Award evidence, and
       says so in plain words. The portfolio of record is the weekly evidence
       pack; the in-lesson print sections are working documents. This panel is
       not a third portfolio and must not become one by drift. */
    var independent = el('details', { class: 'avl-independent', style: { marginTop: '10px' } },
      el('summary', { text: 'Independent transfer task' }),
      el('p', { class: 'avl-small', text: payload.independent || 'Use the completed visual to produce an independent explanation.' }),
      el('p', { class: 'avl-small avl-not-evidence', text: 'This is a teaching activity, not Arts Award evidence. Nothing here goes in the portfolio — record evidence on the weekly evidence pack as usual.' })
    );
    body.appendChild(independent);
    body.appendChild(live);

    var staticButton = el('button', { type: 'button', class: 'avl-ghost', 'aria-pressed': 'false', text: 'Static diagrams: off', onclick: function () {
      var on = !panel.classList.contains('avl-static'); panel.classList.toggle('avl-static', on);
      staticButton.setAttribute('aria-pressed', String(on)); staticButton.textContent = 'Static diagrams: ' + (on ? 'on' : 'off');
      announce(ctx, on ? 'Static diagram mode is on. All essential information remains available.' : 'Finite motion is available again.', 'notice');
    } });
    var resetButton = el('button', { type: 'button', class: 'avl-neutral', text: 'Reset lab', onclick: function () {
      var fresh = buildPanel(slug, payload); panel.replaceWith(fresh); fresh.scrollIntoView({ block: 'nearest' });
    } });
    var copyButton = el('button', { type: 'button', class: 'avl-ghost', text: 'Show evidence note to copy', onclick: function () {
      var note = ctx.evidenceInput && ctx.evidenceInput.value.trim();
      var text = payload.title + '\n' + (note || 'No evidence note recorded yet.') + '\nIndependent transfer: ' + (payload.independent || '');
      showNoteForManualCopy(ctx, text);
      announce(ctx, 'The note is selected below. Copy it yourself if you want it — nothing has been copied for you.', 'notice');
    } });
    body.appendChild(el('div', { class: 'avl-toolbar' }, el('div', { class: 'avl-actions' }, resetButton, staticButton), copyButton));
    panel.append(head, body);
    return panel;
  }

  function mountBySlug(slug, target) {
    slug = normaliseSlug(slug);
    var payload = PAYLOADS[slug];
    if (!payload || !target) return null;
    if (target.querySelector && target.querySelector('.avl-panel[data-lesson="' + cssEscape(slug) + '"]')) return target.querySelector('.avl-panel[data-lesson="' + cssEscape(slug) + '"]');
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

  global.ArtVisualLearning = {
    version: '1.0.0',
    mountAll: mountAll,
    mountBySlug: mountBySlug,
    payloads: PAYLOADS
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mountAll, { once: true });
  else mountAll();
})(typeof window !== 'undefined' ? window : this);

