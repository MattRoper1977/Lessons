/* Offline pack navigation adapter. The bundled Site hud.js remains byte-exact.
   Loaded immediately after that HUD using ordered defer scripts. */
(function () {
  'use strict';
  var script = document.currentScript;
  if (!script || !script.src) return;
  var back = document.getElementById('mbmhud-back');
  if (back) {
    back.setAttribute('href', new URL('Lessons/index.html', script.src).href);
    back.textContent = '← Downloaded lessons';
    back.setAttribute('aria-label', 'Back to this downloaded lesson pack');
  }
  var home = document.getElementById('mbmhud-home');
  if (home) {
    var target = home.getAttribute('href') || '';
    if (target.charAt(0) === '/' && target.charAt(1) !== '/') {
      home.setAttribute('href', 'https://madebymatt.uk' + target);
      home.setAttribute('title', (home.getAttribute('title') || 'Your homepage') + ' (online; needs internet)');
      home.setAttribute('aria-label', (home.getAttribute('aria-label') || 'Your homepage') + ' (online; needs internet)');
      var caption = home.querySelector('span');
      if (caption) caption.textContent += ' · online';
    }
  }
}());
