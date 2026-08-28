#!/usr/bin/env python3
"""N6-F §F1 — prove `s24-print-renders` red. A gate never seen red is not evidence.

Two perturbations, one per defect the gate was written for. Each is applied to a
throwaway copy of a known-good deck; the repository tree is never modified.

  A · the learner-confirmation block is moved out of `.print-pack` and appended
      before `</body>` — exactly the placement the August run shipped. The block
      is still in the file and a grep still finds it; the container's
      `body>*:not(.print-pack){display:none!important}` keeps it off the paper.

  B · the LAUNCH print block's height overrides are removed, so the SCREEN
      heights survive onto paper — `.deck` at 92vh, `.slide` at `height:91%`.
      That is the shipped defect: the donor still reveals all nine slides, so
      every `@media print` presence check passes, and the deck emits a sheet
      carrying an empty bordered box. Note what that page looks like to a
      measurement: zero characters, but ~0.7% ink from the border. An ink-only
      threshold calls it a working page. This perturbation is the reason the
      blank test is an OR.

Usage: n6_s24_redproof.py [outfile.md]
"""
import os, sys, re, shutil, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gates as G

BUILD_DECK = 'BUILD_ASDAN/Autumn2_W1-W6_2026-27/BUILD_ASDAN_A2_CON_W1_Materials_Tools_and_Safety.html'
LAUNCH_DIR = 'LAUNCH_ASDAN/W7-W12_2026-27'

OPEN, CLOSE = '<!--n6-learner-confirm:v1-->', '<!--/n6-learner-confirm-->'


def run(files, label):
    name, ok, detail, rows = G.g11_print_renders(files)
    tag = 'PASS' if ok else ('INVALID' if ok is None else 'FAIL')
    out = ['%-8s %s' % (tag, label), '         %s' % detail]
    for r in rows[:6]:
        out.append('         · %s' % ' | '.join(str(x) for x in r))
    if len(rows) > 6:
        out.append('         · ... %d more' % (len(rows) - 6))
    return ok, '\n'.join(out)


def perturb_a(tmp):
    """Move the confirmation block out of .print-pack, back before </body>."""
    p = os.path.join(tmp, os.path.basename(BUILD_DECK))
    shutil.copy(os.path.join(ROOT, BUILD_DECK), p)
    s = open(p, encoding='utf-8').read()
    i = s.find(OPEN)
    j = s.index(CLOSE, i) + len(CLOSE)
    blk = s[i:j]
    s = s[:i] + s[j:]
    s = s.replace('</body>', blk + '</body>', 1)
    open(p, 'w', encoding='utf-8').write(s)
    return [p]


DECK_H = '.deck{height:auto!important;display:block!important;padding:0!important}'
SLIDE_H = ('.slide{height:auto!important;min-height:0!important;'
           'overflow:visible!important;display:block!important;'
           'border-radius:0;box-shadow:none}')
BODY_H = 'html,body{overflow:visible!important;height:auto!important}'


def perturb_b(tmp):
    """Put the blank-sheet bug back into one LAUNCH deck."""
    src = None
    for d, _, fs in os.walk(os.path.join(ROOT, LAUNCH_DIR)):
        for f in fs:
            q = os.path.join(d, f)
            if f.endswith('.html') and OPEN in open(q, encoding='utf-8', errors='ignore').read():
                src = q
                break
        if src:
            break
    p = os.path.join(tmp, os.path.basename(src))
    shutil.copy(src, p)
    s = open(p, encoding='utf-8').read()
    for frag in (DECK_H, SLIDE_H, BODY_H):
        if frag not in s:
            raise SystemExit('perturb B: expected fragment absent in %s:\n  %s'
                             % (src, frag[:70]))
    s = s.replace(DECK_H, '.deck{display:block!important;padding:0!important}', 1)
    s = s.replace(SLIDE_H, '.slide{display:block!important;border-radius:0;'
                           'box-shadow:none}', 1)
    s = s.replace(BODY_H, 'html,body{overflow:visible!important}', 1)
    open(p, 'w', encoding='utf-8').write(s)
    return [p]


def main():
    lines = ['# s24-print-renders — red-proof', '',
             'Both perturbations are applied to throwaway copies. The repository tree',
             'is not modified by this script.', '']
    overall_ok = True

    clean_build = [os.path.join(ROOT, BUILD_DECK)]
    ok, txt = run(clean_build, 'baseline · the unperturbed deck')
    lines += ['## Baseline', '', '```', txt, '```', '']
    if ok is not True:
        overall_ok = False
        lines.append('> BASELINE DID NOT PASS — the red-proof proves nothing. Stop.')

    for label, fn, expect in (
            ('A · confirmation block moved outside `.print-pack`', perturb_a,
             'CONFIRMATION BLOCK NOT ON PAPER'),
            ('B · print height overrides removed, `.slide` back at `height:91%`',
             perturb_b, 'BLANK PAGE')):
        tmp = tempfile.mkdtemp(prefix='s24-red-')
        try:
            files = fn(tmp)
            ok, txt = run(files, label)
            hit = expect in txt
            lines += ['## Perturbation %s' % label, '', '```', txt, '```', '',
                      '- gate result: **%s**' % ('RED (correct)' if ok is False else
                                                 'GREEN — THE GATE MISSED IT'),
                      '- names the defect (`%s`): **%s**' % (expect, 'yes' if hit else 'NO'),
                      '- names the file: **%s**' % ('yes' if os.path.basename(files[0]) in txt else 'NO'),
                      '']
            if ok is not False or not hit:
                overall_ok = False
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    verdict = ('Gate passes clean and fails on both defects it was written for.'
               if overall_ok else 'RED-PROOF FAILED — the gate is not trustworthy.')
    lines += ['## Verdict', '', verdict, '']
    out = '\n'.join(lines)
    print(out)
    if len(sys.argv) > 1:
        open(sys.argv[1], 'w', encoding='utf-8').write(out)
    return 0 if overall_ok else 1


if __name__ == '__main__':
    sys.exit(main())
