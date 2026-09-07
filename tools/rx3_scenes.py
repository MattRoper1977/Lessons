#!/usr/bin/env python3
"""RX3 R1 — deterministic flat SVG scenes for the BUILD Humanities belonging lesson ("A place in the group").

Replaces the AI photoreal composite (four imagined school groups) with four authored flat scenes in one
2×2 card, no faces: every figure is a simple rounded silhouette. Output is a single SVG ≤40 KB whose four
panels are labelled exactly as the lesson's caption labels them (top left: our class · top right: football
team · bottom left: garden group · bottom right: games club). Alt text (returned by alt()) says what each
scene shows and what the pupil must decide from it.

Usage: rx3_scenes.py [--out file.svg] [--datauri]   (prints size and the alt text)
"""
import sys,html,urllib.parse
W,H=1200,800
def fig(x,y,body,head,scale=1.0,pose='stand'):
    # rounded silhouette: head circle + body capsule; no facial features by design
    s=scale
    parts=[f'<circle cx="{x}" cy="{y-46*s:.0f}" r="{16*s:.0f}" fill="{head}"/>',
           f'<rect x="{x-18*s:.0f}" y="{y-28*s:.0f}" width="{36*s:.0f}" height="{56*s:.0f}" rx="{14*s:.0f}" fill="{body}"/>']
    if pose=='sit': parts.append(f'<rect x="{x-20*s:.0f}" y="{y+24*s:.0f}" width="{40*s:.0f}" height="{10*s:.0f}" rx="5" fill="{body}"/>')
    else: parts+= [f'<rect x="{x-14*s:.0f}" y="{y+26*s:.0f}" width="{11*s:.0f}" height="{30*s:.0f}" rx="5" fill="{head}"/>',f'<rect x="{x+3*s:.0f}" y="{y+26*s:.0f}" width="{11*s:.0f}" height="{30*s:.0f}" rx="5" fill="{head}"/>']
    return ''.join(parts)
SKIN=['#c68642','#8d5524','#e0ac69','#f1c27d','#5a3a1e']
def panel(x0,y0,title,bg,content):
    return (f'<g transform="translate({x0},{y0})"><rect x="8" y="8" width="{W//2-16}" height="{H//2-16}" rx="22" fill="{bg}" stroke="#1f2937" stroke-width="3"/>'
            f'<rect x="8" y="8" width="{W//2-16}" height="54" rx="22" fill="#1f2937"/><rect x="8" y="40" width="{W//2-16}" height="22" fill="#1f2937"/>'
            f'<text x="{W//4}" y="46" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="30" font-weight="700" fill="#fff">{html.escape(title)}</text>{content}</g>')
def classroom():
    c=['<rect x="120" y="230" width="360" height="26" rx="8" fill="#b45309"/><rect x="140" y="256" width="18" height="90" fill="#92400e"/><rect x="442" y="256" width="18" height="90" fill="#92400e"/>']
    for i,(bx,col) in enumerate([(160,'#2563eb'),(230,'#16a34a'),(300,'#dc2626'),(370,'#7c3aed')]):
        c.append(f'<rect x="{bx}" y="206" width="52" height="34" rx="4" fill="{col}"/><rect x="{bx+6}" y="212" width="40" height="4" fill="#fff" opacity=".8"/><rect x="{bx+6}" y="222" width="30" height="4" fill="#fff" opacity=".8"/>')
    for i,x in enumerate([180,260,340,420]): c.append(fig(x,300,['#1d4ed8','#0f766e','#b91c1c','#6d28d9'][i],SKIN[i],pose='sit'))
    c.append('<rect x="60" y="90" width="470" height="90" rx="10" fill="#fff" stroke="#94a3b8" stroke-width="3"/><text x="295" y="145" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="26" fill="#334155">Learning together</text>')
    return ''.join(c)
def football():
    c=['<rect x="20" y="230" width="560" height="150" rx="16" fill="#4ade80"/><rect x="60" y="250" width="480" height="4" fill="#fff" opacity=".8"/><rect x="298" y="250" width="4" height="110" fill="#fff" opacity=".8"/>',
       '<rect x="470" y="200" width="90" height="70" fill="none" stroke="#fff" stroke-width="6"/><line x1="470" y1="270" x2="560" y2="200" stroke="#fff" stroke-width="3" opacity=".7"/><line x1="470" y1="200" x2="560" y2="270" stroke="#fff" stroke-width="3" opacity=".7"/>']
    for i,x in enumerate([110,210,320]): c.append(fig(x,280,'#f97316',SKIN[(i+1)%5]))
    c.append(fig(420,285,'#fde047',SKIN[3]))
    c.append('<circle cx="380" cy="352" r="16" fill="#fff" stroke="#1f2937" stroke-width="4"/><path d="M372 344 l8 6 l8 -6 l-3 10 l-10 0 z" fill="#1f2937"/>')
    return ''.join(c)
