/* Native controls only; no network, persistence, timers or focus trap. */
(function () {
  'use strict';
  function mount(root) {
    if (root.dataset.activityReady) return;
    const status = root.querySelector('.mbm-act-status');
    const rows = Array.from(root.querySelectorAll('[data-activity-row]'));
    const actions = root.querySelectorAll('[data-activity-action]');
    const explanations = root.querySelector('.mbm-act-explanations');
    const explainButton = root.querySelector('[data-activity-action="explain"]');
    let data;
    try {
      data = JSON.parse(root.querySelector('[data-activity-data]').textContent);
      if (!['sort', 'match', 'choice', 'order'].includes(data.mode)
          || data.items.length !== rows.length || !rows.length) throw new Error('shape');
      data.items.forEach(function (item, i) {
        const controls = Array.from(rows[i].querySelectorAll('option, input[type="radio"]'));
        if (typeof item.answer !== 'string' || !controls.some(node => node.value === item.answer)) throw new Error('answer');
      });
    } catch (_) {
      status.textContent = 'This activity could not load. Use the printed task or discuss the questions with your teacher.';
      actions.forEach(button => { button.disabled = true; });
      root.dataset.activityReady = 'error';
      return;
    }
    root.dataset.activityReady = 'true';
    function selected(row) {
      const select = row.querySelector('select');
      const radio = row.querySelector('input[type="radio"]:checked');
      return select ? select.value : (radio ? radio.value : '');
    }
    function clearFeedback() {
      rows.forEach(function (row) {
        row.querySelector('.mbm-act-row-feedback').textContent = '';
        row.removeAttribute('data-check');
      });
    }
    root.addEventListener('change', function (event) {
      if (!event.target.matches('select, input[type="radio"]')) return;
      clearFeedback();
      status.textContent = 'Choice changed. Use Check choices when you are ready.';
    });
    root.addEventListener('click', function (event) {
      const button = event.target.closest('[data-activity-action]');
      if (!button || !root.contains(button)) return;
      const action = button.dataset.activityAction;
      if (action === 'retry') {
        root.querySelectorAll('select').forEach(select => { select.value = ''; });
        root.querySelectorAll('input[type="radio"]').forEach(input => { input.checked = false; });
        clearFeedback();
        explanations.hidden = true;
        explainButton.setAttribute('aria-expanded', 'false');
        explainButton.textContent = 'Show explanations';
        status.textContent = 'Choices cleared. Try again, or discuss a question with a partner.';
        const first = rows[0].querySelector('select, input[type="radio"]');
        if (first) first.focus();
      } else if (action === 'explain') {
        explanations.hidden = !explanations.hidden;
        explainButton.setAttribute('aria-expanded', String(!explanations.hidden));
        explainButton.textContent = explanations.hidden ? 'Show explanations' : 'Hide explanations';
        status.textContent = explanations.hidden ? 'Model explanations hidden.' : 'Model explanations shown below. Compare the reasons with your own.';
      } else if (action === 'check') {
        const values = rows.map(selected);
        const duplicates = data.mode === 'order'
          ? values.filter((v, i) => v && values.indexOf(v) !== i) : [];
        let missing = false, revisit = false;
        rows.forEach(function (row, i) {
          let text, result;
          if (!values[i]) {
            text = 'Choose a response, or point to your choice with a partner.';
            result = 'missing'; missing = true;
          } else if (duplicates.includes(values[i])) {
            text = 'This position is used more than once. Give each note a different position.';
            result = 'review'; revisit = true;
          } else if (values[i] === data.items[i].answer) {
            text = 'Matches the model. Can you explain your choice?'; result = 'match';
          } else {
            text = 'Compare your reason with the model explanation, then keep or change your choice.';
            result = 'review'; revisit = true;
          }
          row.querySelector('.mbm-act-row-feedback').textContent = text;
          row.dataset.check = result;
        });
        status.textContent = missing
          ? 'Some choices are still blank. Choose, point or discuss; then check again.'
          : revisit
            ? 'Some choices differ from the model. Read the explanations and discuss your reasons.'
            : 'Your choices match the model. Explain one, then use the idea in your own work.';
      }
    });
  }
  function boot() {
    document.querySelectorAll('[data-mbm-activity]').forEach(mount);
    const deck = document.querySelector('main.deck');
    const toolbar = document.querySelector('.controls');
    if (!deck || !toolbar || !deck.querySelector('[data-mbm-activity]')) return;
    // Wrapped toolbar rows can be taller than the donor's fixed allowance.
    // Reserve their actual height so the last response can scroll clear.
    const reserve = function () {
      const space = Math.max(0, window.innerHeight - toolbar.getBoundingClientRect().top) + 18;
      deck.style.paddingBottom = space + 'px';
      deck.style.scrollPaddingBottom = space + 'px';
    };
    reserve();
    window.addEventListener('resize', reserve);
    if (window.ResizeObserver) new ResizeObserver(reserve).observe(toolbar);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot, {once: true});
  else boot();
}());
