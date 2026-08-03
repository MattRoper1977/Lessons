#!/usr/bin/env python3
from __future__ import annotations

# Branch synchronisation marker: the publication gate removes this temporary script.
from pathlib import Path

JS_PATH = Path('BUILD_ASDAN/_framework/asdan-teach.js')
README_PATH = Path('BUILD_ASDAN/_framework/README.md')
MARKER = 'function atProtectLoopLabels(block)'

FUNCTION = r'''
  /* Keep words readable when a diagram uses a pulsing glow on a group that
     contains both a shape and its text label. The pulse moves to the visual
     branches only; the exact authored label remains inside the finite build. */
  function atProtectLoopLabels(block) {
    if (!block || block.getAttribute('data-at-loop-labels') === 'ready') return;
    block.setAttribute('data-at-loop-labels', 'ready');

    block.querySelectorAll('.glow').forEach(function (loop) {
      var labels = loop.querySelectorAll ? loop.querySelectorAll('text') : [];
      if (!labels.length) return;

      var delay = getComputedStyle(loop).animationDelay || '';
      loop.classList.remove('glow');

      Array.prototype.forEach.call(loop.children || [], function (child) {
        var tag = (child.tagName || '').toLowerCase();
        if (tag === 'text' || (child.querySelector && child.querySelector('text'))) return;
        child.classList.add('glow', 'at-label-safe-glow');
        if (delay && delay !== '0s') child.style.animationDelay = delay;
      });
    });
  }

'''


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected one signature, found {count}')
    return text.replace(old, new, 1)


def main() -> None:
    js = JS_PATH.read_text(encoding='utf-8')
    if MARKER in js:
        raise SystemExit('Loop-label protection already present')

    js = replace_once(
        js,
        '  function atClassifyIlluminatorMotion(block) {\n',
        FUNCTION + '  function atClassifyIlluminatorMotion(block) {\n',
        'motion classifier insertion',
    )
    js = replace_once(
        js,
        """    document.querySelectorAll('.ilm').forEach(function (block) {\n      atEnsureMotionSweep(block);\n      atClassifyIlluminatorMotion(block);\n""",
        """    document.querySelectorAll('.ilm').forEach(function (block) {\n      atEnsureMotionSweep(block);\n      atProtectLoopLabels(block);\n      atClassifyIlluminatorMotion(block);\n""",
        'motion setup hook',
    )
    JS_PATH.write_text(js, encoding='utf-8')

    readme = README_PATH.read_text(encoding='utf-8')
    old = (
        '- In diagrams that combine a staged build with decorative glow or ripple, those\n'
        '  decorative loops settle after the teaching window. The four loop-only concept\n'
        '  diagrams remain continuous because their cycle carries the meaning.\n'
    )
    new = (
        '- In diagrams that combine a staged build with decorative glow or ripple, those\n'
        '  decorative loops settle after the teaching window. The four loop-only concept\n'
        '  diagrams remain continuous because their cycle carries the meaning.\n'
        '- When a pulsing glow contains a written SVG label, only the visual shape pulses;\n'
        '  the exact authored label remains at full opacity throughout the cycle.\n'
    )
    readme = replace_once(readme, old, new, 'README motion note')
    README_PATH.write_text(readme, encoding='utf-8')
    print('Patched loop-label protection for pulsing SVG groups')


if __name__ == '__main__':
    main()