def garden():
    c=['<rect x="30" y="250" width="540" height="130" rx="14" fill="#a16207"/><rect x="30" y="250" width="540" height="18" fill="#78350f"/>']
    for i,x in enumerate([90,170,250,330,410,490]):
        c.append(f'<rect x="{x-3}" y="{190+ (i%2)*20}" width="6" height="{80-(i%2)*20}" fill="#15803d"/><ellipse cx="{x-18}" cy="{220+(i%2)*20}" rx="18" ry="9" fill="#22c55e" transform="rotate(-30 {x-18} {220+(i%2)*20})"/><ellipse cx="{x+18}" cy="{235+(i%2)*20}" rx="18" ry="9" fill="#22c55e" transform="rotate(30 {x+18} {235+(i%2)*20})"/>')
        if i%3==0: c.append(f'<circle cx="{x}" cy="{186+(i%2)*20}" r="12" fill="#f43f5e"/>')
    c.append(fig(130,330,'#0ea5e9',SKIN[4],pose='sit')); c.append(fig(300,330,'#a21caf',SKIN[0],pose='sit')); c.append(fig(470,330,'#0d9488',SKIN[2],pose='sit'))
    c.append('<path d="M360 300 h60 v40 h-60 z M420 310 h22 v10 h-22 z" fill="#64748b"/><rect x="368" y="292" width="44" height="10" rx="4" fill="#94a3b8"/>')
    return ''.join(c)
def games():
    c=['<rect x="110" y="240" width="380" height="24" rx="8" fill="#7c2d12"/><rect x="130" y="264" width="16" height="90" fill="#431407"/><rect x="454" y="264" width="16" height="90" fill="#431407"/>',
       '<rect x="200" y="196" width="200" height="50" rx="6" fill="#fef3c7" stroke="#92400e" stroke-width="3"/>']
    for r in range(2):
        for k in range(6): c.append(f'<rect x="{208+k*32}" y="{204+r*22}" width="26" height="16" rx="3" fill="{["#dc2626","#2563eb","#16a34a","#f59e0b","#7c3aed","#0891b2"][(k+r)%6]}"/>')
    for i,x in enumerate([150,300,450]): c.append(fig(x,300,['#be123c','#1d4ed8','#047857'][i],SKIN[(i*2)%5],pose='sit'))
    c.append('<circle cx="330" cy="176" r="14" fill="#fff" stroke="#1f2937" stroke-width="3"/><circle cx="325" cy="171" r="3" fill="#1f2937"/><circle cx="335" cy="181" r="3" fill="#1f2937"/>')
    return ''.join(c)
def build():
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="rx3t"><title id="rx3t">{html.escape(alt())}</title>'
            f'<rect width="{W}" height="{H}" fill="#f8fafc"/>'
            + panel(0,0,'Our class · learning together','#dbeafe',classroom()) + panel(W//2,0,'Football team · practice','#dcfce7',football())
            + panel(0,H//2,'Garden group · growing plants','#fef9c3',garden()) + panel(W//2,H//2,'Games club · a table game','#fae8ff',games()) + '</svg>')
def alt():
    return ('Four flat illustrated scenes of imagined school groups, no real pupils: top left, a class learning together at a table with books; '
            'top right, a football team practising on a pitch with a goal and a ball; bottom left, a garden group planting and watering in a raised bed; '
            'bottom right, a games club playing a table game with counters and a dice. Decide which group each activity belongs to, and which group you would join.')
if __name__=='__main__':
    svg=build(); out=None; uri='--datauri' in sys.argv
    if '--out' in sys.argv: out=sys.argv[sys.argv.index('--out')+1]; open(out,'w',encoding='utf-8').write(svg)
    data='data:image/svg+xml;charset=utf-8,'+urllib.parse.quote(svg,safe="-_.~ :/?#[]@!$&'()*+,;=")
    print('svg bytes',len(svg.encode()),'| data-uri chars',len(data),'| <=40KB:',len(svg.encode())<=40960); print('ALT:',alt())
    if uri: print(data)
