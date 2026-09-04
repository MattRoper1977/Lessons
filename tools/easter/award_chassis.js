/* Runtime for newly authored award decks; no persistence or external dependencies. */
(function () {
  'use strict';

  function boot() {
    const deck = document.querySelector('main.deck');
    const slides = Array.from(document.querySelectorAll('main.deck > .slide'));
    if (!deck || !slides.length) return;
    const progress = document.querySelector('.prog');
    const bar = document.querySelector('.prog > span');
    const overlay = document.getElementById('taOverlay');
    const card = overlay && overlay.querySelector('.overlay-card');
    const closeButton = overlay && overlay.querySelector('[data-close-overlay]');
    const teacherButtons = document.querySelectorAll('[data-tool="1"]');
    let index = Math.max(0, slides.findIndex(slide => slide.classList.contains('active')));
    let returnFocus = null;
    let notes = null;
    let slotHost = null;

    function show(next) {
      index = (next + slides.length) % slides.length;
      slides.forEach(function (slide, i) {
        slide.classList.toggle('active', i === index);
        slide.setAttribute('aria-hidden', i === index ? 'false' : 'true');
      });
      if (bar) bar.style.width = ((index + 1) / slides.length * 100) + '%';
      if (progress) {
        progress.removeAttribute('aria-hidden');
        progress.setAttribute('role', 'progressbar');
        progress.setAttribute('aria-label', 'Lesson progress');
        progress.setAttribute('aria-valuemin', '1');
        progress.setAttribute('aria-valuemax', String(slides.length));
        progress.setAttribute('aria-valuenow', String(index + 1));
        progress.setAttribute('aria-valuetext', 'Stage ' + (index + 1) + ' of ' + slides.length);
      }
      deck.scrollTop = 0;
    }

    function isOpen() {
      return Boolean(overlay && overlay.classList.contains('on'));
    }

    function fillNotes() {
      notes.replaceChildren();
      const heading = document.createElement('h3');
      heading.textContent = slides[index].dataset.title || 'Current stage';
      notes.appendChild(heading);
      ['ta1', 'ta2'].forEach(function (key) {
        const text = slides[index].dataset[key];
        if (!text) return;
        const paragraph = document.createElement('p');
        paragraph.textContent = text;
        notes.appendChild(paragraph);
      });
      const sources = index === 0 ? [slides[0]] : [slides[index], slides[0]];
      sources.forEach(function (source) {
        source.querySelectorAll('[data-mbm-guide]').forEach(function (note) {
          // The slot reader has its own live state and file listener: never clone it.
          if (note.id === 'award-slot-panel' || note.closest('#award-slot-panel')) return;
          const copy = note.cloneNode(true);
          copy.removeAttribute('id');
          copy.querySelectorAll('[id]').forEach(node => node.removeAttribute('id'));
          notes.appendChild(copy);
        });
      });
      // mount() runs on DOMContentLoaded. A real click comes after that event,
      // regardless of the order in which the two embedded scripts were loaded.
      const panel = document.getElementById('award-slot-panel');
      if (panel && !slotHost.contains(panel)) slotHost.appendChild(panel);
    }

    function openTeacher(button) {
      if (!card || isOpen()) return;
      returnFocus = button || document.activeElement;
      fillNotes();
      overlay.classList.add('on');
      overlay.setAttribute('aria-hidden', 'false');
      teacherButtons.forEach(node => node.setAttribute('aria-expanded', 'true'));
      (closeButton || card).focus();
    }

    function closeTeacher() {
      if (!isOpen()) return;
      overlay.classList.remove('on');
      overlay.setAttribute('aria-hidden', 'true');
      teacherButtons.forEach(node => node.setAttribute('aria-expanded', 'false'));
      if (returnFocus && returnFocus.isConnected) returnFocus.focus();
    }

    function focusable() {
      return Array.from(card.querySelectorAll('a[href], button, input, select, textarea, [tabindex]'))
        .filter(node => !node.disabled && node.tabIndex >= 0 && node.getClientRects().length);
    }

    if (card) {
      overlay.setAttribute('role', 'dialog');
      overlay.setAttribute('aria-modal', 'true');
      overlay.setAttribute('aria-hidden', 'true');
      overlay.classList.remove('on');
      card.tabIndex = -1;
      let title = card.querySelector('h2');
      if (!title) {
        title = document.createElement('h2');
        card.prepend(title);
      }
      title.id = 'award-teacher-title';
      title.textContent = 'Teacher tools';
      overlay.setAttribute('aria-labelledby', title.id);
      notes = document.createElement('div');
      notes.id = 'award-teacher-notes';
      slotHost = document.createElement('div');
      slotHost.id = 'award-teacher-slots';
      card.insertBefore(notes, closeButton);
      card.insertBefore(slotHost, closeButton);
      if (closeButton) closeButton.addEventListener('click', closeTeacher);
      teacherButtons.forEach(function (button) {
        button.setAttribute('aria-controls', overlay.id);
        button.setAttribute('aria-expanded', 'false');
        button.addEventListener('click', () => openTeacher(button));
      });
      // Keep focus in the open dialog, including when scripts attempt to move it.
      document.addEventListener('focusin', function (event) {
        if (isOpen() && !overlay.contains(event.target)) (closeButton || card).focus();
      });
    }

    document.querySelectorAll('[data-nav="previous"], [data-tool="5"]')
      .forEach(button => button.addEventListener('click', () => { if (!isOpen()) show(index - 1); }));
    document.querySelectorAll('[data-nav="next"], [data-tool="6"]')
      .forEach(button => button.addEventListener('click', () => { if (!isOpen()) show(index + 1); }));
    document.querySelectorAll('[data-tool="2"]')
      .forEach(button => button.addEventListener('click', () => window.print()));
    [['3', 'calm'], ['4', 'teacher-freeze']].forEach(function (item) {
      const buttons = document.querySelectorAll('[data-tool="' + item[0] + '"]');
      function sync() {
        const active = document.body.classList.contains(item[1]);
        buttons.forEach(button => button.setAttribute('aria-pressed', String(active)));
      }
      buttons.forEach(button => button.addEventListener('click', function () {
        document.body.classList.toggle(item[1]);
        sync();
      }));
      sync();
    });

    document.addEventListener('keydown', function (event) {
      if (isOpen()) {
        if (event.key === 'Escape') {
          event.preventDefault();
          closeTeacher();
        } else if (event.key === 'Tab') {
          const items = focusable();
          const first = items[0] || card;
          const last = items[items.length - 1] || card;
          if (!items.length || !items.includes(document.activeElement)
              || (event.shiftKey && document.activeElement === first)
              || (!event.shiftKey && document.activeElement === last)) {
            event.preventDefault();
            (event.shiftKey ? last : first).focus();
          }
        }
        return;
      }
      const target = event.target;
      if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey
          || (target && (target.isContentEditable
              || (typeof target.closest === 'function' && target.closest('input, textarea, select'))))
          || document.querySelector('dialog[open], .overlay.on, [role="dialog"][aria-hidden="false"]')) return;
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault();
        show(index + (event.key === 'ArrowRight' ? 1 : -1));
      }
    });
    show(index);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot, {once: true});
  else boot();
}());
