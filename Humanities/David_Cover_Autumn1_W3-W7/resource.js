'use strict';
// Responses are deliberately ephemeral. This page has no storage or network calls.
const deck = document.querySelector('[data-lesson-deck]');
if (deck) {
  const stages = [...deck.querySelectorAll('[data-stage]')];
  const nav = document.querySelector('.stage-nav');
  const previous = nav.querySelector('[data-prev]');
  const next = nav.querySelector('[data-next]');
  const select = nav.querySelector('select');
  const status = nav.querySelector('.stage-status');
  let current = 0;
  function show(index, focus = false) {
    current = Math.max(0, Math.min(stages.length - 1, index));
    for (const [i, stage] of stages.entries()) stage.hidden = i !== current;
    previous.disabled = current === 0;
    next.disabled = current === stages.length - 1;
    select.value = String(current);
    status.textContent = `Stage ${current + 1} of ${stages.length} · ${stages[current].dataset.minutes} minutes · 40 minutes in total`;
    if (focus) stages[current].querySelector('h2').focus({preventScroll: false});
  }
  previous.addEventListener('click', () => show(current - 1, true));
  next.addEventListener('click', () => show(current + 1, true));
  select.addEventListener('change', () => show(Number(select.value), true));
  document.addEventListener('keydown', event => {
    if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    if (event.target.closest('input,textarea,select,summary,[contenteditable=true]')) return;
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      show(current + (event.key === 'ArrowRight' ? 1 : -1), true);
    }
  });
  nav.hidden = false;
  show(0);
}
