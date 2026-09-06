#!/usr/bin/env python3
"""R4 (VB-RUN11F): fix the STATE, not the CSS. printPack(level) = printArm(level) + window.print();
on load and on beforeprint, if no tier is armed, arm the default (Standard). Print CSS is untouched.
Usage: r4_patch.py <deck> [<deck> ...]   (refuses a deck whose printPack does not end in a single window.print())"""
import re, sys, pathlib
MARK = '/* R4 default-Standard */'
for p in sys.argv[1:]:
    path = pathlib.Path(p); s = path.read_text(encoding='utf-8')
    if MARK in s: print('already', p); continue
    m = re.search(r'function printPack\(level\)\{(.*?)window\.print\(\)\}', s, re.S)
    if not m or 'window.print()' in m.group(1) or 'function ' in m.group(1):
        print('HELD (mechanism differs)', p); continue
    r4 = ("function printArm(level){" + m.group(1) + "}"
          "function printPack(level){printArm(level);window.print()}"
          "(function(){function armed(){return /\\bprint-(supported|standard|stretch)\\b/.test(document.body.className)}"
          "function r4(){if(!armed())printArm('standard')}window.addEventListener('beforeprint',r4);"
          "if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',r4);else r4();})();" + MARK)
    s = s[:m.start()] + r4 + s[m.end():]
    path.write_text(s, encoding='utf-8'); print('patched', p)
