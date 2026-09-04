/* One current slot source. Embedded only in slot-dependent award decks. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.MBMArtsSlots = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  function readSlots(doc, required) {
    if (!doc || doc.schema !== 'arts-award-slots-v1' || !doc.slots || !Array.isArray(required)) {
      throw new Error('Choose the current Arts Award slots file.');
    }
    return required.map(function (key) {
      const slot = doc.slots[key];
      if (!slot || !Array.isArray(slot.entries)) throw new Error('A required slot is missing.');
      const entries = slot.entries.map(function (entry) {
        if (!entry || typeof entry !== 'object' || Array.isArray(entry)) throw new Error('Invalid slot entry.');
        const status = String(entry.status || 'UNCONFIRMED').toUpperCase();
        const confirmed = status === 'CONFIRMED' || status === 'BOOKED';
        const name = String(entry.name || entry.title || '').trim();
        const route = String(entry.route || '').trim();
        return {name: name, route: route, date: String(entry.date || ''),
          confirmed: confirmed && Boolean(name) && ['R1', 'R2', 'R3'].includes(route)};
      });
      return {key: key, entries: entries, ready: entries.some(e => e.confirmed)};
    });
  }
  async function loadHosted(url, required, fetcher) {
    const response = await fetcher(url, {cache: 'no-store', credentials: 'same-origin'});
    if (!response.ok) throw new Error('Current slots could not be loaded.');
    return readSlots(await response.json(), required);
  }
  async function loadFile(file, required) {
    if (!file || file.size > 1048576) throw new Error('Choose a slots JSON file smaller than 1 MB.');
    return readSlots(JSON.parse(await file.text()), required);
  }
  function mount(config) {
    const host = document.querySelector('section[data-min]');
    if (!host || document.getElementById('award-slot-panel')) return;
    const panel = document.createElement('div');
    panel.id = 'award-slot-panel';
    panel.className = 'box rehearsal';
    panel.dataset.mbmGuide = 'staff';
    panel.dataset.audience = 'staff';
    const heading = document.createElement('h3');
    heading.textContent = 'Current session details';
    const status = document.createElement('p');
    status.setAttribute('role', 'status');
    const list = document.createElement('ul');
    const label = document.createElement('label');
    label.textContent = 'Open the current SLOTS.json file: ';
    const input = document.createElement('input');
    input.type = 'file'; input.accept = '.json,application/json';
    label.appendChild(input);
    panel.append(heading, status, list, label); host.appendChild(panel);
    let generation = 0;
    function fallback(message) {
      list.replaceChildren();
      status.textContent = 'Unconfirmed — preparation only. ' + message;
    }
    function show(rows) {
      list.replaceChildren();
      const allReady = rows.length > 0 && rows.every(row => row.ready);
      status.textContent = allReady
        ? 'A confirmed route is recorded. Staff must check arrangements before delivery.'
        : 'Unconfirmed — preparation only. Complete the actual experience when a route is ready.';
      rows.forEach(function (row) {
        const item = document.createElement('li');
        const ready = row.entries.filter(entry => entry.confirmed);
        item.textContent = row.key + ': ' + (ready.length
          ? ready.map(e => [e.name, e.route, e.date].filter(Boolean).join(' · ')).join('; ')
          : 'no confirmed entry');
        list.appendChild(item);
      });
    }
    input.addEventListener('change', async function () {
      const ticket = ++generation;
      fallback('Reading the selected file.');
      try { const rows = await loadFile(input.files[0], config.required); if (ticket === generation) show(rows); }
      catch (_) { if (ticket === generation) fallback('The selected file could not be read.'); }
    });
    fallback('Load the shared slots file to check the current route.');
    if (location.protocol === 'http:' || location.protocol === 'https:') {
      const ticket = ++generation;
      loadHosted(config.url, config.required, window.fetch.bind(window))
        .then(rows => { if (ticket === generation) show(rows); })
        .catch(() => { if (ticket === generation) fallback('Open the local slots file if you are offline.'); });
    }
  }
  return {readSlots: readSlots, loadHosted: loadHosted, loadFile: loadFile, mount: mount};
}));
